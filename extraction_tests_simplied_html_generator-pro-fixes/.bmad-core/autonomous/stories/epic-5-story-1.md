# Story 5.1: Collaboration Page & Team Member List

Status: Ready for Review
Epic: 5

## Acceptance Criteria
- [x] Collaboration page loads at /article/:id/collaboration with sidebar navigation
- [x] Page header displays "Team Collaboration" heading and "Manage contributors, reviewers, and permissions" subtitle
- [x] "Invite Collaborator" button displays in top-right (primary purple button)
- [x] "Current Team Members" section displays list of all collaborators
- [x] Each team member card shows: avatar with initials, name, email, role badge (Creator/Contributor/Reviewer), permission description
- [x] Creator/Owner is listed first and marked as non-removable
- [x] Each non-owner collaborator has action buttons: "Change Role", "Remove"
- [x] Role badges are color-coded: Creator (purple), Contributor (blue), Reviewer (green)
- [x] Collaborator data is fetched from article.collaborators[] array in Firestore
- [x] Empty state displays if no collaborators besides owner

## Tasks
- [x] Create collaboration page route and component structure
- [x] Implement team member list UI with avatar, name, email, role badge
- [x] Add Firestore query to fetch article collaborators
- [x] Create role badge component with color coding
- [x] Implement "Invite Collaborator" button in header
- [x] Add action buttons (Change Role, Remove) for non-owner collaborators
- [x] Implement empty state for collaborators list
- [x] Add sidebar navigation integration
- [x] Style page according to design system
- [x] Write tests for collaboration page rendering

## Dev Agent Record
### Debug Log
- No major blockers encountered
- All tests passing (30/30 tests for new components)
- Successfully integrated with existing ArticleEditorPage sidebar navigation
- Empty state logic refined to show creator while displaying empty state message

### Completion Notes
Successfully implemented full collaboration page with team member management UI:
- Created reusable RoleBadge component with color-coded roles (Creator: purple, Contributor: blue, Reviewer: green)
- Built CollaborationPage with complete team member list UI including avatars, names, emails, roles, and permissions
- Integrated sidebar navigation consistent with ArticleEditorPage design
- Implemented empty state for articles with no collaborators
- Added placeholder handlers for Invite, Change Role, and Remove actions (to be implemented in future stories)
- Extended Article types to support displayName and new role values
- All acceptance criteria met and tested

### File List
**Created:**
- /usr/local/google/home/stonejiang/scitility/frontend/src/pages/CollaborationPage.tsx
- /usr/local/google/home/stonejiang/scitility/frontend/src/pages/CollaborationPage.test.tsx
- /usr/local/google/home/stonejiang/scitility/frontend/src/components/RoleBadge.tsx
- /usr/local/google/home/stonejiang/scitility/frontend/src/components/RoleBadge.test.tsx

**Modified:**
- /usr/local/google/home/stonejiang/scitility/frontend/src/App.tsx (added collaboration route)
- /usr/local/google/home/stonejiang/scitility/frontend/src/pages/ArticleEditorPage.tsx (made sidebar navigation clickable)
- /usr/local/google/home/stonejiang/scitility/frontend/src/types/article.ts (extended ArticleCollaborator interface)

### Change Log
1. Created RoleBadge component with color-coded role display
2. Extended ArticleCollaborator type to include displayName and new role types (creator/contributor/reviewer)
3. Built CollaborationPage component with:
   - Sidebar navigation matching ArticleEditorPage
   - Team Collaboration header with subtitle
   - Invite Collaborator button (primary purple)
   - Current Team Members section with member count
   - Team member cards with Avatar, name, email, role badge, permission description
   - Action buttons (Change Role, Remove) for non-owner members
   - Empty state display when only owner exists
4. Added /article/:id/collaboration route to App.tsx
5. Updated ArticleEditorPage sidebar to enable navigation to collaboration page
6. Wrote comprehensive test suite:
   - 4 tests for RoleBadge component (all passing)
   - 26 tests for CollaborationPage component (all passing)
   - Tests cover loading states, error handling, UI rendering, navigation, and user interactions

## Testing
- ✅ Unit tests for RoleBadge component (4/4 passing)
- ✅ Unit tests for CollaborationPage component (26/26 passing)
- ✅ Integration test for fetching collaborators from Firestore
- ✅ UI rendering tests for team member cards
- ✅ Navigation tests for sidebar integration
- ✅ Action button interaction tests
- ✅ Empty state rendering tests
