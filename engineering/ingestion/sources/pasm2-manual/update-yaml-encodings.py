#!/usr/bin/env python3
"""
Update PASM2 instruction YAML files with properly structured encoding table data.

Replaces the old corrupted 'encoding' field with:
- encoding: [list of properly parsed rows]
- encoding_notes: [list of footnotes, if any]
"""

import json
import re
from pathlib import Path
import yaml
from collections import OrderedDict


def represent_ordereddict(dumper, data):
    """Custom YAML representer to maintain field order."""
    return dumper.represent_dict(data.items())

# Register the custom representer
yaml.add_representer(OrderedDict, represent_ordereddict)


def parse_encoding_row(row_data):
    """Extract the 5 columns from a table row."""
    line = row_data['line'].strip()
    cont = row_data.get('continuation', '').strip()

    # Extract encoding - try multiple patterns
    # Pattern 1: Standard - encoding fields separated by 1-3 spaces, then 3+ spaces before write column
    match = re.match(r'\s*(EEEE(?:\s{1,3}[\dA-Z]+)+)\s{3,}(.*)$', line)

    if not match:
        # Pattern 2: Encoding with exactly 5 fields (EEEE OPCODE FX DEST SRC)
        # This handles cases where write column has spaces (no 2+ space separator)
        match = re.match(r'\s*(EEEE\s+\S+\s+\S+\s+\S+\s+\S+)\s+(.*)$', line)

    if not match:
        return None

    encoding = match.group(1).strip()
    line_remainder = match.group(2).strip()

    # If there's a continuation line, handle it specially
    if cont:
        # Line has: encoding + write column
        # Continuation has: c, z, clocks (aligned at their column positions)
        result = {
            'bits': encoding,
            'write': line_remainder  # Everything after encoding is the write column
        }

        # Parse continuation for c, z, clocks
        cont_parts = re.split(r'\s{2,}', cont)
        cont_parts = [p.strip() for p in cont_parts if p.strip()]

        if len(cont_parts) >= 1:
            result['c'] = cont_parts[0]
        if len(cont_parts) >= 2:
            result['z'] = cont_parts[1]
        if len(cont_parts) >= 3:
            # Handle complex clock expressions (might span multiple parts)
            result['clocks'] = ' '.join(cont_parts[2:])
    else:
        # No continuation - all data is on one line
        # Split remainder on 2+ spaces to get columns
        parts = re.split(r'\s{2,}', line_remainder)
        parts = [p.strip() for p in parts if p.strip()]

        result = {
            'bits': encoding,
            'write': parts[0] if len(parts) > 0 else '',
            'c': parts[1] if len(parts) > 1 else '',
            'z': parts[2] if len(parts) > 2 else '',
            'clocks': parts[3] if len(parts) > 3 else ''
        }

        # Handle complex clocks that might be in parts[4+]
        if len(parts) > 4:
            result['clocks'] = ' '.join(parts[3:])

    # Clean up empty values
    return {k: v for k, v in result.items() if v}


def update_yaml_file(instruction_name, table_data, yaml_dir, output_dir):
    """Update a single YAML file with new encoding data."""
    
    # Find the YAML file (case-insensitive)
    yaml_file = yaml_dir / f"{instruction_name.lower()}.yaml"
    
    if not yaml_file.exists():
        print(f"  ⚠️  YAML not found: {yaml_file.name}")
        return None
    
    # Load existing YAML
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Remove old encoding field if it exists
    if 'encoding' in data:
        old_encoding = data.pop('encoding')
        if isinstance(old_encoding, str):
            # Single-line corruption - good, we're replacing it
            pass
        elif isinstance(old_encoding, list):
            # Already has list format - check if it's our new format
            if old_encoding and isinstance(old_encoding[0], dict) and 'bits' in old_encoding[0]:
                print(f"  ℹ️  {instruction_name}: Already has new encoding format, skipping")
                return None
    
    # Parse encoding rows
    encoding_rows = []
    for row in table_data['rows']:
        parsed = parse_encoding_row(row)
        if parsed:
            encoding_rows.append(parsed)
    
    if not encoding_rows:
        print(f"  ⚠️  {instruction_name}: Could not parse encoding rows")
        return None
    
    # Build new structure (preserve order of original fields where possible)
    new_data = OrderedDict()
    
    # Copy fields in a good order
    field_order = [
        'instruction', 'syntax', 'brief_description', 'category', 
        'description', 'result', 'parameters', 'flags_affected',
        'syntax_variants', 'usage_notes', 'timing',
        'documentation_source', 'documentation_level',
        'compiler_operand_format', 'compiler_encoding',
        'enhancement_source', 'last_updated', 'manual_extraction_date',
        'oneliner'
    ]
    
    # Add existing fields in preferred order
    for field in field_order:
        if field in data:
            new_data[field] = data[field]
    
    # Add any remaining fields not in our order list
    for key, value in data.items():
        if key not in new_data and key != 'encoding':
            new_data[key] = value
    
    # Now insert encoding right after timing (if it exists) or after syntax
    insert_after = 'timing' if 'timing' in new_data else 'syntax'
    
    # Find insertion point
    keys = list(new_data.keys())
    if insert_after in keys:
        insert_idx = keys.index(insert_after) + 1
    else:
        insert_idx = 2  # After instruction and syntax
    
    # Create final ordered dict with encoding inserted
    final_data = OrderedDict()
    for i, key in enumerate(keys[:insert_idx]):
        final_data[key] = new_data[key]
    
    # Add encoding with comment
    final_data['encoding'] = encoding_rows
    
    # Add remaining fields
    for key in keys[insert_idx:]:
        final_data[key] = new_data[key]
    
    # Add encoding notes if there are footnotes
    if table_data['footnotes']:
        notes = [fn['text'] for fn in table_data['footnotes']]
        # Insert encoding_notes right after encoding
        final_data_with_notes = OrderedDict()
        for key, value in final_data.items():
            final_data_with_notes[key] = value
            if key == 'encoding':
                final_data_with_notes['encoding_notes'] = notes
        final_data = final_data_with_notes
    
    # Write to output directory
    output_file = output_dir / f"{instruction_name.lower()}.yaml"
    
    # Custom dump with comment
    yaml_content = yaml.dump(final_data, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    # Add comment to encoding line
    yaml_content = yaml_content.replace(
        'encoding:',
        'encoding:  # [bits|write|c|z|clocks] See encoding-table-reference.yaml'
    )
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    
    return output_file


def main():
    # Paths
    script_dir = Path(__file__).parent
    tables_file = script_dir / 'extracted-instruction-tables.json'
    yaml_dir = Path('/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/language/pasm2')
    output_dir = script_dir / 'updated-yamls'
    
    # Load extracted tables
    with open(tables_file, 'r', encoding='utf-8') as f:
        tables = json.load(f)
    
    print(f"Updating YAML files with encoding table data...")
    print(f"Source: {tables_file}")
    print(f"YAML dir: {yaml_dir}")
    print(f"Output: {output_dir}")
    print("=" * 80)
    
    updated = []
    skipped = []
    errors = []
    
    for table in tables:
        instruction = table['instruction']
        
        try:
            result = update_yaml_file(instruction, table, yaml_dir, output_dir)
            if result:
                updated.append(instruction)
                print(f"✓ {instruction:15} -> {result.name}")
            else:
                skipped.append(instruction)
        except Exception as e:
            errors.append((instruction, str(e)))
            print(f"✗ {instruction:15} ERROR: {e}")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Updated: {len(updated)} files")
    print(f"Skipped: {len(skipped)} files")
    print(f"Errors:  {len(errors)} files")
    
    if errors:
        print("\nErrors:")
        for instr, error in errors:
            print(f"  {instr}: {error}")
    
    if skipped:
        print(f"\nSkipped: {', '.join(skipped[:10])}" + ("..." if len(skipped) > 10 else ""))


if __name__ == '__main__':
    main()
