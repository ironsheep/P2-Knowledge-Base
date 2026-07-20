# P2 Manual / Reference Coverage by Capability Domain

> **Status:** v1 (2026-06-29), *Capability Coverage & App-Note Roster* sprint —
> groundwork for the coverage matrix (Phase 6, #137). This is the **"manual
> coverage" column** of the matrix: for each spine domain, what existing P2
> **manuals** (the human docs) and **reference YAMLs** (`deliverables/ai/P2/`)
> systematically cover — and, critically, *what kind* of coverage (reference vs.
> guided-application). Sources: `PUBLICATION-ROSTER.md` (live manuals) +
> `deliverables/ai/P2/{architecture,language,guides}/`.

## Live P2 manuals → domain

| Manual | Primary domain | Coverage type |
|---|---|---|
| P2 I/O & Smart Pins User Guide ("Blue Book", 387pp) | **B** Smart Pins & I/O | systematic reference — *the* B manual |
| P2 Assembly Language Reference (PASM2, 503pp) | **A** (instruction set) | reference — every PASM2 instruction; touches all domains but as ISA, not application |
| DeSilva PASM2 Tutorial (162pp) | **A** | tutorial — learning PASM2 |
| P2 Streamer Programming Guide (68pp) | **D** Streaming & video gen | systematic reference |
| P2 Interpreters & Emulators Guide (XBYTE) (v1.0.0, released) | **D** (XBYTE engine) | reference |
| P2 Debug Window Manual (156pp) | **K** Dev tools | reference |
| P2 Single-Step Debugger Manual | **K** | reference |
| Getting Started with the P2 (25pp) | **K** / orientation | on-ramp (cross-cutting) |
| The P2 Architect's Guide (design book, in dev) | **A** / design | guided design (decomposition) |
| Spin2 Reference Manual (parked) | cross-cutting (Spin2 language) | reference |
| AI Privacy Guide | — | N/A (not P2-technical) |

## Reference YAMLs (`deliverables/ai/P2/architecture/` + `language/`) → domain
- **A:** `cog`, `cog_attention`, `event_system`, `interrupts`, `locks`, `multi_resource_management`, `system-registers`, `language/pasm2`, `language/spin2`, `language/fundamentals`
- **B:** `smart_pins`, `smart_pin_patterns`, `smart-pins/`, `io_pin_timing`
- **C:** `cordic`
- **D:** `streamer/`, `fifo`, `xbyte_engine`
- **I:** `hub`, `lookup_ram`
- **A/K (system):** `clock_system`, `boot-rom`, `serial_loader`, `debug_interrupt`

## Coverage verdict by domain

| Domain | Manual coverage | Type | Note for the matrix |
|---|---|---|---|
| **A. Core compute model** | **Strong (reference)** | PASM2 ref + DeSilva + Architect's Guide + arch YAMLs (cog/events/interrupts/locks/multitasking) | ⚠️ Covered as **ISA reference + tutorial**, NOT as *guided application*. The P1-app-note topics here (multicore template, coroutines→multitasking, execution-timing, stack) have **no guided-composition tier** — this is the key app-note opening. |
| **B. Smart Pins & I/O** | **Strong** | the dedicated IOSP User Guide + smart_pin YAMLs | Well covered, reference + applied patterns. |
| **C. Math & DSP (CORDIC)** | **Partial** | `cordic.yaml` + PASM2-ref instructions; **no dedicated manual** | P2-unique; covered as instructions, not as a guided "using CORDIC for X" tier. |
| **D. Streaming & video gen** | **Good** | Streamer guide + XBYTE guide + streamer/fifo/xbyte YAMLs | Reference well covered. |
| **E. Comms & protocols** | **Weak** | only via smart-pin serial modes (IOSP); no comms manual | Inherently community/app-note territory (applications). |
| **F. Sensors & environment** | **None** | no manual; arch doesn't model sensors | Pure application domain → OBEX/QB/app-note. |
| **G. Displays & graphics** | **Weak** | video-gen *mechanism* in Streamer (D); display **drivers/GUI** unmanualed | Application domain → community/app-note. |
| **H. Motors & motion** | **None** | no manual | Application domain → community/app-note. |
| **I. Storage & memory** | **Partial** | `hub`/`lookup_ram` YAMLs; external RAM / SD / flash unmanualed | Subsystem (hub) covered; storage *applications* are community. |
| **J. Audio** | **None** | no manual | Application domain → community/app-note. |
| **K. Dev tools & workflow** | **Good** | Debug Window + Single-Step + Getting Started + getting-started guides | Well covered. |

## The pattern (feeds the roster)

1. **Manuals cover chip *subsystems* (A-reference, B, D, K) and the architecture
   YAMLs back A/C/I — the *application* domains (E/F/G/H/J) are barely manualed**,
   because they're applications, not subsystems. This is the placement rubric
   working as intended: *manuals document subsystems; applications are
   community/app-note territory.*
2. **Even where a domain is well-covered, the coverage is reference/ISA, not
   guided-application.** Domain A is the sharpest case: strong instruction-set and
   architecture coverage, but **zero guided-composition tier** for exactly the
   compute-model tasks the P1 app notes taught (multicore, coroutines, timing,
   stack). The manual column being "strong" here does NOT close the app-note gap.
3. **Implication for #137/#138:** the matrix's "manual coverage" cell must record
   coverage *type*, not just presence — a "strong reference" cell can still sit
   atop an app-note gap. The richest app-note candidates are where **reference
   coverage exists but guided-application does not** (domain A), and where an
   **application domain has community demos but no synthesizing guide** (E/F/G/H/J
   with QB/OBEX but no app note).

> Feeds the coverage matrix (#137) as the manual column; the OBEX + Quick Byte
> columns come from the catalogs (#132/#135), the P1 column from
> `p1-app-note-spine-mapping.md` (#136).
