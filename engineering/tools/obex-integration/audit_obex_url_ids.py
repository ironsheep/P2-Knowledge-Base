#!/usr/bin/env python3
"""
CRITICAL: Check OBEX URLs for embedded Object IDs vs manifest/filename Object IDs
This is likely where the mismatch is occurring
"""

import os
import yaml
import re
from pathlib import Path

class ObexUrlIdAuditor:
    def __init__(self, objects_dir):
        self.objects_dir = Path(objects_dir)
        self.id_mismatches = []
        
    def audit_obex_url_ids(self):
        """Check if OBEX URLs contain different Object IDs than filenames/manifests"""
        print("CRITICAL AUDIT: OBEX URL Object IDs vs File/Manifest Object IDs")
        print("=" * 80)
        
        total_files = 0
        url_mismatch_count = 0
        no_url_count = 0
        
        for yaml_file in sorted(self.objects_dir.glob("*.yaml")):
            if yaml_file.name == "_template.yaml":
                continue
                
            total_files += 1
            
            # Extract Object ID from filename
            filename_id = yaml_file.stem  # e.g., "4883" from "4883.yaml"
            
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    
                yaml_object_id = data['object_metadata'].get('object_id', '')
                title = data['object_metadata'].get('title', 'NO TITLE')
                obex_url = data['object_metadata']['urls'].get('obex_page', '')
                download_url = data['object_metadata']['urls'].get('download_direct', '')
                
                # Extract Object ID from OBEX URLs
                obex_url_id = None
                download_url_id = None
                
                if obex_url:
                    # Look for Object ID patterns in OBEX page URL
                    # Common patterns: /object-name-1234/, /object-1234/, etc.
                    url_match = re.search(r'(\d{4,5})', obex_url.split('/')[-2] if obex_url.endswith('/') else obex_url.split('/')[-1])
                    if url_match:
                        obex_url_id = url_match.group(1)
                
                if download_url:
                    # Look for Object ID in download URL: obuid=OB1234
                    download_match = re.search(r'obuid=OB(\d{4,5})', download_url)
                    if download_match:
                        download_url_id = download_match.group(1)
                
                # Check for inconsistencies
                authoritative_url_id = download_url_id or obex_url_id  # Download URL is more authoritative
                
                if not obex_url and not download_url:
                    no_url_count += 1
                    print(f"⚠️ {filename_id}: No URLs available")
                elif not authoritative_url_id:
                    print(f"⚠️ {filename_id}: Could not extract Object ID from URLs")
                elif authoritative_url_id != filename_id or authoritative_url_id != yaml_object_id:
                    url_mismatch_count += 1
                    mismatch = {
                        'filename': yaml_file.name,
                        'filename_id': filename_id,
                        'yaml_object_id': yaml_object_id,
                        'obex_url_id': obex_url_id,
                        'download_url_id': download_url_id,
                        'authoritative_url_id': authoritative_url_id,
                        'title': title,
                        'obex_url': obex_url,
                        'download_url': download_url,
                        'file_path': yaml_file
                    }
                    self.id_mismatches.append(mismatch)
                    
                    print(f"❌ MISMATCH: {yaml_file.name}")
                    print(f"   Filename ID: {filename_id}")
                    print(f"   YAML Object ID: {yaml_object_id}")
                    print(f"   OBEX URL ID: {obex_url_id}")
                    print(f"   Download URL ID: {download_url_id}")
                    print(f"   Authoritative URL ID: {authoritative_url_id}")
                    print(f"   Title: {title}")
                    print(f"   OBEX URL: {obex_url}")
                    print()
                else:
                    print(f"✅ {filename_id}: Consistent Object IDs")
                    
            except Exception as e:
                print(f"❌ ERROR reading {yaml_file}: {e}")
                url_mismatch_count += 1
        
        print(f"\nURL OBJECT ID AUDIT RESULTS:")
        print(f"Total files audited: {total_files}")
        print(f"Files with no URLs: {no_url_count}")
        print(f"URL Object ID mismatches: {url_mismatch_count}")
        print(f"URL consistency: {((total_files - url_mismatch_count)/total_files)*100:.1f}%")
        
        return self.id_mismatches
    
    def generate_correction_plan(self):
        """Generate plan to correct Object ID mismatches"""
        if not self.id_mismatches:
            print("\n✅ All OBEX URL Object IDs are consistent!")
            return []
        
        print(f"\nCORRECTION PLAN FOR {len(self.id_mismatches)} MISMATCHES:")
        print("=" * 60)
        
        corrections = []
        
        for mismatch in self.id_mismatches:
            correct_id = mismatch['authoritative_url_id']
            filename_id = mismatch['filename_id']
            yaml_id = mismatch['yaml_object_id']
            
            correction = {
                'current_filename': mismatch['filename'],
                'correct_filename': f"{correct_id}.yaml",
                'current_yaml_id': yaml_id,
                'correct_yaml_id': correct_id,
                'needs_file_rename': correct_id != filename_id,
                'needs_yaml_update': correct_id != yaml_id,
                'title': mismatch['title'],
                'file_path': mismatch['file_path']
            }
            
            corrections.append(correction)
            
            print(f"🔧 {mismatch['filename']}:")
            print(f"   Title: {mismatch['title']}")
            print(f"   Correct Object ID: {correct_id}")
            
            if correction['needs_file_rename']:
                print(f"   📁 Rename file: {mismatch['filename']} → {correct_id}.yaml")
            
            if correction['needs_yaml_update']:
                print(f"   📝 Update YAML object_id: '{yaml_id}' → '{correct_id}'")
            
            print()
        
        return corrections

def main():
    objects_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects"
    
    auditor = ObexUrlIdAuditor(objects_dir)
    
    # Perform URL Object ID audit
    mismatches = auditor.audit_obex_url_ids()
    
    # Generate correction plan
    corrections = auditor.generate_correction_plan()
    
    if corrections:
        print(f"🚨 CRITICAL: Found {len(corrections)} Object ID inconsistencies!")
        print("These need to be corrected before the OBEX integration can be published.")
    
    return corrections

if __name__ == "__main__":
    main()