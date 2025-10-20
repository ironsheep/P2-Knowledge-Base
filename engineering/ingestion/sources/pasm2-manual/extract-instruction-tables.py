#!/usr/bin/env python3
"""
Extract instruction decoding tables from PASM2 manual .txt file.

Each table has:
- Header: COND INSTR FX DEST SRC | Write | C Flag | Z Flag | Clocks
- 1+ rows starting with " EEEE" (may span 2 lines)
- Optional footnotes (number + text)
"""

import re
import json
from pathlib import Path


def find_instruction_name(lines, table_line_num, lookback=50):
    """Find the instruction name by looking back from the table."""
    for i in range(table_line_num - 1, max(0, table_line_num - lookback), -1):
        line = lines[i].strip()
        
        # Skip empty lines and common non-instruction lines
        if not line or line.startswith('●') or line.startswith('Result:'):
            continue
            
        # Look for instruction name patterns (ALL CAPS, possibly with operands)
        match = re.match(r'^([A-Z][A-Z0-9]+)\b', line)
        if match:
            instruction = match.group(1)
            # Avoid section headers and common words
            if instruction not in ['COND', 'INSTR', 'EEEE', 'EXPLANATION', 'RESULT']:
                return instruction, line
    
    return None, None


def extract_tables(txt_file):
    """Extract all instruction decoding tables from the text file."""
    
    with open(txt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    tables = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a table header
        if re.match(r'^COND\s+INSTR.*FX.*DEST.*SRC', line):
            # Found a table!
            instruction, full_instruction_line = find_instruction_name(lines, i)
            
            table = {
                'line_number': i + 1,  # 1-based
                'instruction': instruction,
                'instruction_line': full_instruction_line,
                'header': line.strip(),
                'rows': [],
                'footnotes': []
            }
            
            i += 1  # Move to next line after header
            
            # Collect all EEEE rows (which may span 2 lines)
            while i < len(lines):
                row_line = lines[i]
                
                if row_line.strip().startswith('EEEE'):
                    # This is an EEEE row
                    row_data = {'line': row_line.rstrip('\n')}
                    i += 1
                    
                    # Check if next line is a continuation (heavily indented, no EEEE)
                    if i < len(lines):
                        next_line = lines[i]
                        # Continuation lines are very indented and start with whitespace
                        # They contain the C Flag, Z Flag, Clocks columns
                        if (next_line.startswith(' ' * 50) and 
                            not next_line.strip().startswith('EEEE') and
                            next_line.strip() and
                            not re.match(r'^\d+$', next_line.strip())):
                            row_data['continuation'] = next_line.rstrip('\n')
                            i += 1
                    
                    table['rows'].append(row_data)
                    
                elif row_line.strip() == '':
                    # Blank line
                    i += 1
                    continue
                else:
                    # Not an EEEE row, check for footnotes
                    break
            
            # Check for footnotes
            # Footnotes are: standalone number on a line, followed by indented text
            while i < len(lines):
                line_stripped = lines[i].strip()
                
                # Check if this is a footnote marker (just a number, typically 1-3 digits)
                if re.match(r'^\d{1,2}$', line_stripped):
                    footnote_num = line_stripped
                    i += 1
                    
                    # Collect footnote text (indented lines that follow)
                    footnote_text = []
                    while i < len(lines):
                        footnote_line = lines[i]
                        # Footnote text is indented (starts with spaces) and not empty
                        if footnote_line.startswith('    ') and footnote_line.strip():
                            footnote_text.append(footnote_line.strip())
                            i += 1
                        elif footnote_line.strip() == '':
                            # Blank line within or after footnote
                            i += 1
                            # Check if next line is also footnote text or if we're done
                            if i < len(lines) and lines[i].startswith('    ') and lines[i].strip():
                                continue  # More footnote text
                            else:
                                break  # End of footnote
                        else:
                            break  # End of footnote
                    
                    table['footnotes'].append({
                        'number': footnote_num,
                        'text': ' '.join(footnote_text)
                    })
                    
                elif line_stripped.startswith('Explanation:') or line_stripped == '':
                    # End of table section
                    i += 1
                    break
                else:
                    i += 1
                    break
            
            tables.append(table)
        else:
            i += 1
    
    return tables


def parse_row_columns(row_data):
    """
    Parse a table row into the 5 columns: INSTR encoding, Write, C Flag, Z Flag, Clocks.
    
    Returns dict with column values or None if can't parse.
    """
    line = row_data['line'].strip()
    continuation = row_data.get('continuation', '').strip()
    
    # The first line after EEEE contains the encoding and sometimes the Write column
    # The continuation line (if present) contains C Flag, Z Flag, Clocks
    
    # Split on multiple spaces to find column boundaries
    parts = re.split(r'\s{2,}', line)
    cont_parts = re.split(r'\s{2,}', continuation) if continuation else []
    
    # Extract encoding (everything up to the Write column)
    # The encoding is: EEEE + binary/letter patterns
    match = re.match(r'(EEEE\s+[\d\sA-Z]+)\s{2,}(.+)', line)
    if not match:
        return None
    
    encoding = match.group(1).strip()
    remainder = match.group(2).strip()
    
    # The remainder and continuation contain: Write, C Flag, Z Flag, Clocks
    all_parts = [remainder] + cont_parts if continuation else remainder.split()
    
    result = {
        'encoding': encoding,
        'write': None,
        'c_flag': None,
        'z_flag': None,
        'clocks': None,
        'raw_line': line,
        'raw_continuation': continuation
    }
    
    # For now, just store the raw data and let user parse it
    # The column alignment varies too much for reliable parsing
    if len(all_parts) >= 4:
        result['write'] = all_parts[0] if len(all_parts) > 0 else None
        result['c_flag'] = all_parts[1] if len(all_parts) > 1 else None
        result['z_flag'] = all_parts[2] if len(all_parts) > 2 else None
        result['clocks'] = all_parts[3] if len(all_parts) > 3 else None
    
    return result


def main():
    # File paths
    script_dir = Path(__file__).parent
    txt_file = script_dir / 'pasm2-manual-narrative.txt'
    output_file = script_dir / 'extracted-instruction-tables.json'
    
    print(f"Extracting tables from: {txt_file}")
    tables = extract_tables(txt_file)
    
    # Add parsed column data
    for table in tables:
        for row in table['rows']:
            parsed = parse_row_columns(row)
            if parsed:
                row['parsed'] = parsed
    
    print(f"\nFound {len(tables)} tables")
    total_rows = sum(len(t['rows']) for t in tables)
    print(f"Total rows: {total_rows}")
    print(f"Tables with footnotes: {sum(1 for t in tables if t['footnotes'])}")
    
    # Print first few examples
    print("\n" + "="*80)
    print("Sample extractions:")
    print("="*80)
    
    for i, table in enumerate(tables[:5]):
        print(f"\n{i+1}. Instruction: {table['instruction']}")
        print(f"   Line: {table['line_number']}")
        print(f"   Rows: {len(table['rows'])}")
        print(f"   Footnotes: {len(table['footnotes'])}")
        if table['rows']:
            row = table['rows'][0]
            print(f"   First row: {row['line'][:80]}...")
            if 'continuation' in row:
                print(f"              {row['continuation'][:80]}...")
        if table['footnotes']:
            for fn in table['footnotes']:
                print(f"   Footnote {fn['number']}: {fn['text'][:60]}...")
    
    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tables, f, indent=2)
    
    print(f"\n\nSaved all tables to: {output_file}")
    
    # Also create a summary
    summary_file = script_dir / 'extraction-summary.txt'
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("PASM2 Instruction Table Extraction Summary\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total tables extracted: {len(tables)}\n")
        f.write(f"Total rows: {total_rows}\n")
        f.write(f"Tables with footnotes: {sum(1 for t in tables if t['footnotes'])}\n")
        f.write(f"Multi-line rows: {sum(1 for t in tables for r in t['rows'] if 'continuation' in r)}\n\n")
        
        f.write("Instructions with tables:\n")
        f.write("-" * 80 + "\n")
        for table in tables:
            multi_line = sum(1 for r in table['rows'] if 'continuation' in r)
            f.write(f"{table['instruction']:15} Line {table['line_number']:5} "
                   f"Rows: {len(table['rows'])} MultiLine: {multi_line} "
                   f"Footnotes: {len(table['footnotes'])}\n")
    
    print(f"Summary written to: {summary_file}")


if __name__ == '__main__':
    main()
