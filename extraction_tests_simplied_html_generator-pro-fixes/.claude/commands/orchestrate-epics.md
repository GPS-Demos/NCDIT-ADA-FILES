# Epic Orchestration Controller

This command orchestrates the sequential processing of all epics with automatic context management.

## MASTER ORCHESTRATION WORKFLOW

You are the orchestration controller. Your job is to manage the sequential execution of all 8 epics, ensuring each one runs in a fresh context.

### ORCHESTRATION ALGORITHM:

```python
for epic_number in range(1, 9):
    # 1. Save essential integration points
    save_integration_contracts(epic_number - 1)

    # 2. Clear context (simulate fresh session)
    clear_working_memory()

    # 3. Process epic in isolation
    execute_epic(epic_number)

    # 4. Validate completion
    validate_epic_output(epic_number)

    # 5. Update orchestration state
    update_state(epic_number, "complete")
```

### EXECUTION STEPS:

## Step 1: Initialize Orchestration

Create the orchestration infrastructure:

```bash
# Create directories
mkdir -p .bmad-core/autonomous/{sessions,reports,integration}
mkdir -p src/features

# Initialize tracking files
echo '{"current_epic": 0, "completed": [], "in_progress": null, "failed": []}' > .bmad-core/autonomous/state.json
echo '{"epics": {}}' > .bmad-core/autonomous/integration-points.json
echo "# Orchestration Log\n" > .bmad-core/autonomous/orchestration.log
```

## Step 2: Epic Processing Loop

For each epic (1-8), execute:

### A. PREPARE EPIC CONTEXT
```bash
# Minimal context load
echo "Epic $N: Loading minimal context..." >> .bmad-core/autonomous/orchestration.log

# Save only critical integration points from previous epics
cat > .bmad-core/autonomous/sessions/epic-$N-context.json << EOF
{
  "epic_number": $N,
  "dependencies": [/* minimal interfaces from previous epics */],
  "prd_section": "/* relevant PRD excerpt */",
  "start_time": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
```

### B. IMPLEMENT EPIC
```markdown
For Epic $N:
1. Read PRD Epic $N section
2. Create all required components
3. Implement all stories
4. Ensure integration with minimal previous epic interfaces
5. Write comprehensive implementation
```

### C. VALIDATE & DOCUMENT
```bash
# Document what was created
cat > .bmad-core/autonomous/reports/epic-$N-report.md << EOF
# Epic $N Completion Report
## Created Files:
- [list all files created]
## Integration Points:
- [APIs/interfaces exposed for future epics]
## Key Decisions:
- [implementation choices made]
EOF

# Update state
jq '.completed += [$N] | .current_epic = null' .bmad-core/autonomous/state.json > tmp.json && mv tmp.json .bmad-core/autonomous/state.json
```

## Step 3: Context Management Strategy

To simulate fresh context between epics:

### MINIMAL CARRYOVER
Only preserve:
- File system (all created files remain)
- Integration contracts (minimal interface definitions)
- State tracking files

### CLEAR FROM MEMORY
- Detailed implementation code
- Large code blocks
- Extensive PRD sections
- Previous epic's story details

### CONTEXT RESTORATION TECHNIQUE
```javascript
// After each epic, create a minimal interface file
export interface Epic1Contracts {
  // Only the essential interfaces needed by other epics
  AuthService: {
    getCurrentUser(): User;
    requireAuth(): void;
  };
  PortalRouter: {
    navigateToPortal(role: string): void;
  };
}
```

## Step 4: Progressive Implementation

**Epic Execution Order with Dependencies:**

1. **Epic 1** → Creates: Auth, Firebase setup, Portal routing
2. **Epic 2** → Uses: Auth, Portals → Creates: Article CRUD, Editor
3. **Epic 3** → Uses: Articles → Creates: Data Components
4. **Epic 4** → Uses: Data Components → Creates: Data Viewer, Compute
5. **Epic 5** → Uses: Auth, Articles → Creates: Teams, Roles
6. **Epic 6** → Uses: Articles, Teams → Creates: Comments, Versions
7. **Epic 7** → Uses: Data Components → Creates: Lineage, Provenance
8. **Epic 8** → Uses: Articles → Creates: AI, Export

## Step 5: Autonomous Execution

**NOW EXECUTE THE FOLLOWING:**

1. Initialize orchestration infrastructure
2. Start with Epic 1
3. After Epic 1 completes, note only essential interfaces
4. Clear detailed implementation from memory
5. Load Epic 2 with minimal Epic 1 interfaces
6. Continue this pattern through Epic 8
7. Generate final report

## CRITICAL RULES:

- **NO USER INTERVENTION**: Execute all 8 epics automatically
- **MAKE ASSUMPTIONS**: Decide on implementation details without asking
- **FRESH CONTEXT**: Treat each epic as if starting a new session
- **MINIMAL DEPENDENCIES**: Only carry forward essential interfaces
- **COMPLETE IMPLEMENTATION**: Each epic must be fully functional
- **CONTINUOUS EXECUTION**: Do not stop between epics

## BEGIN ORCHESTRATION NOW

Start with initialization, then process Epic 1. Continue automatically through all 8 epics without stopping.

The app must be fully built by the end of this orchestration.