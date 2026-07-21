---
manual_slug: p2-architect-guide
doc_class: reference            # narrative DESIGN/METHOD book — classed reference for grounding rigor (no hallucination/voice pass); see note below
code_line_budget_K: 76          # platform reference K; the book carries ZERO code by design (voice-guide §4) — budget applies only if a future snippet is ever added
last_published_tag: p2-architect-guide-v1.0.1   # baseline for Dimension #15 (advanced at the v1.0.1 release, 2026-07-12)
guide_paths:
  creation_guide: ./creation-guide.md
  voice_guide: ./voice-guide.md
  style_guide: ./voice-guide.md  # no separate style-guide; terminology/format rules live in the voice-guide (§4)
authoritative_sources: see ./creation-guide.md
high_risk_tables: []            # no transposition-prone data tables; the only tables are Appendix A's space/time + FPGA-terminology tables (prose-grade, see fragile_areas)
high_risk_quant:                # Dimension #5 hot spots — few, this is a method book not a spec
  - "The '12 real projects' provenance figure (Parts I & III are distilled from them) — keep the count honest to the source"
  - "PSRAM vs on-chip LUT RAM / CORDIC / streamer distinction (v1.0.1 accuracy fix) — PSRAM is an EXTERNAL resource; never let the design prose imply it is on-chip"
fragile_areas:                  # known load-bearing / historically-sensitive — weight heavily
  - "Anti-prescription (voice-guide §2.4, LOAD-BEARING) — any Part II sentence that reads as a design rule out of context is a defect; the two worked derivations (walking robot · streaming pipeline) must each be framed as 'one application's answer,' never a template. This is the book's central discipline; weight Dimension #9 heavily here."
  - "Cadence / recognizably-AI voice (voice-guide §2.6) — pure narrative argument with no code/tables to break rhythm makes this the FLEET'S HIGHEST-RISK document for metronomic closing beats. Protect the declared refrains ('Carry the method, never the map') and the earned §5.5 'So go build something' send-off; keep the chapter closers before it flat. Run Dimension #4c payoff-sentence sweep."
  - "Appendix B citations — every further-reading citation must be REAL and verified against the LIVE source, not a ledger (feedback_verify_citations_live_not_ledger; the XBYTE guide shipped fabricated App C names). Each carries a one-line 'why it matters here.'"
  - "Appendix A (space/time + FPGA terminology) — must ALWAYS carry the what-transfers/what-doesn't honesty; never let the borrowed FPGA vocabulary imply the P2 *is* an FPGA."
  - "Split seams — this book took the functional-decomposition + appendices half of the 2026-06-24 split from the 4-chapter first draft; *Getting Started* is the prerequisite. Any passage that RE-TEACHES orientation (what a cog/hub/smart pin is, how to read P2 code) is a defect — assume it, reference it, link out (voice-guide §2.2)."
---

# The P2 Architect's Guide — Descriptor

Thin per-manual overlay read by `document-audit` (and `prepare-manual` / `release-manual` /
`document-finalize`). Everything not listed in the front-matter is inherited from the central
skill body + the guides above.

**doc_class note.** This is a **narrative design/method book**, not an instruction reference — but it
is classed `reference` *for grounding rigor* (the same choice as the sibling *Getting Started*):
every architectural/language fact it states must trace to the KB YAML
(`deliverables/ai/P2/architecture/`, `language/`) or the Silicon Doc, and it gets **no**
tutorial-voice hallucination pass. Most of the book, however, is *method and reasoning* (the
functional-decomposition procedure, the two worked derivations, the agent-amplification argument) —
that content is not KB-derived fact, so the audit's centre of gravity is **voice/stance conformance
(Dimension #9, the anti-prescription + cadence discipline)** and **citation verification**, not
fact-tracing. Coverage is **deliberately non-exhaustive and non-cataloguing** — the book teaches a
method and links OUT to the reference manuals and *Getting Started* — so "doesn't cover X" is by
design, never a Dimension-C coverage finding.

**Structure (Dimension #10).** Three acts — Part I *Getting a Project Off the Ground* · Part II
*Thinking in P2* (the decomposition method + two derivations) · Part III *The Same Work, with an
Agent* — plus *In Closing* and Appendices A–B. 4 TikZ figures; **no example ZIP** (0 embedded code
by design). Front matter = house standard.

**Origin.** The design/realization companion to the reference manuals; took the decomposition +
appendices half of the 2026-06-24 split from the 4-chapter *P2 Architect's Guide* first draft (the
orientation half became *Getting Started with the Propeller 2*, `../p2-getting-started-guide/`).
Re-scoped 2026-07-08 to the shipped v1.0.0 three-act realization.
