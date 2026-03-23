# Autonomous Development Orchestration - Technical Documentation

## Architecture Overview

This directory contains the autonomous development orchestration system for BMAD.

### Components

```
autonomous/
├── __init__.py                      # Package initialization
├── orchestrator.py                  # Main orchestration engine
├── state_manager.py                 # State persistence & management
├── agent_invoker.py                 # Agent invocation via Claude Code
├── workflow_controller.py           # Workflow loop (PLAN→BUILD→VALIDATE→CHECKPOINT)
├── prd_parser.py                    # PRD parsing (YAML/JSON/Markdown)
├── claude_code_integration.py       # Claude Code Task tool integration
├── config.yaml                      # Configuration file
└── README.md                        # This file
```

## Data Flow

```
PRD File
  ↓
PRDParser.parse()
  ↓
AutonomousOrchestrator.run()
  ↓
For each epic:
  WorkflowController.execute_epic()
    ↓
    Loop:
      1. AgentInvoker.invoke_agent('pm', ...)     → Plan phase
      2. AgentInvoker.invoke_agent('dev', ...)    → Build phase
      3. AgentInvoker.invoke_agent('qa', ...)     → Validate phase
      4. AgentInvoker.invoke_agent('orchestrator', ...) → Checkpoint
    ↓
    StateManager.save()
  ↓
Final Report
```

## State Management

### State Structure

```python
{
  'prd': {...},                    # Parsed PRD
  'epics': [                       # List of epics
    {
      'id': 'epic-1',
      'title': 'Feature Name',
      'status': 'completed',       # pending|running|completed|blocked
      'tasks': [                   # Tasks within epic
        {
          'id': 'task-1',
          'status': 'completed',
          'result': {...}
        }
      ]
    }
  ],
  'current_epic_index': 0,         # Current epic being processed
  'completed_epics': 0,            # Count of completed epics
  'total_tasks_completed': 0,      # Total tasks across all epics
  'iterations': 0,                 # Total iterations
  'status': 'running',             # running|completed|blocked|stopped
  'start_time': '2025-11-03T...',
  'last_updated': '2025-11-03T...',
  'checkpoints': [...]             # Checkpoint history
}
```

### State Persistence

- **File**: `.ai/autonomous-state.yaml`
- **Format**: YAML for human readability
- **Backup**: Automatic backup before each save (`.yaml.bak`)
- **Resume**: Load existing state with `--resume` flag

## Agent Invocation

### Agent Prompt Structure

```
# Agent Activation: {agent_name}

## Role
{agent_title}

## Persona
Role: {persona.role}
Style: {persona.style}
Focus: {persona.focus}

## Task
{task_description}

## Context
{context as JSON}

## Core Principles
- {principle 1}
- {principle 2}

## Output Requirements
{expected JSON response format}
```

### Agent Response Format

```json
{
  "decision": "continue|complete_epic|blocked|...",
  "output": {
    // Agent-specific outputs
  },
  "next_action": "What should happen next",
  "artifacts": [
    // Files, documents, data created
  ]
}
```

## Workflow Loop

### Phase 1: PLAN (PM Agent)

**Input:**
- Epic definition
- Completed tasks
- Remaining requirements

**Process:**
- Analyze requirements
- Identify next task
- Break down into steps
- Define test requirements

**Output:**
- Task definition
- Implementation steps
- Files to modify
- Test requirements
- Decision: continue|complete_epic|blocked

### Phase 2: BUILD (Dev Agent)

**Input:**
- Task definition
- Implementation steps
- Files to modify
- Test requirements

**Process:**
- Implement code
- Write tests
- Run tests (up to 3 attempts)
- Document changes

**Output:**
- Modified files
- Test results
- Implementation notes
- Decision: tests_pass|tests_fail|blocked

### Phase 3: VALIDATE (QA Agent)

**Input:**
- Task implementation
- Build results
- Epic acceptance criteria

**Process:**
- Review code changes
- Verify test coverage
- Check edge cases
- Validate against criteria

**Output:**
- Validation status
- Issues found
- Coverage assessment
- Decision: accept|reject|needs_human_review

### Phase 4: CHECKPOINT (Orchestrator)

**Input:**
- Epic state
- Completed tasks
- Global statistics

**Process:**
- Review progress
- Assess completion
- Determine next action
- Check stop conditions

**Output:**
- Progress summary
- Completion assessment
- Decision: continue|complete|checkpoint|blocked

## Configuration

### Key Settings

```yaml
# Execution limits
max_iterations: 50              # Max iterations per run
checkpoint_frequency: 5         # Checkpoint every N tasks
max_fix_attempts: 3             # Max test fix attempts

# Autonomy
auto_continue_on_checkpoint: true   # Auto-continue at checkpoints
auto_continue_on_blocker: false     # Stop on blockers

# Paths
state_file: .ai/autonomous-state.yaml
bmad_core_path: .bmad-core
```

## Decision Tree

```
PLAN Phase
  ├─ continue → BUILD Phase
  ├─ complete_epic → Next Epic
  └─ blocked → Stop & Report

BUILD Phase
  ├─ tests_pass → VALIDATE Phase
  ├─ tests_fail (attempts < max) → Retry BUILD
  └─ blocked → Stop & Report

VALIDATE Phase
  ├─ accept → CHECKPOINT Phase
  ├─ reject → BUILD Phase (with feedback)
  └─ needs_human_review → Stop & Report

CHECKPOINT Phase
  ├─ continue → PLAN Phase (next task)
  ├─ complete → Next Epic
  ├─ checkpoint → Pause for review
  └─ blocked → Stop & Report
```

## Error Handling

### Recoverable Errors
- Test failures → Retry up to `max_fix_attempts`
- Validation rejection → Return to BUILD with feedback

### Non-Recoverable Errors
- Max iterations reached
- Agent blocked
- Repeated failures after max attempts
- Invalid PRD format

### Recovery Strategy
1. Save current state
2. Log error details
3. Set appropriate status
4. Allow resume with `--resume`

## Integration with Claude Code

### Task Tool Invocation

The system integrates with Claude Code's Task tool to invoke agents:

```python
# Conceptual - actual implementation uses Claude Code's internal APIs
task_result = claude_code.invoke_task(
    agent_type="general-purpose",
    prompt=agent_prompt,
    description=f"Execute {agent_id} agent"
)
```

### Context Management

Each agent invocation:
- Gets fresh context window
- Receives specific task context
- Returns structured output
- Maintains isolation from other agents

## Extending

### Adding New Phases

1. Add phase to workflow configuration
2. Implement `_execute_<phase>_phase()` in `WorkflowController`
3. Define agent invocation
4. Handle phase decisions

### Custom Agents

1. Create agent definition in `.bmad-core/agents/`
2. Register in configuration
3. Use in workflow phases

### Custom PRD Format

1. Add parser method in `PRDParser`
2. Implement `_parse_<format>()` method
3. Return normalized PRD structure

## Testing

### Unit Tests
```bash
# Test PRD parser
python -m pytest tests/test_prd_parser.py

# Test state manager
python -m pytest tests/test_state_manager.py
```

### Integration Tests
```bash
# Run with sample PRD
python run_autonomous.py examples/sample-prd.yaml --validate-only
```

### Dry Run
```bash
# Enable dry-run mode (no actual code changes)
python run_autonomous.py examples/sample-prd.yaml --dry-run
```

## Monitoring

### Real-time Monitoring
```bash
# Watch logs
tail -f .ai/orchestrator.log

# Watch state changes
watch -n 5 'cat .ai/autonomous-state.yaml | grep -A 5 current_epic'
```

### Progress Query
```python
from autonomous import StateManager

state_mgr = StateManager('.ai/autonomous-state.yaml')
state = state_mgr.load()
stats = state_mgr.get_statistics(state)
print(f"Progress: {stats['completed_epics']}/{stats['total_epics']} epics")
```

## Performance Considerations

- **Context Size**: Each epic starts fresh to avoid context bloat
- **Iteration Limits**: Prevents infinite loops with `max_iterations`
- **Checkpoint Frequency**: Balance between autonomy and oversight
- **State Saves**: Automatic backup before each save

## Security Considerations

- **Code Execution**: Agents execute code - review PRD carefully
- **Credentials**: Never include credentials in PRD
- **File Access**: Agents can modify files in project directory
- **External Services**: Be cautious with external API calls

## Debugging

### Enable Debug Logging
```yaml
# In config.yaml
verbose_logging: true
```

### Inspect Agent Prompts
```python
# In agent_invoker.py, set log level to DEBUG
self.logger.setLevel(logging.DEBUG)
```

### Manual State Manipulation
```python
import yaml

with open('.ai/autonomous-state.yaml', 'r') as f:
    state = yaml.safe_load(f)

# Modify state
state['current_epic_index'] = 1

with open('.ai/autonomous-state.yaml', 'w') as f:
    yaml.dump(state, f)
```

## API Reference

See docstrings in each module for detailed API documentation:
- `orchestrator.py` - Main orchestrator class
- `state_manager.py` - State management methods
- `agent_invoker.py` - Agent invocation methods
- `workflow_controller.py` - Workflow execution methods
- `prd_parser.py` - PRD parsing methods
