# P2KB Correction Plan — Fix Pass

**Date:** 2026-05-31
**Companion:** `P2KB-CORRECTION-FINDINGS.md` (the findings + the per-finding "Root-source verification" table). This plan is *how* we apply them.

---

## Governing principle: hard facts only

**The trusted YAML contains only facts traceable to a golden ingestion source (`engineering/ingestion/sources/`).** This is the basis of the trust chain — a consumer (an AI generating code, or a human) must be able to rely on every claim.

- **Add only what a golden source states.** Every edit cites its source (file + line/row).
- **Deterministic derivation from stated facts is allowed** — applying a documented formula, computing a value from stated inputs. That is arithmetic on hard facts, not inference.
- **Speculation about un-stated behavior is forbidden.** If no golden source supports it, it does not go in — even if it "seems obvious from the mechanism." Verify it to root first, leave it out, or log it as an explicit *known-unknown* (clearly marked not-a-fact). Never assert it.

We removed a manual's worth of inference-presented-as-fact this session; we do not reintroduce any.

## Method

- **Tool:** `yaml-knowledge-base-maintenance` skill — edit in place, no renames.
- **Sacred Rule #7:** never delete a cross-reference; redirect it to where the content now lives.
- **Every edit cites its golden source.** No edit without a citation.
- **Compile-check** any code examples added/changed (`pnut_ts`).
- **After edits:** `validate-crossref-keys.py` → `generate-p2kb-index.py` (post-commit, Path-B two-commit: content commit → regen → index commit → tag) → publish so `p2kb-mcp` serves the corrected KB.

---

## Edit plan (priority order)

### Batch 1 — Safety-critical silicon errata

| F | Files | Edit | Golden source |
|---|-------|------|---------------|
| **F-006** | `pasm2/concepts/setq_block_ops.yaml` (+ hazard note in `setq.yaml`, `rdlong.yaml`; mirror for `wrlong.yaml`/`wmlong.yaml`) | Add `silicon_errata`: an intervening ALTx/AUGS/AUGD between SETQ/SETQ2 and a PTRx block transfer cancels the block-size PTRx delta (PTRx += 4, not N×4). Include the doc's code example + workaround (keep them adjacent). | `silicon-doc/p2-documentation.txt:197–211` (KNOWN BUGS, Rev C) — verbatim |
| **F-007** | `pasm2/augs.yaml` | Add `silicon_errata`: an ALTx with immediate `#S` between AUGS and its target is also augmented; workaround = use a register for the ALTx S operand. **AUGS only.** | `…p2-documentation.txt:212–227` (Rev C) — verbatim |
| **F-012** | `architecture/io_pin_timing.yaml` (+ cross-ref from `smart_pins.yaml`, a hardware guide) | Add `absolute_maximum_ratings` + `input_voltage_and_protection`: pin abs-max `-0.3 V to (Vxxyy+0.3 V)` ≈ 3.6 V; internal protection diode to the I/O rail; ±10 mA forward-bias limit; verbatim datasheet footnote; "reading >3.6 V (e.g. 5 V) needs a series resistor sized to keep diode current ≤ ±10 mA" with the Ohm's-law derivation shown. | `p2-datasheet/p2-datasheet-narrative.txt:6185–6241` (abs-max table + footnote 1) |

> **F-007 / AUGD (hard-facts rule):** the Silicon Doc names only **AUGS**. We do **not** add an AUGD errata claim. Logged as a known-unknown in the findings register; verify against hardware / a future silicon-doc rev before ever asserting it.

### Batch 2 — Instruction-fact corrections

| F | Files | Edit | Golden source |
|---|-------|------|---------------|
| **F-009** | ~30 non-RND `bit*/dir*/drv*/out*/flt*.yaml` | Set `flags_affected.C` **and `.Z`** (currently `C: No effect`) and the blank `encoding[].c`/`.z` fields to the original target bit — BIT: `original D[S[4:0]]`; DIR: `DIR bit`; OUT/FLT/DRV: `OUT bit`. Mirror the already-correct RND-variant wording. | `p2-instructions-csv/…Rev B_C Silicon.csv` rows 43–381 (`C,Z = …`) |
| **F-008** | `pasm2/concepts/conditional_execution.yaml` | Add the missing per-code aliases **and fix the misplacement**: move `IF_BE`/`IF_LE` from `%1011` to `%1110`. | `pnut-ts-pasm-ref/PASM2-Condition-Codes.json` + CSV 411–460 |
| **F-001** | `spin2/methods/qsin.yaml`, `qcos.yaml` | Rewrite `syntax`/`parameters`/`returns`/`notes`/`examples` to `QSIN(length, step, stepsInCircle)`; fix the angle-unit model (caller-defined via `stepsInCircle`). Check `related` CORDIC files for the same confusion. Compile-check examples. | `spin2-v51/spin2-text.txt:5141–5148` + `pnut_ts` |
| **F-003** | `pasm2/concepts/streamer_smartpin_control.yaml` | Replace the XZERO `operation: "Stream zeros (no hub read)"` with "buffer command on final NCO rollover, zeroing the NCO phase accumulator." (`xzero.yaml` is already correct — align to it.) | `…p2-documentation.txt:2743` + `:3508–3519` |
| **F-010** | `pasm2/concepts/cog_hub_execution.yaml` | Replace the `common_mistakes` "REP in hubexec — Won't work!" entry with the correct note: REP works in hubexec, paying the hidden-jump (FIFO-refill) cost per iteration. | `…p2-documentation.txt:1733` |

### Batch 3 — Re-grounding + cross-references

| F | Files | Edit | Golden source |
|---|-------|------|---------------|
| **F-005** | *(HELD — see below)* `spin2/debug-displays/{plot,logic,midi}.yaml`; `spin2/debug-commands/{pc_key,pc_mouse}.yaml` | **Deferred.** Re-ground from the official doc once the theory-of-operations are refreshed. | `spin2-v51/debug-section.txt`; v3 manual chapters corroborate |

> **F-005 HELD (2026-05-31, user direction).** Do not fix debug-related KB facts in this pass. The re-grounding source (the per-window theory-of-operations Bibles) was reverse-engineered from PNut v51a; the compiler/DEBUG feature set may have changed since. **Refresh the theory-of-operations against the current compiler first**, then lift the hold. This also gates the Debug Window Manual.
| **F-004** | 7 `deliverables/ai/P2/` files | Redirect stale `engineering/knowledge-base/P2/<x>` refs → `deliverables/ai/P2/<x>` (the content's current home). Run cross-ref validator after. | actual current file locations |

### Batch 4 — Low priority

| F | Files | Edit | Golden source |
|---|-------|------|---------------|
| **F-011** | new `pasm2/idioms/_index.yaml` only | Add the idioms discovery/compendium index (mirror `architecture/streamer/_index.yaml`, `boot-rom/_index.yaml`). **Item A (inline `halt_technique` into `hubset.yaml`) is NOT done** — already documented in `idioms/halt-and-fault-response.yaml` and cross-linked from `hubset.yaml`; inlining would duplicate a fact and invite drift. | existing idiom files + `streamer/_index.yaml` pattern |

---

## Flagged decisions — RESOLVED (2026-05-31)

1. **F-005 — HELD.** Deferred until the debug theory-of-operations are refreshed against the current compiler. No depth decision needed now.
2. **F-008 aliases — assembler-facing only.** Add only the `IF_` aliases. Do **not** add compiler-internal underscore forms (`_GT`, `_NC`, …) — the user (consumer) writes assembler, not compiler internals; that's the gate.
3. **F-011 — index only.** Do **Item B** (`idioms/_index.yaml`). **Item A is closed as resolved-by-cross-ref** (no inline; do not revisit).
4. **AUGD (F-007) — HELD.** Document AUGS only; log AUGD as a known-unknown; do not assert it.

## Definition of done
- Every edit cites a golden source; zero un-cited additions.
- `validate-crossref-keys.py` clean (F-004, F-005).
- Any added/changed code examples compile (`pnut_ts`).
- Index regenerated (Path B) and tagged; KB published so `p2kb-mcp` serves the corrections.
