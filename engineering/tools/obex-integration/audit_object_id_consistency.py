#!/usr/bin/env python3
"""
CRITICAL: Audit Object ID vs filename consistency across all YAML files
"""

import os
import yaml
from pathlib import Path
import re

class ObjectIdAuditor:
    def __init__(self, objects_dir):
        self.objects_dir = Path(objects_dir)
        self.mismatches = []
        self.correct_mappings = []
        
    def audit_all_object_files(self):
        """Audit every YAML file for Object ID vs filename consistency"""
        print("CRITICAL AUDIT: Object ID vs Filename Consistency")
        print("=" * 80)
        
        total_files = 0
        mismatch_count = 0
        
        for yaml_file in sorted(self.objects_dir.glob("*.yaml")):
            if yaml_file.name == "_template.yaml":
                continue
                
            total_files += 1
            
            # Extract expected Object ID from filename
            filename_id = yaml_file.stem  # e.g., "4883" from "4883.yaml"
            
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    
                # Extract actual Object ID from YAML content
                yaml_object_id = data['object_metadata'].get('object_id', '')
                title = data['object_metadata'].get('title', 'NO TITLE')
                obex_url = data['object_metadata']['urls'].get('obex_page', '')
                download_url = data['object_metadata']['urls'].get('download_direct', '')
                
                # Check for mismatch
                if filename_id != yaml_object_id:
                    mismatch_count += 1
                    self.mismatches.append({
                        'filename': yaml_file.name,
                        'filename_id': filename_id,
                        'yaml_object_id': yaml_object_id,
                        'title': title,
                        'obex_url': obex_url,
                        'download_url': download_url,
                        'file_path': yaml_file
                    })
                    
                    print(f"❌ MISMATCH: {yaml_file.name}")
                    print(f"   Filename suggests: {filename_id}")
                    print(f"   YAML contains: {yaml_object_id}")
                    print(f"   Title: {title}")
                    print(f"   OBEX URL: {obex_url}")
                    print()
                else:
                    self.correct_mappings.append({
                        'object_id': filename_id,
                        'title': title,
                        'file_path': yaml_file
                    })
                    
            except Exception as e:
                print(f"❌ ERROR reading {yaml_file}: {e}")
                mismatch_count += 1
        
        print(f"AUDIT RESULTS:")
        print(f"Total files audited: {total_files}")
        print(f"Correct mappings: {len(self.correct_mappings)}")
        print(f"MISMATCHES FOUND: {mismatch_count}")
        print(f"Data integrity: {(len(self.correct_mappings)/total_files)*100:.1f}%")
        
        return self.mismatches, self.correct_mappings
    
    def analyze_mismatch_patterns(self):
        """Analyze patterns in the mismatches to understand root cause"""
        if not self.mismatches:
            return
            
        print(f"\nMISMATCH PATTERN ANALYSIS:")
        print("-" * 40)
        
        # Check if OBEX URLs contain the correct Object ID
        url_pattern_matches = 0
        for mismatch in self.mismatches:
            obex_url = mismatch['obex_url']
            download_url = mismatch['download_url']
            
            # Check if URLs contain object ID clues
            url_id_match = None
            if obex_url:
                # Look for object ID patterns in OBEX URL
                url_match = re.search(r'/obex/[^/]*?(\d{4,5})', obex_url)
                if url_match:
                    url_id_match = url_match.group(1)
            
            if download_url:
                # Look for object ID in download URL
                download_match = re.search(r'obuid=OB(\d{4,5})', download_url)
                if download_match:
                    download_id = download_match.group(1)
                    if url_id_match is None:
                        url_id_match = download_id
            
            if url_id_match:
                url_pattern_matches += 1
                print(f"📍 {mismatch['filename']}: URLs suggest Object ID {url_id_match}")
                
                # Update mismatch with URL-suggested ID
                mismatch['url_suggested_id'] = url_id_match
        
        print(f"URLs provide ID clues for {url_pattern_matches}/{len(self.mismatches)} mismatches")
    
    def determine_correct_object_ids(self):
        """Determine the authoritative Object ID for each mismatch"""
        print(f"\nDETERMINING CORRECT OBJECT IDs:")
        print("-" * 40)
        
        corrections = []
        
        for mismatch in self.mismatches:
            filename_id = mismatch['filename_id']
            yaml_id = mismatch['yaml_object_id']
            url_id = mismatch.get('url_suggested_id', None)
            
            # Priority: URL > Filename > YAML content
            # URLs are most authoritative since they come from OBEX itself
            
            if url_id and url_id != filename_id and url_id != yaml_id:
                # URL suggests different ID - this is most authoritative
                correct_id = url_id
                action = f"URL-authoritative: {correct_id}"
            elif url_id and url_id == filename_id:
                # URL confirms filename
                correct_id = filename_id
                action = f"URL confirms filename: {correct_id}"
            elif url_id and url_id == yaml_id:
                # URL confirms YAML
                correct_id = yaml_id
                action = f"URL confirms YAML: {correct_id}"
            elif filename_id.isdigit() and len(filename_id) >= 4:
                # Filename looks like valid Object ID
                correct_id = filename_id
                action = f"Filename appears valid: {correct_id}"
            elif yaml_id.isdigit() and len(yaml_id) >= 4:
                # YAML ID looks valid
                correct_id = yaml_id
                action = f"YAML ID appears valid: {correct_id}"
            else:
                # Can't determine - flag for manual review
                correct_id = None
                action = "MANUAL REVIEW REQUIRED"
            
            corrections.append({
                'filename': mismatch['filename'],
                'current_filename_id': filename_id,
                'current_yaml_id': yaml_id,
                'url_suggested_id': url_id,
                'correct_id': correct_id,
                'action': action,
                'file_path': mismatch['file_path'],
                'title': mismatch['title']
            })
            
            print(f"🔍 {mismatch['filename']}: {action}")
        
        return corrections
    
    def generate_correction_report(self, corrections):
        """Generate detailed correction report"""
        print(f"\nCORRECTION PLAN SUMMARY:")
        print("=" * 80)
        
        needs_filename_change = []
        needs_yaml_change = []
        needs_manual_review = []
        
        for correction in corrections:
            if correction['correct_id'] is None:
                needs_manual_review.append(correction)
            elif correction['correct_id'] != correction['current_filename_id']:
                needs_filename_change.append(correction)
            elif correction['correct_id'] != correction['current_yaml_id']:
                needs_yaml_change.append(correction)
        
        print(f"Files needing filename changes: {len(needs_filename_change)}")
        print(f"Files needing YAML content changes: {len(needs_yaml_change)}")
        print(f"Files needing manual review: {len(needs_manual_review)}")
        
        if needs_filename_change:
            print(f"\nFILENAME CHANGES REQUIRED:")
            for correction in needs_filename_change:
                old_name = correction['filename']
                new_name = f"{correction['correct_id']}.yaml"
                print(f"  {old_name} → {new_name}")
        
        if needs_yaml_change:
            print(f"\nYAML CONTENT CHANGES REQUIRED:")
            for correction in needs_yaml_change:
                print(f"  {correction['filename']}: object_id '{correction['current_yaml_id']}' → '{correction['correct_id']}'")
        
        if needs_manual_review:
            print(f"\nMANUAL REVIEW REQUIRED:")
            for correction in needs_manual_review:
                print(f"  {correction['filename']}: Cannot determine correct Object ID")
                print(f"    Title: {correction['title']}")
        
        return {
            'filename_changes': needs_filename_change,
            'yaml_changes': needs_yaml_change,
            'manual_review': needs_manual_review
        }

def main():
    objects_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects"
    
    auditor = ObjectIdAuditor(objects_dir)
    
    # Perform comprehensive audit
    mismatches, correct_mappings = auditor.audit_all_object_files()
    
    if mismatches:
        print(f"\n🚨 CRITICAL DATA INTEGRITY ISSUE DETECTED!")
        print(f"Found {len(mismatches)} Object ID mismatches out of {len(mismatches) + len(correct_mappings)} total files")
        
        # Analyze patterns
        auditor.analyze_mismatch_patterns()
        
        # Determine corrections
        corrections = auditor.determine_correct_object_ids()
        
        # Generate correction plan
        correction_plan = auditor.generate_correction_report(corrections)
        
        return corrections, correction_plan
    else:
        print(f"\n✅ All Object IDs are consistent!")
        return [], {}

if __name__ == "__main__":
    main()