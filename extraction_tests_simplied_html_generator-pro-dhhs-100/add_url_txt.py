#!/usr/bin/env python3
import csv
import os

CSV_PATH = "/usr/local/google/home/stonejiang/Downloads/New Batch 50 DHHS and 50 DIT - random_pdf_sample_set-50_dor-50_dhhs.csv"
TARGET_DIR = "/usr/local/google/home/stonejiang/NCDIT-ADA-FILES/extraction_tests_simplied_html_generator-pro-dhhs-100/json_to_html_to_auditor"

with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

written = 0
skipped = 0
for row in rows:
    name = row['name'].strip()
    url = row['url'].strip()
    folder_name = name.replace(' ', '_').replace('/', '')
    folder_path = os.path.join(TARGET_DIR, folder_name)
    if not os.path.isdir(folder_path):
        skipped += 1
        continue
    url_file = os.path.join(folder_path, 'url.txt')
    with open(url_file, 'w') as out:
        out.write(url + '\n')
    written += 1

print(f"Done. Wrote {written} url.txt files, skipped {skipped} (no matching folder).")
