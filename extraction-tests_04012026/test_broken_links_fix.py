"""
Test script for the _fix_broken_hyperlinks post-processing step.

Tests the fix against actual JSON files from the affected documents
listed in FIXES.md Section F (Broken/Wrong Hyperlinks).
"""

import json
import sys
from pathlib import Path

# Add parent to path so we can import the extractor
sys.path.insert(0, str(Path(__file__).parent))

from extract_structured_json import PDFExtractor

BASE = Path(__file__).parent / "json_to_html_to_auditor"

SECTION_F_FILES = [
    "seal-image-table-6870",
    "powerpoint-slides-fef1",
    "gicc-smac-agenda-20210120-68839aac",
    "911-education-committee-meeting-agenda-packet-03-25-2021-685f9fa9",
    "gicc-meeting-minutes-02122003-685fb099",
    "seal-imagery-table-with-shading-132c",
    "20200522-board-agenda-685f9ca8",
    "logo-tables-shading-watermark-photos-13a3",
    "nc-911-board-meeting-agenda-aug-26-2022-685f9a31",
    "near-perfect-powerpoint-slides-by-accessibility-experts-47b0",
    "gicc-ncdot-florence-20181107-68614eed",
    "map-imagery-photos-tables-screenshots-diagrams-data-charts-0fb1",
    "map-imagery-photos-tables-screenshots-diagrams-data-charts-365a",
    "logos-graphic-colors-photos-icons-diagrams-charts-53e1",
]


def load_json(folder_name):
    """Load the JSON file for a given folder name."""
    json_path = BASE / folder_name / f"{folder_name}.json"
    if not json_path.exists():
        return None
    with open(json_path, "r") as f:
        return json.load(f)


def count_broken_links(content):
    """Count link items that have broken URLs (url == text or invalid URL)."""
    broken = 0
    for item in content:
        if item.get("type") != "link":
            continue
        url = item.get("url", "").strip()
        text = item.get("text", "").strip()
        if not PDFExtractor._is_valid_url(url):
            broken += 1
        elif url == text and not url.startswith(("http://", "https://", "mailto:", "tel:", "ftp://")):
            broken += 1
    return broken


def count_bare_domain_links(content):
    """Count link items with bare domain URLs (missing protocol)."""
    count = 0
    for item in content:
        if item.get("type") != "link":
            continue
        url = item.get("url", "").strip()
        if url and not url.startswith(("http://", "https://", "mailto:", "tel:", "ftp://", "/")):
            import re
            if re.match(r'^[\w.-]+\.\w{2,}(?:/\S*)?$', url):
                count += 1
    return count


def count_consecutive_same_url_links(content):
    """Count groups of consecutive link items with the same URL."""
    groups = 0
    i = 0
    while i < len(content):
        if content[i].get("type") == "link":
            url = content[i].get("url", "")
            j = i + 1
            while j < len(content) and content[j].get("type") == "link" and content[j].get("url") == url:
                j += 1
            if j > i + 1:
                groups += 1
            i = j
        else:
            i += 1
    return groups


def main():
    extractor = PDFExtractor()

    total_broken_before = 0
    total_broken_after = 0
    total_bare_domain_before = 0
    total_bare_domain_after = 0
    total_consec_before = 0
    total_consec_after = 0
    total_fixed = 0

    print("=" * 80)
    print("Testing _fix_broken_hyperlinks on Section F files")
    print("=" * 80)

    for folder in SECTION_F_FILES:
        data = load_json(folder)
        if data is None:
            print(f"\n  SKIP: {folder} (JSON not found)")
            continue

        print(f"\n  {folder}")

        # Collect all content from all pages
        all_content_before = []
        for page in data.get("pages", []):
            all_content_before.extend(page.get("content", []))

        broken_before = count_broken_links(all_content_before)
        bare_before = count_bare_domain_links(all_content_before)
        consec_before = count_consecutive_same_url_links(all_content_before)

        # Apply fix
        fixed_content, links_fixed = extractor._fix_broken_hyperlinks(list(all_content_before))

        broken_after = count_broken_links(fixed_content)
        bare_after = count_bare_domain_links(fixed_content)
        consec_after = count_consecutive_same_url_links(fixed_content)

        print(f"    Broken links:      {broken_before} -> {broken_after}")
        print(f"    Bare domain URLs:  {bare_before} -> {bare_after}")
        print(f"    Consecutive dupes: {consec_before} -> {consec_after}")
        print(f"    Total fixed:       {links_fixed}")

        total_broken_before += broken_before
        total_broken_after += broken_after
        total_bare_domain_before += bare_before
        total_bare_domain_after += bare_after
        total_consec_before += consec_before
        total_consec_after += consec_after
        total_fixed += links_fixed

    print("\n" + "=" * 80)
    print("TOTALS across all Section F files:")
    print(f"  Broken links:      {total_broken_before} -> {total_broken_after}")
    print(f"  Bare domain URLs:  {total_bare_domain_before} -> {total_bare_domain_after}")
    print(f"  Consecutive dupes: {total_consec_before} -> {total_consec_after}")
    print(f"  Total links fixed: {total_fixed}")
    print("=" * 80)

    # Also test on ALL files to check for regressions
    print("\n\nRegression check on ALL files...")
    all_folders = [d.name for d in BASE.iterdir() if d.is_dir() and (d / f"{d.name}.json").exists()]

    total_links_before = 0
    total_links_after = 0
    total_valid_links_before = 0
    total_valid_links_after = 0
    total_all_fixed = 0

    for folder in sorted(all_folders):
        data = load_json(folder)
        if data is None:
            continue

        all_content = []
        for page in data.get("pages", []):
            all_content.extend(page.get("content", []))

        link_count_before = sum(1 for item in all_content if item.get("type") == "link")
        valid_links_before = sum(
            1 for item in all_content
            if item.get("type") == "link" and PDFExtractor._is_valid_url(item.get("url", ""))
        )

        fixed_content, fixed = extractor._fix_broken_hyperlinks(list(all_content))

        link_count_after = sum(1 for item in fixed_content if item.get("type") == "link")
        valid_links_after = sum(
            1 for item in fixed_content
            if item.get("type") == "link" and PDFExtractor._is_valid_url(item.get("url", ""))
        )

        total_links_before += link_count_before
        total_links_after += link_count_after
        total_valid_links_before += valid_links_before
        total_valid_links_after += valid_links_after
        total_all_fixed += fixed

        if fixed > 0:
            print(f"  {folder}: {link_count_before} links -> {link_count_after} links ({fixed} fixed)")

    print(f"\n  ALL FILES TOTAL:")
    print(f"    Links before:       {total_links_before}")
    print(f"    Links after:        {total_links_after}")
    print(f"    Valid links before: {total_valid_links_before}")
    print(f"    Valid links after:  {total_valid_links_after}")
    print(f"    Total fixed:        {total_all_fixed}")

    # Verify no valid links were lost
    if total_valid_links_after < total_valid_links_before:
        print(f"\n  WARNING: Valid links decreased from {total_valid_links_before} to {total_valid_links_after}!")
        print("  This may indicate a regression.")
    else:
        print(f"\n  OK: All {total_valid_links_after} valid links preserved (was {total_valid_links_before})")


if __name__ == "__main__":
    main()
