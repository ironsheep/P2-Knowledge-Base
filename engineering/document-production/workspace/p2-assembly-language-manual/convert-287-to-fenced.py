#!/usr/bin/env python3
"""
Convert 287 pasm2 divs to fenced code blocks, preserving original 43 divs.

This script identifies the original 43 divs by instruction+context patterns
and converts all others to ```pasm2 fenced code blocks.
"""
import re
from pathlib import Path

# Patterns that identify the original 43 divs (instruction, context1, context2)
ORIGINAL_43_PATTERNS = [
    # CORDIC examples (8)
    ("QDIV", "1000000", ""),
    ("QEXP", "log_value", ""),
    ("SETQ", "C0000000", ""),
    ("QLOG", "1000", ""),
    ("QMUL", "1000000", ""),
    ("SETQ", "#200", "#$20000000"),  # QROTATE with specific angle
    ("QSQRT", "1000000", ""),
    ("QVECTOR", "#100", ""),
    # Shift instructions (14)
    ("SAL", "data", ""),
    ("SAR", "value", ""),
    ("SCA     FACTOR", "$8000", "SCALE BY 0.5"),  # Match instruction format exactly
    ("SETBYTE", "data", ""),
    ("SETNIB", "data", ""),
    ("SETQ", "#16-1", "RDLONG"),
    ("SETQ", "#16-1", "WRLONG"),
    ("SETQ2", "#256-1", ""),
    ("SETWORD", "data", ""),
    ("SHL", "value", "Multiply"),
    ("SHR", "value", "Divide"),
    ("SIGNX", "value", ""),
    ("SKIP", "#%10101", ""),
    ("STALLI", "", ""),
    ("SUB", "count, #1 WZ", "Decrement"),
    # Test instructions (5)
    ("TEST", "flags WCZ", ""),
    ("TESTB", "flags, #7", ""),
    ("TESTP", "#10 WC", ""),
    ("TJNZ", "count", ""),
    ("ADDS", "result, delta", ""),
    # Wait instructions (3)
    ("WAITATN", "", "attention"),
    ("SETPAT", "mask, pattern", ""),
    ("WAITX", "#99", ""),
    # Write instructions (4)
    ("WRBYTE", "value, ptra++", ""),
    ("WRFAST", "buffer_addr", ""),
    ("WRLUT", "#100", ""),
    # Pin/other (4)
    ("DIRL", "#10", "Reset"),
    ("WYPIN", "pwm_value", ""),
    ("XINIT", "mode, data", ""),
    ("MOV", "seed, initial", ""),
    # ZEROX (1)
    ("' Extract", "lower byte", ""),
    # Appendix J bugs (4)
    ("SETQ", "#16-1", "ALTD"),
    ("' Workaround: Adjust", "", ""),
    ("AUGS", "FFFFF123", ""),
    ("' Workaround: Use register", "", ""),
]


def is_original_43(content):
    """Check if div content matches one of the original 43 patterns."""
    text = content.upper()
    for instr, ctx1, ctx2 in ORIGINAL_43_PATTERNS:
        if instr.upper() in text and ctx1.upper() in text:
            if ctx2 == "" or ctx2.upper() in text:
                return True
    return False


def process_file(filepath):
    """Process a single markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'^::: pasm2\n(.*?)^:::$'

    kept_count = 0
    converted_count = 0

    def replacer(match):
        nonlocal kept_count, converted_count
        div_content = match.group(1)

        if is_original_43(div_content):
            kept_count += 1
            return match.group(0)  # Keep as div
        else:
            converted_count += 1
            return f'```pasm2\n{div_content}```'  # Convert to fenced

    new_content = re.sub(pattern, replacer, content, flags=re.MULTILINE | re.DOTALL)

    if converted_count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return kept_count, converted_count


def main():
    opus_master = Path('/workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master')

    total_kept = 0
    total_converted = 0

    md_files = list(opus_master.rglob('*.md'))

    print("Converting pasm2 divs to fenced blocks (preserving original 43)...")
    print()

    for filepath in sorted(md_files):
        kept, converted = process_file(filepath)
        if kept > 0 or converted > 0:
            rel_path = filepath.relative_to(opus_master)
            print(f"  {rel_path}: kept {kept}, converted {converted}")
            total_kept += kept
            total_converted += converted

    print()
    print("=" * 60)
    print(f"Total kept as divs: {total_kept} (target: 43)")
    print(f"Total converted to fenced: {total_converted} (target: 287)")
    print("=" * 60)


if __name__ == '__main__':
    main()
