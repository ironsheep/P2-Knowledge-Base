#!/usr/bin/env python3
"""
Extract documentation from the instruction tables in the PASM2 manual.
The manual has detailed instruction tables around line 8000+.
"""

import re
import yaml
from pathlib import Path

# Instructions marked as weak in the heat map
WEAK_INSTRUCTIONS = [
    'REP', 'JMP', 'RDLONG', 'WRLONG', 'RDBYTE', 'RDWORD', 'WRBYTE', 'WRWORD',
    'POP', 'PUSH', 'RET', 'RETA', 'RETB', 'CALL', 'CALLA', 'CALLB', 
    'CALLPA', 'CALLPB', 'MODC', 'MODZ', 'RDPIN', 'WRPIN', 'WXPIN', 'WYPIN',
    'TESTB', 'AND', 'OR', 'XOR', 'NOT', 'GETCT', 'WAITCT1', 'WAITCT2', 'WAITCT3'
]

def extract_from_tables():
    """Extract from the instruction tables section of the manual."""
    manual_path = '/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources/pasm2-manual/pasm2-manual-narrative.txt'
    
    with open(manual_path, 'r') as f:
        lines = f.readlines()
    
    # Focus on the table section (lines 8000-9000)
    table_section = lines[8000:9000]
    
    output_dir = Path('/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/document-production/manuals/pasm2-reference/instruction-templates/generated')
    output_dir.mkdir(exist_ok=True, parents=True)
    
    found_instructions = {}
    
    for i, line in enumerate(table_section):
        for instr in WEAK_INSTRUCTIONS:
            # Match instruction at start of line
            pattern = f"^{instr}\\s+"
            if re.match(pattern, line):
                # Parse the table line
                # Format appears to be: INSTR params description timing
                parts = line.strip().split(maxsplit=2)
                if len(parts) >= 3:
                    instruction = parts[0]
                    syntax = parts[1] if len(parts) > 1 else ""
                    rest = parts[2] if len(parts) > 2 else ""
                    
                    # Split description and timing
                    # Timing is usually at the end like "2/2" or "4 / 13...20"
                    timing_match = re.search(r'\s+(\d+(?:\.\.\.\d+)?(?:\s*/\s*\d+(?:\.\.\.\d+)?)?)\s*$', rest)
                    if timing_match:
                        description = rest[:timing_match.start()].strip()
                        timing = timing_match.group(1).strip()
                    else:
                        description = rest.strip()
                        timing = ""
                    
                    found_instructions[instruction] = {
                        'syntax': syntax,
                        'description': description,
                        'timing': timing,
                        'line': 8000 + i
                    }
    
    return found_instructions

def create_instruction_template(instr, info):
    """Create a markdown template for an instruction."""
    template = f"""# {instr}
**{info.get('description', 'Instruction').split('.')[0]}**

*Instruction Category* - {info.get('description', '')}

## Syntax
```pasm2
{instr} {info.get('syntax', '')}
```

## Description
{info.get('description', '')}

## Timing
- Clock cycles: {info.get('timing', 'Not specified')}

## Parameters
- TODO: Add parameter descriptions

## Encoding
- TODO: Add encoding table

## Examples
```pasm2
' TODO: Add examples
```

## Related Instructions
- TODO: Add related instructions

## Notes
- Extracted from PASM2 Manual line {info.get('line', 'unknown')}
"""
    return template

def main():
    print("Extracting from instruction tables...")
    instructions = extract_from_tables()
    
    output_dir = Path('/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/document-production/manuals/pasm2-reference/instruction-templates/generated')
    output_dir.mkdir(exist_ok=True, parents=True)
    
    print(f"\nFound {len(instructions)} instructions in tables:\n")
    
    for instr, info in sorted(instructions.items()):
        print(f"✅ {instr:10s} - {info['description'][:60]}...")
        
        # Create template
        template = create_instruction_template(instr, info)
        
        # Save template
        template_file = output_dir / f"{instr}.md"
        with open(template_file, 'w') as f:
            f.write(template)
    
    # Create summary
    summary = f"""# Extracted Instructions Summary

Found {len(instructions)} instructions from the manual tables:

| Instruction | Description | Timing |
|-------------|-------------|--------|
"""
    
    for instr, info in sorted(instructions.items()):
        desc = info['description'][:50] + '...' if len(info['description']) > 50 else info['description']
        summary += f"| {instr} | {desc} | {info['timing']} |\n"
    
    summary_file = output_dir / "extraction-summary.md"
    with open(summary_file, 'w') as f:
        f.write(summary)
    
    print(f"\nCreated {len(instructions)} template files in {output_dir}")

if __name__ == "__main__":
    main()