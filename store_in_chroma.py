"""Store precomputed chunk embeddings in a local persistent Chroma collection."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import chromadb


EMBEDDINGS_PATH = Path("processed/chunks.embeddings.json")
CHROMA_PATH = Path("chroma_db")
COLLECTION_NAME = "hackathon_guide"
DISTANCE_METRIC = "cosine"
CHROMA_BATCH_SIZE = 100

Chunk = dict[str, Any]


def safe_print(text: str = "") -> None:
    """Print safely on Windows consoles that are not UTF-8."""
    encoding = sys.stdout.encoding or "utf-8"
    sys.stdout.write(text.encode(encoding, errors="replace").decode(encoding) + "\n")


def load_embedded_chunks(path: Path) -> list[Chunk]:
    if not path.exists():
        raise FileNotFoundError(
            f"Embedded chunk file not found: {path}. Run embed_and_merge_modal.py first."
        )

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list) or not payload:
        raise ValueError(f"Expected a non-empty JSON list of chunks in {path}.")

    required_fields = {
        "chunk_id",
        "text",
        "source_file",
        "source_filename",
        "source_type",
        "section_title",
        "chunk_position",
        "token_count",
        "embedding",
    }
    invalid_chunks: list[str] = []
    embedding_dimensions: set[int] = set()
    chunk_ids: list[str] = []

    for index, chunk in enumerate(payload):
        if not isinstance(chunk, dict) or not required_fields.issubset(chunk):
            chunk_id = chunk.get("chunk_id", f"index {index}") if isinstance(chunk, dict) else index
            invalid_chunks.append(str(chunk_id))
            continue

        chunk_id = str(chunk["chunk_id"])
        chunk_ids.append(chunk_id)
        embedding = chunk["embedding"]
        if (
            not isinstance(embedding, list)
            or not embedding
            or any(not isinstance(value, (int, float)) for value in embedding)
        ):
            invalid_chunks.append(chunk_id)
            continue
        embedding_dimensions.add(len(embedding))

    if invalid_chunks:
        examples = ", ".join(invalid_chunks[:5])
        raise ValueError(f"Invalid or missing chunk embeddings: {examples}.")
    if len(set(chunk_ids)) != len(chunk_ids):
        raise ValueError("Duplicate chunk_id values found in the embedded chunk file.")
    if len(embedding_dimensions) != 1:
        raise ValueError(
            "Embedding vectors do not all have the same dimension: "
            f"{sorted(embedding_dimensions)}."
        )

    return payload


def chroma_metadata(chunk: Chunk) -> dict[str, str | int | float | bool]:
    fields = (
        "chunk_id",
        "source_file",
        "source_filename",
        "source_type",
        "section_title",
        "chunk_position",
        "token_count",
    )
    metadata: dict[str, str | int | float | bool] = {}
    for field in fields:
        value = chunk.get(field)
        if value is None:
            continue
        if isinstance(value, (str, int, float, bool)):
            metadata[field] = value
        else:
            metadata[field] = str(value)
    return metadata


def fresh_collection(client: Any, name: str) -> Any:
    existing_names = {
        collection if isinstance(collection, str) else collection.name
        for collection in client.list_collections()
    }
    if name in existing_names:
        client.delete_collection(name=name)
    collection = client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": DISTANCE_METRIC},
    )
    configured_metric = collection.configuration.get("hnsw", {}).get("space")
    if configured_metric != DISTANCE_METRIC:
        raise RuntimeError(
            f"Chroma metric mismatch: expected {DISTANCE_METRIC}, "
            f"found {configured_metric}."
        )
    return collection


def store_chunks(
    chunks: list[Chunk],
    chroma_path: Path,
    collection_name: str,
) -> int:
    chroma_path.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(chroma_path))
    collection = fresh_collection(client, collection_name)

    for start in range(0, len(chunks), CHROMA_BATCH_SIZE):
        batch = chunks[start : start + CHROMA_BATCH_SIZE]
        collection.add(
            ids=[str(chunk["chunk_id"]) for chunk in batch],
            embeddings=[
                [float(value) for value in chunk["embedding"]] for chunk in batch
            ],
            documents=[str(chunk["text"]) for chunk in batch],
            metadatas=[chroma_metadata(chunk) for chunk in batch],
        )

    stored_count = collection.count()
    if stored_count != len(chunks):
        raise RuntimeError(
            f"Chroma count mismatch: expected {len(chunks)}, found {stored_count}."
        )
    return stored_count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Store precomputed hackathon chunk embeddings in local ChromaDB."
    )
    parser.add_argument("--chunks", type=Path, default=EMBEDDINGS_PATH)
    parser.add_argument("--chroma-path", type=Path, default=CHROMA_PATH)
    parser.add_argument("--collection", default=COLLECTION_NAME)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        chunks = load_embedded_chunks(args.chunks)
        safe_print(f"Total chunks read: {len(chunks)}")
        stored_count = store_chunks(chunks, args.chroma_path, args.collection)
        safe_print(f"Total chunks added to Chroma: {len(chunks)}")
        safe_print(f"Collection distance metric: {DISTANCE_METRIC}")
        safe_print(
            f"Collection count confirmed: {stored_count} "
            f"(matches source chunk count)"
        )
    except (FileNotFoundError, json.JSONDecodeError, ValueError, RuntimeError) as error:
        safe_print(f"Error: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
