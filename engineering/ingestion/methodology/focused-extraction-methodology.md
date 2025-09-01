# Focused Extraction Methodology

## Overview
Transform broad source documents into purpose-built, validated sources for specific user manuals.

## Process Steps

### 1. Focused Extraction
- Extract EVERYTHING related to the target feature from all sources
- Include:
  - Feature descriptions
  - Code examples
  - Configuration options
  - Constants/parameters
  - Screenshots/visuals
  - Related behaviors
  - Cross-references

### 2. Full Validation Suite
Run complete audit process:
- **Completeness Audit**: What's present vs missing?
- **Questions Audit**: What needs clarification?
- **Conflicts Audit**: Any contradictory information?
- **Gaps Audit**: What knowledge is missing?
- **Visual Audit**: What screenshots/diagrams exist or are needed?

### 3. Trust Level Assignment
Mark extraction with confidence levels:
- 🟢 **Green**: Complete, validated, ready for manual generation
- 🟡 **Yellow**: Mostly complete, minor gaps identified
- 🔴 **Red**: Significant gaps, needs additional sources

### 4. Enrichment Opportunities
Identify where we can add value:
- **Why** explanations (use cases, design decisions)
- **When** guidance (best practices, trade-offs)
- **How** patterns (combining features, optimization)
- **Creative** applications (novel uses, combinations)
- **Visual** suggestions (diagrams, screenshots, animations)

### 5. Validation Checkpoint
Before marking as validated source:
- All critical questions answered
- No unresolved conflicts
- Sufficient examples present
- Clear path to manual generation

## Current Focused Extractions

### Terminal Window Extraction
**Source**: SPIN2 v51 documentation
**Target**: Terminal Window User's Manual
**Content**: Debug visualization windows, feeding patterns, display options

### Single Step Debugger Extraction  
**Source**: SPIN2 v51 documentation
**Target**: Single Step Debugger User's Manual
**Content**: Debugger startup, constants, behaviors, control options

## Benefits
- Clean separation of concerns
- Validated sources before documentation
- Clear enrichment paths
- Traceable knowledge lineage
- Enables parallel documentation work