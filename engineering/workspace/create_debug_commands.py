#!/usr/bin/env python3
import json
import os

# Load JSON data
json_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/external-inputs/from-pnut-ts/SPIN2-Language-Specification.json"
with open(json_path) as f:
    data = json.load(f)

# Output directory  
output_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/spin2/debug-commands"

# Extract debug commands from JSON
commands = data.get('debugCommands', [])
print(f"Found {len(commands)} debug commands in JSON")

# Create YAML file for each debug command
for command in commands:
    name = command.get('name', 'UNKNOWN')
    category = command.get('category', 'Debug')
    description = command.get('description', 'No description')
    syntax = command.get('syntax', '')
    examples = command.get('examples', [])
    
    # Build YAML content
    yaml_content = f'''command: "{name}"
type: debug_command
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
    
    # Add additional debug-specific fields if available
    if command.get('format'):
        yaml_content += f"\nformat: \"{command['format']}\""
    if command.get('output'):
        yaml_content += f"\noutput: \"{command['output']}\""
    
    # Create filename - handle special characters
    filename_base = name.lower().replace(' ', '_').replace('`', '').replace('.', '_')
    filename = f"{filename_base}.yaml"
    filepath = os.path.join(output_dir, filename)
    
    # Write the file
    with open(filepath, 'w') as f:
        f.write(yaml_content)
    
    print(f"Created: {filename}")

print(f"\nSuccessfully created {len(commands)} debug command YAML files")