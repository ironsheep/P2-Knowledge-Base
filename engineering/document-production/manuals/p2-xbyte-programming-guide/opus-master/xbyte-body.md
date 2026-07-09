# Part I: XBYTE Fundamentals

This first part builds the mental model. It opens on the one idea XBYTE exists to serve — the loop at the center of every interpreter — then teaches the **skip family** (SKIP, SKIPF, EXECF) that XBYTE is built from, the **FIFO** that feeds it bytecodes, and the **LUT dispatch table** it reads. By the end of Part I, XBYTE itself (Part II) is no longer magic: it is hardware that runs a dispatch you already understand, once per bytecode, for free.

# Chapter 1: Understanding XBYTE {#ch-1}

## 1.1 The loop at the center of every interpreter

Every interpreter ever written runs the same loop. Fetch the next instruction — a small number, a *bytecode* — from a stream. Look up what that number means. Jump to the code that does it. Run that code. Repeat.

A *bytecode* is just one small number that stands for one operation the interpreter knows how to perform: "push a constant," "add the top two stack items," "jump if zero." A program, in this style, is a stream of those numbers. The interpreter's whole job is to walk the stream and, for each number, run the matching *routine* (also called a *handler*).

Written by hand on the P2, that loop costs something on every single bytecode: read the byte, use it to index a table, branch to the handler. Those few instructions run *between* every pair of useful operations, so their cost is multiplied by the length of the program. For an interpreter, the dispatch loop is the tax you pay on everything.

## 1.2 What XBYTE is

**XBYTE is hardware that runs that loop for you.** Once armed, the P2's bytecode-execution engine fetches the next bytecode from the hub FIFO, writes it where your handler can see it, indexes a 256-entry dispatch table in LUT RAM, and jumps to the handler — and when the handler ends, it does it all again, automatically, until you stop it. You write the handlers; the engine runs the loop between them.

```{=latex}
\DiagXbyteLoop
```

The payoff is the cost of that loop. The *Parallax Propeller 2 Documentation v35* states the overhead of XBYTE dispatch is **6 clocks per bytecode**, *"including `_RET_` at the end of each bytecode routine"* — against the **9 clocks** the same fetch-look-up-execute sequence costs in software (*"2+3+4, or 9, clocks to get the next bytecode, look it up, then execute that bytecode's routine"*). A bytecode routine *"could be as short as a single 2-clock instruction with a `_RET_` prefix, making the total XBYTE loop take only 8 clocks."*

::: hardware
**XBYTE is built out of ordinary instructions you can use yourself.** The engine's dispatch is an **EXECF** — a jump plus a skip pattern — fed from a **RDLUT**, fed from an **RFBYTE** off the FIFO. None of these are special to XBYTE. Chapter 2 teaches them as the everyday instructions they are; Chapter 5 shows the engine running exactly that sequence, in hardware, in six clocks.
:::

## 1.3 Why the P2 has it

The P2 is fast at running native PASM2, but native code is large: a big program does not fit in a cog's 512 longs, and even hub-executed code trades speed for space. Interpreted bytecode is the classic answer — compact programs, a small interpreter — and it is how Spin2 itself runs on the P2. The cost of interpretation is the dispatch loop, and XBYTE exists to make that cost small enough that an interpreted language, or an emulated CPU, stays practical.

That last case is the one this guide builds toward. Emulating another processor is interpretation: each of the guest's instructions is a "bytecode," and the handler is the PASM2 that reproduces it. When dispatch is cheap, a single cog can emulate a whole small CPU and still have clocks left to drive video and sound — which is exactly what the community projects in Appendix C do.

## 1.4 The pieces, and where they live

XBYTE coordinates five pieces of the P2 you already have. This guide devotes a chapter to each; here is the map.

| Piece | What it does for XBYTE | Where it is | Chapter |
|-------|------------------------|-------------|---------|
| The **hub FIFO** | delivers the bytecode stream, one byte at a time | hub → cog, primed by **RDFAST** | 3 |
| The **dispatch table** | maps each bytecode to a handler + a skip pattern | 256 longs in LUT RAM | 4 |
| **EXECF** | the jump-plus-skip that *is* dispatch | a cog instruction | 2 |
| **PA** (`$1F6`) | holds the current bytecode for the handler to use | a cog register | 4 |
| **PB** (`$1F7`) | holds the FIFO pointer (for inline operands) | a cog register | 3 |
| The **hardware stack** | holds `$1FF`, the address each routine returns *to* | the cog's call stack | 6 |

The handlers themselves live in cog or LUT RAM and end in **RET** or **`_RET_`**. The engine is armed with one instruction — **SETQ** (or **SETQ2**) — and a `$1FF` on the stack. Those are Chapter 6.

## 1.5 When to reach for XBYTE

XBYTE pays off when dispatch cost dominates — any time your "program" is a stream of byte-sized operations read from hub memory and each one selects a small piece of work. The famous case is an interpreter or VM with many small operations, or a CPU emulator, but it is not the only one: a protocol parser, a data-format decoder, a graphics display list, an event sequencer — anything shaped like *walk a byte stream, dispatch on each byte* is a candidate. Chapter 13 widens the lens well beyond interpreters; this section is the general test.

It is the wrong tool when there is no stream to walk — a single fixed computation, or code small enough to run natively — or when the "dispatch" is really just a table lookup with no per-symbol work to do (a plain `RDLUT` is cheaper than arming the engine). And it consumes resources: the dispatch table occupies LUT RAM, and handlers live in cog/LUT space (Chapter 8 covers the limits; §13.7 collects the anti-patterns).

::: tip
If you have written an interpreter before: XBYTE replaces your `next:` dispatch label — the `fetch / index / jump` you wrote by hand — with hardware. Your handlers stay yours; you delete the loop between them.
:::

To see what the engine makes possible in real, on-silicon projects — a single P2 emulating an 8-bit micro per cog while generating video and audio, and full console emulators — see **Appendix C: Further Implementations**; for the breadth of *non*-interpreter uses, see **Chapter 13: XBYTE Beyond Interpreters**.

# Chapter 2: The Skip Family {#ch-2}

XBYTE is built out of three related instructions: **SKIP**, **SKIPF**, and **EXECF**. They are useful on their own, and understanding them is the whole secret to understanding the engine — because XBYTE's dispatch *is* an EXECF, and its compact handlers are built with SKIPF. This chapter teaches the family first, as ordinary instructions. The engine in Part II then needs almost no new ideas.

All three take a pattern of bits and use it to *not execute* selected instructions. The difference is in *how* they skip and *what else* they do.

## 2.1 SKIP — cancel instructions in place {#sec-2-1}

**SKIP** takes a 32-bit pattern in D and, as the next up-to-32 instructions come down the pipeline, **cancels** each one whose corresponding bit is set. Bit 0 governs the first instruction after SKIP, bit 1 the second, and so on. A cancelled instruction still passes through the pipeline — it simply has no effect, taking its time but doing nothing.

```pasm2
                skip    ##%0000_0110        ' cancel the 2nd and 3rd
                                            ' following instructions
                add     x, #1               ' bit 0 = 0 -> runs
                add     x, #10              ' bit 1 = 1 -> cancelled
                add     x, #100             ' bit 2 = 1 -> cancelled
                add     x, #1000            ' bit 3 = 0 -> runs
```

Because a cancelled instruction still spends its clocks, SKIP's cost is the cost of the instructions it skips over. Its value is that one straight-line block of code can be made to behave like many different sequences, chosen by the pattern — the basis of a *shared handler*.

::: hardware
**SKIP works even in hub-executed code.** It is the general-purpose member of the family — it stays in the normal execution flow and cancels, rather than jumping. That makes it the one to reach for in hubexec, where SKIPF's PC-leap does not apply.
:::

## 2.2 SKIPF — leap the PC over instructions {#sec-2-2}

**SKIPF** is the *fast* skip. Instead of cancelling instructions one by one as they arrive, it makes the program counter **leap past** the skipped instructions entirely, in cog or LUT RAM. Where SKIP pays for what it skips, SKIPF skips for free — a run of skipped instructions costs essentially nothing, because the PC simply does not visit them.

```pasm2
                skipf   ##%0000_0110        ' leap over the 2nd and 3rd
                add     x, #1               ' runs
                add     x, #10              ' leapt over (no cost)
                add     x, #100             ' leapt over (no cost)
                add     x, #1000            ' runs
```

The trade for that speed is the restriction: SKIPF works in **cog and LUT RAM only** (the PC-leap needs the cog/LUT addressing), and its pattern is **22 bits** wide, governing the next 22 instructions. That width is not a coincidence — it is exactly the width XBYTE stores in each dispatch-table entry.

## 2.3 EXECF — jump, then skip {#sec-2-3}

**EXECF** is SKIPF with a jump bolted on. Its single operand D carries both:

- **D[9:0]** — a 10-bit cog/LUT address to **jump to**
- **D[31:10]** — a 22-bit **SKIPF pattern** to apply once there

So EXECF means: *go to this routine, and skip these instructions inside it.* One instruction, one operand, and you have selected both *which* code to run and *which variant* of it.

That is the entire mechanism of dispatch. If a table entry holds an EXECF operand — a handler address in the low 10 bits, a skip pattern in the high 22 — then "execute the operand" is exactly "run handler N in variant M." XBYTE's dispatch table is precisely a table of EXECF operands (Chapter 4), and the engine's core step is precisely an EXECF (Chapter 5).

| Instruction | Skips by | Also does | Pattern width | Works in |
|-------------|----------|-----------|---------------|----------|
| **SKIP**  | cancelling in place | — | 32 bits | cog, LUT, hub |
| **SKIPF** | leaping the PC | — | 22 bits | cog, LUT |
| **EXECF** | leaping the PC | jumps to D[9:0] first | 22 bits (D[31:10]) | cog, LUT |

## 2.4 One body, many bytecodes — the shared-handler idiom {#sec-2-4}

The reason the skip family matters to an interpreter is *code sharing*. Many bytecodes differ only slightly — "add," "subtract," "and," "or" might be one routine that loads two operands, performs one ALU operation, and stores the result, where only the middle instruction changes. Rather than write four routines, write one body containing all four ALU operations and give each bytecode a skip pattern that leaves *its* operation and skips the other three.

```pasm2
' One shared body for several two-operand ALU bytecodes.
' Each bytecode's dispatch entry supplies a SKIPF pattern that
' leaves exactly one of the four ALU lines and skips the rest.
alu_body
                call    #pop_two            ' operands -> a, b
                add     a, b                 ' "ADD" bytecode keeps this
                sub     a, b                 ' "SUB" bytecode keeps this
                and     a, b                 ' "AND" bytecode keeps this
                or      a, b                 ' "OR"  bytecode keeps this
        _ret_   call    #push_a              ' result -> stack, return
```

The bytecode that means "subtract" points at `alu_body` with a skip pattern that leaps the `add`, `and`, and `or` lines; "add" skips the other three; and so on. Four bytecodes, one body. This is the single most common XBYTE handler pattern, and it is pure SKIPF — the engine just supplies the pattern for you, from the table, on every bytecode.

::: tip
Design handler bodies so the *common* path has the fewest skips. Every kept instruction runs; every skipped one is free. A well-factored shared body can serve a dozen related bytecodes with one copy of the code.
:::

# Chapter 3: The Bytecode Stream {#ch-3}

XBYTE reads its bytecodes from the **hub FIFO** — the same fast, sequential hub-reading hardware every cog has. This chapter covers how the stream is primed and read, because a bytecode program is just bytes in hub memory, and the FIFO is how they reach the engine.

## 3.1 Priming the FIFO with RDFAST {#sec-3-1}

Before any bytecode can be fetched, the cog's FIFO must be pointed at the bytecode stream in hub memory. **RDFAST** does that: it begins a fast, sequential hub read starting at a given address.

```pasm2
                rdfast  #0, ##program       ' FIFO now streams bytes
                                            ' from 'program' onward
```

- **S** holds the hub start address (S[19:0]).
- **D** holds the block size in 64-byte units (D[13:0]); **0 means "no limit"** — the FIFO streams continuously, which is what an interpreter usually wants. D[31] is a no-wait flag.

After RDFAST, the FIFO delivers bytes in order, refilling from hub memory on its own.

::: caution
**Arm the FIFO before arming the engine.** XBYTE's very first action is an **RFBYTE** off the FIFO (Chapter 5). If RDFAST has not pointed the FIFO at your bytecode stream, that first fetch reads undefined data and the interpreter dispatches garbage. RDFAST first, then start XBYTE.
:::

## 3.2 Fetching bytecodes — RFBYTE {#sec-3-2}

**RFBYTE** reads the next byte from the FIFO, zero-extended, into D. It is the instruction XBYTE issues to fetch each bytecode.

```pasm2
                rfbyte  bytecode            ' next stream byte -> bytecode
```

RFBYTE is a 2-clock instruction. It optionally sets flags (C = the byte's MSB, Z if the byte is zero), though in XBYTE dispatch the engine manages flags itself (Chapter 7). Its companions **RFWORD** and **RFLONG** read a word or a long from the stream the same way — useful inside a handler that needs a fixed-size *inline operand* following the bytecode.

## 3.3 Variable-length operands — RFVAR and RFVARS {#sec-3-3}

Many bytecode formats follow an operation with an operand whose size varies — a small value takes one byte, a larger one takes more. The FIFO reads these directly:

- **RFVAR** reads a **zero-extended** 1-to-4-byte variable-length value into D (C is cleared).
- **RFVARS** reads a **sign-extended** 1-to-4-byte variable-length value into D (C = the value's MSB).

```pasm2
' Inside a "push constant" handler: the constant follows the
' bytecode in the stream as a variable-length value.
push_const
                rfvar   value               ' pull the inline constant
        _ret_   call    #push_value         ' onto the VM stack, return
```

Because the FIFO advances as it is read, a handler can pull as many inline operand bytes as the operation needs and the next RFBYTE — the next dispatch — naturally lands on the following bytecode. The stream stays self-describing: operations and their operands interleave, and the read position takes care of itself.

::: tip
Use **RFVAR** for unsigned operands (addresses, indices) and **RFVARS** for signed ones (relative branches, signed immediates). Choosing the right one means the value arrives already correctly extended — no masking or sign-fixing in the handler.
:::

## 3.4 The read pointer — GETPTR and PB {#sec-3-4}

Sometimes a handler needs to know *where* in hub memory the stream currently sits — to take a relative branch, or to compute a target address. **GETPTR** returns the FIFO's current hub pointer into D.

XBYTE makes this automatic: on every dispatch it writes the FIFO pointer into **PB** (`$1F7`), so a handler can read the current stream position from `PB` without issuing GETPTR itself. Between `PA` (the current bytecode, §4.3) and `PB` (the current stream pointer), a handler has both halves of its context handed to it for free.

# Chapter 4: LUT Dispatch {#ch-4}

The last piece before the engine itself is the **dispatch table**: how a bytecode becomes a handler address. XBYTE keeps this table in LUT RAM, and its design is the reason dispatch costs only a few clocks.

## 4.1 The table is 256 EXECF operands in LUT {#sec-4-1}

A cog's LUT is 512 longs. XBYTE uses a block of it — up to 256 longs — as the dispatch table, indexed by the bytecode. Bytecode `N` selects entry `N`. (Smaller tables are possible; Chapter 7 covers the size and compression options. The full-size case is 256 entries.)

Each entry is **one long**, and that long is an **EXECF operand** — exactly the operand Chapter 2 described:

- **bits [9:0]** — the handler's address in cog/LUT RAM
- **bits [31:10]** — the 22-bit SKIPF pattern applied on entry to the handler

The *Parallax Propeller 2 Documentation v35* states it directly: the table *"must consist of long data which EXECF would use, where the 10 LSBs are an address to jump to in cog/LUT RAM and the 22 MSBs are a SKIPF pattern to be applied."*

```{=latex}
\DiagLutEntry
```

::: caution
**Do not transpose the two fields.** The address is the **low** 10 bits; the skip pattern is the **high** 22 bits. A handler that lives at LUT address `$200` with no skipping has the entry `$0000_0200`, not the address shifted left. Build entries with the address in the low bits and the pattern shifted up by 10.
:::

## 4.2 Building a table entry {#sec-4-2}

Because an entry packs an address and a pattern, build it by OR-ing the two fields. Assemblers let you compute this at assembly time:

```pasm2
' A dispatch entry: jump to 'push_const', no skipping.
                long    push_const                 ' addr in [9:0],
                                                    ' pattern [31:10] = 0

' A shared-body entry: jump to 'alu_body', skip pattern selects SUB.
                long    alu_body | (sub_skip << 10) ' addr | (pattern<<10)
```

The handler address comes from the label; the skip pattern is whatever leaves the instructions that bytecode needs and skips the rest (the shared-handler idiom of §2.4). The table is just 256 such longs, loaded into LUT before the engine starts.

## 4.3 The bytecode is handed to you in PA {#sec-4-3}

When XBYTE dispatches bytecode `N`, it writes `N` into **PA** (`$1F6`) before the handler runs. The handler can therefore use the bytecode value itself as data — as an immediate operand, a small constant, or an index — without re-reading it.

This matters for **compression** (Chapter 7), where a group of bytecodes shares one table entry and the handler tells them apart by reading `PA`. It is also simply convenient: a "push small constant" family can encode the constant *in the bytecode* and read it straight from `PA`.

## 4.4 Dispatch, by hand {#sec-4-4}

Putting Chapters 2–4 together, here is the dispatch loop XBYTE automates — written by hand, so the engine in Chapter 5 holds no surprises:

```pasm2
nextbc                                      ' the hand-written loop
                rfbyte  index               ' fetch bytecode
                add     index, #tbl_base    ' index into the LUT table
                rdlut   entry, index        ' read the EXECF operand
                execf   entry               ' jump + skip = dispatch
' ... each handler ends with a jmp back to #nextbc ...
```

Read a byte, use it to index the table, read the entry, execute it. That is fetch-look-up-execute — the loop from §1.1, in four instructions. **XBYTE is this loop in hardware**, with the return folded in so handlers end in `_RET_` and the engine re-enters the loop on its own — it also writes the bytecode to `PA` and the stream pointer to `PB` along the way, which the hand-written version above does not. Chapter 5 walks the hardware version clock by clock.

# Part II: The XBYTE Engine

Part I built the pieces: the skip family, the FIFO stream, the LUT dispatch table. This part is the engine itself — the cycle that runs those pieces in hardware, the single instruction that arms it, the table-size and compression options that shape it, and the rules the handlers must follow. It is the reference for how XBYTE behaves.

# Chapter 5: The Dispatch Cycle {#ch-5}

XBYTE's dispatch is the hand-written loop of §4.4, executed by hardware as a fixed sequence. The *Parallax Propeller 2 Documentation v35* specifies it as an **8-clock** sequence with a **6-clock overhead** per bytecode. This chapter walks it clock by clock — not because you write any of it, but because knowing exactly what the engine touches, and when, is what lets you reason about `PA`, `PB`, the flags, and timing inside a handler.

## 5.1 The eight clocks {#sec-5-1}

Each bytecode dispatch runs this sequence. Clock 1 overlaps the `_RET_` that ended the previous handler, which is why the per-bytecode overhead is 6 clocks, not 8.

| Clock | XBYTE activity | What it means |
|-------|----------------|---------------|
| 1 | `RFBYTE` bytecode · `SKIPF #0` | fetch the next bytecode from the FIFO; cancel any leftover skip pattern from the previous bytecode |
| 2 | `MOV PA,`bytecode · `RDLUT` | write the bytecode to `PA` ($1F6); begin the table read indexed by it |
| 3 | `RDLUT` (data → D) | the table's EXECF operand arrives |
| 4 | `EXECF D` (begin) | start the dispatch jump-plus-skip |
| 5 | `MOV PB,`(GETPTR) · `MODCZ` · `EXECF D` (branch) | write the FIFO pointer to `PB` ($1F7); set C,Z from the index if enabled; take the branch |
| 6 | flush pipeline | the branch flushes the pipeline |
| 7 | reload pipeline | the pipeline reloads at the handler |
| 8 | first handler instruction | the handler's first instruction executes; on its closing `_RET_`/`RET`, loop to clock 1 |

The engine fetches, writes `PA`, looks up, writes `PB`, optionally sets flags, and branches — the entire fetch-look-up-execute loop — and hands control to your handler at clock 8.

```{=latex}
\DiagDispatchCycle
```

## 5.2 The overhead, exactly {#sec-5-2}

Three figures from the silicon documentation, stated precisely so they are not confused:

- **6 clocks** — the dispatch **overhead** per bytecode, *"including `_RET_` at the end of each bytecode routine."* This is the tax XBYTE charges; the handler's own work is on top of it.
- **9 clocks** — the overhead of the **software** equivalent (*"2+3+4, or 9, clocks to get the next bytecode, look it up, then execute that bytecode's routine"*). XBYTE's hardware saves the difference on every bytecode.
- **8 clocks** — the **minimum total loop**: a routine *"as short as a single 2-clock instruction with a `_RET_` prefix"* gives 6 overhead + 2 body.

::: hardware
These are **hardware dispatch** clocks — a property of the engine, measured against the P2's sysclk. They are not the run time of any particular interpreted language's methods, which depend on the handlers a given interpreter ships. The figure to cite for XBYTE is the 6-clock overhead.
:::

## 5.3 Flags and interruption {#sec-5-3}

At clock 5 the engine can write **C** and **Z** from the low bits of the bytecode index, when the **F bit** is set in the mode operand (Chapter 7). When F is clear, dispatch leaves the flags alone, so a handler can carry flag state across bytecodes deliberately.

XBYTE is also **interruptible**: an interrupt can occur during dispatch, and the engine resumes the bytecode stream afterward. Bytecode interpretation does not lock out a cog's interrupts.

# Chapter 6: Arming XBYTE {#ch-6}

Starting the engine is a single instruction — but it is an unusual one, because it does two things at once and relies on a value already sitting on the hardware stack. This chapter covers the arming sequence, the `$1FF` convention, and the persistent-vs-one-shot choice.

## 6.1 One instruction, with $1FF on the stack {#sec-6-1}

The *Parallax Propeller 2 Documentation v35* puts it plainly: *"Starting XBYTE and establishing its operating mode is done all at once by a `_RET_ SETQ {#}D` instruction, with the top of the hardware stack holding `$1FF`."*

So arming XBYTE takes two things in place:

1. **`$1FF` on top of the hardware stack** — this is the address every bytecode routine "returns to." When a handler ends in `RET`/`_RET_`, the return target `$1FF` is what triggers the engine to fetch and dispatch the next bytecode.
2. **A `_RET_ SETQ {#}D`** — the `_RET_` prefix performs the return (consuming the `$1FF`) and, in the same step, **SETQ** loads the **mode operand** D that configures the engine.

```pasm2
                rdfast  #0, ##program       ' 1. point the FIFO at the
                                            '    bytecode stream
                push    #$1ff               ' 2. return target for every
                                            '    bytecode routine
        _ret_   setq    #$100               ' 3. arm: 256-entry EXECF
                                            '    table at LUT $100 — XBYTE
                                            '    starts now
```

After that `_ret_ setq`, the engine is running: it fetches the first bytecode and dispatches it, and keeps going until stopped.

::: caution
**The `$1FF` must be on the stack before the arming `_RET_`.** Without it, the `_RET_` returns somewhere else and the engine never engages. The usual idiom is an explicit `PUSH #$1FF` (or arriving via a `CALL` whose return address is `$1FF`) immediately before the `_ret_ setq`.
:::

## 6.2 The mode operand {#sec-6-2}

The D value handed to SETQ is the **mode operand**. It packs three independent choices, all detailed in Chapter 7:

- the **table base address** in LUT (the high bits),
- the **table size / compression** selection (which bit pattern), and
- the **F bit** (bit 0) — whether dispatch writes the flags.

For a full 256-entry table at LUT base `$100` with flags untouched, the operand is `$100` — table base in the high bits, the size/F bits clear. Chapter 7 is the full map.

## 6.3 Persistent vs one-shot — SETQ and SETQ2 {#sec-6-3}

There are two arming instructions, and the choice between them is **orthogonal** to the operand value. The operand says *how* to dispatch; SETQ-vs-SETQ2 says *for how long*:

- **SETQ** arms the **persistent** mode. The configuration is retained and applies to **every** subsequent bytecode. This is how you start the engine and how it stays running.
- **SETQ2** arms a **one-shot** mode that applies to **exactly the next bytecode**, after which the engine automatically reverts to the mode last set by SETQ — *"without having to restore the original XBYTE mode afterwards."*

The one-shot form lets a VM keep a default dispatch table and *borrow* an alternate table for a single bytecode at a time. The classic use is a **prefix bytecode**: a bytecode whose handler issues `_ret_ setq2` to select an alternate table, so the *following* bytecode dispatches through that alternate table and then control returns to the default. This is exactly how a guest CPU's "extended opcode" pages are handled — the subject of the 6809 vignette in Chapter 12.

| | SETQ | SETQ2 |
|---|------|-------|
| Persistence | persistent — every bytecode | one-shot — the next bytecode only |
| After it fires | stays in effect | reverts to the last SETQ mode |
| Typical use | arm and run the engine | a prefix/alternate-table bytecode |

::: tip
The "2" in SETQ2 is the alternate/one-shot form throughout the instruction set — the same personality split as the block-move SETQ/SETQ2. If you remember "SETQ2 = the temporary one," you will reach for the right one when building a prefix bytecode.
:::

# Chapter 7: Table-Size & Compression Modes {#ch-7}

A bytecode set rarely needs all 256 codes, and LUT RAM is shared with everything else a cog does. XBYTE therefore supports smaller dispatch tables and a compression scheme, all selected by the **mode operand** handed to SETQ/SETQ2. This chapter is the reference for those modes and for the **F bit**.

## 7.1 Reading the mode operand {#sec-7-1}

The mode operand is written `%A...F` — a high field **A** that sets the LUT base address, a middle pattern that selects the table size, and the low **F** bit for flag writing. The same value chooses table base, size/compression, and flags at once. The table below is the full set from the *Parallax Propeller 2 Documentation v35*.

```{=latex}
\DiagModeOperand
```

## 7.2 Table sizes {#sec-7-2}

| LUT size | Index bits | Operand pattern | LUT base | Index from bytecode |
|----------|-----------|-----------------|----------|---------------------|
| **256** | 8 | `%A000000`*x*`F` | `%A00000000` | I = b[7:0] |
| **128** | 7 | `%AAxx0010F` | `%AA0000000` | I = b[6:0] |
| **64**  | 6 | `%AAAx1010F` | `%AAA000000` | I = b[5:0] |
| **32**  | 5 | `%AAAAx100F` | `%AAAA00000` | I = b[4:0] |
| **16**  | 4 | `%AAAAA110F` | `%AAAAA0000` | I = b[3:0] |

The more **A** bits the operand carries, the higher the LUT base can sit and the smaller the table — a 16-entry table needs only 4 index bits, so the other bits position it. Each size also has an **alternate** form that indexes from the bytecode's *high* bits instead of its low bits (for example, 128-entry `%AAxx0011F` indexes by b[7:1]); these let the dispatch key on the top of the bytecode while the low bits stay free as an operand in `PA`. Appendix A tabulates every form.

## 7.3 Compression — 16 primary plus 240 extended {#sec-7-3}

The 256-entry mode has a compression option, written `%ABBBB00xF` with the 4-bit threshold **BBBB** greater than zero. It lets *"sets of 16 bytecodes, which would use identical LUT values, … be represented by a single LUT value, effectively compressing blocks of 16 LUT values into single LUT values."*

The rule is on the bytecode's high nibble:

- if **b[7:4] < BBBB**, the bytecode indexes the table normally (I = b[7:0]) — these are the **primary** bytecodes, each with its own entry;
- if **b[7:4] ≥ BBBB**, the whole group of 16 that shares that high nibble maps to a **single** entry — these are the **extended** bytecodes.

This is most useful *"when the bytecode, which is always written to PA, is used as an operand within the bytecode routine."* A family like "push constant 0..15" can be 16 bytecodes that share one handler — the handler reads the actual value from `PA`. Sixteen opcodes, one table entry, one routine.

## 7.4 The F bit — flags from the bytecode {#sec-7-4}

Bit 0 of the mode operand is the **F bit**:

- **F = 0** — dispatch does not affect C or Z; flag state carries across bytecodes.
- **F = 1** — at clock 5, dispatch writes **C = bytecode index bit 1** and **Z = bytecode index bit 0**.

Setting F lets a routine *"differentiate behavior within a bytecode routine, especially in cases of conditional looping, where a SKIPF pattern would have been insufficient, on its own."* In other words, when one handler must behave four slightly different ways and a skip pattern cannot express the difference, encode two selector bits in the bytecode's low bits and let the flags carry them in.

::: hardware
The F bit and the SKIPF pattern are complementary selectors. The skip pattern chooses *which instructions* a handler runs; the flags (via F) let those instructions *branch* on two bits of the bytecode. Compression, the SKIPF pattern, and the F bit together are how a small table serves a large, regular bytecode set.
:::

# Chapter 8: Bytecode Routines {#ch-8}

The handlers are the code you write. XBYTE runs the loop between them, but the routines themselves must follow a few rules so the engine can re-enter cleanly. This chapter collects those rules and the idioms that come from them.

## 8.1 The rules a routine follows {#sec-8-1}

| Rule | Why |
|------|-----|
| Live in **cog or LUT RAM** | dispatch is an EXECF jump to a 10-bit cog/LUT address; hub-resident routines cannot be the EXECF target |
| End in **RET** or **`_RET_`** | the return to `$1FF` is what tells the engine to fetch the next bytecode |
| Respect the **hardware stack** (8 levels) | nested `CALL`s inside a handler share the cog's 8-level stack; overflowing it corrupts returns |

Within those rules a handler is ordinary PASM2. It can call subroutines, read and write hub, drive pins — anything a cog can do — as long as it returns to `$1FF` when done.

::: caution
**Watch the stack depth.** XBYTE's re-entry rides on the hardware stack, and the stack is only 8 levels deep. A handler that calls a subroutine that calls another is fine; one that recurses deeply, or leaves calls unbalanced, will exhaust the stack and break dispatch. Keep handler call chains shallow.
:::

## 8.2 The bytecode as an operand — PA {#sec-8-2}

Because the engine writes the bytecode to **PA** (`$1F6`) before the handler runs, the handler can use the bytecode itself as data. This is what makes compression (§7.3) and the small-constant idiom work:

```pasm2
' "push small constant 0..15" — 16 bytecodes, one entry, one routine.
' The value lives in the low nibble of the bytecode, read from PA.
push_small
                mov     value, pa
                and     value, #$0f         ' the constant is in PA[3:0]
        _ret_   call    #push_value         ' onto the VM stack, return
```

## 8.3 Inline operands — the FIFO and PB {#sec-8-3}

A handler that needs a larger operand pulls it from the **FIFO**, which is sitting on the byte right after the bytecode (§3.3). Reading it with RFVAR/RFVARS/RFLONG advances the stream so the next dispatch lands correctly:

```pasm2
' "jump relative" — a signed offset follows the bytecode in the stream.
jmp_rel
                rfvars  offset              ' signed inline operand
                getptr  ptr                 ' or read PB for current pos
                add     ptr, offset
        _ret_   rdfast  #0, ptr             ' re-point the FIFO -> branch
```

Re-pointing the FIFO with RDFAST is how a guest "branch" works under XBYTE: change where the stream reads from, and the next bytecode comes from the new location. `PB` gives the handler the current position to compute the target from.

## 8.4 Stopping the engine {#sec-8-4}

XBYTE runs until a handler chooses **not** to return to `$1FF`. A "halt" bytecode's handler simply does not end in the dispatch-continuing return — it branches to ordinary code instead, leaving the engine. That is the clean way to exit: one bytecode whose handler jumps out of the loop rather than back into it.

# Part III: Building a VM

Parts I and II explained the engine. This part proves it by building. Chapter 9 builds a complete, working bytecode VM from nothing — the smallest thing that exercises the whole engine. Chapter 10 steps back to ask which *guest CPUs* map well onto XBYTE and which fight it. Chapters 11 and 12 then build a tiny illustrative 6502 emulator and a 6809 vignette that shows the one-shot SETQ2 trick. Chapter 13 closes the part by widening the frame off of interpreters entirely — the same engine parsing protocols, decoding formats, and driving displays.

Everything in this part is **tiny and illustrative** — sized to show a technique end to end and to compile, not to be a faithful or complete implementation. That is a deliberate charter, restated where it matters.

# Chapter 9: A Minimal Custom VM {#ch-9}

The smallest useful XBYTE program is a stack machine with a handful of bytecodes. Building it touches every part of the engine once: load a dispatch table into LUT, point the FIFO at a bytecode program, arm the engine, and write a few handlers. This chapter is that build, complete.

## 9.1 The instruction set {#sec-9-1}

Four bytecodes are enough to be a real VM:

| Bytecode | Name | Action |
|----------|------|--------|
| `$00` | `PUSHC` | read a variable-length constant from the stream, push it |
| `$01` | `ADD` | pop two, push their sum |
| `$02` | `SUB` | pop two, push their difference |
| `$03` | `HALT` | leave the engine |

The VM stack is a few longs of cog memory with a pointer. `PUSHC` uses an inline operand (§3.3); `ADD` and `SUB` are a shared body candidate (§2.4), but are written separately here for clarity.

## 9.2 The complete program {#sec-9-2}

```spin2
CON
  _clkfreq = 200_000_000

DAT
                org

' ---- start the VM -------------------------------------------------
start
                setq2   #4-1                ' load 4 longs into LUT $000..
                rdlong  $000, ##disp_table  ' the dispatch table
                rdfast  #0, ##program       ' FIFO -> bytecode stream
                push    #$1ff               ' return target per bytecode
        _ret_   setq    #0                  ' arm: 256-entry table @ LUT
                                            ' $000, F=0 — XBYTE starts now
' XBYTE now runs the stream; control reaches 'done' only via HALT.
done
                jmp     #done               ' park the cog

' ---- bytecode handlers (cog-resident) -----------------------------
h_pushc                                     ' $00: push inline constant
                rfvar   v
                wrlong  v, sp
        _ret_   add     sp, #4

h_add                                       ' $01: pop b, a; push a+b
                sub     sp, #4
                rdlong  b, sp
                sub     sp, #4
                rdlong  a, sp
                add     a, b
                wrlong  a, sp
        _ret_   add     sp, #4

h_sub                                       ' $02: pop b, a; push a-b
                sub     sp, #4
                rdlong  b, sp
                sub     sp, #4
                rdlong  a, sp
                sub     a, b
                wrlong  a, sp
        _ret_   add     sp, #4

h_halt          jmp     #done               ' $03: exit XBYTE

' ---- cog variables ------------------------------------------------
sp              long    stack                ' VM stack pointer (hub)
v               res     1
a               res     1
b               res     1

' ---- hub data: dispatch table, program, stack ---------------------
                orgh
disp_table      long    h_pushc             ' entry $00 -> PUSHC
                long    h_add               ' entry $01 -> ADD
                long    h_sub               ' entry $02 -> SUB
                long    h_halt              ' entry $03 -> HALT

program         byte    $00, 7              ' PUSHC 7
                byte    $00, 5              ' PUSHC 5
                byte    $01                 ' ADD      -> 12
                byte    $00, 3              ' PUSHC 3
                byte    $02                 ' SUB      -> 9
                byte    $03                 ' HALT

stack           long    0[16]               ' VM stack lives in hub
```

That is a working XBYTE VM. The dispatch table is four longs in hub, loaded into LUT `$000` with `setq2`+`rdlong`; each entry is a handler's cog address with a zero skip pattern, so no SKIPF is needed here. The program is a byte stream in hub; `rdfast` points the FIFO at it. The `_ret_ setq #0` arms the simplest mode — a 256-entry table at LUT base `$000`, flags off; only the first four entries are populated because the program uses only bytecodes `$00`–`$03`. The engine runs until `HALT`'s handler jumps to `done`.

::: hardware
**Why the table entries are just handler addresses.** With no skipping, an entry's SKIPF pattern (bits [31:10]) is zero, so the long is simply the handler's cog address in bits [9:0]. The moment you adopt the shared-handler idiom (§2.4), those high bits fill with per-bytecode skip patterns — see §9.3.
:::

## 9.3 Folding ADD and SUB into a shared body {#sec-9-3}

`ADD` and `SUB` differ by one instruction. Per §2.4 they can share a body, with each bytecode's table entry carrying the skip pattern that selects its operation:

```pasm2
alu                                         ' shared ADD/SUB body
                sub     sp, #4
                rdlong  b, sp
                sub     sp, #4
                rdlong  a, sp
                add     a, b                 ' kept by ADD, skipped by SUB
                sub     a, b                 ' kept by SUB, skipped by ADD
                wrlong  a, sp
        _ret_   add     sp, #4
```

`ADD`'s entry skips the `sub a,b` line; `SUB`'s entry skips the `add a,b` line. The table changes from two handler addresses to two `alu`-with-pattern entries; the body exists once. For two bytecodes the saving is small, but for a dozen ALU operations it is the difference between one routine and a dozen.

# Chapter 10: Mapping CPU Families onto XBYTE {#ch-10}

XBYTE was built for byte-stream bytecode, and emulating a CPU is exactly that — *if* the guest's instructions are a byte stream. This chapter is the design judgement that comes before any emulator: how well a given processor's instruction shape fits the engine, and where you adapt. It is the reasoning behind choosing the 6502 for this guide's capstone.

## 10.1 The two assets XBYTE offers {#sec-10-1}

XBYTE gives an emulator two separable things:

1. **Auto-fetch** — the FIFO pulls the next byte and the engine dispatches it with no software in the loop. This fits any guest whose instructions are a **byte stream read in order**.
2. **Table/EXECF dispatch** — a single indexed jump-plus-skip selects the handler. This fits any guest with a **first-byte opcode** that can index a table.

A guest CPU uses *both* assets when its instructions are byte-stream, opcode-first. The further a guest departs from that shape, the more of the engine you supply by hand.

## 10.2 Where families fall {#sec-10-2}

| Guest family | Instruction shape | Fit with XBYTE |
|--------------|-------------------|----------------|
| **8-bit micros** (6502, 6809, 8080, Z80, 8051) | byte stream, opcode first | the sweet spot — auto-fetch *and* table dispatch both apply directly |
| **Word-opcode CISC** (68000) | 16-bit opcode words + extension words | dispatch on the opcode word via a table; auto-fetch is partial — read the word with `RFWORD`, decode further by hand |
| **Variable-length CISC** (x86) | prefixes, escape bytes, ModR/M, SIB | the byte stream fits; the *decode* explodes — prefixes and escapes are a job for one-shot SETQ2 alternate tables, and the long tail is hand-rolled |
| **Fixed-width RISC** (MIPS, ARM) | 32-bit instruction words, bit-field decode | no byte stream — read the word with `RFLONG` and dispatch on an extracted opcode field; table dispatch helps, auto-fetch does not |

The pattern is clear: **the more byte-stream-and-opcode-first a guest is, the more XBYTE does for you.** An 8-bit micro is the case where the engine does almost everything; a fixed-width RISC is the case where you use the dispatch table but feed it yourself.

## 10.3 Why the 6502 {#sec-10-3}

The capstone in Chapter 11 is the **6502**, for reasons this chapter's framework makes concrete:

- **Byte-stream, opcode-first.** Every 6502 instruction begins with a one-byte opcode, followed by 0–2 operand bytes — exactly auto-fetch's sweet spot. `RFBYTE` fetches the opcode; `RFVAR`/`RFVARS` pull the operands.
- **A table that fits.** The 6502 defines ~151 of 256 opcodes; a 256-entry dispatch table maps them directly, one bytecode per opcode.
- **Regular families.** Addressing modes and ALU operations are regular enough that the shared-handler idiom (§2.4) collapses many opcodes onto a few bodies — a natural showcase for SKIPF patterns.
- **Recognizable and tractable.** It is small enough to build illustratively and famous enough to be worth recognizing.

The **8080/Z80** and **8051** fit equally well and would make fine alternates; the 6502 is chosen for familiarity. The **6809** appears in Chapter 12 specifically because its `$10`/`$11` prefix pages are the perfect, minimal demonstration of one-shot SETQ2 dispatch.

# Chapter 11: A Tiny CPU Emulator (6502) {#ch-11}

This chapter builds an illustrative slice of a 6502 on XBYTE — enough opcodes to show how a real CPU's instructions become bytecode handlers, and how the engine's pieces (PA, the FIFO, the shared body, the skip pattern) carry the emulation. It is **not** a complete or cycle-accurate 6502, by charter; it is the technique, shown end to end on a representative handful of instructions.

## 11.1 The mapping {#sec-11-1}

In a 6502 emulator the correspondence is direct:

| 6502 concept | XBYTE realization |
|--------------|-------------------|
| the opcode byte | the **bytecode** — fetched by the engine, handed to the handler in `PA` |
| operand bytes (immediate, address) | **inline operands** — `RFVAR`/`RFVARS` off the FIFO |
| the opcode → microcode decode | the **dispatch table** — one entry per opcode |
| the program counter | the **FIFO read position** — advanced by reads, re-pointed by `RDFAST` on a branch |
| A, X, Y, S, P registers | cog registers |

The guest's program counter *is* the FIFO position, which is the single most elegant part of the fit: incrementing the PC is free (the FIFO advances as it reads), and a branch is a `RDFAST` to the new address.

## 11.2 Register file and dispatch {#sec-11-2}

The 6502 register set is a few cog longs, and arming is the same sequence as Chapter 9 — a 256-entry table for the full opcode space:

```pasm2
                setq2   ##256-1             ' load 256 longs into LUT
                rdlong  $100, ##op_table    ' the opcode dispatch table,
                                            ' LUT $100..$1FF
                rdfast  #0, ##reset_vector  ' FIFO -> 6502 code in hub
                push    #$1ff
        _ret_   setq    #$100               ' 256-entry table @ LUT $100,
                                            ' F=0 (see Ch.7 for the operand)
```

Each opcode that the slice implements gets a table entry pointing at its handler; unimplemented opcodes point at a shared `op_undef` that flags the gap. (A real build fills all 256; this slice fills the few below and routes the rest to `op_undef`.)

## 11.3 Representative handlers {#sec-11-3}

**`LDA #imm` ($A9)** — load the accumulator with an immediate. The operand byte follows the opcode in the stream; N and Z flags are set from the result.

```pasm2
op_lda_imm                                  ' $A9: LDA #immediate
                rfbyte  a                   ' inline operand -> A
        _ret_   call    #set_nz             ' update N,Z; return to dispatch
```

**`INX` ($E8)** — increment X, a single-byte instruction with no operand, flags from the result. The mask keeps the guest register 8-bit.

```pasm2
op_inx                                      ' $E8: INX
                add     x, #1
                and     x, #$ff             ' 6502 X is 8-bit
        _ret_   call    #set_nz             ' update N,Z; return to dispatch
```

**`JMP abs` ($4C)** — an absolute jump: read the 16-bit target from the stream, then re-point the FIFO at it. This is where "the PC is the FIFO position" pays off.

```pasm2
op_jmp_abs                                  ' $4C: JMP $hhll
                rfword  target              ' 16-bit absolute address
        _ret_   rdfast  #0, target          ' FIFO -> target = the branch
```

The shared-body idiom collapses the 6502's many ALU and load/store opcodes the way §9.3 collapsed ADD/SUB: one body per family (loads, ALU ops, branches), with each opcode's table entry supplying the SKIPF pattern and, where four-way behavior is needed, the F bit (§7.4) carrying two opcode bits into the flags.

## 11.4 What this slice shows, and what it omits {#sec-11-4}

The slice demonstrates the full technique: opcode-as-bytecode, operands from the FIFO, PC-as-FIFO-position, branches as `RDFAST`, and shared bodies for regular families. A faithful 6502 adds the rest of the opcode table, the full addressing-mode matrix, decimal mode, correct flag semantics on every operation, and accurate timing — none of which change the XBYTE technique, all of which are deliberately out of scope here. The point is the shape of the solution, not a finished emulator.

# Chapter 12: The 6809 SETQ2 Vignette {#ch-12}

One XBYTE feature has not yet earned its keep in an example: the one-shot **SETQ2** mode (§6.3). The 6809 is the cleanest small demonstration of why it exists, so it appears here as a short vignette — not a second emulator, just the one trick.

## 12.1 The problem: prefix pages {#sec-12-1}

The Motorola 6809 extends its opcode space with two **prefix bytes**, `$10` and `$11`. An opcode introduced by `$10` belongs to "page 2"; one introduced by `$11` belongs to "page 3". The same second byte means different things depending on which prefix — if any — preceded it. A flat 256-entry table cannot express that: byte `$83` is one instruction on page 1 and another on page 2.

## 12.2 The solution: a one-shot alternate table {#sec-12-2}

This is exactly what one-shot SETQ2 is for. Keep the page-1 table as the persistent mode (armed once with SETQ). Make `$10` and `$11` *prefix bytecodes* whose handlers do nothing but select the matching alternate table **for the next bytecode only**:

```pasm2
op_page2                                    ' $10: select page-2 table
        _ret_   setq2   #page2_mode         ' next bytecode dispatches
                                            ' through page 2, then reverts

op_page3                                    ' $11: select page-3 table
        _ret_   setq2   #page3_mode         ' next bytecode dispatches
                                            ' through page 3, then reverts
```

When the 6809 stream contains `$10 $83`, the `$10` handler arms the page-2 table one-shot; the `$83` that follows dispatches through page 2; and the engine then reverts to page 1 on its own — *"without having to restore the original XBYTE mode afterwards."* No flag to clear, no mode to put back. The prefix byte costs one dispatch, and the alternate page is in effect for exactly the one opcode that needs it.

::: tip
This is the general pattern for **any** guest with escape/prefix opcodes — the 6809's pages, the Z80's `$CB`/`$ED` prefixes, the x86 `$0F` escape. Each prefix becomes a one-shot-SETQ2 handler that points at the alternate table for that page. SETQ2's automatic revert is what makes it free.
:::

# Chapter 13: XBYTE Beyond Interpreters {#ch-13}

Parts I–III taught XBYTE as the engine under a language or a CPU, because that is what it was built for and where it shines. But strip the word "bytecode" away and the machine is more general: **XBYTE is hardware table-driven dispatch over a byte stream.** It reads the next byte, indexes a table, jumps to a handler, and loops — and nothing in that sentence requires the stream to be a *program*. Any problem shaped like *walk a stream of bytes, and for each one do one of a small set of things* can ride the same six-clock loop. This chapter widens the lens: the engine that runs a VM will also parse a protocol, decode a format, drive a display, or sequence a show.

## 13.1 Two assets, three widening features {#sec-13-1}

Chapter 10 named XBYTE's **two separable assets** for a CPU emulator; they are just as useful outside emulation:

- **Auto-fetch** — the FIFO pulls the next byte and dispatch happens with no software in the loop. Any *ordered byte stream* gets this.
- **Table/EXECF dispatch** — one indexed jump-plus-skip selects the handler. Any *first-byte selector* gets this.

An application draws on whatever mix of the two its data calls for. Three features you have already met turn that mix into a wide range of uses:

| Feature | Taught in | What it unlocks |
|---------|-----------|-----------------|
| **The byte *is* data** — it lands in `PA`, and compression lets a group share one handler | §4.3, §7.3, §8.2 | the symbol doubles as an operand or index: a channel number, a small constant, a packed length |
| **The table *is* state** — `SETQ2` borrows an alternate table for one byte; `SETQ` swaps it for good | §6.3 | escape and prefix bytes, mode shifts, whole state machines: change the table, change what the machine *is* |
| **The stream can *seek*** — `PB` gives the position, `RDFAST` re-points it | §3.4, §8.3 | loops, jumps, replays, back-references: the read cursor is a free, movable "program counter" |

The rest of the chapter applies these to problems that are not interpreters — with the same honest fit-grading Chapter 10 used for CPUs, because the engine helps some of them far more than others.

## 13.2 The application map {#sec-13-2}

A survey of where XBYTE earns its keep beyond languages and CPUs. Fit is graded **★** (strong — both assets plus a feature), **◑** (partial — leans on one asset), **○** (marginal — the dispatch is really just a lookup).

| Application | The stream is… | Main lever | Fit |
|-------------|----------------|------------|-----|
| **Terminal / ANSI (VT100) reader** | characters + escape sequences | table-as-state (`ESC` → one-shot table) | ★ |
| **MIDI stream engine** | status + data bytes | byte-as-data (channel in `PA`) | ★ |
| **Graphics display list** | draw commands + inline coordinates | seek + auto-fetch | ★ |
| **Binary format / TLV decoder** (MessagePack, CBOR) | type-tagged records | byte-as-data (the type tag) | ★ |
| **Event / timeline sequencer** (LED art, tracker, animatronics) | time-ordered events | seek (loop / branch) | ★ |
| **Stream decompression** (multi-code RLE, packed sprites) | control tokens + payload | auto-fetch — dispatch pays only with *many* codes | ◑ |
| **Inter-cog command coprocessor** | a live command ring | dispatch — the stream is live, not stored | ◑ |
| **Lexer / protocol state machine** | input symbols | table-as-state, one table per DFA state (advanced) | ◑ |
| **Forth inner interpreter** | a threaded word stream | both — but interpreter-adjacent | ◑ |
| **Charset map / Morse / template expand** | symbols → output | ○ — a plain `RDLUT` wins unless there is real per-symbol work |

The three sketches that follow take one ★ case for each widening feature. Each is **tiny and illustrative** — a handful of handlers to show the shape, not a finished driver — the same charter as the rest of Part III.

## 13.3 A terminal reader — the table as state {#sec-13-3}

A serial terminal receives a stream of output bytes. Most are printable characters to place on screen; a few are controls, and one — `$1B`, `ESC` — announces that *the next byte begins an escape sequence* that must be read from a different set of rules. That is exactly one-shot `SETQ2` (§6.3): the `ESC` handler borrows an escape table for the single byte that follows, and the engine reverts to the text table on its own.

```pasm2
h_print                                     ' most bytes: emit the char
                wrbyte  pa, scrnptr         ' PA holds the current byte
        _ret_   add     scrnptr, #1

h_esc                                       ' $1B: arm the escape table
        _ret_   setq2   #esc_mode           ' next byte only, then reverts
```

The elegance is what is *absent*. A hand-written terminal keeps an "am I in an escape?" flag and branches on it for every byte; here there is no flag and no branch. `ESC` shifts the machine for exactly one dispatch, and normal text resumes with no code to put the state back. A multi-byte sequence (`ESC [ 3 1 m`) chains the same trick — each state's handler arms the table for the next byte — so the parser *is* its table set, not a tangle of conditionals.

::: tip
The reverting one-shot is the whole reason this stays clean. If a sequence needs to hold an alternate table across several bytes, arm it with persistent `SETQ` on the way in and re-arm the base table on the way out — `SETQ2` for a one-byte shift, `SETQ` for a mode you stay in.
:::

## 13.4 A MIDI dispatcher — the byte as data {#sec-13-4}

MIDI is a byte stream whose **status byte** packs two fields: the high nibble is the command (`$9`_n_ = Note On, `$8`_n_ = Note Off, `$B`_n_ = Control Change, …) and the low nibble is the channel. XBYTE hands the whole status byte to the handler in `PA`, so the command *selects* the handler while the channel *rides along* as data in the same byte:

```pasm2
h_note_on                                   ' $9n: Note On, channel n
                mov     chan, pa
                and     chan, #$0f          ' channel is PA[3:0]
                rfbyte  note                ' data byte 1: note number
                rfbyte  vel                 ' data byte 2: velocity
        _ret_   call    #voice_on           ' start the voice, return
```

This is "the byte is both the selector and an operand" in its cleanest form. Because the eight commands live in the *high* nibble, the alternate high-bit index of a 16-entry table (§7.2) dispatches straight on the command with the channel falling out in `PA[3:0]` — sixteen entries cover every voice message, and the channel never costs a fetch. Running status (a data byte arriving with no fresh status byte, meaning "same command as last time") is a natural extension: a data-valued byte re-enters the current command's handler, and the FIFO's self-advancing read keeps the note/velocity pairs aligned.

## 13.5 A display list — the stream as a movable cursor {#sec-13-5}

A **display list** is a stream of drawing commands — set a color, move the pen, draw a run — that a renderer walks once per frame. Each command byte selects a primitive; its parameters follow inline in the stream, pulled with the FIFO reads of Chapter 3. And because the FIFO position *is* the list cursor (§8.3), a "repeat" or "jump" command is nothing but an `RDFAST` to a new address — the very mechanism a guest CPU's branch used in Chapter 11, here doing ordinary graphics:

```pasm2
h_moveto                                    ' set the pen position
                rfword  penx                ' inline X (16-bit)
        _ret_   rfword  peny                ' inline Y (16-bit), return

h_setcolor                                  ' load the current color
        _ret_   rfvar   pencol              ' inline color, return

h_loop                                      ' restart: re-point the FIFO
        _ret_   rdfast  #0, ##displaylist   ' stream resumes from the top
```

The command stream is *data you emit*, not a program you compile — a scene, a sprite list, a UI layout — yet the engine walks it with the same auto-fetch and dispatch a language gets. This is the mental shift the chapter turns on: XBYTE runs bytecode, and a display list is just bytecode whose "instructions" draw.

::: hardware
The FIFO reads (`RFWORD`, `RFVAR`) that pull a command's parameters advance the same read cursor the next dispatch fetches from, so operations and their operands interleave in one stream and the read position takes care of itself — exactly as it did for inline VM operands (§3.3) and guest-CPU operand bytes (§11.1). One mechanism, three very different uses.
:::

## 13.6 SETQ2 is a general mode switch {#sec-13-6}

Chapter 12 introduced one-shot `SETQ2` through the 6809's prefix pages, where it can read as a CPU-emulation trick. It is neither a trick nor about CPUs. `SETQ2` is the general operation *"dispatch the next byte through a different table, then restore mine"* — and every escape or mode shift in a byte stream is an instance of it:

- the **6809** `$10` / `$11` prefix pages (Chapter 12),
- an **ANSI terminal**'s `ESC` (§13.3),
- **MIDI** System Exclusive, where `$F0` opens a manufacturer data block a different table consumes,
- the **Z80** `$CB` / `$ED` and **x86** `$0F` escape prefixes (§10.2).

It is also how Parallax's own **Spin2 interpreter** works internally: the interpreter uses one-shot `SETQ2` to reach a whole family of *variable-operator* bytecodes through an alternate table, then reverts — the persistent table never has to hold room for them. When you meet a stream where "the next thing means something different," `SETQ2` is the answer, and its automatic revert (§6.3) is what makes the shift free.

## 13.7 When XBYTE is the wrong tool {#sec-13-7}

The engine is not free, and some stream-shaped problems still do not want it. Reach for something else when:

| The situation | Why XBYTE does not help | Use instead |
|---------------|-------------------------|-------------|
| There is no ordered byte stream to walk | auto-fetch has nothing to fetch | a plain loop over the data |
| The stream has one fixed record format | the many-way table sits idle — you only use auto-fetch | the FIFO reads (`RDFAST` + `RFxxxx`) directly, no engine |
| Each symbol maps straight to output, no logic | dispatch is just a lookup | a `RDLUT` per byte is cheaper than arming the engine |
| The state changes on nearly every symbol | constant `SETQ`/`SETQ2` re-arming outweighs the saved dispatch | a conventional `RDLUT`-plus-branch state loop |
| The unit is a fixed-width word, not a byte | the byte-stream auto-fetch does not apply (the RISC case, §10.2) | read the word with `RFLONG`, dispatch on an extracted field |

The through-line is Chapter 10's two-asset test, generalized: XBYTE pays when you use *both* auto-fetch and many-way dispatch, and at least one of the three widening features. Use fewer of them and a simpler loop will match it without spending LUT RAM on a table.

::: tip
A quick decision rule: if you can describe the job as *"read a byte, pick one of many things to do, repeat"* — and the pick is not a trivial lookup — XBYTE fits. The more the byte doubles as data, the table doubles as state, or the cursor moves, the better the fit.
:::

# Part IV: Reference

This part is for lookup. Chapter 14 is the per-instruction reference for everything XBYTE is built from; Chapter 15 collects the configuration values — the mode-operand layout, the registers, and the memory ranges — in one place. The appendices that follow add quick-reference cards, the encoding summary, pointers to community implementations, and troubleshooting.

# Chapter 14: Instruction Reference {#ch-14}

The instructions XBYTE uses, grouped by role. Encodings are given in the P2's `EEEE` form (the leading `EEEE` is the condition field). All are 2-clock instructions except **EXECF** (4 clocks).

## 14.1 The skip family {#sec-14-1}

| Instruction | Syntax | Encoding | Effect |
|-------------|--------|----------|--------|
| **SKIP** | `SKIP {#}D` | `EEEE 1101011 00L DDDDDDDDD 000110001` | Cancel each of the next up-to-32 instructions whose bit in D is set; cancelled instructions still consume their clocks. Works in cog, LUT, and hub. No flag effect. |
| **SKIPF** | `SKIPF {#}D` | `EEEE 1101011 00L DDDDDDDDD 000110010` | Fast skip: the PC leaps over each of the next up-to-22 instructions whose bit in D is set; skipped instructions cost nothing. Cog/LUT only. No flag effect. |
| **EXECF** | `EXECF {#}D` | `EEEE 1101011 00L DDDDDDDDD 000110011` | Jump to D[9:0] in cog/LUT, then apply D[31:10] as a SKIPF pattern. PC = {10'b0, D[9:0]}. The dispatch vehicle. No flag effect. 4 clocks. |

## 14.2 Arming {#sec-14-2}

| Instruction | Syntax | Encoding | Effect |
|-------------|--------|----------|--------|
| **SETQ** | `SETQ {#}D` | `EEEE 1101011 00L DDDDDDDDD 000101000` | Load D as the **persistent** XBYTE mode operand (with `_RET_` and `$1FF` on the stack, starts/continues the engine). Outside XBYTE, sets Q for block transfers. |
| **SETQ2** | `SETQ2 {#}D` | `EEEE 1101011 00L DDDDDDDDD 000101001` | Load D as a **one-shot** XBYTE mode operand — applies to the next bytecode only, then reverts to the last SETQ mode. Outside XBYTE, sets Q for LUT block transfers. |

## 14.3 The FIFO bytecode stream {#sec-14-3}

| Instruction | Syntax | Encoding | Effect |
|-------------|--------|----------|--------|
| **RDFAST** | `RDFAST {#}D,{#}S` | `EEEE 1100011 1LI DDDDDDDDD SSSSSSSSS` | Begin a fast sequential hub FIFO read at S[19:0]; D[13:0] = block size in 64-byte units (0 = unlimited), D[31] = no-wait. Precedes all RFxxxx reads. |
| **RFBYTE** | `RFBYTE D {WC/WZ/WCZ}` | `EEEE 1101011 CZ0 DDDDDDDDD 000010000` | Read a zero-extended byte from the FIFO into D. C = byte MSB, Z if zero. Fetches the bytecode. |
| **RFWORD** | `RFWORD D {WC/WZ/WCZ}` | (FIFO read family) | Read a zero-extended word from the FIFO — a fixed 16-bit inline operand. |
| **RFLONG** | `RFLONG D {WC/WZ/WCZ}` | (FIFO read family) | Read a long from the FIFO — a fixed 32-bit inline operand. |
| **RFVAR** | `RFVAR D {WC/WZ/WCZ}` | `EEEE 1101011 CZ0 DDDDDDDDD 000010011` | Read a **zero-extended** 1–4-byte variable-length value into D. C = 0. |
| **RFVARS** | `RFVARS D {WC/WZ/WCZ}` | `EEEE 1101011 CZ0 DDDDDDDDD 000010100` | Read a **sign-extended** 1–4-byte variable-length value into D. C = value MSB. |
| **GETPTR** | `GETPTR D` | `EEEE 1101011 000 DDDDDDDDD 000110100` | Get the current FIFO hub pointer into D. XBYTE writes this to `PB` each dispatch. |

# Chapter 15: Configuration Constants & Patterns {#ch-15}

## 15.1 The mode operand {#sec-15-1}

The value handed to SETQ/SETQ2, written `%A...F`:

- **A** (high bits) — the LUT base address of the dispatch table; the number of A bits grows as the table shrinks (§7.2).
- **middle pattern** — selects table size (256/128/64/32/16) and, in the 256 case, compression (§7.2–7.3).
- **F** (bit 0) — flag write: F=1 writes C ← index bit 1, Z ← index bit 0 each dispatch; F=0 leaves flags alone (§7.4).

| Goal | Operand |
|------|---------|
| 256-entry table at LUT `$100`, flags off | `$100` (`%1_0000_0000_0`) |
| 256-entry table at LUT `$000`, flags off | `$0` |
| 256-entry table, flags **on** | base, with bit 0 = 1 |
| 256 with 16-primary compression, threshold B | `%ABBBB00xF` (§7.3) |
| smaller tables | per the §7.2 patterns |

## 15.2 Registers and ranges {#sec-15-2}

| Item | Value |
|------|-------|
| `PA` | `$1F6` — current bytecode (written clock 2); usable as an immediate operand in the handler |
| `PB` | `$1F7` — current FIFO read pointer (written clock 5) |
| Return target on stack | `$1FF` — what each bytecode routine returns to, triggering the next dispatch |
| Handler address range | cog `$000`–`$1FF`, LUT `$200`–`$3FF` (EXECF jumps to a 10-bit cog/LUT address) |
| LUT entry format | [9:0] = handler address, [31:10] = 22-bit SKIPF pattern |
| Hardware stack depth | 8 levels |
| Dispatch overhead | 6 clocks/bytecode; minimum loop 8 clocks |

## 15.3 The arming pattern {#sec-15-3}

```pasm2
                setq2   #N-1                ' load N-long table into LUT
                rdlong  $000, ##table       '   (or the chosen LUT base)
                rdfast  #0, ##program       ' FIFO -> bytecode stream
                push    #$1ff               ' return target per bytecode
        _ret_   setq    #mode               ' arm persistent mode = start
```

# Part V: Appendices

The appendices are lookup material and pointers: the quick-reference cards, the encoding summary, community implementations to study, and a troubleshooting guide.

# Appendix A: XBYTE Quick Reference {#app-a}

**The dispatch cycle (8 clocks, 6 overhead):**

| Clk | Activity |
|-----|----------|
| 1 | `RFBYTE` bytecode · `SKIPF #0` (overlaps prior `_RET_`) |
| 2 | `MOV PA,`bytecode · `RDLUT` |
| 3 | `RDLUT` → D |
| 4 | `EXECF D` begin |
| 5 | `MOV PB,`GETPTR · `MODCZ` (if F) · `EXECF` branch |
| 6–7 | pipeline flush + reload |
| 8 | first handler instruction; `_RET_` → loop to clock 1 |

**Table sizes (mode operand `%A...F`):**

| Size | Operand | Base | Index | Alt index |
|------|---------|------|-------|-----------|
| 256 | `%A000000xF` | `%A00000000` | b[7:0] | — |
| 256+compress | `%ABBBB00xF` | `%A00000000` | b[7:4]<B → b[7:0]; else group | — |
| 128 | `%AAxx0010F` | `%AA0000000` | b[6:0] | `%AAxx0011F` → b[7:1] |
| 64 | `%AAAx1010F` | `%AAA000000` | b[5:0] | `%AAAx1011F` → b[7:2] |
| 32 | `%AAAAx100F` | `%AAAA00000` | b[4:0] | `%AAAAx101F` → b[7:3] |
| 16 | `%AAAAA110F` | `%AAAAA0000` | b[3:0] | `%AAAAA111F` → b[7:4] |

**F bit:** 0 = flags untouched; 1 = C ← index bit 1, Z ← index bit 0.

**Arming checklist:** load table → LUT · `RDFAST` the stream · `PUSH #$1FF` · `_RET_ SETQ #mode`.

# Appendix B: Instruction Encoding Summary {#app-b}

| Instruction | Encoding | Clocks | Flags |
|-------------|----------|--------|-------|
| SKIP `{#}D` | `EEEE 1101011 00L DDDDDDDDD 000110001` | 2 | — |
| SKIPF `{#}D` | `EEEE 1101011 00L DDDDDDDDD 000110010` | 2 | — |
| EXECF `{#}D` | `EEEE 1101011 00L DDDDDDDDD 000110011` | 4 | — |
| SETQ `{#}D` | `EEEE 1101011 00L DDDDDDDDD 000101000` | 2 | — |
| SETQ2 `{#}D` | `EEEE 1101011 00L DDDDDDDDD 000101001` | 2 | — |
| RDFAST `{#}D,{#}S` | `EEEE 1100011 1LI DDDDDDDDD SSSSSSSSS` | 2 | — |
| RFBYTE `D {WC/WZ/WCZ}` | `EEEE 1101011 CZ0 DDDDDDDDD 000010000` | 2 | C=MSB, Z |
| RFVAR `D {WC/WZ/WCZ}` | `EEEE 1101011 CZ0 DDDDDDDDD 000010011` | 2 | C=0, Z |
| RFVARS `D {WC/WZ/WCZ}` | `EEEE 1101011 CZ0 DDDDDDDDD 000010100` | 2 | C=MSB, Z |
| GETPTR `D` | `EEEE 1101011 000 DDDDDDDDD 000110100` | 2 | — |

# Appendix C: Further Implementations {#app-c}

The P2 community has built real interpreters and CPU/console emulators that run on physical silicon. These are pointers for further study — each entry gives the project, who built it, what it emulates, where to find it, and its license where stated. Whether a given project uses XBYTE for its dispatch, versus a hand-rolled loop, is noted only where the project's own materials state it.

## C.1 P2 Arc8de — eight 8080 arcade machines on one P2 {#sec-c-1}

A single P2 module emulating the **Intel 8080** and driving **up to eight simultaneous mini arcade cabinets** — one cog per console, each running an 8080 emulator while also generating composite video and one channel of audio. The arcade games run original ROM code; a multiplayer tank game and a light-cycles game were written in 8080 assembler for the project.

- **Builders:** Chip Egues (lead architect); Baggers (8080 emulator co-development, original multiplayer games); VonSzarvas (PCB); Coley (cabinet); cabinet graphics by Andy C. Spencer (Retro Computer Museum, UK).
- **What it emulates:** Intel 8080 (one instance per cog).
- **Links:** Parallax product page — `https://www.parallax.com/p2arc8de-one-p2-ec-module-provides-audio-video-and-buttons-for-eight-8-concurrent-games/`; forum thread "P2 Arc8de Project" — `https://forums.parallax.com/discussion/173341/p2-arc8de-project`; Autodesk Fusion cabinet model on OBEX — `https://obex.parallax.com/obex/autodesk-fusion-model-of-p2-arca8de-8in1/`.
- **License:** CC BY-SA 3.0 (project materials).
- **Dispatch mechanism:** not stated in the project's public materials.

## C.2 The "Yume" emulator suite — console emulators on P2 + PSRAM {#sec-c-2}

A family of console emulators by **wuerfel_21** (GitHub organization **IRQsome**), under the umbrella project **p2-dreamy-emulators** (`https://sr.ht/~wuerfel_21/p2-dreamy-emulators/`). Each runs console ROM images on a P2 with external PSRAM. Their guest CPUs are concrete instances of the families discussed in Chapter 10.

| Project | Console | Guest CPU(s) | Repository | Status |
|---------|---------|--------------|------------|--------|
| **MegaYume** | Sega Mega Drive / Genesis | Motorola 68000 + Z80 | `https://github.com/IRQsome/MegaYume` | released |
| **NeoYume** | SNK Neo Geo AES | Motorola 68000 + Z80 | `https://github.com/IRQsome/NeoYume` | released |
| **MisoYume** | Super Nintendo (SNES) | 65(C)816 | `https://github.com/IRQsome/MisoYume` | beta |

- **License / dispatch mechanism:** see each repository. A 68000 guest is the "word-opcode CISC" case of §10.2, where dispatch and auto-fetch apply only partially — confirm any specifics from the project source rather than assuming.

# Appendix D: Troubleshooting {#app-d}

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Engine never dispatches | no `$1FF` on the stack before the arming `_RET_` | `PUSH #$1FF` immediately before `_RET_ SETQ` (§6.1) |
| First bytecode is garbage | FIFO not primed | run `RDFAST` on the bytecode stream before arming (§3.1) |
| Wrong handler runs | address/skip fields transposed in a table entry | address in [9:0], SKIPF pattern in [31:10] (§4.1) |
| Handler runs the wrong variant | wrong SKIPF pattern in the table entry | recompute the pattern; remember every set bit *skips* (§2.4) |
| Dispatch corrupts after a few bytecodes | hardware stack overflow | shorten handler call chains; the stack is 8 levels (§8.1) |
| Flags behave unexpectedly across bytecodes | F bit set when not intended (or vice-versa) | set/clear bit 0 of the mode operand deliberately (§7.4) |
| A prefixed/extended opcode decodes as the base opcode | no alternate-table handling | make the prefix a one-shot `SETQ2` handler (§6.3, Ch. 12) |
| Branch goes nowhere | guest PC changed without re-pointing the FIFO | a branch is a `RDFAST` to the new address (§8.3) |

# Index {#index}

- **Application map** (other uses) — Ch. 13, §13.2
- **Arming** — Ch. 6; quick card, App. A
- **Beyond interpreters** (applications) — Ch. 13
- **Bytecode** (definition) — Ch. 1; in `PA` — Ch. 4, §8.2
- **Compression mode** (`%ABBBB`) — §7.3
- **Dispatch cycle** (8 clocks) — Ch. 5; App. A
- **Dispatch table** (LUT) — Ch. 4; building entries — §4.2
- **Display list** (application) — §13.5
- **EXECF** — §2.3; Ch. 14
- **F bit** (flags from bytecode) — §7.4, §15.1
- **FIFO** — Ch. 3; `RDFAST` — §3.1
- **GETPTR / PB** — §3.4, §15.2
- **Hardware stack / `$1FF`** — §6.1, §8.1
- **Inline operands** — §3.3, §8.3
- **LUT entry format** — §4.1, §15.2
- **MIDI dispatcher** (application) — §13.4
- **Mode operand** — §6.2, Ch. 7, §15.1
- **Overhead** (6 clocks) — §1.2, §5.2
- **PA** (current bytecode) — §4.3, §15.2
- **Prefix / alternate table** — §6.3, §13.6, Ch. 12
- **RFBYTE / RFWORD / RFLONG** — §3.2, Ch. 14
- **RFVAR / RFVARS** — §3.3, Ch. 14
- **SETQ / SETQ2** — §6.3, §13.6, Ch. 14
- **Shared-handler idiom** — §2.4, §9.3
- **SKIP** — §2.1, Ch. 14
- **SKIPF** — §2.2, Ch. 14
- **State machine** (table-as-state) — §13.3, §13.6
- **Table sizes** — §7.2; App. A
- **Terminal / ANSI reader** (application) — §13.3
- **When to reach for XBYTE** — §1.5, §13.7
- **6502 emulator** — Ch. 11
- **6809 / SETQ2 vignette** — Ch. 12


