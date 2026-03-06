# NCDIT 100-Doc Pipeline Report
**Batch**: ncdit-audit-20260306-155358
**Date**: 2026-03-06
**Branch**: fix/edge-cases (post Fix B + C + D)
**Fixes Applied**: Flatten subsections (B), Post-merge section/image dedup (C), Table row-count validation (D)
**Total PDFs**: 100 (93 succeeded, 7 timed out)
**Total Time**: 79 min across 10 GCP projects

## Pipeline Routing

| needs_retry | 41 | 44% |
| auto_approve | 32 | 34% |
| flag_for_review | 20 | 21% |
| failed | 1 | 1% |

## Confidence Scores

- **Mean**: 96.9%
- **Min**: 87.0%
- **Max**: 100.0%

| Range | Count |
|-------|-------|
| 99-100% | 35 |
| 95-98% | 42 |
| 90-94% | 14 |
| 85-89% | 2 |
| <85% | 0 |

## Word Coverage (gemini/baseline)

- **Mean** (excl scanned outliers): 0.98
- **Docs under 50%**: 1

| Document | Word Ratio |
|----------|-----------|
| draft-addressnc-specifications-20210811-68610610.pdf | 0.39 |

## Table Extraction

- **Docs with tables**: 43
- **Severe mismatch (<50%)**: 7

| Document | Baseline | Gemini | Ratio |
|----------|----------|--------|-------|
| logo-imagery-graphic-colors-map-imagery-f80b.pdf | 3 | 0 | 0% |
| ncom-update-gicc-05-15-2014-68612fe6.pdf | 3 | 0 | 0% |
| powerpoint-slides-1793.pdf | 1 | 0 | 0% |
| esrmo-newsletter-september-2021-686b1e03.pdf | 11 | 1 | 9% |
| 20200522-nc911-board-minutes-approved-685f9cb7.pdf | 4 | 1 | 25% |
| logos-graphic-colors-photos-icons-diagrams-charts-53e1.pdf | 12 | 3 | 25% |
| draft-addressnc-specifications-20210811-68610610.pdf | 11 | 3 | 27% |

## Edge Case Flags

| Flag | Count |
|------|-------|
| image_resolution_issue | 45 |
| many_images | 17 |
| complex_tables | 9 |
| table_extraction_mismatch | 7 |
| scanned_document | 5 |
| chunk_conversion_failure | 1 |

## Bottom 10 by Accuracy

| Document | Accuracy | Word Ratio | Confidence | Routing |
|----------|----------|-----------|------------|---------|
| appenc-initialdatalayers-685fad7d.pdf | 0.46 | 2.66 | 93% | flag_for_review |
| draft-addressnc-specifications-20210811-68610610.pdf | 0.53 | 0.39 | 88% | flag_for_review |
| scanned-from-paper-many-pages-of-tables-6878.pdf | 0.70 | 0.55 | 93% | flag_for_review |
| 20200522-nc911-board-minutes-approved-685f9cb7.pdf | 0.71 | 0.73 | 94% | needs_retry |
| logo-imagery-screenshot-imagery-fca1.pdf | 0.83 | 0.69 | 97% | flag_for_review |
| powerpoint-slides-f832.pdf | 0.85 | 0.85 | 95% | needs_retry |
| nc-911-board-technology-committee-minutes-nov-4-2021-685fa41d.pdf | 0.85 | 0.86 | 97% | needs_retry |
| powerpoint-slides-1793.pdf | 0.87 | 0.94 | 90% | flag_for_review |
| table-seal-imagery-diagram-1468.pdf | 0.87 | 0.89 | 95% | needs_retry |
| 911-board-technology-committee-agenda-june-9-2022-685fa07f.pdf | 0.87 | 0.86 | 96% | needs_retry |

## Top 10 by Accuracy

| Document | Accuracy | Word Ratio | Confidence | Routing |
|----------|----------|-----------|------------|---------|
| 10-22-20-edu-committee-agenda-packet-685f9fde.pdf | 1.00 | 0.92 | 99% | needs_retry |
| 20190416-nc-911-board-minutes-approved-687248c4.pdf | 1.00 | 0.96 | 99% | needs_retry |
| 20190726-board-agenda-685f9db9.pdf | 1.00 | 0.92 | 100% | auto_approve |
| 20190814-nc-911-board-minutes-approved-685f9d99.pdf | 1.00 | 0.94 | 100% | auto_approve |
| 20200522-board-agenda-685f9ca8.pdf | 1.00 | 0.97 | 99% | auto_approve |
| 911-board-education-committee-meeting-minutes-april-21-2022-685f9f9d.pdf | 1.00 | 0.92 | 99% | needs_retry |
| 911-telecommunicators-resolution-mitchell-county-685f6fd1.pdf | 1.00 | 245.00 | 100% | auto_approve |
| 911-telecommunicators-resolution-rockingham-county-685f6ff5.pdf | 1.00 | 243.00 | 100% | auto_approve |
| agency-onboarding-68607a87.pdf | 1.00 | 174.00 | 100% | auto_approve |
| colored-text-logos-676a.pdf | 1.00 | 0.92 | 99% | auto_approve |

## All Documents

| # | Document | Accuracy | Words | Conf | Routing | Flags |
|---|----------|----------|-------|------|---------|-------|
| 1 | 10-22-20-edu-committee-agenda-packet-685f9fde.pdf | 1.00 | 0.92 | 99% | needs_retry | complex_tables |
| 2 | 2019-20-smac-work-plan-685fadcf.pdf | 0.94 | 0.89 | 98% | flag_for_review | — |
| 3 | 20190416-nc-911-board-minutes-approved-687248c4.pdf | 1.00 | 0.96 | 99% | needs_retry | — |
| 4 | 20190726-board-agenda-685f9db9.pdf | 1.00 | 0.92 | 100% | auto_approve | — |
| 5 | 20190814-nc-911-board-minutes-approved-685f9d99.pdf | 1.00 | 0.94 | 100% | auto_approve | — |
| 6 | 20200522-board-agenda-685f9ca8.pdf | 1.00 | 0.97 | 99% | auto_approve | — |
| 7 | 20200522-nc911-board-minutes-approved-685f9cb7.pdf | 0.71 | 0.73 | 94% | needs_retry | table_extraction_mismatch |
| 8 | 208m-endpoint-reseller-price-list-686b18db.pdf | 0.94 | 1.76 | 96% | flag_for_review | image_resolution_issue |
| 9 | 911-board-education-committee-meeting-minutes-april-21-2022-685f9f9d.pdf | 1.00 | 0.92 | 99% | needs_retry | — |
| 10 | 911-board-technology-committee-agenda-june-9-2022-685fa07f.pdf | 0.87 | 0.86 | 96% | needs_retry | image_resolution_issue |
| 11 | 911-telecommunicators-resolution-mitchell-county-685f6fd1.pdf | 1.00 | 245.00 | 100% | auto_approve | scanned_document |
| 12 | 911-telecommunicators-resolution-rockingham-county-685f6ff5.pdf | 1.00 | 243.00 | 100% | auto_approve | scanned_document |
| 13 | agency-onboarding-68607a87.pdf | 1.00 | 174.00 | 100% | auto_approve | scanned_document |
| 14 | appenc-initialdatalayers-685fad7d.pdf | 0.46 | 2.66 | 93% | flag_for_review | — |
| 15 | colored-text-logos-676a.pdf | 1.00 | 0.92 | 99% | auto_approve | — |
| 16 | create-beautiful-sharepoint-sites-685fb98c.pdf | 1.00 | 0.98 | 100% | auto_approve | image_resolution_issue |
| 17 | cyber-incident-reporting-north-carolina-state-government-686b1b59.pdf | 0.99 | 0.98 | 100% | auto_approve | — |
| 18 | draft-addressnc-specifications-20210811-68610610.pdf | 0.53 | 0.39 | 88% | flag_for_review | many_images, complex_tables, table_extraction_mismatch |
| 19 | draft-fy23-25-goals-and-priorities-685fc8b0.pdf | 0.97 | 0.98 | 99% | needs_retry | — |
| 20 | esrmo-newsletter-april-2017-686b1f74.pdf | 1.00 | 1.00 | 97% | auto_approve | image_resolution_issue |
| 21 | esrmo-newsletter-april-2024-686b1c64.pdf | 0.97 | 1.00 | 98% | flag_for_review | image_resolution_issue |
| 22 | esrmo-newsletter-december-2018-686b1ee1.pdf | 0.99 | 0.98 | 99% | needs_retry | — |
| 23 | esrmo-newsletter-january-2017-686b1f87.pdf | 0.99 | 0.98 | 100% | auto_approve | — |
| 24 | esrmo-newsletter-july-2021-686b1e10.pdf | 0.98 | 1.28 | 96% | needs_retry | image_resolution_issue |
| 25 | esrmo-newsletter-march-2018-686b1f23.pdf | 0.99 | 0.98 | 99% | auto_approve | image_resolution_issue |
| 26 | esrmo-newsletter-september-2021-686b1e03.pdf | 0.93 | 0.99 | 97% | needs_retry | complex_tables, image_resolution_issue, table_extraction_mismatch |
| 27 | federal-interagency-committee-agenda20190516-68614dc2.pdf | 1.00 | 1.00 | 98% | needs_retry | — |
| 28 | federalagencyhurricanecoordination-686132f8.pdf | 0.95 | 0.96 | 96% | flag_for_review | many_images, image_resolution_issue |
| 29 | fillable-form-logo-imagery-bddf.pdf | 1.00 | 0.99 | 95% | flag_for_review | — |
| 30 | fillable-form-logo-imagery-bdfc.pdf | 1.00 | 0.99 | 97% | auto_approve | — |
| 31 | gdac-legislative-report-may-2016-68610a4b.pdf | 0.92 | 0.93 | 95% | flag_for_review | — |
| 32 | gicc-2020-census-nc-factsheet-20170809-686131e8.pdf | 0.97 | 1.19 | 96% | needs_retry | image_resolution_issue |
| 33 | gicc-agenda-05-19-2021-68611645.pdf | 1.00 | 1.00 | 95% | needs_retry | — |
| 34 | gicc-agenda-20160810-68613387.pdf | 1.00 | 1.00 | 100% | auto_approve | — |
| 35 | gicc-agenda-20200506-68839aed.pdf | 1.00 | 1.00 | 100% | auto_approve | — |
| 36 | gicc-goals-2021-2023-discussion-68612ed7.pdf | 0.94 | 1.00 | 99% | needs_retry | — |
| 37 | gicc-goals-and-strategic-direction-2021-23-685fd67f.pdf | 1.00 | 0.99 | 98% | needs_retry | complex_tables, image_resolution_issue |
| 38 | gicc-lgc-censussurveyresults-20200506-68839ae8.pdf | 0.93 | 0.94 | 96% | flag_for_review | many_images, image_resolution_issue |
| 39 | gicc-meeting-minutes-02122003-685fb099.pdf | 1.00 | 0.98 | 99% | needs_retry | — |
| 40 | gicc-meeting-minutes-08072007-685fb034.pdf | 1.00 | 0.99 | 100% | auto_approve | — |
| 41 | gicc-mo-minutes-20191216-68614cc3.pdf | 1.00 | 1.00 | 100% | auto_approve | — |
| 42 | gicc-ncdot-florence-20181107-68614eed.pdf | 1.00 | 1.05 | 97% | needs_retry | image_resolution_issue |
| 43 | gicc-smac-agenda-20210120-68839aac.pdf | 1.00 | 0.91 | 98% | flag_for_review | — |
| 44 | gicc-tims-may-2016-686133f1.pdf | 0.88 | 0.78 | 96% | flag_for_review | image_resolution_issue |
| 45 | logo-imagery-graphic-colors-map-imagery-6e2e.pdf | 0.93 | 1.82 | 99% | needs_retry | image_resolution_issue |
| 46 | logo-imagery-graphic-colors-map-imagery-f80b.pdf | 0.88 | 0.93 | 92% | needs_retry | image_resolution_issue, table_extraction_mismatch |
| 47 | logo-imagery-graphic-colors-map-imagery-tables-4807.pdf | 0.95 | 8.00 | 100% | auto_approve | scanned_document |
| 48 | logo-imagery-screenshot-imagery-fca1.pdf | 0.83 | 0.69 | 97% | flag_for_review | image_resolution_issue |
| 49 | logo-tables-shading-watermark-photos-13a3.pdf | 0.93 | 0.92 | 92% | flag_for_review | many_images, image_resolution_issue |
| 50 | logos-graphic-colors-photos-icons-diagrams-charts-53de.pdf | 1.00 | 0.97 | 100% | auto_approve | image_resolution_issue |
| 51 | logos-graphic-colors-photos-icons-diagrams-charts-53e1.pdf | 0.94 | 0.92 | 93% | needs_retry | complex_tables, image_resolution_issue, table_extraction_mismatch |
| 52 | logos-graphic-colors-table-screenshot-images-fc98.pdf | 0.90 | 0.82 | 98% | needs_retry | image_resolution_issue |
| 53 | map-imagery-logo-imagery-4809.pdf | 1.00 | 0.99 | 100% | auto_approve | — |
| 54 | map-imagery-logo-imagery-f810.pdf | 1.00 | 0.99 | 100% | auto_approve | — |
| 55 | map-imagery-photos-tables-screenshots-diagrams-data-charts-0fb1.pdf | 0.95 | 0.90 | 93% | needs_retry | many_images, complex_tables, image_resolution_issue |
| 56 | map-imagery-photos-tables-screenshots-diagrams-data-charts-365a.pdf | 0.99 | 0.93 | 96% | needs_retry | image_resolution_issue |
| 57 | map-imagery-photos-tables-screenshots-diagrams-data-charts-ff40.pdf | 0.96 | 0.99 | 91% | needs_retry | many_images, image_resolution_issue |
| 58 | map-imagery-photos-tables-screenshots-diagrams-data-charts-i-e5cc.pdf | 0.96 | 0.92 | 91% | needs_retry | many_images, complex_tables, image_resolution_issue |
| 59 | map-imagery-photos-tables-screenshots-diagrams-data-charts-i-f7f6.pdf | 0.95 | 0.96 | 95% | needs_retry | many_images, image_resolution_issue |
| 60 | memo-with-links-1334.pdf | 1.00 | 0.98 | 94% | needs_retry | — |
| 61 | mo-minutes-20160620-686133d2.pdf | 1.00 | 0.99 | 100% | auto_approve | — |
| 62 | mostly-text-charts-tables-screenshots-maps-67fb.pdf | 1.00 | 0.93 | 98% | needs_retry | — |
| 63 | multi-factor-authentication-report-december-2015-68613ee4.pdf | 1.00 | 0.92 | 97% | auto_approve | — |
| 64 | nc-911-board-education-committee-meeting-agenda-packet-feb-685f9e81.pdf | 0.93 | 0.95 | 97% | flag_for_review | image_resolution_issue |
| 65 | nc-911-board-meeting-agenda-aug-26-2022-685f9a31.pdf | 1.00 | 0.92 | 98% | needs_retry | — |
| 66 | nc-911-board-minutes-september-30-2022-685f9a2b.pdf | N/A | N/A | N/A | failed | — |
| 67 | nc-911-board-monthly-dispatch-march-2025-685f7179.pdf | 1.00 | 2209.00 | 99% | auto_approve | scanned_document, image_resolution_issue |
| 68 | nc-911-board-technology-committee-minutes-nov-4-2021-685fa41d.pdf | 0.85 | 0.86 | 97% | needs_retry | — |
| 69 | ncom-update-gicc-05-15-2014-68612fe6.pdf | 0.93 | 0.97 | 91% | flag_for_review | table_extraction_mismatch |
| 70 | near-perfect-powerpoint-slides-by-accessibility-experts-47b0.pdf | 1.00 | 0.92 | 87% | needs_retry | many_images, image_resolution_issue |
| 71 | near-perfect-powerpoint-slides-by-accessibility-experts-47b2.pdf | 0.94 | 0.88 | 98% | needs_retry | image_resolution_issue |
| 72 | newsletter-with-many-images-and-formatted-text-117c.pdf | 1.00 | 0.94 | 100% | auto_approve | image_resolution_issue |
| 73 | newsletter-with-many-images-and-formatted-text-21fb.pdf | 0.98 | 1.08 | 99% | auto_approve | many_images, image_resolution_issue |
| 74 | powerpoint-slides-1793.pdf | 0.87 | 0.94 | 90% | flag_for_review | many_images, image_resolution_issue, table_extraction_mismatch |
| 75 | powerpoint-slides-f832.pdf | 0.85 | 0.85 | 95% | needs_retry | many_images, image_resolution_issue |
| 76 | powerpoint-slides-fed0.pdf | 1.00 | 0.94 | 99% | auto_approve | image_resolution_issue |
| 77 | powerpoint-slides-feef.pdf | 1.00 | 0.97 | 95% | auto_approve | image_resolution_issue |
| 78 | powerpoint-slides-fef1.pdf | 0.97 | 0.97 | 96% | flag_for_review | many_images, image_resolution_issue |
| 79 | powerpoint-slides-fef5.pdf | 0.91 | 0.89 | 97% | flag_for_review | many_images, image_resolution_issue |
| 80 | powerpoint-slides-ff0a.pdf | 1.00 | 1.00 | 98% | needs_retry | image_resolution_issue |
| 81 | powerpoint-slides-ff0c.pdf | 0.95 | 0.93 | 93% | needs_retry | many_images, image_resolution_issue |
| 82 | powerpoint-slides-ff0d.pdf | 0.96 | 0.96 | 96% | needs_retry | many_images, image_resolution_issue |
| 83 | scanned-from-paper-many-pages-of-tables-6878.pdf | 0.70 | 0.55 | 93% | flag_for_review | complex_tables, chunk_conversion_failure |
| 84 | scio-physical-and-environmental-protection-686b1b84.pdf | 0.89 | 0.99 | 93% | needs_retry | — |
| 85 | screenshot-images-11b5.pdf | 1.00 | 1.00 | 100% | auto_approve | image_resolution_issue |
| 86 | seal-image-table-6870.pdf | 1.00 | 0.98 | 98% | needs_retry | — |
| 87 | seal-imagery-table-with-shading-132c.pdf | 0.98 | 0.92 | 97% | needs_retry | complex_tables, image_resolution_issue |
| 88 | smac-lidar-apr-10-2024-6860db7b.pdf | 1.00 | 5.41 | 95% | flag_for_review | — |
| 89 | standards-committee-meeting-agenda-packet-october-7-2021-685fa26e.pdf | 0.98 | 1.03 | 99% | auto_approve | — |
| 90 | table-seal-imagery-diagram-1468.pdf | 0.87 | 0.89 | 95% | needs_retry | — |
| 91 | text-background-colors-53e2.pdf | 1.00 | 0.96 | 97% | auto_approve | — |
| 92 | text-some-colored-text-3638.pdf | 1.00 | 0.94 | 100% | auto_approve | — |
| 93 | wearencgov-broadbandinitiatives-685fc6d1.pdf | 0.94 | 0.94 | 97% | needs_retry | many_images, image_resolution_issue |
| 94 | wearencgov-presentation3-685fc6b2.pdf | 0.99 | 0.90 | 98% | needs_retry | image_resolution_issue |

---
*Report generated automatically from pipeline result.json files.*
*Auditor scores (fidelity + quality gate) will be added separately.*