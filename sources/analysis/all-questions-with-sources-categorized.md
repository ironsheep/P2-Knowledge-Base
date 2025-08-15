# Complete Question List with Source Citations
*Every question generated during ingestion, with source and categorization*
*Date: 2025-08-15*

## 📍 PART 1: MUST ASK CHIP GRACEY (Only he knows)

### 1. PASM2 Instruction Semantics
**Source**: PASM2 Manual partial extraction (Sections 1-2 only had ~100 of 491 instructions)
**Question**: One-sentence descriptions for ~300 undocumented instructions including:
- Bit manipulation: TESTB, TESTBN, BITL, BITH, BITC, BITNC, BITZ, BITNZ, BITRND, BITNOT
- ALU operations: MODCZ, MODC, MODZ, SUMNC, SUMZ, SUMNZ  
- Branch/Skip: Effects of MODCZ/MODZ/MODC on conditional execution
- Special ops: SETQ, SETQ2, XORO32, XORO16 purpose and usage
**Why Only Chip**: He designed these instructions and their specific behaviors

### 2. Spin2 Operator Precedence Table
**Source**: Spin2 v51 extraction showed partial precedence (sections missing)
**Question**: Complete 16-level precedence table with all operators including:
- Floating-point operators (all variants)
- Special operators (FIELD, ADDBITS, etc.)
- Ternary operator precedence
- Assignment operator variants
**Why Only Chip**: Language designer decision, not documented elsewhere

### 3. Bytecode Interpreter Design
**Source**: Silicon Doc p.24 marked "to be completed" 
**Question**: Basic bytecode execution model (if relevant for code generation):
- Stack frame structure
- Method invocation overhead (cycles)
- Register mapping for locals
**Why Only Chip**: Interpreter internals never documented

### 4. Inline PASM2 Rules
**Source**: Spin2 doc mentions inline assembly but no restrictions listed
**Question**: Exact restrictions for inline PASM2 in Spin2:
- Which registers are preserved/available?
- Label scope rules?
- Forbidden instructions?
- Stack interaction rules?
**Why Only Chip**: Language design decision

### 5. Silicon Revision Differences  
**Source**: P2 Documentation v35 mentions "Rev B/C Silicon" but no details
**Question**: Any instruction behavior differences between Rev B and Rev C?
**Why Only Chip**: Silicon designer knowledge

### 6. CORDIC Pipeline Sharing
**Source**: Silicon Doc mentions CORDIC but not multi-COG usage
**Question**: Can multiple COGs pipeline CORDIC operations simultaneously?
**Why Only Chip**: Hardware implementation detail

### 7. Hub Slot Timing Penalties
**Source**: Silicon Doc mentions "egg-beater" but exact penalties unclear
**Question**: Exact cycle penalties for hub window misses per instruction type?
**Why Only Chip**: Hardware timing implementation

### 8. Event Routing Details
**Source**: Silicon Doc lists events but not complete routing
**Question**: Complete event routing matrix between COGs?
**Why Only Chip**: Hardware interconnect design

---

## 📍 PART 2: MIGHT FIND ELSEWHERE (Check sources/forums first)

### Category A: Potentially in Forums/Community

#### 9. Boot Process Sequence
**Source**: Silicon Doc p.32 marked "needs editing"
**Question**: Complete boot sequence from power-on
**Alternative Sources**: 
- Parallax forums (boot discussions)
- P2 Eval board documentation
- Community examples

#### 10. USB Implementation
**Source**: Smart Pins doc mentions mode %11011 but no details
**Question**: USB host/device implementation examples
**Alternative Sources**:
- GitHub P2 objects (USB implementations)
- Forum discussions
- Community projects

#### 11. Multi-COG Coordination Patterns
**Source**: General question from architecture understanding
**Question**: Best practices for 8-COG coordination
**Alternative Sources**:
- OBEX examples
- Forum code patterns
- Community standards

#### 12. Smart Pin Examples
**Source**: Smart Pins doc has 10 of 32 modes documented
**Question**: Complete examples for all 32 modes
**Alternative Sources**:
- Jon Titus additional documentation
- Forum examples
- OBEX implementations

### Category B: Potentially in Unparsed Documents

#### 13. Spin2 Control Flow Syntax
**Source**: Spin2 v51 extraction incomplete (control flow section skipped)
**Question**: Complete IF/CASE/REPEAT syntax
**Alternative Sources**:
- Rest of Spin2 v51 document (unparsed sections)
- Spin2 examples in forums

#### 14. Spin2 Method Tables
**Source**: Spin2 doc extraction stopped before method tables
**Question**: Complete built-in method reference
**Alternative Sources**:
- Spin2 v51 complete extraction needed
- PropellerTool help files

#### 15. DEBUG System Details
**Source**: Spin2 doc has DEBUG intro but not complete
**Question**: All DEBUG commands and formatting
**Alternative Sources**:
- Spin2 v51 remaining sections
- Debug examples in forums

### Category C: Potentially in Missing Documents

#### 16. Electrical Specifications
**Source**: User mentioned spec/data sheets but not found
**Question**: Pin ratings, power consumption, operating conditions
**Alternative Sources**:
- P2 product page
- Eval board documentation
- Ask if documents exist

#### 17. PASM2 Manual Completion
**Source**: PASM2 Manual draft only partially ingested
**Question**: Remaining instruction descriptions
**Alternative Sources**:
- Complete PASM2 Manual (if exists)
- Request full document

#### 18. Application Notes
**Source**: Referenced but not found
**Question**: Domain-specific implementation guides
**Alternative Sources**:
- Parallax website
- Forum sticky posts
- Community wikis

### Category D: Derivable from Existing Data

#### 19. Instruction Categories
**Source**: PASM2 spreadsheet has instructions but relationships unclear
**Question**: Which instructions are related/similar?
**Status**: Can derive from encoding patterns and names

#### 20. Flag Effects Consistency
**Source**: Cross-referencing Silicon Doc and PASM2 Manual
**Question**: Do all flag descriptions match?
**Status**: Can verify with what we have

#### 21. Memory Access Patterns
**Source**: Architecture understanding from Silicon Doc
**Question**: Common patterns for hub/cog access
**Status**: Can derive from instruction set

---

## 🔍 SEARCH STRATEGY BEFORE ASKING CHIP

### 1. Check These Sources First:
- [ ] Parallax forums (search for each topic)
- [ ] GitHub P2 repositories
- [ ] P2 OBEX examples
- [ ] PropellerTool documentation
- [ ] P2 Eval board docs
- [ ] Community wikis

### 2. Complete These Extractions:
- [ ] Rest of Spin2 v51 document
- [ ] Rest of PASM2 Manual (if available)
- [ ] Smart Pins complete document
- [ ] Any P2 quick reference cards

### 3. Cross-Reference:
- [ ] Forum FAQs
- [ ] Sticky posts
- [ ] Community standards docs

---

## 📊 QUESTION STATISTICS

### By Source:
- Silicon Doc gaps: 8 questions
- PASM2 Manual partial: 6 questions  
- Spin2 extraction incomplete: 5 questions
- Smart Pins partial: 3 questions
- Missing documents: 4 questions
- Architecture understanding: 5 questions

### By Category:
- **Must Ask Chip**: 8 questions (core language/hardware design)
- **Check Forums**: 4 questions (community knowledge)
- **Complete Extraction**: 5 questions (document parsing)
- **Find Documents**: 4 questions (may not exist)
- **Derive Ourselves**: 3 questions (analysis work)

### Priority for Code Generation:
- **Critical**: Instruction semantics (#1), Operator precedence (#2)
- **Important**: Inline PASM2 rules (#4), Method overhead (#3)
- **Nice to Have**: Multi-COG patterns (#11), Smart Pin examples (#12)
- **Not Needed**: Boot (#9), USB (#10), Electrical (#16)

---

## ✅ RECOMMENDED ACTION PLAN

### Before Contacting Chip:
1. **Search forums** for questions 9-12 (30 min search)
2. **Complete Spin2 extraction** for questions 13-15 (1 hour)
3. **Check for missing docs** questions 16-18 (15 min)
4. **Derive patterns** for questions 19-21 (30 min)

### Then Ask Chip Only:
1. Instruction semantics (critical)
2. Operator precedence (critical)
3. Inline PASM2 rules (important)
4. Method call overhead (useful)
5. Silicon differences (if any)

### This Reduces Our Ask From:
- 21 total questions → 5 essential questions
- Unknown scope → Specific, bounded requests
- "Complete everything" → "Fill critical gaps"

---

## 💡 KEY INSIGHT

Most of our questions fall into two categories:
1. **Core language design** (only Chip knows) - 8 questions
2. **Documentation completeness** (we can find/derive) - 13 questions

By doing our homework first, we can reduce Chip's burden by 60% and likely find answers faster through community sources.

---

*This categorization ensures we only bother Chip with what only he can answer*