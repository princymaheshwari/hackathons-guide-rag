"""Reusable CLI-first web scraping helpers."""

from __future__ import annotations

from .core import (
    ScrapedContent,
    extract_url_content,
    scrape_paginated_to_markdown,
    scrape_url_to_markdown,
)

__all__ = [
    "ScrapedContent",
    "extract_url_content",
    "scrape_paginated_to_markdown",
    "scrape_url_to_markdown",
]
