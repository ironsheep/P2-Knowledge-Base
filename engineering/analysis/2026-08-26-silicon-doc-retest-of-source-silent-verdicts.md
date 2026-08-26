# Re-test of source-silent verdicts against the completed silicon-doc extraction

**Run:** 2026-08-26, task «#312» · **Against:** `silicon-doc-text.txt` +
`complete-silicon-doc-reference.md` + `assets/images-silicon-doc-2026-08-26/` (DOCX-primary,
48/48 tables, 34/34 media).

## Why this had to be re-run

Every *"no source states it"* verdict from the YAML-fidelity sprint was reached while the **Tier-1
authority was 75% ingested and contributing none of its 48 tables**. Those verdicts were not wrong
by carelessness — they were drawn against a corpus with a known hole. Re-testing them is the point
of this sprint; the extraction was only the means.

**A verdict left unexamined is not confirmed.** Each row below was re-run and carries an explicit
outcome with its evidence.

## Verdicts

| # | Verdict | Outcome |
|---|---|---|
| **G-021** — TQFP-100 package dimensions | **✅ OVERTURNED — CLOSED** | The drawing was in the Silicon Doc the whole time |
| **G-019** — I/O AC switching characteristics | **CONFIRMED**, with a refinement | Core stands; two I/O facts newly available |
| **G-020** — thermal / derating / decoupling / EMC | **CONFIRMED** | Zero content, false positives ruled out |
| **F-347** — the 13 "never returns (UNSOURCED)" | **CONFIRMED correctly purged** | New extract corroborates the *replacement* |
| **F-334** — the 48-block hardware purge | **CONFIRMED, nothing owed** | The 2 chip-level blocks are already restored |

---

### G-021 — OVERTURNED

`silicon-034.png` is the ON Semiconductor **MECHANICAL CASE OUTLINE / PACKAGE DIMENSIONS** sheet:
**TQFP100 14×14, 0.5P, CASE 932BR, ISSUE O**, 03 JUL 2018, document **98AON94348G**.

Read off the rendered drawing **twice** — whole page, then the dimension table at 3.5× zoom — with
both reads agreeing. **Deliberately not OCR'd:** tesseract misreads digits on these sheets (`@`/`Q`
for `0`, `4` for `1`), and these are precision values.

| DIM | MIN | NOM | MAX | | DIM | MIN | NOM | MAX |
|---|---|---|---|---|---|---|---|---|
| A | — | — | 1.20 | | E | 15.80 | 16.00 | 16.20 |
| A1 | 0.05 | — | 0.15 | | E1 | 13.80 | 14.00 | 14.20 |
| A2 | 0.95 | 1.00 | 1.05 | | E2 | 9.50 REF | | |
| b | 0.17 | 0.22 | 0.27 | | e | 0.50 BSC | | |
| c | 0.20 REF | | | | L | 0.45 | 0.60 | 0.75 |
| D | 15.80 | 16.00 | 16.20 | | L1 | 1.00 REF | | |
| D1 | 13.80 | 14.00 | 14.20 | | M | 0° | — | 7° |
| D2 | 9.50 REF | | | | | | | |

Recommended mounting footprint also present: 16.83 / 9.60 outer, 100× 1.49, 100× 0.28, 0.50 pitch.

**The row's own disposition was right** — *"closable from a source we already hold"*. What kept it
open was that the source had never been fully extracted. Transcription into `deliverables/` is the
YAML head's; this task does not edit shipped YAML.

### G-019 — CONFIRMED, with a refinement worth making

**Core stands.** `propagation delay`, `rise time`, `fall time`, `slew rate` → **zero hits** in the
completed extract.

All **9** `ns` quantities were read individually rather than counted:

| Locator | Quantity | What it actually is |
|---|---|---|
| `:81` | `<2ns @100us` | **PLL jitter** |
| `:199` | `120-ohm (3ns)` | **DAC** settling — the same lone figure the datasheet had |
| `:2807` | `6.25ns/clock` | **clock period** at 160 MHz |
| `:2817`, `:2827` | `12.5ns`, `600ns` | **digital input-filter** low-pass times (Table 30) |

**Refinement — the row overstated its own scope and is corrected.** Two I/O-electrical facts *are*
now available that were not before:

1. **Table 30, the digital input-filter low-pass times**, computed in the document itself:
   `filt0: 6.25ns × 1 × 2 = 12.5ns`, `filt1: 6.25ns × 32 × 3 = 600ns`. **This table lives inside a
   table cell**, so no PDF-era capture could carry it — and our own first DOCX pass flattened it
   until «#310» fixed the walker.
2. **The drive-mode ladder**, stated in one line at `:206`.

Neither is a pin-driver AC characterisation, so **the gap does not close**. But the row's clause
*"no per-drive-mode current in mA anywhere in the corpus"* is now too strong, and leaving it would
be leaving a false negative in the register.

### G-020 — CONFIRMED

Measured: `thermal resist` 0 · `junction-to` 0 · `decoupl` 0 · `EMC` 0 · `heatsink` 0 ·
`heat sink` 0 · `ground plane` 0.

**Apparent hits ruled out rather than ignored:** the 4 `theta` matches are the CORDIC polar angle
(`Rho32,Theta32`, `:179-181`); the 3 `derat` matches are the substring inside `CONSIDERATIONS`; the
single `thermal` match is *"31 bits of thermal noise gleaned from pin 63"* for PRNG seeding
(`:2854`). The fully-extracted Tier-1 authority contains **no thermal-design content whatsoever**.

### F-347's 13 "never returns (UNSOURCED)" — CONFIRMED correctly purged

The F-327 fabrication family. The question was whether the recovered tables now source any of it.

**They do not — and the reason is the interesting part.** The Silicon Doc states the drive ladder
in one line at `:206`:

> *"Separate drive modes for high and low output: logic / 1.5 k / 15 k / 150 k / 1 mA / 100 µA / 10 µA / float"*

That matches the **replacement** content in `architecture/pin-drive-configuration.yaml` on all
eight rungs (`%000` Fast/logic … `%111` Float), which already cites the Datasheet Pin Mode Legend
and the Hardware Manual. So the new extract is a **fourth corroborating source for what replaced the
fabrication**, not a restorer of what was purged. The purge was right and stays right.

### F-334's 48-block hardware purge — CONFIRMED, nothing owed

The Silicon Doc documents the **chip**; `hardware/` is board-level, so most of these are out of its
domain by construction. **Rather than assume that, the block list was scanned for chip-level
content:** two entries qualify — `boot_modes` in `edge-32mb-module.yaml` and
`edge-standard-module.yaml`. **Both are PRESENT in the shipped files today**, i.e. already restored
in the 45 "restored with a trace". Nothing is owed.

Worth noting alongside: **E-014** established that the Silicon Doc's own boot description is
*incomplete* (it omits microSD), so it would have been the wrong source to restore `boot_modes`
from even if they had been missing. The Hardware Manual's boot-source table is the better one, and
is what the KB already uses.

## What this changes

- **One gap closes outright** (G-021), from a source that had been sitting in the repo unextracted.
- **One gap is corrected rather than closed** (G-019) — the register was carrying a claim broader
  than the evidence supported.
- **Three verdicts survive re-testing** and are now confirmed against a complete corpus instead of a
  75% one, which is worth more than the two that moved.
