# Backup Strategy

## Overview
Backup files are created before any significant file modification to protect against data loss. These backups are stored in local `backups/` directories and excluded from version control.

## Directory Structure
```
any-directory/
├── important-file.md          # Working file
└── backups/                   # Backup directory (not in git)
    ├── important-file.md.backup.20250821_193319
    └── important-file.md.backup.20250821_194500
```

## Backup Naming Convention
`[filename].backup.[YYYYMMDD_HHMMSS]`
- Timestamp ensures uniqueness
- Easy to identify source file
- Sortable by date/time

## Creating Backups
Before modifying any file > 100 lines or critically important:
```bash
cp filename.md filename.md.backup.$(date +%Y%m%d_%H%M%S)
# Then move to backups/ directory
mv filename.md.backup.* backups/
```

Or directly to backup directory:
```bash
cp filename.md backups/filename.md.backup.$(date +%Y%m%d_%H%M%S)
```

## Exclusion from Version Control
The `.gitignore` file contains:
```
# Backup directories
**/backups/
backups/
```

This ensures:
- Backup directories are never committed
- Repository stays clean
- Personal backup preferences don't affect others

## Backup Locations
Common backup directories exist in:
- `/tools/backups/` - Tool script backups
- `/pipelines/backups/` - Pipeline documentation backups
- `/exports/pdf-generation/workspace/*/backups/` - PDF generation backups
- `/documentation/*/backups/` - Documentation backups

## Recovery
To recover from a backup:
```bash
# List available backups
ls -la backups/

# Compare with current
diff backups/file.md.backup.20250821_193319 file.md

# Restore if needed
cp backups/file.md.backup.20250821_193319 file.md
```

## Cleanup
Periodically clean old backups:
```bash
# Remove backups older than 7 days
find . -path "*/backups/*.backup.*" -mtime +7 -delete
```

## Benefits
- Protection against accidental data loss
- Quick recovery from mistakes
- No repository bloat
- Personal safety net during complex edits