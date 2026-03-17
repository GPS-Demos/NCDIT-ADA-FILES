#!/usr/bin/env python3
"""Regenerate alt text for images in existing JSON files using per-image Gemini calls.

This is a standalone tool that:
1. Reads existing extraction JSON files
2. For each image with base64 data, calls Gemini to generate accurate alt text
3. Updates the JSON file in-place with new descriptions
4. Re-renders the HTML from the updated JSON

Usage:
    python regenerate_alt_text.py <folder_name>          # Single file
    python regenerate_alt_text.py <folder_name> --page 7 # Single page
    python regenerate_alt_text.py --all                   # All files (WARNING: many API calls)
    python regenerate_alt_text.py --dry-run <folder>      # Preview without API calls
"""

import argparse
import base64
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from extract_structured_json import PDFExtractor
from render_json import main as render_main

DATA_DIR = Path(__file__).parent / "json_to_html_to_auditor"


def regenerate_file(folder_name: str, page_filter: int = None, dry_run: bool = False):
    """Regenerate alt text for a single file."""
    json_file = DATA_DIR / folder_name / f"{folder_name}.json"
    if not json_file.exists():
        print(f"JSON not found: {json_file}")
        return False

    with open(json_file) as f:
        data = json.load(f)

    ext = PDFExtractor()
    total_updated = 0
    total_input_tokens = 0
    total_output_tokens = 0

    for page in data["pages"]:
        page_num = page.get("page_number", 0)
        if page_filter and page_num != page_filter:
            continue

        images = [item for item in page.get("content", []) if item.get("type") == "image"]
        if not images:
            continue

        for i, img in enumerate(images):
            if "base64_data" not in img:
                continue

            try:
                image_bytes = base64.b64decode(img["base64_data"])
            except Exception:
                continue

            if len(image_bytes) < 1024:
                continue

            old_desc = img.get("description", "")
            img_format = img.get("format", "png")
            is_composite = img.get("_full_page_render", False)

            if dry_run:
                print(f"  P{page_num} Image {i+1}: Would regenerate (currently: \"{old_desc[:60]}\")")
                total_updated += 1
                continue

            try:
                if is_composite:
                    alt_text, inp, out = ext._call_gemini_for_alt_text(
                        image_bytes, img_format, ext.FULL_PAGE_ALT_TEXT_PROMPT
                    )
                else:
                    alt_text, inp, out = ext.generate_alt_text_for_image(
                        image_bytes, img_format
                    )
                total_input_tokens += inp
                total_output_tokens += out

                if alt_text:
                    img["description"] = alt_text
                    total_updated += 1
                    print(f"  P{page_num} Image {i+1}: \"{alt_text[:70]}\"")
            except Exception as e:
                print(f"  P{page_num} Image {i+1}: ERROR - {e}")

    if not dry_run and total_updated > 0:
        # Save updated JSON
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  Saved: {total_updated} images updated, {total_input_tokens + total_output_tokens:,} tokens")

        # Re-render HTML
        sys.argv = ["render_json.py", str(json_file.parent)]
        try:
            render_main()
        except SystemExit:
            pass
    elif dry_run:
        print(f"  Dry run: {total_updated} images would be updated")
    else:
        print(f"  No images to update")

    return True


def main():
    parser = argparse.ArgumentParser(description="Regenerate alt text for images")
    parser.add_argument("folder", nargs="?", help="Folder name to process")
    parser.add_argument("--page", type=int, help="Only process this page number")
    parser.add_argument("--all", action="store_true", help="Process all files")
    parser.add_argument("--dry-run", action="store_true", help="Preview without API calls")
    args = parser.parse_args()

    if args.all:
        folders = sorted(d.name for d in DATA_DIR.iterdir() if d.is_dir())
        for folder in folders:
            print(f"\n{'='*60}")
            print(f"Processing: {folder}")
            print(f"{'='*60}")
            regenerate_file(folder, dry_run=args.dry_run)
    elif args.folder:
        print(f"Processing: {args.folder}")
        regenerate_file(args.folder, page_filter=args.page, dry_run=args.dry_run)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
