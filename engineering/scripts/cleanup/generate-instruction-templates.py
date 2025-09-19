#!/usr/bin/env python3
"""
Generate markdown templates for all fair and poor instructions and directives.
Consolidates all available information from YAMLs into editable templates.
"""

import yaml
from pathlib import Path
from datetime import datetime
import re

# Paths
PASM2_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/pasm2")
DIRECTIVES_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/spin2/assembly-directives")
OUTPUT_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/document-production/manuals/pasm2-reference/instruction-templates/generated-batch")

# Create output directory
OUTPUT_PATH.mkdir(exist_ok=True)

print("Loading instruction analysis...")
data = yaml.safe_load(open('instruction_analysis.yaml'))
yaml_items = data['yaml_items']

# Find all items with scores below 60
items_to_template = []
for name, info in yaml_items.items():
    if info['score'] < 60:
        items_to_template.append((name, info))

# Sort by score (worst first) then by name
items_to_template.sort(key=lambda x: (x[1]['score'], x[0]))

print(f"Found {len(items_to_template)} instructions/directives needing templates (score < 60)")

def generate_template(name, info):
    """Generate a markdown template for an instruction or directive."""
    
    # Determine if this is a directive or instruction
    is_directive = info.get('is_directive', False)
    item_type = "Directive" if is_directive else "Instruction"
    
    # Load the actual YAML file for full details
    if is_directive:
        yaml_path = DIRECTIVES_PATH / f"{name.lower()}.yaml"
    else:
        yaml_path = PASM2_PATH / f"{name.lower()}.yaml"
    
    yaml_data = {}
    if yaml_path.exists():
        with open(yaml_path, 'r') as f:
            yaml_data = yaml.safe_load(f) or {}
    
    # Check if this is part of a grouped instruction
    grouped_with = ""
    if info.get('is_grouped_in_manual'):
        members = info.get('manual_group_members', [])
        if members and len(members) > 1:
            grouped_with = " / ".join(members)
    
    # Start building the template
    lines = []
    
    # Title
    if grouped_with:
        lines.append(f"# {grouped_with}")
    else:
        lines.append(f"# {name}")
    
    # Brief title/description
    brief = yaml_data.get('brief_description', '')
    if not brief and yaml_data.get('category'):
        # Extract brief from category if possible
        category = yaml_data['category']
        if ' - ' in category:
            brief = category.split(' - ', 1)[1]
    if brief:
        lines.append(f"**{brief}**")
    lines.append("")
    
    # Category/Group
    group = yaml_data.get('group', yaml_data.get('category', 'Unknown'))
    lines.append(f"*{group}*")
    lines.append("")
    
    # Syntax section
    lines.append("## Syntax")
    lines.append("```pasm2")
    syntax = yaml_data.get('syntax', f"{name} [parameters]")
    lines.append(syntax)
    
    # Add syntax variants if they exist
    syntax_variants = yaml_data.get('syntax_variants', [])
    for variant in syntax_variants:
        if variant != syntax:
            lines.append(variant)
    lines.append("```")
    lines.append("")
    
    # Encoding section (if available)
    encoding = yaml_data.get('encoding', '')
    if encoding:
        lines.append("## Encoding")
        lines.append(f"`{encoding}`")
        lines.append("")
    
    # Timing section (if available)
    timing = yaml_data.get('timing', {})
    if timing:
        cycles = timing.get('cycles', '?')
        timing_type = timing.get('type', '')
        lines.append("## Timing")
        if timing_type:
            lines.append(f"**{cycles} cycles** ({timing_type})")
        else:
            lines.append(f"**{cycles} cycles**")
        lines.append("")
    
    # Description section
    lines.append("## Description")
    description = yaml_data.get('description', yaml_data.get('detailed_description', ''))
    if description:
        # Clean up description formatting
        description = description.replace('\n', '\n\n')
        lines.append(description)
    else:
        lines.append(f"[TODO: Add detailed description of what {name} does]")
    lines.append("")
    
    # Parameters section (if available)
    parameters = yaml_data.get('parameters', [])
    if parameters:
        lines.append("## Parameters")
        for param in parameters:
            if isinstance(param, str):
                lines.append(f"- {param}")
            elif isinstance(param, dict):
                param_name = param.get('name', 'Parameter')
                param_desc = param.get('description', '')
                lines.append(f"- **{param_name}** - {param_desc}")
        lines.append("")
    elif not is_directive:
        # For instructions, add parameter placeholders
        lines.append("## Parameters")
        if 'D' in syntax and 'S' in syntax:
            lines.append("- **D** - Destination register")
            lines.append("- **S** - Source register or immediate value")
        elif 'D' in syntax:
            lines.append("- **D** - Destination register or immediate value")
        else:
            lines.append("[TODO: Document parameters]")
        lines.append("")
    
    # Flags affected section (if applicable)
    flags = yaml_data.get('flags_affected', yaml_data.get('flags', {}))
    if flags:
        lines.append("## Flags Affected")
        if isinstance(flags, dict):
            for flag, flag_info in flags.items():
                if isinstance(flag_info, dict):
                    formula = flag_info.get('formula', '')
                    lines.append(f"- **{flag}**: {formula}")
                else:
                    lines.append(f"- **{flag}**: {flag_info}")
        else:
            lines.append(f"{flags}")
        lines.append("")
    
    # Examples section
    lines.append("## Examples")
    examples = yaml_data.get('examples', [])
    if examples:
        lines.append("```pasm2")
        for example in examples[:3]:  # Show up to 3 examples
            if isinstance(example, str):
                lines.append(example)
            elif isinstance(example, dict):
                code = example.get('code', '')
                comment = example.get('comment', '')
                if code:
                    if comment:
                        lines.append(f"{code}  ' {comment}")
                    else:
                        lines.append(code)
        lines.append("```")
    else:
        lines.append("```pasm2")
        lines.append(f"' TODO: Add example usage of {name}")
        lines.append("```")
    lines.append("")
    
    # Related instructions (if any)
    related = yaml_data.get('related', yaml_data.get('see_also', []))
    if related:
        lines.append("## Related Instructions")
        if isinstance(related, list):
            for item in related:
                lines.append(f"- {item}")
        else:
            lines.append(f"- {related}")
        lines.append("")
    elif grouped_with:
        # Add group members as related
        lines.append("## Related Instructions")
        for member in info.get('manual_group_members', []):
            if member != name:
                lines.append(f"- {member}")
        lines.append("")
    
    # Notes section
    lines.append("## Notes")
    usage_notes = yaml_data.get('usage_notes', '')
    critical_req = yaml_data.get('critical_requirement', '')
    
    if usage_notes:
        lines.append(usage_notes)
    if critical_req:
        lines.append(f"**Critical:** {critical_req}")
    
    if not usage_notes and not critical_req:
        lines.append("[TODO: Add implementation notes, special cases, or tips]")
    
    lines.append("")
    
    # Metadata footer
    lines.append("---")
    lines.append(f"*Template generated: {datetime.now().strftime('%Y-%m-%d')}*")
    lines.append(f"*Score: {info['score']}/100*")
    if info.get('in_manual'):
        lines.append(f"*Documented in manual: Yes*")
    else:
        lines.append(f"*Documented in manual: No*")
    
    return "\n".join(lines)

# Generate templates
print(f"\nGenerating templates in {OUTPUT_PATH}/")
print("=" * 60)

generated_count = 0
directives_count = 0
instructions_count = 0

for name, info in items_to_template:
    template = generate_template(name, info)
    
    # Save template
    output_file = OUTPUT_PATH / f"{name}.md"
    with open(output_file, 'w') as f:
        f.write(template)
    
    generated_count += 1
    if info.get('is_directive'):
        directives_count += 1
        print(f"  Directive: {name} (score: {info['score']})")
    else:
        instructions_count += 1
        if generated_count <= 10:  # Show first 10
            print(f"  Instruction: {name} (score: {info['score']})")

if generated_count > 10:
    print(f"  ... and {generated_count - 10} more")

print("\n" + "=" * 60)
print(f"✅ Generated {generated_count} templates:")
print(f"   - {instructions_count} instruction templates")
print(f"   - {directives_count} directive templates")
print(f"\nTemplates saved to:")
print(f"  {OUTPUT_PATH}/")
print("\nThese templates are ready for manual editing to improve documentation!")