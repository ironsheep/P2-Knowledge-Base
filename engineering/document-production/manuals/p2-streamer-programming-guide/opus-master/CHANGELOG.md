# P2 Streamer Programming Guide - Changelog

## Unreleased

Content additions from a P2 forum-thread reconciliation pass — designer-authoritative
findings folded in. No mode encodings changed.

- **§10.4 — SINC2 Goertzel silicon limitation.** Documented that SINC2's double integration
  requires a constant iteration count per Goertzel cycle: a non-power-of-two NCO rate makes
  GETXACC read an off-by-one integration, corrupting the current and next samples (periodic
  ~30–60 ms glitches). Three workarounds given (power-of-two clock, SINC1, or XZERO + sub-20 ms
  period). From the *Parallax Propeller 2 Documentation* Goertzel note dated 2024.12.16; also
  cross-referenced in the Appendix D "Goertzel Results Invalid" checklist.
- **§15.2 — HDMI/DVI blanking guidance.** Blanking is display-limited, not analog-mandated:
  observed horizontal floors ~16–68 px (multiple of 8) and minimal ~8-line vertical blanking;
  audio-carrying HDMI needs ~34 horizontal blank pixel-periods (community-measured — verify
  against the data-island spec).
- **§9.2 — capture-to-spectrum pointer** linking high-rate ADC capture to the CORDIC FFT
  technique worked in the *CORDIC for Real Work* application note (P2AN002).

## v1.0.2 (2026-06-26)

Presentation refresh adopting the shared manual-family typography. No chapters added,
no mode encodings changed.

- **Typography** — the IBM Plex type family throughout, with code set in clean boxes and
  no line-number gutter, matching the rest of the manual family.
- **LUMA8 color reference** — §7.2 tabulates the eight `S[2:0]` output colors.
- **Mode-field shorthand** — §6.1 explains the `%MMMM_CCCC` notation (mode field D[31:28]
  plus config field D[19:16]) used across the mode tables.

## v1.0.1 (2026-06-19)

Correctness, accuracy-guidance, and presentation update following a full grounding
audit against the Silicon Doc and a detailed review pass. No new chapters; every
mode encoding from v1.0.0 is unchanged.

- **Corrected the mode reference tables** — the Pins / DAC-channel / DAC-bit columns
  in the immediate, RDFAST, and pin-capture tables (and Appendix A) now read correctly
  per the Silicon Doc; some pin and DAC-channel counts had been transposed. The mode
  *encodings* themselves were always correct.
- **Code examples now compile cleanly** — fixed PASM2 label syntax, the `wrlut` and
  `clkfreq` usages, and a few mode/symbol choices across the example programs.
- **Rewrote §3.4 "Choosing a Pixel Rate"** around what actually matters: per-pixel
  jitter (and removing it with an integer sysclk-to-pixel ratio) rather than frequency
  error, with PLL-verified jitter-free clock options and a worked example.
- **Added §3.5 "Clock Accuracy and Jitter"** — what governs absolute accuracy, the
  P2 Edge module's ±0.5 ppm TCXO, and the crystal trade-off on a custom board.
- **More guidance, less raw lookup** — §3.2 (exact vs rounded ratios), §7.1 (memory
  cost per RGB format vs hub size), §12.1 (pin-group wrap-around), and the
  RDFAST/WRFAST FIFO notes now explain the decision, not just the values.
- **Clarified semantics** — event clearing (§14.3), WAITXFI (§16.2), and the
  XCONT/XZERO usage note (§4.7).
- **Presentation** — advisory callouts (Tip / Caution / Hardware) now render as styled
  boxes; Figure 2.1 corrected to show DAC channels driving pins; list and table
  formatting cleaned up.

## v1.0.0 (2026-06-10)

Initial community review release.

- 18 chapters across five parts: Streamer Fundamentals, Mode Reference, Configuration Reference, Applications, and Appendices
- Complete mode reference — immediate, RDFAST/WRFAST, RGB video, ADC sampling, and DDS/Goertzel — with command-word structure, NCO timing, and frequency calculation
- Configuration reference for DAC channel routing, pin selection, programming constants, and events/synchronization
- Application chapters: video output, high-speed serial (SPI), signal processing, and integration patterns
- Appendices: complete mode encoding table, symbol quick reference, frequency calculation tables, and troubleshooting guide
- Clickable index linking each entry to its chapter, section, or appendix
