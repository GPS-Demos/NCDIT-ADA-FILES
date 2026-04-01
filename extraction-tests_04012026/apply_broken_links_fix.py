"""
Apply the _fix_broken_hyperlinks post-processing step to existing JSON files.
Then regenerate the HTML for each file.

Usage:
    python apply_broken_links_fix.py <folder_name>     # Single file
    python apply_broken_links_fix.py --section-f        # All Section F files
    python apply_broken_links_fix.py --all              # All files
    python apply_broken_links_fix.py --dry-run <folder> # Preview without saving
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from extract_structured_json import PDFExtractor
from render_json import render_document, _apply_ada_remediation

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


def apply_fix_to_file(folder_name, dry_run=False):
    """Apply the broken links fix to a single JSON file and regenerate HTML."""
    json_path = BASE / folder_name / f"{folder_name}.json"
    html_path = BASE / folder_name / f"{folder_name}.html"

    if not json_path.exists():
        print(f"  SKIP: {folder_name} (JSON not found)")
        return 0

    with open(json_path, "r") as f:
        data = json.load(f)

    extractor = PDFExtractor()
    total_fixed = 0

    for page in data.get("pages", []):
        content = page.get("content", [])
        if not content:
            continue
        fixed_content, fixed = extractor._fix_broken_hyperlinks(content)
        if fixed > 0:
            page["content"] = fixed_content
            total_fixed += fixed

    if total_fixed > 0:
        if dry_run:
            print(f"  [DRY RUN] {folder_name}: would fix {total_fixed} links")
        else:
            with open(json_path, "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            # Regenerate HTML (apply ADA remediation first for proper dedup)
            _apply_ada_remediation(data)
            html_content = render_document(data)
            with open(html_path, "w") as f:
                f.write(html_content)
            print(f"  FIXED: {folder_name}: {total_fixed} links fixed, HTML regenerated")
    else:
        print(f"  OK: {folder_name}: no broken links found")

    return total_fixed


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]

    if not args:
        print("Usage: python apply_broken_links_fix.py [--dry-run] <folder_name|--section-f|--all>")
        sys.exit(1)

    if "--section-f" in args:
        folders = SECTION_F_FILES
        print(f"Applying fix to {len(folders)} Section F files...")
    elif "--all" in args:
        folders = sorted(
            d.name for d in BASE.iterdir()
            if d.is_dir() and (d / f"{d.name}.json").exists()
        )
        print(f"Applying fix to all {len(folders)} files...")
    else:
        folders = args
        print(f"Applying fix to {len(folders)} file(s)...")

    total = 0
    for folder in folders:
        fixed = apply_fix_to_file(folder, dry_run=dry_run)
        total += fixed

    print(f"\nTotal links fixed: {total}")


if __name__ == "__main__":
    main()
