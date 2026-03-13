# Full Pipeline: JSON → ADA-Compliant HTML → Auditor

New pipeline in: /usr/local/google/home/stonejiang/NCDIT-ADA-FILES/extraction_tests_simplied_html_generator/render_json.py
First, run extract_structured_json.py 

All commands run from `google/backend/`.

```bash
DOC_ROOT="/usr/local/google/home/stonejiang/NCDIT-ADA-FILES/extraction_tests_03122026/output/json_to_html_to_auditor"
cd /usr/local/google/home/stonejiang/ada-compliance-engine/google/backend
```

## Step 1: Generate ADA-Compliant HTML

Renders each extraction JSON to ADA-compliant HTML with all 13 remediation steps (heading normalization, table header inference, link injection, etc.):

```bash
for dir in "$DOC_ROOT"/*/; do
  json_file=$(find "$dir" -maxdepth 1 -name "*.json" ! -name "semantic.json" ! -name "result.json" | head -1)
  if [ -n "$json_file" ]; then
    python scripts/render_json.py "$json_file" -o "${dir}output.html"
  fi
done
```

## Step 2: Run the Full Auditor

This finds subdirs with `source.pdf` + `output.html`, generates `semantic.json` and `result.json`, runs fidelity scoring (3 Gemini calls/doc), runs the auditor (1 Gemini call/doc), and writes per-document `audit-report.json` + summary `results.json`.

### With LLM scoring (recommended — meaningful scores):

```bash
python scripts/audit_rendered.py \
  --doc-root "$DOC_ROOT" \
  --json-dir "$DOC_ROOT" \
  --concurrency 5
```

~4 Gemini API calls per document. 100 docs = ~400 calls, ~20-30 min.

### Without LLM (fast, but scores cap at 75%):

```bash
python scripts/audit_rendered.py \
  --doc-root "$DOC_ROOT" \
  --json-dir "$DOC_ROOT" \
  --skip-llm
```

## Step 3: Review Results

Summary with all scores:

```bash
cat "$DOC_ROOT/results.json" | python -m json.tool | head -50
```

Per-document reports:

```bash
cat "$DOC_ROOT/<document-slug>/audit-report.json" | python -m json.tool
```

Get combined analysis
/usr/local/google/home/stonejiang/ada-compliance-engine/google/analysis.py


Get the full dir at: /usr/local/google/home/stonejiang/NCDIT-ADA-FILES/extraction_tests_03122026