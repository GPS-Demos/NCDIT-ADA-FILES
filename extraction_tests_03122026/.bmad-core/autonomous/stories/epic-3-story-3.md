# Story: Add Data Component - Step 2 (Storage Layer Selection)
Status: Ready for Review
Epic: 3

## Description
Create Step 2 of the workflow for selecting storage backend.

## Acceptance Criteria
- [x] Step 2 page displays storage backend selection with 6 option cards
- [x] Storage options displayed: Google Cloud Storage (recommended, selected by default), AWS S3, Azure Blob Storage, Institutional Repository, Zenodo, Custom S3-Compatible
- [x] Each storage card shows: icon, name, tier label (Recommended/Enterprise/Open Science/Advanced), feature bullets, pricing info
- [x] Only one storage option can be selected at a time (radio behavior)
- [x] Clicking a storage card highlights it and updates "Selected Storage" display below cards
- [x] "Selected Storage" panel shows two inputs: "Bucket/Container Name" (text) and "Region/Location" (dropdown)
- [x] Region dropdown populates based on selected storage backend (e.g., us-central1, us-east1 for GCS)
- [x] Information panel explains storage abstraction layer and ability to move data between repositories
- [x] Validation requires storage selection and bucket/region inputs before proceeding to Step 3

## Tasks
- [x] Create Step 2 component
- [x] Create storage option cards
- [x] Implement radio selection behavior
- [x] Add bucket/region inputs
- [x] Populate region dropdown based on selection
- [x] Add validation
- [x] Add "Back" and "Next" buttons
- [x] Update progress indicator (2 of 6)

## Dev Agent Record
### Debug Log
- Used existing DataComponentFormContext from Story 2 instead of creating duplicate
- Fixed controlled/uncontrolled input warning by initializing step2 data in context
- All 17 tests passing successfully

### Completion Notes
- Successfully implemented Step 2 Storage Layer Selection component
- Integrated with existing AddDataComponentPage from Story 2
- 6 storage option cards with radio selection behavior implemented
- Region dropdown dynamically populates based on selected storage backend
- Form validation ensures storage, bucket name, and region are selected before proceeding
- Comprehensive test coverage with 17 passing tests
- Used existing shared Context from Story 2 for state management
- Progress indicator shows "Step 2 of 6"

### File List
- /usr/local/google/home/stonejiang/scitility/frontend/src/components/Step2StorageSelection.tsx (new)
- /usr/local/google/home/stonejiang/scitility/frontend/src/components/Step2StorageSelection.test.tsx (new)
- /usr/local/google/home/stonejiang/scitility/frontend/src/pages/AddDataComponentPage.tsx (modified)
- /usr/local/google/home/stonejiang/scitility/frontend/src/contexts/DataComponentFormContext.tsx (modified)

### Change Log
- Created Step2StorageSelection component with 6 storage backend options (GCS, S3, Azure, Institutional, Zenodo, Custom)
- Implemented storage card UI with icons, tier labels, feature bullets, and pricing information
- Added radio selection behavior for storage options with visual highlighting
- Created dynamic region dropdown that populates based on selected storage backend
- Implemented Storage Configuration panel with bucket/container name input and region selector
- Added comprehensive form validation for storage selection, bucket name, and region
- Integrated Step 2 into AddDataComponentPage workflow
- Updated DataComponentFormContext to properly initialize step2 data
- Created 17 comprehensive tests covering all user interactions and validation scenarios
- All tests passing successfully

## Testing
- [x] Test storage card selection
- [x] Test bucket/region inputs
- [x] Test region dropdown population
- [x] Test validation
- [x] Test navigation
