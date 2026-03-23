"""
Workflow Controller for Autonomous Development
==============================================
Implements the PLAN -> BUILD -> VALIDATE -> CHECKPOINT loop.
"""

import logging
from typing import Dict, Optional
from datetime import datetime

from .agent_invoker import AgentInvoker, AgentResponse
from .state_manager import StateManager


class WorkflowController:
    """Controls the autonomous development workflow loop."""

    def __init__(self, state_manager: StateManager, agent_invoker: AgentInvoker, config: Dict):
        """
        Initialize workflow controller.

        Args:
            state_manager: State manager instance
            agent_invoker: Agent invoker instance
            config: Configuration dictionary
        """
        self.state_manager = state_manager
        self.agent_invoker = agent_invoker
        self.config = config
        self.logger = logging.getLogger(__name__)

    def execute_epic(self, epic: Dict, global_state: Dict) -> Dict:
        """
        Execute workflow for a single epic.

        Args:
            epic: Epic definition
            global_state: Global orchestration state

        Returns:
            Epic execution result
        """
        self.logger.info(f"Starting epic: {epic['title']}")

        # Initialize epic state
        epic_state = {
            'epic': epic,
            'tasks': [],
            'current_task': None,
            'iterations': 0,
            'status': 'running',
            'start_time': datetime.now().isoformat()
        }

        # Main workflow loop: PLAN -> BUILD -> VALIDATE -> CHECKPOINT
        while epic_state['status'] == 'running':
            epic_state['iterations'] += 1
            self.state_manager.increment_iteration(global_state)

            self.logger.info(f"Epic iteration {epic_state['iterations']}")

            # Check iteration limit
            if epic_state['iterations'] > self.config['max_iterations']:
                self.logger.warning("Max iterations reached for epic")
                epic_state['status'] = 'max_iterations_reached'
                break

            # Phase 1: PLAN
            plan_result = self._execute_plan_phase(epic_state, global_state)
            if plan_result['decision'] == 'complete_epic':
                epic_state['status'] = 'completed'
                break
            elif plan_result['decision'] == 'blocked':
                epic_state['status'] = 'blocked'
                epic_state['blocker_reason'] = plan_result.get('blocker_reason', 'Unknown')
                break

            # Phase 2: BUILD
            build_result = self._execute_build_phase(epic_state, plan_result, global_state)
            if build_result['decision'] == 'blocked':
                epic_state['status'] = 'blocked'
                epic_state['blocker_reason'] = build_result.get('blocker_reason', 'Build failed')
                break

            # Phase 3: VALIDATE
            validate_result = self._execute_validate_phase(epic_state, build_result, global_state)
            if validate_result['decision'] == 'reject':
                # Return to BUILD with feedback
                self.logger.info("Validation rejected, retrying build...")
                continue
            elif validate_result['decision'] == 'needs_human_review':
                epic_state['status'] = 'checkpoint'
                break

            # Phase 4: CHECKPOINT
            checkpoint_result = self._execute_checkpoint_phase(epic_state, global_state)
            if checkpoint_result['decision'] == 'complete':
                epic_state['status'] = 'completed'
                break
            elif checkpoint_result['decision'] == 'checkpoint':
                # Pause for human review
                if epic_state['iterations'] % self.config['checkpoint_frequency'] == 0:
                    epic_state['status'] = 'checkpoint'
                    break

            # Continue loop for next task
            self.logger.info("Continuing to next task...")

        # Finalize epic results
        epic_state['end_time'] = datetime.now().isoformat()

        return {
            'status': epic_state['status'],
            'tasks_completed': len(epic_state['tasks']),
            'iterations': epic_state['iterations'],
            'start_time': epic_state['start_time'],
            'end_time': epic_state['end_time'],
            'blocker_reason': epic_state.get('blocker_reason'),
            'tasks': epic_state['tasks']
        }

    def _execute_plan_phase(self, epic_state: Dict, global_state: Dict) -> Dict:
        """
        Execute PLAN phase using PM agent.

        Args:
            epic_state: Current epic state
            global_state: Global state

        Returns:
            Plan result dictionary
        """
        self.logger.info("PHASE: PLAN - Identifying next task")

        context = {
            'epic': epic_state['epic'],
            'completed_tasks': [t for t in epic_state['tasks'] if t.get('status') == 'completed'],
            'remaining_requirements': self._get_remaining_requirements(epic_state),
            'iteration': epic_state['iterations']
        }

        task_description = """
        Analyze the epic requirements and completed tasks to identify the next highest-priority task to implement.

        Your responsibilities:
        1. Review epic acceptance criteria
        2. Identify which requirements are not yet implemented
        3. Select the next task based on dependencies and priority
        4. Break down the task into specific implementation steps
        5. Define test requirements for the task

        Output should include:
        - Task ID and title
        - Implementation steps
        - Files to modify/create
        - Test requirements
        - Decision: 'continue' (more work), 'complete_epic' (all done), or 'blocked' (need help)
        """

        # Invoke PM agent
        response = self.agent_invoker.invoke_agent('pm', context, task_description)

        # Parse response
        plan_result = {
            'decision': response.get('decision', 'continue'),
            'task': response.get('output', {}).get('task'),
            'implementation_steps': response.get('output', {}).get('steps', []),
            'files': response.get('output', {}).get('files', []),
            'test_requirements': response.get('output', {}).get('tests', [])
        }

        if plan_result['task']:
            epic_state['current_task'] = plan_result['task']
            self.logger.info(f"Next task identified: {plan_result['task'].get('title', 'Untitled')}")

        return plan_result

    def _execute_build_phase(self, epic_state: Dict, plan_result: Dict, global_state: Dict) -> Dict:
        """
        Execute BUILD phase using Dev agent.

        Args:
            epic_state: Current epic state
            plan_result: Result from plan phase
            global_state: Global state

        Returns:
            Build result dictionary
        """
        self.logger.info("PHASE: BUILD - Implementing task")

        task = epic_state['current_task']
        if not task:
            return {'decision': 'blocked', 'blocker_reason': 'No task to build'}

        context = {
            'task': task,
            'implementation_steps': plan_result['implementation_steps'],
            'files_to_modify': plan_result['files'],
            'test_requirements': plan_result['test_requirements'],
            'epic_context': epic_state['epic']
        }

        task_description = """
        Implement the planned task according to the implementation steps provided.

        Your responsibilities:
        1. Read and understand the task requirements
        2. Implement the code changes as specified
        3. Write comprehensive tests
        4. Run tests and ensure they pass
        5. Document your implementation

        If tests fail, attempt to fix them (max 3 attempts).

        Output should include:
        - List of files modified/created
        - Test results (pass/fail)
        - Implementation notes
        - Decision: 'tests_pass' (success), 'tests_fail' (after max attempts), or 'blocked' (need help)
        """

        # Invoke Dev agent
        build_attempts = 0
        max_attempts = self.config['max_fix_attempts']

        while build_attempts < max_attempts:
            build_attempts += 1
            self.logger.info(f"Build attempt {build_attempts}/{max_attempts}")

            response = self.agent_invoker.invoke_agent('dev', context, task_description)

            # Check if tests passed
            if response.get('output', {}).get('tests_passed', False):
                self.logger.info("Build successful - tests passed!")
                return {
                    'decision': 'tests_pass',
                    'files_changed': response.get('output', {}).get('files_changed', []),
                    'test_results': response.get('output', {}).get('test_results', {}),
                    'notes': response.get('output', {}).get('notes', '')
                }

            self.logger.warning(f"Tests failed on attempt {build_attempts}")

            # Update context with failure info for retry
            context['previous_failure'] = response.get('output', {}).get('test_results', {})

        # Max attempts reached
        return {
            'decision': 'blocked',
            'blocker_reason': 'Tests failed after max attempts',
            'last_test_results': response.get('output', {}).get('test_results', {})
        }

    def _execute_validate_phase(self, epic_state: Dict, build_result: Dict, global_state: Dict) -> Dict:
        """
        Execute VALIDATE phase using QA agent.

        Args:
            epic_state: Current epic state
            build_result: Result from build phase
            global_state: Global state

        Returns:
            Validation result dictionary
        """
        self.logger.info("PHASE: VALIDATE - Testing against acceptance criteria")

        task = epic_state['current_task']

        context = {
            'task': task,
            'epic': epic_state['epic'],
            'implementation': build_result,
            'files_changed': build_result.get('files_changed', [])
        }

        task_description = """
        Validate the implemented task against the epic's acceptance criteria.

        Your responsibilities:
        1. Review the code changes
        2. Verify tests cover all requirements
        3. Run full test suite if applicable
        4. Check for edge cases and error handling
        5. Validate against epic acceptance criteria

        Output should include:
        - Validation status (pass/fail)
        - Issues found (if any)
        - Coverage assessment
        - Decision: 'accept' (good), 'reject' (needs work), or 'needs_human_review' (uncertain)
        """

        # Invoke QA agent
        response = self.agent_invoker.invoke_agent('qa', context, task_description)

        validate_result = {
            'decision': response.get('decision', 'reject'),
            'validation_status': response.get('output', {}).get('status', 'fail'),
            'issues': response.get('output', {}).get('issues', []),
            'coverage': response.get('output', {}).get('coverage', {})
        }

        if validate_result['decision'] == 'accept':
            self.logger.info("Validation passed!")
            # Mark task as complete
            task['status'] = 'completed'
            task['completed_at'] = datetime.now().isoformat()
            epic_state['tasks'].append(task)
            global_state['total_tasks_completed'] += 1
        else:
            self.logger.warning(f"Validation result: {validate_result['decision']}")

        return validate_result

    def _execute_checkpoint_phase(self, epic_state: Dict, global_state: Dict) -> Dict:
        """
        Execute CHECKPOINT phase using Orchestrator agent.

        Args:
            epic_state: Current epic state
            global_state: Global state

        Returns:
            Checkpoint result dictionary
        """
        self.logger.info("PHASE: CHECKPOINT - Determining next action")

        context = {
            'epic': epic_state['epic'],
            'completed_tasks': epic_state['tasks'],
            'iterations': epic_state['iterations'],
            'global_stats': self.state_manager.get_statistics(global_state)
        }

        task_description = """
        Review progress and determine the next action.

        Your responsibilities:
        1. Review tasks completed in this iteration
        2. Check if epic is complete (all acceptance criteria met)
        3. Determine if human checkpoint is needed
        4. Decide whether to continue or complete

        Output should include:
        - Progress summary
        - Completion assessment
        - Decision: 'continue' (more work), 'complete' (epic done), 'checkpoint' (human review), or 'blocked'
        """

        # Invoke Orchestrator agent
        response = self.agent_invoker.invoke_agent('bmad-orchestrator', context, task_description)

        return {
            'decision': response.get('decision', 'continue'),
            'summary': response.get('output', {}).get('summary', ''),
            'progress': response.get('output', {}).get('progress', {})
        }

    def _get_remaining_requirements(self, epic_state: Dict) -> list:
        """Get list of requirements not yet implemented."""
        completed_task_ids = {t['id'] for t in epic_state['tasks'] if t.get('status') == 'completed'}

        all_requirements = epic_state['epic'].get('requirements', [])
        remaining = [req for req in all_requirements if req.get('id') not in completed_task_ids]

        return remaining
