# Extraction Technical Debt - Taxonomy & Prioritization

**Key Insight**: Not all extraction debt is equal - different types serve different strategic purposes

## Extraction Debt Categories

### 🔴 **Asset Extraction Debt** (Document-blocking)
**Purpose**: Enable immediate document creation  
**Driver**: Specific manual/guide needs  
**Priority**: High when document sprint planned  
**Timeline**: Pull-forward 1 week before document sprint  

**Example**:
```
Document Sprint: Terminal Window Manual
Asset Debt: DEBUG terminal screenshots missing
Action: Pull forward → Stephen captures → Manual creation proceeds
Impact: Blocks manual completion without these assets
```

### 🟡 **Source Improvement Debt** (Quality enhancement)  
**Purpose**: Improve underlying information quality  
**Driver**: Better coverage, accuracy, completeness  
**Priority**: Medium - when capacity allows between document sprints  
**Timeline**: Background work during enhancement sprints  

**Example**:
```
Source: SPIN2 v51 extraction at 85% completeness
Improvement Debt: Missing advanced SCOPE features, multi-COG details
Action: Enhance extraction → Better foundation for future documents  
Impact: Improves all downstream documents, but not V1.0 blocking
```

### 🟢 **Foundation Extraction Debt** (Future enablement)
**Purpose**: Enable future document categories  
**Driver**: Anticipated manual needs, AI optimization  
**Priority**: Low - strategic investment  
**Timeline**: Infrastructure sprints or major version boundaries  

**Example**:
```
Future Need: Advanced Smart Pins Manual (V1.1)
Foundation Debt: Smart Pins documentation incomplete  
Action: Comprehensive Smart Pins extraction before V1.1 sprint
Impact: Enables high-quality V1.1 Smart Pins Manual
```

## Tagging System for Extraction Debt

### Asset Extraction Tags
```
#asset-extraction #blocking #v1.0-terminal-manual
- DEBUG terminal output screenshots
- SCOPE display examples  
- Multi-window debugging layouts
```

### Source Improvement Tags  
```
#source-improvement #enhancement #spin2-debugger
- Multi-COG debugging workflows validation
- Advanced breakpoint management details
- Performance monitoring features
```

### Foundation Extraction Tags
```
#foundation-extraction #strategic #v1.1-enabler  
- Complete Smart Pins mode documentation
- CORDIC math engine comprehensive extraction
- Streamer subsystem detailed analysis
```

## Strategic Reasoning Analysis

### V1.0 Release Strategy: **Rapid Document Movement**

**What we prioritized**:
- Asset extraction for Terminal Window Manual
- Asset extraction for Debugger Manual
- Source completion just enough for V1.0 deliverables

**What we deferred** (correctly):
- Source improvement to 95%+ completeness
- Foundation extraction for V1.1+ features  
- Perfectionist extraction enhancement

**Why this was correct**:
```
Strategic Goal: Ship useful V1.0 documentation NOW
Constraint: Limited time before release window
Decision: Asset extraction (blocking) > Source improvement (nice-to-have)
Result: V1.0 can ship with good manuals, source improvement becomes V1.1 work
```

### V1.1+ Strategy: **Source Quality Investment**

**Next phase priorities**:
- Source improvement debt for better foundations
- Foundation extraction for new document categories
- Quality investment for long-term sustainability

## Prioritization Framework

### Document Sprint Planning
1. **Asset Extraction Debt** → Immediate pull-forward
2. **Source Improvement Debt** → Only if directly supports document  
3. **Foundation Extraction Debt** → Defer unless sprint theme requires

### Enhancement Sprint Planning  
1. **Source Improvement Debt** → Primary focus for quality
2. **Foundation Extraction Debt** → If aligns with enhancement theme
3. **Asset Extraction Debt** → Only for immediate document needs

### Infrastructure Sprint Planning
1. **Foundation Extraction Debt** → Strategic investment focus
2. **Process improvements** for extraction efficiency  
3. **Automation** for routine extraction tasks

## Decision Matrix

| Sprint Type | Asset Extraction | Source Improvement | Foundation Extraction |
|-------------|------------------|-------------------|---------------------|
| **Document** | 🔴 Pull Forward | 🟡 If Required | 🔴 Defer |
| **Enhancement** | 🟡 As Needed | 🔴 Primary Focus | 🟡 If Aligned |
| **Infrastructure** | 🟡 As Needed | 🟡 Process Focus | 🔴 Strategic Investment |

## Current V1.0 Status Assessment

### Asset Extraction (V1.0 focus) ✅
```
Terminal Window Manual Assets: 🟡 Stephen capturing
Debugger Manual Assets: 🟡 Placeholders ready
PDF Generation Assets: 🟡 Build process ready
Status: On track for V1.0 document delivery
```

### Source Improvement (Deferred) ⏸️
```
SPIN2 debugger extraction: 85% → could be 95%
Terminal window extraction: 95% → could be 99%  
Hardware manual extraction: 90% → could be 95%
Status: Good enough for V1.0, improvement debt for V1.1
```

### Foundation Extraction (Future) 🔮
```
Smart Pins comprehensive: Needed for V1.1 Smart Pins Manual
CORDIC detailed analysis: Needed for V1.2 Math Manual  
Streamer full extraction: Needed for V1.2 Multimedia Manual
Status: Strategic debt for future capability
```

## Implementation in Technical Debt System

### File Structure Update
```
/technical-debt/
├── VISUAL-ASSETS-DEBT.md              # Asset extraction focus
├── SOURCE-IMPROVEMENT-DEBT.md         # Source quality enhancement  
├── FOUNDATION-EXTRACTION-DEBT.md      # Strategic extraction investment
├── EXTRACTION-DEBT-TAXONOMY.md        # This file - categorization
└── sprint-selections/
    ├── v1.0-asset-selections.md       # What assets we pulled forward
    ├── v1.1-source-improvements.md    # Planned source quality work
    └── v1.2-foundation-extractions.md # Strategic extraction roadmap
```

### Tagging in Issues/Tasks
```
GitHub Issues:
- [ASSET-EXTRACTION] [V1.0-BLOCKING] Need DEBUG terminal screenshots
- [SOURCE-IMPROVEMENT] [V1.1-QUALITY] Enhance multi-COG debugging docs  
- [FOUNDATION-EXTRACTION] [V1.2-STRATEGIC] Complete CORDIC math extraction
```

## Success Validation

### V1.0 Strategy Validation ✅
**Question**: Did rapid document movement work?
**Evidence**: 
- Debugger Manual: Ready for professional PDF generation
- Terminal Manual: Asset capture in progress  
- Source quality: Good enough for V1.0 user needs
- Timeline: On track for V1.0 release

**Conclusion**: Strategy was correct - asset extraction prioritization enabled document delivery

### Future Strategy Planning
**V1.1**: Source improvement investment phase
**V1.2**: Foundation extraction for advanced manuals
**V2.0**: Comprehensive extraction completeness

## Process Integration

### Sprint Planning Questions
1. **Is this a document sprint?** → Prioritize asset extraction debt
2. **What's the document scope?** → Pull forward specific asset debt
3. **Is source quality blocking?** → Only then prioritize source improvement
4. **Future document needs?** → Foundation extraction in infrastructure sprints

### Quality Gates
- **V1.0**: Asset extraction complete, source "good enough"
- **V1.1**: Source improvement investment, foundation prep
- **V1.2**: Foundation extraction complete, advanced capabilities
- **V2.0**: Comprehensive quality across all categories

---

**Strategic Insight**: The choice to prioritize rapid document movement over perfectionist source improvement was strategically correct for V1.0. This taxonomy ensures we continue making optimal extraction investment decisions aligned with release goals.