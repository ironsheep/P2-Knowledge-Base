# Changeset-Integrity Audit — P2AN004

**Doc:** P2AN004 — "Read Real-World Sensors by Frequency, Rotation, and RC Timing on a P2 Pin"
**Baseline tag:** P2AN004-v1.0.0 (`8b2d2e8b`)
**HEAD audited:** `60d0a18a`
**Diff scope:** `git diff P2AN004-v1.0.0..HEAD -- .../app-notes/P2AN004 .../workspace/P2AN004`
**Hunks:** 3 (all in commit `f3e702ed`, "Fabrication-audit §6"), across 2 files
**Audit stance:** Independent / adversarial — each hunk anchored to a PRIMARY source (Silicon Doc / Spin2 v55), not to the sweep catalog's assertion.

**BOTTOM LINE:** All 3 hunks are `faithful`. Each removes a real, disprovable defect (a fabricated "300 MHz max" spec, a wrong filter-length profile, a title naming a nonexistent "Period" instrument) and replaces it with a claim confirmed verbatim in a Tier-1 source. Zero flags. Ship.

---

## Traceability table

| File | Hunk summary | Traced source (verified this audit) | Verdict | Note |
|------|--------------|-------------------------------------|---------|------|
| `opus-master/P2AN004.md` §R3 Hardware callout (line 304) | `P_FILT1_AB` "two-clock input filtering" → "route A/B through the global FILT1 digital filter (reset default ≈600 ns low-pass)" | Silicon Doc `part3-pages-37-38.txt` L20-58: four **global** filters usable by each smart pin; **filt1** reset default = length 1 (3 ff), tap 5, **600 ns** (6.25ns×3×32). Spin2 v55 `spin2-v55-text.txt` L1451: `P_FILT1_AB` = "Select FILT1 settings for A, B". | `faithful` | Old "two-clock" (=12.5 ns, 2 ff, tap 0) was the reset default of **FILT0**, not FILT1 — an outright wrong figure. New text is exact to source. |
| `opus-master/P2AN004.md` §Pitfalls "stay at a legal clock" (line ~336) | "The P2's specified maximum is 300 MHz" → "200 MHz — the top of the P2 PLL VCO's designed 100–200 MHz range, so they sit comfortably within spec." | Silicon Doc `p2-documentation.txt` L6233: "The PLL's VCO is designed to run between 100 MHz and 200 MHz and should be kept within that range." L6142-43: overclock "can be pushed to 350 MHz using the 'VCO / 1' mode." No "300 MHz specified maximum" exists anywhere in the doc. | `faithful` | Highest-risk hunk. The removed "300 MHz max" was a **fabrication** (contradicted source: real overclock ceiling is 350 MHz, real designed range tops at 200 MHz). New 100–200 MHz range is verbatim-sourced. |
| `opus-master/front-matter.md` title (line 23) | "…by Frequency, **Period**, and RC Timing…" → "…by Frequency, **Rotation**, and RC Timing…" | P2AN004.md body: three recipes are R1 RC-Decay (`P_HIGH_TICKS`), R2 Light-to-Frequency (`P_COUNTER_TICKS`+`P_COUNTER_PERIODS`), **R3 Quadrature-Knob (`P_QUADRATURE`)**. No period-measurement instrument exists. L7/L31: "decode a rotation… a signed count." | `faithful` | Title now names the three actual techniques. "Period" named an instrument the note never builds; "Rotation" (R3 quadrature encoder) is what recipe #2 in the title slot actually measures. |

---

## Flags

**None.**

Each hunk was tested adversarially against the specific failure mode the task called out:

- **≈600 ns filter figure — CONFIRMED, not invented.** The Silicon Doc's own reset-defaults table gives filt1 = 600 ns explicitly, with the arithmetic shown (6.25 ns × 3 flipflops × 32 clocks/sample). `P_FILT1_AB` → FILT1 is confirmed in Spin2 v55 L1451. FILT1 is genuinely "global" (Silicon Doc: "four global digital filter settings which can be used by each smart pin"). The change also correctly **removed** a wrong number: "two-clock" described FILT0's 12.5 ns profile, so leaving it would have mislabeled the filter the code actually selects.

- **PLL-VCO 100–200 MHz range — CONFIRMED verbatim.** Silicon Doc L6233 states the designed range word-for-word. The prior "300 MHz specified maximum" is the fabrication: it appears in **no** source, and it contradicts the two real numbers the doc does give (designed ceiling 200 MHz; overclock ceiling 350 MHz). This is the strongest of the three corrections — it deletes an invented headline spec.
  - *Minor, non-blocking:* "sit comfortably within spec" is slightly loose, since 200 MHz sysclock sits at the **top edge** of the designed VCO range rather than mid-band. This is rhetorical framing, not a sourced-number error, and does not rise to a flag.

- **Title "Rotation" vs "Period" — CONFIRMED against body.** The note builds exactly three instruments; the second is a quadrature encoder (P_QUADRATURE, R3) that produces a signed rotation count, and there is no period-measuring recipe. The old title's "Period" was a genuine title/content mismatch; "Rotation" resolves it. (Note: the KB YAML filename still reads `...frequency-period-pulse-measurement.yaml` — that is a separate artifact's naming, out of this diff's scope, and does not affect the title's fidelity to the body. Worth a glance in a future YAML pass but not a changeset defect here.)

---

## Bottom-line recommendation

**Accept all three hunks.** This changeset is a model of a well-grounded correction sweep: three surgical edits, each deleting a disprovable defect and substituting a claim traceable to a specific Tier-1 line (Silicon Doc L6233 / part3-pages-37-38 filter table / Spin2 v55 L1451 / the note's own recipe list). The two "suspicious specific numbers" the audit was told to distrust — ≈600 ns and the 100–200 MHz range — both check out verbatim against the Silicon Doc; the number that was actually fabricated ("300 MHz specified maximum") is the one this commit **removed**. No scope-creep, no overstatement, no unsourced additions. Proportionate and correct.
