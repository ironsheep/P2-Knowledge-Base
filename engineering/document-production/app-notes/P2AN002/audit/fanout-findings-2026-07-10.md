# Fan-Out Fabrication-Audit Findings — App Note P2AN002

**Slug:** P2AN002 · **Spec:** fan-out v1.1.0 · **Generated:** 2026-07-10 (plan §5 / task #177)  
**Claims extracted:** 70 · **Survivors:** 4 · **Rejected by verify:** 2

> Candidate findings — each survived an independent adversarial refute pass. **Pending human hand-check + class-wide sweep.** Not yet applied to the document.

## Survivors (confirmed/refine)

| Location | Kind | Verdict | Conf | Class | Claim | Tier-1 says | Correct statement |
|----------|------|---------|------|-------|-------|-------------|-------------------|
| P2AN002.md §Recipe 3 'How this works | example | misaligned | low | constant-overflow-misatt | "...STEPS equal steps are 2^32 / STEPS apart. That value would overflo | The step VALUE (2^32/STEPS = 2^26 for STEPS=64) is only 27 bits and fi | The quotient itself fits fine; the reason for the workaround is that t |
| P2AN002.md §Going Further + Resource | capability | misaligned | low | obex-author-attribution | "...a complete open library (SaucySoliton's FFT/IFFT, OBEX #5361)..."  | The authoritative OBEX index records OBEX #5361's author as 'James Smi | Attribute OBEX #5361 to the name the OBEX record carries ('James Smith |
| P2AN002.md §See It Work / Verify, li | behavior | unverifiable | low | cordic-precision-bits-un | "The trigonometric operations carry about 28 bits of precision, so a v | The full Silicon Doc and Datasheet describe 'scale-factor correction'  | State the precision only if sourced (e.g. cite an empirical hardware-v |
| P2AN002.md §Pitfalls & Notes, line 3 | behavior | unverifiable | low | cordic-precision-bits-un | "Rotate, vector, sine, log, and exp are computed to roughly 28 bits, w | 'scale-factor correction' is documented (matches 'scale-factor correct | Keep the 'exact for integer ops / approximate for the iterative ops, s |

### Full detail per survivor

**S1. P2AN002.md §Recipe 3 'How this works', line 157** — `misaligned`/low · class `constant-overflow-misattribution`  
- Claim: "...STEPS equal steps are 2^32 / STEPS apart. That value would overflow a 32-bit constant written directly, so it is formed as $8000_0000 / (STEPS / 2)"  
- Anchor: "That value would overflow a 32-bit constant written directly, so it is formed as"  
- Tier-1 (pnut_ts v1.55.0 compile test: `$1_0000_0000 / STEPS` => error 'Constant exceeds 32 bits'; quotient 2^32/64 = $0400_0000 ): The step VALUE (2^32/STEPS = 2^26 for STEPS=64) is only 27 bits and fits a 32-bit constant. What actually overflows is the dividend literal $1_0000_0000 (2^32, 33 bits) if written directly.  
- Correct: The quotient itself fits fine; the reason for the workaround is that the DIVIDEND 2^32 ($1_0000_0000) cannot be written as a 32-bit constant literal, so it is halved to $8000_0000 with STEPS/2.  
- Verify: Independent pnut-ts v1.55.0 compiles (not trusting finder's cite):  (1) `STEPVAL = $1_0000_0000 / STEPS` (STEPS=64):   "The result (4294967296) does not fit in 32 bits"   "/tmp/t_stepval.spin2:3:error:Constant exceeds 32 bits"   -> The offending value is 4294967296 = 2^32 = the D  

**S2. P2AN002.md §See It Work / Verify, line 339** — `unverifiable`/low · class `cordic-precision-bits-unsourced`  
- Claim: "The trigonometric operations carry about 28 bits of precision, so a value you predicted as exactly (0, 100) may read (0, 99) or (1, 100)."  
- Anchor: "The trigonometric operations carry about 28 bits of precision, so a value you predicted"  
- Tier-1 (Silicon Doc v35 p2-documentation.txt line 425 ('32-bit, pipelined CORDIC solver with scale-factor correction') and CORDI): The full Silicon Doc and Datasheet describe 'scale-factor correction' for the CORDIC but state NO specific precision figure. The only numeric scale-factor mentioned (1.646) is for the separate 5-stage color-space CORDIC rotator (line 4779), not the 54-stage solver.  
- Correct: State the precision only if sourced (e.g. cite an empirical hardware-verification finding); otherwise describe qualitatively ('the low few bits may be approximate') without the specific '~28 bits' figure.  
- Verify: I pulled Tier 1 myself, not trusting the finder's cite.  (1) FULL Silicon Doc CORDIC Solver section, p2-documentation.txt lines 7270-7442, read in full. It states: "In the hub, there is a 54-stage pipelined CORDIC solver..." and lists all eight functions (QMUL/QDIV/QSQRT/QROTATE/  

**S3. P2AN002.md §Pitfalls & Notes, line 354** — `unverifiable`/low · class `cordic-precision-bits-unsourced`  
- Claim: "Rotate, vector, sine, log, and exp are computed to roughly 28 bits, with the magnitude scale-factor corrected in hardware."  
- Anchor: "Rotate, vector, sine, log, and exp are computed to roughly 28 bits, with the magnitude"  
- Tier-1 (Silicon Doc v35 line 425 + CORDIC section lines 7270-7442; P2 Datasheet CORDIC pages. Same search as line-339 finding.): 'scale-factor correction' is documented (matches 'scale-factor corrected in hardware' — that half is fine); the '~28 bits' precision figure is NOT stated for the 54-stage solver anywhere in the full Silicon Doc or Datasheet.  
- Correct: Keep the 'exact for integer ops / approximate for the iterative ops, scale-factor corrected in hardware' distinction (all Tier-1-supported), but drop or source the specific '~28 bits' number.  
- Verify: Independently re-pulled full Tier-1 (not the facts summary). Silicon Doc p2-documentation.txt:7271 (== part3-end.txt:335): "In the hub, there is a 54-stage pipelined CORDIC solver that can compute the following functions for all cogs:" — lists 32x32 multiply/64:32 divide/sqrt/rot  

**S4. P2AN002.md §Going Further + Resources, lines 327 and 369** — `misaligned`/low · class `obex-author-attribution`  
- Claim: "...a complete open library (SaucySoliton's FFT/IFFT, OBEX #5361)..." (repeated line 369: 'OBEX #5361 — FFT/IFFT (SaucySoliton)')  
- Anchor: "a complete open library (SaucySoliton's FFT/IFFT, **OBEX #5361**) is also listed in Resources"  
- Tier-1 (p2kb_obex_get '5361' => object_id 5361, title 'FFT IFFT', author 'James Smith'. (Object ID and 'real-input FFT' descript): The authoritative OBEX index records OBEX #5361's author as 'James Smith', not 'SaucySoliton'.  
- Correct: Attribute OBEX #5361 to the name the OBEX record carries ('James Smith'), unless 'SaucySoliton' is confirmed to be that author's forum handle.  
- Verify: Independently re-pulled the authoritative OBEX index (not the finder's cite; this is an OBEX-attribution claim, not a silicon claim, so the OBEX record is Tier 1). p2kb_obex_get "5361" returns: object_id "5361", title "FFT IFFT", author "James Smith", description "Demo Files: rea  

## Rejected by adversarial verify

- **front-matter.md line 45 ("What You'll Build" box intro)** (misaligned/low): Re-fetched FULL silicon doc (not the summary): p2-documentation.txt line 434 — "Cogs can start CORDIC operations every 1/2/4/8/16 (#cogs) clocks and get results 55 clocks later"; l
- **P2AN002.md §The Ceiling — Three-Phase Motor Control, line 317** (unverifiable/low): FULL Tier-1 is genuinely silent on motor-control transforms: `grep -in "park\|clarke\|field.orient\|foc"` on engineering/ingestion/sources/silicon-doc/p2-documentation.txt returned
