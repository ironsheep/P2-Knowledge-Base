# P2KB-CORRECTION-FINDINGS archive — 2026-10-10, close-out sprint («#423»)

Five findings closed by the close-out sprint with **nothing left to validate or ship**, swept out of the live
register in the same pass that closed them: **F-218** (the KB was already correct; the defect is in an
upstream document), **F-336** (closed with no content by Stephen's Q6 ruling), and **F-364, F-405, F-441**
(the gates they named as owed are built and their negative controls have run — they ship no KB content).
Every other close-out finding that the sprint applied stays in `../P2KB-CORRECTION-FINDINGS.md` as
`PENDING-VALIDATION` until the release serves it. Entries below are moved verbatim; the only addition is the
closing note at the head of each.

---

## XBYTE technique-mining sweep — reference implementations expose two doc defects (2026-07-14) — F-217, F-218

> **Origin.** Stephen asked for a per-processor "what will hurt when you emulate this" table in the XBYTE
> Guide, and proposed we ground it by studying **live, working emulators** rather than reasoning from ISA
> facts. The study immediately surfaced two defects. Full evidence ledger:
> `engineering/document-production/manuals/p2-xbyte-programming-guide/TECHNIQUE-MINING.md`
> (per-source, because the techniques enter the manual body *anonymously* — the ledger is the only place
> the lineage lives). **Note the path:** it lives at the manual **root**, not in `audit/`, because
> `.gitignore:175` ignores `manuals/*/audit/` — a durable source-of-record cannot live there.

> **Swept closed 2026-10-10 («#423»): no KB work is owed.** The KB was verified correct 2026-08-25
> («#300»), the defect is in a pnut-ts-side document that is not a registered ingested source, and no
> published manual carries the wrong gloss. The upstream residue (which host-side test draws the checkmark)
> is routed, not ours.

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

---

## Six defects surfaced while building the single constant-definition home (2026-08-25, «#295» phase 2) — F-336…F-341

> **Closed 2026-10-10 («#423») with no content — F-336 only; F-337 and F-341 stay live in the register.**
> Stephen's Q6 (close-out study, 2026-10-09): the `P_HIGH_15K | P_LOW_FLOAT` "Weak Pull-Up" line exists only
> in our own catalog extract (`smart-pins-catalog/ingestionSources/basic-io/spin2-v51-extract.md:284-287`),
> no Parallax document. "Drop it": `architecture/pin-drive-configuration.yaml` no longer carries
> `not_documented_here.high_side_weak_with_low_side_floated` or its register self-cite, no bench run is owed
> and the ladder sweep is not owed. The manual sites that still teach the composition are F-356's.

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

---

## Two release-path defects, one root cause — F-440, F-441

> **Closed 2026-10-10 («#423»), RESOLVED — the gate this entry named as owed is built and its validation
> has run.** `engineering/tools/validation/audit-index-integrity.py` (sha256 limb: every index entry's
> `sha256` equals the SHA-256 of `git show HEAD:<path>`; also no HEAD-tracked YAML missing from the index) is
> a blocking check in `validate-dod-release.py` ("Index Integrity vs Committed Blobs (F-441/F-405)"), with a
> negative control that plants stale, flipped, absent and unindexed entries. Run 2026-10-10: 1,136 entries,
> stale 0, absent at HEAD 0, tracked YAML with no entry 0. Built in «#410» (commit e2addad0).

### F-441 — v1.19.1 published an index the integrity check could not verify — `PARTIAL — v1.19.2, 2026-09-19; published state re-verified against raw.githubusercontent.com; the owed index-sha256-vs-committed-blob gate is not built (re-verified 2026-10-05 «#386»)`

v1.19.1's index carried the **pre-change** SHA-256 for the two files that release edited, so the
MCP refused to serve them: *"Content for 'p2kbPasm2Xinit' is temporarily unavailable — verification
failed."* The release was live and broken for `p2kbPasm2Xinit` and `p2kbArchOverview`.

**Cause: step ordering.** `release-yamls` §6b regenerates derived artifacts **against the committed
state**, and it is a separate step for exactly this reason — the generator hashes the **git blob**,
so an index built while the edits are still uncommitted records the OLD hashes. This pass collapsed
6a/6b and regenerated before committing content. The gates could not catch it: `validate-dod-release`
checks index/gzip parity and structure, not whether each entry's sha256 matches its committed blob.

**Same root cause as F-440**, one release apart: both are *reading from what I had done rather than
from what was committed* — once into a release note, once into a derived artifact. The first was
caught by auditing claims against the tree; the second by the consumer's own integrity check, which
is the only reason it surfaced at all.

**Fixed and verified on the artifact, not the gate:** index regenerated post-commit, then every
entry's sha256 compared against `git cat-file blob HEAD:<path>` — **0 of 1131 mismatch**. Published
state confirmed from outside: `raw.githubusercontent.com` serves the corrected `xinit.yaml`, its
sha256 equals the published index's entry, and the content carries the fix.

**Owed — the gate that would have caught it:** a release check asserting every index entry's sha256
matches the committed blob it names. Cheap (one `git cat-file` per entry), and it makes the
6a→6b ordering self-enforcing rather than a rule someone has to remember. Pairs with F-440's
CHANGELOG-vs-diff check; both belong in `validate-dod-release.py`.

**Not a defect, recorded so it is not chased:** `p2kb-mcp` still reports the failure in this session
after the fix. It serves a boot-time snapshot and does not reload on republish — a stale read needs
an MCP restart, not `p2kb_refresh`.

F-440 (the CHANGELOG claim that was never applied) is archived — `correction-sweeps/2026-10-03-P2KB-CORRECTION-FINDINGS-archive.md`.

---

## The index and its gzip drifted apart again and the release validator sat red in committed history for four days — F-357's defect, recurred (2026-09-09, ledger re-derivation) — F-405

> **Closed 2026-10-10 («#423»), RESOLVED — both checks this entry said would close it are wired and have
> run.** (1) `audit-yaml-duplicate-keys.py` is a blocking check in `validate-dod-release.py` ("Duplicate YAML
> Keys"; 1,135 files, 0 with duplicate keys, 2026-10-10). (2) The index-freshness check is the `fresh` limb of
> `audit-index-integrity.py` (clone the repo at HEAD, regenerate the index there, compare ignoring
> `system.generated`), with the `gz` limb repeating the pair-consistency check; negative control included.
> Run 2026-10-10 on a clean tree: the index equals a fresh regeneration at HEAD and the `.gz` decompresses to
> exactly the index bytes. The "nothing makes it run" half was already stale on 2026-10-09: `release-yamls`
> §5.5 and §6c and `baseline-health` invoke the runner.

### F-405 — `validate-dod-release.py` exits 1 on a stale gzip, and nothing in this project makes it run — `PARTIAL`

> **Re-checked 2026-10-09 (close-out study «#407», group F):** the "nothing makes it run" half is
> stale — `release-yamls` (§5.5, §6c) and `baseline-health`'s project overlay invoke the DoD runner, and
> the ENH-03 compile gate is now armed through it (`audit-gate-arming.py`). What is still owed is the
> **freshness** limb (regenerate the index in a clone of the commit and compare): build spec in
> `engineering/analysis/2026-10-08-p2kb-close-out-evidence/gates-groupF-specs.md` (new
> `audit-index-integrity.py`, run post-commit). Today the committed index is stale against HEAD.

**Location:** `deliverables/ai/p2kb-index.json` / `deliverables/ai/p2kb-index.json.gz`, and the absence of any trigger for `engineering/tools/validate-dod-release.py`.

**What was measured.** Run at `b0057ec1` before any repair, the release validator reported **`❌ Gzip Compression: FAIL — Gzip content does not match JSON file`** and exited **1** (*VALIDATION FAILURES - DO NOT RELEASE*). The other ten checks passed.

**Why.** Derived from `git log` on the two paths, not recalled:

| | `p2kb-index.json` | `p2kb-index.json.gz` |
|---|---|---|
| last regenerated | `da896073` (2026-09-05) | **`b753a29d` (2026-08-30)** |
| commits touching it since `9ab0433b` | `d55b6c7f`, `da896073` | **none** |

The 2026-09-05 findability pass regenerated the JSON **twice** and the gzip **neither time**. **This is F-357 recurring while F-357 reads `RESOLVED`** — which is what makes it a regression rather than an open item.

**A second, unrelated staleness in the same artifact.** The index was generated on 09-05 and the 09-08 boot-ROM pass (F-403) committed content afterwards. Regenerating updated exactly **two** entries — `p2kbArchBootRomContents` and `p2kbArchIndex` (`architecture/boot-rom/_index.yaml`), mtime and sha256 both — and added or removed none; the count stayed at 1,133. So the pair was *inconsistent* **and** the index was *stale*, and those are two different defects with two different remedies.

**Repaired 2026-09-09.** Both regenerated together, in the required order (the index stores the git blob sha256, so it must be rebuilt after the content commit). `gzip -cd … | cmp -` is clean and the validator is green at 11 of 11.

**Why this is `PARTIAL` and not `RESOLVED`.** The drift is gone; **the reason it happened is not.** The instrument worked — it caught the drift on its first run. What failed is that **nothing invokes the instrument**: a red release gate lived in committed history for four days and was found only because the change ledger was being re-derived. That is the same sentence F-360 has been carrying about the duplicate-key gate, now with a demonstration attached instead of a prediction.

**What closes it — two checks, one wiring pass** (task «#339», block H):
1. Wire `audit-yaml-duplicate-keys.py` into `validate-dod-release.py` as a blocking gate (F-360's open half).
2. Add an **index-freshness** check: run `generate-p2kb-index.py`, then `git diff --quiet` on the pair. The pair-*consistency* check already exists and just proved itself; **freshness** is the one that is missing, and it is what would have caught the two stale boot-ROM entries.

**The generalisable shape, stated so it is not relearned:** *a defect closed by a one-time repair, with no gate wired to the release path, is a defect scheduled to come back.* F-357 is the proof — repaired 2026-08-26, recurred 2026-09-05.

---

## The COG register map's PA/PB row lost the return-vs-parameter distinction, and its index dangles 13 of 16 pointers (2026-08-26, silicon-doc DOCX re-extraction) — F-363 · F-364

> **Closed 2026-10-10 («#423»), RESOLVED — the `yaml_file:` gate this entry named as owed exists and its
> negative control has run.** `validate-crossref-keys.py` resolves every path token in every string,
> `yaml_file:` values included (`check_path_token`); «#410» added the control cases `nc/yaml_file_dangling`,
> `nc/yaml_file_bare` (both must fail) and `nc/yaml_file_good` (must pass). `--negative-control` run
> 2026-10-10: 12 of 12 cases PASS, "NEGATIVE CONTROL: PASS"; the control runs inside the DoD's
> Cross-References check.

### F-364 — the same index advertises 16 register files; 13 of the pointers do not exist — `PARTIAL` (re-verified 2026-10-05 «#386»: pointers removed and shipped; the gate reading `yaml_file:` is not built)

> **Re-checked 2026-10-09 (close-out study «#407», group F):** the gate exists —
> `validate-crossref-keys.py` checks every path token in every string, `yaml_file:` values included
> (`check_path_token`, `:545-567`), and today's 3 pointers resolve. What is owed is a negative-control case
> proving a dangling `yaml_file:` fails (spec in `…/close-out-evidence/gates-groupF-specs.md`); then F-364
> closes.

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

Status: `PARTIAL` (2026-10-05: the `yaml_file:` gate is still owed) — 13 dangling pointers removed, content kept inline, 3/3 remaining pointers
resolve. The instrument gap (no gate reads `yaml_file:`) remains open.
