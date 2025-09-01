# Document Generation Process Guide

**Complete checklist for generating new manuals and document revisions**

*Created: 2025-08-20*  
*Purpose: Ensure consistent quality and tracking for all document production*

## 🎯 Overview

This guide ensures every document we produce:
- Gets properly tracked in our systems
- Has asset needs documented
- Updates dashboard visibility
- Follows quality standards
- Maintains process consistency

## 📋 Complete Document Generation Checklist

### Phase 1: Planning & Setup
- [ ] **Identify document need** and target audience
- [ ] **Add to Document Pipeline** (`/pipelines/document-production-pipeline.md`)
- [ ] **Assign initial status** (🔴 Planned)
- [ ] **Note in sprint candidates** if not immediate priority
- [ ] **Determine initial version** (start with v0.1-DRAFT)

### Phase 1.5: Draft Status Protocol 🚧

**MANDATORY for ALL documents:**

#### Document Marking Requirements:
- [ ] **Version suffix**: Add "-DRAFT" to version (e.g., v0.1-DRAFT)
- [ ] **Header warning**: Add draft warning box at document top
- [ ] **Footer marking**: Include "DRAFT" prefix in footer
- [ ] **Title page**: Add red warning text and status box

#### Draft Warning Template:
```markdown
# 🚧 DRAFT - FOR [PURPOSE] REVIEW ONLY 🚧

⚠️ **DRAFT STATUS**: [Executive/Technical/Internal] Review Version  
⚠️ **NOT FOR RELEASE**: [Reason - incomplete, needs approval, etc.]  
⚠️ **PURPOSE**: [Why this draft exists]  
⚠️ **VERSION**: [0.1-DRAFT]
```

#### Version Progression Path:
```
v0.1-DRAFT → v0.2-DRAFT → ... → v0.9-DRAFT → v1.0-RC → v1.0-RELEASE
```

#### Dashboard Tracking Requirements:
- [ ] **Version** field shows draft/release status
- [ ] **Release Status** explicitly states NOT FOR RELEASE or READY
- [ ] **Draft Markers** confirms what warnings are applied
- [ ] **Purpose** clarifies review type (executive/technical/user)
- [ ] **Missing Flags** counts active content flags

### Phase 2: Content Creation
- [ ] **Choose appropriate model**:
  - Opus 4.1: Rich prose, tutorials, user-facing docs
  - Sonnet 4: Technical reference, structured content
  - Haiku 3.5: Simple updates, basic formatting
- [ ] **Create document structure** in appropriate location:
  - `/documentation/manuals/[manual-name]/` for manuals
  - `/documentation/guides/` for guides
  - `/documentation/reference/` for references
- [ ] **Write content** following style guidelines
- [ ] **Create `assets-needed.md`** listing missing elements:
  ```markdown
  # [Document Name] - Assets Needed
  
  **Document**: [Name and Version]
  **Status**: [Current Status]
  **Created**: [Date]
  **Location**: [Path]
  
  ## 🔴 Critical Assets Needed
  
  ### 1. [Asset Category]
  **Location in Document**: [Chapter/Section]
  **What's Missing**: [Specific description]
  **Current State**: [Placeholder or missing]
  **What's Needed**: [Detailed requirements]
  **Format**: [Expected format]
  **Source**: [Where to find it]
  
  ## 📊 Asset Priority Matrix
  | Priority | Asset | Blocks | Impact |
  |----------|-------|--------|--------|
  | 🔴 HIGH | [Asset] | [What it blocks] | [Chapters affected] |
  ```

### Phase 3: Pre-Production Updates
- [ ] **Update Document Pipeline** (`/pipelines/document-production-pipeline.md`):
  - Change status to 🟡 Content Ready or 🟢 In Production
  - Add location paths
  - Note any blockers
- [ ] **Update Operations Dashboard** (`/engineering/README.md`):
  - Update Document Production Pipeline section
  - Add to Document Production Status section if active
  - List critical asset needs with counts
  - Link to assets-needed.md

### Phase 4: PDF Generation Preparation
- [ ] **Create output directory**: `/exports/pdf-generation/outbound/[doc-name-version]/`
- [ ] **Generate `document.md`**: Combined markdown file
- [ ] **Create `request.json`**:
  ```json
  {
    "documents": [{
      "input": "document.md",
      "output": "[Document_Name]_v[version].pdf",
      "template": "[template-name]",
      "variables": {
        "title": "[Full Title]",
        "version": "[X.Y]",
        "date": "[Month Year]",
        "author": "[Author/Organization]",
        "company": "[Company/Tagline]"
      }
    }],
    "options": {
      "cleanup": true,
      "archive": true,
      "optimize": true
    }
  }
  ```
- [ ] **Copy any images** to `/images/` subdirectory if needed
- [ ] **Verify LaTeX template** exists or create one

### Phase 5: Production Handoff
- [ ] **Final dashboard update**:
  - Status: "PDF Generation Requested"
  - Note handoff timestamp
- [ ] **Context save** for resume:
  ```bash
  mcp__todo-mcp__context_set key:"doc_[name]_status" value:"PDF requested [date]"
  ```
- [ ] **Handoff notification** to human operator

### Phase 6: Post-Production
- [ ] **Check `/inbound/`** for completed PDF
- [ ] **Review PDF** for quality issues
- [ ] **Update Document Pipeline**: Status to ✅ Released
- [ ] **Update Dashboard**: Move from active to completed
- [ ] **Archive source files** if needed
- [ ] **Clean up `/outbound/`** directory

## 🔄 For Document Revisions

### Additional Steps for Revisions:
- [ ] **Create revision branch** or new version directory
- [ ] **Document changes** in revision log
- [ ] **Update version numbers** throughout
- [ ] **Preserve previous version** for reference
- [ ] **Note revision reason** in dashboard

## 🎨 Style Consistency Checklist

### For deSilva-Style Documents:
- [ ] Conversational voice with "Well, ..." corrections
- [ ] 60% examples, 40% theory ratio
- [ ] "Medicine Cabinet" simplifications
- [ ] "Uff!" moments after complexity
- [ ] Personal expressions maintained
- [ ] Empathetic acknowledgment of difficulty

### For Technical References:
- [ ] Clear hierarchical structure
- [ ] Consistent terminology
- [ ] Complete cross-references
- [ ] Verified technical accuracy
- [ ] Comprehensive index

## 📊 Dashboard Update Templates

### For Operations Dashboard:
```markdown
### [Document Name] v[X.Y]
**Status**: 🟢 [Current Status]  
**[Milestone]**: [Date]  
**Statistics**:  
- [Key metric 1]
- [Key metric 2]

**Current Blockers - Assets Needed**:
- 🔴 [Critical blocker]
- 🟡 [Medium priority]
- [→ Full Asset List](path/to/assets-needed.md)
```

### For Document Pipeline:
```markdown
### [Document Name]
**Status**: 🟢 [Status]  
**Source**: [Source description]  
**Format**: [Output format]  
**Audience**: [Target audience]  
**Location**: [Path]  
**Assets Needed**: [[Count] items](link)  
**Note**: [Current state/next steps]
```

## 🚨 Common Pitfalls to Avoid

1. **Forgetting dashboard updates** - Use this checklist!
2. **Missing assets documentation** - Create assets-needed.md immediately
3. **Wrong model choice** - Opus for prose, Sonnet for structure
4. **No version tracking** - Always include version in filenames
5. **Skipping context saves** - Essential for work resumption
6. **Not updating pipeline tracker** - Breaks visibility

## 📝 Global Markdown Formatting Fixes

### Bold Headings with Colons Before Lists
**Issue**: Lists don't render properly when placed directly after bold headings ending with colons  
**Pattern**: `**Heading:**` immediately followed by list items (no blank line)  
**Fix**: Add blank line between heading and list

**Example Before**:
```markdown
**The Smart Pin Advantage:**
- Item 1
- Item 2
```

**Example After**:
```markdown
**The Smart Pin Advantage:**

- Item 1
- Item 2
```

**Common Occurrences**:
- Executive summaries with feature lists
- Mode variant descriptions
- Advantage/disadvantage lists
- Configuration step lists

**Detection Pattern**: Search for `**.*:**` followed immediately by `\n-` or `\n*` or `\n1.`

### Headings Followed by Code Blocks
**Issue**: Code blocks placed directly after headings without blank line cause formatting issues  
**Pattern**: Any heading level (`#` through `######`) immediately followed by code fence  
**Fix**: Add blank line between heading and code block

**Example Before**:
```markdown
#### Step 2: Configure the Pin
```pasm2
wrpin mode, #pin
```
```

**Example After**:
```markdown
#### Step 2: Configure the Pin

```pasm2
wrpin mode, #pin
```
```

**Common Occurrences**:
- Tutorial step headings with code examples
- "Mistake" or "Anti-pattern" headings with bad code examples
- Configuration sections with code blocks
- Implementation headings with example code

**Detection Commands**:
```bash
# Find headings followed by code blocks
awk '/^#{1,6} .*$/ {heading=$0; line=NR; getline; if ($0 ~ /^```/) print line ": " heading}' document.md
```

### Regular Text with Colons Before Lists
**Issue**: Lists don't render when placed directly after regular text ending with colon  
**Pattern**: Non-heading text ending with `:` immediately followed by list  
**Fix**: Add blank line between text and list

**Example Before**:
```markdown
The system provides these features:
- Feature 1
- Feature 2
```

**Example After**:
```markdown
The system provides these features:

- Feature 1  
- Feature 2
```

**Common Occurrences**:
- Feature descriptions
- System capabilities
- Function parameter lists
- Architecture component lists

**Detection Pattern**: Search for lines ending with `:# Document Generation Process Guide

**Complete checklist for generating new manuals and document revisions**

*Created: 2025-08-20*  
*Purpose: Ensure consistent quality and tracking for all document production*

## 🎯 Overview

This guide ensures every document we produce:
- Gets properly tracked in our systems
- Has asset needs documented
- Updates dashboard visibility
- Follows quality standards
- Maintains process consistency

## 📋 Complete Document Generation Checklist

### Phase 1: Planning & Setup
- [ ] **Identify document need** and target audience
- [ ] **Add to Document Pipeline** (`/pipelines/document-production-pipeline.md`)
- [ ] **Assign initial status** (🔴 Planned)
- [ ] **Note in sprint candidates** if not immediate priority
- [ ] **Determine initial version** (start with v0.1-DRAFT)

### Phase 1.5: Draft Status Protocol 🚧

**MANDATORY for ALL documents:**

#### Document Marking Requirements:
- [ ] **Version suffix**: Add "-DRAFT" to version (e.g., v0.1-DRAFT)
- [ ] **Header warning**: Add draft warning box at document top
- [ ] **Footer marking**: Include "DRAFT" prefix in footer
- [ ] **Title page**: Add red warning text and status box

#### Draft Warning Template:
```markdown
# 🚧 DRAFT - FOR [PURPOSE] REVIEW ONLY 🚧

⚠️ **DRAFT STATUS**: [Executive/Technical/Internal] Review Version  
⚠️ **NOT FOR RELEASE**: [Reason - incomplete, needs approval, etc.]  
⚠️ **PURPOSE**: [Why this draft exists]  
⚠️ **VERSION**: [0.1-DRAFT]
```

#### Version Progression Path:
```
v0.1-DRAFT → v0.2-DRAFT → ... → v0.9-DRAFT → v1.0-RC → v1.0-RELEASE
```

#### Dashboard Tracking Requirements:
- [ ] **Version** field shows draft/release status
- [ ] **Release Status** explicitly states NOT FOR RELEASE or READY
- [ ] **Draft Markers** confirms what warnings are applied
- [ ] **Purpose** clarifies review type (executive/technical/user)
- [ ] **Missing Flags** counts active content flags

### Phase 2: Content Creation
- [ ] **Choose appropriate model**:
  - Opus 4.1: Rich prose, tutorials, user-facing docs
  - Sonnet 4: Technical reference, structured content
  - Haiku 3.5: Simple updates, basic formatting
- [ ] **Create document structure** in appropriate location:
  - `/documentation/manuals/[manual-name]/` for manuals
  - `/documentation/guides/` for guides
  - `/documentation/reference/` for references
- [ ] **Write content** following style guidelines
- [ ] **Create `assets-needed.md`** listing missing elements:
  ```markdown
  # [Document Name] - Assets Needed
  
  **Document**: [Name and Version]
  **Status**: [Current Status]
  **Created**: [Date]
  **Location**: [Path]
  
  ## 🔴 Critical Assets Needed
  
  ### 1. [Asset Category]
  **Location in Document**: [Chapter/Section]
  **What's Missing**: [Specific description]
  **Current State**: [Placeholder or missing]
  **What's Needed**: [Detailed requirements]
  **Format**: [Expected format]
  **Source**: [Where to find it]
  
  ## 📊 Asset Priority Matrix
  | Priority | Asset | Blocks | Impact |
  |----------|-------|--------|--------|
  | 🔴 HIGH | [Asset] | [What it blocks] | [Chapters affected] |
  ```

### Phase 3: Pre-Production Updates
- [ ] **Update Document Pipeline** (`/pipelines/document-production-pipeline.md`):
  - Change status to 🟡 Content Ready or 🟢 In Production
  - Add location paths
  - Note any blockers
- [ ] **Update Operations Dashboard** (`/OPERATIONS-DASHBOARD.md`):
  - Update Document Production Pipeline section
  - Add to Document Production Status section if active
  - List critical asset needs with counts
  - Link to assets-needed.md

### Phase 4: PDF Generation Preparation
- [ ] **Create output directory**: `/exports/pdf-generation/outbound/[doc-name-version]/`
- [ ] **Generate `document.md`**: Combined markdown file
- [ ] **Create `request.json`**:
  ```json
  {
    "documents": [{
      "input": "document.md",
      "output": "[Document_Name]_v[version].pdf",
      "template": "[template-name]",
      "variables": {
        "title": "[Full Title]",
        "version": "[X.Y]",
        "date": "[Month Year]",
        "author": "[Author/Organization]",
        "company": "[Company/Tagline]"
      }
    }],
    "options": {
      "cleanup": true,
      "archive": true,
      "optimize": true
    }
  }
  ```
- [ ] **Copy any images** to `/images/` subdirectory if needed
- [ ] **Verify LaTeX template** exists or create one

### Phase 5: Production Handoff
- [ ] **Final dashboard update**:
  - Status: "PDF Generation Requested"
  - Note handoff timestamp
- [ ] **Context save** for resume:
  ```bash
  mcp__todo-mcp__context_set key:"doc_[name]_status" value:"PDF requested [date]"
  ```
- [ ] **Handoff notification** to human operator

### Phase 6: Post-Production
- [ ] **Check `/inbound/`** for completed PDF
- [ ] **Review PDF** for quality issues
- [ ] **Update Document Pipeline**: Status to ✅ Released
- [ ] **Update Dashboard**: Move from active to completed
- [ ] **Archive source files** if needed
- [ ] **Clean up `/outbound/`** directory

## 🔄 For Document Revisions

### Additional Steps for Revisions:
- [ ] **Create revision branch** or new version directory
- [ ] **Document changes** in revision log
- [ ] **Update version numbers** throughout
- [ ] **Preserve previous version** for reference
- [ ] **Note revision reason** in dashboard

## 🎨 Style Consistency Checklist

### For deSilva-Style Documents:
- [ ] Conversational voice with "Well, ..." corrections
- [ ] 60% examples, 40% theory ratio
- [ ] "Medicine Cabinet" simplifications
- [ ] "Uff!" moments after complexity
- [ ] Personal expressions maintained
- [ ] Empathetic acknowledgment of difficulty

### For Technical References:
- [ ] Clear hierarchical structure
- [ ] Consistent terminology
- [ ] Complete cross-references
- [ ] Verified technical accuracy
- [ ] Comprehensive index

## 📊 Dashboard Update Templates

### For Operations Dashboard:
```markdown
### [Document Name] v[X.Y]
**Status**: 🟢 [Current Status]  
**[Milestone]**: [Date]  
**Statistics**:  
- [Key metric 1]
- [Key metric 2]

**Current Blockers - Assets Needed**:
- 🔴 [Critical blocker]
- 🟡 [Medium priority]
- [→ Full Asset List](path/to/assets-needed.md)
```

### For Document Pipeline:
```markdown
### [Document Name]
**Status**: 🟢 [Status]  
**Source**: [Source description]  
**Format**: [Output format]  
**Audience**: [Target audience]  
**Location**: [Path]  
**Assets Needed**: [[Count] items](link)  
**Note**: [Current state/next steps]
```

## 🚨 Common Pitfalls to Avoid

1. **Forgetting dashboard updates** - Use this checklist!
2. **Missing assets documentation** - Create assets-needed.md immediately
3. **Wrong model choice** - Opus for prose, Sonnet for structure
4. **No version tracking** - Always include version in filenames
5. **Skipping context saves** - Essential for work resumption
6. **Not updating pipeline tracker** - Breaks visibility

## 📝 Global Markdown Formatting Fixes

### Bold Headings with Colons Before Lists
**Issue**: Lists don't render properly when placed directly after bold headings ending with colons  
**Pattern**: `**Heading:**` immediately followed by list items (no blank line)  
**Fix**: Add blank line between heading and list

**Example Before**:
```markdown
**The Smart Pin Advantage:**
- Item 1
- Item 2
```

**Example After**:
```markdown
**The Smart Pin Advantage:**

- Item 1
- Item 2
```

**Common Occurrences**:
- Executive summaries with feature lists
- Mode variant descriptions
- Advantage/disadvantage lists
- Configuration step lists

**Detection Pattern**: Search for `**.*:**` followed immediately by `\n-` or `\n*` or `\n1.`

### Headings Followed by Code Blocks
**Issue**: Code blocks placed directly after headings without blank line cause formatting issues  
**Pattern**: Any heading level (`#` through `######`) immediately followed by code fence  
**Fix**: Add blank line between heading and code block

**Example Before**:
```markdown
#### Step 2: Configure the Pin
```pasm2
wrpin mode, #pin
```
```

**Example After**:
```markdown
#### Step 2: Configure the Pin

```pasm2
wrpin mode, #pin
```
```

**Common Occurrences**:
- Tutorial step headings with code examples
- "Mistake" or "Anti-pattern" headings with bad code examples
- Configuration sections with code blocks
- Implementation headings with example code

**Detection Commands**:
```bash
# Find headings followed by code blocks
awk '/^#{1,6} .*$/ {heading=$0; line=NR; getline; if ($0 ~ /^```/) print line ": " heading}' document.md
```

### Regular Text with Colons Before Lists
**Issue**: Lists don't render when placed directly after regular text ending with colon  
**Pattern**: Non-heading text ending with `:` immediately followed by list  
**Fix**: Add blank line between text and list

**Example Before**:
```markdown
The system provides these features:
- Feature 1
- Feature 2
```

**Example After**:
```markdown
The system provides these features:

- Feature 1  
- Feature 2
```

**Common Occurrences**:
- Feature descriptions
- System capabilities
- Function parameter lists
- Architecture component lists

 followed by `\n-` or `\n*` or `\n1.`

### Horizontal Rules at Chapter/Section Ends
**Issue**: Horizontal rules (`---`) at chapter ends are redundant with clear headings  
**Pattern**: Lines containing only `---` typically at section boundaries  
**Fix**: Remove all horizontal rules - headings provide sufficient separation

**Example Before**:
```markdown
End of chapter content.

---

## Next Chapter
```

**Example After**:
```markdown
End of chapter content.

## Next Chapter
```

**Removal Command**:
```bash
# Remove all horizontal rules (macOS)
sed -i '' '/^---$/d' document.md

# Remove all horizontal rules (Linux)
sed -i '/^---$/d' document.md
```

**Rationale**:
- Chapter headings provide clear visual separation
- Reduces visual clutter in rendered output
- PDF formatting will add natural breaks at chapters
- Cleaner, more professional appearance

## 🔗 Related Documents

- [PDF Workflow](pdf-workflow.md) - Technical PDF generation
- [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) - Doc-forge requirements
- [Document Production Pipeline](document-production-pipeline.md) - Status tracking
- [Operations Dashboard](../../README.md) - Project visibility

## 📝 Process Improvement

If you identify improvements to this process:
1. Update this document
2. Note change in revision history below
3. Update any affected templates

---

## Revision History

- **2025-08-20**: Initial creation after P2 Manual v1.0 experience
  - Added comprehensive checklist
  - Included dashboard update requirements
  - Created templates for consistency
  - Added assets tracking process
- **2025-08-29**: Added global markdown formatting fixes section
  - Documented bold heading with colon list rendering issue
  - Added detection pattern and fix instructions
  - Added heading + code block formatting issue  
  - Added regular text with colon + list formatting issue
  - Added horizontal rule removal guidance