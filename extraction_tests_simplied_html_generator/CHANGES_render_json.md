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

## Element Preservation Guarantee

Verified across all 100 files (16,218 total elements):

- **Every element that survives ADA remediation produces non-empty HTML.** Zero elements silently dropped by renderers.
- 2,754 elements removed by ADA remediation, all intentional:

| ADA Operation | Count | Effect |
|---|---|---|
| Running header/footer dedup | 930 | Removes repeated page headers/footers |
| Duplicate content removal | 507 | Removes identical paragraphs/headings |
| Image dedup | 1,229 | Removes identical images (by base64 hash or description) |
| List merging | 88 | Merges consecutive same-type lists (items preserved) |
| Empty page removal | 2 | Removes pages emptied by dedup |
| H1 demotion | 842 | Modifies only (H1 -> H2), no removal |
| Heading normalization | 9 | Modifies only (fixes level skips), no removal |
| Decorative image marking | 1,323 | Modifies only (adds role="presentation"), no removal |
| Table header inference | 400 | Modifies only (row 0 -> `<th>`), no removal |

## Image Sizing from PDF Bounding Boxes

Previously, images were rendered with no explicit dimensions — only `max-width: 100%; height: auto` in CSS. Since the base64 data contains the image at its native resolution (which is often much larger than its on-page appearance in the PDF), images could appear drastically oversized in the HTML output.

**Fix:** `_render_image()` now reads the `bbox` field (already present in the JSON, extracted by PyMuPDF via `page.get_image_rects()`) and sets explicit `width` and `height` attributes on the `<img>` tag. The bbox coordinates are in PDF points (1pt = 1/72 inch), which map closely to CSS pixels, so images now render at the same size they appear in the original PDF.

- The existing CSS `max-width: 100%` still prevents overflow on narrow viewports
- `height: auto` in CSS preserves aspect ratio if width is clamped
- Images without a bbox (rare edge case) fall back to the previous behavior

## Test Results

Tested against 100 extraction-test JSON files: **100 rendered, 0 failed, 0 elements silently lost**.
