#!/usr/bin/env python3
import json
import os

# Load JSON data
json_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/external-inputs/from-pnut-ts/SPIN2-Language-Specification.json"
with open(json_path) as f:
    data = json.load(f)

# Output directory  
output_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/spin2/special-symbols"

# Extract special symbols from JSON
symbols = data.get('specialSymbols', [])
print(f"Found {len(symbols)} special symbols in JSON")

# Create YAML file for each special symbol
for symbol in symbols:
    symbol_char = symbol.get('symbol', 'UNKNOWN')
    category = symbol.get('category', 'Special')
    description = symbol.get('description', 'No description')
    syntax = symbol.get('syntax', '')
    examples = symbol.get('examples', [])
    context = symbol.get('context', '')
    
    # Build YAML content
    yaml_content = f'''symbol: "{symbol_char}"
type: special_symbol
category: "{category}"
description: |
  {description}'''
    
    if syntax:
        yaml_content += f'\nsyntax: "{syntax}"'
    
    if context:
        yaml_content += f'\ncontext: "{context}"'
    
    if examples:
        yaml_content += '\nexamples:'
        for example in examples:
            # Escape the example properly
            example_escaped = example.replace('"', '\\"')
            yaml_content += f'\n  - "{example_escaped}"'
    
    # Create filename - map special characters to safe names
    filename_map = {
        '$': 'dollar',
        '$$': 'double_dollar',
        '@': 'at',
        '@@': 'double_at',
        '#': 'hash',
        '##': 'double_hash',
        '_': 'underscore',
        '\\': 'backslash',
        '%': 'percent',
        '%%': 'double_percent',
        '..': 'double_dot',
        '...': 'triple_dot'
    }
    
    filename_base = filename_map.get(symbol_char, symbol_char.replace(' ', '_').replace('/', '_'))
    filename = f"{filename_base}.yaml"
    filepath = os.path.join(output_dir, filename)
    
    # Write the file
    with open(filepath, 'w') as f:
        f.write(yaml_content)
    
    print(f"Created: {filename} for symbol '{symbol_char}'")

print(f"\nSuccessfully created {len(symbols)} special symbol YAML files")