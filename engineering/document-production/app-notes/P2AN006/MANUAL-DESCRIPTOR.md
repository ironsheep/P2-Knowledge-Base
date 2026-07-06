---
manual_slug: P2AN006
doc_class: reference                              # app note — YAML/KB-backed; verifies claims against KB YAML + pnut_ts
element_type: application-note                    # ships doc + first-party YAML companion (four-artifact model)
code_line_budget_K: 76                            # inherits platform K (creation-guide §6.3); Dimension #3b
last_published_tag: unreleased                    # first draft (v0.1.0); Dimension #15 baseline = whole doc
guide_paths:
  creation_guide: ../APP-NOTE-CREATION-GUIDE.md
  voice_guide: ../APP-NOTE-VOICE-GUIDE.md
  style_guide: ../APP-NOTE-VOICE-GUIDE.md
companion_yaml: deliverables/ai/P2/application-notes/p2an006-sizing-cog-task-stacks.yaml
authoritative_sources: see ../APP-NOTE-CREATION-GUIDE.md §5.1 # Spin2 Language Documentation (cogspin/coginit + TASKSPIN stack params; params->results->locals packing) + P2KB cogspin.yaml (stack floor ~32, typical 64-128, "overflow not detected") + stack_operations.yaml (hardware-stack distinction, cited to keep separate) + isp_stack_check.spin2 (Stephen M. Moraco, MIT — the shipped instrument) + pnut_ts v1.55.0
high_risk_quant:
  - "isp_stack_check constants: NOT_WRITTEN_MARK = $a5a50df0 (fill pattern), DO_NOT_WRITE_MARK = $addee5e5 (sentinel just past the buffer)"
  - "API takes (pStack, nStackLongCt) in LONGS: prepStackForCheck (fill+sentinel, before launch), checkStack (halts on overflow), getStackDepth (high-water count), reportStackUse (prints 'STACK used N of M')"
  - "Sizing method: start 128 -> exercise deepest path -> reportStackUse reads N -> set buffer ~1.5xN -> keep checkStack guard. Cog stack floor ~32, typical 64-128 (cogspin.yaml)"
  - "Stack consumes params -> results -> locals in declaration order, plus nested-call depth (Spin2 v55 text:284)"
  - "Two contexts, one technique: new-cog stack (cogspin) and intra-cog task stack (TASKSPIN); the instrument only watches a hub buffer"
fragile_areas:
  - "The sentinel long (endStackMark) MUST abut the stack buffer in the SAME DAT block — a gap breaks the technique (the overflow won't hit the sentinel first / the check reads the wrong long)"
  - "getStackDepth high-water only counts paths that ACTUALLY RAN — exercise the worst case before trusting the number (else you size too small)"
  - "checkStack detects the BOUNDARY was crossed (the one long past the buffer), not arbitrary corruption; sound because growth is contiguous, but frame it as 'boundary held/crossed'"
  - "isp_stack_check keeps working values in shared object DAT vars (pEndStackMark, nStkChkIdx, nStkChkUsed) -> ONE checker at a time; every recipe has a single thread check (reentrancy hazard if multiple cogs self-check concurrently)"
  - "The HUB Spin2 method stack sized here is NOT the P2 8-level HARDWARE call stack (PASM CALL/RET) — do not conflate; stack_operations.yaml's PTRA/PTRB CMP idiom is a different resource"
  - "R1-R3 are ordinary Spin2 (no directive); ONLY R4 needs {Spin2_v47} (it uses TASKSPIN) — keep the directive off R1-R3"
  - "isp_stack_check.spin2 ships VERBATIM (MIT, Stephen M. Moraco) with its license header retained; do not modify the object — describe it"
  - "P2 operator is `<=` not `=<` (pnut_ts rejects `=<` with 'Expected end of line') — caught during authoring"
---

# P2AN006 — Sizing Cog & Task Stacks — Descriptor

Thin per-note overlay read by document-audit (and prepare-/release-/finalize-manual).
Sixth app note; reuses the companion schema piloted on [[P2AN001]] and carried by [[P2AN004]].
Roster C3 in the **Concurrency & New Language Features** family; the companion to [[P2AN005]]
(cooperative multitasking) — C3 answers the stack-sizing question C1 raises. Owning manual
(Spin2 Reference) is PARKED → this note is the guided home; advanced-fork-only.

- **Grounding model:** `reference` — verify against `cogspin.yaml` / `taskspin.yaml` (stack params),
  `stack_operations.yaml` (hardware-stack distinction, cited to keep separate), the Spin2 v55
  stack-packing text, `pnut_ts` v1.55.0, and the shipped `isp_stack_check.spin2` (MIT). No P1
  content read or cited (lineage only; AN019 un-ingested and not needed).
- **App-note agreement gate:** doc and `companion_yaml` must AGREE (instrument API, constants, sizing
  method, gotchas). Companion is a digest+links, never a prose clone.
- **Structure (Dimension #10):** techniques-catalog per creation-guide §1.1/§4 — shared base
  (Abstract → Prereqs → The Idea → How It Works/sentinel technique + sizing method → Choosing) then
  Recipes R1–R4 (each Build + 🔍 Verify) → Adapt It → Pitfalls → Conclusion → Resources → References →
  Revision History → Copyright/Acknowledgments. **No ToC.**
- **Verification model:** every embedded block + every `examples-library/*.spin2` compiles under
  `pnut_ts -d` (each OBJ-includes `isp_stack_check.spin2`; the utility uses `debug()`). Overflow
  detection + the halt/lockup are runtime behaviors described from the utility's design; observing
  them fire is a bench step (→ EF ledger when accepted). No invented DEBUG captures.
- **Attribution:** `isp_stack_check` is credited to Stephen M. Moraco (Iron Sheep Productions, LLC)
  under MIT in Resources, References, and Acknowledgments; the bundled file keeps its own MIT header.
- **Code (Dimensions #3/#3b):** K=76; inline code ASCII-only; no wrapped lines.
