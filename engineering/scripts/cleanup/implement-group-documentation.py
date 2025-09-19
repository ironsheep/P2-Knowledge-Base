#!/usr/bin/env python3
"""
Implement two-tier documentation for PASM2 grouped instructions.
Creates group documentation files and updates individual YAMLs with group references.
"""

import yaml
import re
from pathlib import Path
from datetime import datetime

# Base paths
YAML_DIR = Path('/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/pasm2')
GROUPS_DIR = YAML_DIR / 'groups'
MANUAL_PATH = Path('/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/pasm2-manual/pasm2-manual-narrative.txt')

# Group definitions with their documentation locations
INSTRUCTION_GROUPS = {
    'counter_event_jumps': {
        'title': 'Counter Event Jump Instructions',
        'members': {
            'jct1': {'desc': 'Jump if counter 1 event flag is set', 'counter': 1, 'condition': 'set'},
            'jct2': {'desc': 'Jump if counter 2 event flag is set', 'counter': 2, 'condition': 'set'},
            'jct3': {'desc': 'Jump if counter 3 event flag is set', 'counter': 3, 'condition': 'set'},
            'jnct1': {'desc': 'Jump if counter 1 event flag is NOT set', 'counter': 1, 'condition': 'not set'},
            'jnct2': {'desc': 'Jump if counter 2 event flag is NOT set', 'counter': 2, 'condition': 'not set'},
            'jnct3': {'desc': 'Jump if counter 3 event flag is NOT set', 'counter': 3, 'condition': 'not set'}
        },
        'manual_section': (4850, 4900),
        'related': ['ADDCT1', 'ADDCT2', 'ADDCT3', 'POLLCT1', 'POLLCT2', 'POLLCT3', 'WAITCT1', 'WAITCT2', 'WAITCT3']
    },
    'counter_event_waits': {
        'title': 'Counter Event Wait Instructions',
        'members': {
            'waitct1': {'desc': 'Wait for counter 1 event flag, then clear it', 'counter': 1},
            'waitct2': {'desc': 'Wait for counter 2 event flag, then clear it', 'counter': 2},
            'waitct3': {'desc': 'Wait for counter 3 event flag, then clear it', 'counter': 3}
        },
        'related': ['ADDCT1', 'ADDCT2', 'ADDCT3', 'POLLCT1', 'POLLCT2', 'POLLCT3']
    },
    'counter_event_polls': {
        'title': 'Counter Event Poll Instructions',
        'members': {
            'pollct1': {'desc': 'Check if counter 1 event flag is set', 'counter': 1},
            'pollct2': {'desc': 'Check if counter 2 event flag is set', 'counter': 2},
            'pollct3': {'desc': 'Check if counter 3 event flag is set', 'counter': 3}
        },
        'related': ['ADDCT1', 'ADDCT2', 'ADDCT3', 'WAITCT1', 'WAITCT2', 'WAITCT3']
    },
    'selector_event_jumps': {
        'title': 'Selector Event Jump Instructions',
        'members': {
            'jse1': {'desc': 'Jump if selector 1 event flag is set', 'selector': 1, 'condition': 'set'},
            'jse2': {'desc': 'Jump if selector 2 event flag is set', 'selector': 2, 'condition': 'set'},
            'jse3': {'desc': 'Jump if selector 3 event flag is set', 'selector': 3, 'condition': 'set'},
            'jse4': {'desc': 'Jump if selector 4 event flag is set', 'selector': 4, 'condition': 'set'},
            'jnse1': {'desc': 'Jump if selector 1 event flag is NOT set', 'selector': 1, 'condition': 'not set'},
            'jnse2': {'desc': 'Jump if selector 2 event flag is NOT set', 'selector': 2, 'condition': 'not set'},
            'jnse3': {'desc': 'Jump if selector 3 event flag is NOT set', 'selector': 3, 'condition': 'not set'},
            'jnse4': {'desc': 'Jump if selector 4 event flag is NOT set', 'selector': 4, 'condition': 'not set'}
        },
        'related': ['SETSE1', 'SETSE2', 'SETSE3', 'SETSE4', 'POLLSE1', 'POLLSE2', 'POLLSE3', 'POLLSE4']
    },
    'selector_event_waits': {
        'title': 'Selector Event Wait Instructions',
        'members': {
            'waitse1': {'desc': 'Wait for selector 1 event flag, then clear it', 'selector': 1},
            'waitse2': {'desc': 'Wait for selector 2 event flag, then clear it', 'selector': 2},
            'waitse3': {'desc': 'Wait for selector 3 event flag, then clear it', 'selector': 3},
            'waitse4': {'desc': 'Wait for selector 4 event flag, then clear it', 'selector': 4}
        },
        'related': ['SETSE1', 'SETSE2', 'SETSE3', 'SETSE4', 'POLLSE1', 'POLLSE2', 'POLLSE3', 'POLLSE4']
    },
    'interrupt_resume': {
        'title': 'Interrupt Resume Instructions',
        'members': {
            'resi0': {'desc': 'Resume from interrupt 0', 'interrupt': 0},
            'resi1': {'desc': 'Resume from interrupt 1', 'interrupt': 1},
            'resi2': {'desc': 'Resume from interrupt 2', 'interrupt': 2},
            'resi3': {'desc': 'Resume from interrupt 3', 'interrupt': 3}
        },
        'related': ['RETI0', 'RETI1', 'RETI2', 'RETI3', 'SETINT1', 'SETINT2', 'SETINT3']
    },
    'interrupt_return': {
        'title': 'Interrupt Return Instructions',
        'members': {
            'reti0': {'desc': 'Return from interrupt 0', 'interrupt': 0},
            'reti1': {'desc': 'Return from interrupt 1', 'interrupt': 1},
            'reti2': {'desc': 'Return from interrupt 2', 'interrupt': 2},
            'reti3': {'desc': 'Return from interrupt 3', 'interrupt': 3}
        },
        'related': ['RESI0', 'RESI1', 'RESI2', 'RESI3', 'SETINT1', 'SETINT2', 'SETINT3']
    }
}

def extract_group_documentation(group_id, group_info):
    """Extract comprehensive documentation for a group from the manual."""
    with open(MANUAL_PATH, 'r') as f:
        lines = f.readlines()
    
    doc = {
        'explanation': '',
        'timing_details': '',
        'addressing': '',
        'examples': []
    }
    
    # If manual section is specified, extract from there
    if 'manual_section' in group_info:
        start, end = group_info['manual_section']
        section = ''.join(lines[start:end])
        
        # Extract explanation
        exp_match = re.search(r'Explanation:(.*?)(?=\n[A-Z]{2,}|\Z)', section, re.DOTALL)
        if exp_match:
            doc['explanation'] = exp_match.group(1).strip()
        
        # Extract timing information
        timing_match = re.search(r'(\d+(?:\s+or\s+\d+)?(?:\s*/\s*\d+(?:\.\.\.\d+)?)?)', section)
        if timing_match:
            doc['timing_details'] = f"Timing: {timing_match.group(1)}"
        
        # Look for addressing information
        if 'relative' in section or 'absolute' in section:
            addr_match = re.search(r'(The address.*?(?:\.|$))', section, re.DOTALL)
            if addr_match:
                doc['addressing'] = addr_match.group(1).strip()
    
    return doc

def create_group_file(group_id, group_info):
    """Create a group documentation YAML file."""
    
    # Extract documentation from manual
    group_doc = extract_group_documentation(group_id, group_info)
    
    # Build the group YAML structure
    group_yaml = {
        'group_id': group_id,
        'title': group_info['title'],
        'members': {},
        'shared_documentation': {
            'explanation': group_doc['explanation'] or f"These instructions are part of the {group_info['title']} family.",
            'timing_details': group_doc['timing_details'] or "See individual instructions for specific timing.",
            'addressing': group_doc['addressing'] if group_doc['addressing'] else None
        },
        'related_instructions': group_info.get('related', []),
        'examples': [],
        'created': datetime.now().isoformat(),
        'source': 'PASM2 Manual 2022-11-01'
    }
    
    # Add member details
    for instr, details in group_info['members'].items():
        group_yaml['members'][instr.upper()] = details['desc']
    
    # Add example patterns
    if 'counter' in group_id:
        group_yaml['examples'].append({
            'title': 'Basic counter timeout pattern',
            'code': 'ADDCT1  ##1_000_000\n; ... do work ...\nJCT1    #timeout_handler'
        })
    elif 'interrupt' in group_id:
        group_yaml['examples'].append({
            'title': 'Interrupt handler pattern',
            'code': 'INT0_handler:\n    ; save state\n    ; handle interrupt\n    RESI0  ; or RETI0 to return'
        })
    
    # Save the group file
    group_path = GROUPS_DIR / f"{group_id}.yaml"
    with open(group_path, 'w') as f:
        yaml.dump(group_yaml, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    return group_path

def update_individual_yaml(instr, group_id, member_info):
    """Update an individual instruction YAML with group reference."""
    yaml_path = YAML_DIR / f"{instr}.yaml"
    
    if not yaml_path.exists():
        print(f"  ⚠️  {instr}.yaml not found")
        return False
    
    # Load existing YAML
    with open(yaml_path, 'r') as f:
        yaml_data = yaml.safe_load(f) or {}
    
    # Add/update brief description
    yaml_data['brief_description'] = member_info['desc']
    
    # Add group membership
    yaml_data['group_membership'] = {
        'group_id': group_id,
        'group_file': f"groups/{group_id}.yaml",
        'related': [m for m in INSTRUCTION_GROUPS[group_id]['members'].keys() if m != instr]
    }
    
    # Add instruction-specific details
    yaml_data['specifics'] = {}
    if 'counter' in member_info:
        yaml_data['specifics']['counter_number'] = member_info['counter']
        yaml_data['specifics']['event_flag'] = f"CT{member_info['counter']}"
    if 'selector' in member_info:
        yaml_data['specifics']['selector_number'] = member_info['selector']
        yaml_data['specifics']['event_flag'] = f"SE{member_info['selector']}"
    if 'interrupt' in member_info:
        yaml_data['specifics']['interrupt_number'] = member_info['interrupt']
    if 'condition' in member_info:
        yaml_data['specifics']['condition'] = member_info['condition']
    
    # Add a quick example if not present
    if 'examples' not in yaml_data or not yaml_data['examples']:
        if 'jump' in member_info['desc'].lower():
            yaml_data['quick_example'] = f"{instr.upper()} #handler  ; {member_info['desc']}"
        elif 'wait' in member_info['desc'].lower():
            yaml_data['quick_example'] = f"{instr.upper()}  ; {member_info['desc']}"
    
    # Update documentation metadata
    yaml_data['documentation_level'] = 'structured'
    yaml_data['has_group_documentation'] = True
    yaml_data['last_updated'] = datetime.now().isoformat()
    
    # Save updated YAML
    with open(yaml_path, 'w') as f:
        yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    return True

def main():
    print("=" * 60)
    print("Implementing Two-Tier Group Documentation")
    print("=" * 60)
    
    stats = {
        'groups_created': 0,
        'instructions_updated': 0,
        'instructions_not_found': 0
    }
    
    print("\nPhase 1: Creating group documentation files...\n")
    
    for group_id, group_info in INSTRUCTION_GROUPS.items():
        print(f"Creating group: {group_id}")
        group_path = create_group_file(group_id, group_info)
        print(f"  ✅ Created: {group_path.name}")
        stats['groups_created'] += 1
    
    print("\nPhase 2: Updating individual instruction YAMLs...\n")
    
    for group_id, group_info in INSTRUCTION_GROUPS.items():
        print(f"\nProcessing group: {group_id}")
        for instr, member_info in group_info['members'].items():
            if update_individual_yaml(instr, group_id, member_info):
                print(f"  ✅ Updated: {instr}.yaml")
                stats['instructions_updated'] += 1
            else:
                stats['instructions_not_found'] += 1
    
    # Create implementation report
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Groups created: {stats['groups_created']}")
    print(f"Instructions updated: {stats['instructions_updated']}")
    print(f"Instructions not found: {stats['instructions_not_found']}")
    
    # Save report
    report_path = YAML_DIR / 'group-implementation-report.md'
    with open(report_path, 'w') as f:
        f.write(f"# Group Documentation Implementation Report\n\n")
        f.write(f"Date: {datetime.now().isoformat()}\n\n")
        f.write(f"## Statistics\n")
        f.write(f"- Groups created: {stats['groups_created']}\n")
        f.write(f"- Instructions updated: {stats['instructions_updated']}\n")
        f.write(f"- Success rate: {stats['instructions_updated']/(stats['instructions_updated']+stats['instructions_not_found'])*100:.1f}%\n\n")
        f.write(f"## Groups Created\n")
        for group_id in INSTRUCTION_GROUPS.keys():
            f.write(f"- `groups/{group_id}.yaml`\n")
        f.write(f"\n## Two-Tier Structure\n")
        f.write(f"1. Individual YAMLs contain essential info + group reference\n")
        f.write(f"2. Group files contain comprehensive shared documentation\n")
        f.write(f"3. One extra fetch provides complete understanding of instruction family\n")
    
    print(f"\n✅ Implementation complete!")
    print(f"📁 Group files created in: {GROUPS_DIR}")
    print(f"📄 Report saved to: {report_path.name}")

if __name__ == "__main__":
    main()