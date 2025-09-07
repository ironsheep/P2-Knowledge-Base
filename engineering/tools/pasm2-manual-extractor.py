#!/usr/bin/env python3
"""
Extract PASM2 manual content into separate YAML files for comparison - Version 3.
This version handles page breaks and extracts content more accurately.

This script extracts instruction documentation from the PASM2 manual
and saves it to separate YAML files for review before merging.
"""

import yaml
import re
import sys
from pathlib import Path
from typing import Dict, Optional, List, Tuple

class ManualExtractor:
    def __init__(self, manual_path: str, output_dir: str):
        self.manual_path = Path(manual_path)
        self.output_dir = Path(output_dir)
        self.manual_content = ""
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def load_manual(self):
        """Load the manual content"""
        with open(self.manual_path, 'r', encoding='utf-8') as f:
            self.manual_content = f.read()
            
        print(f"Loaded manual: {len(self.manual_content)} characters")
        
        # Clean up form feeds and other special characters that might interfere
        # But keep track of where they were for reference
        self.page_breaks = [m.start() for m in re.finditer(r'\x0c', self.manual_content)]
        print(f"Found {len(self.page_breaks)} page breaks in manual")
            
    def find_detailed_instruction_sections(self) -> Dict[str, dict]:
        """Find detailed instruction documentation sections"""
        
        instructions = {}
        
        # Pattern for detailed instruction sections with page break handling:
        # Might have \x0c (form feed) before instruction name
        # Line 1: Instruction name alone (e.g., "ADD")
        # Line 2: Short title (e.g., "Add")
        # Line 3: Category with "Instruction" (e.g., "Math Instruction - Add two unsigned values.")
        
        # Allow for optional page break before instruction
        pattern = r'(?:\x0c)?([A-Z][A-Z0-9/]+)\n([^\n]+?)\n([^\n]*?Instruction[^\n]+)'
        
        for match in re.finditer(pattern, self.manual_content):
            instr_name = match.group(1).strip()
            title = match.group(2).strip()
            category = match.group(3).strip()
            
            # Skip if instruction name is too long
            if len(instr_name) > 10:
                continue
                
            # Skip if title is all caps and long (probably another instruction)
            if title.isupper() and len(title) > 15:
                continue
                
            # Skip if title contains "Copyright"
            if 'Copyright' in title or 'Parallax' in title:
                continue
                
            instructions[instr_name] = {
                'start': match.start(),
                'match_end': match.end(),
                'title': title,
                'category': category
            }
            
        print(f"Found {len(instructions)} detailed instruction sections")
            
        # Find the end of each instruction section
        instr_names = sorted(instructions.keys(), key=lambda x: instructions[x]['start'])
        
        for i, name in enumerate(instr_names):
            if i < len(instr_names) - 1:
                next_name = instr_names[i + 1]
                instructions[name]['end'] = instructions[next_name]['start']
            else:
                # Last instruction - take reasonable amount
                instructions[name]['end'] = min(
                    instructions[name]['start'] + 5000,
                    len(self.manual_content)
                )
                
        return instructions
        
    def extract_instruction_content(self, name: str, bounds: dict) -> Dict:
        """Extract structured content for a specific instruction"""
        
        # Get the full section
        section = self.manual_content[bounds['match_end']:bounds['end']]
        
        result = {
            'instruction': name,
            'title': bounds['title'],
            'category': bounds['category']
        }
        
        # Extract syntax line more carefully
        # It should be: INSTRUCTION Dest, {#}Src {effects}
        syntax_pattern = rf'^{name}\s+(.+?)$'
        syntax_match = re.search(syntax_pattern, section, re.MULTILINE)
        if syntax_match:
            syntax = syntax_match.group(1).strip()
            # Make sure it's not another section header
            if not syntax.isupper() or '{' in syntax or ',' in syntax:
                result['syntax'] = f"{name} {syntax}"
            
        # Extract Result section
        result_match = re.search(r'^Result:\s*(.+?)(?=\n\s*●|\n\s*COND|\n\s*\n)', section, re.MULTILINE | re.DOTALL)
        if result_match:
            result_text = result_match.group(1).strip()
            # Clean up
            result_text = re.sub(r'\s+', ' ', result_text)
            result['result'] = result_text
            
        # Extract parameter bullets more carefully
        bullets = []
        # Find the bullet section
        bullets_section_match = re.search(r'(●.+?)(?=\nCOND\s+INSTR|\nRelated:|\nExplanation:)', section, re.DOTALL)
        if bullets_section_match:
            bullets_text = bullets_section_match.group(1)
            # Split by bullet points
            bullet_items = re.split(r'\n\s*●\s*', bullets_text)
            for item in bullet_items:
                item = item.strip()
                if item and not 'Copyright' in item:
                    # Clean up the item
                    item = re.sub(r'\s+', ' ', item)
                    item = item.replace('●', '').strip()
                    if item:
                        bullets.append(item)
        if bullets:
            result['parameters'] = bullets
            
        # Extract the encoding table row
        table_match = re.search(r'EEEE\s+([01]+\s+[A-Z01]+\s+[A-Z01]+\s+[A-Z01]+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\d+)', section)
        if table_match:
            result['encoding'] = f"EEEE {table_match.group(1)}"
            c_flag = table_match.group(2).strip()
            z_flag = table_match.group(3).strip()
            result['c_flag_effect'] = None if c_flag == '—' else c_flag
            result['z_flag_effect'] = None if z_flag == '—' else z_flag
            result['clock_cycles'] = table_match.group(4)
            
        # Extract Related instructions
        related_match = re.search(r'^Related:\s*(.+?)(?=\n\n|\nExplanation:|$)', section, re.MULTILINE | re.DOTALL)
        if related_match:
            related_text = related_match.group(1).strip()
            # Extract instruction names (uppercase words)
            related_list = re.findall(r'\b[A-Z][A-Z0-9/]+\b', related_text)
            if related_list:
                # Filter out common words that aren't instructions
                related_list = [r for r in related_list if len(r) >= 2 and r not in ['WC', 'WZ', 'WCZ', 'PC', 'CT']]
                if related_list:
                    result['related_instructions'] = related_list
            
        # Extract Explanation section - the detailed description
        explanation_match = re.search(r'^Explanation:\s*(.+?)(?=\n\n[A-Z]|\nExample|\n\x0c|$)', section, re.MULTILINE | re.DOTALL)
        if explanation_match:
            explanation = explanation_match.group(1).strip()
            # Clean up
            explanation = re.sub(r'\s+', ' ', explanation)
            # Fix common ligatures
            explanation = explanation.replace('ﬂ', 'fl')
            explanation = explanation.replace('ﬁ', 'fi')
            explanation = explanation.replace('ﬀ', 'ff')
            result['detailed_explanation'] = explanation
            
        # Check for examples
        if re.search(r'^Example', section, re.MULTILINE):
            result['has_examples'] = True
            
        return result
        
    def process_instructions(self, instruction_list: Optional[List[str]] = None):
        """Process instructions and save to separate files"""
        
        print("\nFinding detailed instruction sections...")
        all_instructions = self.find_detailed_instruction_sections()
        
        if instruction_list:
            # Filter to requested instructions
            instructions = {}
            missing = []
            for instr in instruction_list:
                if instr in all_instructions:
                    instructions[instr] = all_instructions[instr]
                else:
                    missing.append(instr)
            
            print(f"Processing {len(instructions)} of {len(instruction_list)} requested instructions")
            if missing:
                print(f"Not found: {', '.join(missing)}")
        else:
            instructions = all_instructions
            print(f"Processing all {len(instructions)} instructions")
            
        success = 0
        failed = []
        
        for name, bounds in sorted(instructions.items()):
            try:
                content = self.extract_instruction_content(name, bounds)
                
                # Save to YAML file
                output_path = self.output_dir / f"{name.lower()}_extracted.yaml"
                with open(output_path, 'w', encoding='utf-8') as f:
                    yaml.dump(content, f, default_flow_style=False, sort_keys=False, 
                             width=100, allow_unicode=True)
                    
                print(f"✓ {name}")
                success += 1
                
            except Exception as e:
                print(f"✗ {name}: {e}")
                failed.append(name)
                
        print(f"\n{'='*50}")
        print(f"Extraction Summary:")
        print(f"  Success: {success} instructions")
        if failed:
            print(f"  Failed: {len(failed)} - {', '.join(failed[:5])}{'...' if len(failed) > 5 else ''}")
        print(f"  Output: {self.output_dir}")
        print(f"{'='*50}")
        

def main():
    # Paths
    manual_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/pasm2-manual/pasm2-manual-narrative.txt"
    output_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/tools/manual-extractions"
    
    extractor = ManualExtractor(manual_path, output_dir)
    extractor.load_manual()
    
    # Extract ALL instructions
    print("\n" + "="*50)
    print("PASM2 Manual Content Extractor v3 - FULL RUN")
    print("="*50)
    
    extractor.process_instructions()  # No filter = all instructions
    
    print("\n✅ Extraction complete")
    

if __name__ == "__main__":
    main()