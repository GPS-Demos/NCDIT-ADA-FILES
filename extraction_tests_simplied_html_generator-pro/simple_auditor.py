#!/usr/bin/env python3
"""Audit HTML completeness against source PDFs using Gemini.

For each folder in the input directory, compares source.pdf against the
generated .html file and checks whether all content from the PDF made it
into the HTML. Produces a per-document audit report with annotations.

Usage:
    python simple_auditor.py json_to_html_to_auditor/
    python simple_auditor.py json_to_html_to_auditor/ --concurrency 10
    python simple_auditor.py json_to_html_to_auditor/ -o audit_results/
"""

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import backoff
from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ID = "playground-439016"
REGION = "global"
GEMINI_MODEL = "gemini-3.1-pro-preview"
MAX_OUTPUT_TOKENS = 65500
TEMPERATURE = 1.0
TOP_P = 0.95
TOP_K = 40
DEFAULT_CONCURRENCY = 5

# ---------------------------------------------------------------------------
# Gemini client
# ---------------------------------------------------------------------------

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=REGION,
)


def get_safety_settings():
    return [
        types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
        types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
        types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
        types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
    ]


# ---------------------------------------------------------------------------
# Audit prompt
# ---------------------------------------------------------------------------

AUDIT_PROMPT = """\
You are a document completeness auditor. You have been given:
1. A source PDF document (the ground truth)
2. An HTML rendering of that document

Your task is to carefully compare the HTML against the PDF and determine whether
ALL content from the PDF has been faithfully represented in the HTML.

## What to check

Check for completeness across ALL of these content types:
- **Text**: All paragraphs, headings, and body text must be present. Check for missing sentences, truncated paragraphs, or dropped sections.
- **Tables**: All tables must be present with correct structure (rows, columns, headers). Check for missing rows, missing columns, or garbled cell content.
- **Lists**: All bulleted and numbered lists must be present with all items.
- **Images**: All meaningful (non-decorative) images should be referenced or described.
- **Links**: All hyperlinks should be present with correct text.
- **Forms**: All form fields should be represented.
- **Headers/Footers**: Running headers and footers may be intentionally deduplicated — this is acceptable.
- **Page numbers**: Page numbers may be omitted — this is acceptable.

## What is acceptable
- Minor formatting differences (fonts, colors, spacing) are acceptable.
- Decorative images being omitted or marked as decorative is acceptable.
- Running headers/footers being deduplicated is acceptable.
- Page numbers being removed is acceptable.
- Minor whitespace or punctuation normalization is acceptable.

## What is NOT acceptable
- Missing paragraphs or sections of text
- Missing or incomplete tables
- Missing list items
- Truncated content
- Garbled or corrupted text
- Missing headings that exist in the PDF
- Structurally incorrect tables (wrong number of rows/columns)

## Output format

Respond with a JSON object in this exact format:
{
    "is_complete": true/false,
    "completeness_score": <number 0-100>,
    "summary": "<1-2 sentence overall assessment>",
    "missing_elements": [
        {
            "type": "<heading|paragraph|table|list|image|link|form|other>",
            "description": "<what is missing>",
            "pdf_location": "<where in the PDF this appears, e.g. 'page 3, second paragraph'>",
            "html_annotation": "<where in the HTML this should have appeared, e.g. 'after the heading Government Structure on page 2'>"
        }
    ],
    "structural_issues": [
        {
            "type": "<table_structure|heading_hierarchy|list_nesting|other>",
            "description": "<what is wrong structurally>",
            "location": "<where this occurs>"
        }
    ]
}

If the HTML is complete, set is_complete to true, completeness_score to 100,
and leave missing_elements and structural_issues as empty arrays.

Be thorough but fair. Focus on substantive content gaps, not cosmetic differences.
"""

AUDIT_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "is_complete": {"type": "BOOLEAN"},
        "completeness_score": {"type": "INTEGER"},
        "summary": {"type": "STRING"},
        "missing_elements": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "type": {"type": "STRING"},
                    "description": {"type": "STRING"},
                    "pdf_location": {"type": "STRING"},
                    "html_annotation": {"type": "STRING"},
                },
                "required": ["type", "description", "pdf_location", "html_annotation"],
            },
        },
        "structural_issues": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "type": {"type": "STRING"},
                    "description": {"type": "STRING"},
                    "location": {"type": "STRING"},
                },
                "required": ["type", "description", "location"],
            },
        },
    },
    "required": [
        "is_complete",
        "completeness_score",
        "summary",
        "missing_elements",
        "structural_issues",
    ],
}


# ---------------------------------------------------------------------------
# Core audit function
# ---------------------------------------------------------------------------

@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def audit_one(pdf_path: Path, html_path: Path) -> dict:
    """Send PDF + HTML to Gemini and get completeness audit."""
    pdf_bytes = pdf_path.read_bytes()
    html_text = html_path.read_text(encoding="utf-8")

    config = types.GenerateContentConfig(
        max_output_tokens=MAX_OUTPUT_TOKENS,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        top_k=TOP_K,
        response_mime_type="application/json",
        response_schema=AUDIT_SCHEMA,
        safety_settings=get_safety_settings(),
    )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
            types.Part.from_text(text=f"Here is the HTML rendering to audit:\n\n{html_text}"),
            AUDIT_PROMPT,
        ],
        config=config,
    )

    input_tokens = getattr(response.usage_metadata, "prompt_token_count", 0) or 0
    output_tokens = getattr(response.usage_metadata, "candidates_token_count", 0) or 0

    result = json.loads(response.text)
    result["_tokens"] = {"input": input_tokens, "output": output_tokens}
    return result


def process_folder(folder: Path) -> dict:
    """Process a single folder: find PDF + HTML, run audit."""
    folder_name = folder.name

    pdf_path = folder / "source.pdf"
    if not pdf_path.exists():
        return {"folder": folder_name, "error": "source.pdf not found"}

    # Find the .html file (there should be exactly one)
    html_files = list(folder.glob("*.html"))
    if not html_files:
        return {"folder": folder_name, "error": "no .html file found"}
    html_path = html_files[0]

    try:
        start = time.time()
        result = audit_one(pdf_path, html_path)
        elapsed = time.time() - start
        result["folder"] = folder_name
        result["html_file"] = html_path.name
        result["elapsed_seconds"] = round(elapsed, 1)
        return result
    except Exception as e:
        return {"folder": folder_name, "error": str(e)}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit HTML completeness against source PDFs using Gemini."
    )
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Directory containing subfolders with source.pdf and .html files",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output directory for audit results (default: input_dir)",
    )
    parser.add_argument(
        "-c", "--concurrency",
        type=int,
        default=DEFAULT_CONCURRENCY,
        help=f"Number of parallel audit calls (default: {DEFAULT_CONCURRENCY})",
    )
    args = parser.parse_args()

    input_dir = args.input_dir
    if not input_dir.is_dir():
        print(f"Error: {input_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    output_dir = args.output or input_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find all folders that have a source.pdf
    folders = sorted(
        f for f in input_dir.iterdir()
        if f.is_dir() and (f / "source.pdf").exists()
    )

    if not folders:
        print(f"No folders with source.pdf found in {input_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(folders)} documents to audit (concurrency={args.concurrency})\n")

    results = []
    complete_count = 0
    incomplete_count = 0
    error_count = 0
    total_missing = 0

    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        future_to_folder = {
            pool.submit(process_folder, folder): folder for folder in folders
        }

        for future in as_completed(future_to_folder):
            folder = future_to_folder[future]
            result = future.result()
            results.append(result)

            if "error" in result:
                error_count += 1
                print(f"  ERROR  {result['folder']}: {result['error']}")
            elif result.get("is_complete"):
                complete_count += 1
                tokens = result.get("_tokens", {})
                print(
                    f"  PASS   {result['folder']} "
                    f"(score={result['completeness_score']}, "
                    f"{result.get('elapsed_seconds', '?')}s, "
                    f"tokens={tokens.get('input', 0)}+{tokens.get('output', 0)})"
                )
            else:
                incomplete_count += 1
                n_missing = len(result.get("missing_elements", []))
                n_structural = len(result.get("structural_issues", []))
                total_missing += n_missing
                tokens = result.get("_tokens", {})
                print(
                    f"  FAIL   {result['folder']} "
                    f"(score={result['completeness_score']}, "
                    f"missing={n_missing}, structural={n_structural}, "
                    f"{result.get('elapsed_seconds', '?')}s, "
                    f"tokens={tokens.get('input', 0)}+{tokens.get('output', 0)})"
                )
                for elem in result.get("missing_elements", []):
                    print(
                        f"           - [{elem['type']}] {elem['description']}"
                        f"\n             PDF: {elem['pdf_location']}"
                        f"\n             HTML: {elem['html_annotation']}"
                    )

    # Save full results as JSON
    report_path = output_dir / "audit_report.json"
    clean_results = []
    for r in sorted(results, key=lambda x: x.get("folder", "")):
        r_copy = dict(r)
        r_copy.pop("_tokens", None)
        clean_results.append(r_copy)

    report_path.write_text(
        json.dumps(clean_results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # Summary
    print(f"\n{'='*60}")
    print(f"Audit complete: {len(results)} documents")
    print(f"  Complete:   {complete_count}")
    print(f"  Incomplete: {incomplete_count} ({total_missing} total missing elements)")
    print(f"  Errors:     {error_count}")
    print(f"\nFull report: {report_path}")


if __name__ == "__main__":
    main()
