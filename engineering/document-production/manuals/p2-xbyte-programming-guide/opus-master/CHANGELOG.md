# P2 XBYTE Programming Guide - Changelog

## v1.1.0 (unreleased)

**Find your rung before you build** — a Part devoted to the dispatch decision, a second worked program between the smallest build and the hardest, and figures for the ideas the book turns on.

### Added

- **Part III, Choosing Your Rung**: the three decisions that select a dispatch strategy, and what each classic guest CPU costs
- **Chapter 15, Growing the VM**: eleven bytecodes — an ALU family on one shared body, variables, and a branch that re-points the stream
- **The column-map notation for shared handler bodies** (§4.4, §4.6): read a skip pattern off the body by eye instead of decoding binary
- **Three figures**: the dispatch ladder (§7.2), the three decisions (§7.5), and the two kinds of prefix (§18.1)
- **A navigation layer in the front matter**: an Intent Index by project, three reading paths, and the engine in brief on one page
- **The Index carries the reader's own vocabulary**: seventy entries pointing at chapters, sections, and the quick-reference card
- **Three complete programs in the example ZIP**: the minimal VM, the grown VM, and the display-list engine
- **`set_nz` is written out** (§16.3): four instructions, with the contract that the caller leaves the 8-bit result in `val`
- **Why a shared helper is safe inside a skip-built handler** (§16.3): the P2 suspends skipping for the duration of a `CALL`
- **`_RET_ CALL` never returns** (§16.3, hardware callout): `_RET_` returns only if the instruction did not branch, and `CALL` branches
- **Measured on P2 silicon**: an adjacent handler ran whose bytecode was never in the stream, and the program still finished
- **A dispatch entry can carry metadata** (§4.5): a working emulator packs each opcode's cycle count into bits [31:28]
- **Three places for per-instruction work under XBYTE** (§7.4): a family's shared tail, a prologue the skip pattern selects, and the cog's own interrupts
- **The complete community 6502** (§C.5): decimal mode, undocumented opcodes, cycle counting and single-step, standing on rung 2

### Changed

- **Seven Parts, ordered by the reader's decision**: the machinery, then the choice, then the engine, then the builds
- **The facts that carry the argument sit in the running text**, with callout boxes reserved for genuine asides
- **Per-symbol work is priced, not forbidden**: two conditions rule the engine out, and Chapter 17 prices the rest (§3.5, §13.4, §19.7)
- **Handlers end with an explicit `RET` after the call**, throughout the guide's examples
- **The `_RET_ CALL` callout names its examples** (§16.3): `set_nz` ending `_ret_ muxc`, and the `JMP abs` handler ending `_ret_ rdfast`
- **§13.1's `CALL`-depth discussion** states what the skip-suspension does *not* license, and points at §16.3
- **The immediate-load family** (§16.3) shows the shared-body idiom collapsing `LDA`/`LDX`/`LDY`
- **`_RET_`'s semantics are cited to Parallax**: the instruction table in *P2 Instructions v35 – Rev B/C Silicon*, row 410
- **Every example carries a header** naming its manual, version, and where in the book its code appears
- **Guests too large for hub live in an external memory subsystem you fetch from** (§7.3): the Edge module is a starting point
- **Appendix C states its scope** (§C): it lists the implementations located and read, not a census, and invites additions
- **Example source is plain ASCII throughout**, so the shipped `.spin2` files open identically in any editor

## v1.0.1 (2026-08-08)

A licensing change. No technical content changed.

- **Licensed CC BY-SA 4.0**: share and adapt this guide, including commercially, with attribution and under the same terms.


## v1.0.0 (2026-07-20): Initial release for community review

The P2 Interpreters & Emulators Guide: a guide to the Propeller 2's XBYTE
hardware bytecode engine, the skip family (SKIP/SKIPF/EXECF), the FIFO bytecode
stream, and LUT dispatch. It takes a reader from what the engine is and how it
dispatches each bytecode through to building on it: custom virtual machines,
and, where the engine fits the guest, CPU emulation, illustrated end to end.

Written in two registers, a warm teaching layer for the concepts and a precise
reference layer for the tables, encodings, and configuration bits, it
consolidates the P2 documentation, the knowledge base, and worked community code
into one source for readers building interpreters, custom VMs, or CPU emulators
on the P2.
