# Debug-window YAML enrichment plan (F-205b / F-206 / F-207 / F-208)

**Date:** 2026-07-11 · **Head:** yaml (P2KB) · **Rides:** KB release rail (fleet-release §9 / #181)
**Gate:** PLAN-GATED — 8 YAML files → file table + flagged decisions + **wait for Stephen sign-off**
(overlay: 3+ YAML files; `feedback_plan_before_yaml_changes`). **No YAML edit starts until confirmed.**

These four findings were surfaced *after* the §3b operator-sweep sign-off, during the 2026-07-10/11
Debug hardware session. They are the residual "OPEN YAML ENRICHMENTS" from the fleet-release resume
pointer. All are grounded in empirical ledger entries (EF-028/031/032) and/or verbatim v55 text —
**no inference/derivation** (`feedback_no_inference_or_derivation_in_yaml`). The manual side of
F-205 and F-208 is already applied + committed (#195); this plan is the KB-rail counterpart so the
YAML stays consistent with the corrected manual and a remote agent can't regenerate the defects.

---

## File table

| # | File | Finding | Current (verbatim) | Proposed change | Grounding |
|---|------|---------|--------------------|-----------------|-----------|
| 1 | `debug-displays/plot.yaml:67` | F-205b | `TEXTSTYLE n -- style byte 0..255: weight bits0-1, italic bit2, underline bit3, horizontal-align bits4-5, vertical-align bits6-7` | Append the per-axis value→direction mapping + weight caveat: horiz `%10`=right/`%11`=left; vert `%10`=top/`%11`=bottom; weight bits select a nominal weight (thin/normal/bold/heavy) that the DEBUG font does **not** render distinctly. | EF-031 (justification, HW, both platforms) + EF-028 (weight, HW) |
| 2 | `debug-displays/plot.yaml:62` | F-208 | `POLAR ... twopi -1/0 select clockwise/counter-clockwise sense.` | State **θ=0 points East (+x)**; default (positive `twopi`, `$1_0000_0000`) sweep is **counter-clockwise**; a **negative** `twopi` reverses to clockwise. Replace the murky `"twopi -1/0"` shorthand with the sign-based rule. | EF-032 (Test J, both platforms) |
| 3 | `debug-displays/term.yaml:45` | F-206 | `SAVE -- write the window bitmap to <name>.bmp` | Standardize → `SAVE {WINDOW} 'filename' -- write the window (or display-area) bitmap to <filename>.bmp (filename required; WINDOW optional)` | v55 L1139; REF matrix `KeySave` |
| 4 | `debug-displays/fft.yaml:56` | F-206 | `SAVE -- write the window bitmap to <name>.bmp` | same standardization as #3 | v55 L1169; REF matrix |
| 5 | `debug-displays/logic.yaml:46` | F-206 | `SAVE {filename} -- write the window bitmap to <name>.bmp (also a WINDOW / 'l t w h' region variant)` | change `{filename}` → required `'filename'`: `SAVE {WINDOW} 'filename' -- ... (also 'l t w h' region variant)` | v55 L1194; REF matrix |
| 6 | `debug-displays/midi.yaml:38` | F-206 | `SAVE {filename} -- write the window bitmap to <name>.bmp` | same standardization | v55 L1246; REF matrix |
| 7 | `debug-displays/scope.yaml:58` | F-206 | `SAVE {filename} -- write the window bitmap to <name>.bmp` | same standardization | v55 L1222; REF matrix |
| 8 | `debug-displays/scope_xy.yaml:50` | F-206 | `SAVE {filename} -- write the window bitmap to <name>.bmp` | same standardization | v55 L1294; REF matrix |
| 9 | `debug-displays/logic.yaml` (examples + `packed`/`channel_definition_string`) | F-207 A+B | modes listed at `:37`; channel-def at `:38`; no full-window feed example | (A) add a **packed full-window array-feed** example — `` `uhex_long_array_(@buff, N) `` per v55 L1144 — + caveat *a single `` `(packed) `` long advances the scrolling window by one column only; the full window needs the array feed*. (B) add the **mode↔channel-count** rule: for LOGIC, `LONGS_NBIT` ⇒ N one-bit channels (each sub-sample carries one bit per channel per time-step). | v55 L1143–1144 (verbatim) + L1406 (LONGS_1BIT unpack); EF (F-207 Facet B, ch13 B2 dual-channel HW-confirmed 07-11) |
| 10 | `debug-displays/scope.yaml` (examples + `packed:39`) | F-207 A+B | `packed: LONGS_1BIT..BYTES_4BIT ...` at `:39`; no array-feed example | (A) add the same array-feed example + scrolling-window caveat (SCOPE fragments to the left edge without it). (B) note the SCOPE **value-interleave** form: an 8-bit-packed sub-sample is a full per-channel value; channels interleave across consecutive sub-samples (cf. `ch13-packed-scope`, 2 ch via `LONGS_8BIT`). | v55 L1144 pattern; ch13-packed-scope HW render |
| 11 | `statements/debug.yaml` (packed-feed note near `:131`) | F-207 A | `' Logic analyzer: create with named channels, then feed packed samples by name` | add a one-line note that the packed **scrolling**-window feed is the full-window array form `` `uhex_long_array_(@buff, N) `` (BITMAP tolerates a per-long packed feed; LOGIC/SCOPE do not). | v55 L1144; F-207 |

`plot.yaml:77` SAVE is already correct (`SAVE 'name' ...`) → **no change** (F-206 exempts it).
BITMAP is **exempt** from F-207 (frame-buffer window tolerates a per-long packed feed).

---

## Flagged decisions

- **D1 — F-206 bare-`SAVE` lenient form.** `pnut-ts -d` **accepts** a bare `SAVE` (no filename) as
  *syntactically legal* (verified 2026-07-11: `debug(\`MyPlot SAVE)` compiles clean). Whether Term-TS
  *auto-generates* a filename at runtime is unverified (would need hardware/Term-TS). **Proposal:**
  standardize all six YAMLs to the **required-filename** teaching form (`SAVE {WINDOW} 'filename'`),
  and do **not** document a bare-SAVE alternate (unverified runtime behavior; not the form to teach).
  *Decision needed: OK to omit the lenient-alternate note?*
- **D2 — F-207 example size in the YAML.** The v55 authority example (L1144) is a full smart-pin +
  streamer capture demo. **Proposal:** put a **minimal** array-feed snippet in the YAML example
  (`VAR buff[N]` → pack loop → `` `uhex_long_array_(@buff, N) ``) rather than transcribe the whole
  streamer example — the YAML documents the *feed shape*, not a streamer tutorial. *Decision needed:
  minimal snippet vs verbatim v55 example?*
- **D3 — new finding ID.** These consume **F-209** for the bundle registration (F-205b/206/207/208
  already have IDs). No new IDs needed for the edits themselves.

## Verify-first (at edit time)

- **F-207 A wording** — pull the LONGS_2BIT unpack sentence verbatim from v55 L1143 ("*By invoking
  the LONGS_2BIT packed-data mode … yielding 16 sets per long*") and L1406 (LONGS_1BIT = "*32 separate
  1-bit values, starting from the LSB*"); **do not paraphrase**.
- **Post-edit gate** — `validate-yaml-syntax` + `validate-crossref-keys.py` green, index regen, then
  `release-yamls` (p2kb_refresh + MCP restart + content-probe). F-204 (rdpin.yaml, already applied)
  rides the same KB-rail publish.

## Not in this batch (already done)

- §3b operator-sweep YAMLs + **F-204** rdpin.yaml one-NOP fix — **applied** (rdpin.yaml:18 shows the
  single NOP). This batch is *only* the late-surfaced Debug-window enrichments.
