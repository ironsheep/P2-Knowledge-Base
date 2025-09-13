#!/usr/bin/env python3
import json
import os
import yaml
from pathlib import Path

# Load JSON data
json_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/external-inputs/from-pnut-ts/SPIN2-Language-Specification.json"
with open(json_path) as f:
    data = json.load(f)

# Methods directory
methods_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/spin2/methods"

# Extract builtin functions from JSON
builtin_functions = data.get('builtinFunctions', [])
print(f"Found {len(builtin_functions)} builtin functions in JSON")

# Create a map of function names to their JSON data
json_functions = {}
for func in builtin_functions:
    name = func.get('name', '').lower()
    if name:
        json_functions[name] = func

# Process existing method files
enhanced_count = 0
already_good_count = 0

for filename in os.listdir(methods_dir):
    if not filename.endswith('.yaml'):
        continue
    
    filepath = os.path.join(methods_dir, filename)
    method_name = filename.replace('.yaml', '')
    
    # Load existing YAML
    with open(filepath) as f:
        content = f.read()
        try:
            existing_data = yaml.safe_load(content)
        except:
            print(f"Skipping {filename} - cannot parse YAML")
            continue
    
    # Check if we have JSON data for this method
    json_data = json_functions.get(method_name)
    
    if not json_data:
        # No JSON data for this method
        continue
    
    # Check if enhancement is needed
    needs_update = False
    updated_data = existing_data.copy()
    
    # Enhance with compiler metadata
    if not existing_data.get('syntax') and json_data.get('syntax'):
        updated_data['syntax'] = json_data['syntax']
        needs_update = True
    
    if not existing_data.get('category') and json_data.get('category'):
        updated_data['category'] = json_data['category']
        needs_update = True
    
    # Enhance description if JSON has better one
    if json_data.get('description'):
        json_desc = json_data['description']
        existing_desc = existing_data.get('description', '')
        if len(json_desc) > len(existing_desc) or not existing_desc:
            updated_data['description'] = json_desc
            needs_update = True
    
    # Add examples if missing
    if not existing_data.get('examples') and json_data.get('examples'):
        updated_data['examples'] = json_data['examples']
        needs_update = True
    
    if needs_update:
        # Write enhanced YAML
        yaml_content = yaml.dump(updated_data, default_flow_style=False, sort_keys=False, allow_unicode=True)
        with open(filepath, 'w') as f:
            f.write(yaml_content)
        enhanced_count += 1
        print(f"Enhanced: {filename}")
    else:
        already_good_count += 1

print(f"\nEnhancement complete:")
print(f"  Enhanced: {enhanced_count} files")
print(f"  Already good: {already_good_count} files")
print(f"  No JSON match: {len(os.listdir(methods_dir)) - enhanced_count - already_good_count - 1} files")  # -1 for AUDIT-REPORT.md