# PDF Generation Workflow v2.0 (LaTeX/Pandoc)
## 🔴⚡️ THE DEFINITIVE WORKFLOW - NO DEVIATIONS ALLOWED ⚡️🔴

Created: 2025-08-21
Reason: Previous workflow led to damaged masters and repeated errors due to ambiguous file states
**This is THE stake in the ground for how we do PDF generation**

## ⛔️ SESSION START CHECKPOINT - READ THIS FIRST EVERY TIME
**Before ANY PDF work, confirm you understand:**
- [ ] I will NEVER edit files in opus-master/ directory
- [ ] I will NEVER skip the protection step for Opus documents  
- [ ] I will NEVER use ambiguous suffixes like FINAL or COMPLETE
- [ ] I will NEVER manually patch escape issues more than once
- [ ] I will ALWAYS follow the exact directory structure below
- [ ] I will ALWAYS stop work at 3-hour mark or warning signs
- [ ] I understand violating these rules wastes hours and damages files

**If you cannot check ALL boxes, DO NOT proceed with PDF work.**

**Note**: For Pages/docx workflow, see `pdf-generation-methodology.md`

## 🔴 CRITICAL: Protect Opus-Generated Masters IMMEDIATELY

### ⚡️ VIOLATION = CATASTROPHIC LOSS ⚡️
**When Opus generates a complete document, PROTECT IT IMMEDIATELY:**
**NO EXCEPTIONS - Not "after this edit", not "in a minute" - IMMEDIATELY**

```bash
# 1. Move to sacred location
mv generated-document.md workspace/[doc-name]/opus-master/COMPLETE-OPUS-MASTER.md

# 2. Make read-only
chmod 444 workspace/[doc-name]/opus-master/COMPLETE-OPUS-MASTER.md

# 3. Create README-SACRED.md documenting:
#    - Generation date and model
#    - File size for verification  
#    - What it contains
#    - Why it's protected
```

**Why This Matters:**
- **Opus time is expensive** - These documents cost real money to generate
- **Cannot be perfectly regenerated** - Exact context and responses are unique
- **Easy to accidentally damage** - One wrong escape/edit can corrupt
- **Nearly lost one already** - Found De Silva master in archive-old by luck!

**Real Example:** On Aug 22, 2025, we almost lost a 61KB, 16-chapter manual because it wasn't properly protected. Found it by luck in an archive folder.

## 🔴 CRITICAL: Directory Structure & File States

### Mandatory Directory Structure
```
/exports/pdf-generation/
├── workspace/
│   └── [document-name]/
│       ├── opus-master/    # 🔴 SACRED - Never edit! chmod 444
│       │   ├── COMPLETE-OPUS-MASTER.md
│       │   └── README-SACRED.md
│       ├── parts-extracted/ # 📋 Clean extractions from master
│       │   ├── Part1-EXTRACTED.md
│       │   └── Part2-EXTRACTED.md
│       ├── editing/        # ⚠️ WORKING FILES - Human-readable, may have issues
│       │   └── *-WORKING.md
│       ├── ready/          # ✅ CLEAN FILES - Ready to process, no bold markers
│       │   └── *-READY.md  
│       └── templates/      # 📄 LaTeX templates for this document
│           └── *.latex
├── outbound/
│   └── [document-name]/    # 🚀 DEPLOYMENT - One part at a time
│       ├── Part1-Name.md  # ONLY current working file
│       ├── request.json   # Points to current part
│       ├── [template.latex] # Only when template changes
│       └── last-deployed/ # 📋 REFERENCE - Copy of what was sent to PDF Forge
│           ├── *.md       # Snapshot for quick recovery
│           ├── *.latex    # Cleared when moving to next part
│           └── request.json
└── inbound/                # 📥 FINAL PDFs only (no subfolders)
    └── [Final-Manual].pdf  # Human drops completed manual here
```

### P2KB Template Naming Convention
**All templates MUST use P2KB prefix**: `p2kb-[purpose].latex`
- Example: `p2kb-pasm-desilva.latex`
- Benefits: No conflicts, clear ownership, consistent branding

### File Naming States
**MANDATORY SUFFIXES - Never use ambiguous names like FINAL, CLEAN, or COMPLETE**

| Suffix | State | Description | Can Edit? | Can Escape? |
|--------|-------|-------------|-----------|-------------|
| `-WORKING` | In progress | Has bold markers, may have errors | YES | NO |
| `-READY` | Clean master | No bold markers, verified clean | NO | YES |
| `-ESCAPED` | Processed | LaTeX escaped, ready for PDF | NO | NO |

### State Transitions (ONE WAY ONLY)
```
WORKING → READY → ESCAPED → PDF
   ↓        ↓        ↓
 editing/  ready/  outbound/
```

**NEVER GO BACKWARDS** - If you need to edit, start fresh from WORKING

## 📋 Pre-Flight Checklist (MANDATORY)

Before ANY escape operation:
- [ ] Source file is in `ready/` directory
- [ ] Source file has `-READY` suffix
- [ ] Output goes to `outbound/` directory
- [ ] Template has been tested with small sample
- [ ] Escape script regression tests pass
- [ ] No previous escaped version exists (or explicitly overwriting)

## 🚀 Workflow Steps

### Step 1: Prepare Working File
```bash
# In workspace/[document]/editing/
- Follow checklist: document-generation-process.md
- Edit Part1-WORKING.md
- Add content, formatting, bold markers for instructions
- This is your scratch space
```

### Step 2: Create Ready Version
```bash
# Remove bold markers and prepare for escaping
python3 tools/uppercase-instructions-latex.py \
  workspace/[document]/editing/Part1-WORKING.md \
  workspace/[document]/ready/Part1-READY.md

# VERIFY: Check that file has no bold markers, no partial escaping
grep "**" workspace/[document]/ready/Part1-READY.md  # Should return nothing
grep "\\\\" workspace/[document]/ready/Part1-READY.md # Should return nothing
```

### Step 3: Escape for LaTeX (MANDATORY - ALWAYS RUN)
```bash
# ALWAYS escape from ready/ to outbound/ - This step is MANDATORY
# The script is idempotent and ensures consistent processing
./tools/latex-escape-all.sh \
  workspace/[document]/ready/Part1-READY.md \
  outbound/[document]/[document].md

# CRITICAL: This step MUST be run every time, no exceptions
# The script handles all escaping needs and preserves LaTeX environments

# VERIFY: Check escape report
# If ANY unescaped characters remain (except in protected environments):
# STOP - Do not manually fix - Fix the script properly
# NOTE: Verification may show false positives for ^ characters - check actual file
```

### Step 4: Deploy Files
```bash
# Copy template
cp workspace/[document]/templates/p2kb-[name].latex \
   outbound/[document]/p2kb-[name].latex

# Copy Lua filter if using div syntax
cp workspace/[document]/filters/div-to-environment.lua \
   outbound/[document]/div-to-environment.lua

# Create request.json in outbound/[document]/
# CRITICAL: Check workspace for request-requirements.json first!

# 1. CHECK FOR SPECIAL REQUIREMENTS
if [ -f workspace/[document]/request-requirements.json ]; then
  # Document needs special Pandoc arguments
  # Merge requirements into standard template
fi

# 2. STANDARD REQUEST STRUCTURE (merge with requirements if present)
{
  "documents": [{
    "input": "[document-name].md",
    "output": "[document-name].pdf",
    "template": "p2kb-[template-name]",  # NO .latex extension!
    "pandoc_args": [                     # FROM request-requirements.json
      "--top-level-division=part"         # Smart Pins example
    ],
    "variables": {  # or "metadata" - both work
      "title": "...",
      "subtitle": "...",
      "author": "P2 Knowledge Base Team",
      "date": "...",
      "version": "...",
      "footer": "..."
    }
  }]
}
```

### 📋 CRITICAL: Request-Requirements.json Pattern (MANDATORY)

**ALWAYS check workspace for `request-requirements.json` before creating request.json**

#### What is request-requirements.json?
**Purpose**: Documents with special Pandoc arguments store requirements separately from deployment files
**Location**: `workspace/[document-name]/request-requirements.json`
**Why needed**: Special arguments get lost during copy operations, requirements file preserves them

#### Standard Format:
```json
{
  "required_pandoc_args": ["--top-level-division=part"],
  "reason": "Smart Pins uses Part/Chapter structure - # headers become \\part{}, ## headers become \\chapter{}",
  "discovered": "2025-08-25",
  "issue": "Without this, Pandoc defaults to chapter-level division and parts don't get page breaks"
}
```

#### When Documents Need Special Requirements:
- **Part/Chapter structure**: `--top-level-division=part`
- **Custom filters**: `--lua-filter=custom-filter`
- **Bibliography**: `--citeproc`
- **Math rendering**: `--mathml` or `--webtex`
- **Table processing**: `--columns=80`

#### Deployment Process:
1. **Check workspace** for `request-requirements.json`
2. **If present**: Extract `required_pandoc_args` and merge into request.json
3. **If copying from last-deployed**: Use existing request.json (already has requirements merged)
4. **Deploy** complete request.json with all arguments

#### Example Implementations:

**Smart Pins (Part/Chapter Structure)**:
```json
// workspace/smart-pins-manual/request-requirements.json
{
  "required_pandoc_args": ["--top-level-division=part"],
  "reason": "Parts need proper page breaks and numbering"
}

// Merged into outbound/request.json as:
"pandoc_args": ["--top-level-division=part"]
```

**Document with Lua Filter**:
```json
// workspace/advanced-manual/request-requirements.json
{
  "required_pandoc_args": ["--lua-filter=div-to-environment"],
  "reason": "Converts ::: blocks to LaTeX environments"
}

// Merged into outbound/request.json as:
"pandoc_args": ["--lua-filter=div-to-environment"]
```

#### Rules for request-requirements.json:
- **Always version controlled** - Lives in workspace, committed to git
- **Document-specific** - Each document that needs special args has one
- **Never lost** - Survives copy operations and file moves
- **Self-documenting** - Includes reason and discovery date
- **Merge target** - Gets merged into request.json, not used directly

#### Common Mistakes to Avoid:
❌ **Forgetting to check** workspace for requirements file
❌ **Manually adding** pandoc_args without documenting in requirements
❌ **Losing requirements** during file copies
❌ **Inconsistent merging** - missing args from final request.json

#### Recovery Protocol:
If PDF generation fails with "unknown option" or structure errors:
1. **Check workspace** for `request-requirements.json`
2. **Verify merging** - Ensure all `required_pandoc_args` in final request.json
3. **Test incrementally** - Add one arg at a time to isolate issues

**This pattern prevents the most common PDF generation failures caused by missing Pandoc arguments.**

### Step 5: Deploy to PDF Forge

#### 🔴 MANDATORY DEPLOYMENT PROCESS
**The Golden Rule**: `last-deployed/` = Complete set of what Claude last gave to user

#### 5a. ALWAYS Deploy to BOTH Locations
```bash
# MANDATORY: Every file deployment goes to BOTH locations
# Even if updating just ONE file (e.g., only template changed):

# 1. Deploy to main directory (for user to move to PDF Forge)
cp [source-file] outbound/[document]/

# 2. Deploy to reference copy (Claude's record)
cp [source-file] outbound/[document]/last-deployed/

# Standard full deployment example:
cp ready/[document]-ESCAPED.md outbound/[document]/[document].md
cp ready/[document]-ESCAPED.md outbound/[document]/last-deployed/[document].md

cp templates/p2kb-*.latex outbound/[document]/
cp templates/p2kb-*.latex outbound/[document]/last-deployed/

cp outbound/[document]/request.json outbound/[document]/last-deployed/
```

**CRITICAL Rules**:
- **Never partial updates** to `last-deployed/` - it's always the complete set
- **Even single file changes** go to BOTH locations
- **Never skip** the `last-deployed/` copy - it's how Claude knows what you have
- **Never hunt for files** after deployment - they're in `last-deployed/`

**Purpose of last-deployed/**:
- Truth source when user moves files to PDF Forge (main directory empties)
- Reference for "what exact files does user have on PDF Forge?"
- Prevents file hunting and confusion in future sessions
- **CLEARED when moving to next major part** (Part 1→2, Part 2→3)

#### 5b. User Takes to PDF Forge
- User moves files from outbound/ main directory to PDF Forge
- outbound/ main becomes empty (this is normal)
- last-deployed/ retains copies for reference
- PDFs remain on PDF Forge for tracking

#### 5c. Between Parts Cleanup
```bash
# When FINISHED with Part 1 and moving to Part 2:
rm -rf outbound/[document]/last-deployed/*
# Start fresh for Part 2
```

## 🎯 Understanding PDF Forge Behavior

### How PDF Forge Works (External System)

**PDF Forge is an external system with specific file handling behaviors:**

#### On SUCCESS (PDF generates correctly):
1. **PDF Forge ARCHIVES the input files:**
   - Moves markdown file aside (archived/cleaned)
   - Moves request.json aside (archived/cleaned)
   - Template may remain (depends on configuration)
   - Working directory is cleared for next job

2. **What Claude must provide for NEXT part:**
   - ✅ New markdown file (e.g., Part2.md)
   - ✅ Updated request.json (pointing to new markdown)
   - ✅ Template file (if changed or not present)
   - **All THREE files needed for fresh start**

#### On FAILURE (PDF generation error):
1. **PDF Forge PRESERVES the input files:**
   - Keeps markdown file in place
   - Keeps request.json in place
   - Template remains available
   - Ready for retry after fix

2. **What Claude must provide to FIX:**
   - ✅ ONLY the file that needs fixing (usually template)
   - ❌ Do NOT regenerate markdown (it's still there)
   - ❌ Do NOT regenerate request.json (it's still there)
   - **Just ONE file needed for retry**

#### Practical Examples:

**Example 1: Template Error (like today)**
```
Error: ! LaTeX Error: Environment sidetrack undefined.

Action: 
1. Fix template in templates-workspace/
2. Copy ONLY template to outbound/
3. User moves ONLY template to PDF Forge
4. Re-run (markdown + request still there)
```

**Example 2: Successful Part 1, Starting Part 2**
```
Success: Part1.pdf generated

Action:
1. Prepare Part2.md in workspace/
2. Update request.json for Part2
3. Copy ALL files to outbound/
4. User moves ALL files to PDF Forge
5. Run Part 2 generation
```

#### Why This Matters:
- **Errors are actually EASIER** - just fix one file
- **Success requires MORE work** - stage everything fresh
- **Never look in outbound/** - it's just a transit zone
- **Always work from workspace/** - that's where masters live

### Step 6: Final Manual Delivery
- When all parts complete, user drops final PDF in `/inbound/`
- No subfolders needed - Claude recognizes the manual
- Claude moves to versioned release location
- Claude updates documentation with release link

## 🎨 P2KB TEMPLATE DEVELOPMENT & MANAGEMENT WORKFLOW

### 🔴 CRITICAL: Template Canonical Naming Principle
**FUNDAMENTAL RULE**: Templates maintain SAME NAME across ALL locations
- ✅ `p2kb-smart-pins.latex` everywhere (workspace, outbound, PDF Forge)
- ❌ NEVER use state suffixes like `-WORKING`, `-READY`, `-COMPLETE`
- ❌ NEVER rename templates during workflow transitions

**Why This Matters**: 
- Templates are shared across multiple documents
- Name changes break cross-document compatibility
- Different from document files which DO use state suffixes

### 🔴 CRITICAL: P2KB Naming Convention (MANDATORY)
**ALL P2 Knowledge Base templates MUST use P2KB prefix:**

**Format**: `p2kb-[purpose].latex`
- **Prefix**: `p2kb-` (Papa Two Kilo Bravo)
- **Purpose**: Descriptive name (smart-pins, pasm-desilva, user-guide)
- **Extension**: `.latex` for LaTeX template files

**Examples**:
- `p2kb-smart-pins.latex` - Smart Pins reference formatting
- `p2kb-pasm-desilva.latex` - De Silva-style PASM2 manual formatting
- `p2kb-user-guide.latex` - General user guide formatting

**Benefits**:
- Prevents conflicts with existing doc-forge templates
- Clear P2 Knowledge Base ownership and branding
- Easy identification and grouping in file listings
- Consistent project-wide template naming

### 📁 Template Directory Architecture

#### 🔴 Protected Masters (SACRED - chmod 444)
```
/documentation/pdf-templates-master/p2kb-current-gold-standard/
├── p2kb-foundation.sty          # 🔴 MASTER - Core styling (8,708 bytes)
├── p2kb-smart-pins-content.sty  # 🔴 MASTER - Smart Pins content styling
├── p2kb-smart-pins.latex        # 🔴 MASTER - Complete Smart Pins template
├── p2kb-pasm-desilva.latex     # 🔴 MASTER - Complete De Silva template
├── p2kb-tech-review.sty         # 🔴 MASTER - Technical review styling
└── p2kb-presentation.sty        # 🔴 MASTER - Presentation layer styling
```

**PROTECTION PROTOCOL**:
```bash
# ALWAYS protect masters immediately after creation/update
chmod 444 /documentation/pdf-templates-master/p2kb-current-gold-standard/*
```

#### ⚙️ Development Workspace
```
/exports/pdf-generation/workspace/manual-templates/
├── p2kb-foundation.sty          # Working copy for development
├── p2kb-smart-pins-content.sty  # Working copy for development
├── p2kb-smart-pins.latex        # Working copy for development
├── p2kb-pasm-desilva.latex     # Working copy for development
├── p2kb-tech-review.sty         # Working copy for development
├── p2kb-presentation.sty        # Working copy for development
└── experiments/                  # Test versions and experiments
    ├── test-variations/
    └── archived-attempts/
```

#### 🚀 Document-Specific Templates
```
/exports/pdf-generation/workspace/[document-name]/templates/
└── p2kb-[document-specific].latex  # Document-customized template
```

### 🔧 Template Development Workflow

#### Phase 1: Development & Testing
```bash
# 1. Work in development workspace
cd /exports/pdf-generation/workspace/manual-templates/

# 2. Edit template (never edit protected masters directly)
edit p2kb-[template-name].latex

# 3. Test with minimal sample
cp p2kb-[template-name].latex /exports/pdf-generation/outbound/test-document/
# User tests on PDF Forge with small sample content

# 4. Iterate until working
# Fix issues, repeat steps 2-3 until PDF generates correctly
```

#### Phase 2: Shared Template Impact Analysis (MANDATORY)
**CRITICAL**: Before updating any foundation or shared .sty files:

```bash
# 1. IDENTIFY ALL CONSUMERS
# Check which documents use this template component
grep -r "p2kb-foundation" /exports/pdf-generation/workspace/*/templates/
grep -r "p2kb-[template-name]" /documentation/manuals/*/

# 2. ASSESS IMPACT
# List all documents that will be affected by changes:
#   - Smart Pins Manual
#   - PASM2 De Silva Manual  
#   - [Other documents using this template]

# 3. PLAN TESTING
# Prepare to test ALL affected documents, not just current one
# Changes to foundation styles affect EVERYTHING
```

**SHARED TEMPLATE COMPONENTS**:
- `p2kb-foundation.sty` - Affects ALL P2KB documents
- `p2kb-tech-review.sty` - Affects ALL technical review documents
- `p2kb-presentation.sty` - Affects ALL presentation-layer formatting

**DOCUMENT-SPECIFIC TEMPLATES**:
- `p2kb-smart-pins.latex` - Only affects Smart Pins documents
- `p2kb-pasm-desilva.latex` - Only affects De Silva-style documents

#### Phase 3: Master Update & Protection
```bash
# 1. Update protected master (requires unlocking)
chmod 644 /documentation/pdf-templates-master/p2kb-current-gold-standard/p2kb-[name].latex
cp workspace/manual-templates/p2kb-[name].latex \
   /documentation/pdf-templates-master/p2kb-current-gold-standard/

# 2. Re-protect immediately
chmod 444 /documentation/pdf-templates-master/p2kb-current-gold-standard/p2kb-[name].latex

# 3. Document the change
echo "Updated $(date): [description of changes]" >> \
  /documentation/pdf-templates-master/p2kb-current-gold-standard/CHANGELOG.md
```

#### Phase 4: Document Integration
```bash
# 1. Copy to document-specific location
cp /documentation/pdf-templates-master/p2kb-current-gold-standard/p2kb-[name].latex \
   workspace/[document-name]/templates/

# 2. Deploy for production use
cp workspace/[document-name]/templates/p2kb-[name].latex \
   outbound/[document-name]/
```

### 🔬 Template Testing Protocol

#### Minimal Sample Testing
**ALWAYS test templates with small sample before full document**:

```bash
# 1. Create minimal test content
echo "# Test Document\n\nMinimal content for template testing." > test-minimal.md

# 2. Create test request.json
{
  "documents": [{
    "input": "test-minimal.md",
    "output": "test-minimal.pdf",
    "template": "p2kb-[template-name]"
  }]
}

# 3. Deploy to outbound/test-template-[name]/
# 4. User tests on PDF Forge
# 5. If successful, proceed to full document
```

#### Full Document Testing
**Only after minimal sample succeeds**:
```bash
# Deploy full document with updated template
# Follow standard workflow Steps 3-5
```

### 🚨 Template Error Recovery

#### Template Generation Errors
**If PDF generation fails with template errors**:

```bash
# 1. IDENTIFY EXACT ERROR
# Check PDF Forge error message for specific LaTeX error
# Example: "Environment sidetrack undefined"

# 2. FIX IN DEVELOPMENT WORKSPACE ONLY
edit /exports/pdf-generation/workspace/manual-templates/p2kb-[template].latex
# Fix the specific issue (add missing environment, fix syntax, etc.)

# 3. TEST FIX WITH MINIMAL SAMPLE
# Use minimal sample testing protocol above

# 4. DEPLOY ONLY TEMPLATE (NOT full document)
# PDF Forge preserves markdown and request.json on failure
# Only copy the fixed template file
cp workspace/manual-templates/p2kb-[template].latex outbound/[document]/

# 5. USER DEPLOYS ONLY TEMPLATE TO PDF FORGE
# Re-run generation (markdown + request.json still there)
```

#### Template Recovery Principles
- **Incremental fixes**: Change ONE thing at a time
- **Minimal deployment**: Only deploy what changed
- **Test progression**: Minimal sample → Full document
- **Never mass-replace**: Fix specific issues, don't recreate

### 📋 Template Workflow Checklist

#### Before Template Development:
- [ ] Template follows P2KB naming convention (`p2kb-[name].latex`)
- [ ] Working in development workspace, NOT protected masters
- [ ] Identified all documents that will be affected by changes
- [ ] Planned testing strategy for shared components

#### During Development:
- [ ] Testing with minimal sample first
- [ ] Making incremental changes only
- [ ] Documenting specific issues and fixes
- [ ] Following canonical naming (same name everywhere)

#### Before Master Update:
- [ ] Template successfully generates PDF
- [ ] All affected documents tested (for shared components)
- [ ] Ready to protect updated master immediately
- [ ] Change documented in CHANGELOG.md

#### After Master Update:
- [ ] Master re-protected (chmod 444)
- [ ] Working copies updated from master
- [ ] Document-specific templates updated
- [ ] Production deployment successful

### 🔴 Template Workflow Violations & Consequences

#### NEVER DO THESE:
- ❌ Edit protected masters directly (breaks protection paradigm)
- ❌ Use state suffixes in template names (breaks canonical naming)
- ❌ Deploy untested templates to production documents
- ❌ Skip shared component impact analysis
- ❌ Update templates without minimal sample testing
- ❌ Use non-P2KB naming convention

#### Violation Consequences:
- **Direct master editing**: Loss of template protection, potential corruption
- **Name variations**: Cross-document compatibility breaks
- **Untested deployment**: Document generation failures, wasted time
- **Skipping impact analysis**: Breaks other documents unexpectedly
- **Non-P2KB naming**: Template conflicts, confusion

### 📚 Template Architecture Understanding

#### Layered Template System
**Templates build in layers** (see `/documentation/pdf-forge-system/layered-template-architecture.md`):

1. **Foundation Layer** (`p2kb-foundation.sty`)
   - Core document structure
   - Basic typography and spacing
   - Universal P2KB branding

2. **Content Layer** (`p2kb-[content-type]-content.sty`)
   - Content-specific environments (sidetrack, interlude)
   - Specialized formatting for content type
   - Content-aware styling

3. **Presentation Layer** (`p2kb-presentation.sty`)
   - Visual polish and refinement
   - Color schemes and visual hierarchy
   - Print-ready finishing touches

4. **Complete Templates** (`p2kb-[document].latex`)
   - Combines all layers for specific document type
   - Document-specific customizations
   - Ready for production use

#### Template Modification Strategy
**Choose the right layer for your changes**:
- **Universal changes**: Modify `p2kb-foundation.sty`
- **Content-type changes**: Modify content-specific .sty files
- **Document-specific changes**: Modify document .latex files
- **Visual polish**: Modify `p2kb-presentation.sty`

## 🛑 STOP SIGNALS - When to Halt Work

### ⚡️ MANDATORY STOP TRIGGERS - NO NEGOTIATION ⚡️
**When these occur, STOP IMMEDIATELY - Do not "just finish this one thing":**

1. **Same bug encountered 3+ times** 
   → STOP, document in FRICTION_LOG, clear session
   → Violation example: Manually fixing `2^9` repeatedly instead of fixing script
   
2. **Manually patching same issue repeatedly** 
   → STOP, fix root cause with regression test
   → Violation example: Adding `\` to every `^` by hand
   
3. **Confusion about file states** 
   → STOP, verify directory structure matches this guide exactly
   → Violation example: "Is this the ready version or working?"
   
4. **3-4 hours elapsed** 
   → STOP, checkpoint, clear conversation - NO EXCEPTIONS
   → Violation result: Quality degrades exponentially after 3 hours
   
5. **Files in wrong directories** 
   → STOP, reorganize first, then continue
   → Violation example: Editing files directly in outbound/

### 🟡 Warning Signs (Complete current atomic task ONLY, then stop)
- Starting to forget recent changes
- Making contradictory decisions  
- Files have ambiguous names (FINAL-v2-CLEAN-COMPLETE.md)
- Escape script showing unexpected errors
- Multiple backup files accumulating
- Asking "What was I doing?" more than once

## 🔧 Recovery Procedures

### If Master Damaged
1. Check backups: `ls -la *backup*`
2. Find pre-damage `-WORKING` version
3. Start fresh from there
4. Document cause

### If State Confused
- `**text**` = WORKING (has bold)
- `\\#` = ESCAPED (LaTeX ready)
- Clean text = READY
→ Move to correct directory, rename with suffix

## 📝 Session Management

### At Session Start
```bash
mcp__todo-mcp__context_resume  # Check previous state
# Look for:
# - critical_escape_script_bug
# - current_deliverables_ready
# - session_escape_workflow_lesson
```

### Before Clearing Session
```bash
# Document current state
mcp__todo-mcp__context_set key:"pdf_generation_state" \
  value:"Working=[files], Ready=[files], Outbound=[files], Issues=[any problems]"

# Note session duration and why clearing
mcp__todo-mcp__context_set key:"session_clear_reason_[timestamp]" \
  value:"Duration: Xh, Reason: [specific trigger]"
```

## 🔬 Regression Testing Critical Scripts

### LaTeX Escape Script Testing
**Location**: `/tools/latex-escaping-regression/`

**🔴 CRITICAL: Prove Failure Before Fix**
1. Add failing case to `input/test-cases.md`
2. Update `golden/test-cases-GOLDEN.md` with expected output
3. **Run `./test-runner.sh` - MUST show FAIL** (proves bug exists)
4. Fix script to handle the case
5. **Run `./test-runner.sh` - MUST show PASS** (proves fix works)

**Class Problem Principle**:
- One bug = entire class of bugs
- `\item` broken? → Fix ALL list commands (`\item`, `\begin{itemize}`, etc.)
- `2^9` unescaped? → Fix ALL math (`^`, `_`, `$`, etc.)
- Template env broken? → Fix ALL environments (sidetrack, interlude, etc.)

**Violation = Repeated Manual Patches** (5+ hours wasted on same bug)

## 🐛 Known Issues to Fix

### Issue: Escape Script Bug with Template Environments
- **Problem**: Content inside `\begin{sidetrack}`, `\begin{interlude}`, etc. not being escaped
- **Example**: `2^9` not becoming `2\^{}9` inside sidetrack
- **Status**: Needs regression test and fix
- **Workaround**: NONE - Do not manually patch

## 📚 Related Documentation
- `/pipelines/pdf-generation-format-guide.md` - Overall PDF pipeline
- `/documentation/pipelines/document-production-pipeline.md` - Document workflow

## ⚡️ ENFORCEMENT & ACCOUNTABILITY ⚡️

### This Document is LAW
**Every deviation from this workflow:**
- Wastes 3-5 hours minimum
- Risks losing irreplaceable Opus content ($$ and time)
- Creates cascading errors requiring session clears
- Degrades final output quality

### Session Start Ritual (MANDATORY)
```bash
# 1. Read the checkpoint at top of this document
# 2. Check all boxes mentally
# 3. Run context resume to check for warnings
mcp__todo-mcp__context_resume

# 4. Look for red flags from previous session:
# - "manual_patch_count" > 2
# - "session_duration" > 3 hours  
# - "confusion_about_file_states"
```

### Quality Gates (NO PROCEEDING WITHOUT)
- **Before escaping**: All files in correct directories with correct suffixes
- **Before manual edit**: Is this the 2nd time fixing this? STOP if yes
- **Before continuing**: Has it been 3 hours? STOP if yes
- **Before any deviation**: Will this save time? (Answer is always NO)

### The Cost of Deviation
**Last night's session (degraded after 4+ hours):**
- Created wrong directory structures  
- Confused file states
- Made contradictory decisions
- Required complete reorganization
- **Result**: 5+ hours of rework

**The solution was already in this document.**

### Remember
- **This workflow exists because we learned these lessons the hard way**
- **Every rule here prevented a specific catastrophe**
- **Following it exactly is ALWAYS faster than any "shortcut"**
- **When in doubt, re-read this document - don't guess**

## Version History
- v2.0 (2025-08-21): Complete rewrite with strict separation after file damage incident
- v1.0: Original version (deprecated due to ambiguous states) - see `pdf-generation-workflow-v1.md`