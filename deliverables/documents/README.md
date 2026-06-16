# P2 Generated Documents

> PDF documents generated from the P2 Knowledge Base.


[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)

## About These Documents

This documentation is produced differently than traditional technical manuals. These are **AI-generated drafts, guided by human expertise** — a collaborative approach where AI assists in structuring and writing while humans provide direction, source material curation, and review.

**Our process emphasizes source fidelity:**
- Source material is rigorously gathered from official Parallax documentation, datasheets, and authoritative community references
- Code examples are compiled and validated using `pnut_ts` wherever possible
- Content is cross-referenced against the project's structured YAML knowledge base

**What this means for community review:**

Because these documents are AI-assisted, the issues you may encounter differ from traditionally authored manuals. Watch for:

- **Plausible but incorrect details** — Specifications that sound right but aren't (wrong clock cycles, flag behaviors, register addresses)
- **Overgeneralization** — Statements presented as universal that have exceptions or edge cases
- **Missing practitioner context** — Technically accurate but lacking the practical insight experienced users know
- **Logic errors in examples** — Code that compiles but doesn't behave as described
- **Terminology drift** — Nearly-correct terms that could mislead

**Your expertise is essential.** This review process depends on practitioners who know the Propeller 2 to catch what automated validation cannot. If something looks wrong, seems incomplete, or contradicts your experience — **[report it via the Issues page](https://github.com/ironsheep/P2-Knowledge-Base/issues)**.

## Documents in Community Review

Four documents are available now for community technical review. We welcome feedback on accuracy, completeness, and clarity. (PDF links download the file directly.)

### [P2 Assembly Language Reference Manual](https://github.com/ironsheep/P2-Knowledge-Base/blob/main/deliverables/documents/DOCs/P2-Assembly-Language-Manual.pdf?raw=1)
**Complete PASM2 Instruction Set Documentation** — *Version 3.0.0*

The definitive reference for P2 assembly language programming. Documents all PASM2 instructions with accurate syntax, encoding tables, behavior descriptions, and practical examples. Organized alphabetically for quick lookup, with comprehensive coverage of directives, special registers, and predefined constants. Includes architectural foundation chapters on execution models, instruction formats, flags, timing, and hardware integration.

*June 2026 - Community Review Edition* | [Changelog](DOCs/p2-assembly-language-manual-changelog.md)

### [P2 Assembly Programming](https://github.com/ironsheep/P2-Knowledge-Base/blob/main/deliverables/documents/DOCs/P2-PASM-deSilva-Style.pdf?raw=1)
**A Human-Centered Approach to Parallel Processing** — *Version 3.0.0*

This tutorial follows in the footsteps of deSilva's legendary P1 Assembly Tutorial, bringing the same approachable, hands-on teaching style to the Propeller 2. Starting with a blinking LED and progressing through COG architecture, hub memory, CORDIC math, Smart Pins, and multi-COG coordination, this manual makes PASM2 genuinely enjoyable to learn. Written with the philosophy: "Learn by doing, celebrate progress, have fun!"

*June 2026 - Community Review Edition* | [Changelog](DOCs/p2-pasm-desilva-style-changelog.md)

### [P2 Streamer Programming Guide](https://github.com/ironsheep/P2-Knowledge-Base/blob/main/deliverables/documents/DOCs/P2-Streamer-Programming-Guide.pdf?raw=1)
**Comprehensive Reference for the Propeller 2 Streamer** — *Version 1.0.0*

The complete reference for the P2 streamer — the DMA-like engine that moves data between hub RAM, pins, and DACs. Covers every streamer mode (immediate, RDFAST/WRFAST, RGB video, ADC sampling, DDS/Goertzel), NCO timing and frequency calculation, DAC channel routing and pin control, and application patterns for video output, high-speed serial, and signal processing. Includes a complete mode encoding table and a clickable index.

*June 2026 - Community Review Edition* | [Changelog](DOCs/p2-streamer-programming-guide-changelog.md)

### [P2 Debug Window Manual](https://github.com/ironsheep/P2-Knowledge-Base/blob/main/deliverables/documents/DOCs/P2-Debug-Window-Manual.pdf?raw=1)
**See What Your Program Is Doing — Nine Display Windows for the Propeller 2** — *Version 1.0.0*

The complete guide to the P2's nine DEBUG display windows — TERM, BITMAP, PLOT, LOGIC, SCOPE, SCOPE_XY, FFT, SPECTRO, and MIDI. Documents every window's directives, parameters, ranges, and defaults, with a worked, software-only example in each chapter — thermal heatmap, PID strip-chart, glitch capture, motor run-up, and more — that runs on a bare P2 board with no wiring. Integration chapters cover packed-data high-rate transfer, multiple windows and PASM debugging, host keyboard and mouse input, and live control and status panels. Includes a downloadable example library of 32 compile-clean Spin2 programs.

*June 2026 - Community Review Edition* | [Changelog](DOCs/p2-debug-window-manual-changelog.md) | [Example Library (ZIP)](https://github.com/ironsheep/P2-Knowledge-Base/blob/main/deliverables/documents/DOCs/p2-debug-window-manual-src-260616.zip?raw=1)

## Also in the Pipeline

Two further manuals are in production and will open for community review as they complete:

### P2 Single-Step Debugger Manual
**Observe and Control Your Running P2 Code** — *coming soon*

A practical guide to single-stepping P2 code — pausing and resuming a running program, inspecting values and timing, and driving the debugger from the host.

### P2 I/O & Smart Pins User Guide
**Complete P2 Pin I/O and Smart Pin Reference** — *coming soon*

The complete reference for P2 pin I/O and the Smart Pins — every smart pin mode, its configuration, and usage patterns.


## Reporting Issues

Found an error or have feedback? We appreciate your help improving these documents!

**[Report a Document Defect](https://github.com/ironsheep/P2-Knowledge-Base/issues/new?template=document_defect.yml)** — Use this when you found an error and know (or can reference) the correct information. Include page number, nearest heading, and source reference.

**[Provide Document Feedback](https://github.com/ironsheep/P2-Knowledge-Base/issues/new?template=document_feedback.yml)** — Use this for suggestions, unclear content, missing information, or when something seems wrong but you're not sure of the fix.

For issues with AI-generated code or the underlying YAML/JSON knowledge base, see:
- [AI Defect Report](https://github.com/ironsheep/P2-Knowledge-Base/issues/new?template=ai_defect_report.yml) — When AI generates incorrect P2 code
- [AI Content Defect](https://github.com/ironsheep/P2-Knowledge-Base/issues/new?template=ai_content_defect.yml) — Errors in YAML/JSON knowledge base files


## Generation

Documents are generated using PDF Forge from markdown sources we've authored.

---

*Built with intention for the P2 community*
