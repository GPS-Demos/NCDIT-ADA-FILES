# NCDIT Audit Batch — ncdit-audit-20260304-064702

**Date**: 2026-03-04 07:42 UTC
**Total PDFs**: 100
**Success Rate**: 82/100 (82%)
**Total Time**: 3311s (55.2min)

---

## Target Documents (Fix Validation)

| Document | Expected Fix | Routing | Confidence | Flags | Status |
|----------|-------------|---------|------------|-------|--------|
| nc-911-board-monthly-dispatch | Fix 1+3: chunk placeholders + scanned scoring | flag_for_review | 94% | scanned_document, image_resolution_issue, chunk_conversion_failure | PASS |
| gicc-mo-minutes-20191216 | Fix 2: one-match link injection | N/A | N/A | none | FAIL: Gemini API error after 3 attempts: Gemini API call |
| multi-factor-authentication-report | Fix 3: scanned doc scoring | auto_approve | 95% | none | PASS |
| gicc-agenda-20160810 | Structural (Noah's scope) | auto_approve | 100% | none | PASS |
| mo-minutes-20160620 | Structural (Noah's scope) | auto_approve | 100% | none | PASS |

---

## All Results

| # | Filename | Routing | Confidence | Flags | Duration | Project |
|---|----------|---------|------------|-------|----------|---------|
| 1 | 10-22-20-edu-committee-agenda-packet-685f9fde | auto_approve | 94% | complex_tables | 362s | P1 |
| 2 | 2019-20-smac-work-plan-685fadcf | auto_approve | 100% | — | 115s | P2 |
| 3 | 20190416-nc-911-board-minutes-approved-687248c4 | needs_retry | 98% | — | 58s | P3 |
| 4 | 20190726-board-agenda-685f9db9 | flag_for_review | 98% | — | 61s | P4 |
| 5 | 20190814-nc-911-board-minutes-approved-685f9d99 | auto_approve | 99% | — | 20s | P5 |
| 6 | 20200522-board-agenda-685f9ca8 | auto_approve | 100% | — | 158s | P6 |
| 7 | 20200522-nc911-board-minutes-approved-685f9cb7 | N/A | N/A | — | 76s | P7 |
| 8 | 208m-endpoint-reseller-price-list-686b18db | N/A | N/A | — | 600s | P8 |
| 9 | 911-board-education-committee-meeting-minutes-apri | auto_approve | 99% | — | 142s | P9 |
| 10 | 911-board-technology-committee-agenda-june-9-2022- | needs_retry | 96% | — | 229s | P10 |
| 11 | 911-education-committee-meeting-agenda-packet-03-2 | N/A | N/A | — | 600s | P1 |
| 12 | 911-telecommunicators-resolution-mitchell-county-6 | auto_approve | 100% | scanned_document | 48s | P2 |
| 13 | 911-telecommunicators-resolution-rockingham-county | auto_approve | 100% | scanned_document | 28s | P3 |
| 14 | agency-onboarding-68607a87 | auto_approve | 100% | scanned_document | 44s | P4 |
| 15 | appenc-initialdatalayers-685fad7d | flag_for_review | 94% | — | 86s | P5 |
| 16 | colored-text-logos-676a | auto_approve | 99% | — | 79s | P6 |
| 17 | create-beautiful-sharepoint-sites-685fb98c | auto_approve | 99% | image_resolution_issue | 116s | P7 |
| 18 | cyber-incident-reporting-north-carolina-state-gove | auto_approve | 100% | — | 38s | P8 |
| 19 | draft-addressnc-specifications-20210811-68610610 | flag_for_review | 90% | many_images, complex_tables, table_extraction_mismatch, chunk_conversion_failure | 204s | P9 |
| 20 | draft-fy23-25-goals-and-priorities-685fc8b0 | needs_retry | 99% | — | 61s | P10 |
| 21 | esrmo-newsletter-april-2017-686b1f74 | auto_approve | 100% | image_resolution_issue | 82s | P1 |
| 22 | esrmo-newsletter-april-2024-686b1c64 | flag_for_review | 98% | image_resolution_issue | 69s | P2 |
| 23 | esrmo-newsletter-december-2018-686b1ee1 | needs_retry | 97% | — | 96s | P3 |
| 24 | esrmo-newsletter-january-2017-686b1f87 | auto_approve | 100% | — | 53s | P4 |
| 25 | esrmo-newsletter-july-2021-686b1e10 | needs_retry | 96% | image_resolution_issue | 68s | P5 |
| 26 | esrmo-newsletter-march-2018-686b1f23 | auto_approve | 99% | image_resolution_issue | 82s | P6 |
| 27 | esrmo-newsletter-september-2021-686b1e03 | needs_retry | 97% | complex_tables, image_resolution_issue, table_extraction_mismatch | 87s | P7 |
| 28 | federal-interagency-committee-agenda20190516-68614 | needs_retry | 98% | — | 19s | P8 |
| 29 | federalagencyhurricanecoordination-686132f8 | needs_retry | 95% | many_images, image_resolution_issue | 75s | P9 |
| 30 | fillable-form-logo-imagery-bddf | needs_retry | 94% | — | 53s | P10 |
| 31 | fillable-form-logo-imagery-bdfc | auto_approve | 99% | — | 19s | P1 |
| 32 | gdac-legislative-report-may-2016-68610a4b | flag_for_review | 95% | — | 234s | P2 |
| 33 | gicc-2020-census-nc-factsheet-20170809-686131e8 | needs_retry | 92% | image_resolution_issue, table_extraction_mismatch | 28s | P3 |
| 34 | gicc-agenda-05-19-2021-68611645 | needs_retry | 99% | — | 44s | P4 |
| 35 | gicc-agenda-20160810-68613387 | auto_approve | 100% | — | 45s | P5 |
| 36 | gicc-agenda-20200506-68839aed | auto_approve | 100% | — | 54s | P6 |
| 37 | gicc-goals-2021-2023-discussion-68612ed7 | needs_retry | 99% | — | 33s | P7 |
| 38 | gicc-goals-and-strategic-direction-2021-23-685fd67 | needs_retry | 96% | complex_tables, image_resolution_issue | 92s | P8 |
| 39 | gicc-lgc-censussurveyresults-20200506-68839ae8 | N/A | N/A | — | 120s | P9 |
| 40 | gicc-meeting-minutes-02122003-685fb099 | needs_retry | 99% | — | 73s | P10 |
| 41 | gicc-meeting-minutes-08072007-685fb034 | auto_approve | 100% | — | 81s | P1 |
| 42 | gicc-mo-minutes-20191216-68614cc3 | N/A | N/A | — | 53s | P2 |
| 43 | gicc-ncdot-florence-20181107-68614eed | flag_for_review | 93% | image_resolution_issue | 72s | P3 |
| 44 | gicc-smac-agenda-20210120-68839aac | flag_for_review | 98% | — | 32s | P4 |
| 45 | gicc-tims-may-2016-686133f1 | needs_retry | 97% | image_resolution_issue | 175s | P5 |
| 46 | ifb-its-400277-2017-1102-final-686b18e9 | N/A | N/A | — | 600s | P6 |
| 47 | logo-imagery-graphic-colors-map-imagery-6e2e | flag_for_review | 97% | image_resolution_issue | 15s | P7 |
| 48 | logo-imagery-graphic-colors-map-imagery-f80b | needs_retry | 92% | image_resolution_issue, table_extraction_mismatch | 39s | P8 |
| 49 | logo-imagery-graphic-colors-map-imagery-tables-480 | auto_approve | 100% | scanned_document | 33s | P9 |
| 50 | logo-imagery-screenshot-imagery-fca1 | N/A | N/A | — | 51s | P10 |
| 51 | logo-tables-shading-watermark-photos-13a3 | N/A | N/A | — | 600s | P1 |
| 52 | logos-graphic-colors-photos-icons-diagrams-charts- | needs_retry | 96% | image_resolution_issue | 338s | P2 |
| 53 | logos-graphic-colors-photos-icons-diagrams-charts- | N/A | N/A | — | 600s | P3 |
| 54 | logos-graphic-colors-table-screenshot-images-fc98 | needs_retry | 89% | image_resolution_issue | 93s | P4 |
| 55 | long-contract-many-pages-of-tables-6881 | N/A | N/A | — | 600s | P5 |
| 56 | map-imagery-logo-imagery-4809 | auto_approve | 100% | — | 30s | P6 |
| 57 | map-imagery-logo-imagery-f810 | auto_approve | 100% | — | 28s | P7 |
| 58 | map-imagery-photos-tables-screenshots-diagrams-dat | flag_for_review | 92% | many_images, complex_tables, image_resolution_issue | 534s | P8 |
| 59 | map-imagery-photos-tables-screenshots-diagrams-dat | needs_retry | 88% | image_resolution_issue | 331s | P9 |
| 60 | map-imagery-photos-tables-screenshots-diagrams-dat | flag_for_review | 88% | many_images, image_resolution_issue, table_extraction_mismatch, chunk_conversion_failure | 115s | P10 |
| 61 | map-imagery-photos-tables-screenshots-diagrams-dat | N/A | N/A | — | 600s | P1 |
| 62 | map-imagery-photos-tables-screenshots-diagrams-dat | needs_retry | 92% | many_images, image_resolution_issue | 321s | P2 |
| 63 | memo-with-links-1334 | needs_retry | 98% | — | 45s | P3 |
| 64 | mo-minutes-20160620-686133d2 | auto_approve | 100% | — | 120s | P4 |
| 65 | mostly-text-charts-tables-screenshots-maps-67fb | N/A | N/A | — | 600s | P5 |
| 66 | multi-factor-authentication-report-december-2015-6 | auto_approve | 95% | — | 145s | P6 |
| 67 | nc-911-board-education-committee-meeting-agenda-pa | flag_for_review | 93% | image_resolution_issue | 99s | P7 |
| 68 | nc-911-board-meeting-agenda-aug-26-2022-685f9a31 | needs_retry | 98% | — | 115s | P8 |
| 69 | nc-911-board-minutes-september-30-2022-685f9a2b | flag_for_review | 97% | — | 134s | P9 |
| 70 | nc-911-board-monthly-dispatch-march-2025-685f7179 | flag_for_review | 94% | scanned_document, image_resolution_issue, chunk_conversion_failure | 356s | P10 |
| 71 | nc-911-board-technology-committee-minutes-nov-4-20 | flag_for_review | 99% | — | 268s | P1 |
| 72 | ncom-update-gicc-05-15-2014-68612fe6 | flag_for_review | 91% | table_extraction_mismatch | 36s | P2 |
| 73 | near-perfect-powerpoint-slides-by-accessibility-ex | needs_retry | 98% | many_images, image_resolution_issue | 335s | P3 |
| 74 | near-perfect-powerpoint-slides-by-accessibility-ex | flag_for_review | 96% | image_resolution_issue, chunk_conversion_failure | 187s | P4 |
| 75 | newsletter-with-many-images-and-formatted-text-117 | auto_approve | 100% | image_resolution_issue | 73s | P5 |
| 76 | newsletter-with-many-images-and-formatted-text-21f | N/A | N/A | — | 600s | P6 |
| 77 | powerpoint-slides-1793 | flag_for_review | 83% | many_images, image_resolution_issue, table_extraction_mismatch | 376s | P7 |
| 78 | powerpoint-slides-f832 | flag_for_review | 91% | many_images, image_resolution_issue, table_extraction_mismatch | 327s | P8 |
| 79 | powerpoint-slides-fed0 | auto_approve | 98% | image_resolution_issue | 122s | P9 |
| 80 | powerpoint-slides-feef | needs_retry | 95% | image_resolution_issue | 189s | P10 |
| 81 | powerpoint-slides-fef1 | flag_for_review | 93% | many_images, image_resolution_issue | 367s | P1 |
| 82 | powerpoint-slides-fef5 | needs_retry | 92% | many_images, image_resolution_issue | 149s | P2 |
| 83 | powerpoint-slides-ff0a | needs_retry | 89% | image_resolution_issue, table_extraction_mismatch | 165s | P3 |
| 84 | powerpoint-slides-ff0c | needs_retry | 95% | many_images, image_resolution_issue | 264s | P4 |
| 85 | powerpoint-slides-ff0d | N/A | N/A | — | 600s | P5 |
| 86 | scanned-from-paper-many-pages-of-tables-6878 | N/A | N/A | — | 600s | P6 |
| 87 | scio-physical-and-environmental-protection-686b1b8 | needs_retry | 96% | — | 149s | P7 |
| 88 | screenshot-images-11b5 | auto_approve | 100% | image_resolution_issue | 18s | P8 |
| 89 | seal-image-table-6870 | needs_retry | 99% | — | 80s | P9 |
| 90 | seal-imagery-11ab | N/A | N/A | — | 600s | P10 |
| 91 | seal-imagery-table-with-shading-132c | flag_for_review | 95% | complex_tables, image_resolution_issue | 303s | P1 |
| 92 | seal-imagery-table-with-shading-colored-text-672b | N/A | N/A | — | 600s | P2 |
| 93 | smac-lidar-apr-10-2024-6860db7b | flag_for_review | 95% | image_resolution_issue | 27s | P3 |
| 94 | standards-committee-meeting-agenda-packet-october- | auto_approve | 100% | image_resolution_issue | 91s | P4 |
| 95 | table-seal-imagery-diagram-1468 | flag_for_review | 94% | image_resolution_issue | 199s | P5 |
| 96 | tables-screenshots-photos-background-colors-59df | N/A | N/A | — | 600s | P6 |
| 97 | text-background-colors-53e2 | auto_approve | 100% | — | 53s | P7 |
| 98 | text-some-colored-text-3638 | auto_approve | 97% | — | 85s | P8 |
| 99 | wearencgov-broadbandinitiatives-685fc6d1 | needs_retry | 96% | many_images, image_resolution_issue | 172s | P9 |
| 100 | wearencgov-presentation3-685fc6b2 | needs_retry | 99% | image_resolution_issue | 100s | P10 |

---

## Routing Summary

- **auto_approve**: 29/100
- **failed**: 18/100
- **flag_for_review**: 22/100
- **needs_retry**: 31/100

## Edge Case Flags

- **image_resolution_issue**: 39 docs
- **many_images**: 12 docs
- **table_extraction_mismatch**: 9 docs
- **complex_tables**: 6 docs
- **scanned_document**: 5 docs
- **chunk_conversion_failure**: 4 docs