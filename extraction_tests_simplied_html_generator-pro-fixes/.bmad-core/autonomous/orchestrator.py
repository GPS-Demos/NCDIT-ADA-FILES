#!/usr/bin/env python3
"""
BMAD Autonomous Development Orchestrator
=========================================
Orchestrates fully autonomous development from PRD to finished application.

Workflow: PRD -> Epics -> For each epic: PLAN -> BUILD -> VALIDATE -> CHECKPOINT (loop)
"""

import json
import yaml
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from .state_manager import StateManager
from .agent_invoker import AgentInvoker
from .workflow_controller import WorkflowController
from .prd_parser import PRDParser


class AutonomousOrchestrator:
    """Main orchestrator for autonomous development workflow."""

    def __init__(self, config_path: str = None):
        """Initialize the orchestrator with configuration."""
        self.config = self._load_config(config_path)
        self.state_manager = StateManager(self.config['state_file'])
        self.agent_invoker = AgentInvoker(self.config['bmad_core_path'])
        self.workflow_controller = WorkflowController(
            self.state_manager,
            self.agent_invoker,
            self.config
        )

        # Setup logging
        self._setup_logging()
        self.logger = logging.getLogger(__name__)

    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load orchestrator configuration."""
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Set defaults
        config.setdefault('state_file', '.ai/autonomous-state.yaml')
        config.setdefault('bmad_core_path', '.bmad-core')
        config.setdefault('max_iterations', 50)
        config.setdefault('checkpoint_frequency', 5)
        config.setdefault('max_fix_attempts', 3)
        config.setdefault('verbose_logging', True)

        return config

    def _setup_logging(self):
        """Configure logging for the orchestrator."""
        log_level = logging.DEBUG if self.config['verbose_logging'] else logging.INFO

        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('.ai/orchestrator.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )

    def run(self, prd_path: str, resume: bool = False) -> Dict:
        """
        Main entry point for autonomous development.

        Args:
            prd_path: Path to the PRD document
            resume: Whether to resume from previous state

        Returns:
            Final execution report
        """
        self.logger.info("=" * 80)
        self.logger.info("BMAD AUTONOMOUS ORCHESTRATOR - Starting")
        self.logger.info("=" * 80)

        try:
            # Initialize or resume state
            if resume:
                self.logger.info("Resuming from previous state...")
                state = self.state_manager.load()
            else:
                self.logger.info(f"Parsing PRD from {prd_path}...")
                prd = PRDParser.parse(prd_path)
                state = self._initialize_state(prd)
                self.state_manager.save(state)

            self.logger.info(f"Total epics to complete: {len(state['epics'])}")
            self.logger.info(f"Current epic: {state['current_epic_index'] + 1}")

            # Main orchestration loop
            while not self._is_complete(state):
                current_epic = state['epics'][state['current_epic_index']]

                self.logger.info("\n" + "=" * 80)
                self.logger.info(f"EPIC {state['current_epic_index'] + 1}/{len(state['epics'])}: {current_epic['title']}")
                self.logger.info("=" * 80)

                # Execute workflow for current epic
                epic_result = self.workflow_controller.execute_epic(
                    current_epic,
                    state
                )

                # Update state
                state['epics'][state['current_epic_index']]['status'] = epic_result['status']
                state['epics'][state['current_epic_index']]['result'] = epic_result

                if epic_result['status'] == 'completed':
                    self.logger.info(f"Epic {current_epic['title']} completed successfully!")
                    state['current_epic_index'] += 1
                    state['completed_epics'] += 1
                elif epic_result['status'] == 'blocked':
                    self.logger.warning(f"Epic {current_epic['title']} is blocked.")
                    if self._handle_blocker(state, epic_result):
                        continue  # Retry after human intervention
                    else:
                        break  # Stop orchestration
                elif epic_result['status'] == 'checkpoint':
                    self.logger.info("Checkpoint reached - waiting for human approval...")
                    if self._handle_checkpoint(state, epic_result):
                        continue  # Continue after approval
                    else:
                        break  # Stop orchestration

                # Save state after each epic
                self.state_manager.save(state)

            # Generate final report
            report = self._generate_final_report(state)
            self.logger.info("\n" + "=" * 80)
            self.logger.info("ORCHESTRATION COMPLETE")
            self.logger.info("=" * 80)

            return report

        except Exception as e:
            self.logger.error(f"Orchestration failed with error: {str(e)}", exc_info=True)
            raise

    def _initialize_state(self, prd: Dict) -> Dict:
        """Initialize orchestration state from PRD."""
        return {
            'prd': prd,
            'epics': prd['epics'],
            'current_epic_index': 0,
            'completed_epics': 0,
            'total_tasks_completed': 0,
            'start_time': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'status': 'running',
            'iterations': 0
        }

    def _is_complete(self, state: Dict) -> bool:
        """Check if all epics are complete."""
        if state['current_epic_index'] >= len(state['epics']):
            return True
        if state['iterations'] >= self.config['max_iterations']:
            self.logger.warning("Max iterations reached!")
            return True
        if state['status'] in ['failed', 'stopped']:
            return True
        return False

    def _handle_blocker(self, state: Dict, epic_result: Dict) -> bool:
        """
        Handle blocked epic - request human intervention.

        Returns:
            True if should continue, False if should stop
        """
        self.logger.warning("\n" + "!" * 80)
        self.logger.warning("BLOCKER DETECTED")
        self.logger.warning("!" * 80)
        self.logger.warning(f"Reason: {epic_result.get('blocker_reason', 'Unknown')}")
        self.logger.warning(f"Details: {epic_result.get('blocker_details', 'No details')}")

        if self.config.get('auto_continue_on_blocker', False):
            return False

        # In autonomous mode, we log and stop
        state['status'] = 'blocked'
        self.state_manager.save(state)
        return False

    def _handle_checkpoint(self, state: Dict, epic_result: Dict) -> bool:
        """
        Handle checkpoint - provide status update.

        Returns:
            True if should continue, False if should stop
        """
        self.logger.info("\n" + "*" * 80)
        self.logger.info("CHECKPOINT")
        self.logger.info("*" * 80)
        self.logger.info(f"Epics completed: {state['completed_epics']}/{len(state['epics'])}")
        self.logger.info(f"Tasks completed: {state['total_tasks_completed']}")
        self.logger.info(f"Current status: {epic_result.get('summary', 'In progress')}")

        if self.config.get('auto_continue_on_checkpoint', True):
            self.logger.info("Auto-continuing after checkpoint...")
            return True

        # In fully autonomous mode, continue automatically
        return True

    def _generate_final_report(self, state: Dict) -> Dict:
        """Generate final orchestration report."""
        report = {
            'status': 'completed' if state['completed_epics'] == len(state['epics']) else 'partial',
            'total_epics': len(state['epics']),
            'completed_epics': state['completed_epics'],
            'total_tasks': state['total_tasks_completed'],
            'start_time': state['start_time'],
            'end_time': datetime.now().isoformat(),
            'iterations': state['iterations'],
            'epics': []
        }

        for epic in state['epics']:
            report['epics'].append({
                'title': epic['title'],
                'status': epic.get('status', 'pending'),
                'tasks_completed': epic.get('result', {}).get('tasks_completed', 0)
            })

        # Save report
        report_path = Path('.ai/autonomous-report.json')
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        self.logger.info(f"Final report saved to {report_path}")

        return report


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='BMAD Autonomous Development Orchestrator'
    )
    parser.add_argument('prd', help='Path to PRD document')
    parser.add_argument('--resume', action='store_true', help='Resume from previous state')
    parser.add_argument('--config', help='Path to config file')

    args = parser.parse_args()

    orchestrator = AutonomousOrchestrator(config_path=args.config)
    report = orchestrator.run(args.prd, resume=args.resume)

    print("\n" + "=" * 80)
    print("ORCHESTRATION COMPLETE")
    print("=" * 80)
    print(f"Status: {report['status']}")
    print(f"Completed: {report['completed_epics']}/{report['total_epics']} epics")
    print(f"Total tasks: {report['total_tasks']}")
    print("=" * 80)


if __name__ == '__main__':
    main()
