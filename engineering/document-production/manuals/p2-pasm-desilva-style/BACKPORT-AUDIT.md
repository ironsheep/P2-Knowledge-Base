# DeSilva Manual Backport Audit

**Date:** 2025-12-06
**Purpose:** Identify content in workspace that must be backported to Opus Master

## Critical Finding

The workspace file (`P2-PASM-deSilva-Style.md`) has diverged significantly from the Opus Master (`COMPLETE-OPUS-MASTER.md`). The workspace contains substantial improvements and PDF-specific formatting that were NEVER backported to the canonical source.

---

## Summary of Differences

| Category | Workspace | Opus Master | Action Required |
|----------|-----------|-------------|-----------------|
| Line count | 5717 | 2315 | Workspace is authoritative for Chapters 1-3 |
| Title page | LaTeX raw block | None | Keep separate (PDF-specific) |
| Clock speed | 200 MHz throughout | 100 MHz | Backport 200 MHz |
| Code fencing | `::: pasm2` divs | ` ```pasm2 ` | Standardize |
| "Why P2?" section | Present | **MISSING** | **BACKPORT** |
| "Clock Preamble" sidetrack | Present | **MISSING** | **BACKPORT** |
| Register terminology note | Present | **MISSING** | **BACKPORT** |
| Labels section | Missing | Present (today's work) | Forward-port |
| Local label fixes | Not applied | Applied | Forward-port |

---

## Content ONLY in Workspace (Must Backport)

### 1. "Why P2?" Section (Lines 255-273)
**Location:** Chapter 1, before "The Hook: Making Light"

```markdown
## Why P2?

Before we dive into code, let me tell you why you're in for something different.

If you've fought with interrupt priority conflicts on an ARM, watched your timing jitter because of cache misses, or discovered that the UART you need is only available on pins you're already using... well, the P2 was designed by someone who got tired of those problems too.

Here's the P2 philosophy in a nutshell:

**Instead of one processor fighting with interrupts**, you get eight complete, identical processors (COGs) that run truly in parallel. Your serial handler never delays your motor control. Your sensor sampling never misses a deadline. Each task owns its own processor.

**Instead of fixed peripherals**, every one of the 64 pins contains its own programmable state machine. Any pin can become a UART, PWM output, quadrature encoder, ADC - whatever you need, wherever you need it.

**Instead of timing that depends on cache luck**, the hub memory has deterministic access. Your timing loops work the same way every time.

**Instead of calling math libraries**, there's a hardware CORDIC that computes sine, cosine, and arctangent in exactly 55 clocks. Every time.

Does this mean P2 is perfect for everything? Of course not. But if your projects involve multiple real-time tasks, precise timing, video or audio generation, or just running out of peripheral pins - you're in the right place.

For a full comparison to ARM, ESP32, Arduino, and PIC platforms, see [Appendix A](#appendix-a-platform-comparison). But you probably want to blink that LED first, don't you?
```

### 2. Clock Preamble Sidetrack (Lines 342-359)
**Location:** Chapter 1, after "But Wait, There's More!"

```markdown
::: sidetrack
### The Clock Preamble

Notice the `CON` section at the top of that example? Every P2 program needs to configure its system clock:

::: pasm2
```
CON
  _clkfreq = 200_000_000  ' 200 MHz system clock
```
:::

This tells the P2 to run at 200 MHz using your board's crystal oscillator. Without it, the chip runs at a sluggish ~20 MHz on its internal RC oscillator—and timing-dependent code (including DEBUG output) won't behave as expected.

At 200 MHz with most instructions taking 2 clocks, each COG executes approximately 100 million instructions per second (100 MIPS). With 8 COGs running in parallel, that's 800 MIPS of total processing power—and that's before Smart Pins start handling I/O autonomously.

**From here on, we'll omit this preamble from examples to keep them focused on the concept being taught.** When you create your own files, always include it at the top before your `PUB` or `DAT` sections.
:::
```

### 3. Register Terminology Note (Line 383)
**Location:** Chapter 1, after "Let's Make It Better"

```markdown
*A note on terminology: P2 documentation often uses "register" to refer to any long in COG RAM. Unlike ARM or x86 where registers are a small, special set (R0-R15, EAX, etc.), every COG RAM location can be used as a general-purpose register. However, the last 16 locations (addresses 496-511) are reserved for special-purpose registers, so avoid those for your variables. When you see "register" in P2 context, think "COG RAM location."*
```

### 4. 200 MHz Timing Values (Throughout)
**All code examples use 200 MHz timing:**
- `##50_000_000` for 0.25 second delays (not `##25_000_000`)
- `##20_000_000` for 0.1 second short pulses
- `##60_000_000` for 0.3 second long pulses
- Comments reference "at 200 MHz" or "at 200MHz"

### 5. CON Block in Code Examples
**Workspace includes CON block in first example:**
```pasm2
CON
  _clkfreq = 200_000_000        ' 200 MHz system clock

DAT
' LED Blinker - Your first PASM2 program!
        org     0               ' Start at COG address 0
```

### 6. Enhanced Preface Sections
**Workspace has different header levels and slight wording:**
- Uses `###` for subsections in Preface
- Includes slight formatting differences

### 7. Pedagogical Fenced Divs
**Workspace uses `::: pasm2`, `::: spin2`, `::: sidetrack`, `::: medicine-cabinet`**
These are Pandoc fenced divs for PDF styling. Need to standardize.

---

## Content ONLY in Opus Master (Already Applied Today)

### 1. Labels Section (Lines 1038-1144)
**"Labels: Naming Your Places"** - Complete section on global/local labels

### 2. Local Label Fixes
All loop labels changed from `loop` to `.loop`, etc.

### 3. REP Enhancement
Label form added alongside count form

### 4. COG Limit Fix
Changed `##1000-1` to `##128-1`

---

## Formatting Differences

### Header Levels
| Section | Workspace | Opus Master |
|---------|-----------|-------------|
| License | `###` | `##` |
| Trademarks | `###` | `##` |
| Disclaimer | `###` | `##` |
| Preface subsections | `###` | `##` |

### Dedication Format
- **Workspace:** Inline paragraphs
- **Opus Master:** Uses `---` dividers and `## To deSilva` headers

### Code Blocks
- **Workspace:** `::: pasm2` + ` ``` ` (fenced div wrapping)
- **Opus Master:** ` ```pasm2 ` (language hint only)

---

## Recommended Migration Strategy

### Option A: Workspace as Truth (RECOMMENDED)
1. Backup Opus Master
2. Replace Opus Master chapters 1-3 with workspace content
3. Apply today's label fixes to the merged content
4. Strip PDF-specific LaTeX blocks (keep in separate file)
5. Standardize code block format

### Option B: Surgical Backport
1. Add "Why P2?" section to Opus Master Chapter 1
2. Add "Clock Preamble" sidetrack
3. Add register terminology note
4. Update all timing values to 200 MHz
5. Verify nothing else missing

---

## Files Involved

| File | Role |
|------|------|
| `workspace/p2-pasm-desilva-style/P2-PASM-deSilva-Style.md` | Workspace with PDF formatting (5717 lines) |
| `opus-master/COMPLETE-OPUS-MASTER.md` | Canonical source with today's fixes (2315 lines) |
| `opus-master/CHAPTERS-7-16-ENHANCED.md` | Later chapters (2707 lines) |

---

## Next Steps

1. Create backup of Opus Master
2. Execute chosen migration strategy
3. Verify all content preserved
4. Apply label fixes uniformly
5. Test PDF generation

---

*Audit completed: 2025-12-06*
