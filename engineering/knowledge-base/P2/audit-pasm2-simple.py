#!/usr/bin/env python3
"""Simple audit of PASM2 files checking for layer keywords."""

import os
from pathlib import Path

def audit_pasm2_files():
    """Audit all PASM2 instruction files for layer completeness."""
    
    pasm2_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/instructions/pasm2")
    
    stats = {
        'total_files': 0,
        'has_layer1': 0,
        'has_layer2': 0,
        'has_layer3': 0,
        'has_layer4': 0,
        'all_layers': 0
    }
    
    completeness_samples = {
        'layer1_only': [],
        'layer1_2': [],
        'layer1_2_3': [],
        'complete': []
    }
    
    for yaml_file in sorted(pasm2_dir.glob("pasm2_*.yaml")):
        stats['total_files'] += 1
        
        with open(yaml_file, 'r') as f:
            content = f.read()
            
        # Check for layer presence
        has_l1 = 'layer1_csv:' in content
        has_l2 = 'layer2_datasheet:' in content  
        has_l3 = 'layer3_silicon_doc:' in content
        has_l4 = 'layer4_chip_clarifications:' in content
        
        if has_l1:
            stats['has_layer1'] += 1
        if has_l2:
            stats['has_layer2'] += 1
        if has_l3:
            stats['has_layer3'] += 1
        if has_l4:
            stats['has_layer4'] += 1
            
        # Categorize completeness
        if has_l1 and has_l2 and has_l3 and has_l4:
            stats['all_layers'] += 1
            if len(completeness_samples['complete']) < 3:
                completeness_samples['complete'].append(yaml_file.name)
        elif has_l1 and has_l2 and has_l3:
            if len(completeness_samples['layer1_2_3']) < 3:
                completeness_samples['layer1_2_3'].append(yaml_file.name)
        elif has_l1 and has_l2:
            if len(completeness_samples['layer1_2']) < 3:
                completeness_samples['layer1_2'].append(yaml_file.name)
        elif has_l1:
            if len(completeness_samples['layer1_only']) < 3:
                completeness_samples['layer1_only'].append(yaml_file.name)
    
    # Print audit report
    print("=" * 70)
    print("PASM2 INSTRUCTION AUDIT REPORT")
    print("=" * 70)
    print(f"\nTotal Files: {stats['total_files']}")
    print(f"Expected: 491 instructions")
    print(f"Coverage: {stats['total_files']}/491 = {stats['total_files']/491*100:.1f}%")
    
    print("\n--- Layer Coverage ---")
    print(f"Layer 1 (CSV): {stats['has_layer1']}/{stats['total_files']} = {stats['has_layer1']/stats['total_files']*100:.1f}%")
    print(f"Layer 2 (Datasheet): {stats['has_layer2']}/{stats['total_files']} = {stats['has_layer2']/stats['total_files']*100:.1f}%")
    print(f"Layer 3 (Silicon Doc): {stats['has_layer3']}/{stats['total_files']} = {stats['has_layer3']/stats['total_files']*100:.1f}%")
    print(f"Layer 4 (Chip Clarifications): {stats['has_layer4']}/{stats['total_files']} = {stats['has_layer4']/stats['total_files']*100:.1f}%")
    print(f"\nFully Complete (all 4 layers): {stats['all_layers']}/{stats['total_files']} = {stats['all_layers']/stats['total_files']*100:.1f}%")
    
    print("\n--- Sample Files by Completeness ---")
    print(f"Layer 1 only: {completeness_samples['layer1_only'][:2]}")
    print(f"Layers 1-2: {completeness_samples['layer1_2'][:2]}")
    print(f"Layers 1-2-3: {completeness_samples['layer1_2_3'][:2]}")
    print(f"Complete (all 4): {completeness_samples['complete'][:2]}")
    
    # File naming check
    print("\n--- File Naming Convention ---")
    hash_files = [f for f in os.listdir(pasm2_dir) if f.startswith('pasm2_') and len(f.split('_')[-1].split('.')[0]) == 8]
    print(f"Files with 8-char hash suffix: {len(hash_files)}/{stats['total_files']}")
    print("All files have hash suffixes - should be removed for cleaner naming")
    
    return stats

if __name__ == "__main__":
    audit_pasm2_files()