"""Embedded event-card scraping entry points."""

from __future__ import annotations

from .core import discover_embedded_event_cards, scrape_card_listing_to_markdown
from .rendered import scrape_rendered_card_listing_to_markdown

__all__ = [
    "discover_embedded_event_cards",
    "scrape_card_listing_to_markdown",
    "scrape_rendered_card_listing_to_markdown",
]
