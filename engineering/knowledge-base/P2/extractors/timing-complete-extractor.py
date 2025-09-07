#!/usr/bin/env python3
"""
Complete timing extractor that handles both individual and group timing declarations
"""

import re
from pathlib import Path
from datetime import datetime

def extract_complete_timing():
    """Extract timing for all instructions including group declarations"""
    
    # Paths
    datasheet_path = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/p2-datasheet/pasm2-complete-instruction-tables.md")
    pasm2_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/instructions/pasm2")
    
    # Read datasheet
    with open(datasheet_path, 'r') as f:
        content = f.read()
    
    # Track timing data
    instruction_timing = {}
    
    # First, find all group timing declarations
    group_timing_sections = {
        "Math and Logic": 2,
        "Pin & Smart Pin": 2,
        "Interrupt": 2,
        "Register Indirection": 2,
        "Color Space Converter": 2
    }
    
    # Process each section
    lines = content.split('\n')
    current_group = None
    group_timing = None
    
    for i, line in enumerate(lines):
        # Check for group headers with timing
        for group_name, cycles in group_timing_sections.items():
            if f"All {group_name} instructions execute in {cycles} clock cycles" in line:
                current_group = group_name
                group_timing = cycles
                print(f"Found group: {group_name} with {cycles} cycles timing")
                break
        
        # Check for section headers that might change context
        if line.startswith('##') and 'Instructions' in line:
            # Check if this is a new section
            if not any(group in line for group in group_timing_sections.keys()):
                current_group = None
                group_timing = None
        
        # Process instruction lines
        if line.startswith('| **') and not line.startswith('| Instruction'):
            # Extract instruction name
            match = re.match(r'\| \*\*([A-Z][A-Z0-9_]*)', line)
            if match:
                inst_name = match.group(1)
                
                # Check if it's a 3-column table (has explicit timing)
                parts = line.split('|')
                if len(parts) >= 4:  # 3-column table
                    timing_str = parts[3].strip()
                    if timing_str and not timing_str.startswith('Clock'):
                        instruction_timing[inst_name] = {
                            'raw': timing_str,
                            'source': 'explicit'
                        }
                elif group_timing is not None:  # 2-column table with group timing
                    instruction_timing[inst_name] = {
                        'raw': str(group_timing),
                        'source': f'group_{current_group.replace(" ", "_").lower()}'
                    }
    
    # Now process tables with explicit timing columns
    current_table = []
    in_table = False
    
    for line in lines:
        if '| Instruction |' in line and '| Clock' in line:
            in_table = True
            current_table = []
        elif in_table and line.startswith('|'):
            if line.startswith('|---'):
                continue
            current_table.append(line)
        elif in_table and not line.startswith('|'):
            # Process the completed table
            for table_line in current_table:
                parts = table_line.split('|')
                if len(parts) >= 4:
                    inst_part = parts[1].strip()
                    timing_part = parts[3].strip()
                    
                    # Extract instruction name
                    match = re.match(r'\*\*([A-Z][A-Z0-9_]*)', inst_part)
                    if match and timing_part:
                        inst_name = match.group(1)
                        # Only update if we don't already have it or if this is explicit
                        if inst_name not in instruction_timing or 'group' in instruction_timing[inst_name].get('source', ''):
                            instruction_timing[inst_name] = {
                                'raw': timing_part,
                                'source': 'explicit'
                            }
            
            in_table = False
            current_table = []
    
    print(f"\nTotal instructions with timing: {len(instruction_timing)}")
    
    # Parse timing patterns
    def parse_timing(timing_str):
        """Parse timing string into structured format"""
        result = {'raw': timing_str}
        
        # Simple fixed timing (just a number)
        if timing_str.isdigit():
            result['base_cycles'] = int(timing_str)
            result['type'] = 'fixed'
            return result
        
        # Range timing (e.g., "13...20")
        if '...' in timing_str:
            match = re.search(r'(\d+)\.\.\.(\d+)', timing_str)
            if match:
                result['min_cycles'] = int(match.group(1))
                result['max_cycles'] = int(match.group(2))
                result['type'] = 'variable'
                result['notes'] = ['Hub window alignment affects timing']
                return result
        
        # Conditional timing (e.g., "2 or 4")
        if ' or ' in timing_str:
            parts = re.findall(r'\d+', timing_str)
            if len(parts) >= 2:
                result['min_cycles'] = int(parts[0])
                result['max_cycles'] = int(parts[-1])
                result['type'] = 'conditional'
                if 'branch' in timing_str.lower() or '/' in timing_str:
                    result['notes'] = ['Branch taken/not taken affects timing']
                return result
        
        # Complex mode-dependent (e.g., "4 / 13...20")
        if '/' in timing_str:
            parts = timing_str.split('/')
            result['cog_lut_timing'] = parts[0].strip()
            if len(parts) > 1:
                result['hub_timing'] = parts[1].strip()
            result['type'] = 'mode_dependent'
            return result
        
        # Special cases
        if '+' in timing_str:
            result['type'] = 'variable'
            result['notes'] = ['Additional cycles based on wait condition']
        else:
            result['type'] = 'special'
        
        return result
    
    # Update YAML files
    updated = 0
    already_has = 0
    not_found = 0
    
    for inst_name, timing_data in instruction_timing.items():
        yaml_path = pasm2_dir / f"pasm2_{inst_name.lower()}.yaml"
        
        if not yaml_path.exists():
            not_found += 1
            print(f"No file for: {inst_name}")
            continue
        
        # Read existing YAML
        with open(yaml_path, 'r') as f:
            yaml_content = f.read()
        
        # Check if layer2_datasheet already exists with timing
        if 'layer2_datasheet:' in yaml_content and 'timing:' in yaml_content:
            already_has += 1
            continue
        
        # Parse the timing
        parsed = parse_timing(timing_data['raw'])
        
        # Create layer2_datasheet section
        timestamp = datetime.now().isoformat()
        
        if 'layer2_datasheet:' not in yaml_content:
            # Add new layer2_datasheet section
            datasheet_section = f"""
layer2_datasheet:
  extraction_date: {timestamp}
  source: P2 Datasheet v35
  timing:
    raw: {timing_data['raw']}"""
            
            if 'base_cycles' in parsed:
                datasheet_section += f"\n    base_cycles: {parsed['base_cycles']}"
            if 'min_cycles' in parsed:
                datasheet_section += f"\n    min_cycles: {parsed['min_cycles']}"
            if 'max_cycles' in parsed:
                datasheet_section += f"\n    max_cycles: {parsed['max_cycles']}"
            if 'type' in parsed:
                datasheet_section += f"\n    type: {parsed['type']}"
            if 'cog_lut_timing' in parsed:
                datasheet_section += f"\n    cog_lut_timing: {parsed['cog_lut_timing']}"
            if 'hub_timing' in parsed:
                datasheet_section += f"\n    hub_timing: {parsed['hub_timing']}"
            if 'notes' in parsed:
                datasheet_section += f"\n    notes:"
                for note in parsed['notes']:
                    datasheet_section += f"\n      - {note}"
            if 'group' in timing_data.get('source', ''):
                datasheet_section += f"\n    source_note: From group declaration - all {timing_data['source'].replace('group_', '').replace('_', ' ')} instructions"
            
            # Append to file
            with open(yaml_path, 'a') as f:
                f.write(datasheet_section + '\n')
        else:
            # Update existing layer2_datasheet with timing
            # This is more complex - would need careful insertion
            # For now, skip if layer2 exists but no timing
            print(f"Skipping {inst_name} - has layer2_datasheet but no timing")
            continue
        
        updated += 1
        print(f"Updated: {inst_name} with timing: {timing_data['raw']}")
    
    print(f"\n=== Summary ===")
    print(f"Total instructions with timing data: {len(instruction_timing)}")
    print(f"Files updated: {updated}")
    print(f"Files already have timing: {already_has}")
    print(f"Files not found: {not_found}")
    
    # List some examples
    print(f"\nExample timings extracted:")
    examples = list(instruction_timing.items())[:10]
    for inst, timing in examples:
        source_note = f" (from {timing['source']})" if 'source' in timing else ""
        print(f"  {inst}: {timing['raw']}{source_note}")

if __name__ == "__main__":
    extract_complete_timing()