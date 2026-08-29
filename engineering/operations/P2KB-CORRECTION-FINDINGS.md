# P2KB Correction Findings — Consolidated Register

**Purpose:** the register of everything we find that is **wrong or needs correction** — primarily in the P2 Knowledge Base YAML (`deliverables/ai/P2/`), but also any other source/content correctness issue worth tracking. This is the hand-off document for the agent that corrects the P2KB (via `yaml-knowledge-base-maintenance`).

**This file carries OPEN work only.** Closed findings are archived, not kept here. Ask "what is
outstanding?" of this file alone — never re-derive completion state from an archive.

**How to use it:**
- When any work (manual production, audits, example compilation, ingestion, bench) surfaces something incorrect, **add it here** — do not leave it only in a per-manual note.
- Each finding gets an ID, a status, the exact location, what is wrong, the evidence, and the proposed correction.
- **Annotate as you fix, in the same pass** — flip the status, add an applied-note and source trace, and log newly-surfaced defects as new findings. A register whose statuses lag the YAML lies and invites re-chasing.
- **One finding lives in exactly one place.** When a finding is revised, **rewrite its entry in place**; never append a correction below the entry it corrects. The prior text is in git and in the archives.
- Consultation protocol (status-before-content, duplicate IDs are a STOP): the project's
  `REGISTER-CONSULTATION` protocol (agent-side; not shipped with this repo).

**Status legend:** `CONFIRMED` (verified against an authority; ready to fix) · `NEEDS-VERIFICATION` (suspected; must be checked before acting) · `PARTIAL` (some of it applied; the rest still owed) · `PENDING-VALIDATION` (the fix is fully applied; only its validation — a render, a release, a re-test — is owed. Added 2026-08-21: the rule below already described this state and there was no token for it, so nine findings sat as `CONFIRMED` with "render owed" prose and tripped the hygiene gate on every run) · `DONE` (corrected + verified) · `WONTFIX` (investigated, not a defect) · `RESOLVED-INVALID` (the reported defect does not exist) · `TRACKED → ingestion` (real, but the resolution lives in the ingestion head) · **`RESOLVED`** (the defect is gone AND its validation has landed — the render/release/re-test was RUN and the artifact READ; a fix applied but unvalidated is `PENDING-VALIDATION`, never this. **Added to this legend 2026-08-25 («#302»): it was already the file's MOST-USED token — 31 of 82 entries — and the legend had never defined it, so a third of the register could not be classified by the very vocabulary this line exists to declare**) · `PARTIALLY CONFIRMED` (a ONE-OFF variant used only by F-202, where part of the claim is grounded in a source and part awaits silicon; it classifies as **`CONFIRMED` — open** — do not spread it).

⚠️ **`RESOLVED` entries are CLOSED and are awaiting the next archive sweep, not awaiting work.** **31 of the 82 live entries are `RESOLVED`, so "how many are outstanding?" is 51, not 82** (measured 2026-08-25, «#302»). The hygiene gate deliberately does NOT treat `RESOLVED` as closed-but-live (only `DONE` / `WONTFIX` / `RESOLVED-INVALID` trip check 3), which is why they accumulate silently between sweeps.

**A fix applied but not yet validated is NOT done** — it stays here until its validation lands (the `[~]` rule from `punch-list-maintenance`). That covers a YAML edit awaiting its EF entry, and a manual fix awaiting its re-test.

**Authority order for P2 facts:** empirical / hardware-verified results in `engineering/ingestion/external-sources/hardware-verification/` (strongest — they have overturned every other tier) → the `pnut-ts` compiler, for legality only → Parallax documentary sources under `engineering/ingestion/sources/` → the published P2KB YAML. Community/forum material is an upstream lead, never a citable authority.

**No inference or derivation.** Every correction must trace to an authoritative source. Aligning a file to an authority it contradicts is fine; **inventing a value or claim that no source states — by computation, reasoning, or "it must logically be" — is not.** If a change can only be justified by inference, log it as a finding that needs a source. Match the source's wording, not an interpretive paraphrase.

**Next finding ID: `F-381`** · gap IDs are **not allocated here** — `engineering/ingestion/KNOWLEDGE-GAPS.md` owns the `G-` allocator and declares its own counter. (This line previously carried `Next gap ID: G-008`, stale by fourteen against that register's actual G-022; two registers claiming one allocator is the collision `audit-register-hygiene.py` exists to catch. Retired 2026-08-26 — see F-352 for the earlier, smaller instance of the same drift.)

**Archives** — search them before re-filing; a finding that reappears is usually a regression:
- F-001…F-124 → `correction-sweeps/2026-06-13-P2KB-CORRECTION-FINDINGS-archive.md`
- F-125…F-266 (closed) → `correction-sweeps/2026-08-15-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-08-19 (18 findings: F-227, F-228, F-254, F-255, F-257, F-258, F-259, F-260, F-261, F-262, F-263, F-264, F-265, F-266, F-267, F-269, F-270, F-273) → `correction-sweeps/2026-08-19-P2KB-CORRECTION-FINDINGS-archive.md`

> **Swept 2026-08-19** per `punch-list-maintenance`, as **rename-then-trim** (the archive is a
> git-tracked rename of the original; both files are subtractions from a preserved copy — see the
> skill's project overlay for why building the output loses content). 18 findings archived, 3,559 →
> 2,478 lines. **Classified by STATUS TOKEN only.** Sixteen findings whose headline reads "source
> fixed"/"tool fixed" **stayed open**, because their status is still `CONFIRMED` and most say
> "render owed" — this file's own rule is that a fix applied but not yet validated is NOT done. A
> first pass that trusted the prose would have archived all sixteen. Verified with
> `audit-register-hygiene.py --sweep-check`, which reads the pre-sweep revision out of git.
>
> **Swept 2026-08-15** per `punch-list-maintenance`: 129 closed findings archived, 3,161 lines → this
> file. The previous sweep was deferred on 2026-06-20 pending G-004 and G-005; G-005 closed
> 2026-07-04, and G-004's remainder was found to be out of KB scope entirely (see its entry), so the
> deferral's condition is discharged.

---




## The SETXFRQ increment rule is quoted in three files and applied in none of their pixel-rate tables — 9 wrong NCO words in the shipped KB, 8 more in a released manual (2026-08-29, «#332» release-review recomputation) — F-380

### F-380 — `SETXFRQ` values computed by truncation or by `round()`, where the source requires truncate-then-increment — `RESOLVED`

**The rule, read at the line.** *Parallax Propeller 2 Documentation* v35, Streamer NCO —
`engineering/ingestion/sources/silicon-doc/part2-pixel-ops.txt:104-117`, with the footnote at
`:117` continuing at `:121` (one sentence, split by a page break):

> "For fractions with remainders, the computed D/# value should be incremented, in order to
> produce proper initial rollover behavior."

The source's own table shows it applied: `1/3` is given as `$2AAA_AAAA+1`, `1/5` as
`$1999_9999+1`, `1/6` and `1/7` likewise, while the exact divisions `1/2`, `1/4` and `1/8` carry
no increment. So the rule is **truncate, then increment when the division leaves a remainder** —
equivalently a ceiling. It is **not round-to-nearest**: a remainder below half still increments.
That distinction is the whole defect.

**What was wrong.** Every affected block *quoted or paraphrased the correct rule* and then failed
to apply it to its own numbers. Nothing detected this: the values are well-formed hex in the right
magnitude, they carry citations, and an off-by-one in bit 0 of a 31-bit phase word is invisible to
every gate we run.

*Shipped KB — `language/pasm2/setxfrq.yaml`, 2 of 4 `common_values`:*

| target @ 250 MHz | rule | shipped |
|---|---|---|
| 25.175 MHz | `$0CE3_BCD4` | `$0CE3_BCD3` |
| 44.1 kHz | `$0005_C7C1` | `$0005_C7C0` |

The other two (`$0CCC_CCCD`, `$0006_4A9D`) were right, and their `arithmetic:` notes said
"remainder rounded up per the source footnote" — the two wrong ones carried no such note. That is
the signature: the increment was applied where someone wrote it down and skipped where they did not.
The file also stated **two different rules** — `computation:` said `D = round(...)` while `source:`
quoted the round-up footnote — and its `cross_checked_against:` cited `nco-timing.yaml` as
agreement, which was self-corroboration: that file carried the same wrong value.

*Shipped KB — `architecture/streamer/nco-timing.yaml`, 7 of 12 `video_rates`:* 25.175 MHz at all
three system clocks (`$0CE3_BCD4` / `$0ABD_C806` / `$0A11_EB86`), 40.000 MHz @ 300 (`$1111_1112`),
65.000 MHz @ 250 (`$2147_AE15`), 74.250 MHz @ 250 (`$2604_1894`) and @ 320 (`$1DB3_3334`). The
same file's `common_values` ratio table is **fully correct at all 8 ratios** and its
`frequency_calculation.note` stated the rule — the file applied it in one block and not the other.

*Released manual — `p2-streamer-programming-guide` v1.1.0 (published 2026-08-22, 91pp), 8 of 18
values in Appendix C's "Common Video Pixel Rates" table,* plus the rule stated as
`round($8000_0000 * pixel_rate / clock_frequency)` in **three** places (the §-body prose, the
worked Example 2, and the table caption). The worked example prints
`word = round($8000_0000 × 25.175 / 250) = $0CE3_BCD3` — teaching the wrong rule and the wrong
result in one line. Wrong rows: 640×480 @25.175 (all three clocks), 720×480 @27.000 MHz @300,
800×600 @300, 1024×768 @250, 1280×720 @250 and @320.

**How it surfaced.** The 2026-08-27 release review flagged `setxfrq common_values` as a two-value,
two-file residue (§0.5 item 13 of the change ledger). Recomputing the whole class rather than the
two named values found 9 wrong in the KB and 8 more in a released manual — the ledger's count was
low because it checked the values the differential read had named, not the class.

**Applied 2026-08-29 («#332»).** All 9 KB values corrected; both files' rule statements rewritten
to state truncate-then-increment explicitly, with the citation and the page-break note; the
`round()` wording removed from `setxfrq.yaml`'s `computation:`, its top-level `description:` and
`frequency_formula.formula`; the self-corroborating `cross_checked_against:` rewritten to say the
source is the authority, not the agreement; a `derivation:` block added to `nco-timing.yaml`
`video_rates` naming which two entries divide exactly; and `nco-timing.yaml`'s note changed from a
list of special cases (1/3, 1/5, 1/10) to the general rule. Manual master
`manuals/p2-streamer-programming-guide/opus-master/streamer-body.md` corrected at all 8 values and
all 3 rule statements — **the workspace render was NOT edited; it regenerates from the master.**

**⚠️ OWED: a Streamer Guide re-release.** The corrected values are in the master; the published
v1.1.0 PDF still carries the 8 wrong ones. Scheduling that release is Stephen's.

---

## `ADDSX` and `SUBSX` ship the PASM2 Manual's wrong C-flag sentence while contradicting it in the same file (2026-08-27, «#328» E-016 sibling sweep) — F-379

### F-379 — the two instructions v1.11.1's signed-flag repair skipped, plus two malformed `SUM*` encoding fields — `RESOLVED`

**This is the outcome the E-016 sibling sweep existed to find: the manual is wrong AND our KB followed it.**

E-016 established that the PASM2 Manual's *prose* describes the signed-add/subtract C flag one way
while the manual's *own table on the same page* says something different and more precise, and that
the table is the more precise statement. `adds.yaml` and `subs.yaml` already rebut the prose. The
sweep found two siblings that do not:

| File | `description` said | its own `flags_affected.C` / `encoding[0].c` said |
|---|---|---|
| `language/pasm2/addsx.yaml` | *"the C flag is set (1) if the result is negative (Result[31] = 1)"* | `sign of (D+S+C)` |
| `language/pasm2/subsx.yaml` | the same sentence verbatim | `sign of D-(S+C)` |

**Each file contradicted itself**, and a reader who reads the `description` — the field a consuming
agent is most likely to surface — learned the wrong quantity. It is wrong in exactly the case that
matters: `Result[31]` and the true sign differ **only on overflow**, which is the condition `TJV`
exists to detect.

**Refuted three times inside the manual itself**, so this needed no external source: Table 9 at
`sources/pasm2-manual/pasm2-manual-text.txt:912` and Table 169 at `:3983` give the true-sign form;
the manual's own `TJV` description at `:4196` (restated `:5168`) says the jump *"requires that C be
updated (to the correct sign) by the previous ADDS / ADDSX / SUBS / SUBSX / CMPS / CMPSX / SUMx"* —
which could never fire if C were `Result[31]`; and the manual's summary tables at `:4482` and
`:4809` say **"correct sign"**.

**Root cause, and it is the useful part.** Commit `87511c99` (v1.11.1, *"signed flags"*) repaired
this exact class across `adds · cmps · cmpsx · subs · sumc · sumnc · sumnz · sumz` — **and skipped
`addsx` and `subsx`**. A class-wide sweep that misses two members leaves a defect that now looks
deliberate, because every neighbour is correct.

**Two further defects in the same family, found in the same pass and fixed with it** — both
column-split artifacts from the original CSV import, both in fields no gate reads:
`sumz.yaml` `encoding[0].z` read `1 then D = D - S, else D = D + S` — the *C column's condition
text* sitting in the Z field, where the manual's Table 172 (`:4039`) gives `Result = 0`. That one
was wrong, not merely malformed. `sumc.yaml` `encoding[0].c` carried the same condition prose welded
in front of a correct C semantic. `sumnc.yaml` and `sumnz.yaml` are clean — the four `SUM*` files
are asymmetric because v1.11.1 rewrote only two of them.

**Applied 2026-08-27.** All four corrected; `addsx`/`subsx` now carry the true-sign statement in the
wording `adds`/`subs` already use, each naming the manual table that overrides the prose and pointing
at E-016. `grep -rn 'Result\[31\] = 1' deliverables/ai/P2/` returns nothing outside the new
rebuttals.

**What no gate could see.** Every instrument in this project passed all four files throughout:
they parse, their keys resolve, their citations are present, and `pnut-ts` assembles the
instructions regardless — a compiler proves legality, never a flag's meaning. Only reading the
`description` against the same file's `flags_affected` catches a file disagreeing with itself.

## The KB ships the compiler's acceptance range as a frequency ceiling, 180 MHz past the silicon limit (2026-08-27, «#326» verification) — F-378

### F-378 — `_CLKFREQ range: "3,333,333 Hz to 500,000,000 Hz"` carries no silicon limit, and a remote agent will act on it — `CONFIRMED`

`deliverables/ai/P2/language/spin2/constants/special-configuration-symbols.yaml:59` gives `_CLKFREQ`
a `range:` of **3,333,333 Hz to 500,000,000 Hz**, sourced to the pnut-ts clock-configuration guide.
That figure is real, and it is the **compiler's acceptance range** — «#326» confirmed empirically
that `_clkfreq = 400_000_000` assembles clean, exit 0.

**The P2 Datasheet's AC Characteristics give the PLL absolute maximum as 320 MHz** (`3.33` min /
`180` typical / `320` max, `p2-datasheet-text.txt:2200`, with footnote 2 at `:2209` stating
*"Nominal PLL frequency (system clock speed) is 180 MHz at up to 105 °C"*).

**Why this is a defect rather than a difference.** The entry does not say which of the two it is
quoting. A remote agent reading only this entry — which is exactly how the shipped set is consumed
— will emit a `_clkfreq` up to 500 MHz, get a clean compile, and ship silicon running 180 MHz past
the datasheet maximum. Nothing anywhere in the path says otherwise: the compiler accepts it and the
KB's own stated range endorses it.

**This is E-007's rule, not a new one.** `SOURCE-ERRATA.md` E-007 settled that where two documents
frame a limit differently, the KB must **label which framing it is quoting**. That ruling was
applied to the clock limits in the Hardware Manual; it was never applied here.

**Fix.** Keep the compiler range — it is true and useful — and label it, adding the datasheet
ceiling beside it, the way «#326» did for `guides/pasm2-getting-started.yaml`
`timing_considerations.clock_frequency`. Sweep the same question across every `range:` in the
shipped set that came from a compiler guide rather than a datasheet.

**Related, and it must not be silently "corrected" back.** «#326» deliberately shipped `%01_11` for
the XI-input-plus-PLL clock mode where our own `spin2-v55-text.txt:1713` and `:1738` read
`01_1 1`. That space is **our extractor's**, not the source's: the arbiter confirmed against
`word/document.xml` that the value is one cell split across two Word runs, that it is the only one
of the nine so split, and that the literal `01_1 1` appears **nowhere** in the DOCX. Recorded in
`engineering/ingestion/sources/spin2-v55/spin2-v55-complete-extraction-audit.md`. A future pass that
"reconciles" the KB to the extraction would introduce a bit pattern that does not exist.

## Two residues the gates cannot see: a citation re-anchor that translated line numbers, and an eighth fabricated-provenance file (2026-08-27, «#325» verification) — F-377

### F-377 — F-365's re-anchor left locators that are in range and point at nothing; `io_pin_timing.yaml` cites a silicon-doc part file that does not exist — `CONFIRMED`

**Part 1 — the re-anchor residue.** F-365 moved 23 shipped citations from the superseded
`p2-documentation.txt` to `silicon-doc-text.txt`, and its own instruction was explicit: *verify each
against the new artifact; never translate line numbers.* Some were translated anyway.

`architecture/streamer/dds-goertzel.yaml:74` cites `silicon-doc-text.txt:1565 and :4062-4095`.
**`:1565` is correct** — it carries *"S[19:0] supplies a 20-bit value which is used to configure the
DDS/Goertzel mode"*. **`:4062` is a blank line.** The same file's `:303` cites `:1636` (`' Setup`,
plausible) and `:4289-4305`, where `:4289` reads `[t34 r3c1] %0000` — a table-cell marker, not the
mode/data longs claimed. `application-notes/p2an002…:103` carries two more of the same shape.

**No instrument can catch this, and that is the point.** A class-wide range check over every
`silicon-doc-text.txt:NNN` citation in the shipped set — **113 citations, file is 5626 lines** —
returns **0 out of range**. A translated locator lands inside the file and reads as valid to
anything that checks bounds. Only opening the line catches it. The suspect set is bounded and
small: the 23 citations F-365 moved.

**Fix.** Re-verify those 23 by *reading* each cited line and confirming it carries the content the
citing block claims — the discipline F-365 stated and did not fully execute. Where it does not,
locate the content in the artifact; do not adjust the number.

**Two more of the same shape, found by «#326» and confirmed by the arbiter — and note they are NOT
F-365 residue, which widens the class.** `architecture/clock_system.yaml`
`anti_patterns.conflicting_definitions.source` cites `spin2-v55-text.txt:1716-1725` for the
sentence *"These symbols must be defined in one of the following combinations"* — that sentence is
at **`:1709`**; `:1716` is the `_rcslow` table row. And `anti_patterns.missing_crystal_frequency.source`
cites `:1718` for the verbatim *"Selects XI/XO-crystal-plus-PLL mode, assumes 20 MHz crystal"* —
that is the `_clkfreq`-alone row at **`:1711`**; `:1718` reads *"No symbol and not DEBUG mode"*.
Both quotes are accurate, both locators point at a different row. `«#326»` also found the same
shape in the differential-read artifact it was handed (a datasheet footnote given as `:2205`, the
`Cin` Mode 3 row, where footnote 2 is at `:2209`).

**So the class is wider than F-365's 23.** Any citation written by translating a number rather than
locating content has this shape, whatever pass wrote it. The sweep should cover every
`spin2-v55-text.txt:` and `p2-datasheet-text.txt:` locator in the shipped set, not only the
re-anchored ones.

**Part 2 — an eighth fabricated-provenance file.** F-359 named seven `architecture/` files carrying
headers that cite silicon-doc part files which have never existed; one was purged and «#323»
re-derived the other six. **`architecture/io_pin_timing.yaml` is an eighth and was never in the
list.** It carries `# Silicon Doc Reference: part3-pins.txt, pages 5-8` at `:2` and
`"part3-pins.txt, Pin Timing Specifications"` at `:193`. The silicon-doc folder contains
`part3-end.txt`, `part3-interrupts.txt`, `part3-pages-37-38.txt`, `part4-locks.txt` and
`part4-smart-pins.txt` — **there is no `part3-pins.txt`**. Same defect, same mechanism: the header
satisfies the citation regex, so the sourcing gate reads the file as cited.

**Fix.** Re-derive it against `silicon-doc-text.txt` exactly as «#323» did the six, and collect
anything that cannot be re-derived rather than deleting it.

**Also repaired on the spot during this verification** (not deferred, one line):
`architecture/interrupts.yaml:27` asserted *"Each interrupt level has its own set of shadow
registers"* while `:43` of the same file, rewritten by «#323» from the source, states *"There are
no shadow register banks."* «#323» corrected the detailed block and left the summary paragraph
contradicting it. The summary now points at `automatic_state_save` instead of restating it.
A prose self-contradiction is invisible to every gate here — the encoding check that verified this
file cannot read sentences.

## The delivery filter strips `documentation_source:` from every file it serves, and 706 of those values are real citations (2026-08-26, «#324» verification) — F-375

### F-375 — a remote agent receives 383 of our files with their source line deleted, and the gate that checks the filter cannot see it — `CONFIRMED`

**The mechanism.** Both delivery paths run the same five-pattern line filter:
`engineering/tools/p2kb/fetch-kb-file.sh:189` and the `FilterMetadata` contract recorded in
`engineering/tools/p2kb-mcp/P2KB-MCP-SPECIFICATION.md`, designed in
`engineering/tools/p2kb/METADATA-FILTER-DESIGN.md`, which describes `documentation_source` as
*"Original doc reference"* — internal bookkeeping not worth shipping.

**That premise is false for the overwhelming majority of them.** Measured 2026-08-26 across all
1133 shipped files:

> **706 `documentation_source:` / `enhancement_source:` values are citation-shaped** — they name a
> document, an edition, a page or a line. **47 are the bare internal tokens the filter was designed
> for** (`enhanced` 16, `original` 15, `p2_datasheet` 8, `code_analysis` 2, and three singletons).
> The citation-shaped values sit in **383 distinct files**.

Examples of what is deleted on the way out:

| File | Value stripped in delivery |
|---|---|
| `language/spin2/assembly-directives/alignl.yaml` | `PASM2 Manual 2022/11/01 Pages 31-147` |
| `language/spin2/registers/pr-registers.yaml` | `PASM2 Manual 2022/11/01 Page 118` |
| `language/spin2/debug-commands/pc_key.yaml` | `Spin2 v51 (debug-section.txt) + PNut v55 directive matrix` |
| `language/spin2/statements/debug.yaml` | `PNut v55 compiler source (p2com.asm: check_word_chr_initial/check_word_chr @8888, debug_symbols table @19335, parse_debug_string, symbol_size_limit=30); hardware-isolated on real silicon 2026-07-27` |

**Why this is the sharpest form of a defect this project already knows.** The shipped set carries
the **agent-consumer** bar — *cite or omit*, because a remote agent cannot weigh a hedge and a
wrong fact becomes silently authoritative in generated code. The filter takes files that satisfy
that bar on disk and delivers them **not satisfying it**. Every gate we run reads the tree; the
consumer reads the filtered stream; nothing compares the two. The KB is cited. What we *serve* is
not.

**Second half, and it is why this was never caught.** `validate-dod-release.py`'s
`validate_metadata_filter` (lines 352-396) checks *which line-patterns the filter removes* and
never re-parses the filtered payload — there is no `yaml.safe_load` and no type comparison anywhere
in the function. «#324» proved the consequence: a block whose only child is `documentation_source:`
is delivered as `null`, and the check passes clean. **The filter is indentation-blind, so it can
destroy a block outright**, and the gate that exists to watch it is measuring the wrong thing.
*A gate must read the artifact* — this one reads the pattern list.

**Fix (two parts).**
1. **Filter:** stop deleting `documentation_source:` / `enhancement_source:` wholesale. Either
   deliver them, or delete only the 47 bare-token values and keep every citation-shaped one. The
   cleanest form is the one the project already uses everywhere else — rename the real ones to
   `source:` and let the filter keep its narrow meaning. That is 383 files, so it is a task.
2. **Gate:** `validate_metadata_filter` must re-parse the filtered payload and compare top-level
   types against the on-disk file, with a negative control that proves it fires. The `shape_probe`
   case from «#324» is a ready-made control.

**How this surfaced.** «#324» was measuring whether 34 YAML shape changes break any consumer. They
do not. But running the real fetch script against the real tree — rather than reading it — showed
what the delivery path does to files that were never part of the shape question at all.

---

## Two silent-failure bugs in the KB tooling (2026-08-26, «#324» verification) — F-376

### F-376 — `fetch-kb-file.sh -v <KEY>` fetches nothing and exits 0; the index generator swallows parse errors — `CONFIRMED`

Two unrelated bugs, same shape: **the failure is silent and the exit code is 0.**

**1. `engineering/tools/p2kb/fetch-kb-file.sh` double-shifts its verbose flag.** The
`--verbose|-v)` case runs `shift` at `:439`, and the argument loop shifts again at `:466`. So the
flag consumes the key that follows it: `fetch-kb-file.sh -v language/pasm2/add.yaml` drops the
key, fetches nothing, and exits 0. Any user or script that puts `-v` before the key gets silence
rather than an error. **Fix:** delete the `shift` inside the `--verbose|-v)` case.

**2. `engineering/tools/generate-p2kb-index.py` swallows every parse failure during alias
harvest** — the harvest ends `except Exception as e: # Silently skip files that can't be parsed /
pass` (~`:116`). A syntactically invalid YAML is still indexed with its path and sha256, silently
loses all of its aliases, and the run exits 0 printing nothing. Since `aliases:` is the mechanism
the whole KB's findability rests on, a file can go unfindable without anything saying so.
**Fix:** count and report skipped files, and fail the run if any file the index claims to cover
could not be parsed.

**Neither is in this sprint's repair scope** — both are tooling, and «#324» was a measurement task.
Recorded here so they are not rediscovered.

## The shipped set scores and star-rates hardware, which the KB entry rule excludes and no source authorises (2026-08-26, «#322» verification) — F-374

### F-374 — 40 quality-score sites across 18 shipped files state a judgement, not a fact — `CONFIRMED`

**The rule this violates** (Stephen, 2026-08-26, saved as `feedback_kb_entries_state_existence_access_utility`): a KB entry states **existence, access and utility**. Never quality commentary, never version comparison. It was given while re-scoping F-370, which had wanted to call ROM TAQOZ *"cut-down"* — and the same shape turns out to be spread across the hardware tree.

**Measured 2026-08-26 by walking every parsed node of all 1132 shipped files:**

| Key | Sites | Example value |
|---|---|---|
| `rating` | 13 | `5_stars_perfect`, `2_stars_limited`, `5_stars_professional` |
| `educational.value` | 8 | `high`, `very_high` |
| `educational_value` | 7 | `10`, `9` (under `quality_metrics`), `high` |
| `quality_rating` | 6 | `production`, `professional`, `specialized_excellent` |
| `recommendation_score` | 6 | `5` |

**40 sites, 18 files — 16 under `hardware/`, 2 under `code-examples/`.**

**Why this is a defect and not a style preference.** Two independent reasons, either sufficient:

1. **Nothing sources it.** `5_stars_perfect` and `recommendation_score: 5` trace to no Parallax document and no measurement. They are our opinion, shipped into a set whose bar is cite-or-omit. `audit-yaml-claim-sourcing.py` does not catch them because they carry no digits it recognises as a quantitative claim — a scoring adjective is an unsourced claim wearing a data key.
2. **The consumer cannot act on it.** `deliverables/ai/P2/` is read by remote agents generating code. An agent asked to pick a carrier board can do something with *"has 8 LDOs, one per 8-pin group"*; it can do nothing correct with *"5 stars"* except launder our preference into its own output as fact.

**Scope boundary — do NOT widen this sweep, and this half matters as much as the other.** The same rule *permits* utility, and the tree is full of legitimate utility statements that must survive untouched: `best_for` (6 sites), `recommendation` (20 sites, e.g. *"Use OBEX driver — do not attempt to implement HUB75 timing manually"*), and `advantages` (30 sites) all answer **what is this good for**, which is exactly the third thing an entry is supposed to state. A sweep that removes them replaces one defect with a worse one. The class here is **scores and ratings**, not guidance.

**Fix.** Per site, one of two: delete the key where the judgement carries nothing (`recommendation_score: 5` on three boards that all score 5 says nothing at all), or replace it with the sourced fact the score was standing in for — `quality_rating: production` on `edge-standard-module.yaml` is presumably reaching for something real about the module's intended use, and the board guide can say it properly.

**How this surfaced.** «#322» dropped a stray `educational_value: "excellent"` from `edge-breadboard-carrier.yaml` as a duplicate-key repair (F-360), noticed the surviving scalar was also bare quality commentary, and reported the pattern as corpus-wide. Arbiter verification measured it: a first pass matching the bare key `value` returned 299 sites and was thrown out as over-broad — most are legitimate — and the count above is the narrowed, defensible class.

## `validate-crossref-keys.py` exempts three top-level fields from resolving, and 14 shipped file paths sitting in them point at nothing (2026-08-26, «#321» verification) — F-373

### F-373 — `see_also`, `references` and `related_concepts` are typed `'text'`, so a file path in any of them is never resolved and the gate stays green — `CONFIRMED`

**Not F-340.** F-340 is the **nested-traversal** blind spot, and it is *disclosed on every run*:
the banner reads `✅ ALL TOP-LEVEL CROSS-REFERENCES RESOLVE — 692 nested site(s) NOT checked
(F-340)`. The sites here are **top-level and ARE traversed** — they are simply exempted from
having to resolve, and that exemption is disclosed nowhere. F-340's own text treats this typing
as the accepted baseline (*"should `related_documentation` be `'text'` like `see_also`?"*), which
is why it has never been filed as a defect in its own right.

**The mechanism.** `engineering/tools/validate-crossref-keys.py` `CROSS_REF_FIELDS` types
`'see_also': 'text'`, `'references': 'text'` and `'related_concepts': 'text'` (*"informational
only"*), and the resolver then does `if ref_type == 'text': continue`. A value in one of those
fields is never looked up, whether it is prose or an unmistakable file path.

**Measured 2026-08-26 over all 1132 shipped files.** 760 top-level values sit in the three
text-typed fields. 160 of them are path-shaped. Resolving each against the KB root, the citing
file's own directory, and the repo root, and setting aside 3 intentional globs
(`architecture/smart-pins/*.yaml`):

> **14 shipped `see_also:` file paths resolve to nothing, with the gate green.**

| Citing file | Value | Why it fails |
|---|---|---|
| `hardware/addon-motor-driver.yaml`, `addon-microsd.yaml`, `addon-hd-audio.yaml`, `addon-rtc.yaml` | `language/spin2/methods/_index.yaml` | no such file (4 sites) |
| `language/pasm2/concepts/labels.yaml` | `jmp.yaml`, `call.yaml`, `djnz.yaml`, `rep.yaml` | **bare names**; the files are at `language/pasm2/` |
| `language/spin2/symbols/streamer-symbols.yaml` | `../../architecture/streamer/modes-reference.yaml`, `…/dac-routing.yaml` | relative depth off by one — both targets exist |
| `language/spin2/methods/cogspin.yaml` | `concepts/multi_cog_synchronization.yaml` | no such file |
| `language/spin2/methods/pinstart.yaml` | `concepts/inline_pasm2.yaml` | no such file; the concept is in `language/spin2/constructs/inline_pasm.yaml` |
| `guides/spin2-getting-started.yaml`, `pasm2-getting-started.yaml` | `manifests/P2/language/*-manifest.yaml` | outside `deliverables/ai/P2/` entirely |

**This is a live negative control, not a hypothetical.** The gate exits 0 and prints
`ALL TOP-LEVEL CROSS-REFERENCES RESOLVE` while fourteen top-level references do not. The banner
is therefore wrong in a second way that F-340's disclosure does not cover, and
`validate-dod-release.py` inherits it. *A gate must read the artifact* — here it reads the
artifact and then declines to check what it read.

**Fix (two parts, neither is "delete the reference" — Sacred Rule #7).**
1. **Instrument:** resolve any text-typed value that is unmistakably a path (ends `.yaml`, no
   glob), leaving genuine prose alone; and say so in the banner, the way F-340's scope line does.
   A negative control is owed with it.
2. **Content:** repoint all 14. Most targets exist and only need the right path — bare names to
   full paths (Sacred Rule #7's stated form), the streamer pair one level up,
   `inline_pasm2.yaml` to `language/spin2/constructs/inline_pasm.yaml`. The `_index.yaml` and
   `multi_cog_synchronization.yaml` targets do not exist, so those redirect to where the content
   **is** documented.

**How this surfaced.** Dispatched work on «#321» reported the `'text'` typing as an out-of-scope
observation, proven by injection into a scratch copy. Arbiter verification replaced the injection
with a measurement of the live tree, which is what turned a design question into fourteen shipped
defects.

## Our USB smart-pin entry states as fact a sentence the DOCX edition dropped, and it contradicts the general WRPIN rule (2026-08-26, «#320» citation re-anchor) — F-372

### F-372 — `%11011` says a new WRPIN needs no reset; the same document's general rule says the opposite — `CONFIRMED`

**How this surfaced.** F-365's re-anchoring reads each stale citation's old target and finds that
content in the new artifact. Twenty-two of twenty-three matched. **One did not exist in the new
artifact at all**, which looked like an extraction defect and is not one.

**What the two editions actually say.** Both are labelled *Propeller 2 Documentation v35 (Rev B/C)*.

| | |
|---|---|
| **PDF-derived capture** `p2-documentation.txt:8886` | *"…will disable output drive and effectively create a USB 'sniffer'. **A new WRPIN can be done to effect such a change without resetting the smart pin.** NOTE: In Propeller 2 emulation on an FPGA…"* |
| **DOCX capture** `silicon-doc-text.txt:4579` | *"…will disable the output drive and effectively create a USB 'sniffer'. NOTE: In Propeller 2 emulation on an FPGA…"* — **the sentence is absent** |

The DOCX paragraph is not merely shorter; it is **differently written**, and it *adds* material:
`%HHH_LLL` drive modes are overridden alongside OUT, and *"The lower pin in the pair is DM, while
the upper pin is DP, per USB naming convention"* — neither of which the PDF version carries. The
heading differs too (`%11011 = USB host/device` vs `%11011 = USB host or device, full-speed
(12Mbps) or low-speed (1.5Mbps)`). **These are two revisions of one document, both claiming v35.**

**Why it matters beyond bookkeeping.** The dropped sentence **contradicts the general rule** this
same document states at `silicon-doc-text.txt:3856` and that «#319» just applied to
`architecture/smart_pins.yaml` as F-369: a WRPIN issued while DIR is high remaps 126 bits of state
underneath a running mode, producing *"unpredictable and quite certainly useless behavior"*, which
is why modes are configured only while DIR is low.

Two readings, and **documents cannot separate them**:

1. **USB is a genuine exception** — the sniffer change is a drive-enable flip rather than a mode
   change, so the multiplexing hazard does not apply, and the DOCX simply lost the sentence.
2. **The sentence was removed because it was wrong**, and the general rule governs `%11011` like
   everything else.

**Reached our KB?** **Yes — as settled fact.**
`architecture/smart-pins/smart-pin-11011-usb-host-device.yaml` `configuration.wrpin_data` ends with
the sentence verbatim, with no caveat, cited to the PDF-derived capture that is now superseded.

**Applied here:** the claim keeps its place — it may well be right, and deleting a plausible
documented behaviour is its own kind of damage — but it now carries the conflict, cites both
editions, and points at the gap. **Routed to `KNOWLEDGE-GAPS` as G-027: bench-testable and
jumper-only** — configure a USB pair, issue a new WRPIN with DIR high, and observe whether the pin
continues or breaks. That is the only thing that settles it.

## The sprint plan's "8 blocked sources" was wrong on five of them (2026-08-26, «#318») — F-371

### F-371 — a document-shaped-file test was applied to sources whose primary artifact is not a document — `RESOLVED`

**This is my own error, in the plan I wrote, and it materially misinformed the reader.** The
ingestion-backlog sprint plan told Stephen that **8 sources are blocked — "no primary document
staged"** and named them. The classification came from one test:

```
find <src> -maxdepth 1 \( -name '*.pdf' -o -name '*.docx' \)
```

That is a test for a **document-shaped file**. Five of the eight sources have a primary artifact
that is not a document, so the test returned nothing and the absence was read as *blocked*.

| Source | What it actually holds | Verdict |
|---|---|---|
| `rom-booter` | `ROM_Booter.lst` **411 KB** + `rom_booter_v33_01j.lst` **432 KB** | **not blocked** — needs audit + cross-source |
| `flash-loader` | `flash_loader.spin2` + a 38 KB Theory-of-Operations | **not blocked** — needs audit + cross-source |
| `pnut-ts-pasm-ref` | `PASM2-Instruction-Database.json` **322 KB** | **not blocked** — needs an audit rollup |
| `p2-qa-spreadsheet` | the `.xlsx` in `external-inputs/p2/`; **991 rows already extracted, audit present** | **not blocked** — needs cross-source |
| `quick-bytes-code` | 3 code archives + a `.spin2` | **not blocked, and mis-scoped** — a *community artifact* to catalogue, not a 7-pass ingestion |
| `p2docs-github-io` | narrative + validation report only | **blocked** — needs the site |
| `iron-sheep-compiler` | one condition-codes `.md` | **blocked** — needs compiler output |

**Two genuinely blocked, not eight.**

**The dashboard said so all along.** `rom-booter`'s note reads *".lst assembly; no audit /
cross-source"* and `p2-qa-spreadsheet`'s reads *"991 rows; audit present; no cross-source"*. **The
rows I was classifying already carried the answer**; the test I ran did not read them. A second
error compounded it — an inventory using `find ! -name '*.md'` hid `p2-qa-spreadsheet`'s extraction
and audit, because both are `.md`.

**Why this is filed rather than quietly corrected.** It is the same defect class this sprint kept
finding in the dashboard — **a number or a status produced by a check that was not measuring what
its label claimed**. F-250's `100% (stated)` over digit-free text, the PASM2 Manual's 64% measuring
the document rather than the capture, `quick-bytes-code`'s 15% grading a catalogue task on an
ingestion scale, and now a *blocked* label produced by a filename pattern. **Writing my own instance
of it into the same register is the only thing that makes the pattern visible as a pattern.**

**Fixed** in `engineering/ingestion/README.md` — a new *"What is actually outstanding, and what would
unblock it"* section gives each source its real primary artifact, what is genuinely missing, and
whether it needs anything from outside the repo. **Status `RESOLVED`:** the plan's claim is corrected
in the dashboard, which is what the next session reads.

## The TAQOZ author says ROM TAQOZ is an EARLY build, not just a cut-down one (2026-08-26, «#317») — F-370

### F-370 — `taqoz-forth.yaml` calls ROM TAQOZ "the finite, fixed version"; its author says it is also an **early** version — `RESOLVED`

**APPLIED 2026-08-26 («#319») — `RESOLVED`, and RE-SCOPED BY STEPHEN.** He ruled on this directly: *"do not put quality information like that in the [YAMLs]. All we want to know is that TAQOZ exists, how you get to it, and what it is useful for."* So the ROM-vs-RELOADED comparison this finding proposed — cut-down, early build, words may behave differently — **was NOT carried**, and the finding's original recommendation is superseded. What went in is the half that is utility: a `useful_for:` block giving the author's own guidance (use ROM TAQOZ for hardware debugging, especially when a larger environment will not load) plus what the resident interpreter is good for. The file already covered existence and access. Rule saved to auto-memory as `feedback_kb_entries_state_existence_access_utility`.

**How this surfaced.** The Bit Bashers Guide DOCX carries two reviewer comments, both anchored to
the same paragraph — the one marked *"(not in ROM)"*. A reader hit exactly that limit; **the author
of TAQOZ answered.**

| | |
|---|---|
| **[0]** Anonymous, 2023-03-30 | *"This did not work for me. I got `??? .D ???` instead of `--- 1234...`"* |
| **[1]** **Peter Jakacki**, 2023-04-06 | *"The ROM version is not only a cut-down version but also **an early version**. Use ROM version for debugging hardware etc especially when you can't seem to load the RELOADED version which can then be backed up to Flash or SD."* |

**Why the tier is high.** Peter Jakacki **is** the author of TAQOZ. For TAQOZ specifically he stands
where Chip Gracey stands for P2 silicon — this is designer testimony inside the document's own
review thread, not a forum lead.

**What our KB says** (`deliverables/ai/P2/architecture/boot-rom/taqoz-forth.yaml:47-50`):

> *"ROM TAQOZ is the finite, fixed version; TAQOZ Reloaded is the actively-developed environment.
> The two have different word sets."*

**Correct as far as it goes, and it misses the consequence.** "Finite and fixed" reads as *a subset,
frozen* — which invites the assumption that a word present in both behaves the same in both. The
author says ROM is also an **earlier build**. **A shared word may therefore differ in behaviour, not
just in presence**, and the KB's framing gives a reader no reason to suspect that.

**Fix (YAML head).** Carry the author's wording and its consequence into
`taqoz-forth.yaml`, cited to
`sources/TAQOZ-Forth-Bitbashers-Guide/reviewer-comments-harvest-2026-08-26.md`. Also worth carrying
his usage guidance, which is practical and nowhere in our tree: **use ROM TAQOZ for hardware
debugging, especially when RELOADED will not load.**

**The file's own chase plan is executable today, and nobody has run it.** Its
`knowledge_gaps.rom_vs_reloaded_word_diff` says *"Which specific words are in ROM TAQOZ vs. only in
TAQOZ Reloaded is not documented"*, with the chase *"Extract ROM dictionary from `ROM_Booter.lst`;
compare with TAQOZ Reloaded glossary"*. **We hold `ROM_Booter.lst`** —
`engineering/ingestion/sources/rom-booter/ROM_Booter.lst`, 411,535 bytes, **48 TAQOZ mentions**. The
first half of that chase needs no new source. Not run in this pass — this is an ingestion task and
the chase is YAML-head work — but recorded as **actionable now** rather than blocked.

## Two same-named Silicon Doc DOCX copies disagree, and the KB garbled a flag semantic from that passage (2026-08-26, «#314» pre-flight) — F-367 · F-368 · F-369

### F-367 — `external-inputs/p2/` and `sources/silicon-doc/` hold DIFFERENT documents under the same filename — `CONFIRMED`

**How this surfaced.** «#314» went looking for a PASM2 DOCX and found `external-inputs/p2/` holds
DOCX originals for several sources — **including a second copy of the Silicon Doc**, same filename,
different size (4,919,444 vs 4,814,991 bytes).

**Measured, not assumed.** Both carry 48 tables and 34 media, so a structural check calls them
identical. Extracting text from each and diffing says otherwise: **972 characters differ across 4
sites.**

| Site | `sources/` (the copy used for the 2026-08-26 re-extraction) | `external-inputs/` |
|---|---|---|
| GETBRK WZ | `Z = 1 if no … pattern queued (D = 0) or **0** if pattern queued (D <> 0)` | `… or **1** if pattern queued (D <> 0)` |
| smart-pin reset | **carries a full paragraph**: *"Once a smart pin is configured via WRPIN and then started by making its DIR bit high, it can be reset at any time by making its DIR bit low. It does not lose its configuration…"* | **paragraph absent** |
| PWM dither rationale | *"a maximum of only two adjacent 8-bit DAC levels are set for every 2…"* | *"a maximum of only two transitions occur for every 256 clocks"* |
| typo | `cog regis+ters:` | `cog registers:` |

**Which is right, and why it is decidable without a third source.** The `external-inputs/` GETBRK
line sets **Z = 1 in both branches**, which makes `WZ` useless and cannot be what the silicon does;
`sources/` gives `Z = 1 / Z = 0`, which is also the conventional Z semantic (`D = 0 → Z = 1`).
**The copy used for the re-extraction is the correct one**, and it additionally carries a paragraph
the other lacks. No prior work is invalidated.

**Why it still matters.** Two files with one name, differing on a flag semantic, is a silent
corruption waiting for whoever opens the wrong one. `external-inputs/p2/` is not a source folder and
carries no dashboard row, no audit and no trust tier — it is a staging area that has quietly become
a second, unlabelled copy of the corpus. **Disposition is Stephen's:** label `external-inputs/p2/`
as staging-only with a pointer to the canonical `sources/` copies, or reconcile the copies. Recorded
as **needs Stephen's accept-or-fix**.

**Also found there and NOT blocked as previously reported:** `Propeller 2 Questions & Answers.xlsx`
— the `p2-qa-spreadsheet` row sits at 80% and was listed in this sprint's plan as having *no primary
document staged*. It has one. That plan line is wrong and is corrected in «#318».

### F-368 — `getbrk.yaml` drops the Z value for the pattern-queued case, and declares `Z: No effect` for an instruction that requires a flag effect — `RESOLVED`

**APPLIED 2026-08-26 («#319») — `RESOLVED`.** The dropped branch is restored: `or 0 if a pattern IS queued (D <> 0)`. `flags_affected` no longer says `Z: No effect` for an instruction that requires a flag effect — it now carries a `note:` that GETBRK has no no-effect form, a per-flag description of what WC and WZ each select, and a `source:` at `silicon-doc-text.txt:2591`.

**The source** (`sources/silicon-doc/silicon-doc-text.txt`, GETBRK D WZ):

> `Z = 1 if no SKIP/SKIPF/EXECF/XBYTE pattern queued (D = 0) or 0 if pattern queued (D <> 0)`

**The shipped YAML** (`deliverables/ai/P2/language/pasm2/getbrk.yaml:36-37`):

> `- WZ: Z = 1 if no SKIP/SKIPF/EXECF/XBYTE pattern is queued (D = 0), or pattern queued if D <> 0.`

**The `0` is gone.** *"or 0 if pattern queued"* became *"or pattern queued if"* — which is not a Z
assignment at all. A reader learns what Z is when no pattern is queued and **nothing** about the
other branch, in the one sentence that exists to tell them.

**Second defect, same file:** `flags_affected: Z: No effect` (`:45`), while `:13` of the same file
states *"GETBRK REQUIRES a flag effect (WC, WZ, or WCZ)"* and `:36` describes what WZ does to Z.
The file contradicts itself.

**Fix (YAML head).** Restore the branch — `or 0 if pattern queued (D <> 0)` — and reconcile
`flags_affected` with the instruction's own requirement.

### F-369 — the smart-pin DIR-reset behaviour is in the Silicon Doc and carried nowhere in the KB — `RESOLVED`

**APPLIED 2026-08-26 («#319») — `RESOLVED`, and it carried more than the finding recorded.** Added `critical_requirements.reset_without_reconfiguring` to `architecture/smart_pins.yaml`. Reading the source paragraph in full turned up the **mechanism** behind a rule the KB already asserted without explaining: each smart pin holds **126 bits of state data** separate from its WRPIN configuration, and WRPIN *multiplexes* those bits to the subcircuit chosen by `%SSSSS`. Issuing WRPIN while DIR is high remaps them underneath live state — *"unpredictable and quite certainly useless behavior"*. So the existing *"configure only while DIR is low"* rule is a consequence of the multiplexing, not a convention, and that is now recorded as `why_this_is_the_rule`.

**The source:** *"Once a smart pin is configured via WRPIN and then started by making its DIR bit
high, it can be reset at any time by making its DIR bit low. It does not lose its configuration set
by the last WRPIN…"* (`sources/silicon-doc/silicon-doc-text.txt:3856`; this entry originally recorded `:3360`, which today reads `(X,Y) ROTATION` — corrected 2026-08-27 during «#328» verification. The shipped YAML always cited `:3856`, so nothing downstream inherited it).

**Measured:** `grep -rl` across all of `deliverables/ai/P2/` for `DIR bit low`, `reset at any time`
and `does not lose its configuration` returns **zero files**.

This is an operational fact a driver author needs — that a smart pin can be reset mid-flight without
re-issuing WRPIN — and it is one of the paragraphs the `external-inputs/` copy is missing, which is
plausibly why it never reached the KB. **Fix (YAML head):** carry it into
`architecture/smart_pins.yaml` with this citation.

## The TQFP-100 package drawing was in the Silicon Doc all along — G-021 closes, and G-019 was overstated (2026-08-26, «#312») — F-366

### F-366 — the shipped KB has no package-dimension record, and the source to write one has been in the repo unextracted — `RESOLVED`

**APPLIED 2026-08-26 («#320») — `RESOLVED`.** `deliverables/ai/P2/hardware/p2-package-mechanical.yaml`
now exists (commit `491d033b`), carrying the millimetre dimension rows off the ON Semiconductor
sheet with its aliases, and stating what the drawing does **not** give — there is no thermal data
on it, so **G-020 stays open**. The status flip was missed at the time and is made here during
«#321» verification: the artifact and its commit were checked directly, not taken from a closing
report.

**How this surfaced.** «#312» re-tested every source-silent verdict against the completed
silicon-doc extraction, because all of them were reached while the Tier-1 authority was 75%
ingested and contributing **none** of its 48 tables.

**G-021 is OVERTURNED.** `assets/images-silicon-doc-2026-08-26/silicon-034.png` is the ON
Semiconductor **MECHANICAL CASE OUTLINE / PACKAGE DIMENSIONS** sheet — **TQFP100 14×14, 0.5P, CASE
932BR, ISSUE O**, 03 JUL 2018, document **98AON94348G** — carrying the complete millimetre table.
Read off the rendered drawing twice (whole page, then the table at 3.5× zoom), both reads agreeing,
and **not OCR'd**: tesseract misreads digits on these sheets and these are precision values.

Full transcription is in
`engineering/analysis/2026-08-26-silicon-doc-retest-of-source-silent-verdicts.md`. Headline values:
`D`/`E` 15.80/16.00/16.20 · `D1`/`E1` 13.80/14.00/14.20 · `e` 0.50 BSC · `b` 0.17/0.22/0.27 ·
`L` 0.45/0.60/0.75 · `A` max 1.20 · `M` 0°–7°.

**What is owed (YAML head).** `deliverables/ai/P2/` has **no package/mechanical record at all**.
The dimensions are now sourced and citable; a record should be written and cited to this drawing.
This task does not edit shipped YAML, so it is handed over rather than applied.

**Also corrected, and this half matters as much.** **G-019 was overstated.** Its clause *"no
per-drive-mode current in mA anywhere in the corpus"* is false against the completed extract: the
drive ladder is stated outright at `silicon-doc-text.txt:206`, and **Table 30** gives digital
input-filter low-pass times computed in the document (`6.25ns × 32 × 3 = 600ns`). The *core* of
G-019 survives — `propagation delay`, `rise time`, `fall time`, `slew rate` all return zero hits,
and all 9 `ns` quantities were read individually and none is a pin-driver AC spec. But a register
row carrying a claim broader than its evidence is a false negative someone will later rely on, so
the row was corrected rather than left.

**Why this is filed as a finding and not just a gap update.** Two of the three re-tested gaps moved
because **the corpus was incomplete, not because the analysis was poor** — and Table 30, the thing
that corrected G-019, lives *inside a table cell*, which is exactly the content class that no
PDF-era capture could carry and that our own first DOCX pass flattened until «#310» fixed the
walker. **The lesson is about sequencing, not diligence: a "source is silent" verdict is only as
good as the extraction it was drawn against**, and this project now has a worked example of that in
both directions.

## 23 shipped-KB citations point into the superseded lossy silicon-doc capture (2026-08-26, «#310») — F-365

### F-365 — the shipped KB cites `p2-documentation.txt`, the PDF-era extraction now known to be lossy — `RESOLVED`

**APPLIED 2026-08-26 («#320») — `RESOLVED`.** All 23 citations re-anchored to
`silicon-doc-text.txt`, each verified by reading the old target and finding the same content in
the new artifact — line numbers were never translated. **Measured during «#321» verification:**
`grep -rn p2-documentation.txt deliverables/ai/P2/` returns **1**, down from **24 across 10 files**
at `36196329`. The one that remains is deliberate —
`architecture/smart-pins/smart-pin-11011-usb-host-device.yaml:19` names the superseded capture on
purpose, because F-372 / G-027 is precisely a conflict *between* the two captures of the same v35
document. The status flip was missed at the time and is made here.

**What was measured.** References to the superseded artifact, outside its own folder:

| Referencing | Count |
|---|---|
| shipped KB `deliverables/ai/P2/` | **24** — of which **23 carry `:line` locators** |
| other `deliverables/` | 3 |
| `engineering/` working docs | 266 |
| **total** | **293** |

**Severity, stated honestly rather than inflated.** The sampled shipped locators (`:188`,
`:3602`, `:3606`, `:3961`, `:3997`, `:3999`) were each read back 2026-08-26 and **all resolve to
content that matches what cites them.** These citations are **not broken**. This is lineage
hygiene, not a correctness emergency, and it should not be reported as though 23 facts were
wrong.

**Why it still matters.** The cited capture is PDF-derived, carries **zero of the document's 48
tables**, and splits code lines. It has already produced one wrong fact that reached the shipped
KB — **F-363**, the `$1F6`/`$1F7` PA/PB row — and the mechanism is visible in the artifact:
`p2-documentation.txt:907-908` are the bare token `CALLD-imm` alone, its table row shredded. A
citation into that capture is a citation into a source we now know drops structure silently.

**Fix (YAML head).** Re-anchor the 23 locators to `silicon-doc-text.txt`, verifying each against
the new artifact rather than translating line numbers — the two files do not share numbering, and
"verify citations live, not from a ledger" applies exactly here.

**The old artifact is deliberately NOT archived.** `ingest-source` §0.6 gates the archive-move on
first re-pointing downstream references; with 293 of them a move would strand every one, which is
a Sacred Rule #7 violation. Marked in place instead —
`engineering/ingestion/sources/silicon-doc/SUPERSEDED-BY-2026-08-26-DOCX.md`. The move happens
after this finding is worked, not before.

## The COG register map's PA/PB row lost the return-vs-parameter distinction, and its index dangles 13 of 16 pointers (2026-08-26, silicon-doc DOCX re-extraction) — F-363 · F-364

### F-363 — `complete-system-registers-index.yaml` says PA/PB hold the "CALLD-imm parameter"; all three authorities say **return** — `RESOLVED`

**APPLIED 2026-08-26 («#319») — `RESOLVED`.** `$1F6` → `CALLD-imm return, CALLPA parameter, or LOC address`; `$1F7` → `...CALLPB...`. Both rows now carry a `source:` naming all three authorities and a `note:` stating why the rows are deliberately not identical. **Citation drift caught while applying:** this finding cited `silicon-doc-text.txt:313-314`, which was the numbering BEFORE «#310» re-emitted that artifact; the live locations are `:452-453`, verified by reading them. The Hardware Manual (`:357`) and Datasheet (`:564-565`) locators were unaffected and re-verified.

**How this surfaced.** «#310» reconciled the prior PDF-era artifact `COG-RAM-REGISTER-MAP.md`
against the new DOCX extraction of the Silicon Doc. The `$1F6`/`$1F7` rows disagreed.

**What each source says.**

| Source | `$1F6` (PA) |
|---|---|
| **silicon-doc** (DOCX, 2026-08-26) `silicon-doc-text.txt:313` | `CALLD-imm return, CALLPA parameter, or LOC address` |
| **p2-hardware-manual** `p2-hardware-manual-text.txt:357` | `CALLD-imm return, CALLPA parameter, or LOC address` |
| **p2-datasheet** `p2-datasheet-text.txt:564` | `CALLD-imm return, CALLPA parameter, or LOC address` |
| **our shipped YAML** `complete-system-registers-index.yaml:73` | `CALLD-imm parameter, or LOC address` |

`$1F7` (PB) is the same, with `CALLPB`. **Three independent ingested authorities agree
verbatim, cell-identical, and the shipped KB disagrees with all three.**

**Two distinct defects in one line.**
1. **`return` became `parameter`.** PA holds the **return address** written by a `CALLD`
   with an immediate operand. Calling it the parameter inverts what the register receives.
2. **The `CALLPA`/`CALLPB` role was dropped entirely** — and with it the PA/PB distinction.
   Our two rows are byte-identical to each other; the sources' are not.

**Where it came from — the mechanism, not just the fact.** The prior PDF-era capture shredded
that table: `p2-documentation.txt:907-908` contain the bare token `CALLD-imm` alone on a line,
its row torn away. The prior artifact then reconstructed a plausible sentence from the fragment,
and the reconstruction is what shipped. **This is the F-250 class in a new place** — a lossy
extraction that reads as fluent, correct-looking prose. The DOCX capture keeps the row intact
because it carries real table structure.

**Reached our KB?** Yes — 2 sites, both in
`deliverables/ai/P2/architecture/system-registers/complete-system-registers-index.yaml`
(`:73`, `:79`). Class sweep for `CALLD-imm` across `deliverables/ai/P2/` returns exactly those
two. No other file carries the wording.

**Fix (YAML head, not this task).** `$1F6` → `CALLD-imm return, CALLPA parameter, or LOC
address`; `$1F7` → `CALLD-imm return, CALLPB parameter, or LOC address`. Triple-sourced, so no
further research is owed.

### F-364 — the same index advertises 16 register files; 13 of the pointers do not exist — `RESOLVED`

**What was measured.** Every `yaml_file:` pointer in
`complete-system-registers-index.yaml`, resolved against its own directory:

| | |
|---|---|
| pointers declared | **16** |
| resolve | **3** |
| **dangle** | **13** (11 distinct filenames) |

Missing: `dual-ijmp3` · `dual-iret3` · `dual-ijmp2` · `dual-iret2` · `dual-ijmp1` ·
`dual-iret1` · `dual-pa` · `dual-pb` · `ptrb-register` · `outa-outb-registers` (×2) ·
`ina-inb-registers` (×2). The directory contains exactly three files:
`complete-system-registers-index.yaml`, `dira-dirb-registers.yaml`, `ptra-register.yaml`.

**Why no gate caught it.** `validate-crossref-keys.py` exits 0 on this tree and has throughout.
It validates `related:` keys; **`yaml_file:` is a different pointer field and nothing checks
it.** So an index can promise thirteen files that were never written and every instrument stays
green — the same shape as F-362 (a register gate reporting CLEAN on entries it never read) and
F-359 (headers citing sources that do not exist). An agent following `yaml_file: dual-pa-register.yaml`
to resolve F-363's own defect would find nothing there.

**Disposition owed — this is a scope call, not a mechanical fix.** Either the eleven files get
written (they are real registers and deserve entries), or the pointers are removed and the index
carries the content inline. **Removing a pointer is not automatically Sacred Rule #7's forbidden
delete** — that rule protects a `related:` link to a concept documented *elsewhere*, and here
there is no elsewhere. But which way to go is {{USER_NAME}}'s call and is recorded as
**needs Stephen's accept-or-fix**, not decided here.

🟢 **RESOLVED 2026-08-26 («#323») — the thirteen dangling pointers were removed; the content
stays inline.** Writing eleven thin files would have put one fact in two homes, which is the
defect class this project keeps finding. **The index already holds everything a per-register file
would need** — address, normal use, special function, description, access, category and key
features — for every register it lists; that is now stated in `metadata.per_register_files`, so
anyone who later wants per-register files can generate them from this file without new research.
The three pointers that resolve (`ptra-register.yaml`, `dira-dirb-registers.yaml` ×2) were left
untouched.

Measured after: `yaml_file:` pointers across all of `deliverables/ai/P2/` — **3 declared, 3
resolve, 0 dangle**. The resolver was shown to be live by pointing one of the three at a
non-existent file, which it reported as DANGLE before being restored.

**Instrument gap, still filed:** whatever the disposition, `yaml_file:` pointers should be
resolved by a gate. Today nothing in the shipped tool set reads them — the resolution above was
done by an ad-hoc walker, not by an armed check. With 3/3 resolving, arming it is cheap now.

Status: `RESOLVED` — 13 dangling pointers removed, content kept inline, 3/3 remaining pointers
resolve. The instrument gap (no gate reads `yaml_file:`) remains open.

## The hygiene gate reports CLEAN on the register that owns the `G-`/`Q-` allocators while reading none of its entries (2026-08-26, p2-click-adapter ingestion) — F-362

### F-362 — `audit-register-hygiene.py` reports CLEAN on the register that owns the `G-` and `Q-` allocators while reading zero of its entries — `RESOLVED`

**How this surfaced.** The p2-click-adapter ingestion (2026-08-26) needed a new gap ID. Allocating
it by hand-reading the maximum `G-` in the table is exactly the two-writer collision the register
discipline exists to prevent, so the gate was run on `KNOWLEDGE-GAPS.md` to confirm the allocation.
It reported one violation (`no-counter`) and, once that was fixed, **CLEAN** — while its own summary
line read `findings : 0 entries, 0 distinct IDs` against a register holding **22 `G-` rows and 8
`Q-` rows**.

**What was measured.** `_ENTRY_HEAD` models exactly two entry dialects:

```
_ENTRY_HEAD = (r"^(?:#{2,4}\s+(<P>-\d+[a-z]?)\s*[—-]"      # heading form  (## F-001 — …)
               r"|-\s+\*\*(<P>-\d+[a-z]?)\s+[—-])")        # bullet form   (- **F-357 — …)
```

`KNOWLEDGE-GAPS.md` uses a **third** dialect exclusively — the markdown table row
(`| G-019 | Domain | … |`) — for both Part A gaps and Part B expert questions. Neither pattern
matches it, so `parse()` returns zero blocks and every per-entry check (duplicate IDs, status
presence, headline-vs-body agreement, ID coverage, orphaned sections) is skipped. Only the counter
check runs.

**Negative control — the proof, not the inference.** A duplicate `G-019` row was planted directly
beneath the real one in a copy of the register and the gate re-run:

```
$ python3 engineering/tools/validation/audit-register-hygiene.py <copy-with-planted-duplicate-G-019>
  next-ID counter   : G-23 (`Next gap ID`; no live G- entries)
  findings          : 0 entries, 0 distinct IDs
  CLEAN  …: no register-hygiene violations
  exit=0
```

**A duplicate ID in a register passes CLEAN with exit 0.** This is the same class as F-359 and the
`logic analyzer` misroute: the instrument answers with the wrong thing rather than nothing, and
"CLEAN" on an unread file is more dangerous than an error, because it is indistinguishable from a
verified pass. A prototype that adds the table-row alternative to `_ENTRY_HEAD` (plus
`m.group(3)` in `parse()`) makes the planted duplicate fire at **exit 1**, confirming the dialect
gap is the whole cause.

**Why the fix is not the one-line dialect add.** With entries visible, the status checks fire on
every row, because `STATUS_WORDS` is a single module-global tuple carrying the *corrections*
register's vocabulary. `KNOWLEDGE-GAPS.md` uses its own lifecycle — `OPEN` / `ANSWERED` /
`STILL-UNKNOWN` / `RELOCATED` / `PARTIAL` — and `OPEN` is **deliberately excluded** from
`STATUS_WORDS`, for a documented reason that is still correct: in the corrections register `OPEN`
is ordinary English prose (8 whole-word uppercase occurrences), and admitting it globally would let
a finding carrying **no** status pass check 4 on a stray word. So the real fix is a **per-register
status vocabulary**, selected the way the ID families already are — read off the counter label the
file declares (`Next gap ID` vs `Next finding ID` vs `Next erratum ID`) rather than hard-coded.
The hook exists: `main()` already rebuilds `FINDING_START` / `ID_RANGE` / `ID_ONE` / `GUARD_RE`
per register from `COUNTER_RE`; `STATUS_RE` needs to join them.

**Scope note.** Deliberately **not** applied in the p2-click-adapter commit. Widening a
module-global status vocabulary that 85 live findings are graded against is a regression surface
that wants its own verification pass (baseline captured: all three registers exit 0, the tool's
`--negative-control` suite passes 13 checks), not a bolt-on at a release boundary. What WAS fixed
in that commit is the allocator defect this finding surfaced — see below.

**Fixed alongside (allocator ownership).** `KNOWLEDGE-GAPS.md` declared **no** counter at all, and
`P2KB-CORRECTION-FINDINGS.md` declared `Next gap ID: G-008` — **stale by fourteen** against the
gaps register's actual `G-022`, and a second register claiming an allocator it does not own. F-352
caught the smaller instance of this same drift (`G-007`) and corrected the number rather than the
ownership, so it recurred. Now: `KNOWLEDGE-GAPS.md` declares `Next gap ID: G-023` ·
`Next expert-question ID: Q-009` and states outright that it owns the `G-` and `Q-` allocators;
the corrections register's duplicate `Next gap ID` clause is retired with a pointer to it. All
three registers exit 0 under the gate afterwards.

**Status:** `RESOLVED` — fixed and verified 2026-08-27 («#327»). Three shapes the tool did not
model, all repaired in `engineering/tools/validation/audit-register-hygiene.py`:

1. **The table-row entry dialect.** `_ENTRY_HEAD` gained `| G-019 | … |`, and `parse()` now also
   returns each row's **status CELL**, located from the table's own `Status` / `State` column
   heading. The cell, not the row, is what the status checks read — because the ledger's own
   lifecycle word `open` is *also* ordinary English in its prose ("_Still open:_ …"), so a
   vocabulary carrying it, searched over a whole row, would have made check 4 unfailable and
   re-created this very finding in a new costume.
2. **Per-register status vocabulary**, selected off the counter label exactly as the ID families
   already were. `OPEN` **stays excluded** from the corrections vocabulary; the ledgers get their
   own (`OPEN` · `ANSWERED` · `STILL-UNKNOWN` · `RELOCATED` · `NARROWED` · `PARTIAL` · `RESOLVED` ·
   `ASKED`, case-folded, with `sweep=False` because a moving ledger keeps an answered row on
   purpose). An unknown label falls back to the corrections vocabulary, which fails loudly on a
   foreign lifecycle rather than passing it.
3. **An ID family is a prefix string, not a letter** — so the P1 quad's namespaced `F-P1-` /
   `G-P1-` / `Q-P1-` allocators parse. Those two registers also declared `**Next ID:`** with no
   `<thing>` word; they were corrected to the convention rather than the pattern loosened, because
   the label now *selects the vocabulary*, and `P1-KNOWLEDGE-GAPS.md` had written that same
   nameless counter twice in one file for two different families. The gate still refuses the
   labelless form — proven by a control case.

**Proof, both directions.** The planted-duplicate `G-019` fixture passes **CLEAN at exit 0**
through the pre-fix tool (read out of `.backups/`, which reports `0 entries, 0 distinct IDs`) and
**fails at exit 1 with `duplicate-id`** through the fixed one. Five registers now exit 0 with the
gate actually reading them: corrections **102 live / 294 archived / 0 unaccounted** (unchanged),
`SOURCE-ERRATA` **17 live** (unchanged), `KNOWLEDGE-GAPS` **36 live** (was `0 entries`),
`P1-CORRECTION-FINDINGS` **0 entries, counter governed** (was exit 1), `P1-KNOWLEDGE-GAPS`
**14 live** (was exit 1 and `0 entries`). `--negative-control` carries **11 new permanent cases**
(24 total), including the planted-duplicate shape itself, a blank status cell, a status word in a
row's prose with the cell blank, two families on one counter line, and both sides of the `OPEN`
exclusion.

**Surfaced but NOT filed** (allocator belongs to the sprint arbiter): the corrections register
carries a third ID series, `ENH-NN`, with **no declared counter** — and live `ENH-02` / `ENH-03`
name different proposals than the archived `ENH-02` / `ENH-03` in
`correction-sweeps/2026-08-15-…-archive.md`, i.e. the allocator has already collided across the
archive boundary. The gate deliberately does not model that family (doing so turns it red over a
defect whose remedy is renumbering live entries), but it now prints an `unmodelled series :
ENH-NNN` report line on every run so the question surfaces instead of staying silent.

## `pin-selection.yaml` printed the streamer's sub-pin table with the wrong bit weights, and shipped the EF-065 trap as its worked example (2026-08-26, found while composing the streamer pin-capture page) — F-361

- **F-361 — Two defects in `deliverables/ai/P2/architecture/streamer/pin-selection.yaml`: a
  `sub_pin_selection` table that contradicts both the Silicon Doc and the bench, and a
  `pin_base_encoding` example that is the EF-065 misalignment trap written out for a reader to
  copy.** — `PENDING-VALIDATION` (both fixed 2026-08-26; a direct bench check of the sub-pin
  weights is arm B of VO-J-005 and has not been run)

  **Defect 1 — the sub-pin table.** The block stated `field: "D[19:17] within mode config"` and then
  gave a **dense slot** mapping: for 2-pin modes `%001 = Pins 3..2`, `%010 = Pins 5..4` … `%111 =
  Pins 15..14`; for 4-pin modes `%001 = Pins 7..4` … `%111 = Pins 31..28`. Both columns are wrong,
  and wrong in a way that matters: they imply a 4-pin capture can be based anywhere in a 32-pin
  window, which is exactly the belief that produces a misaligned base.

  **What the sources say.** Propeller 2 Documentation v35: *"In every mode, the three %ppp bits in
  D[22:20] select the pin group, in 8-pin increments"*
  (`engineering/ingestion/sources/silicon-doc/p2-documentation.txt:3606`) and *"For modes which
  involve less than 8 pins, lower-order %p bit(s) in D[19:19..17] are used to further resolve the
  pin number(s)"* (`:3653`). So the pin number is ONE six-bit field at D[22:17] — `pin << 17` —
  and D[19:17] is `pin & 7`, not a slot index. The Spin2 v55 streamer symbol table states the same
  thing per mode, as the bit templates themselves:
  `X_1P_1DAC1_WFBYTE %1100_DDDD_WPPP_PPPA`, `X_2P_2DAC1_WFBYTE %1101_DDDD_WPPP_PP0A`,
  `X_4P_4DAC1_WFBYTE %1110_DDDD_WPPP_P00A`, `X_8P_4DAC2_WFBYTE %1110_DDDD_WPPP_0110`
  (`engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt:1608-1613`). The fixed zeros at
  D[17] and D[18:17] ARE the alignment rule, stated by encoding.

  **The bench already agreed with the sources, in two mode families.** EF-064: a 1-pin mode with
  `20<<17` drove **P20 exactly**. EF-065: an 8-pin mode with `+ 20<<17` drove **P24..P31** — the
  carry model, not the slot model. Under the table's dense reading neither result follows.

  **Defect 2 — the worked example.** `pin_base_encoding.example` read
  `mode := X_RFBYTE_8P_1DAC8 | X_PINS_ON + 20<<17 + count`: an **8-pin** mode at a base that is not
  a multiple of 8, composed with `+`. That is EF-065 verbatim, in a third mode family, printed as
  the line a reader copies. Assembled with `pnut-ts` v1.55.3 to check rather than assert:

  ```
  X_RFBYTE_8P_1DAC8 | X_PINS_ON + 20<<17 + $FFFF   ->  $A0B6_FFFF
  X_RFBYTE_8P_1DAC8 | X_PINS_ON | (16<<17) | $FFFF ->  $A0AE_FFFF
  X_RFBYTE_8P_1DAC8 | X_PINS_ON | (20<<17) | $FFFF ->  $A0AE_FFFF
  ```

  `$A0B6_FFFF` is D[19:16] = `%0110` (**X_RFBYTE_8P_4DAC2**, a different mode) at D[22:20] = `%011`
  (**P24..P31**, a different group). And the third line is the other half of EF-065: with `|` the
  misaligned base is **byte-identical** to base 16 — it does not carry, it silently vanishes. Both
  compile clean.

  **Applied 2026-08-26.** `sub_pin_selection` rewritten to state the rule and the per-width free
  bits by encoding, with a worked mapping only for the 1-pin case (the one width where all three
  bits are free and no mode caveat applies), plus a `what_a_misaligned_base_does` pointer.
  `pin_base_encoding` now carries the alignment rule, the composition rule, an **aligned** example,
  and both failure modes with their assembled words. `common_configs` re-composed with `|` and each
  base annotated with the rule it satisfies. The file also gained a `source:` (it had none) and the
  capture-path facts this sprint's Section B added.

  **What is still owed.** A bench confirmation of the 2-pin/4-pin sub-field weights specifically.
  EF-064/EF-065 cover the 1-pin and 8-pin families; the 4-pin family is **arm B of VO-J-005**
  (`engineering/ingestion/external-sources/hardware-verification/VERIFICATION-OPPORTUNITIES.md`),
  which captures at base 12 against two distinct static pin patterns and names the reversing
  outcome: if the buffer returns the P8..P11 pattern rather than the P12..P15 pattern, this finding
  is backwards and must be reverted before anything built on it ships.

## Duplicate YAML keys silently destroy content, and no gate can see them (2026-08-25, found by the release-review change ledger) — F-360

- **F-360 — Five duplicate-key sites in the shipped set discard a block's content at parse time,
  and `verify-yaml-format.py` passes every one of them because duplicate keys are legal YAML.** —
  `RESOLVED`

  **The mechanism.** YAML resolves a repeated key by **last-one-wins**, silently. The earlier
  block is not merged and not flagged — it simply does not exist for any consumer. `yaml.safe_load`
  succeeds, so a format gate that asks *"does this parse?"* answers yes. **This is a check that
  cannot fail**, and it was proven so rather than assumed: planting `test_dup: 1` / `test_dup: 2`
  into `architecture/locks.yaml` left `verify-yaml-format.py` at **exit 0**.

  **Found on the arbiter's own work first.** `architecture/pin-drive-configuration.yaml` — the file
  «#295» created as the single definition home for the fact this whole sprint turns on — carried a
  duplicate `note:` under `idioms:`. It was introduced **by the arbiter** hours earlier, while
  correcting the EF-063/EF-064 attribution: `gap_no_dedicated_bench_test:` was written with no
  indented body, so its intended children became siblings, and the new `note:` collided with
  `idioms.note`. **What was destroyed was the corrective sentence itself** — that `%M..M` selects
  drive strength, that the Pin Mode Legend contains no bias-resistor selector, and that the two
  idioms below are hardware-verified rather than documentary. A consumer parsing the file got the
  gap note in its place. **Fixed** (restructured as a proper nested mapping; `idioms.note` restored,
  0 duplicates in that file).

  **Four more are pre-existing and still stand.** Swept all **1130** shipped YAMLs:

  | File | Duplicate key | What is discarded |
  |---|---|---|
  | `architecture/lookup_ram.yaml:90` | `operation` | an entire block-scalar description |
  | `architecture/lookup_ram.yaml:93` | `usage_example` | an entire worked example |
  | `hardware/edge-breadboard-carrier.yaml:174` | `educational_value` | a **structured block**, replaced by the scalar `"excellent"` |
  | `language/pasm2/drvl.yaml:4` | `timing` | a `timing:` block on a PASM2 instruction, where timing is load-bearing |

  **NOT FIXED — deliberately, and this is a decision for Stephen at the release review.** Resolving
  each is a content judgement (which of the two blocks is the intended one), and **arming a
  duplicate-key check would turn the release red on four pre-existing files.** Doing that silently
  at the gate is the same move this sprint spent itself repairing. His options: fix the four and
  arm, arm and accept the red until they are fixed, or ship and schedule both.

  **The "lack".** The format gate asks whether a document *parses*, which duplicate keys do. Nobody
  asked whether it *says what it appears to say*. Sibling to F-335's family — an instrument
  answering a narrower question than its name implies — and to the standing lesson that a gate must
  read the artifact rather than a property of it.

  **Recommended repair when it is armed:** duplicate-key detection belongs in
  `verify-yaml-format.py` (it already loads every file), as a distinct violation class, with a
  negative control that plants a duplicate and requires a non-zero exit.

  **RESOLVED 2026-08-26 — gate armed, all sites fixed, and the count was wrong.** The gate shipped
  as its own instrument, `engineering/tools/validation/audit-yaml-duplicate-keys.py` (armed in
  `02ff61b7`), not folded into `verify-yaml-format.py`. Armed, it found **3 files / 4 sites**, not
  the five this finding recorded: the `pin-drive-configuration.yaml` site was already fixed, and
  the node-tree walk found nothing the manual sweep had missed. `deliverables/ai/P2` now returns
  **0 duplicate keys across 1132 files**.

  **In every one of the four, the surviving value had to be adjudicated — and in two of them the
  value consumers see today was the wrong one:**

  | Site | Kept | Why |
  |---|---|---|
  | `architecture/lookup_ram.yaml` `operation` (90 vs 98) | the **earlier**, discarded block | Lines 98-114 were the orphaned body of a **removed** pseudo-instruction for LUT-to-DAC streaming: its `- instruction:`/`encoding:`/`description:` header had been replaced by a comment, leaving `operation:`/`usage_example:` to be absorbed into the **SETLUTS** entry above and overwrite it. Consumers were reading streamer setup as SETLUTS's operation. SETLUTS's own content restored; the orphan deleted (its substance is already carried, with correct constant names, by `programming_patterns.waveform_generation` and `architecture.special_features` (feature: `LUT_to_DAC_streaming`) in the same file). |
  | `architecture/lookup_ram.yaml` `usage_example` (93 vs 102) | the **earlier**, discarded block | Same orphan, same repair. |
  | `hardware/edge-breadboard-carrier.yaml` `educational_value` (174 vs 205) | the **earlier**, structured block | The scalar `"excellent"` that was winning is also bare quality commentary, which the KB entry rule (existence / access / utility) excludes. Dropped. |
  | `language/pasm2/drvl.yaml` `timing` (4 vs 35) | the **earlier**, richer block | The later block was a strict subset (`cycles`/`type`); the earlier one additionally carried `pin_output_latency`. The discarded block is byte-identical to the one that is **live** in its twin `drvh.yaml`, so DRVL and DRVH were silently disagreeing about pin timing. The claim is sourced — P2 Documentation v35 Rev B/C (`silicon-doc-text.txt:1987`) and the P2 Hardware Manual (`p2-hardware-manual-text.txt:967`) both state the three-clock DIRx/OUTx transition delay — and that citation was added to **both** twins, which carried the claim uncited. |

  **Still open, and it is the same class of lack this finding is about:** the armed gate is **not**
  wired into `validate-dod-release.py`. That validator runs 11 checks and calls two sibling audits
  (`audit-constant-fidelity.py`, `audit-claim-sourcing.py`) as blocking gates; the duplicate-key
  audit is not among them, so a duplicate reintroduced tomorrow turns nothing red at release. The
  gate exists and passes — but nothing makes it run.

  Status: `RESOLVED` — 4/4 sites fixed, gate armed and returning 0; wiring it into
  `validate-dod-release.py` remains open.

---
## The bulk-generation commit wrote FABRICATED PROVENANCE HEADERS, and those headers are what make seven `architecture/` files look cited (2026-08-25, Stephen's question at the release review) — F-359

- **F-359 — Seven `architecture/` files carry a provenance header citing source files that have
  never existed and datasheet pages beyond the end of the datasheet; the header itself satisfies
  the citation regex, so six of the seven still pass the gate today.** — `RESOLVED`

  **How it surfaced.** Stephen asked whether `io_pin_timing.yaml`'s content might have come from
  our own I/O & Smart Pins manual rather than a Parallax source — i.e. whether the provenance was
  circular. **The answer is no, and the truth is worse.**

  **The timeline rules the manual out.** `io_pin_timing.yaml` was created **2025-11-29** in
  `e271cab0`; the IOSP manual's first commit is **2026-01-25**, nearly two months later. Causality
  therefore runs **KB → manual**, not manual → KB. Where that manual repeats the drive-strength
  mislabel (F-356), it most likely **inherited it from this file**, which inverts the assumption
  behind the post-release manual review.

  **Nor did it come from what it cites. Every citation in the header is false:**

  | Header line | Reality |
  |---|---|
  | `Silicon Doc Reference: part3-pins.txt` | **no such file has ever existed** (nor `part1-cog.txt`, nor `part3-smartpins.txt`, nor `part2-cog.txt`) |
  | `Datasheet Reference: pages 42-45` | those pages are the **PASM2 instruction listing** |
  | `Datasheet Reference: … 76-78` | **the datasheet is 50 pages** |
  | `Layer 1: Direct extraction from Silicon Doc v35 and P2 Datasheet` | the values (`2.5/3.5/5.0 ns`, the mA ladder, "slew") appear **zero times** in any ingested source |

  **It is a class of seven, and we purged one.** All seven were written in the same commit —
  `e271cab0`, 2025-11-29, *"Implement DOD v3.0"*, which touched **1,323 files and 973 YAMLs in a
  single commit**. Each carries the same header shape, each names a non-existent silicon-doc file,
  and **each cites a second datasheet range beyond page 50**:

  | File | Cites | Impossible page range | Quantities today |
  |---|---|---|---|
  | `architecture/io_pin_timing.yaml` | `part3-pins.txt` | 76-78 | purged this sprint |
  | `architecture/cog_attention.yaml` | `part1-cog.txt` | 73 | 0 |
  | `architecture/debug_interrupt.yaml` | `part1-cog.txt` | — | 0 |
  | `architecture/event_system.yaml` | `part1-cog.txt` | 74-75 | **6** |
  | `architecture/interrupts.yaml` | `part1-cog.txt` | 71-72 | **2** |
  | `architecture/locks.yaml` | `part1-cog.txt` | 82 | 0 |
  | `architecture/lookup_ram.yaml` | `part1-cog.txt` | 67-68 | **1** |

  🔴 **THE MECHANISM — the fabricated header IS the citation that silences the gate.** Measured
  against `audit-yaml-claim-sourcing.py`'s own regex: all three header forms return
  `INLINE_CITE = True`, because the matcher fires on the tokens *"Silicon Doc"* and *"Datasheet"*
  wherever they appear. **A header that invents its sources reads to the instrument exactly like a
  header that names real ones.** This is F-335's pattern — the citation side matching on the
  presence of a token rather than on whether the sentence attributes the block to a document —
  applied to the KB's original sin rather than to a later edit.

  **Consequence for the release, stated plainly:** at least **9 quantities** across three of these
  files stand under a header citing a file that does not exist, and the current `0 Tier 1` does not
  contradict that — the gate is satisfied by the fabrication. `io_pin_timing.yaml` was caught only
  because it *also* had blocks with no header coverage at all.

  **The "lack" this traces to.** Nothing checked generated content against a source at creation
  time, and **the citation header was generated along with the content it claims to source**. A
  fabricated citation is not an error in sourcing; it is the signature of never having sourced.
  973 YAMLs in one commit is the scale at which that becomes invisible.

  **NOT FIXED — this is a scope decision Stephen owns**, raised at the release review he called
  for. Purging six more files is a widening at the gate, and the release is his call. Options are
  his: purge the class now, ship and schedule it, or re-derive those six from the real sources.
  What must NOT happen is shipping while believing the `0 Tier 1` covers them.

  🟢 **RESOLVED 2026-08-26 («#323») — the third option was taken: all six re-derived from the
  real sources.** The silicon doc is now fully extracted, which is what made this tractable;
  every claim below was read off `sources/silicon-doc/silicon-doc-text.txt` or
  `sources/p2-datasheet/p2-datasheet-text.txt` live, and every citation written into the six
  files was then re-read at the line it names.

  **What the re-derivation actually found is worse than the header.** The fabricated citation was
  the signature, not the extent. Across the six files:

  | | Before | After |
  |---|---|---|
  | `- instruction:` entries carrying an `encoding:` | 47 | 45 |
  | encoding **verbatim-identical** to the silicon doc's PASM2 encoding table | **2** (`RDLUT`, `SETSE1`) | **45** |
  | encoding **wrong** | **41** | **0** |
  | mnemonic **not in the encoding table at all** | **4** | **0** |

  The four absent mnemonics are `RDCOGID`, `RDLUTS`, `NIXINT0` and `TRGINT0`. Each was checked
  three ways: absent from `silicon-doc-text.txt`, absent from every other file under
  `deliverables/ai/P2/`, and not accepted as an instruction by pnut-ts v1.55.3 (`nixint0` and
  `trgint0` assemble to a zero-byte binary because the compiler reads them as labels; `rdcogid`
  and `rdluts` are hard errors). The four RETIx encodings come from this knowledge base's own
  `language/pasm2/reti0..3.yaml`, since RETIx are CALLD aliases and appear in the silicon doc as
  alias definitions (`:5483-5486`) rather than as encoding-table rows.

  Plus these semantic inversions, each of which a code-generating agent would have acted on:
  * `interrupts.yaml` had the **IJMPx/IRETx address map inverted** — it called `$1F0` IJMP1 where
    three authorities (silicon-doc `:2296-2301`, datasheet `:558-563`, and the RETIx alias
    definitions at silicon-doc `:5483-5485`) all say `$1F0` is IJMP3.
  * `interrupts.yaml` claimed **per-level shadow registers** for PA/PB/PTRA/PTRB/Q. There are
    none; the CALLD dispatch saves the return address and C/Z into IRETx and nothing else
    (silicon-doc `:2294`, `:2359`).
  * `lookup_ram.yaml` had **LUT sharing backwards** — it described reading the neighbour's LUT.
    Sharing is a WRITE path into the paired cog's LUT (silicon-doc `:491-500`). It also had
    **WRLUT's operands reversed** (D is the data, S is the address).
  * `locks.yaml` carried a `LOCKTRY (WC mode)` entry meaning "check the owner without acquiring".
    LOCKTRY always attempts to take, and C=1 means *taken* (silicon-doc `:3688`); the query form
    is LOCKREL with WC and a register D (`:3700`).
  * `cog_attention.yaml` had **ATN as event 15**; it is event 14 (`:2053`, `:2290`), and both
    SETINTx examples used the wrong number. Its `setup_for_event` configured SETSE1 for
    attention, which SETSEn cannot select at all (`:2246-2260`).
  * `debug_interrupt.yaml` invented three **"configuration registers"** (BRK as a register with a
    `[31:20]` flags field, plus SKIP and SKIPF as debug registers). BRK is an instruction whose D
    operand is `%aaaaaaaaaaaaaaaaeeee_LKJIHGFEDCBA` (`:2498-2517`), and GETBRK reads cog status
    in three forms rather than reading back a break configuration (`:2527-2593`).
  * `event_system.yaml` carried an invented event taxonomy ("Edge-detect", "IN-rise",
    "CORDIC-done") in place of the sixteen the source enumerates (`:2037-2054`), and its
    pattern-match example selected **mismatch** mode while its comment said match — SETPAT reads
    C and Z as inputs, and takes no WC/WZ effect (confirmed against pnut-ts).

  **The header was replaced in both places it lived** — the leading comment block AND
  `extraction_metadata.source_documents`, which carried the same `part1-cog.txt` and the same
  impossible page ranges. Each file now names the real document, the real section, and a live
  line range, and carries a `re_derivation_note` stating what was corrected.

  ⚠️ **THE GATE IS STILL NOT THE EVIDENCE.** `audit-yaml-claim-sourcing.py` read `0 Tier 1`
  before this work and reads `0 Tier 1` after it, because none of the six carries a
  unit-bearing quantity block. That green says nothing about whether these files are cited; the
  evidence is that every `<file>:<line>` written into them was re-read at the line it names. The
  instrument was separately shown to be live on these files: a planted two-quantity block in
  `locks.yaml` produced `TIER 1 ... 1 violation` and exit 1, and removing it returned exit 0.

  **Eight claims could NOT be re-derived and were NOT deleted — deletion is Stephen's.** Each was
  searched for in the silicon doc, the datasheet and this KB's own per-instruction YAMLs before
  being listed:
  1. `locks.yaml` `architecture.state_bits: 4` with the comment "3 bits COG ID + 1 bit owned
     flag". No source gives a lock any internal bit-width; both authorities say only "16
     semaphore bits" (silicon-doc `:3674`, datasheet `:878`).
  2. `lookup_ram.yaml` `performance_characteristics.power_consumption` (active "similar to COG
     RAM access", idle "static power only"). Zero hits for LUT power in either document.
  3. `lookup_ram.yaml` `bandwidth.streaming: "32 bits per clock (via streamer)"`. That figure is
     the **hub RAM** rate (silicon-doc `:2999`, `:3003`); nothing states it for a LUT-sourced
     streamer.
  4. `lookup_ram.yaml` `bandwidth.internal: "32 bits per 2-3 clocks"` — a restatement of the
     RDLUT/WRLUT timings as a bandwidth, which no source makes.
  5. `debug_interrupt.yaml` `memory_usage.trace_buffer: "Typically 4KB-16KB in hub"`.
  6. `debug_interrupt.yaml` `memory_usage.debug_state: "~100 longs for full state capture"` —
     the source describes 16 longs saved by the ROM routine and 64 bytes per cog per area.
  7. `debug_interrupt.yaml` `limitations.streamer_interaction: "Debug can disrupt streamer
     operations"`. The source makes the opposite kind of claim about the hub FIFO — the scheme
     runs in cog register space precisely so it does *not* disturb it (`:2484`) — and says
     nothing about the streamer.
  8. `cog_attention.yaml` `performance_characteristics.response_latency.waiting: "0 clocks after
     signal arrives"`. The datasheet gives WAITATN as `2+` (`:1914`).

  Not listed above, and deliberately: the `programming_patterns`, `common_applications`,
  `best_practices` and `debugging_tips` sections of all six files are authored guidance rather
  than source claims. They were corrected wherever they encoded one of the defects above (wrong
  event number, fabricated mnemonic, inverted sharing direction, mismatch-mode SETPAT), and
  otherwise left alone.

  **Fabricated NAMES were deleted rather than escalated**, under Stephen's standing rule *"no
  fabricated names in the KB tree -- delete invalid names outright"* — the same rule this
  sprint's C3 applies to the invented part numbers. The four mnemonics were checked three ways
  first: absent from the silicon doc, absent from every other file in `deliverables/ai/P2/`, and
  not accepted as instructions by pnut-ts v1.55.3.

  Status: `RESOLVED` — all six re-derived and cited against live sources; eight non-derivable
  claims listed above are left in place for Stephen's delete-or-keep call.

---
## The published index and its gzip drifted apart in committed history, and the release validator has been red on it (2026-08-25, «#305», arming the content gates) — F-357

- **F-357 — `deliverables/ai/p2kb-index.json.gz` is four days behind `deliverables/ai/p2kb-index.json`
  in committed history, so `validate-dod-release.py` fails its Gzip Compression check on a clean
  tree.** — `RESOLVED`

  **How it surfaced.** «#305» armed two content gates inside `validate-dod-release.py` and ran the
  suite to prove the release path green. Every content check passed and the suite still reported
  **❌ VALIDATION FAILURES - DO NOT RELEASE**. The failure was not the new gates.

  **Measured at `HEAD`, before any edit this session:** the `.json` declares
  `generated: 2026-08-25T05:35:28`, 1130 entries; the `.gz` decompresses to
  `generated: 2026-08-21T23:15:55`, **1129** entries. One key present only in the `.json`
  (`p2kbArchPinDriveConfiguration`) and **181** entries differing between the two. Both files are
  unmodified in the working tree — the drift is committed.

  **Cause.** A task regenerated the index and committed the `.json` without regenerating the `.gz`.
  `release-yamls` Step 5.5 already warns that "both the index AND its `.gz` must be regenerated
  together — that failure is easy to miss if you only regen the `.json`". It was missed anyway,
  and nothing caught it because the DoD suite is not run outside a release.

  **Fixed** by regenerating the `.gz` from the committed `.json`
  (`gzip -c deliverables/ai/p2kb-index.json > deliverables/ai/p2kb-index.json.gz`); the pair is now
  byte-identical on decompression and the suite exits 0. Derived artifact, no content implication.

  **Why it is filed rather than just fixed.** A *published* index and its *published* gzip
  disagreed for four days, and `p2kb-mcp` serves the published state. Any consumer taking the `.gz`
  path saw a 1129-entry index missing a file this sprint added. The `release-yamls` warning
  (2026-08-25 revision) now names this incident so the next reader knows it is not hypothetical.

  **What is NOT closed by this entry:** nothing forces the two into lock-step outside a release
  run. The DoD suite catches it, but only when someone runs it.

  Status: `RESOLVED`

---

## The hygiene gate cannot see the new errata register, so its monotonic allocator is ungoverned (2026-08-25, arbiter, during «#307») — F-355

- **F-355 — `audit-register-hygiene.py` is hard-coded to one register's vocabulary, so
  `engineering/ingestion/SOURCE-ERRATA.md` has an unchecked monotonic allocator.** — `RESOLVED`

  > **Headline corrected 2026-08-25 («#302»).** It read `CONFIRMED` while this entry's own closing
  > line read `Status: RESOLVED` — the scannable layer and the authoritative layer disagreeing, in
  > the *understating* direction that check 10 exists to catch. **Check 10 could not see it:**
  > `BODY_STATUS` matches `^**Status:**` at column 0, and every bullet-form entry in this register
  > (this one included) writes an indented, unbolded `Status:` instead. Verified against the
  > shipped tool source, not inferred. The blind spot is closed in the same pass — see the
  > negative-control note added to the tool.

  **The defect.** The tool's counter check is `re.search(r"\*\*Next finding ID:\s*`?F-(\d+)`?\*\*", text)`
  (`audit-register-hygiene.py:271`) and it emits `no-counter` when absent. The errata register
  declares **`Next erratum ID: \`E-NNN\``** — different label, different prefix — so the gate
  reports nothing about it at all. Every protection it provides for `F-NNN` (counter ahead of every
  allocation, orphaned sections, duplicate IDs, unaccounted coverage) is simply absent for `E-NNN`.

  **Why it matters more than it looks.** The whole reason this project re-checks the next-ID before
  every dispatch is that two agents allocating from a stale number collide silently. The errata
  register is now a live input to «#307» and to every future ingestion, and it allocates two ID
  families (`E-NNN` and `D-NNN`). It is exactly the artifact that needs the gate.

  **This is the arbiter's gap, created the same day.** I stood the register up and gave it a
  counter in a vocabulary no instrument reads — the same class as declaring a section header for an
  ID with no live entry, which this very tool caught me doing hours earlier.

  **Interim, done rather than assumed:** the errata register's IDs were verified by hand at filing
  time — `E-001`…`E-009` present and contiguous, no duplicates, header counter at `E-010` = max+1.
  Command: a parse of `^## (E-\d{3})` against the `Next erratum ID:` header. That is a one-off
  check, not a gate, and it does not survive the next person who forgets.

  **The fix for «#305», specified so it needs no rediscovery:** parameterise the prefix and label —
  take `(label, prefix)` pairs per register file rather than hard-coding `Next finding ID` / `F-`,
  and run the same four checks over each. `SOURCE-ERRATA.md` needs **two** families registered
  (`E-` for errata, `D-` for the open questions in Part B). **Do not "fix" this by renaming the
  errata register's counter to `Next finding ID:`** — that would make two different registers claim
  the same allocator name and is a worse defect than the one it closes.

  ⚠️ Add a **negative control** with the fix: a register with a deliberately stale counter must
  FAIL, and *"the file was not examined at all"* must be a distinct non-zero exit rather than a
  pass. That is the standing lesson from the digit-density gate — a gate that measures nothing and
  exits 0 manufactures confidence.

  **RESOLVED 2026-08-25 by «#305»**, parameterised exactly as specified and NOT by renaming the
  errata counter. `(label, prefix)` are read off the register itself — `COUNTER_RE` matches
  `**Next <word> ID: X-NNN**` in any spelling — and the ID shapes are built from the series the
  file actually uses (`series_in` / `build_id_res`). **Every** declared counter is now checked,
  and a series that is allocated with **no** counter declared is itself a violation, which is
  the general form of this defect.

  **Two further hard-codings surfaced while doing it, both of which would have made the new
  coverage lie:**
  - `canon()` matched `([FG])-0*(\d+)` and returned the ID **unchanged** for anything else. So
    the errata register's canonical live set held `E-001` while the gap scan looked for `E-1`,
    and all ten entries were reported as "went silent" while sitting in plain view. A
    canonicaliser that silently declines to canonicalise is worse than one that raises.
  - The finding heading pattern required `###`. The errata register heads an entry with `##`,
    which the section-structure checks would then have read as a section header. Entry headings
    are now tested first, and `#{2,4}` is accepted.

  **`RESEARCHING` added to `STATUS_WORDS`** (the errata lifecycle's middle state). `OPEN` and
  `GAP` were deliberately **not** added: both occur as ordinary uppercase English in the
  corrections register's prose (8 whole-word occurrences today), and admitting them would let a
  finding carrying no status pass check 4 on a stray word. A vocabulary that silences a check is
  worse than one that is short.

  **`D-` was not registered, because it does not exist.** This finding says the errata register
  "allocates two ID families (`E-NNN` and `D-NNN`)". Measured on disk: `D-` appears **zero**
  times, and Part B's open-question table keys off `E-006`. A `--series` flag exists for a family
  declared before its first filing; nothing needed it.

  **Negative control added, as this finding required:** nine cases through the shipped entry
  point — a stale counter and a clean one in **both** dialects, a register with no counter, a
  series with no counter declared, a missing status, a duplicate ID, and an unreadable register,
  which exits **2** distinctly from a violation's 1. Both live registers verified CLEAN
  afterwards, with the corrections register's numbers unchanged from entry (80 live, 300
  archived, 0 unaccounted, 5 guardrails exempt).

  Status: `RESOLVED`

---
## Check 10 had never once been able to fire, on either side of the comparison it makes (2026-08-25, «#302», the whole-register reconciliation) — F-358

- **F-358 — `audit-register-hygiene.py`'s headline-vs-body check reads `**Status:**` at column 0
  only and the *first physical line* of a headline only, so in this register it could see 5 of 20
  status declarations and missed every wrapped headline — including both live disagreements it
  exists to catch.** — `RESOLVED`

  **How it surfaced.** «#302»'s job was to leave all 81 status tokens accurate. Deriving the state
  per entry by hand — rather than trusting the gate that reports the file CLEAN — turned up two
  entries whose headline and body contradicted each other:

  | Finding | Headline said | Its own body said |
  |---|---|---|
  | **F-355** | `CONFIRMED` (on line **2** of a wrapped headline) | `Status: RESOLVED` (indented) |
  | **F-347** | `PENDING-VALIDATION` (line 2) | `**Disposition.** PARTIAL` (blockquoted) |

  Check 10 exists for exactly this and reported CLEAN on both, every run, since it was written.

  **Two independent blind spots, and each alone was sufficient to hide F-355.**

  1. **Body side — `BODY_STATUS = ^\*\*Status:\*\*` matched column 0 only.** This register declares
     a verdict four other ways: indented under a bullet entry (`  Status: …`), inside a blockquote
     (`> Status: …`), and as `**Disposition.**`. **Measured on the file: 20 status-declaration
     lines, 5 visible, 15 invisible** — three quarters of the bodies.
  2. **Headline side — the checks read `block["headline"]`, which `parse()` sets to the FIRST LINE.**
     Bullet entries routinely wrap and the register puts the status at the end of the bold lead-in,
     i.e. on line 2, 3 or 4. For every wrapped entry `lead_status()` returned `None`, so check 10
     skipped it outright and 4b had nothing to test.

  **F-355 was invisible on BOTH sides simultaneously**, which is why fixing either one alone would
  have left the disagreement standing while reporting the repair complete — the failure mode this
  project already names as *a check derived from the thing it is checking*.

  **The root cause is not either regex. It is that check 10 shipped with no negative control.**
  Every other check here has one; this one was reasoned about and never asked to fail. **A check
  that cannot fail has not been verified, it has been RUN** — the standing lesson from the
  digit-density gate, arriving again in the tool that was built to stop this class.

  **Fixed** by widening `BODY_STATUS` to every spelling the register actually uses, and by adding
  `scannable_head()`, which accumulates the headline until its `**` markers balance so the whole
  bold lead-in is read. **Both proven before/after:** a fixture carrying an indented-`Status:`
  disagreement passed **CLEAN** through the pre-widening tool (read out of `.backups/`) and **FAILS**
  through the fixed one; a second fixture with the status on line 2 of a wrapped headline did the
  same. Four permanent cases were added to `--negative-control` — the two failing spellings, the
  wrapped-headline case, and an **agreeing** case so an over-eager matcher is caught on the other
  side. The control now runs **13** cases and all pass.

  **Both live registers verified CLEAN afterwards** with the widened checks — corrections (81 live,
  300 archived, 0 unaccounted) and `SOURCE-ERRATA.md` (10 live, next `E-011`) — and the errata
  register is unaffected, since it carries its status in the `##` entry heading and declares no
  `Status:` lines at all.

  **Consequence for the register itself, applied in the same pass:** with the checks able to see
  every headline, **6 entries were found carrying no status token in their scannable headline at
  all** (F-250, F-251, F-252, F-328, F-334, F-335) — a reader scanning headlines got nothing, which
  is worse than a disagreement because there is no signal to notice. All six now carry their body's
  token in the lead-in. **All 81 entries now carry a scannable status that agrees with their body.**

  Status: `RESOLVED`

---
## Carry-forward guardrails — investigated and settled; do NOT re-file (full detail in the archive)

- **F-002 (`WONTFIX`):** `?` / `||` operator-form failures were an agent usage error — the KB is correct (`??var` = XORO32 random; `ABS()` not `||`; `?` is the ternary operator).
- **F-036 (`WONTFIX`):** `calld.yaml` — LOC loading a 20-bit address into PA/PB/PTRA/PTRB is not a defect.
- **F-093 (`WONTFIX`):** `lockrel.yaml` C-flag polarity — the appendix's "inverted" claim is the error; the YAML is correct (C = lock-was-held).
- **F-114b (`RESOLVED-INVALID`):** the MIDI display modes KEYBOARD / GRID / ROLL / MONITOR do **not** exist in PNut v55 — do **not** add them to `midi.yaml` (it carries an explicit `not_supported:` claim).
- **Verified-resolved (don't re-chase):** the Jan-2026 streamer KB audit's issues were all reconciled in the 2026-05/06 passes (DAC routing, 32-pin groups, mode encoding, xcont/xzero phase wording, setxfrq 2³¹ formula, streamer symbols). Only the XZERO concept text was open and is fixed (F-003).

---

## The "masters are clean of the drive-strength mislabel" measurement is wrong (2026-08-25, «#301») — F-356

### F-356 — the drive-strength mislabel is alive in the IOSP master at 23 sites, including the one composition this sprint forbids by name — `CONFIRMED`

**How this surfaced.** «#301» was told, as a *measured result and not an assumption*, that a
class-wide sweep on 2026-08-24 found the manual and app-note masters **clean** of this sprint's
defect class (the drive-strength mislabel, the fabricated ladder, pin slew-rate claims) — which is
why Plan §3 excludes manual prose from that class. Working F-251 required reading the deSilva Ch.1
LED aside, whose closing sentence turned out to state the mislabel outright. One site is an
anomaly; the sweep it implied is what produced this finding.

**What was measured.** A sweep of every `opus-master/` body and CHANGELOG across all manuals and all
seven app notes (excluding `archived-2025/` scaffolding and the non-P2 `Donna-Manuscript`) for
pull-up / pull-down language, then each hit graded by hand as *external component* (correct) or
*`P_HIGH_*`/`P_LOW_*` glossed as a bias resistor* (wrong):

| Site class | Count | Where |
|---|---|---|
| A `P_HIGH_*`/`P_LOW_*` constant glossed as a **pull-up/pull-down resistor** | **23 lines** | IOSP `appendix-b-p-constants.md` ×7 · `chapter-12-digital-input.md` ×5 · `chapter-02-enhanced-direct-io.md` ×7 · `chapter-06-digital-output.md` ×2 · `appendix-a-intent-index.md:56` · `part-5-appendices/index.md:221` |
| **"internal pull-up/pull-down"** asserted as a P2 feature | **5 lines** | `chapter-06-digital-output.md:137`, `:144`, `:441` · `chapter-02-enhanced-direct-io.md:431`, `:479` |
| The composition this sprint says to **never** write | **4 sites** | `chapter-02-enhanced-direct-io.md:94`, `:399`, `:439`, `:480` — `P_HIGH_15K \| P_LOW_FLOAT` |

**Why each class is wrong.** A pull-up is active whenever the pin is *not* driven; a drive-strength
selector applies **only while the pin drives that direction** — DIR high, per the Pin Mode Legend
(`deliverables/ai/P2/architecture/pin-drive-configuration.yaml:41-43`, `:166-171`; P2 Datasheet
2022/11/01 p.24). This is F-321's reasoning exactly, and F-321 was applied to
`deliverables/ai/P2/` and **only** there. `chapter-02-enhanced-direct-io.md:53` is the cleanest
example: it prints `| P_HIGH_15K | %010 | Resistive | ~200µA / 15kΩ | **Pull-up resistor** |` — a
component the chip does not have, in a table of things it does. `:441`'s
*"Open-drain + internal pull-up"* is the F-322 inversion in a summary row. And
`P_HIGH_15K | P_LOW_FLOAT` is the composition whose "high side weak, low side floated" variant
`pin-drive-configuration.yaml:250-252` records as having **no Parallax documentary statement and no
empirical record** — the manual teaches it four times, once as a recipe headed **"Pull-Up
Resistor:"**.

**Scope note — this is filed, NOT fixed, and the distinction is deliberate.** Plan §3 puts this
defect class out of scope for manual prose in this sprint, and «#301» was told scope is Stephen's.
So the correct act is to **falsify the measurement the exclusion rests on** and hand it over, not to
widen a roster. The two sites «#301» *did* fix are the ones inside its own roster's findings:
deSilva `COMPLETE-OPUS-MASTER.md:294` (inside F-251's aside), and `:2881` was checked and left
because it is already **correct** (*"No pullup/pulldown by default — Use external resistors or
configure smart pin modes"*).

**What would settle it.** Nothing further to establish — the mechanism is closed (F-321 applied, the
Pin Mode Legend cited, the idioms hardware-verified in
`pin-drive-configuration.yaml:203-239`). What is needed is a decision on **when** the IOSP master
takes the correction, because it is not a token substitution: two constant tables, a chapter section
heading (*"### Button Input with Internal Pull-Up"*), four worked recipes and an intent-index row all
have to be restated in drive-strength terms, and the four `P_LOW_FLOAT` recipes need a form that has
a source behind it. That is a chapter-scale pass on Chapters 2, 6 and 12 plus two appendices, not a
sweep.

**Related:** F-321 (same mislabel, KB side, applied) · F-322 (the disable-the-drive inversion) ·
F-325 (the ladder absent from the shipped KB) · F-336 (`P_HIGH_15K | P_LOW_FLOAT` has neither a
Parallax statement nor a bench result) · F-341 (the same mislabel in our own derived analysis docs) ·
`SOURCE-ERRATA.md` E-004 and **E-010** (Parallax's own guides state it).

> 🔴 **F-341 IS SHARPER THAN "LATENT" — THOSE FILES INVENT PARALLAX PART NUMBERS. Confirmed by
> Stephen 2026-08-26.**
>
> Asked whether our board coverage was complete, the inventory turned up three part numbers with
> **zero occurrences in any ingested source directory** — i.e. in any actual captured Parallax
> document. They exist only in the loose analysis files at `engineering/ingestion/sources/`:
>
> | Invented | Where it appears | What it actually is |
> |---|---|---|
> | **#64025 "LED Board"** | `p2-hardware-validation-checklist.md:102`, `p2-board-power-analysis-matrix.md` | **does not exist** — the real board is **#64006C LED Matrix** |
> | **#64026 "7-Segment Display"** | `p2-hardware-validation-checklist.md:150` | **does not exist** |
> | **#64027 "Switches Board"** | `p2-hardware-validation-checklist.md:191` | **does not exist** — switches are on the **#64006A Control** add-on |
>
> **Stephen, asked directly: "LED board, no. 7-segment, no. Switches, no."**
>
> **Why this is worse than a wrong name.** The inventions are *plausible* — they describe real
> capabilities (LEDs, a display, switches) that map onto real boards, at part numbers adjacent to
> the real #64019/#64020/#64029 range. And `#64027`'s validation section is headed **"Test 1:
> Pull-up Test"**, so the fabricated board carries the fabricated mechanism. A reader has nothing to
> catch it with.
>
> **None of the four files names a Parallax document anywhere.** Their headers are
> *"Comprehensive testing procedures…"*, *"Complete power budget calculations…"*, *"Complete
> cross-reference for automatic code generation"* — authored analysis, with no provenance, sitting
> in the directory reserved for captured sources. **Location is doing the work of attribution.**
>
> 🟢 **CONTAINMENT VERIFIED: zero leakage.** `grep -rl` for all three across `deliverables/ai/P2/`
> returns **0 files**. The shipped KB never carried them, and «#305» had already excluded loose
> root files from the fidelity tool's truth side. The damage is confined to the ingestion tree.
>
> **Still open, and it is a scope call:** the four files remain where sources live, they still assert
> the pull-up mislabel, and the compatibility/power matrices cross-reference boards that do not
> exist — so anything derived from them is derived from fiction. Options: correct them in place and
> relabel as analysis, relocate them out of `sources/`, or retire them. **Not actioned pending
> Stephen's decision.**
>
> 🟢 **THE INVENTED-PART-NUMBER HALF IS CLOSED 2026-08-26 («#323»).** Stephen's standing rule —
> *"no fabricated names in the KB tree, delete invalid names outright"* — settled the disposition
> without needing a further decision, so it was executed. **Every `#64025` / `#64026` / `#64027`
> site in the repository was worked**, which was more than the three the finding names:
>
> | File | What was there | What was done |
> |---|---|---|
> | `sources/p2-hardware-validation-checklist.md` | three validation sections (`:102`, `:150`, `:191`), incl. the `#64027` "Pull-up Test" that carries the F-321 mislabel | sections deleted, dated removal note left in place |
> | `sources/p2-board-power-analysis-matrix.md` | three power-analysis sections, two `case` arms in worked code, five Quick-Reference rows | all deleted, removal note left |
> | `sources/p2-complete-signal-flow-matrix.md` | three signal-path sections, a VIO-load `case`, three `ADDON_*` constants, an impedance-detect routine returning two of the invented boards | all deleted, removal note left |
> | `sources/p2-board-addon-compatibility-matrix.md` | three grid rows, five detailed configurations across two boards, three power rows, three `case` arms | all deleted, removal notes left |
> | `plans/quick-bytes-ingestion-plan.md` | `parallax_id: "64025"` against **"P2 RTC Add-on Board"** | **corrected to `64013`** — the real part number, from `sources/edge-breakout-board/edge-breakout-board-narrative.txt:137` |
> | `knowledge-base/P2-support/extractors/hardware-specs-extractor.py` | a YAML **generator** with all three baked in, emitting them under `source: P2 Documentation Collection` | the three entries deleted, note left |
>
> **Deleted rather than relabelled, deliberately.** The nearest real boards are the **#64006C LED
> Matrix** (an 8×7 Charlieplexed grid driven on 8 pins) and the **#64006A Control** add-on (four
> buttons and four LEDs); there is no 7-segment board in the #64006 series at all. The removed pin
> maps, currents and test procedures described none of those, so relabelling would have attached
> fabricated numbers to real boards — a worse defect than the one being fixed.
>
> After: `grep -rn '64025\|64026\|64027'` across the repository returns **no hit that presents a
> board**. Every surviving occurrence is one of four kinds: a dated removal note at the site the
> content was cut from, the `#64013` correction comment, the sprint plan's task row, or this
> register's own documentation above. Deliberately stated as classes rather than a count — the
> count changes every time this register is edited, and a self-referential tally is stale the
> moment it is written. (Arbiter check, «#323»: the figure first written here was 11; the live
> number was already 15, because writing the table above added hits to the thing being counted.)
>
> **Two halves remain open**, both unchanged by this pass: the four files still sit at
> `sources/` top level asserting the pull-up mislabel (the relocate-or-repair-or-retire call), and
> the *same class* of unverified part numbers survives in them — `#64028` "Buttons Board",
> `#64029` relabelled "Switches and LEDs Combo", `#40003` "Protoboard", `#40007` "Digital I/O
> Board". Those four were left strictly alone because Stephen confirmed three numbers, not seven,
> and «#323» would have been widening its own scope to act on them.

Status: `CONFIRMED` — measured, unfixed by decision; belongs to whoever owns the IOSP manual head.

---

## Five defects surfaced while ending the drive-strength mislabel class (2026-08-25, «#296» §5) — F-342…F-346

> **Origin.** All five were found while correcting F-321…F-324 — three of them only because
> R8 forces a **semantic read** of every example after it compiles. Three are fixed in that same
> pass and marked so; two are not this task's repair and are filed for the head that owns them.
> Every line number below was read off disk on 2026-08-25.

### F-342 — a Parallax board guide states the pull-up mislabel itself, and prescribes it in the one configuration where it cannot work — `RESOLVED — the adjudication this entry owed was made and executed BOTH ways; the source-defect half now lives in the errata register`

> **RELOCATED + CLOSED 2026-08-25 («#302»). Pointer left behind rather than a move, because the
> reasoning above is the origin of the erratum and is worth reading in place.**
>
> This entry is a **source-document defect** by the three-register test — *if Parallax fixed the
> #64013 guide tomorrow, would it disappear?* **Yes.** Its home is
> **`engineering/ingestion/SOURCE-ERRATA.md` → `E-004` (`RESOLVED`)**, *"the pull-up mislabel, in a
> Parallax guide, prescribed where it cannot work"*, which carries the same two locators
> (`P2-RTC-Add-on-text.txt:74-77`, `spin2-v55-text.txt:1505`), the same Pin-Mode-Legend counter-cite,
> and the empirical corroboration with its ⚠️ scoping (EF-063/EF-064 are rig apparatus, never the
> authority). That register did not exist when this was filed — it was created 2026-08-25.
>
> **The adjudication this entry left open is settled, and NOT by picking one branch.** It asked for
> (a) keep the quote and add a DIR-high note, or (b) route it upstream as a board-guide erratum.
> **Both were done.** (b) is `E-004`. (a) is applied and **verified on the artifact, not on a status
> line**: `deliverables/ai/P2/hardware/addon-rtc.yaml` `pin_mode_tip` is no longer the guide's
> sentence — it is a map carrying `source:` (all four citations), `board_fact:` (SCL/INT/CLKOUT
> share the single +0 pin, so only one is usable at a time), `p2_side_mechanism:` (*"Hold the pin
> weakly high with P_HIGH_150K and DIR HIGH"*), and an explicit
> `do_not_copy_the_guides_wording` key quoting the wrong text so it cannot be re-adopted. The KB
> half is tracked under **F-353**.
>
> **The D3/R9 restraint held:** the source's wording was never silently improved — it is quoted,
> labelled wrong, and answered.

> **Where the KB carries it:** `deliverables/ai/P2/hardware/addon-rtc.yaml:49-51` (`pin_mode_tip`).
>
> **Where it comes from:** `engineering/ingestion/sources/P2-RTC-Add-on/P2-RTC-Add-on-text.txt:74-77`
> — *"To use the I2C SCL function, set the I2C output mode to use 3.3 k-ohm pull-up. … then disable
> I2C and set the P2 Smartpin (or equivalent) **input mode** to 150 k-ohm pull-up."*
> (P2 RTC Add-on Board #64013, v1.0 11/29/2022, page 2.) The KB is quoting its source faithfully.
>
> **Why it is a finding and not a KB defect.** Two things are wrong in the source itself:
>
> 1. **The mislabel, from Parallax.** There is no 150 kΩ pull-up on the P2. `P_HIGH_150K` is
>    *"Drive high 150kΩ"* (`sources/spin2-v55/spin2-v55-text.txt:1505`) — a drive-strength
>    selector. This is F-321's exact rename, in a Parallax document.
> 2. **It is F-322-shaped.** "input mode … 150 k-ohm pull-up" is a contradiction on this silicon:
>    input mode is DIR = 0, and the Pin Mode Legend states *"DIR = direction bit; 0: input (float),
>    1: output (drive)"* (`sources/p2-datasheet/p2-datasheet-text.txt:1144`; identical at
>    `sources/p2-hardware-manual/p2-hardware-manual-text.txt:871`). With DIR = 0 the drive-high
>    selection is inactive and the pin is plain high-impedance — the INT/CLKOUT line would float.
>
> **Deliberately NOT rewritten** (D3/R9): a source's wording is not ours to silently improve, and
> the correct replacement is a behaviour claim about the #64013 board that no source states.
>
> **What is owed.** Adjudicate whether the KB should (a) keep the quote and add a note that the
> weak high drive requires DIR high, citing the legend line above, or (b) route the discrepancy
> upstream as a board-guide erratum. This is the second Parallax-source-level instance of the
> F-321 class after F-341's derived-analysis documents, and the first in a *published Parallax
> document* rather than one of ours.

### F-343 — the KB credited the 64006A Control Board with pull-up resistors its own board guide does not give it — `PENDING-VALIDATION`

> **Where:** `deliverables/ai/P2/hardware/p2-hardware-feature-comparison.yaml:141` —
> `special_features: "Current limiting resistors, pull-up resistors"`.
>
> **What the source says.** `engineering/ingestion/sources/p2-eval-add-on-boards/boards/addon-control-64006a.md:16-23`
> (Product Guide v2.0, 1/12/2021) gives every one of the eight I/O pins **one** component: a
> *470 Ω series resistor*. Pull-up and pull-down appear **nowhere** in that board's source. The
> KB's own `hardware/addon-control-board.yaml` agrees — 470 Ω series resistors on all eight pins,
> no bias network.
>
> **Two KB files disagreed about a physical board**, and the wrong one is the comparison table an
> agent reads to pick a board.
>
> **APPLIED 2026-08-25 by «#296» §5**, by deleting the unsupported half:
> `special_features: "Current limiting resistors (470 ohm in series with each LED and each switch)"`.

### F-344 — the derived board extract contradicts itself in one sentence about switch polarity — `CONFIRMED`

> **Where:** `engineering/ingestion/sources/p2-eval-add-on-boards/boards/addon-control-64006a.md:9-11`
> — *"each **active-high** push-button has a **470 Ω series resistor** so the I/O pin is **driven
> low** while the button is asserted."*
>
> **Active-high and driven-low-when-asserted cannot both be true of the same switch.** The rest of
> that same file says active high in the pin map (`:20-23`), and the shipped
> `hardware/addon-control-board.yaml:16-20` says *"the I/O pin reads high while the button is
> pressed"* — so the KB already resolved it the other way. The extract's own summary sentence is
> the outlier.
>
> **Ingestion-tree defect, not a YAML edit** — this file is derived source-research and is frozen
> to KB maintenance. Same class as **F-341** (our own derived documents inside the truth root).
> **What is owed:** re-read the #64006A Product Guide v2.0 page and correct the extract's summary
> sentence, or record why the guide itself says both.

### F-345 — a worked example read a button with inverted flag polarity, under a comment asserting the opposite — `PENDING-VALIDATION`

> **Where:** `deliverables/ai/P2/language/pasm2/concepts/basic-io.yaml`, `common_patterns.button_read`
> (`:243` before the fix): `TESTP #button_pin WZ      ' Z=1 if button pressed (low)`.
>
> **Evidence.** `TESTP` sets the flag **to** the pin state, not to its complement —
> `deliverables/ai/P2/language/pasm2/testp.yaml` encoding table: `c: IN[D[5:0]]`, `z: IN[D[5:0]]`;
> Silicon Doc, `sources/silicon-doc/part2-video-output.txt:291` — *"read pin D bit in INx and
> affect C or Z"*, with `TESTPN` (`:292`) as the inverting form. So `Z = 1` means the pin is
> **high** — the button **released**. The example ran its handler on exactly the wrong half of the
> input, and the following `IF_Z CALL` compiled perfectly.
>
> **This is why a clean compile is not a verification** — the same lesson as F-322, by a different
> mechanism (flag polarity rather than DIR state), found only on the semantic read.
>
> **APPLIED 2026-08-25 by «#296» §5:** `TESTP #button_pin WC ' C = pin state` / `IF_NC CALL
> #button_action ' a press shorts the pin to ground`. Swept: `TESTP`/`TESTPN` with a
> polarity-claiming comment appears nowhere else in the shipped set.

### F-346 — three worked examples were structurally unrunnable, and one rule contradicted its own two examples — `PENDING-VALIDATION`

> **All four found by reading examples I had just compiled successfully.** None was caught by any
> gate; `pnut-ts` is the legality half only.
>
> | Where | What was wrong | Fix applied |
> |---|---|---|
> | `language/pasm2/concepts/basic-io.yaml` `common_patterns.led_blink` | `JMP #$ ' Repeat` — `$` is the **current** instruction's address, so this is a jump to self. The LED blinked once and the cog hung. Proved by byte-identity: `JMP #$` at cog address 1 compiles identically to `JMP #1`, and differently from `JMP #0`. | labelled `blink`, `JMP #blink` |
> | `language/pasm2/concepts/basic-io.yaml` `common_patterns.led_blink`, `.button_read` | neither fragment compiled — a bare `name = value` line with no `CON`, then `ORG` with no `DAT`; `button_read` also called an undefined `#button_action` | `CON`/`DAT` headers added; poll loop and a `button_action` stub added |
> | `architecture/smart-pins/smart-pin-00000-normal-mode.yaml` `pasm2_complete` | `ORG` was followed immediately by `led_pin LONG 56`, so **execution began on data** (cog address 0 held `$38`), and nothing ever called `setup_pins` — the pins the listing exists to configure were never configured | entry point added (`CALL #setup_pins` / `JMP #main_loop`); the two `LONG`s moved below the code beside `pin RES 1` |
> | `language/pasm2/concepts/basic-io.yaml` `safe_initialization_patterns.avoid_glitches` | `rule: "Set DIR before OUT to prevent output glitches"` — while **both** of its own examples set OUT first and DIR second. An agent reading the `rule:` string alone would do the opposite of what the file demonstrates. | `rule: "Set OUT to the desired state while the pin is still floating, then raise DIR"`, and the `wrong:` comment restated to name the actual failure (raising DIR latches the wrong level onto the pin) |
>
> **All four sites recompiled from the shipped YAML bytes after the fix**, and re-read.

---

## Four defects surfaced by the whole-KB promotion filter (2026-08-25, «#298» Plan §7) — F-348…F-351

> **Origin.** «#298» applied the belonging test — *can this block change the code an agent emits?* —
> to every quantitative block in the shipped KB (114) and every block the sprint's two purges removed
> (119). Three of these four are content defects the purge could not see; the fourth is an instrument
> artifact that inflates the Tier-2 count. The dispositioned list is
> `engineering/analysis/2026-08-25-whole-kb-promotion-filter.md`. Every line number below was read off
> disk on 2026-08-25.

### F-348 — a *cited* block shipped a pin-current limit five times the datasheet's absolute maximum, plus TTL logic levels the P2 datasheet does not contain — `PARTIAL`

> **Where:** `deliverables/ai/P2/language/pasm2/concepts/basic-io.yaml` and
> `deliverables/ai/P2/language/spin2/concepts/basic-io.yaml`, both `hardware_specifications`
> (11 lines, byte-identical twins). **Removed 2026-08-25**; backups at
> `.backups/deliverables/ai/P2/language/{pasm2,spin2}/concepts/basic-io.yaml.20260825-082653`.
>
> **What was wrong — five of six values:**
>
> | Shipped | P2 Datasheet |
> |---|---|
> | `max_current_per_pin: "150mA"` | **±30 mA** max allowable current per I/O pin — `sources/p2-datasheet/p2-datasheet-text.txt:2142` |
> | `VIL_max: "0.8V"` / `VIH_min: "2.0V"` | no such pair; a single ratiometric **Vih = Vxxyy × 0.3 / 0.5 / 0.7** — `:2163` |
> | `VOL_max: "0.4V at rated current"` | **15 mV** drop at 1 mA sinking, 510 mV at 30 mA — `:2172`, `:2174` |
> | `VOH_min: "2.4V at rated current"` | **−6 mV** drop at 1 mA sourcing, −580 mV at 30 mA — `:2176`, `:2178` |
>
> The four thresholds are 5 V-TTL boilerplate. The `150mA` is the F-327 drive-ladder fabrication's
> top rung, and it is **the number an agent uses to size an LED series resistor** — a 5× error in the
> direction that damages silicon.
>
> **Why two purges and a whole-class drive-strength sweep all missed it — measured, and it is a
> citation false negative, not a coverage gap.** `audit-yaml-claim-sourcing.py` judged the block
> **cited** because `INLINE_CITE_RE` matched the word **`datasheet`** inside
> `max_current_total: "Check datasheet for package limits"`. That is a **deferral**, not an
> attribution. Verified across the whole cited population: of the 30 cited quantitative blocks in the
> KB, this pair are the **only** two whose citation token identifies **no document at all** — every
> other one resolves to a named document ("P2 Datasheet", "Silicon Doc v35", "AKM AK5704 datasheet",
> "NXP PCF8523 datasheet", "W25Q128JV datasheet"). The nearest neighbour, and the one to watch, is
> `hardware/addon-rtc.yaml` `pin_mode_tip` — it defers to *"the RTC datasheet"*, which is also a
> deferral, but it identifies the document by role and its sibling `rtc_chip` block names it outright
> (NXP PCF8523). That is the line: **naming a document, however briefly, versus naming the class of
> document**. This is the same principle F-334 established — *a citation names a DOCUMENT* — in its
> remaining uncovered form.
>
> Note also that `4cecb02c` ("Correct the drive-strength mislabel class; both fidelity tiers now read
> zero") swept the class and did not reach these, because the fidelity tool is keyed on **named
> constants** and this block names none.
>
> **Nothing was lost.** The correct facts already ship, cited, in
> `deliverables/ai/P2/architecture/io_pin_timing.yaml` `absolute_maximum_ratings` (±30 mA per pin,
> ±10 mA diode) and `input_voltage_and_protection`. No `related:`/`see_also:` anywhere referenced
> `hardware_specifications`; `validate-crossref-keys.py` re-ran clean (3156 refs, 0 unresolved).
>
> **Owed:** «#299» decides whether anything returns in their place, source-first from the datasheet
> lines above. Nothing may return that states a per-pin current above ±30 mA.

### F-349 — PLL lock time is stated as ~10 microseconds in one place and ~10 milliseconds in four others; it is a delay an agent emits — `PENDING-VALIDATION`

> **The outlier:** `architecture/clock_system.yaml` `stabilization_timing` — `pll_lock: "~10 microseconds"`.
> Removed by «#293» (`15c84de5`), so it is **not currently shipping** — but it is a Population-2
> repopulation candidate and would return the contradiction.
>
> **The four that ship, all agreeing on milliseconds:**
> - `language/spin2/methods/clkset.yaml` `timing` — `cycles: "~10-20ms for PLL lock"`
> - `language/spin2/system-variables/clkmode.yaml` `notes` — *"PLL must lock before switching to PLL source (~10ms)"*
> - `language/pasm2/hubset.yaml` `safe_clock_switching` — *"Wait for PLL to lock (~10ms)"*, and its
>   step_2 code computes `clkfreq/100` clocks = 10 ms
> - `language/pasm2/asmclk.yaml` `expansion_details` — emits `WAITX ##20_000_000/100`, a 10 ms wait at 20 MHz
>
> **Why it matters:** this is not a documentation nicety. It is the literal WAITX operand between
> configuring the PLL and switching to it. A three-orders-of-magnitude error in the short direction
> switches the clock source before lock.
>
> **RESOLVED 2026-08-25 by «#299» — the answer is 10 ms, and it is stated outright, not inferred.**
> Three Parallax documents state it, and each was read on **two independent extraction paths** (the
> raw docling text and the reconstructed table):
> - **P2 Datasheet 2022/11/01** p.18 — %E row: *"XI input must be enabled by %CC. Allow 10ms for
>   crystal+PLL to stabilize before switching over to PLL clock source."*
>   (`sources/p2-datasheet/p2-datasheet-text.txt:783-785`; same cell at
>   `sources/p2-datasheet/complete-tables-reference.md:133`). %SS row: *"CC != %00 and E=1, allow
>   10ms for crystal+PLL to stabilize before switching to PLL"* (`:828`, `:151`).
> - **Propeller 2 Documentation v35** — identical wording (`sources/silicon-doc/part3-interrupts.txt:528-529,:576`).
> - **P2 Hardware Manual 2022/11/01** — identical wording
>   (`sources/p2-hardware-manual/p2-hardware-manual-text.txt:572,:592`; `complete-tables-reference.md:105,:123`).
>
> All three also *emit* the wait in their own worked example: `WAITX ##20_000_000/100` — 10 ms at the
> RCFAST rate the code is still running at (`p2-datasheet-text.txt:857-859`;
> `silicon-doc/p2-documentation.txt:6266`; Spin2 v55 states the same line twice, once for `clkmode_`
> and once for `ASMCLK`, `sources/spin2-v55/spin2-v55-text.txt:1725,:1738`). The crystal-only case is
> **5 ms** (`p2-datasheet-text.txt:830`). The `~10 microseconds` figure has no source and is not
> restored; `architecture/clock_system.yaml stabilization_timing` returned carrying the 10 ms / 5 ms
> pair with the citation and a `conflict_resolved` note.
>
> 🔴 **A FIFTH LOCATION THIS FINDING DID NOT NAME, found by working the file rather than the list.**
> `architecture/clock_system.yaml programming_examples` carried **`WAITX ##20_000_000/10000  ' Wait
> 100µs for PLL lock`** in TWO examples — `pll_160mhz_from_20mhz_crystal` and `overclock_250mhz`. The
> sourcing gate cannot see them because they sit inside a code region, which the gate strips by
> design; that is the same blind spot F-333 records for prose. Both corrected in place to
> `WAITX ##20_000_000/100  ' Wait ~10ms for crystal+PLL to stabilize`. **Class-wide sweep run:**
> `grep -rn "PLL lock\|PLL to lock\|pll_lock\|for PLL" --include=*.yaml deliverables/ai/P2/` — the
> only remaining hits are the four surviving millisecond statements this finding already named, plus
> the new cited block. No sixth location.
>
> `PENDING-VALIDATION` — the KB edit is applied and gate-verified; only the YAML release is owed.

### F-350 — the F-328(b) eval-board fabrication class is not confined to `p2-eval-board.yaml` — `PENDING-VALIDATION`

> **Where:** `deliverables/ai/P2/hardware/p2-hardware-feature-comparison.yaml`,
> `development_boards.p2_eval_board` and `compatibility_matrix.eval_board_addons`. Backup at
> `.backups/deliverables/ai/P2/hardware/p2-hardware-feature-comparison.yaml.20260825-082759`.
>
> F-328(b) catalogued invented #64000 hardware in `p2-eval-board.yaml`. Sweeping the **class** rather
> than the occurrence found the same invented peripherals in a second file, which F-328 never named.
>
> **Removed 2026-08-25 (fabricated — the board has none of them; `grep -rn -i "\bVGA\b\|HDMI\|resistor
> DAC\|audio\|prototyp\|breadboard"` over `sources/p2-eval-board/complete-p2-eval-board-reference.md`
> returns zero hits):** `audio_capability: "Stereo DAC output"` · `video_capability: "VGA output"` ·
> `breadboard_area: "Large prototyping area"`.
>
> **Still shipping and WRONG — owed to «#307», needs re-derivation from the repaired capture, not deletion:**
>
> | Key | Ships | `complete-p2-eval-board-reference.md` |
> |---|---|---|
> | `development_boards.p2_eval_board.dimensions` | `127×89mm` | **3.55″ × 3.55″** (`:62`, `:260`) ≈ 90 × 90 mm |
> | `…usb_connectivity` | `USB-C programming + micro-USB serial` | **two micro-USB** (`:59`, `:76`); no USB-C anywhere |
> | `…addon_headers` | `Two 2x6 headers for add-on boards` | **eight** I/O Pin Breakout Edge Headers (`:35`, `:52`) |
> | `…flash_memory` | `16MB (with P2-EC)` | 16 MB correct; the P2 is **soldered on-board** (`:124`), not an edge module |
> | `compatibility_matrix.eval_board_addons` | `Up to 2 add-on boards`; `A-side (P32-P39) + B-side (P24-P31)` | **8 sets of 8** covering all 64 pins (`:52`) |
>
> **The generalizable half.** F-328(b)'s own lesson was that a purge keyed on missing citations cannot
> see a wrong scalar or an invented section. This adds the sibling: **a finding scoped to one file
> cannot see the same fabrication copied into another.** The class-wide sweep is what found it, and it
> is the only thing that would have.
>
> **APPLIED 2026-08-25 («#307»).** All five keys re-derived from the repaired capture and cited, in
> `development_boards` and `compatibility_matrix` — `dimensions` → 3.55 in x 3.55 in ·
> `usb_connectivity` → two micro-USB (PC-USB 500 mA / AUX-USB 2000 mA), no USB-C, no barrel jack ·
> `addon_headers` → eight I/O Pin Breakout Edge Headers · `flash_memory` → 16 MB on the board, the
> P2 soldered on (not an edge-module carrier) · `eval_board_addons` → eight headers in 8 groups of 8
> covering all 64 pins, replacing "Up to 2 add-on boards" and the invented A-side/B-side split.
> **And the class ran wider than five:** the same read found invented carrier part numbers, wrong
> carrier and edge-module dimensions, a fabricated "3.3V input only / edge castellations" mini
> breakout, an eval board with a barrel jack it does not have, and **`64006G` described as a
> "Combined Digital I/O" board** — it is the Goertzel board, i.e. the F-121 fabricated-name family
> in a file F-121 never named. Full list in the file's own `corrections_applied_2026_08_25` keys and
> in **F-353**. The file now cites per block; its six Tier-2 blocks left the advisory lane.
>
> Status: `PENDING-VALIDATION` — applied and gate-verified; only the YAML release is owed.

### F-351 — the sourcing gate reads Parallax part numbers, Unicode code points and an ISO designator as amperes; 12 blocks are pure instrument artifacts — `RESOLVED`

> **RESOLVED 2026-08-25 by «#305»**, both repairs as suggested here plus the thousands-separator
> one. A bare `A` now requires at most three integer digits (a current in this domain is
> `1.5A`/`20A`/`100A`; a part number or standard designator is a four-or-more digit run);
> `U+XXXX` is masked alongside `%binary` and `$hex`; the number pattern accepts `,` groups so
> `3,333,333 Hz` is one token rather than `333 Hz` + `000 Hz`. Deliberately NOT applied to the
> other units — `500,000,000 Hz` and `2000Ohm` are real claims.
>
> **Measured: 9 blocks, not 10.** The tenth on this finding's list
> (`hardware/p2-hardware-feature-comparison.yaml` `selection_criteria`) had already been drained
> by an earlier task and was not in the population when «#305» ran. The other nine are exactly
> as listed. Five negative-control cases were added — the three artifacts MUST NOT fire, and a
> real `1.5A`/`4A` current and a `100A` inrush MUST STILL fire, so the fix cannot be widened
> into a disarm.

> **Instrument:** `engineering/tools/validation/audit-yaml-claim-sourcing.py`, `QTY_RE`. **Do not fix
> here — «#305» owns instrument repair** (see F-335/339/340/341). Filed so the Tier-2 count is read
> correctly in the meantime.
>
> **Mechanism.** `QTY_RE` accepts a bare `A` as amperes with only `(?<![\w%$])` guarding the number's
> left edge. That guard passes at a string's start and after `+`, so:
>
> | Text | Read as | Real meaning |
> |---|---|---|
> | `"64006A"` | 64006 amperes | a Parallax part number |
> | `unicode: "U+221A"` | 221 amperes | the SQUARE ROOT code point |
> | `ISO/IEC 14443 A/MIFARE` | 14443 amperes | the RFID standard's designator |
>
> **Measured, whole-KB:** **10 of the 84 Tier-2 blocks** state no quantity at all — every token in them
> is one of the three artifacts above: `hardware/addon-control-board.yaml` `part_number`, `aliases`,
> `availability` · `hardware/hardware-compatibility-matrix.yaml` `physical_stacking_constraints`,
> `optimal_configurations` · `hardware/p2-hardware-feature-comparison.yaml` `selection_criteria` ·
> `hardware/p2-hardware-selection-guide.yaml` `decision_tree`, `application_specific_guides` ·
> `hardware/p1_rom_font_character_set.yaml` `character_categories` ·
> `community/obex/objects/4070.yaml` `object_metadata`. Two further **cited** blocks are the same
> artifact (`community/quick-bytes/{five-buttons-on-one-pin,leds-beyond-the-basics}.yaml` `quick_byte`,
> both on `related_boards: 64006A`). **Twelve blocks KB-wide.**
>
> **So the true Tier-2 advisory population is 74, not 84** — the gate's own number over-reports by 12%,
> and every one of the ten sits in `hardware/`, the tree where part numbers are densest.
>
> **A second, milder artifact: thousands separators split.** `range: "3,333,333 Hz to 500,000,000 Hz"`
> in `language/spin2/constants/special-configuration-symbols.yaml` `clock_configuration` yields the
> tokens `333 Hz` and `000 Hz`. This does not create a false finding (the block carries real MHz) but
> it inflates the per-block quantity count the advisory prints.
>
> **Suggested repair for «#305» to adjudicate:** require the ampere unit to be preceded by a word
> boundary that is not a digit-run continuation (a part number is `\d{4,}[A-Z]`), and mask `U+XXXX`
> alongside the existing `%binary`/`$hex` masking. Both are testable with the negative-control harness
> the tool already carries.

## Provenance holes the repopulation could not fill (2026-08-25, «#299» Plan §8 part 2) — F-352

> **Origin.** «#299» rebuilt `architecture/`, `language/`, `guides/` and `application-notes/` from
> the repaired sources, source-first. Forty-five of F-347's sixty blocks came back cited. Two did
> not, for the same reason — the KB was their only home — and the rule set had no branch for that
> once the purge had already removed them. Line numbers below were read off disk 2026-08-25.

### F-352 — two shipped KB areas are authored-here content with NO upstream anywhere in the ingestion tree, and once their blocks were purged the promotion filter's sub-rule P had no branch left for them — `CONFIRMED`

> **Found:** 2026-08-25 by «#299», working the sources tree-by-tree rather than the removal list.
> Two of F-347's 60 rows could not be returned source-first, for the same underlying reason, and
> «#298»'s sub-rule P (*presence before removal*) does not cover the case because the removal has
> **already happened**.
>
> | Where | «#298» disposition | What «#299» found |
> |---|---|---|
> | `architecture/click_module_integration.yaml` `best_practices` | **ACTIONABLE** | **No ingested source states any of it.** The file's own `documentation_source: code_analysis` points at `engineering/ingestion/sources/code-analysis/`, which holds exactly three files — `bldc-motor-control-analysis.md`, `debugger-analysis.md`, `flash-loader-analysis.md` — and `grep -rln -i "click\|mikrobus"` over that directory returns **nothing**. The MikroBUS pinout, the P2 Eval Click Adapter offsets and the "three adapter positions" claim the block depends on have no upstream at all. **Recorded as a GAP, not restored.** |
> | `architecture/io_pin_timing.yaml` `best_practices` | **CORRECT BUT NOT ACTIONABLE** | Generic PCB-layout lore — match trace lengths, 22-33 Ω source termination, ~1 ns rise per 10 pF. `grep -rn "22-33\|150 ps\|150ps\|source termination\|match_trace"` over `engineering/ingestion/sources/` returns **zero**. **Held out, and deliberately NOT written to the ingestion tree.** |
>
> 🔴 **Why the io_pin_timing block was not "written to the ingestion tree first".** The C6 instruction
> offers that as the fix for a not-actionable block with no ingestion home. It is the wrong move here,
> and the reason generalises: **`engineering/ingestion/sources/` mirrors INGESTED SOURCE DOCUMENTS.**
> Writing authored-here electronics lore into it would manufacture a Parallax-tier authority out of
> nothing — and that tree is inside `audit-constant-fidelity.py`'s declared *Parallax documentary*
> truth root, which is precisely the defect F-341 already files against six of our own derived
> analysis documents sitting at that tree's root. Curing a provenance hole by inventing provenance is
> worse than the hole. The block stays out; git holds it at `15c84de5^` for anyone who wants it.
>
> **The generalizable half — sub-rule P needs a fourth branch, not a third.** «#298»'s *Sharpening*
> §3 already added *"authored-here content with no upstream at all — stays, and say why"*. That
> branch assumes the block is still **in** the KB, where "stays" is an available answer. Once a purge
> has removed it, "stays" is gone and the only choices are *invent an upstream* or *record the
> absence*. The rule wants: **authored-here, no upstream, ALREADY REMOVED → record it as a gap with
> the acquisition that would close it; never manufacture the source.**
>
> **What would settle each:**
> - *Click*: ingest the Parallax **P2 Eval Click Adapter** product documentation (the MikroBUS
>   offset map and the adapter's base-pin positions). That single ingestion would ground both this
>   block and the `p2_adapter_mapping` offsets the file already ships uncited.
> - *io_pin_timing*: nothing Parallax can settle — it is not a P2 fact. It closes by staying closed.
>
> ⚠️ **Also found while filing:** this register's header reads **`Next gap ID: G-007`**, but
> `engineering/ingestion/KNOWLEDGE-GAPS.md` already allocates **G-007** (Smart Pins / ADC, ANSWERED
> 2026-08-24). The counter is stale by one and the next free gap ID is **G-008**. «#299» allocated no
> G-number rather than collide; the header is left for whoever owns that ledger to correct
> deliberately.

---

## `hardware/` repopulated from the board guides — the return record, and the wrong scalars the source-first read exposed (2026-08-25, «#307» Plan §8 part 2) — F-353 · F-354

> **Origin.** «#294» removed 59 quantitative blocks from `deliverables/ai/P2/hardware/` (F-334, two
> records: 48/16 files and 11/6 files). «#298» dispositioned every one. «#307» worked the **board
> guides**, not the removal list, and wrote back what each guide states. One of the 11 —
> `language/spin2/methods/getct.yaml description` — is outside this tree and belongs to «#299», so
> **58** were in scope here. Every line number below was read off disk 2026-08-25.

### F-353 — the 58 in-scope blocks: 34 returned cited, 24 held in the ingestion tree, 0 whole-block gaps — and six wrong scalars in SURVIVING blocks that only a source-first read could find — `PENDING-VALIDATION`

> **THE THREE NUMBERS.** **34 restored with a trace · 24 held in ingestion · 0 gap.** 34 + 24 = 58;
> plus «#299»'s `getct.yaml description` = F-334's 59. Every ACTIONABLE block came back; no
> ACTIONABLE block failed to verify.
>
> **Restored (34), each written from the guide named in its own `source:` key:**
>
> | File (`deliverables/ai/P2/hardware/`) | Blocks returned | Written from |
> |---|---|---|
> | `edge-32mb-module.yaml` | `specifications` · `pin_mapping` · `boot_modes` · `limitations` · `development_workflow` | P2-EC32MB Edge Module Rev B Guide v2.0 — `sources/edge-32mb-module/edge-32mb-module-narrative.txt` |
> | `edge-standard-module.yaml` | `specifications` · `pin_mapping` · `boot_modes` | P2-EC Edge Module Rev D Product Guide v3.0 — `sources/edge-standard-module/edge-standard-module-narrative.txt` |
> | `p2-eval-board.yaml` | `specifications` | #64000 Eval Board Rev C Guide v2.0 — `sources/p2-eval-board/complete-p2-eval-board-reference.md` (the F-250 forced-OCR re-ingestion) |
> | `addon-motor-driver.yaml` | `signal_map` · `pwm_control` · `current_sense` · `specifications` | #64010 Universal Motor Driver Guide v2.0 — `sources/p2-universal-motor-driver/complete-p2-universal-motor-driver-content.md` |
> | `hub75_adapter.yaml` | `description` · `specifications` · `software_features` · `notes` | #64032 HUB75 Adapter Official Specifications — `sources/p2-hub75-adapter/p2-hub75-adapter-official-specs.md` |
> | `programming-prop-plug.yaml` | `description` · `reset_option` · `specifications` | #32201 Prop Plug Guide v3.0 Rev E — `sources/propplug-rev-e/complete-propplug-rev-e-reference.md` |
> | `addon-serial-host.yaml` | `signal_map` · `usb_host_capabilities` · `development_workflow` | #64006 Series Guide v2.0 — `sources/p2-eval-add-on-boards/p2-eval-add-on-boards-text.txt:99-134` |
> | `addon-serial-device.yaml` | `description` · `signal_map` | same guide, `:253-284` |
> | `addon-goertzel-touch.yaml` | `specifications` | same guide, `:24-46` + `:290-317` |
> | `addon-hd-audio.yaml` | `description` · `dac_board` | #64014 HD Audio Guide v1.0 — `sources/P2-HD-Audio-Add-on/P2-HD-Audio-Add-on-text.txt` |
> | `addon-hyperram-hyperflash.yaml` | `specifications` · `configuration` | #64004-ES Guide v1.0 — `sources/hyperRam-n-hyperFlash/complete-hyperram-hyperflash-reference.md` |
> | `addon-rtc.yaml` | `description` | #64013 RTC Guide v1.0 — `sources/P2-RTC-Add-on/P2-RTC-Add-on-text.txt:15-37` |
> | `addon-wx-wifi.yaml` | `pin_descriptions` | #32420 WX Wi-Fi Module Guide v1.0 — `sources/parallax-wx-wifi/complete-wx-wifi-reference.md:96-114` |
> | `edge-mini-breakout.yaml` | `connectivity` | #64019 Mini Breakout Guide v1.1 — `sources/edge-mini-breakout/edge-mini-breakout-narrative.txt` |
> | `edge-standard-breakout.yaml` | `connectivity` | #64029 Breakout Board Guide v1.0 — `sources/edge-breakout-board/edge-breakout-board-narrative.txt` |
>
> **Held in ingestion (24)** — CORRECT-BUT-NOT-ACTIONABLE per «#298», and each one's content is
> demonstrably still readable in the ingestion tree, so removing it from the KB lost nothing:
> `addon-hd-audio` `set_contents` (`P2-HD-Audio-Add-on-text.txt:17`) · `use_cases` (`:32-35`) ·
> `addon-motor-driver` `power_signals` (`complete-p2-universal-motor-driver-content.md:154-160`) ·
> `protection` (`:41`, `:170`) · `addon-rtc` `power_signals` (`P2-RTC-Add-on-text.txt:56`, `:68`) ·
> `specifications` (`:41-52`, `:89-93`) · `addon-wx-wifi` `part_variants`
> (`complete-wx-wifi-reference.md:5`, `:26-29`) · `specifications` (`:44-61`) ·
> `edge-breadboard-carrier` `power_specifications` / `specialized_features` / `specifications`
> (`edge-module-breadboard-narrative.txt:53-57`, `:60-69`, `:163`, `:167-171`) ·
> `edge-mini-breakout` `power_management` / `specifications`
> (`edge-mini-breakout-narrative.txt:43`, `:54-65`) · `edge-standard-breakout` `power_management` /
> `specifications` (`edge-breakout-board-narrative.txt:35-36`, `:42-64`, `:191`) ·
> `addon-hyperram-hyperflash` `host_note` (`complete-hyperram-hyperflash-reference.md:95-96`) ·
> `addon-serial-device` `rev_b_5v_note` (`p2-eval-add-on-boards-text.txt:113-115`;
> `boards/addon-serial-device-64006f.md:25`) · `specifications` (`:39-42` — see F-354 for the one
> item of it that is NOT there) · `addon-serial-host` `description` / `limitations` /
> `power_requirements` / `specifications` (`:99-115`, `:39-42`) · `edge-standard-module`
> `revision_history` (`edge-standard-module-narrative.txt:519-551`) · `hub75_adapter`
> `power_requirements` (`p2-hub75-adapter-official-specs.md:128-142`, with the caveat in F-354).
>
> 🔴 **SIX WRONG SCALARS IN BLOCKS THE PURGE NEVER TOUCHED.** Reading the guides rather than the
> removal list is what surfaced these; a citation-keyed purge is structurally blind to all of them
> (the same lesson F-328(b) records). All six are **corrected in place** and cited:
>
> | Where | Shipped | The guide says |
> |---|---|---|
> | `edge-32mb-module.yaml` `alternate_part` + one alias + `availability.part_lookup` | `64000-ES` | The guide names this module **#P2-EC32MB** throughout (`edge-32mb-module-narrative.txt:17`, `:41`, `:46`, `:557`). **#64000-ES is a different product** — the limited-edition P2-ES *Eval Board* (`p2-eval-add-on-boards-text.txt:42`; `hyperram-hyperflash-text.txt:22`). A search for the eval board was landing on the edge module. The bad identity traces to a derived analysis file, `sources/edge-32mb-module/edge-32mb-cross-source-analysis.md:16`, not to the guide. |
> | `edge-standard-module.yaml` `comparison_with_32mb.ec32mb_module.fully_free_pins` | `38` | **40** — "Smart I/O pins: 46 accessible, 40 fully free" (`edge-32mb-module-narrative.txt:120`) and "P0-P39 are fully free" (`:417`). The same file's own `compatibility.alternatives.tradeoff` already said 40, so the file contradicted itself. |
> | `edge-mini-breakout.yaml`, `edge-standard-breakout.yaml`, `edge-breadboard-carrier.yaml` — `advantages`, `development_workflow`, `programming.methods`, and the carrier's `connectivity.programming` | "USB programming integrated", "USB (primary - built-in)", "Built-in USB-to-serial", "Connect USB for programming and power" | **None of the three Edge carriers has a USB-to-serial converter.** All three guides say the same thing: "Programming: Serial up to 2 MBaud; **requires** Prop Plug (#32201) programming adapter" (`edge-mini-breakout-narrative.txt:60-61`, `edge-breakout-board-narrative.txt:59`, `edge-module-breadboard-narrative.txt:67`). An agent told the board has built-in USB emits no Prop Plug step at all. Class-wide sweep run: `grep -rn "built-in\|integrated" … hardware/` — the only remaining "USB (primary method)" is `p2-eval-board.yaml:190`, where it is **correct** (the #64000 does carry a built-in FTDI-to-USB interface, `complete-p2-eval-board-reference.md:78`). |
> | `edge-mini-breakout.yaml` `pin_access.blocked_pins` | `P32-P55 (not accessible)` | "Pins P32–P55 **may be accessed** by adding jumper wires on the bottom side of the PCB to the mini prototyping sections" (`edge-mini-breakout-narrative.txt:31-33`). Not accessible *at a header*; not unreachable. |
>
> **F-350's five, and eleven more of the same class, in `p2-hardware-feature-comparison.yaml`.**
> F-350 named five wrong keys still shipping in that file. Correcting them source-first meant
> reading every quantity in the file, and the fabrication went well past five — see the file's own
> `corrections_applied_2026_08_25` keys for the full list. Beyond F-350's five: all three Edge
> carriers carried **invented part numbers** (`P2-EVAL-STD-BREAKOUT`, `P2-EVAL-MINI-BREAKOUT`,
> `P2-EVAL-BREADBOARD-CARRIER` — the real parts are #64029, #64019, #64020) and wrong dimensions;
> the mini breakout was described as "3.3V input only" with "All 64 pins on edge castellations"
> (it is 5 VDC via a barrel jack, with 40 pins at 0.1″ headers); both edge modules carried
> `27×40mm` (the guides say 37 × 51.7 mm); the eval board's programming interface read "USB-C +
> micro-USB + PropPlug header" and its power input "5V USB or 6-15V barrel jack" (the #64000 has
> **two micro-USB sockets and no barrel jack at all**); and **`64006G` was described as a "Combined
> Digital I/O" board with 4 LEDs and 4 switches** — #64006G is the **Goertzel** board, which is the
> F-121 fabricated-board-name family reappearing in a file F-121 never named. All corrected or
> removed against the guides, with a `source:` per block.
>
> **Gate effect, measured.** `audit-yaml-claim-sourcing.py` Tier 1 stayed at **0** across all edits.
> Tier 2 moved **84 → 78**: the six `p2-hardware-feature-comparison.yaml` blocks left the advisory
> lane because that file now cites. The `hardware/` share went 39 → 33. Nothing changed tier in the
> other direction, and no block was demoted.
>
> Status: `PENDING-VALIDATION` — every edit is applied and gate-verified; only the YAML release is owed.

### F-354 — seven content-level holes inside blocks that DID come back, and one held block whose content is only three-quarters in the ingestion tree — `CONFIRMED`

> **Why these are not "gaps" in the three-number sense.** Every ACTIONABLE block returned. What did
> not return is *material inside* those blocks — figures the KB shipped that no ingested source
> states. Each is recorded in the YAML itself, at the point of use, with what would settle it, so a
> reader meets the hole where the fact would have been rather than in a register they may not open.
>
> | Hole | Where it is recorded | What would settle it |
> |---|---|---|
> | HUB75 max clock **40 MHz (35 MHz reliable)** and **13 ns propagation delay** | `hub75_adapter.yaml` `specifications.gap_max_clock` | A level-shifter datasheet, or a measured result in `P2-EMPIRICAL-FINDINGS.md`. ⚠️ The manufacturer's own capture says **70 MHz** (`p2-hub75-adapter-official-specs.md:22`) — the two differ by ~2x and the KB now carries only the sourced figure. |
> | HUB75 **clock/latch/OE pulse-width minimums** (15 ns / 200 ns / 100 ns) and the 3-bit/8-bit refresh table | `hub75_adapter.yaml` `software_features.gap_pulse_widths` | Ingesting the ISP HUB75 driver's own documentation into `engineering/ingestion/sources/`. |
> | HUB75 **"maximum 3 chains"** and **"driver does not use the P2 streamer"** | `hub75_adapter.yaml` `notes.gap_chain_limit` | Same ingestion. The pinout capture argues the opposite for the second (`p2-hub75-adapter-complete-pinout.md:90`, "6-bit parallel data perfect for P2 streamer"). |
> | HUB75 **board current 35 mA @ 35 MHz** and the per-panel typical currents | `hub75_adapter.yaml` `power_requirements` is HELD, but its ingestion home states **under 50 mA** and **1-2 A** where the KB said 35 mA and 1.5 A (`p2-hub75-adapter-official-specs.md:126`, `:131-136`) | Same ingestion. The held block's numbers are NOT the ingestion tree's numbers — a re-check before anyone quotes the removed values from git. |
> | **"One cog consumed by the PSRAM driver"** on the 32 MB module | `edge-32mb-module.yaml` `development_workflow.psram_driver_note` | The #P2-EC32MB guide neither ships nor describes a PSRAM driver. Ingesting the OBEX `psram.spin2` driver documentation would ground it (and the API already sitting in that file's `code_patterns`). |
> | Whether the **#64013 RTC board carries its own SDA/SCL pull-ups** | `addon-rtc.yaml` `pin_mode_tip.scl_pull_up_caveat` | The #64013 board schematic (referenced by the guide, not ingested). |
> | Numeric **PCB dimensions for the #64006 add-on boards** | `addon-goertzel-touch.yaml` `specifications.pcb_size_class` | The guide gives only a drawing and a three-size classification (`p2-eval-add-on-boards-text.txt:45-46`, `:381-396`); the drawing was never resolved to numbers. Re-cutting that page, or the board schematics. |
> | `addon-serial-device.yaml` `specifications` — **the "3.3 V supply" item** | held block | `grep -n -i "3\.3 *v\|3v3"` over the whole #64006 guide and all eight per-board captures returns **one** hit, and it is the A/V board's audio tip. The mounting-hole figures (3.2 mm / 5 mm / 9.5 mm) ARE in the ingestion tree at `:39-42`; the supply voltage is not. Three-quarters held, one quarter a gap. What would settle it: the #64006 board schematics. |
>
> Status: `CONFIRMED`.

---

## `hardware/p2-eval-board.yaml` describes a board the #64000 guide does not (2026-08-24, F-250 re-ingestion) — F-328

> **Origin.** Repairing the #64000 source (F-250 — its extraction had lost every numeral)
> made it possible, for the first time, to check the board YAML against what the guide
> actually says. Every item below was read off the repaired capture
> (`engineering/ingestion/sources/p2-eval-board/complete-p2-eval-board-reference.md`) and
> confirmed on the rendered page. **Nothing here is fixed in this filing** — the ingestion
> head produces raw source data; the YAML is the purge/repopulate tasks' work.

- **F-328 — `deliverables/ai/P2/hardware/p2-eval-board.yaml` carries claims the #64000 Rev C
  guide contradicts, plus whole blocks describing hardware the board does not have; and the
  guide itself contradicts itself on one pin pair.** — `PENDING-VALIDATION` · Two separable halves.

  **(a) The source contradicts itself — a genuine documentary conflict, not an extraction
  defect.** The #64000 guide's §18 "microSD Card Socket" (p.12) lists *"P58 - DI/CD (data in
  and card detect); P59 - DO (data out); P60 - /CS; P61 - CLK"*. Its own I/O Pin Assignments
  table (p.15) lists *"P58 microSD MISO (SDO); P59 microSD MOSI (SDI); P60 microSD CS; P61
  microSD CLK"*. P60/P61 agree; **P58 and P59 are opposite in direction between the two
  places**. Both readings are confirmed on the rendered pages and in the original text layer
  (whose table font preserved the fragments `" D MI O ( DO)"` / `" D MO I ( DI)"`). The guide
  does not resolve it, and this source alone cannot settle which is right.

  **RESOLVED 2026-08-24 by cross-source normalization — no bench, no schematic needed.** The
  answer is **P58 = MISO** (card `DO`, a P2 *input*) and **P59 = MOSI** (card `DI`, a P2
  *output*). The guide's own p.15 I/O table is **correct**; its §18 bullet list is a
  **documentary error in the source** and is recorded as errata. Five independent authorities
  agree, in descending strength:
  1. **`engineering/ingestion/sources/rom-booter/rom_booter_v33_01j.lst:135-138`** — the P2's
     own boot ROM, which is the implementation itself and therefore conclusive:
     `spi_cs = 61 'pin SPI memory select (also sd_ck)` · `spi_ck = 60 '...clock (also sd_cs)` ·
     `spi_di = 59 'pin SPI memory data in (also sd_di)` · `spi_do = 58 'pin SPI memory data
     out (also sd_do)`. It names `sd_di` = **59** and `sd_do` = **58** outright.
  2. **`sources/silicon-doc/p2-documentation.txt:9281-9302`** — the boot-pin table, flattened
     by extraction but unambiguous once re-columned: `P59 (output)` ↔ SPI flash `DI (input)` ↔
     SD card `DI (input)`; `P58 (input)` ↔ flash `DO (output)` ↔ SD `DO (output)`. Note the SD
     column swaps CLK/CSn relative to flash (P61 = SD CLK, P60 = SD CSn), which independently
     corroborates §18's *"P60 - /CS; P61 - CLK"*.
  3. **`sources/p2-eval-board/complete-p2-eval-board-reference.md`** (the repaired capture of
     this very guide) — p.15 I/O table: P58 microSD MISO (SDO), P59 microSD MOSI (SDI).
  4. **`sources/p2-microSD-addon/64009-P2-microSD-AddOn-Guide-v1.0.md:41-42`** — supplies the
     vocabulary key that makes the two statements comparable at all: *"MOSI → Connects to
     SD-DI (CMD/MOSI)"* and *"MISO → Series 240R from SD-DO (MISO)"*. So card `DI` ≡ bus
     `MOSI` and card `DO` ≡ bus `MISO`; the two guides are not using different conventions.
  5. **`sources/p2-board-pin-mapping-knowledge.md:129-130`** — P58 = Flash SPI DO/MISO,
     P59 = Flash SPI DI/MOSI.

  **Consequence: the KB is already correct and must NOT be changed.**
  `P58: "microSD MISO (SDO) / Flash SPI DO"` stands, now with an authority behind it rather
  than a coin flip. Half (a) is therefore **not** a KB defect and is **not** work for the
  repopulation tasks — it is a source errata plus a citation. When «#307» repopulates the
  microSD block, cite the ROM booter (1) or the silicon-doc boot table (2), **never §18**.
  *Lesson worth keeping: the apparent contradiction was legible only after a third source
  supplied the DI/DO ↔ MOSI/MISO vocabulary key. A two-source conflict is sometimes a missing
  translation, not a disagreement — check for the key before escalating to the bench.*

  **(b) The YAML asserts hardware the guide does not describe.** Uncited *and* wrong, which is
  why it is filed rather than left to the uncited-block purge — a purge keyed on missing
  citations will not necessarily reach a scalar or a whole fabricated section:
  - `specifications.microcontroller.revision: "Rev D"` — the guide is **Rev C silicon**
    throughout (`P2X8C4M64PES`, "Rev C Silicon", "Rev C silicon approved for production").
  - `clock_speed: "20MHz crystal, PLL to 320MHz"` — the guide states 20 MHz crystal,
    **recommended maximum 180 MHz**, "overclocking possible beyond 300 MHz", and a **390 MHz**
    experiment. `320MHz` appears nowhere.
  - `built_in_peripherals.proto_area.breadboard_section: "Basic prototyping area"` — **the
    #64000 has no prototyping area.** Fabricated whole.
  - the `video_audio:` block (`vga_support` / `hdmi_support` / `audio_output`) — the guide
    never mentions VGA, HDMI, video, or resistor DACs. Fabricated whole.
  - `connectivity.programming` lists a **Prop Plug (#32201) on a "4-pin header"** and
    `connector: "USB-B or USB-C"` — the guide describes **micro-USB** only, plus the WX WiFi
    SIP module (#32420S) on the P56–P63 header. It never mentions a Prop Plug.
  - `switches.user_switches: "TBD quantity"` — there are none; the switches are the reset
    button and a **4-position mode dip bank** (USB RES · FLASH · P59 △ · P59 ▽).
  - `headers.connector_type: "Standard 0.1 inch headers"` — the I/O breakout headers are
    **2×6 edge headers** (eight of them); the 0.1″-spaced feature is the AUX power **pads**.
  - `flash_size: "TBD - check documentation"`, `physical.dimensions: TBD`,
    `temperature_range: "Commercial grade"`, `current_consumption: "TBD"` — the guide states
    **16 MB (128 Mbit) W25Q128JVSIM**, **3.55″ × 3.55″** with four mounting holes 40 mm apart,
    and **−40 to +85 °C**. These are `TBD` only because the extraction had no digits in it.
  - `supply_voltage: "5V or USB powered"` — the guide: **two micro-USB** inputs (PC-USB
    500 mA, AUX-USB 2000 mA), absolute maximum **5.5 VDC**, plus optional 5V/GND AUX pads at
    4.5–5.5 V. There is **no barrel jack**.
  - `expansion_ecosystem.individual_addons` names #64032 HUB75 and #64008 MicroBUS — not in
    this source (they may be sourced elsewhere; that is the repopulation step's call).

  **→ the sprint's purge/repopulate tasks** (remove-all, then re-derive source-first from the
  repaired capture). Do **not** cite-in-place: half of (b) would then acquire a citation to a
  guide that says the opposite. Half (a) is **closed** — see the resolution above; it needs a
  citation swap, not a decision.

  > **PURGE PASS APPLIED 2026-08-24 («#294») — it reached FOUR of the ten (b) items; SIX stand.**
  > The uncited-block purge removed exactly one top-level block from this file,
  > `specifications` (was `:24-56`, 33 lines). **What that took out (4 of 10):** the `Rev D`
  > scalar (`specifications.microcontroller.revision`, was `:27`); `clock_speed: "20MHz crystal,
  > PLL to 320MHz"` (was `:29`); `supply_voltage: "5V or USB powered"` (was `:52`); and the four
  > TBDs whose answers are in the repaired guide — `flash_size` (was `:37`), `physical.dimensions`
  > (was `:44-48`), `current_consumption` (was `:54`), `temperature_range` (was `:55`).
  >
  > **What SURVIVES the purge, untouched, and is therefore still owed to «#307»** (post-purge
  > line numbers, file is now 172 lines):
  > - `built_in_peripherals.proto_area` (`:54-56`) — the **fabricated prototyping area**.
  > - `switches.user_switches: "TBD quantity"` (`:48`).
  > - `headers.connector_type: "Standard 0.1 inch headers"` (`:52`).
  > - the whole `video_audio:` block — `vga_support` / `hdmi_support` / `audio_output`
  >   (`:70-73`). Fabricated whole; still standing.
  > - `connectivity.programming` (`:58-65`) — `connector: "USB-B or USB-C"` and Prop Plug
  >   **#32201**.
  > - `expansion_ecosystem.individual_addons` (`:127-134`) — #64032 HUB75 / #64008 MicroBUS.
  >
  > **Why all six were missed — one reason, measured, not the one that looks likely.** Each of
  > the four surviving blocks (`built_in_peripherals`, `connectivity`, `video_audio`,
  > `expansion_ecosystem`) states **zero unit-bearing quantities**: "0.1 inch", "16 MB", "32 MB",
  > "4-pin", "#32201" carry no unit the gate counts (inch, MB and bare integers are structure by
  > design). A quantity-keyed gate therefore never looks at any of them. Note what is NOT the
  > cause: `built_in_peripherals` does carry a genuine `source:` for the LED bank (`:45`), which
  > would have silenced it too — but that is belt-and-braces, not the operative reason, and the
  > other three carry no citation at all and were still passed over.
  >
  > **The generalizable lesson:** a purge keyed on MISSING CITATIONS is orthogonal to a WRONG
  > SCALAR and to an INVENTED SECTION. It caught the four items that happened to carry volts,
  > megahertz, or a `TBD` inside a quantitative block, and passed over the six that are pure
  > prose — including both wholly fabricated sections. Removal is not a substitute for the
  > re-derivation; it guarantees only that what remains was never *uncited*, never that it is
  > *true*.

  > **(b) CLOSED OUT 2026-08-25 («#298» + «#307»).** «#298» removed five of the six surviving
  > items as UNSOURCED and kept `expansion_ecosystem.individual_addons` (a cross-reference roster,
  > not a fabrication). «#307» then wrote the TRUE replacements back as a cited `specifications`
  > block on `p2-eval-board.yaml`, source-first from the repaired capture: Rev C silicon
  > (P2X8C4M64PES), 20 MHz crystal with a recommended maximum of 180 MHz, 16 MB W25Q128JVSIM,
  > 3.55 in x 3.55 in, -40 to +85 C, two micro-USB inputs (500 mA / 2000 mA) with an absolute
  > maximum of 5.5 VDC, eight I/O Pin Breakout Edge Headers, and the four-switch mode bank
  > (USB RES · FLASH · P59 up · P59 down) in place of the "TBD quantity" user switches. The
  > fabricated prototyping area, VGA/HDMI/audio block, USB-B/USB-C connector and Prop Plug #32201
  > are gone and were not written back. See **F-353**.

  Status: `PENDING-VALIDATION` — **(a) RESOLVED 2026-08-24** by cross-source normalization against
  the ROM booter and the silicon-doc boot table: P58 = MISO / P59 = MOSI, the KB is already correct
  and stands unchanged, and the guide's §18 is source errata. **(b) applied 2026-08-25** as
  described above; only the YAML release is owed.

---

## The `architecture/`/`language/`/`guides/`/`application-notes/` uncited-block purge — the removal record «#293» owed and did not write (2026-08-25, arbiter) — F-347

> **Why this exists.** «#293»'s own PROTECTION POINT required *"every removal recorded with its
> origin so «#299» can work from a list rather than from git archaeology."* It was not written —
> its executor mirrored only the `io_pin_timing.yaml` portion into the register and left the rest
> in its transcript, which does not survive. **The arbiter verified that task green without
> checking that specific deliverable; that is the miss, and it is the arbiter's, not the
> executor's.** Caught at «#298»'s entry, because «#298» population 2 and «#299» both consume this
> list.
>
> **Reconstructed mechanically** from `git show --unified=0 15c84de5 -- deliverables/ai/P2/`,
> taking every removed line that begins a top-level YAML key. Nothing is lost — the purge is fully
> recoverable from git — but recoverable is not the same as recorded, and a list nobody can find
> is a list that gets re-derived under time pressure.
>
> ⚠️ **COUNT DISCREPANCY, STATED RATHER THAN SMOOTHED: this reconstruction yields 60 top-level key
> deletions; the executor reported 59 blocks.** The likely cause is one key counted differently
> (a `description:` removed as part of a larger block, or a nested key at column 0). «#298» and
> «#299» should work the 60 and treat any that resolves to "was never a block" as a no-op rather
> than assume the reconstruction is wrong. Do not reconcile to 59 by deleting a row.
>
> **Sibling records:** «#294»'s two are in F-334 above (48 blocks / 16 files, and 11 / 6).
>

- **F-347 — «#293»'s removal record was never written, so 60 removed blocks existed only in a git
  diff and in a transcript that does not survive.** — `PARTIAL`

  > **Headline corrected `PENDING-VALIDATION` → `PARTIAL` 2026-08-25 («#302»), to agree with this
  > entry's own Disposition line.** `PENDING-VALIDATION` asserts the fix is fully applied and only
  > its validation is owed; that is not this entry's state. The Disposition sets the closing
  > condition as *"every row carries a returned/not-returned outcome"*, and **the reconstructed
  > table below still has four columns — File · block · pre-removal line · span — and no outcome
  > column at all.** «#299» did execute against it (F-352: *"Forty-five of F-347's sixty blocks came
  > back cited. Two did not"*), so **47 of the 60 rows are accounted for in narrative** — but the
  > record itself carries no outcome column, and the remaining **13 rows are not accounted for by
  > that sentence** (whether each is held in the ingestion tree or simply unstated was NOT
  > determined here — that determination is part of the work this entry still owes). Writing the
  > outcomes onto the rows is **work**, not validation. This disagreement was invisible to check 10 for the same
  > reason as F-355's: the entry declares its status as an indented `Disposition.`/`Status:` line
  > rather than a column-0 `**Status:**`.

  «#293» removed 59-60 uncited quantitative blocks from `architecture/`, `language/`, `guides/`
  and `application-notes/`, and its PROTECTION POINT required that every removal be recorded with
  its origin *"so «#299» can work from a list rather than from git archaeology."* The executor
  mirrored only the `io_pin_timing.yaml` portion into the register. The remainder was left in its
  transcript.

  **The arbiter passed that task green without checking that deliverable.** The other protection
  criteria — the four entry gates, the zero Tier-1 count, the crossref clean — were all verified
  and all held; the *record* was the one criterion nobody re-ran, because it is the only one with
  no instrument behind it. That is the generalizable lesson: **a protection-point criterion that
  no tool can check is the criterion that silently does not happen**, and it needs a named,
  eyes-on verification step rather than inheriting the confidence of the gates around it.

  Reconstructed mechanically at «#298»'s entry (the first task to consume it) from
  `git show --unified=0 15c84de5 -- deliverables/ai/P2/`. The table above is that reconstruction.
  Nothing was lost — a purge is fully recoverable from git — but *recoverable* is not *recorded*,
  and a list nobody can find is a list that gets re-derived under time pressure by whoever needs
  it next.

  **EXECUTED 2026-08-25 by «#299». Every one of the 60 rows now carries an outcome, and the
  count is stated in four numbers rather than one total:**

  | Outcome | Count | What it means |
  |---|---|---|
  | **restored with a trace** | **45** | The repaired source states it and it is ACTIONABLE. Every returned block carries a `source:` naming the document and a `file:line`. |
  | **held out — no ingestion home** | **1** | `architecture/io_pin_timing.yaml best_practices` (generic PCB-layout advice). CORRECT-BUT-NOT-ACTIONABLE per «#298»; see F-352 for why it was not written to the ingestion tree either. |
  | **gap** | **1** | `architecture/click_module_integration.yaml best_practices` — ACTIONABLE per «#298», but no ingested source states any of it. See F-352 for what would settle it. |
  | **never returns (UNSOURCED)** | **13** | The F-327 fabrication family, ruled by «#298». Re-verified absent at HEAD: all nine `io_pin_timing.yaml` keys and all four `basic-io.yaml` twins return `grep -c` = 0, and `grep -rn "150mA\|75mA\|~2000Ω\|3-7ns\|pull_up_modes\|pull_down_modes"` over `deliverables/ai/P2/` returns **0**. |

  45 + 1 + 1 + 13 = 60. **The dispatch's own numbers were checked against disk:** the body's "65
  blocks" is wrong (it is 60, as this entry already recorded), and the register header's
  **`Next gap ID: G-007` is stale** — `engineering/ingestion/KNOWLEDGE-GAPS.md` already allocates
  G-007 (Smart Pins / ADC, ANSWERED 2026-08-24). No G-number was allocated by «#299» for that
  reason; its gap is filed as F-352 instead.

  Two blocks were returned **corrected rather than verbatim**, as C4 required: both
  `internal_pull_resistors` blocks now teach the hardware-verified `P_HIGH_15K` + DIR-high /
  `P_LOW_15K` + DIR-low form from `architecture/pin-drive-configuration.yaml idioms` (EF-063,
  EF-064), and neither reintroduces a `pull_up_modes:` / `pull_down_modes:` key. Both
  `pin_architecture` blocks returned without the `drive_strength: 1.5mA to 150mA` line.

  `PENDING-VALIDATION` — the record is written and executed against; only the YAML release is owed.

### Removal record — «#293», reconstructed by the arbiter 2026-08-25

| File | Top-level block removed | pre-removal line | span |
|---|---|---|---|
| `application-notes/p2an001-single-pin-instrumentation-adc.yaml` | `gotchas` | 92 | 16 |
| `application-notes/p2an002-cordic-for-real-work.yaml` | `gotchas` | 102 | 14 |
| `application-notes/p2an003-dac-analog-signal-generation.yaml` | `key_parameters` | 91 | 13 |
| `application-notes/p2an004-frequency-rotation-rc-timing-measurement.yaml` | `gotchas` | 97 | 16 |
| `architecture/boot-rom/_index.yaml` | `boot_timing` | 25 | 6 |
| `architecture/boot-rom/_index.yaml` | `boot_paths_summary` | 155 | 18 |
| `architecture/boot-rom/boot-pattern-selection.yaml` | `boot_time_clock_state` | 64 | 27 |
| `architecture/boot-rom/boot-pattern-selection.yaml` | `pin_triple_duty` | 64 | 27 |
| `architecture/boot-rom/spi-flash-boot.yaml` | `boot_pattern_trigger` | 29 | 7 |
| `architecture/click_module_integration.yaml` | `best_practices` | 185 | 25 |
| `architecture/clock_system.yaml` | `configuration_constants` | 22 | 34 |
| `architecture/clock_system.yaml` | `configuration_rules` | 22 | 34 |
| `architecture/clock_system.yaml` | `pll_system` | 98 | 65 |
| `architecture/clock_system.yaml` | `hubset_configuration` | 98 | 65 |
| `architecture/clock_system.yaml` | `clock_modes` | 98 | 65 |
| `architecture/clock_system.yaml` | `stabilization_timing` | 175 | 6 |
| `architecture/clock_system.yaml` | `clock_specifications` | 253 | 15 |
| `architecture/clock_system.yaml` | `anti_patterns` | 279 | 21 |
| `architecture/io_pin_timing.yaml` | `description` | 10 | 6 |
| `architecture/io_pin_timing.yaml` | `timing_specifications` | 90 | 173 |
| `architecture/io_pin_timing.yaml` | `clock_relationships` | 90 | 173 |
| `architecture/io_pin_timing.yaml` | `drive_strength_configurations` | 90 | 173 |
| `architecture/io_pin_timing.yaml` | `slew_rate_control` | 90 | 173 |
| `architecture/io_pin_timing.yaml` | `input_characteristics` | 90 | 173 |
| `architecture/io_pin_timing.yaml` | `special_timing_modes` | 298 | 40 |
| `architecture/io_pin_timing.yaml` | `protocol_timing_examples` | 298 | 40 |
| `architecture/io_pin_timing.yaml` | `compensation_techniques` | 359 | 33 |
| `architecture/io_pin_timing.yaml` | `best_practices` | 359 | 33 |
| `architecture/pin-power-domains.yaml` | `description` | 16 | 15 |
| `architecture/pin-power-domains.yaml` | `board_power_grouping` | 43 | 9 |
| `architecture/serial_loader.yaml` | `boot_sequence` | 11 | 26 |
| `architecture/smart-pins/smart-pin-00011-dac-16bit-pwm-dither.yaml` | `operation` | 21 | 6 |
| `architecture/smart-pins/smart-pin-00011-dac-16bit-pwm-dither.yaml` | `pin_behavior` | 55 | 7 |
| `architecture/smart-pins/smart-pin-00011-dac-16bit-pwm-dither.yaml` | `pwm_characteristics` | 189 | 5 |
| `architecture/smart-pins/smart-pin-11011-usb-host-device.yaml` | `detailed_description` | 8 | 13 |
| `architecture/smart_pin_patterns.yaml` | `notes` | 251 | 9 |
| `architecture/smart_pins.yaml` | `input_routing` | 148 | 19 |
| `architecture/smart_pins.yaml` | `related_components` | 405 | 7 |
| `architecture/smart_pins.yaml` | `electrical_limits` | 504 | 4 |
| `guides/pasm2-getting-started.yaml` | `file_structure` | 48 | 66 |
| `language/pasm2/concepts/basic-io.yaml` | `pin_architecture` | 40 | 49 |
| `language/pasm2/concepts/basic-io.yaml` | `control_registers` | 40 | 49 |
| `language/pasm2/concepts/basic-io.yaml` | `drive_strength_configuration` | 241 | 58 |
| `language/pasm2/concepts/basic-io.yaml` | `internal_pull_resistors` | 241 | 58 |
| `language/pasm2/concepts/basic-io.yaml` | `timing_considerations` | 371 | 6 |
| `language/pasm2/concepts/streamer_smartpin_control.yaml` | `protocol_client_code_note` | 480 | 8 |
| `language/pasm2/setxfrq.yaml` | `common_values` | 53 | 13 |
| `language/spin2/concepts/basic-io.yaml` | `pin_architecture` | 40 | 43 |
| `language/spin2/concepts/basic-io.yaml` | `control_registers` | 40 | 43 |
| `language/spin2/concepts/basic-io.yaml` | `drive_strength_configuration` | 173 | 66 |
| `language/spin2/concepts/basic-io.yaml` | `internal_pull_resistors` | 173 | 66 |
| `language/spin2/concepts/basic-io.yaml` | `timing_considerations` | 339 | 8 |
| `language/spin2/debug-commands/pc_key.yaml` | `description` | 4 | 5 |
| `language/spin2/debug-commands/pc_key.yaml` | `usage_rules` | 15 | 8 |
| `language/spin2/methods/getct.yaml` | `pitfalls` | 120 | 19 |
| `language/spin2/methods/waitms.yaml` | `notes` | 84 | 13 |
| `language/spin2/methods/waitms.yaml` | `limitations` | 84 | 13 |
| `language/spin2/methods/waitus.yaml` | `notes` | 92 | 20 |
| `language/spin2/methods/waitus.yaml` | `limitations` | 92 | 20 |
| `language/spin2/methods/waitus.yaml` | `clock_frequency_impact` | 92 | 20 |

**60 top-level blocks across 25 files.**

> **Disposition.** `PARTIAL` — the record exists now and is usable; it closes when «#299» has
> executed against it and every row carries a returned/not-returned outcome.

---

## The `hardware/` uncited-block purge — the removal record, and a citation token that silences the gate (2026-08-24, «#294») — F-334

> **Origin.** Plan §4 part 2 removed all 48 Tier-1 uncited quantitative blocks from
> `deliverables/ai/P2/hardware/`, taking `audit-yaml-claim-sourcing.py` to **0 Tier 1 / exit 0**
> across 1129 files for the first time. Two things are recorded here: the **removal record**,
> which is «#307»'s working list (F8 — «#307» must not have to do git archaeology), and a
> detector defect the pass proved while working inside these files.

### Removal record — 48 blocks, 16 files, 2026-08-24

Line ranges are **pre-removal** (`git show 15c84de5:<path>` reproduces them). Every removal is a
whole top-level YAML key, the unit the gate measures. Nothing was reworded, repointed, or
partially trimmed; surviving keys were verified byte-equal at the parse against the
`.backups/…20260824-233259` copies.

  | File (`deliverables/ai/P2/hardware/`) | n | Blocks removed (pre-removal line range) |
  |---|---|---|
  | `addon-goertzel-touch.yaml` | 1 | `specifications` (74-87) |
  | `addon-hd-audio.yaml` | 4 | `description` (19-25) · `set_contents` (26-30) · `dac_board` (79-120) · `use_cases` (128-135) |
  | `addon-hyperram-hyperflash.yaml` | 2 | `specifications` (73-86) · `configuration` (87-100) |
  | `addon-motor-driver.yaml` | 6 | `signal_map` (45-62) · `power_signals` (63-68) · `pwm_control` (69-81) · `current_sense` (82-86) · `specifications` (87-110) · `protection` (111-116) |
  | `addon-rtc.yaml` | 3 | `description` (18-24) · `power_signals` (52-55) · `specifications` (97-113) |
  | `addon-serial-device.yaml` | 2 | `description` (16-23) · `signal_map` (36-69) |
  | `addon-serial-host.yaml` | 2 | `signal_map` (37-70) · `usb_host_capabilities` (93-111) |
  | `addon-wx-wifi.yaml` | 3 | `part_variants` (3-5) · `pin_descriptions` (78-91) · `specifications` (97-108) |
  | `edge-32mb-module.yaml` | 5 | `specifications` (44-255) · `pin_mapping` (256-405) · `boot_modes` (406-444) · `limitations` (665-675) · `development_workflow` (676-686) |
  | `edge-breadboard-carrier.yaml` | 3 | `specifications` (25-46) · `specialized_features` (73-92) · `power_specifications` (209-225) |
  | `edge-mini-breakout.yaml` | 3 | `specifications` (24-43) · `connectivity` (52-68) · `power_management` (184-190) |
  | `edge-standard-breakout.yaml` | 3 | `specifications` (24-42) · `connectivity` (50-66) · `power_management` (165-170) |
  | `edge-standard-module.yaml` | 3 | `specifications` (43-183) · `pin_mapping` (184-315) · `boot_modes` (316-354) |
  | `hub75_adapter.yaml` | 4 | `description` (13-17) · `specifications` (49-66) · `software_features` (135-185) · `notes` (212-219) |
  | `p2-eval-board.yaml` | 1 | `specifications` (24-56) |
  | `programming-prop-plug.yaml` | 3 | `description` (21-30) · `reset_option` (45-52) · `specifications` (53-64) |

**Findings that name content in this record:** F-328(b) (`p2-eval-board.yaml specifications` —
see that entry for the four items removed and the six that survive) · F-251 and F-252 (the Edge
module LED facts — both annotated in place with their new addresses). **The two heaviest losses
for «#307» to price:** `edge-32mb-module.yaml` 744→321 lines and `edge-standard-module.yaml`
582→270, because in both the entire `pin_mapping` went. Board-level pin maps **pass** the
actionability test (they change which pin numbers appear in generated code), so these are
high-priority repopulation, source-first from the Edge module guides.

- **F-334 — `audit-yaml-claim-sourcing.py` treats a board REVISION (`Rev B` / `Rev C`) and a
  POWER `source:` as citations, which silences the gate on 11 quantitative blocks that are as
  uncited as the 48 just removed.** — `PENDING-VALIDATION` — the gate's `INLINE_CITE_RE` includes `rev\s*[BC]\b`, which
  is a reasonable citation token in `Silicon Doc Rev C` prose and a **false positive** in a
  hardware file, where `Rev B` is the board's own identity: `board_revision: "Rev B (Guide
  v2.0)"`, or plain description text *"Goertzel experimenter board (Rev B) with pads…"*.
  Separately, `CITE_RE` matches any `source:` key — including
  `hub75_adapter.yaml` `source: P2 development board 5V supply` and
  `source: External 5V power supply (required)`, where "source" means a **power** source.

  **Both fire in the citation half only**, so the effect is a **false negative**: one such token
  anywhere in a top-level block marks the whole block cited and the gate never inspects it.
  **Measured, whole-KB, 2026-08-24 (after the purge):**

  | File | Block | qty | silenced by |
  |---|---|---|---|
  | `hardware/addon-hyperram-hyperflash.yaml` | `host_note` | 1 | `Rev B` |
  | `hardware/addon-serial-device.yaml` | `specifications` | 1 | `Rev B` |
  | `hardware/addon-serial-device.yaml` | `rev_b_5v_note` | 2 | `Rev B` |
  | `hardware/addon-serial-host.yaml` | `description` | 4 | `Rev B` |
  | `hardware/addon-serial-host.yaml` | `specifications` | 5 | `Rev B` |
  | `hardware/addon-serial-host.yaml` | `power_requirements` | 6 | `Rev B` |
  | `hardware/addon-serial-host.yaml` | `development_workflow` | 1 | `Rev B` |
  | `hardware/addon-serial-host.yaml` | `limitations` | 3 | `Rev B` |
  | `hardware/edge-standard-module.yaml` | `revision_history` | 6 | `Rev B`, `Rev C` |
  | `hardware/hub75_adapter.yaml` | `power_requirements` | 12 | the two power-`source:` keys |
  | `language/spin2/methods/getct.yaml` | `description` | 1 | `Rev B` |

  **Why «#294» did not act on it.** Three reasons, in order. (1) Its authority to touch the
  detector was bounded to a **proven false positive** — a block wrongly *flagged*; this is the
  opposite direction. (2) `hardware/addon-serial-host.yaml` alone would gain 5 blocks, and the
  purge's own success criterion is `hardware/` = 0, so acting would have made the task's gate
  unreadable mid-flight. (3) One of the 11 — `language/spin2/methods/getct.yaml` — is **outside
  `hardware/`**, in a tree «#293» already closed, which «#294» was forbidden to touch; fixing
  the detector without it would have left Tier 1 at 1 and the tool at exit 1, i.e. a green task
  reported red for a reason unrelated to its work.

  **Repaired 2026-08-24.** Both patterns were tightened around one principle: **a citation names
  a DOCUMENT, or an empirical record — not a hardware revision, and not a physical supply.**

  - `rev\s*[BC]\b` is **gone** from `INLINE_CITE_RE`. It was not replaced with an
    adjacent-to-a-document-word variant because the corpus says that is unnecessary: **every**
    real citation in all 1129 files that carries a revision also names the document it is a
    revision *of* — `"P2 Silicon Doc v35 (KNOWN BUGS, Rev C) -- verbatim"`, `"Propeller 2
    Documentation v35 - Rev B/C Silicon"`, `"#64000 … Eval Board Rev C Guide v2.0"` — so each is
    still recognised by `silicon doc`, `p2 documentation`, or the `guide` value token. Measured
    before deciding: **0 blocks and 0 files** in the KB rested on the revision token as their
    only *genuine* citation signal.
  - `CITE_RE` is replaced by `CITE_KEY_RE` + **`CITE_VALUE_RE`**: the key name is no longer the
    test, the **value** is. A key that introduces structure (`sources:` + a list, `source: |` +
    a block scalar) is tested against its nested body, which is where the document is named.
    The accept-vocabulary is drawn from the 88 corpus values that *are* citations, so every real
    short form still passes (`"P2 Datasheet"`, `"Silicon Doc v35"`, `"Hardware Manual
    2022-11-01"`, `"PNut v47 release notes"`, `flash_loader.spin2`, `parallax-quick-bytes`,
    `complete-builtin-symbols.md`, `…/P2-EMPIRICAL-FINDINGS.md EF-053`). Of the **312** cite-key
    lines in the corpus, **224 name no document at all** — power supplies, pattern-category tags
    (`source: motor_control`), event-name lists (`sources: ["CT-passed-CT1", …]`), compiler
    search paths (`source: "-I directories"`).

  **Negative control: 12 → 25 cases, 0 FAIL** (`--negative-control`, which now prints the count
  and its split: quantity 5 · region 7 · citation 13). The thirteen citation cases each state a
  real quantity, so none of them can pass by having nothing to find — what they measure is purely
  whether the block is judged *cited*. Six of them **FAIL against the shipped detector and PASS
  against the repaired one** (board revision · silicon revision in prose · `source:` naming a
  power supply · `source:` naming a host rail · `source:` naming a pattern category · `sources:`
  listing event names); the other seven prove a real citation is still recognised in each of its
  corpus spellings — short form, versioned, a genuine citation that *also* carries `Rev C`,
  `derived_from:` with a file+line, `verified_against:` with an EF number, a `sources:` list, and
  bare inline attribution with no cite key at all. No MUST-NOT-FIRE case regressed.

  **The instrument, before and after.** The repaired detector reported **4 Tier 1 / exit 1**, and
  the union of Tier 1 + Tier 2 went **84 → 95**: exactly the 11 blocks below became visible and
  **nothing disappeared**. After the removals it reads **0 Tier 1 / exit 0** with Tier 2 back at
  exactly **84** — which is the cross-check this entry asked for, satisfied: no file silently
  changed tier, the eleven were removed rather than demoted. The zero is now a *true* zero: the
  same tool failed, on this tree, an hour earlier.

### Removal record — 11 blocks, 6 files, 2026-08-24 (the same purge, finishing)

Line ranges are **pre-removal**. Every removal is a whole top-level YAML key; surviving keys were
verified parse-identical to the `.backups/…20260824-235306` copies (`yaml.safe_load` diff: only
the named keys gone, no key added, no surviving value changed). No `related:`/`see_also:` line
falls inside any removal range, and no file anywhere deep-links one of these keys — both checked
programmatically before deleting.

  | File | Block (pre-removal range) | What went | Repopulates under |
  |---|---|---|---|
  | `hardware/addon-hyperram-hyperflash.yaml` | `host_note` (26-30) | 5V-socket / ACC-HDR jumper guidance | «#307» |
  | `hardware/addon-serial-device.yaml` | `specifications` (41-59) | 3.3V, 3.2mm, 5mm, 9.5mm | «#307» |
  | `hardware/addon-serial-device.yaml` | `rev_b_5v_note` (60-65) | Rev-B 5V shunt note | «#307» |
  | `hardware/addon-serial-host.yaml` | `description` (16-23) | 500 mA load-switch limit | «#307» |
  | `hardware/addon-serial-host.yaml` | `specifications` (37-58) | 500mA/1A/~2mA + physical dims | «#307» |
  | `hardware/addon-serial-host.yaml` | `power_requirements` (59-71) | the same current budget again | «#307» |
  | `hardware/addon-serial-host.yaml` | `development_workflow` (102-110) | 5V-availability checklist | «#307» |
  | `hardware/addon-serial-host.yaml` | `limitations` (120-126) | 500mA per-port limit | «#307» |
  | `hardware/edge-standard-module.yaml` | `revision_history` (204-235) | VIN 5.5V→16V, 2A→3A, 2.5MHz→750kHz | «#307» |
  | `hardware/hub75_adapter.yaml` | `power_requirements` (127-139) | 35mA @ 35MHz + the four panel budgets | «#307» |
  | `language/spin2/methods/getct.yaml` | `description` (8-15) | "~21 seconds at 200MHz" wrap figure | «#299» |

**Sources to repopulate from:** the `#64006 Series` and `#64004-ES` product guides (already cited
in each file's own `documentation.primary`), the P2-EC Edge Module guide's revision table, the
HUB75 driver study, and — for `getct` — the Spin2 language reference. **`getct.yaml` is the one
outside `hardware/`**: it is «#299»'s, and its wrap figure is *derived* (2³² ÷ 200 MHz), so it
needs a source that states it or a rewrite that does not compute.

  **Three of the dispatched candidates were NOT violations** and were left alone — measured, not
  assumed: `architecture/smart_pin_patterns.yaml` `timing_patterns` and `language/pasm2/waitx.yaml`
  `examples` state **zero** quantities once code regions are stripped (their numbers are all
  inside example bodies), and `architecture/boot-rom/spi-flash-boot.yaml`
  `phase_2_post_load_state` is **correctly** silenced: its `cog_clock.source:` attributes the
  20-30 MHz figure to `architecture/clock_system.yaml`, which does carry it
  (`frequency: "20-30 MHz across process/voltage/temperature"`, line 35). So no `architecture/`
  block was in scope after all — the finding is 11, in two trees, not three.

  **REPOPULATION EXECUTED 2026-08-25 («#307» and «#299»).** All 48 + 11 blocks are dispositioned
  and disposed of: in `hardware/`, 34 returned cited and 24 are held in the ingestion tree
  (**F-353**, with the per-block table and the seven content-level holes in **F-354**); outside it,
  `language/spin2/methods/getct.yaml description` was «#299»'s and is recorded with F-347/F-352.
  Nothing on either record is still owed.

  Status: `PENDING-VALIDATION` — the detector repair, all 59 removals and the whole repopulation
  are applied and gate-verified; only the YAML release is owed. See **F-335**, which this repair
  exposed.

---

## `audit-yaml-claim-sourcing.py` does not know the `documentation: primary:` citation spelling, so a whole class of board file is mis-tiered into the advisory lane (2026-08-24, F-334 repair) — F-335

> 🔴 **(e) A DEFERRAL READS AS A CITATION — ADDED BY THE ARBITER 2026-08-25 (during «#298»), AND IT
> IS THE ONE THAT ACTUALLY HURT SOMEBODY.** `CITE_KEY_RE`/`INLINE_CITE_RE` match the bare word
> *datasheet* anywhere in a block. `language/pasm2/concepts/basic-io.yaml` and its Spin2 twin each
> carried:
>
> ```yaml
>   max_current_per_pin: "150mA"
>   max_current_total: "Check datasheet for package limits"
> ```
>
> The second line is a **deferral — an instruction to go look elsewhere** — and it scored the whole
> block as cited. So the block sailed through «#293» *and* «#294» while asserting
> **`max_current_per_pin: "150mA"` against the datasheet's stated `Max. allowable current per I/O
> pin ±30 mA`** (`sources/p2-datasheet/p2-datasheet-text.txt:2163`). **Five times the absolute
> maximum, in the exact number a reader uses to size an LED series resistor.** The same block
> shipped `VOL_max: "0.4V"` / `VOH_min: "2.4V"` — 5 V-TTL thresholds the P2 datasheet does not
> contain (its real figures are millivolt drops: Vol 15 mV sinking 1 mA, `:2172-2178`).
>
> **This is the third member of the same family**, after (F-334) a board revision `Rev B`/`Rev C`
> and a power `source:`. The pattern is now explicit and should drive the repair rather than three
> more one-off patches: **the citation side matches on the PRESENCE OF A TOKEN, never on whether
> the sentence actually attributes the block to a document.** *"Check datasheet for…"*, *"see the
> datasheet"*, *"per the manual"* are pointers away from the block; a citation points *at* a source
> for the claim being made. Fixing (a)-(e) individually will keep finding a sixth.
>
> Removed under «#298» (both copies, pure deletion) and filed as **F-348**. The correct facts
> already ship, cited, in `architecture/io_pin_timing.yaml absolute_maximum_ratings`.

> 🔴 **TWO FURTHER DEFECT CLASSES, ADDED BY THE ARBITER'S RE-RUN 2026-08-25. «#305» MUST DISPOSE OF
> ALL OF THEM BEFORE ARMING — THEY ARE NOT INDEPENDENT, AND ONE PAIR CANCELS.**
>
> **(c) An escaped single-line string hides example code from `strip_code_regions`.** The stripper
> recognises **block scalars** (`|`). `language/pasm2/waitx.yaml`'s `examples:` stores its PASM2 as a
> double-quoted single-line string with literal `\n` escapes, so the stripper never sees a code
> region and the gate reads **4 quantities** out of PASM2 *comments* — `' For 1kHz PWM at 200MHz
> clock:` and `' 100us @ 200MHz`. Those are chosen demo parameters, which the tool's own header says
> it exists to skip. Measured: 4 quantities raw, **4 surviving the strip** (compare
> `architecture/smart_pin_patterns.yaml timing_patterns`, where 1 raw → **0** stripped, correctly).
>
> **(d) A slug still passes as a citation, so (c) is currently masked.** `waitx.yaml examples` carries
> `source: hub75_driver` · `source: inline_pasm2_pattern` · `source: bit_bang_spi` ·
> `source: software_pwm` · `source: input_debounce` — **pattern-category tags, not documents**. These
> are the same shape as `source: motor_control`, which F-334's repair added as a control and rejects;
> the filename/slug accept-branch lets these through. So the block is not flagged.
>
> 🔴 **THE POINT IS NOT EITHER BUG — IT IS THAT THEY CANCEL.** A quantity-side false positive is
> being hidden by a citation-side false negative, and the block reads clean for two wrong reasons.
> Fix either one alone and the gate starts failing on a block that was never a real violation. That
> is why (a)-(d) must be dispositioned **together**, in the order this finding sets out, and why the
> current `PASS  no Tier 1 violations` — while true for the two paths F-334 repaired — is **not yet a
> safe thing to arm a release gate on.**
>
> **What IS settled and should not be re-litigated:** F-334's two repairs are proven. The arbiter ran
> the five false-negative cases against the pre-repair detector loaded side-by-side: all five scored
> *cited* before and *uncited* after, while three real citation forms — short form, an EF record, and
> one that itself carries `Rev C` — still score cited. 25 controls, 0 FAIL.

> **Origin.** Surfaced while repairing F-334. Removing the `Rev B` token from `INLINE_CITE_RE`
> dropped `addon-serial-host.yaml` and `addon-serial-device.yaml` out of "citing" entirely — and
> that is **wrong**, because both files cite perfectly well, three lines from the bottom. The
> detector simply does not recognise the spelling. Filed rather than fixed: the fix is measured
> below and it is **not safe to arm as-is**, for a reason that is itself a finding.

- **F-335 — the eval add-on board files cite as `documentation:` → `primary: "<doc>"`, a spelling
  no citation key in the tool matches, so files that DO know the citing convention are scored as
  wholly-uncited and their F-327-shaped blocks land in Tier 2 (advisory) instead of Tier 1
  (blocking).** — `RESOLVED` — `addon-serial-host.yaml:171-172` is the type case:

  ```yaml
  documentation:
    primary: "P2 Eval Add-on Boards (#64006 Series) v2.0"
  ```

  That is a citation by any reading, and it is the ONLY one in the file. `CITE_KEY_RE` knows
  `source`/`sources`/`reference`/`references`/`authority`/`derived_from`/`verified_against` and
  not `documentation`, so `file_cites` is false, so **the file's own other sections cannot act as
  the control** and Tier 1 — the tier the release gate «#305» will arm on — never applies to it.
  Until F-334 was repaired the effect was invisible: the `Rev B` token was propping these files
  up in Tier 1 by accident, for entirely the wrong reason.

  **Measured, whole-KB, 2026-08-24.** Adding `documentation` to the key vocabulary (value-tested
  exactly like the others) moves **Tier 1 from 4 to 34 and Tier 2 from 91 to 61** — thirty
  blocks across eight board files that have sat in the advisory lane throughout this sprint:
  `addon-av-breakout` (3), `addon-control-board` (6), `addon-digital-video-out` (4),
  `addon-led-matrix` (3), `addon-microsd` (1), `addon-mini-prototyping` (5), `addon-wx-adapter`
  (1), plus the two serial boards already purged under F-334.

  **Why it was NOT applied in the same pass, and this is the real content of the finding.**
  Reading those thirty blocks shows most of them are not claims at all — they are the **quantity**
  half over-firing, which is a different defect in the other half of the same tool:

  | Kind | Example | Why it is not a measurement |
  |---|---|---|
  | part number | `addon-control-board.yaml:2` `part_number: "64006A"` | `QTY_RE` reads `64006A` as **64006 amperes**. Same string flagged again in `aliases` and in `availability.part_lookup`. |
  | rail NAME | `supply_voltage: "3.3V from host"`, `label: "5V"`, `voltage: "3.3V (VIO)"` | `3.3V`/`5V` here name the rail, the way `GND` names a net. Present in nearly every board file. |
  | connector NAME | `addon-digital-video-out.yaml:83` `name: "5V (5V-arrow)"` | a silkscreen label. |

  Arming the key widening without repairing `QTY_RE` first would therefore force the deletion of
  a board's `part_number` and `aliases` blocks to reach zero — **content destruction to satisfy
  an instrument defect**, which is the exact inversion of what this sprint is for.

  **The scope this finding must own, because it is wider than it looks.** The rail-name over-fire
  is not confined to the thirty: it is also why three of F-334's eleven removals went
  (`addon-hyperram-hyperflash.host_note` on a "5V socket", `addon-serial-host.development_workflow`
  and `addon-serial-device.rev_b_5v_note`, all on rail names with no measurement in them), and it
  reaches back into the 48 (`addon-rtc.power_signals` was removed for
  `VIO3V3: "3.3V supply; powers the RTC…"`). Those removals were made **deliberately, for
  consistency** with the 48 already accepted — but they are the same shape, and the decision
  about rail names should be made **once, globally**, not differently at each task boundary.

  **What is owed, in this order.** (1) Decide the rail-name question: is `3.3V` naming a supply
  rail a claim that must be sourced, or is it structure like a pin number? Whichever way it goes,
  it applies to the 48, to F-334's eleven, and to the Tier 2 population alike. (2) Fix `QTY_RE`
  so a part number (`64006A`) is not a current — that one has no second side, it is simply wrong.
  (3) Only then add `documentation` to `CITE_KEY_RE`, with negative-control cases for the
  spelling, and re-run. **«#305» should not arm the release gate on Tier 1 until (3) lands** —
  not because the gate is wrong today, but because eight board files are currently exempt from it
  for a reason nobody chose.

  **RESOLVED 2026-08-25 by «#305», (a)–(e) together, in the order this finding set out.**

  1. **The rail-name question, decided: a voltage designator in a hardware file IS a claim.**
     It asserts a fact about a physical board — what is printed on it, what it connects to —
     and a reader wires hardware from it. The alternative disarms the gate on `vdd_max` /
     `VOH_min`, which is the exact F-348 shape that shipped a figure five times the
     datasheet's absolute maximum. It is also the reading already applied to the 48 and to
     F-334's eleven, so nothing already accepted has to be re-litigated. Recorded as two
     standing negative-control cases (`label: "5V"` and `vdd_max: "3.6V"` MUST STILL FIRE)
     so the decision cannot flip in silence.
  2. **(b) / F-351 — `QTY_RE` repaired.** A bare `A` preceded by four or more integer digits
     is a part number or a standard designator, not a current; `U+XXXX` is masked alongside
     `%binary` and `$hex`; the number accepts thousands separators. Measured: **9 blocks**
     that stated no quantity at all left the advisory lane (`addon-control-board` ×3,
     `hardware-compatibility-matrix` ×2, `p2-hardware-selection-guide` ×2,
     `p1_rom_font_character_set`, `obex/objects/4070`). F-351 listed ten; the tenth
     (`p2-hardware-feature-comparison` `selection_criteria`) had already been drained by an
     earlier task, so it was not in today's population.
  3. **(c) and (d) landed in the same edit, because they cancel.** (c): a code example stored
     as a **double-quoted scalar with literal `\n` escapes** was invisible to the region
     stripper, which now judges a quoted scalar by the same `CODE_MARKER_RE` test it applies
     to a `|` block — plus a guard requiring a real `\n` escape, without which the rule
     blanked `p2an003-dac-analog-signal-generation.yaml:118`, a `source_statement:` holding a
     quoted SENTENCE that opens with an apostrophe. Blanking prose is the "turn the gate off
     by stealth" failure, reproduced in the other value shape. (d): a lowercase snake_case
     slug is a pattern-category tag, not a document — vetoed by shape rather than by token.
  4. **(e) — a deferral is not a citation.** Vetoed as a PHRASE (`check|see|refer to|consult
     |look up|read|review` + a document noun) rather than anchored at the start of the value,
     because *"Sinks 150mA per pin; see the datasheet for package limits"* reads the same way
     and an anchor would miss it. A deferral that NAMES the document (`"See P2 Silicon Doc
     v35"`) is an attribution and still counts. Applied to the inline path per LINE, which is
     the half that actually fired.
  5. **(a) — `documentation` added to `CITE_KEY_RE` last, as this finding required.**

  ⚠️ **TWO CORRECTIONS TO THIS FINDING'S OWN TEXT, measured against the tree 2026-08-25.**
  - (d) attributes the leak to "the filename/slug accept-branch". It is not that: of the five
    slugs on `waitx.yaml`, **only `inline_pasm2_pattern` passed**, and it passed because the
    bare `pasm2` token in `CITE_VALUE_RE` matches INSIDE the identifier. The corpus carried
    exactly two such values (the other is `lock_validation` at `lockrel.yaml:70`, via
    `validat`). `hub75_driver`, `bit_bang_spi`, `software_pwm` and `input_debounce` never
    passed at all.
  - (c) states `waitx.yaml` reads "4 quantities raw, 4 surviving the strip". **That does not
    reproduce**: with the pre-repair detector loaded side by side, the file yields **0**
    quantities raw and 0 after the strip. The PASM2 comments carrying `1kHz` / `200MHz` /
    `100us` sit after `#pwm_loop` on the same physical line, and `strip_yaml_comment` reads
    that `#` as a YAML comment and drops the rest. So the block read clean for a THIRD wrong
    reason, not two. The underlying defect in (c) is real and is fixed; its stated symptom
    was masked by an unrelated accident.

  **Measured effect of (a)–(e) together, instrument only, against the committed tree:**
  Tier 1 **0 → 20**, Tier 2 **78 → 49**. The 29 that left Tier 2 are the 20 re-tiered by (a)
  plus the 9 artifacts removed by (b). The 20 were then drained source-first (see F-335's
  disposition in the sprint plan §10): 17 blocks gained a per-block `source:`, three unsourced
  inferences were removed. Final state: **0 Tier 1, 49 Tier 2**, and both gates armed.

  Status: `RESOLVED`

---

## The P2 Hardware Manual states a VCO range the datasheet and the Silicon Doc both contradict (2026-08-24, `p2-datasheet` re-ingestion) — F-330

> **Origin.** The `p2-datasheet` table recovery (plan §8) cross-checked every recovered table
> against the DOCX-derived `p2-hardware-manual` tables. Nine of ten comparisons agreed cell for
> cell. This is the one that did not. **Nothing is fixed in this filing** — the ingestion head
> produces source data; any YAML consequence belongs to the purge/repopulate tasks.

- **F-330 — Two Parallax documents of the SAME edition date (2022/11/01) give different
  recommended VCO ranges in the same `%MMMMMMMMMM` table note, and the P2 Hardware Manual is
  the outlier.** — `RESOLVED — relocated to the errata register as E-003; the guard this entry existed to be is now served there`

  > **RELOCATED + CLOSED 2026-08-25 («#302»), pointer left behind, never a silent move.**
  >
  > By the three-register test — *if Parallax fixed the Hardware Manual's Table 10 note tomorrow,
  > would this disappear?* — **yes**, so this is an **erratum**, not a KB correction. This entry
  > says so itself: *"Treat the Hardware Manual's Table 10 note as source errata."* It now lives at
  > **`engineering/ingestion/SOURCE-ERRATA.md` → `E-003` (`RESOLVED`)**, *"the VCO note contradicts
  > the manual's own PLL Example"*, which carries all six rows of evidence (including the decisive
  > self-contradiction at `:574` vs `:603`), the same 100–200 MHz verdict, the same 350 MHz =
  > VCO/1-overclock-ceiling disambiguation, and the Spin2 v51 solver bound as the third legitimate
  > context for the number. That register was created 2026-08-25, after this was filed.
  >
  > **The guard function is preserved, which is the only thing this entry was for.** It carried
  > **no owed KB work** — *"KB impact: NONE"*, `clock_system.yaml` already draws the line correctly
  > — and existed solely *"to prevent a future agent from 'fixing' that 200 to 350 on the Hardware
  > Manual's authority."* `E-003` performs exactly that guard, in the register an ingestion agent
  > actually consults before trusting a source.
  >
  > ⚠️ **THIS ENTRY'S OWN DESCRIPTION OF THE KB IS STALE, AND WAS CORRECTED ONLY BECAUSE THE FILE WAS
  > RE-READ.** It states the KB carries `vco_range: "99 MHz to 201 MHz"`, `max_overclock: "350 MHz"`
  > and `absolute_max: "350 MHz (may be unstable)"`. **None of those three keys exists on disk today**
  > — `clock_system.yaml` was rewritten during this sprint's uncited-block purge (F-347's removal
  > record lists `configuration_constants`, `pll_system`, `clock_specifications` and `anti_patterns`
  > among the blocks removed from this very file). Repeating the entry's own text as verification
  > would have published a false confirmation of a file nobody had opened.
  >
  > **What is actually there, measured 2026-08-25 — and it is STRONGER than what this entry
  > described:**
  > - `:104` `vco_range:` now quotes the source verbatim — *"The PLL's VCO is designed to run between
  >   100 MHz and 200 MHz and should be kept within that range."*
  > - `:129` `overclocking:` and `:270` `overclock_ceiling:` carry the 350 MHz VCO/1 figure **with its
  >   Silicon Doc locator**, kept separate from the recommendation.
  > - `:209` states the third context explicitly — *"350 MHz is the absolute VCO/1 overclock ceiling,
  >   NOT the XI-input limit."*
  > - `:130` `cross_source_conflict:` **names F-330 by ID inside the shipped YAML** and states the
  >   resolution. **The guard is now in the artifact itself**, which is a better place for it than any
  >   register — it reaches the agent at the moment of use.
  >
  > **Consequence for whoever maintains that file:** `:130` points at `F-330`. That pointer still
  > resolves — this entry stays in place — but the evidence now lives at `E-003`, so a future
  > citation refresh should carry the reader on to the errata register.

  **The identical sentence, two numbers:**

  | Source | Sentence, verbatim |
  |---|---|
  | **P2 Datasheet**, p.18 (`sources/p2-datasheet/p2-datasheet-text.txt:793`) | "The VCO frequency should be kept within 100 MHz to **200 MHz**." |
  | **P2 Datasheet**, p.19 PLL Example (`:850`) | "The PLL's VCO is designed to run between 100 MHz and **200 MHz** and should be kept within that range." |
  | **Propeller 2 Documentation v35 Rev B/C** (`sources/silicon-doc/part3-interrupts.txt:545` area) | "The VCO frequency should be kept within 100 MHz to **200 MHz**." |
  | **Propeller 2 Documentation v35 Rev B/C** (`sources/silicon-doc/p2-documentation.txt:6233`) | "The PLL's VCO is designed to run between 100 MHz and **200 MHz** and should be kept within that range." |
  | **P2 Hardware Manual**, Table 10 (`sources/p2-hardware-manual/complete-tables-reference.md:107`) | "The VCO frequency should be kept within 100 MHz to **350 MHz**." |

  **Verified at the source, not only in the extract.** The manual's `350` was read directly out
  of `word/document.xml` of
  `sources/p2-hardware-manual/Propeller 2 Hardware Manual - 20221101.docx`, so it is the
  document's own text and not a DOCX-walk artifact.

  🔴 **DECISIVE, AND ADDED BY THE ARBITER'S RE-RUN: THE HARDWARE MANUAL CONTRADICTS ITSELF.**
  The filing above frames this as three documents against one, which would leave it a question
  of relative document authority. It is not — the manual states **both** numbers, twelve
  paragraphs apart, in the same voice:

  | Same document, two numbers | Sentence, verbatim |
  |---|---|
  | **Table 10 note** (`sources/p2-hardware-manual/p2-hardware-manual-text.txt:574`) | "The VCO frequency should be kept within 100 MHz to **350 MHz**." |
  | **Its own PLL prose** (`sources/p2-hardware-manual/p2-hardware-manual-text.txt:603`) | "The PLL's VCO is designed to run between 100 MHz and **200 MHz** and should be kept within that range." |

  Line 603 is verbatim identical to the datasheet's `:850` and the Silicon Doc's `:6233`. So the
  manual's own body text agrees with the other two sources and disagrees with its own table note.
  That settles it without weighing authority at all: **the Table 10 note is a localized
  substitution error inside an otherwise-correct document**, which is exactly what "source
  errata" means and is why G-016/G-017-class upstream reporting is the right disposition rather
  than any re-ranking of the manual as a source.

  **Where 350 legitimately belongs — the vocabulary key.** 350 MHz is a real P2 number, but it
  is the **overclock ceiling**, not the recommended range. The Silicon Doc says so in the very
  next row of the very same table, against `%PPPP`: *"For fastest overclocking, the PLL can be
  pushed to 350 MHz using the 'VCO / 1' mode (%PPPP = 15)."* Spin2 v51's clock-setup symbols
  carry the same bound as a compiler constraint
  (`sources/spin2-v51/complete-clock-setup-symbols.md:276`, "MUST be between 100 MHz and
  350 MHz"). The Hardware Manual appears to have substituted the overclock ceiling into the
  *recommendation* sentence, which is why this is a defect rather than two documents describing
  two different things: both sentences make the same claim ("should be kept within") with
  different numbers, and they cannot both be the recommended range.

  **Resolution for downstream use.** Recommended/design VCO range = **100–200 MHz** (datasheet
  and Silicon Doc, two independent sources, each stating it twice). **350 MHz** = the VCO/1
  overclock ceiling and the Spin2 solver's upper bound. Treat the Hardware Manual's Table 10
  note as **source errata**; do not cite it to raise a recommended-range figure.

  **KB impact: NONE — recorded so it is not "corrected" later.**
  `deliverables/ai/P2/architecture/clock_system.yaml` already draws the line correctly
  (`vco_range: "99 MHz to 201 MHz"`, `max_overclock: "350 MHz"`,
  `absolute_max: "350 MHz (may be unstable)"`, and an explicit note distinguishing the two).
  **This finding exists to prevent a future agent from "fixing" that 200 to 350 on the Hardware
  Manual's authority.** No YAML edit is owed.

---


## WRPIN D-operand field map: three field descriptions wrong in the YAML, ten mode numbers footnote-fused in an ingestion artifact (2026-08-24, `KNOWLEDGE-GAPS` pass-6 catch-up) — F-331, F-332

> **Origin.** The pass-6 gap-ledger catch-up read the WRPIN bit-field map in both 2026-08-24
> repaired captures (P2 Datasheet pp.23-25, P2 Hardware Manual Tables 16-25) to close
> `KNOWLEDGE-GAPS.md` **G-001** and **G-008**. Both defects below were found while doing that
> reading. **Nothing is fixed in this filing.**

### F-331 — `pasm2/wrpin.yaml` mislabels three of the six WRPIN D-operand fields; two agreeing Parallax sources and the YAML's own sibling file all say otherwise — `PENDING-VALIDATION`

> **APPLIED 2026-08-25 by «#295» phase 2 — REPOINTED, not re-worded.** The `d_operand_format.fields:`
> map no longer restates the six fields at all. It now carries three pointers:
> `reference:` → `architecture/smart_pins.yaml (configuration_format.fields)`, which already has all
> six right; `m_sub_fields:` → the new `architecture/pin-drive-configuration.yaml`; and
> `input_selectors:` → the block below it, which was correct and is untouched.
>
> **Why repoint rather than re-word.** The three sources word `M` two ways ("pin mode" /
> "low-level pin control"), so re-wording means picking one; pointing at the single home means
> picking none, and it removes the third copy that made the drift possible. Deletion is the
> correction.
>
> **Evidence is triple-sourced, one better than this finding records** — the Silicon Doc agrees
> with the datasheet and the Hardware Manual: `part4-smart-pins.txt:55` reads *"%M..M: low-level pin
> control"* and `:63` reads *"%TT: pin DIR/OUT control (default = %00)"*, with `%SSSSS` at `:107`.
> None of the three says "DAC/output mode", "DAC/output value", or "+ smart-pin mode".
> (This finding's own body cites `:59` for the `%TT` line; measured, it is `:63`.)
>
> **Owed:** index regeneration + `validate-crossref-keys.py` after the boundary commit.

**Location:** `deliverables/ai/P2/language/pasm2/wrpin.yaml:34-36` (the `d_operand_format.fields:` map).

**What the two sources say, verbatim and identically** — P2 Datasheet @ 2022/11/01 p.23
(`engineering/ingestion/sources/p2-datasheet/p2-datasheet-text.txt:1054-1059`) and P2 Hardware
Manual @ 2022/11/01 (`engineering/ingestion/sources/p2-hardware-manual/p2-hardware-manual-text.txt:786-791`):
`A` = PIN input selector · `B` = ADJ input selector · `F` = PIN and ADJ input logic/filtering ·
**`M` = pin mode** · **`T` = pin DIR/OUT control (default = %00)** · **`S` = smart mode**.

| Field | YAML says | Both sources say |
|---|---|---|
| `M` | "13-bit low-level pin control **+ smart-pin mode**" | **pin mode** — the smart mode is `S`, a different field |
| `TT` | "**DAC/output mode**" | **pin DIR/OUT control** (default `%00`) |
| `SSSSS` | "**DAC/output value or pin-output bit selection**" | **smart mode** (the 32 `%SSSSS` modes) |

**The file's own sibling already has all six right** —
`deliverables/ai/P2/language/spin2/methods/wrpin.yaml:28-35` reads "Bits 20:8 (M): Low-level pin
control", "Bits 7:6 (TT): Pin DIR/OUT control", "Bits 5:1 (SSSSS): Smart pin mode selector
(5 bits, 32 modes)". So the two WRPIN entries in the shipped KB describe the same 32-bit word
differently, and an agent that reads the PASM2 one is told `SSSSS` selects a DAC value.

**Not the whole file** — the same file's `input_selectors:` block (`:37-56`) is **correct** and
matches both sources including the two rows Titus rev5 had swapped (`x101` = relative −3,
`x111` = relative −1). Only the three `fields:` descriptions are wrong; do not purge the block.

**Proposed correction:** replace the three descriptions with the sources' own words (`M` = pin
mode; `TT` = pin DIR/OUT control, default `%00`; `SSSSS` = smart mode), keeping the existing
bit-range annotations from the Spin2 sibling. **Closes the last open half of `KNOWLEDGE-GAPS`
G-008.**

### F-332 — the P2 Hardware Manual's table artifact carries ten six-digit `%SSSSS` values for a five-bit field, with no reconciliation note — `CONFIRMED`

**Location:** `engineering/ingestion/sources/p2-hardware-manual/complete-tables-reference.md:287-314`
(Table 25) and the same table in
`engineering/ingestion/sources/p2-hardware-manual/p2-hardware-manual-text.txt:1030-1036, 1053, 1054, 1056`.

**Ten values, each a 5-bit mode with its superscript footnote `¹` fused on:** `001001` `001011`
`001101` `001111` `010001` `010011` `010101` `110111` `111001` `111101` — correctly
`%00100¹` `%00101¹` `%00110¹` `%00111¹` `%01000¹` `%01001¹` `%01010¹` `%11011¹` `%11100¹`
`%11110¹`, footnote 1 being *"OUT signal overridden"* (the artifact carries that footnote
immediately below the table).

**This is a known, already-adjudicated class — and the adjudication is in the wrong file.** The
`p2-datasheet` artifact names the identical defect as reconciliations **R1** and **R2**
(`sources/p2-datasheet/complete-tables-reference.md:49-50`), decided by three of four extraction
paths plus a visual read of the rendered pp.34-35, and its **R8** even records that "The Hardware
Manual's DOCX (Table 9) carries the identical fusion, so this reconciliation applies to both
sources" — for Table 9's `INA`/`INB` only. **No such note exists anywhere in the Hardware
Manual's own artifact** (a case-insensitive search of that file for *footnote*, *superscript*,
*reconcil*, and *OUT signal overridden* returns nothing).

**KB impact: NONE today — recorded so it stays that way.** No fused value reached
`deliverables/ai/P2/` (grepped for all ten; the only near-hits are COGINIT mode bits in
`spin2/patterns/implementation/spin2_cog_management.yaml`, unrelated). The exposure is forward:
an agent deriving smart-pin YAML from the Hardware Manual artifact alone gets `%001001` for
pulse/cycle output.

**Proposed correction (ingestion head, not a YAML edit):** add the R1/R2 reconciliation note to
`sources/p2-hardware-manual/complete-tables-reference.md` beside Table 25, in the form the
datasheet artifact already uses. **Wider question worth one pass:** the DOCX walk drops
superscript markers into the adjacent numeral generally — Table 9's `INA1`/`INB2` is the same
mechanism, so Table 25 is unlikely to be the only other instance.

---


## Six defects surfaced while building the single constant-definition home (2026-08-25, «#295» phase 2) — F-336…F-341

> **Origin.** All six were found while implementing «#295» — promoting the drive ladder into the
> KB and collapsing two `P_*` definition homes into one. Two are fixed in that same pass and are
> marked so; four are not this task's repair and are filed for the task that owns them. Every
> number below was measured against disk on 2026-08-25, not carried from the design.

### F-336 — the weak-drive idiom set is one composition wide: `P_HIGH_15K | P_LOW_FLOAT` has neither a Parallax statement nor a bench result, and the ladder has never been swept against a load — `CONFIRMED`

> **This is a GAP, filed instead of content.** Read the arbiter's F-322 attribution correction in
> the section below first — it settles where the `P_HIGH_15K | P_LOW_FLOAT` string comes from
> (`smart-pins-catalog/ingestionSources/basic-io/spin2-v51-extract.md:284-287`, our own derived
> catalog extract) and it is not re-filed here.
>
> **What is missing, stated positively.** Spin2 v55 — the current edition — defines both constants
> individually (`spin2-v55-text.txt:1504` `P_HIGH_15K | Drive high 15kΩ`; `:1519` `P_LOW_FLOAT |
> Float low`) and composes them into **no idiom at all**. The empirical ledger carries the
> *other* composition: EF-063 and EF-064 both use `P_HIGH_15K` / `P_LOW_15K` with **DIR high** and
> **never** `P_LOW_FLOAT` (`P2-EMPIRICAL-FINDINGS.md:827,840`). So the one-sided variant — weak on
> one side, floating on the other, which is what an open-drain-style idiom actually needs — is
> asserted by nothing.
>
> **What is owed, and it is a bench item.** Extend the EF-063/EF-064 rig
> (`campaigns/2026-08-manual-corrections/tests/test-f272-streamer-dac-tt.spin2:212-220` is the
> routine) to (a) run `P_HIGH_15K | P_LOW_FLOAT` with DIR high against a known load and record
> whether it behaves as a one-sided weak drive, and (b) sweep all eight ladder rungs on both sides
> against the same load, so the KB can say what each rung does rather than only what the legend
> calls it. Until then `architecture/pin-drive-configuration.yaml` ships the two verified idioms
> and names this omission in its own `idioms.not_documented_here:` block.
>
> **«#296» must not ship the `P_HIGH_15K | P_LOW_FLOAT` string as sourced.**

### F-337 — the P2 Datasheet and the P2 Hardware Manual agree with each other and contradict the Silicon Doc on `%TT` in DAC_MODE, and the shipped YAML follows the minority source — `CONFIRMED`

> **Two disagreements, both in the `(T) Pin DIR/OUT Control` table, both about whether it is the
> DAC or the ADC that gets enabled.**
>
> | Context | Datasheet 2022/11/01 + Hardware Manual 2022/11/01 | Silicon Doc v35 |
> |---|---|---|
> | smart pin off, DAC_MODE, `%TT = 00` | **`DIR enables DAC`**, M[7:0] sets DAC level | **`OUT enables ADC`**, M[7:0] sets DAC level |
> | DAC smart-pin modes (`%SSSSS = %00001..%00011`), `0x` | `OUT enables **DAC** in DAC_MODE`, M[7:0] overridden | `OUT enables **ADC** in DAC_MODE`, M[7:0] overridden |
>
> **Verbatim locations, all four read this session:**
> `engineering/ingestion/sources/p2-datasheet/p2-datasheet-text.txt:1175` and `:1183` ·
> `engineering/ingestion/sources/p2-hardware-manual/p2-hardware-manual-text.txt:897` and `:905` ·
> `engineering/ingestion/sources/silicon-doc/part4-smart-pins.txt:83` and `:98`.
>
> **Where the KB stands.** `deliverables/ai/P2/architecture/smart_pins.yaml`
> `configuration_format.fields.tt.behavior_by_context` carries the **Silicon Doc** wording in both
> places (`dac_mode."%00": "OUT enables ADC, M[7:0] sets DAC level"` and
> `dac_smart_pin_modes.adc_control: "0x=OUT enables ADC..."`). Two agreeing 2022/11/01 sources say
> otherwise, and this is the field an agent reads to work out why a DAC will not drive.
>
> **Not resolved here, and not guessable.** EF-054/EF-055 already probed this bit family
> empirically (they established that `%01` switches the DAC's *source*), so the ledger may already
> settle it or be one short rig away from settling it. Empirical outranks both documentary
> sources; that is the route, not picking the majority.

### F-338 — `P_LEVEL_B` and `P_SCHMITT_B` do not exist: two fabricated constant names stood in four `related_symbols:` lists, and nothing in the toolchain could see them — `PARTIAL`

> **Evidence, three ways.** Neither name is in the Spin2 v55 symbol table (114 rows, 116 distinct
> names, `spin2-v55-text.txt:1419-1562`). Neither is on `audit-constant-fidelity.py`'s 120-name
> truth side. `pnut-ts` v1.55.3 **rejects both** as `PUB main()` / `wrpin(0, NAME)`, while
> accepting all seven of the legal siblings they are near-misses on — `P_LEVEL_A`,
> `P_LEVEL_A_FBN`, `P_LEVEL_B_FBP`, `P_LEVEL_B_FBN`, `P_SCHMITT_A`, `P_SCHMITT_A_FB`,
> `P_SCHMITT_B_FB`. That seven-accept control is what proves the harness discriminates rather than
> rejecting everything.
>
> ⚠️ **A naive grep says both names EXIST.** They are substrings of the `_FB` / `_FBP` / `_FBN`
> forms, so `grep P_LEVEL_B` returns hits for `P_LEVEL_B_FBP` and `P_LEVEL_B_FBN`. Match on word
> boundaries — `grep -P '\bP_LEVEL_B\b(?!_)'` — or this reads as a false clear.
>
> **APPLIED 2026-08-25:** all four entries deleted from
> `language/spin2/symbols/spin2-builtin-symbols-complete.yaml`, **substituting nothing** (a
> substitution would be an inference about what the author meant). Whole-tree re-grep with word
> boundaries: **0 hits**.
>
> **Why this is `PARTIAL` and not closed: the class is still undetectable.** Nothing found these
> for years, and nothing would find the next one — see **F-340**. This entry stays open until that

> 🔴 **MEASURED BY THE ARBITER 2026-08-25 (during «#304») — THE EXPOSURE IS 24% OF ALL REFERENCE
> SITES, AND THE GATE'S GREEN IS NOT A STATEMENT ABOUT THEM.**
>
> `validate-crossref-keys.py` iterates a **fixed 15-name `CROSS_REF_FIELDS` dict** and tests
> `if field_name not in content` — `content` being the **top level** of each document (`:447-492`).
> So a reference field is checked only when it is a top-level key, and any reference nested below
> that is invisible. Counted across `deliverables/ai/P2/`:
>
> | | sites |
> |---|---|
> | reference-field occurrences the validator **sees** (top level) | **742** |
> | occurrences it **structurally cannot see** (nested) | **230** |
> | **coverage** | **76%** |
>
> Nested, by field: `related_symbols` **136** · `related` 57 · `see_also` 25 ·
> `related_instructions` 6 · `cross_references` 3 · `related_pasm` 2 · `combines_with` 1.
>
> **`related_symbols` alone is 136 unchecked sites, and that is exactly where the two fabricated
> names (`P_LEVEL_B`, `P_SCHMITT_B`) lived undetected.** They were not missed by bad luck; they
> were in a field the instrument does not read.
>
> ⚠️ **AND «#304» FOUND THE SECOND HALF OF THE SAME HOLE:** a field that is not in the dict at all
> is invisible even at top level. `knowledge_progression:` and `next_steps:` in
> `guides/*-getting-started.yaml` carried the citations that route every new agent into
> `concepts/basic-io.yaml` — **the validator could not have reported them wherever they pointed.**
> Its exit 0 was silence, not a verdict.
>
> **For «#305»: `3161 refs, 0 unresolved` must not be read, or reported at release, as
> "cross-references are clean."** It means *the 76% the instrument looks at resolve.* Either widen
> the traversal to nested occurrences and unknown reference-shaped fields, or state the scope
> wherever the number is quoted. **A gate whose green is narrower than its name is the defect this
> sprint exists to repair, one level up.**
> detection gap is dispositioned.

### F-339 — `audit-constant-fidelity.py`'s own docstring misstates the size and the shape of the blind spot it declares — `RESOLVED`

> **RESOLVED 2026-08-25 by «#305».** Both numbers re-measured against disk before the
> docstring was rewritten: the v55 table carries **116** distinct `P_` constants over **114**
> rows (two rows name a constant *and* its brevity alias), **ADDED = 0**, **RE-DESCRIBED =
> 20**. This finding's figures are confirmed exactly; the task body dispatched with «#305»
> repeated the wrong 100 and was corrected. 19 of the 20 move visibly once v55 is on the truth
> side; `P_OR_AB` is the twentieth and moves invisibly for the self-cancelling `strip_desc`
> reason this finding already documents — left alone, as instructed. `KNOWN LIMITATIONS`
> item 4 now records the closure and the measured cost instead of the estimate.

> **Location:** `engineering/tools/validation/audit-constant-fidelity.py`, `KNOWN LIMITATIONS`
> item 4 (around `:114`). For **«#305»**, which arms this gate; **do not fix it inside a task that
> is being measured by it.**
>
> | The docstring says | Measured 2026-08-25 |
> |---|---|
> | the v55 table "carries 100 distinct `P_` constants" | **116** (114 table rows; two rows carry a name *and* a brevity alias — `P_TRUE_OUTPUT`/`P_TRUE_OUT`, `P_INVERT_OUTPUT`/`P_INVERT_OUT`) |
> | the blind spot is "wherever v55 ADDED or RE-DESCRIBED a constant" | **ADDED is 0** — every one of the 116 is already on the truth side. **RE-DESCRIBED is 20**, and that is the entire exposure |
>
> **So the gap is not missing names, it is 20 superseded descriptions**, and framing it as
> add-or-redescribe hides which half matters. The 20, measured by loading the tool's own
> `harvest_source()` and diffing it against a hand parse of `spin2-v55-text.txt:1419-1562`:
> `P_ADC`, `P_ADC_EXT`, `P_ASYNC_RX`, `P_ASYNC_TX`, `P_COUNT_HIGHS`, `P_COUNT_RISES`,
> `P_INVERT_OUT`, `P_NCO_DUTY`, `P_NCO_FREQ`, `P_OR_AB`, `P_PULSE`, `P_PWM_SAWTOOTH`,
> `P_PWM_SMPS`, `P_PWM_TRIANGLE`, `P_QUADRATURE`, `P_REG_UP`, `P_REG_UP_DOWN`, `P_SYNC_RX`,
> `P_SYNC_TX`, `P_TRUE_OUT`. Four v51-only names are absent from v55 — `P_COMPARATOR`,
> `P_COMPARATOR_FB`, `P_FLOAT`, `P_PASS` — and the KB references and defines none of them.
>
> **The KB side is already at v55**, as of «#295» phase 2: all 116 records carry the v55 wording.
> Verified before adopting it that this moves nothing — 0 `QUANTITY` clashes and 0 `CONTRADICT`
> clashes across all 116 when the v55 text is compared against the v51 truth side. So closing this
> is a docstring-and-harvest repair, not a content change.
>
> **One artifact that is NOT a defect and must not be "fixed".** `strip_desc()` keeps the *last*
> pipe-delimited cell, so a description containing a `|` is truncated. Only `P_OR_AB`
> ("Select A | B, B") does, the tool truncates both sides identically, and it self-cancels. The
> shipped record is correct as written; do not align it to the tool's displayed `"B, B"`.

### F-340 — `validate-crossref-keys.py` validates TOP-LEVEL keys only, so 67 nested `related_symbols:` lists in one file are never checked at all — `PARTIAL`

> **Location:** `engineering/tools/validate-crossref-keys.py:491-492` —
> `if field_name not in content or not content[field_name]: continue`, where `content` is the
> parsed file's **top-level** mapping. Every `CROSS_REF_FIELDS` entry is looked up there and
> nowhere else. For **«#305»**.
>
> **Measured consequence.** `language/spin2/symbols/spin2-builtin-symbols-complete.yaml` carries
> **135 `related_symbols:` lists**, every one nested inside a record, and the validator reports
> `related_symbols: 7 resolved` for the whole KB. Those 7 are the seven entries of the **one**
> top-level `related_symbols:` in the entire corpus — `language/pasm2/asmclk.yaml:76-83` — and this
> file contributes **zero** references to the count. **This is exactly how F-338
> survived**: two names that do not exist, sitting in a field the validator names in its own
> vocabulary, in the file that holds 99% of that field's instances.
>
> **What is owed.** Walk nested structures for the cross-reference fields, not just the top-level
> mapping — and add a negative control that plants a known-bad name in a nested list and proves
> the walk fails on it. A field that reports "resolved" while reading none of the corpus is worse
> than no check: it reads as coverage.
>
> **«#305» DISPOSITION, 2026-08-25 — the SCOPE half is done; the TRAVERSAL half is still owed.**
>
> This finding was assigned to «#305» because that task arms two release gates and must not
> arm anything on a number that reads wider than it is. What «#305» did:
>
> - **The blind spot is now MEASURED AND PRINTED on every run.** The validator counts the
>   reference sites its traversal cannot reach and reports them beside the rate:
>   *"⚠️ SCOPE: this traversal reads TOP-LEVEL fields only. 688 nested reference site(s) were
>   NOT checked (82% of 3849 coverage)."* A gate must read the artifact; a blind spot that is
>   counted is no longer silent.
> - **The inflated banner is gone.** `✅ ALL CROSS-REFERENCES VALIDATED SUCCESSFULLY` now reads
>   `✅ ALL TOP-LEVEL CROSS-REFERENCES RESOLVE — 688 nested site(s) NOT checked (F-340)`, and
>   `validate-dod-release.py` reports *"All TOP-LEVEL cross-references resolve"* rather than
>   *"All cross-references resolve"*. The same wording is carried into `release-yamls` Step 1
>   and into the sprint plan's *what a green exit does not certify* section.
> - **A missing measurement now FAILS the release.** The DoD check previously passed silently
>   when the validator printed no resolution rate at all; a validator that printed no
>   measurement audited nothing, and that now fails.
>
> **Why the traversal itself was NOT landed here, measured rather than assumed.** With the
> nested walk enabled, **54 references do not resolve** — 26 `related_symbols` (including four
> JSON-Schema keywords, `type`/`items`/`description`/`required`, which the walk reaches inside
> `spin2-language-schema.yaml` and which are not references at all), 15 `related_documentation`
> (descriptive text such as *"P2 Silicon Documentation"*, *"Pin mapping references"*), 2
> `related_pasm`, and the rest spread thin. Roughly half are content triage and half are a
> field-typing question (should `related_documentation` be `'text'` like `see_also`?). That is
> a task, not a side effect of arming a different gate, and landing it inside «#305» would have
> turned a green release path red on 54 items with no owner.
>
> ⚠️ **Counting units differ between this entry and «#305»'s measurement, and both are right.**
> This finding counts **sites** (742 seen / 230 unseen, 76%). «#305» counts **individual
> references** (3161 seen / 688 unseen, 82%). Same defect, same dominant field
> (`related_symbols`), different denominators — do not treat one as correcting the other.
>
> Status: `PARTIAL` — scope stated, measured and printed; the nested traversal + its negative
> control remain owed, with the 54 unresolved references above as the known entry cost.

### F-341 — six of our own derived analysis documents sit at the root of `engineering/ingestion/sources/`, repeat the pull-up mislabel F-321 exists to kill, and are inside the fidelity gate's declared *Parallax documentary* truth root — `PARTIAL`

> 🔴 **THE LATENT DISARM WENT ACTIVE, EXACTLY AS THIS FINDING PREDICTED — and is now closed
> at the instrument (2026-08-25, «#305»).** This entry says the disarm is "a shape away, not a
> policy away". «#305» changed the shape (the harvest had to read the current-edition v55
> table, whose rows put the name in column 2), and with the repaired parser and no guard,
> `p2-complete-signal-flow-matrix.md:100` — a **signal-flow** table whose last cell happens to
> hold a constant name — defined `P_PWM_SAWTOOTH` as **"P38"**, the pin number in the
> neighbouring cell. One of our own derived documents teaching the instrument our own
> inference, in the first run after the shape changed.
>
> **Closed structurally, not by a list of six names.** An ingested source **is a directory**:
> every real source under `sources/` lives in its own folder because that is what the ingestion
> process creates, so a loose file at the root of a truth root was put there by something else
> and is not an ingested source document (`MIN_DEPTH_BELOW_ROOT`). That rule excludes all
> **twelve** loose files at `sources/` top level, not just these six, and it catches the next
> stray file without an edit. A second, independent guard bounds the name cell to the first two
> columns — a constant in the last column is a *use*, not a definition. Both carry negative
> controls, including the exact `P_PWM_SAWTOOTH | P38` row.
>
> **`TRUTH_ROOTS` was NOT widened or narrowed** — the roots are unchanged; only what counts as
> a file inside them is now defined.
>
> **Still open, and it is the half this finding actually asked for:** the six documents remain
> at `sources/` top level, still asserting a 15 kΩ internal pull-up the P2 does not have. The
> instrument can no longer be misled by them; a reader still can. Relocating them to a derived/
> analysis area, or repairing them against the Datasheet legend, is unchanged and unowned.
>
> Status: `PARTIAL` — instrument disarm closed and controlled; the invented-part-number half
> is closed at every site in the repository (2026-08-26, «#323» — see the boxed note under
> F-356); the content relocation, and the four further unverified part numbers those files
> carry (#64028, #64029-as-combo, #40003, #40007), are owed.

> **The six**, all at `engineering/ingestion/sources/` top level, all self-describing as
> generated cross-references rather than Parallax publications:
> `p2-board-addon-compatibility-matrix.md` · `p2-complete-signal-flow-matrix.md` ·
> `p2-hardware-validation-checklist.md` · `p2-board-power-analysis-matrix.md` ·
> `p2-board-pin-mapping-knowledge.md` · `p2-addon-board-circuit-knowledge.md`.
> Their own subtitles give them away — *"Complete cross-reference for automatic code generation"*,
> *"Comprehensive testing procedures"*, *"Knowledge Base"*. No Parallax document is named on any
> of them.
>
> **What they assert.** The F-321 mislabel, verbatim and repeatedly:
> `p2-complete-signal-flow-matrix.md:127` *"WRPIN(pin, P_HIGH_15K) ' 15kΩ pull-up"*, `:62`
> *"Input Type: Digital with internal pull-up"*, `:65` *"220µA through pull-up when pressed"*;
> `p2-board-power-analysis-matrix.md:79` *"Internal pull-up: 15kΩ to 3.3V"*;
> `p2-board-addon-compatibility-matrix.md:84` *"8 × 220µA pull-up current = 1.76mA"*;
> `p2-hardware-validation-checklist.md:198` *"Enable internal pull-ups"*. The P2 has no such
> component — `P_HIGH_15K` selects **drive strength**, per the Datasheet p.24 Pin Mode Legend
> (`p2-datasheet-text.txt:1139-1147`). The 220 µA and 1.76 mA figures are stated by no Parallax
> source.
>
> **Why it is more than stale prose.** `audit-constant-fidelity.py` scopes its truth side to
> `TRUTH_ROOTS = [ingestion/sources, ingestion/smart-pins-catalog]` with a comment explaining that
> an unauthoritative source does not add a wrong answer, it **DISARMS the check** — that is why
> `external-inputs/` was excluded. These six are unauthoritative and are *inside* the root.
> **Measured today: they contribute 0 entries to the truth table**, because their pull-up lines do
> not happen to match `ROW_RE` or `BULLET_RE`. The disarm is latent, not active — a shape away, not
> a policy away.
>
> **What is owed.** Decide what these files are and put them where that is true: relocate to a
> derived/analysis area outside `sources/`, or repair them against the Datasheet legend and label
> their provenance. Either way they must stop reading as Parallax documentary sources.
> **Same class as the arbiter's F-322 correction** — a derived extract inside the ingestion tree
> mistaken for the source it was derived from. Two instances in two days makes it a class, not an
> accident: an audit of what actually lives under `ingestion/sources/` is owed.

---

## Pin drive-strength documented as bias resistors, and one block fabricated outright (2026-08-24, agent-report sweep) — F-321…F-327, F-329, F-333

> 🔴 **F-322's SOURCE ATTRIBUTION IS WRONG — CORRECTED BY THE ARBITER 2026-08-25 (during «#295»
> phase 1). The finding's VERDICT stands; its cited evidence does not, and «#296» must not inherit
> the string.**
>
> F-322 reads: *"What the source actually prescribes — same file, §'Weak Pull-Up':
> `WRPIN(pin, P_HIGH_15K | P_LOW_FLOAT)`"*, citing `sources/silicon-doc/part4-smart-pins.txt`.
> **There is no such section in that file.** Case-insensitive search for *pull-up* / *pull up* /
> *pullup* / *pull-down* across `part4-smart-pins.txt` returns **zero hits**.
>
> **Where the string actually comes from, measured:** `engineering/ingestion/smart-pins-catalog/
> ingestionSources/basic-io/spin2-v51-extract.md:284-287` — a **derived catalog extract**, not a
> Parallax document, carrying a `### Weak Pull-Up` heading over
> `WRPIN(pin, P_HIGH_15K | P_LOW_FLOAT)` with the hand-written comment *"15kΩ pull-up, float when
> driving low"*. Its neighbours (*"Hysteresis for noisy signals"*, *"Maximum drive strength
> (default)"*) are the same authored-commentary shape. **This is our own writing, not the source's.**
>
> ⚠️ **AND THE OPPOSITE OVERSTATEMENT IS ALSO WRONG.** «#295»'s design concluded *"no Parallax
> documentary source states a `P_HIGH_15K | P_LOW_FLOAT` idiom."* Too strong as worded — the string
> does exist in the ingestion tree, at the line above. The accurate statement is narrower and is
> what phase 2 must carry: **Spin2 v55 — the current edition, which supersedes v51 — defines both
> constants individually and composes them into no idiom at all.** `spin2-v55-text.txt:1504`
> = *"P_HIGH_15K | Drive high 15kΩ"*; `:1519` = *"P_LOW_FLOAT | Float low"*. The composition, and
> the word "pull-up" attached to it, are ours.
>
> **Disposition, unchanged in outcome:** under D4 the idiom does not ship as documentary. What ships
> instead is stronger — **EF-063/EF-064**, hardware-verified on real silicon
> (`external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md:827,840`), which state
> `P_HIGH_15K` with **DIR high** and do **not** use `P_LOW_FLOAT`. Empirical outranks documentary
> here, so the substitution is an upgrade rather than a workaround.
>
> 🔴 **THIS IS THE SECOND CONFIRMED FINDING TODAY WHOSE EVIDENCE CITATION WAS WRONG** — F-327's
> `:296` attribution was the first, corrected in this same section. Both were caught by
> re-verification during execution, not by review at filing time. A finding's VERDICT and its
> CITED EVIDENCE are separately fallible, and this register's own citations need the same
> hand-verification we apply to the KB's. Route to «#300»/«#302» as a register-wide evidence audit.

> 🔴 **SCOPE OF F-321/F-323 CHANGED BY «#293» — MEASURED BY THE ARBITER 2026-08-24, READ THIS
> BEFORE WORKING «#296».** «#293» removed the uncited `pull_up_modes:` / `pull_down_modes:` blocks
> from `language/spin2/concepts/basic-io.yaml` and `language/pasm2/concepts/basic-io.yaml` as part
> of the §4 purge. Those blocks were carrying most of the mislabel, so the deletion resolved much
> of F-321/F-323 as a side effect:
>
> | `audit-constant-fidelity.py` | at «#293» entry | after «#293» |
> |---|---|---|
> | `[CONTRADICT]` (Tier 2) | **23** | **5** |
> | `[UNDEFINED]` (Tier 1) | **50** | **55** |
>
> **«#296»'s verify criterion is therefore `5 → 0`, not `23 → 0`.** Do not read the remaining 5 as
> a partial failure of anything.
>
> **And «#295» must now define 55, not 50.** The five that newly became `[UNDEFINED]` are
> `P_HIGH_150K` · `P_HIGH_15K` · `P_HIGH_1K5` · `P_LOW_15K` · `P_LOW_1K5` — drive-strength
> selectors whose ONLY definition in the shipped set lived inside the deleted mislabel blocks, so
> removing the wrong description removed the only definition with it. That is remove-all working as
> designed, not a regression: «#295» defines them from the source, in the source's own words.
>
> The «#293» executor did not surface this — it never ran `audit-constant-fidelity.py`, which is
> not in its task's verify list. The arbiter measured it at the boundary by diffing HEAD against
> the working tree. A dispatched agent sees one task, not the dependency graph.

> **Origin.** An agent consuming the published KB could not work out how to use pull-ups and
> pull-downs, and reported conflicts around the smart-pin area (relayed by Stephen, 2026-08-24).
> Agent report is a lead, not a source; every item below was re-derived from
> `{{DOMAIN_AUTHORITY}}` before filing.
>
> **F-329 was added to this section 2026-08-24**, after the `p2-hardware-manual` DOCX re-ingestion
> found the *same* fabricated ladder in three further blocks of `io_pin_timing.yaml` that F-327's
> location line does not cover. It belongs to this root cause, not a new one.
>
> **Root cause, one sentence:** *the P2 has no pull-up or pull-down resistors, and the KB
> documents a whole family of them.* `P_HIGH_*` / `P_LOW_*` select **drive strength** — how hard
> the pin drives **while it is driving** — and the KB reframes them as always-on bias resistors.
> Every downstream error in this sweep follows from that one reframing.
>
> **NOT a regression of the 2026-07-01 `P_*` audit (F-177…F-183).** That audit's question was
> *"is this constant NAME legal in v55?"* — arbiter `pnut-ts`, enumeration the v55 manual — and
> its answer still holds: every name here is legal. It never asked whether the KB's **description**
> of a constant matches the source's. `P_HIGH_15K` is a legal name carrying a wrong definition,
> which the name audit cannot see by construction. **Name coverage is not semantic coverage.**
> This sweep is the first evidence of that gap having live consequences, and it is the case that
> motivates the source-fidelity gate.
>
> **Primary source for the whole sweep:**
> `engineering/ingestion/smart-pins-catalog/ingestionSources/basic-io/spin2-v51-extract.md`,
> the predefined-label tables at lines ~150–195, plus
> `engineering/ingestion/sources/silicon-doc/part4-smart-pins.txt` for the DIR/output rule.

### F-321 — the 16 `P_HIGH_*` / `P_LOW_*` drive-strength selectors are documented as pull-up/pull-down resistors — `PENDING-VALIDATION`

> **Where:** `language/spin2/concepts/basic-io.yaml:203-213` (`pull_up_modes:` / `pull_down_modes:`)
> and `language/pasm2/concepts/basic-io.yaml:271-281` (same two blocks, same values).
>
> **What is wrong.** The source names these by what they do; the KB renames them by what a reader
> coming from another MCU expects:
>
> | Constant | Source wording | KB wording |
> |---|---|---|
> | `P_HIGH_1K5` | Drive high 1.5kΩ | "1.5kΩ **pull-up** (strong)" |
> | `P_HIGH_15K` | Drive high 15kΩ | "15kΩ **pull-up** (medium)" |
> | `P_HIGH_150K` | Drive high 150kΩ | "150kΩ **pull-up** (weak)" |
> | `P_HIGH_1MA` | Drive high 1mA | "1mA constant current **pull-up**" |
> | `P_LOW_1K5` | Drive low 1.5kΩ | "1.5kΩ **pull-down** (strong)" |
> | `P_LOW_15K` | Drive low 15kΩ | "15kΩ **pull-down** (medium)" |
> | `P_LOW_150K` | Drive low 150kΩ | "150kΩ **pull-down** (weak)" |
> | `P_LOW_1MA` | Drive low 1mA | "1mA constant current **pull-down**" |
>
> The KB also drops the two ends of each ladder entirely — `P_*_FAST` (drive fast, 30mA; the
> default) and `P_*_FLOAT` (float) — and omits `P_*_100UA` / `P_*_10UA` from these blocks.
>
> **Why it matters, not just a wording preference.** A pull-up is active whenever the pin is not
> driven. A drive-strength selector applies **only while the pin drives that direction**. The two
> behave differently in exactly the case a reader reaches for a pull-up — a released bus, a button
> to ground — so the rename does not simplify the model, it inverts it. F-322 is the direct
> consequence.
>
> **Correction.** Restate all sixteen in the source's own terms — drive strength for the high side
> and the low side, selected independently — and delete the `pull_up_modes:` / `pull_down_modes:`
> framing. Where the reader's *intent* is a pull-up, document the idiom, not a fictional component
> (see F-325). Match the source's wording, not an interpretive paraphrase.
>
> **APPLIED 2026-08-25 by «#296» §5, across three tasks.** «#293» deleted the two `pull_up_modes:` /
> `pull_down_modes:` blocks; «#295» re-defined all sixteen from the source in the single home
> (`language/spin2/symbols/spin2-builtin-symbols-complete.yaml`); «#296» removed the surviving
> mislabel from every remaining site. `audit-constant-fidelity.py` `[CONTRADICT]` **5 → 0**
> (`PASS  no Tier 1 violations across 120 source-defined constant(s); 0 Tier 2`).
>
> **Sites corrected in this pass, with the source line each was matched against** — all four
> quantities re-read on disk 2026-08-25, and v55 (current edition) preferred over the v51 extract
> the tool cites:
>
> | Site | Was | Now | Source |
> |---|---|---|---|
> | `language/spin2/conventions/johnny-mac-documentation-style.yaml:303` | "150K pullup resistor" | `P_HIGH_15K` · "drive high 15 kOhm" | `sources/spin2-v55/spin2-v55-text.txt:1504` |
> | `language/spin2/conventions/spin2-docs-jonnymac.yaml:196` | "150K pullup resistor" | `P_HIGH_15K` · "drive high 15 kOhm" | `spin2-v55-text.txt:1504` |
> | `architecture/smart-pins/smart-pin-00000-normal-mode.yaml:53` | "Add pull-up" | "Drive high 15kOhm" | `spin2-v55-text.txt:1504` |
> | `architecture/smart-pins/smart-pin-00000-normal-mode.yaml:84` | "With pull-up" | "Drive high 15kOhm" | `spin2-v55-text.txt:1504` |
> | `language/pasm2/concepts/basic-io.yaml:241` | "Enable pull-up" | "Drive high 15kOhm" | `spin2-v55-text.txt:1504` |
>
> **Why the two `conventions/*.yaml` rows also change CONSTANT.** Their example is a bit-banged
> sensor read on a timing loop, and both were rewritten to the verified `weak_high` composition
> that `architecture/pin-drive-configuration.yaml` ships — which is stated with `P_HIGH_15K`
> (EF-063). `P_HIGH_150K` is the weakest resistive rung but one; holding a bit-banged line through
> it is not a composition any source or bench result states, so keeping the name would have meant
> shipping an unverified idiom to preserve a constant that was only ever incidental to a
> *documentation-style* example. The rung actually verified on silicon is what ships.
>
> **Plus eleven sites the instrument cannot see** (its limitation 3 — prose that names no constant,
> and a comment on the line *above* the constant rather than at end-of-line): the
> "internal pull resistors" framing in both `concepts/basic-io.yaml` summary/description/
> critical_distinction blocks and their `configuration_layer.methods` lists, the two
> `guides/*-getting-started.yaml` "pull resistors" blurbs, `hardware/addon-control-board.yaml`'s
> "internal pull-down (P_LOW_15K)" notes (×4 + 2 code comments),
> `hardware/p2-hardware-feature-comparison.yaml:141` (see **F-343**),
> `language/spin2/methods/pinfloat.yaml:67`, `language/spin2/methods/cogstop.yaml:110` and
> `code-examples/smart-pins-002-button-reading.yaml:62` (the last three said "pull-up/pull-down
> resistors" without saying *external*, which in a P2 file reads as a chip feature — each now says
> **external**, matching `pinfloat.yaml:78`'s own already-correct wording).
>
> **Not rewritten, because the source itself carries the mislabel:** `hardware/addon-rtc.yaml:49-51`
> — filed as **F-342**.
>
> **Verified, not asserted.** The zero was proved non-vacuous by a negative control: the mislabel was
> re-inserted into all five flagged files, `audit-constant-fidelity.py` reported exactly those five
> `[CONTRADICT]` rows, and the files were restored (`git status --short deliverables/ai/P2` back to
> the 12 intended files). A gate that cannot fail has not been verified.

### F-322 — every worked pull-up example disables the drive it just configured, so none of them work — `PENDING-VALIDATION`

> **Where — 8 sites, 3 files:**
> `language/spin2/concepts/basic-io.yaml:218-219, 229-230, 296-297, 377-378` ·
> `language/pasm2/concepts/basic-io.yaml:286-287, 348-349` ·
> `architecture/smart-pins/smart-pin-00000-normal-mode.yaml:53-54, 84-85`
>
> **The shape, in every one of them:**
> ```spin2
> PINSTART(16, P_HIGH_15K, 0, 0)   ' "15kΩ pull-up"
> PINFLOAT(16)                     ' "Input with pull-up"
> ```
> and its PASM2 twin, `WRPIN ##P_HIGH_15K` followed by `DIRL`.
>
> **Evidence it cannot work.** `part4-smart-pins.txt:74` — *"for smart pin mode off
> (%SSSSS = %00000): **DIR enables output**."* `PINFLOAT` / `DIRL` set DIR=0. With the output
> disabled the drive-high selector is inactive, so the pin is plain high-impedance: **no pull-up
> of any strength.** An agent following any of these ships a floating input whose reads depend on
> whatever is on the board.
>
> **What ships instead** ⚠️ *(this paragraph REWRITTEN IN PLACE by the arbiter 2026-08-25 during
> «#296». What stood here — a `WRPIN(pin, P_HIGH_15K | P_LOW_FLOAT)` attributed to a Silicon Doc
> §"Weak Pull-Up" — was **wrong about its source and is not shipped**. The section-preamble block
> above carries the full measurement. It is rewritten rather than annotated because a reader
> arriving top-down would otherwise act on a false claim before reaching the note that retracts
> it — which is the same two-places-drift defect this whole section is about.)*
>
> There is **no** Silicon Doc §"Weak Pull-Up"; `sources/silicon-doc/part4-smart-pins.txt` returns
> zero hits for pull-up/pull-down. Spin2 **v55** — the current edition — defines the two constants
> individually (`spin2-v55-text.txt:1504` *"Drive high 15kΩ"*, `:1519` *"Float low"*) and composes
> them into **no idiom at all**. The composition, and the word "pull-up" attached to it, are ours.
>
> The correct composition is **hardware-verified, which outranks documentary here** — EF-063/EF-064
> (`external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md:827,840`): `WRPIN` with
> `P_HIGH_15K`, then **DIR high** (`PINHIGH` / `DRVH`), and **no `P_LOW_FLOAT`**.
>
> 🔴 **The part of the original paragraph that was RIGHT, and is the finding's actual substance:
> DIR must be HIGH, not low.** A drive-strength selection does nothing while the pin is floated —
> that is precisely what F-322's `PINFLOAT`/`DIRL` examples destroyed, and why a clean compile
> proved nothing about them. Shipped in `architecture/pin-drive-configuration.yaml` as the
> `weak_high` / `weak_low` idioms, DIR stated in both.
>
> **Correction.** Rewrite all eight against the source idiom, with DIR high and the low side
> floated, and say plainly why DIR=0 defeats it — that sentence is the one a reader needs and no
> file currently contains it.
>
> 🔴 **The "What the source actually prescribes" paragraph above is SUPERSEDED** by the arbiter's
> attribution correction at the head of this section (2026-08-25). `P_HIGH_15K | P_LOW_FLOAT` under
> a §"Weak Pull-Up" heading is **our own** derived catalog extract, not a Parallax statement, and it
> was **not** shipped. Read that block before this one.
>
> **APPLIED 2026-08-25 by «#296» §5.** Four sites survived «#293»'s purge; all four were rewritten to
> the **hardware-verified** composition (EF-063 / EF-064,
> `external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md:827,840`) that
> `architecture/pin-drive-configuration.yaml` already ships — `P_HIGH_15K` with **DIR high**, and no
> `P_LOW_FLOAT`. Every one now carries the DIR sentence explicitly:
> *"DIR=1, OUT=1 - a drive is live only while DIR is high."*
>
> | Site | Was | Now |
> |---|---|---|
> | `architecture/smart-pins/smart-pin-00000-normal-mode.yaml:53-54` | `WRPIN(...P_HIGH_15K)` + `PINFLOAT` | `WRPIN` + `PINHIGH` |
> | `architecture/smart-pins/smart-pin-00000-normal-mode.yaml:84-85` | `WRPIN ##...P_HIGH_15K` + `DIRL` | `WRPIN` + `DRVH` |
> | `language/pasm2/concepts/basic-io.yaml` `button_read` | `WRPIN ##P_HIGH_15K` + `DIRL` | `DIRL` (pre-config) → `WRPIN` → `DRVH` |
> | `language/spin2/concepts/basic-io.yaml` `button_read` | `PINSTART(...)` + `PINFLOAT` | `PINCLEAR` → `WRPIN` → `PINHIGH` |
>
> **Plus one the finding's location line did not cover:** `language/spin2/concepts/basic-io.yaml`
> `application_examples.matrix_keypad` had the identical `PINSTART(... P_HIGH_15K ...)` +
> `PINFLOAT(...)` pair on the column pins, so the whole scan read undriven pins. Rewritten to the
> same idiom.
>
> **And the two `conventions/*.yaml` style files** carried the same shape a third way: they
> configured `P_HIGH_150K` and never raised DIR at all, then read the pin with `RDPIN` — which
> returns the *smart pin's* Z register and is meaningless with the smart pin off
> (`%SSSSS = %00000`). Both rewritten: `P_HIGH_15K` → `WRPIN` → `DRVH` → `TESTP … WC` → `RCL`.
>
> **Compiled AND read for semantics, separately — a clean compile is not a verification, and this
> finding is why.** All nine touched examples compile under `pnut-ts v1.55.3` from the *shipped YAML
> bytes* (extracted with `yaml.safe_load`, not retyped). `P_HIGH_15K` was confirmed to be `$1000`
> and `##P_NORMAL | P_HIGH_15K` confirmed to bind the `##` to the whole expression, by byte-identity
> of the compiled binaries against `##$1000` — and against `##($C0 | $1000)` for `P_TT_11`, so the
> control has a non-zero left operand.

### F-323 — the two `basic-io.yaml` files give contradictory mechanisms for the same feature — `PENDING-VALIDATION`

> **Where:** `language/spin2/concepts/basic-io.yaml:197-201` says internal bias is enabled
> *"via **PINSTART()** with special modes"*; `language/pasm2/concepts/basic-io.yaml:265-269` says
> *"via **WRPIN** smart pin modes."* Same concept, two files, two mechanisms.
>
> **Both are wrong, in different directions**, which is why this is filed separately from F-321.
> `WRPIN` alone sets the configuration but leaves DIR untouched. `PINSTART` is the *smart-pin*
> start sequence (WRPIN + WXPIN + WYPIN + DIRH) — using it to set a **non**-smart-pin drive
> strength starts a smart pin that was never wanted, and its DIRH is then immediately undone by
> the `PINFLOAT` on the next line (F-322).
>
> **This is the conflict the reporting agent hit.** It is the only true *conflict* in this sweep;
> everything else here is unanimous error, which is why a conflict-detection gate alone would not
> have caught the rest.
>
> **Correction.** One mechanism, stated once, in the file that owns the concept; the other file
> points at it rather than restating it.
>
> **APPLIED 2026-08-25 by «#296» §5 — by deletion and repointing, not by rewording both copies.**
> «#293» deleted both `internal_pull_resistors:` sections, which carried the two contradictory
> mechanism sentences. «#296» removed what survived them: the residual
> `- "PINSTART() - Enable internal pull resistors"` (spin2, `:29`) and
> `- "WRPIN - Enable internal pull resistors"` (pasm2, `:29`), plus the "pull resistors" phrase in
> both files' `summary:`, `description:` and `critical_distinction:`.
>
> **Neither file restates the mechanism now.** Both point at the single home built by «#295»:
> `deliverables/ai/P2/architecture/pin-drive-configuration.yaml` (index key
> `p2kbArchPinDriveConfiguration`), added as a **full path** in each file's `see_also:` alongside
> `.../spin2-builtin-symbols-complete.yaml`; the surviving `WRPIN` line names the target inline.
> Same repointing added to `architecture/smart-pins/smart-pin-00000-normal-mode.yaml` (`related:`)
> and `language/spin2/methods/pinfloat.yaml` (`see_also:`).
>
> 🔴 **No constant name was written as a YAML key anywhere in this pass.** That shape is what
> `audit-constant-fidelity.py`'s `DEF_RE` reads as a *definition*, and using it would have
> re-manufactured this very finding inside the task chartered to end it. Verified mechanically:
> the tool still attributes **120 source-defined constants** and reports **0** `DIVERGENT`.
>
> `validate-crossref-keys.py`: **3149 → 3156** references, **0 unresolved**, 100.0%.

### F-324 — `bits_M_6_0: "Control drive strength"` is wrong at both ends — `PENDING-VALIDATION`

> **Where:** `language/pasm2/concepts/basic-io.yaml:262`.
>
> **Evidence, decoded from the source's own bit patterns** (13-bit `%M..M` field, M12…M0):
>
> | Constant | Source pattern (M field) | Bits set |
> |---|---|---|
> | `P_HIGH_1K5` | `0000000001000` | M[3] |
> | `P_HIGH_150K` | `0000000011000` | M[4:3] |
> | `P_HIGH_FLOAT` | `0000000111000` | M[5:3] |
> | `P_LOW_1K5` | `0000000000001` | M[0] |
> | `P_LOW_FLOAT` | `0000000000111` | M[2:0] |
> | `P_INVERT_OUTPUT` | `0000001000000` | M[6] |
>
> So **drive-high = M[5:3]**, **drive-low = M[2:0]**, and the source's own encoding notes agree
> (`%…xxxxxxxHHHxxx…` and `%…xxxxxxxxxxLLL…`). **M[6] is output polarity, not drive strength.**
> The KB's `M[6:0]` wrongly annexes the polarity bit and erases the high/low split that makes the
> field usable.
>
> **Correction.** State the two 3-bit sub-fields with their positions. Also fix the companion
> dangling pointer at `language/spin2/concepts/basic-io.yaml:195` —
> *"Consult smart pin mode documentation for drive strength bit encoding"* — which points at
> nothing that exists (F-325 is what it should point at).
>
> **APPLIED 2026-08-25, in two tasks — verified on disk, not carried from the plan.**
>
> - **The wrong field itself is gone.** `bits_M_6_0: "Control drive strength"` was inside the
>   `wrpin_encoding:` block that «#293» deleted from `language/pasm2/concepts/basic-io.yaml`; the
>   companion dangling pointer at `language/spin2/concepts/basic-io.yaml:195` went with the same
>   purge. Confirmed by `grep -n 'wrpin_encoding\|bits_M_6_0'` over both files — **zero hits** —
>   and against `git show 15c84de5~1:` for what was removed.
> - **The correct layout ships**, stated by position, in the home «#295» built:
>   `architecture/pin-drive-configuration.yaml` `sub_fields:` — `output_polarity` **M[6]**,
>   `drive_high` **M[5:3]** (legend `HHH`), `drive_low` **M[2:0]** (legend `LLL`), plus `C` M[8],
>   `I` M[7] and the mode-select bits. The two sources that independently confirm the split are both
>   cited there: the Spin2 v55 symbol-table masks
>   (`sources/spin2-v55/spin2-v55-text.txt:1501` `%…xxxxxxxHHHxxx…`, `:1511` `%…xxxxxxxxxxLLL…`,
>   `:1497` the `O` polarity bit) and the P2 Datasheet 2022/11/01 p.24 Pin Mode Legend
>   (`sources/p2-datasheet/p2-datasheet-text.txt:1131-1147`), cell-identical in the P2 Hardware
>   Manual (`sources/p2-hardware-manual/p2-hardware-manual-text.txt:847-873`).
> - **Nothing in «#296» re-states it.** Per R4 the touched files point at that home rather than
>   carrying a second copy of the bit ranges.

### F-325 — the drive-strength ladder is fully documented in the ingestion tree and entirely absent from the shipped KB — `PENDING-VALIDATION`

> **APPLIED 2026-08-25 by «#295» phase 2, in two homes with a boundary between them.**
>
> - **`language/spin2/symbols/spin2-builtin-symbols-complete.yaml`** — 68 records added, so the
>   file now defines **all 116** `P_*` constants the Spin2 v55 symbol table carries
>   (`spin2-v55-text.txt:1419-1562`), each with the source's own wording, its 32-bit value and its
>   bit pattern. `audit-constant-fidelity.py` `[UNDEFINED]` **55 → 0**, exit 1 → 0. Fourteen
>   pre-existing glossed descriptions were re-worded to v55 in the same pass, and a top-level
>   `aliases:` block was added so those 116 names are reachable through the published index at all —
>   `generate-p2kb-index.py` harvests top-level `aliases:` only, and this file had none, so not one
>   of its constants was findable by name.
> - **`architecture/pin-drive-configuration.yaml`** *(new)* — the `%M..M` field: every sub-field
>   with its bit range (this is also F-324's "state the two 3-bit sub-fields"), the eight-rung drive
>   ladder, and the DIR/OUT rule.
>
> 🔴 **The ladder is stated BY ENCODING, never as `NAME: "description"`.** That shape is what
> `audit-constant-fidelity.py` reads as a *definition*, so writing the ladder the natural way would
> have made the new file a **second definition home** for 16 constants and re-manufactured
> F-321/F-323 inside the task chartered to end them. Verified mechanically, not by eye: the tool's
> own `DEF_RE`/`RECORD_RE` match **0** lines in the new file, and the tool attributes **0**
> definitions to it. Measured after: **116 constants defined in the KB, 0 with more than one
> definition, 0 defined outside the single home** (down from 58 defined across two homes with 7
> duplicated).
>
> **The pull-up idiom this finding asks for is NOT shipped as documentary** — see the arbiter's
> F-322 attribution correction above. What ships is the hardware-verified composition
> (EF-063/EF-064): `P_HIGH_15K` / `P_LOW_15K` with **DIR high**, and no `P_LOW_FLOAT`. Both idioms
> carry DIR explicitly, because omitting it is exactly F-322. Both compile under `pnut-ts` v1.55.3
> and were read for semantics; the unverified `P_HIGH_15K | P_LOW_FLOAT` variant is filed as a gap
> (**F-336**), not shipped as content.
>
> **Owed:** index regeneration + `validate-crossref-keys.py` after the boundary commit — the new
> file's index key `p2kbArchPinDriveConfiguration` does not exist until then.

> **What is missing.** Eight high-side values and eight low-side values, each with its bit pattern
> and its meaning — `FAST (30mA)` · `1K5` · `15K` · `150K` · `1MA` · `100UA` · `10UA` · `FLOAT` —
> plus the sub-mode selectors that share the field (`P_SYNC_IO`, `P_INVERT_IN`,
> `P_INVERT_OUTPUT`, the `P_TT_*` / `P_OE` / `P_BITDAC` DIR-OUT controls).
>
> **Where it already exists:** `basic-io/spin2-v51-extract.md:150-195`, as clean tables. It was
> extracted and never promoted into a YAML. Sixteen shipped files *use* these constants; **no
> shipped file defines them.**
>
> **Correction.** Promote the ladder into the KB. Placement is a design decision to settle before
> editing (new `architecture/pin-drive-configuration.yaml` vs. extending the `basic-io` pair) —
> flag it per the `sprint-plan` overlay's design-decision rule rather than deciding it in passing.
> The pull-up/pull-down *idiom* belongs here too, stated as a composition of drive settings
> (`P_HIGH_15K | P_LOW_FLOAT`, DIR high) rather than as a component the chip does not have.

### F-326 — `wrpin.yaml` expands three of its six D-operand fields and stubs the one that carries the pin configuration — `PENDING-VALIDATION`

> **APPLIED 2026-08-25 by «#295» phase 2. The deferral now has somewhere to go.** The stub
> `M: "13-bit low-level pin control + smart-pin mode"` is gone; `pasm2/wrpin.yaml`'s
> `d_operand_format.fields:` now points at `architecture/pin-drive-configuration.yaml` for the
> field's internals and at `architecture/smart_pins.yaml` for all six field ranges. The finding's
> own instruction — *"point it at the file F-325 creates, but not at prose that does not exist"* —
> is what was done. `architecture/smart_pins.yaml` gained the reciprocal pointer inside
> `configuration_format.fields.m:`.
>
> **The companion check this finding asks for was done too.** `language/spin2/methods/wrpin.yaml`
> had the same shape *and worse*: `common_smart_modes:` (13 keys) and `tt_field.constants:`
> (4 keys) were **17 second definitions** of constants the symbols file also defines. Both blocks
> are replaced with pointers; the four `P_TT_*` keep their values, binaries and `P_OE`/`P_CHANNEL`/
> `P_BITDAC` aliases in `smart_pins.yaml`, so nothing is lost. Everything else in `tt_field:` —
> `context_dependent:`, `p_oe_required_for:`, `one_bit_three_names:`, `when_smart_pin_on:`,
> `source_selection:` — is field *behaviour*, is cited and correct, and is untouched.
>
> **Owed:** index regeneration + `validate-crossref-keys.py` after the boundary commit.

> **Where:** `language/pasm2/wrpin.yaml`, `d_operand_format.fields`. `AAAA`, `BBBB` and `FFF` get
> full treatment — `input_selectors` enumerates all eight source-select encodings and the invert
> bit. The 13-bit field is one line: **`M: "13-bit low-level pin control + smart-pin mode"`**.
> `language/spin2/methods/wrpin.yaml` should be checked for the same shape.
>
> **Why it happened, and why it is still ours to fix.** The Silicon Doc defers at exactly this
> field — *"In the Spin2 documentation, there are many predefined labels documented, which cover
> these pin configurations"* (`part4-smart-pins.txt`, after the `%FFF` table). The ingestion
> followed the source faithfully to the deferral and then **stopped at the pointer instead of
> following it**, even though the target was itself ingested (F-325). `wrpin.yaml` is where an
> agent asking "how do I configure a pin" lands, so the stub sits directly on the path that
> generated this whole sweep.
>
> **Correction.** Expand the field, or point it at the file F-325 creates — but not at prose that
> does not exist. **A deferral in a source is a work item, not an answer**, and this sweep is the
> cost of treating one as an answer.

### F-327 — `io_pin_timing.yaml` documents a pin drive-strength system, and a slew-rate control, that no source describes — `PENDING-VALIDATION`

> **Where:** `architecture/io_pin_timing.yaml:200-233` (`drive_strength_configurations:`)
> and `:234-246` (`slew_rate_control:`).
>
> **This is a different and more severe class than F-321.** F-321 is a *mislabel* — the KB
> renamed a real mechanism. This is **fabrication**: the KB describes a mechanism that does
> not exist. Four claims, none of which any authoritative source states:
>
> | KB claim | Source check |
> |---|---|
> | Drive ladder `1.5mA · 3.0mA · 15mA · 30mA · 75mA · 150mA` | **Not in any source.** The real ladder is `FAST (30mA) · 1.5kΩ · 15kΩ · 150kΩ · 1mA · 100µA · 10µA · FLOAT`, eight values per side. |
> | Impedance table `~2000Ω · ~1000Ω · ~200Ω · ~100Ω · ~40Ω · ~20Ω` | **Zero hits** for this framing in `sources/silicon-doc/`. |
> | `WRPIN_bits: "M[6:5,4:3,2:1,0]"` | Wrong. Drive-high is `M[5:3]`, drive-low `M[2:0]`, and `M[6]` is output polarity (see F-324). |
> | `slew_rate_control:` — fast/slow slew, `<2ns` / `5-10ns`, EMI trade-off | **The string "slew" appears ZERO times** across `sources/silicon-doc/`, `sources/spin2-v51/`, and `smart-pins-catalog/`. The P2 has no documented programmable slew rate. |
>
> **Independent confirmation of the real encoding**, from a second source not used for F-324 —
> `sources/silicon-doc/assets/images-20260706/P2-Silicon-Doc-v35_image_catalog.md:139,161`
> describes the WRPIN figure's own legend: *"HHH/LLL Drive-strength"* and *"the H/L → DRIVE
> strength table (000 Digital, 001 1.5k, 010 15k, 011 150k, …)"*. Three bits per side, and the
> ladder is resistive, exactly as the Spin2 label table has it.
>
> **Likely provenance, offered as a lead and not as a finding:** `150mA` *does* appear in the
> sources — as the **VIO group current budget** (`p2-complete-signal-flow-matrix.md:193-200`),
> a board-power fact about eight-pin groups. A per-pin drive ladder built from a per-group
> power limit would explain the shape. Do not act on this without checking; it is a hypothesis
> about how the text arose, not a source.
>
> **The tell that makes this mechanically detectable.** The same file cites sources where it
> has them — `absolute_maximum_ratings:` names the Parallax Datasheet (`:267`), and
> `input_voltage_and_protection:` names Silicon Doc v35 in its `latchup_context.source` (`:296`).
> The two fabricated blocks carry **no `source:` field at all**. A file that demonstrates it knows
> how to cite, and then states six quantities and a whole feature without citing anything, is
> flagging itself.
>
> ⚠️ **ATTRIBUTION CORRECTED 2026-08-24 (arbiter, during «#293»).** This paragraph originally
> credited `:296` to **`special_timing_modes:`**. That was wrong, and it mattered: at the HEAD this
> finding was written against, `:296` is a `source:` nested under `latchup_context:` inside the
> **preceding** block `input_voltage_and_protection:` (`:276-297`); `special_timing_modes:` began at
> `:298` and was itself **genuinely uncited** — which is why the sourcing tool flagged it and «#293»
> removed it. The finding's conclusion is unaffected (`:267` does cite, and both fabricated blocks
> do not). Only the second example was misattributed, by exactly the off-by-one-block error that
> **citing a register finding by line number instead of by ID** produces. Resolve findings by ID.
>
> **Correction.** `slew_rate_control:` has no correct form — **delete it outright**; there is
> nothing to align it to. `drive_strength_configurations:` is replaced by the real ladder,
> which after F-325 lands should be a pointer to the single definition home rather than a
> fourth copy. Neither block is "corrected in place": an unsourced claim is removed, not
> rewritten, per this register's no-inference rule.
>
> **Why the fidelity instrument did not catch this, and what it means for the gate.**
> `audit-constant-fidelity.py` compares the KB's description of a *named constant* against the
> source's. These blocks **name no constants** — they describe the mechanism in prose and
> numbers. That is limitation 3 in the tool's own docstring, and it proved itself within the
> hour of being written: *name coverage is not semantic coverage, and that cuts both ways.*
> Detecting this class needs a second detector — **an uncited quantitative claim in a file that
> cites elsewhere** — which is the "information that should no longer be in the files" half of
> the release gate, and is now sprint scope rather than a nice-to-have.
>
> **Class-wide sweep result (2026-08-24): the manuals are CLEAN.** No manual or app-note
> opus-master carries the fabricated ladder, the impedance table, or a pin slew-rate claim.
> (`architect-guide-body.md`'s "slew" hits are rate-adapters in a dataflow sense — unrelated.)
> This class is confined to the YAML, so no manual corrections wave follows from it.

> **APPLIED «#293» 2026-08-24 — REMOVED, repopulation owed.** Both named blocks are gone from
> `architecture/io_pin_timing.yaml`, removed as whole top-level blocks at their entry-state ranges:
> `drive_strength_configurations:` **`:200-233`** (34 lines, 21 quantities) and `slew_rate_control:`
> **`:234-246`** (13 lines, 2 quantities). Removed under the sprint's remove-all rule (D7), **not**
> corrected in place — this entry's proposed "replaced by the real ladder" is withdrawn as
> claim-first; the `SOURCE-REPAIR-ORDER` rule (agent-side) §2 governs, and «#299» re-derives from the
> repaired source or not at all. `slew_rate_control:` is **never** repopulated.
>
> **The zero-hit `slew` claim re-verified at HEAD**, now across five source trees rather than three
> — `sources/silicon-doc`, `sources/spin2-v51`, `smart-pins-catalog`, and both of this sprint's
> re-ingestions, `sources/p2-datasheet` and `sources/p2-hardware-manual`: **0 hits each**.
>
> **«#299» 2026-08-25 — the repopulation decision is made and it is NOTHING.** Working the sources
> rather than the blocks, no Parallax document states a per-pin milliamp drive ladder, an impedance
> table, or a slew rate; the datasheet states drive as eight named MODES
> (*"Separate drive modes for high and low output: logic / 1.5 k / 15 k / 150 k / 1 mA / 100 µA /
> 10 µA / float"*, `sources/p2-datasheet/p2-datasheet-text.txt:117`), which already ship cited in
> `architecture/pin-drive-configuration.yaml drive_ladder`. **None of F-327's or F-329's nine
> `io_pin_timing.yaml` blocks returned**, nor the four `basic-io.yaml` copies. Instead, the two
> `pin_architecture` blocks came back carrying a `no_milliamp_ladder:` key that states the absence
> and points at the definition home, so the next agent to look finds a denial rather than a silence.
>
> `PENDING-VALIDATION` — the removal is applied, the repopulation question is answered, and only
> the YAML release is owed.

### F-329 — the SAME fabricated drive ladder stands twice more in `io_pin_timing.yaml`, in blocks F-327 does not name, alongside ~20 nanosecond quantities that NEITHER of the sprint's two extraction paths carries — `PARTIAL`

> **Found:** 2026-08-24, by the DOCX-primary re-ingestion of `p2-hardware-manual` (the source
> plan §8 names as the datasheet's cross-check partner). This is **additive to F-327, not a
> re-file**: F-327's location line is `:200-233` + `:234-246`, and every claim below sits
> **outside** those ranges. Applied literally to the lines it names, F-327's fix would leave the
> fabricated ladder standing in two other blocks of the same file.
>
> **Where — three blocks, none of them named by F-327:**
>
> | Lines | Block | What it carries |
> |---|---|---|
> | `:96-105` | `timing_specifications.output_timing.propagation_delay.fast_mode` / `.normal_mode` | `2.5/3.5/5.0 ns` and `3.5/5.0/7.0 ns` |
> | `:108-113` | `…propagation_delay.drive_strength_impact` | **2nd copy of the fabricated ladder** — `1.5mA · 3.0mA · 15mA · 30mA · 75mA · 150mA`, each with a ns delta |
> | `:118-137` | `…output_timing.rise_time.configurations` | **3rd copy** — five `drive:` entries `150mA/75mA/30mA/15mA/1.5mA`, each with a `15pF` load and a ns rise time |
> | `:145-158` | `timing_specifications.input_timing.propagation_delay` | `2.0/3.0/4.5 ns`, `3.5/5.0/7.0 ns` |
>
> **None of these blocks carries a `source:` field** — the same self-flagging tell F-327 identified.
>
> **1. The cited datasheet pages do not exist.** Line 3 reads
> `# Datasheet Reference: pages 42-45, 76-78, Electrical Specifications`.
> `Propeller2-P2X8C4M64P-Datasheet-20221101.pdf` is **50 pages** (`pdfinfo`). Pages 76-78 cannot
> exist. Its electrical tables are **DC Characteristics on p.47 and AC Characteristics on p.48**;
> pages 42-45 are not them. This is not an off-by-a-few citation — it points outside the document.
>
> **2. Neither of the two independent extraction paths carries I/O-pin timing in nanoseconds.**
>
> - **Path A — P2 Hardware Manual (2022/11/01), re-ingested DOCX-primary 2026-08-24.** Its
>   *I/O Pin Timing* section states delay **only in clock cycles** ("three additional clocks",
>   "three clocks before", "two clocks before"). Its three timing diagrams
>   (`assets/images-p2-hardware-manual-20260824/fig-34..36`, newly extracted — this source had
>   **no image catalog at all** before) are clock-numbered `0..6` with **no nanosecond axis**;
>   `fig-34` was rendered and read to confirm. Across the whole extract
>   (`p2-hardware-manual-text.txt`, 159,098 chars) the unit tokens present are
>   `MHz · V · ms · kΩ · kHz · Ω · µA · pF · mA` — **`ns` appears zero times, and so does the word
>   "nanosecond"**. The document has no nanosecond quantity anywhere in it.
> - **Path B — P2 Datasheet.** Its AC Characteristics table contains exactly **two** symbols:
>   `Freq` (oscillator frequency) and `Cin` (XI/XO pin capacitance). There is no propagation-delay,
>   rise-time or input-timing row anywhere in it.
>
> **Stated as a measurement, not a verdict:** the datasheet's extraction is the known-broken
> `p2-datasheet-narrative.txt`, so "the datasheet does not say X" is weaker evidence than
> "the hardware manual says Y". The AC table's *content* is present in that extract (all symbols,
> parameters, conditions, values and units, merely column-linearized) and it is the only AC table
> in a 50-page document — but **the `camelot lattice` pass owed by plan §8 is what settles it**.
> The drive-ladder half below does not depend on that and is decisive on its own.
>
> **3. The relabeling is decisive on documentary grounds.** The P2 Hardware Manual gives the pin
> drive ladder in two independent places within itself, and both are **resistive**:
>
> - **Table 18's nested legend** (`complete-tables-reference.md`, Table 21 — a table nested inside
>   a cell, which is why a naive DOCX walk drops it): `HHH/LLL` = `000 Fast · 001 1.5 kΩ ·
>   010 15 kΩ · 011 150 kΩ · 100 1 mA · 101 100 µA · 110 10 µA · 111 Float`.
> - **The equivalent-schematic figures** (`fig-10`..`fig-33`), whose on-diagram legend reads
>   `000 Digital · 001 1.5k · 010 15k · 011 150k · 100 1mA · 101 100uA · 110 10uA · 111 Float`.
>
> The KB's `1.5mA / 15mA / 150mA` reuse the numerals of the **kΩ** rungs with the unit changed.
> This is the third source to say so, after F-324's bit-pattern decode and F-327's silicon-doc
> image catalog.
>
> **4. Two of the fabricated rungs exceed the device's rated maximum.** Both sources agree the
> **maximum current per I/O pin is ±30 mA** (Hardware Manual *Specifications* table, verbatim
> `Max current per I/O | +/- 30mA`; the datasheet's DC Characteristics characterises `Vol`/`Voh`
> at sinking/sourcing 1 mA, 10 mA and 30 mA — 30 mA is the top of its own characterisation).
> A `75mA` or `150mA` per-pin drive mode is not a P2 capability, so `rise_time` rows keyed to
> them describe nothing.
>
> **What is NOT wrong in this file, and must survive the purge.** `instruction_to_pin_timing:`
> (`:16-89`) is **exactly corroborated** by the Hardware Manual, clause for clause: output latency
> 3 clocks after the instruction; `INx` reads 3 clocks stale; `TESTP`/`TESTPN` 2 clocks stale
> ("fresher than INx"); smart-pin IN drop 2 clocks after `WRPIN/WXPIN/WYPIN/RDPIN/AKPIN`. That is
> the corroborated core of the file and it is *un*cited today — it needs a citation added, not
> removal. **Recording this is the point of running the ingestion before the purge**: without it,
> a remove-all sweep over uncited quantitative blocks takes the good half with the bad.
>
> **Correction.** Remove `:96-105`, `:108-113`, `:118-137` and `:145-158` under the sprint's
> source-first rule (an uncited claim is removed, not rewritten). Fix or delete the impossible
> page citation on line 3. Re-derive `instruction_to_pin_timing:` in place with a citation to
> the Hardware Manual's *I/O Pin Timing* section. Fold the drive-ladder occurrences into whatever
> single definition home F-325 creates rather than leaving a fourth, fifth and sixth copy.
>
> **Lesson for the sweep that follows.** F-327 found this class and named two blocks; the same
> fabrication was sitting in three more blocks of the same file, and the deciding evidence for
> two of them was **inside a table nested in another table's cell** and **inside a figure**.
> A finding's location line is where it was *seen*, never the extent of the defect —
> sweep the file, not the line range.

> **APPLIED «#293» 2026-08-24 — REMOVED, one item owed.** All four locations this entry names sit
> inside the single top-level block `timing_specifications:` (`:90-172` at entry state), which was
> removed whole — 83 lines, 45 quantities — taking `:96-105`, `:108-113`, `:118-137` and `:145-158`
> with it. Six further uncited quantitative blocks in the same file went in the same pass, per this
> entry's own "sweep the file, not the line range": `clock_relationships:` `:173-199`,
> `input_characteristics:` `:247-262`, `special_timing_modes:` `:298-320`,
> `protocol_timing_examples:` `:321-337`, `compensation_techniques:` `:359-374`,
> `best_practices:` `:375-391`. The file went 433 → 175 lines (`wc -l`).
>
> **The impossible page citation is gone in both of its two locations** — the header comment
> (`# Datasheet Reference: pages 42-45, 76-78, Electrical Specifications`) *and* its restatement
> inside `extraction_metadata.source_documents` as a `- document: "P2 Datasheet"` entry listing the
> same two ranges plus "Timing characteristics tables". This entry named only the header; sweeping
> the file found the second copy, which is this entry's own lesson applied to itself.
>
> **`instruction_to_pin_timing:` survived, as this entry requires** — it is intact at `:15` and was
> never flagged (it states delay in clocks, which carry no unit token). Its citation is owed to
> «#299», and its corroboration is already found and recorded here.
>
> `PARTIAL` because the removals are applied and the `instruction_to_pin_timing:` citation is owed.

### F-333 — the fabricated slew-rate claim ALSO stood in `io_pin_timing.yaml`'s top-level `description:`, where no instrument could see it, because it carries no unit — `PENDING-VALIDATION`

> **Found:** 2026-08-24, by «#293», *after* removing every block F-327 and F-329 name. A residual
> `grep -i slew` over the file — run because F-329's lesson says to sweep the file, not the line
> range — returned one surviving hit that both prior findings had walked past.
>
> **Where:** `architecture/io_pin_timing.yaml:9-14`, the top-level `description:` block, reading
> *"Each pin can be configured for different drive strengths, slew rates, and input
> characteristics."* Removed whole (6 lines). The file now returns **0** hits for `slew`.
>
> **Why no instrument caught it, and this is the point of the finding.**
> `audit-yaml-claim-sourcing.py` fires on an uncited block that states a **physical quantity**, and
> a quantity requires a **unit token** — that is what makes the gate mechanical rather than a matter
> of taste. This sentence names the fabricated *mechanism* and attaches **no number to it at all**,
> so it scores zero quantities and is structurally invisible to the gate, exactly as
> `audit-constant-fidelity.py` was structurally blind to F-327 for naming no constants.
>
> **Both of this sprint's instruments therefore share one shape of blind spot:** each keys off a
> *token* — a constant name, a unit — and a fabrication written in plain prose carries neither. The
> gate is still worth having; it found 59 blocks in these four trees. But **passing it is not
> evidence that a file is free of fabrication**, and no release note should imply otherwise.
>
> **No new evidence is owed.** The claim is F-327's, already `CONFIRMED`, and «#293» re-verified its
> zero-hit basis across five source trees at HEAD. This entry records a third *location*, not a new
> claim.
>
> **Consequence for «#299»:** `io_pin_timing.yaml` now has no top-level `description:`. Whatever is
> written back must not restore "slew rates", and must come from the repaired Hardware Manual /
> Datasheet rather than from the removed text.
>
> **REPLACEMENT WRITTEN 2026-08-25 by «#299».** `architecture/io_pin_timing.yaml` now carries a
> top-level `description:` derived from the repaired P2 Datasheet, cited to
> `sources/p2-datasheet/p2-datasheet-text.txt:117` and `:2126-2149`. It says what the file carries
> (instruction-to-pin latency, absolute maximum ratings, 5 V handling) and then says outright what
> it does NOT carry and where those live — drive strength at
> `architecture/pin-drive-configuration.yaml`, and slew rate nowhere, because there is none.
>
> ⚠️ **THE ZERO-HIT CRITERION IN THIS ENTRY IS NOW WRONG AND MUST NOT BE RE-RUN AS WRITTEN.**
> `grep -ci slew` on `io_pin_timing.yaml` returns **2**, and both hits are the new description
> **naming slew rate in order to forbid it** — the same deliberate-mention shape
> `audit-guide-conformance.py` already classifies as `[D6] named in order to forbid it`, and the
> same shape `pin-drive-configuration.yaml not_documented_here` uses. The correct check is that no
> hit ASSERTS a slew rate. Stated here explicitly so a later sweep does not "fix" the denial back
> into a silence, which is what let this claim survive two purges in the first place.
>
> `PENDING-VALIDATION` — the removal and the replacement are both applied; only the YAML release
> is owed.


---

## Open — CONFIRMED corrections (2026-08-11, DeSilva reader-report sweep)

> **Sweep origin:** a reader reported that the DeSilva tutorial's Ch.1 "Experiment 3:
> Fading" does not fade on a P2 EVAL (#64000 Rev B) — copied, pasted, triple-checked.
> Root cause: the smart-pin mode was written **without `P_OE`**, so the smart pin
> generated the PWM but the pin's output driver stayed disabled. Confirmed against
> `language/spin2/methods/wrpin.yaml` `tt_field` — `when_smart_pin_on: "x0=output
> disabled, x1=output enabled (regardless of DIR)"` and `p_oe_required_for: "All output
> modes (NCO, PWM, Pulse, Transition, Serial TX, DAC, USB)"`. The manual was fixed the
> same pass; **the same class is still present in the KB's own examples**, below.
> Note this class had already been fixed once in DeSilva (v3.0.3 corrected the
> async-serial TX recipe to `P_ASYNC_TX | P_OE`) but was **not swept class-wide** —
> which is how the PWM example survived to a reader.

- **F-250 — the #64000 Eval Board Rev C guide was ingested with EVERY DIGIT MISSING; any
  numeric fact traced to it is unsafe.** — `PARTIAL` · `engineering/ingestion/sources/p2-eval-board/`
  was extracted with a text-layer tool, but that PDF's font encoding does not map numerals —
  `pdftotext` silently drops them. Evidence: the shipped `p2-eval-board-narrative.txt` has
  digits on **91 of 1315 lines**; `pdf-ocr --force-ocr` + re-extract yields **368**. Lines
  read *"The Propeller has cores, KB of hub RAM, and Smart I/O pins"* (8 / 512 / 64 gone)
  and *"Buffered LEDs on top eight I/O pins"* survives only because "eight" is spelled out.
  **Consequences:** (1) the LED pin map sat as `TBD` in `hardware/p2-eval-board.yaml` for
  months while the answer was in the repo (F-248) — no grep for `P56` could hit a document
  with no digits; (2) **every** voltage, current, capacity, pin number, part number and page
  reference sourced from this extraction is suspect; (3) the extraction audit and
  cross-source analysis both list "LED pins" as a *gap*, so the loss was mistaken for the
  source being silent. **→ TRACKED → ingestion:** re-ingest this source with forced OCR,
  re-verify every numeric claim already derived from it, and — the general lesson —
  **add a digit-density sanity check to the ingestion pass**: a hardware document whose
  extraction is nearly digit-free has failed, not been read. Worth spot-checking the other
  board/hardware sources for the same font family.
  >
  > **INGESTION HALF APPLIED 2026-08-24** (sprint task #306, ahead of the #294 purge — under
  > remove-all, whatever this failed to recover would have been *permanently* gone).
  >
  > - **Re-ingested, forced OCR.** `pdf-ocr --force-ocr --deskew` → `pdftotext -layout` →
  >   `engineering/ingestion/sources/p2-eval-board/p2-eval-board-text.txt`. Density
  >   **1.5% → 56.5%** on the gate tool's metric (lines of ≥12 chars), **10.0% → 52.6%** on
  >   non-blank lines — the frame this filing used above, where its 91/1315 counted every
  >   line including blanks. Quote the metric with the number; they are not interchangeable.
  >   In the 29–58% peer band. Prior capture archived, not deleted:
  >   `sources/p2-eval-board/archive/` (+ `archive/README.md` pointer, + a fresh `pdftotext`
  >   run kept as the evidence exhibit).
  > - **Recovered, triple-validated** (OCR ∩ original text layer ∩ rendered page — the two
  >   text layers are complementary here: the body font keeps letters and drops digits, the
  >   *table* font keeps digits and drops letters). Both ruled tables re-cut with
  >   `camelot lattice`; `pdf2md`/docling added as a fourth leg across all 17 pages (whole-doc
  >   runs OOM'd; `pdfseparate` + one page at a time got through) and agrees throughout.
  >   **All 17 pages read against their rendered image; nothing
  >   unrecoverable.** Curated capture: `sources/p2-eval-board/complete-p2-eval-board-reference.md`.
  >   Two things only the rendered page could give: the edge-header **pin order** (in no text
  >   layer at all), and that the boot-mode switch columns are the silkscreen triangles
  >   **P59 △ / P59 ▽** — OCR reads them as the letters "A"/"V".
  > - **Downstream re-verified.** `sources/p2-eval-board/p2-eval-board-rev-c-complete-extraction-audit.md`
  >   (its false "100% across the board" replaced by measured coverage) and
  >   `sources/p2-eval-board/p2-eval-board-cross-source-analysis.md` (which had described a
  >   board with a barrel jack, a proto area and VGA/HDMI — none of it in the source).
  >   `engineering/ingestion/README.md:51` no longer reads `100% (stated)`.
  > - **The general lesson is now an instrument, not a note.**
  >   `engineering/tools/validation/audit-extraction-digit-density.py`, wired into
  >   the `ingest-source` skill (agent-side) **§2a as a mandatory pass-1 gate** (plus the
  >   pass-1 convention list, the §7 hand-back, and *What NOT to do*). Corpus sweep
  >   `--all`: **clean, 53 artifacts**, 4 hand-written folder descriptions exempted by name
  >   with reasons. Negative control: the archived lossy artifact scores 1.5% and exits 1.
  > - **Spot-check of the other board/hardware sources: `p2-eval-board` was the only
  >   outlier** (10% against 29–58% across eleven peers). **This is not a clean bill of
  >   health for the other eleven** — digit density catches *total* numeral loss, never
  >   partial. It is a smoke alarm.
  >
  > **What is still owed, and by whom:** the #64000 board YAML itself. Re-verification found
  > claims the repaired source contradicts or does not contain — filed separately as
  > **F-328**, and repaired by the sprint's purge/repopulate tasks, not here. The ingestion
  > head is done with this one.
  >
  Status: `PARTIAL` — ingestion half complete 2026-08-24; the KB-side re-derivation it
  exposed is carried by F-328.

- **F-251 — the "why do the LEDs glow when I touch a pin" explanation must account for the
  LED BUFFER, and the freshly-shipped DeSilva v3.0.5 aside does not.** — `PARTIAL` · The #64000 guide
  (feature 12) and both Edge module YAMLs describe the onboard LEDs as **buffered** — the P2
  pin drives a buffer *input*, and the buffer drives the LED. DeSilva v3.0.5's new Chapter 1
  aside "Why Your LEDs Glow When You Touch Them" instead explains the effect as microamps
  coupling *through the LED itself*, which would produce a faint glow. On a buffered board
  the floating **buffer input** picks up the coupling and the buffer drives the LED at full
  strength — which matches the reader's actual report ("the leds will light up", not "glow
  faintly"). The aside's conclusion (floating pins have no opinion; drive them or use
  pull-ups) is right; the mechanism is wrong. **→ manual head:** correct the aside in the
  next DeSilva patch. Also worth stating there that on the #64000 **P58-P63 are shared with
  the USB-data and memory signals**, so those LEDs are active at power-up and after reset by
  design — a second, entirely non-mysterious reason a reader sees lit LEDs.

  > **EVIDENCE BASE MOVED 2026-08-24 by the «#294» uncited-block purge — read before citing.**
  > This finding's premise says *"the #64000 guide (feature 12) and **both Edge module YAMLs**
  > describe the onboard LEDs as buffered."* **The Edge half of that is no longer true of the
  > KB.** The purge removed `pin_mapping` from both Edge module YAMLs, and with them every
  > `led_buffered` entry; `buffer` now matches nothing LED-related in either file (only
  > unrelated "framebuffer" prose).
  > **What still stands, and is the stronger citation anyway:**
  > `hardware/p2-eval-board.yaml:27` `type: "Buffered LED bank"` and `:29` `buffer: "Driven
  > through an LED buffer that isolates them from the I/O signals"` — inside the
  > `built_in_peripherals` block, which survived the purge *and* carries a real `source:` line
  > (`:45`) naming the #64000 Rev C Guide feature 12. The P58-P63 shared-signal point this
  > finding also wants stated is at `:31-34` (`power_at_startup`), same block, same citation.
  > So the manual fix is **not blocked** — cite the eval-board file, not the Edge files. If the
  > buffered-LED fact is wanted for the Edge modules specifically, it is «#307» repopulation
  > work, source-first from the Edge module guides.

  > **RE-MEASURED 2026-08-25 («#301»). The mechanism half was ALREADY FIXED — and the sentence this
  > finding called "right" is the one that was wrong.**
  >
  > **What was already done, on 2026-08-17.** Commit `a0fb4884` (*"DeSilva v3.0.5: the LEDs are
  > buffered — correcting the aside I shipped hours ago"*) rewrote the Ch.1 aside. It now teaches
  > exactly the buffered mechanism this finding asked for — *"Your P2 pin doesn't feed the LED
  > directly; it feeds the *input* of a buffer… It takes very little to push that floating input past
  > the buffer's threshold, and when it crosses, the buffer switches: the LED doesn't glimmer, it
  > comes **on**"* — and it carries the P58–P63 shared-signal point this finding also wanted, as a
  > second, non-mysterious cause. Nothing was owed on the mechanism.
  >
  > 🔴 **What was NOT done, and was a live defect until today.** This entry ends by saying *"the
  > aside's conclusion (floating pins have no opinion; drive them or use pull-ups) is right."*
  > **The pull-up half is not right, and the aside shipped it**: `COMPLETE-OPUS-MASTER.md:294` read
  > *"If you want a pin held at a known level **without driving it**, the P2 gives you pull-ups and
  > pull-downs for exactly that."* The P2 has **no bias resistors at all** — `P_HIGH_*`/`P_LOW_*`
  > select **drive strength**, and per the Pin Mode Legend a drive selection is live **only while DIR
  > is high** (`deliverables/ai/P2/architecture/pin-drive-configuration.yaml:41-43`, `:166-171`,
  > sourced to P2 Datasheet 2022/11/01 p.24). So the sentence was wrong twice over: it invents a
  > component, and its "without driving it" framing is the exact inversion F-322 exists to kill.
  > This entry predates that determination, which is why it blessed the sentence.
  >
  > **Fixed, and used as the teaching moment rather than deleted** — the reader is standing in front
  > of a floating pin, which is the best possible moment to learn this: *"…if you are reaching for the
  > pull-up resistor you would have switched on somewhere else — there isn't one. The P2 has no bias
  > resistors at all. What it has instead is a choice of *how hard to drive*: the same `drvh`, but
  > through 15 kΩ rather than through a fast transistor, if you ask for it (Chapter 14)… a weak drive
  > is still a drive, so `dir` stays high either way."* Chapter 14 verified as the manual's smart-pin
  > /`WRPIN` chapter (`:4614`). The wording is aligned to the KB's `weak_high` idiom
  > (`pin-drive-configuration.yaml:203-222`) rather than inventing a third form.
  >
  > **Cross-checked and deliberately left alone:** `COMPLETE-OPUS-MASTER.md:2881` ("Common I/O
  > Gotchas" #2) already says *"**No pullup/pulldown by default** — Use external resistors or
  > configure smart pin modes"*, which is **correct**. The two sites disagreed with each other; now
  > they do not.
  >
  > **Owed to «#302»/release:** page-level confirmation of the reflowed `::: sidetrack` in Ch.1, then
  > release. The eval-board citation this entry recommends is re-verified live at
  > `hardware/p2-eval-board.yaml:109-111` (`type: "Buffered LED bank"`, `pins: "P56-P63 (one LED per
  > pin)"`) and `:124` (P58–P63 shared with USB data and P2 memory signals) — note both moved from
  > the `:27`/`:29`/`:31-34` this entry recorded.

  Status: `PARTIAL — mechanism fixed 2026-08-17; the pull-up sentence this entry called "right" was wrong and is fixed 2026-08-25 («#301»); render + release owed`.

- **F-252 — the Getting Started guide hardcodes `LED = 56` with no board caveat (same class
  as the DeSilva fix).** — `PARTIAL` · `p2-getting-started-guide/opus-master/getting-started-body.md:558`
  declares `LED = 56  ' the pin our LED is on`, used by the blink examples at `:493` and
  `:408`. On a **P2 Edge 32MB PSRAM Module** P56 is the PSRAM **clock** — the example lights
  nothing and drives the memory bus; the LEDs there are **P38/P39**. This is exactly the
  failure a reader hit this session, and it lands in the guide most likely to be a
  newcomer's *first* P2 program. **Fix:** one line naming the per-board LED pins (the
  DeSilva Ch.1 aside is the model, but Getting Started wants a single sentence, not a
  sidetrack). Sources now in the KB: `hardware/edge-standard-module.yaml` (P56/P57),
  `hardware/edge-32mb-module.yaml` (P38/P39), `hardware/p2-eval-board.yaml` (P56-P63,
  P56/P57 free). **→ manual head.** Surfaced by the v1.16.2 YAML→Manual impact survey.

  > **TWO OF THE THREE NAMED SOURCES MOVED 2026-08-24 («#294» uncited-block purge). The fact
  > survives; the addresses changed.** Verified line by line against the post-purge files:
  > - `hardware/edge-32mb-module.yaml` (P38/P39) — **gone from this file entirely.** The purge
  >   removed its `pin_mapping` block (which held `led_buffered: 2  # P38-P39` and the P38/P39
  >   pin entries) and its `boot_modes` block (which held the `LED:` DIP-switch line naming
  >   P38/P39). `P38`/`P39` now match **nothing** in that file.
  > - `hardware/edge-standard-module.yaml` (P56/P57) — **survives, at a new address.** Its own
  >   `pin_mapping` went too, but the `comparison_with_32mb` block was not flagged and stands:
  >   `:158` `led_pins: "P56, P57"` and `:164` `led_pins: "P38, P39"`. That single surviving
  >   block now carries **both** boards' LED pins, so it alone can source the whole caveat.
  > - `hardware/p2-eval-board.yaml` (P56-P63, P56/P57 free) — **survives untouched** at `:28`
  >   (`pins: "P56-P63 (one LED per pin)"`) and `:31-34`, inside the cited
  >   `built_in_peripherals` block.
  >
  > **The manual fix is not blocked** — every pin number the caveat needs is still in the KB.
  > Cite `edge-standard-module.yaml:158,164` for the Edge pair and `p2-eval-board.yaml:28` for
  > the eval board. When «#307» repopulates `edge-32mb-module.yaml`, P38/P39 must come back
  > there source-first; until it does, do not cite that file for this fact.

  > **APPLIED 2026-08-25 («#301») — and the "do not cite that file" warning above is now STALE, which
  > is why every locator was re-verified on disk before use rather than copied from this entry.**
  >
  > **`edge-32mb-module.yaml` has been repopulated.** The 2026-08-24 annotation says P38/P39 *"match
  > **nothing** in that file"*. Today they match plenty, source-first as required: `:140-141`
  > (`P38: "Buffered LED"`, `P39: "Buffered LED"`), `:165` (`pins: "P38, P39"`), `:201` (the `LED`
  > DIP switch), all under a real `source:` at `:175` naming *P2-EC32MB Edge Module Rev B Guide v2.0,
  > §7 LED Buffer and §8 LEDs P38 and P39*. So the per-board file **is** citable again and was cited.
  > The other two locators also moved: `edge-standard-module.yaml:145` (`pins: "P56, P57"`, now with
  > its own `warning:` at `:146-148` — *"DIFFERENT PINS from the P2-EC32MB module… Confusing the two
  > puts an LED write on a PSRAM data line"*) and `p2-eval-board.yaml:110`
  > (`pins: "P56-P63 (one LED per pin)"`).
  >
  > **The PSRAM claim was verified, not assumed:** `edge-32mb-module.yaml:137` reads
  > `"P56": "PSRAM CLK (Common)"`. So `LED = 56` on that board really does drive a memory clock line.
  >
  > **Fix, in the shape this finding specified** — one bullet, not a sidetrack — added to the bullet
  > list under the first runnable program in `getting-started-body.md`: *"**One board check before you
  > run it.** `56` is the LED pin on a P2 Eval Board and on the standard P2 Edge Module, but the **P2
  > Edge 32MB Module** puts its two LEDs on **P38 and P39** — and P56 there is a PSRAM clock line, so
  > as written this program would light nothing and write to the memory bus instead. Change `LED` to
  > match your board."*
  >
  > **The code block was deliberately NOT touched.** It is captioned `ch03-blink-led.spin2`, so it is
  > byte-identity-paired to an example file; changing `LED = 56` there would have broken that pairing
  > and made the guide's first program board-specific in a different direction. The caveat is prose
  > beside the listing, which is what this finding asked for. `sync-manual-examples.py --check`
  > reports **no** "BODY differs" for the guide, so the pairing is intact. The other `LED = 56` sites
  > (`:339` skeleton, `:644`, `:704`, and `LED_A = 56` at `:603`) are left alone on purpose: the
  > caveat belongs once, at the first program a newcomer actually runs.
  >
  > **Owed to «#302»/release:** confirm the added bullet sets on the page, then release.

  Status: `PARTIAL — caveat added to opus-master 2026-08-25 («#301»); render + release owed`.

---

## Forum docs-feedback (2026-08-16) — the DDS LUT is not fixed at 512 entries — F-302

**Origin:** Christof Eb., Parallax forum 2026-08-16, reviewing the *P2 Streamer Programming
Guide* §17.2. Raw post + full analysis at
`engineering/document-production/FORUM-NO-COMMMIT/Docs-findings-260819/` (gitignored — find it
by path). Same reviewer as F-256. His parenthetical *"(No, it does not need to be 512
entries.)"* is **correct**, and it lands on the KB as well as the manual.

### F-302 — `p2kbArchDdsGoertzel` states the DDS/Goertzel LUT window as a flat `entries: 512`, hiding a selectable 8-way loop size, a bounded-region offset, and a phase-offset field. `RESOLVED 2026-08-22 — KB applied 2026-08-21; the manual half shipped in Streamer Guide v1.1.0`

> **MANUAL HALF SHIPPED 2026-08-22, Streamer Guide v1.1.0 (91pp).** §10.3 "LUT Window" is
> a new section carrying all eight loop sizes with the `%A` region bits and the `%T` phase
> offset, and §17.2 was rebuilt on top of it — the flat "must contain 512 entries" claim is
> gone from the manual as it is from the KB.

> **KB APPLIED 2026-08-21.** All six sites. `entries: 512` is now `entries_default` plus an
> `entries_note` saying it is the %000 case, beside a `lut_window:` block carrying all eight
> loop sizes with their NCO index bits and LUT ranges, and named `capabilities` for the two
> things the %A and %T bits actually buy — bounded sub-regions and phase offset/modulation.
> `s_operand.field_11_0` is split into `field_11_9` (loop-size selector) and `field_8_0` (%A/%T),
> quoting Silicon Doc :4093-4095 verbatim. `operation.steps.1` no longer states NCO[30:22] as a
> general rule. The two `repeat i from 0 to 511` loops are correct FOR the %000 case and now say
> so rather than reading as the only option. **The table and the quote were re-read out of
> `p2-documentation.txt:4058-4095` before being written, not copied from this register.**

**Location:** the DDS/Goertzel architecture YAML behind P2KB key `p2kbArchDdsGoertzel` —
`lut_setup.entries: 512` and `s_operand.field_11_0: "loop size + LUT window"`.

**What is wrong.** `entries: 512` reads as a hardware requirement; it is only the `%000` case.
`field_11_0` names the field but carries none of its content, so nothing downstream can use it.
The KB is *not false* here in the way the manual is (the manual says "**must** contain 512
entries"), but it is thin in exactly the place the manual went wrong, and it is what a
downstream author would consult.

**Evidence — Silicon Doc `sources/silicon-doc/p2-documentation.txt:4062-4092`, verbatim table:**

| `S[11:0]` | Loop Size | NCO Bits | LUT Range |
|---|---|---|---|
| `%000_TTTTTTTTT` | 512 | 30..22 | `%000000000..%111111111` |
| `%001_ATTTTTTTT` | 256 | 30..23 | `%A00000000..%A11111111` |
| `%010_AATTTTTTT` | 128 | 30..24 | `%AA0000000..%AA1111111` |
| `%011_AAATTTTTT` | 64 | 30..25 | `%AAA000000..%AAA111111` |
| `%100_AAAATTTTT` | 32 | 30..26 | `%AAAA00000..%AAAA11111` |
| `%101_AAAAATTTT` | 16 | 30..27 | `%AAAAA0000..%AAAAA1111` |
| `%110_AAAAAATTT` | 8 | 30..28 | `%AAAAAA000..%AAAAAA111` |
| `%111_AAAAAAATT` | 4 | 30..29 | `%AAAAAAA00..%AAAAAAA11` |

and (`:4093-4095`, verbatim): *"On each clock, the lookup RAM is read at the 9-bit location
bound by the %A bits, with the lower bits being the sum of the %T bits and the topmost NCO
bits. This allows you to set bounded areas within the LUT and to shift or modulate the phase of
playback."*

**Proposed correction.** Replace `lut_setup.entries: 512` with a `lut_window:` block carrying
the eight loop sizes and their NCO index bits; expand `s_operand.field_11_0` into the three
sub-fields — loop-size selector `S[11:9]`, `%A` region-bound bits, `%T` phase-offset bits — and
state the two capabilities the Silicon Doc names explicitly: **bounded LUT sub-regions** (more
than one waveform resident at once) and **phase offset / modulation**. Keep `entries: 512` only
as the `%000` default, labelled as such.

**Why it matters beyond the correction.** The guide's §17.2 headline applications are
"Function generator, audio synthesis, **RF modulation**" — and the field that does modulation is
the one neither the KB nor the manual documents.

**Additional YAML sites found by the 2026-08-20 class-wide sweep — these are part of F-302, not
separate findings.** The correction above named `lut_setup.entries` and `s_operand.field_11_0`
only; the sweep found the same assumption stated four more times in the same file:

| `architecture/streamer/dds-goertzel.yaml` | What is wrong |
|---|---|
| `:57` | `operation.steps` step 1 — `"Read LUT entry at NCO[30:22]"` as an **unconditioned general rule**. This is the KB twin of the manual's §10.2 defect and was **missing from this finding's original correction text.** |
| `:89` | `' Build 512-entry sine/cosine table` (code example) |
| `:100` | `repeat i from 0 to 511` in the `sinc2_amplitude` example |
| `:227` | `usage_pattern.data` comment restating `512-entry LUT window` as fact |

Sibling files verified **correct** and usable as the fix template: `dds-goertzel.yaml:11,:18`
(`%1111_0ppp_p111` / `%1111_1ppp_p111`, with the correct `D[22:19]` multiple-of-four caveat).

**Downstream (manual head, not a YAML edit):** *Streamer Guide* §10.2 `:648`
(`LUT[NCO[30:22]]` stated as the general rule), §10.3 `:674` ("must contain 512 entries" —
**false**), §17.2 tip `:1458` ("the 512 entries"), the `:1424` code comment ("512-entry LUT
window"), and the `\DiagDdsGoertzel` diagram in
`workspace/p2-streamer-programming-guide/templates/p2kb-streamer-diagrams.sty` (which renders
`entry = LUT[NCO[30:22]]`) — plus its **cloned copies** at
`workspace/p2-layout-torture-test/templates/p2kb-torture-diagrams.sty:207` and the staged
`pdf-forge/interactive-testing/templates/p2kb-torture-diagrams.sty:207`. Tracked in
`engineering/planning/STREAMER-GUIDE-CORRECTNESS-SPRINT-PLAN.md`; fix ships with that release.

---

## Class-wide sweep of the Streamer findings — the same errors live in OTHER artifacts (2026-08-20) — F-303…F-309

**Origin.** The Streamer Guide's 2026-08-19 class audit produced four confirmed factual errors.
Sweeping them across every manual, app note, `deliverables/ai/P2/`, and workspace diagram template
found them **outside** that manual as well. Recorded here — **not** scoped into the Streamer
sprint, which is deliberately confined to its own document. **Stephen decides at that sprint's
release gate whether the affected artifacts co-release.** Full sweep detail + the verified-correct
list: `engineering/planning/STREAMER-GUIDE-CORRECTNESS-SPRINT-PLAN.md` §13.

> **Before fixing any of these, read the "verified correct" list in that plan section.** The sweep
> deliberately separated look-alikes: the Assembly Manual's Appendix G **ADC Sampling Modes** and
> **DDS/Goertzel** *constant-value* tables were decoded row by row and are **correct** — they are
> named-symbol value tables, not field-encoding templates. Do not "fix" them.

### F-303 — the RGBI8 `2:2:2:2` fabrication is in a second released manual and in two live KB files. `RESOLVED 2026-08-22 — every released and live-KB site corrected; KB 2026-08-21, Assembly v3.1.7`

> **CLOSED 2026-08-23.** Both live-KB sites applied 2026-08-21 (`2:2:2:2` re-swept 2026-08-23:
> **zero** occurrences in `deliverables/ai/P2/`), and the Assembly Language Reference's site
> shipped in v3.1.7 and was read on p475 of the returned PDF. **The fourth row of the table below
> is NOT a correctness finding and never gated this one**: the P2 Layout Torture Test is an
> internal test instrument, never released and not consistency-bound (roster: *"serves the manual
> layout-standards effort, not the community"*). Its stale `\DiagRgbFormats` clone is recorded as
> instrument-local housekeeping in `PUNCH-LIST.md`, not as pending correction work — an instrument
> must never hold a published-artifact finding open.

> **VALIDATED on the returned v3.1.7 PDF, 2026-08-22 (505pp, read on the page).** p475 prints *"Read byte as color + intensity: P[7:5] selects the color, P[4:0] is the intensity"*, and `2:2:2:2` appears **zero** times in 505 pages. The LUMA8 row beside it now reads *"the color is selected by S[2:0]"*.


> **Assembly fixed 2026-08-22 (v3.1.7).** `appendix-g-streamer-constants.md:115` now reads *"Read byte as color + intensity: P[7:5] selects the color, P[4:0] is the intensity"*, with a paragraph above the table contrasting RGBI8 against LUMA8. Sourced live from Silicon Doc `p2-documentation.txt:3800`, which also shows the colour table has **eight** entries — so the old row was wrong on the colour count as well as the field split.

> **KB APPLIED 2026-08-21.** `streamer-symbols.yaml:186` and `modes-reference.yaml:221` both now
> read *"upper 3 bits select a colour, lower 5 bits are intensity"*, the framing the released
> Debug Window Manual v1.1.3 already uses. Swept: `2:2:2:2` no longer appears anywhere in
> `deliverables/ai/P2/`. *(Still-owed list as written on 2026-08-21, both since discharged:
> `appendix-g-streamer-constants.md:115` shipped in Assembly v3.1.7, and the torture-test clone
> is instrument-local — see the CLOSED note above.)*

The truth (Silicon Doc `p2-documentation.txt:3800`): RGBI8 is a **3-bit colour select + 5-bit
luminance** format, structurally the same as LUMA8. It has no per-channel R/G/B fields.

| Location | Status |
|---|---|
| `manuals/p2-assembly-language-manual/opus-master/part-iii/appendix-g-streamer-constants.md:115` — *"Read byte as RGBI 2:2:2:2 (16 colors + intensity)"* | **RELEASED** — Assembly Language Reference v3.1.6, 2026-08-18, 502pp |
| `deliverables/ai/P2/language/spin2/symbols/streamer-symbols.yaml:186` — `"RFBYTE → RGBI 2:2:2:2"` | **LIVE KB** (served by `p2kb-mcp`); the one wrong row in an otherwise-correct table |
| `deliverables/ai/P2/architecture/streamer/modes-reference.yaml:221` — same description, second copy | **LIVE KB** |
| `workspace/p2-layout-torture-test/templates/p2kb-torture-diagrams.sty:176` — `\DiagRgbFormats` cloned, draws `R 2 \| G 2 \| B 2 \| I 2` | **NOT A FINDING SITE** — internal test instrument, never released. Housekeeping only; tracked in `PUNCH-LIST.md` |

**Fix template already exists, in a released manual:** *P2 Debug Window Manual* v1.1.3
`ch04-bitmap.md:100` — *"Upper 3 bits select a color, lower 5 bits are intensity"* — and it
contrasts RGBI8 against LUMA8 immediately above. Copy that framing.

### F-305 — the Assembly Manual teaches a streamer DAC example without the pin-setup step. `RESOLVED 2026-08-22 (v3.1.7)`

> **VALIDATED on the returned v3.1.7 PDF, 2026-08-22 (505pp, read on the page).** The Audio DAC example on p480 carries `COGID` / `SETNIB` / `WRPIN` / `DIRH`, and its routing reads `X_DACS_X_X_X_0` — one channel for a one-channel mode.


> **Fixed 2026-08-22 (v3.1.7).** The "Audio DAC Output" example now carries the full `cogid` / `setnib` / `wrpin` / `dirh` sequence per F-272, and the example compiles under `pnut-ts` v1.55.3.
>
> **A second defect in the same example, not in the original enumeration:** the mode was `X_RFBYTE_1P_1DAC1` — one DAC channel — routed with `X_DACS_3_2_1_0`, which the appendix's own table defines as four channels. Now `X_DACS_X_X_X_0`. Fixing the pin setup alone would have shipped a half-corrected example.

`manuals/p2-assembly-language-manual/opus-master/part-iii/appendix-g-streamer-constants.md:237`
shows `mov mode, ##X_RFBYTE_1P_1DAC1 | X_DACS_3_2_1_0` with no `WRPIN` DAC-mode configuration and
no `DIRH` — the same omission the Streamer sprint fixes book-wide. **RELEASED** in Assembly
Language Reference v3.1.6.

Per **F-272** (resolved 2026-08-20) the correct setup is now fully citable: `%TT = %01`
(`P_CHANNEL`) with the COGID in `M[3:0]`, `DIRH` the pin, channel selected by the pin's two low
bits. `deliverables/ai/P2/architecture/streamer/dds-goertzel.yaml:203` carries a worked example,
and `wrpin.yaml:54` documents the field.

**Note the asymmetry that makes this easy to get wrong** — and note the half of it that was itself
wrong until 2026-08-20. The **`WRPIN`** part applies to **DAC** output only: ordinary digital pin
output via `X_PINS_ON` (`D[23]=1`) needs no DAC mode, no COGID and no channel, so do not add *mode*
setup to digital-output examples. But it **does** need `DIRH` like any driven pin — `X_PINS_ON`
enables the streamer's contribution to the pin's output *state*, never its output *enable*. See
**F-308** / **EF-062** (bench-proven: DIR low 4-of-8, `DIRH` 8-of-8). The citation this note used to
carry, `Silicon Doc :3602-3603`, resolves to nothing in `engineering/ingestion/` and has been dropped.

### F-308 — "digital pin output through `X_PINS_ON` requires no `DIRH`" is wrong: the streamer feeds the pin's output STATE, and DIR is still the output ENABLE. `RESOLVED 2026-08-22 — Streamer bench-sealed (EF-062), Assembly shipped in v3.1.7`

> **VALIDATED on the returned v3.1.7 PDF, 2026-08-22 (505pp, read on the page).** `DIRH` appears **8 times** across Appendix G (pp.471-482): all four usage examples, the `HARDWARE` callout carrying the EF-062 numbers, and the control-flag prose. The no-`WRPIN` half survives intact.


> **Assembly fixed 2026-08-22 (v3.1.7).** All three example sites now `DIRH` their pins, and a `::: hardware` callout under the control-flag table states the state-vs-enable distinction with the EF-062 numbers. The **no-`WRPIN`** half is preserved.
>
> **Two sites the enumeration missed**, both glossing `X_PINS_ON` as *"Enable pin outputs"* — `appendix-g-streamer-constants.md:203` and `part-i/chapter-05-hardware.md:347`. Source-faithful to the Silicon Doc's encoding wording, and the exact phrasing that installs the wrong model in a reader; both now say the streamer drives the pin's output *state*.

**How it surfaced.** Two bench runs of the VO-J-003 rig (2026-08-20, logs in that rig's `logs/`).
Its digital self-test drove `DAC_PIN` through `X_PINS_ON` with DIR left low — on the strength of the
claim below — and scored **4 of 8** then **3 of 8** toggles, i.e. the pin was never driven and the
readback was float noise. Going to the primary source to explain it produced this finding.

**Locations (both live):**
- `engineering/document-production/manuals/p2-streamer-programming-guide/opus-master/streamer-body.md:834`
  — a `::: hardware` callout in §11.0: *"Ordinary pin output through `X_PINS_ON` drives the pin bus
  directly and requires no `WRPIN` and no `DIRH`."* **RELEASED in Streamer Guide v1.0.9**; v1.1.0 is
  in its correctness sprint now.
- `engineering/operations/P2KB-CORRECTION-FINDINGS.md:251` — F-305's closing note repeats the claim
  as guidance ("Do not add pin setup to digital-output examples") and cites `Silicon Doc :3602-3603`.
  **That citation does not resolve** to any extraction in `engineering/ingestion/`.

**What the primary source actually says.** *Parallax Propeller 2 Documentation v35 (Rev B/C
Silicon)*, text extracted from the shipped `.docx`:
- STREAMER section: *"Modes which can output to pins OR the streamer pin-output bus **with {OUTB,
  OUTA}** to produce the final 64 pin **output states** on each clock for the cog. For these modes,
  %e in D[23] must be '1' to enable pin output."*
- SMART PINS section: *"Normally, an I/O pin's **output enable is controlled by its DIR bit** and its
  **output state is controlled by its OUT bit**, while the IN bit returns the pin's read state."*

The streamer's pin data is OR'd into the **output state** — the OUT side. Nothing in the document
gives the streamer any authority over the output **enable**. The one documented way to drive a pin
with DIR low is the smart-pin `%TT` field (*"the %TT bits … will govern the pin's output enable,
regardless of the DIR state"*), and `X_PINS_ON` digital output uses no smart pin. So `DIRH` **is**
required, and D[23] enables the streamer's contribution to OUT, not the pin's driver.

**The "no `WRPIN`" half is correct** and should survive the fix — no smart-pin mode is needed. Only
the "no `DIRH`" half is wrong. Note the internal tension the claim already had:
`streamer-body.md:796`, twenty-eight lines earlier in the same section, states the general rule
correctly — *"**`DIRH`** on the pin. Until DIR is high, the pin does not drive."*

**Proposed correction.** Rewrite the §11.0 callout so it separates the two: digital output needs no
`WRPIN` (no DAC mode, no COGID, no channel), but it does need `DIRH` like any driven pin. Fix
F-305's note in the same pass and drop or replace its unresolvable citation.

**SEALED ON SILICON 2026-08-20 → EF-062.** VO-J-003's run 3 ran the A/B: the same streamer command
with DIR low and then `DIRH`, the `DIRH` leg starting from `OUT`=0 so a pass proves the streamer
overrode `OUT`. *Result:* `D1` plain drive (no streamer) **8 of 8** · `D2` DIR low **4 of 8** · `D3`
`DIRH` **8 of 8**. The prediction and its falsifying outcome ("if `D2` passes, reverse F-308") were
written into the program before the run; the bench was free to reverse this and did not.

**The class — the book is inconsistent with itself, and the majority of it is already right.**

*Correct, do not touch:* `streamer-body.md:796` ("Until DIR is high, the pin does not drive") ·
`:1490` the §15.2 HDMI program, which does `drvl #7<<6 + HDMI_BASE` · `:2038` the troubleshooting
checklist, "Pins configured as outputs (DRVH/DRVL as needed)" · `:623`, `:816`, `:1767` (ADC, DAC,
DDS pin enables).

*Wrong prose — **FIXED 2026-08-20**:* `:834` the §11.0 callout (rewritten: keeps "no `WRPIN`",
adds what `DIRH` is for and what a DIR-low streamer command looks like on a bench) · `:410` §5.2's
"the pin columns need none".

*Code blocks that omitted the pin enable — **ALL FIXED 2026-08-20** («#289»):*
- `:405` `X_IMM_32X1_LUT` (32-pin) -> `drvl ##31<<6` · `:435` `X_IMM_4X8_1DAC8` (8-pin) ->
  `drvl #7<<6 + pin` · `:470` `X_RFLONG_4X8_LUT` (32-pin) -> `drvl ##31<<6 + base` ·
  `:497` `X_RFBYTE_8P_1DAC8` (8-pin) -> `drvl #7<<6 + base`. Span forms compiled before use.
- §16.1 SPI — the configuration block set up `spi_clk` and never touched `spi_do`, the pin the
  streamer drives. Fixed earlier the same day.
- **§15.1 VGA — rebuilt.** It carried **four** defects, not the one this finding named, and they
  were fixed in a single edit rather than four passes: (1) no §11.0 DAC-pin setup at all for the RGB
  channels; (2) `VGA_BASE` undefined; (3) `framebuffer` undefined; (4) **a 640×480 framebuffer at
  16 bpp is 600 KB and hub RAM holds 512 KB** — the program could not have existed as written. It
  now declares `VGA_BASE = 16` (a multiple of 4, so each pin's low two bits pick its own DAC
  channel), does the §11.0 setup (`COGID` into `M[3:0]`, `P_CHANNEL`, `DIRH`) across a 4-pin span,
  and paints 350 lines into a declared `orgh` framebuffer while blanking the rest of an unchanged
  525-line field — the same trade §15.2's HDMI program already makes for the same reason (§7.1).
  **Extracted from the manuscript and compiled: 452,096 bytes**, matching §15.2's block exactly.
  The compiler caught a collision the new `CON` introduced — P2 symbols are case-insensitive, so a
  `VSYNC_PIN` constant clashed with the `vsync_pin` register; the constant was dropped.

*Not touched, and correctly so:* the §7.3 RGB pattern block already carries a `**Pattern**` label
and points at §11.0 for its DAC pins.

**Why the sweep was routed rather than done at filing time.** It was folded into «#289» and run
alongside «#280», the pass that reads every code block, so that one hand added the missing line to
every block under one contract. Routing inside a sprint, not deferral across a release — none of it
ships until v1.1.0. The failure mode being avoided is the one «#282» records: "the finding named a
row, the fix corrected a row, nobody swept the table." Worth noting that the sweep *earned its keep* —
it found §15.1 carrying four defects where this finding had named one, and a fifth `pin<<17` site
(`:435`) that the original enumeration missed.

**Sprint impact.** This is sprint decision #4 ("Digital ≠ DAC. `X_PINS_ON` needs NO wrpin/dirh"),
which later tasks were told to respect. **That decision is now half wrong and must not be applied as
written.** Surfaces at the Streamer v1.1.0 co-release gate («#288») with F-302…F-307.

**Status:** `RESOLVED 2026-08-22 — BOTH halves complete and validated on their returned PDFs.` The
Assembly Language Reference's sites shipped in **v3.1.7** and were read on the page: `DIRH` appears
8 times across Appendix G (pp.471-482) — all four usage examples, the `HARDWARE` callout carrying
the EF-062 numbers, and the control-flag prose — while the no-`WRPIN` half survives intact. The
enumeration named three sites; two more carried the same wrong model as a gloss
(`appendix-g:203`, `part-i/chapter-05-hardware.md:347`) and were corrected in the same pass.
The v1.1.0 PDF was read at «#287»
2026-08-21 and the §11.0 callout renders as the corrected split — *"X_PINS_ON requires no WRPIN: no
DAC mode, no COGID, no channel… What digital output still needs is DIRH. X_PINS_ON enables the
streamer's contribution… Until DIR is high, the pin does not drive."* The no-`WRPIN` half survived,
the no-`DIRH` half is gone, exactly as EF-062 sealed it. Still owed:
`part-iii/appendix-g-streamer-constants.md:228/:255/:289`, RELEASED in v3.1.6.

---

## `object-image-dedup.yaml`'s map_caveat goes stale when pnut-ts 1.55.4 ships (2026-08-22) — F-320

### F-320 — `p2kbSpin2ObjectImageDedup`'s `map_caveat` warns readers off .map labels that 1.55.4 makes correct, while the limitation that SURVIVES the fix is documented nowhere. `CONFIRMED — HELD by decision (Stephen, 2026-08-22) until the new compiler and its fixture set are in hand`

**Origin.** `engineering/ingestion/external-inputs/p2kb-update-requests/P2KB-map-caveat-retraction-1.55.4.md`
— an upstream request from the pnut-ts side proposing an amendment. Treated as **input, not
authority** ([[feedback_upstream_input_docs_not_authority]]): its finding was checked here, its
proposed text was not adopted.

**The site.** `deliverables/ai/P2/language/spin2/concepts/object-image-dedup.yaml:123-126` — the only
copy. Four other files reference the entry (`method-pointers`, `object_archetypes`, `OBJ`,
`shared-bus-replication`) but none duplicate the caveat.

### Measured HERE on pnut-ts 1.55.3, 2026-08-22 — the "before" baseline

Rebuilt the entry's own `cascade_through_tiers` fixture and read it as `verification.method` says
to. **The label defect reproduces, and is worse than the request describes:**

```
  case4  (1 methods)
      +-- A : casc_mid
      |   \-- LEAF : object_3          <- placeholder name
      |       \-- child_0 : object_4   <- a tier that DOES NOT EXIST
      \-- B : casc_leaf                <- wrong SOURCE FILE (B is casc_mid)
```

B's real child is absent and an extra tier is invented. **Send upstream as a 1.55.4 regression
check** if their fixtures do not already cover the invented-tier and wrong-source-file shapes.

Two things confirmed independently of the fix, and they are why the entry is otherwise sound:

- **`Objects: 5`** — exactly the entry's measured value. The count IS reliable, as the caveat says.
- **`SYMBOL INDEX` carries ONE `MTAG` ($00034) and ONE `LTAG` ($00048)** while `MEMORY LAYOUT`
  shows two images of each source. The second image's DAT addresses appear nowhere in that section.
  This is **structural — symbols are stored per source file — so it is NOT version-coupled and
  survives the 1.55.4 fix.** It is documented in no punch list here despite the request saying it is
  tracked, so this entry is also that gap's only record.

### The proposed text is REJECTED — it reinstates the shape PL-004 just stripped from this file

The request asks for prose reading *"Fixed in pnut-ts 1.55.4. Through 1.55.3 the multi-instance .map
could show… As of 1.55.4…"*, and offers a `verification.method` line *"confirmed correct at pnut-ts
1.55.4"* as an alternative anchor. **Both are build stamps.**

`[[reference_kb_is_always_latest_no_version_citations]]` — *cite the EDITION, never the BUILD* — uses
**this exact file** as its worked example: it said *"re-verify on a compiler version bump"* pinned at
v1.55.0 while v1.55.3 was installed; the bump had happened and the re-verify had not. PL-004 removed
the `toolchain:` field for that reason, and `verification.method` now carries the durable
replacement: *"Compiler-coupled behaviour: re-measure rather than assume if a result surprises you."*

The request understood half of it — it dropped its own `toolchain:` proposal as moot — then moved the
build numbers into prose. Same rot, different field.

### Amendment to apply (current-state only, nothing to maintain at the next bump)

```yaml
  map_caveat: |
    SYMBOL INDEX reports one row per SOURCE FILE, so when an override forks a file into
    several images only the first image's DAT address appears there. For per-instance DAT
    addresses read MEMORY LAYOUT or ADDRESS INDEX, which list every image. The Objects:
    count is reliable.
```

Nothing else in the entry needs changing: `description`, THE RULE, `singleton_rule`,
`forking_a_dat_region`, `the_silent_trap`, `the_other_silent_trap`, `cascade_through_tiers`,
`completeness_rule` and `verification.measured` all re-read clean against the request's own
re-measurement.

### Why it is HELD, and what releases it

**Sequencing is the whole reason.** On 1.55.3 the labels genuinely ARE wrong — measured above — so
dropping the warning while readers are still on 1.55.3 publishes guidance that is wrong for them.
The amendment is only correct once 1.55.4 is what people have.

Release conditions, both required:

1. **pnut-ts 1.55.4 is in this devcontainer**, so the fix can be verified here rather than taken on
   the request's word. The container is on 1.55.3 (`Build date: 8/9/2026`) as of filing.
2. **The compiler side's test source set is in hand** — offered 2026-08-22 and expected to evidence
   the new map details directly, so the fixtures do not have to be reconstructed from the entry's
   prose. Re-run the "before" shapes above against it; every one should invert.

Then: apply the amendment, and record the result in `verification.measured` **without a build
number**.

> ### GAP RECORDED 2026-08-25 («#300») — the HELD decision stands, and both release conditions were MEASURED
>
> This finding was on «#300»'s roster and **closes this sprint as a recorded gap, not as work**. Stephen's
> 2026-08-22 decision to hold it was **not re-opened, not re-argued, and the amendment was not applied.**
> The only thing done here was to check — rather than assume — whether the two release conditions this entry
> names have since been met. **Both are still unmet:**
>
> 1. **pnut-ts 1.55.4 is NOT in this devcontainer.** `pnut-ts --version` → **`PNut-TS: v1.55.3`**. The
>    compiler that makes the amended text true is still not the one installed, so publishing the amendment
>    now would hand 1.55.3 readers guidance that is wrong *for them* — the exact sequencing risk this entry
>    was held on.
> 2. **The compiler side's test source set is NOT in hand.**
>    `engineering/ingestion/external-inputs/p2kb-update-requests/` contains only the originating request,
>    `P2KB-map-caveat-retraction-1.55.4.md`. No fixture set accompanied it.
>
> **What would settle it:** both conditions together — 1.55.4 installed here, plus the fixtures — after which
> the entry's own "before" shapes (placeholder name, invented tier, wrong source file) are re-run and every
> one should invert. **Until then this is a gap, and the KB text stays as it is.**
>
> **The half that is NOT version-coupled remains this entry's only record**, and is unaffected by the hold:
> `SYMBOL INDEX` stores symbols **per source file**, so a forked file's second image has no row there. That
> survives 1.55.4 and is documented nowhere else.

## The rights guard fails open, so an unadopted document emits a malformed rights string (2026-08-22) — F-319

### F-319 — `p2kb-platform-foundation.sty`'s pdfkeywords guard does not fire for a document whose `\Doc*` macros are at their defaults, so it emits `"; licensed under "` instead of nothing. `CONFIRMED — carved out of v3.1.7 deliberately; see "Why not fixed here"`

**How it surfaced.** The Assembly Language Reference v3.1.7 render (2026-08-22) came back with
`Keywords: "; licensed under "` — the both-values-present branch, with both values empty.

**Proven from the artifact, not inferred.** That exact string is what
`\hypersetup{pdfkeywords={\DocCopyright; licensed under \DocLicense}}` produces when both macros
expand to nothing. For it to be emitted at all, **both** `\ifx` tests must have taken their
not-empty path — so the guard did not fire.

**The guard (`:332-350`) and the defaults (`:288-299`):**

```latex
\providecommand{\DocCopyright}{}       % and \DocLicense, \DocTitle, ...
...
\ifx\DocCopyright\@empty ... \else ... \fi
```

The comment above it claims *"a document that has not adopted these keys writes no pdfkeywords at
all, exactly as before, so an unconverted document is unchanged rather than given a malformed
rights string."* **The artifact falsifies that claim.**

**Hypothesis for the mechanism — NOT proven, no TeX engine in this container.** `\providecommand`
routes through `\newcommand`, which defines a `\long` macro; `\@empty` is `\def\@empty{}` and is
not `\long`. `\ifx` compares the prefix as well as the body, so `\long macro:->` never tests equal
to `macro:->`. Plausible and consistent with the evidence, but **verify before relying on it**
(`EXEC_ENV_CANONICAL` has the engine).

**Proposed fix — correct under EITHER explanation**, because it normalises by full expansion rather
than depending on how the default was declared:

```latex
\AtBeginDocument{%
  \edef\P@rc{\DocCopyright}\edef\P@rl{\DocLicense}%
  \ifx\P@rc\@empty ... \fi
}
```

**Blast radius.** Every document that loads the platform foundation and has **not** wired the seven
`\renewcommand{\Doc*}` lines into its own `*-reference.latex`. Per
`PLATFORM-FEATURE-ADOPTION.md` that is every row except Streamer, Single-Step Debugger and now
Assembly — so **~14 documents**, each at its next render. Assembly is simply the first unadopted
document to render since the foundation gained this code, which is why it had not shown before.

**Why not fixed in v3.1.7 (explicit carve-out).** Assembly's own template is now wired, so its
rights emit correctly and this release ships clean — the defect is genuinely separable and is not
holding the quality bar for this document. Fixing it means editing a **shared** file that all 18
documents load, using an idiom that **cannot be tested in this container** (no TeX engine), while a
manual is mid-render. Landing it blind risks breaking rights emission for Streamer and the
Single-Step Debugger, which are proven working today.

**A LIVE VICTIM, found 2026-08-22 — and FIXED the same day, before it rendered.**
`pnut-term-ts-user-guide` was about to render for its v1.0.0 release with five of the seven `\Doc*`
macros bound and neither rights macro, and no `copyright`/`license` in its `request.json` either —
so it would have emitted the malformed `"; licensed under "` exactly as Assembly's first v3.1.7
render did. Both halves are now wired (template 7/7; `request.json` carrying
`"Copyright 2026 Iron Sheep Productions, LLC"` + `"CC BY-SA 4.0"`, the one ISP-alone document in
the set). Detail in `PLATFORM-FEATURE-ADOPTION.md` footnote ¹².

**The mechanism hypothesis above is now believed CONFIRMED by reading, though still not executed.**
`\providecommand` routes through `\newcommand`, which defines a **`\long`** macro; `\@empty` is
`\def\@empty{}` and is not `\long`. `\ifx` compares that prefix as part of the meaning, so
`\ifx\DocCopyright\@empty` can never be true for a macro declared this way — the guard takes the
both-present branch **every** time, for **every** unadopted document. That is consistent with the
only artifact evidence in hand (Assembly's `"; licensed under "`). Still unexecuted: no TeX engine
in this container. `EXEC_ENV_CANONICAL` has one.

**Consequence of fixing the victim:** the pool of available negative controls shrank again. Neither
Assembly nor PNut-Term-TS can serve — an adopted document never takes the guarded branch, so it
proves nothing. The **Layout Torture Test** is now the only candidate named for this purpose. A fix
to the shared guard must be validated by rendering an *unadopted* document and confirming the
returned PDF carries **no** Keywords at all.

**What it needs instead — and this is the point:** its own change, with a **negative control** that
Assembly can no longer provide. Render an *unadopted* document (the layout torture test is the
natural candidate) and confirm the returned PDF carries **no** Keywords at all. A fix validated only
against an adopted document proves nothing, because an adopted document never takes the guarded
branch. (`a gate must read the artifact`; `prove with a negative control`.)

## Appendix G's mode tables misdecode the naming convention the same appendix documents (2026-08-22) — F-318

### F-318 — 31 of 36 streamer mode-table rows state a wrong pin count, a wrong DAC-channel count, or both, and every usage example in the appendix cannot run as printed. `RESOLVED 2026-08-22 (v3.1.7)`

> **VALIDATED on the returned v3.1.7 PDF, 2026-08-22 (505pp, read on the page).** Appendix G grew 9pp -> 12pp (pp.471-482) and **that +3 is the manual's ENTIRE page delta** — no other section moved. The decode rule now opens the appendix; all 36 rows read correctly; the four rebuilt examples print with `SETXFRQ`, an OR-ed `D[15:0]` count and `DIRH`. `SETLUTS`-for-streamer-LUT and *"Appendix F (Streamer Mode Constants)"* both appear **zero** times. Column separation measured: tightest constant->value gap **+14.1pt**, so the v3.1.5 overlap class is absent.


**How it surfaced.** Fixing F-303's single row in `appendix-g-streamer-constants.md` and then re-deriving the
rest of the table from the artifact instead of trusting the enumeration. **The register named one wrong row in
that file; thirty-one more were wrong.** Fourteenth instance of the class — see the F-304 note.

**The rule (Silicon Doc `part2-pixel-ops.txt:139-227`).** Every streamer mode is listed as `<n>-pin + <k>-DAC<b>`
— *n pins, k DAC channels, b bits per channel* — under column headers reading literally `Pins | DAC Channels`.
Appendix G's own "Mode Naming Convention" stated the same rule: *"`_nP` Number of pins used · `_nDACn` Number of
DAC channels, bits per channel."*

**The defect.** Every description read `kDACb` as *"k pins, b DAC channels"* — the channel count taken for a pin
count, the bit width taken for a channel count. Where the name carried an explicit `nP`, the description
**ignored it**. `X_RFBYTE_8P_2DAC4` — 8 pins, 2 channels at 4 bits — printed as *"2 pins, 4 DAC channels"*.

| Table | Rows | Wrong |
|---|:--:|:--:|
| Immediate to Pins/DACs | 12 | 11 |
| RDFAST Byte Operations | 9 | 8 |
| RDFAST Word/Long | 3 | 2 |
| WRFAST Operations (capture) | 12 | 10 |
| **Total** | **36** | **31** |

**The `Value` column was correct throughout** — every encoding checks out against the Silicon Doc. The bits were
right and the prose describing them was wrong, which is why nothing downstream caught it.

**Root cause is layout, and the fix addresses it.** The naming convention sat **180 lines below** the tables that
needed it, so whoever wrote the descriptions did not have the decode rule in view. It now **opens** the appendix,
names `_kDACb` as the field that gets misread, and works three same-pin-count examples (`8P_1DAC8` / `8P_2DAC4` /
`8P_4DAC2`) that can only be told apart by decoding it correctly.

**Found in the same pass, same file:**

- **`X_RFBYTE_LUMA8` was described as grayscale.** Silicon Doc `part2-more-content.txt:48`: *"LUMA8 mode uses
  three bits in S[2:0] as colors and the 8-bit pixels as luminance values."* The colour comes from the `XINIT`
  **S operand**. FABRICATED, and the exact mirror of F-303: LUMA8 takes its colour from S, RGBI8 from the pixel.
- **All four Usage Examples could not run as printed.** Each put a frequency in `XINIT`'s `S` operand — which is
  mode-specific data, not the rate (`SETXFRQ` owns that) — and none set `D[15:0]`, so the transfer count was
  zero and the streamer stops immediately. All four rebuilt and compiled under `pnut-ts` v1.55.3.
- **`SETLUTS #0` was captioned *"Use LUT for color palette"*.** `SETLUTS` enables LUT **sharing between adjacent
  cog pairs** and has nothing to do with streamer LUT lookup; `#0` is its *disable* value (Silicon Doc `:995-1000`).
  A fabricated claim attached to a real instruction. Removed — the streamer LUT modes need no enabling
  instruction, only the palette present in lookup RAM.
- **The ADC sampling modes never named their prerequisites** — `SETSCP` to point the SCOPE pipe at a four-pin
  block, and an ADC smart pin mode on each sampled pin (Silicon Doc `:3968-3977`). Same missing-setup class as F-305.
- **`D[22:20]` (pin group, 8-pin increments, "in every mode" — `:3606`) and `D[15:0]` (transfer count) were
  documented nowhere**, though every constant leaves both at zero.
- **`X_PINS_ON` and `X_WRITE_ON` print the same value** and were presented as two unrelated flags. They are one
  bit, `D[23]`, read by the mode's direction (`%e` / `%w`, `:3602-3604`).
- **Chapter 5 §5.3.4 pointed at "Appendix F (Streamer Mode Constants)"** — Appendix F is *Smart Pin* Mode
  Constants; the streamer appendix is G. A broken cross-reference in a released manual. It also claimed "78 mode
  constants" (there are 79); the count is now gone rather than maintained, per the perishable-catalog rule.
- **§5.3.4 also described mode families that do not exist** — *"NCO mode uses data as frequency control words, RF
  mode uses data as modulation patterns."* `RF` is Read-from-FIFO; there is no NCO mode. FABRICATED.
- **The front matter named four appendices differently from their own titles** (A, D, I, J) — the reader's first
  navigation page disagreeing with the pages it indexes.

**A correction to the sweep plan's own caveat.** `STREAMER-GUIDE-CORRECTNESS-SPRINT-PLAN.md` §13 carried a
completeness note that *"neither table discloses that setting `D[19]` selects the other four-pin block."*
Checked live against the Silicon Doc, that is wrong on both halves: `D[22:19]` is a **four-bit block number**
(base pin = number x 4) and it belongs to **DDS/Goertzel only** (`:3997`) — the ADC sampling modes take their
block from `SETSCP` instead. The caveat was carried into a draft of this fix and removed before it shipped.
**Verify a ledger claim against the live source before writing it into a manual.**

**Verified correct and deliberately untouched:** the ADC Sampling Modes table (decodes `kDAC8` correctly), the
DDS/Goertzel constant values, and the RDFAST-to-LUT encodings — all re-checked row by row this pass.

## YAML→Manual impact survey — KB v1.16.3 (2026-08-16, `release-yamls` §8)

Delta: `spin2/methods/wrpin.yaml` · `architecture/smart_pins.yaml` ·
`architecture/smart-pins/smart-pin-11011-usb-host-device.yaml` · `architecture/cordic.yaml` ·
`architecture/streamer/overview.yaml` · `architecture/streamer/dds-goertzel.yaml` ·
`pasm2/getxacc.yaml` · `spin2/integration/spin2-pasm2-integration.yaml` ·
`spin2/special-symbols/at.yaml`.

Intersected against every live manual's `MANUAL-DESCRIPTOR.md` declared sources. **Survey done, not
skipped.** Most intersections are already owned by an in-flight Sprint 2 task, so no duplicate flag
is raised for them; the ones that are **not** covered are flagged below.

| Element | Intersects on | Disposition |
|---|---|---|
| Streamer Guide | streamer, dds-goertzel, getxacc, DEBUG_COGS | **covered** — «#220» «#221» |
| IOSP | `architecture/smart-pins/`, smart_pins | **covered** — «#219» (and the F-264 %TT material rides its v1.0.9 pass) |
| Assembly Reference | cordic, streamer | **covered** — «#228» |
| P2AN002 | cordic | **covered** — «#236» |
| XBYTE Guide | streamer | **covered** — «#227» (§15.3 restructure); see the F-268 flag below |
| **P2AN001 / P2AN003** | wrpin | **⚑ FLAG — re-audit against v1.16.3.** These two were read site-by-site and taken OUT of the release wave, but that read answered **F-259's** question (does every executable example carry `\| P_OE`?). **F-264 is a different fact** — that `%TT` is context-dependent and that adding `P_OE`/`P_CHANNEL` to a **non-smart-pin cog DAC** kills it. Any cog-DAC or `P_DAC_*` configuration in these app notes was never checked against that. Do not treat the wave exclusion as covering it. |
| **P2AN004** | wrpin | **⚑ FLAG — same class as above**, and it was never in the wave at all. |
| **Architect's Guide** | CORDIC, streamer | **⚑ FLAG — re-audit against v1.16.3.** Not in the release wave. Declares both sources; the CORDIC hub-in-loop rule (F-263) and the `DEBUG_COGS` streamer caveat (F-266) are new since its last pass. |
| **DeSilva Tutorial** | CORDIC | **⚑ FLAG — re-audit against v1.16.3.** It *is* in the wave, but for §1/§2 (Acknowledgments, Appendix A) only — its CORDIC material is untouched by «#222»/«#223» and unexamined against F-263. |
| All elements showing PASM fragments | `spin2-pasm2-integration.yaml` | **⚑ FLAG — F-268 class sweep**, filed below and deliberately not folded into a correction task. |

These flags are the drift signal `document-audit` drains on each element's next pass. They are
**not** Sprint 2 scope and must not be pulled into it silently — surface them to Stephen as a scope
decision.

---

## Spin2/PASM2 boundary defect promoted from the empirical ledger (2026-08-16) — F-268

### F-268 — inside a Spin2 object, `##hubsymbol` in a `DAT` block resolves against `$400`, not the object's load address. `PARTIAL — KB DONE 2026-08-16; guide-side sweep owed`

**Origin:** EF-060, which had no F-number and no KB entry. Surfaced while getting the F-256/EF-058
rig working, so it is a by-product rather than a target — and it is the broadest-reach item the
2026-08 campaign produced.

**The fact.** A PASM fragment that is correct in a **standalone** PASM file reads **interpreter
memory** when pasted into a Spin2 object's `DAT` block: `##hubsym` resolves against `$400` rather
than the object's load address. Measured on real P2 silicon: `@disp` = `$1AF9` from Spin2 versus
`##disp` = `$0651` from PASM in the same object — **5,288 bytes apart**, and the `##` form returned
garbage.

**Why it matters more than its size suggests.** It bites anyone who copies a PASM fragment out of a
guide or reference into a Spin2 object — which is how most P2 code is written. It assembles, it
runs, and it reads the wrong memory. **Workaround:** pass hub addresses in from Spin2 with `@`, or
address through PTRA/PTRB.

> **KB APPLIED 2026-08-16 («#218»).**
> `language/spin2/integration/spin2-pasm2-integration.yaml` →
> `integration_rules.hub_address_resolution`: the rule, where it is instead correct (standalone
> PASM), why it bites, the workaround, and the measurement. Findability: a matching one-line pointer
> added to `language/spin2/special-symbols/at.yaml` `notes:`, since `@`'s
> object-relative-vs-absolute entry is exactly where a reader chasing this lands — that file already
> documented the Spin2 side of the same boundary and had no route to the PASM side.
> Source trace: EF-060.

**Still owed (manual head, NOT tasked in Sprint 2):** our guides present standalone-PASM fragments
without saying so. A class-wide sweep of `##hubsym`-style fragments across the live manual set is
the durable fix; scope it as its own item rather than folding it into a correction task.

> **KB + KB-GUIDE HALVES RE-VERIFIED ON DISK 2026-08-25 («#300») — both clean; only the MANUAL sweep remains.**
>
> - **KB half — DONE, confirmed at the file.**
>   `deliverables/ai/P2/language/spin2/integration/spin2-pasm2-integration.yaml:427-436` carries
>   `integration_rules.hub_address_resolution` complete: the rule, `correct_in` (standalone PASM),
>   `why_it_bites`, the `workaround` (pass `@` in from Spin2, or address through PTRA/PTRB), the
>   `measured` figures (`@disp` `$1AF9` vs `##disp` `$0651`, 5,288 bytes apart) and
>   `source: … P2-EMPIRICAL-FINDINGS.md EF-060 (2026-08-14)`. The findability pointer is live at
>   `language/spin2/special-symbols/at.yaml:219`.
> - **KB-guide half — NOTHING OWED, and this was measured rather than assumed.** Swept
>   `deliverables/ai/P2/guides/` for `##`-prefixed hub-symbol fragments: **zero hits**. The KB's guide layer
>   does not present any standalone-PASM fragment that would carry this defect, so there is no guide-side
>   sweep to run.
> - **What is left is the MANUAL set only** — the class-wide sweep named above, which is «#301»'s scope,
>   not a KB item. Status stays `PARTIAL` for that reason alone.

---

## The whole app-note companion set is version-frozen (2026-08-16) — F-271

### F-271 — every `application-notes/*.yaml` companion still carries its maiden `version:` while the note it ships with has moved on, so an agent cannot tell which edition it holds. `RESOLVED — DECIDED 2026-08-16 (Stephen); the KB has one edition, so the field is deleted rather than maintained. Carried to PUNCH-LIST.md PL-004; its "Sprint 2 first" gate discharged when Sprint 2 closed 2026-08-19, and PL-004 parts 1 + 3 are being worked now.`

**Surfaced by:** the F-270 content probe against the published MCP. The corrected SINC2 line came
back live and correct — sitting four lines under `version: "1.0.0"`, in a companion to a note that
is at **1.0.3** and going to 1.0.4.

**The defect, across all seven:**

| Companion | `version:` | Note's released version (roster) |
|---|---|---|
| p2an001-single-pin-instrumentation-adc | `1.0.0` | **1.0.3** (→1.0.4 in the wave) |
| p2an002-cordic-for-real-work | `1.0.0` | **1.0.2** |
| p2an003-dac-analog-signal-generation | `1.0.0` | **1.0.2** |
| p2an004-frequency-rotation-rc-timing-measurement | `1.0.0` | **1.0.2** |
| p2an005-cooperative-multitasking-tasks | `0.1.0` | **1.0.2** |
| p2an006-sizing-cog-task-stacks | `0.1.0` | **1.0.1** |
| p2an007-data-structures-new-facilities | `1.0.0` | **1.0.1** |

**Seven for seven — so this is the convention failing, not a missed file.** The stamp has never been
advanced by any release.

**Why it matters — and the severity claim this entry first carried was WRONG, corrected 2026-08-16
on Stephen's challenge ("why are there version numbers in the yaml?").**

The original text said a frozen stamp is *"worse than absent, because an agent that caches by version
sees no change and keeps serving the stale body."* **Nothing caches by version.** Checked, not
assumed: the published index carries exactly `path`, `mtime`, `sha256` per entry — change detection
is the git commit timestamp plus a content hash, both of which updated correctly when F-270 shipped.
A consumer mechanism was asserted without being verified, which is this sprint's own named failure
mode. **The field is inert.**

**What is left is real but smaller:** the stamp misleads anyone who *reads* it — a human opening the
file, or an agent quoting `version` when citing the companion. P2AN001's was edited twice this sprint
(F-269, F-270) and still reads `1.0.0`. It is a truthfulness defect in shipped metadata, not a
cache-correctness defect. **Priority drops accordingly** — this is not urgent, and it is certainly
not worth a bulk edit of seven published files.

**The deeper finding, which is the actual reason to keep this entry.** `version:` appears in only
**24 of 1129** published YAMLs, carrying **two unrelated meanings** under one key name, with no
schema doc defining either (`APP-NOTE-DESIGN-DECISIONS.md`, which the companion header cites as its
schema authority, does not mention `version` at all):

| Population | What `version:` means there | Tell |
|---|---|---|
| **17 files** — `architecture/smart_pins.yaml` (1.2), `architecture/streamer/_index.yaml` (2.0), `spin2/conventions/*` (1.0.0–2.0.0), `guides/*` | **the file's own content revision** | almost always paired with `last_updated:`; refers to nothing outside the file |
| **7 app-note companions** | positioned as **the note's** version — sits under `doc_id:` and above `kind: application-note`, beside the note's `title`/`subtitle` | no `last_updated:` |

**So "which meaning is right" has no documented answer, and the tree's majority reading is the
opposite of the one this entry first recommended.** That recommendation was made from the app-note
files alone, before the other seventeen were looked at.

**This is F-270's rule showing up structurally.** F-270 established that *an app-note correction is
not complete until its YAML companion carries it.* The companion here **did** carry the content — and
still shipped a false edition stamp. So the rule needs its second half: **the companion ships under
the note's version, and that stamp is advanced at release, not at edit.**

**Deliberately NOT swept.** Two things need Stephen's decision before any edit:
1. **Semantics.** Does `version:` mean *the note's version* (then all seven get stamped and it becomes
   a `release-manual` step) or *the companion's own schema/content revision* (then it needs renaming
   to say so, and a separate `note_version:` added)? The files carry no comment either way. Guessing
   here and sweeping seven published files is exactly the F-211 failure mode — a class-wide sweep
   amplifying an ungrounded reading.
2. **Whether it is a KB bump at all.** These are published `deliverables/ai/P2/` files, so any stamp
   change ships in a KB release; but the *natural* moment to advance them is each app note's own
   release. Those two cadences are not the same and the answer decides which skill owns the step.

**Ask the prior question first: what is this field FOR?** (Stephen, 2026-08-16: *"how is that version
useful to agents?"*) Worked through honestly, **a bare `version:` is of no use to an agent**:

- It is **not** how change is detected — that is `mtime` + `sha256` in the index, and they work.
- It is **not** how content is selected — an agent fetches by key and gets exactly one body. There is
  no version negotiation, no second edition to choose between, no `1.0.3` still on the shelf.
- It **cannot** be compared against anything the agent holds, because the agent has no prior copy.
- A stamp only earns its place if something can be **checked against** it. `1.0.4` next to nothing is
  a number an agent can only quote — and quoting it is precisely how a stale one does harm.

**What would actually serve an agent** is the *note's* version — not as a bare number, but as the
answer to a question an agent really has: *"the PDF in front of the user — does this digest match
it?"* That makes the useful field an explicit, self-describing link to the human artifact
(e.g. `describes_document: {doc_id: P2AN001, version: 1.0.4, released: 2026-08-16}`), which a
reader can compare against the cover of the PDF they are holding. The bare `version:` key answers no
question and, worse, reads as the *file's* version to anyone applying the tree's majority convention.

**Revised recommendation — cheaper and more honest than the original.** Do **not** stamp the seven
files with note versions and add a fourth version location to maintain. Instead:
1. **Delete the bare `version:` from the seven companions** — it is inert, ambiguous, and currently
   false. Removing a field that answers nothing beats maintaining it in seven places forever.
2. **If** the match-the-PDF question is worth answering, add the explicit `describes_document:`
   block in its place, stamped by `release-manual` alongside the roster row and cover/`request.json`
   — one self-describing field, not a number whose meaning must be inferred.
3. Leave the **17 non-app-note** files alone; there `version:` + `last_updated:` is a coherent
   file-revision convention. Worth documenting, not changing.

**Note the reversal:** this entry originally recommended stamping all seven to track the note. That
was written from the app-note files alone, before the other seventeen or the index schema were
looked at, and it would have institutionalised the ambiguity rather than removing it.
[[feedback_drop_techniques_that_lower_quality]] — when a shape keeps producing defects, remove the
shape rather than add a rule to maintain it.

**Status:** `RESOLVED — DECIDED AND PUNCH-LISTED (2026-08-16)`. **Do not re-file, do not work it now.**

**Stephen's decision supersedes both recommendations above, including the revised one.** The
principle is broader than this field: **the published KB has exactly one edition — the current one —
so nothing in the tree should cite currency or a version at all.** Every reference means *latest*.
That rules out the `describes_document:` block too; it is still a currency citation, just a
better-labelled one. **Delete the shape rather than maintain it.**

**Deferred deliberately, not forgotten** — *"we are trying to get to released documents, and we are
not there yet given our task list. We should stay away from any diversions at this point in time."*
Sprint 2's release wave comes first.

> **PL-004 PARTS 1 AND 3 EXECUTED 2026-08-21.** The "Sprint 2's release wave comes first" gate
> discharged when Sprint 2 closed 2026-08-19. **Part 1:** the bare `version:` is deleted from all
> seven companions. **Part 3:** 25 build stamps rewritten plus the stale `version_info` block in
> `tools/pnut-ts-compiler.yaml` (which read v1.51.5, four minor versions behind) removed. The
> dividing line applied throughout — **cite the EDITION, never the BUILD**: `Spin2 v55`,
> `Added in PNut v47`, `{Spin2_v54}`, `minimum_version:` are facts about the LANGUAGE that a
> reader can hit, and all 278 survive untouched; `compile-verified with pnut_ts v1.55.0` is a
> record of what someone happened to run, and is gone. The seven app-note `toolchain:` lines were
> EDITED, not deleted — their `-d` requirement, `_clkfreq` and `{Spin2_v45}` gating are durable
> and load-bearing; only the `1.55` clause went. **Part 2 (the other 17 `version:`/`last_updated:`
> bearers) remains open** and still needs the per-population decision PL-004 requires; it was
> deliberately not swept on the app-note reading.

**Carried to → `engineering/tools/p2kb-mcp/PUNCH-LIST.md` PL-004**, which holds the full scope
(7 companions to strip; the other 17 `version:`/`last_updated:` bearers to review per-population,
NOT to sweep on the app-note reading; prose "as of" sweep; PDF versioning explicitly out of scope).

---

## IOSP suppressed-qualifier probe (2026-08-16, «#230») — F-274…F-275

> **Method and full result:** `engineering/analysis/2026-08-16-iosp-suppressed-qualifier-probe.md`.
> The probe asked whether a qualifier was ever **never written** — the half no diff can see, after
> «#214» returned NIL on qualifier *removal*. Result is **not nil**: two findings, both in Ch.19,
> the one chapter our own `KNOWLEDGE-GAPS.md` already flags as OPEN (G-005).
>
> **The pattern is the useful part, and it inverts hedge-counting.** Ch.16 (ADC) — the chapter that
> qualifies most — is right, and says so explicitly (*"nominal resolution … not ENOB"*, *"a
> mechanism, not a guaranteed specification"*, *"never a datasheet value"*). Ch.19 — the chapter
> that qualifies least — is the one with the gap. The guide is well calibrated where its evidence
> is rich, and goes quiet about its own uncertainty exactly where the evidence is thinnest. The
> signature to look for is a missing **dependency**, not a missing **word**.
>
> **Neither finding ships in the current wave.** IOSP left it when F-261 reversed into F-269, so
> both wait for IOSP's next release rather than being force-fitted into this one.

### F-274 — IOSP Ch.19 §19.4 teaches an FS-USB configuration at exactly the clock its own source flags, and states no sysclk dependency anywhere. `PARTIAL — corrected in opus-master 2026-08-25 («#301»); render + release owed`

**Location:** `manuals/p2-io-and-smart-pins-user-guide/opus-master/part-4-special-modes/chapter-19-usb.md:122-128`.
**RELEASED (v1.0.8).**

The chapter's only worked baud example computes full-speed (12 Mbps) USB at **80 MHz**.
`engineering/ingestion/KNOWLEDGE-GAPS.md` **G-005 is OPEN**: *"Scope of smart-pin USB support;
documented sysclk floor (**FS-USB > 80 MHz**, LS-USB less)."* The chapter states **no sysclk
dependency for USB anywhere** — not in §19.4, not in §19.9 Limitations, not in the Quick Reference.
A reader following the worked example lands on the boundary the open gap is about with nothing to
tell them a boundary exists.

**Do NOT "fix" this by asserting the floor.** G-005's only source is a reviewer comment (Granville)
on the Titus document — an **upstream lead, not a citation**, and not something to carry into
reader-facing prose as fact. Doing so would trade a silence for an unsourced claim.

🟢 **NEW EVIDENCE 2026-08-24 (`KNOWLEDGE-GAPS` pass-6 catch-up) — the correction is no longer
stuck between a silence and an unsourced number.** The DOCX-primary **P2 Hardware Manual @
2022/11/01** *does* state a sysclk dependency for USB, authoritatively and quantitatively:
the baud field is a 16-bit fraction of the system clock "whose two MSBs must be 0, **necessitating
that the baud rate be less than 1/4th of the system clock frequency**", with a worked 12 MHz-at-80
MHz full-speed example (`engineering/ingestion/sources/p2-hardware-manual/p2-hardware-manual-text.txt:1489`).
That is a citable hardware constraint the chapter can state on its own authority. It is **not** the
Granville floor and must not be presented as one — the > 80 MHz claim stays unsourced (`Q-003`),
and G-005 stays `PARTIAL` for exactly that reason.

**Proposed correction:** rework the worked example at a clock unambiguously clear of the question
(the chapter's own Spin2 example at `:264` already runs at 200 MHz), and state the **documented**
dependency — baud < sysclk/4, cited to the Hardware Manual — while saying the practical floor for
reliable FS signaling is unsettled. §19.4's existing transmit-pacing `::: caution` is the shape to
copy — it already names its own limit correctly.

**Not in scope of this finding:** the register-layer content (WXPIN config word, WYPIN line states,
the 16-bit RX status word, per-pin IN semantics) is properly sourced to Silicon
`p2-documentation.txt:8886-9006` and was verified sound during the probe. It is not implicated.

> **APPLIED IN OPUS-MASTER 2026-08-25 («#301») — RENDER OWED, so this is NOT closed.**
> All three legs of the proposed correction are in
> `…/opus-master/part-4-special-modes/chapter-19-usb.md`:
> - **The worked example moved off the boundary.** §19.4's baud example now computes 12 Mbps at
>   **200 MHz** — the clock the chapter's own Spin2 example (`:264`) and Quick Reference already
>   use — giving `$0F5C` and a host WXPIN word of `$CF5C`. Arithmetic re-derived on disk, not
>   copied: `12_000_000 / 200_000_000 × $10000 = 3932 = $0F5C`; `$C000 | $0F5C = $CF5C`.
>   The old 80 MHz / `$2666` / `$E666` figures were correct *as arithmetic* (they are the Hardware
>   Manual's own worked example) — they were removed because the clock, not the maths, was the
>   defect.
> - **The documented dependency is now stated WITH its citation**, which it was not: the ¼-`clkfreq`
>   ceiling is attributed in-text to the *P2 Hardware Manual* 2022/11/01 §*USB Host/Device
>   (%11011)*. Verified live at `engineering/ingestion/sources/p2-hardware-manual/p2-hardware-manual-text.txt:1489`
>   — *"a 16-bit fraction of the system clock, whose two MSBs must be 0, necessitating that the baud
>   rate be less than 1/4th of the system clock frequency."*
> - **The unsettled floor is named as unsettled, and carries no number.** A new `::: caution`
>   ("Clearing the ÷4 rule is not the same as having enough clock") says the ÷4 ceiling is the only
>   sysclk dependency any Parallax source states, that full speed clears it above 48 MHz — which is
>   that stated rule applied to the stated 12 Mbps, not a new claim — and that **no published source
>   settles what full-speed work needs in practice**. The Granville *> 80 MHz* figure is **not**
>   carried, in line with this finding's own instruction and `Q-003`.
> - **Discoverability fixed too**, which was half the complaint: the dependency was absent from
>   §19.9 and the Quick Reference, so a reader scanning limitations never met it. §19.9 gains a
>   **Clock Requirements** subsection and §19.10 a Key Points bullet, both pointing back at §19.4.
>
> **Gates:** `audit-code-line-length.py --budget 76` and `audit-inline-code-ascii.py` both exit 0 on
> the chapter (each proved able to fail on a negative control the same session). **No code block was
> touched** — the one edited line inside a fence is the ` ```formula ` block, which pairs to no
> example file — so byte-identity is untouched and `pnut-ts` does not apply.
> **Owed to «#302»:** confirm on the rendered page that the new `::: caution` and the §19.9
> subsection set, and that the reflowed §19.4 does not push the following table. `G-005` stays
> `PARTIAL` and `Q-003` stays open; neither is this finding's to close.

### F-275 — IOSP Ch.19 §19.5 states the P2 provides USB bus power; §19.8 correctly says it does not. `RESOLVED — verified IN THE RELEASE TAG 2026-08-25 («#301»), not inferred from this entry`

**Location:** `…/chapter-19-usb.md:210` against `:329`. **RELEASED (v1.0.8).**

`:210` — *"As a USB host, the P2: **Provides bus power (5V)**"*. The P2's I/O is 3.3 V and it
sources no 5 V rail. `:329` correctly lists *"5V power supply for VBUS"* among the external
components a host design must provide.

A plain factual error, self-contradicted two sections later. Not a calibration defect — surfaced by
the same read-the-claims pass, and recorded here rather than split off because it was found by the
probe and belongs with its record.

**Proposed correction:** §19.5 says the P2 *initiates* communication and *requires* a board-supplied
5 V VBUS rail, pointing at §19.8 for the external components.

**RESOLVED 2026-08-17 («#246»).** The bullet is out of the P2-verb list — it never described anything
the P2 does — and the fact it was carrying now stands on its own after the list: a host port supplies
5 V on VBUS, the P2 cannot source it (3.3 V I/O), and §19.8 has the external supply and its current
limiting. Fixed in opus-master; **IOSP is not in the release wave**, so it ships at IOSP's next
release alongside F-278's site conversions.

**ROOT CAUSE, and the fix extended (Stephen, 2026-08-17).** The claim was not invented — **the P2 Edge
breakout boards really do carry 5 V to the I/O headers**, which is almost certainly where "the P2
provides bus power" came from. Removing the wrong sentence without explaining the true one would have
left the next reader to make the same inference from the same board. §19.8 now carries what the board
guides actually say, and it is more specific than "the headers have 5 V":

- Each 8-pin accessory header provides two grounds, a **Vxx** pin (3.3 V from that group's LDO), and
  **optionally** 5 V — **passed straight through from the power jack**, not generated by the board.
- **Two headers have no 5 V routed at all: P24–P31 and P56–P63.** The second bank contains **pins
  56/57, which is the pair this chapter's own examples use** — so the chapter was teaching a host
  design on the one header that cannot supply its VBUS.
- Because the header 5 V is the input supply passed through, it carries no current limit, so §19.8's
  current-limiting requirement still lands on the design.

**Sources (three board guides, consistent):** *P2 Edge Mini Breakout Board* (#64019) §6–§7, *P2 Edge
Breakout Board* (#64029) §6–§7, *P2 Edge Module Breadboard* (#64020) §12–§13 — the last gating header
5 V behind an ACC ON/OFF shunt. The guides anticipate the confusion themselves: *"5V OUTPUT VOLTAGE IS
PROVIDED TO POWER EXTERNAL ACCESSORIES & SENSORS. DO NOT CONNECT 5V DIRECTLY TO ANY OF THE P2 SMART
I/O PINS! ALL I/O PINS OPERATE AT 3.3V LOGIC LEVEL AND ARE NOT 5V TOLERANT!"*

**Class-wide sweep done, and it is clean.** Every other `5 V` mention across all manual and app-note
masters was read: the Architect's Guide (level shifters), deSilva ("P2 is 3.3V, not 5V tolerant"),
IOSP Ch.12 (legacy 5 V logic as an input case), and P2AN004 (the TSL235R's 2.7–5.5 V supply range) are
all correct. **F-275 was the only site** — verified rather than assumed.

**Related — looked at and FIXED 2026-08-17, at the next pass as scheduled.** Pins 56/57 are also the
Edge Module's onboard LED pins and sit in the programming/WX-adapter bank — and the manual itself uses
56 as `LED_PIN` in five places and 57 as `BUTTON_PIN`. Worse, this very release adds the statement
that P56–P63 carries no 5V, so the chapter would have demonstrated a **bus-powered** peripheral on the
one bank with no bus power. §19.8 had absorbed that by adding a caveat — *"the pin pair this chapter's
examples use... must take VBUS from elsewhere"* — which is a workaround for a pin choice, not a
reason for it.

**Chapter 19's examples now use P8/P9**: a free even/odd pair in a 5V-bearing bank, clear of every
other pin constant in the manual. The §19.8 caveat is gone with the need for it, and the bank fact
stands on its own. Verified: byte-identity GREEN 15/15, `ch19-usb-device-config.spin2` compiles clean
under `pnut-ts -d`, all IOSP gates clean. The "Valid pairs" enumeration still lists 56/57 — it is an
enumeration of what the silicon allows, which is unchanged.

**The lesson is the caveat itself.** Prose was written to explain around a defect instead of removing
it, and that prose then read as settled. A sentence that exists only to excuse a choice is a marker
for the choice, not a resolution of it.

> **CLOSED 2026-08-25 («#301») — and the closure was measured against the TAG, because this entry's
> own text is what went stale.** The body above said *"IOSP is not in the release wave, so it ships
> at IOSP's next release"* and then nothing came back when that release happened. It did:
> `git show p2-io-and-smart-pins-user-guide-v1.0.9:…/chapter-19-usb.md` carries **all three** halves
> of the fix — the wrong bullet is gone, the replacement sentence stands at `:214` (*"Bus power is a
> board responsibility, not a P2 one… the P2 cannot source it — its I/O operates at 3.3V"*), and the
> examples are on the 5V-bearing pair at `:54` / `:266` (`USB_DM = 8`). Nothing is owed: master
> fixed **and** shipped. Same drift direction as F-278 — the record understated what had been done,
> which sends the next reader to redo finished work.

**Next finding ID after this block: F-276.**

---

## Stephen's review of the Sprint 2 gate release (2026-08-16, «#234») — F-276…F-283

> **Full dispositions and reasoning:** `engineering/planning/SPRINT2-VISUAL-REVIEW-NOTES-2026-08-16.md`.
> Eight observations (V-1…V-8) worked one at a time against the gate commit `fea28f1c`. Four became
> findings; the rest were scope and structure decisions recorded in that file.
>
> **All four are tasked into the voice-conformance family «#240»–«#248» and are absorbed into the
> per-manual pass rather than applied as point fixes** — applying them first and conformance-checking
> after would write the same prose twice and have the second pass judge what the first just wrote.
>
> **Two of these were found by the review, not by the sprint's own sweeps**, and that is the useful
> part: F-277's site sits in body text no Sprint 2 task touched. A findings-driven sweep sees the
> diff; it does not see the document.

### F-276 — deSilva Appendix A grounds the P2's value in "missed deadlines," an argument that fails against the reader it is aimed at. `PARTIAL — all three sites corrected in opus-master (Appendix A 2026-08-17, the two residual shapes 2026-08-25 «#301»); render + release owed`

**Location:** `manuals/p2-pasm-desilva-style/opus-master/COMPLETE-OPUS-MASTER.md` — §*"What You Are
Buying With That"* (`:5993-6001`), with the same shape at `:225`, `:6001`, `:6049`.
**RELEASED — and the blast radius grew while this line said otherwise.** Written during Sprint 2,
committed at `fea28f1c`, and **v3.0.6 PUBLISHED 2026-08-17** (166pp). This annotation read
`NOT RELEASED … ships in v3.0.6` until 2026-08-23; it was a *prediction*, correct when written and
false the moment v3.0.6 shipped, and nothing came back to update it. The finding is **still open** —
re-verified against the master 2026-08-23, the shape survives at `:229` (*"Your sensor sampling never
misses a deadline"*) and `:6061` (*"missed timing deadlines"*). `:5995` uses "deadline" in the
project-schedule sense and `:4279` in the counter-wraparound sense — both legitimate, leave them.

The section argues that conventional MCUs turn hard real-time into a scheduling problem with "a long
tail of *why did that deadline slip once an hour?*", and that the P2 therefore "raises your odds of
finishing." Three defects:

1. **It argues against a strawman.** A correctly prioritised Cortex-M meets its deadlines; rate-monotonic
   analysis is fifty years old. An RP2350 PIO state machine meets them absolutely. The reader best
   qualified to judge the appendix concludes we are comparing the P2 against *badly built* alternatives.
2. **It is unfalsifiable and unsourced.** "Raises your odds of finishing" is a project-outcome claim with
   no evidence — a marketing claim in an engineering voice, in a document whose credibility is its
   checkability.
3. **It contradicts a passage two pages earlier.** The RP2350/PIO paragraph added in the same sprint
   (`:5868`) already tells the reader that cheap deterministic offload hardware exists.

It is also a declared **R1** violation under the manual's own `voice-guide.md` (ADOPT, scoped to
technical P2 claims), written the day before the prose was.

**Proposed correction:** replace with the **composability** claim — adding a task to a shared core
perturbs the timing of the tasks already there; giving a task its own cog does not. Take the concept
from the Architect's Guide Ch.7 but **not its vocabulary** (no "forces", no "cadence boundary"): use
cogs, pins and locks, which the reader has earned over sixteen chapters. The section must stand fully
alone for a reader who never opens that book. Sweep the same shape at `:225`, `:6001`, `:6049`;
`:4275` uses "deadline" legitimately (delta-vs-absolute comparison under counter wraparound) — leave it.

> **ALL THREE SITES NOW CORRECTED — the main one was ALREADY DONE and this entry did not know.**
> Re-measured on disk 2026-08-25 («#301»), and split into what was already fixed and what was not:
>
> **§*"What You Are Buying With That"* was rebuilt on 2026-08-17** by `361ac02a` (*"deSilva voice
> pass, part 2: Appendix A rebuilt"*), and it was rebuilt on **exactly the composability argument
> this finding proposed** — *"Put eight jobs on one processor and they are sharing it… Give each job
> its own cog and that simply stops being true — adding the eighth cog does not disturb the first
> seven, because they were never sharing anything to disturb."* It also does the two things the
> finding asked for and did not spell out: it concedes the P2 is *"often neither"* faster nor
> cheaper, and it hands the reader to an ESP32 where an ESP32 is the right answer. No "forces", no
> "cadence boundary". Nothing was owed here and nobody had said so.
>
> **The two residual shapes were real, and are fixed now** (`COMPLETE-OPUS-MASTER.md`, master
> line numbers as found today, not as this entry recorded them):
> - **`:229`** (Ch.1 *"Why P2?"*) read *"Your serial handler never delays your motor control. Your
>   sensor sampling never misses a deadline."* Both halves overreach: a cog can miss a deadline
>   perfectly well if the code in it is too slow. Replaced with the mechanism instead of the
>   promise — the handler *cannot* delay the motor control **because it is not on the same processor
>   to delay it**, and *"add another job later and the ones already running keep the timing they had
>   — they were never sharing anything for the new one to take."* Same claim as the rebuilt Appendix,
>   arriving 5,700 lines earlier, in Chapter 1 vocabulary.
> - **`:6061`** (Summary) read *"Engineers who've fought … missed timing deadlines … find P2
>   refreshing. You spend your time solving your actual problem, not fighting your MCU."* That is
>   defect 2 of this finding verbatim — an unfalsifiable project-outcome claim in an engineering
>   voice. Replaced with reader-recognition that keeps the pedagogy and drops the marketing: *"If you
>   have ever re-tuned a whole interrupt priority table because you added one handler… The work does
>   not disappear — you will still write the driver, and you will still get the timing wrong the
>   first time. What changes is that you stop having to redo it every time the design grows."*
>
> **`:5995` and `:4279` were re-read and deliberately left**, as this entry instructs: the first uses
> "deadline" in the project-schedule sense, the second in the counter-wraparound sense.
> **Gates:** `audit-code-line-length.py --budget 76` and `audit-inline-code-ascii.py` exit 0 on the
> master; no code block touched, so byte-identity is untouched. **Owed to «#302»/release:** the
> master is 166 pp at v3.0.6 and these are body-text reflows — confirm on the page, then release.

### F-277 — deSilva tells the reader that peripheral conflicts are impossible on the P2. They are not, and our own published manual documents why. `RESOLVED — fixed 2026-08-17, shipped in v3.0.6; the owed class-wide check RUN and CLEAN 2026-08-25 («#301»)`

**Location:** `…/COMPLETE-OPUS-MASTER.md:6045` — *"**64 smart pins** means peripheral conflicts become
impossible"* — and `:5940` — *"I/O flexibility that eliminates peripheral conflicts."*
**RELEASED (v3.0.5)** — both sites are pre-existing body text; neither was touched by any Sprint 2 task.

Smart pins eliminate the **pinmux** conflict: any pin can be any function, so a design never runs out of
"the SPI pins." They do **not** eliminate **resource** conflict. *The P2 Architect's Guide* (v1.0.3,
Ch.7 Force 1) states the opposite from the silicon: P2 pin outputs are OR'd with no hardware arbiter, so
two cogs driving one bus corrupt it — and the symptom "presents as flaky hardware — intermittent,
timing-dependent, and miserable to debug, because the symptom is three layers away from the cause."

This is the most expensive kind of wrong claim: it tells a beginner that a real, nasty bug class cannot
happen, in the manual most likely to be their first contact with the chip. It is also a declared **R1**
violation, whose stated reason is precisely this case — *"a tutorial's worked examples are exactly where
an overstated claim reaches a beginner who cannot yet check it."*

**Proposed correction:** state what smart pins actually remove (the pinmux conflict, and running out of
peripheral blocks) and keep single-ownership of a shared bus as a live concern. **Class-wide check
owed:** the same "conflicts impossible / eliminates conflicts" phrasing may appear in other manuals.

**Related, same pass, same manual — not separately numbered:** `:6042` "eliminates entire categories of
problems"; `:3897` "No surprises, ever / Timing is guaranteed", self-contradicted by the *correct* hedge
at `:5911` (5911 is right); `:3729` "impossible to achieve this precision with interrupts" (F-276's
strawman); `:5804`'s impossibility aside. ⚠️ **The reader-celebration at `:5804` STAYS** — deSilva's
voice guide explicitly protects celebration of reader progress as pedagogy, and an early draft of this
finding wrongly proposed cutting it.

> **CLOSED 2026-08-25 («#301»). Both named sites and all four related sites were fixed on
> 2026-08-17 by `9f4ddb4f` — the commit is literally named *"deSilva voice pass, part 1: F-277 and
> the claims that overreached"* — and shipped in **v3.0.6** the same day. This entry was left saying
> `CONFIRMED` for eight days.** Verified by reading the commit's diff, not by trusting its message:
> `-**64 smart pins** means peripheral conflicts become impossible` → `+ … means no function is ever
> stuck waiting for the one pin that supports it`; `-I/O flexibility that eliminates peripheral
> conflicts` → `+ … and no more shuffling functions around to find pins that support them`;
> `-one that eliminates entire categories of problems` → `+ … one that changes which problems you
> spend your time on`; and the `:3897` / `:3729` absolutes are gone.
>
> **The `:5804` ⚠️ was honoured, and that is worth recording because it is the part a sweep gets
> wrong.** The celebration was **reshaped, not cut**: *"You're not just another embedded programmer
> anymore. You think in parallel. You see solutions that others miss."* survives verbatim; only the
> false-impossibility tail (*"When someone says 'that's impossible in real-time,' you know better"*)
> was replaced, with a move rather than a boast — *"When someone starts sketching an interrupt scheme
> to keep one job on time, you reach for a different move first — give that job a cog of its own."*
>
> **THE CLASS-WIDE CHECK THIS FINDING DECLARED OWED IS NOW RUN, and it is clean.** Swept **every**
> `opus-master/` body and CHANGELOG across all manuals and all seven app notes for
> `conflicts (become) impossible` / `eliminates … conflicts` and, more broadly, for the bare word
> *impossible*: **zero** conflict-impossibility claims anywhere in the P2 set. The only surviving
> `impossible` uses are legitimate — `architect-guide-body.md:101`/`:116`/`:358`/`:959` (a datasheet
> that is hard to find, a hand-wiring limit, a cohesion argument, and a torn read under a
> sequence/**acknowledge** handshake, which P2AN007 R3 `:214` confirms is the load-bearing part) and
> `xbyte-body.md:169`/`:638`, which *argue against* impossibility framing rather than assert it.
> (`Donna-Manuscript` hits are a private non-P2 book and out of scope.) Verified rather than assumed,
> which is the standard this finding set for itself.

### F-278 — wrong-code examples ship in ordinary syntax-highlighted blocks, distinguished only by a comment, in three manuals. `PARTIAL`

**Locations (8 sites — the 7 first enumerated, plus the 8th the narrow pattern missed).** Sites are
named by section rather than by line, because master line numbers move with every content task and a
stale number sends the next reader to the wrong block. **All 8 are CONVERTED, and 7 of them have
SHIPPED — verified against the release tags on 2026-08-20 («#282»), not inferred from this register:**

| Manual | Site | State |
|---|---|---|
| Streamer | §13.4's `\|`-vs-`+` pair | converted · **RELEASED v1.0.9** (2026-08-19) |
| Debug Window | `ch12-bidirectional.md`, both sites | converted · **RELEASED v1.1.3** (2026-08-18) |
| IOSP | `appendix-e-troubleshooting.md` ×3, `chapter-17-serial-receive.md`, `chapter-11-serial-transmit.md` | converted · **RELEASED v1.0.9** (2026-08-18) |
| Debug Window | `ch08-scope-xy.md` blockquote pair | **deliberately deferred** — see below |

**This annotation used to read `(NOT RELEASED, v1.0.9)` / `(NOT RELEASED, v1.1.3)` / `(RELEASED,
v1.0.8)`, and all three were stale.** The releases happened on 2026-08-18 and 2026-08-19 and nothing
came back to say so. Note the direction: the record understated what had been done, so a reader is
sent to redo finished work. `audit-register-hygiene.py` cannot see this class — it detects only the
opposite drift, a headline claiming a fix over a status token that does not agree. Same gap as F-272.

The platform provides `AntipatternBlock` (`p2kb-platform-content.sty:277` — red fill, red border, 4 pt
left rule), reachable as a ```` ```antipattern ```` fence or `::: antipattern` div via
`p2kb-platform-code-coloring.lua`. deSilva (6 sites) and Assembly (`appendix-h-reserved-words.md:569`)
use it correctly. The seven sites above do not — wrong code sits in ```` ```spin2 ````, marked only by a
`' WRONG` comment, so it carries identical highlighting and identical visual authority to correct code.

**Streamer's is the worst**, because the correct and the wrong form share **one block**. A reader
skimming code blocks — how people actually use a reference guide — can lift the wrong line without
reading the comment. It is the EF-053 `P_OE` material, where the failure is silent and total: measured
on silicon at 6,737 ADC counts for `|` against 1,407 for `+`, indistinguishable from no drive.

**Proposed correction:** split Streamer's into two **adjacent** blocks — correct stays ```` ```spin2 ````,
wrong becomes ```` ```antipattern ````. Green beside red is a stronger contrast than two comments in one
block, so the pedagogy improves rather than suffers. Convert the Debug Window and IOSP sites in place.

**Zero platform cost — verified:** `p2kb-streamer-reference.latex:21`, `p2kb-debugwin.latex:23` and
`p2kb-iosp-reference.latex:22` all already load `p2kb-platform-content.sty`. Markdown-only in all three.

**A fourth Debug Window site is deliberately NOT converted.** `ch08-scope-xy.md:71` pairs a wrong
line and its corrected form inside a **blockquote** callout (`> ```spin2`). Converting it would make
`> ```antipattern` the **first instance of that fence-inside-blockquote combination anywhere in the
set** — `> ```spin2` appears only in this one file (2 uses, shipped in v1.1.2, so that form is
render-proven; the antipattern form is not). Introducing an unverified fence combination into a
manual shipping in the current wave risks a silent render defect for a two-line paired contrast that
already reads correctly. **Action: verify `> ```antipattern` at the next Forge round-trip
(`forge-test`), then convert if it renders.** Same reasoning as the `\|`-in-a-table-code-span trap:
no precedent in the set is a render risk, not a green light.

**IOSP is not in the release wave.** Its sites are fixed in opus-master and ship at its next release —
editing a master is not releasing a document. *(That next release came: **v1.0.9, 2026-08-18**. All
five conversions are in the tag.)*

**IOSP RESOLVED 2026-08-17 («#246») — five sites, not four.** The four declared sites are converted.
A **fifth** turned up because this pass used the broader wrong-code pattern
(`WRONG|Wrong|INCORRECT|Do not do this`) rather than the `^' *WRONG` form that missed the Debug Window
blockquote: `part-2-output-modes/chapter-11-serial-transmit.md:174`, a `**Wrong:**`-labelled
```` ```spin2 ```` block already paired with its `**Correct:**` twin. **The narrow pattern under-counted
this finding in two manuals; the enumeration above is the floor, not the census.** Three of the IOSP
sites carried the wrong and correct forms in **one** block and were split the way Streamer's was —
```` ```antipattern ```` then ```` ```spin2 ```` — so the reader gets red-beside-green rather than two
comments in one box.

> **RE-MEASURED 2026-08-25 («#301») — the 8th site is ALREADY CONVERTED IN THE MASTER, so what is
> owed has changed shape.** `ch08-scope-xy.md:70` now reads `> ```antipattern` (with its `> ```spin2`
> twin at `:74`), converted by `f769b46a` on 2026-08-17 — i.e. it went in **ahead of the render gate
> this finding set for it**, not after. The status text below still describes a decision
> ("convert if it renders"); the decision is made and the code is in the file. Grep confirms this is
> still the **only** fence-inside-blockquote construction in the whole set: `> ``` ` matches
> `ch08-scope-xy.md` and nothing else, at exactly those four lines.
>
> **So the risk this finding identified is now live rather than avoided**, and that is the honest
> reading: an unproven fence combination is sitting in a master that will render. Nothing here can
> settle it — a PDF is produced on the Forge, not in this container.
>
> **Owed to «#302» / the next Debug Window `forge-test`, and this is the whole of it:** open the
> rendered page for §SCOPE_XY's create-line callout and confirm the `> ```antipattern` block renders
> as an AntipatternBlock **inside** the blockquote — red fill, red border, left rule — rather than
> collapsing to a plain quote, swallowing the fence markers, or breaking out of the callout. If it
> renders, this finding closes with no further edit. If it does not, revert `:70`/`:74` to
> `> ```spin2` and record the platform limitation. `p2kb-debugwin.latex:23` already loads
> `p2kb-platform-content.sty`, so a failure would be a filter/blockquote interaction, not a missing
> package.
>
> **The other 7 sites are re-confirmed shipped** and are not part of what is owed.

**Status:** `PARTIAL — 8 of 8 sites converted IN SOURCE; 7 shipped (Streamer v1.0.9, Debug Window
v1.1.3, IOSP v1.0.9). The 8th (ch08-scope-xy.md's blockquote pair) is converted but its render is
UNPROVEN — it is the only `> ```antipattern` in the set. Verify it on the page at the next Debug
Window Forge round-trip; that render is the only thing between this finding and closure.`

### F-279 — the XBYTE guide grounds a load-bearing hardware claim on a sibling manual in the same family, without disclosing it. `RESOLVED — fixed in the v1.1.0 restructure, shipped 2026-08-19; closed on re-verification 2026-08-23`

> **CLOSED 2026-08-23, verified against the master, not inferred.** The circular citation is **gone**:
> *"P2 Assembly Language Reference"* now appears **zero** times in `xbyte-body.md`. The `_RET_ CALL`
> hazard moved to §16.3 in the v1.1.0 restructure and is grounded on a **primary** source —
> *"Parallax's instruction table (P2 Instructions v35 – Rev B/C Silicon, row 410) defines `_RET_` as
> 'execute `<inst>` always and return if no branch.'"* That is exactly the fix this finding asked for.
>
> **This finding read `CONFIRMED` / `NOT RELEASED … ships in v1.0.2` for four days after it was done.**
> Two independent staleness paths crossed here: the fix rode a restructure that renumbered the target
> version (v1.0.2 was never published — **v1.1.0** shipped 2026-08-19 instead), and the cited line
> `:1427` now points at unrelated content because the restructure moved everything. A finding pinned to
> a line number and an unshipped version number is a finding nobody can re-check cheaply.

**Location (as filed):** `manuals/p2-xbyte-programming-guide/opus-master/xbyte-body.md:1427` — line
reference is **historical**; the restructure invalidated it.

The `_RET_ CALL` hazard block cites *"the condition table in the **P2 Assembly Language Reference
Manual**"* for `_RET_`'s branch-conditional semantics. That title is **not fabricated** — it is the cover
title of our own manual (`p2-assembly-language-manual/opus-master/front-matter.md:20`). The defect is
**circularity**: a peer derivation cannot ground a hardware claim, and unlike `P2AN002.md:378` — which
cites the same manual while labelling it *"a companion P2 Knowledge Base publication"* — this site
discloses nothing, so it reads to a reader as an external authority.

**Proposed correction:** repoint to the Parallax primary sources F-273 was actually grounded on —
*Propeller 2 Assembly Language (PASM2) Manual* draft (2022-11-01, p.68) and *P2 Instructions v35*
(row 410). **Verify the citation against the live source, not against this register** — a ledger is not
citation authority, and this guide has shipped fabricated names before (Appendix C).

**No set-wide normalisation owed.** The other four sites naming this document were checked and are
sound: deSilva `:5845` uses the Parallax name correctly, and the remainder are our own cover title and a
CHANGELOG font note.

### F-280 — `pnut_ts` survives in 16 masters as a command that does not run. `PARTIAL — the whole declared sweep APPLIED in opus-master 2026-08-25 («#301»); publication owed, per document`

**Found:** 2026-08-17 during the P2AN001/P2AN002 voice pass («#247»), by checking the compiler name
the two notes hand the reader against the name of the binary that exists.

**This was already adjudicated and only half-swept.** Commit `c203fa52` (2026-08-11) established the
finding on its merits: `command -v pnut_ts` finds nothing, the installed binary is `pnut-ts`, and the
tool's own usage banner reads *"PNut-TS: Usage: pnut-ts [optons] filename"*. SSDB and the PNut-Term-TS
guide were corrected then — 21 sites — and both voice guides were amended so it could not come back.
**The rest of the set was never swept.** Thirty-three occurrences remain across eighteen files, against
thirty-nine correct ones — a near-even split, so the set currently teaches both.

**Fixed in this pass (2 sites, the two notes being touched):** `P2AN001/opus-master/CHANGELOG.md:37`
and `P2AN002/opus-master/CHANGELOG.md:35`. Both are reader-facing — an app-note CHANGELOG is promoted
to the published `p2anNNN-changelog.md` beside its PDF.

**Remaining (31 sites, 16 files) — the class-wide sweep this finding owns:**

| Element | Sites |
|---|---|
| Getting Started Guide | `getting-started-body.md` ×1 — **highest reader risk**: a beginner's first compile |
| Architect's Guide | `architect-guide-body.md` ×1, `CHANGELOG.md` ×2 |
| ~~Assembly Language Manual~~ | ~~`CHANGELOG.md` ×1~~ — **CLEAR, verified 2026-08-22**: `pnut_ts` appears nowhere in `opus-master/`. (Its three *process* docs carried 10 tool-invocation uses; corrected the same day. The remaining hits in `audit/`, `archive/` and `code-validation/` are frozen records, and `external-inputs/pnut_ts_facts/` is a real path — all correctly left alone.) |
| PNut-Term-TS Guide | `CHANGELOG.md` ×1 (the body was swept at `c203fa52`; its CHANGELOG was missed) |
| deSilva | `archived-2025/README-COMBINED-MASTER.md` ×3 — **archived scaffolding, not shipped; excluded** |
| P2AN003 – P2AN007 | body ×17, `CHANGELOG.md` ×5 |

**Not swept here on purpose.** Conform-on-touch: these elements are not being touched by Sprint 2, and
pulling sixteen masters into a voice pass is the big-bang sweep the rule exists to avoid. Each takes it
at its next visit — this row is what makes sure the visit knows.

**The correction is one substitution** — `pnut_ts` → `pnut-ts` — with no prose consequence. Check each
site is the *command*; the project name in running text is properly **PNut-TS**.

> **SWEEP APPLIED 2026-08-25 («#301»). The conform-on-touch deferral above is discharged: the visit
> came.** All 27 reader-facing occurrences substituted across **14 files**, line counts unchanged
> (4,907 before and after), diff is exactly 27 insertions / 27 deletions.
>
> **⚠️ The row header's own arithmetic was wrong, and re-measuring it is how the extra defect turned
> up.** It reads *"Remaining (31 sites, 16 files)"*; the table under it sums to **30 sites / 15
> files**, because the `~~Assembly Language Manual~~ CHANGELOG ×1` row was struck through as CLEAR on
> 2026-08-22 and the header was never re-totalled. Measured on disk today: **30** occurrences across
> **15** files under `opus-master/`, of which **3** in **1** file are the excluded deSilva
> `archived-2025/README-COMBINED-MASTER.md` — leaving **27 in 14**, which is what was fixed. The
> table's per-element counts were all correct: Getting Started ×1, Architect body ×1 + CHANGELOG ×2,
> PNut-Term-TS CHANGELOG ×1, P2AN003–007 body ×17 + CHANGELOG ×5.
>
> **A second wrong name rode along on one of the lines, and is fixed with it.**
> `pnut-term-ts-user-guide/opus-master/CHANGELOG.md:106` carried *"`pnut_ts` + `pnut_term_ts`"* —
> **both** underscore forms, in the guide whose own `MANUAL-DESCRIPTOR.md:28` and `voice-guide.md:83`
> declare *"the underscore forms `pnut_ts` / `pnut_term_ts` are wrong and no such executable is
> installed."* `command -v pnut-term-ts` finds nothing under that spelling either; the installed
> binary is `/usr/local/bin/pnut-ts`. Corrected to `pnut-term-ts` in the same pass — leaving it would
> have fixed half a sentence.
>
> **Every site was checked for sense, not just substituted** — this finding requires it ("check each
> site is the *command*"). Counted off the pre-edit backups: **23 of the 27 are inside backticks**
> (13 as `` `pnut_ts -d` ``, 10 as bare `` `pnut_ts` ``), unambiguously the command. The **other 4**
> are the compound adjective *"pnut_ts-verified"* — `architect-guide/CHANGELOG.md:102` and `:114`,
> `architect-guide-body.md:19`, `getting-started-body.md:17`. Those are the one shape where this
> finding says **PNut-TS** might be proper instead; they were still taken to `pnut-ts` because
> "verified by running it" names the *binary*, and that is the form already shipping in running text
> at `p2-assembly-language-manual/opus-master/CHANGELOG.md:196` ("348 code examples audited with
> pnut-ts v1.51.7"). Two of the four (`architect-guide-body.md:19`,
> `getting-started-body.md:17`) sit inside the masters' `<!-- CONVENTIONS -->` authoring comments and
> reach no reader — corrected anyway, because a convention block that names a non-existent binary is
> how the next author reintroduces it. The result matches the form P2AN001/P2AN002 already ship
> (`P2AN001/opus-master/P2AN001.md:622`, `P2AN002/opus-master/P2AN002.md:357`), so the set no longer
> teaches both spellings. `grep -c pnut_ts` over `manuals/*/opus-master/` + `app-notes/*/opus-master/`
> is now **0** outside `archived-2025/`.
>
> **Deliberately NOT swept, and why:** the 3 sites in
> `p2-pasm-desilva-style/opus-master/archived-2025/README-COMBINED-MASTER.md` — archived scaffolding
> that ships to nobody, excluded by this finding's own table. Frozen records under `audit/`,
> `archive/` and `code-validation/`, and the real path `external-inputs/pnut_ts_facts/`, are likewise
> untouched.
>
> **Gates:** `audit-code-line-length.py --budget 76` and `audit-inline-code-ascii.py` exit 0 on all
> 14 files. **No occurrence was inside a code fence** — verified by mapping every changed line number
> against the files' fence ranges — so no example file changed, byte-identity is untouched, and
> `pnut-ts` compilation does not apply to this finding.
>
> **What remains is publication, not authorship.** Nine reader-facing documents now carry the
> correction in source and none of them has been re-released: Getting Started, Architect's Guide,
> PNut-Term-TS Guide, and P2AN003–P2AN007. Each ships it at its next release. **This is not a render
> gate** — a token substitution has no layout consequence — so «#302» need not look at it; it is a
> release-wave item.

### F-282 — every `MANUAL-DESCRIPTOR.md` records a stale `last_published_tag`, so every diff-since-published audit reads the wrong baseline. `RESOLVED` — **the whole fleet corrected and the guard's own blind spot closed 2026-08-25 («#302»)**

> **CLOSED 2026-08-25 («#302») — both halves, measured against `git tag` rather than against any
> file's own claim.**
>
> **(a) Eight descriptors were still stale at HEAD, and seven of them were invisible to the check
> built to catch this.** Measured before any edit:
>
> | Element | Descriptor said | Actually tagged | |
> |---|---|---|---|
> | Assembly | `…-v3.1.6` | **`…-v3.1.7`** | 1 release behind |
> | P2AN001 | `unreleased` | **`p2an001-v1.0.4`** | whole doc read as unreviewed |
> | P2AN002 | `unreleased` | **`p2an002-v1.0.3`** | ” |
> | P2AN003 | `unreleased` | **`p2an003-v1.0.2`** | ” |
> | P2AN004 | `unreleased` | **`p2an004-v1.0.2`** | ” |
> | P2AN005 | `unreleased` | **`p2an005-v1.0.2`** | ” |
> | P2AN006 | `unreleased` | **`p2an006-v1.0.1`** | ” |
> | P2AN007 | `unreleased` | **`p2an007-v1.0.1`** | ” |
>
> All eight advanced, each with its trailing comment rebuilt from git — `git log -1 --format=%ad`
> for the date and `git show <tag>:…pdf | pdfinfo -` for the page count, never from memory or the
> roster, because *a stale comment beside a corrected value is the same defect wearing a disguise*.
> The two genuinely-unreleased seeds (Single-Step Debugger, PNut-Term-TS) correctly carry an empty
> value and were left alone. **All 17 descriptors now match.**
>
> **(b) THE DURABLE GUARD HAD THE SAME HOLE THE FINDING DESCRIBES.** `release-manual`'s
> project-overlay added the Phase-3 advance and a fleet-verification loop — but that loop globs
> `manuals/*/MANUAL-DESCRIPTOR.md` **only**, so all seven app-note descriptors sat outside every run
> of it, and it keys a **case-sensitive** `grep "^$slug-v"` off an uppercase directory (`P2AN001`)
> against a tag namespace that went lowercase at the 2026-07-12 fleet release — the exact
> case-split this finding already identified as what produced its own original wrong filing. Run as
> written it reported **one** stale element; run corrected it reports **eight**. A fleet check that
> cannot see part of the fleet exits 0 and proves nothing.
>
> Both defects fixed in the `release-manual` skill overlay (agent-side): the glob now covers
> `app-notes/*/` and the lookup is `grep -i`, with the reasoning recorded inline so neither is
> re-simplified away.
>
> **Proven able to fail (F3).** After the fix the corrected sweep reports **no** stale elements; a
> negative control that reverted P2AN006 to `p2an006-v1.0.0` made it fire —
> `STALE P2AN006: 'p2an006-v1.0.0' vs 'p2an006-v1.0.1'` — and the file was restored. A check that
> cannot fail has not been verified, it has been run.

> **Wave descriptors fixed 2026-08-17**, each checked against `git tag` rather than against the file's
> own claim: Debug Window `v1.0.0`→**`v1.1.2`**, IOSP `unreleased`→**`v1.0.8`**, Assembly
> `v3.1.2`→**`v3.1.5`**. Their trailing baseline comments described the OLD tags (wrong dates, wrong
> page counts, one still calling IOSP a maiden release) and were rewritten to the real released dates
> and page counts. **A stale comment beside a corrected value is the same defect wearing a disguise.**
> Descriptors outside the wave are untouched and still stale.

> **Rewritten in place 2026-08-17, hours after it was filed.** The original text claimed the app-note
> *tags* were two to three releases behind and that the app-note release path "never lays the tag."
> **That was wrong, and the error was in the probe, not the repo.** The scan grepped for the
> uppercase prefix `P2AN001-`, but the app-note tag namespace switched to **lowercase** at the
> 2026-07-12 fleet release. `p2an001-v1.0.3`, `p2an002-v1.0.2`, `p2an003-v1.0.2`, `p2an004-v1.0.2`
> all exist, and `git for-each-ref --format='%(creatordate:short)'` shows each was created **on its
> release date** — not retroactively. Every app note and every manual is tagged current. The
> conclusion "specific to the app-note release path" was false in both halves.
>
> The *symptom* the finding described is real. The cause is below.

**Found:** 2026-08-17, enumerating what was pending for release alongside Debug Window and IOSP.
**Corrected the same day**, when preparing the six-element wave put the actual tag list on screen.

**The tags are complete.** Every released version of every manual and app note has a tag at the
commit that shipped it. Nothing is owed here.

**The descriptors are stale.** `document-audit`'s changeset-integrity dimension (Dimension #15) does
not read `git tag` — it reads the `last_published_tag:` field in each `MANUAL-DESCRIPTOR.md`. Those
fields were written at seed time and never advanced by a release:

| Element | Descriptor says | Actually released + tagged | Baseline error |
|---|---|---|---|
| P2AN001 | `unreleased` | **1.0.3** | whole doc reads as unreviewed |
| P2AN002 | `unreleased` | **1.0.2** | whole doc reads as unreviewed |
| P2AN003 | `unreleased` | **1.0.2** | whole doc reads as unreviewed |
| P2AN004 | `unreleased` | **1.0.2** | whole doc reads as unreviewed |
| Assembly | `v3.1.2` | **3.1.5** | 3 releases of published work |
| Streamer | `v1.0.6` | **1.0.8** | 2 releases |
| deSilva | `v3.0.1` | **3.0.5** | 4 releases |
| Debug Window | `v1.0.0` | **1.1.2** | 5 releases |
| XBYTE | `none` — "NOT yet released" | **1.0.1** | whole doc reads as unreviewed |

So this is **not** an app-note problem. It is fleet-wide, and it is worse on the manuals than on the
app notes — the opposite of what the original finding said.

**Why it bites.** With the recorded baseline several releases behind, the audit diffs against content
that shipped months ago and reports **already-published work as unreviewed change** — noise that
trains the reader to skip the signal. It fails in a direction that looks like diligence.

**A second, smaller defect, and the one that caused the misdiagnosis:** the app-note tag namespace is
**case-inconsistent** — `P2AN001-v1.0.0`/`-v1.0.1` uppercase, `p2an001-v1.0.2` onward lowercase. Any
case-sensitive lookup of a "latest tag" silently resolves to the pre-July tag. That is what made the
original probe read three missing releases that were never missing.

**Fix:** (a) advance every `last_published_tag:` to the element's actually-released tag, and make
advancing it a step in `release-manual` so it cannot drift again; (b) settle the app-note tag case
one way and treat lookups as case-insensitive until it is. No tags need to be created.

**Lesson, recorded because it cost a wrong finding:** the probe's *absence of a result* was read as
a fact about the repository. A grep locates; it never concludes. This is the same failure mode as
"a status line is not evidence," and it was caught only because a later task put the full `git tag`
output on screen for an unrelated reason.

---

## Published PDFs carry no machine-readable rights (2026-08-21) — F-316

### F-316 — every published PDF states CC BY-SA 4.0 and a joint copyright on its own page, and carries neither in its metadata. `PARTIAL — mechanism DONE and PROVEN 2026-08-22; adoption is per document`

**How it surfaced.** Stephen, reading the Streamer v1.1.0 metadata at the «#287» gate, asked whether
the PDF's rights should name both companies. The `Author` field is correct as written — Iron Sheep
Productions is the author, and authorship is not copyright — but the question exposed that the
copyright and licence are **absent from the metadata entirely**.

**Measured on the returned v1.1.0 PDF:**

```
Title:            P2 Streamer Programming Guide
Subject:          Comprehensive Reference for Propeller 2 Streamer Hardware
Author:           Iron Sheep Productions, LLC
Custom Metadata:  no
Metadata Stream:  no          <- no XMP at all
```

while `front-matter.md:112` reads *"Copyright © 2026 Iron Sheep Productions, LLC and Parallax Inc."*
and the page below it grants **CC BY-SA 4.0**. Nothing in
`platform/templates/p2kb-platform-foundation.sty` sets `pdfkeywords`, and `hyperxmp` is not loaded,
so no `dc:rights` is emitted.

**Why it matters more than its size suggests.** CC BY-SA exists to be machine-readable. An
aggregator, a search index or a model crawler reading these files sees a document with no licence —
so a deliberately-open set reads as unlicensed, which is the opposite of the intent.

**The split is real, and the fix must respect it.** Surveyed 2026-08-21 across every manuscript:

| Population | Count | Copyright line |
|---|---|---|
| Manuals, guides and all 7 app notes | 17 | Iron Sheep Productions, LLC **and Parallax Inc.** |
| `pnut-term-ts-user-guide` | 1 | Iron Sheep Productions, LLC **only** |
| `Donna-Manuscript` | 1 | private, separate author — out of scope |
| `p2-layout-torture-test` | 1 | instrument, no copyright page — out of scope |

So the string **must be single-sourced per document from `request.json`**, never hardcoded in the
platform. A platform constant would silently attribute Parallax to the one document they have no
part in — precisely the class of defect the metadata single-sourcing work («#283») was built to end.

**Proposed correction.** Two new `request.json` metadata keys (`copyright`, `license`), consumed the
way `\DocTitle` / `\DocAuthor` already are. Emit through `\hypersetup{pdfkeywords=…}`, which needs no
new package; add XMP `dc:rights` via `hyperxmp` **only if** the Forge's TeX Live carries it — that is
unverifiable from the container and must be probed on the interactive daemon rather than discovered
in a production build.

**Sequencing — IN THIS WAVE. Stephen's call, 2026-08-21, overriding a first recommendation to
defer it.** The initial reasoning was that a platform change invalidates the built Streamer PDF and
everything queued behind it. That is true and it is the wrong trade: **this wave is the metadata wave
by design** — «#283» converted identity strings to platform single-sourcing and this release is the
first time the full metadata set reaches the documents. Deferring rights to a later adoption round
means a SECOND metadata round-trip for every document, and an interval in which every published PDF
carries half its metadata. One round-trip, complete, is cheaper and correct. Get it right the first
time it ships.

**Not a manuscript defect.** Every copyright page is already correct and states both parties where
both apply. Nothing in any master needs editing.

**Status:** `PARTIAL — the mechanism is DONE and PROVEN on a returned PDF; the other 17 documents adopt at their next render.`

> **PROVEN 2026-08-22 on the returned Streamer v1.1.0 PDF — read from the artifact, not the log.**
> `Keywords` now reads *"Copyright 2026 Iron Sheep Productions, LLC and Parallax Inc.; licensed
> under CC BY-SA 4.0"*. `\DocCopyright`/`\DocLicense` join the `\Doc*` family, fed per document
> from its own `request.json`.
>
> **The build is byte-stable**: 91 pages, 24,737 words, and **ZERO pages whose text differs**
> from the pre-rights build — which is what a guarded metadata-only platform change should
> produce, and is now measured rather than assumed.
>
> **Two defects were caught by arming the gate against the returned build**, both mine, and both
> would have shipped: the first emitted string read *"Parallax Inc.. Licensed under"* because the
> template appended a full stop to a value that already ended in one (now a semicolon, fixed in
> the platform so none of the 17 documents still to adopt inherits it); and the gate itself was
> checking only that SOMETHING rights-shaped was present, never that the declared values actually
> arrived. It now verifies each one round-tripped. That is the second time in one day this gate
> passed on intent rather than artifact — worth remembering as a shape, not an incident.
>
> **Owed:** the other 17 documents, tracked in `PLATFORM-FEATURE-ADOPTION.md`'s new Rights column;
> and XMP `dc:rights`, which needs `hyperxmp` and stays gated on confirming that package exists in
> the Forge's TeX Live rather than assuming it. `Keywords` is the carrier today.

> **ADOPTION MEASURED ON THE ARTIFACTS, 2026-08-25 («#302»).** `pdfinfo` over all 15 files in
> `deliverables/documents/DOCs/`: **2 carry a rights `Keywords` string, 13 carry none.**
>
> - **Assembly Reference** — *"Copyright 2025-2026 Iron Sheep Productions, LLC and Parallax Inc.;
>   licensed under CC BY-SA 4.0"*
> - **Streamer Guide** — *"Copyright 2026 Iron Sheep Productions, LLC and Parallax Inc.; licensed
>   under CC BY-SA 4.0"*
> - **EMPTY:** Getting Started · I/O & Smart Pins · DeSilva · Debug Window · Architect's Guide ·
>   XBYTE · P2AN001…P2AN007
>
> Both adopted strings use the **semicolon** form, so the *"Parallax Inc.. Licensed under"*
> double-stop defect is confirmed absent from everything that has shipped — the platform fix held,
> and none of the 13 still to adopt can inherit it.
>
> **The `pnut-term-ts-user-guide` split is intact and is the reason this must never become a
> platform constant:** its row is ✅ in the adoption table with the ISP-only string, distinct from
> the 17 joint-copyright documents.
>
> **Two things remain owed, and NEITHER can be discharged in this container:**
> 1. **13 published documents adopt at their next render** on `EXEC_ENV_CANONICAL`.
> 2. **XMP `dc:rights` stays gated on whether `hyperxmp` exists in the Forge's TeX Live** — a probe
>    on the interactive daemon, Stephen's side. Until then `Keywords` is the carrier and
>    `Metadata Stream: no` is expected, not a defect. **Do not "fix" this by loading `hyperxmp`
>    speculatively in a production build.**

---

## Nine documents carry a request.json subtitle their own cover contradicts (2026-08-22) — F-317

### F-317 — the subtitle in `request.json` disagrees with the printed cover in 9 of 15 published documents, and adopting metadata single-sourcing is what makes that visible. `CONFIRMED` — **all 9 re-measured 2026-08-25 («#302»): unchanged, still drifting, none adopted**

**How it surfaced.** Stephen: *"fix README if needed, always."* Sweeping the public index's
subtitle lines against the PDFs found 10 apparent mismatches — but checking them against
`request.json` was the wrong comparison, because **`request.json` only reaches the PDF for a
document that has ADOPTED metadata single-sourcing**, and only three have. Re-run against the
**printed cover**, the picture inverted: the README was right in almost every case, and it is
`request.json` that is out of step.

**The real defect, and it is latent rather than shipped.** For an unadopted document
`request.json`'s subtitle reaches nothing, so the disagreement is invisible. The moment that
document adopts — `\DocSubtitle` → `pdfsubject` — that string **becomes the PDF's Subject** and
contradicts the subtitle printed on its own cover. **This already happened once**: «#283» hit it
on the Streamer Guide, and the rule recorded then is **the cover wins**.

| Document | `request.json` subtitle | printed cover says |
|---|---|---|
| `p2-pasm-desilva-style` | Build, Experiment, and Master the Propeller 2 | A Human-Centered Approach to Parallel Processing |
| `p2-debug-window-manual` | See What Your Program Is Doing — Nine Display Windows for the Propeller 2 | See What Your Program Is Doing |
| P2AN001 | Application Note P2AN001 — No External ADC | Measure an Absolute Voltage in Microvolts on a P2 Pin |
| P2AN002 | Application Note P2AN002 — Hardware Math on the P2 | CORDIC for Real Work |
| P2AN003 | Application Note P2AN003 — No External DAC | Generate Analog Waveforms and Audio on a P2 Pin |
| P2AN004 | Application Note P2AN004 — No External Counter or ADC | Read Real-World Sensors by Frequency, Rotation, and RC Timing on a P2 Pin |
| P2AN005 | Application Note P2AN005 — Run Several Jobs in One Cog | Cooperative Multitasking with Spin2 TASK Methods |
| P2AN006 | Application Note P2AN006 — Size Every Stack, Catch Every Overflow | Sizing Cog & Task Stacks |
| P2AN007 | Application Note P2AN007 — STRUCT Records, Shared Safely Across Cogs | Data Structures with the New Language Facilities |

**Correction.** Before each document adopts metadata single-sourcing, bring its `request.json`
subtitle to the string its cover prints — **the cover wins**, per «#283». Doing it at adoption
time is the natural moment: that is the render where the value first matters, and
`audit-pdf-metadata.py` will compare the Subject against `request.json` on the returned PDF, so a
wrong value fails the gate rather than shipping. For the seven app notes, note their cover puts a
*descriptive line* under the title — decide per document whether that line or the catalog tagline
is the subtitle, rather than sweeping one reading across all seven.

**Also fixed here (2026-08-22):** the public index's bold line for the Streamer Guide read *"A
Guide to the Propeller 2 Streamer, Its Modes and Function"* while the document it links to prints
*"Comprehensive Reference for Propeller 2 Streamer Hardware"*. That one WAS shipped drift — the
catalog misdescribing the download — and is corrected. Every other index line was verified against
its cover and is correct; the app notes deliberately use `Application Note P2ANxxx · <topic>` as an
index label while their **heading** carries the cover's title, which is a consistent scheme, not
drift.

> **RE-MEASURED 2026-08-25 («#302») — all nine `request.json` subtitles read off disk: every one is
> UNCHANGED from the table above. The drift is intact, and none of the nine has adopted.** So the
> defect is still latent rather than shipped, exactly as recorded — but see the sharpening below,
> which changes when it stops being latent.
>
> ⚠️ **`pdfsubject` IS wired, so "latent until adoption" now means "fires at the very next
> adoption".** This entry was written while F-300 step 4 said *"Do NOT wire `pdfsubject`"*. The two
> adopted PDFs measured today both carry a populated `Subject` (Assembly: *"Complete PASM2
> Instruction Set Documentation"*; Streamer: *"Comprehensive Reference for Propeller 2 Streamer
> Hardware"* — the **cover** string, i.e. «#283»'s cover-wins rule already applied). Neither is in
> the drift table, which is why nothing has shipped wrong yet. **That is luck of ordering, not a
> guard.** The next of the nine to render will publish its `request.json` subtitle as the PDF
> Subject and contradict its own cover.
>
> **So the correction is now a PRE-RENDER step, not a same-render one:** bring the `request.json`
> subtitle to the cover string **before** staging that document, and let `audit-pdf-metadata.py`
> confirm it on the returned PDF. The seven app-note rows still need the per-document decision this
> entry calls for (cover descriptive line vs catalog tagline) — **do not sweep one reading across
> all seven.**

**Status:** `CONFIRMED — resolve each document's subtitle to its printed cover BEFORE the render that adopts metadata single-sourcing; all 9 rows verified still drifting 2026-08-25.`

## Open — enhancement proposals (new content, not corrections)

- **ENH-03 — a gating compile step for every code block in `deliverables/ai/P2/`.** *Filed 2026-08-21;
  Stephen's call, and he asked for it in these words: "we must, for all code in YAML files, compile
  that code and assure ourselves that it compiles correctly. We do not publish a release unless all
  the code publishes correctly."* Nothing in this project compiles KB code examples, which is how
  F-311…F-313 and F-315 shipped. **Census: 1913 code-shaped blocks across 438 files; only 118 are
  complete programs, so 1795 need a synthesized context.** Design points already settled:
  - **The blocker is not the compiler, it is that the KB never declares which strings are code.** A
    heuristic sweep pulled 166 of 541 PASM2-shaped blocks out of *prose* fields. So the first
    deliverable is a per-block marker — `compile: program` / `compile: fragment` /
    `compile: never` + reason — not a runner. A guessing gate cries wolf, and a gate that cries wolf
    gets ignored.
  - **`compile: never` must be ASSERTED TO FAIL**, not skipped. The KB teaches anti-patterns; a
    wrong-code example that quietly starts compiling means the wrongness was edited away.
  - **It proves LEGALITY, not correctness**, and must never be cited otherwise. F-312 is the proof:
    fixing `qvector y_val` so it assembles would have left X and Y still swapped.
  - **No build stamps** (PL-004). The gate runs against whatever compiler is installed; a bump that
    breaks something turns the release red, which is the gate working. That is also what makes the
    surviving `re-verify on a compiler version bump` notes deletable.
  - Prototype validated 2026-08-21: it asks the compiler which identifiers are declarable rather than
    carrying a keyword list that would rot. 4/4 known-bad caught, 4/4 known-good passed. Its known
    weakness is auto-declaration colliding with symbols a block defines itself, which produced
    `Symbol is already defined` on blocks that compile correctly by hand — fix that before trusting
    any pass-rate number from it.
  - Hooks: `release-yamls` as a hard gate (~0.8 s/block, ~25 min full sweep), and
    `yaml-knowledge-base-maintenance` on touched files so it fails at edit time, not release time.

- **ENH-02 — make the platform fail loudly on a code line that cannot fit.** *Filed 2026-08-21 when F-281 closed.* F-281's three over-wide lines were fixed and v1.1.3 shipped margin-clean, but **nothing stops the class recurring**: `p2kb-platform-code-coloring.lua` emits `\begin{Verbatim}[xleftmargin=-10pt]` with no break options at all ten sites, and the `breaklines=true` at `p2kb-platform-foundation.sty:317` is a pre-existing `\lstset` that the Verbatim path never consults. So an over-long line silently runs off the page and the compile log stays clean — the exact shape of every render defect this project has shipped. The source-side `audit-code-line-length.py` gate catches most of it, and `audit-pdf-margin-overflow.py` catches it after the fact; what is missing is the platform refusing to typeset it. Not a defect in any document — an absent guard.

- **ENH-01 — Harvest the Architect's Guide *project front-end* into a new KB node set.** *Scheduled
  2026-07-08 (deferred from the Architect's Guide v1.0.0 release); Stephen go/no-go before authoring.*
  Source: *The P2 Architect's Guide* v1.0.0, **Part I (Act I)**. The decomposition-reasoning layer
  (`architecture/decomposition/`) begins *at* "which cog owns what"; nothing in the KB captures the
  **pre-decomposition** front-of-project work Part I lays out. Candidate new node set — reusable P2
  **design-process** patterns that sit *above* the decomposition layer: feasibility-before-design ·
  **narrow-vs-broad comms selection** (I²C/SPI vs host-style ribbon) · **offload-vs-port /
  companion-device partitioning** · pin-budget → adapter-board · "characterization becomes the spec" ·
  firmware-loaded-device → loader. Also a small KB touch worth doing: **performance → P2-resource
  mapping** (which performance need → LUT RAM / PSRAM / CORDIC / streamer — Architect's Guide Act III
  P-7). **Do NOT harvest the Act III agentic principles** (about *using agents*, not the P2 — low KB
  value). Fuller rationale table lives in the manual's `PLANNING.md` (KB-harvest proposals).

---

## Open — TRACKED in the ingestion head (resolution lives there, not in a YAML edit)

- **F-123 — TAQOZ-Forth / ROM-Monitor capability detail rests partly on preliminary web research.** `TRACKED → ingestion` Grounding plan in `engineering/ingestion/sources/taqoz/taqoz-content-gaps-and-grounding-plan.md` (mine `ROM_Booter.lst`; verify vs Peter Jakacki's `TAQOZ.spin2`).
  > **Routing re-verified 2026-08-25 («#300») — still live, and one of its two inputs is missing.** The
  > routing target resolves: the grounding plan exists at the path above, and the first input is in hand —
  > `engineering/ingestion/sources/rom-booter/ROM_Booter.lst` **and** `rom_booter_v33_01j.lst` are both
  > present (the `v33_01j` copy is the one E-005 cites, so it is the mined edition). **The second input is
  > NOT in hand:** no `TAQOZ*.spin2` exists anywhere in the repo, so the *"verify vs Peter Jakacki's
  > `TAQOZ.spin2`"* half cannot run today. **What would settle it:** obtain Jakacki's `TAQOZ.spin2` source;
  > until then the ROM-monitor half is groundable from `ROM_Booter.lst` alone and the Forth-vocabulary half
  > is not. Stays `TRACKED → ingestion` — the preliminary web-research material
  > (`taqoz-web-research-preliminary.md`) remains community-tier and is still not citable.

---

## P2KB YAML corrections

> **Sweep origin (2026-06-13):** surfaced while auditing the Debug Window Manual's
> examples against the DEBUG display windows KB. Ground truth used is the **v55 Spin2
> documentation primary source** (`engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt`,
> the per-window directive tables at lines ~1118–1417), which revealed the v1.8.0/v1.9.0
> reconciled `debug-displays/*.yaml` carry several errors/omissions vs that source. All
> findings below are CONFIRMED against the v55 primary source. The manual was, in several
> cases, MORE correct than the YAML.

> **✅ AUTHORITY CORRECTION — RESOLVED (2026-06-14).** The findings below were originally
> derived using the v55 **published documentation text** as authority. That was the wrong
> order: the **Pascal source** (`DebugDisplayUnit.pas`) is ground truth, and the
> `DEBUG-WINDOW-DIRECTIVE-MATRIX.md` (+ per-window theory-of-operations docs) are
> Pascal-derived — the published text is the derivative that carries the off-by-ones. The
> matrix + theory-of-operations were **re-audited against the Pascal source and re-imported**
> (2026-06-14, `REF/` under `p2-debug-window-manual`). The full analysis was **rerun against
> the matrix as authority** and the findings applied/closed below. Net outcome: in the
> majority case the matrix was right and the YAML already matched it (→ `RESOLVED-INVALID`);
> a smaller set were genuine defects (→ `DONE`); and three NEW writing-debug-statement defects
> surfaced during the rerun (F-132/F-133/F-134, all `DONE`). Every changed example was
> compile-verified with `pnut-ts -d`.

### F-207 — packed-data feed for **scrolling** LOGIC/SCOPE windows requires a **full-window array feed** (`` `uhex_long_array_ ``); a single `` `(packed) `` long does NOT fill the window — `PARTIAL — manual DONE + HW-verified · KB DONE (v1.15.0) · one manual design decision open`

> **Heading corrected in place 2026-08-15.** It read *"KB enrichment pending"* while this entry's own
> body recorded **"KB APPLIED 2026-07-11 — PUBLISHED in KB v1.15.0. Both facets landed."** Verified
> against the YAML rather than the note: `language/spin2/debug-displays/logic.yaml` carries the
> array-feed example **and** the sub-sample-width = channel-count rule; `scope.yaml` carries the
> array feed; `language/spin2/statements/debug.yaml` carries the cross-referencing example. **No KB
> work is owed — do not re-file this as a YAML item.**
>
> **What is actually still open, and it is manual-head:** whether `ch13-packed-logic-stream` becomes
> the richer **2-channel + `LONGS_2BIT`** demo. Today's single-channel `'D0'` + `LONGS_1BIT` version
> is internally consistent and hardware-confirmed, so nothing is broken; adopting the richer form
> costs one more render. **Stephen's design call.**
>
> **Ordering caveat worth carrying:** this entry's own "verify first" note says Facet B (the
> mode↔channel-count rule) was a **peer report, not our own hardware run**, and directs us to confirm
> on silicon *before* enriching the KB — but the KB enrichment shipped in v1.15.0 regardless, so that
> order was inverted. The 2-channel render above **is** the confirming run. Until it happens, Facet B
> in the KB rests on a peer report plus how LOGIC is documented to unpack, not on our own bench.

**Surfaced:** 2026-07-11, fleet-release sweep — two published Debug Window Manual ch13 examples rendered only a fragment. **Root cause hardware-verified** the same day (Stephen ran the reshaped figure-generators; Claire read the BMPs back via image-tools).

**What's wrong (empirical ground truth):** for the **scrolling time-series** windows (LOGIC, SCOPE), feeding packed sample data as a **single** `` `(packed) `` long per message renders only a fragment — it does **not** accumulate/unpack across the window. The **only** feed that fills the window is the **full-window array feed** `` `uhex_long_array_(@buff, N) ``, which is also the **only packed example the v55/v51 docs ever show** (v55 text line ~1144 / v51 line ~1858, identical). The BITMAP (frame-buffer) window **tolerates** a per-long packed feed — which is why `ch13-packed-bitmap-frame` was always correct and was left untouched; that isolates the defect to the **feed shape for scrolling windows**, not the packing mechanism itself.
- **Pre-fix measurements:** LOGIC — data only in the last long's band (right-edge fragment). SCOPE — data only in the first few bands (left-edge fragment).
- **Post-fix hardware renders (2026-07-11 19:00, `fig-13-*_WDW.bmp`):** LOGIC = **full-width** random D0 trace (left edge, blank pre-fix, now packed with transitions); SCOPE = **two 0–255 sawtooths** (A + B), full vertical sweep. Both fixes empirically confirmed.
- SCOPE also had a 2nd defect: channel-defs lacked the **required** range → fixed to `'A' 0 255 'B' 0 255` (per the `'label' AUTO|lo hi` rule, F-137/EF-003 lineage).

**Manual — DONE (this sweep, HW-confirmed).** Fixed lockstep in opus-master `ch13-packed-data.md` + examples-library + figure-generators (byte-identical example↔code-block; corpus identity GREEN 32/32; compile clean `pnut-ts -d`): logic → `VAR buff[8]` (8 longs = 256 samples) fed via `` `uhex_long_array_(@buff, 8) ``; scope → `VAR buff[128]` array feed + the `'A' 0 255 'B' 0 255` ranges; prose gained an array-feed paragraph.

**Facet B — packing mode must match the LOGIC channel count (user-reported + HW-CONFIRMED 2026-07-11).** Stephen, exercising the *shipped* ZIP, found the (old) `packed-logic-stream` example declared **two** channels but used **LONGS_1BIT** → **all samples drew on the first channel only**; changing it to **LONGS_2BIT** made both channels display. The rule (grounded in how LOGIC unpacks): for LOGIC the packing mode's **bits-per-sub-sample must equal the channel count** — `LONGS_1BIT` = 1 channel, `LONGS_2BIT` = 2, `LONGS_4BIT` = 4, `LONGS_8BIT` = 8; each sub-sample carries one bit **per channel** per time-step. (SCOPE differs: an 8-bit-packed SCOPE sub-sample is a full per-channel *value*, and channels interleave across consecutive sub-samples — cf. `ch13-packed-scope` = 2 channels A/B via `LONGS_8BIT`.) Our reshaped `ch13-packed-logic-stream` currently sidesteps this by using a **single** channel `'D0'` + `LONGS_1BIT` (consistent, HW-confirmed) — the shipped bug cannot recur in it — but the richer, on-intent demo is 2 channels + `LONGS_2BIT` (design decision open with Stephen; would need one more render).

**KB — enrichment pending (the class-wide/systemic angle → yaml head).** The shipped KB documents the packing **modes** (`debug-displays/logic.yaml:37`, `scope.yaml:39`) and the concept ("packed-data modes let you pack multiple sub-samples", `logic.yaml:88`), and `statements/debug.yaml` shows the normal per-sample feed — but **no KB file shows the packed full-window feed**, states the single-`` `(packed) ``-long-won't-fill-a-scrolling-window fact, **or ties the packing mode to the channel count** (`logic.yaml:38` only covers the multi-bit-*bus* `count` field, not mode↔channel-count). A remote agent generating packed LOGIC/SCOPE code from the KB would reproduce both the fragment defect and the all-on-channel-0 defect.

**Proposed KB action:** (1) add a **packed full-window array-feed example** to `debug-displays/logic.yaml` and `debug-displays/scope.yaml` (and the packed-mode note in `statements/debug.yaml`) — `` `uhex_long_array_(@buff, N) `` matching v55's only packed example — plus the caveat: *a single packed-long feed advances the scrolling window by one column only; the full window requires the array feed* (BITMAP is exempt). (2) Document the **mode↔channel-count** rule in `logic.yaml` (LONGS_NBIT ⇒ N one-bit channels) and the SCOPE value-interleave form in `scope.yaml`.

> **KB APPLIED 2026-07-11 — PUBLISHED in KB v1.15.0.** Both facets landed. `logic.yaml` — `packed:` gains the
> sub-sample-width = channel-count rule (Facet B) + a new LONGS_2BIT full-window array-feed example
> and an array-feed/unpack note (Facet A, unpack semantics quoted from v55 L1143/L1406). `scope.yaml`
> — `packed:` gains the per-channel-value interleave form (Facet B) + a LONGS_8BIT array-feed example
> and left-edge-fragment caveat (Facet A). `statements/debug.yaml` — a packed scrolling-window
> array-feed example cross-referencing both. D2 (Stephen): essential feed-shape snippet, NOT the
> verbatim v55 streamer example (incidental + misleading re streamer-required); unpack semantics
> quoted verbatim.

**Verify first (at fix time, §4.5):** open v55 text line ~1144 (and the REF Pascal-derived matrix / `DebugDisplayUnit.pas SetPack`) and match wording exactly — do not paraphrase. Facet A's feed-shape claim is grounded in the 2026-07-11 hardware renders + v55 showing only the array form. **Facet B is a peer report (Stephen), not yet our own hardware run — confirm on silicon before enriching the KB** (empirical > documentary); the LONGS_2BIT 2-channel render, if we adopt that example, IS that confirmation.

### F-208 — PLOT POLAR orientation (θ=0 baseline direction) is undocumented; the rotation-sense wording is murky/likely-wrong — `CONFIRMED` (Test J)

**Surfaced:** 2026-07-11 — Test J had to be run to *learn* the POLAR orientation because it is documented nowhere. Per the **test-to-learn = doc/KB gap** rule (Stephen's call this date), the learned fact must be written back into both the KB and the manual, not consumed once.

**What's wrong / missing:**
- **θ=0 baseline direction is documented NOWHERE** — neither `debug-displays/plot.yaml` nor ch05-plot.md states where angle 0 points. Test J resolved it: **θ=0 → East (+x); increasing θ is counter-clockwise** (math convention); no flip.
- **Rotation-sense wording is murky/likely-wrong:** `plot.yaml:62` — *"twopi -1/0 select clockwise/counter-clockwise sense."* The default `twopi` is `$1_0000_0000` (positive → CCW), **not** 0; and the "-1/0" shorthand fails to convey the actual rule — a **negative** `twopi` reverses to clockwise.

**Evidence:** Test J (`conflict-testJ-polar-theta0`, both platforms 2026-07-11): sampling ρ≈150 from origin — **East=RED (0°)**, North/up=GREEN (90°), West=BLUE (180°), South=YELLOW (270°) → θ=0 East, CCW. Recorded in `audit/v55-vs-REF-reconciliation-2026-07-10.md`; EF entry pending (§7.6 / #196).

**Proposed correction (KB → yaml head):** in `plot.yaml` POLAR directive, state that **θ=0 points East (+x)**; the default (positive `twopi`) sense is **counter-clockwise**; a **negative `twopi` reverses to clockwise**. Replace the `"twopi -1/0"` shorthand with that sign-based rule.

> **YAML APPLIED 2026-07-11 — PUBLISHED in KB v1.15.0.** `plot.yaml:62` POLAR now reads "*Orientation:
> theta=0 points East (+x); with the default (positive) twopi the angle increases counter-clockwise;
> a NEGATIVE twopi reverses the sweep to clockwise*" — the murky `"twopi -1/0"` shorthand is gone.
> Manual side already applied (#195). Grounded EF-032/Test J.

**Manual side (→ ch05-post #195-C):** add the same orientation fact to the ch05-plot.md POLAR section — re-scoped from "optional enhancement" to **required gap-fill**.

**Grounding:** Test J (empirical > documentary). Cite the EF once promoted.

> **KB HALF RE-VERIFIED ON DISK 2026-08-25 («#300») — DONE, and richer than the entry proposed. No KB work
> is owed.** Read at the file, not from the status note above:
> `deliverables/ai/P2/language/spin2/debug-displays/plot.yaml:62` now carries **both** repairs this finding
> asked for, plus a distinction the proposal did not make:
> *"twopi = full-circle units (default $100000000): **0 => +$100000000** (default, counter-clockwise
> winding), **-1 => -$100000000** (reversed, clockwise winding) — **0 and -1 are NOT equivalent**; any other
> value is taken literally (e.g. 360 = degrees). **Orientation: theta=0 points East (+x)**; positive twopi
> increases theta counter-clockwise, negative twopi clockwise."*
> The murky `"twopi -1/0"` shorthand this finding named is gone, θ=0 is stated, and the sign-based rule
> replaced it. **Status stays `CONFIRMED` only because the manual half is still owed** — routed to «#301»,
> which owns the ch05-plot.md POLAR section. **This entry is not a KB item; do not re-file it as one.**

## Systematic `P_*` constant-name audit (2026-07-01) — F-177…F-183

> **Origin & method (Stephen's call).** After F-174/175/176 kept surfacing fictitious `P_*`
> constants ad-hoc, we ran a **corpus-wide audit** to make it the last time. Method: the
> **legality arbiter is `pnut-ts` v1.55** (our authority order: compiler → v55 doc → Silicon);
> the **v55 Spin2 manual is the enumeration**. Extracted every unique `P_[A-Z0-9_]+` token in
> `deliverables/ai/P2/` (115) and compile-tested each. **Result: after the fixes below, the
> YAMLs contain ONLY legal v55 constant names** — `Y-legal \ L` is empty (no legal-but-nonstandard
> names), and all 8 fictitious names are gone corpus-wide. Also ran the **Opus-Master propagation**:
> the manuals are clean in body (they'd already removed these — see F-176 vindication). Two
> non-blocking findings remain: **F-182** (coverage gap) and **F-183** (donor staleness).

### F-183 — count-mode *concise donors* (10100/10101/10110/10111) are broadly stale/divergent from published — `RESOLVED 2026-08-25 («#300») — re-verified on disk; the defect this tracked no longer exists`
> **CLOSED ON RE-VERIFICATION, not on assumption.** Four checks were run against the four donor
> directories under `engineering/ingestion/smart-pins-catalog/ingestionSources/` (16 files), and all four
> legs of this finding came back clean:
>
> 1. **The undefined mode-name constants are GONE from the donors.** A Unicode-tolerant sweep
>    (`grep -rniE "PERIODS.{0,3}STATES|PERIODS.{0,3}CLOCKS|B.{0,3}A.{0,3}INPUT"` over all four donor dirs
>    — deliberately loose, because `smartpin-symbols.txt` has a history of zero-width characters defeating
>    an exact grep) returns **only folder-name echoes in `source-metadata.md`**, never a constant. The
>    donors now carry exactly the legal names published uses: `P_PERIODS_HIGHS`, `P_COUNTER_TICKS`,
>    `P_COUNTER_HIGHS`, `P_COUNTER_PERIODS`.
> 2. **Nothing leaked into the shipped KB.** `P_PERIODS_STATES` / `P_PERIODS_CLOCKS_*` appear nowhere in
>    `deliverables/ai/P2/`. `P_B_A_INPUT` appears once, at
>    `application-notes/p2an004-frequency-rotation-rc-timing-measurement.yaml:101`, and it is a **guard**
>    — *"P_B_A_INPUT does not exist … Never add P_B_A_INPUT"* — i.e. the anti-pattern, correctly stated.
> 3. **The reseed vector is gone.** This entry's worry was that the concise-YAML pipeline would re-emit the
>    donors over published. There are **0 `.yaml` files anywhere under `smart-pins-catalog/`**; the donors
>    are now `.md` extracts only. There is nothing left to reseed *from*.
> 4. **The "different taxonomy" is a phrasing difference, not a correctness defect** — and this is the leg
>    that had to be checked source-first rather than taken from the entry. The **donor folder names track
>    the Silicon Doc's wording literally** (`part4-smart-pins.txt:130-133`: *"%10100 = for X periods, count
>    states"* · *"%10101 = for periods in X+ clocks, count time"* · `%10110` *count states* · `%10111`
>    *count periods*), while the **published titles paraphrase the same semantics** (`%10100` *"Sum Pulse
>    Duration Over X Periods"* … `%10110` *"Count Highs Over Periods Within X Clocks"* — "highs" being the
>    A-input's high **state**). Both sides agree with the primary source. The entry's framing — published
>    hand-corrected *away* from stale donors — reads as though one side were wrong; on the evidence
>    **neither is**.
>
> **Nothing is owed at the ingestion head.** Retired rather than left `TRACKED` indefinitely: a tracked
> item whose subject no longer exists is a false open, and it costs every future reader the same check.
>
> Original text, kept for the record: Carved from F-176. The 4 donors carry undefined **mode-name** constants (`P_PERIODS_STATES`, `P_PERIODS_CLOCKS_TIME/STATES/PERIODS`) **and** a different mode taxonomy than the (hand-corrected) published files, on top of the now-removed `P_B_A_INPUT`. Published diverged from them long ago (proving the concise-YAML pipeline isn't re-run for these), so reseed-risk is currently latent. A **full donor↔published resync** (mode names + taxonomy) belongs to the ingestion/smart-pins-catalog head, not a published-YAML edit. Tracked, not release-blocking.

## ADC gain-mode input ranges framed ground-referenced, not centered on VIO/2 (2026-07-07) — F-202

### F-202 — IOSP §16.2 ADC input-mode table (and 5 propagated sites) frame the gain ranges as ground-referenced `0V–ceiling` — `PARTIALLY CONFIRMED: GIO/VIO-as-calibration + mid-supply bias grounded in Silicon Doc; exact centered endpoints UNVERIFIED (no trusted numeric source) → hardware campaign required`
> **Source of report:** community reviewer (2026-07-07, relayed by Stephen): *"the ranges are totally
> wrong… they are centred around 1.65V."* Community-tier input (Titus-tier): challenges our work, is not
> itself a citable source.
> **TRUST-CHAIN DISCIPLINE (Stephen, 2026-07-07):** the **P2AN\*** app notes are derived from the SAME
> ingested sources as the manuals — a **peer derivation, NOT an authority**. Do not justify manual content
> against P2AN001/§16.3; ground only against trusted **ingested** sources (Silicon Doc) or **empirical**
> hardware (EF ledger). This finding was re-grounded on that basis.
> **What the Silicon Doc (trusted ingested) DOES ground:**
> - **GIO/VIO are calibration sources, not input-range modes** — *"Delta-sigma ADC with 5 ranges, 2
>   **sources**, and **VIO/GIO calibration**."* The §16.2 table mislabels them as ranges (`GIO = 0V–3.3V`,
>   `VIO = VIO-relative`). WRONG per a trusted source.
> - **The ADC has a ~mid-supply bias point** — Rev C note: FLOAT mode "useful for determining the
>   **floating bias point of the ADC**." So the gain window sits around mid-supply, **not up from 0 V** —
>   the table's ground-referenced framing is wrong.
> - Tell-tale of how it happened: the table's ceilings (`1.04V / 330mV / 104mV / 33mV`) equal `3.3V ÷ gain`
>   — correct range **widths** placed at `[0, width]` (generic unipolar-PGA assumption) instead of around
>   the mid-supply bias. (§16.7 L469 and §16.3 already describe the bias/references correctly — but those
>   are peer manual sections, cited here only as internal-inconsistency evidence, not as authority.)
> **RESOLUTION — nominal transfer characteristic (releasable-correct without hardware):**
> The exact endpoints are a **nominal / definitional** quantity, not a measured one: the mid-supply
> reference is grounded (Silicon Doc float-bias-point) and the gain factors are grounded (Silicon Doc
> "5 ranges" + image catalog), so the window `= 1.65 V ± (1.65 V / gain)` about mid-supply is **DERIVED**
> (like the Ohm's-law drive currents and `clkfreq/2³²` NCO resolution we already print), NOT AT_RISK —
> **provided it is labelled *nominal* and carries the calibration caveat** (exact endpoints vary with device
> tolerance + VIO; for absolute work calibrate against GIO/VIO, §16.3). This mirrors the manual's already-correct
> nominal-vs-measured handling of resolution ([[F-201]]). This is the distinction I initially over-collapsed:
> a *measured precision spec* needs silicon; the *nominal transfer characteristic* does not. So §16.2 prints the
> nominal windows (labelled) — correct, complete, hardware-independent.
> **Verification split (per VERIFICATION-OPPORTUNITIES.md):**
> - **VO-J-001 (jumper-only — we do it):** on-chip DAC → jumper → ADC pin sweep confirms the centering + √10
>   window scaling on silicon (upgrades nominal → silicon-confirmed). Task #172. NOT a release blocker.
> - **VO-X-001 (external-hardware — cataloged, not committed):** calibrated external reference + precision meter
>   for tolerance-bounded absolute endpoints. Benefit: nominal → datasheet-grade. Deferred.
> **Propagated sites (all same root), IOSP opus-master `part-3-input-modes/chapter-16-adc.md` unless noted:**
> §16.2 table (L39–46) · §16.2 prose (L50–60) · §16.2 example "0-100mV sensor → 30x" (L64–66) ·
> §16.7 Example 4 thermocouple "0-50mV → 100x" (L505–517) · §16.7 quick-ref table (L636–640) ·
> `part-5-appendices/appendix-d-mode-comparison-charts.md` (L195–198). The **examples are the worst**:
> they feed a ground-referenced small-signal sensor (0-100 mV, 0-50 mV thermocouple, mic, strain gauge)
> into a 1.65 V-centered gain mode with **no mid-rail bias network** — they would not work as written.
> **NOT affected (checked, don't over-correct):** §16.3 ratiometric (correct) · §16.7 float note L469
> (correct) · **DAC ranges ch10** `0–3.3V`/`0–2.0V` (correct — DAC is genuinely unipolar 0-to-Vfs,
> matches Silicon Doc drive-level table). Defect is **specific to ADC gain modes**.
> **Secondary check:** `architecture/smart-pins/smart-pin-11000-adc-internal-clock.yaml` L144–145 calls
> GIO/VIO "Ground-referenced input / VIO-referenced input" — loose (they're calibration references);
> tighten wording, and confirm no range claim depends on the ground-referenced framing.
> **SILICON-CONFIRMED 2026-07-07 (EF-024) — supersedes the nominal formula.** VO-J-001 ran on real P2:
> gain modes ARE centered on mid-supply (~1.64 V measured) [structural, definitive], but the **derived
> `1.65 ± 1.65/gain` (3.3 V/gain width) was WRONG** — measured widths are ~1.4× wider (≈4.55 V/gain), √10-laddered.
> Measured representative windows (N=1): 3.16× 0.93–2.36 V · 10× 1.41–1.87 V · 31.6× 1.57–1.71 V · 100× 1.61–1.66 V.
> **Fold into IOSP v1.0.4** (staged): (a) GIO/VIO reclassified [APPLIED]; (b) mid-supply framing + examples
> fixed [APPLIED]; (c) **print the MEASURED windows** (table above) across §16.2 + Appendix B + Appendix C,
> labelled *measured on real P2 silicon, representative single-sample* (per the citation convention), NOT the
> derived formula; rebuild the two examples on the measured centering [PENDING apply]. With (c), F-202 is
> **CLOSED for release** and now hardware-grounded (not merely derived). VO-X-001 (absolute tolerance across
> parts) remains the optional datasheet-grade upgrade.

> ### KB-SIDE SECONDARY CHECK DISCHARGED 2026-08-25 («#300») — and this entry's HEADLINE is stale
>
> 🔴 **Read the headline against this block.** The heading still says *"exact centered endpoints UNVERIFIED
> (no trusted numeric source) → **hardware campaign required**"*. **That campaign already ran.** The
> `SILICON-CONFIRMED 2026-07-07 (EF-024)` note immediately above is the result, and
> `VERIFICATION-OPPORTUNITIES.md:38` records **VO-J-001 → DONE → EF-024**. A top-down reader stops at the
> heading and concludes this is blocked on silicon we cannot reach; it is not. **This is exactly the failure
> mode REGISTER-CONSULTATION §1 exists for** — the status sits at the end, and here the end supersedes the
> front. The heading is left in place rather than rewritten because the entry is mid-flight on the manual
> side, but nothing downstream should quote it.
>
> **KB FIX APPLIED — the "Secondary check" line above, now discharged.**
> `deliverables/ai/P2/architecture/smart-pins/smart-pin-11000-adc-internal-clock.yaml`:
> - `:143-151` — `adc_input_modes` no longer calls GIO/VIO input ranges. `P_ADC_GIO` / `P_ADC_VIO` now read
>   *"…calibration reference to the ADC (a calibration **SOURCE**, not an input range)"*, and `P_ADC_FLOAT`
>   states its actual purpose. Grounded in-file on **Silicon Doc `p2-documentation.txt:452`** — *"Delta-sigma
>   ADC with 5 ranges, 2 **sources**, and **VIO/GIO calibration**"* — with the mode-name glosses cited to
>   **`spin2-v55-text.txt:1466-1473`** (*"ADC GIO → IN"* / *"ADC VIO → IN"* / *"ADC FLOAT → IN"*), and
>   `P_ADC_FLOAT`'s bias-point role to **`p2-documentation.txt:188-190`** (Rev C: *"…but floats the ADC input.
>   This mode is now useful for determining the floating bias point of the ADC."*).
> - `:168-169` — **the range claim that depended on the ground-referenced framing is gone.** The old note
>   *"ADC input modes (GIO/VIO/gain) affect voltage range and sensitivity"* lumped the calibration sources in
>   with the gain ladder as if all of them set a range. It now separates them, and a second note carries the
>   structural EF-024 result: *"The gain-mode window is **CENTERED ON MID-SUPPLY (~VIO/2)**, not referenced up
>   from 0V … centered at ~1.64V for every gain (EF-024). A ground-referenced small-signal source needs a
>   mid-rail bias network before it can be read through a gain mode"* — which is the trap that made this
>   finding's worked examples unrunnable.
> - **Only the structural half of EF-024 was carried into the KB, deliberately.** EF-024 grades the centering
>   as *[structural, definitive]* but its window endpoints as a **representative single sample (N=1)**. The
>   centering is stated; **the N=1 endpoint numbers are NOT printed in the KB**, because a bare table there
>   would read as a specification. Printing them, labelled, is step (c) above — **manual-side, «#301»**.
> - Verified after the edit: `validate-crossref-keys.py` 3161 refs / 0 unresolved ·
>   `audit-yaml-claim-sourcing.py` 0 Tier-1, Tier-2 unchanged at 78 · `verify-yaml-format.py` clean.
>
> **THE GAP THAT ACTUALLY REMAINS — and it is NOT the centering.** It is **VO-X-001**, cataloged at
> `VERIFICATION-OPPORTUNITIES.md:51`: *tolerance-bounded **absolute** endpoints across parts and
> temperatures.* **What would settle it:** a calibrated, traceable external voltage reference plus a
> precision meter, exercised across several parts — **external hardware, which this container cannot reach**
> and which is `CATALOGED`, not committed. Its own entry says it is *"not needed for correctness."*
> **No endpoint number was supplied here, and none should be** — the measured N=1 windows in EF-024 are the
> only figures with evidence behind them, and they are labelled as such at their source.

---

## Quantitative hardware-table audit batch (2026-07-07) — F-203

### F-203 — 4-manual fan-out audit of quantitative hardware tables vs trusted ingested sources — `PARTIAL — 14 CONFIRMED_WRONG (hand-verified) + 8 AT_RISK; the IOSP and deSilva cells are fixed, the Streamer and Debug cells need their own patches`
> **Method:** 9-unit fan-out (IOSP ×5 parts, Streamer, Debug ×2, deSilva) enumerating every quantitative/encoding
> table cell, each classified GROUNDED/DERIVED/AT_RISK/WRONG against **ingested sources only** (Silicon Doc,
> Spin2 v55, P2 datasheet), then adversarially verified. Full verdicts: workflow `wx8vrj00a` output. 1 false
> alarm rejected on hand-verify (ch06 "30mA" — actually GROUNDED, spin2-v55:1502).
>
> **CONFIRMED_WRONG — IOSP (fold into v1.0.4):**
> - `ch02` `P_HIGH_FAST`/`P_LOW_FAST` drive impedance **`~100Ω` → `~17Ω`** (datasheet Vol 510mV@30mA ⇒ ~17Ω; 30mA is correct). **FIXED.**
> - `ch18` §18.6 Hub RAM **`8-15 clocks` → `9-16 clocks`** (datasheet RDLONG `9...16`). **FIXED.**
> - `appendix-b` + `appendix-c` (table **and** the `input_max = 3300mV/gain` formula) — **F-202 ADC-range recurrence** (2 more sites; ground-referenced `0-Xmv`). PENDING (rides the F-202 nominal-table fix across §16.2 + both appendices).
>
> **CONFIRMED_WRONG — deSilva (fold into v3.0.2):**
> - SETSE Event-Modes `%000` **"Never (disabled)" → "LUT read/write & hub-lock events"** (silicon-doc part3-interrupts:48-53). **FIXED.**
> - `EVENT_INT %0000` **"Pin matches interrupt configuration" → "An interrupt occurred"** (part2-video-output:360; pin-match is `EVENT_PAT %1000`). **FIXED.**
> - `EVENT_QMT %1111` **"CORDIC/PIX math complete" → "read with no CORDIC result available"** (part2-video-output:375 — the inverse meaning). **FIXED.**
>
> **CONFIRMED_WRONG — Streamer (needs own patch, NOT in current wave):**
> - §12.2 Sub-Pin Selection table treats `D[19:17]` as a uniform 3-bit selector for 1/2/4-pin; silicon encodes `pppa/pp?a/p??a` (pin-bits shrink 3/2/1; freed low bits = DAC sub-mode). 1-pin col correct; 2/4-pin cols wrong. (p2-documentation:3004-3009).
>
> **CONFIRMED_WRONG — Debug (needs own patch, NOT in current wave):**
> - `ch05` PLOT TEXTSTYLE **horizontal align 2/3 swapped** (source %10=right, %11=left) and **vertical align 2/3 swapped** (%10=bottom, %11=top) — spin2-v55:1282; plus downstream prose **"`$20` left-aligns" → right-aligns**.
> - `ch03` TERM **`TEXTSIZE` default `10` → "editor text size"** (spin2-v55:1305; the 10 is the PLOT default).
>
> **AT_RISK (unsourced specifics — disposition per finding):** IOSP `ch16` §16.8 ADC "input impedance ~500kΩ" + "absolute-error floor ~15mV" (from P2AN001, not in EF ledger — **jumper-only verifiable, VO-J candidate**); `ch10` DAC "Max Load >10kΩ…" (10× rule-of-thumb heuristic); `ch12` "input buffer ~2ns" (sub-component; 3-clk total IS grounded); `ch07` "180MHz rated / 250 overclock" (only 350 grounded; 180 cites external datasheet); Debug `ch05` weight "100/400/700/900" (OpenType nums unsourced; "thin"→"light"); Debug `ch14` "LOCK[15]" + "~10,000 msg/s" (tool/throughput, ungrounded). Disposition: remove the unsourced number or soften to qualitative; the ~15mV/~500kΩ ADC pair → VO-J jumper test.

> ### 🔴 KB-SIDE DISPOSITION 2026-08-25 («#300») — TWO OF THIS ENTRY'S OWN SUB-CLAIMS DO NOT SURVIVE THE SOURCE
>
> Only the **KB-side** halves are dispositioned here; the IOSP / deSilva / Streamer manual cells stay with
> «#301». Every item below was checked **source-first**, and two of them inverted. **Anyone working the
> manual half must read this block before "fixing" the manual to match this entry — two of these
> corrections would introduce a defect, not remove one.**
>
> **(a) Debug `ch05` PLOT `TEXTSTYLE` vertical align — `RESOLVED-INVALID`. The KB is CORRECT; the "swap" is a
> vocabulary collision.** This entry grades the vertical pair against the v55 published text
> (`spin2-v55-text.txt:1282`: *"%YY is vertical justification: %00 = middle, %10 = bottom, %11 = top"*) and
> calls our `%10=top / %11=bottom` a swap. It is not. **The Pascal-derived matrix is the authority for the
> DEBUG windows** — this register's own *AUTHORITY CORRECTION (2026-06-14)* established that, and said the
> published v55 text is the derivative that carries the off-by-ones — and the matrix
> (`p2-debug-window-manual/REF/DEBUG-WINDOW-DIRECTIVE-MATRIX.md:797-828`, from `AngleTextOut`, 3483-3516)
> states **both halves for every value** precisely so this cannot be misread:
>
> > vertical `%10` → `ty := h` (3509) → *"the text sits **ABOVE** the anchor point"*, i.e. *"the anchor is the
> > text's **BOTTOM** edge"*; vertical `%11` → `ty := 0` (3510) → *"the text sits **BELOW** the anchor"*, i.e.
> > *"the anchor is the text's **TOP** edge"*.
>
> The matrix carries an explicit red warning that **"`%10` = left" (anchor-edge vocabulary) and "`%10` = right"
> (ink-side vocabulary) describe the same pixels**, and that this ambiguity *"is what caused this row to be
> documented backwards."* v55 uses **anchor-edge** words for the vertical axis and **ink-side** words for the
> horizontal one, in the same sentence. `plot.yaml:67` uses **ink-side consistently on both axes** — and it
> says so, prefixing the pair with *"Align value->direction"*. Under that vocabulary `%10 = top` (ink above
> the anchor) is **right**. Same for the horizontal pair, which this entry and the KB already agree on.
> **No KB edit made. Making the "fix" would have broken a correct file** — the E-005 lesson (*look for the
> vocabulary key before escalating a two-source conflict*) one register over.
>
> **(b) Debug `ch05` weight `"thin"→"light"` — `RESOLVED-INVALID`, and the numbers are NOT unsourced.** The
> matrix quotes the Pascal array directly: `weight: array [0..3] of integer = (100, 400, 700, 900);` (3485),
> applied as `NewLogFont.lfWeight := weight[style and 3];` (3494). So **100/400/700/900 are sourced**, and
> **100 is OpenType `Thin`** (300 is `Light`) — our `plot.yaml:67` gloss *"0=thin, 1=normal, 2=bold, 3=heavy"*
> is correct against the Pascal. v55's *"%00 = light"* is the outlier. **No KB edit made.**
>
> **(c) Debug `ch03` TERM `TEXTSIZE` default `10` → "editor text size" — `RESOLVED-INVALID` as written; both
> statements are true and the KB's is not wrong.** The matrix settles it at
> `DEBUG-WINDOW-DIRECTIVE-MATRIX.md:502-512`: *"The global `FontSize` preference (set in `EditorUnit`, default
> **10**, user-adjustable 1–72) and the `DefaultTextSize = 10` constant both default to **10**, so every
> display window starts at **10 pt** except MIDI"* — and its per-window table lists **TERM `FontSize` = 10**
> (2186) alongside LOGIC/SCOPE/SCOPE_XY/FFT/PLOT, all 10. v55's *"editor text size"* names the **preference**;
> `10` is that preference's **default**. `term.yaml:32` (*"6..200 (default 10)"*) is therefore accurate.
> Swapping it for *"editor text size"* would have **deleted a true number and replaced it with a vaguer
> phrase**. **No KB edit made.** *(Available enhancement, not a defect and not done here: the six
> debug-display YAMLs could add that the default tracks a user-adjustable editor preference. It applies
> identically to all six, so it is an all-or-none consistency change outside this finding's scope.)*
>
> **(d) IOSP `ch16` §16.8 ADC `~15mV` absolute-error floor — ALREADY SATISFIED in the KB, and refuted on
> silicon.** The VO-J test this entry proposed **was run**: `VERIFICATION-OPPORTUNITIES.md:39` records
> **VO-J-002 → DONE → EF-024** — *"Single-pin abs error **≤9 mV** (reproducible) → does NOT support a ~15 mV
> single-pin floor"*, with the pin-to-pin-spread half reclassified to external-hardware **VO-X-002**. The KB
> already carries exactly this, correctly hedged, at
> `application-notes/p2an001-single-pin-instrumentation-adc.yaml:100`: *"…the ratiometric single-pin absolute
> error was <=9 mV … the wider '~15 mV pin-to-pin spread' figure is a designer report that the bench has NOT
> yet reproduced … **Do not quote 15 mV as a specification.**"* **No KB work owed.**
>
> **(e) IOSP `ch16` §16.8 ADC `~500kΩ` input impedance — never reached the KB.** Swept
> `deliverables/ai/P2/`: no `500k` input-impedance claim exists. It is a manual-only item → «#301».
>
> **KB-side verdict: nothing is owed.** Status stays `PARTIAL` **for the manual cells only** (Streamer §12.2
> sub-pin selection, Debug ch05/ch14, and the remaining IOSP AT_RISK numbers), all of which are «#301»'s.

> ### 🟢 MANUAL-SIDE DISPOSITION 2026-08-25 («#301») — every remaining cell settled; ONE edit, and it went the OPPOSITE way to what this entry says
>
> Each cell was opened **on disk first** and graded against its authority, not applied from this
> entry's verdict. That order mattered: **six of the ten manual cells were already fixed and nobody
> had said so**, and of the four that looked outstanding, **three were RESOLVED-INVALID and applying
> them would have damaged correct pages.** The «#300» warning generalised exactly as it said it would.
>
> **Already fixed — verified in the master, not inferred (6):**
> - **Streamer §12.2 sub-pin selection** — `streamer-body.md:958` now states the correction verbatim:
>   *"It is **not** a uniform 3-bit selector across all pin counts: as the pin count rises, fewer of
>   these bits are pin-select bits and the freed low bits become **DAC-configuration** bits."* The
>   three tables under it (`:960-989`) give 1-pin = 3 pin bits, 2-pin = `D[19:18]` + `D[17]` config,
>   4-pin = `D[19]` + `D[18:17]` config. Checked against the silicon column at
>   `sources/silicon-doc/p2-documentation.txt:3004-3009` — `pppa / pp0a / pp1a / p00a / p01a / p10a` —
>   which is the 3/2/1 shrink exactly. Recorded in Streamer `CHANGELOG.md:102-105`.
> - **IOSP `ch02` drive impedance** — `chapter-02-enhanced-direct-io.md:51`/`:66` read `~30mA / ~17Ω`.
> - **IOSP `ch18` hub access** — `chapter-18-repository.md:346` reads `9-16 clocks/access`.
> - **deSilva `SETSE %000`** — `:5026` reads *"LUT read/write & hub-lock events (not a pin event)"*.
> - **deSilva `EVENT_INT %0000`** — `:5041` reads *"…as a POLL/WAIT event it means an interrupt
>   occurred"*; **`EVENT_QMT %1111`** — `:5056` reads *"GETQX/GETQY read with no CORDIC result
>   available"* (the inverse meaning, correctly stated).
> - **Debug `ch14` `LOCK[15]` and `~10,000 msg/s`** — **gone**. `grep` for either across the whole
>   Debug Window `opus-master/` returns nothing. The ungrounded throughput number is not in the book.
>
> **AT_RISK numbers — all already dispositioned exactly as this entry directed (4):** and the IOSP
> `CHANGELOG.md:53` records the pass, naming Chapters 7, 10, 12, 16.
> - `ch16` **`~500kΩ` input impedance — removed.** `grep "500k"` over the IOSP master returns
>   nothing; `chapter-16-adc.md:598` now says *"The 1× range presents a **high input impedance**"*
>   qualitatively, with the divider consequence. (This entry's KB-side item (e) called it
>   "manual-only → «#301»"; the manual had already dropped it.)
> - `ch16` **`~15mV` error floor — removed and REPLACED WITH THE BENCH RESULT.** `:599` now reads
>   *"a few millivolts (**≤ ~9 mV measured on real P2 silicon**; representative, not a guaranteed
>   spec)"*, with pin-to-pin spread named as the larger effect. That is EF-024 / VO-J-002, i.e. the
>   manual and the KB now agree, and neither quotes 15 mV as a specification.
> - `ch10` **DAC "Max Load"** — the column is renamed **"Min Load (guideline)"** and
>   `chapter-10-dac-output.md` states outright that it *"is a **rule-of-thumb guideline** (roughly
>   10× the output impedance), not a hard specification."*
> - `ch12` **"input buffer ~2ns" — gone.** No `2ns` anywhere in the IOSP master.
> - `ch07` **"180 MHz rated / 250 overclock" — now CITED, both ends.**
>   `chapter-07-pulse-transition.md:271` attributes 180 MHz to the P2 Datasheet and the ~350 MHz
>   ceiling to the Silicon Doc, and frames 250 MHz as *"commonly used"* rather than as a rating.
>   Both citations verified live: `sources/p2-datasheet/p2-datasheet-text.txt:2209` (*"Nominal PLL
>   frequency (system clock speed) is 180 MHz at up to 105 °C"*) and
>   `sources/silicon-doc/part3-interrupts.txt:545` (*"the PLL can be pushed to 350 MHz"*).
>
> **🔴 RESOLVED-INVALID for the MANUAL too — do not apply these; two of them would break correct pages (3):**
> - **Debug `ch05` PLOT `TEXTSTYLE` alignment, BOTH axes — `RESOLVED-INVALID`.** This entry says
>   horizontal 2/3 and vertical 2/3 are each swapped in `ch05`. They are not. `ch05-plot.md:356-357`
>   reads horizontal `2`=right / `3`=left and vertical `2`=top / `3`=bottom — **ink-side vocabulary,
>   used consistently on both axes**, which is the same convention `plot.yaml:67` uses and which the
>   Pascal-derived authority confirms: `REF/DEBUG-WINDOW-DIRECTIVE-MATRIX.md:797-828` gives
>   horizontal `%10` → `tx := 0` → *"the text sits to the **RIGHT** of the anchor"* and vertical
>   `%10` → `ty := h` → *"the text sits **ABOVE** the anchor"*. `ch05-plot.md:360`'s downstream prose
>   *"`$20` right-aligns"* is therefore also **correct** ( `$20` → bits 4-5 = `%10` → ink to the
>   right), not the error this entry records. Applying the swap would have inverted a correct table
>   and a correct sentence. Same vocabulary collision «#300» found on the KB side; the matrix's own
>   red warning says this ambiguity *"is what caused this row to be documented backwards."*
> - **Debug `ch05` weight `"thin"→"light"` — `RESOLVED-INVALID`.** `ch05-plot.md:353` reads
>   `0`=thin, `1`=normal, `2`=bold, `3`=heavy. Against the Pascal
>   (`weight: array [0..3] = (100, 400, 700, 900)`, matrix `:797`), **100 is OpenType *Thin*** —
>   *Light* is 300 — so the manual is right and the proposed change would have introduced the error.
>   ("heavy" for 900 is an accepted synonym of Black; not a defect.)
> - **Debug `ch03` TERM `TEXTSIZE`** — this one is `RESOLVED-INVALID` **and the manual had already
>   taken the invalid change**, so it needed reverting rather than leaving. See below.
>
> **The single edit made, and it runs OPPOSITE to this entry (1):**
> `ch03-term.md:45` had a Default column reading **"editor text size"** — i.e. exactly the swap this
> entry proposed, already applied at some earlier pass. «#300»(c) ruled that
> `RESOLVED-INVALID` because it *"deleted a true number and replaced it with a vaguer phrase"*, and
> the authority agrees: `REF/DEBUG-WINDOW-DIRECTIVE-MATRIX.md:502-512` states the global `FontSize`
> preference (default **10**, user-adjustable) and `DefaultTextSize = 10` both default to **10**, and
> its per-window table lists **TERM `FontSize` = 10** (Pascal 2186). Restored to `10`, with the
> preference stated too so both halves are on the page: *"the default tracks the editor's text-size
> preference, which is itself 10."* Per C4, the REF matrix outranks the v55 prose the old wording came
> from.
>
> **Raised, not just corrected (F2):** `ch05-plot.md` gains a short paragraph after the style table
> making the alignment vocabulary explicit — *"Read those alignment names as where the ink lands
> relative to the anchor point, not as which edge of the text the anchor sits on… If a label lands on
> the wrong side of its point, you have almost certainly read the row in the other vocabulary rather
> than found a bug."* The rows were already right; what was missing was the disambiguation that
> caused this cell to be filed as a defect twice. Stating both halves is what the authority itself
> does, and why.
>
> **Gates:** `audit-code-line-length.py --budget 76` and `audit-inline-code-ascii.py` exit 0 on
> `ch03-term.md` and `ch05-plot.md`; `sync-manual-examples.py --check` reports **no** "BODY differs"
> for the Debug Window manual, so no printed listing drifted from its example file.
>
> **STILL OWED (1 cell, and it is not this finding's to close):** IOSP `appendix-b` + `appendix-c`
> ADC-range cells (table **and** the `input_max = 3300mV/gain` formula). They are the **F-202**
> recurrence and ride that finding's nominal-table fix across §16.2 + both appendices. F-202 is
> `PARTIALLY CONFIRMED` with the exact centered endpoints **UNVERIFIED — no trusted numeric source**,
> so what would settle it is the hardware campaign F-202 names, not an edit here. Touching the
> appendices ahead of F-202 would put a third unsourced framing in the book.
>
> **Manual-side verdict: 6 already fixed · 4 AT_RISK already dispositioned · 3 RESOLVED-INVALID
> (2 of which would have introduced defects) · 1 corrected back toward the authority · 1 owed to
> F-202.** Render owed for the Debug Window edits → «#302».

## XBYTE technique-mining sweep — reference implementations expose two doc defects (2026-07-14) — F-217, F-218

> **Origin.** Stephen asked for a per-processor "what will hurt when you emulate this" table in the XBYTE
> Guide, and proposed we ground it by studying **live, working emulators** rather than reasoning from ISA
> facts. The study immediately surfaced two defects. Full evidence ledger:
> `engineering/document-production/manuals/p2-xbyte-programming-guide/TECHNIQUE-MINING.md`
> (per-source, because the techniques enter the manual body *anonymously* — the ledger is the only place
> the lineage lives). **Note the path:** it lives at the manual **root**, not in `audit/`, because
> `.gitignore:175` ignores `manuals/*/audit/` — a durable source-of-record cannot live there.

### F-218 — `SingleStep-Debugger-Theory-of-Operations.md` §6.4 mislabels `GETBRK` D[25] as "C,Z affected by XBYTE" — `CONFIRMED` — **VERIFIED against the Silicon Doc 2026-08-25 («#300»); the KB was already correct, so no KB work is owed**

**Our own ingested doc says:**

> *"Displayed as 3 hex digits. A checkmark glyph appears if **bit 25** of `mBRKC` is set (**C,Z affected by
> XBYTE**)."*

**The Silicon Doc says otherwise.** Per P2KB `p2kbPasm2Getbrk`, `GETBRK D WC` returns:

| Field | Meaning (Silicon Doc) |
|---|---|
| D[27] | 1 = SKIP · 0 = SKIPF/EXECF/XBYTE |
| D[26] | LUT sharing enabled |
| **D[25]** | **XBYTE pending on next `_RET_`/`RET`** |
| D[24:16] | the 9-bit XBYTE mode |

"C,Z affected by XBYTE" is the **F bit**, which is the *low bit of the mode operand* — i.e. **D[16]**, not
D[25]. The two are different facts about different bits, and our doc appears to have conflated them.

- **NOT SETTLED, and deliberately not fixed.** The checkmark's meaning is decided by the **host-side**
  display code (PNut / term-ts), not by Chip's P2-side debug stub — `Spin2_debugger.spin2` only calls
  `getbrk` and ships the word to the host. So the P2-side source **cannot** adjudicate this. Settling it
  needs the host display source or Chip.
- **Two possible truths:** (i) our gloss is simply wrong and D[25] means "XBYTE pending"; or (ii) the
  debugger's checkmark genuinely reflects the F bit and our doc attributed it to the wrong bit index. Either
  way **the doc as written is wrong**; only the repair differs.
- **Consumer risk:** the XBYTE Guide is about to gain a "Debugging XBYTE" section citing `GETBRK` fields.
  It will cite **the Silicon Doc layout**, not this doc, until this is resolved.
- **Wider lesson (already a standing rule, freshly demonstrated):** our own ingested derivations are **peer
  tier, not authority**. This was caught only because the field layout was cross-checked against P2KB
  instead of being trusted.

> ### ✅ VERIFICATION PERFORMED 2026-08-25 («#300») — this entry's `NEEDS-VERIFICATION` is discharged
>
> The original entry rested on **P2KB** (`p2kbPasm2Getbrk`), which is circular inside this project — the KB
> is what we publish. So it was re-grounded on the **Silicon Doc primary extraction**, and both halves of
> the claim were checked independently. **What could have come back the other way:** had the Silicon Doc's
> own `D[25]` line read *"C,Z affected by XBYTE"*, the finding would have become `RESOLVED-INVALID` and the
> doc would have been right. It does not.
>
> **Half 1 — what D[25] actually is.** `engineering/ingestion/sources/silicon-doc/part3-interrupts.txt:445-446`,
> verbatim, under `GETBRK D WC`:
>
> > `D[25] = 1 if top of stack = $001FF, indicating XBYTE will execute on next _RET_/RET`
> > `D[24:16] = 9-bit XBYTE mode, established by '_RET_ SETQ/SETQ2' when top of stack = $001FF`
>
> **Half 2 — where "C,Z affected by XBYTE" really lives.** It is the `%F` bit, and `%F` is the **LSB of the
> 9-bit mode**, so it lands at **D[16]**. `silicon-doc/p2-documentation.txt:2196-2202`, verbatim:
>
> > *"The %F bit of the SETQ/SETQ2 {#}D value enables C and Z to receive bits 1 and 0 of the index field of
> > the bytecode."* — with the table `%xxxxxxxx0` = *"Do not affect flags on XBYTE"* · `%xxxxxxxx1` =
> > *"Write the bytecode's index LSBs to C and Z"*.
>
> **VERDICT: `CONFIRMED`.** D[25] and D[16] are different bits with different meanings, and §6.4 fuses them.
> The entry's premise holds on the primary source, not merely on P2KB.
>
> **A SECOND SITE, same root cause, found by sweeping the doc (class-wide rule).** The same file's field-map
> row contradicts its own body: `SingleStep-Debugger-Theory-of-Operations.md:1298` states
> *"XBYTE (bits 25..16)"* — a **ten**-bit field that swallows D[25] into the mode — while `:763` computes the
> field as `DebuggerMsg[mBRKC] >> 16 AND $1FF`, i.e. **D[24:16]**, which is correct. `:765` is the §6.4
> sentence this finding names. So the defect is **two sites plus a self-contradiction**, not one sentence.
>
> **🟢 NO KB WORK IS OWED — verified on disk, not assumed.**
> `deliverables/ai/P2/language/pasm2/getbrk.yaml:33` already reads
> *"…D[26] = LUT sharing enabled, **D[25] = XBYTE pending on next `_RET_`/`RET`**, D[24:16]…"* — correct, and
> matching the Silicon Doc. No published manual carries the wrong gloss either (swept: zero hits for
> `C,Z affected` across `manuals/*/opus-master/`). **The defect never reached anything we ship**, which is
> why this closes without a KB edit rather than being left open for one.
>
> **RESIDUAL GAP — narrowed, not closed, and it is not ours.** Which of the two repairs §6.4 needs still
> depends on the **host display source**: if PNut/term-ts really tests bit 25, the *caption* is wrong; if it
> tests bit 16, the *bit index* is wrong. **What would settle it:** the host-side display routine that draws
> the XBYTE checkmark (PNut Pascal or the term-ts mirror), which this repo does not hold — `REF/` under
> `p2-single-step-debugger-manual` carries only the user manual, a screenshot and an audit, no Pascal.
> **This is an upstream document defect with no consumer here**, so it is routed, not worked: the bit
> semantics above are now settled and citable regardless of which repair is chosen.
>
> **Not relocated to `SOURCE-ERRATA.md`, deliberately.** That register's own test is *"if **Parallax** fixed
> their document tomorrow, would this entry disappear?"* — and all nine of its entries are Parallax
> documents. This document is the **pnut-ts side's** (`external-inputs/pnut_ts_facts/`, not a registered
> ingested source), so it fails that test. It is also not a `PNUT-TS-PUNCH-LIST.md` item — that list is
> compiler-behaviour items carrying a runnable repro, not documentation defects. Flagged here as the record.

## CORDIC interrupt hazard — documented on one page, missing from the pages that need it (2026-07-14) — F-224

> **This header replaced a stale one on 2026-08-21.** F-224 had been sitting under
> *"`architecture/xbyte_engine.yaml` — all three programming examples are broken"*, whose four
> findings (F-220…F-223) all closed 2026-07-14/16 and were archived 2026-08-15 — leaving a live
> register asserting that three KB examples were broken when the file had been fixed for a month.
> Verified fixed in `xbyte_engine.yaml` at commits `31bffdce` (F-220/221/222) and `bb02525a`
> (F-223). Detected by `audit-register-hygiene.py` checks 8 and 9.

### F-224 — Assembly Manual: the CORDIC interrupt hazard is documented on the `REP` page, but **not on the CORDIC pages** — `RESOLVED 2026-08-17, shipped in v3.1.6`

> **Status heading corrected 2026-08-22.** It read `CONFIRMED` while this entry's own body recorded the resolution — the entry contradicted itself, and a status line is not evidence. The body below is unchanged.

**Raised by F-217's class-wide sweep.** Having found that the XBYTE Guide sold interruptibility as a
pure benefit, the same question was asked of every other manual: *does anything show a CORDIC
issue/collect pair without telling the reader it must be fenced?*

**The Assembly Manual is NOT wrong.** `part-ii/instructions-r.md` teaches the fence properly, and even
uses a CORDIC example:

> `' Protect CORDIC operation from interrupts` … `qmul  y, x`

and states the mechanism outright: *"Interrupts are blocked during REP execution — including debug
interrupts that ordinary masking cannot hold off — to maintain timing precision and keep the repeated
block atomic."* It also carries the useful nuance that the idiom *"is only needed in PASM2 code with
interrupts enabled; Spin2 operators are already protected by the interpreter."*

**But the warning is not where the affected reader is standing:**

| Page | Content | Interrupt mentions |
|---|---|---|
| `instructions-q.md` | **QMUL · QROTATE · QDIV** — the CORDIC **issue** ops | **0** |
| `instructions-g.md` | **GETQX · GETQY** — the CORDIC **collect** ops | 3 — **all from GETBRK**, none about CORDIC |
| `instructions-r.md` | REP | ✅ the fence, with a CORDIC example |

A reader who looks up `QMUL` — which is exactly what someone about to *write* a CORDIC sequence does —
learns nothing about the hazard. They find it only by happening to read the `REP` page.

- **Severity: low.** This is an omission at the point of need, not a false claim. Same *class* as F-217,
  milder in kind: the information exists in the manual.
- **Fix (small):** a cross-reference note on the CORDIC issue/collect pages — "a CORDIC command and its
  result must not be split by an interrupt; see REP" — costing a few lines, no content change elsewhere.
- **Release consideration for Stephen:** the Assembly Manual shipped **v3.1.4 on 2026-07-14** (a
  render-only patch). This is a *content* change and would need its own bump. It is a documentation
  improvement, not a correctness bug in the shipped text, so it can ride the manual's next natural
  release rather than forcing one.

**RESOLVED 2026-08-17 («#235» wave prep).** Confirmed still open first — `instructions-q.md` had
**zero** interrupt mentions, and `instructions-g.md`'s three were all GETBRK. The rule now opens the
**Q instruction section** (where a reader looking up QMUL or QROTATE lands) and the **CORDIC
Coprocessor category** (which reaches GETQX/GETQY too), both pointing at REP for the pattern and both
noting Spin2 needs no fence. Plain reference prose, not `{.warningbox}` — that convention is reserved
for silicon bugs, and this is a programming hazard. **Rides v3.1.6**, which was otherwise the one wave
element with no prose change, so it costs nothing to carry.

**Also observed (not a defect):** 22 stray `*.backup-encoding-conversion` files sit in
`p2-assembly-language-manual/opus-master/part-ii/`. They are **untracked** — `git ls-files` returns
zero — so nothing ships and no glob in the assemble scripts reaches them (those use explicit
`REQUIRED_FILES[]`). Working-tree clutter only; worth sweeping, not a release concern.

## Forum docs-feedback sweep (2026-08-14) — F-254…F-258

**Origin:** Parallax forum posts #104–#117 (2026-08-12/13), reviewing the deSilva tutorial, the
XBYTE Programming Guide, and the P2 Architect's Guide. Full analysis (with the tone/positioning
items that are *not* defects) lives at
`engineering/document-production/FORUM-NO-COMMMIT/Docs-findings-360813/DOCS-FINDINGS-ANALYSIS.md`
(gitignored — find it by path). Forum posts are the **lead**; every finding below was verified
against the live opus-master, `pnut-ts` 1.55.3, or P2KB before filing.

### F-256 — `_RET_ CALL` never returns, because `_RET_` returns only if the instruction did not branch. A DOCUMENTATION defect, not a hardware one. `RESOLVED — root cause is F-273; KB applied, manual restructure applied 2026-08-16 («#227»)`

**Location:** `xbyte-body.md:879` (*"Chapter 15's `_RET_ CALL #set_nz` idiom depends entirely on
this"*), used at `:1391`, `:1400`, `:416`, `:793`.

Christof (#110) doubted *"you can combine a CALL with ret."* **Tested: `_ret_ call #set_nz`
assembles clean under `pnut-ts` 1.55.3**, and `language/pasm2/call.yaml:11` describes CALL paired
"with a `_RET_` condition" — so as stated the objection is wrong.

**But the compiler proves legality, not semantics.** The open question is what the hardware does
when one instruction both pushes a return address and returns: does control reach the helper and
then return to `$1FF` (XBYTE re-entry intact), or does the push/pop ordering break dispatch?
`architecture/xbyte_engine.yaml:71` is suggestive but addresses a *different* case (why a CALL
cannot substitute for `PUSH #$1FF` at arm time). **Not resolvable from the KB or the Silicon Doc;
no answer is asserted here.**

> **ANSWERED — AND THE ANSWER WAS IN THE INGESTED SOURCES ALL ALONG. See F-273.**
> This was never a hardware question. **`_RET_` executes the instruction and returns *only if that
> instruction did not branch*** — stated by *two* independent Parallax primary sources (Assembly
> Language Manual 2022-11-01, condition table p.68; P2 Instructions v35 Rev B/C Silicon, row 410:
> *"if `<inst>` is not branching then return by popping stack[19:0] into PC"*). `CALL` branches, so
> `_RET_ CALL` cannot return. **The behaviour is specified, not anomalous.**
>
> **The real defect is ours:** our KB documented the prefix as an unconditional *"Always + Return"*
> and the qualifier *"if no branch"* appeared **nowhere** in `deliverables/ai/P2/`. An author
> reading that writes `_RET_ CALL #set_nz` and is right to. **Root cause, KB fix and the
> alignment-check lesson are all in F-273.**
>
> **What the bench actually showed (EF-058, corrected there too):** the handler falls through into
> whatever follows it in cog RAM. In the rig that was another handler, which ran in full and whose
> own `ret` returned to `$1FF` — so **all four bytecodes dispatched and the VM finished normally.**
> The original claim *"dispatch does not resume"* is **false**. The failure mode is **silent extra
> execution**, and it is **layout-dependent**.
>
> **NO FURTHER RIG RUN IS REQUIRED.** Not for generality outside XBYTE — the prefix is architectural
> and the sources say nothing about XBYTE — and not to confirm EF-058, which can only re-observe the
> specification. The `[M-pre]` grade and the staged `DEBUG_COGS` re-run are **moot for the
> conclusion**; the conclusion now rests on documentation, with the bench as corroboration.
>
> **Applied in `xbyte-body.md` («#227», uncommitted under the «#234» gate):** every `_RET_ CALL`
> replaced by `CALL` + `RET` — §15.3's handlers and the shared `ld_imm` family, §4.4's `alu_body`,
> §5's `push_const`, §17's `voice_on` — plus the two explanations that endorsed the idiom (`:882`
> and §15.3). **That structural change stands; its EXPLANATION is being rewritten** to teach the
> documented rule rather than the mechanism previously inferred here. Slices recompile clean.

**Action:** jumper-free, single-board hardware test — arm XBYTE, run a handler ending in
`_RET_ CALL`, report whether dispatch continues. Ideal **VO-J** candidate; result goes to the EF
ledger either way. **A load-bearing idiom in a guide under community review must not stay
unverified.** If it fails, §15.3 and the Chapter 9 explanation both need rework.

## Render-verification wave — defects found by READING the generated PDFs (2026-08-17/19) — F-284…F-294, F-299…F-301

**Origin.** Verifying the six generated wave PDFs page by page rather than reading their compile
logs. Every finding below was invisible to a clean log: LaTeX ate an operator, a filter split a
line, a glyph printed nothing, a gate skipped the blocks it was built to check. F-295…F-298 closed
at the XBYTE sprint closeout and are archived.

> **These sat under the wrong header until 2026-08-21.** The 2026-08-19 sweep archived
> F-259…F-263 but left their `## Community bench review — refaQtor` header in place, so all
> fourteen read as part of a third party's bench review. That header is now in the archive with
> the findings it introduced. Detected by `audit-register-hygiene.py` check 9.

### F-284 — the 9-column encoding-table filter never escaped `&`, so two shipped instruction definitions print with the AND operator eaten by LaTeX. `RESOLVED`

> **VALIDATED against the released v3.1.6 PDF, 2026-08-22** (502pp, text-extracted; the render happened 2026-08-18, after the 2026-08-17 fix). pp.326/329 print `Parity of (D & S)` and `Parity of ((D & !S) == 0)` with the operator intact and the columns in register.


**Found:** 2026-08-17, verifying the six generated wave PDFs page by page. The compile log
reported **zero errors**; the defect was visible only on the page.

**Location:** `platform/filters/p2kb-platform-tables.lua` — the `cell_to_latex` helper in the
9-column instruction-encoding table handler. Visible at **P2-Assembly-Language-Manual pp.326
(TEST) and 329 (TESTN)**, sourced from `part-ii/instructions-t.md:38` and `:169`.

**Mechanism.** That handler flattens each cell with `pandoc.utils.stringify()` and emitted the
result verbatim. The near-identical 6-column handler beside it, at the same file, has always run
`text:gsub("&", "\\&")` plus `%`, `#`, `_`. So one of two adjacent code paths escaped and the
other did not. An unescaped `&` inside a `tblr` cell **is an alignment tab**: it ends the cell,
shifts every later column one to the right, and pushes the row past the table's right border —
which is what the 50.2pt overfull hbox in the log actually was.

The reader sees the TEST row's C column as `Parity of (D` and the next cell as `S)`. **The AND
operator is gone from a bit-level definition of what the instruction computes**, and the row's
remaining columns are all off by one. It has been shipping this way since at least v3.1.5.

**`%` is the worse latent case.** Through the same unescaped path it would comment out the rest
of the row — silent, complete, and with a clean log. Same class as F-281.

**Blast radius measured, not assumed:** 281 nine-column encoding tables across the manual,
scanned for `&`, `%`, `#`, `_` outside code spans. **Exactly 2 hits, both `&`, both in
`instructions-t.md`; zero `%`/`#`/`_` anywhere in that path.** The other five wave elements
contain no nine-column encoding tables and were verified unaffected. The five `&` sites elsewhere
in Assembly and deSilva all go through escaping paths and render correctly — checked in the `.tex`,
not inferred.

**Fix applied:** the 9-column helper now escapes the same four characters as its sibling. Since
`stringify()` has already flattened the cell to plain text, no intentional LaTeX can be harmed.

**Owed:** re-render `p2-assembly-language-manual` v3.1.6 and confirm pp.326/329 read
`Parity of (D & S)` and `Parity of (D & !S)` inside a 9-column row. The platform file is staged.
No version bump — v3.1.6 has not shipped.

**Lesson.** The gate that would have caught this does not exist: we check source characters and we
check compile logs, and this defect is invisible to both. It was found by rendering a page and
looking at it, prompted by triaging an overfull-hbox count. **An overfull hbox in a table is worth
opening**; it is the only signal this failure emits.

### F-286 — the escaping that stops F-284's class was per-call-site discretion, so it drifted to five more raw-emission sites. `RESOLVED`

> **VALIDATED against the released v3.1.6 PDF, 2026-08-22** (502pp, text-extracted; the render happened 2026-08-18, after the 2026-08-17 fix). Assembly exercises the class: headings `2.2.2 The _RET_ Condition`, `3.3.1 The IF_x Prefix`, `B.3 The _RET_ Condition (EEEE=0000)` and `Mode %00000 - %00011: ...` all print correctly in the body **and** in the TOC, and a whole-document sweep finds **zero** literal `\_`, `\%`, `\&` or `\#` escape leakage.


**Found:** 2026-08-17, asking the process question after F-284/F-285: *what would routinely catch
these?* The answer turned out to be a structural fix rather than a checklist.

**The class.** A pandoc Lua filter that calls `stringify()` and emits the result inside a
`RawBlock` bypasses pandoc's escaping entirely. `stringify()` flattens an element to plain text,
so nothing in the result is intentional LaTeX — but `&` in a raw position IS an alignment tab, and
`%` silently comments out the rest of the line **with a clean compile log**. F-284 was one instance.

**The rule already existed, written down, with rationale — and was applied at one site in four.**
`p2kb-platform-code-coloring.lua` carried a comment stating the principle exactly ("Special LaTeX
characters in the title are re-escaped because the title text, once parsed by Pandoc, is emitted
into a raw-LaTeX block"), and its `esc()` helper was declared **inside a single `elseif` branch** —
so the sidetrack handler 100 lines below, which that very comment cites as using "the same
addcontentsline technique", emitted its title unescaped. `p2kb-platform-pagination.lua` was the same
shape: a `latex_escape()` helper at line 26, used for chapter subtitles, **not** used for the Part
title 28 lines below.

**Five unescaped raw-emission sites, all fixed:**

| Filter | Site | Raw position |
|---|---|---|
| `p2kb-platform-pagination.lua` | Part title | `\manualpart{}` |
| `p2kb-platform-figures.lua` | figure caption | `\caption{}` |
| `p2kb-platform-code-coloring.lua` | sidetrack title | `\addcontentsline{}{}{}` |
| `p2kb-platform-tables.lua` | table caption `stringify` fallback | `caption={}` outer key |
| `p2kb-platform-tables.lua` | cell renderer `pandoc.write` fallbacks (×3) | `tblr` cell |

Escaping is now a module-level helper in each filter with the invariant stated at its definition,
rather than a decision re-made at each call site. That is the actual fix: **per-call-site escaping
drifts; one shared helper is why it stops drifting.**

**Blast radius measured, not assumed — zero live exposure.** All 38 `# Part` headings and all
`figurecaption` divs across the live masters were scanned for `&` and `%`: the only hit is in a
`creation-guide.md` (not a rendered master). So the change is **inert on today's content** and the
five already-verified wave renders remain valid. The `tables.lua` cell-renderer holes are fallback
paths that fire only when `pandoc.write` fails.

**Deliberate scope limit.** `tables.lua`'s helper escapes `& % # _` — the same four its cell
renderers already escaped inline — and deliberately **not** `{ } \`, because instruction tables
legitimately carry P2 syntax like `{#}` and escaping those braces would change pages that render
correctly today. Closing a hole must not move correct output.

**Retires an authoring workaround.** Authors were told to spell "and" in Part titles because an `&`
there broke the build. That restriction was a workaround for this bug and is no longer needed.

**Owed:** the Assembly render already owed for F-285 validates all of it. Confirm p.329, and confirm
Part titles and table captions still render as before.

**The process changes that came out of this — the durable half:**
1. **`latex_escape_processor.py` now hard-fails on HTML entities in prose.** Not a warning: this
   processor escapes `&`→`\&` before pandoc runs, so `&nbsp;` becomes `\&nbsp;` and pandoc emits
   the literal text. **There is no configuration in which writing an entity here works**, which is
   why it is a gate and not advice. Verified against the real pre-fix source from git: all 32
   occurrences caught at exact line/column, and silent across all 128 live master files.
2. **`engineering/tools/validation/audit-tex-artifacts.py`** — new. Sweeps the returned `.tex` (the
   only artifact showing what LaTeX actually received) for entities, raw HTML, literal markdown,
   double-escapes, `{=latex}` leaks, `??`, TODO markers. Tuned to **zero false positives** across
   all eight outbound `.tex`; its exclusions are load-bearing and documented in the script header.
   Wired into `release-manual` as step 1e0.
3. **`release-manual` no longer says to ignore overfull hboxes.** That instruction is what let F-284
   ship: a 50.2pt overfull hbox was the defect's only signal, and the skill said to disregard it.
   Now triaged by magnitude and location (≥20pt, or any inside a table ⇒ open the page). Assembly's
   log carries 7,056 overfulls of which 36 are ≥20pt, so ranking is tractable where listing is not.
4. **`release-manual` 1d′ — read the whole page you opened.** F-285 cost nothing because it sat on
   F-284's page; a narrowly-scoped check would have passed it through again.

### F-288 — an effect group in slash form is shaped exactly like a dual mnemonic, so 16 syntax forms print split across two lines. `RESOLVED`

> **VALIDATED against the released v3.1.6 PDF, 2026-08-22** (502pp, text-extracted; the render happened 2026-08-18, after the 2026-08-17 fix). All 16 forms print on one line each — `TESTP {#}Dest WC/WZ`, `TESTP {#}Dest ANDC/ANDZ`, and the TESTB/TESTBN/TESTPN sets beside them.


**Found:** 2026-08-17, during release verification of Assembly v3.1.6. Found by **reading the whole
of p.329** while confirming the F-285 repair — the repair itself is correct; this was the rest of the
page. (Third time in two days that the free evidence on an opened page carried the next defect.)

**Reader impact.** In the TESTB, TESTBN, TESTP and TESTPN entries — four syntax forms each, **16
lines** — the flag-effect group is orphaned onto its own line, with vertical gaps between the pairs:

```
TESTP {#}Dest          instead of      TESTP {#}Dest WC/WZ
WC/WZ                                  TESTP {#}Dest ANDC/ANDZ

TESTP {#}Dest
ANDC/ANDZ
```

In a reference manual's syntax block a form split across two lines reads as **two different forms**,
and these four instructions are exactly where a reader goes to learn which effects each accepts.

**Mechanism (code-verified, not inferred).** `workspace/p2-assembly-language-manual/filters/p2kb-pasm2-entry-format.lua`
inserts `\\` before every bold run that matches an instruction-mnemonic *shape*, one shape being
`^[A-Z][A-Z0-9_]*/[A-Z0-9_]+$` — intended for dual mnemonics like `CALL/RET`. **`WC/WZ`,
`ANDC/ANDZ`, `ORC/ORZ` and `XORC/XORZ` are character-for-character that same shape**, so each was
taken for a new mnemonic and given a break *before the effects*. The filter did try to exclude
effect flags — `not text:match("^{")` — but that only catches the **brace** form `{WC|WZ|WCZ}`,
which is precisely why TEST and TESTN, written that way, always rendered correctly while their
neighbours did not.

**Wider than the 16 visible lines.** The bare forms — `WC`, `WZ`, `WCZ`, `ANDZ`, `ORZ`, `XORZ`, nine
further sites — match the plain-CAPS shape and carried the same latent bug.

**The F-285 repair did not cause these defects — it ACTIVATED them.** (Corrects a first reading that
called it unrelated.) `is_syntax_paragraph()` rejects any paragraph containing a top-level word, and
the literal `&nbsp;` was exactly such a word — so in v3.1.5 the filter **never fired on these
paragraphs at all**, and the four tight lines came from pandoc's hard breaks alone. Removing the
entities made the paragraph parse as a syntax block for the first time, and the filter's latent bugs
took effect. The bugs predate v3.1.5; their visibility does not. Verified against the released v3.1.5
PDF recovered from git.

**A SECOND defect, found by reasoning about what the re-render would show before spending it.** Once
the effect-group breaks were fixed, the four forms would still have been separated by BLANK LINES:
the filter inserts `\\` before each mnemonic **unconditionally**, while the source already ends each
form with a trailing `\` — a markdown hard break pandoc renders as `\\`. The two compose to
`\\\\`, a blank line between every syntax form. The filter now honors an existing `LineBreak` and
supplies one only when the source lacks it — which preserves the reason the filter exists (forms
written on separate source lines with no hard break still get their break).

**Fix applied.** Shape-matching cannot separate these cases; **membership** can. A single
`is_mnemonic()` predicate now decides by membership in an explicit `EFFECT_FLAGS` set (handling the
brace, slash and bare forms), and **both** loops — the mnemonic count and the break insertion — call
it, so the two can never disagree about what a mnemonic is. Verified against the real token
inventory: `WC/WZ`/`ANDC/ANDZ`/`ORC/ORZ`/`XORC/XORZ`/`WC`/`WZ`/`WCZ` are not mnemonics, while
`CALL/RET`, `ABS`, `ADDCT1`, `MUL / MULS` still are. No PASM2 instruction is named `WC`, `ANDC`,
`ORC` or `XORC`, so there is no collision — and `WRC`/`WRZ`, which ARE instructions, are absent from
the flag set and stay mnemonics. Both copies of the filter (workspace + interactive-testing) fixed
and confirmed identical.

**Same class as F-286**, one day apart: a guard written for one shape, left to cover a family. The
countermeasure is the same — one predicate, one place, used by every caller.

**PROVEN ON THE FORGE DAEMON, not merely reviewed** (run `f288-syntax-v1`, 2026-08-17). A five-case
fixture was rendered and READ: the four slash-form `TESTP` forms print one per line with no gaps; the
`{WC|WZ|WCZ}` control is unchanged; bare `WC`/`WZ`/`WCZ` print inline; **and both no-regression cases
hold** — forms written without a hard break still receive an inserted break (the filter's actual
purpose), and `CALL/RET`, `WRC`, `WRZ` are still treated as mnemonics. Compile log clean on all five
serious signatures. This is what a Lua change with no local interpreter requires: the daemon, not a
code read.

**Owed:** one Assembly render (staged). **Assembly v3.1.6 is HELD from the release wave** until p.329
shows the four TESTP forms each on one line in the production build; deSilva, P2AN001 and P2AN002 are
unaffected (this filter is Assembly-local) and release without it.

### F-289 — the code-line gate skipped every CAPTIONED code block, so it reported clean on the manual whose pages were losing channels. `RESOLVED — gate repaired and all 11 IOSP sites brought under K 2026-08-17; VALIDATED ON THE RENDERED PAGES p163 + p178 of released v1.0.9, 2026-08-25 («#302»)`

**Found:** 2026-08-17, asking a plain status question about Debug Window and IOSP while waiting on the
Assembly render. Debug Window's code-line audit reported **clean** at K=76; measuring the same files
by hand found **29 code lines over 76 columns, the worst at 137 and 130** — both longer than any line
F-281 named. A gate that silently passes is worse than no gate: nobody goes looking.

**Mechanism.** `audit-code-line-length.py`'s `is_code_fence()` returned False for **any** fence info
string starting with `{`:

```python
# ```{=latex} / ```{=html} / ```{.foo} attribute syntax -> not a plain code box
if info.startswith('{'):
    return False
```

Only `{=format}` is a raw passthrough. Pandoc **attribute** syntax —
```` ```{.spin2 caption="ch07-scope-three-channel.spin2"} ```` — IS a code box, and it is the
**captioned** form: exactly the form paired with an `examples-library/` file under the byte-identity
rule. So the gate excluded the blocks that carry the shipped examples.

**Fleet exposure: 56 captioned blocks were never gated** — Debug Window 34, IOSP 15, Getting Started
4, deSilva 3.

**This is how F-281 shipped.** Both Debug Window lines that lose a whole channel on the page
(`ch07-scope.md:272`, 121 cols → the third SCOPE channel; `ch06-logic.md:310`, 113 cols → the third
LOGIC channel and the closing paren) sit in captioned fences. The gate declared the manual clean
while two of its pages were dropping code.

**Fixed:** skip only `{=`. The `{=latex}` exemption still holds — verified: `ch03-term.md:73` (137
cols) and `ch05-plot.md:784` (130 cols) are raw passthrough and are correctly still ignored.

**The true picture, now that the gate measures what it claimed to:**

| Manual | over K=76 | past the ~101-col render cliff |
|---|---|---|
| Debug Window (v1.1.2 released) | 24 | **3** — the F-281 trio |
| IOSP (v1.0.8 released) | 11 | **2 — NEW, and shipped** |
| deSilva · Assembly · Streamer · XBYTE · Architect · Getting Started | 0 | 0 |

**TWO SHIPPED IOSP TRUNCATIONS, verified on the released PDF by rendering the pages and looking:**

1. **p178** (`chapter-11-serial-transmit.md:433`, 103 cols) — `reversed := value REV 7` keeps its code,
   but the trailing comment runs past the code box's right border and is cut at the page edge:
   *"...for MSB-first (REV n covers bits 0.."* — the closing `n)` is gone.
2. **p163** (`chapter-10-dac-output.md:462`, 102 cols) — `WXPIN(AUDIO_PIN, …)` keeps its code; the
   comment is cut mid-word at *"a 256-clock multipl"*.

**Severity: below the F-281 SCOPE/LOGIC cases.** In both IOSP sites the CODE is intact and only a
comment tail is lost, so no reader can build a wrong program from them — but the line visibly
breaches the box border, and a truncated explanatory comment is still a reader-facing defect in a
published manual. Neither is a regression: both predate v1.0.8 (`git diff` against the tag shows the
lines unchanged).

**A first-match verification nearly missed this**, twice in one investigation: `reversed := value REV
7` appears on **p175 and p178**, and p175 (a different method, comment moved above the code) renders
perfectly. Checking only the first hit would have cleared a defect two pages later — the same trap
as F-284's `Parity of (D & S)` resolving to p414 instead of the instruction pages.

**Action:** both IOSP sites are repaired by the sanctioned comment fix (move it above the instruction,
as `spi_tx_msb_first` on p175 already does — the manual's own neighbouring example shows the form).
Rides IOSP **v1.0.9**, which is already owed a CHANGELOG entry. Debug Window's trio and its 21 other
over-budget lines ride **v1.1.3**. *(This sentence originally added "and the `breaklines` platform fix
may change what re-authoring is still needed there." It does not — `breaklines` was **REJECTED** later
the same day, see [[F-281]]. Nothing at render time rescues an over-wide line; authorship plus this
repaired gate is the whole mechanism. Corrected 2026-08-19.)*

**Done 2026-08-17 — and the scope was 11, not 2.** Repairing only the two cut sites would have left
nine lines over budget, one of them (`chapter-07-pulse-transition.md:306`, **88 cols**) past the
86-column box border and therefore already spilling into the margin — a visible defect, not a lucky
one. All 11 were brought under K=76 by the sanctioned form: standalone comment blocks rewrapped,
trailing comments moved to their own line above the instruction. Five captioned examples changed in
lockstep with their masters.

**Verified, not assumed:** code-line gate clean across all 30 IOSP masters (was 11 failures);
`verify-example-corpus-identity.py` GREEN 15/15; all five changed examples compile clean under
`pnut-ts -d`. **`pdftotext` reported the p163 comment complete while the rendered page cut it
mid-word at "multipl"** — the text object exists off-page, so extraction is not evidence of what
prints. The page image is.

> **CLOSED 2026-08-25 («#302») — CONFIRMED ON THE PAGE, not on the changelog line.** IOSP
> **v1.0.9** rendered and released 2026-08-18 (`deliverables/documents/DOCs/P2-IO-and-Smart-Pins-User-Guide.pdf`,
> 396pp). Both sites this finding left owed were **rasterised at 150dpi and looked at**, because
> this entry's own lesson is that `pdftotext` reported the p163 comment complete while the page cut
> it mid-word:
>
> - **p163** (`Chapter 10: DAC Output`, Example 2) — the three-line comment *"Initialize audio DAC.
>   The PWM-dither sample period must be a multiple / of 256 clocks, so 44.1 kHz is not exactly
>   achievable: truncating the / period to 4352 clocks yields ~46 kHz (200 MHz / 4352)."* sits
>   **above** the instruction and every line ends inside the code box. The `' Period, rounded down
>   to a 256-clock multiple` line — the one that used to be cut at *"multipl"* — is complete.
> - **p178** (`Chapter 11: Serial Transmission`, Example 2) — `' MSB first: reverse the 8 data bits
>   (REV n covers bits 0..n)` prints in full, closing paren included, with `reversed := value REV 7`
>   on its own line below it.
>
> **The first-match trap this entry warned about was honoured:** `reversed := value REV 7` occurs on
> **both** p175 and p178 in v1.0.9, and p178 — the later, formerly-broken one — is the page verified.
>
> **The repaired gate is still clean at source:** `audit-code-line-length.py` over all 30 IOSP
> masters exits 0, "no code line over K=76" (was 11 failures). Debug Window's masters likewise exit 0.

**Owed: nothing.**

### F-290 — nothing continues a `debug()` directive line: the Spin2 `...` and CON symbols both compile clean and ship a different program. `RESOLVED` — **mechanism established 2026-08-17; guidance corrected at ALL THREE touch points 2026-08-25 («#302»); the repaired line verified on the released page**

**Found:** 2026-08-17, looking for a way to bring `ch06-logic.md:310` (113 cols) under K without
losing what the example teaches. Both candidate fixes were compiled and the emitted binary inspected
rather than trusted.

**A `debug()` backtick directive is a LITERAL STRING assembled at compile time. It is not Spin2
source, so no Spin2 syntax applies inside it.** Two consequences, each verified by compiling with
`pnut-ts -d` and reading the directive text back out of the `.bin`:

| Attempt | Compiles | Bytes | What actually shipped |
|---|---|---|---|
| baseline | ✅ | 9,482 | `LOGIC SPIbus TITLE 'Software SPI' SAMPLES 200 SPACING 3 'CS' 1 $00FFFF 'CLK' 1 $00FF00 'MOSI' 1 $FFFF00` |
| Spin2 `...` continuation | ✅ | **9,438** | `LOGIC SPIbus TITLE 'Software SPI' SAMPLES 200 SPACING 3 ...` — **`...` embedded literally and ALL THREE CHANNELS DROPPED.** The window would be created with zero declared channels. |
| colors as `CON` symbols | ✅ | 9,476 | `'CS' 1 C_CS …` — **symbol names embedded verbatim, never resolved.** The PC-side `KeyColor` cannot read `C_CS`, so every channel silently falls back to `DefaultScopeColors`. |

Only the `` `(expr) `` form substitutes a value into a directive; a bare token is text.

**PROCESS DEFECT THIS EXPOSES — `prepare-manual`'s sanctioned fix is wrong for this line class.**
The code-line gate's guidance reads: *"for a **code** overflow, break at a logical boundary with the
legal Spin2 `...` line-continuation."* That is correct for ordinary Spin2 statements and **silently
destroys a `debug()` directive** — which is the majority of the over-long lines in the Debug Window
manual, i.e. exactly the population the guidance is aimed at. Corrected in the prepare-manual
project overlay.

**Same family as the trailing-`-` trap** already recorded under F-281 (compiles clean, 9,338 vs 9,408
bytes). The generalization is now explicit rather than one anecdote: **a `debug()` directive line
cannot be continued at all — it can only be shortened.** Byte-comparing the binary against the
one-line form is what catches it; the compiler never will.

**Applied to the LOGIC line (F-281, agreed with Stephen):** the create line drops `TITLE`, `SAMPLES`
and `SPACING`, reaching **70 cols** and keeping all three named channels with their exact hex colors:

```
  debug(`LOGIC SPIbus 'CS' 1 $00FFFF 'CLK' 1 $00FF00 'MOSI' 1 $FFFF00)
```

Costs nothing pedagogically — **checked, not assumed**: Chapter 6 already teaches all three dropped
keywords 250 lines earlier (a table row each at 69–72, prose deriving `SAMPLES × SPACING` = window
width at 87–89, and a prior worked example using `SAMPLES 64` at line 46). The over-long line sits in
*"A complete software-only example"*, whose job is the SPI flow, not re-teaching configuration. No
published figure is tied to that example, so nothing needs regenerating. Verified: compiles clean
under `pnut-ts -d`, the emitted directive carries all three channels, and the printed block is
byte-identical to `examples-library/ch06-logic-spi-bus.spin2`.

**Also ruled out, and left as a bench question:** dropping the explicit `1` counts. `LOGIC_Configure`
reads the next token as `count` via `KeyValWithin(v, 1, 32)` **before** reading the color, and whether
a failed count consumes the token is not determinable from the manual's REF. If it consumes, the color
is lost silently. Not usable without a PNut/bench check — which is also why the explicit `1` is
probably load-bearing in every channel declaration in the manual.

**Debug Window's remaining line work:** 23 lines over K=76, **2 still past the ~101-col cliff** —
`ch07-scope.md:272` (121, the SCOPE channel case, source-determined split available) and
`ch14-multiwindow-pasm.md:299` (110, trailing comment only, comment-above fix).

> **CLOSED 2026-08-25 («#302»). The mechanism half was done on 2026-08-17; the GUIDANCE half was
> only half done, and that is what this closure completes.**
>
> **The guidance defect was still live in the place a reader actually reaches.** This entry recorded
> the fix as *"Corrected in the prepare-manual project overlay"* — and it was. But
> the `prepare-manual` skill (agent-side) still stated the destroying rule **twice, unqualified**:
> `:194` (Step 4, code-line gate) — *"for a code overflow, break at a logical boundary with the
> legal Spin2 `...` line-continuation (or aggregate into a named CON)"* — and `:201` (Step 5,
> compile certification) — *"A long line is shortened with the legal Spin2 line continuation `...`
> … (verified: compiles to the identical value)"*, whose verification is exactly the clean-compile
> this finding proves is worthless here. A rule stated correctly in the overlay and incorrectly in
> the body is the drift shape this project already named: **three touch points, and only one was
> fixed.** Both now carry the `debug()` carve-out inline and point at the overlay for the evidence.
>
> **The manual-side line is verified on the artifact, not the changelog.** The repaired form is
> byte-identical across all three places it must agree:
> - master `ch06-logic.md:311`
> - `examples-library/ch06-logic-spi-bus.spin2:25`
> - **released v1.1.3 PDF** (`P2-Debug-Window-Manual.pdf`), which prints
>   `` DEBUG(`LOGIC SPIbus 'CS' 1 $00FFFF 'CLK' 1 $00FF00 'MOSI' 1 $FFFF00) `` — all three named
>   channels with their exact hex colors, the outcome the `...` form destroyed.
>
> **Both cliff lines are gone at source:** `audit-code-line-length.py` over the Debug Window masters
> exits 0, "no code line over K=76" — so the 23-over-budget population and both >101-col cases are
> closed, not merely reduced.
>
> **The bench question is NOT closed by this entry and is deliberately carried:** whether a failed
> `KeyValWithin(v, 1, 32)` count consumes its token is still undetermined, so the explicit `1` in
> every channel declaration stays load-bearing and must not be dropped to save columns.

### F-291 — the escaper missed two code contexts, so five lines of a released manual print a literal backslash. `RESOLVED` — **escaper fixed + sweep extended 2026-08-17; BOTH RELEASED PAGES CONFIRMED CLEAN in v1.1.3, 2026-08-25 («#302»)**

**Found:** 2026-08-17, testing F-278's deferred question (does `> ```antipattern` render inside a
blockquote?) on the daemon before risking a production render. The answer is **yes** — but the test
page showed the code inside the blockquote as `DEBUG(\`SCOPE\_XY W 128 'A')`, with a literal
backslash, while the identical pair *outside* the blockquote rendered `SCOPE_XY` correctly.

**Five lines are affected in the RELEASED Debug Window v1.1.2**, verified by extracting the shipped PDF:

| Page | Prints | Context |
|---|---|---|
| p88 | `DEBUG(\`SCOPE\_XY W 128 'A')` and the `W SIZE` line beside it | fenced block **inside a blockquote** |
| p159 | `PC\_KEY`, `PC\_MOUSE`, `DEBUG\_END\_SESSION` | **double-backtick** inline spans |

**Mechanism — two blind spots in `latex_escape_processor.py`, both proved by probe:**

| Context | Before | Correct? |
|---|---|---|
| prose | escapes `_`→`\_` | ✅ right |
| `` `single span` `` | protected | ✅ right |
| ``` ``double span`` ``` | **escaped** | ❌ → p159 |
| fenced block | protected | ✅ right |
| `> ` fenced block | **escaped** | ❌ → p88 |
| quoted prose | escapes | ✅ right |

1. **Fence detection was not blockquote-aware.** It tested `line.strip()`, which leaves the `> ` in
   place, so `> ```spin2` never registered as a fence; the body was treated as prose and escaped.
   Fixed by stripping leading blockquote markers before the fence test only — quoted *prose* must
   still escape exactly like unquoted prose, and it does.
2. **Double-backtick spans were unmatched.** The inline pattern is `(?<!`)(`[^`\n]+`)`: its body
   excludes backticks and it refuses a preceding backtick, so ``` ``DEBUG(`Name `PC_KEY(@v))`` ```
   — the form used precisely *because* the content contains a backtick — fell through to prose.
   Fixed by protecting double-backtick spans before single ones.

**Why the escaped character PRINTS rather than escaping:** both contexts still render verbatim
downstream, and inside verbatim `\_` is two literal characters. The escape was never wrong in
LaTeX terms; it was applied where LaTeX rules do not apply.

**`audit-tex-artifacts.py` (F-286) MISSED this, and now does not.** The sweep excluded verbatim
regions wholesale — correct for every other check, since code legitimately contains almost every
signature. But *inside* verbatim a backslash-escaped special is the one thing that IS a defect, so
the sweep now scans verbatim for exactly `\_ \& \# \% \$`. Verified it flags the leak and does
**not** flag legitimate PASM2 `#\label` (that is `\l`, not in the set) or correct prose escaping.
**A skip-list is an assumption, and this one had a hole in it.**

**Fixed and verified:** the staged Debug Window markdown now carries `SCOPE_XY`, `PC_KEY`,
`PC_MOUSE` and `DEBUG_END_SESSION` clean in their code contexts, while prose occurrences still
escape correctly (38 legitimate `\_` remain, all prose).

**F-278's deferred site is now converted.** With the fence-in-blockquote combination proven to
render — red antipattern box, correctly indented inside the quote, trailing quoted prose intact —
`ch08-scope-xy.md`'s wrong/right pair is split: the wrong form is an `antipattern` block, the
correct form a `spin2` block beside it, matching the Chapter 12 treatment. Rides v1.1.3.

> **CLOSED 2026-08-25 («#302») — measured on the RELEASED v1.1.3 PDF with the same instrument that
> found the defect.** This finding was detected by extracting the shipped v1.1.2 PDF and counting
> literal `\_`; the count was **5**. Re-run over `P2-Debug-Window-Manual.pdf` at v1.1.3: **0**, in
> all 168 pages. Both named pages were then rasterised and looked at (the page numbers moved by one
> between releases, so they were re-located by content rather than reused):
>
> - **p87** (was p88) — `` DEBUG(`SCOPE_XY W 128 'A') `` prints a clean underscore, inside the red
>   antipattern box, with `' WRONG -- 128 follows no keyword` beside it. The fence-in-blockquote
>   combination and F-278's conversion both render as designed.
> - **p159** — `PC_KEY`, `PC_MOUSE` and `DEBUG_END_SESSION` all print clean underscores in the
>   Appendix A command list, including inside the double-backtick spans that were the second blind
>   spot.
>
> **The extended `audit-tex-artifacts.py` sweep is the durable half** and is unaffected by this
> closure: it now scans verbatim regions for exactly `\_ \& \# \% \$`, which is what makes this
> class visible at source instead of only on a returned PDF.

### F-292 — six printed snippets teach a `...` continuation inside `debug()`, so each one silently ships a different program. `RESOLVED — all six repaired 2026-08-17 and shipped in Debug Window v1.1.3; ALL SIX PRINTED SNIPPETS CONFIRMED ON THE PAGE 2026-08-25 («#302»)`

**Found:** 2026-08-17, answering "any more outstanding issues with this manual?" after F-290
established that a `debug()` directive cannot be continued at all. Searching the masters for the
pattern found six.

**Proved, not inferred.** The ch07 snippet compiled exactly as printed emits
`Waves 'Sine'  -1000 1000 100   0 0 $00FF00 ...` — **the `'Tri'` and `'Noise'` channels are gone**
and the literal `...` is embedded (9,328 vs 9,393 bytes). A reader who copies it gets a one-channel
scope where the page shows three.

| Site | Reader silently got | Route taken | Authority |
|---|---|---|---|
| `ch07-scope.md:109` | 1 of 3 SCOPE channels | three separate feeds | `SCOPE_Update` accepts a channel def and `vIndex` only resets in `SetDefaults` |
| `ch09-fft.md:163` | `'Left'` only, no `'Right'` | two separate feeds | `FFT_Update` accepts "CLEAR/SAVE/PC_KEY/PC_MOUSE **+ channel-defs** + samples" |
| `ch04-bitmap.md:144` | palette truncated at entry 7 | LUTCOLORS as its own feed | REF: "Replace LUT palette entries at runtime"; the house form is proven by generator `fig-13-packed-bitmap-frame.spin2` |
| `ch03-term.md:166` | colour pairs 2 and 3 lost | one line (`SIZE` dropped to fit) | `COLOR` is **config-only** for TERM — no `key_color` arm in `TERM_Update` |
| `ch10-spectro.md:145` | everything after `TRACE 12` lost | one line + waiver | `SPECTRO_Update` accepts only CLEAR/SAVE/PC_KEY/PC_MOUSE |
| `ch10-spectro.md:166` | everything after `TRACE 8` lost | one line + waiver | same |

**Verified by compiling all six fixed forms together and reading the emitted directives:** every
channel, colour pair and config keyword is present, and **zero** literal `...` remain in the binary.

**Why every gate missed them, and this is the transferable part.** These are *uncaptioned*
illustrative snippets — not paired with an `examples-library` file, so never compiled — and each
PHYSICAL line was short, because the `...` is what made them fit. So the width gate saw nothing and
the compile gate never ran. **The defect lived exactly in the gap between "too wide to print" and
"too broken to run", and neither gate covers it.** Extending compile certification to uncaptioned
fragments is a real question (fragments must be wrapped to compile) and is deliberately NOT decided
here.

**One pedagogical change, flagged rather than buried:** `ch04-bitmap.md`'s palette demo moves from
LUT4 with sixteen entries to **LUT2 with four** (pixels `& $03`), because sixteen `$RRGGBB` values
cannot fit a printable line by any means — `LUTCOLORS` overwrites from index 0, so it cannot be split
across messages either. The teaching survives intact (LUT mode, inline palette in one statement,
pixels as indices) at a smaller scale. The chapter's LUT-mode reference table still documents LUT4 as
4 bits / 16 entries.

**It also closes a punch-list question open since June.** The "Other" section asked whether the
original `fig-07` failure — a creation-line channel def drawing an empty "Channel 0" plot — "came
from a `...` line-continuation artifact." It did. The creation-line-versus-separate-feed debate was
chasing the wrong variable; the `...` was dropping the channels, so the REF source was right all
along and the TO-RECONCILE item closes on evidence rather than another capture.

> **CLOSED 2026-08-25 («#302») — every one of the six read off the RENDERED PAGE of the released
> Debug Window **v1.1.3** (`P2-Debug-Window-Manual.pdf`, 168pp, cover states "Version 1.1.3"). Pages
> rasterised at 130dpi and looked at, not extracted:
>
> | Site | Page | What the page now prints |
> |---|---|---|
> | `ch07-scope.md:109` | **p76** | all **three** SCOPE channels — `'Sine'`, `'Tri'`, `'Noise'` — as three separate feed lines under the create line |
> | `ch09-fft.md:163` | **p97** | both `'Left'` **and** `'Right'` declared, then the interleaved sample loop |
> | `ch04-bitmap.md:144` | **p35** | `LUTCOLORS $000000 $FF0000 $00FF00 $0000FF` — the whole 4-entry LUT2 palette in one statement, pixels `& $03` |
> | `ch03-term.md:166` | **p27** | all eight `COLOR` values on one line, closing paren inside the box; the two comment lines above name all four pairs |
> | `ch10-spectro.md:145` | **p106** | `SPECTRO Vert … TRACE 12 RANGE $20000 HSV16X LOGSCALE` — everything after `TRACE 12` present |
> | `ch10-spectro.md:166` | **p106** | `SPECTRO Slow … RATE 512 TRACE 8 RANGE $80000 LUMA8X` — everything after `TRACE 8` present |
>
> **Zero literal `...` continuations remain in any `debug()` directive across the masters.** Swept
> all 26 Debug Window master `.md` files: five lines end in `...` and **none is a directive** — a Spin2
> *expression* continuation in an ordinary assignment (`ch13-packed-data.md:189`, legal), a syntax
> notation (`ch05-plot.md:499` `SPRITEDEF … pixels... colors...`), two elision markers
> (`ch15-panels.md:305`, `ch12-bidirectional.md:75`) and a comment (`ch01-foundation.md:261`).

**Next finding ID after this block: F-295.**

---

### F-301 — the cross-ref filter's adopt-at-next-release rule was passed over about a dozen times, because nothing read the tracker. `CONFIRMED` — **detected 2026-08-19 by comparing the tracker against every `request.json`**

**The rule, written into `CROSSREF-FILTER-ADOPTION.md` when the filter shipped 2026-06-26:**
*"The next time each manual is released (for any reason), its release MUST add
`p2kb-platform-crossref` to that manual's `request.json` `lua_filters` and visually audit the
rendered PDF."* The tracker even names its own consumer — *"`release-manual` Phase 1/Phase 4
**should** consult this tracker."*

**Measured, not assumed.** Every workspace `request.json` read directly against the tracker's rows:

| Document | Tracker | In `request.json`? | Releases since the rule |
|---|---|---|---|
| Assembly | ⏳ pending, at v3.1.0 | **no** | v3.1.1 → v3.1.6 |
| DeSilva | ⏳ pending, at v3.0.1 | **no** | v3.0.2 → v3.0.6 |
| Debug Window | ⏳ pending, at v1.0.1 | **no** | v1.0.2 → v1.1.3 |
| Getting Started | ⏳ pending, at v1.0.0 | **no** | v1.0.1 → v1.0.3 |
| Architect | ⏳ "in development" | **no** | released v1.0.3 |
| XBYTE | **absent from the table** | **no** | v1.0.0, v1.1.0 |
| 7 app notes | **absent from the table** | **no** | 20+ |
| IOSP | 🔧 adopting (pilot) | yes, ordering correct | audit never recorded |
| Streamer | ✅ adopted + audited | yes, ordering correct | — |

**Only two of fifteen ever adopted.** IOSP's row still reads "awaiting Stephen's regen + visual
audit" although it has released three times since, so its filter has certainly rendered — the
**audit** is what is unrecorded, and that half is the half that matters (a mis-fired auto-link is
exactly what the audit exists to catch).

**The statuses are not wrong. Nothing read them.** Every row above is an accurate record of a
decision that was then never consulted at the moment a release happened. This is the same failure
as [[F-281]]'s «#250» in a different costume — a correct record that is not where the decision gets
made — and it is why adoption state moved into `PLATFORM-FEATURE-ADOPTION.md`, which
`prepare-manual` consults on every prepare rather than "should" consult on release.

**FIX — structural, landed 2026-08-19:** one per-document × per-feature matrix
(`PLATFORM-FEATURE-ADOPTION.md`), seeded from **detected** state rather than from what each tracker
claimed, plus a `prepare-manual` check that surfaces a document's outstanding ⏳ features as work
owed **this** release. `CROSSREF-FILTER-ADOPTION.md` keeps the mechanism (including the mandatory
crossref-before-tables ordering) and its status table is frozen as history.

**Still owed per document:** the adopt + visual audit itself, at each document's next release —
that has not been shortcut, only made visible. **ssdb and pnut-term-ts release next and both sit at
⏳**, so they are the first two chances to stop the count growing.

> **RE-MEASURED 2026-08-25 («#302») — read out of every workspace `request.json`, not off the
> tracker, and the two agree row for row.** `p2kb-platform-crossref` present in the `lua_filters`
> list:
>
> | | Documents |
> |---|---|
> | **ADOPTED (4)** | Assembly Reference · I/O & Smart Pins · Streamer Guide · **PNut-Term-TS User Guide** |
> | **⏳ still owed (11 P2 documents)** | Architect's Guide · Debug Window · Getting Started · DeSilva · XBYTE · Single-Step Debugger · P2AN001…P2AN007 |
> | out of scope | `ai-privacy-guide`, `Donna-Manuscript` (private, non-P2), `p2-layout-torture-test` (instrument) |
>
> **The count stopped growing, which is the first evidence the structural fix works.**
> `pnut-term-ts-user-guide` was one of the two "first chances" this entry named, and it **took**
> the feature — adopted **and audited 27 of 27 on the returned PDF** (2026-08-23), the audit half
> that IOSP's pilot row never recorded. The other named chance, **Single-Step Debugger, is still
> ⏳** and is the next test of it.
>
> **This stays `CONFIRMED` because the per-document work is genuinely outstanding, not because
> anything is unknown.** Two things ride every future adoption and must not be dropped:
> **`p2kb-platform-crossref` MUST sit between `figures` and `tables`** (`tables` flattens each cell
> to a string and would leave table-borne refs dead — verified ordering in all four adopted
> `request.json`s), and **the visual audit on the returned PDF is the half that matters**, because
> a mis-fired auto-link is exactly what it exists to catch.

### F-300 — every published PDF in the set ships with empty Title and Author properties. `PENDING-VALIDATION` — **MECHANISM LANDED + PROVEN 2026-08-19; 2 of the 15 published PDFs have adopted, 13 owed at their next render (measured 2026-08-25, «#302»)**

> **ADOPTION MEASURED ON THE ARTIFACTS, 2026-08-25 («#302») — `pdfinfo` over every file in
> `deliverables/documents/DOCs/`, not read off the tracker.**
>
> | State | Count | Which |
> |---|---|---|
> | **Title + Author + Subject + Keywords populated** | **2** | Assembly Reference (`P2 Assembly Language Reference Manual` / `Iron Sheep Productions, LLC`), Streamer Guide (`P2 Streamer Programming Guide` / same) |
> | **all four fields still EMPTY** | **13** | Getting Started · I/O & Smart Pins · DeSilva · Debug Window · Architect's Guide · XBYTE · P2AN001…P2AN007 |
>
> The mechanism is also proven on two documents that are **not yet published to `DOCs/`**
> (Single-Step Debugger, PNut-Term-TS User Guide), so four conversions exist in total.
>
> **This stays `PENDING-VALIDATION`, and it closes per document, on a render — never on an edit
> here.** Each of the 13 adopts by rendering on `EXEC_ENV_CANONICAL`; there is no container-side
> action that can advance it. Per-document state is `PLATFORM-FEATURE-ADOPTION.md`, which
> `prepare-manual` consults, and the measurement above agrees with it row for row.
>
> ⚠️ **`pdfsubject` IS being populated**, contrary to this entry's step 4 (*"Do NOT wire
> `pdfsubject`"*): both adopted PDFs carry a `Subject`. That does not misreport either of them —
> neither appears in **F-317**'s drift table — but it means F-317 is **live at every adoption**, not
> deferred, and each of the 13 must have its `request.json` subtitle reconciled to its printed cover
> **before** it renders.

> **RESOLUTION (2026-08-19).** The fix is **not** the one-line `pdfusetitle` this entry proposed —
> that would have populated the info dictionary and left the cover as a second hand-maintained copy
> of the same five strings, and would have shipped *wrong* titles on 9 of 15 (see the template table
> below). What landed instead: **every identity string lives once, in the document's `request.json`
> metadata, and reaches both the PDF info dictionary and the cover page from there**, via
> `\DocTitle`/`\DocSubtitle`/`\DocVersion`/`\DocDate`/`\DocAuthor` defined in
> `p2kb-platform-foundation.sty` (§ DOCUMENT METADATA). The macros carry the *value*; the cover keeps
> its *presentation*.
>
> **Proven on the interactive daemon, four round-trips, by reading the rendered PDF** — not the
> success flag. Both first converts (Single-Step Debugger, PNut-Term-TS User Guide) came back with
> compile logs clean on every serious signature and Title/Author/Subject populated for the first
> time, covers rendered and looked at. Commit `09958b0a`.
>
> **Unconverted documents are safe:** the foundation `\providecommand`s all five macros empty, so a
> template that has not opted in writes exactly what it wrote before. **Per-document adoption state
> is `PLATFORM-FEATURE-ADOPTION.md`**, and `prepare-manual` now reads it. The analysis below stands
> as the record of how the fix was found; only the proposed one-liner is superseded.

**Surfaced by** the Streamer v1.0.9 release verification — reading the delivered PDF's metadata
dictionary, then checking whether it was a Streamer regression. It is not: **all 15 PDFs in
`deliverables/documents/DOCs/` report `(empty)` for both `title` and `author`** — eight manuals and
seven app notes. Only `creator` (`LaTeX with hyperref`) and `producer` (`xdvipdfmx`) are set.

**What a reader sees.** A PDF viewer's title bar and Document Properties fall back to the *filename*
instead of the document's name, and anything indexing the file — a search tool, a library, a
citation manager — finds no title or author to key on.

**The mechanism, traced end to end.** The `.latex` template sets `\title{P2 Streamer Programming
Guide}` (generated `.tex` line 31), and `p2kb-platform-foundation.sty:259` sets a `\hypersetup`
block — but that block configures **only** link colors and bookmarks. It never sets `pdftitle` or
`pdfauthor`, and **hyperref does not derive them from `\title{}` on its own**; that requires either
`pdfusetitle` or explicit keys. So the title exists in the document body and never reaches the PDF
info dictionary.

**FIX (one line, in the shared platform):** add `pdfusetitle` — or explicit
`pdftitle={...}, pdfauthor={...}` — to the `\hypersetup` block at
`p2kb-platform-foundation.sty:259`. **Zero layout risk**: it writes the PDF info dictionary only and
cannot reflow a page. This is what distinguishes it from [[F-299]], which is parked because it
*does* move type.

**Corrects a claim in our own process doc.** The `prepare-manual` skill states that a `request.json`
metadata change "feeds PDF properties, not just the build." For this manual-production path that is
**not true** — the template hardcodes `\title{}`, and nothing carries `request.json`'s
`metadata.{title,author,version}` into the PDF info dictionary. Re-staging `request.json` on a
document switch is still mandatory for a different and real reason (input/template/filters), so the
rule stands; only its stated justification about PDF properties is wrong. Fix that sentence when the
platform fix lands.

**Sequencing.** No manual should re-render just for this. Let it ride with the next render each
document takes anyway, and take it in the same set-wide sweep as [[F-299]] — one `forge-test` pass,
two set-wide render changes.

> **Stale reference removed 2026-08-19.** This sentence named the fancyvrb `breaklines` work «#250»
> as a third member of the sweep. That work was **REJECTED 2026-08-17** on the round-trip evidence
> (see [[F-281]]); the reference was written after the rejection and never checked against it. The
> sweep is F-300 + F-299, and F-299 is polish. There is no breaklines work to schedule.

⚠️ **TRAP FOR WHOEVER TAKES THIS FIX — the two title sources already disagree.** Because nothing
consumes `request.json`'s metadata today, nobody has had to keep it in step with the cover, and it
has drifted. On the Streamer: the **cover** reads *"Comprehensive Reference for Propeller 2 Streamer
Hardware"* while `request.json` reads *"Comprehensive Reference for the Propeller 2 Streamer"*. The
moment `pdftitle`/`pdfsubject` start being populated, whichever source the fix wires up becomes
reader-visible, and a stale one ships silently. **Before adopting: audit cover-vs-`request.json`
across all 15 documents and reconcile, then decide which source is authoritative** (the cover is
what a reader actually sees, so it should win). Do not wire the metadata through without that pass.

**THAT AUDIT IS NOW MEASURED (2026-08-19), and the drift is systemic, not a Streamer typo.** Comparing
each master's cover block (`\fontsize{36}…\bfseries` title + `{\Large\itshape …}` subtitle) against
its `request.json` `metadata.subtitle`, over the 15 published documents:

| Verdict | Count | Which |
|---|---|---|
| **SAME** | 3 | Architect, Assembly, Getting Started |
| **DRIFT** | 8 | Debug Window, Streamer, P2AN001, P2AN002, P2AN003, P2AN004, P2AN005, P2AN007 |
| **cover block not matched by this scan** | 4 | IOSP, deSilva, XBYTE, P2AN006 — a different cover shape, **unresolved, not clean** |

**Two of the drifts are kinds of drift, not typos, and they change what the fix has to decide:**
1. **The app notes disagree structurally.** `request.json` carries a *catalog label* — "Application
   Note P2AN001 — No External ADC" — while the cover carries a *reader subtitle*: "No external ADC —
   a single-pin instrumentation ADC…". Neither is a stale copy of the other. Wiring the cover through
   verbatim drops the P2AN00N designator from the PDF's Title; wiring `request.json` through gives
   every app note a title that is not what its cover says. **Decide this before touching the
   platform** — likely `pdftitle` = title + designator, `pdfsubject` = the reader subtitle.
2. **Cover strings contain LaTeX.** PNut-Term-TS's cover subtitle carries a literal `\\` line break.
   PDF info-dictionary fields are plain text, so any such markup must be stripped, not passed through
   — one more reason `pdfusetitle` (which takes `\title{}` as-is) is not automatically the right
   mechanism for the subtitle half.

Truncation was not checked: two of these subtitles run past 50 characters and the register scan
compared full strings, so the counts above are exact for equality but say nothing about length limits.

---

**⚠️ THE SUBTITLE DRIFT IS NOT THE GATE. The gate is the templates, and nobody had looked at them
(traced 2026-08-19).** `pdfusetitle` populates `pdftitle` from `\title{}` and `pdfauthor` from
`\author{}` — it never touches the subtitle. So the drift table above gates only a `pdfsubject` we do
not have to wire. What actually decides whether this fix can be turned on and left to ride is what
each template declares, and **9 of the 15 declare something wrong:**

| Template `\title{}` | Documents | Verdict |
|---|---|---|
| `P2 Application Note` (hardcoded, SHARED) | **all 7 app notes** | **BROKEN** — `pdfusetitle` gives seven distinct documents one identical title. Worse than empty in a library or index. |
| `P2 XBYTE Programming Guide` | XBYTE | **STALE** — the released v1.1.0 cover reads *"P2 Interpreters & Emulators Guide"*. The template kept the pre-retitle name. |
| *(no `\title` and no `\author` at all)* | deSilva | **EMPTY** — would stay broken after the fix. |
| correct, matches cover | Architect, Assembly, Debug Window, Getting Started, IOSP, Streamer | ready |

`\author{Iron Sheep Productions, LLC}` is correct in every live template **except deSilva's**, which
has none.

**The one fact that makes all of this safe: `\title{}` is never rendered.** Every cover in the set is
hand-built in the master's `front-matter.md` (`\fontsize{36}{42}\selectfont\bfseries …`). There is no
`\maketitle` anywhere in the published set — the only one in the tree is in `ai-privacy-guide`, which
is not a published document. **So `\title{}` is metadata-only, and changing it cannot move a single
point of type on any page.** That is what turns this from a render-risk change into a ride-along.

**REVISED PLAN — prep in one commit, no renders, then ride:**
1. **Switch every live template from a hardcoded `\title{…}` to `\title{$title$}` / `\author{$author$}`.**
   `request.json` becomes the single source and a template can never go stale against its document
   again — this is what fixes the seven app notes and XBYTE at once, and it is durable rather than a
   catalog of literals to maintain. Verified safe: **`request.json` `metadata.title` equals the cover
   title for 14 of 15**, including all seven app notes (the cover carries the designator on its own
   eyebrow line — *"Propeller 2 • Application Note P2AN006"* — above the title, so nothing is lost).
2. **deSilva is the one real conflict, and it is BOTH fields.** Released cover: *"P2 Assembly
   Programming"* / *"A Human-Centered Approach to Parallel Processing"*. `request.json`:
   *"Discovering P2 Assembly"* / *"Build, Experiment, and Master the Propeller 2"*. The cover wins →
   update `request.json`, then give `p2kb-desilva.latex` the same `$title$`/`$author$` pair.
3. **Add `pdfusetitle`** to the `\hypersetup` at `p2kb-platform-foundation.sty:259`.
4. **Do NOT wire `pdfsubject`.** Leaving it out defers the whole subtitle question above at zero cost;
   revisit it as its own item whenever someone wants Subject populated.
5. **Add a `PLATFORM` ledger line and let each document absorb it at its next natural render.**
   Precedent for the standing: the 2026-07-13 mnemonic-bold line — *live-but-benign, not outstanding
   debt*. No manual re-renders for this.

**One `forge-test` still confirms three things before adoption**, none of them layout: that `$title$`
substitution actually reaches `\title{}` on this path, that `&` survives into the info dictionary
(IOSP *"P2 I/O & Smart Pins User Guide"*, P2AN006 *"Sizing Cog & Task Stacks"*), and that `pdfauthor`
lands. Read the output PDF's metadata dictionary, not the compile log.

### F-299 — wide `tblr` tables overhang the right text edge by ~5–6pt, in the platform, not the manual. `CONFIRMED` — **POLISH, NOT A GATE FAILURE: it is inside the project's own 20pt tolerance (re-graded 2026-08-19, same day, see the correction at the end)**

**Surfaced by** the Streamer v1.0.9 daemon pre-verify — a whole-document margin measurement of the
rendered PDF (every text span's `x1` against the 540pt text edge), not by the compile log, which was
clean on every serious signature in both the v1 and v2 renders.

**The defect.** Two of the Streamer's wide mode-reference tables push their rightmost column past
the text block: §6.2 *RDFAST → Pins/DACs* by **6.1pt** (`DAC Bits` header) and §8.x *Pins/DACs →
Hub* by **5.3pt** (`Hub Write` header). Visible as the table's horizontal rules extending past the
running-header rule directly above them. The compile log reports these as `Overfull \hbox
(26.6406pt too wide)` — the larger number is the whole `tblr` box including padding; the visible
overhang is the 5–6pt the measurement above reports.

**Why it is the platform's, not the manual's.** The column widths are computed by
`p2kb-platform-tables.lua`, which every manual in the set loads. Nothing in the Streamer's markdown
sets a width. A manual-side "fix" would mean hand-tuning a table the filter is supposed to own.

**NOT the two tables an earlier note predicted.** The Streamer release note expected the
`p2kb-platform-tables.lua` column fix to absorb "2 over-wide `Constant | Value | Description`
tables". These two are **6-column** `Mode | Symbol | Type | Pins | DAC Channels | DAC Bits` tables —
a different shape the fix does not reach. The prediction was not wrong about its own targets; it
was applied to the wrong pair. **A status note naming a fix is not evidence the fix covers what you
are looking at** — measure the artifact ([[feedback_status_line_is_not_evidence]]).

**Deliberately not fixed in this release.** A column-width change in
`p2kb-platform-tables.lua` reflows tables in **every** manual, so adopting it while Streamer is
mid-render means re-verifying the whole set against a changed table model for 6pt of rule overhang.
Schedule it when no manual is mid-render, and expect the absorbing manual's next render to shift
table layout. **Pair it with [[F-300]]** — both are set-wide render changes whose failure mode is a
page that looks fine in the log, and both want one `forge-test` sweep across the set rather than two.

> **Stale reference removed 2026-08-19.** This paragraph cited the fancyvrb `breaklines` work «#250»
> as the precedent it followed and the partner to pair with. That work was **REJECTED 2026-08-17**
> ([[F-281]]) — before this entry was written. The scheduling rule it borrowed is sound and stands on
> its own; the partner is F-300.

**Scope when taken:** measure every manual, not just the Streamer — the filter is shared, so any
manual with a 6-column table is a candidate.

---

⚠️ **CORRECTION, same day, before this entry could mislead anyone — I RE-GRADED MY OWN FINDING.**

I measured this with a hand-rolled PyMuPDF scan at a **4pt** threshold. **The project already has a
sanctioned instrument for exactly this** — `engineering/tools/validation/audit-pdf-margin-overflow.py`
— and I did not use it. Run against the shipped v1.0.9 PDF it reports:

```
text-block right edge: prose 540.0pt, code 540.0pt   (tolerance 20pt)
CLEAN  nothing crosses the margin (76 pages measured)
```

**The gate's tolerance is 20pt by design. These tables are 6.1pt and 5.3pt — comfortably inside it.**
So both statements are true and the second is the one that sets priority: the overhang is real and
visible if you look for it (the table rule extends a hair past the running-header rule), and it is
**not** something the project's own margin gate would ever block on.

There is direct precedent for accepting far more: the IOSP v1.0.9 PUBLISH line accepts a chart
bleeding **~24pt** past the text block on evidence — zero overlapping spans measured, every cell
readable — with the explicit note that *magnitude is never the verdict*. A 6pt rule overhang with no
overlap is a smaller version of the same accepted case.

**Re-grade: this is POLISH, not a defect owed.** Still worth taking in the set-wide sweep with
[[F-300]] because the fix is cheap once the platform is open anyway — but it must not be
described as a defect blocking anything, and no manual should re-render for it.

**The transferable lesson — the one worth more than the finding.** Reach for the project's own
instrument before hand-rolling a measurement. Mine was not wrong, but it carried **no calibrated
threshold**, so it reported a number without the judgement that makes the number mean something, and
I very nearly filed a tolerance-conformant table as a defect owed. A raw measurement is not a
verdict; the tolerance IS the verdict ([[feedback_validation_tool_verdict_is_a_claim]] — the inverse
case, where the tool PASSES and the hand-rolled scan is the one overstating).

> ### DISPOSITION CONFIRMED 2026-08-25 («#300») — the re-grade stands; nothing re-measured, nothing re-argued
>
> Carried on «#300»'s roster and **closed here as POLISH, per the same-day correction above.** The 6.1pt and
> 5.3pt overhangs sit inside this project's **20pt** margin tolerance, so
> `audit-pdf-margin-overflow.py` — the sanctioned instrument — reports the shipped v1.0.9 PDF **CLEAN across
> all 76 pages**. **The tolerance IS the verdict.**
>
> **Deliberately NOT re-measured.** A disposition already made on evidence does not get re-litigated by a
> later agent hoping for a different number; re-running the hand-rolled 4pt scan would only reproduce the
> mistake the correction above documents. **No PDF was re-graded and no manual re-rendered for this.**
>
> **Not a gap and not a defect owed** — it is scheduled work with no blocker: take it in the set-wide
> `p2kb-platform-tables.lua` sweep, paired with **F-300**, when no manual is mid-render. Nothing in this
> sprint is waiting on it, and **no document may cite it as blocking**.

### F-294 — a backtick inside a single-backtick span inverts every code span after it, printing seven lines of prose as code. `RESOLVED — span repaired at source 2026-08-17; p84 CONFIRMED ON THE RENDERED PAGE of released v1.1.3, 2026-08-25 («#302»)`

**Found:** 2026-08-17, in the same Debug Window v1.1.3 audit as F-293 — by opening p84 because the
compile log's largest overfull (57.66pt) pointed there.

**What p84 prints.** The whole "Try it" paragraph of Chapter 7 is wrecked: a sentence-initial stray
`.`, a font that flips to monospace mid-sentence and stays there for two lines of ordinary prose
(*"and observe the waveform stand still instead of scrolling. Finally, vary the trigger"*), then
words fused without spaces — `triggeroffsetbetween0,SAMPLES/2,` and `ANDSAMPLES-1'` — and a stray
closing quote. It is the most visibly broken paragraph in the manual.

**Mechanism.** `ch07-scope.md:474` wrote a **single**-backtick span whose body contains a backtick:

    (`debug(`Waves TRIGGER 0 -500 500 256)`)

Pandoc closes a single-backtick span at the *first* backtick it meets, so the span is `debug(`; the
next backtick **opens** a new one that runs until the backtick before `offset`, swallowing two lines
of prose. Every span in the rest of the paragraph is then inverted — code reads as prose, prose reads
as code — which is exactly what the page shows.

**Fixed** by the double-backtick form this manual already uses precisely for backtick-bearing content
(the same form F-291 protected in the escaper): ``` (``debug(`Waves TRIGGER 0 -500 500 256)``) ```.
Verified balanced.

**Swept fleet-wide.** All 155 master files, paragraph-wise (a code span may legally wrap across
lines, so a line-wise check false-positives on four innocent sites). **This is the only real
occurrence.** Two other flagged paragraphs are `CONVENTIONS` authoring headers inside `<!-- -->` in
the Architect and Getting Started masters — confirmed absent from both shipped PDFs.

**⚠️ This overfull was on record as adjudicated and benign.** It was carried as *"the 57.66pt overfull
is an unbreakable `\lstinline` prose run, not a code line"* — which is mechanically true and entirely
misleading: the run is unbreakable **because a span inverted**, and the paragraph around it is
broken. The note explained the symptom accurately enough to stop anyone opening the page. **An
explanation is not a verification**, and "already adjudicated" is exactly the label that keeps a
defect alive — the second time in one audit that a status line was wrong (see F-293 on Assembly).

**Gate gap.** No gate we own sees this: the escaper hands the span through, `audit-tex-artifacts.py`
sees legal `.tex`, the code-line gate measures code blocks, and the compile is clean. The only signal
was an overfull box that had been explained away. A paragraph-wise backtick-balance check on the
masters is the missing instrument.

> **CLOSED 2026-08-25 («#302») — p84 rasterised and READ, because this defect is a font change and
> text extraction cannot see one.** In released **v1.1.3** the whole "Try it" paragraph reads as
> prose in the body face, with only the genuine code spans set in monospace: `Sine`, `-1000 1000`,
> `AUTO`, `qsin`, `` DEBUG(`Waves TRIGGER 0 -500 500 256) ``, `offset`, `0`, `SAMPLES/2`,
> `SAMPLES-1`. **Every symptom this entry listed is gone** — no sentence-initial stray `.`, no
> monospace run through *"and observe the waveform stand still instead of scrolling. Finally, vary
> the trigger"*, no fused `triggeroffsetbetween0,SAMPLES/2,` or `ANDSAMPLES-1'`, no stray closing
> quote. The span inversion is fully unwound.
>
> **The double-backtick form held through the render**, which is what the fix depended on and had
> never been observed end-to-end.
>
> **THE GATE GAP THIS ENTRY NAMES IS ALSO CLOSED — and the first draft of this note said the
> opposite, which is worth recording.** This closure was initially written as *"a paragraph-wise
> backtick-balance check on the masters remains unbuilt"*. **Checked against the disk instead of
> against this entry's prose: `engineering/tools/validation/audit-backtick-balance.py` exists**,
> its docstring opens *"WHY THIS EXISTS — F-294"*, and it implements exactly the specified
> instrument, paragraph-wise for exactly the stated reason (a code span may legally wrap across a
> newline). Run over **every** manual `opus-master` tree: **CLEAN, exit 0.**
>
> ⚠️ **But it was BUILT AND NEVER WIRED.** No skill invoked it — `grep` over the skill set
> returned nothing but the file itself. It had to be run by hand, and nobody had. **A gate nobody
> invokes is a gate that does not exist**, which is F-301's defect in a different costume: a
> correct artifact that is not where the decision gets made. **Now armed** as
> `prepare-manual` **Step 6b**, beside the width/compile/ASCII source gates, so it runs before a
> render is spent rather than after a page ships wrecked.

**Owed: nothing.** Page validated; the declared instrument exists, is clean, and is now armed.


### F-293 — the escaper pre-escapes `^`, so eight exponent expressions across three manuals print a literal `^{}`. `RESOLVED — all three manuals VALIDATED on their released PDFs; the last site closed 2026-08-25 («#302»)`

> **VALIDATED against the released v3.1.6 PDF, 2026-08-22** (502pp, text-extracted; the render happened 2026-08-18, after the 2026-08-17 fix). `^{}` appears **zero** times across all 502 pages, closing the Assembly rows (p93, p209, p284 x2, p350).
>
> **THE IOSP SITE WAS ALREADY CLOSED WHEN THIS ENTRY SAID IT WAS OWED — 2026-08-25 («#302»).** This
> entry predicted the site "absorbs the escaper fix at its next render"; **that render happened on
> 2026-08-18** (IOSP v1.0.9), eight days before anyone checked, and the entry was never advanced.
> A status line lying in the *hides-work-that-is-done* direction, which is the harder direction to
> notice.
>
> **Measured, then looked at.** `^{}` across **all 15 published PDFs in `deliverables/documents/DOCs/`:
> zero, in every one** — not just the three manuals this finding named. **IOSP p320** was then
> rasterised: *"period = 2^X[3:0]^ clocks"* prints as a **true raised superscript**, no braces, no
> circumflex — the notation the entry's 2026-08-17 decision standardised on. (`chapter-16-adc.md:601`
> writes the same expression inside a **code span**, where the literal caret is correct and
> deliberate; it is not a residual site.)
>
> **The deliberate exclusion still stands:** `p2-pasm-desilva-style/opus-master/CHANGELOG.md:98`
> (`2^x`) renders into no PDF and is released history — untouched.


**Found:** 2026-08-17, auditing the Debug Window v1.1.3 render. p107's bullet reads
`multiplies the FFT output by 2^{}shift` — braces on the page.

**Eight sites, verified by extracting the shipped/staged PDFs — not inferred from source:**

| Manual | Pages | Prints |
|---|---|---|
| Debug Window (v1.1.3, staged) | p104, p107 | `2^{}shift` |
| **Assembly (v3.1.6, rendered + marked releasable)** | p93, p209, p284 ×2, p350 | `2^{}x`, `2^{}128`, `2^{}32-1`, `2^{}32` |
| IOSP (v1.0.8, RELEASED) | p320 | `2^{}X[3:0]` |

**Mechanism — a double escape, and the sources are innocent.** Every master writes plain `2^shift`
/ `2^32`. `latex_escape_processor.py` replaced a bare `^` with `\^{}` in the *markdown*; Pandoc then
read `\^` as an escaped literal caret (emitting `\^{}` itself) and escaped the two braces it found
next, producing `\^{}\{\}` — which xelatex prints as `^{}`. The escape was correct LaTeX applied one
stage too early.

**The file already carried the right precedent and did not follow it.** Line 435: *"Don't escape
tildes - Pandoc handles them fine in markdown."* A bare caret is the identical case. The caret path
even had a comment naming the failure — *"If we escape ^ to `\^{}`, Pandoc outputs literal `^{}`
which breaks LaTeX"* — but the guard built from it only protects **matched** `^text^` superscript
pairs. Unmatched carets, which is how every one of these eight is written, fell straight through.

**Fixed in three places, not one.** The prose path plus two latent copies of the same bug — the
markdown-header path (whose `XPROTECT_CARET_X` dance defends the escaper against *itself* while
leaving Pandoc's second pass untouched) and the `\section{...}` content path. No master file changed;
fixing the tool fixes all eight sites at next render.

**Matched superscript pairs are unaffected** — `2^32^` in IOSP still resolves to true superscript.
That is why IOSP shows one broken site and not four.

**Owed: nothing.** ~~re-render Debug Window, Assembly and IOSP, then confirm the listed pages print a
caret and no braces~~ — **all three rendered and all three confirmed** (Debug Window v1.1.3
2026-08-17, Assembly v3.1.6 2026-08-18, IOSP v1.0.9 2026-08-18; verified 2026-08-22 and 2026-08-25).
**Pandoc's handling of a bare caret is no longer "reasoned, not yet observed"** — the round-trip
happened and the observation is the zero-count across all 15 published PDFs plus the rasterised
p320. Local Pandoc remains off-limits and was not used.

**⚠️ This unblocks nothing and blocks one thing: Assembly v3.1.6 was recorded "verified, releasable,
nothing blocking." It carries five of the eight sites.** The verification that cleared it was
thorough about what it looked for — outline, page count, F-288's pages, log signatures — and this was
not on the list. **A verification pass is only as wide as its checklist**, which is the F-285 lesson
arriving a second time.

**RESOLVED 2026-08-17 — the set standardizes on true superscript.** IOSP's appendix-c wrote `2^32^`
(superscript) at lines 35 and 501 but `2^X[3:0]` (literal) at 171 — one document, one concept, two
renderings. All 8 literal sites are now pandoc superscript pairs, joining the 5 that already were:
**13 consistent exponents across three manuals**, verified by re-sweep (0 unmatched carets remain in
renderable prose). The tool fix alone would have printed a correct-but-inconsistent circumflex; the
notation decision is separate from it and is now made, not deferred.

**Left alone deliberately:** `p2-pasm-desilva-style/opus-master/CHANGELOG.md:98` (`2^x`). CHANGELOGs
render into no PDF (verified across all four), and it is a released entry — rewriting shipped history
to fix text nobody renders is churn, not quality.

### F-285 — `&nbsp;` prints literally in 16 instruction-syntax lines of a RELEASED manual. `RESOLVED`

> **VALIDATED against the released v3.1.6 PDF, 2026-08-22** (502pp, text-extracted; the render happened 2026-08-18, after the 2026-08-17 fix). `nbsp` appears **zero** times across all 502 pages.


**Found:** 2026-08-17, verifying the Assembly re-render for F-284. The F-284 fix was confirmed
good on p.326 and p.329 — and p.329 put this defect on screen at the same time. It is unrelated to
F-284 and was not caused by it.

**Location:** `part-ii/instructions-t.md` — 16 sites across the TESTB, TESTBN, TESTP and TESTPN
syntax blocks. Visible at **P2-Assembly-Language-Manual p.329** and neighbours as, literally:

    TESTP {#}Dest&nbsp;&nbsp;WC/WZ

**Mechanism.** The source writes `*Dest*&nbsp;&nbsp;**WC/WZ**`. Pandoc did not resolve `&nbsp;` as
an HTML entity; it treated the ampersand as literal text and emitted `\&nbsp;` into the `.tex`, so
xelatex prints the entity as characters. The escape script is not at fault — the workspace copy
still carries a bare `&nbsp;` — and it produces no warning or error at any stage.

**Not new, and not from the platform fix.** Introduced 2025-12-21 by `096230a4` ("Fix multi-page
tables and TESTP/TESTPN formatting"), present in the v3.1.5 tag's source, and therefore shipped in
at least v3.1.5. The F-284 filter change touches only 9-column table cells; these are body prose.

**It is a one-file anomaly, not a convention.** `&nbsp;` appears **nowhere else** in the manual —
not in the other 21 instruction-letter files, not in Part I, not in Part III. The TEST page's own
neighbouring syntax lines, four lines above the corrupted ones, use a plain space:
`**TEST** *Dest, {#}Src* **{WC|WZ|WCZ}**`. So the fix is to match the file's own surroundings.

**Fix applied:** all 16 `&nbsp;&nbsp;` replaced with a single space. No other file touched. No
version bump — v3.1.6 has not shipped.

**Owed:** one more Assembly render, then confirm p.329 reads `TESTP {#}Dest WC/WZ`.

**Lesson, and it is the same one twice in a day.** Both F-284 and F-285 are invisible to every gate
we own — clean log, no warning, correct source characters — and both were found by rendering a page
and looking at it. F-285 also shows the cheaper half: **the page you open to verify one fix is free
evidence about everything else on it.** Verifying narrowly would have missed this.
