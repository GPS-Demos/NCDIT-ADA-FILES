# Story: Add Data Component - Step 3 (File Upload)
Status: Ready for Review
Epic: 3

## Description
Create Step 3 for file upload with drag-and-drop and progress tracking.

## Acceptance Criteria
- [x] Step 3 displays drag-and-drop file upload zone with dashed border
- [x] Upload zone shows icon (📁), heading "Drop files here or click to browse", and file size limits (Max Single File: 5TB, Total Dataset: Unlimited, Upload Speed: 10 Gbps)
- [x] Clicking upload zone opens file browser dialog
- [x] Dragging files over upload zone highlights zone with background color change
- [x] Dropping files initiates upload process with progress bar
- [x] Multiple files can be uploaded and are listed below upload zone
- [x] Each uploaded file displays: filename, size, upload progress percentage, and remove button
- [x] File upload uses chunked upload for large files (>100MB)
- [x] Upload generates SHA-256 hash for each file during upload process
- [x] Successfully uploaded files are marked with checkmark icon
- [x] Upload errors display error message and allow retry
- [x] Validation requires at least one file uploaded before proceeding to Step 4

## Tasks
- [x] Create Step 3 component
- [x] Implement drag-and-drop zone
- [x] Add file browser integration
- [x] Create file upload handler (Firebase Storage)
- [x] Implement progress tracking
- [x] Generate SHA-256 hash during upload
- [x] Add file list with remove functionality
- [x] Handle upload errors
- [x] Add validation
- [x] Update progress indicator (3 of 6)

## Dev Agent Record
### Debug Log
- Successfully implemented Step 3 component with all required features
- Added Firebase Storage integration for file uploads
- Implemented SHA-256 hash generation using Web Crypto API
- All tests passing (32 new tests added)

### Completion Notes
- Component uses Material-UI for consistent design with rest of application
- File upload supports multiple files with individual progress tracking
- SHA-256 hash is generated during upload for data integrity verification
- Error handling includes retry functionality for failed uploads
- Validation ensures at least one file is uploaded before proceeding
- Upload utilities support files up to 5TB as specified
- Context updated to store uploaded file metadata including hashes and download URLs

### File List
**New Files:**
- frontend/src/components/AddDataStep3FileUpload.tsx
- frontend/src/components/AddDataStep3FileUpload.test.tsx
- frontend/src/utils/hashUtils.ts
- frontend/src/utils/hashUtils.test.ts
- frontend/src/utils/fileUploadUtils.ts
- frontend/src/utils/fileUploadUtils.test.ts

**Modified Files:**
- frontend/src/contexts/DataComponentFormContext.tsx - Added Step3Data interface with UploadedFile type
- frontend/src/config/firebase.ts - Added Firebase Storage initialization
- frontend/src/test/setup.ts - Added File.arrayBuffer polyfill for tests

### Change Log
- Created AddDataStep3FileUpload component with drag-and-drop support
- Implemented file upload to Firebase Storage with progress tracking
- Added SHA-256 hash generation utility using Web Crypto API
- Created file upload utilities for storage path generation and validation
- Updated DataComponentFormContext with Step3Data interface
- Added comprehensive test coverage (32 tests, 100% pass rate)
- Integrated with existing DataComponentFormProvider for state management

## Testing
- Test drag-and-drop
- Test file browser
- Test upload progress
- Test hash generation
- Test file removal
- Test validation
