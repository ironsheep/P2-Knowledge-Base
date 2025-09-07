#!/usr/bin/env python3
"""
Layer 4: Extract Chip Gracey clarifications for PASM2 instructions
"""

from pathlib import Path
import re

def extract_chip_clarifications():
    """Extract instruction clarifications from Chip Gracey documents"""
    
    # Paths
    clarifications_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/chip-gracey-clarifications")
    pasm2_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/instructions/pasm2")
    
    # Clarification files to process
    clarification_files = [
        "chip-instruction-clarifications-2025-08-18.md",
        "chip-instruction-clarifications-2025-09-02.md"
    ]
    
    clarifications = {}
    
    for filename in clarification_files:
        filepath = clarifications_dir / filename
        if not filepath.exists():
            print(f"Warning: {filename} not found")
            continue
            
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Parse instruction sections
        # Looking for patterns like "### 1. INCMOD - Increment with Modulo"
        sections = re.split(r'^###\s+\d+\.\s+', content, flags=re.MULTILINE)
        
        for section in sections[1:]:  # Skip header section
            lines = section.strip().split('\n')
            if not lines:
                continue
                
            # Parse header line like "INCMOD - Increment with Modulo"
            header = lines[0]
            match = re.match(r'^(\w+)\s+-\s+(.+)$', header)
            if not match:
                continue
                
            mnemonic = match.group(1).upper()
            title = match.group(2)
            
            # Extract content sections
            syntax = ""
            function = ""
            use_cases = ""
            
            current_section = None
            content_lines = []
            
            for line in lines[1:]:
                if line.startswith('**Syntax**:'):
                    current_section = 'syntax'
                    syntax = line.replace('**Syntax**:', '').strip()
                elif line.startswith('**Function**:'):
                    current_section = 'function'
                    function = line.replace('**Function**:', '').strip()
                elif line.startswith('**Use Cases**:'):
                    current_section = 'use_cases'
                elif line.startswith('**') or line.startswith('---'):
                    current_section = None
                elif current_section == 'function' and line.strip():
                    if line.startswith('- '):
                        function += '\n' + line
                    else:
                        function += ' ' + line
                elif current_section == 'use_cases' and line.startswith('- '):
                    use_cases += line + '\n'
            
            if mnemonic not in clarifications:
                clarifications[mnemonic] = {
                    'title': title,
                    'syntax': syntax.strip('`'),
                    'function': function.strip(),
                    'use_cases': use_cases.strip(),
                    'source': filename
                }
    
    # Update YAML files
    updated = 0
    no_file = 0
    
    for mnemonic, clarification in clarifications.items():
        yaml_path = pasm2_dir / f"pasm2_{mnemonic.lower()}.yaml"
        
        if not yaml_path.exists():
            no_file += 1
            print(f"No file for: {mnemonic}")
            continue
            
        # Read existing YAML
        with open(yaml_path, 'r') as f:
            content = f.read()
        
        # Check if layer4_chip already exists
        if 'layer4_chip:' in content:
            continue
            
        # Add layer4_chip section
        func = clarification['function'].replace('"', '\\"')
        uses = clarification['use_cases'].replace('"', '\\"')
        date = clarification['source'].replace('chip-instruction-clarifications-', '').replace('.md', '')
        chip_section = f"""
layer4_chip:
  source: Chip Gracey Clarifications
  title: "{clarification['title']}"
  syntax: "{clarification['syntax']}"
  function: "{func}"
  use_cases: "{uses}"
  date: "{date}"
"""
        
        # Append to file
        with open(yaml_path, 'a') as f:
            f.write(chip_section)
        
        updated += 1
        print(f"Updated: {mnemonic}")
    
    print(f"\nComplete:")
    print(f"  Updated: {updated}")
    print(f"  No file found: {no_file}")
    print(f"  Total clarifications: {len(clarifications)}")

if __name__ == "__main__":
    extract_chip_clarifications()