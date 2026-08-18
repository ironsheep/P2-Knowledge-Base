---
manual_slug: p2-debug-window-manual
doc_class: behavior                               # subsystem-operation manual — grounds against source-extraction (Theory-of-Operations), NOT language YAML
code_line_budget_K: 76                            # creation-guide "Code Line Budget"; platform-inherited (LM-Mono reference K)
last_published_tag: p2-debug-window-manual-v1.1.3   # baseline for Dimension #15 (released 2026-08-18, 168pp)
guide_paths:
  creation_guide: ./creation-guide.md
  voice_guide: ./voice-guide.md
  style_guide: ./voice-guide.md                   # no separate style-guide; voice-guide.md carries voice + style conformance
authoritative_sources: see ./creation-guide.md    # behavior-manual grounding; the per-window Theory-of-Operations docs are the "Bible" (creation-guide §0)
source_highlights:
  - ./REF/theory-of-operations/                   # PRIMARY grounding "the Bible" — 9 per-window ToO docs (TERM/BITMAP/PLOT/LOGIC/SCOPE/SCOPE_XY/FFT/SPECTRO/MIDI), current as of PNut v55
  - ./REF/DEBUG-WINDOW-DIRECTIVE-MATRIX.md         # master directive / parameter / range / default matrix across all windows
  - ./REF/DEBUG-Statement-Quoting-Briefing-for-Doc-Agents.md   # DEBUG-statement quoting rules (single-quote text; backtick-command contents)
  - engineering/ingestion/sources/spin2-v55/       # Spin2 v55 DEBUG-display reference (command syntax / keyword gating)
  - engineering/ingestion/external-sources/hardware-verification/campaigns/2026-06-debug-windows-and-smart-pins/   # empirical 🏆 top-of-trust-chain captures
  - pnut-ts                                         # compile-cert of ALL examples — use `pnut-ts -d` (without -d the compiler ignores debug() contents = false pass)
high_risk_tables:
  - "Appendix A command reference — the master directive table (many rows × name / syntax / range / default); transposition-prone, verify each row vs REF/DEBUG-WINDOW-DIRECTIVE-MATRIX.md"
  - "Per-window directive / parameter tables (each window chapter) — parameter / range / default columns vs that window's REF/theory-of-operations/<WINDOW>_Theory_of_Operations.md"
  - "SCOPE / SCOPE_XY / LOGIC trigger + channel-config parameter tables (config rides different messages per window — see fragile_areas)"
fragile_areas:
  - "PLOT coordinate origin — default is bottom-left / Y-UP; CARTESIAN flipy=1 flips to Y-DOWN. Manual + ToO prose historically had this backwards; trust the PLOT_GetXY formula + hardware captures, not loose prose."
  - "DEBUG window 3-phase lifecycle (create → one-time config → looping update). SCOPE/FFT config is its OWN message after the create line; LOGIC/SCOPE_XY config rides the create message — easy to state wrong."
  - "Session-end mechanisms — three distinct forms, often conflated: per-window `` `CLOSE ``; on-chip DEBUG(DEBUG_END_SESSION) ({Spin2_v52}); host --end-marker string."
  - "DEBUG statement quoting — single-quoted display text only; backtick-command contents must compile with `pnut-ts -d` (a no-`d` compile is a false pass; inner-backtick commands slip through)."
  - "DEBUG/window directives are PASM/DEBUG, not Spin2 methods (e.g. DIRH/DIRL) — a pnut-ts blind spot; verify against the directive matrix, not by compile alone."
  - "Window names + counts — nine DEBUG display windows (TERM, BITMAP, PLOT, LOGIC, SCOPE, SCOPE_XY, FFT, SPECTRO, MIDI); assertion of '9 windows' and the window roster is high-bug-density (Dimension #5)."
---

# P2 Debug Window Manual — Descriptor

Thin per-manual overlay read by `document-audit` (and `prepare-manual` / `release-manual` /
`document-finalize`). Everything not listed in the front matter is inherited from the central
`document-audit` skill body + the guides referenced above.

**Grounding-model note:** `doc_class: behavior`. There is little/no language YAML for the DEBUG
display windows — the subsystem is documented by **source-extraction**. The source of truth is the
per-window **Theory-of-Operations** set in `./REF/theory-of-operations/` (the "Bible", current as
of **PNut v55**) plus the `DEBUG-WINDOW-DIRECTIVE-MATRIX.md`, the Spin2 v55 DEBUG reference, and the
hardware-verification debug-windows campaign. Factual dimensions (A, B, #1, #5, C) verify against
*those* documents, **not** `deliverables/ai/P2/language/`; the `p2kb-mcp` currency caveat does not
apply (read the ToO docs from disk). Where a discrepancy exists between PNut behavior and any prose,
**PNut is ground truth** (and `pnut-term-ts` mirrors it).

**Superseded `AUDIT-PROCESS.md` — flagged, not removed.** The folder still carries the legacy
`AUDIT-PROCESS.md` (the old per-manual process doc). Its one unique element — the **two
grounding-models** distinction — is already carried into the central `document-audit` skill (§3 +
the `doc_class` field), so the carry-across is **verified complete**. Per the skill's §11, retiring
the copy is a deliberate consolidation step (archive to a git-ignored `./archive/`, not a delete) —
queued to run as part of this v1.0.1 release, **not** as a side effect of this audit.

**Baseline note (Dimension #15):** `last_published_tag` was created retroactively at the v1.0.0
release commit `17dfa47a` (2026-06-16, the published 159pp PDF) — v1.0.0 was never tagged. The
v1.0.1 delta (`17dfa47a..HEAD`) is the post-release work: caption-driven example-library migration,
re-audit TIER-1/2 fixes, the SCOPE trigger-offset semantics resolution, visual-review content edits,
and name-attribution removal.
