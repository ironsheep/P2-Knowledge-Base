#!/usr/bin/env python3
"""
Fix Greg LaPolla duplicate entries (with and without trailing period)
"""

import os
import yaml
from pathlib import Path
import time

def fix_greg_lapolla_duplicates():
    """Consolidate Greg LaPolla variants"""
    objects_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects")
    
    canonical_author = "Greg LaPolla"
    variants_to_fix = ["Greg LaPolla."]  # Remove trailing period
    
    fixed_count = 0
    
    print("Fixing Greg LaPolla author variants...")
    
    for yaml_file in objects_dir.glob("*.yaml"):
        if yaml_file.name == "_template.yaml":
            continue
            
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            current_author = data['object_metadata'].get('author', '').strip()
            
            # Check if this is a variant that needs fixing
            if current_author in variants_to_fix:
                obj_id = data['object_metadata']['object_id']
                title = data['object_metadata']['title']
                
                print(f"Fixing {obj_id}: '{current_author}' → '{canonical_author}'")
                
                # Update to canonical form
                data['object_metadata']['author'] = canonical_author
                
                # Update metadata
                current_time = time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
                if 'metadata' not in data['object_metadata']:
                    data['object_metadata']['metadata'] = {}
                
                data['object_metadata']['metadata']['last_author_fix'] = current_time
                
                # Write back to file
                with open(yaml_file, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, sort_keys=False)
                
                fixed_count += 1
                
        except Exception as e:
            print(f"Error processing {yaml_file}: {e}")
    
    print(f"✓ Fixed {fixed_count} Greg LaPolla entries")
    return fixed_count

def main():
    fix_greg_lapolla_duplicates()
    print("Greg LaPolla consolidation complete!")

if __name__ == "__main__":
    main()