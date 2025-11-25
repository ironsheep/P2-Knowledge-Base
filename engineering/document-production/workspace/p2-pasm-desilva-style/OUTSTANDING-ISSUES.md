# Outstanding Issues - P2 PASM DeSilva Style

Issues to address in next session.

## Visual/Layout Issues

### 1. Cover Page Improvements
**Screenshot:** `outbound/Screenshot 2025-11-24 at 17.53.17.png`

**Issues identified:**
- **Green box too bright** - The "Tutorial Philosophy" box uses a very bright green that's harsh on the eyes. Consider a darker/muted green (forest green, sage, or similar).
- **Color legend incomplete** - Shows 5-color code system (Green=Spin2, Yellow=PASM2, Purple=CORDIC, Blue=Multi-COG, Red=Antipattern) but doesn't mention other pedagogical blocks used in the manual:
  - Sidetracks (gray dashed border)
  - Interludes (gray, no border)
  - Your Turn exercises (light blue)
  - Medicine Cabinet (quick tips)
  - Chapter Celebrations (green tinted)
- **Consider:** Should the cover mention these other block types, or is the 5-color code system sufficient for the cover?
- **Color consistency:** Verify the actual colors used in the document match what's described on cover

**Location:** Title page defined in `p2kb-desilva.latex` or content layer

---

### 2. "Further Reading" on Same Line as Preceding Text
**Problem:** In PDF output, "(But really, just the beginning…) ## Further Reading" appears on one line.

**Cause:** Demoted from `#` (chapter) to `##` (section), may need blank line or page break before it.

**Fix:** Check markdown for proper blank lines before `## Further Reading`, or consider if it should remain a chapter.

---

### 2. Chapter Heading Vertical Space (PRIORITY)
**Problem:** Chapter headings still have ~1 inch whitespace above them despite attempts to fix with `titlesec`.

**Affected elements:**
- Chapter headings (e.g., "Chapter 1: Your First PASM2 Program")
- Dedication and Acknowledgements
- Preface ("Welcome to the Journey")

**What we tried:**
- `\titleformat{\chapter}` and `\titlespacing*{\chapter}{0pt}{0pt}{12pt}` in `p2kb-desilva-foundation.sty`
- Removed manual `\@makechapterhead` redefinition

**Next steps:**
- Investigate if book class `\chapter` command has hardcoded space that `titlesec` isn't overriding
- Check if dedication/preface use different commands that need separate handling
- May need to look at the actual LaTeX output to see what's generating the space

---

## Content/Technical Issues

### 2. SETQ Instruction Description
**Problem:** Document references SETQ as setting a "Q register" but this may be inaccurate.

**Current text location:** Needs to be found and verified

**Technical question:** Does SETQ:
- Set an associated Q register? OR
- Modify the following instruction directly?

**Action:**
1. Look up SETQ in YAML knowledge base or silicon docs
2. Verify correct behavior
3. Update document text accordingly

---

## Session Notes

Last session: 2025-11-25
- Fixed mnemonic filter word boundary (`long_d` issue)
- Added TikZ diagrams (COG, Hub, Egg Beater, Instruction Anatomy)
- Converted Interrupt Horror Stories to tables
- Demoted Appendix A to "Further Reading" section
- Renamed working copy to `P2-PASM-deSilva-Style.md`
