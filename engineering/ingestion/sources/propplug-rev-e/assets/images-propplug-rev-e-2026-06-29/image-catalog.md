# Image Catalog — Prop Plug Rev E (#32201)

**Source:** `32201-PropPlugRev-Guide-RevE.pdf` (4 pp.) · extracted 2026-06-29 (`pdftoppm -r 200`).
**Method:** the two fact-bearing figures are full-page renders (the guide embeds them as vector
artwork, not as discrete raster media); read visually for the catalog.

| File | Page | Purpose | Content read from figure |
|------|------|---------|--------------------------|
| `page-3.png` | 3 | **Interface to Propeller Chip** wiring schematic (the load-bearing pinout) | Prop Plug 4-pin header silk **RX / TX / RES / VSS**. Connections: PropPlug **RX** ◄ ← Propeller **TX (P30)**; PropPlug **TX** ► → Propeller **RX (P31)**; **RES** → Propeller **RESn**; **VSS** → **GND**. Target shown = Propeller 1 DIP-40 with boot EEPROM (P28/SCL, P29/SDA, 10K pull-up to 3.3 V) + crystal (XI/XO); 100 nF + 10 µF decoupling. |
| `page-2.png` | 2 | Customer Reset Option photo + Specifications | Illustrates the DTR/RTS/none reset option pad and white silk marking area (text captured in the curated reference). |

**Quality:** both renders clean (discrete figures, not black/failed captures). No OCR debt —
labels read directly. Mechanical dimension drawing (page 4) carries only the "~1.3″ (33 mm)
with connectors" figure already captured in Specifications; not separately rendered.
