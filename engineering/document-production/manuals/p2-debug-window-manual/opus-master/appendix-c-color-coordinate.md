# Appendix C: Color and Coordinate Reference {#appendix-c}

## Color values

Colors are 24-bit RGB written `$RRGGBB` (for example `$FF7F00` is orange). You can
also use the Spin2 named color constants where a color is expected.

### TERM color pairs

TERM holds four foreground/background pairs, selected at runtime with command codes
`4`–`7`. Defaults:

| Pair | Code | Foreground | Background |
|------|------|-----------|------------|
| 0 | `4` | Orange | Black |
| 1 | `5` | Black | Orange |
| 2 | `6` | Lime | Black |
| 3 | `7` | Black | Lime |

The default green is `clLime` (`$00FF00`) — pure green, brighter than the `GREEN`
keyword (`$09FF09`). There is no `LIME` keyword; reproduce it with `$00FF00`.

Set your own with `COLOR` on the creation line (eight values: fg0 bg0 fg1 bg1 fg2 bg2 fg3 bg3).

### BITMAP color modes

BITMAP selects a pixel format with one of these mode keywords (default `RGB24`):
`LUT1` `LUT2` `LUT4` `LUT8` · `LUMA8` `LUMA8W` `LUMA8X` · `RGBI8` `RGBI8W` `RGBI8X` ·
`HSV8` `HSV8W` `HSV8X` · `HSV16` `HSV16W` `HSV16X` · `RGB8` (3:3:2) · `RGB16` (5:6:5) · `RGB24` (8:8:8).
`LUT`-mode palettes are loaded with `LUTCOLORS`.

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
| SPECTRO | Horizontal = frequency; the display scrolls over time per `TRACE`/`RATE`; color = magnitude |
| MIDI | A piano keyboard spanning the note `RANGE`; key fill height = note velocity |

Frequency-in-hertz labeling for FFT and SPECTRO is your own calculation from the
sample rate and FFT size — the windows display bins, not hertz.
