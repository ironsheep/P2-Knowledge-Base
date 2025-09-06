#!/usr/bin/env python3
"""
Update image catalog numbering from old format to new 3-4 letter prefix format.
"""

import re

def update_catalog_numbering(catalog_path, old_prefix="P2-", new_prefix="P2DS-"):
    """Update all numbering in markdown catalog"""
    
    with open(catalog_path, 'r') as f:
        content = f.read()
    
    # Find all instances of the old numbering format
    pattern = rf'{re.escape(old_prefix)}(\d+)'
    
    def replace_match(match):
        number = match.group(1)
        return f"{new_prefix}{number}"
    
    # Replace all occurrences
    updated_content = re.sub(pattern, replace_match, content)
    
    # Also update in the summary sections
    updated_content = updated_content.replace(
        f"**Document Prefix**: {old_prefix.rstrip('-')}", 
        f"**Document Prefix**: {new_prefix.rstrip('-')}"
    )
    
    # Update the total numbering line
    updated_content = re.sub(
        rf'{re.escape(old_prefix)}001 through {re.escape(old_prefix)}\d+',
        f"{new_prefix}001 through {new_prefix}039",
        updated_content
    )
    
    with open(catalog_path, 'w') as f:
        f.write(updated_content)
    
    print(f"✅ Updated catalog numbering from {old_prefix}### to {new_prefix}###")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 update_catalog_numbering.py <catalog_path> [old_prefix] [new_prefix]")
        sys.exit(1)
    
    catalog_path = sys.argv[1]
    old_prefix = sys.argv[2] if len(sys.argv) > 2 else "P2-"
    new_prefix = sys.argv[3] if len(sys.argv) > 3 else "P2DS-"
    
    update_catalog_numbering(catalog_path, old_prefix, new_prefix)