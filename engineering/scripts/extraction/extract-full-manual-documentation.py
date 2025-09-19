#!/usr/bin/env python3
"""
Extract COMPLETE documentation from PASM2 manual pages 31-147.
This script captures ALL content including explanations, examples, notes, and warnings.
"""

import re
import yaml
from pathlib import Path
from collections import defaultdict
import json

# Paths
MANUAL_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/pasm2-manual/pasm2-manual-narrative.txt")
PASM2_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/pasm2")
OUTPUT_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/extracted-documentation")

# Create output directory
OUTPUT_PATH.mkdir(exist_ok=True, parents=True)

print("Loading PASM2 manual...")
with open(MANUAL_PATH, 'r', encoding='utf-8') as f:
    manual_lines = f.readlines()

# Convert to single text for some operations
manual_text = ''.join(manual_lines)

def find_instruction_sections():
    """Find all instruction documentation sections in the manual."""
    sections = []
    current_section = None
    in_instruction = False
    
    # Patterns that indicate start of instruction documentation
    instruction_patterns = [
        r'^[A-Z][A-Z0-9]+(?:/[A-Z0-9]+)*$',  # Single or grouped instructions like "ADD" or "ADDCT1/2/3"
        r'^[A-Z][A-Z0-9]+(?:\s+[A-Z][A-Z0-9]+)*$',  # Space-separated like "ADD signed"
    ]
    
    # Pattern that indicates we've hit the next section
    end_patterns = [
        r'^Copyright ©',
        r'^\s*Page \d+',
        r'^[A-Z][A-Z0-9]+(?:/[A-Z0-9]+)*$',  # Next instruction
    ]
    
    i = 0
    while i < len(manual_lines):
        line = manual_lines[i].strip()
        
        # Check if this is an instruction header
        for pattern in instruction_patterns:
            if re.match(pattern, line) and i > 0:
                # Check if next line is a description (not another instruction)
                if i + 1 < len(manual_lines):
                    next_line = manual_lines[i + 1].strip()
                    # If next line is lowercase or contains description-like text
                    if next_line and (next_line[0].islower() or 
                                     any(word in next_line.lower() for word in 
                                         ['instruction', 'directive', 'operation', 'event', 'math', 'bit', 'color'])):
                        
                        # Save previous section if exists
                        if current_section:
                            sections.append(current_section)
                        
                        # Start new section
                        current_section = {
                            'name': line,
                            'start_line': i,
                            'lines': [manual_lines[i]]
                        }
                        in_instruction = True
                        break
        
        # If we're in an instruction section, collect lines
        if in_instruction and current_section:
            if i > current_section['start_line']:
                # Check if we've hit the end
                is_end = False
                for pattern in end_patterns:
                    if re.match(pattern, line) and i > current_section['start_line'] + 2:
                        is_end = True
                        break
                
                if is_end:
                    current_section['end_line'] = i - 1
                    in_instruction = False
                else:
                    current_section['lines'].append(manual_lines[i])
        
        i += 1
    
    # Don't forget the last section
    if current_section and 'end_line' not in current_section:
        current_section['end_line'] = len(manual_lines) - 1
        sections.append(current_section)
    
    return sections

def parse_instruction_section(section):
    """Parse a single instruction section into structured data."""
    lines = section['lines']
    name = section['name']
    
    # Initialize data structure
    data = {
        'instruction_names': [],
        'brief_description': '',
        'category': '',
        'full_description': '',
        'syntax': [],
        'result': '',
        'parameters': [],
        'encoding_table': [],
        'flags': {},
        'related': [],
        'explanation': '',
        'notes': [],
        'examples': [],
        'warnings': [],
        'timing': {}
    }
    
    # Parse instruction names (handle grouped like ADDCT1/2/3)
    if '/' in name:
        # Handle grouped instructions
        parts = name.split('/')
        base = parts[0].rstrip('0123456789')
        for part in parts:
            if part[0].isdigit():
                data['instruction_names'].append(base + part.strip())
            else:
                data['instruction_names'].append(part.strip())
    else:
        data['instruction_names'].append(name)
    
    # Parse the content
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Brief description (usually line 2)
        if i == 1 and line and not line.startswith('COND'):
            data['brief_description'] = line
        
        # Category (usually line 3)
        if i == 2 and 'Instruction' in line:
            data['category'] = line
        
        # Syntax lines
        if i > 0 and any(name in line for name in data['instruction_names']):
            # Check if it's a syntax line (has specific format)
            if re.search(r'\s+(Dest|D|Src|S|{#}|WC|WZ|WCZ)', line):
                data['syntax'].append(line)
        
        # Result line
        if line.startswith('Result:'):
            data['result'] = line[7:].strip()
            # Collect multi-line results
            j = i + 1
            while j < len(lines) and lines[j].startswith('    ') and not lines[j].strip().startswith('●'):
                data['result'] += ' ' + lines[j].strip()
                j += 1
        
        # Parameters (bullet points)
        if line.strip().startswith('●'):
            param_text = line[1:].strip()
            # Collect multi-line parameters
            j = i + 1
            while j < len(lines) and lines[j].startswith('        '):
                param_text += ' ' + lines[j].strip()
                j += 1
            data['parameters'].append(param_text)
        
        # Encoding table
        if 'COND' in line and 'INSTR' in line and 'FX' in line:
            # This is the header of the encoding table
            j = i + 1
            while j < len(lines) and 'EEEE' in lines[j]:
                data['encoding_table'].append(lines[j].strip())
                j += 1
        
        # Related instructions
        if line.startswith('Related:'):
            related_text = line[8:].strip()
            data['related'] = [r.strip() for r in re.split(r'[,;]|and', related_text) if r.strip()]
        
        # Explanation section
        if line.startswith('Explanation:'):
            j = i + 1
            explanation_lines = []
            while j < len(lines) and not lines[j].startswith('Notes:') and not lines[j].startswith('Example'):
                if lines[j].strip():
                    explanation_lines.append(lines[j].strip())
                j += 1
            data['explanation'] = '\n\n'.join(explanation_lines)
        
        # Notes section
        if line.startswith('Notes:') or line.startswith('Note:'):
            j = i + 1
            while j < len(lines) and not lines[j].startswith('Example'):
                if lines[j].strip():
                    if lines[j].strip().startswith('●'):
                        data['notes'].append(lines[j].strip()[1:].strip())
                    else:
                        data['notes'].append(lines[j].strip())
                j += 1
        
        # Examples section
        if line.startswith('Example'):
            j = i + 1
            example_text = []
            while j < len(lines) and j < i + 20:  # Limit example collection
                if lines[j].strip():
                    example_text.append(lines[j])
                j += 1
            if example_text:
                data['examples'].append(''.join(example_text))
        
        # Warnings (often in explanation)
        if 'WARNING' in line.upper() or 'CAUTION' in line.upper():
            data['warnings'].append(line)
        
        # Flag effects (from encoding table or explicit descriptions)
        if 'C Flag' in line or 'Z Flag' in line:
            # Parse flag formulas from encoding table
            if 'EEEE' in line:
                parts = line.split()
                for k, part in enumerate(parts):
                    if k > 0 and parts[k-1] in ['C', 'Flag']:
                        data['flags']['C'] = part
                    if k > 0 and parts[k-1] in ['Z', 'Flag']:
                        data['flags']['Z'] = part
        
        i += 1
    
    return data

def update_yaml_with_manual_data(instruction_name, manual_data):
    """Update or create YAML file with complete manual documentation."""
    yaml_path = PASM2_PATH / f"{instruction_name.lower()}.yaml"
    
    # Load existing YAML if it exists
    existing_data = {}
    if yaml_path.exists():
        with open(yaml_path, 'r') as f:
            existing_data = yaml.safe_load(f) or {}
    
    # Merge manual data into YAML structure
    updated_data = existing_data.copy()
    
    # Update with manual content (preserving existing technical fields)
    if manual_data['brief_description']:
        updated_data['brief_description'] = manual_data['brief_description']
    
    if manual_data['category']:
        updated_data['category'] = manual_data['category']
    
    if manual_data['full_description'] or manual_data['explanation']:
        full_desc = manual_data['full_description']
        if manual_data['explanation']:
            full_desc = (full_desc + '\n\n' + manual_data['explanation']).strip()
        if full_desc:
            updated_data['description'] = full_desc
    
    if manual_data['result']:
        updated_data['result_description'] = manual_data['result']
    
    if manual_data['syntax']:
        # Keep the first clean syntax
        for syntax in manual_data['syntax']:
            if instruction_name in syntax:
                updated_data['manual_syntax'] = syntax.strip()
                break
    
    if manual_data['parameters']:
        updated_data['parameters'] = manual_data['parameters']
    
    if manual_data['related']:
        updated_data['related'] = manual_data['related']
    
    if manual_data['notes']:
        updated_data['usage_notes'] = '\n'.join(manual_data['notes'])
    
    if manual_data['warnings']:
        updated_data['warnings'] = manual_data['warnings']
    
    if manual_data['examples']:
        # Parse examples into structured format
        example_list = []
        for ex in manual_data['examples']:
            # Try to extract code from example text
            lines = ex.split('\n')
            for line in lines:
                if any(instruction_name in line for instruction_name in manual_data['instruction_names']):
                    example_list.append({'code': line.strip()})
        if example_list:
            updated_data['examples'] = example_list
    
    # Update documentation level
    updated_data['documentation_source'] = 'PASM2 Manual 2022/11/01 Pages 31-147'
    updated_data['documentation_level'] = 'comprehensive'
    updated_data['manual_extraction_complete'] = True
    
    return updated_data

# Main extraction process
print("\nFinding all instruction sections in manual...")
sections = find_instruction_sections()
print(f"Found {len(sections)} instruction documentation sections")

# Parse each section
parsed_instructions = {}
for section in sections:
    parsed_data = parse_instruction_section(section)
    
    # Store data for each instruction variant
    for inst_name in parsed_data['instruction_names']:
        parsed_instructions[inst_name] = parsed_data
        print(f"  Parsed: {inst_name}")

# Save extracted data for review
extraction_file = OUTPUT_PATH / "complete_manual_extraction.json"
with open(extraction_file, 'w') as f:
    json.dump(parsed_instructions, f, indent=2)

print(f"\nExtracted documentation saved to: {extraction_file}")

# Generate update report
print("\nGenerating update report...")
update_report = []
yaml_updates = {}

for inst_name, manual_data in parsed_instructions.items():
    yaml_path = PASM2_PATH / f"{inst_name.lower()}.yaml"
    
    if yaml_path.exists():
        # Compare with existing
        with open(yaml_path, 'r') as f:
            existing = yaml.safe_load(f) or {}
        
        missing_fields = []
        if not existing.get('explanation') and manual_data['explanation']:
            missing_fields.append('explanation')
        if not existing.get('parameters') and manual_data['parameters']:
            missing_fields.append('parameters')
        if not existing.get('examples') and manual_data['examples']:
            missing_fields.append('examples')
        if not existing.get('usage_notes') and manual_data['notes']:
            missing_fields.append('notes')
        
        if missing_fields:
            update_report.append({
                'instruction': inst_name,
                'missing': missing_fields,
                'manual_has': {
                    'explanation': len(manual_data['explanation']),
                    'parameters': len(manual_data['parameters']),
                    'examples': len(manual_data['examples']),
                    'notes': len(manual_data['notes'])
                }
            })
            
            # Prepare update
            yaml_updates[inst_name] = update_yaml_with_manual_data(inst_name, manual_data)
    else:
        # New instruction
        yaml_updates[inst_name] = update_yaml_with_manual_data(inst_name, manual_data)
        update_report.append({
            'instruction': inst_name,
            'status': 'NEW - not in YAMLs'
        })

# Save update report
report_file = OUTPUT_PATH / "extraction_update_report.yaml"
with open(report_file, 'w') as f:
    yaml.dump(update_report, f, default_flow_style=False)

print(f"Update report saved to: {report_file}")

# Save prepared YAML updates
updates_dir = OUTPUT_PATH / "yaml_updates"
updates_dir.mkdir(exist_ok=True)

for inst_name, yaml_data in yaml_updates.items():
    update_file = updates_dir / f"{inst_name.lower()}.yaml"
    with open(update_file, 'w') as f:
        yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False)

print(f"\nPrepared {len(yaml_updates)} YAML updates in: {updates_dir}")
print("\nTo apply updates, review the files and copy them to the main YAML directory.")
print("Or run the apply_manual_updates.py script to merge them automatically.")