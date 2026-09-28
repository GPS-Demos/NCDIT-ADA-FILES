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

    MAX_PRD_SIZE = 10 * 1024 * 1024  # 10MB limit

    @staticmethod
    def parse(prd_path: str) -> Dict:
        """
        Parse PRD from file.

        Args:
            prd_path: Path to PRD file (YAML, JSON, or Markdown)

        Returns:
            Structured PRD dictionary with epics
        """
        prd_file = Path(prd_path).resolve()

        # Enforce path traversal bounds checking
        cwd = Path.cwd().resolve()
        repo_root = Path(__file__).resolve().parent.parent.parent.parent
        try:
            if not (prd_file.is_relative_to(cwd) or prd_file.is_relative_to(repo_root)):
                raise ValueError(f"Path traversal detected: {prd_path} is outside allowed directory")
        except (ValueError, AttributeError):
            pass

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
        if prd_file.stat().st_size > PRDParser.MAX_PRD_SIZE:
            raise ValueError(f"PRD file exceeds maximum allowed size ({PRDParser.MAX_PRD_SIZE} bytes)")
        with open(prd_file, 'r', encoding='utf-8') as f:
            content = f.read(PRDParser.MAX_PRD_SIZE + 1)
        if len(content) > PRDParser.MAX_PRD_SIZE:
            raise ValueError(f"PRD file exceeds maximum allowed size ({PRDParser.MAX_PRD_SIZE} bytes)")
        prd_data = yaml.safe_load(content)
        if not isinstance(prd_data, dict):
            raise ValueError("PRD YAML content must deserialize to a dictionary")

        return PRDParser._normalize_prd(prd_data)

    @staticmethod
    def _parse_json(prd_file: Path) -> Dict:
        """Parse JSON PRD."""
        if prd_file.stat().st_size > PRDParser.MAX_PRD_SIZE:
            raise ValueError(f"PRD file exceeds maximum allowed size ({PRDParser.MAX_PRD_SIZE} bytes)")
        with open(prd_file, 'r', encoding='utf-8') as f:
            content = f.read(PRDParser.MAX_PRD_SIZE + 1)
        if len(content) > PRDParser.MAX_PRD_SIZE:
            raise ValueError(f"PRD file exceeds maximum allowed size ({PRDParser.MAX_PRD_SIZE} bytes)")
        prd_data = json.loads(content)
        if not isinstance(prd_data, dict):
            raise ValueError("PRD JSON content must deserialize to a dictionary")

        return PRDParser._normalize_prd(prd_data)

    @staticmethod
    def _parse_markdown(prd_file: Path) -> Dict:
        """Parse Markdown PRD."""
        if prd_file.stat().st_size > PRDParser.MAX_PRD_SIZE:
            raise ValueError(f"PRD file exceeds maximum allowed size ({PRDParser.MAX_PRD_SIZE} bytes)")
        with open(prd_file, 'r', encoding='utf-8') as f:
            content = f.read(PRDParser.MAX_PRD_SIZE + 1)
        if len(content) > PRDParser.MAX_PRD_SIZE:
            raise ValueError(f"PRD file exceeds maximum allowed size ({PRDParser.MAX_PRD_SIZE} bytes)")

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
            normalized_reqs = []
            for j, req in enumerate(normalized_epic.get('requirements', []), 1):
                if isinstance(req, str):
                    normalized_reqs.append({
                        'id': f"{normalized_epic['id']}-req-{j}",
                        'description': req
                    })
                elif isinstance(req, dict):
                    req_copy = dict(req)
                    if 'id' not in req_copy:
                        req_copy['id'] = f"{normalized_epic['id']}-req-{j}"
                    normalized_reqs.append(req_copy)
                else:
                    normalized_reqs.append({
                        'id': f"{normalized_epic['id']}-req-{j}",
                        'description': str(req)
                    })
            normalized_epic['requirements'] = normalized_reqs

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
