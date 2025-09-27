#!/usr/bin/env python3
"""
Build complete PASM2 manifest with all instruction files properly referenced.
Groups instructions by their category field.
"""

import yaml
from pathlib import Path
from collections import defaultdict

# Paths
pasm2_dir = Path("engineering/knowledge-base/P2/language/pasm2")
manifest_path = Path("manifests/P2/language/pasm2-manifest.yaml")

# Read the existing manifest to preserve structure
with open(manifest_path, 'r') as f:
    manifest = yaml.safe_load(f)

# Group all YAML files by category
categories = defaultdict(list)
total_files = 0

for yaml_file in sorted(pasm2_dir.glob("*.yaml")):
    try:
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
        
        if not data:
            continue
        
        # Get category and oneliner
        category = data.get('category', 'misc_ops')
        oneliner = data.get('oneliner', 'No description available')
        instruction = data.get('instruction', yaml_file.stem.upper())
        
        # Special handling for non-instructions
        if category in ['Assembly Directive', 'Numeric Constant', 'Predefined Constant', 'Special Registers']:
            # These go in their special sections
            continue
        
        # Add to category list
        categories[category].append({
            'name': yaml_file.stem,
            'content': yaml_file.name,
            'desc': oneliner
        })
        total_files += 1
        
    except Exception as e:
        print(f"Error processing {yaml_file.name}: {e}")

# Update manifest categories section
if 'categories' not in manifest:
    manifest['categories'] = {}

# Update each category with its items
for category_name, items in sorted(categories.items()):
    if category_name not in manifest['categories']:
        manifest['categories'][category_name] = {}
    
    # Update the category entry
    cat_entry = manifest['categories'][category_name]
    cat_entry['count'] = len(items)
    cat_entry['items'] = sorted(items, key=lambda x: x['name'])
    
    # Remove old manifest reference if it exists
    if 'manifest' in cat_entry:
        del cat_entry['manifest']
    
    # Keep description if it exists, otherwise add default
    if 'description' not in cat_entry:
        cat_entry['description'] = f"{category_name.replace('_', ' ').title()} operations"

# Handle special sections (directives, constants, special_registers)
# These are already properly structured in the backup, just need to ensure they're preserved

print(f"Categorized {total_files} instruction files into {len(categories)} categories")
print("\nCategories and counts:")
for cat, items in sorted(categories.items()):
    print(f"  {cat:20} {len(items):3} instructions")

# Update total count
manifest['total_instructions'] = total_files + 15  # +15 for directives/constants/special_registers

# Write updated manifest
with open(manifest_path, 'w') as f:
    yaml.dump(manifest, f, default_flow_style=False, sort_keys=False, width=120)

print(f"\nManifest updated at {manifest_path}")
print(f"Total entries: {manifest['total_instructions']}")