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

0. [ ] **Ingestion prerequisites** (through `ingest-source` only):
   - [x] (a) ingest the v55 Spin2 interpreter — **done 2026-10-09 («#401»):** new edition at
     `engineering/ingestion/external-inputs/source-code/spin-interpreter/v55/` (byte-identical;
     PNut-TS v1.55.8 embeds exactly its compiled image); delta in
     `sources/spin2-v55/spin-interpreter-v55-delta-analysis.md`;
   - [x] (b) confirm which debugger is current — **done:** the v51 debugger source is current for
     v55 (PNut-TS v1.55.8 embeds exactly its compiled image). No document is missing;
   - (c) audit the operator ingestion: glued, missing or invented operators, and the `&lt;`/`&gt;`
     entities in `spin2-v55-text.txt`.
1. ~~Group E, field-report reconciliation~~ (dropped: every field report has been processed).
2. [ ] **Group A**, decided items: F-359, F-375, F-398, F-381 (24 files), F-547 cascade.
3. [ ] **Group B** by KB area: architecture, then language/spin2, then language/pasm2, then
   hardware, then guides.
4. [ ] **Group C**, knowledge gaps: the sources searched exhaustively for each one.
5. [ ] **Group D**, the bench queue: re-checked against the sources.
6. [ ] **Group F**, gate specs.
7. [ ] **Group G**, a class sweep per row (done as each row is read, and ticked here when the last
   row's sweep is in).
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

*S-001..S-003 were found by the ENH-03 design probe («#399»); the compiler is the authority for
legality only. Their class (PASM2 written as Spin2) gets a class sweep in G.*

## 4. Root-cause groups

*(filled as rows accrue)*

## 5. Bench questions

| VO id | Row(s) | Question | Sources-silent proof (terms · files · control hit) | Test file | Status |
|---|---|---|---|---|---|

## 6. Not read, and why

*(filled at hand-off)*

## 7. Hand-off to `sprint-plan`

*(filled when planning closes)*
