# Voice Guide — P2 Debug Window Manual

**Document:** P2 Debug Window Manual
**Purpose:** Define the writing voice and tone for the manual that documents the P2's nine DEBUG display windows.

**Basis:** Derived from the **P2 I/O & Smart Pins User Guide** voice guide (same document class — a comprehensive user guide for a P2 hardware subsystem with many modes), with debug-domain content rules folded in from the Single-Step Debugger Manual's voice guide. This was chosen deliberately after surveying all manual voice guides; the IOSP model fits a multi-mode subsystem user guide better than the reference-only (Assembly, Streamer) or tutorial (DeSilva, Smart Pins Tutorial) models.

**One deliberate divergence from the IOSP model:** this guide uses **second person** ("you"), to match this manual's onboarding/guiding job and the sibling Single-Step Debugger Manual. All of IOSP's other disciplines — no marketing, no hedging, no celebration, comprehensive coverage, grounded claims — are kept intact; voice rigor is independent of grammatical person.

**Status:** Active — adopted 2026-05-31.

> **Migration note.** The existing v2 master was generated in an enthusiastic
> "Discovery Guide" voice (e.g. "Revolutionary," "20× faster," "rivals \$10,000
> equipment," "Debug Iceberg Effect"). That voice is **out of conformance with the
> entire house standard** — every house voice guide forbids marketing/celebration.
> Bringing v2 into conformance with this guide is a substantial rewrite; the audit's
> voice/tone dimension (#9) will surface its full scope.

---

## 1. Voice Philosophy

### 1.1 The Guiding Principle

> **This guide tells you exactly how to use each P2 DEBUG display window — what it shows, how to configure it, and how to drive it from `DEBUG()` output — with every command and option laid out clearly.**

This is a **practical reference** that supports multiple entry points:
- "I've never used a DEBUG display window" → start with the TERM chapter and the orientation material.
- "I want to accomplish a specific task" → use the task/use-case index.
- "I need the details of one window" → go directly to that window's chapter.

The voice must be:
- **Authoritative** — this is the source of truth for the DEBUG display windows.
- **Precise** — no ambiguity about commands, parameters, or behavior.
- **Comprehensive** — all of a window's commands and options presented, not just the common ones.
- **Practical** — focused on accomplishing real debugging tasks.

### 1.2 Scope: the nine DEBUG display windows

This guide covers the complete set of P2 DEBUG display windows, all hosted in `pnut_term_ts`:

| Window | One-line purpose |
|--------|------------------|
| **TERM** | Text terminal — character-mode output and simple status displays |
| **BITMAP** | Pixel raster — direct framebuffer-style drawing |
| **PLOT** | XY plotting surface with sprites and layered drawing |
| **LOGIC** | Logic-analyzer trace of digital channels |
| **SCOPE** | Time-domain oscilloscope of analog/sampled values |
| **SCOPE_XY** | XY (Lissajous / phase) scope |
| **FFT** | Frequency-domain spectrum |
| **SPECTRO** | Spectrogram (frequency over time) |
| **MIDI** | MIDI event display |

The voice is consistent across all nine — same precision, same per-window format, same thoroughness.

> These display windows are this manual's **subject**. The *single-step debugger*
> window is a different subject covered by the Single-Step Debugger Manual; mention
> it only to cross-reference, never to teach it here.

---

## 2. Voice Characteristics

### 2.1 Technical precision

State exactly what a command does, with concrete parameters and ranges:

```
SCOPE opens a time-domain display. Declare it with `DEBUG(`SCOPE MyScope SIZE
256 128 ...)` — that names the window and sets its pixel dimensions. Each data
packet you send plots one sample column; the window scrolls left when full.
```

- Exact terminology throughout (window type names in caps, command keywords as written).
- Specific values and ranges, sourced from the window's theory-of-operations.
- No hedging: "scrolls" not "typically scrolls."
- Second person, but never chatty: "you send" is fine; "you'll love how easy this is" is not.

### 2.2 Structured predictability

Every window chapter follows the same format:
- What the window shows (one sentence).
- The configuration/declaration command and all its parameters.
- The per-update data commands and their formats.
- Control/feature commands (color, scaling, layers, cropping, triggers — whatever that window supports).
- A complete, `pnut_ts`-compilable example.
- Use cases and considerations.

### 2.3 Comprehensive coverage

For each window, present ALL of its commands and options — not just the ones in the most common example. If a window supports eight control commands, document eight. Missing options are a coverage defect, not a stylistic choice.

### 2.4 Task-oriented guidance

Include "when to use" and "considerations" throughout — which window suits which debugging problem, what its limits are, and how to combine it with others:

```
When to use SCOPE vs PLOT:
- SCOPE — a value changing over time (waveform, sensor trace).
- PLOT  — relationships between values, custom instruments, sprite-based UIs.

Considerations:
- Update rate is bounded by the DEBUG serial link; high-rate captures need
  packed data formats (see the window's theory-of-operations).
```

---

## 3. Voice Rules

### 3.1 Always do

| Rule | Example |
|------|---------|
| Use definitive statements | "PLOT renders to a back buffer, then swaps" ✅ |
| Be specific about values | "channel count 1–8" ✅ |
| List ALL of a window's commands/options | document every control command, not just the example's ✅ |
| Show complete, compilable examples | every example builds with `pnut_ts` ✅ |
| Cross-reference related windows | "See also: SCOPE_XY for phase plots" ✅ |
| Speak to the reader (second person) | "You declare the window with…" ✅ |
| Ground every claim in the theory-of-operations | cite the window's `REF/theory-of-operations/` doc ✅ |

### 3.2 Never do

| Rule | Bad example | Why |
|------|-------------|-----|
| Never use marketing/superlatives | "Revolutionary," "20× faster," "rivals \$10,000 equipment" ❌ | Out of house standard; unverifiable |
| Never celebrate | "Now you've unlocked the power of…" ❌ | Tutorial/marketing voice |
| Never hedge | "The window might scroll" ❌ | Creates ambiguity |
| Never get chatty/breezy | "You'll love how easy this is" ❌ | Second-person tempts celebration/marketing creep |
| Never minimize | "Simply configure…" ❌ | Dismissive of real complexity |
| Never omit options | document one command of several ❌ | Incomplete |
| Never assume context | "As you know…" ❌ | Each chapter must stand alone |

### 3.3 Voice comparison

| Aspect | Discovery-Guide draft (v2) | This user guide |
|--------|----------------------------|-----------------|
| Address | Second person, exclamatory | Second person, measured |
| Tone | Promotional, "iceberg," superlatives | Authoritative, comprehensive |
| Coverage | Highlight reel of impressive features | ALL commands/options per window |
| Claims | "20× faster," "$10,000 equipment" | Source-backed, quantified only when sourced |
| Hedging / celebration | Present | Never |

---

## 4. Debug-domain content rules

These are correctness rules specific to the DEBUG subsystem (carried from the Single-Step Debugger Manual's voice guide, where they were established):

1. **Correct tooling, always.** The compiler is **`pnut_ts`** (`-d` / `--debug` compiles with DEBUG enabled). The host application that opens the DEBUG display windows is **`pnut_term_ts`**. There is no "PNut IDE," no `pnut.exe`, no `Run → Debug Enable` menu. Strip any such reference from the source drafts.
2. **Valid DEBUG output formatters only.** `UDEC` / `SDEC` / `UHEX` / `SHEX` / `UBIN`, each with an optional trailing `_` to suppress the auto label. Never bare `DEC` / `HEX` / `BIN` (not valid Spin2 DEBUG formatters).
3. **Every code example compiles** with `pnut_ts`. Stub any helper methods so examples build without external hardware (this manual's example corpus already uses this pattern).
4. **P2, never P1.** P2 syntax exclusively: `COGSPIN` / `COGINIT` (never `cognew`), `GETCT` (never `CNT`).
5. **Native comment syntax only** in code blocks: `'` line comments, `{ }` / `{{ }}` blocks. No `//`, `/* */`, `;`, or `#`-prefixed comments — even in pseudocode.
6. **Software-only, no external hardware** (creation-guide "Minimal Hardware Design Philosophy" — Level 0 is preferred). Every example must run on a bare P2 board + PC with no wiring, generating its own data in software: CORDIC (`QSIN`/`QROTATE`), the RNG (`GETRND` / `?` operator), counters, `GETCT` timing, and software simulation of sensors/signals/protocols. Never require an external sensor, probe, or wiring to see a window work. If a real-hardware application is worth showing, add it as a short optional "extension" note *after* the software-only version.

---

## 5. Terminology standards

| Canonical | NOT these | Notes |
|-----------|-----------|-------|
| DEBUG display window | debug window, output window | The subject of this manual |
| TERM / BITMAP / PLOT / LOGIC / SCOPE / SCOPE_XY / FFT / SPECTRO / MIDI | mixed case, abbreviations | Window type names in caps, as the `DEBUG()` keyword is written |
| single-step debugger | step debugger, the debugger | The *other* manual's subject; cross-ref only |
| `DEBUG()` statement | debug print, debug call | The Spin2/PASM mechanism that feeds the windows |
| `pnut_term_ts` | terminal, the host | The host application |
| sysclk | system clock | Clock-frequency reference |

- **PASM2 instructions:** bold uppercase. **Spin2 methods:** bold mixed case.
- **DEBUG command keywords** (`SCOPE`, `SIZE`, `TRACE`, …): as written in the `DEBUG()` backtick syntax.

---

## 6. Grounding

Every factual claim grounds in this manual's authoritative sources, in priority order (see `creation-guide.md` §Content Sources):

1. **`REF/theory-of-operations/<WINDOW>_Theory_of_Operations.md`** — the per-window Bible (PNut v55-derived). On any conflict, the theory-of-operations wins.
2. The Spin2 v5.1 source corpus at `engineering/ingestion/sources/spin2-v51/`.
3. This manual's `studies/` and Pascal-source extraction docs.

---

## 7. Quality checklist

Before finalizing any window chapter, verify:

**Voice**
- [ ] Second person; speaks to the reader directly, without chattiness or celebration.
- [ ] No marketing, superlatives, or celebration.
- [ ] No hedging; definitive statements only.

**Completeness**
- [ ] ALL of the window's commands and options documented.
- [ ] A complete, `pnut_ts`-compilable example.
- [ ] "When to use" / considerations included.
- [ ] Cross-references to related windows.

**Accuracy**
- [ ] Every claim traced to the window's theory-of-operations doc.
- [ ] Examples compile; comment syntax is native; formatters are valid.
- [ ] Tooling is `pnut_ts` / `pnut_term_ts` only.

---

## 8. Summary

```
Voice = Authoritative + Comprehensive + Practical — second person, no marketing.
```

A complete reference that answers "how do I use each P2 DEBUG display window?" — from the basic TERM text window through the SCOPE/PLOT/FFT instruments — with every command and option presented, every claim grounded in the per-window theory-of-operations, and not a word of marketing.

---

*Adopted: 2026-05-31. Basis: IOSP User Guide voice model + Single-Step Debugger debug-domain rules.*
