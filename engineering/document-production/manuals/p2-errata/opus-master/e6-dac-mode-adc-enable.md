# Erratum E6: In a DAC Smart-Pin Mode, OUT Needs TT Bit 0 to Run the ADC {#ch-e6}

<!-- include: shared-e6.md -->

## What happens {#sec-e6-actual}

The P2 Documentation, section SMART PINS, describes the `%TT` field of the `WRPIN` word (bits 7:6) with one rule for every smart-pin mode and a second for the DAC smart-pin modes:

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

The two rules act on different bits: bit 0 sets the output enable, and bit 1 chooses whether `OUT` or `OTHER` switches the ADC. By the table, `TT` = `%00` is a pin with its output disabled whose ADC `OUT` switches.

On P2 hardware, in DAC noise mode (`$0014_0002`, `TT` = `%00`), raising `OUT` did not run the ADC: the pin's read state stayed exactly as it was with `OUT` low, 0 in every one of 4,096 reads, in every sample. With `TT` = `%01` (`$0014_0042`), raising `OUT` ran the ADC as the table states, and the read state toggled, high in 1,958 to 2,093 of 4,096 reads. In the mode tested, `OUT` switches the ADC only while `TT` bit 0 also enables the pin's output.

Only programs that use the ADC of a DAC smart-pin mode, switched by `OUT`, with `TT` bit 0 clear, meet this erratum. A pin configured with `P_TT_01` or `P_OE` (the same value) is not affected.

Only DAC noise (`%00001`), the `P_DAC_990R_3V` setting, and `TT` = `%00` and `%01` were tested. The ADC was observed through the pin's read state; its accumulation was not read with `RDPIN`.

## A proven workaround {#sec-e6-workaround}

**What any workaround must do:** set `TT` bit 0 in the `WRPIN` word of a pin in a DAC smart-pin mode whose ADC you switch with `OUT`.

**One way, proven on P2 hardware:** the tested DAC noise word with `TT` = `%01`.

```spin2
  CFG_DAC_TT01      = $0014_0042        ' DAC_MODE, DAC noise, TT = %01
```

Written to the pin with `WRPIN` in place of `$0014_0002`, this word makes `OUT` run the pin's ADC: a *rule at each use*. The change is one bit, bit 6 (`$40`); in Spin2 symbols the word is `P_DAC_990R_3V | P_TT_01 | P_DAC_NOISE`. In another DAC smart-pin word the change is the same bit, but only this word was tested.

**The cost** is the pin's output. With `TT` bit 0 set, the output is enabled regardless of `DIR`, and in DAC noise mode the pin's DAC drives it while the ADC runs, so use a pin that nothing else drives. No tested setting runs the ADC in these modes with the pin undriven.

**Found by** the clean-room design study, as a prediction, and confirmed on P2 hardware on 2026-09-25. Parallax does not list it.
