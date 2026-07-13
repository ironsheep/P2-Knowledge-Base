# Fan-Out Fabrication-Audit Findings — App Note P2AN004

**Slug:** P2AN004 · **Spec:** fan-out v1.1.0 · **Generated:** 2026-07-10 (plan §5 / task #177)  
**Claims extracted:** 39 · **Survivors:** 3 · **Rejected by verify:** 0

> Candidate findings — each survived an independent adversarial refute pass. **Pending human hand-check + class-wide sweep.** Not yet applied to the document.

## Survivors (confirmed/refine)

| Location | Kind | Verdict | Conf | Class | Claim | Tier-1 says | Correct statement |
|----------|------|---------|------|-------|-------|-------------|-------------------|
| P2AN004.md §Recipe R3, Hardware call | behavior | misaligned | high | filter-length-mismatch | If a turned knob jumps or counts backward, add `P_FILT1_AB` to the mod | P_FILT1_AB selects the global FILT1 setting, whose reset default is le | add `P_FILT1_AB` to select the global FILT1 filter setting (reset defa |
| P2AN004.md §Pitfalls & Notes, 'stay  | capability | misaligned | medium | clock-spec-max-overstate | These programs run at 200 MHz. The P2's specified maximum is 300 MHz;  | The silicon doc gives no '300 MHz specified maximum'. It states the VC | Rephrase to match a citable spec: the P2's PLL VCO is designed for 100 |
| front-matter.md §title vs What-You'l | internal-contradiction | misaligned | low | title-recipe-technique-m | Title: "...by Frequency, Period, and RC Timing on a P2 Pin" naming thr | Quadrature encoder mode counts A/B phase steps (position/count), which | Title's three named techniques should match the three recipes: Frequen |

### Full detail per survivor

**S1. front-matter.md §title vs What-You'll-Build box, line 23 (vs lines 25, 54-56)** — `misaligned`/low · class `title-recipe-technique-mismatch`  
- Claim: Title: "...by Frequency, Period, and RC Timing on a P2 Pin" naming three techniques (Frequency, Period, RC Timing), while the box lists three recipes R1 RC-decay, R2 light-to-frequency, R3 quadrature-knob.  
- Anchor: "Read Real-World Sensors by Frequency, Period, and RC Timing on a P2 Pin"  
- Tier-1 (Silicon Doc part4-smart-pins.txt: %01011 A/B quadrature encoder (line 531); time-measurement %10000/%10001 (lines 649,66): Quadrature encoder mode counts A/B phase steps (position/count), which is neither frequency nor period measurement; there is no recipe on this cover corresponding to the title's "Period" technique.  
- Correct: Title's three named techniques should match the three recipes: Frequency (R2), RC Timing (R1), and quadrature/position (R3) — 'Period' names no recipe and the quadrature reader is unnamed in the title.  
- Verify: Full silicon doc part4-smart-pins.txt, independently re-fetched: line 531 "%01011 = A/B-input quadrature encoder"; line 537 "32-bit quadrature step count can always be read via RDPIN/RQPIN" (a signed position/COUNT, not a period or frequency). Line 669 "%10001 = Time A-input high  

**S2. P2AN004.md §Recipe R3, Hardware callout, line 304** — `misaligned`/high · class `filter-length-mismatch`  
- Claim: If a turned knob jumps or counts backward, add `P_FILT1_AB` to the mode for two-clock input filtering  
- Anchor: "add `P_FILT1_AB` to the mode for two-clock input filtering"  
- Tier-1 (Silicon Doc part3-pages-37-38.txt lines 25,52-58: filter length 2/3/5/8 flipflops selected by 0..3; reset defaults filt0): P_FILT1_AB selects the global FILT1 setting, whose reset default is length 1 (3 flipflops), tap 5, ~600 ns low-pass time. The ~2-clock (12.5 ns, 2-flipflop, tap-0) profile is the reset default of FILT0 (P_FILT0_AB), not FILT1.  
- Correct: add `P_FILT1_AB` to select the global FILT1 filter setting (reset default: 3-flipflop, tap-5, ~600 ns low-pass) for the A/B inputs; for a minimal ~2-clock filter use `P_FILT0_AB` (reset default 2-flipflop, tap 0). Filter lengths/taps are globally reconfigurable via HUBSET.  
- Verify: spin2-v55-text.txt line 1451: "\| %0000_0000_101_..._0 \| P_FILT1_AB \| Select FILT1 settings for A, B" — confirms P_FILT1_AB selects the global FILT1 setting (not FILT0). Silicon Doc part3-pages-37-38.txt, reset-default table: line 25 "The filter length is 2, 3, 5, or 8 flipflop  

**S3. P2AN004.md §Pitfalls & Notes, 'stay at a legal clock', line 336** — `misaligned`/medium · class `clock-spec-max-overstated`  
- Claim: These programs run at 200 MHz. The P2's specified maximum is 300 MHz; there is no reason to overclock for any of these measurements  
- Anchor: "The P2's specified maximum is 300 MHz; there is no reason to overclock"  
- Tier-1 (Silicon Doc p2-documentation.txt line 6143 ('the PLL can be pushed to 350 MHz using the VCO/1 mode') and line 6233 ('The): The silicon doc gives no '300 MHz specified maximum'. It states the VCO is designed for 100-200 MHz (so ~200 MHz is the intended sysclock ceiling) and that overclocking can push the PLL to 350 MHz. 300 MHz falls in overclock territory, not a specified maximum.  
- Correct: Rephrase to match a citable spec: the P2's PLL VCO is designed for 100-200 MHz (≈200 MHz nominal sysclock), and can be overclocked well beyond; 200 MHz is comfortably within spec for these measurements. Drop the unsupported '300 MHz specified maximum' figure or cite the Parallax datasheet's actual rated figure.  
- Verify: Independently re-fetched Tier 1. Parallax P2 datasheet (p2-datasheet-narrative.txt:6450, authoritative): "Nominal PLL frequency (system clock speed) is 180 MHz at up to 105 °C." P2 spec sheet (p2-spec-sheet-narrative.txt:43): "Frequency 180 MHz typical, 320 MHz extended." Silicon  
