#!/usr/bin/env python3
"""
Extract Spin2 and PASM2 idioms from source files
Idioms are small, recurring patterns (1-10 lines)
"""

import os
import re
from collections import defaultdict, Counter
from pathlib import Path

def extract_spin2_idioms(content):
    """Extract Spin2 idioms from file content"""
    idioms = []
    
    # Pin operations
    pin_patterns = [
        (r'pin[hla]\[(\d+)\.\.(\d+)\]', 'pin_range_access'),
        (r'pin[hla]\[([^\]]+)\]\s*:=\s*[01]', 'pin_assignment'),
        (r'pin[hla]\[([^\]]+)\]\s*\^\^', 'pin_toggle'),
        (r'waitms\((\d+)\)', 'timing_delay_ms'),
        (r'waitus\((\d+)\)', 'timing_delay_us'),
        (r'waitct\(([^)]+)\)', 'timing_wait_clock'),
        (r'pinstart\(([^,]+),\s*([^,]+),\s*([^,]+),\s*([^)]+)\)', 'smart_pin_start'),
        (r'pinfloat\(([^)]+)\)', 'pin_float'),
        (r'pinlow\(([^)]+)\)', 'pin_low'),
        (r'pinhigh\(([^)]+)\)', 'pin_high'),
        (r'pintoggle\(([^)]+)\)', 'pin_toggle_func'),
    ]
    
    # Bit manipulation
    bit_patterns = [
        (r'(\w+)\s*&\s*\$[0-9A-F]+', 'bit_mask_hex'),
        (r'(\w+)\s*\|\s*\(1\s*<<\s*(\w+)\)', 'bit_set_shift'),
        (r'(\w+)\s*&\s*~\(1\s*<<\s*(\w+)\)', 'bit_clear_shift'),
        (r'(\w+)\s*>>\s*(\d+)\s*&\s*\$[0-9A-F]+', 'bit_extract'),
        (r'(\w+)\s*ROL\s*(\d+)', 'bit_rotate_left'),
        (r'(\w+)\s*ROR\s*(\d+)', 'bit_rotate_right'),
        (r'(\w+)\s*REV\s*(\d+)', 'bit_reverse'),
    ]
    
    # Loop patterns
    loop_patterns = [
        (r'REPEAT\s+WHILE\s+([^\n]+)', 'repeat_while'),
        (r'REPEAT\s+UNTIL\s+([^\n]+)', 'repeat_until'),
        (r'REPEAT\s+(\w+)\s+FROM\s+(\w+)\s+TO\s+(\w+)', 'repeat_for'),
        (r'REPEAT\s+(\d+)', 'repeat_count'),
        (r'REPEAT\s*\n', 'repeat_forever'),
    ]
    
    # Cog operations
    cog_patterns = [
        (r'COGINIT\(([^,]+),\s*([^,]+),\s*([^)]+)\)', 'cog_init'),
        (r'COGNEW\(([^,]+),\s*([^)]+)\)', 'cog_new'),
        (r'COGSTOP\(([^)]+)\)', 'cog_stop'),
        (r'COGID\(\)', 'cog_id'),
    ]
    
    # Memory operations
    memory_patterns = [
        (r'BYTE\[@([^\]]+)\]\[([^\]]+)\]', 'byte_array_access'),
        (r'WORD\[@([^\]]+)\]\[([^\]]+)\]', 'word_array_access'),
        (r'LONG\[@([^\]]+)\]\[([^\]]+)\]', 'long_array_access'),
        (r'@(\w+)', 'address_of'),
        (r'@@(\w+)', 'absolute_address'),
    ]
    
    for patterns, category in [(pin_patterns, 'pin'), (bit_patterns, 'bit'), 
                                (loop_patterns, 'loop'), (cog_patterns, 'cog'),
                                (memory_patterns, 'memory')]:
        for pattern, name in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                idioms.append({
                    'category': category,
                    'name': name,
                    'pattern': match.group(0),
                    'context': extract_context(content, match.start(), match.end())
                })
    
    return idioms

def extract_pasm2_idioms(content):
    """Extract PASM2 idioms from DAT sections"""
    idioms = []
    
    # Find DAT sections
    dat_sections = re.finditer(r'^DAT\s*\n(.*?)(?=^(?:CON|OBJ|VAR|PUB|PRI|DAT|\Z))', 
                               content, re.MULTILINE | re.DOTALL)
    
    for dat_match in dat_sections:
        dat_content = dat_match.group(1)
        
        # Check for ORG (indicates PASM2 code)
        if 'ORG' not in dat_content.upper():
            continue
            
        # PASM2 patterns
        pasm_patterns = [
            # Loop patterns
            (r'(\w+)\s+DJNZ\s+(\w+),\s*#(\w+)', 'djnz_loop'),
            (r'(\w+)\s+REP\s+#(\d+),\s*#(\d+)', 'rep_loop'),
            (r'(\w+)\s+LOOP', 'loop_instruction'),
            
            # Register operations
            (r'MOV\s+(\w+),\s*(\w+)', 'register_move'),
            (r'ADD\s+(\w+),\s*(\w+)', 'register_add'),
            (r'SUB\s+(\w+),\s*(\w+)', 'register_sub'),
            (r'AND\s+(\w+),\s*(\w+)', 'register_and'),
            (r'OR\s+(\w+),\s*(\w+)', 'register_or'),
            (r'XOR\s+(\w+),\s*(\w+)', 'register_xor'),
            
            # Pin operations
            (r'DRVH\s+#(\d+)', 'pin_drive_high'),
            (r'DRVL\s+#(\d+)', 'pin_drive_low'),
            (r'FLTL\s+#(\d+)', 'pin_float'),
            (r'TESTP\s+#(\d+)\s+WC', 'pin_test'),
            (r'WAITX\s+(\w+)', 'wait_cycles'),
            
            # Hub operations
            (r'RDLONG\s+(\w+),\s*(\w+)', 'hub_read_long'),
            (r'WRLONG\s+(\w+),\s*(\w+)', 'hub_write_long'),
            (r'RDBYTE\s+(\w+),\s*(\w+)', 'hub_read_byte'),
            (r'WRBYTE\s+(\w+),\s*(\w+)', 'hub_write_byte'),
            
            # Conditional execution
            (r'IF_Z\s+(\w+)', 'conditional_z'),
            (r'IF_NZ\s+(\w+)', 'conditional_nz'),
            (r'IF_C\s+(\w+)', 'conditional_c'),
            (r'IF_NC\s+(\w+)', 'conditional_nc'),
        ]
        
        for pattern, name in pasm_patterns:
            matches = re.finditer(pattern, dat_content, re.IGNORECASE)
            for match in matches:
                idioms.append({
                    'type': 'pasm2',
                    'name': name,
                    'pattern': match.group(0).strip(),
                    'context': extract_context(dat_content, match.start(), match.end())
                })
    
    return idioms

def extract_context(content, start, end, context_lines=2):
    """Extract surrounding context for an idiom"""
    lines = content.split('\n')
    current_pos = 0
    
    for i, line in enumerate(lines):
        line_end = current_pos + len(line) + 1
        if current_pos <= start < line_end:
            start_line = max(0, i - context_lines)
            end_line = min(len(lines), i + context_lines + 1)
            return '\n'.join(lines[start_line:end_line])
        current_pos = line_end
    
    return ""

def analyze_files(root_dir):
    """Analyze all .spin2 files in directory"""
    spin2_idioms = defaultdict(list)
    pasm2_idioms = defaultdict(list)
    
    spin2_files = list(Path(root_dir).rglob("*.spin2"))
    print(f"Found {len(spin2_files)} .spin2 files")
    
    for i, file_path in enumerate(spin2_files):
        if i % 50 == 0:
            print(f"Processing file {i}/{len(spin2_files)}")
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Extract Spin2 idioms
            for idiom in extract_spin2_idioms(content):
                key = f"{idiom['category']}_{idiom['name']}"
                spin2_idioms[key].append(idiom['pattern'])
            
            # Extract PASM2 idioms
            for idiom in extract_pasm2_idioms(content):
                key = f"{idiom['name']}"
                pasm2_idioms[key].append(idiom['pattern'])
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    return spin2_idioms, pasm2_idioms

def generate_report(spin2_idioms, pasm2_idioms):
    """Generate idiom analysis report"""
    report = []
    report.append("# P2 Idiom Extraction Report")
    report.append(f"*Analyzed 730 source files*\n")
    
    report.append("## Spin2 Idioms (Top 20 by frequency)\n")
    
    # Count and sort Spin2 idioms
    spin2_counts = {}
    for idiom_type, examples in spin2_idioms.items():
        spin2_counts[idiom_type] = len(examples)
    
    for idiom_type, count in sorted(spin2_counts.items(), key=lambda x: x[1], reverse=True)[:20]:
        report.append(f"### {idiom_type}: {count} occurrences")
        # Show first 3 examples
        examples = spin2_idioms[idiom_type][:3]
        for ex in examples:
            report.append(f"  - `{ex}`")
        report.append("")
    
    report.append("\n## PASM2 Idioms (Top 20 by frequency)\n")
    
    # Count and sort PASM2 idioms
    pasm2_counts = {}
    for idiom_type, examples in pasm2_idioms.items():
        pasm2_counts[idiom_type] = len(examples)
    
    for idiom_type, count in sorted(pasm2_counts.items(), key=lambda x: x[1], reverse=True)[:20]:
        report.append(f"### {idiom_type}: {count} occurrences")
        # Show first 3 examples
        examples = pasm2_idioms[idiom_type][:3]
        for ex in examples:
            report.append(f"  - `{ex}`")
        report.append("")
    
    return "\n".join(report)

if __name__ == "__main__":
    root_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/external-inputs/source-code"
    
    print("Starting idiom extraction...")
    spin2_idioms, pasm2_idioms = analyze_files(root_dir)
    
    report = generate_report(spin2_idioms, pasm2_idioms)
    
    output_file = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/idiom-extraction-report.md"
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"\nReport written to {output_file}")
    print(f"Found {len(spin2_idioms)} unique Spin2 idiom types")
    print(f"Found {len(pasm2_idioms)} unique PASM2 idiom types")