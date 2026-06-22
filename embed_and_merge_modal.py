"""Embed and semantically merge structural chunks on a Modal T4 GPU.

The local entrypoint reads processed/chunks.json and writes both a clean JSON file
and a local-only JSON file containing embeddings. Model loading, embedding, token
counting, and semantic merging run inside the Modal function.
"""

from __future__ import annotations

import json
import math
import sys
import time
from collections import OrderedDict
from copy import deepcopy
from pathlib import Path
from typing import Any, Sequence

import modal


APP_NAME = "hackathon-embedding"
MODEL_NAME = "Qwen/Qwen3-Embedding-0.6B"
CHUNKS_PATH = Path("processed/chunks.json")
EMBEDDINGS_PATH = Path("processed/chunks.embeddings.json")
SMOKE_TEST_CLEAN_PATH = Path("processed/chunks.modal-smoke-test.json")
SMOKE_TEST_EMBEDDINGS_PATH = Path(
    "processed/chunks.modal-smoke-test.embeddings.json"
)
SEMANTIC_MERGE_THRESHOLD = 0.75
MAX_TOKENS = 720
HARD_BOUNDARY_TYPES = {"detail", "row", "comment"}
EMBEDDING_BATCH_SIZE = 32
MERGE_EXAMPLE_COUNT = 5

Chunk = dict[str, Any]
Embedding = Sequence[float]

app = modal.App(APP_NAME)
image = modal.Image.debian_slim().pip_install(
    "sentence-transformers==5.6.0",
    "transformers==5.12.1",
    "torch",
)


def safe_print(text: str = "") -> None:
    """Print safely on Windows consoles that are not UTF-8."""
    encoding = sys.stdout.encoding or "utf-8"
    sys.stdout.write(text.encode(encoding, errors="replace").decode(encoding) + "\n")


def validate_structural_chunks(chunks: object) -> list[Chunk]:
    """Validate the local JSON before sending it to Modal."""
    if not isinstance(chunks, list) or not chunks:
        raise ValueError("Expected a non-empty JSON list of structural chunks.")

    required_fields = {
        "chunk_id",
        "text",
        "source_file",
        "source_filename",
        "source_type",
        "section_title",
        "block_types",
        "chunk_position",
        "token_count",
        "char_start",
        "char_end",
    }
    invalid_chunks: list[str] = []
    embedded_chunks: list[str] = []

    for index, chunk in enumerate(chunks):
        if not isinstance(chunk, dict) or not required_fields.issubset(chunk):
            chunk_id = chunk.get("chunk_id", f"index {index}") if isinstance(chunk, dict) else index
            invalid_chunks.append(str(chunk_id))
            continue
        if "embedding" in chunk:
            embedded_chunks.append(str(chunk["chunk_id"]))

    if invalid_chunks:
        examples = ", ".join(invalid_chunks[:5])
        raise ValueError(
            "Chunks are missing required structural metadata, including block_types "
            f"({examples}). Regenerate them with build_chunks.py first."
        )
    if embedded_chunks:
        examples = ", ".join(embedded_chunks[:5])
        raise ValueError(
            "The input already contains embeddings "
            f"({examples}). Regenerate structural chunks with build_chunks.py before rerunning."
        )

    return chunks


def cosine_similarity(left: Embedding, right: Embedding) -> float:
    dot_product = sum(float(a) * float(b) for a, b in zip(left, right, strict=True))
    left_norm = math.sqrt(sum(float(value) ** 2 for value in left))
    right_norm = math.sqrt(sum(float(value) ** 2 for value in right))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return dot_product / (left_norm * right_norm)


def has_hard_boundary(chunk: Chunk) -> bool:
    block_types = {str(block_type) for block_type in chunk.get("block_types", [])}
    return bool(block_types & HARD_BOUNDARY_TYPES)


def combine_unique(left: Sequence[str], right: Sequence[str]) -> list[str]:
    return list(dict.fromkeys([*left, *right]))


def combine_section_titles(left: object, right: object) -> str | None:
    titles = [str(title).strip() for title in (left, right) if title and str(title).strip()]
    unique_titles = list(dict.fromkeys(titles))
    return " | ".join(unique_titles) if unique_titles else None


def group_chunk_indexes(chunks: list[Chunk]) -> OrderedDict[str, list[int]]:
    grouped: OrderedDict[str, list[int]] = OrderedDict()
    for index, chunk in enumerate(chunks):
        source_file = str(chunk["source_file"])
        grouped.setdefault(source_file, []).append(index)

    for indexes in grouped.values():
        indexes.sort(key=lambda index: int(chunks[index]["chunk_position"]))
    return grouped


def reassign_chunk_ids(chunks: list[Chunk]) -> None:
    source_counts: dict[str, int] = {}
    source_prefixes: dict[str, str] = {}

    for chunk in chunks:
        source_file = str(chunk["source_file"])
        source_counts[source_file] = source_counts.get(source_file, 0) + 1
        source_prefixes.setdefault(source_file, str(chunk["chunk_id"]).rsplit("_", 1)[0])
        chunk["chunk_id"] = (
            f"{source_prefixes[source_file]}_{source_counts[source_file]:04d}"
        )


@app.function(gpu="T4", image=image, timeout=600)
def embed_and_merge(structural_chunks: list[Chunk]) -> dict[str, Any]:
    """Embed, semantically merge, and selectively re-embed chunks on Modal."""
    import torch
    from sentence_transformers import SentenceTransformer
    from transformers import AutoTokenizer

    started_at = time.perf_counter()
    if not torch.cuda.is_available():
        raise RuntimeError("Modal did not provide a CUDA GPU to the embedding function.")

    chunks = validate_structural_chunks(structural_chunks)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = SentenceTransformer(MODEL_NAME, device="cuda")

    def count_tokens(text: str) -> int:
        return len(tokenizer.encode(text))

    def embed_texts(texts: list[str]) -> list[Embedding]:
        if not texts:
            return []

        # No prompt or prompt_name: these are document embeddings, not queries.
        encoded = model.encode(
            texts,
            batch_size=EMBEDDING_BATCH_SIZE,
            show_progress_bar=True,
            convert_to_numpy=True,
        )
        return [embedding for embedding in encoded]

    def merge_chunks(left: Chunk, right: Chunk, merged_text: str) -> Chunk:
        merged = deepcopy(left)
        merged["text"] = merged_text
        merged["token_count"] = count_tokens(merged_text)
        merged["char_start"] = left["char_start"]
        merged["char_end"] = right["char_end"]
        merged["section_title"] = combine_section_titles(
            left.get("section_title"), right.get("section_title")
        )
        merged["block_types"] = combine_unique(
            [str(value) for value in left.get("block_types", [])],
            [str(value) for value in right.get("block_types", [])],
        )
        return merged

    structural_embeddings = embed_texts([str(chunk["text"]) for chunk in chunks])
    merged_chunks: list[Chunk] = []
    final_embeddings: list[Embedding | None] = []
    merge_examples: list[dict[str, Any]] = []

    for indexes in group_chunk_indexes(chunks).values():
        cursor = 0
        while cursor < len(indexes):
            first_index = indexes[cursor]
            current_chunk = deepcopy(chunks[first_index])
            current_embedding: Embedding | None = structural_embeddings[first_index]
            current_was_merged = False

            while cursor + 1 < len(indexes):
                left_index = indexes[cursor]
                right_index = indexes[cursor + 1]
                left_original = chunks[left_index]
                right_original = chunks[right_index]

                if has_hard_boundary(left_original) or has_hard_boundary(right_original):
                    break

                similarity = cosine_similarity(
                    structural_embeddings[left_index], structural_embeddings[right_index]
                )
                if similarity <= SEMANTIC_MERGE_THRESHOLD:
                    break

                merged_text = (
                    f"{str(current_chunk['text']).rstrip()}\n\n"
                    f"{str(right_original['text']).lstrip()}"
                )
                if count_tokens(merged_text) > MAX_TOKENS:
                    break

                if len(merge_examples) < MERGE_EXAMPLE_COUNT:
                    merge_examples.append(
                        {
                            "left_chunk_id": left_original["chunk_id"],
                            "right_chunk_id": right_original["chunk_id"],
                            "left_text": left_original["text"],
                            "right_text": right_original["text"],
                            "similarity": similarity,
                        }
                    )

                current_chunk = merge_chunks(current_chunk, right_original, merged_text)
                current_embedding = None
                current_was_merged = True
                cursor += 1

            merged_chunks.append(current_chunk)
            final_embeddings.append(None if current_was_merged else current_embedding)
            cursor += 1

    reembed_indexes = [
        index for index, embedding in enumerate(final_embeddings) if embedding is None
    ]
    refreshed_embeddings = embed_texts(
        [str(merged_chunks[index]["text"]) for index in reembed_indexes]
    )
    for index, embedding in zip(reembed_indexes, refreshed_embeddings, strict=True):
        final_embeddings[index] = embedding

    if any(embedding is None for embedding in final_embeddings):
        raise RuntimeError("A merged chunk is missing its refreshed embedding.")

    reassign_chunk_ids(merged_chunks)
    concrete_embeddings = [
        embedding for embedding in final_embeddings if embedding is not None
    ]
    for chunk, embedding in zip(merged_chunks, concrete_embeddings, strict=True):
        chunk["embedding"] = [float(value) for value in embedding]

    return {
        "chunks": merged_chunks,
        "structural_count": len(chunks),
        "final_count": len(merged_chunks),
        "merge_examples": merge_examples,
        "runtime_seconds": time.perf_counter() - started_at,
    }


def print_merge_examples(examples: list[dict[str, Any]]) -> None:
    safe_print(f"\nMerge examples ({len(examples)}):")
    if not examples:
        safe_print("No adjacent pairs met the threshold and token-limit rules in this run.")
        return

    for number, example in enumerate(examples, start=1):
        safe_print("\n" + "=" * 80)
        safe_print(
            f"Merge {number}: {example['left_chunk_id']} + {example['right_chunk_id']} "
            f"| cosine_similarity={float(example['similarity']):.4f}"
        )
        safe_print("\nLEFT ORIGINAL TEXT:\n")
        safe_print(str(example["left_text"]))
        safe_print("\nRIGHT ORIGINAL TEXT:\n")
        safe_print(str(example["right_text"]))


def write_json_atomically(path: Path, chunks: list[Chunk]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    temporary_path.write_text(
        json.dumps(chunks, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return temporary_path


@app.local_entrypoint()
def main(
    chunks_path: str = str(CHUNKS_PATH),
    embeddings_path: str = str(EMBEDDINGS_PATH),
    limit: int = 0,
) -> None:
    """Invoke Modal, then write clean and embedding-bearing JSON files locally."""
    input_path = Path(chunks_path)
    if not input_path.exists():
        raise FileNotFoundError(
            f"Chunk file not found: {input_path}. Run build_chunks.py first."
        )
    if limit < 0:
        raise ValueError("--limit must be zero or a positive integer.")

    structural_chunks = validate_structural_chunks(
        json.loads(input_path.read_text(encoding="utf-8"))
    )
    selected_chunks = structural_chunks[:limit] if limit else structural_chunks
    if not selected_chunks:
        raise ValueError("The selected chunk subset is empty.")

    if limit:
        clean_destination = SMOKE_TEST_CLEAN_PATH
        embeddings_destination = SMOKE_TEST_EMBEDDINGS_PATH
    else:
        clean_destination = input_path
        embeddings_destination = Path(embeddings_path)

    safe_print(
        f"Sending {len(selected_chunks)} structural chunks to Modal "
        f"using app '{APP_NAME}'..."
    )
    result = embed_and_merge.remote(selected_chunks)
    chunks_with_embeddings = result["chunks"]
    if any("embedding" not in chunk for chunk in chunks_with_embeddings):
        raise RuntimeError("Modal returned one or more chunks without an embedding.")

    clean_chunks = [
        {key: value for key, value in chunk.items() if key != "embedding"}
        for chunk in chunks_with_embeddings
    ]

    embeddings_temporary = write_json_atomically(
        embeddings_destination, chunks_with_embeddings
    )
    clean_temporary = write_json_atomically(clean_destination, clean_chunks)
    embeddings_temporary.replace(embeddings_destination)
    clean_temporary.replace(clean_destination)

    safe_print(f"\nStructural chunks before merging: {result['structural_count']}")
    safe_print(f"Final chunks after semantic merging: {result['final_count']}")
    safe_print(f"Total Modal GPU runtime: {float(result['runtime_seconds']):.1f} seconds")
    safe_print(f"Clean chunks written locally to: {clean_destination}")
    safe_print(f"Chunks with embeddings written locally to: {embeddings_destination}")
    print_merge_examples(result["merge_examples"])

