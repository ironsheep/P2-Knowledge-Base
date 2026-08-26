# YAML release change ledger — `v1.17.0..HEAD`

**Purpose.** Everything that changed in `deliverables/ai/P2/**/*.yaml` since the last release, with
the reason it changed and **what was absent that let the defect exist**. Written for a release
review: the question this answers is *"is it safe to ship, and what did we lose that I cannot see
from a diffstat?"*

**Range.** `v1.17.0` (`7ff76b30`, 2026-08-21) `..` `0a5323ab` (2026-08-25).
**Measured on disk 2026-08-25.** Every number below was re-derived from git and from the parsed
YAML, not carried from a task record. Where a project record and the artifact disagree, the
artifact is reported and the disagreement is named.

**Two views of the same facts.** Part 1 groups by *reason* (a class usually crosses regions).
Part 2 goes region → file, every one of the 61.

---

## Part 0 — Reconciliation, and the eleven things to look at first

### 0.1 Scope, measured

| Quantity | Measured | Command |
|---|---|---|
| Commits touching KB YAML | **11** | `git log --oneline v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml'` |
| YAML files changed | **61** | `git diff --name-only v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml' \| wc -l` |
| Lines | **+3770 / −2751** | `git diff --numstat v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml' \| awk '{a+=$1;r+=$2} END{print a,r}'` |
| New files | **1** (`architecture/pin-drive-configuration.yaml`) | `git diff --diff-filter=A --name-only …` |
| Deleted / renamed files | **0 / 0** | `git diff --diff-filter=DR -M --name-status …` |
| Region spread | hardware 24 · language/spin2 11 · architecture 8 · language/pasm2 4 · architecture/smart-pins 4 · application-notes 4 · architecture/boot-rom 3 · guides 2 · code-examples 1 | `… \| awk -F/ …` |

`fc45912d` ("Write the release entry…") touched `deliverables/ai/P2/CHANGELOG.md` and no YAML — out
of scope, and not mentioned again. `deliverables/ai/P2/README.md` also changed (in `69af3733`) and
is likewise not a YAML file; noted once so its absence from Part 2 is not read as an omission.

### 0.2 The block accounting — where the dispatch numbers land

The two purges removed **top-level YAML blocks**, and that is the unit everything else counts in.

| Claim carried into this review | Measured | Verdict |
|---|---|---|
| 118 uncited blocks removed | **119** | off by one — 60 (`15c84de5`) + 59 (`c733a223`) |
| 79 returned carrying a citation | **80** | off by one — 46 + 34 |
| 13 never returned because disproven | **13 blocks ruled disproven; 12 of those keys are absent at HEAD** | the 13th (`io_pin_timing description`) *is* present, rewritten to state that the fabrication was a fabrication. Right as a content count, wrong as a key count. |
| — | **39 blocks did not come back at all** | 12 fabricated + 24 ruled true-but-not-actionable + 1 held for no ingestion home + **1 gap** + **1 assigned and never executed** |

Measured with: parse the top-level key set of every file at `<purge>^`, at `<purge>`, and at HEAD;
a key present before, absent after, and absent at HEAD is a block that never came back.

> **The register's own arithmetic differs by one from mine, in a knowable way.** `F-347` records
> `45 restored + 1 held + 1 gap + 13 never = 60`. It counts `architecture/io_pin_timing.yaml
> description` among the 13 "never returns" and states *"all nine `io_pin_timing.yaml` keys …
> return `grep -c` = 0."* That key is present at HEAD. The **content** never returned — the
> fabricated slew-rate claim is gone — but the **key** did, carrying new text. Substance holds;
> the verification sentence does not.

### 0.3 Eleven things to look at before shipping

Ordered by what a consumer of the KB would hit.

1. 🔴 **A duplicate YAML key silently destroys the sprint's own central statement.**
   `architecture/pin-drive-configuration.yaml` has `note:` twice inside `idioms:` — once at the top
   (the block scalar that says *"%M..M selects DRIVE STRENGTH, and the Pin Mode Legend enumerates
   the whole field — C, I, O, HHH, LLL — with no bias-resistor selector among them"*), and again at
   line 250. Under any YAML loader the **second wins**, so every consumer of this file — the index
   generator, the MCP server, an agent — reads the bench-gap paragraph where the corrective
   statement should be. The corrective sentence is unreachable at parse time.
   `idioms.gap_no_dedicated_bench_test` also parses as `null` (its intended body became the
   duplicate `note:`).
   *Introduced by `e92aa02f` in a file created by `cd860ba7`. This is the one item I would not ship
   past.*
   `python3 -c "import yaml;d=yaml.safe_load(open('deliverables/ai/P2/architecture/pin-drive-configuration.yaml'));print(d['idioms']['note'][:80])"`

2. 🔴 **A block assigned to a task, recorded as handed over, and never executed.**
   `language/spin2/methods/getct.yaml` lost its top-level `description:` in `c733a223` and never got
   it back. `F-353` explicitly carves it out (*"is outside this tree and belongs to «#299»"*);
   `F-347`'s 60-row outcome table does not contain it; and `F-334`'s disposition asserts *"Nothing on
   either record is still owed."* The artifact says otherwise. **GETCT — the most-consulted timing
   method in the set — now ships with no description at all.**
   `python3 -c "import yaml;print('description' in yaml.safe_load(open('deliverables/ai/P2/language/spin2/methods/getct.yaml')))"`

3. 🔴 **A board name this release identified as invented still stands twice, in the file that
   corrected it.** `hardware/p2-hardware-feature-comparison.yaml` renamed `digital_io_board` →
   `goertzel` and added a `correction_note` reading *"No such board exists in the #64006 series."*
   Two lists in the same file still name it: `feature_matrix.educational_progression.intermediate_path`
   (line 336) and `feature_matrix.application_domains.user_interfaces` (line 345).
   `grep -rn digital_io_board deliverables/ai/P2/`

4. 🔴 **`E-010` is still live in the shipped set.** Both Edge Module YAMLs end
   `pin_mapping.led_pins.mechanism` with *"Drive the pins high or low (or enable a pin pull-up) to
   control the LEDs deterministically."* The P2 has no pull-up to enable. The errata entry is
   `CONFIRMED`, not resolved, and both lines were **re-written in this release** (`491f2b55`) with
   the phrase intact.
   `grep -rn 'enable a pin pull-up' deliverables/ai/P2/`

5. 🟠 **The EF-063/EF-064 attribution was corrected in one file and left standing in four.**
   `e92aa02f` established that neither empirical finding is a drive-strength finding — they are rig
   apparatus for other measurements — and rewrote `pin-drive-configuration.yaml idioms.source` to
   say so. Four other shipped files still present them as the empirical basis:
   `language/pasm2/concepts/basic-io.yaml:233,:244`, `language/spin2/concepts/basic-io.yaml:172,:183`
   (*"This was measured on real silicon (EF-063, EF-064, 2026-08-20)"*),
   `application-notes/p2an004-…yaml:98` (*"hardware-verified in EF-063/EF-064"*), and
   `hardware/addon-rtc.yaml:73`.
   `grep -rn 'EF-063\|EF-064' deliverables/ai/P2/`

6. 🟠 **Shapes changed under consumers, in 24 files, and nothing checks shape.** 30 keys changed
   YAML type this release — `list → dict` mostly, plus `str → dict` for five hardware `description:`
   keys. `signal_map:` is now a mapping in 5 hardware files and a bare list in 9; at `v1.17.0` all
   14 were lists. `gotchas:` is a mapping in 3 application notes and a list in 4. This is a
   **judgement, not a correction** — it was made to give each block a `source:` key — and it is the
   change most likely to break something downstream. See §1.10.

7. 🟠 **A board file that had a wrong number now has no number.**
   `hardware/edge-breadboard-carrier.yaml` shipped *"6-9V barrel jack (recommended)"*; the #64020
   guide says 5 VDC, absolute maximum 5.5 V. The wrong figure was removed with the whole
   `power_specifications` / `power_management` / `specifications` set, and **no supply figure
   returned to that file** — nor did its dimensions. The right numbers now live only in
   `p2-hardware-feature-comparison.yaml`. Its two sibling carriers each gained a
   `connectivity.power_input` line; this one did not.
   `grep -ni 'VDC\|barrel\|volt' deliverables/ai/P2/hardware/edge-breadboard-carrier.yaml`

8. 🟠 **A board file lost its identity string.** `hardware/addon-serial-host.yaml` has no top-level
   `description:` and no `basic_info:` — the removal was a deliberate CORRECT-BUT-NOT-ACTIONABLE
   ruling, but nothing put a one-line "what this board is" back. It is the only hardware file in
   that state that this release created.

9. 🟡 **A pre-existing duplicate key survived a file this release edited.**
   `hardware/edge-breadboard-carrier.yaml` has `educational_value:` twice (line 205 wins). Present
   at `v1.17.0`, so not introduced here — but the file was edited twice this range and the defect
   was not caught, because nothing checks for duplicate keys.

10. 🟡 **A metadata field that contradicts its own file, in the file the promotion filter cited for
    its size.** `language/spin2/symbols/spin2-builtin-symbols-complete.yaml` states
    `total_symbols_extracted: 1224`. The file holds **136** symbol records (68 before, 68 added).
    Pre-existing; but `cd860ba7` edited the adjacent line in the same block and left it, and the
    promotion filter's reason for ruling that block ACTIONABLE is *"1224 symbol values and bit
    patterns."*

11. 🟡 **A `#64006` add-on YAML now cites loose files at the ingestion root.**
    `hardware/hub75_adapter.yaml`'s new `source:` keys point at
    `engineering/ingestion/sources/p2-hub75-adapter/p2-hub75-adapter-official-specs.md` and
    `…-complete-pinout.md` — loose files at the truth root, which is the shape `F-341` flags and
    which `43b0ede2` structurally excluded from the constant-fidelity truth side. For this board
    they are the *manufacturer's own* specification (Iron Sheep Productions), so the citation is
    defensible on authority; it is the location that is anomalous. **Stephen's call.**

12. 🔴 **`F-359`, filed by another agent while this ledger was being written, qualifies the `0 Tier 1`
    above — read it before reading §0.4 as reassurance.** It establishes that seven `architecture/`
    files carry a **fabricated provenance header** — citing silicon-doc files that have never
    existed (`part3-pins.txt`, `part1-cog.txt`) and datasheet page ranges beyond the end of a
    50-page datasheet — and that **the fabricated header is what satisfies the sourcing gate's
    citation regex**, because the matcher fires on the tokens *"Silicon Doc"* and *"Datasheet"*
    wherever they appear. All seven were written in one 2025-11-29 commit that touched 973 YAMLs.
    **One of the seven is in this release's change set: `architecture/io_pin_timing.yaml`** — and it
    was caught this sprint only because it *also* had blocks with no header coverage at all. The
    other six are unchanged in this range and therefore outside this ledger's scope, but at least
    **9 quantities** across three of them still stand under an invented citation. Status
    `CONFIRMED`, not fixed; the entry says explicitly that the scope decision is Stephen's and that
    *"what must NOT happen is shipping while believing the `0 Tier 1` covers them."*
    *Not my finding, and not verified by me — recorded here because it lands inside this ledger's
    scope and arrived after §0.4 was measured.*

### 0.4 Gate state at HEAD

Run, not quoted:

| Gate | Result |
|---|---|
| `audit-yaml-claim-sourcing.py` | `PASS` — Tier 1 none across 1130 files; **49 Tier-2 advisory blocks remain** in wholly-uncited files (advisory, non-blocking) |
| `audit-constant-fidelity.py` | `PASS` — Tier 1 none, Tier 2 none, across 120 source-defined constants; truth side 35 files, editions `spin2-v51` + `spin2-v55` |
| `validate-crossref-keys.py` | exit 0 — `ALL TOP-LEVEL CROSS-REFERENCES RESOLVE — 688 nested site(s) NOT checked (F-340)` |
| YAML parse, all 61 changed files | 0 parse errors; **2 duplicate-key defects** (items 1 and 9 above) |

Neither armed gate can see any of items 1–11. Both print that themselves. And per item 12, a green
`0 Tier 1` is satisfied by a fabricated citation as readily as by a real one — so the sourcing
gate's green is narrower than it reads.

---

# PART 1 — By change class

A class is one *reason*. Each carries: what it is · **the lack** — what was absent that let it exist
or persist · every file it touched · the net effect.

---

## 1.1 The uncited-quantity purge — 119 blocks, 41 files

**What.** Every top-level block that stated a physical quantity without naming a source was deleted:
60 from `architecture/`, `language/`, `guides/`, `application-notes/` (`15c84de5`, 25 files) and 59
from `hardware/` plus one straggler (`c733a223`, 17 files). Removal moved first, on purpose: the
damaged set was being served while the repair ran.

**🔴 The lack.** *Nothing had ever compared a quantitative claim against a citation.* There was no
rule that a shipped number must name the document it came from, and no instrument that could tell.
`audit-yaml-claim-sourcing.py` did not exist before this sprint; the moment it did, it found 119
blocks. The purge is not a discovery about the KB so much as a discovery about the toolchain.

> **And the lack goes one level deeper than the purge reaches.** `F-359` (filed 2026-08-25, §0.3
> item 12) establishes that for at least seven `architecture/` files, *"nothing checked generated
> content against a source at creation time, and the citation header was generated along with the
> content it claims to source."* A fabricated citation is not a sourcing error — **it is the
> signature of never having sourced**, and 973 YAMLs in one commit is the scale at which that
> becomes invisible. The purge could only find blocks with *no* citation; a block with an *invented*
> one passes.

**Files (41).** All of `application-notes/` (4) · `architecture/boot-rom/` (3) ·
`architecture/` {click_module_integration, clock_system, io_pin_timing, pin-power-domains,
serial_loader, smart_pin_patterns, smart_pins} · `architecture/smart-pins/`
{00011-dac-16bit-pwm-dither, 11011-usb-host-device} · `guides/pasm2-getting-started` ·
`language/pasm2/` {concepts/basic-io, concepts/streamer_smartpin_control, setxfrq} ·
`language/spin2/` {concepts/basic-io, debug-commands/pc_key, methods/getct, methods/waitms,
methods/waitus} · `hardware/` (16 files).

**Net.** −1043 lines in `15c84de5`, −1500 in `c733a223`, with **4** insertions between them (three
end-of-file newlines and one line). Pure subtraction, by design.

---

## 1.2 Source-first repopulation — 80 blocks returned, cited

**What.** `597dba` (arch/lang/guides/app-notes, 24 files, +867/−6) and `491f2b55` (hardware, 17
files, +1417/−141) went back to the **source documents**, not to the removal list, and wrote each
block from what the document states. Every returned block carries a `source:` key naming a document
and a `file:line`.

**🔴 The lack.** *A purge keyed on citation-absence is orthogonal to truth and to belonging.*
Removal could only say "unsourced"; it could not distinguish *true but uncited* from *false*. Until
`2026-08-25-whole-kb-promotion-filter.md` dispositioned all 233 blocks by hand, no pass had ever
read a block and decided what it was. That read is what separates §1.2 from §1.3.

**Two effects worth naming, because neither is visible in a diffstat:**

- **Several blocks came back with different content, not the same content plus a citation.**
  `guides/pasm2-getting-started.yaml file_structure` returned as the Parallax v55 minimal PASM
  program, dropping the KB's own CON/DAT worked example. `architecture/clock_system.yaml pll_system`
  returned as the datasheet's bit-field tables, dropping the KB's own `constraints:` summary.
- **A returned block can be smaller than what it replaced.** `p2an001` gotchas went 7 items → 6;
  `p2an004` 7 → 6. Named per file in Part 2.

---

## 1.3 The 39 blocks that did not come back — three different outcomes, kept apart

Removal and non-return are the same diff line and four different decisions. They must not be read
as one number.

### (a) Fabricated — 13 blocks ruled disproven, 12 keys absent at HEAD

The `F-327` family: a per-pin milliamp drive ladder (1.5 / 3 / 15 / 30 / 75 / 150 mA with invented
impedances ~2000 Ω … ~20 Ω), a programmable slew-rate control, and a propagation / rise / fall
timing model built on top of both.

| File | Blocks |
|---|---|
| `architecture/io_pin_timing.yaml` | `timing_specifications` · `clock_relationships` · `drive_strength_configurations` · `slew_rate_control` · `input_characteristics` · `special_timing_modes` · `protocol_timing_examples` · `compensation_techniques` (8 keys) — plus `description`, whose key returned carrying wholly new text |
| `language/pasm2/concepts/basic-io.yaml` | `drive_strength_configuration` · `timing_considerations` |
| `language/spin2/concepts/basic-io.yaml` | `drive_strength_configuration` · `timing_considerations` |

**🔴 The lack.** `"slew"` returns **zero hits** across every ingested Parallax source — Silicon Doc,
both Spin2 editions, the smart-pins catalog, the re-ingested Datasheet and Hardware Manual. Nothing
had ever asked the corpus whether a feature the KB documents exists at all. The claim survived
because it was *plausible for a modern CMOS part*, and plausibility was the only filter in place.

The real ladder — eight rungs, FAST / 1.5 kΩ / 15 kΩ / 150 kΩ / 1 mA / 100 µA / 10 µA / float — is
in `architecture/pin-drive-configuration.yaml drive_ladder`, cited to the Datasheet Pin Mode Legend,
with a `no_other_rungs` key stating *"Any per-pin current or impedance figure beyond them is not in
the source."*

### (b) True, and still out — 25 blocks the promotion filter ruled not-actionable

The test applied to every block: **"can this change the code an agent emits?"** These could not, so
they left the shipped set for the ingestion tree.

| File | Blocks held out |
|---|---|
| `hardware/addon-hd-audio.yaml` | `set_contents` · `use_cases` |
| `hardware/addon-hyperram-hyperflash.yaml` | `host_note` |
| `hardware/addon-motor-driver.yaml` | `power_signals` · `protection` |
| `hardware/addon-rtc.yaml` | `power_signals` · `specifications` |
| `hardware/addon-serial-device.yaml` | `specifications` · `rev_b_5v_note` |
| `hardware/addon-serial-host.yaml` | `description` · `specifications` · `power_requirements` · `limitations` |
| `hardware/addon-wx-wifi.yaml` | `part_variants` · `specifications` |
| `hardware/edge-breadboard-carrier.yaml` | `specifications` · `specialized_features` · `power_specifications` |
| `hardware/edge-mini-breakout.yaml` | `specifications` · `power_management` |
| `hardware/edge-standard-breakout.yaml` | `specifications` · `power_management` |
| `hardware/edge-standard-module.yaml` | `revision_history` |
| `hardware/hub75_adapter.yaml` | `power_requirements` |
| `architecture/io_pin_timing.yaml` | `best_practices` (generic PCB layout; no ingestion home either) |

**🔴 The lack.** *"Belonging" had no owner and no test.* `deliverables/ai/P2/README.md` claims the
set is "optimized for AI code generation" and nothing enforced it, so a block could be true,
technical, well-formed and still displace what an agent needs. **This is a judgement class in its
entirety** — every one of these was decided by reading, not measured. Two consequences worth
reviewing (items 7 and 8 in §0.3).

### (c) A gap — 1 block ruled ACTIONABLE that no source states

`architecture/click_module_integration.yaml best_practices` (25 lines: *"Always use offset
constants, never hardcode pins"*, *"Make base pin a runtime parameter"*, reset-during-init,
configure-before-enable). Ruled **ACTIONABLE** — it is literally the shape of emitted code — and
then found to have **no upstream anywhere**: the file's own `documentation_source: code_analysis`
points at our own reading. Recorded as a gap under `F-352` and deliberately not restored.

**🔴 The lack.** The KB has authored-here content with no ingestion home, and sub-rule P of the
promotion filter had no branch for it — the rule assumed a block either *is* in the ingestion tree
(remove it) or *should be written there first*. There was no "stays, and say why" branch, so this
one left. That file is now **+0 / −25**: pure loss.

### (d) Not executed — 1 block, item 2 of §0.3

`language/spin2/methods/getct.yaml description`. Handed from `#307` to `#299` in writing; absent
from `#299`'s own outcome table; absent from disk.

**🔴 The lack.** *Nothing closes the loop between a disposition document and the tree it
dispositions.* The promotion filter was written as an instruction to two later tasks, and no check
compares the instruction against the result. One scripted key-set comparison found this in a single
pass — it did not need a human read.

---

## 1.4 The drive-strength mislabel — the class this sprint started from

**What.** The 16 `P_HIGH_*` / `P_LOW_*` selectors were documented across the KB as internal pull-up
and pull-down **resistors**. The P2 has none. They select a **drive strength**, and a drive
selection is live **only while `DIR` is high** — so every worked example that configured a weak
drive and then floated the pin was teaching a mechanism that does nothing.

`4cecb02c` (12 files, +109/−81) resolved the five remaining `CONTRADICT` rows structurally: no file
restates the mechanism; each now points at the single definition home.

| Region | Files |
|---|---|
| `architecture/smart-pins/` | `smart-pin-00000-normal-mode.yaml` — Spin2 and PASM2 examples both rewritten; `PINFLOAT`/`DIRL` → `PINHIGH`/`DRVH` |
| `code-examples/` | `smart-pins-002-button-reading.yaml` — one word: "Pull-up or pull-down resistor" → **"External** pull-up or pull-down resistor" |
| `guides/` | `pasm2-getting-started.yaml`, `spin2-getting-started.yaml` — the routing blurb no longer promises "pull resistors" |
| `hardware/` | `addon-control-board.yaml` — "Use internal pull-down (P_LOW_15K)" → weak-low-drive-with-DIR-high, ×4 switch rows + the init pattern; `p2-hardware-feature-comparison.yaml` — "Current limiting resistors, pull-up resistors" → the 470 Ω the guide actually states |
| `language/pasm2/` | `concepts/basic-io.yaml` — `internal_pull_resistors` returned corrected, with `there_is_no_bias_resistor_selector` and `the_dir_rule` |
| `language/spin2/` | `concepts/basic-io.yaml` (same); `conventions/johnny-mac-documentation-style.yaml` + `conventions/spin2-docs-jonnymac.yaml` (the inline-PASM sensor example); `methods/cogstop.yaml` ("may need **external** pull-up/down resistors"); `methods/pinfloat.yaml` (adds *"a drive-strength selection applies only while the pin drives"*) |

**Also killed: an idiom that is ours.** `P_HIGH_15K | P_LOW_FLOAT` was attributed in `F-322` to a
Silicon Doc section titled *"Weak Pull-Up"*. **No such section exists.** The string was written into
a derived catalog extract of ours, beside hand-authored commentary, and read back as source. It now
appears in `pin-drive-configuration.yaml not_documented_here` as an explicit non-statement:
*"has no Parallax documentary statement and no empirical record."*

**🔴 The lack — three of them, and they are different.**

1. **`audit-constant-fidelity.py` reads constant NAMES.** A block that names `P_HIGH_15K` correctly
   and *describes* it as a resistor passes a name check and a citation check. Name coverage is not
   semantic coverage — the tool prints that itself now.
2. **Where the phrase carries no `P_*` symbol at all, neither instrument can see it.** That is
   exactly the Edge-module case (`E-010`, §0.3 item 4): *"have I/O pin pull-ups activated"* names no
   constant, so the fidelity gate is blind, and it states no quantity, so the sourcing gate is
   blind.
3. **`F-321`'s applied sweep was scoped to `language/`.** `hardware/` was never in it. The class was
   found in one tree and fixed in one tree; the second tree took `491f2b55` and `43b0ede2` to reach,
   and two files still carry it.

**And the sprint's own scope measurement was false.** `e92aa02f` re-ran the check that had declared
the manual masters clean and found **23 mislabel lines, 5 internal-pull-up assertions and 4 sites
teaching the invented composition** in the IOSP master — a flat glob had missed a per-chapter
directory tree. Filed as `F-356` rather than fixed, because scope is Stephen's. *No YAML
consequence; recorded here because it changes what "this class is closed" means.*

---

## 1.5 One definition home, and the block that made it reachable

**What.** `cd860ba7`, 5 files, **+1338 / −45**.

- **`architecture/pin-drive-configuration.yaml` — new file, 275 lines.** The 13-bit `%M..M` field:
  sub-fields with bit ranges, the eight-rung drive ladder **stated by encoding**, the `DIR`/`OUT`
  rule, two hardware-grounded idioms, and a `not_documented_here` block naming what no source
  states (open drain, open source, keeper/bus-hold, per-pin current beyond the eight rungs).
  *Deliberately expressed by encoding, never as name-to-description, so the fidelity tool does not
  read it as a second definition home for sixteen constants.*
- **`language/spin2/symbols/spin2-builtin-symbols-complete.yaml` — +1036 / −20.** 68 new `P_*`
  records (48 → **116**, every v55 constant, each defined exactly once, no duplicates), worded from
  **Spin2 v55** rather than the v51 extracts. Plus a **top-level `aliases:` block of 116 names.**
- **De-duplication by pointer, not by correction.** `language/spin2/methods/wrpin.yaml` deleted its
  13 restated mode constants and its 4 `%TT` constants; `language/pasm2/wrpin.yaml` replaced its
  six D-operand field descriptions with a reference (three of the six had drifted wrong — `F-331`);
  `architecture/smart_pins.yaml` gained a `sub_fields_reference` and a `related:` block.

**🔴 The lack — two, and the second is the sharper one.**

1. **A constant was used and defined nowhere, and no instrument compared use against definition.**
   An agent meeting `P_ADC_GIO` or `P_HIGH_1K5` in the shipped set had no way to resolve it. 55
   constants were in that state. *That is the mechanism behind the failure that started this
   sprint* — an agent could not work out how to configure a pull-up, and reported contradictions
   around smart pins.
2. **`generate-p2kb-index.py` harvests top-level `aliases:` ONLY, and this file had none.** So the
   **48 constants it already defined were unreachable by name through the published index**, and
   the 55 new ones would have satisfied every gate while leaving the reporting agent exactly where
   it started. Defining them was necessary and not sufficient; nothing made the definitions
   *findable*. The `aliases:` block is the fix at the mechanism.

**And how two fabricated names survived.** `P_LEVEL_B` and `P_SCHMITT_B` do not exist —
`pnut-ts` rejects them while seven real siblings compile, and v55 carries only their `_FB`/`_FBP`/
`_FBN` forms. They stood in four `related_symbols:` lists and were deleted with nothing
substituted. **The lack:** `validate-crossref-keys.py` iterates a fixed field list against the
**top level** of each document. This file carries **135 nested `related_symbols:` lists** and the
validator reports `related_symbols: 7 resolved` for the entire corpus — all seven from one
unrelated file. The names sat in a field the instrument names in its own vocabulary and does not
read. That measurement is now printed on every run (`688 nested site(s) NOT checked`).

> ⚠️ **Claim vs diff.** The commit subject says *"Define all 55 undefined constants."* The diff adds
> **68** records. Both are true — 55 were referenced-but-undefined, 13 more were v55 constants the
> KB referenced nowhere — but the subject understates the file change by 13 records.

---

## 1.6 Wrong scalars that were cited, or looked cited

Six numbers, each of which an agent would have emitted.

| Scalar | Was | Is | Where | The lack |
|---|---|---|---|---|
| `max_current_per_pin` | **150 mA** | *removed*; the datasheet's **±30 mA** absolute max is carried, cited, in `io_pin_timing.yaml absolute_maximum_ratings` | `language/pasm2/concepts/basic-io.yaml`, `language/spin2/concepts/basic-io.yaml` (byte-identical twins) | 🔴 **The citation test matched the bare word "datasheet" inside a neighbouring *deferral*** — `max_current_total: "Check datasheet for package limits"`. Every other block judged cited by an inline token names a real document; this one named none, and absence-of-citation was therefore never detected. It survived **both** purges. `F-348` |
| `VIL_max` 0.8 V / `VIH_min` 2.0 V / `VOL_max` 0.4 V / `VOH_min` 2.4 V | shipped | *removed* | same two files | 5 V-TTL boilerplate the P2 datasheet does not contain — it states a single ratiometric `Vih` of `Vxxyy × 0.3/0.5/0.7`, and `Vol`/`Voh` as millivolt drops at a stated current. Same false-negative citation. |
| PLL lock | **~10 µs** | **10 ms** (crystal+PLL); 5 ms crystal-only | `architecture/clock_system.yaml stabilization_timing` | Three Parallax sources state 10 ms, each via two independent extraction paths, and all three *emit* `WAITX ##20_000_000/100`. `F-349` |
| the same error, in code | `WAITX ##20_000_000/10000  ' Wait 100µs for PLL lock` × 2 | `WAITX ##20_000_000/100  ' Wait ~10ms` | `clock_system.yaml programming_examples` — `pll_160mhz_from_20mhz_crystal` and `overclock_250mhz` | 🔴 **The sourcing gate strips code regions by design**, so a wrong constant inside an example is structurally invisible to it. `F-349` found these by working the file, not the finding's own list. |
| `WAITMS` max | *"~4,294 seconds (71 minutes)"* | `$8000_0000` **clocks** — `max ms = $8000_0000 / (CLKFREQ/1000)`, ≈ 10.7 s at 200 MHz | `language/spin2/methods/waitms.yaml` | The old figure is 2³² milliseconds — the argument's own 32-bit range read as the wait the chip performs. Nothing compared a stated range against the **unit the source states the bound in**. |
| `WAITUS` max | *"1–4,294,967,295 µs"* | same `$8000_0000`-clock bound | `language/spin2/methods/waitus.yaml` | same |
| `FIT $1F0` / "496 longs" | shipped | `FIT $1F8`, with `why_1F8` explaining `$1F0..$1F7` are dual-use | `guides/pasm2-getting-started.yaml size_checking` | v55 states the default cog limit as `$1F8`; `$1F0` was a habit, not a source. Marked in-file as `correction_2026_08_25` and **not restored**. |

> ⚠️ **One of these corrections overstates itself.** `waitms.yaml correction_2026_08_25` says the old
> figure was *"three orders of magnitude"* too large. `2³¹ / 200 MHz` = 10.74 s against a claimed
> 4,294 s is **≈ 400×** — between two and three orders of magnitude, and ~40× at 20 MHz. The
> correction is right; its own multiplier is not. Same wording in `waitus.yaml`.

---

## 1.7 Board facts — what the boards actually are

`491f2b55` + `1f37ae58` + `43b0ede2`. The largest single-region correction in the release.

**#64006G is the Goertzel board, not a "Combined Digital I/O" board.** The KB described a board with
4 LEDs, 4 switches, 4 shared pins and "electrical isolation". No such board exists in the series.
The entry is now the Rev B Goertzel experimenter board with its five sense pads and three
switch-style pads, plus a `correction_note` naming the fabrication class. *(Residual: §0.3 item 3.)*

**Invented part numbers, deleted.** `P2-EVAL-STD-BREAKOUT`, `P2-EVAL-MINI-BREAKOUT`,
`P2-EVAL-BREADBOARD-CARRIER` → `64029`, `64019`, `64020`. `64000-ES` was carried as the P2-EC32MB's
`alternate_part` and as an alias — it is a **different product** (the limited-edition P2-ES Eval
Board); removed from both, with the reason in-file.

**A barrel jack that does not exist**, and one that does. `p2-hardware-feature-comparison` said the
#64000 eval board takes *"5V USB or 6-15V barrel jack"*. It has **two micro-USB sockets and no
barrel jack**. The three Edge carriers *do* have one — centre-positive 2.1 mm, 5 VDC, absolute max
5.5 V — and now say so.

**All three Edge carriers were credited with a built-in USB-to-serial converter.** None has one.
Every one now states *"the board has no on-board USB-to-serial converter"* and names the Prop Plug
(#32201) as the only wired path, plus the WX wireless option.

**Other corrections, each on the board's own guide:**

| Was | Is | File |
|---|---|---|
| Eval board = "Rev D" silicon, "PLL to 320MHz", flash "TBD", dimensions "TBD" | Rev C `P2X8C4M64PES`, recommended max **180 MHz**, **16 MB W25Q128JVSIM**, **3.55 in × 3.55 in** | `p2-eval-board.yaml` |
| Eval board has a prototyping area, user switches, 0.1″ headers, VGA/HDMI/audio, USB-B/USB-C, Prop Plug header | all six removed — `grep` over the repaired capture returns zero hits for every one | `p2-eval-board.yaml` (`1f37ae58`) |
| "Up to 2 add-on boards", "A-side (P32-P39) + B-side (P24-P31)" | **eight** I/O breakout edge headers covering all 64 pins in 8 groups of 8 | `p2-hardware-feature-comparison.yaml` |
| Edge modules "27×40mm" | **1.45 × 2.04 in (37 × 51.7 mm)** | `p2-hardware-feature-comparison.yaml` |
| P2-EC32MB `io_pins_total: 64` | **46 accessible, 40 fully free** (P40–P57 are PSRAM) | `p2-hardware-feature-comparison.yaml` |
| P2-EC32MB `fully_free_pins: 38` | **40** — *"The value shipped here was 38, which no source states."* | `edge-standard-module.yaml comparison_with_32mb` |
| A/V breakout `pins_required: 16`, `rca_outputs: 3` | **8** pins, **4** RCA sockets | `p2-hardware-feature-comparison.yaml` |
| Mini breakout "3.3V input only", "All 64 pins on edge castellations" | 5 VDC barrel jack; **40 pins** at five header sockets, P32–P55 reachable only by soldering | `p2-hardware-feature-comparison.yaml`, `edge-mini-breakout.yaml` |
| Carriers `crystal_frequency: 20MHz` | *"n/a — the crystal is on the edge module"* | `p2-hardware-feature-comparison.yaml` |
| HUB75 "40 MHz max (35 MHz reliable)", "13 ns propagation", "Maximum 3 chains", "does not use P2 streamer", per-panel current table, clock/latch/OE pulse widths | removed with an explicit `gap_*` key naming what would settle each; manufacturer states **70 MHz** | `hub75_adapter.yaml` |
| Control board `current_per_led_ma: 4`, `total_current_ma: 16`, "~2.0 V LED drop", "~20 ms" debounce | removed — the #64006A guide states 470 Ω and nothing else | `addon-control-board.yaml` (`43b0ede2`) |

**🔴 The lack — two distinct ones.**

1. **For the eval board: the source capture had lost every numeral.** The #64000 guide's text layer
   OCR'd without digits, so the KB filled the gaps with plausible values and `TBD`s. Nothing
   measured **digit density** on an ingested capture until `8167f233` armed that gate and forced a
   re-ingestion (`F-250`). Every quantity in `p2-eval-board.yaml` now traces to the repaired
   capture, triple-validated against OCR text, original text layer, and rendered page.
2. **For the Goertzel board and the five eval-board fabrications: they carry no unit-bearing
   quantity, so the sourcing gate structurally never inspected them.** *"Combined Digital I/O"*,
   *"USB-B or USB-C"*, *"Basic prototyping area"* — none of these is a number, so two purges passed
   over all of them. `F-328(b)` is the record; the promotion filter's own note is
   *"the six items the sourcing gate structurally cannot see."*

> **One item the dispatch expected to be a fabrication and is not.**
> `p2-eval-board.yaml expansion_ecosystem.individual_addons` was flagged as invented and is a real
> cross-reference roster: #64032 HUB75 has its own KB file, #64008 MicroBUS appears in the ingestion
> tree. **Kept.** Recorded because a review that only lists what was deleted teaches the wrong
> lesson.

---

## 1.8 Not-actionable content removed — the promotion filter

Covered as an outcome in §1.3(b); the *reason* belongs here because it is its own class.

**What.** `2026-08-25-whole-kb-promotion-filter.md` applied one test — *"can this block change the
code an agent emits?"* — to 233 blocks: the 114 that survived the purges and the 119 the purges
removed. `1f37ae58` executed the removals it could execute within `architecture/`/`language/`
(4 files, +0/−43); `491f2b55` executed the hardware side by not returning 24 blocks.

The boundary is not where instinct puts it. `p2-hardware-selection-guide.yaml` is a **buying guide,
entire** — three blocks of purchase decision trees, dollar estimates and curriculum week counts,
nothing naming a pin, constant or bound. `hardware-compatibility-matrix.yaml` **splits three-three**
in the same file: `addon_board_host_compatibility` (pins per board), `performance_considerations`
(the 50 Hz flicker floor) and `incompatibilities` (the P0–P7 conflict rule) pass;
`physical_stacking_constraints`, `power_compatibility` and `optimal_configurations` fail.
`advantages:` blocks **fail as a class** — marketing bullets whose every technical fact is already
stated actionably in the same file.

**🔴 The lack.** See §1.3(b) — "belonging" had no owner and no test. And a second one the filter
surfaced about itself: **the three dispositions have no slot for *apparatus*.** Provenance blocks,
cross-reference indexes and `aliases:` are not claims and change no emitted code — the test says
"not actionable", and acting on that would strip the trust chain and break findability. Five blocks
landed there and were retained by exception rather than by rule.

**Two boundary calls worth a second look, because both could have gone the other way:**

- `hardware/p1_rom_font_character_set.yaml character_categories` → **ACTIONABLE**. A 256-entry font
  table reads as reference data; the codes are byte constants an agent emits to draw on a P2 text
  display. Code 189 + 190 is *how you draw a resistor*.
- `hardware/addon-microsd.yaml power_signals` → **NOT ACTIONABLE**, despite being a
  "what-is-wired-where" hardware fact, because nothing an agent emits changes based on VIO3V3
  powering the card. The contrast is `addon-serial-host`, whose 5 V rail *is* software-enabled at
  two named offsets and therefore passes.

**And one place the filter's own rule ran out.** The buying-guide content has **no ingestion home**:
`grep -rln '\$150-200\|educational_rating\|cost_tier'` over `engineering/ingestion/sources/` returns
nothing. It is authored-here content with no upstream, which cannot be "returned" to a tree it never
came from — so it **stays**, now labelled in-file: *"authored in this knowledge base and have NO
upstream source in the ingestion tree … treat them as guidance, not as documented fact"*
(`p2-hardware-feature-comparison.yaml selection_criteria`, and an `authored_here_note` above
`educational_progression`). `F-352`.

---

## 1.9 Source errata — where Parallax's own document is wrong

A distinct class from "our KB was wrong": the test is *"if Parallax fixed their document tomorrow,
would this entry disappear?"* Ten entries, `E-001`…`E-010`. Four have a YAML consequence in this
release.

| # | The source defect | Reached our KB? | This release |
|---|---|---|---|
| `E-001` | Hardware Manual: `COGATN #00001100` lost its `%` and does not assemble | never carried | — |
| `E-002` | Hardware Manual: `ROLBYTE y,x` — no such two-operand form | never carried | — |
| `E-003` | Hardware Manual Table 10 states the VCO range as 100–350 MHz; its own PLL Example, the Datasheet (twice) and the Silicon Doc all say **100–200 MHz** | follows the majority | ✅ `clock_system.yaml pll_system` now states 100–200 MHz **and names the conflict in-file** (`cross_source_conflict`, `F-330`), with 350 MHz labelled as the `VCO/1` overclock ceiling rather than a recommendation |
| `E-004` | #64013 RTC guide prescribes *"input mode to 150 k-ohm pull-up"* — our own mislabel, in a published Parallax document, **and** in the one configuration where it cannot work | diverged | ✅ `addon-rtc.yaml pin_mode_tip` rebuilt as board-fact + working P2 mechanism (`P_HIGH_150K` with `DIR` HIGH) + an explicit `do_not_copy_the_guides_wording` key quoting the guide and stating both errors. A companion `scl_pull_up_caveat` records that the guide's *"3.3 k-ohm pull-up"* names a rung the P2 ladder does not have at all, and carries a GAP: no ingested source says whether the board provides its own SDA/SCL pull-ups |
| `E-005` | #64000 guide §18 reverses the SPI/SD pin directions | never carried | ✅ reinforced — `boot-rom/_index.yaml`, `boot-pattern-selection.yaml`, both Edge YAMLs now state **P58 = MISO (P2 in), P59 = MOSI (P2 out)** and, critically, that **P60/P61 SWAP between flash and SD** (flash: P61=CSn, P60=CLK; SD: P61=CLK, P60=CSn), citing the ROM booter listing |
| `E-006` | #64006 guide calls a switch "active-high" *and* says the pin is "driven low when asserted", in one sentence | ⚠️ **diverges** | `RESEARCHING`. `addon-control-board.yaml` resolves it opposite to the guide's mechanical description (*"the I/O pin reads high while the button is pressed"*) and now attributes that sentence to the guide. **Unresolved: which half is true decides whether generated code tests for high or low.** A jumper-only bench test would settle it |
| `E-007` | Hardware Manual states *recommended use*, Datasheet states *absolute limits*, for the same clock inputs | follows, **unlabelled** | ⚠️ partially — `clock_system.yaml clock_specifications` now carries the datasheet AC table with `measurement_condition` and the 180 MHz-at-105 °C footnote, but the KB still does not label which framing it is quoting elsewhere |
| `E-008` | #64010 pin table duplicates channel X on offsets 9/8 and omits channel U | never carried | ✅ `addon-motor-driver.yaml` gained a `signal_map.pin_label_errata` key stating the contradiction, that it is in the source PDF's own text layer (not an extraction artifact), and why the p.5 header pinout wins |
| `E-009` | #64000 prints *"3.55″ × 3.55″ (90 x 90 cm)"* — the metric unit is wrong by 10× | never carried | ✅ `p2-eval-board.yaml physical.dimensions_note` quotes the inch figure and names the typo |
| `E-010` | **Both** Edge Module guides say *"have I/O pin pull-ups activated"* | ⚠️ **YES — carried verbatim, both files** | ❌ **not fixed.** §0.3 item 4 |

**🔴 The lack, for the class.** *There was no register for "the source is wrong."* A cross-source
conflict that resolved to *"Parallax's document is the defect"* had nowhere to go: it was not a KB
correction (our KB might be right), and not a knowledge gap (we knew the answer). It ended up in
someone's head or in a closed conversation. `SOURCE-ERRATA.md` was created `39ec6d8d` and rebuilt
`809b347b` this range, with the rule that every entry cites **all sides** in each document's own
navigable terms — so a claim can be confirmed with Parallax by opening the page.

---

## 1.10 ⚖️ Schema reshaping — a judgement, not a correction

**What.** 30 top-level keys changed YAML *type* across 24 files, almost all so a block could carry a
`source:` key beside its content.

| Shape change | Files |
|---|---|
| `list → {source, items}` / `{source, pins}` / `{source, rules}` | `p2an001`, `p2an002`, `p2an004` (`gotchas`) · `addon-av-breakout`, `addon-control-board`, `addon-motor-driver`, `addon-serial-device`, `addon-serial-host` (`signal_map`) · `addon-serial-host`, `edge-32mb-module` (`development_workflow`) · `addon-wx-wifi` (`pin_descriptions`) · `edge-32mb-module` (`limitations`) · `hub75_adapter` (`notes`) · `clock_system` (`configuration_rules`) · `setxfrq` (`common_values`) · `pc_key` (`usage_rules`) · `waitms` (`notes`, `limitations`) · `waitus` (`notes`, `limitations`, `clock_frequency_impact`) |
| `str → dict` on **`description:`** | `addon-hd-audio`, `addon-rtc`, `addon-serial-device`, `hub75_adapter`, `programming-prop-plug` |
| `str → dict` elsewhere | `smart-pin-00011` (`operation`, `pwm_characteristics`) · `addon-rtc` (`pin_mode_tip`) · `streamer_smartpin_control` (`protocol_client_code_note`) |

**Result: the shipped set is now mixed.** `signal_map` is a mapping in 5 hardware files and a list
in 9. `gotchas` is a mapping in 3 application notes and a list in 4. `description` is a mapping in 5
hardware files and a string in 11. **At `v1.17.0` each of these was uniform.**

**🔴 The lack.** *There is no schema for these files and no instrument reads shape.* Both armed
gates read *content* — quantities and constant names. A key can change from a list to a mapping,
in half the files of a region, and nothing anywhere notices. Any consumer that iterates
`signal_map` as a list (or reads `description` as a string) now works on some hardware files and
not others.

**Marked as a judgement** because it was a deliberate authoring choice made to satisfy the citation
rule, not a defect being corrected — and because the alternative (a sibling `signal_map_source:`
key) would have left the shapes uniform. Worth a decision either way; it should not drift further.

---

## 1.11 Citation paths that route every new agent

**What.** `69af3733`, 4 files + `README.md`, +33/−24. Fourteen bare paths in the two getting-started
guides and six more inside the two `basic-io.yaml` files became repo-absolute. Each guide's
`content_base` gained a comment saying it is **not** a resolution base.

**Why it mattered here specifically.** Both guides tell an agent that `concepts/basic-io.yaml` is
**required reading before any I/O work** — which pointed straight at the file that carried the
broken pull-up examples. And the citation was ambiguous: **two real files answer to that name**
(`language/pasm2/concepts/basic-io.yaml` and `language/spin2/concepts/basic-io.yaml`).

**🔴 The lack — and it is a good one.** Each guide declares a `content_base` that would disambiguate,
and then *refutes it three lines earlier*: a sibling entry in the same block cites
`architecture/p2-architecture-mental-model.yaml`, which under `content_base` would name a directory
that does not exist. **One path base-relative, its neighbour root-relative, in one block.** The
citations were right by the luck of the reader's guess.

**And why nothing caught it.** `validate-crossref-keys.py` iterates a **fixed fifteen-name field
list** against the **top level** of each document. The guide citations sit in `knowledge_progression`
and `next_steps` — on neither list — so `exit 0` was never evidence about them at all. The blind
spot is now counted and printed on every run, and the banner no longer overclaims. `F-340` remains
`PARTIAL`: the **scope** half is done, the **traversal** half is owed.

> ⚠️ **The project holds two different measurements of that blind spot and they do not agree.**
> `69af3733`'s message says the validator *"sees 742 reference sites and cannot see 230, so it
> reports on 76%"*, and that **136** of the invisible ones are `related_symbols:`. `F-340`'s
> «#305» disposition, and the live run at HEAD, print *"688 nested reference site(s) were NOT
> checked (82% of 3849 coverage)"* and say the symbols file carries **135** `related_symbols:`
> lists. Both are in the record; nothing reconciles them. The *shape* of the finding is unaffected —
> the field where the two fabricated names lived is the one the instrument does not read, and the
> live run confirms it (`related_symbols: 7 resolved` corpus-wide, all seven from one unrelated
> file) — but do not quote either pair of numbers as settled.

> ⚠️ **Residual, minor.** `4cecb02c` added `see_also` entries as bare
> `deliverables/ai/P2/architecture/pin-drive-configuration.yaml` (no leading slash) in both
> `basic-io.yaml` files, while `69af3733` made the neighbouring paths `/deliverables/…`. Both
> resolve; the file is now internally inconsistent about the form.

---

## 1.12 Worked code that compiled and did not work

**What.** `4cecb02c` did more than its subject line. Nine examples were extracted **from the shipped
YAML bytes**, compiled, and then **read for semantics** — because `F-322`'s examples all compiled
and were all wrong.

| Defect found | File |
|---|---|
| `TESTP pin WC` under a comment asserting the opposite flag polarity — the handler ran on the wrong half of the condition | `smart-pin-00000-normal-mode.yaml`, `language/pasm2/concepts/basic-io.yaml` |
| `JMP #$` self-jump — the LED blinked once and the program hung | `language/pasm2/concepts/basic-io.yaml led_blink` |
| `ORG` immediately followed by data — execution began on a `LONG` | `smart-pin-00000-normal-mode.yaml pasm2_complete` |
| a `setup_pins` routine nothing called | `smart-pin-00000-normal-mode.yaml` |
| a glitch rule that contradicted both of its own examples (*"Set DIR before OUT"* with a `wrong:` block that sets OUT first) | both `basic-io.yaml` files `safe_initialization_patterns` |
| `RDPIN` used to read a **non-smart** pin, then `WRLONG …, PTRA` to "write to SPIN2 variable" inside inline PASM | both JonnyMac convention files |
| `WAITMS #500` in a **PASM2-only** program — `WAITMS` is a Spin2 method, not a PASM2 instruction | `guides/pasm2-getting-started.yaml minimal_program` (replaced; the returned block adds a `why_waitx_not_waitms` key) |

**🔴 The lack.** *Nothing extracts, compiles, or reads the code embedded in YAML string blocks.*
`pnut-ts` proves legality and is not run against these at all; the sourcing gate strips code regions
by design; the fidelity gate reads constant names. A worked example is the highest-leverage content
in the set — it is copied verbatim — and it is the least instrumented. Filed as `F-345` and `F-346`,
both `PENDING-VALIDATION`.

---

## 1.13 Two register corrections REJECTED — and why that is the valuable half

`9370c580` dispositioned nine findings and **refused** three `F-203` sub-claims, two of which would
have introduced defects into content that is currently correct.

- **The PLOT `TEXTSTYLE` vertical-align "swap" is not a swap.** The Pascal-derived directive matrix
  warns that anchor-edge and ink-side vocabularies describe the same pixels, and that this exact
  ambiguity already caused the row to be documented backwards once. `plot.yaml` uses ink-side
  consistently and says so. Applying the "correction" would have inverted a correct page.
- **`weight: 100` is "thin", not "light".** The Pascal source declares `weight[0..3] = (100,400,700,900)`;
  100 is OpenType **Thin**. Light is 300.
- **`F-218` rested on P2KB itself** — circular inside this project — so it was re-grounded on the
  Silicon Doc primary extraction, which confirms the KB was **already correct**. Nothing owed.

**No YAML change from any of the three.** Recorded here because a ledger that only lists edits
teaches that every finding is an edit.

---

## 1.14 Instruments armed as blocking release gates

`43b0ede2`. No YAML content class of its own beyond the 20 re-tiered blocks (§1.7), but it changes
what "green" means for this release.

- Both audits now run inside `validate-dod-release.py` and `release-yamls`, each executing its
  **negative control before its audit** — a planted uncited block turns the release path red and
  names file, line, block and units; removing it returns green with the file byte-identical. **Exit
  2 fails too**: nothing-audited is never a pass.
- **No baseline, no tolerance, no ratchet** — the purge removed the population first precisely so
  there is nothing to grandfather.
- The truth side now globs `.txt` as well as `.md` and parses pipe rows **by cell**, so the current
  v55 symbol table (tab-indented, value in column one) is finally on it: **116 constants where there
  were none**, with edition precedence so a superseded extract cannot outrank the current one.
- Five citation/quantity misfires fixed together because they interact: part numbers stopped being
  read as amperes (`F-351` — 12 blocks were pure instrument artifacts, including an ISO designator
  and Unicode code points); escaped example code became visible; a slug and a **deferral** stopped
  counting as citations (that is the `150mA` mechanism, §1.6); and a documentation key started
  counting as one — which **re-tiered 20 blocks into Tier 1**. Those 20 were drained source-first:
  **17 gained verified citations, 3 inferences were removed.**
- **A latent defect went active under the repaired parser and was caught by its own control**: with
  pipe rows read by cell, one of our own analysis documents began defining a smart-pin constant as a
  pin number. Loose files at a truth root are now excluded structurally. *The six misfiled documents
  themselves (`F-341`) are still owed.*
- Every run now prints what a green exit does **not** certify.

---

# PART 2 — By region → file

Per file: what a consumer would notice first · Added / Removed / Corrected with reasons · net
`+/−` for the range · which commits touched it. **⚖️** marks a judgement rather than a correction.

The `+/−` figures here are the **net range diff** (`v1.17.0..HEAD`) — what ships. They differ
slightly from the per-commit sums in the working matrix (e.g. `p2an001` is +15/−15 net against
+16/−16 summed), because a line touched in two commits is counted twice by a sum.

Genuinely one-line entries, called out so they read as deliberate: `code-examples/smart-pins-002`,
`language/spin2/methods/cogstop.yaml`. Everything else is substantive.

---

## Region: `application-notes/` — 4 files

### `p2an001-single-pin-instrumentation-adc.yaml` · +15/−15 · `15c84de5`, `597dba`
**A consumer would notice:** the ADC accuracy figure changed meaning, and two pitfalls are gone.
- ⚖️ **Reshaped** `gotchas` from a list to `{source, items}`. §1.10.
- **Corrected — the headline number.** *"pins read as much as 15 mV apart … a DESIGNER-STATED
  figure"* is replaced by the **hardware-verified** floor: *"ratiometric single-pin absolute error
  was ≤ 9 mV, reproducible, with a small positive offset at low V and ~0 at mid/high"* (2026-07-07,
  real P2). The 15 mV figure survives as an explicit caution — *"the bench has NOT yet reproduced
  [it] … Do not quote 15 mV as a specification."* The multi-pin extension that would settle it is
  open.
- **Corrected.** *"builds run at 200 MHz; P2 spec max is 300 MHz"* → the datasheet AC row
  (min 3.33 / typ 180 / max 320 MHz) with the 105 °C footnote.
- **Removed, not replaced (2).** *"High-impedance sources load the pin (input resistance ~500 kOhm)
  and read low — buffer, or account for the divider (Recipe 4)"* and *"The DAC loopback is a
  FUNCTIONAL check, not an accuracy benchmark."* 7 items → 6, plus one new hardware item on mode
  selection. **Reason: no source states the 500 kΩ input resistance.** *No `gap` key records
  either loss in-file.*
- **Added.** A `source:` naming the datasheet feature list, AC characteristics, the Silicon Doc
  ADC sections and the empirical ledger; and the SINC2/SINC3 accumulator bounds
  (512 clocks SINC3, 11,585 SINC2) quoted verbatim.

### `p2an002-cordic-for-real-work.yaml` · +14/−12 · `15c84de5`, `597dba`
**A consumer would notice:** the CORDIC precision figure is gone, and the pipeline pitfall is now
scoped.
- ⚖️ Reshaped `gotchas`.
- **Removed.** *"Precision ~28 bits for trig, exact for integer ops."* Replaced by the Silicon
  Doc's own words — *"32-bit, pipelined CORDIC solver with scale-factor correction"* — with the
  practical consequence retained (*a predicted (0,100) may read (0,99)*). **Reason: 28 bits is not
  stated by any source.**
- **Corrected — scope, not fact.** The hub-access pitfall now names `EF-053`, its date, its rig, its
  seven runs, and — from the finding itself — *"this measures WHERE results are lost, not why; state
  it as the tested shape … not as a law about any hub access."* The previous wording generalised.
- **Corrected.** *"keep issued-minus-retired within what the pipeline holds"* → the documented
  event: *"GETQX/GETQY executed without any CORDIC results available or in progress"* (event 15).
- **Added.** The 55-clock latency and 1/2/4/8/16-clock issue cadence quoted verbatim.

### `p2an003-dac-analog-signal-generation.yaml` · +17/−13 · `15c84de5`, `597dba`
**A consumer would notice: two formulas an agent emits are gone from the block, replaced by a note
saying they are not source statements.**
- 🔴 **Removed — `voltage_math` and `dds_phase_increment`.** `V = (code / 65536) * Vfs; $8000 → 1.65 V`
  and `inc = f * 2^32 / sample_rate`. A new `formulas_note` says they *"are the arithmetic of a
  16-bit code and a 32-bit phase accumulator, not statements taken from a Parallax source. They are
  kept out of this block."* **The promotion filter ruled `key_parameters` ACTIONABLE naming exactly
  these two** (*"the V = code/65536 * Vfs math … and the DDS phase-increment formula"*). This is the
  one place the repopulation applied a stricter rule than the disposition it was executing.
  ⚖️ **A judgement, and the one I would ask about second** (after §0.3 item 1).
- **Corrected.** The `sample_clock` entry no longer states `200 MHz / 256 clocks = 781_250 samples/s`
  — the source states the mechanism (Y captured, IN raised) but not that rate.
- **Added.** Verbatim source statements for both dither modes, `low_level_pin_requirement`
  (`M[12:10] = %101`), and the 11,585-clock SINC2 filtering bound.
- **Note.** `gotchas` here is still a **list** — the only one of the three reshaped app-notes that
  was not converted. §1.10.

### `p2an004-frequency-rotation-rc-timing-measurement.yaml` · +14/−14 · `15c84de5`, `597dba`
**A consumer would notice:** the TSL235R sensor guidance is gone, deliberately.
- ⚖️ Reshaped `gotchas`.
- **Removed, with a reason in-file.** The TSL235R supply range, dark-output and decoupling advice,
  replaced by a `gap` flag: *"Sensor-specific electrical figures … belong to the sensor's own
  datasheet, which is not in this project's ingestion tree."* This is the right shape — the loss is
  visible where the reader meets it.
- **Removed, no reason given (2).** The R2 reciprocal-vs-fixed-gate tip and the R3 Tier-0
  verification recipe (*"jumper 40→32 and 41→33 … the reads are the known answers 5 then 3"*). 7 → 6.
  The R3 recipe is still described in `hardware_status`, so it is not wholly lost.
- **Corrected.** `P_LOW_FLOAT` is now explained as *a rung of the eight-rung ladder* rather than as
  a special mode — the drive-strength class reaching an application note.
- 🟠 **Carries the EF-063/EF-064 mis-attribution** (§0.3 item 5).

---

## Region: `architecture/boot-rom/` — 3 files

All three are pure purge-and-return, and all three came back **materially better than they went**.

### `_index.yaml` · +18/−15 · `15c84de5`, `597dba`
**A consumer would notice: the boot pin roles are now correct per boot source.**
- **Corrected — the important one.** `boot_paths_summary` previously gave one pin map for SPI flash
  (`P61 CS, P60 CK`) and *"routed via the SD card interface"* for SD. It now states both, and that
  **P60/P61 swap**: flash `P61=CSn, P60=CLK`; SD `P61=CLK, P60=CSn`. Plus `P59 (out) = DI (MOSI)`,
  `P58 (in) = DO (MISO)` named *from the flash chip's side* so the direction cannot be misread.
  This is `E-005`'s companion trap.
- **Corrected.** `boot_timing` now quotes the manual (3 ms delay, fast clock, bootloader within
  2 ms) and adds the datasheet's *"Within 5 ms"* and the manual's *"serial loader becomes active
  within 15 ms of reset being released"* — a bound the file did not carry.
- **Corrected.** `canonical_entry` paths were relative (`../serial_loader.yaml`,
  `spi-flash-boot.yaml`); now repo-relative.
- **Added.** `pattern_notation` (float / up / down / any), `p60_pullup_note` (*"built into the
  microSD card"*).
- **Removed.** `timeout_options` and `fallback` as separate keys — folded into the `triggered_when`
  prose, which now quotes the pattern table verbatim.

### `boot-pattern-selection.yaml` · +15/−17 · `15c84de5`, `597dba`
**A consumer would notice: the boot-time clock story gained two facts it did not have.**
- **Added.** `the_one_boot_time_clock_change` — the serial loader's `Prop_Clk` command, with the
  ROM's own two-step switch (`HUBSET` partial, `WAITX ##rc_max/200`, `HUBSET` full) cited to
  `ROM_Booter.lst:578-587`; and `shutdown_clock` (`HUBSET #1`, 20 kHz, before `COGSTOP` floats the
  pins).
- **Added.** `rom_own_calibration` — the ROM sizes timeouts against the RCFAST **maximum**
  (`rc_max = 30_000_000`), not a nominal value.
- **Corrected.** `pin_triple_duty.roles` now names role 2 per boot source with the P60/P61 swap,
  and quotes the manual's own P58–P63 sentence rather than paraphrasing.
- **Corrected.** `custom_board_implication` no longer asserts *"no conflict because the boot pattern
  is sampled before the flash interface activates"* — a mechanism claim no source states.

### `spi-flash-boot.yaml` · +5/−2 · `15c84de5`, `597dba`
- **Corrected.** `boot_pattern_trigger.flash_priority_patterns` restructured from paraphrase to
  `{pattern, procedure}` pairs quoting the Boot Pattern table verbatim, with a `source:`.
- Smallest boot-rom change; nothing removed on net.

---

## Region: `architecture/` (8 files)

### 🔴 `pin-drive-configuration.yaml` · **NEW**, +275 · `cd860ba7`, `e92aa02f`
**A consumer would notice: this is the file everything else now points at — and it has a parse
defect (§0.3 item 1).**
- **Added.** `field_position` (`%M..M` = D[20:8], 13 bits) · `sub_fields` stating how the datasheet
  actually expresses the field (four families of `M[12:0]` bit patterns, not one fixed split) ·
  `drive_ladder` — the eight rungs **as an encoding table** (`%000`→Fast … `%111`→Float) with the
  `P_HIGH_*`/`P_LOW_*` name per rung and a `no_other_rungs` guard · `dir_and_out_rule` ·
  `idioms.weak_high` / `weak_low` as complete routines · `not_documented_here` (open drain, open
  source, keeper/bus-hold, the `P_HIGH_15K | P_LOW_FLOAT` variant, per-pin current beyond the eight
  rungs) · a top-level `aliases:` block including "pull-up" and "pull-down" so the term an agent
  searches for lands here.
- ⚖️ **Deliberately not a definition home.** A constant name appears only as a *value* or in prose,
  never as a defining key — so the fidelity tool cannot read this file as a second home for sixteen
  constants inside the task chartered to end that defect. Verified against the tool's own regexes.
- **Corrected by `e92aa02f`.** `idioms.source` no longer presents EF-063/EF-064 as the authority:
  the authority is documentary (Datasheet Pin Mode Legend + v55 wording) and the empirical findings
  *corroborate incidentally, as rig apparatus*. A `gap_no_dedicated_bench_test` names the missing
  measurement and how to run it. `not_documented_here` was promoted from nested-under-`idioms` to
  top level.
- 🔴 **And that same edit introduced the duplicate `note:` key.** §0.3 item 1.

### `clock_system.yaml` · +185/−136 · `15c84de5`, `597dba`
**A consumer would notice: the PLL lock wait changed by three orders of magnitude, in two places
that ship as code.**
- 🔴 **Corrected — `stabilization_timing`.** `pll_lock: "~10 microseconds"` → *"Allow 10ms for
  crystal+PLL to stabilize"* and *"Allow 5ms for crystal"*, with a `conflict_resolved` key. `F-349`.
- 🔴 **Corrected — two `programming_examples`.** `WAITX ##20_000_000/10000  ' Wait 100µs for PLL lock`
  → `WAITX ##20_000_000/100  ' Wait ~10ms`. **Found by working the file, not by the finding's own
  list** — the sourcing gate strips code regions.
- **Rebuilt — `pll_system`.** Was a `constraints` summary (`vco_range: "99 MHz to 201 MHz"`,
  `output_frequency.max_overclock: "350 MHz"`). Now the datasheet's own bit fields: `%E`, `%DDDDDD`,
  `%MMMMMMMMMM`, the full 16-row `%PPPP` post-divider map, and the two equations. **`vco_range` is
  now 100–200 MHz** with `cross_source_conflict` naming `F-330` / `E-003` in-file, and 350 MHz
  labelled as the `VCO/1` overclock ceiling.
- **Rebuilt — `configuration_rules`.** Was six prose bullets. Now the **closed set of nine legal CON
  combinations** with the `%CC_SS` value each selects, plus the cap-selection rule
  (`_xtlfreq ≥ 16 MHz → 15 pF`).
- **Rebuilt — `hubset_configuration`.** Adds the `safe_switching_warning` (*switching away from
  `%SS = %11` can hang the clock circuit; go via `HUBSET #$F0`/`#$F1` first*), the deglitching
  description, and the datasheet's worked 148.5 MHz sequence.
- **Rebuilt — `clock_specifications`.** Was `recommended: 180 MHz / typical_overclock: 250 MHz /
  absolute_max: "350 MHz (may be unstable)"` plus frequency-vs-voltage and temperature prose. Now
  the datasheet Oscillator Frequency table (RCSLOW 12/20/30 kHz, RCFAST 20/24/30 MHz, XI DC–200 MHz,
  crystal 1–50 MHz, PLL 3.33/180/320 MHz) with `measurement_condition` and pin capacitances.
- ⚖️ **De-duplicated.** `configuration_constants` became a pointer to
  `language/spin2/constants/special-configuration-symbols.yaml` (the definition home) plus the v55
  symbol list and the compiler-defined `clkfreq_`/`clkmode_`.
- **Removed, with the reason stated in-file.** Two `anti_patterns` — a hardcoded-`WAITX` pattern and
  a use-`CLKFREQ`-before-init pattern — *"are authored advice that no ingested source states, and
  are not restored."* Three source-stated anti-patterns replace them, including the new
  `unsafe_switch_away_from_pll`.

### `io_pin_timing.yaml` · +18/−256 · `15c84de5`, `597dba`
**A consumer would notice: this file went 433 → 195 lines, and now says what it deliberately does
not carry.**
- 🔴 **Removed — the `F-327` fabrication family, 9 blocks, never to return.** `timing_specifications`
  (propagation/rise/fall tables keyed to a 1.5–150 mA ladder that does not exist),
  `drive_strength_configurations`, `slew_rate_control`, `clock_relationships` (5–8 / 7–10 / 6–9 ns
  path totals), `input_characteristics` (VIL 0.8 / VIH 2.0 / Schmitt 1.65/1.35/300 mV),
  `special_timing_modes` (~100 MHz sync-serial, ~10 Mbps UART, ~50 MHz DDR),
  `protocol_timing_examples` (generic SPI/I²C/SD lore), `compensation_techniques` (150 ps/inch FR4,
  0.3 %/10 °C, 2 %/100 mV), `best_practices` (generic PCB layout — not-actionable, and with no
  ingestion home either).
- **Returned corrected — `description`.** Rewritten to state **what this file carries and what it
  deliberately does not**, naming where each displaced fact lives: drive strength →
  `pin-drive-configuration.yaml`; slew rate → *"There is none to document. `slew` returns zero hits
  across every ingested Parallax source"*; propagation/rise/fall → *"No Parallax source states
  them."*
- **Kept, and it is the point of the file.** `instruction_to_pin_timing` (the clock-cycle latency an
  agent can act on), `absolute_maximum_ratings` (±30 mA per pin, ±10 mA protection diode) and
  `input_voltage_and_protection` (the ≥1 kΩ series-resistor recipe for a 5 V signal) all survive
  cited.
- **Corrected.** `extraction_metadata` no longer cites *"P2 Datasheet pages 42-45, 76-78"* — pages
  that carry none of this. 🔴 **`F-359` (filed 2026-08-25, not by me) establishes what that citation
  actually was:** pages 42–45 are the PASM2 instruction listing and **the datasheet is 50 pages**,
  so 76–78 do not exist; the file header's `Silicon Doc Reference: part3-pins.txt` names a file that
  **has never existed**; and the header itself is what satisfied the sourcing gate's citation regex.
  The header line was removed here — but the same header shape stands in six sibling
  `architecture/` files that this release does not touch. §0.3 item 12.

### `pin-power-domains.yaml` · +35/−19 · `15c84de5`, `597dba`
**A consumer would notice: the board-layer numbers came back, richer.**
- **Returned cited — `board_power_grouping`.** Now carries the full `V00`→P0-P7 … `V56`→P56-P63 map,
  the naming rule (*"the two digits after the V refer to the first of 8 I/O pins"*), the per-pin
  30 mA / per-group 300 mA pair with the datasheet's absolute-maximum line beside it, and a
  `budget_rule` the file did not have: **eight pins at 30 mA is 240 mA inside a 300 mA LDO, but the
  edge-connector `Vxx` pin draws from the same 300 mA**.
- **Rewritten — `description`.** The silicon-4 / board-8 distinction is now stated in the Edge
  guide's own words, with the consequence spelled out: the ADC references its **silicon** group, so
  a shared-node absolute measurement must stay within four pins even though the board wires eight to
  one LDO. Plus the guide's own caveat that the distributed scheme *"is not a requirement of the P2
  microprocessor; rather a design choice for this particular module."*

### `serial_loader.yaml` · +14/−15 · `15c84de5`, `597dba`
- **Corrected.** `serial_triggered_when` was a paraphrase of the pattern ladder; now four verbatim
  rows from the Boot Pattern table, including the 60 s fallback case.
- **Corrected.** `serial_pins` now states *which end* each pin is named from and adds the open-drain
  behaviour of P62 during multiprogramming.
- **Added.** `line_format` — 8N1, 9,600 to 2,000,000 baud, **signal inverted** (start bit low, data
  bits high for 0). The file did not carry the inversion.
- **Corrected.** `execution.target` quotes the booter's actual behaviour (`COGINIT #0,#0` on valid
  checksum; wait for another command when invalid) with the ROM listing line as confirmation.
- **Removed.** `timing.activity_timeout: "None after first command"` — unsourced.

### `smart_pins.yaml` · +63/−21 · `15c84de5`, `cd860ba7`, `597dba`
**A consumer would notice: the `%AAAA`/`%BBBB`/`%FFF` selectors are now fully enumerated.**
- **Rebuilt — `input_routing`.** Was *"4-bit field selects source"* plus a four-line filter list.
  Now the complete 8-value A-selector encoding (`x000` this pin … `x111` relative −1) with the
  polarity bit, the B selector, the full `%FFF` table (`000` A,B … `111` filt3), and a
  `global_digital_filters` block: what the four filters are, the four `HUBSET` forms that configure
  them, the length/tap encodings, and the reset defaults with the source's own 6.25 ns/clock
  arithmetic shown. **The four filter times (12.5 ns / 600 ns / 16.4 ms / 210 ms) are unchanged** —
  verified against the Silicon Doc on return.
- **Returned cited — `electrical_limits`.** Was a bare pointer; now carries the VIO supply range
  (3.15/3.3/3.45 V), the pin-voltage limit, the ±10 mA diode limit and ±30 mA per pin, and states
  *"The P2 is a 3.3 V I/O device and is NOT natively 5 V-tolerant"* as a safety line rather than a
  cross-reference.
- **Added.** `configuration_format.fields.m.sub_fields_reference` → `pin-drive-configuration.yaml`;
  a top-level `related:` block (the only *added* top-level key in the region).
- **Returned — `related_components`.** Restored as apparatus, with the GETCT ceiling delegated to
  `timing_operations.yaml method_selection` rather than restated.

### `smart_pin_patterns.yaml` · +5/−7 · `15c84de5`, `597dba`
**A consumer would notice: `notes` went from 7 bullets to 4, and two of the losses are practical.**
- **Returned cited (2).** The 33-bit outgoing bus / `RDPIN`/`RQPIN` multiplexing statement, and
  long-repository mode as the cog-to-cog mailbox — both quoted from the Silicon Doc.
- **Removed, not replaced (4).** *"Smart pins offload timing-critical operations from COGs"*,
  *"Each pin operates independently once configured"*, *"Calibration essential for accurate ADC
  readings"*, **"PWM dead-time critical for motor control safety"**. The last is the one worth
  noting: the concrete figure survives in `hardware/addon-motor-driver.yaml pwm_control.minimum_deadtime`
  (250 ns, with the reason), but the *general* safety rule no longer appears on the smart-pin
  patterns page where a PWM author would meet it.
- **Corrected.** The GETCT/GETMS steering no longer states *"overflow past ~10 s at 200 MHz"* inline;
  it names the mechanism (`2^31 / CLKFREQ`) and points at the one table that carries the
  per-frequency figures. **Verified: `timing_operations.yaml method_selection` does carry them**
  (~10.7 s / ~8.6 s / ~6.7 s).

### `click_module_integration.yaml` · **+0/−25** · `15c84de5`
**A consumer would notice: pure loss.**
- 🔴 **Removed and never returned — `best_practices`.** Ruled **ACTIONABLE** by the promotion filter
  (*"'Always use offset constants, never hardcode pins' and 'make base pin a runtime parameter' are
  the emitted code's shape"*), then found to have no ingested source anywhere. Recorded as a gap in
  `F-352`. §1.3(c).
- 🟡 **Not swept.** This file still carries `' Initialize I2C driver (with pull-ups)` /
  `i2c.setup(sclPin, sdaPin, I2C_SPEED, I2C_PULLUP)` and *"Interrupt pins may need pull-ups"* — the
  same driver-library-setting-vs-P2-capability ambiguity that `addon-rtc.yaml` was explicitly
  relabelled to remove. The `4cecb02c` sweep did not reach `architecture/`.

---

## Region: `architecture/smart-pins/` — 4 files

### `smart-pin-00000-normal-mode.yaml` · +18/−11 · `4cecb02c`
**A consumer would notice: both complete examples were wrong and now are not.**
- **Corrected — Spin2.** `WRPIN(…P_HIGH_15K)` + `PINFLOAT(BUTTON_PIN)  ' Input mode` →
  `PINHIGH(BUTTON_PIN)  ' DIR=1, OUT=1 — a drive is live only while DIR is high`. As written, the
  original configured a weak drive and then turned it off.
- **Corrected — PASM2, three separate defects.** `ORG` was immediately followed by `led_pin LONG 56`
  (execution began on a data long); `setup_pins` was defined and never called; `DIRL pin ' Input
  mode` disabled the drive. The block now has an entry point (`CALL #setup_pins` / `JMP #main_loop`),
  `DRVH` instead of `DIRL`, and the `LONG`s moved below the code.
- **Corrected.** `TESTP pin WC  ' Read pin to C` → `' C = pin state` (the old comment invited the
  polarity error `F-345` records elsewhere).
- **Added.** `related:` converted from a one-element inline list to a block list with the two new
  definition homes.

### `smart-pin-00011-dac-16bit-pwm-dither.yaml` · +17/−15 · `15c84de5`, `597dba`
- ⚖️ Reshaped `operation` and `pwm_characteristics` from prose blocks to `{source, …}` mappings.
- **Returned cited.** `operation` now quotes the Silicon Doc directly on the 256-multiple sample
  period, the Y[15:0] capture, the IN-raised-on-completion coordination rule, and the
  *"maximum of only two transitions … Fclock/256 … at −48dB"* trade-off.
- **Returned cited.** `pin_behavior` — the reset state and the ADC-on-`OUT`-high load-measurement
  path (*"RDPIN/RQPIN can be used to retrieve the 16-bit ADC accumulation"*), which the old
  four-word entry did not convey.
- **Added.** `low_level_pin_requirement: M[12:10] = %101`, stated twice (in `operation` and
  `pin_behavior`) because it is the step that is silently omitted.
- **Note.** `pwm_advantages` still restates *"Only 2 transitions per 256 clocks"* alongside the new
  `pwm_characteristics.transition_bound`. Harmless duplication, but it is the shape that drifts.

### `smart-pin-11000-adc-internal-clock.yaml` · +9/−4 · `9370c580`
**A consumer would notice: three ADC "input modes" are not input modes.**
- 🔴 **Corrected.** `P_ADC_GIO`/`P_ADC_VIO`/`P_ADC_FLOAT` were listed as *"Ground-referenced input"*,
  *"VIO-referenced input"*, *"Floating input"* — reading as gain/range selections alongside
  1x…100x. They are **calibration sources**, not input ranges: GIO/VIO substitute an internal
  reference for the pin. `P_ADC_FLOAT` floats the ADC input to find its bias point (Rev C silicon).
- 🔴 **Added — the fact that changes a circuit.** *"The gain-mode window is CENTERED ON MID-SUPPLY
  (~VIO/2), not referenced up from 0V. Measured on real P2 silicon: centered at ~1.64V for every
  gain (EF-024). A ground-referenced small-signal source needs a mid-rail bias network before it can
  be read through a gain mode."* This is `F-202`, and it is the correction most likely to change a
  reader's schematic.
- **Corrected.** *"ADC input modes (GIO/VIO/gain) affect voltage range and sensitivity"* — false for
  GIO/VIO — split into two accurate statements.

### `smart-pin-11011-usb-host-device.yaml` · +13/−11 · `15c84de5`, `597dba`
**A consumer would notice: the USB mode is now documented well enough to implement.**
- **Rebuilt — `detailed_description`.** Was two prose paragraphs (`operation` + `timing`). Now:
  `pin_pairing` (even/odd, LSB-only difference, with examples) · `which_pin_is_which` (upper/odd =
  DP, IN on output-buffer-empty, no WXPIN/WYPIN; lower/even = DM, IN on receiver status change,
  `RDPIN` for the 16-bit status word, `WXPIN` sets the baud NCO) · `configuration` (`%1_11011_0` vs
  `%0_11011_0` for a sniffer; the `D[15]` host/device and `D[14]` speed bits; the *"baud must be
  < ¼ system clock"* constraint) · a worked `WXPIN ##$E666` example · `start_sequence` ·
  `state_machines` (*"the receiver receives … all local output, as well"*).
- **Removed.** The `timing` key. Its content (*"USB 1.1 Full Speed (12 Mbps) and Low Speed
  (1.5 Mbps)"*) survives in `registers.D_14` and in `advantages`, so nothing is lost.
- 🟡 **One thing to read with the drive-strength class in mind.** The returned `fpga_note` quotes the
  Silicon Doc verbatim: *"In Propeller 2 emulation on an FPGA, there are no built-in 1.5k and 15k
  **resistors**, like the ASIC smart pins have."* That is the source's own word for the drive
  ladder, and it sits in a release whose headline is *"the P2 has no pull-up resistors."* Faithful
  quotation, but a reader could take it as a contradiction. **Worth a decision: annotate, or leave
  the source's wording alone.**

---

## Region: `guides/` — 2 files

### `guides/pasm2-getting-started.yaml` · +58/−67 · `15c84de5`, `4cecb02c`, `597dba`, `69af3733`
**A consumer would notice: the minimal program example is a different program, `_clkfreq` is no
longer required, and `FIT $1F0` is now `FIT $1F8`.**
- **Returned, rebuilt — `file_structure`.** The promotion filter ranked this #4 of the highest-value
  returns. What came back is **source-first, and smaller**:
  - **Corrected.** `FIT $1F0` / "496 longs" → `FIT $1F8`, with `why_1F8` explaining that
    `$1F8`–`$1FF` are the mapped special-purpose registers and `$1F0`–`$1F7` are dual-use. Carries
    its own `correction_2026_08_25` key: *"Not restored."*
  - **Corrected.** The `CON` block's `_clkfreq` is **no longer stated as required** — v55: with no
    clock-setup symbol and not in DEBUG mode, the compiler selects RCFAST. A `clock_setup` block
    adds the auto-prepended 16-long clock-setter and `_AUTOCLK = 0` to inhibit it.
  - **Corrected — a non-compiling line.** The old `minimal_program` used `WAITMS #500` in a
    PASM2-only program. `WAITMS` is a Spin2 *method*. The new block replaces it with the Parallax
    v55 example (`DRVRND`/`WAITX ##clkfreq_/10`) and adds `why_waitx_not_waitms`.
  - ⚖️ **And it dropped the CON block.** The old example showed `CON` with `_clkfreq` and `LED_PIN`,
    a labelled entry point, a `.loop`, and `FIT`. The new one is four DAT lines. An agent copying
    from this file no longer sees a worked pin-assignment CON. **Defensible (source-first) and a
    real reduction; flagging it rather than arguing it.**
  - **Added.** The full `ORG`/`ORGH` variant tables with cog/LUT limits, `$`-stepping (1 per
    cog-exec instruction, 4 per hub-exec), `ORGF` and `RES`.
- **Corrected — routing.** *"covers … drive strength, pull resistors"* → *"…and drive strength"*
  (`4cecb02c`).
- **Corrected — citations (`69af3733`).** 8 bare paths made repo-absolute, including the two
  `next_steps` entries and the `rdlong.yaml`/`wrlong.yaml` timing references; `content_base` gained
  its "not a resolution base" comment. §1.11.

### `guides/spin2-getting-started.yaml` · +12/−8 · `4cecb02c`, `69af3733`
- **Corrected — routing.** Same "pull resistors" removal.
- **Corrected — citations.** Six citation lines (seven paths) made repo-absolute, including
  `spin2-formatting-standards.yaml` and both documentation-style files; `content_base` comment
  added.
- Nothing removed. Smallest guide change.

---

## Region: `code-examples/` — 1 file

### `smart-pins-002-button-reading.yaml` · +1/−1 · `4cecb02c`
**Genuinely one line.** `hardware_requirements`: *"Pull-up or pull-down resistor as needed"* →
*"**External** pull-up or pull-down resistor as needed"*. One word, and it is the difference between
naming a board component and naming a chip feature the P2 does not have.

---

## Region: `language/pasm2/` — 4 files

### `concepts/basic-io.yaml` · +91/−121 · `15c84de5`, `4cecb02c`, `1f37ae58`, `597dba`, `69af3733`
**Five commits — the most-touched file in the release.** A consumer would notice: the pull-resistor
mechanism is gone, the 150 mA figure is gone, and both worked examples run.
- 🔴 **Removed — `hardware_specifications`** (`1f37ae58`). `max_current_per_pin: "150mA"` — **five
  times** the datasheet's ±30 mA absolute maximum, in the exact number used to size an LED series
  resistor — plus the four TTL logic-level pairs. **The lack: the citation test matched the bare
  word "datasheet" inside `max_current_total: "Check datasheet for package limits"` — a deferral,
  not an attribution — so the block read as cited through two purges.** `F-348`. The correct facts
  ship, cited, in `io_pin_timing.yaml absolute_maximum_ratings`. Verified as a pure deletion:
  `git diff --numstat` reports 0 insertions, and `validate-crossref-keys.py` re-ran clean.
- 🔴 **Removed, never to return (2).** `drive_strength_configuration` (the `F-327` ladder verbatim,
  with `bits_M_6_0: "Control drive strength"` — wrong at both ends) and `timing_considerations`
  (`pin_propagation: "3-7ns"`; its correct 2-clock instruction figure is already carried, cited, in
  `cog.yaml` and `pasm2-getting-started.yaml`).
- **Returned corrected — `internal_pull_resistors`.** The constants are real, the old mechanism was
  not. Now: `there_is_no_bias_resistor_selector` · `the_dir_rule` · `substitute_for_a_pull_up` /
  `_pull_down` as complete `WRPIN`+`DRVH`/`DRVL`+`TESTP` sequences · a `corrected_2026_08_25` key
  quoting the pre-purge `DIRL #16 ' Use as input with pull-up` and saying why it is wrong. **The
  block name was kept on purpose** — it is the term a reader searches for.
- **Returned cited — `control_registers`** and **`pin_architecture`**. Registers now carry addresses
  and the `$1F8`–`$1FF` mapping note plus the `$1FE`/`$1FF` debug-interrupt overlap. `pin_architecture`
  drops `drive_strength: "1.5mA to 150mA"` and `pull_resistors:`, gains the datasheet's verbatim
  drive-mode list and a `no_milliamp_ladder` guard.
- **Corrected — the glitch rule** (`4cecb02c`). *"Set DIR before OUT to prevent output glitches"*
  contradicted its own `wrong:`/`correct:` examples (both of which set OUT first). Now *"Set OUT to
  the desired state while the pin is still floating, then raise DIR."*
- **Corrected — both examples.** `led_blink` had `JMP #$` (blinks once, hangs) → `JMP #blink`, and
  gained the `CON`/`DAT` frame. `button_read` had `DIRL` twice with `' Input with pull-up`, `TESTP …
  WZ` with an inverted comment, and called an undefined `button_action` → rewritten with `DRVH`,
  `WC`, a `poll` loop and a defined `button_action`. `F-345`, `F-346`.
- **Corrected — citations** (`69af3733`). 3 paths absolutised. 🟡 The two `see_also` entries added by
  `4cecb02c` are still bare `deliverables/ai/P2/…` without the leading slash. §1.11.
- 🟠 **Carries the EF-063/EF-064 mis-attribution** (§0.3 item 5).

### `concepts/streamer_smartpin_control.yaml` · +6/−8 · `15c84de5`, `597dba`
- ⚖️ Reshaped `protocol_client_code_note` from a prose block to `{source, scope, which_timebase, full_rule}`.
- **Corrected.** *"GETCT-based deadlines silently overflow past ~10 s at 200 MHz"* → the v55
  definitions quoted (`GETCT` = 32-bit counter; `GETMS` = *"uses 64-bit system counter and CLKFREQ,
  rolls over every 49.7 days"*) with the consequence stated as a bound rather than a single number.
- Moved from the bottom of the file (after `related:`) to a proper position before it.

### `setxfrq.yaml` · +22/−12 · `15c84de5`, `597dba`
**A consumer would notice: the four precomputed values are unchanged and now show their work.**
- ⚖️ Reshaped `common_values` from a list to `{source, computation, cross_checked_against, values, cog_start_default}`.
- **Added — the derivation.** `D = round(target * $8000_0000 / clkfreq)` with the source's own
  round-up footnote, and a per-value `arithmetic:` string. *"Every value below was recomputed at
  restore and each matches to the LSB."*
- **Added.** `cross_checked_against: architecture/streamer/nco-timing.yaml video_rates` — both carry
  `$0CE3_BCD3` for the 25.175 MHz VGA clock at 250 MHz, and they agree. The promotion filter asked
  for exactly this check.
- **Added.** `cog_start_default: "$8000_0000"` — the 1:1 multiplier, which the file did not state.

### `wrpin.yaml` · +13/−6 · `cd860ba7`
**A consumer would notice: the six D-operand field descriptions are now a pointer.**
- ⚖️ **Removed by pointer, not corrected in place.** All six one-line field descriptions replaced by
  a `reference:` to `smart_pins.yaml configuration_format.fields`, an `m_sub_fields:` pointer to
  `pin-drive-configuration.yaml`, and an `input_selectors:` self-reference. **Reason, stated in the
  file: three of the six had drifted wrong (`F-331`), and `F-321`/`F-323` exist precisely because
  one fact was written twice and the copies drifted.**
- **Added.** `related:` gains the two definition homes.
- The full `input_selectors` encoding table stays in this file — it is not duplicated elsewhere.

---

## Region: `language/spin2/` — 11 files

### `concepts/basic-io.yaml` · +84/−121 · `15c84de5`, `4cecb02c`, `1f37ae58`, `597dba`, `69af3733`
The byte-identical twin of the PASM2 file above; everything in that entry applies, with these
differences:
- **Removed — `hardware_specifications`**: the same block, the same `150mA`, the same
  false-negative citation.
- **Removed — `timing_considerations`**: this copy already carried a comment declining to publish
  per-call clock counts, but still shipped `pin_propagation: "3-7ns"`. Gone.
- **Corrected — the Spin2-specific wrong idiom.** `PINSTART(16, P_HIGH_15K, 0, 0)` followed by
  `PINFLOAT(16)  ' Input with pull-up` appeared **three times** (the `internal_pull_resistors`
  example, `common_patterns.button_read`, and `application_examples.scanKeypad`). All three replaced
  by `PINCLEAR` → `WRPIN(pin, P_HIGH_15K)` → `PINHIGH(pin)`. The keypad case matters most: it
  configured pull-ups on four column pins and then floated all four.
- **Added.** `control_registers.spin2_access` naming both routes (named registers vs `PINREAD`/
  `PINWRITE`), which the PASM2 twin does not need.
- 🟠 EF-063/EF-064 mis-attribution, both sites.

### `symbols/spin2-builtin-symbols-complete.yaml` · +1036/−20 · `cd860ba7`
**A consumer would notice: `p2kb_get` can now resolve a `P_*` name — which it could not before.**
- **Added — 68 symbol records.** 48 → **116** `P_*` constants, every one in the v55 table, each
  defined exactly once (verified: 116 unique, 0 duplicates), each with `value`, `bit_pattern`,
  `usage_context`, `related_symbols`, `hardware_relationship`.
- 🔴 **Added — a top-level `aliases:` block of 116 names.** *This is the change that makes the other
  1035 lines reachable.* `generate-p2kb-index.py` harvests top-level `aliases:` only; this file had
  none, so **not one of its 48 existing constants resolved by name through the published index**.
  Verified: all 116 aliases correspond to a `symbol_name` defined in the file; no `P_*` symbol is
  missing from the aliases.
- **Corrected — edition.** Header and `extraction_metadata.technical_accuracy` now record v55 for
  the 116 `P_*` records and v51 for the rest. Eight constants were superseded between the editions.
- **Removed — 2 fabricated names.** `P_LEVEL_B` and `P_SCHMITT_B` deleted from four
  `related_symbols:` lists with nothing substituted (v55 carries only their `_FB`/`_FBP`/`_FBN`
  forms; `pnut-ts` rejects the bare names while seven real siblings compile). **The lack:
  `validate-crossref-keys.py` reads top-level keys only, and this file's 135 `related_symbols:`
  lists are all nested.** `F-338`, `F-340`.
- 🟡 **Not corrected.** `total_symbols_extracted: 1224` against 136 actual records. §0.3 item 10.

### `methods/getct.yaml` · +23/−27 · `15c84de5`, `c733a223`, `597dba`
**A consumer would notice: this method has no description.**
- 🔴 **Removed and never returned — `description`.** §0.3 item 2. The old text carried a **derived**
  figure (*"wraps … approximately every 21 seconds at 200MHz"* = 2³²/200 MHz), which is why it was
  removed rather than repopulated verbatim; the disposition said *"return with a source or rewrite
  so it does not compute."* Neither happened.
- **Returned cited — `pitfalls`, rewritten and moved.** Now titled *"GETCT deadlines are bounded by
  the 32-bit counter, not by the 64-bit one"*, quoting the v55 definitions of `GETCT`/`GETMS`/`GETSEC`
  with their stated rollovers (49.7 days, 136 years). **Correctly reframed**: the old entry blamed
  arithmetic overflow in `(CLKFREQ/1000) * ms`; the real bound is the 32-bit counter itself.
- ⚖️ **De-duplicated.** The per-frequency ceilings (~10.7 s / ~8.6 s / ~6.7 s) are no longer restated
  here; a `per_frequency_ceilings:` key points at `timing_operations.yaml method_selection`.
  **Verified present at the target.**

### `methods/waitms.yaml` · +17/−11 · `15c84de5`, `597dba`
- 🔴 **Corrected — a ~400× wrong bound.** *"Maximum delay ~4,294 seconds (71 minutes)"* → the v55
  statement *"duration must not exceed `$8000_0000` clocks"*, with `ceiling_formula:
  "$8000_0000 / (CLKFREQ / 1000)"` and an in-file `correction_2026_08_25` marked *"Not restored."*
- **Added.** `clkfreq_dependent` — the same argument is a different number of clocks at every clock
  frequency, so the ceiling moves.
- ⚖️ Reshaped `notes` and `limitations` to mappings.
- ⚠️ The correction's own *"three orders of magnitude"* overstates a ~400× error. §1.6.

### `methods/waitus.yaml` · +21/−16 · `15c84de5`, `597dba`
- 🔴 **Corrected — the same class.** *"1–4,294,967,295 microseconds"* (the argument's 32-bit unsigned
  range) → the `$8000_0000`-clock bound, with `ceiling_formula` and a `correction_2026_08_25`.
- **Rebuilt — `clock_frequency_impact`.** Was a four-row table of clocks-per-µs. Now states the
  mechanism (`CLKFREQ / 1_000_000`), the granularity floor (*below 1 MHz, one microsecond is less
  than one clock and WAITUS cannot resolve its own unit*), and `when_to_use_waitx_instead` — naming
  the form the Parallax sources themselves emit during boot.
- ⚠️ Same *"three orders of magnitude"* wording.

### `methods/wrpin.yaml` · +21/−19 · `cd860ba7`
- ⚖️ **Removed 17 duplicate definitions by pointer.** The 4 `%TT` constants (`tt_field.constants`)
  and 13 smart-pin mode constants (`common_smart_modes`) deleted, replaced by references to
  `smart_pins.yaml` and the symbols file. **Reason stated in the file:** *"This block defined
  thirteen P_* constants a second time, in wording that had drifted from the source."*
- **Kept.** `tt_field.context_dependent` — the four `%TT` meaning-sets — stays here, because it is
  not duplicated anywhere; only its cross-reference wording changed.
- **Added.** `related:`.

### `debug-commands/pc_key.yaml` · +32/−11 · `15c84de5`, `597dba`
**A consumer would notice: the silent-failure rule is now explained, not just asserted.**
- ⚖️ Reshaped `usage_rules` from a list to `{source, rules, backtick_rule}`.
- **Returned cited.** `description` now quotes the v55 entry verbatim and explains what the 100 ms
  latch means for poll rate (*poll slower and you miss keypresses; poll faster and you read 0
  between them*).
- **Added — the mechanism behind the highest-value rule.** `backtick_rule` now gives the *why*
  (inside a backtick display message everything is text unless a further backtick escapes it back
  into a command, quoted from v55) alongside the *what*, and states the consequence plainly: *"It
  compiles clean, so the failure is silent and only visible at runtime."*
- **Added.** The Spin2-hub / PASM-cog pointer rule as a rule rather than only a separate block.
- **Removed.** *"Universal: accepted in every DEBUG display window's update phase."* The equivalent
  fact survives at line 83 (*"the keyboard mapping is the same in all nine windows"*), so nothing is
  lost.

### `conventions/johnny-mac-documentation-style.yaml` · +13/−10 · `4cecb02c`
### `conventions/spin2-docs-jonnymac.yaml` · +13/−10 · `4cecb02c`
Two files, one example, identical treatment.
- **Corrected — the mislabel.** `MOV pin_config, ##P_HIGH_150K  ' 150K pullup resistor` →
  `##P_HIGH_15K  ' drive high 15 kOhm`, plus the `DRVH sensor_pin` line the example needed and did
  not have.
- **Corrected — the example did not work.** `RDPIN sensor_bit, sensor_pin` reads a **smart pin**
  result; this is a plain bit-banged line. Replaced by `TESTP … WC` + `RCL sensor_value, #1`, which
  also removes the shift/or pair. The trailing `WRLONG sensor_value, PTRA  ' write to SPIN2
  variable` was wrong about how inline PASM returns a value; deleted.
- **Corrected — it did not compile as shown.** `sensor_pin`, `delay_count`, `bit_counter` and
  `sensor_delay` were all undeclared. Now a `CON SENSOR_DELAY`, a `sensor_pin` parameter, and the
  locals in the method's `|` list.
- **Note:** these are *documentation-style* files. The example is there to demonstrate commenting
  convention, and it was demonstrating it on code that could not run.

### `methods/pinfloat.yaml` · +3/−1 · `4cecb02c`
- **Corrected.** `common_uses`: *"Allow pull-up/pull-down resistors to set level"* → *"**External**
  pull-up/pull-down…"*. The file was already right where it was explicit (*"External pull-up/pull-down
  resistors will determine the level"*) and wrong one line above.
- **Added — the reason this file matters.** *"A drive-strength selection (`P_HIGH_*`/`P_LOW_*`)
  applies only while the pin drives, so floating the pin makes it inactive."* **This is where a
  reader looking for a pull-up lands**, so it is where the `DIR` rule has to appear.
- **Added.** `see_also: architecture/pin-drive-configuration.yaml`.

### `methods/cogstop.yaml` · +1/−1 · `4cecb02c`
**Genuinely one line.** `warnings`: *"Pins float - may need pull-up/down resistors"* → *"…may need
**external** pull-up/down resistors"*. In context (a stopped cog's pins floating) the missing word
made it read as a chip feature.

---

## Region: `hardware/` — 24 files

The largest region and the one with the most correction-per-line. Files are grouped by how they were
worked.

### Boards repopulated source-first from their own guides (`c733a223` → `491f2b55`)

#### `edge-32mb-module.yaml` · +213/−417 · **the biggest single file change**
**A consumer would notice: the pin map is back, correct, and the module no longer claims a second
part number it does not have.**
- 🔴 **Returned — `pin_mapping`.** The promotion filter ranked this **#1 of all returns**: it decides
  which pin numbers appear in generated code, and the file went 744 → 321 lines when it left. Back
  as: the summary sentence quoted from the guide (*"P0-P39 fully free; P40-P57 routed to on-module
  32 MB RAM; P58-P63 …"*), the eight `io_groups` with their `Vxx` edge pins and the P24-P31
  simultaneous-switching caution, the `vio_naming` rule, the PSRAM bank map, `alternative_functions`,
  the microSD socket pin roles, and the LED pins.
- 🔴 **Added — `boot_pin_direction_note`.** P58 = P2 **input** (MISO), P59 = P2 **output** (MOSI),
  and **P60/P61 swap between flash and SD**, cited to the ROM booter listing. This is `E-005` and
  its companion trap, landed in the board file where a designer meets it.
- **Corrected.** `alternate_part: "64000-ES"` and the matching alias **removed** — 64000-ES is a
  *different product*, the limited-edition P2-ES Eval Board. Reason stated in-file with two source
  locators. `availability.part_lookup` corrected to match.
- **Returned cited.** `specifications` (PSRAM part and organisation, the 3.8 V I/O pre-regulator the
  file did not carry, the 20 ms/2.5 ms short-circuit retry cycle, the ratings table),
  `boot_modes` (the six-row DIP table verbatim **with `table_note` explaining that rows 1 and 5
  carry the same switch setting and are disambiguated by card presence** — a real reading trap),
  `limitations`, `development_workflow` (now naming the card-edge socket part numbers and adding
  `psram_driver_note`: *the product guide neither ships nor describes a PSRAM driver*).
- ⚖️ **Reshaped.** `development_workflow` and `limitations` list → mapping.
- **Content that left `pin_mapping` and did not come back there:** the PSRAM `address_space`
  (`0x00000000–0x01FFFFFF`, 25 address bits, wrap at the 32 MB boundary) and the explicit
  access-mode table. **The driver-critical constants survive in `protocol_constraints`** —
  `chip_max_clock_mhz: 133`, `cs_low_note: "Must release CE# within 8us"`, `burst_size` — which was
  untouched by this release. Verified on disk.
- 🔴 **Still carries `E-010`**: `led_pins.mechanism` ends *"(or enable a pin pull-up)"*.

#### `edge-standard-module.yaml` · +162/−335
**A consumer would notice: the LEDs are on P56/P57 here and P38/P39 on the 32MB module, and the file
now says so in bold.**
- 🔴 **Returned — `pin_mapping`.** Ranked **#2**: the pins **differ** from the 32MB module, and
  confusing them puts an LED write on a PSRAM data line. 582 → 270 lines when it left. Back with
  eight `io_groups` (P0-P7 … P56-P63), `alternative_functions`, the microSD socket (added in Rev C),
  and `led_pins.warning:` — *"DIFFERENT PINS from the P2-EC32MB module, whose LEDs are on P38/P39.
  Confusing the two puts an LED write on a PSRAM data line."*
- 🔴 **Corrected — a number no source states.** `comparison_with_32mb.ec32mb_module.fully_free_pins:
  38` → **40**, with `accessible_pins: 46` added and a `source:` saying *"The value shipped here was
  38, which no source states."*
- **Added.** Same `boot_pin_direction_note`; the same `boot_modes` table and `table_note`;
  `specifications.memory.volatile: "none — this module has no PSRAM (contrast the P2-EC32MB)"` as an
  explicit discriminator.
- **Removed and not returned.** `revision_history` (Rev A→D VIN, current and switcher-frequency
  changes) — ruled not-actionable; nothing an agent emits changes.
- 🔴 **Still carries `E-010`.**

#### `addon-motor-driver.yaml` · +116/−67
**A consumer would notice: the pin table now records that the guide contradicts itself.**
- 🔴 **Added — `signal_map.pin_label_errata`.** The #64010 guide labels offsets 9/8 `PWM_UH`/`PWM_UL`
  in its header pinout and `PWM_XH`/`PWM_XL` in its pin-definitions table — duplicating channel X
  and leaving channel **U** undocumented. The KB previously carried a note calling this a *"docling
  table copy-error"*. **It is not**: the raw text layer carries the same duplication, so it is in
  the PDF. `E-008`. The distinction matters — an extraction artifact is fixed by re-extracting; a
  source defect never will be.
- ⚖️ Reshaped `signal_map` list → `{source, upper_header_note, lower_header_note, pins,
  voltage_sense_example, hall_header, pin_label_errata}`.
- **Returned cited.** `pwm_control` (the low-side-priority interlock quoted verbatim, the 250 ns
  deadtime **with its reason** — ~20 ns driver propagation but MOSFET settling time, so both can be
  partially on — the pull-down default state, the 0.8 V/2.2 V input thresholds), `current_sense`
  (3 mΩ shunt × INA180B2 gain 50 = **150 mV/A**, with the worked 1500 mV → 10 A example),
  `specifications` (restructured into `power` / `current` / `logic_levels` / `terminals`, adding the
  Rev B PCB change 80×64 → 70×70 mm).
- **Removed and not returned.** `power_signals` and `protection` — both ruled not-actionable. The
  12 V/50 mA and 5 V/100 mA boost regulators survive inside `specifications.power`; the Hall
  header's 5 V/100 mA survives inside `signal_map.hall_header`. **The protection list (reverse-biased
  diode per switching node, driver under-voltage lockout) is gone with no replacement.**

#### `hub75_adapter.yaml` · +100/−93
**A consumer would notice: several timing numbers were removed rather than corrected, each with a
note saying what would settle it.**
- 🔴 **Removed, with `gap_*` keys naming the missing source (3 groups).**
  - `gap_max_clock`: *"40 MHz max (35 MHz reliable), 13 ns propagation delay"* — *"appear in NO
    ingested source, and the manufacturer's own specification says 70 MHz."*
  - `gap_pulse_widths`: clock/latch/OE minimums (15 ns / 200 ns / 100 ns) and the 3-bit/8-bit
    colour-depth refresh table.
  - `gap_chain_limit`: *"Maximum 3 chains supported"* and *"Driver does not use P2 streamer"* — the
    second contradicted by the pinout capture (*"6-bit parallel data perfect for P2 streamer"*).
  **This is the right shape for a removal: the loss is stated where the reader meets it, with the
  document that would settle it named.**
- **Removed.** `power_requirements` — the per-panel current table (1.5 A–5 A typical, 4 A–20 A peak).
  Ruled not-actionable (external PSU sizing). The *rule* survives in `notes` (*"Never power a panel
  through the P2 board"*, 18 AWG or larger, distributed injection).
- **Returned cited.** `description`, `specifications` (70 MHz ceiling, < 50 mA board draw, the
  address-line/scan/panel-height mapping), `software_features` (measured refresh rates at 24-bit
  colour and 200 MHz, a bandwidth model with a worked example), `notes`.
- ⚖️ Reshaped `description`, `notes`; `software_features` rebuilt.
- 🟡 **Cites loose files at the ingestion root** — §0.3 item 11.

#### `addon-hd-audio.yaml` · +59/−49
- **Returned cited — `dac_board`.** Ranked #5 of the highest-value returns. The four `P_DAC_*` drive
  options with their impedance/peak-voltage pairs, the **parallel-drive rule** (four pins per
  channel wired in parallel → effective impedance = mode impedance / N), and the guide's own worked
  example (`123.75 / 4 = 30.9375 Ω`, *"you could plug the headphones directly into the audio jack"*).
- ⚖️ **Reshaped `description` to `{source, text}`** — one of the five hardware files where
  `description` is no longer a string. §1.10.
- **Removed and not returned.** `set_contents`, `use_cases` — not-actionable.
- **Removed content worth naming.** The `drive_strength_design.sixteen_steps` explanation (4 modes ×
  4 paralleled pins = the guide's "16 steps", which resolved gap **G-014**) and `parallel_technique`
  naming the official driver's `start()` default. The **conclusion** survives
  (`specs.drive_impedance: "18.75 ohms to 990 ohms, configurable in 16 steps"`); the derivation that
  made "16 steps" comprehensible does not.

#### `addon-hyperram-hyperflash.yaml` · +60/−23
- **Returned cited and substantially expanded.** `configuration` went from four prose lines to a
  per-section map: `reset_pads` with the shipped shunt position spelled out as a driver
  consequence — *"an emitted driver MUST drive IO+15 high before the memory will respond"* — the
  two memory-type shunts by section number and silk label, the three per-device resistors
  (`+ R C`: 10 kΩ CS# pull-up, 10 Ω on RWDS, 10 Ω on CK) with their pin offsets, and the full
  optional-pad table with the `RSTO` routing split.
- **Added.** A capture caveat: *"The capture was made with forced OCR because the PDF's embedded
  text layer is ciphered; part numbers and URLs carrying transcription risk are flagged [VERIFY]."*
- **Removed and not returned.** `host_note` — a jumper-position note; the board draws no 5 V so
  nothing emitted changes. Its substance (this board targets the #64000-ES specifically) is in
  `specifications.source`.

#### `addon-rtc.yaml` · +55/−33
**A consumer would notice: the file now tells you not to copy its own source.**
- 🔴 **Rebuilt — `pin_mode_tip`, and this is `E-004`.** The #64013 guide's Code Tip says *"set the P2
  Smartpin (or equivalent) **input mode** to **150 k-ohm pull-up**"* — our own mislabel, in a
  published Parallax document, **and** prescribed in the one configuration where it cannot work
  (input mode is `DIR` low; every drive selection is inactive while the pin is an input). The key is
  now: `board_fact` (SCL/INT/CLKOUT share the single +0 pin) · `p2_side_mechanism` (`P_HIGH_150K`
  with `DIR` **HIGH**) · `do_not_copy_the_guides_wording` quoting the guide and stating both errors
  · `scl_pull_up_caveat` — the guide's companion *"3.3 k-ohm pull-up"* names a value **the P2 drive
  ladder does not carry at all**, with the eight real rungs listed and a **GAP**: no ingested source
  says whether the board provides its own SDA/SCL pull-ups.
- **Corrected — two prose mentions relabelled.** The Parallax driver's *"3.3K pull-up"* setting is
  now explicitly *"the driver library's own term … on the P2 there is no pull-up resistor and no
  3.3 kΩ rung"*, in `rtc_chip` and in `resources.example_driver`.
- ⚖️ Reshaped `description` and `pin_mode_tip` to mappings.
- **Removed and not returned.** `power_signals` (two rails, no software enable) and `specifications`
  (battery chemistry, mechanical, shipping class). **The Seiko MS421R cell, its 1.5 mAh / 150 nA
  figures, the PCB dimensions and the Class 9 transport note are gone from the shipped set** — the
  correct disposition (nothing emitted changes), but the whole battery story left with it.
- 🟠 Carries the EF-063/EF-064 mis-attribution in `pin_mode_tip.source`.

#### `addon-serial-host.yaml` · +47/−107 · **the largest net removal among the add-on boards** (−60 lines; only the two Edge modules shrank more, and they shrank while gaining accuracy)
- 🔴 **Lost its top-level `description`** — §0.3 item 8. Ruled not-actionable (the software-relevant
  part is the enable pin, which is in `signal_map`), which is defensible; the file having *no*
  identity line is a consequence nobody chose.
- **Returned cited.** `signal_map` (the two 5 V **software enables** at offsets 1 and 5 — the reason
  this board's rails pass the actionability test at all), `usb_host_capabilities` with the enable
  sequence quoted verbatim and `requires_5v` stated, and a rebuilt `development_workflow` as a
  six-step emitted sequence.
- ⚖️ Reshaped `signal_map` and `development_workflow`.
- **Removed and not returned.** `specifications`, `power_requirements`, `limitations` — the per-port
  500 mA / 1 A total / ~2 mA per LED budget and the physical dimensions. The 500 mA figure survives
  in `usb_host_capabilities.power_switch`; the 1 A total does not.

#### `addon-serial-device.yaml` · +28/−63
- ⚖️ Reshaped `description` and `signal_map`.
- **Added — `usb_pin_pairing_note`.** *"Each channel's D-/D+ occupy an adjacent even/odd pin pair …
  the even pin of the pair is the one named when configuring the mode."* This is the fact that makes
  the board usable with the `%11011` smart-pin mode, and it was not in the file.
- **Removed and not returned.** `specifications` (3.3 V supply + mechanical) and `rev_b_5v_note`
  (a shunt-jumper note for one board revision).

#### `addon-wx-wifi.yaml` · +31/−30
- ⚖️ Reshaped `pin_descriptions` list → `{source, columns, pins, uart_orientation, prop_plug_note, schematic_caution}`.
- **Added — `uart_orientation`.** *"DO is the module's transmit and DI its receive, so a host's TX
  goes to DI and a host's RX comes from DO."* The table always implied it; nothing stated it.
- **Added — `schematic_caution`.** *"The guide's schematic pinout figure OCR'd to noisy labels; the
  Pin Descriptions table above is the authoritative source and the figure is illustrative only."*
  An honest note about our own capture quality.
- **Removed and not returned.** `part_variants` (32420D DIP vs 32420S SIP) and `specifications`
  (voltage per form factor, 75 mA typical / 360 mA transmit peak, logic levels, dimensions,
  operating temperature, and the *"DIP is NOT compatible with Parallax XBee adapter boards"* note).
  Ruled not-actionable. 🟡 **The two form factors are still referred to by name elsewhere in the
  file and in three carrier files (`#32420S`), with nothing now defining the difference.**

#### `programming-prop-plug.yaml` · +51/−28
- ⚖️ Reshaped `description` to `{source, text}`.
- **Returned cited and expanded — `reset_option`.** The DTR / RTS / none choice is now three named keys with
  the physical component position for each, plus the ~20 µs (15–25 µs) pulse and the silk marking
  area. **This is a host-side tool's download handshake** — the reason the block is actionable.
- **Returned cited — `specifications`.** 300 baud–3 Mbps, USB 2.0 FS, FT231X, 5 V-tolerant buffered
  RX, dimensions with and without connectors.
- Nothing removed on net; this file only gained.

#### `addon-goertzel-touch.yaml` · +25/−14
- **Returned cited — `specifications`.** `io_pins_used: 8`, the compatible-host list, the mounting
  hole, and a `pcb_size_class` that is honest about what the capture could not resolve: *"the guide
  … gives numeric dimensions only in a drawing, which the capture did not resolve to numbers."*
- **Added.** `pin_addressing` (base_pin + offset) and the auxiliary-power recommendation.
- Note the *identity* correction for this board lives in `p2-hardware-feature-comparison.yaml`
  (§1.7), not here — this file was already the Goertzel board.

#### `edge-mini-breakout.yaml` · +39/−48
- 🔴 **Corrected — a phantom feature.** *"USB connector onboard / Built-in USB-to-serial"* → *"This
  carrier has NO built-in USB-to-serial converter."* Prop Plug (#32201) is the only wired path;
  wireless via the WX Adapter.
- **Corrected — a pin claim.** *"All 64 pins on edge castellations"* / *"blocked_pins: P32-P55 (not
  accessible)"* → 40 pins at five header sockets, and P32–P55 *"may be accessed by adding jumper
  wires on the bottom side of the PCB … so they are reachable, but only by soldering, never by
  plugging an accessory in."*
- **Added.** The barrel-jack power input, the reset button, the two 4×5 prototyping matrices, and
  the accessory list.
- **Removed and not returned.** `specifications` and `power_management` (dimensions, "5V or USB
  powered", "Onboard 3.3V for module"). The last was wrong anyway — VIO comes from the edge module.

#### `edge-standard-breakout.yaml` · +29/−45
- 🔴 **Corrected — the same phantom USB-to-serial.**
- **Added.** Eight 2×6 accessory headers; the note that the **last** header carries P58–P63 + RES for
  wireless programming; the 2×3 power header; the barrel jack; the per-pin 30 mA figure.
- **Removed and not returned.** `specifications`, `power_management` — same class as the mini
  breakout.

#### `edge-breadboard-carrier.yaml` · +15/−67
- 🔴 **Corrected — the same phantom USB-to-serial**, with the correction written as a comment block
  citing the guide.
- 🔴 **Removed and not replaced — every electrical and physical figure.** `specifications`
  (8.0 × 3.5 in, area, size comparison), `power_specifications` (*"6-9V barrel jack
  (recommended)"* — **wrong**; the guide says 5 VDC, abs max 5.5 V) and `power_management`
  (regulators, rails, protection) all left, and **no supply figure or dimension returned to this
  file**. Its two sibling carriers each gained a `connectivity.power_input` line; this one did not.
  §0.3 item 7.
- **Removed and not returned.** `specialized_features` — the ~830 tie points, the 8 servo ports'
  3-pin connector type and separate 5 V rail. The servo ports survive as a bare mention in
  `advantages` and in `p2-hardware-feature-comparison.yaml`.
- 🟡 Carries a **pre-existing** duplicate `educational_value:` key. §0.3 item 9.

### Boards corrected in place (`1f37ae58`, `43b0ede2`, `4cecb02c`)

#### `p2-eval-board.yaml` · +95/−49 · `c733a223`, `1f37ae58`, `491f2b55`
**A consumer would notice: almost every specification changed, and five features the board does not
have are gone.**
- 🔴 **Removed — five fabrications** (`1f37ae58`, `F-328(b)`): `built_in_peripherals.proto_area`
  (*"prototyp"*/*"breadboard"* return **zero hits** in the repaired capture), `switches.user_switches:
  "TBD quantity"` (there are four DIP switches and a reset button; no user switches),
  `headers.connector_type: "Standard 0.1 inch headers"` (the 0.1″ feature is the AUX **power pads**),
  the whole `video_audio:` block (VGA/HDMI/audio — *"Fabricated whole"*), and
  `connectivity.programming` (USB-B/USB-C + Prop Plug #32201 — the board has two micro-USB sockets
  and no Prop Plug header).
- 🔴 **Corrected — the silicon.** `revision: "Rev D"`, `chip: "P2X8C4M64P"` → **Rev C**,
  `P2X8C4M64PES`, with a `part_number_note` recording that the guide itself is inconsistent across
  four locations.
- 🔴 **Corrected — the clock.** `"20MHz crystal, PLL to 320MHz"` → recommended maximum **180 MHz**,
  with overclocking recorded as the guide states it.
- **Corrected — everything that was `TBD`.** Flash `"TBD - check documentation"` → **16 MB
  W25Q128JVSIM**; dimensions `TBD` → **3.55 × 3.55 in** with `dimensions_note` recording `E-009`;
  weight/current/temperature `TBD` → the real ratings, two USB current limits (500 mA / 2000 mA),
  the 5.5 V absolute maximum, the brownout threshold.
- 🔴 **Added — a behavioural fact an agent must get right.** `buffer_polarity`: the eval board's LED
  buffer *"drives the status LED ON when the P2 I/O signal line is **LOW**. NOTE this is the
  OPPOSITE polarity to the P2 Edge modules."*
- **Kept, against expectation.** `expansion_ecosystem.individual_addons` was flagged as fabricated
  and is a real cross-reference roster. §1.7.
- 🟡 **Residual.** `connectivity.expansion.headers: "Standard 2x6 expansion headers"` and
  `built_in_peripherals.headers.pin_access` still stand alongside the new
  `specifications.headers.io_breakout` (eight edge headers). Not wrong, but the file now says it
  twice at two levels of accuracy.

#### `p2-hardware-feature-comparison.yaml` · +225/−115 · `4cecb02c`, `1f37ae58`, `491f2b55`
**A consumer would notice: a whole board entry was the wrong board.**
- 🔴 **Corrected — `digital_io_board` → `goertzel`.** *"Combined Digital I/O … 4 LEDs, 4 switches,
  4 shared pins, electrical isolation"* → the Rev B Goertzel experimenter board, with a
  `correction_note`: *"No such board exists in the #64006 series."* **Residual: the old key name
  still stands twice in this file — §0.3 item 3.**
- 🔴 **Corrected — three fabricated eval-board peripherals** (`1f37ae58`): `audio_capability: "Stereo
  DAC output"`, `video_capability: "VGA output"`, `breadboard_area: "Large prototyping area"`.
- 🔴 **Corrected — three invented carrier part numbers** → `64029` / `64019` / `64020`, plus their
  wrong dimensions, the mini breakout's *"3.3V input only"*, and `crystal_frequency: 20MHz` on
  carriers that carry no crystal.
- 🔴 **Corrected — the add-on capacity claim.** *"Up to 2 add-on boards"* / *"A-side (P32-P39) +
  B-side (P24-P31)"* → eight headers covering all 64 pins, with the ACC HDR 5 V gating, the two
  headers that have no 5 V pin, and a caution that the P56–P63 group carries the serial link, flash
  and microSD.
- **Corrected.** Edge module dimensions (27×40 mm → 37 × 51.7 mm), P2-EC32MB pin counts
  (64 → 46 accessible / 40 free), A/V breakout (`pins_required: 16` → 8, `rca_outputs: 3` → 4),
  the eval board's USB story (no USB-C, no barrel jack), the control board's *"pull-up resistors"*
  (`4cecb02c`).
- ⚖️ **Added — provenance honesty.** `selection_criteria.source` and an `authored_here_note` state
  that the cost tiers, educational ratings and recommendations *"are authored in this knowledge base
  and have NO upstream source in the ingestion tree (F-352 sub-rule P): treat them as guidance, not
  as documented fact."* This is the right disposal for content that cannot be returned to a tree it
  never came from.

#### `addon-control-board.yaml` · +55/−38 · `4cecb02c`, `43b0ede2`
- 🔴 **Corrected — the mislabel, five sites.** *"Use internal pull-down (P_LOW_15K)"* → *"Hold the pin
  low with a weak drive (`WRPIN P_LOW_15K`, then `PINLOW` so DIR is high)"*, in all four switch rows
  and in `code_patterns.init_control_board` (which previously commented `PINLOW` as *"Activate
  pull-downs"*).
- 🔴 **Removed — three inferences** (`43b0ede2`). `current_per_led_ma: 4`, `total_current_ma: 16`,
  and *"~4 mA, ~2.0 V LED drop"* / *"~20 ms"* debounce from the signal-map notes. **Reason: the
  #64006A guide states 470 Ω and nothing else — it gives no LED current, no forward drop and no
  debounce interval, so neither do we.** A clean example of a citation gate producing a *reduction*
  rather than a citation.
- ⚖️ Reshaped `signal_map` list → `{source, pins}`.
- 🟡 **`E-006` is unresolved here.** `description` states *"the I/O pin reads high while the button is
  pressed"* and now attributes it to the guide — but that same guide sentence also says the pin is
  *"driven low while the button is asserted"*. Which half is true decides whether generated code
  tests high or low. A jumper-only bench test would settle it.

#### `addon-av-breakout.yaml` · +70/−44 · `43b0ede2`
- ⚖️ **Reshaped `signal_map`** list → `{source, pins}` — one of the two files where `43b0ede2`
  introduced the split (§1.10).
- **Added.** Verified `source:` keys on `signal_map`, `specifications` and `audio_capabilities`,
  each naming the #64006 guide line range and the per-board capture, plus the host VIO rail
  (*"3.3 V up to 300 mA per 8 I/O pins"*) from the eval board guide.
- Content unchanged — this is a citation pass, and it is the largest one.

#### `addon-digital-video-out.yaml` · +21/−2 · `43b0ede2`
- **Added.** `source:` on `unused_connector_signals` and `specifications`; the description now
  attributes itself to the guide.
- **Corrected — a small provenance repair.** `advantages`: *"Optional monitor power supply connection
  via ACC 5V bridge"* → *"Optional monitor power supply via the ACC bridge (see
  `unused_connector_signals`)"* — a marketing bullet that restated a technical fact now points at
  where the fact is stated.

#### `addon-led-matrix.yaml` · +14/−2 · `43b0ede2`
- **Added.** `source:` on `specifications`; guide attribution in `description`.
- **Corrected.** `advantages`: *"Low instantaneous current (~4 mA, one LED at a time)"* → *"…one LED
  lit at a time (figure stated under `description`)"*. Same de-duplication move: the number lives
  once.

#### `addon-mini-prototyping.yaml` · +32/−4 · `43b0ede2`
- **Added.** `source:` on `power_rails`, `prototyping_grid` and `specifications` (three blocks that
  had none), plus guide attribution in `description`.
- **Corrected.** `advantages`: *"Both 3.3V (VIO) and 5V power supplies available at the grid"* →
  *"Both host power rails available at the grid (named under `power_rails`)"*.

#### `addon-microsd.yaml` · +7/−0 · `43b0ede2`
- **Added only.** A `source:` on `power_signals` quoting the #64009 guide, including *"Do not supply
  power to both the accessory header pin and SIP breakout pad at the same time"* — a rule the block
  already stated, now traceable.

#### `addon-wx-adapter.yaml` · +4/−0 · `43b0ede2`
- **Added only.** A `source:` on `power_signals` quoting the #64007 guide's one relevant table row.
  The smallest hardware change in the release.

---

## Appendix A — Commit legend, with what each actually did

| Hash | Task | Subject says | Diff also shows |
|---|---|---|---|
| `15c84de5` | «#293» §4a | Remove all 59 uncited quantitative blocks | **60** blocks, 25 files. The record's own reconstruction confirms 60; the executor's 59 was an undercount. |
| `c733a223` | «#294» §4b | Purge the hardware tree, then repair two gate defects | 59 blocks, 17 files — 48 + 11 in two records. Four `-key:`/`+key:` pairs are end-of-file newline no-ops, not removals. |
| `cd860ba7` | «#295» §6 | Define all 55 undefined constants | **68** symbol records added (48 → 116); the `aliases:` block; 17 duplicate definitions removed by pointer; 2 fabricated names deleted; 6 findings filed. |
| `4cecb02c` | «#296» §5 | Correct the drive-strength mislabel class | **Also** repaired five semantic defects in worked examples (`F-345`, `F-346`) and rewrote `F-322`'s own body after finding its Silicon Doc attribution does not exist. |
| `1f37ae58` | «#298» §7 | Apply the promotion filter, delete a pin-current figure | 4 files, +0/−43. Two `hardware_specifications` blocks and 8 sub-keys. Verified as pure deletions. |
| `597dba` | «#299» §8b | 45 blocks return cited, 13 stay gone, three shipped errors fall out | **46** blocks returned by key count (the 46th is `io_pin_timing description`, returned rewritten). One ACTIONABLE block became a gap; one assigned block was not executed. |
| `491f2b55` | «#307» §8b | Repopulate hardware source-first, stop calling the Goertzel board a Digital I/O board | 34 returned, 24 held. **Also** corrected six wrong scalars in *surviving* blocks that only a source-first read could find. |
| `9370c580` | «#300» §9a | Drain KB-side findings, reject two register corrections | 1 YAML file. The rejections are the substance; the ADC mid-supply centering (`EF-024`) is the change. |
| `e92aa02f` | «#301» §9b | Drain manual-prose findings, falsify "masters are clean" | 1 YAML file. Corrected the EF-063/EF-064 attribution — **and introduced the duplicate `note:` key.** |
| `69af3733` | «#304» | Fix the citations that route every new agent | 4 YAML files + `README.md`. Measured the crossref gate's blind spot — see the caveat in §1.11: the commit's figure and the one the tool prints at HEAD disagree. |
| `43b0ede2` | «#305» §10b | Arm both instruments as blocking gates, repair the harvest | 7 YAML files. 17 blocks gained citations, 3 inferences removed. **Also** reshaped `signal_map` in two files. |
| `fc45912d` | — | Write the release entry | **No YAML.** Out of scope. |

## Appendix B — Findings referenced, with status as recorded

| ID | Status | One line |
|---|---|---|
| `F-250` | — | Forced-OCR re-ingestion of the #64000 guide; the source of every corrected eval-board quantity |
| `F-321` | `PENDING-VALIDATION` | The 16 drive-strength selectors documented as bias resistors |
| `F-322` | `PENDING-VALIDATION` | Every worked pull-up example disables the drive it configured; its Silicon Doc attribution is ours |
| `F-323` | `PENDING-VALIDATION` | The two `basic-io.yaml` files gave contradictory mechanisms |
| `F-324` | `PENDING-VALIDATION` | `bits_M_6_0: "Control drive strength"` wrong at both ends |
| `F-325` | `PENDING-VALIDATION` | The real ladder was fully in the ingestion tree and entirely absent from the KB |
| `F-326` | `PENDING-VALIDATION` | `wrpin.yaml` stubbed the field that carries the pin configuration |
| `F-327` / `F-329` / `F-333` | `PENDING-VALIDATION` / `PARTIAL` | The fabricated drive ladder + slew rate + timing model |
| `F-328` | — | `p2-eval-board.yaml` describes a board the #64000 guide does not |
| `F-330` | — | Hardware Manual VCO range contradicts Datasheet + Silicon Doc (= `E-003`) |
| `F-331` | `PENDING-VALIDATION` | Three of six WRPIN D-operand fields mislabelled |
| `F-334` / `F-347` | `PARTIAL` | The two purge removal records |
| `F-336` | `CONFIRMED` | `P_HIGH_15K \| P_LOW_FLOAT` has no Parallax statement and no bench result |
| `F-337` | `CONFIRMED` | Datasheet + Hardware Manual vs Silicon Doc on `%TT` in DAC_MODE; **the KB follows the minority** |
| `F-338` | `PARTIAL` | `P_LEVEL_B` / `P_SCHMITT_B` do not exist |
| `F-340` | `PARTIAL` | Crossref validator reads top-level only — scope half done, traversal half owed |
| `F-341` | `PARTIAL` | Six of our own analysis documents sit inside the fidelity gate's truth root |
| `F-342` | `RESOLVED` | The RTC guide states the mislabel itself (= `E-004`) |
| `F-343` | `PENDING-VALIDATION` | The Control board credited with a bias network its guide does not give it |
| `F-345` / `F-346` | `PENDING-VALIDATION` | Inverted flag polarity; three structurally unrunnable examples |
| `F-348` | `PARTIAL` | A *cited* block shipped 5× the datasheet's absolute maximum |
| `F-349` | `PENDING-VALIDATION` | PLL lock 10 µs vs 10 ms, **and two emitted `WAITX` lines** |
| `F-350` | `PENDING-VALIDATION` | The eval-board fabrication class is not confined to one file |
| `F-351` | `RESOLVED` | The gate read part numbers and Unicode code points as amperes |
| `F-352` | `CONFIRMED` | Two KB areas are authored-here with no upstream; sub-rule P had no branch |
| `F-353` / `F-354` | `PENDING-VALIDATION` / `CONFIRMED` | The hardware return record; seven content-level holes inside blocks that did come back |
| `F-356` | `CONFIRMED` | The mislabel is alive in the IOSP master at 23 sites — **manual scope, not YAML** |
| `F-359` | `CONFIRMED` | Seven `architecture/` files carry a fabricated provenance header, and the header is what silences the sourcing gate. Filed by another agent during this ledger's writing; one of the seven (`io_pin_timing.yaml`) is in scope. §0.3 item 12 |
| `E-001`…`E-010` | see §1.9 | Source errata |

`F-354` is worth reading beside this ledger: it records **seven content-level holes inside blocks
that DID come back**, which is a category this ledger's key-level accounting cannot see.

---

*Written 2026-08-25 from `v1.17.0..0a5323ab`. Every quantity re-derived from git and from parsed
YAML at the time of writing. No YAML was edited in the making of this document.*


---

# ADDENDUM — commit `ad4f974f`, added after this ledger was first written

> ⚠️ **This ledger was built against the range ending at `43061dad`.** One further commit has since
> touched the shipped set, and it is included here so the review covers the whole release. Nothing
> above is changed by it.

**`ad4f974f` — "Document what the streamer captures, and why a smart-pin bus must be watched from
next door"** · 12 YAML files · **+741 / −75**

## The reason, and the lack behind it

Stephen asked a research question — *can four smart pins running SPI be traced through their
nearest neighbours via the streamer, at Nyquist rates?* Answering it required four facts. The KB
carried two well, one half, and **one not at all**: that on a pin running a smart-pin mode, `IN` is
the smart pin's event flag rather than the pin's logic level.

**The lack:** the KB stated only the harmless half of that fact — *"the resultant 'A' will drive
the IN signal in non-smart-pin modes"* — as an aside inside the input-selector discussion. **Nothing
stated the contrapositive**, which is the operative half. A reader could conclude direct capture
works, build it, and record ready-pulses instead of traffic. Nothing checked for a missing
contrapositive because no instrument can.

## What changed

| File | |
|---|---|
| `architecture/streamer/pin-capture.yaml` | +312 / −0 |
| `architecture/streamer/pin-selection.yaml` | +188 / −57 |
| `architecture/smart_pins.yaml` | +85 / −0 |
| `architecture/streamer/modes-reference.yaml` | +42 / −7 |
| `architecture/streamer/_index.yaml` | +25 / −0 |
| `language/spin2/debug-displays/logic.yaml` | +22 / −0 |
| `architecture/streamer/overview.yaml` | +21 / −4 |
| `architecture/streamer/dds-goertzel.yaml` | +15 / −3 |
| `architecture/streamer/nco-timing.yaml` | +11 / −2 |
| `architecture/streamer/dac-routing.yaml` | +10 / −2 |
| `language/pasm2/wrpin.yaml` | +9 / −0 |
| `architecture/pin-drive-configuration.yaml` | +1 / −0 |

**Added.** `architecture/streamer/pin-capture.yaml` (new) — why capturing a smart-pin bus directly
fails, the neighbour-routing composition, the alignment rule restated where it would be copied, and
an explicit refusal to state a sample-rate ceiling no source gives.
`smart_pins.yaml` gains `in_signal_semantics:`. All seven streamer files gain `aliases:` — they had
**none**, so none was reachable by name.

**Corrected.** `pin-selection.yaml`'s `input_modes:` said only *"WRFAST enabled"*; it now states
what is read, the widths, and the accrual rule. Its `sub_pin_selection` table gave a dense-slot
mapping contradicting the 8-pin-increment rule **and printed the unaligned-base trap as the line a
reader copies** — filed as **F-361**. `smart_pins.yaml`'s `in_flag.clearing` listed three
instructions; the source gives five.

**Judgement, not correction.** `logic analyzer` now resolves to **both** the capture page and the
DEBUG LOGIC window, rather than one replacing the other — a capture and its display compose.

## Two claims of mine this commit corrected

1. I reported that `logic analyzer` misrouted to a Spin2 `LOGIC` **operator**. **No such operator
   exists in the KB** — it resolves to the DEBUG LOGIC display window, which is the P2's actual
   logic-analyser. The alias was right all along; I had diagnosed a confident wrong answer and
   produced one.
2. I wrote that `RQPIN` lowers the `IN` flag. The Silicon Doc says read-quiet **does not
   acknowledge** — which is precisely why many cogs can use it at once.

## Status of this material — read before relying on it

An external project building the same instrument has since reported a bench result that would
**contradict the mechanism above** — that the streamer reads the pin rather than `IN`, making
neighbour routing ineffective. **Stephen has withdrawn that report as not yet reliable**
(2026-08-26): their tool is still being brought up, and real findings will follow.

**So this content stands as shipped** — it is sourced to the Silicon Doc (`p2-documentation.txt:3961`,
`:7833`, `:7615`) and correctly cited — **but it is the documentary reading, and a bench result
outranks it in this project's authority order.** `VO-J-005` is written and its arm D is close to the
deciding experiment. Treat this section as the one place in the release where a known challenge is
outstanding.
