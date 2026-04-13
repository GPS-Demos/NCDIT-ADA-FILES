# March 25, 2026 — Auditor V3 Batch Report

Generated: 2026-03-25 23:10 UTC
Branch: fix/auditor-improvements-v3
Model: gemini-3.1-pro-preview
Documents: 100

## Executive Summary

| Metric | Value |
|--------|-------|
| Documents Processed | 100 |
| Average Quality Score | 52.1 |
| Auto-Approve Rate | 22% (22/100) |
| Human Review | 24 (24%) |
| Reject | 24 (24%) |
| Excluded | 30 (30%) |

## Routing Breakdown

| Route | Count | % | Avg Score |
|-------|-------|---|-----------|
| Auto Approve | 22 | 22% | 100.0 |
| Human Review | 24 | 24% | 95.3 |
| Reject | 24 | 24% | 30.0 |
| Excluded | 30 | 30% | 0.0 |

## Exclusion Categories

| Category | Count |
|----------|-------|
| FORM | 3 |
| SINGLE_GRAPHIC | 2 |
| SLIDE_DECK | 25 |

## Fidelity Component Averages (non-excluded, n=70)

| Component | Average | Min | Max |
|-----------|---------|-----|-----|
| Content | 0.9748 | 0.0000 | 1.0000 |
| Structural | 0.9299 | 0.0000 | 1.0000 |
| Visual | 0.7633 | 0.1429 | 1.0000 |

## Defect Summary

| Severity | Count | Avg per Doc |
|----------|-------|-------------|
| Critical | 26 | 0.4 |
| Major | 52 | 0.7 |
| Minor | 21 | 0.3 |
| **Total Concerns** | **351** | **3.5** |
| Deduplicated | 15 | 0.1 |

## Day-over-Day Delta

| Metric | March 23 | March 24 | March 25 | Delta (24-25) |
|--------|----------|----------|----------|---------------|
| Documents | 99 | 100 | 100 | -- |
| Avg Score | 57.8 | 44.9 | 52.1 | +7.2 |
| Auto-Approve Rate | 4% | 13% | 22% | +9pp |
| Total Concerns | 376 | 472 | 351 | -121 |
| Deduplicated | 3 | 6 | 15 | +9 |
| Critical Defects | 0 | 35 | 26 | -9 |
| Major Defects | 0 | 87 | 52 | -35 |
| Rejects | 18 | 27 | 24 | -3 |

## Changes in This Patch (fix/auditor-improvements-v3)

### Bug Fixes
1. **Missing LLM-Programmatic Equivalences** -- Added 14 new entries covering S7 (link detectors), V2 (corrupt images), S3 (table headers), and S5 (list structure) programmatic detectors. Prevents duplicate concerns from inflating the Final Decider input.

2. **Post-Dedup Composite Knockout Cap** -- Replaced simple weighted mean with knockout-cap-aware recompute in dedup adjustment. Ensures post-dedup composite score correctly applies critical_veto, dimension_zero, and other knockout caps.

3. **Merge Conservative Penalty** (from Wave 2) -- When one structural sub-call fails, adds MAJOR penalty per missing check (5pts each) instead of marking as complete with inflated score.

4. **Classification Hints Double-Counting** (from Wave 2) -- Tables count cell text OR item text, not both, fixing word count inflation.

5. **S7/S8 Dedup Equivalence** (from Wave 2) -- Added S7/S8 to cross-call equivalences to prevent double-counting broken links across the two structural sub-calls.

### Prompt Improvements
6. **C7 Underline Pattern** -- Added underline as visual emphasis pattern (3rd case) -- no markdown representation means no false positive risk.

7. **Form Detection Expansion** -- Added: please print, fill in, complete this form, applicant, employer identification, checkbox variants.

8. **Watermark Preservation Note** -- V3 prompt notes text watermarks (DRAFT, CONFIDENTIAL) may be meaningful for government documents.

## Auto-Approved Documents

- **20190814-nc-911-board-minutes-approved-685f9d99** -- Score: 100
- **911-telecommunicators-resolution-rockingham-county-685f6ff5** -- Score: 100
- **cyber-incident-reporting-north-carolina-state-government-686b1b59** -- Score: 100
- **draft-fy23-25-goals-and-priorities-685fc8b0** -- Score: 100
- **esrmo-newsletter-april-2024-686b1c64** -- Score: 100
- **esrmo-newsletter-january-2017-686b1f87** -- Score: 100
- **esrmo-newsletter-july-2021-686b1e10** -- Score: 100
- **esrmo-newsletter-march-2018-686b1f23** -- Score: 100
- **federal-interagency-committee-agenda20190516-68614dc2** -- Score: 100
- **gicc-agenda-20200506-68839aed** -- Score: 100
- **gicc-goals-2021-2023-discussion-68612ed7** -- Score: 100
- **gicc-meeting-minutes-02122003-685fb099** -- Score: 100
- **gicc-meeting-minutes-08072007-685fb034** -- Score: 100
- **memo-with-links-1334** -- Score: 100
- **multi-factor-authentication-report-december-2015-68613ee4** -- Score: 100
- **scanned-from-paper-many-pages-of-tables-6878** -- Score: 100
- **screenshot-images-11b5** -- Score: 100
- **seal-image-table-6870** -- Score: 100
- **seal-imagery-11ab** -- Score: 100
- **standards-committee-meeting-agenda-packet-october-7-2021-685fa26e** -- Score: 100
- **text-background-colors-53e2** -- Score: 100
- **text-some-colored-text-3638** -- Score: 100

## Rejected Documents

- **911-education-committee-meeting-agenda-packet-03-25-2021-685f9fa9** -- Score: 29, Critical: 1, Major: 0
- **20200522-nc911-board-minutes-approved-685f9cb7** -- Score: 30, Critical: 1, Major: 3
- **911-board-technology-committee-agenda-june-9-2022-685fa07f** -- Score: 30, Critical: 1, Major: 1
- **agency-onboarding-68607a87** -- Score: 30, Critical: 1, Major: 0
- **esrmo-newsletter-april-2017-686b1f74** -- Score: 30, Critical: 1, Major: 0
- **esrmo-newsletter-december-2018-686b1ee1** -- Score: 30, Critical: 1, Major: 0
- **esrmo-newsletter-september-2021-686b1e03** -- Score: 30, Critical: 1, Major: 1
- **gicc-2020-census-nc-factsheet-20170809-686131e8** -- Score: 30, Critical: 1, Major: 0
- **gicc-agenda-20160810-68613387** -- Score: 30, Critical: 1, Major: 1
- **logo-imagery-screenshot-imagery-fca1** -- Score: 30, Critical: 1, Major: 0
- **logo-tables-shading-watermark-photos-13a3** -- Score: 30, Critical: 1, Major: 0
- **logos-graphic-colors-photos-icons-diagrams-charts-53de** -- Score: 30, Critical: 1, Major: 0
- **logos-graphic-colors-photos-icons-diagrams-charts-53e1** -- Score: 30, Critical: 1, Major: 1
- **logos-graphic-colors-table-screenshot-images-fc98** -- Score: 30, Critical: 1, Major: 0
- **long-contract-many-pages-of-tables-6881** -- Score: 30, Critical: 1, Major: 1
- **map-imagery-logo-imagery-4809** -- Score: 30, Critical: 1, Major: 0
- **map-imagery-photos-tables-screenshots-diagrams-data-charts-0fb1** -- Score: 30, Critical: 1, Major: 1
- **map-imagery-photos-tables-screenshots-diagrams-data-charts-365a** -- Score: 30, Critical: 1, Major: 1
- **map-imagery-photos-tables-screenshots-diagrams-data-charts-i-e5cc** -- Score: 30, Critical: 1, Major: 2
- **nc-911-board-education-committee-meeting-agenda-packet-feb-685f9e81** -- Score: 30, Critical: 1, Major: 1
- **nc-911-board-monthly-dispatch-march-2025-685f7179** -- Score: 30, Critical: 1, Major: 0
- **newsletter-with-many-images-and-formatted-text-117c** -- Score: 30, Critical: 1, Major: 1
- **newsletter-with-many-images-and-formatted-text-21fb** -- Score: 30, Critical: 1, Major: 0
- **table-seal-imagery-diagram-1468** -- Score: 30, Critical: 1, Major: 0
