# Study — P2KB content trust: did the Aug/Sep change set weaken the KB?

**Task:** «#350» · **Opened:** 2026-09-22 · **Status:** in progress (instrument 2 complete)
**Absorbs:** «#349» (the flip-flop study — instrument 1 produces its answer as a by-product)

---

## 1. Agreed scope

**The question, in one sentence:** did the August and September 2026 change set *weaken*
the shipped P2KB, is every claim still locked to a golden trusted source, and where does
the hardware-test periphery sit around what documentary sources can settle?

**Surface**

- `deliverables/ai/P2/**/*.yaml` — the shipped set, 1,131 files
- Its git history from 2026-08-01 to HEAD — 6,600 deleted lines, ~1,600 of them prose
- `engineering/ingestion/**` as the authority the shipped set must trace to
- `P2-EMPIRICAL-FINDINGS.md` — 60 EF entries — as the record of what hardware has settled

**Excluded, each with its reason**

| Excluded | Reason |
|---|---|
| `engineering/knowledge-base/` | transient tree, not shipped |
| The manuals | audited separately and recently (Streamer 09-21, Assembly 09-22) |
| `community/obex/objects/` (131 files) | the OBEX object ID *is* the citation and the object is the artifact; declared as an exemption in the gate, never a silent skip |
| Correctness of claims that did not change | this study measures *weakening* and *traceability*; a claim that has been wrong since January and untouched is out of scope for instrument 1 and is only *found*, not certified, by instrument 2 |

**Severity scale:** breaks users · wrong but contained · latent · hygiene.

**What done means:** instrument 2 over the whole shipped set (complete); instrument 1 over
every deleted hunk since 2026-08-01 with a stated coverage; instrument 3 as a ranked
periphery map. No fixes — the study reports.

---

## 2. Read order

1. ✅ **Instrument 2 — golden-source lock.** Whole set. Cheapest, scriptable, and it
   produces the map that tells instrument 1 which deleted hunks matter.
2. ⬜ **Instrument 1 — deletion audit.** Per-hunk, 2026-08-01 → HEAD.
3. ⬜ **Instrument 3 — hardware periphery map.** Seeded by the residue of 1 and 2.

Order is deliberate: reading ~1,600 hunks without knowing which files are already
unsourced is reading blind.

---

## 3. The measurements that framed the study

| | Added | Deleted | Net |
|---|--:|--:|--:|
| August 2026 | +8,262 | −4,330 | **+3,932** |
| September 2026 | +2,451 | −2,270 | **+181** |

September is near-total churn: half the content turned over for a flat net. That flat net
is the reason "what did we add" cannot answer the question, and it is where a weakening
would be invisible.

Only 2 files were deleted outright and 4 added — this is all in-place editing.

⚠️ **A correction carried from the framing pass.** An earlier read of mine attributed the
deletion volume to the hygiene sweeps (`educational_value`, `production_readiness`, quality
scores). That was wrong: those touched many *files* but only **62 lines of 6,600**. The
deletions are overwhelmingly prose, and a line-level grep **cannot** distinguish *replaced*
from *vanished*. That distinction requires per-hunk reading, which is why instrument 1 is
expensive and cannot be shortcut.

---

## 4. Instrument 2 — golden-source lock · COMPLETE

**Tool:** `engineering/tools/validation/audit-yaml-source-lock.py`
**Baseline:** `engineering/tools/validation/baselines/yaml-source-lock.json`
**Wired into:** `validate-dod-release.py` as `validate_source_lock` (ratchet mode)

### The model

Provenance is tiered by **how far the citation can be followed**, because presence is not
correctness — `source: enhanced` satisfies a presence check while naming no document, and
that is how F-348's pin-current limit (5× the datasheet's absolute maximum) survived two
purges wearing a citation.

| Tier | Meaning | Checkable by |
|---|---|---|
| `RESOLVABLE` | names a repo path that exists | a machine |
| `NAMED` | names a real document, no locator | a human holding it |
| `WEAK` | a token naming no document | nobody |
| `ABSENT` | no provenance key at all | nobody |

### Result — whole shipped set

```
audited 1000 file(s); 131 exempt by declared rule

  RESOLVABLE     88     8.8%
  NAMED         458    45.8%
  WEAK           15     1.5%
  ABSENT        439    43.9%

block-level junk citations: 31 in 31 file(s)
  of which HIDDEN by the file roll-up: 16
self-declared source conflicts: 12 in 10 file(s)
```

**The headline: 8.8% of the shipped KB carries provenance a machine can follow.**
45.8% names a document but gives no locator — followable by a person who has the document
open. **45.4% (`WEAK` + `ABSENT`) is followable by no one.**

### Findings register — instrument 2

| # | Severity | Finding | Evidence | Mark |
|---|---|---|---|---|
| S-1 | latent | 439 claim-bearing shipped files carry no primary provenance key at all | `audit-yaml-source-lock.py --tier ABSENT --list` | traced |
| S-2 | wrong but contained | 31 blocks cite a token that names no document (`enhanced`, `original`); **16 are hidden** because the file scores better on a different citation — this is F-348's exact shape | gate output, block-level section | traced |
| S-3 | latent | Only 88 of 1,000 citations resolve to a path. The good form (`name -- engineering/…path[:line]`) exists and is used 74 times — it is established practice, not a new convention to invent | gate output | traced |
| S-4 | latent | 12 self-declared source conflicts in 10 files — the KB already records where its sources disagree | `architecture/clock_system.yaml` `[cross_source_conflict]`, `architecture/streamer/dds-goertzel.yaml` `[source_tension]`, `architecture/streamer/pin-capture.yaml` `[known_source_defect_in_that_passage]`, `architecture/io_pin_timing.yaml` `[not_stated_by_any_source]`, `architecture/boot-rom/*`, 4 app-note companions | traced |

**S-4 is the instrument-3 seed.** These are Class B periphery by the KB's own admission: a
contradiction between trusted sources cannot be closed by reading more of them.

### Two candidate findings REJECTED after checking

Recorded so nobody re-raises them:

- **`enhancement_source: PNUT_TS_v2.0_*` — 356 files.** Not a junk citation: all 356 also
  carry a real `documentation_source:`. It is a legitimate secondary key naming the tooling
  pass that enriched the entry. Scoring it weak would have produced **346 false findings**.
- **`source: parallax-quick-bytes` — 42 files.** The corpus does exist under
  `engineering/ingestion/sources/quick-bytes-*`. Thin (only partly processed), but real.

### Two defects found in the instrument itself, by its own controls

Recorded because the method is the deliverable:

1. **File-level roll-up hid block-level junk.** A file scoring `RESOLVABLE` on one citation
   masked a *different* block inside it carrying `enhanced` — precisely F-348's shape. Fixed
   by reporting block-level junk independently of the file tier; that is where the "16
   hidden" number comes from.
2. **Keyword matching on "source" was wrong for this KB.** `clock_source`, `event_sources`,
   `interrupt_sources`, `ptra_source`, `source_bit`, `source_select` are *domain* words here.
   A pattern match scores every one as a citation. Replaced with a curated allow-list built
   from an enumeration of every provenance-shaped key in the shipped set; that correction
   alone moved 19 files out of `ABSENT`.

### Verification of the instrument — both limbs

A gate shown only healthy input has not been verified.

| Limb | Expected | Result |
|---|---|---|
| True baseline | PASS | PASS, exit 0 |
| A file recorded better than it now is | FAIL | `WEAKENED: … RESOLVABLE -> NAMED`, exit 1 |
| A file absent from the baseline and unsourced | FAIL | `NEW unsourced file: … [ABSENT]`, exit 1 |
| Known-junk file (`event_interrupt_config.yaml`) | `WEAK` | `WEAK` |
| Known-unsourced file (`sqrt.yaml`) | `ABSENT` | `ABSENT` |
| Known-named file (`addct1.yaml`) | `NAMED` | `NAMED` |
| Arming meta-gate | script must become ARMED | ARMED 24 → 25, UNASSIGNED 4 → 3 |

### Why a ratchet and not an absolute gate

45.4% unsourced cannot be a blocking release gate today — a gate that is permanently red is
a gate people learn to scroll past. It runs as a **regression ratchet**: the standing backlog
is the study's job to shrink, and the gate's job is to stop it growing. `--write-baseline`
records the state; `--baseline` blocks anything worse.

---

## 5. Not yet read

- Every deleted hunk since 2026-08-01 (instrument 1) — ~1,600 prose lines
- The periphery map and its Class B contradiction scan (instrument 3)
- Whether any `NAMED` citation actually *supports* the claim it is attached to. This study
  measures **traceability**, not correctness. `locknew.yaml` states "The P2 has 16 hardware
  locks (0-15) shared across all 8 COGs" with no source — the claim is *true* and *unlocked*.
  Unsourced does not mean wrong, and the register must not be read as though it did.

## 6. Open questions

- Is the 45.4% unsourced population a **backlog** (old entries predating the citing
  convention) or a **live practice problem** (new entries still shipping unsourced)? The
  baseline plus instrument 1 answers this, and the answer changes whether the fix is a
  one-time sweep or a process change.
- Do the `NAMED` citations with three different spellings of the same document
  (`PASM2 Manual 2022/11/01 Pages 31-147` / `2022-11-01` / `2022/11/01`) want normalising to
  the resolvable form? Scope call, not a defect.
