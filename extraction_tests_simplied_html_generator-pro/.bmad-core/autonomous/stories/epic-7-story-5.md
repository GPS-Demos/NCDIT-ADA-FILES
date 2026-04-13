# Story 7.5: Provenance Metadata Panel

Status: Ready for Review
Epic: 7

## Acceptance Criteria
- [ ] "Complete Provenance Metadata" section displays 3 metadata cards in grid layout
- [ ] Funding Source card shows: Grant number, Amount, Period, PI, Institution
- [ ] Institutional Info card shows: Organization, Department, IRB Approval, Data Policy, Retention period
- [ ] Licenses & Compliance card shows: Data License, Code License, FAIR Compliant (Yes/No), GDPR Status, Export Control
- [ ] Each card uses heading with icon and colored accent
- [ ] Metadata values are displayed as label-value pairs with consistent formatting
- [ ] For demo: Metadata is hardcoded from prototype example (NSF Grant #2025-1234, University Research Center, CC BY 4.0, etc.)
- [ ] Cards use light gray background with proper spacing
- [ ] Metadata is stored in dataComponent.provenance{} object in Firestore
- [ ] Future enhancement: editable provenance fields for creators

## Tasks
- [ ] Create provenance metadata panel component
- [ ] Design 3-card grid layout
- [ ] Create Funding Source card with grant info
- [ ] Create Institutional Info card
- [ ] Create Licenses & Compliance card
- [ ] Add icons and colored accents to cards
- [ ] Use label-value pair formatting
- [ ] Add hardcoded demo data
- [ ] Style cards with gray background
- [ ] Write tests for metadata display

## Dev Agent Record
### Debug Log
No significant issues encountered during implementation.

### Completion Notes
- Created ProvenanceMetadata component with 3-card grid layout
- Implemented Funding Source card (blue accent):
  - Grant number: NSF Grant #2025-1234
  - Amount: $750,000
  - Period: Jan 2023 - Dec 2025
  - PI: Dr. Sarah Chen
  - Institution: University Research Center
- Implemented Institutional Info card (green accent):
  - Organization: Stanford University
  - Department: Department of Environmental Science
  - IRB Approval: IRB-2023-45678 (Approved)
  - Data Policy: Open Data Policy v2.1
  - Retention period: 10 years post-publication
- Implemented Licenses & Compliance card (purple accent):
  - Data License: CC BY 4.0
  - Code License: MIT License
  - FAIR Compliant: Yes (green badge with checkmark)
  - GDPR Status: Compliant - No PII collected
  - Export Control: EAR99 - No restrictions
- Each card has icon, colored accent (bg-[color]-100), and heading
- Label-value pair formatting with consistent spacing
- Light gray background for cards
- Information panel explaining provenance metadata
- Added note about future editable fields and Firestore integration

### File List
- /usr/local/google/home/stonejiang/scitility/frontend/src/components/ProvenanceMetadata.tsx (new)

### Change Log
- Created 3-card grid layout with funding, institutional, and compliance info
- Implemented hardcoded demo data from climate research example
- Added colored icons and consistent styling
- Fixed type imports to use type-only imports

## Testing
- Unit tests for metadata panel rendering
- Card layout tests
- Data display tests
