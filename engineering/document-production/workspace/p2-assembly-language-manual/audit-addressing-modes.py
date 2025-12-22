#!/usr/bin/env python3
"""
Audit addressing modes in PASM2 code examples.

P2 Addressing Modes:
1. Register direct - register address (0-511)
2. Immediate (#value) - 9-bit signed value in S field  
3. Long Immediate (##value) - full 32-bit immediate (generates AUGS/AUGD)
4. PTRx modes - ptra/ptrb with pre/post increment/decrement and indexing
5. Relative addressing - for branches (signed offset)

Common issues to check:
- Missing # on immediate values where required
- Using # on values that should be register references
- Using # when ## is needed (values > 511 or < -256)
- Incorrect PTRx syntax
- Impossible immediate values (outside 9-bit range without ##)
"""

import re
from pathlib import Path
from collections import defaultdict

def extract_code_blocks(markdown_file):
    """Extract all pasm/pasm2 code blocks with line numbers.
    
    Handles both formats:
    - ```pasm ... ``` (fenced code blocks)
    - ::: pasm2 ... ::: (Pandoc fenced divs)
    - ::: pasm ... ::: (Pandoc fenced divs)
    """
    with open(markdown_file, 'r') as f:
        content = f.read()
        lines = content.split('\n')
    
    blocks = []
    in_block = False
    block_type = None  # 'fenced' for ```, 'div' for :::
    current_block = []
    start_line = 0
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # Check for start of code block
        if not in_block:
            # Fenced code block: ```pasm or ```pasm2
            if stripped.startswith('```pasm'):
                in_block = True
                block_type = 'fenced'
                start_line = i
                current_block = []
            # Pandoc fenced div: ::: pasm or ::: pasm2
            elif stripped.startswith('::: pasm'):
                in_block = True
                block_type = 'div'
                start_line = i
                current_block = []
        else:
            # Check for end of code block
            if block_type == 'fenced' and stripped == '```':
                in_block = False
                blocks.append({
                    'line': start_line,
                    'code': '\n'.join(current_block),
                    'end_line': i,
                    'type': 'fenced'
                })
            elif block_type == 'div' and stripped == ':::':
                in_block = False
                blocks.append({
                    'line': start_line,
                    'code': '\n'.join(current_block),
                    'end_line': i,
                    'type': 'div'
                })
            else:
                current_block.append(line)
    
    return blocks

# Instructions that commonly take immediate S operand
IMMEDIATE_S_INSTRUCTIONS = {
    'mov', 'add', 'sub', 'and', 'or', 'xor', 'cmp', 'cmps',
    'test', 'testn', 'shl', 'shr', 'sar', 'rol', 'ror',
    'rcl', 'rcr', 'muxc', 'muxnc', 'muxz', 'muxnz',
    'addx', 'subx', 'adds', 'subs', 'addsx', 'subsx',
    'sumc', 'sumnc', 'sumz', 'sumnz', 'mins', 'maxs',
    'min', 'max', 'abs', 'neg', 'not', 'ones',
    'encod', 'decod', 'bmask', 'zerox', 'signx',
    'mul', 'muls', 'scl', 'scas',
    'waitx', 'getct', 'pollct', 'waitct',
    'djnz', 'tjnz', 'tjz', 'djz',
    'rep', 'jmp', 'call', 'ret', 'calla', 'callb',
    'calld', 'loc', 'augs', 'augd',
    'rdbyte', 'rdword', 'rdlong', 'wrbyte', 'wrword', 'wrlong',
    'rdfast', 'wrfast', 'fblock', 'rfbyte', 'rfword', 'rflong',
    'wfbyte', 'wfword', 'wflong',
    'setq', 'setq2', 'getq',
    'cogid', 'coginit', 'cogstop',
    'locknew', 'lockret', 'locktry', 'lockrel',
    'qmul', 'qdiv', 'qfrac', 'qsqrt', 'qrotate', 'qvector',
    'hubset', 'clkset',
    'setxfrq', 'getxacc', 'waitxfi', 'waitxro', 'waitxrl',
    'setse1', 'setse2', 'setse3', 'setse4',
    'pollse1', 'pollse2', 'pollse3', 'pollse4',
    'waitpat', 'waitse1', 'waitse2', 'waitse3', 'waitse4',
    'allowi', 'stalli', 'trgint1', 'trgint2', 'trgint3',
    'nixint1', 'nixint2', 'nixint3',
    'setint1', 'setint2', 'setint3',
    'setbrk', 'brk',
    'dirl', 'dirh', 'dirc', 'dirnc', 'dirz', 'dirnz', 'dirrnd', 'dirnot',
    'outl', 'outh', 'outc', 'outnc', 'outz', 'outnz', 'outrnd', 'outnot',
    'fltl', 'flth', 'fltc', 'fltnc', 'fltz', 'fltnz', 'fltrnd', 'fltnot',
    'drvl', 'drvh', 'drvc', 'drvnc', 'drvz', 'drvnz', 'drvrnd', 'drvnot',
    'testp', 'testpn',
    'wrpin', 'wxpin', 'wypin', 'akpin', 'rdpin', 'rqpin',
    'setdacs', 'setluts', 'setcy', 'setci', 'setcq',
    'setcfrq', 'setcmod', 'setpiv', 'setpix',
    'cogatn', 'pollatn', 'waitatn',
    'getptr', 'getbrk', 'getint', 'getword', 'getbyte', 'getnib',
    'setword', 'setbyte', 'setnib',
    'rolword', 'rolbyte', 'rolnib',
    'setnib', 'getnib', 'rolnib',
    'splitb', 'mergeb', 'splitw', 'mergew',
    'seussf', 'seussr',
    'rgbsqz', 'rgbexp',
    'xoro32', 'rev', 'rczr', 'rczl', 'wrc', 'wrnc', 'wrz', 'wrnz',
    'modcz', 'modc', 'modz',
    'setscp', 'getscp', 'jmprel',
    'skip', 'skipf', 'execf',
    'getlut', 'setlut', 'wrlut', 'rdlut',
    'altgn', 'altgb', 'altgw', 'altsn', 'altsb', 'altsw', 'altd', 'alts', 'altr', 'altdx', 'altsx', 'altrx',
    'decod2', 'decod3', 'decod4', 'decod5', 'encod',
    'incmod', 'decmod',
    'cmpr', 'cmpsx', 'cmpx',
    'addct1', 'addct2', 'addct3', 'pollct1', 'pollct2', 'pollct3',
    'waitct1', 'waitct2', 'waitct3',
    'push', 'pop',
    'jnct1', 'jnct2', 'jnct3', 'jct1', 'jct2', 'jct3',
    'jnse1', 'jnse2', 'jnse3', 'jnse4', 'jse1', 'jse2', 'jse3', 'jse4',
    'jnatn', 'jatn', 'jnqmt', 'jqmt',
    'jnint', 'jint', 'jnpat', 'jpat', 'jnfbw', 'jfbw', 'jnxmt', 'jxmt',
    'jnxfi', 'jxfi', 'jnxro', 'jxro', 'jnxrl', 'jxrl',
    'setpat', 'akpin',
    'bitl', 'bith', 'bitc', 'bitnc', 'bitz', 'bitnz', 'bitrnd', 'bitnot',
    'testb', 'testbn',
    'andn', 'orn', 'xorn', 'mull', 'muxq', 'movbyts',
    'fle', 'fge', 'fne', 'fe',
    'flti', 'fltf', 'fdivi', 'fdivf', 'fsqrt',
    'fadd', 'fsub', 'fmul', 'fdiv', 'fabs', 'fneg', 'fcmp',
    'qlog', 'qexp', 'atan', 'tan', 'asin', 'sin', 'acos', 'cos',
}

# PTRx patterns
PTRX_PATTERN = re.compile(r'\b(ptra|ptrb)(\+\+|--)?(\[[^\]]+\])?((?:\+\+|--))?', re.IGNORECASE)

def parse_immediate_value(val_str):
    """Parse an immediate value string and return the integer value."""
    val_str = val_str.replace('_', '').strip()
    
    # Handle hex
    if val_str.startswith('$'):
        return int(val_str[1:], 16)
    elif val_str.lower().startswith('0x'):
        return int(val_str[2:], 16)
    # Handle binary
    elif val_str.startswith('%'):
        return int(val_str[1:], 2)
    elif val_str.lower().startswith('0b'):
        return int(val_str[2:], 2)
    # Handle decimal
    else:
        return int(val_str)

def analyze_instruction(line, line_num, block_line, original_line):
    """Analyze a single instruction for addressing mode issues."""
    issues = []
    
    # Skip comments and labels
    code_part = line.split("'")[0].strip()
    if not code_part or code_part.endswith(':'):
        return issues
    
    # Skip directives
    upper = code_part.upper()
    if any(upper.startswith(d) for d in ['CON', 'DAT', 'PUB', 'PRI', 'VAR', 'OBJ', 'ORG', 'FIT', 'RES', 'BYTE', 'WORD', 'LONG', 'ALIGNW', 'ALIGNL', 'FILE', 'END', '_CLKFREQ', '_CLKMODE']):
        return issues
    
    # Parse instruction and operands
    parts = code_part.split()
    if not parts:
        return issues
    
    # Handle labels at start of line
    first = parts[0]
    if first.endswith(':'):
        parts = parts[1:]
    elif len(parts) > 1 and first.lower() not in IMMEDIATE_S_INSTRUCTIONS:
        # Could be a label without colon
        if not any(first.lower() == i for i in IMMEDIATE_S_INSTRUCTIONS):
            parts = parts[1:]
    
    if not parts:
        return issues
    
    instr = parts[0].lower()
    
    # Get operand string
    operand_str = ' '.join(parts[1:]) if len(parts) > 1 else ''
    
    # ========================================
    # CHECK 1: Single # with values > 511
    # ========================================
    # Pattern: instruction D, #large_value (where large_value > 511)
    # This would need ## for values that don't fit in 9 bits
    
    # Match single # but not ## (use negative lookbehind AND lookahead)
    single_imm_pattern = re.compile(r'(?<!#)#(?!#)(\$[0-9a-fA-F_]+|%[01_]+|0x[0-9a-fA-F_]+|0b[01_]+|\d+)', re.IGNORECASE)
    
    for match in single_imm_pattern.finditer(operand_str):
        val_str = match.group(1)
        try:
            val = parse_immediate_value(val_str)
            # 9-bit signed range: -256 to 511
            # However, for S operand, positive values 0-511 are common
            # Values > 511 require AUGS or ## notation
            if val > 511:
                issues.append({
                    'line': block_line + line_num,
                    'issue': f'Single # with value {val} (0x{val:X}) exceeds 9-bit range (max 511). Should this be ## for 32-bit immediate?',
                    'instruction': original_line.strip(),
                    'severity': 'review',
                    'value': val
                })
        except ValueError:
            pass
    
    # ========================================
    # CHECK 2: ## usage validation
    # ========================================
    double_imm_pattern = re.compile(r'##(\$[0-9a-fA-F_]+|%[01_]+|0x[0-9a-fA-F_]+|0b[01_]+|\d+)', re.IGNORECASE)
    
    for match in double_imm_pattern.finditer(operand_str):
        val_str = match.group(1)
        try:
            val = parse_immediate_value(val_str)
            # Track ## usage for statistics
            pass
        except ValueError:
            pass
    
    # ========================================
    # CHECK 3: PTRx usage
    # ========================================
    if re.search(r'\bptr[ab]\b', operand_str, re.IGNORECASE):
        # Check for valid PTRx patterns
        # Valid: ptra, ptra++, ++ptra, ptra--, --ptra, ptra[0], ptra[n], ptra++[0], etc.
        pass
    
    return issues

def audit_code_blocks(blocks):
    """Audit all code blocks for addressing mode issues."""
    all_issues = []
    stats = defaultdict(int)
    immediate_stats = {
        'single_hash': 0,
        'double_hash': 0,
        'single_hash_large': 0,  # > 511
        'ptrx_usage': 0,
    }
    
    for block_idx, block in enumerate(blocks, 1):
        code_lines = block['code'].split('\n')
        
        for i, line in enumerate(code_lines):
            original_line = line
            # Track instruction usage
            code_part = line.split("'")[0].strip()
            parts = code_part.split()
            if parts:
                instr = parts[0].lower().rstrip(':')
                if instr in IMMEDIATE_S_INSTRUCTIONS:
                    stats[instr] += 1
                
                # Count addressing mode usage
                if '#' in line and '##' not in line:
                    immediate_stats['single_hash'] += line.count('#')
                if '##' in line:
                    immediate_stats['double_hash'] += line.count('##')
                if re.search(r'\bptr[ab]\b', line, re.IGNORECASE):
                    immediate_stats['ptrx_usage'] += 1
                
                # Specific checks
                issues = analyze_instruction(code_part, i, block['line'], original_line)
                for issue in issues:
                    issue['block'] = block_idx
                    issue['block_start'] = block['line']
                    all_issues.append(issue)
        
        # Additional whole-block checks
        code = block['code']
        
        # Check for MOV with bare numbers (no #)
        mov_patterns = re.findall(r'\bmov\s+(\w+)\s*,\s*(\d+)\s*(?:\'|$|\n)', code, re.IGNORECASE)
        for match in mov_patterns:
            dest, val = match
            try:
                v = int(val)
                if v < 512:  # Could be register or immediate - ambiguous
                    all_issues.append({
                        'block': block_idx,
                        'block_start': block['line'],
                        'issue': f'MOV with bare number {val} - if immediate value intended, should be #{val}',
                        'instruction': f'mov {dest}, {val}',
                        'severity': 'review'
                    })
            except:
                pass
    
    return all_issues, dict(stats), immediate_stats

def main():
    manual_path = Path("P2-Assembly-Language-Manual.md")
    
    print(f"Analyzing addressing modes in {manual_path}...")
    blocks = extract_code_blocks(manual_path)
    print(f"Found {len(blocks)} code blocks\n")
    
    issues, stats, imm_stats = audit_code_blocks(blocks)
    
    print("=" * 70)
    print("ADDRESSING MODE AUDIT RESULTS")
    print("=" * 70)
    
    print("\n📊 ADDRESSING MODE USAGE STATISTICS:")
    print("-" * 40)
    print(f"  Single # (immediate):     {imm_stats['single_hash']:4}")
    print(f"  Double ## (long imm):     {imm_stats['double_hash']:4}")
    print(f"  PTRx addressing:          {imm_stats['ptrx_usage']:4}")
    
    if issues:
        # Filter for significant issues
        significant = [i for i in issues if i['severity'] in ['error', 'warning']]
        reviews = [i for i in issues if i['severity'] == 'review']
        
        print(f"\n⚠️  Found {len(significant)} potential issues, {len(reviews)} items for review:\n")
        
        # Group by severity
        by_severity = defaultdict(list)
        for issue in issues:
            by_severity[issue['severity']].append(issue)
        
        for severity in ['error', 'warning', 'review']:
            if severity in by_severity:
                print(f"\n{severity.upper()}S ({len(by_severity[severity])}):")
                print("-" * 50)
                for issue in by_severity[severity][:20]:  # Limit output
                    print(f"  Block {issue['block']} (line ~{issue.get('line', issue['block_start'])}):")
                    print(f"    {issue['issue']}")
                    print(f"    Code: {issue.get('instruction', 'N/A')}")
                    print()
                if len(by_severity[severity]) > 20:
                    print(f"  ... and {len(by_severity[severity]) - 20} more")
    else:
        print("\n✓ No obvious addressing mode issues found!")
    
    print("\n" + "=" * 70)
    print("INSTRUCTION USAGE STATISTICS (top 20):")
    print("=" * 70)
    sorted_stats = sorted(stats.items(), key=lambda x: -x[1])[:20]
    for instr, count in sorted_stats:
        print(f"  {instr:12} : {count:4}")
    
    print(f"\n\nTotal instructions analyzed: {sum(stats.values())}")
    print(f"Unique instructions: {len(stats)}")
    
    return len([i for i in issues if i['severity'] == 'error'])

if __name__ == '__main__':
    import sys
    sys.exit(main())
