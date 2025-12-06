# PDF Generation Rules for Claude

**Purpose**: Critical rules for PDF work - prevents common mistakes that waste time.

**Read first**: `engineering/document-production/PDF-PRODUCTION-ARCHITECTURE.md`

---

## Cardinal Rule: Edit in the Right Place

| Edit Type | Correct Location | WRONG Location |
|-----------|------------------|----------------|
| Content changes | `manuals/[doc]/opus-master/` | workspace/ or outbound/ |
| Template changes | `workspace/[doc]/templates/` | outbound/ |
| Filter changes | `workspace/[doc]/filters/` | outbound/ |

**Why**: Editing workspace copies instead of manuals/opus-master causes double-work. The workspace contains production copies assembled FROM the masters.

---

## Never Generate PDFs Locally

Local Pandoc exists but is **off-limits**:
- Local: v1.19.2.1 (ancient, NO Lua filter support)
- PDF Forge: v2.17.1.1 (modern, full support)

**Pretend local Pandoc doesn't exist.** All PDF generation happens on PDF Forge.

---

## File Naming Discipline

**Forbidden**:
- `template-fixed.sty`
- `template-v2.latex`
- `request-test.json`
- ANY `-fixed`, `-v2`, `-working`, `-new` suffixes

**Required**:
- Edit existing files in place
- Request file is ALWAYS `request.json`
- Document filenames never change

---

## Outbound Structure

**Outbound is FLAT** - no subdirectories for templates or filters:

```
outbound/[doc-name]/
├── Document.md        ← Escaped
├── template.latex     ← At root, not in templates/
├── styles.sty         ← At root, not in templates/
├── filter.lua         ← At root, not in filters/
└── request.json
```

---

## What Claude Does vs User Does

| Claude | User |
|--------|------|
| Edit content in manuals/opus-master/ | Deploy outbound to PDF Forge |
| Prepare templates in workspace/ | Run PDF generation |
| Stage escaped files to outbound/ | Provide visual feedback |
| Run interactive tests (when enabled) | Start Forge listener |

---

## Quick Checklist Before Staging

- [ ] Content edits made in `manuals/opus-master/`, not workspace
- [ ] LaTeX escape script run on markdown
- [ ] Files staged to outbound (FLAT structure)
- [ ] request.json is valid
- [ ] No forbidden file naming patterns

---

## Related Documents

- `PDF-PRODUCTION-ARCHITECTURE.md` - Complete architecture overview
- `work-modes/production-pdf-generation.md` - Production workflow
- `work-modes/automated-pdf-testing.md` - Interactive testing
- `PRODUCTION-REQUEST-FORMAT.md` - Request format reference

---

*If questioning these rules: Local Pandoc incompatibility wasted hours. Wrong edit locations caused double-work. These rules prevent real problems.*
