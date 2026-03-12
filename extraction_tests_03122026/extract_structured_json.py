"""
PDF Structured JSON Extraction Tool with Quality Verification

This script processes all PDFs in the pdfs/ folder, extracts structured JSON
(paragraphs, tables, images) using Gemini, and verifies extraction quality.

Usage:
    python extract_structured_json.py

Output:
    - Per-PDF JSON files: output/{pdf_id}.json
    - Aggregate reports: output/_reports/summary.json, quality_report.html
"""

import base64
import json
import re
from datetime import datetime, timezone
from difflib import SequenceMatcher
from multiprocessing import Pool
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import backoff
import logging
import fitz  # PyMuPDF
import pypdfium2 as pdfium
from tqdm import tqdm
from google import genai
from google.genai import types

# Configuration
PROJECT_ID = "playground-439016"
REGION = "global"  # so we can call Gemini 3
GEMINI_MODEL = "gemini-3.1-flash-lite-preview"
MAX_OUTPUT_TOKENS = 65500
TEMPERATURE_EXTRACTION = 1.0  # Gemini 3.x default; lower values can cause looping/degradation
TEMPERATURE_VALIDATION = 1.0  # Gemini 3.x default; lower values can cause looping/degradation
TOP_P = 0.95
TOP_K = 40

# Processing settings
MAX_WORKERS = 10  # Number of pages to process in parallel
SIMILARITY_THRESHOLD = 0.80
RENDER_SCALE = 3  # 216 DPI (was 2 = 144 DPI). Increase to 4 for 288 DPI if needed.

# Feature flags
ENABLE_COHERENCE_CHECK = True  # LLM-based quality check
ENABLE_IMAGE_EXTRACTION = True  # Include base64 image data in output
ENABLE_VIDEO_DETECTION = True

# Video platform patterns
VIDEO_PATTERNS = [
    r'youtube\.com/watch',
    r'youtu\.be/',
    r'vimeo\.com/',
    r'sharepoint\.com.*video',
    r'sharepoint\.com.*:v:',
    r'stream\.microsoft\.com',
]

# Directories
DATA_FOLDER = Path("../output-96-files-03-10-2026/ncdit-audit-20260310-073415")
OUTPUT_FOLDER = Path("output")
REPORTS_FOLDER = OUTPUT_FOLDER / "_reports"

# Test file list - if set, only process these document IDs
TEST_FILE_LIST = Path("NC ADA 100 Test files.md")


# Suppress Google GenAI warning about non-text parts (thought_signature)
# See: https://github.com/googleapis/python-genai/issues/850
class _SuppressNonTextPartsWarning(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return "there are non-text parts in the response:" not in record.getMessage()


logging.getLogger("google_genai.types").addFilter(_SuppressNonTextPartsWarning())


# Initialize Google Gen AI client (uses Vertex AI backend)
client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=REGION
)


def read_string_from_file(fname):
    with open(fname, "r") as f:
        return f.read()


EXTRACTION_PROMPT = read_string_from_file("PROMPT_FOR_EXTRACT.md")
COHERENCE_CHECK_PROMPT = read_string_from_file("PROMPT_FOR_VALIDATE.md")


def parse_test_file_list(md_path: Path) -> List[str]:
    """Parse document IDs from the test files list.

    Supports two formats:
    1. Plain text: one document ID per line
    2. Markdown table: document names in the second column (| # | Document | ...)

    Returns list of document IDs (folder names under data/).
    """
    if not md_path.exists():
        print(f"Warning: Test file list not found at {md_path}, processing all PDFs")
        return []

    text = md_path.read_text(encoding="utf-8")
    doc_ids = []

    # Detect format: if any non-empty line starts with |, treat as markdown table
    lines = text.splitlines()
    is_table = any(line.strip().startswith("|") for line in lines if line.strip())

    if is_table:
        for line in lines:
            line = line.strip()
            if not line.startswith("|"):
                continue
            cols = [c.strip() for c in line.split("|")]
            if len(cols) < 3:
                continue
            num_col = cols[1]
            if not num_col or num_col.startswith("#") or num_col.startswith(":") or num_col.startswith("-"):
                continue
            try:
                int(num_col)
            except ValueError:
                continue
            doc_id = cols[2]
            if doc_id:
                doc_ids.append(doc_id)
    else:
        # Plain text: one document ID per line
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#"):
                doc_ids.append(line)

    return doc_ids

# Schema for structured output - uses anyOf for type-specific field validation
# Each content type only allows its specific fields to reduce token usage and prevent field confusion
# Note: Uses standard JSON Schema types (lowercase) for google-genai SDK
EXTRACTION_SCHEMA = {
    "type": "array",
    "items": {
        "anyOf": [
            # Heading: type, level, text
            {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["heading"]},
                    "level": {"type": "integer"},
                    "text": {"type": "string"},
                },
                "required": ["type", "level", "text"],
            },
            # Paragraph: type, text
            {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["paragraph"]},
                    "text": {"type": "string"},
                },
                "required": ["type", "text"],
            },
            # Table: type, cells
            {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["table"]},
                    "cells": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string"},
                                "column_start": {"type": "integer"},
                                "row_start": {"type": "integer"},
                                "num_columns": {"type": "integer"},
                                "num_rows": {"type": "integer"},
                            },
                            "required": ["text", "column_start", "row_start"],
                        },
                    },
                },
                "required": ["type", "cells"],
            },
            # Image: type, description, caption, position
            {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["image"]},
                    "description": {"type": "string"},
                    "caption": {"type": "string"},
                    "position": {"type": "string"},
                },
                "required": ["type", "description"],
            },
            # Video: type, url, description
            {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["video"]},
                    "url": {"type": "string"},
                    "description": {"type": "string"},
                },
                "required": ["type", "url"],
            },
            # Form: type, title, fields
            {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["form"]},
                    "title": {"type": "string"},
                    "fields": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "label": {"type": "string"},
                                "field_type": {
                                    "type": "string",
                                    "enum": [
                                        "text", "textarea", "checkbox", "radio",
                                        "dropdown", "date", "signature", "number",
                                        "email", "phone", "unknown"
                                    ],
                                },
                                "value": {"type": "string"},
                                "options": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                },
                                "required": {"type": "boolean"},
                                "position": {"type": "string"},
                            },
                            "required": ["label", "field_type"],
                        },
                    },
                },
                "required": ["type", "fields"],
            },
            # List: type, list_type, items (supports nested lists)
            {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["list"]},
                    "list_type": {
                        "type": "string",
                        "enum": ["ordered", "unordered"],
                    },
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string"},
                                "children": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "text": {"type": "string"},
                                        },
                                        "required": ["text"],
                                    },
                                },
                            },
                            "required": ["text"],
                        },
                    },
                },
                "required": ["type", "list_type", "items"],
            },
            # Header/Footer: type, subtype, text
            {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["header_footer"]},
                    "subtype": {
                        "type": "string",
                        "enum": ["header", "footer"],
                    },
                    "text": {"type": "string"},
                },
                "required": ["type", "subtype", "text"],
            },
            # Link: type, text, url
            {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["link"]},
                    "text": {"type": "string"},
                    "url": {"type": "string"},
                },
                "required": ["type", "text", "url"],
            },
        ],
    },
}


def _esc(text: str) -> str:
    """HTML-escape a string."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_content_item_html(item: Dict) -> str:
    """Render a single extracted content item as an HTML fragment.

    Handles all schema types: heading, paragraph, table, image, video,
    form, list, header_footer, link.
    """
    item_type = item.get("type", "unknown")

    if item_type == "heading":
        level = item.get("level", 1)
        text = _esc(item.get("text", ""))
        return (
            f'<div class="content-item">'
            f'<div class="content-type">Heading (H{level})</div>'
            f'<div><strong>{text}</strong></div>'
            f'</div>'
        )

    if item_type == "paragraph":
        text = _esc(item.get("text", ""))
        return (
            f'<div class="content-item">'
            f'<div class="content-type">Paragraph</div>'
            f'<div>{text}</div>'
            f'</div>'
        )

    if item_type == "table":
        cells = item.get("cells", [])
        if not cells:
            return (
                '<div class="content-item">'
                '<div class="content-type">Table (empty)</div>'
                '</div>'
            )
        max_row = max((c.get("row_start", 0) + c.get("num_rows", 1)) for c in cells)
        max_col = max((c.get("column_start", 0) + c.get("num_columns", 1)) for c in cells)
        tbl = '<table class="extracted-table">'
        for r in range(max_row):
            tbl += "<tr>"
            for c in range(max_col):
                cell_text = ""
                for cell in cells:
                    if cell.get("row_start") == r and cell.get("column_start") == c:
                        cell_text = _esc(cell.get("text", ""))
                        break
                tbl += f"<td>{cell_text}</td>"
            tbl += "</tr>"
        tbl += "</table>"
        return (
            f'<div class="content-item">'
            f'<div class="content-type">Table ({len(cells)} cells)</div>'
            f'{tbl}'
            f'</div>'
        )

    if item_type == "image":
        desc = _esc(item.get("description", "No description"))
        caption = item.get("caption", "")
        caption_html = f"<div><em>{_esc(caption)}</em></div>" if caption else ""
        return (
            f'<div class="content-item">'
            f'<div class="content-type">Image</div>'
            f'<div>{desc}</div>'
            f'{caption_html}'
            f'</div>'
        )

    if item_type == "video":
        url = _esc(item.get("url", ""))
        return (
            f'<div class="content-item">'
            f'<div class="content-type">Video</div>'
            f'<div><a href="{url}" target="_blank">{url}</a></div>'
            f'</div>'
        )

    if item_type == "form":
        form_title = _esc(item.get("title", "Untitled Form"))
        fields = item.get("fields", [])
        ftbl = '<table class="extracted-table"><tr><th>Label</th><th>Type</th><th>Value</th></tr>'
        for field in fields:
            label = _esc(field.get("label", ""))
            ftype = _esc(field.get("field_type", "unknown"))
            value = _esc(str(field.get("value") or "[empty]"))
            ftbl += f"<tr><td>{label}</td><td>{ftype}</td><td>{value}</td></tr>"
        ftbl += "</table>"
        return (
            f'<div class="content-item">'
            f'<div class="content-type">Form: {form_title}</div>'
            f'{ftbl}'
            f'</div>'
        )

    if item_type == "list":
        list_type = item.get("list_type", "unordered")
        tag = "ol" if list_type == "ordered" else "ul"
        items_html = ""
        for li in item.get("items", []):
            children_html = ""
            children = li.get("children", [])
            if children:
                children_html = "<ul>"
                for child in children:
                    children_html += f"<li>{_esc(child.get('text', ''))}</li>"
                children_html += "</ul>"
            items_html += f"<li>{_esc(li.get('text', ''))}{children_html}</li>"
        return (
            f'<div class="content-item">'
            f'<div class="content-type">List ({list_type})</div>'
            f'<{tag}>{items_html}</{tag}>'
            f'</div>'
        )

    if item_type == "header_footer":
        subtype = item.get("subtype", "header")
        label = "Header" if subtype == "header" else "Footer"
        text = _esc(item.get("text", ""))
        color = "#607D8B"
        return (
            f'<div class="content-item" style="border-left-color: {color}; background: #eceff1;">'
            f'<div class="content-type">{label}</div>'
            f'<div style="color: #546E7A; font-size: 0.9em;">{text}</div>'
            f'</div>'
        )

    if item_type == "link":
        text = _esc(item.get("text", ""))
        url = item.get("url", "")
        url_esc = _esc(url)
        return (
            f'<div class="content-item" style="border-left-color: #1976D2;">'
            f'<div class="content-type">Link</div>'
            f'<div><a href="{url_esc}" target="_blank">{text}</a></div>'
            f'<div style="font-size: 0.8em; color: #999;">{url_esc}</div>'
            f'</div>'
        )

    # Fallback for unknown types
    return (
        f'<div class="content-item">'
        f'<div class="content-type">{_esc(item_type)}</div>'
        f'<div>{_esc(json.dumps(item, default=str)[:500])}</div>'
        f'</div>'
    )


# Shared CSS used by both per-document HTML and sample review HTML
CONTENT_CSS = """
    body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.5; }
    h1 { color: #333; border-bottom: 2px solid #2196F3; padding-bottom: 10px; }
    h2 { color: #555; margin-top: 30px; }
    .page-section { margin: 20px 0; padding: 15px; border: 1px solid #e0e0e0; border-radius: 8px; background: #fafafa; }
    .page-header { font-size: 1.1em; font-weight: bold; color: #333; margin-bottom: 10px; padding-bottom: 8px; border-bottom: 1px solid #ddd; }
    .content-item { margin-bottom: 10px; padding: 8px; border-left: 3px solid #2196F3; background: #f5f5f5; }
    .content-type { font-weight: bold; color: #666; font-size: 0.85em; text-transform: uppercase; margin-bottom: 4px; }
    table.extracted-table { border-collapse: collapse; width: 100%; font-size: 0.9em; }
    table.extracted-table th, table.extracted-table td { border: 1px solid #ddd; padding: 4px 8px; }
    table.extracted-table th { background: #e0e0e0; }
    .meta { color: #888; font-size: 0.9em; margin-bottom: 15px; }
    ol, ul { margin: 4px 0; padding-left: 24px; }
    a { color: #1976D2; text-decoration: none; }
    a:hover { text-decoration: underline; }
"""


def generate_document_html(result: Dict, output_path: Path):
    """Generate a full HTML document from a single PDF's extracted JSON.

    Args:
        result: The full extraction result dict for one PDF (with pages array).
        output_path: Path to write the .html file.
    """
    pdf_id = result.get("pdf_id", "unknown")
    total_pages = result.get("total_pages", 0)
    timestamp = result.get("extraction_timestamp", "")
    metrics = result.get("quality_metrics", {})
    coherence = metrics.get("avg_coherence_score", "N/A")

    pages_html = ""
    for page in result.get("pages", []):
        page_num = page.get("page_number", "?")
        error = page.get("error")
        content = page.get("content", [])
        val = page.get("validation", {})
        page_coherence = val.get("coherence_score", "N/A")

        if error:
            content_html = f'<p style="color: #c62828;">Extraction error: {_esc(error)}</p>'
        elif not content:
            content_html = '<p style="color: #999;">No content extracted</p>'
        else:
            content_html = "\n".join(render_content_item_html(item) for item in content)

        pages_html += f"""
    <div class="page-section">
        <div class="page-header">Page {page_num} <span style="font-weight: normal; color: #888;">(coherence: {page_coherence}/10)</span></div>
        {content_html}
    </div>
"""

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{_esc(pdf_id)} - Extracted Content</title>
    <style>{CONTENT_CSS}</style>
</head>
<body>
    <h1>{_esc(pdf_id)}</h1>
    <div class="meta">
        Pages: {total_pages} | Avg Coherence: {coherence}/10 | Extracted: {timestamp}
    </div>
{pages_html}
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


def _render_single_page(args: Tuple[str, int]) -> bytes:
    """Render a single PDF page to PNG bytes. Module-level for ProcessPoolExecutor."""
    import io
    pdf_path_str, page_num = args
    doc = pdfium.PdfDocument(pdf_path_str)
    page = doc.get_page(page_num)
    bitmap = page.render(scale=RENDER_SCALE)
    pil_image = bitmap.to_pil()
    buffer = io.BytesIO()
    pil_image.save(buffer, format="PNG")
    return buffer.getvalue()


def _process_page_worker(args: Tuple[str, int, str]) -> Tuple[str, int, Dict]:
    """Process a single PDF page in a worker process.

    Module-level function for multiprocessing.Pool. Each worker process
    re-imports this module and gets its own Gemini client.

    Args:
        args: Tuple of (pdf_path_str, page_num, doc_id)

    Returns:
        Tuple of (doc_id, page_num, result_dict)
    """
    pdf_path_str, page_num, doc_id = args
    extractor = PDFExtractor()
    result = extractor.process_single_page(Path(pdf_path_str), page_num)
    return doc_id, page_num, result


def get_safety_settings():
    """Return safety settings that allow all content."""
    return [
        types.SafetySetting(
            category="HARM_CATEGORY_HARASSMENT",
            threshold="BLOCK_NONE"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_HATE_SPEECH",
            threshold="BLOCK_NONE"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
            threshold="BLOCK_NONE"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_DANGEROUS_CONTENT",
            threshold="BLOCK_NONE"
        ),
    ]


class PDFExtractor:
    """Main class for PDF extraction with quality verification."""

    def __init__(self):
        self.stats = {
            "total_pdfs": 0,
            "total_pages": 0,
            "successful_extractions": 0,
            "failed_extractions": 0,
            "pages_by_confidence": {"high": 0, "medium": 0, "low": 0},
            "total_input_tokens": 0,
            "total_output_tokens": 0,
        }

    def render_page_to_image(self, pdf_path: Path, page_num: int) -> bytes:
        """Render a PDF page to PNG image bytes."""
        doc = pdfium.PdfDocument(str(pdf_path))
        page = doc.get_page(page_num)
        bitmap = page.render(scale=RENDER_SCALE)
        pil_image = bitmap.to_pil()

        # Convert to bytes
        import io
        buffer = io.BytesIO()
        pil_image.save(buffer, format="PNG")
        return buffer.getvalue()

    @backoff.on_exception(backoff.expo, Exception, max_tries=2)
    def call_gemini_for_extraction(self, image_bytes: bytes, temperature: float = TEMPERATURE_EXTRACTION) -> Tuple[str, int, int]:
        """Call Gemini API with structured output schema (synchronous).

        Args:
            image_bytes: PNG image data
            temperature: Model temperature (default TEMPERATURE_EXTRACTION)

        Returns:
            Tuple of (response_text, input_tokens, output_tokens)
        """
        model = GEMINI_MODEL

        config = types.GenerateContentConfig(
            max_output_tokens=MAX_OUTPUT_TOKENS,
            temperature=temperature,
            top_p=TOP_P,
            top_k=TOP_K,
            response_mime_type="application/json",
            response_schema=EXTRACTION_SCHEMA,
            safety_settings=get_safety_settings(),
            media_resolution=types.MediaResolution.MEDIA_RESOLUTION_HIGH
        )

        response = client.models.generate_content(
            model=model,
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
                EXTRACTION_PROMPT,
            ],
            config=config,
        )

        # Extract token usage from response metadata
        input_tokens = getattr(response.usage_metadata, 'prompt_token_count', 0) or 0
        output_tokens = getattr(response.usage_metadata, 'candidates_token_count', 0) or 0

        return response.text, input_tokens, output_tokens

    @backoff.on_exception(backoff.expo, Exception, max_tries=2)
    def call_gemini_text_sync(self, prompt: str, temperature: float = TEMPERATURE_VALIDATION) -> Tuple[str, int, int]:
        """Call Gemini API with text-only prompt (no image).

        Returns:
            Tuple of (response_text, input_tokens, output_tokens)
        """
        config = types.GenerateContentConfig(
            max_output_tokens=MAX_OUTPUT_TOKENS,
            temperature=temperature,
            top_p=TOP_P,
            top_k=TOP_K,
            safety_settings=get_safety_settings(),
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=config,
        )

        # Extract token usage from response metadata
        input_tokens = getattr(response.usage_metadata, 'prompt_token_count', 0) or 0
        output_tokens = getattr(response.usage_metadata, 'candidates_token_count', 0) or 0

        return response.text, input_tokens, output_tokens

    def check_coherence(self, content: List[Dict]) -> Tuple[Dict, int, int]:
        """
        Use LLM to evaluate the coherence and completeness of extracted content.

        Returns:
            Tuple of (result dict with coherence_score and issues, input_tokens, output_tokens)
        """
        if not ENABLE_COHERENCE_CHECK:
            return {"coherence_score": None, "issues": []}, 0, 0

        # Format content for review
        content_text = self._format_content_for_review(content)

        # Limit content length to avoid token limits
        if len(content_text) > 8000:
            content_text = content_text[:8000] + "\n... [truncated for review]"

        prompt = COHERENCE_CHECK_PROMPT.format(content=content_text)

        try:
            response, input_tokens, output_tokens = self.call_gemini_text_sync(prompt, temperature=TEMPERATURE_VALIDATION)

            # Parse the response
            text = response.strip()
            if text.startswith("```"):
                text = re.sub(r'^```(?:json)?\s*\n', '', text)
                text = re.sub(r'\n```\s*$', '', text)

            result = json.loads(text)
            return {
                "coherence_score": result.get("coherence_score"),
                "issues": result.get("issues", []),
            }, input_tokens, output_tokens
        except Exception as e:
            return {
                "coherence_score": None,
                "issues": [f"Coherence check failed: {str(e)}"],
            }, 0, 0

    def _format_content_for_review(self, content: List[Dict]) -> str:
        """Format extracted content as readable text for coherence review."""
        parts = []
        for item in content:
            item_type = item.get("type")
            if item_type == "heading":
                level = item.get("level", 1)
                parts.append(f"[H{level}] {item.get('text', '')}\n")
            elif item_type == "paragraph":
                parts.append(f"[PARAGRAPH]\n{item.get('text', '')}\n")
            elif item_type == "table":
                parts.append("[TABLE]")
                cells = item.get("cells", [])
                if cells:
                    # Group cells by row
                    rows = {}
                    for cell in cells:
                        row = cell.get("row_start", 0)
                        if row not in rows:
                            rows[row] = []
                        rows[row].append(cell.get("text", ""))
                    for row_num in sorted(rows.keys()):
                        parts.append(f"  Row {row_num}: {' | '.join(rows[row_num])}")
                parts.append("")
            elif item_type == "image":
                desc = item.get("description", "No description")
                parts.append(f"[IMAGE: {desc}]\n")
            elif item_type == "video":
                url = item.get("url", "")
                parts.append(f"[VIDEO: {url}]\n")
            elif item_type == "list":
                list_type = item.get("list_type", "unordered")
                parts.append(f"[LIST ({list_type})]")
                for idx, li in enumerate(item.get("items", []), 1):
                    prefix = f"  {idx}." if list_type == "ordered" else "  -"
                    parts.append(f"{prefix} {li.get('text', '')}")
                    for child in li.get("children", []):
                        parts.append(f"    - {child.get('text', '')}")
                parts.append("")
            elif item_type == "form":
                form_title = item.get("title", "Untitled Form")
                parts.append(f"[FORM: {form_title}]")
                for field in item.get("fields", []):
                    label = field.get("label", "Unknown")
                    field_type = field.get("field_type", "unknown")
                    value = field.get("value", "")
                    parts.append(f"  - {label} ({field_type}): {value or '[empty]'}")
                parts.append("")
            elif item_type == "header_footer":
                subtype = item.get("subtype", "header").upper()
                parts.append(f"[{subtype}] {item.get('text', '')}\n")
            elif item_type == "link":
                text = item.get("text", "")
                url = item.get("url", "")
                parts.append(f"[LINK: {text} -> {url}]\n")
        return "\n".join(parts)

    def parse_json_response(self, response_text: str) -> Tuple[List[Dict], bool, str]:
        """Parse JSON from Gemini response, handling markdown code blocks.

        Returns:
            Tuple of (data, success, error_detail)
            - data: parsed list of content items (empty list on failure)
            - success: True if parsing succeeded
            - error_detail: description of failure (empty string on success)
        """
        # Handle None response (can happen when Gemini returns empty/blocked response)
        if response_text is None:
            return [], False, "Empty response from Gemini (response.text was None)"

        text = response_text.strip()

        # Check for empty response
        if not text:
            return [], False, "Empty response from Gemini"

        # Remove markdown code blocks if present
        if text.startswith("```"):
            text = re.sub(r'^```(?:json)?\s*\n', '', text)
            text = re.sub(r'\n```\s*$', '', text)

        try:
            data = json.loads(text)
            if isinstance(data, list):
                return data, True, ""
            # Valid JSON but not a list
            return [], False, f"Response is {type(data).__name__}, not list. Content: {text[:200]}"
        except json.JSONDecodeError as e:
            # Truncate response for error message
            snippet = text[:200] + "..." if len(text) > 200 else text
            return [], False, f"JSON parse error: {e}. Response: {snippet}"

    def extract_video_links_from_page(self, pdf_path: Path, page_num: int) -> List[Dict]:
        """Extract video links from a PDF page using PyMuPDF."""
        if not ENABLE_VIDEO_DETECTION:
            return []

        doc = fitz.open(str(pdf_path))
        page = doc[page_num]
        links = page.get_links()

        video_links = []
        for link in links:
            uri = link.get("uri", "")
            if not uri:
                continue

            # Check if URL matches any video platform pattern
            is_video = False
            platform = None
            for pattern in VIDEO_PATTERNS:
                if re.search(pattern, uri, re.IGNORECASE):
                    is_video = True
                    if "youtube" in pattern or "youtu.be" in pattern:
                        platform = "youtube"
                    elif "vimeo" in pattern:
                        platform = "vimeo"
                    elif "sharepoint" in pattern or "stream.microsoft" in pattern:
                        platform = "microsoft"
                    break

            if is_video:
                # Get link bounding box
                link_rect = link.get("from")
                bbox = None
                if link_rect:
                    bbox = {
                        "x0": link_rect.x0,
                        "y0": link_rect.y0,
                        "x1": link_rect.x1,
                        "y1": link_rect.y1,
                    }

                video_links.append({
                    "url": uri,
                    "platform": platform,
                    "bbox": bbox,
                })

        doc.close()
        return video_links

    def extract_hyperlinks_from_page(self, pdf_path: Path, page_num: int) -> List[Dict]:
        """Extract all non-video hyperlinks from a PDF page using PyMuPDF.

        Returns a list of dicts with keys: url, text, bbox.
        The 'text' is extracted from the text under the link's bounding box.
        Video links are excluded (handled separately by extract_video_links_from_page).
        """
        doc = fitz.open(str(pdf_path))
        page = doc[page_num]
        links = page.get_links()

        hyperlinks = []
        for link in links:
            uri = link.get("uri", "")
            if not uri:
                continue

            # Skip video links - those are handled by extract_video_links_from_page
            is_video = any(
                re.search(pattern, uri, re.IGNORECASE)
                for pattern in VIDEO_PATTERNS
            )
            if is_video:
                continue

            # Get the display text under the link's bounding box
            link_rect = link.get("from")
            display_text = ""
            bbox = None
            if link_rect:
                display_text = page.get_text("text", clip=link_rect).strip()
                bbox = {
                    "x0": link_rect.x0,
                    "y0": link_rect.y0,
                    "x1": link_rect.x1,
                    "y1": link_rect.y1,
                }

            # Use URL as fallback display text if none found
            if not display_text:
                display_text = uri

            hyperlinks.append({
                "url": uri,
                "text": display_text,
                "bbox": bbox,
            })

        doc.close()
        return hyperlinks

    def extract_images_from_pdf_page(self, pdf_path: Path, page_num: int) -> List[Dict]:
        """Extract embedded images from a PDF page using PyMuPDF.

        When ENABLE_IMAGE_EXTRACTION is True, includes base64 image data.
        When False, still returns image metadata (bbox, format) but no base64 data.
        """
        doc = fitz.open(str(pdf_path))
        page = doc[page_num]
        image_list = page.get_images(full=True)

        extracted_images = []
        for img_index, img in enumerate(image_list):
            xref = img[0]
            try:
                base_image = doc.extract_image(xref)
                image_ext = base_image["ext"]

                # Get bounding box
                image_rects = page.get_image_rects(xref)
                bbox = None
                if image_rects:
                    rect = image_rects[0]
                    bbox = {
                        "x0": rect.x0,
                        "y0": rect.y0,
                        "x1": rect.x1,
                        "y1": rect.y1,
                    }

                image_entry = {
                    "index": img_index,
                    "format": image_ext,
                    "bbox": bbox,
                }

                # Only include base64 data if image extraction is enabled
                if ENABLE_IMAGE_EXTRACTION:
                    image_bytes = base_image["image"]
                    image_entry["base64_data"] = base64.b64encode(image_bytes).decode("utf-8")

                extracted_images.append(image_entry)
            except Exception:
                continue

        doc.close()
        return extracted_images

    def extract_text_with_pymupdf(self, pdf_path: Path, page_num: int) -> str:
        """Extract text from a PDF page using PyMuPDF for cross-validation."""
        doc = fitz.open(str(pdf_path))
        page = doc[page_num]
        text = page.get_text("text")
        doc.close()
        return text

    def _bboxes_overlap(self, bbox1: Optional[Dict], bbox2: Optional[Dict], threshold: float = 0.5) -> bool:
        """Check if two bounding boxes overlap significantly."""
        if not bbox1 or not bbox2:
            return False

        # Calculate intersection
        x_left = max(bbox1["x0"], bbox2["x0"])
        y_top = max(bbox1["y0"], bbox2["y0"])
        x_right = min(bbox1["x1"], bbox2["x1"])
        y_bottom = min(bbox1["y1"], bbox2["y1"])

        if x_right < x_left or y_bottom < y_top:
            return False

        intersection_area = (x_right - x_left) * (y_bottom - y_top)

        # Calculate areas
        bbox1_area = (bbox1["x1"] - bbox1["x0"]) * (bbox1["y1"] - bbox1["y0"])
        bbox2_area = (bbox2["x1"] - bbox2["x0"]) * (bbox2["y1"] - bbox2["y0"])

        # Check if intersection is significant relative to either bbox
        min_area = min(bbox1_area, bbox2_area)
        if min_area == 0:
            return False

        overlap_ratio = intersection_area / min_area
        return overlap_ratio >= threshold

    def match_images_to_descriptions(
        self, gemini_images: List[Dict], pymupdf_images: List[Dict],
        video_links: List[Dict], page_height: float
    ) -> Tuple[List[Dict], List[Dict]]:
        """
        Match Gemini image descriptions to PyMuPDF extracted images by position.
        Also identifies which images are actually video thumbnails.

        Returns:
            Tuple of (matched_images, video_items)
        """
        matched_images = []
        video_items = []

        # First, identify images that are video thumbnails by checking bbox overlap
        video_image_indices = set()
        for video_link in video_links:
            video_bbox = video_link.get("bbox")
            if not video_bbox:
                continue

            # Find image that overlaps with this video link
            for i, pymupdf_img in enumerate(pymupdf_images):
                if self._bboxes_overlap(video_bbox, pymupdf_img.get("bbox")):
                    video_image_indices.add(i)

                    # Create video item with thumbnail
                    video_item = {
                        "type": "video",
                        "url": video_link["url"],
                        "platform": video_link["platform"],
                        "thumbnail_format": pymupdf_img["format"],
                        "bbox": video_bbox,
                        "description": None,  # Will be filled from Gemini if available
                    }
                    if "base64_data" in pymupdf_img:
                        video_item["thumbnail_base64"] = pymupdf_img["base64_data"]
                    video_items.append(video_item)
                    break
            else:
                # No matching image found, still create video item without thumbnail
                video_items.append({
                    "type": "video",
                    "url": video_link["url"],
                    "platform": video_link["platform"],
                    "bbox": video_bbox,
                    "description": None,
                })

        # Remove video thumbnails from the image list
        remaining_images = [
            img for i, img in enumerate(pymupdf_images)
            if i not in video_image_indices
        ]

        if not remaining_images and not gemini_images:
            return [], video_items

        # Map position strings to vertical ranges
        position_ranges = {
            "top": (0, page_height / 3),
            "middle": (page_height / 3, 2 * page_height / 3),
            "bottom": (2 * page_height / 3, page_height),
        }

        for gemini_img in gemini_images:
            position = gemini_img.get("position", "middle-center")
            vertical_pos = position.split("-")[0] if "-" in position else position

            # Check if this Gemini description matches a video (by position)
            matched_video = False
            for video_item in video_items:
                if video_item.get("bbox"):
                    video_y = (video_item["bbox"]["y0"] + video_item["bbox"]["y1"]) / 2
                    v_range = position_ranges.get(vertical_pos, position_ranges["middle"])
                    if v_range[0] <= video_y <= v_range[1]:
                        # This description likely refers to the video
                        video_item["description"] = gemini_img.get("description", "")
                        matched_video = True
                        break

            if matched_video:
                continue

            # Find best matching PyMuPDF image by vertical position
            best_match = None
            best_distance = float("inf")

            v_range = position_ranges.get(vertical_pos, position_ranges["middle"])
            target_y = (v_range[0] + v_range[1]) / 2

            for pymupdf_img in remaining_images:
                if pymupdf_img.get("bbox"):
                    img_y = (pymupdf_img["bbox"]["y0"] + pymupdf_img["bbox"]["y1"]) / 2
                    distance = abs(img_y - target_y)
                    if distance < best_distance:
                        best_distance = distance
                        best_match = pymupdf_img

            # Combine Gemini description with PyMuPDF data
            combined = {
                "type": "image",
                "description": gemini_img.get("description", ""),
                "caption": gemini_img.get("caption"),
                "position": position,
            }

            if best_match:
                if "base64_data" in best_match:
                    combined["base64_data"] = best_match["base64_data"]
                combined["format"] = best_match["format"]
                combined["bbox"] = best_match["bbox"]
                # Remove used image to prevent double-matching
                remaining_images.remove(best_match)

            matched_images.append(combined)

        # Add any remaining PyMuPDF images that weren't matched
        for remaining in remaining_images:
            unmatched_image = {
                "type": "image",
                "description": "Unidentified image",
                "format": remaining["format"],
                "bbox": remaining["bbox"],
            }
            if "base64_data" in remaining:
                unmatched_image["base64_data"] = remaining["base64_data"]
            matched_images.append(unmatched_image)

        return matched_images, video_items

    def process_single_page(
        self, pdf_path: Path, page_num: int
    ) -> Dict:
        """Process a single page with just-in-time rendering and extraction."""
        pdf_name = pdf_path.name
        print(f"  [{pdf_name}] Page {page_num + 1}: Starting...")

        result = {
            "page_number": page_num + 1,  # 1-indexed for output
            "content": [],
            "validation": {
                "coherence_score": None,
                "coherence_issues": [],
            },
            "error": None,
            "token_usage": {"input_tokens": 0, "output_tokens": 0},
        }

        try:
            # Render page to PNG
            print(f"  [{pdf_name}] Page {page_num + 1}: Rendering PNG...")
            image_bytes = _render_single_page((str(pdf_path), page_num))
            print(f"  [{pdf_name}] Page {page_num + 1}: Rendered {len(image_bytes):,} bytes")

            # Extraction with structured output schema (guarantees valid JSON)
            # Try Flash first, fall back to Gemini 3 on exception or invalid JSON
            primary_content = []
            primary_valid = False
            flash_error = None

            try:
                print(f"  [{pdf_name}] Page {page_num + 1}: Calling Gemini for extraction...")
                primary_response, input_tokens, output_tokens = self.call_gemini_for_extraction(image_bytes)
                print(f"  [{pdf_name}] Page {page_num + 1}: Gemini returned ({input_tokens} in, {output_tokens} out tokens)")
                result["token_usage"]["input_tokens"] += input_tokens
                result["token_usage"]["output_tokens"] += output_tokens
                primary_content, primary_valid, parse_error = self.parse_json_response(primary_response)
                if not primary_valid:
                    flash_error = f"[{GEMINI_MODEL}] Invalid JSON: {parse_error}"
            except Exception as e:
                flash_error = f"[{GEMINI_MODEL}] {type(e).__name__}: {e}"
                print(f"  [{pdf_name}] Page {page_num + 1}: Gemini error: {flash_error}")

            if not primary_valid:
                result["error"] = flash_error or "Unknown extraction error"
                print(f"  [{pdf_name}] Page {page_num + 1}: Failed - {result['error']}")
                return result

            # Separate images from other content
            gemini_images = [item for item in primary_content if item.get("type") == "image"]
            other_content = [item for item in primary_content if item.get("type") != "image"]

            # Extract actual images from PDF with PyMuPDF
            pymupdf_images = self.extract_images_from_pdf_page(pdf_path, page_num)

            # Extract video links from PDF
            video_links = self.extract_video_links_from_page(pdf_path, page_num)

            # Extract hyperlinks from PDF using PyMuPDF (non-video links)
            pymupdf_hyperlinks = self.extract_hyperlinks_from_page(pdf_path, page_num)

            # Get page height for position matching
            doc = fitz.open(str(pdf_path))
            page_height = doc[page_num].rect.height
            doc.close()

            # Match and merge image data, separating out videos
            merged_images, video_items = self.match_images_to_descriptions(
                gemini_images, pymupdf_images, video_links, page_height
            )

            # Build link items from PyMuPDF hyperlinks
            link_items = [
                {"type": "link", "text": h["text"], "url": h["url"]}
                for h in pymupdf_hyperlinks
            ]

            # Combine all content: text content + images + videos + links
            combined_content = other_content + merged_images + video_items + link_items

            # Post-process content (deduplication, character normalization)
            result["content"], post_process_stats = self._post_process_content(combined_content)
            result["validation"]["post_processing"] = post_process_stats

            # Coherence check (LLM-based quality assessment)
            if ENABLE_COHERENCE_CHECK:
                print(f"  [{pdf_name}] Page {page_num + 1}: Running coherence check...")
                coherence_result, coh_input_tokens, coh_output_tokens = self.check_coherence(result["content"])
                print(f"  [{pdf_name}] Page {page_num + 1}: Coherence check done (score: {coherence_result.get('coherence_score')})")
                result["token_usage"]["input_tokens"] += coh_input_tokens
                result["token_usage"]["output_tokens"] += coh_output_tokens
                result["validation"]["coherence_score"] = coherence_result.get("coherence_score")
                result["validation"]["coherence_issues"] = coherence_result.get("issues", [])

            print(f"  [{pdf_name}] Page {page_num + 1}: Complete")

        except Exception as e:
            result["error"] = str(e)
            print(f"  [{pdf_name}] Page {page_num + 1}: Exception - {e}")

        return result

    def _flatten_to_text(self, content: List[Dict]) -> str:
        """Flatten extracted content to plain text for comparison."""
        texts = []
        for item in content:
            item_type = item.get("type")
            if item_type == "paragraph":
                texts.append(item.get("text", ""))
            elif item_type == "table":
                for cell in item.get("cells", []):
                    texts.append(cell.get("text", ""))
            elif item_type == "list":
                for li in item.get("items", []):
                    texts.append(li.get("text", ""))
                    for child in li.get("children", []):
                        texts.append(child.get("text", ""))
            elif item_type == "header_footer":
                texts.append(item.get("text", ""))
            elif item_type == "link":
                texts.append(item.get("text", ""))
        return " ".join(texts)

    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts using SequenceMatcher."""
        # Normalize whitespace and case
        t1 = " ".join(text1.split()).lower()
        t2 = " ".join(text2.split()).lower()

        if not t1 and not t2:
            return 1.0
        if not t1 or not t2:
            return 0.0

        return SequenceMatcher(None, t1, t2).ratio()

    def _compare_extractions(self, primary: List[Dict], secondary: List[Dict]) -> float:
        """Compare two extractions for consistency."""
        primary_text = self._flatten_to_text(primary)
        secondary_text = self._flatten_to_text(secondary)
        return self._calculate_text_similarity(primary_text, secondary_text)

    def _normalize_ocr_characters(self, text: str) -> str:
        """
        Normalize common OCR errors and character artifacts.

        Fixes:
        - Doubled trademark symbols (™™ → ™)
        - Doubled registered symbols (®® → ®)
        - Doubled copyright symbols (©© → ©)
        - Common character confusions in specific contexts
        """
        if not text:
            return text

        # Fix doubled special symbols
        replacements = [
            ('™™', '™'),
            ('®®', '®'),
            ('©©', '©'),
            ('™ ™', '™'),  # With space between
            ('® ®', '®'),
            ('© ©', '©'),
            ('™™™', '™'),  # Triple
            ('®®®', '®'),
            ('©©©', '©'),
        ]

        result = text
        for old, new in replacements:
            result = result.replace(old, new)

        return result

    def _deduplicate_consecutive_paragraphs(self, content: List[Dict], similarity_threshold: float = 0.95) -> List[Dict]:
        """
        Remove consecutive duplicate or near-duplicate paragraphs.

        This addresses the issue where the same paragraph is extracted multiple times
        in a row (e.g., from track changes or reading order issues).

        Args:
            content: List of content items
            similarity_threshold: How similar two paragraphs must be to be considered duplicates (0-1)

        Returns:
            Deduplicated content list
        """
        if not content:
            return content

        result = []
        prev_text = None
        prev_type = None
        duplicate_count = 0

        for item in content:
            item_type = item.get("type")

            # Only deduplicate paragraphs and headings
            if item_type in ("paragraph", "heading"):
                current_text = item.get("text", "")

                # Check if this is a duplicate of the previous item
                is_duplicate = False
                if prev_type == item_type and prev_text and current_text:
                    # Normalize for comparison
                    prev_normalized = " ".join(prev_text.split()).lower()
                    curr_normalized = " ".join(current_text.split()).lower()

                    # Exact match or very high similarity
                    if prev_normalized == curr_normalized:
                        is_duplicate = True
                    elif len(prev_normalized) > 20 and len(curr_normalized) > 20:
                        # Only check similarity for longer texts to avoid false positives
                        similarity = self._calculate_text_similarity(prev_text, current_text)
                        if similarity >= similarity_threshold:
                            is_duplicate = True

                if is_duplicate:
                    duplicate_count += 1
                    continue  # Skip this duplicate

                prev_text = current_text
                prev_type = item_type
            else:
                # Non-text items reset the duplicate tracking
                prev_text = None
                prev_type = None

            result.append(item)

        if duplicate_count > 0:
            # Log for diagnostics (could be captured in validation)
            pass

        return result

    def _post_process_content(self, content: List[Dict]) -> Tuple[List[Dict], Dict]:
        """
        Apply all post-processing steps to extracted content.

        Returns:
            Tuple of (processed_content, post_processing_stats)
        """
        stats = {
            "duplicates_removed": 0,
            "characters_normalized": 0,
        }

        if not content:
            return content, stats

        # Count items before deduplication
        original_count = len(content)

        # Step 1: Normalize OCR characters in all text fields
        for item in content:
            item_type = item.get("type")

            if item_type in ("paragraph", "heading"):
                original_text = item.get("text", "")
                normalized_text = self._normalize_ocr_characters(original_text)
                if normalized_text != original_text:
                    item["text"] = normalized_text
                    stats["characters_normalized"] += 1

            elif item_type == "table":
                for cell in item.get("cells", []):
                    original_text = cell.get("text", "")
                    normalized_text = self._normalize_ocr_characters(original_text)
                    if normalized_text != original_text:
                        cell["text"] = normalized_text
                        stats["characters_normalized"] += 1

            elif item_type == "image":
                for field in ["description", "caption"]:
                    if field in item and item[field]:
                        original_text = item[field]
                        normalized_text = self._normalize_ocr_characters(original_text)
                        if normalized_text != original_text:
                            item[field] = normalized_text
                            stats["characters_normalized"] += 1

            elif item_type == "list":
                for li in item.get("items", []):
                    original_text = li.get("text", "")
                    normalized_text = self._normalize_ocr_characters(original_text)
                    if normalized_text != original_text:
                        li["text"] = normalized_text
                        stats["characters_normalized"] += 1
                    for child in li.get("children", []):
                        original_text = child.get("text", "")
                        normalized_text = self._normalize_ocr_characters(original_text)
                        if normalized_text != original_text:
                            child["text"] = normalized_text
                            stats["characters_normalized"] += 1

            elif item_type == "header_footer":
                original_text = item.get("text", "")
                normalized_text = self._normalize_ocr_characters(original_text)
                if normalized_text != original_text:
                    item["text"] = normalized_text
                    stats["characters_normalized"] += 1

            elif item_type == "link":
                original_text = item.get("text", "")
                normalized_text = self._normalize_ocr_characters(original_text)
                if normalized_text != original_text:
                    item["text"] = normalized_text
                    stats["characters_normalized"] += 1

        # Step 2: Deduplicate consecutive paragraphs
        content = self._deduplicate_consecutive_paragraphs(content)
        stats["duplicates_removed"] = original_count - len(content)

        return content, stats

    def _calculate_pdf_metrics(self, pages: List[Dict]) -> Dict:
        """Calculate aggregate quality metrics for a PDF.

        Confidence scoring now uses:
        - Coherence score (1-10 from LLM) - primary metric
        - Re-extraction consistency - secondary metric
        - PyMuPDF similarity is only kept for diagnostic purposes
        """
        total_pages = len(pages)
        pages_with_errors = sum(1 for p in pages if p.get("error"))

        # Collect scores for averaging
        coherence_scores = [
            p["validation"].get("coherence_score")
            for p in pages
            if p["validation"].get("coherence_score") is not None
        ]

        # Classify pages by confidence based on coherence score
        high_confidence = 0
        medium_confidence = 0
        low_confidence = 0

        for page in pages:
            if page.get("error"):
                continue

            # Get coherence score (1-10 scale)
            coherence = page["validation"].get("coherence_score")
            if coherence is None:
                coherence = 8  # Default assumption

            if coherence >= 9:
                high_confidence += 1
            elif coherence >= 7:
                medium_confidence += 1
            else:
                low_confidence += 1

        return {
            "pages_successful": total_pages - pages_with_errors,
            "pages_failed": pages_with_errors,
            "pages_high_confidence": high_confidence,
            "pages_medium_confidence": medium_confidence,
            "pages_low_confidence": low_confidence,
            "avg_coherence_score": round(sum(coherence_scores) / len(coherence_scores), 2) if coherence_scores else None,
        }

    def get_completed_pdfs(self) -> set:
        """Get set of PDF IDs that have already been processed."""
        completed = set()
        if OUTPUT_FOLDER.exists():
            for json_file in OUTPUT_FOLDER.glob("*.json"):
                if not json_file.name.startswith("_"):
                    completed.add(json_file.stem)
        return completed

    def _get_pdf_files(self) -> List[Tuple[str, Path]]:
        """Get list of (doc_id, pdf_path) tuples to process.

        Reads source.pdf from data/{doc_id}/ folders. If a test file list
        is configured, only returns PDFs matching that list.
        """
        # Parse test file list for filtering
        target_ids = []
        if TEST_FILE_LIST:
            target_ids = parse_test_file_list(TEST_FILE_LIST)
            if target_ids:
                print(f"Filtering to {len(target_ids)} documents from test file list")

        pdf_files = []
        if target_ids:
            # Only look for specific document IDs
            for doc_id in target_ids:
                pdf_path = DATA_FOLDER / doc_id / "source.pdf"
                if pdf_path.exists():
                    pdf_files.append((doc_id, pdf_path))
                else:
                    # Try partial match (directory name may differ slightly)
                    matches = list(DATA_FOLDER.glob(f"{doc_id}*/source.pdf"))
                    if matches:
                        matched_id = matches[0].parent.name
                        pdf_files.append((matched_id, matches[0]))
                    else:
                        print(f"  Warning: PDF not found for '{doc_id}'")
        else:
            # Process all PDFs in data folder
            for source_pdf in sorted(DATA_FOLDER.glob("*/source.pdf")):
                doc_id = source_pdf.parent.name
                pdf_files.append((doc_id, source_pdf))

        return pdf_files

    def process_all_pdfs(self):
        """Process all PDFs with flat page-level concurrency using multiprocessing.Pool."""
        # Create output directories
        OUTPUT_FOLDER.mkdir(exist_ok=True)
        REPORTS_FOLDER.mkdir(exist_ok=True)

        # Get list of PDFs (filtered by test file list if configured)
        pdf_files = self._get_pdf_files()
        self.stats["total_pdfs"] = len(pdf_files)

        # Check for already completed PDFs (resume capability)
        completed = self.get_completed_pdfs()
        pending_pdfs = [(doc_id, p) for doc_id, p in pdf_files if doc_id not in completed]

        print(f"Found {len(pdf_files)} PDFs total")
        print(f"Already completed: {len(completed)}")
        print(f"Pending: {len(pending_pdfs)}")

        # Collect all pages to process across all PDFs
        all_page_tasks = []
        pdf_info = {}  # Store PDF metadata for building results later
        for doc_id, pdf_path in pending_pdfs:
            try:
                doc = pdfium.PdfDocument(str(pdf_path))
                page_count = len(doc)
                doc.close()
            except Exception as e:
                print(f"  Warning: Skipping '{doc_id}' - failed to open PDF: {e}")
                continue
            pdf_info[doc_id] = {
                "pdf_path": pdf_path,
                "pdf_filename": pdf_path.name,
                "total_pages": page_count,
            }
            for page_num in range(page_count):
                all_page_tasks.append((str(pdf_path), page_num, doc_id))

        print(f"Processing {len(all_page_tasks)} pages with {MAX_WORKERS} workers")
        print()

        # Process all pages using multiprocessing.Pool
        results_by_pdf = {}
        all_failed_pages = []

        with Pool(processes=MAX_WORKERS) as pool:
            for doc_id, page_num, page_result in tqdm(
                pool.imap_unordered(_process_page_worker, all_page_tasks),
                total=len(all_page_tasks),
                desc="Processing pages",
            ):
                if doc_id not in results_by_pdf:
                    results_by_pdf[doc_id] = {}
                results_by_pdf[doc_id][page_num] = page_result

                # Track failed pages for retry
                if page_result.get("error"):
                    pdf_path_str = str(pdf_info[doc_id]["pdf_path"])
                    all_failed_pages.append((pdf_path_str, page_num, doc_id))

                # Update token stats
                token_usage = page_result.get("token_usage", {})
                self.stats["total_input_tokens"] += token_usage.get("input_tokens", 0)
                self.stats["total_output_tokens"] += token_usage.get("output_tokens", 0)

        # Retry failed pages at end of run
        if all_failed_pages:
            print(f"\n{'='*60}")
            print(f"RETRYING {len(all_failed_pages)} FAILED PAGES")
            print(f"{'='*60}")
            self._retry_failed_pages(all_failed_pages, results_by_pdf)

        # Build final results, calculate metrics, and save JSON files
        all_results = []
        for pdf_id, info in pdf_info.items():
            page_results_dict = results_by_pdf.get(pdf_id, {})
            # Convert dict to sorted list by page number
            pages = [page_results_dict[i] for i in sorted(page_results_dict.keys())]

            result = {
                "pdf_id": pdf_id,
                "source_path": str(info["pdf_path"]),
                "total_pages": info["total_pages"],
                "extraction_timestamp": datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z"),
                "pages": pages,
            }

            # Calculate quality metrics
            result["quality_metrics"] = self._calculate_pdf_metrics(pages)

            # Calculate token usage for this PDF
            pdf_input_tokens = sum(p.get("token_usage", {}).get("input_tokens", 0) for p in pages)
            pdf_output_tokens = sum(p.get("token_usage", {}).get("output_tokens", 0) for p in pages)
            result["token_usage"] = {
                "input_tokens": pdf_input_tokens,
                "output_tokens": pdf_output_tokens,
            }

            # Save individual PDF result
            output_path = OUTPUT_FOLDER / f"{pdf_id}.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            # Generate per-document HTML immediately after JSON
            html_path = OUTPUT_FOLDER / f"{pdf_id}.html"
            generate_document_html(result, html_path)

            all_results.append(result)

            # Update aggregate stats
            metrics = result["quality_metrics"]
            self.stats["total_pages"] += info["total_pages"]
            self.stats["successful_extractions"] += metrics.get("pages_successful", 0)
            self.stats["failed_extractions"] += metrics.get("pages_failed", 0)
            self.stats["pages_by_confidence"]["high"] += metrics.get("pages_high_confidence", 0)
            self.stats["pages_by_confidence"]["medium"] += metrics.get("pages_medium_confidence", 0)
            self.stats["pages_by_confidence"]["low"] += metrics.get("pages_low_confidence", 0)

        # Generate summary report
        self._generate_summary_report(all_results)

        return all_results

    def _retry_failed_pages(self, failed_pages: List[Tuple[str, int, str]], results_by_pdf: Dict):
        """Retry failed pages using multiprocessing.Pool and update results dict.

        Args:
            failed_pages: List of (pdf_path_str, page_num, doc_id) tuples to retry
            results_by_pdf: Dict mapping pdf_id -> {page_num: page_result} (modified in place)
        """
        if not failed_pages:
            return

        print(f"Retrying {len(failed_pages)} pages...")
        successful_retries = 0
        still_failed = 0

        with Pool(processes=MAX_WORKERS) as pool:
            for doc_id, page_num, retry_result in tqdm(
                pool.imap_unordered(_process_page_worker, failed_pages),
                total=len(failed_pages),
                desc="Retrying pages",
            ):
                # Update token stats from retry
                token_usage = retry_result.get("token_usage", {})
                self.stats["total_input_tokens"] += token_usage.get("input_tokens", 0)
                self.stats["total_output_tokens"] += token_usage.get("output_tokens", 0)

                if retry_result.get("error"):
                    still_failed += 1
                else:
                    successful_retries += 1

                # Update the result in place
                if doc_id in results_by_pdf:
                    results_by_pdf[doc_id][page_num] = retry_result

        print(f"Retry complete: {successful_retries} succeeded, {still_failed} still failed")

    def _generate_summary_report(self, results: List[Dict]):
        """Generate aggregate summary report."""
        # Collect all metrics
        all_coherence_scores = []
        pdfs_by_status = {
            "fully_successful": [],
            "partial_issues": [],
            "failed": [],
        }

        for result in results:
            pdf_id = result["pdf_id"]
            metrics = result.get("quality_metrics", {})

            if metrics.get("pages_failed", 0) == 0 and metrics.get("pages_low_confidence", 0) == 0:
                pdfs_by_status["fully_successful"].append(pdf_id)
            elif metrics.get("pages_failed", 0) == result.get("total_pages", 1):
                pdfs_by_status["failed"].append(pdf_id)
            else:
                pdfs_by_status["partial_issues"].append(pdf_id)

            # Collect page-level scores
            for page in result.get("pages", []):
                val = page.get("validation", {})
                if val.get("coherence_score") is not None:
                    all_coherence_scores.append(val["coherence_score"])

        # Calculate success rate
        total_pages = self.stats["total_pages"]
        success_rate = self.stats["successful_extractions"] / total_pages if total_pages > 0 else 0

        summary = {
            "generated_at": datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z"),
            "total_pdfs": self.stats["total_pdfs"],
            "pdfs_processed": len(results),
            "total_pages_processed": total_pages,
            "successful_extractions": self.stats["successful_extractions"],
            "failed_extractions": self.stats["failed_extractions"],
            "success_rate": round(success_rate, 3),
            "quality_breakdown": {
                "high_confidence": self.stats["pages_by_confidence"]["high"],
                "medium_confidence": self.stats["pages_by_confidence"]["medium"],
                "low_confidence": self.stats["pages_by_confidence"]["low"],
            },
            "avg_coherence_score": round(sum(all_coherence_scores) / len(all_coherence_scores), 2) if all_coherence_scores else None,
            "pdfs_by_status": pdfs_by_status,
            "token_usage": {
                "total_input_tokens": self.stats["total_input_tokens"],
                "total_output_tokens": self.stats["total_output_tokens"],
            },
        }

        # Save summary JSON
        summary_path = REPORTS_FOLDER / "summary.json"
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        # Generate HTML report
        self._generate_html_report(summary, results)

        print("\n" + "=" * 60)
        print("EXTRACTION COMPLETE")
        print("=" * 60)
        print(f"Total PDFs processed: {len(results)}")
        print(f"Total pages: {total_pages}")
        print(f"Success rate: {success_rate:.1%}")
        print(f"High confidence: {summary['quality_breakdown']['high_confidence']}")
        print(f"Medium confidence: {summary['quality_breakdown']['medium_confidence']}")
        print(f"Low confidence: {summary['quality_breakdown']['low_confidence']}")
        print()
        print(f"Token usage:")
        print(f"  Input tokens:  {self.stats['total_input_tokens']:,}")
        print(f"  Output tokens: {self.stats['total_output_tokens']:,}")
        print(f"  Total tokens:  {self.stats['total_input_tokens'] + self.stats['total_output_tokens']:,}")
        print(f"\nReports saved to: {REPORTS_FOLDER}")

    def _generate_html_report(self, summary: Dict, results: List[Dict]):
        """Generate human-readable HTML quality report."""
        # Calculate percentage safely
        total_pages = summary['total_pages_processed'] or 1
        high_pct = summary['quality_breakdown']['high_confidence'] / total_pages * 100
        med_pct = summary['quality_breakdown']['medium_confidence'] / total_pages * 100
        low_pct = summary['quality_breakdown']['low_confidence'] / total_pages * 100

        # Collect problem pages for detailed reporting
        failed_pages = []
        low_confidence_pages = []
        for result in results:
            pdf_id = result['pdf_id']
            pdf_filename = result.get('source_path', '')
            for page in result.get('pages', []):
                page_num = page.get('page_number', '?')
                # Check for extraction errors
                if page.get('error'):
                    failed_pages.append({
                        'pdf_id': pdf_id,
                        'pdf_filename': pdf_filename,
                        'page': page_num,
                        'error': page['error']
                    })
                # Check for low confidence (coherence < 7)
                coherence = page.get('validation', {}).get('coherence_score')
                if coherence is not None and coherence < 7:
                    issues = page.get('validation', {}).get('coherence_issues', [])
                    low_confidence_pages.append({
                        'pdf_id': pdf_id,
                        'pdf_filename': pdf_filename,
                        'page': page_num,
                        'score': coherence,
                        'issues': issues
                    })

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>PDF Extraction Quality Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .summary {{ background: #f5f5f5; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .metric {{ display: inline-block; margin-right: 30px; margin-bottom: 10px; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #2196F3; }}
        .metric-label {{ color: #666; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background: #f9f9f9; }}
        .status-success {{ color: #4CAF50; }}
        .status-partial {{ color: #FF9800; }}
        .status-failed {{ color: #F44336; }}
        .score-high {{ color: #4CAF50; font-weight: bold; }}
        .score-medium {{ color: #FF9800; }}
        .score-low {{ color: #F44336; }}
        .note {{ background: #fff3cd; padding: 10px; border-radius: 4px; margin: 10px 0; }}
        .error-section {{ background: #ffebee; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #F44336; }}
        .warning-section {{ background: #fff8e1; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #FF9800; }}
        .error-text {{ color: #c62828; font-family: monospace; font-size: 0.9em; word-break: break-all; }}
        a {{ color: #1976D2; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>PDF Extraction Quality Report</h1>
    <p>Generated: {summary['generated_at']}</p>

    <div class="summary">
        <div class="metric">
            <div class="metric-value">{summary['pdfs_processed']}</div>
            <div class="metric-label">PDFs Processed</div>
        </div>
        <div class="metric">
            <div class="metric-value">{summary['total_pages_processed']}</div>
            <div class="metric-label">Total Pages</div>
        </div>
        <div class="metric">
            <div class="metric-value">{summary['success_rate']:.1%}</div>
            <div class="metric-label">Success Rate</div>
        </div>
        <div class="metric">
            <div class="metric-value">{summary.get('avg_coherence_score', 'N/A')}/10</div>
            <div class="metric-label">Avg Coherence Score</div>
        </div>
    </div>

    <div class="note">
        <strong>Metrics Explained:</strong>
        <ul style="margin: 5px 0;">
            <li><strong>Success Rate:</strong> Percentage of pages where extraction completed without errors (API failures, parsing issues)</li>
            <li><strong>Confidence:</strong> Based on coherence score (1-10) from LLM quality assessment. High = 9-10, Medium = 7-8, Low = &lt;7</li>
        </ul>
    </div>

    <h2>Quality Breakdown</h2>
    <table>
        <tr>
            <th>Confidence Level</th>
            <th>Page Count</th>
            <th>Percentage</th>
        </tr>
        <tr>
            <td class="score-high">High (9-10)</td>
            <td>{summary['quality_breakdown']['high_confidence']}</td>
            <td>{high_pct:.1f}%</td>
        </tr>
        <tr>
            <td class="score-medium">Medium (7-8)</td>
            <td>{summary['quality_breakdown']['medium_confidence']}</td>
            <td>{med_pct:.1f}%</td>
        </tr>
        <tr>
            <td class="score-low">Low (&lt;7)</td>
            <td>{summary['quality_breakdown']['low_confidence']}</td>
            <td>{low_pct:.1f}%</td>
        </tr>
    </table>
"""

        # Add Failed Pages section if there are any
        if failed_pages:
            html += f"""
    <div class="error-section">
        <h2 style="margin-top: 0; color: #c62828;">Failed Pages ({len(failed_pages)})</h2>
        <p>These pages had extraction errors and could not be processed:</p>
        <table>
            <tr>
                <th>PDF</th>
                <th>Page</th>
                <th>Error</th>
            </tr>
"""
            for fp in failed_pages:
                error_escaped = fp['error'].replace('<', '&lt;').replace('>', '&gt;')
                html += f"""            <tr>
                <td>{fp['pdf_id']}</td>
                <td>{fp['page']}</td>
                <td class="error-text">{error_escaped}</td>
            </tr>
"""
            html += """        </table>
    </div>
"""

        # Add Low Confidence Pages section if there are any
        if low_confidence_pages:
            html += f"""
    <div class="warning-section">
        <h2 style="margin-top: 0; color: #e65100;">Low Confidence Pages ({len(low_confidence_pages)})</h2>
        <p>These pages have coherence scores below 7 and may need manual review:</p>
        <table>
            <tr>
                <th>PDF</th>
                <th>Page</th>
                <th>Score</th>
                <th>Issues</th>
            </tr>
"""
            for lcp in low_confidence_pages:
                # Format issues as a bullet list or "None reported"
                issues_html = ""
                if lcp['issues']:
                    issues_escaped = [issue.replace('<', '&lt;').replace('>', '&gt;') for issue in lcp['issues']]
                    issues_html = "<ul style='margin: 0; padding-left: 20px;'>" + "".join(f"<li>{issue}</li>" for issue in issues_escaped) + "</ul>"
                else:
                    issues_html = "<em>None reported</em>"
                html += f"""            <tr>
                <td>{lcp['pdf_id']}</td>
                <td>{lcp['page']}</td>
                <td class="score-low">{lcp['score']}</td>
                <td>{issues_html}</td>
            </tr>
"""
            html += """        </table>
    </div>
"""

        html += f"""
    <h2>PDF Status Summary</h2>
    <table>
        <tr>
            <th>Status</th>
            <th>Count</th>
            <th>PDF IDs</th>
        </tr>
        <tr>
            <td class="status-success">Fully Successful</td>
            <td>{len(summary['pdfs_by_status']['fully_successful'])}</td>
            <td>{', '.join(summary['pdfs_by_status']['fully_successful'][:5])}{'...' if len(summary['pdfs_by_status']['fully_successful']) > 5 else ''}</td>
        </tr>
        <tr>
            <td class="status-partial">Partial Issues</td>
            <td>{len(summary['pdfs_by_status']['partial_issues'])}</td>
            <td>{', '.join(summary['pdfs_by_status']['partial_issues'][:5])}{'...' if len(summary['pdfs_by_status']['partial_issues']) > 5 else ''}</td>
        </tr>
        <tr>
            <td class="status-failed">Failed</td>
            <td>{len(summary['pdfs_by_status']['failed'])}</td>
            <td>{', '.join(summary['pdfs_by_status']['failed'][:5])}{'...' if len(summary['pdfs_by_status']['failed']) > 5 else ''}</td>
        </tr>
    </table>

    <h2>Individual PDF Results</h2>
    <table>
        <tr>
            <th>PDF ID</th>
            <th>Pages</th>
            <th>Successful</th>
            <th>Avg Coherence</th>
            <th>Confidence</th>
        </tr>
"""

        for result in results:
            metrics = result.get("quality_metrics", {})
            coherence = metrics.get('avg_coherence_score')

            # Calculate confidence class based on coherence score
            if coherence is not None:
                if coherence >= 9:
                    conf_class = "score-high"
                    conf_label = "High"
                elif coherence >= 7:
                    conf_class = "score-medium"
                    conf_label = "Medium"
                else:
                    conf_class = "score-low"
                    conf_label = "Low"
            else:
                conf_class = ""
                conf_label = "N/A"

            html += f"""        <tr>
            <td>{result['pdf_id']}</td>
            <td>{result['total_pages']}</td>
            <td>{metrics.get('pages_successful', 0)}</td>
            <td>{coherence if coherence is not None else 'N/A'}</td>
            <td class="{conf_class}">{conf_label}</td>
        </tr>
"""

        html += """    </table>
</body>
</html>"""

        html_path = REPORTS_FOLDER / "quality_report.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)


def main():
    """Main entry point."""
    print("=" * 60)
    print("PDF Structured JSON Extraction Tool")
    print("=" * 60)
    print()
    print(f"Data Folder: {DATA_FOLDER}")
    print(f"Output Folder: {OUTPUT_FOLDER}")
    print(f"Max Workers: {MAX_WORKERS}")
    print()

    extractor = PDFExtractor()
    extractor.process_all_pdfs()


if __name__ == "__main__":
    main()
