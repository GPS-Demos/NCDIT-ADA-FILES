# Auditor Report

**Batch**: `ncdit-audit-04-17`
**Date**: 2026-03-19
**Total documents**: 100
**Successful**: 100
**Failed/Timeout**: 0

## Routing Distribution

| Routing      | Count | %   |
| ------------ | ----- | --- |
| auto_approve | 2     | 2%  |
| human_review | 66    | 66% |
| reject       | 1     | 1%  |
| excluded     | 31    | 31% |

## Grade Distribution

| Grade    | Score Range | Count | %   |
| -------- | ----------- | ----- | --- |
| Good     | 90-100      | 23    | 23% |
| Fair     | 70-89       | 33    | 33% |
| Poor     | 50-69       | 10    | 10% |
| Critical | 0-49        | 34    | 34% |

## Detection vs Human Review

Comparison of auditor issue detection against human reviewer findings. "Caught" = auditor flagged the same issue. "Partial" = auditor flagged the doc but not the specific issue, or flagged with wrong severity.

| Category                     | Total  | Caught | Partial | Missed | Detection %  |
| ---------------------------- | ------ | ------ | ------- | ------ | ------------ |
| List numbering/structure     | 18     | 14     | 1       | 3      | 83%          |
| Missing/broken hyperlinks    | 15     | 10     | 0       | 5      | 67%          |
| Image duplication/cropping   | 22     | 12     | 8       | 2      | 91%          |
| Table structure              | 10     | 10     | 0       | 0      | 100%         |
| Retained headers/footers     | 5      | 5      | 0       | 0      | 100%         |
| Text formatting loss         | 3      | 3      | 0       | 0      | 100%         |
| Severity underrating         | 6      | 0      | 6       | 0      | 100% partial |
| Heading misclassification    | 4      | 1      | 0       | 3      | 25%          |
| Footnotes/watermarks/content | 4      | 3      | 0       | 1      | 75%          |
| Should-have-been-excluded    | 4      | 0      | 3       | 1      | 75%          |
| **TOTAL**                    | **91** | **58** | **18**  | **15** | **84%**      |

## All Results

| #   | Document                                                             | Score | Routing      | Concerns |
| --- | -------------------------------------------------------------------- | ----- | ------------ | -------- |
| 1   | 10-22-20-edu-committee-agenda-packet-685f9fde                        | 89    | human_review | 4        |
| 2   | 2019-20-smac-work-plan-685fadcf                                      | 92    | human_review | 4        |
| 3   | 20190416-nc-911-board-minutes-approved-687248c4                      | 79    | human_review | 6        |
| 4   | 20190726-board-agenda-685f9db9                                       | 83    | human_review | 4        |
| 5   | 20190814-nc-911-board-minutes-approved-685f9d99                      | 92    | human_review | 3        |
| 6   | 20200522-board-agenda-685f9ca8                                       | 90    | human_review | 4        |
| 7   | 20200522-nc911-board-minutes-approved-685f9cb7                       | 40    | human_review | 10       |
| 8   | 208m-endpoint-reseller-price-list-686b18db                           | 91    | human_review | 10       |
| 9   | 911-board-education-committee-meeting-minutes-april-21-2022-685f9f9d | 90    | human_review | 3        |
| 10  | 911-board-technology-committee-agenda-june-9-2022-685fa07f           | 61    | human_review | 8        |
| 11  | 911-education-committee-meeting-agenda-packet-03-25-2021-685f9fa9    | 24    | reject       | 14       |
| 12  | 911-telecommunicators-resolution-mitchell-county-685f6fd1            | 98    | human_review | 3        |
| 13  | 911-telecommunicators-resolution-rockingham-county-685f6ff5          | 92    | human_review | 3        |
| 14  | agency-onboarding-68607a87                                           | 0     | excluded     | 0        |
| 15  | appenc-initialdatalayers-685fad7d                                    | 83    | human_review | 7        |
| 16  | colored-text-logos-676a                                              | 98    | human_review | 5        |
| 17  | create-beautiful-sharepoint-sites-685fb98c                           | 0     | excluded     | 0        |
| 18  | cyber-incident-reporting-north-carolina-state-government-686b1b59    | 81    | human_review | 4        |
| 19  | draft-addressnc-specifications-20210811-68610610                     | 91    | human_review | 4        |
| 20  | draft-fy23-25-goals-and-priorities-685fc8b0                          | 81    | human_review | 3        |
| 21  | esrmo-newsletter-april-2017-686b1f74                                 | 61    | human_review | 10       |
| 22  | esrmo-newsletter-april-2024-686b1c64                                 | 79    | human_review | 7        |
| 23  | esrmo-newsletter-december-2018-686b1ee1                              | 59    | human_review | 10       |
| 24  | esrmo-newsletter-january-2017-686b1f87                               | 72    | human_review | 7        |
| 25  | esrmo-newsletter-july-2021-686b1e10                                  | 63    | human_review | 8        |
| 26  | esrmo-newsletter-march-2018-686b1f23                                 | 90    | human_review | 5        |
| 27  | esrmo-newsletter-september-2021-686b1e03                             | 77    | human_review | 8        |
| 28  | federal-interagency-committee-agenda20190516-68614dc2                | 100   | human_review | 1        |
| 29  | federalagencyhurricanecoordination-686132f8                          | 0     | excluded     | 0        |
| 30  | fillable-form-logo-imagery-bddf                                      | 0     | excluded     | 0        |
| 31  | fillable-form-logo-imagery-bdfc                                      | 0     | excluded     | 0        |
| 32  | gdac-legislative-report-may-2016-68610a4b                            | 88    | human_review | 8        |
| 33  | gicc-2020-census-nc-factsheet-20170809-686131e8                      | 86    | human_review | 5        |
| 34  | gicc-agenda-05-19-2021-68611645                                      | 90    | human_review | 3        |
| 35  | gicc-agenda-20160810-68613387                                        | 90    | human_review | 4        |
| 36  | gicc-agenda-20200506-68839aed                                        | 92    | human_review | 2        |
| 37  | gicc-goals-2021-2023-discussion-68612ed7                             | 92    | auto_approve | 1        |
| 38  | gicc-goals-and-strategic-direction-2021-23-685fd67f                  | 0     | excluded     | 0        |
| 39  | gicc-lgc-censussurveyresults-20200506-68839ae8                       | 0     | excluded     | 0        |
| 40  | gicc-meeting-minutes-02122003-685fb099                               | 80    | human_review | 5        |
| 41  | gicc-meeting-minutes-08072007-685fb034                               | 82    | human_review | 5        |
| 42  | gicc-mo-minutes-20191216-68614cc3                                    | 75    | human_review | 4        |
| 43  | gicc-ncdot-florence-20181107-68614eed                                | 0     | excluded     | 0        |
| 44  | gicc-smac-agenda-20210120-68839aac                                   | 88    | human_review | 5        |
| 45  | gicc-tims-may-2016-686133f1                                          | 0     | excluded     | 0        |
| 46  | ifb-its-400277-2017-1102-final-686b18e9                              | 40    | human_review | 14       |
| 47  | logo-imagery-graphic-colors-map-imagery-6e2e                         | 0     | excluded     | 0        |
| 48  | logo-imagery-graphic-colors-map-imagery-f80b                         | 0     | excluded     | 0        |
| 49  | logo-imagery-graphic-colors-map-imagery-tables-4807                  | 0     | excluded     | 0        |
| 50  | logo-imagery-screenshot-imagery-fca1                                 | 80    | human_review | 6        |
| 51  | logo-tables-shading-watermark-photos-13a3                            | 79    | human_review | 16       |
| 52  | logos-graphic-colors-photos-icons-diagrams-charts-53de               | 57    | human_review | 11       |
| 53  | logos-graphic-colors-photos-icons-diagrams-charts-53e1               | 80    | human_review | 8        |
| 54  | logos-graphic-colors-table-screenshot-images-fc98                    | 79    | human_review | 10       |
| 55  | long-contract-many-pages-of-tables-6881                              | 80    | human_review | 19       |
| 56  | map-imagery-logo-imagery-4809                                        | 0     | excluded     | 0        |
| 57  | map-imagery-logo-imagery-f810                                        | 0     | excluded     | 0        |
| 58  | map-imagery-photos-tables-screenshots-diagrams-data-charts-0fb1      | 73    | human_review | 5        |
| 59  | map-imagery-photos-tables-screenshots-diagrams-data-charts-365a      | 88    | human_review | 7        |
| 60  | map-imagery-photos-tables-screenshots-diagrams-data-charts-ff40      | 0     | excluded     | 0        |
| 61  | map-imagery-photos-tables-screenshots-diagrams-data-charts-i-e5cc    | 70    | human_review | 7        |
| 62  | map-imagery-photos-tables-screenshots-diagrams-data-charts-i-f7f6    | 0     | excluded     | 0        |
| 63  | memo-with-links-1334                                                 | 80    | human_review | 5        |
| 64  | mo-minutes-20160620-686133d2                                         | 82    | human_review | 4        |
| 65  | mostly-text-charts-tables-screenshots-maps-67fb                      | 84    | human_review | 15       |
| 66  | multi-factor-authentication-report-december-2015-68613ee4            | 88    | human_review | 5        |
| 67  | nc-911-board-education-committee-meeting-agenda-packet-feb-685f9e81  | 90    | human_review | 6        |
| 68  | nc-911-board-meeting-agenda-aug-26-2022-685f9a31                     | 90    | human_review | 3        |
| 69  | nc-911-board-minutes-september-30-2022-685f9a2b                      | 77    | human_review | 8        |
| 70  | nc-911-board-monthly-dispatch-march-2025-685f7179                    | 96    | human_review | 11       |
| 71  | nc-911-board-technology-committee-minutes-nov-4-2021-685fa41d        | 89    | human_review | 5        |
| 72  | ncom-update-gicc-05-15-2014-68612fe6                                 | 0     | excluded     | 0        |
| 73  | near-perfect-powerpoint-slides-by-accessibility-experts-47b0         | 0     | excluded     | 0        |
| 74  | near-perfect-powerpoint-slides-by-accessibility-experts-47b2         | 0     | excluded     | 0        |
| 75  | newsletter-with-many-images-and-formatted-text-117c                  | 81    | human_review | 6        |
| 76  | newsletter-with-many-images-and-formatted-text-21fb                  | 79    | human_review | 11       |
| 77  | powerpoint-slides-1793                                               | 0     | excluded     | 0        |
| 78  | powerpoint-slides-f832                                               | 0     | excluded     | 0        |
| 79  | powerpoint-slides-fed0                                               | 0     | excluded     | 0        |
| 80  | powerpoint-slides-feef                                               | 0     | excluded     | 0        |
| 81  | powerpoint-slides-fef1                                               | 0     | excluded     | 0        |
| 82  | powerpoint-slides-fef5                                               | 0     | excluded     | 0        |
| 83  | powerpoint-slides-ff0a                                               | 0     | excluded     | 0        |
| 84  | powerpoint-slides-ff0c                                               | 0     | excluded     | 0        |
| 85  | powerpoint-slides-ff0d                                               | 0     | excluded     | 0        |
| 86  | scanned-from-paper-many-pages-of-tables-6878                         | 92    | human_review | 3        |
| 87  | scio-physical-and-environmental-protection-686b1b84                  | 60    | human_review | 6        |
| 88  | screenshot-images-11b5                                               | 90    | human_review | 2        |
| 89  | seal-image-table-6870                                                | 90    | human_review | 3        |
| 90  | seal-imagery-11ab                                                    | 68    | human_review | 7        |
| 91  | seal-imagery-table-with-shading-132c                                 | 61    | human_review | 10       |
| 92  | seal-imagery-table-with-shading-colored-text-672b                    | 68    | human_review | 9        |
| 93  | smac-lidar-apr-10-2024-6860db7b                                      | 0     | excluded     | 0        |
| 94  | standards-committee-meeting-agenda-packet-october-7-2021-685fa26e    | 83    | human_review | 5        |
| 95  | table-seal-imagery-diagram-1468                                      | 92    | auto_approve | 1        |
| 96  | tables-screenshots-photos-background-colors-59df                     | 69    | human_review | 9        |
| 97  | text-background-colors-53e2                                          | 92    | human_review | 2        |
| 98  | text-some-colored-text-3638                                          | 80    | human_review | 6        |
| 99  | wearencgov-broadbandinitiatives-685fc6d1                             | 0     | excluded     | 0        |
| 100 | wearencgov-presentation3-685fc6b2                                    | 0     | excluded     | 0        |
