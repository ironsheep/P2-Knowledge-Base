# CRITICAL: Non-Destructive Work Protocols

**Created**: 2025-08-21  
**Reason**: Major data loss incident - 3300+ lines of PDF generation guide lost  
**Severity**: CRITICAL - Cannot happen again

## MANDATORY Rules - NO EXCEPTIONS

### 1. ALWAYS Create Backups Before Modifications
```bash
# BEFORE any destructive operation:
cp original.md original.md.backup.$(date +%Y%m%d_%H%M%S)

# OR use git for tracked files:
git add file.md && git commit -m "Backup before modification"
```

### 2. NEVER Use Destructive Operations on Large Files
**FORBIDDEN**:
- `mv temp-file.md important-file.md` (overwrites without backup)
- `> file.md` (truncates file)
- Direct replacement of files over 100 lines

**REQUIRED**:
- Always use `cp` to create backups first
- Use `git diff` to verify changes before applying
- Use incremental edits with Edit tool, not wholesale replacement

### 3. File Size Awareness Protocol
**Before modifying ANY file**:
```bash
wc -l filename.md  # Check line count
ls -lh filename.md # Check file size
```

**If file > 1000 lines OR > 50KB**:
1. MANDATORY backup creation
2. Incremental editing only (Edit/MultiEdit tools)
3. NEVER wholesale replacement

### 4. Recovery-First Mindset
**ALWAYS ask**: "If this operation fails, can I recover the original?"
- If answer is NO → Create backup first
- If answer is MAYBE → Create backup first  
- If answer is YES → Proceed with caution

### 5. Corruption Handling Protocol
**When encountering file corruption**:
1. ✅ Identify exact corrupted lines/sections
2. ✅ Create backup of entire file first
3. ✅ Use surgical editing (Edit tool) to fix specific issues
4. ❌ NEVER truncate or replace entire file

## This Incident: What Went Wrong

**File**: `/documentation/pipelines/pdf-generation-format-guide.md`
**Size Lost**: 3300+ lines of critical documentation
**Cause**: Destructive replacement instead of surgical editing
**Impact**: Major knowledge base loss

**What I Should Have Done**:
1. `cp pdf-generation-format-guide.md pdf-generation-format-guide.md.backup.20250821`
2. Use Edit tool to fix only lines 360-365 (corrupted section)
3. Append new LaTeX escaping section at end
4. Preserve all existing content

**What I Actually Did**:
1. ❌ Used `head -n 359` to truncate file
2. ❌ Lost 3300+ lines of valuable content
3. ❌ No backup created
4. ❌ Replaced instead of repaired

## Prevention Checklist

Before ANY file modification:
- [ ] File size checked (`wc -l`, `ls -lh`)
- [ ] Backup created if size > threshold
- [ ] Understanding of what could be lost
- [ ] Recovery plan in place
- [ ] Using incremental tools (Edit/MultiEdit) not replacement

## Emergency Recovery Protocol

When data loss occurs:
1. Immediately stop all operations
2. Check for any available backups (git, system, conversation history)
3. Attempt reconstruction from available sources
4. Document what was lost
5. Implement stronger safeguards

**This protocol is now MANDATORY for all file operations.**