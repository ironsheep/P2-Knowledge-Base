#!/usr/bin/env python3
"""
Fix objects imported by GitHub archiver - extract real authors and add archiver metadata
"""

import os
import yaml
import re
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import time

class ArchiverImportFixer:
    def __init__(self, objects_dir):
        self.objects_dir = Path(objects_dir)
        self.archiver_objects = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
    def find_archiver_imports(self):
        """Find all objects with 'Restricted' author that might be archiver imports"""
        print("Finding potential GitHub archiver imports...")
        
        for yaml_file in sorted(self.objects_dir.glob("*.yaml")):
            if yaml_file.name == "_template.yaml":
                continue
                
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    
                obj_id = data['object_metadata']['object_id']
                title = data['object_metadata']['title']
                author = data['object_metadata'].get('author', '')
                obex_url = data['object_metadata']['urls'].get('obex_page', '')
                
                # Look for "Restricted" authors - likely archiver imports
                if author == 'Restricted':
                    self.archiver_objects.append({
                        'object_id': obj_id,
                        'title': title,
                        'file_path': yaml_file,
                        'obex_url': obex_url,
                        'data': data
                    })
                    
            except Exception as e:
                print(f"Error processing {yaml_file}: {e}")
        
        print(f"Found {len(self.archiver_objects)} 'Restricted' author objects to check")
        return self.archiver_objects
    
    def extract_archiver_info(self, obex_url, obj_id):
        """Extract archiver import information from OBEX page"""
        if not obex_url:
            return None
            
        try:
            # Rate limiting
            time.sleep(1.2)
            
            response = self.session.get(obex_url, timeout=30)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            page_text = soup.get_text()
            
            # Look for archiver pattern: "Author : phonoclese | added by Archiver"
            archiver_match = re.search(r'Author\s*:\s*([^|]+?)\s*\|\s*added\s+by\s+Archiver', page_text, re.IGNORECASE)
            
            if archiver_match:
                real_author = archiver_match.group(1).strip()
                archiver_action = "archiver_import"
                
                # Extract archiver date: "Archiver / November 16, 2023"
                archiver_date_match = re.search(r'Archiver\s*/\s*([A-Za-z]+\s+\d{1,2},\s+\d{4})', page_text)
                archiver_date = None
                if archiver_date_match:
                    # Convert to YYYY-MM-DD format
                    date_str = archiver_date_match.group(1)
                    try:
                        from datetime import datetime
                        parsed_date = datetime.strptime(date_str, '%B %d, %Y')
                        archiver_date = parsed_date.strftime('%Y-%m-%d')
                    except ValueError:
                        pass
                
                # Object creation date should already be extracted, but verify
                object_date_match = re.search(rf'Object\s+ID\s*:\s*{obj_id}\s*\((\d{{4}}-\d{{2}}-\d{{2}})\)', page_text)
                object_date = None
                if object_date_match:
                    object_date = object_date_match.group(1) + ' 12:00:00'
                
                return {
                    'real_author': real_author,
                    'archiver_action': archiver_action,
                    'archiver_date': archiver_date,
                    'object_date': object_date,
                    'is_archiver_import': True
                }
                
        except Exception as e:
            print(f"Error fetching {obex_url}: {e}")
            
        return None
    
    def fix_archiver_imports(self):
        """Fix all identified archiver import objects"""
        if not self.archiver_objects:
            print("No archiver imports to fix.")
            return 0
            
        print(f"\nAnalyzing {len(self.archiver_objects)} 'Restricted' author objects for archiver pattern...")
        
        fixed_count = 0
        failed_count = 0
        not_archiver_count = 0
        
        for i, obj_info in enumerate(self.archiver_objects, 1):
            print(f"\n[{i}/{len(self.archiver_objects)}] {obj_info['object_id']}: {obj_info['title']}")
            
            # Extract archiver information
            archiver_info = self.extract_archiver_info(obj_info['obex_url'], obj_info['object_id'])
            
            if archiver_info and archiver_info['is_archiver_import']:
                try:
                    # Update the YAML data
                    data = obj_info['data']
                    
                    # Update author to real author
                    data['object_metadata']['author'] = archiver_info['real_author']
                    
                    # Add archiver metadata
                    if 'metadata' not in data['object_metadata']:
                        data['object_metadata']['metadata'] = {}
                    
                    data['object_metadata']['metadata']['import_source'] = 'github_archiver'
                    data['object_metadata']['metadata']['original_platform'] = 'github'
                    
                    if archiver_info['archiver_date']:
                        data['object_metadata']['metadata']['archiver_date'] = archiver_info['archiver_date']
                    
                    # Update object date if we found one and it's missing
                    if archiver_info['object_date'] and not data['object_metadata']['metadata'].get('created_date'):
                        data['object_metadata']['metadata']['created_date'] = archiver_info['object_date']
                    
                    # Add timestamp
                    current_time = time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
                    data['object_metadata']['metadata']['last_archiver_fix'] = current_time
                    
                    # Write back to file
                    with open(obj_info['file_path'], 'w', encoding='utf-8') as f:
                        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
                    
                    print(f"   ✓ Fixed archiver import:")
                    print(f"     Real author: {archiver_info['real_author']}")
                    print(f"     Archiver date: {archiver_info['archiver_date']}")
                    print(f"     Object date: {archiver_info['object_date']}")
                    fixed_count += 1
                    
                except Exception as e:
                    print(f"   ✗ Error updating file: {e}")
                    failed_count += 1
            else:
                print(f"   ℹ️  Not an archiver import - keeping 'Restricted' author")
                not_archiver_count += 1
        
        print(f"\n✅ ARCHIVER IMPORT FIX COMPLETE:")
        print(f"   Archiver imports fixed: {fixed_count}")
        print(f"   Not archiver imports: {not_archiver_count}")
        print(f"   Failed fixes: {failed_count}")
        if len(self.archiver_objects) > 0:
            print(f"   Success rate: {(fixed_count / len(self.archiver_objects) * 100):.1f}%")
        
        return fixed_count

def main():
    objects_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects"
    
    fixer = ArchiverImportFixer(objects_dir)
    
    print("GITHUB ARCHIVER IMPORT ATTRIBUTION FIX")
    print("=" * 70)
    
    # Find potential archiver imports
    archiver_objects = fixer.find_archiver_imports()
    
    if archiver_objects:
        print(f"\n🔧 ANALYZING ARCHIVER IMPORTS:")
        print("-" * 50)
        
        fixed_count = fixer.fix_archiver_imports()
        
        if fixed_count > 0:
            print(f"\n📝 Next step: Regenerate manifests to reflect proper attribution")
        
        return len(archiver_objects) - fixed_count  # Return remaining issues
    else:
        print("\n✅ No 'Restricted' author objects found!")
        return 0

if __name__ == "__main__":
    exit(main())