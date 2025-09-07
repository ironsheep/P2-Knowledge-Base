#!/usr/bin/env python3
"""
Add timing field to existing layer2_datasheet sections for group-timed instructions
"""

import re
from pathlib import Path
from datetime import datetime

def add_timing_to_layer2():
    """Add timing to layer2_datasheet sections that are missing it"""
    
    # Paths
    datasheet_path = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/p2-datasheet/pasm2-complete-instruction-tables.md")
    pasm2_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/instructions/pasm2")
    
    # Read datasheet to identify group instructions
    with open(datasheet_path, 'r') as f:
        lines = f.readlines()
    
    # Collect instructions from 2-cycle groups
    instructions_2cycle = set()
    current_group = None
    in_two_column_table = False
    
    for line in lines:
        line = line.strip()
        
        # Detect group timing declarations
        if "All Math and Logic instructions execute in 2 clock cycles" in line:
            current_group = "Math and Logic"
            in_two_column_table = True
        elif "All Pin & Smart Pin instructions execute in 2 clock cycles" in line:
            current_group = "Pin & Smart Pin"  
            in_two_column_table = True
        elif "All Interrupt instructions execute in 2 clock cycles" in line:
            current_group = "Interrupt"
            in_two_column_table = True
        elif "All Register Indirection instructions execute in 2 clock cycles" in line:
            current_group = "Register Indirection"
            in_two_column_table = True
        elif "All Color Space Converter instructions execute in 2 clock cycles" in line:
            current_group = "Color Space Converter"
            in_two_column_table = True
        
        # Detect transition to 3-column table
        if "| Instruction |" in line and "| Clock" in line:
            in_two_column_table = False
            current_group = None
        
        # Collect instructions from 2-column tables
        if in_two_column_table and current_group and line.startswith("| **"):
            match = re.match(r'\| \*\*([A-Z][A-Z0-9_]*)', line)
            if match:
                inst_name = match.group(1)
                parts = line.split('|')
                if len(parts) == 4:  # 2-column table
                    instructions_2cycle.add(inst_name.lower())
    
    print(f"Found {len(instructions_2cycle)} instructions in 2-cycle groups")
    
    # Process YAML files
    updated = 0
    already_has_timing = 0
    no_layer2 = 0
    
    for yaml_path in pasm2_dir.glob("pasm2_*.yaml"):
        inst_name = yaml_path.stem.replace('pasm2_', '')
        
        # Skip if not in 2-cycle group
        if inst_name not in instructions_2cycle:
            continue
        
        # Read file
        with open(yaml_path, 'r') as f:
            lines = f.readlines()
        
        # Find layer2_datasheet section
        layer2_start = -1
        has_timing = False
        next_section_start = len(lines)
        
        for i, line in enumerate(lines):
            if line.startswith('layer2_datasheet:'):
                layer2_start = i
            elif layer2_start >= 0 and line.startswith('layer'):
                # Found next section
                next_section_start = i
                break
            elif layer2_start >= 0 and '  timing:' in line:
                has_timing = True
                break
        
        if layer2_start < 0:
            no_layer2 += 1
            continue
        
        if has_timing:
            already_has_timing += 1
            continue
        
        # Add timing field to layer2_datasheet
        # Find the right place to insert (before next layer or at end of layer2)
        insert_pos = next_section_start
        
        # Create timing section
        timing_section = [
            "  timing:\n",
            "    raw: 2\n",
            "    base_cycles: 2\n",
            "    type: fixed\n",
            "    source_note: From group declaration - all instructions in this group execute in 2 cycles\n"
        ]
        
        # Insert timing
        new_lines = lines[:insert_pos] + timing_section
        if insert_pos < len(lines):
            new_lines.extend(lines[insert_pos:])
        
        # Write back
        with open(yaml_path, 'w') as f:
            f.writelines(new_lines)
        
        updated += 1
        print(f"Updated: {inst_name.upper()}")
    
    print(f"\n=== Summary ===")
    print(f"Files updated: {updated}")
    print(f"Already had timing: {already_has_timing}")
    print(f"No layer2_datasheet: {no_layer2}")

if __name__ == "__main__":
    add_timing_to_layer2()