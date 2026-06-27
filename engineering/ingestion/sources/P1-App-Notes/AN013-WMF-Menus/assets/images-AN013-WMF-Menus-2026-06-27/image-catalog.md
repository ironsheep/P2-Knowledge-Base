# AN013 WMF Menus — Image Catalog

**Source:** AN013 v1.0 (49 pp). **Extraction:** PyMuPDF raster extraction (PDF-only ladder,
pass 3), 2026-06-27. **Quality gate:** PIL dominant-color + dimension check — all 26 healthy
(no `#000000` black-failure capture; no full-page mis-capture). **OCR:** screenshots are
legible 800×600 VGA captures; key labels read directly (no separate OCR pass required).

26 raster fragments correspond to the document's **17 numbered figures** — several figures
were stored as 2–4 horizontal image slices (the PDF split wide diagrams/photos). Fragment
groups are noted below.

| Figure | File(s) | px (each) | Page | Type | Content |
|--------|---------|-----------|-----:|------|---------|
| Fig 1 | `p02_img01`,`p02_img02` | 897×287 | 2 | diagram | 800×600 VGA text-screen layout, 8×12 char font ⇒ 100×50 chars |
| Fig 2 | `p03_img01`,`p03_img02` | 898×244 | 3 | diagram | Software object-model relationship (User_App → WMF_Framework → VGA/Mouse/Keyboard) |
| Fig 3 | `p04_img01`,`p04_img02`,`p04_img03` | 847×~255 | 4 | diagram | Data-flow model of the WMF event-driven system (controls → queue → handlers) |
| Fig 4 | `p06_img01` | 1200×654 | 6 | screenshot | Multi-control demo overview (blue theme) — various controls + static elements |
| Fig 5 | `p08_img01` | 488×312 | 8 | diagram | Anatomy of a Button (6 fields: type/attr/x,y/state/id/label) |
| Fig 6 | `p11_img01` | 1200×667 | 11 | screenshot | Result of button1/2/3 declarations: RED/GREEN/YELLOW, plain/border/border+shadow (orange theme) |
| Fig 7 | `p12_img01` | 1253×367 | 12 | diagram | Details of a HotBar (horizontal menu items / hot buttons) |
| Fig 8 | `p16_img01` | 1200×678 | 16 | screenshot | HotBar menu demo result (gray theme) — 4 hotbar variants |
| Fig 9 | `p17_img01` | 743×398 | 17 | diagram | Details of a HotList (vertical menu items, padded to width) |
| Fig 10 | `p20_img01` | 1178×539 | 20 | screenshot | HotList menu demo result (blue theme) — 3 hotlist variants |
| Fig 11 | `p25_img01` | 600×408 | 25 | screenshot | TemplateDemo in action (orange) — 1 string + 1 "Push Me" button + message printout |
| Fig 12 | `p31_img01` | 1200×667 | 31 | screenshot | ButtonDemo running (orange) — 3 buttons + pPhone keypad matrix |
| Fig 13 | `p34_img01` | 1200×678 | 34 | screenshot | HotBarMenuDemo running (gray) — 4 corner hotbars + Message/Input boxes |
| Fig 14 | `p36_img01` | 1200×663 | 36 | screenshot | HotListMenuDemo running (blue) — 3 hotlists |
| Fig 15 | `p37_img01` | 1200×654 | 37 | screenshot | MultiControlDemo running (blue) — LED Control Panel hotbar, Motor Speed Control hotlist, pPhone keypad, LCD Display + message log |
| Fig 16 | `p38_img01`,`p38_img02`,`p38_img03` | 600×132 | 38 | **photo** | Propeller Demo Board hardware setup: VGA connector (blue), transistor/resistor driver circuit, 4 LEDs, DC motor |
| Fig 17 | `p44_img01`–`p44_img04` | 782×202 | 44 | diagram | GUI + event-handling model for Example 4 (User Application ↔ ProcessGUI ↔ ProcessMenus/ProcessButtons; message routing to handlers) |

## Notes

- **Diagrams (Figs 1–3, 5, 7, 9, 17)** are the highest-value reuse assets — they teach the
  WMF architecture and the data-driven control/event model independent of P1 silicon.
- **Screenshots (Figs 4, 6, 8, 10–15)** are 800×600 VGA captures of the running demos; the
  text-mode GUI (box-drawing chars, color themes Autumn/blue/gray) is legible at this res.
- **Fig 16** is the only photograph (real hardware: motor + LEDs + driver transistor).
- Figure fragments were stored as horizontal slices in the PDF; reassembly (vertical concat
  of each group) is deferred image-enhancement debt — not required for cataloging/findability.
