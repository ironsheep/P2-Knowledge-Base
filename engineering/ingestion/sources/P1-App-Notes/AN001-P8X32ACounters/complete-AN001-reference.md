# AN001 — Propeller P8X32A Counters (v2.0) — Curated Reference

> **Curated pass-1 extraction.** Platform: **Propeller 1 (P8X32A)** — Spin1 + PASM1. Source: Parallax Semiconductor Application Note **AN001**, *Propeller P8X32A Counters*, **v2.0**, © 2011 Parallax, Inc. dba Parallax Semiconductor. 19 pages.
> This reference preserves the app note's **section structure, teaching order, and authorial voice** (a downstream pass studies it to build a P2 app-note style/voice guide). Raw layout extract: `AN001-P8X32ACounters-text.txt`. Code: `assets/code-2026-06-27/`. Images: `assets/images-AN001-P8X32ACounters-2026-06-27/`.

---

## Document identity & front matter

- **Title:** Propeller P8X32A Counters (v1.0 title was "Propeller Counters"; renamed in v2.0).
- **Type:** Application Note AN001, Parallax Semiconductor.
- **Abstract (verbatim voice):** "Each of the multicore P8X32A's eight processors (cogs) has two independent hardware counter modules. Each counter is a configurable state machine for sensing or generating repetitive signals, potentially on every clock cycle. Use the counter modules as flexible subsystems that can often take the place of dedicated cogs or peripheral hardware, reducing code complexity and component count in an application."

## Section map (teaching order — preserved)

1. **Introduction** — 16 counters total (2 per cog × 8 cogs), each independent, 32 modes; promises detailed mode coverage + usage examples; Figure 1 = master block diagram.
2. **Counter Registers** — CTRA/FRQA/PHSA (counter A), CTRB/FRQB/PHSB (counter B); field layout; OUT/DIR interaction; reset behavior; the "we'll only discuss Counter A" simplification note.
3. **Counter Operation** — the FRQA→PHSA accumulate-each-true-cycle model; the 80 MHz worked example.
4. **Counter Modes** — the 32-mode master table (Table 2) + application-grouping table (Table 3).
5. **NCO Modes** (`%0010X`) — incl. the PWM-as-NCO subsection.
6. **PLL modes** (`%0000X`).
7. **Duty Cycle modes** (`%0011X`) — incl. DAC.
8. **Logic modes** (`%1XXXX`).
9. **Pin State Detection Modes** (`%01XXX`) — incl. Σ∆-ADC and edge/frequency counting.
10. **Conclusion** — capability roll-up.
11. **Resources** / **Revision History** / disclaimer + copyright.

**Voice characteristics:** second-person practical register ("Use the counter modules as…"), worked numeric examples with real clock values (5 MHz xtal × 16 PLL = 80 MHz recurs throughout), each mode introduced as *what it does → block diagram → code example → oscilloscope figure → governing equation*. Heavy use of concrete application framing ("Servo control, PWM motor control, LED dimming"). Footnotes were "unbound and placed inline" in v2.0. Reassuring/teacherly tone; occasional design-caution asides (e.g. RC-filter placement within 1 inch, "will not work on a breadboard").

---

## Counter Registers (the model)

Each counter has **three** registers. Counter A: **CTRA** (control), **FRQA** (frequency/increment), **PHSA** (phase accumulator). Counter B: CTRB/FRQB/PHSB, operation identical.

- **CTRA/CTRB** sets the **CTRMODE** field (mode), **PLLDIV** (PLL division factor, PLL modes only), and **APIN/BPIN** (the two pins used as I/O per mode).
- **PHSA/PHSB** — "the heart of the counter"; the accumulator holding the current value; readable/writable by a program (writing often unnecessary).
- **FRQA/FRQB** — the value added to the accumulator whenever the **accumulate condition** (set by CTRMODE) is true.
- On cog start, all six registers init to `$0000_0000`; on cog stop, all counter activity ceases and registers reset to `$0000_0000`.

### Table 1 — CTRA/CTRB register bit-field layout

| Bits | 31 | 30..26 | 25..23 | 22..15 | 14..9 | 8..6 | 5..0 |
|------|----|--------|--------|--------|-------|------|------|
| Field | — | CTRMODE | PLLDIV | — | BPIN | — | APIN |

- Fields are arranged to exploit the assembly instructions **MOVS** (sets APIN), **MOVD** (sets BPIN), **MOVI** (sets CTRMODE/PLLDIV).
- BPIN and APIN are 6 bits each; the **highest bit of each (bits 5 and 14) is reserved** and ignored by the P8X32A.
- **Output combining:** a counter's actual pin output (per CTRMODE + APIN/BPIN) is **OR'd** with the corresponding OUTA bit and **AND'd** with the corresponding DIRA bit. Typical operation: OUT bit = 0, DIR bit = 1; they can be set differently to mask the counter output.

### Counter Operation worked example
Counter adds FRQA to PHSA on each clock cycle the accumulate condition is true. At 5 MHz × 16 PLL = 80 MHz, the accumulate happens up to 80 million times/second.

---

## Table 2 — Counter Modes (CTRMODE field values, all 32)

Columns: CTRMODE · Description · Accumulate FRQx→PHSx · APIN Output* · BPIN Output*. (*Must set the corresponding DIR bit to affect the pin.) Notation: `A¹` = APIN delayed 1 clock, `A²` = APIN delayed 2 clocks, `B¹` = BPIN delayed 1 clock.

| CTRMODE | Description | Accumulate | APIN out | BPIN out |
|---------|-------------|------------|----------|----------|
| %00000 | Counter disabled (off) | 0 (never) | 0 (none) | 0 (none) |
| %00001 | PLL internal (video mode) | 1 (always) | 0 | 0 |
| %00010 | PLL single-ended | 1 | PLLx | 0 |
| %00011 | PLL differential | 1 | PLLx | !PLLx |
| %00100 | NCO single-ended | 1 | PHSx[31] | 0 |
| %00101 | NCO differential | 1 | PHSx[31] | !PHSx[31] |
| %00110 | DUTY single-ended | 1 | PHSx-Carry | 0 |
| %00111 | DUTY differential | 1 | PHSx-Carry | !PHSx-Carry |
| %01000 | POS detector | A¹ | 0 | 0 |
| %01001 | POS detector with feedback | A¹ | 0 | !A¹ |
| %01010 | POSEDGE detector | A¹ & !A² | 0 | 0 |
| %01011 | POSEDGE detector w/ feedback | A¹ & !A² | 0 | !A¹ |
| %01100 | NEG detector | !A¹ | 0 | 0 |
| %01101 | NEG detector with feedback | !A¹ | 0 | !A¹ |
| %01110 | NEGEDGE detector | !A¹ & A² | 0 | 0 |
| %01111 | NEGEDGE detector w/ feedback | !A¹ & A² | 0 | !A¹ |
| %10000 | LOGIC never | 0 | 0 | 0 |
| %10001 | LOGIC !A & !B | !A¹ & !B¹ | 0 | 0 |
| %10010 | LOGIC A & !B | A¹ & !B¹ | 0 | 0 |
| %10011 | LOGIC !B | !B¹ | 0 | 0 |
| %10100 | LOGIC !A & B | !A¹ & B¹ | 0 | 0 |
| %10101 | LOGIC !A | !A¹ | 0 | 0 |
| %10110 | LOGIC A <> B | A¹ <> B¹ | 0 | 0 |
| %10111 | LOGIC !A \| !B | !A¹ \| !B¹ | 0 | 0 |
| %11000 | LOGIC A & B | A¹ & B¹ | 0 | 0 |
| %11001 | LOGIC A == B | A¹ == B¹ | 0 | 0 |
| %11010 | LOGIC A | A¹ | 0 | 0 |
| %11011 | LOGIC A \| !B | A¹ \| !B¹ | 0 | 0 |
| %11100 | LOGIC B | B¹ | 0 | 0 |
| %11101 | LOGIC !A \| B | !A¹ \| B¹ | 0 | 0 |
| %11110 | LOGIC A \| B | A¹ \| B¹ | 0 | 0 |
| %11111 | LOGIC always | 1 | 0 | 0 |

### Table 3 — Mode-group application examples
| CTRMODE* | Group | Example applications |
|----------|-------|----------------------|
| %0001X | PLL | RF carrier synthesis, clock generation |
| %0010X | NCO | Servo control, PWM motor control, LED dimming, audio generation |
| %0011X | DUTY | Digital-to-analog conversion, audio generation |
| %01X00 | POS/NEG detector | Pulse width measurement, duty cycle measurement |
| %01X01 | POS/NEG detector w/ feedback | Analog-to-digital conversion |
| %01X1X | POSEDGE/NEGEDGE | Event counter, frequency measurement |
| %1XXXX | LOGIC | Propagation delay measurement, long-duration event timer |

(* X = 0 or 1; multiple modes applicable.)

---

## NCO Modes (`%00100` single-ended, `%00101` differential)

FRQA added to PHSA every clock. PHSA[31] → APIN; in `%00101`, !PHSA[31] → BPIN. Applications: motor control, audio generation.

**In-PDF example (NCO single-ended):**
```spin
''Demonstration of NCO counter mode (%00100)
CON
  _clkmode = xtal1 + pll16x
  _xinfreq = 5_000_000

PUB NCO_single_ended_mode
'             mode PLL         BPIN     APIN
  ctra    := %00100_000 << 23 + 1 << 9 + 0 'Establish mode and APIN (BPIN is ignored)
  frqa    := $8000_0000                     'Set FRQA so PHSA[31] toggles every clock
  dira[0] := 1                              'Set APIN to output
  repeat                                    'infinite loop, so counter continues to run
```

**Table 4 — NCO state progression** (FRQA=$8000_0000): PHSA toggles `$0000_0000`↔`$8000_0000` each clock; APIN = PHSA[31] = 0,1,0,1,…
- At 80 MHz → APIN = 40 MHz (½ system clock). FRQA=$4000_0000 → PHSA[31] = 0,0,1,1,… = ¼ clock. (Figure 3 = %00100 output; Figure 4 = %00101 differential, blue=APIN, red=BPIN.)

**Equation 1 — NCO frequency:** `f(Hz) = (FRQA / 2³²) × SystemFrequency`. Valid for FRQA in 0…$8000_0000; above $8000_0000 output frequency decreases (Figure 5). For FRQA not a power of 2 (FRQA ≠ 2ᴺ) there is **jitter** since PHSA's MSB toggles at an inconstant rate. Rapidly-changing FRQA (e.g. audio) requires assembly — Spin cannot update FRQA fast enough.

### PWM as an NCO
"Pulse Width Modulation is a Numerically Controlled Oscillator where the amount of high time and low time… may be unequal but the period… remains equal." Code scales the high fraction 0→100%:
```spin
''Demonstration of PWM version of NCO counter mode
CON _clkmode = xtal1 + pll16x
    _xinfreq = 5_000_000
VAR long parameter
PUB go | x
  cognew(@entry, @parameter)                     'start assembly cog
  repeat
    repeat x from 0 to period                    'linearly advance parameter 0..100
      parameter := x
      waitcnt(100_000 + cnt)
DAT
        org
entry    mov dira, diraval        'set APIN to output
         mov ctra, ctraval        'establish counter A mode and APIN
         mov frqa, #1             'increment 1 each cycle
         mov time, cnt
         add time, period
:loop    rdlong value, par        'get an up-to-date pulse width
         waitcnt time, period
         neg phsa, value          'back up phsa so it trips "value" cycles from now
         jmp #:loop
diraval long |< 0
ctraval long %00100 << 26 + 0     'NCO/PWM APIN=0
period long 100                   '800kHz period (_clkfreq / period)
time   res 1
value res 1
```
The PASM cog re-sets `PHSA := 0 − parameter` each period so PHSA's MSB transitions `parameter` cycles later (Figure 6 = scaling PWM output sawtooth). Sawtooth jaggedness smooths with an RC filter on the output.

---

## PLL modes (`%00001`, `%00010`, `%00011`)

Like NCO but with a Phase-Locked Loop. A PLL multiplies an input clock via a VCO and locks output phase to input. `%00010` (PLL single-ended) ~ `%00100` + PLL; `%00011` (PLL differential) ~ `%00101` + PLL. `%00001` (PLL internal / video mode) is a special TV audio-subcarrier mode, **beyond this note's scope**.

- The per-counter PLL **multiplies input ×16** and offers 8 output taps (16×,8×,4×,2×,1×,½×,¼×,⅛×). **PLLDIV** (CTRA) selects which tap → APIN (PLL modes are the only users of PLLDIV).
- **Table 5 — PLLDIV field:** %000→VCO÷128, %001→÷64, %010→÷32, %011→÷16, %100→÷8, %101→÷4, %110→÷2, %111→÷1.
- PLL input range **4–8 MHz** → VCO output **64–128 MHz**; with division, APIN frequencies as low as 500 kHz. **Any frequency 500 kHz–128 MHz** can be generated. Useful for RF and for de-jittering non-power-of-2 FRQA values (de-jitter effectiveness depends on input spectral purity and app noise sensitivity).

---

## Duty Cycle modes (`%00110` single-ended, `%00111` differential)

Output is the **carry** of PHSA: when PHSA overflows ($FFFF_FFFF→$0000_0000), APIN→1.
- FRQA=$0000_0001 → carry once every 2³² (4,294,967,296) cycles ≈ once/54 s at 80 MHz. FRQA=$FFFF_FFFF → carry 0 only once every 2³². (Figure 10 = waveform examples for FRQA $C000_0000…$1000_0000.)
- Signal is high **FRQA÷2³²** of the time (the definition of duty cycle). NCO mode by contrast is fixed 50% (for power-of-2 FRQA). Duty and NCO produce identical waveforms only when FRQA=$8000_0000.

**DAC use** — RC on APIN averages output to an analog voltage. **Equation 2:** `V = 3.3 × (FRQA / 2³²)`.
```spin
{{
     Demonstration of scaling Duty Cycle
                  10kΩ
            APIN ─┳── Out
                  │
                .1μF
     Delta modulation has no fundamental freq but has quantization noise
}}
CON _clkmode = xtal1 + pll16x
    _xinfreq = 5_000_000
VAR long parameter
PUB go | x
  cognew(@entry, @parameter)
  repeat
    repeat x from 0 to period
      parameter := $20C49B * x   '$1_0000_0000 / period * x  <- full-scale voltage
      waitcnt(1000 + cnt)
DAT
        org
entry    mov dira, diraval
         mov ctra, ctraval
         mov time, cnt
         add time, period
:loop    rdlong value, par
         waitcnt time, period
         mov frqa, value         'update the duty cycle
         jmp #:loop
diraval long |< 0
ctraval long %00111 << 26 + 0    'NCO/PWM APIN=0 {BPIN=1} <-not used
period long 2000                 '40kHz period (_clkfreq / period)
time    res 1
value res 1
```
Output (Figure 11) with RC attached is a ramp; the voltage at Out is `(3.3 × x)/period` due to the $20C49B scaling.

---

## Logic modes (`%10000`–`%11111`)

APIN and BPIN are **inputs**; FRQA is added to PHSA only when the mode's logic equation is true. `%10000` (LOGIC never) ≡ counter off; `%11111` (LOGIC always) accumulates every cycle like the system clock. Modes operate on **buffered inputs** (previous clock cycle's pin values) to stabilize the signal — "in a manner similar to the inputs of the SX microcontroller."

**Table 6 — accumulate-when conditions:** %10001 A=0&B=0; %10010 A=1&B=0; %10011 B=0; %10100 A=0&B=1; %10101 A=0; %10110 A≠B; %10111 A=0|B=0; %11000 A=1&B=1; %11001 A=B; %11010 A=1; %11011 A=1|B=0; %11100 B=1; %11101 A=0|B=1; %11110 A=1|B=1.

Use: running tallies of external events (pulse widths, RC time constants). Worked complex system: counter 1 in Duty mode emits a high once/ms; counter 2 in `%11000` (LOGIC A&B) tallies → PHSA = milliseconds BPIN has been high → measures events 1 ms to ~50 days with ms resolution (accuracy bounded by the Propeller clock and the 1 ms reference).

---

## Pin State Detection modes (`%01000`–`%01111`)

Track APIN state (Table 7). `%01X0X` use buffered APIN; `%01X1X` use buffered + double-buffered APIN to detect a transition.

**Table 7 — Pin-state equations** (Accumulate / Feedback-to-BPIN):
%01000 APIN=1 / no · %01001 APIN=1 / yes · %01010 APIN rising-edge / no · %01011 rising-edge / yes · %01100 APIN=0 / no · %01101 APIN=0 / yes · %01110 falling-edge / no · %01111 falling-edge / yes.

- `%01000` (POS detector) ≡ `%11010` (LOGIC A); `%01100` (NEG detector) ≡ `%10101` (LOGIC !A). **Feedback** = the inverse of APIN output to BPIN.

### Σ∆-ADC (`%01001` POS-detector-with-feedback)
Modes `%01001`/`%01101` make Sigma-Delta ADC simple. **Figure 14 external circuit:** APIN—100kΩ—Analog In, two 1 nF caps, a sense component (asterisk) chosen per app: capacitor (0.1 μF) for AC, resistor (150 kΩ) for DC full-scale. Components must sit **within 1 inch (2.5 cm)** of the chip, excess leads cut; **will not work on a breadboard**.

```spin
''This program demonstrates the use of the counter in POS detector with feedback to
''perform ADC calculations.
CON
  _clkmode = xtal1 + pll16x
  _xinfreq = 5_000_000
' At 80MHz the ADC/DAC sample resolutions and rates:
'  bits  rate          bits  rate
'   5  2.5 MHz          10  78 KHz
'   6 1.25 MHz          11  39 KHz
'   7  625 KHz          12 19.5 KHz
'   8  313 KHz          13 9.77 KHz
'   9  156 KHz          14 4.88 KHz
  bits = 12          'try different values from table here
  fbpin = 2          'feedback pin (BPIN)
  adcpin = 7         'feedin pin (APIN)
OBJ
      txt : "VGA_Text"
VAR long value
PUB go
  txt.start(16)
  cognew(@asm_entry, @value)
  txt.out($00)
  repeat
    waitcnt(40_000_000 + cnt)   'wait 1/2 second
    txt.out($00)
    txt.dec(value)
DAT
                org
asm_entry       mov  dira,asm_dira
                movs ctra,#adcpin            'POS W/FEEDBACK mode for CTRA
                movd ctra,#fbpin
                movi ctra,#%01001_000
                mov  frqa,#1
                mov  asm_cnt,cnt
                add  asm_cnt,asm_cycles
:loop           waitcnt asm_cnt,asm_cycles
                mov  asm_sample,phsa         'capture PHSA, get difference
                sub  asm_sample,asm_old
                add  asm_old,asm_sample
                wrlong asm_sample, par
                jmp  #:loop
asm_cycles      long |< bits - 1             'sample time
asm_dira        long |< fbpin                'output mask
asm_cnt         res  1
asm_old         res  1
asm_sample      res  1
```
Waits 2ⁿᵇⁱᵗˢ−1 cycles, differences PHSA → value, written to hub for the Spin `go` to display on VGA. Non-power-of-2 bases via waiting other cycle counts (100 cycles → percentage). This example deliberately sets up the counter via **movs/movd/movi** to illustrate the alternative; keep **movi last** since the counter starts immediately after it.

### Edge / frequency counting (`%0101X` POSEDGE, `%0111X` NEGEDGE)
```spin
''Demonstration of the counter used as a frequency counter
CON
  _clkmode = xtal1 + pll16x
  _XinFREQ = 5_000_000
OBJ
  txt : "VGA_Text"
VAR long ctr, frq
PUB Go | freq
  txt.start(16)
  cognew(@entry, @freq)
  repeat
    txt.out($00)
    txt.dec(freq)         'display value (in Hz)
DAT
        org
entry    mov ctra, ctra_   'establish mode and start counter
         mov frqa, #1      'increment per edge
         mov cnt_, cnt
         add cnt_, cntadd
:loop    waitcnt cnt_, cntadd
         mov new, phsa
         mov temp, new
         sub new, old
         mov old, temp
         wrlong new, par
         jmp #:loop
ctra_    long %01010 << 26 + 7   'mode + APIN
cntadd   long 80_000_000         'wait 1 second, answer in Hz
cnt_     res 1
new      res 1
old      res 1
temp     res 1
```
Counts positive edges on APIN over 1 second → frequency in Hz on VGA.

---

## Conclusion (voice)
"…the counters contained within the Propeller are very powerful and capable of simplifying many counter based functions." With 32 modes each counter can act as: waveform generation (square/saw/sinusoid/audio); PWM driver (servo/motor/LED fading); DAC; ADC; frequency counting; event counting; RF carrier up to 128 MHz; "and many other applications." Counters offload computation from the cog, freeing it for other tasks and achieving higher bandwidth under dynamic manipulation.

## Resources
Example code downloadable from `parallaxsemiconductor.com/an001`. `CTR.spin` and `VGA_Text.spin` ship with the Propeller Tool software library (free download from `parallaxsemiconductor.com/software`).

## Revision History
**v2.0:** Title updated from "Propeller Counters." Updated to Parallax Semiconductor contact info & disclaimer. Updated Figures 1, 2, 8, 9, 12, 13. NCO/PWM mode now referred to as simply NCO mode. Footnotes unbound and placed inline.

## Copyright / trademark
© 2011 Parallax, Inc. dba Parallax Semiconductor. All rights reserved. Propeller and Parallax Semiconductor are trademarks of Parallax, Inc.
