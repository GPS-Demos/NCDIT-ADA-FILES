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
7. **Decorative image detection** — Marks images as decorative based on description AND bbox dimensions (see "Enhanced Decorative Image Detection" below)
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

## Image Sizing from PDF Bounding Boxes (`render_json.py`)

Previously, images were rendered with no explicit dimensions — only `max-width: 100%; height: auto` in CSS. Since the base64 data contains the image at its native resolution (which is often much larger than its on-page appearance in the PDF), images could appear drastically oversized in the HTML output.

**Fix:** `_render_image()` now reads the `bbox` field (already present in the JSON, extracted by PyMuPDF via `page.get_image_rects()`) and sets explicit `width` and `height` attributes on the `<img>` tag. The bbox coordinates are in PDF points (1pt = 1/72 inch), which map closely to CSS pixels, so images now render at the same size they appear in the original PDF.

- The existing CSS `max-width: 100%` still prevents overflow on narrow viewports
- `height: auto` in CSS preserves aspect ratio if width is clamped
- Images without a bbox (rare edge case) fall back to the previous behavior
- **Decorative images are excluded** from bbox sizing — they use `display:none` instead

## Enhanced Decorative Image Detection (`render_json.py`)

`_mark_decorative_images()` previously only checked for generic descriptions. PDFs — especially design-heavy ones — contain many decorative elements (gradient strips, thin lines, background textures) extracted as separate images by PyMuPDF. When displayed with bbox sizing, these create huge stretched artifacts (e.g., a 1px-wide gradient displayed at 1x792px).

Images are now marked decorative based on **three criteria**:

1. **Generic description** — empty, "unidentified image", "image", "decorative image", "logo"
2. **Thin strips** — either bbox dimension < 10px (gradient lines, hairlines)
3. **Extreme aspect ratio** — bbox ratio > 15:1 (decorative bands, sidebar strips)

**Decorative images are hidden** with `display:none` instead of being rendered with `role="presentation"`. This prevents design elements from creating visual noise in the HTML while keeping them in the DOM for completeness.

## Image Extraction: Hybrid Approach (`extract_structured_json.py`)

`extract_images_from_pdf_page()` uses three strategies depending on image characteristics:

### 1. Stacked full-page background layers → `page.get_pixmap(clip=rect)`
PDFs sometimes stack **multiple** full-page images at the same bbox (photo + grunge texture + gradient overlay) that only look correct when composited together. Individual layers look like garbage (gray noise, color-inverted textures).

**Detection:** Only triggers when a page has **2+ images** covering ≥90% page width and ≥50% page height. Single full-page images use raw `extract_image()` like everything else.

**Rendering:** `page.get_pixmap(matrix=Matrix(3, 3), clip=rect)` at 3x scale. No text redaction — text in the image is preserved as-is (some pages have text baked into their design). Only the first stacked layer triggers the render; duplicate layers are skipped (ADA dedup handles them).

### 2. Images with SMask (transparency) → `doc.extract_image()` + PIL
SMask is stored as a separate PDF object. `extract_image()` returns the base image without transparency (black background for JPEG). PIL composites the mask as an alpha channel and outputs PNG.

### 3. All other images → `doc.extract_image()` raw bytes
Zero post-processing. Preserves indexed/palette colorspaces and original compression (JPEG stays JPEG). This is what `ada-compliance-engine` uses for all images.

### Approaches tried and reverted:
- **`fitz.Pixmap(doc, xref)`** — Produces garbage for indexed/palette colorspaces
- **`page.get_pixmap(clip=rect)` for all images** — Captures overlapping content from other layers for non-background images
- **Raw `extract_image()` for all images** — Missing SMask transparency (logos get black backgrounds) and full-page background layers render as individual garbled textures

## Content Ordering Fix (`extract_structured_json.py`)

Previously, `process_single_page()` separated images from Gemini's output and appended them at the end:
```python
combined_content = other_content + merged_images + video_items + link_items
```
This broke reading order — e.g., a logo at the top of a PDF page would appear at the bottom of the HTML.

**Fix:** Images are now replaced in-place in Gemini's reading order. Only unmatched PyMuPDF images (those without a Gemini description) and videos/links are appended at the end.

## Diagram Fragment Consolidation (`extract_structured_json.py`)

PDFs containing diagrams (network diagrams, flowcharts, org charts, etc.) store each visual element — icons, arrows, cloud shapes, server icons — as a separate embedded raster image. PyMuPDF's `page.get_images()` extracts every one individually, producing dozens of tiny fragments (often 2x3px to 50x90px in PDF points) that are meaningless on their own.

**Problem:** These fragments would each become a separate `<img>` tag in the HTML, scattered with no spatial relationship, completely unlike the original diagram. Most would also be labeled "Unidentified image" by Gemini (since individual fragments are unrecognizable), marked decorative, and hidden.

**Fix:** `extract_images_from_pdf_page()` now detects diagram pages by counting small image fragments (both dimensions < 100 PDF points). When 5+ small fragments are found, the entire page is rendered as a **single full-page PNG screenshot** via `page.get_pixmap()` at the configured `RENDER_SCALE` (3x = 216 DPI). This single image replaces all individual fragments, preserving all spatial relationships exactly as they appear in the PDF.

- **Threshold:** 5+ images with both width and height < 100 PDF points
- **Rendering:** `page.get_pixmap(matrix=Matrix(RENDER_SCALE, RENDER_SCALE))` — full page, no clipping
- **Output:** Single image entry with `_full_page_render: true` metadata flag
- **Text extraction unaffected:** Gemini still extracts text content from its own page render; the full-page image only replaces the fragmented PyMuPDF image entries

### Example: `table-seal-imagery-diagram-1468`

| | Before | After |
|---|---|---|
| Embedded images extracted | 50 (49 tiny fragments + 1 seal) | 1 full-page render |
| Visible in HTML | 0 (all hidden as decorative) | 1 (complete diagram) |
| Image fidelity | Individual icons/arrows with no context | Exact replica of PDF page |

## Smarter Decorative Image Detection (`render_json.py`)

Updated `_mark_decorative_images()` to avoid hiding images that have real visual content.

**Before:** Any image with description in `{"", "unidentified image", "image", "decorative image", "logo"}` was unconditionally marked decorative and hidden with `display:none`.

**After:** Images are only marked decorative when they lack substantial content:

1. **Always decorative:** Empty description or explicitly "decorative image" — but only if no substantial base64 data (≤ 500 chars)
2. **Generic descriptions** ("unidentified image", "image", "logo") — decorative only if ALSO lacking substantial base64 data OR bbox is tiny (< 10px in either dimension)
3. **Images with real base64 data** (> 500 chars) are kept visible even with generic descriptions; "unidentified image" gets relabeled to "Document image" for better alt text
4. **Thin strips / extreme aspect ratios** — unchanged (still decorative)

This prevents the full-page renders and other meaningful composited images from being incorrectly hidden.

## Test Results

Tested against 100 extraction-test JSON files: **100 rendered, 0 failed, 0 elements silently lost**.
