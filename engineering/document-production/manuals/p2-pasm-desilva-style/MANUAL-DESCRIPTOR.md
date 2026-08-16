---
manual_slug: p2-pasm-desilva-style
doc_class: tutorial                               # deSilva teaching voice — tutorial voice IS permitted (Dimension #9)
code_line_budget_K: 76                            # platform-inherited (creation-guide "Code Line Budget"); LM-Mono calibrated
last_published_tag: p2-pasm-desilva-style-v3.0.1  # baseline for Dimension #15 (PDF dated 2026-06-25, 162pp)
guide_paths:
  creation_guide: ./creation-guide.md
  voice_guide: ./voice-guide.md                   # thin per-document guide: ADOPT/ADAPT/REJECT against house rules R1-R4 (added 2026-08-15); voice rationale in ./why-desilva-voice-works.md
  style_guide: ./desilva-style-guide.md
authoritative_sources: see ./creation-guide.md    # canonical source list + Content Verification Protocol live there
source_highlights:
  - deliverables/ai/P2/language/pasm2/             # primary derived YAML (instruction behavior / flags / clocks)
  - deliverables/ai/P2/language/spin2/             # Spin2 interop used in examples
  - engineering/ingestion/sources/silicon-doc/     # silicon truth (architecture / cog memory / egg-beater)
  - engineering/ingestion/external-sources/hardware-verification/   # empirical ledger (smart-pin ordering, etc.)
  - pnut-ts                                        # compiler validation (use -d for any DEBUG-window code)
high_risk_tables:
  - "SKIP / SKIPF bit-order table (LSB-first) — historically inverted, fixed in the v3.0.0 re-audit"
  - "Smart-pin mode / recipe table (Ch 14) — DIRH-before-WYPIN ordering (v3.0.1 fix)"
  - "Instruction summary / flag tables embedded in chapter prose"
fragile_areas:
  - "Ch 2 'Cog Anatomy 101' — the `\\CogAnatomyDiagram` image was repaired in v3.0.1 ('Each Cog Contains:' / 'Cog RAM'); egg-beater diagram fixed in v3.0.0. Re-verify the diagram still reads as a P2 part each render."
  - "Smart-pin recipe (Ch 14) — enable pin (DIRH) before writing Y (WYPIN); the one ordering correct for every mode (v3.0.1)"
  - "LOCKTRY spin-locks — correct carry polarity on retry (two were inverted pre-v3.0.0)"
  - "SETSE edge/level modes — a fabricated edge mode was removed in v3.0.0; re-verify against silicon"
  - "Built-in code examples — ALL examples pnut-ts compile-certified in v3.0.1 (use -d for DEBUG blocks); re-certify against the current compiler every release"
---

# DeSilva PASM2 Tutorial — Manual Descriptor

Thin per-manual overlay read by `document-audit` (and, going forward, `prepare-manual` /
`release-manual` / `document-finalize`). Everything not listed in the front matter is inherited
from the central `document-audit` skill body + the guides referenced above.

**Doc-class note:** `tutorial` (deSilva-style). Factual dimensions (A, B, #1, #5, C) still verify
against the reference KB read from disk under `deliverables/ai/P2/language/` (not `p2kb-mcp`, which
serves the lagging published index) and P2 Documentation v35 for architecture claims. **Dimension #9
permits tutorial voice** — the deSilva voice (encouragement, "Your Turn", Medicine Cabinet,
celebration moments) is intentional per `./desilva-style-guide.md` and is NOT a finding.

**Unreleased efforts since `last_published_tag`** (the changeset-integrity baseline, Dimension #15):
**none** — `last_published_tag` is `v3.0.1` (released 2026-06-25), which shipped the smart-pin Ch 14
ordering refresh, the Plex / glyph-fallback typography pass on the current platform, the data-set-wide
KB accuracy corrections (CORDIC / COGINIT / LSTRING, KB v1.11.2), and both former v3.0.0
DEFERRED-REQUIRED items (the `\CogAnatomyDiagram` repair + the pnut-ts compile-cert of all examples).
The baseline is current; the next audit measures the changeset from v3.0.1 forward.
