#!/usr/bin/env python3
import json
import os
from pathlib import Path

# Load JSON data
json_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/external-inputs/from-pnut-ts/SPIN2-Language-Specification.json"
with open(json_path) as f:
    data = json.load(f)

# Get all operators from JSON
json_operators = {op.get('symbol', 'NO_SYMBOL') for op in data.get('operators', [])}

# Get existing operator files
operator_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/spin2/operators"
existing_files = os.listdir(operator_dir)
existing_operators = set()

for f in existing_files:
    if f.endswith('.yaml'):
        # Convert filename to operator symbol
        op = f.replace('op_', '').replace('.yaml', '')
        # Handle special cases
        if op == '\\':
            op = '\\'
        elif op == 'addgt':
            op = '+>'
        elif op == 'addgteq':
            op = '+>='
        elif op == 'addlt':
            op = '+<'
        elif op == 'addlteq':
            op = '+<='
        elif op == 'addlteqgt':
            op = '+<>=>'
        elif op == 'adddiv':
            op = '+/'
        elif op == 'adddot':
            op = '+.'
        elif op == 'and':
            op = '&'
        elif op == 'andand':
            op = '&&'
        elif op == 'colon':
            op = ':'
        elif op == 'dec':
            op = '--'
        elif op == 'div':
            op = '/'
        elif op == 'divdiv':
            op = '//'
        elif op == 'divdot':
            op = '/.'
        elif op == 'eqeq':
            op = '=='
        elif op == 'eqeqeq':
            op = '==='
        elif op == 'gt':
            op = '>'
        elif op == 'gteq':
            op = '>='
        elif op == 'inc':
            op = '++'
        elif op == 'lt':
            op = '<'
        elif op == 'lteq':
            op = '<='
        elif op == 'lteqgt':
            op = '<=>'
        elif op == 'ltgt':
            op = '<>'
        elif op == 'ltshr':
            op = '<<'
        elif op == 'max':
            op = '<#'
        elif op == 'min':
            op = '#>'
        elif op == 'mul':
            op = '*'
        elif op == 'muldot':
            op = '*.'
        elif op == 'not':
            op = '!'
        elif op == 'notandand':
            op = '!!'
        elif op == 'question':
            op = '?'
        elif op == 'rand':
            op = '??'
        elif op == 'shl':
            op = '<<'
        elif op == 'shr':
            op = '>>'
        elif op == 'sub':
            op = '-'
        elif op == 'subdot':
            op = '-.'
        elif op == 'xor':
            op = '^'
        elif op == 'add':
            op = '+'
        elif op == 'modulo_add':
            op = '++'
        else:
            # For named operators like ABS, REV, keep as is
            op = op.upper()
        existing_operators.add(op)

# Find missing operators
missing = json_operators - existing_operators

print(f"Total operators in JSON: {len(json_operators)}")
print(f"Existing operator files: {len(existing_operators)}")
print(f"Missing operators: {len(missing)}")
print("\nMissing operators:")
for op in sorted(missing):
    print(f"  {op}")

# Get full operator data for missing ones
print("\n\nFull data for missing operators:")
for op_data in data.get('operators', []):
    if op_data.get('symbol') in missing:
        print(f"\n{op_data.get('symbol')}:")
        print(f"  Category: {op_data.get('category', 'Unknown')}")
        print(f"  Description: {op_data.get('description', 'No description')}")