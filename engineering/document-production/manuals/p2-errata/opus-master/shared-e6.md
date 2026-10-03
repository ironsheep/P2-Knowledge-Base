::: caution
**Who meets it:** a pin in a DAC smart-pin mode (`%SSSSS` = `%00001` to `%00011`) configured with `TT` = `%00`, whose ADC the program switches on with `OUT`.

**What you see:** raising `OUT` does not start the ADC.

**What to do:** set `TT` bit 0 (`$40` in the `WRPIN` word, `P_TT_01` in Spin2). The pin's DAC then drives the pin while the ADC runs.
:::
