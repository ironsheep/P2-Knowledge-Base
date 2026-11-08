# Run sheet — KB contract-gaps bench, November 2026

Two programs. **Bare board, nothing attached, no jumpers.**

**For the run**
1. USB serial connected (DEBUG on P62/P63). Board on its 20 MHz crystal.
2. **Power-cycle the board before each program.** Program 2 needs a cog that has not run since power-up.
3. Build each with `pnut-ts -d` and load it to RAM with DEBUG on, one download per program:
   - `pnut-ts -d tests/test-contract-gaps-p1-instruction-flow.spin2`
   - `pnut-ts -d tests/test-contract-gaps-p2-cog-lifecycle.spin2`
4. Check that the log's `DOWNLOAD TO RAM` line names the program's binary: `test-contract-gaps-p1-instruction-flow.bin` (27,654 bytes from pnut-ts 1.55.10) or `test-contract-gaps-p2-cog-lifecycle.bin` (22,506 bytes).
5. **Save the whole console output** of each run into `tests/logs/` (create the folder if it is not there). The terminal's own file name is fine.
6. If no `=== END ===` appears within the hang limit: power-cycle and save the log as it is. That is a hang, not a result.

| Program | Pins in use (keep clear) | Runs | Hang limit | Look for |
|---|---|---|---|---|
| `test-contract-gaps-p1-instruction-flow.spin2` | **none** | under 1 s | 20 s | `VERDICT` lines for A to H, `=== END ===` |
| `test-contract-gaps-p2-cog-lifecycle.spin2` | **P0–P2** (driven) | about 1 s | 30 s | `VERDICT` lines for I to O, `=== END ===` |

**Questions**
- **A:** does a far `CALLD PA,#label` in hub land on its label, or where a byte field puts it?
- **B:** does a backward `DJNZ x,##label` land on its label in cog and in hub?
- **C, D:** does a pending `SETQ`, `AUGS` or `AUGD` survive an instruction cancelled by a false condition or by `SKIP`?
- **E:** do `CALLA`/`RETA`, `CALLB`/`RETB` and `CALLD`/`JMP PA` suspend a skip pattern, as `CALL` does?
- **F:** does `ALTD`, `ALTS` or `ALTR` apply past an instruction `SKIP` cancels?
- **G:** does a `_RET_ SETQ2` at the end of a bytecode routine leave Q for the next routine?
- **H:** does `TRGINT1` branch while `STALLI` is active?
- **I:** what a `COGINIT` of a running cog, a stopped cog and itself leaves of DIR, OUT, C, Z, the stack, PA, PB, Q, the LUT, the CT1 target, a skip pattern and a REP.
- **J:** is a cog's OUT gated by its own DIR?
- **K:** which read, `GETQX` or `GETQY`, moves the CORDIC on to the next result?
- **L:** what `QDIV` returns when the quotient exceeds 32 bits.
- **M:** what `GETQX` returns with nothing pending, and in how many clocks.
- **N:** whether `RDLUT`/`WRLUT` PTRA indexes and updates count longs or step by four.
- **O:** the bit order `CRCNIB` takes from Q.

**Reading it.** Each question has controls that must come out both ways. These labels mean that arm is not a result: `RIG FAIL` (a control or a premise missed), `INCONCLUSIVE` (the two sides could not differ), `NO READING` (no reading the program expects, or a step hung) and `STEP HUNG` (a worker did not finish in its limit). `OTHER` and `MIXED` are readings outside the expected ones, and their raw values are printed. Either way, send the log as it is.
