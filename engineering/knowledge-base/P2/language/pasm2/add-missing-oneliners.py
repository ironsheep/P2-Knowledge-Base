#!/usr/bin/env python3
"""
Add oneliners to PASM2 files that are missing them.
Extract from description field, taking first sentence.
"""

import yaml
import re
from pathlib import Path

def extract_oneliner_from_description(desc):
    """Extract first sentence from description as oneliner"""
    if not desc:
        return None
    
    # Convert to string and clean up
    desc = str(desc).strip()
    
    # Remove common prefixes
    desc = re.sub(r'^(This instruction |The \w+ instruction )', '', desc, flags=re.I)
    
    # Find first sentence (ending with . or newline)
    match = re.match(r'^([^.\n]+)', desc)
    if match:
        oneliner = match.group(1).strip()
        
        # Clean up common patterns
        oneliner = oneliner.replace('\\n', ' ')
        oneliner = re.sub(r'\s+', ' ', oneliner)
        
        # Truncate if too long
        if len(oneliner) > 80:
            # Try to break at a natural point
            if ',' in oneliner[:80]:
                oneliner = oneliner[:oneliner.rindex(',', 0, 80)]
            elif ' ' in oneliner[:80]:
                oneliner = oneliner[:oneliner.rindex(' ', 0, 80)]
            else:
                oneliner = oneliner[:77] + '...'
        
        return oneliner
    
    return None

# Process all YAML files
yaml_files = sorted(list(Path('.').glob('*.yaml')))
print(f"Checking {len(yaml_files)} PASM2 files for missing oneliners...\n")

fixed = 0
already_has = 0
no_description = 0

for yaml_file in yaml_files:
    try:
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
        
        if not data:
            continue
        
        if 'oneliner' in data:
            already_has += 1
            continue
        
        # Try to extract from description
        if 'description' in data:
            oneliner = extract_oneliner_from_description(data['description'])
            if oneliner:
                data['oneliner'] = oneliner
                with open(yaml_file, 'w') as f:
                    yaml.dump(data, f, default_flow_style=False, sort_keys=False, width=120)
                print(f"Added oneliner to {yaml_file.name}: {oneliner[:60]}...")
                fixed += 1
            else:
                print(f"WARNING: Could not extract oneliner from {yaml_file.name}")
        else:
            no_description += 1
            print(f"ERROR: {yaml_file.name} has no description field")
    
    except Exception as e:
        print(f"Error processing {yaml_file.name}: {e}")

print(f"\n{'='*60}")
print(f"SUMMARY:")
print(f"  Already had oneliner: {already_has}")
print(f"  Added oneliner: {fixed}")
print(f"  No description field: {no_description}")
print(f"  Total with oneliners now: {already_has + fixed}")