# P2KB Correction Findings — Consolidated Register

**Purpose:** A single, append-only register of everything we discover that is **wrong or needs correction** — primarily in the P2 Knowledge Base YAML (`deliverables/ai/P2/`), but also any other source/content correctness issue worth tracking. This is the hand-off document for the agent that corrects the P2KB (via the `yaml-knowledge-base-maintenance` skill).

**How to use this register:**
- When any work (manual production, audits, example compilation, ingestion) surfaces something incorrect, **add it here** — do not leave it only in a per-manual note.
- Each finding gets: an ID, a status, the exact location, what's wrong, the evidence, and the proposed correction.
- **Annotate as you fix, same pass** — flip the status, add an applied-note + source trace, and log any newly-surfaced defects as new findings. See `yaml-knowledge-base-maintenance` skill §4.5. A stale register (statuses lagging the YAML) lies and invites re-chasing.

**Status legend:** `CONFIRMED` (verified against an authority; ready to fix) · `NEEDS-VERIFICATION` (suspected; must be checked before acting) · `DONE` (corrected + verified) · `WONTFIX` (investigated, not a defect) · `RESOLVED-INVALID` (the reported defect does not exist) · `TRACKED → ingestion` (real, but the resolution lives in the ingestion head, not a YAML edit).

**Authority order for P2 language facts:** the `pnut_ts` compiler (ground truth for what compiles) → the Spin2 v51 documentation (`engineering/ingestion/sources/spin2-v51/`) → the Silicon Doc. The KB YAML must match these.

**Next finding ID: `F-125`**

**Archive:** findings F-001..F-124 (all `DONE` / closed) live in
`engineering/operations/correction-sweeps/2026-06-13-P2KB-CORRECTION-FINDINGS-archive.md`.
**Search the archive before re-filing** — most past defects (and the reasons they were settled) are there.

---

## Carry-forward guardrails — investigated and settled; do NOT re-file (full detail in the archive)

- **F-002 (`WONTFIX`):** `?` / `||` operator-form failures were an agent usage error — the KB is correct (`??var` = XORO32 random; `ABS()` not `||`; `?` is the ternary operator).
- **F-036 (`WONTFIX`):** `calld.yaml` — LOC loading a 20-bit address into PA/PB/PTRA/PTRB is not a defect.
- **F-093 (`WONTFIX`):** `lockrel.yaml` C-flag polarity — the appendix's "inverted" claim is the error; the YAML is correct (C = lock-was-held).
- **F-114b (`RESOLVED-INVALID`):** the MIDI display modes KEYBOARD / GRID / ROLL / MONITOR do **not** exist in PNut v55 — do **not** add them to `midi.yaml` (it carries an explicit `not_supported:` claim).
- **Verified-resolved (don't re-chase):** the Jan-2026 streamer KB audit's issues were all reconciled in the 2026-05/06 passes (DAC routing, 32-pin groups, mode encoding, xcont/xzero phase wording, setxfrq 2³¹ formula, streamer symbols). Only the XZERO concept text was open and is fixed (F-003).

---

## Open — TRACKED in the ingestion head (resolution lives there, not in a YAML edit)

- **F-121 — #64006 P2 Eval Add-on Board roster needs authoritative per-board pin maps via cross-edition ingestion.** Ingest the Aug-2020 `#64006-ES` Product Guide (stage the PDF) and cross-check against the already-ingested Aug-2025 `#64006` edition; reconcile `hardware/addon-*.yaml`. The 2 fabricated entries (`addon-digital-io-board`, `addon-servo-header`) were **removed** in v1.9.0; the 4 part-number-less orphans (`7_segment_display`, `buttons_board`, `switches_and_leds`, `switches_board`) still need verification. Queued in `engineering/ingestion/README.md`. Authoritative 2025 map: A=Control B=Serial Host C=LED Matrix D=Digital Video Out E=Mini Prototyping F=Serial Device G=Goertzel H=A/V Breakout; `#64006-ES` = Complete Accessory Set SKU.
- **F-122 — 64004-ES HyperRAM/HyperFlash add-on board has no standalone YAML.** Product Guide staged + queued as the next ingestion (`sources/hyperRam-n-hyperFlash/`). Do **not** fabricate from raw CAD.
- **F-123 — TAQOZ-Forth / ROM-Monitor capability detail rests partly on preliminary web research.** Grounding plan in `engineering/ingestion/sources/taqoz/taqoz-content-gaps-and-grounding-plan.md` (mine `ROM_Booter.lst`; verify vs Peter Jakacki's `TAQOZ.spin2`).

---

## P2KB YAML corrections

_(No open YAML-correction findings. Append new findings below this line as `### F-125 — …`.)_

---

*Move-aside 2026-06-13 after the v1.9.0 release closed out F-001..F-124. The archive holds the full history; this active register carries only the carry-forward guardrails and the ingestion-tracked items. New findings continue at F-125.*
