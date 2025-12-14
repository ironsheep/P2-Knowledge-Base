# Technical Debt - P2 Assembly Language Manual

Track improvement opportunities identified during development that we're intentionally deferring.

## Observations and Ideas

- [2025-12-09] Copyright and licensing needs review:
  - Current: CC BY-SA 4.0, "P2 Knowledge Base Project"
  - Repository uses MIT License with Parallax Inc. copyright
  - Documents should likely be dual copyright: Iron Sheep Productions, LLC and Parallax Inc.
  - Need to determine appropriate license for documentation (MIT vs CC BY-SA)
  - This affects all manuals, not just this one
- [Add new observations here with date]

## Deferred Improvements

- [2025-12-13] **Remove legacy diagram aliases in p2kb-pasm2-diagrams.sty**
  - Problem: Markdown uses old alias names that were preserved for backward compatibility
  - Current aliases: `EightCogOverviewDiagram`, `EggBeaterDiagram`
  - Should use canonical names: `EightCogEggbeaterDiagram`, `EggbeaterHubTimingDiagram`
  - Action: Search/replace in markdown, then remove aliases from .sty file
  - Estimated effort: 30 minutes

- [2025-12-12] **Internal links not visually distinct in PDF**
  - Problem: Hyperlinks within the document (instruction cross-references, TOC entries) work correctly but have no visual indicator (no blue color, no underline)
  - Cursor changes to hand pointer on hover, but there's no static visual cue
  - Attempted fixes that didn't work:
    - `colorlinks=true, linkcolor=blue` in hypersetup
    - `hidelinks=false` explicitly set
    - `\AtBeginDocument{\hypersetup{...}}` to force settings after Pandoc
  - Possible future approaches:
    - Use `pdfborderstyle={/S/U/W 0.5}` for underlined links
    - Define explicit RGB color instead of named `blue`
    - Investigate if Pandoc's PDF engine is overriding hyperref settings
    - Check PDF Forge's Pandoc configuration for conflicting options

---

*Created: 2025-12-09*
