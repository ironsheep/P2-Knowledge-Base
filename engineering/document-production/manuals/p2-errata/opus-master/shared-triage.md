The seven errata found so far are not equally likely to reach a program, and the table lists them in the order a programmer is likely to meet them. E3 is the one that ordinary multi-cog code can meet. Each of the others needs an unusual arrangement of instructions or a specialist feature.

| Erratum | Your program meets it if it… | How often that comes up |
|---|---|---|
| **E3** GETCT Returns a Stale Upper Long | reads `GETCT WC`, `GETMS()`, `GETSEC()` or DEBUG time stamps in a cog of 4-7 that it starts more than 2^32^ clocks (21.47 s at 200 MHz) after reset | Often: ordinary multi-cog code that runs for more than 21.47 s |
| **E7** After a No-Wait RDFAST, the Next Hub Instruction Can Complete Early | starts a hub instruction fewer than 16 clocks after a no-wait `RDFAST` | Rarely: code normally does other work after a no-wait `RDFAST` |
| **E1** SETQ Block Transfers Lose Their Pointer Step | places an `ALTx`, `AUGS` or `AUGD`, or a `##` operand, between a `SETQ` and a block transfer that updates `PTRx` | Rarely: an unusual arrangement |
| **E2** An Immediate ALTx Takes a Pending AUGS | writes an `AUGS` explicitly and places an immediate-`#S` `ALTx` before its target | Rarely: only with an explicit `AUGS` |
| **E4** GETXACC Clears Only During a Goertzel Burst | runs DDS/Goertzel bursts one at a time and clears the sums with `GETXACC` | Only Goertzel measurements |
| **E5** The Goertzel Accumulators Trail by One Clock | reads the DDS/Goertzel sums with `GETXACC` after each burst | Only Goertzel measurements |
| **E6** In a DAC Smart-Pin Mode, OUT Needs TT Bit 0 to Run the ADC | switches the ADC of a DAC smart-pin mode with `OUT`, with `TT` = `%00` | Only that pin configuration |
