#!/usr/bin/env python3
"""
Convert PASM2 instructions to UPPERCASE + BOLD in markdown code blocks
"""

import re
import sys

# Common PASM2 instructions to convert to UPPERCASE + BOLD
INSTRUCTIONS = {
    'org', 'drvh', 'drvl', 'waitx', 'jmp', 'mov', 'add', 'sub', 'and', 'or', 'xor',
    'shl', 'shr', 'sar', 'rol', 'ror', 'cmp', 'test', 'rdlong', 'wrlong', 'rdbyte',
    'wrbyte', 'rdword', 'wrword', 'coginit', 'cogstop', 'hubset', 'wxpin', 'wypin',
    'mul', 'div', 'abs', 'neg', 'not', 'incmod', 'decmod', 'testp', 'testpn',
    'djnz', 'tjnz', 'tjz', 'call', 'ret', 'push', 'pop', 'getct', 'waitct',
    'locknew', 'lockret', 'locktry', 'lockrel', 'lockset', 'lockclr', 'setq',
    'setq2', 'getqx', 'getqy', 'cordic', 'qrotate', 'qvector', 'qdiv', 'qsqrt',
    'qlog', 'qexp', 'wrpin', 'rdpin', 'rqpin', 'akpin', 'wrfast', 'rdfast',
    'wflong', 'wfword', 'wfbyte', 'rflong', 'rfword', 'rfbyte', 'getbyte',
    'setbyte', 'getword', 'setword', 'alti', 'altd', 'altr', 'alts', 'altb',
    'setcz', 'modcz', 'modc', 'modz', 'wc', 'wz', 'wcz', 'if_z', 'if_nz',
    'if_c', 'if_nc', 'if_c_and_z', 'if_c_and_nz', 'if_nc_and_z', 'if_nc_and_nz',
    'nop', 'augd', 'augs', 'bitc', 'bitnc', 'bitz', 'bitnz', 'bitrnd', 'bitnot',
    'loc', 'pollct', 'pollse', 'pollpat', 'pollfbw', 'pollxmt', 'pollxfi',
    'pollxro', 'pollxrl', 'waitct', 'waitse', 'waitpat', 'waitfbw', 'waitxmt',
    'waitxfi', 'waitxro', 'waitxrl', 'allowi', 'stalli', 'trgint', 'nixint',
    'setint', 'setse', 'pollint', 'waitint', 'encod', 'ones', 'bmask', 'cogatn',
    'pollatn', 'waitatn', 'wrlut', 'rdlut', 'addct', 'mulpix', 'blnpix', 'mixpix',
    'fitaccs', 'movbyts', 'splitb', 'mergeb', 'splitw', 'mergew', 'seussf',
    'seussr', 'rgbsqz', 'rgbexp', 'xoro32', 'rczr', 'rczl', 'rep', 'skip',
    'skipf', 'execf', 'getptr', 'getint', 'setbrk', 'cogbrk', 'brk', 'setluts',
    'setcy', 'setci', 'setcq', 'setcfrq', 'setcmod', 'setpiv', 'setpix', 'testn',
    'cmpx', 'cmpsub', 'subr', 'subx', 'addx', 'addsx', 'subsx', 'cmpsx', 'cmpr',
    'cmpm', 'mins', 'maxs', 'min', 'max', 'fge', 'fle', 'fges', 'fles', 'sumc',
    'sumnc', 'sumz', 'sumnz', 'muls', 'scl', 'sca', 'addpix', 'mulpix', 'blnpix',
    'mixpix', 'mul', 'muls', 'sca', 'scas', 'addpix', 'mulpix', 'blnpix', 'mixpix',
    'ptrs', 'ptra', 'ptrb', 'dirl', 'dirh', 'dirc', 'dirnc', 'dirz', 'dirnz',
    'dirrnd', 'dirnot', 'outl', 'outh', 'outc', 'outnc', 'outz', 'outnz',
    'outrnd', 'outnot', 'fltl', 'flth', 'fltc', 'fltnc', 'fltz', 'fltnz',
    'fltrnd', 'fltnot', 'wrz', 'wrnz', 'wrc', 'wrnc', 'modz', 'modc', 'modn',
    'zerox', 'signx', 'topone', 'botone', 'incmod', 'decmod', 'mul', 'muls',
    'getmull', 'getmulh', 'div', 'divs', 'div64d', 'divs64d', 'sqrt32', 'sqrt64',
    'qmul', 'qdiv', 'qfrac', 'qrotate', 'qvector'
}

def process_line(line, in_code_block):
    """Process a single line, converting instructions to UPPERCASE + BOLD if in code block."""
    if not in_code_block:
        return line
    
    # Skip comment-only lines and empty lines
    if line.strip().startswith("'") or not line.strip():
        return line
    
    # Split line into code and comment parts
    parts = line.split("'", 1)
    code_part = parts[0]
    comment_part = "'" + parts[1] if len(parts) > 1 else ""
    
    # Process the code part
    # Look for instruction at the beginning of the line or after a label
    words = code_part.split()
    if words:
        for i, word in enumerate(words):
            # Check if this word is an instruction (case-insensitive)
            word_lower = word.lower()
            if word_lower in INSTRUCTIONS:
                # Replace with UPPERCASE + BOLD
                words[i] = f"**{word.upper()}**"
                break  # Only the first instruction-like word
            # If first word has a label (ends with colon or is just text), check next word
            if i == 0 and not word_lower in INSTRUCTIONS:
                continue
    
    # Reconstruct the line
    processed_code = " ".join(words) if words else code_part
    return processed_code + comment_part

def process_file(input_file, output_file):
    """Process a markdown file, converting PASM2 instructions in code blocks."""
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    output_lines = []
    in_code_block = False
    
    for line in lines:
        # Check for code block markers
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            output_lines.append(line)
        else:
            output_lines.append(process_line(line, in_code_block))
    
    with open(output_file, 'w') as f:
        f.writelines(output_lines)
    
    print(f"Processed {input_file} -> {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python uppercase-instructions.py input.md output.md")
        sys.exit(1)
    
    process_file(sys.argv[1], sys.argv[2])