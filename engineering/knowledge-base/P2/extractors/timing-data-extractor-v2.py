#!/usr/bin/env python3
"""
P2 Datasheet Timing Data Extractor V2
Simplified version with better YAML handling
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class SimpleTimingExtractor:
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
            
        # Find sections with timing info
        sections = content.split('##')
        
        for section in sections:
            if 'Instructions' not in section:
                continue
            
            # Default timing for sections
            default_timing = None
            if 'execute in 2 clock cycles' in section:
                default_timing = 2
            
            # Parse instruction lines
            for line in section.split('\n'):
                if not line.startswith('| **'):
                    continue
                    
                # Extract mnemonic and timing
                parts = line.split('|')
                if len(parts) < 3:
                    continue
                    
                # Get mnemonic
                instruction_part = parts[1].strip()
                match = re.match(r'\*\*([A-Z][A-Z0-9]*)', instruction_part)
                if not match:
                    continue
                    
                mnemonic = match.group(1)
                
                # Get timing (last column or default)
                timing_str = None
                if len(parts) >= 4:
                    # Try to find timing in last column
                    last_col = parts[-2].strip()
                    if last_col and (last_col[0].isdigit() or last_col in ['2', '2+', 'varies']):
                        timing_str = last_col
                
                # Use default if no specific timing found
                if not timing_str and default_timing:
                    timing_str = str(default_timing)
                
                if timing_str:
                    timing_by_mnemonic[mnemonic] = self._parse_timing(timing_str)
        
        return timing_by_mnemonic
    
    def _parse_timing(self, timing_str: str) -> Dict[str, Any]:
        """Parse timing string into structured format"""
        result = {
            'raw': timing_str,
            'base_cycles': None,
            'notes': []
        }
        
        # Simple number
        if timing_str.isdigit():
            result['base_cycles'] = int(timing_str)
            result['type'] = 'fixed'
            
        # Range (e.g., "13...20")
        elif '...' in timing_str:
            match = re.match(r'(\d+)\.\.\.(\d+)', timing_str)
            if match:
                result['min_cycles'] = int(match.group(1))
                result['max_cycles'] = int(match.group(2))
                result['type'] = 'variable'
                result['notes'].append('Hub window alignment affects timing')
                
        # Conditional (e.g., "2 or 4")
        elif ' or ' in timing_str:
            parts = timing_str.split(' or ')
            if all(p.strip().isdigit() for p in parts):
                result['cycles_options'] = [int(p.strip()) for p in parts]
                result['type'] = 'conditional'
                result['notes'].append('Timing depends on condition')
                
        # Variable (e.g., "2+D", "2+")
        elif '+' in timing_str:
            match = re.match(r'(\d+)\+(.*)$', timing_str)
            if match:
                result['base_cycles'] = int(match.group(1))
                result['type'] = 'variable'
                variable = match.group(2).strip()
                if variable:
                    result['notes'].append(f'Plus {variable} cycles')
                else:
                    result['notes'].append('Plus wait condition')
        
        return result
    
    def update_yaml_files(self, timing_data: Dict[str, Any]) -> None:
        """Update YAML files with layer2 timing data"""
        yaml_files = list(self.yaml_dir.glob('pasm2_*.yaml'))
        
        print(f"Processing {len(yaml_files)} YAML files...")
        
        for yaml_file in yaml_files:
            try:
                # Read YAML file content
                with open(yaml_file, 'r') as f:
                    content = f.read()
                
                # Extract mnemonic using simple pattern matching
                mnemonic = None
                for line in content.split('\n'):
                    if 'mnemonic:' in line:
                        parts = line.split(':', 1)
                        if len(parts) > 1:
                            mnemonic = parts[1].strip()
                            break
                
                if mnemonic and mnemonic in timing_data:
                    # Check if layer2_datasheet already exists
                    if 'layer2_datasheet:' not in content:
                        # Find where to insert layer2 (after layer1_csv section)
                        lines = content.split('\n')
                        insert_index = None
                        
                        # Find end of layer1_csv section
                        in_layer1 = False
                        for i, line in enumerate(lines):
                            if 'layer1_csv:' in line:
                                in_layer1 = True
                            elif in_layer1 and line and not line.startswith(' '):
                                # End of layer1_csv section
                                insert_index = i
                                break
                        
                        if insert_index is None:
                            insert_index = len(lines)
                        
                        # Build layer2 content
                        layer2_lines = [
                            'layer2_datasheet:',
                            f'  extraction_date: {datetime.now().isoformat()}',
                            '  source: P2 Datasheet v35',
                            '  timing:'
                        ]
                        
                        timing = timing_data[mnemonic]
                        for key, value in timing.items():
                            if isinstance(value, list):
                                if key == 'notes' and value:
                                    layer2_lines.append(f'    {key}:')
                                    for note in value:
                                        layer2_lines.append(f'      - {note}')
                                elif key == 'cycles_options':
                                    layer2_lines.append(f'    {key}: [{", ".join(str(v) for v in value)}]')
                            elif value is not None:
                                layer2_lines.append(f'    {key}: {value}')
                        
                        # Insert layer2 content
                        lines.insert(insert_index, '\n'.join(layer2_lines))
                        
                        # Write updated content
                        with open(yaml_file, 'w') as f:
                            f.write('\n'.join(lines))
                        
                        self.matched_count += 1
                        self.audit_log.append({
                            'action': 'updated',
                            'file': yaml_file.name,
                            'mnemonic': mnemonic,
                            'timing': timing.get('raw', 'unknown')
                        })
                    else:
                        self.audit_log.append({
                            'action': 'already_has_layer2',
                            'file': yaml_file.name,
                            'mnemonic': mnemonic
                        })
                else:
                    self.unmatched_count += 1
                    if mnemonic:
                        self.audit_log.append({
                            'action': 'no_timing_found',
                            'file': yaml_file.name,
                            'mnemonic': mnemonic
                        })
                    
            except Exception as e:
                self.audit_log.append({
                    'action': 'error',
                    'file': yaml_file.name,
                    'error': str(e)
                })
                print(f"Error processing {yaml_file.name}: {e}")
    
    def write_audit_report(self) -> None:
        """Write timing extraction audit report"""
        audit_file = self.yaml_dir.parent / "timing-extraction-audit.md"
        
        with open(audit_file, 'w') as f:
            f.write("# Timing Data Extraction Audit Report\n\n")
            f.write(f"**Date**: {datetime.now().isoformat()}\n")
            f.write(f"**Source**: {self.datasheet_path.name}\n")
            f.write(f"**Target Directory**: {self.yaml_dir}\n\n")
            
            f.write("## Summary\n")
            f.write(f"- Instructions with timing added: {self.matched_count}\n")
            f.write(f"- Instructions without timing: {self.unmatched_count}\n")
            
            if (self.matched_count + self.unmatched_count) > 0:
                coverage = round(self.matched_count / (self.matched_count + self.unmatched_count) * 100, 2)
                f.write(f"- Coverage: {coverage}%\n\n")
            
            f.write("## Timing Data Found\n")
            f.write(f"Total mnemonics with timing data: {len(self.timing_data)}\n\n")
            
            f.write("### Sample Timing Data\n")
            for mnemonic, timing in list(self.timing_data.items())[:10]:
                f.write(f"- **{mnemonic}**: {timing.get('raw', 'unknown')}\n")
            
            f.write("\n## Processing Log\n")
            
            # Group by action type
            actions = {}
            for entry in self.audit_log:
                action = entry.get('action', 'unknown')
                if action not in actions:
                    actions[action] = []
                actions[action].append(entry)
            
            for action, entries in actions.items():
                f.write(f"\n### {action.replace('_', ' ').title()} ({len(entries)} files)\n")
                if len(entries) <= 10:
                    for entry in entries:
                        f.write(f"- {entry.get('file', 'unknown')}")
                        if 'mnemonic' in entry:
                            f.write(f" ({entry['mnemonic']})")
                        f.write("\n")
                else:
                    f.write(f"- {len(entries)} files processed\n")
        
        print(f"Audit report written to: {audit_file}")
    
    def run(self) -> None:
        """Run the complete timing extraction process"""
        print(f"Starting timing extraction from: {self.datasheet_path.name}")
        
        # Parse datasheet timing
        print("Parsing datasheet timing information...")
        self.timing_data = self.parse_datasheet_timing()
        print(f"Found timing data for {len(self.timing_data)} mnemonics")
        
        # Show sample of timing data found
        if self.timing_data:
            print("\nSample timing data found:")
            for mnemonic, timing in list(self.timing_data.items())[:5]:
                print(f"  {mnemonic}: {timing.get('raw', 'unknown')}")
        
        # Update YAML files
        print("\nUpdating YAML files with layer2 timing data...")
        self.update_yaml_files(self.timing_data)
        
        # Write audit report
        print("\nWriting audit report...")
        self.write_audit_report()
        
        # Report results
        print(f"\nTiming extraction complete:")
        print(f"  Instructions updated: {self.matched_count}")
        print(f"  Instructions without timing: {self.unmatched_count}")
        if (self.matched_count + self.unmatched_count) > 0:
            coverage = round(self.matched_count / (self.matched_count + self.unmatched_count) * 100, 2)
            print(f"  Coverage: {coverage}%")

if __name__ == "__main__":
    # Configure paths
    datasheet_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/p2-datasheet/pasm2-complete-instruction-tables.md"
    yaml_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/instructions/pasm2"
    
    # Run extraction
    extractor = SimpleTimingExtractor(datasheet_path, yaml_dir)
    extractor.run()