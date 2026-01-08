# PASM2 Manual User Review Sprint

**Status**: UPCOMING  
**Reviewer**: Rayman  
**Review Date**: 2025-12-24  
**Sprint Created**: 2026-01-03  
**Target Document**: P2 Assembly Language Reference Manual (Opus Master)

---

## Sprint Overview

This sprint addresses user feedback from Rayman's review of the P2 Assembly Language Reference Manual. The review identified factual errors, valid improvements, and design choices requiring discussion.

**Document Location**: `engineering/document-production/workspace/p2-assembly-language-manual/P2-Assembly-Language-Manual.md`

---

## Work Categories

### Category A: Factual Errors (MUST FIX)

These are incorrect statements that must be corrected:

| ID | Section | Current Text | Correction | Source Reference |
|----|---------|--------------|------------|------------------|
| A1 | 1.4.1 (line 382) | "single-cycle access like COG RAM" | RDLUT is **3 clocks**, not single-cycle | `deliverables/ai/P2/language/pasm2/rdlut.yaml` - `clocks: '3'` |
| A2 | Key Concepts (line 451) | "single-cycle execution for most instructions" | Should be **2-cycle** (pipeline throughput) | P2 pipeline is 2-stage |

---

### Category B: Document Is Correct (USER INCORRECT)

These items require NO changes - document is technically accurate:

| ID | User Claim | Our Position | Evidence |
|----|------------|--------------|----------|
| B1 | "LUT sharing" not just "write sharing" | **Write-only** sharing is correct | `setluts.yaml`: "LUT writes...are copied to this cog's LUT" |
| B2 | "concurrently" better than "simultaneously" | **Simultaneously** is correct | True parallel execution, not time-slicing |
| B3 | "every eighth clock" is P1-style | **Egg-beater applies to P2** | `architecture-extractor.py`: 8-clock window rotation |

**Response to User**: Prepare brief explanations for these items if user questions them.

---

### Category C: Valid Improvements (ACCEPT)

These suggestions improve the document without changing technical accuracy:

| ID | Section | Change Description |
|----|---------|-------------------|
| C1 | All figures | Add figure numbering system (Figure 1.1, 1.2, etc.) |
| C2 | 1.1.2 (line 305) | Change to "COGs **can** communicate **with each other** through shared Hub memory" |
| C3 | 1.1.2 (line 305) | Change "signal another COG" to "signal **other COGs**" (COGATN uses bitmask for multiple) |
| C4 | 1.3.3 | Add RDFAST/WRFAST and CORDIC to Hub Instructions section |
| C5 | 1.4.1 | Add paletted VGA as LUT application example |
| C6 | 1.3.1 (line 351) | Add caveat about accessing hub addresses below $400 |
| C7 | Key Concepts | Add "however complete interrupt mechanisms are provided" after interrupt statement |

---

### Category D: Design Choices (DISCUSS WITH USER)

These are valid suggestions but represent stylistic/organizational preferences:

| ID | Suggestion | Considerations |
|----|------------|----------------|
| D1 | Remove LUT sharing from overview diagram | User says "advanced feature whose practical use may be limited" |
| D2 | Simplify "memory and registers" wording | In P2 context, COG RAM locations ARE registers - somewhat redundant |
| D3 | Reorder sections: LUT (1.4) before Hub (1.3) | Pedagogical choice - LUT is more similar to COG; Hub is more fundamental |
| D4 | Clarify hubexec typically uses ORGH ($400+) | Text is technically correct but may be misleading |
| D5 | Add "private" emphasis to LUT description | Each COG has its own LUT (sharing is optional via SETLUTS) |
| D6 | Change "deterministic" to "predictable" for Hub timing | Timing IS deterministic (0-7 clocks) but variable per access |
| D7 | Add explicit P1 vs P2 differences section | Front matter references differences but doesn't enumerate them |

---

### Category E: Visual/Diagram Verification

These require checking the rendered PDF output:

| ID | Issue | Location |
|----|-------|----------|
| E1 | Bracket orientation in COG memory map | `templates/p2kb-pasm2-diagrams.sty` - CogMemoryMapDiagram |
| E2 | PTRA/PTRB grouping with Special registers | Same diagram |
| E3 | R/W annotations (unnecessary if all are R/W?) | Same diagram |

---

### Category F: Needs Clarification

| ID | User Comment | Status |
|----|--------------|--------|
| F1 | "Maybe 'special pointer'" | Context unclear - defer until user clarifies |

---

## Questions to Resolve Before Sprint

1. **D1**: Should LUT sharing be removed from the overview diagram?
2. **D3**: Prefer LUT before Hub, or keep current order?
3. **D7**: How detailed should P1 vs P2 comparison be?
4. **E1-E3**: Need to render PDF and visually verify diagram issues
5. **F1**: What did "special pointer" refer to?

---

## Execution Plan

### Phase 1: Factual Corrections
- [ ] Fix A1: LUT timing (3 clocks, not single-cycle)
- [ ] Fix A2: Pipeline timing (2-cycle, not single-cycle)

### Phase 2: Accepted Improvements
- [ ] C1: Implement figure numbering
- [ ] C2: Reword COG communication phrase
- [ ] C3: Pluralize COGATN target
- [ ] C4: Expand Hub Instructions section
- [ ] C5: Add paletted VGA example
- [ ] C6: Add low hub address caveat
- [ ] C7: Add interrupt mechanism clarification

### Phase 3: Design Decisions (After Discussion)
- [ ] Resolve D1-D7 with user input
- [ ] Implement agreed changes

### Phase 4: Visual Verification
- [ ] Render PDF
- [ ] Verify E1-E3 diagram issues
- [ ] Fix any confirmed problems

### Phase 5: Validation
- [ ] Full document review
- [ ] Regenerate PDF
- [ ] User approval

---

## Original User Feedback (Raw)

Preserved verbatim for reference:

```
It might be useful if the figures had numbers, so can be referred to.

The very first figure says "LUT write sharing". But, I think it's both read and write, so maybe just "LUT sharing"?
Also, I might not even show this in the very first figure. That's kind of an advanced feature whose practical use may be limited...

After that, "Executes instructions independently and simultaneously". I'm questioning the "simultaneously"... Maybe concurrently is better?

Then, "Has its own dedicated memory and registers". I'm thinking memory and registers are basically the same thing, right?

"COGs communicate through shared Hub memory," might be better as "COGs can communicate with each other through shared Hub memory,"

"allows one COG to signal another COG" might be more precise as "allows one COG to signal other COGs", because can signal multiple cogs at once...

The cog memory map figure has multiple issues. the brackets are flipped horizontally. Special should include ptra and ptrb. I think everything is read/write, so not sure why that is there...

Maybe "special pointer"

I'm feeling like the LUT section 1.4 should come before the HUB section 1.3...

"Each COG receives a dedicated access window every eighth clock cycle. "
I think this is the P1 way. Pretty sure P2 has hub memory access on every clock...

"Hub Instructions" Seems should mention RDFAST/WRFAST here as well...

Actually, I think there are a lot more hub instructions... Like cordic, etc...

1.4.2 LUT Instructions
Think you need to mention here that LUT access is slower than cog access. Think it is RDLUT is 3 clocks instead of 2.

1.4.1 LUT Characteristics
Here, I would give paletted VGA as an example at the end...

1.3.1
"All eight COGs can read and write any location in this space."
This might be true but reading/writing below $400 can be tricky.

1.6.2
"Hub execution mode provides access to the full 512KB Hub address space,"
Think this is mostly false. Hubexec is generally required to use orgh so is above $400.

Key concepts is not the way I would put it

The P2 has 8 independent COGs executing in a truly parallel fashion

Each COG has 512 longs of private RAM plus 512 longs of **private LUT**

Hub memory (512KB) is shared among all COGs with predictable access timing **Think access timing is variable and not sure always deterministic from the user point of view.**

Special registers at $1F0-$1FF provide hardware I/O functions

COGs can execute from COG RAM (fast), LUT RAM (fast), or Hub RAM (larger capacity)

Hub execution uses FIFO for instruction prefetch; FIFO instructions unavailable in Hub mode

The pipeline provides **2-cycle** execution for most instructions

No interrupts are required due to true parallel execution**, however complete interrupt mechanisms are provided**

"How to use this manual"
"Review Chapter 1 for key differences between P1 and P2"
I'm thinking it would be useful to spell out differences between P1 and P2. I'm not seeing much of that here...
```

---

## Context Keys

- `review_rayman_2025-12-24_audit` - Full analysis with source references

---

## Sprint Metrics (To Be Filled)

| Metric | Value |
|--------|-------|
| Total Items | 17 |
| Factual Errors | 2 |
| Valid Improvements | 7 |
| Design Choices | 7 |
| Verification Needed | 3 |
| Clarification Needed | 1 |
| User Incorrect | 3 |

---

*Sprint plan created: 2026-01-03*  
*Ready to execute when user initiates*
