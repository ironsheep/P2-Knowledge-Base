# AN004-GUI-StartVGA — Extraction Audit (pass 5: completeness validation)

**Source:** `AN004-GUI-StartVGA-v1.0.pdf` — Parallax Semiconductor App Note AN004 v1.0,
16 pp., © 2011. **Platform: Propeller 1 (P8X32A).** Mode: **new** (greenfield).
**Wave:** `p1-appnotes-2026-06` (MAP agent, passes 1–5 STAGE-ONLY).

## Text-layer integrity

- `pdftotext -f 1 -l 1` sample: **clean** — real curly quotes / en-dashes, no ToUnicode
  cipher. **No OCR required** for body text. Page numbers / running header
  ("GUI & Graphics Series … v1.0   N of 16" / "Parallax Semiconductor   AN004") present on
  every page and excluded from prose.

## Section-by-section coverage (all 16 pages)

| Section | Pages | Captured? | Notes |
|---|---|---|---|
| Header / Abstract | 1 | ✅ | abstract verbatim |
| Introduction | 1–2 | ✅ | driver-selection rationale + 7 feature bullets |
| VGA Driver Features in Detail | 2–3 | ✅ | ScreenPtr/ColorPtr/CursorPtr; MODE table; RGB[2:2:2:0] |
| Terminal Services & Console Support | 3–4 | ✅ | 5 feature bullets; WMF = Window Manager Framework note |
| Sub-Object Locations in Hierarchy | 4–5 | ✅ | Spin1 call-graph rules |
| Example 1: Hello World | 5–8 | ✅ | Start + CreateAppGUI listings captured |
| Example 2: Guess My Number | 8–11 | ✅ | RNG seed, Start loop, GetStringTerm listings captured |
| Example 3: Color Themes | 11–13 | ✅ | CTHEME constants + color-design guidelines |
| Summary | 13 | ✅ | |
| API Listing | 13–15 | ✅ | all ~35 public methods captured |
| Resources / References / Revision History | 15–16 | ✅ | code ZIP URL, OBEX ref, v1.0 |
| Legal / copyright | 16 | ✅ | preserved in reference md metadata |

**Tables:** 1 true tabular structure (cursor MODE 3-bit encoding) — captured as a markdown
table. Other "tables" in the doc are bullet lists / inline format specs (RGB byte layout,
resolution→grid map) — captured as lists.

## Pass counts

- **Prose:** ~60 paragraphs across 10 sections + 1 abstract; raw `*-text.txt` = 854 lines
  (layout-preserving `pdftotext -layout`).
- **In-PDF code listings:** 6 (Start ×2, CreateAppGUI, RNG-seed snippet, GuessMyNumber Start
  loop, GetStringTerm, CTHEME constants) — captured into the curated md as illustrative
  Spin1; these are **excerpts of** the companion files, not separate programs.
- **Tables:** 1 (cursor MODE encoding).
- **Code files (companion):** 7 `.spin` captured verbatim + cataloged — **NOT validated**
  (`code_validated: false`; no P1 compiler — charter §3).
- **Images:** 16 extracted / 16 quality-passed / 2 diagram figures OCR'd (Fig 2, Fig 3);
  16 → 7 logical figures.

## Fidelity / risk flags

- Companion `.spin` files are **UTF-16 LE** — flagged in code-catalog; not a defect.
- PDF prose has minor in-source typos preserved verbatim (e.g.
  `CTHEME_ATARI_64_FG` vs `CTHEME_ATARI_C64_FG` in one sentence; "PWM#" object alias used in
  prose where code uses `WMF#`/`PWM#` — a doc inconsistency, not an extraction error). Logged
  as a candidate gap, not corrected.
- No content was dropped, summarized-away, or fabricated. Code excerpts in the curated md are
  transcribed from the PDF body, lightly normalized (ASCII quotes) and labeled as excerpts.

## Verdict

**Extraction COMPLETE for passes 1–3 + validated (pass 5).** Ready for reduce-phase pass-6
(cross-source Q&A) and pass-7 (registration / audit-of-record promotion). No canonical
`sources/` files were modified; all outputs are in the wave staging tree.
