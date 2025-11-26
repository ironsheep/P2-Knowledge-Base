#!/usr/bin/env python3
"""
Extract documentation for instructions marked as weak in the heat map
but actually documented in the PASM2 manual.
"""

import re
import os
import yaml
from pathlib import Path

# Instructions marked as poor (score < 40) in the heat map
# that we should check in the manual
WEAK_INSTRUCTIONS = [
    'ADDCT1', 'ADDCT2', 'ADDCT3', 'ALIGNL', 'ALIGNW',
    'CRCNIB', 'DJZ', 'GETPTR', 'GETSCP', 'HUBSET', 'IJZ',
    'JATN', 'JCT1', 'JCT2', 'JCT3', 'JFBW', 'JINT',
    'JNCT1', 'JNCT2', 'JNCT3', 'JNSE1', 'JNSE2', 'JNSE3', 'JNSE4',
    'JPAT', 'JQMT', 'JSE1', 'JSE2', 'JSE3', 'JSE4',
    'JXFI', 'JXMT', 'JXRL', 'JXRO', 'LOC', 'LOCKRET', 
    'MERGEB', 'MERGEW', 'MOVBYTS', 'MULPIX', 'NIXINT1', 'NIXINT2', 'NIXINT3',
    'POLLCT1', 'POLLCT2', 'POLLCT3', 'POLLSE1', 'POLLSE2', 'POLLSE3', 'POLLSE4',
    'PUSH', 'PUSHA', 'PUSHB', 'REP', 'RESI0', 'RESI1', 'RESI2', 'RESI3',
    'RETI0', 'RETI1', 'RETI2', 'RETI3', 'SETINT1', 'SETINT2', 'SETINT3',
    'SETPIV', 'SETPIX', 'SETSE1', 'SETSE2', 'SETSE3', 'SETSE4', 'SETXFRQ',
    'SPLITB', 'SPLITW', 'TJF', 'TJS', 'TJZ', 'TRGINT1', 'TRGINT2', 'TRGINT3',
    'WFBYTE', 'WRBYTE', 'WRC', 'WRLUT', 'WRWORD', 'WRZ', 'XSTOP',
    'AND', 'BITC', 'BITH', 'BITZ', 'BLNPIX', 'CALLA', 'CALLPA',
    'CRCBIT', 'DIRC', 'DIRH', 'DIRZ', 'DJF', 'DRVC', 'DRVH', 'DRVZ',
    'FLTC', 'FLTH', 'FLTZ', 'GETCT', 'GETQX', 'GETQY', 'GETRND',
    'JMP', 'JMPREL', 'LOCKNEW', 'MIXPIX', 'MODC', 'MODZ', 'MUXC', 'MUXZ',
    'NOT', 'OUTC', 'OUTH', 'OUTZ', 'POP', 'POPA', 'POPB',
    'RDBYTE', 'RDLONG', 'RDLUT', 'RDPIN', 'RDWORD',
    'RET', 'RETA', 'RETB', 'RFBYTE', 'RFLONG', 'RFVAR', 'RFVARS', 'RFWORD',
    'RGBEXP', 'RGBSQZ', 'RQPIN', 'SETCFRQ', 'SETCI', 'SETCMOD', 'SETCQ',
    'SETCY', 'SETDACS', 'SETSCP', 'SUMC', 'SUMZ', 'TESTB',
    'WAITCT1', 'WAITCT2', 'WAITCT3', 'WAITSE1', 'WAITSE2', 'WAITSE3', 'WAITSE4',
    'WFLONG', 'WFWORD', 'WRLONG', 'XCONT', 'XORO32', 'XZERO',
    'EXECF', 'POLLXFI', 'POLLXRL', 'REV', 'WRNC', 'ASMCLK', 'DEBUG'
]

def load_manual():
    """Load the PASM2 manual narrative text."""
    manual_path = '/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/pasm2-manual/pasm2-manual-narrative.txt'
    with open(manual_path, 'r') as f:
        return f.readlines()

def find_instruction_in_manual(lines, instruction):
    """Find an instruction's documentation in the manual."""
    # Look for instruction patterns
    patterns = [
        f"^{instruction}\\b",  # Start of line
        f"^{instruction} /",   # Instruction with variant
        f"^{instruction}$",     # Exact match
    ]
    
    results = []
    for i, line in enumerate(lines):
        for pattern in patterns:
            if re.match(pattern, line):
                # Found instruction, now extract description
                start = i
                end = min(i + 150, len(lines))  # Look ahead up to 150 lines
                
                # Extract the section
                section = []
                for j in range(start, end):
                    section.append(lines[j])
                    # Stop at next instruction or major section
                    if j > start + 5 and (
                        re.match(r'^[A-Z]{2,}', lines[j]) or
                        re.match(r'^Copyright', lines[j])
                    ):
                        break
                
                results.append({
                    'line': i + 1,
                    'instruction': instruction,
                    'text': ''.join(section)
                })
    
    return results

def extract_instruction_details(text):
    """Parse instruction text to extract key details."""
    details = {
        'syntax': [],
        'description': '',
        'flags': {},
        'timing': '',
        'encoding': '',
        'examples': []
    }
    
    lines = text.split('\n')
    in_example = False
    
    for i, line in enumerate(lines):
        # Look for syntax patterns
        if re.match(r'^[A-Z]+\s+[\{\[]', line) or re.match(r'^[A-Z]+\s+#', line):
            details['syntax'].append(line.strip())
        
        # Look for Result: or Description:
        if line.startswith('Result:'):
            details['description'] = line[7:].strip()
            # Get following lines that are part of description
            j = i + 1
            while j < len(lines) and lines[j].startswith('    '):
                details['description'] += ' ' + lines[j].strip()
                j += 1
        
        # Look for flag effects
        if 'C Flag' in line or 'Z Flag' in line:
            if 'C Flag' in line:
                details['flags']['C'] = line.split('C Flag')[-1].strip()
            if 'Z Flag' in line:
                details['flags']['Z'] = line.split('Z Flag')[-1].strip()
        
        # Look for timing
        if 'Clocks' in line or 'cycles' in line.lower():
            details['timing'] = line.strip()
        
        # Look for encoding table
        if 'COND INSTR' in line or 'EEEE' in line:
            details['encoding'] = line.strip()
        
        # Look for examples
        if line.strip().startswith(';') or line.strip().startswith("'"):
            in_example = True
        if in_example and line.strip():
            details['examples'].append(line.strip())
    
    return details

def create_yaml_content(instruction, details, manual_text):
    """Create YAML content for an instruction."""
    yaml_content = {
        'mnemonic': instruction,
        'name': instruction,
        'description': details['description'] or f'{instruction} instruction',
        'syntax': details['syntax'] if details['syntax'] else [instruction],
    }
    
    if details['flags']:
        yaml_content['flags'] = details['flags']
    
    if details['timing']:
        yaml_content['timing'] = details['timing']
    
    if details['encoding']:
        yaml_content['encoding'] = details['encoding']
    
    if details['examples']:
        yaml_content['examples'] = details['examples'][:3]  # Limit to 3 examples
    
    # Add source reference
    yaml_content['source'] = 'PASM2 Manual 2022-11-01'
    yaml_content['extracted_from_manual'] = True
    
    return yaml_content

def main():
    print("Loading PASM2 manual...")
    lines = load_manual()
    
    output_dir = Path('/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/document-production/manuals/pasm2-reference/extracted-from-manual')
    output_dir.mkdir(exist_ok=True)
    
    found_count = 0
    not_found = []
    
    print(f"\nSearching for {len(WEAK_INSTRUCTIONS)} weak instructions in manual...\n")
    
    for instruction in WEAK_INSTRUCTIONS:
        results = find_instruction_in_manual(lines, instruction)
        
        if results:
            found_count += 1
            print(f"✅ Found {instruction} at line {results[0]['line']}")
            
            # Extract details
            details = extract_instruction_details(results[0]['text'])
            
            # Create YAML content
            yaml_content = create_yaml_content(instruction, details, results[0]['text'])
            
            # Save to file
            output_file = output_dir / f"{instruction}.yaml"
            with open(output_file, 'w') as f:
                yaml.dump(yaml_content, f, default_flow_style=False, allow_unicode=True)
            
            # Also save raw text for reference
            text_file = output_dir / f"{instruction}.txt"
            with open(text_file, 'w') as f:
                f.write(results[0]['text'])
        else:
            not_found.append(instruction)
            print(f"❌ Not found: {instruction}")
    
    print(f"\n=== Summary ===")
    print(f"Found: {found_count}/{len(WEAK_INSTRUCTIONS)} instructions")
    print(f"Not found: {len(not_found)} instructions")
    
    if not_found:
        print(f"\nInstructions not found in manual:")
        for instr in sorted(not_found):
            print(f"  - {instr}")
    
    # Create a summary report
    summary_file = output_dir / "extraction-summary.md"
    with open(summary_file, 'w') as f:
        f.write("# Extraction Summary\n\n")
        f.write(f"Date: 2025-01-19\n\n")
        f.write(f"## Statistics\n")
        f.write(f"- Searched: {len(WEAK_INSTRUCTIONS)} instructions\n")
        f.write(f"- Found: {found_count} instructions\n")
        f.write(f"- Not found: {len(not_found)} instructions\n\n")
        
        if not_found:
            f.write("## Instructions Not Found\n")
            for instr in sorted(not_found):
                f.write(f"- {instr}\n")

if __name__ == "__main__":
    main()