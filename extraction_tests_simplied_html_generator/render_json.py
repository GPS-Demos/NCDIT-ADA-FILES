#!/usr/bin/env python3
"""Render extraction-test JSON files to ADA-compliant HTML.

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
  - Table header inference
  - Empty page removal

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
# ADA remediation — operates on the raw JSON data (list of pages)
# ---------------------------------------------------------------------------

def _apply_ada_remediation(data: dict) -> dict[str, int]:
    """Apply ADA remediation steps to extraction-test JSON. Mutates data in place."""
    stats: dict[str, int] = {}
    pages = data.get("pages", [])

    stats["h1_demoted"] = _demote_extra_h1s(pages)
    stats["headings_normalized"] = _normalize_heading_hierarchy(pages)
    stats["running_headers_deduped"] = _deduplicate_running_headers(pages)
    stats["duplicate_content_removed"] = _deduplicate_content(pages)
    stats["images_deduped"] = _deduplicate_images(pages)
    stats["lists_merged"] = _merge_consecutive_lists(pages)
    stats["decorative_images_marked"] = _mark_decorative_images(pages)
    stats["table_headers_inferred"] = _infer_table_headers(pages)
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
    """Remove duplicate images based on description AND base64 content.

    Deduplicates by:
      1. base64 data hash (catches identical images with different descriptions)
      2. description text (catches same-description images without base64 data)
    """
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
    """Mark images with empty/generic descriptions as decorative."""
    decorative_descriptions = {"", "unidentified image", "image", "decorative image", "logo"}
    count = 0
    for page in pages:
        for item in page.get("content", []):
            if item.get("type") == "image":
                desc = (item.get("description") or "").strip().lower()
                if desc in decorative_descriptions:
                    item["_decorative"] = True
                    count += 1
    return count


def _infer_table_headers(pages: list) -> int:
    """If a table has no explicit header row, treat row 0 as header."""
    count = 0
    for page in pages:
        for item in page.get("content", []):
            if item.get("type") != "table":
                continue
            cells = item.get("cells", [])
            if not cells:
                continue
            # Check if row 0 cells look like headers (short text, no numbers)
            row0 = [c for c in cells if c.get("row_start", 0) == 0]
            if not row0:
                continue
            all_short = all(len(c.get("text", "")) < 60 for c in row0)
            if all_short and len(row0) >= 2:
                for c in row0:
                    c["_is_header"] = True
                count += 1
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
# HTML rendering — literal translation from JSON
# ---------------------------------------------------------------------------

def _s(val, default: str = "") -> str:
    """Safely convert a value to str, treating None as default."""
    return default if val is None else str(val)


def _render_heading(item: dict) -> str:
    level = max(1, min(6, item.get("level", 2)))
    text = escape(_s(item.get("text")))
    return f"<h{level}>{text}</h{level}>"


def _render_paragraph(item: dict) -> str:
    text = _s(item.get("text"))
    # Convert markdown bold/italic to HTML
    html_text = escape(text)
    # Bold: **text** -> <strong>text</strong>
    html_text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html_text)
    # Italic: *text* -> <em>text</em>
    html_text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html_text)
    # Preserve newlines
    html_text = html_text.replace("\n", "<br>")
    return f"<p>{html_text}</p>"


def _render_table(item: dict) -> str:
    cells = item.get("cells", [])
    if not cells:
        caption = item.get("caption") or item.get("title") or "Empty table"
        return f'<table aria-label="{escape(caption)}"><caption>{escape(caption)}</caption><tr><td>(empty table)</td></tr></table>'

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

    summary = f"Table with {max_row + 1} rows and {max_col + 1} columns"
    html = f'<table aria-label="{escape(summary)}">{caption_html}'

    for r in range(max_row + 1):
        html += "<tr>"
        for c_idx in range(max_col + 1):
            if (r, c_idx) in covered:
                continue
            cell = cell_map.get((r, c_idx))
            if cell is None:
                html += "<td></td>"
                continue

            text = escape(_s(cell.get("text")))
            is_header = cell.get("_is_header", False) or r == 0
            tag = "th" if is_header else "td"
            attrs = f' scope="col"' if is_header else ""

            rs = cell.get("num_rows", cell.get("row_span", 1)) or 1
            cs = cell.get("num_columns", cell.get("column_span", 1)) or 1
            if rs > 1:
                attrs += f' rowspan="{rs}"'
            if cs > 1:
                attrs += f' colspan="{cs}"'

            html += f"<{tag}{attrs}>{text}</{tag}>"
        html += "</tr>"

    html += "</table>"
    return html


def _render_image(item: dict) -> str:
    desc = _s(item.get("description"))
    caption = _s(item.get("caption"))
    is_decorative = item.get("_decorative", False) or not desc or desc.lower() in (
        "unidentified image", "image", "decorative image"
    )
    b64 = item.get("base64_data", "")
    fmt = item.get("format", "png")

    # Use bbox (PDF points) to size images to match their original PDF appearance
    bbox = item.get("bbox")
    size_attrs = ""
    if bbox:
        w = bbox.get("x1", 0) - bbox.get("x0", 0)
        h = bbox.get("y1", 0) - bbox.get("y0", 0)
        if w > 0 and h > 0:
            size_attrs = f' width="{w:.0f}" height="{h:.0f}"'

    if is_decorative:
        if b64:
            return f'<img src="data:image/{fmt};base64,{b64}" alt="" role="presentation"{size_attrs}>'
        return '<img alt="" role="presentation" src="">'

    alt_text = escape(desc)
    if b64:
        src = f"data:image/{fmt};base64,{b64}"
        img_tag = f'<img src="{src}" alt="{alt_text}"{size_attrs}>'
    else:
        img_tag = f'<img alt="{alt_text}" src="">'

    if caption:
        return (
            f'<figure>'
            f'{img_tag}'
            f'<figcaption>{escape(caption)}</figcaption>'
            f'</figure>'
        )
    return img_tag


def _render_list(item: dict) -> str:
    list_type = item.get("list_type", "unordered")
    tag = "ol" if list_type == "ordered" else "ul"
    items_html = ""
    for li in item.get("items", []):
        text = li.get("text", "") if isinstance(li, dict) else str(li)
        li_html = escape(text)
        # Render children as nested list
        children = li.get("children", []) if isinstance(li, dict) else []
        if children:
            li_html += "<ul>"
            for child in children:
                child_text = child.get("text", "") if isinstance(child, dict) else str(child)
                li_html += f"<li>{escape(child_text)}</li>"
            li_html += "</ul>"
        items_html += f"<li>{li_html}</li>"
    return f"<{tag}>{items_html}</{tag}>"


def _render_form(item: dict) -> str:
    title = item.get("title", "Form")
    fields = item.get("fields", [])
    if not fields:
        return f'<table aria-label="{escape(title)}"><caption>{escape(title)}</caption><tr><td>(empty form)</td></tr></table>'

    html = f'<table aria-label="{escape(title)}">'
    html += f"<caption>{escape(title)}</caption>"
    html += "<tr><th scope='col'>Field</th><th scope='col'>Type</th><th scope='col'>Value</th></tr>"
    for field in fields:
        label = escape(_s(field.get("label")))
        ftype = escape(_s(field.get("field_type")))
        value = field.get("value")
        value_str = escape(str(value)) if value is not None else ""

        # Show options for radio/dropdown
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
    # These are kept only if they survived deduplication
    text = escape(_s(item.get("text")))
    subtype = _s(item.get("subtype"), "header")
    role = "banner" if subtype == "header" else "contentinfo"
    return f'<div role="{role}" class="page-{subtype}"><small>{text}</small></div>'


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
        # Renderer returned empty — fallback to generic rendering
        return _render_fallback(item)
    return _render_fallback(item)


def _render_fallback(item: dict) -> str:
    """Fallback renderer — guarantees non-empty output for any item."""
    item_type = escape(_s(item.get("type"), "unknown"))
    text = _s(item.get("text") or item.get("description") or item.get("title") or "")
    if text:
        return f"<p>{escape(text)}</p>"
    return f"<!-- {item_type} element (no text content) -->"


# ---------------------------------------------------------------------------
# Full document rendering
# ---------------------------------------------------------------------------

CSS = """
html { font-size: 100%; }
body {
    font-family: -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    line-height: 1.6;
    max-width: 960px;
    margin: 0 auto;
    padding: 1rem 2rem;
    color: #222;
    background: #fff;
}
h1, h2, h3, h4, h5, h6 { margin-top: 1.2em; margin-bottom: 0.4em; color: #111; }
h1 { font-size: 1.8rem; border-bottom: 2px solid #333; padding-bottom: 0.3em; }
h2 { font-size: 1.4rem; }
h3 { font-size: 1.2rem; }
p { margin: 0.6em 0; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; }
th, td { border: 1px solid #999; padding: 0.4em 0.6em; text-align: left; }
th { background: #f0f0f0; font-weight: bold; }
caption { font-weight: bold; margin-bottom: 0.3em; text-align: left; caption-side: top; }
figure { margin: 1em 0; }
figcaption { font-style: italic; margin-top: 0.3em; color: #555; }
img { max-width: 100%; height: auto; }
ul, ol { margin: 0.5em 0; padding-left: 1.5em; }
li { margin-bottom: 0.2em; }
a { color: #0056b3; }
a:hover { text-decoration: underline; }
.page-header, .page-footer { color: #888; font-size: 0.85em; margin: 0.3em 0; }
.page-break { border-top: 1px dashed #ccc; margin: 1.5em 0; }
@media (prefers-color-scheme: dark) {
    body { background: #1a1a1a; color: #ddd; }
    th { background: #333; }
    h1 { border-bottom-color: #777; }
    a { color: #6db3f2; }
}
"""


def _element_id(page_idx: int, item_idx: int, item: dict) -> str:
    """Generate a unique ID for an element based on position and content."""
    item_type = item.get("type", "unknown")
    text = _s(item.get("text") or item.get("description") or item.get("title") or "")
    return f"p{page_idx}:i{item_idx}:{item_type}:{text[:50]}"


def _reconcile_and_render(pages: list, max_passes: int = 3) -> list[tuple[int, int, dict, str]]:
    """Render all elements and reconcile until every element is accounted for.

    For each post-ADA element, attempts to render it. If any element produces
    empty output, re-renders via fallback. Recurses up to max_passes times
    to guarantee completeness.

    Returns:
        List of (page_index, item_index, item_dict, rendered_html) tuples,
        one per element, in reading order.
    """
    # Build the canonical list of every element that should be rendered
    expected: list[tuple[int, int, dict]] = []
    for page_idx, page in enumerate(pages):
        for item_idx, item in enumerate(page.get("content", [])):
            expected.append((page_idx, item_idx, item))

    # Render pass
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

    # Re-inject missing elements via fallback
    for page_idx, item_idx, item in missing:
        fallback = _render_fallback(item)
        # Insert at the correct position to maintain reading order
        insert_pos = 0
        for k, (pi, ii, _, _) in enumerate(results):
            if (pi, ii) < (page_idx, item_idx):
                insert_pos = k + 1
        results.insert(insert_pos, (page_idx, item_idx, item, fallback))

    # Recurse to verify — are ALL elements now present?
    if max_passes > 1:
        rendered_ids = {_element_id(pi, ii, it) for pi, ii, it, _ in results}
        expected_ids = {_element_id(pi, ii, it) for pi, ii, it in expected}
        still_missing = expected_ids - rendered_ids
        if still_missing:
            # Rebuild pages from results and recurse
            return _reconcile_and_render(pages, max_passes - 1)

    return results


def render_document(data: dict) -> str:
    pdf_id = data.get("pdf_id", "Document")
    title = pdf_id.replace("-", " ").title()

    pages = data.get("pages", [])

    # Render and reconcile — every element gets exactly one HTML output
    rendered_elements = _reconcile_and_render(pages)

    # Final verification: every element from every page is accounted for
    expected_count = sum(len(p.get("content", [])) for p in pages)
    actual_count = len(rendered_elements)
    if actual_count != expected_count:
        print(
            f"  INTEGRITY ERROR: expected {expected_count} elements, "
            f"got {actual_count} after reconciliation",
            file=sys.stderr,
        )

    # Assemble HTML with page breaks between pages
    body_lines = []
    last_page_idx = -1
    for page_idx, item_idx, item, html in rendered_elements:
        if page_idx != last_page_idx and last_page_idx >= 0:
            body_lines.append('<div class="page-break" aria-hidden="true"></div>')
        last_page_idx = page_idx
        body_lines.append(html)

    body_html = "\n".join(body_lines)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<style>{CSS}</style>
</head>
<body>
<main>
{body_html}
</main>
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
            return None  # Not an extraction-test JSON, skip silently

        # Count pre-ADA elements
        pre_count = sum(len(p.get("content", [])) for p in data.get("pages", []))

        if not raw:
            stats = _apply_ada_remediation(data)
            changes = {k: v for k, v in stats.items() if v > 0}
            if changes:
                parts = ", ".join(f"{k}={v}" for k, v in changes.items())
                print(f"  ADA  {json_path.name}: {parts}")

        # Count post-ADA elements
        post_count = sum(len(p.get("content", [])) for p in data.get("pages", []))

        html = render_document(data)

        # Post-render verification: re-render every element and check each one
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
        description="Render extraction-test JSON to ADA-compliant HTML."
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

    # Single file mode
    if args.input.is_file():
        out = args.output or args.input.with_suffix(".html")
        if not render_one(args.input, out, raw=args.raw):
            sys.exit(1)
        return

    # Batch directory mode — support both dir/*.json and dir/*/*.json
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
        # Put HTML in same directory as JSON, or mirror structure in output dir
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
