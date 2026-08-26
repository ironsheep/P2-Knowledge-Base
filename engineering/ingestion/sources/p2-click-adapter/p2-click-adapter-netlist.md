# P2 to mikroBUS Click Adapter (#64008 Rev A) — schematic netlist

**Source**: `64008-RevA-P2-Click-Adapter-SCHEMATIC-OS.pdf` — Rev A, "Last Update: 10 Aug 2020 (MM)",
1 page A4 landscape, 59,249 bytes. Parallax Inc., Copyright 2020, **Open Source Hardware,
CC BY-SA 4.0** (license stated in the sheet's own title block).

**Extraction date**: 2026-08-26
**Extraction path**: **rendered-page visual read** — see "Why not text extraction" below.

---

## Why not text extraction

This sheet has a text layer, but it contains **the title block only** (407 characters: company
address, part number, revision, copyright, license, update date). The schematic body is **vector
art with its text converted to curves**, and the PDF holds **zero image XObjects** — so there is
no bitmap to OCR either.

Negative control, run 2026-08-26 (`pdftotext <file> - | grep -c <token>`):

| token | occurrences in text layer |
|---|---|
| `AN` `RST` `MISO` `MOSI` `SCK` `PWM` `SDA` `SCL` | **0** each |
| `J100` `J102` | **0** each |
| `mikroBUS` | 2 — *title block only* |

Every net name, signal name, and reference designator returns zero. `pdftotext`, `pdf2md`,
`pdf-layout`, and `camelot` therefore cannot recover any of the content below, and `pdf-ocr` has
no raster to work on. The netlist was read from the page rendered at 200 dpi (whole sheet) and
600 dpi (each connector), archived under `assets/render-2026-08-26/` so the read is checkable
without re-rendering.

---

## Sheet inventory

Four connectors, two logical sides, no active components on the sheet.

| Refdes | Side | Description |
|---|---|---|
| `J100` | P2 | "P2 EVAL Edge expansion socket (Dual)" — 2x6 socket, header **A** |
| `J101` | P2 | 2x6 socket, header **B** |
| `J102` | mikroBUS | MikroE mikroBUS socket, left row |
| `J103` | mikroBUS | MikroE mikroBUS socket, right row |

The adapter is **passive** — sockets and routing only. No logic, no level shifting, no
regulators, no passives shown.

---

## P2 side — two adjacent 2x6 accessory headers

Offsets are relative to `base_pin`, the first P2 I/O of header A. `X` = no connect.

### J100 — header A

| Pin | Net | Pin | Net |
|---|---|---|---|
| 1 | Vss | 2 | Vss |
| 3 | IO+0 | 4 | IO+1 |
| 5 | IO+2 | 6 | IO+3 |
| 7 | IO+4 | 8 | IO+5 |
| 9 | IO+6 | 10 | IO+7 |
| 11 | 5V_A | 12 | VIO_3V3_A |

### J101 — header B

| Pin | Net | Pin | Net |
|---|---|---|---|
| 1 | Vss | 2 | Vss |
| 3 | IO+8 | 4 | IO+9 |
| 5 | IO+10 | 6 | IO+11 |
| 7 | **X** (no connect) | 8 | **X** (no connect) |
| 9 | **X** (no connect) | 10 | **X** (no connect) |
| 11 | 5V_B | 12 | VIO_3V3_B |

**The adapter spans 16 I/O positions and uses 12.** The four `X` positions on J101 are
`IO+12`..`IO+15`. This is the mechanism behind the catalog page's *"a Click-ready socket of
12 signals (with 4 spare I/Os)"* — the two statements reconcile exactly.

**Power rail note (read strictly from the sheet):** the mikroBUS socket draws its `+3.3V` from
`VIO_3V3_A` and its `+5V` from `5V_A` — i.e. **header A's rails**. `5V_B` / `VIO_3V3_B` appear on
J101 but the sheet draws no connection from them to the mikroBUS socket. Whether the `_A` and `_B`
rails are commoned is **not shown on this sheet** and is not asserted here.

---

## mikroBUS side

Signal names as drawn on the sheet. The mikroBUS pin numbers in the right-hand column are the
**MikroElektronika standard** numbering (not printed on this sheet) and are supplied here for
cross-reference only.

### J102 — mikroBUS left row

| J102 pin | mikroBUS signal | P2 net | mikroBUS std pin |
|---|---|---|---|
| 8 | AN | **IO+6** | 1 |
| 7 | RST | **IO+7** | 2 |
| 6 | CS | **IO+8** | 3 |
| 5 | SCK | **IO+9** | 4 |
| 4 | MISO | **IO+10** | 5 |
| 3 | MOSI | **IO+11** | 6 |
| 2 | +3.3V | VIO_3V3_A | 7 |
| 1 | GND | Vss | 8 |

### J103 — mikroBUS right row

| J103 pin | mikroBUS signal | P2 net | mikroBUS std pin |
|---|---|---|---|
| 8 | PWM | **IO+5** | 16 |
| 7 | INT | **IO+4** | 15 |
| 6 | RX | **IO+3** | 14 |
| 5 | TX | **IO+2** | 13 |
| 4 | SCL | **IO+1** | 12 |
| 3 | SDA | **IO+0** | 11 |
| 2 | +5V | 5V_A | 10 |
| 1 | GND | Vss | 9 |

---

## Consolidated offset map

The twelve signal offsets, ascending:

| Offset | mikroBUS signal | Header |
|---|---|---|
| +0 | SDA | A |
| +1 | SCL | A |
| +2 | TX | A |
| +3 | RX | A |
| +4 | INT | A |
| +5 | PWM | A |
| +6 | AN | A |
| +7 | RST | A |
| +8 | CS | B |
| +9 | SCK | B |
| +10 | MISO | B |
| +11 | MOSI | B |
| +12..+15 | *(spare, no connect)* | B |

**The SPI four (CS, SCK, MISO, MOSI) all sit in header B; every other signal sits in header A.**
The sheet's own `_A` / `_B` rail suffixes are what establish that these are two distinct
accessory headers rather than one wide connector.

---

## Orientation note (drawn on the sheet, verbatim)

> Note: If this adapter is plugged into the P2-EVAL top edge,
> then P2 MISO/MOSI are aligned with the mikroBUS MISO/MOSI

Rendered on the sheet in orange, centred below the connectors.

---

## What this sheet does NOT establish

Recorded so these are not later mistaken for schematic-sourced facts:

- **TX/RX direction semantics.** The sheet gives net *names* (`TX` -> IO+2, `RX` -> IO+3). Whether
  `TX` denotes the P2's transmit or the Click module's transmit is not settled by this sheet. The
  MikroElektronika mikroBUS standard is the authority for that, and it is not held in this repo.
- **Whether `5V_B` / `VIO_3V3_B` are commoned with the `_A` rails.** Not drawn.
- **Which base pins the adapter may be plugged into.** The sheet is base-relative throughout; the
  set of legal `base_pin` values is a property of the host board, not of this adapter.
- **Any current limit, pull-up, or termination.** No passives appear on the sheet.
