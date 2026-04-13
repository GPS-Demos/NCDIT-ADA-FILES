# Story 7.1: Data Lineage Page Structure

Status: Ready for Review
Epic: 7

## Acceptance Criteria
- [ ] Data lineage page loads at /data-lineage/:componentId
- [ ] Page header displays "Data Lineage & Provenance" heading and data component title as subtitle
- [ ] Header includes action buttons: "Export Lineage", "View Verification Report"
- [ ] Page sections: Complete Data Lineage Graph, Reproducibility Capsules, Complete Version History, Complete Provenance Metadata
- [ ] Each section uses distinct background color and clear headings
- [ ] Page fetches lineage data from data component metadata and related documents
- [ ] Loading state displays while fetching lineage information
- [ ] Back button navigates to data viewer page

## Tasks
- [ ] Create data lineage page route at /data-lineage/:componentId
- [ ] Implement page header with title and action buttons
- [ ] Create four main sections for lineage content
- [ ] Add loading state during data fetch
- [ ] Implement back navigation to data viewer
- [ ] Add error handling for missing data components
- [ ] Style sections with distinct backgrounds
- [ ] Integrate with data component service
- [ ] Add route to App.tsx
- [ ] Write tests for page structure

## Dev Agent Record
### Debug Log
No significant issues encountered during implementation.

### Completion Notes
- Created DataLineagePage.tsx with routing at /data-lineage/:componentId
- Implemented page header with title, subtitle, and action buttons (Export Lineage, View Verification Report)
- Created four main sections with distinct background colors:
  - Complete Data Lineage Graph (blue-50)
  - Reproducibility Capsules (green-50)
  - Complete Version History (yellow-50)
  - Complete Provenance Metadata (purple-50)
- Added loading and error states
- Implemented back navigation to data viewer page
- Added route to App.tsx
- Connected "View Lineage" button in DataViewerPage to navigate to lineage page

### File List
- /usr/local/google/home/stonejiang/scitility/frontend/src/pages/DataLineagePage.tsx (new)
- /usr/local/google/home/stonejiang/scitility/frontend/src/App.tsx (modified)
- /usr/local/google/home/stonejiang/scitility/frontend/src/pages/DataViewerPage.tsx (modified)

### Change Log
- Created complete data lineage page structure with four sections
- Added routing and navigation handlers
- Integrated with data component service for loading data
- Fixed type imports to use type-only imports

## Testing
- Unit tests for page structure rendering
- Navigation tests
- Loading state tests
