# P2 Debug Window Manual: Change Log

## v1.1.2 (2026-08-08)

A licensing change. No technical content changed.

- **Licensed CC BY-SA 4.0**: share and adapt this manual, including commercially, with attribution and under the same terms.


## v1.1.1 (2026-07-27)

**Every program in the example library runs on hardware.** All 34 programs verified on real P2
silicon under PNut v55, the interactive ones included. **Download the current example ZIP.**

### Fixed

- The keyboard and mouse examples (Chapter 12) and the control panel (Chapter 15) read host input
  and respond to it.
- Chapter 14's coordinated scope-and-status example opens both of its windows, and Chapter 5's
  `LINE` snippet opens its plot.
- Ordinary English words that share a P2 mnemonic's spelling, "fit", "test", read as prose.

### Added

- **Both input commands carry their own backtick** (Chapter 12, Appendix A): working and
  non-working forms side by side, with the runtime symptom.
- **Naming a display window** (Chapter 2): the complete five-part rule, including the 103 reserved
  display words (Spin2's own reserved words stay available).
- **Mouse coordinates against panel artwork** (Chapter 15): drawn panels need no conversion;
  bitmap-authored panels need a Y flip.

## v1.1.0 (2026-07-14)

**Verified against P2 silicon.** Every load-bearing claim in this manual was re-tested on real
hardware, and the example library is updated to match, **download the current example ZIP** to
pick up the latest programs.

### Fixed

- The PLOT worked example draws a full cycle of a CORDIC sine wave, taking its full-circle angle
  step with Spin2's unsigned divide (`+/`).
- The Chapter 13 packed-data examples place each sample in the low bits first, the order the host
  unpacks them in.
- The LOGIC channel-declaration example gives each channel an explicit count (`'CLK' 1 $00FF00`)
  and ships as a compile-and-run program in the library.
- PLOT `PRECISE` starts off, the first `PRECISE` selects sub-pixel positioning.
- PLOT text renders in the color you set: a `COLOR` reaches `TEXT` when `TEXT` is the next key.
- SPECTRO axes: at the default `TRACE $F` the horizontal axis is time and the vertical is
  frequency, in both Chapter 10 and Appendix C.
- SCOPE channel definitions belong in a message sent after the create line.
- FFT: `MAG` is a gain, the channel `grid` field is four bits, and `LOGSCALE` is described by what
  it draws.
- `LINESIZE` is stated in half-pixels for the LOGIC, SCOPE and FFT windows.
- Worked `SAVE` examples name the file they write.

### Added

- **What `PC_MOUSE` delivers to your program** (Chapter 12): in the LOGIC, SCOPE, SCOPE_XY, FFT
  and MIDI windows you receive raw client pixels; the coordinate shown beside the pointer is drawn
  host-side. A table gives the basis for all nine windows.
- **The four `SAVE` traps** (Chapter 1): the filename is required and comes last, buffered mode
  captures the frame you are showing, and `SAVE WINDOW` captures the screen.
- **Window lifecycle** (Chapter 1): `CLOSE` runs after the rest of its message and returns one of
  the 32 display slots; `DEBUG_END_SESSION` ends the whole session.
- **The named-color keyword system** (Appendix C): ten keywords, a 0–15 brightness, and the values
  they resolve to.
- **Create-line rules**: every value on a SCOPE_XY create line belongs to a keyword; a LOGIC
  channel color follows an explicit count.
- **Window placement**: with no `POS`, your tool places the window; give `POS` when the layout
  matters.
- **Runtime behavior worth knowing**: `OPACITY` wraps above 255, a runtime `RATE -1` stops a
  BITMAP refreshing, and a PLOT sprite's orientation is three composable bits (flip-X, flip-Y,
  transpose).
- **The unsigned operators** (Chapter 5): when a value spans the full 32-bit range, `+/` and `+//`
  are the ones you want.
- A new LOGIC example brings the downloadable library to 34 compile-clean Spin2 programs.

## v1.0.2 (2026-07-07)

**Text- and link-detail encodings aligned with Spin2 v55.** No windows, examples, or code changed.

- **PLOT text style (Chapter 5)**: the `TEXTSTYLE` bit table gives horizontal alignment as `2`=right, `3`=left, and vertical alignment as `2`=top, `3`=bottom; `$20` right-aligns. Weight values are labeled light / normal / bold / heavy.
- **TERM text size default (Chapter 3)**: `TEXTSIZE` defaults to the editor text size.
- **Multi-window debug link (Chapter 14)**: the shared debug lock is described as a hardware lock, and output-pacing guidance advises tuning combined traffic against your own serial baud rate and message sizes.

## v1.0.1 (2026-06-26)

**Accuracy and typography refresh.** Every `DEBUG()` display example uses the single-quoted text and `` `(value) `` value-substitution form the windows actually render, so the code you copy behaves exactly as the manual shows it, and the worked FFT spectrum and motor run-up programs produce the multi-tone spectrum and rising waterfall they describe. Per-window details are tightened across the book: trigger-offset behavior in LOGIC and SCOPE, parameter defaults and ranges, the PLOT polar origin, the packed-data ALT field-swap, and MIDI note-off handling. The type design moves to the current platform look, IBM Plex with cleaner, unnumbered code blocks. The downloadable library of 32 example programs is updated to match.

## v1.0.0 (2026-06-16)

**Initial release for community review.** The complete guide to the Propeller 2's nine DEBUG display windows, TERM, BITMAP, PLOT, LOGIC, SCOPE, SCOPE_XY, FFT, SPECTRO, and MIDI, documenting every window's directives, parameters, ranges, and defaults. It teaches the create-by-name / feed-by-name model and a no-hardware setup, gives a worked, software-only example in every window (thermal heatmap, PID strip-chart, glitch capture, motor run-up, and more, each with a "where you'd use this"), and works through integration topics from packed-data high-rate transfer to multi-window PASM debugging, host keyboard and mouse input, and live control panels. Includes command-reference appendices and a downloadable library of 32 compile-clean Spin2 programs that run on a bare P2 board.
