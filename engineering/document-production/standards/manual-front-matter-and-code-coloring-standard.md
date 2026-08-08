# Manual Publication Standard: Front Matter & Code Coloring

**Status:** Standard — applies to every manual we produce under `engineering/document-production/manuals/`.
**Established:** 2026-05-31 (codifying the consistent pattern already used by the Assembly Language, Smart Pins, IOSP, and Single-Step Debugger manuals).

This document defines two house conventions that **every** P2 manual must follow so the published set looks like one family: the **front matter** (cover + organization + copyright) and the **code-block coloring** scheme.

---

## 1. Front Matter

The front matter lives in the manual's `opus-master/front-matter.md` and is **prepended to the body** at assembly time (so it flows through Pandoc + the template, not hardcoded in the `.latex`). The template's `\begin{document}` is followed only by `$body$` — it must **not** contain a hardcoded `\begin{titlepage}`.

### Required structure (in order)

1. **Banner image** — the Parallax-approved cover art, `book-artwork.png`, full width inside a drop-shadow `tcolorbox`:
   ```latex
   \begin{tcolorbox}[enhanced, boxrule=1.5pt, colframe=gray!60, colback=white,
     drop shadow southeast, shadow={3pt}{-3pt}{1mm}{black!15},
     left=0pt,right=0pt,top=0pt,bottom=0pt, width=\textwidth, arc=0pt, outer arc=0pt]
   \includegraphics[width=\linewidth]{inbox/assets/book-artwork.png}
   \end{tcolorbox}
   ```
   The **same** `book-artwork.png` is used by every manual. Copy it into the manual's `workspace/<slug>/assets/` and stage it to `outbound/<slug>/assets/`.

2. **Centered title block** — title at `\fontsize{36}{42}\bfseries`, subtitle `\Large\itshape`, then date `\large`, then `{\large\color{blue}Version N.M}`.

3. **Organization panel** — a light-gray `tcolorbox` titled **"Manual Organization"** (or "User Guide Organization"), containing a one-line tagline and **two `minipage` columns** listing the chapters/parts. (Uses `enumitem` itemize options `leftmargin=*, itemsep=1pt, topsep=2pt`.)

4. **Publisher lines** — `{\small Iron Sheep Productions, LLC}` and `{\small P2 Knowledge Base Project}`, centered.

5. **`\clearpage \pagestyle{fancy}`**, then **`\tableofcontents \clearpage`**. Add **`\listoffigures \clearpage`** *only if the manual actually contains figures* (omit it for figure-free manuals to avoid an empty page).

6. **Copyright & License** (markdown `# Copyright and License`): `Copyright © <year> Iron Sheep Productions, LLC and Parallax Inc.`, the **CC BY-SA 4.0** statement, a **Trademarks** note (`Parallax, Propeller, Spin, and the Parallax logo are trademarks of Parallax Inc.`) carrying the trademark-scope sentence, and optional **Acknowledgments**.
   **Copy the block verbatim from `engineering/standards/LICENSING-DECISION.md` §5.1** — that record is authoritative and this entry defers to it. (This standard already specified BY-SA when 17 documents were flipped to BY-NC-ND around it in 2026-06; nothing checked the documents against it, so the drift shipped for two months. `engineering/tools/validation/audit-license-block.py` is now that check.)

7. Close with a `{=latex} \clearpage`.

### Template-package requirements (in the manual's foundation `.sty`)

`tcolorbox` + `\tcbuselibrary{skins,breakable}` (banner drop shadow), `fancyhdr` (`\pagestyle{fancy}`), `enumitem` (organization-panel itemize), `xcolor` (the blue version line). `\fontsize`, `\tableofcontents`, `\listoffigures` are core.

Reference implementations: `manuals/p2-single-step-debugger-manual/opus-master/front-matter.md` and `manuals/p2-io-and-smart-pins-user-guide/opus-master/front-matter.md`.

---

## 2. Code-Block Coloring

The shared, **IDE-aligned** scheme — identical across Assembly Language, Smart Pins, IOSP, and Single-Step Debugger:

| Language | Background | Border | HTML |
|----------|-----------|--------|------|
| **Spin2** | light **blue** | blue | bg `E3F2FD`, border `1976D2` |
| **PASM2 / assembly** | light **green** | green | bg `EBFCEB`, border `4CB04C` |

(Some manuals add `antipattern` = soft pink `FFF5F5`/`C08080` where they teach anti-patterns.)

### Mechanism

Two interchangeable wirings exist; **use the one that matches the manual's code style**:

- **Fenced code blocks** (```` ```spin2 ````, ```` ```pasm2 ````) — a `CodeBlock` Lua filter maps the language class to a colored `tcolorbox` wrapping a `fancyvrb` `Verbatim` (preserves blank lines and special characters; bypasses `--listings`). This is the Single-Step Debugger / Debug Window model.
- **Fenced divs** (`::: spin2`, `::: pasm2`, `::: antipattern`) — a `Div` filter does the same for div-wrapped blocks. This is the Smart Pins model.

Both produce the **same** `Spin2Block` / `Pasm2Block` (`PASM2Block`) `tcolorbox` environments — a **thick 4pt left rule** (the left-edge accent), thin `0.5pt` other sides, rounded corners, and `left=30pt` to clear the inset line numbers:
```latex
\newtcolorbox{Spin2Block}{colback=<spin2-bg>, colframe=<spin2-border>,
  boxrule=2pt, leftrule=4pt, rightrule=0.5pt, toprule=0.5pt, bottomrule=0.5pt,
  rounded corners, left=30pt, right=10pt, top=8pt, bottom=8pt,
  before skip=15pt, after skip=15pt, breakable}
```
**Line numbering is required** (it is part of the house look): the filter must emit the code inside `\begin{Verbatim}[numbers=left,numbersep=8pt,xleftmargin=-10pt]` (fenced-block model) or the equivalent `lstlisting[numbers=left,numbersep=8pt,xleftmargin=-10pt,...]` (div model). The `left=30pt` box inset plus the `xleftmargin=-10pt` pulls the numbers into the left gutter. Omit these and the blocks have no left-edge accent and no line numbers, and will not match the other manuals.

### Wiring checklist

1. Content `.sty`: define the four colors above + `Spin2Block` / `Pasm2Block` `tcolorbox`es. Ensure `fancyvrb` is loaded (foundation usually does).
2. Add the `*-code-coloring.lua` filter to the manual's `filters/`.
3. List it in `request.json` `lua_filters`.

Reference: `workspace/p2-single-step-debugger-manual/filters/p2kb-ssdbg-code-coloring.lua` (+ `templates/p2kb-ssdbg-content.sty`) for the fenced-block model; `workspace/p2-smart-pins-tutorial/filters/p2kb-sp-code-coloring.lua` for the div model.

---

*Apply both sections to every new manual at workspace-setup time. When a manual diverges, bring it back to this standard rather than inventing a new look.*
