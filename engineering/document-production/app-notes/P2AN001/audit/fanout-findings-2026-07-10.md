# Fan-Out Fabrication-Audit Findings — App Note P2AN001

**Slug:** P2AN001 · **Spec:** fan-out v1.1.0 · **Generated:** 2026-07-10 (plan §5 / task #177)  
**Claims extracted:** 78 · **Survivors:** 6 · **Rejected by verify:** 4

> Candidate findings — each survived an independent adversarial refute pass. **Pending human hand-check + class-wide sweep.** Not yet applied to the document.

> ## ⛔ S1 · S2 · S3 ARE WRONG — DO NOT RE-DERIVE FROM THEM (2026-08-16)
>
> The three `adc-pin-power-group-size` rows below (S1, S2, S3) inverted a **correct** fact. They
> claim the P2's I/O power domains are "8 groups of EIGHT"; the silicon's domains are **16 groups
> of FOUR** (P0-3, P4-7, … P60-63). The document was **right before** this audit; applying these
> rows is what shipped the error into KB v1.15.0 and into P2AN001 v1.0.2 (commit `f3e702ed`).
> Repaired 2026-08-16 in KB v1.16.3 and in P2AN001 v1.0.4.
>
> **Their "Tier-1 says" column is not Tier 1.** S2 cites our own internal
> `VERIFICATION-OPPORTUNITIES.md` note (no source of its own — since corrected); S1 and S3 cite the
> Silicon Doc's `{x}_{y}` **placeholder** pin-description text, which states no number, and read
> that silence as "eight". The actual authority is the package **pinout figure** seven pages
> earlier (v35 Part 1 p.9 — sixteen `VIO_0_3 … VIO_60_63` pins, each centred in the four it names,
> closing the TQFP-100 count at exactly 100) plus the P2 datasheet's *"powered in groups of 4 via
> VIO pins."*
>
> **Both numbers exist and only one is silicon.** P2 Edge modules do group headers in eights — one
> board LDO feeds **two** silicon domains. Board-level "8-pin group" statements are correct where
> they appear and must never be swept.
>
> Full grounding, blast radius and remediation: **F-269** in
> `engineering/operations/P2KB-CORRECTION-FINDINGS.md`. Everything else in this file stands.

## Survivors (confirmed/refine)

| Location | Kind | Verdict | Conf | Class | Claim | Tier-1 says | Correct statement |
|----------|------|---------|------|-------|-------|-------------|-------------------|
| P2AN001.md §How It Works (in brief), | scope | misaligned | high | adc-pin-power-group-size | the P2 powers its I/O pins in isolated groups of four, and a pin's ADC | The P2's 64 I/O pins are powered in 8 isolated groups of EIGHT (P0-7,  | the P2 powers its I/O pins in isolated groups of eight (P0-7, P8-15, . |
| P2AN001.md §Recipe 2, line 247 | scope | misaligned | high | adc-pin-power-group-size | Those four are one complete 4-pin power group (32–35), so the three me | Pins 32-35 are only HALF of a power group; the real group is the 8 pin | Those four pins all sit inside power group P32-39 (an 8-pin group), so |
| P2AN001.md §Pitfalls & Notes, line 6 | scope | misaligned | high | pin-power-group-size | The P2 powers its I/O pins in isolated groups of four — pins 0–3, 4–7, | P2 I/O pins are powered/grounded in groups of EIGHT (P0-7, P8-15, … P5 | The P2 powers its I/O pins in isolated groups of EIGHT — pins 0–7, 8–1 |
| P2AN001.md §See It Work / Verify, li | behavior | misaligned | medium | muldiv64-unsigned-signed | Below the ground reference the reading goes negative; above the supply | MULDIV64 is an UNSIGNED operation. A negative (pinRef − gioRef) is pas | The base build and Recipes 1/2/4/5 compute the ratio with the UNSIGNED |
| P2AN001.md §Pitfalls & Notes (Tip —  | internal-contradiction | misaligned | medium | sinc2-sampling-vs-filter | In SINC2 sampling mode the period is 2^X[3:0] and cannot be freely dit | The power-of-two restriction belongs to SINC2 SAMPLING mode (%00). The | These builds use SINC2 *filtering* mode, in which the period is NOT re |
| P2AN001.md §Pitfalls & Notes (legal  | capability | unverifiable | low | clock-spec-unverified | The P2's specified maximum is 300 MHz ... The ADC works at any clock f | The full Silicon Doc does not state a '300 MHz specified maximum' syst | Cite the actual P2 datasheet clock rating for the 'specified maximum'  |

### Full detail per survivor

**S1. P2AN001.md §How It Works (in brief), line 47** — `misaligned`/high · class `adc-pin-power-group-size-four-vs-eight`  
- Claim: the P2 powers its I/O pins in isolated groups of four, and a pin's ADC measures the VIO/GIO of its own group  
- Anchor: "the P2 powers its I/O pins in isolated groups of four, and a pin's ADC measures the VIO/GIO"  
- Tier-1 (Silicon Doc p2-documentation.txt L511-517 (VIO_{x}_{y}/GIO_{x}_{y} = 'Power/Ground for smart pins {x} through {y}'); har): The P2's 64 I/O pins are powered in 8 isolated groups of EIGHT (P0-7, P8-15, ... P56-63); each group has its own VIO/GIO reference pair. The number is eight, not four.  
- Correct: the P2 powers its I/O pins in isolated groups of eight (P0-7, P8-15, ... P56-63), and a pin's ADC measures the VIO/GIO of its own group  
- Verify: I independently pulled the FULL silicon doc and hardware-verification ledger — I did not trust the finder's cite.  (1) Silicon Doc p2-documentation.txt L511-517: the power/reference pins are named `VIO_{x}_{y}` (3.3V) and `GIO_{x}_{y}` (0V) — the {x}_{y} range notation denotes a   

**S2. P2AN001.md §Recipe 2, line 247** — `misaligned`/high · class `adc-pin-power-group-size-four-vs-eight`  
- Claim: Those four are one complete 4-pin power group (32–35), so the three measurement pins share a single VIO/GIO reference domain  
- Anchor: "Those four are one complete 4-pin power group (32–35), so the three measurement pins share a single VIO/GIO reference domain"  
- Tier-1 (hardware-verification VERIFICATION-OPPORTUNITIES.md:57 ('8 groups of 8 (P0-7, P8-15, ...)'); edge-module-breakout-compat): Pins 32-35 are only HALF of a power group; the real group is the 8 pins P32-39, sharing one VIO/GIO pair. There is no '4-pin power group'.  
- Correct: Those four pins all sit inside power group P32-39 (an 8-pin group), so the three measurement pins share a single VIO/GIO reference domain  
- Verify: Independently re-fetched Tier 1 (not finder's summary). Hardware-verification VERIFICATION-OPPORTUNITIES.md:57-60 states verbatim: "VIO/GIO are PER-GROUP, not global. The 64 pins are 8 groups of 8 (P0-7, P8-15, … P56-63); each group has its own VIO_{x}_{y} (3.3 V) and GIO_{x}_{y}  

**S3. P2AN001.md §Pitfalls & Notes, line 632** — `misaligned`/high · class `pin-power-group-size`  
- Claim: The P2 powers its I/O pins in isolated groups of four — pins 0–3, 4–7, …, 60–63 — and each group shares one VIO/GIO supply pair.  
- Anchor: "The P2 powers its I/O pins in **isolated groups of four** — pins 0–3, 4–7, …, 60–63"  
- Tier-1 (Silicon Doc p2-documentation.txt L511-517/L533-534 (VIO_{x}_{y}='Power for smart pins {x} through {y}', GIO_{x}_{y}='Gro): P2 I/O pins are powered/grounded in groups of EIGHT (P0-7, P8-15, … P56-63), each 8-pin group sharing one VIO/GIO pair; pin groups are addressed in 8-pin increments.  
- Correct: The P2 powers its I/O pins in isolated groups of EIGHT — pins 0–7, 8–15, …, 56–63 — and each 8-pin group shares one VIO/GIO supply pair. (Pins 32–35 used here sit within the single group 32–39, so they do share a reference domain — the advice holds, but the group is eight pins, not four.)  
- Verify: Re-fetched FULL silicon doc myself. p2-documentation.txt L511-534: VIO_{x}_{y}='Power for smart pins {x} through {y}', GIO_{x}_{y}='Ground for smart pins {x} through {y} and other related circuits' (generic range; size not stated at this line). p2-documentation.txt L3606 and part  

**S4. P2AN001.md §See It Work / Verify, line 615** — `misaligned`/medium · class `muldiv64-unsigned-signedness`  
- Claim: Below the ground reference the reading goes negative; above the supply reference it exceeds full scale. All four behaviors are correct.  
- Anchor: "Below the ground reference the reading goes negative; above the supply reference it exceeds full scale. All four behaviors are correct."  
- Tier-1 (Spin2 v55 reference L566: 'MULDIV64(mult1,mult2,divisor) : quotient \| ... return quotient (unsigned operation).'; CSV r): MULDIV64 is an UNSIGNED operation. A negative (pinRef − gioRef) is passed as a ~2^32 unsigned value, so the quotient is a huge positive number, not a negative reading.  
- Correct: The base build and Recipes 1/2/4/5 compute the ratio with the UNSIGNED muldiv64, so a pin driven below the ground reference does NOT read negative — the subtraction wraps and the result pegs off-scale-high/garbage. Only Recipe 3 (which uses ABS + `if_c neg` around a CORDIC QFRAC) actually produces a signed, negative reading below ground.  
- Verify: I re-fetched Tier 1 myself, not the finder's cite.  SPIN2 v55 reference (spin2-v55-text.txt L566), exact text: "MULDIV64(mult1,mult2,divisor) : quotient \| Divide the 64-bit product of 'mult1' and 'mult2' by 'divisor', return quotient (unsigned operation)." => MULDIV64 is explici  

**S5. P2AN001.md §Pitfalls & Notes (Tip — sample period), line 634** — `misaligned`/medium · class `sinc2-sampling-vs-filtering-period`  
- Claim: In SINC2 sampling mode the period is 2^X[3:0] and cannot be freely dithered. ... if you change it, keep it a power of two.  
- Anchor: "In SINC2 sampling mode the period is `2^X[3:0]` and cannot be freely dithered."  
- Tier-1 (Silicon Doc part4-smart-pins.txt L816 (period=POWER(2,X[3:0])), L919-921 ('SINC2 sampling ... only works at power-of-2 s): The power-of-two restriction belongs to SINC2 SAMPLING mode (%00). The builds here use SINC2 FILTERING mode (X=%01_0111, X[5:4]=01), which specifically ALLOWS non-power-of-2 periods via a WYPIN override — that is the reason the filtering mode exists.  
- Correct: These builds use SINC2 *filtering* mode, in which the period is NOT restricted to a power of two — WYPIN can set an arbitrary period (up to ~11,585 clocks). The 128-clock power-of-two period is just the convenient default from X[3:0]; it can be changed to any value.  
- Verify: Full Silicon Doc part4-smart-pins.txt, independently re-fetched, contradicts the tip. L820-821: X[5:4]=%00 is SINC2 Sampling, %01 is SINC2 Filtering. L915-921 (SINC2 Sampling Mode, %00): "The limitation of this mode is that it only works at power-of-2 sample periods... There is a  

**S6. P2AN001.md §Pitfalls & Notes (legal clock), line 636** — `unverifiable`/low · class `clock-spec-unverified`  
- Claim: The P2's specified maximum is 300 MHz ... The ADC works at any clock from about 10 MHz up.  
- Anchor: "The P2's specified maximum is 300 MHz; the original research code ran at 320 MHz, which is over spec."  
- Tier-1 (Silicon Doc p2-documentation.txt — no stated max system-clock spec found (grep '300 mhz\|180 mhz\|maximum clock\|specifi): The full Silicon Doc does not state a '300 MHz specified maximum' system clock, nor a '~10 MHz ADC minimum'. The 10-20 MHz figure in the doc is the supported crystal range, unrelated to the ADC minimum clock.  
- Correct: Cite the actual P2 datasheet clock rating for the 'specified maximum' (commonly cited as lower than 300 MHz for guaranteed operation) rather than an unsourced 300 MHz; and source the '~10 MHz up' ADC lower bound, which is not in the Silicon Doc.  
- Verify: Independently re-pulled the FULL silicon doc and the in-repo P2 datasheet (finder only checked the silicon doc). SILICON DOC (p2-documentation.txt): L6102-6103 "The VCO frequency should be kept within 100 MHz to 200 Mhz."; L6143-6144 "For fastest overclocking, the PLL can be push  

## Rejected by adversarial verify

- **front-matter.md §What You'll Build box, line 45** (unverifiable/low): Independently re-fetched FULL silicon doc /engineering/ingestion/sources/silicon-doc/part4-smart-pins.txt. Confirmed sigma-delta ADC is native to the P2 smart pin on a single pin (
- **P2AN001.md §How It Works (in brief), line 49** (unverifiable/low): TIER 1 (silicon doc) — I re-fetched the full SINC2 section, p2-documentation.txt L8429-8464 (mirror: part4-smart-pins.txt L873-889). It literally says: "SINC2 filtering works by su
- **P2AN001.md §References, item 1, line 654** (misaligned/low): Independently re-fetched Silicon Doc part4-smart-pins.txt (NOT the summary). The smart-pin %-mode listing L134-137: "11000 = ADC sample/filter/capture, internally clocked / 11001 =
- **P2AN001.md §Pitfalls & Notes, line 628** (unverifiable/low): Independently grepped the FULL silicon doc set myself (not the summary): p2-documentation.txt + all part*.txt including part4-smart-pins.txt, for resist\|ohm\|impedance\|500\|input
