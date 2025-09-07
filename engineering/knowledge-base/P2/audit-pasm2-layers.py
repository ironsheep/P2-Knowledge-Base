#!/usr/bin/env python3
"""Audit PASM2 instruction files for layer completeness."""

import os
import yaml
from pathlib import Path
from collections import defaultdict

def audit_pasm2_files():
    """Audit all PASM2 instruction files for layer completeness."""
    
    pasm2_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/instructions/pasm2")
    
    stats = {
        'total_files': 0,
        'empty_files': 0,
        'layer1_only': 0,
        'layer1_2': 0,
        'layer1_2_3': 0,
        'layer1_2_3_4': 0,
        'missing_layer1': 0
    }
    
    layer_coverage = defaultdict(int)
    instruction_audit = {}
    
    for yaml_file in sorted(pasm2_dir.glob("pasm2_*.yaml")):
        stats['total_files'] += 1
        
        try:
            with open(yaml_file, 'r') as f:
                data = yaml.safe_load(f)
                
            if not data:
                stats['empty_files'] += 1
                continue
                
            # Extract mnemonic from layer1 if present
            mnemonic = None
            if 'layer1_csv' in data and 'mnemonic' in data['layer1_csv']:
                mnemonic = data['layer1_csv']['mnemonic']
            
            # Check which layers are present
            layers_present = []
            if 'layer1_csv' in data and data['layer1_csv']:
                layers_present.append(1)
                layer_coverage['layer1'] += 1
            if 'layer2_datasheet' in data and data['layer2_datasheet']:
                layers_present.append(2)
                layer_coverage['layer2'] += 1
            if 'layer3_silicon_doc' in data and data['layer3_silicon_doc']:
                layers_present.append(3)
                layer_coverage['layer3'] += 1
            if 'layer4_chip_clarifications' in data and data['layer4_chip_clarifications']:
                layers_present.append(4)
                layer_coverage['layer4'] += 1
            
            # Categorize completeness
            if not layers_present:
                stats['empty_files'] += 1
            elif 1 not in layers_present:
                stats['missing_layer1'] += 1
            elif layers_present == [1]:
                stats['layer1_only'] += 1
            elif layers_present == [1, 2]:
                stats['layer1_2'] += 1
            elif layers_present == [1, 2, 3]:
                stats['layer1_2_3'] += 1
            elif layers_present == [1, 2, 3, 4]:
                stats['layer1_2_3_4'] += 1
            
            instruction_audit[yaml_file.name] = {
                'mnemonic': mnemonic,
                'layers': layers_present,
                'file_size': yaml_file.stat().st_size
            }
            
        except Exception as e:
            print(f"Error reading {yaml_file.name}: {e}")
            stats['empty_files'] += 1
    
    # Print audit report
    print("=" * 70)
    print("PASM2 INSTRUCTION AUDIT REPORT")
    print("=" * 70)
    print(f"\nTotal Files: {stats['total_files']}")
    print(f"Expected: 491 instructions")
    print(f"Coverage: {stats['total_files']}/491 = {stats['total_files']/491*100:.1f}%")
    
    print("\n--- Layer Completeness ---")
    print(f"Empty files: {stats['empty_files']}")
    print(f"Missing Layer 1 (CSV base): {stats['missing_layer1']}")
    print(f"Layer 1 only: {stats['layer1_only']}")
    print(f"Layers 1-2: {stats['layer1_2']}")
    print(f"Layers 1-2-3: {stats['layer1_2_3']}")
    print(f"Layers 1-2-3-4 (complete): {stats['layer1_2_3_4']}")
    
    print("\n--- Layer Coverage ---")
    print(f"Layer 1 (CSV): {layer_coverage['layer1']}/{stats['total_files']} = {layer_coverage['layer1']/stats['total_files']*100:.1f}%")
    print(f"Layer 2 (Datasheet): {layer_coverage['layer2']}/{stats['total_files']} = {layer_coverage['layer2']/stats['total_files']*100:.1f}%")
    print(f"Layer 3 (Silicon Doc): {layer_coverage['layer3']}/{stats['total_files']} = {layer_coverage['layer3']/stats['total_files']*100:.1f}%")
    print(f"Layer 4 (Chip Clarifications): {layer_coverage['layer4']}/{stats['total_files']} = {layer_coverage['layer4']/stats['total_files']*100:.1f}%")
    
    # Find examples of each category
    print("\n--- Sample Files by Completeness ---")
    for filename, info in sorted(instruction_audit.items())[:5]:
        if info['layers'] == [1, 2, 3]:
            print(f"Layers 1-2-3: {filename} ({info['mnemonic']})")
            break
    
    for filename, info in sorted(instruction_audit.items())[:5]:
        if info['layers'] == [1, 2]:
            print(f"Layers 1-2: {filename} ({info['mnemonic']})")
            break
            
    for filename, info in sorted(instruction_audit.items())[:5]:
        if info['layers'] == [1]:
            print(f"Layer 1 only: {filename} ({info['mnemonic']})")
            break
    
    # Check naming convention
    print("\n--- File Naming Convention ---")
    hash_pattern_count = sum(1 for f in instruction_audit.keys() if '_' in f and len(f.split('_')[-1].split('.')[0]) == 8)
    print(f"Files with hash suffix: {hash_pattern_count}/{stats['total_files']}")
    print("Recommendation: Remove hash suffixes for cleaner naming")
    
    return stats, instruction_audit

if __name__ == "__main__":
    audit_pasm2_files()