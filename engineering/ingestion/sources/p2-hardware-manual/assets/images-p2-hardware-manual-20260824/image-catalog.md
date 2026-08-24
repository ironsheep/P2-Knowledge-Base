# P2 Hardware Manual (2022/11/01) — Image / Visual Catalog

Pass 3 of the `ingest-source` 7-pass ingestion. **This catalog did not exist before 2026-08-24**;
the dashboard row carried `no images` and the source had no `assets/` tree at all.

## Provenance

Extracted losslessly from `word/media/` inside
`Propeller 2 Hardware Manual - 20221101.docx` — the original embedded assets, not a
re-render. Each file is placed in **document order** (`fig-NN`) by walking `word/document.xml`
and resolving each `a:blip/@r:embed` through `word/_rels/document.xml.rels`, so `fig-NN`
numbering follows the reader's order rather than the DOCX's internal `imageNN` numbering
(which is arbitrary and differs between exports of the same document).

**Media accounting — all 39 files in the DOCX are accounted for:**

| | Count |
|---|---:|
| `word/media/*` in the DOCX | 39 |
| placed as body figures (`fig-01`..`fig-37`) | 37 |
| referenced only from `word/_rels/header1.xml.rels` (page-header branding, not content) | 2 |

## Quality gate — and a correction to how it must be read here

The methodology's gate treats a `#000000`-dominant reading as the signature of a **failed**
extraction. **That test inverts on this source and must not be applied naively:**
**34 of 37 figures are RGBA PNGs with a transparent background**, and
`image_dominant_colors` reports the transparent pixels as `#000000` — `fig-34` reads
`#000000` at **91.4%** while being a perfectly clean line drawing (verified by rendering it).

So the gate was run as: PNG colour-type from the file header (is there an alpha channel?),
plus dimensions (is this a discrete figure or a full-page mis-capture?), plus rendering the
image and looking at it. **No figure in this set is a black frame or a full-page capture.**

| Colour type | Count |
|---|---:|
| RGBA (alpha — `#000000`-dominant reading is an artifact) | 34 |
| RGB | 1 |
| palette PNG | 1 |
| GIF | 1 |

## OCR confidence — read this before citing anything below

OCR on this set splits sharply, and the split is worth recording because it decides what may
be cited:

- **Prose labels read reliably** (0.90–0.97 confidence) — every schematic *title* below is
  trustworthy.
- **Binary literals do NOT.** The mode prefixes are misread systematically: leading `0`
  becomes `8` or `4`, trailing `0` becomes `@` (`%00110` → `%80110`, `%01000` → `%8100@`,
  `%01010` → `%48101@`). **The raw OCR string is recorded verbatim below and marked
  OCR-RISK; the authoritative M[12:0] patterns are Table 18 of the text extract, not these.**
- **Rotated pin labels (fig-01) return noise** and are recorded as un-recovered.

## The catalog

### I/O pin equivalent schematics (fig-10 .. fig-33)

24 figures, one per unique I/O pin configuration, under the heading
*Equivalent Schematics for Each Unique I/O Pin Configuration*. **The section is entirely
figures — it has no body text at all**, so everything these carry exists only as an image.

Every one of the 24 repeats the same **H/L → DRIVE** legend, read off `fig-10` visually:

| H/L code | DRIVE |
|---|---|
| `000` | Digital |
| `001` | 1.5k |
| `010` | 15k |
| `011` | 150k |
| `100` | 1mA |
| `101` | 100uA |
| `110` | 10uA |
| `111` | Float |

`fig-10` also shows the DRIVE block's inputs wired as **`H2 H1 H0` from `M5 M4 M3`** and
**`L2 L1 L0` from `M2 M1 M0`**, with `M6` feeding the OUT-side XOR and `M7` the IN-side XOR.
That places the drive field at **M[5:3] (high) and M[2:0] (low)** — M6 and M7 are the
invert bits, not drive bits. This agrees with Table 18's `CIOHHHLLL` layout in the text extract.

| Figure | Title (OCR, high confidence) | Mode prefix as OCR'd — **OCR-RISK, see Table 18** |
|---|---|---|
| `fig-10.png` | Logic | `%00000MMMMMMMM` |
| `fig-11.png` | Logic, Clocked | `%00001MMMMMMMM` |
| `fig-12.png` | Logic with Feedback | `%00018MMMMMMMM` |
| `fig-13.png` | Logic with Feedback, Clocked | `%00011MMMMMMMM` |
| `fig-14.png` | Logic with Adjacent-Pin Feedback | `%0010@MMMMMMMM` |
| `fig-15.png` | Logic with Adjacent-Pin Feedback, Clocked | `%00101MMMMMMMM` |
| `fig-16.png` | Schmitt | `%80110MMMMMMMM` |
| `fig-17.png` | Schmitt, Clocked | `%80111MMMMMMMM` |
| `fig-18.png` | Schmitt with Feedback | `%8100@MMMMMMMM` |
| `fig-19.png` | Schmitt with Feedback, Clocked | `%81001MMMMMMMM` |
| `fig-20.png` | Schmitt with Adjacent-Pin Feedback | `%48101@MMMMMMMM` |
| `fig-21.png` | Schmitt with Adjacent-Pin Feedback, Clocked | _not read_ |
| `fig-22.png` | Comparator | _not read_ |
| `fig-23.png` | Comparator, Clocked | _not read_ |
| `fig-24.png` | Comparator with Feedback | _not read_ |
| `fig-25.png` | Comparator with Feedback, Clocked | _not read_ |
| `fig-26.png` | ADC with Optional Drive | `%1@@MMMMMMMMMM_` |
| `fig-27.png` | DAC with Optional ADC | _not read_ |
| `fig-28.png` | Level Comparator with 1.5k Output | `%110@@MMMMMMMM` |
| `fig-29.png` | Level Comparator with 1.5k Output, Clocked | _not read_ |
| `fig-30.png` | Level Comparator with Local Feedback | _not read_ |
| `fig-31.png` | Level Comparator with Local Feedback, Clocked | _not read_ |
| `fig-32.png` | Level Comparator with Separate Feedback | _not read_ |
| `fig-33.png` | Level Comparator with Separate Feedback, Clocked | _not read_ |

### I/O pin timing diagrams (fig-34 .. fig-36)

**Directly relevant to the constant-fidelity sprint.** All three express delay in
**clock cycles**, matching the body text (*"three additional clocks"*, *"two clocks"*).
**None of them carries a nanosecond value.**

- **`fig-34.png`** — DRVH #0 timing: clocks 0..6; `DIRA:`/`OUTA:` rows show `reg`,`reg`,`reg` then `P0 OE` / `P0 HIGH` at clock 5. NO nanosecond values — the axis is CLOCK CYCLES.
- **`fig-35.png`** — TESTB INx-read timing: clocks 0..6, `Clock:` / `Instruction:` rows. NO nanosecond values.
- **`fig-36.png`** — TESTP/TESTPN pin-read timing: clocks 0..6. NO nanosecond values.

### Other figures

| Figure | Section | Content | OCR quality |
|---|---|---|---|
| `fig-01.png` | Part Number Legend | TQFP-100 pinout drawing, part marking `P2X8C4M64P`; pin labels around all four edges (P0..P63, VDD, GND, RESn, TEST, XI, XO, Vxxyy). | LOW — pin labels are rotated 90 degrees on two edges and OCR returns noise (`iooadonowuonrnwvdonovaunanadagrTr`). Only `P2X8C4M64P`, `P46` and a few edge labels read. Pin-number order is NOT recovered; treat this figure as un-OCR'd and read the image when a pin map is needed. |
| `fig-02.png` | Hardware Connections | Photo: P2 Edge Module (#P2-EC) and P2 Mini Breakout Board (#64019). | n/a — photograph, no text content to recover. |
| `fig-03.png` | Cog Memory | Cog memory map diagram (Register RAM / Lookup RAM address ranges). | not OCR'd — see the Cog Memory tables in the text extract. |
| `fig-04.png` | Isolated Instruction Processing | Instruction pipeline stage diagram: clocks 1..6 across `Fetch 1 | Fetch 2 | Fetch 3 | Execute | Store`, with per-stage actions (Read RAM D, Latch D, Read RAM S, Latch S, ALU, Mux, Latch I). | GOOD for stage names and clock numbers; the inner action labels read partially (`Read RAMS`, `Latch`, `ALU`, `Mux`). |
| `fig-05.png` | Instruction Pipeline Flow | Instruction pipeline flow diagram. | not OCR'd — waveform/flow art. |
| `fig-06.png` | Pipeline Stall | Pipeline stall (wait) timing diagram. | not OCR'd — waveform art. |
| `fig-07.png` | Pipeline Flush | Pipeline flush (branch) timing diagram. | not OCR'd — waveform art. |
| `fig-08.gif` | HUB | Hub / cog slot rotation animation (GIF). | n/a — animated GIF, first frame only. |
| `fig-09.png` | I/O Pin Circuit | I/O pin block symbol: inputs M12..M0, DIR, OUT, IN, CLK; VIO from `Vxxyy`, GND; outputs to PIN and ADJACENT PIN. Captioned `P0..P63 (64 Instances)`. | READ VISUALLY and confirmed — this is the figure that names the 13 mode bits as M12..M0. |
| `fig-37.png` | ADC Scope With Trigger (%11010) | ADC scope filter responses: `28-tap Hann`, `45-tap Tukey`, `68-tap Tukey`. | GOOD — all three labels read at >0.91 confidence. |

## Figure inventory (all 37)

| File | Order | Section | Pixels | Colour type | Bytes | DOCX media | md5 |
|---|---:|---|---|---|---:|---|---|
| `fig-01.png` | 1 | Part Number Legend | 1648x1652 | RGB | 360910 | `image39.png` | `aab9bdf38682` |
| `fig-02.png` | 2 | Hardware Connections | 864x614 | RGBA | 451893 | `image12.png` | `47ce454ce0ab` |
| `fig-03.png` | 3 | Cog Memory | 2048x1254 | RGBA | 391352 | `image30.png` | `61fce0433cad` |
| `fig-04.png` | 4 | Isolated Instruction Processing | 929x210 | RGBA | 20684 | `image25.png` | `33c2e539e268` |
| `fig-05.png` | 5 | Instruction Pipeline Flow | 971x549 | RGBA | 73576 | `image26.png` | `998946a6dbeb` |
| `fig-06.png` | 6 | Pipeline Stall | 970x420 | RGBA | 58051 | `image10.png` | `9c4504381352` |
| `fig-07.png` | 7 | Pipeline Flush | 972x606 | RGBA | 93943 | `image13.png` | `409069bdf420` |
| `fig-08.gif` | 8 | HUB | 400x500 | GIF | 172585 | `image31.gif` | `315ce1177ed8` |
| `fig-09.png` | 9 | I/O Pin Circuit | 1063x1710 | RGBA | 84226 | `image24.png` | `a8b637393420` |
| `fig-10.png` | 10 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x582 | RGBA | 113323 | `image2.png` | `e7aabbc35bb3` |
| `fig-11.png` | 11 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x646 | RGBA | 102908 | `image5.png` | `e54093ed15ac` |
| `fig-12.png` | 12 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x676 | RGBA | 100354 | `image32.png` | `dc1cb0645bc4` |
| `fig-13.png` | 13 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x678 | RGBA | 110394 | `image37.png` | `a76640c0345b` |
| `fig-14.png` | 14 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x678 | RGBA | 110847 | `image6.png` | `62239d5dbfb1` |
| `fig-15.png` | 15 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x676 | RGBA | 120372 | `image19.png` | `ebddba44289e` |
| `fig-16.png` | 16 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x582 | RGBA | 86597 | `image33.png` | `d213eeb0875a` |
| `fig-17.png` | 17 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x646 | RGBA | 99164 | `image4.png` | `1e4a92f9c6de` |
| `fig-18.png` | 18 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x678 | RGBA | 98408 | `image1.png` | `d8e8567020d9` |
| `fig-19.png` | 19 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x676 | RGBA | 108886 | `image27.png` | `01ff3997dcad` |
| `fig-20.png` | 20 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x676 | RGBA | 108582 | `image15.png` | `f761d08c6637` |
| `fig-21.png` | 21 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x678 | RGBA | 117357 | `image36.png` | `ee91c14bafd7` |
| `fig-22.png` | 22 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x710 | RGBA | 104489 | `image38.png` | `13ba7ad6553f` |
| `fig-23.png` | 23 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x706 | RGBA | 113906 | `image14.png` | `8b007933992f` |
| `fig-24.png` | 24 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x740 | RGBA | 113114 | `image18.png` | `01e9fb71e162` |
| `fig-25.png` | 25 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x737 | RGBA | 121344 | `image21.png` | `0f99bb1e35a1` |
| `fig-26.png` | 26 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x645 | RGBA | 122461 | `image34.png` | `865663d82016` |
| `fig-27.png` | 27 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x549 | RGBA | 106592 | `image16.png` | `a2c69827af3a` |
| `fig-28.png` | 28 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x773 | RGBA | 102072 | `image8.png` | `ef9ffc9d1bc1` |
| `fig-29.png` | 29 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x773 | RGBA | 111013 | `image20.png` | `2d2949f2616b` |
| `fig-30.png` | 30 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x773 | RGBA | 105263 | `image29.png` | `6bb2541f9f71` |
| `fig-31.png` | 31 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x773 | RGBA | 111295 | `image17.png` | `ecaed3e77084` |
| `fig-32.png` | 32 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x773 | RGBA | 120387 | `image23.png` | `56cddf46b340` |
| `fig-33.png` | 33 | Equivalent Schematics for Each Unique I/O Pin Configuration | 2048x773 | RGBA | 126319 | `image22.png` | `13fafd83dde0` |
| `fig-34.png` | 34 | I/O Pin Timing | 819x252 | RGBA | 20169 | `image7.png` | `c47b2f753d5c` |
| `fig-35.png` | 35 | I/O Pin Timing | 816x202 | RGBA | 14130 | `image11.png` | `cc5038fbcb23` |
| `fig-36.png` | 36 | I/O Pin Timing | 817x204 | RGBA | 12852 | `image9.png` | `9d2a2216e38e` |
| `fig-37.png` | 37 | ADC Scope With Trigger (%11010) | 760x211 | palette | 5667 | `image3.png` | `6adeb9911b15` |

## Image-enhancement debt

- **`fig-01` (TQFP-100 pinout)** — pin labels are rotated on two edges; OCR returns noise and
  the pin-number *order* is not recovered. Anyone needing the pin map must read the rendered
  image. Same class as the Titus waveform-label debt.
- **Mode prefixes on `fig-21`..`fig-33`** — not read; Table 18 carries them authoritatively,
  so this is debt only if someone wants the figure to be self-describing.
- **`fig-05`..`fig-08`** — pipeline/hub flow art, not OCR'd; the body text describes them.

