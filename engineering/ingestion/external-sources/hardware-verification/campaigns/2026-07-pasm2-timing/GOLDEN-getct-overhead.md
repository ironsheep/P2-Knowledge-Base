# Golden analysis — GETCT bracket measurement overhead (EF-035)

**Test:** `getct-overhead-char.spin2` (cog-resident, 2-clock-exact PASM).
**Run:** 2026-07-11, real P2 (Stephen), `pnut-ts -d`, debug-log readback.

## Golden result
```
d_ctrl = 2, d_10 = 22, d_20 = 42
```

## Interpretation
- `d_ctrl` = back-to-back GETCT delta = the bracket overhead = **2 clocks**.
- `d_10` = 10 NOPs (20 clk) bracketed = 20 + 2 = **22**.
- `d_20` = 20 NOPs (40 clk) bracketed = 40 + 2 = **42**.
- Overhead read three independent ways (`d_ctrl`, `d_10`−20, `d_20`−40) → all **2**.
- Slope = (42−22)/(40−20) = 1 clk/clk (linearity = the two-tailed control: the reading
  tracks inserted cycles, so it is not a fixed-value artifact; it would read 4/24/44 under
  the refuted "4-cycle" model).

## Verdict
GETCT bracket overhead = **2 clocks**, CONFIRMED. Pre-sweep "4-cycle" REFUTED.
**Scope:** proves the RESULT (2), not the intra-instruction latch point (start-vs-end
latch both yield 2 for two identical ops) — the manual states the result, not a mechanism.

Raw logs are regenerable from this `.spin2` and are not versioned.
