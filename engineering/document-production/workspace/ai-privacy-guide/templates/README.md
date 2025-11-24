# AI Privacy Guide - Template Documentation

## Template Prefix
**Prefix:** `p2kb-presentation-*`
**Purpose:** Presentation-style privacy guide document

## Template Hierarchy

This document uses a **simple single-template** approach:

### Main Template
**File:** `p2kb-presentation.latex`
**Purpose:** Presentation-style document template
**Provides:**
- Clean, modern layout
- Presentation-optimized formatting
- Privacy guide content structure

### Shared Foundation (Available)
**File:** `p2kb-foundation.sty`
**Purpose:** Generic P2KB foundation infrastructure
**Status:** Available for use if needed

## Loading Order

Currently minimal - template is self-contained:
```latex
1. p2kb-presentation.latex  % Main template only
```

## Request.json Configuration

Reference the template in request.json as:
```json
{
  "documents": [{
    "template": "p2kb-presentation",
    "variables": {
      "title": "AI Privacy Guide for P2 Developers",
      "subtitle": "Claude Code Privacy Guidelines",
      "date": "2025"
    }
  }]
}
```

## Template Status

**Note:** This document is currently **deferred** in the production pipeline (not P2-related). Template is minimal and ready for future development if needed.

## Template Evolution

This template is **document-specific** and will evolve if work resumes:
- Currently minimal/experimental
- Can be enhanced based on presentation needs
- May adopt layered approach if complexity grows
