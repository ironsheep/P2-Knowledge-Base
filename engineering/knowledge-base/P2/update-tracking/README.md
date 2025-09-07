# Update Tracking

## Overview
Maintains version history, change logs, and update metadata for all repository entries.

## Tracking Files

### Change Logs
- `changelog-YYYY-MM.yaml` - Monthly change summaries
- `updates-pending.yaml` - Queued updates to process
- `updates-completed.yaml` - Processed update history

### Source Updates
- `source-versions.yaml` - Tracks source document versions
- `extraction-runs.yaml` - History of extraction processes
- `conflict-resolutions.yaml` - Decisions on conflicting data

### Version Control
- Git commits provide atomic change tracking
- Each update includes:
  - Timestamp
  - Source document(s) affected
  - Entries modified
  - Completeness score changes
  - Rationale for changes

## Update Schema
```yaml
update_id: "2025-01-06-001"
timestamp: "2025-01-06T10:30:00Z"
source_trigger: "Silicon Doc v35 Part 3 update"
entries_affected:
  - "instructions/pasm2/wrpin-instruction.yaml"
  - "components/smart-pins/mode-07-pwm.yaml"
changes:
  - entry: "wrpin-instruction"
    field: "description"
    old_score: 5
    new_score: 7
    reason: "Added detailed narrative from Silicon Doc"
processed_by: "extraction-pipeline-v1.0"
verification_status: "verified"
```

## Update Workflow
1. Detect source document changes
2. Run targeted extraction
3. Compare with existing entries
4. Apply conflict resolution rules
5. Update affected YAML files
6. Regenerate quality audits
7. Commit with detailed message
8. Update tracking logs