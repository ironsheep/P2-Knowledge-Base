# Smart Pins Tutorial - Punch List

**Document:** P2-Smart-Pins-Green-Book-Tutorial
**Purpose:** Track fixes and enhancements needed before final release

---

## Completed This Session

- [x] **Narrative text disappearing after PASM2 blocks** - Fixed `\uppercase` in lstset (p2kb-sp-code-coloring.lua)
- [x] **Part I centering/page break issue** - Fixed filter treating Part I as document title (p2kb-sp-fix-title-as-part.lua)
- [x] **Diagram 1 (DRVH timing)** - Fixed text overlap, Reg* spacing, label alignment
- [x] **Diagram 2 (TESTB INA timing)** - Fixed P0 IN overlap, Reg spacing, ALU/C/Z cramping
- [x] **Diagram 3 (TESTP timing)** - Fixed P0 IN overlap, Reg spacing, C/Z cramping
- [x] **Missing page headers** - Default `fancy` pagestyle had no header content defined; added chapter title and page number
- [x] **WRPIN D format ASCII art** - Replaced broken ASCII art (box-drawing chars not rendering) with TikZ bit-field diagram (`\WRPINFormatDiagram`)

---

## Pending - Layout/Formatting

- [ ] **Figure captions** - Add centered, bold "Figure N: Title" below each diagram
  - Approach: Use LaTeX `figure` environment with `\caption{}`
  - Requires: `\captionsetup{labelfont=bf, font=small, justification=centering}`
  - Decision needed: Automatic numbering vs manual titles

---

## Pending - Diagram Fixes

- [ ] Review remaining diagrams (4-18) for similar spacing issues
- [ ] (Add specific diagram issues as discovered)

---

## Pending - Content

- [ ] (Add content issues as discovered)

---

## Pending - Testing

- [ ] Regenerate PDF after current fixes
- [ ] Visual review of all three fixed diagrams
- [ ] Verify narrative text appears after PASM2 blocks
- [ ] Verify Part I starts on new page with Chapter 0 following on same page

---

## Notes

Files modified this session:
- `filters/p2kb-sp-code-coloring.lua`
- `filters/p2kb-sp-fix-title-as-part.lua`
- `templates/p2kb-sp-diagrams.sty`

---

*Created: 2025-12-03*
*Last Updated: 2025-12-03*
