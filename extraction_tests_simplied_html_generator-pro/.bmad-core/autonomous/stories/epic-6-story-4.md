# Story 6.4: Resolve Comments

Status: Ready for Review
Epic: 6

## Acceptance Criteria
- [x] Each comment displays "Resolve" button (or checkbox "Mark as resolved")
- [x] Clicking resolve button updates comment.resolved = true via API
- [x] Resolved comments display with visual indicator: grayed out text, checkmark icon, "Resolved" badge
- [x] Resolved comments can be filtered/hidden with toggle "Show resolved comments"
- [x] Comment author or article creator can resolve comments (permission check)
- [x] Resolving parent comment also marks all replies as resolved (cascade)
- [x] Resolved comments can be un-resolved (toggle button changes to "Unresolve")
- [x] Activity feed logs comment resolution: "[User] resolved comment in [Section]"
- [x] Comment count excludes resolved comments (or shows "3 active, 2 resolved")
- [x] Resolved state persists across sessions

## Tasks
- [x] Add "Resolve" button/checkbox to comment component
- [x] Implement resolve comment API call
- [x] Update UI to show resolved state (grayed, checkmark, badge)
- [x] Add "Show resolved comments" toggle filter
- [x] Implement permission check (author or creator only)
- [x] Add cascade resolve for parent comment threads
- [x] Implement unresolve functionality
- [x] Log resolution to activity feed
- [x] Update comment count logic to handle resolved
- [x] Write tests for resolve functionality

## Dev Agent Record
### Debug Log
No issues encountered. All features implemented successfully.

### Completion Notes
Implemented complete comment resolution system with:
- Resolve/Unresolve buttons in CommentItem component
- Permission checks: only comment author or article creator can resolve
- Cascade resolution: resolving parent comment resolves all replies via batch update
- Visual indicators: grayed out text, green checkmark icon, "Resolved" badge
- Filter toggle in CommentList: "Show resolved" switch
- Comment count split into "active" and "resolved" chips
- Activity feed integration with logCommentResolutionActivity
- Persistent state via Firestore with resolvedBy, resolvedAt fields
- Real-time updates for resolution state changes

### File List
- /frontend/src/types/comment.ts (updated with resolvedBy/resolvedAt fields)
- /frontend/src/services/commentService.ts (added resolveCommentThread, unresolveCommentThread)
- /frontend/src/services/commentService.test.ts (added resolution tests)
- /frontend/src/services/activityService.ts (added logCommentResolutionActivity)
- /frontend/src/components/CommentItem.tsx (added Resolve/Unresolve button)
- /frontend/src/components/CommentItem.test.tsx (added resolution tests)
- /frontend/src/components/CommentList.tsx (added filter toggle, count logic)
- /frontend/src/components/SectionCommentsPanel.tsx (integrated resolution handlers)

### Change Log
- Added resolvedBy and resolvedAt fields to Comment type
- Created resolveCommentThread function with cascade batch updates
- Created unresolveCommentThread function with cascade batch updates
- Implemented permission check in CommentItem (author or creator only)
- Added visual styling for resolved comments (opacity, green badge)
- Implemented "Show resolved" toggle switch in CommentList
- Created countComments function to split active/resolved counts
- Added activity feed logging for comment resolution
- Ensured resolved state persists via Firestore
- Created comprehensive tests for all resolution features

## Testing
- Unit tests for resolve/unresolve
- Permission check tests
- Cascade resolve tests
- Filter toggle tests
