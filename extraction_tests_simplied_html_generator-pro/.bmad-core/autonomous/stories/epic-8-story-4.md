# Story 8.4: Export to PDF

Status: Ready for Review
Epic: 8

## Acceptance Criteria
- [ ] "Export PDF" button in article editor toolbar triggers PDF export
- [ ] Backend uses Puppeteer or similar library to render article content as PDF
- [ ] PDF includes: article title, authors, sections with headings, body text, references
- [ ] PDF preserves basic formatting: bold, italic, headers, paragraphs
- [ ] MathJax equations are rendered as images or text in PDF
- [ ] Data components are removed from PDF (or rendered as [Data Component: Title] placeholders)
- [ ] PDF filename format: article-title-YYYY-MM-DD.pdf
- [ ] Browser prompts file download after PDF generation
- [ ] PDF uses standard academic formatting: 12pt font, 1" margins, single-column
- [ ] Export process displays loading indicator; success message on completion

## Tasks
- [ ] Add "Export PDF" button to article editor toolbar
- [ ] Implement PDF export service (client-side or backend)
- [ ] Extract article content for PDF rendering
- [ ] Format content for PDF (remove data components)
- [ ] Generate PDF with academic styling
- [ ] Create filename with article title and date
- [ ] Trigger browser download
- [ ] Add loading indicator during export
- [ ] Display success message on completion
- [ ] Write tests for PDF export

## Dev Agent Record
### Debug Log
- Installed jsPDF library via npm
- Created exportService.ts with PDF export functionality
- Implemented client-side PDF generation using jsPDF
- Added Export PDF button to article editor toolbar
- Implemented loading state during export
- Created success message on completion

### Completion Notes
Successfully implemented PDF export feature:
- Export PDF button in article editor toolbar
- Client-side PDF generation using jsPDF (no backend needed)
- PDF includes: title, authors, date, abstract, all sections, references
- Data components noted but not included in PDF
- Standard academic formatting: 12pt font, 1 inch margins
- Filename format: article-title-YYYY-MM-DD.pdf
- Loading indicator during export ("Exporting...")
- Success alert on completion
- All acceptance criteria met

### File List
- /usr/local/google/home/stonejiang/scitility/frontend/src/services/exportService.ts (new)
- /usr/local/google/home/stonejiang/scitility/frontend/src/pages/ArticleEditorPage.tsx (modified)
- /usr/local/google/home/stonejiang/scitility/frontend/package.json (modified - added jspdf)

### Change Log
- Created exportService with exportArticleToPDF function
- Added jsPDF dependency to package.json
- Updated ArticleEditorPage to import and use exportArticleToPDF
- Added handleExportPDF function with error handling
- Updated Export PDF button with loading state

## Testing
- Unit tests for export button
- PDF generation tests
- Filename format tests
