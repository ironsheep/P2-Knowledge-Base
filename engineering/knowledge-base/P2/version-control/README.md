# P2 Knowledge Base Version Control System

## Overview
Comprehensive version tracking, change detection, and rollback system for the P2 Knowledge Base repository. This system ensures data integrity, tracks all changes, and provides recovery mechanisms for problematic updates.

## System Components

### 1. Git Hooks (`.git-hooks/`)
Automated validation and tracking on every commit.

#### Pre-Commit Hook (`pre-commit`)
Runs before each commit to:
- Validate YAML schemas
- Check cross-references
- Validate instruction encodings (32-bit)
- Update version tracking
- Check completeness scores
- Generate commit metadata

#### Post-Commit Hook (`post-commit`)
Runs after successful commits to:
- Finalize version tracking with commit hash
- Generate change reports
- Update affected entry audits
- Check for source document updates
- Update repository statistics
- Tag significant commits

### 2. Change Detection (`change-detector.py`)
Identifies changes in source documents and repository entries.

**Features:**
- SHA-256 hash-based change detection
- Source document monitoring
- Entry change tracking
- Dependency identification
- Extraction trigger generation

**Usage:**
```bash
# Run once
python3 version-control/change-detector.py

# Watch continuously
python3 version-control/change-detector.py --watch
```

### 3. Update Propagation (`update-propagator.py`)
Propagates changes from source documents to repository entries.

**Features:**
- Layer-based merging strategy
- Conflict detection and resolution
- Automatic backup creation
- Completeness score recalculation
- Detailed propagation reports

**Usage:**
```bash
# Process all pending triggers
python3 version-control/update-propagator.py

# Dry run without changes
python3 version-control/update-propagator.py --dry-run
```

### 4. Version Comparison (`version-comparator.py`)
Compares repository versions and generates migration guides.

**Features:**
- Commit-to-commit comparison
- Tag-based comparison
- Entry-level diff analysis
- Statistical comparison
- Migration guide generation
- Breaking change detection

**Usage:**
```bash
# Compare two commits
python3 version-control/version-comparator.py \
  --from-version abc123 --to-version def456

# Compare tag to current
python3 version-control/version-comparator.py \
  --from-tag v1.0.0 --output migration-guide.md
```

### 5. Rollback Manager (`rollback-manager.py`)
Manages rollback operations and recovery from backups.

**Features:**
- Entry-level rollback
- Commit-level rollback
- Time-based rollback
- Named restore points
- Safety backups
- Old backup cleanup

**Usage:**
```bash
# Rollback single entry
python3 version-control/rollback-manager.py \
  --rollback-entry instructions/pasm2/add-instruction.yaml

# Rollback entire commit
python3 version-control/rollback-manager.py \
  --rollback-commit abc123 --reason "Bad extraction"

# Rollback last 2 hours
python3 version-control/rollback-manager.py \
  --rollback-hours 2 --reason "Extraction errors"

# Create restore point
python3 version-control/rollback-manager.py \
  --create-restore-point "before-major-update"

# Restore from point
python3 version-control/rollback-manager.py \
  --restore-from "before-major-update"

# Clean old backups
python3 version-control/rollback-manager.py \
  --cleanup-days 30
```

## Version Tracking Workflow

### 1. Normal Development Flow
```
Edit Files → Pre-Commit Validation → Commit → Post-Commit Processing
     ↓              ↓                    ↓            ↓
  Changes      Schema Check         Git History   Reports
                                                   Statistics
```

### 2. Source Update Flow
```
Source Change → Change Detection → Extraction Trigger → Propagation
      ↓              ↓                    ↓                ↓
  .csv/.md      Hash Compare         Trigger File     Update Entries
```

### 3. Rollback Flow
```
Problem Detected → Identify Scope → Select Backup → Rollback
        ↓               ↓               ↓             ↓
    Validation      Entry/Commit    Most Recent    Restore
```

## Directory Structure

```
version-control/
├── change-detector.py       # Change detection system
├── update-propagator.py     # Update propagation
├── version-comparator.py    # Version comparison
├── rollback-manager.py      # Rollback management
└── README.md               # This file

.git-hooks/
├── pre-commit              # Pre-commit validation
└── post-commit             # Post-commit processing

update-tracking/
├── source-hashes.json      # Source file hashes
├── entry-hashes.json       # Entry file hashes
├── version-log.yaml        # Version history
├── repository-stats.json   # Repository statistics
├── extraction-triggers/    # Pending extractions
├── reports/               # Change and propagation reports
├── backups/               # Entry backups
├── conflicts/             # Conflict resolution
└── rollback-log.yaml      # Rollback history
```

## Setup Instructions

### 1. Install Git Hooks
```bash
cd /path/to/P2-Knowledge-Base
ln -s engineering/knowledge-base/P2/.git-hooks/pre-commit .git/hooks/
ln -s engineering/knowledge-base/P2/.git-hooks/post-commit .git/hooks/
chmod +x .git/hooks/pre-commit .git/hooks/post-commit
```

### 2. Initialize Tracking
```bash
# Create initial hashes
python3 version-control/change-detector.py

# Create first restore point
python3 version-control/rollback-manager.py \
  --create-restore-point "initial-setup"
```

### 3. Configure Automation (Optional)
Add to crontab for hourly change detection:
```cron
0 * * * * cd /path/to/repo && python3 version-control/change-detector.py
```

## Configuration

### Layer Priority (in `update-propagator.py`)
```python
layer_priority = {
    'P2-Instruction-Set.csv': 1,  # Base definitions
    'P2-Datasheet': 2,            # Official specs
    'Silicon-Doc': 3,             # Rich narratives
    'Forum': 4                    # Clarifications
}
```

### Backup Retention (in `rollback-manager.py`)
Default: 30 days
Modify with: `--cleanup-days N`

### Conflict Resolution Strategy
1. **Automatic**: Higher priority sources override
2. **Manual**: Conflicts saved to `update-tracking/conflicts/`
3. **Review**: Check conflict files before resolution

## Monitoring and Reports

### Status Commands
```bash
# Check current version
git rev-parse HEAD

# View recent changes
cat update-tracking/reports/changes-*.md | head -50

# Check pending triggers
ls update-tracking/extraction-triggers/

# View repository statistics
cat update-tracking/repository-stats.json
```

### Health Checks
```bash
# Validate repository
python3 validators/repository-validator.py

# Check for conflicts
ls update-tracking/conflicts/

# List available backups
python3 version-control/rollback-manager.py
```

## Best Practices

### 1. Regular Backups
- Restore points before major updates
- Automatic backups on every change
- Cleanup old backups monthly

### 2. Change Detection
- Run after source document updates
- Process triggers promptly
- Review conflicts before resolution

### 3. Version Tagging
```bash
# Tag stable versions
git tag -a v1.0.0 -m "First stable release"

# Tag before major changes
git tag -a pre-extraction-2025-01-06
```

### 4. Rollback Strategy
1. Try entry-level rollback first
2. Use commit rollback for systematic issues
3. Create restore points before risky operations
4. Keep safety backups for 30+ days

## Troubleshooting

### Common Issues

#### "No backups found"
- Check backup directory exists
- Verify backup creation in propagation
- Look for safety backups in rollback-safety/

#### "Extraction trigger not processed"
- Check trigger file format
- Verify affected_entries paths
- Look for errors in propagation report

#### "Conflicts detected"
- Review conflict files in conflicts/
- Check source priority settings
- Manually resolve in YAML files

#### "Rollback failed"
- Check file permissions
- Verify backup file integrity
- Try git-based rollback

## Migration Guide for Updates

When updating the version control system:

1. **Create restore point**
   ```bash
   python3 rollback-manager.py --create-restore-point "pre-update"
   ```

2. **Update scripts**
   ```bash
   git pull origin main
   ```

3. **Test on subset**
   ```bash
   python3 change-detector.py --test
   ```

4. **Run full update**
   ```bash
   python3 update-propagator.py
   ```

5. **Verify results**
   ```bash
   python3 validators/repository-validator.py
   ```

## API Integration

### For Document Generation
```python
# Check for updates before generation
from version_control.change_detector import ChangeDetector

detector = ChangeDetector(repo_path)
changes = detector.detect_entry_changes()

if changes:
    print(f"Warning: {len(changes)} entries changed since last generation")
```

### For Extraction Pipeline
```python
# Create extraction trigger
trigger_data = {
    'trigger_time': datetime.now().isoformat(),
    'source_file': 'sources/P2-Instruction-Set.csv',
    'change_type': 'modified',
    'affected_entries': ['instructions/pasm2/*.yaml']
}
```

## Future Enhancements

### Planned Features
- Real-time change monitoring
- Automated conflict resolution
- Distributed backup storage
- Web-based version browser
- Integration with CI/CD

### Proposed Improvements
- Parallel propagation processing
- Smart backup compression
- Incremental hash computation
- Machine learning for conflict resolution
- Automated rollback triggers