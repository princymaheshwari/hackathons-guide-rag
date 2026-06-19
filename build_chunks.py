"""Build inspectable RAG chunks from cleaned Markdown documents.

Milestone 3 output is a flat JSON file, not a vector database. ChromaDB starts
in Milestone 4 after these chunks have been inspected.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from html import unescape
from pathlib import Path
from typing import Iterable


DOCUMENTS_DIR = Path("documents")
OUTPUT_PATH = Path("processed/chunks.json")
TARGET_TOKENS = 512
MAX_TOKENS = 720
OVERLAP_RATIO = 0.15

TOKEN_RE = re.compile(r"\w+(?:[-']\w+)*|[^\w\s]", re.UNICODE)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
SPECIAL_BLOCK_RE = re.compile(r"^###\s+(Row|Comment|Detail)\b.*", re.IGNORECASE)


def safe_print(text: str = "") -> None:
    """Print safely on Windows consoles that are not UTF-8."""
    encoding = sys.stdout.encoding or "utf-8"
    sys.stdout.write(text.encode(encoding, errors="replace").decode(encoding) + "\n")


@dataclass
class SourceDocument:
    path: Path
    metadata: dict[str, str]
    body: str
    title: str
    source_type: str


@dataclass
class TextBlock:
    text: str
    section_title: str | None
    block_type: str
    char_start: int
    char_end: int


def count_tokens(text: str) -> int:
    return len(TOKEN_RE.findall(text))


def token_windows(text: str, max_tokens: int, overlap_tokens: int) -> list[str]:
    tokens = TOKEN_RE.findall(text)
    if len(tokens) <= max_tokens:
        return [text.strip()] if text.strip() else []

    windows: list[str] = []
    step = max(1, max_tokens - overlap_tokens)
    for start in range(0, len(tokens), step):
        window = tokens[start : start + max_tokens]
        if not window:
            break
        windows.append(" ".join(window).strip())
        if start + max_tokens >= len(tokens):
            break
    return windows


def parse_front_matter(raw_text: str) -> tuple[dict[str, str], str]:
    if not raw_text.startswith("---\n"):
        return {}, raw_text

    lines = raw_text.splitlines()
    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break

    if end_index is None:
        return {}, raw_text

    metadata: dict[str, str] = {}
    for line in lines[1:end_index]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')

    body = "\n".join(lines[end_index + 1 :]).strip()
    return metadata, body


def clean_markdown_body(body: str) -> str:
    body = unescape(body)
    body = re.sub(r"<[^>\n]+>", "", body)
    body = body.replace("\r\n", "\n").replace("\r", "\n")
    return body.strip() + "\n"


def title_from_body(body: str, fallback: str) -> str:
    for line in body.splitlines():
        match = HEADING_RE.match(line.strip())
        if match:
            return match.group(2).strip()
    return fallback


def infer_source_type(path: Path, metadata: dict[str, str]) -> str:
    filename = path.name.lower()
    url = metadata.get("source_url", "").lower()
    raw_type = metadata.get("source_type", "").lower()

    if "reddit" in raw_type or "reddit.com" in url or "www-reddit-com" in filename:
        return "reddit"
    if "news.ycombinator.com" in url or filename.startswith("news-ycombinator-com"):
        return "hacker_news"
    if "mlh.com" in url or "major league hacking" in metadata.get("title", "").lower():
        return "mlh"
    if "devpost.com" in url or "devpost" in filename:
        return "devpost"
    if raw_type in {"html_table", "tabular_data"} or "docs-google" in filename:
        return "table"
    if any(
        marker in filename
        for marker in (
            "directory",
            "allhackathons",
            "kompulsa",
            "get-tech-180-student-hackathons",
            "compiled-list",
        )
    ):
        return "directory"
    if "guide" in filename or "guide" in metadata.get("title", "").lower():
        return "guide"
    return "blog"


def load_document(path: Path) -> SourceDocument:
    raw_text = path.read_text(encoding="utf-8")
    metadata, body = parse_front_matter(raw_text)
    body = clean_markdown_body(body)
    title = metadata.get("title") or title_from_body(body, path.stem)
    source_type = infer_source_type(path, metadata)
    return SourceDocument(path, metadata, body, title, source_type)


def line_offsets(lines: list[str]) -> list[int]:
    offsets: list[int] = []
    cursor = 0
    for line in lines:
        offsets.append(cursor)
        cursor += len(line) + 1
    return offsets


def block_type_for_heading(line: str) -> str:
    special = SPECIAL_BLOCK_RE.match(line.strip())
    if special:
        return special.group(1).lower()
    return "heading"


def split_paragraph_blocks(
    lines: list[str],
    offsets: list[int],
    start: int,
    end: int,
    section_title: str | None,
) -> list[TextBlock]:
    blocks: list[TextBlock] = []
    paragraph: list[str] = []
    paragraph_start = start

    def flush(current_index: int) -> None:
        nonlocal paragraph, paragraph_start
        text = "\n".join(paragraph).strip()
        if text:
            char_start = offsets[paragraph_start]
            last_line_index = max(paragraph_start, current_index - 1)
            char_end = offsets[last_line_index] + len(lines[last_line_index])
            blocks.append(
                TextBlock(
                    text=text,
                    section_title=section_title,
                    block_type="paragraph",
                    char_start=char_start,
                    char_end=char_end,
                )
            )
        paragraph = []
        paragraph_start = current_index + 1

    for index in range(start, end):
        line = lines[index]
        if not line.strip():
            flush(index)
            continue
        if not paragraph:
            paragraph_start = index
        paragraph.append(line)
    flush(end)
    return blocks


def parse_blocks(document: SourceDocument) -> list[TextBlock]:
    lines = document.body.splitlines()
    offsets = line_offsets(lines)
    blocks: list[TextBlock] = []
    heading_stack: list[tuple[int, str]] = []
    index = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        heading = HEADING_RE.match(stripped)

        if not stripped:
            index += 1
            continue

        if SPECIAL_BLOCK_RE.match(stripped):
            start = index
            index += 1
            while index < len(lines):
                next_line = lines[index].strip()
                if SPECIAL_BLOCK_RE.match(next_line):
                    break
                index += 1
            text = "\n".join(lines[start:index]).strip()
            blocks.append(
                TextBlock(
                    text=text,
                    section_title=HEADING_RE.match(stripped).group(2).strip()
                    if HEADING_RE.match(stripped)
                    else stripped.lstrip("#").strip(),
                    block_type=block_type_for_heading(stripped),
                    char_start=offsets[start],
                    char_end=offsets[index - 1] + len(lines[index - 1]),
                )
            )
            continue

        if heading:
            level = len(heading.group(1))
            title = heading.group(2).strip()
            heading_stack = [(lvl, text) for lvl, text in heading_stack if lvl < level]
            heading_stack.append((level, title))
            blocks.append(
                TextBlock(
                    text=stripped,
                    section_title=title,
                    block_type="heading",
                    char_start=offsets[index],
                    char_end=offsets[index] + len(line),
                )
            )
            index += 1
            continue

        start = index
        current_section = heading_stack[-1][1] if heading_stack else None
        while index < len(lines):
            next_line = lines[index].strip()
            if SPECIAL_BLOCK_RE.match(next_line) or HEADING_RE.match(next_line):
                break
            index += 1
        blocks.extend(split_paragraph_blocks(lines, offsets, start, index, current_section))

    return blocks


def split_oversized_block(block: TextBlock, max_tokens: int, overlap_tokens: int) -> list[TextBlock]:
    if count_tokens(block.text) <= max_tokens:
        return [block]

    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", block.text) if part.strip()]
    if len(paragraphs) > 1:
        split_blocks: list[TextBlock] = []
        for paragraph in paragraphs:
            if count_tokens(paragraph) <= max_tokens:
                split_blocks.append(
                    TextBlock(
                        text=paragraph,
                        section_title=block.section_title,
                        block_type=block.block_type,
                        char_start=block.char_start,
                        char_end=block.char_end,
                    )
                )
            else:
                split_blocks.extend(split_oversized_text(block, paragraph, max_tokens, overlap_tokens))
        return split_blocks

    return split_oversized_text(block, block.text, max_tokens, overlap_tokens)


def split_oversized_text(
    block: TextBlock,
    text: str,
    max_tokens: int,
    overlap_tokens: int,
) -> list[TextBlock]:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    if len(sentences) > 1:
        grouped: list[str] = []
        current: list[str] = []
        current_tokens = 0
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            sentence_tokens = count_tokens(sentence)
            if current and current_tokens + sentence_tokens > max_tokens:
                grouped.append(" ".join(current).strip())
                current = []
                current_tokens = 0
            if sentence_tokens > max_tokens:
                grouped.extend(token_windows(sentence, max_tokens, overlap_tokens))
                continue
            current.append(sentence)
            current_tokens += sentence_tokens
        if current:
            grouped.append(" ".join(current).strip())
        return [
            TextBlock(
                text=part,
                section_title=block.section_title,
                block_type=block.block_type,
                char_start=block.char_start,
                char_end=block.char_end,
            )
            for part in grouped
            if part.strip()
        ]

    return [
        TextBlock(
            text=part,
            section_title=block.section_title,
            block_type=block.block_type,
            char_start=block.char_start,
            char_end=block.char_end,
        )
        for part in token_windows(text, max_tokens, overlap_tokens)
    ]


def expanded_blocks(blocks: Iterable[TextBlock], max_tokens: int, overlap_tokens: int) -> list[TextBlock]:
    expanded: list[TextBlock] = []
    for block in blocks:
        expanded.extend(split_oversized_block(block, max_tokens, overlap_tokens))
    return expanded


def tail_overlap_blocks(blocks: list[TextBlock], overlap_tokens: int) -> list[TextBlock]:
    overlap: list[TextBlock] = []
    total = 0
    for block in reversed(blocks):
        tokens = count_tokens(block.text)
        if total + tokens > overlap_tokens and overlap:
            break
        if tokens > overlap_tokens:
            break
        overlap.insert(0, block)
        total += tokens
    return overlap


def should_start_new_chunk(current: list[TextBlock], next_block: TextBlock) -> bool:
    if not current:
        return False

    current_tokens = sum(count_tokens(block.text) for block in current)
    next_tokens = count_tokens(next_block.text)
    if current_tokens + next_tokens > MAX_TOKENS:
        return True

    hard_boundary_types = {"detail"}
    if next_block.block_type in hard_boundary_types and current_tokens >= TARGET_TOKENS // 2:
        return True

    previous_section = current[-1].section_title
    if (
        current_tokens >= TARGET_TOKENS
        and next_block.section_title
        and previous_section
        and next_block.section_title != previous_section
    ):
        return True

    return False


def build_chunk_text(blocks: list[TextBlock]) -> str:
    parts: list[str] = []
    for block in blocks:
        text = block.text.strip()
        if not text:
            continue
        if parts and parts[-1] == text:
            continue
        parts.append(text)
    return "\n\n".join(parts).strip()


def make_chunk(
    document: SourceDocument,
    blocks: list[TextBlock],
    position: int,
) -> dict[str, object]:
    text = build_chunk_text(blocks)
    token_count = count_tokens(text)
    section_titles = [block.section_title for block in blocks if block.section_title]
    section_title = section_titles[-1] if section_titles else None
    chunk_id = f"{document.path.stem}_{position + 1:04d}"

    return {
        "chunk_id": chunk_id,
        "text": text,
        "source_file": str(document.path.as_posix()),
        "source_filename": document.path.name,
        "source_url": document.metadata.get("source_url"),
        "source_type": document.source_type,
        "raw_source_type": document.metadata.get("source_type"),
        "title": document.title,
        "section_title": section_title,
        "chunk_position": position,
        "token_count": token_count,
        "char_start": min(block.char_start for block in blocks),
        "char_end": max(block.char_end for block in blocks),
        "metadata": {
            "collected_at": document.metadata.get("collected_at"),
            "capture_method": document.metadata.get("capture_method"),
        },
    }


def chunk_document(document: SourceDocument) -> list[dict[str, object]]:
    overlap_tokens = max(1, round(TARGET_TOKENS * OVERLAP_RATIO))
    blocks = expanded_blocks(parse_blocks(document), MAX_TOKENS, overlap_tokens)
    chunks: list[dict[str, object]] = []
    current: list[TextBlock] = []

    for block in blocks:
        if not block.text.strip():
            continue
        if should_start_new_chunk(current, block):
            chunks.append(make_chunk(document, current, len(chunks)))
            overlap = []
            if (
                block.block_type not in {"detail", "row", "comment"}
                and current
                and current[-1].section_title == block.section_title
            ):
                overlap = tail_overlap_blocks(current, overlap_tokens)
                overlap_tokens_count = sum(count_tokens(item.text) for item in overlap)
                if overlap_tokens_count + count_tokens(block.text) > MAX_TOKENS:
                    overlap = []
            current = [*overlap, block]
        else:
            current.append(block)

    if current:
        chunks.append(make_chunk(document, current, len(chunks)))

    return [chunk for chunk in chunks if str(chunk["text"]).strip()]


def build_chunks(documents_dir: Path) -> list[dict[str, object]]:
    chunks: list[dict[str, object]] = []
    for path in sorted(documents_dir.glob("*.md")):
        document = load_document(path)
        chunks.extend(chunk_document(document))
    return chunks


def write_chunks(chunks: list[dict[str, object]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(chunks, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def chunk_stats(chunks: list[dict[str, object]]) -> dict[str, object]:
    counts = [int(chunk["token_count"]) for chunk in chunks]
    if not counts:
        return {"total_chunks": 0}
    return {
        "total_chunks": len(chunks),
        "min_tokens": min(counts),
        "max_tokens": max(counts),
        "avg_tokens": round(sum(counts) / len(counts), 1),
        "over_max_chunks": sum(1 for count in counts if count > MAX_TOKENS),
    }


def print_samples(chunks: list[dict[str, object]], sample_count: int) -> None:
    if sample_count <= 0:
        return

    safe_print("\nSample chunks:")
    spread_indexes = []
    if chunks:
        step = max(1, len(chunks) // sample_count)
        spread_indexes = list(range(0, len(chunks), step))[:sample_count]

    for index in spread_indexes:
        chunk = chunks[index]
        text = str(chunk["text"])
        preview = text if len(text) <= 700 else text[:700].rstrip() + "..."
        safe_print("\n" + "=" * 80)
        safe_print(f"{chunk['chunk_id']} | {chunk['source_filename']} | {chunk['token_count']} tokens")
        safe_print(preview)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Milestone 3 chunks from cleaned Markdown docs.")
    parser.add_argument("--documents-dir", type=Path, default=DOCUMENTS_DIR)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--print-samples", type=int, default=5)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    chunks = build_chunks(args.documents_dir)
    write_chunks(chunks, args.output)
    stats = chunk_stats(chunks)

    safe_print(f"Wrote {stats['total_chunks']} chunks to {args.output}")
    safe_print(
        "Token stats: "
        f"min={stats.get('min_tokens')}, "
        f"avg={stats.get('avg_tokens')}, "
        f"max={stats.get('max_tokens')}, "
        f"over_max={stats.get('over_max_chunks')}"
    )
    print_samples(chunks, args.print_samples)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
