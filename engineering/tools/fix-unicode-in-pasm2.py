#!/usr/bin/env python3
"""
Fix Unicode Characters in PASM2 YAML Files

Replaces all Unicode escape sequences with ASCII equivalents in PASM2 instruction files.
Preserves file structure and only modifies content, not formatting.

Usage:
    python3 engineering/tools/fix-unicode-in-pasm2.py [--dry-run]

Arguments:
    --dry-run    Show what would be changed without modifying files
"""

import os
import sys
import re
from pathlib import Path
import argparse

# Unicode to ASCII replacement mapping
UNICODE_REPLACEMENTS = {
    # Typography ligatures (most common)
    r'\\uFB02': 'fl',      # ﬂ -> fl (896 occurrences)
    r'\\uFB01': 'fi',      # ﬁ -> fi (629 occurrences)
    r'\\uFB03': 'ffi',     # ﬃ -> ffi (1 occurrence)
    
    # Dashes
    r'\\u2014': '--',      # — (em dash) -> -- (543 occurrences)
    r'\\u2013': '-',       # – (en dash) -> - (243 occurrences)
    r'\\u2011': '-',       # ‑ (non-breaking hyphen) -> - (2 occurrences)
    
    # Bullets and symbols
    r'\\u25CF': '*',       # ● (bullet) -> * (128 occurrences)
    r'\\u25AA': '*',       # ▪ (small square) -> * (20 occurrences)
    
    # Arrows
    r'\\u21E8': '->',      # ⇨ (arrow) -> -> (12 occurrences)
    r'\\u21D2': '=>',      # ⇒ (implies arrow) -> => (1 occurrence)
    r'\\u21C4': '<->',     # ⇄ (bidirectional arrow) -> <-> (1 occurrence)
    
    # Mathematical symbols
    r'\\u221A': 'sqrt',    # √ (square root) -> sqrt (6 occurrences)
    r'\\u2248': '~=',      # ≈ (approximately) -> ~= (2 occurrences)
    r'\\u2264': '<=',      # ≤ (less than/equal) -> <= (1 occurrence)
    r'\\u03C0': 'pi',      # π (pi) -> pi (1 occurrence)
    
    # Quotes
    r'\\u2019': "'",       # ' (right single quote) -> ' (3 occurrences)
    r'\\u201C': '"',       # " (left double quote) -> " (1 occurrence)
    r'\\u201D': '"',       # " (right double quote) -> " (1 occurrence)
}

def count_unicode_occurrences(content: str) -> dict:
    """Count occurrences of each Unicode pattern in content"""
    counts = {}
    for unicode_pattern in UNICODE_REPLACEMENTS.keys():
        matches = re.findall(unicode_pattern, content)
        if matches:
            counts[unicode_pattern] = len(matches)
    return counts

def replace_unicode_in_content(content: str) -> tuple[str, dict]:
    """Replace all Unicode patterns with ASCII equivalents"""
    replacements_made = {}
    modified_content = content
    
    for unicode_pattern, ascii_replacement in UNICODE_REPLACEMENTS.items():
        matches = re.findall(unicode_pattern, modified_content)
        if matches:
            replacements_made[unicode_pattern] = len(matches)
            modified_content = re.sub(unicode_pattern, ascii_replacement, modified_content)
    
    return modified_content, replacements_made

def process_file(file_path: Path, dry_run: bool = False) -> dict:
    """Process a single YAML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Count original Unicode occurrences
        original_counts = count_unicode_occurrences(original_content)
        
        if not original_counts:
            return {'status': 'clean', 'file': file_path}
        
        # Replace Unicode with ASCII
        fixed_content, replacements = replace_unicode_in_content(original_content)
        
        if dry_run:
            return {
                'status': 'would_fix',
                'file': file_path,
                'original_counts': original_counts,
                'replacements': replacements
            }
        else:
            # Write the fixed content back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            return {
                'status': 'fixed',
                'file': file_path,
                'original_counts': original_counts,
                'replacements': replacements
            }
    
    except Exception as e:
        return {
            'status': 'error',
            'file': file_path,
            'error': str(e)
        }

def main():
    parser = argparse.ArgumentParser(description='Fix Unicode characters in PASM2 YAML files')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be changed without modifying files')
    args = parser.parse_args()
    
    # Get the repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent
    pasm2_dir = repo_root / "engineering" / "knowledge-base" / "P2" / "language" / "pasm2"
    
    if not pasm2_dir.exists():
        print(f"❌ PASM2 directory not found: {pasm2_dir}")
        sys.exit(1)
    
    print(f"🔍 Scanning PASM2 directory: {pasm2_dir}")
    if args.dry_run:
        print("🧪 DRY RUN MODE - No files will be modified")
    print()
    
    # Find all YAML files in PASM2 directory
    yaml_files = list(pasm2_dir.rglob("*.yaml"))
    
    if not yaml_files:
        print("❌ No YAML files found in PASM2 directory")
        sys.exit(1)
    
    print(f"📄 Found {len(yaml_files)} YAML files")
    print()
    
    # Process statistics
    total_files = len(yaml_files)
    clean_files = 0
    fixed_files = 0
    error_files = 0
    total_replacements = {}
    
    # Process each file
    for yaml_file in yaml_files:
        result = process_file(yaml_file, args.dry_run)
        
        if result['status'] == 'clean':
            clean_files += 1
        elif result['status'] in ['fixed', 'would_fix']:
            fixed_files += 1
            # Accumulate replacement counts
            for unicode_pattern, count in result['replacements'].items():
                total_replacements[unicode_pattern] = total_replacements.get(unicode_pattern, 0) + count
            
            # Show file details for verbose output
            relative_path = yaml_file.relative_to(repo_root)
            action = "Would fix" if args.dry_run else "Fixed"
            print(f"✏️  {action}: {relative_path}")
            for unicode_pattern, count in result['replacements'].items():
                ascii_replacement = UNICODE_REPLACEMENTS[unicode_pattern]
                print(f"     {unicode_pattern} -> '{ascii_replacement}' ({count} times)")
        
        elif result['status'] == 'error':
            error_files += 1
            relative_path = yaml_file.relative_to(repo_root)
            print(f"❌ Error processing: {relative_path}")
            print(f"   {result['error']}")
    
    # Print summary
    print()
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Total files processed: {total_files}")
    print(f"Clean files (no Unicode): {clean_files}")
    
    if args.dry_run:
        print(f"Files that would be fixed: {fixed_files}")
    else:
        print(f"Files fixed: {fixed_files}")
    
    if error_files > 0:
        print(f"Files with errors: {error_files}")
    
    print()
    
    if total_replacements:
        print("🔄 Unicode Replacements Made:")
        for unicode_pattern, total_count in sorted(total_replacements.items(), 
                                                  key=lambda x: x[1], reverse=True):
            ascii_replacement = UNICODE_REPLACEMENTS[unicode_pattern]
            print(f"   {unicode_pattern} -> '{ascii_replacement}': {total_count} times")
        
        total_unicode_fixed = sum(total_replacements.values())
        print(f"\n✅ Total Unicode characters replaced: {total_unicode_fixed}")
        
        if args.dry_run:
            print(f"\n🧪 This was a DRY RUN - no files were actually modified")
            print(f"Run without --dry-run to apply these changes")
    else:
        print("✅ No Unicode characters found - all files are already clean!")
    
    print()
    
    # Exit with error code if there were any errors
    if error_files > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()