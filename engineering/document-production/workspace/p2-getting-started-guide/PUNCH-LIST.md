# Getting Started with the Propeller 2 — Punch List

Active-work register. Completed items are swept into the dated archive at the bottom at
each closeout; the list above carries only **outstanding** work.

---

## Outstanding

- _(none — v1.0.0 released 2026-06-24, initial Community Review Edition)_

---

## Archive

### v1.0.0 released 2026-06-24 (initial Community Review Edition)

- [x] **Three figures** present and verified (Chapter 1): the P2-Edge-on-Breakout photo
      (`\screenshotfig`, keyline framed), the eight-cogs-around-the-hub diagram
      (`\EightCogSimpleDiagram`), and the memory-hierarchy diagram
      (`\CogHubRelationshipDiagram`) — both diagrams reused verbatim from the Assembly manual.
- [x] **Tip asides** render as platform-styled `::: tip` callout boxes (no raw-emoji glyph drop).
- [x] **Chapter headings** carry the `Chapter N:` convention (no auto-number; platform `secnumdepth=-1`).
- [x] **Release-gate audited** (YAML-HEAD drain GREEN) **+ finalized**; production PDF verified
      25 pp, clean compile log; four runnable Spin2 examples compile clean (`pnut-ts`).

> **Origin.** Split 2026-06-24 from the *P2 Architect's Guide* first draft. The draft's
> Ch4 / appendix figures (the temporal↔spatial spectrum and robot-decomposition diagrams),
> the emoji-marker style decision, and the platform tall-table overflow issue all moved with
> the functional-decomposition content to the design book, *The P2 Architect's Guide* — they
> do not apply to this orientation book. (The tall-table platform bug is tracked under
> `project_manual_layout_standards`.)
