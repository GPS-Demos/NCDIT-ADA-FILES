## Overall Rating
Has minor cosmetic defects

## Critical Issues
None.

## Major Issues
None.

## Minor Issues
*   In the first table row for "No Taxable Income", the cell for "Computed Gross Tax Liability [$]" contains a hyphen ("-"), but the corresponding cell for "Computed NC Taxable Income [includes returns with deficit]: [before residency proration] [$]" contains "(3,323,392,356)". In the PDF, the "(3,323,392,356)" value is actually split across two cells as "(3,323," and "392,356)". While this does not affect the data accuracy of the total value, the table structure slightly deviates from the visual layout of the PDF.
*   The PDF contains a trailing asterisk on the text "Effective Tax Rate*" in the table header, which is missing from the HTML column header `Effective Tax Rate* [%]`.
*   The footnote in the PDF contains two separate lines starting with an asterisk: `*Effective tax rate for NCTI basis...` and `*Effective tax rate for FAGI basis...`. The HTML replicates this as two separate paragraphs, but the second asterisk is missing in the HTML: `<p>*Effective tax rate for FAGI basis=Net Tax as a % of Federal Adjusted Gross Income</p>` (it should be `**Effective tax rate...`).
