---
manual_slug: p2-single-step-debugger-manual
doc_class: behavior                               # documents the on-chip debugger's behavior — grounds against the debugger implementation + hardware, NOT language YAML
code_line_budget_K: 76                            # platform-inherited reference K (creation-guide.md §5b); this manual consumes the platform code boxes unchanged
last_published_tag:                               # none — v1.0.0 is the initial release
guide_paths:
  creation_guide: ./creation-guide.md
  voice_guide: ./voice-guide.md
  style_guide: ./voice-guide.md                   # no separate style-guide; voice-guide.md carries voice + style conformance
authoritative_sources: see ./creation-guide.md
source_highlights:
  - ./REF-NO-COMMIT/SINGLE-STEP-DEBUGGER-MANUAL-SOURCE.md   # PRIMARY — the full interaction set (keys, Ctrl combinations, per-region clicks, wheel tiers), derived from the PNut v55 Pascal source (DebuggerUnit.pas, v55 parity baseline). SOURCE ONLY — never shipped, never cited in the manual.
  - ./REF-NO-COMMIT/SingleStep-Debugger-Interactive-Test-Plan.md  # the Tests 0-14 hardware walk that confirmed the above on real silicon
  - ./REF/SingleStep-Debugger-Operation-Guide-and-Audit.md  # mechanism reference (debug ISR, stall/go, serial exchange) + the audit that drove the blend
  - ./screenshots/                                # the eleven captures behind Chapter 3's region tour; ssdb-fullScreen.png is the whole-window reference
high_risk_tables:
  - "Chapter 5 keyboard table — Space / Enter / B / D / I / M / R / arrows / PgUp / PgDn. Each row is a live command; a wrong row misdrives the reader's debugger."
  - "Chapter 5 Ctrl-combination table — exactly five combinations reach hub navigation (Ctrl+C/D/K/L/M); every other Ctrl combination does nothing. Do not let this table grow by inference."
  - "Chapter 5 click tables (Running the program / Looking at something) — 16 regions with left and right stated separately. Left and right differ in most rows and the difference is the whole point in several."
  - "Chapter 5 wheel-tier table — four tiers across three columns (disassembly cog, disassembly hub, hub data). The hub-data column is NOT monotonic (16 / 1 / 4 / 128); a 'tidied' ordering would be wrong."
  - "Chapter 3 region tour — the per-region Mouse and Keys columns must not contradict Chapter 5. Chapter 3 teaches where controls live; Chapter 5 is the complete set. Any interaction correction lands in BOTH."
  - "Appendix A feature-availability-by-version table — version gating; verify against the Spin2 language-version record, not against memory."
fragile_areas:
  - "Chapter 3 vs Chapter 5 are deliberately redundant, not duplicated. Chapter 3 = regions and what they are for; Chapter 5 = the complete lookup set. Never 'deduplicate' one into the other — the split is the pedagogy."
  - "Ctrl+D is hub-scroll-down, NOT the DEBUG toggle. This is the manual's ::: caution and the single most misleading thing about the key set. Keep the caution wherever the D key is taught."
  - "Argument-less DEBUG is what opens the single-step debugger. A DEBUG with arguments is display/terminal output. Conflating them breaks Chapters 2, 4, and 9 at once."
  - "The nine DEBUG display windows are CROSS-REFERENCED to the P2 Debug Window Manual, never taught here (creation-guide §5). Chapter 9 is a pointer chapter; resist growing it."
  - "Tool names — compiler is pnut-ts (built with -d, or DEBUG is stripped); host is pnut-term-ts. There is no PNut IDE and no pnut.exe in this manual; both source blends are PNut-IDE-flavored and that flavor must not leak back in."
  - "P1-isms from the source blends: cognew -> COGSPIN/COGINIT, CNT -> GETCT. The manual names the P1->P2 bridge once, deliberately; do not add an architecture refresher."
  - "Timing claims — do not measure across a DEBUG statement (the cog waits for the serial TX to finish) and do not measure by stepping. Chapter 8 states both; keep them together."
  - "AUGS/AUGD atomicity — one Space can advance two instructions when the first is a ## prefix. This reads as a stuck key; the troubleshooting row explaining it is load-bearing."
  - "Release gate: co-releases with the PNut-Term-TS User Guide, timed to PNut-Term-TS v1.0."
---

# P2 Single-Step Debugger Manual — Descriptor

Thin per-manual overlay read by `document-audit` (and `prepare-manual` /
`release-manual` / `document-finalize`). Everything not listed in the front
matter is inherited from the central skill bodies + the guides referenced above.

**Grounding-model note:** `doc_class: behavior`. The subject is the P2's built-in
single-step debugger — a piece of shipped firmware plus its host-side display, not
a silicon or language feature. Factual dimensions verify against the **debugger's
own implementation** (captured in the `REF-NO-COMMIT/` source feed, derived from
the PNut v55 Pascal baseline) and against the **Tests 0–14 hardware walk**, *not*
against `deliverables/ai/P2/language/`. Where an interaction and any prose
disagree, **the debugger is ground truth.**

The manual does make a handful of ordinary P2 claims in passing (`GETCT`,
`COGSPIN`, C/Z flags, smart pins, events). Those *are* language/silicon claims and
verify normally against the KB.

**Source-file note (read before "cleaning up" this folder).** Two files sit at the
manual root and look like abandoned drafts. They are not — `creation-guide.md` §2
names both as the **pre-blend source inputs** the Opus Master was built from:

| File | Role |
|------|------|
| `current-document.md` | the SHAPE — narrative arc, Quick Start, version-history appendix. Tutorial-shaped; self-dates "August 2025, Target SPIN2 v51+", which is what makes it look stale. |
| `DEBUGGER-USER-MANUAL.md` | what we TEACH — the interaction model, ported unchanged from the classic debugger. |

Note that `REF/DEBUGGER-USER-MANUAL.md` is a **different, later document** with the
same filename (region-oriented, mechanism-accurate; the root copy is
feature-oriented). Neither supersedes the other cleanly and neither is the master —
the Opus Master is the blend. Keep both; cite neither.

**Baseline note:** `last_published_tag` is empty. v1.0.0 is the **initial**
release, so audits have no prior published baseline to diff against — the
changeset-integrity (delta-since-last-published) gate does not apply, and the
CHANGELOG entry follows the initial-release form in
`methodology/changelog-style-guide.md` (a description of the document, not a delta).
