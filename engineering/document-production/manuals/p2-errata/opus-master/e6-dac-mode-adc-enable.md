# Erratum E6: In a DAC Smart-Pin Mode, OUT Needs TT Bit 0 to Run the ADC {#ch-e6}

::: caution
**Expected:** in a DAC smart-pin mode with `TT` = `%00`, the pin's output is off and raising `OUT` turns on the pin's ADC.

**Actual:** with `TT` = `%00`, raising `OUT` runs nothing: the ADC stays off, and the pin reads exactly as it does with `OUT` low.

**Fix:** set `TT` bit 0 in your `WRPIN` word (`$0014_0042` in place of `$0014_0002`) and let the pin's DAC drive the pin while the ADC runs; see *The fix*.
:::

This erratum affects a program that configures a pin for one of the DAC smart-pin modes (`%SSSSS` = `%00001` to `%00011`, with `M[12:10]` = `%101`) with `TT` bit 0 clear, and relies on `OUT` to run the pin's ADC. A pin configured with `TT` = `%01`, the value of the Spin2 symbols `P_TT_01` and `P_OE`, is not affected. Of the three DAC smart-pin modes, only DAC noise (`%00001`) was tested.

## What the P2 is documented to do {#sec-e6-documented}

The P2 Documentation (Parallax), section SMART PINS, describes the `%TT` field of the `WRPIN` configuration word (bits 7:6) in a table that gives one rule for every smart-pin mode and a second rule for the DAC smart-pin modes:

> for all smart pin modes (%SSSSS > %00000):
>
> x0 = output disabled, regardless of DIR
>
> x1 = output enabled, regardless of DIR
>
> for DAC smart pin modes (%SSSSS = %00001..%00011):
>
> 0x = OUT enables ADC in DAC_MODE, M[7:0] overridden
>
> 1x = OTHER enables ADC in DAC_MODE, M[7:0] overridden

The same table defines the pin state the second rule refers to: "'DAC_MODE' is enabled when M[12:10] = %101". The two rules act on different bits. Bit 0 of `TT` sets the output enable; bit 1 chooses whether `OUT` or `OTHER` switches the ADC. By the table, `TT` = `%00` in a DAC smart-pin mode is a pin whose output is disabled and whose ADC `OUT` switches, and `TT` = `%01` is the same with the output enabled. Nothing in the table makes the ADC depend on the output enable.

The mode descriptions in the section SMART PIN MODES say what the ADC provides. For DAC noise, the mode tested here:

> RDPIN/RQPIN can be used to retrieve the 16-bit ADC accumulation from the last sample period.

For the two dithered DAC modes, `%00010` and `%00011`, each description carries the same sentence, which names `OUT` as the switch:

> If OUT is high, the ADC will be enabled and RDPIN/RQPIN can be used to retrieve the 16-bit ADC accumulation from the last sample period.

The KNOWN BUGS section of the P2 Documentation does not list this behaviour.

## What the P2 actually does {#sec-e6-actual}

The part was tested in DAC noise mode (`%SSSSS` = `%00001`) with `M[12:10]` = `%101` and `M[9:8]` = `%00`, the setting the Spin2 symbol `P_DAC_990R_3V` names: a 990-ohm DAC of 3.3 V peak, with the ADC feeding the pin's input. The two configuration words differ only in bit 6, which is `TT` bit 0:

- `$0014_0002`: `TT` = `%00`. Raising `OUT` does not run the ADC. The pin's read state stays exactly as it is with `OUT` low: 0 in every one of 4,096 reads, in every sample taken.
- `$0014_0042`: `TT` = `%01`. Raising `OUT` runs the ADC, as the table states. The pin's read state toggles, high in 1,958 to 2,093 of 4,096 reads per sample across the two runs. With `OUT` low the ADC is off and the read state is 0 in every read.

So in the mode tested, and at the two `TT` settings tested, `OUT` switches the ADC only while `TT` bit 0 also enables the pin's output. The two settings in which `OTHER` switches the ADC, `TT` = `%10` and `%11`, were not tested.

## What your program sees {#sec-e6-sees}

If your program configures a DAC smart-pin mode with `TT` = `%00` and raises `OUT` to start the ADC, the ADC does not start. The pin behaves as it does with `OUT` low: in the test, its read state held at 0 through every read.

The test program read the pin's state through its neighbouring pin, and did not issue `RDPIN` or `RQPIN`. What `RDPIN` returns in DAC noise mode at `TT` = `%00` with `OUT` high was not measured here.

## The fix {#sec-e6-fix}

```spin2
  CFG_DAC_TT01      = $0014_0042        ' DAC_MODE, DAC noise, TT = %01
```

Written to the pin with `WRPIN` in place of `$0014_0002`, this word makes `OUT` run the pin's ADC; it is a rule at each use, applied wherever you configure a pin for a DAC smart-pin mode and switch its ADC with `OUT`.

The change is one bit: bit 6 of the `WRPIN` word, `TT` bit 0, value `$40`. In Spin2 symbols the word is `P_DAC_990R_3V | P_TT_01 | P_DAC_NOISE`; `P_OE` is another name for the same value as `P_TT_01`. The test program checked at run time that this composition equals `$0014_0042`. In another DAC smart-pin word the corresponding change is the same bit 6; only the word above was tested (limits below).

The cost is the pin's output. With `TT` bit 0 set, the table's first rule enables the pin's output regardless of `DIR`, and in DAC noise mode the P2 Documentation says the mode feeds "the pin's 8-bit DAC pseudo-random data on every clock". While the ADC runs, the pin is driven by its DAC. Use a pin that nothing else drives. The test pin had nothing attached, so the drive itself was not observed on the bench.

The limits of the proof:

- Only DAC noise (`%00001`) was tested. The dithered DAC modes (`%00010`, `%00011`) share the table rows quoted above but were not tested.
- Only the `M[9:8]` = `%00` DAC setting (`P_DAC_990R_3V`) was tested.
- Only `TT` = `%00` and `%01` were tested. `TT` = `%10` and `%11`, where `OTHER` switches the ADC, were not.
- The ADC was observed through the pin's read state. Its accumulation was not read with `RDPIN`, and no `WXPIN` or `WYPIN` was issued to the pin.
- The rows of the table for a DAC pin with the smart pin off (`%SSSSS` = `%00000`) are a different case and were not tested.

No setting tested runs the ADC in these modes with the pin's output disabled. A program that needs the ADC with the pin undriven has no tested setting in the DAC smart-pin modes.

## Why it happens {#sec-e6-why}

The account below is the clean-room design study's reading of the mechanism, stated at the level of the programmer's model. The measurements in the next section match it.

In every smart-pin mode, `TT` bit 0 is the pin's output enable, as the table's first rule says; the P2 Documentation adds that "while a smart pin is configured, the %TT bits, explained above, will govern the pin's output enable, regardless of the DIR state". `OUT` reaches the I/O pin circuit as the pin's output bit: in the DAC smart-pin modes the smart pin does not take the output bit over, and with `TT` bit 1 clear it is not replaced by `OTHER`.

In the DAC pin state (`M[12:10]` = `%101`), the I/O pin circuit runs its DAC only while the output enable is high, and runs its ADC only while the output enable and the output bit are both high. With the output enable low, nothing in the circuit runs. The table's second rule describes the ADC switch as depending only on the bit that `TT` bit 1 selects; the circuit adds the output enable as a second condition. With `TT` = `%00`, raising `OUT` sets the output bit, but the output enable stays low, and the ADC does not start.

The same reading gives the cost of the fix. Setting `TT` bit 0 raises the output enable, which turns on the DAC as well, so the ADC runs only while the DAC drives the pin.

The study left open what the pin's read state carries in the DAC pin state while the ADC is off. The test measured it rather than assuming it; the values are in the next section.

## How it was proven on a real P2 {#sec-e6-proof}

**The arrangement.** One P2 board at 200 MHz, with nothing attached to P4 or P5.

- P4 is the pin under test. P5 observes it.
- Every pin operation and every read ran in a measuring cog started by `COGINIT` (cog 1 in both runs). The debugger was confined to cog 0 (`DEBUG_COGS = %0000_0001`), which only collected the results from hub RAM and printed them.
- P4's own `IN` bit cannot show the ADC: in a smart-pin mode, `IN` is the smart pin's flag. P5 was configured once with `$7000_0000` and left with `DIR` low for the whole run, so it never drove. That word selects "relative -1 pin's read state" as P5's A input (`%AAAA` = `%0111`) with P5's smart pin off, and in that case "The resultant 'A' will drive the IN signal". Bit 5 of `INA` therefore carries P4's read state.
- One sample is 4,096 consecutive reads of `INA` in a three-instruction `REP` loop (6 clocks per read), counting the reads in which bit 5 is 1.

**The conditions.** Each condition sets P4 afresh, in this order: `DIRL` (smart pin held in reset while it is configured); `WRPIN` with the condition's word; `DIRH`; `OUTL` or `OUTH`, set explicitly whatever the previous condition left; a `WAITX` of 10,000 clocks; one sample.

| Condition | `WRPIN` word | `TT` | `OUT` |
|---|---|---|---|
| C1 | `$0014_0042` | `%01` | low |
| C2 | `$0014_0042` | `%01` | high |
| C3 | `$0014_0002` | `%00` | low |
| C4 | `$0014_0002` | `%00` | high |

The run was five rounds of C1, C2, C3, C4 in that order, which spreads each condition's five samples across the run.

**The outcomes, written into the program before the run.** Condition X *separates* from condition Y when every sample of X lies outside the range from the smallest to the largest sample of Y.

- C2 must separate from C1, or the reading does not show the ADC at all and the run decides nothing.
- The defect: C4 does not separate from C3, and C4 separates from C2. `OUT` does nothing at `TT` = `%00`.
- The documented behaviour: C4 separates from C3, and C4 does not separate from C2. `OUT` runs the ADC at `TT` = `%00`.
- Any other pattern is inconclusive.

No value was predicted for C1 and C3; they were measured and printed.

**The controls**, each of which had to pass before the program would print a verdict:

- each configuration word, decoded into its published `WRPIN` fields, had the expected values, and equalled its Spin2 symbol composition (`P_DAC_990R_3V | P_TT_00 | P_DAC_NOISE`, `P_DAC_990R_3V | P_TT_01 | P_DAC_NOISE`, `P_MINUS1_A | P_LOGIC_A | P_TT_00 | P_NORMAL`);
- before the rounds and again after them, P4 as a plain pin (`WRPIN #0`) driven high by `DRVH` had to read 4,096 of 4,096 at P5, and driven low by `DRVL` had to read 0. This shows that P5 follows P4's read state and that the loop counts every read.

**The results.** Every control passed in both runs: the path control read 4,096 and 0 before the rounds and 4,096 and 0 after them. The samples, as counts of reads with bit 5 high out of 4,096:

| Condition | Run | Round 1 | Round 2 | Round 3 | Round 4 | Round 5 |
|---|---|---|---|---|---|---|
| C2: `TT` = `%01`, `OUT` high | 1 | 1,963 | 2,093 | 2,025 | 1,986 | 2,056 |
| C2: `TT` = `%01`, `OUT` high | 2 | 2,006 | 2,017 | 1,958 | 1,985 | 2,016 |
| C1, C3 and C4 | 1 and 2 | 0 | 0 | 0 | 0 | 0 |

In both runs, C2 separated from C1, C4 did not separate from C3, and C4 separated from C2: the pattern written down in advance for the defect. With `TT` = `%00`, `OUT` high read the same as `OUT` low in every sample, and never as the running ADC.

The same run proves the fix. C2 is the fix: with `$0014_0042`, `OUT` high ran the ADC in all ten samples of the two runs, and with `OUT` low (C1) the ADC was off in all ten.

The test ran on 2026-09-25, twice. Apart from the C2 samples and the C2 range computed from them, the two runs printed the same values.

## The test program {#sec-e6-program}

The test program is `e6-dac-mode-adc-enable-test.spin2` in the examples archive. Its Spin2 code in cog 0 decodes and checks the three configuration words, starts the measuring cog, waits for it to finish, prints every sample, checks the path control, and prints the separation tests and one verdict. The measuring cog is PASM2 in the program's `DAT` block and is the only code that touches the pins.

The measuring cog runs the four conditions in a loop of five rounds. `cfg_` holds the `WRPIN` word and `outlvl_` the `OUT` level for the next condition:

```pasm2
                mov     round_, #ROUNDS
.round          mov     cfg_, cfg_tt01_         ' C1: TT = %01, OUT low
                mov     outlvl_, #OUT_LOW
                call    #do_cond
                mov     outlvl_, #OUT_HIGH      ' C2: TT = %01, OUT high
                call    #do_cond
                mov     cfg_, cfg_tt00_         ' C3: TT = %00, OUT low
                mov     outlvl_, #OUT_LOW
                call    #do_cond
                mov     outlvl_, #OUT_HIGH      ' C4: TT = %00, OUT high
                call    #do_cond
                djnz    round_, #.round
```

`cfg_tt01_` and `cfg_tt00_` are `DAT` longs holding `$0014_0042` and `$0014_0002`. The routine `do_cond` issues `DIRL`, `WRPIN cfg_`, `DIRH`, then `OUTL` or `OUTH` by the value of `outlvl_`, and calls `sample`. Every sample waits 10,000 clocks, then counts the reads of `INA` in which bit 5 (`PIN_NBR`) is 1:

```pasm2
' One sample: settle, then READS_PER_SAMPLE reads of INA, counting bit P+1.
sample          waitx   ##SETTLE_CLK
                mov     count_, #0
                rep     #3, reads_
                mov     insnap_, ina
                testb   insnap_, #PIN_NBR       wc
        if_c    add     count_, #1
                wrlong  count_, ptrb
                add     ptrb, #4
                ret
```

`reads_` holds 4,096. The path control runs before and after the rounds, with P4 returned to a plain pin:

```pasm2
' Control K: pin P as a plain pin (smart pin off, DIR enables the output),
' one sample driven high, one driven low.
path_control    dirl    #PIN_P
                wrpin   #0, #PIN_P
                drvh    #PIN_P                  ' DIR = 1, OUT = 1
                call    #sample
                drvl    #PIN_P                  ' DIR = 1, OUT = 0
                call    #sample
                ret
```

At the end the measuring cog returns both pins to the smart-pin-off state with `DIRL`, `WRPIN #0` and `OUTL` before it signals that it is done.

To run it, compile with `pnut-ts -d` and load it with DEBUG enabled. P4 and P5 must be free: the program drives P4, and a device attached to either pin can fail the path control. A run that decides the question prints no `RIG FAIL` lines, the path-control counts 4,096 and 0, and one `VERDICT:` line. Every sample is printed as well, so the verdict can be re-derived from the output rather than taken from the program.

## Status {#sec-e6-status}

| Field | Content |
|---|---|
| Erratum | E6 |
| Published by Parallax | No |
| Found by | Predicted by the clean-room design study; confirmed here |
| Confirmed on silicon | Yes — 2026-09-25, on a P2 board at 200 MHz, run twice |
| Fix proven on silicon | Yes — 2026-09-25; a rule at each use: set `TT` bit 0 in the `WRPIN` word |
| Affects | a pin in a DAC smart-pin mode with `TT` = `%00`: raising `OUT` does not run its ADC. Tested in DAC noise mode (`%00001`), `P_DAC_990R_3V`, `TT` = `%00` and `%01` only |
| Test program | `e6-dac-mode-adc-enable-test.spin2` |
