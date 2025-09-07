#!/usr/bin/env python3
"""
PASM2 Instruction CSV Extractor - Updated for clean naming
Updates existing YAML files with Layer 1 CSV data
"""

import csv
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class InstructionExtractor:
    def __init__(self, csv_path: str, output_dir: str):
        self.csv_path = Path(csv_path)
        self.output_dir = Path(output_dir)
        self.instructions_dir = self.output_dir / "instructions" / "pasm2"
        self.audit_log = []
        self.mapping = {}
        self.instruction_count = 0
        self.error_count = 0
        self.updated_count = 0
        self.created_count = 0
        
    def parse_csv(self) -> List[Dict[str, Any]]:
        """Parse the CSV file and extract instruction data"""
        instructions = []
        
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                # Read raw lines to handle multi-line cells
                content = f.read()
                lines = content.split('\n')
                
                # Parse header
                reader = csv.DictReader(lines)
                
                for row_num, row in enumerate(reader, start=2):  # Start at 2 for 1-based + header
                    if self._is_instruction_row(row):
                        instruction = self._extract_instruction(row, row_num)
                        if instruction:
                            instructions.append(instruction)
                            
        except Exception as e:
            self.audit_log.append({
                'timestamp': datetime.now().isoformat(),
                'error': f"Failed to parse CSV: {str(e)}",
                'severity': 'critical'
            })
            
        return instructions
    
    def _is_instruction_row(self, row: Dict[str, str]) -> bool:
        """Check if row contains instruction data"""
        # Check for assembly syntax column
        syntax_col = row.get("#S = immediate (I=1). S = register.\n#D = immediate (L=1). D = register.\n\n- Assembly Syntax -", "")
        
        # Skip empty rows or header-like rows
        if not syntax_col or syntax_col.strip() == "":
            return False
            
        # Skip rows that are clearly headers or separators
        if "Assembly Syntax" in syntax_col or "---" in syntax_col:
            return False
            
        return True
    
    def _extract_instruction(self, row: Dict[str, str], row_num: int) -> Optional[Dict[str, Any]]:
        """Extract instruction data from CSV row"""
        try:
            # Map CSV columns to meaningful names
            syntax = row.get("#S = immediate (I=1). S = register.\n#D = immediate (L=1). D = register.\n\n- Assembly Syntax -", "").strip()
            group = row.get("- Group -", "").strip()
            encoding = row.get("- Encoding -", "").strip()
            alias = row.get("- Alias -", "").strip()
            description = row.get("* Z = (result == 0).\n** If #S and cogex, PC += signed(S). If #S and hubex, PC += signed(S*4). If S, PC = register S.\n\n- Description -", "").strip()
            interrupt_shield = row.get("Next Inst\nShielded\nfrom\nInterrupt", "").strip()
            
            # Extract timing information
            cog_exec_8 = row.get("Clock Cycles (8 cogs)\n\n- Cog Exec Mode -\n- LUT Exec Mode -", "").strip()
            hub_exec_8 = row.get("Clock Cycles (8 cogs)\n* +1 if crosses hub long\n\n- Hub Exec Mode -", "").strip()
            cog_exec_16 = row.get("Clock Cycles (16 cogs)\n\n- Cog Exec Mode -\n- LUT Exec Mode -", "").strip()
            hub_exec_16 = row.get("Clock Cyles (16 cogs)\n* +1 if crosses hub long", "").strip()
            
            # Parse instruction mnemonic from syntax
            mnemonic = self._extract_mnemonic(syntax)
            if not mnemonic:
                self.audit_log.append({
                    'row': row_num,
                    'issue': 'Could not extract mnemonic',
                    'syntax': syntax
                })
                return None
            
            # Generate clean instruction ID (no hash)
            instruction_id = self._generate_clean_id(mnemonic)
            
            # Build instruction structure
            instruction = {
                'metadata': {
                    'id': instruction_id,
                    'version': '1.0',
                    'extraction_date': datetime.now().isoformat(),
                    'source': {
                        'document': 'P2 Instructions v35',
                        'type': 'csv',
                        'row': row_num
                    }
                },
                'layer1_csv': {
                    'mnemonic': mnemonic,
                    'syntax': syntax,
                    'group': group if group else None,
                    'encoding': encoding if encoding else None,
                    'alias': alias if alias != '-' else None,
                    'description': description if description else None,
                    'interrupt_shield': interrupt_shield == 'Yes' if interrupt_shield else False,
                    'timing': {
                        'cog_exec_8_cogs': self._parse_timing(cog_exec_8),
                        'hub_exec_8_cogs': self._parse_timing(hub_exec_8),
                        'cog_exec_16_cogs': self._parse_timing(cog_exec_16),
                        'hub_exec_16_cogs': self._parse_timing(hub_exec_16)
                    }
                }
            }
            
            # Track mapping
            self.mapping[instruction_id] = {
                'csv_row': row_num,
                'mnemonic': mnemonic,
                'syntax': syntax
            }
            
            self.instruction_count += 1
            return instruction
            
        except Exception as e:
            self.error_count += 1
            self.audit_log.append({
                'row': row_num,
                'error': str(e),
                'severity': 'error'
            })
            return None
    
    def _extract_mnemonic(self, syntax: str) -> Optional[str]:
        """Extract instruction mnemonic from syntax string"""
        if not syntax:
            return None
            
        # Handle special cases
        syntax_clean = syntax.strip()
        
        # Remove condition codes and effects
        syntax_clean = re.sub(r'\{[^}]+\}', '', syntax_clean)
        
        # Extract first word as mnemonic
        parts = syntax_clean.split()
        if parts:
            mnemonic = parts[0].upper()
            # Remove any trailing punctuation
            mnemonic = re.sub(r'[^\w]', '', mnemonic)
            return mnemonic
            
        return None
    
    def _generate_clean_id(self, mnemonic: str) -> str:
        """Generate clean ID for instruction (no hash)"""
        # Handle special prefixes (condition codes)
        if mnemonic.startswith('_'):
            return f"pasm2{mnemonic.lower()}"
        else:
            return f"pasm2_{mnemonic.lower()}"
    
    def _parse_timing(self, timing_str: str) -> Optional[int]:
        """Parse timing information from string"""
        if not timing_str:
            return None
            
        # Extract numeric value
        match = re.search(r'(\d+)', timing_str)
        if match:
            return int(match.group(1))
            
        return None
    
    def update_or_create_yaml_files(self, instructions: List[Dict[str, Any]]) -> None:
        """Update existing YAML files or create new ones"""
        for instruction in instructions:
            try:
                # Generate filename from ID
                filename = f"{instruction['metadata']['id']}.yaml"
                filepath = self.instructions_dir / filename
                
                # Check if file exists
                if filepath.exists():
                    # Read existing content
                    with open(filepath, 'r') as f:
                        content = f.read()
                    
                    # Parse existing YAML (simple approach - preserve other layers)
                    existing_lines = content.split('\n')
                    new_lines = []
                    in_layer1 = False
                    skip_until_next_layer = False
                    
                    for line in existing_lines:
                        if line.startswith('layer1_csv:'):
                            in_layer1 = True
                            skip_until_next_layer = True
                            # Add new layer1 data
                            new_lines.append('layer1_csv:')
                            layer1_data = instruction['layer1_csv']
                            new_lines.append(f"  mnemonic: {layer1_data['mnemonic']}")
                            new_lines.append(f"  syntax: |")
                            new_lines.append(f"    {layer1_data['syntax']}")
                            new_lines.append(f"  group: {layer1_data['group']}")
                            new_lines.append(f"  encoding: {layer1_data['encoding']}")
                            new_lines.append(f"  alias: {layer1_data['alias'] if layer1_data['alias'] else '.'}")
                            new_lines.append(f"  description: {layer1_data['description']}")
                            new_lines.append(f"  interrupt_shield: {str(layer1_data['interrupt_shield']).lower()}")
                            new_lines.append(f"  timing:")
                            new_lines.append(f"    cog_exec_8_cogs: {layer1_data['timing']['cog_exec_8_cogs']}")
                            new_lines.append(f"    cog_exec_16_cogs: {layer1_data['timing']['cog_exec_16_cogs']}")
                        elif line.startswith('layer2_') or line.startswith('layer3_') or line.startswith('layer4_'):
                            skip_until_next_layer = False
                            in_layer1 = False
                            new_lines.append(line)
                        elif not skip_until_next_layer:
                            new_lines.append(line)
                    
                    # Write updated content
                    with open(filepath, 'w') as f:
                        f.write('\n'.join(new_lines))
                    
                    self.updated_count += 1
                    self.audit_log.append({
                        'timestamp': datetime.now().isoformat(),
                        'action': 'updated',
                        'file': str(filepath),
                        'instruction': instruction['metadata']['id']
                    })
                else:
                    # Create new file with simple YAML format
                    with open(filepath, 'w') as f:
                        # Write metadata
                        f.write("metadata:\n")
                        f.write(f"  id: {instruction['metadata']['id']}\n")
                        f.write(f"  version: {instruction['metadata']['version']}\n")
                        f.write(f"  extraction_date: |\n")
                        f.write(f"    {instruction['metadata']['extraction_date']}\n")
                        f.write(f"  source:\n")
                        f.write(f"    document: {instruction['metadata']['source']['document']}\n")
                        f.write(f"    type: {instruction['metadata']['source']['type']}\n")
                        f.write(f"    row: {instruction['metadata']['source']['row']}\n")
                        
                        # Write layer1_csv
                        f.write("layer1_csv:\n")
                        layer1 = instruction['layer1_csv']
                        f.write(f"  mnemonic: {layer1['mnemonic']}\n")
                        f.write(f"  syntax: |\n")
                        f.write(f"    {layer1['syntax']}\n")
                        f.write(f"  group: {layer1['group']}\n")
                        f.write(f"  encoding: {layer1['encoding']}\n")
                        f.write(f"  alias: {layer1['alias'] if layer1['alias'] else '.'}\n")
                        f.write(f"  description: {layer1['description']}\n")
                        f.write(f"  interrupt_shield: {str(layer1['interrupt_shield']).lower()}\n")
                        f.write(f"  timing:\n")
                        f.write(f"    cog_exec_8_cogs: {layer1['timing']['cog_exec_8_cogs']}\n")
                        f.write(f"    cog_exec_16_cogs: {layer1['timing']['cog_exec_16_cogs']}\n")
                    
                    self.created_count += 1
                    self.audit_log.append({
                        'timestamp': datetime.now().isoformat(),
                        'action': 'created',
                        'file': str(filepath),
                        'instruction': instruction['metadata']['id']
                    })
                
            except Exception as e:
                self.error_count += 1
                self.audit_log.append({
                    'instruction': instruction.get('metadata', {}).get('id', 'unknown'),
                    'error': f"Failed to write YAML: {str(e)}",
                    'severity': 'error'
                })
    
    def run(self) -> None:
        """Run the complete extraction process"""
        print(f"Starting extraction from: {self.csv_path}")
        
        # Parse CSV
        print("Parsing CSV...")
        instructions = self.parse_csv()
        print(f"Extracted {len(instructions)} instructions")
        
        # Update or create YAML files
        print("Updating/creating YAML files...")
        self.update_or_create_yaml_files(instructions)
        
        # Report results
        print(f"\nExtraction complete:")
        print(f"  Instructions processed: {self.instruction_count}")
        print(f"  Files updated: {self.updated_count}")
        print(f"  Files created: {self.created_count}")
        print(f"  Errors encountered: {self.error_count}")

if __name__ == "__main__":
    # Configure paths
    csv_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv"
    output_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2"
    
    # Run extraction
    extractor = InstructionExtractor(csv_path, output_dir)
    extractor.run()