#!/usr/bin/env python3
"""
fix-pinr-calls.py - Replace invalid pinr() calls with correct Spin2 methods.

pinr() does not exist in Spin2. The correct replacements are:
- For IN flag checking: testp(pin)
- For Z register reading: rdpin(pin) or rqpin(pin)
- For actual pin state: pinread(pin)

IMPORTANT: Mode configuration cannot be read back from pins.
"""

import re
import sys

def fix_pinr_calls(content):
    """Replace all pinr() calls with appropriate Spin2 methods."""

    lines = content.split('\n')
    changes = []

    for i, line in enumerate(lines):
        original = line
        line_num = i + 1

        if 'pinr(' not in line:
            continue

        # Pattern 1: pinr(PIN) & $8000_0000 or $80000000 (checking IN flag bit 31)
        # These should become testp(PIN)
        # Note: $8000_0000 has underscore separator, $80000000 does not

        # Regex pattern for hex IN flag mask (bit 31): $8000_0000 or $80000000
        hex_mask = r'\$8000_?0000'

        # Handle: repeat until pinr(X) & $8000_0000 == 0
        # This checks if IN flag is NOT set, so use: repeat while testp(X)
        match = re.search(r'repeat until pinr\(([^)]+)\)\s*&\s*' + hex_mask + r'\s*==\s*0', line)
        if match:
            pin = match.group(1)
            line = re.sub(
                r'repeat until pinr\(' + re.escape(pin) + r'\)\s*&\s*' + hex_mask + r'\s*==\s*0',
                f'repeat while testp({pin})',
                line
            )

        # Handle: repeat until pinr(X) & $8000_0000 or $80000000
        match = re.search(r'repeat until pinr\(([^)]+)\)\s*&\s*' + hex_mask, line)
        if match and 'repeat while' not in line:  # Don't double-process
            pin = match.group(1)
            line = re.sub(
                r'repeat until pinr\(' + re.escape(pin) + r'\)\s*&\s*' + hex_mask,
                f'repeat until testp({pin})',
                line
            )

        # Handle: if pinr(X) & $8000_0000 or $80000000
        match = re.search(r'if pinr\(([^)]+)\)\s*&\s*' + hex_mask, line)
        if match:
            pin = match.group(1)
            line = re.sub(
                r'if pinr\(' + re.escape(pin) + r'\)\s*&\s*' + hex_mask,
                f'if testp({pin})',
                line
            )

        # Handle: (pinr(X) & $8000_0000) <> 0 or != 0
        match = re.search(r'\(pinr\(([^)]+)\)\s*&\s*' + hex_mask + r'\)\s*(<>|!=)\s*0', line)
        if match:
            pin = match.group(1)
            line = re.sub(
                r'\(pinr\(' + re.escape(pin) + r'\)\s*&\s*' + hex_mask + r'\)\s*(<>|!=)\s*0',
                f'testp({pin})',
                line
            )

        # Pattern 2: Simple pinr(PIN) without mask - checking IN flag
        # repeat until pinr(X) -> repeat until testp(X)
        match = re.search(r'repeat until pinr\(([^)]+)\)(?!\s*&)', line)
        if match:
            pin = match.group(1)
            line = re.sub(
                r'repeat until pinr\(' + re.escape(pin) + r'\)(?!\s*&)',
                f'repeat until testp({pin})',
                line
            )

        # if pinr(X) -> if testp(X) (simple check without mask)
        # But need to be careful not to match already-processed lines
        match = re.search(r'if pinr\(([^)]+)\)(?!\s*&)', line)
        if match:
            pin = match.group(1)
            line = re.sub(
                r'if pinr\(' + re.escape(pin) + r'\)(?!\s*&)',
                f'if testp({pin})',
                line
            )

        # Pattern 3: pinr(X) & $3F - trying to read mode config
        # This doesn't work - mode config can't be read back
        # Replace with comment noting this is illustrative
        match = re.search(r'(\w+)\s*:=\s*pinr\(([^)]+)\)\s*&\s*\$3F', line)
        if match:
            var = match.group(1)
            pin = match.group(2)
            # Replace with a note that this is illustrative (can't actually read mode)
            line = re.sub(
                r'(\w+)\s*:=\s*pinr\(' + re.escape(pin) + r'\)\s*&\s*\$3F',
                f"{var} := 0  ' NOTE: Mode config cannot be read back from pin",
                line
            )

        # Pattern 4: config := pinr(pin) - trying to read full config
        match = re.search(r'(\w+)\s*:=\s*pinr\(([^)]+)\)(?!\s*&)', line)
        if match:
            var = match.group(1)
            pin = match.group(2)
            line = re.sub(
                r'(\w+)\s*:=\s*pinr\(' + re.escape(pin) + r'\)(?!\s*&)',
                f"{var} := 0  ' NOTE: Pin config cannot be read back; track in software",
                line
            )

        # Pattern 5: pinr(X) & 1 - checking bit 0 (pin input state)
        # This should be pinread(X)
        match = re.search(r'pinr\(([^)]+)\)\s*&\s*1(?!\d)', line)
        if match:
            pin = match.group(1)
            line = re.sub(
                r'pinr\(' + re.escape(pin) + r'\)\s*&\s*1(?!\d)',
                f'pinread({pin})',
                line
            )

        if line != original:
            changes.append((line_num, original.strip(), line.strip()))
            lines[i] = line

    return '\n'.join(lines), changes

def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'P2-Smart-Pins-Green-Book-Tutorial.md'

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    fixed_content, changes = fix_pinr_calls(content)

    # Report changes
    print(f"=== pinr() Replacement Report ===")
    print(f"Total changes: {len(changes)}")
    print()

    for line_num, old, new in changes:
        print(f"Line {line_num}:")
        print(f"  OLD: {old}")
        print(f"  NEW: {new}")
        print()

    # Write output
    output_file = input_file.replace('.md', '-fixed.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    print(f"Fixed content written to: {output_file}")
    print(f"Run: diff {input_file} {output_file} | head -200")

if __name__ == '__main__':
    main()
