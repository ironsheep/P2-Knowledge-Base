# Appendix A: Command Reference

A per-window summary of creation/configuration keywords and runtime commands.
Ranges and defaults are as documented in each window's chapter. Commands shared by
every window are listed once at the end.

## TERM — text terminal (Chapter 3)

**Create:** `` DEBUG(`TERM Name <config>) ``
**Config:** `TITLE 'text'` · `POS left top` · `SIZE cols rows` (1–256, default 40×20) · `TEXTSIZE pts` · `COLOR` (8 values = 4 fg/bg pairs) · `BACKCOLOR rgb` · `UPDATE` · `HIDEXY`
**Feed — command codes:** `0` clear+home · `1` home · `2 col` set column · `3 row` set row · `4`–`7` select color pair 0–3 · `8` backspace (cursor only) · `9` tab · `10`/`13` newline · `32`–`255` character
**Runtime keywords:** `CLEAR` · `UPDATE` (buffered repaint) · `SAVE`

## BITMAP — pixel display (Chapter 4)

**Create:** `` DEBUG(`BITMAP Name <config>) ``
**Config:** `TITLE` · `POS` · `SIZE w h` (1–2048) · color mode (see Appendix C) · `DOTSIZE` (1–256) · `SPARSE` · `TRACE` (0–15) · `RATE` · `UPDATE` · `HIDEXY`
**Feed:** numeric pixel values (streamed per the trace pattern; packable — Appendix B)
**Runtime:** `LUTCOLORS` (load palette) · `TRACE` · `RATE` · `SET x y` · `SCROLL` · `CLEAR` · `UPDATE` · `SAVE`. *BITMAP has no drawing primitives — those belong to PLOT.*

## PLOT — vector drawing canvas (Chapter 5)

**Create:** `` DEBUG(`PLOT Name <config>) ``
**Config:** `TITLE` · `POS` · `SIZE w h` (32–2048, default 256×256) · `DOTSIZE x {y}` (1–256) · color mode (see Appendix C) · `LUTCOLORS` · `BACKCOLOR` · `UPDATE` · `HIDEXY`
**Position/state (runtime):** `SET x y` · `ORIGIN {x y}` · `PRECISE` · `COLOR rgb` · `OPACITY 0-255` · `LINESIZE` · `CARTESIAN {flipy {flipx}}` · `POLAR {twopi {theta}}` · `TEXTSIZE`
**Primitives (cursor-relative):** `DOT {linesize {opacity}}` · `LINE x y {linesize {opacity}}` · `CIRCLE diameter {...}` · `OVAL w h {...}` · `BOX w h {...}` · `OBOX w h xr yr {...}` · `TEXT {size {style {angle}}} 'string'`
**Layers/sprites:** `LAYER n 'file.bmp'` (n = 1–8) · `CROP n` / `CROP n AUTO x y` / `CROP n left top w h {x y}` · `SPRITEDEF id xsize ysize ...` (id 0–255, size 1–32) · `SPRITE id orient ...` (orient 0–7)
**Runtime:** `CLEAR` · `UPDATE` (buffered repaint trigger) · `SAVE`

## LOGIC — logic analyzer (Chapter 6)

**Create:** `` DEBUG(`LOGIC Name <config> <channels>) ``
**Config:** `TITLE` · `POS` · `SAMPLES` (4–2047) · `SPACING` (1–32) · `RATE` (1–2048) · `DOTSIZE` (0–32) · `LINESIZE` (1–32) · `TEXTSIZE` · `COLOR back grid` · `HIDEXY` · packing keyword (Appendix B)
**Channels (as creation elements):** `'label' {bit-count} {RANGE} {color}`. Up to 32 channels; one shared 2048-sample buffer.
**Runtime:** `TRIGGER mask match {offset}` · `HOLDOFF` (2–2048) · `CLEAR` · `SAVE`. *Shows raw waveforms — no built-in protocol decoding.*

## SCOPE — time-domain oscilloscope (Chapter 7)

**Create:** `` DEBUG(`SCOPE Name <config> <channels>) ``
**Config:** `TITLE` · `POS` · `SIZE w h` (32–2048) · `SAMPLES` (16–2048) · `RATE` (1–2048 divisor) · `DOTSIZE` · `LINESIZE` · `TEXTSIZE` · `COLOR back grid` · `HIDEXY` · packing
**Channels (as creation elements):** `'label' {AUTO | lo hi} {tall} {base} {grid} {color}`. Up to 8 channels.
**Feed:** one numeric value per channel per time step.
**Runtime:** `TRIGGER channel {AUTO | arm fire} {offset}` (rising if fire≥arm, else falling) · `HOLDOFF` · `CLEAR` · `SAVE`

## SCOPE_XY — XY / phase display (Chapter 8)

**Create:** `` DEBUG(`SCOPE_XY Name <config> <channels>) ``
**Config:** `TITLE` · `POS` · `SIZE radius` (single value) · `RANGE extent` (single, symmetric ±) · `SAMPLES` (persistence depth; 0 = no fade) · `RATE` · `DOTSIZE` · `TEXTSIZE` · `COLOR back {grid}` · `POLAR {twopi {offset}}` · `LOGSCALE` · `HIDEXY`
**Channels:** `'name' {color}` (up to 8). **Feed:** `` `(x, y) `` pairs (in channel order).
**Runtime:** `CLEAR` · `SAVE`

## FFT — frequency spectrum (Chapter 9)

**Create:** `` DEBUG(`FFT Name <config> <channels>) ``
**Config:** `TITLE` · `POS` · `SIZE w h` (32–2048 px) · `SAMPLES N {first last}` (N = FFT size, power of 2, 4–2048; optional bin range) · `RATE` (1–2048) · `DOTSIZE` · `LINESIZE` (−32…32; negative = filled bars) · `TEXTSIZE` · `COLOR back grid` · `LOGSCALE` (log2 amplitude) · `HIDEXY`
**Channels:** `'label' MAG-shift(0-11) high tall base grid color`. A Hanning window is always applied; it is not selectable.
**Runtime:** `CLEAR` · `SAVE`

## SPECTRO — spectrogram / waterfall (Chapter 10)

**Create:** `` DEBUG(`SPECTRO Name <config>) `` (single channel)
**Config:** `TITLE` · `POS` · `SAMPLES` (FFT size, power of 2, 4–2048) · `DEPTH` (1–2048) · `RANGE ceiling` (single value) · `RATE` (1–2048; default SAMPLES/8) · `TRACE` (0–15; bit 3 = scroll) · `MAG` (0–11) · `DOTSIZE` (1–16) · `LOGSCALE` · `HIDEXY` · color mode (LUMA8/W/X, HSV16/W/X) · packing
**Runtime:** `CLEAR` · `SAVE`

## MIDI — piano-keyboard display (Chapter 11)

**Create:** `` DEBUG(`MIDI Name <config>) ``
**Config:** `TITLE` · `POS` · `SIZE` (key-size multiplier 1–50, default 4) · `RANGE first last` (notes 0–127, default 21–108) · `CHANNEL` (0–15, default 0) · `COLOR white-active black-active` (two RGB24; defaults cyan/magenta)
**Feed:** raw MIDI bytes as numeric values — Note-On `$9n note velocity`, Note-Off `$8n note velocity` (running status supported). Only `$8n`/`$9n` are recognized.
**Runtime:** `CLEAR` · `SAVE`

## Commands common to every window

- `` DEBUG(`Name PC_KEY(@keyvar)) `` — host writes the latest key code (0 if none) into the long at `@keyvar`. See Chapter 12 for the key-code table.
- `` DEBUG(`Name PC_MOUSE(@mousevar)) `` — host fills a 7-long array: xpos, ypos, wheel, left, middle, right (each button 0 or −1), pixel-under-cursor. See Chapter 12.
- `` DEBUG(`Name CLEAR) `` — clear the window.
- `` DEBUG(`Name SAVE {WINDOW} 'file') `` — save the window image to a host file.
