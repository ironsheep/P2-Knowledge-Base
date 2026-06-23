# P1 — Knowledge Gaps & Questions-for-Experts (Moving Ledger)

> The P1 (Propeller 1) gap ledger — standalone, parallel to the P2 `KNOWLEDGE-GAPS.md`. Stood up 2026-06-22
> (P1 bootstrap). Namespaced IDs: **`G-P1-NNN`** (gaps) · **`Q-P1-NNN`** (expert questions). The P1 dashboard
> rolls up the open-question count from here.
>
> **Bootstrap note (charter §6):** this corpus starts empty. The **first** source (the P1 Propeller Manual)
> only *raises* questions — there is nothing prior to answer. That is expected, not the "zero-answered =
> exception to justify" defect the mature-corpus rule flags.

## Part A — Gap-evolution ledger
**Next ID: `G-P1-008`** — seeded 2026-06-22 by the backbone ingestion (P1 Propeller Manual v1.2). Per
charter §6, doc #1 only *raises* gaps; each is fillable by another golden P1 source (not designer-only).

| # | Domain | The gap (question / missing fact) | Status | Filled by (source @ edition) | Opened | Closed |
|---|--------|-----------------------------------|--------|------------------------------|--------|--------|
| G-P1-001 | PASM1 | Per-instruction cycle timing + opcode encodings. **LARGELY ANSWERED 2026-06-22:** the Instruction Master Table (with full encoding columns + Clocks) **is captured in the v1.2 layout text pp253–256** (camelot mislabeled it, `pdf-layout` got it); the errata pins hub instrs = **8..23**, WAITCNT/WAITPEQ/WAITPNE = **6+**, WAITVID = **4+** (Note 5: 4 itself, 7/6 for frame handoff). Remaining = structured per-instruction parse (YAML build step). | NARROWED | v1.2 master table (layout text) + errata v1.1 | 2026-06-22 | — |
| G-P1-002 | Hardware/electrical | DC characteristics, absolute maximums, ESD, detailed timing parameters. The Manual gives functional specs only (Table 1-2). | OPEN | P1 Datasheet v1.4 (queued) | 2026-06-22 | — |
| G-P1-003 | Boot | Boot Loader host **serial download/handshake protocol** on P30/P31. Manual describes the boot *sequence* (p18) but not the wire protocol. | OPEN | Parallax app notes / datasheet / community | 2026-06-22 | — |
| G-P1-004 | Spin1 | Spin **bytecode / interpreter internals** — not documented (interpreter ships in ROM). Likely permanently community-only. | OPEN | community / reverse-engineering (out of golden scope) | 2026-06-22 | — |
| G-P1-005 | ROM tables | Exact **sine / log / anti-log** table values + the usage transformations. Manual points to Appendix B (p380); verify the numeric-table extraction. | OPEN | P1 Manual Appendix B (camelot numeric extract) | 2026-06-22 | — |
| G-P1-006 | Architecture | INB/OUTB/DIRB are marked "**reserved for future use**" (Table 1-3) — P1 has no Port B. Historical: what was intended, and how it relates to P2's eventual 64-pin design. | OPEN | P1→P2 lineage / Chip Gracey (low priority) | 2026-06-22 | — |
| G-P1-007 | Pedagogy / source | **The "Propeller Programming Tutorial" is a missing P1 source.** The P1 Manual is explicitly a *reference* (p338, p745) and points the language tutorial OUT to the **Propeller Tool's on-line help** ("Propeller Programming Tutorial" + "Spin Language Tutorial") — which we have **not** ingested (only the deSilva P1 tutorial is in our P1 sources). This is the P1 ecosystem's from-zero language-orientation doc; surfaced 2026-06-23 while building the P2 Architect's Guide Ch2 ("Reading P2 Code"), whose role parallels it. | OPEN | Propeller Tool on-line help (Parallax) / IDE help export | 2026-06-23 | — |

## Part B — Questions for experts (answerable only by the designer/community)
**Next ID: `Q-P1-001`** (none yet).

**Who-to-ask routing:** P1 silicon/semantics → **Chip Gracey** (P1 designer); P1 idiom/pedagogy → P1 community
(deSilva, Parallax forums). 

| # | The question | Who to ask | Opened | Status |
|---|--------------|-----------|--------|--------|
| _(empty)_ | | | | |
