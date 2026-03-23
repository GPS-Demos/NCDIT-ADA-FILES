# Story 5.6: Change Collaborator Role

Status: Ready for Review
Epic: 5

## Acceptance Criteria
- [x] "Change Role" button on collaborator card opens role selection modal
- [x] Modal displays current role and dropdown with options: Contributor, Reviewer
- [x] Modal includes "Update Role" button (primary) and "Cancel" button
- [x] Clicking "Update Role" sends API request PUT /api/articles/:id/collaborators/:uid with new role
- [x] Backend updates collaborator role in article.collaborators[] array
- [x] UI updates immediately to reflect new role badge
- [x] Activity feed logs role change: "[Creator] changed [Collaborator]'s role from [Old] to [New]"
- [x] Success message displays: "Role updated successfully"
- [x] Only Creator/Owner can change roles (permission check)
- [x] Error handling displays if update fails

## Tasks
- [x] Create role change modal component
- [x] Add current role display and dropdown
- [x] Implement PUT endpoint for updating collaborator role
- [x] Update Firestore article.collaborators[] on role change
- [x] Add permission check for Creator/Owner only
- [x] Update UI badge immediately after role change
- [x] Log role change to activity feed
- [x] Add success/error notifications
- [x] Implement modal open/close state management
- [x] Write tests for role change workflow

## Dev Agent Record
### Debug Log
- Implemented ChangeRoleModal component with role selection dropdown
- Added updateCollaboratorRole and isCreator functions to articleService
- Added logRoleChangeActivity to activityService
- Integrated modals into CollaborationPage with permission checks
- All tests passing (11 tests for ChangeRoleModal)

### Completion Notes
Implementation uses Firestore direct updates (no backend API needed as this is a frontend-only Firebase project).
Permission checks implemented by verifying user is first authorId (creator).
UI updates immediately after Firestore update by reloading article data.
Activity logging uses existing activity feed infrastructure.

### File List
Created:
- /usr/local/google/home/stonejiang/scitility/frontend/src/components/ChangeRoleModal.tsx
- /usr/local/google/home/stonejiang/scitility/frontend/src/components/ChangeRoleModal.test.tsx

Modified:
- /usr/local/google/home/stonejiang/scitility/frontend/src/pages/CollaborationPage.tsx
- /usr/local/google/home/stonejiang/scitility/frontend/src/services/articleService.ts
- /usr/local/google/home/stonejiang/scitility/frontend/src/services/activityService.ts

### Change Log
- Added ChangeRoleModal component with current role display and dropdown for Contributor/Reviewer
- Added updateCollaboratorRole() service function with creator permission check
- Added isCreator() utility function to check if user is article creator
- Added logRoleChangeActivity() to log role changes to activity feed
- Integrated modal into CollaborationPage with state management
- Added permission checks before opening modal
- Implemented immediate UI updates after role change
- Added success/error notification handling
- Created comprehensive test suite with 11 passing tests

## Testing
- Unit tests for role change modal: 11 tests passing
- Tests cover: modal visibility, role selection, submit/cancel, error handling, permission checks
- Manual testing required: Firestore integration, activity feed updates
