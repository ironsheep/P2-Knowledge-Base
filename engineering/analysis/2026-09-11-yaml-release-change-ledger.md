# YAML release change ledger — `v1.18.1..HEAD`

**Purpose.** Everything that differs in `deliverables/ai/P2/**/*.yaml` between the last release and
HEAD, with the reason it changed and **what was absent that let the defect exist**. Written for a
release review; the question it answers is *"is it safe to ship, and what did we lose that I cannot
see from a diffstat?"*

**This document shows CURRENT differences only.** An item that has been fixed is **gone from here**,
not annotated as fixed. For the history of what was once outstanding, read the archived predecessor
and the git log — not this file.

**Range.** `v1.18.1` (`57ef2e0d`, 2026-09-10) `..` `617c69d9` (2026-09-11).
**Measured on disk 2026-09-11** — every count below derived from git and from the parsed YAML at
HEAD, not carried forward.

**Supersedes** `engineering/analysis/2026-08-27-yaml-release-change-ledger.md`, archived to
`engineering/analysis/archived/2026-08-27-yaml-release-change-ledger.md`, **byte-identical to its
last committed revision** before this supersession (`git show 5cb9467e^:… | cmp -` returns clean).
*The path is `archived/`, not `archive/`: `.gitignore` carries a bare `archive/` rule that would
swallow the directory.*

> ⚠ **Why the predecessor was archived, and it is a defect worth naming.** That ledger declared its
> range as `v1.17.0..b0057ec1` (2026-09-08). `b0057ec1` **is an ancestor of `v1.18.1`** — its entire
> range shipped on 2026-09-10 as v1.18.0 and v1.18.1. It was therefore **spent**, and on 2026-09-11
> this session appended a new section (§1.26) to it and pointed Stephen at it as the live release
> gate. Both were wrong: a spent ledger cannot gate an unshipped release, and content for a new
> range does not belong in a document describing a released one. Stephen caught it — *"the ledger
> you are pointing me to should be post v1.18.0."* The append was reverted, the predecessor restored
> byte-identical and archived, and its content re-derived here against the correct range.
> **The general shape: a release ledger has an expiry — the moment its range ships — and nothing in
> the process was checking that.**

---

## §0.1 — The range, measured

| | |
|---|---:|
| commits in range (all) | **40** |
| commits touching `deliverables/ai/P2` | **3** |
| YAML files changed | **20** |
| line delta | **+8 / −66** |

The three KB-YAML commits:

| commit | what |
|---|---|
| `e80be72c` | block F — F-374: 40 unsourced quality-judgement sites removed, 18 files |
| `2ef758db` | block G — one uncited derivation dropped; one self-contradicting companion made consistent; F-426 fixed |
| `617c69d9` | F-425 — the same class under three further key names |

**This release is almost entirely SUBTRACTION.** +8 / −66 across 20 files: 66 lines removed, 8
added, and of those 8, four are rewrites of prose lines and two are relabelled section banners.
Nothing new is asserted. That is the correct shape for a release whose subject is *unsourced content
leaving the KB*, and it is the first thing to check against the diffstat.

---

## §0.2 — Where a record disagrees with the artifact

Two counts in the register moved between filing and fixing. Both are recorded rather than
smoothed over, because the drift is the point:

| record | said | measured 2026-09-11 |
|---|---|---|
| F-374 | 40 sites / 18 files | **42 sites / 19 files** at re-derivation (`educational_value` had grown 7 → 9); **40 deleted**, 2 correctly left as legitimate |
| F-375 | 397 `documentation_source` values / 396 files | **396 / 395** |
| F-425 | two prose lines | **four** — and the `production_readiness` sites sat under a `# QUALITY RATINGS` banner the finding never noticed |

A finding written from a grep is a **map, not an inventory**. Every count in this ledger was
re-derived at HEAD for that reason.

---

## §1.1 — F-374: 40 quality-judgement sites removed (`e80be72c`)

**The rule.** A P2KB entry states **existence, access and utility** — what a thing is, how to reach
it, what it is useful for. It does not grade. Two independent reasons, either sufficient: nothing
sources a star rating, and a remote agent generating code cannot act on one.

| key shape | sites removed |
|---|---:|
| `rating` | 12 |
| `educational_value` | 8 |
| `educational: value:` (nested) | 8 |
| `recommendation_score` | 6 |
| `quality_rating` | 6 |
| **total** | **40** |

Plus the orphaned `minimum_educational_value` threshold and the 4 schema sub-keys belonging to the
schema field it gated (`code-example-schema.yaml`).

**100% deletion, 0% replacement — and that is the finding, not a shortcut.** For every site, the
concrete fact the score gestured at was *already stated elsewhere in the same file*. The grade was
never carrying information; it was sitting next to the information.

**Two survivors, each read rather than counted:**
- `addon-motor-driver.yaml:155` — `rating: "VIN and output-channel spring terminal blocks rated 32 A / 400 V"`. An electrical spec the bare-key grep catches by accident.
- `edge-breadboard-carrier.yaml:225` — `educational_value:` heads a block of `learning_objectives`. The key *name* resembles the class; the content does not.

---

## §1.2 — F-425: the same class under three further key names (`617c69d9`)

Filed during block F and **fixed the same day**, after Stephen's correction: *"If we find problems,
we're supposed to get them out to the agents as soon as possible. If you file it, we're not doing
that."* `p2kb-mcp` serves the **published** tree, so a filed-but-unfixed defect reaches nobody.

| site | disposition |
|---|---|
| `hardware-compatibility-matrix.yaml` — `cost_efficiency` ×6 | **deleted.** Every row already states `module_free_pins`, `carrier_header_pins` and `use_case`. `"expensive_overkill"` is an opinion about someone else's product. |
| `edge-standard-module.yaml`, `edge-32mb-module.yaml` — `production_readiness: "excellent"` ×2 | **deleted**, with the literal `# QUALITY RATINGS` banner heading them. `memory_class: "high_capacity"` kept (a fact); its banner relabelled `CLASSIFICATION`. |
| `p2-eval-board.yaml` — `target_audience` ×4 | **adjective stripped, fact kept.** *"Ideal - no hardware selection needed"* → *"No hardware selection needed -- board, USB and power are one part."* |

**Deliberately kept:** four `production_readiness` values reading `"prototype_platform"` or
`"not_applicable"`. Those state what a board is **for** — utility, which the rule permits. Only
`"excellent"` was a grade.

---

## §1.3 — Block G: the app-note companions (`2ef758db`)

**One derivation dropped.** `p2an001`'s `raw_sample_rate_sps: 1_562_500  # 200_000_000 / 128` was
arithmetic with a comment where a citation belongs. The ingestion tree was grepped in three
spellings and **no Parallax source states that figure**. P2AN003 had already deleted the identical
construction, so the region was applying two opposite rules to one shape — which was the actual
defect, not the value.

**One file stopped contradicting itself.** `p2an004` said in three places whether it restates the
sensor's datasheet figures. Supply-range and dark-output figures removed (genuinely restated, no
algorithmic use here); the **calibration point kept**, because the note's own
`Ee = freq * 430 / 250_000` formula and its `CAL_UW`/`CAL_HZ` constants scale from it — deleting it
would have stranded the formula and recreated the item-2 defect one line away. Datasheet named by
number inline, matching the citation already present.

---

## §1.4 — F-426: a wrong maximum, found one line from the line being fixed

`p2an004`'s `measurement_ceiling` read *"runs at a legal 200 MHz (300 MHz max)"*. F-413 had already
ruled that exact claim — *"300 MHz appears in no source we hold and in no KB file. The datasheet
maximum is 320 MHz"* — but F-413 was scoped to P2AN001 and **never looked at this companion**, so
the number survived one file over. Fixed in the same pass.

⭐ **The trap, and the reason a string sweep would have made this worse.** `300 MHz` **is** genuinely
sourced, three times, and never as a maximum:

| site | says | verdict |
|---|---|---|
| four board files | Parallax's own feature list, *"Overclocking possible beyond 300 MHz"* | **correct — keep** |
| `special-configuration-symbols.yaml:97` | the datasheet rates direct XI drive to 200 MHz max; *"The compiler accepts 300 MHz beyond that"* | **correct — keep** |
| `timing_operations.yaml`, `spin2-getting-started.yaml` | 300 MHz as an example `clock_freq` | **correct — a usable value** |
| `p2an004:90` | 300 MHz as **the maximum** | **the defect** |

The defect was never the number. It was the **role** the number was given — an overclocking
threshold and a compiler ceiling promoted to a silicon specification.

---

## §1.5 — What the delivery strips (F-375, gate half resolved)

F-375's structural complaint was *every gate reads the tree, the consumer reads the stream, and
nothing compares them.* The gate half is now fixed (`75911edb`): `validate-dod-release.py`'s
`validate_metadata_filter` used to classify which lines the filter REMOVED and never re-parse what
it DELIVERED, so a mapping key whose only children were filtered fields arrived as `null` and
passed clean. It now parses the delivered payload and fails on any key that collapsed to `None` —
proven with a negative control built independently of the fix.

**The numbers, re-derived 2026-09-11.** `fetch-kb-file.sh` strips five fields from every delivered
file:

| field stripped | values | files |
|---|---:|---:|
| `documentation_level` | 408 | 408 |
| `documentation_source` | **396** | 395 |
| `last_updated` | 389 | 389 |
| `enhancement_source` | 356 | 356 |
| `manual_extraction_date` | 147 | 147 |

**The `documentation_source` split is the decision:**

| | count | share |
|---|---:|---:|
| real provenance | **363** | **91%** |
| bookkeeping tokens | 33 | 9% |

Bookkeeping is only `enhanced` (16), `original` (15), `code_analysis` (1), `redirect_stub` (1).
Everything else is a genuine citation — *PASM2 Manual 2022/11/01 Pages 31-147* (145), *PASM2 Manual
2022-11-01* (116), *PASM2 Manual 2022/11/01* (60), *PNut v55 (DebugDisplayUnit.pas)* (9),
*p2_datasheet* (8), *Silicon Doc v35* (4), *P2 Instructions v35 CSV* (2), plus per-page cites.

**So the set satisfies cite-or-omit ON DISK and is delivered NOT satisfying it.** 363 real citations
are stripped at delivery; nine tenths of what the filter removes is the provenance the project's own
rule requires. A remote agent fetching a key receives content with no statement of where it came
from, while every gate we run reads the tree, where the citation is still present.

---

## §0.5 — What is Stephen's, and still open

- **F-375's other half — the 383-file rename.** A scope call, not research. Unchanged by this range.
- **The release itself** — commit, tag, push. Nothing here is tagged or pushed.

## §0.6 — Gate state at HEAD

```
verify-yaml-format.py      1133/1133 parsed clean
validate-crossref-keys.py  100% top-level resolution
validate-dod-release.py    12/12 PASS — "READY FOR RELEASE"
```

`validate-dod-release.py` gained a twelfth check in this range (`75911edb`): the duplicate-key
audit, which had been armed and returning 0 across 1132 files while **nothing ran it**.
