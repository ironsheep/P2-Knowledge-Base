#!/usr/bin/env python3
"""Survey all keys in PASM2 YAML files to understand schema consistency."""

import yaml
import os
import glob
from collections import Counter

# Get all PASM2 YAML files
pasm2_dir = 'engineering/knowledge-base/P2/language/pasm2/'
yaml_files = glob.glob(f'{pasm2_dir}*.yaml')

print(f"Surveying {len(yaml_files)} PASM2 YAML files...")

# Count keys across all files
key_counter = Counter()
file_count = 0

for yaml_file in yaml_files:
    try:
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
            if data and isinstance(data, dict):
                file_count += 1
                for key in data.keys():
                    key_counter[key] += 1
    except Exception as e:
        print(f"Error reading {yaml_file}: {e}")

print(f"\nSuccessfully processed {file_count} files")
print("\n=== KEY FREQUENCY ANALYSIS ===")
print(f"{'Count':<8} {'Percent':<8} {'Key'}")
print("-" * 50)

# Sort by frequency
for key, count in key_counter.most_common():
    percent = (count / file_count * 100) if file_count > 0 else 0
    print(f"{count:<8} {percent:6.1f}%  {key}")
    
# Identify outliers
print("\n=== STANDARD vs NON-STANDARD KEYS ===")
standard_threshold = file_count * 0.8  # Keys in 80%+ of files are "standard"
standard_keys = [k for k, c in key_counter.items() if c >= standard_threshold]
occasional_keys = [k for k, c in key_counter.items() if c >= file_count * 0.1 and c < standard_threshold]
rare_keys = [k for k, c in key_counter.items() if c < file_count * 0.1]

print(f"\nStandard keys (80%+ files): {', '.join(standard_keys)}")
print(f"\nOccasional keys (10-80% files): {', '.join(occasional_keys)}")
print(f"\nRare keys (<10% files): {', '.join(rare_keys)}")

# Check for problematic duplicates
print("\n=== DUPLICATE/CONFLICTING KEYS ===")
if 'group' in key_counter and 'category' in key_counter:
    print(f"WARNING: Both 'group' ({key_counter['group']} files) and 'category' ({key_counter['category']} files) exist")
    
print("\n=== KEY PATTERNS ===")
# Look for patterns like compiler_ prefix
compiler_keys = [k for k in key_counter.keys() if k.startswith('compiler_')]
manual_keys = [k for k in key_counter.keys() if 'manual' in k.lower()]
enhancement_keys = [k for k in key_counter.keys() if 'enhancement' in k.lower()]

if compiler_keys:
    print(f"Compiler-prefixed keys: {', '.join(compiler_keys)}")
if manual_keys:
    print(f"Manual-related keys: {', '.join(manual_keys)}")
if enhancement_keys:
    print(f"Enhancement keys: {', '.join(enhancement_keys)}")