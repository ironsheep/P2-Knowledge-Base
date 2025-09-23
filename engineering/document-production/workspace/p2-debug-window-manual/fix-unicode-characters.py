#!/usr/bin/env python3
"""
Fix Unicode characters in Debug Window Manual for LaTeX compatibility.
"""

import sys
import re

def fix_unicode_characters(content):
    """Replace problematic Unicode characters with ASCII equivalents."""
    
    # Count changes for reporting
    changes = {}
    
    # 1. Multiplication sign (×) -> x
    count = content.count('×')
    if count > 0:
        content = content.replace('×', 'x')
        changes['× → x'] = count
    
    # 2. Em dash (—) -> -- (double hyphen for LaTeX)
    count = content.count('—')
    if count > 0:
        content = content.replace('—', '--')
        changes['— → --'] = count
    
    # 3. Less than or equal (≤) -> <=
    count = content.count('≤')
    if count > 0:
        content = content.replace('≤', '<=')
        changes['≤ → <='] = count
    
    # 4. Greater than or equal (≥) -> >=
    count = content.count('≥')
    if count > 0:
        content = content.replace('≥', '>=')
        changes['≥ → >='] = count
    
    # 5. Arrow (→) -> ->
    count = content.count('→')
    if count > 0:
        content = content.replace('→', '->')
        changes['→ → ->'] = count
    
    # 6. Checkmarks in lists (at start of line after ✓ )
    pattern = r'^(\s*)✓\s+\*\*'
    matches = re.findall(pattern, content, re.MULTILINE)
    if matches:
        content = re.sub(pattern, r'\1**', content, flags=re.MULTILINE)
        changes['✓ removed from list items'] = len(matches)
    
    # 7. X marks in lists
    pattern = r'^(\s*)✗\s+\*\*'
    matches = re.findall(pattern, content, re.MULTILINE)
    if matches:
        content = re.sub(pattern, r'\1**', content, flags=re.MULTILINE)
        changes['✗ removed from list items'] = len(matches)
    
    # 8. Emoji checkmarks/X in code comments
    content = content.replace('✅', '[OK]')
    content = content.replace('❌', '[NO]')
    if '✅' in content or '❌' in content:
        changes['✅/❌ → [OK]/[NO]'] = True
    
    # 9. Degree symbol in inline code (backticks)
    # Pattern to find degree in inline code
    pattern = r'`([^`]*°[^`]*)`'
    matches = re.findall(pattern, content)
    for match in matches:
        fixed = match.replace('°', 'deg')
        content = content.replace(f'`{match}`', f'`{fixed}`')
    if matches:
        changes['° → deg in inline code'] = len(matches)
    
    # 10. Theta in inline code (if any - we already handled this but double-check)
    pattern = r'`([^`]*θ[^`]*)`'
    matches = re.findall(pattern, content)
    for match in matches:
        fixed = match.replace('θ', 'theta')
        content = content.replace(f'`{match}`', f'`{fixed}`')
    if matches:
        changes['θ → theta in inline code'] = len(matches)
    
    return content, changes

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 fix-unicode-characters.py input.md output.md")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Read input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix Unicode characters
    fixed_content, changes = fix_unicode_characters(content)
    
    # Write output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    # Report changes
    print(f"Unicode character fixes applied to {output_file}:")
    if changes:
        for change, count in changes.items():
            if isinstance(count, bool):
                print(f"  - {change}")
            else:
                print(f"  - {change}: {count} occurrences")
    else:
        print("  No Unicode characters needed fixing")

if __name__ == "__main__":
    main()