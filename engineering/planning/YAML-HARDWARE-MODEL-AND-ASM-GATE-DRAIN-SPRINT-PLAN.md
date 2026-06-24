# YAML Hardware-Model + Assembly-Manual Gate-Drain — Sprint Plan

> **Head:** yaml (P2KB) · **Unblocks:** manual:p2-assembly-language-manual release
> **Plan authored:** 2026-06-24 · **Status:** PLANNING — §Open Questions must reach empty before `sprint-start`
> **Registry:** `engineering/operations/P2KB-CORRECTION-FINDINGS.md` (F-161, F-160, F-121, F-122)

## Goal

Turn the Assembly manual's **RED YAML-HEAD drain gate GREEN** by resolving the
four actionable findings — and, because three of them touch hardware YAMLs,
**make every board in the KB answer the same questions through one self-contained
shape**: *is it an eval-board header occupant, what pin group (8 or 16), which
signal sits at which offset and in which direction, and how does that map to a
real P2 pin (`actual = base + offset`)?* Stand up the long-missing **YAML-head
dashboard** (release ledger + known-hardware inventory) in the same release.

Everything ships in **one YAML release / one commit-release session**.

---

## § Open Questions

**RESOLVED 2026-06-24 (Stephen):**
- **OQ-1 — direction on #64006 boards: YES, normalize** — derive `direction`
  from each pin's explicitly-documented behavior, **preferring an official signal
  name where the name alone conveys direction**. Hard guardrail: *direction
  labeling must never obscure or interfere with understanding the hardware
  function* — be conservative; where direction isn't cleanly stated, keep the
  function clear and leave direction unmarked rather than guess.
  [[feedback_no_inference_or_derivation_in_yaml]]
- **OQ-2 — field shape: approved** as listed (`eval_header_occupant`,
  `pin_group.size`, `signal_map[{offset,signal,direction,notes}]`, `addressing`,
  `base_pin_options`).
- **OQ-3 — F-160: remove from all 3 files.** Confirmed.
- **OQ-4 — version: decided later at `sprint-start`** (build-number step);
  reconcile the v1.10.x/tag-v1.9.1 drift there.

- **OQ-5 — unified eval-header category: FLAT single category** `hardware/eval_addon_boards`
  (the 10 occupants; per-board `series`/type field preserves addon/adapter/memory
  without splitting the browse list). Confirmed 2026-06-24.

**Questions pass: EMPTY — plan ready for `plan-to-tasks`.**

---

## Sprint-start record (2026-06-24)

- **Build number: `v1.11.0`** (YAML head). Minor bump — substantial new content
  (standardized board model, authored HyperRAM board, new `eval_addon_boards`
  category, RDLUT/WRLUT contract facts) plus corrections. Builds on the current
  published **v1.10.1**.
- **Version state — no drift.** Earlier "missing v1.10.x tags" was a false alarm
  (`git tag | tail` lexical-sort artifact). Verified `--sort=version:refname`:
  `v1.10.0→0a61cae2`, `v1.10.1→62be6f63` both exist on their index-regen commits
  per convention; `v1.10.1` is in HEAD. Nothing back-filled.
- **§4 Entry baseline — GREEN.** `validate-yaml-syntax.py` ✓ all valid;
  `validate-crossref-keys.py` ✓ all cross-refs resolved (1783 `related`, 662
  `see_also`, …). Closeout must hold this.
- **§3 Tracking — 4 leftover tasks parked** (3 paused IOSP #54/#46/#47 + 1 pending
  doc-style #110); unrelated to this sprint, not folded in.
- **§2 Working tree — blast radius clean** (only this plan doc, untracked). 3 manual
  workspace-render files modified (Architect, IOSP, Single-Step) — outside blast
  radius, generated renders; left untouched per Stephen.

---

## Design decisions already flagged & settled (this conversation)

- **No cross-YAML→engineering links.** Boards stay self-contained; the
  base+offset *architecture narrative* lives in the dashboard (human-facing,
  engineering side) only. [[feedback_yaml_self_sufficient_references]]
- **Orphans removed outright** (no re-home) — new boards take their place.
- **One combined release**; dashboard created in the same session.
- **Findability:** aliases already present; the real gap is the category JSON
  delete/add + the new `pin_group`/`signal_map` fields.

---

## File table

| # | File | Action | Source of truth |
|---|------|--------|-----------------|
| 1 | `language/pasm2/rdlut.yaml`, `wrlut.yaml` | Add literal `#0–#255` cap, register/PTRx route, bit-8 reason, `##` guardrail | `LUT-Immediate-Addressing-Briefing-for-Doc-Agents.md` |
| 1 | `language/pasm2/{rdlong,wrlong,rdbyte,wrbyte,rdword,wrword,wmlong}.yaml` | One-line shared-cap note | same briefing |
| 2 | `hardware/hardware-compatibility-matrix.yaml`, `edge-mini-breakout.yaml`, `edge-standard-breakout.yaml` | **Remove** `pin_efficiency` (keep `pin_access`) | F-160 (unsourced) |
| 3 | `hardware/addon-{control-board,serial-host,led-matrix,digital-video-out,mini-prototyping,serial-device,goertzel-touch,av-breakout}.yaml` (×8) | Verify vs source; add `pin_group`+`signal_map`+`direction`+`eval_header_occupant`+`addressing` | `sources/p2-eval-add-on-boards/boards/addon-*-64006*.md` |
| 4 | `hardware/addon-hyperram-hyperflash.yaml` | **Author** (16-pin; park `[VERIFY]` OCR fields); fix bare name `p2-eval-board.yaml:145` | `sources/hyperRam-n-hyperFlash/complete-hyperram-hyperflash-reference.md` |
| 5 | `hardware/hub75_adapter.yaml` | Touch-up: flat `pin_offsets:` → standard `signal_map`+`direction`; add `eval_header_occupant`+`pin_group:16` | `sources/p2-hub75-adapter-complete-pinout.md` |
| 6 | `hardware/{7_segment_display,buttons_board,switches_and_leds,switches_board}.yaml` (×4) | **Delete** (zero cross-refs) | F-121 (not #64006) |
| 7 | `engineering/tools/p2kb-categories.json` | **Consolidate** to one `hardware/eval_addon_boards` category = the 10 eval-header occupants (drop 4 orphans, fold in HUB75, add HyperRAM) | consumer of #4 + #6 |
| 8 | `engineering/operations/YAML-HEAD-DASHBOARD.md` | **Create** (engineering tree): release ledger + known-hardware inventory | git tags + this release |
| 9 | `engineering/README.md` | Re-point YAML-head row to the new dashboard | — |
| — | regen index (`generate-p2kb-index.py`) + validate (`validate-crossref-keys.py`, `validate-yaml-syntax.py`) | Post-edit; Path B two-commit per [[reference_index_generator_post_commit]]; **assert index board-set ≡ real set 1:1** | — |

---

## 1. F-161 — RDLUT/WRLUT immediate-address contract *(do first)*

**Why:** the LUT-operand contract omits that a *plain immediate* address is
capped `#0–#255` (a hard compile error past it), the full 0–511 range is reached
only via register/PTRx, and *why* (the 9-bit `S` field's bit-8 is the
pointer/expression selector). Pairs with the manual's OBS-09 — the YAML must
carry the fact the manual derives from.

**Starting point:** `rdlut.yaml`, `wrlut.yaml` present; hub family (`rdlong`
… `wmlong`) all present.

**Target:** add to `rdlut`/`wrlut` the four CONFIRMED facts + the briefing's
guardrails (don't say `#500` "wraps"/"reads wrong long"; don't say "256 longs
inaccessible"; don't recommend `##`; bit-field diagrams not numeric opcodes).
One-line shared-cap note to the 7 hub-family files (it rarely bites there —
20-bit hub addresses use register/PTRx/`##`).

**Verify:** every claim traces to the briefing (no inference); honor guardrails;
parse + crossref clean. *Edge:* the `##500` trap is *documented as a trap*, not
recommended. *Error:* confirm we never imply a silent runtime behavior.

## 2. F-160 — remove the unsourced `pin_efficiency` metric

**Why:** the percentages (87%/30% at identical `pin_access: 40`) have no sourced
definition; the only "fix" is to invent a formula — forbidden. Decision already
made: **remove the field.**

**Starting point:** present in 3 files (see file table). **Target:** delete the
`pin_efficiency` key from all 3; keep `pin_access`. **Verify:** grep confirms
zero remaining occurrences; parse + crossref clean.

## 3. F-121 — #64006 board model standardization (×8)

**Why:** the prior concern was a fabricated lineup; research confirms the
**current 8 files are real** and already carry aliases + a pin map, but **lack
the explicit `pin_group` size and a uniform direction-bearing `signal_map`** — so
an agent can't reliably answer "8 or 16 pins? which signal at which offset, which
direction, what real pin?"

**Starting point:** 8 `addon-*.yaml`, each with prose specs + a pin-map section;
all categorized under `addons`. **Per-board sources** are the short
`boards/addon-*-64006*.md` (cross-edition-verified).

**Target (every board):** full source-diff verification of the existing pin map;
add `eval_header_occupant: true`, `pin_group: {size: 8}`, normalized
`signal_map` (offset → signal + direction + notes), `addressing` note. **Two need
richer shape:** **A/V Breakout** — `signal_map` with a `mode:` dimension
(common / VIDEO / AUDIO, dip-switch-selected); **LED Matrix** — a
`charlieplex_table` (each of 56 LEDs = an offset *pair* HIGH/LOW), not
one-signal-per-pin. **Mini Prototyping** carries raw I/O 0–7 + 5V/VIO/GND
availability (no fixed assignment).

**Verify:** each board's offsets match its source exactly; `pin_group.size: 8`
for all eight; direction present per OQ-1; parse + crossref clean. *Edge:* A/V
mode multiplexing represented without losing the "common" pins. *Error:* no
invented signals.

## 4. F-122 — author the HyperRAM/HyperFlash add-on (16-pin)

**Why:** today it's only a bare name on `p2-eval-board.yaml:145`. **Source:**
`complete-hyperram-hyperflash-reference.md` (pin map triple-validated; already
gives `IO+0..IO+15` offsets + Type = MOSI/MISO/In-Out — direction is *sourced*
here).

**Target:** author `hardware/addon-hyperram-hyperflash.yaml` in the standard
shape — `eval_header_occupant: true`, `pin_group: {size: 16}`, `signal_map`
(offset → HyperBUS signal + direction + device A/B), `addressing` note, aliases.
**Park** the `[VERIFY]` OCR fields (datasheet part #s + URLs) — present but
flagged, not blocking (KNOWLEDGE-GAPS). Register in `p2kb-categories.json`
`addons`. Optionally enrich the `p2-eval-board.yaml:145` descriptive line.

**Verify:** offsets match the reference; `[VERIFY]` fields clearly flagged;
category registered; parse + crossref clean.

## 5. HUB75 (#64032) — schema-alignment touch-up (16-pin)

**Why:** best-documented board but uses a one-off flat `pin_offsets: {CLK: 0,…}`;
bring it onto the shared shape so the *whole* board set speaks one language.

**Starting point:** `hub75_adapter.yaml` — has aliases, `category: addon`,
`base_pin_options: [0,16,32,48]`, flat `pin_offsets`. **Source:**
`p2-hub75-adapter-complete-pinout.md` (explicit base+offset table).

**Target:** convert `pin_offsets` → `signal_map` (offset → signal + direction +
notes), add `eval_header_occupant: true`, `pin_group: {size: 16}`, `addressing`
note. Preserve the panel/scan-rate/driver-chip detail it already carries.

**Verify:** offsets unchanged from source; 14 used + 2 unused represented;
parse + crossref clean.

## 6. Orphan removal + unified eval-header category + 1:1 index integrity

**Why:** two intertwined goals — (a) the 4 fabricated orphans must leave the KB
entirely (files + index), and (b) every eval-header occupant must answer **one
query**, "what eval boards do we know about?", returning the **complete list**.
Today they're split (`addons` = #64006 set + orphans; `adapters` = HUB75;
HyperRAM unregistered), so that question can't be answered cleanly.

**Targets:**
- **Delete** the 4 orphan `hardware/*.yaml` files (zero cross-refs — Sacred Rule
  #7 satisfied, nothing to redirect).
- **Consolidate** `p2kb-categories.json`: one category **`hardware/eval_addon_boards`**
  holding the **10** eval-header occupants — 8×#64006 + `hub75_adapter` (moved
  from `adapters`) + `addon-hyperram-hyperflash` (new). Orphans dropped. Per-board
  `series`/type field preserves addon/adapter/memory distinction without splitting
  the list. *(Pending OQ-5: flat vs. grouped-with-type — flat recommended.)*
- Membership is **also** self-contained per board via `eval_header_occupant: true`
  (the authoritative data-level marker; the category is the browse layer).

**Verify (1:1 integrity gate):** after `generate-p2kb-index.py`, the regenerated
index's eval-board set **equals the real set exactly** — all 10 present, the 4
orphans absent everywhere (files, category JSON, index), no dangling entry, no
missing board. Validator + DoD clean.

## 7. YAML-head dashboard (engineering tree)

**Why:** the YAML head is the only head with no dashboard of its own; no rolling
release history, no hardware inventory, no YAML CHANGELOG. **Home:**
`engineering/operations/YAML-HEAD-DASHBOARD.md` (single file — no folder per
Stephen, 2026-06-24).

**Target (glanceable per [[feedback_dashboard_design_density]]):**
- **Release ledger** — last 4–5 versions, each with *what & why* (seed from git
  tags + corrections register; reconcile the v1.10.x/tag drift per OQ-4).
- **Known-hardware inventory** — every board the KB serves: part #, name,
  pin-group size (8/16), eval-header occupant?, status. The base+offset
  architecture narrative is stated **here** (human-facing), not in the YAML.
- Re-point `engineering/README.md`'s YAML-head row to this dashboard.

**Verify:** dashboard rows match the post-sprint hardware set (incl. HyperRAM,
minus orphans); heads-board link resolves.

## 8. Build / regen / validate (close-out)

Per [[reference_index_generator_post_commit]] (Path B, two-commit): content
commit → `generate-p2kb-index.py` regen → index commit → tag. Run
`validate-yaml-syntax.py` + `validate-crossref-keys.py` + DoD validator green
before release. Re-run `document-audit --depth=release-gate` on the Assembly
manual → expect GREEN → manual unblocks.

---

## Exit / done-means

All 4 findings resolved; every board self-contained in the uniform shape;
orphans gone (files + category); HyperRAM authored; HUB75 aligned; dashboard
live + linked; validators green; **gate GREEN**; one YAML release ready for
`sprint-start` to version + ship.

## Section ↔ task cross-reference (plan-to-tasks, 2026-06-24)

Sprint tag: `yaml-eval-boards` · build `v1.11.0`

| Plan § | Deliverable | Task | seq |
| ------ | ----------- | ---- | --- |
| §1 | F-161 RDLUT/WRLUT immediate-address contract + hub family | «#112» | 13 |
| §2 | F-160 remove `pin_efficiency` (3 files) | «#113» | 14 |
| §3 | F-121 #64006 boards — 6 straightforward | «#114» | 15 |
| §3 | F-121 #64006 boards — 2 complex (A/V dip-mode, LED Charlieplex) | «#115» | 16 |
| §4 | F-122 author HyperRAM/HyperFlash (16-pin) | «#116» | 17 |
| §5 | HUB75 (#64032) schema-alignment touch-up | «#117» | 18 |
| §6 | Orphan removal + unified `eval_addon_boards` category + 1:1 integrity | «#118» | 19 |
| §7 | YAML-head dashboard + heads-board relink | «#119» | 20 |
| §8 | Build / regen / validate + re-open release gate (tag v1.11.0) | «#120» | 21 |

## Skill-evolution candidate (noted, non-blocking)

`release-yamls` should, going forward, append a release-ledger line to
`YAML-HEAD-DASHBOARD.md` at each release (this sprint seeds it by hand). Log to
[[feedback_skill_evolution_candidates]] at retrospective.
