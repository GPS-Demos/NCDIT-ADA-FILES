#!/usr/bin/env python3
import csv
import os
import subprocess
import sys

CSV_PATH = "/usr/local/google/home/stonejiang/Downloads/New Batch 50 DHHS and 50 DIT - random_pdf_sample_set-50_dor-50_dhhs.csv"
OUTPUT_DIR = "/usr/local/google/home/stonejiang/NCDIT-ADA-FILES/extraction_tests_simplied_html_generator-pro-dhhs-100"

with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

total = len(rows)
for i, row in enumerate(rows, 1):
    name = row['name'].strip()
    url = row['url'].strip()
    folder_name = name.replace(' ', '_').replace('/', '')
    folder_path = os.path.join(OUTPUT_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    out_path = os.path.join(folder_path, 'source.pdf')
    if os.path.exists(out_path):
        print(f"[{i}/{total}] SKIP (exists): {folder_name}")
        continue
    print(f"[{i}/{total}] Downloading: {folder_name}")
    result = subprocess.run(
        ['curl', '-L', '-s', '-o', out_path, '--max-time', '30', url],
        capture_output=True
    )
    if result.returncode != 0:
        print(f"  ERROR: curl returned {result.returncode} for {url}")
    else:
        size = os.path.getsize(out_path) if os.path.exists(out_path) else 0
        print(f"  OK: {size} bytes")

print("Done.")
