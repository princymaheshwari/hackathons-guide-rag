"""Playwright-backed scraping for JavaScript-rendered pages and event cards."""

from __future__ import annotations

import asyncio
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit

from bs4 import BeautifulSoup, NavigableString, Tag
from playwright.async_api import (
    Browser,
    Page,
    TimeoutError as PlaywrightTimeoutError,
    async_playwright,
)

from .core import (
    clean_inline_text,
    clean_soup,
    choose_content_root,
    html_table_to_rows,
    rows_to_markdown,
    write_markdown_file,
)


MINIMUM_TEXT_LENGTH = 200
DEFAULT_SCROLL_ITERATIONS = 4
DEFAULT_WAIT_MS = 1_000
DEFAULT_TIMEOUT_MS = 60_000
DEFAULT_WORKERS = 4
BLOCK_PAGE_MARKERS = (
    "captcha",
    "verify you are human",
    "checking your browser",
    "access denied",
    "unusual traffic",
    "enable javascript and cookies to continue",
    "cloudflare ray id",
)
BLOCK_TAGS = {
    "address",
    "article",
    "aside",
    "blockquote",
    "details",
    "div",
    "dl",
    "fieldset",
    "figure",
    "footer",
    "form",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "header",
    "hr",
    "main",
    "nav",
    "ol",
    "p",
    "pre",
    "section",
    "table",
    "ul",
}


@dataclass
class RenderedPage:
    title: str
    final_url: str
    visible_text: str
    body_markdown: str
    status_code: int | None
    expanded_elements: int = 0


@dataclass
class RenderedDetail:
    requested_url: str
    event_names: list[str]
    page: RenderedPage | None
    error: str | None


def safe_print(text: str = "", *, file: object = sys.stdout) -> None:
    """Print safely on Windows consoles that are not UTF-8."""
    stream = file if hasattr(file, "write") else sys.stdout
    encoding = getattr(stream, "encoding", None) or "utf-8"
    rendered = text.encode(encoding, errors="replace").decode(encoding)
    stream.write(rendered + "\n")


def normalize_visible_text(text: str) -> str:
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    normalized: list[str] = []
    previous_was_blank = False

    for line in lines:
        if not line:
            if normalized and not previous_was_blank:
                normalized.append("")
            previous_was_blank = True
            continue
        normalized.append(line)
        previous_was_blank = False

    return "\n".join(normalized).strip()


def _inline_markdown(node: object, base_url: str) -> str:
    if isinstance(node, NavigableString):
        text = str(node)
        if re.fullmatch(
            r"\s*<(?:i|span)\b[^>]*>\s*</(?:i|span)>\s*",
            text,
            flags=re.IGNORECASE,
        ):
            return ""
        return re.sub(r"\s+", " ", text)
    if not isinstance(node, Tag):
        return ""

    name = node.name.lower()
    if name == "br":
        return "\n"
    if name == "img":
        alt = clean_inline_text(str(node.get("alt") or ""))
        return f"[Image: {alt}]" if alt else ""

    content = "".join(_inline_markdown(child, base_url) for child in node.children)
    content = re.sub(r"[ \t]+", " ", content)
    content = re.sub(r" *\n *", "\n", content).strip()
    if not content:
        return ""

    if name == "a":
        href = node.get("href")
        if isinstance(href, str) and href.strip() and not href.lower().startswith(
            ("javascript:", "mailto:", "tel:")
        ):
            return f"[{content}]({urljoin(base_url, href.strip())})"
    if name in {"strong", "b"}:
        return f"**{content}**"
    if name in {"em", "i"}:
        return f"*{content}*"
    if name == "code":
        return f"`{content}`"
    return content


def _render_list(list_tag: Tag, base_url: str, depth: int = 0) -> str:
    lines: list[str] = []
    ordered = list_tag.name.lower() == "ol"
    items = list_tag.find_all("li", recursive=False)

    for index, item in enumerate(items, start=1):
        inline_parts = [
            _inline_markdown(child, base_url)
            for child in item.children
            if not (isinstance(child, Tag) and child.name.lower() in {"ul", "ol"})
        ]
        item_text = clean_inline_text(" ".join(part for part in inline_parts if part))
        marker = f"{index}." if ordered else "-"
        if item_text:
            lines.append(f"{'  ' * depth}{marker} {item_text}")

        for nested in item.find_all(["ul", "ol"], recursive=False):
            nested_markdown = _render_list(nested, base_url, depth + 1)
            if nested_markdown:
                lines.append(nested_markdown)

    return "\n".join(lines)


def _render_definition_list(tag: Tag, base_url: str) -> str:
    blocks: list[str] = []
    for child in tag.find_all(["dt", "dd"], recursive=False):
        text = _inline_markdown(child, base_url).strip()
        if not text:
            continue
        blocks.append(f"**{text}**" if child.name.lower() == "dt" else text)
    return "\n\n".join(blocks)


def _render_container(container: Tag, base_url: str) -> list[str]:
    blocks: list[str] = []
    inline_buffer: list[str] = []

    def flush_inline() -> None:
        text = clean_inline_text(" ".join(inline_buffer))
        inline_buffer.clear()
        if text:
            blocks.append(text)

    for child in container.children:
        if isinstance(child, NavigableString):
            rendered_text = _inline_markdown(child, base_url)
            if clean_inline_text(rendered_text):
                inline_buffer.append(rendered_text)
            continue
        if not isinstance(child, Tag):
            continue

        name = child.name.lower()
        if name not in BLOCK_TAGS:
            rendered_inline = _inline_markdown(child, base_url)
            if rendered_inline:
                inline_buffer.append(rendered_inline)
            continue

        flush_inline()
        rendered_block = _render_block(child, base_url)
        if rendered_block:
            blocks.append(rendered_block)

    flush_inline()
    return blocks


def _render_block(tag: Tag, base_url: str) -> str:
    name = tag.name.lower()
    if re.fullmatch(r"h[1-6]", name):
        text = _inline_markdown(tag, base_url).strip()
        return f"{'#' * int(name[1])} {text}" if text else ""
    if name in {"p", "address", "figcaption", "summary"}:
        return _inline_markdown(tag, base_url).strip()
    if name in {"ul", "ol"}:
        return _render_list(tag, base_url)
    if name == "blockquote":
        quote = "\n\n".join(_render_container(tag, base_url))
        return "\n".join(f"> {line}" if line else ">" for line in quote.splitlines())
    if name == "pre":
        code = tag.get_text("\n", strip=True)
        return f"```text\n{code}\n```" if code else ""
    if name == "table":
        headers, rows = html_table_to_rows(tag)
        if not headers or not rows:
            return ""
        caption = tag.find("caption")
        title = clean_inline_text(caption.get_text(" ", strip=True)) if caption else "Table"
        return rows_to_markdown(headers, rows, title)
    if name == "dl":
        return _render_definition_list(tag, base_url)
    if name == "hr":
        return "---"

    return "\n\n".join(_render_container(tag, base_url))


def markdown_from_rendered_html(html: str, base_url: str) -> str:
    """Convert a rendered DOM to Markdown without flattening its block structure."""
    soup = BeautifulSoup(html, "html.parser")
    clean_soup(soup, keep_visible_chrome=True)
    content_root = choose_content_root(soup)
    if content_root.name == "body":
        for chrome in content_root.select("nav, footer, aside, header[role='banner']"):
            chrome.decompose()
    markdown = "\n\n".join(_render_container(content_root, base_url))
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    return markdown.strip()


async def _visible_dom_html(page: Page) -> str:
    """Clone the DOM and remove CSS-hidden responsive copies without mutating it."""
    return await page.evaluate(
        """
        () => {
            const original = [document.documentElement, ...document.documentElement.querySelectorAll('*')];
            const clone = document.documentElement.cloneNode(true);
            const copied = [clone, ...clone.querySelectorAll('*')];
            const hiddenIndexes = [];

            original.forEach((element, index) => {
                if (!(element instanceof Element)) return;
                const style = window.getComputedStyle(element);
                if (
                    element.hidden ||
                    element.getAttribute('aria-hidden') === 'true' ||
                    style.display === 'none' ||
                    style.visibility === 'hidden'
                ) {
                    hiddenIndexes.push(index);
                }
            });

            hiddenIndexes.reverse().forEach((index) => copied[index]?.remove());
            return '<!DOCTYPE html>\\n' + clone.outerHTML;
        }
        """
    )


async def _expand_faq_content(page: Page, wait_ms: int) -> int:
    """Open visible FAQ/details controls before extracting the rendered DOM."""
    expanded = await page.evaluate(
        """
        () => {
            const isVisible = (element) => {
                const style = window.getComputedStyle(element);
                const rect = element.getBoundingClientRect();
                return (
                    rect.width > 0 &&
                    rect.height > 0 &&
                    style.display !== 'none' &&
                    style.visibility !== 'hidden'
                );
            };

            let expandedCount = 0;

            document.querySelectorAll('details:not([open])').forEach((details) => {
                if (!isVisible(details)) return;
                const summary = details.querySelector(':scope > summary');
                if (summary instanceof HTMLElement) {
                    summary.click();
                } else {
                    details.open = true;
                    details.dispatchEvent(new Event('toggle', { bubbles: false }));
                }
                expandedCount += 1;
            });

            const selector = [
                "button[aria-expanded='false']",
                "[role='button'][aria-expanded='false']",
                "button[data-state='closed']",
                "[role='button'][data-state='closed']",
                "[class*='faq' i] button",
                "[class*='faq' i] [role='button']",
                "[class*='faq-question' i]",
                "[class*='accordion' i] button",
                "[class*='accordion' i] [role='button']",
                "[class*='accordion-header' i]",
                "[class*='accordion-trigger' i]"
            ].join(',');

            document.querySelectorAll(selector).forEach((element) => {
                if (!(element instanceof HTMLElement)) return;
                if (!element.isConnected || !isVisible(element)) return;
                if (element.dataset.scrapeWebExpanded === 'true') return;

                const text = (element.innerText || element.textContent || '').trim();
                const context = element.closest(
                    "[class*='faq' i], [id*='faq' i], " +
                    "[class*='accordion' i], [id*='accordion' i]"
                );
                const looksLikeQuestion = text.endsWith('?');
                if (!context && !looksLikeQuestion) return;
                if (element.getAttribute('aria-expanded') === 'true') return;
                if (element.getAttribute('data-state') === 'open') return;

                element.dataset.scrapeWebExpanded = 'true';
                element.click();
                expandedCount += 1;
            });

            return expandedCount;
        }
        """
    )

    if expanded:
        await page.wait_for_timeout(max(500, min(wait_ms, 2_000)))
        try:
            await page.wait_for_load_state("networkidle", timeout=5_000)
        except PlaywrightTimeoutError:
            pass
        await page.evaluate(
            """
            () => {
                const reveal = (panel) => {
                    if (!(panel instanceof HTMLElement)) return;
                    panel.hidden = false;
                    panel.removeAttribute('hidden');
                    panel.setAttribute('aria-hidden', 'false');
                    panel.style.setProperty('display', 'block', 'important');
                    panel.style.setProperty('visibility', 'visible', 'important');
                    panel.style.setProperty('height', 'auto', 'important');
                    panel.style.setProperty('max-height', 'none', 'important');
                    panel.style.setProperty('opacity', '1', 'important');
                    panel.style.setProperty('overflow', 'visible', 'important');
                };

                document.querySelectorAll('[aria-controls]').forEach((control) => {
                    const context = control.closest(
                        "[class*='faq' i], [id*='faq' i], " +
                        "[class*='accordion' i], [id*='accordion' i]"
                    );
                    const text = (control.innerText || control.textContent || '').trim();
                    if (!context && !text.endsWith('?')) return;
                    const panelId = control.getAttribute('aria-controls');
                    if (panelId) reveal(document.getElementById(panelId));
                });

                const answerSelector = [
                    "[class*='faq-answer' i]",
                    "[class*='faq-content' i]",
                    "[class*='accordion-content' i]",
                    "[class*='accordion-panel' i]",
                    "[class*='collapse' i]",
                    "[role='region'][aria-labelledby]"
                ].join(',');
                document.querySelectorAll(answerSelector).forEach((panel) => {
                    const context = panel.closest(
                        "[class*='faq' i], [id*='faq' i], " +
                        "[class*='accordion' i], [id*='accordion' i]"
                    );
                    if (context) reveal(panel);
                });
            }
            """
        )
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(max(250, min(wait_ms, 1_000)))

    return int(expanded)


def _capture_failure_reason(page: RenderedPage) -> str | None:
    if page.status_code is not None and page.status_code >= 400:
        return f"HTTP {page.status_code}"
    if len(page.visible_text) < MINIMUM_TEXT_LENGTH:
        return (
            f"only {len(page.visible_text)} visible characters were extracted "
            f"(minimum {MINIMUM_TEXT_LENGTH})"
        )
    if len(page.body_markdown) < MINIMUM_TEXT_LENGTH:
        return "the rendered page did not contain enough structured main content"

    text_to_check = f"{page.title}\n{page.visible_text[:3000]}".casefold()
    marker = next(
        (candidate for candidate in BLOCK_PAGE_MARKERS if candidate in text_to_check),
        None,
    )
    if marker:
        return f"the page looks like a CAPTCHA or bot response ({marker!r})"
    return None


async def _capture_page(
    page: Page,
    url: str,
    scroll_iterations: int,
    wait_ms: int,
    timeout_ms: int,
) -> RenderedPage:
    response = await page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
    try:
        await page.wait_for_load_state("networkidle", timeout=min(timeout_ms, 8_000))
    except PlaywrightTimeoutError:
        # Analytics and live widgets can keep network connections open indefinitely.
        pass

    await page.wait_for_timeout(wait_ms)
    for _ in range(scroll_iterations):
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(wait_ms)

    expanded_elements = await _expand_faq_content(page, wait_ms)
    visible_text = normalize_visible_text(await page.locator("body").inner_text())
    final_url = page.url
    visible_html = await _visible_dom_html(page)
    return RenderedPage(
        title=(await page.title()).strip() or "JavaScript-rendered page",
        final_url=final_url,
        visible_text=visible_text,
        body_markdown=markdown_from_rendered_html(visible_html, final_url),
        status_code=response.status if response else None,
        expanded_elements=expanded_elements,
    )


async def _extract_embedded_event_cards(
    page: Page,
    card_group: str,
) -> list[dict[str, object]]:
    group_keys = {
        "upcoming": (("upcomingEvents", "Upcoming Events"),),
        "past": (("pastEvents", "Past Events"),),
        "all": (
            ("upcomingEvents", "Upcoming Events"),
            ("pastEvents", "Past Events"),
        ),
    }[card_group]
    cards: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    scripts = page.locator('script[type="application/json"]')

    for script_index in range(await scripts.count()):
        raw_payload = await scripts.nth(script_index).text_content()
        if not raw_payload:
            continue
        try:
            payload = json.loads(raw_payload)
        except json.JSONDecodeError:
            continue

        props = payload.get("props") if isinstance(payload, dict) else None
        if not isinstance(props, dict):
            continue

        for group_key, group_label in group_keys:
            records = props.get(group_key)
            if not isinstance(records, list):
                continue
            for record in records:
                if not isinstance(record, dict) or not record.get("name"):
                    continue
                event_id = str(record.get("id") or record.get("slug") or "")
                if event_id and event_id in seen_ids:
                    continue

                card = dict(record)
                card["group_label"] = group_label
                href = record.get("websiteUrl") or record.get("url")
                if isinstance(href, str) and href.strip():
                    card["event_link"] = urljoin(page.url, href.strip())
                cards.append(card)
                if event_id:
                    seen_ids.add(event_id)

    return cards


def _format_card_mode(value: object) -> str:
    modes = {
        "physical": "IN-PERSON",
        "digital": "DIGITAL",
        "hybrid": "HYBRID",
    }
    normalized = str(value or "").strip()
    return modes.get(normalized.casefold(), normalized.upper())


def _format_custom_fields(custom_fields: object) -> list[str]:
    if not isinstance(custom_fields, dict):
        return []

    lines: list[str] = []
    for key, value in custom_fields.items():
        if value in (None, "", [], {}):
            continue
        label = str(key).replace("_", " ").strip().title()
        if isinstance(value, list):
            rendered_value = ", ".join(str(item) for item in value)
        elif isinstance(value, dict):
            rendered_value = ", ".join(
                f"{nested_key}: {nested_value}"
                for nested_key, nested_value in value.items()
            )
        else:
            rendered_value = str(value)
        lines.append(f"- {label}: {rendered_value}")
    return lines


def event_cards_to_markdown(cards: list[dict[str, object]]) -> str:
    sections: list[str] = []
    card_number = 0

    for group_label in ("Upcoming Events", "Past Events"):
        grouped_cards = [card for card in cards if card.get("group_label") == group_label]
        if not grouped_cards:
            continue
        sections.append(f"## {group_label}")

        for card in grouped_cards:
            card_number += 1
            lines = [f"### Card {card_number}: {card['name']}"]
            for key, label in (
                ("dateRange", "Date"),
                ("startsAt", "Starts (UTC)"),
                ("endsAt", "Ends (UTC)"),
                ("location", "Location"),
                ("region", "Region"),
                ("status", "Status"),
            ):
                value = card.get(key)
                if value not in (None, ""):
                    lines.append(f"- {label}: {value}")

            mode = _format_card_mode(card.get("formatType"))
            if mode:
                lines.append(f"- Mode: {mode}")
            lines.extend(_format_custom_fields(card.get("customFields")))

            event_link = card.get("event_link")
            if event_link:
                lines.append(f"- Event link: [Open event page]({event_link})")
            sections.append("\n".join(lines))

    return "\n\n".join(sections)


def _canonical_url(url: str) -> str:
    parsed = urlsplit(url)
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit(
        (parsed.scheme.lower(), parsed.netloc.lower(), path, parsed.query, "")
    )


def _unique_card_destinations(
    cards: list[dict[str, object]],
) -> list[tuple[str, list[str]]]:
    destinations: dict[str, tuple[str, list[str]]] = {}
    for card in cards:
        event_link = card.get("event_link")
        if not isinstance(event_link, str) or not event_link:
            continue
        key = _canonical_url(event_link)
        name = str(card.get("name") or "Unnamed event")
        if key in destinations:
            if name not in destinations[key][1]:
                destinations[key][1].append(name)
        else:
            destinations[key] = (event_link, [name])
    return list(destinations.values())


def _shift_headings(markdown: str, levels: int = 3) -> str:
    def replace(match: re.Match[str]) -> str:
        hashes = match.group(1)
        return f"{'#' * min(6, len(hashes) + levels)} "

    return re.sub(r"^(#{1,6})\s+", replace, markdown, flags=re.MULTILINE)


async def _capture_detail(
    browser: Browser,
    semaphore: asyncio.Semaphore,
    index: int,
    total: int,
    url: str,
    event_names: list[str],
    scroll_iterations: int,
    wait_ms: int,
    timeout_ms: int,
) -> RenderedDetail:
    async with semaphore:
        safe_print(f"[{index}/{total}] Rendering {url}")
        page = await browser.new_page(viewport={"width": 1440, "height": 1000})
        try:
            rendered = await _capture_page(
                page,
                url,
                scroll_iterations,
                wait_ms,
                timeout_ms,
            )
            failure = _capture_failure_reason(rendered)
            if failure:
                return RenderedDetail(url, event_names, None, failure)
            return RenderedDetail(url, event_names, rendered, None)
        except Exception as exc:
            return RenderedDetail(url, event_names, None, str(exc).replace("\n", " "))
        finally:
            await page.close()


def _details_to_markdown(details: list[RenderedDetail]) -> str:
    sections = ["## Linked Event Websites"]
    for index, detail in enumerate(details, start=1):
        display_name = detail.event_names[0]
        lines = [
            f"### Website {index}: {display_name}",
            f"- Card URL: [{detail.requested_url}]({detail.requested_url})",
            f"- Referenced by: {', '.join(detail.event_names)}",
        ]
        if detail.error:
            lines.append(f"- Capture status: Failed - {detail.error}")
        elif detail.page:
            lines.extend(
                [
                    f"- Rendered title: {detail.page.title}",
                    f"- Final URL: [{detail.page.final_url}]({detail.page.final_url})",
                    f"- Expanded FAQ/accordion controls: {detail.page.expanded_elements}",
                    "",
                    _shift_headings(detail.page.body_markdown),
                ]
            )
        sections.append("\n".join(lines))
    return "\n\n".join(sections)


async def _scrape_rendered_page(
    url: str,
    output: Path | None,
    title_override: str | None,
    scroll_iterations: int,
    wait_ms: int,
    timeout_ms: int,
    headed: bool,
) -> Path:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=not headed)
        page = await browser.new_page(viewport={"width": 1440, "height": 1000})
        try:
            rendered = await _capture_page(
                page,
                url,
                scroll_iterations,
                wait_ms,
                timeout_ms,
            )
        finally:
            await page.close()
            await browser.close()

    failure = _capture_failure_reason(rendered)
    if failure:
        raise ValueError(f"Likely rendering failure: {failure}")
    safe_print(f"Expanded FAQ/accordion controls: {rendered.expanded_elements}")
    safe_print(f"Extracted structured text length: {len(rendered.body_markdown)} characters")
    safe_print(f"Preview:\n{rendered.body_markdown[:500]}")
    return write_markdown_file(
        url,
        title_override or rendered.title,
        rendered.body_markdown,
        "scrape_web:playwright_rendered",
        "rendered_web_page",
        {
            "rendered_url": rendered.final_url,
            "http_status": str(rendered.status_code or ""),
            "scroll_iterations": str(scroll_iterations),
            "expanded_faq_controls": str(rendered.expanded_elements),
        },
        output,
    )


async def _scrape_rendered_card_listing(
    url: str,
    output: Path | None,
    title_override: str | None,
    card_group: str,
    card_limit: int | None,
    scroll_iterations: int,
    wait_ms: int,
    timeout_ms: int,
    workers: int,
    headed: bool,
) -> Path:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=not headed)
        listing_page = await browser.new_page(viewport={"width": 1440, "height": 1000})
        try:
            listing = await _capture_page(
                listing_page,
                url,
                scroll_iterations,
                wait_ms,
                timeout_ms,
            )
            cards = await _extract_embedded_event_cards(listing_page, card_group)
        finally:
            await listing_page.close()

        if not cards:
            await browser.close()
            raise ValueError(
                "No embedded upcomingEvents or pastEvents records were found on the "
                "rendered page."
            )
        if card_limit is not None:
            cards = cards[:card_limit]

        destinations = _unique_card_destinations(cards)
        safe_print(
            f"Found {len(cards)} cards and {len(destinations)} unique linked websites."
        )
        semaphore = asyncio.Semaphore(workers)
        tasks = [
            _capture_detail(
                browser,
                semaphore,
                index,
                len(destinations),
                destination_url,
                event_names,
                scroll_iterations,
                wait_ms,
                timeout_ms,
            )
            for index, (destination_url, event_names) in enumerate(destinations, start=1)
        ]
        details = await asyncio.gather(*tasks)
        await browser.close()

    successful = sum(detail.page is not None for detail in details)
    failed = len(details) - successful
    expanded_controls = sum(
        detail.page.expanded_elements for detail in details if detail.page is not None
    )
    body_text = f"{event_cards_to_markdown(cards)}\n\n{_details_to_markdown(details)}"
    safe_print(
        f"Rendered linked websites: {successful} succeeded, {failed} failed; "
        f"expanded {expanded_controls} FAQ/accordion controls; "
        f"output length: {len(body_text)} characters."
    )
    return write_markdown_file(
        url,
        title_override or f"{listing.title} - rendered event websites",
        body_text,
        "scrape_web:playwright_rendered_card_links",
        "rendered_card_detail_pages",
        {
            "rendered_listing_url": listing.final_url,
            "card_group": card_group,
            "cards_collected": str(len(cards)),
            "unique_websites": str(len(destinations)),
            "detail_pages_collected": str(successful),
            "detail_pages_failed": str(failed),
            "expanded_faq_controls": str(expanded_controls),
            "scroll_iterations": str(scroll_iterations),
        },
        output,
    )


def _validate_options(
    card_limit: int | None,
    scroll_iterations: int,
    wait_ms: int,
    timeout_ms: int,
    workers: int,
) -> None:
    if card_limit is not None and card_limit < 1:
        raise ValueError("--card-limit must be 1 or greater.")
    if scroll_iterations < 0:
        raise ValueError("--scroll-iterations cannot be negative.")
    if wait_ms < 0 or timeout_ms < 1:
        raise ValueError("wait and timeout values must be non-negative.")
    if workers < 1:
        raise ValueError("--js-workers must be 1 or greater.")


def scrape_rendered_url_to_markdown(
    url: str,
    output: Path | None,
    title_override: str | None,
    scroll_iterations: int = DEFAULT_SCROLL_ITERATIONS,
    wait_ms: int = DEFAULT_WAIT_MS,
    timeout_ms: int = DEFAULT_TIMEOUT_MS,
    headed: bool = False,
) -> Path:
    _validate_options(None, scroll_iterations, wait_ms, timeout_ms, 1)
    return asyncio.run(
        _scrape_rendered_page(
            url,
            output,
            title_override,
            scroll_iterations,
            wait_ms,
            timeout_ms,
            headed,
        )
    )


def scrape_rendered_card_listing_to_markdown(
    url: str,
    output: Path | None,
    title_override: str | None,
    card_group: str = "all",
    card_limit: int | None = None,
    scroll_iterations: int = DEFAULT_SCROLL_ITERATIONS,
    wait_ms: int = DEFAULT_WAIT_MS,
    timeout_ms: int = DEFAULT_TIMEOUT_MS,
    workers: int = DEFAULT_WORKERS,
    headed: bool = False,
) -> Path:
    _validate_options(card_limit, scroll_iterations, wait_ms, timeout_ms, workers)
    return asyncio.run(
        _scrape_rendered_card_listing(
            url,
            output,
            title_override,
            card_group,
            card_limit,
            scroll_iterations,
            wait_ms,
            timeout_ms,
            workers,
            headed,
        )
    )


__all__ = [
    "RenderedPage",
    "event_cards_to_markdown",
    "markdown_from_rendered_html",
    "scrape_rendered_card_listing_to_markdown",
    "scrape_rendered_url_to_markdown",
]
