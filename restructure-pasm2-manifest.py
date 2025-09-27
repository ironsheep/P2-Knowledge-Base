#!/usr/bin/env python3
"""Restructure PASM2 manifest to flatten categories and use direct content references."""

import yaml
import os
import glob

# Read current manifest
with open('manifests/P2/language/pasm2-manifest.yaml', 'r') as f:
    manifest = yaml.safe_load(f)

# Get all PASM2 files
pasm2_dir = 'engineering/knowledge-base/P2/language/pasm2/'
yaml_files = glob.glob(f'{pasm2_dir}*.yaml')

# Build categories from actual files
categories_by_type = {}

for yaml_file in yaml_files:
    filename = os.path.basename(yaml_file)
    try:
        with open(yaml_file, 'r') as f:
            content = yaml.safe_load(f)
            category = content.get('category', 'Unknown')
            name = content.get('name', filename.replace('.yaml', ''))
            desc = content.get('description', '').split('\n')[0][:100]  # First line, max 100 chars
            
            # Normalize category names for use as keys
            cat_key = category.lower().replace(' ', '_').replace('-', '_').strip('_')
            
            if cat_key not in categories_by_type:
                categories_by_type[cat_key] = {
                    'description': category,
                    'items': []
                }
            
            categories_by_type[cat_key]['items'].append({
                'name': name.lower(),
                'content': filename,
                'desc': desc
            })
    except Exception as e:
        print(f"Error processing {yaml_file}: {e}")

# Sort items within each category
for cat in categories_by_type.values():
    cat['items'].sort(key=lambda x: x['name'])

# Build new manifest structure
new_manifest = {
    'version': manifest.get('version', '2.0'),
    'schema_version': manifest.get('schema_version'),
    'last_updated': manifest.get('last_updated'),
    'category': manifest.get('category'),
    'base_path': manifest.get('base_path'),
    'structure': 'flat',  # Changed from hierarchical
    'total_instructions': len(yaml_files),
    'description': manifest.get('description'),
    'categories': categories_by_type,
    'quick_lookup': manifest.get('quick_lookup', {})
}

# Write new manifest
output_file = 'manifests/P2/language/pasm2-manifest-flat.yaml'
with open(output_file, 'w') as f:
    yaml.dump(new_manifest, f, default_flow_style=False, sort_keys=False, width=120)

print(f"Created flattened manifest at {output_file}")
print(f"Total categories: {len(categories_by_type)}")
for cat_key, cat_data in sorted(categories_by_type.items()):
    print(f"  {cat_key}: {len(cat_data['items'])} items")