#!/usr/bin/env python3
"""
Update PASM2 YAML files with rich documentation from the PASM2 manual.
Focus on the 168 weak instructions that were found in the manual.
"""

import yaml
import re
from pathlib import Path
import shutil
from datetime import datetime

# Base paths
YAML_DIR = Path('/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/pasm2')
MANUAL_PATH = Path('/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/pasm2-manual/pasm2-manual-narrative.txt')
BACKUP_DIR = YAML_DIR / 'backup_before_update'

# Instructions from heat map that need improvement (score < 40)
WEAK_INSTRUCTIONS = [
    'addct1', 'addct2', 'addct3', 'crcnib', 'djz', 'getptr', 'getscp',
    'hubset', 'ijz', 'jatn', 'jct1', 'jct2', 'jct3', 'jfbw', 'jint',
    'jnct1', 'jnct2', 'jnct3', 'jnse1', 'jnse2', 'jnse3', 'jnse4',
    'jpat', 'jqmt', 'jse1', 'jse2', 'jse3', 'jse4', 'jxfi', 'jxmt',
    'jxrl', 'jxro', 'loc', 'lockret', 'mergeb', 'mergew', 'movbyts',
    'mulpix', 'nixint1', 'nixint2', 'nixint3', 'pollct1', 'pollct2',
    'pollct3', 'pollse1', 'pollse2', 'pollse3', 'pollse4', 'push',
    'pusha', 'pushb', 'rep', 'resi0', 'resi1', 'resi2', 'resi3',
    'reti0', 'reti1', 'reti2', 'reti3', 'setint1', 'setint2', 'setint3',
    'setpiv', 'setpix', 'setse1', 'setse2', 'setse3', 'setse4', 'setxfrq',
    'splitb', 'splitw', 'tjf', 'tjs', 'tjz', 'trgint1', 'trgint2',
    'trgint3', 'wfbyte', 'wrbyte', 'wrc', 'wrlut', 'wrword', 'wrz',
    'xstop', 'and', 'bitc', 'bith', 'bitz', 'blnpix', 'calla', 'callpa',
    'crcbit', 'dirc', 'dirh', 'dirz', 'djf', 'drvc', 'drvh', 'drvz',
    'fltc', 'flth', 'fltz', 'getct', 'getqx', 'getqy', 'getrnd', 'jmp',
    'jmprel', 'locknew', 'mixpix', 'modc', 'modz', 'muxc', 'muxz',
    'not', 'outc', 'outh', 'outz', 'pop', 'popa', 'popb', 'rdbyte',
    'rdlong', 'rdlut', 'rdpin', 'rdword', 'ret', 'reta', 'retb',
    'rfbyte', 'rflong', 'rfvar', 'rfvars', 'rfword', 'rgbexp', 'rgbsqz',
    'rqpin', 'setcfrq', 'setci', 'setcmod', 'setcq', 'setcy', 'setdacs',
    'setscp', 'sumc', 'sumz', 'testb', 'waitct1', 'waitct2', 'waitct3',
    'waitse1', 'waitse2', 'waitse3', 'waitse4', 'wflong', 'wfword',
    'wrlong', 'xcont', 'xoro32', 'xzero', 'execf', 'pollxfi', 'pollxrl',
    'rev', 'wrnc'
]

class ManualParser:
    def __init__(self):
        with open(MANUAL_PATH, 'r') as f:
            self.lines = f.readlines()
        self.instruction_data = {}
        
    def find_instruction(self, instr):
        """Find comprehensive documentation for an instruction."""
        instr_upper = instr.upper()
        data = {
            'found': False,
            'description': '',
            'long_description': '',
            'syntax_variants': [],
            'timing': {},
            'flags': {},
            'examples': [],
            'notes': [],
            'related': []
        }
        
        # Search in instruction table (lines 8000-9000)
        for i in range(8000, min(9000, len(self.lines))):
            line = self.lines[i]
            if line.startswith(instr_upper + ' ') or line.startswith(instr_upper + '\t'):
                # Found in table - extract description
                parts = line.strip().split(maxsplit=2)
                if len(parts) >= 3:
                    data['found'] = True
                    syntax = parts[1] if len(parts) > 1 else ""
                    rest = parts[2] if len(parts) > 2 else ""
                    
                    # Parse timing from end
                    timing_match = re.search(r'(\d+(?:\.\.\.\d+)?(?:\s*/\s*\d+(?:\.\.\.\d+)?)?)\s*$', rest)
                    if timing_match:
                        data['description'] = rest[:timing_match.start()].strip()
                        timing_str = timing_match.group(1).strip()
                        if '...' in timing_str:
                            data['timing']['type'] = 'variable'
                            data['timing']['range'] = timing_str
                        else:
                            data['timing']['cycles'] = timing_str
                    else:
                        data['description'] = rest.strip()
                    
                    if syntax and syntax != data['description']:
                        data['syntax_variants'].append(f"{instr_upper} {syntax}")
                break
        
        # Search for detailed description in main text
        for i, line in enumerate(self.lines):
            # Look for instruction header patterns
            if re.match(f'^{instr_upper}\\b', line):
                # Check if this is a detailed section (not in a table)
                if i < 8000 or i > 9000:
                    # Extract detailed description
                    detail_lines = []
                    j = i + 1
                    while j < len(self.lines) and j < i + 50:
                        next_line = self.lines[j]
                        # Stop at next instruction or section
                        if re.match(r'^[A-Z]{2,}', next_line) and not next_line.startswith('    '):
                            break
                        detail_lines.append(next_line)
                        j += 1
                    
                    # Parse the detailed section
                    detail_text = ''.join(detail_lines)
                    
                    # Look for Result:
                    result_match = re.search(r'Result:\s*(.+?)(?=\n[A-Z]|\n\n|\Z)', detail_text, re.DOTALL)
                    if result_match:
                        data['long_description'] = result_match.group(1).strip()
                    
                    # Look for examples
                    example_matches = re.findall(r"'([^']+)'", detail_text)
                    if example_matches:
                        data['examples'] = example_matches[:3]  # Limit to 3
                    
                    # Look for flag effects
                    if 'C Flag' in detail_text or 'C =' in detail_text:
                        c_match = re.search(r'C\s*(?:Flag\s*)?[=:]\s*([^\n]+)', detail_text)
                        if c_match:
                            data['flags']['C'] = c_match.group(1).strip()
                    
                    if 'Z Flag' in detail_text or 'Z =' in detail_text:
                        z_match = re.search(r'Z\s*(?:Flag\s*)?[=:]\s*([^\n]+)', detail_text)
                        if z_match:
                            data['flags']['Z'] = z_match.group(1).strip()
        
        return data

def update_yaml_file(instr, manual_data):
    """Update a YAML file with data from the manual."""
    yaml_path = YAML_DIR / f"{instr}.yaml"
    
    if not yaml_path.exists():
        print(f"  ⚠️  YAML file not found: {instr}.yaml")
        return False
    
    # Load existing YAML
    with open(yaml_path, 'r') as f:
        yaml_data = yaml.safe_load(f) or {}
    
    # Track if we made updates
    updated = False
    
    # Update description if we found better one
    if manual_data['description'] and len(manual_data['description']) > len(yaml_data.get('description', '')):
        yaml_data['description'] = manual_data['description']
        updated = True
    
    # Add long description if found
    if manual_data['long_description']:
        yaml_data['long_description'] = manual_data['long_description']
        updated = True
    
    # Add examples if we found any
    if manual_data['examples'] and not yaml_data.get('examples'):
        yaml_data['examples'] = manual_data['examples']
        updated = True
    
    # Update timing if more detailed
    if manual_data['timing']:
        if 'timing' not in yaml_data:
            yaml_data['timing'] = {}
        yaml_data['timing'].update(manual_data['timing'])
        updated = True
    
    # Update flags if more detailed
    if manual_data['flags']:
        if 'flags_affected' not in yaml_data:
            yaml_data['flags_affected'] = {}
        for flag, effect in manual_data['flags'].items():
            if flag not in yaml_data['flags_affected'] or not yaml_data['flags_affected'][flag]:
                yaml_data['flags_affected'][flag] = {'formula': effect}
                updated = True
    
    # Add syntax variants
    if manual_data['syntax_variants']:
        existing_syntax = yaml_data.get('syntax', '')
        for variant in manual_data['syntax_variants']:
            if variant not in existing_syntax:
                yaml_data['syntax_variants'] = yaml_data.get('syntax_variants', []) + [variant]
                updated = True
    
    # Update documentation status
    if updated:
        yaml_data['documentation_source'] = 'PASM2 Manual 2022-11-01'
        yaml_data['documentation_level'] = 'enhanced'
        yaml_data['last_updated'] = datetime.now().isoformat()
        yaml_data['needs_documentation'] = False
    
    # Write updated YAML
    if updated:
        with open(yaml_path, 'w') as f:
            yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        return True
    
    return False

def main():
    print("=" * 60)
    print("PASM2 YAML Documentation Update from Manual")
    print("=" * 60)
    
    # Create backup directory
    BACKUP_DIR.mkdir(exist_ok=True)
    
    # Initialize parser
    parser = ManualParser()
    
    # Statistics
    stats = {
        'total': len(WEAK_INSTRUCTIONS),
        'found_in_manual': 0,
        'updated': 0,
        'not_found_yaml': 0,
        'not_found_manual': 0,
        'no_updates': 0
    }
    
    print(f"\nProcessing {stats['total']} weak instructions...\n")
    
    for instr in WEAK_INSTRUCTIONS:
        print(f"Processing {instr}...")
        
        # Backup existing YAML if it exists
        yaml_path = YAML_DIR / f"{instr}.yaml"
        if yaml_path.exists():
            backup_path = BACKUP_DIR / f"{instr}.yaml"
            shutil.copy2(yaml_path, backup_path)
        
        # Find in manual
        manual_data = parser.find_instruction(instr)
        
        if manual_data['found']:
            stats['found_in_manual'] += 1
            
            # Update YAML
            if update_yaml_file(instr, manual_data):
                stats['updated'] += 1
                print(f"  ✅ Updated with manual documentation")
            else:
                if not yaml_path.exists():
                    stats['not_found_yaml'] += 1
                    print(f"  ⚠️  YAML file not found")
                else:
                    stats['no_updates'] += 1
                    print(f"  ℹ️  No updates needed")
        else:
            stats['not_found_manual'] += 1
            print(f"  ❌ Not found in manual")
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total instructions processed: {stats['total']}")
    print(f"Found in manual: {stats['found_in_manual']}")
    print(f"Successfully updated: {stats['updated']}")
    print(f"YAML files not found: {stats['not_found_yaml']}")
    print(f"Not found in manual: {stats['not_found_manual']}")
    print(f"No updates needed: {stats['no_updates']}")
    
    print(f"\n✅ Backup created in: {BACKUP_DIR}")
    print(f"✅ Updated {stats['updated']} YAML files with manual documentation")
    
    # Create update report
    report_path = YAML_DIR / 'update-report.md'
    with open(report_path, 'w') as f:
        f.write(f"# YAML Update Report\n\n")
        f.write(f"Date: {datetime.now().isoformat()}\n\n")
        f.write(f"## Statistics\n")
        f.write(f"- Total processed: {stats['total']}\n")
        f.write(f"- Updated: {stats['updated']}\n")
        f.write(f"- Found in manual: {stats['found_in_manual']}\n")
        f.write(f"- Success rate: {stats['updated']/stats['total']*100:.1f}%\n")

if __name__ == "__main__":
    main()