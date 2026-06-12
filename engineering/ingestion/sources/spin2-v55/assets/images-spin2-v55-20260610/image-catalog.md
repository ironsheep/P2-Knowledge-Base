# Spin2 v55 — Image Catalog

**Source:** `Parallax Spin2 Documentation v55.docx` (24 embedded figures, all PNG/GIF — directly viewable).  
**Extracted:** 2026-06-10 via DOCX `word/media/` (lossless; no PyMuPDF/coordinate-rescue needed).  
**Quality:** 0 black/failed extractions (DOCX-media source eliminates that failure class).

| File | WxH | Location in doc | Purpose |
|------|-----|-----------------|---------|
| `image1.gif` | 452x268 | SPECTRO Display Spectrograph with 4..2048- | waitus(100) |
| `image2.png` | 795x1740 | PASM-Level Debugger | For decent debugger performance, it is necessary to go into the Window |
| `image3.png` | 226x249 | SCOPE_XY Display XY oscilloscope with 1..8 | debug(`MyXY `(x,y)) |
| `image4.png` | 445x321 | FIELD POINTERS | debug(ubin_long(k)) |
| `image5.gif` | 594x154 | MIDI Display MIDI keyboard for viewing not | debug(`MyMidi $80 `(i, 0)) |
| `image6.png` | 805x1174 | BITMAP Display Pixel-driven bitmap | image5 file "bird_rgb24.bmp" |
| `image7.gif` | 324x347 | SCOPE_XY Display XY oscilloscope with 1..8 | waitms(5) |
| `image8.png` | 805x879 | BITMAP Display Pixel-driven bitmap | * Color is ORANGE / BLUE / GREEN / CYAN / RED / MAGENTA / YELLOW / GRA |
| `image9.gif` | 267x161 | BITMAP Display Pixel-driven bitmap | long %%0000000000000000 |
| `image10.gif` | 553x152 | Graphical DEBUG Displays | waitms(50) |
| `image11.png` | 226x249 | SCOPE_XY Display XY oscilloscope with 1..8 | debug(`MyXY `(x,y)) |
| `image12.gif` | 433x89 | LOGIC Display Logic analyzer with single a | waitms(20) |
| `image13.png` | 906x179 | SPECTRO Display Spectrograph with 4..2048- | Below, a SPECTRO display was fed ADC samples from a pin attached to a  |
| `image14.gif` | 297x121 | TERM Display Terminal for displaying text | waitms(500) |
| `image15.gif` | 360x452 | BITMAP Display Pixel-driven bitmap | Rate is set to 1 so that each pixel can be seen as it's loaded. |
| `image16.gif` | 408x511 | PLOT Display General-purpose plotter with  | k++ |
| `image17.png` | 1113x805 | PASM-Level Debugger | Note that 'DEBUG' break sensitivity is exclusive to all but 'INIT' (CO |
| `image18.gif` | 326x149 | LOGIC Display Logic analyzer with single a | waitms(25) |
| `image19.png` | 572x304 | FIELD POINTERS | debug(ubin_long(k), udec(field[p]++)) 'show k and three bits via p |
| `image20.png` | 1113x805 | PASM-Level Debugger | Note that 'DEBUG' break sensitivity is exclusive to all but 'INIT' (CO |
| `image21.gif` | 579x268 | FFT Display Fast Fourier Transform with 1. | waitus(100) |
| `image22.gif` | 846x131 | MIDI Display MIDI keyboard for viewing not | x res 1 |
| `image23.png` | 667x448 | DEBUG() memory utilization | that a bytecode is needed to read the variable 'i', and then three obl |
| `image24.gif` | 278x324 | SCOPE Display Oscilloscope with 1..8 chann | waitus(200) |

## Notes
- All 24 figures are DEBUG-display screenshots / illustrative diagrams (SCOPE, SCOPE_XY, LOGIC, BITMAP, PLOT, FFT, MIDI, SPECTRO, TERM), the PASM-Level Debugger, FIELD POINTERS, and DEBUG() memory utilization.
- These are **screenshots** (high color count), not line-diagrams, so OCR yields limited structured text; figure *purpose* is carried by the doc heading/caption mapping above.
- `image-tools-mcp` available for on-demand OCR/region analysis of any figure (quality-gate + label extraction).
