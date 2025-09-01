#!/usr/bin/env python3
"""
Comprehensive LaTeX brace checker that tracks nesting and finds mismatches.
"""

import sys
import re

def check_braces(filename):
    """Check for brace mismatches in a LaTeX file."""
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    print(f"Checking {filename}...")
    print("=" * 60)
    
    # Track overall balance
    total_open = 0
    total_close = 0
    
    # Track nesting level
    nesting_stack = []  # Stack of (char, line_num, col_num)
    
    # Track problems
    problems = []
    
    for line_num, line in enumerate(lines, 1):
        for col_num, char in enumerate(line, 1):
            if char == '{':
                total_open += 1
                nesting_stack.append(('{', line_num, col_num))
            elif char == '}':
                total_close += 1
                if not nesting_stack:
                    problems.append(f"Line {line_num}, Col {col_num}: Closing brace with no opening brace")
                else:
                    nesting_stack.pop()
    
    # Report overall statistics
    print(f"Total braces: {total_open} open, {total_close} close")
    print(f"Difference: {total_open - total_close}")
    print()
    
    # Report unclosed braces
    if nesting_stack:
        print(f"UNCLOSED BRACES: {len(nesting_stack)} braces never closed")
        for char, line_num, col_num in nesting_stack[:10]:  # Show first 10
            line = lines[line_num - 1].rstrip()
            print(f"  Line {line_num}, Col {col_num}: {line[:80]}...")
        if len(nesting_stack) > 10:
            print(f"  ... and {len(nesting_stack) - 10} more")
        print()
    
    # Report problems
    if problems:
        print(f"PROBLEMS FOUND: {len(problems)}")
        for problem in problems[:10]:
            print(f"  {problem}")
        if len(problems) > 10:
            print(f"  ... and {len(problems) - 10} more")
        print()
    
    # Check specific command definitions
    print("CHECKING COMMAND DEFINITIONS:")
    for line_num, line in enumerate(lines, 1):
        if '\\newcommand' in line or '\\renewcommand' in line:
            # Check if it's a complete single-line definition
            if not line.rstrip().endswith('{%') and not line.rstrip().endswith('{'):
                open_count = line.count('{')
                close_count = line.count('}')
                if open_count != close_count:
                    print(f"  Line {line_num}: Unbalanced ({open_count} open, {close_count} close)")
                    print(f"    {line.strip()[:100]}")
    print()
    
    # Check specific environment definitions
    print("CHECKING ENVIRONMENT DEFINITIONS:")
    in_env_def = False
    env_start_line = 0
    env_lines = []
    env_open_count = 0
    
    for line_num, line in enumerate(lines, 1):
        if '\\newenvironment' in line or '\\renewenvironment' in line:
            in_env_def = True
            env_start_line = line_num
            env_lines = [line]
            env_open_count = line.count('{') - line.count('}')
        elif in_env_def:
            env_lines.append(line)
            env_open_count += line.count('{') - line.count('}')
            # Environment definitions usually end when braces balance
            if env_open_count == 0:
                # Full environment collected, check it
                full_env = ''.join(env_lines)
                # Environment should have format: \newenvironment{name}{begin}{end}
                # So we expect certain number of top-level groups
                if full_env.count('{') != full_env.count('}'):
                    print(f"  Lines {env_start_line}-{line_num}: Unbalanced environment definition")
                    print(f"    First line: {env_lines[0].strip()[:80]}")
                in_env_def = False
    
    # Final verdict
    print("=" * 60)
    if total_open == total_close and not problems and not nesting_stack:
        print("✅ FILE IS BALANCED")
    else:
        print("❌ FILE HAS BRACE ISSUES")
        if total_open != total_close:
            print(f"   Need {abs(total_open - total_close)} more {'closing' if total_open > total_close else 'opening'} braces")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_braces(sys.argv[1])
    else:
        # Default to checking the .tex file
        check_braces("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/exports/pdf-generation/outbound/P2-PASM-deSilva-Style/P2-PASM-deSilva-Style-Part1.tex")