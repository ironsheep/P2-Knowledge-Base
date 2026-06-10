# PASM2 Assembly Language Manual — Full Content Audit, 2026-06-10

**Status: CONTENT CERTIFIED (2026-06-10) — all three release gates closed; ready for the platform/styling migration.** (PDF/release still pending the styling phase + chip review.) The three gates: (1) 4 deferrals closed [+ the §4.2.3 REP/`9..35` row], (2) P2KB update sprint landed (v1.6.3, all F-026..F-101 verified in local YAML + published index), (3) all ~20 KB-anchored manual fixes re-certified against the final KB (20/20 CERTIFIED, zero discrepancies — see gate-3 note below).

This is the committed status record of the full content audit of the P2 Assembly
Language (PASM2) Manual against the current P2 Knowledge Base. The detailed
per-finding evidence lives in the local (gitignored) working folder
`audit/full-audit-2026-06-10/` (`_ADJUDICATION-LEDGER.md`,
`_ADJUDICATION-DETAIL.md`, `_CONSOLIDATED.json`, `_VERDICTS-final.json`, and the
50 per-section auditor reports).

## Why this audit ran

The manual's last content audit was the periodic audit of 2026-05-23 (v2.3.0).
Since then the KB moved materially — releases through v1.6.2 and, decisively, the
new **`PASM2-ENCODING-REFERENCE.md`** (commit `dfed5c5`, 2026-06-03). New
ground-truth in the KB is the standing trigger for an exhaustive re-audit.

## Method (exhaustive, hand-verified — no severity triage)

- **Stage A — findings:** 50 parallel auditors, one per manual section (22
  instruction-letter files with the 7 largest split, `directives`,
  `special-registers`, `instruction-categories`, 6 Part-I chapters, 10 Part-III
  appendices, front-matter). Each extracted every checkable claim and
  cross-referenced it against the local `deliverables/ai/P2/` YAML + the encoding
  reference. → **208 raw findings.**
- **Stage B — verification:** one adversarial verifier per finding (208), each
  prompted to *refute*, using `pnut-ts` compiler probes + Silicon Doc + Spin2 v51
  as authorities above the KB YAML. Every finding hand-verified; defect side
  re-adjudicated. → **159 confirmed, 17 partially-confirmed, 32 refuted (~15%).**

The ~15% refutation rate validates verifying *every* finding: a fix-them-all
approach would have corrupted ~15% of correct passages. Several auditor
mis-attributions were overturned where the manual was right and the **KB** was
wrong (GETCT 64-bit, HUBSET reset bit, Prop_Hex, the debug-mask gate, ALTI, the
IF_NEVER encoding note).

## Outcome

| Bucket | Count | Disposition |
|--------|-------|-------------|
| Manual-side corrections | 129 | **All applied** to opus-master (this pass); 4 *residual/adjacent* items surfaced + deferred — see below |
| KB/YAML defect candidates | 72 | **Queued** to `engineering/operations/P2KB-CORRECTION-FINDINGS.md` as F-026..F-097 (`NEEDS-VERIFICATION`) |
| Refuted / dropped | 24 | No action (recorded in the ledger) |

### Manual edits applied (all 129)

All 129 findings' in-scope corrections were applied surgically to `opus-master/`
across 29 files, each with a `*.backup.AUDIT-20260610` backup; code-fence/
fenced-div parity verified on all files. During application, 4 **residual/adjacent
issues** surfaced that fell outside the findings' literal scope (a redesign or a
pre-existing latent defect) — the appliers correctly refused to guess and flagged
them for follow-up (see Open items).

### KB defect candidates — queued, NOT confirmed

The 72 KB-side findings are filed **NEEDS-VERIFICATION**, not confirmed. The YAML
is our **primary source**; the manual-audit evidence (though compiler/Silicon-Doc
backed) must be re-confirmed by a dedicated deep-research pass before any YAML is
edited, and some are expected to be refuted on deeper review. Root cause is
documented in the register section header (Silicon Doc never reconciled into the
per-instruction layer; fabrications in unattributed concept files; cross-file
inconsistency).

## ⚠️ Re-certification required (sequencing note)

This audit was run in **reverse** of the canonical order: the manual was corrected
*before* the KB. Because the YAML is primary, the manual must be **re-certified
against the corrected KB** after the P2KB update sprint completes. Specifically:

- 109 of the 129 manual fixes are anchored to the compiler + Silicon Doc directly
  (independent of the KB sprint).
- ~20 manual fixes rest on the KB YAML alone and must be re-checked after the KB
  is corrected: AF-004, 007, 008, 009, 068, 073, 081, 083, 123, 132, 143, 164,
  165, 166, 196, 199, 204, 205, 206, 207.

**No PDF / release** until: ~~(1) the 4 deferrals are closed~~ ✅ **DONE** (AF-144,
AF-147/141, AF-186, AF-191 — see Open items below), ~~(2) the P2KB update
sprint lands~~ ✅ **DONE**, and (3) the manual is re-certified against the corrected KB.

### Gate (2) closed — KB-landing verification (post-v1.6.3)

The P2KB update sprint landed as release **v1.6.3** (content `b0f48a8` + index
`7805b3e`, tag `v1.6.3`). A dedicated landing-verification pass then confirmed that
**every actionable finding F-026..F-101 is present in BOTH the local committed YAML
tree AND the published `p2kb-mcp` index** (index v3.5.0, 1045 entries):

- 4 parallel auditors, one per finding-batch, each reading the register entry,
  the local `deliverables/ai/P2/` YAML, and a `p2kb_get` probe of the published
  index for the affected instruction/concept.
- **All per-instruction and per-concept YAML body fixes verified live in the
  published index.** The only non-MCP rows are by design: encoding-reference-doc /
  generator-script fixes (F-047, F-066, F-067, F-081) and architecture files the
  index does not surface as discrete keys (F-090 `serial_loader.yaml`) — all
  confirmed present in the committed tree.
- The two WONTFIX items (F-036, F-093) were verified correctly **not** re-applied,
  with their rationale still holding.

Gate (2) is therefore **closed**. Remaining release gates: (1) the 4 deferrals and
(3) re-certifying the ~20 KB-anchored manual fixes (AF-004 … AF-207 listed above)
against the now-final v1.6.3 KB.

## Open items (4 deferrals — need runtime research to close)

These were deferred during application because closing them requires authoring/
research that may change once the KB lands. They are **not** beyond our ability —
they are sequenced after the KB update.

1. **AF-144** — ✅ **RESOLVED (post-v1.6.3).** Rewrote the §4.6.1 aligned-loop
   example: corrected `16 total / 2× hub period / 3-cycle wait` (arithmetically
   impossible — floor is 19) to **24 cycles / 3× hub period / constant 5-cycle
   slot-wait**. Verified by closed-form derivation `w_next = (−9 − F) mod 8`
   (independent of entry phase) + cycle traces from three entry phases, against
   the chapter's own §4.3.1 egg-beater model. Prose now notes the loop
   self-aligns after one iteration regardless of the padding NOP.
   ~~(`part-i/chapter-04-timing.md`, §4.6.1) — the "align to 8-cycle
   boundary" loop example needs a corrected, cycle-exact rewrite given the
   corrected RDLONG timing (9–16 clocks, not 2); reconcile the "X total cycles /
   Nx hub period" prose at the same location.
2. **AF-147 / AF-141** — ✅ **RESOLVED (post-v1.6.3).** The §4.2.3 notation row
   `2 / 8-23 | COG mode / Hub mode` was both a non-real notation and the
   overturned per-instruction-fetch model. Re-grounded to a real taken-branch
   example `4 (cog) / 13-20 (hub-exec)` (notation + values sourced from the
   encoding reference's TJV/CALLA/RETA rows) and rewrote the explanation to the
   corrected model (FIFO-prefetched sequential hubexec = 2 cyc; penalty only at
   taken branches / hub data accesses; xref §4.8). **Also fixed in the same
   table (certified):** the "Variable range" row cited a fabricated `9..35`
   value attributed to REP, but P2KB/encoding-reference confirm REP is fixed
   `2/2` (it only loads the hardware repeat counter; `9..35` appears in no
   source). Re-grounded to LOCKNEW's real bounded range `4...11` (`type:
   variable` in `locknew.yaml`), with prose explaining the hub-arbitration
   variability and a note correcting the REP misconception.
   ~~(`part-i/chapter-04-timing.md`, §4.2.3) — the `2 / 8-23`
   hubexec-fetch notation is stale after the hubexec-fetch model was overturned~~
3. **AF-186** — ✅ **RESOLVED (post-v1.6.3).** Rewrote all 16 `X_DACS`
   description cells to Silicon-Doc-exact text (source `silicon-doc/
   part2-pixel-ops.txt:259-280`), replacing vague "1,0 pattern" / "odd inverted"
   language with explicit per-channel `!X0/X0/X1` mappings on every differential
   and X1/X0-pair row. Cross-checked symbol↔`%dddd`↔value pairings against the KB
   `architecture/streamer/dac-routing.yaml` (which already matched the Silicon
   Doc). Symbol names and constant values left unchanged (already verified).
   ~~(`part-iii/appendix-g-streamer-constants.md`) — the remaining
   `X_DACS` stereo rows (single-channel + 1N1/stereo pattern rows) need
   Silicon-Doc-accurate descriptions authored.~~
4. **AF-191** — ✅ **RESOLVED (post-v1.6.3).** Re-derived the Spin2 subtotal by
   summing the 14 enumerated category sections (all of which were verified to
   match their Summary-table rows exactly): 20+120+34+22+11+16+14+32+28+8+27+32+
   12+20 = **396** (the "586" was the latent defect, off by 190). Cascaded the
   correction through every dependent figure in the appendix: Spin2 subtotal
   586→396 (4 places), PASM2+Spin2 total 1,042→**852**, Grand Total 1,236→**1,046**
   (= 456 PASM2 + 396 Spin2 + ~194 hardware). PASM2 subtotal 456 re-checked and
   left (it sums correctly). No invented total — derived purely from what is
   enumerated. (The v1.0.0 CHANGELOG's "1,236+" is left as a historical record.)
   ~~the master Spin2
   reserved-word subtotal "586" is a **pre-existing latent defect**~~

## Artifacts

- **Committed:** this report; the 129 manual edits in `opus-master/`; register
  entries F-026..F-097.
- **Local-only (gitignored `audit/full-audit-2026-06-10/`):** full ledger, detail,
  consolidated findings JSON, final verdicts, per-section auditor reports,
  `_APPLY-*.json` subsets.
