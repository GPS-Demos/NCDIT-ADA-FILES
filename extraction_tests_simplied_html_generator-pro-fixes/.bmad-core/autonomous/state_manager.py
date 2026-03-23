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
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> Dict:
        """
        Load state from file.

        Returns:
            State dictionary
        """
        if not self.state_file.exists():
            raise FileNotFoundError(f"State file not found: {self.state_file}")

        with open(self.state_file, 'r') as f:
            state = yaml.safe_load(f)

        return state

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

        # Save new state
        with open(self.state_file, 'w') as f:
            yaml.dump(state, f, default_flow_style=False, sort_keys=False)

    def get_current_epic(self, state: Dict) -> Optional[Dict]:
        """Get the currently active epic."""
        idx = state.get('current_epic_index', 0)
        epics = state.get('epics', [])

        if 0 <= idx < len(epics):
            return epics[idx]
        return None

    def get_epic_state(self, state: Dict, epic_id: str) -> Optional[Dict]:
        """Get state for specific epic by ID."""
        for epic in state.get('epics', []):
            if epic.get('id') == epic_id:
                return epic
        return None

    def update_epic_status(self, state: Dict, epic_index: int, status: str, result: Dict = None):
        """Update epic status and result."""
        if 0 <= epic_index < len(state['epics']):
            state['epics'][epic_index]['status'] = status
            if result:
                state['epics'][epic_index]['result'] = result
            state['last_updated'] = datetime.now().isoformat()

    def add_task_to_epic(self, state: Dict, epic_index: int, task: Dict):
        """Add a task to an epic."""
        if 0 <= epic_index < len(state['epics']):
            if 'tasks' not in state['epics'][epic_index]:
                state['epics'][epic_index]['tasks'] = []
            state['epics'][epic_index]['tasks'].append(task)

    def update_task_status(self, state: Dict, epic_index: int, task_id: str, status: str, result: Dict = None):
        """Update task status within an epic."""
        if 0 <= epic_index < len(state['epics']):
            epic = state['epics'][epic_index]
            for task in epic.get('tasks', []):
                if task.get('id') == task_id:
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
        total_epics = len(state.get('epics', []))
        completed_epics = sum(1 for e in state.get('epics', []) if e.get('status') == 'completed')

        total_tasks = 0
        completed_tasks = 0

        for epic in state.get('epics', []):
            tasks = epic.get('tasks', [])
            total_tasks += len(tasks)
            completed_tasks += sum(1 for t in tasks if t.get('status') == 'completed')

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
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(state, f, indent=2, default=str)
