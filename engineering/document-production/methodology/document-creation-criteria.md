# Document Creation Decision Criteria

## Philosophy: Purposeful, Not Avoidant

**Goal**: Higher gate for new documents, not prevention  
**Principle**: Work harder to justify, but create when truly needed  
**Test**: Is this genuinely new content type that serves a distinct purpose?

---

## Create New Document When:

### **1. Distinct Content Type**
- **Content serves fundamentally different purpose** from existing docs
- **Different audience** (process vs deliverable vs reference)
- **Different lifecycle** (living vs archival vs template)

**Example**: Sprint retrospective template vs PROJECT-MASTER current state
- Different purpose: template vs status
- Different lifecycle: reusable vs evolving

### **2. High-Value Separation**  
- **Frequently referenced independently** from other content
- **Shared across multiple contexts** (multiple sprints, team members)
- **Reduces cognitive load** when focused on specific task

**Example**: MCP template vs individual sprint MCP
- Template: reusable across sprints
- Individual MCP: specific to one execution

### **3. Size/Complexity Threshold**
- **Content would overwhelm** a consolidated document
- **Different maintenance cadence** (updated at different rates)
- **Search/navigation improved** by separation

**Example**: Detailed audit procedures vs high-level project overview

### **4. Risk Mitigation**
- **Editing conflicts** if consolidated (multiple people updating)
- **Version control clarity** (track changes to specific content type)
- **Backup/recovery** benefits from separation

---

## Consolidate/Merge When:

### **1. Content Overlap**
- **Saying similar things** in different documents
- **Cross-references dominate** the content
- **Maintenance burden** of keeping synchronized

### **2. Low Individual Value**
- **Rarely referenced independently**
- **Makes more sense in context** of larger document
- **Too small** to justify separate navigation

### **3. Temporal Relationship**
- **Sequential workflow** where documents are always used together
- **Same decision-making context**
- **Same update frequency**

---

## Decision Process

### **Before Creating New Document:**

1. **Purpose Test**: What specific purpose does this serve that existing docs don't?
2. **Audience Test**: Who will use this and how is that different from existing docs?
3. **Lifecycle Test**: How often updated? When referenced? How maintained?
4. **Value Test**: Does separation create more value than consolidation cost?

### **Consolidation Triggers:**

1. **Redundancy Check**: Are we saying the same things multiple places?
2. **Maintenance Burden**: Are we struggling to keep related docs synchronized?
3. **Navigation Confusion**: Are people having trouble finding the right document?
4. **Size Check**: Have documents become too small to justify separate existence?

---

## Current Document Architecture Assessment

### **Existing Documents - Justified:**

#### **engineering/operations/README.md** (was PROJECT-MASTER.md)
- **Purpose**: Single source of truth for current project state
- **Audience**: Anyone needing to understand "where we are now"  
- **Lifecycle**: Living document, frequently updated
- **Value**: Essential orientation document

#### **Document Creation Criteria** (this document)
- **Purpose**: Decision framework for document architecture
- **Audience**: Document creators (us) when facing create/consolidate decisions
- **Lifecycle**: Template/reference, infrequently updated
- **Value**: Prevents ad-hoc decision making

#### **MCP Templates**
- **Purpose**: Reusable structure for detailed task planning
- **Audience**: Sprint planners creating detailed execution plans
- **Lifecycle**: Template, stable but evolving based on experience
- **Value**: Consistency and completeness in sprint execution

### **Recently Created - Assessment:**

#### **project-information-architecture.md**
- **Purpose**: Archive organization strategy
- **Justification**: New content type (information architecture) not covered elsewhere
- **Value**: Prevents loss of sprint learning, enables process improvement
- **Verdict**: ✅ Justified - distinct content type serving archive/recovery needs

---

## Guidelines for Sprint Document Creation

### **Each Sprint May Need:**
- **Planning Documents**: Question exhaustion process (temporary, archived)
- **MCPs**: Detailed execution plans (temporary, archived)  
- **Execution Artifacts**: Work outputs (permanent deliverables)
- **Should-Have-Considered**: Mid-sprint insights (temporary, archived)
- **Retrospective**: Process improvements (archived, but informs future)

### **Document Creation Pattern:**
1. **Start with existing templates** where possible
2. **Justify new documents** using criteria above
3. **Name purposefully** (clear what it is and why separate)
4. **Plan lifecycle** (temporary vs permanent vs archived)

---

## Success Metrics

### **Good Document Architecture:**
- **Coffee-deprived recovery test**: Can quickly orient after time away
- **Minimal hunting**: Find needed information quickly  
- **Clear purposes**: Each document has distinct value
- **Low maintenance**: Documents don't fight each other

### **Warning Signs:**
- **Saying same things** in multiple places
- **Frequent cross-references** instead of consolidated content
- **Confusion about where to put new information**
- **Documents that are never referenced independently**

---

## Content Verification Protocol (Hallucination Prevention)

**Added:** 2026-01-23
**Derived from:** PASM2 Manual Content Verification Sprint findings

### Why This Section Exists

The PASM2 manual audit discovered that **hallucinations occur at the moment of writing**, not after. Two critical fabrications (HUBSET "sync" capabilities that don't exist) passed multiple review cycles because no verification protocol existed at write-time.

**Key insight**: Voicing guides tell you HOW to say things; creation guides tell you WHAT structure to follow. Neither tells you HOW TO VERIFY what you're about to write is true.

### Before Writing ANY Technical Claim

**Mandatory verification steps:**

1. **Identify the claim type** - What kind of statement is this?
   - Behavior/functionality claim
   - Timing/performance claim
   - Capability claim
   - Configuration/parameter claim

2. **Identify required source** - Where must this be verified?
   - Primary specification (silicon doc, official manual)
   - Implementation validation (compiler, working code)
   - Derived knowledge base (YAML files)

3. **Locate the supporting evidence** - Find it before writing
   - Specific page/line/section in source
   - If you can't find it, **don't write it**

4. **Note the citation** - For traceability
   - Add source reference in comment or margin note
   - Enables future verification

### Hallucination Red-Flag Phrases

**Stop and verify when you're about to write:**

| Phrase | Risk | Why It's Suspicious |
|--------|------|---------------------|
| "also provides" | HIGH | Fabricated secondary capabilities |
| "side effect" | HIGH | Invented behaviors not in sources |
| "eliminates" | HIGH | Optimization claim needing proof |
| "automatically" | MEDIUM | Automatic behavior must be documented |
| "can be used to" (vague) | MEDIUM | Use case without verification |
| "mechanism" (no details) | MEDIUM | Hand-waving without implementation |
| "enables/allows" | MEDIUM | Capability attribution |
| "additionally/furthermore" | MEDIUM | Often precedes fabricated extras |

**If you catch yourself writing these patterns**: Stop. Find the source. Verify. Then write.

### Claim Verification Quick Check

```
┌─────────────────────────────────────────────────────────────┐
│              BEFORE WRITING A TECHNICAL CLAIM               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1. What type of claim? (behavior/timing/capability)       │
│   2. What source should verify this?                        │
│   3. Can I cite a specific location in that source?         │
│   4. Does the source say this EXACTLY or am I extrapolating?│
│                                                             │
│   If you can't answer #3: DON'T WRITE THE CLAIM             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Document-Specific Source Mapping

Each creation guide should define:

| Claim Type | Required Source | Example |
|------------|-----------------|---------|
| Instruction behavior | YAML + Silicon Doc | "ADD sets C flag on carry" |
| Timing values | YAML `clocks:` field | "Instruction takes 2 cycles" |
| Smart Pin modes | Silicon Doc + Spin2 constants | "Mode %00010 provides DAC" |
| Configuration | Official documentation | "WRPIN sets mode register" |

### What To Do When Source Doesn't Exist

1. **Don't invent** - If it's not documented, we can't claim it
2. **Mark as gap** - Use `:::missing` or similar marker
3. **Document the unknown** - "Behavior not specified in available sources"
4. **Request clarification** - Note need for authoritative source

### Prevention Example: How F01/F02 Would Have Been Caught

**The fabricated claim**: "HUBSET sync eliminates hub wait variation"

**Applying the protocol**:
1. Claim type: Capability claim (instruction does X)
2. Required source: YAML `hubset.yaml` + Silicon Doc HUBSET section
3. Can I cite? Check YAML → No "sync" in description. Check Silicon Doc → 5 functions listed, none are sync.
4. Extrapolating? YES - "sync" word doesn't appear in any HUBSET documentation

**Result**: Claim would have been blocked at step 3.

### Integration with Creation Guides

Each document's creation guide should include:

1. **Source Authority Hierarchy** - Which sources are authoritative for this document type
2. **Claim-to-Source Mapping** - What source verifies each claim type
3. **Red-Flag Patterns** - Domain-specific phrases that need extra verification
4. **Verification Examples** - Show the process for this document's content

### Full Methodology Reference

For comprehensive audit methodology (post-write verification), see:
`engineering/operations/process/TECHNICAL-DOCUMENT-AUDIT-METHODOLOGY.md`

---

**Decision Rule**: When in doubt, **err toward creation** with clear justification rather than **forced consolidation** that loses value.