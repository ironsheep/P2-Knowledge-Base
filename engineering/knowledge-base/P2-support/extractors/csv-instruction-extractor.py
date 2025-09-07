#!/usr/bin/env python3
"""
PASM2 Instruction CSV Extractor
Extracts instruction data from P2 Instructions v35 CSV and generates YAML files
"""

import csv
import yaml
import os
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

class InstructionExtractor:
    def __init__(self, csv_path: str, output_dir: str):
        self.csv_path = Path(csv_path)
        self.output_dir = Path(output_dir)
        self.instructions_dir = self.output_dir / "instructions" / "pasm2"
        self.audit_log = []
        self.mapping = {}
        self.instruction_count = 0
        self.error_count = 0
        
        # Ensure output directories exist
        self.instructions_dir.mkdir(parents=True, exist_ok=True)
        
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
            
            # Generate instruction ID
            instruction_id = self._generate_id(mnemonic, syntax)
            
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
    
    def _generate_id(self, mnemonic: str, syntax: str) -> str:
        """Generate unique ID for instruction"""
        # Create hash from syntax for uniqueness
        syntax_hash = hashlib.md5(syntax.encode()).hexdigest()[:8]
        return f"pasm2_{mnemonic.lower()}_{syntax_hash}"
    
    def _parse_timing(self, timing_str: str) -> Optional[int]:
        """Parse timing information from string"""
        if not timing_str:
            return None
            
        # Extract numeric value
        match = re.search(r'(\d+)', timing_str)
        if match:
            return int(match.group(1))
            
        return None
    
    def generate_yaml_files(self, instructions: List[Dict[str, Any]]) -> None:
        """Generate individual YAML files for each instruction"""
        for instruction in instructions:
            try:
                # Generate filename from ID
                filename = f"{instruction['metadata']['id']}.yaml"
                filepath = self.instructions_dir / filename
                
                # Write YAML file
                with open(filepath, 'w') as f:
                    yaml.dump(instruction, f, default_flow_style=False, sort_keys=False)
                    
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
    
    def write_mapping_file(self) -> None:
        """Write mapping file tracking CSV rows to YAML files"""
        mapping_file = self.output_dir / "csv-to-yaml-mapping.yaml"
        
        with open(mapping_file, 'w') as f:
            yaml.dump({
                'metadata': {
                    'generated': datetime.now().isoformat(),
                    'source_csv': str(self.csv_path),
                    'total_instructions': self.instruction_count
                },
                'mappings': self.mapping
            }, f, default_flow_style=False)
            
        self.audit_log.append({
            'timestamp': datetime.now().isoformat(),
            'action': 'created_mapping',
            'file': str(mapping_file),
            'entries': len(self.mapping)
        })
    
    def write_audit_log(self) -> None:
        """Write extraction audit log"""
        audit_file = self.output_dir / "extraction-audit.yaml"
        
        with open(audit_file, 'w') as f:
            yaml.dump({
                'metadata': {
                    'extraction_date': datetime.now().isoformat(),
                    'source_csv': str(self.csv_path),
                    'total_processed': self.instruction_count,
                    'total_errors': self.error_count
                },
                'log_entries': self.audit_log
            }, f, default_flow_style=False)
    
    def validate_extraction(self) -> Dict[str, Any]:
        """Validate extraction completeness"""
        validation = {
            'timestamp': datetime.now().isoformat(),
            'total_extracted': self.instruction_count,
            'total_errors': self.error_count,
            'checks': []
        }
        
        # Check for duplicate mnemonics
        mnemonics = {}
        for inst_id, mapping in self.mapping.items():
            mnemonic = mapping['mnemonic']
            if mnemonic in mnemonics:
                mnemonics[mnemonic].append(inst_id)
            else:
                mnemonics[mnemonic] = [inst_id]
        
        # Report duplicates (expected for variants)
        for mnemonic, ids in mnemonics.items():
            if len(ids) > 1:
                validation['checks'].append({
                    'type': 'duplicate_mnemonic',
                    'mnemonic': mnemonic,
                    'variants': len(ids),
                    'ids': ids
                })
        
        # Check for missing core instructions (basic check)
        core_instructions = ['ADD', 'SUB', 'MOV', 'JMP', 'CALL', 'RET', 'AND', 'OR', 'XOR']
        missing = []
        for inst in core_instructions:
            if inst not in mnemonics:
                missing.append(inst)
        
        if missing:
            validation['checks'].append({
                'type': 'missing_core_instructions',
                'missing': missing,
                'severity': 'warning'
            })
        
        validation['status'] = 'complete' if self.error_count == 0 else 'completed_with_errors'
        
        return validation
    
    def run(self) -> None:
        """Run the complete extraction process"""
        print(f"Starting extraction from: {self.csv_path}")
        
        # Parse CSV
        print("Parsing CSV...")
        instructions = self.parse_csv()
        print(f"Extracted {len(instructions)} instructions")
        
        # Generate YAML files
        print("Generating YAML files...")
        self.generate_yaml_files(instructions)
        
        # Write mapping
        print("Writing mapping file...")
        self.write_mapping_file()
        
        # Validate
        print("Validating extraction...")
        validation = self.validate_extraction()
        
        # Write audit log
        print("Writing audit log...")
        self.write_audit_log()
        
        # Report results
        print(f"\nExtraction complete:")
        print(f"  Instructions extracted: {self.instruction_count}")
        print(f"  Errors encountered: {self.error_count}")
        print(f"  Status: {validation['status']}")
        
        if validation['checks']:
            print(f"  Validation notes: {len(validation['checks'])} items")

if __name__ == "__main__":
    # Configure paths
    csv_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv"
    output_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2"
    
    # Run extraction
    extractor = InstructionExtractor(csv_path, output_dir)
    extractor.run()