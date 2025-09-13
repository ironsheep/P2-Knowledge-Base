#!/usr/bin/env python3
import json
import os

# Load JSON data
json_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/external-inputs/from-pnut-ts/SPIN2-Language-Specification.json"
with open(json_path) as f:
    data = json.load(f)

# Output directory
output_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/spin2/assembly-directives"

# Extract assembly directives from JSON
directives = data.get('assemblyDirectives', [])
print(f"Found {len(directives)} assembly directives in JSON")

# Create YAML file for each directive
for directive in directives:
    name = directive.get('name', 'UNKNOWN')
    category = directive.get('category', 'Assembly')
    description = directive.get('description', 'No description')
    syntax = directive.get('syntax', '')
    examples = directive.get('examples', [])
    
    # Build YAML content
    yaml_content = f'''directive: "{name}"
type: assembly_directive
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
    
    # Create filename
    filename = f"{name.lower()}.yaml"
    filepath = os.path.join(output_dir, filename)
    
    # Write the file
    with open(filepath, 'w') as f:
        f.write(yaml_content)
    
    print(f"Created: {filename}")

print(f"\nSuccessfully created {len(directives)} assembly directive YAML files")