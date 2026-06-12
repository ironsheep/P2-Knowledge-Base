# Smart Pins (Titus) rev 5 — Complete Extraction Audit (Audit of Record)

**Source ID:** `src:smart-pins-titus` · **Edition:** rev 5 (`Smart Pins rev 5.docx`, 2026-03-31)
**Ingested:** 2026-06-12 · **Skill:** `ingest-source` (7-pass, DOCX-primary) · **Role:** 🟡 cross-check
**Type:** **RE-EXTRACTION** — supersedes the lossy PDF-scraped prior in `smart-pins-catalog/`
**Certification run** for the updated `ingest-source` skill (quad-update + reviewer-harvest + §0.6 obsolescence).

---

## Verdict: COMPLETE — ~90% · all gates closed except OCR-enhancement debt (non-blocking)

A comprehensive, well-structured Smart Pins reference: **all 32 smart-pin modes** (%00000–%11111)
covered in prose, plus the I/O-pin instruction set and I/O-bit timing. Faithfully re-extracted from
the DOCX (no page-break code fragmentation, no whitespace loss — the defects that forced the prior
5-script PDF recovery are gone at the source).

## Per-pass results

| # | Pass | Result |
|---|------|--------|
| 1 | **Content** | 1,732 paragraphs, ~109 KB text. Structure: STANDARD I/O PINS → I/O registers/instructions → I/O-bit timing → Smart Pins (32 modes). **0 Word tables** (Titus uses aligned preformatted text for register layouts — extracted as code/text). `smart-pins-titus-text.txt`. **32/32 modes have prose.** |
| 2 | **Code** | 144 monospace blocks → **40 structured** + 104 illustrative snippets. Of the 40: **10 are instruction-reference/syntax tables** (dropped — not examples), **30 are code examples** → **28 compile clean** under `pnut-ts v1.55.0` (PNut v55) in a standard COG-PASM harness (mode-config block + scaffold), **2 are conceptual Silicon-Doc-style fragments** (undefined `adcpin`/`pinblock`, `#expr\|n` immediate syntax). Autocorrect normalized (curly quotes, en/em-dash, nbsp). Catalog: `assets/code-2026-06-12/`. |
| 3 | **Images** | **21 figures** (18 jpg + 3 png) from `word/media/` (lossless). **Quality gate: 21/21 PASS** (white-bg diagrams, brightness 238–250, no black/full-page mis-captures — DOCX-media eliminated the v3.0 failure class). Each mapped to its mode/section. **4 OCR'd** across all diagram families (I/O-timing, NCO register-value, encoder, PWM); 17 waveform OCRs deferred as enhancement debt. `assets/images-…/image-catalog.md`. |
| 4 | **Post-processing** | Per-mode coverage matrix built (prose/code/image per mode). Modes lacking a code example: %00101, %01010 (SMPS — confirms reviewer #20), %01100/%01101, %10100–%10111, %11000, %11011 (USB), %11100 (refers to prior). |
| 5 | **Validation** | Section-by-section: all 32 modes present; I/O instruction set complete (DIR/OUT/FLT/DRV families + IN). Code compile-validated (above). Images quality-gated (above). Defects catalogued (below). |
| 6 | **Cross-source Q&A** | **27 reviewer comments harvested + classified** (`reviewer-comments-harvest.md`); 1 factual claim CONFIRMED against Silicon Doc (#21 WRPIN selector swap); gap ledger + expert questions → `KNOWLEDGE-GAPS.md`; **0 corrections-register entries** (no conflict with published YAML). Detail: `cross-source-qa.md`. |
| 7 | **Registration** | Dashboard row updated (0% → ~90%, C·K·I·A·X); tier 🟡 re-confirmed in `AUTHORITATIVE-SOURCES`; re-extraction supersession completed in `DOCUMENT-LINEAGE`; prior PDF extraction archived per §0.6. |

## C·K·I·A·X gate status (for the dashboard)
- **C** content ✅ · **K** code ✅ (28/30 validated) · **I** images ✅ (21/21 gated; OCR debt) · **A** audit ✅ · **X** cross-source ✅

## Confirmed source defects (Titus errata — its own editorial process owns the fix; NOT our YAML)
1. **WRPIN %AAAA/%BBBB input-selector swap** — `x101` and `x111` reversed vs Silicon Doc (should be −3 / −1; Titus has −1 / −3). Reviewer #21 (Walter Mosscrop) correct. *Verified against silicon-doc.*
2. **BBBB row typo** — `x011 = …+3 = P39` should be **P40** (AAAA row is correct).
3. **Missing `wc`** in the %10000 Time-A-input example `.test_loop_x` (`rqpin … #A_in` then `if_nc` on stale carry). Reviewer #18 (Carroll Moore) correct.
4. **`COM` mis-typed section header** (→ `CON`) in 4 mode examples.
5. **%01010 PWM-SMPS has no code example** (reviewer #20). 
6. Sync-serial start-bit framing questioned (reviewer #5) — unverified, routed to experts.

## Trust scoring (this source)
🟡 **cross-check / MEDIUM** confirmed by this run: a concrete bit-field table here was **wrong** and caught
only in peer review. Use Titus to *corroborate and add color* (techniques, application notes, external-ADC
references) — **never as the authority for a bit-field or encoding**; those resolve to Silicon Doc / `pnut_ts`.

## Obsolescence handling (§0.6) — prior PDF extraction
The prior PDF-scraped Titus capture (`engineering/ingestion/smart-pins-catalog/`: 21 recovered examples,
`byMode/`, the 5 recovery scripts, `TITUS-CODE-RECOVERY.md`) is **obsolete** (a lossy capture, now replaced).
**Archived (not deleted)** with a pointer to this extraction; git history remains the record. Downstream
Titus-derived content re-validated against this authoritative extraction — see `DOCUMENT-LINEAGE.md`.

## Provenance
Extraction scripts ran from `/tmp` (not committed — methodology, not artifact). Inputs: the rev5 DOCX
(`word/document.xml`, `word/comments.xml`, `word/media/*`). Validators: `pnut-ts v1.55.0`, `image-tools-mcp`,
cross-check vs `src:silicon-doc`. Raw text + comments JSON + assets are the durable artifacts.
