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
- Use for body text, lists, and regular content (NOT headings)
- Preserve bold (**text**) and italics (*text*)
- Follow natural reading order (see Multi-Column Layouts section below)
- IGNORE page numbers, headers, and footers

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
- Do NOT group by type - interleave paragraphs, images, and tables as they appear on the page
- Be precise with table cell positions
- For tables, verify that all data rows have the same number of cells as header rows

Return ONLY the JSON array. No explanations or markdown code blocks.