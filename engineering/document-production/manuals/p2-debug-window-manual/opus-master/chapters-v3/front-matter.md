# P2 Debug Window Manual

*See What Your Program Is Doing — Nine Display Windows for the Propeller 2*

**Author:** Iron Sheep Productions, LLC
**Compiler:** `pnut_ts`  **Debug host:** `pnut_term_ts`
**Version:** Version 1.0 (draft)  **Date:** May 2026

---

## How this manual is organized

The P2's `DEBUG` system can do far more than print text. It drives nine graphical
display windows — terminals, bitmaps, plots, logic and waveform views, spectrum
and spectrogram displays, and a MIDI keyboard — all from `DEBUG()` statements in
your own program, with no external hardware.

- **Part I — Foundation (Chapters 1–2)** establishes the shared model: how you
  create a window, feed it by name, and read its output, and how to get a first
  window on screen.
- **Part II — The Windows (Chapters 3–11)** is one chapter per window type:
  TERM, BITMAP, PLOT, LOGIC, SCOPE, SCOPE_XY, FFT, SPECTRO, and MIDI. Each chapter
  covers creating the window, feeding it data, its full command set, and a complete
  worked example you can run with no wiring.
- **Part III — Integration (Chapters 12–14)** covers the features that span
  windows: reading the host keyboard and mouse, sending data compactly with packed
  formats, using several windows at once, and debugging from PASM.
- **Appendices** give a per-window command reference, the packed-data formats, and
  a color and coordinate reference.

Every example in this manual compiles with `pnut_ts` and runs on a bare P2 board
plus a PC — the data is generated in software, so you can see each window work
before you connect anything to the chip.

> The *single-step debugger* — which halts and steps your code — is a different
> tool with its own manual. This manual is about the *display* windows, which
> visualize data while your program runs.
