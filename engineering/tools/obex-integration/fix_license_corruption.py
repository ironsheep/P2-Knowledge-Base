#!/usr/bin/env python3
"""
Fix corrupted license fields containing extraction artifacts
"""

import os
import yaml
import re
from pathlib import Path
import time

class LicenseCorruptionFixer:
    def __init__(self, objects_dir):
        self.objects_dir = Path(objects_dir)
        self.corrupted_licenses = []
        
    def find_corrupted_licenses(self):
        """Find all objects with corrupted license fields"""
        print("Scanning for license field corruption...")
        
        corruption_patterns = [
            r'Content\s*$',  # Extraction artifact ending
            r'\\n',  # Escaped newlines
            r'OtherContent\s',  # License extraction artifacts
            r'MITContent\s',  # License extraction artifacts
            r'Verified with',  # Verification text
            r'Get pseudo',  # Description leakage
            r'Provides P',  # Description leakage
            r'Interface for',  # Description leakage
            r'This object',  # Description leakage
        ]
        
        for yaml_file in sorted(self.objects_dir.glob("*.yaml")):
            if yaml_file.name == "_template.yaml":
                continue
                
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    
                obj_id = data['object_metadata']['object_id']
                title = data['object_metadata']['title']
                license_info = data['object_metadata']['metadata'].get('license', '')
                
                if not license_info:
                    continue
                
                license_str = str(license_info)
                
                # Check for corruption patterns
                is_corrupted = False
                corruption_types = []
                
                for pattern in corruption_patterns:
                    if re.search(pattern, license_str, re.IGNORECASE | re.MULTILINE):
                        is_corrupted = True
                        corruption_types.append(pattern[:20] + '...')
                
                if is_corrupted:
                    # Extract clean license
                    clean_license = self.extract_clean_license(license_str)
                    
                    corruption = {
                        'object_id': obj_id,
                        'title': title,
                        'file_path': yaml_file,
                        'corrupted_license': license_str,
                        'clean_license': clean_license,
                        'corruption_types': corruption_types
                    }
                    self.corrupted_licenses.append(corruption)
                    
                    print(f"❌ {obj_id}: License corruption detected")
                    print(f"   Title: {title}")
                    print(f"   Corruption types: {', '.join(corruption_types)}")
                    print(f"   Current: {license_str[:80]}...")
                    print(f"   Clean: {clean_license}")
                    print()
                    
            except Exception as e:
                print(f"Error processing {yaml_file}: {e}")
        
        print(f"Found {len(self.corrupted_licenses)} objects with license corruption")
        return self.corrupted_licenses
    
    def extract_clean_license(self, license_str):
        """Extract clean license from corrupted field"""
        if not license_str:
            return "Other"
        
        # Remove obvious corruption artifacts
        clean_license = license_str
        
        # Remove newline artifacts
        clean_license = re.sub(r'\\n', ' ', clean_license)
        clean_license = re.sub(r'\\r', ' ', clean_license)
        
        # Extract license type from common patterns
        license_patterns = {
            r'MIT': 'MIT',
            r'GPL': 'GPL',
            r'BSD': 'BSD',
            r'Apache': 'Apache',
            r'Public Domain': 'Public Domain',
            r'Creative Commons': 'Creative Commons',
            r'LGPL': 'LGPL',
        }
        
        for pattern, license_type in license_patterns.items():
            if re.search(pattern, clean_license, re.IGNORECASE):
                return license_type
        
        # Look for license at the start before corruption
        first_word = clean_license.split()[0] if clean_license.split() else ''
        if first_word in ['MIT', 'GPL', 'BSD', 'Apache', 'Other', 'MITContent', 'OtherContent']:
            if first_word.endswith('Content'):
                return first_word[:-7]  # Remove 'Content' suffix
            return first_word
        
        # Default fallback
        return "Other"
    
    def fix_corrupted_licenses(self):
        """Fix all identified license corruption issues"""
        if not self.corrupted_licenses:
            print("No license corruption to fix.")
            return 0
        
        print(f"Fixing {len(self.corrupted_licenses)} objects with license corruption...")
        
        fixed_count = 0
        for corruption in self.corrupted_licenses:
            try:
                with open(corruption['file_path'], 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                # Update license field
                old_license = data['object_metadata']['metadata']['license']
                data['object_metadata']['metadata']['license'] = corruption['clean_license']
                
                # Update metadata timestamp
                current_time = time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
                data['object_metadata']['metadata']['last_license_corruption_fix'] = current_time
                
                # Write back to file
                with open(corruption['file_path'], 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, sort_keys=False)
                
                print(f"✓ Fixed {corruption['object_id']}: {corruption['title']}")
                print(f"   Old: {str(old_license)[:80]}...")
                print(f"   New: {corruption['clean_license']}")
                print()
                
                fixed_count += 1
                
            except Exception as e:
                print(f"✗ Error fixing {corruption['object_id']}: {e}")
        
        print(f"✓ Fixed {fixed_count}/{len(self.corrupted_licenses)} license corruption issues")
        return fixed_count

def main():
    objects_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects"
    
    fixer = LicenseCorruptionFixer(objects_dir)
    
    print("LICENSE CORRUPTION ANALYSIS AND FIX")
    print("=" * 70)
    
    # Find all corruption issues
    corrupted = fixer.find_corrupted_licenses()
    
    if corrupted:
        print(f"\n🔧 FIXING LICENSE CORRUPTION ISSUES:")
        print("-" * 50)
        
        # Fix the issues
        fixed_count = fixer.fix_corrupted_licenses()
        
        print(f"\n✅ LICENSE CORRUPTION FIX COMPLETE:")
        print(f"   Corrupted licenses found: {len(corrupted)}")
        print(f"   Licenses fixed: {fixed_count}")
    else:
        print("\n✅ No license corruption found!")

if __name__ == "__main__":
    main()