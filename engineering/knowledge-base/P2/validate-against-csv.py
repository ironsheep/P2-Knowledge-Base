#!/usr/bin/env python3
"""
Validate YAML files against authoritative instruction list from CSV
"""

import csv
from pathlib import Path

def validate_against_csv():
    """Check YAML files against actual instructions from CSV"""
    
    # Paths
    csv_path = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv")
    pasm2_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/instructions/pasm2")
    
    # Get real instructions from CSV
    real_instructions = set()
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Get instruction syntax column
            syntax = row.get("#S = immediate (I=1). S = register.\n#D = immediate (L=1). D = register.\n\n- Assembly Syntax -", "").strip()
            if not syntax:
                continue
            
            # Extract mnemonic (first word)
            parts = syntax.split()
            if parts:
                mnemonic = parts[0].upper()
                # Skip conditionals and meta-instructions
                if not any(cond in mnemonic for cond in ['IF_', '_RET_', 'MODCZ', 'MODC', 'MODZ']):
                    if mnemonic not in ['C', 'NC', 'Z', 'NZ', 'CLR', 'EMPTY', 'SET', 'INST']:
                        real_instructions.add(mnemonic.lower())
    
    print(f"Found {len(real_instructions)} real instructions in CSV\n")
    
    # Get current YAML files
    yaml_files = set()
    for yaml_file in pasm2_dir.glob("pasm2_*.yaml"):
        inst_name = yaml_file.stem.replace('pasm2_', '')
        yaml_files.add(inst_name)
    
    print(f"Found {len(yaml_files)} YAML files\n")
    
    # Find issues
    should_not_exist = yaml_files - real_instructions
    missing = real_instructions - yaml_files
    
    # Categorize files that shouldn't exist
    conditionals = []
    pseudo = []
    unknown = []
    
    for inst in sorted(should_not_exist):
        if any(pattern in inst for pattern in ['if_', 'c_', 'nc_', 'z_', 'nz_', '_ret_']):
            conditionals.append(inst)
        elif inst in ['c', 'nc', 'z', 'nz', 'clr', 'empty', 'inst', 'set', 'ret_']:
            pseudo.append(inst)
        elif inst in ['e', 'ne', 'gt', 'ge', 'lt', 'le']:
            conditionals.append(inst)
        else:
            unknown.append(inst)
    
    print("=" * 60)
    print("FILES THAT SHOULD NOT EXIST:")
    print("=" * 60)
    
    if conditionals:
        print(f"\nConditionals ({len(conditionals)}):")
        for inst in conditionals[:20]:
            print(f"  pasm2_{inst}.yaml")
        if len(conditionals) > 20:
            print(f"  ... and {len(conditionals) - 20} more")
    
    if pseudo:
        print(f"\nPseudo-instructions ({len(pseudo)}):")
        for inst in pseudo:
            print(f"  pasm2_{inst}.yaml")
    
    if unknown:
        print(f"\nUnknown/Unexpected ({len(unknown)}):")
        for inst in unknown:
            print(f"  pasm2_{inst}.yaml")
    
    print(f"\nTotal files to remove: {len(should_not_exist)}")
    
    if missing:
        print("\n" + "=" * 60)
        print("MISSING INSTRUCTIONS (should have files):")
        print("=" * 60)
        for inst in sorted(missing)[:20]:
            print(f"  {inst.upper()}")
        if len(missing) > 20:
            print(f"  ... and {len(missing) - 20} more")
    
    # Create removal script
    if should_not_exist:
        script_path = pasm2_dir / 'remove_invalid_files.sh'
        with open(script_path, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write(f"# Remove {len(should_not_exist)} files that don't match CSV instructions\n\n")
            f.write(f"echo 'Removing {len(should_not_exist)} invalid files...'\n\n")
            
            for inst in sorted(should_not_exist):
                f.write(f"rm -f pasm2_{inst}.yaml\n")
            
            f.write(f"\necho 'Removed {len(should_not_exist)} files'\n")
            f.write(f"echo 'Remaining valid instruction files: {len(real_instructions)}'\n")
        
        print(f"\nCreated removal script: {script_path}")
        print("Run with: bash remove_invalid_files.sh")
    
    return should_not_exist, missing

if __name__ == "__main__":
    invalid, missing = validate_against_csv()
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Files to remove: {len(invalid)}")
    print(f"  Missing files: {len(missing)}")
    print(f"  Expected final count: {440 - len(invalid)} files")