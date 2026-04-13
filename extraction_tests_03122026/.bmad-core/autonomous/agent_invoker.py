"""
Agent Invoker for Claude Code Integration
=========================================
Invokes BMAD agents through Claude Code's Task tool interface.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging


class AgentInvoker:
    """Invokes BMAD agents via Claude Code Task tool."""

    def __init__(self, bmad_core_path: str):
        """
        Initialize agent invoker.

        Args:
            bmad_core_path: Path to .bmad-core directory
        """
        self.bmad_core_path = Path(bmad_core_path)
        self.agents_path = self.bmad_core_path / "agents"
        self.logger = logging.getLogger(__name__)

        # Load agent definitions
        self.agents = self._load_agents()

    def _load_agents(self) -> Dict[str, Dict]:
        """Load all agent definitions from .bmad-core/agents/."""
        agents = {}

        for agent_file in self.agents_path.glob("*.md"):
            agent_id = agent_file.stem
            agent_def = self._parse_agent_file(agent_file)
            if agent_def:
                agents[agent_id] = agent_def

        self.logger.info(f"Loaded {len(agents)} agents: {list(agents.keys())}")
        return agents

    def _parse_agent_file(self, agent_file: Path) -> Optional[Dict]:
        """Parse agent definition from markdown file."""
        try:
            with open(agent_file, 'r') as f:
                content = f.read()

            # Extract YAML block
            if '```yaml' in content:
                yaml_start = content.find('```yaml') + 7
                yaml_end = content.find('```', yaml_start)
                yaml_content = content[yaml_start:yaml_end].strip()

                agent_def = yaml.safe_load(yaml_content)
                return agent_def
            else:
                self.logger.warning(f"No YAML block found in {agent_file}")
                return None

        except Exception as e:
            self.logger.error(f"Failed to parse agent file {agent_file}: {e}")
            return None

    def invoke_agent(self, agent_id: str, context: Dict, task_description: str) -> Dict:
        """
        Invoke an agent with given context.

        Args:
            agent_id: Agent identifier (pm, dev, qa, etc.)
            context: Context dictionary with all necessary information
            task_description: Description of what the agent should do

        Returns:
            Agent response dictionary
        """
        if agent_id not in self.agents:
            raise ValueError(f"Unknown agent: {agent_id}")

        agent = self.agents[agent_id]
        agent_name = agent.get('agent', {}).get('name', agent_id)

        self.logger.info(f"Invoking agent: {agent_name} ({agent_id})")

        # Build agent prompt
        prompt = self._build_agent_prompt(agent, context, task_description)

        # In a real implementation, this would use Claude Code's Task tool
        # For now, we'll return a simulated response structure
        self.logger.info(f"Agent prompt built: {len(prompt)} characters")

        # This is where Claude Code's Task tool would be invoked
        # The Task tool would execute the agent in a new context
        response = {
            'agent_id': agent_id,
            'agent_name': agent_name,
            'status': 'success',
            'prompt': prompt,
            'context': context,
            'task': task_description,
            # In real implementation, these would be populated by the agent's actual response
            'output': {},
            'decision': None,
            'artifacts': []
        }

        return response

    def _build_agent_prompt(self, agent: Dict, context: Dict, task_description: str) -> str:
        """
        Build a comprehensive prompt for the agent.

        Args:
            agent: Agent definition
            context: Execution context
            task_description: What the agent should do

        Returns:
            Complete agent prompt
        """
        agent_info = agent.get('agent', {})
        persona = agent.get('persona', {})

        prompt_parts = [
            f"# Agent Activation: {agent_info.get('name', 'Agent')}",
            f"",
            f"## Role",
            f"{agent_info.get('title', 'Specialist')}",
            f"",
            f"## Persona",
            f"Role: {persona.get('role', 'Specialist')}",
            f"Style: {persona.get('style', 'Professional')}",
            f"Focus: {persona.get('focus', 'Task completion')}",
            f"",
            f"## Task",
            f"{task_description}",
            f"",
            f"## Context",
        ]

        # Add context information
        for key, value in context.items():
            if isinstance(value, (dict, list)):
                prompt_parts.append(f"### {key}")
                prompt_parts.append(f"```json")
                prompt_parts.append(json.dumps(value, indent=2))
                prompt_parts.append(f"```")
            else:
                prompt_parts.append(f"### {key}")
                prompt_parts.append(f"{value}")
            prompt_parts.append("")

        # Add core principles
        if 'core_principles' in persona:
            prompt_parts.append("## Core Principles")
            for principle in persona.get('core_principles', []):
                prompt_parts.append(f"- {principle}")
            prompt_parts.append("")

        # Add output requirements
        prompt_parts.extend([
            "## Output Requirements",
            "Please provide your response in the following JSON format:",
            "```json",
            "{",
            '  "decision": "continue|complete_epic|all_complete|blocked|...",',
            '  "output": {',
            '    // Agent-specific outputs',
            "  },",
            '  "next_action": "Description of what should happen next",',
            '  "artifacts": [',
            '    // Any files, documents, or data created',
            "  ]",
            "}",
            "```"
        ])

        return "\n".join(prompt_parts)

    def get_available_agents(self) -> List[str]:
        """Get list of available agent IDs."""
        return list(self.agents.keys())

    def get_agent_info(self, agent_id: str) -> Optional[Dict]:
        """Get information about a specific agent."""
        return self.agents.get(agent_id)


class AgentResponse:
    """Wrapper for agent responses with convenience methods."""

    def __init__(self, response: Dict):
        self.raw = response
        self.agent_id = response.get('agent_id')
        self.status = response.get('status')
        self.output = response.get('output', {})
        self.decision = response.get('decision')
        self.artifacts = response.get('artifacts', [])

    def is_success(self) -> bool:
        """Check if agent execution was successful."""
        return self.status == 'success'

    def is_blocked(self) -> bool:
        """Check if agent is blocked."""
        return self.decision == 'blocked'

    def is_complete(self) -> bool:
        """Check if agent completed the task."""
        return self.decision in ['complete', 'complete_epic', 'all_complete']

    def should_continue(self) -> bool:
        """Check if workflow should continue."""
        return self.decision == 'continue'

    def get_artifact(self, artifact_type: str) -> Optional[Any]:
        """Get specific artifact by type."""
        for artifact in self.artifacts:
            if artifact.get('type') == artifact_type:
                return artifact.get('content')
        return None
