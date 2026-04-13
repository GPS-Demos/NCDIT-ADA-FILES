## Overall Rating
Has serious structural or content issues

## Critical Issues
- **Table Data Error (MO Missouri):** The HTML row for "MO Missouri" shows "0.1700" for "Methanol (Gallons)" and "0.1700" for "E-85 (Gallons)". According to the source PDF, the value for "Methanol" is "-" (missing/no tax) and "E-85" is "0.1700".
- **Table Data Error (MS Mississippi):** The HTML row for "MS Mississippi" contains 11 values instead of 12 (it is missing the final "Biodiesel" column data). The row is shifted to the left, resulting in incorrect data assignments for the columns.
- **Table Data Error (KS Kansas):** The HTML row for "KS Kansas" contains 12 values, but they do not match the PDF source. The source PDF lists "-" (missing) for "A-55" and "0.2600" for "Biodiesel". The HTML lists "0.2600" for "A-55" and "0.2600" for "Biodiesel", misaligning the row.

## Major Issues
- **Table Structure/Sequence:** The table rows in the HTML do not follow the visual order of the source PDF. Specifically, the rows "MS Mississippi", "MA Massachusetts", and several others are presented in a different order than the PDF, making it difficult to verify data against the source.
- **Header Duplication/Redundancy:** The HTML includes two separate `<div class="page-header">` blocks that repeat metadata and titles, which does not reflect the document structure accurately and adds redundant content.

## Minor Issues
- **Typo in Header:** The HTML header contains "GAS-1278" and "2nd Quarter 2017 IFTA Tax Rates" in a structure that deviates from the logical document order provided in the PDF pages.
