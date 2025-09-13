#!/usr/bin/env python3
import json
import os

# Load JSON data
json_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/external-inputs/from-pnut-ts/SPIN2-Language-Specification.json"
with open(json_path) as f:
    data = json.load(f)

# Output directory  
output_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/spin2/registers"

# Extract registers from JSON
registers = data.get('registers', [])
print(f"Found {len(registers)} registers in JSON")

# Create YAML file for each register
for register in registers:
    name = register.get('name', 'UNKNOWN')
    category = register.get('category', 'Register')
    description = register.get('description', 'No description')
    syntax = register.get('syntax', '')
    examples = register.get('examples', [])
    
    # Build YAML content
    yaml_content = f'''register: "{name}"
type: register
category: "{category}"
description: |
  {description}'''
    
    if syntax:
        yaml_content += f'\nsyntax: "{syntax}"'
    
    if examples:
        yaml_content += '\nexamples:'
        for example in examples:
            # Escape the example properly
            example_escaped = example.replace('"', '\\"')
            yaml_content += f'\n  - "{example_escaped}"'
    
    # Add additional register-specific fields if available
    if register.get('address'):
        yaml_content += f"\naddress: \"{register['address']}\""
    if register.get('access'):
        yaml_content += f"\naccess: \"{register['access']}\""
    if register.get('bits'):
        yaml_content += f"\nbits: {register['bits']}"
    
    # Create filename
    filename = f"{name.lower()}.yaml"
    filepath = os.path.join(output_dir, filename)
    
    # Write the file
    with open(filepath, 'w') as f:
        f.write(yaml_content)
    
    print(f"Created: {filename}")

print(f"\nSuccessfully created {len(registers)} register YAML files")