#!/usr/bin/env python3
import json
import os

# Load JSON data
json_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/external-inputs/from-pnut-ts/SPIN2-Language-Specification.json"
with open(json_path) as f:
    data = json.load(f)

# Output directory  
output_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/spin2/system-variables"

# Extract system variables from JSON
variables = data.get('systemVariables', [])
print(f"Found {len(variables)} system variables in JSON")

# Create YAML file for each system variable
for variable in variables:
    name = variable.get('name', 'UNKNOWN')
    data_type = variable.get('dataType', 'Unknown')
    description = variable.get('description', 'No description')
    access = variable.get('access', '')
    examples = variable.get('examples', [])
    scope = variable.get('scope', '')
    
    # Build YAML content
    yaml_content = f'''variable: "{name}"
type: system_variable
data_type: "{data_type}"
description: |
  {description}'''
    
    if access:
        yaml_content += f'\naccess: "{access}"'
    
    if scope:
        yaml_content += f'\nscope: "{scope}"'
    
    if examples:
        yaml_content += '\nexamples:'
        for example in examples:
            # Escape the example properly
            example_escaped = example.replace('"', '\\"')
            yaml_content += f'\n  - "{example_escaped}"'
    
    # Add notes if available
    if variable.get('notes'):
        yaml_content += f"\nnotes: |\n  {variable['notes']}"
    
    # Create filename
    filename = f"{name.lower()}.yaml"
    filepath = os.path.join(output_dir, filename)
    
    # Write the file
    with open(filepath, 'w') as f:
        f.write(yaml_content)
    
    print(f"Created: {filename}")

print(f"\nSuccessfully created {len(variables)} system variable YAML files")