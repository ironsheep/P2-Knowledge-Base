# Critical Protocols Extracted from Context
*Generated 2025-08-26 from critical_* context keys*

## LaTeX Processing Critical Fixes

### Spacefactor Solution (SOLVED 2025-08-21)
**Problem:** \spacefactor command triggered in vertical mode  
**Location:** \renewcommand{\chaptermark} line using \  (backslash space)  
**Root cause:** \  sets spacefactor and can't be used in page header context  
**SOLUTION:** Replace \  with ~ (tilde) for non-breaking space:
- OLD: `\renewcommand{\chaptermark}[1]{\markboth{\chaptername\ \thechapter:\ #1}{}}`
- NEW: `\renewcommand{\chaptermark}[1]{\markboth{\chaptername~\thechapter:~#1}{}}`

### Pandoc Wrap Discovery (MAJOR)
**Issue:** LaTeX thispagestyle extra brace error caused by Pandoc's automatic line wrapping at ~80 chars breaking LaTeX commands mid-syntax  
**Solution:** `--wrap=preserve` in pandoc_args respects original single-line markdown titles  
**Impact:** Likely ROOT CAUSE for many LaTeX compilation errors in PDF pipeline

### Escape Script Bug  
**Issue:** latex_escape_processor.py NOT escaping special characters (like ^) inside custom template environments like \begin{sidetrack}...\end{sidetrack}  
**Status:** Script works on test cases but fails on production files  
**Need:** Proper regression test addition and script fix

## PDF Generation Workflow Rules

### Naming Protocol (CRITICAL)
**ALWAYS use production-ready names from start:**
- ✅ p2kb-pasm-desilva.latex (NOT -SEMANTIC, -TEST, -v2)
- ✅ P2-PASM-deSilva-Style.md (base document name)
- ✅ request.json (standard name)
**NEVER create temporary/test suffixes that require renaming later**

### Request JSON Format
**ALWAYS use documents array! Template name NO extension!**  
Check `/exports/pdf-generation/REQUEST-JSON-FORMAT-CRITICAL.md` EVERY TIME

### Last Deployed Workflow
**ALWAYS maintain last-deployed/ folder** with copies of ALL files sent to PDF Forge  
This is recovery mechanism and reference point - check here FIRST when resuming

### PDF Forge Versioning Protocol
When PDF Forge changes work correctly, ask user to COMMIT with descriptive message like 'MILESTONE: Enable pandoc_args and Lua filter support'  
Creates piton/stake to return to if future changes break

## Content Standards

### Formatting Rule (ABSOLUTE)
**Follow creation guides EXACTLY to the letter. No deviations.**  
If guide says dashed borders → implement dashed borders  
If guide says gray with dotted border → implement exactly that  
Visual formatting specifications are MANDATORY not suggestions

### PASM Instruction Formatting
**ABSOLUTE REQUIREMENT:** All PASM instruction names must be:
- ✅ **Bold** (**instruction**) - for maximum readability  
- ✅ **Backticked** (`instruction`) - for code highlighting
- ❌ **NEVER italic** - reduces readability
- ❌ **NEVER plain text** - instructions must stand out
Examples: **`drvh`**, **`waitx`**, **`jmp`**, **`mov`**, **`wrpin`**, **`rdpin`**

### Product Numbering Convention
**MANDATORY:** Always use # prefix for product numbers  
P2 Edge Mini Breakout = #64019, P2 Edge Standard Breakout = #64029, etc.

## System Environment Rules

### No Local Pandoc
**NEVER use pandoc locally** even though it exists at `/Users/stephen/anaconda3/bin/pandoc`  
ALL PDF generation happens on PDF Forge only - local pandoc OFF LIMITS

### Template Compatibility Requirements  
**MANDATORY:** Smart Pins template ALWAYS needs Pandoc compatibility definitions:  
\real{} command + \tightlist + \passthrough + \subtitle + etc.  
Template degradation causes recurring \real{} errors

## Hardware Documentation Rules

### P2 vs Edge Module Distinction
**CRITICAL:** Edge Module pinout ≠ P2 chip pinout  
Edge Module = breakout board with 80-pin edge connector  
P2 chip = 100-pin TQFP  
Must keep separate in knowledge base

### Power Specifications
**CRITICAL:** P2 chip power ≠ Edge module power  
P2 chip = internal VDD/VIO requirements  
Edge module = system-level 5-16VDC input + onboard regulators

### RAM Module Board Conflict
**CRITICAL:** P2 Edge 32MB uses P40-P57 for RAM, but Edge breadboards/breakout boards likely expect those pins for external connections  
Need compatibility matrix knowledge