# AN013-WMF-Menus — Extraction Audit (pass 5, STAGE-ONLY)

**Source:** AN013 *GUI & Graphics Series — Menus and Messaging with the Propeller Window
Manager Framework* v1.0 · Parallax Semiconductor · © 2011 · 49 pp · PDF-only.
**Platform:** Propeller 1 (P8X32A), Spin1 + PASM1.
**Mode:** new (greenfield) · **Wave:** p1-appnotes-2026-06 · **Date:** 2026-06-27.
**Tooling:** `pdftotext -layout` (content), PyMuPDF (images), verbatim copy (code).

## Text-layer integrity
- `pdftotext -f1-l1` sample: **clean** (only cosmetic letter-spacing in the
  header/footer band — `sa le s@…`, `ph on e:`). Body text decodes correctly. **Not ciphered;
  OCR not required.**
- Full extract: **2,737 lines** to `AN013-WMF-Menus-text.txt`. All 49 page footers present
  ("…Framework v1.0  N of 49"); no page gaps.

## Pass-by-pass results

| Pass | Output | Result |
|------|--------|--------|
| 1 Content | `AN013-WMF-Menus-text.txt` (raw) + `complete-AN013-reference.md` (curated) | ✅ complete — 14 authored sections + 4-demo walkthrough + full API listing captured; prose voice/structure profile recorded |
| 2 Code | `assets/code-2026-06-27/` (12 `.spin`) + `code-catalog.md` | ✅ captured + cataloged · ❌ **NOT validated** (`code_validated:false`, no P1 compiler — charter §3) |
| 3 Images | `assets/images-AN013-WMF-Menus-2026-06-27/` (26 PNG) + `image-catalog.md` | ✅ 26 fragments → 17 figures; quality-gate all healthy; no OCR needed (screenshots legible) |
| 4 Post-proc | (light) constants/message tables consolidated into the curated md | ✅ N/A for P1 stage-only — no central P2 matrices touched |
| 5 Validation | this file | ✅ |

### Content coverage checklist
- [x] Introduction + GUI/event-driven philosophy
- [x] Architecture: WMF single-object model, text-GUI 800×600/8×12/100×50, object & data-flow models
- [x] Controls & events model (data-driven DAT, message queue producer/consumer)
- [x] Buttons: 6 fields, DAT format, ATTR/STYLE flags, IDs, Attach/Detach/Draw
- [x] HotBar: header, width formula, ASCII filler constants, item list
- [x] HotList: header, simplified width, hotbar/hotlist interchangeability
- [x] Attaching controls + NUM_* limits + DrawButton/DrawHotMenu commands
- [x] Application template + CreateAppGUI + Init packed-return decode
- [x] Main event loop + messaging API + message format + all WMF_MSG_* codes
- [x] 4 demos (Button/Button2, HotBar, HotList, MultiControl) + hardware (LEDs/motor/DTMF)
- [x] Event-handler model (Fig 17), routing-by-ID-range, handler guidelines
- [x] Full API listing (8 method groups), Resources, References, Revision History
- [x] Box-drawing ASCII constants, color themes (CTHEME_AUTUMN_*), filter idiom

### Code capture
12/12 files copied byte-for-byte (6,884 LOC total). Dependency tree resolved
(6 top-level demos → `WMF_Framework_010` → VGA/Mouse/Keyboard; MultiControl adds sound + PWM).
4 shared drivers (Keyboard_011, Mouse_011, VGA_HiRes_Text_010, WMF_Framework_010) are the same
stack shipped with AN004 — each AN keeps its own copy (self-containment; do NOT de-dup).

### Image capture
26 raster fragments cover all 17 numbered figures (Figs 1–17). Several wide diagrams/photos
stored as 2–4 horizontal slices (Fig 1, 2, 3, 16, 17). All pass dominant-color + dimension
quality gate (no black-failure, no full-page mis-capture). Fragment re-assembly = deferred
image-enhancement debt (not blocking).

## Caveats / known gaps
- **No code validation** — inherent to P1 in this container; not a defect, a charter constraint.
- A handful of doc minor inconsistencies (authorial, in original): Resources list names
  `WMF_HotBarDemo_010` / `WMF_HotListDemo_010` / `pwmasm_010` while the ZIP ships
  `WMF_HotBarMenuDemo_010` / `WMF_HotListMenuDemo_010` / `pwmAsm_010` (case/name drift in the
  app note's own Resources section — recorded, not corrected; affects nothing in our capture).
- The PDF's `www.parallaxsemicondutor.com/an013` (typo, missing 'c') is reproduced as-authored.

## Auth tier & scoring (proposed — reduce confirms)
- **Authority:** 🏆 Parallax primary (official Parallax Semiconductor application note + the
  author-distributed companion source ZIP).
- **C·K·I·A·X:** **C**ontent ✅ · **K**nowledge/code ✅(captured, unvalidated) · **I**mages ✅ ·
  **A**udit ✅ · **X**-ref (pass 6 Q&A) deferred to reduce.
- **Completeness:** **~95%** (everything authored is extracted; the residual 5% is the
  uncompilable-here code-validation leg, structurally unavailable for P1).
