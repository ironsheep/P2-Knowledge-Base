#!/usr/bin/env python3
"""
Comprehensive sanity check on all YAML fields for corruption, artifacts, and data quality issues
"""

import os
import yaml
import re
from pathlib import Path
from collections import defaultdict

class ComprehensiveYamlChecker:
    def __init__(self, objects_dir):
        self.objects_dir = Path(objects_dir)
        self.issues = defaultdict(list)
        self.stats = defaultdict(int)
        
    def check_all_fields(self):
        """Perform comprehensive sanity check on all YAML fields"""
        print("COMPREHENSIVE YAML FIELD SANITY CHECK")
        print("=" * 70)
        
        corruption_patterns = [
            # HTML and extraction artifacts
            r'<[^>]*>',  # HTML tags
            r'&[a-z]+;',  # HTML entities
            r'\\[rn]',  # Escaped newlines
            r'Content\s*:\s*Code',  # Extraction metadata
            r'Author\s*:\s*[^:]+:',  # Malformed author patterns
            r'Microcontroller\s*:\s*Propeller',  # Extraction artifacts
            r'Language\s*:\s*SPIN2',  # Language extraction in wrong field
            r'Category\s*:\s*[A-Z]',  # Category extraction artifacts
            r'Licence?\s*:\s*[A-Z]',  # License extraction artifacts
            r'Object\s+ID\s*:\s*\d+',  # Object ID extraction
            r'Downloads?\s*:', # Download references
            r'To\s+view\s+this\s+content',  # JavaScript warnings
            r'follow\s+these\s+instructions',  # Interface instructions
            r'Select\s+all\s+Deselect',  # Interface controls
            r'Name\s+Size\s+Modified',  # File listing headers
        ]
        
        field_specific_issues = {
            'title': ['Untitled', 'Object', 'Test', ''],
            'author': ['Unknown', 'Anonymous', ''],
            'license': ['Unknown', 'Other', ''],
            'description_short': ['', 'No description'],
            'description_full': ['', 'No description'],
            'category': ['', 'other', 'unknown'],
            'file_size': ['0 B', '1 B', '2 B'],  # Suspiciously small files
        }
        
        for yaml_file in sorted(self.objects_dir.glob("*.yaml")):
            if yaml_file.name == "_template.yaml":
                continue
                
            self.stats['total_objects'] += 1
            
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    
                obj_id = data['object_metadata']['object_id']
                self.check_object_structure(obj_id, data, yaml_file)
                self.check_field_corruption(obj_id, data, corruption_patterns, yaml_file)
                self.check_field_quality(obj_id, data, field_specific_issues, yaml_file)
                
            except Exception as e:
                self.issues['parse_errors'].append({
                    'file': yaml_file.name,
                    'error': str(e)
                })
        
        self.report_findings()
        return self.issues
    
    def check_object_structure(self, obj_id, data, yaml_file):
        """Check for structural issues in YAML"""
        required_sections = ['object_metadata', 'object_metadata.functionality', 
                           'object_metadata.technical_details', 'object_metadata.metadata']
        
        for section_path in required_sections:
            current = data
            for key in section_path.split('.'):
                if key not in current:
                    self.issues['missing_sections'].append({
                        'object_id': obj_id,
                        'file': yaml_file.name,
                        'missing_section': section_path
                    })
                    break
                current = current[key]
    
    def check_field_corruption(self, obj_id, data, patterns, yaml_file):
        """Check all text fields for corruption patterns"""
        text_fields = [
            ('title', data['object_metadata'].get('title', '')),
            ('author', data['object_metadata'].get('author', '')),
            ('description_short', data['object_metadata']['functionality'].get('description_short', '')),
            ('description_full', data['object_metadata']['functionality'].get('description_full', '')),
            ('license', data['object_metadata']['metadata'].get('license', '')),
        ]
        
        for field_name, field_value in text_fields:
            if not field_value:
                continue
                
            field_str = str(field_value)
            for pattern in patterns:
                if re.search(pattern, field_str, re.IGNORECASE):
                    self.issues['corruption_detected'].append({
                        'object_id': obj_id,
                        'file': yaml_file.name,
                        'field': field_name,
                        'pattern': pattern[:30] + '...',
                        'value': field_str[:100] + '...' if len(field_str) > 100 else field_str
                    })
    
    def check_field_quality(self, obj_id, data, quality_checks, yaml_file):
        """Check for quality issues in specific fields"""
        
        # Check title quality
        title = data['object_metadata'].get('title', '')
        if not title or len(title) < 3 or title in quality_checks['title']:
            self.issues['poor_quality_title'].append({
                'object_id': obj_id,
                'file': yaml_file.name,
                'title': title
            })
        
        # Check author quality
        author = data['object_metadata'].get('author', '')
        if not author or author in quality_checks['author']:
            self.issues['poor_quality_author'].append({
                'object_id': obj_id,
                'file': yaml_file.name,
                'author': author
            })
        
        # Check description quality
        desc_short = data['object_metadata']['functionality'].get('description_short', '')
        desc_full = data['object_metadata']['functionality'].get('description_full', '')
        
        if not desc_short and not desc_full:
            self.issues['missing_descriptions'].append({
                'object_id': obj_id,
                'file': yaml_file.name
            })
        elif len(desc_short) < 10 and len(desc_full) < 10:
            self.issues['very_short_descriptions'].append({
                'object_id': obj_id,
                'file': yaml_file.name,
                'desc_short': desc_short,
                'desc_full': desc_full
            })
        
        # Check file size quality
        file_size = data['object_metadata']['technical_details'].get('file_size', '')
        if file_size in quality_checks['file_size']:
            self.issues['suspicious_file_size'].append({
                'object_id': obj_id,
                'file': yaml_file.name,
                'file_size': file_size
            })
        
        # Check license quality
        license_info = data['object_metadata']['metadata'].get('license', '')
        if isinstance(license_info, str):
            if not license_info or license_info in quality_checks['license']:
                self.issues['poor_quality_license'].append({
                    'object_id': obj_id,
                    'file': yaml_file.name,
                    'license': license_info
                })
            elif '\\n' in license_info or 'Content' in license_info:
                self.issues['corrupted_license'].append({
                    'object_id': obj_id,
                    'file': yaml_file.name,
                    'license': license_info[:100] + '...' if len(license_info) > 100 else license_info
                })
        
        # Check category quality
        category = data['object_metadata']['functionality'].get('category', '')
        if not category or category in quality_checks['category']:
            self.issues['poor_quality_category'].append({
                'object_id': obj_id,
                'file': yaml_file.name,
                'category': category
            })
    
    def report_findings(self):
        """Generate comprehensive report of all findings"""
        print(f"\\n📊 SANITY CHECK RESULTS:")
        print(f"   Total objects checked: {self.stats['total_objects']}")
        print()
        
        # Report each issue category
        for issue_type, issue_list in self.issues.items():
            if issue_list:
                print(f"🔍 {issue_type.replace('_', ' ').title()}: {len(issue_list)}")
                for issue in issue_list[:5]:  # Show first 5 examples
                    if issue_type == 'corruption_detected':
                        print(f"   ❌ {issue['object_id']}: {issue['field']} - Pattern: {issue['pattern']}")
                        print(f"      Value: {issue['value']}")
                    elif issue_type == 'poor_quality_title':
                        print(f"   ❌ {issue['object_id']}: '{issue['title']}'")
                    elif issue_type == 'poor_quality_author':
                        print(f"   ❌ {issue['object_id']}: '{issue['author']}'")
                    elif issue_type == 'corrupted_license':
                        print(f"   ❌ {issue['object_id']}: '{issue['license']}'")
                    elif issue_type == 'suspicious_file_size':
                        print(f"   ❌ {issue['object_id']}: {issue['file_size']}")
                    else:
                        print(f"   ❌ {issue['object_id']}")
                
                if len(issue_list) > 5:
                    print(f"   ... and {len(issue_list) - 5} more")
                print()
        
        # Summary
        total_issues = sum(len(issue_list) for issue_list in self.issues.values())
        if total_issues == 0:
            print("✅ No significant quality issues found!")
        else:
            print(f"⚠️  Found {total_issues} total issues across {len(self.issues)} categories")

def main():
    objects_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects"
    
    checker = ComprehensiveYamlChecker(objects_dir)
    issues = checker.check_all_fields()
    
    # Return count for automation
    total_issues = sum(len(issue_list) for issue_list in issues.values())
    return total_issues

if __name__ == "__main__":
    exit(main())