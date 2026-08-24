# P2 Datasheet — Complete Extraction Audit (audit of record)

**Source:** *Parallax Propeller 2 (P2X8C4M64P) Datasheet*, Parallax Inc., **Release November 1, 2022**
**File:** `engineering/ingestion/external-inputs/archive/Propeller2-P2X8C4M64P-Datasheet-20221101.pdf`
**Ingestion:** PDF-primary, **2026-08-24** — targeted completion of the ten structurally-lost tables
identified in `identified-broken-tables.md`, plus the raw-text and table artifacts the source never had.
**Prior audit:** `datasheet-audit-report.md` (2025-08-14) — retained, corrected, and demoted to a
historical record; §0 below says why.

---

## 0. Why this audit exists, and what the prior one got wrong

`identified-broken-tables.md` (2025-09-05) listed **ten** tables whose column structure the 2025
extraction had destroyed, and it ended with an unanswered question to a human — *"Would it help if I
showed you specific line numbers…?"* — so nothing was ever recovered. Meanwhile
`datasheet-audit-report.md` scored the source **94% overall**, *"Tables preserved: 85%"*, *"Technical
accuracy: 100%"*, *"Zero contradictions found"*, and the ingestion dashboard row read **94%**.

Both statements described the same source. Both cannot be true.

**Three concrete corrections to the prior record, each measured:**

| Prior claim | Measured 2026-08-24 |
|---|---|
| *"Tables preserved: 85%"* | Ten named tables were structurally lost; no table artifact existed at all. There were **no** extracted tables in the repository to preserve — only `p2-datasheet-narrative.txt`, in which every multi-column table is linearized to one value per line. |
| *"Zero contradictions found"* / *"Cross-Referenced With: Silicon Documentation"* | A cross-check against the DOCX-derived P2 Hardware Manual found **one real conflict** — the VCO recommended-range sentence, now filed as **F-330**. It sits in a table the prior pass never extracted, which is why it could not be seen. |
| *"39 successfully extracted images · Success rate 100% (39/39)"* | The PDF carries **40** image XObjects. **One was never captured** — page 22's first I/O-pin-timing figure. The old folder's own filenames skip `page22_img01`. |

This is the sprint's recurring failure mode in its third form: not a mangled extraction (F-250), not a
status line with no artifact underneath it (`p2-hardware-manual`), but a **percentage computed over
work that was never done**. A completeness score is not a measurement unless something was measured.

---

## 1. There is no DOCX edition of this datasheet

Checked at ingestion: every `.docx` in `engineering/ingestion/` is accounted for and the datasheet is
not among them. Unlike `p2-hardware-manual`, there is **no structured-source escape hatch** — PDF
extraction is the only path, which is why this ingestion runs four independent paths and reconciles
them rather than trusting one.

**Document facts, from `pdfinfo`:**

| | |
|---|---|
| Pages | **50** |
| Page size | 612 x 792 pt (letter) |
| Producer | Skia/PDF m109 Google Docs Renderer |
| Created / Modified | 2022-11-03 21:34 / 21:43 UTC |
| Bytes | 2,822,684 |
| Text layer | present and complete — **no OCR needed or used** |

---

## 2. Pass 1 — content

| Metric | Value |
|---|---|
| Artifact | **`p2-datasheet-text.txt`** — CREATED 2026-08-24 (2,272 lines, 173,061 bytes) |
| Pages captured | **50 of 50**, each delimited `=== PAGE n / 50 ===` |
| Method | `pdf-layout` (`pdftotext -layout`) — x-position-preserving |
| Prior artifact | `p2-datasheet-narrative.txt` — **kept, not replaced**. It is the 2025 column-linearized capture; it remains the provenance record and the target of `table-reconstruction-notes.md`. Where the two disagree on tabular material, the new artifacts win. |

The datasheet's printed page numbers equal the physical page index (p.47's footer reads "Page 47"),
so every page citation in this folder is unambiguous.

### Digit-density gate (`ingest-source` §2a) — MANDATORY, run, and passed

```
python3 engineering/tools/validation/audit-extraction-digit-density.py engineering/ingestion/sources/p2-datasheet
```

| Artifact | Substantive lines | With a digit | Density |
|---|---|---|---|
| `p2-datasheet-text.txt` | 1,572 | 1,128 | **71.8%** |
| `complete-tables-reference.md` | 383 | 274 | **71.5%** |
| `p2-datasheet-narrative.txt` (prior) | 1,624 | 925 | 57.0% |

Corpus-wide (`--all`): **CLEAN at 57 artifacts, exit 0** — up from the 55-artifact baseline, the
growth being this ingestion's two new artifacts. **This is a smoke alarm, not a completeness
certificate**: it detects total numeral loss only, never partial, and passing it says nothing about
whether a table came out with its columns intact. That is what §3 is for.

---

## 3. Pass 1b — tables: four paths, reconciled

**Artifact: `complete-tables-reference.md` — CREATED 2026-08-24.**

| Path | Tool | Result |
|---|---|---|
| A | `camelot lattice -p all -f csv` | **45 ruled tables** found |
| B | `pdf-layout` → `p2-datasheet-text.txt` | correct vertical alignment; separates superscripts |
| C | `pdftoppm` page render, read visually | tie-breaker of record |
| D | `pdf2md` (docling) | 4th path; also recovers the document's **own Table of Contents** |

**Eight cell-level disagreements were found and resolved** (R1–R8, tabulated in
`complete-tables-reference.md`). The consequential one:

> **R1 — path A alone would have shipped ten wrong smart-pin mode numbers.** `camelot` fused each
> `%SSSSS` value to its superscript footnote marker, emitting six-digit values (`001001`, `110111`,
> `111001`, …) for a **five-bit** field. Paths B, C and D each independently show `00100¹`,
> `11011¹`, `11100¹` … with footnote 1 = *"OUT signal overridden"*. The rendered pages were read to
> settle it.

**This is the task's central lesson in one artifact:** a single extraction path, however good its
exit status, is not evidence. `camelot lattice` is the best structural tool available here and it
was wrong about ten values in one table.

### Tooling note — the documented `camelot` invocation does not run

`CLAUDE.md` and `/opt/pdf-tools/README.md` both give the command as:

```
camelot --pages all --format csv lattice <file.pdf>      # ← fails
```

The installed camelot rejects it: `Error: No such option '--pages'`. In this build the options
belong to the **subcommand**, not the group:

```
camelot lattice -p all -f csv -o <out.csv> <file.pdf>    # ← works
```

`-o` is a template — each table is written as `<stem>-page-<P>-table-<T>.csv`. Recorded here because
the wrong form fails with a usage message and **exit status 2** (arbiter-measured 2026-08-24;
an earlier draft of this section said exit 0 — it does not, and the distinction matters: exit 2
is a loud failure a script WILL catch), so a script that does not read the
output would report success having extracted nothing. That is the same shape as the failure this
whole ingestion exists to catch.

### `camelot stream` — run, and what it showed

Run over the 24 pages `lattice` found no table on (`-p 2-5,7-12,16,17,19,20,22,26-32,49`). It
reported 33 "tables", **all of them false positives** — bullet lists, prose blocks, page footers.
No real table was hiding on those pages. Recorded because the negative result is what licenses the
"not in this document" verdicts in §4.

---

## 4. The ten structurally-lost tables — per-table disposition

Numbering follows `identified-broken-tables.md`. **All ten are closed: eight recovered, two
determined not to be tables in this document.**

| # | Table | Where it actually is | Disposition |
|---|---|---|---|
| 1 | Memory Configuration | **p.1** | **RECOVERED** — path A, 5 x 5, clean first pass. Cross-checks cell-for-cell against Hardware Manual Table 3 / RAM config. |
| 2 | Pin Descriptions | **p.6** (the *section* starts p.5 — both prior page claims are right about different things) | **RECOVERED** — path A, 10 x 4. Identical to Hardware Manual Table 4. |
| 3 | Smart Pin Mode Configuration ("~line 1736") | **p.24** — it is the **(M) Pin Mode** table | **RECOVERED** — path A structure + path B values, then machine-verified: all 204 non-empty cells (of 24 x 9) found verbatim in path B's independent text, with a negative control. |
| 4 | **DC Characteristics** | **pp.47-48** (not p.34) | **RECOVERED** — all four paths agree. 4 rows on p.47 + 4 continuation rows on p.48. |
| 5 | **AC Characteristics** | **p.48** (not p.35) | **RECOVERED** — all four paths agree. **Exactly two symbols: `Freq` and `Cin`.** See §5. |
| 6 | I/O Pin Equivalent Circuit | **pp.26-32** | **NOT A TABLE** — 1 circuit diagram + 24 equivalent schematics, four to a page. Both table paths correctly find nothing; the pages' text layer is heading + footer only. Already captured as 25 images in `assets/images-20250906/`. The on-figure drive legend was **read off the rendered image** and is transcribed in `complete-tables-reference.md`. |
| 7 | Smart Pin Mode Summary | **pp.34-35** — the **(S) Smart Pin Modes** table | **RECOVERED**, 35 rows — after the R1 reconciliation above. |
| 8 | Clock Mode Settings | **p.18** | **RECOVERED** — three tables (`%E`/`%DDDDDD`/`%MMMMMMMMMM`/`%PPPP`, `%CC`, `%SS`). `%PPPP`'s 16 value/effect pairs were rebuilt from path B after path A linearized them. |
| 9 | Boot Source Selection | **NOT IN THIS DOCUMENT** | **DETERMINED, not gapped.** The datasheet's entire boot treatment is p.11 prose — *"The Bootloader checks the boot pattern (configuration) on pins P59-P61"* — closing *"See Propeller 2 Hardware Manual's Boot Up procedure section for more information."* Boot-mode selection appears on p.10 as a **switch in a schematic** plus two bullets, read off the rendered page. `lattice` finds no table on pp.8-11; `stream` returns only the bullet prose. The 9-row **Boot Pattern** table exists in the Hardware Manual (its Table 5) — exactly where the datasheet points. |
| 10 | HUBSET Bit Fields | **p.18** | **RECOVERED** — the format line `HUBSET ##%0000_000E_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS` plus the three field tables of #8. They are the same content; the prior note filed them twice. |

**Zero tables remain unrecoverable. No stop-1 escalation is owed.**

---

## 5. The AC Characteristics table — measured, not inferred

This is the table the sprint most needed settled, because `deliverables/ai/P2/architecture/io_pin_timing.yaml`
carries ~20 nanosecond quantities citing the datasheet's electrical specifications.

**The AC Characteristics table contains exactly two symbols and nine data lines:**

- `Freq` — Oscillator Frequency: RCSLOW 12/20/30 kHz · RCFAST 20/24/30 MHz · Direct drive DC/-/200 MHz ·
  Crystal 1/-/50 MHz · PLL 3.33/180²/320 MHz
- `Cin` — XI and XO pin Capacitance: modes 0-3 at 2 / 2 / 15 / 30 pF

**There is no propagation-delay row, no rise-time row, no input-timing row, and no nanosecond
quantity anywhere in it.** The table ends at `Cin` mode 3; the remainder of page 48 is white space
and two footnotes.

**How that was established — the distinction this ingestion exists to make.** A mangled table looks
exactly like a number that was never there, so the absence was not inferred from an extractor's
silence. Page 48 was **rendered and read**, and all four extraction paths were compared. They agree
on every cell. The source is silent; the extractor is not failing.

**Corroborating evidence from three other places in the same document:**

1. **p.22's three I/O-pin-timing figures are numbered in CLOCK EDGES with no time axis** — read off
   the images (see `assets/images-20260824/`). One of the three had never been extracted at all.
2. **p.22's body text says why**, verbatim: *"the duration until complete depends on clock frequency
   and circuit load. The I/O pads are asynchronous (not tied strictly to the clock)…"* The datasheet
   explicitly declines to specify a fixed transition time.
3. **The whole document contains exactly ONE nanosecond quantity, and it is not a pin-timing
   number.** Measured with `grep -nEo '[0-9]+(\.[0-9]+)? ?n[sS]([^a-zA-Z]|$)'` over
   `p2-datasheet-text.txt`: a single hit, **line 109, page 3, in the FEATURES bullet list** —
   *"8-bit, 120-ohm (**3ns**) and 1k-ohm DACs with 16-bit oversampling, noise, and high/low digital
   modes"*. The datasheet **does not say what that `3ns` measures** — it is an unlabelled parenthetical
   attached to the fast DAC (the p.24 (M) Pin Mode table gives that DAC's impedance as `123.75 Ω`,
   which the bullet rounds to "120-ohm"). What can be stated is what it is *not*: it is not a
   propagation delay, not a rise time, and not an I/O-pin timing specification — it is attached to a
   DAC in a features list. The identical bullet appears in Propeller 2 Documentation v35 Rev B/C
   (`sources/silicon-doc/p2-documentation.txt:451`), also unexplained. The word "nanosecond" appears
   **zero** times. The document's unit vocabulary is otherwise
   `V · mV · µA · mA · A · W · kV · pF · Ω · kHz · MHz · ms · °C`.

   **Recorded deliberately, because a careless grep for `ns` will find it.** A future agent looking
   to source `io_pin_timing.yaml`'s `2.5 / 3.5 / 5.0 ns` propagation delays must not mistake this
   DAC figure for one of them. It is the only `ns` in the document and it belongs to a DAC.

**Consequence for F-329:** its Path-B claim — *"the datasheet's AC Characteristics table contains
exactly two symbols, `Freq` and `Cin`"* — was recorded as the weaker half because it rested on the
known-broken narrative extract. **The `camelot lattice` pass plan §8 owed is now run, and it
confirms the claim rather than overturning it.** F-329's page numbers (DC p.47, AC p.48) are also
confirmed; see §6.

**Consequence for the corroborated half of that file:** `io_pin_timing.yaml`'s
`instruction_to_pin_timing:` block (3 clocks output latency, 3 clocks `INx` staleness, 2 clocks
`TESTP`) is now corroborated by the **datasheet** as well as the Hardware Manual, at p.22, in the
document's own words and figures. It needs a citation, not deletion — and there are now two
independent documentary sources to cite.

---

## 6. The page-number dispute — settled by the document itself

Three incompatible page claims were in play. The datasheet's **own Table of Contents** (recovered by
path D) settles it:

```
| SYSTEM CHARACTERISTICS               | 47 |
| Absolute Maximum Electrical Ratings  | 47 |
| DC Characteristics                   | 47 |
| AC Characteristics                   | 48 |
| PACKAGING                            | 49 |
| CHANGE LOG                           | 50 |
```

| Claim | Source | Verdict |
|---|---|---|
| DC p.47 · AC p.48 | finding **F-329** | ✅ **CONFIRMED** — by the TOC, by the printed page footers, and by reading both rendered pages. |
| DC p.34 · AC p.35 | `identified-broken-tables.md` | ❌ **REFUTED.** Pages 34-35 are the *(S) Smart Pin Modes* table. |
| "pages 42-45, 76-78" | `deliverables/ai/P2/architecture/io_pin_timing.yaml` line 3 | ❌ **REFUTED, both halves.** The document is **50 pages**, so **76-78 cannot exist**; and pp.42-45 are the PASM2 instruction listing (Hub RAM / branch / CORDIC groups), not electrical specifications. The header also claims *"Layer 1: Direct extraction from … P2 Datasheet"* for content the datasheet does not contain. |

That YAML file is **not touched by this ingestion** — repair belongs to the purge/repopulate tasks.
Recorded here so the ambiguity that let the numbers ship cannot recur.

---

## 7. Cross-source corroboration — against the Hardware Manual

The P2 Hardware Manual (same 2022/11/01 edition) was re-ingested DOCX-primary on 2026-08-24; its 53
tables carry real structure, making it the strongest available corroborator.

| Subject | Datasheet | Hardware Manual | Result |
|---|---|---|---|
| Part Number Legend | p.1 | Table 3 | identical |
| Pin Descriptions | p.6 | Table 4 | identical on name/direction/V(typ) |
| Special-purpose registers `$1F8..$1FF` | p.14 | Table 9 | identical — **including the same `INA1`/`INB2` superscript fusion**, so the footnote reading (R8) applies to both |
| PLL `%E`/`%DDDDDD`/`%MMMMMMMMMM`/`%PPPP` | p.18 | Table 10 | identical **except** the VCO range — see below |
| `%CC` crystal config | p.18 | Table 11 | identical |
| `%SS` clock source | p.18 | Table 12 | identical (datasheet adds "nominally ~24 MHz" to the RCFAST note) |
| (M) Pin Mode, all 24 rows | p.24 | Table 18 | **identical, cell for cell** — an independent confirmation of the R7 rebuild |
| Pin Mode Legend | p.24 | Tables 20/21/22 (nested-in-cell) | identical |
| Pin drive ladder | p.24 legend **and** the pp.27-32 figures | Table 21 + figs 10-33 | **identical and resistive**: `000 Fast/Digital · 001 1.5 kΩ · 010 15 kΩ · 011 150 kΩ · 100 1 mA · 101 100 µA · 110 10 µA · 111 Float` |
| Max current per I/O pin | p.47, **±30 mA** | Table 2, `+/- 30mA` | agrees |
| Boot Pattern | absent — defers to the manual | Table 5 | a deliberate cross-reference, not a conflict |
| DC / AC Characteristics | pp.47-48 | **absent** — the manual has no electrical-characteristics section | datasheet is the sole documentary authority |

**The drive-ladder row is a fifth independent confirmation of F-329's core claim.** The datasheet
states the ladder twice within itself (the p.24 legend and the on-figure legend of every
equivalent schematic), and both are **resistive**. The KB's `1.5 mA / 15 mA / 150 mA` reuse the
numerals of the **kΩ** rungs with the unit changed.

### One conflict, filed — F-330

| Source | Same sentence, different number |
|---|---|
| Datasheet p.18 and p.19; Propeller 2 Documentation v35 Rev B/C (twice) | VCO *"should be kept within 100 MHz to **200 MHz**"* |
| Hardware Manual Table 10 (verified in the raw `word/document.xml`) | VCO *"should be kept within 100 MHz to **350 MHz**"* |

The vocabulary key was checked first, per standing practice: **350 MHz is real, but it is the
overclock ceiling**, which the Silicon Doc states in the next row of the same table (*"For fastest
overclocking, the PLL can be pushed to 350 MHz using the 'VCO / 1' mode (%PPPP = 15)"*) and which
Spin2 v51 carries as the compiler's upper bound. The Hardware Manual substituted the ceiling into
the recommendation sentence. That does not dissolve the conflict — both sentences make the same
claim with different numbers — so it is filed as **F-330**, `CONFIRMED`. **No KB edit is owed:**
`architecture/clock_system.yaml` already draws the distinction correctly. The finding exists so a
future agent does not "correct" it in the wrong direction.

---

## 8. Images — one gap found and closed

| Metric | Value |
|---|---|
| Image XObjects in the PDF | **40**, across 17 pages (`pdfimages -list`: 68 rows = 40 images + 28 soft masks) |
| Captured 2025-09-06 | 39 (`assets/images-20250906/`) — that catalog claims "100% (39/39)" |
| **Missing** | **1** — page 22 `img01`, the `DRVH #0` output-latency timing diagram. The old folder's filenames skip from `img02` to `img03` with no `img01`. |
| Recovered 2026-08-24 | `assets/images-20260824/` — all three page-22 figures, `pdfimages` lossless XObject extraction, with a catalog naming what each shows |
| Also present | `assets/images-20260706/` — 16 whole-page renders of the image-bearing pages |

The 2025 folder is a dated capture and was **not** modified.

---

## 9. What is still owed (recorded gaps, not silent omissions)

| Gap | Detail |
|---|---|
| **Code-example pass (`ingest-source` pass 2) not run** | The datasheet's code content is small and non-compilable as-is: a **4-line** `HUBSET`/`WAITX` clock-switch sequence (p.19), P2-Monitor terminal transcripts (p.11), and two TAQOZ Forth one-liners (p.12). None is a standalone Spin2/PASM2 program, so none can be `pnut-ts`-validated without authoring a wrapper — which would make the artifact ours, not the source's. **Out of scope for this task and not claimed as done.** |
| **PASM2 instruction listing (pp.36-46) not re-derived** | Already carried by `pasm2-complete-instruction-tables.md` (407 instruction rows). `camelot lattice` recovered 20 tables across those pages independently; they are in the scratch capture but were not merged, to avoid producing a second, competing instruction reference. **Worth a future reconciliation pass**: the existing artifact renders the fixed-2-clock groups as 2-column tables with the clock count stated in prose, while `camelot` recovers the clocks column for every group. |
| **Page 49 (PACKAGING) is an image-only page** | The package outline drawing is captured as `page49_img01.png`; its dimensions are not transcribed. |

---

## 10. Completeness

| Dimension | State |
|---|---|
| Pages captured | **50 / 50** |
| Structurally-lost tables closed | **10 / 10** (8 recovered, 2 determined not to be tables) |
| Table artifact | **created** — `complete-tables-reference.md`, 4 paths reconciled, 8 cell-level repairs named |
| Raw-text artifact | **created** — `p2-datasheet-text.txt`, page-delimited |
| Digit-density gate | run; **71.8% / 71.5%**; corpus CLEAN at 57 artifacts |
| Images | 40 / 40 accounted; the one prior miss recovered |
| Cross-source | run against `p2-hardware-manual`; 11 subjects compared, **1 conflict filed (F-330)** |
| Code examples | **not run — recorded gap (§9)** |
| **Dashboard row** | **94% → 98%**, with the residual being the code pass and the PASM2 reconciliation of §9 |

**What "98%" means here, stated so it cannot be misread as the prior 94% was:** every page is
captured, every named table is closed, and every number in this audit was measured with a command
that can be re-run. The 2% is the two recorded gaps in §9 — not rounding, and not optimism.
