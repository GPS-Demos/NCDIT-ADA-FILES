#!/usr/bin/env python3
"""Download PDFs from URLs and compare file sizes with source.pdf files."""

import csv
import os
import tempfile
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = '/usr/local/google/home/stonejiang/NCDIT-ADA-FILES/extraction_tests_simplied_html_generator-pro-fixes'
CSV_PATH = os.path.join(BASE_DIR, 'output_urls.csv')
SRC_DIR = os.path.join(BASE_DIR, 'json_to_html_to_auditor')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; PDF-checker/1.0)',
    'Accept': 'application/pdf,*/*',
}

def check_one(row):
    fname = row['json_file']
    url = row['url']
    name = fname[:-5]  # strip .json
    source_pdf = os.path.join(SRC_DIR, name, 'source.pdf')

    if not os.path.exists(source_pdf):
        return {'name': name, 'status': 'MISSING_SOURCE', 'source_size': None, 'download_size': None, 'url': url}

    source_size = os.path.getsize(source_pdf)

    try:
        resp = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
        resp.raise_for_status()
        download_size = len(resp.content)
        match = source_size == download_size
        status = 'MATCH' if match else 'MISMATCH'
        return {
            'name': name,
            'status': status,
            'source_size': source_size,
            'download_size': download_size,
            'url': url,
        }
    except Exception as e:
        return {'name': name, 'status': f'ERROR: {e}', 'source_size': source_size, 'download_size': None, 'url': url}


def main():
    rows = []
    with open(CSV_PATH, newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Checking {len(rows)} files...")
    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_one, row): row for row in rows}
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            results.append(result)
            status = result['status']
            print(f"[{i:3d}/100] {status:10s}  {result['name'][:60]}")

    results.sort(key=lambda r: r['name'])

    matches = [r for r in results if r['status'] == 'MATCH']
    mismatches = [r for r in results if r['status'] == 'MISMATCH']
    errors = [r for r in results if r['status'] not in ('MATCH', 'MISMATCH')]

    print(f"\n{'='*70}")
    print(f"MATCHES:    {len(matches)}")
    print(f"MISMATCHES: {len(mismatches)}")
    print(f"ERRORS:     {len(errors)}")

    if mismatches:
        print(f"\nMISMATCHES:")
        for r in mismatches:
            print(f"  {r['name']}")
            print(f"    source:   {r['source_size']:,} bytes")
            print(f"    download: {r['download_size']:,} bytes")
            print(f"    url:      {r['url']}")

    if errors:
        print(f"\nERRORS:")
        for r in errors:
            print(f"  {r['name']}: {r['status']}")
            print(f"    url: {r['url']}")

    # Write results CSV
    out_csv = os.path.join(BASE_DIR, 'pdf_size_check.csv')
    with open(out_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'status', 'source_size', 'download_size', 'url'])
        writer.writeheader()
        writer.writerows(results)
    print(f"\nResults written to {out_csv}")


if __name__ == '__main__':
    main()
