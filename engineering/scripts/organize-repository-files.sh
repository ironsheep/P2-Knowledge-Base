#!/bin/bash
# Organize repository files into proper directories

echo "=== REPOSITORY ORGANIZATION PLAN ==="
echo ""
echo "Files that SHOULD stay at top level (already versioned):"
echo "  • README.md"
echo "  • CHANGELOG.md" 
echo "  • CONTRIBUTING.md"
echo "  • AI-PROMPT-PATTERNS.md"
echo "  • CLAUDE-QUICKSTART.md"
echo "  • USING-WITH-AI.md"
echo ""

echo "Files to move to engineering/scripts/analysis/:"
echo "  • analyze_instruction_coverage.py"
echo "  • generate_heat_maps.py"
echo "  • yaml-quality-assessment.py"
echo "  • find-grouped-instructions.py"
echo "  • audit-yaml-files.py"
echo "  • audit-field-consistency.py"

echo ""
echo "Files to move to engineering/scripts/extraction/:"
echo "  • extract-full-manual-documentation.py"
echo "  • extract-manual-pages-31-147.py"
echo "  • extract-missed-grouped-instructions.py"
echo "  • apply-extracted-documentation.py"
echo "  • apply-manual-updates.py"
echo "  • update-yaml-from-manual.py"

echo ""
echo "Files to move to engineering/scripts/cleanup/:"
echo "  • cleanup-yaml-inconsistencies.py"
echo "  • fix-grouped-instructions.py"
echo "  • update-grouped-instructions.py"
echo "  • implement-group-documentation.py"
echo "  • fix-and-andn-extraction.py"
echo "  • clean-push-pop-descriptions.py"
echo "  • generate-instruction-templates.py"

echo ""
echo "Files to move to engineering/reports/:"
echo "  • instruction_analysis.yaml"
echo "  • PASM2-Documentation-Heat-Map.md"
echo "  • extraction-improvement-summary.md"
echo "  • yaml-quality-improvement-plan.md"
echo "  • YAML-UPDATE-REPORT.md"
echo "  • FINAL-UPDATE-SUMMARY.md"
echo "  • grouped-instructions-comprehensive.md"

echo ""
echo "File to DELETE (in .gitignore, not needed):"
echo "  • CLAUDE.md (already in .gitignore)"

echo ""
echo "Creating directory structure..."

# Create directories
mkdir -p engineering/scripts/analysis
mkdir -p engineering/scripts/extraction  
mkdir -p engineering/scripts/cleanup
mkdir -p engineering/reports

echo "✓ Directories created"
echo ""
echo "Moving files..."

# Move analysis scripts
mv analyze_instruction_coverage.py engineering/scripts/analysis/ 2>/dev/null
mv generate_heat_maps.py engineering/scripts/analysis/ 2>/dev/null
mv yaml-quality-assessment.py engineering/scripts/analysis/ 2>/dev/null
mv find-grouped-instructions.py engineering/scripts/analysis/ 2>/dev/null
mv audit-yaml-files.py engineering/scripts/analysis/ 2>/dev/null
mv audit-field-consistency.py engineering/scripts/analysis/ 2>/dev/null

# Move extraction scripts
mv extract-full-manual-documentation.py engineering/scripts/extraction/ 2>/dev/null
mv extract-manual-pages-31-147.py engineering/scripts/extraction/ 2>/dev/null
mv extract-missed-grouped-instructions.py engineering/scripts/extraction/ 2>/dev/null
mv apply-extracted-documentation.py engineering/scripts/extraction/ 2>/dev/null
mv apply-manual-updates.py engineering/scripts/extraction/ 2>/dev/null
mv update-yaml-from-manual.py engineering/scripts/extraction/ 2>/dev/null

# Move cleanup scripts
mv cleanup-yaml-inconsistencies.py engineering/scripts/cleanup/ 2>/dev/null
mv fix-grouped-instructions.py engineering/scripts/cleanup/ 2>/dev/null
mv update-grouped-instructions.py engineering/scripts/cleanup/ 2>/dev/null
mv implement-group-documentation.py engineering/scripts/cleanup/ 2>/dev/null
mv fix-and-andn-extraction.py engineering/scripts/cleanup/ 2>/dev/null
mv clean-push-pop-descriptions.py engineering/scripts/cleanup/ 2>/dev/null
mv generate-instruction-templates.py engineering/scripts/cleanup/ 2>/dev/null

# Move reports
mv instruction_analysis.yaml engineering/reports/ 2>/dev/null
mv PASM2-Documentation-Heat-Map.md engineering/reports/ 2>/dev/null
mv extraction-improvement-summary.md engineering/reports/ 2>/dev/null
mv yaml-quality-improvement-plan.md engineering/reports/ 2>/dev/null
mv YAML-UPDATE-REPORT.md engineering/reports/ 2>/dev/null
mv FINAL-UPDATE-SUMMARY.md engineering/reports/ 2>/dev/null
mv grouped-instructions-comprehensive.md engineering/reports/ 2>/dev/null

echo "✓ Files moved"
echo ""
echo "Repository is now organized!"