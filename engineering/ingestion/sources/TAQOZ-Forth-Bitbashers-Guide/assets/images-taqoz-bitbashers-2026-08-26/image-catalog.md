# TAQOZ "Bit Bashers Guide" — Image / Visual Catalog

Pass 3 of the `ingest-source` 7-pass ingestion. **This catalog did not exist before 2026-09-10.**
The 25 images were extracted losslessly on 2026-08-26 and accounted for in the source's
extraction audit, but pass 3's actual deliverable — a per-figure catalog — was never written.
That gap was found by `audit-ingestion-row-artifacts.py`, which read the row's `I = ✅` and asked
the folder for the artifact behind it.

## Provenance

Extracted from `word/media/` inside
`The Bit Bashers Guide to the Parallax P2 ~  Using TAQOZ ROM Forth.docx` — the original embedded
assets, not a re-render. **25 of 25 media accounted for.** The extraction audit records document
order as preserved, so `taqoz-NNN` numbering follows the reader's order.

Media are 13 MB of the ~14 MB document: as that audit puts it, *"the document is prose-and-figures;
its size is the 25 images, not its tables."*

## Quality gate — and the reading correction it needs

The methodology treats a `#000000`-dominant reading as the signature of a failed extraction.
**That test inverts here and must not be applied naively:** 11 of the 25 are RGBA with
transparent backgrounds, and a dominant-colour probe reports transparent pixels as `#000000`.
This is the same correction the P2 Hardware Manual catalog records.

The gate was therefore run as **PNG/JPEG header colour-type + dimensions + looking at every
image** (a 5×5 contact sheet rendered at 110 dpi and read). **No image in this set is a black
frame, a blank, or a full-page mis-capture.** Every one of the 25 carries real content.

| Format / colour type | Count |
|---|---:|
| PNG RGBA (transparent — `#000000`-dominant reading is an artifact) | 11 |
| PNG RGB | 12 |
| JPEG | 2 |

## The figures

| # | File | px | What it is |
|---|---|---|---|
| 001 | `taqoz-001.png` | 300×300 | **QR code** |
| 002 | `taqoz-002.png` | 691×335 | **Screenshot** — host disk utility inspecting an SD card: *Multiple Card Reader (1.00)*, serial number, 128 GB device, partitioning *Master Boot Record*, a 17 MB volume shown as *Unallocated Space*, device `/dev/sdb` |
| 003 | `taqoz-003.png` | 154×157 | **QR code** (smaller, RGB — the only non-300×300 QR) |
| 004 | `taqoz-004.jpg` | 225×225 | **Product photo** — SanDisk Ultra PLUS 64 GB microSDXC UHS-I card |
| 005 | `taqoz-005.png` | 267×400 | **Book cover** — Leo Brodie, *Thinking Forth: A Language and Philosophy for Solving Problems* |
| 006 | `taqoz-006.png` | 300×300 | **QR code** |
| 007 | `taqoz-007.png` | 300×300 | **QR code** |
| 008 | `taqoz-008.jpg` | 2048×1536 | **Board photo** — P2D2 module, top view: P2 QFP, micro-USB, full perimeter pin field |
| 009 | `taqoz-009.png` | 1752×1314 | **Board photo** — the same P2D2 at an angle, **microSD card inserted**, cable attached |
| 010 | `taqoz-010.png` | 788×790 | **P2 architecture block diagram** — 512 KB hub RAM (16K×32×8), eight cogs with 2K RAM + 512 LUT each, CORDIC solver, Xoro128 PRNG, 32-bit systick, smart pins around the perimeter, and the **16 K ROM labelled SPI FLASH / SD BOOT / MONITOR / TAQOZ** |
| 011 | `taqoz-011.png` | 716×977 | **Book cover** — Leo Brodie, *Starting FORTH*, FORTH Inc. |
| 012 | `taqoz-012.png` | 580×513 | **Annotated board photo** — P2 EVAL board (P2X8C4M64PES Rev C silicon) with ~20 numbered callouts: LDO regulators, microSD socket, flash memory, mode-selection switch bank, LED bank, I/O breakout edge headers, USB host port, reset button, crystal, ground test post |
| 013 | `taqoz-013.png` | 1648×1652 | **Package pinout** — P2X8C4M64P, pin names on all four sides |
| 014 | `taqoz-014.png` | 300×300 | **QR code** |
| 015 | `taqoz-015.png` | 300×300 | **QR code** |
| 016 | `taqoz-016.png` | 1648×1652 | **Package pinout** — a second P2X8C4M64P pinout. Same dimensions as 013 and **not byte-identical** (352 KB vs 394 KB); which detail differs is not established here |
| 017 | `taqoz-017.png` | 2048×1373 | **Module photo** — small PCB on a gold-plated substrate with a crystal can and a right-angle pin header |
| 018 | `taqoz-018.png` | 2048×1011 | **Module photo** — HC-05/HC-06-class Bluetooth serial module, 6-pin header |
| 019 | `taqoz-019.png` | 300×300 | **QR code** |
| 020 | `taqoz-020.png` | 300×300 | **QR code** |
| 021 | `taqoz-021.png` | 300×300 | **QR code** |
| 022 | `taqoz-022.png` | 635×444 | **Schematic** — SPI flash **and** microSD wired to the boot pins, showing the series resistors and the shared-bus arrangement (33R series, plus 470/1M/220R/475 values) |
| 023 | `taqoz-023.png` | 780×61 | **Component photo** — a single long strip of pin headers |
| 024 | `taqoz-024.png` | 300×300 | **QR code** |
| 025 | `taqoz-025.png` | 1222×1680 | **Full schematic sheet** — P2X8C4M64P with surrounding support circuitry |

## What this catalog does NOT establish

- **The QR codes are not decoded.** Ten of the 25 figures (001, 003, 006, 007, 014, 015, 019, 020,
  021, 024) are QR codes, and a QR in a guide almost always encodes a **URL** — a video, a forum
  thread, a download. **Those links are invisible to the text extraction and are currently lost
  to any reader of the extracted corpus.** Decoding them needs a QR reader this container does not
  have (no PIL, no ImageMagick, no zbar). This is the single highest-value follow-up on this
  source, and it is recorded rather than quietly skipped.
- **No figure captions.** The images are described from looking at them, not from the document's
  own caption text; the extraction is body text and the two were not correlated in this pass.
- **013 vs 016.** Both are P2X8C4M64P pinouts at identical pixel dimensions and different byte
  sizes. They are recorded as two figures because the document carries two; no claim is made about
  what distinguishes them.
