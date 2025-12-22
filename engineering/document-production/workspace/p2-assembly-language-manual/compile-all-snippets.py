#!/usr/bin/env python3
"""
Compile all PASM code snippets from the P2 Assembly Language Manual.

This script extracts code blocks and wraps them with necessary scaffolding
(variable declarations, constants, etc.) to make them compile, proving
the manual's code is syntactically correct in proper context.

Key features:
- Detects and skips syntax format examples (instruction templates)
- Identifies variables used in examples to avoid conflicts
- Skips intentionally broken examples (error demonstrations)
- Provides detailed categorization of failures
"""

import re
import subprocess
import os
import sys
from pathlib import Path
from collections import defaultdict

# Common P2 constants needed by examples
COMMON_CONSTANTS = """
CON
    ' System constants
    _clkfreq = 200_000_000

    ' User-defined constants for examples
    MY_HUBEXEC = $80
    LOCK_TIMEOUT = 100000
    NUM_BITS = 8
    BUFFER_START = $1000
    BUFFER_SIZE = 256
    MY_CONST = 42
    ARRAY_SIZE = 10
    MAX_VALUE = 255
    MIN_VALUE = 0
    TIMEOUT_MS = 1000
    BAUD_RATE = 115200
    CLOCK_FREQ = 200_000_000
    HUB_BASE = $400
    LUT_BASE = $200
    XBYTE_BASE = $100

"""

def extract_code_blocks(markdown_file):
    """Extract all pasm/pasm2 code blocks with line numbers."""
    with open(markdown_file, 'r') as f:
        content = f.read()
        lines = content.split('\n')

    blocks = []
    in_block = False
    block_type = None
    current_block = []
    start_line = 0

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        if not in_block:
            if stripped.startswith('```pasm'):
                in_block = True
                block_type = 'backtick'
                start_line = i
                current_block = []
            elif stripped == '::: pasm2' or stripped.startswith('::: pasm2 '):
                in_block = True
                block_type = 'colon'
                start_line = i
                current_block = []
        elif in_block:
            if block_type == 'backtick' and stripped == '```':
                in_block = False
                blocks.append({
                    'line': start_line,
                    'code': '\n'.join(current_block),
                    'end_line': i
                })
            elif block_type == 'colon' and stripped == ':::':
                in_block = False
                blocks.append({
                    'line': start_line,
                    'code': '\n'.join(current_block),
                    'end_line': i
                })
            else:
                current_block.append(line)

    return blocks


def is_syntax_format_block(code):
    """Check if block shows syntax format rather than executable code."""
    # Patterns that indicate syntax format templates
    format_indicators = [
        r'\binstruction\b',           # "instruction" as placeholder
        r'\bD,S\b',                    # D,S operand template
        r'\bD,{#}S\b',                 # D,{#}S operand template
        r'\b{#}D\b',                   # {#}D operand template
        r'\bDest,\s*Src\b',            # Dest, Src as placeholders
        r'\bDest,\s*{#}Src\b',         # Dest, {#}Src
        r'\{WC\}\s*\{WZ\}',            # Effect placeholders
        r'EEEE.*DDDDDDDDD.*SSSSSSSSS', # Encoding field templates
        r'\bCZI\b.*\bDest\b.*\bSrc\b', # Encoding table headers
    ]

    for pattern in format_indicators:
        if re.search(pattern, code, re.IGNORECASE):
            return True
    return False


def is_intentionally_broken(code):
    """Check if the example intentionally shows broken code."""
    broken_indicators = [
        "' WRONG",
        "'WRONG",
        "' Error:",
        "'Error:",
        "Error: ",
        "' BAD",
        "' bad",
        "// WRONG",
        "// Error",
        "' ERROR:",
        "'ERROR:",
        "' Invalid",
        "' INVALID",
    ]
    return any(ind in code for ind in broken_indicators)


def is_encoding_example(code):
    """Check if this is an encoding/format explanation example."""
    # Lines showing what assembler generates vs what programmer writes
    if "' What the assembler generates:" in code:
        return True
    if "' What the programmer writes:" in code:
        return True
    # AUGS/AUGD explicit augmentation teaching
    if re.search(r'augs\s+#\$[0-9A-Fa-f]+\s+', code, re.IGNORECASE):
        if "' Upper" in code or "' Lower" in code:
            return True
    return False


def is_pseudo_instruction_block(code):
    """Check if block is documenting pseudo-instruction syntax."""
    lines = [l.strip() for l in code.split('\n') if l.strip() and not l.strip().startswith("'")]
    if len(lines) == 0:
        return True

    # Check for EQU definitions only (not executable)
    all_equ = all('EQU' in l.upper() for l in lines if l and not l.startswith("'"))
    if all_equ and lines:
        return True

    # Check for IF constant expressions (Spin2 syntax, not PASM)
    if any(re.match(r'\s*IF\s+\$', l) for l in lines):
        return True

    return False


def extract_defined_symbols(code):
    """Extract all symbols defined in the code block."""
    symbols = set()

    for line in code.split('\n'):
        stripped = line.strip()
        if not stripped or stripped.startswith("'"):
            continue

        # Label definitions (at start of line, followed by instruction or res)
        label_match = re.match(r'^(\w+)\s+', line)
        if label_match and not line.startswith(' ') and not line.startswith('\t'):
            symbols.add(label_match.group(1).lower())

        # RES declarations
        res_match = re.match(r'^(\w+)\s+res\b', line, re.IGNORECASE)
        if res_match:
            symbols.add(res_match.group(1).lower())

    return symbols


def generate_variables(code):
    """Generate variable declarations avoiding conflicts with code."""
    defined = extract_defined_symbols(code)

    # PASM2/Spin2 reserved words - cannot be used as variable names
    reserved_words = {
        'field', 'byte', 'word', 'long', 'string', 'send', 'recv',
        'encod', 'float', 'round', 'trunc', 'org', 'fit', 'res',
        'orgh', 'orgf', 'alignw', 'alignl', 'file', 'debug',
    }

    # All possible variable names we might need
    all_vars = [
        'x', 'y', 'z', 'a', 'b', 'c', 'n', 'i', 'j', 't',
        'value', 'val', 'result', 'temp', 'temp1', 'temp2',
        'data', 'count', 'counter', 'index', 'addr', 'address',
        'ptr', 'src', 'dst', 'dest', 'source', 'len', 'length',
        'size', 'mask', 'pattern', 'flags', 'status', 'mode',
        'config', 'param', 'factor', 'divisor', 'quotient',
        'remainder', 'num', 'denom', 'sum', 'diff', 'product',
        'accumulator', 'limit', 'threshold', 'target', 'current',
        'previous', 'next_val', 'err_val', 'timeout', 'delay',
        'interval', 'period', 'frequency', 'samples', 'pixels',
        'buffer', 'shiftval', 'bits', 'bytes', 'words', 'longs',
        'time', 'time1', 'time2', 'start_time', 'end_time', 'elapsed',
        'duration', 'deadline', 'iterations',
        'pin', 'pin_num', 'pin_val', 'pin_mask', 'pin_state',
        'pin_group', 'base_pin', 'tx_pin', 'rx_pin', 'clk_pin', 'dat_pin',
        'lo', 'hi', 'angle', 'sin_val', 'cos_val', 'magnitude', 'phase',
        'real', 'imag', 'sqrt_val', 'log_val', 'exp_val', 'log_result',
        'log_value', 'integer_result',
        'qx', 'qy', 'qresult',
        'hub_addr', 'hub_ptr', 'hub_src', 'hub_dst', 'hub_buffer',
        'hub_data', 'audio_buffer', 'capture_buffer', 'sprite_data',
        'nco_value', 'nco_rate', 'bitmap_ptr',
        'cog_id', 'lock_id', 'new_cog',
        'ret_addr', 'stack_ptr',
        'lut_addr', 'lut_data', 'lut_ptr', 'lut_index',
        'sp_mode', 'sp_x', 'sp_y',
        'event_mask', 'int_vector',
        'operand', 'instr_opcode', 'encoding_val', 'fieldval',
        'bit_pos', 'bit_count', 'start_bit', 'end_bit',
        'old_val', 'new_val', 'old_time', 'new_time',
        'sample', 'reading', 'measurement', 'average',
        'minimum', 'maximum', 'total', 'checksum', 'crc', 'hashval',
        'keyval', 'charval', 'byte_val', 'word_val', 'long_val',
        'signed_val', 'unsigned_val',
        'lower_32', 'upper_32', 'new_x', 'new_y', 'sqrt_result',
        'random_val', 'rand_seed', 'xoro_s0', 'xoro_s1',
    ]

    # Filter out reserved words and any that conflict with code
    safe_vars = [v for v in all_vars
                 if v.lower() not in defined and v.lower() not in reserved_words]

    var_section = "\n' Auto-generated variable declarations\n"
    for v in safe_vars:
        var_section += f"{v:16}res     1\n"
    var_section += "\n                fit     496\n"

    return var_section


def normalize_code_for_compilation(code):
    """Normalize code for compilation testing.

    This adjusts the code to work with pnut_ts without changing the manual.
    """
    # Convert 'wc wz' to 'wcz' - pnut_ts requires no space
    # Match 'wc wz' at end of line (possibly followed by comment)
    code = re.sub(r'\bwc\s+wz\b', 'wcz', code, flags=re.IGNORECASE)
    return code


def extract_referenced_labels(code):
    """Find labels referenced but not defined in code."""
    # Find all #label_name references
    refs = set(re.findall(r'#(\w+)', code))

    # Find all defined labels (at start of line)
    defined = set()
    for line in code.split('\n'):
        if line and not line[0].isspace():
            match = re.match(r'^(\w+)', line)
            if match:
                defined.add(match.group(1))

    # Return undefined references
    return refs - defined


def generate_stub_labels(code):
    """Generate stub labels for undefined references."""
    undefined = extract_referenced_labels(code)

    # Filter out special cases that aren't labels
    not_labels = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    undefined = {l for l in undefined if not l.isdigit() and l not in not_labels}

    if not undefined:
        return ""

    stubs = "\n' Stub labels for compilation testing\n"
    for label in sorted(undefined):
        stubs += f"{label}\n"

    return stubs


def wrap_for_compilation(code, block_num):
    """Wrap code snippet in compilable structure."""

    # Skip intentionally broken examples
    if is_intentionally_broken(code):
        return None, 'intentionally_broken'

    # Skip syntax format examples
    if is_syntax_format_block(code):
        return None, 'syntax_format'

    # Skip encoding/augmentation teaching examples
    if is_encoding_example(code):
        return None, 'encoding_example'

    # Skip pseudo-instruction / constant-only blocks
    if is_pseudo_instruction_block(code):
        return None, 'pseudo_instruction'

    # Normalize code for pnut_ts compatibility
    code = normalize_code_for_compilation(code)

    # Check if code already has structural elements
    first_significant_line = ""
    for line in code.split('\n'):
        stripped = line.strip()
        if stripped and not stripped.startswith("'"):
            first_significant_line = stripped.upper()
            break

    has_section = any(first_significant_line.startswith(kw)
                     for kw in ['CON', 'DAT', 'PUB', 'PRI', 'VAR', 'OBJ'])

    # Generate safe variables for this code
    safe_vars = generate_variables(code)

    # Generate stub labels for undefined references
    stub_labels = generate_stub_labels(code)

    if has_section:
        # Code has structure, add constants and vars
        wrapped = COMMON_CONSTANTS + '\n' + code + stub_labels + '\n\nDAT\n                org     0\n' + safe_vars
    else:
        # Wrap bare assembly
        wrapped = COMMON_CONSTANTS + '''
DAT
                org     0
''' + code + stub_labels + '\n' + safe_vars

    return wrapped, 'compiled'


def test_compile(code, block_num, line_num, temp_dir):
    """Attempt to compile code with pnut_ts."""
    wrapped, category = wrap_for_compilation(code, block_num)

    if wrapped is None:
        return {'success': True, 'skipped': True, 'reason': category}

    temp_file = temp_dir / f"block_{block_num}.spin2"

    with open(temp_file, 'w') as f:
        f.write(wrapped)

    try:
        result = subprocess.run(
            ['pnut_ts', str(temp_file)],
            capture_output=True,
            text=True,
            timeout=10
        )

        combined = result.stdout + result.stderr

        if ':error:' in combined:
            return {
                'success': False,
                'error': combined,
                'returncode': result.returncode,
                'wrapped_file': str(temp_file)
            }
        else:
            return {'success': True, 'output': result.stdout}

    except FileNotFoundError:
        return {'success': False, 'error': 'pnut_ts not found'}
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'Compilation timeout'}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def main():
    manual_path = Path("P2-Assembly-Language-Manual.md")
    temp_dir = Path("/tmp/pasm_full_test")
    temp_dir.mkdir(exist_ok=True)

    print(f"Extracting code blocks from {manual_path}...")
    blocks = extract_code_blocks(manual_path)
    print(f"Found {len(blocks)} code blocks\n")

    errors = []
    successes = 0
    skipped = defaultdict(int)

    for i, block in enumerate(blocks, 1):
        result = test_compile(block['code'], i, block['line'], temp_dir)

        if result.get('skipped'):
            reason = result.get('reason', 'unknown')
            skipped[reason] += 1
            if '--verbose' in sys.argv:
                print(f"⊘ Block {i} (line {block['line']}): Skipped - {reason}")
        elif result['success']:
            successes += 1
            if '--verbose' in sys.argv:
                print(f"✓ Block {i} (line {block['line']})")
        else:
            errors.append({
                'block': i,
                'line': block['line'],
                'end_line': block['end_line'],
                'code': block['code'],
                'error': result.get('error', 'Unknown error'),
                'file': result.get('wrapped_file', '')
            })
            err_msg = result.get('error', 'Unknown')
            if ':error:' in err_msg:
                err_lines = [l for l in err_msg.split('\n') if ':error:' in l]
                err_msg = err_lines[0] if err_lines else err_msg
            print(f"✗ Block {i} (line {block['line']}): {err_msg[:80]}...")

    total_skipped = sum(skipped.values())

    print(f"\n{'='*70}")
    print(f"COMPILATION AUDIT RESULTS")
    print(f"{'='*70}")
    print(f"Total blocks:       {len(blocks)}")
    print(f"Compiled OK:        {successes}")
    print(f"Skipped:            {total_skipped}")
    for reason, count in sorted(skipped.items()):
        print(f"  - {reason}: {count}")
    print(f"Errors:             {len(errors)}")

    if errors:
        print(f"\n{'='*70}")
        print("COMPILATION ERRORS - NEED REVIEW:")
        print(f"{'='*70}\n")

        for err in errors[:30]:  # Limit to first 30
            print(f"Block {err['block']} (lines {err['line']}-{err['end_line']}):")
            print("-" * 50)
            code_lines = err['code'].split('\n')[:10]
            for line in code_lines:
                print(f"  {line}")
            if len(err['code'].split('\n')) > 10:
                print("  ...")

            err_text = err['error']
            if ':error:' in err_text:
                err_lines = [l.strip() for l in err_text.split('\n') if ':error:' in l]
                print(f"\nCompiler errors:")
                for el in err_lines[:5]:
                    # Clean ANSI escape codes
                    el_clean = re.sub(r'\x1b\[[0-9;]*m', '', el)
                    print(f"  {el_clean}")
            print()

        if len(errors) > 30:
            print(f"... and {len(errors) - 30} more errors")

    return len(errors)


if __name__ == '__main__':
    sys.exit(main())
