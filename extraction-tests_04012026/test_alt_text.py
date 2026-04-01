#!/usr/bin/env python3
"""Test per-image alt text generation on existing JSON files.

Usage:
    python test_alt_text.py <folder_name> [page_number]
    python test_alt_text.py gicc-ncdot-florence-20181107-68614eed 7
    python test_alt_text.py seal-image-table-6870
"""

import base64
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from extract_structured_json import PDFExtractor

DATA_DIR = Path(__file__).parent / "json_to_html_to_auditor"


def test_alt_text(folder_name: str, page_filter: int = None):
    json_file = DATA_DIR / folder_name / f"{folder_name}.json"
    if not json_file.exists():
        print(f"JSON not found: {json_file}")
        sys.exit(1)

    with open(json_file) as f:
        data = json.load(f)

    ext = PDFExtractor()

    for page in data["pages"]:
        page_num = page.get("page_number", 0)
        if page_filter and page_num != page_filter:
            continue

        images = [item for item in page.get("content", []) if item.get("type") == "image"]
        if not images:
            continue

        print(f"\n=== Page {page_num}: {len(images)} images ===")

        for i, img in enumerate(images):
            has_data = "base64_data" in img
            old_desc = img.get("description", "")
            is_composite = img.get("_full_page_render", False)
            bbox = img.get("bbox", {})

            if not has_data:
                print(f"  Image {i+1}: NO DATA - desc=\"{old_desc[:60]}\"")
                continue

            # Decode to check size
            image_bytes = base64.b64decode(img["base64_data"])
            if len(image_bytes) < 1024:
                print(f"  Image {i+1}: TINY ({len(image_bytes)}B) - desc=\"{old_desc[:60]}\"")
                continue

            print(f"  Image {i+1}: {len(image_bytes):,}B, format={img.get('format','?')}, composite={is_composite}")
            print(f"    OLD desc: \"{old_desc[:100]}\"")

            try:
                if is_composite:
                    alt_text, inp, out = ext._call_gemini_for_alt_text(
                        image_bytes, img.get("format", "png"), ext.FULL_PAGE_ALT_TEXT_PROMPT
                    )
                else:
                    alt_text, inp, out = ext.generate_alt_text_for_image(
                        image_bytes, img.get("format", "png")
                    )
                print(f"    NEW desc: \"{alt_text[:100]}\"")
                print(f"    Tokens: {inp} in, {out} out")
            except Exception as e:
                print(f"    ERROR: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_alt_text.py <folder_name> [page_number]")
        sys.exit(1)

    folder = sys.argv[1]
    page = int(sys.argv[2]) if len(sys.argv) > 2 else None
    test_alt_text(folder, page)
