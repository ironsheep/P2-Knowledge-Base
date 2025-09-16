# Pattern Analysis Files

## What These Files Are

These are **statistical analysis results** from examining 730 P2 source code files. They are NOT implementation guides or code templates.

## File Contents

Each `*_analysis.yaml` file contains:
- **Prevalence statistics**: How many files use this pattern (e.g., "38.5% of files")
- **Selection criteria**: When to use or avoid the pattern
- **Resource profiles**: Memory, timing, and complexity analysis
- **Real examples**: Actual applications found in the codebase
- **Composition rules**: What patterns work together
- **Anti-patterns**: Common mistakes to avoid

## For Implementation Code

If you're looking for actual implementation examples, see:
- `/language/spin2/patterns/` - Spin2 implementation patterns
- `/language/pasm2/patterns/` - PASM2 implementation patterns

## File Naming Convention

All files end with `_analysis.yaml` to distinguish them from implementation patterns.

Example:
- `cog_management_analysis.yaml` - Statistical analysis of cog management patterns
- NOT `cog_management.yaml` - That would imply implementation code

## Usage

These analysis files are valuable for:
- Understanding pattern prevalence in real P2 code
- Making architectural decisions
- Identifying common combinations
- Avoiding known anti-patterns

They are NOT meant for:
- Direct code generation
- Copy-paste implementation
- Quick reference snippets