#!/usr/bin/env python3
"""Render extraction-test JSON files to simple, raw HTML.

Self-contained script — no external src/ dependencies.

Reads the extraction-test JSON schema produced by extract_structured_json.py:
  { pdf_id, total_pages, pages: [{ page_number, content: [{type, ...}] }] }

Content types handled: heading, paragraph, table, image, list, form,
                        link, video, header_footer

ADA remediation applied before rendering:
  - H1 demotion (only one H1 = document title)
  - Heading hierarchy normalization (no level skips)
  - Running header/footer deduplication
  - Duplicate content removal (paragraphs, images)
  - Consecutive list merging
  - Decorative image detection
  - Table header inference (only explicit _is_header, NOT auto row-0)
  - Empty page removal
  - Ordered list duplicate number stripping
  - Markdown-to-HTML conversion in all text fields
  - Duplicate link deduplication

No ARIA attributes, no stylesheets, no role attributes — raw simple HTML.

Usage:
    python render_json.py json_to_html_to_auditor/
    python render_json.py path/to/file.json
    python render_json.py path/to/dir/ -o /tmp/output/
    python render_json.py path/to/file.json --raw   # skip ADA remediation
"""

import argparse
import hashlib
import json
import re
import sys
from html import escape
from pathlib import Path


# ---------------------------------------------------------------------------
# Shared text processing — markdown to HTML conversion
# ---------------------------------------------------------------------------

def _md_to_html(text: str) -> str:
    """Convert markdown formatting in text to HTML.

    Handles: **bold**, *italic*, _italic_, [text](url), leader dots,
    literal <u> tags, and preserves newlines.
    Applied AFTER html-escaping the base text.
    """
    html_text = escape(text)

    # Unescape literal <u> and </u> tags that were in the source text
    html_text = html_text.replace("&lt;u&gt;", "<u>").replace("&lt;/u&gt;", "</u>")

    # Bold+Italic: ***text*** -> <strong><em>text</em></strong> (must come FIRST)
    html_text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", html_text, flags=re.DOTALL)
    # Bold: **text** -> <strong>text</strong> (DOTALL to span newlines)
    html_text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html_text, flags=re.DOTALL)
    # Italic: *text* -> <em>text</em> (but not inside <strong> tags)
    html_text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", html_text, flags=re.DOTALL)

    # Markdown underscore italic: _text_ -> <em>text</em>
    # Only match _word_ patterns (not filenames like my_file)
    html_text = re.sub(r"(?<!\w)_([^_]+?)_(?!\w)", r"<em>\1</em>", html_text)

    # Markdown links: [text](url) -> <a href="url">text</a>
    html_text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2">\1</a>',
        html_text,
    )

    # Leader dots: replace 4+ consecutive dots with a single ellipsis
    # Screen readers read each dot individually which is terrible UX
    html_text = re.sub(r"\.{4,}", "…", html_text)

    # Strip orphan/stray asterisks that don't form valid bold/italic pairs
    # These are artifacts from Gemini extraction (e.g., "** text" or "text **")
    # Only strip leading/trailing orphan ** or * that don't have a matching pair
    html_text = re.sub(r"^\s*\*{1,2}\s+", "", html_text)   # leading: "** text" -> "text"
    html_text = re.sub(r"\s+\*{1,2}\s*$", "", html_text)   # trailing: "text **" -> "text"

    # Collapse spaced-out letters (e.g., "A P P . A Z . g o v" -> "APP.AZ.gov")
    # Matches patterns where single chars are separated by spaces
    def _collapse_spaced(m: re.Match) -> str:
        return m.group(0).replace(" ", "")
    html_text = re.sub(r"(?<![a-zA-Z])([a-zA-Z] ){3,}[a-zA-Z](?![a-zA-Z])", _collapse_spaced, html_text)

    # Preserve newlines
    html_text = html_text.replace("\n", "<br>")
    return html_text


def _strip_list_prefix(text: str, list_type: str) -> str:
    """Strip leading number/letter prefixes from ordered list items.

    Removes patterns like: "1. ", "(1) ", "a. ", "b) ", "i. ", "iv. ", etc.
    Only strips from ordered lists to avoid removing bullet markers.
    """
    if list_type != "ordered":
        return text
    stripped = re.sub(
        r"^\s*(?:"
        r"\(?\d+[.)]\)?\s*"       # numeric: 1. 1) (1)
        r"|"
        r"\(?[a-zA-Z][.)]\)?\s*"  # letter: a. a) (a)
        r"|"
        r"\(?(?:i{1,3}|iv|vi{0,3}|ix|xi{0,3})[.)]\)?\s*"  # roman: i. ii. iii. iv.
        r")",
        "",
        text,
        count=1,
    )
    return stripped


def _detect_list_style(items: list) -> str:
    """Detect the list style type from the first item's prefix.

    Returns HTML ol type attribute value: '1' (numeric), 'a' (lowercase letter),
    'A' (uppercase letter), 'i' (lowercase roman), 'I' (uppercase roman).
    """
    for li in items:
        text = li.get("text", "") if isinstance(li, dict) else str(li)
        text = text.strip()
        if re.match(r"^\s*\(?\d+[.)]\)?", text):
            return "1"
        if re.match(r"^\s*\(?[a-z][.)]\)?", text):
            return "a"
        if re.match(r"^\s*\(?[A-Z][.)]\)?", text):
            return "A"
        if re.match(r"^\s*\(?(?:i{1,3}|iv|vi{0,3}|ix|xi{0,3})[.)]\)?", text):
            return "i"
        if re.match(r"^\s*\(?(?:I{1,3}|IV|VI{0,3}|IX|XI{0,3})[.)]\)?", text):
            return "I"
    return "1"


# ---------------------------------------------------------------------------
# ADA remediation — operates on the raw JSON data (list of pages)
# ---------------------------------------------------------------------------

def _apply_ada_remediation(data: dict) -> dict[str, int]:
    """Apply ADA remediation steps to extraction-test JSON. Mutates data in place."""
    stats: dict[str, int] = {}
    pages = data.get("pages", [])

    stats["h1_demoted"] = _demote_extra_h1s(pages)
    stats["headings_normalized"] = _normalize_heading_hierarchy(pages)
    stats["consecutive_headings_merged"] = _merge_consecutive_headings(pages)
    stats["running_headers_deduped"] = _deduplicate_running_headers(pages)
    stats["page_numbers_removed"] = _remove_page_numbers(pages)
    stats["duplicate_content_removed"] = _deduplicate_content(pages)
    stats["images_deduped"] = _deduplicate_images(pages)
    stats["lists_merged"] = _merge_consecutive_lists(pages)
    stats["decorative_images_marked"] = _mark_decorative_images(pages)
    stats["table_headers_inferred"] = _infer_table_headers(pages)
    stats["duplicate_links_removed"] = _deduplicate_links(pages)
    stats["boilerplate_removed"] = _remove_boilerplate(pages)
    stats["empty_pages_removed"] = _remove_empty_pages(pages)

    return stats


def _demote_extra_h1s(pages: list) -> int:
    """Ensure only the first H1 stays as H1; demote others to H2."""
    found_h1 = False
    count = 0
    for page in pages:
        for item in page.get("content", []):
            if item.get("type") == "heading" and item.get("level") == 1:
                if not found_h1:
                    found_h1 = True
                else:
                    item["level"] = 2
                    count += 1
    return count


def _normalize_heading_hierarchy(pages: list) -> int:
    """Fix heading level skips (e.g. H1 -> H4 becomes H1 -> H2)."""
    count = 0
    last_level = 0
    for page in pages:
        for item in page.get("content", []):
            if item.get("type") == "heading":
                level = item.get("level", 2)
                if last_level > 0 and level > last_level + 1:
                    new_level = last_level + 1
                    item["level"] = new_level
                    count += 1
                    last_level = new_level
                else:
                    last_level = level
    return count


def _merge_consecutive_headings(pages: list) -> int:
    """Merge consecutive headings of the same level into a single heading.

    Fixes cases like:
      <h2>NORTH CAROLINA 911 BOARD MEETING</h2>
      <h2>Wednesday, August 14, 2019</h2>
    Becomes:
      <h2>NORTH CAROLINA 911 BOARD MEETING — Wednesday, August 14, 2019</h2>
    """
    count = 0
    for page in pages:
        content = page.get("content", [])
        if len(content) < 2:
            continue
        merged = [content[0]]
        for item in content[1:]:
            prev = merged[-1]
            if (item.get("type") == "heading" and prev.get("type") == "heading"
                    and item.get("level") == prev.get("level")):
                prev_text = prev.get("text", "").strip()
                item_text = item.get("text", "").strip()
                prev["text"] = prev_text + " — " + item_text
                count += 1
            else:
                merged.append(item)
        page["content"] = merged
    return count


def _deduplicate_running_headers(pages: list) -> int:
    """Remove header_footer items that repeat identically across pages."""
    if len(pages) < 2:
        return 0

    # Collect header/footer texts per page
    hf_texts: dict[str, int] = {}
    for page in pages:
        for item in page.get("content", []):
            if item.get("type") == "header_footer":
                text = item.get("text", "").strip()
                # Normalize page numbers (e.g. "Page 1 of 12" -> "Page X of 12")
                normalized = re.sub(r"Page\s+\d+", "Page X", text)
                normalized = re.sub(r"^\d+$", "X", normalized)
                hf_texts[normalized] = hf_texts.get(normalized, 0) + 1

    # Texts appearing on more than half the pages are running headers
    threshold = max(2, len(pages) // 2)
    running = {t for t, c in hf_texts.items() if c >= threshold}

    count = 0
    for page in pages:
        original = page.get("content", [])
        filtered = []
        for item in original:
            if item.get("type") == "header_footer":
                text = item.get("text", "").strip()
                normalized = re.sub(r"Page\s+\d+", "Page X", text)
                normalized = re.sub(r"^\d+$", "X", normalized)
                if normalized in running:
                    count += 1
                    continue
            filtered.append(item)
        page["content"] = filtered
    return count


def _remove_page_numbers(pages: list) -> int:
    """Remove header_footer items that are page numbers.

    Matches patterns like: "1", "- 1 -", "Page 1", "Page 1 of 12",
    "1 | Page", "**2** | Page", "p. 1", "| 1 |", etc.
    """
    page_num_patterns = [
        r"^\s*\d+\s*$",                              # bare number: "1", " 12 "
        r"^\s*-\s*\d+\s*-\s*$",                       # dash-wrapped: "- 1 -"
        r"^\s*\|\s*\d+\s*\|\s*$",                     # pipe-wrapped: "| 1 |"
        r"^\s*page\s+\d+\s*$",                        # "Page 1"
        r"^\s*page\s+\d+\s+of\s+\d+\s*$",             # "Page 1 of 12"
        r"^\s*\d+\s+of\s+\d+\s*$",                    # "1 of 4", "2 of 4"
        r"^\s*p\.?\s*\d+\s*$",                         # "p. 1", "p1"
        r"^\s*\d+\s*\|\s*page\b",                      # "1 | Page"
        r"^\s*\*{0,2}\d+\*{0,2}\s*\|\s*page\b.*$",    # "**2** | Page (Rev ...)"
        r"^\s*\d+\s*\|\s*p\s*a\s*g\s*e\s*$",          # "3 | P a g e"
        r"^\s*\S+\s+page\s+\d+\s+of\s+\d+\b.*$",     # "00234464.25 Page 3 of 39 ..."
        r"^.*\|\s*page\s+\d+\s+of\s+\d+\s*\|.*$",    # "... | Page 37 of 39 | ..."
        r"^.*\|\s*page\s+\d+\s+of\s+\d+\s*$",        # "... | Page 33 of 123" (no trailing pipe)
        r"^.*\d+\s*\|\s*p\s*a\s*g\s*e\s*$",           # "Department of X 10 | P a g e"
        r"^.*\d+\s*\|\s*p\s*a\s*g\s*$",               # Truncated: "Department of X 10 | P a g"
        r"^.*\|\s*page\s+\d+\s*/\s*\d+\s*$",             # "... | Page 1/6"
        r"^.*\|\s*page\s+\d+\s*$",                        # "... | Page 33"
    ]
    combined = re.compile("|".join(page_num_patterns), re.IGNORECASE)

    count = 0
    for page in pages:
        original = page.get("content", [])
        filtered = []
        for item in original:
            if item.get("type") == "header_footer":
                text = item.get("text", "").strip()
                if combined.match(text):
                    count += 1
                    continue
            filtered.append(item)
        page["content"] = filtered
    return count


def _deduplicate_content(pages: list) -> int:
    """Remove duplicate paragraphs and headings across pages."""
    seen_texts: set[str] = set()
    count = 0
    for page in pages:
        original = page.get("content", [])
        filtered = []
        for item in original:
            if item.get("type") in ("paragraph", "heading"):
                text = item.get("text", "").strip()
                if not text:
                    continue
                # Use first 200 chars as dedup key
                key = text[:200].lower()
                if key in seen_texts:
                    count += 1
                    continue
                seen_texts.add(key)
            filtered.append(item)
        page["content"] = filtered
    return count


def _deduplicate_images(pages: list) -> int:
    """Remove duplicate images based on description AND base64 content."""
    seen_hashes: set[str] = set()
    seen_descs: set[str] = set()
    count = 0
    for page in pages:
        original = page.get("content", [])
        filtered = []
        for item in original:
            if item.get("type") == "image":
                b64 = item.get("base64_data") or ""
                desc = (item.get("description") or "").strip().lower()

                # Check by content hash first (most reliable)
                if b64:
                    content_hash = hashlib.md5(b64[:1000].encode()).hexdigest()
                    if content_hash in seen_hashes:
                        count += 1
                        continue
                    seen_hashes.add(content_hash)
                # Fall back to description dedup for images without base64
                elif desc and desc not in (
                    "unidentified image", "image", "decorative image"
                ):
                    if desc in seen_descs:
                        count += 1
                        continue
                    seen_descs.add(desc)
            filtered.append(item)
        page["content"] = filtered
    return count


def _merge_consecutive_lists(pages: list) -> int:
    """Merge consecutive lists of the same type."""
    count = 0
    for page in pages:
        content = page.get("content", [])
        if len(content) < 2:
            continue
        merged = [content[0]]
        for item in content[1:]:
            prev = merged[-1]
            if (item.get("type") == "list" and prev.get("type") == "list"
                    and item.get("list_type") == prev.get("list_type")):
                prev["items"].extend(item.get("items", []))
                count += 1
            else:
                merged.append(item)
        page["content"] = merged
    return count


def _mark_decorative_images(pages: list) -> int:
    """Mark images as decorative based on description, dimensions, AND content."""
    decorative_descriptions = {"", "decorative image"}
    generic_descriptions = {"unidentified image", "image", "logo"}
    count = 0
    for page in pages:
        for item in page.get("content", []):
            if item.get("type") == "image":
                desc = (item.get("description") or "").strip().lower()
                b64 = item.get("base64_data") or ""
                has_substantial_data = len(b64) > 500
                bbox = item.get("bbox")

                if desc in decorative_descriptions and not has_substantial_data:
                    item["_decorative"] = True
                    count += 1
                    continue

                if desc in generic_descriptions:
                    if not has_substantial_data:
                        item["_decorative"] = True
                        count += 1
                        continue
                    if bbox:
                        w = bbox.get("x1", 0) - bbox.get("x0", 0)
                        h = bbox.get("y1", 0) - bbox.get("y0", 0)
                        if w > 0 and h > 0 and (w < 10 or h < 10):
                            item["_decorative"] = True
                            count += 1
                            continue
                    if desc == "unidentified image":
                        item["description"] = "Document image"
                    continue

                if bbox:
                    w = bbox.get("x1", 0) - bbox.get("x0", 0)
                    h = bbox.get("y1", 0) - bbox.get("y0", 0)
                    if w > 0 and h > 0:
                        if w < 10 or h < 10:
                            item["_decorative"] = True
                            count += 1
                            continue
                        ratio = max(w, h) / min(w, h)
                        if ratio > 15:
                            item["_decorative"] = True
                            count += 1
                            continue
    return count


def _infer_table_headers(pages: list) -> int:
    """Mark row-0 cells as headers ONLY if they look like real headers.

    Criteria: all row-0 cells must be short text (< 60 chars), there must be
    at least 2 columns, AND none of the row-0 cells should contain mostly
    numeric data (which suggests data, not headers).
    """
    count = 0
    for page in pages:
        for item in page.get("content", []):
            if item.get("type") != "table":
                continue
            cells = item.get("cells", [])
            if not cells:
                continue
            row0 = [c for c in cells if c.get("row_start", 0) == 0]
            if not row0:
                continue
            all_short = all(len(c.get("text", "")) < 60 for c in row0)
            # Check that row-0 cells don't look like data (mostly numbers, dates, etc.)
            any_numeric = any(
                re.match(r"^\s*[\d$,.%]+\s*$", c.get("text", "").strip())
                for c in row0
                if c.get("text", "").strip()
            )
            if all_short and len(row0) >= 2 and not any_numeric:
                for c in row0:
                    c["_is_header"] = True
                count += 1
    return count


def _deduplicate_links(pages: list) -> int:
    """Remove standalone link elements whose URL already appears in paragraph text or as a prior link.

    Also fixes broken links: when a link has display text as its URL (e.g., href="CLICK HERE")
    and another link with the same display text has a valid URL, the broken one gets corrected.
    """
    count = 0

    # Pre-pass: fix broken link URLs by finding correct URLs for the same display text.
    # Build a map: normalized display text -> correct URL (from any link with a real URL)
    text_to_real_url: dict[str, str] = {}
    for page in pages:
        for item in page.get("content", []):
            if item.get("type") == "link":
                url = (item.get("url") or "").strip()
                text = (item.get("text") or "").strip()
                # A "real" URL starts with http/https/mailto/ftp or contains a dot
                if url and url != text and (
                    url.startswith(("http://", "https://", "mailto:", "ftp://"))
                    or "." in url
                ):
                    norm_text = " ".join(text.split()).lower()
                    if norm_text:
                        text_to_real_url[norm_text] = url

    # Fix broken links using the map
    for page in pages:
        for item in page.get("content", []):
            if item.get("type") == "link":
                url = (item.get("url") or "").strip()
                text = (item.get("text") or "").strip()
                # Check if URL looks broken (url == text and not a real URL)
                url_is_broken = (
                    url == text
                    or (not url.startswith(("http://", "https://", "mailto:", "ftp://", "/"))
                        and "." not in url)
                )
                if url_is_broken:
                    norm_text = " ".join(text.split()).lower()
                    if norm_text in text_to_real_url:
                        item["url"] = text_to_real_url[norm_text]

    # First pass: collect ALL URLs mentioned in paragraphs/headings across ALL pages
    global_text_urls: set[str] = set()
    for page in pages:
        for item in page.get("content", []):
            if item.get("type") in ("paragraph", "heading"):
                text = item.get("text", "")
                for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
                    global_text_urls.add(match.group(2).strip().lower())
                for match in re.finditer(r"https?://\S+", text):
                    global_text_urls.add(match.group(0).strip().lower())

    # Second pass: remove duplicate link items (globally tracked)
    global_seen_urls: set[str] = set()
    for page in pages:
        content = page.get("content", [])
        filtered = []
        for item in content:
            if item.get("type") == "link":
                url = (item.get("url") or "").strip().lower()
                # Remove if URL already in paragraph text or already seen as a standalone link
                if url in global_text_urls or url in global_seen_urls:
                    count += 1
                    continue
                global_seen_urls.add(url)
            filtered.append(item)
        page["content"] = filtered
    return count


def _remove_boilerplate(pages: list) -> int:
    """Remove boilerplate content like 'page intentionally left blank'."""
    boilerplate_patterns = [
        r"^\s*(?:this\s+)?page\s+(?:is\s+)?intentionally\s+left\s+blank\s*\.?\s*$",
        r"^\s*(?:this\s+)?page\s+left\s+(?:intentionally\s+)?blank\s*\.?\s*$",
    ]
    combined = re.compile("|".join(boilerplate_patterns), re.IGNORECASE)
    count = 0
    for page in pages:
        original = page.get("content", [])
        filtered = []
        for item in original:
            if item.get("type") in ("paragraph", "heading"):
                text = item.get("text", "").strip()
                if combined.match(text):
                    count += 1
                    continue
            filtered.append(item)
        page["content"] = filtered
    return count


def _remove_empty_pages(pages: list) -> int:
    """Remove pages with no content after deduplication."""
    count = 0
    i = 0
    while i < len(pages):
        if not pages[i].get("content"):
            pages.pop(i)
            count += 1
        else:
            i += 1
    return count


# ---------------------------------------------------------------------------
# HTML rendering — simple, raw HTML output
# ---------------------------------------------------------------------------

def _s(val, default: str = "") -> str:
    """Safely convert a value to str, treating None as default."""
    return default if val is None else str(val)


def _render_heading(item: dict) -> str:
    level = max(1, min(6, item.get("level", 2)))
    text = _md_to_html(_s(item.get("text")))
    return f"<h{level}>{text}</h{level}>"


def _render_paragraph(item: dict) -> str:
    text = _s(item.get("text"))
    html_text = _md_to_html(text)
    return f"<p>{html_text}</p>"


def _render_table(item: dict) -> str:
    cells = item.get("cells", [])
    if not cells:
        caption = item.get("caption") or item.get("title") or "Empty table"
        return f"<table><caption>{escape(caption)}</caption><tr><td>(empty table)</td></tr></table>"

    max_row = max(c.get("row_start", 0) for c in cells)
    max_col = max(c.get("column_start", 0) for c in cells)

    # Build a lookup: (row, col) -> cell
    cell_map: dict[tuple[int, int], dict] = {}
    for c in cells:
        key = (c.get("row_start", 0), c.get("column_start", 0))
        cell_map[key] = c

    # Track which cells are covered by rowspan/colspan
    covered: set[tuple[int, int]] = set()
    for c in cells:
        r = c.get("row_start", 0)
        col = c.get("column_start", 0)
        rs = c.get("num_rows", c.get("row_span", 1)) or 1
        cs = c.get("num_columns", c.get("column_span", 1)) or 1
        for dr in range(rs):
            for dc in range(cs):
                if dr == 0 and dc == 0:
                    continue
                covered.add((r + dr, col + dc))

    caption = item.get("caption") or item.get("title") or ""
    caption_html = f"<caption>{escape(caption)}</caption>" if caption else ""

    html = f"<table>{caption_html}"

    for r in range(max_row + 1):
        html += "<tr>"
        for c_idx in range(max_col + 1):
            if (r, c_idx) in covered:
                continue
            cell = cell_map.get((r, c_idx))
            if cell is None:
                html += "<td></td>"
                continue

            cell_text = _md_to_html(_s(cell.get("text")))
            # ONLY use _is_header flag — do NOT auto-mark row 0 as header
            is_header = cell.get("_is_header", False)
            tag = "th" if is_header else "td"
            attrs = ""

            rs = cell.get("num_rows", cell.get("row_span", 1)) or 1
            cs = cell.get("num_columns", cell.get("column_span", 1)) or 1
            if rs > 1:
                attrs += f' rowspan="{rs}"'
            if cs > 1:
                attrs += f' colspan="{cs}"'

            html += f"<{tag}{attrs}>{cell_text}</{tag}>"
        html += "</tr>"

    html += "</table>"
    return html


def _render_image(item: dict) -> str:
    desc = _s(item.get("description"))
    caption = _s(item.get("caption"))
    # Treat "Document image" / "document image" as generic — mark decorative if no real data
    is_decorative = item.get("_decorative", False) or not desc or desc.lower() in (
        "unidentified image", "image", "decorative image", "document image",
    )
    b64 = item.get("base64_data", "")
    fmt = item.get("format", "png")

    if is_decorative:
        if b64:
            return f'<img src="data:image/{fmt};base64,{b64}" alt="">'
        return "<!-- decorative image -->"

    alt_text = escape(desc)
    if b64:
        src = f"data:image/{fmt};base64,{b64}"
        img_tag = f'<img src="{src}" alt="{alt_text}">'
    else:
        # Render as visible text placeholder instead of hidden comment
        # so screen readers and users know an image was intended here
        return f"<p>[Image: {alt_text}]</p>"

    if caption:
        cap_stripped = caption.strip()
        # Suppress meaningless figcaptions: very short (< 5 chars), pure numbers/percentages,
        # or generic phrases that don't describe the image
        is_meaningless = (
            len(cap_stripped) < 5
            or re.match(r"^\s*[\d,.%$]+\s*$", cap_stripped)
            or cap_stripped.lower() in ("image", "figure", "photo", "logo", "icon")
        )
        if not is_meaningless:
            return f"<figure>{img_tag}<figcaption>{escape(caption)}</figcaption></figure>"
    return img_tag


def _render_list(item: dict) -> str:
    list_type = item.get("list_type", "unordered")
    tag = "ol" if list_type == "ordered" else "ul"

    # Detect list style (a, A, i, I, 1) and start number from first item prefix
    ol_attrs = ""
    if list_type == "ordered":
        items = item.get("items", [])
        style = _detect_list_style(items)
        if style != "1":
            ol_attrs += f' type="{style}"'
        # Detect start number from first item
        if items:
            first_text = items[0].get("text", "") if isinstance(items[0], dict) else str(items[0])
            first_text = first_text.strip()
            m = re.match(r"^\s*\(?(\d+)[.)]\)?", first_text)
            if m and int(m.group(1)) > 1:
                ol_attrs += f' start="{m.group(1)}"'

    items_html = ""
    for li in item.get("items", []):
        text = li.get("text", "") if isinstance(li, dict) else str(li)
        # Strip duplicate numbering from ordered list items
        text = _strip_list_prefix(text, list_type)
        li_html = _md_to_html(text)
        # Render children as nested list
        children = li.get("children", []) if isinstance(li, dict) else []
        if children:
            child_tag = "ol" if list_type == "ordered" else "ul"
            li_html += f"<{child_tag}>"
            for child in children:
                child_text = child.get("text", "") if isinstance(child, dict) else str(child)
                child_text = _strip_list_prefix(child_text, list_type)
                li_html += f"<li>{_md_to_html(child_text)}</li>"
            li_html += f"</{child_tag}>"
        items_html += f"<li>{li_html}</li>"
    return f"<{tag}{ol_attrs}>{items_html}</{tag}>"


def _render_form(item: dict) -> str:
    title = item.get("title", "Form")
    fields = item.get("fields", [])
    if not fields:
        return f"<table><caption>{escape(title)}</caption><tr><td>(empty form)</td></tr></table>"

    html = "<table>"
    html += f"<caption>{escape(title)}</caption>"
    html += "<tr><th>Field</th><th>Type</th><th>Value</th></tr>"
    for field in fields:
        label = escape(_s(field.get("label")))
        ftype = escape(_s(field.get("field_type")))
        value = field.get("value")
        value_str = escape(str(value)) if value is not None else ""

        options = field.get("options", [])
        if options:
            value_str += " [" + ", ".join(escape(str(o)) for o in options) + "]"

        html += f"<tr><td>{label}</td><td>{ftype}</td><td>{value_str}</td></tr>"
    html += "</table>"
    return html


def _render_link(item: dict) -> str:
    text = escape(_s(item.get("text")))
    url = _s(item.get("url"))
    url_esc = escape(url)
    return f'<p><a href="{url_esc}">{text}</a></p>'


def _render_video(item: dict) -> str:
    url = escape(_s(item.get("url")))
    desc = escape(_s(item.get("description"), "Video"))
    return f'<p><a href="{url}">{desc}</a></p>'


def _render_header_footer(item: dict) -> str:
    # Simple rendering — no role attributes, no <small>, markdown converted
    text = _md_to_html(_s(item.get("text")))
    return f"<p>{text}</p>"


# Dispatch table
_RENDERERS = {
    "heading": _render_heading,
    "paragraph": _render_paragraph,
    "table": _render_table,
    "image": _render_image,
    "list": _render_list,
    "form": _render_form,
    "link": _render_link,
    "video": _render_video,
    "header_footer": _render_header_footer,
}


def render_content_item(item: dict) -> str:
    """Render a single content item. NEVER returns empty string."""
    renderer = _RENDERERS.get(item.get("type", ""), None)
    if renderer:
        result = renderer(item)
        if result and result.strip():
            return result
        return _render_fallback(item)
    return _render_fallback(item)


def _render_fallback(item: dict) -> str:
    """Fallback renderer — guarantees non-empty output for any item."""
    item_type = escape(_s(item.get("type"), "unknown"))
    text = _s(item.get("text") or item.get("description") or item.get("title") or "")
    if text:
        return f"<p>{_md_to_html(text)}</p>"
    return f"<!-- {item_type} element (no text content) -->"


# ---------------------------------------------------------------------------
# Full document rendering
# ---------------------------------------------------------------------------

def _element_id(page_idx: int, item_idx: int, item: dict) -> str:
    """Generate a unique ID for an element based on position and content."""
    item_type = item.get("type", "unknown")
    text = _s(item.get("text") or item.get("description") or item.get("title") or "")
    return f"p{page_idx}:i{item_idx}:{item_type}:{text[:50]}"


def _reconcile_and_render(pages: list, max_passes: int = 3) -> list[tuple[int, int, dict, str]]:
    """Render all elements and reconcile until every element is accounted for."""
    expected: list[tuple[int, int, dict]] = []
    for page_idx, page in enumerate(pages):
        for item_idx, item in enumerate(page.get("content", [])):
            expected.append((page_idx, item_idx, item))

    results: list[tuple[int, int, dict, str]] = []
    missing: list[tuple[int, int, dict]] = []

    for page_idx, item_idx, item in expected:
        rendered = render_content_item(item)
        if rendered and rendered.strip():
            results.append((page_idx, item_idx, item, rendered))
        else:
            missing.append((page_idx, item_idx, item))

    if not missing:
        return results

    for page_idx, item_idx, item in missing:
        fallback = _render_fallback(item)
        insert_pos = 0
        for k, (pi, ii, _, _) in enumerate(results):
            if (pi, ii) < (page_idx, item_idx):
                insert_pos = k + 1
        results.insert(insert_pos, (page_idx, item_idx, item, fallback))

    if max_passes > 1:
        rendered_ids = {_element_id(pi, ii, it) for pi, ii, it, _ in results}
        expected_ids = {_element_id(pi, ii, it) for pi, ii, it in expected}
        still_missing = expected_ids - rendered_ids
        if still_missing:
            return _reconcile_and_render(pages, max_passes - 1)

    return results


def render_document(data: dict) -> str:
    pdf_id = data.get("pdf_id", "Document")
    title = pdf_id.replace("-", " ").title()

    pages = data.get("pages", [])

    rendered_elements = _reconcile_and_render(pages)

    expected_count = sum(len(p.get("content", [])) for p in pages)
    actual_count = len(rendered_elements)
    if actual_count != expected_count:
        print(
            f"  INTEGRITY ERROR: expected {expected_count} elements, "
            f"got {actual_count} after reconciliation",
            file=sys.stderr,
        )

    # Assemble HTML — no page breaks at all
    body_lines = []
    for page_idx, item_idx, item, html in rendered_elements:
        body_lines.append(html)

    body_html = "\n".join(body_lines)

    # Raw simple HTML — no stylesheets, no ARIA, no roles
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{escape(title)}</title>
</head>
<body>
{body_html}
</body>
</html>"""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def render_one(json_path: Path, output_path: Path, raw: bool = False) -> bool | None:
    """Render a single JSON file to HTML. Returns True on success, False on error, None if skipped."""
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))

        if "pages" not in data:
            return None

        pre_count = sum(len(p.get("content", [])) for p in data.get("pages", []))

        if not raw:
            stats = _apply_ada_remediation(data)
            changes = {k: v for k, v in stats.items() if v > 0}
            if changes:
                parts = ", ".join(f"{k}={v}" for k, v in changes.items())
                print(f"  ADA  {json_path.name}: {parts}")

        post_count = sum(len(p.get("content", [])) for p in data.get("pages", []))

        html = render_document(data)

        rendered_count = 0
        missing_elements = []
        for page_idx, page in enumerate(data.get("pages", [])):
            for item_idx, item in enumerate(page.get("content", [])):
                r = render_content_item(item)
                if r and r.strip():
                    rendered_count += 1
                else:
                    missing_elements.append(
                        f"pg{page.get('page_number', page_idx+1)}[{item_idx}] "
                        f"type={item.get('type')}"
                    )

        if missing_elements:
            print(
                f"  WARN {json_path.name}: {len(missing_elements)} elements "
                f"produced empty renders: {', '.join(missing_elements)}",
                file=sys.stderr,
            )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")
        ada_note = f", ADA removed {pre_count - post_count}" if not raw and pre_count != post_count else ""
        print(
            f"  OK   {json_path.name} -> {output_path.name} "
            f"({len(html):,} bytes, {rendered_count}/{pre_count} elements{ada_note})"
        )
        return True
    except Exception as e:
        print(f"  FAIL {json_path.name}: {e}", file=sys.stderr)
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render extraction-test JSON to simple raw HTML."
    )
    parser.add_argument(
        "input", type=Path,
        help="Path to a .json file, a directory of .json files, or a parent "
             "directory with subdirectories containing .json files",
    )
    parser.add_argument(
        "-o", "--output", type=Path, default=None,
        help="Output HTML path (single file) or directory (batch mode)",
    )
    parser.add_argument(
        "--raw", action="store_true",
        help="Skip ADA post-processing (raw render only)",
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: {args.input} not found", file=sys.stderr)
        sys.exit(1)

    if args.input.is_file():
        out = args.output or args.input.with_suffix(".html")
        if not render_one(args.input, out, raw=args.raw):
            sys.exit(1)
        return

    json_files = sorted(args.input.glob("*.json"))
    nested = sorted(args.input.glob("*/*.json"))
    if nested:
        json_files.extend(nested)
    if not json_files:
        print(f"No .json files found in {args.input}", file=sys.stderr)
        sys.exit(1)

    out_dir = args.output or args.input
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Found {len(json_files)} JSON files in {args.input}/\n")
    ok, fail, skipped = 0, 0, 0
    for jf in json_files:
        if args.output:
            rel = jf.relative_to(args.input)
            html_path = out_dir / rel.with_suffix(".html")
        else:
            html_path = jf.with_suffix(".html")

        result = render_one(jf, html_path, raw=args.raw)
        if result is True:
            ok += 1
        elif result is False:
            fail += 1
        else:
            skipped += 1

    print(f"\nDone: {ok} rendered, {fail} failed, {skipped} skipped")
    if fail > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
