# Run sheet — KB findings bench, November 2026

One program. **Bare board, nothing attached, no jumpers.**

**For the run**
1. USB serial connected (DEBUG on P62/P63). Board on its 20 MHz crystal.
2. Build `pnut-ts -d tests/test-f361-f564-subpin-cogstop.spin2`, load to RAM with DEBUG on.
3. **Save the whole console output** to `tests/logs/test-f361-f564-subpin-cogstop.log`.
4. If no `=== END ===` appears within the hang limit: power-cycle, note the last line seen, and send it. That is a hang, not a result.

| Program | Pins in use (keep clear) | Runs | Hang limit | Look for |
|---|---|---|---|---|
| `test-f361-f564-subpin-cogstop.spin2` | **P0–P2, P32–P47** (driven) | under 1 s | 20 s | `VERDICT` lines, `=== END ===` |

**Questions**
- **F-361, VO-J-005 arm B:** which pins a 2-pin and a 4-pin streamer capture read at each base.
- **F-564:** what COGSTOP leaves on a plain pin and on a smart pin the stopped cog configured.

**Reading it.** Each question has arms that must come out both ways. `INCONCLUSIVE` or `RIG FAIL` means a control missed, so the run is not a result: send the log as it is.
