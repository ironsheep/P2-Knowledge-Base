# P2 I/O & Smart Pins User Guide — Change Log

## v1.0.5 (2026-07-11)

A hardware-grounded accuracy pass across smart-pin behavior, pin configuration, and the worked examples.

- **Smart-pin & pin behavior verified against silicon (throughout)** — pin configuration, smart-pin modes, and I/O behavior are documented as measured on real P2 hardware.
- **Worked examples run as written (example library)** — every companion program compiles clean under the current compiler and matches its in-text listing line-for-line.
- **Quantitative values aligned to source** — instruction and pin timings, bit-field encodings, and value ranges read per the P2 datasheet and Silicon Doc.

## v1.0.4 (2026-07-07)

ADC input modes documented as measured on real silicon, a quantitative-table accuracy pass, and example titles that describe the code plainly.

- **ADC input modes (Chapter 16 §16.2 & §16.7, Appendices B, C & D)** — the ADC input modes are documented as measured on a real P2. `P_ADC_GIO`/`P_ADC_VIO` are the ADC's internal **calibration references** (ground and supply); the gain modes measure a window **centered on the ADC's mid-supply bias point (~VIO/2)**, narrowing ~3.16× per gain step. The per-gain windows are the values measured on P2 silicon (representative single-sample — exact endpoints vary part-to-part and with VIO/temperature, so calibrate for absolute work). Reported by a community reviewer; confirmed on P2 silicon.
- **Quantitative-table accuracy (Chapters 2 & 18)** — the fast push-pull driver's effective on-resistance reads **~17 Ω** at ~30 mA drive, and hub-RAM access time reads **9-16 clocks**, both per the P2 datasheet.
- **Example headings (throughout)** — the per-chapter example sections read "Worked Examples," and the Chapter 13 PWM example is titled "PWM Signal Analyzer." These names describe the teaching examples and building blocks plainly. No code changed.
- **Engineering guidance stated qualitatively (Chapters 7, 10, 12, 16)** — several figures without a primary source are given as qualitative guidance rather than spec: the ADC input impedance is high (§16.8); a single pin's ADC absolute error is a few millivolts (≤ ~9 mV measured on silicon), with pin-to-pin spread the larger effect; the DAC loading table's "Min Load" column is a ~10× output-Z guideline (§10.9); the digital-input propagation delay is stated as the grounded 3-clock total (§12.10); and the pulse-mode clock-frequency note attributes 180 MHz to the datasheet and 350 MHz to the Silicon Doc (§7.5). Grounded totals and behaviors are unchanged.

## v1.0.3 (2026-07-06)

ADC resolution, stated precisely.

- **ADC resolution (Chapter 16 & Appendix D)** — the SINC-filter tables read in nominal resolution bits, the width the decimation produces. ENOB (Effective Number of Bits) is presented as the measured effective resolution it is: on the P2 it sits below the nominal figure and is characterized on your own hardware. No effective-resolution figure is claimed.

## v1.0.2 (2026-07-05)

Sharper worked examples for reading smart-pin state timing.

- **State-timing examples (Chapter 13)** — the P_STATE_TICKS PWM-analysis examples read each transition with a single `RDPIN`, taking the state from bit 31 and the tick count from the low bits of that one result.

## v1.0.1 (2026-07-04)

Hardware-verified updates to the event-wait and concurrent-measurement guidance, proven on P2 silicon:

- **Event wait with a timeout (Chapter 5)** — documents the SETQ-armed wait: pre-loading SETQ with a CT deadline arms a single WAIT instruction to stall on a smart-pin event or a timeout, giving a timed wait without a busy-poll loop.
- **Concurrent frequency measurement (Chapter 15)** — the concurrent multi-pin measurement example routes both the A and B inputs to each observed pin, the configuration period-aligned cells require to close their measurement window.

## v1.0.0 (2026-07-03)

**Initial release for community review.** The complete practical reference for the Propeller 2's pin I/O system, working up in three layers: direct pin control (drive, read, and the low-level pin-mode bits), the smart pin architecture and its universal configuration model (WRPIN / WXPIN / WYPIN with a single setup order), and chapters organized by function that together cover all 32 smart pin modes — digital and pulse/transition output, NCO and PWM waveform generation, DAC output, synchronous and asynchronous serial, digital input, timing / counting / period / frequency measurement, ADC (including high-resolution instrumentation techniques), the repository, and USB. Every mode chapter gives register-level configuration, worked Spin2 and PASM2 examples, and a "where you'd use this" framing, with hardware-grounded coverage of the details that bite: init ordering, IN-flag handshakes, data justification, and measurement math. Reference appendices provide a task-oriented intent index, the full P\_ constant tables, a formulas reference, mode-comparison charts, a troubleshooting guide, a complete 32-mode register reference, and FPGA board differences. Includes a downloadable library of 15 compile-clean Spin2 example programs that run on a bare P2 board.
