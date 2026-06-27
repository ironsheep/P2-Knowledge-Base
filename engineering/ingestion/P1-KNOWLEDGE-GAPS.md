# P1 — Knowledge Gaps & Questions-for-Experts (Moving Ledger)

> The P1 (Propeller 1) gap ledger — standalone, parallel to the P2 `KNOWLEDGE-GAPS.md`. Stood up 2026-06-22
> (P1 bootstrap). Namespaced IDs: **`G-P1-NNN`** (gaps) · **`Q-P1-NNN`** (expert questions). The P1 dashboard
> rolls up the open-question count from here.
>
> **Bootstrap note (charter §6):** this corpus starts empty. The **first** source (the P1 Propeller Manual)
> only *raises* questions — there is nothing prior to answer. That is expected, not the "zero-answered =
> exception to justify" defect the mature-corpus rule flags.

## Part A — Gap-evolution ledger
**Next ID: `G-P1-012`** — seeded 2026-06-22 by the backbone ingestion (P1 Propeller Manual v1.2); G-P1-008..011 added 2026-06-27 by the app-notes wave. Per
charter §6, doc #1 only *raises* gaps; each is fillable by another golden P1 source (not designer-only).

| # | Domain | The gap (question / missing fact) | Status | Filled by (source @ edition) | Opened | Closed |
|---|--------|-----------------------------------|--------|------------------------------|--------|--------|
| G-P1-001 | PASM1 | Per-instruction cycle timing + opcode encodings. **LARGELY ANSWERED 2026-06-22:** the Instruction Master Table (with full encoding columns + Clocks) **is captured in the v1.2 layout text pp253–256** (camelot mislabeled it, `pdf-layout` got it); the errata pins hub instrs = **8..23**, WAITCNT/WAITPEQ/WAITPNE = **6+**, WAITVID = **4+** (Note 5: 4 itself, 7/6 for frame handoff). Remaining = structured per-instruction parse (YAML build step). | NARROWED | v1.2 master table (layout text) + errata v1.1 | 2026-06-22 | — |
| G-P1-002 | Hardware/electrical | DC characteristics, absolute maximums, ESD, detailed timing parameters. The Manual gives functional specs only (Table 1-2). | OPEN | P1 Datasheet v1.4 (queued) | 2026-06-22 | — |
| G-P1-003 | Boot | Boot Loader host **serial download/handshake protocol** on P30/P31. Manual describes the boot *sequence* (p18) but not the wire protocol. | OPEN | Parallax app notes / datasheet / community | 2026-06-22 | — |
| G-P1-004 | Spin1 | Spin **bytecode / interpreter internals** — not documented (interpreter ships in ROM). Likely permanently community-only. | OPEN | community / reverse-engineering (out of golden scope) | 2026-06-22 | — |
| G-P1-005 | ROM tables | Exact **sine / log / anti-log** table values + the usage transformations. Manual points to Appendix B (p380); verify the numeric-table extraction. | OPEN | P1 Manual Appendix B (camelot numeric extract) | 2026-06-22 | — |
| G-P1-006 | Architecture | INB/OUTB/DIRB are marked "**reserved for future use**" (Table 1-3) — P1 has no Port B. Historical: what was intended, and how it relates to P2's eventual 64-pin design. | OPEN | P1→P2 lineage / Chip Gracey (low priority) | 2026-06-22 | — |
| G-P1-007 | Pedagogy / source | **The "Propeller Programming Tutorial" is a missing P1 source — an EDITION-LOSS.** It was **Chapter 3 of Propeller Manual v1.0/v1.01** (2006, ISBN 1-928982-38-7; v1.0 also had Ch2 "Using the Propeller Tool"). By **v1.2** (our ingested copy, ISBN 978-1-928982-59-3) Parallax **moved both chapters out to the Propeller Tool's on-line help** and renumbered — so our copy's Ch3 is the Assembly Reference and carries only a *pointer* (p36/p338/p745) to the tutorial. We never had v1.0/v1.01. This is the P1 ecosystem's from-zero language-orientation doc; surfaced 2026-06-23 (Stephen's v1.0 hardcopy) while building the P2 Architect's Guide Ch2 ("Reading P2 Code"), whose role parallels it. **Recoverable:** v1.01 PDF archived at nagasm.org/ASL/Propeller/20080303/WebPM-v101.pdf and archive.org/details/manuallib-id-2594235. | OPEN — obtainable | Propeller Manual **v1.01** (archived PDF) — ingest the "Propeller Programming Tutorial" chapter | 2026-06-23 | — |
| G-P1-008 | P1 library / driver objects | The app-note code reuses **stock Propeller-Tool / OBEX driver objects** not yet inventoried in the KB: `VGA_HiRes_Text_010`, `Keyboard_011`, `Mouse_011`, `WMF_Framework_010` (AN004 + AN013), `NS_sound_drv`, `pwmAsm_010` (AN013); AN001 references `VGA_Text.spin` + `CTR.spin` **not shipped** in its archive. Capture this shared P1 driver/library set as its own ingestion. | OPEN | P1 library-objects ingestion / Propeller Tool library / OBEX | 2026-06-27 | — |
| G-P1-009 | P1 GUI framework (WMF) | The **Window Manager Framework** — a substantial P1 text-mode windowing system (data-driven menus/buttons, event queue, handler routing) documented across the **GUI & Graphics Series** (AN004 foundation · AN005 intro-menus *not yet on disk* · AN013 advanced menus) — has **no current KB representation**. The architecture is silicon-agnostic and the durable, recreation-worthy value of these notes. | OPEN | AN004/AN013 (ingested) + AN005 (pending) | 2026-06-27 | — |
| G-P1-010 | P1 video generation | The **P1 per-cog video generator** (`WAITVID`/`VCFG`/`VSCL` + counter-driven pixel clocking) underpins AN004 + AN013 and is the `%00001` mode AN001 calls "beyond scope" — no KB note characterizes it. High-value P1→P2 contrast (P2 has **no** video generator → the streamer replaces it). | OPEN | P1 Manual video chapter / P1 datasheet | 2026-06-27 | — |
| G-P1-011 | Spin1 / PASM1 semantics | Language/arch details the app notes lean on but the P1 ledger doesn't yet carry: the Spin1 **`?` LFSR pseudo-random operator** (AN004); **`JMPRET` + the 4-stage pipeline** read-before-write that underpins all P1 self-modifying-code idioms, and the **C/Z flag-preservation idioms** across cooperative switches (AN014 `muxnz`/`muxc`/`test #0-0`). | OPEN | P1 Manual (Spin/PASM reference) + AN014 | 2026-06-27 | — |

## Part B — Questions for experts (answerable only by the designer/community)
**Next ID: `Q-P1-004`** — Q-P1-001..003 added 2026-06-27 by the app-notes wave.

**Who-to-ask routing:** P1 silicon/semantics → **Chip Gracey** (P1 designer); P1 idiom/pedagogy → P1 community
(deSilva, Parallax forums). 

| # | The question | Who to ask | Opened | Status |
|---|--------------|-----------|--------|--------|
| Q-P1-001 | Is the **Window Manager Framework** (WMF text-mode GUI, LaMothe) still distributed/maintained by Parallax, or archival-only? (Affects whether it's worth anchoring a P2 GUI-framework port-reference on.) | Parallax | 2026-06-27 | open |
| Q-P1-002 | Which OBEX revisions of the shared P1 drivers (`VGA_HiRes_Text`, `Keyboard`, `Mouse`) are **canonical** to anchor P1 video/IO documentation on? (AN004/AN013 ship `*_010`/`*_011`.) | Parallax / P1 community | 2026-06-27 | open |
| Q-P1-003 | AN001 counter detail: exact **double-buffered APIN latch timing** for edge-detect modes, and the quantitative **PLL de-jitter** bound — hardware specifics the note states qualitatively but does not quantify. | Chip Gracey | 2026-06-27 | open |
