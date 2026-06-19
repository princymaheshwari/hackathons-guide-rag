"""Paginated scraping entry points."""

from __future__ import annotations

from .core import discover_links_by_text, paginated_url, scrape_paginated_to_markdown

__all__ = ["discover_links_by_text", "paginated_url", "scrape_paginated_to_markdown"]
