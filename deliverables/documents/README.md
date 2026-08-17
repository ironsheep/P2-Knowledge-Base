# P2 Generated Documents

> PDF documents generated from the P2 Knowledge Base.


[![License: CC BY-SA 4.0](https://img.shields.io/badge/license-CC%20BY--SA%204.0-brightgreen.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

These documents are licensed **CC BY-SA 4.0**: share and adapt them, including
commercially, with attribution and under the same terms.

## About These Documents

This documentation is produced differently than traditional technical manuals. These are built with **AI assistance under human direction**. The AI work is structural: drafting, organizing, and carrying facts across from the documentation we've ingested. What goes into a manual, how it's organized, and what's worth saying are human calls, as are the source curation and the review.

**Our process emphasizes source fidelity:**
- Source material is rigorously gathered from official Parallax documentation, datasheets, and authoritative community references
- Code examples are compiled and validated using `pnut_ts` wherever possible
- Content is cross-referenced against the project's structured YAML knowledge base

**What this means for community review:**

Because these documents are AI-assisted, the issues you may encounter differ from traditionally authored manuals. Watch for:

- **Plausible but incorrect details.** Specifications that sound right but aren't (wrong clock cycles, flag behaviors, register addresses)
- **Overgeneralization.** Statements presented as universal that have exceptions or edge cases
- **Missing practitioner context.** Technically accurate but lacking the practical insight experienced users know
- **Logic errors in examples.** Code that compiles but doesn't behave as described
- **Terminology drift.** Nearly-correct terms that could mislead

**Your expertise is essential.** This review process depends on practitioners who know the Propeller 2 to catch what automated validation cannot. If something looks wrong, seems incomplete, or contradicts your experience, **[report it via the Issues page](https://github.com/ironsheep/P2-Knowledge-Base/issues)**.

## How These Documents Are Built, and Why You Can Trust Them

Two short companion reads go deeper on the questions every reviewer asks:

**[Why You Can Trust What's in These Manuals](WHY-YOU-CAN-TRUST-THESE-MANUALS.md)**: how a fact gets *into* a manual and how we check it. Jump to: [checked against the silicon](WHY-YOU-CAN-TRUST-THESE-MANUALS.md#checked-against-the-silicon) · [we audit our own work](WHY-YOU-CAN-TRUST-THESE-MANUALS.md#we-audit-our-own-work) · [when you report a problem, it ships](WHY-YOU-CAN-TRUST-THESE-MANUALS.md#when-you-report-a-problem-it-ships).

**[How These Manuals Are Made, and How They Stack Up](HOW-THESE-MANUALS-ARE-MADE.md)**: the craft, measured honestly against how the best reference manuals in the world are produced. Jump to: [the bar we measured against](HOW-THESE-MANUALS-ARE-MADE.md#the-bar-how-the-best-reference-manuals-get-made) · [where we go past a printed book](HOW-THESE-MANUALS-ARE-MADE.md#where-we-go-past-what-a-printed-book-can-do) · [where we don't match them yet](HOW-THESE-MANUALS-ARE-MADE.md#where-we-dont-match-them-yet).

## Documents in Community Review

Eight documents are available now for community technical review, along with seven application notes. We welcome feedback on accuracy, completeness, and clarity. (PDF links download the file directly.)

### [Getting Started with the Propeller 2](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2-Getting-Started-Guide.pdf)
**Meet the Chip, Read Its Code, Put It to Work** · *Version 1.0.3*

The friendly on-ramp to the Propeller 2, the orientation layer that sits below the reference manuals. It builds a mental model of the chip (eight cogs, smart pins, the CORDIC solver, the streamer, the memory tiers, and boot), teaches you to read P2 code (Spin2 and PASM2 structure), and puts it to work with hands-on, compile-clean examples, then points you to the reference manuals for depth and to the *P2 Architect's Guide* for whole-system design. Migration sidebars throughout call out what's the same, changed, or new coming from the Propeller 1.

*August 2026 - Community Review Edition* | [Changelog](DOCs/p2-getting-started-guide-changelog.md)

### [P2 Assembly Language Reference Manual](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2-Assembly-Language-Manual.pdf)
**Complete PASM2 Instruction Set Documentation** · *Version 3.1.5*

The definitive reference for P2 assembly language programming. Documents all PASM2 instructions with accurate syntax, encoding tables, behavior descriptions, and practical examples. Organized alphabetically for quick lookup, with comprehensive coverage of directives, special registers, and predefined constants. Includes architectural foundation chapters on execution models, instruction formats, flags, timing, and hardware integration.

*August 2026 - Community Review Edition* | [Changelog](DOCs/p2-assembly-language-manual-changelog.md)

### [P2 Assembly Programming](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2-PASM-deSilva-Style.pdf)
**A Human-Centered Approach to Parallel Processing** · *Version 3.0.6*

This tutorial follows in the footsteps of deSilva's legendary P1 Assembly Tutorial, bringing the same approachable, hands-on teaching style to the Propeller 2. Starting with a blinking LED and progressing through cog architecture, hub memory, CORDIC math, Smart Pins, and multi-cog coordination, this manual makes PASM2 genuinely enjoyable to learn. Written with the philosophy: "Learn by doing, celebrate progress, have fun!"

*August 2026 - Community Review Edition* | [Changelog](DOCs/p2-pasm-desilva-style-changelog.md) | [Example Library (ZIP)](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/p2-pasm-desilva-style-src.zip)

### [P2 Streamer Programming Guide](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2-Streamer-Programming-Guide.pdf)
**A Guide to the Propeller 2 Streamer, Its Modes and Function** · *Version 1.0.8*

An introduction to the P2 streamer, the DMA-like engine that moves data between hub RAM, pins, and DACs, built to make a genuinely tricky part of the chip make sense. Covers every streamer mode (immediate, RDFAST/WRFAST, RGB video, ADC sampling, DDS/Goertzel), NCO timing and frequency calculation, DAC channel routing and pin control, and application patterns for video output, high-speed serial, and signal processing. Includes a complete mode encoding table and a clickable index.

*August 2026 - Community Review Edition* | [Changelog](DOCs/p2-streamer-programming-guide-changelog.md)

### [P2 Debug Window Manual](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2-Debug-Window-Manual.pdf)
**See What Your Program Is Doing: Nine Display Windows for the Propeller 2** · *Version 1.1.2*

The complete guide to the P2's nine DEBUG display windows: TERM, BITMAP, PLOT, LOGIC, SCOPE, SCOPE_XY, FFT, SPECTRO, and MIDI. Documents every window's directives, parameters, ranges, and defaults, with a worked, software-only example in each chapter (thermal heatmap, PID strip-chart, glitch capture, motor run-up, and more) that runs on a bare P2 board with no wiring. Integration chapters cover packed-data high-rate transfer, multiple windows and PASM debugging, host keyboard and mouse input, and live control and status panels. Every load-bearing claim is verified against P2 silicon. Includes a downloadable example library of 34 compile-clean Spin2 programs.

*August 2026 - Community Review Edition* | [Changelog](DOCs/p2-debug-window-manual-changelog.md) | [Example Library (ZIP)](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/p2-debug-window-manual-src.zip)

### [P2 I/O & Smart Pins User Guide](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2-IO-and-Smart-Pins-User-Guide.pdf)
**Complete P2 Pin I/O and Smart Pin Reference** · *Version 1.0.8*

The complete reference for the Propeller 2's pin I/O and Smart Pins, working up from direct pin control through the smart pin architecture to all 32 smart pin modes. Chapters organized by function (digital, pulse/transition, NCO, PWM, DAC, serial, timing, counting, period/frequency, ADC, repository, USB) give register-level configuration, worked Spin2 and PASM2 examples, and a "where you'd use this" framing, with hardware-grounded coverage of the details that bite: init ordering, IN-flag handshakes, data justification, and measurement math. Reference appendices provide a task-oriented intent index, the full P\_ constant tables, a formulas reference, mode-comparison charts, a troubleshooting guide, a complete 32-mode register reference, and FPGA board differences. Includes a downloadable library of 15 compile-clean Spin2 example programs that run on a bare P2 board.

*August 2026 - Community Review Edition* | [Changelog](DOCs/p2-io-and-smart-pins-user-guide-changelog.md) | [Example Library (ZIP)](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/p2-io-and-smart-pins-user-guide-src.zip)

### [The P2 Architect's Guide](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2-Architect-Guide.pdf)
**Thinking in Cogs, Pins, and Forces** · *Version 1.0.3*

The design-and-realization companion to the reference manuals, picking up where *Getting Started with the Propeller 2* leaves off. It moves in three acts: getting a real project off the ground (choosing hardware and buses, spending the pin budget, getting the parts to talk), then **deriving** the software architecture from physical forces rather than guessing it (which cog owns what, how the pieces talk across the gaps, how mismatched rates are matched), and finally walking the whole process again with an AI agent at your side. It teaches a method, not a catalogue. Its two worked derivations are demonstrations on deliberately different hardware, never templates, and it's grounded throughout in the P2 Knowledge Base and in real, hardware-verified projects.

*August 2026 - Community Review Edition* | [Changelog](DOCs/p2-architect-guide-changelog.md)

### [P2 Interpreters & Emulators Guide](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2-XBYTE-Programming-Guide.pdf)
**The XBYTE Engine and Bytecode Dispatch on the Propeller 2** · *Version 1.0.1*

The complete guide to the Propeller 2's XBYTE hardware bytecode engine: the skip family (SKIP/SKIPF/EXECF), the FIFO bytecode stream, and LUT dispatch that together let one indexed jump select and run a handler with no software in the loop. It works up from what the engine is and how it dispatches each bytecode to building on it: a minimal custom virtual machine, then, where the engine fits the guest, a compact, illustrative CPU emulator, with chapters on servicing guest interrupts, prefix bytes and alternate tables, and using the engine beyond interpreters to parse protocols and drive displays. Written in two registers, a warm teaching layer for the concepts and a precise reference layer for the tables, encodings, and configuration bits, and grounded throughout in the P2 documentation, the knowledge base, and worked community code. Includes a downloadable library of two compile-clean Spin2 example programs.

*August 2026 - Community Review Edition* | [Changelog](DOCs/p2-xbyte-programming-guide-changelog.md) | [Example Library (ZIP)](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/p2-xbyte-programming-guide-src.zip)

### Application Notes

Worked, task-specific companions to the reference manuals. Each pairs a focused technique with compile-clean, runnable code.

#### [Measure an Absolute Voltage in Microvolts on a P2 Pin](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2AN001.pdf)
**Application Note P2AN001 · Single-Pin Instrumentation ADC** · *Version 1.0.4*

Read an absolute voltage in microvolts on a single P2 pin using only the built-in smart-pin sigma-delta ADC, no external converter. It measures the chip's own internal references alongside the pin and takes a ratio, so supply and temperature drift divide out and the reading is absolute. One clean base measurement comes first, then a small catalog of techniques to choose among: three pins for lower noise, a filter cascade that hands you every rate at once, a series resistor to read above 3.3 V, and mains-cycle averaging to erase 50/60 Hz hum, plus a reference eight-channel design. Every worked program compiles clean and runs on a bare P2 board with a single jumper wire.

*August 2026 - Community Review Edition* | [Changelog](DOCs/p2an001-changelog.md) | [Example Library (ZIP)](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2AN001-src.zip)

#### [CORDIC for Real Work](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2AN002.pdf)
**Application Note P2AN002 · Hardware Math on the P2** · *Version 1.0.3*

Put the Propeller 2's shared hardware CORDIC solver to real work, the engine that turns a rotation, a sine, a square root, or a full 64-bit multiply into a single queued operation with a fixed latency. Six runnable recipes to choose among: distance and heading, point rotation, circle layout, sine and cosine waves, 64-bit-safe fixed-point scaling, and pipelining to retire one result every eight clocks, plus a field-oriented motor-control reference design. Because the CORDIC computes exact, deterministic math, every recipe checks against a closed-form answer you can derive by hand, with no bench instruments.

*August 2026 - Community Review Edition* | [Changelog](DOCs/p2an002-changelog.md) | [Example Library (ZIP)](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2AN002-src.zip)

#### [Generate Analog Waveforms and Audio on a P2 Pin](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2AN003.pdf)
**Application Note P2AN003 · DAC & Analog Signal Generation** · *Version 1.0.2*

Turn a single P2 pin into a 16-bit audio-quality analog output using only the built-in smart-pin DAC, no external converter. It dithers the pin's 8-bit DAC to an effective 16 bits and paces it from the smart pin's own sample clock, so a continuous signal is just the right sequence of numbers delivered on time. One shared output stage comes first, then five recipes to choose among: sample playback and waveform synthesis from a DDS phase accumulator, deliberate dither-mode and RC-filter choice for effective resolution, a real-time ADC-to-DAC passthrough, and multi-voice mixing with stereo panning, plus a 32-stream reference ceiling. Every worked program compiles clean and runs on a bare P2 board, with a one-jumper known-answer check that proves the whole signal path with no bench gear.

*August 2026 - Community Review Edition* | [Changelog](DOCs/p2an003-changelog.md) | [Example Library (ZIP)](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2AN003-src.zip)

#### [Read Real-World Sensors by Frequency, Rotation, and RC Timing on a P2 Pin](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2AN004.pdf)
**Application Note P2AN004 · Frequency / Rotation / RC-Timing Measurement** · *Version 1.0.2*

Read a resistive, capacitive, light, or rotary sensor directly on a single P2 pin. The smart pin times, counts, or decodes the signal in hardware and the cog just reads the answer, with no external counter or ADC. One shared idea comes first, then three runnable instruments to choose among by what you're reading: an RC-decay reader that times a capacitor's discharge through a photocell, thermistor, or pot; a light-to-frequency reader that turns a TSL235R's output frequency into an irradiance with a reciprocal frequency counter; and a drop-in quadrature-knob instrument with detent normalization, preset, a range clamp, and a debounced button. Every worked program compiles clean and runs on a bare P2 board. The encoder self-verifies with two jumper wires and a known-answer detent count, while the analog recipes carry no invented readings and defer their absolute calibration to a hardware pass.

*August 2026 - Community Review Edition* | [Changelog](DOCs/p2an004-changelog.md) | [Example Library (ZIP)](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2AN004-src.zip)

#### [Run Several Cooperative Jobs in One P2 Cog](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2AN005.pdf)
**Application Note P2AN005 · Cooperative Multitasking with Spin2 TASK Methods** · *Version 1.0.2*

Run several cooperative jobs in one cog with Spin2's TASK methods. Each job runs until it voluntarily yields, so they take turns with no preemption and no locks. One shared idea comes first, then four runnable recipes to choose among by need: a two-task round-robin that blinks two LEDs at independent rates from a single cog, a cooperative yield that keeps a second job responsive inside a long computation, halt/resume flow control where a consumer pauses and wakes its producer, and a live task dashboard with a clean shutdown. Every worked program compiles clean under the P2 toolchain and runs on a bare board; live scheduling behavior is described from the language documentation and defers its bench confirmation to a hardware pass. The modern replacement for the hand-coded PASM coroutine.

*August 2026 - Community Review Edition* | [Changelog](DOCs/p2an005-changelog.md) | [Example Library (ZIP)](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2AN005-src.zip)

#### [Size Cog and Task Stacks, and Catch Overflow Before It Corrupts Memory](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2AN006.pdf)
**Application Note P2AN006 · Sizing Cog & Task Stacks** · *Version 1.0.1*

Size the stack buffers that new cogs and cooperative tasks need, where an undersized stack silently overwrites hub memory with no hardware trap. One shared idea comes first (fill the stack with a known pattern and watch a sentinel just past its end), then four runnable recipes: instrument a new-cog stack against overflow, find the high-water mark and right-size, pinpoint which routine overran the stack, and size a cooperative task's stack. Built around a small MIT-licensed stack-check utility that ships in the example library; every recipe compiles clean under the P2 toolchain. The companion to the cooperative-multitasking note.

*August 2026 - Community Review Edition* | [Changelog](DOCs/p2an006-changelog.md) | [Example Library (ZIP)](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2AN006-src.zip)

#### [Share Data Between Cogs Without Ever Reading It Half-Written](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2AN007.pdf)
**Application Note P2AN007 · Data Structures with the New Language Facilities** · *Version 1.0.1*

Spin2's STRUCT facility gives the P2 real records: named, typed, packed fields you reach by name instead of juggling parallel arrays. Within one cog that's a convenience; across cogs it's a design question, because a single hub long is written atomically but a multi-field record is not. One shared idea comes first (write the record's fields, then flip one long that publishes them), then six runnable recipes: an in-cog record and array, a lock-free ring buffer, a latest-wins mailbox, a lock-guarded multi-writer queue, a whole record packed into one atomically-published long using the newer member bitfields, and computed member offsets with OFFSETOF for the places raw addressing is unavoidable. Every cross-cog claim is confirmed on real P2 silicon with two cogs actually contending, each discipline measured against a deliberately-broken version of itself. The first document to cover the STRUCT facilities Spin2 has added since records arrived.

*August 2026 - Community Review Edition* | [Changelog](DOCs/p2an007-changelog.md) | [Example Library (ZIP)](https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/DOCs/P2AN007-src.zip)

## The Full Documentation Set

Beyond the documents in review above, here is the complete planned set, so you can see where the whole library is headed. Titles and scope of the not-yet-released items may still evolve.

### In Development & Planned

The rest of the set, in production or on the drawing board:

#### P2 Single-Step Debugger Manual
**Observe and Control Your Running P2 Code**

A practical guide to single-stepping P2 code: pausing and resuming a running program, inspecting values and timing, and driving the debugger from the host.

#### Application Notes in Planning

Further worked companions under consideration:

- **Extended-Precision Integer Math.** 64/96/128-bit integer math built from the carry-chain instructions
- **Fixed-Point Math on the P2.** Fractional math without a floating-point unit
- **Data Structures with the New Language Facilities.** In-cog and cross-cog queues, lists, and FIFOs
- **USB Device/Host with Smart Pins.** Building a working USB device or host on the smart pins


## Reporting Issues

Found an error or have feedback? We appreciate your help improving these documents!

**[Report a Document Defect](https://github.com/ironsheep/P2-Knowledge-Base/issues/new?template=document_defect.yml)**: use this when you found an error and know (or can reference) the correct information. Include page number, nearest heading, and source reference.

**[Provide Document Feedback](https://github.com/ironsheep/P2-Knowledge-Base/issues/new?template=document_feedback.yml)**: use this for suggestions, unclear content, missing information, or when something seems wrong but you're not sure of the fix.

For issues with AI-generated code or the underlying YAML/JSON knowledge base, see:
- [AI Defect Report](https://github.com/ironsheep/P2-Knowledge-Base/issues/new?template=ai_defect_report.yml) : when AI generates incorrect P2 code
- [AI Content Defect](https://github.com/ironsheep/P2-Knowledge-Base/issues/new?template=ai_content_defect.yml) : errors in YAML/JSON knowledge base files


## Generation

Documents are generated using PDF Forge from markdown sources we've authored.

---

*Built with intention for the P2 community*
