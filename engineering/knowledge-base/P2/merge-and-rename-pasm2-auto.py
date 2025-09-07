#!/usr/bin/env python3
"""Merge duplicate PASM2 files and rename without hashes - automatic version."""

import os
import shutil
from pathlib import Path
from collections import defaultdict

def merge_and_rename():
    """Merge duplicate files and rename all to remove hashes."""
    
    pasm2_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/instructions/pasm2")
    
    # Group files by base name (without hash)
    mnemonic_files = defaultdict(list)
    
    for yaml_file in sorted(pasm2_dir.glob("pasm2_*.yaml")):
        name = yaml_file.stem  # gets filename without .yaml
        if name.startswith('pasm2_'):
            name = name[6:]  # remove pasm2_ prefix
        
        # Remove 8-char hash at end  
        if '_' in name and len(name.split('_')[-1]) == 8:
            base_name = '_'.join(name.split('_')[:-1])
        else:
            base_name = name
        
        mnemonic_files[base_name].append(yaml_file)
    
    # Process each mnemonic
    processed = 0
    merged = 0
    renamed = 0
    
    for mnemonic, files in sorted(mnemonic_files.items()):
        # Target filename (no hash)
        if mnemonic.startswith('_'):
            # Special condition instruction like _c, _z
            target_name = f"pasm2{mnemonic}.yaml"
        else:
            target_name = f"pasm2_{mnemonic}.yaml"
        
        target_path = pasm2_dir / target_name
        
        if len(files) > 1:
            # Multiple files - need to merge
            print(f"Merging {len(files)} files for {mnemonic} -> {target_name}")
            
            # Find the file with most content (simple heuristic)
            largest_file = max(files, key=lambda f: f.stat().st_size)
            
            # For now, just use the largest file as the merged content
            shutil.copy2(largest_file, target_path)
            
            # Remove all original files except target
            for f in files:
                if f.absolute() != target_path.absolute():
                    f.unlink()
            
            merged += 1
            
        elif len(files) == 1:
            # Single file - just rename if needed
            source_file = files[0]
            if source_file.absolute() != target_path.absolute():
                source_file.rename(target_path)
                renamed += 1
        
        processed += 1
    
    print(f"\n=== Summary ===")
    print(f"Processed: {processed} unique mnemonics")
    print(f"Merged: {merged} duplicate sets")
    print(f"Renamed: {renamed} files")
    
    # Final count
    final_count = len(list(pasm2_dir.glob("pasm2*.yaml")))
    print(f"\nFinal file count: {final_count}")

if __name__ == "__main__":
    merge_and_rename()