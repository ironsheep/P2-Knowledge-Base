# Handoff — Ratify DEBUG-window REF↔v55 conflicts against the raw `DebugDisplayUnit.pas`

**To:** the pnut-term-ts / REF-authoring agent (the one that produced the `REF/theory-of-operations/*.md`
distillations of `DebugDisplayUnit.pas`).
**From:** Debug-Window manual fleet-release audit, 2026-07-11.
**Ask:** for each conflict below, rule whether the **raw `DebugDisplayUnit.pas`** supports the **v55
language reference** or the **REF markdown** — or is silent. This decides live manual corrections.

---

## Why this pass exists (read first)

A changeset audit found places where the **v55 language reference text** and our **REF theory-of-ops
markdowns** disagree. We are **not ranking one over the other.** They are two views of the *same* v55
release: v55 text = Chip Gracey's human documentation; `DebugDisplayUnit.pas` = the implementation code;
the **REF markdown = your agent-derived reading of that code.** A conflict means one of three things —
the text is imprecise, the code has a quirk, or **the REF markdown misread the code** — and rank cannot
tell us which.

**Rules for this pass:**
1. **Go to the RAW `DebugDisplayUnit.pas`, not the REF markdown.** Re-reading your own distillation would
   be circular (it can't catch its own misread). The raw `.pas` is **not in our repo** — use your copy.
2. Per conflict, return a verdict: **SUPPORTS-V55** / **SUPPORTS-REF** / **SILENT-OR-AMBIGUOUS**, with the
   **exact `.pas` procedure name + line(s) + code quoted**, and a one-line rationale.
3. If the raw code shows **both** the v55 text and the REF markdown are wrong, say so (a fourth outcome).
4. **Caveat — raw Pascal is not final for *render* behavior.** It is PNut's *intent*; the `pnut-ts` port
   can diverge (we just found a `DEBUG_PIN` set-path bug where the tool disagreed with correct docs). So
   where the code is silent/ambiguous, or the question is "what actually draws on screen," mark
   **NEEDS-HARDWARE** and we'll settle it with a render test on real silicon.

---

## Conflicts to ratify

| # | Window · field | v55 text says | REF markdown says (`.pas` cite) | The question for the raw `.pas` |
|---|----------------|---------------|----------------------------------|----------------------------------|
| **D-F1** | PLOT · `PRECISE` default | v55 L1271: sub-pixel **disabled** (off) at start; `PRECISE` turns it on | REF `PLOT_Theory` L215/L244/L383: `vPrecise := 8` in `PLOT_Configure` = sub-pixel **ON at creation**; `PRECISE` XORs 8↔0 | In `PLOT_Configure` (and `SetDefaults`), what is `vPrecise` initialized to — 8 (on) or 0 (off)? |
| **D-F3** | LOGIC · `DOTSIZE` availability | v55 LOGIC instantiation table **omits** `DOTSIZE` | REF `DEBUG-WINDOW-DIRECTIVE-MATRIX` L90/L260: `DOTSIZE` ✅ accepted for LOGIC | Does the LOGIC configure/key parser accept a `DOTSIZE` (dot) key? Is it honored or a no-op? |
| **F-1** | FFT · channel `grid`/`legend` field | (confirm) — does v55 describe a 4-bit `%abcd` field with **min/max-value legend TEXT** (bits 2–3)? | REF `FFT_Theory` L110/L203: field is **`grid`, 2 bits** — bit0 = baseline line, bit1 = top line. No legend-text | In the FFT channel-def parse + draw, how many bits does the grid/legend field use, and is there any **legend-text** rendering (bits 2–3)? |
| **F-2** | BITMAP · `SPARSE` semantics | (confirm) — round-dot mode, needs `DOTSIZE ≥ 4`, sets the **background** color | REF `BITMAP_Theory` L91/L156/L272: `vSparse` = pixel **border** color; bordered blocks; **no ≥4 gate** | What does `vSparse` color? Round dot vs bordered square block? Any `DOTSIZE ≥ 4` gate? *(Prime NEEDS-HARDWARE candidate — visually verifiable.)* |
| **F-3** | BITMAP · LUT default | (confirm) — LUT-without-palette: entries **0–7 hold default colors** | REF `BITMAP_Theory` L605: `SetDefaults` does **not** init `vLut[]` → **garbage** until `LUTCOLORS` | Does any init populate `vLut[]`, or is it uninitialized until `LUTCOLORS`? |
| **F-4** | POS default (TERM/LOGIC/SCOPE_XY/MIDI) | POS default `0,0` (screen origin) | REF `LOGIC_Theory` L362/L506: **cascaded** (host auto-places) | In `KeyPos` / window-creation, if no `POS` is given, is the window placed at 0,0 or cascaded/auto? |
| **F-5** | TITLE default (TERM/PLOT/LOGIC) | TITLE default **none** | REF `LOGIC_Theory` L361: **(window name)** | With no `TITLE`, is the caption empty, or the window's instance name (or a type string)? |
| **N-1** | PLOT default text color | (confirm) — dropped; current wording is "set COLOR before TEXT" | REF `PLOT_Theory` L242: default text color = **white `$FFFFFF`** | What is the default text color before any `COLOR` is set? |

---

## Already settled empirically (for your cross-check, not for ratification)

These were decided by **hardware** on real P2 (empirical outranks both docs). If your raw-`.pas` reading
would *contradict* these, that itself is a finding (Pascal-vs-silicon, or a `pnut-ts` port divergence) —
flag it:
- **TERM default color = `clLime` `$00FF00`** (EF-025), distinct from the `GREEN` keyword `$09FF09`.
- **SCOPE/FFT `LINESIZE` & SCOPE_XY `DOTSIZE` are whole pixels** (EF-027: `LINESIZE 3 → 3px`, 1:1) — the
  "half-pixel/radius" reading is refuted. *If the `.pas` `SmoothLine` size arg is a radius (`shl 6`),
  explain how that maps to the measured 1:1 pixel width — that reconciles the discrepancy for the record.*

---

## Output we need back

A short table: **# · verdict (SUPPORTS-V55 / SUPPORTS-REF / SILENT / BOTH-WRONG / NEEDS-HARDWARE) ·
`.pas` proc+line quoted · one-line rationale · recommended manual action (keep REF fix / revert to v55 /
run hardware test).** That routes each item: supports-REF → our fix stands; supports-v55 → we revert;
silent/render-dependent → we schedule a hardware render test (PRECISE, BITMAP SPARSE, POS, TITLE are all
visually checkable on the bench).
