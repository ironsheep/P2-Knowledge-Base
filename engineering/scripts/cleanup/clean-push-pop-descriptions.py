#!/usr/bin/env python3
"""
Clean up PUSHA/PUSHB/POPA/POPB descriptions while preserving compiler data.
Only fix the garbled description text, don't overwrite good compiler data.
"""

import yaml
from pathlib import Path

PASM2_PATH = Path("engineering/knowledge-base/P2/language/pasm2")

# Define clean descriptions based on the manual entries
clean_descriptions = {
    'pusha': {
        'description': 'Write long in D[31:0] to hub address PTRA++.',
        'brief_description': 'Push long to stack using PTRA',
        'parameters': [
            'D is a register or 9-bit literal value to push onto the stack at PTRA',
            'PTRA is automatically incremented after the write'
        ]
    },
    'pushb': {
        'description': 'Write long in D[31:0] to hub address PTRB++.',
        'brief_description': 'Push long to stack using PTRB', 
        'parameters': [
            'D is a register or 9-bit literal value to push onto the stack at PTRB',
            'PTRB is automatically incremented after the write'
        ]
    },
    'popa': {
        'description': 'Read long from hub address --PTRA into D.',
        'brief_description': 'Pop long from stack using PTRA',
        'parameters': [
            'D is the destination register to receive the popped value',
            'PTRA is automatically decremented before the read'
        ],
        'flags_affected': {
            'C': {
                'formula': 'MSB of long',
                'description': 'Set to bit 31 of the popped value'
            },
            'Z': {
                'formula': 'Result = 0',
                'description': 'Set if popped value is zero'
            }
        }
    },
    'popb': {
        'description': 'Read long from hub address --PTRB into D.',
        'brief_description': 'Pop long from stack using PTRB',
        'parameters': [
            'D is the destination register to receive the popped value',
            'PTRB is automatically decremented before the read'
        ],
        'flags_affected': {
            'C': {
                'formula': 'MSB of long',
                'description': 'Set to bit 31 of the popped value'
            },
            'Z': {
                'formula': 'Result = 0', 
                'description': 'Set if popped value is zero'
            }
        }
    }
}

# Update each file
for inst_name, updates in clean_descriptions.items():
    yaml_path = PASM2_PATH / f"{inst_name}.yaml"
    
    print(f"Cleaning {inst_name.upper()}...")
    
    # Load existing
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f) or {}
    
    # Update ONLY the description fields, preserve everything else
    for field, value in updates.items():
        data[field] = value
    
    # Mark as cleaned up
    data['documentation_level'] = 'enhanced'
    data['last_updated'] = '2025-01-19'
    
    # Write back
    with open(yaml_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, width=100)
    
    print(f"  ✓ Cleaned description")
    print(f"  ✓ Preserved compiler data")

print("\nDone! Push/pop instructions now have clean descriptions while preserving all compiler data.")