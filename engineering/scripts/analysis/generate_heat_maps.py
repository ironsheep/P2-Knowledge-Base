#!/usr/bin/env python3
"""
Generate heat map visualizations for PASM2 documentation quality.
Separate heat maps for instructions and directives.
"""

import yaml
from pathlib import Path
from collections import defaultdict
import math

# Run the analysis first
import subprocess
print("Running analysis...")
result = subprocess.run(['python3', 'analyze_instruction_coverage.py'], capture_output=True, text=True)
print(result.stdout[:500])  # Print first 500 chars of output

# Load analysis data
with open('instruction_analysis.yaml', 'r') as f:
    data = yaml.safe_load(f)

yaml_items = data['yaml_items']
manual_items = data['manual_items']
statistics = data['statistics']

# Separate instructions from directives
instructions = {}
directives = {}

for item, info in yaml_items.items():
    if info.get('is_directive') or info.get('location') == 'assembly-directives':
        directives[item] = info
    else:
        instructions[item] = info

# Known directives that should exist
EXPECTED_DIRECTIVES = {
    'ALIGNL', 'ALIGNW', 'BYTE', 'WORD', 'LONG', 'FILE',
    'ORG', 'ORGH', 'ORGF', 'FIT', 'RES', 'DITTO'
}

# Color mapping based on score
def get_color_code(score):
    """Return color emoji based on documentation score (0-100)"""
    if score >= 80:
        return "🟩"  # Green - Excellent
    elif score >= 60:
        return "🟦"  # Blue - Good  
    elif score >= 40:
        return "🟨"  # Yellow - Fair
    elif score >= 20:
        return "🟧"  # Orange - Poor
    else:
        return "🟥"  # Red - Minimal/Missing

def get_color_name(score):
    """Return color name based on documentation score"""
    if score >= 80:
        return "excellent"
    elif score >= 60:
        return "good"  
    elif score >= 40:
        return "fair"
    elif score >= 20:
        return "poor"
    else:
        return "minimal"

def create_heat_map_grid(items, title, cols=12):
    """Create a heat map grid for a set of items."""
    output = []
    output.append(f"### {title}")
    output.append("")
    
    # Sort items by score (worst to best)
    item_scores = []
    for name, info in items.items():
        score = info.get('score', 0)
        item_scores.append((name, score))
    
    # Add missing items with score 0
    if 'directive' in title.lower():
        for directive in EXPECTED_DIRECTIVES:
            if directive not in items:
                item_scores.append((directive, 0))
    
    item_scores.sort(key=lambda x: x[1])
    
    output.append(f"**Total: {len(item_scores)} items**")
    output.append("")
    
    # Create grid
    rows = math.ceil(len(item_scores) / cols)
    
    output.append("| " + " | ".join([f"Col {i+1}" for i in range(cols)]) + " |")
    output.append("|" + "|\".join([\"-------\"] * cols) + \"|")
    
    for row in range(rows):
        row_data = []
        for col in range(cols):
            idx = row * cols + col
            if idx < len(item_scores):
                name, score = item_scores[idx]
                color = get_color_code(score)
                # Use full name, no truncation
                row_data.append(f"{color} {name}")
            else:
                row_data.append("")
        output.append("| " + " | ".join(row_data) + " |")
    
    # Score distribution for this category
    distribution = {
        'Excellent (80-100)': 0,
        'Good (60-79)': 0,
        'Fair (40-59)': 0,
        'Poor (20-39)': 0,
        'Minimal (0-19)': 0
    }
    
    for _, score in item_scores:
        if score >= 80:
            distribution['Excellent (80-100)'] += 1
        elif score >= 60:
            distribution['Good (60-79)'] += 1
        elif score >= 40:
            distribution['Fair (40-59)'] += 1
        elif score >= 20:
            distribution['Poor (20-39)'] += 1
        else:
            distribution['Minimal (0-19)'] += 1
    
    output.append("")
    output.append(f"**Distribution:**")
    for category, count in distribution.items():
        if count > 0:
            output.append(f"- {category}: {count}")
    
    return output, distribution

# Create markdown output
output = []
output.append("# PASM2 Documentation Quality Heat Maps")
output.append("")
output.append(f"**Analysis Date**: 2025-09-19")
output.append(f"**Separate tracking for instructions and directives**")
output.append("")

output.append("## Key Features")
output.append("")
output.append("- ✅ **Separate heat maps** for instructions vs directives")
output.append("- ✅ **Complete directive coverage** - all assembly directives included")
output.append("- ✅ **Proper categorization** - directives not mixed with instructions")
output.append("- ✅ **Accurate scoring** - different criteria for different categories")
output.append("")

output.append("## Legend")
output.append("")
output.append("| Score | Color | Quality | Description |")
output.append("|-------|-------|---------|-------------|")
output.append("| 80-100 | 🟩 | Excellent | Full documentation with examples, all fields present |")
output.append("| 60-79 | 🟦 | Good | Good documentation, may lack examples or some details |")
output.append("| 40-59 | 🟨 | Fair | Basic documentation, missing important details |")
output.append("| 20-39 | 🟧 | Poor | Minimal documentation, many gaps |")
output.append("| 0-19 | 🟥 | Minimal | Little to no documentation |")
output.append("")

# Instructions heat map
output.append("## 1. PASM2 CPU Instructions Heat Map")
output.append("")
output.append("CPU instructions that execute on the P2 processor.")
output.append("")
instr_grid, instr_dist = create_heat_map_grid(instructions, "CPU Instructions (Worst to Best)")
output.extend(instr_grid)

# Directives heat map
output.append("")
output.append("## 2. Assembly Directives Heat Map")
output.append("")
output.append("Assembler directives for data declaration and memory organization.")
output.append("")
dir_grid, dir_dist = create_heat_map_grid(directives, "Assembly Directives (Worst to Best)")
output.extend(dir_grid)

# Group analysis
output.append("")
output.append("## 3. Instruction Groups Analysis")
output.append("")

# Group instructions by category
instruction_groups = defaultdict(list)
for name, info in instructions.items():
    group = info.get('group', 'Unknown')
    instruction_groups[group].append((name, info['score']))

# Calculate average scores by group
group_scores = {}
for group, items in instruction_groups.items():
    if items:
        scores = [score for _, score in items]
        avg_score = sum(scores) / len(scores)
        group_scores[group] = {
            'avg_score': avg_score,
            'count': len(items),
            'items': items
        }

# Sort groups by average score
sorted_groups = sorted(group_scores.items(), key=lambda x: x[1]['avg_score'])

output.append("| Group | Avg Score | Quality | Count | Sample Instructions |")
output.append("|-------|-----------|---------|-------|---------------------|")

for group, info in sorted_groups[:20]:  # Top 20 groups
    color = get_color_code(info['avg_score'])
    quality = get_color_name(info['avg_score'])
    sample = ", ".join([name for name, _ in info['items'][:3]])
    if len(info['items']) > 3:
        sample += "..."
    group_display = group[:30] if len(group) > 30 else group
    output.append(f"| {group_display} | {color} {info['avg_score']:.0f} | {quality} | {info['count']} | {sample} |")

# Summary statistics
output.append("")
output.append("## 4. Overall Statistics")
output.append("")

total_instructions = len(instructions)
total_directives = len(directives) + len(EXPECTED_DIRECTIVES - set(directives.keys()))

output.append(f"### CPU Instructions")
output.append(f"- Total: {total_instructions}")
output.append(f"- Excellent: {sum(1 for _, i in instructions.items() if i['score'] >= 80)}")
output.append(f"- Good: {sum(1 for _, i in instructions.items() if 60 <= i['score'] < 80)}")
output.append(f"- Fair: {sum(1 for _, i in instructions.items() if 40 <= i['score'] < 60)}")
output.append(f"- Poor: {sum(1 for _, i in instructions.items() if 20 <= i['score'] < 40)}")
output.append(f"- Minimal: {sum(1 for _, i in instructions.items() if i['score'] < 20)}")

output.append("")
output.append(f"### Assembly Directives")
output.append(f"- Total: {total_directives}")
output.append(f"- With documentation: {len(directives)}")
output.append(f"- Missing: {len(EXPECTED_DIRECTIVES - set(directives.keys()))}")
if EXPECTED_DIRECTIVES - set(directives.keys()):
    output.append(f"  - Missing directives: {', '.join(sorted(EXPECTED_DIRECTIVES - set(directives.keys())))}")

# Recommendations
output.append("")
output.append("## 5. Recommendations")
output.append("")

# Find worst documented items
worst_instructions = [(n, i['score']) for n, i in instructions.items() if i['score'] < 40]
worst_directives = [(n, d.get('score', 0)) for n, d in directives.items() if d.get('score', 0) < 40]

if worst_instructions:
    output.append(f"### Priority 1: Fix {len(worst_instructions)} Poor Instructions")
    for name, score in sorted(worst_instructions, key=lambda x: x[1])[:10]:
        output.append(f"- {name} (score: {score})")
    if len(worst_instructions) > 10:
        output.append(f"- ... and {len(worst_instructions) - 10} more")

if worst_directives or (EXPECTED_DIRECTIVES - set(directives.keys())):
    output.append("")
    output.append(f"### Priority 2: Complete Directive Documentation")
    missing = EXPECTED_DIRECTIVES - set(directives.keys())
    if missing:
        output.append(f"- Create YAMLs for: {', '.join(sorted(missing))}")
    for name, score in sorted(worst_directives, key=lambda x: x[1])[:5]:
        output.append(f"- Improve {name} (score: {score})")

output.append("")
output.append("---")
output.append("*Generated by PASM2 documentation analysis tool*")
output.append("*Separate tracking for instructions and directives*")

# Save the heat map document
output_text = "\n".join(output)
with open('PASM2-Documentation-Heat-Map.md', 'w') as f:
    f.write(output_text)

print("\n" + "="*60)
print("Heat map generated: PASM2-Documentation-Heat-Map.md")
print("="*60)
print(f"\nCPU Instructions: {total_instructions}")
print(f"  Well documented (60+): {sum(1 for _, i in instructions.items() if i['score'] >= 60)}")
print(f"  Need work (<60): {sum(1 for _, i in instructions.items() if i['score'] < 60)}")
print(f"\nAssembly Directives: {total_directives}")
print(f"  Documented: {len(directives)}")
print(f"  Missing: {len(EXPECTED_DIRECTIVES - set(directives.keys()))}")