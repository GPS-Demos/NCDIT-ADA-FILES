# NCDIT 100-Doc Batch Audit Report
**Date:** 2026-03-23
**Model:** gemini-3.1-pro-preview
**Branch:** fix/auditor-ncdit-320-improvements
**Workers:** 11 (all API keys)

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Documents processed | 99 (1 skipped — no extraction JSON) |
| Auto-approve | **4** (5.5%) |
| Human review | **51** (69.9%) |
| Reject | **18** (24.7%) |
| Excluded | **26** |
| Errors | **0** |
| Average score (non-excluded) | **78** |

---

## Routing Distribution

```
Auto-approve  ████                               4  (5.5%)
Human review  ████████████████████████████████   51  (69.9%)
Reject        ██████████████                     18  (24.7%)
```

**Excluding the 26 excluded docs, of the 73 scorable documents:**
- Auto-approve: 4 (5.5%)
- Human review: 51 (69.9%)
- Reject: 18 (24.7%)

---

## Auto-Approved Documents (4)

| Document | Score | Fidelity | Concerns |
|----------|-------|----------|----------|
| 20190814-nc-911-board-minutes-approved | 99 | 0.99 | 2 |
| federal-interagency-committee-agenda-20190516 | 100 | 1.00 | 1 |
| gicc-agenda-05-19-2021 | 100 | 1.00 | 1 |
| table-seal-imagery-diagram-1468 | 100 | 1.00 | 0 |

All auto-approved documents have fidelity >= 0.99 and <= 2 concerns.

---

## Rejected Documents (18)

### Hard Veto (V6) — 14 documents

All scored 30/Critical with fidelity = 0.40. Trigger: severe image/content corruption.

| Document | Concerns | Top Issues |
|----------|----------|------------|
| 20200522-nc911-board-minutes-approved | 8 | Fabricated contact info, lists corrupted, visual duplication |
| 911-education-committee-agenda-03-25-2021 | 14 | Images missing/broken, 37 displaced hyperlinks (worst in batch) |
| esrmo-newsletter-april-2017 | 7 | Images missing, image duplication |
| esrmo-newsletter-december-2018 | 8 | Images missing, content duplication |
| esrmo-newsletter-january-2017 | 6 | Images missing, visual duplication, displaced hyperlinks |
| ifb-its-400277-2017-1102-final | 12 | Link injection, reading order broken, lists corrupted |
| logo-tables-shading-watermark-photos | 9 | Link injection, low text recall (38%) |
| logos-graphic-colors-photos-icons-diagrams-charts-53e1 | 7 | Link injection, heading hierarchy broken, image duplication |
| logos-graphic-colors-table-screenshot-images | 10 | Images missing, lists corrupted, images misplaced |
| map-imagery-photos-tables-...0fb1 | 9 | Fabricated paragraphs, table corruption, visual duplication |
| map-imagery-photos-tables-...365a | 7 | Images missing, table corruption, displaced hyperlinks |
| map-imagery-photos-tables-i-e5cc | 8 | Images missing, text formatting lost, table captions as headers |
| nc-911-board-minutes-sep-30-2022 | 8 | Link injection, lists corrupted, table captions as headers |
| nc-911-board-monthly-dispatch-march-2025 | 6 | Complete section missing, images missing, hallucination risk |

### LLM Decider Rejects — 4 documents

| Document | Score | Fidelity | Concerns | Top Issues |
|----------|-------|----------|----------|------------|
| logo-imagery-screenshot-imagery-fca1 | 91 | 0.91 | 7 | All 8 hyperlinks lost, lists corrupted, visual duplication |
| long-contract-many-pages-of-tables | 93 | 0.93 | 15 | Table corruption, lists corrupted, page number artifacts |
| mostly-text-charts-tables-screenshots-maps | 86 | 0.86 | 10 | Table corruption, reading order broken, lists corrupted |
| seal-imagery-table-with-shading-colored-text | 92 | 0.92 | 10 | Table corruption, text formatting lost, 11 displaced hyperlinks |

---

## Excluded Documents (26)

| Category | Count |
|----------|-------|
| SLIDE_DECK | 24 |
| FORM | 1 |
| SINGLE_GRAPHIC | 1 |

All exclusions correctly identified by the Content Fidelity call (Call 1). Includes all `powerpoint-slides-*` docs, presentation decks, and specialized document types.

---

## Human Review Documents — Score Distribution

| Grade | Score Range | Count | % of Human Review |
|-------|-----------|-------|-------------------|
| Good (90-100) | 89-100 | 38 | 74.5% |
| Fair (60-79) | 60-79 | 13 | 25.5% |
| Poor (<60) | <60 | 0 | 0% |

### Top-Scoring Human Review (score >= 99)

| Document | Score | Fidelity | Concerns | Why Not Auto-Approved |
|----------|-------|----------|----------|----------------------|
| draft-addressnc-specifications | 100 | 1.00 | 2 | Header/footer, blue-styled text |
| gicc-2020-census-nc-factsheet | 100 | 1.00 | 2 | Header/footer, displaced hyperlinks |
| gicc-meeting-minutes-02122003 | 100 | 1.00 | 3 | Header/footer, displaced hyperlinks |
| gicc-meeting-minutes-08072007 | 100 | 1.00 | 4 | Header/footer (10 elements), displaced hyperlinks |
| gicc-mo-minutes-20191216 | 100 | 1.00 | 3 | Header/footer, displaced hyperlinks |
| multi-factor-auth-report-dec-2015 | 100 | 1.00 | 3 | Header/footer (14 elements), displaced hyperlinks |
| seal-image-table-6870 | 100 | 1.00 | 4 | Image/table concerns |
| text-some-colored-text-3638 | 100 | 1.00 | 4 | Visual concerns |
| 20190726-board-agenda | 99 | 0.99 | 3 | Header/footer, flattened sub-lists |
| draft-fy23-25-goals-priorities | 99 | 0.99 | 2 | Minor formatting |
| memo-with-links-1334 | 99 | 0.99 | 3 | Displaced hyperlinks, header/footer |

### Fair-Grade Human Review (score 60-79)

| Document | Score | Fidelity | Top Issues |
|----------|-------|----------|------------|
| agency-onboarding | 60 | 0.60 | Visual duplication, Content eval failed |
| colored-text-logos | 60 | 0.60 | 12 displaced hyperlinks, header/footer pollution |
| fillable-form-logo-imagery-bdfc | 60 | 0.60 | Header/footer retained, 15 form fields losing function |
| logo-imagery-graphic-colors-...-tables-4807 | 60 | 0.60 | Content eval failed |
| scanned-from-paper-many-pages-of-tables | 60 | 0.60 | Visual duplication, text formatting lost |
| 911-board-edu-committee-minutes-apr-2022 | 75 | 0.75 | Minor concerns |
| 911-board-tech-committee-agenda-jun-2022 | 75 | 0.75 | 8 concerns |
| appenc-initialdatalayers | 75 | 0.75 | Minor concerns |
| esrmo-newsletter-april-2024 | 75 | 0.75 | Image-related concerns |
| map-imagery-logo-imagery-4809 | 75 | 0.75 | Low text recall (35%), image duplication |
| scio-physical-and-environmental-protection | 75 | 0.75 | Minor concerns |
| seal-imagery-11ab | 75 | 0.75 | Visual concerns |

---

## Key Patterns & Observations

### 1. V6 Hard Veto is the Primary Rejection Mechanism
14 of 18 rejects (78%) triggered by `hard_veto:V6`. All share fidelity = 0.40 and score = 30. This veto fires on severe image/content corruption — a strong guardrail.

### 2. Defect Counts Show 0/0/0 Across All Reports
The `defects.critical/major/minor` fields are unpopulated in all 99 reports. Routing is entirely driven by:
- LLM fidelity composite score
- Programmatic concern detection
- LLM Final Decider judgment
- V6 hard veto

### 3. High-Score Rejects Indicate Concern-Driven Detection
4 documents rejected with scores 86-93 — the LLM decider catches issues (table corruption, lost hyperlinks) that the fidelity score alone would pass.

### 4. Header/Footer Concerns Prevent Auto-Approve
Most 100-score documents route to human_review due to header/footer retention or displaced hyperlinks. These are real concerns but may be overly aggressive for auto-approve gating.

### 5. ESRMO Newsletters Are Consistently Problematic
5 of 6 ESRMO newsletters either rejected (3) or scored Fair (1). Root cause: image-heavy layouts with complex formatting.

### 6. Document Exclusion Working Well
26 documents correctly classified as SLIDE_DECK (24), FORM (1), or SINGLE_GRAPHIC (1). No false exclusions observed. The fillable-form pair (bddf=FORM excluded, bdfc=not excluded, scored 60) shows appropriate differentiation.

---

## Concern Type Frequency (Top 10)

| Concern Type | Approx. Occurrences | Impact |
|-------------|---------------------|--------|
| Displaced hyperlinks | ~35+ docs | Links moved to wrong location |
| Header/footer retained | ~25+ docs | Source doc artifacts in output |
| Images missing/broken | ~15 docs | Visual content loss (triggers V6) |
| Text formatting not preserved | ~15 docs | Emphasis, color, styling lost |
| Table structure corrupted | ~12 docs | Rows/columns merged or split |
| Lists converted incorrectly | ~12 docs | Numbered/bulleted lists flattened |
| Content visually duplicated | ~10 docs | Repeated content blocks |
| Link injection | ~7 docs | Spurious hyperlinks added |
| Image duplication | ~6 docs | Same image rendered multiple times |
| Blue-styled text not linked | ~5 docs | Visual links without href |

---

## Recommendations

1. **Auto-approve rate is low (5.5%)** — Consider relaxing the decider's threshold for documents with score >= 95 and <= 3 minor concerns (header/footer, displaced hyperlinks)
2. **V6 veto is effective** — No false positives observed; keep as-is
3. **Defect count fields unpopulated** — Verify this is expected behavior or fix the defect counting logic
4. **ESRMO newsletters need investigation** — Consider if image-heavy newsletter layouts need special handling
5. **Header/footer detection is sensitive** — Many high-quality documents flagged for minor header/footer leakage that may not warrant human review
