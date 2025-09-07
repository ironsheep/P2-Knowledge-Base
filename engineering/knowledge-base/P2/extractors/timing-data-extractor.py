#!/usr/bin/env python3
"""
P2 Datasheet Timing Data Extractor
Extracts timing information from datasheet and adds as layer2 to YAML files
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

def read_yaml_style(file_path: str) -> Dict[str, Any]:
    """Read YAML-style file into dictionary"""
    result = {}
    current_dict = result
    dict_stack = []
    current_key = None
    in_multiline = False
    multiline_content = []
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
        
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Handle multiline content
        if in_multiline:
            if line and not line[0].isspace():
                # End of multiline
                if current_key and dict_stack:
                    dict_stack[-1][current_key] = '\n'.join(multiline_content)
                in_multiline = False
                multiline_content = []
            else:
                multiline_content.append(line.strip())
                i += 1
                continue
        
        # Skip empty lines
        if not line:
            i += 1
            continue
            
        # Count indentation
        indent = len(line) - len(line.lstrip())
        
        # Parse key-value
        if ':' in line:
            parts = line.split(':', 1)
            key = parts[0].strip()
            value = parts[1].strip() if len(parts) > 1 else ''
            
            # Handle different value types
            if value == '|':
                # Start multiline
                in_multiline = True
                current_key = key
                multiline_content = []
            elif value == '':
                # New dict
                new_dict = {}
                if indent == 0:
                    result[key] = new_dict
                    dict_stack = [result]
                    current_dict = new_dict
                else:
                    # Add to current level
                    if dict_stack:
                        dict_stack[-1][key] = new_dict
            elif value == 'true':
                if dict_stack:
                    dict_stack[-1][key] = True
            elif value == 'false':
                if dict_stack:
                    dict_stack[-1][key] = False
            elif value.isdigit():
                if dict_stack:
                    dict_stack[-1][key] = int(value)
            else:
                if dict_stack:
                    dict_stack[-1][key] = value
        
        i += 1
    
    return result

def write_yaml_style(data: Any, indent: int = 0) -> str:
    """Write data in YAML-like format"""
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

class TimingDataExtractor:
    def __init__(self, datasheet_path: str, yaml_dir: str):
        self.datasheet_path = Path(datasheet_path)
        self.yaml_dir = Path(yaml_dir)
        self.timing_data = {}
        self.audit_log = []
        self.matched_count = 0
        self.unmatched_count = 0
        
    def parse_datasheet_timing(self) -> Dict[str, Any]:
        """Parse timing information from datasheet"""
        timing_by_mnemonic = {}
        
        with open(self.datasheet_path, 'r') as f:
            content = f.read()
            
        # Find instruction tables with timing info
        sections = content.split('##')
        
        for section in sections:
            if 'Instructions' not in section:
                continue
                
            # Check for timing statement
            if 'execute in 2 clock cycles' in section:
                # All instructions in this section have 2 cycle timing
                self._extract_fixed_timing_section(section, 2, timing_by_mnemonic)
            else:
                # Parse individual instruction timing
                self._extract_variable_timing_section(section, timing_by_mnemonic)
        
        return timing_by_mnemonic
    
    def _extract_fixed_timing_section(self, section: str, cycles: int, timing_dict: Dict) -> None:
        """Extract instructions from section with fixed timing"""
        lines = section.split('\n')
        
        for line in lines:
            if line.startswith('| **'):
                # Extract mnemonic from markdown table row
                match = re.match(r'\| \*\*([A-Z][A-Z0-9]*)', line)
                if match:
                    mnemonic = match.group(1)
                    if mnemonic not in timing_dict:
                        timing_dict[mnemonic] = {
                            'base_cycles': cycles,
                            'execution_modes': {
                                'cog': cycles,
                                'lut': cycles
                            },
                            'notes': []
                        }
    
    def _extract_variable_timing_section(self, section: str, timing_dict: Dict) -> None:
        """Extract instructions with variable timing"""
        lines = section.split('\n')
        
        for line in lines:
            if not line.startswith('|'):
                continue
                
            # Parse markdown table row with timing column
            parts = line.split('|')
            if len(parts) >= 4:  # Has timing column
                instruction_part = parts[1].strip()
                timing_part = parts[-2].strip() if len(parts) > 3 else ''
                
                # Extract mnemonic
                match = re.match(r'\*\*([A-Z][A-Z0-9]*)', instruction_part)
                if match and timing_part:
                    mnemonic = match.group(1)
                    
                    # Parse timing information
                    timing_info = self._parse_timing_string(timing_part)
                    if timing_info:
                        if mnemonic not in timing_dict:
                            timing_dict[mnemonic] = timing_info
                        else:
                            # Merge timing info
                            self._merge_timing_info(timing_dict[mnemonic], timing_info)
    
    def _parse_timing_string(self, timing_str: str) -> Optional[Dict[str, Any]]:
        """Parse timing string into structured format"""
        timing_info = {
            'base_cycles': None,
            'execution_modes': {},
            'conditions': [],
            'notes': []
        }
        
        # Clean timing string
        timing_str = timing_str.strip()
        
        # Simple fixed timing (e.g., "2")
        if timing_str.isdigit():
            cycles = int(timing_str)
            timing_info['base_cycles'] = cycles
            timing_info['execution_modes'] = {
                'cog': cycles,
                'lut': cycles
            }
            return timing_info
        
        # Range timing (e.g., "13...20")
        if '...' in timing_str:
            match = re.match(r'(\d+)\.\.\.(\d+)', timing_str)
            if match:
                min_cycles = int(match.group(1))
                max_cycles = int(match.group(2))
                timing_info['base_cycles'] = min_cycles
                timing_info['execution_modes'] = {
                    'hub': {'min': min_cycles, 'max': max_cycles}
                }
                timing_info['notes'].append(f"Hub window alignment: {min_cycles}-{max_cycles} cycles")
                return timing_info
        
        # Conditional timing (e.g., "2 or 4")
        if ' or ' in timing_str:
            parts = timing_str.split(' or ')
            if all(p.strip().isdigit() for p in parts):
                cycles = [int(p.strip()) for p in parts]
                timing_info['base_cycles'] = cycles[0]
                timing_info['conditions'].append({
                    'condition': 'branch_taken',
                    'cycles': cycles
                })
                return timing_info
        
        # Variable timing (e.g., "2+D", "2+")
        if '+' in timing_str:
            match = re.match(r'(\d+)\+(.*)$', timing_str)
            if match:
                base = int(match.group(1))
                variable = match.group(2).strip()
                timing_info['base_cycles'] = base
                if variable:
                    timing_info['conditions'].append({
                        'condition': 'variable',
                        'description': f"Base {base} cycles plus {variable}"
                    })
                else:
                    timing_info['conditions'].append({
                        'condition': 'wait',
                        'description': f"Base {base} cycles plus wait condition"
                    })
                return timing_info
        
        # Split timing (e.g., "Cog & LUT / Hub")
        if '/' in timing_str:
            parts = timing_str.split('/')
            if len(parts) == 2:
                cog_lut = parts[0].strip()
                hub = parts[1].strip()
                
                # Parse cog/lut timing
                if cog_lut.isdigit():
                    cog_cycles = int(cog_lut)
                    timing_info['execution_modes']['cog'] = cog_cycles
                    timing_info['execution_modes']['lut'] = cog_cycles
                    timing_info['base_cycles'] = cog_cycles
                
                # Parse hub timing
                if '...' in hub:
                    match = re.match(r'(\d+)\.\.\.(\d+)', hub)
                    if match:
                        timing_info['execution_modes']['hub'] = {
                            'min': int(match.group(1)),
                            'max': int(match.group(2))
                        }
                elif hub.isdigit():
                    timing_info['execution_modes']['hub'] = int(hub)
                
                return timing_info
        
        return None
    
    def _merge_timing_info(self, existing: Dict, new: Dict) -> None:
        """Merge new timing info into existing"""
        if new.get('base_cycles') and not existing.get('base_cycles'):
            existing['base_cycles'] = new['base_cycles']
        
        existing['execution_modes'].update(new.get('execution_modes', {}))
        existing['conditions'].extend(new.get('conditions', []))
        existing['notes'].extend(new.get('notes', []))
    
    def update_yaml_files(self, timing_data: Dict[str, Any]) -> None:
        """Update YAML files with layer2 timing data"""
        yaml_files = list(self.yaml_dir.glob('pasm2_*.yaml'))
        
        for yaml_file in yaml_files:
            try:
                # Read existing YAML
                instruction = read_yaml_style(yaml_file)
                
                # Get mnemonic from layer1 data
                mnemonic = instruction.get('layer1_csv', {}).get('mnemonic')
                
                if mnemonic and mnemonic in timing_data:
                    # Add layer2 timing data
                    if 'layer2_datasheet' not in instruction:
                        instruction['layer2_datasheet'] = {}
                    
                    instruction['layer2_datasheet']['timing'] = timing_data[mnemonic]
                    instruction['layer2_datasheet']['extraction_date'] = datetime.now().isoformat()
                    instruction['layer2_datasheet']['source'] = 'P2 Datasheet v35'
                    
                    # Write updated YAML
                    with open(yaml_file, 'w') as f:
                        f.write(write_yaml_style(instruction))
                    
                    self.matched_count += 1
                    self.audit_log.append({
                        'action': 'updated',
                        'file': yaml_file.name,
                        'mnemonic': mnemonic,
                        'timing_added': True
                    })
                else:
                    self.unmatched_count += 1
                    self.audit_log.append({
                        'action': 'no_timing_found',
                        'file': yaml_file.name,
                        'mnemonic': mnemonic or 'unknown'
                    })
                    
            except Exception as e:
                self.audit_log.append({
                    'action': 'error',
                    'file': yaml_file.name,
                    'error': str(e)
                })
    
    def write_audit_report(self) -> None:
        """Write timing extraction audit report"""
        audit_file = self.yaml_dir.parent / "timing-extraction-audit.yaml"
        
        audit_data = {
            'metadata': {
                'extraction_date': datetime.now().isoformat(),
                'source_datasheet': str(self.datasheet_path),
                'yaml_directory': str(self.yaml_dir),
                'total_matched': self.matched_count,
                'total_unmatched': self.unmatched_count
            },
            'timing_coverage': {
                'instructions_with_timing': self.matched_count,
                'instructions_without_timing': self.unmatched_count,
                'coverage_percentage': round(self.matched_count / (self.matched_count + self.unmatched_count) * 100, 2) if (self.matched_count + self.unmatched_count) > 0 else 0
            },
            'log_entries': self.audit_log
        }
        
        with open(audit_file, 'w') as f:
            f.write(write_yaml_style(audit_data))
        
        print(f"Audit report written to: {audit_file}")
    
    def run(self) -> None:
        """Run the complete timing extraction process"""
        print(f"Starting timing extraction from: {self.datasheet_path.name}")
        
        # Parse datasheet timing
        print("Parsing datasheet timing information...")
        timing_data = self.parse_datasheet_timing()
        print(f"Found timing data for {len(timing_data)} mnemonics")
        
        # Update YAML files
        print("Updating YAML files with layer2 timing data...")
        self.update_yaml_files(timing_data)
        
        # Write audit report
        print("Writing audit report...")
        self.write_audit_report()
        
        # Report results
        print(f"\nTiming extraction complete:")
        print(f"  Instructions updated: {self.matched_count}")
        print(f"  Instructions without timing: {self.unmatched_count}")
        print(f"  Coverage: {round(self.matched_count / (self.matched_count + self.unmatched_count) * 100, 2)}%")

if __name__ == "__main__":
    # Configure paths
    datasheet_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/p2-datasheet/pasm2-complete-instruction-tables.md"
    yaml_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/instructions/pasm2"
    
    # Run extraction
    extractor = TimingDataExtractor(datasheet_path, yaml_dir)
    extractor.run()