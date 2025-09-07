#!/usr/bin/env python3
"""
Independent verification of instruction counts from multiple sources
"""

import csv
import re
from pathlib import Path

def count_all_sources():
    """Count instructions from all available sources independently"""
    
    counts = {}
    
    # 1. Count from CSV file
    csv_path = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv")
    csv_instructions = set()
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            syntax = row.get("#S = immediate (I=1). S = register.\n#D = immediate (L=1). D = register.\n\n- Assembly Syntax -", "").strip()
            if syntax:
                parts = syntax.split()
                if parts:
                    mnemonic = parts[0].upper()
                    # Skip obvious conditionals
                    if not any(x in mnemonic for x in ['IF_', '_RET_', '<']):
                        csv_instructions.add(mnemonic)
    
    counts['CSV'] = len(csv_instructions)
    
    # 2. Count from P2 Datasheet markdown tables
    datasheet_path = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/p2-datasheet/pasm2-complete-instruction-tables.md")
    datasheet_instructions = set()
    
    with open(datasheet_path, 'r') as f:
        for line in f:
            if line.startswith('| **') and '|' in line:
                match = re.match(r'\| \*\*([A-Z][A-Z0-9_]*)', line)
                if match:
                    mnemonic = match.group(1)
                    # Skip conditionals
                    if not any(x in mnemonic for x in ['IF_', '_RET_']):
                        datasheet_instructions.add(mnemonic)
    
    counts['Datasheet'] = len(datasheet_instructions)
    
    # 3. Count actual YAML files
    yaml_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/instructions/pasm2")
    yaml_files = list(yaml_dir.glob("pasm2_*.yaml"))
    yaml_instructions = set()
    
    for f in yaml_files:
        inst_name = f.stem.replace('pasm2_', '').upper()
        yaml_instructions.add(inst_name)
    
    counts['YAML Files'] = len(yaml_instructions)
    
    # 4. Check Spin2 documentation for PASM2 references
    spin2_doc = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/spin2-doc/Spin2_Language_Documentation_v35_Unblocked.md")
    if spin2_doc.exists():
        with open(spin2_doc, 'r') as f:
            content = f.read()
            # Look for PASM instruction list if present
            pasm_section = re.search(r'PASM2? Instructions.*?(?=\n#|\Z)', content, re.DOTALL)
            if pasm_section:
                spin2_pasm = set(re.findall(r'\b([A-Z][A-Z0-9_]+)\b', pasm_section.group()))
                # Filter to likely instructions
                spin2_pasm = {x for x in spin2_pasm if len(x) >= 2 and len(x) <= 10}
                counts['Spin2 Doc PASM refs'] = len(spin2_pasm)
    
    # Compare sets
    print("=" * 60)
    print("INDEPENDENT INSTRUCTION COUNT VERIFICATION")
    print("=" * 60)
    
    print("\nSource Counts:")
    for source, count in counts.items():
        print(f"  {source:20} : {count:4} instructions")
    
    # Find common core
    if len(counts) >= 3:
        common = csv_instructions & datasheet_instructions & yaml_instructions
        print(f"\nCommon to all three : {len(common):4} instructions")
        
        # Find discrepancies
        csv_only = csv_instructions - datasheet_instructions - yaml_instructions
        datasheet_only = datasheet_instructions - csv_instructions - yaml_instructions
        yaml_only = yaml_instructions - csv_instructions - datasheet_instructions
        
        if csv_only:
            print(f"\nOnly in CSV ({len(csv_only)}):")
            for inst in sorted(csv_only)[:10]:
                print(f"  {inst}")
            if len(csv_only) > 10:
                print(f"  ... and {len(csv_only) - 10} more")
        
        if datasheet_only:
            print(f"\nOnly in Datasheet ({len(datasheet_only)}):")
            for inst in sorted(datasheet_only)[:10]:
                print(f"  {inst}")
            if len(datasheet_only) > 10:
                print(f"  ... and {len(datasheet_only) - 10} more")
        
        if yaml_only:
            print(f"\nOnly in YAML ({len(yaml_only)}):")
            for inst in sorted(yaml_only)[:10]:
                print(f"  {inst}")
            if len(yaml_only) > 10:
                print(f"  ... and {len(yaml_only) - 10} more")
    
    # Final reconciliation
    print("\n" + "=" * 60)
    print("FINAL ASSESSMENT:")
    print("=" * 60)
    
    # Remove known non-instructions from CSV
    filtered_csv = csv_instructions - {'C', 'NC', 'Z', 'NZ', 'CLR', 'EMPTY', 'INST', 'SET'}
    filtered_csv = {x for x in filtered_csv if not x.startswith('_')}
    
    print(f"\nCSV after filtering conditionals: {len(filtered_csv)}")
    print(f"Current YAML files:                {len(yaml_instructions)}")
    print(f"Datasheet tables:                  {len(datasheet_instructions)}")
    
    if len(yaml_instructions) == len(filtered_csv):
        print("\n✅ YAML count matches filtered CSV count!")
    else:
        print(f"\n⚠️  Discrepancy: {abs(len(yaml_instructions) - len(filtered_csv))} difference")
    
    return csv_instructions, datasheet_instructions, yaml_instructions

if __name__ == "__main__":
    csv_set, ds_set, yaml_set = count_all_sources()