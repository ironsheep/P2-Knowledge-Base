#!/usr/bin/env python3
"""
Consolidate duplicate authors where archiver imports should map to existing OBEX accounts
"""

import os
import yaml
from pathlib import Path
import time

class AuthorConsolidator:
    def __init__(self, objects_dir):
        self.objects_dir = Path(objects_dir)
        self.consolidations = {
            # Map archiver import names to OBEX account names
            "Eric R. Smith": "ersmith",
            "mike calyer (mcalyer, mike.calyer@yahoo.com)": "mike calyer",
            "Riley August (riley@robots-everywhere.com)": "Riley August"
        }
        self.updated_objects = []
        
    def consolidate_authors(self):
        """Update author names in archiver import objects"""
        print("CONSOLIDATING DUPLICATE AUTHORS")
        print("=" * 60)
        
        for old_name, new_name in self.consolidations.items():
            print(f"\nMapping: '{old_name}' → '{new_name}'")
            
            # Find objects with the old author name
            objects_to_update = []
            for yaml_file in sorted(self.objects_dir.glob("*.yaml")):
                if yaml_file.name == "_template.yaml":
                    continue
                    
                try:
                    with open(yaml_file, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        
                    author = data['object_metadata'].get('author', '')
                    obj_id = data['object_metadata']['object_id']
                    title = data['object_metadata']['title']
                    
                    if author == old_name:
                        # Verify this is an archiver import
                        import_source = data['object_metadata']['metadata'].get('import_source', '')
                        if import_source == 'github_archiver':
                            objects_to_update.append({
                                'file_path': yaml_file,
                                'object_id': obj_id,
                                'title': title,
                                'data': data
                            })
                            print(f"  Found archiver import: {obj_id} - {title}")
                        else:
                            print(f"  WARNING: {obj_id} has '{old_name}' but no archiver metadata")
                            
                except Exception as e:
                    print(f"Error reading {yaml_file}: {e}")
            
            # Update the objects
            for obj_info in objects_to_update:
                try:
                    data = obj_info['data']
                    
                    # Update author name
                    data['object_metadata']['author'] = new_name
                    
                    # Add consolidation timestamp
                    current_time = time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
                    data['object_metadata']['metadata']['last_author_consolidation'] = current_time
                    data['object_metadata']['metadata']['original_archiver_name'] = old_name
                    
                    # Write back to file
                    with open(obj_info['file_path'], 'w', encoding='utf-8') as f:
                        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
                    
                    print(f"  ✓ Updated {obj_info['object_id']}: {obj_info['title']}")
                    self.updated_objects.append(obj_info['object_id'])
                    
                except Exception as e:
                    print(f"  ✗ Error updating {obj_info['object_id']}: {e}")
        
        print(f"\n✅ CONSOLIDATION COMPLETE:")
        print(f"   Objects updated: {len(self.updated_objects)}")
        print(f"   Updated objects: {', '.join(self.updated_objects)}")
        
        if self.updated_objects:
            print(f"\n📝 Next step: Regenerate manifests to consolidate author listings")
        
        return len(self.updated_objects)

def main():
    objects_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects"
    
    consolidator = AuthorConsolidator(objects_dir)
    updated_count = consolidator.consolidate_authors()
    
    return 0 if updated_count > 0 else 1

if __name__ == "__main__":
    exit(main())