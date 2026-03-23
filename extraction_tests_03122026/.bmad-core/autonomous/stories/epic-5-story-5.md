# Story 5.5: Single-Editor Locking Mechanism

Status: Ready for Review
Epic: 5

## Acceptance Criteria
- [x] When user enters article editor, system checks if article is currently locked
- [x] If unlocked, system sets lock in Firestore: article.currentEditor = {uid, displayName, lockedAt}
- [x] Lock is visible to all users via real-time Firestore listener
- [x] If article is locked by another user, editor displays in read-only mode
- [x] Read-only mode shows banner at top: "Dr. [Name] is currently editing" with orange/yellow background
- [x] All contenteditable elements are disabled (contenteditable="false") in read-only mode
- [x] Toolbar buttons for editing are disabled/grayed out in read-only mode
- [x] User can still navigate, view content, and access other tabs (Collaborators, Data Components) in read-only mode
- [x] Lock is automatically released when user navigates away from editor (onbeforeunload event)
- [x] Lock has timeout (e.g., 30 minutes of inactivity) and auto-releases with warning notification

## Tasks
- [x] Add currentEditor field to article Firestore schema
- [x] Implement lock check on editor page load
- [x] Create lock acquisition logic on editor entry
- [x] Add Firestore real-time listener for lock status
- [x] Implement read-only mode UI with banner
- [x] Disable contenteditable elements in read-only mode
- [x] Disable toolbar buttons in read-only mode
- [x] Implement lock release on page unload (onbeforeunload)
- [x] Add lock timeout mechanism (30 min inactivity)
- [x] Write tests for locking mechanism

## Dev Agent Record
### Debug Log
No major issues encountered. All tests pass successfully.

### Completion Notes
Successfully implemented a comprehensive single-editor locking mechanism for collaborative article editing. The implementation includes:

1. **Lock Acquisition**: When a user enters the article editor, the system attempts to acquire an edit lock. If the article is unlocked or the previous lock has expired (30 minutes), the lock is granted.

2. **Real-time Lock Monitoring**: Using Firestore's onSnapshot listener, all users viewing the article receive real-time updates about lock status changes.

3. **Read-only Mode**: When another user holds the lock, the editor displays in read-only mode with:
   - Orange banner showing who is currently editing
   - All contenteditable elements disabled (set to contenteditable="false")
   - Toolbar editing buttons disabled and grayed out
   - Preview and navigation buttons remain functional

4. **Lock Release**: The lock is automatically released when:
   - User navigates away from the editor
   - Page is closed (onbeforeunload event)
   - Component unmounts
   - 30-minute timeout expires

5. **Lock Timeout**: After 30 minutes of inactivity, the lock automatically expires and the user is notified with an alert, then switched to read-only mode.

6. **Comprehensive Testing**: Added 20+ test cases covering all lock scenarios including acquisition, release, timeout, expiration, and real-time listener functionality.

### File List
**Modified Files:**
- `/usr/local/google/home/stonejiang/scitility/frontend/src/types/article.ts` - Added ArticleEditorLock interface and currentEditor field to Article type
- `/usr/local/google/home/stonejiang/scitility/frontend/src/services/articleService.ts` - Added lock management functions (acquireArticleLock, releaseArticleLock, subscribeToArticle, isLockExpired)
- `/usr/local/google/home/stonejiang/scitility/frontend/src/pages/ArticleEditorPage.tsx` - Implemented lock acquisition, real-time monitoring, read-only mode UI, and cleanup handlers
- `/usr/local/google/home/stonejiang/scitility/frontend/src/services/articleService.test.ts` - Added comprehensive tests for locking mechanism

**New Files:**
None

### Change Log
1. **Article Type Schema (article.ts)**:
   - Added `ArticleEditorLock` interface with uid, displayName, and lockedAt fields
   - Added optional `currentEditor?: ArticleEditorLock` field to Article type

2. **Article Service (articleService.ts)**:
   - Added `LOCK_TIMEOUT_MS` constant (30 minutes)
   - Implemented `acquireArticleLock(articleId, userId, displayName)` function
   - Implemented `releaseArticleLock(articleId, userId)` function
   - Implemented `subscribeToArticle(articleId, callback)` for real-time updates
   - Implemented `isLockExpired(lockedAt)` utility function
   - Updated `documentToArticle()` to properly convert currentEditor field

3. **Article Editor Page (ArticleEditorPage.tsx)**:
   - Added state: `isReadOnly`, `lockAttempted`, and refs for lock tracking
   - Implemented lock acquisition on page load
   - Added real-time listener for lock status changes
   - Implemented 30-minute timeout mechanism with alert notification
   - Added beforeunload event handler for lock release
   - Added read-only banner UI component with orange styling and lock icon
   - Disabled all contenteditable elements in read-only mode
   - Disabled toolbar editing buttons in read-only mode
   - Updated handleBackClick to release lock before navigation

4. **Tests (articleService.test.ts)**:
   - Added 20+ test cases for lock functionality
   - Tests cover: lock acquisition, lock blocking, expired locks, lock release, real-time listeners, and timeout validation
   - All 51 tests pass successfully

## Testing
- [x] Unit tests for lock acquisition/release (8 tests)
- [x] Firestore listener tests for lock status (4 tests)
- [x] Lock timeout tests (4 tests)
- [x] Lock expiration validation tests (4 tests)
- [x] All 51 tests in articleService.test.ts pass
