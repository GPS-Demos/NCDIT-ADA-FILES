#!/usr/bin/env python3
"""Re-extract a single PDF folder using the current extraction pipeline.

Usage:
    python reextract_single.py <folder_name>

The folder must exist under json_to_html_to_auditor/ and contain source.pdf.
Overwrites the existing {folder_name}.json and {folder_name}.html in that folder.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from multiprocessing import Pool

sys.path.insert(0, str(Path(__file__).parent))

from extract_structured_json import (
    PDFExtractor,
    _process_page_worker,
)
import pypdfium2 as pdfium

DATA_DIR = Path(__file__).parent / "json_to_html_to_auditor"


def reextract(folder_name: str):
    folder = DATA_DIR / folder_name
    if not folder.exists():
        print(f"ERROR: folder not found: {folder}")
        sys.exit(1)

    pdf_path = folder / "source.pdf"
    if not pdf_path.exists():
        print(f"ERROR: source.pdf not found in {folder}")
        sys.exit(1)

    doc_id = folder_name
    print(f"Re-extracting: {doc_id}")
    print(f"PDF: {pdf_path}")

    # Count pages
    doc = pdfium.PdfDocument(str(pdf_path))
    page_count = len(doc)
    doc.close()
    print(f"Pages: {page_count}")

    # Build page tasks
    tasks = [(str(pdf_path), page_num, doc_id) for page_num in range(page_count)]

    # Process pages (use single-process for clarity and easier debugging)
    results_by_page = {}
    extractor = PDFExtractor()
    for i, task in enumerate(tasks):
        print(f"  Processing page {i + 1}/{page_count}...")
        _, page_num, result = _process_page_worker(task)
        results_by_page[page_num] = result
        if result.get("error"):
            print(f"    WARNING: page {page_num + 1} error: {result['error']}")

    # Sort pages
    pages = [results_by_page[i] for i in sorted(results_by_page.keys())]

    # Apply cross-page post-processing
    pages = extractor._deduplicate_cross_page_content(pages)
    pages = extractor._merge_cross_page_content(pages)
    pages = extractor._normalize_heading_hierarchy(pages)

    result = {
        "pdf_id": doc_id,
        "source_path": str(pdf_path),
        "total_pages": page_count,
        "extraction_timestamp": datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z"),
        "pages": pages,
        "quality_metrics": extractor._calculate_pdf_metrics(pages),
    }

    # Save JSON
    json_out = folder / f"{doc_id}.json"
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"Saved JSON: {json_out}")

    # Generate HTML using render_json
    from render_json import render_one
    html_out = folder / f"{doc_id}.html"
    render_one(json_out, html_out)
    print(f"Saved HTML: {html_out}")

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python reextract_single.py <folder_name>")
        sys.exit(1)
    reextract(sys.argv[1])
