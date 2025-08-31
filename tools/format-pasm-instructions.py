#!/usr/bin/env python3
"""
Format PASM2 instructions as UPPERCASE + BOLD in markdown files.
Handles both code blocks and inline references.
"""

import re
import sys

# Comprehensive list of PASM2 instructions
PASM_INSTRUCTIONS = {
    # Basic arithmetic and logic
    'mov', 'add', 'adds', 'sub', 'subs', 'mul', 'muls', 'div', 'divs',
    'and', 'or', 'xor', 'not', 'neg', 'abs', 'shl', 'shr', 'sar', 'rol', 'ror',
    'rev', 'signx', 'zerox', 'encod', 'decod', 'ones', 'bmask',
    
    # Comparison and test
    'cmp', 'cmps', 'cmpr', 'cmpm', 'cmpx', 'cmpsx', 'cmpsub', 'test', 'testn',
    'testb', 'testbn', 'min', 'max', 'mins', 'maxs', 'fge', 'fle', 'fges', 'fles',
    
    # Memory operations
    'rdlong', 'wrlong', 'rdword', 'wrword', 'rdbyte', 'wrbyte',
    'rdlut', 'wrlut', 'rdfast', 'wrfast', 'rflong', 'rfword', 'rfbyte',
    'wflong', 'wfword', 'wfbyte',
    
    # Pin operations
    'drvl', 'drvh', 'drvnot', 'drvrnd', 'drvz', 'drvnz', 'drvc', 'drvnc',
    'outl', 'outh', 'outnot', 'outrnd', 'outz', 'outnz', 'outc', 'outnc',
    'fltl', 'flth', 'fltnot', 'fltrnd', 'fltz', 'fltnz', 'fltc', 'fltnc',
    'dirl', 'dirh', 'dirnot', 'dirrnd', 'dirz', 'dirnz', 'dirc', 'dirnc',
    'testp', 'testpn', 'wrpin', 'wxpin', 'wypin', 'wrlut', 'rdpin', 'rqpin', 'akpin',
    
    # Flow control
    'jmp', 'call', 'ret', 'reta', 'retb', 'jmprel', 'skip', 'skipf', 'execf',
    'djnz', 'djz', 'djnf', 'djf', 'ijnz', 'ijz', 'tjnz', 'tjz', 'tjf', 'tjnf',
    'jp', 'jnp', 'callpa', 'callpb',
    
    # COG control
    'coginit', 'cogstop', 'cogid', 'locknew', 'lockret', 'locktry', 'lockrel',
    'cogatn', 'pollatn', 'waitatn', 'hubset', 'cogspin',
    
    # Timing
    'waitx', 'waitct', 'getct', 'addct', 'pollct', 'waitint', 'waitpat',
    'waitse', 'waitfbw', 'waitxmt', 'waitxfi', 'waitxro', 'waitxrl',
    
    # CORDIC
    'qrotate', 'qvector', 'qdiv', 'qfrac', 'qmul', 'qsqrt', 'qlog', 'qexp',
    'getqx', 'getqy', 'cordic',
    
    # Special operations
    'setq', 'setq2', 'push', 'pop', 'altd', 'alts', 'altb', 'altr', 'alti',
    'setr', 'setd', 'sets', 'seti', 'movbyts', 'splitb', 'mergeb', 'splitw', 'mergew',
    'sca', 'scas', 'addpix', 'mulpix', 'blnpix', 'mixpix',
    
    # Conditional execution prefixes
    'if_z', 'if_nz', 'if_c', 'if_nc', 'if_c_and_z', 'if_c_and_nz',
    'if_nc_and_z', 'if_nc_and_nz', 'if_c_or_z', 'if_c_or_nz',
    'if_nc_or_z', 'if_nc_or_nz', 'if_c_eq_z', 'if_c_ne_z',
    
    # Modifiers and flags
    'wz', 'wc', 'wcz', 'andc', 'andz', 'orc', 'orz', 'xorc', 'xorz',
    'modc', 'modz', 'modcz',
    
    # Stack and misc
    'nop', 'org', 'fit', 'res', 'augd', 'augs', 'loc', 'rep',
    'getbyte', 'setbyte', 'getword', 'setword', 'rolbyte', 'rolword',
    'getnib', 'setnib', 'rolnib',
    
    # More Pin/Smart Pin operations
    'pinhigh', 'pinlow', 'pintoggle', 'pinfloat', 'pinread', 'pinwrite',
    'pinclear', 'pinset', 'pinstart', 'pinstop',
    
    # Additional
    'bitc', 'bitnc', 'bitz', 'bitnz', 'bitrnd', 'bitnot',
    'incmod', 'decmod', 'topone', 'botone',
    'lockset', 'lockclr', 'muxc', 'muxnc', 'muxz', 'muxnz',
    'sumc', 'sumnc', 'sumz', 'sumnz', 'subr', 'subx', 'adds', 'addx', 'addsx',
    'subsx', 'cmpsx', 'setcz', 'setci', 'setcq', 'setcy', 'setcfrq', 'setcmod',
    'setpiv', 'setpix', 'allowi', 'stalli', 'trgint', 'nixint', 'setint', 'setse',
    'pollint', 'pollse', 'pollpat', 'pollfbw', 'pollxmt', 'pollxfi', 'pollxro', 'pollxrl',
    'waitse', 'waitse', 'getptr', 'getint', 'setbrk', 'cogbrk', 'brk', 'setluts',
    'rcr', 'rcl', 'rczr', 'rczl', 'seussr', 'seussf', 'rgbsqz', 'rgbexp', 'xoro32'
}

def format_instruction_in_code(line):
    """Format PASM instructions in a line of code to UPPERCASE + BOLD."""
    # Skip pure comment lines
    if line.strip().startswith("'"):
        return line
    
    # Split into code and comment
    if "'" in line:
        code_part, comment_part = line.split("'", 1)
        comment_part = "'" + comment_part
    else:
        code_part = line
        comment_part = ""
    
    # Tokenize the code part preserving whitespace
    import re
    tokens = re.split(r'(\s+)', code_part)
    
    # Process tokens
    formatted_tokens = []
    found_instruction = False
    
    for token in tokens:
        token_lower = token.lower()
        
        # Skip whitespace
        if not token.strip():
            formatted_tokens.append(token)
            continue
            
        # First non-whitespace token might be label (check for : or if it's an instruction)
        if not found_instruction:
            if token_lower in PASM_INSTRUCTIONS:
                # It's an instruction
                formatted_tokens.append(f"**{token.upper()}**")
                found_instruction = True
            else:
                # It's likely a label or other token
                formatted_tokens.append(token)
        else:
            # After instruction, keep everything as-is
            formatted_tokens.append(token)
    
    return ''.join(formatted_tokens) + comment_part

def process_file(input_path, output_path):
    """Process a markdown file to format PASM instructions."""
    
    with open(input_path, 'r') as f:
        lines = f.readlines()
    
    output_lines = []
    in_code_block = False
    code_block_type = None
    
    for line in lines:
        # Check for code block boundaries
        if line.strip().startswith("```"):
            if not in_code_block:
                # Starting a code block
                in_code_block = True
                if 'pasm' in line.lower():
                    code_block_type = 'pasm'
                else:
                    code_block_type = 'other'
            else:
                # Ending a code block
                in_code_block = False
                code_block_type = None
            output_lines.append(line)
        
        elif in_code_block and code_block_type == 'pasm':
            # Format instructions in PASM code blocks
            output_lines.append(format_instruction_in_code(line))
        
        else:
            # For now, pass through other lines unchanged
            # Could add inline instruction formatting here if needed
            output_lines.append(line)
    
    # Write output
    with open(output_path, 'w') as f:
        f.writelines(output_lines)
    
    print(f"Formatted {input_path} -> {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python format-pasm-instructions.py input.md output.md")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    process_file(input_file, output_file)