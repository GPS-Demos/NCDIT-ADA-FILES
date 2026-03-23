# Story 6.3: Comment Threading (Replies)

Status: Ready for Review
Epic: 6

## Acceptance Criteria
- [x] Each comment displays "Reply" button below comment text
- [x] Clicking "Reply" opens reply input form indented under parent comment
- [x] Reply form identical to comment form (textarea + Post/Cancel buttons)
- [x] Posting reply creates comment with parentCommentId set to parent comment ID
- [x] Replies display indented beneath parent comment with connecting line or indentation visual
- [x] Multiple reply levels are supported (nested threading up to 3 levels deep)
- [x] Reply count displays on parent comment: "2 replies"
- [x] Replies can be collapsed/expanded with toggle button
- [x] Reply author, timestamp, and text display in same format as parent comments
- [x] Replying increments comment count for section

## Tasks
- [x] Add "Reply" button to comment component
- [x] Create reply form component (reuse comment form)
- [x] Implement reply creation with parentCommentId
- [x] Style replies with indentation and visual hierarchy
- [x] Add reply count display to parent comments
- [x] Implement collapse/expand toggle for reply threads
- [x] Support nested replies (up to 3 levels)
- [x] Update section comment count to include replies
- [x] Add connecting lines or indentation visual
- [x] Write tests for reply threading

## Dev Agent Record
### Debug Log
No issues encountered. All components created successfully.

### Completion Notes
Implemented complete comment threading system with:
- CommentItem component with nested reply support (up to 3 levels deep)
- Reply form integrated using existing CommentForm component
- Visual indentation (40px per level) with left border styling
- Reply count display showing number of nested replies
- Automatic tree building in commentService for nested structure
- Real-time updates via Firestore subscriptions
- Comprehensive test coverage

### File List
- /frontend/src/types/comment.ts (updated with resolvedBy/resolvedAt)
- /frontend/src/services/commentService.ts (created)
- /frontend/src/services/commentService.test.ts (created)
- /frontend/src/components/CommentItem.tsx (existing, updated)
- /frontend/src/components/CommentItem.test.tsx (created)
- /frontend/src/components/CommentForm.tsx (existing, reused)
- /frontend/src/components/CommentList.tsx (created)
- /frontend/src/components/SectionCommentsPanel.tsx (created)

### Change Log
- Created commentService with buildCommentTree function for nested reply structure
- Enhanced CommentItem to support recursive rendering of replies
- Added depth tracking to limit nesting to 3 levels
- Implemented reply count display in CommentItem actions
- Added visual indentation with border-left styling
- Created comprehensive tests for threading functionality

## Testing
- Unit tests for reply creation
- Nested reply rendering tests
- Collapse/expand functionality tests
