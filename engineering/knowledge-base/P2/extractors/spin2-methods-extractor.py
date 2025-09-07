#!/usr/bin/env python3
"""
Extract Spin2 methods from complete-spin2-methods.md
"""

from pathlib import Path
import re

def extract_spin2_methods():
    """Extract Spin2 built-in methods"""
    
    # Paths
    source_path = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/spin2-v51/complete-spin2-methods.md")
    spin2_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/spin2")
    
    # Read source
    with open(source_path, 'r') as f:
        content = f.read()
    
    methods = []
    current_category = None
    
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Category headers
        if line.startswith('### '):
            current_category = line.replace('###', '').strip()
        
        # Method signatures in code blocks
        elif line.strip() and not line.startswith('#') and not line.startswith('```'):
            # Look for method signatures
            if '(' in line and ')' in line:
                # Extract method name and signature
                match = re.match(r'^(\w+)(\([^)]*\))(.*)$', line.strip())
                if match:
                    name = match.group(1)
                    params = match.group(2)
                    returns = match.group(3).strip()
                    
                    # Look for description on next line
                    description = ""
                    if i + 1 < len(lines) and lines[i + 1].strip().startswith("'"):
                        description = lines[i + 1].strip().lstrip("'").strip()
                        i += 1
                    
                    methods.append({
                        'name': name,
                        'signature': line.strip(),
                        'params': params,
                        'returns': returns,
                        'description': description,
                        'category': current_category or 'General'
                    })
        
        i += 1
    
    # Write YAML files for each method
    created = 0
    for method in methods:
        yaml_path = spin2_dir / f"spin2_{method['name'].lower()}.yaml"
        
        yaml_content = f"""name: {method['name']}
type: method
category: {method['category']}
signature: "{method['signature']}"
description: "{method['description']}"
source: Spin2 Documentation v51
"""
        
        with open(yaml_path, 'w') as f:
            f.write(yaml_content)
        
        created += 1
        print(f"Created: {method['name']}")
    
    print(f"\nComplete:")
    print(f"  Created: {created} method files")

if __name__ == "__main__":
    extract_spin2_methods()