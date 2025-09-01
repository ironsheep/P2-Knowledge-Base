# Internal References to Fix

*Generated during PHASE 5 of repository reorganization*

## Summary
- **Total Files with References**: 50+
- **Total Internal References Found**: 266
- **Pattern**: Markdown links with relative paths starting with `../` or `./`

## Files Requiring Reference Updates

### High Reference Count (10+ references)
1. `deliverables/reference/architecture-overview.md` - 15 references
2. `deliverables/reference/pasm2-essentials.md` - 12 references
3. `deliverables/developer-docs/START-HERE.md` - 18 references
4. `deliverables/learning-paths/P2-Beginner-Path.md` - 14 references
5. `deliverables/learning-paths/P2-Expert-Path.md` - 11 references

### Medium Reference Count (5-9 references)
6. `deliverables/ai-reference/AI-P2-Reference-V2.md` - 8 references
7. `deliverables/ai-reference/AI-P2-Assembly-Guide.md` - 7 references
8. `engineering/knowledge-base/debt.md` - 6 references
9. `engineering/ingestion/debt.md` - 5 references
10. `engineering/document-production/debt.md` - 5 references

### Documentation with Cross-References
11. `documentation/manuals/pasm2-manual/PASM2-Complete-Manual.md` - 9 references
12. `documentation/manuals/smart-pins-manual/Smart-Pins-Tutorial.md` - 8 references
13. `documentation/work-mode-guides/smart-pins-visual-mode.md` - 6 references
14. `documentation/work-mode-guides/desilva-manual-mode.md` - 5 references

### Engineering Documentation
15. `engineering/tools/README.md` - 8 references
16. `engineering/pdf-forge/scripts/README.md` - 4 references
17. `engineering/operations/migration/vision-documents.md` - 7 references
18. `engineering/operations/migration/mapping.csv` - N/A (CSV format)

### Project Guidance
19. `project-guidance/methodology/technical-climbing-methodology.md` - 4 references
20. `project-guidance/methodology/source-quality-matrix-3d.md` - 3 references
21. `project-guidance/PROJECT-MASTER.md` - 12 references

### Planning Documents  
22. `planning/strategic/P2-Claude-Enablement-Strategy.md` - 9 references
23. `planning/strategic/ai-privacy-guide-implementation-plan.md` - 5 references
24. `planning/strategic/smart-pins-visual-strategy.md` - 4 references

### Claude Guidance
25. `claude-guidance/CLAUDE.md` - 11 references
26. `claude-guidance/ai-operational-guide.md` - 6 references
27. `claude-guidance/prompt-engineering-guide.md` - 4 references

### Sources and Extractions
28. `sources/extractions/smart-pins-complete-extraction-audit.md` - 8 references
29. `sources/extractions/pasm2-manual-complete-extraction-audit.md` - 7 references
30. `sources/INGESTED-SOURCES-CATALOG.md` - 15 references

### Exports
31. `exports/pdf-generation/workspace/manual-templates/README.md` - 5 references
32. `exports/pdf-generation/outbound/README.md` - 4 references

### Documentation Folders
33. `documentation/pdf-forge-system/PDF-FORGE-SYSTEM-OVERVIEW.md` - 8 references
34. `documentation/collaboration-guides/human-ai-collaboration-guide.md` - 3 references
35. `documentation/best-practices/naming-conventions.md` - 2 references

## Common Reference Patterns to Fix

### Old Path → New Path Examples
- `../technical-debt/` → `../engineering/knowledge-base/debt.md`
- `../analysis-debt/` → `../engineering/ingestion/debt.md`
- `../tools/` → `../engineering/tools/`
- `../pdf-forge-scripts/` → `../engineering/pdf-forge/scripts/`
- `./ai-reference/` → `../deliverables/ai-reference/`
- `./learning-paths/` → `../deliverables/learning-paths/`

### Reference Types
1. **Relative Path Links**: `[text](../path/to/file.md)`
2. **Image References**: `![alt](../assets/image.png)`
3. **Code Includes**: References in code blocks pointing to files
4. **Documentation Cross-refs**: Links between related documents

## Repair Strategy
1. Use mapping.csv to create systematic old→new path translations
2. Apply MultiEdit tool for batch reference updates per file
3. Verify all references resolve correctly after updates
4. Update any hardcoded paths in scripts/tools

## Priority Order
1. **Critical**: deliverables/ folder (public-facing)
2. **High**: engineering/tools/ and project-guidance/
3. **Medium**: documentation/ and sources/
4. **Low**: archives/ and uncertain/

---
*Next step: Generate old-to-new-map.csv for automated reference repair*