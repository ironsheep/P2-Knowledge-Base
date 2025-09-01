# 🔴 CRITICAL: SOURCE OF TRUTH LOCATIONS

**LESSON LEARNED**: We lost work because we edited in the wrong locations. ALWAYS work from these source of truth locations!

## Smart Pins Document Source of Truth

### 1. MARKDOWN SOURCE OF TRUTH
**ALWAYS EDIT HERE FIRST**: 
```
/exports/pdf-generation/workspace/smart-pins-manual/P2-Smart-Pins-Complete-Reference-WORKING.md
```
- This has all language markers: `{.configuration}`, `{.antipattern}`, `spin2`, `pasm2`
- ALL content changes happen here
- NEVER edit the escaped version directly

### 2. TEMPLATE/STYLE SOURCE OF TRUTH
**ALWAYS EDIT HERE FIRST**:
```
/exports/pdf-generation/workspace/manual-templates/
```
Files:
- `p2kb-foundation.sty` - Foundation layer (Pandoc fixes)
- `p2kb-smart-pins-content.sty` - Smart Pins content layer (color environments)
- `p2kb-smart-pins.latex` - Main template
- `p2kb-tech-review.sty` - Technical review presentation
- `smart-pins-colored-blocks.lua` - Lua filter for colored code blocks

### 3. DEPLOYMENT WORKFLOW
```
workspace/smart-pins-manual/         [SOURCE - Edit markdown here]
           ↓ (latex-escape-all.sh)
outbound/P2-Smart-Pins-Reference/    [STAGING - Never edit here]
           ↓ (User deploys)
PDF Forge                            [PRODUCTION - Never edit here]
```

## 🚫 NEVER EDIT IN THESE LOCATIONS
- ❌ `/engineering/pdf-forge/production/` - Deployment staging only
- ❌ `/pdf-forge-workspace/` - Testing workspace only
- ❌ Escaped markdown files - Always edit WORKING.md then re-escape
- ❌ Any file after deployment to Forge

## ✅ CORRECT WORKFLOW
1. Edit markdown in `workspace/smart-pins-manual/P2-Smart-Pins-Complete-Reference-WORKING.md`
2. Edit templates in `workspace/manual-templates/*.sty`
3. Run escape script: `WORKING.md → outbound/`
4. Copy templates: `workspace/manual-templates/ → outbound/`
5. User deploys from outbound to Forge

## 🔴 WHY THIS MATTERS
- We lost hours of work editing in outbound instead of workspace
- Outbound gets overwritten every time we deploy
- Only workspace changes are preserved
- Source of truth = workspace, everything else is ephemeral

**REMEMBER**: If you're not editing in workspace/, you're losing your work!

---
Created: 2025-08-29
Reason: Lost work due to editing in wrong location