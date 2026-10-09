# P2KB close-out study

**Status:** SCOPE AGREED by Stephen 2026-10-08 (group E dropped at his word). Reading has not
started.
**Skill:** central `study`. The hand-off seeds the close-out sprint plan (`sprint-plan`).
**Element:** `yaml:p2kb`.

## Why this study exists

KB releases have been frequent (40 since 2026-06-13), and every one has shipped with known work
still open. Two causes, both addressed in process on 2026-10-08:

- **We set seen defects aside.** On 2026-10-07, F-548 to F-551 were each logged mid-fix in a file
  that was already open. Doctrine now says: *On the KB, what we see wrong we fix in the same pass,
  and we search wider than the target.*
- **Fixes we only partly made came back as new findings.** Five of the seven defects in the
  2026-10-07 pre-release audit were siblings of fixes made that same day.

Stephen's ordering (2026-10-08):

1. Research every YAML change first.
2. That research yields the bench questions.
3. The bench questions yield the test files.
4. Run the bench.
5. Processing the results closes planning.
6. Only then task the changes, with every answer in hand.

Every task then applies a known answer, so no task has to investigate.

---

## 1. Scope — AGREED 2026-10-08

**The question.** For every open YAML-scoped item, what exactly must change in
`deliverables/ai/P2/`, and on what authority? The authority is an ingested source (`file:line`)
or a bench result (EF/XF).

### In scope

| Group | Items | What the study produces |
|---|---|---|
| **A. Decided 2026-10-08** | F-359 · F-375 · F-398 · F-381 · F-547 (the operator-ingestion audit) · ENH-03 | A change spec per the recorded decision (register notes "DECIDED by Stephen 2026-10-08") |
| **B. Open YAML corrections** | F-550 · F-551 · F-548 · F-545 · F-562 · F-560 · F-392 · F-386 (the ten mode pages) · F-372 · F-354 (three board facts) · F-336 · F-337 (remainder) · F-561 (the YAML companion half only) | A change spec, a bench question, or a blocker that is not a bench question |
| **C. Open knowledge gaps** (`KNOWLEDGE-GAPS.md`) | G-002 · G-004 · G-005 · G-006 · G-009 · G-012 · G-015 · G-019 · G-020 · G-022 · G-023 · G-024 · G-025 · G-027 · G-028 · G-029 | Each is answered from the sources, becomes a bench question, or is declared out of reach (e.g. it needs a document we do not hold) |
| **D. Bench queue already filed** | VO-J-005 (written, not run) · VO-J-006 (not written) · VO-J-028 (not written) | Each is re-checked against the sources first (see the bench rule below), then the test is written or the question retired |
| ~~E. Field-report reconciliation~~ | **Dropped 2026-10-08.** Stephen: *"field reports should already be done. there are no remaining unprocessed that i've given you."* | — |
| **F. YAML-head gates** | F-364 (the gate that reads `yaml_file:`) · F-405 (a stale gzip passes) · F-441 (index sha256 vs the committed blob) · F-454 (an absolute max without its board revision) · F-389 (the key generator drops path components) | A build spec for each gate |
| **G. Class sweeps** | For every row in A–D and F, the wider search: the same wrong claim, pattern or shape anywhere in `deliverables/ai/P2/` | Every sibling found is added to its row |

### The parallel track: the ENH-03 compile gate

Stephen decided it is built **first** and stays a permanent release gate. It is tooling, not
research, so it runs as its own track from day one, under its own tasks, built from the
register's ENH-03 design points:

1. the per-block markers;
2. fix the prototype's collision bug;
3. a hard gate in `release-yamls`;
4. an edit-time check in `yaml-knowledge-base-maintenance`.

The study's "is this example correct?" reads (F-381 reading 1) wait on it.

### Excluded, each with its reason

| Excluded | Why |
|---|---|
| The ~22 `PENDING-VALIDATION` entries (F-546, 547, 543, 549, 542, 525, 421, 436, 377, 383, 393, 387, 320, 552–559), plus F-361 and F-544 | Already applied and independently verified. They close when a release serves them, so there is nothing to research. A class sweep in G that touches their files reads them as it passes. |
| Manual and PDF-head items: F-299, F-300, F-301, F-316, F-317, F-280, F-356, F-424, the manual halves of F-202 and F-268, the F-561 app-note prose, F-418 (torture test) | Not YAML. They are fixed and committed with each document's release. |
| Ingestion-tree artifacts: F-332, F-341, F-344, F-367, F-123 | ⛔ Ingested docs are never edited. These are findings for the ingestion head (`ingest-source`). The study notes whether any of them drives a KB claim. |
| MCP server: F-439, F-544 | They close in the server release (task «#398»), not in this repo. |
| ENH-01 (Architect's Guide harvest) and ENH-02 (platform line overflow) | New content and platform work, not corrections. |
| F-218 | The register already says no KB work is owed. It is swept closed at the hand-off. |

### The bench rule (Stephen, 2026-10-08)

**We only do bench runs for things that are not covered in our ingested source documentation.**

- A row becomes a bench question only after an exhaustive search of the ingested sources finds
  them silent, or finds them contradicting each other on that point.
- Every bench question records that search: the terms, the files, and a control hit.
- Already-filed items (D, F-336, the G-rows) are re-checked against the sources first. A source
  that answers one retires its bench question.
- A question about a tool's limit is never a bench question. Tool limits are not KB facts
  (doctrine).

### Severity scale (agent-consumer framing)

| Severity | Meaning |
|---|---|
| **drives wrong code** | An agent writing code from this produces a wrong program |
| **wrong, not code-driving** | False, but nothing an agent writes depends on it |
| **latent** | Not wrong yet; wrong under a condition (a missing gate, an unsourced claim that happens to be true) |
| **hygiene** | Findability, provenance, structure |

### Freeze rule

Field reports keep arriving. A report that touches a file already in the study joins the study.
Anything else goes to the next cycle, so the close-out has a fixed finish line.

### What done means

The study is done when every in-scope row ends in one of three states:

1. **A complete change spec** — file, block, current text, correct text, and its authority
   (source `file:line`, or an EF/XF result).
2. **A decided bench result** that produced (1).
3. **A recorded reclassification.** Untestable and unsourceable means removed (F-381 reading 4).
   A missing document is named. A call that is Stephen's is answered.

Planning closes at that point. Tasking follows.

### Open questions for the scope (to settle before reading)

1. ~~v1.24.0: ship now, or fold into the close-out release?~~ **DECIDED 2026-10-08: fold in
   (option B).** Stephen: *"we need the new full closeout process."* There is no separate
   v1.24.0. Its 24 commits (the 22 applied fixes, plus the delivery-filter rule at schema 3.6.0)
   ship in the single close-out release, under the §1.5 change-set audit. The MCP go-live
   («#398», F-439) waits for that release.
2. **F-359's debug claims vs the tool-limits principle.** `trace_buffer` ("4–16 KB in hub") and
   possibly `debug_state` describe debugger and application memory rather than silicon. Doctrine
   says tool limits are not KB facts. The research reads the debugger and interpreter as decided,
   and if the answer turns out to be a tool limit, it is put to Stephen rather than stated.

---

## 2. Read order — written before reading (tick as covered)

0. [x] **Ingestion prerequisites** (through `ingest-source` only) — done 2026-10-09; the operator
   re-ingestion it found owed is task «#405»:
   - [x] (a) ingest the v55 Spin2 interpreter — **done 2026-10-09 («#401»):** new edition at
     `engineering/ingestion/external-inputs/source-code/spin-interpreter/v55/` (byte-identical;
     PNut-TS v1.55.8 embeds exactly its compiled image); delta in
     `sources/spin2-v55/spin-interpreter-v55-delta-analysis.md`;
   - [x] (b) confirm which debugger is current — **done:** the v51 debugger source is current for
     v55 (PNut-TS v1.55.8 embeds exactly its compiled image). No document is missing;
   - [x] (c) audit the operator ingestion: glued, missing or invented operators, and the `&lt;`/`&gt;`
     entities in `spin2-v55-text.txt` — **done 2026-10-09 («#402»):** nothing is glued; the invented
     tokens come from the authored v51 summary. Rows S-267..S-278, erratum E-018, F-547's summary
     hunk reverted (`e5f5ab3d`). Re-ingestion of the operator reference is owed (S-267, S-276).
1. ~~Group E, field-report reconciliation~~ (dropped: every field report has been processed).
2. [x] **Group A**, decided items: F-359, F-375, F-398, F-381 (24 files), F-547 cascade — done
   2026-10-09 («#406»): rows S-281..S-315, bench question VO-S304, two questions for Stephen queued.
3. [x] **Group B** by KB area: architecture, then language/spin2, then language/pasm2, then
   hardware, then guides — done 2026-10-09 («#407»): the 13 register items and every S-row (S-001..S-381)
   in a done state; specs in `2026-10-08-p2kb-close-out-evidence/rows-*.md`, `groupB-register-items-specs.md`.
4. [x] **Group C**, knowledge gaps: the sources searched exhaustively for each one — done; registry updated.
5. [x] **Group D**, the bench queue: re-checked against the sources — done; five questions killed, round 1
   is eight rigs for nine questions.
6. [x] **Group F**, gate specs — done (S-382..S-389).
7. [x] **Group G**, a class sweep per row (done as each row is read, and ticked here when the last
   row's sweep is in) — done: every row batch carries its sweep; prose classes included.
8. [ ] **Bench specification**: tests written to house style. Each starts as a
   VERIFICATION-OPPORTUNITIES row, is written in the owning manual's `audit/verification-tests/`,
   and is reviewed adversarially by a fresh agent before the run.
9. [ ] **Bench run, round 1 (Stephen)**: his run, with everything around it ours.
10. [ ] **Results**: an EF entry for each result, rows updated. An inconclusive run or a new
    question gets a round-2 test.
11. [ ] **Planning closes**: every row in a done state (§1). Hand-off to `sprint-plan`.

After the sprint's tasks, the single close-out release goes through `release-yamls` **§1.5,
the change-set audit** (added 2026-10-08). Every hunk since the last tag is audited
adversarially by agents that made none of the changes: wanted, warranted and correct against a
source or bench result, removals justified, siblings complete. Stephen then reviews the audited
set before any tag.

Reading is dispatched per group to fresh read-only agents. Each return is a claim, and the
arbiter verifies its cited lines before a row enters the register. **Nothing in
`deliverables/ai/P2/` changes during the study.**

---

## 3. Findings register

| # | Group | Item | Severity | Finding | Evidence | Mark | Root cause | Resolution (change spec / bench Q / reclass) | Trivially safe? |
|---|---|---|---|---|---|---|---|---|---|
| S-001 | B | new | **drives wrong code** | `code-examples/smart-pins-001-basic-io.yaml`: the `complete_program` block does not compile (`Expected an instruction or variable`, block line 2), yet the file serves `compilation_result: "success"` | `pnut-ts -q` on the block verbatim (byte-identical, checked 2026-10-08); YAML `:18`, `:63` | traced | PASM instruction written as a Spin2 statement; a false "success" stamp | to research | no |
| S-002 | B | new | **drives wrong code** | `code-examples/smart-pins-002-button-reading.yaml`: same shape, `DIRL #BUTTON` in Spin2 (block line 5); serves `compilation_result: "success"` | as S-001; YAML `:18`, `:67` | traced | as S-001 | to research | no |
| S-003 | B | new | **drives wrong code** | `architecture/smart-pins/smart-pin-01010-pwm-smps.yaml:51`, `:56`: `dirh(v_sense)`, `dirh(i_sense)`. `DIRH` is PASM2, not a Spin2 method; the block fails ("Expected an instruction or variable", block line 11) | ENH-03 design probe; YAML read 2026-10-08 | traced | PASM instruction written as a Spin2 call | to research (class: PASM-in-Spin2, with S-001/S-002) | no |
| S-004 | F | new | hygiene | `deliverables/ai/P2/language/pasm2/add-missing-oneliners.py` is a tracked Python script inside the served YAML tree | `git ls-files deliverables/ai/P2 \| grep -v .yaml$` | traced | a generator left in the deliverables tree | to research (the other non-YAML files there are README/CHANGELOG/encoding reference/git hooks; check each is sanctioned) | no |

| S-005 | B | new | **drives wrong code** | `language/spin2/methods/bytecomp.yaml:3` and `wordcomp.yaml:3` describe the method as "Complement bytes/words within a long value". It compares two ranges of hub memory and returns -1 on match, 0 on mismatch | `spin2-v55-text.txt:582` (`BYTECOMP(AddrA, AddrB, Count) : Match`), `:146`, `:36` (v44) | traced | description written from the name, not the source | to research (class: all six v44 COMP/SWAP pages, with S-006) | no |
| S-006 | B | new | **drives wrong code** | `language/spin2/methods/byteswap.yaml:6` (and `wordswap`/`longswap`): the syntax is `BYTESWAP(Address1, Address2)`, with no `Count`. The source has three arguments; the description "swap byte values between two memory locations" is a single-element swap | `spin2-v55-text.txt:579`, `:581` (`…SWAP(AddrA, AddrB, Count)`) | traced | as S-005 | to research (with S-005; also check the pages' `{Spin2_vNN}` gating — the compiler rejects BYTECOMP with no directive, m172, and accepts it from `{Spin2_v45}`) | no |

*S-005/S-006 were found 2026-10-08 checking a proposer stub during ENH-03 B3 («#403»).*

**ENH-03 B3, group G1 (`language/spin2/methods/`, 457 blocks), 2026-10-08.** The reviewer's
site lists, compiler errors, source lines and compiled fixes are in
`2026-10-08-p2kb-close-out-evidence/b3-g1-defects.json` (classes, mapped to rows by
`b3-g1-class-map.json`) and `b3-g1-observations.json` (O-ids). Each sidecar entry's `finding:`
names its row. Arbiter checks: decisions re-applied in a fresh scratch root (same gate result);
the 301 accepted assume names scanned (all user placeholders); source lines for O3, O6, O8, O10,
O11, O13 and the CALL/REGEXEC/WAITCT rows re-read and holding.

| # | Group | Item | Severity | Finding | Evidence | Mark | Root cause | Resolution | Trivially safe? |
|---|---|---|---|---|---|---|---|---|---|
| S-006 *(widened)* | B | G1 | **drives wrong code** | also: 9 example blocks call BYTESWAP/WORDSWAP/LONGSWAP with two arguments (class `swap-methods-missing-count`); the notes claim an "atomic" single-value exchange (O20) | b3-g1 defects/O20; `spin2-v55-text.txt:579-581` | traced | as S-005 | to research | no |
| S-007 | B | G1 | **drives wrong code** | `byte.yaml`/`word.yaml`/`long.yaml` give the VAR declaration as `Name BYTE [Count]` (syntax, contexts, 3 examples); Spin2 is `BYTE Name[Count]` | defects `var-declaration-name-before-type`; O1; `spin2-v55-text.txt:267` | traced | DAT order applied to VAR | to research | no |
| S-008 | B | G1 | drives wrong code | reserved words used as identifiers (`lookup`, `lstr`, `next`), 3 sites | defects `reserved-word-as-identifier` | traced | compiler-unchecked authoring | to research | no |
| S-009 | B | G1 | drives wrong code | two-index arrays `[a][b]`, 3 sites; Spin2 arrays take one size | defects `two-dimensional-array` | traced | other-language habit | to research | no |
| S-010 | B | G1 | **drives wrong code** | CALL and REGEXEC documented as returning a value (`result := CALL(...)`, "result in result1"); neither returns one, and the compiler rejects them as terms. 6 example sites plus page prose (O2) | defects `call-regexec-used-as-expression`; O2; `spin2-v55-text.txt:556-558` | traced | invented return value | to research | no |
| S-011 | B | G1 | drives wrong code | PASM examples move results into `result1`, which does not exist (3 sites); the v55 CALL example passes data through PR0 | defects `undefined-pasm-symbol-result1` | traced | as S-010 | to research (with S-010) | no |
| S-012 | B | G1 | wrong, not code-driving | Spin2 statements at top level beside DAT/VAR, outside any method (9 sites) | defects `statements-outside-method` | traced | shorthand presented as code | to research (show the PUB, or mark the block as excerpt) | no |
| S-013 | B | G1 | **drives wrong code** | `DRVH(pin)` called as a Spin2 method (2 sites); Spin2 uses PINHIGH() | defects `pasm-instruction-called-as-spin2-method` | traced | same class as S-001..S-003 (PASM written as Spin2) | to research (one class sweep with S-001..S-003) | no |
| S-014 | B | G1 | drives wrong code | `COGCHK(n) ? "Running" : "Stopped"`: a multi-character quoted literal used as a string value | defects `string-literal-in-expression` | traced | other-language habit | to research | no |
| S-015 | B | G1 | drives wrong code | `SEND(BYTE[@buffer, 10])`: no such `BYTE[addr, count]` form | defects `send-byte-array-form-invalid` | traced | invented syntax | to research | no |
| S-016 | B | G1 | drives wrong code | LOOKUP/LOOKDOWN argument lists continued after a trailing comma with no `...` (4 sites) | defects `multiline-expression-without-continuation` | traced | other-language habit | to research | no |
| S-017 | B | G1 | drives wrong code | method-pointer call `data := inputMethod()` without the `:1` result count (2 sites) | defects `method-pointer-call-without-result-count` | traced | — | to research (with S-033) | no |
| S-018 | B | G1 | wrong, not code-driving | `@serial.rx` used with no `OBJ serial` line (2 sites) | defects `undeclared-object-instance` | traced | incomplete example | to research | no |
| S-019 | B | G1 | drives wrong code | complete PUB methods using undeclared locals or an undeclared `result` (11 sites) | defects `undeclared-local-in-complete-method` | traced | compiler-unchecked authoring | to research | no |
| S-020 | B | G1 | drives wrong code | `PUB restart_cog(...)` returns a value but declares no result | defects `return-value-without-declared-result` | traced | as S-019 | to research (with S-019) | no |
| S-021 | B | G1 | **drives wrong code** | CLKSET examples use `clkmode_pll`/`clkmode_rcfast`, which do not exist; the page says "use predefined clkmode_ constants" (only `clkmode_` and `clkmode` exist) | defects `undefined-clkmode-constants`; O15; `spin2-v55-text.txt:1725`, `:1730` | traced | invented names | to research | no |
| S-022 | F | G1 | hygiene (tooling) | **not a KB defect**: `getms.yaml:34`, `pollatn.yaml:25` are method bodies that `return` a value; the `spin2-method` wrap declares no result, so no honest context compiles them | defects `undecided-return-in-fragment` | traced | harness gap | **RESOLVED 2026-10-08:** wrap `spin2-method-result` added (53ff8f9f, NC16); both entries reclassified to it and pass | yes |
| S-023 | B | G1 | **drives wrong code** | GETRND described as a true-random hardware RNG "suitable for cryptographic use"; it is the xoroshiro128** PRNG seeded at boot | O3; `spin2-v55-text.txt:567`; `silicon-doc-text.txt:2852-2854` | traced | embellished description | to research | no |
| S-024 | B | G1 | latent | GETCRC: "hardware CRC engine", "initial CRC value is 0" — unsourced | O4; `spin2-v55-text.txt:597` | traced | unsourced embellishment | to research | no |
| S-025 | B | G1 | drives wrong code | `nan.yaml:23`: `sqrt(-1.0)` "creates NaN"; SQRT is the unsigned-integer root operator | O5; `spin2-v55-text.txt:438-439` | traced | float/int operator confusion | to research | no |
| S-026 | B | G1 | **drives wrong code** | QLOG/QEXP described as natural log and e^x, with ln-based examples; the silicon computes log base 2 and 2^x | O6; `silicon-doc-text.txt:3393`, `:3404` | traced | wrong base | to research | no |
| S-027 | B | G1 | **drives wrong code** | `movbyts.yaml:56-58`, `:82-85`: `%%1032` documented as swapping adjacent byte pairs; it swaps the words | O7; MOVBYTS definition (silicon doc) | traced | arithmetic error | to research | no |
| S-028 | B | G1 | **drives wrong code** | `hubset.yaml:37-38`: `HUBSET($8000_0000)` "bit 31 = reset chip"; MSB set seeds the PRNG, reset is `$1000_0000` | O8; `silicon-doc-text.txt:2852`, `:2862-2864` | traced | wrong bit | to research | no |
| S-029 | B | G1 | **drives wrong code** | `wrpin.yaml:74-96`: five mode literals are 31 bits, so each mode field lands one bit low | O9; `silicon-doc-text.txt:3731`, `:4684`, `:4257` | traced | digit-count error | to research | no |
| S-030 | B | G1 | **drives wrong code** | `wxpin.yaml:46`, `:86-89`: sync-serial word size given as X[5:0]; `%1_00111` called 16 bits (it is 8) | O10; `silicon-doc-text.txt:4654`, `:4675` | traced | — | to research | no |
| S-031 | B | G1 | **drives wrong code** | STRCOPY's Max documented as including the terminator; the source says up to Max characters, Max+1 bytes | O11; `spin2-v55-text.txt:590` | traced | off by one | to research | no |
| S-032 | B | G1 | latent | `string.yaml:39`: "escape sequences supported (\n, \t)" for STRING(); escapes belong to the `@\"…\"` form | O12; `spin2-v55-text.txt:50-59`, `:592` | traced | — | to research | no |
| S-033 | B | G1 | **drives wrong code** | RECV/SEND documented as copied out into a LONG and called; they are assigned (`SEND := @OutMethod`) and inherited | O13; `spin2-v55-text.txt:662-667`, `:682-685` | traced | mechanism misread | to research (with S-017) | no |
| S-034 | B | G1 | wrong, not code-driving | COGINIT called with NEWCOG (`cogchk.yaml:44,123`, `longmove.yaml:64`); NEWCOG is COGSPIN's symbol (same value) | O14; `spin2-v55-text.txt:1658-1669` | traced | — | to research | no |
| S-035 | B | G1 | wrong, not code-driving | `getct.yaml:90-92`: "direct access to CNT register" — CNT is P1 | O16; `spin2-v55-text.txt:547` | traced | P1 carry-over | to research | no |
| S-036 | B | G1 | drives wrong code | `waitct.yaml:38,45`: "until counter matches Tick", "exact match"; the wait ends once CT has passed Tick | O17; `spin2-v55-text.txt:549` | traced | — | to research | no |
| S-037 | B | G1 | latent | `cogatn.yaml:138`: "cannot signal yourself" — unsourced; the silicon doc does not exclude the signalling cog | O18; `silicon-doc-text.txt:2015-2021` | inferred | — | to research (possible bench question if the sources stay silent) | no |
| S-038 | B | G1 | latent | BYTEMOVE/WORDMOVE/LONGMOVE documented as overlap-safe with automatic direction; the source is silent | O19; `spin2-v55-text.txt:576-578` | inferred | unsourced | to research (interpreter source first; bench only if silent) | no |
| S-039 | B | G1 | wrong, not code-driving | `byte.yaml:41`: `send(BYTE(...))` presented as a user method; `send` is the built-in SEND pointer (names are case-insensitive) | O21; `spin2-v55-text.txt:662-667` | traced | — | to research | no |
| S-040 | B | G1 | latent | unsourced behaviour claims: "cog 0 always starts first", "cannot stop cog -1", "values outside 0-7 return 0", "maximum 496 longs" (`cogid`, `cogstop`, `cogchk`, `regload`) | O22 | undetermined | unsourced | to research (sources, then bench if silent) | no |

**ENH-03 B3, group G2 (`language/spin2/concepts/`, `conventions/`, 370 blocks), 2026-10-08.**
Evidence: `b3-g2-defects.json` (new classes, plus new sites for S-008, S-012, S-013, S-017,
S-018, S-019, S-020, S-033 and prose sites for S-023, S-025, S-031, S-035), `b3-g2-class-map.json`,
`b3-g2-observations.json`. Arbiter checks: re-applied in a fresh scratch root (same result); all
not-code reasons read; source lines for O2, O3, O7, O11, O12, O14 re-read and holding. **One
reviewer call overturned:** `johnny-mac-documentation-style.yaml` `complete_example.code`, a
complete P1 listing, was marked not-code; it is served as the Spin2 style page's example, so it
is a `program` carrying S-070 and stays red until fixed.

| # | Group | Item | Severity | Finding | Evidence | Mark | Root cause | Resolution | Trivially safe? |
|---|---|---|---|---|---|---|---|---|---|
| S-041 | B | G2 | drives wrong code | `addressing.yaml:164,167`: `REG[#myregs + index]` and notes "# returns cog register address"; the form is `REG[reg][index]` | defects `reg-hash-in-register-index`; O1; `spin2-v55-text.txt:364-365` | traced | PASM `#` habit in Spin2 | to research | no |
| S-042 | B | G2 | drives wrong code | `MOV PA, #@hubData` needs `##` | defects `hub-address-immediate-without-augment` | traced | — | to research | no |
| S-043 | B | G2 | **drives wrong code** | `object_archetypes.yaml:321-371` "pasm_only_object": a DAT-only child cannot be an OBJ, and `@obj.dat_label` is not legal; the archetype's claims fail to compile | defects `child-dat-label-through-object`; O22; `spin2-v55-text.txt:233-236` | traced | invented object mechanism | to research | no |
| S-044 | B | G2 | **drives wrong code** | `operators.yaml:25`, `:198-200`: `a :=: b` swaps plain variables; `:=:` swaps structures (v45) — use `a, b := b, a` | defects `swap-operator-on-plain-variables`; O7; `spin2-v55-text.txt:37`, `:866` | traced | — | to research | no |
| S-045 | B | G2 | drives wrong code | inline PASM register `pin` collides with a PUB parameter of the same name | defects `pasm-register-collides-with-parameter-name` | traced | — | to research | no |
| S-046 | B | G2 | drives wrong code | `{Spin2_v44}` used; the compiler refuses it (structures changed in v45) | defects `unsupported-spin2-v44-directive` | traced | stale gating | to research (class sweep: every `Spin2_v44` in the KB) | no |
| S-047 | B | G2 | drives wrong code | `value := ??` with no operand variable | defects `xoro-operator-without-variable` | traced | — | to research (with S-059) | no |
| S-048 | B | G2 | wrong, not code-driving | `print_string` called with 3 arguments, then 1, in one example | defects `callee-called-with-inconsistent-arity` | traced | — | to research | no |
| S-049 | B | G2 | **drives wrong code** | `type-propagation.yaml:24-43`: BYTE/WORD-typed parameters and results (`PUB foo(BYTE a, b)`, `: BYTE status`) taught as rules; the compiler rejects them (m220/m230) | defects `byte-word-typed-parameter-or-result`; O19; `spin2-v55-text.txt:276-278`, `:288` | traced | invented type rules | to research | no |
| S-050 | B | G2 | drives wrong code | result name `ready` collides with CON `READY` (names are case-insensitive) | defects `result-name-collides-with-constant` | traced | — | to research (with S-071) | no |
| S-051 | B | G2 | drives wrong code | `pub main` with no `()` | defects `parenless-method-header-and-call` | traced | P1 habit | to research | no |
| S-052 | B | G2 | drives wrong code | P1 comparison operators `=>`, `=<` | defects `p1-comparison-operators-equal-first` | traced | P1 habit | to research | no |
| S-053 | B | G2 | **drives wrong code** | `operators.yaml:49-50`: SCAS "(a * b) >> 32"; it is >> 30 | O2; `spin2-v55-text.txt:461-462` | traced | SCA/SCAS conflated | to research | no |
| S-054 | B | G2 | drives wrong code | `operators.yaml:131-133`: REV "reverse bottom N bits", `REV 8` result wrong; `x REV y` reverses bits 0..y (y+1 bits) | O3; `spin2-v55-text.txt:448` | traced | off by one | to research | no |
| S-055 | B | G2 | wrong, not code-driving | `operators.yaml:151`: `-100 +/ 7 = 613566751`; it is 613566742 | O4; `spin2-v55-text.txt:458` | traced | arithmetic | to research | yes |
| S-056 | B | G2 | **drives wrong code** | `operators.yaml:194-196`: `DECOD ENCOD (n - 1)` "round up to next power of 2" gives the power not above n-1 | O5; `spin2-v55-text.txt:434-435` | traced | — | to research | no |
| S-057 | B | G2 | wrong, not code-driving | `operators.yaml:206-208`, `:217`: precedence levels for `==` and `+` misquoted | O6; `spin2-v55-text.txt:464`, `:468-469`, `:478` | traced | — | to research (with the F-547 operator audit, «#402») | no |
| S-058 | B | G2 | latent | `operators.yaml:259`, `:280`: "float ~100x slower", "?? uses XORO32 hardware" — unsourced | O8 | traced | unsourced | to research | no |
| S-059 | B | G2 | **drives wrong code** | `random_generation.yaml:47-60`: the `??` algorithm, period and zero-state claims are invented | O9; `spin2-v55-text.txt:412`; silicon doc XORO32 | traced | invented algorithm | to research | no |
| S-060 | B | G2 | drives wrong code | `random_generation.yaml:220-226`: `GETRND() // 10` "slight bias toward 0-5"; `//` is signed, so the result is -9..9 | O10; `spin2-v55-text.txt:458-459` | traced | — | to research | no |
| S-061 | B | G2 | **drives wrong code** | `basic-io.yaml:109`: PINREAD of one pin returns "TRUE (-1)"; it returns 0/1, so `IF !PINREAD(...)` at `:295` is always true | O11; `Spin2_interpreter.spin2:2409-2415` (v51) | traced | — | to research | no |
| S-062 | B | G2 | **drives wrong code** | `basic-io.yaml:157-161`: pin range written `bottom..top`; Spin2 is Top..Bottom | O12; `spin2-v55-text.txt:390` | traced | — | to research (class sweep: every `..` pin range in the KB) | no |
| S-063 | B | G2 | drives wrong code | `basic-io.yaml:443-452`: "RDPIN blocks until data ready"; it does not wait | O13; `silicon-doc-text.txt:3720` | traced | — | to research | no |
| S-064 | B | G2 | wrong, not code-driving | `basic-io.yaml:382`, `:398-401`: conflicting cog drives "not documented"; the silicon doc says DIR/OUT are OR'd across cogs | O14; `silicon-doc-text.txt:3725` | traced | missed source | to research | no |
| S-065 | B | G2 | drives wrong code | `basic-io.yaml:369-376`: WS2812 timings 800/450/400/850 ns beside `WAITUS(1)`/`WAITUS(0)` | O15 | traced | unsourced, impossible with 1 µs granularity | to research | no |
| S-066 | B | G2 | drives wrong code | `string_constants.yaml:89-108`: escape table lists `\0`, `\"` and applies escapes to all strings; the source gives escapes only for `@\"…\"` and a different set | O16; `spin2-v55-text.txt:46-55` | traced | same class as S-032 | to research (with S-032) | no |
| S-067 | B | G2 | latent | `string_constants.yaml:21`: hub strings and DAT data called "read-only", with "undefined behaviour" on write — unsourced | O17; `spin2-v55-text.txt:303` | traced | — | to research | no |
| S-068 | B | G2 | drives wrong code | `string_constants.yaml:23`: `debug(@"Hello")`, `debug(label_ptr, …)` — a bare term in DEBUG() is output as a character | O18; `spin2-v55-text.txt:919`, `:938` | inferred | — | to research (sources first; bench only if silent) | no |
| S-069 | B | G2 | wrong, not code-driving | `timing_operations.yaml:180-181`: us-to-cycles overflow put at ~2.1B us; it is ~10.7M us at 200 MHz | O20 | traced | arithmetic | to research | yes |
| S-070 | B | G2 | **drives wrong code** | `johnny-mac-documentation-style.yaml:481-569`: the Spin2 style page's complete example is a P1 program (`cnt`, `_clkmode = xtal1 + pll16x`, `=>`) | O21; manifest entry `complete_example.code` (program, red) | traced | P1 source carried into a P2 page | to research | no |
| S-071 | B | G2 | drives wrong code | `johnny-mac-documentation-style.yaml:70-92`: constants `RX_PIN` and variables `rx_pin` side by side — one name, error m240 | O23 | traced | case-insensitivity missed | to research (with S-050) | no |
| S-072 | B | G2 | wrong, not code-driving | two convention pages require different block orders, each "required"; the compiler accepts any order | O24 | traced | — | to research | no |
| S-073 | B | G2 | **drives wrong code** | `johnny-mac-documentation-style.yaml:233`: `wypin(txbyte, TX_PIN)` — arguments swapped; WYPIN(PinField, Data) | O25; `spin2-v55-text.txt:541` | traced | PASM operand order | to research (class sweep: WYPIN/WXPIN/WRPIN argument order) | no |

**ENH-03 B3, group G3 (`language/spin2/constructs/`, `idioms/`, `statements/`, `integration/`,
files directly in `language/spin2/`; 276 blocks), 2026-10-08.** Evidence: `b3-g3-defects.json`
(new classes, plus new sites for S-008, S-009, S-014, S-018, S-020, S-066, and passing sites for
S-054, S-068), `b3-g3-class-map.json`, `b3-g3-observations.json`. Arbiter checks: re-applied in a
fresh scratch root (same result); not-code reasons and the one `never` read; source lines for O3,
O5, O10, O11, O14, O19 re-read and holding. **One reviewer call overturned:** `case.yaml`
`common_patterns[1].code` — `UPPER()` is an ordinary user helper there, not a built-in lookalike,
so it is an accepted assume; the block still fails on S-014.

| # | Group | Item | Severity | Finding | Evidence | Mark | Root cause | Resolution | Trivially safe? |
|---|---|---|---|---|---|---|---|---|---|
| S-074 | B | G3 | drives wrong code | `blocks.yaml`: DAT label `sine_table` after 11 bytes of BYTE data in ORG 0 — a cog label must be long-aligned | defects `cog-label-unaligned-after-byte-data` | traced | — | to research (`ALIGNL`) | no |
| S-075 | B | G3 | drives wrong code | `IF cond : stmt` one-line form does not exist (the CASE colon form does) | defects `inline-if-colon-form` | traced | other-language habit | to research | no |
| S-076 | B | G3 | drives wrong code | `<<=>` typo for `<=>` | defects `signed-comparison-operator-typo` | traced | typo | to research | yes |
| S-077 | B | G3 | drives wrong code | `ptr.value` on an untyped pointer in the short-circuit example | defects `short-circuit-example-untyped-pointer` | traced | — | to research (with S-094) | no |
| S-078 | B | G3 | drives wrong code | `END` used to close a DAT ORG/ORGH section (2 sites); END closes inline PASM only | defects `end-closing-dat-org` | traced | — | to research | no |
| S-079 | B | G3 | drives wrong code | `@var` inside inline PASM | defects `var-address-in-inline-pasm` | traced | — | to research | no |
| S-080 | B | G3 | **drives wrong code** | invented PASM instructions `SETCRC`, `CRC` | defects `invented-crc-instructions` | traced | invented names | to research | no |
| S-081 | B | G3 | drives wrong code | `(@array, size)` in a parameter list | defects `address-of-parameter-declaration` | traced | other-language habit | to research | no |
| S-082 | B | G3 | **drives wrong code** | `@this` and method chaining `obj.a().b()` taught as Spin2 | defects `method-chaining-self-reference` | traced | invented feature | to research | no |
| S-083 | B | G3 | drives wrong code | a local with a VAR's name taught as shadowing; it is a duplicate-name error | defects `local-shadows-object-variable` | traced | — | to research | no |
| S-084 | B | G3 | **drives wrong code** | `REPEAT n WHILE/UNTIL cond` (3 sites); no such form | defects `repeat-count-with-condition` | traced | invented form | to research | no |
| S-085 | B | G3 | drives wrong code | `IN(pin)` is not a method (PINREAD) | defects `nonexistent-in-method` | traced | — | to research | no |
| S-086 | B | G3 | drives wrong code | `REPEAT WAITMS(1) * 1000` — WAITMS returns no value | defects `method-without-result-used-as-value` | traced | — | to research | no |
| S-087 | B | G3 | **drives wrong code** | P1 `cognew()` (2 sites) | defects `p1-cognew-call` | traced | P1 carry-over (class with S-070, S-035, S-051, S-052) | to research (one P1-carry-over class sweep) | no |
| S-088 | B | G3 | **drives wrong code** | invented pin-array syntax `pina[0..7]`, `pinl[..]`, `pinh[..]`, `^^` toggle (5 sites) | defects `invented-pin-array-syntax` | traced | invented syntax | to research | no |
| S-089 | B | G3 | wrong, not code-driving | `blocks.yaml:46`: `#0, IDLE, RUNNING, ERROR ' 0, 1, 2, 3` — three names, four values | O1 | traced | — | to research | yes |
| S-090 | B | G3 | wrong, not code-driving | `blocks.yaml:52`: structures and conditional compilation "v44+"; STRUCT is v45 | O2; `spin2-v55-text.txt:37` | traced | stale gating (with S-046) | to research | no |
| S-091 | B | G3 | **drives wrong code** | `inline_pasm.yaml:166-168`: parameters "in PR0/PR1", return "in PR0"; the method's first 16 longs are at $1E0..$1EF under their own names | O3; `spin2-v55-text.txt:802-803` | traced | invented mapping | to research | no |
| S-092 | B | G3 | **drives wrong code** | `inline_pasm.yaml:184-189`, `method_definition.yaml:278-285`: `MUL` then `GETQX` shown as a multiply; MUL leaves the product in D | O4; p2kb `p2kbPasm2Mul` | traced | MUL/QMUL confusion | to research | no |
| S-093 | B | G3 | wrong, not code-driving | `inline_pasm.yaml:179-182`: "inline PASM labels must start with `.`"; plain labels compile | O5; `spin2-v55-text.txt:813` | traced | — | to research | no |
| S-094 | B | G3 | latent | `if_elseif_else.yaml:187-190`: AND/OR short-circuit — unsourced; the v51 interpreter's `bc_logand` works on evaluated values | O6 | inferred | — | to research (interpreter source; bench only if silent) | no |
| S-095 | B | G3 | drives wrong code | `case.yaml:90-96`: "direct string comparison" with `"START":` | O7; `spin2-v55-text.txt:738-748` | traced | as S-014 | to research (with S-014) | no |
| S-096 | B | G3 | wrong, not code-driving | `case.yaml:170-177`: a variable range bound "won't work"; the compiler accepts it | O8; `spin2-v55-text.txt:743-745` | traced | — | to research | no |
| S-097 | B | G3 | wrong, not code-driving | `repeat.yaml:35-47`: `post_test_*` variants labelled "test at end" with pre-test examples | O9; `spin2-v55-text.txt:764-767` | traced | — | to research | no |
| S-098 | B | G3 | drives wrong code | `repeat.yaml:158-159`: "loop variable is local to the REPEAT block"; it must be a declared variable | O10; `spin2-v55-text.txt:760-761` | traced | — | to research | no |
| S-099 | B | G3 | latent | `repeat.yaml:161-162`: STEP direction override and `FROM 10 TO 0 STEP 1` "never executes" | O11; `spin2-v55-text.txt:762-763` | inferred | — | to research (interpreter source; bench only if silent) | no |
| S-100 | B | G3 | **drives wrong code** | `spin2-pasm2-integration.yaml:112-126`: `CALL(#fastLoop)` on DAT code never loaded into cog registers | O12; `spin2-v55-text.txt:840-843` | traced | — | to research | no |
| S-101 | B | G3 | **drives wrong code** | `spin2-pasm2-integration.yaml:379-413`: REGEXEC chunk length ends before `temp`/`shared_flag_addr`, so they are never loaded | O13; reviewer's pnut-ts listing | traced | — | to research | no |
| S-102 | B | G3 | **drives wrong code** | `spin2-pasm2-integration.yaml:349-366`: `COGINIT(COGEXEC, …)` "start in cog mode" restarts cog 0 | O14; `spin2-v55-text.txt:1660` | traced | — | to research | no |
| S-103 | B | G3 | **drives wrong code** | `register-constants.yaml:100-110`: `rdlong value, ##INA_ADDR` reads hub RAM, not the register | O15; `spin2-v55-text.txt:360` | traced | — | to research | no |
| S-104 | B | G3 | latent | `method_definition.yaml:271`: "~50 clock cycles for call/return" — unsourced, against the KB's own stated position | O16 | traced | unsourced number | to research | no |
| S-105 | B | G3 | wrong, not code-driving | `case.yaml:110-113` etc.: Spin2 control flow "compiled to PASM2", "jump tables in COG RAM" — Spin2 compiles to bytecode | O17 | traced | — | to research | no |
| S-106 | B | G3 | wrong, not code-driving | `method_definition.yaml:79-81`: "arrays and objects pass references" | O18; `spin2-v55-text.txt:275-277` | traced | — | to research | no |
| S-107 | B | G3 | **drives wrong code** | `memory-access.yaml:46-52`: `@@buffer` "get absolute hub address"; `@@x` converts a stored object-relative offset | O19; `spin2-v55-text.txt:300`, `:425` | traced | — | to research | no |
| S-108 | B | G3 | wrong, not code-driving | `next.yaml:52`, `quit.yaml:53`: ABORT "exits entire method"; it unwinds to the trapping caller | O20; `abort.yaml:35-41`, `:120-131` | traced | — | to research | no |
| S-109 | F | G3 | latent (gate coverage) | the finder's net misses some code under `wrong`/`correct`/`syntax` that opens with a Spin2 flow statement (IF/CASE/REPEAT); arbiter census 2026-10-08: ~65 code-shaped multi-line strings outside the net | O21; arbiter scan | traced | net 2 counts block keywords and instructions, not flow statements | **RESOLVED 2026-10-08 (53ff8f9f, NC15a/b):** flow statements counted; an aborted elementize is a candidate. +114 blocks netted (3077 candidates); the 60 in G1–G3 files are classified in the G4 top-up | no |
| S-110 | B | G3 | wrong, not code-driving | `debug.yaml:218`: "automatic type detection", "processed at compile time" | O22; the page's own `:83-91` | traced | — | to research | no |

**ENH-03 B3, group G4 (`language/spin2/keywords/`, `operators/`, `special-symbols/`, `symbols/`,
284 blocks) plus the G1–G3 top-up (60 blocks the widened net caught), 2026-10-09.** Evidence:
`b3-g4-defects.json` (new classes; new sites for S-008 ×8, S-049 ×7, S-044 ×4, S-014 ×3, S-009,
S-012, S-019, S-020, S-077; claim sites for S-023, S-038, S-056, S-058, S-059, S-096, S-105),
`b3-g4-class-map.json`, `b3-g4-observations.json`. Arbiter checks: re-applied in a fresh scratch
root seeded with the 23 top-up files' real sidecars (same result); `spin2-v55-text.txt:249-256`
(typed pointers) and `:470` (ADDBITS) re-read and holding. The one `never` is
`case.yaml` `pitfalls[2].wrong` (CASE_FAST values more than 255 apart; its point is the error).

| # | Group | Item | Severity | Finding | Evidence | Mark | Root cause | Resolution | Trivially safe? |
|---|---|---|---|---|---|---|---|---|---|
| S-111 | B | G4 | drives wrong code | `WITH serial` taught as a Spin2 statement | defects `with-object-context-statement` | traced | invented statement | to research | no |
| S-112 | B | G4 | wrong, not code-driving | the ELSE, ELSEIF, ELSEIFNOT pages' only examples are the clause alone (3) | defects `orphan-clause-example` | traced | — | to research | no |
| S-113 | B | G4 | drives wrong code | `abort()` written as a call after OR/`||` (2) | defects `abort-written-as-call` | traced | — | to research | no |
| S-114 | B | G4 | **drives wrong code** | `typed-pointers.yaml:53-62`, `:261`: `ptr := @x` and `ptr++` taught to set and advance a typed pointer, and "[ptr]++ increments the value"; the source says the reverse — bare `ptr` is the pointed-to variable, `[ptr]` is the pointer itself (2 gated, 8 claim sites) | defects `typed-pointer-assignment-and-increment`; O1; `spin2-v55-text.txt:249-256` | traced | inverted semantics | to research | no |
| S-115 | B | G4 | drives wrong code | `STRUCT node(^node next, ...)` self-referencing member | defects `struct-self-pointer-member` | traced | — | to research | no |
| S-116 | B | G4 | drives wrong code | `: ^BYTE` result with no name | defects `pointer-result-without-name` | traced | — | to research | no |
| S-117 | B | G4 | drives wrong code | `READY_BITS = 3..1` as a CON constant | defects `con-bit-range-constant` | traced | — | to research | no |
| S-118 | B | G4 | drives wrong code | `LONG @State0` in DAT where State0 is a PRI | defects `method-address-in-dat` | traced | — | to research | no |
| S-119 | B | G4 | **drives wrong code** | `$$` used as the current address (3 gated + prose); the source gives `$` | defects `ditto-index-used-as-current-address` | traced | — | to research | no |
| S-120 | B | G4 | drives wrong code | `sin()` in a constant expression | defects `sin-in-constant-expression` | traced | invented function | to research | no |
| S-121 | B | G4 | drives wrong code | prefix `~flag`, `~~flag` (P1 sign-extend/post-set) and `//` as a comment (2) | defects `prefix-tilde-operator` | traced | P1 carry-over | to research (P1 class sweep with S-087) | no |
| S-122 | B | G4 | drives wrong code | bare `LOOKDOWN(...)` as a statement | defects `lookdown-used-as-statement` | traced | — | to research | no |
| S-123 | F | G4 | hygiene (tooling) | **not a KB defect**: 5 blocks need a STRUCT type the harness cannot declare (`STRUCT.yaml:105`, `:121`, `:168`, `:171`; `typed-pointers.yaml:193`) | defects `struct-types-not-declarable-in-harness` | traced | harness gap | **RESOLVED 2026-10-09:** assume kinds `struct:`, `OBJ.struct:`, `NAME:TYPE`, `OBJ.m(N)->T` (NC19a/b). The four STRUCT.yaml blocks pass; `typed-pointers.yaml:193` now fails only on its own S-114 defect (`ptr := @points`) | yes |
| S-124 | B | G4 | drives wrong code | `STRING(number)` presented as converting a number to text; it passes only because `number` is a declared symbol | defects `string-converts-expression` | traced | invented behaviour | to research | no |
| S-125 | B | G4 | drives wrong code | `LOOKUP(day : "Sun","Mon","Tue")` presented as a list of three strings; it is a list of nine characters | defects `lookup-list-quoted-strings` | traced | as S-014 | to research (with S-014) | no |
| S-126 | B | G4 | **drives wrong code** | `FILE.yaml:4-8`: FILE described as a file-inclusion directive (`FILE "config.spin2"`); it is a DAT data directive | O2 | traced | — | to research | no |
| S-127 | B | G4 | latent | `at.yaml:10-12` (@ object-relative in Spin2+PASM) contradicts `double_at.yaml:164` (@ "already absolute") | O3 | undetermined | — | to research (sources; bench only if silent) | no |
| S-128 | B | G4 | wrong, not code-driving | `hash.yaml:105-112`: cog register map ($120-$13F "reserved", "$140-$1CF LUT access window") | O4 | traced | invented map | to research | no |
| S-129 | B | G4 | **drives wrong code** | `op_ADDBITS.yaml:4`: ADDBITS "add bit count to pin number"; it makes a bitfield | O5; `spin2-v55-text.txt:470` | traced | — | to research | no |
| S-130 | B | G4 | wrong, not code-driving | `op_addmodulo.yaml:50-52`: description contradicts the file's own header | O6 | traced | — | to research | no |
| S-131 | B | G4 | wrong, not code-driving | `precedence.yaml:15`, `:64`, `:86`: NOT at level 2, ternary "PUB/PRI only" | O7 | traced | — | to research (with «#402» and S-057) | no |
| S-132 | B | G4 | drives wrong code | `op_POW.yaml:29-31`: POW at level 6; it groups at level 8 with +/- | O8 (compiled probes) | traced | — | to research (with S-057) | no |
| S-133 | B | G4 | latent | unsourced speed figures: "3-10x faster", "~808 cycles", "nearly 2x" (`bytefill.yaml:123`, `longmove.yaml`) | O9 | traced | unsourced numbers | to research | no |
| S-134 | B | G4 | wrong, not code-driving | `if_elseif_else.yaml:218-226`: over-indented statement "not in IF block"; it compiles identically | O10 | traced | — | to research | no |
| S-135 | B | G4 | hygiene | AND/OR/XOR/SCA/SCAS `category: Unary`; `||`/`^^` `category: Bitwise` | O11 | traced | — | to research | yes |
| S-136 | F | G4 | hygiene (tooling) | **not a KB defect**: 12 VAR declaration lines (`BYTE flag`, `^LONG pValues`) have no VAR wrap, so they sit as not-code and are not gated | reviewer DEVIATIONS | traced | harness gap | **RESOLVED 2026-10-09:** wrap `spin2-var`, preferred by the proposer over `pasm2-dat` for declaration-only blocks (NC18/NC18b). The 12 entries reclassified to `fragment`/`spin2-var` and pass | yes |

**ENH-03 B3, group G5 (`language/spin2/` debug-commands, debug-displays, preprocessor, constants,
system-variables, registers, patterns, assembly-directives; 398 blocks, 121 files), 2026-10-09.**
Evidence: `b3-g5-defects.json` (new classes; new sites for S-008, S-013, S-014, S-018, S-019 ×11,
S-020 ×5, S-050, S-052, S-071, S-077, S-088, S-121 ×6, S-124; claim site for S-073),
`b3-g5-class-map.json`, `b3-g5-observations.json`. Arbiter checks: re-applied in a fresh scratch
root (same result); the ten `never` entries read — nine are `#ERROR`/unbalanced/`#IF` blocks whose
point is the build stop with no symbol defined; source lines `spin2-v55-text.txt:40` (preprocessor
is v48) and `:1006` (C_Z) and the interpreter's `taskhlt res 1` (`Spin2_interpreter.spin2:417`)
re-read and holding.

| # | Group | Item | Severity | Finding | Evidence | Mark | Root cause | Resolution | Trivially safe? |
|---|---|---|---|---|---|---|---|---|---|
| S-137 | B | G5 | **drives wrong code** | `;` used as a comment in BYTE/WORD/LONG/FILE directive examples (17); `'` is the comment | defects `semicolon-comment` | traced | other-assembler habit | to research (class sweep: `;` comments anywhere in KB code) | no |
| S-138 | B | G5 | drives wrong code | `wc, wz` written as a pair in `c-z.yaml` (3); the form is `wcz` | defects `wc-wz-written-as-pair` | traced | — | to research | no |
| S-139 | B | G5 | drives wrong code | a bare `if_z` condition prefix used as a Spin2 statement | defects `condition-prefix-written-as-spin2-statement` | traced | PASM in Spin2 (class with S-013) | to research | no |
| S-140 | B | G5 | drives wrong code | `CON`/`OBJ`/`PUB` indented inside `#IFDEF` branches (5) | defects `block-designator-indented-in-conditional` | traced | — | to research | no |
| S-141 | B | G5 | drives wrong code | a backtick in a trailing comment on a DEBUG line breaks the compile | defects `backtick-in-comment-after-debug` | traced | — | to research | no |
| S-142 | B | G5 | drives wrong code | a `VAR` line inside a method-body listing (2) | defects `var-declaration-inside-method-body` | traced | — | to research | no |
| S-143 | B | G5 | drives wrong code | P1 `!OUTA[pin]` as a statement; Spin2 is `!= OUTA[pin]` | defects `p1-bare-not-statement` | traced | P1 carry-over (class with S-121, S-087) | to research | no |
| S-144 | B | G5 | wrong, not code-driving | a CASE with no cases (comment only) | defects `case-with-no-cases` | traced | — | to research | no |
| S-145 | B | G5 | drives wrong code | `plugin_table[i].call(m)` — method call through a dot on a LONG | defects `method-call-through-dot-on-long` | traced | other-language habit | to research | no |
| S-146 | B | G5 | **drives wrong code** | `COMPILER_V48_FEATURES` presented as a predefined symbol; no compiler defines it | defects `invented-predefined-symbol` | traced | invented name | to research | no |
| S-147 | B | G5 | latent | a 31-character method name — rejected by PNut-TS (30), legal by the v55 document (32) | defects `symbol-exceeds-30-characters`; S-251 | undetermined | document vs compiler | decided by S-251's PNut check (punch list item 7); not a KB defect if PNut takes 32 | no |
| S-148 | B | G5 | drives wrong code | two 76 800-long VAR arrays — more than 512 KB of hub RAM | defects `var-arrays-exceed-hub-ram` | traced | — | to research | no |
| S-149 | B | G5 | wrong, not code-driving | utility library's `constrain` calls `max`, which the page never defines | defects `utility-library-calls-undefined-max` | traced | incomplete example | to research | no |
| S-150 | F | G5 | hygiene (tooling) | **not a KB defect**: `special-configuration-symbols.yaml:219` (a `wrong:` block of conflicting clock symbols) is a correct `never`, but the compiler reports the conflict at end of file, so no `fails_at` body line matches and the gate prints NEVER-WRONG-REASON | defects `harness-gap-never-error-at-eof` | traced | harness gap | **RESOLVED 2026-10-09:** `fails_at: eof` (the error must fall past the block's last line, in wrapper text; NC20). The entry now passes as a `never` | yes |
| S-151 | B | G5 | wrong, not code-driving | `elseifndef.yaml:56-67`: the "undefined symbol" error the example claims is not the error the compiler gives (it fails on the 30-character limit) | O1 | traced | — | to research (with S-147) | no |
| S-152 | B | G5 | wrong, not code-driving | `preprocessor-overview.yaml:209-224`: `#IF` "fails at the #ENDIF"; pnut-ts rejects the `#IF` line itself (PNut-TS v1.55.8 shipped that diagnostic) | O2; `DRAFTS/PNUT-TS-PUNCH-LIST.md` item 2 (shipped) | traced | stale tool behaviour stated as fact | to research (doctrine: tool behaviour is not a KB fact — likely remove) | no |
| S-153 | B | G5 | wrong, not code-driving | every preprocessor page says "v47+"; the preprocessor arrived in v48, and `preprocessor-overview.yaml:304` contradicts `:308` | O3; `spin2-v55-text.txt:40` | traced | stale gating (with S-046, S-090) | to research (one gating sweep) | yes |
| S-154 | B | G5 | drives wrong code | `sensor_fusion.yaml:115-116`: integer `* 0.3` multiplies by a float bit pattern | O4 | traced | float/int confusion (with S-025) | to research | no |
| S-155 | B | G5 | **drives wrong code** | `hardware_specific_app.yaml:126`: `clkset(CRYSTAL_FREQ, CPU_FREQ)` passes the crystal frequency as the mode | O5 | traced | — | to research (with S-021) | no |
| S-156 | B | G5 | wrong, not code-driving | `taskhlt.yaml:15`: TASKHLT at "512 ($200)", which is LUT space; it is an interpreter register (`taskhlt res 1`) | O6; `Spin2_interpreter.spin2:417` (v51); `spin2-v55-text.txt:149` | traced | invented address | to research | no |
| S-157 | B | G5 | drives wrong code | `c-z.yaml:25-77`: what `DEBUG(C_Z)` prints after Spin2 statements; the source says only "useful in PASM code" — Spin2 statements do not set C/Z | O7; `spin2-v55-text.txt:1006` | inferred | invented behaviour | to research (sources; bench only if silent) | no |
| S-158 | B | G5 | drives wrong code | `spin2_memory_allocation.yaml:5-14`: heap of 1024 longs indexed as bytes with a 1024 limit | O8 | traced | unit confusion | to research | no |
| S-159 | B | G5 | **drives wrong code** | `configuration_manager.yaml:5-13`: `longmove(@config_data, addr, 32)` into a 19-byte structure (overruns 109 bytes) | O9 | traced | — | to research | no |
| S-160 | B | G5 | drives wrong code | `multi_motor_system.yaml:85` and a sibling: a parameter indexed as an array | O10 | traced | — | to research | no |
| S-161 | B | G5 | drives wrong code | `orgf.yaml:3`: ORGF "set origin with forced alignment", "align to $100"; ORGF fills with zeros up to the given address | O11 | traced | — | to research | no |

**ENH-03 B3, group G7 (files directly in `language/pasm2/`, the instruction pages; 291 blocks,
118 files), 2026-10-09.** Evidence: `b3-g7-defects.json`, `b3-g7-class-map.json`,
`b3-g7-observations.json`. Arbiter checks: re-applied in a fresh scratch root (same result); the
100 not-code reasons read (94 are description prose that opens with an instruction word);
`silicon-doc-text.txt:410-411` (SETQ before COGINIT) re-read; the TRUE/NEGX register-operand
behaviour reproduced with pnut-ts and filed as `DRAFTS/PNUT-TS-PUNCH-LIST.md` item 6 (reviewer O14).

| # | Group | Item | Severity | Finding | Evidence | Mark | Root cause | Resolution | Trivially safe? |
|---|---|---|---|---|---|---|---|---|---|
| S-162 | B | G7 | **drives wrong code** | constants used as register operands without `#`/`##`: `cmp value, POSX` (rejected, 2 sites) and — compiling silently into the wrong operand — `mov flag, TRUE`, `mov flag, FALSE`, `cmps value, NEGX` (`false.yaml:18,24`, `true.yaml:20`, …) | defects `const-as-register-operand`; O3; pnut-ts listing | traced | missing immediate marker | to research (class sweep: every named constant used as a PASM operand) | no |
| S-163 | B | G7 | drives wrong code | `AUGD start_reg` — AUGD/AUGS take an immediate | defects `augx-register-operand` | traced | — | to research | no |
| S-164 | B | G7 | drives wrong code | `NAME = 1` constant assignments inside a PASM block with no CON | defects `const-assign-in-code` | traced | — | to research | no |
| S-165 | B | G7 | wrong, not code-driving | a literal `--or--` line inside `coginit.yaml` code examples (4) | defects `or-separator-in-example` | traced | prose inside a code block | to research | yes |
| S-166 | B | G7 | drives wrong code | DJNZ written with `wz`; DJNZ takes no flag effect | defects `djnz-flag-effect` | traced | — | to research | no |
| S-167 | B | G7 | **drives wrong code** | immediates over 511 with one `#` (`#$8000_0000`, `QLOG #1000`, `#$400`; 3) | defects `imm-over-511-no-aug` | traced | class with S-042 | to research (one sweep with S-042) | no |
| S-168 | B | G7 | drives wrong code | `orgf.yaml` code folded onto one line by YAML quoting; one block then compiles vacuously (3) | defects `folded-single-quoted-code` | traced | YAML authoring | to research (class sweep: single-quoted multi-line code scalars) | no |
| S-169 | B | G7 | wrong, not code-driving | `ORGH $FC000,$FC800` example cannot build into a 512 KB hub | defects `orgh-example-beyond-hub` | traced | — | to research | no |
| S-170 | B | G7 | **drives wrong code** | `MODZ temp,#100` taught as modulo; MODZ modifies Z — use QDIV then GETQY | defects `modz-as-modulo` | traced | name-guessing | to research | no |
| S-171 | B | G7 | **drives wrong code** | `altgb.yaml:59-60`, `:81`: `altgb ptr, ##$100 ' auto-increment by 1`; S[17:9] is 0, so nothing increments (`##$200`) | O1 | traced | — | to research | no |
| S-172 | B | G7 | **drives wrong code** | `coginit.yaml:59-62`: SETQ placed after COGINIT; it must precede it | O2; `silicon-doc-text.txt:410-411` | traced | — | to research | no |
| S-173 | B | G7 | drives wrong code | `conditional-debug.yaml:70-71`: after `cmp a, b wcz`, `if_c_and_z` labelled "a == b AND overflow" | O4 | traced | flag misreading | to research | no |
| S-174 | B | G7 | wrong, not code-driving | `conditional-debug.yaml:5`: "available in v47+, prior caused compile errors" — not in the v55 change log | O5 | traced | stale gating (with S-153) | to research | no |
| S-175 | B | G7 | **drives wrong code** | `testp.yaml:60-66`, `:80`: rising-edge detection tests the wrong flags; `wz` described as XOR | O6 | traced | flag misreading | to research | no |
| S-176 | B | G7 | drives wrong code | `qlog.yaml:65-71`: the mantissa is shifted away, then an unloaded register is ANDed | O7 | traced | — | to research (with S-026) | no |
| S-177 | B | G7 | drives wrong code | `xoro32.yaml:16-28`, `:74-76`: the three-step "xoroshiro32+" algorithm is unsourced and is not that algorithm | O8 | traced | invented algorithm (class with S-059) | to research (with S-059) | no |
| S-178 | B | G7 | drives wrong code | `locktry.yaml:56-62`: the routine returns its outcome by `setd .result`, rewriting its own RET | O9 | traced | — | to research | no |
| S-179 | B | G7 | wrong, not code-driving | `fit.yaml:18-21`, `:34`: `FIT $1F0` "before the special-register area"; the area starts at $1F0 and other limits apply ($1F8 etc.) | O10 | traced | — | to research | no |
| S-180 | B | G7 | wrong, not code-driving | `hubexec.yaml:47`: "set hub execution mode for subsequent code"; HUBEXEC is a COGINIT constant | O11 | traced | — | to research | no |
| S-181 | B | G7 | hygiene | `debug.yaml:4`, `:11-13`: encoding and timing "TBD", description a placeholder | O12 | traced | stub page | to research (fill from the silicon doc and v55) | no |
| S-182 | B | G7 | **drives wrong code** | `xinit.yaml:55-72`: the receive example's streamer count D[15:0] is 0 and the `setword` that sets it is missing | O13 | traced | — | to research | no |

**ENH-03 B3, group G8 (`language/pasm2/` concepts, groups, idioms, patterns, registers; 396
blocks, 35 files), 2026-10-09.** Evidence: `b3-g8-defects.json` (new classes; new sites for
S-008 ×20, S-164 ×5, S-137 ×3, S-167 ×2, S-162, S-042, S-023), `b3-g8-class-map.json`,
`b3-g8-observations.json`, and the arbiter's KB-wide sweep for S-183,
`s183-yaml-hash-truncation-sweep.json`. Arbiter checks: re-applied in a fresh scratch root (same
result); `silicon-doc-text.txt:3688` (LOCKTRY C = taken) and `:2051`, `:2053` (event 12 streamer,
14 ATN) re-read and holding. Reviewer O8 joins S-023, O14 joins S-064, O23 joins S-042.

| # | Group | Item | Severity | Finding | Evidence | Mark | Root cause | Resolution | Trivially safe? |
|---|---|---|---|---|---|---|---|---|---|
| S-183 | B | G8 | **drives wrong code** | **YAML eats PASM immediates.** A plain YAML scalar followed by ` #…` on the same line is cut there, because YAML reads ` #` as a comment: `- MOV reg, #42` is served as `MOV reg,`. 22 gated example sites, and the arbiter's KB-wide sweep finds **47 served strings in 15 files cut this way, including `syntax:` lines** (CALLD's syntax is served as `CALLD PA|PB|PTRA|PTRB,`) — most of them outside the compile gate's net | defects `yaml-hash-comment-truncates-code`; `s183-yaml-hash-truncation-sweep.json` (every site, the served text, the lost text) | traced | YAML authoring: unquoted scalars holding `#` | to research (quote every site; and the gate in S-200) | no |
| S-184 | B | G8 | drives wrong code | `ADDPINS #7`; the count is a plain constant (5) | defects `addpins-hash-count` | traced | — | to research | no |
| S-185 | B | G8 | drives wrong code | `PTRB++[-1]`; the index must be 1..16 | defects `ptrx-postmodify-negative-index` | traced | — | to research | no |
| S-186 | B | G8 | drives wrong code | `IF_C NOP` (NOP is the all-zero word, so it cannot take a condition) | defects `conditional-nop` | traced | — | to research | no |
| S-187 | B | G8 | drives wrong code | `RETI1 WCZ` (2); RETIx is already `CALLD … WCZ` | defects `reti-flag-effect` | traced | — | to research | no |
| S-188 | B | G8 | drives wrong code | `#` used as a PASM comment inside block scalars (2) | defects `hash-comment-in-code` | traced | class with S-137 | to research (with S-137) | no |
| S-189 | B | G8 | **drives wrong code** | P1 `MAX`/`MIN` instructions; P2 has FGE/FLE | defects `p1-max-min-instructions` | traced | P1 carry-over | to research (P1 class sweep) | no |
| S-190 | B | G8 | drives wrong code | COGINIT with three operands (2); it takes two, with SETQ before it | defects `coginit-three-operands` | traced | — | to research (with S-172) | no |
| S-191 | B | G8 | drives wrong code | `LONG @@x` in DAT | defects `at-at-operator-in-dat` | traced | — | to research (with S-107) | no |
| S-192 | B | G8 | drives wrong code | `$$` used as the hub origin | defects `dollar-dollar-not-hub-origin` | traced | class with S-119 | to research (with S-119) | no |
| S-193 | B | G8 | drives wrong code | an instruction mnemonic used as a constant: `##(ADD | …)` | defects `instruction-mnemonic-as-constant` | traced | — | to research | no |
| S-194 | B | G8 | drives wrong code | `ALTS index++` (2); no such syntax | defects `alt-postincrement-syntax` | traced | invented syntax | to research | no |
| S-195 | B | G8 | drives wrong code | `IF_C routine`, where `IF_C CALL #routine` is meant | defects `bare-label-as-instruction` | traced | — | to research | no |
| S-196 | B | G8 | drives wrong code | one-operand `ADDCT1 ##n` on three group pages | defects `addct1-missing-operand` | traced | — | to research | no |
| S-197 | B | G8 | drives wrong code | `ptr++` on a register that is not PTRA/PTRB (3) | defects `postincrement-on-plain-register` | traced | — | to research | no |
| S-198 | F | G8 | hygiene (tooling) | **not a KB defect**: six excerpts reference a `.local` label defined outside them; the assume grammar has no local-label kind, and `with:` text lands before the `DAT`/`org` head, so PASM context cannot be supplied | defects `harness-gap-undefined-local-label` | traced | harness gap | **RESOLVED 2026-10-09:** assume `label:NAME` / `label:.NAME` (NC21). All seven sites pass; none hides a KB defect. `with` was left ahead of the wrap — no site needs it inside | yes |
| S-199 | F | G8 | hygiene (tooling) | **not a KB defect**: one excerpt opens with a relative `$`-address on its first line | defects `harness-gap-relative-dollar-first-line` | traced | harness gap | **RESOLVED 2026-10-09:** assume `lead:N` (N nops before the block; NC22). The site passes | yes |
| S-200 | F | G8 | latent (gate) | no gate catches a YAML scalar silently cut by a same-line comment (S-183): every KB gate reads the parsed value, which looks fine | arbiter sweep method (compose the YAML; a plain scalar whose line continues with ` #<non-space>`) | traced | absent guard | build spec: a structural check in the YAML gate set, run at edit time and release | no |
| S-201 | B | G8 | **drives wrong code** | `basic-io.yaml:404-405` (pasm2): `LOCKTRY … WC` then `IF_C JMP #try_again` "C=1 means locked by another"; C=1 means the lock was taken | O1; `silicon-doc-text.txt:3688`; instruction CSV `:270` | traced | flag inverted | to research | no |
| S-202 | B | G8 | **drives wrong code** | `register_indirection.yaml:78-81`, `:171-177`: ALTB examples address register 0, not the named register | O2; `silicon-doc-text.txt:546-560` | traced | — | to research | no |
| S-203 | B | G8 | drives wrong code | `register_indirection.yaml:47-51`: ALTR result register misdescribed | O3 | traced | — | to research | no |
| S-204 | B | G8 | **drives wrong code** | `event_interrupt_config.yaml:236-240`: `SETINT3 #12 ' ATN event`; ATN is event 14, 12 is streamer rollover | O4; `silicon-doc-text.txt:2051`, `:2053` | traced | — | to research | no |
| S-205 | B | G8 | drives wrong code | `event_interrupt_config.yaml:84-88`: RESIx "like RETI but continues the interrupted instruction" | O5 | traced | — | to research | no |
| S-206 | B | G8 | **drives wrong code** | `branch_addressing.yaml:64-72`: CALLA/CALLB "PTRx = PC+4", "return address in PTRA"; they write {C,Z,PC} to hub at PTRx++ | O6; instruction CSV | traced | — | to research | no |
| S-207 | B | G8 | drives wrong code | `special_registers.yaml:22`: `GETPTR` "reads PTRA/PTRB", and a SETPTR; GETPTR returns the FIFO hub pointer; there is no SETPTR | O7 | traced | invented instruction | to research | no |
| S-208 | B | G8 | drives wrong code | `cordic_solver.yaml:105-109`: POLLQMT used as a non-blocking "result ready" check; the page itself says otherwise at `:155-157` | O9 | traced | self-contradiction | to research | no |
| S-209 | B | G8 | drives wrong code | `rep_instruction.yaml:115-119`, `:135`: REP block sizes that do not match the bodies | O10 | traced | — | to research | no |
| S-210 | B | G8 | wrong, not code-driving | `rep_instruction.yaml:15`, `:22`: block size "0-2^32-1 with ##"; D is 9 bits (as `rep.yaml` says) | O11 | traced | self-contradiction | to research | no |
| S-211 | B | G8 | drives wrong code | `loop-control.yaml:64-65`: DJNF "runs max(1, count) times; safe for count=0" | O12 | traced | — | to research | no |
| S-212 | B | G8 | wrong, not code-driving | `cog_hub_execution.yaml:209-210`: "REP not available" in hubexec, against the same page | O13 | traced | self-contradiction | to research | no |
| S-213 | B | G8 | drives wrong code | `streamer_smartpin_control.yaml:346`: NCO full scale given as 2^32; it is $8000_0000 | O15 | traced | — | to research | no |
| S-214 | B | G8 | **drives wrong code** | `pasm2_hub_synchronization.yaml`: `rdlong … wc ' set C if non-zero`; WC takes the MSB | O16 | traced | flag misreading | to research | no |
| S-215 | B | G8 | drives wrong code | `conditional_execution.yaml:146`: IF_NC_OR_Z given as "unsigned below/equal"; that is IF_C_OR_Z | O17 | traced | — | to research | no |
| S-216 | B | G8 | wrong, not code-driving | `loop-control.yaml:27-35`: a "loop" instruction/marker that does not exist | O18 | traced | invented | to research | no |
| S-217 | B | G8 | latent | `register_indirection.yaml:106-113`: back-to-back ALT stacking taught, and contradicted elsewhere on the page | O19 | undetermined | self-contradiction | to research (silicon doc; bench only if silent) | no |
| S-218 | B | G8 | wrong, not code-driving | `branch_addressing.yaml:53`: "2-cycle latency for all jumps" — branch timing misstated | O20 | traced | — | to research | no |
| S-219 | B | G8 | drives wrong code | `conditional_execution.yaml:231-234`: `TEST value, #$80 WZ ' test sign bit` tests bit 7; `counter_event_polls.yaml:21`: the POLL and WAIT group pages share one JCT1 example that fits neither | O21; O22 | traced | — | to research | no |

**ENH-03 B3, group G9 (`architecture/**`, 353 blocks, 68 files), 2026-10-09.** Evidence:
`b3-g9-defects.json` (new classes; new sites for S-003, S-013 ×4, S-018 ×3, S-019, S-020, S-050,
S-074, S-120, S-137 ×6, S-164, S-165 ×2, S-167, S-198; claim sites for S-091, S-102),
`b3-g9-class-map.json`, `b3-g9-observations.json`. Arbiter checks: re-applied in a fresh scratch
root (same result); `silicon-doc-text.txt:200` (delta-sigma ADC), `:3970-3980` (pulse X halves),
`spin2-v55-text.txt:1469` (P_ADC) re-read and holding. The reviewer overturned three proposer
passes that rested on assumed P1 names (`cnt`, `getcnt()`) or a look-alike built-in (`SIN()`).

| # | Group | Item | Severity | Finding | Evidence | Mark | Root cause | Resolution | Trivially safe? |
|---|---|---|---|---|---|---|---|---|---|
| S-220 | B | G9 | drives wrong code | combined Spin2+PASM listings whose PASM registers share names with `main()`'s locals (6; m242) | defects `dat-pasm-register-same-name-as-method-local` | traced | — | to research (with S-045) | no |
| S-221 | B | G9 | **drives wrong code** | P1 counter names: `cnt` in PASM, `getcnt()` in Spin2 (2) | defects `p1-counter-names` | traced | P1 carry-over | to research (P1 class sweep) | no |
| S-222 | B | G9 | drives wrong code | `data := REV data` — REV is a binary Spin2 operator / a PASM instruction | defects `rev-instruction-as-spin2-unary` | traced | PASM in Spin2 (class with S-013) | to research | no |
| S-223 | B | G9 | drives wrong code | PASM instructions directly after a CON block, with no DAT/ORG | defects `con-block-followed-by-pasm` | traced | — | to research | no |
| S-224 | B | G9 | **drives wrong code** | `smart-pin-11000…yaml:51`, `:119`: `pinstart(adc_pin, $8_C600, …)` leaves the smart pin off (SSSSS = 0); ADC mode is `$0011_8030`-class | O1; `spin2-v55-text.txt:1469`, `:1554`; `silicon-doc-text.txt:4420` | traced | — | to research | no |
| S-225 | B | G9 | **drives wrong code** | `smart-pin-00100…yaml:27,29,74,85`: pulse/cycle X halves swapped (base period X[15:0], compare X[31:16]) | O2; `silicon-doc-text.txt:3970-3980` | traced | — | to research | no |
| S-226 | B | G9 | **drives wrong code** | `smart-pin-00111…yaml:62,76,114`: `$FFFFFFFF` (-1) makes duty 0; MUL takes only 16 bits | O3; instruction CSV (MUL) | traced | — | to research | no |
| S-227 | B | G9 | drives wrong code | `smart-pin-11101…yaml:136-139`: REV after SHR always gives 0 | O4; `silicon-doc-text.txt:4681` | traced | — | to research | no |
| S-228 | B | G9 | **drives wrong code** | `smart-pin-11110/11111…yaml`: `mov ptra, ##message` in cog-mode DAT loads a cog address, not a hub address | O5 | traced | cog/hub address confusion | to research (with S-042) | no |
| S-229 | B | G9 | **drives wrong code** | `cordic.yaml:157-163`: `QDIV divisor, dividend_low` — operands swapped | O6; instruction CSV (QDIV) | traced | — | to research | no |
| S-230 | B | G9 | **drives wrong code** | `smart-pin-01010-pwm-smps.yaml:59,70`: A/B inputs routed to current and voltage the wrong way round | O7; `silicon-doc-text.txt:4080-4091` | traced | — | to research (with S-003) | no |
| S-231 | B | G9 | drives wrong code | `smart-pin-00101…yaml`: sync-serial "companion" examples never set the TX pin up as a sync transmitter with a clock route | O8 | traced | — | to research | no |
| S-232 | B | G9 | drives wrong code | `cog_attention.yaml:221-235`: a barrier waits for "7 signals" with seven WAITATN; ATN is one flag | O9 | inferred | — | to research (silicon doc) | no |
| S-233 | B | G9 | **drives wrong code** | `locks.yaml:121`, `:142-143`, `:182`: "owner ID is in lock_num" after LOCKTRY — LOCKTRY does not write D | O10 | traced | — | to research (with S-201) | no |
| S-234 | B | G9 | wrong, not code-driving | `locks.yaml:367-372`: "system lock assignments" (lock 0 hub mailbox, lock 1 CORDIC…) — invented | O11 | traced | invented | to research | no |
| S-235 | B | G9 | drives wrong code | `p2-architecture-mental-model.yaml:120-121`: hub ops "2-9 clocks"; RDLONG 9…16, WRLONG 3…10 | O12; instruction CSV | traced | — | to research | no |
| S-236 | B | G9 | drives wrong code | `ptra-register.yaml:29`, `:49`: `PTRB--` "decrement then write" — post-decrement writes first | O13 | traced | — | to research | no |
| S-237 | B | G9 | **drives wrong code** | `smart_pins.yaml:54`, `:496-499`, `:548`: pin ADC called "12-bit SAR, up to 1 MSPS"; it is delta-sigma | O14; `silicon-doc-text.txt:200` | traced | invented spec | to research | no |
| S-238 | B | G9 | wrong, not code-driving | `complete-system-registers-index.yaml:23`: register totals that do not add to the page's own map | O15 | traced | — | to research | no |
| S-239 | B | G9 | **drives wrong code** | `clock_system.yaml:235-255`, `:104`, `:129`: 160 MHz and 250 MHz examples use VCO values against the page's own limits | O16 | traced | — | to research | no |
| S-240 | B | G9 | latent | `clock_system.yaml:214`, `:278`: "switching ~5 µs", "ADC clock = sysclk/2" — unsourced | O17 | inferred | unsourced numbers | to research | no |
| S-241 | B | G9 | hygiene | `smart-pin-01110…yaml`: "(This page previously showed WYPIN before DIRH.)" — a change note in served content | O18 | traced | doctrine: the KB states what is true now | to research (delete the note) | yes |
| S-242 | B | G9 | drives wrong code | `event_system.yaml:339-370`: pin-change monitoring reads RDPIN where INA is meant | O19 | inferred | — | to research | no |
| S-243 | B | G9 | drives wrong code | `fifo.yaml:165-174`: `mov dest, temp` / `add dest, #1` — `dest` is the destination itself, not a pointer (needs ALTD) | O20 | inferred | — | to research | no |
| S-244 | B | G9 | drives wrong code | `smart-pin-11001…yaml`: SINC3 post-processing stages do not match the silicon doc's | O21 | traced | — | to research | no |
| S-245 | B | G9 | wrong, not code-driving | `event_system.yaml:435`: `JMPREL #0 ' pipeline sync` — no source | O22 | traced | invented idiom | to research | no |
| S-246 | B | G9 | wrong, not code-driving | `smart-pin-11000…yaml`: "Y = trigger level for scope modes" | O23 | traced | — | to research | no |
| S-247 | B | G9 | drives wrong code | `debug_interrupt.yaml:213`, `:231`: ISR stores a register `PC` that nothing sets | O24 | traced | — | to research (with F-359, study group A) | no |
| S-248 | B | G9 | wrong, not code-driving | `smart_pins.yaml:59-62`: modes %00010/%00011 listed only as "long repository"; with DAC M bits they are DAC modes | O25 | traced | — | to research | no |
| S-249 | B | G9 | drives wrong code | `multi_resource_management.yaml:101-109`: an object `isp_octoport_serial` and its API are not in the OBEX index | O26 | traced | invented object | to research (check the OBEX index; per D4, OBEX references are checked against it only) | no |

**ENH-03 B3, group G10 (everything left: `guides/`, `language/fundamentals/`, `code-examples/`,
`hardware/`, `tools/`, one app note; 192 blocks, 19 files), 2026-10-09.** Evidence:
`b3-g10-defects.json` (S-075 widened with the `IF … THEN` one-line form; new sites for S-001,
S-002, S-018 ×2, S-071, S-078, S-083 ×4), `b3-g10-class-map.json`, `b3-g10-observations.json`.
Arbiter checks: re-applied in a fresh scratch root (same result); `spin2-v55-text.txt:166` (32
characters) re-read and the 30/31-character compile reproduced (`DRAFTS/PNUT-TS-PUNCH-LIST.md` item
7). **This makes S-147 undetermined:** its 31-character name is legal by the document and rejected
only by PNut-TS.

| # | Group | Item | Severity | Finding | Evidence | Mark | Root cause | Resolution | Trivially safe? |
|---|---|---|---|---|---|---|---|---|---|
| S-250 | B | G10 | **drives wrong code** | `pasm-labels.yaml:46`: `jnz .loop` (not a PASM2 instruction), `cmp` with no WZ, `tjz temp, :retry` without `#` | defects `jnz-not-a-p2-instruction` | traced | other-assembler habit | to research | no |
| S-251 | B | G10 | latent | symbol-length limit: v55 says 32, PNut-TS enforces 30; `identifier-rules.yaml:15-83` teaches 32 and its "32-char" example is 31 | O1; `spin2-v55-text.txt:166`; punch list item 7 | undetermined | document vs compiler | **a fact for PNut (ground truth), not a bench question** — the punch-list check decides it; S-147 follows | no |
| S-252 | B | G10 | **drives wrong code** | `spin2-getting-started.yaml:294,300,311`: `=<`/`=>` taught as Spin2; `&&`/`||` called bitwise; `!!` called post-clear | O2; `spin2-v55-text.txt:416-420`, `:489`, `:491` | traced | — | to research (with S-052, «#402») | no |
| S-253 | B | G10 | wrong, not code-driving | `spin2-getting-started.yaml:455,460`: DITTO index given as `$`; it is `$$` | O3; `spin2-v55-text.txt:42` | traced | — | to research (with S-119) | no |
| S-254 | B | G10 | drives wrong code | `spin2-getting-started.yaml:336`: `serial.start(63, 62, 115_200)` — jm_fullduplexserial's `start` takes four arguments | O4; `jm_fullduplexserial.spin2:121` (ingested OBEX source) | traced | — | to research | no |
| S-255 | B | G10 | **drives wrong code** | `spin2-getting-started.yaml:506-507`: `DEBUG("Value: ", DEC value)`; the form is `DEC(value)` (m172) | O5 | traced | — | to research | no |
| S-256 | F | G10 | latent (gate coverage) | code the tutorials present as single-line strings (an `examples:` heading, a DEBUG line, string definitions) is outside the gate's net — design §11 Q3 accepted that limit for notation, but these are real one-line programs | O6 | traced | design limit | to research (decide whether the net admits single-line strings under tutorial keys) | no |
| S-257 | B | G10 | wrong, not code-driving | `tools/pnut-ts-compiler.yaml`: the command written `pnut_ts`; quoted error messages do not match the compiler | O7 | traced | stale tool text (doctrine: tool behaviour is not a KB fact) | to research | no |
| S-258 | B | G10 | latent | `addon-control-board.yaml:115-124`: PWM and other figures absent from the add-on Product Guide | O8 | traced | unsourced numbers | to research | no |
| S-259 | B | G10 | drives wrong code | `edge-32mb-module.yaml:299-301`: burst-size formula with unbalanced parentheses, and its "~1280 bytes" does not follow (1456) | O9 | traced | — | to research | no |
| S-260 | B | G10 | wrong, not code-driving | `case-sensitivity.yaml:49-50`: five spellings "refer to the same constant" — `LedPin` and `ledpin` are the same, but the list mixes in `LED_PIN` (a different name) | O10 | traced | — | to research | yes |
| S-261 | B | G10 | **drives wrong code** | `smart-pins-002-button-reading.yaml:19-24`, `:39`: `BUTTON = 32` then `INA[BUTTON]` — pin 32 is in INB | O11 | traced | — | to research (with S-002) | no |
| S-262 | B | G10 | latent | `quick-queries.yaml:198`: "minimum 32 longs" of stack — unsourced | O12 | traced | unsourced number | to research | no |
| S-263 | B | G10 | drives wrong code | `spin2-getting-started.yaml:261`: `REPEAT idx FROM 99 TO 0 STEP -1` against the tutorial's own rule that FROM/TO sets direction | O13 | inferred | — | to research (with S-099) | no |
| S-264 | B | G10 | latent | `pasm-labels.yaml:78`: "local labels can shadow global labels" — unsourced | O14 | traced | — | to research | no |
| S-265 | B | G10 | hygiene | `pasm2-getting-started.yaml:599`, `:603`: "Silicon Doc v35" and a "Green Book" file name in served content | O15 | traced | codenames and repo file names in served text | to research | yes |
| S-266 | B | G10 | drives wrong code | `pasm2-getting-started.yaml:203`: `ADD x, y WC ' set C if overflow`; C is the unsigned carry | O16 | traced | — | to research | no |

**Answers from the v55 interpreter source («#401», 2026-10-09).** From
`engineering/ingestion/sources/spin2-v55/spin-interpreter-v55-delta-analysis.md` §4; `v55:` is
`external-inputs/source-code/spin-interpreter/v55/Spin2_interpreter.spin2`. The arbiter re-read the
four marked ✓.

| Row | What the interpreter settles | Evidence | Effect on the row |
|---|---|---|---|
| S-061 | PINREAD of one pin returns 0 or 1 (lsb-justified, zero-extended), never -1 ✓ | `v55:2467-2473` | traced; source now the v55 edition |
| S-038 | BYTE/WORD/LONGMOVE choose direction (`cmp ptrb,ptra` → `move_fwd` / `move_rev`) ✓ — so overlapping moves are safe, **the KB claim is right**; it needs this citation, not removal and not a bench run | `v55:2185-2187` | reclassify: unsourced → sourced (keep the claim, cite it) |
| S-099, S-263 | REPEAT FROM/TO: the sign of STEP is ignored (`abs`), direction comes from FROM vs TO ✓; so `FROM 10 TO 0 STEP 1` counts down — the KB's "never executes" is wrong. A compiler-emitted pre-test is not visible here | `v55:345-356` | traced (interpreter); no bench question |
| S-031 | STRCOPY copies up to Max characters then the terminator (Max+1 bytes) ✓ | `v55:2310-2318` | traced |
| S-094 | `bc_logand`/`bc_logor` combine two already-evaluated operands; whether the right side is skipped is a compiler decision not visible in the interpreter | `v55:295-310`, `:1043-1045` | partial — still needs the compiler/doc answer before any bench question |
| S-033 | SEND/RECV are per-frame cog registers saved and restored across calls, cleared at launch, called through the method-pointer path (unset RECV returns 0; unset SEND is dropped) | `v55:439-440`, `:675-685`, `:1397-1413`, `:2038`, `:1528-1546` | mechanism traced; the assignment syntax is the document's (`spin2-v55-text.txt:662-667`) |
| S-156 | `taskhlt` is an interpreter cog register (`res 1`), not LUT space; halt bit n belongs to task 31-n | `v55:430`, `:2959-2960`, `:2995-2997` | traced; its address ($1CC) is derived by counting, not stated — do not publish it |
| S-017 | the method-pointer call bytecode carries no result count; the callee's header supplies it | `v55:884`, `:1570-1578` | partial — the call-site `:N` rule is the document's and the compiler's |

**Operator-ingestion audit («#402», 2026-10-09).** Read-only audit of the operator table: the v55
DOCX (`word/document.xml`) is primary, against both PDFs, `spin2-v55-text.txt` and
`spin2-v51/complete-spin2-operators.md`. **The "glued operators" hypothesis is not supported:**
the DOCX, the v55 PDF, the v51 PDF and the text extraction all carry the same 84-row table with
every comparison token correctly spaced (`spin2-v55-text.txt:472-488`). The invented tokens come
from `complete-spin2-operators.md`, which is an authored summary, not an extraction — it says "52
operators, 16 levels" (the table has 84 rows, priorities 1–17) and its levels disagree with the
table at nearly every row. **Arbiter compile probes (pnut-ts v1.55.8, `CON x = 3 <op> 5`):**
`===`, `<>>`, `!&&`, `!||`, `+<=>`, `<<=>` are rejected; `<=>`, `+<=`, `<=.`, `==.` compile;
`a AND= b`, `OR=`, `XOR=` compile (compiler aliases absent from the table); `a := ??` is rejected
(m251), `??a` compiles. The F-547 hunk to the summary was reverted byte-identical (`e5f5ab3d`).
Previously registered and only referenced here: S-052, S-053, S-054, S-057, S-131, S-132, S-135,
S-252.

| # | Group | Item | Severity | Finding | Evidence | Mark | Root cause | Resolution | Trivially safe? |
|---|---|---|---|---|---|---|---|---|---|
| S-267 | A | F-547 | **drives wrong code** | `complete-spin2-operators.md` (ingested, authored summary) invents `+<=>`, `===`, `<>>`, `!&&`, `!||`, and unary `||x`/`^^x` (P1 encode/decode); the compiler rejects every one | `complete-spin2-operators.md:25-28`, `:71-72`, `:164`, `:174-175`, `:185`, `:189`; DOCX table = `spin2-v55-text.txt:472-488`; arbiter probes | traced | a model-authored summary carried as an ingestion artifact, with P1 carry-over | **re-ingest via `ingest-source`**: a new operator reference generated from the DOCX table, the old summary marked superseded (never edited) | no |
| S-268 | A | F-547 | **drives wrong code** | the same summary swaps `!` (bitwise NOT) and `NOT` (logical), and says float operators auto-convert integers (they reinterpret the bits; FLOAT/ROUND/TRUNC exist for that) | `:58-59`, `:343` vs `spin2-v55-text.txt:428-429`, `:346` | traced | as S-267 | as S-267; then sweep every KB page carrying either claim | no |
| S-269 | A | F-547 | wrong, not code-driving | the summary's levels 8–15 are shifted by one, XOR is misplaced, ADDBITS/ADDPINS and the float compares are missing, ternary and postfix forms are mislabelled | `:4`, `:14-30`, `:384` vs `spin2-v55-text.txt:410-501` | traced | as S-267 | as S-267 | no |
| S-270 | A | F-547 | **drives wrong code** | KB pages for tokens that do not exist: `op_notandand.yaml` (`!&&`), `op_eqeqeq.yaml` (`===`), `op_ltshr.yaml` (`<>>`); `precedence.yaml:53`, `:59` list `!&&`, `!||` | files cited; probes | traced | KB built from the summary | remove with Sacred Rule 7 redirects (inbound `related:` → the real operator pages) — the compiler probe is done | no |
| S-271 | A | F-547 | wrong, not code-driving | inherited summary text: `op_andand.yaml:4` "Boolean AND/NAND"; `op_eqeq.yaml:4`, `op_ltgt.yaml:4` "equal/not equal (logical/bitwise)" | files cited vs DOCX rows | traced | as S-270 | rewrite from the DOCX rows | no |
| S-272 | B | G4 | **drives wrong code** | `if_elseif_else.yaml:141-143`: invented `<<=>` "signed comparison result", `IF x <<=> y == 1` | probe (rejected) | traced | typo of `<=>` (class with S-076) | to research (with S-076) | no |
| S-273 | A | F-547 | wrong, not code-driving | `op_ABS.yaml:3-5`: description is a broken table fragment and `category: \``; `op_ADDBITS.yaml` already S-129 | `op_ABS.yaml:3-5` vs `spin2-v55-text.txt:432` | traced | a table row split during generation | rewrite from the DOCX row | yes |
| S-274 | A | F-547 | wrong, not code-driving | `concepts/operators.yaml:118-139`: REV/ZEROX/SIGNX under "unary" (they are binary, level 3); `:260-276` float list incomplete (`-.`, `<=.`, `>=.`, `==.`, `<>.`); `:21` "+variants for unsigned" beside `<=>` suggests `+<=>`; `:282-283` bare `??` (rejected, S-047) | file cited; DOCX table | traced | not checked against the table | to research (with S-053, S-054, S-057) | no |
| S-275 | A | F-547 | wrong, not code-driving | `spin2-language-schema.yaml:2`, `:19`, `:43-44`, `:427`, `:447`, `:450`: "16 levels", range [1,16], "52 operators", cites the summary as a source; the table has priorities 1–17 and 84 rows | file cited | traced | built from the summary | to research (state the DOCX counts; drop the summary as a source) | no |
| S-276 | — | ingestion | latent | `spin2-v55-text.txt` inserts a space at DOCX run boundaries: `p ost-increment` (×7, `:414-420`), `ENCOD = var` (`:434`), `ADDPINS = y` (`:471`). No operator is lost or glued | text vs DOCX runs and PDF | traced | the extractor joins runs with a space | re-ingest via `ingest-source` (join runs without a separator); nothing edited | no |
| S-277 | — | ingestion | hygiene | the v55 extraction audit repeats the "16 levels" miscount and marks it CLOSED | `spin2-v55-complete-extraction-audit.md:54` | traced | audit copied the summary's count | correct in the re-ingestion's audit (a new audit of record, never an edit) | no |
| S-278 | B | F-547 | hygiene | citation drift: `op_lteqgt.yaml:13` cites `:471-488` (the block is `:472-488`); `concepts/operators.yaml:329` cites `:409-491` (the table runs `:409-501`) | files cited | traced | line drift | to research | yes |

| S-279 | A | F-547 | hygiene | `op_addmodulo.yaml:21`, `:145` and `spin2-language-schema.yaml:19` cite the superseded summary (`op_addmodulo` cites `:715` of a 384-line file) | `git grep complete-spin2-operators` | traced | KB sourced from the summary | re-point to `sources/spin2-v55/spin2-v55-operator-reference.md` (with S-275) | yes |
| S-280 | B | F-547 | latent | the v55 table lists `var\x` as an assign form; pnut-ts rejects `v\3` as a statement ("Variable needs an operator") while the term form `w := v\3` compiles | `spin2-v55-operator-reference.md` row 8 probe | undetermined | document vs compiler | a fact for PNut (ground truth) — add to the PNut-TS punch-list check; no KB page asserts the statement form today | no |

**Re-ingestion done («#405», 2026-10-09):** `sources/spin2-v55/spin2-v55-operator-reference.md`,
generated from the DOCX table (84 rows, priorities 1–17, 137 of 138 forms accepted by pnut-ts,
the five invented tokens rejected as negative controls), with a redirect beside the superseded
summary and an audit of record. S-267/S-276/S-277's re-ingestion half is done; the KB half waits
for the sprint.

**Source erratum filed:** the v55 table's `+//` row reads `x // 7` where `x // y` is meant
(`spin2-v55-text.txt:459`; faithful to the DOCX, so Parallax's typo, not ours) —
`engineering/ingestion/SOURCE-ERRATA.md`.

### Group A — change specs («#406»)

**F-359 (2026-10-09).** Read-only research; the arbiter re-read `p2-datasheet-text.txt:1914`
(WAITATN `2+`), `silicon-doc-text.txt:467-468`, `:2399`, `:2427-2429`, `:2480`, `:2484`, `:2517`,
and the two KB lines being changed. Sources: the v51 debugger (current for v55), the v55
interpreter, the silicon doc, the datasheet, the instruction CSV, the empirical ledger.

| # | File, block | Current text | Correct text | Authority | State |
|---|---|---|---|---|---|
| S-281 | `architecture/locks.yaml:26` | `state_bits: 4  # Per lock: 3 bits COG ID + 1 bit owned flag` | **delete the line** (Stephen: no value to an agent). Nothing else references the key. Review `lock_states` (`:28-37`), which describes the same invented 4-bit encoding, in the same pass against `silicon-doc-text.txt:3673-3700` | decision D1; `grep state_bits` (one hit) | change spec |
| S-282 | `architecture/cog_attention.yaml:346` | `waiting: "0 clocks after signal arrives"` | `waiting: "2+ clocks (2 minimum, plus the wait for the event)"`. Same file `:123` and `:104` are already right. Also review `:358` "instant notification" (unsourced) | `p2-datasheet-text.txt:1914` (`2+`); instruction CSV `:325` (`2+`) | change spec |
| S-283 | `language/pasm2/waitatn.yaml:31-33` (class sweep) | `cycles: 2`, `type: variable` | `2+`, as its own encoding block at `:39` already says | as S-282 | change spec |
| S-284 | `architecture/decomposition/worked-derivation-streaming-pipeline.yaml:76` (class sweep) | "COGATN/WAITATN, 2-clock" | WAITATN is `2+` (COGATN 2) | as S-282 | change spec |
| S-285 | `architecture/debug_interrupt.yaml:381` `trace_buffer` | "Typically 4KB-16KB in hub" | replace the number with the silicon fact: the upper 16 KB of hub ($FC000..$FFFFF) can be write-protected so only a debug ISR writes it, and is shared with the per-cog save areas at $FF800.. | `silicon-doc-text.txt:2399`, `:2872`, `:2427-2429`; the debugger source has no trace buffer | change spec — **and a question for Stephen** (the debugger's own hub use is a tool limit; see below) |
| S-286 | `architecture/debug_interrupt.yaml:382` `debug_state` | "~100 longs for full state capture" | the silicon facts only: the ROM entry routine saves registers $000..$00F (16 longs) per cog; the ISR can read GETBRK status, the return address in INB, the stack by POP, and CT; anything more is the debugger's choice | `silicon-doc-text.txt:2427-2429`, `:2433`; no source gives ~100 | change spec — question for Stephen as S-285 |
| S-287 | `architecture/debug_interrupt.yaml:393-395` `streamer_interaction` | "Debug can disrupt streamer operations" / "Disable debug when using streamer" | scope it to what was measured: with every cog debug-enabled (the default), streamer-based Goertzel results were corrupted and restricting DEBUG_COGS to one cog fixed them (EF-057); the streamer pin/DAC output itself was unchanged with a live debug interrupt (VO-J-004 / EF-062, EF-063). No source states a mechanism | `P2-EMPIRICAL-FINDINGS.md:761-775`, `:861-865`; `silicon-doc-text.txt:2484` | change spec (mechanism bench test only if Stephen wants it) |
| S-288 | `architecture/debug_interrupt.yaml:213`, `:231` (S-247) | `WRLONG PC, trace_ptr` / `WRLONG PC, break_log` | `WRLONG INB, …` — the debug interrupt's return address (with C and Z in its top bits, address in [19:0]) is in INB (IRET0); the page's own tracer already uses INB at `:272`, `:320`. **S-247 is answered by this row** | `silicon-doc-text.txt:467-468`, `:2420`, `:2423`; `Spin2_debugger.spin2:323` | change spec |
| S-289 | `architecture/debug_interrupt.yaml` ISR examples (`:210-216`, `:228-235`, `:247-252`, `:271-276`, `:282-292`, `:298-304`, `:319-323`) | ISR bodies that never execute BRK before exit | add the re-arming `BRK` each needs, or say the example fires once: "bits L to A are cleared on ISR entry; a BRK must be executed before exiting … if a subsequent debug interrupt is desired" | `silicon-doc-text.txt:2517`; the debugger re-arms (`Spin2_debugger.spin2:240`) | change spec |
| S-290 | `architecture/debug_interrupt.yaml` class sweep | `:326-328` "monitor without modifying execution timing"; `:330-336` "FIFO/Streamer status" accessible; `:362-364` "prevents security vulnerabilities"; `:366-378` hubexec entry "13-20 clocks", "0 additional clocks"; `:385-387` "cannot debug the debug ISR"; ISRs writing registers with no note that redirecting IJMP0 loses the ROM save; `:407-434` stale metadata | correct or remove each per the evidence: an ISR costs cog clocks (EF-057); status is only GETBRK D[21]/D[20] + GETPTR; the rest is unsourced | `silicon-doc-text.txt:2480`, `:2484`, `:2536-2537`, `:2760`; EF-057 | to finish in the sprint pass on this file (all evidence is here) |

**F-375 (2026-10-09, arbiter inline).** `CITE_KEY_RE` (`audit-yaml-claim-sourcing.py:133-136`)
lists `source`, `sources`, `citation`, `reference`, `authority`, `derived_from`, `verified_against`,
`documentation` and kin — not `documentation_source` or `enhancement_source`. A key counts only when
its value also matches `CITE_VALUE_RE` (`:161-169`, a document vocabulary). Value tally (grep of
`deliverables/ai/P2/`): `documentation_source` names a real document ~345 times (`PASM2 Manual
2022/11/01 Pages 31-147` 145, `PASM2 Manual 2022-11-01` 116, `PASM2 Manual 2022/11/01` 60, the DEBUG
directive matrix 9, …); **`enhancement_source` has two values only, `PNUT_TS_v2.0_complete_operand_
integration_2025-09-13` (346) and `PNUT_TS_v2.0_operand_fixes_2025-09-13` (10) — labels of an
internal 2025-09-13 pass (there is no PNut-TS v2.0), not documents. `CITE_VALUE_RE` would still
accept them (the `pnut` token matches inside `PNUT_TS`).**

| # | File, block | Current | Correct | Authority | State |
|---|---|---|---|---|---|
| S-291 | `engineering/tools/validation/audit-yaml-claim-sourcing.py:133-136` | `CITE_KEY_RE` blind to `documentation_source` | add `documentation_source` to the key alternation; add a negative control proving a `documentation_source:` naming a manual counts and one holding a bookkeeping word does not; re-run the gate and record the Tier 1/2 movement | decision D2; `:133-136`, `:161-169` | change spec |
| S-292 | 40 sites (`f375-bookkeeping-token-sites.txt`) | `documentation_source: enhanced` (16) / `original` (15) / `p2_datasheet` (8) / `code_analysis` (1) | delete each line — except the 8 `p2_datasheet` sites (all CORDIC: `qvector`, `qfrac`, `qdiv`, `qrotate`, `qmul`, `qsqrt`, `qlog`, `qexp`): there, replace with the real datasheet citation **if** the page's facts are in the Datasheet's CORDIC section (check each), else delete — a citation hint is not removed when it can be made true (D4: do not remove useful things) | decision D2; evidence file | change spec |
| S-293 | 356 `enhancement_source:` lines | `PNUT_TS_v2.0_…_2025-09-13` labels | **not a citation**: do not teach `CITE_KEY_RE` this key (it would count 356 labels as sources); the labels are bookkeeping like S-292's words | as above | **queued question for Stephen** — his D2 said to teach both keys; the values show the second carries no documents. Recommendation: teach `documentation_source` only, and delete the 356 `enhancement_source` lines with S-292 |

**F-398 (2026-10-09, arbiter inline).** Every dollar figure in the KB is in one file: a sweep for
price strings (`\$NN-NN"`, `+\$NN`, `\$NN USD/each/per`) across `deliverables/ai/P2/` hits only
`hardware/p2-hardware-selection-guide.yaml`; every other `$` in `hardware/` is a hex value (I²C
addresses, registers).

| # | File, block | Current | Correct | Authority | State |
|---|---|---|---|---|---|
| S-294 | `hardware/p2-hardware-selection-guide.yaml` — 22 lines: `:23`, `:29`, `:38`, `:44`, `:53`, `:59`, `:68`, `:74` (`cost_estimate`), `:82`, `:105` (`total_investment`), `:121`, `:141`, `:152`, `:156`, `:160` (`cost`), `:127`, `:133` (`additional_cost`), `:165`, `:172`, `:179` (`total_cost`), `:166` (`programming: "PropPlug programmer required (+$30)"`), `:193` (`cost_difference: "$30-50 between P2-EC and P2-EC32MB"`) | dollar ranges | delete each price-only key; on `:166` keep the sentence and drop `(+$30)`; on `:193` delete the key (the memory-upgrade advice stands on `:194-195`). **Keep the tiering** (entry / balanced / maximized; "lower cost", "cost-effective" wording). Add once, at the file's top level: `pricing: "For current pricing, see the Parallax store (parallax.com)."` | decision D3 | change spec |

**F-381 (2026-10-09).** Read-only research over the 27 Tier-2 blocks
(`audit-yaml-claim-sourcing.py --advisory`), classified per D4. Arbiter re-read
`Spin2_interpreter.spin2:1953-1966` (CLKSET's 10 ms wait), `silicon-doc-text.txt:4158`, `:4080`,
`spin2-v55-text.txt:1725`. **No number is unsourced-and-untestable, so nothing is removed.** Four
example defects surfaced; one bench question.

| # | File, block | Current | Correct | Authority | State |
|---|---|---|---|---|---|
| S-295 | `language/spin2/methods/getms.yaml:54`, `getsec.yaml:38` (`silicon_errata`) | correct values, no citation | add `verified_against: "…/P2-EMPIRICAL-FINDINGS.md EF-068, EF-080, EF-082"` (getsec: EF-068, EF-082) | EF ledger `:1001-1018`, `:1334`, `:1374-1378` | change spec |
| S-296 | `waitct.yaml:37`, `single_communication.yaml:149`, `smart-pin-01111…yaml:97`, `smart-pin-10000…yaml:8`, `10001…:8`, `10010…:8`, `10011…:8` | correct derived wrap times (~53 s at 80 MHz; ~21 s; ~10.7 s at 200 MHz) | add `derived_from`/`source`: the counter/Z width + the arithmetic (`spin2-v55-text.txt:547`, `:553`; `silicon-doc-text.txt:4147`, `:4158`, `:4169`, `:4186`, `:4193`, `:4222`) | as cited | change spec |
| S-297 | `clkset.yaml:41` (`timing`) | "~10-20ms for PLL lock" | "~10 ms (20_000_000/100 clocks at RCFAST), only when the new clkmode sets the PLL/crystal bit; otherwise no wait"; cite it | `Spin2_interpreter.spin2:1953-1966` (v55); `spin2-v55-text.txt:1725`, `:1738`; `silicon-doc-text.txt:2613` | change spec (the KB value is wrong) |
| S-298 | `asmclk.yaml:61` | "~10ms" (correct) | add `source: "Spin2 v55 documentation (spin2-v55-text.txt:1725, :1738)"` | as cited | change spec |
| S-299 | `smart-pin-01000-pwm-triangle.yaml:34` | example description "1µs base period" | "40 ns base period" (X[15:0] = 1 clock at 25 MHz); the rest of the arithmetic checks | `silicon-doc-text.txt:4034-4050` | change spec (wrong P2 fact in an example) |
| S-300 | `smart-pin-01010-pwm-smps.yaml:37` | "100kHz switching" | "~39 kHz maximum (frame 256 × 25 clocks at 250 MHz); each cycle starts when A reads low" | `silicon-doc-text.txt:4070-4091` | change spec (with S-003, S-230) |
| S-301 | `smart-pin-01111…yaml` example | `duty_percent := (high_time * 100) / _clkfreq` overflows signed 32-bit above ~10 % duty; the PASM half (X = 0) and Spin half (X = clkfreq) are not equivalent as claimed | `muldiv64(high_time, 100, _clkfreq)`; align or reword the "equivalent" claim | 32-bit arithmetic | change spec (**drives wrong code**) |
| S-302 | `smart-pin-10010…yaml` example | `frequency := (_clkfreq * 100) / period` overflows | `muldiv64(_clkfreq, 100, period)` | 32-bit arithmetic | change spec (**drives wrong code**) |
| S-303 | `waitct.yaml:32-36` example 3 | "All cogs wait for same time" while each cog computes its own `GETCT() + clkfreq` | share `sync_time`, or fix the comment | — | change spec |
| S-304 | `smart-pin-01000/01001/01010` `registers` | base period and frame "1-65536" | **bench question VO-S304** (below); kept served until the bench decides | sources silent: searched `65,?536`, `X.[15..0]` in the silicon doc; control hit `:3925` (DAC/NCO "zero = 65,536") | bench question |
| S-305 | `smart-pin-10001…yaml:75` | "Servo pulse measurement (1-2ms pulses)" | an RC-servo convention, not a P2 fact: move the 1-2 ms into an `example:` child (or label it as the servo convention); keep the application | searched `servo` in the silicon doc and v55: none | reclassification |
| S-306 | decomposition: `worked-derivation-robot-dog.yaml:30`, `:41`; `worked-derivation-streaming-pipeline.yaml:30`, `:45` | scenario cadences in blocks tagged `authority_tier: EXAMPLE` | no content change — the gate exempts EXAMPLE-tier blocks (S-307) | the blocks' own tier | reclassification |
| S-307 | `first-contact-procedure.yaml:26`; `rate-adaptation.yaml:5`, `:51`; `spatial-computing.yaml:65` | scenario cadences in PRINCIPLE-tier prose | move the figures into `example:` children (rate-adaptation already has one at `:101-120`); `spatial-computing`'s sit in `worked_escape` — exempted by S-308 | — | change spec |
| S-308 | `engineering/tools/validation/audit-yaml-claim-sourcing.py` (decision D4 gate) | wholly-uncited files are advisory | (a) exempt example blocks by location: block names matching `^(\w+_)?examples?$` plus `quick_example`, `complete_example`, `usage_example`, any block with `authority_tier: EXAMPLE`, `worked_escape`, and one-line `wrong:`/`correct:`; NOT `anti_patterns`/`common_patterns`; (b) Tier 2 blocks (`main()` ~`:820-824`), switched on once S-295..S-307 are applied; (c) skip `community/obex/objects/` and add a small check of OBEX metadata against the index; (d) recognise `part\d+-…\.txt` silicon-doc citations in `INLINE_CITE_RE` (`:277-280`) — the smart-pin files cite that way and are wrongly "uncited"; negative controls: four must-not-fire (example blocks) and four must-still-fire (uncited prose, `notes` beside exempt examples, PRINCIPLE-tier figures, `common_patterns`) | decision D4; reviewer's line map of the script | build spec |
| S-309 | OBEX 4727, 4858 | "80MHz to 320MHz", "1.5/12 Mbps", "13-bit at 16k sps at 200MHz" in `description_full` | not checkable: the index text is truncated at 100 characters; 4012 matches exactly | `p2kb_obex_get` | reclassification (OBEX self-referencing; checked as far as the index goes) |

**F-547 cascade (2026-10-09).** Every KB operator page against the re-ingested reference
(`sources/spin2-v55/spin2-v55-operator-reference.md`). The page-by-page specs — 37 items, with the
arbiter's compile probes that decide each "probe needed" — are in
`2026-10-08-p2kb-close-out-evidence/f547-operator-cascade-specs.md`. They complete rows S-052,
S-053, S-054, S-056, S-057, S-058, S-121, S-129, S-130, S-131, S-132 (POW is level 8, left to right,
and needs `{Spin2_v51}` — probed), S-135, S-252, S-267..S-275, S-279. New:

| # | File, block | Current | Correct | Authority | State |
|---|---|---|---|---|---|
| S-310 | `operators/op_notandand.yaml`, `op_eqeqeq.yaml`, `op_ltshr.yaml` (S-270) | pages for `!&&`, `===`, `<>>` | no KB `related:` points at them; they are published keys, so the sprint chooses **delete or a redirect stub** in the `modulo_add.yaml` style (targets in the evidence file §A.3). Recommendation: redirect stubs — an agent that asks for `===` learns it is `==` | compiler rejects all three | change spec (stub targets set) |
| S-311 | `operators/op_addmodulo.yaml:88`, `:105`, `:122` | `(head - tail) +// BUFFER_SIZE` "any buffer size works" | holds only for power-of-2 sizes (probe `-3 +// 30` = 13); restrict the claim or rewrite the example | arbiter probe | change spec (**drives wrong code**) |
| S-312 | `spin2-language-complete-map.yaml:49-62` | unsourced counts (74 / 72 / 100 %); float variants written `.+ .- .* ./` | the reference's counts; `+. -. *. /.` | reference | change spec |
| S-313 | `special-symbols/at.yaml:21` | `block_usage: "All blocks"` | "PUB/PRI only" (address operators, T:421) | reference; probe `CON x = @y` fails | change spec |
| S-314 | `concepts/floating_point.yaml:73` | float `<.` "returns TRUE/FALSE" | "returns 0 or -1" | reference row #61 | change spec |
| S-315 | operator coverage | no page for bitwise `!`, `&`, `^`, `|`, unary `-`, `\`, CON `=`, compound and unary assign forms | coverage work for the sprint (new pages), not a correction | reference | noted (coverage) |

### Group B — register items («#407», 2026-10-09)

Read-only research; specs in `2026-10-08-p2kb-close-out-evidence/groupB-register-items-specs.md`.
Arbiter re-read `p2-hardware-manual-text.txt:1488`, `:1611`, `:1634`, `silicon-doc-text.txt:3946`,
`:4579`.

| # | Item | Severity | State | Summary |
|---|---|---|---|---|
| S-316 | F-550 | **drives wrong code** | change spec | serial loader: command syntax, `Prop_Ver G`, Prop_Clk's five fields, reply characters, the checksum long — all from the Hardware Manual's loader section |
| S-317 | F-562 | wrong, not code-driving | change spec | hub75 OBEX name and URL → "ISP Hub75 Matrix Driver" (OBEX 2850 metadata) |
| S-318 | F-561 (YAML) | drives wrong code | change spec | p2an003 init order: not "universal"; DAC modes capture Y while DIR is low (SD:3946); prose twin in P2AN003 changes in the same release |
| S-319 | F-392 | latent | change spec | top-level cog stack documented from the v55 interpreter (frame 6 longs + locals, grows up, no limit check); home file decided in the sprint |
| S-320 | F-548 | wrong, not code-driving | change spec | driver/API restatement removed from hardware pages (edge-32mb + 5 siblings); unsourced `power_sharing` lines removed |
| S-321 | F-551 | **drives wrong code** | change spec (block by block) | pasm2 getting-started guide: LUT access, C = carry, `$` origin, QMUL timing, Spin2 DEBUG in a PASM guide, dangling next-steps |
| S-322 | F-354 | latent | 1 blocked (schematic), 2 change spec (sizes from the guide's drawings), 3 blocked + **question for Stephen** | board facts |
| S-323 | F-386 | latent | **bench question VO-J-028** (eight pages, not ten) | Y written before DIRH in eight counter modes |
| S-324 | F-372 | latent | **bench question VO-F372** + small edit | USB WRPIN switch without reset — the sources disagree |
| S-325 | F-337 | latent | **bench question VO-F337** + interim conflict note | DAC_MODE `%TT=00`: DIR vs OUT |
| S-326 | F-336 | latent | change spec + **question for Stephen** | `P_HIGH_15K \| P_LOW_FLOAT` as a documentary idiom |
| S-327 | F-545 | hygiene | change spec (partial — key census to finish in the sprint) | provenance keys folded or removed; `authority_tier` is content |
| S-328 | F-560 | hygiene | change spec + **question for Stephen** (quick-bytes tags) | 78 label-valued `source:` lines |

### Rows S-001..S-040 — change specs («#407», 2026-10-09)

Every row S-001..S-040 is in a done state; the specs (current → correct → authority, plus class-sweep
sites) are in `2026-10-08-p2kb-close-out-evidence/rows-S001-S040-specs.md`. Arbiter re-read INT
`:2268-2270`, `:2328-2332`, `:2681-2682`, `silicon-doc-text.txt:4090-4091`, `spin2-v55-text.txt:337`,
`:360`. States: change spec — S-001..S-021, S-023..S-036, S-039, S-040 (S-040 answered from the sources,
no bench); RESOLVED — S-022; bench question — S-037 (VO-S037); reclassified sourced — S-038. Code marked
"compile in sprint" is compiled under the ENH-03 gate when applied. Sprint-time choices (not Stephen's):
S-003 PINHIGH vs PINSTART; S-021 an authored PLL-mode example. Noteworthy new truths: `x /. 0.0` and float
overflow give NaN, not Infinity (INT:2681-2682, 2859-2860); COGSTOP/COGCHK use the 4 low bits, so
`COGSTOP(16)` stops cog 0; GETCRC starts from all ones.

| # | Group | Item | Severity | Finding | Evidence | Mark | Root cause | Resolution | Trivially safe? |
|---|---|---|---|---|---|---|---|---|---|
| S-329 | B | S-026 sweep | **drives wrong code** | `qlog.yaml:22,26`, `qexp.yaml:22,26`: `QLOG(v) * 39457 >> 17` etc. — shifts bind tighter than `*`, so the scale is `* 0` / `* 2` | v55:443, :454 (priorities 3 and 7) | traced | precedence | change spec (MULDIV64 forms; numeric check in sprint) | no |
| S-330 | B | S-004 | hygiene | `.git-hooks/pre-commit`, `post-commit` in the served tree point at the dead `engineering/knowledge-base/P2` | `git ls-files` | traced | stale tooling | remove (or move to `engineering/`) with the stray `.py`; **question for Stephen:** README/CHANGELOG under the YAML-only rule | yes |
| S-331 | B | S-012 sweep | **drives wrong code** | `setregs.yaml:25-31`, `getregs.yaml:21-26` save/restore `$1F0-$1FF`, which includes PTRA, the Spin2 stack pointer — restoring it corrupts the cog | v55:806; INT:2136 | traced | — | change spec (rewrite the range; sprint) | no |
| S-332 | B | S-013 sweep | **drives wrong code** | `architecture/streamer/dds-goertzel.yaml:147-161`: a 512-entry LUT table built by `wrlut()` from Spin2 — there is no Spin2 WRLUT, and the interpreter owns LUT $010..$1FF | v55:806 | traced | — | change spec (rewrite as a PASM cog; sprint) | no |
| S-333 | B | S-028 sweep | drives wrong code | `hubset.yaml:22-33`: `waitms(10)` while on RCFAST, with `clkfreq` still holding the PLL value | v55:1725 (the CLKSET sequence) | inferred | — | to verify in the sprint (compile + read) | no |
| S-334 | B | S-025 sweep | **drives wrong code** | `concepts/floating_point.yaml:96-101`: `x / 0` and overflow "→ ±Infinity"; the interpreter returns NaN | INT:2681-2682, 2859-2860 | traced | assumed IEEE behaviour | change spec | no |
| S-335 | B | S-040 | wrong, not code-driving | `cogstop.yaml:23`, `:100`; `cogchk.yaml:19-20`: "invalid numbers have no effect", "values outside 0-7 return 0" — both use the 4 low bits | DS:1788, :1790; SD:421; INT:2076-2077 | traced | — | change spec | no |

### Rows S-041..S-110 — change specs («#407», 2026-10-09)

All 70 rows are in a done state; the specs are in
`2026-10-08-p2kb-close-out-evidence/rows-S041-S110-specs.md` (232 probe compiles; ~70 corrected blocks
compiled; 5 marked "compile in sprint"). States: change spec — S-041..S-108, S-110; RESOLVED — S-109.
**Settled without a bench:** S-094 (`&&`/AND evaluate both operands — `a && f()` and `a & f()` compile to
the same size and differ only in the operator byte; pnut-ts evidence), S-099 (STEP sign ignored,
INT:353-356). One bench question VO-S059 (inside S-059). Class sweeps widened several rows: S-062 — nine
method pages say "(Bottom..Top)"; S-044 — all of `op_swap.yaml` rests on scalar `:=:`; S-049 — the
BYTE/WORD/LONG keyword pages teach typed parameters. Arbiter re-read `spin2-v55-text.txt:92-100`, `:783`.
Sprint choices recorded in the file (D1–D5, D8, D9); D6 (block order) is taken by the arbiter as the
file recommends: each convention page states its own order as a convention and says any order compiles —
the only sourced fact. **NF-1 answers S-127:** `@` in PUB/PRI code is the hub address (v55:311); object-
relative is what `@` stores in DAT data (v55:297-300).

| # | Group | Item | Severity | Finding | Evidence | Mark | Root cause | Resolution | Trivially safe? |
|---|---|---|---|---|---|---|---|---|---|
| S-336 | B | NF-1 | **drives wrong code** | `concepts/addressing.yaml:9-11`, `:55`, `:95`: "`@` returns RELATIVE addresses in Spin2+PASM programs" — in code it is the hub address; relative is what `@` stores in DAT data (also settles S-127) | v55:297-300, :311 | traced | — | change spec | no |
| S-337 | B | NF-2 | latent | `basic-io.yaml:420-428`: a pin in output mode "reads the output latch, not the pin" — unsourced (SD:3706: IN returns the pin's read state) | SD:3706 | inferred | — | **bench question VO-S337** (jumper P0→P1) | no |
| S-338 | B | NF-3 | wrong, not code-driving | `blocks.yaml:90-94`: VAR "LONGs first, WORDs next, BYTEs last" — packed in declaration order | v55:262 | traced | — | change spec | no |
| S-339 | B | NF-4 | wrong, not code-driving | `timing_operations.yaml:164`: overflow at "~21 µs" at 200 MHz — ~10 µs | arithmetic | traced | — | change spec | yes |
| S-340 | B | NF-5 | drives wrong code | `if_elseif_else.yaml:275-278`: PASM illustration takes the wrong branch | compiled counter-form | traced | — | removed with S-105 (D8) | no |
| S-341 | B | NF-6 | drives wrong code | `method_definition.yaml:73-74`: "methods without return values return 0" — used as a term it is a compile error | v55:606, :623; compiler | traced | — | change spec | no |
| S-342 | B | NF-7 | **drives wrong code** | `inline_pasm.yaml:261-269`: RDLONG/ADD/WRLONG taught as "atomic"; not against other cogs, and interrupts run during inline PASM | v55:815; SD:3673-3700 | traced | — | change spec (LOCK guard) | no |
| S-343 | B | NF-8 | **drives wrong code** | `spin2-pasm2-integration.yaml:209-215`: the timer ISR keeps its target in PA, the interpreter's scratch; v55:847 uses PR0 | SD:1173; INT:2455; v55:847 | traced | — | change spec (compile in sprint) | no |
| S-344 | B | NF-9 | wrong, not code-driving | `method-pointers.yaml:30-31`: `LONG ptr : 16` is not a declaration form | compiler | traced | — | change spec | no |
| S-345 | B | NF-10 | latent | `escape-strings.yaml:117-147`: unknown escapes "passed verbatim" (v55:59) but pnut-ts rejects them; `\x00` accepted though outside `\x01..\xFF`; error-message list does not match | v55:59; compiler | undetermined | document vs compiler | a fact for PNut (punch-list item 9), not a bench question | no |
| S-346 | B | NF-11 | drives wrong code | `spin2-naming-jonnymac.yaml:318`, `spin2-formatting-standards.yaml:37`: `serial.start(…)` with three arguments; jm_fullduplexserial (OBEX 2842) takes four (with S-254) | ingested OBEX source `:121` | traced | — | change spec | no |
| S-347 | B | NF-12 | wrong, not code-driving | `repeat.yaml:228-239`: changing the loop variable is "undefined behavior" — the interpreter reads it each pass | INT:366-381 | traced | — | change spec | no |
| S-348 | B | NF-13 | wrong, not code-driving | `statements/debug.yaml:212`: DEBUG "non-blocking" — each DEBUG() runs a debug interrupt and shares the serial pins through LOCK[15] | v55:897-909, :926; EF-057 | traced | — | change spec | no |
| S-349 | B | NF-14 | latent | JonnyMac pages: `longfill(@rx_pin, -1, 4)` fills four longs; their VAR example declares three | page text | undetermined | — | check the real `jm_fullduplexserial.spin2` `stop()` in the sprint | no |

**Source erratum E-019 filed (NF-17):** v55 contradicts itself on NEXT/QUIT levels — `:783` "1..16,
default 1 = the current level" vs `:92-100` "NEXT 1 = 1st-outer", range 1..15; the compiler agrees with
`:92-100`, and so does the KB. No KB change.

### Rows S-111..S-161 — change specs («#407», 2026-10-09)

All 51 rows done; specs in `2026-10-08-p2kb-close-out-evidence/rows-S111-S161-specs.md` (222 probe
compiles; 7 items "compile in sprint"). States: change spec 47 (S-127 answered by S-336; S-153 carries
the one v44/v47 gating sweep with S-046, S-090, S-174); RESOLVED tooling — S-123, S-136, S-150;
undetermined — S-147 (punch list item 7); bench question — S-157 (VO-S157). Sweeps widened: S-137 `;`
comments reach 27 more lines in 22 files; S-140 27 indented-designator lines in 5 preprocessor files;
S-160 a third site; S-156 TASKHLT is `$1CC` (assembled v55 interpreter, INT:430), and
`p2an005-cooperative-multitasking-tasks.yaml:90,131` carry the same wrong address; S-133's speed figures
are false (BYTEMOVE and LONGMOVE share one path, INT:2166-2168); S-114 — every operation on
`typed-pointers.yaml` is inverted, not two blocks. Sprint choices D1–D6, D9 are in the file.
**Arbiter verified the headline finding (S-350):** `x := INA[3]` and `x := REG[INA][3]` compile to
identical binaries, and differ from `x := INA.[3]` (v55:366-367: `AnyVar[index]` indexes longs,
`.[bitfield]` selects bits).

| # | Group | Item | Severity | Finding | Evidence | Mark | Root cause | Resolution | Trivially safe? |
|---|---|---|---|---|---|---|---|---|---|
| S-350 | B | NF-1 | **drives wrong code** | `INA[pin]`, `OUTA[pin]`, `ina[0]` used as pin bits — they index registers (INA[3] = register INA+3). ~17 lines in 9 files: `smart-pins-002-button-reading.yaml:24,38`; `spin2_protocol_implementation.yaml:7-13`; `motor_controller.yaml:15,17`; `hardware_specific_app.yaml:108`; `registers/ina.yaml:7`; `registers/outa.yaml:8`; `smart-pin-01101…:55`, `01011…:55`, `01110…:54`. **Corrects the S-002/S-261 spec and S-143's `!= OUTA[pin]`** | arbiter byte-identity probe; v55:366-367 | traced | P1 idiom (P1 `INA[n]` was a bit) | change spec: `INA.[pin]` / `OUTA.[pin]`, or PINREAD/PINWRITE/PINTOGGLE; class sweep for `IN[AB]\[`, `OUT[AB]\[`, `DIR[AB]\[` | no |
| S-351 | B | NF-3 | wrong, not code-driving | `keywords/REPEAT.yaml:6-14` omits `REPEAT n WITH var` and the test-at-end WHILE/UNTIL forms | v55:756-773 | traced | — | change spec | yes |
| S-352 | B | NF-4 | wrong, not code-driving | `special-symbols/dollar.yaml`: `$` only as a hex prefix — it is also the current origin (cog register in ORG, hub address in ORGH) | v55:312, :321 | traced | — | change spec | yes |
| S-353 | B | NF-5 | drives wrong code | `pasm2/groups/counter_event_*.yaml`: `ADDCT1 ##1_000_000` with one operand (class with S-196) | DS:1851; compiler | traced | — | change spec (with S-137) | no |
| S-354 | B | NF-7 | latent | `preprocessor/external-symbols.yaml:149`, `:162`: glued `-DTARGET_P2_EDGE` — confirm the CLI accepts it | CLI help `-D, --Define <symbol...>` | undetermined | — | check in the sprint (tool behaviour: state the documented form only) | no |

**Bench question VO-S157 registered** (sources silent on what `DEBUG(C_Z)` prints from Spin2). PNut-TS
rejecting `DEBUG(C_Z)` between PASM instructions goes to the punch list (item 10), checked against PNut
first.

### Rows S-162..S-219 — change specs («#407», 2026-10-09)

All 58 rows done; specs in `2026-10-08-p2kb-close-out-evidence/rows-S162-S219-specs.md` (142 probe
compiles; every instruction line in the fences matches a probe). States: change spec 55; build spec —
S-200 (a structural rule that flags 52 cut scalars today and 0 after the S-183 edit); RESOLVED — S-198,
S-199. **Two diagnoses changed:** S-169 — `ORGH $FC000,$FC800` builds in a Spin2+PASM program and fails
only PASM-only (context, not impossibility); S-217 — answered by the PASM2 Manual (the ALT instructions
alter the next instruction regardless of its kind, `pasm2-manual-text.txt:1071`, `:1097`), so a change
spec, not undetermined. **S-183 widened:** an independent sweep reproduces the 47 cut strings and finds 5
more (`calld.yaml:51`, `addressing_modes.yaml:131`, `branch_addressing.yaml:40`, `:41`, `:80`); the quoted
replacements were applied to scratch copies and re-parsed clean. Sprint choices D1, D2, D4–D8 are in the
file; D3 (a gate for lower-case CON constants used bare as operands — undetectable by regexp) goes to
group F as a gate question; D9 (optional ALT silicon check) is not needed. NF-10 is S-288 (answered:
INB); NF-11 sits in S-102's block (check in the sprint).

| # | Group | Item | Severity | Finding | Evidence | Mark | Root cause | Resolution | Trivially safe? |
|---|---|---|---|---|---|---|---|---|---|
| S-355 | B | NF-1 | wrong, not code-driving | `special_registers.yaml:96`: "CORDIC results must be read before the next CORDIC operation" — commands may be overlapped; results are read in order | SD:3413 | traced | — | change spec | yes |
| S-356 | B | NF-2 | wrong, not code-driving | `addressing_modes.yaml:134-137`: AUGS vs AUGD chosen "by value size"; the split is by field (S vs D) | CSV:432-433; the page's own `:22` | traced | — | change spec | no |
| S-357 | B | NF-3 | **drives wrong code** | `multi_cog_synchronization.yaml:305-334` barrier: writes a register never loaded, retry compare cannot work, no atomic add exists | P2 has no hub atomic add; lock version compiled | traced | — | change spec (lock-guarded counter, compiled) | no |
| S-358 | B | NF-4 | **drives wrong code** | `loop-control.yaml:8`: `rep #{iterations}, #{instructions}` — operands swapped (D = instruction count, S = iterations) | SD:757; CSV:257 | traced | — | change spec | yes |
| S-359 | B | NF-5 | drives wrong code | `multi_cog_synchronization.yaml:289-290`: `shl work_index, #16` every pass shifts the packed cog number out | reading of the code | traced | — | change spec (scratch register) | no |
| S-360 | B | NF-6 | wrong, not code-driving | `branch_addressing.yaml:15`: relative branch range "±1MB" — a 20-bit signed byte offset spans ±512 KB | SD:731, :748 (derived) | inferred | — | change spec (state as derived) | no |
| S-361 | B | NF-7 | drives wrong code | `conditional_execution.yaml:309,315`: `TEST flags, #READY_BIT WZ` — tests the wrong mask if READY_BIT is a bit number | page neighbours use bit numbers | undetermined | — | sprint: decide from the page's own constant; TESTB form compiled | no |
| S-362 | B | NF-8 | wrong, not code-driving | `cog_hub_execution.yaml:217`: DJNZ in hubexec "13-14 clocks taken"; CSV gives 2 or 13…20 | CSV:193 | traced | — | change spec ("at least 13") | yes |
| S-363 | B | NF-9 | wrong, not code-driving | `loop-control.yaml:66`, `:96`; `scratch-storage.yaml:46` cite `flash_loader.spin2` lines for code the source does not contain (it reads through the FIFO) | `flash_loader.spin2:56-60` | traced | citation drift | change spec (re-cite or reword) | no |

### Rows S-220..S-280 — change specs («#407», 2026-10-09)

All 61 rows done; specs in `2026-10-08-p2kb-close-out-evidence/rows-S220-S280-specs.md` (28 code rows
compiled; 16 prose/YAML rows "compile in sprint"). States: change spec 44; pointer rows 14 (S-247 → S-288,
S-261 → S-350, S-267..S-275 and S-279 → the F-547 cascade, S-276/S-277 done by «#405»); reclassified —
S-249; undetermined — S-251, S-280 (punch list 7, 8). **Two study resolutions corrected:** S-255 — there
is no plain `DEC`; the forms are `UDEC(value)` / `SDEC(value)` (`spin2-v55-text.txt:947`, `:956` — arbiter
re-read); S-249 — `isp_octoport_serial` is real (OBEX 4257, ingested `isp_octoport_serial.spin2:173,289,440`),
so the row is not "invented object"; what remains is the page passing the object's `MODE_NONE`/`PU_3K3`
without the `serial.` prefix. **Arbiter decisions on the file's D-list:** D5 — delete every change note in
served text (the KB states what is true now); D6 — remove the `:label` spelling from the teaching pages (no
Parallax source; accepted by pnut-ts only — punch list item 11 checks PNut); D8 — fix the command name,
delete `common_errors`, point to `--help` (tool behaviour is not a KB fact); D9 — fix the ~10 served sites
that say "Silicon Doc"; `source:` lines are never served, so the official-title change there is cosmetic and
done mechanically in the sprint; D2 — a bench question (VO-S367). D1, D3, D4, D7, D10, D11 are sprint
choices recorded in the file.

| # | Group | Item | Severity | Finding | Evidence | Mark | Root cause | Resolution | Trivially safe? |
|---|---|---|---|---|---|---|---|---|---|
| S-364 | B | NF-3 | **drives wrong code** | `smart-pin-11001-adc-external-clock.yaml:77`, `:115`: mode literal puts a 1 in M[0] and none in the B selector, while the comment says "P_PLUS1_B for clock" | SD:3731, :3737-3743 | traced | digit placement | change spec | no |
| S-365 | B | NF-5 | drives wrong code | `wxpin.yaml:94`, `:96`, `:100`: X meanings for P_PULSE, P_NCO_FREQ, P_QUADRATURE wrong (rides with S-030) | SD:3970-3972, :4004-4012, :4095-4097 | traced | — | change spec | no |
| S-366 | B | NF-6 | wrong, not code-driving | `complete-system-registers-index.yaml:315-316`: "all register access completes in a single clock", hub timing — unsourced/wrong | CSV (most instructions 2 clocks) | traced | — | change spec | no |
| S-367 | B | NF-4 | latent | `smart-pin-11010-adc-scope-trigger.yaml:53`, `:97`, `:131`: `pinstart(adc_pin, P_ADC_SCOPE, …)` without the ADC-enable bits its own PASM literal carries | page `:77`; sources silent on whether %11010/%11001 need M[12:10] = %100 | undetermined | — | **bench question VO-S367**; interim: make the page self-consistent (`P_ADC_SCOPE \| P_ADC_1X`) | no |
| S-368 | B | NF-7 | latent | `:label` local-label spelling (`pasm-labels.yaml:29-35,38,59-61,68,90-92`; `identifier-rules.yaml:133,141-144`) — no Parallax source; pnut-ts accepts it | greps of SD, v55, v51, PASM2 manual, datasheet | traced | — | remove from teaching pages (arbiter D6); punch list item 11 | no |
| S-369 | — | NF-8 | latent | `sources/spin2-v51/experimental-findings.md:9-12,73-80`: pnut_ts v1.51.5 compiled 31–35-character symbols; v1.55.8 rejects ≥31 — a lead for punch list item 7 | ingested note | traced | tool change | attach to punch list item 7 | yes |
| S-370 | B | NF-9 | latent | `obex-projects/2842-…/jm_fullduplexserial.spin2:403` declares a local `field`, now reserved — the object the KB recommends does not compile unmodified | compiler | traced | language change | note on the KB pages that recommend it (OBEX is self-referencing; no fix to the object) | no |
| S-371 | B | NF-10 | drives wrong code | `debug_enabled.yaml:82-83`: `string("Memory free: ", dec(memory_free))` — STRING takes literals; `dec()` is an object method | v55:592 | traced | — | change spec | no |
| S-372 | B | NF-11 | wrong, not code-driving | `smart_pins.yaml:48` "per-pin 16-bit configuration" (WRPIN D is 32 bits); `:546-547` toggle-rate figures unsourced | SD:3731 | traced | — | change spec | no |
| S-373 | B | NF-12 | hygiene | ~10 served scalars and ~14 YAML comments carry change notes ("previously showed…") — S-241 class | sweep | traced | doctrine: state what is true now | delete all (arbiter D5) | yes |
| S-374 | B | NF-13 | latent | add-on pages' `use_cases`/`applications`/`advantages` lists beyond the Product Guide (`addon-serial-host.yaml:96-106`, `:132-161`; others unread) | guide text | inferred | unsourced capability lists | class sweep in the sprint (with S-258, S-320) | no |
| S-375 | B | NF-14 | latent | `p2-architecture-mental-model.yaml:130-137` CORDIC "7-8 in flight", "55 clocks", "1 result per cog every 8 clocks" | SD:3413 (54-clock pipeline) | inferred | — | re-derive in the sprint (with S-355) | no |

### Group C — the 16 knowledge gaps («#407», 2026-10-09)

Specs in `2026-10-08-p2kb-close-out-evidence/gaps-groupC-specs.md`. Arbiter re-read
`p2-datasheet-text.txt:331-333` (bypass caps, GND pad), `silicon-doc-text.txt:4074`, and the KB's
`addon-hyperram-hyperflash.yaml:153`. States: **ANSWERED** — G-009 (part numbers, read from the guide's
rendered page 7), G-012 (`+N` header convention, read from the figures), G-023 (SMPS IN rises when A reads
low, SD:4080, :4090), G-025 (BITx S[9:5] is the span field — not a BITC defect), and the cadence half of
G-002, the Y-timing half of G-004, the scope half of G-005; **ALREADY CLOSED** — G-006 for `%00110` (EF-013),
G-024 for the KB; **BENCH** — G-027 (VO-F372, reworded below), G-028 (VO-G028), two G-006 sub-questions
(VO-G006a, VO-G006b); **OUT OF REACH** — G-015 (#64009 / #64010 example archives not held), G-019 (Q-007),
G-022 (the mikroBUS specification — Q-010), G-029 (designer — Q-011), the thermal half of G-020, the ENOB
half of G-002 (Q-008). The proposed `KNOWLEDGE-GAPS.md` row moves are in the evidence file's last table and
are applied to the registry with this study's next commit set.

| # | Group | Item | Severity | Finding | Evidence | Mark | Root cause | Resolution | Trivially safe? |
|---|---|---|---|---|---|---|---|---|---|
| S-376 | B | G-004 | drives wrong code | `smart-pin-01010-pwm-smps.yaml:16`, `:23`: base period "system clock ÷ X[15:0]" / "divisor" — X[15:0] is the base period in clocks | SD:4074 | traced | — | change spec (with S-003, S-230, S-300) | yes |
| S-377 | B | G-009 | wrong, not code-driving | `addon-hyperram-hyperflash.yaml:153`: `IS26KL256S-DABL100 [VERIFY]` — the guide's page 7 reads `IS26KL256S-DABLI00` (letter I, then two zeros) | 64004-ES Product Guide p.7 (rendered) | traced | OCR carried into the KB | change spec (drop `[VERIFY]`) | yes |
| S-378 | — | G-009 | latent | ingested OCR text `sources/hyperRam-n-hyperFlash/hyperram-hyperflash-text.txt:153,155` carries two OCR errors in the part numbers | rendered page | traced | OCR | ingestion head: re-extract via `ingest-source` (never edited) | no |
| S-379 | B | G-020 | latent | the KB carries no PCB guidance; the datasheet states bypass caps close to every VDD/Vxxyy pin and the GND pad on a solid ground plane with multiple vias | DS:331-333 | traced | missed source | add to the hardware design page (sprint picks the home) | no |
| S-380 | B | G-025 | drives wrong code | `bitc`, `bitnc`, `bith`, `bitl`, `bitz`, `bitnz.yaml` omit the S[9:5] span rule (a non-zero S[9:5] changes several bits) | CSV row 44; SD:60; PM:1064, :1501-1503 | traced | — | change spec (one line each; `altb.yaml:5` already carries it) | yes |
| S-381 | B | G-027 | wrong, not code-driving | `smart-pin-11011-usb-host-device.yaml:17-29`: conflict note says the documents are "the same document" — three sources carry the sentence, only the newest silicon-doc edition omits it | HW:1488; Titus :1382; `p2-documentation.txt:8885-8886`; SD:4579 | traced | — | change spec (with S-324) | no |

### Group F — gate build specs («#407», 2026-10-09)

Specs in `2026-10-08-p2kb-close-out-evidence/gates-groupF-specs.md`, each with today's population (read-only
scratch counts), home, rule, negative controls, runner and what a green does not certify. The
`KNOWLEDGE-GAPS.md` registry was updated from group C/D in the same pass (backup
`.backups/engineering/ingestion/KNOWLEDGE-GAPS.md.20261009-055543`).

| # | Gate | Catches | Population today | Home | State |
|---|---|---|---|---|---|
| S-382 | S-200 | YAML plain scalar cut by a same-line ` #` | 52 in 15 files | new `audit-yaml-plain-scalar-comment.py` | build spec |
| S-383 | F-364 | dangling `yaml_file:` pointers | 0 — **already gated** by `validate-crossref-keys.py` (`:545-567`) | add a negative-control case | build spec (register note added) |
| S-384 | F-441 | index `sha256` vs the committed blob | committed index 38 of 1131 stale | new `audit-index-integrity.py` (sha256 limb) | build spec |
| S-385 | F-405 | index freshness (regenerate in a clone, compare) | committed index stale; `.gz` pair consistent | same script, freshness limb, `--post-commit` on the DoD runner | build spec (register note: the "nothing runs it" half is stale) |
| S-386 | F-454 | a hardware rating stated without its board revision | 5 rating scalars in 3 files | new `audit-hardware-revision-scope.py` | build spec |
| S-387 | F-389 | a directory name that reaches only some of its files | 8 directories (135 files) partial | new `audit-index-findability.py` with a reviewed baseline | build spec |
| S-388 | S-256 | one-line code outside the compile gate's net | 123 candidates under 13 seed keys | extend `audit-kb-code-compiles.py` (`_oneline-code-keys.yaml`) | build spec |
| S-389 | D3 | a built-in constant used as a bare PASM operand (`mov flag, TRUE`) | 8 sites in 4 files | extend `audit-kb-code-compiles.py` (elementizer token types) | build spec — **partial by nature**: user constants the harness declares are invisible; review covers the rest |
| — | S-308 | claim sourcing per D4 | — | `audit-yaml-claim-sourcing.py` | spec in row S-308 |

**VO-F372 reworded:** host ↔ device is a WXPIN field, already documented as changeable live (SD:4581);
the open question is whether a **WRPIN** sniffer/drive change takes effect without a DIR cycle.

**Bench question VO-S304 (to §5).** With `X[15:0] = 0`, and separately `X[31:16] = 0`, what base
period and frame count does a PWM_TRIANGLE (and PWM_SAWTOOTH) pin produce? Measure with a second
smart pin on a jumper (free pins P0–P7 / P32–P47). Sources silent: the silicon doc gives no range
for these modes; its only "zero = 65,536" statement is for the DAC/NCO modes (`:3925`).

### Stephen's decisions on the queued questions (2026-10-09)

Asked one at a time; each supersedes the "question for Stephen" note on its row.

| # | Rows | Decision |
|---|---|---|
| Q1 | (scope) | **"yes A".** The never-edit rule covers ingested documents, our extractions of them, and accepted bench results. The ingestion registries and the bench workflow (`VERIFICATION-OPPORTUNITIES.md`, new campaigns, the EF ledger) are maintained through their own skills. Doctrine overlay *The chain runs one way* reworded. |
| Q2 | S-285, S-286 | **C — delete the whole `memory_usage` block** of `architecture/debug_interrupt.yaml` (`trace_buffer`, `debug_state`). Stephen: keep it only if it guides code an agent writes; the one such fact (writes to the top 16 KB are dropped in a debug build) is already at `debug-strategy-guide.yaml:93`, `hub.yaml:36-57` and `debug_interrupt.yaml:80-83`. |
| Q3 | S-293 | **A.** Teach `CITE_KEY_RE` `documentation_source` only; delete all 356 `enhancement_source:` lines. New principle: *a citation names an official Parallax document, never one we created* (doctrine overlay, *Provenance is for us*). |
| Q4 | S-392, S-393 (new) | **A.** The one self-created source a claim may cite is an accepted EF record, for a fact measured on silicon. |
| Q5 | S-328 | **A.** Delete `metadata.source: parallax-quick-bytes` from the 42 Quick Bytes entries, keep `scraped:`; the entry's `url:` (all parallax.com) is its citation, and the sourcing gate learns that rule for catalog entries, with a negative control. |
| Q6 | S-326 | **Drop it.** The `P_HIGH_15K \| P_LOW_FLOAT` "Weak Pull-Up" line exists only in our own catalog extract (`smart-pins-catalog/ingestionSources/basic-io/spin2-v51-extract.md:284-287`), no Parallax document. Remove `not_documented_here.high_side_weak_with_low_side_floated` and that block's `sources:` line (a register self-cite) from `pin-drive-configuration.yaml`; F-336 closes with no content and no bench run; the ladder sweep is not owed. Sweep for other KB lines from that extract (S-391). |
| Q7 | S-322 item 3 | **Stephen:** the Rev B jumper is an Eval-board fact — the old P2-ES Eval Board Rev B needs the ACC HDR/5V shunt to put 5 V on the header pins, which matters for any add-on that uses header 5 V. The KB already models it so (`p2-hardware-feature-comparison.yaml:430`, `addon-serial-host.yaml:78,89`). Fix: remove the unsourced "3.3 V supply" from `addon-serial-device.yaml` and state no supply for it. No erratum. |
| Q8 | S-330 | **A, modified.** Remove `.git-hooks/`, `language/pasm2/add-missing-oneliners.py` **and `CHANGELOG.md`** ("why carry a pointer to somewhere else?"); move `language/PASM2-ENCODING-REFERENCE.md` out to `engineering/` and repoint its generator; keep `README.md` as the tree's only non-YAML file, and drop its *Release record* section that links the deleted CHANGELOG. |

**New rows raised by the decisions:**

| # | Severity | Finding | Evidence | Disposition |
|---|---|---|---|---|
| S-390 | latent | `code_author: Jane Doe` on one Quick Bytes entry reads as a placeholder | `grep -h code_author: community/quick-bytes/*.yaml` (1 of 42) | check the article's page on parallax.com; remove if the page does not name her |
| S-391 | latent | KB content may carry other lines that came only from our catalog extract `smart-pins-catalog/…/spin2-v51-extract.md` | the Q6 trace | sweep the KB for strings unique to that extract; each one gets a Parallax source or is removed |
| S-392 | hygiene | ~150 citations point at our text captures (`silicon-doc-text.txt:NNN`, `p2-datasheet-text.txt`, `spin2-v55-text.txt`, `pasm2-manual-text.txt`) and others at our summaries/registers (`complete-*.md`, `SOURCE-ERRATA.md`, the click-adapter netlist) — 131 files | `grep -rlE` over `deliverables/ai/P2`, 2026-10-09 | rewrite each to the Parallax document's title, edition and section/page; a claim with no Parallax document behind it is unsourced and goes through the search |
| S-393 | latent | `audit-yaml-claim-sourcing.py` accepts our own files as citations (`complete-builtin-symbols.md` and `…-text.txt` are its own examples, `:153-169`) | the gate source | the gate counts only a Parallax document or an EF record; negative controls for an extraction path and a register path |

*S-001..S-003 were found by the ENH-03 design probe («#399»); the compiler is the authority for
legality only. Their class (PASM2 written as Spin2) gets a class sweep in G.*

## 4. Root-cause groups

Each group is a candidate section of the sprint plan; rows can sit in more than one.

| # | Root cause | Representative rows | What fixes the class (not just the rows) |
|---|---|---|---|
| R1 | **Code never compiled.** Examples written and served without a compiler; 352 blocks fail today | the ENH-03 failures; S-001..S-021, S-041..S-052, S-074..S-088, S-111..S-122, S-137..S-149, S-162..S-170, S-183..S-197, S-220..S-223, S-250 | the ENH-03 gate (built, blocking); fix every registered block before release |
| R2 | **Propeller 1 carry-over.** P1 names, operators and idioms served as Spin2/PASM2 | S-035, S-051, S-052, S-070, S-087, S-121, S-143, S-189, S-221, **S-350** (`INA[pin]`) | one P1-carry-over class sweep; S-389's operand check; review |
| R3 | **Other-language habits.** C/assembler forms: `;` and `#` comments, two-index arrays, string literals as values, `IF … :`, method chaining, `jnz` | S-009, S-014, S-016, S-075, S-081, S-082, S-137, S-188, S-250 | R1's gate catches the illegal ones; review for the legal-but-wrong |
| R4 | **Invented facts and features.** Instructions, syntax, algorithms, register maps and assignments no source states | S-080, S-084, S-088, S-128, S-146, S-207, S-216, S-234, S-059, S-177 | "no unsourced claims" sweep per page; the claim-sourcing gate (S-308) |
| R5 | **Authored summaries treated as sources.** An AI-written summary ingested as if extracted; KB pages built from it | S-267..S-275 (operator summary), S-277, S-279 | re-ingest from the primary (done for operators, «#405»); flag derived notes as non-sources (G-019, G-020) |
| R6 | **Arithmetic and field-layout errors.** Bit positions, field widths, off-by-one, scale constants, wrap times, precedence | S-027, S-029, S-030, S-031, S-053, S-054, S-056, S-224..S-229, S-299..S-302, S-329, S-358, S-364 | compile + fold the constants (`CON x = …`) in the sprint; derive, don't copy |
| R7 | **Semantics read backwards or from the name.** Flags, pointers, enables, return values | S-005, S-010, S-061, S-114, S-173, S-175, S-201, S-206, S-214, S-215, S-233 | read the source at the line; the interpreter source now answers Spin2 semantics |
| R8 | **YAML mechanics.** Unquoted `#` truncation, folded scalars | S-168, S-183 (52 strings) | S-200's structural gate (S-382) |
| R9 | **Unsourced numbers and tool limits stated as facts.** | S-104, S-133, S-240, S-258, S-262, S-285, S-286, S-297, F-381 rows | D4's gate (S-308); doctrine: tool limits are not KB facts |
| R10 | **Stale version gating and change notes.** v44/v47 stamps, "previously showed" | S-046, S-090, S-153, S-174, S-241, S-373 | one gating sweep against v55's history; delete change notes |
| R11 | **Partial fixes and missing gates.** Siblings left behind; defects no gate could see | five of seven 2026-10-07 audit findings; S-109, S-200, S-256 | doctrine (fix the class in the pass); the §1.5 change-set audit; group F gates |

## 5. Bench questions

**Group D adversarial re-check (2026-10-09, «#407») — this verdict supersedes the Status column below.**
Every question was re-searched against all ingested sources, harder than the first time; detail, search
records, test outlines and house-style exemplars in
`2026-10-08-p2kb-close-out-evidence/bench-groupD-recheck.md`. The arbiter rendered and read Datasheet
2022-11-01 pp.27 and 31 (`external-inputs/archive/Propeller2-P2X8C4M64P-Datasheet-20221101.pdf`): in
Logic mode IN is taken from the PIN node through the input buffer; in `%101` DAC-with-ADC, DIR enables the
DAC driver and OUT enables the ADC.

| Question | Verdict | Why |
|---|---|---|
| VO-S337 | **KILLED** | Datasheet p.27: IN reads the pin node, not the latch (+ SD:3706, DS:1227) → S-337 becomes a change spec |
| VO-F337 | **KILLED** | no conflict: DS:1175 names the DAC enable (DIR), SD:3790 the ADC enable (OUT); Datasheet p.31 shows both; EF-055, EF-071 → S-325 becomes a change spec |
| VO-S367 | **KILLED** | composition of sourced statements: A input defaults to the pin read state (SD:3736), which is the ADC bit only in an ADC pad mode (v55:1465-1469; DS p.31); SD:4262 → the page needs the bits (its own `:140` says so) |
| VO-S157 | **KILLED** | C/Z are rewritten by XBYTE at every bytecode dispatch (SD:1046; INT:406), so no Spin2 statement's flags reach `DEBUG(C_Z)`; the digits depend on interrupt timing — state none; all five `c-z.yaml` examples go |
| VO-G006b | **KILLED** | the documented adder (SD:4004-4012) fixes the interval set; no KB claim depends on jitter |
| VO-J-005 arm B | **KILLED** | SD:1443-1454, v55:1608-1613, EF-059, EF-064, EF-065; arms A, C, D kept as in-rig controls; **J-005 survives reduced** (sustained-rate ceiling and filter skew only) |
| VO-J-006 arms A, B, C, E | **KILLED** | SD:493-499, SD:2249; **J-006 survives reduced** to one test (arms D+F merged — the interpreter loads LUT by SETQ2, INT:2044-2048) |
| VO-J-028 | **SURVIVES** | silent for the eight modes; EF-011 vs EF-090 shows the behaviour is mode-dependent; three arms, DEBUG read-out; **VO-G006a merged into it** |
| VO-F372 | **SURVIVES** | contradictory by edition; one USB pair on P0/P1, no jumper (SD:4614: the receiver sees its own output) |
| VO-S304 | **SURVIVES** | silent for PWM; frame period read from the pin's own IN interval — no second pin |
| VO-G028 | **SURVIVES (narrowed)** | pop-past-bottom is stated (SD:1150); what a ninth push discards is not; pure silicon |
| VO-S059 | **SURVIVES** | the sources name xoroshiro32+ but give no recurrence or zero case |
| VO-S037 | **SURVIVES** | SD:2020 does not exclude the issuing cog; SD:2053 says "another cog"; blocks no fix (`cogatn.yaml:138` is deleted now) |

**Bench round 1 = eight rigs for nine questions:** VO-J-028 (+ VO-G006a merged), VO-F372, VO-S304,
VO-G028, VO-S059, VO-S037, and the reduced VO-J-005 and VO-J-006 (VO-J-005's rig is already written).
None needs an external instrument; only VO-F372's fallback uses a jumper (free pins). No surviving question
is about a tool.

| VO id | Row(s) | Question | Sources-silent proof (terms · files · control hit) | Test file | Status |
|---|---|---|---|---|---|
| VO-J-028 | S-323 (F-386) | eight counter modes (`%01111`, `%10010`–`%10111`, `%11001`): does a Y written while DIR is low survive into operation, versus written after DIRH? | `During reset` · SD, HW, Titus, smart-pin narrative · control: pulse/transition and PWM Y-at-reset statements (`HW:1087`, `:1097`, `:1107`, `:1114`) | to write (step 8) | sources silent |
| VO-F372 | S-324, S-381, G-027 | with a USB pair running, does a new **WRPIN** (sniffer / drive change) take effect with DIR high, without a DIR cycle? (host ↔ device is a WXPIN field, documented live-changeable, SD:4581) | `sniffer` · 5 files · three documents carry the sentence (HW:1488, Titus :1382, `p2-documentation.txt:8885`), the newest silicon doc omits it (SD:4579) | to write | sources disagree |
| VO-G028 | G-028 | push nine values onto the 8-level hardware stack, pop nine: what does the ninth pop return? Pure silicon, no pins | stack depth `8` · SD, PM, CSV · control SD:166, PM:776 (depth 8 stated; overflow silent) | to write | sources silent |
| VO-G006a | G-006 | NCO duty `%00111` with Y = 0: output level? Pure silicon (read back via IN or a jumpered pin) | SD %00111 section; EF-013 covers `%00110` only | to write | sources silent |
| VO-G006b | G-006 | NCO frequency interval jitter (cycle-to-cycle) at a non-integer ratio — catalogue only if it needs an instrument | SD %00110/%00111 sections | to write (or catalogue) | sources silent |
| VO-F337 | S-325 | smart pin off, DAC_MODE `%TT=00`: DIR×OUT four arms — DAC on DIR alone? ADC on OUT alone? | DS `:1175`, `HW:897` vs `part4-smart-pins.txt:83` · EF-071 covers the smart-mode row only | to write | sources disagree |
| VO-S367 | S-367 | do ADC-scope (`%11010`) and ADC-external-clock (`%11001`) smart-pin modes need the ADC enable bits (M[12:10] = %100) to sample? Compare `P_ADC_SCOPE` alone vs `P_ADC_SCOPE \| P_ADC_1X` on a pin fed by a DAC pin (jumper, free pins) | SD smart-pin %11001/%11010 sections · the page's own PASM literal (`:77`) carries the bits · no statement either way | to write | sources silent |
| VO-S157 | S-157 | what does `DEBUG(C_Z)` print after a Spin2 statement (e.g. `x := 0`) — the interpreter's flags at the interrupt, or anything tied to the statement? No pins | v55:913, :1006; debugger DBG:629-633 (prints bits 31/30 of the interrupt return word) · no source gives values for Spin2 · control v55:1006 | to write | sources silent on values |
| VO-S059 | S-059 | with `x := 0`, what do four successive `??x` return, and what is `x` after? Control `x := 1`. No pins (DEBUG read-out) | `seed\|zero\|period\|never` near `xoro32\|xoroshiro32\|??` · SD, DS, v55, v51, PASM2 manual, HW manual, INT, EF ledger · control DS:1557 | to write | sources silent |
| VO-S337 | S-337 | a pin driven high in output mode (`P_HIGH_150K` on P0) while jumpered to a pin driven low (P1): does INA[0] read the pin or the output latch? | SD:3706 states only "the pin's read state" | to write | sources silent on the latch case |
| VO-S037 | S-037 | does `COGATN(1 << COGID())` deliver an attention event to the issuing cog (POLLATN/WAITATN)? No pins | `own\|self\|itself` near `attention\|COGATN` · `sources/` · control SD:2020 | to write | sources silent |
| VO-S304 | S-304 | PWM_TRIANGLE / PWM_SAWTOOTH with `X[15:0] = 0` and with `X[31:16] = 0`: what base period and frame count result? (second smart pin on a jumper, free pins only) | `65,?536`, `X.[15..0]` · `silicon-doc-text.txt` PWM sections `:4034-4067` · control: `:3925` (DAC/NCO "zero = 65,536") | to write (step 8) | sources silent |

## 6. Not read, and why

Stated by the reviewers in each batch's NOT CHECKED, gathered here:

- **No PNut runs.** Every compiler fact is PNut-TS v1.55.8; where PNut might differ the question is on
  `DRAFTS/PNUT-TS-PUNCH-LIST.md` items 5–11 (Stephen's machine). Rows S-147, S-251, S-280, S-345, S-354,
  S-368 wait on them.
- **No silicon runs.** Run-time claims rest on the documents, the interpreter source and EF entries; the
  surviving bench questions (§5) are the planned exceptions.
- **Prose not read end to end:** the hardware add-on pages' `use_cases`/`applications` blocks beyond three
  files (S-374); about 35 smart-pin `TESTP … WC` lines; the full re-derivation of the PASM2
  getting-started guide (F-551, block-level only); the F-545 per-key census; `p2-architecture-mental-model`
  CORDIC figures (S-375). Each is named on its row as sprint work.
- **Documents not held:** the #64013 RTC and #64006F Serial Device schematics (S-322); the #64009/#64010
  example archives (G-015); the mikroBUS specification (G-022, Q-010); ISSI/APS chip datasheets (S-320).
- **Designer-only:** G-029 / Q-011 (LUT as a smart-pin data source).
- **Out of scope by agreement (§1):** manual/PDF-head items, MCP-server items, ENH-01/02, and the
  PENDING-VALIDATION register entries (read only where a sweep passed through their files).

## 7. Hand-off to `sprint-plan`

*(filled when planning closes)*
