#!/usr/bin/env python3
"""
Simple timing data extractor from P2 datasheet markdown tables
"""

import re
from pathlib import Path
from datetime import datetime

def extract_timing_data():
    datasheet_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/p2-datasheet/pasm2-complete-instruction-tables.md"
    yaml_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/instructions/pasm2")
    
    updated = 0
    not_found = 0
    
    # Read datasheet
    with open(datasheet_path, 'r') as f:
        content = f.read()
    
    # Split into sections
    sections = content.split('\n## ')
    
    # Build timing database
    timing_data = {}
    
    for section in sections:
        lines = section.split('\n')
        
        # Check for fixed timing statements
        if 'execute in 2 clock cycles' in section:
            # All instructions in this section have 2 cycle timing
            for line in lines:
                if line.startswith('| **'):
                    match = re.match(r'\| \*\*([A-Z][A-Z0-9]*)', line)
                    if match:
                        mnemonic = match.group(1)
                        if mnemonic not in timing_data:
                            timing_data[mnemonic] = {
                                'raw': '2',
                                'base_cycles': 2,
                                'type': 'fixed'
                            }
        
        # Parse tables with timing columns
        in_table = False
        for line in lines:
            if '|' in line and 'Clock' in line:
                in_table = True
                continue
            
            if in_table and line.startswith('| **'):
                parts = line.split('|')
                if len(parts) >= 3:
                    # Extract mnemonic
                    inst_part = parts[1].strip()
                    match = re.match(r'\*\*([A-Z][A-Z0-9]*)', inst_part)
                    if match:
                        mnemonic = match.group(1)
                        
                        # Check if timing is in column 3 or 4
                        timing_str = None
                        if len(parts) > 3:
                            col3 = parts[3].strip()
                            # Check if col3 looks like timing
                            if any(x in col3 for x in ['2', '3', '4', '...', '+', '/', 'or']):
                                timing_str = col3
                        
                        if timing_str and mnemonic not in timing_data:
                            # Parse timing
                            timing_info = parse_timing(timing_str)
                            if timing_info:
                                timing_data[mnemonic] = timing_info
    
    # Update YAML files
    for yaml_file in yaml_dir.glob("pasm2_*.yaml"):
        try:
            # Read existing file
            with open(yaml_file, 'r') as f:
                content = f.read()
            
            # Extract mnemonic from layer1
            mnemonic = None
            for line in content.split('\n'):
                if line.strip().startswith('mnemonic:'):
                    mnemonic = line.split(':', 1)[1].strip()
                    break
            
            if mnemonic and mnemonic in timing_data:
                # Check if layer2 exists
                if 'layer2_datasheet:' not in content:
                    # Add layer2
                    layer2_content = f"""
layer2_datasheet:
  extraction_date: {datetime.now().isoformat()}
  source: P2 Datasheet v35
  timing:
    raw: {timing_data[mnemonic].get('raw', 'null')}"""
                    
                    if timing_data[mnemonic].get('base_cycles'):
                        layer2_content += f"\n    base_cycles: {timing_data[mnemonic]['base_cycles']}"
                    
                    if timing_data[mnemonic].get('type'):
                        layer2_content += f"\n    type: {timing_data[mnemonic]['type']}"
                    
                    if timing_data[mnemonic].get('notes'):
                        layer2_content += "\n    notes:"
                        for note in timing_data[mnemonic]['notes']:
                            layer2_content += f"\n      - {note}"
                    
                    if timing_data[mnemonic].get('min_cycles'):
                        layer2_content += f"\n    min_cycles: {timing_data[mnemonic]['min_cycles']}"
                    
                    if timing_data[mnemonic].get('max_cycles'):
                        layer2_content += f"\n    max_cycles: {timing_data[mnemonic]['max_cycles']}"
                    
                    # Append to file
                    with open(yaml_file, 'a') as f:
                        f.write(layer2_content)
                    
                    updated += 1
                    print(f"Updated: {mnemonic}")
            else:
                if mnemonic:
                    not_found += 1
                    
        except Exception as e:
            print(f"Error processing {yaml_file.name}: {e}")
    
    print(f"\nComplete:")
    print(f"  Updated: {updated}")
    print(f"  No timing found: {not_found}")
    print(f"  Coverage: {updated/(updated+not_found)*100:.1f}%")

def parse_timing(timing_str):
    """Parse timing string into structured format"""
    result = {'raw': timing_str}
    
    # Simple fixed timing (e.g., "2")
    if timing_str.strip().isdigit():
        result['base_cycles'] = int(timing_str.strip())
        result['type'] = 'fixed'
        return result
    
    # Range timing (e.g., "13...20")
    if '...' in timing_str:
        match = re.search(r'(\d+)\.\.\.(\d+)', timing_str)
        if match:
            result['min_cycles'] = int(match.group(1))
            result['max_cycles'] = int(match.group(2))
            result['type'] = 'variable'
            result['notes'] = ['Hub window alignment affects timing']
            return result
    
    # Conditional timing (e.g., "2 or 4")
    if ' or ' in timing_str:
        match = re.findall(r'\d+', timing_str)
        if match:
            cycles = [int(x) for x in match]
            result['base_cycles'] = cycles[0]
            result['type'] = 'conditional'
            result['notes'] = [f"Conditional timing: {' or '.join(str(c) for c in cycles)} cycles"]
            return result
    
    # Variable with plus (e.g., "2+")
    if '+' in timing_str:
        match = re.match(r'(\d+)\+', timing_str)
        if match:
            result['base_cycles'] = int(match.group(1))
            result['type'] = 'variable'
            result['notes'] = ['Plus additional cycles based on condition']
            return result
    
    # Split timing (e.g., "4 / 13...20")
    if '/' in timing_str:
        parts = timing_str.split('/')
        if len(parts) == 2:
            # Parse first part (cog/lut)
            cog_part = parts[0].strip()
            if cog_part.isdigit():
                result['base_cycles'] = int(cog_part)
                result['type'] = 'mode_dependent'
            
            # Parse second part (hub)
            hub_part = parts[1].strip()
            if '...' in hub_part:
                match = re.search(r'(\d+)\.\.\.(\d+)', hub_part)
                if match:
                    result['hub_min'] = int(match.group(1))
                    result['hub_max'] = int(match.group(2))
                    result['notes'] = ['Different timing for cog/lut vs hub execution']
            
            return result
    
    # Default: just store raw
    result['type'] = 'complex'
    return result

if __name__ == "__main__":
    extract_timing_data()