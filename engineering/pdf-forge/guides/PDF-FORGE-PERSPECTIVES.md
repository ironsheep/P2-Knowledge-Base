# PDF Forge - Multiple Perspectives Reference

*Critical for understanding where files are and why paths differ*

## The Four Perspectives of PDF Forge

### 1. Host-Native View (Your Mac)
**Location**: `/Users/stephen/Projects/.../P2-Knowledge-Base/`
```
P2-Knowledge-Base/
├── pdf-forge-scripts/           # Source of truth for scripts
├── pdf-forge-workspace/         # LOCAL MIRROR of forge testing area
│   ├── test-requests/          # You can create test requests here
│   ├── test-results/           # You can audit .tex files here
│   └── test-documents/         # Test markdown files
└── exports/pdf-generation/
    └── outbound/               # Staging for forge deployment
        └── [document-name]/    # Files to copy to forge
```

### 2. Container Main View (PDF Forge Root)
**Location**: `/workspaces/my-doc-forge/` or `/workspace/`
```
/workspace/                      # PRODUCTION AREA
├── inbox/                      # Drop request.json + *.md + assets/
├── scripts/                    # Production scripts (generate-pdf.js)
├── templates/                  # Production .latex and .sty files
├── filters/                    # Production .lua filters
├── outbox/                     # Generated PDFs appear here
└── shared/                     # TESTING AREA (see below)
```

### 3. Container Testing View (Shared Workspace)
**Location**: `/workspace/shared/`
```
/workspace/shared/               # AUTOMATED TESTING AREA
├── test-requests/              # Watch script monitors *.json here
│   └── processed/              # Archived after processing
├── test-documents/             # Test markdown files
├── templates/                  # TEST templates (isolated)
├── filters/                    # TEST filters (isolated)  
├── output-pdfs/                # Test PDF output
├── test-results/               # Result JSONs and .tex files
└── status/                     # Logs and status files
```

### 4. Temp Working View (During Execution)
**Location**: `/tmp/pandoc-work-*`
```
/tmp/pandoc-work-[name]-[timestamp]/
├── template.latex              # Copied from templates/
├── *.sty                       # ALL .sty files copied here
└── [working files]             # Pandoc runs FROM here
```

## Critical Path Mappings

### Manual PDF Generation (generate-pdf.js)
```
Host: exports/outbound/[doc]/request.json
  ↓ (you copy)
Forge: /workspace/inbox/request.json
  ↓ (script reads)
Process: /workspace/inbox/*.md → /workspace/outbox/*.pdf
```

### Automated Testing (watch-shared-workspace.js)
```
Host: pdf-forge-workspace/test-requests/*.json
  ↓ (you copy)
Forge: /workspace/shared/test-requests/*.json
  ↓ (watch script detects)
Process: /workspace/shared/test-documents/*.md
  ↓ (creates temp dir)
Temp: /tmp/pandoc-work-*/ (copies all dependencies)
  ↓ (generates)
Output: /workspace/shared/output-pdfs/*.pdf
        /workspace/shared/test-results/*.tex (audit files)
```

### Local Auditing Access
```
Forge: /workspace/shared/test-results/*.tex
  ↓ (mirrored to)
Host: pdf-forge-workspace/test-results/*.tex
  ↓ (Claude can read)
Audit: Check if lua filters applied, debug LaTeX issues
```

## Key Insights

### Why These Perspectives Matter

1. **Scripts look in different places**
   - generate-pdf.js: Uses `/workspace/inbox/`, `/workspace/templates/`
   - watch-shared-workspace.js: Uses `/workspace/shared/*`

2. **Your local workspace is a MIRROR**
   - `pdf-forge-workspace/` = `/workspace/shared/` (testing only)
   - NOT the main forge production area

3. **Production vs Testing Isolation**
   - Main forge (`/workspace/`) = Production, manual control
   - Shared area (`/workspace/shared/`) = Testing, automated
   - Never automatically cross this boundary (safety)

4. **Temp directories solve dependencies**
   - Watch script copies ALL .sty files to `/tmp/`
   - This is why layered templates work in testing
   - Each test gets clean, isolated environment

## Common Confusions Resolved

**Q: Why can't the script find my document?**
A: Check which script and which directory:
- generate-pdf.js looks in `/workspace/inbox/`
- watch script looks in `/workspace/shared/test-documents/`

**Q: Why do I have two templates directories?**
A: Isolation between testing and production:
- `/workspace/templates/` = Production (what users get)
- `/workspace/shared/templates/` = Testing (safe to break)

**Q: Where do .tex audit files go?**
A: `/workspace/shared/test-results/` which mirrors to your local `pdf-forge-workspace/test-results/`

**Q: Why does watch script work but generate-pdf fail (or vice versa)?**
A: They use completely different directory structures. Check paths!

## Quick Reference Commands

```bash
# From host (Mac) to see your local test mirror
ls pdf-forge-workspace/test-results/*.tex

# From forge container - check production
ls /workspace/inbox/
ls /workspace/templates/

# From forge container - check testing  
ls /workspace/shared/test-requests/
ls /workspace/shared/test-results/

# See where scripts are running
ps aux | grep node
```

---

*This document is essential for understanding PDF Forge architecture. Without these perspectives, you'll be lost in path confusion.*