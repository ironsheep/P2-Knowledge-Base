# P2KB Correction Findings — Consolidated Register

**Purpose:** A single, append-only register of everything we discover that is **wrong or needs correction** — primarily in the P2 Knowledge Base YAML (`deliverables/ai/P2/`), but also any other source/content correctness issue worth tracking. This is the hand-off document for the agent that corrects the P2KB (via the `yaml-knowledge-base-maintenance` skill).

**How to use this register:**
- When any work (manual production, audits, example compilation, ingestion) surfaces something incorrect, **add it here** — do not leave it only in a per-manual note.
- Each finding gets: an ID, a status, the exact location, what's wrong, the evidence, and the proposed correction.
- The correction agent works the **CONFIRMED** items first, verifying each against the cited authority (compiler / Spin2 v51 spec / Silicon Doc) before editing, then marks them DONE.

**Status legend:** `CONFIRMED` (verified against an authority; ready to fix) · `NEEDS-VERIFICATION` (suspected; must be checked before acting) · `DONE` (corrected + verified) · `WONTFIX` (investigated, not a defect).

**Authority order for P2 language facts:** the `pnut_ts` compiler (ground truth for what compiles) → the Spin2 v51 documentation (`engineering/ingestion/sources/spin2-v51/`) → the Silicon Doc. The KB YAML must match these.

---

## P2KB YAML corrections

### F-001 — `QSIN` / `QCOS` have the wrong signature  ·  `CONFIRMED`

**Files:**
- `deliverables/ai/P2/language/spin2/methods/qsin.yaml`
- `deliverables/ai/P2/language/spin2/methods/qcos.yaml`

**What's wrong:** Both document a **2-argument** signature with the wrong order and a wrong angle-unit model:
- `qsin.yaml` line 6: `syntax: "sine := QSIN(Angle, Length)"`, parameters `Angle` then `Length`, with notes claiming "Angle in P2 angle units (0..$FFFFFFFF = 0..360°)" and "Result = Length × sin(Angle)". Examples use the 2-arg form, e.g. `QSIN($1555_5555, 1000)`.
- `qcos.yaml` mirrors the same error.

**Correct form (verified):** `QSIN(length, step, stepsInCircle) : y` — **three** arguments:
- `length` — the radius / amplitude (output scale)
- `step` — the angle, expressed in units where a full circle = `stepsInCircle`
- `stepsInCircle` — the number of steps in a full revolution (lets the caller choose angle units; it is *not* fixed at `$FFFFFFFF = 360°`)
- returns `y = length × sin(2π · step / stepsInCircle)`

`QCOS(length, step, stepsInCircle) : x` is the cosine counterpart.

**Evidence:**
- Spin2 v51 spec, `engineering/ingestion/sources/spin2-v51/spin2-text.txt:5141–5148`: `QSIN(length, step, stepsInCircle) : y` and `QCOS(length, step, stepsInCircle) : x`. Worked examples in the same source: `qsin(1000, af++, 200)`, `qsin(1000, j, 50_000)`.
- `pnut_ts` v1.55.0: the 3-arg form compiles; the KB 2-arg form fails with `error: Expected ","`.
- Discovered independently by three Debug Window Manual generation agents (SCOPE, SCOPE_XY, PLOT) when KB-form examples would not compile (2026-05-31).

**Proposed correction:** Rewrite both YAMLs' `syntax`, `parameters`, `returns`, `notes`, and `examples` to the 3-argument `(length, step, stepsInCircle)` form. Fix the angle-unit explanation (units are caller-defined via `stepsInCircle`, not a fixed `$FFFFFFFF`). Check `related` CORDIC method/concept files (`rotxy.yaml`, `polxy.yaml`, `xypol.yaml`, `cordic_solver.yaml`) for the same angle-unit confusion while in the area.

---

## To investigate

### F-002 — `?` (RNG) and `||` (abs) operator forms failed to compile in some examples  ·  `NEEDS-VERIFICATION`

During Debug Window Manual generation, agents reported that a bare `?` random-operator form and a `||` absolute-value prefix did not compile in `pnut_ts` v1.55.0 (they substituted `GETRND()` and the `abs` keyword). This may be an **agent usage error** (wrong operator syntax) rather than a KB defect. Before recording as a correction: confirm the exact valid Spin2 syntax for the random operator and absolute value against the v51 spec + compiler, then either close as WONTFIX or, if the KB documents an incorrect form, open a CONFIRMED finding citing the YAML.

---

## Sources to harvest into this register

These pre-existing, scattered findings/gaps docs should be reviewed and any still-valid **P2KB-actionable** items folded in here (then the originals can point back to this register):

- `engineering/document-production/manuals/p2-debug-window-manual/studies/yaml-database-gaps-discovered.md` — debug-window "YAML gaps" (missing window/command YAML). Note: written in the now-retired Discovery voice; the per-window theory-of-operations docs in that manual's `REF/theory-of-operations/` are the authoritative basis for any new debug YAML.
- `engineering/ingestion/external-inputs/pnut_ts_facts/Flash-Loader-P2KB-Update-Request.md` and `…-RCFAST.md` — existing P2KB update requests.
- `engineering/document-production/manuals/p2-assembly-language-manual/audit/` — the PASM2 audit's consolidated findings (e.g. `PART-I-AUDIT-CONSOLIDATED-FINDINGS.md`, the `consistency/findings-task-*.md` set, `HALLUCINATION-PATTERN-FINDINGS.md`) — extract any that indicate the *KB YAML* (not just the manual) is wrong.
- `engineering/ingestion/sources/silicon-doc/silicon-doc-v35-critical-findings.md` — silicon-doc-level findings.

---

*Created 2026-05-31. Append new findings above the "Sources to harvest" section. Keep each finding self-contained and evidence-backed — this register is only as trustworthy as its citations.*
