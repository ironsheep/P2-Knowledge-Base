#!/usr/bin/env python3
"""
Convert all multi-layer source files to clean production files
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

def convert_spin2_file(source_file, production_dir, file_type):
    """Convert a Spin2 method or operator file to production format"""
    
    # Read source file
    with open(source_file, 'r') as f:
        content = f.read()
    
    # Parse fields
    data = {}
    for line in content.split('\n'):
        if 'name:' in line:
            data['name'] = line.split(':', 1)[1].strip()
        elif 'type:' in line:
            data['type'] = line.split(':', 1)[1].strip()
        elif 'syntax:' in line:
            data['syntax'] = line.split(':', 1)[1].strip().strip('"')
        elif 'description:' in line:
            desc = line.split(':', 1)[1].strip().strip('"')
            if desc and 'description' not in data:
                data['description'] = desc
        elif 'returns:' in line:
            data['returns'] = line.split(':', 1)[1].strip()
        elif 'category:' in line:
            data['category'] = line.split(':', 1)[1].strip()
    
    # Generate production YAML
    name = source_file.stem.replace('spin2_', '')
    production_content = []
    
    production_content.append(f"{file_type}: {data.get('name', name)}")
    
    if 'type' in data:
        production_content.append(f"type: {data['type']}")
    
    if 'syntax' in data:
        production_content.append(f"syntax: {data['syntax']}")
    
    if 'description' in data:
        production_content.append(f"description: |")
        production_content.append(f"  {data['description']}")
    
    if 'returns' in data:
        production_content.append(f"returns: {data['returns']}")
    
    if 'category' in data:
        production_content.append(f"category: {data['category']}")
    
    # Write production file
    production_file = production_dir / f"{name}.yaml"
    with open(production_file, 'w') as f:
        f.write('\n'.join(production_content) + '\n')
    
    return production_file

def convert_hardware_file(source_file, production_dir):
    """Convert a hardware specification file to production format"""
    
    # Read source file  
    with open(source_file, 'r') as f:
        content = f.read()
    
    # Parse fields
    data = {}
    in_features = False
    features = []
    
    for line in content.split('\n'):
        if 'name:' in line and 'name' not in data:
            data['name'] = line.split(':', 1)[1].strip()
        elif 'category:' in line:
            data['category'] = line.split(':', 1)[1].strip()
        elif 'description:' in line:
            desc = line.split(':', 1)[1].strip().strip('"').strip('|')
            if desc and 'description' not in data:
                data['description'] = desc
        elif 'features:' in line:
            in_features = True
        elif in_features and line.strip().startswith('-'):
            features.append(line.strip()[1:].strip())
        elif not line.strip().startswith('-'):
            in_features = False
    
    # Generate production YAML
    name = source_file.stem.replace('hw_', '').replace('arch_', '')
    production_content = []
    
    production_content.append(f"component: {data.get('name', name)}")
    
    if 'category' in data:
        production_content.append(f"category: {data['category']}")
    
    if 'description' in data:
        production_content.append(f"description: |")
        production_content.append(f"  {data['description']}")
    
    if features:
        production_content.append("features:")
        for feature in features[:5]:  # Limit to top 5 features
            production_content.append(f"  - {feature}")
    
    # Write production file
    production_file = production_dir / f"{name}.yaml"
    with open(production_file, 'w') as f:
        f.write('\n'.join(production_content) + '\n')
    
    return production_file

def main():
    """Convert all source files to production format"""
    
    base_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2")
    
    # PASM2 instructions (already done, skip if exists)
    source_dir = base_dir / "production/_sources/instructions/pasm2"
    production_dir = base_dir / "production/instructions/pasm2"
    
    if source_dir.exists() and not (production_dir / "add.yaml").exists():
        print(f"Converting PASM2 instructions...")
        count = 0
        for source_file in source_dir.glob("pasm2_*.yaml"):
            convert_pasm2_instruction(source_file, production_dir)
            count += 1
            if count % 50 == 0:
                print(f"  Converted {count} files...")
        print(f"  Total: {count} PASM2 instructions converted")
    
    # Spin2 methods and operators
    spin2_source = base_dir / "production/_sources/language/spin2"
    
    if spin2_source.exists():
        # Methods
        method_count = 0
        for source_file in spin2_source.glob("spin2_*.yaml"):
            # Determine if method or operator based on content
            with open(source_file, 'r') as f:
                content = f.read()
            
            if 'method' in content.lower() or 'debug' in source_file.stem or 'string' in source_file.stem:
                target_dir = base_dir / "production/language/spin2/methods"
                target_dir.mkdir(parents=True, exist_ok=True)
                convert_spin2_file(source_file, target_dir, 'method')
                method_count += 1
            else:
                target_dir = base_dir / "production/language/spin2/operators"
                target_dir.mkdir(parents=True, exist_ok=True)
                convert_spin2_file(source_file, target_dir, 'operator')
        
        print(f"Converted {method_count} Spin2 methods")
        operator_count = len(list((base_dir / "production/language/spin2/operators").glob("*.yaml")))
        print(f"Converted {operator_count} Spin2 operators")
    
    # Hardware specifications
    hw_source = base_dir / "production/_sources/hardware"
    hw_production = base_dir / "production/hardware"
    hw_production.mkdir(parents=True, exist_ok=True)
    
    if hw_source.exists():
        hw_count = 0
        for source_file in hw_source.glob("hw_*.yaml"):
            convert_hardware_file(source_file, hw_production)
            hw_count += 1
        print(f"Converted {hw_count} hardware specifications")
    
    # Architecture components
    arch_source = base_dir / "production/_sources/architecture"
    arch_production = base_dir / "production/architecture"
    arch_production.mkdir(parents=True, exist_ok=True)
    
    if arch_source.exists():
        arch_count = 0
        for source_file in arch_source.glob("arch_*.yaml"):
            convert_hardware_file(source_file, arch_production)
            arch_count += 1
        print(f"Converted {arch_count} architecture components")
    
    print("\nProduction file generation complete!")
    print(f"Files created in: {base_dir}/production/")

if __name__ == "__main__":
    main()