# AI Privacy Guide - Template Theory of Operations

**Documents:** ai-privacy-guide.md, ai-implementation-strategy.md
**Template Prefix:** `p2kb-presentation-*`
**Version:** 1.0
**Last Updated:** 2025-12-03
**Status:** DEFERRED (not P2-related)

## Overview

The AI Privacy Guide workspace uses a **minimal single-template architecture** designed for presentation-style documents. Unlike technical manuals, this document uses a simple, modern layout without multi-layer template stacks or Lua filters. The workspace is currently deferred in the production pipeline.

## Template Stack Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  p2kb-presentation.latex                     │
│                  (Self-Contained Template)                   │
│   Article class, presentation colors, callout boxes, TOC     │
└─────────────────────────────────────────────────────────────┘
           (No layered .sty files - all in one template)

┌─────────────────────────────────────────────────────────────┐
│                   p2kb-foundation.sty                        │
│                    (Available but NOT used)                  │
└─────────────────────────────────────────────────────────────┘
```

### Loading Order
```latex
1. p2kb-presentation.latex  % Self-contained, no external dependencies
```

## Template Details

### p2kb-presentation.latex (195 lines)

**Purpose:** Self-contained presentation-style document template

**Document Class:** `article` (11pt, letterpaper) - NOT book class

**Key Features:**

**Pandoc Compatibility:**
- `\tightlist`, `\passthrough` commands
- Paragraph/subparagraph fixes
- Standard pandoc variable substitution (`$title$`, `$author$`, etc.)

**Color Palette (Professional Blue/Gray):**

| Color | RGB | Purpose |
|-------|-----|---------|
| PresentationBlue | (41,84,144) | Primary branding |
| AccentBlue | (70,130,180) | Secondary accent |
| DarkGray | (60,60,60) | Body text |
| MidGray | (100,100,100) | Subtle text |
| LightGray | (240,240,240) | Backgrounds |
| SuccessGreen | (40,167,69) | Success indicators |
| WarningOrange | (255,133,27) | Warning indicators |

**Typography:**
- Sans-serif default (`\sfdefault`)
- Clean, modern presentation style
- Colored section headings (blue hierarchy)

**Header/Footer:**
- Left header: Title (PresentationBlue)
- Right header: Date (MidGray)
- Left footer: Company
- Center footer: Page number
- Right footer: "P2 Knowledge Base"
- Colored header/footer rules

**Custom Title Page:**
- Centered layout
- Large title in PresentationBlue
- Subtitle in DarkGray
- Horizontal rules for visual separation
- Author, company, date stack
- P2 Knowledge Base branding at bottom

**Callout Boxes:**
- `\infobox{text}` - Blue border, info icon
- `\warningbox{text}` - Orange border, warning icon
- `\successbox{text}` - Green border, checkmark icon

**Section Formatting (via standard LaTeX, not titlesec):**
- Section: Large, bold, PresentationBlue
- Subsection: large, bold, AccentBlue
- Subsubsection: normalsize, bold, DarkGray

**List Formatting:**
- Itemize level 1: Blue bullets
- Itemize level 2: AccentBlue dashes
- Enumerate: Blue numbers

**Hyperlinks:**
- Blue colored links (not underlined)
- PDF metadata auto-populated from variables

### p2kb-foundation.sty (379 lines)

**Status:** Present in templates/ folder but NOT actively used by this document

**Purpose:** Generic P2KB foundation infrastructure - available for future enhancement if the document becomes more complex

## Lua Filter Pipeline

**No Lua filters are used by this document.**

The presentation template is simple enough that all formatting is handled directly by LaTeX.

## Pandoc Arguments (from request.json)

```json
"pandoc_args": [
  "--pdf-engine=xelatex",
  "--toc",
  "--toc-depth=2"
]
```

**Key Settings:**
- `--pdf-engine=xelatex`: For enhanced typography
- `--toc`: Generate table of contents
- `--toc-depth=2`: Show sections and subsections

**Note:** No `--top-level-division` specified - uses default (section-based)

## Document Files in Workspace

### Primary Documents
| File | Purpose | Status |
|------|---------|--------|
| `ai-privacy-guide.md` | Privacy guidelines for P2 developers | Deferred |
| `ai-implementation-strategy.md` | Technical architecture document | Deferred |
| `ai-privacy-guide-escaped.md` | LaTeX-escaped version | Ready |
| `ai-implementation-strategy-escaped.md` | LaTeX-escaped version | Ready |
| `claude-code-privacy-guide-for-p2-developers.md` | Alternative/variant | Unknown |

### Supporting Files
| File | Purpose |
|------|---------|
| `found/p2kb-presentation.latex` | Possibly an earlier version discovery |

## Naming Convention Compliance

### ⚠️ Needs Review When Work Resumes

| File | Expected Pattern | Current Status |
|------|------------------|----------------|
| `p2kb-presentation.latex` | `p2kb-{docprefix}.latex` | ⚠️ Uses generic "presentation" not document-specific prefix |
| `p2kb-foundation.sty` | Shared file | ✅ Appropriate name |

**Recommended rename when work resumes:** Consider renaming to `p2kb-aiprivacy.latex` or similar document-specific prefix if this document returns to active development.

## Multi-Document Workspace

This workspace produces **two PDFs** from one template:

| Input | Output | Purpose |
|-------|--------|---------|
| `ai-privacy-guide-escaped.md` | `P2KB_AI_Privacy_Guide_v1.0.pdf` | Privacy guidelines |
| `ai-implementation-strategy-escaped.md` | `P2KB_AI_Implementation_Strategy_v1.0.pdf` | Technical architecture |

Both use identical template and pandoc arguments, differing only in metadata (title, subtitle).

## Self-Containment Status

### ✅ Self-Contained (Minimal)
- Single template file handles everything
- No external .sty dependencies
- No Lua filters
- p2kb-foundation.sty present but unused

### 📋 Conversion Notes
- This workspace was designed minimal from the start
- Non-P2 content, so less infrastructure needed
- Can be enhanced to layered architecture if complexity grows

## Why This Template is Different

Unlike the technical manuals (Smart Pins, PASM2, DeSilva), this document:

1. **Uses article class, not book class** - No parts/chapters, just sections
2. **Has no code block styling** - No 3-color or 5-color system needed
3. **Has no pedagogical environments** - No sidetrack/experiment boxes
4. **Has no TikZ diagrams** - No architectural illustrations
5. **Is presentation-focused** - Clean, modern, sponsor-ready

This minimal approach is appropriate for:
- Privacy policy documents
- Strategy presentations
- Sponsor materials
- General audience content

## When Working on This Document

### Before Editing:
1. Note this document is DEFERRED - confirm work should resume
2. Understand this is NOT P2 technical content
3. Review presentation color palette
4. Use callout boxes sparingly

### Callout Box Usage:
```latex
\infobox{Important information for the reader.}

\warningbox{Privacy consideration to be aware of.}

\successbox{Best practice confirmation.}
```

### Deployment:
1. Run LaTeX escape script: `../../../tools/conversion/latex-escape-all.sh`
2. Copy to outbound: `*-escaped.md`, templates/, request.json
3. PDF Forge generates both PDFs from single request.json

## Future Enhancement Notes

If this document returns to active development:

1. **Consider layered architecture** if complexity grows
2. **Add document-specific prefix** (e.g., `p2kb-aiprivacy-*`)
3. **Create content layer** if semantic boxes needed
4. **Add Lua filters** if div-syntax processing needed

Currently, the minimal approach is appropriate for the document's scope.
