# Fan-Out Fabrication-Audit Findings — App Note P2AN003

**Slug:** P2AN003 · **Spec:** fan-out v1.1.0 · **Generated:** 2026-07-10 (plan §5 / task #177)  
**Claims extracted:** 92 · **Survivors:** 1 · **Rejected by verify:** 2

> Candidate findings — each survived an independent adversarial refute pass. **Pending human hand-check + class-wide sweep.** Not yet applied to the document.

## Survivors (confirmed/refine)

| Location | Kind | Verdict | Conf | Class | Claim | Tier-1 says | Correct statement |
|----------|------|---------|------|-------|-------|-------------|-------------------|
| P2AN003.md §Pitfalls & Notes, 'Tip — | internal-contradiction | misaligned | medium | pwm-dither-tone-fixed-no | Raising the period lowers the sample rate (and the dither frequency) | For PWM dither the spectral tone is fixed at Fclock/256 because the PW | Raising the period lowers the sample rate; the PWM dither tone stays f |

### Full detail per survivor

**S1. P2AN003.md §Pitfalls & Notes, 'Tip — the sample rate is your headroom', line 549** — `misaligned`/medium · class `pwm-dither-tone-fixed-not-period-scaled`  
- Claim: Raising the period lowers the sample rate (and the dither frequency)  
- Anchor: "Raising the period lowers the sample rate (and the dither frequency); lowering it is bounded by 256"  
- Tier-1 (silicon-doc/part4-smart-pins.txt line 290-302 (%00011 PWM dither): sample period must be a multiple of 256; 'a maximum o): For PWM dither the spectral tone is fixed at Fclock/256 because the PWM completes its dither pattern every 256 clocks; this does NOT depend on the sample period. Raising the sample period lowers only the sample rate (Fclock/period), not the dither tone frequency.  
- Correct: Raising the period lowers the sample rate; the PWM dither tone stays fixed at sysclock/256 regardless of the period.  
- Verify: Independently re-fetched silicon-doc/part4-smart-pins.txt lines 290-302 (%00011 PWM dither): "X[15:0] establishes the sample period in clock cycles. The sample period must be a multiple of 256 (X[7:0]=0), so that an integral number of 256 steps are afforded the PWM, which dithers  

## Rejected by adversarial verify

- **Recipe 4 — "How this works", line 357 (sibling claim in code comment line 342)** (unverifiable/low): Re-fetched FULL silicon doc engineering/ingestion/sources/silicon-doc/part4-smart-pins.txt. Two Tier-1 facts adjudicate this: (1) Lines 862-864: "The smart pin accumulators are 27 
- **How It Works — "The two dither modes", line 52** (misaligned/low): Re-fetched FULL silicon doc part4-smart-pins.txt (independently, not the finder's cite). Line 111 mode table: "00001 = DAC noise (M[12:10] = %101)". Lines 235-238: "%00001 and DAC_
