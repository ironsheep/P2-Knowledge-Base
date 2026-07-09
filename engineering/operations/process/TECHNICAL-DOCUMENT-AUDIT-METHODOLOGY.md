# Technical Document Audit Methodology

**Version:** 2.0.0
**Created:** 2026-01-23 · **Upgraded:** 2026-07-09 (fabrication-audit sprint §2)
**Derived From:** P2 Assembly Language Manual audit experience (2025-12 to 2026-01); upgraded after the 2026-07-09 forum-defect report exposed a coverage gap (Part I prose never claim-audited)
**Purpose:** Generic, document-independent framework for auditing technical documentation for accuracy, completeness, and hallucination

---

## Executive Summary

This methodology provides a systematic approach to audit any technical document for:
- **Hallucinations** - Fabricated information without source basis
- **Inaccuracies** - Correct information stated incorrectly
- **Omissions** - Missing critical information
- **Internal Inconsistencies** - Document contradicting itself
- **Hand-Waving** - Vague claims without concrete details
- **Drift** - Information that was correct but has diverged from current sources

The methodology is organized into phases that can be executed systematically, with increasing depth at each level.

---

## Part I: Foundation - Source Authority Framework

### 1.1 Establish the Source Trust Hierarchy

Before auditing any document, establish what sources are authoritative AND their relationship:

```
┌─────────────────────────────────────────────────────────────┐
│              SOURCE TRUST HIERARCHY TEMPLATE                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Level 1: PRIMARY AUTHORITY                                 │
│  └── Official specifications, silicon docs, standards       │
│      (The "ground truth" - always correct if conflicts)     │
│                                                             │
│  Level 2: IMPLEMENTATION VALIDATION                         │
│  └── Compilers, tools, reference implementations            │
│      (Validates how things actually work in practice)       │
│                                                             │
│  Level 3: DERIVED DATA                                      │
│  └── Knowledge bases, extracted data, YAML/JSON             │
│      (Should match Level 1; errors here are extraction bugs)│
│                                                             │
│  Level 4: TARGET DOCUMENTATION                              │
│  └── The manual being audited                               │
│      (What we're validating against the above levels)       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Key principle**: When sources conflict, trust the higher level. Document any exceptions explicitly.

### 1.2 Source Inventory Template

For each document type, fill out this inventory:

| Source Level | Source Name | Location | Coverage | Last Updated |
|--------------|-------------|----------|----------|--------------|
| Primary | | | | |
| Implementation | | | | |
| Derived | | | | |
| Target | | | | |

### 1.3 Source Trust Rules

1. **Never trust the target document** - It's what you're auditing
2. **Cross-reference multiple sources** - Single-source claims need extra scrutiny
3. **Implementation trumps theory** - If compiler behavior differs from spec, investigate
4. **Newer sources aren't automatically better** - Spec changes can introduce errors
5. **Absence of evidence isn't evidence of absence** - Missing from source ≠ wrong

---

## Part II: Hallucination Detection

### 2.1 Linguistic Red Flags

These patterns frequently accompany hallucinated content:

| Pattern | Risk Level | Why It's Suspicious |
|---------|------------|---------------------|
| "also provides" | HIGH | Fabricated secondary capabilities |
| "side effect" | HIGH | Invented behaviors not in sources |
| "provides control over" | HIGH | Vague capability claim |
| "can be used to" (vague) | MEDIUM | Use case without source verification |
| "mechanism" (no details) | MEDIUM | Hand-waving without concrete implementation |
| "enables/allows" (capability) | MEDIUM | Feature attribution without verification |
| "eliminates" | HIGH | Optimization claim needing proof |
| "automatically" | MEDIUM | Automatic behavior must be documented |
| "additionally" / "furthermore" | MEDIUM | Often precedes fabricated extras |
| "synchroniz*" (domain-specific) | HIGH | Complex mechanism often misunderstood |
| "in parallel" / "overlap*" / "while … proceeds" | HIGH | Claims concurrent execution the hardware may not do (2026-07-09: §4.6.2 "pipelined hub access" fabrication — a blocking RDLONG asserted to run in parallel) |
| "pipelined" (of a blocking op) | HIGH | Attributes latency-hiding to an operation that actually stalls the core |
| "issue … and immediately begin" / "fire-and-continue" | HIGH | Asserts non-blocking issue; most ops block until complete |
| "sets C/Z to indicate <special/edge case>" | HIGH | Invents a flag semantic — verify the flag's ACTUAL meaning vs the primary source (2026-07-09: §3.5.4 ABS "C indicates the edge case" fabrication; C is the original sign bit) |

**Audit action**: Search for these patterns; each instance requires source verification. Worked examples and idiom explanations are the highest-yield hiding place — an example asserting "this takes N clocks" or "C flags the edge case" is a claim, audit it like any other (§5.4).

### 2.2 Content Red Flags

| Pattern | Risk Level | Why It's Suspicious |
|---------|------------|---------------------|
| New capability claims | HIGH | Must exist in authoritative source |
| Optimization techniques | HIGH | Need mechanism basis in source |
| Cross-component interactions | MEDIUM | Complex behaviors prone to fabrication |
| Timing/performance claims | HIGH | Must match source exactly |
| Edge case behavior | MEDIUM | Often extrapolated rather than verified |
| "Hidden" features | HIGH | If not in primary source, probably doesn't exist |

### 2.3 Hallucination Categories

| Category | Definition | Example |
|----------|------------|---------|
| **Pure Fabrication** | Capability that doesn't exist | "HUBSET provides hub synchronization" (it doesn't) |
| **Capability Inflation** | Real feature with exaggerated scope | "Works with all pin modes" (only works with some) |
| **Mechanism Conflation** | Mixing up how similar things work | Confusing wait semantics with sync semantics |
| **Extrapolation** | Extending documented behavior beyond scope | "Since X works, Y must also work" |
| **Reasonable Invention** | Sounds plausible but isn't documented | "Instruction also sets the overflow flag" |

---

## Part III: Truth Matrix Construction

### 3.1 Purpose

A truth matrix normalizes data from all authoritative sources into a comparable format, allowing systematic conflict detection.

### 3.2 Construction Process

```
Phase 1: EXTRACTION
├── Extract relevant fields from each source
├── Normalize data to common format
└── Handle format differences (*, ---, N/A, etc.)

Phase 2: MERGE
├── Combine into single comparison structure
├── Primary key: unique identifier (instruction name, API, etc.)
└── Columns: each source's value for each field

Phase 3: CONFLICT DETECTION
├── Flag any row where sources disagree
├── Categorize conflict type (semantic vs formatting)
└── Prioritize by severity
```

### 3.3 Field Normalization Rules

| Source Format | Normalized |
|---------------|------------|
| Empty/blank/missing | `---` |
| "N/A", "n/a" | `---` |
| Em dash (—) | `---` |
| `*` (shorthand) | Expand to full meaning |
| Different capitalization | Standardize |
| Whitespace variations | Normalize |

### 3.4 Conflict Classification

| Type | Description | Action |
|------|-------------|--------|
| **Source Conflict** | Authoritative sources disagree | Requires human judgment |
| **Extraction Error** | Derived data differs from primary | Fix extraction pipeline |
| **Format Difference** | Same meaning, different expression | Document style decision |
| **Semantic Difference** | Different meaning, both valid | Choose per style guide |
| **Clear Error** | One source clearly wrong | Fix the wrong source |

---

## Part IV: Internal Consistency Audit

### 4.1 Self-Consistency Checks

A document should not contradict itself. Check:

| Check | What to Compare |
|-------|-----------------|
| **Table vs Narrative** | Do tables match prose descriptions? |
| **Syntax vs Behavior** | Does stated syntax match stated capabilities? |
| **Example vs Rule** | Do examples follow the documented rules? |
| **Cross-Reference** | Do referenced items exist and match? |
| **Terminology** | Is the same concept named consistently? |
| **Numbers** | Do numeric values match across mentions? |

### 4.2 Internal Consistency Audit Checklist

For each element in the document:

- [ ] If it appears in multiple places, do all instances agree?
- [ ] If a table summarizes text, do they match?
- [ ] If an example illustrates a rule, does it follow the rule?
- [ ] If a term is defined, is it used consistently?
- [ ] If a value is stated, is it stated the same everywhere?

### 4.3 Cross-Section Validation

| Section A Says | Section B Says | Status |
|----------------|----------------|--------|
| [Claim from earlier] | [Claim from later] | MATCH/CONFLICT |

---

## Part V: Claim Verification Protocol

### 5.1 Claim Classification System

Every technical claim in the document should be classified:

| Status | Definition | Action |
|--------|------------|--------|
| **VERIFIED** | Source confirms exactly | No action |
| **MODIFIED** | Source partially supports | Adjust wording |
| **UNVERIFIED** | No source found | Investigate or add source |
| **FABRICATED** | Source contradicts | Must remove/correct |

### 5.2 Claim Verification Process

```
For each claim:
1. Identify the claim type (timing, behavior, capability, etc.)
2. Identify required source(s) per type
3. Locate claim in source
4. Compare source statement to document statement
5. Classify as VERIFIED/MODIFIED/UNVERIFIED/FABRICATED
6. Document finding with source citation
```

### 5.3 Claim Type to Source Mapping (Template)

| Claim Type | Required Source(s) |
|------------|-------------------|
| Behavior description | Primary specification |
| Timing/performance | Implementation validation |
| Capability claim | Primary specification |
| Best practice | May need multiple sources |
| Warning/limitation | Primary specification |
| Cross-component interaction | Primary + implementation |

### 5.4 Coverage completeness — every claim, all prose (not a feature checklist)

**Root-cause rule (added 2026-07-09).** The audit's unit is **every claim**, extracted
**exhaustively from ALL prose** — narrative sentences, worked examples, and idiom
explanations — **not** a curated list of features/mechanisms. A prior Part I audit of
the PASM2 manual verified 8 chosen architectural features rigorously, declared
"examined ALL / Confidence HIGH," and shipped — while two fabrications sat in the
branchless-idiom and hub-timing **prose it never read claim-by-claim.** Feature-checklist
coverage is not claim coverage.

1. **Exhaustive extraction.** Enumerate every capability/behavior claim in the audited
   region. A worked example is a claim ("this code does X in Y clocks"); an idiom
   explanation is a claim. Sampling (§8.2's 10%) is a smoke test, **never** the
   systematic pass.
2. **Trust-chain proof for prose.** Every claim carries **silicon → YAML → doc**.
   Conceptual/narrative prose gets the **same** rigor as instruction entries — it is
   higher-risk, not exempt (Appendix A.3).
3. **YAML is not authority until proven.** The derived YAML (Level 3) can be wrong too;
   cite it only after confirming it against the primary source (Level 1). A doc-matches-
   YAML result is **not** a pass if the YAML itself is unverified.
4. **Honest scope attestation — silence ≠ audited.** Never report "examined ALL / HIGH
   confidence" unless coverage is provably exhaustive. A scoped audit **states its
   scope** and does not imply the remainder is clean; every region emits an explicit
   clean-or-finding record, and any unaudited region is **named as unaudited.**

---

## Part VI: Semantic vs Formatting Distinction

### 6.1 Why This Matters

Many audit "hits" are formatting differences, not errors. Distinguishing them saves effort.

### 6.2 Classification Guide

| Example | Type | Real Issue? |
|---------|------|-------------|
| "Result = 0" (a comparison) vs "Result == 0" | Semantic, agent-facing | **YES** — a comparison written with a single `=` is a defect; see §6.4 |
| "sign of result" vs "MSB of result" | Semantic equivalent | NO - same concept |
| "2 cycles" vs "2 clocks" | Terminology | NO - same meaning |
| "1 cycle" vs "2 cycles" | Semantic error | YES - different values |
| "carries if overflow" vs "no carry" | Semantic error | YES - opposite behavior |

> **Corrected 2026-07-09.** The prior edition of this table listed `=` vs `==` as
> "Formatting — NO, same meaning." That was wrong and contradicted this doc's own
> §14.2/§14.3. For the agent audience, `=` vs `==` is a **correctness** issue — see
> the operator rule in §6.4.

### 6.3 Decision Framework

```
Is the meaning preserved?
├── YES → Formatting difference (optional style fix)
└── NO → Semantic error (must fix)

Would a reader understand correctly?
├── YES → Not critical
└── NO → Must fix
```

### 6.4 Operator notation — `=` receives, `==` compares, `:=` only in code

Behavior descriptions (flag tables, YAML `c:`/`z:` fields) are math/pseudocode, **not**
source code. Follow the trusted source's own convention, applied consistently:

- **`=` means "receives / is"** — a flag or register takes this value: `C = D[31]`,
  `then D = D − S`. **Correct — leave alone.**
- **`==` means comparison** — a predicate yielding true/false: `Z = (D == 0)`,
  `Result == 0`.

The defect is **only the mismatch**: a comparison written with a single `=`. Fixing
just those makes the notation self-consistent (afterward `=` *always* means receives,
`==` *always* means compare), which is what stops an agent copying the wrong operator
into generated code. The strict Spin2 rule (`:=` assign / `==` compare, no bare `=`)
applies **only to actual Spin2 code examples** (fenced source); PASM2 CON-block `=` is
legitimate assembler syntax and stays. (`feedback_behavior_notation_vs_code_operators`.)

---

## Part VII: User Feedback Integration

### 7.1 Why User Feedback Is Gold

Users find errors that systematic audits miss because they:
- Use the documentation for real tasks
- Have domain expertise
- Test edge cases the auditor didn't consider
- Find "obvious" errors overlooked by familiarity

### 7.2 User Feedback Triage Protocol

No severity ranking (Part IX). Every user-reported item is verified against the
trusted source; if it is wrong it is repaired, and its **class** is swept across all
documents + YAMLs. User feedback is especially valuable because it finds what
systematic audits missed — treat each report as the seed of a class-wide sweep, not a
single-spot fix.

| Step | Action |
|------|--------|
| 1 | Verify the report against the primary source (silicon → YAML → doc) |
| 2 | If wrong: identify the **class** the defect belongs to |
| 3 | Sweep + fix every occurrence in every document AND every YAML |
| 4 | Full-audit any region the report shows was never claim-level audited, before re-release |

### 7.3 User Feedback Analysis Template

| # | User Report | Analysis | Severity | Action | Status |
|---|-------------|----------|----------|--------|--------|
| 1 | "X is wrong" | Verified against source | | | |

---

## Part VIII: Multi-Phase Audit Execution

### 8.1 Phase Overview

| Phase | Focus | Depth | Typical Duration |
|-------|-------|-------|------------------|
| 1: Smoke Test | Obvious errors, red flags | Surface | 1-2 hours |
| 2: Systematic | Every claim against sources | Thorough | 4-8 hours |
| 3: Deep | Cross-reference, edge cases | Exhaustive | 8+ hours |
| 4: Continuous | User feedback, updates | Ongoing | As needed |

### 8.2 Phase 1: Smoke Test

Quick scan for obvious issues:

1. Run hallucination pattern searches
2. Check internal consistency of tables
3. Verify a random 10% sample against sources
4. Review any recent changes/additions

**Stop if**: Many issues found (go to systematic audit)

### 8.3 Phase 2: Systematic Audit

Methodical verification:

1. Build truth matrix from all sources
2. Run automated conflict detection
3. Classify all claims as VERIFIED/MODIFIED/UNVERIFIED/FABRICATED
4. Document all findings

### 8.4 Phase 3: Deep Audit

Exhaustive investigation:

1. Verify every edge case and exception
2. Cross-reference every internal citation
3. Test every example for correctness
4. Verify timing/performance claims with implementation
5. Review architecture/concept explanations for accuracy

### 8.5 Phase 4: Continuous Audit

Ongoing maintenance:

1. Incorporate user feedback
2. Re-audit after source updates
3. Re-audit after document changes
4. Maintain audit trail

### 8.6 Fan-out mode — parallel finders + MANDATORY adversarial verification

For a whole-corpus pass (many documents), fan out per-document finders (per
Part/chapter-range for large docs) each running the exhaustive claim-level protocol
(§5.4). Fan-out is the only way to reach exhaustive coverage across a large corpus in
one pass.

**Non-negotiable safeguard: fan-out audit findings INVERT.** Parallel finders flag
correct content as wrong and miss real defects. Every finding MUST pass an independent
**adversarial-verify** stage (a separate agent prompted to *refute* it against the
trusted source) **and** a human hand-check of the confirmed set, **before** any finding
drives a fix. A raw fan-out finding list is a hypothesis set, never a fix list.
(`feedback_handverify_audit_findings_and_compile_blindspots`.)

**No silent coverage caps.** Every in-scope document emits a register — findings OR an
explicit "audited, clean" attestation. Anything not fully covered is logged, never
omitted (silence ≠ audited).

---

## Part IX: No Severity — Right vs. Wrong, and the Class-Wide Sweep

**Superseded 2026-07-09 (Stephen's directive).** We do **not** rank findings
CRITICAL/HIGH/MEDIUM/LOW. Severity invites deferral and understates systemic
problems. The only judgment is binary: **is the information correct or not?** If it is
wrong — for the human reader OR for the agents that consume the YAMLs — it is
**repaired.** No exceptions, no ranking, no "we'll fix the low-priority ones later."

### 9.1 Every finding triggers a class-wide sweep

A defect is an instance of a **class**. On finding one, identify the class and fix
**every occurrence in every document AND every YAML** — not just the reported spot.
Reject "lightweight" / triage-only responses; they guarantee more defect reports, not
fewer, and the exhaustive sweep is explicitly worth the time.
(`feedback_classwide_sweep_on_every_finding`.)

### 9.2 Systemic ⇒ content bump; full audit gates re-release

A systemic finding (a fabrication, a whole-class notation error) is a **content
version bump, not a patch** — a patch understates the scope and misleads readers. If a
region cannot be shown to have been fully, claim-level audited, it is **fully audited
before its document re-releases.** The full audit is a hard release gate.

---

## Part X: Audit Deliverables

### 10.1 Required Outputs

| Deliverable | Purpose |
|-------------|---------|
| **Source Inventory** | Documents what sources were used |
| **Truth Matrix** | Cross-source comparison data |
| **Findings Report** | Categorized list of issues |
| **Fix Tracking** | Status of each fix |
| **Audit Summary** | Executive overview |

### 10.2 Findings Report Template

```markdown
# Audit Findings Report

**Document**: [name]
**Audit Date**: [date]
**Auditor**: [name]
**Scope**: [what was audited]

## Summary Statistics

| Category | Count |
|----------|-------|
| Total claims audited | |
| VERIFIED | |
| MODIFIED | |
| UNVERIFIED | |
| FABRICATED | |

## Findings (grouped by class — no severity, per Part IX)

| ID | Location | Claim | Issue | Source (silicon→YAML→doc) | Repair | Class-sweep scope |
|----|----------|-------|-------|---------------------------|--------|-------------------|

## Audit Coverage

Every audited region emits a row — findings OR an explicit "audited, clean"
attestation. Name any region NOT claim-level audited (silence ≠ audited).

| Section | Claims extracted | Verified | Findings | Coverage |
|---------|------------------|----------|----------|----------|
```

---

## Part XI: Prevention - Pre-Write Verification

### 11.1 The Best Audit Is Prevention

New content should be verified BEFORE it enters the document.

### 11.2 Pre-Write Checklist

Before adding ANY technical claim:

- [ ] Identified the authoritative source for this claim type
- [ ] Found the specific supporting text in that source
- [ ] Noted the source location for citation
- [ ] Checked for red-flag phrases in my wording
- [ ] Verified this claim doesn't contradict existing content

### 11.3 Content Review Triggers

Request additional review when adding:

- New capability descriptions not directly from sources
- Optimization techniques or best practices
- Cross-component behavior descriptions
- Timing or performance claims
- Any claim using red-flag patterns

---

## Part XII: Tools and Automation

### 12.1 Automatable Audit Tasks

| Task | Tool Type | Benefit |
|------|-----------|---------|
| Pattern searching | grep/regex | Find red flags quickly |
| Cross-source comparison | Script | Build truth matrix |
| Internal consistency | Script | Find self-contradictions |
| Format validation | Linter | Catch structural issues |

### 12.2 Manual-Only Tasks

| Task | Why Not Automatable |
|------|---------------------|
| Semantic verification | Requires understanding |
| Judgment on conflicts | Requires domain expertise |
| Hallucination classification | Requires source interpretation |
| Priority assignment | Requires user impact assessment |

### 12.3 Recommended Script Types

```
extract_{source}_data.py  - Extract data from each source format
merge_truth_matrix.py     - Combine extractions into comparison
detect_conflicts.py       - Find disagreements between sources
validate_document.py      - Compare document against truth matrix
check_consistency.py      - Find internal contradictions
search_patterns.py        - Find hallucination red flags
```

---

## Part XIII: Quick Reference Cards

### 13.1 Hallucination Detection Quick Card

```
┌─────────────────────────────────────────────────────────────┐
│              HALLUCINATION DETECTION QUICK CHECK            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ RED FLAG PHRASES (search and verify):                       │
│   □ "also provides"     □ "side effect"                     │
│   □ "can be used to"    □ "mechanism" (vague)               │
│   □ "enables/allows"    □ "eliminates"                      │
│   □ "automatically"     □ "additionally/furthermore"        │
│                                                             │
│ VERIFICATION QUESTIONS:                                     │
│   □ Is this in the primary source? (cite line/section)      │
│   □ Does implementation confirm this?                       │
│   □ Is this extrapolation or documentation?                 │
│   □ Would another expert agree without checking?            │
│                                                             │
│ IF YOU CAN'T VERIFY: Don't include it.                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 13.2 Claim Verification Quick Card

```
┌─────────────────────────────────────────────────────────────┐
│                 CLAIM VERIFICATION QUICK CHECK              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ FOR EACH CLAIM:                                             │
│   1. What type? (behavior/timing/capability/etc.)           │
│   2. What source? (spec/compiler/KB/etc.)                   │
│   3. Where in source? (page/line/section)                   │
│   4. Does source say this? (exact match/similar/no)         │
│   5. Classification:                                        │
│      • VERIFIED - Source confirms exactly                   │
│      • MODIFIED - Source partially supports                 │
│      • UNVERIFIED - Can't find in source                    │
│      • FABRICATED - Source contradicts                      │
│                                                             │
│ PRIORITY:                                                   │
│   FABRICATED > UNVERIFIED > MODIFIED > VERIFIED             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 13.3 Internal Consistency Quick Card

```
┌─────────────────────────────────────────────────────────────┐
│              INTERNAL CONSISTENCY QUICK CHECK               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ CHECK EACH ELEMENT AGAINST ITSELF:                          │
│   □ Table columns match table header?                       │
│   □ Table data matches narrative explanation?               │
│   □ Examples follow the stated rules?                       │
│   □ Same thing described consistently throughout?           │
│   □ Cross-references point to correct targets?              │
│   □ Numbers match across all mentions?                      │
│                                                             │
│ COMMON ISSUES:                                              │
│   • Column headers shifted from data                        │
│   • "Optional" described as "required" elsewhere            │
│   • Example uses deprecated/wrong syntax                    │
│   • Forward reference to renamed/moved section              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Part XIV: Lessons Learned (from PASM Manual Audit)

### 14.1 What Worked

1. **Multi-source truth matrix** - Caught systematic errors no single source would reveal
2. **Linguistic pattern searching** - Found hallucinations efficiently
3. **User feedback integration** - Found errors our methodology missed
4. **Claim classification system** - Made triage and prioritization clear
5. **Parallel audit agents** - Scaled coverage without quality loss

### 14.2 What We Learned

1. **Column transposition is common** - Tables are high risk; verify alignment
2. **Semantically equivalent expressions confuse** - "=" vs "==" matters
3. **Fabrications sound plausible** - Domain expertise required to catch them
4. **Internal consistency ≠ external accuracy** - Both audits are needed
5. **Architecture sections are higher risk** - Less constrained than reference material
6. **Condition/edge cases get extrapolated** - Watch for invented behavior

### 14.3 Error Categories Found

| Category | % of Issues | Example |
|----------|-------------|---------|
| Column/field alignment | 35% | C, Z, Result columns shifted |
| Semantic notation errors | 25% | "=" instead of "==" |
| Missing "precise" keywords | 15% | "sign" vs "correct sign" |
| Fabricated capabilities | 10% | HUBSET sync claim |
| Timing errors | 10% | 54 vs 55 cycles |
| Internal inconsistency | 5% | Chapter 3 vs Chapter 4 |

---

## Appendix A: Audit Checklist by Document Type

### A.1 Reference Manual (Instructions, APIs, etc.)

- [ ] Every item has correct syntax
- [ ] Every item has correct parameters
- [ ] Flag/return/effect descriptions match source
- [ ] Timing/performance matches source
- [ ] Examples compile/run correctly
- [ ] Cross-references are valid
- [ ] Table columns aligned with headers

### A.2 Tutorial/Guide

- [ ] Steps actually work when followed
- [ ] Prerequisites are complete and correct
- [ ] Examples are tested and correct
- [ ] Claims about "what you'll learn" are fulfilled
- [ ] Referenced features exist and work as described

### A.3 Architecture/Concept Document

- [ ] HIGH RISK for fabrication - extra scrutiny
- [ ] Every capability claim verified against source
- [ ] Mechanisms have concrete implementation details
- [ ] Interactions between components verified
- [ ] Diagrams match textual descriptions

### A.4 Specification/Standard

- [ ] Normative claims are precise and testable
- [ ] Informative sections don't contradict normative
- [ ] Examples conform to specification
- [ ] Edge cases are explicitly addressed
- [ ] Versions/changes tracked accurately

---

## Appendix B: Glossary

| Term | Definition |
|------|------------|
| **Claim** | Any statement of fact in the document |
| **Fabrication** | A claim with no source basis (hallucination) |
| **Ground Truth** | The authoritative source for a domain |
| **Hand-waving** | Vague description without concrete details |
| **Hallucination** | AI-generated content not based on sources |
| **Internal Consistency** | Document agrees with itself |
| **Truth Matrix** | Cross-source comparison structure |
| **Verification** | Confirming claim against authoritative source |

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-23 | Initial version derived from PASM2 manual audit |
| 2.0.0 | 2026-07-09 | Fabrication-audit sprint §2. Root cause: Part I prose was never claim-audited (a curated 8-feature checklist over-attested as "examined ALL"). Added: §5.4 exhaustive claim extraction of ALL prose + trust-chain-proof-for-prose + YAML-not-authority-until-proven + honest-scope-attestation; §6.4 operator rule (= receives / == compares / := code-only) — corrected the prior "= vs == is formatting" guidance; §8.6 fan-out mode with mandatory adversarial-verify + hand-check; Part IX replaced severity with binary right/wrong + class-wide sweep + full-audit-gates-release; §2.1 new fabrication red-flags (parallel/overlap/pipelined-blocking-op/flag-indicates-edge-case); §7.2 feedback triage de-severitized. |

---

*This methodology was derived from real audit experience on the P2 Assembly Language Reference Manual, where systematic audits found ~410 discrepancies across 2,100+ claims, including 2 critical fabrications and 12 critical semantic errors.*
