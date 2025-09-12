#!/usr/bin/env python3
"""
Analyze extraction problems causing empty created_date fields
"""

import os
import yaml
import re
from pathlib import Path
from collections import defaultdict

class CreatedDateAnalyzer:
    def __init__(self, objects_dir):
        self.objects_dir = Path(objects_dir)
        self.empty_dates = []
        self.valid_dates = []
        self.stats = defaultdict(int)
        
    def analyze_created_dates(self):
        """Analyze created_date extraction across all objects"""
        print("CREATED DATE EXTRACTION ANALYSIS")
        print("=" * 70)
        
        for yaml_file in sorted(self.objects_dir.glob("*.yaml")):
            if yaml_file.name == "_template.yaml":
                continue
                
            self.stats['total_objects'] += 1
            
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    
                obj_id = data['object_metadata']['object_id']
                title = data['object_metadata']['title']
                created_date = data['object_metadata']['metadata'].get('created_date', '')
                
                if not created_date or created_date == '':
                    self.empty_dates.append({
                        'object_id': obj_id,
                        'title': title,
                        'file_path': yaml_file,
                        'created_date': created_date
                    })
                    self.stats['empty_dates'] += 1
                else:
                    self.valid_dates.append({
                        'object_id': obj_id,
                        'title': title,
                        'created_date': created_date
                    })
                    self.stats['valid_dates'] += 1
                    
            except Exception as e:
                print(f"Error processing {yaml_file}: {e}")
                self.stats['parse_errors'] += 1
        
        self.report_findings()
        return self.empty_dates, self.valid_dates
    
    def report_findings(self):
        """Report findings on created_date extraction"""
        print(f"📊 CREATED DATE ANALYSIS RESULTS:")
        print(f"   Total objects: {self.stats['total_objects']}")
        print(f"   Valid dates: {self.stats['valid_dates']}")
        print(f"   Empty dates: {self.stats['empty_dates']}")
        print(f"   Parse errors: {self.stats['parse_errors']}")
        print()
        
        if self.empty_dates:
            print(f"🔍 OBJECTS WITH EMPTY CREATED DATES ({len(self.empty_dates)}):")
            for item in self.empty_dates:
                print(f"   ❌ {item['object_id']}: {item['title']}")
            print()
        
        if self.valid_dates:
            print(f"✅ SAMPLE VALID DATES:")
            for item in self.valid_dates[:10]:  # Show first 10
                print(f"   ✓ {item['object_id']}: {item['created_date']}")
            if len(self.valid_dates) > 10:
                print(f"   ... and {len(self.valid_dates) - 10} more")
            print()
        
        # Calculate percentage
        if self.stats['total_objects'] > 0:
            empty_percentage = (self.stats['empty_dates'] / self.stats['total_objects']) * 100
            print(f"📈 EXTRACTION SUCCESS RATE:")
            print(f"   Empty dates: {empty_percentage:.1f}%")
            print(f"   Valid dates: {100 - empty_percentage:.1f}%")
        
        if self.stats['empty_dates'] > 0:
            print(f"\\n⚠️  EXTRACTION PROBLEM IDENTIFIED:")
            print(f"   {self.stats['empty_dates']} objects missing created_date")
            print(f"   This suggests an issue in the OBEX page extraction process")
            print(f"   The created_date field extraction pattern may need improvement")

def main():
    objects_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects"
    
    analyzer = CreatedDateAnalyzer(objects_dir)
    empty_dates, valid_dates = analyzer.analyze_created_dates()
    
    return len(empty_dates)

if __name__ == "__main__":
    exit(main())