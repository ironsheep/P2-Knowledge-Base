# Study — P2KB content trust: did the Aug/Sep change set weaken the KB?

**Task:** «#350» · **Opened / reported:** 2026-09-22 · **Status:** instruments 1 and 2 complete; instrument 3 scoped
**Absorbs:** «#349» (the flip-flop study — see §7, which answers it)

---

## THE VERDICT

**No, the August–September change set did not weaken the knowledge base. It substantially
strengthened it — with four real, localised, recoverable exceptions, all in `hardware/`.**

| Population | Classified | Result |
|---|--:|---|
| MIXED — a replacement went in | 518 hunks | **0 weakened.** 380 stronger-or-equal · 124 non-claim · 13 wrong-introduced (11 already fixed) |
| DELETE-ONLY — language + architecture | 94 hunks | **0 vanished** |
| DELETE-ONLY — `hardware/` tree | 48 hunks | **4 vanished** |
| **Total** | **660 / 660** | no sampling |

The denominator is the point. 380 replacements were checked against sources and found *stronger*,
and **not one hunk in 518 narrowed a claim, hedged it below its source, dropped a caveat, or lost
precision.** A zero with a denominator of 518 is a measurement; a zero without one is an absence of
looking.

What the change set actually was: a **de-fabrication campaign**. It removed invented example
attributions, citations to files that do not exist (`part3-pins.txt`, `part1-cog.txt`, datasheet
pages past the end of a 50-page document), an invented `RDLUTS` mnemonic, four wrong lock
encodings, an inverted LUT-sharing direction, a fabricated event taxonomy, TTL thresholds that are
not the P2's, "built-in USB-to-serial" on two boards that have none, and a 6–9 V supply figure
against a 5.5 V absolute maximum.

---

## 1. Agreed scope

**The question:** did the August and September 2026 change set *weaken* the shipped P2KB, is every
claim still locked to a golden trusted source, and where does the hardware-test periphery sit?

**Surface:** `deliverables/ai/P2/**/*.yaml` (1,131 files) · its git history 2026-08-01 → HEAD ·
`engineering/ingestion/**` as the authority · `P2-EMPIRICAL-FINDINGS.md` (60 EF entries).

**Excluded:** `engineering/knowledge-base/` (transient, not shipped) · the manuals (audited
separately 09-21 and 09-22) · `community/obex/objects/` (131 files — the object ID *is* the
citation; declared as a gate exemption, never a silent skip) · the correctness of claims that did
not change (this study measures *weakening* and *traceability*).

**Severity scale:** breaks users · wrong but contained · latent · hygiene.

---

## 2. What framed it

| | Added | Deleted | Net |
|---|--:|--:|--:|
| August 2026 | +8,262 | −4,330 | **+3,932** |
| September 2026 | +2,451 | −2,270 | **+181** |

September is near-total churn: half the content turned over for a flat net. That is precisely why
"what did we add" cannot answer the question, and why the study is built on **deletions**.

---

## 3. Instrument 2 — the golden-source lock · COMPLETE

**Tool:** `engineering/tools/validation/audit-yaml-source-lock.py` · **Baseline:**
`…/baselines/yaml-source-lock.json` · **Wired:** `validate-dod-release.py` as `validate_source_lock`
(ratchet mode) · arming meta-gate went ARMED 24 → 25.

Provenance is tiered by **how far a citation can be followed**, because presence is not
correctness — `source: enhanced` satisfies a presence check while naming no document, which is how
F-348's pin-current limit (5× the datasheet maximum) survived two purges wearing a citation.

```
audited 1000 file(s); 131 exempt by declared rule
  RESOLVABLE     88     8.8%   names a repo path that exists      -> checkable by a machine
  NAMED         458    45.8%   names a real document, no locator  -> checkable by a person
  WEAK           15     1.5%   a token naming no document         -> checkable by nobody
  ABSENT        439    43.9%   no provenance key at all           -> checkable by nobody
block-level junk citations: 31 in 31 file(s); 16 HIDDEN by the file roll-up
self-declared source conflicts: 12 in 10 file(s)
```

**45.4% of the shipped KB is locked to a source nobody can follow.** It runs as a **ratchet**: 45.4%
cannot be a blocking gate today, and a permanently-red gate is one people learn to scroll past. The
baseline records the state; the gate blocks anything worse.

⚠️ This measures **traceability, not correctness**. `locknew.yaml` states "The P2 has 16 hardware
locks (0-15) shared across all 8 COGs" with no source — true *and* unlocked. Unsourced ≠ wrong.

---

## 4. Instrument 1 — the deletion audit · COMPLETE

**Tool:** `engineering/tools/validation/audit-yaml-deletion-classes.py`

Triage: 1,220 hunks → 179 add-only · 832 mixed · 209 delete-only. 6,600 deleted lines → 4,272
substantive → 42 relocated, 205 rewritten in place → **660 read by six dispatched agents, every
finding re-verified by the arbiter.**

### Findings register

| # | Severity | Finding | Evidence | Mark |
|---|---|---|---|---|
| **D-4** | **breaks users** | `edge-standard-module.yaml` lost its revision history. Shipped now says `vin: "5 V recommended, 16 V maximum"` with **no revision qualifier**. VIN max was **5.5 V on Rev A/B**, raised to 16 V only at Rev C. A user with a Rev B module is told 16 V is acceptable — ~3× their maximum. Also lost: copper 1.5→2 oz, microSD added at Rev C, crystal→TCXO, 2→3 A, 2.5 MHz→750 kHz, 4→6 layers | `edge-standard-module-narrative.txt:519-549` vs `edge-standard-module.yaml:69,84`; tree-wide grep for `revision_history`/`1.5oz`/`5.5V to 16` returns nothing | traced |
| **D-2** | wrong but contained | `addon-rtc.yaml` lost that **VIO3V3 trickle-charges the backup battery** — the mechanism by which the RTC survives power loss. Absent from the entire KB | `P2-RTC-Add-on-text.txt:56`; `trickle\|charge` tree-wide returns only RC-capacitor text in p2an004 | traced |
| **D-1** | wrong but contained | `addon-hyperram-hyperflash.yaml` lost "the board does NOT source power via the 5V socket, so the ACC HDR jumper can remain off." The only surviving `ACC HDR` text is the *Serial Host* board, which states the **opposite** | `hyperram-hyperflash-text.txt:57` vs `addon-serial-host.yaml:78,89` | traced |
| **D-3** | latent | `addon-rtc.yaml` lost the MS421R cell capacity (1.5 mAh / 0.11 g), PCB dimensions, −20…+60 °C range, and the **UN 38.3 / Class 9 Dangerous Goods** classification — which an integrator needs and cannot derive | `complete-P2-RTC-Add-on-reference.md:56,60-61,65-67`; distinctive strings absent tree-wide | traced |
| **X-A** | wrong but contained | `smart-pin-11011-usb-host-device.yaml:76` replaced an honest *"not stated in any primary source"* gap with *"see the P2 datasheet"* for the J/K/SE0/SE1 thresholds. **The datasheet contains zero occurrences** | `grep -cE 'SE0\|line.state' p2-datasheet-text.txt` = 0 | traced |
| **X-B** | wrong but contained | `external-symbols.yaml:278` claims pnut-ts **rejects** `-D symbol=value` with a quoted error and non-zero exit. With a clean control, 1.55.5 accepts it, writes output, exits 0 | arbiter ran it; see §8 | traced |
| **S-1** | latent | 439 claim-bearing files carry no primary provenance key | instrument 2 | traced |
| **S-2** | wrong but contained | 31 junk citations; **16 hidden** by the file roll-up — F-348's exact shape | instrument 2 | traced |
| **S-5** | wrong but contained | `spin2-builtin-symbols-complete.yaml` **advertises records it no longer has**: `:2001-2003` claims `pll_multipliers: 1024 symbols (XMUL1-XMUL1024)` against zero records; `:139-140` says "exactly one XMUL record is carried here" | read the file | traced |
| **S-6** | hygiene | Four hunks deleted **cross-references** rather than facts: `smart_pin_patterns`, `smart_pins`, `pasm2/concepts/streamer_smartpin_control` no longer point at `timing_operations.yaml`. Findability regression — Sacred Rule 7 says redirect, never remove | DO-3 rows 20,22,23,28 | traced |
| **S-4** | latent | 12 self-declared source conflicts in 10 files — the instrument-3 seed | instrument 2 | traced |
| **E-1** | undetermined | `hub75_adapter.yaml`'s isp_hub75 driver block (BCM PWM, measured refresh rates, HUB75 timing minima) has **no ingestion home**. The purge commit's own message names the branch: content "correct, not actionable, and has no ingestion home cannot simply be deleted" | DO-2 row 36 | undetermined |

### The root-cause group behind D-1…D-4

**All four are in `hardware/`, and all four are collateral of one commit — the hardware-tree purge.**
The language and architecture trees produced **zero** class D across 94 delete-only hunks. That
purge was mostly *right*: it correctly removed fabricated electricals and 27 of its 48 hunks were
**delete-then-repopulate-with-citations inside the same file**. It took four real, sourced facts
with it.

**Every one is recoverable by transcription, not research** — each is confirmed verbatim in a source
already in the ingestion tree.

### A new failure mode worth naming

**D-4 is the F-348 shape reached by a different route.** Not a fabricated number: a *correct
current-revision number stripped of the revision scope that made it correct*. Deleting a revision
history silently converts a true claim into a destructive one. No existing gate looks for it.

**X-A and X-B share a second mechanism:** both replaced an *honest, correct* statement with a
*confident, wrong* one — an explicit "no primary source states this" became a pointer to a document
that does not state it; an accurate "the compiler accepts this silently" became "the compiler
REJECTS this" with an invented verbatim error string. Neither is a hedge or a narrowing, which is
exactly why class W came up empty while real damage exists. **The failure mode in this change set is
not softening — it is over-confident replacement.** Same family as the manuals' payoff-sentence
defect: a slot demanding a definite answer gets an invented one.

---

## 5. Instrument 3 — the hardware periphery · SCOPED

Stephen's framing, 2026-09-22: **capability universal, execution selective.** Proving every fact on
hardware is waste; the tests sit at the wall where documentary sources stop.

**Verified against practice:** all 60 EF findings already cluster at exactly those edges — DEBUG
display semantics that live in PNut not silicon (EF-001/026/031/048/061), multi-subsystem
interactions (EF-020 `SETQ`+`WAITSEx`, EF-015 `RDPIN` auto-restart, EF-060 `##hubsymbol` in `DAT`),
and stated-rule/unstated-edge cases (EF-010 `Y=0`, EF-050 out-of-range). Barely any confirm a
plainly-stated fact. **The model is descriptive of good practice**; what is missing is that we
arrive there opportunistically rather than by identifying edges.

**Never tested:** anything the Silicon Doc or the spreadsheet states plainly · anything `pnut-ts`
settles (legality only, never semantics) · anything already in the ledger.

| Class | The wall | Candidates found |
|---|---|---|
| **A** source silent | no trusted source addresses it | F-336 (*"neither a Parallax statement nor a bench result"*), F-202 (*"no trusted numeric source → hardware campaign required"*), F-208, **X-A** (USB J/K/SE0/SE1 thresholds — now confirmed absent from the datasheet) |
| **B** sources disagree | a contradiction documentary work cannot close | **F-337** (`%TT` in DAC_MODE: Datasheet + HW Manual vs Silicon Doc, and our YAML follows the **minority**; EF-055 already adjacent), F-372, F-385, plus the 12 self-declared conflicts |
| **C** rule stated, edge not | the boundary case | F-383 |
| **D** emergent interaction | documented apart, never together | streamer + FIFO + hubexec contention; CORDIC under interrupt |
| **E** we derived it | the instruments-1+2 residue | the 439 ABSENT files, filtered by load-bearing-ness |

**Prioritisation:** value = (wall moved) × (how much depends on that region) ÷ cost on one board with
a jumper. A Class D test can outvalue several Class C tests, because settling an interaction moves
the wall across a region rather than closing one corner.

**Start with Class B.** It is self-identifying, machine-findable once sources are indexed, and
unarguably unclosable by reading more documents. F-337 is open now and EF-055 is already adjacent.

---

## 6. Coverage, and what was not read

660/660 hunks classified, no sampling. Six agents, every finding re-verified by the arbiter.

**Not read:**
- The ~1,900 hunks the two automated cuts cleared (42 relocated, 205 rewritten). The rewritten cut
  is the one to challenge if anything was missed — see §8 for why its threshold is reported as its
  own bucket rather than trusted.
- Whether a `NAMED` citation actually *supports* the claim attached to it. Traceability ≠ correctness.
- Content that never changed and was never sourced. Instrument 2 *finds* those 439 files; finding is
  not certifying, and that is a larger body of work whose size should be measured before committing.
- MX-2 flagged four sub-items it did not verify to the LSB (SETXFRQ constants, BRK trigger bit
  positions, three donor-board base-pin inferences, some eval-board reference lines).

---

## 7. This answers «#349» — the flip-flop question

**Of 13 wrong-introduced errors found across the window, 11 were already caught and corrected by
the project's own process, inside the same window.**

- 9 sites of `rdlong clkf, #$14` (wrong clkfreq address) — introduced, then fixed by **F-445** on
  09-21. Zero occurrences remain.
- 2 citation mis-points in `dds-goertzel.yaml` and `pin-selection.yaml` — introduced and repaired by
  a later commit in the same set. Verified against the live tree.

**Only 2 of 13 are still live** (X-A, X-B). That is not a flip-flopping system; it is a system with a
working correction loop, and a detection rate near 85% inside two weeks.

**So the sensation is real but the diagnosis inverts.** What Stephen is sensing is not wasted motion —
it is the *visible churn of an effective correction machine*, compounded by two things the study can
name precisely: (a) a fix lands in one tree and the other catches up later, which *looks* like a
reversal and is actually a sweep completing (the CT-event rule was corrected in the KB and in the
Assembly manual on consecutive days, «#348»); and (b) **nothing records which way a fact was last
decided or on what authority**, so each repeat-touch reads as a fresh re-decision rather than a step.
H5 from the original framing is the answer: **the fix is visibility, not process.**

---

## 8. Seven inversions — the method note

Every one was caught by running a control, and each would have shipped a wrong finding:

1. `enhancement_source: PNUT_TS_v2.0_*` looked like **346 bogus citations**. All 356 files also carry
   a real `documentation_source` — it is a legitimate secondary key.
2. The file-level provenance roll-up **hid block-level junk** — F-348's shape, invisible to the
   headline number. Fixed; that is where "16 hidden" comes from.
3. Keyword-matching "source" is wrong for this KB: `clock_source`, `event_sources`, `ptra_source`,
   `source_select` are **domain** words. A curated allow-list moved 19 files out of `ABSENT`.
4. The one-way containment test **auto-cleared the `#$14` clkfreq regression** — same vocabulary,
   changed meaning. Made bidirectional; the safer test produced *more* reading (453 → 660), which is
   the correct direction when a bucket decides what nobody looks at.
5. An agent's only class D (deleted `XDIV1`/`XMUL2` symbol records) **inverted**: those appear zero
   times in Spin2 v55, our current source, and only in the stale v51 extraction. But a real finding
   was underneath it — S-5.
6. My own pnut-ts test for those symbols was **invalid**: `_CLKFREQ` and `_XTLFREQ` fail it too, and
   they are known-real. They are symbols you *declare*, not read.
7. My first `-D` fixture **errored on its own source**, proving nothing either way. With a clean
   control the finding stood.

Also corrected mid-study: I attributed the deletion volume to the hygiene sweeps. Those touched many
*files* but **62 lines of 6,600**.

---

## 9. Hand-off — what this seeds

**For `sprint-plan`, as candidate sections:**

1. **Restore the four class-D facts** (D-1…D-4). Transcription from sources already held. D-4 first
   — it is the only *breaks-users* row in the study.
2. **Correct X-A and X-B**, pending Stephen's pnut-ts check on X-B.
3. **Fix S-5** — the summary block advertising 1024 records that do not exist.
4. **Restore the four cross-references** (S-6), per Sacred Rule 7: redirect, never remove.
5. **Shrink the instrument-2 backlog.** The ratchet stops it growing; the 439 + 31 are the work.
6. **Build the Class B periphery queue**, starting at F-337.

**Trivially safe — one green-light decision:** S-6 (four cross-reference redirects) and S-5 (two
stale summary lines). No behaviour change beyond the defect, no consumer to enumerate, and the gates
would show it.

**Two questions for Stephen:**
- **Does your pnut-ts reject `-D VERS=200`?** This container's 1.55.5 (build 2026-08-30) accepts it.
  If yours rejects, X-B collapses and only the "older builds" framing is wrong.
- **Does ISP driver documentation belong in `deliverables/ai/P2/hardware/`** or in the OBEX/community
  tree? E-1 needs a policy call, not more grepping.

**A new gate worth building, from D-4:** nothing checks that a revision-scoped figure keeps its
scope. A shipped absolute maximum stated without the board revision it applies to is a
hardware-damage defect no existing instrument looks for.
