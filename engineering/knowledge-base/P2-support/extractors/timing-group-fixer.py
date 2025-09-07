#!/usr/bin/env python3
"""
Fix timing for instructions in groups that have "All X instructions execute in N cycles"
"""

import re
from pathlib import Path
from datetime import datetime

def fix_group_timing():
    """Apply group timing to instructions that don't have explicit timing"""
    
    # Paths
    datasheet_path = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/p2-datasheet/pasm2-complete-instruction-tables.md")
    pasm2_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/instructions/pasm2")
    
    # Read datasheet
    with open(datasheet_path, 'r') as f:
        lines = f.readlines()
    
    # Track instructions by group
    group_instructions = {
        "math_and_logic": [],
        "pin_and_smart_pin": [],
        "interrupt": [],
        "register_indirection": [],
        "color_space_converter": []
    }
    
    current_group = None
    in_two_column_table = False
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Detect group timing declarations
        if "All Math and Logic instructions execute in 2 clock cycles" in line:
            current_group = "math_and_logic"
            in_two_column_table = True
            print(f"Found Math and Logic group (2 cycles)")
        elif "All Pin & Smart Pin instructions execute in 2 clock cycles" in line:
            current_group = "pin_and_smart_pin"  
            in_two_column_table = True
            print(f"Found Pin & Smart Pin group (2 cycles)")
        elif "All Interrupt instructions execute in 2 clock cycles" in line:
            current_group = "interrupt"
            in_two_column_table = True
            print(f"Found Interrupt group (2 cycles)")
        elif "All Register Indirection instructions execute in 2 clock cycles" in line:
            current_group = "register_indirection"
            in_two_column_table = True
            print(f"Found Register Indirection group (2 cycles)")
        elif "All Color Space Converter instructions execute in 2 clock cycles" in line:
            current_group = "color_space_converter"
            in_two_column_table = True
            print(f"Found Color Space Converter group (2 cycles)")
        
        # Detect transition to 3-column table (has explicit timing)
        if "| Instruction |" in line and "| Clock" in line:
            in_two_column_table = False
            current_group = None
        
        # Detect new section that might reset context
        if line.startswith("##") and "Instructions" in line:
            # Only reset if it's not one of our tracked groups
            if not any(group_name in line for group_name in ["Math and Logic", "Pin & Smart Pin", "Interrupt", "Register Indirection", "Color Space Converter"]):
                in_two_column_table = False
                current_group = None
        
        # Extract instructions from 2-column tables
        if in_two_column_table and current_group and line.startswith("| **"):
            match = re.match(r'\| \*\*([A-Z][A-Z0-9_]*)', line)
            if match:
                inst_name = match.group(1)
                # Check it's really a 2-column table (no third column with timing)
                parts = line.split('|')
                if len(parts) == 4:  # Empty first, instruction, description, empty last
                    group_instructions[current_group].append(inst_name)
    
    # Report findings
    print("\nInstructions by group:")
    total = 0
    for group, instructions in group_instructions.items():
        if instructions:
            print(f"  {group}: {len(instructions)} instructions")
            total += len(instructions)
    print(f"Total instructions in 2-cycle groups: {total}")
    
    # Now update YAML files for instructions that need group timing
    updated = 0
    already_correct = 0
    
    timestamp = datetime.now().isoformat()
    
    for group, instructions in group_instructions.items():
        for inst_name in instructions:
            yaml_path = pasm2_dir / f"pasm2_{inst_name.lower()}.yaml"
            
            if not yaml_path.exists():
                print(f"Warning: No file for {inst_name}")
                continue
            
            # Read existing YAML
            with open(yaml_path, 'r') as f:
                content = f.read()
            
            # Check current timing status
            has_layer2 = 'layer2_datasheet:' in content
            has_timing = 'timing:' in content and 'layer2_datasheet:' in content[:content.find('timing:') if 'timing:' in content else len(content)]
            
            if has_timing:
                # Check if it already has correct timing
                if 'raw: 2' in content or 'base_cycles: 2' in content:
                    already_correct += 1
                else:
                    print(f"  {inst_name} has different timing, not updating")
                continue
            
            # Add or update timing
            if not has_layer2:
                # Add complete layer2_datasheet section
                group_name = group.replace('_', ' ').title()
                new_section = f"""
layer2_datasheet:
  extraction_date: {timestamp}
  source: P2 Datasheet v35
  timing:
    raw: 2
    base_cycles: 2
    type: fixed
    source_note: From group declaration - all {group_name} instructions execute in 2 cycles"""
                
                with open(yaml_path, 'a') as f:
                    f.write(new_section + '\n')
                updated += 1
                print(f"Added timing to {inst_name}")
            else:
                # Has layer2 but no timing - would need careful insertion
                print(f"  {inst_name} has layer2_datasheet but no timing - needs manual fix")
    
    print(f"\n=== Final Summary ===")
    print(f"Files updated with group timing: {updated}")
    print(f"Files already correct: {already_correct}")
    print(f"Total instructions processed: {total}")

if __name__ == "__main__":
    fix_group_timing()