# Auditor Report

**Batch**: `ncdit-audit-04-17`
**Date**: 2026-03-19
**Total documents**: 100
**Successful**: 99
**Failed/Timeout**: 1

## Grade Distribution

| Grade    | Score Range | Count | %   |
| -------- | ----------- | ----- | --- |
| Good     | 90-100      | 20    | 20% |
| Fair     | 70-89       | 40    | 40% |
| Poor     | 50-69       | 4     | 4%  |
| Critical | 0-49        | 35    | 35% |

### Detection by Issue Category (Updated)

| Category                            | Total | Caught | Partial | Detection %  |
| ----------------------------------- | ----- | ------ | ------- | ------------ |
| List numbering/fragmentation        | 10    | 3      | 7       | 100%         |
| Heading/structure misclassification | 5     | 2      | 3       | 100%         |
| Text formatting loss                | 4     | 2      | 2       | 100%         |
| Missing/broken hyperlinks           | 6     | 4      | 2       | 100%         |
| Image duplication/redundant images  | 9     | 5      | 4       | 100%         |
| Missing content                     | 2     | 1      | 1       | 100%         |
| Retained footers/page numbers       | 4     | 3      | 1       | 100%         |
| Should-have-been-excluded           | 3     | 1      | 2       | 100%         |
| Severity underrating                | 3     | 0      | 3       | 100% partial |

## Problem Documents (Reject or Score < 70, non-excluded)

| Document                                                          | Score | Routing      | Concerns |
| ----------------------------------------------------------------- | ----- | ------------ | -------- |
| 911-education-committee-meeting-agenda-packet-03-25-2021-685f9fa9 | 24    | human_review | 6        |
| 20200522-nc911-board-minutes-approved-685f9cb7                    | 40    | human_review | 4        |
| seal-imagery-11ab                                                 | 40    | human_review | 3        |
| ifb-its-400277-2017-1102-final-686b18e9                           | 40    | human_review | 6        |
| esrmo-newsletter-january-2017-686b1f87                            | 63    | human_review | 5        |
| esrmo-newsletter-april-2024-686b1c64                              | 66    | human_review | 6        |
| memo-with-links-1334                                              | 68    | human_review | 5        |
| seal-imagery-table-with-shading-colored-text-672b                 | 68    | human_review | 4        |
| 208m-endpoint-reseller-price-list-686b18db                        | 83    | reject       | 8        |

---

## All Results (Updated with re-run scores)

| #   | Document                                                             | Score   | Routing          | Method                  | Concerns | Time   |
| --- | -------------------------------------------------------------------- | ------- | ---------------- | ----------------------- | -------- | ------ |
| 1   | 10-22-20-edu-committee-agenda-packet-685f9fde                        | 89      | auto_approve     | llm_final_decider       | 3        | 223.6s |
| 2   | 2019-20-smac-work-plan-685fadcf                                      | 92      | auto_approve     | llm_final_decider       | 3        | 106.4s |
| 3   | 20190416-nc-911-board-minutes-approved-687248c4                      | 79      | human_review     | llm_final_decider       | 4        | 136.2s |
| 4   | 20190726-board-agenda-685f9db9                                       | 92      | auto_approve     | llm_final_decider       | 1        | 156.4s |
| 5   | 20190814-nc-911-board-minutes-approved-685f9d99                      | **100** | **human_review** | llm_final_decider       | 1        | —      |
| 6   | 20200522-board-agenda-685f9ca8                                       | 77      | human_review     | llm_final_decider       | 4        | 149.3s |
| 7   | 20200522-nc911-board-minutes-approved-685f9cb7                       | 40      | human_review     | hard_veto:V7            | 4        | 248.6s |
| 8   | 208m-endpoint-reseller-price-list-686b18db                           | 83      | reject           | llm_final_decider       | 8        | 388.3s |
| 9   | 911-board-education-committee-meeting-minutes-april-21-2022-685f9f9d | 90      | human_review     | llm_final_decider       | 2        | 201.0s |
| 10  | 911-board-technology-committee-agenda-june-9-2022-685fa07f           | 70      | human_review     | llm_final_decider       | 4        | 156.6s |
| 11  | 911-education-committee-meeting-agenda-packet-03-25-2021-685f9fa9    | 24      | human_review     | llm_final_decider       | 6        | 215.8s |
| 12  | 911-telecommunicators-resolution-mitchell-county-685f6fd1            | **91**  | **human_review** | llm_final_decider       | 3        | —      |
| 13  | 911-telecommunicators-resolution-rockingham-county-685f6ff5          | **98**  | **human_review** | llm_final_decider       | 2        | —      |
| 14  | agency-onboarding-68607a87                                           | 0       | excluded         | document_classification | 0        | 72.8s  |
| 15  | appenc-initialdatalayers-685fad7d                                    | 83      | human_review     | llm_final_decider       | 6        | 186.9s |
| 16  | colored-text-logos-676a                                              | 98      | human_review     | llm_final_decider       | 2        | 179.7s |
| 17  | create-beautiful-sharepoint-sites-685fb98c                           | 0       | excluded         | document_classification | 0        | 19.2s  |
| 18  | cyber-incident-reporting-north-carolina-state-government-686b1b59    | 78      | human_review     | llm_final_decider       | 2        | 171.8s |
| 19  | draft-addressnc-specifications-20210811-68610610                     | 92      | auto_approve     | llm_final_decider       | 1        | 263.0s |
| 20  | draft-fy23-25-goals-and-priorities-685fc8b0                          | 90      | human_review     | llm_final_decider       | 2        | 140.4s |
| 21  | esrmo-newsletter-april-2017-686b1f74                                 | 79      | human_review     | llm_final_decider       | 3        | 286.8s |
| 22  | esrmo-newsletter-april-2024-686b1c64                                 | 66      | human_review     | llm_final_decider       | 6        | 141.1s |
| 23  | esrmo-newsletter-december-2018-686b1ee1                              | 80      | human_review     | llm_final_decider       | 3        | 217.9s |
| 24  | esrmo-newsletter-january-2017-686b1f87                               | 63      | human_review     | llm_final_decider       | 5        | 130.1s |
| 25  | esrmo-newsletter-july-2021-686b1e10                                  | 73      | human_review     | llm_final_decider       | 3        | 149.9s |
| 26  | esrmo-newsletter-march-2018-686b1f23                                 | 83      | auto_approve     | llm_final_decider       | 2        | 132.2s |
| 27  | esrmo-newsletter-september-2021-686b1e03                             | 79      | human_review     | llm_final_decider       | 2        | 177.4s |
| 28  | federal-interagency-committee-agenda20190516-68614dc2                | 100     | auto_approve     | llm_final_decider       | 0        | 167.5s |
| 29  | federalagencyhurricanecoordination-686132f8                          | 0       | excluded         | document_classification | 0        | 50.8s  |
| 30  | fillable-form-logo-imagery-bddf                                      | 0       | excluded         | document_classification | 0        | 60.7s  |
| 31  | fillable-form-logo-imagery-bdfc                                      | 0       | excluded         | document_classification | 0        | 42.2s  |
| 32  | gdac-legislative-report-may-2016-68610a4b                            | 87      | auto_approve     | llm_final_decider       | 5        | 195.6s |
| 33  | gicc-2020-census-nc-factsheet-20170809-686131e8                      | **100** | **human_review** | llm_final_decider       | 2        | —      |
| 34  | gicc-agenda-05-19-2021-68611645                                      | 90      | auto_approve     | llm_final_decider       | 2        | 210.4s |
| 35  | gicc-agenda-20160810-68613387                                        | 87      | auto_approve     | llm_final_decider       | 3        | 108.0s |
| 36  | gicc-agenda-20200506-68839aed                                        | 90      | auto_approve     | llm_final_decider       | 2        | 122.0s |
| 37  | gicc-goals-2021-2023-discussion-68612ed7                             | 92      | auto_approve     | llm_final_decider       | 1        | 85.5s  |
| 38  | gicc-goals-and-strategic-direction-2021-23-685fd67f                  | 0       | excluded         | document_classification | 0        | 25.7s  |
| 39  | gicc-lgc-censussurveyresults-20200506-68839ae8                       | 0       | excluded         | document_classification | 0        | 35.3s  |
| 40  | gicc-meeting-minutes-02122003-685fb099                               | 79      | human_review     | llm_final_decider       | 2        | 225.0s |
| 41  | gicc-meeting-minutes-08072007-685fb034                               | 89      | human_review     | llm_final_decider       | 2        | 142.7s |
| 42  | gicc-mo-minutes-20191216-68614cc3                                    | **90**  | **human_review** | llm_final_decider       | 4        | —      |
| 43  | gicc-ncdot-florence-20181107-68614eed                                | 0       | excluded         | document_classification | 0        | 32.8s  |
| 44  | gicc-smac-agenda-20210120-68839aac                                   | 77      | human_review     | llm_final_decider       | 4        | 162.7s |
| 45  | gicc-tims-may-2016-686133f1                                          | 0       | excluded         | document_classification | 0        | 92.0s  |
| 46  | ifb-its-400277-2017-1102-final-686b18e9                              | 40      | human_review     | hard_veto:V7            | 6        | 281.1s |
| 47  | logo-imagery-graphic-colors-map-imagery-6e2e                         | 0       | excluded         | document_classification | 0        | 71.2s  |
| 48  | logo-imagery-graphic-colors-map-imagery-f80b                         | 0       | excluded         | document_classification | 0        | 56.2s  |
| 49  | logo-imagery-graphic-colors-map-imagery-tables-4807                  | 0       | excluded         | document_classification | 0        | 23.2s  |
| 50  | logo-imagery-screenshot-imagery-fca1                                 | 79      | human_review     | llm_final_decider       | 3        | 125.7s |
| 51  | logo-tables-shading-watermark-photos-13a3                            | 79      | human_review     | llm_final_decider       | 10       | 188.0s |
| 52  | logos-graphic-colors-photos-icons-diagrams-charts-53de               | 70      | human_review     | llm_final_decider       | 4        | 208.0s |
| 53  | logos-graphic-colors-photos-icons-diagrams-charts-53e1               | 70      | human_review     | llm_final_decider       | 5        | 334.7s |
| 54  | logos-graphic-colors-table-screenshot-images-fc98                    | 80      | human_review     | llm_final_decider       | 5        | 202.3s |
| 55  | long-contract-many-pages-of-tables-6881                              | 86      | auto_approve     | llm_final_decider       | 13       | 378.1s |
| 56  | map-imagery-logo-imagery-4809                                        | 0       | excluded         | document_classification | 0        | 56.5s  |
| 57  | map-imagery-logo-imagery-f810                                        | 0       | excluded         | document_classification | 0        | 32.7s  |
| 58  | map-imagery-photos-tables-screenshots-diagrams-data-charts-0fb1      | 79      | human_review     | llm_final_decider       | 3        | 267.8s |
| 59  | map-imagery-photos-tables-screenshots-diagrams-data-charts-365a      | 88      | auto_approve     | llm_final_decider       | 2        | 200.7s |
| 60  | map-imagery-photos-tables-screenshots-diagrams-data-charts-ff40      | 0       | excluded         | document_classification | 0        | 67.0s  |
| 61  | map-imagery-photos-tables-screenshots-diagrams-data-charts-i-e5cc    | 71      | human_review     | llm_final_decider       | 4        | 282.5s |
| 62  | map-imagery-photos-tables-screenshots-diagrams-data-charts-i-f7f6    | 0       | excluded         | document_classification | 0        | 87.9s  |
| 63  | memo-with-links-1334                                                 | 68      | human_review     | llm_final_decider       | 5        | 150.8s |
| 64  | mo-minutes-20160620-686133d2                                         | 81      | human_review     | llm_final_decider       | 2        | 130.1s |
| 65  | mostly-text-charts-tables-screenshots-maps-67fb                      | 77      | human_review     | llm_final_decider       | 10       | 240.1s |
| 66  | multi-factor-authentication-report-december-2015-68613ee4            | 79      | human_review     | llm_final_decider       | 3        | 179.0s |
| 67  | nc-911-board-education-committee-meeting-agenda-packet-feb-685f9e81  | 90      | human_review     | llm_final_decider       | 2        | 346.3s |
| 68  | nc-911-board-meeting-agenda-aug-26-2022-685f9a31                     | 89      | auto_approve     | llm_final_decider       | 3        | 181.8s |
| 69  | nc-911-board-minutes-september-30-2022-685f9a2b                      | 75      | human_review     | llm_final_decider       | 5        | 247.8s |
| 70  | nc-911-board-monthly-dispatch-march-2025-685f7179                    | 92      | auto_approve     | llm_final_decider       | 6        | 337.0s |
| 71  | nc-911-board-technology-committee-minutes-nov-4-2021-685fa41d        | 89      | human_review     | llm_final_decider       | 3        | 148.5s |
| 72  | ncom-update-gicc-05-15-2014-68612fe6                                 | 0       | excluded         | document_classification | 0        | 18.6s  |
| 73  | near-perfect-powerpoint-slides-by-accessibility-experts-47b0         | 0       | excluded         | document_classification | 0        | 38.8s  |
| 74  | near-perfect-powerpoint-slides-by-accessibility-experts-47b2         | 0       | excluded         | document_classification | 0        | 24.1s  |
| 75  | newsletter-with-many-images-and-formatted-text-117c                  | 79      | human_review     | llm_final_decider       | 4        | 150.4s |
| 76  | newsletter-with-many-images-and-formatted-text-21fb                  | 74      | human_review     | llm_final_decider       | 8        | 299.7s |
| 77  | powerpoint-slides-1793                                               | 0       | excluded         | document_classification | 0        | 42.7s  |
| 78  | powerpoint-slides-f832                                               | 0       | excluded         | document_classification | 0        | 51.2s  |
| 79  | powerpoint-slides-feef                                               | 0       | excluded         | document_classification | 0        | 34.0s  |
| 80  | powerpoint-slides-fef1                                               | 0       | excluded         | document_classification | 0        | 27.9s  |
| 81  | powerpoint-slides-fef5                                               | 0       | excluded         | document_classification | 0        | 67.3s  |
| 82  | powerpoint-slides-ff0a                                               | 0       | excluded         | document_classification | 0        | 78.1s  |
| 83  | powerpoint-slides-ff0c                                               | 0       | excluded         | document_classification | 0        | 70.9s  |
| 84  | powerpoint-slides-ff0d                                               | 0       | excluded         | document_classification | 0        | 80.1s  |
| 85  | scanned-from-paper-many-pages-of-tables-6878                         | 92      | human_review     | llm_final_decider       | 1        | 233.1s |
| 86  | scio-physical-and-environmental-protection-686b1b84                  | 79      | human_review     | llm_final_decider       | 3        | 172.6s |
| 87  | screenshot-images-11b5                                               | 90      | human_review     | llm_final_decider       | 2        | 126.3s |
| 88  | seal-image-table-6870                                                | 87      | auto_approve     | llm_final_decider       | 2        | 175.1s |
| 89  | seal-imagery-11ab                                                    | 40      | human_review     | hard_veto:V7            | 3        | 308.1s |
| 90  | seal-imagery-table-with-shading-132c                                 | 74      | human_review     | llm_final_decider       | 5        | 235.8s |
| 91  | seal-imagery-table-with-shading-colored-text-672b                    | 68      | human_review     | llm_final_decider       | 4        | 457.2s |
| 92  | smac-lidar-apr-10-2024-6860db7b                                      | 0       | excluded         | document_classification | 0        | 96.3s  |
| 93  | standards-committee-meeting-agenda-packet-october-7-2021-685fa26e    | 83      | human_review     | llm_final_decider       | 3        | 268.5s |
| 94  | table-seal-imagery-diagram-1468                                      | 0       | excluded         | document_classification | 0        | 29.3s  |
| 95  | tables-screenshots-photos-background-colors-59df                     | 70      | human_review     | llm_final_decider       | 3        | 190.7s |
| 96  | text-background-colors-53e2                                          | 92      | auto_approve     | llm_final_decider       | 1        | 136.7s |
| 97  | text-some-colored-text-3638                                          | 79      | human_review     | llm_final_decider       | 4        | 251.1s |
| 98  | wearencgov-broadbandinitiatives-685fc6d1                             | 0       | excluded         | document_classification | 0        | 65.5s  |
| 99  | wearencgov-presentation3-685fc6b2                                    | 0       | excluded         | document_classification | 0        | 43.4s  |
