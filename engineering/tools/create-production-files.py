#!/usr/bin/env python3
"""
Convert multi-layer source files to clean production files
"""

from pathlib import Path
import re

def convert_pasm2_instruction(source_file, production_dir):
    """Convert a multi-layer PASM2 instruction file to production format"""
    
    # Read source file
    with open(source_file, 'r') as f:
        content = f.read()
    
    # Parse the layers (simple text parsing)
    data = {}
    current_section = None
    
    for line in content.split('\n'):
        # Detect sections
        if line.startswith('metadata:'):
            current_section = 'metadata'
        elif line.startswith('layer1_csv:'):
            current_section = 'layer1'
        elif line.startswith('layer2_datasheet:'):
            current_section = 'layer2'
        elif line.startswith('layer3_narrative:'):
            current_section = 'layer3'
        elif line.startswith('layer4_'):
            current_section = 'layer4'
        
        # Extract key fields
        if 'mnemonic:' in line:
            data['mnemonic'] = line.split(':', 1)[1].strip()
        elif 'syntax:' in line and current_section in ['layer1', 'layer3']:
            syntax = line.split(':', 1)[1].strip().strip('"').strip('|').strip()
            if 'syntax' not in data or len(syntax) > len(data.get('syntax', '')):
                data['syntax'] = syntax
        elif 'encoding:' in line:
            data['encoding'] = line.split(':', 1)[1].strip()
        elif 'group:' in line:
            data['group'] = line.split(':', 1)[1].strip()
        elif 'description:' in line and current_section in ['layer1', 'layer3']:
            desc = line.split(':', 1)[1].strip().strip('"').strip('|').strip()
            if desc and ('description' not in data or len(desc) > len(data.get('description', ''))):
                data['description'] = desc
        elif 'base_cycles:' in line:
            data['cycles'] = line.split(':', 1)[1].strip()
        elif 'type:' in line and current_section == 'layer2' and 'timing' in content[max(0, content.index(line)-100):content.index(line)]:
            data['timing_type'] = line.split(':', 1)[1].strip()
    
    # Clean up description
    if 'description' in data:
        # Remove excessive spaces
        data['description'] = re.sub(r'\s+', ' ', data['description'])
        # Parse out flag effects if present
        if 'C =' in data['description']:
            c_match = re.search(r'C = ([^.]+)', data['description'])
            if c_match:
                data['c_flag'] = c_match.group(1).strip()
        if 'Z =' in data['description']:
            z_match = re.search(r'Z = ([^.]+)', data['description'])
            if z_match:
                data['z_flag'] = z_match.group(1).strip()
    
    # Generate production YAML
    inst_name = source_file.stem.replace('pasm2_', '')
    production_content = []
    
    production_content.append(f"instruction: {data.get('mnemonic', inst_name.upper())}")
    
    if 'syntax' in data:
        production_content.append(f"syntax: {data['syntax']}")
    
    if 'encoding' in data:
        production_content.append(f"encoding: {data['encoding']}")
    
    if 'description' in data:
        # Clean up the description
        desc = data['description']
        # Remove the formula part if it's redundant with description
        if 'D =' in desc:
            parts = desc.split('.')
            if len(parts) > 1:
                desc = parts[0].strip()
        production_content.append(f"description: |")
        production_content.append(f"  {desc}")
    
    if 'cycles' in data:
        production_content.append(f"timing:")
        production_content.append(f"  cycles: {data['cycles']}")
        if 'timing_type' in data:
            production_content.append(f"  type: {data['timing_type']}")
    
    if 'group' in data:
        production_content.append(f"group: {data['group']}")
    
    # Add flag effects if found
    if 'c_flag' in data or 'z_flag' in data:
        production_content.append("flags_affected:")
        if 'c_flag' in data:
            production_content.append(f"  C: {data['c_flag']}")
        if 'z_flag' in data:
            production_content.append(f"  Z: {data['z_flag']}")
    
    # Write production file
    production_file = production_dir / f"{inst_name}.yaml"
    with open(production_file, 'w') as f:
        f.write('\n'.join(production_content) + '\n')
    
    return production_file

def main():
    """Convert all source files to production format"""
    
    base_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2")
    
    # PASM2 instructions
    source_dir = base_dir / "production/_sources/instructions/pasm2"
    production_dir = base_dir / "production/instructions/pasm2"
    
    if source_dir.exists():
        print(f"Converting PASM2 instructions...")
        count = 0
        for source_file in source_dir.glob("pasm2_*.yaml"):
            convert_pasm2_instruction(source_file, production_dir)
            count += 1
            if count % 50 == 0:
                print(f"  Converted {count} files...")
        print(f"  Total: {count} PASM2 instructions converted")
    
    # TODO: Add converters for Spin2, hardware, architecture
    
    print("\nProduction file generation complete!")
    print(f"Files created in: {base_dir}/production/")

if __name__ == "__main__":
    main()