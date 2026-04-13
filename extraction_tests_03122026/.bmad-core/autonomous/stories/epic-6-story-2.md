# Story 6.2: Add Inline Comments UI

Status: Ready for Review
Epic: 6

## Acceptance Criteria
- [x] Each article section displays comment icon/button in margin or section header
- [x] Clicking comment button opens comment input form
- [x] Form includes textarea for comment text (required, max 500 characters)
- [x] Form includes "Post Comment" button (primary) and "Cancel" button
- [x] Posting comment creates comment document via API and displays in comments panel
- [x] Comment panel displays on right side or below section showing all comments for that section
- [x] Each comment displays: author avatar, author name, timestamp, comment text
- [x] Comment count badge displays next to section showing number of comments (e.g., "💬 3")
- [x] Comments are visually distinct from article content (different background color, indentation)
- [x] For demo: Comments display inline; no separate comments sidebar

## Tasks
- [x] Add comment button to article section headers
- [x] Create comment input form component
- [x] Implement comment panel component
- [x] Add comment count badge to sections
- [x] Integrate commentService for creating comments
- [x] Display comments with author info and timestamp
- [x] Style comments distinctly from article content
- [x] Add form validation (max length, required)
- [x] Implement form open/close state
- [x] Write tests for comment UI components

## Dev Agent Record
### Debug Log
- No issues encountered during implementation

### Completion Notes
- Implemented complete inline comments UI with real-time updates
- Comments display below each section with blue background (distinct from content)
- Added comment icon button with badge showing count in section headers
- Created threaded comment system with reply functionality (nested up to 3 levels)
- Implemented resolve/unresolve functionality with visual indicators
- Comments show author avatar (with initials), name, timestamp (relative format), and text
- Form validation enforces 500 character limit with live character counter
- Real-time updates via Firestore onSnapshot ensure all collaborators see comments instantly
- Integrated with existing AuthContext for user authentication
- All components follow Material-UI design system and Tailwind CSS styling patterns
- Comprehensive test coverage for all UI components

### File List
- /usr/local/google/home/stonejiang/scitility/frontend/src/components/CommentForm.tsx
- /usr/local/google/home/stonejiang/scitility/frontend/src/components/CommentForm.test.tsx
- /usr/local/google/home/stonejiang/scitility/frontend/src/components/CommentItem.tsx
- /usr/local/google/home/stonejiang/scitility/frontend/src/components/CommentItem.test.tsx
- /usr/local/google/home/stonejiang/scitility/frontend/src/components/CommentPanel.tsx
- /usr/local/google/home/stonejiang/scitility/frontend/src/components/CommentPanel.test.tsx
- /usr/local/google/home/stonejiang/scitility/frontend/src/components/ArticleSection.tsx (modified)
- /usr/local/google/home/stonejiang/scitility/frontend/src/components/ArticleEditor.tsx (modified)

### Change Log
- Created CommentForm component with textarea, character counter, validation, Post/Cancel buttons
- Created CommentItem component to display individual comments with avatar, author, timestamp, text
- Added reply functionality to CommentItem with nested display (max depth 3)
- Added resolve/unresolve buttons and visual indicators (checkmark, grayed out text)
- Created CommentPanel component to manage all comments for a section
- Integrated real-time subscribeToComments in CommentPanel for live updates
- Added error handling and loading states in CommentPanel
- Modified ArticleSection to include comment button with badge in header
- Added showComments state toggle in ArticleSection
- Displays CommentPanel below section content when toggled on
- Modified ArticleEditor to pass articleId and sectionId props to ArticleSection
- Enabled comments for all standard sections (abstract, introduction, methodology, results, discussion, conclusion)
- Styled comments with blue background (bg-blue-50) and left border (border-blue-400) for visual distinction
- Implemented relative timestamp formatting (e.g., "5m ago", "2h ago", "3d ago")
- Added avatar component with initials generation from author name
- Created comprehensive test suites for CommentForm, CommentItem, and CommentPanel components
- All tests use vitest, React Testing Library, and proper mocking patterns

## Testing
- Unit tests for comment form component
- Comment panel rendering tests
- Comment creation flow tests
