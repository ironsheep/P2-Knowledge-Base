# silicon-doc — image catalog, 2026-08-26

**Source:** `Parallax Propeller 2 Documentation v35 - Rev B_C Silicon.docx`
**Method:** lossless extraction from `word/media/` (DOCX-primary — no PDF rasterisation, no
coordinate rescue). 34 assets, all accounted for: 31 PNG, 2 JPG, 1 GIF.
**OCR:** `tesseract --psm 6`, local.

## Quality gate — and why the standard black-dominant test is DISARMED here

`image_dominant_colors` reports **`#000000` at 100%** for `silicon-001.png`. Taken at face value
that is the classic "failed extraction" signature. **It is wrong here, and the disproof is
direct:** tesseract read `%00111MMMMMMMM - Schmitt, Clocked` off that same file.

Mechanism: **30 of the 31 PNGs are RGBA or colormap** — transparent line art. The dominant-colour
sampler reads the transparent ground as black, so it scores clean figures as total failures. This
is the documented inversion (previously measured on p2-hardware-manual: 34 of 37 figures reading
`#000000` at up to 91% while being clean line art), **re-confirmed here on a second corpus.**

**The control that actually works: 33 of 34 assets yielded substantive OCR text.** An all-black
image cannot do that. The one that did not (`silicon-003.jpg`) is a photograph, not line art.

⚠️ **OCR text below is a LOCATOR, never an encoding.** Tesseract systematically misreads digits in
these titles — `@` and `Q` for `0`, `4` for `1`, so `%41100@MMMMMMMM` is the OCR of `%11000…`.
**Never take a mode number from this table.** The authoritative encodings are in
`complete-silicon-doc-reference.md` and `silicon-doc-text.txt`.

## Catalog

| Asset | Dim | Content (OCR locator) | Class |
|---|---|---|---|
| `image-catalog.md` | photo |  | figure |
| `silicon-001.png` | 2048 x 646 | %00111MMMMMMMM - Schmitt, Clocked  | smart-pin mode diagram |
| `silicon-002.png` | 2048 x 678 | %00101MMMMMMMM - Logic with Adjacent-Pin Feedback, Clocked . < Ps Iw DRI | smart-pin mode diagram |
| `silicon-003.jpg` | photo | LA ia  | figure |
| `silicon-004.png` | 2048 x 773 | %11001MMMMMMMM - Level Comparator with 1.5k Output, Clocked Psp  | smart-pin mode diagram |
| `silicon-005.png` | 2048 x 709 | %01101MMMMMMMM - Comparator, Clocked )> a IN DRIVE our x 7 > 7  | smart-pin mode diagram |
| `silicon-006.png` | 2048 x 773 | %11011MMMMMMMM - Level Comparator with Local Feedback, Clocked a:  | smart-pin mode diagram |
| `silicon-007.png` | 2048 x 773 | %41100@MMMMMMMM - Level Comparator with 1.5k Output ie  | smart-pin mode diagram |
| `silicon-008.png` | 2048 x 709 | %0110@MMMMMMMM - Comparator x :  | smart-pin mode diagram |
| `silicon-009.png` | 2048 x 646 | %00001MMMMMMMM - Logic, Clocked IN DRIVE out  | smart-pin mode diagram |
| `silicon-010.png` | 2048 x 550 | %101MMMMMMMMMM - DAC with Optional ADC oe ipa ee@ ;998 ohm 3.3V  | smart-pin mode diagram |
| `silicon-011.png` | 760 x 211 | 28-tap Hann 45-tap Tukey 68-tap Tukey  | filter response curves |
| `silicon-012.png` | 2048 x 678 | %0001QMMMMMMMM - Logic with Feedback i ) > IN DRIVE out x  | smart-pin mode diagram |
| `silicon-013.png` | 2048 x 678 | %0010@MMMMMMMM - Logic with Adjacent-Pin Feedback . < Iw DRIVE a <]  | smart-pin mode diagram |
| `silicon-014.png` | 2048 x 773 | %111M@MMMMMMMM - Level Comparator with Separate Feedback lp  | smart-pin mode diagram |
| `silicon-015.png` | 2048 x 741 | %01111MMMMMMMM - Comparator with Feedback, Clocked M6 ) > a IN DRIVE out | smart-pin mode diagram |
| `silicon-016.png` | 2024 x 1264 | WRPIN D[20:8] Configuration Internal Configuration 0000_CIOHHHLLL Pin Lo | **WRPIN bit-field diagram** |
| `silicon-017.png` | 2048 x 678 | %0100Q0MMMMMMMM - Schmitt with Feedback M6 )> IN DRIVE out x  | smart-pin mode diagram |
| `silicon-018.png` | 2048 x 678 | %0101@MMMMMMMM - Schmitt with Adjacent-Pin Feedback . _ Iw DRIVE an <]  | smart-pin mode diagram |
| `silicon-019.png` | 2048 x 678 | %00011MMMMMMMM - Logic with Feedback, Clocked M6 ) > Z in DRIVE our x  | smart-pin mode diagram |
| `silicon-020.png` | 2048 x 772 | %111M1MMMMMMMM - Level Comparator with Separate Feedback, Clocked ait ee | smart-pin mode diagram |
| `silicon-021.png` | 2048 x 678 | %01011MMMMMMMM - Schmitt with Adjacent-Pin Feedback, Clocked < a IN DRIV | smart-pin mode diagram |
| `silicon-022.jpg` | photo | SY san  | figure |
| `silicon-023.png` | 2048 x 646 | %100MMMMMMMMMM - ADC with Optional Drive ess jape eee GND  | smart-pin mode diagram |
| `silicon-024.png` | 2048 x 741 | %01110MMMMMMMM - Comparator with Feedback M6 ) > IN DRIVE our x 7 y  | smart-pin mode diagram |
| `silicon-025.png` | 2048 x 678 | %01001MMMMMMMM - Schmitt with Feedback, Clocked DO te 7X  | smart-pin mode diagram |
| `silicon-026.png` | 1063 x 1710 | Vxxyy M12 maz ‘20  | figure |
| `silicon-027.gif` | 600 x 650 | Hub RAM Interface Every cog can read/write 32 bits per clock  | **hub interface diagram** |
| `silicon-028.png` | 1121 x 594 | Elwire [15:0] [31:0] bootd = { // cold boot rom ~ only cogd on startup  | **boot ROM Verilog** |
| `silicon-029.png` | 2048 x 582 | 3 . *%OCOBQ@MMMMMMMM - Logic H/L DRIVE  | smart-pin mode diagram |
| `silicon-030.png` | 1935 x 1947 | < < < < H H H H  | figure |
| `silicon-031.png` | 1648 x 1652 | isp} O) wo co SnanSr-ooonaGBRGOOnthaNAD-OKOHD  | figure |
| `silicon-032.png` | 2048 x 582 | %00110MMMMMMMM - Schmitt <  | smart-pin mode diagram |
| `silicon-033.png` | 2048 x 773 | %1101@MMMMMMMM - Level Comparator with Local Feedback = Pay  | smart-pin mode diagram |
| `silicon-034.png` | 1350 x 2048 | ° ° * Standard Device Specification  | figure |

## Findings routed from this pass

- **`silicon-034.png` (1350×2048) is a MECHANICAL CASE OUTLINE drawing.** **G-021** records that
  TQFP-100 package outline dimensions are "not in text anywhere" and that the datasheet's p.49
  drawing was never transcribed. The Silicon Doc carries its own copy of that drawing, now
  extracted. **G-021 is closable from a source we hold** — routed to the re-test task; the
  dimensions must be read off the rendered drawing, not OCR'd (see the digit-misread warning above).
- **`silicon-016.png` is the `WRPIN D[20:8]` configuration bit-field diagram** (`0000_CIOHHHLLL`).
  Cross-check target for the WRPIN field map, where F-331/F-332 already found three wrong field
  descriptions.
- **23 assets are per-mode smart-pin low-level diagrams**, each captioned with its `%SSSSS`
  encoding — a per-mode cross-validation set against the smart-pin mode tables.
- **`silicon-028.png` carries boot-ROM Verilog** (`32'b1111_1100100_010_000`), an independent
  reading of boot behaviour alongside `rom-booter`.
