---
manual_slug: P2AN007
doc_class: reference                              # app note — YAML/KB-backed; verifies claims against KB YAML + pnut_ts
element_type: application-note                    # ships doc + first-party YAML companion (four-artifact model)
code_line_budget_K: 76                            # inherits platform K (creation-guide §6.3); Dimension #3b
last_published_tag: unreleased                    # first draft (v0.1.0); Dimension #15 baseline = whole doc
guide_paths:
  creation_guide: ../APP-NOTE-CREATION-GUIDE.md
  voice_guide: ../APP-NOTE-VOICE-GUIDE.md
  style_guide: ../APP-NOTE-VOICE-GUIDE.md
companion_yaml: deliverables/ai/P2/application-notes/p2an007-data-structures-new-facilities.yaml
authoritative_sources: see ../APP-NOTE-CREATION-GUIDE.md §5.1 # Spin2 Language Documentation v45+ (STRUCT: decl/typed members/arrays/nesting/SIZEOF/pointers/v49 cross-object export-import) + hardware lock methods (LOCKNEW/LOCKTRY/LOCKREL/LOCKRET) + architecture/locks.yaml (16 locks, test-and-set, deadlock ordering) + data-flow-contracts.yaml + latest-wins/buffer-management patterns (mechanisms CITED, contract CHOICE deferred to Architect's Guide) + pnut_ts v1.55.0
high_risk_quant:
  - "STRUCT requires {Spin2_v45}; members default LONG, packed (no padding); reading_t(LONG,LONG,BYTE)=9 bytes; SIZEOF returns byte size"
  - "Pass-by-value <=15 longs; larger use BYTEMOVE internally. Receiving ^structName from a CHILD object needs bracket notation `[pRec] := child.method()` or >15-long structs throw a compile error"
  - "P2 has 16 hardware locks. LOCKNEW returns 0..15 or -1 (check it); LOCKTRY(id) nonzero if captured; LOCKREL(id); LOCKRET(id) frees. REPEAT UNTIL LOCKTRY = spin-acquire"
  - "Atomicity model: a single hub LONG is read/written atomically; a multi-field record is NOT. Publish = write fields FIRST, flip one long (index/seq) LAST"
  - "Single writer of an index/seq long -> no lock (R2 ring, R3 mailbox). Several writers -> one lock (R4 queue)"
fragile_areas:
  - "Uses the REAL P2 locks LOCKNEW/LOCKTRY/LOCKREL — NEVER the P1 lockset()/lockclr() (F-199: those are P1, do not exist in P2, would not compile)"
  - "Publish-index/seq-LAST is load-bearing: write the record's fields, THEN advance the index or bump the sequence counter; reversing them yields torn/partial reads"
  - "Release the lock on EVERY exit path from a critical section (early RETURN/ABORT must LOCKREL first); free with LOCKRET when done"
  - "Two-lock designs must acquire in the SAME order (ascending by id) — mismatched order deadlocks (locktry.yaml anti-pattern)"
  - "SCOPE: implementation-only. The contract DECISION (which structure, copy vs reference, refcount-vs-copy fan-out) is CITED to the P2 Architect's Guide + data-flow-contracts.yaml, never taught here"
  - "Child-object struct-pointer return needs `[pRec] := child.method()` bracket receipt (only across OBJ boundaries)"
  - "P2 operator is `<=` not `=<` (pnut_ts rejects `=<`)"
---

# P2AN007 — Data Structures with the New Language Facilities — Descriptor

Thin per-note overlay read by document-audit (and prepare-/release-/finalize-manual).
Seventh app note; reuses the companion schema piloted on [[P2AN001]] and carried by [[P2AN004]].
Roster C2 in the **Concurrency & New Language Features** family; sibling to [[P2AN005]] /
[[P2AN006]]. Owning manual (Spin2 Reference) is PARKED → this note is the guided home;
advanced-fork-only.

- **Grounding model:** `reference` — verify against `keywords/STRUCT.yaml` (+ `concepts/struct-
  bitfields.yaml`), the lock method YAMLs + `architecture/locks.yaml`, `data-flow-contracts.yaml`
  and the latest-wins/buffer-management pattern YAMLs (mechanisms only — the CHOICE is the
  Architect's Guide's), and `pnut_ts` v1.55.0. No P1 content read or cited (lineage only).
- **SCOPE (Dimension #10 + boundary):** implementation-only. Teaches the worked code; CITES the
  P2 Architect's Guide + `data-flow-contracts.yaml` for which-structure-and-why (esp. the
  irreversible refcount-vs-copy fan-out decision). Do NOT let the note grow the contract-decision
  reasoning.
- **App-note agreement gate:** doc and `companion_yaml` must AGREE (STRUCT facts, the atomic-publish
  discipline, lock usage, gotchas). Companion is a digest+links, never a prose clone.
- **Structure:** techniques-catalog — shared base (Abstract → Prereqs → The Idea → How It Works →
  Choosing) then Recipes R1–R4 (each Build + 🔍 Verify) → Adapt It → Pitfalls → Conclusion →
  Resources → References → Revision History → Copyright/Acknowledgments. **No ToC.**
- **Verification model:** every embedded block + every `examples-library/*.spin2` compiles under
  `pnut_ts -d`. Cross-cog atomicity/race-freedom is a runtime multi-cog property (compile proves
  legality only); described from the atomic-single-long model, hardware confirmation deferred
  (→ EF ledger when accepted). No invented DEBUG captures.
- **Code (Dimensions #3/#3b):** K=76; inline code ASCII-only; no wrapped lines. Uses real P2 locks
  (never P1 lockset/lockclr).
