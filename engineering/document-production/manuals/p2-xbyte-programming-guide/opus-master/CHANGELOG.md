# P2 XBYTE Programming Guide - Changelog

## v1.1.0 (unreleased)

**What the engine costs, and where the work goes** — the guide draws the line between what XBYTE forbids and what it merely charges you for, defines the shared flag helper its handlers depend on, and points at the complete community 6502 that sits one rung below the book's own capstone.

### Added

- **`set_nz` is written out** (§16.3): four instructions, with the contract that the caller leaves the 8-bit result in `val` and the helper reads only `val`
- **Why a shared helper is safe inside a skip-built handler** (§16.3): the P2 suspends skipping for the duration of a `CALL` and resumes on return
- **`_RET_ CALL` never returns** (§16.3, hardware callout): `_RET_` returns only if the instruction did not branch, and `CALL` branches
- **It assembles clean and nothing faults** (§16.3) — execution runs out of the handler into whatever the assembler placed next
- **Measured on P2 silicon**: an adjacent handler ran whose bytecode was never in the stream, then returned to dispatch and the program finished
- **The complete community 6502** (§C.5): a full instruction set with decimal mode, the undocumented opcodes, cycle counting and single-step — standing on rung 2, with the loop body that puts it there
- **A dispatch entry can carry metadata** (§4.5): how many high bits a pattern leaves free depends on the handler's length, and a working emulator packs each opcode's cycle count into bits [31:28]
- **Chapter 17 is named as the price list** for per-symbol work, from §3.5, §3.6, §13.4 and §19.7

### Changed

- **Handlers end with an explicit `RET` after the call**, throughout the guide's examples
- **The `_RET_ CALL` callout names its examples** (§16.3): `set_nz` ending `_ret_ muxc`, and the `JMP abs` handler ending `_ret_ rdfast`
- **§13.1's `CALL`-depth discussion** states what the skip-suspension does *not* license, and points at §16.3
- **The immediate-load family** (§16.3) shows the shared-body idiom collapsing `LDA`/`LDX`/`LDY`, which differ only in the receiving register
- **`_RET_`'s semantics are cited to Parallax**: the instruction table in *P2 Instructions v35 – Rev B/C Silicon*, row 410
- **Per-symbol work is priced, not forbidden** (§3.5, §19.7): two conditions rule the engine out — a stream outside hub RAM, and an unavailable LUT. Work between symbols is a third thing, a budget: it goes inside the handlers and costs from about two clocks a symbol down to nearly nothing when it can be confined to the handlers that matter
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
