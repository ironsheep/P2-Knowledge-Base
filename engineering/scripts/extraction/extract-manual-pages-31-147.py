#!/usr/bin/env python3
"""
Extract COMPLETE documentation from PASM2 manual pages 31-147.
This version properly identifies instruction boundaries and captures all content.
"""

import re
import yaml
from pathlib import Path
from collections import defaultdict
import json

# Paths
MANUAL_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/pasm2-manual/pasm2-manual-narrative.txt")
PASM2_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/pasm2")
DIRECTIVES_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/spin2/assembly-directives")
OUTPUT_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/extracted-documentation")

# Create output directory
OUTPUT_PATH.mkdir(exist_ok=True, parents=True)

print("Loading PASM2 manual...")
with open(MANUAL_PATH, 'r', encoding='utf-8') as f:
    manual_lines = f.readlines()

def find_all_instruction_sections():
    """Find ALL instruction documentation sections in the manual."""
    sections = []
    
    # Find where instruction documentation starts and ends
    start_line = None
    end_line = None
    
    for i, line in enumerate(manual_lines):
        # Look for ABS instruction (first detailed instruction doc on page 31)
        if i > 1500 and line.strip() == 'ABS' and i+1 < len(manual_lines):
            if 'Absolute' in manual_lines[i+1]:
                start_line = i
                print(f"Found documentation start at line {i}: ABS")
                break
    
    # Find end of instruction documentation (around page 147)
    if start_line:
        for i in range(start_line + 1000, min(start_line + 20000, len(manual_lines))):
            line = manual_lines[i].strip()
            # Look for section headers that indicate end of instructions
            if 'INDEX' in line or 'Appendix' in line or 'GLOSSARY' in line:
                end_line = i
                print(f"Found documentation end at line {i}: {line}")
                break
    
    if not end_line:
        end_line = len(manual_lines)
    
    print(f"Processing lines {start_line} to {end_line}")
    
    # Now find each instruction section
    i = start_line
    current_section = None
    
    while i < end_line:
        line = manual_lines[i].strip()
        
        # Check for instruction header pattern
        # Pattern: ALL CAPS word at start of line, followed by description on next line
        if (line and 
            len(line) <= 20 and  # Instruction names are short
            re.match(r'^[A-Z][A-Z0-9/]+$', line) and  # All caps, possibly with slash for grouped
            i+1 < len(manual_lines)):
            
            next_line = manual_lines[i+1].strip()
            
            # Check if next line looks like a description
            # Descriptions often start with a capital letter or contain "instruction"
            if (next_line and 
                (next_line[0].isupper() or 
                 'instruction' in next_line.lower() or
                 'directive' in next_line.lower() or
                 'event' in next_line.lower())):
                
                # Save previous section if exists
                if current_section:
                    current_section['end_line'] = i - 1
                    sections.append(current_section)
                
                # Start new section
                current_section = {
                    'name': line,
                    'start_line': i,
                    'lines': []
                }
                print(f"  Found instruction: {line} at line {i}")
        
        # Collect lines for current section
        if current_section:
            current_section['lines'].append(manual_lines[i])
        
        i += 1
    
    # Don't forget the last section
    if current_section:
        current_section['end_line'] = end_line - 1
        sections.append(current_section)
    
    print(f"Total sections found: {len(sections)}")
    return sections

def parse_instruction_content(section):
    """Parse the content of an instruction section into structured data."""
    lines = section['lines']
    name = section['name'].strip()
    
    # Initialize comprehensive data structure
    data = {
        'instruction': name,
        'instruction_names': [],
        'brief_description': '',
        'category': '',
        'syntax': [],
        'syntax_variants': [],
        'result': '',
        'parameters': [],
        'encoding': [],
        'flags_affected': {},
        'related': [],
        'explanation': [],
        'notes': [],
        'examples': [],
        'timing': {},
        'full_text': ''.join(lines)  # Keep full text for reference
    }
    
    # Handle grouped instructions (e.g., ADDCT1/2/3)
    if '/' in name:
        # Parse grouped variants
        base = re.match(r'^([A-Z]+)', name).group(1)
        suffixes = re.findall(r'/(\d+|\w+)', name)
        data['instruction_names'] = [name.split('/')[0]]
        for suffix in suffixes:
            data['instruction_names'].append(base + suffix)
    else:
        data['instruction_names'] = [name]
    
    # Parse line by line
    in_explanation = False
    in_notes = False
    in_example = False
    explanation_lines = []
    notes_lines = []
    example_lines = []
    
    for i, line in enumerate(lines):
        line_text = line.rstrip()
        stripped = line_text.strip()
        
        # Get brief description (line 2)
        if i == 1 and stripped and not stripped.startswith('Copyright'):
            data['brief_description'] = stripped
        
        # Get category (line 3, often contains "Instruction")
        if i == 2 and 'Instruction' in line_text:
            data['category'] = stripped
        
        # Syntax lines (contain instruction name with parameters)
        if any(inst in line_text for inst in data['instruction_names']):
            # Check for syntax pattern
            if re.search(r'(Dest|{#}Src|WC|WZ|WCZ|\[|\])', line_text):
                syntax = stripped
                if syntax and syntax not in data['syntax_variants']:
                    data['syntax_variants'].append(syntax)
                    if not data['syntax']:
                        data['syntax'] = syntax
        
        # Result line
        if stripped.startswith('Result:'):
            data['result'] = stripped[7:].strip()
            # Continue collecting if wrapped
            j = i + 1
            while j < len(lines) and lines[j].startswith('    ') and not lines[j].strip().startswith('●'):
                data['result'] += ' ' + lines[j].strip()
                j += 1
        
        # Parameters (bullet points)
        if stripped.startswith('●'):
            param = stripped[1:].strip()
            # Collect wrapped parameter text
            j = i + 1
            while j < len(lines) and lines[j].startswith('        '):
                param += ' ' + lines[j].strip()
                j += 1
            data['parameters'].append(param)
        
        # Encoding table
        if 'COND' in line_text and 'INSTR' in line_text and 'DEST' in line_text:
            # This is the header, next lines contain encoding
            j = i + 1
            while j < len(lines) and 'EEEE' in lines[j]:
                encoding_line = lines[j].strip()
                data['encoding'].append(encoding_line)
                
                # Parse flags from encoding table
                parts = encoding_line.split()
                if len(parts) >= 7:
                    # Try to extract C and Z flag formulas
                    for k in range(5, len(parts)):
                        if 'carry' in parts[k].lower() or 'S[31]' in parts[k] or 'D[31]' in parts[k]:
                            data['flags_affected']['C'] = ' '.join(parts[k:k+3]) if k+3 <= len(parts) else parts[k]
                        elif 'Result' in parts[k] and '=' in ' '.join(parts[k:k+3]):
                            data['flags_affected']['Z'] = ' '.join(parts[k:k+3])
                j += 1
        
        # Timing info (look for "Clocks" column value)
        if 'Clocks' in line_text and i > 0:
            # Next line might have timing
            if i + 1 < len(lines) and 'EEEE' in lines[i+1]:
                timing_line = lines[i+1].strip().split()
                if timing_line and timing_line[-1].isdigit():
                    data['timing'] = {'cycles': int(timing_line[-1]), 'type': 'fixed'}
        
        # Related instructions
        if stripped.startswith('Related:'):
            related_text = stripped[8:].strip()
            # Parse comma/and separated list
            related_items = re.split(r',|and', related_text)
            data['related'] = [item.strip() for item in related_items if item.strip()]
        
        # Section transitions
        if stripped.startswith('Explanation:'):
            in_explanation = True
            in_notes = False
            in_example = False
            continue
        elif stripped.startswith('Notes:') or stripped.startswith('Note:'):
            in_notes = True
            in_explanation = False
            in_example = False
            continue
        elif stripped.startswith('Example'):
            in_example = True
            in_notes = False
            in_explanation = False
            continue
        
        # Collect section content
        if in_explanation and stripped and not stripped.startswith('Copyright'):
            explanation_lines.append(stripped)
        elif in_notes and stripped and not stripped.startswith('Copyright'):
            if stripped.startswith('●'):
                notes_lines.append(stripped[1:].strip())
            else:
                notes_lines.append(stripped)
        elif in_example and stripped and not stripped.startswith('Copyright'):
            example_lines.append(line_text)  # Keep formatting for examples
    
    # Process collected sections
    if explanation_lines:
        data['explanation'] = '\n\n'.join(explanation_lines)
    
    if notes_lines:
        data['notes'] = notes_lines
    
    if example_lines:
        # Try to extract code examples
        code_examples = []
        current_example = []
        for line in example_lines:
            # Look for lines that contain instruction usage
            if any(inst in line.upper() for inst in data['instruction_names']):
                if current_example:
                    code_examples.append('\n'.join(current_example))
                    current_example = []
                current_example.append(line)
            elif current_example:
                current_example.append(line)
        if current_example:
            code_examples.append('\n'.join(current_example))
        data['examples'] = code_examples
    
    return data

# Main extraction
print("\n" + "="*60)
print("EXTRACTING ALL INSTRUCTION DOCUMENTATION FROM PAGES 31-147")
print("="*60)

sections = find_all_instruction_sections()

# Parse all sections
all_instructions = {}
instruction_count = 0
directive_count = 0

for section in sections:
    parsed = parse_instruction_content(section)
    
    # Store for each variant
    for inst_name in parsed['instruction_names']:
        all_instructions[inst_name] = parsed
        instruction_count += 1
        
        # Check if it's a directive
        if inst_name in ['ALIGNL', 'ALIGNW', 'ORG', 'ORGF', 'ORGH', 'RES', 'FIT', 'BYTE', 'WORD', 'LONG', 'FILE']:
            directive_count += 1

print(f"\nExtracted {instruction_count} instruction variants")
print(f"Including {directive_count} directives")

# Save complete extraction
extraction_file = OUTPUT_PATH / "pages_31_147_complete_extraction.json"
with open(extraction_file, 'w') as f:
    json.dump(all_instructions, f, indent=2)

print(f"\nComplete extraction saved to: {extraction_file}")

# Create update statistics
stats = {
    'total_extracted': len(all_instructions),
    'has_explanation': sum(1 for d in all_instructions.values() if d['explanation']),
    'has_parameters': sum(1 for d in all_instructions.values() if d['parameters']),
    'has_examples': sum(1 for d in all_instructions.values() if d['examples']),
    'has_notes': sum(1 for d in all_instructions.values() if d['notes']),
    'has_encoding': sum(1 for d in all_instructions.values() if d['encoding']),
    'has_timing': sum(1 for d in all_instructions.values() if d['timing']),
    'has_flags': sum(1 for d in all_instructions.values() if d['flags_affected'])
}

print("\nExtraction Statistics:")
for key, value in stats.items():
    print(f"  {key}: {value}")

# Generate YAML updates
print("\n" + "="*60)
print("GENERATING YAML UPDATES")
print("="*60)

updates_dir = OUTPUT_PATH / "yaml_updates_pages_31_147"
updates_dir.mkdir(exist_ok=True)

update_count = 0
for inst_name, data in all_instructions.items():
    # Determine if instruction or directive
    is_directive = inst_name in ['ALIGNL', 'ALIGNW', 'ORG', 'ORGF', 'ORGH', 'RES', 'FIT', 'BYTE', 'WORD', 'LONG', 'FILE']
    
    if is_directive:
        yaml_path = DIRECTIVES_PATH / f"{inst_name.lower()}.yaml"
        yaml_type = "directive"
    else:
        yaml_path = PASM2_PATH / f"{inst_name.lower()}.yaml"
        yaml_type = "instruction"
    
    # Load existing YAML or start fresh
    existing = {}
    if yaml_path.exists():
        with open(yaml_path, 'r') as f:
            existing = yaml.safe_load(f) or {}
    
    # Build updated YAML preserving existing fields
    updated = existing.copy()
    
    # Update with extracted content
    if data['brief_description']:
        updated['brief_description'] = data['brief_description']
    
    if data['category']:
        updated['category'] = data['category']
    
    if data['syntax']:
        updated['syntax'] = data['syntax']
    
    if data['syntax_variants']:
        updated['syntax_variants'] = data['syntax_variants']
    
    if data['explanation']:
        # Merge with existing description if present
        if 'description' in updated:
            if data['explanation'] not in updated['description']:
                updated['description'] = updated['description'] + '\n\n' + data['explanation']
        else:
            updated['description'] = data['explanation']
    
    if data['result']:
        updated['result'] = data['result']
    
    if data['parameters']:
        updated['parameters'] = data['parameters']
    
    if data['encoding']:
        # Convert to single encoding string if multiple
        if len(data['encoding']) == 1:
            updated['encoding'] = data['encoding'][0]
        else:
            updated['encoding'] = data['encoding']
    
    if data['timing']:
        updated['timing'] = data['timing']
    
    if data['flags_affected']:
        updated['flags_affected'] = data['flags_affected']
    
    if data['related']:
        updated['related'] = data['related']
    
    if data['notes']:
        updated['usage_notes'] = '\n'.join(data['notes'])
    
    if data['examples']:
        # Convert to structured format
        example_list = []
        for ex in data['examples']:
            if ex.strip():
                example_list.append({'code': ex.strip()})
        if example_list:
            updated['examples'] = example_list
    
    # Mark as comprehensively documented
    updated['documentation_source'] = 'PASM2 Manual 2022/11/01 Pages 31-147'
    updated['documentation_level'] = 'comprehensive'
    updated['manual_extraction_date'] = '2025-01-19'
    
    # Save update file
    update_file = updates_dir / f"{inst_name.lower()}.yaml"
    with open(update_file, 'w') as f:
        yaml.dump(updated, f, default_flow_style=False, sort_keys=False, width=100)
    
    update_count += 1
    if update_count <= 10:
        print(f"  Created update for {inst_name} ({yaml_type})")

if update_count > 10:
    print(f"  ... and {update_count - 10} more")

print(f"\nGenerated {update_count} YAML updates in: {updates_dir}/")
print("\nNext step: Run apply-manual-updates.py to merge these into the knowledge base")