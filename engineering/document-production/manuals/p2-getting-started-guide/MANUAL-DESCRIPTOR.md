---
manual_slug: p2-getting-started-guide
doc_class: reference          # orientation DISTILLATION — facts must trace to the KB (no hallucination/voice pass); see note below
code_line_budget_K: 76        # creation-guide.md §7 "Max code columns (K): 76"
last_published_tag: p2-getting-started-guide-v1.0.3   # baseline for Dimension #15 (released 2026-08-08, 25pp)
guide_paths:
  creation_guide: ./creation-guide.md
  voice_guide: ./voice-guide.md
  style_guide: ./voice-guide.md   # no separate style-guide; terminology/style rules live in the voice-guide
authoritative_sources: see ./creation-guide.md
high_risk_tables: []            # the book carries no transposition-prone data tables (only the cover org panel)
fragile_areas:
  - "Split seams — forward-references to the removed Chapter 4 / decomposition (split out 2026-06-24 to the design book). The 2026-06-24 release-gate found 2 dangling 'Chapter 4 / final chapter' refs here; weight Dimension #2 heavily on any prose that promises later content."
  - "Figure captions — the parenthetical quantitative asides (e.g. memory-tier access cycles) overspecify; verify each number against the architecture YAML (Dimension #5)."
---

# Getting Started with the Propeller 2 — Descriptor

Thin per-manual overlay read by `document-audit` (and `prepare-manual` / `release-manual` /
`document-finalize`). Everything not listed in the front-matter is inherited from the central
skill body + the guides above.

**doc_class note.** This is an **orientation distillation**, not an instruction reference — but it
is classed `reference` *for grounding rigor*: every architectural/language fact must trace to the
KB YAML (Ch1 → `deliverables/ai/P2/architecture/`; Ch2-3 → `deliverables/ai/P2/language/` + the
Spin2 v55 doc), and it gets **no** tutorial-voice hallucination pass. The warm mentor voice is
governed by `voice-guide.md` (Dimensions #8/#9), not by the doc_class. Coverage is **deliberately
non-exhaustive** — the book orients then links OUT to the reference manuals — so "doesn't cover X
exhaustively" is by design, never a Dimension-C coverage finding.

**Origin.** Split 2026-06-24 from the 4-chapter *P2 Architect's Guide* first draft; this is the
orientation half (Ch1 Meet the Propeller 2 · Ch2 Reading P2 Code · Ch3 Putting It to Work + Where
to Next). Functional decomposition + appendices + glossary moved to the sibling design book
*The P2 Architect's Guide* (`../p2-architect-guide/`).
