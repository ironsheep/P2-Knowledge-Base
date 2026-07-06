# P2 I/O & Smart Pins User Guide — Change Log

## v1.0.3 (2026-07-06)

Corrected the ADC resolution tables to use "ENOB" precisely.

- **ADC resolution terminology (Chapter 16 & Appendix D)** — the SINC filter tables previously labeled their bit figures "ENOB." Those figures are the filter's *nominal* resolution (the width the decimation math produces), not ENOB. ENOB (Effective Number of Bits) is the *measured* effective resolution after noise and distortion, and on the P2 it is lower and must be characterized on your own hardware. The tables now read in nominal bits, with a note that the higher SINC3 figures assume an idealized doubling the P2's ADC does not actually deliver. No effective-resolution figure is claimed. (Aligns the manual with the P2 designer's own guidance that the Silicon Doc's ENOB figures need revising.)

## v1.0.2 (2026-07-05)

Sharper worked examples for reading smart-pin state timing.

- **State-timing examples (Chapter 13)** — the P_STATE_TICKS PWM-analysis examples read each transition with a single `RDPIN`, taking the state from bit 31 and the tick count from the low bits of that one result.

## v1.0.1 (2026-07-04)

Hardware-verified updates to the event-wait and concurrent-measurement guidance, proven on P2 silicon:

- **Event wait with a timeout (Chapter 5)** — documents the SETQ-armed wait: pre-loading SETQ with a CT deadline arms a single WAIT instruction to stall on a smart-pin event or a timeout, giving a timed wait without a busy-poll loop.
- **Concurrent frequency measurement (Chapter 15)** — the concurrent multi-pin measurement example routes both the A and B inputs to each observed pin, the configuration period-aligned cells require to close their measurement window.

## v1.0.0 (2026-07-03)

**Initial release for community review.** The complete practical reference for the Propeller 2's pin I/O system, working up in three layers: direct pin control (drive, read, and the low-level pin-mode bits), the smart pin architecture and its universal configuration model (WRPIN / WXPIN / WYPIN with a single setup order), and chapters organized by function that together cover all 32 smart pin modes — digital and pulse/transition output, NCO and PWM waveform generation, DAC output, synchronous and asynchronous serial, digital input, timing / counting / period / frequency measurement, ADC (including high-resolution instrumentation techniques), the repository, and USB. Every mode chapter gives register-level configuration, worked Spin2 and PASM2 examples, and a "where you'd use this" framing, with hardware-grounded coverage of the details that bite: init ordering, IN-flag handshakes, data justification, and measurement math. Reference appendices provide a task-oriented intent index, the full P\_ constant tables, a formulas reference, mode-comparison charts, a troubleshooting guide, a complete 32-mode register reference, and FPGA board differences. Includes a downloadable library of 15 compile-clean Spin2 example programs that run on a bare P2 board.
