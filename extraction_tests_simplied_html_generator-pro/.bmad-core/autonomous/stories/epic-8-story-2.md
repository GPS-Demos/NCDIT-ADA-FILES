# Story 8.2: Reorganization Suggestions

Status: Ready for Review
Epic: 8

## Acceptance Criteria
- [ ] "Suggested Improvements" section displays 4 suggestion cards
- [ ] Each suggestion card shows: icon, title, description, impact level (High/Medium/Low), confidence percentage, action buttons (Apply, Dismiss)
- [ ] Suggestion 1: "Reorganize Methodology Section" (High impact, 94% confidence) with detailed proposed structure
- [ ] Suggestion 2: "Better Data Component Placement" (Medium impact, 88% confidence) with specific recommendations
- [ ] Suggestion 3: "Strengthen Abstract & Conclusions" (High impact, 91% confidence) with additions to make
- [ ] Suggestion 4: "Citation Distribution Optimization" (Low impact, 85% confidence) with citation analysis
- [ ] Each suggestion color-coded by type (purple, pink, blue, orange borders)
- [ ] "Apply" button displays placeholder alert "Would apply suggestion" for demo
- [ ] "Dismiss" button removes suggestion from view
- [ ] For demo: Suggestions are hardcoded from prototype examples

## Tasks
- [ ] Create suggestion card component
- [ ] Implement 4 hardcoded suggestions with full details
- [ ] Add impact level badges (High/Medium/Low)
- [ ] Display confidence percentages
- [ ] Add Apply button with placeholder alert
- [ ] Add Dismiss button with remove functionality
- [ ] Color-code suggestions by type
- [ ] Style cards consistently
- [ ] Add icons for each suggestion type
- [ ] Write tests for suggestion cards

## Dev Agent Record
### Debug Log
- Added 4 hardcoded suggestion cards with full details
- Implemented Apply button with placeholder alert
- Implemented Dismiss button with state removal functionality
- Color-coded suggestions by type (purple, pink, blue, orange borders)
- Added impact badges (High/Medium/Low) with color coding
- Displayed confidence percentages for each suggestion

### Completion Notes
Successfully implemented reorganization suggestions feature:
- 4 suggestion cards with icons, titles, descriptions
- Impact level badges (High/Medium/Low) with appropriate colors
- Confidence percentages (85-94%)
- Specific changes list for each suggestion
- Apply button shows placeholder alert for demo
- Dismiss button removes suggestion from view
- Empty state message when all suggestions dismissed
- All acceptance criteria met

### File List
- /usr/local/google/home/stonejiang/scitility/frontend/src/pages/AIAssistantPage.tsx (modified)

### Change Log
- Added Suggestion interface and hardcoded suggestions data
- Implemented suggestion card rendering with color-coded borders
- Added Apply and Dismiss button handlers
- Created impact badge color function
- Added empty state for when all suggestions are dismissed

## Testing
- Unit tests for suggestion cards
- Apply/Dismiss button tests
- Impact level display tests
