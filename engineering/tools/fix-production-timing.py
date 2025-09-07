#!/usr/bin/env python3
"""
Fix timing extraction in production files by pulling from source files
"""

from pathlib import Path
import re

def extract_timing_from_source(source_file):
    """Extract timing information from multi-layer source file"""
    
    with open(source_file, 'r') as f:
        content = f.read()
    
    timing_data = {}
    
    # Look for different timing formats in the source
    lines = content.split('\n')
    in_timing = False
    
    for i, line in enumerate(lines):
        # Detect timing sections
        if 'timing:' in line:
            in_timing = True
            continue
            
        if in_timing:
            # End of timing section
            if line and not line.startswith(' '):
                in_timing = False
                continue
                
            # Extract timing values
            if 'cog_exec_8_cogs:' in line:
                cycles = line.split(':')[1].strip()
                timing_data['cycles'] = cycles
                timing_data['type'] = 'fixed'
                
            elif 'cog_exec_16_cogs:' in line:
                # Use this if we don't have 8_cogs
                if 'cycles' not in timing_data:
                    cycles = line.split(':')[1].strip()
                    timing_data['cycles'] = cycles
                    timing_data['type'] = 'fixed'
                    
            elif 'base_cycles:' in line:
                cycles = line.split(':')[1].strip()
                timing_data['cycles'] = cycles
                timing_data['type'] = 'fixed'
                
            elif 'raw:' in line:
                raw = line.split(':', 1)[1].strip()
                # Parse raw timing like "2 or 4 / 2 or 13...20"
                # Take the first number as cycles
                if not timing_data.get('cycles'):
                    match = re.search(r'(\d+)', raw)
                    if match:
                        timing_data['cycles'] = match.group(1)
                        if '...' in raw or 'or' in raw:
                            timing_data['type'] = 'variable'
                        else:
                            timing_data['type'] = 'fixed'
    
    return timing_data

def fix_production_file(prod_file, source_file):
    """Update production file with timing from source"""
    
    # Get timing from source
    timing = extract_timing_from_source(source_file)
    
    if not timing:
        return False
    
    # Read production file
    with open(prod_file, 'r') as f:
        lines = f.readlines()
    
    # Check if timing already exists
    has_timing = any('timing:' in line for line in lines)
    
    if has_timing:
        return False  # Already has timing
    
    # Find where to insert timing (after description or encoding)
    insert_pos = len(lines)
    for i, line in enumerate(lines):
        if line.startswith('group:'):
            insert_pos = i
            break
        elif line.startswith('flags_affected:'):
            insert_pos = i
            break
    
    # Insert timing
    timing_lines = ['timing:\n']
    if 'cycles' in timing:
        timing_lines.append(f"  cycles: {timing['cycles']}\n")
    if 'type' in timing:
        timing_lines.append(f"  type: {timing['type']}\n")
    
    # Insert into file
    lines[insert_pos:insert_pos] = timing_lines
    
    # Write back
    with open(prod_file, 'w') as f:
        f.writelines(lines)
    
    return True

def main():
    """Fix timing in all production files"""
    
    base_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base")
    
    prod_dir = base_dir / "P2/instructions/pasm2"
    source_dir = base_dir / "P2-support/sources/_sources/instructions/pasm2"
    
    if not prod_dir.exists() or not source_dir.exists():
        print("ERROR: Directories not found!")
        return
    
    fixed = 0
    already_ok = 0
    no_source = 0
    
    for prod_file in sorted(prod_dir.glob("*.yaml")):
        inst_name = prod_file.stem
        source_file = source_dir / f"pasm2_{inst_name}.yaml"
        
        if not source_file.exists():
            print(f"⚠️  No source for {inst_name}")
            no_source += 1
            continue
        
        if fix_production_file(prod_file, source_file):
            print(f"✅ Fixed timing for {inst_name}")
            fixed += 1
        else:
            already_ok += 1
    
    print(f"\n📊 Summary:")
    print(f"  Fixed: {fixed}")
    print(f"  Already had timing: {already_ok}")
    print(f"  No source file: {no_source}")
    print(f"  Total files: {fixed + already_ok + no_source}")
    
    # Calculate new coverage
    total = fixed + already_ok + no_source
    with_timing = fixed + already_ok
    coverage = (with_timing / total) * 100 if total > 0 else 0
    print(f"  New timing coverage: {coverage:.1f}%")

if __name__ == "__main__":
    main()