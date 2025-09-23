#!/usr/bin/env python3
"""
Analyze PASM2 instructions and categorize them for hierarchical manifest creation
"""

import os
import yaml
from pathlib import Path
from collections import defaultdict

def categorize_instructions():
    base_path = Path("engineering/knowledge-base/P2/language/pasm2")
    
    # Categories based on instruction patterns and functionality
    categories = {
        'arithmetic': {
            'patterns': ['add', 'sub', 'mul', 'div', 'abs', 'neg', 'sum', 'sca', 'inc', 'dec', 'fge', 'fle', 'fges', 'fles'],
            'instructions': []
        },
        'logic': {
            'patterns': ['and', 'or', 'xor', 'not', 'test', 'cmp', 'mov'],
            'instructions': []
        },
        'bit_ops': {
            'patterns': ['bit', 'shl', 'shr', 'rol', 'ror', 'sar', 'sal', 'rev', 'rgbsqz', 'rgbexp'],
            'instructions': []
        },
        'memory': {
            'patterns': ['rd', 'wr', 'rfast', 'wfast', 'rfbyte', 'wfbyte', 'rfword', 'wfword', 'rflong', 'wflong', 'movbyts', 'setbyts'],
            'instructions': []
        },
        'control_flow': {
            'patterns': ['jmp', 'call', 'ret', 'djnz', 'djz', 'tjz', 'tjnz', 'tjf', 'ijnz', 'ijz', 'rep', 'skip'],
            'instructions': []
        },
        'pin_io': {
            'patterns': ['drv', 'flt', 'out', 'dir', 'wrpin', 'wxpin', 'wypin', 'rdpin', 'rqpin', 'akpin', 'pin'],
            'instructions': []
        },
        'timing': {
            'patterns': ['wait', 'poll', 'getct', 'addct', 'cogatn', 'stalli'],
            'instructions': []
        },
        'cordic': {
            'patterns': ['q', 'getq', 'setq', 'cordic'],
            'instructions': []
        },
        'streamer': {
            'patterns': ['xcont', 'xzero', 'xinit', 'xstop', 'setcmod', 'setcy', 'setci', 'setcq', 'setcfrq', 'setcy'],
            'instructions': []
        },
        'interrupts': {
            'patterns': ['setint', 'allowi', 'stalli', 'trgint', 'nixint', 'reti', 'resi'],
            'instructions': []
        },
        'hub_ctrl': {
            'patterns': ['cog', 'hub', 'lock', 'getbrk', 'setbrk', 'brk', 'pop', 'push'],
            'instructions': []
        },
        'special': {
            'patterns': ['nop', 'debug', 'loc', 'aug', 'alt', 'set', 'get', 'lutson', 'modcz', 'modc', 'modz', 'decmod', 'encod', 'decod', 'bmask', 'ones', 'mux'],
            'instructions': []
        }
    }
    
    # Get all YAML files
    yaml_files = sorted(base_path.glob("*.yaml"))
    uncategorized = []
    
    for yaml_file in yaml_files:
        name = yaml_file.stem
        categorized = False
        
        # Try to categorize by pattern
        for cat_name, cat_data in categories.items():
            for pattern in cat_data['patterns']:
                if pattern in name.lower() or name.lower().startswith(pattern):
                    cat_data['instructions'].append(name)
                    categorized = True
                    break
            if categorized:
                break
        
        if not categorized:
            # Try to read the file and check its group/category
            try:
                with open(yaml_file, 'r') as f:
                    content = yaml.safe_load(f)
                    if content and 'group' in content:
                        group = content['group'].lower()
                        if 'math' in group or 'arithmetic' in group:
                            categories['arithmetic']['instructions'].append(name)
                        elif 'logic' in group:
                            categories['logic']['instructions'].append(name)
                        elif 'memory' in group:
                            categories['memory']['instructions'].append(name)
                        elif 'branch' in group or 'jump' in group:
                            categories['control_flow']['instructions'].append(name)
                        elif 'pin' in group or 'i/o' in group:
                            categories['pin_io']['instructions'].append(name)
                        else:
                            uncategorized.append(name)
                    else:
                        uncategorized.append(name)
            except:
                uncategorized.append(name)
    
    # Print results
    total = 0
    for cat_name, cat_data in categories.items():
        if cat_data['instructions']:
            print(f"\n{cat_name.upper()} ({len(cat_data['instructions'])} instructions):")
            print(f"  {', '.join(sorted(cat_data['instructions'])[:10])}")
            if len(cat_data['instructions']) > 10:
                print(f"  ... and {len(cat_data['instructions']) - 10} more")
            total += len(cat_data['instructions'])
    
    if uncategorized:
        print(f"\nUNCATEGORIZED ({len(uncategorized)} instructions):")
        print(f"  {', '.join(uncategorized[:20])}")
        if len(uncategorized) > 20:
            print(f"  ... and {len(uncategorized) - 20} more")
    
    print(f"\nTOTAL CATEGORIZED: {total}")
    print(f"TOTAL FILES: {len(yaml_files)}")
    
    return categories, uncategorized

if __name__ == "__main__":
    categorize_instructions()