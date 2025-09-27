#!/usr/bin/env python3
"""Survey all keys across PASM2 instruction files to understand field usage patterns"""

import os
import yaml
from collections import Counter
from pathlib import Path

# Path to PASM2 instruction files
pasm2_dir = Path("engineering/knowledge-base/P2/language/pasm2")

# Collect all YAML files
yaml_files = list(pasm2_dir.glob("*.yaml"))
print(f"Found {len(yaml_files)} YAML files in {pasm2_dir}\n")

# Counter for all keys across all files
key_counter = Counter()
key_samples = {}  # Store sample values for each key

# Process each file
for yaml_file in yaml_files:
    try:
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
            if data:
                for key in data.keys():
                    key_counter[key] += 1
                    # Store a sample value if we haven't seen this key before
                    if key not in key_samples and data[key]:
                        # Truncate long values for display
                        value = str(data[key])
                        if len(value) > 100:
                            value = value[:97] + "..."
                        key_samples[key] = (yaml_file.name, value)
    except Exception as e:
        print(f"Error reading {yaml_file.name}: {e}")

# Display results
print("=" * 80)
print("KEY USAGE SUMMARY ACROSS ALL PASM2 FILES")
print("=" * 80)
print(f"\nTotal unique keys found: {len(key_counter)}\n")

print("Key frequency (sorted by count):")
print("-" * 80)

for key, count in sorted(key_counter.items(), key=lambda x: (-x[1], x[0])):
    percentage = (count / len(yaml_files)) * 100
    print(f"{key:30} {count:4} files ({percentage:6.1f}%)")
    if key in key_samples:
        filename, sample = key_samples[key]
        print(f"  Sample from {filename}: {sample[:70]}")
    print()

print("\n" + "=" * 80)
print("ANALYSIS SUMMARY")
print("=" * 80)

# Identify core fields (present in >90% of files)
core_fields = [k for k, v in key_counter.items() if v > len(yaml_files) * 0.9]
print(f"\nCore fields (>90% presence): {', '.join(core_fields) if core_fields else 'None'}")

# Identify common fields (50-90%)
common_fields = [k for k, v in key_counter.items() 
                 if len(yaml_files) * 0.5 <= v <= len(yaml_files) * 0.9]
print(f"\nCommon fields (50-90%): {', '.join(common_fields) if common_fields else 'None'}")

# Identify rare fields (<10%)
rare_fields = [k for k, v in key_counter.items() if v < len(yaml_files) * 0.1]
print(f"\nRare fields (<10%): {', '.join(rare_fields) if rare_fields else 'None'}")

# Check for problematic patterns
print("\n" + "=" * 80)
print("PROBLEMS IDENTIFIED")
print("=" * 80)

# Files with both group and category
both_group_category = 0
for yaml_file in yaml_files:
    try:
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
            if data and 'group' in data and 'category' in data:
                both_group_category += 1
    except:
        pass

print(f"\nFiles with BOTH 'group' and 'category': {both_group_category}")

# Check for description field variations
desc_variations = [k for k in key_counter.keys() if 'desc' in k.lower()]
print(f"\nDescription field variations found: {', '.join(desc_variations)}")

# Check for related/see_also variations
related_variations = [k for k in key_counter.keys() if 'related' in k or 'see' in k]
print(f"\nRelated/see_also variations: {', '.join(related_variations)}")