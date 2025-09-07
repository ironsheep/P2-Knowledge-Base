#!/usr/bin/env python3
"""Find duplicate instruction mnemonics."""

from pathlib import Path
from collections import defaultdict

pasm2_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/instructions/pasm2")

# Group files by base name (without hash)
mnemonic_files = defaultdict(list)

for yaml_file in sorted(pasm2_dir.glob("pasm2_*.yaml")):
    # Remove pasm2_ prefix and hash suffix
    name = yaml_file.stem  # gets filename without .yaml
    if name.startswith('pasm2_'):
        name = name[6:]  # remove pasm2_ prefix
    
    # Remove 8-char hash at end
    if '_' in name and len(name.split('_')[-1]) == 8:
        base_name = '_'.join(name.split('_')[:-1])
    else:
        base_name = name
    
    mnemonic_files[base_name].append(yaml_file.name)

# Print duplicates
print("DUPLICATE INSTRUCTION FILES (same mnemonic, multiple files):")
print("=" * 60)

duplicate_count = 0
total_extra_files = 0

for mnemonic, files in sorted(mnemonic_files.items()):
    if len(files) > 1:
        duplicate_count += 1
        total_extra_files += len(files) - 1
        print(f"\n{mnemonic}: {len(files)} files")
        for f in files:
            print(f"  - {f}")

print(f"\n{duplicate_count} mnemonics have duplicates")
print(f"{total_extra_files} extra files that should be merged")
print(f"\nUnique mnemonics: {len(mnemonic_files)}")
print(f"Total files: {sum(len(files) for files in mnemonic_files.values())}")