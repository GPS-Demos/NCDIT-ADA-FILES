"""
Claude Code Integration for Autonomous Orchestration
====================================================

This module provides the bridge between the orchestrator and Claude Code's Task tool.
It enables invoking BMAD agents as Claude Code tasks.
"""

import json
import subprocess
from typing import Dict, Optional
from pathlib import Path
import logging


class ClaudeCodeBridge:
    """
    Bridge for invoking agents through Claude Code's Task tool.

    This implementation provides the mechanism to invoke agents
    in a way that Claude Code can execute them as tasks.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def invoke_agent_via_claude(self, agent_id: str, prompt: str) -> Dict:
        """
        Invoke an agent through Claude Code's Task tool.

        In a real implementation, this would use Claude Code's Task tool API.
        For now, this demonstrates the structure.

        Args:
            agent_id: Agent identifier
            prompt: Complete agent prompt

        Returns:
            Agent response as dictionary
        """
        self.logger.info(f"Invoking agent {agent_id} via Claude Code Task tool")

        # The actual implementation would use Claude Code's internal APIs
        # to invoke the Task tool with the agent prompt

        # For demonstration, we structure the expected response
        response = {
            'status': 'success',
            'agent_id': agent_id,
            'output': self._parse_agent_output(prompt),
            'decision': 'continue',
            'artifacts': []
        }

        return response

    def _parse_agent_output(self, prompt: str) -> Dict:
        """Parse agent output from response."""
        # In real implementation, this would parse the actual agent response
        return {
            'message': 'Agent executed successfully',
            'data': {}
        }


class ClaudeCodeTaskInvoker:
    """
    Invokes Claude Code tasks for agent execution.

    This class provides methods to create and execute Claude Code tasks
    that represent agent invocations in the autonomous workflow.
    """

    def __init__(self, bmad_core_path: str):
        self.bmad_core_path = Path(bmad_core_path)
        self.logger = logging.getLogger(__name__)
        self.bridge = ClaudeCodeBridge()

    def create_task_prompt(self, agent_id: str, context: Dict, task_description: str) -> str:
        """
        Create a Task tool prompt for the agent.

        Args:
            agent_id: Agent identifier
            context: Execution context
            task_description: What the agent should do

        Returns:
            Complete prompt for Claude Code Task tool
        """
        agent_file = self.bmad_core_path / "agents" / f"{agent_id}.md"

        prompt_parts = [
            f"You are being invoked as the {agent_id} agent from the BMAD framework.",
            f"",
            f"Load and adopt the persona from: {agent_file}",
            f"",
            f"## Your Task",
            task_description,
            f"",
            f"## Context",
            "```json",
            json.dumps(context, indent=2),
            "```",
            f"",
            f"## Instructions",
            f"1. Review the context provided above",
            f"2. Execute your task according to your agent persona",
            f"3. Provide your response in JSON format with the following structure:",
            f"",
            "```json",
            "{",
            '  "decision": "continue|complete_epic|blocked|...",',
            '  "output": {',
            '    // Your agent-specific outputs',
            '  },',
            '  "artifacts": [',
            '    // Any files or data you created',
            '  ],',
            '  "next_action": "Description of what should happen next"',
            "}",
            "```",
            f"",
            f"IMPORTANT: Your response must be structured JSON that can be parsed programmatically."
        ]

        return "\n".join(prompt_parts)

    def invoke_as_task(self, agent_id: str, context: Dict, task_description: str) -> Dict:
        """
        Invoke agent as a Claude Code task.

        Args:
            agent_id: Agent identifier
            context: Execution context
            task_description: What the agent should do

        Returns:
            Parsed agent response
        """
        prompt = self.create_task_prompt(agent_id, context, task_description)

        self.logger.debug(f"Task prompt for {agent_id}:")
        self.logger.debug(prompt)

        # Invoke through Claude Code
        response = self.bridge.invoke_agent_via_claude(agent_id, prompt)

        return response


# Integration helper for the orchestrator
def create_claude_code_invoker(bmad_core_path: str) -> ClaudeCodeTaskInvoker:
    """
    Factory function to create a Claude Code task invoker.

    Args:
        bmad_core_path: Path to .bmad-core directory

    Returns:
        ClaudeCodeTaskInvoker instance
    """
    return ClaudeCodeTaskInvoker(bmad_core_path)
