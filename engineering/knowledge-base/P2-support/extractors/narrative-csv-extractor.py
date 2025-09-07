#!/usr/bin/env python3
"""
Layer 3: Extract narrative descriptions from P2 Instructions CSV
"""

import csv
from pathlib import Path

def extract_narratives():
    """Extract instruction descriptions from CSV"""
    
    # Paths
    csv_path = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv")
    pasm2_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/instructions/pasm2")
    
    # Read CSV
    instructions = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Get instruction mnemonic from syntax column
            syntax = row.get("#S = immediate (I=1). S = register.\n#D = immediate (L=1). D = register.\n\n- Assembly Syntax -", "").strip()
            if not syntax:
                continue
                
            # Extract mnemonic (first word)
            parts = syntax.split()
            if not parts:
                continue
            mnemonic = parts[0].upper()
            
            # Get description - it's in a column with complex header
            description = row.get("* Z = (result == 0).\n** If #S and cogex, PC += signed(S). If #S and hubex, PC += signed(S*4). If S, PC = register S.\n\n- Description -", "").strip()
            
            if mnemonic and description:
                instructions.append({
                    'mnemonic': mnemonic,
                    'syntax': syntax,
                    'description': description
                })
    
    # Update YAML files
    updated = 0
    no_file = 0
    
    for inst in instructions:
        yaml_path = pasm2_dir / f"pasm2_{inst['mnemonic'].lower()}.yaml"
        
        if not yaml_path.exists():
            no_file += 1
            print(f"No file for: {inst['mnemonic']}")
            continue
            
        # Read existing YAML
        with open(yaml_path, 'r') as f:
            content = f.read()
        
        # Check if layer3_narrative already exists
        if 'layer3_narrative:' in content:
            continue
            
        # Add layer3_narrative section
        desc = inst['description'].replace('"', '\\"')
        syn = inst['syntax'].replace('"', '\\"')
        narrative_section = f"""
layer3_narrative:
  source: P2 Instructions CSV v35
  description: "{desc}"
  syntax: "{syn}"
"""
        
        # Append to file
        with open(yaml_path, 'a') as f:
            f.write(narrative_section)
        
        updated += 1
        print(f"Updated: {inst['mnemonic']}")
    
    print(f"\nComplete:")
    print(f"  Updated: {updated}")
    print(f"  No file found: {no_file}")
    print(f"  Total instructions in CSV: {len(instructions)}")

if __name__ == "__main__":
    extract_narratives()