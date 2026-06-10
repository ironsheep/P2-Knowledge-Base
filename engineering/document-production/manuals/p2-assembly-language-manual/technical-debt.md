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

- [2026-06-10] **Full-audit deferrals + re-certification** (see `FULL-AUDIT-2026-06-10-REPORT.md`)
  - The 2026-06-10 full content audit applied 129 manual fixes and queued 72 KB
    defects (register F-026..F-097, `NEEDS-VERIFICATION`). Four manual findings
    were deferred because closing them needs runtime research and may change once
    the KB update lands:
    - **AF-144** (ch04 §4.6.1) — author a corrected, cycle-exact aligned-loop
      example for the new RDLONG 9–16 clock timing; reconcile the "X cycles / Nx
      hub period" prose.
    - **AF-147 / AF-141** (ch04 §4.2.3) — re-ground or retire the stale `2 / 8-23`
      hubexec-fetch notation example.
    - **AF-186** (appendix G) — author Silicon-Doc-accurate descriptions for the
      remaining `X_DACS` stereo rows.
    - **AF-191** (appendix H) — re-derive the master Spin2 reserved-word subtotal
      "586" against the enumerated sections (pre-existing latent defect; do not
      invent a total).
  - **Re-certification (blocking for PDF/release):** the audit ran in reverse
    (manual before KB). After the P2KB update sprint, re-certify the manual against
    the corrected KB — in particular the ~20 KB-only-anchored fixes listed in the
    report. No PDF until the 4 deferrals are closed AND the manual is re-certified.

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
