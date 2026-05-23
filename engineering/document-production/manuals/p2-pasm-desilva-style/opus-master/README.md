# Opus Master Document - Source of Truth

## This Directory Contains the Authoritative Master

**File**: `COMPLETE-OPUS-MASTER.md`
**Originally Generated**: August 20, 2025
**Model**: Claude Opus 4.1
**Protection**: Git version control (full history preserved)

## What This Is

This is the complete 16-chapter De Silva style P2 Assembly manual. It includes:
- Full front matter (dedication, acknowledgments, preface)
- All 16 chapters of content
- Appendices
- Index

## Why This Is Important

1. **Opus Time is Expensive** - Original generation represented significant Opus 4.1 time
2. **Source of Truth** - All workspace copies are derived from this file
3. **Git Protected** - Version history provides safety for careful edits
4. **Nearly Lost Once** - Found in archive-old folder on Aug 22, 2025

## How to Use

1. **Edit this file carefully** - It is the source of truth
2. **Git provides safety** - You can always revert if needed
3. **Copy to workspace** - For PDF production workflow
4. **Escape and deploy** - Workspace copy gets escaped to outbound

## Workflow

```bash
# 1. Edit COMPLETE-OPUS-MASTER.md as needed

# 2. Copy to workspace
cp COMPLETE-OPUS-MASTER.md \
   ../../../workspace/p2-pasm-desilva-style/P2-PASM-deSilva-Style.md

# 3. Escape and stage (from workspace directory)
cd ../../../workspace/p2-pasm-desilva-style
../../../tools/conversion/latex-escape-all.sh \
    P2-PASM-deSilva-Style.md \
    ../../outbound/p2-pasm-desilva-style/P2-PASM-deSilva-Style.md
```

## Historical Note

Originally this file was marked READ-ONLY (chmod 444) for protection. That approach has been superseded by git version control, which provides better protection through full history and easy rollback.

The August 2025 near-loss taught us to always commit masters to git immediately after generation.

---

*Originally recovered on 2025-08-22 by Claude & Stephen*
*Workflow updated 2025-12-10*