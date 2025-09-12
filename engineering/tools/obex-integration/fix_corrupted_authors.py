#!/usr/bin/env python3
"""
Fix corrupted author names that contain HTML/extraction artifacts
"""

import os
import yaml
from pathlib import Path
import re

def fix_corrupted_authors(objects_dir):
    """Fix author names that contain HTML artifacts or extraction errors"""
    objects_dir = Path(objects_dir)
    
    fixes_applied = 0
    corrupted_authors = []
    
    # Common patterns that indicate corruption
    corruption_patterns = [
        r'Archivercontent\s*:\s*Code',
        r'Each Smart Pin To Low-Pass',
        r'Some Over The Ws2812',
        r'Te Data \(Qr Has',
        r'Extension$',
        r'The Arduino Easy',
        r'Others -- Some Of Whom',
        r'The Spin Api Example',
        r'Hundreds Of Regression',
        r'Te Header \(\$Aaaa\)',
        r'Greg Lapolla Which Includes',
        r'Parallax\.Com Or By Mikroe',
        r'^5$',
        r'The Parent Application',
        r'^Applications\.$',
        r'Measuring-Floating-Pi',
        r'Bya Thomas \| Added',
        r'Skipping Spc700 Cycles',
        r'^Tes\.$'
    ]
    
    for yaml_file in objects_dir.glob("*.yaml"):
        if yaml_file.name == "_template.yaml":
            continue
            
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            obj_id = data['object_metadata']['object_id']
            title = data['object_metadata']['title']
            current_author = data['object_metadata'].get('author', '').strip()
            
            # Check if author name looks corrupted
            is_corrupted = False
            for pattern in corruption_patterns:
                if re.search(pattern, current_author, re.IGNORECASE):
                    is_corrupted = True
                    break
            
            # Also check for very long author names (likely extraction artifacts)
            if len(current_author) > 100:
                is_corrupted = True
            
            if is_corrupted:
                corrupted_authors.append({
                    'object_id': obj_id,
                    'title': title,
                    'bad_author': current_author,
                    'yaml_file': yaml_file
                })
                
                print(f"Found corrupted author in {obj_id}: {current_author[:100]}...")
                
                # Clear the corrupted author name
                data['object_metadata']['author'] = ''
                
                # Write back to file
                with open(yaml_file, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, sort_keys=False)
                
                fixes_applied += 1
                
        except Exception as e:
            print(f"Error processing {yaml_file}: {e}")
    
    print(f"\n✓ Fixed {fixes_applied} corrupted author names")
    print(f"✓ Objects now need author re-extraction: {len(corrupted_authors)}")
    
    return corrupted_authors

def main():
    objects_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects"
    
    print("Fixing corrupted author names...")
    corrupted_authors = fix_corrupted_authors(objects_dir)
    
    if corrupted_authors:
        print(f"\nObjects that need author re-extraction:")
        for item in corrupted_authors:
            print(f"  {item['object_id']}: {item['title']}")

if __name__ == "__main__":
    main()