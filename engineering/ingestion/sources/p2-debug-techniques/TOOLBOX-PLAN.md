# p2-debug-techniques — debug toolbox plan («#433», DESIGN)

**What this is.** The plan that makes every agent-actionable trap, technique and fact in
`CLAIM-LEDGER.md` reachable through the KB (`p2kb_get` / `p2kb_find`), under **Standard A**
(Stephen, 2026-10-15, "yes A"): every fact a row rests on is sourced at its tier, and the technique
as a whole is proven by a compile proof (CP) or a bench run (EF); what cannot be proven yet becomes a
specific bench question, not KB text. Documents are suspended; the KB comes first.

**Status.** Design only. Nothing in `deliverables/ai/P2/`, no ledger and no register changes in this
task. F-numbers and CP numbers are allocated by the arbiter at execution. Every batch is gated by
Phase S (an independent sourced/derived/advice/unsourced classing of each added statement) before
its commit; no release without Stephen.

**Inputs.** `CLAIM-LEDGER.md` (411 rows, read in full); `.claude/doctrine-overlay.md` (the
sections named in the task); `COMPILE-PROOFS.md` (CP-001..CP-025); `P2-EMPIRICAL-FINDINGS.md`
(EF ledger); `EXTERNAL-HARDWARE-FINDINGS.md` (XF-001..XF-018); `VERIFICATION-OPPORTUNITIES.md`;
`engineering/tools/generate-p2kb-index.py` (alias harvest, key derivation, delivery filter);
`engineering/tools/p2kb-categories.json`; the KB entries named per row.

---

## 0. How to read this plan

**Row tokens** (each main-table row carries exactly one primary form token):

| token | meaning |
|---|---|
| `F=POU` | point of use: the trap/fact goes into the entry an agent opens while writing that code |
| `F=HUB` | symptom hub: the row supplies a symptom or a cause in a troubleshooting entry (§3) |
| `F=PAT` | pattern: a compilable technique entry under `language/spin2/patterns/` (§4) |
| `F=SHIP` | already in the KB (COVERED before the ingestion, or shipped by «#430» batch 1/2): an input, not redo; its home is named |
| `F=HELD` | its only evidence is an UNGRADED partner record (XF-005..XF-018); nothing ships until the partner's run records are graded |
| `F=NAA` | not agent-actionable, with the reason |

Secondary routes are written `+HUB(S-nn)`, `+POU`, `+PAT-n`.

**Proof tokens:** `P=SRC` (a Parallax document or a listing at its edition states the whole) ·
`P=CP-0nn` (existing compile proof) · `P=NEWCP-nn` (a new CP, probe already run in the scratchpad,
command in §5.2) · `P=EF-0nn` / `P=XF-00n` (existing bench record) · `P=BQ-nn` (bench question for
Stephen, §5.3) · `P=PQ` (partner records already requested in «#429»; no new request) · `P=—`.

**Source abbreviations** (provenance for us; the shipped YAML carries none of it):
v55 = Parallax Spin2 Language Documentation v55 (`spin2-v55-text.txt`, line given for us);
v35 = Parallax Propeller 2 Documentation v35, Rev B/C silicon (`silicon-doc/p2-documentation.txt`);
INT55 = Parallax Spin2 Interpreter v55 listing; DBG51 = Parallax Spin2 Debugger v51 listing (the
only ingested edition of the debugger); DS = `language/spin2/debug-commands/debug-strategy-guide.yaml`;
DM = `language/spin2/constants/debug-mask.yaml`; SC = `language/spin2/constants/special-configuration-symbols.yaml`;
P2AN006 = `application-notes/p2an006-sizing-cog-task-stacks.yaml`. Hub files H-A..H-D are in §3.

**Batches** (§6): B0 defects · B1a-c pitfall-key conversion · B4 debug POU · B5 preprocessor POU ·
B6 cogs/pins/streamer POU · B7 patterns · B8a/b symptom hubs · B9 bench-dependent · B10 partner-dependent.

**How every count in this plan is produced** (re-runnable; no script):

```text
grep -c "^| DT-[0-9]* " engineering/ingestion/sources/p2-debug-techniques/CLAIM-LEDGER.md        -> 411 rows
grep -c "^| DT-[0-9]* .*| drop" .../CLAIM-LEDGER.md                                             -> 82 drop-led rows
grep -c "^| DT-[0-9]* | [A-E]-[0-9]* | .* | method | " .../CLAIM-LEDGER.md                       -> 74 method rows
grep -c "^| DT-[0-9]* | [a-z]* | F=POU" .../TOOLBOX-PLAN.md   (and F=HUB, F=PAT, F=SHIP, F=HELD, F=NAA) -> per-form counts, §1.1 rows only
grep -c "^| DT-[0-9]* | .*+HUB" .../TOOLBOX-PLAN.md                                              -> §1.1 rows that also feed a hub symptom
```

Rows split: **265** trap/technique/fact rows not drop-led (§1.1) + **72** drop-led
trap/technique/fact rows (§1.2) + **74** method rows (§1.3) = 411. The arbiter's earlier tally
("~290 not drop-only") used a narrower drop-only definition; this plan lists every row, so the
difference in definition loses nothing.

---

## A. Findings that shape the design (read before §1)

**A.1 An agent cannot reach a symptom today.** `p2kb_get("debug output stops")` against the
published index (2026-10-15) returned *Multiple matches* with 21 suggestions at score 0.33, none of
them a diagnosis. Retrieval is three routes only — the `aliases` table (exact match, verbatim and
upper-cased), the fuzzy camelCase key, and category membership; an index entry carries no title or
description, so there is no content search (`generate-p2kb-index.py`, `harvest_aliases_from_yaml`,
`NAME_FIELDS`). `keywords:` is not harvested; `title:` is (exact value). A symptom reaches an agent
only as an exact alias. Two files carrying the same alias produce an array, which `p2kb_get`
returns as suggestions, so **each symptom phrase must be owned by exactly one file** (§3.3).

**A.2 Symptom aliases already exist at a point of use.** DS carries `"object has DEBUG_MASK = 0
but still prints"`, `"debug output garbled after changing the clock"`, `"debug stops working after
clkset"`; `architecture/pin-drive-configuration.yaml` carries a "symptom-shaped" alias. The hub
design keeps those where they are (§3.3).

**A.3 `guides/` is served and categorised.** `guides/*.yaml` get the key prefix `p2kbGuide`
(`get_category_prefix`), the category `guides.getting_started` (`p2kb-categories.json`), and
`p2kb_find("guide")` lists `p2kbGuideQuickQueries` and the two getting-started guides.
`guides/quick-queries.yaml` (the self-declared bootstrap) has a `troubleshooting:` section of three
keys-only checklists, some unsourced ("Account for hub access timing").

**A.4 The delivery filter strips `source`, `sources`, `documentation_source` and column-0
comments** (`DELIVERY_FILTER`), so per-cause provenance in a hub file stays for the gates and never
reaches the agent. **The claim-sourcing gate is key-agnostic** (`audit-yaml-claim-sourcing.py`
exempts only example blocks; "NOT anti_patterns / common_patterns -- those state claims"), and no
tool or schema reads any pitfall key by name (`grep -rl "anti_patterns" engineering --include=*.py`
→ the audit only), so a key rename breaks no gate.

**A.5 Two source facts settle ledger rows the extraction left open.**
- **DBG51 `debug_done`** waits on `rdpin t1,_txpin_ wc` until the transmitter is not busy, then
  floats the TX pin; v35 (async serial TX, "RDPIN/RQPIN with WC always returns the 'busy' flag into
  C. This is useful for knowing when a transmission has completed"; the busy flag clears after the
  STOP bit). So a DEBUG statement returns only after its last stop bit has left the P2 — the P2 side
  does not cut a completed line (DT-116/117, XF-006).
- **v55 inline PASM procedure** (:792-798, :808, :835): Spin2 "Save[s] the current streamer
  bytecode address", lets the PASM "Use the FIFO temporarily", then "Restore[s] the streamer address
  and resume[s] Spin2 bytecode execution" (INT55 restarts with `_ret_ rdfast #0,pb`). This sources the
  half of DT-231 that is a statement; the trap itself is BQ-07.

**A.6 Defects seen while designing (served now; fixed first in B0, register-first).**
- **D-1** SC `DEBUG_DISABLE.description`: "Globally disables ALL debug statements" — v55:1028 says
  "disable all DEBUG statements in the file/object". An agent reading it disables one library and
  believes the whole program is silent. Also "zero runtime overhead" (red-flag wording, unsourced).
- **D-2** `language/pasm2/concepts/streamer_smartpin_control.yaml` `debugging.monitoring`: "TESTP for
  pin state" (on a smart-pin pin TESTP returns the smart pin's flag — the same file's subject; v35
  :7502, testp.yaml) and "Use lock[15] for debug monitor"; `best_practices`: "Reserve lock[15] for
  debug" (v55:926: LOCK[15] is allocated by the debugger in a -d build).
- **D-3** `language/spin2/methods/cogspin.yaml` `warnings`: "Insufficient stack causes crashes"
  contradicts the same file's `size_and_limit` (no stack-limit compare in INT55; overflow is not
  detected) and DT-143 (silent corruption, not a crash).
- **D-4** `guides/quick-queries.yaml` `troubleshooting`: unsourced checklist items ("Verify COG code
  is in DAT section", "Account for hub access timing", "Check for blocking operations"); fixed with
  the hubs in B8a (it becomes the pointer to them).

**A.7 Probes run for this design** (scratchpad only, pnut-ts v1.55.8; commands in §5.2):
p01 refutes DT-012 (an OR-expression DEBUG_MASK override compiles, binary identical to the literal);
p02 proves DT-013; p03 proves DT-064 and shows a never-called method's `debug()` still costs its
record; p04 proves DT-238/240/242/250; p05 proves DT-068/069; p09 proves DT-105/244; p10 shows DT-190
compiles; p11 proves the split-statement cure for DT-042's one-record limit; p06/p07/p08 compile the
pattern code for PAT-2/PAT-1/PAT-4.

---

## 1. RE-ROUTE

### 1.1 Trap / technique / fact rows (265)

Columns: id · kind · form · KB destination · facts → source · whole → proof · batch.

#### Part A — debug channel, budgets, format-into-memory (38)

| DT | kind | form | KB destination | facts → source | whole → proof | batch |
|---|---|---|---|---|---|---|
| DT-006 | trap | F=SHIP +HUB(S-03) | DS `common_mistakes` ("can still be chatty and still use up the limits"); DS alias owns the symptom | v55:1027 | P=CP-015 | B8a |
| DT-007 | trap | F=SHIP +HUB(S-03) | DS `common_mistakes` ("record and DEBUG data stay in the budget") | v55:1027 | P=CP-015 | B8a |
| DT-011 | tech | F=NAA | — | premise refuted: the direct OBJ override works | P=CP-014 | — |
| DT-012 | trap | F=NAA | — (no KB text) | refuted: OR-expression override compiles, same binary as `%11` | P=NEWCP-01 (records the refutation) | B4 |
| DT-013 | tech | F=POU | DS `mechanism_details.debug_mask.per_object`; DM | `-D` reaches every object (CP-013); a mask belongs to its file/object (v55:1027, CP-014) | P=NEWCP-02 | B4 |
| DT-015 | fact | F=SHIP | DS (no `{Spin2_v46}` remains: `grep -rn "Spin2_v46"` on DS and DM is empty) | v55:38 | P=CP-025 | — |
| DT-022 | fact | F=SHIP | SC `DEBUG_COGS` (F-585) | v55:1011 | P=CP-018 | — |
| DT-024 | tech | F=SHIP +HUB(S-09) | DS `measuring_with_debug_on`; `architecture/streamer/overview.yaml` | v55:1011, :1068 | P=EF-057 | B8a |
| DT-027 | trap | F=HUB(S-01) | H-A S-01 (compile gate vs runtime gate) | v55:1011, :1027, :1068; DM `debug_cogs_interaction` | P=CP-014, CP-015, CP-018 (compile side); runtime side P=SRC (v55:1068) | B8a |
| DT-032 | fact | F=SHIP | SC `DEBUG_TIMESTAMP` (F-586) | DBG51 (GETCT in the sending cog's ISR) | P=SRC | — |
| DT-033 | trap | F=SHIP +HUB(S-06) | SC `DEBUG_TIMESTAMP`; `architecture/silicon_errata.yaml` E3 | EF-068 | P=EF-083 | B8a |
| DT-039 | trap | F=NAA | technique already SHIP: DS `how_it_fails`, `stay_well_inside` | tool limit: loud m151 at the cap; the mute-at-load zone was struck (VO-J-027) | P=— | — |
| DT-044 | fact | F=NAA | technique SHIP: DS `how_you_find_out` (read the listing) | tool limit (a baseline figure) | P=— | — |
| DT-046 | trap | F=NAA | technique SHIP (DS) | tool limit (soft zone) | P=— | — |
| DT-057 | tech | F=SHIP +POU | DS `lock_15_per_statement` (LOCK[15] entry/exit and DLY release shipped, F-587); "one statement is one unbroken line" not shipped (Phase S DERIVED) | v55:926, :1003; DBG51 `.wait locktry #15` / `lockrel #15` | whole: P=BQ-02 | B9 |
| DT-058 | tech | F=PAT +PAT-1 | `language/spin2/patterns/implementation/spin2_debug_line_buffer.yaml` (new) | v55 value-only ZSTR_ (:1001); CP-022 (DAT text is not DEBUG data) | P=NEWCP-09 | B7 |
| DT-060 | trap | F=PAT +PAT-1 (sourced half) | PAT-1 states only: the DAT buffer is one per image, shared by every instance | CP-024 | "two cogs corrupt it" is DERIVED (a generic race): not shipped, no BQ | B7 |
| DT-061 | tech | F=PAT +PAT-1 | PAT-1 | CP-024; v55 DAT | P=NEWCP-09 | B7 |
| DT-062 | tech | F=NAA | — | DEBUG_DISABLE removes only that object's statements (v55:1028); every other statement still reconfigures the TX pin (DS `p62_is_reconfigured_by_every_debug_call`); the sourced rule is DS `cog_start_traffic` (build without -d) | P=— | — |
| DT-064 | trap | F=POU +HUB(S-04) | DS `the_compilers_limits.what_debug_data_counts` + `reducing_bytes_and_records` | a statement is a record whether or not it runs; #ifdef removes code | P=NEWCP-03 | B4 |
| DT-068 | trap | F=POU +HUB(S-01) | SC `DEBUG_DISABLE` (after D-1); DS `mechanism_details.debug_disable` | v55:1028 | P=NEWCP-05 | B4 |
| DT-069 | tech | F=POU | DS `mechanism_details.debug_disable`: pass the value out through a method and print it where debug is compiled | v55:1028; Spin2 method results (v55) | P=NEWCP-05 | B4 |
| DT-072 | tech | F=SHIP +HUB(S-09) | DS `hub_memory`; `architecture/hub.yaml` | v55:900 | P=SRC | B8a |
| DT-076 | trap | F=SHIP +HUB(S-10) | DS `p62_is_reconfigured_by_every_debug_call` | DBG51 (fltl/wrpin/drvl of the TX pin at each entry) | P=SRC + XF-002 | B8a |
| DT-078 | tech | F=SHIP | `language/spin2/methods/locknew.yaml` (check `< 0`, F-592) | v55 LOCKNEW; INT55 | P=SRC | — |
| DT-083 | tech | F=SHIP | DS `measuring_with_debug_on`; streamer `overview.yaml` | EF-057 | P=EF-057 (the DEBUG_COGS half); "capture, stop, then print" ordering is DERIVED: not shipped | — |
| DT-086 | tech | F=SHIP +POU | DS `pins_62_63`/`clock_source` (shipped); verify `language/spin2/methods/clkset.yaml` says CLKSET keeps the debugger's frequency current | v55:28, :927, :1059 | P=SRC (v55 states the effect) | B4 |
| DT-087 | fact | F=HUB(S-09) | H-A S-09 cause: the debug interrupt is taken at each COGINIT of an enabled cog and at each DEBUG statement | v55:897, :1011, :1069 | P=SRC; "no per-instruction overhead" stays withdrawn (F-588) | B8a |
| DT-088 | trap | F=HELD | (H-A S-09 if graded) | XF-009 UNGRADED | P=PQ | B10 |
| DT-089 | trap | F=HUB(S-07) pending | H-A S-07/S-08 cause, only after BQ-01 | XF-008 UNGRADED; sources silent | P=BQ-01 | B9 |
| DT-091 | tech | F=NAA | — | its purpose is inspection in the host single-step debugger; no P2 claim to carry | P=— | — |
| DT-092 | trap | F=SHIP | `language/pasm2/concepts/rep_instruction.yaml` (F-609) | v35 REP | P=SRC | — |
| DT-093 | trap | F=SHIP | `language/spin2/methods/cogstop.yaml` (F-595) | v55 REPEAT note; v35 LOCKS, WRFAST | P=SRC | — |
| DT-095 | fact | F=NAA | — | third-party toolchain (flexspin); sources silent | P=— | — |
| DT-103 | tech | F=NAA | — | channel-assignment style; no P2 fact | P=— | — |
| DT-105 | fact | F=POU | DM `channel_mapping`; `language/spin2/preprocessor/preprocessor-overview.yaml` | v55:1027; #ifdef excludes code | P=NEWCP-06 | B4 |
| DT-108 | tech | F=NAA | — | host shell recipe; the P2 fact it checks is at DS | P=— | — |
| DT-111 | fact | F=POU | `language/spin2/constructs/method_definition.yaml` (absent there; present in `language/fundamentals/variable-scoping-best-practices.yaml`) | v55:286, v37 note :29 | P=SRC | B4 |

#### Part B — wrong printouts, silence, stacks, worker + mailbox (72)

| DT | kind | form | KB destination | facts → source | whole → proof | batch |
|---|---|---|---|---|---|---|
| DT-112 | trap | F=HELD | (H-A if graded) | XF-005 UNGRADED, no named cause | P=PQ | B10 |
| DT-113 | tech | F=HELD | (H-A if graded) | XF-005 | P=PQ | B10 |
| DT-114 | trap | F=HELD | (H-A if graded) | XF-005 | P=PQ | B10 |
| DT-116 | trap | F=NAA +POU(counter-fact) | P2-side loss is contradicted; ship the sourced counter-fact in DS `lock_15_per_statement` and H-A S-08: a DEBUG statement returns only after its last stop bit has left the transmitter | DBG51 `debug_done`; v35 async TX busy flag | P=SRC (listing at edition v51 + v35) | B4 |
| DT-117 | tech | F=NAA | — | no drain step is needed on the P2 side (A.5); XF-006 UNGRADED | P=— | — |
| DT-118 | trap | F=NAA | — | generic test logic | P=— | — |
| DT-119 | tech | F=NAA | — | generic test logic | P=— | — |
| DT-121 | fact | F=NAA | — | host chain (USB link, terminal, harness) | P=— | — |
| DT-122 | tech | F=NAA | — | PNut-Term-TS option; the KB defers that tool's options to its `--help` (`tools/pnut-ts-compiler.yaml`) and no source documents `-u` | P=— | — |
| DT-123 | trap | F=NAA | — | host terminal/log encoding | P=— | — |
| DT-124 | trap | F=NAA | — | host `grep` behaviour | P=— | — |
| DT-125 | tech | F=NAA | — | host harness | P=— | — |
| DT-127 | trap | F=HUB(S-07) | H-A S-07 with sourced causes only: top method returned or aborted (v55:39; `abort.yaml`); an ISR's retrigger lost after DEBUG (DS); every cog's DEBUG output shares LOCK[15] | v55:39, :926; DBG51 locktry wait | P=SRC per cause; the 98-s observation itself HELD (XF-007, P=PQ) | B8a |
| DT-129 | fact | F=HUB(S-07) | H-A S-07 (sourced half: one LOCK[15]-shared TX path serves every cog) | v55:926 | P=SRC; "silence cannot tell them apart" is DERIVED: not shipped | B8a |
| DT-130 | tech | F=NAA | — | generic instrumentation | P=— | — |
| DT-131 | tech | F=NAA | — | arbiter: METHOD (an inference) | P=— | — |
| DT-132 | tech | F=PAT +PAT-2 | `language/spin2/patterns/implementation/spin2_progress_observer.yaml` (new) | hub VAR/DAT are shared by the cogs (v55); single-long publish (EF-037) | P=NEWCP-10 (legality) + BQ-10 (whole) | B9 |
| DT-133 | tech | F=PAT +PAT-2 | PAT-2 readings (each a pre-registered BQ-10 leg) | as DT-132 | P=BQ-10 | B9 |
| DT-134 | fact | F=PAT +PAT-2 | PAT-2 `resources` (describes the code: one hub write per unit of work) | the code itself | P=NEWCP-10 | B9 |
| DT-135 | tech | F=NAA | — | needs an external instrument | P=— | — |
| DT-136 | fact | F=NAA | — | external instrument; arithmetic on a baud | P=— | — |
| DT-137 | trap | F=NAA | — | generic; its P2 half is DT-139 | P=— | — |
| DT-138 | trap | F=NAA | — | generic editing | P=— | — |
| DT-139 | fact | F=SHIP +POU +HUB(S-30) | `cogspin.yaml` (TASKSTOP(-1) note, shipped); whole class: add to `language/spin2/methods/taskspin.yaml` (absent) | v55:39 | P=SRC | B6, B8b |
| DT-140 | tech | F=PAT +PAT-2 | PAT-2 (end every base method in a reporting park) | v55:39 | P=NEWCP-10 + BQ-10 | B9 |
| DT-141 | tech | F=PAT +PAT-2 | PAT-2 (observer times out and reports) | — | P=BQ-10 | B9 |
| DT-143 | fact | F=SHIP +HUB(S-31) | `cogspin.yaml` `size_and_limit` (D-3 fixed first) | INT55 (no stack-limit compare) | P=SRC | B0, B8b |
| DT-144 | fact | F=SHIP | `cogspin.yaml` | INT55 | P=SRC | — |
| DT-145 | fact | F=SHIP | `cogspin.yaml` growth | INT55 | P=SRC | — |
| DT-146 | trap | F=POU | `cogspin.yaml` growth + P2AN006 `placement_rule` (the guard-before case) | stack grows upward (INT55) | P=BQ-03 | B9 |
| DT-147 | trap | F=NAA | — | anecdote; DT-146 carries the trap | P=— | — |
| DT-148 | tech | F=SHIP | P2AN006 | — | (app note) | — |
| DT-149 | tech | F=SHIP | P2AN006 | — | (app note) | — |
| DT-150 | tech | F=SHIP | P2AN006 | — | (app note) | — |
| DT-151 | tech | F=SHIP | P2AN006 | — | (app note) | — |
| DT-152 | fact | F=NAA | — | no demonstrated trigger in Spin2 (locals zeroed, v55:286; F-575) | P=— | — |
| DT-153 | tech | F=SHIP | P2AN006 `getStackDepth` | — | (app note) | — |
| DT-154 | trap | F=NAA | — | refuted for Spin2 frames (v55:286); P2AN006 claims nothing (F-575) | P=— | — |
| DT-155 | fact | F=NAA | — | follows DT-154 | P=— | — |
| DT-156 | trap | F=NAA | — | an algorithmic property of the scan, not P2 behaviour; P2AN006 already reports "used N of M" | P=— | — |
| DT-157 | tech | F=NAA | — | reporting advice | P=— | — |
| DT-158 | trap | F=SHIP | P2AN006 `gotchas` (floor, two causes) | — | (app note) | — |
| DT-159 | tech | F=NAA | — | wording advice | P=— | — |
| DT-160 | tech | F=NAA | — | P2AN006 already says confirm the prepare step ran | P=— | — |
| DT-161 | trap | F=SHIP | P2AN006 `gotchas` | — | (app note) | — |
| DT-162 | tech | F=SHIP | P2AN006 | — | (app note) | — |
| DT-163 | fact | F=SHIP | `cogspin.yaml` `p1_symbols_do_not_apply` | — | — | — |
| DT-164 | fact | F=SHIP | `cogspin.yaml` `top_level_stack` | INT55 | P=SRC | — |
| DT-165 | tech | F=PAT +PAT-2 | PAT-2 (work on an owned-stack cog; cog 0 observes) | cogspin `top_level_stack` | P=BQ-10 | B9 |
| DT-166 | tech | F=PAT +PAT-2 | PAT-2 code property (observer does hub reads only); no claim | — | P=NEWCP-10 | B9 |
| DT-167 | tech | F=PAT +PAT-2 | PAT-2 + P2AN006 `getStackDepth` | — | P=BQ-10 | B9 |
| DT-168 | tech | F=PAT +PAT-2 | PAT-2 variant: diagnostic command through the latest-wins mailbox | EF-038 | P=BQ-10 | B9 |
| DT-169 | trap | F=NAA | — | a stopped cog executes nothing (v55 COGSTOP); self-evident | P=— | — |
| DT-171 | trap | F=NAA | — | sizing advice (P2AN006 owns sizing) | P=— | — |
| DT-172 | fact | F=SHIP | `cogspin.yaml` growth (6 + 1 longs) | INT55 | P=SRC | — |
| DT-173 | fact | F=SHIP | `method_definition.yaml` | v55 | P=SRC | — |
| DT-174 | fact | F=SHIP | `inline_pasm.yaml` `stack_usage` | v55:812 | P=SRC | — |
| DT-175 | trap | F=SHIP +HUB(S-33) | `cogspin.yaml` `not_an_input` | v55:1664, :1669 | P=SRC | B8b |
| DT-176 | fact | F=NAA | — | reasoning (DERIVED) | P=— | — |
| DT-177 | tech | F=SHIP | `spin2_latest_wins_mailbox.yaml` (seq/ack) | EF-038 | P=EF-038 | — |
| DT-178 | tech | F=PAT +PAT-2 | PAT-2 in-flight triple | — | P=BQ-10 | B9 |
| DT-179 | tech | F=PAT +PAT-2 | PAT-2 phase word | — | P=BQ-10 | B9 |
| DT-180 | tech | F=PAT +PAT-2 | PAT-2 readings | — | P=BQ-10 | B9 |
| DT-181 | tech | F=PAT +PAT-2 | PAT-2 pointer-returning getter | v55 `@` | P=NEWCP-10 | B9 |
| DT-182 | tech | F=PAT +PAT-2 | PAT-2 `NOT ARMED` sentinel | — | P=BQ-10 | B9 |
| DT-183 | tech | F=PAT +PAT-2 | PAT-2 tick report | — | P=BQ-10 | B9 |
| DT-184 | tech | F=NAA | — | generic invariant checking | P=— | — |
| DT-186 | fact | F=NAA | — | a soft interpreter timing figure (the KB states method-call clock count is not documented); XF ungraded | P=— | — |
| DT-187 | tech | F=NAA | — | instrumentation policy | P=— | — |
| DT-190 | trap | F=POU | `preprocessor-overview.yaml` `anti_patterns` | VAR is zeroed at run time (v55:265); an #ifdef-off writer is removed | P=NEWCP-07 + SRC (v55:265) | B5 |
| DT-191 | tech | F=NAA | — | advice | P=— | — |
| DT-192 | trap | F=NAA | — | generic | P=— | — |

#### Part C — pins, streamer, conditional compilation (65)

| DT | kind | form | KB destination | facts → source | whole → proof | batch |
|---|---|---|---|---|---|---|
| DT-193 | fact | F=SHIP | `architecture/decomposition/resource-ownership.yaml` (F-601) | v35 :7560; HW | P=SRC | — |
| DT-194 | fact | F=POU +HUB(S-40) | `resource-ownership.yaml`; `language/spin2/concepts/basic-io.yaml` | v35 :7560 (DIR and OUT OR'd) | P=BQ-04 (Phase S ruled the instance DERIVED) | B9 |
| DT-195 | trap | F=NAA | — | ownership advice, project-specific | P=— | — |
| DT-197 | fact | F=SHIP | DS (F-590) | v55 DEBUG_PIN_TX/RX | P=SRC | — |
| DT-198 | fact | F=SHIP | `pinlow.yaml` (F-600) | v55 pin field | P=SRC | — |
| DT-199 | trap | F=SHIP +POU +HUB(S-41) | shipped in the 7 Spin2 pin methods; whole class: check the PASM2 pin-instruction entries (`dirh` `dirl` `drvh` `drvl` `outh` `outl` `fltl` `flth` and siblings) for the D[10:6] field and a register holding -1 | v35 pin field (ADDPINS) | P=SRC | B6, B8b |
| DT-200 | tech | F=SHIP | pin methods (hazard stated); "validate first" is advice | — | — | — |
| DT-201 | tech | F=POU | `architecture/streamer/pin-capture.yaml` (landing pad: jumper the signal to a spare pin the capture cog owns, count or capture there) | XF-004 (100 ohm jumper to a plain pin; DC check and 137-edge self-test as controls) | P=XF-004 | B6 |
| DT-202 | tech | F=SHIP +PAT-4 | `pin-capture.yaml` `neighbour_capture_composition`; PAT-4 carries the code | v35 WRPIN A/B selectors | P=XF-002 | B7 |
| DT-203 | tech | F=PAT +PAT-4 | `language/spin2/patterns/implementation/spin2_neighbour_pin_observer.yaml` (new); `smart-pin-01110…yaml` `observer_use` (shipped F-604) | v35 %01110; v55 P_COUNT_RISES (:1544), P_MINUS1_A (:1432) | P=XF-002 + NEWCP-11 | B7 |
| DT-204 | fact | F=NAA (open bench item) | — until VO-J-005 runs | whether a selected neighbour reads level or flag when the subject runs a smart-pin mode is VO-J-005 | P=— (VO-J-005, existing) | — |
| DT-206 | trap | F=SHIP | `hardware/edge-standard-module.yaml` (F-602; the check-first advice cut) | v35 selectors; EDGE pin table | P=SRC | — |
| DT-207 | trap | F=SHIP +HUB(S-10) | DS `p62_is_reconfigured_by_every_debug_call` | DBG51 | P=SRC | B8a |
| DT-208 | trap | F=SHIP +HUB(S-42) | `testp.yaml`, `testpn.yaml`, `pinread.yaml`, `rdpin`… (shipped); D-2 fixed first | v35 :7502 | P=SRC | B0, B8b |
| DT-209 | fact | F=SHIP | `smart-pin-00101-transition-output.yaml` `in_flag` | v35 | P=SRC | — |
| DT-210 | trap | F=HUB(S-42) | H-D S-42 (sourced half: on a smart-pin pin IN is the flag; check: a neighbour counter, PAT-4) | v35 :7502 | P=XF-003 | B8b |
| DT-212 | fact | F=SHIP | `smart-pin-11101-sync-serial-receive.yaml` (F-603) | v35 %11101 | P=SRC | — |
| DT-213 | tech | F=NAA | — | (a) shipped then cut by Phase S as DERIVED diagnostic; (b) not certified | P=— | — |
| DT-214 | trap | F=HELD | (`smart-pin-11101` + H-D S-46 once proven) | B = the pin's read state from any source (v35, F-603); the counting consequence was DERIVED; XF-010 UNGRADED | P=PQ then BQ-05 | B10 |
| DT-215 | trap | F=HELD | (as DT-214) | XF-010 | P=PQ then BQ-05 | B10 |
| DT-216 | fact | F=SHIP +HUB(S-46) | `smart-pin-11101` (DIR-low reset shipped); the re-arm half is the existing bench candidate | v35; EF-011, EF-012 | P=BQ-05 for the re-arm half | B9 |
| DT-217 | tech | F=HELD | (depends on DT-215/216) | — | P=PQ then BQ-05 | B10 |
| DT-218 | trap | F=SHIP | `architecture/pin-drive-configuration.yaml` (no change; vocabulary only) | datasheet drive table | P=SRC | — |
| DT-219 | tech | F=NAA | — | advice (Phase S); XF-011 UNGRADED | P=— | — |
| DT-220 | fact | F=SHIP | `boot-rom/sd-card-boot.yaml`, `edge-standard-module.yaml` | ROM listing | P=SRC | — |
| DT-221 | fact | F=SHIP +HUB(S-47) | `edge-standard-module.yaml` (F-610) | ROM listing; EDGE | P=SRC | B8b |
| DT-222 | tech | F=NAA | — | advice; its sourced causes feed S-47 via DT-220/221 | P=— | — |
| DT-223 | fact | F=SHIP | `pin-capture.yaml` | EF-095 | P=EF-095 | — |
| DT-224 | trap | F=SHIP +HUB(S-43) | `pin-capture.yaml` `why_direct_capture_fails` | v35 | P=XF-003 | B8b |
| DT-225 | tech | F=SHIP | `pin-capture.yaml` (F-606); the P_TRANSITION limit waits on VO-J-005 / VO-P-002 | v35; EF-095 | P=XF-003 | — |
| DT-226 | tech | F=SHIP | `pin-capture.yaml` (EF-095 neighbour lane); the busy-smart-pin contrast is VO-J-005 | EF-095 | P=EF-095 | — |
| DT-228 | trap | F=SHIP +HUB(S-44) | `xinit.yaml` ($FFFF perpetual) | v35 XINIT | P=SRC | B8b |
| DT-229 | trap | F=SHIP +HUB(S-44) | `xinit.yaml` (F-608) | v35 XINIT | P=CP-023; the count-0 half P=BQ-06 | B8b |
| DT-230 | trap | F=SHIP | `pin-capture.yaml` `alignment_constraint` | EF-065 | P=EF-065 | — |
| DT-231 | trap | F=POU | `language/spin2/constructs/inline_pasm.yaml` + `language/pasm2/wrfast.yaml` (sourced half: inline PASM may use the FIFO only temporarily; on return Spin2 restores its bytecode stream) | v55 :792-798, :808, :835; INT55 | sourced half P=SRC; the trap whole P=BQ-07 | B6, B9 |
| DT-232 | tech | F=POU | `wrfast.yaml` / `architecture/fifo.yaml` (sourced half: block count 0 writes on through the hub map; a non-zero block count wraps to the start address) | v35 :6672-6675 | P=SRC; the sentinel-bytes advice is not shipped | B6 |
| DT-233 | tech | F=POU | `architecture/streamer/pin-selection.yaml`: drive the pin with DIR high and OUT low (DRVL) before XINIT | v35 :3602, :7499 | P=EF-062 (leg D3: DIR high from OUT = 0) — re-opens a Phase S advice cut, J-10 | B6 |
| DT-234 | trap | F=POU +HUB(S-45) | `pin-selection.yaml` | v35 :3602 | P=BQ-08 | B9 |
| DT-235 | fact | F=SHIP | `xinit.yaml`; `nco-timing.yaml` | v35 | P=SRC | — |
| DT-236 | tech | F=SHIP +HUB(S-09) | streamer `overview.yaml` `debug_interaction` | EF-057 | P=EF-057 | B8a |
| DT-237 | fact | F=NAA | — | generic; the specific traps are DT-238/240/242 | P=— | — |
| DT-238 | trap | F=POU +HUB(S-20) | `preprocessor-overview.yaml` `anti_patterns` | #ifdef semantics | P=NEWCP-04 | B5 |
| DT-240 | fact | F=POU +HUB(S-20) | `preprocessor-overview.yaml` | — | P=NEWCP-04 | B5 |
| DT-241 | tech | F=POU | `preprocessor-overview.yaml` (compare the two binaries before a run); "automate it" is NAA | — | P=NEWCP-04 | B5 |
| DT-242 | trap | F=POU +HUB(S-21) | `preprocessor-overview.yaml`; `pragma-exportdef.yaml` | #define is file-local; `-D` is global (CP-013) | P=NEWCP-04 | B5 |
| DT-244 | tech | F=POU +HUB(S-21) | `preprocessor-overview.yaml` | — | P=NEWCP-06 | B5 |
| DT-246 | fact | F=SHIP | `pragma-exportdef.yaml` | — | P=CP-013 | — |
| DT-247 | tech | F=SHIP | `pragma-exportdef.yaml` | — | P=CP-013 | — |
| DT-249 | fact | F=SHIP | `pragma-exportdef.yaml` | — | P=CP-013 | — |
| DT-250 | tech | F=PAT +PAT-3 | `language/spin2/patterns/implementation/spin2_compiled_feature_mask.yaml` (new) | a child's CON is readable as `obj.CONST` (v55 OBJ) | P=NEWCP-04 | B7 |
| DT-251 | trap | F=NAA | — | generic; the sourced fact is DT-244 | P=— | — |
| DT-252 | tech | F=NAA | — | advice | P=— | — |
| DT-253 | fact | F=SHIP | `preprocessor-overview.yaml` (#ERROR only from taken branches) | — | P=SRC | — |
| DT-258 | fact | F=SHIP | `object-image-dedup.yaml` | — | P=CP-024 | — |
| DT-259 | trap | F=SHIP +HUB(S-23) | `object-image-dedup.yaml` `the_other_silent_trap` | — | P=CP-024 | B8a |
| DT-260 | fact | F=SHIP | `object-image-dedup.yaml` | v55 | P=CP-019 | — |
| DT-261 | fact | F=SHIP | `object-image-dedup.yaml` `singleton_rule` | — | P=CP-024 | — |
| DT-262 | tech | F=SHIP | `object-image-dedup.yaml` (sourced half; advice cut) | — | P=CP-024 | — |
| DT-269 | fact | F=SHIP | `inline_pasm.yaml` | v55:285 | P=CP-020 | — |
| DT-270 | trap | F=SHIP +HUB(S-24) | `inline_pasm.yaml` (F-597); add the error text as an alias | — | P=CP-020 | B8a |
| DT-271 | trap | F=SHIP | `op_oror.yaml` | — | P=SRC | — |
| DT-272 | trap | F=SHIP +HUB(S-24) | `operators.yaml`, `precedence.yaml` (F-598) | — | P=CP-021 | B8a |
| DT-273 | fact | F=SHIP | `op_min.yaml`, `op_max.yaml` | — | P=SRC | — |
| DT-274 | trap | F=SHIP +HUB(S-24) | `case-sensitivity.yaml` (m220; CP-016's home) | — | P=CP-016 | B8a |
| DT-275 | trap | F=NAA | — | refuted (an apostrophe in a debug string compiles; arbiter container check) | P=— | — |

#### Part D — trusting an instrument, time, locks, discipline (38)

| DT | kind | form | KB destination | facts → source | whole → proof | batch |
|---|---|---|---|---|---|---|
| DT-276 | fact | F=NAA | — | generic (CRC catalogue vector) | P=— | — |
| DT-277 | fact | F=NAA | — | generic | P=— | — |
| DT-279 | trap | F=NAA | — | generic self-test design | P=— | — |
| DT-280 | trap | F=NAA | — | generic integrity coverage | P=— | — |
| DT-281 | trap | F=NAA | — | generic | P=— | — |
| DT-282 | trap | F=NAA | — | generic | P=— | — |
| DT-283 | trap | F=NAA | — | generic | P=— | — |
| DT-285 | tech | F=NAA | — | generic | P=— | — |
| DT-286 | tech | F=NAA | — | generic | P=— | — |
| DT-287 | trap | F=NAA | — | generic | P=— | — |
| DT-288 | tech | F=NAA | — | generic | P=— | — |
| DT-289 | fact | F=NAA | — | generic | P=— | — |
| DT-291 | trap | F=HUB(S-31) | H-C S-31 cause "a cog wrote hub at the wrong address" stated as the documented write paths only | v35 cog-hub interface (F-611 `write_paths`) | P=SRC | B8b |
| DT-292 | fact | F=SHIP | F-611 `write_paths` (reduced) | v35; HW | P=SRC | — |
| DT-293 | trap | F=NAA | — | reasoning | P=— | — |
| DT-299 | tech | F=NAA | — | rig method (our EF rigs already do it) | P=— | — |
| DT-301 | trap | F=NAA | — | generic | P=— | — |
| DT-305 | trap | F=NAA | — | generic test assertion | P=— | — |
| DT-306 | tech | F=NAA | — | generic | P=— | — |
| DT-310 | trap | F=NAA | — | generic | P=— | — |
| DT-311 | trap | F=NAA | — | generic; XF-018 UNGRADED, cause not isolated | P=— | — |
| DT-312 | trap | F=SHIP +HUB(S-34) | `waitms.yaml` `limitations` (reframed F-615) | v55:551 | P=SRC | B8b |
| DT-313 | fact | F=SHIP | `waitms.yaml` `ceiling_formula` | v55:551 | P=SRC | — |
| DT-315 | tech | F=SHIP | `waitms.yaml` `long_waits` (prose); the code example stays cut (J-14) | v55 | P=— | — |
| DT-316 | trap | F=HELD | — | XF-016 UNGRADED | P=PQ | B10 |
| DT-318 | tech | F=NAA | — | arbiter: METHOD (documentation practice) | P=— | — |
| DT-319 | trap | F=HELD | — | XF-016 | P=PQ | B10 |
| DT-320 | trap | F=HELD | (the phase shape is already SHIP via XF-001 in `streamer_smartpin_control.yaml`) | XF-016 | P=PQ | B10 |
| DT-323 | fact | F=SHIP | `streamer_smartpin_control.yaml` `write_side` | XF-001 | P=XF-001 | — |
| DT-324 | tech | F=SHIP | same (sweep method cut as advice) | XF-001 | P=XF-001 | — |
| DT-326 | fact | F=SHIP | `cogstop.yaml`, `architecture/locks.yaml` | v35 LOCKS; F-442 | P=SRC | — |
| DT-327 | fact | F=SHIP | `locks.yaml` | F-442 | P=SRC | — |
| DT-328 | trap | F=SHIP +HUB(S-32) | `cogstop.yaml`, `locks.yaml` `the_leak` | F-442; v55 LOCKNEW | P=SRC | B8b |
| DT-329 | tech | F=SHIP | `cogstop.yaml` `best_practices` | — | P=SRC | — |
| DT-330 | fact | F=SHIP | `locks.yaml` | v35 | P=SRC | — |
| DT-331 | trap | F=SHIP +HUB(S-32) | `locknew.yaml` (`< 0`, F-592) | v55; INT55 | P=SRC | B8b |
| DT-332 | fact | F=SHIP +HUB(S-32) | `locknew.yaml`, DS `a_lock` | v55:926 | P=SRC | B8b |
| DT-338 | trap | F=HUB(S-10) | H-A S-10 / H-D S-40 (sourced causes: the debugger reconfigures its TX pin; DIR/OUT are OR'd across cogs) | DS; v35 :7560 | P=SRC | B8a |

#### Part E — the source project's own write-up (52)

| DT | kind | form | KB destination | facts → source | whole → proof | batch |
|---|---|---|---|---|---|---|
| DT-345 | fact | F=SHIP | DS (16 KB region); the figure half is a tool limit | v55:897-901 | P=SRC | — |
| DT-346 | fact | F=SHIP | DS `what_debug_data_counts` | — | P=CP-022 | — |
| DT-347 | trap | F=NAA | technique SHIP (DS) | refuted (loud m151) / tool limit | P=— | — |
| DT-348 | tech | F=PAT +PAT-1 | PAT-1 (labels in DAT) | CP-022 | P=NEWCP-09 | B7 |
| DT-349 | tech | F=PAT +PAT-1 | PAT-1 | DS `over_on_records` | P=NEWCP-09 | B7 |
| DT-350 | tech | F=SHIP | DS `over_on_bytes` ((b) advice cut, F-589 withdrawn) | — | P=CP-022 | — |
| DT-351 | fact | F=SHIP | DS (one record); the atomic-line half is BQ-02 | v55:926; DBG51 | P=BQ-02 | B9 |
| DT-352 | trap | F=POU +HUB(S-20) | `preprocessor-overview.yaml` | — | P=NEWCP-04 | B5 |
| DT-355 | fact | F=SHIP | SC `DEBUG_COGS` | v55:1011 | P=SRC | — |
| DT-356 | fact | F=SHIP | SC; `architecture/debug_interrupt.yaml` | v55:1011, :1068 | P=SRC | — |
| DT-357 | fact | F=SHIP | SC (F-585) | — | P=CP-018 | — |
| DT-358 | trap | F=SHIP | DM `debug_cogs_interaction` | — | P=SRC | — |
| DT-359 | tech | F=SHIP +HUB(S-09) | `pin-capture.yaml` `measurement_hygiene`; SC | — | P=EF-057 | B8a |
| DT-360 | fact | F=SHIP | DM | v55:38, :1027 | P=SRC | — |
| DT-361 | trap | F=SHIP | DM | — | P=CP-015 | — |
| DT-362 | trap | F=SHIP +HUB(S-03) | DS `common_mistakes` | — | P=CP-015 | B8a |
| DT-363 | trap | F=SHIP +HUB(S-03) | DS `common_mistakes` | — | P=CP-015 | B8a |
| DT-364 | trap | F=NAA | — | refuted | P=CP-014 | — |
| DT-365 | fact | F=SHIP +HUB(S-24) | DM (add the error text as an alias) | — | P=CP-025 | B8a |
| DT-366 | fact | F=SHIP +HUB(S-01) | DM `debug_cogs_interaction` | v55 | P=SRC | B8a |
| DT-367 | trap | F=HUB(S-07) pending | (as DT-089) | sources silent (arbiter batch 2) | P=BQ-01 | B9 |
| DT-369 | trap | F=POU +HUB(S-21) | `preprocessor-overview.yaml` (as DT-242) | — | P=NEWCP-04 | B5 |
| DT-370 | fact | F=SHIP | `pragma-exportdef.yaml` (behaviour line 34: "the file holding the pragma is not affected") | — | P=CP-013 | — |
| DT-374 | fact | F=SHIP +HUB(S-31) | F-611 `write_paths` (reduced) | v35 | P=SRC | B8b |
| DT-375 | fact | F=SHIP | `cogspin.yaml`; P2AN006 | INT55 | P=SRC | — |
| DT-376 | trap | F=NAA | — | project-specific; DT-146 carries the trap | P=— | — |
| DT-377 | trap | F=SHIP | P2AN006 | — | (app note) | — |
| DT-378 | tech | F=NAA | — | reporting advice | P=— | — |
| DT-379 | trap | F=SHIP | P2AN006 | — | (app note) | — |
| DT-380 | tech | F=SHIP | P2AN006 (downward scan); the upward-hole half is NAA (DT-154) | — | (app note) | — |
| DT-381 | trap | F=NAA | — | as DT-156 | P=— | — |
| DT-382 | trap | F=POU | as DT-232 (sourced half only) | v35 :6672-6675 | P=SRC | B6 |
| DT-383 | fact | F=SHIP | `object-image-dedup.yaml` | — | P=CP-024 | — |
| DT-384 | trap | F=SHIP +HUB(S-23) | `object-image-dedup.yaml` | — | P=CP-024 | B8a |
| DT-385 | trap | F=SHIP | `object-image-dedup.yaml` | — | P=CP-019 | — |
| DT-386 | fact | F=SHIP | `inline_pasm.yaml` | v55:285 | P=CP-020 | — |
| DT-389 | fact | F=NAA | — | generic | P=— | — |
| DT-390 | fact | F=NAA | — | generic | P=— | — |
| DT-391 | fact | F=NAA | — | generic | P=— | — |
| DT-392 | trap | F=NAA | — | generic | P=— | — |
| DT-393 | tech | F=NAA | — | generic | P=— | — |
| DT-394 | tech | F=NAA | — | generic | P=— | — |
| DT-395 | tech | F=NAA | — | generic | P=— | — |
| DT-402 | tech | F=NAA | — | PNut-Term-TS option (as DT-122) | P=— | — |
| DT-403 | fact | F=SHIP | `cogstop.yaml`, `locks.yaml` | v35 | P=SRC | — |
| DT-404 | trap | F=SHIP | `cogstop.yaml`, `locks.yaml` | F-442 | P=SRC | — |
| DT-405 | fact | F=SHIP | `locks.yaml` (release half) | v35 | P=SRC | — |
| DT-407 | trap | F=SHIP +HUB(S-34) | `waitms.yaml`/`waitus.yaml` ("not documented past the bound", F-615) | v55 | P=BQ-09 (existing candidate) | B8b |
| DT-408 | tech | F=SHIP | `waitms.yaml` `long_waits` prose; code cut stands (J-14) | v55 | P=— | — |
| DT-409 | fact | F=SHIP | `operators.yaml` | v55 | P=SRC | — |
| DT-410 | trap | F=SHIP | `operators.yaml` | — | P=CP-021 | — |
| DT-411 | fact | F=SHIP | SC | v55:1011 | P=CP-018 | — |

### 1.2 Drop-led trap/technique/fact rows (72) — the "tool limits are not KB facts" check

Every row below stays dropped. Where the drop was a **tool limit**, the technique that keeps a
program inside it is routed.

| group | rows | why dropped | technique routed / hub use |
|---|---|---|---|
| tool limit | DT-037, DT-038, DT-047 | figures are the compiler's (overlay, *A bench question must be specific*) | DS `how_you_find_out`, `stay_well_inside`, `reducing_bytes_and_records` (SHIP) |
| tool limit, technique missing | DT-042 | one-record figure is the compiler's | **routed: F=POU** DS `reducing_bytes_and_records`: a statement rejected with m150 is cured by splitting it into statements (or moving its text into DAT, CP-022). P=NEWCP-08 (p11). Batch B4. |
| covered in KB | DT-002, 003, 004, 005, 008, 009, 014, 016, 017, 018, 019, 020, 021, 023, 026, 028, 029, 030, 031, 035, 036, 040, 041, 043, 045, 052, 053, 054, 055, 056, 065, 066, 067, 070, 071, 073, 074, 077, 079, 080, 081, 082, 084, 085, 096, 097, 098, 100, 101, 102, 107 | already in DS/DM/SC | hub use: 003/004/017/018/026/028 → S-01; 071 → S-09; 074 → S-10; 079/080/085 → S-05; 077 → S-32; 014 → S-24 (alias the error text) |
| refuted | DT-010, 048, 094, 106 | source wrong, KB right (CP-014; DS; DM; container) | — |
| version history / fixed tool bug | DT-254, 263, 264, 267, 268 | the KB is always latest; manuals document intent | — |
| project example / tooling | DT-245, 290, 303, 308, 314, 317, 321, 396 | carried by another row or not P2 | — |

### 1.3 Method rows (74) — excluded, with the exceptions that are P2 techniques

Excluded (Stephen's separate idea): DT-001, 049, 050, 051, 059, 063, 075, 099, 104, 109, 110,
115, 120, 126, 128, 142, 170, 185, 188, 189, 205, 211, 227, 243, 248, 256, 257, 265, 266, 278,
284, 294, 295, 296, 297, 298, 300, 302, 304, 307, 309, 322, 325, 333, 334, 335, 336, 337, 339,
340, 341, 342, 343, 344, 371, 372, 373, 387, 388, 397, 398, 399, 400, 401 (64 rows).

**Really P2 techniques (10), listed as the task asks:**

| DT | what makes it a P2 technique | route |
|---|---|---|
| DT-025, DT-239, DT-353, DT-354 | comparing the binaries of two build arms proves a build-time setting reached the image (pnut-ts behaviour) | folded into DT-238/241 POU (`preprocessor-overview.yaml`), P=NEWCP-04 and CP-018 |
| DT-368 | walking the open #IFDEF stack before inserting code | folded into DT-244 POU, P=NEWCP-06 |
| DT-255 | a deliberately violating build must fail: #ERROR stops the build | optional NEWCP (not run): a taken `#error` exits non-zero; KB home `preprocessor-overview.yaml` line 320 already states taken-branch firing |
| DT-406 | LOCKRET on every path | already SHIP (`cogstop.yaml` `best_practices`) |
| DT-034 | do not order cross-cog events by DEBUG timestamp alone | rests on EF-083 (SHIP via F-586); the advice itself is not routed (J-12) |
| DT-090 | take the final reading before stopping anything | rests on BQ-01; not routed until it answers (J-12) |
| DT-196 | an observer must not drive a pin | rests on the DIR/OUT OR rule; PAT-4's code embodies it; the rule as advice is not routed (J-12) |

---

## 2. PITFALL KEY

### 2.1 Survey (what each spelling actually holds)

Commands: `grep -rlE "^anti_patterns:" deliverables/ai/P2 --include=*.yaml` (and the same for each
key); nested forms: `grep -rnE "^\s+(anti_patterns|limitations|gotchas|gotcha|warnings|warning|common_mistakes|pitfalls|common_pitfalls|caveats):"`;
others: `grep -rnoE "^\s*(hazards|failure_modes|common_errors|known_issues|common_issues):"` and
`grep -rlE "^(debugging|troubleshooting):"`.

| key | files | what it holds | item shapes |
|---|---|---|---|
| `anti_patterns` | 31 top-level | (a) silent-wrong code with wrong/correct (LOOKUP/LOOKDOWN family, LOCKNEW/LOCKTRY, WAITMS, GETRND, `??`, CLKFREQ, clock_system, operators, string constants, basic-io, abort, float, pragma-exportdef, include); (b) design, performance or maintainability advice (`timing_operations` busy_waiting "performance", `preprocessor-overview` "maintainability", `object_archetypes`, 5 pattern files' string lists); (c) EF-proven traps (`spin2_latest_wins_mailbox`) | list of `{anti_pattern, severity, description, wrong, correct}`; mapping `name: {wrong, correct, source}`; list of strings |
| `limitations` | 37 top-level + 6 nested | bounds and capability limits: 22 hardware product limits; instruction/feature bounds (`fifo`, `instruction_skipping`, `coginit`, `debug_interrupt` with `workaround`); `waitms`/`waitus` mix a bound, an undocumented past-the-bound statement and a technique (`long_waits`) | list of strings; list of `{limitation, description, workaround}`; mapping |
| `gotchas` | 10 | 7 app-note YAMLs mirror the document's flag boxes (`flag: pitfall/tip/hardware/verify/gap`); `STRUCT`, `typed-pointers` (silent traps with rule + example); async-TX (a community claim measured NOT-OBSERVED) | `{flag, text}`; `name: {description, rule, source, example}`; `{symptom, workaround, attribution, status}` |
| `warnings` | 9 (Spin2 methods: longfill, bytefill, bytemove, longmove, wrpin, wxpin, wypin, cogstop, cogspin) | one-line generic strings; one contradicts its own file (D-3); several unsourced ("Incorrect mode can damage external circuits") | list of strings |
| `common_mistakes` | 5 top-level + 3 nested (fundamentals quick-reference blocks) | mistakes with explanation and fix; some silent, some compile errors | `{mistake, explanation, solution}`; `{mistake, wrong, right}` |
| `pitfalls` | 6 (getct, repeat, case, inline_pasm, method_definition, if_elseif_else) | wrong/correct code mistakes | `{pitfall, description, wrong, correct}` |
| `common_pitfalls` | 2 top-level + 1 nested (pasm-labels) | as `pitfalls`; several are compile errors | `{pitfall, description, wrong, correct}` |
| `caveats` | 2 top-level + 3 nested | qualifiers on an idiom (bounds and side conditions) | list of strings |
| `common_errors` | 2 (skipf_branching, setq_block_ops nested) | field-layout mistakes | mapping of lists / strings |
| `known_issues` | 1 (vscode-pnut-documentation-style) | one compile rejection (CP-009) | list |
| `common_issues` | 1 nested (streamer_smartpin_control `debugging`) | a generic checklist, unsourced | list |
| `debugging` | 13 | per-entry debugging content: limitations, techniques, monitoring tips — generic, often unsourced, two wrong (D-2) | mixed mappings |
| singular `warning` / `gotcha` | 6 nested singletons (edge-standard-module, table_lookup, labels, cordic, boot-pattern-selection; type-propagation `gotcha`) | one trap or bound each | string |
| **not trap meanings** | `cog.yaml` `hazards` (pipeline hazards), `spi-flash-boot.yaml` `failure_modes` (ROM behaviour facts), `best_practices` (advice class) | — | excluded from the conversion (J-19) |

**What the survey shows.** Two meanings recur under every spelling: **(1) a trap** — code or setup
that does not do what it appears to (silently, or by an error the agent will meet), and **(2) a
limitation** — what the thing cannot do or is bounded by. A third thing rides along under several
keys and is neither: **advice** (performance, style, design preference), which Phase S already
classes and does not ship unless a source states it. `limitations` is used almost entirely in
meaning (2); every other spelling is used in meaning (1) or mixed (1)+advice.

### 2.2 Proposal

**Two canonical pitfall keys, because the meanings differ:**

```yaml
anti_patterns:               # code or setup that does not do what it appears to
  - anti_pattern: snake_case_id
    when: "the code or setup"                 # required
    effect: "what actually happens"           # required; sourced or CP/EF-proven
    instead: "the sourced correct form"       # optional; sourced, never advice
    wrong: |                                  # optional code; compile-manifest entry
    correct: |                                # optional code; compile-manifest entry
    error: "verbatim compiler message"        # only when the compiler rejects it
    source: "..."                             # provenance; filtered on delivery

limitations:                 # what the thing cannot do or is bounded by
  - limitation: snake_case_id                 # or a plain string where the file already uses strings
    description: "..."
```

**The trap key is `anti_patterns:`** (Stephen's ruling J-1, 2026-11-04: "so yes, anti_patterns").
It is the term our documents teach: the platform's `antipattern` presentation block and the planned
*P2 Anti-Patterns* manual, whose subject is this same meaning. The key name removes no advice, so
item-level classing still runs on the 31 files already using it; the other ~57 files converge to it.

`debugging:` is kept as a **third, non-pitfall key** for a proven per-entry debugging technique
(Standard A applies to every item); its trap items move to `anti_patterns:`, its bounds to `limitations:`,
and generic unsourced items go through Phase S (J-2).

**Conversion rule per item:** trap → `anti_patterns:`; bound → `limitations:`; advice → Phase S (kept only
where a source states it, under the file's existing `best_practices:`; otherwise removed with a
register entry); wrong claim → fixed in the same pass (KB carve-out). Item-level classing is the
first step of each conversion batch; this map is at key level.

### 2.3 Per-file conversion map (key level)

`→ T` = to `anti_patterns:`; `→ L` = to `limitations:`; `→ T/L` = split per item; `adv?` = holds advice items
Phase S must class; `!` = holds a defect already named in A.6.

| file (under `deliverables/ai/P2/`) | key now | → | note |
|---|---|---|---|
| language/spin2/system-variables/clkfreq.yaml | anti_patterns | T | mapping shape |
| language/spin2/methods/lookdownz.yaml | anti_patterns | T | |
| language/spin2/methods/lookdown.yaml | anti_patterns | T | |
| language/spin2/methods/lookup.yaml | anti_patterns | T | |
| language/spin2/methods/lookupz.yaml | anti_patterns | T | |
| language/spin2/methods/waitms.yaml | anti_patterns; limitations | T; T/L | `periodic_drift` adv?; `past_the_bound` stays L |
| language/spin2/methods/waitus.yaml | limitations | T/L | as waitms |
| language/spin2/methods/float.yaml | anti_patterns | T | adv? (`unnecessary_conversion`) |
| language/spin2/methods/locktry.yaml | anti_patterns | T | |
| language/spin2/methods/getrnd.yaml | anti_patterns | T | adv? (`modulo_bias`) |
| language/spin2/methods/locknew.yaml | anti_patterns | T | |
| language/spin2/methods/getct.yaml | pitfalls | T | |
| language/spin2/methods/cogstop.yaml | warnings | T | |
| language/spin2/methods/cogspin.yaml | warnings | T | ! D-3 |
| language/spin2/methods/longfill.yaml | warnings | T | adv? |
| language/spin2/methods/bytefill.yaml | warnings | T | adv? |
| language/spin2/methods/bytemove.yaml | warnings | T | adv? |
| language/spin2/methods/longmove.yaml | warnings | T | adv? |
| language/spin2/methods/wrpin.yaml | warnings | T | adv? ("can damage external circuits" unsourced) |
| language/spin2/methods/wxpin.yaml | warnings | T | adv? |
| language/spin2/methods/wypin.yaml | warnings | T | adv? |
| language/spin2/methods/coginit.yaml | limitations | L | no change |
| language/spin2/methods/cogatn.yaml | limitations | L | no change |
| language/spin2/operators/op_rand.yaml | anti_patterns | T | |
| language/spin2/operators/typed-pointers.yaml | gotchas | T | |
| language/spin2/constructs/abort.yaml | anti_patterns | T | |
| language/spin2/constructs/repeat.yaml | pitfalls | T | |
| language/spin2/constructs/case.yaml | pitfalls | T | |
| language/spin2/constructs/inline_pasm.yaml | pitfalls | T | |
| language/spin2/constructs/method_definition.yaml | pitfalls | T | |
| language/spin2/constructs/if_elseif_else.yaml | pitfalls | T | |
| language/spin2/keywords/STRUCT.yaml | gotchas | T | |
| language/spin2/special-symbols/double_at.yaml | common_mistakes | T | |
| language/spin2/concepts/floating_point.yaml | anti_patterns | T | |
| language/spin2/concepts/random_generation.yaml | anti_patterns | T | |
| language/spin2/concepts/string_constants.yaml | anti_patterns | T | |
| language/spin2/concepts/basic-io.yaml | anti_patterns | T | |
| language/spin2/concepts/table_lookup.yaml | anti_patterns; nested warning | T | |
| language/spin2/concepts/operators.yaml | anti_patterns | T | |
| language/spin2/concepts/object_archetypes.yaml | anti_patterns | T | adv? |
| language/spin2/concepts/timing_operations.yaml | anti_patterns | T | adv? ("performance") |
| language/spin2/concepts/type-propagation.yaml | common_mistakes; nested gotcha | T | |
| language/spin2/preprocessor/preprocessor-overview.yaml | anti_patterns | T | adv? ("maintainability"); receives DT-190/238/240/241/242/244/352/369 |
| language/spin2/preprocessor/pragma-exportdef.yaml | anti_patterns | T | |
| language/spin2/preprocessor/include.yaml | anti_patterns | T | |
| language/spin2/patterns/implementation/spin2_buffer_management.yaml | anti_patterns | T | strings; adv? |
| language/spin2/patterns/implementation/spin2_cooperative_tasking.yaml | anti_patterns | T | strings; adv? |
| language/spin2/patterns/implementation/spin2_cog_management.yaml | anti_patterns | T | `insufficient_stack` "hard to debug crashes" — same class as D-3 |
| language/spin2/patterns/implementation/spin2_slew_easing_engine.yaml | anti_patterns | T | strings; adv? |
| language/spin2/patterns/implementation/spin2_rate_domain_decoupler.yaml | anti_patterns | T | strings; adv? |
| language/spin2/patterns/implementation/spin2_timing_control.yaml | anti_patterns | T | strings; adv? |
| language/spin2/patterns/implementation/spin2_latest_wins_mailbox.yaml | anti_patterns | T | EF-036..EF-038 traps |
| language/spin2/debug-commands/debug-strategy-guide.yaml | common_mistakes | T | receives DT-013/042/057/064/068/069/116 |
| language/spin2/conventions/vscode-pnut-documentation-style.yaml | known_issues | T | CP-009 |
| language/fundamentals/case-sensitivity.yaml | common_pitfalls; nested common_mistakes | T | |
| language/fundamentals/identifier-rules.yaml | common_pitfalls; nested common_mistakes | T | |
| language/fundamentals/variable-scoping-best-practices.yaml | nested common_mistakes | T | |
| language/fundamentals/pasm-labels.yaml | nested common_pitfalls | T | |
| language/spin2/assembly-directives/file.yaml | limitations | L | no change |
| language/pasm2/idioms/pin-control.yaml | caveats | T/L | |
| language/pasm2/idioms/self-modifying-code.yaml | caveats | T/L | |
| language/pasm2/idioms/scratch-storage.yaml | nested caveats (2) | T/L | |
| language/pasm2/idioms/halt-and-fault-response.yaml | nested caveats | T/L | |
| language/pasm2/concepts/conditional_execution.yaml | common_mistakes; debugging | T | |
| language/pasm2/concepts/cog_hub_execution.yaml | common_mistakes; nested limitations (2) | T; L | |
| language/pasm2/concepts/event_interrupt_config.yaml | limitations | L | no change |
| language/pasm2/concepts/instruction_skipping.yaml | limitations; debugging | L; per item | |
| language/pasm2/concepts/register_indirection.yaml | limitations; debugging | L; per item | |
| language/pasm2/concepts/skipf_branching.yaml | common_errors | T | |
| language/pasm2/concepts/setq_block_ops.yaml | nested limitations; nested common_errors; debugging | L; T | |
| language/pasm2/concepts/rep_instruction.yaml | debugging (nested limitations, techniques) | L; per item | "Add markers…", "Use straight-line code" adv? |
| language/pasm2/concepts/execution_modes.yaml | debugging | per item | generic, adv? |
| language/pasm2/concepts/stack_operations.yaml | debugging | per item | generic, adv? |
| language/pasm2/concepts/streamer_smartpin_control.yaml | debugging (monitoring, common_issues) | per item | ! D-2 |
| language/pasm2/concepts/labels.yaml | nested warning | T | |
| language/spin2/concepts/addressing.yaml | debugging | per item | |
| architecture/clock_system.yaml | anti_patterns; debugging | T; per item | |
| architecture/cordic.yaml | nested warning | T | |
| architecture/hub.yaml | debugging | per item | sourced (v35 DEBUG INTERRUPT) |
| architecture/xbyte_engine.yaml | limitations; debugging | L; per item | |
| architecture/click_module_integration.yaml | debugging | per item | |
| architecture/smart-pins/smart-pin-11110-async-serial-transmit.yaml | gotchas | T | the item is a NOT-OBSERVED community claim; Phase S decides whether it stays |
| architecture/boot-rom/boot-pattern-selection.yaml | nested warning | T | |
| architecture/debug_interrupt.yaml, event_system.yaml, xbyte_engine.yaml, cog_attention.yaml, fifo.yaml, lookup_ram.yaml, system-registers/ptra-register.yaml | limitations | L | no change |
| architecture/multi_resource_management.yaml | nested limitations | L | no change |
| hardware/edge-standard-module.yaml | limitations; nested warning | L; T | |
| hardware/ (21 other files with `limitations`) | limitations | L | no change |
| hardware/p2-hardware-selection-guide.yaml | nested limitations | L | no change |
| application-notes/p2an001…p2an007 (7 files) | gotchas `{flag, text}` | flag pitfall → T; hardware → L or `notes`; tip/verify/gap → `notes` | J-3 |
| guides/quick-queries.yaml | troubleshooting | becomes the pointer to the hubs (§3.5) | ! D-4 |

---

## 3. SYMPTOM HUB

### 3.1 Location (decided after checking how `guides/` is served — A.3)

Four domain files under `deliverables/ai/P2/guides/` (key prefix `p2kbGuide`, served, and added to a
new category `guides.troubleshooting` in `engineering/tools/p2kb-categories.json`):

| hub | file | index key |
|---|---|---|
| H-A | `guides/troubleshooting-debug-output.yaml` | `p2kbGuideTroubleshootingDebugOutput` |
| H-B | `guides/troubleshooting-build-and-preprocessor.yaml` | `p2kbGuideTroubleshootingBuildAndPreprocessor` |
| H-C | `guides/troubleshooting-cogs-memory-locks.yaml` | `p2kbGuideTroubleshootingCogsMemoryLocks` |
| H-D | `guides/troubleshooting-pins-smart-pins-streamer.yaml` | `p2kbGuideTroubleshootingPinsSmartPinsStreamer` |

Why four and not one: `p2kb_get` returns the whole file for an alias hit, so one hub of ~25 symptoms
would hand an agent every domain to find one; why not under `debug-commands/`: half the symptoms are
not about DEBUG. `guides/quick-queries.yaml` `troubleshooting:` becomes the index of the four (J-4).

### 3.2 Schema

```yaml
title: "Troubleshooting: debug output"          # harvested (exact value)
type: guide
category: Troubleshooting
aliases:                                         # every symptom phrase of this file, each owned by this file only
  - "debug prints nothing"
  - ...
description: |
  Symptom-first diagnosis. Find the symptom, run each cause's check, apply its fix.
symptoms:
  - id: S-01
    symptom: "debug() prints nothing"
    causes:
      - cause: "..."        # a sourced or CP/EF-proven statement
        check: "..."        # an action whose reading is sourced or proven (a listing line, a compile result, a register read) — never an inference
        fix: "..."          # sourced
        entry: language/spin2/constants/debug-mask.yaml   # the point-of-use entry (full path)
        source: "..."       # provenance, filtered on delivery
related: [ ...the entries named above... ]
```

### 3.3 Alias ownership rule

One phrase, one file (A.1). A symptom with **one** cause: its phrases are aliases of the
point-of-use entry and the hub lists it with `entry:` only. A symptom with **several** causes: the
hub owns the phrases. Before adding an alias, the batch greps `deliverables/ai/P2` for it
(`grep -rni '^  - "<phrase>"'`); the phrases proposed below returned no hit on 2026-10-15 for
`debug prints nothing`, `no debug output`, `board hangs`, `memory corruption`, `hub ram corrupted`,
`waitxfi hangs`, `pin stuck high`, `cog stops by itself`, `locknew fails`, `locknew returns -1`,
`waitms returns immediately`, `debug timestamps out of order`, `binaries identical`,
`-D flag has no effect`.

### 3.4 Symptom list (drawn from the ledger; aliases in an agent's words)

| id | hub | symptom | aliases (owner) | causes → entry (ledger rows) |
|---|---|---|---|---|
| S-01 | H-A | debug() prints nothing | "debug prints nothing", "no debug output", "debug() not printing", "debug output missing", "debug statement does nothing" (H-A) | built without -d (DT-003); the object sets DEBUG_DISABLE (DT-068 → SC); bit N clear in that object's DEBUG_MASK (DT-026/027/366 → DM); the cog's bit clear in DEBUG_COGS (DT-017/018 → SC); RCFAST/RCSLOW clock (KB-resident, DS `clock_source`, J-6); TX pin not 62 for windows (DT-028 → SC). Check: `pnut-ts -d -l` listing `DEBUG records` (NEWCP-05, CP-014, CP-015) |
| S-02 | H-A | a child object's debug output is missing | "child object debug not printing", "driver debug output missing", "included object debug silent" (H-A) | the child's own mask (DT-013 → DS, NEWCP-02, CP-014); the child's DEBUG_DISABLE (DT-068) |
| S-03 | H-A | an object with DEBUG_MASK = 0 still prints or still uses the budget | DS owns "object has DEBUG_MASK = 0 but still prints" | plain debug() ignores the mask (DT-006/007/362/363 → DS, CP-015) |
| S-04 | H-A | "DEBUG data is too long" / too many records | DS owns "DEBUG data is too long", "too many records", "record exceeds" | DS techniques (SHIP); a debug() that never runs still counts (DT-064, NEWCP-03); split an over-long statement (DT-042, NEWCP-08) |
| S-05 | H-A | debug output is garbage | "debug output is garbage", "garbled debug output", "random characters in debug output" (H-A); DS keeps its clock-specific alias | clock changed without CLKSET (DT-085/086 → DS, v55:28); a program's own serial on the debug pins (DT-079/080 → DS `cog_start_traffic`); something else configured on the TX pin (DT-074) |
| S-06 | H-A | DEBUG_TIMESTAMP lines out of time order | "debug timestamps out of order", "DEBUG_TIMESTAMP wrong", "timestamps jump backwards" (SC, single cause) | stamp from the sending cog's own counter; E3 stale window (DT-032/033 → SC, EF-083) |
| S-07 | H-A | debug output stops / the board looks hung | "board hangs", "P2 appears hung", "program stops printing", "debug output stops", "no more output" (H-A) | top method returned or aborted (DT-139 → cogspin, abort.yaml); ISR retrigger lost after DEBUG (DS); one LOCK[15]-shared TX path for every cog (DT-129); cog stopped mid-statement (DT-089/367, after BQ-01). Check: progress observer (PAT-2, after BQ-10) |
| S-08 | H-A | the last debug line is missing from the log | "last debug line missing", "debug output cut off at the end", "final debug line truncated" (H-A) | the P2 side completes each statement before returning (DT-116 → DS, A.5); cog stopped mid-statement (after BQ-01) |
| S-09 | H-A | the program behaves differently with -d | "works without debug fails with debug", "program changes when built with -d", "measurements differ in debug build", "streamer capture corrupted in debug build" (H-A) | top 16 KB taken (DT-070/071/072 → DS `hub_memory`); one fewer lock (DT-077 → DS); debug pins taken (DT-073/074); a debug interrupt per enabled cog at COGINIT and at each DEBUG (DT-087, v55); streamer measurements disturbed (DT-024/236/359, EF-057); ISR retrigger (DS) |
| S-10 | H-A | a smart pin or counter on the debug TX pin reads dead | DS owns new alias "counter on P62 reads zero" | reconfigured by every debug() (DT-076/207/338 → DS) |
| S-20 | H-B | two build variants give the same binary / a -D flag does nothing | "binaries identical", "-D flag has no effect", "build flag does nothing", "define has no effect" (H-B) | the flag guards nothing on the path (DT-238/240/352 → preprocessor-overview, NEWCP-04); check: compare the two binaries (DT-241) |
| S-21 | H-B | code I added is not in the program | "code not compiled", "ifdef code missing", "added code has no effect" (H-B) | inside an #ifdef branch that is off (DT-244, NEWCP-06); definition-only flag (DT-242/369, NEWCP-04); `#pragma exportdef` not seen by its own file (DT-246 → pragma-exportdef, CP-013) |
| S-22 | H-B | a getter always returns zero | "getter returns zero", "counter always zero" (preprocessor-overview, single cause) | its only writer is under a flag that is off (DT-190, NEWCP-07) |
| S-23 | H-B | an object meant to be one copy has two | object-image-dedup owns "singleton split", "two copies of object" | override on one sibling forks the DAT (DT-259/384, CP-024) |
| S-24 | H-B | compiler errors from this ledger | each verbatim error text aliased at its home: "Local variable must be LONG and within first 16 longs" (inline_pasm), "DEBUG_MASK symbol must be defined for DEBUG[0..31] usage" (DM), "Expected a unique parameter name" (case-sensitivity), "record exceeds" (DS, exists); "Expected end of line (m281)" has several causes → H-B | CP-020, CP-025, CP-016, CP-021, CP-003, CP-009 (DT-014/270/272/274/365) |
| S-30 | H-C | a cog stopped by itself | "cog stops by itself", "cog stopped unexpectedly", "my cog quit" (H-C) | top method returned → TASKSTOP(-1) (DT-139 → cogspin, taskspin); uncaught ABORT (abort.yaml) |
| S-31 | H-C | unrelated variables are corrupted | "memory corruption", "hub ram corrupted", "variables change by themselves", "data overwritten" (H-C) | stack overflow, never detected (DT-143 → cogspin, P2AN006); the documented hub write paths (DT-291/292/374, F-611); cogspin(-1) starts two cogs on one stack (DT-175); buffer in the top 16 KB under -d (S-09) |
| S-32 | H-C | LOCKNEW returns a negative value | "locknew fails", "locknew returns -1", "no locks available" (H-C) | lock numbers leaked by stopping cogs (DT-328 → cogstop, locks); LOCK[15] allocated by the debugger (DT-332); check `< 0` (DT-331 → locknew) |
| S-33 | H-C | two cogs run the same method | cogspin owns "cogspin -1 starts two cogs" | DT-175 → cogspin `not_an_input` |
| S-34 | H-C | WAITMS returns too soon | waitms owns "waitms returns immediately", "waitms too short" | past the $8000_0000-clock bound (DT-312/407 → waitms, waitus) |
| S-40 | H-D | a pin stays driven / another cog cannot release it | "pin stuck high", "pin won't go low", "pin driven by another cog" (H-D) | DIR/OUT OR'd across cogs (DT-193, then DT-194 after BQ-04); the debugger's TX pin (DT-338) |
| S-41 | H-D | a pin call with -1 affects half the chip | "pin -1 affects 32 pins", "pinhigh -1 toggles many pins" (H-D: seven method files carry the same text) | DT-199 → pin methods (+ PASM2 whole class) |
| S-42 | H-D | TESTP / IN reports completions, not edges | "TESTP reads wrong on smart pin", "IN is not the pin level", "edge count wrong with smart pin" (H-D) | smart-pin IN is the flag (DT-208/210 → testp, pinread, rdpin; XF-003); check: a neighbour counter (PAT-4) |
| S-43 | H-D | a streamer capture records flags, not traffic | pin-capture owns "streamer capture shows ready pulses" | DT-224 → pin-capture |
| S-44 | H-D | WAITXFI never returns | "waitxfi hangs", "streamer never finishes", "xinit never completes" (H-D) | count above 16 bits spills (DT-229, CP-023); $FFFF is perpetual (DT-228); count 0 (after BQ-06) |
| S-45 | H-D | streamer output does not appear on the pin | "streamer output not on pin", "x_pins_on no output" (H-D) | DIR low (DT-233, EF-062); stale OUT high (DT-234, after BQ-08) |
| S-46 | H-D | sync-serial receive misframed after a streamer burst | "sync serial rx misaligned", "smart pin receive misframed" (H-D) | DIR-low reset (DT-216, SHIP); the rest after BQ-05 / XF-010 |
| S-47 | H-D | a device on P58-P61 misbehaves after reset | edge-standard-module owns "P59 pulses at reset", "flash pins toggle at reset" | ROM booter drives the pins (DT-220/221, F-610) |

28 symptoms (S-01..S-10, S-20..S-24, S-30..S-34, S-40..S-47); every phrase is the plan's proposal for
the batch to collision-check.

### 3.5 quick-queries

`guides/quick-queries.yaml` `troubleshooting:` is rewritten in B8a as four question entries pointing
at the hub keys, its unsourced checklist items removed (D-4), and its "why is my serial not
working" entry pointed at H-A S-05/H-D.

---

## 4. PATTERN ENTRIES

Each lives under `language/spin2/patterns/implementation/` with `pattern_id`, `aliases:` (patterns
today carry none; `pattern_id` is harvested), `when_use`, `implementation`, `anti_patterns`, `resources`,
`related`, and a compile-manifest entry under
`engineering/tools/validation/kb-compile-manifest/language/spin2/patterns/implementation/`
(legality only); it is listed in `pattern-index.yaml`. Every claim in the entry is sourced; the code
is the probe already compiled (or its cleaned form, re-compiled before commit).

| id | file | code it must carry | compile proof (pnut-ts -d) | whole proven by | rows |
|---|---|---|---|---|---|
| PAT-1 | `spin2_debug_line_buffer.yaml` | DAT line buffer + DAT labels; `putStr`/`putDec` that never write past `LINE_MAX`; one `debug(zstr_(@line))` (probe p07) | `pnut-ts -d -l …/p07/linebuf.spin2` → exit 0, `DEBUG records: 1`, `DEBUG data: 3` | CP-022 + NEWCP-09; ZSTR_ output documented (v55) | DT-058, 060, 061, 348, 349 |
| PAT-2 | `spin2_progress_observer.yaml` | worker publishes a heartbeat long, a phase word + argument, an in-flight triple; an observer cog (cog 0) that does hub reads only, times out, prints `NOT ARMED` when unregistered; reporting park at the end of the base method (probe p06) | `pnut-ts -d -l …/p06/observer.spin2` → exit 0, `DEBUG records: 2` | **BQ-10** (no source states the technique; CP proves legality only) | DT-132, 133, 134, 140, 141, 165, 166, 167, 168, 178, 179, 180, 181, 182, 183 |
| PAT-3 | `spin2_compiled_feature_mask.yaml` | a child publishes `COMPILED_FEATURES` built under its #ifdefs (an in-file `#define` for an implied flag); the parent prints `d.COMPILED_FEATURES` in its run header; a note to compare the binaries of two arms (probe p04) | `pnut-ts -d -l -o arm-full -D FEAT_FULL …/p04/top.spin2` → listing `OBJ_CON_INT 00000003 COMPILED_FEATURES`; `cmp arm-none arm-unused` → exit 0 (identical); `cmp -l arm-none arm-trace` → differs | NEWCP-04 (LAYOUT: the effect is a compile effect) | DT-250 (+ DT-238/240/242 at POU) |
| PAT-4 | `spin2_neighbour_pin_observer.yaml` | `pinstart(OBSERVER, …, 0, 0)` with mode `P_COUNT_RISES` bitwise-OR `P_MINUS1_A` and no P_OE, then `waitms`, `rdpin`, `pinclear` (probe p08) | `pnut-ts -d -l …/p08/neighbour.spin2` → exit 0 | XF-002 (CONFIRMED, matched control) + v35 %01110 | DT-202, 203 |

PAT-4 note: p08 composes the mode with `|` (bitwise OR); the KB's convention for smart-pin mode
composition (EF-054/EF-065: `+` breaks overlapping fields, OR is safe) is checked against the
entry before commit.

---

## 5. STANDARD A

### 5.1 Sourcing per row

The per-row sourcing is the **facts → source** and **whole → proof** columns of §1.1. Search
discipline for every row that ends in BQ or NAA-for-silence: Spin2 v55 text, v35 text, the
Hardware Manual, the P2 Edge guide, INT55, DBG51, the ROM booter listing, the Chip Gracey
clarifications, the EF and XF ledgers, and `VERIFICATION-OPPORTUNITIES.md` — each BQ below records
its terms, files and a control hit. Rows marked `P=—` claim nothing for the KB.

### 5.2 New compile proofs (probes run; the arbiter registers them)

All in `/tmp/claude-1000/-workspaces-P2-Knowledge-Base/58bf89f5-1df4-42ec-ac73-ca38d9041ea1/scratchpad/`
(`$S` below), pnut-ts v1.55.8, build 9/19/2026. Note: `-o` takes a basename; an absolute path is
joined to the source directory (ENOENT), so the arms below use bare names.

| id | rows | command(s) | result |
|---|---|---|---|
| NEWCP-01 | DT-012 | `pnut-ts -d -l $S/p01/parent-or.spin2` · `pnut-ts -d -l $S/p01/parent-lit.spin2` · `pnut-ts -d -l $S/p01/parent-paren.spin2` · `cmp $S/p01/parent-or.bin $S/p01/parent-lit.bin` | all exit 0; each `DEBUG records: 3`; cmp exit 0 (identical) — the OR-expression override works (LEGALITY) |
| NEWCP-02 | DT-013 | `pnut-ts -d -l -D CHILD_DEBUG $S/p02/parent.spin2` then `pnut-ts -d -l $S/p02/parent.spin2` | `DEBUG records: 2` with the symbol, `1` without (LAYOUT) |
| NEWCP-03 | DT-064 | `pnut-ts -d -l $S/p03/early-return.spin2` · `…/p03/uncalled.spin2` · `…/p03/ifdef-gated.spin2` | early return: 1 record, 75 bytes; never called: 1 record, 75 bytes; #ifdef-gated: 0, 0 (LAYOUT) |
| NEWCP-04 | DT-238/240/241/242/250/352/369 | `pnut-ts -d -l -o arm-none $S/p04/top.spin2` · `-o arm-unused -D FEAT_UNUSED` · `-o arm-trace -D FEAT_TRACE` · `-o arm-full -D FEAT_FULL` · `cmp $S/p04/arm-none $S/p04/arm-unused` · `cmp -l $S/p04/arm-none $S/p04/arm-trace` · `grep -n "COMPILED_FEATURES" $S/p04/top.lst` | unused arm byte-identical (cmp exit 0); trace arm differs; full arm listing `00000003 COMPILED_FEATURES` (LAYOUT) |
| NEWCP-05 | DT-068/069 | `pnut-ts -d -l $S/p05/top.spin2` | `DEBUG records: 1` — the parent's; the DEBUG_DISABLE child's statement compiled to nothing (LAYOUT) |
| NEWCP-06 | DT-105/244 | `pnut-ts -d -l $S/p09/gated.spin2` · `pnut-ts -d -l -o gated-arm -D TRACE_ARM $S/p09/gated.spin2` | 0 records without the symbol; 1 with it (channel-1 statement, bit clear, absent in both) (LAYOUT) |
| NEWCP-07 | DT-190 | `pnut-ts -d -l $S/p10/tier.spin2` | exit 0: the getter compiles with its only writer removed (LEGALITY); the zero comes from v55:265 |
| NEWCP-08 | DT-042 | `pnut-ts -d -l $S/p11/oneline.spin2` · `pnut-ts -d -l $S/p11/split.spin2` | one statement: exit 1, `DEBUG data is too long: record exceeds … bytes (m150)`; split: exit 0 (LEGALITY; the figure is never carried) |
| NEWCP-09 | PAT-1 | `pnut-ts -d -l $S/p07/linebuf.spin2` | exit 0; 1 record; DEBUG data 3 bytes (LAYOUT) |
| NEWCP-10 | PAT-2 | `pnut-ts -d -l $S/p06/observer.spin2` | exit 0; 2 records (LEGALITY only) |
| NEWCP-11 | PAT-4 | `pnut-ts -d -l $S/p08/neighbour.spin2` | exit 0 (LEGALITY only) |

The probes are scratch; at execution the arbiter copies the kept sources into
`compiler-verification/proofs/` under the allocated CP numbers and re-runs them there.

### 5.3 Bench questions for Stephen (only after the search was silent)

| id | the P2 question | rows | search record (terms · files · control hit) |
|---|---|---|---|
| BQ-01 | In a -d build, a cog is stopped with COGSTOP while it is inside a DEBUG statement (holding LOCK[15], transmitting). Is the line in flight cut, and does the next DEBUG from another cog print whole? (= the arbiter's DT-367 bench candidate) | DT-089, 367; DT-090 | LOCK[15], DLY, COGSTOP, lock release · v55 DEBUG (:926, :1003, :1068), DBG51 (`locktry #15`, `lockrel #15`, `debug_done`), v35 LOCKS · control: DBG51 `debug_done` busy wait found |
| BQ-02 | Two cogs issue long DEBUG statements continuously. Is any line ever split by the other cog's output? | DT-057, 351 | interleav*, LOCK[15], time-share · v55, v35, DBG51, Chip clarifications · no hit for "interleav"; control: v55:926 time-share sentence found |
| BQ-03 | A guard long placed immediately before a cog's stack buffer, the cog recursing past the top: does the before-guard stay intact while an after-guard is overwritten? | DT-146 | stack, grow, guard · v55, INT55, cogspin.yaml, P2AN006 · control: growth direction stated (INT55 via cogspin `growth`); the before-guard outcome not stated |
| BQ-04 | Cog A sets a pin's DIR high; cog B executes DIRL on the same pin. Does the pin stay driven? | DT-194 | OR'd, DIR, output enable · v35 (:7499, :7560), HW · control: v35:7560 "in the same way DIR and OUT bits are OR'd" found; the two-cog outcome is an instance (Phase S: DERIVED) |
| BQ-05 | After a sync-serial receive pin is clocked by a burst that is not a multiple of its word size, which operations restore word alignment — DIR-low reset only, or also WXPIN/WYPIN re-arm or AKPIN? (existing candidate, after XF-010 records) | DT-215, 216, 217 (and DT-214) | arbiter batch 2: SOURCES-SILENT; control: the DIR-low reset passage |
| BQ-06 | XINIT with a count of 0: does WAITXFI return? (existing candidate) | DT-229 | arbiter batch 2: SOURCES-SILENT; control: a short transfer |
| BQ-07 | A streamer capture started with WRFAST + XINIT in inline PASM, the PASM returning to Spin2 before WAITXFI: does the capture complete into hub? | DT-231 | FIFO, temporarily, restore, WRFAST, hub exec · v55 (:787, :792-798, :808, :835), INT55 (`_ret_ rdfast`), v35 FIFO/hub exec · control: v55:808 "Use the FIFO temporarily" found; the in-flight outcome not stated |
| BQ-08 | A pin left with OUT = 1 and DIR high, then driven by streamer output (X_PINS_ON): does it read constant high? (one more leg, D4, on EF-062's rig) | DT-234 | OR, OUTB/OUTA, X_PINS_ON · v35 (:3602), EF-062 · control: v35:3602 found; EF-062's legs started from OUT = 0 |
| BQ-09 | WAITMS/WAITUS past the $8000_0000-clock bound: what does the call do? (existing candidate, DT-407) | DT-407 | arbiter batch 2 (F-615) · XF-015 UNGRADED |
| BQ-10 | Progress-observer rig: a worker increments a hub heartbeat and phase word; cog 0 observes. Pre-registered legs: running → count advances; worker COGSTOPped → count frozen while the observer ticks; instrument unregistered → `NOT ARMED`; control: a known number of increments read back exactly | PAT-2 rows | heartbeat, watchdog, phase · v55, v35, HW, Chip clarifications · no hit; control: EF-037 (single-long publish) found |

Partner-held rows (P=PQ) need no new request: the records for XF-005..XF-018 were requested once
in «#429».

---

## 6. EXECUTION BATCHES

Rules for every batch: register first (the arbiter allocates F-numbers and CP numbers at
execution); new CPs registered before the YAML that cites them; collision-check every new alias;
re-compile every code block (compile manifest); Phase S (an independent classing of every added
statement) before the commit; search `deliverables/ai/P2` wider than the target and fix the class
in the same pass; no release without Stephen.

| batch | content | ledger rows | gate before it starts |
|---|---|---|---|
| B0 | Defects D-1 (SC DEBUG_DISABLE "Globally"), D-2 (streamer_smartpin_control TESTP / lock[15]), D-3 (cogspin "causes crashes"; the same class in `spin2_cog_management` `insufficient_stack`) | DT-143, DT-208 (homes) | none — served now |
| B1a | Pitfall-key conversion: `language/spin2/methods`, `operators`, `constructs`, `keywords`, `special-symbols`, `system-variables` (§2.3) | — (files ≈ 30) | J-1 (ruled 2026-11-04) |
| B1b | Conversion: `language/spin2/concepts`, `preprocessor`, `patterns`, `debug-commands`, `conventions`, `language/fundamentals` | — (files ≈ 27) | J-1 |
| B1c | Conversion: `language/pasm2`, `architecture`, `hardware` nested singletons, app notes (J-3), `debugging:` blocks | — (files ≈ 30) | J-1, J-2, J-3 |
| B4 | Debug POU: DS, DM, SC, `clkset.yaml`, `method_definition.yaml`; NEWCP-01/02/03/05/06/08 | DT-012, 013, 042, 064, 068, 069, 086, 105, 111, 116 (10) | NEWCPs registered |
| B5 | Preprocessor POU; NEWCP-04/07 | DT-190, 238, 240, 241, 242, 244, 352, 369 (8) | NEWCPs registered |
| B6 | Cogs / pins / streamer POU | DT-139 (taskspin), 199 (PASM2 class), 201, 231 (sourced half), 232, 382, 233 (7) | J-10 for DT-233 |
| B7 | Patterns PAT-1, PAT-3, PAT-4 + compile manifest + `pattern-index.yaml`; NEWCP-09/11 | DT-058, 060, 061, 348, 349, 250, 202, 203 (8) | NEWCPs registered |
| B8a | Hubs H-A, H-B; quick-queries rewrite (D-4); category `guides.troubleshooting`; aliases at POU homes | DT-006, 007, 024, 027, 033, 072, 076, 087, 127, 129, 207, 236, 259, 270, 272, 274, 338, 359, 362, 363, 365, 366, 384 (23) | B4, B5 done (the hubs point at their text) |
| B8b | Hubs H-C, H-D | DT-139, 143, 175, 199, 208, 210, 221, 224, 228, 229, 291, 312, 328, 331, 332, 374, 407 (17) | B6 done |
| B9 | Bench-dependent rows, each only after its BQ answers: PAT-2 (BQ-10); DT-057/351 (BQ-02); DT-089/367 (BQ-01); DT-146 (BQ-03); DT-194 (BQ-04); DT-231 whole (BQ-07); DT-234 (BQ-08); DT-216 re-arm (BQ-05); DT-229 count 0 (BQ-06) | 25 rows | Stephen's answers |
| B10 | Partner-dependent rows, after XF grading | DT-088, 112, 113, 114, 214, 215, 217, 316, 319, 320 (10) | XF records graded |

Order: B0 → (J-1/J-2/J-3 ruled) → B1a → B1b → B1c → B4 → B5 → B6 → B7 → B8a → B8b; B9 and B10 as
their blockers clear. New traps written in B4-B7 use the canonical key from the start.

---

## 7. Judgement calls Stephen might rule differently

| id | the call this plan makes | the alternative |
|---|---|---|
| J-1 | canonical trap key `anti_patterns:`; the other ~57 files converge to it | `traps:` (rejected: it would give one concept two names across the KB and the manuals) |
| J-2 | three keys: `anti_patterns`, `limitations`, and `debugging` kept for proven per-entry techniques | two keys only; `debugging` items moved to `anti_patterns`/`limitations` or removed |
| J-3 | app-note `gotchas {flag}`: pitfall → `anti_patterns`, hardware → `limitations` or `notes`, tip/verify/gap → `notes` | leave app-note YAMLs as document mirrors until each app note's next revision (a carve-out expiring then) |
| J-4 | four domain hub files under `guides/`, quick-queries as their index | one hub file; or hubs under `language/spin2/debug-commands/` |
| J-5 | alias ownership: single-cause symptom phrases live at the point-of-use entry, multi-cause at the hub | every symptom phrase at the hub (needs alias removal from DS and others to avoid arrays) |
| J-6 | a ledger-drawn symptom may list KB-resident sourced causes the ledger never named (RCFAST clock under S-01) | ledger causes only |
| J-7 | a hub `check` must be an action with a sourced or proven reading; diagnostic inference is excluded | allow labelled reasoning in `check` |
| J-8 | a Parallax statement that itself states a technique's effect proves the whole (P=SRC), e.g. CLKSET keeps the debugger current (v55:28) | require a CP or EF for every technique |
| J-9 | DBG51 + v35 settle DT-116/117 (a DEBUG statement returns after its last stop bit): P2-side loss NAA, counter-fact shipped | keep DT-116 open as a bench question (XF-006 paired run) |
| J-10 | re-open a Phase S advice cut when an EF now proves the whole: DT-233 DRVL-before-XINIT via EF-062 leg D3 | Phase S cuts stay cut |
| J-11 | host-tool rows (PNut-Term-TS `-u`, terminal encoding, grep, harness) and generic engineering rows (CRC/integrity, test assertions) are NAA | a KB home for host-tool debugging (e.g. `tools/`) |
| J-12 | method exceptions: 025/239/353/354/368 folded into POU as compile-proven checks; 255 optional CP; 034/090/196 listed, not routed | route 034/090/196 as POU advice once their facts are proven |
| J-13 | PAT-2 (progress observer) goes to the bench (BQ-10) | rule it NAA as generic multi-cog instrumentation, or accept NEWCP-10 + EF-036..039 as enough |
| J-14 | DT-315/408 long-wait loop code stays cut (Phase S); no bench question | ship it as a pattern under a BQ |
| J-15 | DT-146/194/234 "a direct instance of a stated rule" go to the bench (Phase S: DERIVED) | treat a single-step instance of a stated formula as sourced |
| J-16 | DT-201 landing pad proven by XF-004 (the count is not a KB fact; the technique is) | not proven until an EF |
| J-17 | B0 defects fixed before the key ruling | fold them into B1/B4 |
| J-18 | counting: drop-led = destination cell begins "drop" (82 rows) | the arbiter's narrower drop-only tally (~46) |
| J-19 | `hazards` (cog.yaml), `failure_modes` (spi-flash-boot.yaml) and `best_practices` are outside the conversion | include `best_practices` (advice class) in a Phase S sweep |
| J-20 | DT-012's refutation registered as a CP although no KB text changes | no CP for a refutation with no KB home |

---

## 8. Arbiter rulings (2026-10-15, after verification)

**Verified by the arbiter before these rulings:** every one of the 411 ledger rows appears in the
plan (§1.1 table rows plus the bare numbers of §1.2/§1.3, compared against the ledger's DT ids);
the form counts of §1.1 re-counted (POU 22 · HUB 9 · PAT 22 · SHIP 119 · HELD 10 · NAA 83 = 265);
probe p03 re-run (`early-return` 1 record / 75 bytes, `ifdef-gated` 0 / 0); D-1 confirmed
(SC says "Globally disables ALL", Spin2 v55 says "in the file/object"); the DT-116/117 refutation
confirmed (Spin2_debugger v51 `debug_done` waits on the TX busy flag; the silicon document says
RDPIN WC returns busy); XF-004 is CONFIRMED.

| call | ruling | on what |
|---|---|---|
| J-1 | **Stephen ruled 2026-11-04: `anti_patterns:`** | the term the documents teach; naming a key across ~88 files |
| J-2 | accepted | `debugging:` holds proven techniques under Standard A; a third meaning, not a third spelling |
| J-3 | accepted | KB carve-out: a wrong-key item is fixed in the pass; the `flag` survives as the item's class |
| J-4 | accepted | `p2kb_get` returns the whole file per hit; four domains keep a hit small |
| J-5 | accepted | one phrase, one owner; the single-cause home is where the agent writes the code |
| J-6 | accepted | a sourced cause is not less true for being absent from the lead |
| J-7 | accepted | a `check` whose reading is inferred is DERIVED (overlay, *The chain runs one way*) |
| J-8 | accepted | a Parallax statement of the effect is a sourced fact; Standard A's proof is needed only where no source states the whole |
| J-9 | accepted | verified above |
| J-10 | accepted | Standard A: an EF proving the whole is what admits a technique |
| J-11 | accepted | PNut-Term-TS is an ISP-only document, not KB family; generic engineering rows are the method class Stephen set aside |
| J-12 | accepted | 034/090/196 stay listed until their facts are proven |
| J-13 | accepted | no source states the technique; legality is not the whole |
| J-14 | accepted | Phase S cut stands; no new source |
| J-15 | accepted | Phase S ruled the single-step instances DERIVED; consistent with the overlay |
| J-16 | accepted | XF-004 CONFIRMED; the XF tier is equal to EF |
| J-17 | accepted | served defects are fixed at the next opportunity, which is now |
| J-18 | accepted | the wider count loses nothing |
| J-19 | accepted | not trap meanings; `best_practices` is reached by each batch's Phase S where a batch touches it |
| J-20 | accepted | a refutation recorded as a proof stops the claim returning |

**Execution note.** The probes (p01–p11) were run in a session scratchpad, which is not durable;
their 20 `.spin2` sources are kept beside this plan in `toolbox-probes/pNN/` (the `$S/pNN/` paths
of §5.2). Each NEWCP is registered by copying its probe into
`engineering/ingestion/external-sources/compiler-verification/proofs/` under its CP number and
re-compiling it there from the repository root, before the YAML that cites it.
