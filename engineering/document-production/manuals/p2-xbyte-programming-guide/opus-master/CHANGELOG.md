# P2 XBYTE Programming Guide - Changelog

## v1.0.2 (2026-08-16)

**The shared flag helper, defined** — §15.3 states the calling convention its handlers depend on, and the guide is explicit that the return cannot be folded into the call.

### Added

- **`set_nz` is written out** (§15.3) with its contract stated: the caller leaves the 8-bit result in `val` immediately before the call, and the helper reads only `val`. Four instructions, called by every load, ALU and increment opcode in the guest — which is what makes defining it once worthwhile.
- **Why a shared helper works inside a skip-built handler** (§15.3): the P2 suspends skipping for the duration of a `CALL` and resumes on return, so the helper's own instructions are safe from the caller's skip pattern.
- **Do not fold the return into the call** (§15.3, hardware callout): `_RET_` executes the instruction and returns **only if it did not branch**, and `CALL` branches — so `_RET_ CALL` never returns. It assembles without complaint, nothing faults, and no flag is set; execution runs out of the handler into whatever the assembler placed next. Measured on P2 silicon running an entire adjacent handler whose bytecode was never in the stream, after which that handler's own `RET` returned to dispatch and the program finished having silently done work it was never asked to do.

### Changed

- **Handlers end with an explicit `RET` after the call**, throughout the guide's examples.
- **§11.1's `CALL`-depth discussion** notes what the skip-suspension does *not* license, and points at §15.3.
- **The immediate-load family** (§15.3) shows the shared-body idiom collapsing `LDA`/`LDX`/`LDY`, which differ only in which guest register receives the byte.
- **The `_RET_ CALL` callout says which examples it is about.** The chapter folds the return twice within twenty lines — `set_nz` ends `_ret_ muxc`, the `JMP abs` handler ends `_ret_ rdfast` — so the callout now names them and reads as the boundary of the idiom the reader has just learned, rather than a free-standing gotcha.
- **`_RET_`'s semantics are cited to Parallax**, from the instruction table in *P2 Instructions v35 – Rev B/C Silicon* (row 410), rather than to a companion volume in this same documentation family.
- **Instruction mnemonics read uniformly** where `SKIPF` appeared plain in §11.1.

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
