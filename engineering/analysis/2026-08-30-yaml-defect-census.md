# YAML defect census — measured depth, 2026-08-30

**Why this exists.** Every repair in the 2026-08-29 pass revealed more work, and the depth was being
discovered by tripping over it. This document replaces that with measurement: every open class
enumerated corpus-wide, every gate's blind spot simulated and counted, **read-only, no edits**.
The question it answers is *"how deep is this, and what actually has to be in this release."*

**Measured at** `79fbbe1e`, tree clean. Every number below is reproducible by the commands in the
appendix. **The tree was restored and verified clean after the simulation** (`git status` empty).

**What this is not.** A snapshot against *known* instruments and *registered* findings. It cannot
prove completeness — a genuinely new defect class will still appear later. That is the nature of a
corpus whose true defect population is unknown, and it is the reason "release when clean" is not an
achievable target. "Release when the severity bar is met and everything else is counted" is.

---

## The triage rule this census sorts against

> **Does this make an agent emit wrong code, or damage hardware?**
>
> **Yes → category 1.** Ships in this release. No exceptions.
> **No → category 2.** Registered, counted, scheduled. Does not hold the release.

This does not weaken *no deferring*. Fix-now applies to **the blast radius of what you touched** —
knowing something is wrong, having your hands on it, and walking away stays forbidden. Survey-and-
schedule applies to **classes measured but not entered**. A counted, triaged, registered finding was
never deferred; it was scoped.

---

## Headline: the release scope is much smaller than the backlog

| | count | category |
|---|---|---|
| **Citations that must be read to rule out a wrong value** | **409** | **1 — the only place a wrong value can still hide** |
| **Uncited electrical figures in 2 hardware files** | **19 quantities** | **1 — the shape that produced the 150 mA defect** |
| Citation locators mechanically broken | 15 | 2 |
| Tier-2 unmasking (F-381) | 32 blocks / 24 files | 2 (except the hardware ones, above) |
| Cross-references that resolve to nothing | 91 + 35 paths | 2 |
| Quality-judgement sites (F-374) | 9 / 40 / 60 — **class undefined** | 2 |
| Gate wiring gaps | 3 | 2 |
| Delivery strips citations (F-375) | 397 values / 396 files | 2 |

**Everything in category 2 is bounded and counted. Only category 1 gates the release.**

---

## 1. Citation locators — 424 measured, 51 source files

| finding | count | |
|---|---|---|
| line is **out of range** | **0** | the range check is already clean, which is why F-377 says no tool can see this |
| **file does not exist anywhere** | **2** | `edge-standard-module.yaml:53` and `edge-32mb-module.yaml:57`, both citing a bare `narrative.txt` |
| **ambiguous — basename exists in 2+ places** | **1** | `pin-drive-configuration.yaml:162` cites `complete-tables-reference.md:326`; that name exists under **both** `p2-datasheet/` and `p2-hardware-manual/`. F-367 established two same-named documents can differ, so this is not cosmetic |
| **lands on a BLANK line** | **12** | mechanically detectable slice of the F-377 class |
| **lands on a real, non-blank line** | **409** | ✅ resolvable — ❗ says nothing about whether the line *supports the claim* |

**85 of the citations use a short form** (bare `silicon-doc-text.txt:3790` rather than the full
path). All 85 resolve uniquely against the ingestion tree and land on non-blank lines, so they are
**not** broken — but they resolve *by convention*, not by construction. A second file of the same
basename turns any of them into the ambiguous case above.

### The 409 are the whole of the remaining category-1 risk

F-377's finding is that a locator can be **in range, non-blank, and still point at the wrong line** —
and if a KB claim was derived from the wrong line, *the claim itself may be wrong*. No instrument in
this project can detect that; it requires opening the line and reading it. The 2026-08-29 pass found
exactly this shape three times.

**So: 409 citations is the measured size of the last place a wrong value can hide.** That is a
bounded, countable job with a definite end — not an open-ended audit.

---

## 2. F-381 — the Tier-2 blind spot is **exactly 32 blocks**, not a floor

**Simulated**: for each of the 24 wholly-uncited files, insert one citation the gate recognises, run
the gate, count the blocks that become blocking. Tree restored after each.

**Result: 32 — identical to the advisory count.**

> ⚠️ **This corrects a claim made on 2026-08-29** (in the ledger §0.5 item 12b, in F-381, and in
> conversation): that "32 is only what the gate can name" and the true figure was larger. **It is
> not.** The advisory count is an accurate census of the blocks. The three-file sample that yielded
> 12 was consistent with it all along — those files held 16 advisory blocks, 12 surfaced as blocking
> and 4 were covered by the citations added. The blind spot is real; its *size* was not underreported.

| area | files | blocks | disposition |
|---|---|---|---|
| `architecture/smart-pins/` | 8 | 9 | ordinary citation debt |
| `language/` clock + timing | 6 | 7 | ordinary citation debt |
| `architecture/decomposition/` | 5 | 8 | reasoning layer — *needs a policy, not a citation* |
| `hardware/` | 2 | **5** | **category 1 — see §3** |
| `community/obex/objects/` | 3 | 3 | community metadata — *may have no Parallax citation to give* |

Worst single file: `hardware/hardware-compatibility-matrix.yaml`, **4 blocks**.

---

## 3. The two hardware files — the only category-1 item besides the 409

`hardware-compatibility-matrix.yaml` carries **14 uncited quantities** in V and mA across 4 blocks;
`p2-hardware-selection-guide.yaml` carries **5** in A, V and mA. Samples, verbatim:

```
"64006A (Control) - ~16mA max (4 LEDs)"
"64006C (LED Matrix) - 4mA (Charlieplexed)"
"64006B (Serial Host) - 500mA per USB port + 5V required"
"64006H (A/V Breakout) - 80mW audio amplifier + video drivers"
```

None has been checked against a source. **They are not known to be wrong.** They are category 1
because of their *shape*: this KB's worst shipped defect was `max_current_per_pin: 150mA` in
`basic-io.yaml` — five times the datasheet's ±30 mA absolute maximum, in the exact number used to
size a series resistor — and it survived two purges because nothing cited it and nothing could block
on it. **Uncited electrical figures sitting where the blocking gate structurally cannot reach them
is that setup, reproduced.**

19 quantities is a morning's work to source or remove. It should not wait behind 8 smart-pin pages.

---

## 4. Cross-references — 2,304 bare-name entries

| class | count | verdict |
|---|---|---|
| resolves | 1,500 | ✅ |
| **prose, not a key** | **649** | ✅ by design — `see_also` is free text in the decomposition layer |
| **family/wildcard form** | **64** | ⚠️ `POLLCTx`, `WAITCTx`, `JCTx`, `JNCTx` — the numbered siblings exist, the wildcard does not. Conceptually fine, literally unresolvable by an agent |
| **genuinely absent** | **91** | see split below |

The 91 split three ways, and only the third is a defect in the ordinary sense:

- **37 are document names in `references:`** — `silicon_doc` ×15, `instruction_set` ×8,
  `optimization_guide` ×7, plus `architecture_guide`, `timing_doc`, `assembler_manual`. These name
  *documents*, not KB entries, in a field that also holds KB keys. **The field is doing two jobs**;
  that is the finding, not the values.
- **12 are real P2 constants the KB does not document** — `COGEXEC_NEW`, `COGEXEC_NEW_PAIR`,
  `HUBEXEC_NEW`, `X_DACS_OFF`, `EVENT_INT`, `XDIV1`. **All six verified present in Spin2 v51/v55
  sources**, so these are *coverage gaps*, not fabricated names. (Checked specifically because a
  fabricated constant name would have been category 1. None is.)
- **42 concept names that exist nowhere** — `spi_communication`, `i2c_communication`,
  `circular_buffers`, `hub_memory`, `events`, `round_robin_scheduling`. Ordinary dead links.

Separately, **35 broken `see_also` *path* values** (18 carrying a `deliverables/ai/P2/` prefix,
12 pointing at a real file from the wrong base, 3 globs, 2 naming manifests that exist nowhere).

---

## 5. F-374 — the class has no agreed boundary

Three defensible readings, three different sizes:

| definition | sites | files |
|---|---|---|
| narrow — `educational_value` / bare `value:` with a judgement word | **9** | 9 |
| the ledger's recorded figure | **40** | 18 |
| broad — any judgement-valued key incl. `complexity` (39 of them) and `confidence` | **60** | 34 |

**This is not a measurement disagreement, it is an undefined class.** `complexity: medium` is 39 of
the 60; whether it is excluded judgement or useful navigation is a decision nobody has made. Making
that decision costs minutes and turns a vague finding into a countable one.

---

## 6. Instrument gaps, all three confirmed at HEAD

| gap | status |
|---|---|
| `audit-yaml-duplicate-keys.py` armed, clean across 1132 files, **not called by `validate-dod-release.py`** | confirmed — that script calls only `audit-constant-fidelity`, `audit-yaml-claim-sourcing`, `validate-crossref-keys` |
| `validate_metadata_filter` reads the **pattern list**, never re-parses the filtered payload | confirmed (F-375 half) |
| `fetch-kb-file.sh -v <KEY>` exits 0 fetching nothing; index generator's alias harvest ends in `except Exception: pass` | confirmed (F-376) |

Delivery strip, re-measured: **397 `documentation_source` values across 396 files**, of which roughly
362 are real provenance. All removed at delivery by `fetch-kb-file.sh:189`.

---

## 7. How many passes — the answer

**Category 1, this release:** the 409-citation read, and 19 hardware quantities. Bounded, and the
only work where a wrong value can still be hiding.

**Category 2, scheduled by area** — each a closed set with a definition of done that cannot grow,
because growth found inside it was already counted here and growth found outside goes to the register:

| phase | contents | size |
|---|---|---|
| A | 15 broken locators + 35 broken `see_also` paths + 43 dead concept names | 93 sites |
| B | F-381 ordinary debt: 14 files (smart-pins + clock/timing) | 16 blocks |
| C | the three gate repairs + the F-375 delivery decision | 3 + 1 scope call |
| D | **policy first, then work**: decomposition layer, OBEX metadata, `references:` doing two jobs, F-374's boundary | 4 decisions |

Phase D is decisions, not repairs. Everything in it is currently miscounted *because* the policy is
missing — which is why it is last and why estimating it before deciding would be guesswork.

---

## Appendix — reproducing every number

```bash
# §1 citation locators: extract every <path>:<line> from the shipped YAML, resolve short forms
#     against engineering/ingestion/**, then classify missing / out-of-range / blank / ok.
# §2 F-381 simulation: for each wholly-uncited file, append a recognised `source:` key,
#     run audit-yaml-claim-sourcing.py, count UNCITED_IN_CITING_FILE rows for that file, restore.
python3 engineering/tools/validation/audit-yaml-claim-sourcing.py --advisory   # the 32 / 24
# §4 cross-references: walk every related_symbols/see_also/references/related_concepts/related
#     entry; resolve against p2kb-index.json keys+aliases and every file stem+aliases;
#     split identifier-shaped from prose, then family-form from genuinely absent.
# §5 F-374: three greps, three class definitions — the point is that they disagree.
# §6 grep -n 'duplicate' engineering/tools/validate-dod-release.py   # returns nothing
```

**Tree state:** clean at `79fbbe1e`. Nothing in this pass edited a file; the simulation restored
each file it touched and `git status` was verified empty afterwards.
