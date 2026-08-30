# YAML release change ledger — `v1.17.0..HEAD`

**Purpose.** Everything that differs in `deliverables/ai/P2/**/*.yaml` between the last release and
HEAD, with the reason it changed and **what was absent that let the defect exist**. Written for a
release review; the question it answers is *"is it safe to ship, and what did we lose that I cannot
see from a diffstat?"*

**This document shows CURRENT differences only.** An item that has been fixed is **gone from here**,
not annotated as fixed. If you want the history of what was once outstanding, read the archived
predecessor named below and the git log — not this file.

**Range.** `v1.17.0` (`7ff76b30`, 2026-08-21) `..` `efc683a8` (2026-08-29).
**Re-derived on disk 2026-08-29.** Every count below was measured from git and from the parsed YAML
at HEAD. *(The 2026-08-27 revision of this document measured the range ending at `b466a538`; the
2026-08-29 pre-release fix pass added three commits touching KB YAML — §1.18 — and every count in
§0.1, §0.4 and §0.5 was re-measured, not adjusted.)* Where a project record, a commit message or a companion analysis disagrees with the
artifact, the artifact is reported and the disagreement is named (§0.2).

**Supersedes** `engineering/analysis/2026-08-25-yaml-release-change-ledger.md`, archived to
`engineering/analysis/archived/2026-08-25-yaml-release-change-ledger.md`, **byte-identical to its
last committed revision** (`git show HEAD:… | cmp -` returns clean). *Note the path is `archived/`,
not `archive/`: `.gitignore:179` carries a bare `archive/` rule that matches any directory of that
name anywhere in the tree — archiving into one would have silently dropped the document out of
version control, which is the opposite of what an archive is for.* That document measured
**61 files / 11 commits** and was correct when written; 28 more files and 13 more commits landed
after it. It was **re-derived, not patched** — hand-patching a derived document preserves exactly
the drift this re-derivation exists to remove.

**Two views of the same facts.** Part 1 groups by *reason* — a class usually crosses regions.
Part 2 goes region → file, all 92, **each carrying its differential-read verdict**.

---

## Part 0 — Scope, reconciliation, gate state, and what is still open

### 0.1 Scope, measured at HEAD

| Quantity | Measured | Command |
|---|---|---|
| Commits touching KB YAML | **27** | `git log --oneline v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml' \| wc -l` |
| Commits in the range, all paths | **118** | `git log --oneline v1.17.0..HEAD \| wc -l` |
| YAML files changed | **92** | `git diff --name-only v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml' \| wc -l` |
| Lines | **+6363 / −3402** | `git diff --numstat … \| awk '{a+=$1;r+=$2} END{print a,r}'` |
| New files | **4** | `git diff --diff-filter=A --name-only …` |
| Deleted / renamed files | **0 / 0** | `git diff --diff-filter=DR -M --name-status …` |
| Shipped set size | **1129 → 1133 files** | `git archive` both revisions, count `*.yaml` |
| Region spread | hardware 27 · architecture 14 · language/spin2 15 · language/pasm2 12 · architecture/streamer 8 · architecture/smart-pins 4 · architecture/boot-rom 4 · application-notes 4 · guides 2 · code-examples 1 · architecture/system-registers 1 | `… \| awk -F/ …` |

The four new files: `architecture/pin-drive-configuration.yaml`,
`architecture/streamer/pin-capture.yaml`, `hardware/addon-click-adapter.yaml`,
`hardware/p2-package-mechanical.yaml`.

**Out of scope, named once so their absence from Part 2 is not read as an omission.**
`deliverables/ai/P2/CHANGELOG.md`, `deliverables/ai/P2/README.md` and `deliverables/ai/README.md`
changed in this range and are not YAML. `deliverables/ai/p2kb-index.json` and its `.gz` are
regenerated artifacts, not content. And **one commit in the range is not this release's work**:
`7be432a6` ("pnut-ts 015504, and the Dockerfile no longer names the version") belongs to another
session and touches no KB YAML.

### 0.2 Reconciliation — every number that disagreed, and why

Nothing here is a defect in the artifact; each is a measurement taken at a different revision or by
a different method. Recorded because a stale count is what sent this document back for re-derivation.

| Source | Its number | Measured at HEAD | Why |
|---|---|---|---|
| The archived 2026-08-25 ledger | 61 files, 11 commits, 1 new file, +3770/−2751 | **89 · 24 · 4 · +6246/−3355** | It was right at `0a5323ab`. Thirteen commits landed after it. |
| `2026-08-26-yaml-differential-read.md` | 85 files, 81 modified / 4 added, +6137/−3341 | **89 · 85/4 · +6246/−3355** | It measured at `4caeb6cc`. The four files added since are `language/pasm2/{addsx,subsx,sumc,sumz}.yaml`, all from `b466a538`; `ca07aaf7` moved lines without adding files. **85 + 4 = 89, reconciled exactly.** |
| `2026-08-26-yaml-shape-change-consumer-audit.md` | 34 keys / 24 files / 23 `list→dict` / 11 `str→dict` | **34 · 24 · 23 · 11 — reproduced independently at HEAD** | No drift. Re-measured by parsing every top-level key of every changed file at both revisions and comparing `type()`. |
| `15c84de5`'s own subject line | "59 uncited quantitative blocks" | **60** | The commit's own body and `597d5eba`'s body both say 60; the subject is off by one. Measured as a key-set delta across the commit. |
| `491f2b55`'s own body | "Of the 59 blocks … 34 return … 24 stay" | 34 + 24 = **58** | One hardware block is unaccounted for in that commit's arithmetic. Not reconciled here; the HEAD-side key-set delta (§0.3, 41 keys) is the reliable instrument. |
| `11ebec54`'s commit message, and this task's own dispatch | "validate-dod-release: **12** checks" | **11** | The script's `validations` list holds eleven functions (`validate-dod-release.py:661-673`); its output prints eleven named checks plus a summary line. It held **nine** at `v1.17.0`; the two content gates armed by `43b0ede2` took it to eleven. It has never been twelve. The shape-change audit's own §6 also records eleven. |
| `2026-08-26-yaml-differential-read.md` §8.6 | `audit-register-hygiene.py … P1-CORRECTION-FINDINGS.md` remains exit 1 `no-counter` | **exit 0, CLEAN** | Repaired after that read, by `d62544ea`. Both P1 registers now name their allocators. |

### 0.3 The block accounting — where the content went

The two purges removed **top-level YAML blocks**, and that is the unit everything else counts in.
Measured by parsing the top-level key set of every file at each commit's parent, at the commit, and
at HEAD.

| Movement | Measured | Detail |
|---|---|---|
| Blocks removed by the purges | **119**, across **41 distinct files** | 60 (`15c84de5`, 25 files) + 59 (`c733a223`, 17 files); one file appears in both |
| Blocks returned carrying a citation | **80** | 46 (`597d5eba`, 24 files) + 34 (`491f2b55`, 15 files) |
| Blocks removed *by the repopulation* | **1** | `hardware/edge-32mb-module.yaml alternate_part` — the fabricated `64000-ES` part number, deleted with a note saying why |
| **Top-level keys present at `v1.17.0` and absent at HEAD** | **41, across 18 files** | the reliable instrument: a strict key-set delta at HEAD, immune to any intermediate churn |

**Disposition of the 41** — carried from the differential read §3 and checked here: every key it
names appears in the HEAD-side delta, and the three groups sum to 41 exactly.

| Disposition | Keys | Where |
|---|---|---|
| **Fabricated / disproven** — no source states it, and several are contradicted | **15** | `io_pin_timing` ×8 · `{pasm2,spin2}/concepts/basic-io` ×3 each · `p2-eval-board video_audio` |
| **True but not actionable** — cannot change emitted code; verified present in the ingestion tree | **24** | all in `hardware/`, across 13 files |
| **Authored here, no upstream** — correct, actionable, unsupportable by anything we hold | **2** | `io_pin_timing best_practices` · `click_module_integration best_practices` — **F-352, open** |

The differential read separately estimates **1930 leaf facts across 73 files** whose value string
appears nowhere in the shipped KB at HEAD, and states plainly that this over-reports: a reworded
fact counts as absent. It is quoted here as a *candidate* population, not a loss figure. Not
re-derived in this document.

### 0.4 Gate state at HEAD — all eight run, none quoted

| Gate | Result | Exit |
|---|---|---|
| `verify-yaml-format.py` | 1133 scanned, 1133 parsed clean, 0 failures | 0 |
| `validate-crossref-keys.py` | ALL TOP-LEVEL CROSS-REFERENCES RESOLVE — **698 nested sites NOT checked (F-340)** | 0 |
| `validation/audit-yaml-claim-sourcing.py` | Tier 1 **none** across 1133 files; **32 Tier-2 advisory** blocks in **24** wholly-uncited files (was 48 on 2026-08-27; §1.18 cited three of those files, moving 16 blocks out of the advisory class — and see **F-381**, which is what that move exposed) | 0 |
| `validation/audit-constant-fidelity.py` | Tier 1 none, Tier 2 none, across 120 source-defined constants; truth side 35 files, editions `spin2-v51` + `spin2-v55` | 0 |
| `validation/audit-extraction-digit-density.py --all` | CLEAN, 65 artifacts at or above the 20% floor, 4 declared exempt | 0 |
| `validation/audit-yaml-duplicate-keys.py` | 1132 scanned, **0 files with duplicate keys** | 0 |
| `validation/audit-register-hygiene.py` ×3 | corrections **105 live / 294 archived / 0 unaccounted**, next `F-382` · gaps **36 live**, next `G-28` / `Q-10` · errata **17 live**, next `E-18` | 0, 0, 0 |
| `validate-dod-release.py` | **11 checks, all PASS** — READY FOR RELEASE | 0 |

`deliverables/ai/p2kb-index.json.gz` decompresses **byte-identical** to `p2kb-index.json`
(`gzip -cd … | cmp -s - …`). That pair drifted for four days as **F-357**; it is in sync, and it must
be regenerated *after* the content commit because the index stores the **git blob** sha256.

⚠️ **What these greens do not certify, and each instrument says so itself.** The sourcing gate
checks that a citation is *present*, never that it is *right* — nothing here opens the cited
document. F-359 established that a **fabricated** provenance header satisfies that same regex, and
F-377 that a locator can be in range and still point at the wrong line. The constant gate checks
*named constants*; name coverage is not semantic coverage. `b466a538` is the current proof: four
files that parsed, resolved, carried citations and assembled under `pnut-ts` while each contradicted
itself about a flag's meaning. **No instrument in this project can read a sentence.**

**2026-08-29 adds a second, sharper proof, and it is the reason to distrust a green here.** §1.18
recomputed the SETXFRQ NCO class instead of re-reading the two values a prior pass had named. Nine
shipped values were wrong — an off-by-one in bit 0 of a 31-bit phase word — in files that parsed,
resolved, carried correct citations, and **quoted the very rule they were violating**. Every gate in
this table was green before that fix and is green after it. The same pass found the KB describing the
64-bit system counter as 32-bit, and a `~1-2 ns` smart-pin figure that exists in no Parallax source.
None of it was detectable by any instrument listed above. **Read this table as "not caught by these
checks", never as "correct" — the gates themselves say so in their own closing banners.**

### 0.5 What is still open — the pre-ship list, as it actually stands at HEAD

This replaces the twelve-item checklist the archived ledger carried. Nine of those twelve are gone
because they were fixed (`getct` description, the E-010 pull-up, `digital_io_board`, the
EF-063/EF-064 attribution, the shape-change question, `edge-breadboard-carrier`'s missing supply
figure, `addon-serial-host`'s identity string, both duplicate keys, and the `1224` symbol count).
What follows is what a release reviewer would still hit.

**🔴 Needs Stephen — the release cannot decide these itself**

1. **Eight claims that could not be re-derived are still standing in the shipped files.** «#323»
   re-derived six fabricated-provenance `architecture/` files against the live silicon doc and
   found the header was the signature, not the extent — 41 of 45 encodings wrong, four mnemonics
   that do not exist, six semantic inversions. Eight further claims survived: LUT power figures,
   LUT bandwidth restated from instruction timings, a lock "state bits: 4" width no source gives, a
   trace-buffer size, a debug-state size the source contradicts, a streamer-disruption claim the
   source rebuts, and a `0 clocks` WAITATN latency the datasheet gives as `2+`. They were
   **collected rather than deleted, because deletion is his.** Enumerated in **F-359**.
2. **F-367 — two different documents under one filename.** `external-inputs/p2/` and
   `sources/silicon-doc/` hold Silicon Doc DOCX copies that differ in 972 characters across four
   sites, including a GETBRK `WZ` semantic where one copy sets `Z = 1` in both branches. The
   `sources/` copy is demonstrably the right one and is what every extraction used, so nothing
   downstream is wrong. `b466a538` labelled `external-inputs/p2/` a staging area and wrote the
   mapping README; **reconcile-or-delete is his.** `CONFIRMED`.
3. **F-375 — both delivery paths strip `documentation_source:`, and 706 of those values are real
   citations, across 383 files.** The shipped set satisfies *cite-or-omit* on disk and is delivered
   not satisfying it. Every gate reads the tree; the consumer reads the filtered stream; nothing
   compares them. The remedy is a 383-file rename, which is a scope call, not a repair to start
   unasked. `CONFIRMED`.
4. **`ENH-NN` is an ungoverned allocator that has already collided.** The corrections register
   carries a third ID series with no declared counter, and live `ENH-02`/`ENH-03` name different
   proposals than the archived `ENH-02`/`ENH-03`. `d62544ea` made the hygiene gate print
   `unmodelled series : ENH-NNN` on every run without failing on it. Renumbering the live entries
   and inventing a proposal-status vocabulary are his calls.

**🟠 Real defects in the shipped set, scoped and unstarted**

5. **F-377 part 1 — translated locators. STILL OPEN — this is the largest unstarted item.** F-365 re-anchored 23 citations from the superseded
   `p2-documentation.txt` and instructed that line numbers must never be translated; some were.
   `streamer/dds-goertzel.yaml:74` cites `:4062`, a blank line, beside a correct `:1565`. A
   class-wide range check over all **113** `silicon-doc-text.txt` citations returns **0 out of
   range** — a translated locator lands inside the file and reads as valid to anything checking
   bounds. Two more of the same shape in `clock_system.yaml` are **not** F-365 residue, which
   widens the class beyond the 23. Only opening the line catches it. `CONFIRMED`.
6. ~~**F-377 part 2 — an eighth fabricated-provenance file.**~~ **CLOSED 2026-08-29 («#333»,
   §1.18).** `architecture/io_pin_timing.yaml`'s `part3-pins.txt` citation is gone. The content was
   checked and proved genuine, so it was re-anchored rather than removed: the four timing claims now
   cite `silicon-doc-text.txt:1987`, `:1997`, `:2005` and `:3847`, each re-read at the line, and the
   latch-up figure cites `:101` with the note that it comes from ON Semi failure analysis of one
   wafer lot quoted in the revision history, not a characterised limit. Reading the file also killed
   an unsourced `~1-2 ns` smart-pin timing claim and labelled a `5 clocks` total the source never
   states as the sum it is.
7. ~~**F-378 — the KB ships the compiler's acceptance range as a frequency ceiling.**~~ **CLOSED
   2026-08-29 («#334», §1.18)** — and it was five sites, not one. The sweep F-378's own text called
   for found `_CLKFREQ` (500 MHz vs the datasheet's 320), `_XINFREQ` (500 vs 200 for direct drive),
   `_XTLFREQ` (60 vs 50 for a crystal), `clkmode.yaml`'s "up to 500 MHz", and a 500 MHz row in
   `timing_operations.yaml`'s rollover table. All five now state the compiler range labelled as the
   compiler range, the datasheet rating beside it, and the Silicon Doc's 350 MHz `VCO / 1` overclock
   ceiling — three different numbers a reader was previously handed as one. **Superseded text
   follows for the record only:**
   `language/spin2/constants/special-configuration-symbols.yaml:59` gives `_CLKFREQ` a range of
   3,333,333 Hz to **500,000,000 Hz**, unlabelled. That is pnut-ts's acceptance range; the
   datasheet's PLL absolute maximum is **320 MHz**. An agent reading only that entry emits a
   `_clkfreq` up to 500 MHz, compiles clean, and ships silicon 180 MHz past the datasheet maximum.
   **The file is not in this release's change set** — it is a standing defect this sprint found, not
   one it introduced. E-007's label-which-framing rule applies and was never applied here.
   `CONFIRMED`.
8. **F-373 — three top-level fields are typed `text`, so a file path in any of them is never
   resolved.** `see_also`, `references` and `related_concepts`; 14 shipped file paths sitting in them
   point at nothing, and `validate-crossref-keys.py` stays green. Companion to F-340's 698
   unchecked nested sites. `CONFIRMED`.
9. **F-374 — 40 quality-score sites across 18 shipped files state a judgement, not a fact.**
   Star ratings and scores that the KB entry rule (existence · access · utility) excludes and no
   source authorises. `CONFIRMED`.
10. **F-372 / G-027 — the USB smart-pin entry states as fact a sentence the DOCX edition dropped.**
    *"A new WRPIN can be done to effect such a change without resetting the smart pin"* exists in
    the PDF-era capture of v35 and is absent from the DOCX capture of the same document, which
    states the opposite general rule. The KB now carries the conflict rather than deleting the
    claim, since it may well be right. **Bench-testable and jumper-only.** `CONFIRMED`.
11. **F-352 — two shipped areas are authored-here with no upstream anywhere.**
    `io_pin_timing best_practices` and `click_module_integration best_practices` were removed as
    uncited and cannot be restored without manufacturing provenance inside the fidelity gate's
    truth root (the defect F-341 files). The removal rule has no branch for *correct, actionable,
    unsupportable*. `CONFIRMED`.
12. **F-354 — seven content-level holes inside blocks that DID come back**, recorded at the point of
    use rather than in a separate document, plus one held block only three-quarters present in the
    ingestion tree. `CONFIRMED`.

12b. **F-381 — the Tier-2 advisory class is "no control available", not "reviewed and accepted",
    and it hides uncited quantity blocks from the blocking gate.** Proved by accident on 2026-08-29:
    adding silicon-limit citations to three clock files took `audit-yaml-claim-sourcing.py` from
    **0 Tier-1 violations to 12**. Nothing broke. Those files had cited *nothing anywhere*, which
    parks every quantity block in Tier 2; the gate judges a block against **its own file's other
    sections as the control**, and a wholly-uncited file supplies none. One real citation turns the
    rest of the file red. The 12 were always uncited — they were merely invisible. **32 advisory
    blocks across 24 files remain in that state** — **measured, not inferred**: a simulation
    inserting one recognised citation into each of the 24 files returns exactly 32, matching the
    advisory count. *(Corrects the 2026-08-29 wording, which called 32 a floor. Census §2.)* The 24 split
    into ordinary citation debt (8 smart-pin mode pages, 6 clock/timing language files) and content
    that may need a *declared exemption* rather than a citation (3 OBEX object-metadata files,
    5 `architecture/decomposition/` reasoning-layer files, 2 hardware guides — one of which is
    already item 17 below). **Deciding which is a scope call, not a repair to start unasked.**
    `CONFIRMED`.

**🟡 Residues named by the differential read and still open at HEAD** — each re-checked in the tree
today; the two that `ca07aaf7` closed have been dropped from this list.

13. ~~`language/pasm2/setxfrq.yaml common_values` — two of four values…~~ **CLOSED 2026-08-29
    («#332», §1.18), and the class was eight times the size recorded here.** This entry named 2
    values in 2 files. Recomputing the whole class instead of re-reading the named values found
    **9 wrong in the shipped KB** (setxfrq 2 of 4, `nco-timing.yaml video_rates` **7 of 12**) and
    **8 more in the published Streamer Guide v1.1.0**, which also taught the rule as `round()` in
    three places. Filed **F-380**. ⚠️ **A Streamer Guide re-release is owed** — the master is fixed,
    the shipped PDF is not. *This is the clearest instance of the counting lesson in §0.6.*
14. `application-notes/p2an004-…yaml` contradicts itself: `:111` says the sensor's electrical
    figures are "deliberately not restated here", `:87` restates them, `:127` cites the datasheet by
    document number.
15. Inconsistent treatment of derived arithmetic inside one region: `p2an003` deleted
    `200 MHz / 256 = 781_250 sps` as a derivation, while `p2an001:80` keeps
    `raw_sample_rate_sps: 1_562_500  # 200_000_000 / 128`, the identical construction, uncited.
16. `p2an001…:93` cites `p2-datasheet-text.txt:2199`; the PLL row is `:2200` (`:2199` is the Crystal
    row). Same shape as F-377, different pass.
17. `hardware/p2-hardware-selection-guide.yaml` (all three blocks) and
    `p2-hardware-feature-comparison.yaml selection_criteria` are authored buying-guide content,
    correctly retained under the promotion filter's sub-rule P and **never given a disposition** —
    the same missing branch as F-352.
18. **Two tooling silent-failures (F-376).** `fetch-kb-file.sh -v <KEY>` fetches nothing and exits 0;
    `generate-p2kb-index.py`'s alias harvest ends in `except Exception: pass`, so a syntactically
    invalid file is still indexed with a path and a sha256 while silently losing its aliases, and
    the run exits 0 printing nothing. **A green index generation is not evidence that the corpus
    parses** — `verify-yaml-format.py` is the tool that answers that. `CONFIRMED`.
19. **The duplicate-key gate exists, passes, and nothing makes it run.**
    `validation/audit-yaml-duplicate-keys.py` was armed by `02ff61b7` and returns 0 across 1132
    files — but it is **not wired into `validate-dod-release.py`**, which calls
    `audit-constant-fidelity.py` and `audit-yaml-claim-sourcing.py` as blocking gates and not this
    one. A duplicate key reintroduced tomorrow turns nothing red at release. Named in **F-360**'s
    own closing line as the one thing that entry leaves open.
20. **`validate_metadata_filter` reads the pattern list, not the artifact.** It classifies which
    lines the filter removed and never re-parses the filtered payload, so a block delivered as
    `null` passes it clean. The corpus is clean today (0 of 1133); the gate is measuring the wrong
    thing. Half of F-375. `CONFIRMED`.

**⚪ Known, measured, and NOT blocking**

21. **The shape mixture is deliberate and rule-determined.** 34 top-level keys across 24 files
    changed YAML type (23 `list→dict`, 11 `str→dict`) — re-derived here at HEAD, matching the
    consumer audit exactly. All five consumers were **executed** against the new shapes and each was
    **made to fail** on a shape it cannot handle, so the greens discriminate. The decisive
    experiment: moving the citations to the uniform-shape alternative drives
    `audit-yaml-claim-sourcing.py` to **exit 1 with 22 Tier 1 violations** — the reshape was forced
    by the armed gate, not chosen. And **0 of the 28** blocks still carrying the old shape is one the
    gate would demand a reshape for. Verdict: **MEASURED-SAFE.** What it does not settle is that
    nothing enforces or records the rule; if a schema is ever wanted, that is the rule to write down.
22. **32 Tier-2 advisory blocks** remain in wholly-uncited files (48 on 2026-08-27; §1.18 cited
    three of those files). Advisory by design, non-blocking, and its population is not zero.
    ⚠️ **Re-graded 2026-08-29 — this is no longer "known, measured and NOT blocking".** See
    **F-381** / item 12b: the advisory class is not an accepted exemption, and citing any one of
    those 24 files turns its remaining blocks Tier-1 RED. It is listed here because it does not
    block *today*, not because it has been adjudicated.
23. **698 nested cross-reference sites are never checked** (F-340) and three top-level fields are
    exempt (F-373). `validate-crossref-keys.py`'s exit 0 covers less than it reads as covering.

---

## 0.6 The 2026-08-29 pre-release fix pass — and the counting lesson it kept teaching

**Why there is a second pass at all.** The 2026-08-27 review left this document at release position
with §0.5 as the pre-ship list. Reading that list rather than trusting it turned up defects the list
had *named* but under-counted, every single time. In three consecutive cases the real class was
larger than the entry recorded:

| §0.5 entry | recorded | actually found | ratio |
|---|---|---|---|
| item 13 — SETXFRQ rounding | 2 values, 2 files | **17 values, 3 files** (incl. a published manual) | 8.5× |
| item 7 — F-378 compiler range | 1 site | **5 sites** | 5× |
| item 6 — F-377 pt2 fabricated header | header only | header **+ 2 further defects in the file** | — |

**The lesson, stated so the next pass does not relearn it: §0.5's counts are what the differential
read NAMED, not the size of the class.** The differential read examined the files that changed; a
defect class does not respect that boundary. Every entry here should be treated as *"at least this
many"* and the class recomputed from the rule, not from the list. Three of the four biggest finds in
this pass were invisible to every gate and would have shipped.

**A second-order lesson, from F-381.** Fixing a file can *reveal* defects rather than introduce
them. Citing three previously-uncited files moved them out of the sourcing gate's advisory class and
turned 12 always-uncited blocks into blocking violations. A gate going red after a repair is not
necessarily a regression — check whether the repair changed what the gate can *see* before treating
it as one.


---

# PART 1 — By change class

A class is one *reason*. Each carries: **what** it is · **the lack** — what was absent that let it
exist or persist · the files it touched · the net effect. A class usually crosses regions; Part 2
is the same facts arranged the other way.

---

## 1.1 The uncited-quantity purge — 119 blocks, 41 files

**What.** Every top-level block that stated a physical quantity without naming a source was deleted:
**60** from `architecture/`, `language/`, `guides/`, `application-notes/` (`15c84de5`, 25 files) and
**59** from `hardware/` (`c733a223`, 17 files). Removal moved first, on purpose — the damaged set was
being served while the repair ran, and there was to be nothing to grandfather when the gate was armed.

**The lack.** Nothing had ever asked whether a stated quantity named its source. `io_pin_timing.yaml`
went 433 lines to 175 in one commit, and that included both blocks F-327 proved fabricated **and**
four further ranges F-327's line numbers did not cover — a fix applied literally to those lines would
have left the same ladder standing in two more blocks.

**Two gate defects surfaced *by* the purge, and the first zero was false.** `c733a223` records that
`INLINE_CITE_RE` read `rev B` / `rev C` as a citation — on a board file that is a board revision, and
worst precisely in the tree where every file legitimately names one — and that `CITE_RE` tested the
key name rather than the value, so `source: External 5V power supply` counted as a citation of a power
supply. Both silence rather than over-fire, which is how a purge could report success over eleven
blocks it never looked at. `1f37ae58` then found a third member of the same family: the deferral
*"Check datasheet for package limits"* matching on the token `datasheet`. The generalisation is in
**F-335**: the citation side matched on the presence of a token, not on whether the sentence
attributes the block to a document.

**Two consequences the executing agent could not see**, measured at the boundary: deleting the uncited
`pull_up_modes`/`pull_down_modes` blocks resolved 18 of the 23 drive-strength CONTRADICT rows as a
side effect, and orphaned five constants whose only definition lived inside those blocks — which is
why §1.5 defines 55 rather than 50.

---

## 1.2 Source-first repopulation — 80 blocks returned, cited

**What.** The removed blocks were rebuilt **by reading the source, not the removed block**: 46 return
in `597d5eba` (24 files) and 34 in `491f2b55` (15 files), each carrying the document and a
`file:line` into it.

**The lack.** Nothing had ever required a block to be written *from* a source rather than checked
*against* one. Reading the sources first is what paid beyond the brief, and it paid every time:

* **WAITMS / WAITUS shipped a ceiling wrong by a factor of four hundred.** The files claimed
  1–4,294,967 **milliseconds**; v55 bounds them in **clocks**, at `$8000_0000`, which at 200 MHz is
  under eleven seconds. That is the kind of wrong a long delay discovers at runtime.
* **A restored guide block claimed ORG's cog limit as `$1F0`.** v55 says `$1F8`.
* **A boot block claimed the ROM issues no `HUBSET` before jumping.** Its own listing contradicts it;
  the `Prop_Clk` and shutdown paths both do.
* **The PLL lock conflict settled at 10 ms, not ~10 µs** — three Parallax documents state it on two
  extraction paths each, all three emit `WAITX ##20_000_000/100`, and v55 states it twice more. The
  microsecond figure has no source at all. Settling it turned up a **fifth** site the finding never
  named: two `clock_system` examples waiting 100 µs, invisible to the gate because it strips code
  regions before scanning.
* **The `alternate_part: 64000-ES`** on `edge-32mb-module.yaml` was deleted *by the repopulation*,
  with a note saying why — it is the only block the repopulation removed.

---

## 1.3 The 41 blocks that did not come back — three different outcomes, kept apart

Collapsing these into one number would say we could not verify content we know is fabricated.
The strict key-set delta at HEAD is **41 keys across 18 files** (§0.3).

**(a) Fabricated or disproven — 15 keys.** `architecture/io_pin_timing.yaml` ×8
(`timing_specifications`, `clock_relationships`, `drive_strength_configurations`, `slew_rate_control`,
`input_characteristics`, `special_timing_modes`, `protocol_timing_examples`,
`compensation_techniques`); `language/pasm2/concepts/basic-io.yaml` and
`language/spin2/concepts/basic-io.yaml` ×3 each (`drive_strength_configuration`,
`timing_considerations`, `hardware_specifications`); `hardware/p2-eval-board.yaml video_audio`.

The falsification was run against the **completed** Silicon Doc extraction, not the earlier partial
one: `slew` returns **0** hits across `silicon-doc/`, `p2-datasheet/`, `p2-hardware-manual/`,
`smart-pins/` and `spin2-v55/`; so do `fall time` and `FR4`; `VIL`/`VIH` return **0** in the datasheet,
the Silicon Doc and the Hardware Manual. `Schmitt` appears 103 times — always as an input **mode**
(`Pin Schmitt`, `P_SCHMITT_A`), never as a threshold. **The mode is documented and is in the KB; its
electrical characterisation is documented nowhere and is correctly absent.**

**(b) True, and still out — 24 keys, all in `hardware/`.** Ruled correct but *not actionable*: they
cannot change the code an agent emits. Each is verified present in the ingestion tree, so nothing is
lost — it is not shipped. Across `addon-hd-audio` (2), `addon-hyperram-hyperflash` (1),
`addon-motor-driver` (2), `addon-rtc` (2), `addon-serial-device` (2), `addon-serial-host` (3),
`addon-wx-wifi` (2), `edge-32mb-module` (1), `edge-breadboard-carrier` (3), `edge-mini-breakout` (2),
`edge-standard-breakout` (2), `edge-standard-module` (1), `hub75_adapter` (1).

One of them came **back** later by a different route: `addon-wx-wifi part_variants` carried the
DIP-to-Activity-Board mapping, and `599d3660` recovered that content from the ingestion tree into a
cited `form_factors` block. The key name did not return; the fact did.

**(c) Authored here, no upstream — 2 keys. This is the open gap.** `io_pin_timing best_practices` and
`click_module_integration best_practices` are correct and actionable, and **nothing we hold supports
them**. Writing them into the ingestion tree to cite them would manufacture provenance inside the
fidelity gate's documentary truth root — the exact defect F-341 files. **F-352** records that the
removal rule needs a fourth branch for authored-here content with no upstream. Still open.

---

## 1.4 The drive-strength mislabel — the class this sprint started from

**What.** The P2 has **no pull-up or pull-down resistors.** `P_HIGH_*` / `P_LOW_*` select **drive
strength**, and the shipped KB described them as bias resistors — so an agent asking how to enable a
pull-up was handed a mechanism the silicon does not have. That was the reported symptom.

**The lack.** One fact written in many places, with no single home, and no instrument that reads a
sentence. The purge had already resolved 18 of the 23 CONTRADICT rows by deleting their blocks; the
remaining five were reworded from the v55 table, and the structural half is **deletion and
repointing**, not rewording in place: no file restates the mechanism, and each carries a full-path
reference to the single definition home.

**Files.** `language/spin2/methods/{pinfloat,cogstop,wrpin}.yaml` ·
`language/spin2/conventions/{johnny-mac-documentation-style,spin2-docs-jonnymac}.yaml` ·
`language/{pasm2,spin2}/concepts/basic-io.yaml` · `guides/{pasm2,spin2}-getting-started.yaml` ·
`code-examples/smart-pins-002-button-reading.yaml` ·
`architecture/smart-pins/smart-pin-00000-normal-mode.yaml` · `hardware/addon-control-board.yaml` ·
`hardware/addon-rtc.yaml` · `hardware/edge-{32mb,standard}-module.yaml` ·
`architecture/pin-drive-configuration.yaml` (new).

**What reading the examples found, beyond the mislabel.** Nine examples were extracted from the
shipped YAML **bytes** rather than retyped, compiled, and then read for semantics — which is the whole
point, because F-322's examples all compiled and were all wrong. The reading found a `TESTP` whose
comment inverted the flag polarity so the handler ran on the wrong half; a `JMP #$` self-jump that
blinked once and hung; an `ORG` followed by data so execution began on a LONG; a setup routine
nothing called; and a glitch rule that contradicted both of its own examples. Filed as F-345/F-346.

**Two residues this sprint killed after the fact.** `75971308` removed E-010 from the shipped set —
both Edge Module files said the LEDs could be held by *"enabling a pin pull-up"*, and **both lines
had been rewritten in this release with the phrase intact**, which is how it survived. And
`ca07aaf7` dropped "pull resistors" from a routing blurb in `spin2-getting-started.yaml`, honest now
that `basic-io.yaml` states the P2 has no internal pull network.

**Two findings went to Parallax rather than into the KB** (F-342, F-344): the RTC add-on guide itself
teaches the mislabel and prescribes it in input mode, where a drive selection cannot do anything; and
an eval add-on guide calls a switch active-high and says the pin is driven low when asserted, in one
sentence.

---

## 1.5 One definition home, and the aliases that made it reachable

**What.** The KB referenced **55 constants it defined nowhere.** All 55 are now defined, worded from
the Spin2 v55 table rather than the v51 extracts (superseded for eight of them), in one file that
covers all 116 v55 constants, each defined exactly once. Seventeen duplicate definitions in
`language/spin2/methods/wrpin.yaml` and `architecture/smart_pins.yaml` were replaced with **pointers
rather than corrected**, because F-321 and F-323 exist precisely because one fact was written twice
and the copies drifted. Six one-line restatements in `language/pasm2/wrpin.yaml` went the same way.

**The lack — and it is the mechanism behind the whole sprint.** `generate-p2kb-index.py` harvests
top-level `aliases:` **only**, and the symbol file had none. Not one of its 48 existing constants
resolved through `p2kb_get`, and 55 more would have satisfied the gate while leaving the reporting
agent exactly where it started. A top-level `aliases:` block of 116 names fixes that at the mechanism.
`ad4f974f` then found seven `streamer/` files with no aliases at all — unreachable by name — and gave
them some.

**The new `architecture/pin-drive-configuration.yaml` states its facts by ENCODING, never as
name-to-description**, and that shape is deliberate: the fidelity tool reads a constant name used as a
YAML key as a *definition*, so the natural spelling would have created a second definition home for
sixteen constants inside the task chartered to end that defect. Verified against the tool's own
regexes, not by eye.

**Two fabricated names deleted with nothing substituted.** `P_LEVEL_B` and `P_SCHMITT_B` are rejected
by `pnut-ts` while seven real siblings compile, and v55 carries only their `_FB`/`_FBP`/`_FBN` forms.
**F-340** records how they survived: the crossref validator reads top-level keys only, so nested
`related_symbols:` lists have never been checked — they were not missed by bad luck, they sat in a
field the instrument does not read.

---

## 1.6 The fabricated-provenance class — six files re-derived from scratch

**What.** **F-359** established that seven `architecture/` files carry a provenance header citing
silicon-doc files that have **never existed** (`part3-pins.txt`, `part1-cog.txt`) and datasheet page
ranges beyond the end of a 50-page datasheet — all written in one 2025-11-29 commit that touched
1,323 files and 973 YAMLs. One was purged this sprint; `9a1f14a3` **re-derived the other six** against
the now-complete silicon doc.

**The header was the signature, not the extent.** Across the six files:

| | Before | After |
|---|---|---|
| `- instruction:` entries carrying an `encoding:` | 47 | 45 |
| encoding **verbatim-identical** to the silicon doc's PASM2 encoding table | **2** | **45** |
| encoding **wrong** | **41** | **0** |
| mnemonic **not in the encoding table at all** | **4** | **0** |

**The semantic inversions, each of which a code-generating agent would have acted on:**
`interrupts.yaml` had the **IJMPx/IRETx address map inverted** — `$1F0` called IJMP1 where three
authorities say IJMP3; it also claimed per-level **shadow registers**, of which there are none.
`lookup_ram.yaml` had **LUT sharing backwards** (it is a WRITE path into the paired cog's LUT) and
**WRLUT's operands reversed** (D carries data, S carries address). `locks.yaml` carried a `LOCKTRY`
"query" form that actually **acquires**. `cog_attention.yaml` had **ATN as event 15**; it is 14, and
both SETINTx examples used the wrong number. `debug_interrupt.yaml` invented three "configuration
registers". `event_system.yaml` carried an invented event taxonomy in place of the sixteen the source
enumerates, and its pattern-match example selected **mismatch** mode while its comment said match.

**Four fabricated mnemonics deleted** — `RDCOGID`, `RDLUTS`, `NIXINT0`, `TRGINT0` — each checked three
ways first: absent from the silicon doc, absent from every other file under `deliverables/ai/P2/`, and
not accepted by `pnut-ts` v1.55.3, with `cogid` compiling clean as the control. Each site keeps a note
saying what was removed and why, so nothing restores them.

**The lack.** Nothing checked generated content against a source at creation time, and **the citation
header was generated along with the content it claims to source**. A fabricated citation is not an
error in sourcing; it is the signature of never having sourced. 973 YAMLs in one commit is the scale
at which that becomes invisible. 🔴 **And the gate is not the evidence:** `audit-yaml-claim-sourcing`
read `0 Tier 1` before this work and reads `0 Tier 1` after it, because none of the six carries a
unit-bearing quantity block. The evidence is that every `<file>:<line>` written into them was re-read
at the line it names. The instrument was separately shown live on these files — a planted two-quantity
block in `locks.yaml` produced `TIER 1 … 1 violation` and exit 1; removing it returned exit 0.

**Still open from this class:** the **eight non-derivable claims** (§0.5 item 1, F-359) and the
**eighth file** the list never contained (§0.5 item 6, F-377).

---

## 1.7 Wrong scalars and invented board identities — what a source-first read exposed

**What.** Reading the guides instead of the removed blocks found defects in blocks that had **survived
both purges**, because a purge keyed on missing citations does not find a wrong scalar or an invented
section.

* 🔴 **`max_current_per_pin: "150mA"` in both `basic-io.yaml` files.** The datasheet's absolute
  maximum is **±30 mA**. That is five times the limit, in the exact number a reader uses to size an
  LED series resistor, and following it damages hardware. The same block carried `VOL 0.4 V` /
  `VOH 2.4 V`, which are 5V-TTL figures. Both copies deleted; the correct facts already ship, cited,
  in `io_pin_timing.yaml`.
* 🔴 **`#64006G` was described as a Combined Digital I/O board** with four LEDs and four switches.
  `#64006G` is the **Goertzel** board; the LEDs and switches belong to `#64006A`. An agent generating
  code against that entry gets pin assumptions for a different board entirely. The corrected file
  still named the invented `digital_io_board` slug in two guidance lists afterwards; `75971308`
  removed it, and sweeping that class found two more slugs naming no board at all (`eval_board`,
  where the key is `p2_eval_board`, and `breakouts`). **Nothing validates these lists**, which is why
  a fabricated name lived there.
* **Invented carrier part numbers** where real ones exist · a carrier dimension off by a factor · a
  mini breakout credited with all 64 pins on castellations · an eval board given a barrel jack it
  does not have · a fabricated "USB connector onboard" on two breakouts · a false "all add-ons use
  P0-P7" in the compatibility matrix · a fabricated `alternate_part: 64000-ES`.
* **`p2-eval-board.yaml`**: Rev D → Rev C, 320 MHz → 180 MHz recommended, the real flash part,
  3.55 in, and roughly ten `TBD` placeholders replaced with sourced values.
* **`hub75_adapter.yaml`**: the manufacturer's **70 MHz** replaces the unsourced 40/35 MHz.

**The lack.** No instrument reads a scalar for plausibility, and none reads a board name for
existence. Both classes are caught only by reading the guide.

---

## 1.8 Not-actionable content removed — the promotion filter

**What.** `1f37ae58` asked a question neither purge asked: not whether a block is true, nor whether it
is cited, but **whether it can change the code an agent emits.** 233 blocks across both populations
were given a written disposition — 114 that survived the purge, and 119 the purge removed that the
repopulation would otherwise have had to re-decide.

**The lack.** The KB had no stated rule for *correct but useless*. Quality commentary is the clearest
case: `waitus.yaml`'s removed content was "excellent / good / marginal resolution" — a judgement, and
the KB entry rule states existence, access and utility, never quality.

**Still un-dispositioned** (§0.5 item 17): `hardware/p2-hardware-selection-guide.yaml` and
`p2-hardware-feature-comparison.yaml selection_criteria` were correctly *retained* under sub-rule P
and never given a disposition — the same missing branch as F-352.

---

## 1.9 Citation paths — the ones that route every new agent, and 23 that pointed at a dead artifact

**What, part one (`69af3733`).** Both getting-started guides tell an agent that
`concepts/basic-io.yaml` is required reading before any I/O work — **and two real files answer to that
name**, so the citation pointed at nothing deterministic, straight at the files carrying the broken
pull-up examples. Each guide declared a `content_base` that would disambiguate and then refuted it
three lines earlier, with one path base-relative and its neighbour P2-root relative **in one block**.
The citations were right by the luck of the reader's guess. Fourteen bare paths across the two guides
are now repo-absolute, six more inside the `basic-io` files with them, and each `content_base` carries
a comment saying it is not a resolution base.

**The lack, measured.** `validate-crossref-keys.py` iterates a fixed fifteen-name field list against
the **top level** of each document. A reference nested below that is invisible; a field not on the
list is invisible even at the top. It sees 742 reference sites and cannot see 230 — it reports on
**76%**. The guide citations sat in `knowledge_progression` and `next_steps`, on neither list, so
exit 0 was never evidence about them. 136 of the invisible sites are `related_symbols` — precisely
where the two fabricated constant names lived. **F-340** and **F-373** carry the remainder.

**What, part two (`491d033b`).** All **23** shipped citations into `p2-documentation.txt` — the PDF-era
capture now known to be lossy — were re-anchored to `silicon-doc-text.txt`. Each was resolved **by
reading what the old locator pointed at and finding that content in the new artifact**, never by
translating line numbers, which do not correspond. The shipped KB no longer references
`p2-documentation.txt` at all. **One did not resolve, and that is the find**: F-372 + G-027.

**And the rule was not fully kept — §0.5 item 5.** F-377 found locators that *were* translated. A
range check over all 113 `silicon-doc-text.txt` citations returns 0 out of range, because a
translated locator lands inside the file. Only opening the line catches it.

---

## 1.10 Duplicate keys, and the gate that now exists

**What.** A duplicate YAML key does not error: `yaml.safe_load` keeps the **last** and discards the
first, silently. On 2026-08-25 that destroyed the central corrective sentence of this entire sprint —
`pin-drive-configuration.yaml` had `note:` twice inside `idioms:`, the second won, and every consumer
read the bench-gap paragraph where the corrective statement should be. `43061dad` restored it.

**The sweep found four more sites, all pre-existing**, and `d756b44c`+`e9dc9507` adjudicated every one:

* **`architecture/lookup_ram.yaml`** — an orphaned block (the body of a removed pseudo-instruction
  whose header had become a comment) was being absorbed into the **SETLUTS** entry above it and
  overwriting SETLUTS's `operation` and `usage_example`. **Anyone reading SETLUTS was reading streamer
  setup.**
* **`language/pasm2/drvl.yaml`** — the discarded `timing:` block was a strict subset of the kept one,
  and byte-identical to the live one in its twin `drvh.yaml`. So **DRVL and DRVH were disagreeing
  about pin timing in what consumers read**, and the three-clock DIRx/OUTx delay was uncited in both.
  Now cited in both, from the Silicon Doc and the Hardware Manual. *(The first source found for it was
  Titus material — an upstream lead, never citable. The Parallax primaries say the same thing.)*
* **`hardware/edge-breadboard-carrier.yaml`** — a structured `educational_value` mapping shadowed by
  the scalar `"excellent"`.
* Fixed with them: `edge-breadboard-carrier` has a power figure again (**5 VDC, 5.5 V absolute
  maximum**, cited) where a wrong 6–9 V had been removed with its whole block and nothing put back;
  `addon-serial-host` has an identity string again, with **500 mA continuous per socket** rather than
  the summed "up to 1A" nobody sourced; and the symbol file's claimed `1224` records over 136 actual
  ones is corrected — 1224 is the source document's whole universe, 1024 of the clock category being
  `XMUL1..XMUL1024` — with the provenance recorded so nobody restores it.

**The lack, and it is closed.** `verify-yaml-format.py` stays at exit 0 on a planted duplicate,
because duplicate keys are **legal YAML**. It asks whether a document parses, which they do; nobody
asked whether it says what it appears to say. `02ff61b7` armed
`validation/audit-yaml-duplicate-keys.py`, which walks the **composed node tree** rather than the
loaded object — by the time you have a dict the evidence is gone — and reports which line wins and
which is discarded. Its negative control fires on a duplicate at the root, nested in a mapping, and
inside a list item, and stays clean on good input and on the same key legitimately reused at a
different depth. It exits **2** on "nothing measured" rather than reporting an empty scan as a pass.
**Current state: 1132 files, 0 duplicates.**

---

## 1.11 New coverage written this release — four files

| File | Why it exists |
|---|---|
| `architecture/pin-drive-configuration.yaml` | The replacement for the fabricated drive ladder: the 13-bit field's sub-fields, eight real rungs, and the DIR/OUT rule, expressed by encoding and cited. §1.5. |
| `architecture/streamer/pin-capture.yaml` | Stephen asked whether four smart pins running SPI can be traced through their nearest neighbours at Nyquist rates. **They can, and the neighbour routing is required, not a convenience**: on a pin running a smart-pin mode, `IN` is the smart pin's **event flag**, not the pin's logic level, so pointing the capture path at the bus records ready pulses instead of traffic. The KB held the harmless half of that fact and not the operative half. The page refuses to state a sample-rate ceiling no source gives. |
| `hardware/addon-click-adapter.yaml` | `#64008` had no hardware record. Written from the schematic — the first source in this corpus where **no text-extraction path can work at all**: the sheet is vector art with its text converted to curves, proven by a negative control returning 0 occurrences of every net, signal and refdes token. Read from the page rendered at 200 and 600 dpi, with all four renders committed so the netlist is checkable without re-rendering. |
| `hardware/p2-package-mechanical.yaml` | `deliverables/ai/P2/` had **no package or mechanical record of any kind**. Full CASE 932BR dimension table (15 rows), recommended mounting footprint, pin-corner numbering, 12 aliases. Read from the transcription verified in «#312», **not** re-OCR'd — tesseract misreads digits on these sheets and these are precision values. Closes **G-021**. It also says what the drawing does **not** give: no thermal resistance, derating curve or thermal-via guidance exists anywhere in the corpus, so the record says so rather than letting a reader infer a thermal solution from pad size (**G-020 stays open**). |

**A self-audit followed the Click record** (`601e65ce`): three places where inference had been written
as reading are now labelled with what actually establishes them — "the 4 spare I/Os are free for other
use" (the sheet draws no pass-through), `base_pin_options [0,16,32,48]` (the sheet is base-relative
throughout), and the `signal_map` direction column (the sheet's arrows are net-label pointers and
carry no direction information).

---

## 1.12 Ingestion findings applied to the shipped YAML

The ingestion sprint routed its findings to the register by design — `ingest-source` forbids YAML
edits — so nothing it found had reached the KB until this release.

* **F-363** — `$1F6`/`$1F7` now read *"CALLD-imm return, CALLPA parameter"* / *"…CALLPB…"*. The two
  rows had been byte-identical where all three authorities draw a CALLPA/CALLPB distinction, and
  "parameter" named **neither** role.
* **F-364** — 13 dangling `yaml_file:` pointers removed from the register index (it advertised 16
  register files and 13 of the pointers did not exist); content kept inline.
* **F-368** — `getbrk.yaml`'s WZ sentence had lost the Z value for the queued branch, and the file
  declared `Z: No effect` three lines after stating that GETBRK **requires** a flag effect.
* **F-369** — the smart-pin DIR-reset mechanism, in the Silicon Doc and carried nowhere in the KB:
  each smart pin holds 126 bits of state separate from its WRPIN configuration.
* **F-370** — `taqoz-forth.yaml` called ROM TAQOZ "the finite, fixed version"; its author says it is
  also an **early** version. Sourced to the author's own reviewer comment.
* **`599d3660`** — the WX module's two form factors: `#32420S` (SIP) → the P2 WX Adapter `#64007`,
  which carries the 2×6 accessory-header footprint; `#32420D` (DIP) → the Propeller Activity Board
  socket, a **P1** board. Both records now say plainly that `#64007` is the only P2 WX adapter.

🔴 **Citation drift caught while applying, twice.** F-363 cited `silicon-doc-text.txt:313-314` — the
numbering from *before* the artifact was re-emitted; live location is `:452-453`. And F-369's own
register entry cited `:3360`, which today reads `(X,Y) ROTATION`, while the shipped YAML always cited
`:3856` correctly. Both found by **reading the cited lines rather than trusting them**, and corrected
in the register. Nothing downstream inherited either.

---

## 1.13 Files that disagreed with themselves — the class no instrument can see

**What.** Three separate repairs this release, all the same shape: one field in a file contradicting
another field in the same file, with every gate green throughout.

* **`language/pasm2/{addsx,subsx}.yaml` (`b466a538`, F-379).** Both carried the PASM2 Manual's prose
  verbatim — *"the C flag is set (1) if the result is negative (Result[31] = 1)"* — while
  `flags_affected` and the encoding row in the **same file** gave the true-sign form. `Result[31]` and
  the true sign differ **only on overflow**, which is exactly the condition `TJV` exists to detect,
  and the manual's own TJV description requires C to hold the correct sign. Refuted three times inside
  the manual itself (Tables 9 and 169; the TJV description; the summary tables). **Root cause:**
  commit `87511c99` (v1.11.1) repaired this class across `adds · cmps · cmpsx · subs` and three `SUM`
  files and **skipped these two** — a class sweep that misses two members leaves a defect that now
  looks deliberate, because every neighbour is correct. Two more in the same family, both CSV
  column-split artifacts in fields no gate reads: `sumz.yaml encoding[0].z` held the **C column's**
  condition text where the manual gives `Result = 0`; `sumc.yaml encoding[0].c` had the same prose
  welded in front of a correct semantic.
* **`architecture/interrupts.yaml` (`4caeb6cc`).** The top-level `description` at `:26` said *"Each
  interrupt level has its own set of shadow registers"* — forty lines above the file's own sourced
  statement at `:38-46` that **there are no shadow register banks**. §1.6 corrected the detailed block
  and left the summary contradicting it. The `description` is the first thing a retrieving agent
  reads.
* **`language/spin2/methods/pinfloat.yaml` (`4cecb02c`).** Right where it was explicit and wrong one
  line above: *"External pull-up/pull-down resistors will determine the level"* is the anti-mislabel
  statement, while the line before it omitted "external" and so read as a chip feature — in the P2
  method file a reader looking for a pull-up actually lands on.

**The lack, stated exactly.** Every instrument here passed all of these throughout: the files parse,
their keys resolve, their citations are present, and `pnut-ts` assembles the instructions regardless.
**A compiler proves legality, never a flag's meaning.** The encoding check that verified all 45
encodings in §1.6 cannot read sentences. Only reading a `description` against the same file's
`flags_affected` catches a file disagreeing with itself, and no gate does that.

---

## 1.14 The one gutted file — found by the differential read, restored source-first

**What.** `guides/pasm2-getting-started.yaml` lost its `file_structure.clock_setup` block: the file
explained what happens when you declare a non-RCFAST clock mode and **never said how to declare one**,
while citing the very source table that would. That is the differential read's `gutted` test — content
the KB **needs** *and* that a source we hold **can support**, both halves required. It was the only
one of 85 files to meet it.

**Restored (`ca07aaf7`), and not verbatim.** All nine legal CON declaration combinations are back with
their `%CC_SS` values, the `_errfreq` default of `1_000_000` and the 15/30 pF crystal-loading rule,
each carrying the v55 line it came from. The deleted text had called `_clkfreq` **"Required"**; v55's
own table row — *no symbol and not DEBUG mode selects RCFAST* — says nothing is required. That claim
was a **two-file class**: `spin2-getting-started.yaml` kept its block *and* the claim, in the key name,
the description and the example. Both corrected; a widened grep finds no others.

**The clock-ceiling block was replaced, not restored.** Its three figures were uncited, its "default"
contradicted the same file's own `clock_setup`, and *"340+ MHz"* traces only to a TAQOZ overclocking
anecdote — community material, an upstream lead, never citable — against a datasheet maximum of 320.
It now carries the datasheet's AC Characteristics min/typ/max, labelled as **absolute limits** rather
than recommended-use range, which is what **E-007** requires.

**One deliberate divergence from our own extraction**, recorded so nobody "reconciles" it back: the KB
ships `%01_11` where `spin2-v55-text.txt` reads `01_1 1`. The DOCX confirms that cell is split across
two Word runs, is the only one of the nine so split, and the spaced form appears **nowhere** in the
source. Our extractor inserted the space. A future pass that aligns the KB to the extraction would
introduce a bit pattern that does not exist.

---

## 1.15 Two register corrections REJECTED — and that is the valuable half

**What.** `9370c580` and `e92aa02f` refused corrections that would have introduced defects into
content that is currently correct.

* **The PLOT `TEXTSTYLE` vertical-align "swap" is not a swap.** The Pascal-derived directive matrix
  carries a warning that anchor-edge and ink-side vocabularies describe the same pixels, and that this
  exact ambiguity caused the row to be documented backwards once already. The v55 text mixes both
  vocabularies in one sentence; `plot.yaml` uses ink-side consistently and says so. What was actually
  missing is the **disambiguation the authority itself carries** — which is why this got filed as a
  defect twice.
* **The weight correction wanted "thin" changed to "light" for value 100.** The Pascal source declares
  `weight[0..3] = (100,400,700,900)`, and 100 is OpenType **Thin**. Light is 300.
* **Deleting F-251's pull-up sentence would have left a hole exactly where the reader is standing in
  front of a floating pin**, so it was raised instead of cut: no bias resistors, a choice of how hard
  to drive, and a weak drive is still a drive.

**And a measurement this sprint's own scope rested on was falsified rather than quietly widened.**
Plan §3 excluded manual prose because a sweep found the masters clean. Searching the IOSP master
**recursively** — it is split per chapter under `part-*` directories, which is how a flat glob misses
it — finds 23 mislabel lines, 5 internal-pull-up assertions, and four sites teaching the
`P_HIGH_15K | P_LOW_FLOAT` composition that has **no Parallax source at all**. Filed as **F-356**,
still `CONFIRMED`, because scope is Stephen's and the honest move is to falsify the measurement.

**An attribution error was corrected in five files.** `EF-063` and `EF-064` had been cited as the
empirical basis for "the P2 has no pull-ups". They are not pull-up findings: EF-063 certifies jumper
continuity, EF-064 establishes streamer pin placement. The weak drive is their **rig apparatus**, not
their subject, and the ledger holds no dedicated drive-strength finding. `e92aa02f` fixed
`pin-drive-configuration.yaml`; `75971308` swept the other four. Three of the ten citations were left
alone because they describe what the rigs actually did.

---

## 1.16 Schema reshaping — measured, and forced by the instrument

**What.** **34 top-level keys across 24 files changed YAML type** (23 `list→dict`, 11 `str→dict`),
re-derived here at HEAD. The typical case: a `signal_map` that was a list of rows becomes a mapping
whose sibling key is the citation for the rows.

**It is not a judgement call, and that was established by experiment.** With the citations moved to
the uniform-shape alternative — a sibling `signal_map_source:` key — `audit-yaml-claim-sourcing.py`
returns **exit 1 with 22 Tier 1 violations**, including all 19 of the blocks the in-block form
silences. The uniform alternative does not satisfy the armed gate. And for every block still carrying
the **old** shape (`signal_map` list ×10, app-note `gotchas` list ×4, hardware `description` str ×14),
the question *"would the gate demand a reshape here?"* was evaluated with the auditor's own helpers:
**0 of 28**. Not one is a block that got away. The rule is exact: **reshaped ⟺ the block stated an
uncited quantity inside a file that demonstrably cites.**

**All five consumers were executed against the new shapes and each was made to fail** on a shape it
cannot handle — `generate-p2kb-index.py`, `fetch-kb-file.sh`, `validate-crossref-keys.py`,
`audit-yaml-claim-sourcing.py`, and the p2kb-mcp fetch contract. Nothing breaks. **Verdict:
MEASURED-SAFE.**

**One of the 34 is not a reshape at all.** `hardware/edge-breadboard-carrier.yaml educational_value`
was a **duplicate top-level key** at `v1.17.0` — a mapping shadowed by the scalar `"excellent"`, which
YAML's last-wins rule made parse as `str`. HEAD removed the shadowing scalar, so the mapping that was
always in the file now parses. The type changed; nobody reshaped anything.

**What it does not settle.** Nothing enforces the rule and nothing records it in the tree. The next
block that acquires a quantity will drift the shape further, and the only thing that would catch it is
the citation gate firing — which fixes citation, not uniformity. Not blocking; no consumer is affected
today.

---

## 1.17 Instruments armed as blocking release gates

**What.** Three gates went from advisory to blocking in this range, and one was built from nothing.

| Gate | Armed by | Proven able to fail |
|---|---|---|
| `audit-yaml-claim-sourcing.py` | `43b0ede2` | A planted uncited quantitative block turns the release path red and names the file, line, block and units; removing it returns green with the file byte-identical. |
| `audit-constant-fidelity.py` | `43b0ede2` | A fabricated constant fires it; so does an instrument that cannot reach its inputs — **exit 2 on "nothing audited", with a message saying why, because nothing audited is never a pass.** |
| `audit-yaml-duplicate-keys.py` | `02ff61b7` | 5 negative-control cases; fires at the root, nested in a mapping, and inside a list item; clean on good input and on legitimate reuse at a different depth. §1.10. |
| `audit-register-hygiene.py` | `d62544ea` | The planted-duplicate `G-019` fixture passes **CLEAN at exit 0** through the pre-fix tool and **fails at exit 1** through the fixed one. |

**No baseline, no tolerance, no ratchet** — the purge removed the population first precisely so there
is nothing to grandfather.

**Arming meant fixing the harvest first, because a gate is only as true as what it reads.** The
fidelity truth side now globs `.txt` as well as `.md` and parses pipe rows by cell, so the current
Spin2 v55 symbol table — tab-indented, value in column one — is finally on it: **116 constants where
there were none**, with edition precedence so a superseded extract cannot outrank the current one.
`TRUTH_ROOTS` was deliberately **not** widened; widening it is what let a derived fact sheet shadow a
real source during planning (**F-341**).

**And `d62544ea` fixed a gate that was reporting CLEAN while reading nothing.** `audit-register-hygiene`
printed `0 entries` against a register full of table rows. Three changes: the table-row dialect is a
recognised entry form; the status vocabulary is **per-register**, selected off the counter label the
file declares (so `OPEN` stays excluded for the corrections register, where it is ordinary prose, pinned
by a control case); and the status is read from the row's own Status **cell** rather than anywhere in
the row, because the ledgers use lowercase lifecycle words that appear in prose too. A fifth register
nobody had looked at had the same defect. The ID family is a prefix **string** now, so the P1
namespaced allocators are governed rather than renamed. **All five registers now exit 0 with the gate
actually reading them.**

## 1.18 The 2026-08-29 pre-release fix pass — 6 files, 3 commits, all source-first

Every change below was made against a source read **at the line**, and the source is quoted in the
file. Nothing was inferred, and no value was changed to make a gate pass.

**`856ef2f2` — the SETXFRQ increment rule (F-380).** The *Parallax Propeller 2 Documentation* v35
states one rule for the streamer NCO word (`part2-pixel-ops.txt:117`, continuing at `:121` — one
sentence split by a page break): *"For fractions with remainders, the computed D/# value should be
incremented, in order to produce proper initial rollover behavior."* Its own table applies it —
`1/3` is `$2AAA_AAAA+1`, `1/5` is `$1999_9999+1`, while `1/2`, `1/4`, `1/8` carry nothing. So the
rule is **truncate, then increment on a remainder**; it is **not** round-to-nearest, which agrees
with the source only when the remainder happens to exceed half.

| file | wrong / total | what it also got wrong |
|---|---|---|
| `language/pasm2/setxfrq.yaml` | 2 of 4 | stated the rule **twice, differently** — `source:` quoted the footnote, `computation:` said `round()`; and cited `nco-timing.yaml` as a cross-check that "the two agree" while that file carried the same wrong value |
| `architecture/streamer/nco-timing.yaml` | **7 of 12** | its own ratio table is correct at **all 8** entries — the file applied the rule in one block and not the next |
| *(not KB)* Streamer Guide v1.1.0 master | **8 of 18** | taught `round()` in three places, incl. a worked example printing the wrong result |

*The lack:* nothing in this project can detect an off-by-one in bit 0 of a 31-bit phase word. The
values are well-formed hex of the right magnitude, they carry citations, and they compile. Only
recomputing from the quoted rule finds it. **⚠️ A Streamer Guide re-release is owed.**

**`9723e482` — `architecture/io_pin_timing.yaml`, the eighth fabricated-provenance file (F-377 pt2).**
Header cited `part3-pins.txt, pages 5-8`; no such file exists under `sources/silicon-doc/` and none
ever did. F-359 named seven such files. **The content proved genuine** — all four timing claims are
really in the Silicon Doc — so it was re-anchored, not removed: `:1987` (DIRx/OUTx three-clock
latency), `:1997` (INx read), `:2005` (TESTP read), `:3847` (smart-pin IN-flag reset), `:101`
(latch-up onset, now labelled as ON Semi wafer-lot failure analysis quoted in the revision history
rather than a characterised limit). Reading it found two more: **`"Smart pins add ~1-2ns to base
timing"` has no source** — zero nanosecond figures for this exist in any ingested Parallax source,
removed under cite-or-omit (F-327/F-333 class) — and `total_latency: 5 clocks` is a sum of a 2-clock
`DRVH` and the source's THREE, which the source never states as a total. The abs-max table was
re-read against `p2-datasheet-text.txt:2126-2149` and matches verbatim; the four package-and-supply
limits stated beside it are now named as deliberately out of scope, so their absence reads as a
choice rather than a gap.

*The lack:* a fabricated citation satisfies the sourcing gate exactly as well as a real one. The
gate checks that a citation is present; it never opens the file named.

**`efc683a8` — whose limit is it, the compiler's or the silicon's (F-378, and F-381 as a by-product).**

| symbol | shipped range (= pnut-ts acceptance) | P2 Datasheet rating | over by |
|---|---|---|---|
| `_CLKFREQ` | 3,333,333 Hz – **500,000,000 Hz** | PLL max **320 MHz** (`p2-datasheet-text.txt:2200`) | 180 MHz |
| `_XINFREQ` | 250 kHz – **500 MHz** | direct drive into XI max **200 MHz** (`:2198`) | 300 MHz |
| `_XTLFREQ` | 1 – **60 MHz** "typical" | crystal max **50 MHz** (`:2199`) | 10 MHz |

Plus `clkmode.yaml`'s PLL `use_case: "High-speed operation (up to 500 MHz)"` and a **500 MHz row**
in `timing_operations.yaml`'s rollover table — a speed no P2 clock source is rated to reach (now
320 MHz: 13.4 s rollover, 3.125 ns cycle, recomputed). All five now carry the compiler range
*labelled as the compiler range*, the datasheet rating beside it, and the *Parallax Propeller 2
Documentation*'s 350 MHz `VCO / 1` overclock ceiling (`part3-interrupts.txt:545`) — three distinct
numbers the reader was previously handed as one. This is **E-007's label-which-framing rule**, which
had been settled for the Hardware Manual's clock limits and never applied here.

Two further defects, found by reading the files while citing them: `timing_operations.yaml`
described the system counter as **32-bit** where the Silicon Doc says it was *"extended to 64 bits.
GETCT WC retrieves upper 32-bits"* (`silicon-doc-text.txt:55`) — the file now says the counter is
64-bit and that the rollover discussion concerns the 32-bit value `GETCT` returns alone; and its
`minimum_resolution` block carried a `min_practical` column (~1 us / ~100 ns / ~50 ns / ~30 ns) plus
*"Spin2 interpreter overhead adds several microseconds to any operation"*, **neither of which any
source states nor any bench result here measures**. Removed, with a note that the overhead is real
and wants a silicon measurement before the KB prints a figure for it.

*The lack:* nothing compares a `range:` against the silicon rating for the same quantity, and
nothing flags that a range's source is a **compiler guide**. Both numbers are true; the entry never
said which question it was answering.

**Per-file, this pass:**

| file | +/− | new to the change set? | verdict |
|---|---|---|---|
| `language/pasm2/setxfrq.yaml` | +18/−15 | no (already in the 89) | **stronger** — 2 wrong values, rule restated, self-corroborating cross-check removed |
| `architecture/streamer/nco-timing.yaml` | +28/−10 | no | **stronger** — 7 wrong values, `source:` added to `video_rates` |
| `architecture/io_pin_timing.yaml` | +29/−14 | no | **stronger** — provenance re-anchored, 1 unsourced claim removed |
| `language/spin2/constants/special-configuration-symbols.yaml` | +17/−3 | **yes** | **stronger** — 3 ranges labelled, 4 blocks cited |
| `language/spin2/concepts/timing_operations.yaml` | +31/−12 | **yes** | **stronger** — counter width corrected, unsourced estimates removed, 6 blocks cited |
| `language/spin2/system-variables/clkmode.yaml` | +3/−2 | **yes** | **stronger** — PLL ceiling corrected, 2 blocks cited |

**Registers moved:** `F-380` filed (SETXFRQ class) · `F-381` filed (Tier-2 structural) · `F-378`
rewritten in place and **RESOLVED** · next finding ID now `F-382`.


---

# PART 2 — By region → file

**All 89 files, each carrying its differential-read verdict.** Regions are ordered by file count as
measured at HEAD, so related corrections sit together.

**The verdicts** (`2026-08-26-yaml-differential-read.md` §0.1): **stronger** — what was removed was
replaced by better-sourced content. **equal** — reworded or restructured, same substance.
**thinner-but-honest** — removed because unsourced, wrong, or deliberately out of scope; its absence
is *correct*. **gutted** — removed content the KB **needs** *and* that a source we hold **can
support**; both halves required. **new file** — nothing could have been removed from it.

**Tally at HEAD: 78 stronger · 6 equal · 1 gutted-then-restored · 4 new file = 89.** Zero files are
`thinner-but-honest` at *file* level; that verdict lives at block level (§1.3). The four
`language/pasm2` files added after the differential read was written are verdicted here, from
`b466a538`'s diff.

`GONE` = top-level keys present at `v1.17.0` and absent at HEAD **plus** leaf-fact candidates whose
value string appears nowhere in the shipped KB, as measured by the differential read. It
over-reports — a reworded fact counts as gone — and is a *reading list*, not a loss figure.

---

## `hardware/` — 27 files · 25 stronger · 2 new

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `edge-32mb-module.yaml` | +223/−417 | 224 | stronger | Pin map, boot table, 8 µs CS limit, PSRAM banks all returned cited; P58-P61 anchored to the **boot-ROM listing** rather than the eval guide, which the errata register records as reversing the directions. Fabricated `alternate_part: 64000-ES` removed **with a note saying why**. E-010's "enable a pin pull-up" removed (`75971308`). |
| `edge-standard-module.yaml` | +172/−335 | 176 | stronger | `pin_mapping` returned cited with an explicit *"LEDs are P56/P57, NOT P38/P39"* warning; boot-mode table records that two rows are the same switch setting, disambiguated by card presence, stated as the source states it. E-010 removed. |
| `p2-hardware-feature-comparison.yaml` | +244/−121 | 104 | stronger | **`#64006G` re-identified as the Goertzel board**, not a Digital I/O board; invented carrier part numbers replaced with real ones; a carrier dimension off by a factor corrected. `75971308` then removed the `digital_io_board` slug from two guidance lists and found two more slugs naming no board. |
| `addon-motor-driver.yaml` | +116/−67 | 62 | stronger | All 16 pin offsets, the PWM interlock, 250 ns deadtime and 150 mV/A returned cited; a guide self-contradiction resolved and filed as errata — **our own extraction audit blamed docling and was wrong**: plain `pdftotext` carries the same duplication, so it is in the PDF and no re-extraction would fix it. |
| `hub75_adapter.yaml` | +100/−93 | 58 | stronger | Manufacturer's **70 MHz** replaces the unsourced 40/35 MHz; three explicit `gap_*` keys record what was removed and what would settle it. Its `source:` keys point at loose files at the ingestion root (F-341's shape) — defensible on authority, anomalous in location. |
| `p2-eval-board.yaml` | +95/−49 | 36 | stronger | Rev D→Rev C, 320→180 MHz recommended, real flash part, 3.55 in; ~10 `TBD` placeholders replaced with sourced values. F-328(b)'s fabrication class drained. |
| `addon-wx-wifi.yaml` | +61/−30 | 33 | stronger | `pin_descriptions` returned as a full table with SIP/DIP numbers; `part_variants` → cited `form_factors` with the `#32420S`/`#32420D` split (`599d3660`). |
| `addon-serial-host.yaml` | +61/−106 | 62 | stronger | Enables at offsets 1/5, D-/D+ pairs and the enable sequence returned cited; new Spin2 `code_patterns`. **Identity string restored** (`e9dc9507`) with 500 mA continuous per socket rather than the summed "up to 1A" nobody sourced. |
| `addon-hyperram-hyperflash.yaml` | +60/−23 | 10 | stronger | `configuration`/`specifications` returned cited; the RES shunt now stated as a **driver requirement**. |
| `addon-hd-audio.yaml` | +59/−49 | 22 | stronger | `dac_board` returned with the four `P_DAC_*` constants and the parallel-pin impedance rule. |
| `addon-rtc.yaml` | +58/−33 | 15 | stronger | **E-004 closed** — the guide's "150 kΩ pull-up" mislabel restated as a P2 drive-strength mechanism with DIR high, quoting the guide under a key that says not to copy it; PCF8523 map + `$68` added. Fixing it surfaced a second mismatch the finding never named: the guide also prescribes a 3.3 kΩ pull-up, and the P2 ladder has **no 3.3 k rung at all**. |
| `addon-control-board.yaml` | +55/−38 | 7 | stronger | Description/signal map returned cited; the `P_LOW_15K` read idiom **corrected** to require DIR high. Three inferences removed because the guide states 470 Ω and nothing else — no LED current, no forward drop, no debounce interval, so neither do we. |
| `programming-prop-plug.yaml` | +51/−28 | 12 | stronger | 3 Mbaud ceiling, DTR/RTS reset selection, ~20 µs pulse returned cited; new `header_pinout`. |
| `edge-mini-breakout.yaml` | +39/−48 | 30 | stronger | Fabricated "USB connector onboard" removed; cited `connectivity` gives the real P0-P31 + P56-P63. |
| `addon-mini-prototyping.yaml` | +32/−4 | 2 | stronger | Description, power rails and grid retained and cited. |
| `edge-standard-breakout.yaml` | +29/−45 | 27 | stronger | Same fabrication removed; cited `connectivity` adds the eight 2×6 headers. |
| `addon-serial-device.yaml` | +28/−63 | 26 | stronger | LEDs at 0/1/6/7 and D-/D+ at 2/3, 4/5 returned cited; new even/odd smart-pin pairing note. |
| `hardware-compatibility-matrix.yaml` | +27/−2 | 2 | stronger | False *"all add-ons use P0-P7"* replaced by the correct single/dual-header model (`ccddcbe6`). |
| `addon-goertzel-touch.yaml` | +25/−14 | 7 | stronger | `specifications` returned cited plus a board-revision note. |
| `addon-digital-video-out.yaml` | +21/−2 | 2 | stronger | Same facts, reworded with a citation; ACC-5V bridge retained. |
| `addon-wx-adapter.yaml` | +18/−0 | 0 | stronger | Insertions only — citation + `sole_p2_wx_adapter` disambiguation (`599d3660`). |
| `addon-led-matrix.yaml` | +14/−2 | 2 | stronger | Charlieplex rule and ~4 mA retained; description now cited. |
| `addon-microsd.yaml` | +7/−0 | 0 | stronger | Insertions only — `power_signals` gained a citation. |
| `edge-breadboard-carrier.yaml` | +66/−69 | 43 | stronger | Wrong "6-9 V" and a non-existent on-board USB-to-serial gone; **5 VDC / 5.5 V max restored cited** and the `educational_value` duplicate key resolved (`e9dc9507`). |
| `addon-av-breakout.yaml` | +70/−44 | 0 | stronger | `signal_map` restructured, guide citation + per-board capture added. |
| `addon-click-adapter.yaml` | **+195/−0** | — | *new file* | `#64008` from the schematic — the first source here where no text-extraction path works at all. §1.11. Three inference-as-reading claims self-audited and labelled (`601e65ce`). |
| `p2-package-mechanical.yaml` | **+102/−0** | — | *new file* | CASE 932BR, 15 rows, footprint, 12 aliases. **G-021 closes.** §1.11. |

## `architecture/` (top level) — 14 files · 13 stronger · 1 new

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `interrupts.yaml` | +219/−115 | 78 | stronger | 🔴 **The worst correction in the range**: IJMP3/IJMP1 were **inverted** — anyone generating interrupt code got the wrong vector addresses for levels 1 and 3. The `shadow_registers` model is disproven; there are no shadow banks, only `CALLD IRETx,IJMPx WCZ`. A summary paragraph still contradicting that was repaired by `4caeb6cc`. §1.6, §1.13. |
| `debug_interrupt.yaml` | +208/−92 | 64 | stronger | Three invented configuration registers and the fabricated `NIXINT0`/`TRGINT0` removed; real `BRK`/`COGBRK`/`GETBRK` encodings substituted. Two of the eight non-derivable claims live here (§0.5 item 1). |
| `smart_pins.yaml` | +173/−21 | 13 | stronger | `%AAAA`/`%BBBB`/`%FFF` selectors given full bit ranges and cited; the four global filter defaults now carry length, tap **and** the source's own arithmetic. Gained the **IN rule** with its consequence stated (`ad4f974f`) and F-369's 126-bit state mechanism (`36196329`). |
| `clock_system.yaml` | +185/−136 | 85 | stronger | Rebuilt from v55's own "Clock Setup" closed set with `%CC_SS` per row; PLL fields, `%CC`/`%SS` tables and the datasheet's worked 148.5 MHz sequence all cited. **`pll_lock: ~10 microseconds` was wrong — three Parallax sources say 10 ms.** Two `anti_patterns` locators point at the wrong row (§0.5 item 5). |
| `lookup_ram.yaml` | +152/−99 | 47 | stronger | Fabricated `RDLUTS` deleted; **LUT sharing direction corrected** and `WRLUT`'s operand order fixed. The orphaned block that had been overwriting **SETLUTS** removed (`e9dc9507`). Three of the eight non-derivable claims live here. |
| `cog_attention.yaml` | +124/−49 | 36 | stronger | Fabricated `RDCOGID` deleted; **ATN corrected from event 15 to event 14**; encodings replaced with the real ones; `setup_for_event` no longer configures SETSE1 for attention, which SETSEn cannot select at all. |
| `event_system.yaml` | +109/−55 | 52 | stronger | The whole 16-event catalogue restored verbatim and cited; the `SETSE` restriction (pin/LUT/lock only) added. |
| `click_module_integration.yaml` | +70/−33 | 20 | stronger | `documentation_source` went `code_analysis` → `schematic_primary`; **all twelve CLICK_OFST values confirmed against the #64008 sheet with zero corrections** — they had been derived from the P2-Click-eInk driver and every one was exactly right. Gained `uart_direction_caveat` and `header_span`. Its removed `best_practices` is authored-here with no upstream — **F-352, open**. |
| `locks.yaml` | +89/−53 | 26 | stronger | The invented `LOCKTRY` "query" form — which actually **acquires** — removed; real encodings substituted. One non-derivable claim (`state_bits: 4`) stands here. |
| `pin-power-domains.yaml` | +35/−19 | 8 | stronger | The two-layer distinction rebuilt with sources — silicon 16 groups of 4, Edge board 8 LDOs of 8 — plus *why* a ratiometric measurement must stay within four. |
| `io_pin_timing.yaml` | +18/−256 | 146 | stronger | The F-327 fabrication family — a milliamp drive ladder, programmable slew, and a propagation/rise/fall model built on both — removed; cited absolute-maximum ratings, the protection-diode mechanism and the 5 V series-resistor technique added. **Still carries the `part3-pins.txt` fabricated header (F-377, §0.5 item 6)** and a residual `~1-2ns` from the same nanosecond family. |
| `serial_loader.yaml` | +14/−15 | 10 | stronger | All boot facts returned quoted from source, plus P62's open-drain behaviour under a non-zero INA/INB mask. |
| `smart_pin_patterns.yaml` | +5/−7 | 7 | stronger | Generic unsourced notes replaced by verbatim cited statements; the timing cross-reference kept **and** promoted into `related:`. |
| `pin-drive-configuration.yaml` | **+277/−0** | — | *new file* | Eight real rungs, cited, expressed by encoding. §1.5. Its duplicate `note:` — which silently discarded the sprint's own central corrective sentence — was found and fixed by `43061dad`. |

## `language/spin2/` — 15 files · 14 stronger · 1 equal

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `concepts/timing_operations.yaml` | +31/−12 | 2 | stronger | **§1.18.** System counter corrected from 32-bit to **64-bit** (`silicon-doc-text.txt:55`, "GETCT WC retrieves upper 32-bits"), with the rollover discussion scoped to the 32-bit value GETCT returns alone. The 500 MHz rollover row → 320 MHz, recomputed. The 2 GONE are the unsourced `min_practical` column and "Spin2 interpreter overhead adds several microseconds" — **no source states either**. Six blocks gained `derived_from:`/`source:`; those blocks were always uncited and were invisible until the file gained its first citation (F-381). |
| `constants/special-configuration-symbols.yaml` | +17/−3 | 0 | stronger | **§1.18.** `_CLKFREQ`, `_XINFREQ` and `_XTLFREQ` ranges labelled as **pnut-ts acceptance ranges**, each with the P2 Datasheet's rating beside it (320 / 200 / 50 MHz) — the compiler accepts 180, 300 and 10 MHz beyond them respectively. Four further blocks cited to the compiler guide's own rules 1-5 and to `spin2-v55-text.txt:1018`/`:1027`. |
| `system-variables/clkmode.yaml` | +3/−2 | 0 | stronger | **§1.18.** PLL `use_case` no longer says "up to 500 MHz"; states the datasheet's 320 MHz max and 180 MHz typical plus the 350 MHz `VCO / 1` overclock ceiling. `bit_fields` and the PLL-lock `~10 ms` note cited (`silicon-doc-text.txt:2621`, `:2687`, `:2635`). |
| `symbols/spin2-builtin-symbols-complete.yaml` | +1052/−23 | 20 | stronger | 874 → 1937 leaves carrying v55's own wording; **all 116 v55 constants defined exactly once**, plus a top-level `aliases:` block of 116 names that makes them reachable at all. The 20 GONE are 3 corrected counts, 13 rewordings and **4 fabricated symbol names** — zero real losses. The `1224` record count corrected to 136 with its provenance (`e9dc9507`). |
| `concepts/basic-io.yaml` | +89/−121 | 59 | stronger | Source-first rebuild; three disproven blocks deleted incl. `max_current_per_pin: 150mA` — **five times the datasheet's ±30 mA absolute maximum**, in the exact number used to size an LED resistor. |
| `methods/getct.yaml` | +45/−25 | 4 | stronger | Derived figures replaced by cited v55 + datasheet statements. Its `description` was purged and not returned for a while; **restored by `75971308`**, quoted rather than derived. |
| `debug-commands/pc_key.yaml` | +32/−11 | 5 | stronger | Every removed rule restated from v55; one new rule added (hub `@key` vs cog `#key`). |
| `methods/wrpin.yaml` | +22/−20 | 26 | stronger | All 26 are **de-duplication**; every one of the 13 mode constants and all four `P_TT_*` verified present exactly once in the definition home. |
| `debug-displays/logic.yaml` | +22/−0 | 0 | stronger | Pure addition — the capture-vs-display split, a `pin-capture.yaml` cross-reference and a cited worked example. |
| `methods/waitus.yaml` | +21/−16 | 15 | stronger | The wrong 1–4,294,967 ms ceiling replaced by v55's `$8000_0000`-clock bound plus a `ceiling_formula`. Removals are quality commentary — `thinner-but-honest` at block level under the KB entry rule. |
| `methods/waitms.yaml` | +17/−11 | 10 | stronger | Same correction. Its `notes:`/`limitations:` went list→dict where every sibling keeps them as lists (§1.16). |
| `conventions/johnny-mac-documentation-style.yaml` | +13/−10 | 1 | stronger | Inline example corrected: `P_HIGH_150K "150K pullup resistor"` → `P_HIGH_15K` + `drvh`. Compiles. |
| `conventions/spin2-docs-jonnymac.yaml` | +13/−10 | 1 | stronger | Same correction, uppercase variant. |
| `methods/pinfloat.yaml` | +3/−1 | 1 | stronger | "external" added one line above where it was already right, plus a note that a `P_HIGH_*` selection goes inactive when the pin floats. §1.13. |
| `methods/cogstop.yaml` | +1/−1 | 1 | equal | One word: "pull-up/down resistors" → "**external** pull-up/down resistors". |

## `language/pasm2/` — 12 files · 12 stronger

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `concepts/basic-io.yaml` | +96/−121 | 62 | stronger | Byte-twin of the Spin2 file; same disproven blocks removed, and the `Set DIR before OUT` glitch rule was **backwards** and is now corrected. |
| `setxfrq.yaml` | +22/−12 | 3 | stronger | All four SETXFRQ words retained; the block now carries the source rule and per-value arithmetic. ⚠️ **Two of the four values contradict the rounding rule the block itself cites** — §0.5 item 13. |
| `wrpin.yaml` | +22/−6 | 6 | stronger | Six drifted one-line restatements de-duplicated to `architecture/smart_pins.yaml`, verified to carry all six with bit ranges. |
| `getbrk.yaml` | +16/−4 | 3 | stronger | `flags_affected: C/Z: No effect` was **wrong** for an instruction that requires a flag effect; replaced with cited per-flag behaviour and the WZ polarity corrected (**F-368**). |
| `subsx.yaml` | +8/−2 | 0 | stronger | The manual's `Result[31]` prose replaced with the true-sign form its own Table 169 gives, naming E-016. §1.13. |
| `drvh.yaml` | +7/−0 | 0 | stronger | Citation added for the existing 3-clock pin latency. |
| `drvl.yaml` | +7/−3 | 0 | stronger | Same citation, **plus a duplicate `timing:` key removed** — DRVL and DRVH had been disagreeing about pin timing in what consumers read. §1.10. |
| `concepts/streamer_smartpin_control.yaml` | +6/−8 | 1 | stronger | The removed block returned structured and cited; a derived figure replaced by the source's own wording. |
| `addsx.yaml` | +1/−1 | 0 | stronger | The same `Result[31]` sentence replaced, naming Table 9 and the TJV requirement. §1.13. |
| `getxacc.yaml` | +1/−1 | 1 | stronger | A dead locator re-anchored to a live, verified one (**F-365**). |
| `sumc.yaml` | +1/−1 | 0 | stronger | `encoding[0].c` had the C column's condition prose welded in front of a correct semantic — a CSV column-split artifact in a field no gate reads. |
| `sumz.yaml` | +1/−1 | 0 | stronger | `encoding[0].z` held the **C column's** condition text where the manual gives `Result = 0`. Wrong, not merely malformed. |

## `architecture/streamer/` — 8 files · 4 stronger · 3 equal · 1 new

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `pin-capture.yaml` | **+312/−0** | — | *new file* | Why a smart-pin bus must be watched from next door. §1.11. |
| `pin-selection.yaml` | +188/−57 | 34 | stronger | **F-361**: the dense sub-pin slot table no source states and the bench contradicts is gone, replaced by the real rule (`pin << 17`, `D[19:17] = pin & 7`); the `pin_base_encoding` example was the EF-065 misalignment trap written out for a reader to copy. |
| `modes-reference.yaml` | +43/−8 | 4 | stronger | `field_notation_caveat` expanded with a second bench proof and a source. |
| `_index.yaml` | +25/−0 | 0 | stronger | Gained the whole `pin_capture` routing entry plus aliases. |
| `dds-goertzel.yaml` | +22/−10 | 10 | stronger | Citations re-anchored from the partial `p2-documentation.txt` extract to `silicon-doc-text.txt`; aliases added. ⚠️ **Two locators only half re-anchored** — `:4062` is a blank line (**F-377**, §0.5 item 5). |
| `overview.yaml` | +21/−4 | 0 | equal | Apparatus only — aliases, `related:`, full-path `see_also`. |
| `nco-timing.yaml` | +11/−2 | 2 | equal | Apparatus only. Its `video_rates:92` carries the same `$0CE3_BCD3` as `setxfrq` (§0.5 item 13). |
| `dac-routing.yaml` | +10/−2 | 2 | equal | Apparatus only — aliases added, `see_also` bare names → full paths. No content change. |

## `architecture/smart-pins/` — 4 files · 4 stronger

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `smart-pin-11011-usb-host-device.yaml` | +28/−12 | 2 | stronger | USB 12 Mbps / 1.5 Mbps returned with the `D_14` field, the DP/DM roles and the FPGA resistor note. Carries **F-372 / G-027** — the sentence one edition of v35 states and the other omits, now presented as a conflict rather than as fact. |
| `smart-pin-00000-normal-mode.yaml` | +18/−11 | 2 | stronger | Both worked examples **corrected**: they taught the disproven `WRPIN P_HIGH_15K` + `DIRL` pull-up idiom. |
| `smart-pin-00011-dac-16bit-pwm-dither.yaml` | +17/−15 | 6 | stronger | Dither facts returned verbatim from `part4-smart-pins.txt:284-308`, plus the `M[12:10]=%101` requirement. |
| `smart-pin-11000-adc-internal-clock.yaml` | +9/−4 | 4 | stronger | `P_ADC_GIO`/`P_ADC_VIO` **redefined correctly** — they are calibration *sources*, not input ranges. The old text was a legal name with a wrong definition, which is the shape no constant gate can catch. |

## `architecture/boot-rom/` — 4 files · 4 stronger

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `_index.yaml` | +18/−15 | 12 | stronger | Boot timing and all three path summaries returned cited, with pin directions named **from the flash chip's side**. |
| `taqoz-forth.yaml` | +17/−0 | 0 | stronger | Gained `useful_for`, sourced to the author's own reviewer comment (**F-370**): ROM TAQOZ is an *early* build, not merely a cut-down one. |
| `boot-pattern-selection.yaml` | +15/−17 | 7 | stronger | **Corrected**: the claim that the ROM issues no `HUBSET` is contradicted by its own listing — the `Prop_Clk` and shutdown paths both do, now cited to `ROM_Booter.lst`. |
| `spi-flash-boot.yaml` | +5/−2 | 2 | stronger | Patterns returned verbatim; DI/DO direction disambiguated. |

## `application-notes/` — 4 files · 4 stronger

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `p2an003-dac-analog-signal-generation.yaml` | +17/−13 | 9 | stronger | `key_parameters` returns with verbatim dither text plus a new sourced `M[12:10]=%101` requirement. Deleted `200 MHz / 256 = 781_250 sps` as a derivation — see the inconsistency at §0.5 item 15. |
| `p2an001-single-pin-instrumentation-adc.yaml` | +15/−15 | 7 | stronger | Two removals were **corrections**: the designer's 15 mV became the hardware-verified ≤9 mV with an explicit *"do not quote 15 mV"*, and *"P2 spec max is 300 MHz"* was simply wrong (datasheet PLL max 320 MHz). Keeps an uncited derived `raw_sample_rate_sps` and one off-by-one locator (§0.5 items 15-16). |
| `p2an002-cordic-for-real-work.yaml` | +14/−12 | 7 | stronger | Six gotchas return with Silicon Doc quotes + EF-053; two dropped claims are **refuted**, not lost. Two locators of the F-377 shape. |
| `p2an004-frequency-rotation-rc-timing-measurement.yaml` | +14/−14 | 9 | stronger | Gotchas re-anchored to the datasheet Pin Mode Legend and the `%AAAA`/`%BBBB` table; the EF-063/EF-064 mis-attribution removed (`75971308`). ⚠️ Carries a self-contradiction about sensor figures (§0.5 item 14). |

## `guides/` — 2 files · 1 gutted-then-restored · 1 equal

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `pasm2-getting-started.yaml` | +135/−70 | 24 | ✅ **gutted → RESTORED** | The CON clock-setup declarations went missing while the file kept explaining what happens once you declare one. Net a large improvement everywhere else, which is exactly why a gate would have passed it. Restored source-first by `ca07aaf7`, with the "Required" claim dropped and the clock-ceiling block **replaced** rather than restored. §1.14. |
| `spin2-getting-started.yaml` | +31/−13 | 7 | equal | Relative→absolute path re-anchors, all targets verified present, plus dropping "pull resistors" from a routing blurb — honest, since `basic-io.yaml` now states the P2 has no internal pull network. Carried the same "Required" claim and was corrected with its sibling. |

## `architecture/system-registers/` — 1 file · 1 stronger

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `complete-system-registers-index.yaml` | +36/−17 | 15 | stronger | 13 dangling `yaml_file:` pointers removed (**F-364**), content kept inline; `$1F6`/`$1F7` descriptions **corrected** — PA/PB hold the CALLD-imm *return* address and the CALLPA/CALLPB parameter, which "CALLD-imm parameter" named neither (**F-363**). |

## `code-examples/` — 1 file · 1 equal

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `smart-pins-002-button-reading.yaml` | +1/−1 | 1 | equal | One word: "Pull-up or pull-down resistor" → "**External** …", so it cannot be read as an internal P2 pull. |

---

# Appendix A — Commit legend

The **24 commits that touched `deliverables/ai/P2/**/*.yaml`**, oldest first. (107 commits landed in
the range across all paths; the rest touched tooling, registers, ingestion sources, analysis
documents or manuals.)

| # | Commit | Date | What it did to the shipped YAML |
|---|---|---|---|
| 1 | `15c84de5` | 08-24 | Removed **60** uncited quantitative blocks from `architecture/`, `language/`, `guides/`, `application-notes/` (25 files). Fixed six detector defects in the same pass; the negative control grew 5 → 13 cases, three of them MUST-STILL-FIRE controls that caught a first attempt quietly switching the gate off. |
| 2 | `c733a223` | 08-25 | Removed **59** uncited blocks from `hardware/` (17 files) — and repaired the two citation-side false negatives (`Rev B` as a citation, a key-name test) that had made the previous zero false. Control set 12 → 25 cases. |
| 3 | `cd860ba7` | 08-25 | Defined all **55** undefined constants in one home; 116 `aliases:` made them reachable; created `pin-drive-configuration.yaml`; deleted `P_LEVEL_B` / `P_SCHMITT_B`. |
| 4 | `4cecb02c` | 08-25 | Corrected the drive-strength mislabel class; both fidelity tiers to zero; nine examples extracted from the shipped bytes, compiled, **and read**. |
| 5 | `1f37ae58` | 08-25 | Applied the promotion filter to 233 blocks; deleted the `150mA` pin-current figure and the TTL logic levels beside it. |
| 6 | `597d5eba` | 08-25 | **46** blocks return cited to `architecture/`/`language/`/`guides/`/`app-notes`; three shipped errors fell out of reading the sources first. |
| 7 | `491f2b55` | 08-25 | **34** blocks return cited to `hardware/`; the Goertzel/Digital-I/O misidentification corrected; E-004 closed. |
| 8 | `9370c580` | 08-25 | Drained the KB-side findings; **rejected** two register corrections that would have introduced defects. |
| 9 | `e92aa02f` | 08-25 | Drained the manual-prose findings; falsified this sprint's own "masters are clean" (F-356); corrected the EF-063/EF-064 attribution. |
| 10 | `69af3733` | 08-25 | Fixed the citations that route every new agent; measured what the crossref gate cannot see (76%). |
| 11 | `43b0ede2` | 08-25 | Armed both content instruments as blocking release gates, after repairing the harvest behind them (116 constants on the truth side where there were none). |
| 12 | `43061dad` | 08-25 | Restored the corrective sentence a duplicate `note:` had been silently discarding; swept 1130 files and filed F-360. |
| 13 | `ad4f974f` | 08-26 | Streamer pin capture: the `IN`-is-the-event-flag rule, a new `pin-capture.yaml`, and aliases for seven unreachable `streamer/` files. |
| 14 | `ccddcbe6` | 08-26 | Ingested the `#64008` Click Adapter from its schematic; **all 12 mikroBUS offsets confirmed, 0 corrections**; new `addon-click-adapter.yaml`. |
| 15 | `601e65ce` | 08-26 | Self-audit of that record: three inference-as-reading claims labelled with what actually establishes them. |
| 16 | `599d3660` | 08-26 | The WX module's two form factors; recovered content the purge had removed, from the ingestion tree. |
| 17 | `36196329` | 08-26 | Applied **F-363**, **F-368**, **F-369**, **F-370** — the first ingestion findings to reach the KB. |
| 18 | `491d033b` | 08-26 | Wrote the package record (**F-366** / G-021) and re-anchored **23** citations off the superseded capture (**F-365**); one did not resolve → **F-372** + **G-027**. |
| 19 | `75971308` | 08-26 | Repaired four red ledger items: GETCT's description, E-010's pull-up that survived a rewrite, the fabricated `digital_io_board` in two guidance lists, and the EF-063/EF-064 attribution in four more files. |
| 20 | `e9dc9507` | 08-26 | The content half of `d756b44c` (which staged only three ingestion-source renames): duplicate keys to zero, SETLUTS's own content back, DRVL/DRVH reconciled and cited, `edge-breadboard-carrier`'s supply figure and `addon-serial-host`'s identity restored, the `1224` symbol count corrected. **`d756b44c` + `e9dc9507` are one unit** — `git add` aborted atomically on the first; the pair was not amended. |
| 21 | `9a1f14a3` | 08-26 | Re-derived the six fabricated-provenance files; the interrupt vector map was inverted. §1.6. |
| 22 | `4caeb6cc` | 08-27 | Two residues the gates cannot see, found while verifying the differential read: `interrupts.yaml` contradicting its own corrected block, and **F-377**. |
| 23 | `ca07aaf7` | 08-27 | Restored the clock-setup declarations (the one gutted file) and stopped telling readers `_clkfreq` was required. §1.14. |
| 24 | `b466a538` | 08-27 | The E-016 sibling sweep found its case: `ADDSX`/`SUBSX` shipping the manual's wrong C-flag sentence while contradicting it in the same file, plus two `SUM*` encoding fields. **F-379**. |

**In the range, touching no shipped YAML, and load-bearing for this release:**
`d756b44c` (the three `p2-hub75-adapter` source renames — half of #20) ·
`02ff61b7` (armed `audit-yaml-duplicate-keys.py`) ·
`d62544ea` (repaired `audit-register-hygiene.py` so it reads the registers it was reporting clean on)
· `11ebec54` (regenerated the index **and** its gzip together, the pair F-357 records as having
drifted for four days) · `fc45912d` (the `deliverables/ai/P2/CHANGELOG.md` release entry).

**In the range and NOT this release's work:** `7be432a6` ("pnut-ts 015504, and the Dockerfile no
longer names the version") — another session, no KB YAML.

---

# Appendix B — Findings, errata and gaps referenced, with status at HEAD

Status read from the registers at HEAD, not carried from a task record. `RESOLVED` entries are
**closed and awaiting the next archive sweep**, not awaiting work.

## Corrections register — the entries this release moved or created

| ID | Status at HEAD | Subject |
|---|---|---|
| F-379 | `RESOLVED` | `ADDSX`/`SUBSX` shipped the manual's wrong C-flag sentence; two `SUM*` encoding fields malformed |
| **F-378** | **`CONFIRMED`** | `_CLKFREQ range` ships the compiler's acceptance range, unlabelled, 180 MHz past the datasheet ceiling |
| **F-377** | **`CONFIRMED`** | Translated locators that are in range and point at nothing; an eighth fabricated-provenance file |
| **F-376** | **`CONFIRMED`** | Two silent-failure bugs in the KB tooling, both exit 0 |
| **F-375** | **`CONFIRMED`** | The delivery filter strips `documentation_source:` from 383 files; 706 values are real citations |
| **F-374** | **`CONFIRMED`** | 40 quality-score sites across 18 files state a judgement, not a fact |
| **F-373** | **`CONFIRMED`** | Three top-level fields typed `text`; 14 shipped paths in them resolve to nothing |
| **F-372** | **`CONFIRMED`** | `%11011` says a new WRPIN needs no reset; the same document's general rule says the opposite |
| F-371 | `RESOLVED` | The sprint plan's "8 blocked sources" was wrong on five |
| F-370 | `RESOLVED` | ROM TAQOZ is an EARLY build, not just a cut-down one |
| F-369 | `RESOLVED` | The smart-pin DIR-reset mechanism, in the Silicon Doc and carried nowhere |
| F-368 | `RESOLVED` | `getbrk.yaml` dropped a Z value and declared `Z: No effect` for an instruction requiring one |
| **F-367** | **`CONFIRMED`** | `external-inputs/p2/` and `sources/silicon-doc/` hold different documents under one filename |
| F-366 | `RESOLVED` | No package record existed; the source had been in the repo unextracted |
| F-365 | `RESOLVED` | 23 shipped citations pointed into the superseded lossy capture |
| F-364 | `RESOLVED` | The register index advertised 16 files; 13 pointers did not exist |
| F-363 | `RESOLVED` | PA/PB described as "CALLD-imm parameter"; all three authorities say **return** |
| F-362 | `RESOLVED` | The hygiene gate reported CLEAN while reading zero entries |
| F-361 | `PENDING-VALIDATION` | `pin-selection.yaml`'s wrong sub-pin bit weights; the EF-065 trap as its example |
| F-360 | `RESOLVED` | Duplicate keys destroy content silently — **gate armed; wiring it into the release validator is still open** |
| F-359 | `RESOLVED` | Fabricated provenance headers — **the eight non-derivable claims are left standing for Stephen** |
| F-358 | `RESOLVED` | Check 10 had never once been able to fire |
| F-357 | `RESOLVED` | The index and its gzip drifted in committed history for four days |
| **F-356** | **`CONFIRMED`** | The drive-strength mislabel is alive in the IOSP master at 23 sites |
| F-355 | `RESOLVED` | The hygiene gate could not see the new errata register |
| **F-354** | **`CONFIRMED`** | Seven content-level holes inside blocks that DID come back |
| F-353 | `PENDING-VALIDATION` | The 58 in-scope hardware blocks, plus six wrong scalars in surviving blocks |
| **F-352** | **`CONFIRMED`** | Two shipped areas are authored-here with no upstream; the removal rule has no branch for them |
| F-351 | `RESOLVED` | The sourcing gate read part numbers and code points as amperes |
| F-350 | `PENDING-VALIDATION` | The eval-board fabrication class is not confined to one file |
| F-349 | `PENDING-VALIDATION` | PLL lock stated as ~10 µs in one place and ~10 ms in four |
| F-348 | `PARTIAL` | A *cited* block shipped a pin-current limit five times the absolute maximum |
| F-347 | `PARTIAL` | The `architecture/`-side purge removal record |
| F-345 · F-346 | `PENDING-VALIDATION` | Inverted flag polarity in a worked example; three structurally unrunnable examples |
| F-344 | `CONFIRMED` | A derived board extract contradicts itself about switch polarity → Parallax |
| F-343 | `PENDING-VALIDATION` | The Control Board credited with pull-ups its guide does not give it |
| F-342 | `RESOLVED` | A Parallax guide states the mislabel itself, in the one configuration where it cannot work |
| F-341 | `PARTIAL` | Six derived analysis documents sit inside the fidelity gate's documentary truth root |
| F-340 | `PARTIAL` | The crossref validator reads top-level keys only |
| F-338 | `PARTIAL` | `P_LEVEL_B` / `P_SCHMITT_B` do not exist |
| **F-337** | **`CONFIRMED`** | Datasheet + Hardware Manual vs Silicon Doc on `%TT` in DAC_MODE; the YAML follows the minority |
| **F-336** | **`CONFIRMED`** | The weak-drive idiom set is one composition wide, and that composition has no source |
| F-335 | `RESOLVED` | A whole class of board file mis-tiered into the advisory lane by a citation spelling |
| F-334 | `PENDING-VALIDATION` | The `hardware/` purge removal record; a citation token that silences the gate |
| **F-332** | **`CONFIRMED`** | Ten six-digit `%SSSSS` values for a five-bit field, with no reconciliation note |
| F-331 | `PENDING-VALIDATION` | Three of the six WRPIN D-operand fields mislabelled |
| F-329 · F-333 | `PARTIAL` · `PENDING-VALIDATION` | The fabricated drive ladder in blocks F-327 does not name; the same claim in a `description:` |
| F-328 | `PENDING-VALIDATION` | `p2-eval-board.yaml` describes a board the `#64000` guide does not |
| F-321…F-327 | `PENDING-VALIDATION` | The drive-strength mislabel class this sprint started from |

**One status was corrected while building this table.** F-360's headline read `CONFIRMED` while its
own body's closing line read ``Status: `RESOLVED` ``. Flipped to `RESOLVED`, which is what the body
establishes (4/4 sites fixed, gate armed, 0 duplicates across 1132 files). **The hygiene gate reports
CLEAN both before and after the flip**, so it cannot see this class: F-358's headline-vs-body check
reads `**Status:**` at column 0, and this entry states its status indented inside a bullet. Not
filed as a new finding — the allocator is the arbiter's — but it is the same shape as F-358.

**Register state at HEAD:** 103 live · 294 archived · 0 unaccounted · next `F-380`.
**Seven findings were filed during this sprint** (F-373…F-379), every one of them by a verification
step rather than by the work it was verifying.

## Source errata

**17 live, next `E-018`.** Referenced above: **E-004** (an RTC guide's "150 kΩ pull-up" mislabel —
closed in the KB by `491f2b55`), **E-007** (where two documents frame a limit differently, the KB
must label which framing it is quoting — applied by `ca07aaf7`, **not yet applied to F-378**),
**E-010** (the Edge guides' "enable a pin pull-up" — out of the shipped set as of `75971308`),
**E-012**…**E-016** (Propeller 2 Documentation v35 and the PASM2 Manual contradicting themselves),
and **E-017**, filed this sprint: `COGATN`'s operand width, where the Datasheet's prose says 8 bits,
its own instruction table says `D[15:0]`, and the Silicon Doc says 16.

**E-016 is the one that reached the shipped YAML.** Its sibling sweep is `b466a538` / F-379: the
manual is wrong **and our KB followed it**, in two of the eight files in the family.

## Knowledge gaps

**36 live, next `G-028` / `Q-010`.**

| ID | State | Note |
|---|---|---|
| **G-021** | **ANSWERED — APPLIED** | The TQFP-100 package drawing was in the Silicon Doc all along. Closed by `491d033b`. |
| **G-026** | **ANSWERED** | microSD boot selection is **P59**, not P60, and it is a DIP switch pair rather than a single pull-down — closed from the Edge Module Rev D guide. It corrects the Silicon Doc reviewer comment that raised the gap. The KB already carried the table; it was never connected to this gap. |
| **G-027** | **OPEN** | Can a new WRPIN reconfigure a *running* USB smart pin? Two editions of one document disagree. **Bench-testable and jumper-only.** Paired with F-372. |
| **G-020** | **OPEN — re-tested and CONFIRMED** | No thermal-design content exists anywhere in the corpus. The new package record says so explicitly rather than letting a reader infer a thermal solution from exposed-pad size. |
| **Q-009** | open | Under what conditions does RDFAST corrupt? Established as real by the designer in the Silicon Doc's own review thread, where both he and the reporter state they cannot explain it — so **no document can close it**. |

---

## How to re-derive every number in this document

```bash
G="git"   # the -c safe.directory workaround is retired: /etc/gitconfig carries
         # safe.directory=/workspaces/* at system scope (8778e6a2). Do not re-add it.

# Scope (§0.1)
$G diff --name-only  v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml' | wc -l     # 92
$G log  --oneline    v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml' | wc -l     # 27
$G log  --oneline    v1.17.0..HEAD | wc -l                                       # 118
$G diff --numstat    v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml' \
   | awk '{a+=$1;r+=$2} END{print a,r}'                                          # 6363 3402
$G diff --diff-filter=A  --name-only    v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml'   # 4
$G diff --diff-filter=DR -M --name-status v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml' # empty

# Blocks (§0.3) and shapes (§1.16): parse both revisions and compare top-level key sets / types
$G archive v1.17.0 deliverables/ai/P2 | tar -x -C /tmp/old
$G archive HEAD    deliverables/ai/P2 | tar -x -C /tmp/new

# Gates (§0.4) — run, never quoted
python3 engineering/tools/verify-yaml-format.py
python3 engineering/tools/validate-crossref-keys.py
python3 engineering/tools/validation/audit-yaml-claim-sourcing.py
python3 engineering/tools/validation/audit-constant-fidelity.py
python3 engineering/tools/validation/audit-extraction-digit-density.py --all
python3 engineering/tools/validation/audit-yaml-duplicate-keys.py
python3 engineering/tools/validation/audit-register-hygiene.py engineering/operations/P2KB-CORRECTION-FINDINGS.md
python3 engineering/tools/validation/audit-register-hygiene.py engineering/ingestion/KNOWLEDGE-GAPS.md
python3 engineering/tools/validation/audit-register-hygiene.py engineering/ingestion/SOURCE-ERRATA.md
python3 engineering/tools/validate-dod-release.py                                # 11 checks

# The index pair — regenerate TOGETHER, and AFTER the content commit (the index stores git blob sha256)
python3 engineering/tools/generate-p2kb-index.py
gzip -c deliverables/ai/p2kb-index.json > deliverables/ai/p2kb-index.json.gz
gzip -cd deliverables/ai/p2kb-index.json.gz | cmp - deliverables/ai/p2kb-index.json
```

**The tree is at release position and is deliberately unreleased.** No version bump, no tag, no push.
What still needs Stephen is in `engineering/analysis/2026-08-27-awaiting-stephen.md` — noting that
its item 1 predates the 2026-08-29 fix pass (§0.6), so read that item's *options* as still live but
its "already done" paragraph as superseded by §0.1 and §0.5 here.

**Reviewing this document is the release gate.** Stephen, 2026-08-29: *"we don't release until my
visual check of the all changes document confirms the content."* Nothing is tagged or pushed until
that read happens.
