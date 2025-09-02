# From Layered Truth to Central Repository: Architecture Strategy

## The Current Reality: Layered Truth

### Our Source Hierarchy (Established)
```
1. Chip Gracey (P2 Designer)     [ABSOLUTE TRUTH]
2. Silicon Documentation          [SILICON TRUTH]  
3. Official CSV/Spreadsheets      [OFFICIAL TRUTH]
4. Parallax Documentation         [VENDOR TRUTH]
5. Community Resources            [COMMUNITY TRUTH]
6. Derived/Inferred Knowledge     [ANALYTICAL TRUTH]
```

### What We Have Now
```
/engineering/ingestion/sources/
├── chip-gracey-clarifications/   [Multiple dates, absolute authority]
├── silicon-doc/                  [Deep technical, some gaps]
├── p2-instructions-csv/          [Complete instructions, official]
├── smart-pins/                   [Titus + Silicon Doc, validated]
├── iron-sheep-compiler/          [Condition codes, validated]
├── p2docs-github-io/            [Useful but unverified]
└── [20+ other sources...]        [Various authority levels]
```

## The Question: Should We Create a Central Repository?

### YES - We Absolutely Should. Here's Why:

#### 1. **Resolution of Conflicts**
Currently, we have to check multiple sources and remember their authority levels. A central repository would:
- Pre-resolve conflicts using our hierarchy
- Present single, authoritative answer
- Maintain source attribution for traceability

#### 2. **Deduplication**
The same information appears in multiple sources:
- ADD instruction in CSV, Silicon Doc, PASM2 manual
- Smart Pins in Silicon Doc, Titus, examples
- PTRA/PTRB in multiple places

Central repository = one canonical description with all details merged

#### 3. **Gap Filling**
We can combine partial truths:
```
CSV:         "ADD D, S - Add S to D"
Silicon Doc: "Sets C flag on overflow"  
Chip:        "Use ADDS for signed operations"
→ Central:   Complete, unified description
```

## Proposed Central Repository Structure

### Core Design: Entity-Based Knowledge Model

```yaml
P2-Knowledge-Base/
├── instructions/
│   ├── ADD.yaml
│   │   ├── mnemonic: "ADD D,{#}S {WC/WZ/WCZ}"
│   │   ├── encoding: "EEEE 0001000 CZI DDDDDDDDD SSSSSSSSS"
│   │   ├── description: [Consolidated from all sources]
│   │   ├── timing: {cog: 2, hub: 2}
│   │   ├── flags: {C: "carry out", Z: "result==0"}
│   │   ├── examples: [...]
│   │   ├── extended_precision_usage: [From Chip]
│   │   ├── silicon_bugs: []
│   │   ├── sources: [
│   │   │     {doc: "CSV", row: 10, authority: "OFFICIAL"},
│   │   │     {doc: "Silicon Doc", page: 45, authority: "SILICON"},
│   │   │     {doc: "Chip-2025-09-02", authority: "ABSOLUTE"}
│   │   │   ]
│   │   └── confidence: "VERIFIED"
│   │
│   ├── ADDX.yaml
│   └── [489 more instructions...]
│
├── architecture/
│   ├── cogs/
│   ├── memory/
│   ├── pipeline/
│   └── special-registers/
│
├── subsystems/
│   ├── smart-pins/
│   ├── cordic/
│   ├── streamer/
│   └── events/
│
├── programming-patterns/
│   ├── extended-precision/
│   ├── fifo-operations/
│   └── interrupt-handling/
│
└── metadata/
    ├── source-authority.yaml
    ├── knowledge-coverage.yaml
    └── validation-status.yaml
```

## The Pipeline: Ingestion → Central → Production

### Stage 1: Ingestion (Current)
```
Raw Sources → Extraction → Narrative Text → Cross-Validation
```

### Stage 2: Consolidation (Proposed)
```
All Narratives → Conflict Resolution → Merge by Entity → Central Repository
                      ↓
              [Apply Authority Hierarchy]
                      ↓
              [Fill Gaps with Lower Authority]
                      ↓
              [Mark Confidence Levels]
```

### Stage 3: Production (For Download-on-Demand)
```
Central Repository → Transform → Optimized Formats
                         ↓
                  [Instruction Cards]
                  [Quick References]  
                  [Code Examples]
                  [Relationship Graphs]
                         ↓
                  Download-on-Demand API
```

## Key Design Decisions

### 1. **Format for Central Repository**
Options:
- **YAML/JSON**: Machine-readable, structured, validation possible
- **Markdown**: Human-readable, harder to validate
- **Database**: Powerful queries, complex maintenance
- **Hybrid**: YAML for data, Markdown for narratives

**Recommendation**: YAML for structured data, Markdown for explanations

### 2. **Granularity**
Each instruction as separate file vs. grouped files?
**Recommendation**: Separate files - easier versioning, cleaner diffs

### 3. **Relationship Management**
How to handle "ADD relates to ADDX, ADDS, ADDSX"?
**Recommendation**: Explicit relationship fields in each entity

### 4. **Confidence Scoring**
How to convey "we're 95% sure about this"?
**Recommendation**: 
```yaml
confidence: VERIFIED     # Multiple sources agree
confidence: SINGLE_SOURCE # Only one source
confidence: INFERRED     # We figured it out
confidence: UNCERTAIN    # Conflicting info
```

## Benefits of This Approach

### For Central Knowledge Base
1. **Single Source of Truth**: No more checking multiple documents
2. **Conflict Resolution**: Pre-resolved using authority hierarchy
3. **Complete Picture**: All knowledge about each entity in one place
4. **Traceable**: Every fact linked to its source
5. **Maintainable**: Update one place when new info arrives

### For Download-on-Demand
1. **Pre-Validated**: No runtime conflict resolution needed
2. **Efficient Queries**: "Give me everything about ADD" is one file
3. **Relationship-Aware**: Can fetch related knowledge easily
4. **Confidence-Rated**: AI knows how much to trust each fact
5. **Granular Access**: Download only what's needed

## Implementation Strategy

### Phase 1: Define Schema
- Create YAML schema for instructions
- Create schemas for other entity types
- Define relationship types
- Establish confidence levels

### Phase 2: Build Consolidator
- Script to read all narratives
- Apply authority hierarchy
- Merge into central entities
- Validate completeness

### Phase 3: Initial Population
- Start with instructions (highest value)
- Add architecture knowledge
- Include subsystems
- Import examples

### Phase 4: Production Pipeline
- Transform central → API format
- Build query interface
- Create caching strategy
- Test with AI agents

## Critical Questions to Resolve

1. **How do we handle evolution?** 
   - When Chip clarifies something, how does it flow through?
   - Version the central repository?

2. **What about visual content?**
   - Timing diagrams, pin layouts, block diagrams
   - Store as separate assets or inline?

3. **Examples and code snippets?**
   - Part of instruction entity or separate?
   - How to validate they still compile?

4. **Relationships and dependencies?**
   - How deep do we model connections?
   - Is "ADDX depends on ADD" enough or do we need more?

5. **Update frequency?**
   - Rebuild central on every ingestion?
   - Incremental updates?
   - How to track what changed?

## Conclusion

**Yes, we should create a central repository**. It should be:
1. The consolidation point for all our layered truths
2. The single source feeding download-on-demand
3. Structured for both human understanding and machine consumption
4. Traceable to original sources
5. Confidence-rated for trust levels

This central repository becomes our **"manufactured truth"** - carefully assembled from all sources, conflicts resolved, gaps filled, and ready for any consumption pattern.

---

*This is the bridge from ingestion chaos to organized knowledge delivery.*