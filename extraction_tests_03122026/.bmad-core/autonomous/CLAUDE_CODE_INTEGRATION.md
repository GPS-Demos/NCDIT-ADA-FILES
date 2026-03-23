# Claude Code Integration Guide

This guide explains how the autonomous orchestration system integrates with Claude Code.

## Overview

The orchestration system leverages Claude Code's **Task tool** to invoke agents in isolated contexts. This provides:

- **Fresh context windows** for each epic
- **Isolated execution** between agents
- **Structured agent invocation** with clear inputs/outputs
- **Integration with existing BMAD agents**

## Integration Architecture

```
┌─────────────────────────────────────────────┐
│     Autonomous Orchestrator (Python)         │
│  • Manages workflow state                    │
│  • Coordinates agent execution               │
│  • Handles epic progression                  │
└──────────────┬──────────────────────────────┘
               │
               │ Invokes via Task tool
               ▼
┌─────────────────────────────────────────────┐
│         Claude Code Task Tool                │
│  • Spawns agent in fresh context            │
│  • Executes agent with prompt               │
│  • Returns structured result                │
└──────────────┬──────────────────────────────┘
               │
               │ Loads agent definition
               ▼
┌─────────────────────────────────────────────┐
│      BMAD Agent (from .bmad-core/agents/)   │
│  • PM Agent (planning)                       │
│  • Dev Agent (implementation)                │
│  • QA Agent (validation)                     │
│  • Orchestrator Agent (coordination)         │
└─────────────────────────────────────────────┘
```

## How It Works

### 1. Orchestrator Prepares Agent Invocation

```python
# In workflow_controller.py
context = {
    'epic': epic_state['epic'],
    'completed_tasks': [...],
    'remaining_requirements': [...]
}

task_description = """
Analyze the epic requirements and identify the next task...
"""

# Invoke agent
response = agent_invoker.invoke_agent('pm', context, task_description)
```

### 2. Agent Invoker Builds Prompt

```python
# In agent_invoker.py
def invoke_agent(self, agent_id: str, context: Dict, task_description: str):
    # Load agent definition
    agent = self.agents[agent_id]  # From .bmad-core/agents/pm.md

    # Build comprehensive prompt
    prompt = self._build_agent_prompt(agent, context, task_description)

    # Invoke through Claude Code
    response = self._invoke_via_claude_code(agent_id, prompt)

    return response
```

### 3. Claude Code Executes Agent

The prompt instructs Claude Code's Task tool to:
1. Load the agent persona from `.bmad-core/agents/{agent_id}.md`
2. Adopt the agent's role and behavior
3. Process the provided context
4. Execute the requested task
5. Return structured JSON response

### 4. Response Processing

```python
# Agent returns structured response
{
    "decision": "continue",  # or complete_epic, blocked, etc.
    "output": {
        "task": {...},
        "steps": [...],
        "files": [...]
    },
    "artifacts": [...],
    "next_action": "Proceed to implementation..."
}
```

## Implementing the Integration

### Option 1: Using Claude Code Task Tool Directly

To actually invoke Claude Code's Task tool, modify `agent_invoker.py`:

```python
# In agent_invoker.py
def invoke_agent(self, agent_id: str, context: Dict, task_description: str) -> Dict:
    """Invoke agent through Claude Code Task tool."""

    prompt = self._build_agent_prompt(agent, context, task_description)

    # ACTUAL CLAUDE CODE INVOCATION:
    # When running inside Claude Code, you would use the Task tool like this:
    #
    # from claude_code import task_tool
    #
    # result = task_tool.invoke(
    #     subagent_type="general-purpose",
    #     description=f"Execute {agent_id} agent",
    #     prompt=prompt,
    #     model="sonnet"  # or haiku for faster execution
    # )
    #
    # return self._parse_task_result(result)

    # For now, return mock response
    return self._create_mock_response(agent_id, prompt)
```

### Option 2: Running as Subprocess

If Claude Code provides a CLI interface:

```python
import subprocess
import json

def invoke_agent_via_cli(self, agent_id: str, prompt: str) -> Dict:
    """Invoke agent using Claude Code CLI."""

    # Save prompt to temp file
    prompt_file = f'/tmp/agent_prompt_{agent_id}.txt'
    with open(prompt_file, 'w') as f:
        f.write(prompt)

    # Invoke Claude Code CLI
    result = subprocess.run(
        ['claude-code', 'task', '--prompt-file', prompt_file, '--json'],
        capture_output=True,
        text=True
    )

    # Parse result
    return json.loads(result.stdout)
```

### Option 3: API Integration

If Claude Code provides an API:

```python
import requests

def invoke_agent_via_api(self, agent_id: str, prompt: str) -> Dict:
    """Invoke agent using Claude Code API."""

    response = requests.post(
        'http://localhost:8080/api/task',
        json={
            'subagent_type': 'general-purpose',
            'description': f'Execute {agent_id} agent',
            'prompt': prompt,
            'model': 'sonnet'
        },
        headers={'Authorization': f'Bearer {api_token}'}
    )

    return response.json()
```

## Agent Prompt Structure

Each agent receives a prompt in this format:

```
You are being invoked as the {agent_id} agent from the BMAD framework.

Load and adopt the persona from: .bmad-core/agents/{agent_id}.md

## Your Task
{task_description}

## Context
```json
{context}
```

## Instructions
1. Review the context provided above
2. Execute your task according to your agent persona
3. Provide your response in JSON format:

```json
{
  "decision": "continue|complete_epic|blocked|...",
  "output": {
    // Agent-specific outputs
  },
  "artifacts": [],
  "next_action": "..."
}
```

IMPORTANT: Your response must be structured JSON.
```

## Running from Within Claude Code

### Method 1: As a Claude Code Workflow

Create `.claude/commands/autonomous-dev.md`:

```markdown
# Autonomous Development

Execute autonomous development from a PRD using the orchestration system.

## Input
- PRD file path

## Execution
Run the autonomous orchestrator:
```bash
python run_autonomous.py {prd_path}
```

Monitor progress and report completion status.
```

Then use: `/autonomous-dev examples/sample-prd.yaml`

### Method 2: As a Task Agent

The orchestrator itself could be invoked as a Claude Code task:

```python
# From within Claude Code
task_result = task_tool.invoke(
    subagent_type="general-purpose",
    description="Run autonomous development from PRD",
    prompt=f"""
    Execute autonomous development orchestration for the PRD at:
    {prd_path}

    Use the orchestrator system at .bmad-core/autonomous/

    Run: python run_autonomous.py {prd_path}

    Monitor progress and report completion.
    """,
    model="sonnet"
)
```

## State Management Across Invocations

Each agent invocation is stateless, but state is maintained through:

1. **State File**: `.ai/autonomous-state.yaml` persists between invocations
2. **Context Passing**: Each agent receives full context in prompt
3. **Artifacts**: Agent outputs saved to state for next iteration

```python
# Before agent invocation
state = state_manager.load()
context = build_context_from_state(state)

# Invoke agent
response = invoke_agent(agent_id, context, task)

# After agent invocation
state = update_state_with_response(state, response)
state_manager.save(state)
```

## Error Handling

```python
def invoke_agent_with_retry(self, agent_id, context, task, max_retries=3):
    """Invoke agent with automatic retry on failure."""

    for attempt in range(max_retries):
        try:
            response = self.invoke_agent(agent_id, context, task)

            # Validate response structure
            if self._validate_response(response):
                return response
            else:
                self.logger.warning(f"Invalid response format, attempt {attempt + 1}")

        except Exception as e:
            self.logger.error(f"Agent invocation failed: {e}")
            if attempt == max_retries - 1:
                raise

        time.sleep(2 ** attempt)  # Exponential backoff

    raise RuntimeError(f"Agent {agent_id} failed after {max_retries} attempts")
```

## Performance Optimization

### Use Haiku for Simple Tasks

```python
# In config.yaml
agents:
  pm:
    model: sonnet  # Complex planning needs Sonnet
  dev:
    model: sonnet  # Implementation needs Sonnet
  qa:
    model: haiku   # Validation can use faster Haiku
  orchestrator:
    model: haiku   # Coordination can use faster Haiku
```

### Parallel Agent Invocation

For independent tasks, invoke agents in parallel:

```python
import concurrent.futures

def execute_parallel_validation(self, tasks):
    """Validate multiple tasks in parallel."""

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(self.invoke_agent, 'qa', task, 'Validate task'): task
            for task in tasks
        }

        results = []
        for future in concurrent.futures.as_completed(futures):
            task = futures[future]
            try:
                result = future.result()
                results.append((task, result))
            except Exception as e:
                self.logger.error(f"Validation failed for {task}: {e}")

        return results
```

## Debugging Agent Invocations

### Log Agent Prompts

```python
# In agent_invoker.py
self.logger.debug(f"=== Agent Prompt for {agent_id} ===")
self.logger.debug(prompt)
self.logger.debug(f"=== End Prompt ===")
```

### Save Prompts to Files

```python
# Save each prompt for debugging
prompt_file = f'.ai/prompts/{agent_id}_{timestamp}.txt'
Path(prompt_file).parent.mkdir(parents=True, exist_ok=True)
with open(prompt_file, 'w') as f:
    f.write(prompt)
```

### Inspect Agent Responses

```python
# Save raw agent responses
response_file = f'.ai/responses/{agent_id}_{timestamp}.json'
with open(response_file, 'w') as f:
    json.dump(response, f, indent=2)
```

## Security Considerations

1. **Prompt Injection**: Validate and sanitize all context data
2. **File Access**: Agents can access project files - review PRD carefully
3. **Code Execution**: Dev agent executes code - use in trusted environments
4. **Credentials**: Never pass credentials in context

## Testing the Integration

```python
# Test agent invocation
def test_agent_invocation():
    invoker = AgentInvoker('.bmad-core')

    context = {
        'epic': {'title': 'Test Epic'},
        'completed_tasks': []
    }

    task = "Identify next task to implement"

    response = invoker.invoke_agent('pm', context, task)

    assert response['status'] == 'success'
    assert 'decision' in response
    assert 'output' in response
```

## Future Enhancements

1. **Streaming Responses**: Stream agent output in real-time
2. **Agent Collaboration**: Multiple agents working on same task
3. **Feedback Loops**: Agents can request clarification from other agents
4. **Learning**: Agents learn from previous epic completions
5. **Custom Tool Access**: Agents can use specialized tools

## Complete Integration Example

See `claude_code_integration.py` for a complete implementation that can be adapted to your specific Claude Code integration method.

The key is to ensure that:
1. Agents receive complete context
2. Agents return structured responses
3. State is maintained between invocations
4. Errors are handled gracefully
5. Progress is logged and resumable
