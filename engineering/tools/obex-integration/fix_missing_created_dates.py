#!/usr/bin/env python3
"""
Fix missing created_date fields by extracting from OBEX pages
"""

import os
import yaml
import re
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

class CreatedDateFixer:
    def __init__(self, objects_dir):
        self.objects_dir = Path(objects_dir)
        self.missing_dates = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
    def find_missing_created_dates(self):
        """Find all objects missing created_date"""
        print("Finding objects with missing created_date...")
        
        for yaml_file in sorted(self.objects_dir.glob("*.yaml")):
            if yaml_file.name == "_template.yaml":
                continue
                
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    
                obj_id = data['object_metadata']['object_id']
                title = data['object_metadata']['title']
                created_date = data['object_metadata']['metadata'].get('created_date', '')
                obex_url = data['object_metadata']['urls'].get('obex_page', '')
                
                if not created_date or created_date == '':
                    self.missing_dates.append({
                        'object_id': obj_id,
                        'title': title,
                        'file_path': yaml_file,
                        'obex_url': obex_url,
                        'data': data
                    })
                    
            except Exception as e:
                print(f"Error processing {yaml_file}: {e}")
        
        print(f"Found {len(self.missing_dates)} objects missing created_date")
        return self.missing_dates
    
    def extract_created_date_from_obex(self, obex_url):
        """Extract created_date from OBEX page"""
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
            
            # Look for creation date patterns
            date_patterns = [
                r'Created[:\\s]*(\d{4}-\d{2}-\d{2}[\\s]+\d{2}:\d{2}:\d{2})',
                r'Date[:\\s]*(\d{4}-\d{2}-\d{2}[\\s]+\d{2}:\d{2}:\d{2})',
                r'(\d{4}-\d{2}-\d{2}[\\s]+\d{2}:\d{2}:\d{2})',
                r'Created[:\\s]*(\d{4}-\d{2}-\d{2})',
                r'Date[:\\s]*(\d{4}-\d{2}-\d{2})',
            ]
            
            for pattern in date_patterns:
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                if matches:
                    # Take the first reasonable looking date
                    date_str = matches[0]
                    # Validate it's a reasonable date (not too old, not in future)
                    try:
                        if ' ' in date_str:
                            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                        else:
                            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                            date_str += ' 12:00:00'  # Add default time
                        
                        # Check if date is reasonable (between 2010 and now)
                        if 2010 <= date_obj.year <= datetime.now().year:
                            return date_str
                    except ValueError:
                        continue
                        
        except Exception as e:
            print(f"Error fetching {obex_url}: {e}")
            
        return None
    
    def fix_missing_dates(self):
        """Fix all missing created_date fields"""
        if not self.missing_dates:
            print("No missing dates to fix.")
            return 0
            
        print(f"\\nExtracting created_date from {len(self.missing_dates)} OBEX pages...")
        print("This will take several minutes due to rate limiting...")
        
        fixed_count = 0
        failed_count = 0
        
        for i, missing in enumerate(self.missing_dates, 1):
            print(f"\\n[{i}/{len(self.missing_dates)}] {missing['object_id']}: {missing['title']}")
            
            # Extract date from OBEX page
            created_date = self.extract_created_date_from_obex(missing['obex_url'])
            
            if created_date:
                try:
                    # Update the YAML data
                    data = missing['data']
                    data['object_metadata']['metadata']['created_date'] = created_date
                    
                    # Add extraction timestamp
                    current_time = time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
                    data['object_metadata']['metadata']['last_created_date_fix'] = current_time
                    
                    # Write back to file
                    with open(missing['file_path'], 'w', encoding='utf-8') as f:
                        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
                    
                    print(f"   ✓ Extracted date: {created_date}")
                    fixed_count += 1
                    
                except Exception as e:
                    print(f"   ✗ Error updating file: {e}")
                    failed_count += 1
            else:
                print(f"   ❌ Could not extract date from: {missing['obex_url']}")
                failed_count += 1
        
        print(f"\\n✅ CREATED DATE FIX COMPLETE:")
        print(f"   Dates fixed: {fixed_count}")
        print(f"   Failed extractions: {failed_count}")
        print(f"   Success rate: {(fixed_count / len(self.missing_dates) * 100):.1f}%")
        
        return fixed_count

def main():
    objects_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects"
    
    fixer = CreatedDateFixer(objects_dir)
    
    print("MISSING CREATED DATE EXTRACTION FIX")
    print("=" * 70)
    
    # Find missing dates
    missing = fixer.find_missing_created_dates()
    
    if missing:
        print(f"\\n🔧 FIXING MISSING CREATED DATES:")
        print("-" * 50)
        
        # Ask user before proceeding (this will take a while)
        proceed = input(f"\\nThis will extract dates from {len(missing)} OBEX pages (~{len(missing) * 1.5:.0f} minutes).\\nProceed? (y/N): ")
        
        if proceed.lower() in ['y', 'yes']:
            fixed_count = fixer.fix_missing_dates()
            return len(missing) - fixed_count  # Return remaining issues
        else:
            print("Cancelled by user.")
            return len(missing)
    else:
        print("\\n✅ No missing created_date fields found!")
        return 0

if __name__ == "__main__":
    exit(main())