#!/usr/bin/env python3
"""
Extract Spin2 operators from complete-spin2-operators.md
"""

from pathlib import Path
import re

def extract_spin2_operators():
    """Extract Spin2 operators"""
    
    # Paths
    source_path = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/spin2-v51/complete-spin2-operators.md")
    spin2_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/spin2")
    
    # Read source
    with open(source_path, 'r') as f:
        content = f.read()
    
    # Parse operator table
    operators = []
    in_table = False
    
    for line in content.split('\n'):
        if '| Priority |' in line:
            in_table = True
            continue
        
        if in_table and line.startswith('|'):
            if '---' in line or 'Priority' in line:
                continue
                
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 6:
                priority = parts[1].replace('**', '').strip()
                if priority and priority not in ['Priority', 'Lowest']:
                    ops = parts[2].strip()
                    op_type = parts[3].strip()
                    description = parts[4].strip()
                    
                    # Parse individual operators
                    for op in ops.split():
                        op = op.strip('`')
                        if op:
                            operators.append({
                                'operator': op,
                                'priority': priority,
                                'type': op_type,
                                'description': description
                            })
    
    # Write YAML files
    created = 0
    for op in operators:
        # Create safe filename
        safe_name = op['operator'].replace('++', 'inc').replace('--', 'dec').replace('??', 'rand')
        safe_name = safe_name.replace('!', 'not').replace('||', 'encode').replace('^^', 'decode')
        safe_name = safe_name.replace('>>', 'shr').replace('<<', 'shl').replace('&', 'and')
        safe_name = safe_name.replace('^', 'xor').replace('|', 'or').replace('*', 'mul')
        safe_name = safe_name.replace('/', 'div').replace('+', 'add').replace('-', 'sub')
        safe_name = safe_name.replace('#>', 'max').replace('<#', 'min').replace('<', 'lt')
        safe_name = safe_name.replace('>', 'gt').replace('=', 'eq').replace(':', 'colon')
        safe_name = safe_name.replace('?', 'question').replace('.', 'dot')
        
        yaml_path = spin2_dir / f"spin2_op_{safe_name}.yaml"
        
        yaml_content = f"""name: "{op['operator']}"
type: operator
priority: {op['priority']}
category: {op['type']}
description: "{op['description']}"
source: Spin2 Documentation v51
"""
        
        with open(yaml_path, 'w') as f:
            f.write(yaml_content)
        
        created += 1
        print(f"Created: {op['operator']}")
    
    print(f"\nComplete:")
    print(f"  Created: {created} operator files")

if __name__ == "__main__":
    extract_spin2_operators()