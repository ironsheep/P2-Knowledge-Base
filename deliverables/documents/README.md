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

The following documents are available for community technical review. We welcome feedback on accuracy, completeness, and clarity.

### [P2 Assembly Language Reference Manual](DOCs/P2-Assembly-Language-Manual.pdf)
**Complete PASM2 Instruction Set Documentation** — *Version 2.1.0*

The definitive reference for P2 assembly language programming. Documents all PASM2 instructions with accurate syntax, encoding tables, behavior descriptions, and practical examples. Organized alphabetically for quick lookup, with comprehensive coverage of directives, special registers, and predefined constants. Includes architectural foundation chapters on execution models, instruction formats, flags, timing, and hardware integration.

*January 2026 - Community Review Edition* | [Changelog](DOCs/p2-assembly-language-manual-changelog.md)

### [P2 Assembly Programming](DOCs/P2-PASM-deSilva-Style.pdf)
**A Human-Centered Approach to Parallel Processing** — *Version 2.0*

This tutorial follows in the footsteps of deSilva's legendary P1 Assembly Tutorial, bringing the same approachable, hands-on teaching style to the Propeller 2. Starting with a blinking LED and progressing through COG architecture, hub memory, CORDIC math, Smart Pins, and multi-COG coordination, this manual makes PASM2 genuinely enjoyable to learn. Written with the philosophy: "Learn by doing, celebrate progress, have fun!"

*January 2026 - Community Review Edition* | [Changelog](DOCs/p2-pasm-desilva-style-changelog.md)


## Reporting Issues

Found an error or have feedback? We appreciate your help improving these documents!

**[Report a Document Defect](https://github.com/ironsheep/P2-Knowledge-Base/issues/new?template=document_defect.yml)** — Use this when you found an error and know (or can reference) the correct information. Include page number, nearest heading, and source reference.

**[Provide Document Feedback](https://github.com/ironsheep/P2-Knowledge-Base/issues/new?template=document_feedback.yml)** — Use this for suggestions, unclear content, missing information, or when something seems wrong but you're not sure of the fix.

For issues with AI-generated code or the underlying YAML/JSON knowledge base, see:
- [AI Defect Report](https://github.com/ironsheep/P2-Knowledge-Base/issues/new?template=ai_defect_report.yml) — When AI generates incorrect P2 code
- [AI Content Defect](https://github.com/ironsheep/P2-Knowledge-Base/issues/new?template=ai_content_defect.yml) — Errors in YAML/JSON knowledge base files


## Coming Soon

- Propeller 2 Manual
- Propeller 2 Smart Pins & I/O - Master Every Aspect of P2 Input/Output Through Progressive Learning
- Learning to use Debug Windows
- Single-step Debugger Reference Guide

## Generation

Documents are generated using PDF Forge from markdown sources we've authored.

---

*Built with intention for the P2 community*
