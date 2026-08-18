# P2 XBYTE Programming Guide - Voice Guide

**Document:** P2 XBYTE Programming Guide
**Purpose:** Define writing voice and tone — a guide that teaches XBYTE conceptually, then serves as a precise reference for building interpreters and emulators
**Created:** 2026-06-26
**Model:** P2 Streamer Programming Guide voice-guide (two-register approach), adapted to XBYTE

---

## 1. Voice Philosophy

### 1.1 The Guiding Principle

> **This guide first helps you understand what XBYTE is and why you would build on it, then tells you exactly how the engine dispatches each bytecode and how to configure it.**

The document does two jobs, so it speaks in **two registers**:

- A **teaching register** — the landscape chapters that open the book (Ch. 1–2), the conceptual chapter (Ch. 3), the skip-family foundation (Ch. 4), and each chapter's opening orientation — warm, plain-spoken, motivated, for a reader meeting XBYTE for the first time.
- A **reference register** — the dispatch-cycle walk, the mode/encoding tables, the bit-field specifications, and the per-instruction detail — for a reader who already knows what they need and wants it fast. The reference register is authoritative, precise, dense, and practical.

### 1.2 The Spine (carry it through every chapter)

XBYTE automates the inner loop of every bytecode VM — *fetch the next bytecode → look up its handler → dispatch → run → repeat* — in hardware, at **6 clocks of overhead per bytecode**. Teach the whole engine, then prove it by building a small VM and a tiny CPU emulator. Every chapter should connect back to that loop.

### 1.3 Target Audience

A **spectrum**, and the two registers serve both ends:

- **Newcomers** — developers who have heard of XBYTE but do not yet know what it is, why the P2 has it, or when to reach for it. The **teaching register** is for them: Chapters 1–4 assume no prior XBYTE knowledge and define unfamiliar terms as they appear — the emulation vocabulary in Part I (§2.7 "The words for all this"), then bytecode, dispatch, LUT table, and SKIPF pattern in Part II.
- **Builders** — readers who understand P2 cog/hub/LUT architecture and want to implement an interpreter, a custom VM, or a CPU emulator. The **reference register** is for them: quick lookup of the cycle, the modes, the encodings, and the configuration bits.

The teaching layer builds the background a newcomer needs (the FIFO, the LUT, the hardware stack, `_RET_`); the reference layer assumes it. A reader typically starts in the teaching register and graduates into the reference register as they build.

### 1.4 The Two Registers — Teaching and Reference

**Use the teaching register for:** Part I (Ch. 1–2, the landscape a newcomer needs before any machinery), Chapter 3 (Understanding XBYTE), Chapter 4 (the skip family, the conceptual foundation), the opening orientation of each Part and chapter, and the first explanation of any unfamiliar concept (bytecode dispatch, the LUT table, the auto-XBYTE loop, compression modes).

Teaching-register rules:

- **Plain language first.** Define every unfamiliar term on first use, in one or two sentences, with a concrete use — e.g., a *bytecode* as "one small number that stands for one operation the interpreter knows how to perform; a program is a stream of them."
- **Motivate before mechanism.** Say *why* something matters before *how* it works.
- **"You" and light analogy are allowed and encouraged.** The assembly-line dispatcher, the lookup table as a switchboard, the skip pattern as a stencil over a shared routine — imagery is how a newcomer forms a mental model. Use it.
- **Differentiate by contrast.** SKIP vs SKIPF vs EXECF, SETQ vs SETQ2, persistent vs one-shot — show what makes them *different* rather than describing each in isolation.
- **Comparative grounding is a soft bridge, never a crutch.** A real-world parallel (a `switch` statement, a threaded interpreter) can be offered as a clearly skippable aside — a `> If you've written an interpreter before:` note. The explanation must always stand on its own.
- **Applications are pointers, not pitches.** "If you're emulating an 8-bit micro, these are the modes to understand."

**Use the reference register for:** the dispatch-cycle table, mode/compression tables, the LUT-entry bit-field, per-instruction syntax and effects, configuration recipes, and worked code. Third person, no *vague* hedging (§2.2a), dense, exact.

**The handoff.** A chapter typically opens in the teaching register (a short orientation — what this mechanism is for, how the pieces differ) then shifts into the reference register for the tables and code. Guidance up front, precision underneath.

---

## 2. Voice Characteristics

### 2.1 What We DO Say

| Pattern | Example |
|---------|---------|
| Definitive statements | "XBYTE writes the fetched bytecode to PA before dispatch." |
| Precise specifications | "The LUT entry's low 10 bits are the routine address; the high 22 bits are the SKIPF pattern." |
| Clear constraints | "Bytecode routines must reside in cog or LUT RAM and end in RET or `_RET_`." |
| Practical guidance | "Arm the persistent mode once with `_RET_ SETQ`; borrow an alternate table for one bytecode with `_RET_ SETQ2`." |
| Direct comparisons | "SKIP cancels instructions in place; SKIPF leaps the PC over them." |

### 2.2 What We DON'T Say

| Avoid | Why | Instead |
|-------|-----|---------|
| "Let's explore XBYTE..." | Tutorial voice (reference layer) | "XBYTE dispatches..." |
| "You might wonder why..." | **Tutorial filler** (NOT the same as calibrated confidence — see §2.2a) | State the fact directly |
| "Simply arm the engine..." | Dismissive of complexity | "Arm the engine..." |
| "Basically, it works like..." | Vague | Precise description |
| "Congratulations!" | Tutorial celebration | (omit) |
| "the obvious way to think about X is wrong" · "it is tempting to..." · "Read that again" | **Reader-as-foil** — tells the reader what they think, then corrects them (the "besserwisser" register) | State the correct fact; let the reader draw the contrast |
| "this one is free money" · "the single most elegant part" · "nothing else comes close" · "if you read one thing, read this" | **Self-admiration** — the text praising its subject or its own explanation | State what the thing does; let the reader judge it |
| "and here is the trap" · "they stop one sentence too early" · "Hold that result" | **Staged reveal** — withholding a fact to manufacture a beat | Deliver the fact where it belongs, unstaged |
| interpreter clock timings for Spin2 methods | Banned class (unverifiable, rev-dependent) | cite the 6-clock HARDWARE overhead only, or describe the code path |

#### 2.2a Calibrated confidence is required — it is not hedging {#sec-2-2a}

> **Where the rules live.** §2.2a and §2.4 were authored here, from the 2026-07-20 review,
> and were then promoted into the house canon:
> `engineering/standards/documentation-standards/documentation-voices-catalog.md`
> ("The Shared Discipline — the four house rules"), where they are **R1** and **R4**.
> That file is now the single statement of the rules; this guide states this document's
> position on them. Being the origin is not an exemption from citing the canon — until
> 2026-08-15 this was the only voice guide in the fleet that cited it nowhere at all,
> which is how the rule and its birthplace drift apart.

Banning tutorial filler ("you might wonder", "let's explore") does **not** mean
banning *uncertainty*. A qualifier that reflects the true state of the evidence
— "usually", "often", "on most guests", "in practice" — is **accuracy**, not
hedging, and it is required wherever the unqualified claim would overstate.

The test is one line: **never state a claim above its evidence.** "It sits there
forever" is wrong if the code exits on any interrupt; "most emulators" is wrong
if you have counted none. Say what is true at the confidence it is true, and
point at the primary source when a solid figure is lacking (see the
[[document-audit]] payoff-sentence sweep, Dimension #4c, and the
[[document-finalize]] write-time counterpart). A rhetorical flourish that
*demands* a punchy payoff is exactly where an unsupported claim slips in — strip
the flourish and read what is left as a bare claim before keeping it.

### 2.3 Voice Comparison

| Aspect | DeSilva Tutorial | This Guide (reference layer) | This Guide (teaching layer) |
|--------|------------------|------------------------------|-----------------------------|
| Person | Second ("you") | Third (component names) | Second allowed, sparingly |
| Tone | Warm, encouraging | Authoritative, precise | Warm, plain-spoken |
| Tutorial filler | Occasional | Never | Never |
| Calibrated qualifiers | Yes | **Yes, where true** (§2.2a) | **Yes, where true** (§2.2a) |
| Analogy | Yes | Rarely | Yes, as a mental-model aid |
| Celebration | Yes ("Uff!") | Never | Never |
| Closing beat every section | — | No (budget — §2.4) | No (budget — §2.4) |

### 2.4 Cadence budget — not every section earns a beat {#sec-2-4}

A *beat* is a closing sentence that lands a rhetorical punch rather than
finishing the exposition — a verdict, a reversal, a directive to the reader, an
aphorism that restates with force. One well-placed beat is good writing. The
failure mode is **regularity**: when nearly every section ends on one, the
reader stops hearing the individual beat and starts hearing the *metronome* —
"instantly recognizable and becoming rapidly fatiguing" (Chip Gracey, XBYTE review 2026-07-20).

The recognizable-AI quality is the pattern, not any one sentence, so the fix is
distribution, not deletion. Budget:

**Decision: ADOPT R4 as written** — the budget, the run limit, the chapter-closer
emphasis, the declared-refrain carve-out, and the protection for earned beats all apply
to this document unchanged. The numbers themselves are stated once, in the house canon
(`engineering/standards/documentation-standards/documentation-voices-catalog.md`, R4);
they are not copied here, because a copied number is one that drifts from the rule it
came from while still reading as authoritative.

Detection tooling: the [[document-audit]] payoff-sentence sweep (Dimension #4c)
measures closing-beat rate and the longest consecutive run.

---

## 3. Enhancement Markers

| Marker | When to Use | Example |
|--------|-------------|---------|
| **⚠️ Pitfall:** | Common mistakes with non-obvious consequences | "⚠️ **Pitfall:** Forgetting `PUSH #$1FF` before arming XBYTE — the first `_RET_` returns to the wrong address and dispatch never begins." |
| **💡 Tip:** | Non-obvious techniques or optimizations | "💡 **Tip:** Point several bytecodes at one routine body and vary only the SKIPF pattern in their LUT entries — one handler serves a whole family of related opcodes." |
| **🔧 Hardware:** | Silicon-level details affecting usage | "🔧 **Hardware:** The bytecode is always written to PA ($1F6), so a routine can use it directly as an immediate operand." |

---

## 4. Terminology Standards

### 4.1 Canonical Terms

| Canonical Term | NOT These | Notes |
|----------------|-----------|-------|
| bytecode | opcode, token | the unit fetched from the stream and dispatched |
| dispatch | decode, branch-to | selecting and jumping to the handler |
| routine / handler | function, sub | the per-bytecode code body in cog/LUT RAM |
| the skip family | "skip instructions" | SKIP, SKIPF, EXECF as a related set |
| SKIPF pattern | skip mask, skip bits | the 22-bit field that leaps the PC |
| dispatch table / LUT table | jump table | the 256-entry table of EXECF operands in LUT |
| mode operand | config word, setup value | the `{#}D` value to SETQ/SETQ2 |
| persistent mode / one-shot mode | sticky/temporary | SETQ vs SETQ2 personality |
| overhead | cost, penalty | the 6-clock per-bytecode figure |
| cog | CPU, COG (all-caps) | lowercase in prose |

### 4.2 Instruction Formatting

| Context | Format | Example |
|---------|--------|---------|
| In prose | Bold uppercase | "The **EXECF** instruction..." |
| In lists | Uppercase, no bold | SKIP, SKIPF, EXECF |
| In code | lowercase or uppercase per source convention | `_ret_ setq #$100` |

### 4.3 Bit Field Notation

- Brackets: D[31:10], D[9:0], b[7:4]
- Binary with underscores: `%A000000xF` (mode operand), `%1101_0110`
- Hex with prefix: `$1F6`, `$1FF`, `$200`
- Symbols / registers in monospace: `PA`, `PB`, `_RET_`

---

## 5. Section-Specific Voice

### 5.1 Mechanism Descriptions (reference)

```
✅ "On each dispatch, XBYTE reads one byte from the FIFO, writes it to PA,
    indexes the LUT table with it, and executes the resulting EXECF operand —
    a jump plus a SKIPF pattern — in six clocks of overhead."

❌ "Let's see what happens when XBYTE runs. It's pretty clever because it..."
   (tutorial voice in the reference layer)
```

### 5.2 Code Examples — show *why*, not just *what*

```pasm2
✅         push    #$1ff               ' return target for every bytecode
   _ret_   setq    #$100               ' arm persistent mode: 256-entry table @ LUT $100

❌         push    #$1ff               ' push
   _ret_   setq    #$100               ' setq
```

### 5.3 Cross-References — direct

```
✅ "See Chapter 11 for the full table-size and compression encodings."
✅ "Related: SKIP, SKIPF, EXECF."

❌ "You might want to check out the modes chapter later..."
```

---

## 6. Quality Checklist

### Voice Consistency
- [ ] Reference layer: third person, no tutorial voice, **voice rules R1–R4 satisfied — see §2.2a
      and §2.4.** (This item points; it does not re-encode.)
- [ ] Teaching layer: plain language, terms defined on first use, analogy as a mental-model aid
- [ ] No celebration, no "simply"/"basically"

### Terminology Consistency
- [ ] Instruction names bold uppercase in prose
- [ ] Canonical terms from §4.1 (bytecode/dispatch/routine/mode operand/overhead)
- [ ] "cog" lowercase in prose
- [ ] Registers/symbols in monospace (`PA`, `PB`, `_RET_`)

### Discipline
- [ ] Every hardware claim traces to the P2 Documentation v35 / KB YAML (grounding digest)
- [ ] The 6-clock figure cited as the hardware overhead; NO Spin2-method interpreter clock timings
- [ ] Capstone/vignette code is tiny & illustrative and compiles with `pnut-ts`
- [ ] No "systems similar to the P2" content in v0.1.0; external projects only in Appendix C as links

### Enhancement Completeness
- [ ] Pitfalls / Tips / Hardware notes placed where they earn their keep
- [ ] Cross-references to related chapters and instructions

---

*Version: 0.1 - Initial Voice Guide (XBYTE), modeled on the Streamer two-register guide*
*Created: 2026-06-26*
