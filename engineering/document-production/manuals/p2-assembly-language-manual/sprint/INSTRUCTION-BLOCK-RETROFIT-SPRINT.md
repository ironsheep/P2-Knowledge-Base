# Instruction Block Retrofit Sprint

**Sprint Goal:** Retrofit all Part II instruction blocks with consistent formatting, correct links, and color bar visual anchors.

**Sprint Type:** Mini-sprint (single-pass retrofit)

**Created:** 2025-12-04

---

## Executive Summary

This sprint retrofits all ~290 instruction entries plus directives and constants in Part II of the P2 Assembly Language Reference Manual. All changes are made in a single pass per file to minimize PDF generation runs.

---

## Final Color Selections

| Entry Type | Color Name | Hex Code | Purpose |
|------------|------------|----------|---------|
| **Instructions** | Brick Red | `#C62828` | Primary content - most visually dominant |
| **Directives** | Amber 600 | `#FF8F00` | Assembly-time commands |
| **Constants** | Violet 600 | `#8E24AA` | Reference values (matches syntax highlighting) |

---

## Changes Per Instruction Block

Each instruction block will be updated with ALL of the following in a single edit pass:

### 1. Header Format Verification
Ensure the 5-line identity block structure:
```markdown
## MNEMONIC {#anchor}

Mnemonic Expansion (Title Case)

[Category](#category-anchor) - Single-line description.

**MNEMONIC** *params* **{flags}**
```

**⚠️ Expansion Line Rule:** If a word in the expansion happens to match the mnemonic, it must use normal Title Case, NOT ALL-CAPS. The expansion is readable English prose, not a repetition of the mnemonic.

**Correct:**
- `## CALL {#call}` followed by `Call Subroutine` ✅
- `## TEST {#test}` followed by `Test Bits` ✅

**Incorrect:**
- `## CALL {#call}` followed by `CALL Subroutine` ❌
- `## TEST {#test}` followed by `TEST Bits` ❌

### 2. Category Name Normalization
- **Convert** all non-standard category names to the 17 defined categories
- Ensure anchor matches exactly
- This is a NORMALIZATION pass - existing variant names must be converted

**Valid Categories (17 total):**
| Category | Anchor | Common Variants to Convert |
|----------|--------|---------------------------|
| Branch | `#branch` | Branching, Jump, Flow Control |
| CORDIC Solver | `#cordic-solver` | CORDIC, Cordic, Math Coprocessor |
| Color Space Converter | `#color-space-converter` | Color, RGB, Colorspace |
| Event | `#event` | Events, Event Handling |
| Hub Control | `#hub-control` | Hub, Hub Operations |
| Hub FIFO | `#hub-fifo` | FIFO, Hub FIFO Operations |
| Hub RAM | `#hub-ram` | Memory, RAM, Hub Memory |
| Interrupt | `#interrupt` | Interrupts, INT, IRQ |
| Lookup Table | `#lookup-table` | LUT, Lookup, Table |
| Math and Logic | `#math-and-logic` | Math, Logic, ALU, Arithmetic |
| Miscellaneous | `#miscellaneous` | Misc, Other, General |
| Pin | `#pin` | Pins, I/O, GPIO, Pin I/O |
| Pixel Mixer | `#pixel-mixer` | Pixel, Graphics, Video |
| Register Indirection | `#register-indirection` | Indirection, Register, Indirect |
| Smart Pin | `#smart-pin` | Smart Pins, SmartPin |
| Streamer | `#streamer-category` | Stream, DMA, Streaming |
| System Control | `#system-control` | System, Control, Configuration |

**⚠️ CRITICAL**: Any category name NOT in this list must be converted to the closest match.

### 3. Related Links Fix
- All related links must resolve to existing anchors
- Many-to-one mapping: multiple instructions can link to one block anchor
- Create instruction → anchor mapping table first

### 4. Color Bar Wrapper
Wrap the 3-line identity block with entry type environment. The div contains exactly 3 consecutive lines with NO blank lines between them.

**For Instructions:**
```markdown
::: instrheader
## MNEMONIC {#mnemonic}
Mnemonic Expansion
Category: [Category Name](categories.md#anchor)
:::

**MNEMONIC** *Dest, {#}Src* **{WC|WZ|WCZ}**

---

**Result:** ...
```

**For Directives:**
```markdown
::: dirheader
## DIRECTIVE {#directive}
Directive Expansion
Category: [Directives](directives.md#directives)
:::

**DIRECTIVE** *operands*

---

**Result:** ...
```

**For Constants:**
```markdown
::: constheader
## CONSTANT_NAME {#constant_name}
Constant Expansion
Category: [Constants](constants.md#constants)
:::

**Value:** $xxxx_xxxx

---

**Usage:** ...
```

**Key Points:**
- The div contains exactly 3 consecutive lines (NO blank lines inside)
- Line 1: H2 heading with `{#anchor}`
- Line 2: Expansion in Title Case (e.g., "Add Signed" not "ADD Signed")
- Line 3: Category line with link
- The `:::` close tag comes immediately after line 3
- Syntax line(s), horizontal rule, and all content stay OUTSIDE the div

---

## Implementation Phases

### Phase 1: Preparation (No PDF Generation)

**1.1 Category Audit**
- Scan all instruction files for current category names
- Identify non-standard categories needing normalization
- Create mapping: current name → normalized name
- Output: List of all category conversions needed

**1.2 Create Instruction → Anchor Mapping Table**
- List all multi-instruction blocks
- Map each instruction name to its block's primary anchor
- Example: BITNC → #bitc, BITZ → #bitc, BITNZ → #bitc

**1.3 Update Template with Final Color Bar Environments**
- Add `instrheader`, `dirheader`, `constheader` environments to `p2kb-pasm2-content.sty`
- Use final colors: #C62828, #FF8F00, #8E24AA
- 4pt bar width, 10pt left padding

**1.4 Create/Update Lua Filter**
- Convert `::: instrheader` → `\begin{instrheader}...\end{instrheader}`
- Handle all three entry types

**1.5 Audit Instruction Format Chapter**
- Review Part I Chapter 2 (Instruction Format Overview)
- Add explanation of color bar visual anchors
- Document what each color means (red=instruction, amber=directive, violet=constant)
- Ensure readers understand the visual cues before encountering them in Part II

**1.6 Create Validation Checklist**
Per-block checklist for single-pass editing

---

### Phase 2: Single Pass Retrofit (No PDF Generation Yet)

Edit each instruction file in `opus-master/part-ii/` exactly once:

| File | Entry Count | Content |
|------|-------------|---------|
| `instructions-a.md` | ~20 | ABS through AUGD |
| `instructions-b.md` | ~15 | BITC through BRK |
| `instructions-c.md` | ~25 | CALL through CRCNIB |
| `instructions-d.md` | ~15 | DECMOD through DRVNOT |
| `instructions-e.md` | ~5 | ENCOD through EXECF |
| `instructions-f.md` | ~10 | FBLOCK through FLE |
| `instructions-g.md` | ~10 | GETBRK through GETWORD |
| `instructions-h.md` | ~2 | HUBSET |
| `instructions-i.md` | ~5 | INCMOD through IJNZ |
| `instructions-j.md` | ~10 | JMP through JNXROT |
| `instructions-k.md` | ~2 | (if any) |
| `instructions-l.md` | ~10 | LOCKNEW through LTIX |
| `instructions-m.md` | ~20 | MERGEB through MUXZ |
| `instructions-n.md` | ~10 | NEG through NOP |
| `instructions-o.md` | ~10 | OR through OUTL |
| `instructions-p.md` | ~15 | POLLATN through PUSH |
| `instructions-q.md` | ~10 | QDIV through QVECTOR |
| `instructions-r.md` | ~30 | RCZL through RQPIN |
| `instructions-s.md` | ~50 | SAL through SUMNZ |
| `instructions-t.md` | ~15 | TEST through TRGINT |
| `instructions-w.md` | ~15 | WAITATN through WXPIN |
| `instructions-x.md` | ~10 | XCONT through XZERO |
| `instructions-z.md` | ~5 | ZEROX |
| `directives.md` | ~15 | ORG, ORGF, BYTE, etc. |
| `constants.md` | ~50+ | P_HIGH_15K, etc. |

**Per-File Process:**
1. Open file
2. For each entry block:
   - [ ] Verify header format (5 lines)
   - [ ] **Fix expansion line** - ensure Title Case, no ALL-CAPS mnemonic echoes
   - [ ] **Normalize category name** to one of 17 valid categories
   - [ ] Fix category anchor to match normalized name
   - [ ] Verify/fix related links
   - [ ] Add color bar wrapper
3. Save file
4. Move to next file

**Expansion Line Fixes:**
- `CALL Subroutine` → `Call Subroutine`
- `TEST Bits` → `Test Bits`
- `ADD Unsigned` → `Add Unsigned`

**Category Normalization Examples:**
- `[Math](#math)` → `[Math and Logic](#math-and-logic)`
- `[Pin I/O](#pin-io)` → `[Pin](#pin)`
- `[Branching](#branching)` → `[Branch](#branch)`
- `[CORDIC](#cordic)` → `[CORDIC Solver](#cordic-solver)`

---

### Phase 3: Assembly & Test (1 PDF Generation)

**3.1 Concatenate to Workspace**
```bash
# Concatenate all parts to workspace document
cat front-matter.md \
    part-i/*.md \
    part-ii/instruction-categories.md \
    part-ii/instructions-*.md \
    part-ii/directives.md \
    part-ii/constants.md \
    part-ii/special-registers.md \
    part-iii/*.md \
    > ../../workspace/p2-assembly-language-manual/P2-Assembly-Language-Manual.md
```

**3.2 Escape to Outbound**
```bash
../../../tools/conversion/latex-escape-all.sh \
    P2-Assembly-Language-Manual.md \
    ../../outbound/p2-assembly-language-manual/P2-Assembly-Language-Manual.md
```

**3.3 Copy Modified Templates**
```bash
cp templates/p2kb-pasm2-content.sty ../../outbound/p2-assembly-language-manual/
```

**3.4 Generate PDF**
- Deploy to PDF Forge
- Single generation run (~10 minutes)

---

### Phase 4: Visual Audit

Review the generated PDF for:
- [ ] Color bars appear correctly on all entries
- [ ] Bar colors match entry types (red=instruction, amber=directive, violet=constant)
- [ ] Header format consistent across all entries
- [ ] No broken internal links
- [ ] Visual hierarchy is clear

---

### Phase 5: Fixes (If Needed)

If issues found:
1. Fix in opus-master source files
2. Re-concatenate
3. Re-escape
4. Second PDF generation (target: maximum 2 total runs)

---

## Deliverables

1. **Updated source files** in `opus-master/part-ii/`
2. **Updated template** `p2kb-pasm2-content.sty` with color bar environments
3. **Instruction → Anchor mapping table** (reference document)
4. **Validated PDF** with all formatting correct

---

## Success Criteria

- [ ] All ~290+ entries have correct 5-line header format
- [ ] All category links use only the 17 defined categories
- [ ] All related links resolve to valid anchors
- [ ] All entries have appropriate color bar (red/amber/violet)
- [ ] Maximum 2 PDF generation runs
- [ ] Visual audit passes

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Multi-instruction blocks break related links | Create mapping table BEFORE editing |
| Color bars don't render | Test template in isolation first (done) |
| Too many PDF runs | Single-pass editing, thorough preparation |
| Missing entries | Use file inventory to track completion |

---

## Schedule

This is a focused mini-sprint. Estimated effort:
- Phase 1 (Preparation): 1-2 hours
- Phase 2 (Retrofit): 4-6 hours (single pass through all files)
- Phase 3 (Assembly & Test): 30 minutes + 10 min PDF generation
- Phase 4 (Visual Audit): 30 minutes
- Phase 5 (Fixes): 0-2 hours if needed

**Total: 6-10 hours of work, 1-2 PDF generation runs**

---

*Sprint Created: 2025-12-04*
*Status: Ready for Execution*
