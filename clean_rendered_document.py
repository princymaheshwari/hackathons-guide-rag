"""Remove visual and duplicated scrape artifacts from rendered Markdown."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from scrape_web.rendered import markdown_from_rendered_html


LINKED_IMAGE_RE = re.compile(
    r"\[(?P<images>(?:\[Image:[^\]]*\])+)]\((?P<url>[^)]+)\)",
    re.IGNORECASE,
)
PLAIN_IMAGE_RE = re.compile(r"\[Image:[^\]]*\]", re.IGNORECASE)
STANDARD_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
RAW_IMAGE_URL_RE = re.compile(
    r"^https?://\S+\.(?:avif|gif|jpe?g|png|svg|webp)(?:\?\S*)?$",
    re.IGNORECASE,
)
HTML_FRAGMENT_RE = re.compile(r"</?[a-z][a-z0-9:-]*\b", re.IGNORECASE)
FINAL_URL_RE = re.compile(r"^- Final URL: \[[^]]*]\((?P<url>[^)]+)\)$", re.MULTILINE)
WEBSITE_SPLIT_RE = re.compile(r"(?=^### Website \d+:)", re.MULTILINE)
NOISE_BLOCK_RE = re.compile(
    r"^(?:"
    r"font awesome\s+fontawesome\.com|"
    r"player\s*[\u00b7-]\s*ready|"
    r"go somewhere|"
    r"end sponsors\s*&\s*partners|"
    r"slide\s+\d+|"
    r"[/#-]*main-nav|"
    r"[?<>|\u00d7\u2039\u203a\u2190\u2192]+"
    r")$",
    re.IGNORECASE,
)
GENERIC_IMAGE_LABELS = (
    "background",
    "banner",
    "binding",
    "bunny",
    "carousel",
    "corner img",
    "decor",
    "door and glow",
    "falling radish",
    "frame",
    "gallery image",
    "hero image",
    "icon",
    "lamp",
    "logo",
    "mascot",
    "memory",
    "pathway",
    "pattern",
    "placeholder",
    "project 1",
    "slide",
    "trust badge",
)


@dataclass
class CleaningStats:
    image_markers_removed: int = 0
    image_links_simplified: int = 0
    raw_image_urls_removed: int = 0
    html_blocks_converted: int = 0
    noise_blocks_removed: int = 0
    duplicate_blocks_removed: int = 0


def split_front_matter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end == -1:
        return "", text
    boundary_end = end + len("\n---\n")
    return text[:boundary_end], text[boundary_end:]


def source_url_from_front_matter(front_matter: str) -> str:
    match = re.search(r'^source_url:\s*"(?P<url>[^"]+)"', front_matter, re.MULTILINE)
    return match.group("url") if match else "https://www.mlh.com/"


def clean_url(url: str) -> str:
    parsed = urlsplit(url.strip())
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, parsed.query, ""))


def meaningful_image_label(label: str) -> str:
    cleaned = re.sub(r"\s+", " ", label).strip(" -|/")
    lowered = cleaned.casefold()
    if len(cleaned) < 2:
        return ""
    if lowered in {"image", "photo", "picture", "screenshot", "thumbnail"}:
        return ""
    if any(term in lowered for term in GENERIC_IMAGE_LABELS):
        return ""
    if lowered.startswith("major league hacking") and "season" in lowered:
        return ""
    return cleaned


def simplify_image_markup(text: str, stats: CleaningStats) -> str:
    def replace_linked_image(match: re.Match[str]) -> str:
        labels = [
            meaningful_image_label(marker[7:-1])
            for marker in PLAIN_IMAGE_RE.findall(match.group("images"))
        ]
        labels = list(dict.fromkeys(label for label in labels if label))
        stats.image_markers_removed += len(PLAIN_IMAGE_RE.findall(match.group("images")))
        if not labels:
            return ""
        stats.image_links_simplified += 1
        return f"[{' / '.join(labels)}]({clean_url(match.group('url'))})"

    text = LINKED_IMAGE_RE.sub(replace_linked_image, text)
    remaining_markers = len(PLAIN_IMAGE_RE.findall(text))
    stats.image_markers_removed += remaining_markers
    text = PLAIN_IMAGE_RE.sub("", text)
    standard_images = len(STANDARD_IMAGE_RE.findall(text))
    stats.image_markers_removed += standard_images
    text = STANDARD_IMAGE_RE.sub("", text)
    return text


def normalize_block(block: str) -> str:
    block = block.replace("\u22c5", "-")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in block.splitlines()]
    return "\n".join(line for line in lines if line).strip()


def normalized_key(block: str) -> str:
    return re.sub(r"\s+", " ", block).strip().casefold()


def should_remove_noise(block: str) -> bool:
    normalized = normalized_key(block)
    if not normalized:
        return True
    if not any(character.isalnum() for character in normalized):
        return True
    if RAW_IMAGE_URL_RE.fullmatch(normalized):
        return True
    if NOISE_BLOCK_RE.fullmatch(normalized):
        return True
    if normalized.startswith("lorem ipsum"):
        return True
    return False


def clean_blocks(
    text: str,
    base_url: str,
    stats: CleaningStats,
) -> list[str]:
    cleaned_blocks: list[str] = []
    for raw_block in re.split(r"\n\s*\n", text):
        block = raw_block.strip()
        if not block:
            continue

        if HTML_FRAGMENT_RE.search(block):
            converted = markdown_from_rendered_html(block, base_url)
            block = converted
            stats.html_blocks_converted += 1

        block = simplify_image_markup(block, stats)
        for candidate in re.split(r"\n\s*\n", block):
            candidate = normalize_block(candidate)
            if should_remove_noise(candidate):
                if RAW_IMAGE_URL_RE.fullmatch(normalized_key(candidate)):
                    stats.raw_image_urls_removed += 1
                else:
                    stats.noise_blocks_removed += 1
                continue
            cleaned_blocks.append(candidate)
    return cleaned_blocks


def deduplicate_website_blocks(
    blocks: list[str],
    stats: CleaningStats,
) -> list[str]:
    keys = [normalized_key(block) for block in blocks]
    counts = Counter(keys)
    seen: set[str] = set()
    kept: list[str] = []

    for block, key in zip(blocks, keys, strict=True):
        is_heading = block.startswith("#")
        duplicate_is_noise = (
            key in seen
            and (
                len(key) >= 40
                or counts[key] >= 3
                or (is_heading and len(key) >= 12)
            )
        )
        if duplicate_is_noise:
            stats.duplicate_blocks_removed += 1
            continue
        kept.append(block)
        seen.add(key)
    return kept


def clean_rendered_document(text: str) -> tuple[str, CleaningStats]:
    front_matter, body = split_front_matter(text)
    listing_url = source_url_from_front_matter(front_matter)
    marker = "## Linked Event Websites"
    if marker not in body:
        raise ValueError(
            "Expected a rendered card document containing '## Linked Event Websites'."
        )

    listing, website_text = body.split(marker, 1)
    stats = CleaningStats()
    listing_blocks = clean_blocks(listing, listing_url, stats)
    output_sections = ["\n\n".join(listing_blocks), marker]

    for section in WEBSITE_SPLIT_RE.split(website_text):
        if not section.strip():
            continue
        final_url_match = FINAL_URL_RE.search(section)
        base_url = final_url_match.group("url") if final_url_match else listing_url
        blocks = clean_blocks(section, base_url, stats)
        blocks = deduplicate_website_blocks(blocks, stats)
        output_sections.append("\n\n".join(blocks))

    cleaned_body = "\n\n".join(section for section in output_sections if section.strip())
    cleaned_body = re.sub(r"\n{3,}", "\n\n", cleaned_body).strip() + "\n"
    return front_matter + cleaned_body, stats


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clean image, raw-HTML, and duplicate artifacts from rendered Markdown."
    )
    parser.add_argument("path", type=Path, help="Rendered Markdown document to clean in place.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyze and print cleaning statistics without modifying the file.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.path.exists():
        raise FileNotFoundError(args.path)

    original = args.path.read_text(encoding="utf-8")
    cleaned, stats = clean_rendered_document(original)
    print(f"Input: {args.path}")
    print(f"Characters: {len(original)} -> {len(cleaned)}")
    print(f"Image markers removed: {stats.image_markers_removed}")
    print(f"Meaningful image links simplified: {stats.image_links_simplified}")
    print(f"Raw image URLs removed: {stats.raw_image_urls_removed}")
    print(f"Raw HTML blocks converted: {stats.html_blocks_converted}")
    print(f"Noise blocks removed: {stats.noise_blocks_removed}")
    print(f"Duplicate blocks removed: {stats.duplicate_blocks_removed}")

    if not args.dry_run:
        temporary_path = args.path.with_suffix(args.path.suffix + ".tmp")
        temporary_path.write_text(cleaned, encoding="utf-8")
        temporary_path.replace(args.path)
        print("Cleaned document written atomically.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
