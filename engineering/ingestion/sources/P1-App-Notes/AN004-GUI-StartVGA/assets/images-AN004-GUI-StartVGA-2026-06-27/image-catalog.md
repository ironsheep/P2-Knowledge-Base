# AN004 — Image Catalog (pass 3)

**Extraction:** `pdfimages -png` from `AN004-GUI-StartVGA-v1.0.pdf` (PDF-only ladder).
16 embedded raster images → 7 logical figures. **Quality gate:** all images passed —
`image_dominant_colors` shows healthy palettes (no `#000000`-dominant failures, no
full-page mis-captures). Diagram figures OCR'd with `image_ocr_full`.

| File | Pg | px (W×H) | Figure | Type | Quality |
|---|---:|---|---|---|---|
| `an004-img-000.png` | 2 | 897×287 | **Figure 1** (base) | Line diagram | PASS (light-grey diagram, 0.96% black) |
| `an004-img-001.png` | 2 | 897×287 | **Figure 1** (overlay/mask layer) | Line diagram | PASS |
| `an004-img-002.png` | 4 | 441×453 | **Figure 2** | Line diagram | PASS (OCR good) |
| `an004-img-003.png` | 5 | 801×545 | **Figure 3** | Line diagram | PASS (OCR good) |
| `an004-img-004.png` | 6 | 600×409 | **Figure 4** | VGA screenshot | PASS (blue-dominant = Atari theme) |
| `an004-img-005.png` | 8 | 518×326 | **Figure 5** | VGA screenshot | PASS |
| `an004-img-006.png` | 12 | 655×285 | **Figure 6** | VGA screenshot | PASS |
| `an004-img-007.png` | 13 | 300×164 | **Figure 7** thumb 1 | VGA screenshot | PASS |
| `an004-img-008.png` | 13 | 300×157 | **Figure 7** thumb 2 | VGA screenshot | PASS |
| `an004-img-009.png` | 13 | 300×164 | **Figure 7** thumb 3 | VGA screenshot | PASS |
| `an004-img-010.png` | 13 | 300×157 | **Figure 7** thumb 4 | VGA screenshot | PASS |
| `an004-img-011.png` | 13 | 300×165 | **Figure 7** thumb 5 | VGA screenshot | PASS |
| `an004-img-012.png` | 13 | 300×164 | **Figure 7** thumb 6 | VGA screenshot | PASS |
| `an004-img-013.png` | 13 | 300×164 | **Figure 7** thumb 7 | VGA screenshot | PASS |
| `an004-img-014.png` | 13 | 300×170 | **Figure 7** thumb 8 | VGA screenshot | PASS |
| `an004-img-015.png` | 13 | 300×164 | **Figure 7** thumb 9 | VGA screenshot | PASS |

## Figure descriptions (caption from PDF + extracted/OCR content)

- **Figure 1 — "Details of a 800x600 Pixel VGA Screen with 8x12 Character Font"** (imgs
  000+001, two layers). Diagram illustrating the 100×50 character grid, the 8×12 font cell,
  and the `ScreenPtr`/`ColorPtr`/`CursorPtr` buffer mechanics described in §2.

- **Figure 2 — "Components of a VGA Application"** (img 002). Component stack. **OCR:**
  `Top Level VGA Application` → `mouse_011.spin`, `keyboard_011.spin` (siblings at top) and
  `VGA Terminal Services Driver / WMF_Terminal_Services_010.spin` → `VGA Text Mode Driver /
  VGA_HiRes_Text_010.spin`. Confirms the build graph in code-catalog (terminal driver
  *contains* the VGA driver; mouse/keyboard are instantiated at the top level).

- **Figure 3 — "Legal Calls from Parent to Child Objects"** (img 003). Spin1 object call-graph
  rules. **OCR:** `Parent Object "A"` instantiates "B" and "C"; "B" instantiates "D";
  *Illegal Call!* — `"D" is a child of "B", but not of "A"; "B" and "C" are siblings of "A"
  so they can't directly communicate.` Confirms §4 prose.

- **Figure 4 — "The 'Hello World' Output on VGA at 800x600 in 100x50 Character Mode"**
  (img 004). Photo/screenshot of the Hello-World demo (white-on-blue Atari/C64 theme — blue
  dominant palette confirms).

- **Figure 5 — "'Guess My Number?' Demo on VGA at 800x600 in 100x50 Character Mode"**
  (img 005). Screenshot of the text-input demo.

- **Figure 6 — "'Color Theme Demo' Demo on VGA at 800x600 in 100x50 Character Mode"**
  (img 006). Screenshot of the color-theme demo.

- **Figure 7 — "Screen Shots of the Pre-defined Color Themes in the Terminal Services
  Driver"** (imgs 007–015, nine thumbnails). The nine `CTHEME_*` schemes, in PDF caption
  order: `CTHEME_WHITENBLACK`, `CTHEME_BLACKNWHITE`, `CTHEME_ATARI_C64`, `CTHEME_APPLE2`,
  `CTHEME_WASP`, `CTHEME_AUTUMN`, `CTHEME_CREAMSICLE`, `CTHEME_ORCHID`, `CTHEME_GREMLIN`.

## Notes

- No OCR-rescue needed for screenshots (they are photographic VGA captures, cataloged by
  caption + theme name, not by text extraction).
- Figure 1 arrives as two stacked images (a base raster + an index/mask layer) — both kept;
  together they compose the single published figure.
