# render_json.py Fixes Documentation

## Overview

This document details all changes made to `render_json.py` to address problems identified in `problems.csv`, as well as problems that **cannot** be fixed in the renderer because they originate in the JSON extraction step (`extract_structured_json.py` / Gemini).

---

## Fixes Applied to render_json.py (32 total)

### 1. Removed All CSS/Stylesheets

**Problem:** User requested raw, simple HTML with no styling.

**What changed:** Removed the entire `CSS` constant (~35 lines of CSS) and the `<style>` tag from the HTML template.

**Files affected:** All 100 output files.

---

### 2. Removed All ARIA Attributes

**Problem:** Multiple reviewers flagged `aria-label`, `aria-hidden`, and `aria-controls` attributes.

**What changed:** Removed `aria-label` from tables, `aria-hidden` from page breaks, `role="presentation"` from images.

**CSV references:** 2019-20-smac-work-plan, gicc-goals-2021-2023-discussion, seal-image-table-6870, logo-tables-shading-watermark-photos-13a3, long-contract-many-pages-of-tables-6881

---

### 3. Removed All `role` Attributes

**Problem:** `role="banner"` / `role="contentinfo"` on header/footer elements.

**What changed:** Header/footer items render as plain `<p>text</p>`.

**CSV references:** 2019-20-smac-work-plan, logo-tables-shading-watermark-photos-13a3, long-contract-many-pages-of-tables-6881

---

### 4. Removed All `class` Attributes

**What changed:** All class attributes removed from output.

---

### 5. Removed `scope="col"` from Table Headers

**What changed:** `<th>` cells no longer include `scope="col"`.

---

### 6. Removed Viewport Meta Tag

**What changed:** Removed `<meta name="viewport">` from HTML head.

---

### 7. Removed `<main>` Wrapper

**What changed:** Body content no longer wrapped in `<main>`.

---

### 8. Page Breaks Removed Entirely

**Problem:** Page breaks rendered as `<div class="page-break" aria-hidden="true"></div>`. Screen readers couldn't interpret them.

**What changed:** No page break markers at all. Content flows continuously.

**CSV references:** near-perfect-powerpoint-slides-47b0/47b2, newsletter-with-many-images-117c/21fb, powerpoint-slides-1793/f832/fed0/feef, logos-graphic-colors-53de/53e1, logos-graphic-colors-table-screenshot-fc98, long-contract-many-pages-of-tables-6881, map-imagery-365a, 10-22-20-edu-committee-agenda-packet, 20200522-nc911-board-minutes-approved, 911-board-education-committee-meeting-minutes

---

### 9. Page Numbers Removed

**Problem:** Page numbers from PDF (e.g., "1", "Page 2 of 5", "3 | P a g e") included in output.

**What changed:** Added `_remove_page_numbers()` that strips header_footer items matching page number patterns.

**CSV references:** 10-22-20-edu-committee-agenda-packet, 2019-20-smac-work-plan, 208m-endpoint-reseller-price-list, multi-factor-authentication-report-december-2015, scanned-from-paper-many-pages-of-tables-6878, logo-tables-shading-watermark-photos-13a3, long-contract-many-pages-of-tables-6881

---

### 10. Markdown Bold `**text**` Converted to `<strong>` in ALL Renderers

**Problem:** Only paragraph renderer converted bold. Headings, table cells, list items, header/footer output literal `**`.

**What changed:** Shared `_md_to_html()` function applied to ALL renderers. Uses `re.DOTALL` for multi-line support.

**CSV references:** seal-imagery-table-with-shading-132c, seal-imagery-table-with-shading-colored-text-672b, smac-lidar-apr-10-2024, standards-committee-meeting-agenda-packet, table-seal-imagery-diagram-1468, tables-screenshots-photos-background-colors-59df, wearencgov-presentation3, logo-tables-shading-watermark-photos-13a3, logos-graphic-colors-table-screenshot-fc98, long-contract-many-pages-of-tables-6881, appenc-initialdatalayers, create-beautiful-sharepoint-sites, draft-fy23-25-goals-and-priorities, nc-911-board-technology-committee-minutes, scio-physical-and-environmental-protection, scanned-from-paper-many-pages-of-tables-6878, seal-imagery-11ab, gicc-agenda-20160810, near-perfect-powerpoint-slides-47b0/47b2, powerpoint-slides-f832/fed0/feef/fef1/fef5/ff0a/ff0c/ff0d, seal-image-table-6870, mostly-text-charts-tables-screenshots-maps-67fb, nc-911-board-education-committee-meeting-agenda-packet, nc-911-board-meeting-agenda-aug-26-2022, nc-911-board-minutes-september-30-2022, newsletter-with-many-images-117c, esrmo-newsletter-april-2017, esrmo-newsletter-december-2018, esrmo-newsletter-july-2021, esrmo-newsletter-march-2018

---

### 11. Markdown Italic `*text*` Converted to `<em>` in ALL Renderers

**Problem:** Only paragraph renderer converted italic. Other renderers output literal `*text*`.

**What changed:** `_md_to_html()` converts `*text*` to `<em>text</em>`.

**CSV references:** memo-with-links-1334, gicc-agenda-20160810, mo-minutes-20160620, gicc-ncdot-florence-20181107, gicc-smac-agenda-20210120, esrmo-newsletter-april-2017, esrmo-newsletter-december-2018, esrmo-newsletter-july-2021, esrmo-newsletter-march-2018

---

### 12. Markdown Links `[text](url)` Converted to `<a href>` in ALL Renderers

**Problem:** Markdown link syntax rendered as literal text.

**What changed:** `_md_to_html()` converts `[text](url)` to `<a href="url">text</a>`.

**CSV references:** seal-image-table-6870, logo-tables-shading-watermark-photos-13a3

---

### 13. Ordered List Duplicate Number Stripping

**Problem:** Gemini embeds number prefixes in list item text (e.g., "1. text") AND `<ol>` adds numbering = double numbers.

**What changed:** `_strip_list_prefix()` removes leading numeric, alphabetic, and roman numeral prefixes.

**CSV references:** 10-22-20-edu-committee-agenda-packet, seal-imagery-table-with-shading-132c, 911-board-education-committee-meeting-minutes, 20200522-nc911-board-minutes-approved, seal-imagery-table-with-shading-colored-text-672b, 20190814-nc-911-board-minutes-approved, nc-911-board-meeting-agenda-aug-26-2022, nc-911-board-education-committee-meeting-agenda-packet, nc-911-board-technology-committee-minutes, logos-graphic-colors-table-screenshot-fc98, long-contract-many-pages-of-tables-6881, mostly-text-charts-tables-screenshots-maps-67fb, multi-factor-authentication-report-december-2015, powerpoint-slides-f832, near-perfect-powerpoint-slides-47b0, gicc-meeting-minutes-08072007, map-imagery-365a, nc-911-board-minutes-september-30-2022

---

### 14. Table Header: Removed Auto-Mark of Row 0 as `<th>`

**Problem:** Original code treated ALL row-0 cells as `<th>` regardless of content.

**What changed:** Only cells explicitly marked `_is_header=True` by ADA remediation are rendered as `<th>`.

**CSV references:** nc-911-board-technology-committee-minutes, multi-factor-authentication-report-december-2015, powerpoint-slides-f832, 20200522-nc911-board-minutes-approved, 911-education-committee-meeting-agenda-packet, long-contract-many-pages-of-tables-6881, seal-image-table-6870

---

### 15. Improved Table Header Inference Heuristic

**Problem:** `_infer_table_headers` was too aggressive — marked rows with numeric data as headers.

**What changed:** Added check: if any row-0 cell is mostly numeric, the row is NOT marked as header.

---

### 16. Duplicate Link Deduplication

**Problem:** Gemini produces inline links AND separate standalone link elements = duplicates.

**What changed:** `_deduplicate_links()` removes standalone link elements whose URL already appears in text, or same-page duplicate link elements.

**CSV references:** colored-text-logos-676a, seal-imagery-table-with-shading-colored-text-672b, logos-graphic-colors-table-screenshot-fc98, long-contract-many-pages-of-tables-6881, near-perfect-powerpoint-slides-47b0/47b2, newsletter-with-many-images-21fb, powerpoint-slides-1793, federal-interagency-committee-agenda20190516, gicc-meeting-minutes-02122003, newsletter-with-many-images-117c, gicc-mo-minutes-20191216, memo-with-links-1334, mostly-text-charts-tables-screenshots-maps-67fb, multi-factor-authentication-report-december-2015, esrmo-newsletter-april-2017, esrmo-newsletter-september-2021

---

### 17. Nested List Children Use Matching List Type

**Problem:** Nested lists inside `<ol>` always rendered as `<ul>`.

**What changed:** Children match parent tag.

**CSV references:** gicc-agenda-20160810, gicc-smac-agenda-20210120, ncom-update-gicc-05-15-2014

---

### 18. Leader Dots Replaced with Ellipsis

**Problem:** Sequences of 4+ dots (`.........`) from agendas/TOCs. Screen readers read each dot.

**What changed:** `_md_to_html()` replaces 4+ consecutive dots with `…`.

**CSV references:** 20200522-board-agenda

---

### 19. Literal `<u>` Tags Unescaped

**Problem:** Literal `<u>` tags escaped to `&lt;u&gt;` and displayed as text.

**What changed:** `_md_to_html()` unescapes `&lt;u&gt;` and `&lt;/u&gt;` back to real HTML.

**CSV references:** map-imagery-photos-tables-screenshots-diagrams-data-charts-0fb1

---

### 20. Markdown Underscore Italic `_text_` Converted to `<em>`

**Problem:** Underscore-style markdown `_text_` rendered as literal underscores.

**What changed:** `_md_to_html()` converts `_text_` to `<em>text</em>` (word-boundary only).

**CSV references:** map-imagery-photos-tables-screenshots-diagrams-data-charts-0fb1

---

### 21. Back-to-Back Same-Level Headings Merged

**Problem:** Gemini splits multi-line headings into multiple consecutive same-level headings.

**What changed:** `_merge_consecutive_headings()` joins them with ` — ` separator.

**CSV references:** 20190814-nc-911-board-minutes-approved, 2019-20-smac-work-plan, logo-tables-shading-watermark-photos-13a3

---

### 22. Removed `<small>` Tags from Header/Footer

**Problem:** `<small>` tags unnecessary for raw simple HTML.

**What changed:** Header/footer renders as plain `<p>text</p>`.

---

### 23. Ordered List `type` Attribute Set from Prefix Detection

**Problem:** `<ol>` defaults to numeric (1, 2, 3) even when PDF used alphabetic (a, b, c) or roman numeral (i, ii, iii) lists.

**What changed:** `_detect_list_style()` examines the first item's prefix and sets `type="a"`, `type="A"`, `type="i"`, or `type="I"` on the `<ol>` tag as appropriate.

**CSV references:** 2019-20-smac-work-plan ("Ordered list using numbers instead of letters"), seal-imagery-table-with-shading-132c ("Ordered list keeping numbers instead of replacing with letters and roman numerals"), nc-911-board-minutes-september-30-2022 ("Letters in numbered lists are replaced with circles")

---

### 24. Ordered List `start` Attribute for Cross-Page Continuation

**Problem:** Lists split across pages restart numbering at 1 instead of continuing from previous page.

**What changed:** If the first item's numeric prefix is > 1, the renderer sets `start="N"` on the `<ol>` tag.

**CSV references:** nc-911-board-meeting-agenda-aug-26-2022 ("numbering restarted from 1"), mostly-text-charts-tables-screenshots-maps-67fb ("numbers restarted at 1"), nc-911-board-minutes-september-30-2022 ("Numbered list starts back at 1"), gicc-meeting-minutes-08072007 ("restarts the list on the new page")

---

### 25. Orphan/Stray Asterisks Stripped

**Problem:** Gemini extraction adds unpaired `*` or `**` to text that don't form valid bold/italic pairs (e.g., `"** text"` or `"text **"`).

**What changed:** `_md_to_html()` strips leading and trailing orphan asterisk patterns.

**CSV references:** 20200522-nc911-board-minutes-approved ("Asterisks added to HTML that aren't on PDF"), 911-board-education-committee-meeting-minutes ("Asterisks not on PDF added to HTML"), 20190416-nc-911-board-minutes-approved ("Multiple asterisks added to table headings"), 20200522-board-agenda ("Misuse of asterisks changing meaning")

---

### 26. "Page Intentionally Left Blank" Boilerplate Removed

**Problem:** Boilerplate text like "This page intentionally left blank" carried from PDF into HTML.

**What changed:** `_remove_boilerplate()` strips paragraphs/headings matching these patterns.

**CSV references:** map-imagery-photos-tables-screenshots-diagrams-data-charts-365a ("page intentionally left blank literally added")

---

### 27. "Document image" Alt Text Treated as Decorative / Missing Image Placeholders

**Problem:** Images with generic `alt="Document image"` or `alt="document image"` provide no useful information. Images without base64 data were hidden as HTML comments.

**What changed:**
- "Document image" alt text now treated as decorative (same as "unidentified image")
- Images without base64 data now render as visible `[Image: description]` text placeholders instead of hidden HTML comments

**CSV references:** near-perfect-powerpoint-slides-47b2 ("Alt text just says 'Document image'"), map-imagery-0fb1 ("alt text of main image is 'document image'"), logo-tables-shading-watermark-photos-13a3 ("Alt text is 'document image'"), logos-graphic-colors-table-screenshot-fc98 ("alt text of submit button image is 'document image'"), map-imagery-365a ("Large block of whitespace disguised as an image with alt='document image'"), map-imagery-ff40 ("Inserted many screenshots with alt='document image'"), near-perfect-powerpoint-slides-47b0 ("Images missing and replaced by alt text commented into the html")

---

### 28. Extended Page Number/Footer Pattern Matching

**Problem:** Footer text like "Department of Information Technology 10 | P a g e" was not being caught by the page number removal regex because the existing patterns only matched when the text started with a number or "Page".

**What changed:** Added five new patterns to `_remove_page_numbers()`:
- `^.*\d+\s*\|\s*p\s*a\s*g\s*e\s*$` — catches "X text N | P a g e"
- `^.*\d+\s*\|\s*p\s*a\s*g\s*$` — catches truncated variants like "X text N | P a g"
- `^.*\|\s*page\s+\d+\s*/\s*\d+\s*$` — catches "... | Page 1/6"
- `^.*\|\s*page\s+\d+\s*$` — catches "... | Page 33"
- `^.*\|\s*page\s+\d+\s+of\s+\d+\s*$` — catches "... | Page 33 of 123" (no trailing pipe)

**CSV references:** gdac-legislative-report-may-2016 ("Department of Information Technology X | P a g e" on multiple pages), multi-factor-authentication-report-december-2015 (similar truncated footer), long-contract-many-pages-of-tables-6881 ("... | Page 1/6"), seal-imagery-table-with-shading-colored-text-672b ("... | Page 33 of 123")

---

### 29. Cross-Page Link Deduplication

**Problem:** The link deduplication only worked within a single page. Standalone link elements with URLs already seen on earlier pages were not removed, causing repeated link blocks across the document.

**What changed:** `_deduplicate_links()` now tracks URLs globally across ALL pages instead of per-page. First pass collects all URLs from paragraph/heading text globally, second pass removes link items whose URL was already in text or already seen as a standalone link on any earlier page.

**CSV references:** logos-graphic-colors-table-screenshot-fc98 (same myncid.nc.gov link repeated 5 times), esrmo-newsletter-april-2017 (links grouped at end of pages), seal-imagery-table-with-shading-colored-text-672b (links duplicated at bottom of pages)

---

### 30. Spaced Letter Text Collapse

**Problem:** OCR/extraction artifacts produce text with spaces between every character (e.g., "A P P . A Z . g o v" instead of "APP.AZ.gov"). Screen readers read each letter individually.

**What changed:** `_md_to_html()` now detects patterns of 4+ single characters separated by spaces and collapses them (removes internal spaces).

**CSV references:** long-contract-many-pages-of-tables-6881 ("A P P . A Z . g o v" in link text)

---

### 31. Short/Meaningless Figcaption Suppression

**Problem:** Images with very short or meaningless captions (e.g., "38%", "image", "logo") produced unhelpful `<figcaption>` elements.

**What changed:** `_render_image()` now suppresses figcaptions that are less than 5 characters, are purely numeric/percentage values, or match generic terms like "image", "figure", "photo", "logo", "icon".

**CSV references:** logo-tables-shading-watermark-photos-13a3 ("Strange figcaption added (38%)")

---

### 32. Bold+Italic Triple Asterisk Nesting Fix

**Problem:** `***text***` (Markdown bold+italic) produced incorrectly nested tags: `<strong><em>text</strong></em>`. The bold regex consumed 2 leading asterisks and matched the last 2 closing asterisks, leaving a stray `*` that caused the italic regex to capture across the `</strong>` tag boundary.

**What changed:** Added a dedicated regex for `***text***` → `<strong><em>text</em></strong>` that runs BEFORE the separate bold and italic regexes.

**CSV references:** 20190416-nc-911-board-minutes-approved ("***LOGISTICS FOR FUTURE BOARD MEETINGS ARE UNDERWAY***"), 20200522-board-agenda, map-imagery-0fb1 (all files with bold+italic content)

---

## Remaining Legitimate `**` in Output

4 files still contain literal `**` characters that are actual footnote markers in the original PDF:

| File | Example | Reason |
|------|---------|--------|
| long-contract-many-pages-of-tables-6881 | `IX5HF**`, `**Includes Quadient...` | Footnote markers |
| federalagencyhurricanecoordination-686132f8 | Various `**` in content | Presentation annotations |
| powerpoint-slides-1793 | Various `**` in content | Slide annotations |
| powerpoint-slides-ff0c | Various `**` in content | Slide annotations |

---

## Problems That CANNOT Be Fixed in render_json.py

These issues originate in the JSON extraction step (Gemini/PyMuPDF) and require changes to `extract_structured_json.py` or the Gemini extraction prompt.

### A. Wrong/Inaccurate/Swapped Alt Text on Images

**STATUS: FIXED** — Per-image alt text generation via Gemini (EXT-13) regenerated accurate alt text for all affected files. Each image is now sent individually to Gemini, eliminating position-based swaps and producing specific, accurate descriptions.

- [x] "alt text is wrong" (gicc-tims-may-2016 — pg 5, 6, 7, 9, 12, 13, 15, 22, 23) — **FIXED: 47 images regenerated**
- [x] "Alt text for images is swapped (tagged to the wrong image)" (gicc-ncdot-florence-20181107 — pg 7, 10) — **FIXED: 28 images regenerated, swaps eliminated**
- [x] "Incorrect alt text on images" (newsletter-with-many-images-117c, 21fb, powerpoint-slides-1793) — **FIXED: 6 + 43 + 34 images regenerated**
- [x] "Alt text just says 'Document image'" (near-perfect-powerpoint-slides-47b2 — pg 16) — **FIXED: now describes actual content**
- [x] "Image of drone has completely wrong alt text" (gicc-ncdot-florence-20181107 — pg 5) — **FIXED: now correctly describes "quadcopter drone"**
- [x] "When a page has multiple images, the alt text is switched" (logos-graphic-colors-53de — pg 7, 8) — **FIXED: per-image calls eliminate swapping**
- [x] "Alt text for images swapped" (near-perfect-powerpoint-slides-47b2 — pg 19) — **FIXED: 40 images regenerated**
- [x] "Alt text for image contains alt text for both images on the page" (near-perfect-powerpoint-slides-47b0 — pg 25, 26) — **FIXED: 100 images regenerated, each gets own description**
- [x] "alt text not complete" (gicc-tims-may-2016 — pg 1) — **FIXED: complete descriptions generated**
- [x] "Alt text includes 'sheriff's office personnel' but seems like hallucination" (logos-graphic-colors-53e1 — pg 21) — **FIXED: 43 images regenerated with accurate descriptions**
- [x] "Incomplete alt text for large flow chart" (logos-graphic-colors-53e1 — pg 32) — **FIXED: per-image description of flow chart**
- [x] "An image of people's hands up but alt text says it's the NC logo" (map-imagery-ff40 — pg 13) — **FIXED: 24 images regenerated**
- [x] "Describes state seal but not anything else in the image (flow chart)" (agency-onboarding-68607a87) — **FIXED: 1 image regenerated**
- [x] "Text in logos not used in alt text" (logo-tables-shading-watermark-photos-13a3 — pg 8) — **FIXED: 45 images regenerated**
- [x] "Some of the alt text is confusing and listed as a comment" (gicc-ncdot-florence-20181107 — pg 2) — **FIXED: clear descriptions generated**
- [x] "Image alt text and captions mixed up" (newsletter-with-many-images-117c) — **FIXED: 6 images regenerated**
- [x] "alt text is incorrect" (logo-imagery-screenshot-imagery-fca1) — **FIXED: 3 images regenerated**
- [x] "Text below images included with image and document image alt text" (208m-endpoint-reseller-price-list — pg 9-10) — **FIXED: 15 images regenerated**
- [x] "Alt text issues" (gdac-legislative-report-may-2016, gicc-2020-census-nc-factsheet, multiple powerpoint files) — **FIXED: 2 + 5 images regenerated**

### B. Missing Images

Images Gemini described but PyMuPDF couldn't extract have no base64 data.

- "Multiple images missing" (map-imagery-e5cc)
- "Missing images" (powerpoint-slides-1793, near-perfect-powerpoint-slides-47b2)
- "image missing" (esrmo-newsletter-december-2018, gicc-tims-may-2016)
- "Image is missing / broken image icon" (map-imagery-logo-imagery-4809, f810)
- "Missing image on page 37" (911-education-committee-meeting-agenda-packet)
- "Image depicting connections completely missing" (gicc-tims-may-2016 — pg 8)
- "Missing graphic completely" (gicc-tims-may-2016 — pg 19)
- "Only part of image transferred over" (near-perfect-powerpoint-slides-47b0)
- "Missing images, alt text mixed up" (newsletter-with-many-images-117c — pg 11)

### C. Content Out of Order

Page-by-page extraction produces content in wrong reading order.

- "Images out of order compared to the original PDF" (screenshot-images-11b5)
- "Text content ordered incorrectly" (newsletter-with-many-images-117c — pg 5, 9)
- "One of the Images placed after text block" (esrmo-newsletter-july-2021, march-2018)
- "order of paragraphs changed" (esrmo-newsletter-december-2018)
- "Images placed in wrong order" (near-perfect-powerpoint-slides-47b2 — pg 15)
- "data out of order" (map-imagery-f7f6 — pg 34)
- "all images out of order" (logo-imagery-screenshot-imagery-fca1)
- "Image from pg. 13 put in wrong place" (map-imagery-e5cc)
- "Images oriented incorrectly" (newsletter-with-many-images-117c — pg 9)
- "Placed the list of links after the wrong block" (logos-graphic-colors-53de — pg 15)

### D. Hallucinated Content

Gemini generates content not in the original PDF.

- "Hallucinated a link, 'network'" (seal-imagery-11ab)
- "Hallucinated links" (powerpoint-slides-1793)
- "Hallucinated the incorrect price for part '185669'" (scanned-from-paper-many-pages-of-tables-6878)
- "Added links that don't appear on page" (logos-graphic-colors-53de — pg 17, 18, 24, 25; logos-graphic-colors-53e1 — pg 11)
- "unknown content showing up" (map-imagery-f7f6)
- "Added links from example image, links were not originally clickable" (near-perfect-powerpoint-slides-47b0 — pg 17)
- "Added a broken link as a duplicate of a working link" (logos-graphic-colors-53e1 — pg 4, 7, 9, 12, 20, 32, 33, 41)
- "Truncated/Hallucinated ToC" (seal-imagery-11ab)
- "Added list bullets where no list was in pdf" (logo-tables-shading-watermark-photos-13a3 — pg 4)

### E. Missing Watermarks

Watermarks are visual overlays Gemini doesn't extract.

- "Missing DRAFT watermark" (10-22-20-edu-committee-agenda-packet)
- "Watermark not included on HTML" (911-board-education-committee-meeting-minutes)
- "Missing 'Draft' watermark" (nc-911-board-education-committee-meeting-agenda-packet)
- "Missing watermark throughout" (nc-911-board-minutes-september-30-2022)
- "Draft watermark not accounted for" (logo-tables-shading-watermark-photos-13a3)
- "Watermarked document with large landscape oriented print tables" (draft-addressnc-specifications-20210811)

### F. Broken/Wrong Hyperlinks (Extraction)

Gemini uses link text as URL or produces broken hrefs.

- "Copilot Lab link literally has 'Copilot Lab' as the href" (powerpoint-slides-fef1)
- "CLICK HERE has an href of literally 'CLICK HERE'" (seal-image-table-6870)
- "Blue text in an image is mistaken as links" (gicc-ncdot-florence-20181107)
- "Underlined text improperly converted to hyperlink" (near-perfect-powerpoint-slides-47b0)
- "Links do not have a valid destination" (seal-imagery-table-with-shading-132c)
- "Created broken links from blue/underlined text" (map-imagery-0fb1)
- "Broken links created when occurring underlined text" (20200522-board-agenda)
- "Created a link from underlined text" (logo-tables-shading-watermark-photos-13a3)
- "Underlined content looks like linkable text but is not" (nc-911-board-meeting-agenda-aug-26-2022)
- "Link in PDF doesn't have a destination but conversion set the link text as the href" (logo-tables-shading-watermark-photos-13a3)
- "href is wrong on first link and second link is missing href" (gicc-smac-agenda-20210120)
- "Link on page five converted from absolute to relative, causing 404" (911-education-committee-meeting-agenda-packet)
- "url not pulled from source doc" (gicc-meeting-minutes-02122003)
- "Hyperlink in wrong spot" (near-perfect-powerpoint-slides-47b0)
- "Link separated into two links" (map-imagery-365a — pg 22)
- "Link text wrapped in the PDF so the converter created 2 links" (logos-graphic-colors-53e1 — pg 10)

### G. Text Extracted from Screenshots/Images

Gemini transcribes visible text from screenshots.

- "Transcribed the full text from the screenshot. Should have just put alt text on the image" (powerpoint-slides-fef1, near-perfect-powerpoint-slides-47b0)
- "All UI in screenshots is being transcribed" (powerpoint-slides-1793)
- "Entire slides being transcribed after an entire image" (near-perfect-powerpoint-slides-47b0)
- "Image transcribed along with image" (powerpoint-slides-1793, newsletter-with-many-images-117c)
- "text from image was converted into a series of tables" (gicc-tims-may-2016)
- "content from images with text added to the HTML page" (esrmo-newsletter-april-2017)
- "pulling lines of text and creating an image of them" (gicc-lgc-censussurveyresults-20200506)
- "Table in the image interpreted as a Form" (esrmo-newsletter-december-2018)
- "Entire slide is being added instead of just one particular image" (powerpoint-slides-f832)
- "Put all the screenshots of background images into the HTML" (powerpoint-slides-fef1)

### H. Duplicate/Repeated Content from Images

Gemini outputs image AND text transcription.

- "Image copy of table copied over twice in two different sizes" (nc-911-board-technology-committee-minutes)
- "Image of entire page of document copied over in two different sizes" (nc-911-board-technology-committee-minutes)
- "Converted page to text but still kept the image" (smac-lidar-apr-10-2024, standards-committee-meeting-agenda-packet)
- "Text content duplicated by image of page" (map-imagery-0fb1)
- "Inserted a screenshot of the page" (map-imagery-ff40)
- "Repeats text from image as paragraph below" (logo-imagery-graphic-colors-map-imagery-6e2e)
- "Image of main PDF pages duplicated by screen text" (logos-graphic-colors-table-screenshot-fc98)
- "Put the image alt text and the image both in the HTML" (seal-imagery-11ab)
- "image legend duplicated as a table" (logo-imagery-graphic-colors-map-imagery-f80b)
- "table created from image that is not accurate" (logo-imagery-screenshot-imagery-fca1)
- "Background image transferred over" (newsletter-with-many-images-117c)
- "Background highlighting of headshot images transferred separately" (near-perfect-powerpoint-slides-47b0)
- "Image duplicated on page, color corrected losing grayscale" (near-perfect-powerpoint-slides-47b0)
- "Duplicate image improperly removed, different keys highlighted" (near-perfect-powerpoint-slides-47b2)
- "Every page has an image, and all of the images are embedded and all content is repeating" (nc-911-board-monthly-dispatch-march-2025)
- "The table on pg. 1 repeats three times" (nc-911-board-minutes-september-30-2022)
- "Campaign Airings data repeated on pg. 9" (nc-911-board-education-committee-meeting-agenda-packet)

### I. Wrong Heading Hierarchy from Context

Gemini marks headings at wrong levels based on document context.

- "The following headers should be H3, but are H2" (text-some-colored-text-3638)
- "All headers that should be H3 are H2" (wearencgov-presentation3)
- "Heading levels are off: Priorities 2-4 are H2 when they should be H4" (gicc-meeting-minutes-08072007)
- "Incorrect heading hierarchy" (logos-graphic-colors-53de, 53e1)
- "Visual heading hierarchy not represented semantically, all H2s" (logos-graphic-colors-53de)
- "Headings order and hierarchy is incorrect" (federalagencyhurricanecoordination, esrmo-newsletter-september-2021)
- "Header hierarchy issue, all headers are the same" (newsletter-with-many-images-117c)
- "Not ranking headings correctly, all h2s" (logo-tables-shading-watermark-photos-13a3)
- "Heading levels didn't carry over from context on previous page" (logos-graphic-colors-53de)
- "Subheading listed at same level as heading" (gicc-ncdot-florence-20181107)
- "headings are slightly off" (gicc-smac-agenda-20210120)
- "Interpreted an infographic as headings" (logos-graphic-colors-53de, 53e1)
- "Made a bunch of names headings when they shouldn't be" (map-imagery-ff40)
- "'Accessibility Items' should not be h2" (near-perfect-powerpoint-slides-47b2)
- "Didn't generate the h1 completely" (map-imagery-ff40)
- "PDF text with Italic has * added and promoted to heading" (esrmo-newsletter-april-2017)

### J. Content Split Across Pages

Page-by-page extraction splits paragraphs, lists, and tables at page boundaries.

- "Paragraphs are split because of page splits" (seal-imagery-11ab)
- "Page break cuts text into multiple paragraphs" (newsletter-with-many-images-21fb)
- "text split across pages" (logos-graphic-colors-53e1)
- "Word breaks are odd because of the page-by-page approach" (seal-imagery-11ab)
- "Table split by pagination causing subsequent tables to have bad column headers" (map-imagery-365a)
- "Page break interrupted the TOC list" (map-imagery-0fb1)
- "'Container-based Encryption' and 'Full Disk Encryption' indentation flattened" (seal-imagery-11ab)

### K. Form Handling

PDF forms don't map cleanly to HTML.

- "N/A - Includes form" (ifb-its-400277-2017-1102-final)
- "Form" (fillable-form-logo-imagery-bddf, bdfc)
- "Check blocks turned into a table" (seal-imagery-table-with-shading-132c)
- "Signature block turned into table" (seal-imagery-table-with-shading-132c)

### L. Nested Tables / Table Structure Errors

Gemini flattens or misinterprets table structures.

- "Nested table incorrectly interpreted" (20190416-nc-911-board-minutes-approved, 20190726-board-agenda)
- "Nested table converted into parent table" (20190416-nc-911-board-minutes-approved, 20190726-board-agenda)
- "Broke up the 2nd row of the table into two rows" (scanned-from-paper-many-pages-of-tables-6878)
- "rows split content that should be together" (scanned-from-paper-many-pages-of-tables-6878)
- "Table should be broken up into multiple tables or lists" (map-imagery-0fb1)
- "Tables created with incorrect header row. First row should be the table caption" (map-imagery-0fb1)
- "Table restarts with new header row that should not be a header" (208m-endpoint-reseller-price-list)
- "Data call marked up as table heading" (20200522-nc911-board-minutes-approved)
- "List of phone numbers marked up as separate table heading" (20200522-nc911-board-minutes-approved)
- "Items formatted as table on PDF, running together on HTML" (20200522-board-agenda)
- "Half of the TOC was put into a table the other half was not" (nc-911-board-meeting-agenda-aug-26-2022)
- "Table headers inside paragraph above table" (nc-911-board-technology-committee-minutes)
- "Table headers not properly marked as headers" (powerpoint-slides-f832)
- "Number 8 in table went to an H1" (nc-911-board-minutes-september-30-2022)
- "Irregular tables missing colgroup and scope" (208m-endpoint-reseller-price-list)
- "Table column headers not semantically marked up" (logo-tables-shading-watermark-photos-13a3)
- "Empty table rows added to bottom of table" (logo-tables-shading-watermark-photos-13a3)

### M. Multi-Line / Split Headings from Extraction

Gemini splits headings into multiple elements.

- "Multi-line header at the top was considered a paragraph" (gicc-mo-minutes-20191216)
- "Title is split between H1 & H2" (gicc-tims-may-2016)
- "Header text repeated on multiple pages" (2019-20-smac-work-plan)
- "The header was pulled over every time. Should just be pulled over once" (scio-physical-and-environmental-protection)
- "data table header row repeated" (nc-911-board-education-committee-meeting-agenda-packet)

### N. Links Inside Tables Placed Below / Link Placement Issues

Gemini extracts links from table cells as separate elements.

- "Links inside a table in PDF were placed below the table in HTML" (cyber-incident-reporting)
- "Links have been removed from the table and placed at the bottom" (gicc-agenda-20160810)
- "Pulled nested list out of table and placed it under the table" (gicc-agenda-20200506)
- "Link should be below list" (ncom-update-gicc-05-15-2014)
- "Paragraph break appears when link does, breaking text flow" (newsletter-with-many-images-21fb)
- "Links are being listed as a separate paragraph" (gicc-meeting-minutes-08072007)
- "Placed a link within a paragraph in its own `<p>`" (map-imagery-365a)
- "Unnecessary returns before and after URL links" (multi-factor-authentication-report-december-2015)
- "Hyperlinked content starts from the new line each time" (esrmo-newsletter-september-2021)

### O. Compressed/Cut Images

Image quality or cropping issues.

- "Compressed and cut images so that they are no longer viewable" (wearencgov-broadbandinitiatives)
- "cut off part of the NCDIT logo" (gicc-goals-and-strategic-direction-2021-23)
- "Image highlights missing" (near-perfect-powerpoint-slides-47b2)
- "Font styling examples not transferred" (near-perfect-powerpoint-slides-47b0)
- "Images transferred as just one cluster" (newsletter-with-many-images-117c)

### P. Logo Extraction Failures

Logos missing, duplicated, or replaced with text.

- "DPS Logo missing" (logo-imagery-graphic-colors-map-imagery-f80b, logo-imagery-graphic-colors-map-imagery-tables-4807)
- "MyNCID Logo not pulled in" (logo-imagery-screenshot-imagery-fca1)
- "Missing State Crest on all pages" (seal-imagery-table-with-shading-132c)
- "Failed to bring over the seal of the state of NC logo" (scio-physical-and-environmental-protection)
- "Replaced logo seal with screen text" (long-contract-many-pages-of-tables-6881)
- "Logo repeating" (logo-tables-shading-watermark-photos-13a3 — pg 3)
- "Duplicated logo" (logo-tables-shading-watermark-photos-13a3 — pg 8)
- "additional logo from the footer added" (nc-911-board-education-committee-meeting-agenda-packet)

### Q. Missing/Incorrect Footer Content

- "Footer is missing" (esrmo-newsletter-april-2017)
- "Footer repeated" (multi-factor-authentication-report-december-2015, nc-911-board-education-committee-meeting-agenda-packet)
- "Footer showing up mid-page" (nc-911-board-meeting-agenda-aug-26-2022)

### R. Content Loss

Gemini fails to extract content from pages.

- "Loss of text content" (logo-tables-shading-watermark-photos-13a3 — pg 12, 24)
- "Missing content" (map-imagery-f7f6, federalagencyhurricanecoordination)
- "Major content loss from the infographic" (logos-graphic-colors-53e1 — pg 14, 15)
- "Major content loss: headings in TOC missing" (long-contract-many-pages-of-tables-6881 — pg 26)
- "Heading text lost" (logos-graphic-colors-53e1 — pg 13, 23, 29, 41)
- "'Goals' heading lost" (logos-graphic-colors-53de — pg 13)
- "Missing 'Goal 1' Reference" (gicc-goals-and-strategic-direction-2021-23 — pg 5-8)
- "All content from page 21 missing" (powerpoint-slides-fef1)
- "Objectives missing" (esrmo-newsletter-april-2024 — pg 25)
- "Table of contents visual hierarchy lost" (logos-graphic-colors-53e1)

### S. List Type/Structure Errors from Extraction

Gemini misidentifies list type or structure.

- "A bulleted list (a,b,c) continued as an ordered list after page break" (gicc-mo-minutes-20191216)
- "Letters f, g, etc. are all a bulleted list instead of ordered list" (scio-physical-and-environmental-protection)
- "letters a & b are missing" (scio-physical-and-environmental-protection)
- "Sublist is an unordered list when it should be ordered" (powerpoint-slides-f832)
- "List bullets appearing in pdf, but not formatted as list in html" (logo-tables-shading-watermark-photos-13a3)
- "Using asterisks instead of `<ul>`" (map-imagery-0fb1)

### T. Link Not Detected (Not Visually Styled)

Gemini misses links that aren't blue/underlined.

- "A link in the pdf was missed, likely because not blue or underlined" (gicc-meeting-minutes-08072007)
- "missing multiple hyperlinks on text that is not shown as blue and underlined" (gicc-smac-agenda-20210120, logo-imagery-graphic-colors-map-imagery-6e2e)
- "Hyperlinks aren't formatted as hyperlinks" (seal-imagery-11ab)
- "Broadband hyperlink dropped" (mostly-text-charts-tables-screenshots-maps-67fb)
- "hyperlinks are missing" (esrmo-newsletter-september-2021)

### U. Video/Embedded Content Issues

- "Made text for link the alt text of embedded videos, link leads to youtube home page" (newsletter-with-many-images-117c)
- "Links to embedded videos lead to youtube home page" (newsletter-with-many-images-117c)

### V. Miscellaneous Extraction Issues

- "Entire PDF added as image then transcribed" (911-telecommunicators-resolution-mitchell-county, rockingham-county)
- "social media icons do not align with text" (gicc-goals-and-strategic-direction-2021-23)
- "AI created a strange image" (logo-tables-shading-watermark-photos-13a3 — pg 21)
- "Missed underlining text" (gicc-meeting-minutes-08072007)
- "Header should be before image and table" (gicc-ncdot-florence-20181107)
- "Some images nested as figures and others are not" (gicc-ncdot-florence-20181107)
- "Middle image not listed as a figure, missing caption" (gicc-ncdot-florence-20181107)
- "Checkmark image from end of list items placed at bottom of page" (ncom-update-gicc-05-15-2014)
- "Email address populated twice in table and 3rd time under table" (seal-imagery-table-with-shading-colored-text-672b)
- "Chart did not transfer properly" (wearencgov-presentation3)
- "Image on slide did not transfer into text" (wearencgov-presentation3)
- "The colors of the counties which correspond to the legend are not described in text" (map-imagery-logo-imagery-4809)
- "Pulled out text from distance image but doesn't make sense without image" (map-imagery-logo-imagery-4809)
- "Duplicate text used for purpose of example removed" (near-perfect-powerpoint-slides-47b0)
- "graph missing increase and decrease arrow indicators" (nc-911-board-education-committee-meeting-agenda-packet)

---

## Fixes Applied to extract_structured_json.py (5 total)

These changes address problems that originate during the extraction step. They modify post-processing logic in `extract_structured_json.py` and the Gemini extraction prompt (`PROMPT_FOR_EXTRACT.md`).

### EXT-1. Smart PyMuPDF Link Integration (replaces naive append)

**Problem:** PyMuPDF-extracted hyperlinks were blindly appended at the end of each page's content, causing:
- Duplicate links (Gemini already extracted them inline)
- Links separated from their context (placed at bottom of page instead of inline)
- Garbled text from PyMuPDF bbox text extraction (newline artifacts)
- Links from inside tables duplicated below the table

**What changed:** New `_merge_pymupdf_links()` method replaces the old `link_items = [...]` + `combined_content.extend(link_items)` pattern. The new approach:
1. Builds a lookup of PyMuPDF links by normalized display text
2. Enriches Gemini's existing link objects that have broken URLs (url == display text) with correct URLs from PyMuPDF
3. Collects ALL URLs already present in content (paragraphs, tables, lists, existing links)
4. Only adds PyMuPDF links whose URL is NOT already present in content
5. Cleans garbled text (newline/whitespace artifacts) from PyMuPDF link text

**Impact:** 650 trailing link items across 100 test files would be deduplicated. Fixes broken URLs like `"CLICK HERE"` → actual URL.

**CSV references:** cyber-incident-reporting ("Links inside a table placed below the table"), gicc-agenda-20160810 ("Links removed from table and placed at the bottom"), seal-image-table-6870 ("CLICK HERE has href of literally 'CLICK HERE'"), colored-text-logos-676a ("Duplicate links in footer"), logos-graphic-colors-table-screenshot-fc98 ("Creating extra links after the content"), long-contract-many-pages-of-tables-6881 ("Duplicated links at the bottom"), esrmo-newsletter-april-2017 ("all links grouped at end of page"), many others

---

### EXT-2. Cross-Page Header/Footer/Table Deduplication

**Problem:** Many PDFs have header tables or header/footer text that repeats on every page (e.g., document metadata tables with organization name, document number, effective date, page number). These repeat in the JSON because each page is processed independently.

**What changed:** New `_deduplicate_cross_page_content()` method runs after all pages are collected but before saving JSON. It:
1. Fingerprints all tables and header_footer items on page 1
2. Checks which fingerprints repeat on page 2
3. Removes matching items from pages 2+ (keeps page 1 intact)
4. Normalizes page numbers and markdown formatting before comparison so "Page 1 of 12" matches "Page 2 of 12"

**Impact:** 441 repeated items removed across 100 test files.

**CSV references:** scio-physical-and-environmental-protection ("The header was pulled over every time. Should just be pulled over once"), 2019-20-smac-work-plan ("Header text repeated on multiple pages"), nc-911-board-education-committee-meeting-agenda-packet ("data table header row repeated")

---

### EXT-3. Extraction Prompt Improvements (PROMPT_FOR_EXTRACT.md)

**Problem:** Gemini's extraction behavior caused several systematic issues that no amount of post-processing can fully fix. The prompt needed stronger guidance.

**Changes made to PROMPT_FOR_EXTRACT.md:**

1. **No spurious asterisks in table cells:** Added "CRITICAL: Do NOT add ** asterisks or * to table cell text. Table header cells are identified by position, not by markdown bold. Write cell text as plain text only."

2. **No spurious asterisks in paragraphs:** Added "CRITICAL: Do NOT add ** or * around text that is not bold or italic in the original PDF. Only use markdown formatting when the visual appearance clearly shows bold or italic styling"

3. **Better alt text guidance:** Added specific instructions for image descriptions — "Be specific: identify the subject (person, logo, map, chart type, screenshot subject), not generic labels like 'Document image'" and "CRITICAL: When a page has MULTIPLE images, ensure each image's description matches THAT specific image. Do NOT swap or combine descriptions across images."

4. **No screenshot transcription:** Added new section "IMPORTANT for screenshots and UI images" — do NOT transcribe all visible text from screenshots as separate content elements. Describe screenshots as images with summary descriptions.

5. **Better heading hierarchy:** Added "CRITICAL: Maintain proper heading hierarchy... subsections MUST use a deeper level than their parent. Do NOT make all headings the same level" and "Do NOT promote regular body text to headings just because it is bold or italic"

6. **No hallucinated content:** Added "CRITICAL: Do NOT hallucinate or invent content... Do NOT add links, text, or data that does not exist in the original document" and "Do NOT fabricate or guess URLs"

7. **Preserve numeric values:** Added "CRITICAL: Preserve exact numeric values from the document. Do NOT change prices, quantities, dates"

8. **Background images:** Added "When the same image appears as a background or decoration, do NOT transcribe its content as separate text elements"

**CSV references:** All files with "Asterisks added where formatting used", all files with "Alt text issues", powerpoint-slides-fef1 ("Transcribed the full text from the screenshot"), scanned-from-paper-many-pages-of-tables-6878 ("Hallucinated the incorrect price"), text-some-colored-text-3638 ("headers should be H3, but are H2"), many others

---

### EXT-4. Strip Markdown from Table Cells and Headings in Post-Processing

**Problem:** Even with prompt improvements, Gemini frequently adds `**bold**` markdown to table cell text and heading text. This causes duplicate formatting when the renderer also applies bold, or literal `**` showing up in output.

**What changed:** New `_strip_spurious_markdown()` method added to `_post_process_content()`. Runs after OCR normalization but before paragraph deduplication. Strips `***`, `**`, and `*` markdown formatting from:
- All table cell text
- All heading text

Carefully preserves text where asterisks are actual content (e.g., footnote markers like `IX5HF**` where there's no opening pair).

**Impact:** 1,663 table cells/headings cleaned across 100 test files.

**CSV references:** seal-imagery-table-with-shading-132c, seal-imagery-table-with-shading-colored-text-672b, smac-lidar-apr-10-2024, standards-committee-meeting-agenda-packet, table-seal-imagery-diagram-1468, tables-screenshots-photos-background-colors-59df, wearencgov-presentation3, logo-tables-shading-watermark-photos-13a3, logos-graphic-colors-table-screenshot-fc98, long-contract-many-pages-of-tables-6881, and many others with "Asterisks added where formatting used" or "Bold replaced by **"

---

### EXT-5. Duplicate Image Deduplication (Overlapping Bboxes)

**Problem:** PyMuPDF sometimes extracts the same page area as multiple images (e.g., same content captured at different sizes/resolutions). This caused images to appear twice or more in the output.

**What changed:** New `_deduplicate_overlapping_images()` method in `extract_images_from_pdf_page()`. After extracting images but before the 5+ image full-page-render threshold:
1. Compares bounding boxes of all extracted images
2. When two images overlap by >80%, keeps only the larger one
3. Uses the existing `_bboxes_overlap()` method for overlap detection

**CSV references:** nc-911-board-technology-committee-minutes ("Image copy of table copied over twice in two different sizes", "Image of entire page of document copied over in two different sizes"), nc-911-board-monthly-dispatch-march-2025 ("Every page has an image, and all of the images are embedded and all content is repeating"), near-perfect-powerpoint-slides-47b0 ("Image duplicated on page")

---

### EXT-6. Extend Markdown Stripping to List Items

**Problem:** Fix EXT-4 only stripped markdown from table cells and headings. List items also frequently had spurious `**bold**` markers, causing the same double-formatting issue.

**What changed:** Extended the Step 2 markdown stripping loop in `_post_process_content()` to also process list items and their children using the existing `_strip_spurious_markdown()` method.

**Impact:** 1,035 additional list items cleaned across 49 files (on top of the 1,663 table cells/headings from EXT-4, for a total of 2,698).

**CSV references:** 911-board-education-committee-meeting-minutes ("Asterisks not on PDF added to HTML"), 20200522-nc911-board-minutes-approved ("Asterisks add to HTML ordered list items"), gicc-mo-minutes-20191216, many others

---

### EXT-7. Strip Duplicate List Numbering from Ordered List Items

**Problem:** Gemini includes the list number/letter in the text of ordered list items (e.g., `"1. text"`, `"(a) text"`, `"iv. text"`) while also marking the list as `list_type: "ordered"`. When rendered as `<ol><li>`, this produces double numbering like "1. 1. text".

**What changed:** New `_strip_list_number_prefix()` method added as Step 3 in `_post_process_content()`. Strips leading numeric, alphabetic, and roman numeral prefixes from ordered list item text. Patterns handled:
- Numeric: `"1."`, `"1)"`, `"(1)"`
- Alphabetic: `"a."`, `"a)"`, `"(a)"`
- Roman numeral: `"i."`, `"ii)"`, `"(iii)"`

Only strips if followed by whitespace and more text, preventing false positives.

**Impact:** 762 list items cleaned across 32 files.

**CSV references:** 10-22-20-edu-committee-agenda-packet ("Ordered list keeping number in text instead of replacing"), seal-imagery-table-with-shading-132c ("Ordered list keeping numbers in text instead of replacing with letters and roman numerals"), gicc-meeting-minutes-08072007 ("restarts the list on the new page"), nc-911-board-meeting-agenda-aug-26-2022 ("numbering restarted from 1"), multi-factor-authentication-report-december-2015 ("extra numbers added to the lists"), nc-911-board-technology-committee-minutes ("List items incorrectly numbered, duplicate numbering"), mostly-text-charts-tables-screenshots-maps-67fb ("additional numbers were added to the TOC"), seal-imagery-table-with-shading-colored-text-672b ("Numbered lists adding additional numbers"), nc-911-board-minutes-september-30-2022 ("Number lists are all messed up")

---

### EXT-8. Merge Consecutive Fragmented Lists

**Problem:** Gemini sometimes splits a single logical list into multiple single-item list objects, especially when lists span page breaks or when each agenda item is treated as its own list. This creates incorrect document structure.

**What changed:** New `_merge_consecutive_lists()` method added as Step 4 in `_post_process_content()`. When adjacent list objects have the same `list_type` (both ordered or both unordered) with no intervening content, merges their items into a single list.

Only merges lists that are directly adjacent — lists with paragraphs or other content between them are preserved as separate lists.

**Impact:** 30 lists merged across 12 files.

**CSV references:** gicc-mo-minutes-20191216 ("A bulleted list continued as an ordered list after page break"), scio-physical-and-environmental-protection ("Letters f, g, etc. are all a bulleted list instead of ordered list")

---

### EXT-9. Remove "Page Intentionally Left Blank" Boilerplate

**Problem:** PDFs containing boilerplate text like "This page intentionally left blank" carried this text through to the JSON. While render_json.py already stripped these during rendering, having them in the JSON is unnecessary.

**What changed:** Added Step 5 in `_post_process_content()` that filters out paragraph/heading items matching blank page patterns. Handles multiple word orderings:
- "This page intentionally left blank"
- "Page left intentionally blank"
- "This page left blank intentionally"
- "This page was intentionally left blank."
- With or without surrounding markdown asterisks

**CSV references:** map-imagery-photos-tables-screenshots-diagrams-data-charts-365a ("page intentionally left blank literally added")

---

### EXT-10. Filter Large "Unidentified Image" Page Screenshots

**Problem:** When PyMuPDF extracts images that Gemini didn't describe, they're added as "Unidentified image" entries. Many of these are full-page or near-full-page screenshots that duplicate the text content already extracted by Gemini. They add no value and confuse the output with redundant page captures.

**What changed:** In `match_images_to_descriptions()`, unmatched PyMuPDF images whose bounding box covers >40% of the page area are now filtered out. These are almost always background images or page screenshots. Smaller unmatched images (logos, icons, decorative elements) are preserved.

**Impact:** 129 large page-screenshot images filtered across 23 files.

**CSV references:** nc-911-board-technology-committee-minutes ("Image of entire page of document copied over in two different sizes"), nc-911-board-minutes-september-30-2022 ("Every table was put in the footer and repeats three times"), map-imagery-ff40 ("Inserted a screenshot of the page"), logos-graphic-colors-table-screenshot-fc98 ("Image of main PDF pages duplicated by screen text"), powerpoint-slides-fef1 ("Put all the screenshots of background images into the HTML"), nc-911-board-monthly-dispatch-march-2025 ("all of the images are embedded and all content is repeating")

---

### EXT-11. Improved 2D Image-Description Position Matching

**Problem:** The original `match_images_to_descriptions()` only used vertical position (top/middle/bottom thirds of the page) to match Gemini's image descriptions to PyMuPDF's extracted images. When two images were at similar vertical positions but different horizontal positions (e.g., left vs right), descriptions could be assigned to the wrong image — causing "swapped alt text."

**What changed:** Enhanced position matching to use 2D Euclidean distance instead of 1D vertical distance:
1. Parse both vertical (top/middle/bottom) AND horizontal (left/center/right) components from Gemini's position string
2. Calculate target (x, y) coordinates from the position grid
3. Match using `sqrt((dx/page_width)^2 + (dy/page_height)^2)` — normalized 2D distance
4. This correctly distinguishes "top-left" from "top-right" images

**CSV references:** gicc-ncdot-florence-20181107 ("Alt text for images is swapped, tagged to the wrong image — pg 7, 10"), logos-graphic-colors-53de ("When a page has multiple images, the alt text is switched — pg 7, 8"), near-perfect-powerpoint-slides-47b2 ("Alt text for images swapped — pg 19"), near-perfect-powerpoint-slides-47b0 ("Alt text for image contains alt text for both images on the page — pg 25, 26")

---

### EXT-12. Fallback Image Rendering for Missing Images

**Problem:** When Gemini detects and describes an image but PyMuPDF fails to extract the binary data (no `base64_data`), the image appears as a broken/missing placeholder in the HTML output. This affected 488 images across 44 files.

**What changed:** New `_render_image_region_fallback()` method renders the approximate page region where the missing image should be, using PyMuPDF's `page.get_pixmap(clip=rect)`. After image matching in `process_single_page()`:
1. Identifies Gemini-described images without `base64_data`
2. Uses the position string to calculate the approximate bounding box
3. Renders that page region at RENDER_SCALE resolution
4. Stores the rendered PNG as fallback `base64_data`
5. Marks the image with `_fallback_render: True` for transparency

Only renders for images with actual descriptions (not "Unidentified image" or empty).

**Impact:** Up to 488 missing images could be recovered across 44 files (requires re-extraction to measure actual impact since this runs during the extraction pipeline).

**CSV references:** map-imagery-e5cc ("Multiple images missing"), powerpoint-slides-1793 ("Missing images"), esrmo-newsletter-december-2018 ("image missing"), map-imagery-logo-imagery-4809/f810 ("Image is missing / broken image icon"), gicc-tims-may-2016 ("Image depicting connections completely missing", "Missing graphic completely"), 911-education-committee-meeting-agenda-packet ("Missing image on page 37")

---

### EXT-13. Per-Image Alt Text Generation via Gemini

**Problem:** The original extraction generated alt text by having Gemini describe images from the full-page rendering. This caused:
- **Swapped alt text**: When multiple images were on the same page, descriptions were matched by position (top/middle/bottom), often assigning the wrong description to the wrong image
- **Generic descriptions**: Gemini produced vague labels like "Document image" instead of specific content descriptions
- **Combined descriptions**: One description covering both images on a page instead of separate descriptions for each
- **Wrong content**: Descriptions that didn't match the actual image at all (e.g., "NC logo" for a photo of people)

**What changed:** New `generate_alt_text_for_image()` and `regenerate_alt_text_for_images()` methods send each individual extracted image to Gemini with a focused alt text prompt. This runs:
1. **During extraction** (`ENABLE_PER_IMAGE_ALT_TEXT` flag): After images are matched to PyMuPDF data, each image with base64 data gets its own Gemini call
2. **Post-hoc** (`regenerate_alt_text.py` tool): Can regenerate alt text on existing JSON files without full re-extraction

Key design decisions:
- **No OCR**: The prompt explicitly says "Do NOT transcribe all text in the image — just summarize what it shows." Gemini generates visual descriptions, not text transcriptions.
- **Image positions unchanged**: Only the `description` field is updated. Image `bbox`, `position`, and reading order in the content array are preserved exactly.
- **Composite images**: When 5+ images merge into a single full-page render (marked `_full_page_render: True`), a specialized prompt generates one description for the composite — only ONE Gemini call for the combined image.
- **Tiny images skipped**: Images < 1KB (spacers, dots, 1-pixel images) are skipped to avoid wasting API calls.
- **Graceful failure**: If a Gemini call fails, the original description is preserved.

**Alt text prompt:**
> "Describe this image for use as alt text on a web page. Write a concise description (1-3 sentences) of what the image visually shows. Be specific: identify people, objects, logos, charts, maps, diagrams, or scenes. If there is text visible in the image (e.g., a title, label, or caption), include the key text. Do NOT say 'image of' or 'picture of'. Do NOT transcribe all text in the image — just summarize what it shows."

**Impact:** 443 images regenerated across 16 Section A files. All swapped, wrong, generic, and incomplete alt text issues in Section A are now fixed.

**Standalone tool:** `regenerate_alt_text.py` allows regenerating alt text on any existing JSON file:
```
python regenerate_alt_text.py <folder_name>           # Single file
python regenerate_alt_text.py <folder_name> --page 7  # Single page
python regenerate_alt_text.py --all                    # All files
python regenerate_alt_text.py --dry-run <folder>       # Preview
```

**CSV references:** All items in Section A above.

---

## Test Results

A test script (`test_post_processing.py`) was created to validate post-processing improvements against existing JSON files without re-running extraction. Results across all 100 test files:

| Fix | Metric | Impact |
|-----|--------|--------|
| EXT-1 (Link integration) | Trailing links deduplicated | 650 |
| EXT-2 (Cross-page dedup) | Repeated items removed | 441 |
| EXT-4+6 (Markdown stripping) | Cells/headings/list items cleaned | 2,698 |
| EXT-7 (List number stripping) | Duplicate numbers removed | 762 |
| EXT-8 (List merging) | Fragmented lists merged | 30 |
| EXT-10 (Large image filtering) | Page screenshots removed | 129 |
| EXT-13 (Per-image alt text) | Images with regenerated alt text | 443 |
| **Total** | **Content items improved** | **6,153** |

Additionally, the following fixes activate during the extraction pipeline (require re-extraction):

| Fix | Metric | Potential Impact |
|-----|--------|-----------------|
| EXT-3 (Prompt improvements) | Reduced asterisks, better alt text, no hallucination | All 100 files |
| EXT-5 (Image bbox dedup) | Overlapping duplicate images removed | ~23 files |
| EXT-9 (Blank page removal) | Boilerplate removed | ~3 files |
| EXT-11 (2D position matching) | Swapped alt text fixed | ~7 files |
| EXT-12 (Fallback rendering) | Missing images recovered | Up to 488 images in 44 files |
| EXT-13 (Per-image alt text) | Accurate per-image descriptions | All images in all files |

