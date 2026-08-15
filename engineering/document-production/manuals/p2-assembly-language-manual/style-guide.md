# P2 Assembly Language Manual - Style Guide

**Document:** P2 Assembly Language (PASM2) Manual
**Purpose:** Define visual formatting, typography, and LaTeX conventions

---

## 1. Document Design Philosophy

### 1.1 Design Goals

This manual prioritizes **rapid lookup** and **information density**. The visual design must:

- Enable instant visual parsing of instruction entries
- Distinguish sections at a glance (no hunting for information)
- Present encoding data clearly and accurately
- Support both screen reading and print output
- Maintain professional, authoritative appearance

### 1.2 Contrast with DeSilva Tutorial Style

| Aspect | DeSilva Tutorial | This Reference |
|--------|------------------|----------------|
| Primary use | Sequential reading | Random access lookup |
| Density | Spacious, breathing room | Dense, information-packed |
| Visual elements | Sidetrack boxes, friendly callouts | Encoding boxes, structured entries |
| Color usage | Warm accents, inviting | Functional, minimal |
| Typography | Readable body text focus | Code and tables emphasis |

### 1.3 Visual Identity

The PASM2 Reference Manual visual identity conveys:
- **Authority** - This is the definitive source
- **Precision** - Every detail matters
- **Efficiency** - Find what you need fast
- **Completeness** - Nothing is missing

---

## 2. File Organization & Naming Conventions

### 2.1 Directory Structure

Following the established P2KB document production pattern:

```
/engineering/document-production/
├── manuals/
│   └── p2-assembly-language-manual/       # Guide documents (versioned)
│       ├── README.md                       # Overview and source references
│       ├── creation-guide.md               # Content strategy and architecture
│       ├── voice-guide.md                  # Writing style and tone
│       └── style-guide.md                  # Visual formatting (this document)
│
└── workspace/
    └── p2-assembly-language-manual/       # Working files (active development)
        ├── README.md                       # Workspace-specific quick reference
        ├── P2-Assembly-Language-Manual.md  # Master markdown document
        ├── templates/                      # LaTeX templates (workspace copies)
        │   ├── README.md                   # Template stack documentation
        │   ├── p2kb-pasm2-reference.latex  # Main template
        │   └── p2kb-pasm2-*.sty            # Supporting style files
        ├── filters/                        # Lua filters for Pandoc
        │   └── *.lua
        ├── assets/                         # Images, diagrams
        ├── request.json                    # PDF Forge configuration
        ├── request-requirements.json       # Mandatory pandoc arguments
        └── VERSION-TRACKING.md             # Document version history
```

### 2.2 Template Naming Convention

**Prefix:** `p2kb-pasm2-*`

All LaTeX templates for this manual use the prefix `p2kb-pasm2-` to distinguish from:
- `p2kb-desilva-*` (DeSilva tutorial manual)
- `p2kb-smart-pins-*` (Smart Pins Tutorial — **retired**; the prefix is listed so it is
  recognised, not so it is copied. The live smart-pin manual is
  `p2-io-and-smart-pins-user-guide`, prefix `p2kb-iosp-*`.)
- `p2kb-foundation.*` (shared foundation, if applicable)

### 2.3 Document Naming

**Master Document:** `P2-Assembly-Language-Manual.md`
- Title case with hyphens
- Matches canonical folder name
- Single master file (no `-Working-Copy` variants)

**Backups:** made with **`engineering/tools/backup-file.sh <path>`** — the only sanctioned
way. It writes to `.backups/<repo-relative-path>.<YYYYMMDD-HHMMSS>`, outside the working
tree and covered by one `.gitignore` rule.

- **Never hand-name a backup**, and never add a per-file backup rule to `.gitignore`.
- Never back up a regenerable artifact (workspace renders, generated indexes) — the
  generator is the backup.
- Full rationale: `engineering/standards/BACKUP-CONVENTION.md`

> *(This entry previously prescribed `*.md.backup.YYYYMMDD_HHMMSS` beside the file —
> hand-named, inside the working tree, in direct violation of Sacred Rule #1.)*

### 2.4 Deployment Structure

**Outbound Directory:** `/engineering/document-production/outbound/p2-assembly-language-manual/`

```
outbound/p2-assembly-language-manual/    # FLAT directory - no subdirectories!
├── P2-Assembly-Language-Manual.md        # LaTeX-escaped markdown
├── p2kb-pasm2-reference.latex            # Main template
├── p2kb-pasm2-*.sty                      # Supporting styles (flat, not in templates/)
├── *.lua                                  # Lua filters (flat, not in filters/)
└── request.json                          # PDF Forge configuration
```

**Critical:** Outbound directory must be FLAT. PDF Forge expects all files at root level.

### 2.5 Workspace README Template

Each workspace should have a README.md following this structure:

```markdown
# [Document Name] - Workspace Guide

## Quick Reference
**Canonical Name:** `folder-name`
**Document Title:** Full Document Title
**Creation Guide:** `/engineering/document-production/manuals/folder-name/creation-guide.md`
**Outbound Deployment:** `/engineering/document-production/outbound/folder-name/`
**Status:** [Development Phase]

## Template Stack
**Prefix:** `p2kb-prefix-*`
[Layer documentation]

## Special Requirements
[Any mandatory pandoc arguments, special environments]

## Workflow Quick Start
[Essential commands for content editing and deployment]
```

---

## 3. Typography Standards

### 3.1 Font Families

```latex
% Body text - Professional serif
\setmainfont{TeX Gyre Termes}  % or similar serif

% Headings - Clean sans-serif
\setsansfont{TeX Gyre Heros}   % or similar sans

% Code - Monospace with good glyph coverage
\setmonofont{Fira Code}        % or Inconsolata, Source Code Pro
```

### 3.2 Font Sizes

| Element | Size | Notes |
|---------|------|-------|
| Body text | 10pt | Dense but readable |
| Instruction name (heading) | 14pt bold | Clear entry marker |
| Section headers | 11pt bold | Within entry |
| Code examples | 9pt mono | Slightly smaller for density |
| Encoding diagrams | 8pt mono | Compact bit fields |
| Footnotes | 8pt | Minimal use |

### 3.3 Instruction Name Display

Instruction names appear in multiple contexts:

**As entry heading:**
```latex
\section*{\texttt{\Large\textbf{ADD}}}
\addcontentsline{toc}{section}{ADD}
```

**In prose references:**
```latex
The \instr{ADD} instruction performs...
% Produces: bold uppercase in sans-serif
```

**In code examples:**
```latex
\begin{pasm}
        add     dest, src       wc
\end{pasm}
% Produces: lowercase in monospace
```

**In cross-references:**
```latex
See also: \instrref{ADDX}, \instrref{ADDS}
% Produces: linked references
```

### 3.4 Custom Commands

```latex
% Instruction reference (in prose)
\newcommand{\instr}[1]{\textbf{\textsf{#1}}}

% Instruction cross-reference (linked)
\newcommand{\instrref}[1]{\hyperref[instr:#1]{\textbf{\textsf{#1}}}}

% Register reference
\newcommand{\reg}[1]{\texttt{#1}}

% Flag reference
\newcommand{\flag}[1]{\textsf{#1 flag}}

% Bit field reference
\newcommand{\bitfield}[1]{\texttt{#1}}

% Immediate value
\newcommand{\imm}[1]{\texttt{\##1}}
```

---

## 4. Page Layout

### 4.1 Page Geometry

```latex
\usepackage[
    papersize={8.5in, 11in},  % US Letter
    margin=0.75in,            % Tight margins for density
    inner=0.9in,              % Slightly larger for binding
    outer=0.7in,
    top=0.75in,
    bottom=0.75in,
    headheight=14pt,
    headsep=0.3in,
    footskip=0.4in
]{geometry}
```

### 4.2 Two-Column Option

For Part II (instruction reference), consider two-column layout:

```latex
\usepackage{multicol}
\setlength{\columnsep}{0.3in}
\setlength{\columnseprule}{0.4pt}

% In Part II:
\begin{multicols}{2}
% Instruction entries...
\end{multicols}
```

**Decision point:** Two-column increases density but complicates encoding diagrams. Test both layouts.

### 4.3 Headers and Footers

```latex
\usepackage{fancyhdr}
\pagestyle{fancy}

% Part I chapters
\fancyhead[LE]{\textsl{\leftmark}}   % Chapter name
\fancyhead[RO]{\textsl{\rightmark}}  % Section name
\fancyhead[RE,LO]{}
\fancyfoot[C]{\thepage}

% Part II instruction reference
\fancyhead[LE]{P2 Assembly Language Manual}
\fancyhead[RO]{\textsl{Instructions: \leftmark}}  % Current letter range
\fancyfoot[C]{\thepage}
```

### 4.4 Running Headers for Instruction Section

In alphabetical reference, running headers should show current instruction range:

```
Left page:  "P2 Assembly Language Manual"
Right page: "Instructions: ADD - ADDX"
```

---

## 5. Instruction Entry Formatting

### 5.1 Entry Structure Visual Hierarchy

Each instruction entry follows strict visual hierarchy:

```
┌─────────────────────────────────────────────────────────────┐
│ INSTRUCTION NAME                           [Large, Bold]    │
│ Full Name | Category                       [Subtitle line]  │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ AT A GLANCE BOX                         [Shaded box]    │ │
│ │ Primary syntax, cycles, flags                           │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ SYNTAX                                    [Section header]  │
│   Syntax forms listed                                       │
│                                                             │
│ PARAMETERS                                                  │
│   • Bulleted parameter descriptions                         │
│                                                             │
│ ENCODING                                                    │
│   ┌───────────────────────────────────────────────────────┐ │
│   │ Bit field diagram                    [Bordered box]   │ │
│   └───────────────────────────────────────────────────────┘ │
│                                                             │
│ OPERATION  (only where it earns its place)                  │
│   Compact pseudocode line — NOT numbered steps              │
│                                                             │
│ TIMING                                                      │
│   Cycle and hub access information                          │
│                                                             │
│ RELATED INSTRUCTIONS                                        │
│   Categorized cross-references                              │
│                                                             │
│ EXAMPLE (optional)                                          │
│   Code block with comments                                  │
│                                                             │
│ NOTES (optional)                                            │
│   Pitfalls, tips, hardware notes                            │
└─────────────────────────────────────────────────────────────┘
```

#### 5.1.1 The `Operation:` line — include by exception

The `Operation:` line gives exact pseudocode of an instruction's effect. It is
**not a mandatory field.** Carry it only when an instruction's behavior is **not
obvious from its one-line description.** The test —

**Include an `Operation:` line when ANY of these holds:**
- a **flag-effect subtlety** — C or Z is set from something a reader could get wrong (e.g. ADDS: `C = true sign of (D + S)`; ADDX: `Z = Z AND (result == 0)`);
- an **encoding or operand quirk** — an operand is interpreted in a non-obvious way;
- a **side effect or gotcha** — the instruction does something beyond the headline (e.g. REP shielding its block from interrupts);
- **genuinely complex mechanics** — multi-step, conditional, or bitfield manipulation (the ALT\* family, MUXQ, bit-scan instructions).

**Omit it** when the description plus the syntax already convey the full effect —
the common case. ADD ("add two unsigned values") needs none even though the
source spreadsheet lists `D = D + S`; the line would only restate the
description. **An `Operation:` line on an obvious instruction is redundant noise
and must be trimmed.**

**Consistency within a family.** Presence must track *actual* complexity across
related instructions, not land randomly: if ADDS carries one for its signed-C
semantics, SUBS should too; if ADDX carries one, SUBX should.

**Source — never inferred.** The pseudocode is taken **verbatim** from the
Parallax *P2 Instructions v35 – Rev B/C Silicon* spreadsheet (the operation/
effect column — the same authority used for encodings). Do **not** compose or
reword the operation from reasoning. If the spreadsheet has no operation for a
row, no line is added.

**Format and placement.** `**Operation:**` (bold label) followed by the
pseudocode in inline code, placed **between the syntax line and `**Result:**`.**
The pseudocode must be ASCII (the inline-code path forbids non-ASCII — use `AND`,
`OR`, `->`, `==`, etc.).

**Non-instruction entries.** Assembler directives and special-register entries
carry **no** `Operation:` line — they are not runtime operations.

**Grouped multi-instruction entries** (event-jump / poll / wait families
documented as one entry): if the family's behavior is non-obvious, give a compact
**per-instruction mini-table** (instruction → operation) rather than one line, so
every bundled instruction is covered.

### 5.2 At A Glance Box

```latex
\newenvironment{ataglance}{%
    \begin{tcolorbox}[
        colback=gray!8,
        colframe=gray!40,
        boxrule=0.5pt,
        arc=2pt,
        left=6pt, right=6pt, top=4pt, bottom=4pt,
        fontupper=\ttfamily\small
    ]
}{%
    \end{tcolorbox}
}

% Usage:
\begin{ataglance}
ADD Dest, \{#\}Src \{WC|WZ|WCZ\}\\
Cycles: 2 \quad Hub: No \quad Flags: C=carry, Z=zero
\end{ataglance}
```

### 5.3 Encoding Box

```latex
\newenvironment{encodingbox}{%
    \begin{tcolorbox}[
        colback=white,
        colframe=black,
        boxrule=0.8pt,
        arc=0pt,          % Sharp corners for technical feel
        left=4pt, right=4pt, top=4pt, bottom=4pt,
        fontupper=\ttfamily\footnotesize
    ]
}{%
    \end{tcolorbox}
}
```

### 5.4 Section Headers Within Entry

```latex
\newcommand{\entrysection}[1]{%
    \vspace{6pt}%
    \noindent\textbf{\textsf{#1}}%
    \vspace{2pt}%
    \par
}

% Usage:
\entrysection{SYNTAX}
\entrysection{PARAMETERS}
\entrysection{ENCODING}
```

---

## 6. Code Formatting

### 6.1 PASM2 Code Blocks

```latex
\usepackage{listings}

\lstdefinelanguage{pasm2}{
    morekeywords={add, sub, mov, jmp, call, ret, cmp, test, and, or, xor,
                  rdlong, wrlong, rdbyte, wrbyte, rdword, wrword,
                  waitx, cogid, coginit, hubset, setq, setq2,
                  wc, wz, wcz, if_c, if_nc, if_z, if_nz, if_c_and_z,
                  org, fit, res, byte, word, long},
    sensitive=false,
    morecomment=[l]{'},
    morestring=[b]",
}

\lstdefinestyle{pasm}{
    language=pasm2,
    basicstyle=\ttfamily\small,
    keywordstyle=\bfseries,
    commentstyle=\itshape\color{gray!60!black},
    columns=fixed,
    keepspaces=true,
    showstringspaces=false,
    tabsize=8,
    xleftmargin=2em,
    frame=none,
    aboveskip=4pt,
    belowskip=4pt,
}

\lstnewenvironment{pasm}{\lstset{style=pasm}}{}
```

### 6.2 Code Alignment Standards

PASM2 code follows strict column alignment:

```
Column 1-8:   Label (optional)
Column 9-16:  Instruction mnemonic
Column 17-24: Destination operand
Column 25-32: Source operand
Column 33+:   Effects (WC, WZ) and comments
```

```latex
% Example of properly aligned code:
\begin{pasm}
loop    add     count, #1       wc      ' Increment counter
        addx    count_hi, #0            ' Propagate carry
        djnz    iterations, #loop       ' Loop until done
\end{pasm}
```

### 6.3 Inline Code

```latex
% For instruction mnemonics in prose:
Use \texttt{add} with the \texttt{wc} effect...

% For register names:
The result is stored in \reg{PTRA}...

% For immediate values:
Add \imm{5} to the accumulator...
```

---

## 7. Tables and Diagrams

### 7.1 Parameter Tables

```latex
\newenvironment{paramtable}{%
    \begin{tabular}{@{}l@{\quad}p{0.75\linewidth}@{}}
}{%
    \end{tabular}
}

% Usage:
\begin{paramtable}
\textbullet\ Dest & Register containing first operand; receives the sum \\
\textbullet\ Src & Register, 9-bit immediate, or augmented immediate \\
\textbullet\ WC & Set C flag if unsigned overflow \\
\end{paramtable}
```

### 7.2 Encoding Diagram Style (TikZ)

See `creation-guide.md` Section 8.5 for complete TikZ diagram strategy.

**Key visual standards for encoding diagrams:**

```latex
% Standard encoding diagram dimensions
\newcommand{\bitwidth}{0.28cm}      % Width per bit
\newcommand{\bitheight}{0.6cm}      % Height of bit cells
\newcommand{\labeloffset}{0.3cm}    % Space for bit numbers

% Colors for encoding diagrams
\definecolor{condfield}{HTML}{E8E8E8}   % EEEE condition field
\definecolor{opcodefield}{HTML}{D8D8D8} % Opcode bits
\definecolor{flagfield}{HTML}{F0F0F0}   % CZI flags
\definecolor{destfield}{HTML}{E0E8E0}   % Destination field
\definecolor{srcfield}{HTML}{E0E0E8}    % Source field
```

### 7.3 Categorical Index Tables

```latex
\begin{longtable}{@{}l l p{5cm}@{}}
\toprule
\textbf{Instruction} & \textbf{Cycles} & \textbf{Brief Description} \\
\midrule
\endfirsthead
% ... continuation header ...
\endhead

\multicolumn{3}{l}{\textbf{Math Instructions}} \\
\midrule
ADD & 2 & Add two unsigned values \\
ADDS & 2 & Add two signed values \\
ADDX & 2 & Add with carry-in (extended) \\
% ... etc ...

\bottomrule
\end{longtable}
```

### 7.4 Table Design Decisions

This section documents the rationale behind table formatting choices made during PDF generation refinement.

#### 7.4.1 Encoding Tables - Design Intent

**Goal:** Encoding tables must be visually consistent throughout the document. Every encoding table—whether in Part I explanatory chapters or Part II instruction entries—should look identical so readers learn to parse the format once and apply that knowledge everywhere.

**Structure:** All encoding tables use 9 columns:

| Column | Purpose | Width Strategy |
|--------|---------|----------------|
| EEEE | Condition code | Fixed (5.5%) - always 4 chars |
| Opcode | 7-bit opcode | Fixed (10%) - always 7 chars |
| CZI | Flag/immediate bits | Fixed (3.5%) - always 3 chars |
| D | Destination field | Fixed (11%) - always 9 chars |
| S | Source field | Fixed (11%) - always 9 chars |
| C | C flag effect | Flexible (X) - content varies |
| Z | Z flag effect | Flexible (X) - content varies |
| Result | What's written | Flexible (X) - content varies |
| Clks | Clock cycles | Flexible (X) - content varies |

**Implementation:** Uses `tabularx` with fixed-width columns for the predictable encoding fields (left 5) and flexible `X` columns for the variable-content result fields (right 4). This ensures:
- Encoding fields always align perfectly across all tables
- Result columns share remaining space based on actual content
- Tables respect page margins (use `\linewidth` not `\textwidth`)

**Header styling:** Gray background (`pasm2-encoding-header` color) on header row using `\cellcolor` on each cell. We use `\cellcolor` instead of `\rowcolor` because `\rowcolor` is incompatible with `tabularx` flexible columns.

**Consistency requirement:** The same `encodingtable` environment and `encodingrow`/`encodingrowcont` commands are used in:
- Part I Chapter 2 (instruction format explanation)
- Part II instruction entries
- Any other location showing encoding information

Never use a different table format for encoding data. If a simpler display is needed, use `\simpleencoding` (single-row) which has identical visual appearance.

#### 7.4.2 General Tables - Column Width Strategy

**Problem solved:** Tables with narrow columns (e.g., 10% width) caused text overlap when content exceeded the allocated space.

**Solution:** Minimum column widths of 15% for text-containing columns. This is enforced in the `p2kb-pasm2-tables.lua` filter which processes Pandoc-generated tables.

**Rationale:**
- 10% of `\linewidth` ≈ 0.6 inches - too narrow for most text
- 15% of `\linewidth` ≈ 0.9 inches - accommodates typical cell content
- Tables with many columns may need manual width adjustments in the markdown source

#### 7.4.3 Table Margins and Boundaries

**Problem solved:** Tables extending beyond the right margin to the page edge.

**Solution:** All tables use `\linewidth` (respects current text margins) rather than `\textwidth` (full page width). This ensures tables stay within the content column.

**Implementation:** The encoding table environments in `p2kb-pasm2-content.sty` explicitly use:
```latex
\begin{tabularx}{\linewidth}{...}
```

#### 7.4.4 Visual Consistency Across Document Sections

**Principle:** A reader should not be able to tell which section of the document they're in based on table appearance alone. All tables of the same type (encoding, parameter, reference) should be visually identical regardless of location.

**Specific applications:**
- Encoding examples in Chapter 2 use the same `encodingtable` as Part II entries
- The ADD example in Section 2.8.2 uses `\simpleencoding` (same format as single-row instruction encodings)
- Appendix encoding tables match the Part II format

---

## 8. Special Elements

### 8.1 Note Markers

```latex
% Pitfall warning
\newcommand{\pitfall}[1]{%
    \par\noindent
    \textcolor{warningcolor}{\faExclamationTriangle}%
    \textbf{ Pitfall:} #1
    \par
}

% Tip
\newcommand{\tip}[1]{%
    \par\noindent
    \textcolor{tipcolor}{\faLightbulbO}%
    \textbf{ Tip:} #1
    \par
}

% Hardware note
\newcommand{\hardwarenote}[1]{%
    \par\noindent
    \textcolor{hardwarecolor}{\faWrench}%
    \textbf{ Hardware:} #1
    \par
}

% Colors for notes
\definecolor{warningcolor}{HTML}{CC6600}  % Orange for pitfalls
\definecolor{tipcolor}{HTML}{006699}       % Blue for tips
\definecolor{hardwarecolor}{HTML}{666666}  % Gray for hardware
```

### 8.2 Cross-Reference Formatting

```latex
% Related instructions section
\newcommand{\related}[1]{%
    \entrysection{RELATED INSTRUCTIONS}
    #1
}

% Usage:
\related{
    \textbullet\ \textbf{Family:} \instrref{ADDX}, \instrref{ADDS}, \instrref{ADDSX}\\
    \textbullet\ \textbf{Contrast:} \instrref{SUB}\\
    \textbullet\ \textbf{See also:} \instrref{ADDCT1}, \instrref{ADDPIX}
}
```

### 8.3 Flag Effect Summary

```latex
\newcommand{\flageffects}[2]{%
    \par\noindent
    \textbf{C Flag:} #1\\
    \textbf{Z Flag:} #2
    \par
}

% Usage:
\flageffects{Set if carry (unsigned overflow)}{Set if result is zero}
```

---

## 9. Color Palette

### 9.1 Functional Colors

```latex
% Primary palette - minimal, functional
\definecolor{p2kb-dark}{HTML}{2C3E50}      % Dark blue-gray (headings)
\definecolor{p2kb-medium}{HTML}{7F8C8D}    % Medium gray (secondary)
\definecolor{p2kb-light}{HTML}{ECF0F1}     % Light gray (backgrounds)
\definecolor{p2kb-accent}{HTML}{3498DB}    % Blue (links, highlights)

% Encoding diagram colors
\definecolor{encoding-cond}{HTML}{E8E8E8}  % Condition field
\definecolor{encoding-op}{HTML}{D0D0D0}    % Opcode field
\definecolor{encoding-flag}{HTML}{E8E0E0}  % Flag field
\definecolor{encoding-dest}{HTML}{E0E8E0}  % Dest field
\definecolor{encoding-src}{HTML}{E0E0E8}   % Src field

% Note colors
\definecolor{pitfall-bg}{HTML}{FFF3E0}     % Light orange
\definecolor{tip-bg}{HTML}{E3F2FD}         % Light blue
\definecolor{hardware-bg}{HTML}{F5F5F5}    % Light gray
```

### 9.2 Color Usage Rules

- **Headings:** p2kb-dark for instruction names, black for section headers
- **Body text:** Black (never gray for main content)
- **Code:** Black on white (maximum contrast)
- **Links:** p2kb-accent (blue), underlined in PDF
- **Backgrounds:** Minimal use, only for boxes and diagrams
- **Encoding diagrams:** Subtle field differentiation, not distracting

---

## 10. Part I Chapter Formatting

### 10.1 Chapter Opening

```latex
\newcommand{\partichapter}[2]{%
    \chapter{#1}
    \begin{center}
    \large\itshape #2  % Chapter subtitle/summary
    \end{center}
    \vspace{1em}
}

% Usage:
\partichapter{The P2 Execution Model}{%
    Understanding cogs, Hub memory, and the unique P2 architecture
}
```

### 10.2 Key Concepts Box

Each Part I chapter ends with a summary box:

```latex
\newenvironment{keyconcepts}{%
    \vspace{1em}
    \begin{tcolorbox}[
        colback=p2kb-light,
        colframe=p2kb-dark,
        title={\textbf{Key Concepts}},
        fonttitle=\sffamily
    ]
    \begin{itemize}[leftmargin=*, nosep]
}{%
    \end{itemize}
    \end{tcolorbox}
}

% Usage:
\begin{keyconcepts}
\item Each cog has 512 longs of private register memory
\item Hub memory is shared among all cogs
\item Hub access follows the "egg beater" timing pattern
\item Most instructions execute in 2 clock cycles
\item The P2 achieves determinism through architecture, not interrupts
\end{keyconcepts}
```

---

## 11. Appendix Formatting

### 11.1 Master Encoding Table

```latex
\begin{landscape}
\begin{longtable}{@{}l l l l l l@{}}
\caption{Complete Instruction Encoding Table} \\
\toprule
\textbf{Instruction} & \textbf{Opcode} & \textbf{CZI} & \textbf{Cycles} & \textbf{C Effect} & \textbf{Z Effect} \\
\midrule
\endfirsthead
% ... continuation ...
\endhead

ADD  & 0001000 & CZI & 2 & Carry    & Zero \\
ADDS & 0001010 & CZI & 2 & Overflow & Zero \\
% ... all 359 instructions ...

\bottomrule
\end{longtable}
\end{landscape}
```

### 11.2 Categorical Index Format

Group instructions by function with brief descriptions:

```latex
\section*{Appendix B: Categorical Instruction Index}

\subsection*{Math Instructions}
\begin{multicols}{2}
\begin{description}[style=nextline, leftmargin=1em]
\item[\instrref{ADD}] Add unsigned values
\item[\instrref{ADDS}] Add signed values
\item[\instrref{ADDX}] Add with carry-in
% ...
\end{description}
\end{multicols}
```

---

## 12. Index Generation

### 12.1 Index Entry Types

```latex
% Primary instruction entry
\newcommand{\indexinstr}[1]{\index{#1@\texttt{#1}|textbf}}

% Category entry
\newcommand{\indexcat}[2]{\index{#1!#2@\texttt{#2}}}

% Concept entry
\newcommand{\indexconcept}[1]{\index{#1}}

% Usage in instruction entry:
\indexinstr{ADD}
\indexcat{Math Instructions}{ADD}
\indexconcept{unsigned addition}
```

### 12.2 Index Formatting

```latex
\usepackage{imakeidx}
\makeindex[columns=3, intoc, options={-s index_style.ist}]

% In preamble, create index_style.ist with:
% heading_prefix "{\\bfseries "
% heading_suffix "}\\nopagebreak\n"
% headings_flag 1
```

---

## 13. PDF Output Settings

### 13.1 PDF Metadata

```latex
\usepackage{hyperref}
\hypersetup{
    pdftitle={P2 Assembly Language (PASM2) Manual},
    pdfauthor={P2 Knowledge Base Project},
    pdfsubject={Propeller 2 Assembly Language Reference},
    pdfkeywords={Propeller 2, P2, PASM2, assembly language, reference},
    pdfcreator={LaTeX with hyperref},
    colorlinks=true,
    linkcolor=p2kb-accent,
    urlcolor=p2kb-accent,
    bookmarks=true,
    bookmarksnumbered=true,
    bookmarksopen=true,
    bookmarksopenlevel=1
}
```

### 13.2 PDF Bookmarks Structure

```
P2 Assembly Language Manual
├── How to Use This Manual
├── Part I: Architectural Foundation
│   ├── Chapter 1: The P2 Execution Model
│   ├── Chapter 2: The Instruction Format
│   ├── Chapter 3: Flags and Conditional Execution
│   ├── Chapter 4: Timing and Determinism
│   └── Chapter 5: Special Hardware Overview
├── Part II: Language Reference
│   ├── Instructions A-B
│   ├── Instructions C-D
│   │   (collapsed by default - 359 entries)
│   ├── Directives
│   ├── Constants
│   └── Special Registers
├── Part III: Appendices
│   ├── A. Instruction Encoding Table
│   ├── B. Categorical Index
│   └── ...
└── Index
```

---

## 14. Quality Checklist

### 14.1 Visual Consistency

- [ ] All instruction entries use identical section structure
- [ ] At a Glance boxes are visually identical
- [ ] Encoding boxes use consistent dimensions
- [ ] Code examples follow alignment standards
- [ ] Cross-references are properly formatted and linked
- [ ] Note markers (pitfall/tip/hardware) use consistent styling

### 14.2 Typography Consistency

- [ ] Instruction names: bold sans-serif in prose, monospace in code
- [ ] Register names: always monospace
- [ ] Flag references: always "C flag" / "Z flag" format
- [ ] Section headers: consistent sizing and spacing
- [ ] Code blocks: consistent indentation and column alignment

### 14.3 Color Consistency

- [ ] Encoding diagrams use standard field colors
- [ ] Note backgrounds match their type
- [ ] Links are consistently colored
- [ ] No gratuitous color use

### 14.4 PDF Quality

- [ ] All hyperlinks work
- [ ] Bookmarks navigate correctly
- [ ] Index entries link to correct pages
- [ ] No orphaned headings (instruction name on one page, content on next)
- [ ] Tables don't break awkwardly across pages

---

## 15. LaTeX Package Requirements

```latex
% Essential packages
\usepackage{fontspec}           % Modern font handling
\usepackage{geometry}           % Page layout
\usepackage{fancyhdr}           % Headers/footers
\usepackage{tcolorbox}          % Colored boxes
\usepackage{listings}           % Code formatting
\usepackage{longtable}          % Multi-page tables
\usepackage{booktabs}           % Professional tables
\usepackage{multicol}           % Multi-column layout
\usepackage{hyperref}           % PDF links
\usepackage{imakeidx}           % Index generation
\usepackage{tikz}               % Diagrams
\usepackage{xcolor}             % Color definitions
\usepackage{enumitem}           % List customization
\usepackage{pdflscape}          % Landscape pages

% TikZ libraries
\usetikzlibrary{shapes.geometric, arrows.meta, positioning, calc}

% Font Awesome for icons (optional)
\usepackage{fontawesome}
```

---

## 16. Template File Location

The master LaTeX template for this manual will be:

```
/engineering/document-production/templates/master/p2kb-pasm2-reference.latex
```

When ready for PDF generation, deploy to:

```
/engineering/pdf-forge/production/p2-assembly-language-manual/
├── p2-assembly-language-manual.md    # Combined markdown
├── p2kb-pasm2-reference.latex        # LaTeX template
├── request.json                       # PDF Forge request
└── lua/                               # Any Lua filters needed
```

---

*Last Updated: 2025-12-02*
*Version: 1.1 - Added Section 7.4 Table Design Decisions*
