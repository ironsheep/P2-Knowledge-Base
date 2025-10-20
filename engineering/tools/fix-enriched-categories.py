#!/usr/bin/env python3
"""
Fix enriched instruction files by restoring correct categories and oneliners from KB files.
Replaces 'group:' with 'category:' and adds 'oneliner:' for schema consistency.
"""

import os
import re
import yaml

# Paths
enriched_dir = "engineering/ingestion/enriched-instructions/pasm2-narratives"
kb_dir = "engineering/knowledge-base/P2/language/pasm2"

def extract_field(file_path, field_name):
    """Extract a specific field value from a YAML file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            # Use regex to find the field (handles multi-line values)
            pattern = rf'^{field_name}:\s*(.+?)(?=\n\w+:|$)'
            match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
            if match:
                return match.group(1).strip()
    except Exception as e:
        print(f"  Error reading {file_path}: {e}")
    return None

def fix_enriched_file(enriched_path, kb_path):
    """Fix one enriched file by restoring category and oneliner from KB."""
    filename = os.path.basename(enriched_path)
    
    # Get correct values from KB file
    kb_category = extract_field(kb_path, 'category')
    kb_oneliner = extract_field(kb_path, 'oneliner')
    
    if not kb_category:
        print(f"  ⚠️  {filename}: No category found in KB file")
        return False
    
    # Read enriched file
    try:
        with open(enriched_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"  ❌ {filename}: Error reading enriched file: {e}")
        return False
    
    original_content = content
    changes = []
    
    # Replace 'group:' with 'category:'
    if 'group:' in content:
        # Find and replace the group line
        content = re.sub(r'^group:.*$', f'category: {kb_category}', content, flags=re.MULTILINE)
        changes.append(f"group → category: {kb_category}")
    
    # Add oneliner if missing (insert after category or group)
    if 'oneliner:' not in content and kb_oneliner:
        # Find where to insert (after category line)
        content = re.sub(
            r'(^category:.*$)',
            rf'\1\noneliner: {kb_oneliner}',
            content,
            flags=re.MULTILINE
        )
        changes.append(f"added oneliner: {kb_oneliner}")
    
    # Write back if changes were made
    if content != original_content:
        try:
            with open(enriched_path, 'w') as f:
                f.write(content)
            print(f"  ✅ {filename}: {', '.join(changes)}")
            return True
        except Exception as e:
            print(f"  ❌ {filename}: Error writing: {e}")
            return False
    else:
        print(f"  ℹ️  {filename}: No changes needed")
        return False

def main():
    print("=== Fixing Enriched Instruction Files ===")
    print(f"Enriched dir: {enriched_dir}")
    print(f"KB dir: {kb_dir}")
    print()
    
    # Get all enriched YAML files
    enriched_files = sorted([f for f in os.listdir(enriched_dir) if f.endswith('.yaml')])
    
    fixed_count = 0
    error_count = 0
    
    for filename in enriched_files:
        enriched_path = os.path.join(enriched_dir, filename)
        kb_path = os.path.join(kb_dir, filename)
        
        if not os.path.exists(kb_path):
            print(f"  ⚠️  {filename}: KB file not found")
            error_count += 1
            continue
        
        if fix_enriched_file(enriched_path, kb_path):
            fixed_count += 1
    
    print()
    print(f"=== Summary ===")
    print(f"Total files: {len(enriched_files)}")
    print(f"Fixed: {fixed_count}")
    print(f"Errors: {error_count}")

if __name__ == "__main__":
    main()
