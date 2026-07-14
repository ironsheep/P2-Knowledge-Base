# XBYTE Technique Mining — Source Ledger

**Started:** 2026-07-14
**Lives at the manual root, deliberately.** It was first written to `audit/` and was therefore
**not versioned at all** — `.gitignore:175` ignores `manuals/*/audit/`, which is a transient
workspace. A durable source-of-record cannot live there. If you add a standing record for a manual,
put it beside `PLANNING.md`.
**Purpose:** Study live, working XBYTE implementations; extract techniques; carry them into the
guide **in our own words and our own compiled code**, crediting the projects in **Appendix C** as
live implementations a reader can go study.

**Why this ledger exists.** The techniques enter the manual body *anonymously* — ideas in a manual
carry no byline. That means **this file is the only place the lineage lives.** It is also the only
way to apply the promotion filter below, which depends on knowing *how many independent
implementations* attest a technique.

---

## 0. The promotion filter (agreed with Stephen, 2026-07-14)

A working emulator mixes four different things: genuine idioms, workarounds for *that project's*
constraints, the author's taste, and kludges that happen to work. Harvesting uncritically would
launder one project's hacks into "best practice" with our name on them.

A technique may be stated as a **RULE / best practice** only if:

- **(a) convergence** — it appears in two or more independent implementations; **or**
- **(b) reference** — it appears in Chip Gracey's Spin2 interpreter (the reference implementation
  of the feature, by its designer); **or**
- **(c) mechanism** — it can be shown *from the silicon's documented behavior* why it is right.

Everything else is reported honestly as **"one way, and here is the tradeoff"** — never promoted.

**Expression, not attribution, is the boundary we must not cross:** never lift a line of code.
Everything we publish is written by us and compiled with `pnut_ts`.

**Anything the live code contradicts in our current text goes to the corrections register**
(`engineering/operations/P2KB-CORRECTION-FINDINGS.md`), not quietly into new prose.

---

## 1. Source register

| ID | Source | Date | Tier | Role |
|----|--------|------|------|------|
| **A** | `REF-NO-COMMIT/P2SpaciesVGA/8080GamesEmulator.spin2` | 2021-01-28 | community implementation | upstream **lead** + existence proof — never a reader-facing citation |
| **A′** | `REF-NO-COMMIT/P2_Space_Invaders/8080GamesEmulator.spin2` | 2021-01-26 | (same project, older) | superseded by **A** |
| **B** | `REF-NO-COMMIT/pnut-ts-parts/Spin2_interpreter.spin2` | 2026-05-13 | **reference implementation** | Chip Gracey's own XBYTE — highest authority for *idiomatic* XBYTE |
| **C** | `REF-NO-COMMIT/pnut-ts-parts/Spin2_debugger.spin2` | 2025-05-18 | reference (P2-side) | authority for what the debug stub does on the P2 |
| **C′** | `engineering/ingestion/external-inputs/pnut_ts_facts/SingleStep-Debugger-Theory-of-Operations.md` | — | **our own derivation** | peer tier — **not** authority; see correction **X2** |
| **D** | P2KB `p2kbPasm2Getbrk` (← P2 Silicon Doc) | — | **documentary authority** | authority for `GETBRK` field layout |
| **E** | `REF-NO-COMMIT/larger-emulators/MegaYume/` — SEGA Mega Drive (**68000** + Z80) | 2025-10-29 | community implementation | Wuerfel_21 · **OBEX 4162** |
| **F** | `REF-NO-COMMIT/larger-emulators/NeoYume/` — NeoGeo AES (**68000** + Z80) | 2025-11-03 | community implementation | Wuerfel_21 · **OBEX 4087** |
| **G** | `REF-NO-COMMIT/larger-emulators/MisoYume/` — SNES (**65816** + SPC700) | 2025-12-06 | community implementation | Wuerfel_21 · beta — **the decisive counter-example** |
| **H** | `REF-NO-COMMIT/riscv/riscvemu/` — **RISC-V** | — | community implementation | totalspectrum (Eric Smith) — **JITs, does not interpret** |
| **I** | `REF-NO-COMMIT/zog/zog-master/zog_p2.spin` — **ZPU** | — | community implementation | totalspectrum, forked from heater — **uses XBYTE** |
| **J** | `REF-NO-COMMIT/official-parallax/xbyte.spin2` | — | **OFFICIAL PARALLAX** | `parallaxinc/propeller` → `resources/FPGA Examples/` — the canonical demo **+ Parallax's own clock-by-clock dispatch table** |

### A vs A′ — which 8080 copy?

**A (`P2SpaciesVGA`) is the newer**, by two days. It carries a configurable `displaytype` constant
(HDMI and/or VGA selectable); A′ still has hardcoded `coginit`s and a `pgm_debug` development cog.

**It does not matter for mining: the XBYTE emulator core is byte-identical between them** — 566
lines each, zero diff once whitespace is normalized. Every difference lives in the launcher, the
display driver, and the debug cog. **Cite A.**

> Citations below anchor to **labels**, not line numbers — labels are stable across both copies.

---

## 2. Source A — the 8080 games emulator

### A1 · Guest interrupt servicing — *the answer we did not have*

The guest's IRQ arrives as a **P2 ATN event** from another cog. A running bytecode handler polls
it at a safe point with `JATN`; if the guest's interrupt-enable is set, the emulator **injects the
guest's interrupt by hand-executing an `EXECF` with a constructed, table-entry-shaped operand**:

- `jatn #int_event` — polled inside the handler chain (`i_ret` / `i_pchl`).
- `int_event` — reads the interrupt vector; `if_c jmp #reset_8080` (reset always wins).
- `bitl INTE,#0 wcz` — the guest's interrupt-enable flag is **a cog register**, tested *and cleared*.
- `if_nz jmp #int_ignore` — not enabled → resume the stream.
- `mov pb,t1` — stash the guest return address in `PB`.
- `execf ##int_go | %011111110000 << 10` — **inject**: handler address OR'd with a skip pattern
  shifted left 10 — i.e. a *synthesized dispatch-table entry*, executed directly.

`i_di` / `i_ei` are one-liners over the same cog register (`bitl` / `bith  INTE,#0`).

**This is the mechanism our manual is completely silent on.** See gap **G1**.

### A2 · Guest `HLT` — halt-and-wait-for-interrupt

`i_hlt` parks the cog on `jnatn #i_hlt_natn` (wait for ATN). If an interrupt arrives *and* `INTE`
is set, it rejoins `int_event_go`. Otherwise `i_hlt_natn` does `sub pb,#1` / `_ret_ rdfast #0,pb`
— **backs the stream up one byte and re-executes the `HLT`**. Correct 8080 halt semantics, in four
instructions, using the FIFO position as the guest PC.

### A3 · The trailing-skip landing pad — *a trap we never warn about*

> `instloop  nop   'landing pad for trailing skip patterns that xbyte would cancel`

…followed by fifteen more `nop`s. **A handler's trailing SKIPF bits run past the end of the
handler and cancel whatever follows.** Related mechanism: **D3** (skipping is *suspended* inside a
`CALL`, which is why calls out of a handler are safe but fall-through is not).

### A4 · How to actually debug an XBYTE program — de-arm and substitute

In `reset_8080` the arming pair is **commented out**:

> `'  push   #$1FF   'start xbyte    COMMENT OUT TO SINGLE-STEP`
> `'  _ret_  setq    #$000           COMMENT OUT TO SINGLE-STEP`

…and replaced with a hand-rolled software dispatch loop carrying a `debug()`:
`rfbyte pa` → `getptr pb` → `sub pb,ptra` → `debug(uhex_byte(pa),uhex_word(pb,regp))` →
`add pb,ptra` → `rdlut t1,pa` → `execf t1`.

**Consequence for the manual:** the software dispatch loop we teach in **§4.4 ("Dispatch, by
hand")** purely as *pedagogy* is in fact the working **guest-level debug mode**. Swap the hardware
engine for its software equivalent and you can instrument every dispatch — printing the guest PC
and opcode per bytecode, which hardware dispatch cannot show you. §4.4 has a real purpose and we
never say so.

**Complementary, not contradictory, to C1/D2:** the P2 debugger *can* step and display XBYTE state
(mode, skip pattern), but it steps **P2 instructions**. The software-loop swap is what gets you a
**guest-instruction** trace. Both belong in a "Debugging XBYTE" section.

### A5 · Resuming the stream after a hub call

`i_in` / `i_out` call out to hub code for port emulation (`rdlong pa,ptra[-2]` / `[-3]`, then
`call pa`), and resume with:

> `i_out_resume  add pb,#1` / `_ret_  rdfast #0,pb`

We name `PB` as the FIFO position; we never teach this **re-point-the-FIFO-from-PB** resume idiom.

### A6 · Mode operand actually used

`setq #$000` — *"full 8-bit lookup at lut $000"*. A plain 256-entry table at LUT base $000, F=0.
The simple end of the mode space. (Contrast **B2**, the compressed end.)

---

## 3. Source B — Chip Gracey's Spin2 interpreter *(the reference)*

### B1 · Table-entry format — **CONFIRMS our §4.1**

> `bc_get_field  long  var_ptr | %00 << 10`
> `bc_read       long  var_rd  | %0111001110 << 10`

Handler address OR'd with the SKIPF pattern shifted left 10 — exactly our §4.1 claim (address in
`[9:0]`, pattern in `[31:10]`). ✅ **Our manual is right.**

He places tables with **`orgf <lut addr>`** so that an entry's address is `base + bytecode`
automatically — entries appear in bytecode order, each commented with its bytecode value.

### B2 · Mode `$1A1` — **CONFIRMS our §7.3 and §7.4**

> `wrf_wr  _ret_  setq  #$1A1   '(initially: begin xbyte, compress Ax..Fx, write flags)`

Decoded against our §7.3 pattern `%ABBBB00xF`: **A=1** → table base LUT `$100`; **BBBB=`$A`** →
compress high-nibbles `$Ax`…`$Fx`; **F=1** → dispatch writes C,Z. That is precisely Chip's own
comment, and it is **independently corroborated by placement**: `orgf $300` puts the main table at
LUT `$100` — exactly the base A=1 selects. ✅ **Our compression rule and F bit are right, and now
empirically confirmed rather than merely transcribed.**

### B3 · Two live dispatch tables — `SETQ2` as a **grammar**, not just prefix pages

Chip runs **two** tables at once and flips between them with one-shot `SETQ2`:

| Table | Mode | Base | Placed by | Contents |
|-------|------|------|-----------|----------|
| main bytecodes | `$1A1` | LUT `$100` | `orgf $300` | the Spin2 bytecode set |
| variable operators | `$081` | LUT `$000` | `orgf $215` | bytecodes `$15`…`$1E` |

`$081` decodes as A=0 (base LUT `$000`), BBBB=8, F=1 — corroborated by placement: `orgf $215` =
LUT `$015`, and the first entry there is commented `'15`, i.e. bytecode `$15`. Entry address =
base + bytecode. ✅

Handlers end:

> `_ret_  setq2  #$081   '(next bytecode is a variable operator)`

and the file states the contract outright: *"must end in `_ret_ setq2 #$081` to invoke variable
operator bytecodes."*

**This is a much bigger idea than our Chapter 12 teaches.** We present one-shot `SETQ2` narrowly,
as a *prefix-page* mechanism (the 6809's `$10`/`$11`). Chip uses it as a **two-stage bytecode
grammar**: "the byte that follows is of a *different kind*." Same instruction, far wider concept.

### B4 · `REP` as an interrupt shield — **the safety rule we are missing**

Attested **eight times**, in Chip's own words:

- `rep #99,#1`   — *"use REP to protect cordic operation until ret/_ret_"*
- `rep #99,#1`   — *"use REP to protect cordic operation until call/ret/_ret_"*
- `rep @stall,#1` — *"use REP to protect variable from interrupts"*
- `rep #99,#1`   — *"use REP to stall interrupts until _ret_"* (`clkset_init`)
- ×4 more — *"use REP to stall interrupts to protect cordic operation"*

Passes the filter on **(b) reference**, **(a) convergence within the reference** (8 sites), and
**(c) mechanism**. See gap **G2** — this is a **correctness hazard**, not a style note.

### B5 · Self-modifying arming pair — **CURIOSITY, NOT a best practice**

`wrf_rd` / `wrf_wr` — the two arming instructions (`push #$1FF` and `_ret_ setq #$1A1`) are
**rewritten at run time into the bitfield read/write slots**. Launch enters via
`push #wrf_rd  'return to wrf_rd to start xbyte after callinit`, so the pristine (unrewritten)
pair *is* the arming sequence; once the engine is running, those two longs are reused as scratch.

Elegant, and exactly the kind of cog-space squeeze that belongs to an interpreter that is out of
room. **Verdict: report as "one way, and here is the tradeoff." Do not promote.**

### B6 · `SETQ2`'s double meaning — a collision we never flag

- `setq2 #(lut_code-1) & $1FF` + `rdlong 0,ptrb` → **block-clear LUT**
- `setq2 #lut_end-lut_code-1` + `rdlong` → **block-load LUT**
- `setq2 #$081` + `_ret_` → **one-shot XBYTE mode**

Same mnemonic, two entirely different jobs, distinguished only by what follows it. Our manual uses
**both** forms (Ch. 11 loads the table with `setq2`+`rdlong`; Ch. 12 arms one-shot mode with
`setq2`) and **never warns the reader they are different things**. See gap **G5**.

### B7 · Dispatching an `EXECF` value by hand

> `if_nz  rdlut  z,z    'look up execf value`
> `if_nz  execf  z      'chain to setup byte/word/long[pop address]`

Chained dispatch outside the engine — the same primitive the engine uses, driven manually.

---

## 4. Source C/D — the single-step debugger and `GETBRK`

### D1 · Authoritative `GETBRK` layout (P2KB ← Silicon Doc)

**`GETBRK D WC`:**

| Field | Meaning |
|-------|---------|
| C | LSB of the SKIP/SKIPF/EXECF/XBYTE pattern |
| D[31:28] | 4-bit **CALL depth since the pattern** — *skipping **suspended** if not `%0000`* |
| D[27] | 1 = SKIP · 0 = SKIPF/EXECF/XBYTE |
| D[26] | LUT sharing enabled |
| D[25] | **XBYTE pending on next `_RET_`/`RET`** |
| D[24:16] | **the 9-bit XBYTE mode** |
| D[15:00] | 16 event-trap flags |

**`GETBRK D WZ`:** Z=1 if no pattern queued (D=0); otherwise **D = the full 32-bit pattern**,
used LSB-first.

✅ **Third independent confirmation that the mode operand is 9 bits** (our Ch. 7).

### D2 · The P2 debugger supports XBYTE natively — we never mention it

The single-step debugger's top row displays **`[SKIP/SKIPF pattern]  [XBYTE]`**: the live 32-bit
skip pattern and the 9-bit XBYTE mode. In the disassembly view, **instructions whose SKIP bit is
set are drawn struck through** — you can *see* which instructions the pattern is cancelling.

### D3 · Skipping is **suspended inside a `CALL`** — a mechanism fact we never state

From D1: the CALL-depth field carries *"skipping suspended if not `%0000`."* So a handler may
`CALL` a helper and the helper's instructions **will not be eaten** by the handler's skip pattern.

**This is load-bearing and undocumented in our manual.** Our own Chapter 11 depends on it —
`op_lda_imm` ends `_ret_ call #set_nz` — and we never tell the reader *why* that is safe. It is
also the other half of **A3**: skipping is suspended *inside* a call, but a trailing pattern still
runs *past* the end of the handler, which is what the NOP landing pad absorbs.

### D4 · Why XBYTE survives a debug interrupt

The debug ISR **saves and restores the full 8-level hardware stack** (`POP` ×8 on entry; `PUSH
stk7`…`stk0` on exit). That is precisely why XBYTE survives being debugged: the `$1FF` the engine
depends on is preserved. Good mechanism detail for the "Debugging XBYTE" section.

---

## 5. Consolidated technique inventory

| # | Technique | Attested by | Filter | Verdict | Lands in |
|---|-----------|-------------|--------|---------|----------|
| T1 | Guest-interrupt injection via a synthesized `EXECF` operand; guest IE as a cog reg; `JATN` poll at a safe point | A | (c) mechanism; 1 impl | **RULE** *(pending 2nd impl — confirm vs 68000/Z80)* | new §, + concerns-table "guest interrupts" column |
| T2 | Guest `HLT` = park on `JNATN`, else back the FIFO up one byte and re-run | A | 1 impl | one way + tradeoff | same § |
| T3 | **`REP` as an interrupt shield** around atomic sequences in a handler | B ×8 | (b)+(c) | **RULE — correctness hazard** | fix to §5.3 + new safety § |
| T4 | **Skipping is suspended inside a `CALL`** | D (Silicon Doc) | (c) | **RULE — mechanism fact** | Ch. 2 / Ch. 8 |
| T5 | Trailing skip pattern runs *past* the handler → NOP landing pad | A + D3 | (a)+(c) | **RULE** | Ch. 2 / Appendix D |
| T6 | De-arm XBYTE, substitute the software loop, instrument it → **guest-level trace** | A | (c) | **RULE** | new "Debugging XBYTE" §; retro-justifies §4.4 |
| T7 | `GETBRK` exposes XBYTE mode + live skip pattern; debugger displays both | C/D | (c) documentary | **RULE** | "Debugging XBYTE" § |
| T8 | Re-point the FIFO from `PB` to resume after a hub call | A | 1 impl | one way + tradeoff | Ch. 8 |
| T9 | **`SETQ2` as a two-stage bytecode grammar** (not merely prefix pages) | B | (b) | **RULE** | widen Ch. 12 / Ch. 13 |
| T10 | Two live dispatch tables at different LUT bases | B | (b) | **RULE** | Ch. 7 / Ch. 12 |
| T11 | `orgf <lut addr>` to place a table so entry addr = base + bytecode | B | (b) | **RULE** | Ch. 4 |
| T12 | `SETQ2` means two different things (block-move vs one-shot mode) | B | (c) | **RULE — caution** | Ch. 6 |
| T13 | Self-modify the arming pair into scratch registers | B | (b) but project-specific | **curiosity — do NOT promote** | at most an aside |
| T14 | Compression + F together in a real bytecode set (`$1A1`) | B | (b) | worked reference | Ch. 7 example |

---

## 6. Gaps in our manual that this mining exposed

| # | Gap | Evidence |
|---|-----|----------|
| **G1** | **Guest interrupts** — how to service the *guest's* IRQ/NMI when dispatch is hardware. §5.3 covers *P2* interrupts only. | A1, A2 |
| **G2** | **`REP` interrupt shield.** §5.3 presents interruptibility as a **pure benefit** and never states the consequence: an atomic sequence in a handler can be split by an interrupt. Zero occurrences of `REP` in the manual. | B4 |
| **G3** | **Skip-suspension inside `CALL`.** Zero occurrences of "suspend"/"call depth". Our own Ch. 11 relies on it. | D3 |
| **G4** | **Debugging XBYTE.** Zero occurrences of "GETBRK" or "debug" in the manual. Two complementary techniques exist and we teach neither. | A4, D2, D4 |
| **G5** | **`SETQ2` collision** never flagged, though we use both forms. | B6 |
| **G6** | **`SETQ2` taught too narrowly** — prefix pages only, not as a grammar. | B3 |

---

## 7. Corrections raised (route to the register — do NOT fix silently)

| # | Against | Finding | Status |
|---|---------|---------|--------|
| **X1** | our manual §5.3 | Presents XBYTE interruptibility as a pure benefit; omits that handlers doing atomic work must shield with `REP`. Not wrong, but **dangerously incomplete**. | to raise |
| **X2** | **our own** `SingleStep-Debugger-Theory-of-Operations.md` §6.4 | Says the checkmark appears *"if bit 25 of `mBRKC` is set (**C,Z affected by XBYTE**)."* The Silicon Doc (via P2KB `p2kbPasm2Getbrk`) says **D[25] = "XBYTE pending on next `_RET_`/`RET`"**. "C,Z affected" is the **F bit**, which is **D[16]** — the low bit of the 9-bit mode in D[24:16]. **The gloss appears to be wrong.** | to raise — **NOT settled**: the display gloss lives **host-side** (PNut/term-ts), not in Chip's P2-side stub, so settling it needs the host display source or Chip |
| **X3** | our manual §10.2 | *"68000: read the word with `RFWORD`, decode further by hand"* is **Claude's derivation, never observed in any implementation.** | **blocked on source E** |

---

## 8. THE BIG FINDING — who actually uses XBYTE, and who doesn't (sources E–J)

**Our §10.2 grades guest CPUs on *instruction shape*. That is not the axis that decides it.**

| Implementation | Guest CPU | Instruction shape | Our §10.2 verdict | **Actually uses XBYTE?** |
|---|---|---|---|---|
| Spin2 interpreter (B) | Spin2 bytecode | byte stream | — | ✅ **yes** |
| 8080 games emulator (A) | 8080 | byte, opcode-first | sweet spot | ✅ **yes** |
| Zog (I) | ZPU | byte, opcode-first | sweet spot | ✅ **yes** |
| Parallax demo (J) | (toy bytecode) | byte stream | — | ✅ **yes** |
| **MisoYume (G)** | **65816** | **byte, opcode-first** | **"the sweet spot"** | ❌ **NO** |
| MegaYume (E) | 68000 | 16-bit words | partial | ❌ no |
| NeoYume (F) | 68000 + Z80 | 16-bit words | partial | ❌ no |
| riscvemu (H) | RISC-V | 32-bit fixed | "table only" | ❌ no — **JITs to native PASM2** |

> Grep hygiene note: an initial `grep -i xbyte` over the Yume sources produced hits that were
> **substring false positives** — `ma**xbyte**s`, `t**xbyte**`, `r**xbyte**`. Corrected: the Yume
> family contains **zero** XBYTE. They use `EXECF`/`SKIPF` heavily (11–28 sites each) — **dispatch
> without the engine.**

### The decisive counter-example — MisoYume (65816)

The 65816 is byte-stream and opcode-first: by our §10.2 it is *"the sweet spot — auto-fetch **and**
table dispatch both apply directly."* **The real SNES emulator uses neither.** Two causes, both
verified in the source:

1. **The guest's code is not in hub.** A SNES ROM is megabytes; it lives in **PSRAM**. The hub FIFO
   streams **hub memory only** — so `RDFAST`/`RFBYTE` auto-fetch is *structurally impossible*.
   MisoYume hand-rolls the fetch: `PSRAM_QUESIZE`, `rk_romque_reload`, `rk_romque_left`, a prefetch
   queue, and `call rk_readcode_f` — where **`rk_readcode_f` is a register (`res 1`)**, so the fetch
   routine is **swappable per memory region** (ROM / RAM / MMIO / bank).
2. **LUT is not free.** XBYTE reads its dispatch table from **LUT**. MisoYume needs LUT for the
   PSRAM prefetch queue, so its dispatch table went to **hub** — `rk_optbase long @rk_opcode_tbl`,
   read with `rdlong rk_opimpl, rk_memv`. The smoking gun is in the source: **`'rdlut rk_opimpl,
   rk_memv` sits commented out directly above the `rdlong` that replaced it.** They moved the table
   out of LUT, and XBYTE went with it.

**What they keep is the dispatch.** All of them still use `EXECF`/`SKIPF`. This *vindicates* our
§10.1 "two separable assets" framing exactly — the real world keeps **table/EXECF dispatch** and
drops **auto-fetch**. We simply never told the reader *which question decides it*.

### The two columns the concerns table was missing — and they dominate

| Question | If yes | If no |
|---|---|---|
| **Does the guest's code live in HUB?** | auto-fetch works | hand-roll the fetch (auto-fetch is impossible, not merely awkward) |
| **Is LUT free (256 longs)?** | XBYTE dispatch works | table goes to hub; XBYTE is off the table entirely |

Contended by: PSRAM/HyperRAM prefetch queues, palettes, line buffers, sprite tables. **These
outrank instruction shape for every real emulation target**, which is why the resource-budget
section (plan item 3) is load-bearing, not decorative.

### T15 · Two-stage dispatch — opcode → addressing mode → operation *(MisoYume)*

Solves the addressing-mode matrix our §11.4 declares out of scope. The table entry packs **both**
the handler's `EXECF` value **and** a 4-bit addressing-mode selector (nibble 7). An `ALTD`-patched
`SKIPF` runs the shared addressing-mode block (operand read, X/Y indexing, DP/SP wrap, cycle
penalties), *then* the opcode's own `EXECF` runs the operation:

`rdlong rk_opimpl,rk_memv` → `bitl rk_opimpl,#10 wcz` → `if_nc execf rk_opimpl` *(simple opcodes
dispatch immediately)* → else `getnib pa,rk_opimpl,#7` → `altd pa,#rk_amode_tbl` → `skipf 0-0` →
shared addressing-mode block → `execf rk_opimpl`.

This is the **industrial** version of the shared-body idiom we only sketch in §2.4 / §11.3.

### T16 · For fixed-width RISC, the answer may be "don't interpret" *(riscvemu)*

`riscvemu` carries a **`jit/`** directory and translates guest instructions to **native PASM2**. Our
§10.2 tells the RISC reader to use table dispatch and feed it by hand; the real implementation
declines to interpret at all. **A JIT is an option our manual never names.**

### T17 · Cycle accuracy is pervasive, and XBYTE gives you nowhere free to put it *(MisoYume)*

`add rk_cycles,#6  'internal cycle`, `rk_dp_penalty`, `rk_xy_penalty` — guest cycles are counted
explicitly, everywhere. A console emulator *must* be cycle-accurate (video/audio timing). XBYTE
makes **dispatch** free but every handler still pays to count guest cycles.

Corroborating, from the thread author's own words (source lead **L2**, Wuerfel_21 — the author of
E, F, **and** G): *"I had previously created 68000, Z80 and SPC700 cores"* … those had
*"instruction-level timing at best (or no timing for the 68000)."*

---

## 9. Source J — Parallax's OFFICIAL `xbyte.spin2`

From `parallaxinc/propeller` → `resources/FPGA Examples/xbyte.spin2`. Sixty-three lines, and it is
**documentary authority**, not a community lead.

### J1 · Parallax's own clock-by-clock table — **CONFIRMS our Chapter 5**

| clock | phase | hidden | description |
|---|---|---|---|
| 1 | go | `RFBYTE` byte | last clock of the instruction executing `RET`/`_RET_` to `$1F8..$1FF` |
| 2 | get | `RDLUT` @byte, **write byte to PA** | 1st clock of 1st cancelled instruction |
| 3 | go | LUT long → next D | 2nd clock of 1st cancelled instruction |
| 4 | get | `EXECF D,` | 1st clock of 2nd cancelled instruction |
| 5 | go | `EXECF D,` **write GETPTR to PB** | 2nd clock of 2nd cancelled instruction |
| 6 | get | flush pipe | 1st clock of 3rd cancelled instruction |
| 7 | go | flush pipe | 2nd clock of 3rd cancelled instruction |
| 8 | get | — | 1st clock of the routine — **loop to 1 if `_RET_`** |

✅ Our §5.1 "the eight clocks" ✓ · `PA` written at clock 2 (§4.3) ✓ · `PB` gets `GETPTR` at clock 5
(§3.4) ✓ · header states *"Overhead is 6 clocks, including `_RET_`"* ✓ (§1.2, §5.2).

### J2 · The canonical relative-branch bytecode

```
r4       rfvars  pa       'get offset      <- SIGNED variable-length read
         add     pb,pa    'add offset
  _ret_  rdfast  #0,pb    'init fifo read at new address
```

`RFVARS` (**signed**) + `PB` + `RDFAST` — the canonical relative branch. Our §3.3 teaches
`RFVAR`/`RFVARS` and our §8.3 teaches `PB`; **neither shows this, the obvious reason both exist.**

### J3 · OPEN QUESTION — *"no stack pop"*

The arming line reads:

> `_ret_  setq  #$100    'start xbyte with lut base = $100, **no stack pop**`

**We do not know what "no stack pop" means**, and our Chapter 6 does not mention any such option.
Is there an arming variant in which XBYTE *pops* the stack? If so, Ch. 6 has a hole. **Verify
against the Silicon Doc before writing anything near it.** Do **not** guess.

---

## 10. Source leads — forum threads (**BLOCKED: captcha**)

**The Parallax forum cannot be fetched from this container.** Every request — including
`forums.parallax.com/` itself — returns **HTTP 202** plus a redirect to
`/.well-known/sgcaptcha/`. This is SiteGround bot protection, not a rate limit or a user-agent
problem. **Stephen must capture these** (browser → save/copy). Recorded here so they are findable
again:

| # | Thread | URL | Why it matters |
|---|---|---|---|
| **L1** | Intel 8086 CPU Emulator | `forums.parallax.com/discussion/174634/intel-8086-cpu-emulator` | the **x86 row**. **≥4 pages** (p2/p3/p4 exist) |
| **L2** | Complete cycle-correct emulation of CPU with external bus | `forums.parallax.com/discussion/175304/…` | **cycle accuracy + external bus** — the two concerns §8 just proved dominant. By Wuerfel_21 (author of E/F/G) |
| **L3** | **8086 CPU XBYTE emulator working** | `forums.parallax.com/discussion/173345/…` | **NOT on Stephen's list — found by search.** An 8086 built **WITH XBYTE**. Directly tests §10.2's "x86: the decode explodes" |
| **L4** | ByteCode Executor | `forums.parallax.com/discussion/173531/…` | XBYTE-adjacent |
| **L5** | towards a P2 Virtual Machine using XBYTE and Subsystems | `forums.parallax.com/discussion/comment/1567366/` | XBYTE VM design discussion |

**What search already told us about the 8086 emulator** (unverified — from result snippets, not the
thread itself; **treat as lead, not fact**): all instructions implemented, including single-step and
breakpoint interrupts; emulates 256KB RAM + 64KB ROM + an ACIA-ish serial port at 115_200; runs the
Seattle Computer Products 8086 Monitor; **~33 P2 cycles per 8086 cycle** (160 MHz P2 vs 4.77 MHz
8086); the stated goal is a "P2-DOS" running MS-DOS 2.11. Source availability described as limited /
work-in-progress. **And, crucially:** *"XBYTE interpreters for the 8086 have been written and work
very well, with XBYTE resulting in the fastest possible emulation."* — if true, **x86 belongs in the
XBYTE column**, and our §10.2 grading of it needs revisiting.

---

## 10b. Source K — `Simple-i8086` (**the x86 row**, from thread L1)

`REF-NO-COMMIT/Simple-i8086/simple_i8086.spin2` — 92 KB, archived 2022-06-09. Ships with
`MONITOR.ASM` + `MONITOR.ROM` (the Seattle Computer Products 8086 monitor). **Stephen captured this
from the captcha-walled thread L1.**

### K1 · It uses the dispatch asset, NOT the auto-fetch asset — the loop is hand-rolled

```
i_next
        call    #\i_readop      ' fetch the opcode ourselves
        push    #i_nextop       ' push OUR OWN return address -- not $1FF
        execf   i_opimpl        ' dispatch

i_readop
        call    #\i_readcodeb   ' read a code byte via segmented CS:IP
        mov     i_opcode, i_tmpb
        shl     i_tmpb, #2
        add     i_tmpb, i_optable
  _ret_ rdlong  i_opimpl, i_tmpb   ' <- primary table lives in HUB
```

**No `push #$1FF`. No `_RET_ SETQ` arming. No `RDFAST`/`RFBYTE`.** This is precisely the software
dispatch loop our §4.4 teaches as *pedagogy* — running in production, in a full 8086. (Third
independent sighting of the software loop as a real tool: cf. **A4**, **G**.)

**Table placement:** the **primary** opcode table is in **hub** (`rdlong ... , i_optable`); the
**secondary** group tables are in **LUT** (`add pa, #i_rotshift8_tbl - $200` → `rdlut i_opimpl, pa`
— the `- $200` is LUT-space addressing). So LUT is spent on the *second* decode level.

### K2 · Two-level decode — the ModR/M group tables

x86's "group" opcodes select among 8 sub-operations via the ModR/M **reg** field. The emulator
extracts it and indexes a **second** `EXECF` table in LUT:

`mov pa,i_modrm` → `shr pa,#3` → `and pa,#7` → `add pa,#i_rotshift8_tbl - $200` →
`rdlut i_opimpl,pa` → `call #\i_rep_opimpl`.

This is the same **two-stage dispatch** shape as MisoYume's addressing-mode table (**T15**), reached
independently by a different author on a different guest. **T15 is now converged (a) — promote.**

### K3 · **§10.2 is WRONG about x86 prefixes** — they are not one SETQ2 job

Our §10.2 says of x86: *"prefixes and escapes are a job for one-shot SETQ2 alternate tables."* The
real 8086 does **not** do that for segment overrides. It uses a **shared body + a state register +
re-fetch**:

```
i_seg_cs   mov  i_override, i_cs    ' a      <- one body, four prefixes,
i_seg_ds   mov  i_override, i_ds    ' | b       selected by the table entry's
i_seg_es   mov  i_override, i_es    ' | | c     skip pattern (note the a/b/c/d
i_seg_ss   mov  i_override, i_ss    ' | | | d   comment columns)
           bith i_override, #31     ' a b c d
           jmp  #\i_next            ' a b c d <- set state, GO FETCH AGAIN
```

**The distinction our manual is missing.** Prefixes are not one thing — they are **two**:

| Kind | Examples | What it changes | Right tool |
|---|---|---|---|
| **Map / escape prefix** | 6809 `$10`/`$11`, Z80 `CB`/`ED`, x86 `$0F` | **which handler runs** — it selects a different opcode map | **one-shot `SETQ2`** ✅ (our Ch. 12 is right *here*) |
| **Modifier prefix** | x86 segment override, `REP`, `LOCK`, operand-size | **not** which handler runs — *how it behaves* | **state register + re-fetch loop** ❌ SETQ2 is the wrong tool |

An alternate table redirects dispatch; a segment override does not want dispatch redirected — it
wants the *same* handler to touch *different memory*. Our §10.2 lumps "prefixes, escape bytes,
ModR/M, SIB" together and assigns them all to SETQ2. **That is Claude's derivation and it is wrong
for the modifier half.** → correction **X4**.

### K4 · `REP` — why the engine's auto-fetch buys nothing here

```
i_rep_opimpl
.loop           push    #.ret
                execf   i_opimpl
.ret    _ret_   djnz    i_rep_cnt, #.loop
```

`REP` must re-execute **the following instruction** N times **without re-fetching it each time**.
Under XBYTE's fetch-on-`_RET_` loop you *cannot* express that as a plain `_RET_` handler — the
engine would fetch a new bytecode every iteration. The `REP` handler must therefore hand-roll its
own fetch and re-dispatch, which is exactly what this does (`i_repne` / `i_rep_loop` do
`call #\i_readop`, then loop `execf`).

> **Stated carefully:** this does **not** make `REP` *impossible* under XBYTE — a handler may loop
> internally instead of returning. It makes the engine's auto-fetch **worthless on that path**: you
> hand-roll the fetch anyway. Do not overstate this in the manual.

### K5 · Also present

- **Cycle counting** — `mov i_cycles, #0` per instruction (cf. **T17**).
- **The guest's trap flag *is* single-step** — `testb i_flags,#I_TF_BIT` → `i_trap`. The 8086's TF
  is the guest-side equivalent of the debug interrupt; a nice mirror for the debugging section.

### K6 · The x86 verdict for the concerns table

| Asset | x86 | Why |
|---|---|---|
| Table/`EXECF` dispatch | ✅ **yes** — two-level (hub primary + LUT group tables) | the opcode still indexes a table |
| Auto-fetch | ❌ **no** | the stream is **segmented `CS:IP`**, not a linear hub address; modifier prefixes re-fetch with state; `REP` re-executes without re-fetching |

**⚠️ NOT the last word.** Thread **L3** ("8086 CPU XBYTE emulator working") describes a *different*
8086 that reportedly **does** use XBYTE. If both exist, we have the richest possible teaching
contrast — **the same guest CPU, two strategies, tradeoffs explicit** — which is far better than a
single verdict. **L3 is now the highest-value missing source.**

---

## 10c. Sources L/M — `i8086_xt` + `i8086_xt-psram` — **the controlled experiment**

`REF-NO-COMMIT/i8086_xt/` (2022-07-12, 8,314 lines) — a full IBM PC **XT**: BIOS ROM, CGA, BASIC.
Ships **both** variants: `i8086_xt.spin2` (guest memory in **hub**) and `i8086_xt-psram.spin2`
(guest memory in **PSRAM**). Same emulator, two memory backends. Also from thread **L1**.

### L1 · THE CONTROLLED EXPERIMENT — dispatch is orthogonal to the memory model

Diffing the hub variant against the PSRAM variant:

| Measure | Result |
|---|---|
| Total changed lines | **115** of 8,314 (~1.4%) |
| Changed lines touching **dispatch** (`execf` / `i_opimpl` / `i_optable`) | **ZERO** |
| What *did* change | **only** the memory-access path — PSRAM pin config, a scratch buffer, the read/write routines |

**They swapped the entire memory backend and the dispatch did not notice.**

### L2 · The three separable concerns — and the coupling lesson

Our §10.1 teaches **two separable assets** (auto-fetch, table dispatch). The evidence says the honest
model has **three separable concerns**:

1. **The fetch** — where does the guest's code come from?
2. **The dispatch** — how do you get from opcode to handler?
3. **The memory model** — how does the guest read/write data?

The XT pair proves **(2) is independent of (1) and (3)**.

**And here is *why* they could do that — the lesson worth the chapter.** They **hand-rolled the
fetch** (`call #\i_readcodeb`, which goes through the memory path). So when guest memory moved to
PSRAM, the fetch followed for free. **Had they taken XBYTE's auto-fetch, the PSRAM port would have
been impossible without rewriting the dispatch mechanism entirely** — the FIFO streams hub only.

> **THE TRADEOFF, provable from this single pair of files:**
> **XBYTE's auto-fetch is free speed, but it welds the guest's code to hub RAM.** A hand-rolled fetch
> costs clocks and buys a **swappable memory backend**. If the guest might ever outgrow hub, do not
> take the auto-fetch — you will pay for it once, in a rewrite.

This reframes the concerns table's *"where does the guest's code live"* column: it is **not a yes/no
gate on a feature — it is a coupling decision made at the start of the project.** That is the single
most useful thing this mining has produced.

### L3 · Same guest CPU, three dispatch strategies — a ladder, not a binary

| Implementation | Fetch | Dispatch | P2 features used |
|---|---|---|---|
| **`i8086_xt`** | hand-rolled | **plain jump table** — `rdlong i_opimpl,…` + **`jmp i_opimpl`**; prefixes by explicit `cmp` chain (`$26/$2E/$36/$3E`, `$F2/$F3`) | **none** |
| **`Simple-i8086`** (K) | hand-rolled | **`EXECF` + skip patterns**; shared bodies; two-level LUT group tables | dispatch asset |
| **thread L3 (missing)** | ? | **XBYTE** (reportedly) | both assets |

Three rungs of one ladder, **on one guest CPU**. This shows the reader that **you do not have to
climb all the way** — the honest thing our §10.1 implies and never demonstrates. It is a far better
Chapter 10 than the one we have, and it is *free*: the material already exists.

> Do **not** infer an evolution story (Simple → XT) from the archive dates. `Simple-i8086` (2022-06-09)
> uses `EXECF`; `i8086_xt` (2022-07-12) does not. Authorship/lineage is **not established** — record
> the strategies, not a narrative about how they came to be.

### L4 · The FIFO is spent elsewhere

In the XT, `RDFAST`/`RFBYTE` appear **only** in the **CGA video** path and the **serial TX buffer** —
never in instruction fetch. Another instance of the resource-contention point: the FIFO, like LUT, is
a *cog* resource that the rest of the system also wants.

---

## 11. Open questions

1. **X2** — is `GETBRK` D[25] "XBYTE pending" (Silicon Doc) or "C,Z affected" (our theory doc)?
   Needs the host-side debugger display source, or Chip.
2. **X3 — now answerable, and the answer is not what we wrote.** §10.2 says the 68000 case is
   *"dispatch on the opcode word via a table; auto-fetch is partial — read the word with `RFWORD`."*
   **Two 68000 emulators exist (E, F) and neither uses XBYTE at all.** Whatever we say about the
   68000 must be rewritten from what MegaYume/NeoYume actually do. **Not yet read in detail.**
3. **J3** — what is *"no stack pop"*?
4. **T1** — guest-interrupt injection still rests on **one** implementation (A). Do the Yume cores
   do it the same way? (They have no XBYTE, so their answer may not transfer.)
5. **L3** — an XBYTE 8086 would be the single most valuable remaining source. **Blocked on the
   captcha.**
