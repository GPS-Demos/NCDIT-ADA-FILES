# render_json.py Fixes Documentation

## Overview

This document details all changes made to `render_json.py` to address problems identified in `problems.csv`, as well as problems that **cannot** be fixed in the renderer because they originate in the JSON extraction step (`extract_structured_json.py` / Gemini).

---

## Fixes Applied to render_json.py (27 total)

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

## Problems That CANNOT Be Fixed in render_json.py

These issues originate in the JSON extraction step (Gemini/PyMuPDF) and require changes to `extract_structured_json.py` or the Gemini extraction prompt.

### A. Wrong/Inaccurate/Swapped Alt Text on Images

Gemini generates the alt text during extraction. The renderer outputs whatever is in the JSON.

- "alt text is wrong" (gicc-tims-may-2016 — pg 5, 6, 7, 9, 12, 13, 15, 22, 23)
- "Alt text for images is swapped (tagged to the wrong image)" (gicc-ncdot-florence-20181107 — pg 7, 10)
- "Incorrect alt text on images" (newsletter-with-many-images-117c, 21fb, powerpoint-slides-1793)
- "Alt text just says 'Document image'" (near-perfect-powerpoint-slides-47b2 — pg 16)
- "Image of drone has completely wrong alt text" (gicc-ncdot-florence-20181107 — pg 5)
- "When a page has multiple images, the alt text is switched" (logos-graphic-colors-53de — pg 7, 8)
- "Alt text for images swapped" (near-perfect-powerpoint-slides-47b2 — pg 19)
- "Alt text for image contains alt text for both images on the page" (near-perfect-powerpoint-slides-47b0 — pg 25, 26)
- "alt text not complete" (gicc-tims-may-2016 — pg 1)
- "Alt text includes 'sheriff's office personnel' but seems like hallucination" (logos-graphic-colors-53e1 — pg 21)
- "Incomplete alt text for large flow chart" (logos-graphic-colors-53e1 — pg 32)
- "An image of people's hands up but alt text says it's the NC logo" (map-imagery-ff40 — pg 13)
- "Describes state seal but not anything else in the image (flow chart)" (agency-onboarding-68607a87)
- "Text in logos not used in alt text" (logo-tables-shading-watermark-photos-13a3 — pg 8)
- "Some of the alt text is confusing and listed as a comment" (gicc-ncdot-florence-20181107 — pg 2)
- "Image alt text and captions mixed up" (newsletter-with-many-images-117c)
- "alt text is incorrect" (logo-imagery-screenshot-imagery-fca1)
- "Text below images included with image and document image alt text" (208m-endpoint-reseller-price-list — pg 9-10)
- "Alt text issues" (gdac-legislative-report-may-2016, gicc-2020-census-nc-factsheet, multiple powerpoint files)

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
- "figcaption created on short alt text" (logo-tables-shading-watermark-photos-13a3)
- "Strange figcaption added (38%)" (logo-tables-shading-watermark-photos-13a3)
- "Duplicate text used for purpose of example removed" (near-perfect-powerpoint-slides-47b0)
- "graph missing increase and decrease arrow indicators" (nc-911-board-education-committee-meeting-agenda-packet)

---

## Remaining Legitimate `**` in Output

5 files still contain literal `**` characters that are actual footnote markers in the original PDF:

| File | Example | Reason |
|------|---------|--------|
| long-contract-many-pages-of-tables-6881 | `IX5HF**`, `**Includes Quadient...` | Footnote markers |
| seal-imagery-table-with-shading-colored-text-672b | `** Agencies should contact...` | Footnote annotation |
| federalagencyhurricanecoordination-686132f8 | Various `**` in content | Presentation annotations |
| powerpoint-slides-1793 | Various `**` in content | Slide annotations |
| powerpoint-slides-ff0c | Various `**` in content | Slide annotations |
