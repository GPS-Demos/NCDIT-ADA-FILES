# render_json.py Fixes Documentation

## Overview

This document details all changes made to `render_json.py` to address problems identified in `problems.csv`, as well as problems that **cannot** be fixed in the renderer because they originate in the JSON extraction step (`extract_structured_json.py` / Gemini).

---

## Fixes Applied to render_json.py

### 1. Removed All CSS/Stylesheets

**Problem:** User requested raw, simple HTML with no styling.

**What changed:** Removed the entire `CSS` constant (~35 lines of CSS) and the `<style>` tag from the HTML template. Output is now unstyled HTML.

**Files affected:** All 100 output files.

---

### 2. Removed All ARIA Attributes

**Problem:** Multiple reviewers flagged `aria-label`, `aria-hidden`, and `aria-controls` attributes as problematic or unnecessary.

**What changed:**
- Removed `aria-label="Table with N rows and N columns"` from all `<table>` tags
- Removed `aria-hidden="true"` from page break divs (now removed entirely — no page breaks in output)
- Removed `role="presentation"` from decorative images

**Files affected:** All 100 output files.

**CSV references:**
- "Remove Page numbers wrapped in role=contentinfo" (2019-20-smac-work-plan)
- "Aria Labels" (gicc-goals-2021-2023-discussion)
- "aria-label on the table" (seal-image-table-6870)

---

### 3. Removed All `role` Attributes

**Problem:** `role="banner"` and `role="contentinfo"` on header/footer elements, `role="presentation"` on decorative images.

**What changed:** Header/footer items now render as plain `<p><small>text</small></p>` instead of `<div role="contentinfo">`.

**Files affected:** All files with header/footer content.

**CSV references:**
- "Remove Page numbers wrapped in role=contentinfo" (2019-20-smac-work-plan)
- "Added role=contentinfo elements that include the pdf page number" (logo-tables-shading-watermark-photos-13a3, long-contract-many-pages-of-tables-6881)

---

### 4. Removed All `class` Attributes

**Problem:** Simplification request — no `class="page-break"`, `class="page-header"`, etc.

**What changed:** All class attributes removed from output HTML.

**Files affected:** All 100 output files.

---

### 5. Removed `scope="col"` from Table Headers

**Problem:** Simplification — raw HTML without accessibility scope attributes.

**What changed:** Table header cells (`<th>`) no longer include `scope="col"`.

**Files affected:** All files with tables.

---

### 6. Removed Viewport Meta Tag

**Problem:** Simplification — raw HTML.

**What changed:** Removed `<meta name="viewport" content="width=device-width, initial-scale=1">` from the HTML head.

**Files affected:** All 100 output files.

---

### 7. Removed `<main>` Wrapper

**Problem:** Simplification — raw HTML.

**What changed:** Body content is no longer wrapped in a `<main>` element.

**Files affected:** All 100 output files.

---

### 8. Page Breaks Removed Entirely

**Problem:** Page breaks were rendered as `<div class="page-break" aria-hidden="true"></div>` which screen readers couldn't interpret. Reviewers noted "A screen reader user won't know that the page breaks exist." Page breaks are PDF artifacts that don't belong in HTML output.

**What changed:** Page breaks are no longer rendered at all. Content flows continuously without any page separation markers.

**Files affected:** All multi-page files.

**CSV references:**
- "Dashed lines are used to visually represent page breaks. A screen reader user won't know that the page breaks exist. Was coded using a `<div aria-hidden=true>` instead of an `<hr>`" (near-perfect-powerpoint-slides-47b0, 47b2, newsletter-with-many-images-117c, 21fb, powerpoint-slides-1793, f832, fed0, feef, logos-graphic-colors-53de, 53e1, logos-graphic-colors-table-screenshot-fc98, long-contract-many-pages-of-tables-6881, map-imagery-365a)
- "Remove page breaks and divs" (10-22-20-edu-committee-agenda-packet)
- "Page breaks continue between pages" (20200522-nc911-board-minutes-approved, 911-board-education-committee-meeting-minutes-april-21-2022)

---

### 9. Page Numbers Removed

**Problem:** Page numbers from the original PDF (e.g., "1", "Page 2 of 5", "- 3 -", "3 | P a g e", "1 of 4") were being included in the HTML output as `<p><small>...</small></p>` elements. These are PDF artifacts that don't belong in HTML.

**What changed:** Added `_remove_page_numbers()` to ADA remediation that strips `header_footer` items matching page number patterns:
- Bare numbers: `1`, `12`
- Dash-wrapped: `- 1 -`
- "Page N", "Page N of M"
- "N of M" (e.g., `1 of 4`)
- "N | Page", "N | P a g e"
- Pipe-separated footers containing page numbers: `00234464.25 | Page 37 of 39 | June 12, 2025`
- Bold-wrapped page numbers: `**2** | Page (Rev 06-05-15)`

**Files affected:** All files with page number footer/header elements.

**CSV references:**
- "Page numbers included: all pages" (10-22-20-edu-committee-agenda-packet)
- "Page numbers included" (2019-20-smac-work-plan)
- "Page number and page break on p. 14-15" (208m-endpoint-reseller-price-list)
- "page numbers show up on pg 5" (multi-factor-authentication-report-december-2015)
- "The footers (e.g. Page 3 of 39 June 12, 2025) show up in the HTML" (scanned-from-paper-many-pages-of-tables-6878)
- "Added role=contentinfo elements that include the pdf page number" (logo-tables-shading-watermark-photos-13a3, long-contract-many-pages-of-tables-6881)

---

### 10. Markdown Bold `**text**` Converted to `<strong>` in ALL Renderers

**Problem:** Only the paragraph renderer converted `**bold**` to `<strong>`. Headings, table cells, list items, header/footer, and fallback renderers output literal `**` characters.

**What changed:** Created a shared `_md_to_html()` function that converts `**text**` to `<strong>text</strong>`. Applied to ALL renderers:
- `_render_heading`
- `_render_paragraph`
- `_render_table` (cell text)
- `_render_list` (item text and children)
- `_render_header_footer`
- `_render_fallback`

Also uses `re.DOTALL` flag so bold spanning multiple lines (with `\n`) is correctly converted.

**Files affected:** ~81 files with bold text.

**CSV references:**
- "Asterisks added where formatting used" (seal-imagery-table-with-shading-132c, seal-imagery-table-with-shading-colored-text-672b, smac-lidar-apr-10-2024, standards-committee-meeting-agenda-packet, table-seal-imagery-diagram-1468, tables-screenshots-photos-background-colors-59df, wearencgov-presentation3, logo-tables-shading-watermark-photos-13a3, logos-graphic-colors-table-screenshot-fc98, long-contract-many-pages-of-tables-6881)
- "Double asterisks around text" (appenc-initialdatalayers, create-beautiful-sharepoint-sites, draft-fy23-25-goals-and-priorities)
- "Bold text replaced by plaintext enclosed by 2 asterisks" (nc-911-board-technology-committee-minutes)
- "Bold is rendered as ** instead of `<strong>`" (scio-physical-and-environmental-protection, scanned-from-paper-many-pages-of-tables-6878, seal-imagery-11ab)
- "Markdown not interpreted as HTML" (gicc-agenda-20160810, nc-911-board-technology-committee-minutes, near-perfect-powerpoint-slides-47b0/47b2, powerpoint-slides-f832/fed0/feef/fef1/fef5/ff0a/ff0c/ff0d, seal-image-table-6870, seal-imagery-11ab)
- "On the TOC bold text is replaced with **" (mostly-text-charts-tables-screenshots-maps-67fb)
- "bold replaced by **" (nc-911-board-education-committee-meeting-agenda-packet, nc-911-board-meeting-agenda-aug-26-2022, nc-911-board-minutes-september-30-2022)
- "Extraneous asterisks added in place of bold text" (newsletter-with-many-images-117c)
- "Extraneous asterisks added" (powerpoint-slides-f832, powerpoint-slides-feef)
- "Numerous improper asterisks" (near-perfect-powerpoint-slides-47b2)
- "Many extraneous asterisks" (near-perfect-powerpoint-slides-47b0)

---

### 11. Markdown Italic `*text*` Converted to `<em>` in ALL Renderers

**Problem:** Same as bold — only the paragraph renderer handled italic conversion. Other renderers output literal `*text*`.

**What changed:** The shared `_md_to_html()` function also converts `*text*` to `<em>text</em>` (with lookahead/lookbehind to avoid matching `**`). Applied to all renderers. Uses `re.DOTALL` for multi-line support.

**Files affected:** ~65 files with italic text.

**CSV references:**
- "Italics missing and replaced with **" (memo-with-links-1334, gicc-agenda-20160810, mo-minutes-20160620)
- "Italic text is not being converted from markdown. Displayed as `*...*`" (gicc-ncdot-florence-20181107)
- "italics show as `*text*`" (gicc-smac-agenda-20210120)
- "PDF text with Italic has * added" (esrmo-newsletter-april-2017)
- "Text is not Bold, but listed with **" (esrmo-newsletter-december-2018)
- "Bold text presented w **" (esrmo-newsletter-july-2021, esrmo-newsletter-march-2018)

---

### 12. Markdown Links `[text](url)` Converted to `<a href>` in ALL Renderers

**Problem:** Some text fields contained markdown-style links that were rendered literally as `[text](url)` instead of clickable HTML links.

**What changed:** The `_md_to_html()` function converts `[text](url)` to `<a href="url">text</a>`.

**Files affected:** Files with markdown link syntax in text.

**CSV references:**
- "Emails are hyperlinks in the original PDF but in the HTML they are outputted as markdown ([email](link))" (seal-image-table-6870)
- "Link markdown formatting used instead of html" (logo-tables-shading-watermark-photos-13a3)

---

### 13. Ordered List Duplicate Number Stripping

**Problem:** When Gemini extracts ordered lists, it embeds the number/letter prefix in the item text (e.g., `"1. Approve minutes"`). When rendered inside `<ol><li>`, the browser adds its own numbering, resulting in double numbers like "1. 1. Approve minutes".

**What changed:** Added `_strip_list_prefix()` function that removes leading prefixes from ordered list items:
- Numeric: `1.`, `1)`, `(1)`
- Alphabetic: `a.`, `a)`, `(a)`
- Roman numerals: `i.`, `ii.`, `iii.`, `iv.`

Applied to both parent items and nested children.

**Files affected:** ~15+ files with ordered lists.

**CSV references:**
- "Ordered list keeping number in text instead of replacing" (10-22-20-edu-committee-agenda-packet, seal-imagery-table-with-shading-132c)
- "Ordered list items have additional number in text" (911-board-education-committee-meeting-minutes, 20200522-nc911-board-minutes-approved, seal-imagery-table-with-shading-colored-text-672b)
- "Ordered lists keeping original number in addition to list item markup" (20190814-nc-911-board-minutes-approved)
- "extra numbers added to numbered list" (nc-911-board-meeting-agenda-aug-26-2022, nc-911-board-education-committee-meeting-agenda-packet)
- "List items incorrectly numbered, duplicate numbering and a reset in order" (nc-911-board-technology-committee-minutes)
- "Duplicating list numbers within `<li>`" (logos-graphic-colors-table-screenshot-fc98)
- "Generating list item letters in addition to showing list item numbers" (long-contract-many-pages-of-tables-6881)
- "additional numbers were added to the TOC" (mostly-text-charts-tables-screenshots-maps-67fb)
- "extra numbers added to the lists" (multi-factor-authentication-report-december-2015)
- "Duplicate list numbering" (powerpoint-slides-f832, powerpoint-slides-feef)
- "List numbering duplicated" (near-perfect-powerpoint-slides-47b0)
- "numbered list restarts at new page with duplicate numbering" (gicc-meeting-minutes-08072007)
- "List separated by pagination. Second half displays two sets of numbers" (map-imagery-365a)

---

### 14. Table Header: Removed Auto-Mark of Row 0 as `<th>`

**Problem:** The original code treated ALL row-0 cells as `<th>` headers regardless of content. This caused data rows to be incorrectly marked as headers when the first row contained data, not column labels.

**What changed:** Removed the `or r == 0` fallback in `_render_table`. Now only cells explicitly marked with `_is_header=True` (by the ADA remediation's `_infer_table_headers`) are rendered as `<th>`.

**Files affected:** All files with tables.

**CSV references:**
- "First row of table incorrectly converted to table header" (nc-911-board-technology-committee-minutes, multi-factor-authentication-report-december-2015, powerpoint-slides-f832)
- "Table identifies wrong row as table heading row" (20200522-nc911-board-minutes-approved, 911-education-committee-meeting-agenda-packet)
- "First row incorrectly marked as header" (powerpoint-slides-f832)
- "Formatted the first row of the data tables as column headers when they should not be" (long-contract-many-pages-of-tables-6881)
- "First row of the table was made a table header instead of a normal table row" (seal-image-table-6870)

---

### 15. Improved Table Header Inference Heuristic

**Problem:** The `_infer_table_headers` function marked row-0 as headers if all cells had short text and there were 2+ columns. This was too aggressive — it marked rows with numeric data (prices, dates) as headers.

**What changed:** Added a check: if any row-0 cell contains mostly numeric data (`$`, `%`, digits), the row is NOT marked as a header row.

**Files affected:** All files with tables.

---

### 16. Duplicate Link Deduplication

**Problem:** Gemini extraction often produces both inline link references in paragraph text AND separate standalone `link` elements for the same URLs. This results in links appearing twice — once inline and once at the bottom of the page/section.

**What changed:** Added `_deduplicate_links()` to ADA remediation. For each page, it:
1. Collects all URLs mentioned in paragraph/heading text (both markdown links and raw URLs)
2. Removes standalone `link` elements whose URL already appears in the text
3. Also removes duplicate `link` elements (same URL appearing multiple times)

**Files affected:** ~30+ files with duplicate links.

**CSV references:**
- "Duplicate links in footer" (colored-text-logos-676a)
- "links duplicated at bottom of pages" (seal-imagery-table-with-shading-colored-text-672b, logos-graphic-colors-table-screenshot-fc98, long-contract-many-pages-of-tables-6881)
- "Links duplicated" (near-perfect-powerpoint-slides-47b0, 47b2, newsletter-with-many-images-21fb, powerpoint-slides-1793)
- "extra link at the bottom of the page" (federal-interagency-committee-agenda20190516)
- "duplicated link at the end of page" (gicc-meeting-minutes-02122003)
- "Correct links duplicated to bottom of page" (newsletter-with-many-images-117c)
- "link duplicated in middle of paragraph and bottom of page" (gicc-mo-minutes-20191216)
- "Originally hyperlinked text duplicated" (near-perfect-powerpoint-slides-47b0)
- "Extra and unnecessary page breaks around links and links were repeated at the bottom" (memo-with-links-1334)
- "hyperlinks duplicated at the bottom of every page" (mostly-text-charts-tables-screenshots-maps-67fb)
- "urls repeated at the bottom of the doc" (multi-factor-authentication-report-december-2015)
- "Creating extra links after the content" (logos-graphic-colors-table-screenshot-fc98)
- "all links from the page grouped and listed together at the end of the page" (esrmo-newsletter-april-2017)

---

### 17. Nested List Children Use Matching List Type

**Problem:** Nested lists inside ordered lists were always rendered as `<ul>` (unordered), even when the parent was `<ol>` (ordered).

**What changed:** Nested child lists now use the same tag as the parent (`<ol>` children under `<ol>`, `<ul>` children under `<ul>`).

**Files affected:** Files with nested ordered lists.

**CSV references:**
- "Nested lists are not pulling over" (gicc-agenda-20160810)
- "missing 3rd indent in list (needs additional nesting)" (gicc-smac-agenda-20210120)
- "List hierarchy did not transfer" (ncom-update-gicc-05-15-2014)

---

## Problems That CANNOT Be Fixed in render_json.py

These issues originate in the JSON extraction step (Gemini/PyMuPDF) and require changes to `extract_structured_json.py` or the extraction prompt.

### A. Wrong/Inaccurate Alt Text on Images

The alt text is generated by Gemini during extraction. The renderer faithfully outputs whatever description is in the JSON.

**CSV references:**
- "alt text is wrong" (gicc-tims-may-2016 — multiple pages)
- "Alt text for images is swapped (tagged to the wrong image)" (gicc-ncdot-florence-20181107)
- "Incorrect alt text on images" (newsletter-with-many-images-117c, 21fb, powerpoint-slides-1793)
- "Alt text just says 'Document image'" (near-perfect-powerpoint-slides-47b2)
- "alt text of main image is 'document image'" (map-imagery-0fb1)
- "Image of drone has completely wrong alt text" (gicc-ncdot-florence-20181107)
- "Alt text issues" (multiple files)

### B. Missing Images

Images that Gemini described but PyMuPDF couldn't extract have no base64 data. The renderer correctly comments these out rather than showing broken image icons.

**CSV references:**
- "Multiple images missing" (map-imagery-e5cc)
- "Missing images" (powerpoint-slides-1793, near-perfect-powerpoint-slides-47b2)
- "image missing" (esrmo-newsletter-december-2018, gicc-tims-may-2016)
- "Image is missing / broken image icon" (map-imagery-logo-imagery-4809, f810)

### C. Content Out of Order

Page-by-page extraction can produce content in wrong reading order, especially for complex layouts.

**CSV references:**
- "Images out of order compared to the original PDF" (screenshot-images-11b5)
- "Text content ordered incorrectly" (newsletter-with-many-images-117c)
- "One of the Images placed after text block" (esrmo-newsletter-july-2021, march-2018)
- "order of paragraphs changed" (esrmo-newsletter-december-2018)
- "Images placed in wrong order" (near-perfect-powerpoint-slides-47b2)
- "data out of order" (map-imagery-f7f6)

### D. Hallucinated Content

Gemini sometimes generates content that doesn't exist in the original PDF.

**CSV references:**
- "Hallucinated a link, 'network', to go to some random site" (seal-imagery-11ab)
- "Hallucinated links" (powerpoint-slides-1793)
- "Hallucinated the incorrect price for part '185669'" (scanned-from-paper-many-pages-of-tables-6878)
- "Added links that don't appear on page" (logos-graphic-colors-53de, 53e1)
- "Added some links that don't appear on page" (logos-graphic-colors-53de)
- "Hallucinated a link" (seal-imagery-11ab)
- "unknown content showing up" (map-imagery-f7f6)

### E. Missing Watermarks

Watermarks are visual overlays that Gemini doesn't extract into the JSON structure.

**CSV references:**
- "Missing DRAFT watermark" (10-22-20-edu-committee-agenda-packet)
- "Watermark not included on HTML" (911-board-education-committee-meeting-minutes)
- "Missing 'Draft' watermark" (nc-911-board-education-committee-meeting-agenda-packet)
- "Missing watermark throughout" (nc-911-board-minutes-september-30-2022)
- "Draft watermark not accounted for" (logo-tables-shading-watermark-photos-13a3)

### F. Broken/Wrong Hyperlinks

When Gemini extracts links, it sometimes uses the link text as the URL or produces broken hrefs. This is an extraction issue.

**CSV references:**
- "Copilot Lab link literally has 'Copilot Lab' as the href" (powerpoint-slides-fef1)
- "CLICK HERE has an href of literally 'CLICK HERE'" (seal-image-table-6870)
- "Blue text in an image is mistaken as links" (gicc-ncdot-florence-20181107)
- "Underlined text improperly converted to hyperlink leading to nowhere" (near-perfect-powerpoint-slides-47b0)
- "Links do not have a valid destination" (seal-imagery-table-with-shading-132c)
- "Created broken links from blue/underlined text" (map-imagery-0fb1)

### G. Text Extracted from Screenshots/Images

Gemini transcribes text visible in screenshots and adds it to the HTML, which is often incorrect behavior.

**CSV references:**
- "Transcribed the full text from the screenshot and put it in the HTML. Should have just put alt text on the image" (powerpoint-slides-fef1, near-perfect-powerpoint-slides-47b0)
- "All UI in screenshots is being transcribed" (powerpoint-slides-1793)
- "Entire slides being transcribed after an entire image" (near-perfect-powerpoint-slides-47b0)
- "Image transcribed along with image" (powerpoint-slides-1793, newsletter-with-many-images-117c)
- "text from image was converted into a series of tables" (gicc-tims-may-2016)

### H. Duplicate/Repeated Content from Images

Gemini sometimes outputs the image AND a text transcription of its contents.

**CSV references:**
- "Image copy of table copied over twice in two different sizes" (nc-911-board-technology-committee-minutes)
- "Image of entire page of document copied over in two different sizes" (nc-911-board-technology-committee-minutes)
- "Converted page to text but still kept the image" (smac-lidar-apr-10-2024, standards-committee-meeting-agenda-packet)
- "Text content duplicated by image of page" (map-imagery-0fb1)
- "Inserted a screenshot of the page" (map-imagery-ff40)

### I. Wrong Heading Hierarchy from Context

Some headings should be H3/H4 based on document context but Gemini marks them as H2.

**CSV references:**
- "The following headers should be H3, but are H2" (text-some-colored-text-3638)
- "All headers that should be H3 are H2" (wearencgov-presentation3)
- "Heading levels are off: Priorities 2-4 are H2 when they should be H4" (gicc-meeting-minutes-08072007)
- "Incorrect heading hierarchy" (logos-graphic-colors-53de, 53e1)
- "Visual heading hierarchy not represented semantically" (logos-graphic-colors-53de)
- "Headings order and hierarchy is incorrect" (federalagencyhurricanecoordination, esrmo-newsletter-september-2021)

### J. Content Split Across Pages

Page-by-page extraction splits paragraphs, lists, and tables at page boundaries.

**CSV references:**
- "Paragraphs are split because of page splits" (seal-imagery-11ab)
- "Page break cuts text into multiple paragraphs" (newsletter-with-many-images-21fb)
- "text split across pages" (logos-graphic-colors-53e1)
- "Word breaks are odd because of the page-by-page approach" (seal-imagery-11ab)
- "Table split by pagination" (map-imagery-365a)

### K. Form Handling

PDF forms are complex structures that don't map cleanly to HTML.

**CSV references:**
- "N/A - Includes form" (ifb-its-400277-2017-1102-final)
- "Form" (fillable-form-logo-imagery-bddf, bdfc)
- "Check blocks turned into a table" (seal-imagery-table-with-shading-132c)

### L. Nested Tables Incorrectly Interpreted

Gemini flattens nested tables into the parent table structure.

**CSV references:**
- "Nested table incorrectly interpreted" (20190416-nc-911-board-minutes-approved, 20190726-board-agenda)
- "Nested table converted into parent table" (20190416-nc-911-board-minutes-approved, 20190726-board-agenda)

### M. Back-to-Back Headings from Extraction

Gemini sometimes splits a multi-line heading into multiple heading elements.

**CSV references:**
- "Heading marked up in separate back-to-back h2s instead of single" (20190814-nc-911-board-minutes-approved, 2019-20-smac-work-plan)
- "Header text repeated on multiple pages" (2019-20-smac-work-plan)
- "Multi-line header at the top was considered a paragraph" (gicc-mo-minutes-20191216)
- "Title is split between H1 & H2" (gicc-tims-may-2016)

### N. Links Inside Tables Placed Below

When Gemini encounters links inside table cells, it sometimes extracts them as separate link elements below the table.

**CSV references:**
- "Links inside a table in PDF were placed below the table in HTML" (cyber-incident-reporting)
- "Links have been removed from the table and placed at the bottom" (gicc-agenda-20160810)
- "Pulled nested list out of table and placed it under the table" (gicc-agenda-20200506)

### O. Compressed/Cut Images

Image quality issues from extraction.

**CSV references:**
- "Compressed and cut images so that they are no longer viewable" (wearencgov-broadbandinitiatives)
- "Only part of image transferred over" (near-perfect-powerpoint-slides-47b0)

### P. Underlined Text Converted to Links

Gemini interprets underlined text as hyperlinks even when they aren't.

**CSV references:**
- "Broken links created when occurring underlined text" (20200522-board-agenda)
- "Created a link from underlined text" (logo-tables-shading-watermark-photos-13a3)
- "Underlined text improperly converted to hyperlink" (near-perfect-powerpoint-slides-47b0)
- "Underlined content from PDF looks like linkable text on HTML but it is not" (nc-911-board-meeting-agenda-aug-26-2022)

### Q. Missing/Incorrect Footer Content

Footer handling during extraction.

**CSV references:**
- "Footer is missing" (esrmo-newsletter-april-2017)
- "Footer repeated" (multi-factor-authentication-report-december-2015, nc-911-board-education-committee-meeting-agenda-packet)
- "Footer showing up mid-page" (nc-911-board-meeting-agenda-aug-26-2022)

### R. Content Loss

Gemini sometimes fails to extract all content from a page.

**CSV references:**
- "Loss of text content" (logo-tables-shading-watermark-photos-13a3)
- "Missing content" (map-imagery-f7f6, federalagencyhurricanecoordination)
- "Major content loss from the infographic" (logos-graphic-colors-53e1)
- "Major content loss: headings in TOC missing" (long-contract-many-pages-of-tables-6881)
- "Heading text lost" (logos-graphic-colors-53e1)

---

## Remaining Legitimate `**` in Output

5 files still contain literal `**` characters. These are **not bugs** — they are actual footnote markers or annotation symbols in the original PDF content:

| File | Example | Reason |
|------|---------|--------|
| long-contract-many-pages-of-tables-6881 | `IX5HF**`, `**Includes Quadient...` | Footnote markers |
| seal-imagery-table-with-shading-colored-text-672b | `** Agencies should contact...` | Footnote annotation |
| federalagencyhurricanecoordination-686132f8 | Various `**` in content | Presentation annotations |
| powerpoint-slides-1793 | Various `**` in content | Slide annotations |
| powerpoint-slides-ff0c | Various `**` in content | Slide annotations |

These cannot be converted to `<strong>` because they don't form valid `**text**` bold pairs — they're standalone symbols.
