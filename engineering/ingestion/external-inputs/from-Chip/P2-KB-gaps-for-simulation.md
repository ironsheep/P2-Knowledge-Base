# P2 Knowledge Base: gaps found while building a P2 simulator

**From:** Chip Gracey (with Claude), November 2026
**For:** Stephen Moraco, for the P2 Knowledge Base
**KB version used:** `ironsheep/P2-Knowledge-Base` at commit `1b0b173` (2026-10-12)

## Background

We built a P2 simulator ("Virtual P2") inside the single-file Spin2 editor. It runs the exact binary PNut-TS produces, Spin2 interpreter included, on eight simulated cogs, and shows the 64 pins live.

- **Decoder:** generated automatically from the KB's `language/pasm2/*.yaml` encodings. That covers 357 instructions in 407 encodings, and all of them decoded.
- **Behaviour:** each instruction follows the KB's descriptions.
- **Checks:** 62 Spin2 results and 31 PASM / multi-cog results, compared with values computed separately. All of them pass.

The KB got us most of the way. This document lists every place where we had to:

- **(G) guess:** the KB doesn't say, and the simulator may be wrong;
- **(V) verify elsewhere:** we found the answer by assembling with PNut-TS or by reading the Spin2 interpreter source. The KB should state it, so others don't have to repeat that work;
- **(X) skip:** the subject is too thinly covered to simulate at all.

Items are roughly in order of importance for a correct simulator.

---

## 1. Branch and address encodings (V, then G)

- **(V) `JMP #A` / `CALL #A` / `CALLA` / `CALLB` / `CALLD` relative, in cog/LUT execution.** The KB says "PC += A". The assembler actually encodes the offset in **bytes**: `jmp #lbl` three instructions back encodes −12. In cog/LUT mode the PC is therefore adjusted by A/4. In hub execution A is in bytes. The KB should say so explicitly.
- **(V) 9-bit relative branches** (`DJNZ`, `TJZ`, `IJNZ`, `JATN`, etc., with `#S`). These are in **instructions**: −4 means 4 instructions back. In hub execution that's ×4 bytes.
- **(V) `LOC PA/PB/PTRx,#A` relative in cog mode.** This is in **longs**. `loc pa,#lbl` six instructions back encodes −6, not −24. That's inconsistent with JMP/CALL, so it deserves an explicit note.
- **(G) `##` (AUGS) with 9-bit-S branches.** For example `djnz x,##far`: is the 20-bit offset counted in instructions (×4 in hub) or in bytes?
- **(G) `JMPREL`.** The KB says hub execution uses `D[17:0] << 2`. Please confirm this for cog/LUT.

## 2. PTRA/PTRB expressions (V)

The KB mentions `#%1SUPNNNNN` but doesn't define it. Assembling with PNut-TS shows:

- **Layout:** `%1 S U P NNNNN`. S: 0 = PTRA, 1 = PTRB. U: 1 = update the pointer. P: 1 = post-modify (use, then update), 0 = pre-modify.
- **Index width:**
  - With U = 0, the index is **6 bits** signed (−32..31), using P as its top bit.
  - With U = 1 it's **5 bits** signed, and `00000` means **16**.
- **Scaling:** the index is multiplied by the access size (1, 2 or 4).
- **(G) Block transfers:** with `SETQ` + `RDLONG`/`WRLONG` and an updating PTRx, we assumed the update is index × 4 × (Q+1). The interpreter's `setq #2-1 / rdlong y,--ptra` depends on this.
- **(V) Augmented form:** after `AUGS`, the 32-bit value is `%1 S U P` at bits 23..20 plus a 20-bit signed index. Bits 31..24 are zero.
- **Plain immediates:** an immediate hub address without AUGS is limited to 0–255. The KB already notes this.

## 3. SETQ, AUGS and AUGD lifetime (V/G)

- **(V)** `SETQ` passes through `AUGS`/`AUGD` as well as through ALTx. The KB only mentions ALTx. The interpreter's start-up depends on it: `setq dbase_init`, then `coginit #hubexec,##launch_spin`, where the `##` inserts an AUGS between them.
- **(G) Which instructions actually use Q?** We assumed:
  - RDLONG/WRLONG/WMLONG blocks;
  - MUXQ, COGINIT, QDIV, QFRAC, QROTATE, CRCNIB;
  - the span field of the BITx/DIRx families;
  - WRPIN/WXPIN/WYPIN ranges.
  A complete list would help.
- **(G) Condition false:** does a SETQ, AUGS or AUGD survive an intervening instruction whose condition is false? Is it used up by a cancelled (SKIP) instruction?
- **(G) Two AUGS in a row:** does the second replace the first?

## 4. XBYTE (V/G)

`architecture/xbyte_engine.yaml` is good. We still needed:

- **(V) Compressed-index formula.** For bytecodes at or above the %BBBB threshold, index = `(BBBB << 4) + (b[7:4] − BBBB)`. We confirmed it against the interpreter's tables at LUT $100 and $215. The KB says "compressed index" without the formula.
- **(G) Flags with F=1.** Are C/Z loaded from bits 1/0 of the **table index** (as the KB says) or of the **bytecode**? They differ for compressed bytecodes.
- **(G) The $1FF stack entry.** On a RET or `_RET_` to $1FF, is $1FF popped and re-pushed, or not popped at all? The interpreter's "pop v so $1FF pops on next ret" comments suggest it is never consumed. Also, the KB says "RET to $1F8..$1FF". What happens for $1F8–$1FE?
- **(V) A `_RET_ SETQ2` that dispatches a bytecode only sets the one-shot table.** Q must not also apply to the first instruction of the next bytecode routine.
- **(G) Exact sequencing:** where `PB` (GETPTR) is sampled, and whether the 6 overhead clocks include the `_RET_`.

## 5. SKIP, SKIPF, EXECF, CALL and REP interactions (G)

- **CALL inside a skip pattern:** we assumed the pattern is suspended until the matching return.
  - Which instructions count as calls? CALL, CALLPA, CALLPB, CALLA, CALLB, CALLD?
  - Which count as returns? RET, `_RET_`, RETA, RETB?
  - What about interrupts?
- **JMP inside a skip pattern:** we assumed the pattern keeps running across jumps. The interpreter relies on this.
- **SKIPF in hub execution:** it acts like SKIP. What does a leaped-over instruction cost: 0 clocks in cog mode, 2 in hub?
- **ALTx followed by a skipped instruction:** is the ALT applied to the next *executed* instruction, or lost?
- **REP:**
  - Is it cancelled by any branch, including a `_RET_`?
  - How does it behave in hub execution, and with SKIP/SKIPF inside the block?
  - What exactly happens with D = 0 and with S = 0?

## 6. ALTI (G)

The KB names the fields `%rrr_ddd_sss_RRR_DDD_SSS` but doesn't give the table of control codes. We only implemented two cases:

- **Execute D as the next instruction:** `%101_100_100`, as `alti rd` in the interpreter uses it.
- **A guess at the general case:** 1xx = substitute the field, and the low two bits 01/10 = increment/decrement.

The full table is needed:
- what each RRR value does (result address vs instruction substitution);
- the mask-size semantics;
- the interaction with the next instruction's I bit.

## 7. CORDIC (G)

- **Algorithms:**
  - `QROTATE`, `QVECTOR`, `QLOG`, `QEXP`: the exact algorithms, including iteration count, gain compensation and rounding, so results can match silicon bit for bit. We currently use floating point.
  - `QSQRT`: rounding (floor or round), and which operand is the high long. We assumed `{S, D}`.
  - `QDIV`/`QFRAC`: the results for divide by zero and for quotients over 32 bits.
- **Result buffering:**
  - How many results can be outstanding?
  - Do `GETQX` and `GETQY` each consume a result, or read the same one?
  - What happens to a result whose X was read but not its Y when a new command is issued? The interpreter issues `QDIV` + `GETQX` only, then later `QDIV` + `GETQY`. That worked only after we made a new command retire partly-read results.
- **Timing:** the issue rate (one command every N clocks), the stall rules, and what `GETQX` returns when nothing is pending.

## 8. Random numbers (G)

- **`GETRND`:** the xoroshiro128** variant, how it's seeded at reset and by `HUBSET`, whether it advances every clock, and which bits each cog sees ("unique per cog").
- **`XORO32`:** the exact algorithm (constants, and how the 32-bit result is built from 16-bit iterations).
- **`BITRND`, `DIRRND`/`OUTRND`/`FLTRND`/`DRVRND`, and `WAITX WC`:** which random bits they use.

Exactness matters here: without it, a simulated `getrnd()` program can never match hardware traces.

## 9. Hub timing (G)

- **The egg-beater formula:** which bank a cog can reach on which clock, as a function of `CT`, cog ID and `addr[4:2]` (or wider).
- **Exact clock counts:** the RDxxx 9–16 and WRxxx 3–10 ranges, unaligned accesses, SETQ block transfers, RDFAST/WRFAST start-up, and FIFO refill.
- **Hub execution:** the cost per instruction, the cost of a branch (13–20), and how hub execution and RDFAST share the FIFO.

## 10. Interrupts and debug (X)

We couldn't simulate these from the KB alone:

- **Interrupts:**
  - `SETINTx` event codes and priorities;
  - the IJMP and IRET registers;
  - `STALLI`/`ALLOWI`, `RESIx`/`RETIx`, `TRGINTx`/`NIXINTx`;
  - shielding rules (after ALTx, AUGx, REP, and so on).
- **The debug interrupt:**
  - `HUBSET` debug enable;
  - the debug ISR entry and register save area at $FC000+;
  - the `BRK` conditions and `GETBRK` fields;
  - `COGBRK`.
- **The Spin2 debugger's protocol:** how DEBUG output reaches the serial pin.

This is what's needed to show DEBUG output from a simulated program, which would be the most useful next feature.

## 11. Events (G/X)

- **`SETSE1..4`:** the encoding of the configuration bits (pin edge/level, lock events, and so on).
- **The other events:** `SETPAT` and the PAT event; the FBW, XMT, XFI, XRO and XRL events.
- **Clearing rules:** for each event, which instructions clear it.
- **CT1–CT3:** confirm that the event fires when `CT` equals the target exactly, and how a target in the past is handled.

## 12. Smart pins (X, beyond storing X/Y/Z)

All 32 modes have their own KB files, but simulating them needs clock-level detail:

- **When things happen:** when IN rises, when Z updates, and what `RDPIN` returns before the first result.
- **Async serial TX/RX:** buffering (how many words), the start/stop framing, the exact bit timing with fractional `X[31:16]`, and when IN rises relative to the stop bit.
- **The mode word:** the full `WRPIN` field layout, including the A/B input selectors, filters, logic/inversion, the output select bits and the DIR/OUT override.
- **Ranges:** do pin ranges wrap within the 32-pin port for every pin instruction (`DIRx`/`OUTx`/`DRVx`/`FLTx`) or only for `WRPIN`/`WXPIN`/`WYPIN`?
- **Reconfiguring:** what happens on `WRPIN` while DIR is high, beyond "unpredictable".

## 13. Pin I/O model (G)

- **Combining cogs:** how the eight cogs' DIR and OUT combine. We assumed each is ORed independently. Is OUT gated by that cog's own DIR?
- **Priority:** a smart pin's output vs OUT.
- **Latency:** the registered delays from OUT to the pin and from the pin to INA, in clocks.
- **Reading back:** INA for a pin that's driven. Does it read the actual pin level?

## 14. COGINIT, cogs and hub configuration (G)

- **What `COGINIT` resets:** DIR/OUT, PA/PB, flags, hardware stack, skip and REP state, LUT, events.
- **Timing:** load time for cog-exec starts, and start-up time for hub-exec starts. Also what a cog sees when it re-launches itself.
- **`COGID {#}D WC`:** the exact semantics.
- **LUT sharing:** `SETLUTS` and cog pairs.
- **`HUBSET`:** every mode (clock, filters, debug, reset, PRNG seed), the clock-switch timing rules, and the actual RCFAST frequency to assume.
- **(V) Empty hub space:** $80000–$FBFFF reads as zero, and the top 16 KB also appears at $FC000. The interpreter depends on the zeroes (`loc ptrb,#$80000`). The KB should state both.

## 15. Instruction details (G, small)

- **Pixel operations:** exact formulas for `ADDPIX`, `MULPIX`, `BLNPIX`, `MIXPIX` and `SETPIV`/`SETPIX`.
- **Bit permutations:** the exact `SEUSSF`/`SEUSSR` permutation. We also need `RGBSQZ`/`RGBEXP` rounding, and the bit order for `CRCBIT` and `CRCNIB` (which Q bit is used first).
- **Edge cases worth one line each in the KB:**
  - `ROR`/`SHR`/`SAR`/`RCR` with a shift of 0: C = D[0];
  - `ADDS`/`ADDSX`: C = the true sign. The KB's own text and table disagree here; the table is right;
  - `ENCOD`/`ONES`/`TESTN` flags;
  - which of `GETBYTE`/`GETWORD` set Z;
  - `RDLUT` with PTRx.
- **`TESTB`/`TESTP` vs `BITx`/`DIRx`:** they share encodings and are told apart by WC/WZ (01 or 10 vs 00 or 11). The KB has duplicate encodings without saying this, which a mechanical decoder trips over.
- **YAML files:** about 140 entries have `bits` fields that aren't 32-bit patterns (for example `asmclk.yaml`). It would help if every instruction file had a machine-readable `bits` field, and pseudo-instructions were marked as such.

---

## What would help most

1. **Exact CORDIC and PRNG algorithms** (sections 7 and 8). Without them, simulated results can't match hardware.
2. **Interrupts and debug** (section 10). That would let DEBUG output work in the simulator.
3. **Clock-level smart-pin behaviour**, at least for async serial (section 12).
4. **The ALTI control-code table and the XBYTE flag/stack details** (sections 4 and 6).
5. **A set of "golden" hardware traces:** small programs that print results via DEBUG on real silicon, together with their output. Every simulator, and the KB itself, could then be checked against them. We have two such test programs (`tests/sim/ops.spin2`, `tests/sim/cogs.spin2`) and would be glad to run more.

The (V) items are settled. We confirmed each one against PNut-TS's own encodings or the v55 interpreter source, and each can go into the KB as written.
