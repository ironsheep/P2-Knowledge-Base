# Appendix C: Color and Coordinate Reference {#appendix-c}

## Color values

Colors are 24-bit RGB written `$RRGGBB` (for example `$FF7F00` is orange).

### Named color keywords

Anywhere a debug display takes a color you may write a **keyword** instead of a
number. There are ten, and eight of them accept an optional trailing **brightness**
nibble, `0`–`15`, defaulting to `8`:

```debug-update
COLOR GREEN        ' green at the default brightness, 8
COLOR GREEN 15     ' the brightest green
COLOR GREEN 2      ' a dark green
```

| Keyword | at brightness 8 | Keyword | at brightness 8 |
|---------|-----------------|---------|-----------------|
| `BLACK` | `$000000` (fixed) | `CYAN` | `$09FFFF` |
| `WHITE` | `$FFFFFF` (fixed) | `RED` | `$FF0909` |
| `ORANGE` | `$FF8409` | `MAGENTA` | `$FF09FF` |
| `BLUE` | `$0909FF` | `YELLOW` | `$FFFF09` |
| `GREEN` | `$09FF09` | `GRAY` | `$848484` |

A higher brightness blends the hue toward white, a lower one toward black.
`BLACK` and `WHITE` are fixed literals and take no brightness.

> **A keyword does not reproduce the color of the same name.** The eight tinted
> keywords are *computed* through the `RGBI8X` color space, while the window's own
> defaults are fixed palette literals. They are near neighbors, not equals:
> `ORANGE` at the default brightness is `$FF8409`, but the default orange a window
> paints itself with is `$FF7F00`. If you need an exact color, write the
> `$RRGGBB` value — do not type the keyword and expect a match.
>
> One consequence catches people out: there is **no `LIME` keyword**. TERM's default
> green is the palette literal `$00FF00` (a pure, fully saturated green). The `GREEN`
> keyword resolves to `$09FF09`, which carries a little red and blue and so reads as
> slightly *washed out* next to it. To reproduce TERM's green exactly, write `$00FF00`.

### TERM color pairs

TERM holds four foreground/background pairs, selected at runtime with command codes
`4`–`7`. Defaults:

| Pair | Code | Foreground | Background |
|------|------|-----------|------------|
| 0 | `4` | Orange (`$FF7F00`) | Black |
| 1 | `5` | Black | Orange (`$FF7F00`) |
| 2 | `6` | Green (`$00FF00`) | Black |
| 3 | `7` | Black | Green (`$00FF00`) |

Set your own with `COLOR` on the creation line (eight values: fg0 bg0 fg1 bg1 fg2 bg2 fg3 bg3).

### BITMAP color modes

BITMAP and PLOT select a pixel format with one of these 19 mode keywords
(default `RGB24`), in this order:

`LUT1` `LUT2` `LUT4` `LUT8` · `LUMA8` `LUMA8W` `LUMA8X` · `HSV8` `HSV8W` `HSV8X` ·
`RGBI8` `RGBI8W` `RGBI8X` · `RGB8` (3:3:2) · `HSV16` `HSV16W` `HSV16X` ·
`RGB16` (5:6:5) · `RGB24` (8:8:8).

`LUT`-mode palettes are loaded with `LUTCOLORS`. Until you load one, every LUT
entry is `$000000` — a `LUT` mode with no `LUTCOLORS` draws a black picture.

### SPECTRO color modes

SPECTRO maps magnitude to color using `LUMA8` / `LUMA8W` / `LUMA8X` (default `LUMA8X`)
or `HSV16` / `HSV16W` / `HSV16X`.

## Coordinates

| Window | Coordinate system |
|--------|-------------------|
| TERM | Character grid, 0-based: column 0…cols−1, row 0…rows−1 (top-left = 0,0) |
| BITMAP | Pixels from the top-left; the trace cursor advances per the `TRACE` pattern, or you place it with `SET x y` |
| PLOT | Cartesian by default (origin movable with `ORIGIN`), or `POLAR` (rho, theta); `SET` positions the drawing cursor |
| SCOPE | Time advances left-to-right one step per sample set; vertical is the channel's value range (`AUTO` or `lo hi`) |
| SCOPE_XY | Centered; `SIZE` is the radius and `RANGE` the symmetric ± extent; `POLAR` accepts (rho, theta) |
| FFT | Horizontal = frequency bin (bin k ≈ k × sample_rate / N); vertical = magnitude |
| SPECTRO | At the default `TRACE $F`: horizontal = **time** (the display scrolls), vertical = **frequency**; color = magnitude. Only traces `0`–`3` swap the axes, putting frequency on the horizontal ([Chapter 10](#ch-10)) |
| MIDI | A piano keyboard spanning the note `RANGE`; key fill height = note velocity |

Frequency-in-hertz labeling for FFT and SPECTRO is your own calculation from the
sample rate and FFT size — the windows display bins, not hertz.
