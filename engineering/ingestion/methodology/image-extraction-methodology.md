# Image Extraction Methodology

## Overview
Systematic workflow for extracting, documenting, and enriching images from source documents to create informed visual sources for documentation.

## Process Steps

### 1. Claude Creates Consolidated Request
Document: `import/requirements/screenshots-needed-master.md`

**CRITICAL**: Use **req## numbering** (req01, req02... req24) instead of "Image #1, #2"

Each entry contains:
- **Image ID**: Sequential number for tracking
- **Source Document**: Which PDF/document it's from
- **Location**: Page number, section heading
- **Document Title**: Title as it appears in source
- **Extraction Target**: Which extraction needs this image
- **Purpose**: Why this image is needed
- **Expected Content**: What Claude expects to see
- **Usage Intent**: How it will be used in final documentation

Example:
```markdown
### Image #1
- **Source**: SPIN2 v51 Documentation
- **Location**: Page 125, Section "DEBUG SCOPE Display"
- **Title**: "Oscilloscope with Anti-aliasing"
- **For Extraction**: Terminal Window Focused Extraction
- **Purpose**: Demonstrates anti-aliasing feature in SCOPE display
- **Expected**: Sine wave with smooth edges showing AA effect
- **Usage**: Terminal Window Manual - Oscilloscope Features section
```

### 2. Stephen Creates Folder Structure
```
/import/
├── requirements/
│   └── screenshots-needed-master.md  ← Requirements source
├── p2/
│   ├── parallax-info/     → (move to .personnel-observations/)
│   ├── ironsheep-info/    → (move to .personnel-observations/)
│   └── images/            → (screenshots go here)
└── images/                ← Alternative staging location
```

**Key Decision**: Requirements document moved to `/import/requirements/` for better discoverability

### 3. Stephen Captures Images
- Gather all images from source documents
- **Keep original timestamped names** during staging (e.g., `Screenshot 2025-08-15 at 17.38.17.png`)
- Drop in `/import/p2/images/` OR `/import/images/`
- **Final naming happens during integration** (Step 7)

### 4. Claude Generates Image Catalog
Document: `/import/p2/images/image-catalog.md`

Creates numbered markdown with:
- All images embedded using **i-numbers** (i1, i2, i3... for this session)
- Original context from request
- Space for Stephen's descriptions
- **Important**: i-numbers are temporary workflow numbers, req-numbers are permanent

```markdown
## Image #1: Oscilloscope with Anti-aliasing
![Image 1](./spin2-v51-p125-scope-antialiasing.png)

**Source Context**:
- From: SPIN2 v51, Page 125
- Purpose: Demonstrates anti-aliasing in SCOPE display
- For: Terminal Window Manual

**Visual Description**: [Stephen will add]

---
```

### 5. Stephen Provides Visual Descriptions
Reviews catalog and adds descriptions for each image:
- What's visible in the image
- Key features to notice
- How it demonstrates the concept
- Any important details

### 6. Claude Updates Catalog
Incorporates Stephen's descriptions AND establishes **dual numbering**:
- **i-numbers**: Workflow tracking for this acquisition session
- **req-numbers**: Permanent requirement fulfillment tracking

**Format**: `Image i1 → req01: DEBUG Terminal Output`

### 7. Integration into Knowledge Base Extractions  
After catalog is complete with Stephen's descriptions:

**CRITICAL DECISION: Asset Ownership Model**

**Primary Extraction Owns Assets (Option 1B - IMPLEMENTED)**:
```
/sources/extractions/
├── [primary-extraction-name]/
│   ├── assets/images-[YYYYMMDD]/
│   │   ├── Screenshot files
│   │   └── image-catalog.md (original with human descriptions)
│   └── ASSET-CONSUMERS.md (consumer registry for automated forwarding)
└── [specialized-extraction-name]/
    └── assets/
        └── images-[YYYYMMDD].md (reference file pointing to primary)
```

**Why Option 1B?**
- **Clear hierarchy**: Primary extraction owns, specialized extractions reference
- **No duplication**: Single source of truth for actual image files
- **Easy maintenance**: Update images in one place
- **Scalable**: Multiple specialized extractions can reference same primary assets
- **Consistent structure**: All extractions have `assets/` folders

**Update Extraction Documents**:
Add "VISUAL ASSETS INTEGRATED/EXTRACTED" section to each relevant extraction:
```markdown
## VISUAL ASSETS INTEGRATED

### Screenshot Collection ([DATE])
- **Source**: [Document] screenshots provided by Stephen
- **Images**: [N] relevant screenshots
- **Asset Location**: `/sources/assets/[extraction]/images-[date]/`
- **Catalog**: `[context]-catalog.md` with context-specific descriptions
- **Coverage**: [List what the images show]
- **Human Validation**: Complete with detailed visual descriptions
- **Integration Status**: ✅ Assets integrated into [extraction] knowledge base
```

**Asset Integration Process**:
1. **Rename files to req## convention**: `spin2-v51-req01-debug-terminal-output.png`
2. **Move to primary extraction**: `/sources/extractions/[primary]/assets/images-[date]/`
3. **Create reference files for specialized extractions**: `assets/images-[date].md` files
4. **Update primary extraction document** with "VISUAL ASSETS EXTRACTED" section using req-numbers
5. **Update specialized extraction documents** with "VISUAL ASSETS INTEGRATED" section using req-numbers
6. **Clean staging directory**: Remove files from `/import/p2/images/`, keep structure
7. **Drop i-numbers from permanent docs**: Only req-numbers survive integration

**File Naming Convention**: `[source]-req##-[description].png`
- Example: `spin2-v51-req01-debug-terminal-output.png`
- Bonus images: `spin2-v51-bonus01-scope-sawtooth-display.png`

**Reference File Content Template**:
```markdown
# [Specialized Context] Assets - [Source] Screenshots

**Asset Location**: `/sources/extractions/[primary]/assets/images-[date]/`
**Reference Type**: Pointer to primary extraction assets
**Relevant Images**: req01, req04, req06 (subset of total)

## [Context] Image Mapping:
- **req01**: [Description] → [Specialized usage]
- **req04**: [Description] → [Specialized usage]

## Cross-Reference:
- **Primary Source**: [Link to primary catalog]
- **Original Requests**: `/import/requirements/screenshots-needed-master.md`
```

**Consumer Registry System (ASSET-CONSUMERS.md)**:
Primary extraction maintains a registry of ALL consumers for automated forwarding:

```markdown
## Secondary Extractions (Immediate Updates)
- `/sources/extractions/spin2-terminal-windows/` → req01, req04, req06, bonus01
- `/sources/extractions/spin2-debugger/` → req03

## Documents (Technical Debt Queue)  
- `/documentation/manuals/terminal-window-manual.md` → Available: req01, req04, req06, bonus01
- `/documentation/manuals/debugger-manual.md` → Available: req03
```

**Two-Tier Consumer Update Process**:

**Tier 1: Immediate Updates (Secondary Extractions)**
- Reference files updated automatically when new assets arrive
- Maintains knowledge base integrity and asset visibility
- No sprint planning required

**Tier 2: Deferred Updates (Documents)**  
- New assets create technical debt entries for sprint selection
- Documents are deliverables with strategic release timing
- Enhancement opportunities queued in `/technical-debt/VISUAL-ASSETS-DEBT.md`

**Key Decisions**:
- **Consumer Registry**: Primary extraction knows ALL downstream consumers
- **Automated Forwarding**: No manual discovery of update targets
- **Bonus Image Auto-Include**: Bonus images automatically forwarded to relevant consumers
- **Minimal Reference Approach**: Keep reference files lightweight
- **Always point back to primary** for full details and Stephen's descriptions
- **Use req-numbers only** in permanent documentation
- **Preserve i-numbers** only in acquisition catalogs for session history

### 8. Consumer Update Automation
**After asset integration, activate the consumer registry system:**

**Step 8a: Update Secondary Extractions (Immediate)**
For each secondary extraction listed in `ASSET-CONSUMERS.md`:
1. **Check asset relevance** to extraction focus area
2. **Update reference file** (`assets/images-[YYYYMMDD].md`) with new relevant assets
3. **Include bonus images** automatically if contextually relevant
4. **Add contextual usage descriptions** for new assets
5. **Maintain session history** (multiple timestamped references if needed)

**Step 8b: Update Technical Debt (Deferred)**
For each document listed in `ASSET-CONSUMERS.md`:
1. **Assess enhancement value** of new assets for document
2. **Update technical debt entry** in `/technical-debt/VISUAL-ASSETS-DEBT.md`
3. **Aggregate available assets** (req01-req06 becomes req01-req12 after next session)
4. **Revise effort estimates** based on total available enhancement
5. **Mark for sprint selection** as ready enhancement opportunity

**Consumer Update Example (When req07-req12 arrive)**:
```
# Terminal Windows Reference File Updates:
## Available Assets (Multi-Session):
- **Session 1** (2025-08-15): req01, req04, req06, bonus01
- **Session 2** (2025-08-20): req07, req09, req12, bonus02
- **Total Available**: 8 screenshots ready for terminal window manual enhancement

# Technical Debt Update:
#### Terminal Window Manual Updates Available:
OLD: - **Available**: 4 screenshots (req01, req04, req06, bonus01)
NEW: - **Available**: 8 screenshots (req01, req04, req06-req07, req09, req12, bonus01-02)
     - **Enhancement Value**: +25% → +45% visual learning effectiveness
     - **Integration Effort**: Medium (2-3 hours) → Medium-High (4-5 hours)
```

**Benefits of Consumer Registry System**:
1. **Zero Discovery Overhead**: No manual searching for update targets
2. **Complete Coverage**: Registry ensures no consumers are missed
3. **Automated Scaling**: New consumers easily added to registry
4. **Strategic Document Control**: Technical debt system prevents unplanned document work
5. **Bonus Image Visibility**: Relevant bonus content automatically included
6. **Session Aggregation**: Multi-session assets properly accumulated

### 9. Subsequent Image Import Sessions
**When additional images are needed for the same source document:**

**Scenario**: First extraction imported i1-i5, but screenshots-needed-master.md shows Images #1-24 still needed.

**Process for Additional Imports**:
1. **Create new timestamped folder**: `/sources/extractions/[primary]/assets/images-[YYYYMMDD2]/`
2. **Follow same import process**: Staging → Catalog → Descriptions → Integration
3. **Continue i-numbering**: New batch starts at i6, i7, i8... (continues from previous session)
4. **Update primary extraction document**: Add new "VISUAL ASSETS EXTRACTED" section for second batch
5. **Update specialized extraction references**: Modify `assets/images-[date].md` files to include newly relevant images

**Multi-Session Asset Structure**:
```
/sources/extractions/[primary]/
├── assets/
│   ├── images-20250815/     ← First batch (i1-i5)
│   │   ├── Screenshot files
│   │   └── image-catalog.md
│   └── images-20250820/     ← Second batch (i6-i12)
│       ├── Screenshot files
│       └── image-catalog.md
└── [extraction].md         ← Multiple VISUAL ASSETS sections
```

**Reference File Updates**:
Specialized extractions update their `assets/images-[date].md` to reference multiple sessions:
```markdown
## Multi-Session Asset References:
- **Batch 1**: `/sources/extractions/[primary]/assets/images-20250815/` (i1, i3, i5)
- **Batch 2**: `/sources/extractions/[primary]/assets/images-20250820/` (i7, i9)
```

**Benefits of Multi-Session Approach**:
- **Traceable import history**: Each session has clear timestamp and context
- **Incremental progress**: Don't need all images at once
- **Session-specific validation**: Each batch gets separate human validation
- **Flexible scheduling**: Accommodate Stephen's availability for image capture

### 10. Use in Documentation  
Images can now be intelligently referenced with:
- Full context of what they show
- Why they're important  
- Where they belong in documentation
- Human-validated descriptions of visual content
- Permanent locations in knowledge base structure
- Clear import session history and traceability
- **Automated consumer awareness** - all consumers know when new assets are available
- **Strategic document integration** - technical debt system manages enhancement timing
- **Bonus content visibility** - supplementary examples automatically surfaced to relevant consumers

## Benefits

1. **Context Preservation**: Never lose why an image was captured
2. **Intelligent Usage**: Know exactly when/how to use each image
3. **Efficient Workflow**: Batch processing of images per document
4. **Rich Documentation**: Images become teaching tools, not just illustrations
5. **Traceable Lineage**: Always know source and purpose
6. **Knowledge Base Integration**: Assets become permanent parts of extraction knowledge
7. **Multi-Context Usage**: Same images serve multiple specialized extractions
8. **Human Validation**: Visual descriptions ensure accurate understanding
9. **Clean Organization**: Systematic asset management with proper cleanup
10. **Incremental Progress**: Support multiple import sessions for large image sets
11. **Session History**: Clear tracking of when and how images were acquired
12. **Flexible Scheduling**: Accommodate human availability for image capture

## File Locations

### During Import Process:
- **Request List**: `/import/requirements/screenshots-needed-master.md`
- **Staging Images**: `/import/p2/images/` OR `/import/images/`
- **Staging Catalog**: `/import/p2/images/image-catalog.md`
- **Company Info**: `.personnel-observations/` (after initial import)

### After Integration (Permanent):
- **Primary Assets**: `/sources/extractions/[primary-extraction]/assets/images-[date]/`
- **Reference Files**: `/sources/extractions/[specialized-extraction]/assets/images-[date].md`
- **Updated Extractions**: `/sources/extractions/[extraction].md` (with VISUAL ASSETS sections)
- **Staging**: `/import/p2/images/` (cleaned, ready for next batch)

## Notes

- **Requirements document location**: Moved to `/import/requirements/` for better discoverability
- **Dual numbering system**: i-numbers for workflow, req-numbers for requirements
- **File naming convention**: Final files use req-numbers (`spin2-v51-req01-description.png`)
- **Reference file approach**: Minimal, always point back to primary for full details
- **Asset ownership**: Primary extraction owns, specialized extractions reference
- Always include page numbers for easy location in source documents
- Keep original timestamped names during staging
- Note any special features visible in screenshots
- Flag any images that need enhancement or annotation