---
manual_slug: P2AN005
doc_class: reference                              # app note — YAML/KB-backed; verifies claims against KB YAML + pnut-ts
element_type: application-note                    # ships doc + first-party YAML companion (four-artifact model)
code_line_budget_K: 76                            # inherits platform K (creation-guide §6.3); Dimension #3b
last_published_tag: unreleased                    # first draft (v0.1.0); Dimension #15 baseline = whole doc
guide_paths:
  creation_guide: ../APP-NOTE-CREATION-GUIDE.md
  voice_guide: ../APP-NOTE-VOICE-GUIDE.md
  style_guide: ../APP-NOTE-VOICE-GUIDE.md
companion_yaml: deliverables/ai/P2/application-notes/p2an005-cooperative-multitasking-tasks.yaml
authoritative_sources: see ../APP-NOTE-CREATION-GUIDE.md §5.1 # Spin2 Language Documentation v47+ (TASK method family + NEWTASK/THISTASK + TASKHLT register) + Spin2 v55 keyword table (engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt:39,149) + the P2KB cooperative-tasking pattern (spin2_cooperative_tasking.yaml) + pnut-ts v1.55.0 ground-truth probes
high_risk_quant:
  - "TASKCHK returns 0=free / 1=running / 2=halted (taskchk.yaml) — R3 tests ==2 for halted, R4 tallies 1 vs 2"
  - "TASKSPIN expression form returns the assigned task id, or -1 if all 32 slots are full (v55 text:39; compile-proved) — R3 captures prodId this way"
  - "TASKHLT register @ $200: 32 halt bits in REVERSE order (bit 0 = task 31, bit 31 = task 0) — R4 prints it as a raw bitmap, never indexes task N = bit N"
  - "NEWTASK and THISTASK both carry -1; context distinguishes (NEWTASK for TASKSPIN's slot arg, THISTASK for TASKHALT/TASKSTOP's target)"
  - "Version gate {Spin2_v47} MUST be the first source line or the TASK keywords are unrecognized"
fragile_areas:
  - "TASKWAIT does NOT exist (F-196, compile-proved 'Expected an instruction or variable') — never (re)introduce it into any recipe; the wait-with-yield idiom is a TASKCHK/TASKNEXT poll loop"
  - "TASKHLT bits are REVERSED — task 0 is bit 31; use TASKCHK(id) for a specific task's state, TASKHLT only for bulk bitmaps (R4 pitfall)"
  - "A task that halts itself (TASKHALT(THISTASK)) auto-yields; something else must TASKCONT it — R3's producer relies on this"
  - "Returning from a task's top method is an implicit TASKSTOP(THISTASK); the last task's return stops the cog"
  - "Cooperative = voluntary: a loop path with no tasknext() starves all siblings — every recipe yields every pass"
  - "The shutdown flag in R4 must be a shared VAR (not a local) so every worker sees it"
  - "taskptr table lives in cog regs $100..$11F (downward), overlapping the inline-PASM ORG..END area — heavy multitasking + heavy inline PASM compete (framed as a 🔧 Hardware note, not a recipe constraint)"
---

# P2AN005 — Cooperative Multitasking with Spin2 TASK Methods — Descriptor

Thin per-note overlay read by document-audit (and prepare-/release-/finalize-manual).
Fifth app note; reuses the companion schema piloted on [[P2AN001]] and carried by [[P2AN004]].
The lead of the **Concurrency & New Language Features** family (roster C1); companion to
[[P2AN006]] (stack sizing). Owning manual (Spin2 Reference) is PARKED → this note is the guided
home; advanced-fork-only (foundational fork EMPTY).

- **Grounding model:** `reference` — verify against the TASK method/constant/register YAMLs
  (`language/spin2/methods/task*.yaml`, `constants/{newtask,thistask}.yaml`,
  `registers/taskhlt.yaml`), the cooperative-tasking pattern
  (`patterns/implementation/spin2_cooperative_tasking.yaml`), the **Spin2 v55** keyword table, and
  `pnut-ts` v1.55.0 for every code-legality claim. No P1 content is read or cited (lineage only).
- **App-note agreement gate:** doc and `companion_yaml` must AGREE (method inventory, key
  semantics, gotchas). Companion is a digest+links, never a prose clone.
- **Structure (Dimension #10):** techniques-catalog per creation-guide §1.1/§4 — shared base
  (Abstract → Prereqs → The Idea → How It Works → Choosing) then Recipes R1–R4 (each Build + 🔍
  Verify) → Adapt It → Pitfalls → Conclusion → Resources → References → Revision History →
  Copyright/Acknowledgments. **No ToC.** No rendered figures (code + DEBUG only).
- **Verification model:** every embedded block + every `examples-library/*.spin2` compiles under
  `pnut-ts -d` (all four use `debug()`). Live scheduling / halt-resume timing / cog-frees-on-last-
  return are runtime behaviors described from the v47+ docs; hardware confirmation deferred (→ EF
  ledger when a run is accepted). No invented DEBUG captures.
- **Code (Dimensions #3/#3b):** K=76; inline code ASCII-only; no wrapped lines.
