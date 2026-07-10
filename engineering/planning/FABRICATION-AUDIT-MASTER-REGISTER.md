# Fabrication-Audit Fan-Out — MASTER REGISTER (Batch 1: narrative core)

**Sprint:** Fabrication Audit & Correctness Sweep — plan §5 fan-out (task #177)  
**Spec:** FABRICATION-AUDIT-FAN-OUT-SPEC.md v1.1.0  
**Batch 1 docs:** 12 (Getting Started, Streamer, Architect, DeSilva, Debug Window, Assembly front-matter, P2AN001–006)  
**Generated:** 2026-07-10 (Batch 2 = IOSP, pending)

> Candidate findings: each survived an independent adversarial refute-verify. **Still pending human hand-check + class-wide sweep** (§6/§7). Per-doc detail in each doc's `audit/fanout-findings-2026-07-10.md`.

## Cross-doc scorecard

| Doc | Claims | Raw | Survivors | Rejected |
|-----|-------:|----:|----------:|---------:|
| Getting Started | 95 | 6 | 4 | 2 |
| Streamer Guide | 323 | 10 | 8 | 2 |
| Architect's Guide | 125 | 6 | 1 | 5 |
| DeSilva PASM Tutorial | 648 | 70 | 63 | 7 |
| Debug Window Manual | 939 | 123 | 97 | 26 |
| Assembly (front-matter only) | 32 | 2 | 1 | 1 |
| App Note P2AN001 | 78 | 10 | 6 | 4 |
| App Note P2AN002 | 70 | 6 | 4 | 2 |
| App Note P2AN003 | 92 | 3 | 1 | 2 |
| App Note P2AN004 | 39 | 3 | 3 | 0 |
| App Note P2AN005 | 69 | 1 | 1 | 0 |
| App Note P2AN006 | 49 | 0 | 0 | 0 |
| **TOTAL** | **2559** | | **189** | **51** |

## Survivor breakdown
- By verdict: {'unverifiable': 45, 'misaligned': 143, 'fabricated': 1}
- By confidence: {'low': 84, 'high': 35, 'medium': 70}

## Recurring defect classes (survivors, ≥2)

| n | defect_class |
|--:|--------------|
| 6 | cycle-count-vs-instruction-count |
| 4 | hub-loop-cycle-understatement |
| 4 | packing-signedness-misattribution |
| 3 | invented-default-value |
| 3 | color-format-rgb24-vs-named |
| 3 | debug-window-range-mismatch |
| 2 | false-chapter-backreference |
| 2 | color-name-green-vs-lime |
| 2 | term-default-pair3-color |
| 2 | luma-hsv-x-variant-mischaracterized |
| 2 | save-missing-filename-arg |
| 2 | default-value-mismatch |
| 2 | alt-modifier-semantics-wrong |
| 2 | adc-pin-power-group-size-four-vs-eight |
| 2 | cordic-precision-bits-unsourced |

## Priority set — HIGH-confidence fabricated/misaligned (hand-check first)

| Doc | Location | Verdict | Class | Claim |
|-----|----------|---------|-------|-------|
| p2-getting-started-guide | getting-started-body.md Ch3 §"Shar | misaligned | false-chapter-backreferenc | the P2 gives you **locks** (the 16 hardware locks from Chapter 1) to g |
| p2-streamer-programming-guide | Appendix D §"Corrupted Data from R | misaligned | fifo-wrap-address-alignmen | Buffer address aligned to 64-byte boundary for wrap mode |
| p2-pasm-desilva-style | Ch2 §Your Turn Experiment 2 'Paral | misaligned | ptrb-not-a-user-parameter | rdlong delay, ptrb reads a per-cog 'delay' parameter passed to the cog |
| p2-pasm-desilva-style | COMPLETE-OPUS-MASTER.md, Ch.4 Comm | misaligned | hub-immediate-bit-width | A bare #address only encodes 9 bits ... Always use ## for hub addresse |
| p2-pasm-desilva-style | COMPLETE-OPUS-MASTER.md Ch5 Common | misaligned | mul-16x16-mischaracterized | MUL gives only low 32 bits; for the full 64-bit result you must use QM |
| p2-pasm-desilva-style | opus-master/COMPLETE-OPUS-MASTER.m | misaligned | cordic-per-cog-fabrication | Each cog has its own CORDIC, but starting a new operation before retri |
| p2-pasm-desilva-style | opus-master/COMPLETE-OPUS-MASTER.m | misaligned | cordic-overwrite-vs-pipeli | starting a new operation before retrieving your result overwrites it! |
| p2-pasm-desilva-style | Ch.8 §Reading Multiple Pins area,  | misaligned | testp-flag-polarity-invert | if_z jmp #sensor_low ' Jump if pin low (Z=1 when pin=0)  /  if_nz jmp  |
| p2-pasm-desilva-style | Ch.8 §Timing Is Everything, line 2 | misaligned | sequential-instructions-cl | When you execute drvh #56 then drvl #57, 'Pin 56 goes high and pin 57  |
| p2-pasm-desilva-style | COMPLETE-OPUS-MASTER.md Ch.10 'Lon | misaligned | address-width-32-vs-20-bit | jmp #\far_away — '\ forces a 32-bit absolute address' |
| p2-pasm-desilva-style | COMPLETE-OPUS-MASTER.md Ch.10 'Per | misaligned | alignl-8byte-vs-4byte-long | 'Align branch targets to 8-byte boundaries' followed by 'alignl ' Alig |
| p2-pasm-desilva-style | Chapter 12 §The Hook, COMPLETE-OPU | misaligned | hub-loop-cycle-understatem | Before optimization: 13 clocks (for the rdlong/add/wrlong/add/djnz loo |
| p2-pasm-desilva-style | Chapter 12 §The Hook, COMPLETE-OPU | misaligned | cycle-count-vs-instruction | Almost twice as fast! (the 'after optimization' loop that merged the p |
| p2-pasm-desilva-style | Chapter 12 §Hub Access Optimizatio | misaligned | hub-alignment-timing-fabri | Non-long-aligned hub access is slower and long-aligned access is faste |
| p2-pasm-desilva-style | Chapter 12 §The FIFO Fast Path, CO | misaligned | hub-loop-cycle-understatem | Traditional hub reading (rdlong ptra++ / add / djnz loop): ~6 clocks a |
| p2-pasm-desilva-style | Chapter 12 §Real-World Example Fas | misaligned | hub-loop-cycle-understatem | copy_better (rdlong ptra++ / wrlong ptrb++ / djnz) runs ~8 clocks per  |
| p2-pasm-desilva-style | COMPLETE-OPUS-MASTER.md Ch.12 'Unr | misaligned | ptr-expression-scope-overg | ptra++ only works with hub-access instructions like RDLONG. |
| p2-pasm-desilva-style | COMPLETE-OPUS-MASTER.md Ch.13 'Com | misaligned | cog-ram-address-range-erro | In 'mov value, $200', $200 is a cog RAM address (so it reads cog RAM,  |
| p2-pasm-desilva-style | COMPLETE-OPUS-MASTER.md §Ch13 'Wha | misaligned | cycle-count-wrong | 3-clock deterministic access via RDLUT / WRLUT |
| p2-pasm-desilva-style | §'ATN - Inter-Cog Events', COMPLET | misaligned | cogatn-mask-width | The COGATN instruction takes an 8-bit mask where each bit corresponds  |
| p2-debug-window-manual | ch02-getting-started.md §The no-ha | misaligned | random-operator-single-vs- | the random-number generator — `GETRND` (or the `?` operator) for noise |
| p2-debug-window-manual | ch03-term.md §A positioned dashboa | misaligned | term-default-pair3-color | Selecting color pair 3 (code 7) in this example gives red 'HIGH' text. |
| p2-debug-window-manual | ch05-plot.md §The update model / P | misaligned | precise-default-inverted | the window keeps sub-pixel precision (1/256 of a pixel) by default; PR |
| p2-debug-window-manual | ch06-logic.md §Creating a LOGIC wi | misaligned | worked-example-bit-mapping | a sample value of %1011 lights channel 0 (CLK) high, channel 1 (DATA)  |
| p2-debug-window-manual | ch06-logic.md config-keyword table | misaligned | logic-keyword-defaults-cop | LINESIZE default 3, range 1–32 |
| p2-debug-window-manual | ch08-scope-xy.md §Creating a SCOPE | misaligned | dotsize-pixels-vs-half-pix | DOTSIZE argument is in pixels and sets the dot diameter, range 2-20 (s |
| p2-debug-window-manual | ch13-packed-data.md §The ALT and S | misaligned | alt-modifier-semantics-wro | ALT — the host swaps adjacent same-width fields throughout the element |
| p2-debug-window-manual | ch13-packed-data.md §Consideration | misaligned | alt-modifier-semantics-wro | Use ALT only to swap adjacent same-width fields throughout the element |
| p2-debug-window-manual | appendix-b-packed-data.md § Modifi | misaligned | alt-modifier-reversal-misc | ALT: swap adjacent same-width fields ... not a reversal |
| p2-debug-window-manual | appendix-b-packed-data.md § Modifi | misaligned | alt-modifier-scope-oversta | ALT: swap ... fields throughout the container |
| P2AN001 | P2AN001.md §How It Works (in brief | misaligned | adc-pin-power-group-size-f | the P2 powers its I/O pins in isolated groups of four, and a pin's ADC |
| P2AN001 | P2AN001.md §Recipe 2, line 247 | misaligned | adc-pin-power-group-size-f | Those four are one complete 4-pin power group (32–35), so the three me |
| P2AN001 | P2AN001.md §Pitfalls & Notes, line | misaligned | pin-power-group-size | The P2 powers its I/O pins in isolated groups of four — pins 0–3, 4–7, |
| P2AN004 | P2AN004.md §Recipe R3, Hardware ca | misaligned | filter-length-mismatch | If a turned knob jumps or counts backward, add `P_FILT1_AB` to the mod |
| P2AN005 | P2AN005.md §Adapt It / Going Furth | misaligned | false-negative-capability- | which would need a hardware mutex the P2 doesn't have |
