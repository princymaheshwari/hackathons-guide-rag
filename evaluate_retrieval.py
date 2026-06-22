"""Run the five planned evaluation questions against semantic retrieval."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from retrieval import DEFAULT_TOP_K, retrieve


OUTPUT_PATH = Path("processed/retrieval_test_results.json")
EVALUATION_QUESTIONS = (
    "What roles or skills do online sources recommend looking for when forming a hackathon team?",
    "What kinds of projects have historically won at AI-focused or beginner-friendly hackathons, according to Devpost or recap posts?",
    "What hackathons does MLH organize or list for the Southeast/Atlanta region?",
    "What do sources say about the tradeoffs between spending time on hackathons versus LeetCode/DSA practice for job preparation?",
    "What is the difference between MLH-affiliated hackathons and independently run hackathons, according to community discussion?",
)


def safe_print(text: str = "") -> None:
    """Print safely on Windows consoles that are not UTF-8."""
    encoding = sys.stdout.encoding or "utf-8"
    sys.stdout.write(text.encode(encoding, errors="replace").decode(encoding) + "\n")


def print_query_results(
    query_number: int,
    query: str,
    results: list[dict[str, Any]],
) -> None:
    safe_print("\n" + "#" * 100)
    safe_print(f"QUERY {query_number}: {query}")

    for result_number, result in enumerate(results, start=1):
        safe_print("\n" + "=" * 100)
        safe_print(
            f"RESULT {result_number} | distance={result['distance']:.6f} "
            f"| chunk_id={result['chunk_id']}"
        )
        safe_print(f"source_filename: {result['source_filename']}")
        safe_print(f"source_type: {result['source_type']}")
        safe_print(f"section_title: {result['section_title']}")
        safe_print("\nFULL CHUNK TEXT:\n")
        safe_print(str(result["text"]))


def print_summary(evaluations: list[dict[str, Any]]) -> None:
    safe_print("\n" + "#" * 100)
    safe_print("TOP-RESULT DISTANCE SUMMARY")
    safe_print(f"{'#':<3} {'Distance':<12} Query")
    safe_print("-" * 100)

    for query_number, evaluation in enumerate(evaluations, start=1):
        results = evaluation["results"]
        distance = f"{results[0]['distance']:.6f}" if results else "no results"
        safe_print(f"{query_number:<3} {distance:<12} {evaluation['query']}")


def write_results(evaluations: list[dict[str, Any]]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = OUTPUT_PATH.with_suffix(OUTPUT_PATH.suffix + ".tmp")
    temporary_path.write_text(
        json.dumps(evaluations, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(OUTPUT_PATH)


def main() -> int:
    evaluations: list[dict[str, Any]] = []

    for query_number, query in enumerate(EVALUATION_QUESTIONS, start=1):
        results = retrieve(query, top_k=DEFAULT_TOP_K)
        evaluation = {"query": query, "top_k": DEFAULT_TOP_K, "results": results}
        evaluations.append(evaluation)
        print_query_results(query_number, query, results)

    write_results(evaluations)
    print_summary(evaluations)
    safe_print(f"\nSaved complete retrieval results to: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
