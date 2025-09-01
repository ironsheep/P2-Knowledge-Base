# PDF Forge Workflow Architecture Thoughts

*Notes from discussion on 2025-08-27 about testing vs production workflows*

## The Three Directory Contexts

### 1. Main Forge Production (`/workspace/`)
```
/workspace/
├── inbox/       # Manual PDF generation (drag & drop)
├── scripts/     # Production scripts
├── templates/   # Production templates  
├── filters/     # Production filters
└── outbox/      # Generated PDFs
```

### 2. Shared Testing Area (`/workspace/shared/`)
```
/workspace/shared/
├── test-requests/   # Watch script monitors here
├── test-documents/  # Test markdown files
├── templates/       # Test templates (isolated)
├── filters/         # Test filters (isolated)
├── output-pdfs/     # Test output
└── status/          # Logs and status
```

### 3. Temp Working (`/tmp/pandoc-work-*`)
- Watch script creates isolated temp directories
- Copies ALL .sty files to ensure dependencies work
- Runs pandoc from clean environment

## The Core Tension: Testing vs Production

### The Dream (What You Expected)
- Test in shared/ → Success → Auto-promotes to production templates/
- Testing uses production locations directly
- What passes testing is immediately available
- No manual file copying needed

### The Reality (Current Implementation)
- Testing isolated in `/workspace/shared/`
- Production protected in `/workspace/` 
- Manual promotion required
- Safety but with friction

## The Workflow Dilemma

### Arguments FOR Auto-Promotion
✅ Removes human toil (no dragging files)
✅ What passed is exactly what deploys
✅ Faster iteration cycles
✅ That emotional satisfaction of efficiency

### Arguments AGAINST Auto-Promotion
❌ No cooling-off period
❌ Test success ≠ ready for all documents
❌ Half-finished work could break other documents
❌ Shared .sty files affect multiple document stacks

### The Process Guy Paradox
- You ARE the quality gate (50 years experience)
- But you're doing mechanical work (copying files)
- The "lossy transfer" problem: test 5 files, copy 4
- Not about being replaced, about being a faulty cable

## The Manifest Complexity

### Why Simple Manifests Don't Work
- Sonnet might test with stripped-down .sty files
- Partial templates that work for test but not production
- "What passed testing" ≠ "What should go to production"
- Size checks unreliable (could be slightly smaller after cleanup)

### The Fidelity Loss Problem
- Claude tests successfully
- Human copies files
- Things get missed or wrong versions copied
- Failure not from bad code but bad transfer

## Potential Solutions (For Shower Thinking)

### Middle Ground: Promotion Command
```bash
make test           # Run in shared/
make review         # See what passed
make promote        # Atomic copy to production
```

### Test Result Manifest
- List EXACTLY what files passed
- Include checksums/versions
- One command promotes entire set
- Human reviews manifest, not individual files

### Workflow Inversion
Instead of: Human pushes → System responds
Consider: System acts → Human reviews

## Current Decision

For now:
1. Keep watch script isolated in `/workspace/shared/`
2. Keep production protected
3. Both scripts support lua_filters array
4. Focus on making current workflow reliable
5. Let the elegant solution emerge through usage

## Script Enhancements Completed

### Both Scripts Now Support
```json
{
  "lua_filters": ["smart-pins-block-coloring"],
  "pandoc_args": ["--top-level-division=part"]
}
```

### Key Enhancement
- `lua_filters` array for clean filter specification
- Automatic path resolution (name → filters/name.lua)
- Filters applied BEFORE pandoc_args (correct order)

## The Feeling That Pulls

There's a solution here where:
- Automation handles the mechanical
- Human provides the judgment
- No lossy transfer between test and production
- Efficient without being reckless

The shape is there, just not quite visible yet.

---

*This document captures the workflow tensions and thoughts for future consideration. The immediate task is to make both workflows (manual and automated) reliable with the current separation.*