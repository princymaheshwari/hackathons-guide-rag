"""Semantic retrieval from the local hackathon guide Chroma collection."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import chromadb
from sentence_transformers import SentenceTransformer


MODEL_NAME = "Qwen/Qwen3-Embedding-0.6B"
CHROMA_PATH = Path("chroma_db")
COLLECTION_NAME = "hackathon_guide"
EXPECTED_DISTANCE_METRIC = "cosine"
DEFAULT_TOP_K = 5

# Loaded once per Python process and reused by every retrieve() call.
_model = SentenceTransformer(MODEL_NAME)
_client = chromadb.PersistentClient(path=str(CHROMA_PATH))
_collection = _client.get_collection(name=COLLECTION_NAME)


def _validate_collection() -> None:
    configured_metric = _collection.configuration.get("hnsw", {}).get("space")
    if configured_metric != EXPECTED_DISTANCE_METRIC:
        raise RuntimeError(
            f"Chroma collection '{COLLECTION_NAME}' uses {configured_metric!r}, "
            f"not {EXPECTED_DISTANCE_METRIC!r}. Rebuild it with store_in_chroma.py."
        )
    if _collection.count() == 0:
        raise RuntimeError(f"Chroma collection '{COLLECTION_NAME}' is empty.")


_validate_collection()


def retrieve(query: str, top_k: int = DEFAULT_TOP_K) -> list[dict[str, Any]]:
    """Return the nearest stored chunks for a natural-language query."""
    normalized_query = query.strip()
    if not normalized_query:
        raise ValueError("query must not be empty")
    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    query_embedding = _model.encode(
        [normalized_query],
        prompt_name="query",
        convert_to_numpy=True,
    )[0]
    response = _collection.query(
        query_embeddings=[[float(value) for value in query_embedding]],
        n_results=min(top_k, _collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    ids = response.get("ids", [[]])[0]
    documents = response.get("documents", [[]])[0]
    metadatas = response.get("metadatas", [[]])[0]
    distances = response.get("distances", [[]])[0]

    results: list[dict[str, Any]] = []
    for chunk_id, document, metadata, distance in zip(
        ids,
        documents,
        metadatas,
        distances,
        strict=True,
    ):
        metadata = metadata or {}
        results.append(
            {
                "text": document or "",
                "source_filename": metadata.get("source_filename"),
                "source_type": metadata.get("source_type"),
                "section_title": metadata.get("section_title"),
                "chunk_id": metadata.get("chunk_id", chunk_id),
                "distance": float(distance),
            }
        )

    return results

