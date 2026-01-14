# PASM2 Manual Content Verification Sprint

**Status**: PLANNED
**Priority**: HIGH
**Created**: 2026-01-14
**Target Document**: P2 Assembly Language Reference Manual (Opus Master)
**Estimated Scope**: 400+ page manual, Part I primary focus

---

## Problem Statement

### Incident That Triggered This Sprint

On 2026-01-14, during Rayman review implementation, we discovered a **fabricated section** in Chapter 4:

**Section 4.5.3 "Hub Slot Synchronization"** claimed:
> "Programs that need predictable hub access timing can synchronize with the hub rotation using HUBSET. This instruction provides control over hub timing parameters and can align a COG's execution with its hub access windows."

**Reality:** HUBSET does NOT provide hub slot synchronization. The silicon documentation shows HUBSET has exactly five functions:
1. Clock configuration (`%0000`)
2. Hard reset (`%0001`)
3. Write-protect + debug enables (`%0010`)
4. Digital filter configuration (`%0100`)
5. PRNG seeding (`%1xxx`)

None of these relate to hub timing synchronization. **The section was entirely fabricated.**

### Why This Is Critical

This manual is intended to be the **authoritative source of truth** for PASM2. Fabricated content:
- Misleads developers into writing non-functional code
- Damages credibility of the entire manual
- May propagate to AI training data, perpetuating errors
- Violates the trust chain: `Trusted Sources → Trusted YAML → Trusted Documentation`

### Root Cause Analysis

The fabricated section exhibited classic AI hallucination patterns:
1. **Vague mechanism** - "provides control over hub timing parameters" without specifying which bits
2. **No working code** - Example was generic, not demonstrating the claimed feature
3. **Plausible-sounding but unverifiable** - Sounds like something that *could* exist
4. **"Side effects" claim** - "also provides synchronization side effects" is a hallucination red flag

---

## Audit Objectives

1. **Identify all fabricated content** in the manual
2. **Verify every technical claim** against authoritative sources
3. **Establish traceability** from manual content to source documents
4. **Create quality gates** to prevent future fabrication
5. **Document verification status** for each section

---

## Authoritative Source Hierarchy

When verifying claims, use this precedence:

| Priority | Source | Location | Authority Level |
|----------|--------|----------|-----------------|
| 1 | Silicon Documentation v35 | `sources/silicon-doc/` | Ground truth - hardware behavior |
| 2 | YAML Knowledge Base | `deliverables/ai/P2/language/pasm2/` | Validated, structured data |
| 3 | P2 Spreadsheet | (ingested) | Encoding accuracy |
| 4 | Parallax PASM2 Manual | `sources/pasm2-manual/` | Secondary - prose reference |
| 5 | P2 Datasheet | `sources/p2-datasheet/` | Hardware specifications |

**Rule:** If a claim cannot be traced to Priority 1-3 sources, it is suspect.

---

## Audit Methodology

### Phase 1: High-Risk Section Identification

**Highest risk areas** (prioritize these):

| Risk Level | Content Type | Why High Risk |
|------------|--------------|---------------|
| CRITICAL | Timing/synchronization claims | Easy to fabricate plausible-sounding timing behavior |
| CRITICAL | "Side effects" of instructions | Classic hallucination pattern |
| CRITICAL | Advanced features | Less commonly documented, easier to invent |
| HIGH | Instruction behavior in Part I | Narrative descriptions may drift from YAML |
| HIGH | Architectural explanations | Complex systems invite plausible invention |
| MEDIUM | Part II instruction entries | Generated from YAML, lower risk |
| LOW | Appendix tables | Directly extracted from sources |

### Phase 2: Claim Extraction

For each Part I section, extract:

1. **Instruction claims** - "INSTRUCTION does X"
2. **Timing claims** - "takes N cycles", "every N clocks"
3. **Register claims** - "register X controls Y"
4. **Mechanism claims** - "the system works by..."
5. **Capability claims** - "can be used to...", "enables..."

Create tracking spreadsheet:

| Section | Line | Claim | Claim Type | Source | Verified | Notes |
|---------|------|-------|------------|--------|----------|-------|
| 4.5.3 | 413 | "HUBSET provides hub timing control" | Capability | NONE | FABRICATED | Removed 2026-01-14 |

### Phase 3: Source Verification

For each extracted claim:

1. **Locate source document** that supports the claim
2. **Quote the specific passage** from the source
3. **Mark verification status**:
   - `VERIFIED` - Source confirms claim
   - `MODIFIED` - Source partially supports, claim needs adjustment
   - `UNVERIFIED` - No source found, needs investigation
   - `FABRICATED` - Source contradicts claim

### Phase 4: Cross-Reference Validation

For every instruction mentioned in Part I:

```bash
# Extract instruction from YAML and compare
cat deliverables/ai/P2/language/pasm2/<instruction>.yaml
```

Verify:
- Description matches manual's claim
- Timing matches manual's claim
- Flags/effects match manual's claim
- Any "also does X" claims are in YAML

### Phase 5: Pattern Detection

Search for hallucination linguistic patterns:

| Pattern | Example | Risk |
|---------|---------|------|
| Vague mechanism | "provides control over..." | HIGH |
| Unspecified side effects | "also provides... effects" | CRITICAL |
| Missing specifics | Features without bit patterns | HIGH |
| Hedge words in technical claims | "can be used to..." | MEDIUM |
| Synchronization without cycles | "aligns with..." | CRITICAL |

```bash
# Search for suspicious patterns
grep -n "provides control" chapter-*.md
grep -n "side effect" chapter-*.md
grep -n "can be used to" chapter-*.md
grep -n "also provides" chapter-*.md
grep -n "synchroniz" chapter-*.md
```

---

## Section-by-Section Audit Checklist

### For Each Section, Answer:

1. [ ] What specific P2 feature does this describe?
2. [ ] What source document(s) support this content?
3. [ ] Are there concrete details (bit patterns, cycle counts, addresses)?
4. [ ] Could someone implement this based solely on this description?
5. [ ] Does every instruction mentioned behave as described in its YAML?
6. [ ] Are timing claims verified against silicon doc?
7. [ ] Are any "advanced features" or "side effects" mentioned?

**If #4 is "no"** - Section may be too vague or fabricated.
**If #7 is "yes"** - Extra scrutiny required.

---

## Part I Chapter Audit Plan

### Chapter 1: The P2 Execution Model

| Section | Risk Level | Key Claims to Verify |
|---------|------------|---------------------|
| 1.1 Eight-COG Architecture | MEDIUM | COG count, independence, clock speed |
| 1.2 COG Memory | MEDIUM | 512 longs, address range, special registers |
| 1.3 LUT Memory | HIGH | 3-cycle timing, sharing mechanism, streamer integration |
| 1.4 Hub Memory | HIGH | 512KB, round-robin timing, access windows |
| 1.5 Execution Pipeline | HIGH | 2-stage, cycle counts, forwarding |
| 1.6 Execution Modes | HIGH | COG vs Hub execution, FIFO behavior |

### Chapter 2: The Instruction Format

| Section | Risk Level | Key Claims to Verify |
|---------|------------|---------------------|
| Encoding fields | MEDIUM | Bit positions against spreadsheet |
| Condition codes | MEDIUM | EEEE field values |
| AUGS/AUGD | HIGH | Augmentation mechanism |

### Chapter 3: Flags and Conditional Execution

| Section | Risk Level | Key Claims to Verify |
|---------|------------|---------------------|
| C and Z flags | LOW | Well-documented |
| IF_x conditions | LOW | Table can be verified |
| Flag modification | MEDIUM | WC/WZ/WCZ effects |

### Chapter 4: Timing and Determinism

| Section | Risk Level | Key Claims to Verify |
|---------|------------|---------------------|
| Instruction timing | HIGH | Every cycle count claim |
| Hub access rotation | HIGH | 8-cycle window, wait times |
| Synchronization | CRITICAL | Any sync mechanism claims |
| FIFO behavior | HIGH | Prefetch, streaming |

### Chapter 5: Special Hardware Overview

| Section | Risk Level | Key Claims to Verify |
|---------|------------|---------------------|
| CORDIC | HIGH | Pipeline depth, operations |
| Smart Pins | HIGH | Mode descriptions |
| Streamer | HIGH | Transfer mechanisms |
| Events/Interrupts | HIGH | 16 events, 3 interrupts |

---

## Verification Tools

### Script: Extract Instruction Claims

```bash
#!/bin/bash
# extract-instruction-claims.sh
# Find all instruction mentions in Part I and list for verification

grep -ohE '\b[A-Z]{2,}[A-Z0-9]*\b' part-i/*.md | \
  sort | uniq -c | sort -rn | \
  while read count instr; do
    if [ -f "../../deliverables/ai/P2/language/pasm2/${instr,,}.yaml" ]; then
      echo "FOUND: $instr ($count mentions)"
    else
      echo "CHECK: $instr ($count mentions) - no YAML"
    fi
  done
```

### Script: Verify Timing Claims

```bash
#!/bin/bash
# verify-timing-claims.sh
# Extract timing claims and cross-reference with YAML

grep -n "clock\|cycle\|takes [0-9]" part-i/*.md
```

### Manual Verification Process

For each suspicious claim:

1. Open silicon doc: `sources/silicon-doc/p2-documentation.txt`
2. Search for the instruction/feature name
3. Compare silicon doc description to manual claim
4. Document finding in tracking spreadsheet

---

## Quality Gates for Future Content

### Before Adding New Content:

1. [ ] Identify source document for every technical claim
2. [ ] Quote source in comment: `<!-- Source: silicon-doc p.XX -->`
3. [ ] Verify instruction behavior against YAML
4. [ ] Include specific details (bit patterns, cycle counts)
5. [ ] Avoid vague language ("provides control", "can be used")

### Red Flags to Avoid:

- "INSTRUCTION also provides..." (side effect claims)
- "can synchronize with..." (without specific mechanism)
- "provides control over..." (without specifying what/how)
- Features without code examples that actually work
- Timing claims without cycle counts

---

## Execution Plan

### Sprint Phase 1: Critical Risk Sections (Week 1)

- [ ] Audit Chapter 4 (Timing) - highest risk for fabrication
- [ ] Audit all synchronization claims
- [ ] Audit all "side effect" claims
- [ ] Create tracking spreadsheet

### Sprint Phase 2: High Risk Sections (Week 2)

- [ ] Audit Chapter 1 sections 1.3-1.6
- [ ] Audit Chapter 5 (Special Hardware)
- [ ] Verify all instruction behavior claims

### Sprint Phase 3: Medium Risk Sections (Week 3)

- [ ] Audit Chapter 2 (Instruction Format)
- [ ] Audit Chapter 1 sections 1.1-1.2
- [ ] Audit Chapter 3 (Flags)

### Sprint Phase 4: Part II Spot Check (Week 4)

- [ ] Random sample of 20 instruction entries
- [ ] Verify against YAML source
- [ ] Check for drift from generated content

### Sprint Phase 5: Documentation & Prevention

- [ ] Document all findings
- [ ] Update CLAUDE.md with verification requirements
- [ ] Create verification checklist for future edits

---

## Success Criteria

1. **100% of Part I claims traced to sources** - Every technical claim has documented source
2. **Zero fabricated sections remain** - All unverifiable content removed or corrected
3. **Tracking spreadsheet complete** - Every claim logged with verification status
4. **Prevention measures in place** - Quality gates documented for future work

---

## Lessons Learned (Pre-Sprint)

From the Hub Slot Synchronization incident:

1. **Vague descriptions are red flags** - Real features have specific implementations
2. **"Side effects" claims need extra scrutiny** - Classic AI hallucination pattern
3. **Cross-reference everything** - Silicon doc is ground truth
4. **Working code examples matter** - If you can't write working code for a feature, it may not exist
5. **Trust but verify** - Even plausible-sounding content can be fabricated

---

## References

- Silicon Documentation: `engineering/ingestion/sources/silicon-doc/p2-documentation.txt`
- YAML Knowledge Base: `deliverables/ai/P2/language/pasm2/`
- Parallax PASM2 Manual: `engineering/ingestion/sources/pasm2-manual/`
- Manual Source: `engineering/document-production/manuals/p2-assembly-language-manual/opus-master/`

---

*Sprint plan created: 2026-01-14*
*Triggered by: Fabricated Hub Slot Synchronization section discovery*
*Priority: HIGH - Manual credibility depends on content accuracy*
