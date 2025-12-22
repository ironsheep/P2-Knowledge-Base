#!/usr/bin/env python3
"""
Convert ```pasm code blocks to ::: pasm2 fenced divs.

Safety features:
1. Stateful parsing - only converts matching open/close pairs
2. Dry-run mode - shows what would change without modifying
3. Validates block counts before/after
4. Creates backups before modifying
5. Shows per-file diffs

Usage:
    python3 convert-pasm-to-pasm2.py --dry-run    # Preview changes
    python3 convert-pasm-to-pasm2.py --execute    # Make changes
"""

import argparse
import shutil
from pathlib import Path
from datetime import datetime
import difflib

OPUS_MASTER = Path('/workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master')


def convert_file(filepath: Path, dry_run: bool = True) -> tuple[int, str, str]:
    """
    Convert ```pasm blocks to ::: pasm2 in a single file.
    
    Returns: (blocks_converted, original_content, new_content)
    """
    original = filepath.read_text()
    lines = original.split('\n')
    new_lines = []
    
    in_pasm_block = False
    blocks_converted = 0
    
    for line in lines:
        stripped = line.strip()
        
        if stripped == '```pasm':
            # Convert opening
            new_lines.append('::: pasm2')
            in_pasm_block = True
            blocks_converted += 1
        elif stripped == '```' and in_pasm_block:
            # Convert closing (only if we're in a pasm block)
            new_lines.append(':::')
            in_pasm_block = False
        else:
            # Keep line unchanged
            new_lines.append(line)
    
    new_content = '\n'.join(new_lines)
    return blocks_converted, original, new_content


def count_blocks(content: str) -> dict:
    """Count different block types in content."""
    lines = content.split('\n')
    counts = {
        'pasm_fenced': 0,
        'pasm2_fenced': 0,
        'pasm2_div': 0,
    }
    
    for line in lines:
        stripped = line.strip()
        if stripped == '```pasm':
            counts['pasm_fenced'] += 1
        elif stripped == '```pasm2':
            counts['pasm2_fenced'] += 1
        elif stripped == '::: pasm2':
            counts['pasm2_div'] += 1
    
    return counts


def show_diff(filepath: Path, original: str, new: str):
    """Show unified diff for a file."""
    diff = difflib.unified_diff(
        original.splitlines(keepends=True),
        new.splitlines(keepends=True),
        fromfile=f'a/{filepath.name}',
        tofile=f'b/{filepath.name}',
        lineterm=''
    )
    diff_text = ''.join(diff)
    if diff_text:
        print(f"\n{'='*60}")
        print(f"FILE: {filepath.relative_to(OPUS_MASTER)}")
        print('='*60)
        # Show abbreviated diff (first 30 lines)
        diff_lines = diff_text.split('\n')
        for line in diff_lines[:30]:
            print(line)
        if len(diff_lines) > 30:
            print(f"... ({len(diff_lines) - 30} more lines)")


def main():
    parser = argparse.ArgumentParser(description='Convert ```pasm to ::: pasm2')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without modifying')
    parser.add_argument('--execute', action='store_true', help='Actually make the changes')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show diffs')
    args = parser.parse_args()
    
    if not args.dry_run and not args.execute:
        print("ERROR: Must specify --dry-run or --execute")
        print("  --dry-run : Preview what would change")
        print("  --execute : Make the changes (creates backups)")
        return 1
    
    if args.execute:
        print("⚠️  EXECUTE MODE - Files will be modified")
        print("    Backups will be created with .backup-pasm-conversion suffix")
    else:
        print("🔍 DRY-RUN MODE - No files will be modified")
    
    print(f"\nScanning: {OPUS_MASTER}")
    print()
    
    # Collect all markdown files
    md_files = [f for f in OPUS_MASTER.rglob('*.md') if 'backup' not in str(f)]
    
    # Pre-conversion counts
    total_before = {'pasm_fenced': 0, 'pasm2_fenced': 0, 'pasm2_div': 0}
    for f in md_files:
        counts = count_blocks(f.read_text())
        for k, v in counts.items():
            total_before[k] += v
    
    print("BEFORE conversion:")
    print(f"  ```pasm blocks:  {total_before['pasm_fenced']}")
    print(f"  ```pasm2 blocks: {total_before['pasm2_fenced']}")
    print(f"  ::: pasm2 divs:  {total_before['pasm2_div']}")
    print()
    
    # Process files
    total_converted = 0
    files_modified = 0
    
    for filepath in sorted(md_files):
        blocks_converted, original, new_content = convert_file(filepath, dry_run=args.dry_run)
        
        if blocks_converted > 0:
            files_modified += 1
            total_converted += blocks_converted
            
            if args.verbose or args.dry_run:
                show_diff(filepath, original, new_content)
            
            if args.execute:
                # Create backup
                backup_path = filepath.with_suffix('.md.backup-pasm-conversion')
                shutil.copy2(filepath, backup_path)
                # Write new content
                filepath.write_text(new_content)
                print(f"  ✓ {filepath.relative_to(OPUS_MASTER)}: {blocks_converted} blocks converted")
    
    print()
    print(f"{'='*60}")
    print("SUMMARY")
    print('='*60)
    print(f"  Files scanned:    {len(md_files)}")
    print(f"  Files modified:   {files_modified}")
    print(f"  Blocks converted: {total_converted}")
    
    # Post-conversion counts (for dry-run, simulate; for execute, re-read)
    if args.execute:
        total_after = {'pasm_fenced': 0, 'pasm2_fenced': 0, 'pasm2_div': 0}
        for f in md_files:
            counts = count_blocks(f.read_text())
            for k, v in counts.items():
                total_after[k] += v
        
        print()
        print("AFTER conversion:")
        print(f"  ```pasm blocks:  {total_after['pasm_fenced']}")
        print(f"  ```pasm2 blocks: {total_after['pasm2_fenced']}")
        print(f"  ::: pasm2 divs:  {total_after['pasm2_div']}")
        
        # Validation
        expected_pasm2_divs = total_before['pasm2_div'] + total_before['pasm_fenced']
        if total_after['pasm2_div'] == expected_pasm2_divs and total_after['pasm_fenced'] == 0:
            print()
            print("✓ VALIDATION PASSED: Block counts match expected values")
        else:
            print()
            print("⚠️  VALIDATION WARNING: Counts don't match expected")
            print(f"    Expected ::: pasm2: {expected_pasm2_divs}, got: {total_after['pasm2_div']}")
    else:
        print()
        print("EXPECTED after conversion:")
        print(f"  ```pasm blocks:  0")
        print(f"  ```pasm2 blocks: {total_before['pasm2_fenced']}")
        print(f"  ::: pasm2 divs:  {total_before['pasm2_div'] + total_before['pasm_fenced']}")
    
    return 0


if __name__ == '__main__':
    exit(main())
