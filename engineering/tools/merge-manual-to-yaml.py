#!/usr/bin/env python3
"""
Merge PASM2 manual content into instruction YAML files.

This script extracts detailed instruction documentation from the PASM2 manual
and merges it into the existing minimal YAML files, creating rich documentation
for AI consumption.
"""

import yaml
import re
import sys
from pathlib import Path
from typing import Dict, Optional, List

class ManualToYamlMerger:
    def __init__(self, manual_path: str, yaml_dir: str):
        self.manual_path = Path(manual_path)
        self.yaml_dir = Path(yaml_dir)
        self.manual_content = ""
        
    def load_manual(self):
        """Load the manual content"""
        with open(self.manual_path, 'r', encoding='utf-8') as f:
            self.manual_content = f.read()
            
    def extract_instruction_section(self, instruction: str) -> Optional[Dict]:
        """Extract detailed content for a specific instruction from the manual"""
        
        # Try multiple patterns to find instruction sections
        patterns = [
            rf'^{instruction.upper()}\s+[A-Z]',  # Instruction followed by description
            rf'^{instruction.upper()}\n',        # Just instruction on its own line
            rf'^{instruction.upper()}\s'         # Instruction with any whitespace
        ]
        
        match = None
        for pattern in patterns:
            match = re.search(pattern, self.manual_content, re.MULTILINE)
            if match:
                break
                
        if not match:
            return None
            
        start = match.start()
        
        # Find the next instruction (to know where this one ends)
        # Look for next all-caps line that could be an instruction
        next_pattern = r'^[A-Z][A-Z0-9/]+\n'
        next_match = re.search(next_pattern, self.manual_content[match.end():], re.MULTILINE)
        
        if next_match:
            end = match.end() + next_match.start()
        else:
            # Take reasonable chunk if no next instruction found
            end = start + 5000
            
        section = self.manual_content[start:end]
        
        # Parse the section
        return self.parse_instruction_section(section, instruction)
        
    def parse_instruction_section(self, section: str, instruction: str) -> Dict:
        """Parse an instruction section into structured data"""
        
        result = {}
        
        # Extract title (usually second line)
        lines = section.split('\n')
        if len(lines) > 1:
            result['title'] = lines[1].strip()
            
        # Extract category (usually third line, contains "Instruction")
        if len(lines) > 2:
            for line in lines[2:5]:
                if 'Instruction' in line:
                    result['category'] = line.strip()
                    break
                    
        # Extract detailed explanation
        explanation_match = re.search(r'Explanation:(.*?)(?:Related:|$)', section, re.DOTALL)
        if explanation_match:
            result['detailed_explanation'] = explanation_match.group(1).strip()
            
        # Extract related instructions
        related_match = re.search(r'Related:\s*(.*?)(?:\n\n|$)', section)
        if related_match:
            related = related_match.group(1).strip()
            result['related_instructions'] = [i.strip() for i in related.split(',')]
            
        # Extract examples if present
        if 'Example' in section:
            result['has_examples'] = True
            
        # Extract result description
        result_match = re.search(r'Result:\s*(.*?)(?:\n\n|$)', section, re.DOTALL)
        if result_match:
            result['detailed_operation'] = result_match.group(1).strip()
            
        return result
        
    def enhance_yaml(self, instruction: str) -> bool:
        """Enhance a single instruction YAML file with manual content"""
        
        yaml_path = self.yaml_dir / f"{instruction.lower()}.yaml"
        
        if not yaml_path.exists():
            print(f"Warning: {yaml_path} does not exist")
            return False
            
        # Load existing YAML
        try:
            with open(yaml_path, 'r') as f:
                yaml_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"YAML error in {yaml_path}: {e}")
            return False
            
        # Extract manual content
        manual_data = self.extract_instruction_section(instruction)
        
        if not manual_data:
            print(f"No manual content found for {instruction}")
            return False
            
        # Merge manual content into YAML
        if 'title' in manual_data:
            yaml_data['title'] = manual_data['title']
            
        if 'category' in manual_data:
            yaml_data['category'] = manual_data['category']
            
        if 'detailed_operation' in manual_data:
            yaml_data['detailed_operation'] = manual_data['detailed_operation']
            
        if 'detailed_explanation' in manual_data:
            yaml_data['notes'] = manual_data.get('notes', '') + '\n\n' + manual_data['detailed_explanation']
            
        if 'related_instructions' in manual_data:
            yaml_data['related_instructions'] = manual_data['related_instructions']
            
        # Mark as enhanced
        yaml_data['manual_reference'] = {
            'status': 'enhanced_from_manual',
            'manual_version': '2022/11/01'
        }
        
        # Write enhanced YAML
        with open(yaml_path, 'w') as f:
            yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False, width=100)
            
        print(f"Enhanced {instruction}")
        return True
        
    def process_all_instructions(self, instruction_list: Optional[List[str]] = None):
        """Process all instructions or a specific list"""
        
        if instruction_list is None:
            # Get all YAML files
            instruction_list = [f.stem.upper() for f in self.yaml_dir.glob("*.yaml") 
                               if not f.stem == 'concepts']
                               
        success = 0
        failed = 0
        
        for instruction in instruction_list:
            if self.enhance_yaml(instruction):
                success += 1
            else:
                failed += 1
                
        print(f"\nProcessed {success + failed} instructions:")
        print(f"  Enhanced: {success}")
        print(f"  Skipped: {failed}")
        

def main():
    # Paths
    manual_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/pasm2-manual/pasm2-manual-narrative.txt"
    yaml_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/pasm2"
    
    merger = ManualToYamlMerger(manual_path, yaml_dir)
    merger.load_manual()
    
    # Process all instructions
    print("Processing all PASM2 instructions...")
    merger.process_all_instructions()
    

if __name__ == "__main__":
    main()