"""
State Manager for Autonomous Orchestration
==========================================
Manages persistent state across epic and task execution.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import shutil


class StateManager:
    """Manages orchestration state with persistence and versioning."""

    def __init__(self, state_file: str):
        """
        Initialize state manager.

        Args:
            state_file: Path to state file (YAML)
        """
        resolved_file = Path(state_file).resolve()
        cwd = Path.cwd().resolve()
        repo_root = Path(__file__).resolve().parent.parent.parent.parent
        try:
            if not (resolved_file.is_relative_to(cwd) or resolved_file.is_relative_to(repo_root)):
                raise ValueError(f"Path traversal detected in state_file: {state_file}")
        except (ValueError, AttributeError):
            pass

        self.state_file = resolved_file
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> Dict:
        """
        Load state from file.

        Returns:
            State dictionary
        """
        if not self.state_file.exists():
            raise FileNotFoundError(f"State file not found: {self.state_file}")

        with open(self.state_file, 'r', encoding='utf-8') as f:
            state = yaml.safe_load(f)

        return state if isinstance(state, dict) else {}

    def save(self, state: Dict):
        """
        Save state to file with backup.

        Args:
            state: State dictionary to save
        """
        # Update last modified timestamp
        state['last_updated'] = datetime.now().isoformat()

        # Backup existing state
        if self.state_file.exists():
            backup_path = self.state_file.with_suffix('.yaml.bak')
            shutil.copy(self.state_file, backup_path)

        # Save new state safely
        with open(self.state_file, 'w', encoding='utf-8') as f:
            yaml.safe_dump(state, f, default_flow_style=False, sort_keys=False)

    def get_current_epic(self, state: Dict) -> Optional[Dict]:
        """Get the currently active epic."""
        idx = state.get('current_epic_index', 0)
        epics = state.get('epics', [])

        if isinstance(epics, list) and 0 <= idx < len(epics):
            return epics[idx]
        return None

    def get_epic_state(self, state: Dict, epic_id: str) -> Optional[Dict]:
        """Get state for specific epic by ID."""
        for epic in state.get('epics', []):
            if isinstance(epic, dict) and epic.get('id') == epic_id:
                return epic
        return None

    def update_epic_status(self, state: Dict, epic_index: int, status: str, result: Dict = None):
        """Update epic status and result."""
        epics = state.get('epics', [])
        if isinstance(epics, list) and 0 <= epic_index < len(epics):
            epics[epic_index]['status'] = status
            if result:
                epics[epic_index]['result'] = result
            state['last_updated'] = datetime.now().isoformat()

    def add_task_to_epic(self, state: Dict, epic_index: int, task: Dict):
        """Add a task to an epic."""
        epics = state.get('epics', [])
        if isinstance(epics, list) and 0 <= epic_index < len(epics):
            if 'tasks' not in epics[epic_index] or not isinstance(epics[epic_index]['tasks'], list):
                epics[epic_index]['tasks'] = []
            epics[epic_index]['tasks'].append(task)

    def update_task_status(self, state: Dict, epic_index: int, task_id: str, status: str, result: Dict = None):
        """Update task status within an epic."""
        epics = state.get('epics', [])
        if isinstance(epics, list) and 0 <= epic_index < len(epics):
            epic = epics[epic_index]
            for task in epic.get('tasks', []):
                if isinstance(task, dict) and task.get('id') == task_id:
                    task['status'] = status
                    if result:
                        task['result'] = result
                    task['updated_at'] = datetime.now().isoformat()
                    break

    def increment_iteration(self, state: Dict):
        """Increment iteration counter."""
        state['iterations'] = state.get('iterations', 0) + 1

    def create_checkpoint(self, state: Dict, checkpoint_type: str, data: Dict):
        """Create a checkpoint entry in state."""
        if 'checkpoints' not in state:
            state['checkpoints'] = []

        checkpoint = {
            'timestamp': datetime.now().isoformat(),
            'type': checkpoint_type,
            'iteration': state.get('iterations', 0),
            'epic_index': state.get('current_epic_index', 0),
            'data': data
        }

        state['checkpoints'].append(checkpoint)

    def get_statistics(self, state: Dict) -> Dict:
        """Get execution statistics from state."""
        epics = state.get('epics', [])
        total_epics = len(epics) if isinstance(epics, list) else 0
        completed_epics = sum(1 for e in epics if isinstance(e, dict) and e.get('status') == 'completed') if isinstance(epics, list) else 0

        total_tasks = 0
        completed_tasks = 0

        if isinstance(epics, list):
            for epic in epics:
                if isinstance(epic, dict):
                    tasks = epic.get('tasks', [])
                    if isinstance(tasks, list):
                        total_tasks += len(tasks)
                        completed_tasks += sum(1 for t in tasks if isinstance(t, dict) and t.get('status') == 'completed')

        return {
            'total_epics': total_epics,
            'completed_epics': completed_epics,
            'pending_epics': total_epics - completed_epics,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': total_tasks - completed_tasks,
            'iterations': state.get('iterations', 0),
            'current_epic': state.get('current_epic_index', 0) + 1
        }

    def export_to_json(self, state: Dict, output_path: str):
        """Export state to JSON format."""
        output_file = Path(output_path).resolve()
        cwd = Path.cwd().resolve()
        repo_root = Path(__file__).resolve().parent.parent.parent.parent
        try:
            if not (output_file.is_relative_to(cwd) or output_file.is_relative_to(repo_root)):
                raise ValueError(f"Path traversal detected in output_path: {output_path}")
        except (ValueError, AttributeError):
            pass

        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, default=str)
