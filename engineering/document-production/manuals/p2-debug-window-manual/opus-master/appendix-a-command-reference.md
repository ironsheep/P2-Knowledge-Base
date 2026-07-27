# Appendix A: Command Reference {#appendix-a}

A per-window summary of creation/configuration directives and runtime commands.
Ranges and defaults are as documented in each window's chapter. Commands shared by
every window are listed once at the end.

> **Every directive listed here is also a name your window cannot have.** The
> display parser recognizes keywords before names, so `` DEBUG(`SCOPE Trace …) ``
> or `` DEBUG(`PLOT Box …) `` declares no window — silently, with no compile
> error. Read this appendix as the reserved-word list when you name a display.
> See [Chapter 2](#ch-2).

## TERM — text terminal (Chapter 3)

**Create:** `` DEBUG(`TERM Name <config>) ``

**Configuration directives:**

| Directive | Notes |
|-----------|-------|
| `TITLE 'text'` | |
| `POS left top` | |
| `SIZE cols rows` | 1–256, default 40×20 |
| `TEXTSIZE pts` | |
| `COLOR` | 8 values = 4 fg/bg pairs |
| `BACKCOLOR rgb` | |
| `UPDATE` | |
| `HIDEXY` | |

**Feed — command codes:**

| Code | Effect |
|------|--------|
| `0` | clear + home |
| `1` | home |
| `2 col` | set column |
| `3 row` | set row |
| `4`–`7` | select color pair 0–3 |
| `8` | backspace (cursor only) |
| `9` | tab |
| `10` / `13` | newline |
| `32`–`255` | character |

**Runtime commands:**

| Directive | Notes |
|-----------|-------|
| `CLEAR` | |
| `UPDATE` | buffered repaint |
| `SAVE` | |
| `CLOSE` | close + free this window |

## BITMAP — pixel display (Chapter 4)

**Create:** `` DEBUG(`BITMAP Name <config>) ``

**Configuration directives:**

| Directive | Notes |
|-----------|-------|
| `TITLE` | |
| `POS` | |
| `SIZE w h` | 1–2048 |
| color mode | see [Appendix C](#appendix-c) |
| `DOTSIZE` | 1–256 |
| `SPARSE` | |
| `TRACE` | 0–15 |
| `RATE` | |
| `UPDATE` | |
| `HIDEXY` | |

**Feed:** numeric pixel values (streamed per the trace pattern; packable — [Appendix B](#appendix-b)).

**Runtime commands:**

| Directive | Notes |
|-----------|-------|
| `LUTCOLORS` | load palette |
| `TRACE` | |
| `RATE` | |
| `SET x y` | |
| `SCROLL` | |
| `CLEAR` | |
| `UPDATE` | |
| `SAVE` | |
| `CLOSE` | close + free this window |

*BITMAP has no drawing primitives — those belong to PLOT.*

## PLOT — vector drawing canvas (Chapter 5)

**Create:** `` DEBUG(`PLOT Name <config>) ``

**Configuration directives:**

| Directive | Notes |
|-----------|-------|
| `TITLE` | |
| `POS` | |
| `SIZE w h` | 32–2048, default 256×256 |
| `DOTSIZE x {y}` | 1–256 |
| color mode | see [Appendix C](#appendix-c) |
| `LUTCOLORS` | |
| `BACKCOLOR` | |
| `UPDATE` | |
| `HIDEXY` | |

**Position / state (Update directives):**

| Directive | Notes |
|-----------|-------|
| `SET x y` | |
| `ORIGIN {x y}` | |
| `PRECISE` | |
| `COLOR rgb` | |
| `OPACITY 0-255` | |
| `LINESIZE` | |
| `CARTESIAN {flipy {flipx}}` | |
| `POLAR {twopi {offset}}` | |
| `TEXTSIZE` | |

**Primitives (cursor-relative):**

| Directive | Notes |
|-----------|-------|
| `DOT {linesize {opacity}}` | |
| `LINE x y {linesize {opacity}}` | |
| `CIRCLE diameter {...}` | |
| `OVAL w h {...}` | |
| `BOX w h {...}` | |
| `OBOX w h xr yr {...}` | |
| `TEXT {size {style {angle}}} 'string'` | |

**Layers / sprites:**

| Directive | Notes |
|-----------|-------|
| `LAYER n 'file.bmp'` | n = 1–8 |
| `CROP n` / `CROP n AUTO x y` / `CROP n left top w h {x y}` | crop/composite a layer |
| `SPRITEDEF id xsize ysize ...` | id 0–255, size 1–32 |
| `SPRITE id orient ...` | orient 0–7 |

**Runtime commands:**

| Directive | Notes |
|-----------|-------|
| `CLEAR` | |
| `UPDATE` | buffered repaint trigger |
| `SAVE` | |
| `CLOSE` | close + free this window |

## LOGIC — logic analyzer (Chapter 6)

**Create:** `` DEBUG(`LOGIC Name <config> <channels>) ``

**Configuration directives:**

| Directive | Notes |
|-----------|-------|
| `TITLE` | |
| `POS` | |
| `SAMPLES` | 4–2047 |
| `SPACING` | 1–32 |
| `RATE` | 1–2048 |
| `DOTSIZE` | 0–32 |
| `LINESIZE` | 1–32 |
| `TEXTSIZE` | |
| `COLOR back grid` | |
| `HIDEXY` | |
| packing keyword | see [Appendix B](#appendix-b) |

**Channels (as creation elements):** `'label' {bit-count} {RANGE} {color}`. Up to 32 channels; one shared 2048-sample buffer.

**Runtime commands:**

| Directive | Notes |
|-----------|-------|
| `TRIGGER mask match {offset}` | |
| `HOLDOFF` | 2–2048 |
| `CLEAR` | |
| `SAVE` | |
| `CLOSE` | close + free this window |

*Shows raw waveforms — no built-in protocol decoding.*

## SCOPE — time-domain oscilloscope (Chapter 7)

**Create:** `` DEBUG(`SCOPE Name <config>) `` — configuration keywords only.
**Then declare channels in a second message:** `` DEBUG(`Name <channels>) ``.
A channel label on the create line **prevents the window from being created at all**.

**Configuration directives:**

| Directive | Notes |
|-----------|-------|
| `TITLE` | |
| `POS` | |
| `SIZE w h` | 32–2048 |
| `SAMPLES` | 16–2048 |
| `RATE` | 1–2048 divisor |
| `DOTSIZE` | |
| `LINESIZE` | |
| `TEXTSIZE` | |
| `COLOR back grid` | |
| `HIDEXY` | |
| packing | see [Appendix B](#appendix-b) |

**Channels (as creation elements):** `'label' {AUTO | lo hi} {tall} {base} {grid} {color}`. Up to 8 channels.

**Feed:** one numeric value per channel per time step.

**Runtime commands:**

| Directive | Notes |
|-----------|-------|
| `TRIGGER channel {AUTO | arm fire} {offset}` | rising if fire >= arm, else falling |
| `HOLDOFF` | |
| `CLEAR` | |
| `SAVE` | |
| `CLOSE` | close + free this window |

## SCOPE_XY — XY / phase display (Chapter 8)

**Create:** `` DEBUG(`SCOPE_XY Name <config> <channels>) ``

**Configuration directives:**

| Directive | Notes |
|-----------|-------|
| `TITLE` | |
| `POS` | |
| `SIZE radius` | single value |
| `RANGE extent` | single, symmetric ± |
| `SAMPLES` | persistence depth; 0 = no fade |
| `RATE` | |
| `DOTSIZE` | |
| `TEXTSIZE` | |
| `COLOR back {grid}` | |
| `POLAR {twopi {offset}}` | |
| `LOGSCALE` | |
| `HIDEXY` | |

**Channels:** `'name' {color}` (up to 8).

**Feed:** `` `(x, y) `` pairs (in channel order).

**Runtime commands:**

| Directive | Notes |
|-----------|-------|
| `CLEAR` | |
| `SAVE` | |
| `CLOSE` | close + free this window |

## FFT — frequency spectrum (Chapter 9)

**Create:** `` DEBUG(`FFT Name <config>) `` — configuration keywords only.
**Then declare channels in a second message:** `` DEBUG(`Name <channels>) ``.
A channel label placed on the create line is rejected by the parser.

**Configuration directives:**

| Directive | Notes |
|-----------|-------|
| `TITLE` | |
| `POS` | |
| `SIZE w h` | 32–2048 px |
| `SAMPLES N {first last}` | N = FFT size, power of 2, 4–2048; optional bin range |
| `RATE` | 1–2048 |
| `DOTSIZE` | |
| `LINESIZE` | −32…32; negative = filled bars |
| `TEXTSIZE` | |
| `COLOR back grid` | |
| `LOGSCALE` | logarithmic amplitude |
| `HIDEXY` | |

**Channels:** `'label' MAG-shift(0-11) high tall base grid color`. A Hanning window is always applied; it is not selectable.

**Runtime commands:**

| Directive | Notes |
|-----------|-------|
| `CLEAR` | |
| `SAVE` | |
| `CLOSE` | close + free this window |

## SPECTRO — spectrogram / waterfall (Chapter 10)

**Create:** `` DEBUG(`SPECTRO Name <config>) `` (single channel)

**Configuration directives:**

| Directive | Notes |
|-----------|-------|
| `TITLE` | |
| `POS` | |
| `SAMPLES` | FFT size, power of 2, 4–2048 |
| `DEPTH` | 1–2048 |
| `RANGE ceiling` | single value |
| `RATE` | 1–2048; default SAMPLES/8 |
| `TRACE` | 0–15; bit 3 = scroll |
| `MAG` | 0–11 |
| `DOTSIZE` | 1–16 |
| `LOGSCALE` | |
| `HIDEXY` | |
| color mode | LUMA8/W/X, HSV16/W/X |
| packing | see [Appendix B](#appendix-b) |

**Runtime commands:**

| Directive | Notes |
|-----------|-------|
| `CLEAR` | |
| `SAVE` | |
| `CLOSE` | close + free this window |

## MIDI — piano-keyboard display (Chapter 11)

**Create:** `` DEBUG(`MIDI Name <config>) ``

**Configuration directives:**

| Directive | Notes |
|-----------|-------|
| `TITLE` | |
| `POS` | |
| `SIZE` | key-size multiplier 1–50, default 4 |
| `RANGE first last` | notes 0–127, default 21–108 |
| `CHANNEL` | 0–15, default 0 |
| `COLOR white-active black-active` | two RGB24; defaults cyan/magenta |

**Feed:** raw MIDI bytes as numeric values — Note-On `$9n note velocity`, Note-Off `$8n note velocity` (running status supported). Only `$8n`/`$9n` are recognized.

**Runtime commands:**

| Directive | Notes |
|-----------|-------|
| `CLEAR` | |
| `SAVE` | |
| `CLOSE` | close + free this window |

## Commands common to every window

- `` DEBUG(`Name `PC_KEY(@keyvar)) `` — host writes the latest key code (0 if none) into the long at `@keyvar`. **Note the second backtick**: `PC_KEY` is a Spin2 debug command, not display text, so it must be ticked back into command mode. See [Chapter 12](#ch-12) for the key-code table.
- `` DEBUG(`Name `PC_MOUSE(@mousevar)) `` — host fills a 7-long array: xpos, ypos, wheel, left, middle, right (each button 0 or −1), pixel-under-cursor. Same backtick rule as `PC_KEY`. See [Chapter 12](#ch-12).
- `` DEBUG(`Name CLEAR) `` — clear the window.
- `` DEBUG(`Name SAVE {WINDOW} 'file') `` — save to `file.bmp` on the host (no
  extension in the name). **The filename is required and must be last**: a bare
  `SAVE` writes nothing, and a keyword placed after `SAVE` is consumed and discarded.
  In buffered mode `SAVE` captures the *front* buffer — send `` `UPDATE `` first. See
  [Chapter 1](#ch-1).
- `` DEBUG(`Name CLOSE) `` — close and free this one window; reclaims one of the 32
  display slots. Runs *after* the rest of its message, and accepts several window
  names. A different action from ending the whole debug session; works on all nine
  window types.
- `` DEBUG(DEBUG_END_SESSION) `` — `{Spin2_v52}`. Ends the whole session: closes every
  window and the `DEBUG.LOG` file. The P2 program keeps running. Note this is a
  `DEBUG()` statement in its own right, not a `` `Name `` window command.
