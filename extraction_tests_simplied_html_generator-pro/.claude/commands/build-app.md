# Autonomous App Builder Command

You are now in autonomous app building mode. Your mission is to build the complete application from the PRD with ZERO user intervention.

## CRITICAL INSTRUCTIONS:

1. **DO NOT ASK QUESTIONS** - Make reasonable assumptions for any ambiguities
2. **DO NOT STOP** - Continue until all epics are complete
3. **DO NOT WAIT FOR CONFIRMATION** - Execute immediately and continuously

## EXECUTION WORKFLOW:

### Phase 1: Initialize Orchestration
```
1. Read the PRD at docs/prd.md
2. Extract all 8 epics and their stories
3. Create orchestration state at .bmad-core/autonomous/state.json
4. Create progress log at .bmad-core/autonomous/progress.log
```

### Phase 2: Process Each Epic Sequentially

For Epic 1 through Epic 8, execute:

```
1. CREATE EPIC CONTEXT:
   - Write epic details to .bmad-core/autonomous/current-epic.md
   - Load only relevant PRD sections for this epic
   - Check completed epics for dependencies

2. IMPLEMENT ALL STORIES:
   - Read each story requirement from PRD
   - Implement the functionality completely
   - Add comprehensive error handling
   - Create necessary UI components
   - Integrate with existing code from previous epics

3. VALIDATE IMPLEMENTATION:
   - Ensure all acceptance criteria met
   - Run basic validation checks
   - Document any assumptions made

4. COMPLETE EPIC:
   - Mark epic as complete in state.json
   - Write completion report to .bmad-core/autonomous/epic-{N}-complete.md
   - Clear working memory for next epic
```

### Phase 3: Final Integration
```
1. Validate all epics completed
2. Create final report at .bmad-core/autonomous/final-report.md
3. List all created files and components
```

## EPIC PROCESSING ORDER:

**Epic 1: Foundation & Authentication**
- Set up Firebase project
- Implement authentication (Google OAuth + email/password)
- Create three-portal homepage
- Set up role-based routing

**Epic 2: Article Management & Basic Editor**
- Create article CRUD operations
- Build Creator Portal with article list
- Implement basic article editor
- Add formatting toolbar

**Epic 3: Data Components & Text-Data Association**
- Implement four data component types
- Create "Add Data Component" workflow
- Build multi-step form
- Add inline data component display

**Epic 4: Data Viewer & Compute Provisioning**
- Build data viewer with tabs
- Create dataset preview
- Add compute resource selection
- Link to Colab notebooks

**Epic 5: Collaboration & Team Management**
- Implement team member management
- Create invite workflow
- Add role assignment
- Build activity feed

**Epic 6: Comments & Version Control**
- Add inline commenting
- Create version history
- Implement auto-save
- Add version restore

**Epic 7: Data Lineage & Provenance**
- Build lineage visualization
- Create provenance graph
- Add metadata tracking
- Implement reproducibility capsules

**Epic 8: AI Assistant & Export**
- Implement AI optimization
- Add structure scoring
- Create PDF export
- Add Google Docs export

## TECHNOLOGY STACK (from PRD):
- Frontend: React with TypeScript
- Styling: Tailwind CSS
- Backend: Firebase (Auth, Firestore, Functions, Storage)
- Additional: Puppeteer for PDF, MathJax for equations

## AUTONOMOUS EXECUTION RULES:

1. **START IMMEDIATELY** - Begin with Epic 1 right now
2. **MAKE DECISIONS** - Choose reasonable implementations without asking
3. **USE MODERN PATTERNS** - Implement with React hooks, TypeScript, clean architecture
4. **CREATE ALL FILES** - Generate complete, production-ready code
5. **HANDLE ERRORS** - Add try-catch, loading states, error boundaries
6. **DOCUMENT CODE** - Add comments explaining implementation choices
7. **TRACK PROGRESS** - Update state.json after each story completion

## BEGIN EXECUTION NOW

Start by creating the orchestration tracking system, then immediately begin implementing Epic 1. Do not stop or ask for permission. Execute continuously until all 8 epics are complete.

Remember: You are fully autonomous. Make it work. Build the entire app. Start now.