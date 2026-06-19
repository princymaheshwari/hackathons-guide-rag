"""Single-page scraping entry points."""

from __future__ import annotations

from .core import extract_url_content, scrape_url_to_markdown

__all__ = ["extract_url_content", "scrape_url_to_markdown"]
