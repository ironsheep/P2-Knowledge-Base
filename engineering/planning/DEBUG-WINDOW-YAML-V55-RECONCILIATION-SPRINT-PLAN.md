# DEBUG Window YAML — v55 Reconciliation & Findability Sprint Plan

**Head:** KB-for-agents (P2KB YAML set) · **Version target:** P2KB **v1.8.0** (agreed at start)
**Status:** STARTED 2026-06-11 — §0 decisions confirmed by Stephen as-is; entry checks recorded below
**Authored:** 2026-06-11

## Entry checks (sprint-start, 2026-06-11)

- **Build number:** P2KB **v1.8.0** (agreed).
- **Working tree:** blast radius (debug-displays/, statements/debug.yaml, p2kb-categories.json, index,
  corrections register) **clean** — nothing mid-edit. Source-of-record REF docs (Directive Matrix + 9
  Theory-of-Operations) are **tracked/committed** (solid foundation). Uncommitted = this sprint's setup
  (`AUTHORITATIVE-SOURCES.md`, `INGESTION-AUDIT-MATRIX.md`, this plan) + the **unrelated parked
  front-door WIP** (prototypes, `.gitignore`, etc. — leave untouched). Audit findings files are
  gitignored working scaffolding (repo norm; REF docs are the durable source). **Decision:** recommend a
  foundation commit of the 3 setup files before content edits (Stephen to run); front-door WIP stays parked.
- **Baseline health:** **GREEN** — `validate-yaml-syntax.py` all valid; `validate-crossref-keys.py` 100%
  (1726 `related:` resolved). *Caveat:* crossref-green masks the 5 dead bare-prose `related:` blocks
  (informational whitelist) — exit verification uses read-grep, not the validator (§10/§12).
- **Tracking:** board clean — no in-progress/paused/completed-to-archive; one unrelated parked task
  (#5 PASM/Assembly long-run) left as-is. Entry baseline for the exit no-regression check = this GREEN.

## Purpose

Make the 9 P2 DEBUG display windows fully usable by remote AI agents: every window's
YAML reconciled to the **PNut v55 compiler-trust** source of record, all fabricated
features removed, and the **findability gap closed** so an agent querying "debug terminal"
or "logic analyzer" actually lands on correct content. This is a single sprint — the gap
is blocking agent codegen *today*.

## Source of record (compiler trust — `AUTHORITATIVE-SOURCES.md` #14)

- `engineering/document-production/manuals/p2-debug-window-manual/REF/DEBUG-WINDOW-DIRECTIVE-MATRIX.md`
- `…/REF/theory-of-operations/<WINDOW>_Theory_of_Operations.md` (×9, PNut v55 `DebugDisplayUnit.pas`)
- **Audit basis:** `…/audit/yaml-coverage/00-COVERAGE-MATRIX-AND-FINDINGS.md` + per-window
  `<WINDOW>-yaml-coverage-audit.md` (carry the exhaustive directive/param tables with v55 line cites — the executor builds each YAML *from these*, not from memory).

## Target tree

`deliverables/ai/P2/language/spin2/debug-displays/` (8 existing + 1 new) ·
`language/spin2/statements/debug.yaml` (entry point) · `engineering/tools/p2kb-categories.json` ·
`deliverables/ai/p2kb-index.json` (regenerated) · `engineering/operations/P2KB-CORRECTION-FINDINGS.md`.

---

## §0 — File table + design decisions to flag (CONFIRM BEFORE EDITING)

Per the YAML-change discipline ([[feedback_plan_before_yaml_changes]]): this sprint edits
8 files, creates 1, and adds a concept (aliases/category). The table and decisions below
must be confirmed **before §1 editing begins**.

### File table

| File | Action | Scope |
|------|--------|-------|
| `debug-displays/term.yaml` | **rewrite** | v55 directive surface; strip 9 fabrications (incl. code-12); aliases; related→paths |
| `debug-displays/scope.yaml` | **rewrite** | v55 directives; strip 9 fabricated feature blocks; aliases; related→paths |
| `debug-displays/fft.yaml` | **rewrite** | v55 directives; strip 6 fabrications; fix Hanning/2048; aliases; related |
| `debug-displays/spectro.yaml` | **rewrite** | v55 directives; strip 11 fabrications; fix TRACE-axes; aliases; related |
| `debug-displays/bitmap.yaml` | **rewrite** | v55 23-directive surface; strip 11 fabrications; add PC_KEY/MOUSE; aliases; related |
| `debug-displays/scope_xy.yaml` | **CREATE** | new 9th window; XY/polar; modeled on `plot.yaml`; aliases; related |
| `debug-displays/logic.yaml` | **targeted fix** | param ranges/defaults; fix SAMPLES/DOTSIZE/SPACING/TRIGGER; aliases |
| `debug-displays/plot.yaml` | **enrich** | geometry/sprite param shapes; OBOX label; aliases |
| `debug-displays/midi.yaml` | **enrich (minor)** | aliases; optional RANGE/CHANNEL note; mark phantom-modes RESOLVED-INVALID |
| `statements/debug.yaml` | **edit** | add `related:` full-path down-links to all 9 detail files |
| `tools/p2kb-categories.json` | **edit** | add `spin2.debug_displays` category (9 files) |
| `deliverables/ai/p2kb-index.json` | **regenerate** | post-content commit (two-commit pattern) |
| `operations/P2KB-CORRECTION-FINDINGS.md` | **append** | per-window fabrication findings (resolved same-sprint) |

### Design decisions to flag

1. **SCOPE_XY → new file** (`scope_xy.yaml`, `display_type: SCOPE_XY`), *not* folded into
   scope.yaml. It's a distinct display type with unique directives (POLAR, RANGE,
   persistence-on-SAMPLES, square SIZE). **Recommend: new file, modeled on the v55 `plot.yaml` exemplar.**
2. **Findability field = `aliases:`, NOT `keywords:`.** Research confirmed the index generator
   never reads `keywords:`. (Stated, not a real choice — flagged so no one "helpfully" adds keywords.)
3. **Per-window alias vocabulary** (the searchable terms). Proposed set in §10 — **confirm the
   terms**; these determine what queries resolve.
4. **Register a category** `spin2.debug_displays` in `p2kb-categories.json` listing all 9.
   **Recommend: yes** — gives `p2kb_find` set-browsing.
5. **Entry-point down-links via `related:`** (must-resolve, full paths) from `statements/debug.yaml`
   to the 9 detail files. **Recommend: `related:`** (navigable + validated) over a prose-only `see_also`.
6. **Negative-claims pattern** — each rewritten window documents what it does **not** support
   (MIDI's model), so agents don't re-hallucinate and the retired features stay retired.
   **Recommend: yes**, with a short `not_supported:`/notes block.
7. **`documentation_source` standardized** to `PNut v55 (DebugDisplayUnit.pas)` across all 9.
8. **Corrections-register granularity** — **one summary finding per rewritten window** (counts +
   pointer to its audit file), not 46 atomic rows. **Recommend: per-window summary.**

---

## §1 — TERM rewrite  *(the trigger window)*

**Why:** `term.yaml` is v51 prose; 14 missing directives, 9 fabrications, and the bug that
started this: `"12": clear-screen` is **fabricated** (code 12 is a no-op in v55; clear is `0`/`CLEAR`).
**Current start:** `debug-displays/term.yaml` (full file) · spec: `TERM-yaml-coverage-audit.md`.
**Target:** complete v55 config surface (SIZE cols×rows 1–256, TEXTSIZE, COLOR 4-pair model,
BACKCOLOR, UPDATE, HIDEXY), numeric control codes 0–7 with correct semantics, and
CLEAR/UPDATE/SAVE/PC_KEY/PC_MOUSE keywords — each with type/range/default + v55 line cite.
Strip the 9 prose fabrications (scrollback, copy/paste, ANSI/VT100, themes, timestamps, …).
**Integration:** aliases (§10); `related:`→full paths (term's bare-prose block); inbound link from §10.
**Verify:** *normal* — DEBUG(`TERM…`) example compiles `pnut_ts -d`; *edge* — code 12 documented
as no-op (negative claim), clear shown via 0/CLEAR; *error* — no fabricated capability remains;
`grep` confirms no bare-prose `related:`.

## §2 — SCOPE rewrite

**Why:** fully hallucinated oscilloscope-GUI; 0 real directives, 9 fabricated feature blocks
(Vpp/RMS/frequency cursors, trigger modes, XY/FFT-overlay, play/pause/export) that re-introduce
retired non-existent features. **Start:** `scope.yaml` · spec: `SCOPE-yaml-coverage-audit.md`
(SCOPE_Theory Directive Reference). **Target:** the real ~18 directives (TITLE/SIZE/SAMPLES/RATE/
DOTSIZE/LINESIZE/TEXTSIZE/COLOR/HIDEXY/pack config; TRIGGER/HOLDOFF/CLEAR/SAVE/PC_KEY/PC_MOUSE),
real channel-def grammar, **level-based arm/fire TRIGGER** (not GUI trigger). **Verify:** example
compiles `-d`; TRIGGER semantics match source; zero measurement/cursor features; related resolve.

## §3 — FFT rewrite

**Why:** brochure; ~20 missing directives, 6 fabrications (THD/SNR/peak/harmonic/averaging/
waterfall/markers), MIS-DOC (Hanning is *fixed* — no window choice; SAMPLES max **2048** not 4096;
magnitude-only, no phase). **Start:** `fft.yaml` · spec: `FFT-yaml-coverage-audit.md` (Configure
1552–1618 / Update 1620–1679). **Target:** 12-directive config grammar incl. `SAMPLES {first last}`,
channel-def string `'label' {mag high tall base grid color}`, numeric sample-stream feed,
PC_KEY/PC_MOUSE/CLEAR/SAVE. **Verify:** `-d` compile; Hanning documented as fixed (negative claim);
no measurement features; related resolve.

## §4 — SPECTRO rewrite

**Why:** pre-v55 stub; 20 missing, 11 fabrications (named color maps, persistence, time-freq
cursors), and a **wrong axes model** (axis assignment is TRACE-dependent, not fixed Time/Freq).
**Start:** `spectro.yaml` · spec: `SPECTRO-yaml-coverage-audit.md` (Configure 1719–1790).
**Target:** 13-directive config (SAMPLES/DEPTH/MAG/RANGE/RATE/TRACE/DOTSIZE/color-mode/LOGSCALE/
HIDEXY/pack/TITLE/POS), the **restricted** color set (LUMA8/8W/8X, HSV16/16W/16X only), display +
CLEAR/SAVE/PC_KEY/PC_MOUSE. **Verify:** `-d` compile; TRACE-dependent axes documented; color set
matches source line 1767; no fabricated maps; related resolve.

## §5 — BITMAP rewrite

**Why:** ~0% salvageable placeholder; 23 missing, 11 fabrications (RGBA8888/alpha, zoom/pan,
animation, histogram, color-picker). **Start:** `bitmap.yaml` · spec: `BITMAP-yaml-coverage-audit.md`.
**Target:** full 23-directive v55 surface — 19 color modes (LUT1..RGB24, **max RGB24, no alpha**),
TRACE (8 patterns + scroll bit 0–15), RATE, SPARSE/DOTSIZE, 12 pack keywords, and the CRITICAL
`PC_KEY`/`PC_MOUSE` interactive section (2-LONG layout + Y-inversion note). Do **not** add
SPRITE/SPRITEDEF (those are PLOT). **Verify:** `-d` compile; no 32-bit/alpha/zoom claims; related resolve.

## §6 — SCOPE_XY new file

**Why:** the 9th window is entirely unrepresented. **Start:** none — greenfield ·
spec: `SCOPE_XY-yaml-coverage-audit.md` (Configure 1386–1441 / Update 1443–1509). **Target:** new
`scope_xy.yaml`, `display_type: SCOPE_XY`, modeled on v55 `plot.yaml` structure: 14 config directives
(TITLE/POS/SIZE-as-radius/RANGE/SAMPLES/RATE/DOTSIZE/TEXTSIZE/COLOR/**POLAR {twopi {theta}}**/
LOGSCALE/HIDEXY/pack/label), 5 display (XY & rho-theta numeric stream, CLEAR, SAVE, PC_KEY, PC_MOUSE).
Document unique features: signal-vs-signal XY (Lissajous/phase), Cartesian+polar, RANGE explicit
extent, persistence-on-SAMPLES (`0`=persistent accumulate; `>0`=fading trail). **Negative claims:**
no TRIGGER/HOLDOFF/LINESIZE/auto-range/UPDATE; **`PC_MOUSE` returns raw client pixels, not
scaled/polar values** (no `dis_scope_xy` branch in SendMousePos). **Verify:** `-d` compile;
appears in index with aliases + category; related resolve to siblings.

## §7 — LOGIC targeted fix

**Why:** mostly v55-correct but param-level defects. **Start:** `logic.yaml` · spec:
`LOGIC-yaml-coverage-audit.md`. **Target (in-place edits, not rewrite):** remove fabricated
`SAMPLES {first last}` (LOGIC SAMPLES is single int 4–2047) and `DOTSIZE x {y}` (single scalar 0–32);
fix `SPACING` (it's *horizontal* sample spacing / X time-base, not vertical channel spacing); document
`TRIGGER` as **edge-armed** (disarm→arm→fire); add the full v55 numeric ranges/defaults
(SAMPLES/SPACING/RATE/DOTSIZE/LINESIZE/TEXTSIZE/HOLDOFF/offset). Preserve LOGIC's existing correct
disclaimers (no protocol decode). **Verify:** `-d` compile; each fixed param matches source range;
existing 3 related still resolve.

## §8 — PLOT enrichment

**Why:** v55-complete breadth, but param shapes elided — an agent can't emit valid sprite/geometry
streams. **Start:** `plot.yaml` (already v55, no edition drift) · spec: `PLOT-yaml-coverage-audit.md`.
**Target:** fill geometry param shapes (CIRCLE/OVAL/BOX/OBOX with `linesize 0 = filled`; relabel
**OBOX = rounded** rect, not "outlined"); SPRITEDEF element-array shape + SPRITE params
(`id 0–255 / xsize·ysize 1–32 / orient 0–7 / scale 1–64`); config defaults (SIZE 256×256, DOTSIZE
1–256, OPACITY 0–255, LAYER 1–8); TEXT inline-override `{size {style {angle}}}`; SAVE region syntax.
**No** separate `plot-layers.yaml` (LAYER/CROP/SPRITE share PLOT dispatch state). **Verify:** sprite
+ geometry examples compile `-d`; related already clean.

## §9 — MIDI minor enrichment

**Why:** clean/v55-accurate — lightest touch. **Start:** `midi.yaml` · spec:
`MIDI-yaml-coverage-audit.md`. **Target:** add aliases (§10); optional inline RANGE default/clamp +
CHANNEL "0 = channel-0-only" note; keep the explicit HIDEXY-rejected negative claim. **Verify:**
both related still resolve; primary queries land.

## §10 — Findability layer (all 9 + entry points)

**Why:** the root cause. Index harvests only `aliases:`; the 9 files have none and are in no
category; the parent enumerates windows as prose but links to none.
**Work:**
1. **`aliases:` on all 9** (generator auto-adds UPPERCASE; include lowercase phrasings). Proposed —
   **confirm (decision 3):** TERM=`terminal, text window, serial terminal, DEBUG TERM`; SCOPE=`oscilloscope,
   waveform, analog display, DEBUG SCOPE`; SCOPE_XY=`XY oscilloscope, Lissajous, polar plot, phase plot,
   scope_xy`; FFT=`spectrum, frequency display, DEBUG FFT`; SPECTRO=`spectrogram, waterfall, DEBUG
   SPECTRO`; PLOT=`plot, sprite, layer, canvas, polar plot, DEBUG PLOT`; BITMAP=`bitmap, image display,
   framebuffer, DEBUG BITMAP`; LOGIC=`logic analyzer, digital signals, waveform, DEBUG LOGIC`;
   MIDI=`MIDI, piano keyboard, note display, DEBUG MIDI`.
2. **Category** `spin2.debug_displays` in `p2kb-categories.json` listing all 9.
3. **Repair bare-prose `related:`** → full paths in term/scope/fft/spectro/bitmap (template: plot/logic/midi).
   Find by **reading** — the validator passes them silently (INFORMATIONAL whitelist).
4. **Entry-point down-links:** add `related:` full paths to all 9 in `statements/debug.yaml`
   (it already lists them as prose); consider same in `debug-commands/debug.yaml`.
**Verify:** *normal* — `p2kb_find` for each proposed alias resolves to the right key (post-regen,
post-push, content-probe per [[reference_p2kb_mcp_serves_published]]); *edge* — category browse returns
the set of 9; *error* — `validate-crossref-keys.py` clean AND a read-grep confirms zero remaining
bare-prose `related:`.

## §11 — Corrections register

**Why:** the ~46 fabrications are confirmed P2KB defects; the register is the system of record
([[project_p2kb_corrections_register]]). **Work:** append one **summary finding per rewritten window**
(TERM/SCOPE/FFT/SPECTRO/BITMAP) to `P2KB-CORRECTION-FINDINGS.md` — fabrication count + pointer to the
window's audit file + "resolved in v1.8.0 §N". Mark MIDI phantom-modes (KEYBOARD/GRID/ROLL/MONITOR)
**RESOLVED-INVALID**. **Verify:** every window's fabrications have a register line; statuses set.

## §12 — Validate, regenerate index, release v1.8.0

**Why:** publish so agents get it (push = publish). **Work:** run `validate-yaml-syntax.py` +
`validate-crossref-keys.py` (expect 100%); compile all changed DEBUG examples `pnut_ts -d`;
`validate-dod-release.py`. Then the **two-commit index pattern** ([[reference_index_generator_post_commit]]):
content commit → `generate-p2kb-index.py` → index commit → tag `v1.8.0`. Confirm the new `scope_xy`
key + all 9 aliases + the category are in `p2kb-index.json`. Post-push: `p2kb_refresh` + restart MCP +
**content-probe** TERM/SCOPE_XY (counts/version can lie — probe bodies). **Verify:** *normal* — fresh
agent query "debug terminal window" → term.yaml body; *edge* — "XY oscilloscope" → scope_xy.yaml;
*error* — no validator failures, no `-d` compile errors, DoD ALL PASS.

---

## Verification summary (sprint exit)

- All 9 windows reconciled to v55; **zero fabricated features** remain (read-audit, not just validator).
- Every DEBUG code example compiles under `pnut_ts -d`.
- `p2kb_find` resolves each window by natural-language alias; category browse returns the 9-set.
- crossref 100%, DoD ALL PASS, index regenerated, MCP content-probe confirms TERM + SCOPE_XY live.
- Corrections register carries the fabrication findings (resolved); MIDI phantom-modes closed-invalid.

## Out of scope (named, not silently dropped)

- The **single-step debugger** (`DebuggerUnit.pas`) — excluded by the source matrix by design.
- The debug **manual** (PDF) — its REF docs are the *source* here; manual regeneration is a separate
  manual-production effort, not this YAML sprint.
- Migrating the compiler-trust REF docs out of the manual workspace into `external-inputs/` — flagged
  earlier as a placement question; deferred to the ingestion-head prototype work.

---

## Section ↔ task cross-reference (sprint tag `debug-window-v55`)

Tasks generated by `plan-to-tasks` 2026-06-11. Per-window aliases + `related:` repair are folded into
each window's task (§1–§9); §10 carries only the cross-cutting wiring; §12 split into a validation gate
(#39) + release (#40).

| Plan § | Deliverable | Task | seq |
|--------|-------------|------|-----|
| §1 | TERM rewrite (template-setter; trigger window) | «#28» | 2 |
| §2 | SCOPE rewrite | «#29» | 3 |
| §3 | FFT rewrite | «#30» | 4 |
| §4 | SPECTRO rewrite | «#31» | 5 |
| §5 | BITMAP rewrite | «#32» | 6 |
| §6 | SCOPE_XY create (9th window) | «#33» | 7 |
| §7 | LOGIC targeted fix | «#34» | 8 |
| §8 | PLOT enrichment | «#35» | 9 |
| §9 | MIDI minor enrichment | «#36» | 10 |
| §10 | Findability wiring (category + entry-point down-links) | «#37» | 11 |
| §11 | Corrections register | «#38» | 12 |
| §12 | Final validation gate | «#39» | 13 |
| §12 | Release P2KB v1.8.0 | «#40» | 14 |

*Note:* the unrelated parked task «#5» (PASM/Assembly long-run) holds seq 1; work this sprint with
`todo_next tags:["debug-window-v55"]` so the set walks #28→#40 in order regardless of #5.
