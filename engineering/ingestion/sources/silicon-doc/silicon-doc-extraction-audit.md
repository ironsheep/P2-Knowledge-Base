# silicon-doc — Extraction Audit (DOCX re-extraction)

**Source:** `Parallax Propeller 2 Documentation v35 - Rev B_C Silicon.docx` — Parallax Inc.,
v35 (Rev B/C silicon), 4,814,991 bytes.
**Mode:** re-extraction. The prior capture is PDF-derived and carries zero tables. This
re-extraction was scheduled 2026-06-22 and had not been run.
**Extraction date:** 2026-08-26
**Tooling:** `engineering/tools/extraction/docx_walk.py` (document-order walk, recurses into
table cells) · `pnut-ts v1.55.3 -d` · `tesseract` · `audit-extraction-digit-density.py`

## Pre-flight

DOCX, so no text-layer cipher risk and no OCR needed for body content. Structural survey:

| | |
|---|---|
| `<w:p>` paragraphs (total, incl. in-cell) | 5,719 |
| body-level paragraphs | 3,351 |
| monospace paragraphs | 1,105 |
| `<w:tbl>` tables | **48** (1 nested inside a table cell) |
| `word/media` assets | **34** (31 png, 2 jpg, 1 gif) |
| `word/comments.xml` | **present** — reviewer notes to harvest in pass 6 |

## Digit-density gate (§2a) — MANDATORY, run on the pass-1 artifacts

```
python3 engineering/tools/validation/audit-extraction-digit-density.py \
        engineering/ingestion/sources/silicon-doc
```

| artifact | lines | w/digit | density |
|---|---|---|---|
| `silicon-doc-text.txt` | 3,648 | 2,838 | **77.8%** |
| `complete-silicon-doc-reference.md` | 3,480 | 2,607 | **74.9%** |

Floor is 20% of substantive lines. **Exit 0.** Carrying the tool's own caveat rather than
paraphrasing it: this detects **total** numeral loss only, is **blind to partial loss**, and is
**never a completeness certificate**.

## A defect this audit found in its own extraction — and fixed

**The first pass was wrong, and the gates did not say so.** `docx_walk.py` collapsed whitespace
inside table cells. The Silicon Doc keeps large listings *in* cells — the worst holds **636
newlines / 32,199 characters** — so that cell became a single 24,645-character line. **31 of the
48 tables have multi-line cells**, so this was the common case, not an edge case.

Every gate stayed green through it: 48/48 tables counted (true), digit density 71.3% (true),
`validate-dod-release` exit 0 (true). **A correct count over mangled content.** Fixed by
preserving intra-cell newlines; the artifact went from a 24,645-char longest line to 950, from
3,667 lines to 5,625, and digit density *rose* to 77.8% because the flattening had been diluting
it. The PASM2 instruction encoding table is now **406 individually addressable `EEEE` lines**
instead of one blob.

## Section-by-section coverage

| Area | Captured | Notes |
|---|---|---|
| Version/revision history, chip identity | YES | |
| Instruction encoding master table | YES | 406 `EEEE`-prefixed lines, line-addressable |
| Condition/effect field legend (C, Z, I, L, R, WW, D, S, A, N) | YES | `silicon-doc-text.txt:180-190` |
| COG/LUT RAM map, dual- and special-purpose registers | YES | **disagreement found → F-363** |
| Instruction timing pipeline diagram | YES | ASCII, preserved |
| Smart pin modes (per-mode narrative + tables) | YES | plus 23 per-mode figures |
| Streamer, CORDIC, boot, interrupts, events, locks | YES | |
| MODCZ constants, instruction aliases, assembler directives | YES | |
| Worked examples (XBYTE, Goertzel, VGA/HDMI) | YES | **initially missed — see below** |

## Pass 2 — code

180 monospace blocks → 61 prose (dropped, not failures), 13 encoding tables, 106 PASM2
fragments. Fragments reference symbols the narrative defines, so each was harnessed
(`CON`/`DAT`/`org 0`, parent label) with undefined symbols declared: **67/106 compile clean**.
All 39 remaining were inspected and trace to the block not being code, or to a limit of the
auto-declarer — **never to an extraction defect**.

**Then the cell-collapse fix exposed a second miss:** pass 2 read paragraphs only, and this
document keeps its worked examples in table cells. Six cell-hosted listings, 121 code lines,
recovered — the XBYTE demo, the bytecode executor, Goertzel, and a 252-line VGA 640×480 HDMI
program. **4 of the 6 compile clean with no harness and no declared symbols.** One is a
deliberate mid-program fragment; one fails only on `DAT file not found [birds_16bpp.bmp]`, an
external asset the document does not ship.

## Pass 3 — images

34/34 extracted losslessly from `word/media`. **The standard black-dominant quality test is
disarmed here:** `image_dominant_colors` reports `#000000` at 100% for a figure `tesseract` then
read text off, because 30 of 31 PNGs are RGBA/colormap. The control that works is OCR yield —
**33 of 34** assets returned substantive text. Second corpus to show this inversion.

## Reconciliation against the prior PDF-era artifacts

| Prior artifact | Verdict |
|---|---|
| `COG-RAM-REGISTER-MAP.md` | **DISAGREES** on `$1F6`/`$1F7` → **F-363** (triple-corroborated against the new extraction, the Hardware Manual and the Datasheet) |
| `WW-FIELD-ENCODING.md` | agrees; its `Line 667-669` citation is into the superseded artifact (new location `:185`) |
| `INSTRUCTION-TIMING-AND-ENCODING.md` | agrees |
| `KNOWN-BUGS-CRITICAL.md` | agrees |
| `instruction-encodings-for-verification.md` | agrees |
| `silicon-doc-v35-facts-only.md` | agrees |

## Obsolescence handling

**Mark-in-place, no move** — `SUPERSEDED-BY-2026-08-26-DOCX.md`. 293 references to
`p2-documentation.txt` exist outside this folder (24 in the shipped KB, 23 of them with `:line`
locators). Moving the file would strand every one. Re-anchoring tracked as **F-365**.

## Trust

**GREEN** — Tier-1 Parallax authority, DOCX-primary, structure preserved, and the one substantive
disagreement with prior artifacts resolved *against* our shipped KB by three independent sources.
The audit's own extraction defect was found, fixed, and recorded rather than shipped.
