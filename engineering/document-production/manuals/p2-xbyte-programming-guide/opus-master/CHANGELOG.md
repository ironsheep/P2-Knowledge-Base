# P2 XBYTE Programming Guide - Changelog

## v1.0.2 (2026-08-16)

**The shared flag helper, defined** — §15.3 states the calling convention its handlers depend on, and the guide is explicit that the return cannot be folded into the call.

### Added

- **`set_nz` is written out** (§15.3): four instructions, with the contract that the caller leaves the 8-bit result in `val` and the helper reads only `val`
- **Why a shared helper is safe inside a skip-built handler** (§15.3): the P2 suspends skipping for the duration of a `CALL` and resumes on return
- **`_RET_ CALL` never returns** (§15.3, hardware callout): `_RET_` returns only if the instruction did not branch, and `CALL` branches
- **It assembles clean and nothing faults** (§15.3) — execution runs out of the handler into whatever the assembler placed next
- **Measured on P2 silicon**: an adjacent handler ran whose bytecode was never in the stream, then returned to dispatch and the program finished

### Changed

- **Handlers end with an explicit `RET` after the call**, throughout the guide's examples
- **The `_RET_ CALL` callout names its examples** (§15.3): `set_nz` ending `_ret_ muxc`, and the `JMP abs` handler ending `_ret_ rdfast`
- **§11.1's `CALL`-depth discussion** states what the skip-suspension does *not* license, and points at §15.3
- **The immediate-load family** (§15.3) shows the shared-body idiom collapsing `LDA`/`LDX`/`LDY`, which differ only in the receiving register
- **`_RET_`'s semantics are cited to Parallax**: the instruction table in *P2 Instructions v35 – Rev B/C Silicon*, row 410

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
