# Autonomous Build - Leveraging BMAD Dev Agent

This command orchestrates the **FULLY AUTONOMOUS** app generation from your PRD by leveraging the `.bmad-core/agents/dev.md` agent for story implementation. The system processes all 8 epics sequentially with zero user intervention.

## ACTIVATION PROTOCOL

You are now the **AUTONOMOUS BUILD ORCHESTRATOR**. You will:
1. Coordinate epic-by-epic build using the dev agent
2. Generate stories from PRD epics
3. Invoke the dev agent for each story implementation
4. Manage context between epics
5. Continue until the entire app is built

## EXECUTION FRAMEWORK

### Phase 1: Orchestration Setup (2 minutes)

```bash
# Initialize orchestration infrastructure
mkdir -p .bmad-core/autonomous/{epics,stories,state,reports}
mkdir -p src/features

# Create orchestration state
cat > .bmad-core/autonomous/state/orchestration.json << 'EOF'
{
  "mode": "FULLY_AUTONOMOUS",
  "current_epic": 0,
  "total_epics": 8,
  "completed_epics": [],
  "current_story": null,
  "created_files": [],
  "integration_contracts": {},
  "start_time": "$(date -Iseconds)",
  "dev_agent_sessions": []
}
EOF

# Load PRD
export PRD_PATH="requirements/PRD-ScientificPapersData.md"
```

### Phase 2: Epic-to-Story Conversion

For each epic in the PRD, generate executable story files:

```typescript
interface EpicProcessor {
  convertEpicToStories(epicNumber: number): Story[] {
    // 1. Extract epic requirements from PRD
    // 2. Break down into discrete stories
    // 3. Generate story files in BMAD format
    // 4. Each story includes:
    //    - Clear acceptance criteria
    //    - Task breakdown with checkboxes
    //    - Dev Agent Record sections
    //    - Testing requirements
  }
}
```

### Phase 3: Dev Agent Orchestration

For each story, invoke the dev agent to implement:

```bash
# Story implementation loop for each epic
for story in epic_stories; do
  # 1. Create story file in BMAD format
  cat > .bmad-core/autonomous/stories/epic-${EPIC_NUM}-story-${STORY_NUM}.md << 'STORY'
  # Story: [Story Title]
  Status: In Progress
  Epic: ${EPIC_NUM}

  ## Acceptance Criteria
  - [ ] [Specific requirement 1]
  - [ ] [Specific requirement 2]

  ## Tasks
  - [ ] Implement component structure
  - [ ] Add business logic
  - [ ] Create services/hooks
  - [ ] Add error handling
  - [ ] Write tests

  ## Dev Agent Record
  ### Debug Log
  ### Completion Notes
  ### File List
  ### Change Log

  ## Testing
  - Unit tests for all functions
  - Component rendering tests
  - Integration tests
  STORY

  # 2. Invoke dev agent with the story
  echo "Launching dev agent for Epic ${EPIC_NUM}, Story ${STORY_NUM}"

  # Use Task tool to launch dev agent
  # The agent will:
  # - Read the story file
  # - Implement all tasks sequentially
  # - Update story checkboxes
  # - Run tests
  # - Mark story complete

  # 3. Save integration points after completion
  # Extract public APIs and interfaces for next epic
done
```

### Phase 4: Epic-Specific Implementation Using Dev Agent

#### Epic 1: Foundation & Authentication
```bash
# Generate stories for Epic 1
stories=(
  "Setup Firebase project configuration"
  "Implement authentication with Google OAuth and email"
  "Create three portal components (Author/Reviewer/Reader)"
  "Setup routing with role-based access"
  "Create user context and custom hooks"
)

# For each story, create story file and invoke dev agent
for story in "${stories[@]}"; do
  # Create story file with proper BMAD format
  # Invoke dev agent using Task tool:
  Task(
    subagent_type="general-purpose",
    description="Implement story via dev agent",
    prompt="""
    Load and activate the dev agent from .bmad-core/agents/dev.md
    Execute the story file: .bmad-core/autonomous/stories/epic-1-story-X.md
    Use the *develop-story command to implement
    Do not ask any questions - make all assumptions
    Continue until story status is "Ready for Review"
    """
  )
done
```

#### Epic 2: Article Management
```bash
# Stories for article system
stories=(
  "Create Firestore schema for articles"
  "Implement article CRUD operations"
  "Build article editor with contenteditable"
  "Add formatting toolbar with commands"
  "Implement auto-save functionality"
)
# Process with dev agent...
```

#### Epic 3: Data Components
```bash
# Stories for data component system
stories=(
  "Define 4 data component types"
  "Create multi-step upload workflow"
  "Integrate storage providers (Drive/S3/GitHub)"
  "Add cryptographic hashing"
  "Build inline display system"
)
# Process with dev agent...
```

#### Epic 4: Data Viewer
```bash
# Stories for data viewer
stories=(
  "Create tabbed viewer interface"
  "Build dataset preview tables"
  "Implement compute resource selector"
  "Add Colab notebook integration"
  "Create visualization components"
)
# Process with dev agent...
```

#### Epic 5: Collaboration
```bash
# Stories for team features
stories=(
  "Build team management UI"
  "Create invite system with email"
  "Implement role assignment"
  "Add activity feed"
  "Setup permission system"
)
# Process with dev agent...
```

#### Epic 6: Version Control
```bash
# Stories for versioning
stories=(
  "Add inline commenting system"
  "Create version history UI"
  "Implement diff viewer"
  "Add restore functionality"
  "Setup auto-save versioning"
)
# Process with dev agent...
```

#### Epic 7: Data Lineage
```bash
# Stories for lineage tracking
stories=(
  "Build provenance graph"
  "Create lineage visualizer"
  "Add metadata tracking"
  "Implement reproducibility"
  "Create capsule system"
)
# Process with dev agent...
```

#### Epic 8: AI & Export
```bash
# Stories for AI and export
stories=(
  "Integrate AI optimization"
  "Add structure scoring"
  "Implement PDF export with Puppeteer"
  "Add Google Docs export"
  "Create formatting analyzer"
)
# Process with dev agent...
```

## DEV AGENT INVOCATION PROTOCOL

For each story, use the Task tool to launch a dev agent session:

```javascript
async function implementStoryWithDevAgent(epicNum, storyNum, storyFile) {
  // 1. Launch dev agent via Task tool
  const result = await Task({
    subagent_type: "general-purpose",
    description: `Dev agent story ${epicNum}-${storyNum}`,
    model: "haiku", // Use fast model for efficiency
    prompt: `
      # ACTIVATE DEV AGENT FOR AUTONOMOUS STORY IMPLEMENTATION

      1. Load and activate: .bmad-core/agents/dev.md
      2. Read story file: ${storyFile}
      3. Execute: *develop-story
      4. Follow the dev agent protocols:
         - Implement all tasks sequentially
         - Update checkboxes when complete
         - Run tests for validation
         - Update Dev Agent Record sections
      5. Make ALL decisions autonomously:
         - Choose simplest working solutions
         - Use standard patterns (React hooks, TypeScript, Tailwind)
         - Add comprehensive error handling
         - Never ask for clarification
      6. Continue until story status: "Ready for Review"
      7. Return summary of:
         - Created/modified files
         - Public APIs/interfaces
         - Key implementation decisions
    `
  });

  // 2. Extract integration contracts from result
  saveIntegrationContracts(epicNum, result);

  // 3. Update orchestration state
  updateState({
    completedStory: `${epicNum}-${storyNum}`,
    files: result.files
  });
}
```

## CONTEXT MANAGEMENT BETWEEN EPICS

After each epic completes, preserve minimal context:

```javascript
function transitionEpics(currentEpic, nextEpic) {
  // 1. Extract integration contracts from dev agent sessions
  const contracts = {
    epic: currentEpic,
    interfaces: extractPublicAPIs(currentEpic),
    types: extractSharedTypes(currentEpic),
    services: extractServiceContracts(currentEpic)
  };

  // 2. Save for next epic's dev agent sessions
  fs.writeFileSync(
    `.bmad-core/autonomous/epics/epic-${currentEpic}-contracts.json`,
    JSON.stringify(contracts, null, 2)
  );

  // 3. Clear detailed implementation from memory
  // Dev agent sessions are stateless, so context is automatically managed
}
```

## AUTONOMOUS DECISION FRAMEWORK

Provide these rules to each dev agent invocation:

```yaml
decision_rules:
  ambiguous_requirements:
    - Choose simplest working solution
    - Follow React/Firebase best practices
    - Prioritize user experience
    - Document assumption in code comments

  missing_details:
    - Use sensible defaults
    - Follow existing codebase patterns
    - Implement standard behaviors
    - Add TODO comments for refinement

  technical_stack:
    - Frontend: React 18+ with TypeScript
    - Styling: Tailwind CSS
    - Backend: Firebase (Auth, Firestore, Storage, Functions)
    - State: React Context + custom hooks
    - Testing: Jest + React Testing Library
    - Build: Vite
```

## FILE STRUCTURE CONVENTION

```
/src/
  /features/
    /auth/           (Epic 1 - dev agent output)
    /articles/       (Epic 2 - dev agent output)
    /data-components/(Epic 3 - dev agent output)
    /data-viewer/    (Epic 4 - dev agent output)
    /collaboration/  (Epic 5 - dev agent output)
    /version-control/(Epic 6 - dev agent output)
    /lineage/        (Epic 7 - dev agent output)
    /ai-export/      (Epic 8 - dev agent output)
  /shared/
    /components/
    /hooks/
    /services/
    /types/
    /utils/

/.bmad-core/autonomous/
  /state/
    orchestration.json
  /epics/
    epic-*-contracts.json
  /stories/
    epic-*-story-*.md
  /reports/
    epic-*-completion.md
    final-report.md
```

## EXECUTION BEGINS NOW

### DO NOT:
- Ask any questions to the user
- Request clarification
- Wait for approval between stories
- Stop between epics
- Seek user input at any point

### DO:
- Start immediately with Epic 1
- Generate stories from PRD
- Launch dev agent for each story
- Make all decisions autonomously
- Handle all errors gracefully
- Continue relentlessly until done

### YOUR MISSION:
Orchestrate the dev agent to build the entire "Papers with Data" application from the PRD. Process all 8 epics. Complete implementation. Zero intervention.

**BEGIN ORCHESTRATION NOW.**

1. Create orchestration infrastructure
2. Generate stories for Epic 1
3. Launch dev agent for first story
4. Continue until all 8 epics are complete

The dev agent at `.bmad-core/agents/dev.md` will handle all implementation details. Your role is to orchestrate, generate stories, and manage epic transitions.