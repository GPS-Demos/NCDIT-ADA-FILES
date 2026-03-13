#!/bin/bash
# Find the source.pdf with the most pages in all subdirectories

results=""
max_pages=0
max_file=""

for pdf in */source.pdf; do
    pages=$(pdfinfo "$pdf" 2>/dev/null | grep "^Pages:" | awk '{print $2}')
    if [ -n "$pages" ]; then
        results+="$(printf "%4d pages  %s\n" "$pages" "$pdf")"$'\n'
        if [ "$pages" -gt "$max_pages" ]; then
            max_pages=$pages
            max_file=$pdf
        fi
    fi
done

echo "$results" | sort -rn

echo ""
echo "=== LARGEST FILE ==="
echo "$max_file — $max_pages pages"
