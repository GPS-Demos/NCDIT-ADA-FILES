#!/usr/bin/env python3
"""Test post-processing improvements on existing JSON files.

This script loads existing extraction JSON, applies the new post-processing
steps from extract_structured_json.py, and reports what would change.

Usage:
    python test_post_processing.py <folder_name>
    python test_post_processing.py scio-physical-and-environmental-protection-686b1b84
    python test_post_processing.py all  # test all folders
"""

import json
import sys
import re
from pathlib import Path

# Add parent dir to path so we can import from extract_structured_json
sys.path.insert(0, str(Path(__file__).parent))

from extract_structured_json import PDFExtractor

DATA_DIR = Path(__file__).parent / "json_to_html_to_auditor"


def test_post_processing_on_file(json_path: Path):
    """Apply post-processing fixes to an existing JSON file and report changes."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    pdf_id = data.get("pdf_id", json_path.stem)
    pages = data.get("pages", [])

    extractor = PDFExtractor()
    changes = []

    # Test 1: _strip_spurious_markdown on table cells, headings, and list items
    markdown_stripped = 0
    for page in pages:
        for item in page.get("content", []):
            if item.get("type") == "table":
                for cell in item.get("cells", []):
                    original = cell.get("text", "")
                    stripped = extractor._strip_spurious_markdown(original)
                    if stripped != original:
                        markdown_stripped += 1
                        if markdown_stripped <= 5:
                            changes.append(f"  Table cell: \"{original[:60]}\" -> \"{stripped[:60]}\"")
            elif item.get("type") == "heading":
                original = item.get("text", "")
                stripped = extractor._strip_spurious_markdown(original)
                if stripped != original:
                    markdown_stripped += 1
                    if markdown_stripped <= 5:
                        changes.append(f"  Heading: \"{original[:60]}\" -> \"{stripped[:60]}\"")
            elif item.get("type") == "list":
                for li in item.get("items", []):
                    original = li.get("text", "")
                    stripped = extractor._strip_spurious_markdown(original)
                    if stripped != original:
                        markdown_stripped += 1
                        if markdown_stripped <= 5:
                            changes.append(f"  List item: \"{original[:60]}\" -> \"{stripped[:60]}\"")
                    for child in li.get("children", []):
                        original = child.get("text", "")
                        stripped = extractor._strip_spurious_markdown(original)
                        if stripped != original:
                            markdown_stripped += 1

    # Test 1b: list number prefix stripping
    list_numbers_stripped = 0
    for page in pages:
        for item in page.get("content", []):
            if item.get("type") == "list" and item.get("list_type") == "ordered":
                for li in item.get("items", []):
                    original = li.get("text", "")
                    stripped = extractor._strip_list_number_prefix(original)
                    if stripped != original:
                        list_numbers_stripped += 1

    # Test 1c: list merging
    import copy
    lists_merged = 0
    for page in pages:
        content = page.get("content", [])
        merged = extractor._merge_consecutive_lists(copy.deepcopy(content))
        orig_lists = sum(1 for i in content if i.get("type") == "list")
        merged_lists = sum(1 for i in merged if i.get("type") == "list")
        lists_merged += (orig_lists - merged_lists)

    # Test 2: Cross-page deduplication
    original_items = sum(len(p.get("content", [])) for p in pages)
    deduped_pages = extractor._deduplicate_cross_page_content(
        # Deep copy to avoid mutating
        json.loads(json.dumps(pages))
    )
    deduped_items = sum(len(p.get("content", [])) for p in deduped_pages)
    items_removed = original_items - deduped_items

    # Test 3: Link merging (simulate - count existing link items at end of pages)
    link_items_at_end = 0
    for page in pages:
        content = page.get("content", [])
        # Count trailing link items
        for item in reversed(content):
            if item.get("type") == "link":
                link_items_at_end += 1
            else:
                break

    # Report
    print(f"\n{'='*60}")
    print(f"File: {pdf_id}")
    print(f"{'='*60}")

    if markdown_stripped > 0:
        print(f"  Markdown stripped from {markdown_stripped} table cells/headings/list items")
        for c in changes:
            print(c)

    if list_numbers_stripped > 0:
        print(f"  List number prefixes stripped: {list_numbers_stripped}")

    if lists_merged > 0:
        print(f"  Consecutive lists merged: {lists_merged}")

    if items_removed > 0:
        print(f"  Cross-page dedup: {items_removed} items removed (repeated headers/tables)")

    if link_items_at_end > 0:
        print(f"  Trailing link items: {link_items_at_end} (would be deduplicated by link merging)")

    has_changes = markdown_stripped + list_numbers_stripped + lists_merged + items_removed + link_items_at_end
    if has_changes == 0:
        print("  No changes needed")

    return {
        "pdf_id": pdf_id,
        "markdown_stripped": markdown_stripped,
        "list_numbers_stripped": list_numbers_stripped,
        "lists_merged": lists_merged,
        "items_removed_by_dedup": items_removed,
        "trailing_links": link_items_at_end,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_post_processing.py <folder_name|all>")
        sys.exit(1)

    target = sys.argv[1]

    if target == "all":
        folders = sorted(DATA_DIR.iterdir())
    else:
        folder = DATA_DIR / target
        if not folder.exists():
            print(f"Folder not found: {folder}")
            sys.exit(1)
        folders = [folder]

    total_stats = {
        "files_tested": 0,
        "total_markdown_stripped": 0,
        "total_list_numbers": 0,
        "total_lists_merged": 0,
        "total_items_deduped": 0,
        "total_trailing_links": 0,
    }

    for folder in folders:
        if not folder.is_dir():
            continue
        json_file = folder / f"{folder.name}.json"
        if not json_file.exists():
            continue

        stats = test_post_processing_on_file(json_file)
        total_stats["files_tested"] += 1
        total_stats["total_markdown_stripped"] += stats["markdown_stripped"]
        total_stats["total_list_numbers"] += stats["list_numbers_stripped"]
        total_stats["total_lists_merged"] += stats["lists_merged"]
        total_stats["total_items_deduped"] += stats["items_removed_by_dedup"]
        total_stats["total_trailing_links"] += stats["trailing_links"]

    if total_stats["files_tested"] > 1:
        print(f"\n{'='*60}")
        print(f"SUMMARY ({total_stats['files_tested']} files tested)")
        print(f"{'='*60}")
        print(f"  Total markdown stripped: {total_stats['total_markdown_stripped']}")
        print(f"  Total list number prefixes stripped: {total_stats['total_list_numbers']}")
        print(f"  Total consecutive lists merged: {total_stats['total_lists_merged']}")
        print(f"  Total items removed by cross-page dedup: {total_stats['total_items_deduped']}")
        print(f"  Total trailing link items: {total_stats['total_trailing_links']}")


if __name__ == "__main__":
    main()
