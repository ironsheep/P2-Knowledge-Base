#!/usr/bin/env python3
import json
import os
from pathlib import Path

# Load JSON data
json_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/external-inputs/from-pnut-ts/SPIN2-Language-Specification.json"
with open(json_path) as f:
    data = json.load(f)

# Output directory
operator_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/spin2/operators"

# Map of missing operators to create (31 total)
missing_operators = {
    'BMASK': {'filename': 'op_BMASK.yaml', 'description': 'Create bit mask from bit count (also PASM2 instruction)'},
    'DECOD': {'filename': 'op_DECOD.yaml', 'description': 'Decode bit position to mask (also PASM2 instruction)'},
    'ENCOD': {'filename': 'op_ENCOD.yaml', 'description': 'Encode highest bit position (also PASM2 instruction)'},
    'FABS': {'filename': 'op_FABS.yaml', 'description': 'Floating point absolute value'},
    'FSQRT': {'filename': 'op_FSQRT.yaml', 'description': 'Floating point square root'},
    'ONES': {'filename': 'op_ONES.yaml', 'description': 'Count number of 1 bits (also PASM2 instruction)'},
    'QEXP': {'filename': 'op_QEXP.yaml', 'description': 'Quick exponential (also PASM2 instruction)'},
    'QLOG': {'filename': 'op_QLOG.yaml', 'description': 'Quick logarithm (also PASM2 instruction)'},
    'SQRT': {'filename': 'op_SQRT.yaml', 'description': 'Integer square root'},
    '|': {'filename': 'op_or.yaml', 'description': 'Bitwise OR'},
    '+//': {'filename': 'op_addmodulo.yaml', 'description': 'Unsigned remainder (modulo)'},
    'FRAC': {'filename': 'op_FRAC.yaml', 'description': 'Calculate fraction'},
    'SCA': {'filename': 'op_SCA.yaml', 'description': 'Scale value (also PASM2 instruction)'},
    'SCAS': {'filename': 'op_SCAS.yaml', 'description': 'Scale value signed (also PASM2 instruction)'},
    'ADDBITS': {'filename': 'op_ADDBITS.yaml', 'description': 'Add bit count to pin number'},
    'ADDPINS': {'filename': 'op_ADDPINS.yaml', 'description': 'Add pin count to pin number'},
    '<.': {'filename': 'op_ltdot.yaml', 'description': 'Floating point less than comparison'},
    '<=.': {'filename': 'op_lteqdot.yaml', 'description': 'Floating point less than or equal comparison'},
    '<>.': {'filename': 'op_ltgtdot.yaml', 'description': 'Floating point inequality comparison'},
    '==.': {'filename': 'op_eqeqdot.yaml', 'description': 'Floating point equality comparison'},
    '>.': {'filename': 'op_gtdot.yaml', 'description': 'Floating point greater than comparison'},
    '>=.': {'filename': 'op_gteqdot.yaml', 'description': 'Floating point greater than or equal comparison'},
    'NOT': {'filename': 'op_NOT.yaml', 'description': 'Logical NOT (also PASM2 instruction)'},
    'AND': {'filename': 'op_AND.yaml', 'description': 'Logical AND (also PASM2 instruction)'},
    '^^': {'filename': 'op_xorxor.yaml', 'description': 'Logical XOR operator'},
    'XOR': {'filename': 'op_XOR.yaml', 'description': 'Logical XOR (also PASM2 instruction)'},
    '||': {'filename': 'op_oror.yaml', 'description': 'Logical OR operator'},
    'OR': {'filename': 'op_OR.yaml', 'description': 'Logical OR (also PASM2 instruction)'},
    '? :': {'filename': 'op_ternary.yaml', 'description': 'Ternary conditional operator'},
    ':=': {'filename': 'op_assign.yaml', 'description': 'Assignment operator'},
    ':=:': {'filename': 'op_swap.yaml', 'description': 'Swap operator'}
}

# Get full operator data from JSON
operator_map = {}
for op in data.get('operators', []):
    symbol = op.get('symbol')
    if symbol:
        operator_map[symbol] = op

# Create YAML files for missing operators
created_count = 0
for symbol, file_info in missing_operators.items():
    filepath = os.path.join(operator_dir, file_info['filename'])
    
    # Get operator data from JSON if available
    op_data = operator_map.get(symbol, {})
    
    # Determine category
    category = op_data.get('category', 'Unknown')
    if category == 'Unknown':
        # Infer category from operator type
        if symbol in ['BMASK', 'DECOD', 'ENCOD', 'ONES', 'QEXP', 'QLOG', 'SCA', 'SCAS', 'NOT', 'AND', 'XOR', 'OR']:
            category = 'Unary'
        elif symbol in ['FABS', 'FSQRT', 'SQRT', 'FRAC']:
            category = 'Math'
        elif symbol in ['<.', '<=.', '<>.', '==.', '>.', '>=.']:
            category = 'Float Compare'
        elif symbol in ['|', '||', '^^']:
            category = 'Bitwise'
        elif symbol in ['+//']:
            category = 'Arithmetic'
        elif symbol in ['ADDBITS', 'ADDPINS']:
            category = 'Pin'
        elif symbol in ['? :', ':=', ':=:']:
            category = 'Assignment'
    
    # Build YAML content
    yaml_content = f'''operator: "{symbol}"
type: operator
description: |
  {file_info['description']}
category: {category}'''
    
    # Add syntax if available
    if op_data.get('syntax'):
        yaml_content += f"\nsyntax: \"{op_data['syntax']}\""
    
    # Add examples if available
    if op_data.get('examples'):
        yaml_content += "\nexamples:"
        for example in op_data['examples']:
            yaml_content += f'\n  - "{example}"'
    
    # Write the file
    with open(filepath, 'w') as f:
        f.write(yaml_content)
    created_count += 1
    print(f"Created: {file_info['filename']}")

print(f"\nSuccessfully created {created_count} operator YAML files")