#!/usr/bin/env python3
"""
Consolidate duplicate Jon McPhalen entries into single canonical form
"""

import os
import yaml
from pathlib import Path
import time

def consolidate_jon_mcphalen_entries():
    """Consolidate all Jon McPhalen variants to 'Jon McPhalen (jonnymac)'"""
    objects_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects")
    
    canonical_author = "Jon McPhalen (jonnymac)"
    variants_to_consolidate = ["Jon McPhalen"]  # Keep the (jonnymac) version as canonical
    
    consolidated_count = 0
    
    print("Consolidating Jon McPhalen author entries...")
    
    for yaml_file in objects_dir.glob("*.yaml"):
        if yaml_file.name == "_template.yaml":
            continue
            
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            current_author = data['object_metadata'].get('author', '').strip()
            
            # Check if this is a variant that needs consolidation
            if current_author in variants_to_consolidate:
                obj_id = data['object_metadata']['object_id']
                title = data['object_metadata']['title']
                
                print(f"Consolidating {obj_id}: '{current_author}' → '{canonical_author}'")
                
                # Update to canonical form
                data['object_metadata']['author'] = canonical_author
                
                # Update metadata
                current_time = time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
                if 'metadata' not in data['object_metadata']:
                    data['object_metadata']['metadata'] = {}
                
                data['object_metadata']['metadata']['last_author_consolidation'] = current_time
                
                # Write back to file
                with open(yaml_file, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, sort_keys=False)
                
                consolidated_count += 1
                
        except Exception as e:
            print(f"Error processing {yaml_file}: {e}")
    
    print(f"✓ Consolidated {consolidated_count} entries to '{canonical_author}'")
    return consolidated_count

def main():
    consolidate_jon_mcphalen_entries()
    print("\nJon McPhalen consolidation complete!")

if __name__ == "__main__":
    main()