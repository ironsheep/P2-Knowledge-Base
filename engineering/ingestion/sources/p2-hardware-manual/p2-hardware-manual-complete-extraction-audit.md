# P2 Hardware Manual — Complete Extraction Audit (audit of record)

**Source:** *Propeller 2 (P2X8C4M64P) Hardware Manual*, Parallax Inc., **2022/11/01**
**Ingestion:** DOCX-primary, 7-pass `ingest-source`, **2026-08-24**
**Supersedes:** the 2025-08-15 audit of the same name (prior text preserved in git and in
`.backups/`). It is replaced rather than amended because its headline numbers were not
measurements of anything in this repository — see *§0 What the prior audit claimed*.

---

## 0. What the prior audit claimed, and why it is replaced

The 2025-08-15 audit reported **"Extraction Complete ✅ 100%"**, **"Tables Preserved ✅ 100%"** and
**"Overall Extraction Health: 100%"**, and the dashboard row read **~65%**.

**No extracted text existed in the repository.** The source folder held four markdown
*analysis summaries* (6–7 KB each) describing what the document contains. There was no raw text
artifact, no table extract, no code catalog, and no image catalog — nothing a later task could read
a number out of. The three figures the prior audit quoted (3,026 paragraphs / 53 tables /
2,144 sections) came from a 2025 extraction run whose **output was never committed**.

This is the failure mode the sprint exists to catch, in its second form: not a mangled extraction
(F-250), but a **status line with no artifact underneath it**. Both read identically from the
dashboard.

*One prior number is confirmed:* **53 tables**. The other two are not reproducible from anything
here and are not carried forward.

---

## 1. Which DOCX is canonical — determined, not assumed

Two files bear the same name and edition, and the ingestion dashboard's scheduled-work row called
the second "an older export … reconcile which is canonical at ingestion."

| | `sources/p2-hardware-manual/` | `external-inputs/p2/` |
|---|---|---|
| bytes | **6,751,607** | **6,697,923** |
| md5 | `00ff14d35b3cfad2f0bf7bba1573d2ee` | `0773c0e31c3f04f3485cf6a0b638083d` |
| zip entry timestamps | 2026-06-22 | 2025-08-14 |

**Verdict: they are the SAME EDITION exported twice. The content is identical.**

Evidence — every one of these was measured, not inferred:

| Test | Result |
|---|---|
| Full document text, whitespace-exact, including the TOC/`w:sdt` content | **byte-identical**: 148,053 chars, **0 diff lines** |
| Digits in that text | **5,209 in both** |
| `w:p` / `w:tbl` / `w:tr` / `w:tc` / drawings | **3,198 / 53 / 280 / 907 / 37 — identical** |
| Embedded media | **39 files in both; the md5 SETS are identical** — only the `imageNN` numbering differs |
| Tracked changes (`w:ins` / `w:del`) | **10 / 3 in both**, same authors, same ids, same timestamps (latest: Bill Gertz, 2024-12-30) |
| Printed footer date | `2022/11/01` in both |

The 53,684-byte size difference is **export mechanics only**: the `sources/` copy carries
`w:embedTrueTypeFonts` plus 458 `w:bCs` / 68 `w:iCs` complex-script attributes the other lacks, and
the two embed different font subsets. No content bit differs.

**Canonical: `engineering/ingestion/sources/p2-hardware-manual/Propeller 2 Hardware Manual - 20221101.docx`** —
it is the copy in the canonical source folder and the later export. Because the content is identical
the choice carries no fidelity consequence, which is itself the finding.

**Two corrections to the record follow, and both are the "status line is not evidence" failure:**

1. The dashboard's *"`external-inputs/p2/` holds an older export"* is **wrong as stated**. It is an
   *earlier export* (2025-08-14) of the **same** content, not an older edition. Nothing was gained
   by preferring one, and nothing would have been lost by preferring the other.
2. The tasking recorded the `external-inputs/p2/` copy as **6,993,299 bytes**. It is
   **6,697,923**. 6,993,299 is the size of `Parallax Spin2 Documentation v51.docx`, which sits in
   the same directory. A sighting was transposed between neighbouring rows.

---

## 2. Pass 1 — content

| Metric | Value |
|---|---|
| Artifact | `p2-hardware-manual-text.txt` (159,098 chars, 1,908 lines) |
| Tables | **53** — 49 top-level + **4 nested inside another table's cell** |
| Table artifact | `complete-tables-reference.md` (all 53, rendered as markdown) |
| Paragraphs walked | **3,198 of 3,198** |
| Headings | 12 H1 · 38 H2 · 70 H3 · 17 H4 · 4 H6 |
| Figure references in text | 37 |

**Losslessness is proven, not asserted.** Every paragraph's text was re-extracted from
`word/document.xml` independently and searched for verbatim in the output:
**2,659 paragraph segments checked, 0 missing.** The table artifact was checked the same way
against table-cell content only: **1,670 cell segments, 0 missing.**

**The four nested tables are why that check earns its place.** A straightforward DOCX walk emits
tables at body level and renders a cell's contents as text, which silently drops a table nested
*inside a cell*. The first extraction here did exactly that, and the containment check caught it as
21 missing segments. What was being dropped was **the pin drive-strength ladder**
(`000 Fast · 001 1.5 kΩ · 010 15 kΩ · 011 150 kΩ · 100 1 mA · 101 100 µA · 110 10 µA · 111 Float`)
and the pin-mode legend — the single most sprint-relevant table in the document. The extractor was
fixed to emit nested tables inline; the check now reports 0.

### Digit-density gate (`ingest-source` §2a) — MANDATORY, run, and passed

```
python3 engineering/tools/validation/audit-extraction-digit-density.py \
        engineering/ingestion/sources/p2-hardware-manual
```

| Artifact | Substantive lines | Lines with a digit | Density |
|---|---:|---:|---:|
| `p2-hardware-manual-text.txt` | 1,402 | 1,060 | **75.6%** |
| `complete-tables-reference.md` | 363 | 258 | **71.1%** |

**Exit 0**, floor 20%. **Carrying the tool's own caveat, unparaphrased:** *"NOT a completeness
certificate — this catches TOTAL numeral loss only, never partial."* It is a smoke alarm. It says
the numbers are not all gone; it does not say they are all right, and it says nothing about any
other source.

For scale: the corpus sweep that established the floor measured `p2-hardware-manual` at **29%** —
that figure was taken on the thin 2025 summary artifacts, which is the only text that existed.

### Completeness check — the document's own table of contents

The manual carries a 117-entry TOC. Every entry was matched against the extracted heading set:
**117 of 117 present. 0 unmatched.** This is a real check on section coverage because the TOC is
the document's own claim about what it contains.

---

## 3. Pass 2 — code examples

Catalog: `assets/code-20260824/CODE-EXTRACTION.md`. Compiler: **`pnut-ts v1.55.3`**.

**This document contains no complete programs** — its code is inline illustrative fragments. Code is
marked out by **font, not by style name**: the `Title` paragraph style resolves to
`Roboto Mono Medium` in `word/styles.xml`, and reading style names alone misses ~128 code
paragraphs. Because monospace is also used for whole prose paragraphs here, each monospace line was
then classified against the 358-mnemonic PASM2 set.

| Class | Blocks | Disposition |
|---|---:|---|
| `code` — compiles in the harness | **24** | staged as `blkNNN.spin2` |
| `code` — does not compile | **2** | source errata → `KNOWLEDGE-GAPS.md` G-016, G-017 |
| `illustrative-fragment` | 1 | deliberately incomplete (bare `WRPIN`) |
| `syntax-notation` | 14 | `D/#,S/#` / `{WC}` templates — not code |
| `bitfield-template` | 1 | binary literal with letter placeholders |
| `prose-in-monospace` | 9 | dropped per §2 "validate, then filter" |
| **Total monospace blocks** | **51** | |

**24 of 24 staged fragments compile from their committed location** (re-verified after staging, not
inherited from the run that produced them).

**`pnut-ts -d`:** the `-d` path is wired but **was never exercised — no fragment in this document
contains `debug()`.** Recorded as a fact about the source, not as a step performed.

**Both non-compiling blocks were confirmed verbatim in `word/document.xml` before being called
errata**, and neither appears anywhere in `deliverables/ai/P2/`:

- `COGATN #00001100` — decimal 1,100, outside the 0..511 immediate range; the comment
  ("cogs 2 and 3") requires `%00001100`. A `%` is missing.
- `ROLBYTE y,x` ×4 — a 2-operand form that does not exist; only `ROLBYTE D,{#}S,#N` and the
  `ALTGB`-alias `ROLBYTE D` do. Intended form `ROLBYTE y,x,#0`.

**A note on method, because it nearly produced two false findings.** The first validation run
reported 20 failures. Most were defects in the harness, not the document: undefined-symbol
collection missed mixed-case operands; `#adcpin` was being eaten by a hex-literal regex (`adc` are
hex digits); `X` and `x` were declared twice because PASM2 symbols are case-insensitive; and a
block carrying its own `DAT ORG` was double-wrapped. **A compiler's FAIL is a claim about the
harness as much as about the source.** Only after those were fixed did the residue — 2 real errata
— stand up.

---

## 4. Pass 3 — images / visual catalog

Catalog: `assets/images-p2-hardware-manual-20260824/image-catalog.md`.
**This catalog did not exist before this run** — the dashboard row read `no images` and the source
had no `assets/` tree at all.

| | Count |
|---|---:|
| `word/media/*` in the DOCX | **39** |
| Placed as body figures, in document order (`fig-01`..`fig-37`) | **37** |
| Page-header branding (referenced only from `header1.xml.rels`) | 2 |

Figures are numbered in **reading order** by walking `word/document.xml` and resolving each
`a:blip/@r:embed` through the relationship map — deliberately not by the DOCX's internal `imageNN`
numbering, which §1 shows is arbitrary and differs between exports of the same document.

**The quality gate had to be re-derived for this source, and that is a methodology finding.**
The standing gate treats a `#000000`-dominant reading as the signature of a failed extraction.
**34 of the 37 figures are RGBA PNGs with a transparent background**, and `image_dominant_colors`
reports transparent pixels as black: `fig-34` reads `#000000` at **91.4%** while being a clean line
drawing. Applied naively the gate would have condemned the whole set. The gate was run instead as
PNG colour-type from the file header + dimensions + **rendering the image and looking at it**.
**No figure is a black frame or a full-page mis-capture.**

**OCR splits sharply, and the split decides what may be cited.** Prose labels read at 0.90–0.97
confidence — all 24 schematic titles are trustworthy. **Binary literals do not**: leading `0` reads
as `8`/`4`, trailing `0` as `@` (`%00110`→`%80110`, `%01000`→`%8100@`). The raw OCR strings are
recorded verbatim and flagged OCR-RISK in the catalog; **the authoritative M[12:0] patterns are
Table 18 of the text extract, never the OCR.**

**What the figures carry that exists nowhere else in the document:**

- **`fig-10`..`fig-33` (24 figures)** — the *Equivalent Schematics for Each Unique I/O Pin
  Configuration* section **has no body text at all**; it is entirely figures. Each repeats the
  H/L→DRIVE legend, and `fig-10` shows the DRIVE block wired **`H2 H1 H0` ← `M5 M4 M3`** and
  **`L2 L1 L0` ← `M2 M1 M0`**, with `M6`/`M7` as the OUT/IN invert bits. That independently places
  the drive field at **M[5:3] and M[2:0]** and agrees with Table 18's `CIOHHHLLL` layout.
- **`fig-34`..`fig-36`** — the three I/O pin timing diagrams, clock-numbered `0..6`.
  **None carries a nanosecond value.** Directly load-bearing for F-329.
- **`fig-01`** — TQFP-100 pinout. Rotated pin labels return OCR noise; **pin order is not
  recovered** and is logged as image-enhancement debt.

---

## 5. Passes 4–6 — cross-source corroboration and conflicts

The sprint plan §8 names this source as the **cross-check partner** for the datasheet's electrical
tables. Corroborated against `p2-datasheet` (`p2-datasheet-narrative.txt`, DC Characteristics p.47 /
AC Characteristics p.48):

| Fact | Hardware Manual | Datasheet | Verdict |
|---|---|---|---|
| Nominal system clock | `180 MHz @ 105 ℃` | *"Nominal PLL frequency … is 180 MHz at up to 105 °C"* | **exact agreement** |
| Core / I/O supply | `1.8 V Core, 3.3 V I/O`; `VDD 1.8`, `Vxxyy 3.3` | `Vdd` 1.7/1.8/1.9 V; `Vxxyy` 3.15/3.3/3.45 V | **agree** (manual states typ; datasheet adds min/max) |
| Max current per I/O | `+/- 30mA` | `Vol`/`Voh` characterised at sinking/sourcing 1 mA, 10 mA, **30 mA** | **agree** |
| Internal oscillators | `~24 MHz or ~20 kHz` | RCFAST typ 24 MHz; RCSLOW typ 20 kHz | **agree** |
| XI/XO capacitance | `%10 … 15pF per pin`, `%11 … 30pF per pin` | Mode 2 (Crystal ≥16 MHz) 15 pF; Mode 3 (Crystal <16 MHz) 30 pF | **agree — plus a vocabulary key** (see below) |
| External clock limits | crystal `10 - 20 MHz`; oscillator `0 to 180 MHz (nominal)` | Crystal 1–50 MHz; direct drive DC–200 MHz; PLL 3.33–320 MHz | **different framings** → gap **G-018** |
| I/O pin timing | **clock cycles only** (3 / 3 / 2) | **absent** — the AC table has only `Freq` and `Cin` | **neither source states ns** → **F-329** |

**A vocabulary key, not a disagreement.** The manual labels the crystal capacitance modes `%10` and
`%11`; the datasheet calls the same things "Mode 2" and "Mode 3". The values match once the
naming is aligned — the same shape as the microSD `DI/DO ≡ MOSI/MISO` resolution on «#306». It is
recorded here so a later reader does not file it as a conflict.

**Internal corroboration worth recording:** Table 18 gives DAC output impedances
`990 Ω, 3.3 V / 600 Ω, 2.0 V / 123.75 Ω, 3.3 V / 75 Ω, 2.0 V`, and the reserved-word table in the
same document lists `P_DAC_990R_3V`, `P_DAC_600R_2V`, **`P_DAC_124R_3V`**, `P_DAC_75R_2V`. So
**123.75 Ω is the precise value and `124R` is the rounded symbol name** — two independent places in
one document, which settles a naming question without needing a second source.

**This ingestion repairs several of the datasheet's structurally-lost tables.** Of the ten in
`sources/p2-datasheet/identified-broken-tables.md`, this DOCX carries clean, structured equivalents
for **#2 Pin Descriptions** (Table 4), **#3 Smart Pin Mode Configuration** — the one the datasheet
extract reduced to the bare fragment `OUT / CIOHHHLLL / DIR` (Table 18 + nested Tables 19–22),
**#6 I/O Pin Equivalent Circuit** (the 24 figures), and **#8 Clock Mode Settings**
(`HUBSET ##%0000_000E_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS` + its field tables). This is the DOCX-carries-
table-structure win the re-ingestion was queued for, and it is what converts «#297» from an
extraction fight into a corroboration.

**Routed out of this run:**

- **`P2KB-CORRECTION-FINDINGS.md` F-329** (`CONFIRMED`) — three blocks of
  `architecture/io_pin_timing.yaml` that F-327's location line does not cover, carrying two further
  copies of the fabricated mA drive ladder and ~20 ns quantities neither extraction path supports,
  plus a datasheet page citation (`pages 76-78`) that cannot exist in a **50-page** document
  (`pdfinfo`). The finding also records what must **survive** the purge:
  `instruction_to_pin_timing:` is exactly corroborated here and needs a citation, not deletion.
- **`KNOWLEDGE-GAPS.md` G-016, G-017** — the two source errata (§3), upstream-report items with
  nothing to fix in our tree.
- **`KNOWLEDGE-GAPS.md` G-018** — the external-clock framing difference.

**Prior gaps answered:** none. G-001..G-015 are Smart-Pins-detail and add-on-board questions this
document does not address; it is a hardware overview, not a smart-pin reference.

---

## 6. Completeness

**Assessed: 95%.** Stated as a measurement with its basis, and deliberately not 100%:

| Pass | State | Basis |
|---|---|---|
| 1 Content | ✅ | 3,198/3,198 paragraphs; 53/53 tables; 0 missing segments on two independent containment checks; 117/117 TOC entries; digit gate exit 0 at 75.6% |
| 2 Code | ✅ | 51 blocks classified; 24/24 compile; 2 errata identified and confirmed against the raw XML |
| 3 Images | ✅ | 39/39 media accounted for; 37 figures catalogued with OCR + quality gate |
| 4 Post-processing | ✅ | cross-source corroboration matrix (§5); datasheet broken-table repair map |
| 5 Validation | ✅ | this document |
| 6 Cross-source | ✅ | F-329 + G-016/017/018 routed |
| 7 Registration | ✅ | dashboard, `AUTHORITATIVE-SOURCES`, `DOCUMENT-LINEAGE` |

**The residual 5%, named rather than rounded away:**

- **`fig-01`'s pin map is not machine-readable.** Rotated labels defeat OCR; the TQFP-100 pin
  *order* exists only as pixels. Anyone needing it must read the image.
- **Mode-bit prefixes on `fig-21`..`fig-33`** were not read reliably; Table 18 carries them, so this
  is debt only against the figures being self-describing.
- **Five figures** (`fig-03`, `fig-05`..`fig-08`) are flow/animation art that was not OCR'd; the
  body text describes them.

**No section of this document was unrecoverable. No extraction path was exhausted without success,
so nothing here escalates under `SOURCE-REPAIR-ORDER.md` §4.**

**What this audit does NOT certify.** That every number in the document is correct, or that the KB
agrees with it. The digit gate catches total numeral loss only; the corroboration in §5 covers the
facts actually checked, not the document as a whole. Coverage of names is not coverage of meaning.
