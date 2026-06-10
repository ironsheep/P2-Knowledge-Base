# PASM2 Assembly Language Manual — Full Content Audit, 2026-06-10

**Status: AUDIT WORK IN PROGRESS — manual edits applied, NOT yet certified.**

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

**No PDF / release** until: (1) the 4 deferrals are closed, (2) the P2KB update
sprint lands, and (3) the manual is re-certified against the corrected KB.

## Open items (4 deferrals — need runtime research to close)

These were deferred during application because closing them requires authoring/
research that may change once the KB lands. They are **not** beyond our ability —
they are sequenced after the KB update.

1. **AF-144** (`part-i/chapter-04-timing.md`, §4.6.1) — the "align to 8-cycle
   boundary" loop example needs a corrected, cycle-exact rewrite given the
   corrected RDLONG timing (9–16 clocks, not 2); reconcile the "X total cycles /
   Nx hub period" prose at the same location.
2. **AF-147 / AF-141** (`part-i/chapter-04-timing.md`, §4.2.3) — the `2 / 8-23`
   hubexec-fetch notation is stale after the hubexec-fetch model was overturned;
   decide whether/how to re-ground the notation example.
3. **AF-186** (`part-iii/appendix-g-streamer-constants.md`) — the remaining
   `X_DACS` stereo rows (single-channel + 1N1/stereo pattern rows) need
   Silicon-Doc-accurate descriptions authored.
4. **AF-191** (`part-iii/appendix-h-reserved-words.md`) — the master Spin2
   reserved-word subtotal "586" is a **pre-existing latent defect** (category rows
   never sum to 586); re-derive against the enumerated sections (do not invent a
   total). All locally-enumerable counts were corrected and are internally
   consistent.

## Artifacts

- **Committed:** this report; the 129 manual edits in `opus-master/`; register
  entries F-026..F-097.
- **Local-only (gitignored `audit/full-audit-2026-06-10/`):** full ledger, detail,
  consolidated findings JSON, final verdicts, per-section auditor reports,
  `_APPLY-*.json` subsets.
