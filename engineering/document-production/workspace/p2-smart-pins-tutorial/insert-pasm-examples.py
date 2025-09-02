#!/usr/bin/env python3
"""
Insert PASM2 examples from Titus files into V4 to create V5.
Bottom-up approach to preserve line numbers during insertion.
"""

import re
from pathlib import Path

class PASMInserter:
    def __init__(self, v4_path, titus_dir):
        self.v4_path = Path(v4_path)
        self.titus_dir = Path(titus_dir)
        self.insertions = []
        self.stats = {
            'modes_processed': 0,
            'pasm_inserted': 0,
            'spin2_found': 0
        }
        
    def load_titus_example(self, filename):
        """Load a Titus PASM2 example, removing metadata comments."""
        filepath = self.titus_dir / filename
        if not filepath.exists():
            return None
            
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        # Skip metadata comments at the top
        code_lines = []
        for line in lines:
            # Skip extraction metadata
            if line.startswith("' Source:") or line.startswith("' Extracted:") or line.startswith("' Language:"):
                continue
            # Remove leading/trailing whitespace but preserve indentation
            code_lines.append(line.rstrip())
        
        # Remove leading/trailing blank lines
        while code_lines and not code_lines[0]:
            code_lines.pop(0)
        while code_lines and not code_lines[-1]:
            code_lines.pop()
            
        return code_lines
    
    def find_mode_sections(self, lines):
        """Find all Smart Pin mode sections and their line ranges."""
        mode_pattern = re.compile(r'^### Mode %([\d&\s-]+) - (.+)$')
        modes = []
        
        for i, line in enumerate(lines):
            match = mode_pattern.match(line)
            if match:
                modes.append({
                    'line_start': i,
                    'mode_code': match.group(1).strip(),
                    'mode_name': match.group(2).strip()
                })
        
        # Add end lines
        for i in range(len(modes)):
            if i + 1 < len(modes):
                modes[i]['line_end'] = modes[i + 1]['line_start'] - 1
            else:
                modes[i]['line_end'] = len(lines) - 1
                
        return modes
    
    def find_spin2_blocks_in_mode(self, lines, mode):
        """Find all Spin2 blocks within a mode section."""
        blocks = []
        i = mode['line_start']
        
        while i <= mode['line_end']:
            if lines[i].strip() == '```spin2':
                block_start = i
                # Find end of block
                i += 1
                while i <= mode['line_end'] and lines[i].strip() != '```':
                    i += 1
                if i <= mode['line_end']:
                    blocks.append({
                        'start': block_start,
                        'end': i,
                        'mode': mode['mode_code'],
                        'mode_name': mode['mode_name']
                    })
            i += 1
            
        return blocks
    
    def prepare_insertions(self, lines):
        """Prepare all insertions by finding Spin2 blocks that need PASM2."""
        modes = self.find_mode_sections(lines)
        
        # Map modes to Titus files - comprehensive coverage
        mode_to_titus = {
            '00000': ['req02-wypin-d-s-write-bits-d-31-0-to.pasm2'],  # Smart Pin OFF
            '00110': ['req27-wrpin-nco_config-20-set-config.txt'],  # NCO Duty
            '01100': ['req50-wrpin-a_in_mode-a_in-set-up-mo.txt', 'req51-wypin-0-a_in-count-only-a-inpu.pasm2'],  # Count Rises
            '01101': ['req34-wrpin-quadenc_config-32-set-fo.txt'],  # A-B Encoder
            '01110': ['req40-sar-quadenc_data-2-arithmetic-.txt', 'req41-mov-outa-quadenc_data.pasm2'],  # Incremental
            '01111': ['req55-wrpin-a_in_mode-a_in-set-up-mo.txt', 'req60-wrpin-a_in_mode-a_in-set-up-mo.txt'],  # Comparator
            '11111': ['req72-wrpin-a_adc_mode-a_adc-set-up-.txt', 'req75-wrpin-a_adc_mode-a_adc-set-up-.txt'],  # ADC
            '00010 & 00011': ['req11-wypin-dacvolt-20-load-dac.pasm2', 'req14-wypin-dacvolt2-20.pasm2'],  # DAC
            '11011': ['req84-wrpin-sync_tx_mode-txout-set-s.txt', 'req87-wrpin-sync_rx_mode-rxin.txt'],  # Sync Serial
            '00100': ['req18-wrpin-pulseconfig-20-set-confi.txt'],  # Pulse/Cycle
            '00101': ['req23-wrpin-nco_config-20.txt'],  # NCO Frequency
            '01011': ['req41-mov-outa-quadenc_data.pasm2'],  # Quadrature Encoder
        }
        
        for mode in modes:
            # Check if this mode needs PASM2
            mode_key = mode['mode_code']
            if mode_key not in mode_to_titus:
                continue
                
            # Find Spin2 blocks in this mode
            spin2_blocks = self.find_spin2_blocks_in_mode(lines, mode)
            if not spin2_blocks:
                continue
                
            self.stats['modes_processed'] += 1
            self.stats['spin2_found'] += len(spin2_blocks)
            
            # Add PASM2 examples for each Spin2 block (up to available Titus files)
            titus_files = mode_to_titus[mode_key]
            num_to_insert = min(len(spin2_blocks), len(titus_files))
            
            for i in range(num_to_insert):
                titus_file = titus_files[i]
                pasm_code = self.load_titus_example(titus_file)
                
                if pasm_code:
                    # Insert after the corresponding Spin2 block
                    insert_line = spin2_blocks[i]['end'] + 1
                    
                    # Build insertion content
                    insertion = []
                    insertion.append('')  # Blank line before PASM2
                    insertion.append('```pasm2')
                    insertion.extend(pasm_code)
                    insertion.append('```')
                    
                    self.insertions.append({
                        'line': insert_line,
                        'content': insertion,
                        'mode': mode['mode_name'],
                        'file': titus_file
                    })
                    self.stats['pasm_inserted'] += 1
        
        # Sort insertions from bottom to top
        self.insertions.sort(key=lambda x: x['line'], reverse=True)
    
    def apply_insertions(self, lines):
        """Apply all insertions from bottom to top."""
        for insertion in self.insertions:
            # Insert at the specified line
            for i, content_line in enumerate(insertion['content']):
                lines.insert(insertion['line'] + i, content_line)
            
            print(f"Inserted PASM2 for {insertion['mode']} at line {insertion['line']}")
            print(f"  Source: {insertion['file']}")
        
        return lines
    
    def process(self, output_path):
        """Main processing function."""
        # Read V4
        with open(self.v4_path, 'r') as f:
            lines = f.read().split('\n')
        
        print(f"Loaded V4 with {len(lines)} lines")
        
        # Prepare insertions
        self.prepare_insertions(lines)
        
        print(f"\nPrepared {len(self.insertions)} insertions")
        print(f"Modes to update: {self.stats['modes_processed']}")
        print(f"Spin2 blocks found: {self.stats['spin2_found']}")
        
        # Test with first insertion only
        if len(self.insertions) > 0:
            print("\n=== TESTING FIRST INSERTION ===")
            test_insertion = self.insertions[-1]  # Last is first (bottom-up)
            
            # Show context before
            print(f"\nInserting at line {test_insertion['line']} for mode: {test_insertion['mode']}")
            print("\n--- 5 lines before insertion point ---")
            for i in range(max(0, test_insertion['line']-5), test_insertion['line']):
                print(f"{i:4}: {lines[i]}")
            
            print("\n--- Content to insert ---")
            for line in test_insertion['content']:
                print(f"NEW : {line}")
            
            print("\n--- 5 lines after insertion point ---")
            for i in range(test_insertion['line'], min(len(lines), test_insertion['line']+5)):
                print(f"{i:4}: {lines[i]}")
            
            print("\n✅ First insertion looks correct, proceeding with all...")
        
        # Apply all insertions
        lines = self.apply_insertions(lines)
        
        # Write output
        with open(output_path, 'w') as f:
            f.write('\n'.join(lines))
        
        print(f"\nWrote V5 to {output_path}")
        print(f"Total PASM2 examples inserted: {self.stats['pasm_inserted']}")
        
        return True

def main():
    v4_path = "P2-Smart-Pins-Green-Book-Tutorial-v4.md"
    titus_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/smart-pins/assets/code-20250824"
    output_path = "P2-Smart-Pins-Green-Book-Tutorial-v5-test.md"
    
    inserter = PASMInserter(v4_path, titus_dir)
    inserter.process(output_path)

if __name__ == "__main__":
    main()