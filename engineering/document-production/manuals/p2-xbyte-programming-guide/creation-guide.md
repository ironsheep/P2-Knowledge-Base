# P2 XBYTE Programming Guide - Creation Guide

**Canonical Name:** `p2-xbyte-programming-guide`
**Document Title:** P2 XBYTE Programming Guide
**Subtitle:** Building Interpreters and Emulators on the Propeller 2
**Created:** 2026-06-26
**Model:** P2 Streamer Programming Guide (layout, two-register voice, richness)

---

## 1. Document Identity

### 1.1 Purpose and Scope

This guide does two complementary jobs. It **teaches** what XBYTE is, why the P2 has it, and how to think about it — the conceptual understanding a reader needs before the details mean anything — and it serves as the **reference** for the engine: the dispatch cycle, the arming sequence, the table-size and compression modes, the instruction set XBYTE is built from, and the configuration bits. It consolidates the Silicon Doc, the KB YAML, and worked code into a single authoritative source, written in two registers (see `voice-guide.md` §1.4): a warm teaching register for the conceptual chapters and chapter openers, and a precise reference register for the tables, encodings, and specifications.

**This document IS:**
- A conceptual introduction to XBYTE — what it is, why it exists, when to reach for it
- A complete explanation of the skip family (SKIP / SKIPF / EXECF) as the foundation XBYTE is built from
- A reference for the dispatch cycle, arming, table-size/compression modes, and the F bit
- A practical guide that builds a small custom VM and a tiny illustrative CPU emulator (6502), with working, compiled code

**This document is NOT:**
- A general PASM2 tutorial — it assumes familiarity with cog/hub/LUT architecture, basic PASM2, and the FIFO
- A faithful or complete emulator — the capstone 6502 and the 6809 vignette are deliberately *tiny & illustrative* teaching artifacts (see §5.1), not reference implementations
- A survey of architectures similar to the P2 — that material is explicitly out of scope for this edition (see PLANNING.md)

### 1.2 Target Audience

Developers who want to:
1. **Build an interpreter or a custom VM** on the P2 with hardware-accelerated dispatch
2. **Emulate a small CPU** (8-bit micros are the sweet spot)
3. **Understand the skip family** (SKIP/SKIPF/EXECF) and use it well, with or without XBYTE
4. **Read or debug** XBYTE-based code

**Assumed Knowledge:** P2 cog/hub/LUT architecture; basic PASM2; the hub FIFO (RDFAST/RFxxxx); the hardware stack and `_RET_`.

### 1.3 Relationship to Other Manuals

| Manual | Relationship |
|--------|-------------|
| **P2 Assembly Language Manual** | Documents the individual instructions (SKIP/SKIPF/EXECF/SETQ/SETQ2/RDFAST/RFxxxx); this guide covers their *use to build a dispatch engine* |
| **P2 Streamer Programming Guide** | Sibling reference on another autonomous P2 engine; this guide follows its layout and voice |
| **DeSilva PASM Style** | A true step-by-step tutorial; this guide teaches concepts and explains the hardware, but is not a guided build |

---

## 2. Document Architecture

```
FRONT MATTER
├── Title Page (single-image cover, subtitle, v0.1.0)
├── Copyright / License / Acknowledgments / Sources
├── How to Use This Guide
└── Conventions + Enhancement Markers

PART I: XBYTE FUNDAMENTALS (teaching)
├── Chapter 1: Understanding XBYTE
├── Chapter 2: The Skip Family (SKIP / SKIPF / EXECF)
├── Chapter 3: The Bytecode Stream (FIFO)
└── Chapter 4: LUT Dispatch

PART II: THE XBYTE ENGINE (reference)
├── Chapter 5: The Dispatch Cycle
├── Chapter 6: Arming XBYTE (SETQ / SETQ2 / $1FF)
├── Chapter 7: Table-Size & Compression Modes
└── Chapter 8: Bytecode Routines

PART III: BUILDING A VM (practical)
├── Chapter 9: A Minimal Custom VM
├── Chapter 10: Mapping CPU Families onto XBYTE
├── Chapter 11: A Tiny CPU Emulator (6502 capstone)
└── Chapter 12: The 6809 SETQ2 Vignette

PART IV: REFERENCE (lookup)
├── Chapter 13: Instruction Reference
└── Chapter 14: Configuration Constants & Patterns

APPENDICES
├── A: XBYTE Quick Reference
├── B: Instruction Encoding Summary
├── C: Further Implementations (external links only)
└── D: Troubleshooting

INDEX
```

**Part rationale.** Part I builds the mental model — and, per the locked pedagogy, teaches the **skip family first**, because EXECF/SKIPF *are* what XBYTE is built from. Part II is the engine reference: the cycle, the arming, the modes, the routine rules. Part III proves the engine by building (a minimal VM, then a tiny 6502). Part IV is fast lookup.

---

## 3. Pedagogical Framework

This guide reuses the two-register learning model of the Streamer guide (`../p2-streamer-programming-guide/creation-guide.md` §3): the **teaching layer** uses advance organizers, motivation-before-mechanism, concrete imagery, and differentiation-by-contrast; the **reference layer** serves learning through consistent structure, pattern recognition, and reliable findability. The markers (⚠️ 💡 🔧) compress hard-won wisdom into dense, findable notes.

**XBYTE-specific pedagogical decision (LOCKED):** teach **SKIP/SKIPF/EXECF first** (Ch. 2), then reveal XBYTE (Ch. 4–5) as "the hardware that runs an EXECF dispatch for you, once per bytecode, for free." The reader meets the engine's parts as ordinary instructions before meeting the engine, so the engine is demystified rather than magical.

---

## 4. Source Materials

### 4.1 Primary Sources

| Source | Location | Content | Authority |
|--------|----------|---------|-----------|
| **Silicon Doc v35 — XBYTE section** | `engineering/ingestion/sources/silicon-doc/` (`part2-code-blocks.txt`, `part2-beginning.txt`) | the dispatch walk, overhead figures, mode/compression table, F bit, arming | PRIMARY — hardware truth |
| **XBYTE engine YAML** | `deliverables/ai/P2/architecture/xbyte_engine.yaml` | structured XBYTE reference (cycle, modes, registers, constraints) | PRIMARY — KB |
| **Instruction YAML** | `deliverables/ai/P2/language/pasm2/{skip,skipf,execf,setq,setq2,rdfast,rfbyte,rfvar,rfvars,getptr}.yaml` | encodings, syntax, flag effects, timing | PRIMARY — KB |
| **Grounding digest** | `./audit/xbyte-source-grounding-digest-2026-06-26.md` | the above, compiled + cross-checked, with citations | derived — cite the primaries it points to |

**Guest-CPU facts** (6502, 6809) for Part III are stable historical ISA facts (not P2 claims); the **PASM2 that emulates them must compile with `pnut-ts`**. **Appendix C** external-project facts (Arc8de, the Yume suite) are gathered + verified from the project pages/repos (or carried from PLANNING.md §8, already verified) — never from memory; each entry = URL + author + what-it-emulates + license.

### 4.2 Authority Hierarchy

1. **Silicon Doc** — hardware behavior is ground truth
2. **KB YAML** — structured derived truth (aligned to the Silicon Doc)
3. **Compiled example code** — `pnut-ts`-proven patterns
4. **External project pages** — Appendix C references only

### 4.3 Content Verification Protocol (Hallucination Prevention)

Hallucinations occur **at the moment of writing**. Before writing any XBYTE claim:

1. **What am I claiming?** (cycle / mode bits / encoding / register / overhead)
2. **Which source contains it?** (Silicon Doc XBYTE section / instruction YAML / xbyte_engine.yaml)
3. **Can I cite the exact location?** (file + section/line via the grounding digest)
4. **Does the source say this exactly?** YES → write it; extrapolating → don't; absent → mark unverified / log a finding.

**Red-flag phrases — STOP and verify:** "automatically" (XBYTE requires explicit arming), "synchronizes," "optimizes," "eliminates," "also provides," "side effect," vague "enables." And the banned class: any **Spin2-method interpreter clock timing** — cite the 6-clock *hardware* overhead or describe the code path instead.

---

## 5. Content Specifications

### 5.1 The "Tiny & Illustrative" charter (LOCKED)

The minimal VM (Ch. 9), the 6502 capstone (Ch. 11), and the 6809 vignette (Ch. 12) are **teaching artifacts**: enough to show the technique end-to-end and to compile with `pnut-ts`, explicitly **NOT** complete or faithful emulators. Neither we nor a future contributor should over-build them. Each such chapter states this limit in its opener.

### 5.2 Chapter / Entry Format

- Teaching opener (register: teaching) — what this mechanism is for, how the pieces differ.
- Reference body (register: reference) — tables (cycle, modes, encodings), bit-fields, per-instruction detail.
- Worked code — PASM2 (and Spin2 where clearer), comments explaining *why*, K ≤ 76 columns, compiled.
- Markers — ⚠️ Pitfall / 💡 Tip / 🔧 Hardware where they earn their keep.
- Cross-references — direct ("See Chapter 7"; "Related: SKIP, SKIPF, EXECF").

### 5.3 Code Example Standards

- Complete and compilable with `pnut-ts` (use `-d` if a debug() directive appears).
- Comments explain purpose, not the instruction name.
- No line-wrapping; over-long lines are an authorship defect (see Code Line Budget).
- Show the symbolic constants the compiler knows; validate symbol↔value off to the side.

---

## 6. Production Workflow

1. **Edit** `opus-master/{front-matter,xbyte-body}.md` (canonical source).
2. **prepare-manual** — `assemble-manual.sh` (prepend front matter) + `latex-escape-all.sh`; stage CHANGED files to `../../outbound/p2-xbyte-programming-guide/`.
3. **PDF Forge** (user) — generate `P2-XBYTE-Programming-Guide.pdf` on the manual-store Forge.
4. **Verify** the render — page count, outline, key sections, compile log (guard against silent content-drop), marker rendering, code-box style, K-budget.
5. **Audit** — `document-audit` at the chosen depth against this guide + the grounding digest.

**Workspace:** `engineering/document-production/workspace/p2-xbyte-programming-guide/`
**Outbound:** `engineering/document-production/outbound/p2-xbyte-programming-guide/`
**Template:** `p2kb-xbyte-reference` (platform stack + thin local).

---

## 7. Code Line Budget

Code boxes do **not** wrap — a typeset wrap can't break a comment and re-indent it, nor add a language line-continuation, so over-long code lines are an authorship defect to fix in source, not a template concern. The `prepare-manual` line-length audit (`engineering/tools/validation/audit-code-line-length.py`) flags any source code line wider than the budget below.

- **Max code columns (K): 76**
- **Code-box style / font:** the shared platform code-box family (`p2kb-platform-content.sty` — ```` ```spin2 ```` / ```` ```pasm2 ```` colored boxes). XBYTE is a **twin** that consumes the platform stack unchanged, so it **inherits the platform reference K = 76**. It does not re-measure unless it diverges its code font (it does not).

---

*Version: 0.1 - Initial Creation Guide (XBYTE), modeled on the Streamer guide*
*Created: 2026-06-26*
