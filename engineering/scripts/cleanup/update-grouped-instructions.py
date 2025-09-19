#!/usr/bin/env python3
"""
Update PASM2 YAML files for grouped instructions from the manual.
Handles cases like "JCT1/2/3 / JNCT1/2/3" where one narrative covers multiple instructions.
"""

import yaml
import re
from pathlib import Path
import shutil
from datetime import datetime

# Base paths
YAML_DIR = Path('/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/pasm2')
MANUAL_PATH = Path('/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/pasm2-manual/pasm2-manual-narrative.txt')

# Grouped instructions patterns found in the manual
GROUPED_INSTRUCTIONS = {
    'JCT1/2/3 / JNCT1/2/3': {
        'instructions': ['jct1', 'jct2', 'jct3', 'jnct1', 'jnct2', 'jnct3'],
        'start_line': 4850,
        'end_line': 4900
    },
    'WAITCT1/2/3': {
        'instructions': ['waitct1', 'waitct2', 'waitct3'],
        'pattern': r'WAITCT[123]'
    },
    'WAITSE1/2/3/4': {
        'instructions': ['waitse1', 'waitse2', 'waitse3', 'waitse4'],
        'pattern': r'WAITSE[1234]'
    },
    'POLLCT1/2/3': {
        'instructions': ['pollct1', 'pollct2', 'pollct3'],
        'pattern': r'POLLCT[123]'
    },
    'POLLSE1/2/3/4': {
        'instructions': ['pollse1', 'pollse2', 'pollse3', 'pollse4'],
        'pattern': r'POLLSE[1234]'
    },
    'SETSE1/2/3/4': {
        'instructions': ['setse1', 'setse2', 'setse3', 'setse4'],
        'pattern': r'SETSE[1234]'
    },
    'ADDCT1/2/3': {
        'instructions': ['addct1', 'addct2', 'addct3'],
        'pattern': r'ADDCT[123]'
    },
    'SETINT1/2/3': {
        'instructions': ['setint1', 'setint2', 'setint3'],
        'pattern': r'SETINT[123]'
    },
    'TRGINT1/2/3': {
        'instructions': ['trgint1', 'trgint2', 'trgint3'],
        'pattern': r'TRGINT[123]'
    },
    'NIXINT1/2/3': {
        'instructions': ['nixint1', 'nixint2', 'nixint3'],
        'pattern': r'NIXINT[123]'
    },
    'RESI0/1/2/3': {
        'instructions': ['resi0', 'resi1', 'resi2', 'resi3'],
        'pattern': r'RESI[0123]'
    },
    'RETI0/1/2/3': {
        'instructions': ['reti0', 'reti1', 'reti2', 'reti3'],
        'pattern': r'RETI[0123]'
    },
    'JSE1/2/3/4 / JNSE1/2/3/4': {
        'instructions': ['jse1', 'jse2', 'jse3', 'jse4', 'jnse1', 'jnse2', 'jnse3', 'jnse4'],
        'pattern': r'J(?:N)?SE[1234]'
    }
}

class GroupedManualParser:
    def __init__(self):
        with open(MANUAL_PATH, 'r') as f:
            self.lines = f.readlines()
    
    def find_grouped_documentation(self, group_name, group_info):
        """Extract documentation for a group of related instructions."""
        
        # Look for the group header
        results = {}
        
        # Search for the group pattern in the manual
        for i, line in enumerate(self.lines):
            if group_name in line or (group_info.get('pattern') and re.search(group_info['pattern'], line)):
                # Found a potential match, extract the section
                start = i
                end = min(i + 200, len(self.lines))  # Look ahead up to 200 lines
                
                # Extract the documentation section
                section_lines = []
                syntax_lines = []
                in_syntax = False
                result_text = ''
                description_text = ''
                timing_info = ''
                
                for j in range(start, end):
                    current_line = self.lines[j]
                    
                    # Capture syntax patterns
                    if re.match(r'^[A-Z]+[0-9]*\s+\{', current_line):
                        syntax_lines.append(current_line.strip())
                        in_syntax = True
                    elif in_syntax and not current_line.strip():
                        in_syntax = False
                    
                    # Look for Result:
                    if 'Result:' in current_line:
                        k = j
                        result_lines = []
                        while k < end and not re.match(r'^[A-Z]', self.lines[k+1]):
                            result_lines.append(self.lines[k])
                            k += 1
                            if k >= end or self.lines[k].strip() == '':
                                break
                        result_text = ' '.join([l.replace('Result:', '').strip() for l in result_lines])
                    
                    # Look for Explanation:
                    if 'Explanation:' in current_line:
                        k = j + 1
                        exp_lines = []
                        while k < end and not re.match(r'^[A-Z]{2,}', self.lines[k]):
                            if self.lines[k].strip():
                                exp_lines.append(self.lines[k].strip())
                            k += 1
                        description_text = ' '.join(exp_lines)
                    
                    # Look for timing in tables
                    timing_match = re.search(r'(\d+(?:\s+or\s+\d+)?(?:\s*/\s*\d+(?:\.\.\.\d+)?)?)\s*$', current_line)
                    if timing_match and 'Clock' not in current_line:
                        timing_info = timing_match.group(1).strip()
                    
                    section_lines.append(current_line)
                    
                    # Stop at next major section
                    if j > start + 5 and re.match(r'^[A-Z]{2,}.*[A-Z]{2,}', current_line):
                        if not any(instr.upper() in current_line.upper() for instr in group_info['instructions']):
                            break
                
                # Build result for each instruction in the group
                for instr in group_info['instructions']:
                    results[instr] = {
                        'found': True,
                        'description': result_text or description_text,
                        'long_description': description_text if result_text else '',
                        'syntax': [s for s in syntax_lines if instr.upper() in s.upper()],
                        'timing': timing_info,
                        'group_doc': True,
                        'group_name': group_name,
                        'related': [i for i in group_info['instructions'] if i != instr]
                    }
                
                if any(r['found'] for r in results.values()):
                    break
        
        return results

def update_yaml_with_group_data(instr, doc_data):
    """Update a YAML file with grouped documentation."""
    yaml_path = YAML_DIR / f"{instr}.yaml"
    
    if not yaml_path.exists():
        print(f"  ⚠️  YAML not found: {instr}.yaml")
        return False
    
    # Load existing YAML
    with open(yaml_path, 'r') as f:
        yaml_data = yaml.safe_load(f) or {}
    
    updated = False
    
    # Update description
    if doc_data.get('description'):
        # Customize description for specific instruction
        desc = doc_data['description']
        # Replace generic counter references with specific ones
        if 'counter 1, 2, or 3' in desc:
            counter_num = instr[-1] if instr[-1].isdigit() else ''
            if counter_num:
                desc = desc.replace('counter 1, 2, or 3', f'counter {counter_num}')
                desc = desc.replace('CT1, CT2, or CT3', f'CT{counter_num}')
        yaml_data['description'] = desc
        updated = True
    
    # Add long description
    if doc_data.get('long_description'):
        yaml_data['long_description'] = doc_data['long_description']
        updated = True
    
    # Add syntax if found
    if doc_data.get('syntax'):
        yaml_data['syntax_variants'] = doc_data['syntax']
        updated = True
    
    # Update timing
    if doc_data.get('timing'):
        if 'timing' not in yaml_data:
            yaml_data['timing'] = {}
        yaml_data['timing']['cycles'] = doc_data['timing']
        if 'or' in doc_data['timing']:
            yaml_data['timing']['type'] = 'conditional'
        updated = True
    
    # Add related instructions
    if doc_data.get('related'):
        yaml_data['related_instructions'] = doc_data['related']
        updated = True
    
    # Mark as documented from group
    if updated:
        yaml_data['documentation_source'] = f"PASM2 Manual 2022-11-01 (grouped: {doc_data.get('group_name', '')})"
        yaml_data['documentation_level'] = 'comprehensive'
        yaml_data['needs_documentation'] = False
        yaml_data['last_updated'] = datetime.now().isoformat()
    
    # Write updated YAML
    if updated:
        with open(yaml_path, 'w') as f:
            yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    return updated

def main():
    print("=" * 60)
    print("PASM2 Grouped Instructions Documentation Update")
    print("=" * 60)
    
    parser = GroupedManualParser()
    
    stats = {
        'groups_processed': 0,
        'instructions_updated': 0,
        'instructions_not_found': 0,
        'total_instructions': 0
    }
    
    print("\nProcessing grouped instructions...\n")
    
    for group_name, group_info in GROUPED_INSTRUCTIONS.items():
        print(f"\nProcessing group: {group_name}")
        stats['groups_processed'] += 1
        
        # Find documentation for this group
        docs = parser.find_grouped_documentation(group_name, group_info)
        
        # Update each instruction's YAML
        for instr in group_info['instructions']:
            stats['total_instructions'] += 1
            
            if instr in docs and docs[instr]['found']:
                if update_yaml_with_group_data(instr, docs[instr]):
                    print(f"  ✅ {instr} - Updated with group documentation")
                    stats['instructions_updated'] += 1
                else:
                    print(f"  ℹ️  {instr} - No updates needed or YAML not found")
            else:
                print(f"  ❌ {instr} - Documentation not found")
                stats['instructions_not_found'] += 1
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Groups processed: {stats['groups_processed']}")
    print(f"Total instructions: {stats['total_instructions']}")
    print(f"Successfully updated: {stats['instructions_updated']}")
    print(f"Not found: {stats['instructions_not_found']}")
    print(f"Success rate: {stats['instructions_updated']/stats['total_instructions']*100:.1f}%")
    
    # Create report
    report_path = YAML_DIR / 'grouped-update-report.md'
    with open(report_path, 'w') as f:
        f.write(f"# Grouped Instructions Update Report\n\n")
        f.write(f"Date: {datetime.now().isoformat()}\n\n")
        f.write(f"## Statistics\n")
        f.write(f"- Groups processed: {stats['groups_processed']}\n")
        f.write(f"- Total instructions: {stats['total_instructions']}\n")
        f.write(f"- Updated: {stats['instructions_updated']}\n")
        f.write(f"- Success rate: {stats['instructions_updated']/stats['total_instructions']*100:.1f}%\n\n")
        f.write(f"## Groups Processed\n")
        for group_name, group_info in GROUPED_INSTRUCTIONS.items():
            f.write(f"- {group_name}: {', '.join(group_info['instructions'])}\n")

if __name__ == "__main__":
    main()