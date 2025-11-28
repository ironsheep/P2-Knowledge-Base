# PASM2 Manual Generation Sprint

**Sprint Name:** P2 Assembly Language Manual Generation
**Document:** P2 Assembly Language (PASM2) Manual
**Canonical Name:** `p2-assembly-language-manual`
**Sprint Start:** TBD
**Model:** Opus (throughout, including sub-agents)

---

## 1. Sprint Objective

Produce the complete P2 Assembly Language Manual from start to finish:
- Part I: Architectural Foundation (5 chapters, ~40 pages)
- Part II: Language Reference (380 entries - 359 instructions, 14 directives, 6 constants, special registers)
- Part III: Appendices (encoding tables, categorical index, reference data)
- Professional PDF output via PDF Forge

---

## 2. Source Materials

### 2.1 Primary Source: YAML Knowledge Base
**Location:** `/engineering/knowledge-base/P2/language/pasm2/`
**Count:** 380 YAML files
**Status:** Recently cleaned (v1.6.0) - flags_affected standardized, oneliners fixed

**YAML provides (authoritative):**
- Instruction/directive names
- Syntax forms and variants
- Encoding bit patterns
- Flag effects (C, Z) - standardized format
- Timing/cycle counts
- Category classification
- Related instructions
- Oneliner descriptions
- Parameters (varying detail)

**YAML varies/lacks:**
- Rich prose descriptions (~40 instructions have sparse content)
- Worked examples (only some directives have these)
- Pitfall warnings, tips, hardware notes
- Cross-references to architectural concepts

### 2.2 Secondary Source: Parallax Draft Manual
**Location:** `/engineering/ingestion/sources/pasm2-manual/`
**Document:** `P2-Assembly-Language-PASM2-Manual-Draft-221117.pdf`
**Status:** PRELIMINARY/DRAFT, ~315 instructions documented

**Parallax provides:**
- Prose descriptions for most instructions
- Some worked examples
- Architectural context
- Original voice/tone reference

### 2.3 Guide Documents
**Location:** `/engineering/document-production/manuals/p2-assembly-language-manual/`
- `creation-guide.md` - Document architecture, entry template, pedagogical framework
- `style-guide.md` - Visual formatting, typography, LaTeX conventions
- `voice-guide.md` - Writing tone, terminology standards, enhancement markers

---

## 3. Key Design Decisions

### 3.1 TikZ Diagram Strategy

All diagrams rendered as TikZ (LaTeX vector graphics) for:
- Resolution independence
- Visual consistency
- Maintainability (diagrams are code)

**Diagram Types Required:**

| Type | Count | Usage |
|------|-------|-------|
| Instruction Encoding | 359 | Every instruction entry |
| Memory Layout | ~5 | Part I, memory instructions |
| Register Maps | ~4 | Part I, special registers |
| Architecture Diagrams | ~6 | Part I chapters |
| Bit Field Diagrams | ~10 | Various |

**Markdown-to-TikZ Convention:**

Use direct LaTeX passthrough in markdown:
```markdown
```{=latex}
\InstructionEncoding{ADD}{EEEE}{0001000}{CZI}{DDDDDDDDD}{SSSSSSSSS}
```
```

This requires LaTeX macros defined in template before content generation.

### 3.2 Production Quality Standard

**Single-pass, production-ready output.** No iterative refinement passes.

Every piece of work is:
- Full production quality from the start
- Best technical accuracy possible
- Consistent voice throughout
- Camera-ready when complete

We do NOT do multiple passes with increasing quality. Head-to-tail, full quality, once.

### 3.3 Source Material Philosophy

**YAML-only approach.** Do NOT reference the Parallax draft manual.

Rationale:
- Single voice, single author feel
- No validation burden against external source
- No voice contamination from different writing style
- YAML is authoritative and recently validated (v1.6.0)
- This manual is a reinterpretation, not a derivative

The Parallax draft exists in the ingestion folder but agents should NOT read it.

### 3.4 Thin Entry Handling

~40 instructions have sparse YAML descriptions. Strategy:
1. Generate entry with available data, enhance through inference
2. Mark with: `<!-- TECHNICAL REVIEW: Description sparse, needs developer input -->`
3. Continue without stopping
4. Post-production technical review phase addresses these

### 3.5 Entry Generation Approach

**Single bulk pass** for all 380 entries:
- Maintains voice consistency
- Builds cross-reference awareness
- Efficient use of context window
- Category-aware batching within the pass

### 3.6 Part I Depth Philosophy

**Foundational, not exhaustive.**

The test for including content: "Do I need to know this to write PASM2 effectively?"
- If yes → Include it
- If interesting-but-not-actionable → Omit it

Part I teaches the mental model required to use Part II. It is not a comprehensive P2 architecture document. Readers should be able to write correct PASM2 code with this manual alone.

### 3.7 Example Strategy

**Category-based with parameter form and symbol coverage.**

Examples are NOT:
- One per instruction (too many, trivial instructions don't need them)
- One per family only (too few, misses parameter variations)

Examples ARE:
- Representative of each instruction family
- Covering different parameter forms (register, immediate, augmented, pointer)
- Demonstrating predefined symbol usage where applicable (Smart Pin symbols, COG symbols, Streamer symbols)
- Showing real usage patterns, not just syntax demonstration

This means more examples than "one per family" but targeted at what readers need to see.

### 3.8 Cross-Reference Philosophy

**Moderate density. No noise.**

Internal cross-references (within this manual):
- "Related Instructions" section in each entry
- "See Chapter X" for architectural concepts
- Keep it useful, not exhaustive

External cross-references (to other P2KB manuals):
- **Appendix only** - "Further Reading" or "Related Manuals" section
- NOT inline references like "See Smart Pins Tutorial Chapter 4"
- Positioned as "for deeper exploration" not "required reading"

### 3.9 Manual Self-Sufficiency

**This manual stands alone for its purpose.**

A reader with only this manual can:
- Understand P2 architecture sufficiently to write PASM2
- Look up any instruction and know how to use it
- Write correct, working PASM2 code

Other manuals serve different questions:
- "What does this instruction do?" → **This manual**
- "How do I accomplish this task?" → Tutorials (Smart Pins, DeSilva)
- "Why isn't my code working?" → Debug manual

The other manuals help write *better* or *more sophisticated* code. This manual is sufficient for *correct* code.

### 3.10 Chapter 2 Priority

Chapter 2 (The Instruction Format) written early because:
- Teaches readers how to interpret Part II entries
- Defines encoding diagram semantics
- Establishes terminology used throughout
- Can be written before Part II exists

---

## 4. Production Phases

### Phase 0: Design System
**Goal:** Establish all infrastructure before content generation

**Tasks:**
- [ ] Create workspace directory structure
- [ ] Design instruction encoding TikZ macro (`\InstructionEncoding{}`)
- [ ] Design memory layout TikZ macro (`\MemoryMap{}`)
- [ ] Design bit field TikZ macro (`\BitField{}`)
- [ ] Define color palette in LaTeX
- [ ] Build complete LaTeX template (`p2kb-pasm2-reference.latex`)
- [ ] Create exemplar entry (ADD instruction) with full formatting
- [ ] Test PDF generation of exemplar via PDF Forge
- [ ] Validate encoding diagram renders correctly
- [ ] Document the markdown conventions for authors

**Deliverables:**
- Working LaTeX template with all TikZ infrastructure
- Exemplar ADD entry (gold standard for all entries)
- Markdown authoring conventions document

**Validation:** PDF of ADD entry renders correctly with encoding diagram

---

### Phase 1: Part I Skeleton + Chapter 2
**Goal:** Establish architectural framework and reader orientation

**Tasks:**
- [ ] Create Part I outline (all 5 chapters)
- [ ] Identify all diagrams needed per chapter
- [ ] Write Chapter 2: The Instruction Format (complete)
  - [ ] 32-bit instruction anatomy
  - [ ] Condition codes (EEEE field)
  - [ ] How to read encoding diagrams
  - [ ] Destination/Source field semantics
  - [ ] Immediate vs Register operands
  - [ ] AUGS/AUGD for 32-bit immediates
  - [ ] How to use this manual (entry walkthrough)
- [ ] Create Chapter 2 diagrams
- [ ] Stub remaining chapters with section headings
- [ ] Document diagram placeholders for Chapters 1, 3, 4, 5

**Deliverables:**
- Part I skeleton with all chapter outlines
- Chapter 2 complete with diagrams
- Diagram inventory for remaining chapters

**Validation:** Chapter 2 makes sense standalone; reader could interpret Part II entries

---

### Phase 2: Part II - Instructions A-M
**Goal:** Generate first half of instruction entries

**Tasks:**
- [ ] Extract YAML data for instructions A-M (~180 entries)
- [ ] Generate entries following template:
  - At a Glance box
  - Syntax (all forms)
  - Parameters
  - Encoding diagram
  - Operation (prose from YAML + enhancement)
  - Timing
  - Related Instructions
  - Example (where valuable)
  - Notes (pitfalls, tips, hardware - where applicable)
- [ ] Apply voice guide consistently
- [ ] Mark thin entries for technical review
- [ ] Include encoding diagram LaTeX for each

**Deliverables:**
- Instructions A-M complete in markdown
- List of entries marked for technical review

**Validation:** Entries follow template exactly; voice is consistent

---

### Phase 3: Part II - Instructions N-Z
**Goal:** Generate second half of instruction entries

**Tasks:**
- [ ] Extract YAML data for instructions N-Z (~179 entries)
- [ ] Generate entries following same process as Phase 2
- [ ] Ensure cross-references to A-M entries work
- [ ] Mark thin entries for technical review

**Deliverables:**
- Instructions N-Z complete in markdown
- Updated technical review list

**Validation:** All 359 instructions complete; cross-references valid

---

### Phase 4: Part II - Directives, Constants, Special Registers
**Goal:** Complete non-instruction language elements

**Tasks:**
- [ ] Generate 14 directive entries (ORG, ORGH, ORGF, BYTE, WORD, LONG, RES, FIT, ALIGNL, ALIGNW, BYTEFIT, WORDFIT, DITTO, HUBEXEC)
- [ ] Generate 6 constant entries (TRUE, FALSE, PI, NEGX, POSX, COGEXEC)
  - Note: COGEXEC has variants (COGEXEC_NEW, COGEXEC_NEW_PAIR) documented within entry
  - Note: HUBEXEC has variants (HUBEXEC_NEW, HUBEXEC_NEW_PAIR) documented in directive entry
- [ ] Generate Special Registers section covering all 16 registers:
  - Dual-purpose ($1F0-$1F7): IJMP3, IRET3, IJMP2, IRET2, IJMP1, IRET1, PA, PB
  - Fixed special ($1F8-$1FF): PTRA, PTRB, DIRA, DIRB, OUTA, OUTB, INA, INB
  - Note: INA/INB also serve as debug interrupt call/return addresses
- [ ] Ensure consistent formatting with instruction entries

**Deliverables:**
- All directives, constants, special registers documented
- Part II complete

**Validation:** 380 total entries match YAML inventory

---

### Phase 5: Part I Completion
**Goal:** Write remaining architectural chapters

**Tasks:**
- [ ] Write Chapter 1: The P2 Execution Model
  - [ ] COG architecture (512 longs, 8 cogs)
  - [ ] Hub memory (512KB shared)
  - [ ] LUT memory (per-cog)
  - [ ] Execution pipeline
  - [ ] Key Concepts box
- [ ] Write Chapter 3: Flags and Conditional Execution
  - [ ] C and Z flag semantics
  - [ ] WC, WZ, WCZ effects
  - [ ] Complete IF_x condition table
  - [ ] Conditional execution patterns
  - [ ] Key Concepts box
- [ ] Write Chapter 4: Timing and Determinism
  - [ ] Clock cycles per instruction
  - [ ] Hub access windows (egg beater)
  - [ ] Deterministic timing guarantees
  - [ ] Timing-critical code patterns
  - [ ] Key Concepts box
- [ ] Write Chapter 5: Special Hardware Overview
  - [ ] CORDIC coprocessor (brief, points to instructions)
  - [ ] Smart Pins (brief, points to separate manual)
  - [ ] Streamer (brief, points to instructions)
  - [ ] Event system and interrupts
  - [ ] Key Concepts box
- [ ] Create all architectural diagrams
- [ ] Write Front Matter (How to Use, Conventions, Credits)

**Deliverables:**
- Part I complete with all diagrams
- Front matter complete

**Validation:** Part I standalone makes architectural concepts clear

---

### Phase 6: Part III - Appendices
**Goal:** Generate reference appendices from Part II data

**Tasks:**
- [ ] Generate Appendix A: Instruction Encoding Master Table
  - [ ] All 359 instructions
  - [ ] Columns: Instruction, Opcode, CZI, Cycles, C Effect, Z Effect
  - [ ] Landscape format
- [ ] Generate Appendix B: Categorical Instruction Index
  - [ ] Group by category (Math, Logic, Memory, Control, etc.)
  - [ ] Brief description per instruction
  - [ ] Enable "I need to do X" discovery
- [ ] Generate Appendix C: Special Registers Reference
- [ ] Generate Appendix D: Predefined Constants
- [ ] Generate Appendix E: Reserved Words (PASM2 + Spin2)
- [ ] Generate Appendix F: Opcode Bit Patterns

**Deliverables:**
- All appendices complete
- Part III complete

**Validation:** Appendix data matches Part II entries exactly

---

### Phase 7: Assembly and PDF Production
**Goal:** Combine all parts and produce PDF

**Tasks:**
- [ ] Assemble master markdown document
  - [ ] Front matter
  - [ ] Part I (5 chapters)
  - [ ] Part II (380 entries, alphabetical)
  - [ ] Part III (6 appendices)
- [ ] Cross-reference validation pass
  - [ ] All "Related Instructions" links valid
  - [ ] All "See Chapter X" references accurate
  - [ ] All internal hyperlinks work
- [ ] Run LaTeX escape script
- [ ] Create request.json for PDF Forge
- [ ] Deploy to PDF Forge
- [ ] Generate PDF
- [ ] Review PDF for formatting issues
- [ ] Fix any rendering problems

**Deliverables:**
- Complete master markdown
- Production PDF
- List of any issues found

**Validation:** PDF renders completely; no broken references; diagrams correct

---

### Phase 8: Parallax Gap Analysis (Post-Production)
**Goal:** Identify significant information gaps by comparing against Parallax draft

**Rationale:** The Parallax draft (~315 instructions) may contain technical details that YAML lacks. This phase catches gaps WITHOUT contaminating voice - we scan for missing *information*, then write new content in our established voice.

**Tasks:**
- [ ] For each instruction covered in Parallax draft:
  - [ ] Compare our entry against Parallax content
  - [ ] Identify any significant technical details we missed
  - [ ] Note behavioral nuances, edge cases, or usage patterns not in YAML
- [ ] For identified gaps:
  - [ ] Write new content in our established voice
  - [ ] Integrate into existing entries
  - [ ] Do NOT copy or adapt Parallax prose directly
- [ ] Skip instructions not in Parallax draft (~45 instructions)
- [ ] Update PDF with augmented entries

**What we're looking for:**
- Technical details about edge cases
- Behavioral nuances not captured in YAML
- Important usage patterns or constraints
- Hardware-level details that inform correct usage

**What we're NOT doing:**
- Copying Parallax prose
- Adapting their voice
- Validating our content against theirs
- Treating Parallax as authoritative over YAML

**Deliverables:**
- Gap analysis notes
- Augmented entries (in our voice)
- Updated PDF

**Validation:** All Parallax-covered instructions reviewed; gaps filled in our voice

---

### Phase 9: Technical Review (Post-Production)
**Goal:** Address thin entries with developer input

**Tasks:**
- [ ] Extract all entries still marked `<!-- TECHNICAL REVIEW -->`
- [ ] Prepare review document for chip developer
- [ ] Collect developer feedback
- [ ] Integrate enhanced descriptions
- [ ] Regenerate affected entries
- [ ] Update PDF

**Deliverables:**
- Technical review document
- Enhanced entries
- Final PDF

**Validation:** No entries remain marked for review

---

## 5. File Organization

### 5.1 Workspace Structure

```
/engineering/document-production/workspace/p2-assembly-language-manual/
├── README.md                           # Workspace quick reference
├── P2-Assembly-Language-Manual.md      # Master markdown document
├── templates/
│   ├── README.md                       # Template stack documentation
│   ├── p2kb-pasm2-reference.latex      # Main LaTeX template
│   └── p2kb-pasm2-diagrams.sty         # TikZ diagram definitions
├── filters/
│   └── (any Lua filters if needed)
├── assets/
│   └── (any external images)
├── parts/
│   ├── front-matter.md                 # Title, credits, how to use
│   ├── part-i/
│   │   ├── chapter-01-execution-model.md
│   │   ├── chapter-02-instruction-format.md
│   │   ├── chapter-03-flags.md
│   │   ├── chapter-04-timing.md
│   │   └── chapter-05-hardware.md
│   ├── part-ii/
│   │   ├── instructions-a.md
│   │   ├── instructions-b.md
│   │   ├── ... (alphabetical files)
│   │   ├── directives.md
│   │   ├── constants.md
│   │   └── special-registers.md
│   └── part-iii/
│       ├── appendix-a-encoding-table.md
│       ├── appendix-b-categorical-index.md
│       ├── appendix-c-special-registers.md
│       ├── appendix-d-constants.md
│       ├── appendix-e-reserved-words.md
│       └── appendix-f-opcodes.md
├── request.json                        # PDF Forge configuration
├── request-requirements.json           # Mandatory pandoc arguments
└── VERSION-TRACKING.md                 # Document version history
```

### 5.2 Assembly Strategy

Parts written separately, assembled into single master document for PDF generation:
```bash
cat front-matter.md part-i/*.md part-ii/*.md part-iii/*.md > P2-Assembly-Language-Manual.md
```

Or use Pandoc's multi-file input capability.

---

## 6. Quality Gates

### Per-Phase Validation

| Phase | Gate |
|-------|------|
| 0 | Exemplar PDF renders correctly |
| 1 | Chapter 2 explains how to read entries |
| 2-3 | Entries match template exactly |
| 4 | All 380 language elements documented |
| 5 | Part I establishes complete mental model |
| 6 | Appendix data matches Part II |
| 7 | PDF complete, no broken references |
| 8 | No entries marked for review remain |

### Voice Consistency Checks

Throughout all phases:
- [ ] Third person only (no "you", "we", "I")
- [ ] No hedging ("may", "might", "probably")
- [ ] Definitive statements
- [ ] Consistent terminology (C flag, Z flag, COG, Hub, LUT)
- [ ] Enhancement markers used correctly (⚠️💡🔧)

---

## 7. Risk Mitigation

### Risk: TikZ diagrams don't render
**Mitigation:** Phase 0 validates diagram system before bulk content generation

### Risk: Voice drift across 380 entries
**Mitigation:** Category batching; periodic voice consistency review

### Risk: Thin entries block progress
**Mitigation:** Mark and continue; technical review is separate phase

### Risk: Cross-references break
**Mitigation:** Validation pass in Phase 7; use consistent anchor naming

### Risk: PDF too large for single generation
**Mitigation:** Part-by-part assembly; test generation at phase boundaries

---

## 8. Success Criteria

Sprint complete when:
- [ ] PDF renders completely (all pages, no errors)
- [ ] All 380 language elements documented
- [ ] All TikZ diagrams render correctly
- [ ] Part I provides complete architectural foundation
- [ ] Cross-references and hyperlinks work
- [ ] Voice guide compliance verified
- [ ] Technical review entries addressed (or documented for future)

---

## 9. Session Planning

### 9.1 Sequential Estimate (without agents)

| Phase | Sessions | Focus |
|-------|----------|-------|
| Phase 0 | 1 | Design system, template, exemplar |
| Phase 1 | 1 | Part I skeleton, Chapter 2 |
| Phase 2 | 2-3 | Instructions A-M |
| Phase 3 | 2-3 | Instructions N-Z |
| Phase 4 | 1 | Directives, constants, registers |
| Phase 5 | 2 | Part I completion |
| Phase 6 | 1 | Appendices |
| Phase 7 | 1 | Assembly, PDF |
| Phase 8 | TBD | Technical review |

**Sequential total:** 12-15 sessions

### 9.2 Optimized Estimate (with parallel agents)

| Phase | Sessions | Strategy |
|-------|----------|----------|
| Phase 0 | 1 | Sequential (design coherence) |
| Phase 1 | 1 | Sequential (convention setting) |
| Phase 2-3 | 2 | **Parallel agents by letter range** |
| Phase 4 | 0.5 | **3 parallel agents** |
| Phase 5 | 1 | **4 parallel agents for chapters** |
| Phase 6 | 0.5 | **Parallel appendix generation** |
| Phase 7 | 1 | Sequential (assembly/coordination) |
| Phase 8 | 1-2 | Parallax gap analysis |
| Phase 9 | TBD | Technical review (human-dependent) |

**Optimized total:** 8-10 sessions (plus technical review)

### 9.3 Recommended Approach

Use parallel agents for bulk generation phases (2-6), sequential for design and assembly phases (0, 1, 7). This balances speed with quality control.

---

## 10. Multi-Agent Strategy

### 10.1 Where Parallel Agents Add Value

The Task tool allows spawning sub-agents that work in parallel. For this sprint, agents provide value where:

1. **Work is independent** - No dependencies between tasks
2. **Work is well-defined** - Clear inputs and outputs
3. **Work is substantial** - Worth the overhead of agent coordination
4. **Results can be merged** - Output integrates cleanly

### 10.2 Parallel Agent Opportunities by Phase

| Phase | Opportunity | Agent Strategy |
|-------|-------------|----------------|
| **Phase 2-3** | Instruction generation by letter | 3-4 agents: A-F, G-M, N-S, T-Z |
| **Phase 4** | Directives vs Constants vs Registers | 3 agents in parallel |
| **Phase 5** | Part I chapters | Up to 4 agents for chapters 1,3,4,5 (Ch.2 done in Phase 1) |
| **Phase 6** | Appendix generation | 3-4 agents for different appendices |

### 10.3 NOT Suitable for Parallel Agents

| Phase | Why Sequential |
|-------|----------------|
| **Phase 0** | Design system must be coherent; single vision |
| **Phase 1** | Chapter 2 sets conventions; must be unified |
| **Phase 7** | Assembly requires single coordinating agent |
| **Phase 8** | Technical review requires human integration |

### 10.4 Agent Control Pattern

**For instruction generation (Phases 2-3):**

```
Main Agent (Coordinator)
├── Reads all guide documents
├── Establishes conventions and exemplar
├── Spawns parallel agents with:
│   ├── Letter range assignment (e.g., "A-F")
│   ├── Full template specification
│   ├── Voice guide rules
│   ├── Encoding diagram convention
│   └── Output format requirements
├── Collects outputs from all agents
├── Merges into unified Part II
└── Validates consistency across agent outputs
```

**Agent prompt pattern:**
```
Generate instruction entries for letters [X-Y].

INPUT:
- YAML files: /engineering/knowledge-base/P2/language/pasm2/
- Entry template: [full template from creation-guide.md]
- Voice rules: [key rules from voice-guide.md]
- Encoding convention: [LaTeX macro usage]

OUTPUT:
- Complete markdown for each instruction
- Mark thin entries with <!-- TECHNICAL REVIEW -->
- Follow alphabetical order within your range

CRITICAL:
- Third person only
- No hedging language
- Include encoding diagram LaTeX for each
- Use exact terminology from guide
```

### 10.5 Consistency Enforcement

**Challenge:** Multiple agents might drift in voice or formatting.

**Solutions:**
1. **Exemplar in every prompt** - Include the ADD entry as gold standard
2. **Voice checklist in prompt** - Explicit rules agents must follow
3. **Post-merge validation** - Coordinator reviews for drift
4. **Same model for all agents** - Opus throughout, no model mixing

### 10.6 Merge Strategy

After parallel agents complete:

1. **Collect outputs** - Each agent returns markdown for its range
2. **Alphabetical assembly** - Interleave to proper A-Z order
3. **Cross-reference validation** - Ensure Related Instructions links work across ranges
4. **Voice audit** - Sample 10% of entries for consistency
5. **Fix any drift** - Coordinator corrects inconsistencies

### 10.7 Estimated Efficiency Gain

| Phase | Sequential Time | With Agents | Speedup |
|-------|-----------------|-------------|---------|
| Phase 2-3 | 4-6 sessions | 2 sessions | ~2-3x |
| Phase 4 | 1 session | 0.5 session | ~2x |
| Phase 5 | 2 sessions | 1 session | ~2x |
| Phase 6 | 1 session | 0.5 session | ~2x |

**Total sprint reduction:** ~12-15 sessions → ~8-10 sessions

### 10.8 Agent Failure Handling

If an agent fails or produces poor output:
1. **Identify affected range** - Which entries are impacted
2. **Re-run that range only** - Don't redo everything
3. **Isolate the issue** - Was it prompt clarity? Model capacity?
4. **Adjust prompt** - Refine for re-run

### 10.9 Practical Execution

**Phase 2 Example (Instructions A-M):**

```
Session start:
1. Coordinator reads guides, confirms conventions
2. Coordinator spawns 3 agents in parallel:
   - Agent 1: A-D (~60 instructions)
   - Agent 2: E-I (~60 instructions)
   - Agent 3: J-M (~60 instructions)
3. Agents work simultaneously
4. Coordinator collects all outputs
5. Coordinator merges and validates
6. Session ends with A-M complete
```

**Coordination overhead:** ~15-20 minutes per parallel batch for setup and merge.

---

## 11. Notes and Open Questions

### Resolved
- Model: Opus throughout (no switching needed)
- Approach: Bulk generation with thin entry marking
- Diagrams: TikZ with direct LaTeX passthrough

### To Confirm at Sprint Start
- Exact session schedule
- Technical reviewer availability for Phase 8
- Any priority adjustments

---

*Document Created: 2025-11-27*
*Version: 1.1 - Updated with corrected counts from YAML review*

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-27 | Initial sprint plan |
| 1.1 | 2025-11-28 | Corrected directive count (10→14), expanded special registers (6→16), added variant documentation notes |
