# Operational Lessons Extracted from Context
*Generated 2025-08-26 from lesson_* context keys*

## Session Management
### lesson_optimal_session_length
Based on experience: ~3-4 hours optimal before clearing. Signals to clear: 1) Forgetting recent details, 2) User mentions 'fuzzy', 3) 4+ hours elapsed, 4) Major task transitions, 5) After 15-20 complex file operations. Clear BEFORE degradation, not after.

### lesson_session_length_critical
HARD STOP at 3-4 hours. This session went 5+ hours. Clear degradation signs: 1) Same bug (2^9) handled 6 different ways, 2) Damaged recoverable master files, 3) Lost track of file states, 4) Made same mistakes repeatedly. When you see yourself fixing the same issue more than twice, STOP IMMEDIATELY. The cost of degradation is higher than restarting fresh.

## Todo MCP Patterns
### lesson_auto_resume_failure
After clear + context_resume showing in-progress task, must AUTO-START it, not ask. User correctly observed we failed to auto-resume task which was already in_progress with elapsed time.

### lesson_batch_create_preference
For planned task generation (like sprint planning), use mcp__todo-mcp__todo_batch_create instead of individual creates. More efficient, atomic, cleaner, and more professional. Individual creates are better for ad-hoc or exploratory task creation.

### lesson_plan_vs_task_guidance
Plan feeds ADVICE forward, not requirements. Task generation has freedom to accept/reject guidance. We suggest optimizations and perspectives, not mandates. Tags, ordering suggestions are opportunities, not rules.

## Context Management
### lesson_context_cleanup
186 keys→nuclear cleanup. Pattern: dump with context, preserve valuable to .todo-mcp/preserved-context/, clear all, rebuild minimal. Value size matters, not key count.

## Development Anti-Patterns
### lesson_suffix_addiction
SELF-AWARENESS: I have a compulsive habit of adding suffixes (-enhanced, -backup, -v2, -FINAL) instead of just replacing files cleanly. This creates cognitive overload and confusion. Need to resist the urge to create 'museum of variants'.

## P2 Knowledge Base Specific
### lesson_code_examples_inaccessible
267 Spin2 code examples + 283 other examples = 550+ total examples EXIST but are NOT individually accessible. They're buried in audit files. Critical gap: Cannot retrieve specific examples for user requests. Needs targeted extraction into catalog format.

### lesson_desilva_pdf_gap
DeSilva P1 Assembly Tutorial PDF exists at sources/originals/ but was NEVER extracted - only style guide created. This is a major gap for AD-003 task. Shows importance of verifying actual extraction vs assumed extraction.

### lesson_ingested_sources_catalog
Created INGESTED-SOURCES-CATALOG.md as master inventory of all sources with metadata: file sizes, dates, completion status, source attribution, relationships. Added to README operations dashboard. Shows 10 primary sources, 12 completed extractions, 5 planned extractions.

### lesson_pdf_extraction_capability
We have pdftotext available via Bash! Can extract DeSilva P1 Assembly Tutorial PDF directly. This enables AD-003 task to proceed with actual content extraction → voice analysis (Opus) → P2 guide creation.

## PDF Generation & Templates
### lesson_creation_guides_absolute
CRITICAL LEARNING: Creation guides are BIBLE. Never compromise requirements like dashed borders. User had to remind me multiple times. This is unacceptable. Creation guide requirements are non-negotiable.

### lesson_escape_workflow
NEVER escape master files in workspace. Masters stay clean and readable. Only escape during deployment when copying to outbound. Workflow: Edit master → Remove bold markers → Escape while copying to outbound.

### lesson_pandoc_environment_mismatch
Local Pandoc (/Users/stephen/anaconda3/bin/pandoc) is in WRONG CONTEXT - different version, missing packages, missing fonts, different paths. Testing locally would give FALSE results. PDF Forge has the complete, correct environment. Never test locally - results would be misleading!

### lesson_template_degradation_20250823
Template degraded from 1302 to 354 lines during work session. Lost Eisvogel base features. Lesson: Need checkpoint strategy - save 'known-good' versions before modifications. Template versioning process would prevent this. Recovery required merging stripped version with morning's full version. Always backup before major template surgery.

## Development Methodology
### lesson_class_problem_principle
CLASS PROBLEM PRINCIPLE: Every bug is a symptom of a class of bugs. When fixing, always ask "What's the whole class?" and fix ALL similar cases at once. Example: Don't just fix \item, fix ALL LaTeX list/sectioning/formatting commands. This prevents future breaks and reduces maintenance cycles. Now documented in TOOL-REGRESSION-PATTERN.md