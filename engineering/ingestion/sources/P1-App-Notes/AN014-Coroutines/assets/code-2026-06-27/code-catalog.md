# Code Catalog — AN014 Coroutines

**Captured:** 2026-06-27 · **Mode:** capture + catalog only (NO compile)
**Validation status:** `code_validated: false` — **NOT validated, no P1 compiler** (pnut_ts is P2-only; P1 flexspin not installed — charter §3). Code is captured verbatim and findable; deep validation deferred to a dedicated P1 code pass.

## File inventory

| File | Encoding | Lines (total / non-blank) | License | Origin |
|------|----------|---------------------------|---------|--------|
| `appnote_coroutine.spin` | UTF-16 LE, CRLF | 134 / 103 | MIT (© 2011 Parallax, Inc.) | AN014 companion download (`parallaxsemiconductor.com/an014`); copied byte-for-byte (md5 `0c723dfb8c55646cdb0f4881210bbb1b`) |

The file is a **single self-contained Spin1 object** — `CON` + one `PUB Start` + one `DAT` PASM block + an MIT license block. It is the centerpiece of this software-technique note.

## What it demonstrates

A complete, runnable demonstration of **cooperative two-task multitasking inside one cog** using the coroutine pattern. Two coroutines (`ping` and `pong`) each blink a separate LED (pins 16/17 on the Propeller Demo Board #32100) at different rates — ping at clkfreq·11/16, pong at clkfreq·13/16 — by yielding to each other rather than running on separate cogs or using interrupts.

## Structure

- **`CON`** — clock setup (`xtal1 + pll16x`, 5 MHz crystal) and `PING_LED`/`PONG_LED` pin constants (Demo-Board-specific; the note explicitly invites changing these for other boards).
- **`PUB Start`** — Spin1 launcher: computes the two LED half-periods from `clkfreq`, then `cognew(@pingpong, 0)` loads the PASM `DAT` block into a fresh cog.
- **`DAT` PASM1 block** — five labeled sections (mirrors the appnote's own `'-------[ ... ]` banner style):
  1. `pingpong` — init: enable both pins in `dira`, seed `ping_time`/`pong_time` from `cnt`.
  2. `ping` coroutine — explicit on/off LED control, with **two** distinct `call #swap` yield points (`ping` and `ping_on`), proving execution resumes where it left off.
  3. `pong` coroutine — same timing logic but a single yield, toggling its pin with `xor outa,pong_mask`.
  4. `swap` / `swap_ret` — the **one-instruction coroutine switcher** (a single self-modifying `jmp`).
  5. variables — `long` masks/periods and `res`-reserved scratch (`ping_time`, `pong_time`, `acc`).

## The coroutine mechanism it implements (how it yields/resumes within one cog)

The whole switch is **one location**:

```
swap
swap_ret        jmp         #pong          'Initialized to point at pong.
```

`swap` and `swap_ret` label the *same* instruction. Every yield is `call #swap`. On the P8X32A, `call` is a `jmpret` in disguise: it jumps to `swap` **and** stuffs the address of the instruction *after the call* into `swap`'s **source field** (its jump target), self-modifying the single `jmp` in place.

Because of the Propeller's 4-step execution sequence (fetch → write-previous-result → source-fetch → dest-fetch), the **old** target stored in `swap` is read and taken *before* the new return address overwrites it. So each `call #swap`:

1. reads the currently-stored target (the *other* coroutine's resume point) and jumps there, while
2. simultaneously recording *this* caller's resume point into `swap` for next time.

The result is a strict ping-pong: control alternates `ping ⇄ pong`, each side always re-entering exactly where it last yielded. No stack, no interrupt, no second cog — one shared `jmp` slot ferries two execution contexts. Seed direction is set by initializing `swap_ret jmp #pong`.

### Caveats the code teaches (carried from the prose)

- A shared scratch variable (`acc`) is safe **only if its value need not survive a `call #swap`** — the complement may clobber it.
- **C and Z flags are not preserved across `swap`.** The appnote's flag save/restore idioms (`muxnz`/`muxc` into a restore-instruction or an external `flags` long, then `test`) are the documented fix; they appear in the prose, not in this example file.

## LOC

~103 non-blank lines (134 total incl. banner/license comments). Roughly 35 lines of executable PASM1 + Spin1; the remainder is the documentation header, section banners, and the MIT license block.
