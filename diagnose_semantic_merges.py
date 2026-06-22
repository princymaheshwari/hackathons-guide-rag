"""Diagnose adjacent-chunk similarities using saved embeddings only.

This script is read-only: it does not load an embedding model, modify either
chunk JSON file, contact Modal, or write to ChromaDB.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any, Sequence

from build_chunks import HARD_BOUNDARY_TYPES, MAX_TOKENS, count_tokens


EMBEDDINGS_PATH = Path("processed/chunks.embeddings.json")
SEMANTIC_MERGE_THRESHOLD = 0.75
DEFAULT_TOP_COUNT = 10
DEFAULT_PREVIEW_CHARS = 150

Chunk = dict[str, Any]
Embedding = Sequence[float]
PairDiagnostic = dict[str, Any]


def safe_print(text: str = "") -> None:
    """Print safely on Windows consoles that are not UTF-8."""
    encoding = sys.stdout.encoding or "utf-8"
    sys.stdout.write(text.encode(encoding, errors="replace").decode(encoding) + "\n")


def load_embedded_chunks(path: Path) -> list[Chunk]:
    if not path.exists():
        raise FileNotFoundError(
            f"Embedded chunk file not found: {path}. Run the full Modal job first."
        )

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list) or not payload:
        raise ValueError(f"Expected a non-empty JSON list of chunks in {path}.")

    required_fields = {
        "chunk_id",
        "text",
        "source_file",
        "block_types",
        "chunk_position",
        "embedding",
    }
    invalid_chunks: list[str] = []
    embedding_dimensions: set[int] = set()

    for index, chunk in enumerate(payload):
        if not isinstance(chunk, dict) or not required_fields.issubset(chunk):
            chunk_id = chunk.get("chunk_id", f"index {index}") if isinstance(chunk, dict) else index
            invalid_chunks.append(str(chunk_id))
            continue

        embedding = chunk["embedding"]
        if (
            not isinstance(embedding, list)
            or not embedding
            or any(not isinstance(value, (int, float)) for value in embedding)
        ):
            invalid_chunks.append(str(chunk["chunk_id"]))
            continue
        embedding_dimensions.add(len(embedding))

    if invalid_chunks:
        raise ValueError(
            "Invalid or missing embeddings for chunks: " + ", ".join(invalid_chunks[:5])
        )
    if len(embedding_dimensions) != 1:
        raise ValueError(
            "Embedding vectors do not all have the same dimension: "
            f"{sorted(embedding_dimensions)}."
        )

    return payload


def cosine_similarity(left: Embedding, right: Embedding) -> float:
    """Use the same cosine calculation as the semantic merge implementation."""
    dot_product = sum(float(a) * float(b) for a, b in zip(left, right, strict=True))
    left_norm = math.sqrt(sum(float(value) ** 2 for value in left))
    right_norm = math.sqrt(sum(float(value) ** 2 for value in right))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return dot_product / (left_norm * right_norm)


def group_chunk_indexes(chunks: list[Chunk]) -> OrderedDict[str, list[int]]:
    grouped: OrderedDict[str, list[int]] = OrderedDict()
    for index, chunk in enumerate(chunks):
        source_file = str(chunk["source_file"])
        grouped.setdefault(source_file, []).append(index)

    for indexes in grouped.values():
        indexes.sort(key=lambda index: int(chunks[index]["chunk_position"]))
    return grouped


def hard_boundary_types(left: Chunk, right: Chunk) -> list[str]:
    left_types = {str(value) for value in left.get("block_types", [])}
    right_types = {str(value) for value in right.get("block_types", [])}
    return sorted((left_types | right_types) & HARD_BOUNDARY_TYPES)


def analyze_pairs(chunks: list[Chunk]) -> list[PairDiagnostic]:
    diagnostics: list[PairDiagnostic] = []

    for source_file, indexes in group_chunk_indexes(chunks).items():
        for left_index, right_index in zip(indexes, indexes[1:]):
            left = chunks[left_index]
            right = chunks[right_index]
            merged_text = (
                f"{str(left['text']).rstrip()}\n\n{str(right['text']).lstrip()}"
            )
            merged_token_count = count_tokens(merged_text)
            boundary_types = hard_boundary_types(left, right)
            similarity = cosine_similarity(left["embedding"], right["embedding"])
            over_max_tokens = merged_token_count > MAX_TOKENS

            diagnostics.append(
                {
                    "source_file": source_file,
                    "left_chunk_id": left["chunk_id"],
                    "right_chunk_id": right["chunk_id"],
                    "left_text": left["text"],
                    "right_text": right["text"],
                    "similarity": similarity,
                    "hard_boundary_types": boundary_types,
                    "merged_token_count": merged_token_count,
                    "over_max_tokens": over_max_tokens,
                    "eligible": not boundary_types and not over_max_tokens,
                    "above_threshold": similarity > SEMANTIC_MERGE_THRESHOLD,
                }
            )

    return diagnostics


def preview(text: object, max_chars: int) -> str:
    normalized = " ".join(str(text).split())
    if len(normalized) <= max_chars:
        return normalized
    return normalized[: max(0, max_chars - 3)].rstrip() + "..."


def print_all_pairs(diagnostics: list[PairDiagnostic]) -> None:
    safe_print("Adjacent pair scores:")
    for number, pair in enumerate(diagnostics, start=1):
        boundary_label = ",".join(pair["hard_boundary_types"]) or "none"
        safe_print(
            f"{number:04d} | similarity={pair['similarity']:.6f} "
            f"| {pair['source_file']} "
            f"| {pair['left_chunk_id']} -> {pair['right_chunk_id']} "
            f"| hard_boundary={boundary_label} "
            f"| merged_tokens={pair['merged_token_count']} "
            f"| over_max={pair['over_max_tokens']} "
            f"| eligible={pair['eligible']}"
        )


def print_summary(diagnostics: list[PairDiagnostic]) -> None:
    scores = [float(pair["similarity"]) for pair in diagnostics]
    if not scores:
        safe_print("No adjacent pairs were found.")
        return

    eligible = [pair for pair in diagnostics if pair["eligible"]]
    above_threshold = [pair for pair in diagnostics if pair["above_threshold"]]
    eligible_above_threshold = [
        pair for pair in eligible if pair["above_threshold"]
    ]
    hard_excluded = [pair for pair in diagnostics if pair["hard_boundary_types"]]
    token_excluded = [pair for pair in diagnostics if pair["over_max_tokens"]]
    excluded_by_both = [
        pair
        for pair in diagnostics
        if pair["hard_boundary_types"] and pair["over_max_tokens"]
    ]

    safe_print("\nSummary statistics:")
    safe_print(f"Adjacent pairs: {len(diagnostics)}")
    safe_print(f"Minimum similarity: {min(scores):.6f}")
    safe_print(f"Maximum similarity: {max(scores):.6f}")
    safe_print(f"Mean similarity: {statistics.fmean(scores):.6f}")
    safe_print(f"Median similarity: {statistics.median(scores):.6f}")
    safe_print(
        f"Pairs above {SEMANTIC_MERGE_THRESHOLD:.2f}: {len(above_threshold)}"
    )
    safe_print(f"Hard-boundary exclusions: {len(hard_excluded)}")
    safe_print(f"Over-{MAX_TOKENS}-token exclusions: {len(token_excluded)}")
    safe_print(f"Excluded by both rules: {len(excluded_by_both)}")
    safe_print(f"Pairs eligible for merging: {len(eligible)}")
    safe_print(
        "Eligible pairs above threshold: "
        f"{len(eligible_above_threshold)}"
    )

    if eligible:
        eligible_scores = [float(pair["similarity"]) for pair in eligible]
        highest_eligible = max(
            eligible,
            key=lambda pair: float(pair["similarity"]),
        )
        safe_print(f"Eligible minimum similarity: {min(eligible_scores):.6f}")
        safe_print(f"Eligible maximum similarity: {max(eligible_scores):.6f}")
        safe_print(f"Eligible mean similarity: {statistics.fmean(eligible_scores):.6f}")
        safe_print(f"Eligible median similarity: {statistics.median(eligible_scores):.6f}")
        safe_print(
            "Highest eligible pair: "
            f"{highest_eligible['left_chunk_id']} -> "
            f"{highest_eligible['right_chunk_id']}"
        )


def print_top_pairs(
    diagnostics: list[PairDiagnostic],
    top_count: int,
    preview_chars: int,
) -> None:
    safe_print(f"\nTop {min(top_count, len(diagnostics))} adjacent pairs:")
    ranked = sorted(
        diagnostics,
        key=lambda pair: float(pair["similarity"]),
        reverse=True,
    )[:top_count]

    for number, pair in enumerate(ranked, start=1):
        boundary_label = ", ".join(pair["hard_boundary_types"]) or "none"
        safe_print("\n" + "=" * 80)
        safe_print(
            f"#{number} similarity={pair['similarity']:.6f} "
            f"| source={pair['source_file']}"
        )
        safe_print(
            f"Chunks: {pair['left_chunk_id']} -> {pair['right_chunk_id']}"
        )
        safe_print(
            f"Excluded by hard boundary: {bool(pair['hard_boundary_types'])} "
            f"({boundary_label})"
        )
        safe_print(
            f"Excluded by token cap: {pair['over_max_tokens']}"
        )
        safe_print(
            f"Merged token count: {pair['merged_token_count']} "
            f"(limit {MAX_TOKENS})"
        )
        safe_print(f"Eligible for merging: {pair['eligible']}")
        safe_print(f"Left:  {preview(pair['left_text'], preview_chars)}")
        safe_print(f"Right: {preview(pair['right_text'], preview_chars)}")


def print_would_merge_pairs(
    diagnostics: list[PairDiagnostic],
    preview_chars: int,
) -> None:
    candidates = [
        pair
        for pair in diagnostics
        if pair["eligible"] and pair["above_threshold"]
    ]
    safe_print(
        f"\nPairs that would merge at threshold "
        f"{SEMANTIC_MERGE_THRESHOLD:.2f}: {len(candidates)}"
    )

    for number, pair in enumerate(candidates, start=1):
        safe_print("\n" + "-" * 80)
        safe_print(
            f"#{number} similarity={pair['similarity']:.6f} "
            f"| source={pair['source_file']}"
        )
        safe_print(
            f"Chunks: {pair['left_chunk_id']} -> {pair['right_chunk_id']}"
        )
        safe_print(
            f"Merged token count: {pair['merged_token_count']} "
            f"(limit {MAX_TOKENS})"
        )
        safe_print(f"Left:  {preview(pair['left_text'], preview_chars)}")
        safe_print(f"Right: {preview(pair['right_text'], preview_chars)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect semantic-merge similarities from precomputed embeddings."
    )
    parser.add_argument("--chunks", type=Path, default=EMBEDDINGS_PATH)
    parser.add_argument("--top", type=int, default=DEFAULT_TOP_COUNT)
    parser.add_argument("--preview-chars", type=int, default=DEFAULT_PREVIEW_CHARS)
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Skip the full per-pair listing but still print statistics and top pairs.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.top < 1:
        safe_print("Error: --top must be at least 1.")
        return 1
    if args.preview_chars < 20:
        safe_print("Error: --preview-chars must be at least 20.")
        return 1

    try:
        chunks = load_embedded_chunks(args.chunks)
        diagnostics = analyze_pairs(chunks)
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as error:
        safe_print(f"Error: {error}")
        return 1

    if not args.summary_only:
        print_all_pairs(diagnostics)
    print_summary(diagnostics)
    print_would_merge_pairs(diagnostics, args.preview_chars)
    print_top_pairs(diagnostics, args.top, args.preview_chars)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
