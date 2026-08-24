# P2 Datasheet — Page 22 I/O Pin Timing Figures (image-gap recovery, 2026-08-24)

**Source PDF:** `engineering/ingestion/external-inputs/archive/Propeller2-P2X8C4M64P-Datasheet-20221101.pdf`
**Extraction:** `pdfimages -png -f 22 -l 22` (lossless XObject extraction), 2026-08-24.

## Why this folder exists

The 2025-09-06 catalog (`../images-20250906/`) claims *"39 successfully extracted images ·
Success rate 100% (39/39)"*. Measured against the PDF, the document carries **40 image XObjects**
across 17 pages (`pdfimages -list` reports 68 rows: 40 images + 28 soft masks). **One image was
never captured** — the first of page 22's three figures. Its absence is visible in the old
folder's own filenames, which jump from `page22_img02` to `page22_img03` with no `img01`.

That page is *I/O Pin Timing*, which is the exact subject of correction-register finding **F-329**,
so the missing figure was the one most worth having.

All three page-22 figures are captured here so the page is complete in one place. `img02` and
`img03` duplicate figures already in the 2025 folder at a different resolution (that capture used
render-and-crop at 1400 px wide; this one takes the embedded XObject at its native size). The
2025 folder is **not** modified — it is a dated capture and stays as it was.

## Images

### page22_img01 — output latency: `DRVH #0` to pin transition  ‹NEWLY RECOVERED›
**File:** `Propeller2-P2X8C4M64P-Datasheet-20221101_page22_img01.png` — 819 x 252 px
**Shows:** a clock waveform with vertical clock-edge rules; `DRVH #0` issued, then `DIRA` / `OUTA`
followed by three `reg` stages, then `P0 OE` / `P0 HIGH`.
**Context (p.22 body text, verbatim):** *"When a DIRx/OUTx bit is changed by any instruction, it
takes three additional clocks after the instruction before the pin starts transitioning to the new
state. Here this delay is demonstrated using DRVH to set I/O pin P0's output enable (OE) and drive
P0's output latch high."*

### page22_img02 — input latency via the `INx` registers
**File:** `..._page22_img02.png` — 816 x 202 px
**Shows:** `P0 IN` → three `reg` stages → `ALU` → `C/Z`, with `TESTB INA,#0` issued at the ALU stage.

### page22_img03 — input latency via `TESTP`
**File:** `..._page22_img03.png` — 817 x 204 px
**Shows:** `P0 IN` → three `reg` stages → `C/Z`, with `TESTP #0` issued one stage earlier than the
`TESTB` case — the "fresher data" the text describes.

## The measurement these figures carry

**All three diagrams are numbered in CLOCK EDGES. None of them has a time axis, and no nanosecond
quantity appears on any of them.** Read directly off the rendered images, 2026-08-24.

The body text on the same page says why, verbatim: *"Note that 'P0 OE' and 'P0 HIGH' begin their
transition on the rising edge of clock 5; however, **the duration until complete depends on clock
frequency and circuit load. The I/O pads are asynchronous (not tied strictly to the clock)** so with
a slow operating frequency, the transition may complete within 1 clock, whereas with higher
frequencies it may take multiple clocks to complete."* The datasheet is explicit that pin-transition
duration is **not** a fixed specified quantity — which is exactly why no nanosecond figure exists to
be extracted.

This is the datasheet-side half of the evidence for **F-329**: the P2 Hardware Manual's equivalent
figures (`sources/p2-hardware-manual/assets/.../fig-34..36`) were already found to be clock-numbered
with no nanosecond axis, and the datasheet's own timing figures are the same. Two independent
documents, and neither states pin timing in nanoseconds — only in clocks.
