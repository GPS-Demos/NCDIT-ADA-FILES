# Story 6.8: Version Diff View (Placeholder)

Status: Ready for Review
Epic: 6

## Acceptance Criteria
- [x] "View Diff" button on version card triggers diff view action
- [x] For demo/MVP: Button displays alert "Diff view coming soon" or placeholder page
- [x] Placeholder page shows: "Version Comparison" heading, selected version info, message explaining future feature
- [x] Future enhancement: Side-by-side comparison with highlighted additions (green) and deletions (red)
- [x] Future enhancement: Word-level diff for precise change tracking
- [x] Placeholder maintains consistent page styling
- [x] Back button returns to version history page

## Tasks
- [x] Add "View Diff" button to version card
- [x] Create placeholder diff view page
- [x] Display version comparison heading
- [x] Show selected version information
- [x] Add message explaining future feature
- [x] Implement back navigation to version history
- [x] Style placeholder page consistently
- [x] Add TODO comments for future diff implementation
- [x] Write tests for placeholder page

## Dev Agent Record
### Debug Log
- Created VersionDiffPage as placeholder component with comprehensive UI
- Added route for /article/:id/versions/:versionId/diff
- Updated VersionHistoryPage to navigate to diff page on "View Diff" button click
- Comprehensive tests written for placeholder page

### Completion Notes
Implementation complete with all acceptance criteria met:
1. "View Diff" button navigates to dedicated diff page
2. Placeholder page displays "Version Comparison" heading and version info
3. Planned features list explains future functionality (side-by-side, additions/deletions highlighting, word-level diff)
4. Back button functionality implemented (appears in header and as action button)
5. Consistent styling with rest of application (Tailwind CSS)
6. TODO comment added at top of VersionDiffPage component
7. Full test coverage for placeholder page including navigation, error states, and content display

### File List
- /usr/local/google/home/stonejiang/scitility/frontend/src/pages/VersionDiffPage.tsx (new)
- /usr/local/google/home/stonejiang/scitility/frontend/src/pages/VersionDiffPage.test.tsx (new)
- /usr/local/google/home/stonejiang/scitility/frontend/src/pages/VersionHistoryPage.tsx (updated)
- /usr/local/google/home/stonejiang/scitility/frontend/src/App.tsx (updated)

### Change Log
- Created VersionDiffPage placeholder component with version info display and planned features
- Added route /article/:id/versions/:versionId/diff to App.tsx
- Updated handleViewDiff in VersionHistoryPage to navigate to diff page
- Implemented back navigation from diff page to version history
- Added comprehensive tests for VersionDiffPage component

## Testing
- Unit tests for diff placeholder page
- Navigation tests
- Button interaction tests
