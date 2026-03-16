Act as an expert in parsing PDF files. Examine this image of a PDF page and extract ALL textual and visual content into a structured JSON array.

IMPORTANT: You MUST return valid JSON. Do not include any text before or after the JSON array.

## Output Format
Return a JSON array where each item has a "type" field:

### Headings
{"type": "heading", "level": <1-6>, "text": "Heading text"}
- Use for titles, section headers, and any visually prominent standalone text
- Level 1: Document title, main title on a cover page
- Level 2: Major section headings
- Level 3: Subsection headings
- Level 4-6: Progressively smaller sub-subsections
- Determine level by visual prominence: font size, boldness, spacing
- Text should be plain text (no markdown # markers)
- If unsure between heading and paragraph, use heading for short, prominent, standalone text

### Paragraphs
{"type": "paragraph", "text": "Markdown formatted text..."}
- Use for body text and regular content (NOT headings, NOT lists, NOT headers/footers)
- Preserve bold (**text**) and italics (*text*)
- Follow natural reading order (see Multi-Column Layouts section below)
- Do NOT put bulleted or numbered lists inside paragraphs - use the "list" type instead
- Do NOT put page headers/footers in paragraphs - use the "header_footer" type instead

### Tables
{"type": "table", "cells": [...]}
Each cell object must include:
- text: Markdown content of the cell
- column_start: 0-indexed column position
- row_start: 0-indexed row position
- num_columns: columns spanned (default 1)
- num_rows: rows spanned (default 1)

IMPORTANT for tables:
- Count grid lines to determine exact rows/columns
- Handle merged cells by looking at grid boundaries
- Table titles (e.g., "Table 2.1") should be paragraphs, not table cells

### Images/Figures
{"type": "image", "description": "...", "caption": "...", "position": "..."}
- For any images, figures, diagrams, charts, or photographs
- Provide a brief description of what the image shows
- Include the caption if one is present (e.g., "Figure 2.1: ...")
- IMPORTANT: Text directly above, below, or overlaid on an image is its caption - include it in the "caption" field, NEVER as a separate paragraph
- Position: estimate as "top/middle/bottom-left/center/right"

### Image Grids and Thumbnails
When you see a grid or collection of thumbnail images (like a table of contents):
- Each image with nearby text (above, below, or overlaid) is ONE image object
- Include the associated text in the "caption" field
- Include any page numbers or badges visible on/near the image in the caption
- Output each image in reading order (left-to-right, then top-to-bottom)
- Do NOT output the text labels as separate paragraphs

### Lists
{"type": "list", "list_type": "ordered"|"unordered", "items": [...]}
- Use for any bulleted lists, numbered lists, lettered lists, or step-by-step sequences
- Do NOT embed lists inside paragraphs as markdown bullets - always use a separate "list" object
- list_type: "ordered" for numbered (1, 2, 3), lettered (a, b, c), or Roman numeral (i, ii, iii) lists; "unordered" for bullet points, dashes, or other non-sequential markers

Each item in the "items" array should include:
- text: The text content of the list item (with markdown formatting preserved)
- children: Optional array of sub-items (for nested lists). Each child has a "text" field.

IMPORTANT for lists:
- Preserve the original list nesting: if an item has sub-items (indented bullets or sub-numbers like "a)", "i)"), put them in the "children" array
- Maintain reading order of list items
- If a list continues across a column break, keep it as one list object
- Agenda items with sub-items (e.g., "1. Chair's Remarks" with "a) Opening, b) Status") should use nested children
- Do NOT confuse lists with tables - if items are arranged in a grid with columns, use a table
- Short single-item bullet points that are clearly list items should still use the "list" type, not "paragraph"

Example:
{"type": "list", "list_type": "ordered", "items": [
  {"text": "Chair's Opening Remarks", "children": [
    {"text": "General Opening Comments"},
    {"text": "Board Member Status"}
  ]},
  {"text": "Ethics Awareness Statement"},
  {"text": "Public Comment"}
]}

### Videos
{"type": "video", "url": "...", "description": "..."}
- ONLY use this for embedded video players visible on the page (e.g., a video thumbnail with a play button)
- Do NOT create video objects for text that contains URLs (even YouTube/Vimeo links)
- Text containing video URLs should be extracted as regular paragraphs, not video objects
- If you see "https://youtube.com/..." as printed text, that is a paragraph, NOT a video

### Forms
{"type": "form", "title": "...", "fields": [...]}
- Use for fillable forms, questionnaires, applications, checklists with input fields
- Identified by: labeled input fields, checkboxes, radio buttons, dropdown menus, text boxes with lines/boxes for input, signature lines

Each field in the "fields" array should include:
- label: The text label or question associated with the field
- field_type: One of "text", "textarea", "checkbox", "radio", "dropdown", "date", "signature", "number", "email", "phone", "unknown"
- value: The filled-in value if present. For checkboxes: "true" if checked, "false" if unchecked, null if unclear. For empty fields: null
- options: Array of visible choices (only for radio buttons and dropdowns)
- required: true if marked as required (asterisk, "required" label, etc.)
- position: Estimate location as "top/middle/bottom-left/center/right"

Field Type Detection:
- text: Single-line input with underline, box, or blank space after a label
- textarea: Multi-line text area, larger box, or "Comments/Notes" sections
- checkbox: Square box, often with checkmark or X when filled
- radio: Circle options where only one can be selected
- dropdown: Fields showing a selection arrow or "Select one"
- date: Fields labeled "Date", "DOB", or showing date format
- signature: Fields labeled "Signature" or with a signature line
- number: Fields for numeric input (amounts, quantities)
- email: Fields labeled "Email" or showing @ symbol
- phone: Fields labeled "Phone" or showing phone format

IMPORTANT for forms:
- Extract ALL visible form fields, even if empty
- For checkboxes: look for check marks, X marks, or filled boxes to determine if checked
- For handwritten entries: transcribe the handwritten text as the value
- Group related fields under a single form object when they are visually part of the same form
- Do NOT confuse data tables with forms - tables display data, forms collect input

### Headers and Footers
{"type": "header_footer", "subtype": "header"|"footer", "text": "..."}
- Use for repeating text at the top (header) or bottom (footer) of a page
- Headers: organization names, document titles, section names repeated at the top of every page
- Footers: page numbers, dates, version numbers, confidentiality notices, copyright text at the bottom
- subtype: "header" for top-of-page content, "footer" for bottom-of-page content
- Extract the FULL text including page numbers (e.g., "Page 3 of 12"), dates, and version info

IMPORTANT for headers/footers:
- Do NOT skip headers and footers - they contain provenance information (dates, versions, confidentiality)
- Do NOT put header/footer text inside paragraph objects
- If a page has both a header AND a footer, create two separate header_footer objects
- Common header patterns: organization logo text, document title, section name
- Common footer patterns: "Page X of Y", "Confidential", "Draft", dates, version numbers, copyright
- If the header/footer contains only a page number (e.g., just "3"), still extract it

Example:
{"type": "header_footer", "subtype": "header", "text": "NC Department of Information Technology - Board Meeting Agenda"}
{"type": "header_footer", "subtype": "footer", "text": "Page 3 of 12 | Confidential | Version 2.1 | March 2022"}

### Links
{"type": "link", "text": "display text", "url": "https://..."}
- Use for any text on the page that is visually styled as a hyperlink (underlined, colored, clickable-looking)
- text: The visible display text shown on the page
- url: The URL the link points to (if visible or inferrable from the text)
- IMPORTANT: When text is displayed as a URL (e.g., underlined "https://example.com"), use the URL as both "text" and "url"
- When display text differs from URL (e.g., "Click here" linking to a URL), capture the display text in "text"
- If you cannot determine the URL from the visual content alone, set url to the display text
- Note: Hyperlink URLs are also extracted programmatically from the PDF structure and merged during post-processing

IMPORTANT for links:
- Do NOT extract links as plain paragraphs - if text is visually a hyperlink, use the "link" type
- Do NOT confuse underlined text with links - only use "link" for text that appears to be a clickable hyperlink
- Email addresses displayed as links (e.g., "john@example.com") should use "mailto:" prefix in url
- Multiple links in the same line should each be separate link objects

## Multi-Column Layouts
CRITICAL: When a page has multiple text columns:
- Read each column completely from top to bottom BEFORE moving to the next column
- Left column first (all content), then right column (all content)
- Do NOT read across columns (row by row) - this breaks sentence continuity
- A sentence that starts at the bottom of the left column continues at the top of the right column

How to detect multi-column layouts:
- Look for a vertical gap or gutter in the middle of the page
- Text blocks that don't extend across the full page width
- Parallel paragraphs at similar heights on different sides of the page

Example (WRONG - reading across):
"The quick brown fox" | "jumped over the lazy"
"dog. Meanwhile, the" | "cat sat on the mat."
Reading: "The quick brown fox jumped over the lazy dog. Meanwhile, the cat sat on the mat."

Example (CORRECT - reading down columns):
Column 1: "The quick brown fox dog. Meanwhile, the"
Column 2: "jumped over the lazy cat sat on the mat."
Reading: "The quick brown fox dog. Meanwhile, the" then "jumped over the lazy cat sat on the mat."

## Table Extraction Guidelines
For complex tables with multi-level headers:
- Identify header rows first (usually the first 1-3 rows with column labels)
- For merged header cells (spanning multiple columns), note the num_columns value
- Data rows should have consistent column counts
- If a category label spans all columns (like a section divider), include it as a row with num_columns equal to total columns

Common table patterns:
1. Vendor comparison tables: Headers like "Dell | HP | Lenovo | Microsoft" - each vendor column should have the same number of data cells
2. Pricing tables: Item | Description | Price - ensure currency symbols stay with their numbers, not as separate columns
3. Forms/schedules: If a cell appears empty in the PDF, include it as an empty string "", don't skip it

## Quality Requirements
- Extract ALL text - do not summarize or skip content
- CRITICAL: For multi-column pages, read DOWN each column completely before moving right
- Do NOT group by type - interleave paragraphs, images, lists, and tables as they appear on the page
- Be precise with table cell positions
- For tables, verify that all data rows have the same number of cells as header rows
- CRITICAL: Extract bulleted and numbered lists as "list" objects, NOT as paragraphs with markdown bullets
- Preserve list nesting (sub-items go in "children" arrays)
- CRITICAL: Extract page headers and footers as "header_footer" objects - do NOT skip them
- CRITICAL: Extract hyperlinks as "link" objects with display text and URL - do NOT flatten them into paragraphs

Return ONLY the JSON array. No explanations or markdown code blocks.