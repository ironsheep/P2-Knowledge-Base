# P2 Streamer Programming Guide - Changelog

## v1.1.0 (2026-08-22)

**Getting the signal out of the chip** — the pin-side setup every DAC example depends on, the LUT window's eight loop sizes, and streamer behavior confirmed on P2 silicon.

### Added

- **§11.0 Getting a DAC Channel Onto a Pin**: `WRPIN` with a DAC pin-mode constant, this cog's ID in `M[3:0]`, and `DIRH`
- **A pin's low two bits choose its DAC channel** (§11.0, §11.2), so a four-channel arrangement takes a base that is a multiple of four
- **`%TT` decides where a DAC's value comes from** (§11.0): `%01` (`P_CHANNEL`) for a streamer-driven DAC, `%00` for the pin's own level field
- **`SETDACS` sets what the untouched channels emit** (§11.0, §11.1): a routing field that drives two channels leaves the other two at that value
- **`X_PINS_ON` supplies a pin's output state; `DIR` enables it to drive** (§11.0): on silicon, eight of eight pins drove with `DIRH` and four with DIR low
- **§10.3 The LUT Window**: `S[11:0]` selects one of eight loop sizes, the `%A` region bits that place it, and the `%T` offset that shifts playback phase
- **§12.0 Reading a Pin Field**: streamer command fields are positional and mode-specific, and `pin<<17` splits a pin number across `D[22:20]` and `D[19:17]`
- **§15.0 The Colorspace Converter**: the `CY`/`CI`/`CQ` matrix, the modulator, and `CMOD[6:5]` output selection including the S-Video split
- **§15.2 carries a complete HDMI/DVI program**, the pair order `CMOD[8:7]` selects, and the `P[1]` bit that sends a channel literally rather than TMDS-encoded
- **§15.3 gives composite video's configuration and names what you supply**: `CMOD[6:5]` = `%11`, and why the NTSC/PAL coefficients are yours to derive
- **§17.2 is a one-channel function generator**: DAC-pin setup, `X_DACS_X_X_X_0`, and the `$FFFF` count that runs a command perpetually
- **Every code block declares what it is** (front matter, *Code Blocks*): an unlabelled block leaves nothing for you to supply, a **Pattern** lead-in names what you do
- **The *Goertzel Results Invalid* checklist covers all three dominant causes** (Appendix D)
- **The Index reaches the new material**, including the LUT window, the pin field, and the DAC-pin procedure

### Changed

- **RGBI8 carries a 3-bit color select and a 5-bit luminance** (§7.2, Appendix A, Appendix B)
- **Appendix A's `D[19:16]` column reads per the *Parallax Propeller 2 Documentation*** across the single-pin and single-DAC modes
- **The SINC2 constant-iteration constraint is the P2 designer's, reported 2024-12-16** (§10.5), and is not in the released *Parallax Propeller 2 Documentation*
- **§3.1 states the every-clock exception**: DDS/Goertzel advances on every system clock rather than on NCO rollover
- **The colorspace converter and the streamer's RGB unpacking are separate stages** (Chapter 7, §15.0), sharing only the `CMOD` register
- **The guide identifies itself in a reader or library**: its title, subtitle, author, version and date fill the PDF's properties and match the cover
- **The PDF states its copyright and CC BY-SA 4.0 licence in its own metadata**, so the terms travel with the file rather than only on the page

### Fixed

- **§9.2's `SETSCP` literal enables the scope**: `#%100_0000` sets `D[6]` and puts the four-pin block at base 0
- **§15.1 is a complete VGA program**: 640×350 painted into the full 525-line field at 25.0 MHz, with its four DAC pins configured for output
- **A 640×480 framebuffer at 16 bits per pixel is 600 KB** (§7.1, §15.1, §15.2), so both video programs paint 350 lines and blank the rest
- **§12.0 gives the alignment rule for eight pins and wider**: `D[19:17]` holds no pin bits there, so the operand is a multiple of 8
- **Compose a mode word with `|`, not `+`** (§12.0, §13.4): an unaligned value added to one carries into the mode field, selecting a different mode and window

## v1.0.9 (2026-08-19)

**The input is not where you think it is** — how each ADC path actually selects its pins, one read per Goertzel command, and why DEBUG moves your measurements.

### Added

- **§9.2 ADC input arrives through the cog's four-channel scope**: `SETSCP` enables it in `D[6]` and names a four-pin block in `D[5:2]`
- **The command selects the channel in `S[1:0]`** (§9.2), and these modes read an enabled smart pin — `DIRH` is required
- **Streamer command fields are positional and mode-specific** (§9.2): an idiom correct in one mode is not portable to another
- **The input is a four-pin block** (§13.4, §17.1): `D[22:19]` selects it, base pin `%pppp` × 4 — `adc_base<<17` is exact only on a multiple of four
- **`S[15:12]` selects which of the four are summed, and is mandatory** (§17.1): zero sums nothing, and every magnitude reads as noise
- **Goertzel ADC pins are raw bitstreams** (§17.1): mode field `%00000`, DIR low — an enabled smart pin accumulates nothing. The reverse of §9.2
- **Gain is a property of the coupling** (§17.1), not of the mode
- **One `GETXACC` per command** (§17.1): it captures both accumulators and clears them, so read before and after a command and take the difference
- **An absolute accumulator read fails invisibly** (§17.1): the number is large, stable and entirely plausible
- **Measured selectivity** (§17.1): a 1 MHz detector read 1,059,000 on tone, 2,575 at double, 286 at half, 430 silent
- **SINC2 DAC output rails at `$7F` and `$80`** (§17.1): the bytes are emitted with their MSB inverted
- **§14.5 Debugging Streamer Code**: `-d` puts the highest-priority interrupt in your streaming cog, and `DEBUG_COGS` defaults to all eight
- **The measured cost** (§14.5): accumulators reading in the millions against true values in the hundreds
- **The one-`CON`-line fix** (§14.5), and the rule that a hardware sequencer under measurement wants a cog the debugger is not interrupting
- **Two troubleshooting symptoms** (Appendix D): a `-d` check under *Goertzel Results Invalid*, and *Measurements Change When You Add DEBUG*

### Changed

- **Combine pin-mode constants with `|`, never `+`** (§13.4): the `P_*` constants are bit fields inside the mode word, not additive flags
- **`P_TT_01`, `P_OE` and `P_CHANNEL`** are one bit-field value under three context names
- **On silicon** the `|` form drove a cog DAC at 6,737 ADC counts against the `+` form's 1,407
- **§13.4 sets the two forms in adjacent blocks**, the wrong one red — copying that line fails silently and completely

### Fixed

- **Scope-fed ADC modes have no pin field** (§9.2): `D[22:20]` are fixed zeros, so a pin number added to the command selects a different mode
- **The transfer size is the only symptom** (§9.2): the same block writes 1,024, 2,048 or 4,096 bytes as a pin number is added
- **The §9.2 example takes its input from the scope**: the streamer command carries the sample count and no pin number
- **The §16.1 SPI clock pin combines its mode constants with `|`**, so the pin is left in transition mode with its output enabled

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
- **Mode-encoding reference (Appendix A)**: the RFBYTE single-pin + single-DAC mode encodings read per the *Parallax Propeller 2 Documentation*.

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
audit against the *Parallax Propeller 2 Documentation* and a detailed review pass. No new chapters; every
mode encoding from v1.0.0 is unchanged.

- **Corrected the mode reference tables**: the Pins / DAC-channel / DAC-bit columns
  in the immediate, RDFAST, and pin-capture tables (and Appendix A) now read correctly
  per the *Parallax Propeller 2 Documentation*; some pin and DAC-channel counts had been transposed. The mode
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
