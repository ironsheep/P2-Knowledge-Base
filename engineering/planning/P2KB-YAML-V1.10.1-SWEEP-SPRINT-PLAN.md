# P2KB YAML v1.10.1 Sweep — Sprint Plan

**Head:** KB-for-agents (P2KB YAML set)
**Source of truth:** `engineering/operations/P2KB-CORRECTION-FINDINGS.md` (register — complete as of this plan)
**Type:** Plan (ship commitment — apply corrections + additions, release the KB)
**Out of scope (explicit):** all manuals. The IOSP manual's RA-10 reversal and any
manual regeneration are tracked with the IOSP resume, **not** here.

This sprint applies the corrections + additions already filed in the register,
updates the YAML-head dashboards/docs to match, and ships the result as a new KB
release. Each finding was investigated and `CONFIRMED` when logged — the register
carries the file:line + authority for every one; this plan groups them into
deliverables and surfaces the cross-cutting decisions to settle before editing.

---

## § Open Questions — RESOLVED (Stephen, this planning pass)

Per the sprint-plan overlay (3+ YAML files → flag design decisions and wait for
per-decision confirmation). All four settled:

1. **Version — v1.10.1 (patch).** Stephen's call: ship as a **patch**, not a minor.
   Section 6 + all dashboard lines use **v1.10.1**.
2. **G-001 placement — inline.** Add the WRPIN `%AAAA`/`%BBBB` input-selector
   encoding *inline* in `language/pasm2/wrpin.yaml`, with a `related:` from the
   smart-pin routing tables (one home, cross-referenced).
3. **G-004 partial-completion marking — in-file `open_questions:` block.** The stub
   gains the Silicon-backed layer; an explicit `open_questions:` block names the
   Chip-gated sub-parts, and the register entry stays open.
4. **F-153 triage — fix 7, skip 1, full-fix 1.** Apply the 7 clear sub-items; **skip
   `term.yaml` LIME→GREEN** (ruled not-a-bug in F-128 — the constant *is* `clLime`);
   for `precedence.yaml` do **both** (add missing `ADDBITS`/`ADDPINS` **and** align
   the absolute level-numbers to v55).

*Gate met: no open questions remain — plan is execution-ready.*

---

## § Sprint Start — entry checks (2026-06-20)

- **Head/element:** KB-for-agents → the P2KB YAML set (`deliverables/ai/P2/`).
- **Build number:** **v1.10.1** (patch — Stephen's call).
- **Working tree:** blast radius (`deliverables/ai/P2/`) **clean**; `main` in sync with
  `origin/main`. Two uncommitted **planning artifacts** (this plan + the register's
  G-001…G-005 additions) → committed as the sprint foundation before editing.
- **Tracking-readiness:** 8 leftover tasks on the board, all `iosp`-tagged (the IOSP
  manual element — *different head*), paused. None completed (nothing to archive).
  **Decision: leave paused** — they belong to the Smart Pins resume, not folded into
  this YAML sprint. (todo #55 closes here — resolved by F-135.)
- **Baseline-health (entry baseline):** **GREEN** — `validate-yaml-syntax.py` clean ·
  `validate-crossref-keys.py` 100% (0 unresolved). Exit must hold this.

---

## File table — every YAML this sprint touches

> Counts verified against the tree this plan was written from (0 missing).

### Corrections (F-)
| Finding | File(s) | One-line scope |
|---|---|---|
| F-141 | `architecture/smart_pin_patterns.yaml` | 3 wrong register-roles → reconcile to per-mode files + universal init order |
| F-142 ★ | `language/pasm2/wrpin.yaml` | reorder WYPIN-after-DIRH in `critical_requirement` + PWM example |
| F-143 ★ | `architecture/cordic.yaml` | QFRAC=**divide** (not mult), QSQRT 64→32, QMUL unsigned, latency 55 |
| F-144 ★ | `architecture/interrupts.yaml` | INT priority **INT1 highest**; rewrite source-ID table to Silicon |
| F-145 ★ | `language/pasm2/concepts/basic-io.yaml` **+ verify** `language/spin2/concepts/basic-io.yaml` twin | OUTA/OUTB/INA/INB addresses transposed → correct the four |
| F-146 | `language/spin2/concepts/operators.yaml` | `~`/`~~` P2 post-clear/set; fix inverted precedence claims |
| F-147 | `language/pasm2/concepts/addressing_modes.yaml`, `…/register_indirection.yaml` | AUGS/AUGD split by field not width; ALTR is 2-term |
| F-148 | `language/pasm2/{drvrnd,fltrnd,dirrnd}.yaml` + `{dirnot,drvnot,fltnot,outnot}.yaml` (≤7 — **enumerate at start**) | WCZ flag source = **new** OUT/DIR bit, not "original" |
| F-149 | `language/spin2/statements/debug.yaml` | split SCOPE channel-def off the CREATE line (2 examples) |
| F-150 | `language/spin2/patterns/implementation/spin2_pin_control.yaml` | swap smart-pin method args **pin-first** |
| F-151 | `hardware/{hardware-compatibility-matrix,p2-hardware-feature-comparison,p2-hardware-selection-guide}.yaml` | re-sync flash/PSRAM to Edge module detail pages |
| F-152 | **create** `language/spin2/methods/taskcont.yaml`; **stub** `taskresume.yaml`; redirect `taskhalt/taskstop/taskspin.yaml` cross-refs | TASKRESUME fabricated → TASKCONT (stub-don't-delete) |
| F-153 | batch (rdfast, fifo, jnxmt/jnxro, jfbw/jqmt/jxmt/jxrl, setq_block_ops, precedence, plot, p2-architecture-mental-model, cog, term, debug provenance) | per-sub-item triage (see Open Q4) |
| F-154 ★ | `language/spin2/symbols/streamer-symbols.yaml` | un-transpose pin↔DAC-channel counts (description text) |
| F-155 | `architecture/streamer/pin-selection.yaml` | `%101` group is 32 pins, not 24 |
| F-158 ★ | `architecture/streamer/modes-reference.yaml` | `spi_output` → `X_IMM_32X1_1DAC1`; recheck IMM pin counts |

### Additions (G-)
| Gap | File(s) | One-line scope |
|---|---|---|
| G-001 | `language/pasm2/wrpin.yaml` (+ smart-pin routing tables) — *placement = Open Q2* | add A/B input-selector relative-pin encoding + `aliases:` |
| G-002 | `architecture/smart-pins/smart-pin-1000{0,1}-*.yaml`, `smart-pin-1001{0,1}-*.yaml` (+ check `architecture/smart_pins.yaml` overview) | record DIR=0 `Z` preload ($1 timing / $0 period-counting). *Note: the register's "appendix tables" = IOSP manual appendix-f → out of scope.* |
| G-003 | `architecture/smart-pins/smart-pin-0001{0,1}-*.yaml` + DAC resolution claims | add nominal/averaged ENOB caveat (framing only, no number) |
| G-004 | `architecture/smart-pins/smart-pin-11011-usb-host-device.yaml` | add Silicon-backed USB register layer; flag gated remainder (Open Q3) |
| G-005 | `architecture/smart-pins/smart-pin-11110-async-serial-transmit.yaml` | add first-byte glitch as attributed gotcha; flag for HW-confirm |

---

## Section 1 — Sprint entry & register reconciliation

**Why:** the register is the work list; align it + the task tracker before editing.

- **Close todo #55** — resolved by **F-135** (Y=0 is idle; YAML corrected 2026-06-18).
  Its only live consequence (reverse the IOSP manual's RA-10) is **manual work →
  out of scope**; note it on the IOSP resume.
- Confirm the register reflects **F-115 / F-116 / F-119 = DONE** (archived
  2026-06-13) so the dashboard updates in Section 5 are grounded.
- **Verification:** register has zero CONFIRMED items mislabeled open; todo #55 closed.

## Section 2 — Apply corrections (F-)

**Why:** these are confirmed defects in the served KB; the manuals derive from it.

Apply via `yaml-knowledge-base-maintenance` (Sacred Rule #7: never delete a
`related:` — redirect). Group by severity to retire correctness risk first:

- **2a — ★critical:** F-142, F-143, F-144, F-145, F-154, F-158.
- **2b — remaining:** F-141, F-146, F-147, F-148, F-149, F-150, F-151, F-152, F-153, F-155.

Per-finding the register gives the exact site + authority. Special handling:
- **F-145 / F-147 twins** — `basic-io.yaml` exists in both `pasm2` and `spin2`
  concepts; check the spin2 twin for the same transposition (data-set-wide
  discipline) and fix both if present.
- **F-148** — enumerate the exact `*rnd`/`*not` set carrying the "original"
  wording at start (≤7); align flag wording to the plain siblings.
- **F-152** — create `taskcont.yaml`, leave a `taskresume.yaml` **stub** that
  redirects (supersession convention), fix the three cluster cross-refs.

**Verification (each):** `validate-yaml-syntax.py` clean · `validate-crossref-keys.py`
clean · normal case (the corrected claim now matches the cited authority) · edge
(twin files / batch sub-items all swept) · error (no dangling `related:` introduced).

## Section 3 — Apply additions, fully confirmable (G-001, G-002, G-003)

**Why:** content the KB lacks today, each backed by the Silicon Doc.

- **G-001** — WRPIN A/B input-selector encoding (placement per Open Q2) **+ `aliases:`**
  so agents can reach it (findability mandate).
- **G-002** — DIR=0 `Z` preload rule across the four timing-mode files (+ check the
  `smart_pins.yaml` overview). The manual appendix-f tables are out of scope.
- **G-003** — ENOB nominal/averaged caveat at every "16-bit" DAC claim; **no number**.

**Verification:** added text matches the cited Silicon lines; new keys carry
`aliases:`/`related:`; validators clean; a content probe finds the new G-001 field.

## Section 4 — Apply gated additions (G-004, G-005)

**Why:** ship the part we can prove now; leave the gated remainder visibly open.

- **G-004** — add the Silicon-Doc USB register layer (WXPIN/WYPIN/RX-status/IN
  semantics); mark the Chip-gated remainder per Open Q3; **leave the register
  entry open**.
- **G-005** — add the async first-byte glitch as an **attributed** gotcha (Ray
  Rodrick), flagged for hardware confirmation in IOSP Batch 2 (todo #53).

**Verification:** validators clean; gated sub-parts named in-file *and* still open
in the register (not silently "done"); attribution preserved (provenance rule).

## Section 5 — Update dashboards & related docs (NOT manuals)

**Why:** the YAML-head dashboards must tell the truth after the sweep.

- `engineering/README.md` — YAML-head row: drop stale "open: F-115, F-116, G-001";
  reflect F-115/F-116/F-119 **DONE** + the new open/closed set + the shipped version.
- `engineering/ingestion/README.md` — replace the stale "F-116/F-115 YAML round
  (incl. G-001)" next-step line.
- `engineering/operations/P2KB-CORRECTION-FINDINGS.md` — intro/summary counts; mark
  this sprint's F-/G- items resolved (per `punch-list-maintenance`: completed →
  dated archive, active list carries only outstanding work — i.e. the gated G-004/
  G-005 remainders).
- **Verification:** no dashboard still lists a DONE finding as open; counts match the
  register; every link resolves.

## Section 6 — Release (version per Open Q1)

**Why:** publishing IS the act that serves the corrected KB to agents.

Via `release-yamls`, **Path B two-commit** (index generator needs git history):
content commit → regenerate index (`generate-p2kb-index.py`) → index commit + tag →
push. Then refresh `p2kb-mcp` and **verify by content probe**, not version/counts
(push is publish; the MCP serves the published index — restart/refresh, then probe a
known-changed body, e.g. QFRAC=divide or the new G-001 selector field).

**Verification:** DoD (`validate-dod-release.py`) clean · tag present · content probe
returns corrected bodies (F-143 QFRAC, G-001 selector) · no stale-cache false-fail.

---

## Notes / boundaries

- **Gated open questions stay out:** DAC dither cadence, NCO Y=0 validity, scope
  filter taps are KNOWLEDGE-GAPS / Chip-queue items — not confirmable YAML edits, so
  not in this sprint (they ride the IOSP expert/Batch-2 queues).
- **No manuals** touched. The KB→manual propagation (incl. IOSP RA-10 reversal)
  happens when the Smart Pins manual resumes, on top of this released KB.
- **Findability:** every file touched gets a findability glance (aliases/categories)
  per the continual-improvement mandate, not just G-001.

---

## § Section ↔ task cross-reference

Sprint tag: **`yaml-v1.10.1`** · element: P2KB YAML set · foundation commit `6f001d9`.

| Plan § | Deliverable | Task | seq |
| ------ | ----------- | ---- | --- |
| §1 | Entry & register reconciliation (close #55) | «#79» | 6 |
| §2a | ★critical corrections — F-142/143/144/145/154/158 | «#80» | 7 |
| §2b | Remaining corrections — F-141/146/147/148/149/150/151/152/153/155 | «#81» | 8 |
| §3 | Confirmable additions — G-001/002/003 | «#82» | 9 |
| §4 | Gated additions — G-004/005 | «#83» | 10 |
| §5 | Dashboards & related docs (no manuals) | «#84» | 11 |
| §6 | Release v1.10.1 (release-yamls Path B) | «#85» | 12 |

*(8 `iosp` tasks set to `paused` at task-gen — different element, per the entry-check
decision; resume them when the Smart Pins manual work restarts.)*
