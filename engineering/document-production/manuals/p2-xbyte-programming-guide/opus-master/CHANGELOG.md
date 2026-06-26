# P2 XBYTE Programming Guide - Changelog

## v0.1.0 (2026-06-26)

First draft — initial review build. Stands up the manual on the shared `p2kb-platform-*`
stack, modeled on the P2 Streamer Programming Guide (layout, two-register voice, richness).
Authored ground-up and grounded in the Silicon Doc v35 XBYTE section + the KB YAML
(`xbyte_engine.yaml` and the skip/FIFO/SETQ instruction set). NOT yet released.

- **Part I — XBYTE Fundamentals** — Understanding XBYTE (the bytecode VM inner loop in
  hardware); the skip family (SKIP / SKIPF / EXECF) taught first as the foundation XBYTE is
  built from; the FIFO bytecode stream (RDFAST + RFBYTE/RFWORD/RFLONG/RFVAR/RFVARS, GETPTR);
  LUT dispatch (the 256-entry table, each entry an EXECF operand).
- **Part II — The XBYTE Engine** — the 8-clock dispatch cycle walked clock-by-clock and the
  6-clock overhead; arming with SETQ / SETQ2 (persistent vs one-shot) and the `$1FF` stack
  convention; the table-size & compression modes (256/128/64/32/16, `%ABBBB`) and the F bit;
  bytecode-routine constraints and shared-handler skip patterns.
- **Part III — Building a VM** — a minimal custom VM (the auto-XBYTE loop from scratch); how
  guest CPU instruction shapes map onto XBYTE; a tiny illustrative 6502 emulator (capstone);
  the 6809 SETQ2 alternate-table vignette.
- **Part IV — Reference** — the instruction reference and the configuration-constants /
  mode-operand reference.
- **Appendices** — A: XBYTE Quick Reference · B: Encoding Summary · C: Further Implementations
  (community projects, external links only) · D: Troubleshooting · clickable Index.
- **Figures** — four TikZ diagrams on the shared platform diagram stack: the dispatch loop
  (Fig 1.1), the LUT dispatch-table entry bit-field (Fig 4.1), the 8-clock dispatch cycle
  (Fig 5.1), and the mode-operand layout (Fig 7.1), with a List of Figures.

Known first-draft limits (for the review): the example-library ZIP is not yet built; the
capstone 6502 and the 6809 vignette are deliberately tiny & illustrative, not faithful
emulators.
