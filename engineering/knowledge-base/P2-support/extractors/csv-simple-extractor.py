#!/usr/bin/env python3
"""
Simple CSV extractor that handles the actual format
"""

import csv
import re
from pathlib import Path
from datetime import datetime

def extract_csv_data():
    csv_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv"
    output_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/instructions/pasm2")
    
    updated = 0
    created = 0
    errors = 0
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row_num, row in enumerate(reader, start=2):
            try:
                # Get the assembly syntax column (has the long multiline header)
                syntax = row.get("#S = immediate (I=1). S = register.\n#D = immediate (L=1). D = register.\n\n- Assembly Syntax -", "").strip()
                
                if not syntax or syntax == "" or "Assembly Syntax" in syntax:
                    continue
                
                # Extract mnemonic
                syntax_clean = re.sub(r'\{[^}]+\}', '', syntax).strip()
                parts = syntax_clean.split()
                if not parts:
                    continue
                    
                mnemonic = parts[0].upper()
                mnemonic = re.sub(r'[^\w_]', '', mnemonic)
                
                # Get other fields
                group = row.get("- Group -", "").strip()
                encoding = row.get("- Encoding -", "").strip()
                alias = row.get("- Alias -", "").strip()
                description = row.get("* Z = (result == 0).\n** If #S and cogex, PC += signed(S). If #S and hubex, PC += signed(S*4). If S, PC = register S.\n\n- Description -", "").strip()
                interrupt = row.get("Next Inst\nShielded\nfrom\nInterrupt", "").strip()
                
                # Timing columns
                cog_exec_8 = row.get("Clock Cycles (8 cogs)\n\n- Cog Exec Mode -\n- LUT Exec Mode -", "").strip()
                cog_exec_16 = row.get("Clock Cycles (16 cogs)\n\n- Cog Exec Mode -\n- LUT Exec Mode -", "").strip()
                
                # Generate filename
                if mnemonic.startswith('_'):
                    filename = f"pasm2{mnemonic.lower()}.yaml"
                else:
                    filename = f"pasm2_{mnemonic.lower()}.yaml"
                
                filepath = output_dir / filename
                
                # Parse timing
                def parse_timing(t):
                    if not t:
                        return None
                    m = re.search(r'(\d+)', t)
                    return int(m.group(1)) if m else None
                
                cog8_timing = parse_timing(cog_exec_8)
                cog16_timing = parse_timing(cog_exec_16)
                
                # Build layer1 content
                layer1_content = f"""metadata:
  id: pasm2_{mnemonic.lower()}
  version: 1.0
  extraction_date: |
    {datetime.now().isoformat()}
  source:
    document: P2 Instructions v35
    type: csv
    row: {row_num}
layer1_csv:
  mnemonic: {mnemonic}
  syntax: |
    {syntax}
  group: {group if group else 'null'}
  encoding: {encoding if encoding else 'null'}
  alias: {alias if alias and alias != '-' else 'null'}
  description: {description if description else 'null'}
  interrupt_shield: {str(interrupt == 'Yes').lower()}
  timing:
    cog_exec_8_cogs: {cog8_timing if cog8_timing else 'null'}
    cog_exec_16_cogs: {cog16_timing if cog16_timing else 'null'}
"""
                
                # Update or create file
                if filepath.exists():
                    # Read existing content
                    with open(filepath, 'r') as f:
                        existing = f.read()
                    
                    # Simple approach: if layer1_csv exists, replace it; otherwise append
                    if 'layer1_csv:' in existing:
                        # Find and replace layer1 section
                        lines = existing.split('\n')
                        new_lines = []
                        skip = False
                        
                        for line in lines:
                            if line.startswith('layer1_csv:'):
                                skip = True
                                # Add our new layer1
                                new_lines.extend(layer1_content.split('\n')[7:])  # Skip metadata part
                            elif line.startswith('layer2_') or line.startswith('layer3_') or line.startswith('layer4_'):
                                skip = False
                                new_lines.append(line)
                            elif not skip:
                                new_lines.append(line)
                        
                        with open(filepath, 'w') as f:
                            f.write('\n'.join(new_lines))
                        updated += 1
                    else:
                        # Append layer1 to existing file
                        with open(filepath, 'a') as f:
                            f.write('\n' + '\n'.join(layer1_content.split('\n')[7:]))
                        updated += 1
                else:
                    # Create new file
                    with open(filepath, 'w') as f:
                        f.write(layer1_content)
                    created += 1
                    
                print(f"Processed: {mnemonic} ({filename})")
                
            except Exception as e:
                errors += 1
                print(f"Error on row {row_num}: {e}")
    
    print(f"\nComplete:")
    print(f"  Updated: {updated}")
    print(f"  Created: {created}")
    print(f"  Errors: {errors}")

if __name__ == "__main__":
    extract_csv_data()