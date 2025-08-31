# Titus Smart Pins Manual - Narrative Extraction Validation Instructions

## Purpose
Ensure 100% capture of Jon Titus's pedagogical content before Green Book generation.

## STEP 1: Read Source Documents

### Primary Source
**Read**: Jon Titus Smart Pins Manual (original PDF)
- Location: `/sources/originals/` (find Smart Pins PDF)
- Focus on: Narrative explanations, not just specifications

### Current Extraction
**Read**: `/sources/extractions/smart-pins-complete-extraction-audit/extraction-audit.md`
- Note what's already captured
- Identify sections marked as extracted

## STEP 2: Perform Content Audit

### A. Narrative Content Audit (CRITICAL - Currently Missing!)

**For EACH of the 32 Smart Pin modes, verify extraction of:**

1. **Mode Introduction Narrative**
   - Look for: "This mode allows you to..." or "Use this mode when..."
   - Check extraction has: The explanatory paragraph(s) that introduce each mode
   - If missing: Re-extract the introductory text for that mode

2. **Configuration Explanations**
   - Look for: "Set X to Y because..." or "This value determines..."
   - Check extraction has: WHY each parameter is set to specific values
   - If missing: Re-extract the configuration reasoning

3. **Step-by-Step Tutorials**
   - Look for: "First, configure..." "Next, enable..." "Finally, read..."
   - Check extraction has: The teaching sequence Titus uses
   - If missing: Re-extract the tutorial flow

4. **Practical Applications**
   - Look for: "Common uses include..." or "This mode is ideal for..."
   - Check extraction has: Real-world use cases
   - If missing: Re-extract application descriptions

5. **Tips and Warnings**
   - Look for: "Note that..." "Be careful..." "Remember to..."
   - Check extraction has: Pitfalls and best practices
   - If missing: Re-extract tips and warnings

### B. Code Example Audit (Verify Completeness)

**Check**: `/sources/extractions/smart-pins-complete-extraction-audit/assets/code-*/`

1. **Count examples** - Should be 174 total
2. **Verify each example has:**
   - Complete code (compilable)
   - Comments preserved
   - Both Spin2 and PASM2 versions where applicable
   - Context explaining what it demonstrates

### C. Visual Asset Audit

**Check**: `/sources/extractions/smart-pins-complete-extraction-audit/assets/images-*/`

1. **For each mode that has diagrams in the original:**
   - Verify block diagram extracted
   - Verify timing diagram extracted (where applicable)
   - Verify signal flow diagram extracted
   - Check image quality is readable

## STEP 3: Document Findings

### Create Extraction Gap Report

**Create file**: `narrative-gaps-found.md` in this directory

**Document each gap found:**
```markdown
## Mode %00010 - DAC 124Ω, 3.3V
### Missing Content:
- Introduction narrative (pages 23-24)
- Configuration reasoning (page 25)
- Application examples text (page 26)

### Action Required:
- Re-extract pages 23-26 focusing on text
- Preserve tutorial flow and explanations
```

## STEP 4: Re-Extract Missing Content

### If Narrative Gaps Found:

1. **Use extraction tool on specific pages**
   - Target pages identified in gap report
   - Focus on text extraction, not code/tables

2. **Preserve tutorial structure**
   - Keep paragraph breaks
   - Maintain heading hierarchy
   - Preserve emphasis (bold, italic)

3. **Capture complete thoughts**
   - Don't truncate mid-explanation
   - Include preceding/following context
   - Keep examples with their explanations

## STEP 5: Validate Re-Extraction

### Final Checklist Before Green Book Generation:

- [ ] All 32 modes have introduction narratives
- [ ] All configurations have "why" explanations  
- [ ] All 174 code examples are present with context
- [ ] All diagrams are captured
- [ ] Tutorial progression is preserved
- [ ] Tips and warnings are included

## Success Criteria

✅ **Ready for Green Book generation when:**

1. **Narrative Coverage**: Every mode has teaching content, not just specs
2. **Pedagogical Flow**: Simple → complex progression intact
3. **Complete Examples**: All 174 with explanatory context
4. **Visual Assets**: All diagrams present and referenced
5. **No Gaps**: `narrative-gaps-found.md` is empty or all gaps resolved

## Output Files

After completing this validation:

1. **`narrative-gaps-found.md`** - List of any missing content
2. **`extraction-complete.md`** - Confirmation that extraction is 100%
3. **Updated extraction files** - With any re-extracted content added

## Next Step

Once validation passes:
→ Proceed to Green Book generation with Opus using the creation guide

---

**Remember**: The difference between a reference manual and a tutorial is the narrative. Without Titus's explanations, we're missing the "soul" of the Smart Pins documentation.