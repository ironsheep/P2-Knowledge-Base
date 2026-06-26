# P2 Debug Window Manual — Change Log

## v1.0.1 (2026-06-26)

**Accuracy and typography refresh.** Every `DEBUG()` display example uses the single-quoted text and `` `(value) `` value-substitution form the windows actually render, so the code you copy behaves exactly as the manual shows it — and the worked FFT spectrum and motor run-up programs produce the multi-tone spectrum and rising waterfall they describe. Per-window details are tightened across the book: trigger-offset behavior in LOGIC and SCOPE, parameter defaults and ranges, the PLOT polar origin, the packed-data ALT field-swap, and MIDI note-off handling. The type design moves to the current platform look — IBM Plex with cleaner, unnumbered code blocks. The downloadable library of 32 example programs is updated to match.

## v1.0.0 (2026-06-16)

**Initial release for community review.** The complete guide to the Propeller 2's nine DEBUG display windows — TERM, BITMAP, PLOT, LOGIC, SCOPE, SCOPE_XY, FFT, SPECTRO, and MIDI — documenting every window's directives, parameters, ranges, and defaults. It teaches the create-by-name / feed-by-name model and a no-hardware setup, gives a worked, software-only example in every window (thermal heatmap, PID strip-chart, glitch capture, motor run-up, and more, each with a "where you'd use this"), and works through integration topics from packed-data high-rate transfer to multi-window PASM debugging, host keyboard and mouse input, and live control panels. Includes command-reference appendices and a downloadable library of 32 compile-clean Spin2 programs that run on a bare P2 board.
