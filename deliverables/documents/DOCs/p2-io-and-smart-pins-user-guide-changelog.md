# P2 I/O & Smart Pins User Guide — Change Log

## v1.0.1 (2026-07-04)

Hardware-verified updates to the event-wait and concurrent-measurement guidance, proven on P2 silicon:

- **Event wait with a timeout (Chapter 5)** — documents the SETQ-armed wait: pre-loading SETQ with a CT deadline arms a single WAIT instruction to stall on a smart-pin event or a timeout, giving a timed wait without a busy-poll loop.
- **Concurrent frequency measurement (Chapter 15)** — the concurrent multi-pin measurement example routes both the A and B inputs to each observed pin, the configuration period-aligned cells require to close their measurement window.

## v1.0.0 (2026-07-03)

**Initial release for community review.** The complete practical reference for the Propeller 2's pin I/O system, working up in three layers: direct pin control (drive, read, and the low-level pin-mode bits), the smart pin architecture and its universal configuration model (WRPIN / WXPIN / WYPIN with a single setup order), and chapters organized by function that together cover all 32 smart pin modes — digital and pulse/transition output, NCO and PWM waveform generation, DAC output, synchronous and asynchronous serial, digital input, timing / counting / period / frequency measurement, ADC (including high-resolution instrumentation techniques), the repository, and USB. Every mode chapter gives register-level configuration, worked Spin2 and PASM2 examples, and a "where you'd use this" framing, with hardware-grounded coverage of the details that bite: init ordering, IN-flag handshakes, data justification, and measurement math. Reference appendices provide a task-oriented intent index, the full P\_ constant tables, a formulas reference, mode-comparison charts, a troubleshooting guide, a complete 32-mode register reference, and FPGA board differences. Includes a downloadable library of 15 compile-clean Spin2 example programs that run on a bare P2 board.
