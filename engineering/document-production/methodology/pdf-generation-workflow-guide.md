# PDF Generation Format Guide - RECOVERED CONTENT - DeSilva Specific

**CRITICAL**: This is recovered content after data loss incident on 2025-08-21
**Original size**: 3740 lines  
**Recovered**: Partial content from conversation memory
**Status**: INCOMPLETE - Major content still missing

## 🔧 PDF Forge Installation Requirements

### ✅ Current Installation Status (2025-08-20)
**PDF Forge now has complete LaTeX installation**:
```bash
# Complete TeXLive installation command used:
sudo apt-get install texlive-full
```

### What texlive-full Provides
| Component | Included | Benefits |
|-----------|----------|----------|
| **ALL LaTeX packages** | Complete distribution | No missing dependencies |
| **XeLaTeX engine** | Modern font handling | Unicode support, Charter fonts |
| **tcolorbox with ALL libraries** | skins, breakable, etc. | Advanced colored boxes with dashed borders |
| **Font packages** | Charter, Palatino, etc. | Professional typography |
| **Graphics packages** | TikZ, PGF complete | Complex diagrams and borders |
| **Math packages** | amsmath, amsfonts, etc. | Mathematical typesetting |

## 🎨 Visual Element Requirements (deSilva Style)

### Color-Coded Content Boxes
- 🚧 **Violet boxes** (`missingviolet`) = Missing content placeholders
- 🔍 **Orange boxes** (`revieworange`) = Needs review sections  
- 🎨 **Blue boxes** (`diagramblue`) = Diagrams needed
- **Gray boxes with dashed borders** = Sidetracks (MANDATORY dashed, not solid)
- **Gray boxes without borders** = Interludes
- **Light blue boxes** = "Your Turn" exercises (changed from yellow to avoid conflict)
- **Green tinted boxes** = Chapter endings

### Typography Requirements
- **Font**: Charter/Palatino (NOT Computer Modern)
- **Footer**: Must appear on every page
- **Chapter numbering**: Proper format (Chapter N, not 0.N)
- **Page breaks**: Each chapter starts on new page

## 🚫 LaTeX Debugging Solutions

### Common "Missing $ inserted" Errors
**Root Cause**: LaTeX special characters in assembly code

### Critical Character Escaping Rules
```
Assembly immediate values:
##1000000 → \#\#1000000
#0 → \#0

Dollar signs in text:
$1_0000_0000 → \$1\_0000\_0000

Underscores:
variable_name → variable\_name

Exponents:
e^2 → e\^{}2
```

## 📝 Template Management Workflow

### Master Template System
- **Template name**: `p2kb-pasm-desilva.latex`
- **Location**: `/documentation/pdf-templates-master/`
- **Requirements**: 
  - tcolorbox with enhanced features
  - Dashed border capability
  - Color definitions for all content types
  - Chapter formatting with proper numbering

## 🚀 PDF Generation Workflow

### File Preparation
1. **Create** markdown content with proper escaping
2. **Prepare** request.json configuration
3. **Transfer** files to PDF Forge
4. **Execute** generation command
5. **Verify** output quality

### Request.json Format
```json
{
  "documents": [{
    "input": "document.md",
    "output": "document.pdf", 
    "template": "p2kb-pasm-desilva",
    "variables": {
      "title": "Document Title",
      "subtitle": "Subtitle",
      "version": "1.0",
      "date": "Date",
      "author": "Author",
      "footer": "Footer Text"
    }
  }],
  "options": {
    "cleanup": true,
    "archive": true,
    "optimize": true
  }
}
```

## ⚠️ MAJOR CONTENT LOST

## 🔧 PDF Forge System Architecture - COMPLETE DETAILS

### Environment Specifications
- **Base**: Node.js 20 on Debian Bookworm
- **PDF Engine**: XeLaTeX (Unicode + professional fonts)
- **User**: `node` (non-root security model)
- **Working Directory**: `/workspace/`

### Complete Package Inventory
- **Core**: pandoc, texlive-full (4GB complete LaTeX)
- **Fonts**: Liberation, Noto, Noto-CJK, FiraCode
- **Graphics**: librsvg2-bin, imagemagick, poppler-utils, ghostscript
- **Python Filters**: pandoc-include, pandoc-plantuml-filter, pandoc-mustache, panflute, pypandoc, weasyprint
- **Development**: markdownlint-cli, prettier, serve, make, jq, inotify-tools

### Directory Structure
```
/workspace/
├── inbox/          # Input files (MD, request.json)
├── outbox/         # Generated PDFs  
├── templates/      # User LaTeX templates
├── output/         # Intermediate files
├── logs/           # Generation logs
└── config/         # Configuration files
```

### Package Verification Commands
```bash
# All these should return file paths:
kpsewhich tcolorbox.sty         # ✅ Advanced colored boxes
kpsewhich tikz.sty              # ✅ Graphics and borders
kpsewhich charter.sty           # ✅ Charter font
kpsewhich soul.sty              # ✅ Text highlighting
xelatex --version               # ✅ XeLaTeX engine
```

### Advanced Features Now Supported
- **Dashed/dotted borders**: `borderline={1pt}{0pt}{gray!50, dashed}`
- **Enhanced tcolorbox**: All skin libraries available
- **Professional fonts**: Charter, Palatino, Latin Modern
- **Graphics**: TikZ for complex diagrams
- **Math**: Complete mathematical typesetting
- **Unicode**: Full international character support

### Why texlive-full vs Individual Packages
| Approach | Size | Reliability | Features |
|----------|------|-------------|----------|
| **Individual packages** | ~1GB | Dependency issues possible | Limited |
| **texlive-full** | ~4GB | 100% reliable | Complete |

## 🏗️ Template Architecture

### Master Template Location
- **Path**: `/documentation/pdf-templates-master/p2kb-pasm-desilva.latex`
- **Purpose**: Single source of truth for all P2 manual formatting
- **Version Control**: Template changes tracked, not working copies

### Template Components
```latex
% Core packages required
\usepackage[utf8]{inputenc}
\usepackage{charter}          % Primary font
\usepackage{xcolor}
\usepackage[most]{tcolorbox}  % CRITICAL: [most] for all features
\tcbuselibrary{skins,breakable}
\usepackage{mdframed}
\usepackage{soul}
\usepackage{listings}
\usepackage{array}           % Enhanced table formatting
\usepackage{calc}            % Mathematical calculations
```

### Color Definitions (EXACT)
```latex
\definecolor{codegray}{HTML}{F5F5F5}
\definecolor{inlineyellow}{HTML}{FFFACD}
\definecolor{missingviolet}{HTML}{E6E6FA}
\definecolor{revieworange}{HTML}{FFE4B5}
\definecolor{diagramblue}{HTML}{E0F2FF}
\definecolor{chaptergreen}{HTML}{F0FFF0}
\definecolor{yourturncolor}{HTML}{E6F3FF}
```

## 🎨 Visual Element Specifications

### Sidetrack Box (Dashed Borders - MANDATORY)
```latex
\newtcolorbox{sidetrack}{
  enhanced,
  colback=codegray,
  colframe=gray!50,
  boxrule=0pt,
  borderline={1pt}{0pt}{gray!50, dashed},
  title={\textbf{Sidetrack}},
  fonttitle=\bfseries\color{black},
}
```

### Content Flag Boxes
```latex
% Missing content: Violet with thick border
\newtcolorbox{missing}{
  colback=missingviolet,
  colframe=violet!70,
  boxrule=2pt,
  title={🚧 \textbf{CONTENT MISSING}},
  fonttitle=\large\bfseries\color{black},
}

% Review needed: Orange with thick border
\newtcolorbox{review}{
  colback=revieworange,
  colframe=orange!70,
  boxrule=2pt,
  title={🔍 \textbf{NEEDS REVIEW}},
  fonttitle=\large\bfseries\color{black},
}

% Diagram needed: Blue with border
\newtcolorbox{diagram}{
  colback=diagramblue,
  colframe=blue!50,
  boxrule=2pt,
  title={🎨 \textbf{DIAGRAM NEEDED}},
  fonttitle=\large\bfseries\color{black},
}
```

### Your Turn Exercises (Changed from Yellow)
```latex
% Your Turn: Light blue exercise box
\newtcolorbox{yourturn}{
  colback=yourturncolor,
  colframe=blue!30,
  boxrule=1pt,
  title={\textbf{Your Turn}},
  fonttitle=\bfseries\color{black},
}
```

**CRITICAL**: Yellow reserved for inline code only. "Your Turn" boxes use light blue to avoid color conflict.

### Chapter Formatting
```latex
% Proper chapter numbering starting from 1
\setcounter{chapter}{0}
\titleformat{\chapter}[display]
  {\normalfont\huge\bfseries}
  {Chapter \thechapter}
  {20pt}
  {\Huge}

% Force chapters to start on new page with proper breaks
\let\oldchapter\chapter
\renewcommand{\chapter}{%
  \cleardoublepage
  \oldchapter
}
```

## 🚫 LaTeX Debugging Solutions - COMPREHENSIVE

### Template Compilation Errors

#### "Missing $ inserted" Root Causes
1. **Unescaped special characters in code blocks**
2. **Math delimiter parsing issues**  
3. **Unicode characters without proper encoding**

#### "Command not found" Errors
```latex
% Fix for table calculations
\newcommand{\real}[1]{#1}
```

#### "Environment already defined" Errors
- **Cause**: Duplicate environment definitions
- **Solution**: Use `\renewenvironment` or check for existing definitions

#### "Borderline not recognized" 
- **Cause**: Missing tcolorbox libraries
- **Solution**: `\usepackage[most]{tcolorbox}` and `\tcbuselibrary{skins,breakable}`

### Binary Search Debugging Method
When facing compilation errors:
1. **Extract problematic range** using line bisection
2. **Isolate to smallest failing section** (e.g., 94 lines from 6000)
3. **Apply systematic character escaping**
4. **Test in isolation before applying to full document**

## 📝 Working File Formats

### Request.json Template
```json
{
  "documents": [
    {
      "input": "document-name.md",
      "output": "document-name.pdf",
      "template": "p2kb-pasm-desilva",
      "variables": {
        "title": "Document Title", 
        "subtitle": "Document Subtitle",
        "version": "1.0",
        "date": "Month Year",
        "author": "Author Name",
        "footer": "Footer Text"
      }
    }
  ],
  "options": {
    "cleanup": true,
    "archive": true,
    "optimize": true
  }
}
```

**CRITICAL**: File name must be exactly `request.json` for PDF Forge compatibility.

### Markdown Structure Requirements
- **Headers**: Use `#`, `##`, `###` for proper hierarchy
- **Code blocks**: Triple backticks with `pasm2` language identifier
- **LaTeX environments**: Use `\begin{environment}` syntax for colored boxes
- **Math expressions**: Proper escaping of special characters

## 🎯 Quality Assurance Checklist

### Pre-Generation Verification
- [ ] All special characters properly escaped
- [ ] Template file deployed to PDF Forge
- [ ] Request.json syntax validated
- [ ] File paths correct and accessible
- [ ] Unicode characters properly encoded

### Post-Generation Verification
- [ ] All colored boxes render correctly
- [ ] Dashed borders appear (not solid)
- [ ] Typography uses Charter/Palatino font
- [ ] Chapter numbering correct (not 0.# format)
- [ ] Page breaks between chapters
- [ ] Footer appears on all pages
- [ ] Table of contents generated
- [ ] No LaTeX error artifacts

## 🔄 Workflow Integration

### File Preparation Sequence
1. **Generate content** with proper pedagogical structure
2. **Apply LaTeX escaping** systematically
3. **Create request.json** with exact specifications
4. **Deploy files** to PDF Forge environment
5. **Execute generation** and capture any errors
6. **Iterate** on problematic sections using binary search

### Error Resolution Protocol
1. **Capture exact error message** from PDF Forge output
2. **Identify error type** (missing $, undefined command, etc.)
3. **Apply systematic fixes** based on error category
4. **Test fixes** in isolation before full document
5. **Document solution** for future reference

## 🔄 Complete PDF Forge Workflow System

### 📁 Directory Structure & Organization

#### Master Templates Location
- **Path**: `/documentation/pdf-templates-master/`
- **Contents**: 4 P2KB-prefixed templates (source of truth)
  - `P2KB-pasm-desilva.latex` - deSilva pedagogical style
  - `P2KB-pasm2-manual.latex` - Standard P2 manual format
  - `P2KB-pasm2-minimal.latex` - Minimal/basic formatting
  - `P2KB-presentation.latex` - Presentation format

#### Document Working Areas
- **Outbound**: `/exports/pdf-generation/outbound/[document-folder]/`
  - Contains: `README.md`, `[document-name].md`, `request.json`
  - Optional: Template file (if modifications needed)
- **Inbound**: `/exports/pdf-generation/inbound/`
  - Contains: Accepted PDFs ready for publication
- **Public**: `/documentation/published-documents/` (to be created)
  - Contains: Final PDFs with metadata

### 🔧 Template Management Process

#### Template Modification Workflow
1. **Modify**: Edit template in `/documentation/pdf-templates-master/P2KB-[name].latex`
2. **Deploy**: Copy modified template to `/exports/pdf-generation/outbound/[document-folder]/`
3. **Signal**: Human sees template file appear in document folder
4. **Action**: Human manually moves template to PDF Forge, replacing existing
5. **Confirmation**: Template file disappears from document folder = deployed successfully
6. **Proceed**: Document processing continues with updated template

#### Status Tracking by File Presence
- **Template Present** = Waiting for human deployment
- **Template Absent** = Successfully deployed to PDF Forge

### 📋 Document Processing Workflow

#### File Management & Protection
- **Risk**: Files in outbound disappear when moved to PDF Forge
- **Solution**: Maintain internal working copies separate from outbound
- **Process**: Keep repairing/regenerating files until final version accepted
- **Round Trip**: When PDF accepted → outbound files become "latest masters"
- **Version Control**: Both source files AND accepted PDFs under git control

#### Processing Steps
1. **Preparation**: Generate content, apply LaTeX escaping, create request.json
2. **Deploy**: Copy files to `/exports/pdf-generation/outbound/[document-folder]/`
3. **Transfer**: Human manually moves files to PDF Forge
4. **Processing**: PDF Forge generates PDF
5. **Acceptance**: PDF appears in `/exports/pdf-generation/inbound/`
6. **Quality Assignment**: Human assigns quality stage and release date
7. **Publication**: Move to public folder with metadata
8. **Dashboard Update**: Update operational dashboard with new document status

### 🏷️ Document Quality Stages

#### Quality Stages with Purpose
1. **`technical-review`** - We need to validate technical content accuracy
2. **`early-draft`** - Enough content for public release, but still missing content/assets  
3. **`ready-for-company-evaluation`** - All assets complete, awaiting company decision on final format
4. **`company-evaluated`** - Company approved final format, ready for formal release scheduling
5. **`published-v1.0`** - Formal public release (company-assigned release date)
6. **`published-v1.x`** - Updated versions with corrections

#### Quality Assignment Prompt
When PDF appears in inbound:
```
📄 New PDF: [filename] 
🏷️ Quality stage (select with purpose):
   1. technical-review (We need to validate technical content accuracy)
   2. early-draft (Enough content for public release, but still missing content/assets)  
   3. ready-for-company-evaluation (All assets complete, awaiting company decision on final format)
   4. company-evaluated (Company approved final format, ready for formal release scheduling)
   5. published-v1.x (Formal public release with company or system-assigned release date)

📅 Release date: [auto: today] or [company-assigned date]?
```

#### Release Date Assignment
- **Draft stages**: Release date = date PDF accepted from inbound
- **Published stages**: Release date = company-assigned date OR system-assigned if none
- **Metadata**: All dates tracked for public reference

### 📖 Public Documentation Format

#### Document References
```markdown
[P2 Assembly Manual](link/to/document.pdf) (early-draft, 2025-08-21)
[CORDIC Guide](link/to/guide.pdf) (published-v1.2, 2025-07-15)
```

#### Metadata Tracking
- JSON file alongside each PDF with quality stage, date, version
- Dashboard/README updates include status indicators
- Version history maintained

### 📊 Operational Dashboard Updates

#### When to Update Dashboard
- **Trigger**: Each time a PDF is accepted and quality stage assigned
- **Frequency**: Immediate after publication step
- **Scope**: All public-facing documents (not technical-review stage)

#### Dashboard Update Information
```markdown
## Available Documents

### P2 Assembly Documentation
- [Discovering P2 Assembly - deSilva Style](path/to/pdf) (early-draft, 2025-08-21)
- [P2 CORDIC Operations Guide](path/to/pdf) (published-v1.1, 2025-07-15)
- [Smart Pins Reference](path/to/pdf) (ready-for-company-evaluation, 2025-08-20)

### Status Legend
- **early-draft**: Public release, content still being added
- **ready-for-company-evaluation**: Complete content, awaiting format approval
- **company-evaluated**: Approved format, pending release scheduling  
- **published-v1.x**: Official release with version number
```

#### Update Process
1. **Document Accepted**: PDF moved to public folder with metadata
2. **Dashboard Entry**: Add new document with quality stage and date
3. **Status Updates**: Modify existing entries when quality stage changes
4. **Link Validation**: Ensure all document links remain functional
5. **Git Commit**: Version control dashboard changes

#### Dashboard Locations to Update
- **Primary**: `engineering/README.md` (main status board)
- **Public README**: Repository main README.md (if applicable)
- **Project Documentation**: Any project-specific documentation indexes

### 🔐 Version Control Requirements

#### Critical Files Under Git Control
- All master templates (`/documentation/pdf-templates-master/`)
- All process documentation (including this guide)
- Final accepted source files (post-round-trip)
- Published PDFs with metadata
- Quality stage assignments and history

#### Backup Protocol
- ALWAYS backup before modifying large files
- Use timestamped backups: `file.md.backup.YYYYMMDD_HHMMSS`
- Commit process documents after major updates

**CRITICAL**: This workflow documentation is now under version control to prevent future data loss incidents.

## LaTeX Character Escaping Rules for P2 Assembly

**Added**: 2025-08-21 after binary search debugging success  
**Source**: Perplexity comprehensive escaping guide  
**Success**: Fixed "Missing $ inserted" errors in P2 Assembly manual

### Essential LaTeX Escaping for P2 Assembly Code

**CRITICAL**: Assembly code contains many LaTeX special characters that MUST be escaped:

#### Assembly Immediate Values - Escape `#` Characters
```
WRONG: mov value, ##1000000
RIGHT: mov value, \#\#1000000

WRONG: qsqrt value, #0  
RIGHT: qsqrt value, \#0
```

#### Dollar Signs in Text - Escape `$`
```
WRONG: full circle = $1_0000_0000
RIGHT: full circle = \$1\_0000\_0000
```

#### Underscores in Math/Text - Escape `_`
```
WRONG: $1_0000_0000
RIGHT: $1\_0000\_0000
```

#### Carets for Exponents - Use `\^{}`
```
WRONG: e\^2 = 7.389
RIGHT: e\^{}2 = 7.389
```

### Complete LaTeX Special Character Reference

| Character | Escape As | Usage |
|-----------|-----------|-------|
| `#` | `\#` | Assembly immediate values |
| `$` | `\$` | Hex values, math mode delimiter |
| `%` | `\%` | Comments (rare in our content) |
| `&` | `\&` | Alignment (rare in our content) |
| `~` | `\textasciitilde{}` | Approximation symbol |
| `_` | `\_` | Underscores in identifiers |
| `^` | `\^{}` | Exponents, XOR operations |
| `\` | `\textbackslash{}` | Backslashes |
| `{` | `\{` | Literal braces |
| `}` | `\}` | Literal braces |

### Binary Search Debugging Success Story

**Problem**: Lines 3095-3188 causing "Missing $ inserted" error  
**Solution Process**:
1. Isolated 94 problematic lines through binary search
2. Applied systematic character escaping:
   - `$1_0000_0000` → `\$1\_0000\_0000`
   - `##1000000` → `\#\#1000000`
   - `e\^2` → `e\^{}2`
3. **Result**: PDF generation successful!

### Integration into Content Generation

**MANDATORY STEP**: When generating P2 assembly content:
1. Write content normally first
2. Apply systematic character escaping before PDF generation
3. Test problematic sections in isolation
4. Use binary search if issues persist

**Tools Available**:
- Content bisection for error isolation
- Test file generation (`test-XXXX-YYYY.md`)
- Incremental testing approach

### Template Compatibility

This escaping works with:
- `p2kb-pasm-desilva.latex` template
- Pandoc → XeLaTeX → PDF pipeline
- tcolorbox colored environments
- Markdown code blocks (```pasm2)

**CRITICAL SUCCESS FACTOR**: Assembly code readability in PDF must match source fidelity while ensuring LaTeX compilation success.

## 🔧 Operational Procedures & Edge Cases

### Error Recovery Process (Iterative Debugging)
1. **Generate**: Create document with best-known escaping
2. **Test**: Human copies files to PDF Forge for processing
3. **Feedback**: Human pastes error messages back for analysis
4. **Fix**: Apply character escaping or template modifications
5. **Iterate**: Repeat 10-15 times until PDF generation succeeds
6. **Review**: Continue style iterations until ready for technical review
7. **Stake**: Mark final version as quality stage milestone

### Multi-Document Processing
- **Standard**: Single document per folder (most common)
- **Multiple Documents**: Occasionally multiple in same folder
- **Configuration**: Single `request.json` with multiple input/output pairs
- **Separation**: Different input filenames, different output PDF names
- **Use Cases**: Testing, style examples, template validation

### Template Evolution Process
- **No Formal Validation**: Templates improve through document iteration
- **Strength Building**: Each successful iteration strengthens template
- **Persistence**: Template stays with document through completion
- **Future Stability**: Modifications decrease as template matures
- **Version Control**: Template and document evolve together

### Construction Guides (Critical Documentation)
- **Purpose**: Complete manual creation guide for each document type
- **Contains**: Voice, style, fonts, source material mapping, formatting rules
- **Example**: deSilva P2 manual construction guide
- **Recovery Insurance**: Rebuild manual from scratch if content lost
- **Evolution**: Guide iterates alongside template and content
- **Components**: Template + Construction Guide = Complete Process Description

### Image & Asset Handling (To Be Learned)
- **Expected Structure**: Assets folder containing images
- **Markdown References**: Standard image linking syntax
- **PDF Integration**: PDF Forge assembles complete document
- **Status**: Documentation pending first implementation
- **Approach**: Document process when we encounter first image-heavy document

### Performance Characteristics
- **Limits**: Unknown - to be discovered through operation
- **File Sizes**: No known constraints yet
- **Processing Time**: Varies by document complexity
- **Memory Usage**: Not yet characterized
- **Documentation**: Track limits as we encounter them

### Error Message Catalog (Building Forward)
- **Historical Loss**: Previous error solutions lost in documentation incident
- **Current Foundation**: Character escaping table (comprehensive)
- **Future Tracking**: Document all new errors and solutions
- **Critical Reference**: LaTeX character escaping table (see above)
- **Growth**: Catalog builds with each debugging session

## 📂 Content Categories to Restore (Placeholders)

*These sections existed in the original guide and need content restoration from operational knowledge*

### 🔧 File Naming & Management Policies
**Status**: Found in backup, needs integration
- Template naming policy (CRITICAL: no version suffixes)
- Document naming policy (same rule + debug mode exceptions)
- Outbound directory cleanup procedures
- File type restrictions and guidelines

### ✅ Pre-Generation Validation & Checklists
**Status**: Found in backup, needs verification for current system
- Complete validation checklist before PDF Forge
- File inclusion/exclusion rules
- Markdown syntax restrictions
- Template reference validation

### 🔄 Content Conversion Guidelines
**Status**: Found in backup, needs accuracy verification
- LaTeX to Markdown conversion table
- Supported vs unsupported syntax
- Special block formatting rules
- Code block requirements

### 🚫 Common Mistakes & Avoidance
**Status**: Found in backup, needs current system review
- Files not to send to PDF Forge
- Markdown syntax to avoid
- Template reference errors
- Version suffix problems

### 📋 Available Templates Catalog
**Status**: Found in backup but outdated, needs refresh from master directory
- Complete template inventory
- Template purposes and features
- Selection guidelines
- Deployment status tracking

### 🎨 Visual Elements & Formatting Standards
**Status**: Partially recovered, needs completion
- Complete color specifications
- Typography requirements
- Layout standards
- Quality verification criteria

### 🔍 Advanced Troubleshooting
**Status**: Lost, needs rebuilding from operational experience
- Complex error scenarios beyond character escaping
- Multi-step debugging procedures
- Performance optimization techniques
- System limitation workarounds

### 🔗 Integration Procedures
**Status**: Needs development based on current workflow
- Connection with other pipeline tools
- Dependency management
- Version compatibility requirements
- Update procedures

**Action Items**:
- Review backup content for integration priority
- Verify accuracy against current texlive-full system
- Add content as operational knowledge accumulates
- Maintain placeholders until sections complete