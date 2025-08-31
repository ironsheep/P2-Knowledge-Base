# LaTeX Template Backup Policy

## 🔴 CRITICAL: Always Keep Last Known-Good Template

### Backup Rules

1. **Before ANY template modification**:
   ```bash
   cp template.latex backups/template.latex.$(date +%Y%m%d_%H%M%S).working
   ```

2. **After SUCCESSFUL PDF generation**:
   ```bash
   cp template.latex backups/template.latex.$(date +%Y%m%d_%H%M%S).verified
   ```

3. **Backup Directory Structure**:
   ```
   /documentation/pdf-templates-master/
   ├── [template-name].latex           # Current working version
   ├── backups/
   │   ├── [template].latex.YYYYMMDD_HHMMSS.working   # Pre-modification backup
   │   └── [template].latex.YYYYMMDD_HHMMSS.verified  # Known-good after PDF success
   ```

### Backup Suffixes
- `.working` - Backed up before changes, may or may not work
- `.verified` - Successfully generated a PDF, known-good state

### Recovery Process
1. List backups: `ls -la backups/*.verified | tail -5`
2. Find most recent verified: `ls -la backups/*.verified | tail -1`
3. Restore: `cp backups/[chosen-backup] [template-name].latex`

### Retention
- Keep last 5 `.verified` versions
- Keep last 10 `.working` versions
- Clean older ones periodically

### Current Status
- Latest verified backup: Check `ls -la backups/*.verified | tail -1`
- Latest working backup: Created when you read this file

## Why This Matters
- Template syntax errors can waste hours
- Splicing/merging can introduce systematic issues
- Always need quick fallback to known-good state
- Peace of mind when experimenting with fixes