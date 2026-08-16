# P2 Streamer Programming Guide - Changelog

## v1.0.9 (2026-08-16)

**Goertzel, as a protocol you can build from** — the mode works, and this release states the parts the guide never did: what the input actually selects, how to read the accumulators, and why your measurements change when you add DEBUG.

### Added

- **Reading the result: one `GETXACC` per command** (§17.1). `GETXACC` captures both accumulators into holding registers and clears them. A second read with no intervening streamer command returns the same numbers, and a read taken before a command belongs to the previous one — so read before and after and take the difference. An absolute read in that pattern fails invisibly, because the number returned is large, stable and entirely plausible.
- **The input is a four-pin block, not a pin** (§17.1): `D[22:19]` selects a block of four whose base pin is `%pppp x 4`; the `S` operand chooses what happens to those four.
- **Goertzel ADC pins are raw bitstreams** (§17.1): configure them with the smart-pin mode field at `%00000` and leave DIR low — an enabled smart pin on these pins produces no accumulation at all. This is the reverse of the scope-fed ADC modes of §9.2. Gain is a property of the coupling, not of the mode.
- **§14.5 Debugging Streamer Code**: compiling with `-d` puts the P2's highest-priority interrupt inside your streaming cog, and `DEBUG_COGS` defaults to all eight. Carries the measured cost — accumulators reading in the millions where the true values were in the hundreds — the one-`CON`-line fix, and the general rule that any hardware sequencer under measurement wants a cog the debugger is not interrupting.
- **Two troubleshooting symptoms** (Appendix D): a `-d` check under *Goertzel Results Invalid*, and *Measurements Change When You Add DEBUG*.

### Changed

- **Combine pin-mode constants with `|`, never `+`** (§13.4): the `P_*` constants are bit fields positioned inside the mode word, not additive flags. `P_TT_01`, `P_OE` and `P_CHANNEL` are one bit-field value under three context names — measured on silicon, the `|` form drove a cog DAC at 6,737 ADC counts where the `+` form read 1,407.
- **Source documents are named by their official titles**, so a newcomer can search for them.

## v1.0.8 (2026-08-08)

A licensing change. No technical content changed.

- **Licensed CC BY-SA 4.0**: share and adapt this guide, including commercially, with attribution and under the same terms.


## v1.0.7 (2026-07-21)

A readability refinement. No chapters added, no mode encodings or technical content changed.

- **Prose**: several chapter openers read more directly. All mode tables, encodings, and worked examples are unchanged.

## v1.0.6 (2026-07-11)

A Silicon-Doc accuracy pass across the streamer's timing, worked examples, and mode-encoding reference. No chapters added.

- **NCO frequency resolution (Ch 3)**: the phase accumulator masks its MSB each clock, so the average output rate resolves to `sysclk / 2^31` and is essentially exact at any sysclk.
- **Worked examples (video & SPI)**: the 640×480 VGA driver's field timing and DAC-routed RGB mode word, and the SPI clock setup, are stated as the silicon requires, so the examples drive correct signals.
- **FIFO wrap mode (Appendix D)**: the wrap-mode buffer start address requirement is long-alignment (address ends in `%00`).
- **Mode-encoding reference (Appendix A)**: the RFBYTE single-pin + single-DAC mode encodings read per the Silicon Doc.

## v1.0.5 (2026-07-07)

A sub-pin selection correction. No chapters added.

- **Sub-pin selection (§12.2)**: the sub-pin field is documented per the silicon's actual field
  widths, which vary with pin count: **1-pin** modes use all of D[19:17] as the pin offset; **2-pin**
  modes use D[19:18] (four pin pairs), with D[17] selecting DAC configuration; **4-pin** modes use
  D[19] (two groups), with D[18:17] selecting DAC configuration. Higher pins are reached by moving
  the 32-pin window with the group field D[22:20] (§12.1).

## v1.0.4 (2026-07-04)

Guidance refinements in the video and DDS/Goertzel chapters. No chapters added, no mode
encodings changed.

- **HDMI audio blanking (§15.2)**: audio-carrying HDMI needs more horizontal blanking than
  video-only timing; size that budget from the HDMI data-island specification for your exact mode.
- **DVI/HDMI blanking floors (§15.2)**: the observed per-display floors are framed as
  display-specific values to test against your own monitor, not as fixed limits.
- **SINC2 measurement period (§10.4)**: the non-power-of-two-rate workaround gives an
  approximate measurement-period bound (on the order of 20 ms) to verify for your rate.

## v1.0.3 (2026-07-03)

Designer-authoritative guidance additions to the DDS/Goertzel and video chapters.
No mode encodings changed.

- **SINC2 constant-iteration constraint**: §10.4 documents the silicon requirement that
  every Goertzel cycle integrate a constant iteration count, with three workarounds; the
  Appendix D troubleshooting checklist points to it.
- **HDMI/DVI blanking guidance**: §15.2 adds practical DVI/HDMI blanking limits
  (display-limited, not analog-mandated) and the extra horizontal blanking that
  audio-carrying HDMI needs.
- **Capture-to-spectrum pointer**: §9.2 links high-rate ADC capture to the CORDIC FFT
  technique for on-chip spectral analysis.

## v1.0.2 (2026-06-26)

Presentation refresh adopting the shared manual-family typography. No chapters added,
no mode encodings changed.

- **Typography**: the IBM Plex type family throughout, with code set in clean boxes and
  no line-number gutter, matching the rest of the manual family.
- **LUMA8 color reference**: §7.2 tabulates the eight `S[2:0]` output colors.
- **Mode-field shorthand**: §6.1 explains the `%MMMM_CCCC` notation (mode field D[31:28]
  plus config field D[19:16]) used across the mode tables.

## v1.0.1 (2026-06-19)

Correctness, accuracy-guidance, and presentation update following a full grounding
audit against the Silicon Doc and a detailed review pass. No new chapters; every
mode encoding from v1.0.0 is unchanged.

- **Corrected the mode reference tables**: the Pins / DAC-channel / DAC-bit columns
  in the immediate, RDFAST, and pin-capture tables (and Appendix A) now read correctly
  per the Silicon Doc; some pin and DAC-channel counts had been transposed. The mode
  *encodings* themselves were always correct.
- **Code examples now compile cleanly**: fixed PASM2 label syntax, the `wrlut` and
  `clkfreq` usages, and a few mode/symbol choices across the example programs.
- **Rewrote §3.4 "Choosing a Pixel Rate"** around what actually matters: per-pixel
  jitter (and removing it with an integer sysclk-to-pixel ratio) rather than frequency
  error, with PLL-verified jitter-free clock options and a worked example.
- **Added §3.5 "Clock Accuracy and Jitter"**: what governs absolute accuracy, the
  P2 Edge module's ±0.5 ppm TCXO, and the crystal trade-off on a custom board.
- **More guidance, less raw lookup**: §3.2 (exact vs rounded ratios), §7.1 (memory
  cost per RGB format vs hub size), §12.1 (pin-group wrap-around), and the
  RDFAST/WRFAST FIFO notes now explain the decision, not just the values.
- **Clarified semantics**: event clearing (§14.3), WAITXFI (§16.2), and the
  XCONT/XZERO usage note (§4.7).
- **Presentation**: advisory callouts (Tip / Caution / Hardware) now render as styled
  boxes; Figure 2.1 corrected to show DAC channels driving pins; list and table
  formatting cleaned up.

## v1.0.0 (2026-06-10)

Initial community review release.

- 18 chapters across five parts: Streamer Fundamentals, Mode Reference, Configuration Reference, Applications, and Appendices
- Complete mode reference, immediate, RDFAST/WRFAST, RGB video, ADC sampling, and DDS/Goertzel, with command-word structure, NCO timing, and frequency calculation
- Configuration reference for DAC channel routing, pin selection, programming constants, and events/synchronization
- Application chapters: video output, high-speed serial (SPI), signal processing, and integration patterns
- Appendices: complete mode encoding table, symbol quick reference, frequency calculation tables, and troubleshooting guide
- Clickable index linking each entry to its chapter, section, or appendix
