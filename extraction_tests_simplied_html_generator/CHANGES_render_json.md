# render_json.py — Rewrite Changelog

## What Changed

The `render_json.py` script was rewritten from scratch to be **fully self-contained** with no external dependencies beyond Python's standard library.

### Before (old version)

- Depended on the full backend framework:
  - `src.models.semantic` (SemanticDocument, Heading, Paragraph, Table, Image, List, etc.)
  - `src.services.rendering` (render_document)
  - `src.services.conversion` (_normalize_heading_hierarchy)
  - `src.services.link_injection` (inject_links)
  - `src.services.processing.pipeline` (ProcessingService — instantiated via `__new__` hack)
- Required converting JSON into Pydantic model objects before rendering
- Used the backend's CSS and HTML rendering engine
- Would fail if `src/` was not available or models changed

### After (new version)

- **Zero external dependencies** — only uses `argparse`, `hashlib`, `json`, `re`, `sys`, `html.escape`, `pathlib`
- Operates directly on the extraction-test JSON (no intermediate model conversion)
- Literal translation: each JSON content type maps directly to semantic HTML
- Minimal, readable CSS inline in the output

## Content Types Handled

All 9 types from the `extract_structured_json.py` schema:

| Type | HTML Output |
|------|-------------|
| `heading` | `<h1>`–`<h6>` with proper hierarchy |
| `paragraph` | `<p>` with markdown bold/italic converted to `<strong>`/`<em>` |
| `table` | `<table>` with `<th>`/`<td>`, `scope`, `rowspan`/`colspan`, `<caption>`, `aria-label` |
| `image` | `<img>` with `alt` text, `<figure>`/`<figcaption>` for captioned images, `role="presentation"` for decorative |
| `list` | `<ol>`/`<ul>` with nested `<ul>` for children |
| `form` | `<table>` with Field/Type/Value columns and `<caption>` |
| `link` | `<a href="...">` |
| `video` | `<a href="...">` with description text |
| `header_footer` | `<div role="banner/contentinfo">` (only if survived deduplication) |

## ADA Compliance & Deduplication (Preserved)

All remediation steps are self-contained — no external services needed:

1. **H1 demotion** — Only the first H1 is kept; subsequent H1s become H2
2. **Heading hierarchy normalization** — Fixes level skips (H1 -> H4 becomes H1 -> H2)
3. **Running header/footer deduplication** — Removes header_footer items that repeat across >50% of pages (with page-number normalization)
4. **Duplicate content removal** — Removes duplicate paragraphs and headings (first 200 chars, case-insensitive)
5. **Image deduplication** — Two-layer dedup:
   - By base64 content hash (catches identical images with different descriptions)
   - By description text fallback (for images without base64 data)
6. **Consecutive list merging** — Merges adjacent lists of the same type
7. **Decorative image detection** — Marks images with empty/generic descriptions as decorative (empty alt, `role="presentation"`)
8. **Table header inference** — Treats row 0 as header if cells are short text
9. **Empty page removal** — Removes pages left empty after deduplication

## CLI Interface

Unchanged:
```
python render_json.py path/to/file.json              # single file
python render_json.py path/to/dir/                    # batch: *.json and */*.json
python render_json.py path/to/dir/ -o /tmp/output/    # custom output directory
python render_json.py path/to/file.json --raw          # skip ADA remediation
```

## Test Results

Tested against 100 extraction-test JSON files: **100 rendered, 0 failed**.
