# Process Single Epic Command

Process a single epic from the PRD autonomously. This command is designed to be called multiple times, once per epic, with fresh context each time.

## Usage: /process-epic [epic_number]

## INSTRUCTIONS:

You are processing Epic {{epic_number}} in isolation. Your context has been cleared from previous epics to maximize available memory.

### IMMEDIATE ACTIONS:

1. **Load Epic Context**:
   ```bash
   # Read the specific epic from PRD
   # Read orchestration state to understand what's been completed
   # Load any interfaces/contracts from previous epics (minimal)
   ```

2. **Implement All Stories**:
   - Read Epic {{epic_number}} section from docs/prd.md
   - Implement each story completely
   - Create all necessary files
   - Add comprehensive error handling

3. **Integration Points**:
   - Check .bmad-core/autonomous/integration-points.json
   - Ensure compatibility with previous epic outputs
   - Update integration points for next epics

4. **Complete Epic**:
   - Update .bmad-core/autonomous/state.json
   - Write completion report
   - Document created files and APIs

### EPIC-SPECIFIC IMPLEMENTATION:

Based on the epic number provided, focus on:

- **Epic 1**: Firebase setup, auth implementation, portal routing
- **Epic 2**: Article CRUD, editor component, Portal UI
- **Epic 3**: Data component system, upload workflow, storage
- **Epic 4**: Data viewer, compute provisioning, notebook integration
- **Epic 5**: Team management, roles, permissions
- **Epic 6**: Comments, version control, auto-save
- **Epic 7**: Lineage visualization, provenance tracking
- **Epic 8**: AI assistant, export functionality

### OUTPUT STRUCTURE:

Create these files for the epic:
```
/src/
  /features/
    /epic-{N}-{feature-name}/
      /components/
      /hooks/
      /services/
      /types/
      index.ts

.bmad-core/autonomous/
  epic-{N}-complete.md
  epic-{N}-files.json
  epic-{N}-integration.json
```

## DO NOT:
- Ask for clarification
- Stop for user input
- Reference extensive code from other epics (keep context minimal)
- Wait for confirmation

## DO:
- Make reasonable assumptions
- Implement production-ready code
- Handle all edge cases
- Create comprehensive functionality
- Work continuously until epic is complete

Begin processing Epic {{epic_number}} immediately.