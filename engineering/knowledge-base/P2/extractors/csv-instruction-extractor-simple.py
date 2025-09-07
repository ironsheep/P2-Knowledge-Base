#!/usr/bin/env python3
"""
PASM2 Instruction CSV Extractor (Simple Version)
Extracts instruction data from P2 Instructions v35 CSV and generates YAML files
No external dependencies - uses built-in Python modules only
"""

import csv
import json
import os
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

def write_yaml_style(data: Any, indent: int = 0) -> str:
    """Write data in YAML-like format without yaml library"""
    result = []
    indent_str = "  " * indent
    
    if isinstance(data, dict):
        for key, value in data.items():
            if value is None:
                continue
            elif isinstance(value, (dict, list)) and value:
                result.append(f"{indent_str}{key}:")
                result.append(write_yaml_style(value, indent + 1))
            elif isinstance(value, bool):
                result.append(f"{indent_str}{key}: {str(value).lower()}")
            elif isinstance(value, (int, float)):
                result.append(f"{indent_str}{key}: {value}")
            else:
                # Handle strings with special characters
                value_str = str(value)
                if '\n' in value_str or ':' in value_str or '#' in value_str:
                    # Multi-line or special chars - use literal block
                    lines = value_str.split('\n')
                    result.append(f"{indent_str}{key}: |")
                    for line in lines:
                        result.append(f"{indent_str}  {line}")
                else:
                    result.append(f"{indent_str}{key}: {value_str}")
    
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                result.append(f"{indent_str}-")
                result.append(write_yaml_style(item, indent + 1))
            else:
                result.append(f"{indent_str}- {item}")
    
    return '\n'.join(result)

class SimpleInstructionExtractor:
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
                # Read the CSV
                reader = csv.reader(f)
                
                # Get header
                header = next(reader)
                
                # Process rows
                for row_num, row in enumerate(reader, start=2):  # Start at 2 for 1-based + header
                    if len(row) > 1 and row[1].strip():  # Check syntax column has content
                        instruction = self._extract_instruction(header, row, row_num)
                        if instruction:
                            instructions.append(instruction)
                            
        except Exception as e:
            self.audit_log.append({
                'timestamp': datetime.now().isoformat(),
                'error': f"Failed to parse CSV: {str(e)}",
                'severity': 'critical'
            })
            print(f"Error parsing CSV: {e}")
            
        return instructions
    
    def _extract_instruction(self, header: List[str], row: List[str], row_num: int) -> Optional[Dict[str, Any]]:
        """Extract instruction data from CSV row"""
        try:
            # Ensure we have enough columns
            if len(row) < 6:
                return None
                
            # Extract data from known column positions
            order = row[0].strip() if len(row) > 0 else ""
            syntax = row[1].strip() if len(row) > 1 else ""
            group = row[2].strip() if len(row) > 2 else ""
            encoding = row[3].strip() if len(row) > 3 else ""
            alias = row[4].strip() if len(row) > 4 else ""
            description = row[5].strip() if len(row) > 5 else ""
            interrupt_shield = row[6].strip() if len(row) > 6 else ""
            
            # Skip empty or header-like rows
            if not syntax or "Assembly Syntax" in syntax or "---" in syntax:
                return None
            
            # Extract timing information if available
            cog_exec_8 = row[7].strip() if len(row) > 7 else ""
            hub_exec_8 = row[8].strip() if len(row) > 8 else ""
            cog_exec_16 = row[9].strip() if len(row) > 9 else ""
            hub_exec_16 = row[10].strip() if len(row) > 10 else ""
            
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
                    'group': group if group and group != '-' else None,
                    'encoding': encoding if encoding else None,
                    'alias': alias if alias and alias != '-' else None,
                    'description': description if description else None,
                    'interrupt_shield': interrupt_shield.lower() == 'yes' if interrupt_shield else False,
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
                
                # Write YAML-style file
                with open(filepath, 'w') as f:
                    f.write(write_yaml_style(instruction))
                    
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
        
        mapping_data = {
            'metadata': {
                'generated': datetime.now().isoformat(),
                'source_csv': str(self.csv_path),
                'total_instructions': self.instruction_count
            },
            'mappings': self.mapping
        }
        
        with open(mapping_file, 'w') as f:
            f.write(write_yaml_style(mapping_data))
            
        self.audit_log.append({
            'timestamp': datetime.now().isoformat(),
            'action': 'created_mapping',
            'file': str(mapping_file),
            'entries': len(self.mapping)
        })
    
    def write_audit_log(self) -> None:
        """Write extraction audit log"""
        audit_file = self.output_dir / "extraction-audit.yaml"
        
        audit_data = {
            'metadata': {
                'extraction_date': datetime.now().isoformat(),
                'source_csv': str(self.csv_path),
                'total_processed': self.instruction_count,
                'total_errors': self.error_count
            },
            'log_entries': self.audit_log
        }
        
        with open(audit_file, 'w') as f:
            f.write(write_yaml_style(audit_data))
    
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
        duplicate_count = 0
        for mnemonic, ids in mnemonics.items():
            if len(ids) > 1:
                duplicate_count += 1
                validation['checks'].append({
                    'type': 'duplicate_mnemonic',
                    'mnemonic': mnemonic,
                    'variants': len(ids),
                    'ids': ids
                })
        
        print(f"Found {duplicate_count} mnemonics with multiple variants")
        
        # Check for missing core instructions
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
            print(f"Warning: Missing core instructions: {missing}")
        
        validation['status'] = 'complete' if self.error_count == 0 else 'completed_with_errors'
        
        return validation
    
    def run(self) -> None:
        """Run the complete extraction process"""
        print(f"Starting extraction from: {self.csv_path.name}")
        
        # Parse CSV
        print("Parsing CSV...")
        instructions = self.parse_csv()
        print(f"Extracted {len(instructions)} instructions")
        
        if instructions:
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
        else:
            print("No instructions extracted - check CSV format")

if __name__ == "__main__":
    # Configure paths
    csv_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv"
    output_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2"
    
    # Run extraction
    extractor = SimpleInstructionExtractor(csv_path, output_dir)
    extractor.run()