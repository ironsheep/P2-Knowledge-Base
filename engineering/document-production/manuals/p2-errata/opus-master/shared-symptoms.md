| Symptom | Erratum |
|---|---|
| `GETCT WC`, `GETMS()`, `GETSEC()` or a `DEBUG_TIMESTAMP` stamp reads behind by 2^32^ clocks (21.47 s at 200 MHz), or a multiple of it, in one group of cogs | **E3** |
| DEBUG messages from different cogs carry time stamps out of order by 21.47 s at 200 MHz | **E3** |
| A `RDBYTE`, `RDWORD` or `RDLONG` returns the previous hub read's data, with that value's flags | **E7** |
| A `WRBYTE`, `WRWORD` or `WRLONG` is lost | **E7** |
| A `SETQ` block `RDLONG` writes one wrong long and changes other cog registers, or the cog stops responding | **E7** |
| An `RFLONG` after a waiting `RDFAST` returns `$0000_0000` | **E7** |
| After a `SETQ` block transfer through `PTRx++`, the pointer moved by one long, not by the block | **E1** |
| An `ALTx` with an immediate `#S` moves its `D` register | **E2** |
| `GETXACC` read with the streamer idle does not clear the Goertzel sums | **E4** |
| A Goertzel burst's sum lacks its last term and holds the last term of the burst before it | **E5** |
| In a DAC smart-pin mode with `TT` = `%00`, raising `OUT` does not run the pin's ADC | **E6** |
