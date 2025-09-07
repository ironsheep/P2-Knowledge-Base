#!/usr/bin/env python3
"""
Identify and remove conditional files that shouldn't exist as instructions
"""

from pathlib import Path

def identify_conditionals():
    """Find all conditional files that need to be removed"""
    
    pasm2_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/instructions/pasm2")
    
    # Patterns for conditionals (not real instructions)
    conditional_patterns = [
        'if_',     # IF_00, IF_NC_AND_Z, etc.
        'c_and_',  # C_AND_Z, C_AND_NZ
        'c_eq_',   # C_EQ_Z
        'c_ne_',   # C_NE_Z
        'c_or_',   # C_OR_Z, C_OR_NZ
        'nc_and_', # NC_AND_Z, NC_AND_NZ
        'nc_or_',  # NC_OR_Z, NC_OR_NZ
        'z_and_',  # Z_AND_C, Z_AND_NC
        'z_eq_',   # Z_EQ_C
        'z_ne_',   # Z_NE_C
        'z_or_',   # Z_OR_C, Z_OR_NC
        'nz_and_', # NZ_AND_C, NZ_AND_NC
        'nz_or_',  # NZ_OR_C, NZ_OR_NC
        '_ret_',   # _RET_ suffix conditionals
    ]
    
    # Also single-name conditionals
    single_conditionals = [
        'c', 'nc', 'z', 'nz',  # Flag conditionals
        'e', 'ne',              # Equal/not equal
        'gt', 'ge', 'lt', 'le', # Comparisons
        'empty',                # Pseudo-instruction
        'clr',                  # Pseudo-instruction (alias for MOV)
        'inst',                 # Meta-instruction
        'set',                  # Might be pseudo
        'ret_',                 # Conditional return prefix
    ]
    
    files_to_remove = []
    
    for yaml_file in pasm2_dir.glob("pasm2_*.yaml"):
        filename = yaml_file.stem.replace('pasm2_', '')
        
        # Check patterns
        for pattern in conditional_patterns:
            if pattern in filename:
                files_to_remove.append(yaml_file)
                break
        
        # Check exact matches
        if filename in single_conditionals:
            files_to_remove.append(yaml_file)
    
    # Sort and report
    files_to_remove = sorted(set(files_to_remove))
    
    print(f"Found {len(files_to_remove)} conditional/pseudo files to remove:\n")
    
    # Group by type for clarity
    if_files = [f for f in files_to_remove if 'if_' in f.name]
    c_files = [f for f in files_to_remove if 'c_' in f.name and 'if_' not in f.name]
    z_files = [f for f in files_to_remove if ('z_' in f.name or 'nz_' in f.name) and 'if_' not in f.name and 'c_' not in f.name]
    comparison_files = [f for f in files_to_remove if f.stem.replace('pasm2_', '') in ['e', 'ne', 'gt', 'ge', 'lt', 'le']]
    flag_files = [f for f in files_to_remove if f.stem.replace('pasm2_', '') in ['c', 'nc', 'z', 'nz']]
    pseudo_files = [f for f in files_to_remove if f.stem.replace('pasm2_', '') in ['empty', 'clr', 'inst', 'set', 'ret_']]
    
    print(f"IF conditionals ({len(if_files)}):")
    for f in if_files[:10]:
        print(f"  {f.name}")
    if len(if_files) > 10:
        print(f"  ... and {len(if_files) - 10} more")
    
    print(f"\nC flag conditionals ({len(c_files)}):")
    for f in c_files[:10]:
        print(f"  {f.name}")
    if len(c_files) > 10:
        print(f"  ... and {len(c_files) - 10} more")
    
    print(f"\nZ flag conditionals ({len(z_files)}):")
    for f in z_files[:10]:
        print(f"  {f.name}")
    if len(z_files) > 10:
        print(f"  ... and {len(z_files) - 10} more")
    
    print(f"\nComparison conditionals ({len(comparison_files)}):")
    for f in comparison_files:
        print(f"  {f.name}")
    
    print(f"\nFlag conditionals ({len(flag_files)}):")
    for f in flag_files:
        print(f"  {f.name}")
    
    print(f"\nPseudo-instructions ({len(pseudo_files)}):")
    for f in pseudo_files:
        print(f"  {f.name}")
    
    # Create removal script
    print(f"\n{'='*60}")
    print("Creating removal script...")
    
    with open(pasm2_dir / 'remove_conditionals.sh', 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("# Remove conditional and pseudo-instruction files\n\n")
        f.write(f"echo 'Removing {len(files_to_remove)} conditional/pseudo files...'\n\n")
        
        for file in files_to_remove:
            f.write(f"rm -f {file.name}\n")
        
        f.write(f"\necho 'Removed {len(files_to_remove)} files'\n")
    
    print(f"Created removal script: remove_conditionals.sh")
    print(f"Run with: bash remove_conditionals.sh")
    
    return files_to_remove

if __name__ == "__main__":
    files = identify_conditionals()
    print(f"\nTotal files to remove: {len(files)}")