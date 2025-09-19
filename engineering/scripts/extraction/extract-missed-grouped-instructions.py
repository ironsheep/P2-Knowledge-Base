#!/usr/bin/env python3
"""
Extract missed grouped instructions like AND/ANDN that have special formatting.
"""

import yaml
from pathlib import Path
import re

# Paths
MANUAL_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/pasm2-manual/pasm2-manual-narrative.txt")
PASM2_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/pasm2")
OUTPUT_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/extracted-documentation/missed-grouped")

OUTPUT_PATH.mkdir(exist_ok=True, parents=True)

print("Loading PASM2 manual...")
with open(MANUAL_PATH, 'r', encoding='utf-8') as f:
    manual_lines = f.readlines()

# Known grouped instructions that were missed
missed_groups = [
    ('AND / ANDN', 2605, 2650),
    # Add more as we find them
]

def extract_grouped_section(name, start_line, end_line):
    """Extract content for a grouped instruction section."""
    lines = manual_lines[start_line:end_line]
    
    # Parse instruction names from header
    header = name.replace(' ', '')
    instructions = [inst.strip() for inst in header.split('/')]
    
    # Find key content
    data = {
        'instructions': instructions,
        'brief_description': '',
        'category': '',
        'syntax': [],
        'description': '',
        'parameters': [],
        'encoding': [],
        'flags': {},
        'explanation': ''
    }
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Brief description (line 2)
        if i == 1 and stripped:
            data['brief_description'] = stripped
            
        # Category (line 3)
        if i == 2 and 'Instruction' in stripped:
            data['category'] = stripped
            
        # Syntax lines
        if any(inst in line for inst in instructions):
            if 'Dest' in line or '{#}Src' in line:
                data['syntax'].append(stripped)
                
        # Result
        if stripped.startswith('Result:'):
            data['result'] = stripped[7:].strip()
            
        # Parameters
        if stripped.startswith('●'):
            data['parameters'].append(stripped[1:].strip())
            
        # Encoding table
        if 'EEEE' in stripped:
            data['encoding'].append(stripped)
            
        # Explanation section
        if stripped.startswith('Explanation:'):
            # Collect explanation lines
            j = i + 1
            exp_lines = []
            while j < len(lines) and not lines[j].startswith('Related:'):
                if lines[j].strip():
                    exp_lines.append(lines[j].strip())
                j += 1
            data['explanation'] = '\n\n'.join(exp_lines)
    
    # Full description from result + explanation
    full_desc = []
    if data.get('result'):
        full_desc.append(data['result'])
    if data['explanation']:
        full_desc.append(data['explanation'])
    data['description'] = '\n\n'.join(full_desc)
    
    return data

# Extract missed grouped instructions
print("\nExtracting missed grouped instructions...")
extracted_groups = {}

for name, start, end in missed_groups:
    data = extract_grouped_section(name, start, end)
    for inst in data['instructions']:
        extracted_groups[inst] = data
        print(f"  Extracted: {inst}")

# Now update the YAMLs
print("\nUpdating YAMLs...")
for inst_name, group_data in extracted_groups.items():
    yaml_path = PASM2_PATH / f"{inst_name.lower()}.yaml"
    
    # Load existing YAML
    existing = {}
    if yaml_path.exists():
        with open(yaml_path, 'r') as f:
            existing = yaml.safe_load(f) or {}
    
    # Update with extracted content
    if group_data['brief_description']:
        existing['brief_description'] = group_data['brief_description']
    
    if group_data['category']:
        existing['category'] = group_data['category'] 
        
    if group_data['description']:
        existing['description'] = group_data['description']
        
    if group_data['parameters']:
        existing['parameters'] = group_data['parameters']
        
    if group_data['encoding']:
        # For grouped instructions, both encodings are relevant
        existing['encoding'] = group_data['encoding']
        
    # Mark as updated
    existing['documentation_source'] = 'PASM2 Manual 2022/11/01 Pages 31-147'
    existing['documentation_level'] = 'comprehensive'
    existing['manual_extraction_date'] = '2025-01-19'
    existing['last_updated'] = '2025-01-19'
    
    # Handle grouped instructions specially
    if len(group_data['instructions']) > 1:
        existing['group_documentation'] = True
        existing['grouped_with'] = group_data['instructions']
    
    # Save back
    with open(yaml_path, 'w') as f:
        yaml.dump(existing, f, default_flow_style=False, sort_keys=False, width=100)
    
    print(f"  Updated: {inst_name}")

print(f"\nCompleted updating {len(extracted_groups)} instructions")