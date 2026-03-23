"""
PRD Parser for Autonomous Orchestration
=======================================
Parses Product Requirements Documents and extracts epics/features.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List
import re


class PRDParser:
    """Parses PRD documents to extract structured requirements."""

    @staticmethod
    def parse(prd_path: str) -> Dict:
        """
        Parse PRD from file.

        Args:
            prd_path: Path to PRD file (YAML, JSON, or Markdown)

        Returns:
            Structured PRD dictionary with epics
        """
        prd_file = Path(prd_path)

        if not prd_file.exists():
            raise FileNotFoundError(f"PRD file not found: {prd_path}")

        # Determine file type and parse accordingly
        if prd_file.suffix in ['.yaml', '.yml']:
            return PRDParser._parse_yaml(prd_file)
        elif prd_file.suffix == '.json':
            return PRDParser._parse_json(prd_file)
        elif prd_file.suffix in ['.md', '.markdown']:
            return PRDParser._parse_markdown(prd_file)
        else:
            raise ValueError(f"Unsupported PRD file format: {prd_file.suffix}")

    @staticmethod
    def _parse_yaml(prd_file: Path) -> Dict:
        """Parse YAML PRD."""
        with open(prd_file, 'r') as f:
            prd_data = yaml.safe_load(f)

        return PRDParser._normalize_prd(prd_data)

    @staticmethod
    def _parse_json(prd_file: Path) -> Dict:
        """Parse JSON PRD."""
        with open(prd_file, 'r') as f:
            prd_data = json.load(f)

        return PRDParser._normalize_prd(prd_data)

    @staticmethod
    def _parse_markdown(prd_file: Path) -> Dict:
        """Parse Markdown PRD."""
        with open(prd_file, 'r') as f:
            content = f.read()

        # Extract title
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else "Untitled PRD"

        # Extract overview
        overview_match = re.search(r'##\s+Overview\s+(.+?)(?=##|$)', content, re.DOTALL)
        overview = overview_match.group(1).strip() if overview_match else ""

        # Extract epics
        epics = []
        epic_pattern = r'##\s+Epic[:\s]+(.+?)(?=##\s+Epic|##\s+Feature|$)'

        for match in re.finditer(epic_pattern, content, re.DOTALL | re.IGNORECASE):
            epic_content = match.group(1).strip()
            epic = PRDParser._parse_epic_section(epic_content)
            if epic:
                epics.append(epic)

        # If no epics found, try features
        if not epics:
            feature_pattern = r'##\s+Feature[:\s]+(.+?)(?=##\s+Feature|$)'
            for match in re.finditer(feature_pattern, content, re.DOTALL | re.IGNORECASE):
                feature_content = match.group(1).strip()
                epic = PRDParser._parse_epic_section(feature_content, is_feature=True)
                if epic:
                    epics.append(epic)

        prd_data = {
            'title': title,
            'overview': overview,
            'epics': epics
        }

        return PRDParser._normalize_prd(prd_data)

    @staticmethod
    def _parse_epic_section(content: str, is_feature: bool = False) -> Dict:
        """Parse epic/feature section from markdown."""
        lines = content.split('\n')
        title = lines[0].strip() if lines else "Untitled"

        # Extract description
        description_lines = []
        acceptance_criteria = []
        requirements = []

        in_acceptance = False
        in_requirements = False

        for line in lines[1:]:
            line = line.strip()

            if re.match(r'###\s+Acceptance Criteria', line, re.IGNORECASE):
                in_acceptance = True
                in_requirements = False
                continue
            elif re.match(r'###\s+Requirements', line, re.IGNORECASE):
                in_requirements = True
                in_acceptance = False
                continue
            elif line.startswith('###'):
                in_acceptance = False
                in_requirements = False
                continue

            if in_acceptance and line.startswith('-'):
                acceptance_criteria.append(line[1:].strip())
            elif in_requirements and line.startswith('-'):
                requirements.append(line[1:].strip())
            elif not in_acceptance and not in_requirements and line:
                description_lines.append(line)

        epic_id = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

        return {
            'id': epic_id,
            'title': title,
            'description': '\n'.join(description_lines).strip(),
            'acceptance_criteria': acceptance_criteria,
            'requirements': [{'id': f"{epic_id}-{i}", 'description': req}
                           for i, req in enumerate(requirements, 1)],
            'status': 'pending',
            'type': 'feature' if is_feature else 'epic'
        }

    @staticmethod
    def _normalize_prd(prd_data: Dict) -> Dict:
        """Normalize PRD structure."""
        # Ensure required fields
        prd = {
            'title': prd_data.get('title', 'Untitled PRD'),
            'overview': prd_data.get('overview', prd_data.get('description', '')),
            'epics': []
        }

        # Process epics
        for i, epic in enumerate(prd_data.get('epics', []), 1):
            normalized_epic = {
                'id': epic.get('id', f"epic-{i}"),
                'title': epic.get('title', f"Epic {i}"),
                'description': epic.get('description', ''),
                'acceptance_criteria': epic.get('acceptance_criteria', []),
                'requirements': epic.get('requirements', []),
                'status': 'pending',
                'priority': epic.get('priority', i)
            }

            # Ensure requirements have IDs
            for j, req in enumerate(normalized_epic['requirements'], 1):
                if isinstance(req, str):
                    normalized_epic['requirements'][j] = {
                        'id': f"{normalized_epic['id']}-req-{j}",
                        'description': req
                    }
                elif 'id' not in req:
                    req['id'] = f"{normalized_epic['id']}-req-{j}"

            prd['epics'].append(normalized_epic)

        return prd

    @staticmethod
    def validate_prd(prd: Dict) -> List[str]:
        """
        Validate PRD structure.

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        if not prd.get('title'):
            errors.append("PRD missing title")

        if not prd.get('epics'):
            errors.append("PRD has no epics defined")

        for i, epic in enumerate(prd.get('epics', []), 1):
            if not epic.get('title'):
                errors.append(f"Epic {i} missing title")
            if not epic.get('acceptance_criteria'):
                errors.append(f"Epic {i} ({epic.get('title', 'untitled')}) has no acceptance criteria")

        return errors
