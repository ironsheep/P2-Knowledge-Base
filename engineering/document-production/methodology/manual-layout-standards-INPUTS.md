# Manual Layout Standards — Collected Inputs

**Status:** Raw collection, assembly in progress
**Purpose:** Gather external-agent input on general manual-production layout/typography
practices into one place. This is **not** specific to any single manual. Once all parts
are collected, we analyze and produce a synthesized recommendation (and may promote a
clean `manual-layout-standards.md` from the result).

**Handling:** Each part is preserved **verbatim** under its own labeled section to keep the
source intact for analysis.

---

## Part 1 — Traditional hardcopy layout standards (conventions & best practices)

> Topic: Are there traditional hardcopy layout standards for figures, tables, how things
> split across page boundaries, what matter stays together (titles/intro, paragraphs,
> footers), and are there publications providing standards for typeset manuals?

Yes—there are long-standing typographic and publishing conventions for this, even if they are not always framed as one universal "standard." The core ideas are to keep related material together, avoid awkward splits, and let tables/figures either fit cleanly or continue in a clearly signposted way.

### What should stay together

Common practice is to keep these items from being awkwardly broken across pages:

- A heading with at least the first paragraph that follows it, often called "keep with next" in layout software.
- A paragraph's first or last single line at a page boundary, which is the widow/orphan problem and is usually controlled automatically or manually.
- Table titles with their tables, and figure captions with their figures, so the reader does not have to hunt for the label.
- Short items like bibliography entries or list items, when they would look silly split over pages; the preferred fix is "keep lines together," not a hard manual page break.

### Tables and figures

For tables, the usual guidance is: keep the title/caption with the table, repeat the header row on continuation pages, and label continuation pages clearly, such as "Table 1 (continued)". For figures, many style guides prefer the full figure caption to stay with the figure, and if a figure truly spans pages, it should be handled deliberately rather than split casually. Many academic and technical guides also recommend placing tables and figures close to their first mention, or grouping them at the end if that produces a cleaner document.

### Widows and orphans

Widows and orphans are among the most widely recognized page-break problems in typography: a widow is a short line at the top of a page, and an orphan is a stranded first line at the bottom of a page. Professional layout practice generally tries to avoid them, but modern guidance accepts that occasional exceptions may be less disruptive than forcing ugly white space or over-manipulating the layout. The standard fixes are keep-lines-together, keep-with-next, adjusting hyphenation/spacing, and only then rewriting text or moving objects.

### Good manual rules

For a good-looking manual, these rules usually help most:

- Start chapters on a new page.
- Keep section headings with at least 1–2 following lines or the first paragraph.
- Avoid leaving a heading at the bottom of a page with no body text after it.
- Avoid splitting a table or figure unless you clearly mark the continuation.
- Use consistent margins, caption placement, and spacing around visuals.
- Prefer automatic pagination controls over hand-inserted page breaks wherever possible.

---

## Part 2 — Implementing the standards in LaTeX

> Topic: How LaTeX encodes the "what stays together" rules — penalties, floats, float-control
> packages, longtable, needspace — and the automation-vs-forcing balance.

LaTeX is a good fit for this. The "what should stay together" rules are typographic, and LaTeX gives you mechanisms to encode them in your document so the layout looks professional.

### Core LaTeX tools for layout

LaTeX already implements most traditional page-breaking rules with:

- **Paragraphs and headings:** it avoids overfull pages and bad breaks by default; you can fine-tune with penalties like `\clubpenalty` (no orphan first lines) and `\widowpenalty` (no widow last lines).
- **Floats (figures/tables):** environments like `figure` and `table` are floats whose placement is controlled by options `[htbp]` ("here", top, bottom, float page).
- **Float control packages:** `placeins` adds `\FloatBarrier` per section so floats do not drift too far; `flafter` prevents floats from appearing before their mention.

Example:

```tex
\usepackage[section]{placeins} % keep floats in their section
\usepackage{flafter}           % no float before first reference
```

This encodes "keep related material close" without manually forcing every page break.

### Keeping figures and tables "with" their content

To keep captions and objects visually coherent:

- Use standard `figure`/`table` floats with caption inside the environment so LaTeX naturally keeps them together.
- Use placement options like `[htbp]` and avoid overusing `H` (from the float package), which can destroy LaTeX's ability to optimize page breaks.
- For long tables, use `longtable` or similar, which repeats headers on each page and clearly indicates continuation; this mimics the "Table X (continued)" convention.

Example:

```tex
\begin{figure}[htbp]
  \centering
  \includegraphics{myplot}
  \caption{Signal timing diagram}
  \label{fig:signal-timing}
\end{figure}
```

For tabular data:

```tex
\usepackage{longtable}
...
\begin{longtable}{lll}
\caption{Instruction encodings}\label{tab:insn-enc}\\
\hline
Opcode & Mnemonic & Description\\
\hline
\endfirsthead
\multicolumn{3}{c}{\tablename\ \thetable\ (continued)}\\
\hline
Opcode & Mnemonic & Description\\
\hline
\endhead
...
\end{longtable}
```

This implements the "multi-page table with repeated header and continuation label" best practice.

### Controlling bad page breaks (widows, orphans, headings)

Traditional rules like "no heading at the bottom of a page with no text after it" and "avoid widows/orphans" can be handled by:

Global penalties in the preamble:

```tex
\clubpenalty=10000  % avoid orphan first lines
\widowpenalty=10000 % avoid widow last lines
```

These correspond directly to the widow/orphan controls from typography and word processors.

Using `\needspace{<len>}` (from the needspace package) before headings or special blocks so they move to the next page if there isn't enough room.

Example:

```tex
\usepackage{needspace}
...
\needspace{4\baselineskip}
\section{Propeller 2 CORDIC Engine}
```

This encodes the rule "heading + some following lines must stay together."

### Balancing "automation vs. forcing"

The main LaTeX-specific best practices echo what book designers say:

- Let LaTeX float figures and tables using sensible `[htbp]` hints; do not fight it with `[H]` everywhere, which tends to create awkward white space and bad breaks.
- Use `\clearpage` or `\FloatBarrier` only at logical boundaries (e.g., before a new chapter/major section) to flush queued floats, not constantly throughout the text.
- Encode rules in styles and packages (penalties, placeins, longtable, needspace) rather than sprinkling manual `\newpage` and `\pagebreak` commands, which can make maintenance painful.

### Putting it all together for a "manual" look

For an embedded-systems style manual in LaTeX, a practical baseline setup might be:

```tex
\usepackage[section]{placeins}
\usepackage{flafter}
\usepackage{longtable}
\usepackage{needspace}
\clubpenalty=10000
\widowpenalty=10000
```

Then adopt these habits:

- Use `figure`/`table` with `[htbp]` for all illustrations and data.
- Use `longtable` for anything that might span pages.
- Precede major headings and important code examples with `\needspace`.
- Use `\clearpage` or `\FloatBarrier` only before big structural jumps (e.g., between chapters).

> Offer from source: a minimal LaTeX template (preamble plus a few example sections,
> figures, and tables) tuned for a hardware datasheet or programming reference.

---

## Part 3 — Minimal LaTeX manual/datasheet template (worked example)

> Topic: A compact LaTeX "manual/datasheet" template tuned for hardware/programming
> references, baking in float behavior, widow/orphan control, multi-page tables, and
> Note/Warning blocks.
>
> **IMPORTANT — not literal guidance.** This is sample output from the external agent.
> It must be studied against our own PDF Forge / template system before any of it is
> adopted. Do not treat any package, macro, or default here as a recommendation yet.

Here's a compact LaTeX "manual/datasheet" template tuned for hardware and programming references. It bakes in decent defaults for floats, widows/orphans, and multi-page tables.

### High-level structure

Features baked in:

- Book/report class with chapter/section structure.
- Better float behavior for figures/tables.
- Widow/orphan control and "keep heading with content" tricks.
- Example figure, single-page table, and long multi-page table.
- A "Note/Warning" block style that tries not to split awkwardly.

You can drop this into `manual.tex` and compile with `pdflatex` or `lualatex`.

```tex
\documentclass[11pt,a4paper]{report}

% ------------------
% Packages & layout
% ------------------
\usepackage[margin=1in]{geometry}
\usepackage{graphicx}
\usepackage{booktabs}   % nicer tables
\usepackage{longtable}  % multipage tables
\usepackage{array}
\usepackage{amsmath}
\usepackage{hyperref}
\usepackage[section]{placeins} % keep floats in their section
\usepackage{flafter}           % floats never before first reference
\usepackage{needspace}         % keep headings with following text
\usepackage{xcolor}
\usepackage{caption}
\usepackage{listings}          % code listings

% ------------------
% Widow/orphan control
% ------------------
\clubpenalty=10000   % no single first line of paragraph at bottom (orphan)
\widowpenalty=10000  % no single last line of paragraph at top (widow)

% ------------------
% Hyperref setup
% ------------------
\hypersetup{
  colorlinks=true,
  linkcolor=blue,
  urlcolor=blue,
  citecolor=blue
}

% ------------------
% Code listings style
% ------------------
\lstdefinestyle{code}{
  basicstyle=\ttfamily\small,
  frame=single,
  breaklines=true,
  columns=fullflexible,
  keepspaces=true,
  numbers=left,
  numberstyle=\tiny,
  xleftmargin=2em
}

\lstset{style=code}

% ------------------
% Simple Note/Warning environments
% ------------------
\newcommand{\Note}[1]{%
  \needspace{3\baselineskip}%
  \noindent\textbf{Note:} #1%
}

\newcommand{\Warning}[1]{%
  \needspace{4\baselineskip}%
  \noindent\textbf{\textcolor{red}{Warning:}} #1%
}

% ------------------
% Sectioning helpers
% ------------------
% Ensure there's space for heading + at least 2 lines of text.
\newcommand{\safeSection}[1]{%
  \needspace{4\baselineskip}%
  \section{#1}%
}

\newcommand{\safeSubsection}[1]{%
  \needspace{3\baselineskip}%
  \subsection{#1}%
}

\begin{document}

\title{Example Hardware Reference Manual}
\author{Your Company Name}
\date{\today}

\maketitle
\tableofcontents
\clearpage

% ------------------
% Chapter 1
% ------------------
\chapter{Overview}

\safeSection{Device Summary}

This manual describes the \emph{P2X8C4M64P}-style multicore microcontroller,
its internal architecture, and recommended programming practices in C, Spin,
and assembly.

\Note{This template is intended as a starting point for a hardware datasheet
or programming reference. Adjust fonts, spacing, and colors to match your
house style.}

\safeSection{Key Features}

\begin{itemize}
  \item Eight identical 32-bit cores with shared hub RAM.
  \item Deterministic instruction timing.
  \item Multiple smart pins for serial, PWM, and timing functions.
  \item On-chip boot ROM with serial and SPI boot options.
\end{itemize}

% ------------------
% Example Figure
% ------------------
\safeSection{Block Diagram}

As shown in Figure~\ref{fig:block-diagram}, the device uses a shared hub
memory with independent COGs and smart I/O pins.

\begin{figure}[htbp]
  \centering
  % Replace with your actual diagram
  \fbox{\rule{0pt}{2in}\rule{3in}{0pt}}%
  \caption{Top-level device block diagram}
  \label{fig:block-diagram}
\end{figure}

\Warning{Ensure that all supply rails are within specification before
releasing reset. Undervoltage conditions can lead to unpredictable behavior.}

\clearpage

% ------------------
% Chapter 2
% ------------------
\chapter{Electrical Characteristics}

\safeSection{Absolute Maximum Ratings}

Table~\ref{tab:abs-max} lists the absolute maximum ratings. Operation outside
these limits can cause permanent damage.

\begin{table}[htbp]
  \centering
  \caption{Absolute maximum ratings}
  \label{tab:abs-max}
  \begin{tabular}{@{} l l l @{}}
    \toprule
    Parameter      & Min        & Max        \\
    \midrule
    Supply voltage & -0.3 V     & 4.0 V      \\
    I/O pin voltage & -0.3 V    & V\textsubscript{DD} + 0.3 V \\
    Storage temp   & -55 \(^{\circ}\)C & +150 \(^{\circ}\)C \\
    \bottomrule
  \end{tabular}
\end{table}

\safeSection{Operating Conditions}

The device is intended for operation under the conditions summarized
in Table~\ref{tab:operating}.

\begin{table}[htbp]
  \centering
  \caption{Recommended operating conditions}
  \label{tab:operating}
  \begin{tabular}{@{} l l l @{}}
    \toprule
    Parameter          & Min       & Max        \\
    \midrule
    V\textsubscript{DD} core       & 1.8 V     & 1.9 V     \\
    V\textsubscript{DD} I/O        & 3.0 V     & 3.6 V     \\
    Ambient temperature & -40 \(^{\circ}\)C & +85 \(^{\circ}\)C \\
    \bottomrule
  \end{tabular}
\end{table}

\clearpage

% ------------------
% Chapter 3
% ------------------
\chapter{Programming Model}

\safeSection{Core Architecture}

Each core executes instructions from hub memory or local COG memory
with deterministic timing. Interrupts are typically replaced by
deterministic polling or explicit event scheduling.

\safeSubsection{Register Summary}

Table~\ref{tab:registers-long} shows an example of a long register map that
may span multiple pages. The \texttt{longtable} environment handles
header repetition and continuation labels.

\setlength{\LTpre}{0pt}
\setlength{\LTpost}{0pt}

\begin{longtable}{@{} l l p{7cm} @{}}
\caption{Example control register map}
\label{tab:registers-long}\\
\toprule
Address & Name   & Description \\
\midrule
\endfirsthead

\multicolumn{3}{c}{\tablename~\thetable\ (continued)}\\
\toprule
Address & Name   & Description \\
\midrule
\endhead

\bottomrule
\endfoot

0x0000 & CTRL0  & Global control register 0. Enables core clocks and basic
                 configuration. \\
0x0004 & CTRL1  & Global control register 1. Configures debug options
                 and boot mode. \\
0x0008 & STATUS & Global status register. Indicates reset reason, clock
                 status, and fault conditions. \\
0x000C & INTEN  & Interrupt enable mask for optional event sources. \\
0x0010 & INTSTS & Interrupt status flags for optional event sources. \\
0x0014 & GPIO0  & GPIO port 0 direction and output control. \\
0x0018 & GPIO1  & GPIO port 1 direction and output control. \\
0x001C & GPIO2  & GPIO port 2 direction and output control. \\
0x0020 & GPIO3  & GPIO port 3 direction and output control. \\
0x0024 & TIMER0 & Timer 0 configuration and counter. \\
0x0028 & TIMER1 & Timer 1 configuration and counter. \\
0x002C & TIMER2 & Timer 2 configuration and counter. \\
0x0030 & TIMER3 & Timer 3 configuration and counter. \\
0x0034 & UART0  & UART0 configuration and status. \\
0x0038 & UART1  & UART1 configuration and status. \\
0x003C & SPI0   & SPI0 configuration and status. \\
0x0040 & SPI1   & SPI1 configuration and status. \\
% ... add as many rows as needed ...
\end{longtable}

\safeSubsection{Code Example}

Listing~\ref{lst:init} shows a short initialization sequence.

\begin{lstlisting}[language=C,caption={Example device initialization},label={lst:init}]
#include <stdint.h>

#define REG32(addr) (*(volatile uint32_t *)(addr))

#define CTRL0   0x00000000u
#define STATUS  0x00000008u
#define GPIO0   0x00000014u

void init_device(void)
{
    /* Enable core clocks */
    REG32(CTRL0) = 0x00000001u;

    /* Configure GPIO0 as outputs, initial low */
    REG32(GPIO0) = 0x0000FFFFu;

    /* Wait for clock stable indication */
    while ((REG32(STATUS) & 0x1u) == 0u) {
        /* spin */
    }
}
\end{lstlisting}

\end{document}
```

### How this template addresses the concerns (per source)

- **Widows/orphans:** `\clubpenalty` and `\widowpenalty` are set high so LaTeX works harder to avoid single lines at page tops/bottoms.
- **Headings plus intro text:** `\safeSection` and `\safeSubsection` use `\needspace` to ensure there is room for the heading and a few lines of text before a page break.
- **Figures and tables:** They use proper float environments with `[htbp]`, relying on LaTeX's float placement rather than hard `\newpage`s.
- **Multi-page tables:** `longtable` repeats headers and adds a "(continued)" line, matching common datasheet practice.
- **Special blocks:** `\Note` and `\Warning` reserve vertical space with `\needspace` to avoid being stranded at the bottom of a page.

## Part 4 — Table-internal layout rules (lightweight, scannable tables)

> Topic: General rules for the *inside* of a table — header presentation, borders/rules,
> alignment, row/column ordering, how a table starts and ends, and cross-manual
> consistency — to make tables easier and lighter to read.
>
> **Not literal guidance** — to be studied against our own table conventions and
> PDF Forge templates before adoption.

Yes. There are fairly consistent "lightweight" design rules for how the inside of a table should look so it's easy to scan, especially in technical docs and datasheets.

### Headers and structure

- Give every column a clear, short heading; the leftmost "stub" column should also effectively label the row, even if its heading is omitted.
- Keep headings brief and parallel in wording (same grammatical pattern, similar length), and use the same style across all tables in the manual.
- Use one header row (possibly with grouped "spanner" headers) and then a clean body; don't stack lots of header rows unless absolutely necessary.
- If you have calculated/derived columns (e.g., percent, delta), put them to the right of the raw data they're derived from so the relationship is visually obvious.

Example header pattern for a register table:

```
Address    Name    Bits    Description
```

That's usually enough and is consistent from table to table.

### Borders, lines, and "lightweight" feel

- Prefer minimal rules: a line at the top, under the headers, and at the bottom; maybe one extra rule above totals or summary rows.
- Avoid vertical lines; spacing and alignment are usually enough to make columns readable and the page looks much lighter without them.
- Use thin, light rules (visually subtle) rather than thick gridlines so the data, not the frame, attracts the eye.
- If you need more guidance across rows, alternate row shading (very light gray) is widely recommended for readability but should be subtle.

In LaTeX, this matches booktabs style (`\toprule`, `\midrule`, `\bottomrule`) with no vertical bars.

### Alignment and spacing

- Left-align text columns, especially the stub (leftmost) column; left alignment is easier to read than centered text.
- Right-align numeric data related to magnitude (counts, voltages, times, sizes), and align on decimal points when precision matters so comparisons are easy.
- Keep consistent spacing between columns: enough room that columns don't visually merge, but no big gaps that make the table feel scattered.
- Choose column widths that fit content: narrow columns for short codes and flags, wider for descriptions; avoid forcing long prose into narrow columns that create ugly wrapping.

For a register map, a very readable pattern is: left-aligned Address/Name, centered or right-aligned bit fields, and a wide, left-aligned Description.

### Ordering and grouping of rows/columns

- Order rows in the way the reader will most likely look them up: by address, by signal name, or by functional group (e.g., timers together, GPIO together).
- Keep closely related fields adjacent in both rows and columns so comparisons are "down a column" rather than jumping around; numbers are easier to compare vertically than horizontally.
- For hierarchical row labels (e.g., "GPIO0" with sub-functions), use indentation in the stub column or an extra column rather than complicated cut-in headings.
- Put summary or total rows at the bottom and separate them with a rule or a subtle style change if they're aggregations.

### How the table starts and ends

- Start with a clear title and number (e.g., "Table 3–2. GPIO Control Registers") and put units in the column headers instead of repeating units in every cell where possible.
- Ensure that the table is "self-contained": the reader should understand what it shows without needing to read the surrounding text, aside from deep context.
- Put short explanatory notes or clarifications below the table (abbreviation expansions, special cases) instead of stuffing them into cell text.
- End with a clean bottom rule and any notes. Don't leave dangling extra blank rows or decorative junk; simplicity is what makes it feel light.

In LaTeX, that's typically:

```tex
\begin{table}
  \caption{GPIO control registers}
  \label{tab:gpio}
  \begin{tabular}{lllp{7cm}}
    \toprule
    Address & Name & Bits & Description \\
    \midrule
    ...
    \bottomrule
  \end{tabular}
  \begin{flushleft}
  \footnotesize Note. All registers are little-endian. Reserved bits must be written as 0.
  \end{flushleft}
\end{table}
```

### Consistency across the manual

- Use one consistent layout recipe for each table type (electrical specs, timing, registers, pin lists) so once the reader "learns" your pattern, every table is immediately legible.
- Keep font, size, and capitalization style consistent with the rest of the document; avoid mixing odd fonts or decorative effects in tables.
- Apply units, abbreviations, and symbol conventions uniformly (e.g., always "VDD", always °C, always "ms").

For a P2/P1-style hardware manual, I would normally define 3–4 table templates: "ElectricalCharacteristics," "Pinout," "RegisterMap," and "InstructionEncoding," each with fixed column order, alignment, and header naming.

> Offer from source: sketch these as specific LaTeX table macros (e.g.,
> `\begin{regtable}...\end{regtable}`) tuned for Propeller 2 register maps for mechanical reuse.

---

## Field-found defect — tall non-encoding tables silently clip (2026-07-08)

A concrete rendering defect surfaced while producing *The P2 Architect's Guide* v1.0.0 — a real
input for the table-layout analysis, and a platform bug to fix:

- **`p2kb-platform-tables.lua` routes a tall, non-encoding, multi-column table to a non-breaking
  `tblr`** (tabularray), which **silently clips** any rows past the page bottom — **no compile
  error, no warning**. It reads as "the table rendered fine" when rows are actually missing.
- **Seen on:** the Architect's Guide Appendix A 12-row terminology table (worked around by splitting
  it into two 6-row tables); the 5-row budget table was fine.
- **Fix:** in the filter's breakable-vs-non-breaking heuristic, route tall / non-encoding
  multi-column tables to **`longtblr`** (breakable) instead of `tblr`.
- **How to prove the fix:** add a fixture to the **layout torture test**
  (`workspace/p2-layout-torture-test/`) — a non-encoding multi-column table long enough to overflow
  one page (~20+ rows) — generate on the Forge, and confirm **every row appears** (overflow flows to
  the next page, not dropped).
- **Blast radius:** any manual with a long explanatory (non-register) table; silent, so it can ship
  missing content undetected.

---

## Collection complete — analysis pending

All four parts collected. **None of this is adopted guidance.** Next step is to study
these inputs against our own system (PDF Forge templates, Lua filters, existing manual
preambles and conventions) and decide — per item — what to adopt, adapt, or reject.

Pending offers from the source, to consider during analysis:
- A minimal tuned LaTeX template (Part 3 delivered a version of this).
- Specific LaTeX table macros (e.g., `\begin{regtable}`) for P2 register maps (Part 4).
