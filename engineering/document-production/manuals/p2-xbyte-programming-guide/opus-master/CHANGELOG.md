# P2 XBYTE Programming Guide - Changelog

## v1.0.1 (2026-08-08)

A licensing change. No technical content changed — not a page of it.

- **License restored to CC BY-SA 4.0.** This guide is again licensed Creative Commons Attribution–ShareAlike 4.0 International, the license the community-review editions carried from 2025-12-09 through 2026-05-22. You may share and adapt it, including commercially, with attribution and under the same terms.
- **Why it changed back.** The CC BY-NC-ND terms it carried from 2026-06 went well beyond their intent. NonCommercial does not restrict resale — it restricts *all* commercial use, including a paid course referencing a chapter or a distributor bundling the PDF with a board. NoDerivatives blocked translations, excerpting, and community forks. The concern behind that change was only that someone might resell this as their own product.
- **Trademark, not copyright, addresses that concern.** The Trademarks note now states that the license grants permissions under copyright only: a reuser may copy, adapt, translate, and sell the text, but may not present the result as the official edition or imply endorsement.
- **Nothing was retroactively taken.** Creative Commons licenses are irrevocable, so every copy distributed under BY-SA stays BY-SA permanently.

## v1.0.0 (2026-07-20) — Initial release for community review

The P2 Interpreters & Emulators Guide: a guide to the Propeller 2's XBYTE
hardware bytecode engine — the skip family (SKIP/SKIPF/EXECF), the FIFO bytecode
stream, and LUT dispatch. It takes a reader from what the engine is and how it
dispatches each bytecode through to building on it: custom virtual machines,
and — where the engine fits the guest — CPU emulation, illustrated end to end.

Written in two registers, a warm teaching layer for the concepts and a precise
reference layer for the tables, encodings, and configuration bits, it
consolidates the P2 documentation, the knowledge base, and worked community code
into one source for readers building interpreters, custom VMs, or CPU emulators
on the P2.
