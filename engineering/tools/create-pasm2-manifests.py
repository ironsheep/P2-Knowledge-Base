#!/usr/bin/env python3
"""
Create hierarchical PASM2 manifests with 100% instruction coverage
"""

import os
import yaml
from pathlib import Path
from collections import defaultdict
import json

def load_instruction_metadata(yaml_path):
    """Load basic metadata from an instruction YAML file."""
    try:
        with open(yaml_path, 'r') as f:
            content = yaml.safe_load(f)
            if content:
                return {
                    'group': content.get('group', ''),
                    'description': content.get('description', ''),
                    'syntax': content.get('syntax', ''),
                    'timing': content.get('timing', {})
                }
    except:
        pass
    return {}

def categorize_all_instructions():
    """Categorize ALL PASM2 instructions, ensuring 100% coverage."""
    base_path = Path("engineering/knowledge-base/P2/language/pasm2")
    
    # Categories with patterns - order matters (more specific first)
    categories = {
        'arithmetic': {
            'patterns': ['add', 'sub', 'mul', 'div', 'abs', 'neg', 'sum', 'sca', 'inc', 'dec', 'max', 'min', 'limit', 'fge', 'fle', 'fges', 'fles'],
            'instructions': [],
            'description': 'Arithmetic and math operations'
        },
        'logic': {
            'patterns': ['and', 'or', 'xor', 'not', 'test', 'cmp', 'mov', 'mux'],
            'instructions': [],
            'description': 'Logical and comparison operations'
        },
        'bit_manipulation': {
            'patterns': ['bit', 'shl', 'shr', 'rol', 'ror', 'sar', 'sal', 'rev', 'signx', 'zerox', 'rgbsqz', 'rgbexp', 'bmask', 'decod', 'encod', 'ones'],
            'instructions': [],
            'description': 'Bit manipulation and shifting'
        },
        'memory_hub': {
            'patterns': ['rd', 'wr', 'rf', 'wf', 'movbyts', 'setbyts', 'setbyte', 'getbyte', 'rolbyte'],
            'instructions': [],
            'description': 'Hub memory operations'
        },
        'memory_cog': {
            'patterns': ['sets', 'setd', 'getnib', 'setnib', 'getword', 'setword'],
            'instructions': [],
            'description': 'Cog/LUT memory operations'
        },
        'control_flow': {
            'patterns': ['jmp', 'call', 'ret', 'djnz', 'djz', 'tjz', 'tjnz', 'tjf', 'ijnz', 'ijz', 'rep', 'skip', 'execf'],
            'instructions': [],
            'description': 'Branches, jumps, and calls'
        },
        'pin_control': {
            'patterns': ['drv', 'flt', 'out', 'dir', 'wrpin', 'wxpin', 'wypin', 'rdpin', 'rqpin', 'akpin', 'pin', 'testp'],
            'instructions': [],
            'description': 'Digital pin and smart pin control'
        },
        'timing_events': {
            'patterns': ['wait', 'poll', 'getct', 'addct', 'cogatn', 'stalli', 'wai'],
            'instructions': [],
            'description': 'Timing, waiting, and events'
        },
        'cordic': {
            'patterns': ['qmul', 'qdiv', 'qfrac', 'qsqrt', 'qrotate', 'qvector', 'qlog', 'qexp', 'getq'],
            'instructions': [],
            'description': 'CORDIC math operations'
        },
        'streamer': {
            'patterns': ['xcont', 'xzero', 'xinit', 'xstop', 'setxfrq', 'getxacc'],
            'instructions': [],
            'description': 'Streamer operations'
        },
        'colorspace': {
            'patterns': ['setcy', 'setci', 'setcq', 'setcfrq', 'setcmod', 'blnpix', 'mixpix', 'addpix', 'mulpix'],
            'instructions': [],
            'description': 'Pixel and colorspace operations'
        },
        'interrupts': {
            'patterns': ['setint', 'allowi', 'stalli', 'trgint', 'nixint', 'reti', 'resi'],
            'instructions': [],
            'description': 'Interrupt configuration and handling'
        },
        'cog_control': {
            'patterns': ['cog', 'hub', 'lock', 'getbrk', 'cogbrk', 'brk', 'cogid', 'coginit', 'cogstop'],
            'instructions': [],
            'description': 'Cog and hub control'
        },
        'stack_ops': {
            'patterns': ['pop', 'push', 'call', 'ret'],
            'instructions': [],
            'description': 'Stack operations'
        },
        'special_ops': {
            'patterns': ['nop', 'debug', 'loc', 'aug', 'alt', 'set', 'get', 'modcz', 'modc', 'modz', 'decmod', 'lutson', 'splitb', 'mergeb', 'splitw', 'mergew', 'seussf', 'seussr'],
            'instructions': [],
            'description': 'Special operations and modifiers'
        },
        'misc_ops': {
            'patterns': [],  # Catch-all for uncategorized
            'instructions': [],
            'description': 'Miscellaneous operations'
        }
    }
    
    # Get all YAML files
    yaml_files = sorted(base_path.glob("*.yaml"))
    all_instructions = []
    
    for yaml_file in yaml_files:
        # Skip non-instruction files
        if yaml_file.stem in ['pattern-index', 'README', 'index']:
            continue
        all_instructions.append(yaml_file.stem)
    
    # Categorize each instruction
    for instruction in all_instructions:
        categorized = False
        
        # Try each category's patterns
        for cat_name, cat_data in categories.items():
            if cat_name == 'misc_ops':  # Skip misc for now
                continue
            for pattern in cat_data['patterns']:
                if (pattern in instruction.lower() or 
                    instruction.lower().startswith(pattern) or
                    (len(pattern) > 3 and instruction.lower().endswith(pattern))):
                    cat_data['instructions'].append(instruction)
                    categorized = True
                    break
            if categorized:
                break
        
        # If not categorized, put in misc_ops
        if not categorized:
            categories['misc_ops']['instructions'].append(instruction)
    
    # Print summary
    total = 0
    for cat_name, cat_data in categories.items():
        if cat_data['instructions']:
            print(f"{cat_name}: {len(cat_data['instructions'])} instructions")
            total += len(cat_data['instructions'])
    
    print(f"\nTotal instructions: {total}")
    print(f"Expected: {len(all_instructions)}")
    print(f"Coverage: {total}/{len(all_instructions)} = {(total/len(all_instructions)*100):.1f}%")
    
    if total != len(all_instructions):
        print("\nERROR: Not all instructions categorized!")
        # Find missing instructions
        categorized_set = set()
        for cat_data in categories.values():
            categorized_set.update(cat_data['instructions'])
        missing = set(all_instructions) - categorized_set
        if missing:
            print(f"Missing: {missing}")
    
    return categories, len(all_instructions)

def create_category_manifest(category_name, instructions, description, base_path="engineering/knowledge-base/P2/language/pasm2/"):
    """Create a category manifest file."""
    manifest = {
        'category': category_name,
        'description': description,
        'instruction_count': len(instructions),
        'base_path': base_path,
        'instructions': []
    }
    
    # Add each instruction with metadata
    for instr in sorted(instructions):
        yaml_path = Path(base_path) / f"{instr}.yaml"
        metadata = load_instruction_metadata(yaml_path)
        
        entry = {
            'name': instr,
            'file': f"{instr}.yaml"
        }
        
        # Add description if available
        desc = metadata.get('description', '')
        if desc:
            # Truncate long descriptions
            if len(desc) > 100:
                desc = desc[:97] + "..."
            entry['desc'] = desc.replace('\n', ' ').replace('\ufb01', 'fi').replace('\ufb02', 'fl')
        
        manifest['instructions'].append(entry)
    
    return manifest

def create_root_manifest(categories):
    """Create the root PASM2 manifest."""
    manifest = {
        'version': "2.0",
        'schema_version': "2024-12-30",
        'last_updated': "2025-09-23T00:00:00Z",
        'category': "pasm2_instructions",
        'structure': "hierarchical",
        'total_instructions': sum(len(cat['instructions']) for cat in categories.values()),
        'description': "Complete PASM2 instruction set with hierarchical organization for efficient discovery",
        
        'categories': {}
    }
    
    for cat_name, cat_data in categories.items():
        if cat_data['instructions']:
            manifest['categories'][cat_name] = {
                'manifest': f"pasm2/{cat_name}.yaml",
                'count': len(cat_data['instructions']),
                'description': cat_data['description'],
                'sample_instructions': sorted(cat_data['instructions'])[:5]
            }
    
    # Add quick lookup for common instructions
    manifest['quick_lookup'] = {
        'common_instructions': {
            'ADD': 'arithmetic',
            'SUB': 'arithmetic', 
            'MOV': 'logic',
            'JMP': 'control_flow',
            'CALL': 'control_flow',
            'RET': 'control_flow',
            'RDLONG': 'memory_hub',
            'WRLONG': 'memory_hub',
            'WAITX': 'timing_events',
            'REP': 'control_flow'
        }
    }
    
    return manifest

def main():
    """Create all manifests."""
    print("Analyzing PASM2 instructions...")
    categories, total = categorize_all_instructions()
    
    if sum(len(cat['instructions']) for cat in categories.values()) != total:
        print("\nERROR: Not all instructions accounted for. Aborting.")
        return
    
    print("\nCreating manifest structure...")
    
    # Create manifests directory
    manifest_dir = Path("manifests/pasm2")
    manifest_dir.mkdir(exist_ok=True)
    
    # Create category manifests
    for cat_name, cat_data in categories.items():
        if cat_data['instructions']:
            manifest = create_category_manifest(
                cat_name, 
                cat_data['instructions'],
                cat_data['description']
            )
            
            output_path = manifest_dir / f"{cat_name}.yaml"
            with open(output_path, 'w') as f:
                yaml.dump(manifest, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            print(f"Created {output_path}")
    
    # Create root manifest
    root_manifest = create_root_manifest(categories)
    root_path = Path("manifests/pasm2-manifest.yaml")
    
    # Save backup of old manifest
    if root_path.exists():
        backup_path = Path("manifests/pasm2-manifest.yaml.backup")
        os.rename(root_path, backup_path)
        print(f"Backed up old manifest to {backup_path}")
    
    with open(root_path, 'w') as f:
        yaml.dump(root_manifest, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print(f"Created {root_path}")
    
    print(f"\n✅ Successfully created hierarchical manifest structure")
    print(f"   Root manifest + {len([c for c in categories.values() if c['instructions']])} category manifests")
    print(f"   Total instructions covered: {total}")

if __name__ == "__main__":
    main()