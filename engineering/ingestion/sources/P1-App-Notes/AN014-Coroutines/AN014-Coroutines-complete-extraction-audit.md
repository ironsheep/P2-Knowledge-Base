# Extraction Audit — AN014 Coroutines (Pass 5 validation)

**Source:** Parallax Semiconductor AN014, *Coroutines in Propeller Assembly Language*, v1.0 (2011)
**Platform:** Propeller 1 (P8X32A) — Spin1 + PASM1
**Ingestion mode:** new (greenfield) · MAP agent, wave `p1-appnotes-2026-06` · passes 1–5 STAGE-ONLY
**Audited:** 2026-06-27

## Section-by-section completeness

| PDF section (pp 1–5) | Captured in `complete-AN014-reference.md`? | Notes |
|----------------------|-------------------------------------------|-------|
| Header / contact / AN number | yes | front-matter |
| Abstract | yes | verbatim sense |
| Introduction | yes | |
| Coroutine Principle + Figure 1 | yes | figure extracted (vector → page-render+crop) |
| (post-figure prose: interleaving, use cases) | yes | full-duplex serial / encoder+motor examples |
| Propeller Coroutine Implementation — 4-step sequence | yes | numbered list preserved |
| `JMPRET` / "call is jmpret in disguise" + 2 equivalence listings | yes | both code listings preserved |
| `swap` same-location trick + 3-step walk | yes | |
| Program Example (full CON/PUB/DAT listing) | yes | matches companion `.spin` |
| Two "points worth noting" (shared var, C/Z flags) | yes | |
| Flag save/restore idioms (3 listings) | yes | `muxnz`/`muxc` + `test`/`shr` patterns |
| Resources / References / Revision History | yes | |
| Legal / copyright footer | yes | preserved in front-matter |

**Result: 100% of document content captured.** No section dropped; no table content (document has no tables — only numbered lists). Text layer clean throughout (no OCR, no cipher).

## Per-pass results

| Pass | Output | Count | Status |
|------|--------|-------|--------|
| 1 Content | `AN014-Coroutines-text.txt` (raw, 298 ln) + `complete-AN014-reference.md` (curated) | ~22 prose paragraphs/lists; 0 tables; 5 in-prose code listings | COMPLETE |
| 2 Code | `assets/code-2026-06-27/appnote_coroutine.spin` + `code-catalog.md` | 1 file captured + cataloged; **0 validated** (no P1 compiler — charter §3) | CAPTURED-NOT-VALIDATED |
| 3 Images | `assets/images-AN014-Coroutines-2026-06-27/` + `image-catalog.md` | 1 figure extracted / 1 quality-passed / 0 OCR-forced (read directly) | COMPLETE |
| 4 Post-processing | (light — single-source technique note; relationships captured inline) | n/a | N/A for greenfield map |
| 5 Validation | this file | — | COMPLETE |

## Fidelity checks

- **Code ↔ prose cross-check:** the `DAT` listing in the PDF Program Example (text.txt ll. 164–222) matches `appnote_coroutine.spin` line-for-line (same labels, operands, comments). PASS.
- **Figure ↔ prose:** Figure 1's interleave order (A,a,B,b,C,c,D,a) agrees with the prose "execution bounces back and forth … interleaved execution." PASS.
- **Encoding:** `.spin` is UTF-16 LE (CRLF) — copied **byte-for-byte** (md5 verified identical to canonical source); not transcoded.
- **Canonical source untouched:** all tool output directed to staging; `sources/` unmodified.

## Known limitations

- **Code not compiler-validated** (no P1 toolchain in container). `code_validated: false`. This is the single dimension preventing 100% — inherent to P1 charter §3, not an extraction defect.
- Figure 1 crop carries a 1-line cosmetic footer-rule sliver (noted in image-catalog; non-blocking).

## Completeness

**~95%** — content/figure capture complete and faithful; only the code-validation dimension is open (P1-compiler-blocked, by charter).
