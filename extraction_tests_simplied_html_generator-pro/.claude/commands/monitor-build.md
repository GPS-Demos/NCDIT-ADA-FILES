# Monitor Autonomous Build

This command provides monitoring and status checking for the autonomous build process.

## MONITORING FUNCTIONS

### 1. Check Current Status

```bash
# Read orchestration state
cat .bmad-core/autonomous/state.json

# Check current epic progress
ls -la .bmad-core/autonomous/epic-*/

# View orchestration log
tail -f .bmad-core/autonomous/orchestration.log
```

### 2. View Epic Reports

Display completion status for each epic:

```javascript
function getEpicStatus() {
  const epics = [
    "Foundation & Authentication",
    "Article Management & Basic Editor",
    "Data Components & Text-Data Association",
    "Data Viewer & Compute Provisioning",
    "Collaboration & Team Management",
    "Comments & Version Control",
    "Data Lineage & Provenance",
    "AI Assistant & Export"
  ];

  epics.forEach((epic, index) => {
    const num = index + 1;
    const reportPath = `.bmad-core/autonomous/epic-${num}/report.md`;
    const status = fileExists(reportPath) ? "✅ COMPLETE" : "⏳ PENDING";
    console.log(`Epic ${num}: ${epic} - ${status}`);
  });
}
```

### 3. List Created Files

```bash
# Find all files created by the autonomous build
find src/features -type f -newer .bmad-core/autonomous/state.json | sort

# Count files per epic
for i in {1..8}; do
  echo "Epic $i files:"
  find src/features -name "*epic-$i*" -o -name "*Epic$i*" | wc -l
done
```

### 4. Validate Integration Points

```javascript
function validateIntegration() {
  const checks = {
    "Epic 1": ["Auth service exists", "Portal routing works"],
    "Epic 2": ["Article CRUD operational", "Editor component renders"],
    "Epic 3": ["Data components created", "Upload workflow functional"],
    "Epic 4": ["Data viewer displays", "Compute provisioning available"],
    "Epic 5": ["Team management active", "Roles assigned"],
    "Epic 6": ["Comments system works", "Versions tracked"],
    "Epic 7": ["Lineage visible", "Provenance tracked"],
    "Epic 8": ["AI assistant responds", "Export generates"]
  };

  Object.entries(checks).forEach(([epic, requirements]) => {
    console.log(`\n${epic} Integration:`);
    requirements.forEach(req => {
      console.log(`  - ${req}: [CHECK]`);
    });
  });
}
```

### 5. Generate Progress Report

```markdown
# Autonomous Build Progress Report

## Overall Status
- Start Time: [timestamp]
- Current Epic: [number]
- Completed Epics: [list]
- Failed Epics: [list]
- Estimated Completion: [time]

## Epic Details
[For each epic, show:]
- Status: [Pending/In Progress/Complete/Failed]
- Files Created: [count]
- Stories Implemented: [count/total]
- Integration Points: [list]
- Key Decisions Made: [list]

## File System Impact
- Total Files Created: [number]
- Total Lines of Code: [number]
- Components Created: [number]
- Services Implemented: [number]

## Next Steps
- Current Task: [description]
- Upcoming Epic: [number and name]
- Blockers: [if any]
```

### 6. Recovery Options

If the build stalls or fails:

```bash
# Resume from last epic
/autonomous-build --resume-from-epic [number]

# Retry failed epic
/autonomous-build --retry-epic [number]

# Skip problematic epic
/autonomous-build --skip-epic [number]

# Force continue
/autonomous-build --force-continue
```

## USAGE

Run this monitoring command in parallel with the autonomous build to track progress:

```bash
# Start monitoring
/monitor-build

# Check specific epic
/monitor-build --epic 3

# Generate full report
/monitor-build --report

# Watch live progress
/monitor-build --watch
```

## ALERTS

The monitor will alert you when:
- An epic completes successfully ✅
- An epic fails ❌
- The build stalls for >10 minutes ⚠️
- All epics complete 🎉
- Critical errors occur 🚨

## DO NOT INTERFERE

Remember: The autonomous build is designed to run without intervention. Use this monitor only to observe progress, not to interfere with execution.