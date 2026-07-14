# P2 Debug Window Manual — Change Log

## v1.1.0 (2026-07-14)

**Verified against real silicon — and it changed the book.** Every load-bearing claim in this
manual was re-tested against a P2 running PNut, and the results corrected code and text that had
been wrong since the first edition. **Six defects were serious enough to block a release, and
three of them were in example programs you may have downloaded and run.** If you have used the
example library, replace it: the ZIP has been rebuilt.

**Corrected example programs — please re-download:**

- **The PLOT chapter's sine wave was a flat line.** `ch05-plot-wave-scatter.spin2` computed its
  angle step with `/`, and Spin2's `/` is a **signed** divide — so `$FFFF_FFFF / 511` was `−1 / 511`,
  which is **0**. Every column got the same angle, and the "one cycle of a CORDIC sine wave" drew as a
  horizontal line lying exactly on top of the grey axis the program draws two statements earlier. It
  compiled, it ran, and it looked plausible. Fixed to the unsigned `+/`, and Chapter 5 now teaches the
  trap.
- **The packed-data examples replayed time backwards.** Both `ch13-packed-logic-*` programs packed
  their samples MSB-first while the host unpacks LSB-first — so each long replayed in **reverse time
  order**, contradicting the chapter's own stated rule. The bug survived a run on real hardware because
  the payload was random: reversed noise looks exactly like forward noise.
- **The LOGIC chapter's first example declared 32 channels, not 4.** The first number after a channel
  label is the channel **count**, so `'CLK' $00FF00` asked for 65,280 channels — and `DATA`, `CS`, and
  `WR` were silently dropped. Chapter 6 now shows the explicit counts, states the rule, and ships as a
  compile-and-run example program of its own (it had none before, which is exactly why the error
  survived).

**Corrections to the text:**

- **PLOT `PRECISE` was documented backwards** — sub-pixel positioning is **off** by default, so the
  first `PRECISE` turns it *on*.
- **PLOT text came out invisible.** `COLOR` only becomes the *text* color when `TEXT` is the very next
  key — so the labels example was drawing white text on a white background. Chapter 5 shows the correct
  idiom.
- **SPECTRO's axes were inverted in Appendix C** — at the default `TRACE $F`, the horizontal axis is
  **time** and the vertical is frequency. (Chapter 10 already had this right; the appendix contradicted
  its own chapter.)
- **SCOPE:** a channel definition on the create line does not "open a window with no channels" — it
  **prevents the window from being created at all**. And the chapter's `SAVE` example wrote nothing: the
  filename is required.
- **FFT:** `LOGSCALE` does not draw "power-of-2 markers" — it draws nothing but the word `logscale`.
  `MAG` is a **gain**, not an attenuation. The channel `grid` field is 4 bits, and the upper two print
  legend text.
- **MIDI:** a string in the feed **aborts the rest of the message** rather than being ignored.
- **LINESIZE is measured in half-pixels** in the LOGIC, SCOPE, and FFT windows — the default `3` draws a
  1.5-pixel trace. `DOTSIZE` is a whole-pixel diameter in those windows, but half-pixels in SCOPE_XY.

**New material — things the manual never told you:**

- **The mouse gives your program raw pixels, not the number on the screen.** In the LOGIC, SCOPE,
  SCOPE_XY, FFT, and MIDI windows, the friendly coordinate shown next to the pointer is drawn by the
  host; what `PC_MOUSE` actually delivers to the P2 is the **raw pixel position**. Any hit-test built on
  the readout is quietly wrong. Chapter 12 now spells out what each window really sends.
- **The four `SAVE` traps** (Chapter 1), all silent: no filename means no file; a keyword after `SAVE`
  is swallowed; in buffered mode `SAVE` captures the *previous* frame unless you `UPDATE` first; and
  `SAVE WINDOW` scrapes the desktop.
- **Every value on a `SCOPE_XY` create line must belong to a keyword** — a bare number, typically left
  stranded by a dropped `SIZE` keyword, is invalid there, and a debug tool has no window in which to report
  it. Chapter 8 now says what to check when a SCOPE_XY window never appears.
- **`OPACITY 256` makes everything vanish** — the value wraps to 0, fully transparent.
- **A runtime `` `RATE -1 `` freezes a BITMAP** (it is a create-line-only shorthand).
- **The named-color keyword system** (Appendix C) — ten keywords with a brightness nibble — and the
  catch that a keyword does **not** reproduce the palette color of the same name.
- **`DEBUG_END_SESSION`**, the counterpart to `CLOSE` that ends the whole session (Chapter 1).
- **`CLOSE` semantics** — it runs *after* the rest of its message, and gives back one of the 32 display
  slots.
- **Window placement is up to your tool.** Omit `POS` and where the window lands is not a P2 behavior —
  some hosts tile, some stack. Give `POS` when the layout matters.

## v1.0.2 (2026-07-07)

**Text- and link-detail encodings aligned with Spin2 v55.** No windows, examples, or code changed.

- **PLOT text style (Chapter 5)** — the `TEXTSTYLE` bit table gives horizontal alignment as `2`=right, `3`=left, and vertical alignment as `2`=top, `3`=bottom; `$20` right-aligns. Weight values are labeled light / normal / bold / heavy. *(Later confirmed on hardware: the vertical values printed here are correct, and differ from the Spin2 v55 reference — see v1.1.0.)*
- **TERM text size default (Chapter 3)** — `TEXTSIZE` defaults to the editor text size.
- **Multi-window debug link (Chapter 14)** — the shared debug lock is described as a hardware lock, and output-pacing guidance advises tuning combined traffic against your own serial baud rate and message sizes.

## v1.0.1 (2026-06-26)

**Accuracy and typography refresh.** Every `DEBUG()` display example uses the single-quoted text and `` `(value) `` value-substitution form the windows actually render, so the code you copy behaves exactly as the manual shows it — and the worked FFT spectrum and motor run-up programs produce the multi-tone spectrum and rising waterfall they describe. Per-window details are tightened across the book: trigger-offset behavior in LOGIC and SCOPE, parameter defaults and ranges, the PLOT polar origin, the packed-data ALT field-swap, and MIDI note-off handling. The type design moves to the current platform look — IBM Plex with cleaner, unnumbered code blocks. The downloadable library of 32 example programs is updated to match.

## v1.0.0 (2026-06-16)

**Initial release for community review.** The complete guide to the Propeller 2's nine DEBUG display windows — TERM, BITMAP, PLOT, LOGIC, SCOPE, SCOPE_XY, FFT, SPECTRO, and MIDI — documenting every window's directives, parameters, ranges, and defaults. It teaches the create-by-name / feed-by-name model and a no-hardware setup, gives a worked, software-only example in every window (thermal heatmap, PID strip-chart, glitch capture, motor run-up, and more, each with a "where you'd use this"), and works through integration topics from packed-data high-rate transfer to multi-window PASM debugging, host keyboard and mouse input, and live control panels. Includes command-reference appendices and a downloadable library of 32 compile-clean Spin2 programs that run on a bare P2 board.
