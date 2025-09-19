#!/usr/bin/env python3
"""
Fix AND/ANDN extraction with correct content.
"""

import yaml
from pathlib import Path

# Paths
PASM2_PATH = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/pasm2")

# Correct content for AND/ANDN
correct_data = {
    'brief_description': 'And not',
    'category': 'Bit Operation Instruction - Bitwise AND a value with another, or with the NOT of another.',
    'description': '''AND or ANDN performs a bitwise AND of the value in Src (or !Src) into that of Dest. Result: Dest AND Src (or Dest AND !Src) is stored in Dest and flags are optionally updated with parity and zero status.

If the WC or WCZ effect is specified, the C flag is set (1) if the result contains an odd number of high (1) bits, or is cleared (0) if it contains an even number of high bits.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the Dest AND Src (or Dest AND !Src) equals zero, or is cleared (0) if it is non-zero.''',
    'parameters': [
        'Dest is the register containing the value to bitwise AND with Src (or with !Src) and is the destination in which to write the result.',
        'Src is a register, 9-bit literal, or 32-bit augmented literal whose value (or inverse value) will be bitwise ANDed into Dest.',
        'WC, WZ, or WCZ are optional effects to update flags.'
    ],
    'documentation_source': 'PASM2 Manual 2022/11/01 Page 49',
    'documentation_level': 'comprehensive',
    'manual_extraction_date': '2025-01-19',
    'last_updated': '2025-01-19'
}

# Fix AND
print("Fixing AND...")
and_path = PASM2_PATH / "and.yaml"
with open(and_path, 'r') as f:
    and_data = yaml.safe_load(f) or {}

# Update with correct content
and_data.update(correct_data)
and_data['instruction'] = 'AND'
and_data['syntax'] = 'AND     D,{#}S   {WC/WZ/WCZ}'
and_data['encoding'] = 'EEEE 0101000 CZI DDDDDDDDD SSSSSSSSS'
and_data['grouped_with'] = ['AND', 'ANDN']
and_data['group_documentation'] = True

# Preserve compiler fields
if 'compiler_operand_format' in and_data:
    pass  # Keep existing
if 'compiler_encoding' in and_data:
    pass  # Keep existing
if 'enhancement_source' in and_data:
    pass  # Keep existing

with open(and_path, 'w') as f:
    yaml.dump(and_data, f, default_flow_style=False, sort_keys=False, width=100)

print("  ✓ Fixed AND")

# Fix ANDN
print("Fixing ANDN...")
andn_path = PASM2_PATH / "andn.yaml"
with open(andn_path, 'r') as f:
    andn_data = yaml.safe_load(f) or {}

# Update with correct content
andn_data.update(correct_data)
andn_data['instruction'] = 'ANDN'
andn_data['syntax'] = 'ANDN    D,{#}S   {WC/WZ/WCZ}'
andn_data['encoding'] = 'EEEE 0101001 CZI DDDDDDDDD SSSSSSSSS'
andn_data['grouped_with'] = ['AND', 'ANDN']
andn_data['group_documentation'] = True

# Preserve compiler fields
if 'compiler_operand_format' in andn_data:
    pass  # Keep existing
if 'compiler_encoding' in andn_data:
    pass  # Keep existing
if 'enhancement_source' in andn_data:
    pass  # Keep existing

with open(andn_path, 'w') as f:
    yaml.dump(andn_data, f, default_flow_style=False, sort_keys=False, width=100)

print("  ✓ Fixed ANDN")

print("\nBoth instructions now have correct documentation from manual page 49.")