#!/usr/bin/env python3
"""
Audit field name consistency across YAML files.
Separate analysis for instructions vs directives.
"""

import yaml
from pathlib import Path
from collections import defaultdict

# Paths
PASM2_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/pasm2")
DIRECTIVES_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/spin2/assembly-directives")

def analyze_fields(path, category_name):
    """Analyze field usage in YAML files."""
    field_usage = defaultdict(int)
    field_examples = defaultdict(list)
    total_files = 0
    
    yaml_files = list(path.glob("*.yaml"))
    
    for yaml_file in yaml_files:
        if yaml_file.stem in ['concepts', 'patterns', 'idioms']:
            continue
            
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            if data and isinstance(data, dict):
                total_files += 1
                for field in data.keys():
                    field_usage[field] += 1
                    if len(field_examples[field]) < 3:
                        field_examples[field].append(yaml_file.stem)
                        
        except Exception as e:
            print(f"Error processing {yaml_file}: {e}")
    
    print(f"\n{'='*60}")
    print(f"{category_name} Field Analysis")
    print(f"{'='*60}")
    print(f"Total files analyzed: {total_files}")
    print(f"\nField usage (sorted by frequency):")
    
    # Sort by usage frequency
    sorted_fields = sorted(field_usage.items(), key=lambda x: x[1], reverse=True)
    
    for field, count in sorted_fields:
        percentage = (count / total_files * 100) if total_files > 0 else 0
        examples = ", ".join(field_examples[field][:3])
        print(f"  {field:30} {count:4} ({percentage:5.1f}%) - e.g., {examples}")
    
    # Identify inconsistencies
    print(f"\n{category_name} Potential Inconsistencies:")
    
    # Look for similar field names
    field_names = list(field_usage.keys())
    for i, field1 in enumerate(field_names):
        for field2 in field_names[i+1:]:
            # Check for similar names (e.g., description vs detailed_description)
            if (field1 in field2 or field2 in field1) and field1 != field2:
                print(f"  - '{field1}' ({field_usage[field1]}) vs '{field2}' ({field_usage[field2]})")
    
    return field_usage, total_files

# Analyze PASM2 instructions
print("Analyzing PASM2 instruction YAMLs...")
instr_fields, instr_count = analyze_fields(PASM2_PATH, "PASM2 Instructions")

# Analyze assembly directives  
print("\nAnalyzing assembly directive YAMLs...")
dir_fields, dir_count = analyze_fields(DIRECTIVES_PATH, "Assembly Directives")

# Compare field sets
print(f"\n{'='*60}")
print("Field Standardization Recommendations")
print(f"{'='*60}")

# Core fields that should be in all instructions
core_instruction_fields = {
    'instruction', 'syntax', 'encoding', 'timing', 'group', 'description'
}

# Core fields that should be in all directives
core_directive_fields = {
    'directive', 'syntax', 'description', 'group'
}

print("\nSuggested Core Fields for Instructions:")
for field in core_instruction_fields:
    count = instr_fields.get(field, 0)
    percentage = (count / instr_count * 100) if instr_count > 0 else 0
    status = "✓" if percentage > 90 else "⚠" if percentage > 50 else "✗"
    print(f"  {status} {field:20} - {count}/{instr_count} ({percentage:.1f}%)")

print("\nSuggested Core Fields for Directives:")
for field in core_directive_fields:
    count = dir_fields.get(field, 0)
    percentage = (count / dir_count * 100) if dir_count > 0 else 0
    status = "✓" if percentage > 90 else "⚠" if percentage > 50 else "✗"
    print(f"  {status} {field:20} - {count}/{dir_count} ({percentage:.1f}%)")

# Identify fields that should be renamed
print("\nRecommended Field Renames:")

rename_suggestions = {
    # Instructions
    'detailed_description': 'description',
    'brief_description': 'description',
    'long_description': 'description',
    'flags': 'flags_affected',
    
    # Both
    'category': 'group',
}

for old_name, new_name in rename_suggestions.items():
    if old_name in instr_fields:
        print(f"  Instructions: '{old_name}' -> '{new_name}' ({instr_fields[old_name]} files)")
    if old_name in dir_fields:
        print(f"  Directives: '{old_name}' -> '{new_name}' ({dir_fields[old_name]} files)")

print("\nUnique fields per category:")
print(f"  Instruction-only fields: {set(instr_fields.keys()) - set(dir_fields.keys())}")
print(f"  Directive-only fields: {set(dir_fields.keys()) - set(instr_fields.keys())}")