---
manual_slug: p2-diagnostics-handbook
doc_class: reference          # diagnostics handbook: every fact traces to a Parallax source, a bench entry or a compile proof
code_line_budget_K: 76        # inherits the platform reference K (the XBYTE / Getting Started family budget)
last_published_tag: none      # never released; v0.1.0 is a shape prototype for review
guide_paths:
  creation_guide: none        # authored with the full build («#431»); until then ./PLANNING.md carries the decisions
  voice_guide: none
  style_guide: none
authoritative_sources: Spin2 v55 documentation and the Propeller 2 Documentation v35 under engineering/ingestion/sources/; the EF/XF bench ledgers and the CP compile-proof register under engineering/ingestion/external-sources/. The p2-debug-techniques claim ledger is a LEAD only.
high_risk_tables:
  - "Symptom Map — every row routes to a Section N.M heading that must exist; the crossref filter turns each into a link"
fragile_areas:
  - "Tool limits: the compiler and debugger figures (record count, record size, total DEBUG data) are never stated as numbers; the reader reads them from the listing"
  - "Run-time claims: a compile proves legality and listing counts, not what the program prints at run time"
  - "Partner-project material: no project names, file paths or file:line evidence from the private source files in reader text"
---

# P2 Diagnostics Handbook — Descriptor

Thin per-manual overlay read by `document-audit`, `prepare-manual`, `release-manual` and
`document-finalize`. Everything not listed above is inherited from the central skill bodies.

**State.** A **shape prototype** («#428», 2026-10-13): the full skeleton, the Symptom Map and one
written chapter (Chapter 2). Stephen reviews it to choose one handbook (A1) or separate notes and a
map (A2). The title and slug are working names. The creation and voice guides are written with the
full build, «#431»; until then `PLANNING.md` holds the decisions, the feed map and the Chapter 2
trace.
