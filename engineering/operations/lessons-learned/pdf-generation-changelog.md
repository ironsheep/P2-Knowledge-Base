# PDF Generation Changelog & Lessons Learned

**Purpose**: Document issues discovered during PDF generation work to inform future document production. Read this before starting work on any new document.

**Last Updated**: 2025-11-24 (DeSilva Manual work)

---

## Critical Issues

### 1. XeLaTeX Font Configuration (2025-11-24)
**Symptom**: Apostrophes and special characters missing or corrupted in PDF output.

**Cause**: Using `inputenc` and `fontenc` packages which are for pdfLaTeX, not XeLaTeX.

**Wrong**:
```latex
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage{lmodern}
```

**Correct** (for XeLaTeX with `--pdf-engine=xelatex`):
```latex
\RequirePackage{fontspec}
\setmainfont{Latin Modern Roman}
\setsansfont{Latin Modern Sans}
\setmonofont{Latin Modern Mono}
```

**Rule**: Always check which PDF engine is being used. XeLaTeX requires `fontspec`.

---

### 2. Pandoc Strips Document-Level LaTeX Commands (2025-11-24)
**Symptom**: Commands like `\pagestyle{empty}`, `\begin{titlepage}`, `\enlargethispage` disappear from output.

**Cause**: Pandoc filters out certain "document-level" commands from raw LaTeX blocks in markdown.

**Wrong** (in markdown):
```markdown
```{=latex}
\pagestyle{empty}
\begin{titlepage}
...content...
\end{titlepage}
```
```

**Correct**: Put document-level commands in the `.latex` template file:
```latex
\begin{document}

% Title page setup - these survive because they're in template
\pagestyle{empty}
\enlargethispage{2cm}

$body$
```

**Rule**: Any command that controls page-level behavior belongs in the template, not the markdown.

---

### 3. Two-Sided Layout Creates Blank Pages (2025-11-24)
**Symptom**: Blank pages appearing before parts/chapters.

**Cause**: `\documentclass[twoside]{book}` forces parts/chapters to start on odd (right-hand) pages, inserting blanks as needed.

**Solution for screen PDFs**:
```latex
\documentclass[12pt,letterpaper,oneside]{book}
```

**Solution for print with binding** (future):
```latex
\documentclass[12pt,letterpaper,twoside,openany]{book}
```

**Decision**: Use `oneside` for screen viewing. Document in template header that `twoside,openany` is needed for physical print.

---

### 4. Chapter Commands Force Page Breaks (2025-11-24)
**Symptom**: Short front matter sections (License, Trademarks, Disclaimer) each on separate pages.

**Cause**: In markdown with `--top-level-division=part`:
- `#` → `\part{}`
- `##` → `\chapter{}` (forces page break by default)
- `###` → `\section{}` (no page break)

**Wrong**:
```markdown
# Copyright and License
## License
## Trademarks
## Disclaimer
```

**Correct**:
```markdown
# Copyright and License
### License
### Trademarks
### Disclaimer
```

**Rule**: Use `###` (sections) for short items that should flow together. Use `##` (chapters) for substantial content sections.

---

### 5. Part Pages Show Stale Header Content (2025-11-24)
**Symptom**: Header on "Dedication" page shows "Disclaimer" (the previous chapter title).

**Cause**: `\part{}` doesn't clear the chapter mark (`\leftmark`), so headers retain the last chapter's name.

**Fix** in foundation.sty:
```latex
\renewcommand{\part}[1]{%
  \clearpage
  \stepcounter{currentpart}
  \markboth{}{}% <-- ADD THIS: Clear header marks
  \@part{#1}
  ...
}
```

Also change part pages from `\thispagestyle{plain}` to `\thispagestyle{empty}` to avoid showing any header.

---

### 6. Image Paths in XeLaTeX vs Pandoc (2025-11-24)
**Symptom**: Images work in some contexts but not others.

**Cause**:
- Pandoc uses `--resource-path` for finding images
- XeLaTeX uses `TEXINPUTS` environment variable
- PDF Forge sets `TEXINPUTS=./templates//` only

**Solution**: Reference images from paths Pandoc can resolve (`inbox/assets/`), and put image references in markdown (where Pandoc processes them) rather than in raw LaTeX in the template.

**Rule**: Keep images in `inbox/assets/` and reference from markdown, not template.

---

## Process Improvements

### Outbound File Management
- Files are "sticky" on PDF Forge - only send changed files after initial deployment
- Always include `request.json` with each submission
- Clean `.tex` diagnostic files and `.DS_Store` from outbound before submission
- Keep outbound clean between runs

### Template Naming Convention
Format: `p2kb-[doc-prefix]-[name].sty/latex/lua`

Examples:
- `p2kb-desilva-foundation.sty`
- `p2kb-desilva-content.sty`
- `p2kb-desilva.latex`
- `p2kb-desilva-code-coloring.lua`

### Document Decision Recording
Document layout decisions in template headers:
```latex
% LAYOUT DECISION (2025-11-24):
% Using oneside for PDF screen viewing - consistent margins, no blank pages.
% For physical print with binding, change to: twoside,openany
```

---

## Checklist for New Documents

Before starting PDF work on a new document:

- [ ] Read this changelog for known issues
- [ ] Verify template uses `fontspec` (not `inputenc`/`fontenc`) if using XeLaTeX
- [ ] Check `\documentclass` options match intended output (screen vs print)
- [ ] Ensure page-level commands are in template, not markdown
- [ ] Review heading levels - use `###` for short flowing content
- [ ] Test title page and front matter pagination early
- [ ] Verify apostrophes and special characters render correctly in first test PDF
