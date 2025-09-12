#!/usr/bin/env python3
"""
Analyze unknown author objects for potential author clues in descriptions
"""

import os
import yaml
import re
from pathlib import Path

class UnknownAuthorAnalyzer:
    def __init__(self, objects_dir):
        self.objects_dir = Path(objects_dir)
        self.unknown_objects = []
        self.potential_authors = []
        
        # Common author extraction patterns
        self.author_patterns = [
            (r'(?:by|By|BY)\s+([A-Za-z][A-Za-z\s\.]+?)(?:\s*(?:\(|Content|Microcontroller|Language|\n|<|\||$))', 'by_pattern'),
            (r'(?:from|From|FROM)\s+([A-Za-z][A-Za-z\s\.]+?)(?:\s*(?:\(|Content|Microcontroller|Language|\n|<|\||$))', 'from_pattern'),
            (r'(?:author|Author|AUTHOR|written|Written|created|Created)\s*(?:by|BY)?\s*:?\s*([A-Za-z][A-Za-z\s\.]+?)(?:\s*(?:\(|Content|Microcontroller|Language|\n|<|\||$))', 'author_pattern'),
            (r'(?:developed|Developed|programmed|Programmed)\s*(?:by|BY)\s+([A-Za-z][A-Za-z\s\.]+?)(?:\s*(?:\(|Content|Microcontroller|Language|\n|<|\||$))', 'developed_pattern'),
            (r'(?:thanks|Thanks|THANKS)\s*(?:to|TO)\s+([A-Za-z][A-Za-z\s\.]+?)(?:\s*(?:\(|for|FOR|Content|Microcontroller|Language|\n|<|\||$))', 'thanks_pattern'),
        ]
    
    def load_objects(self):
        """Load all YAML objects and identify those with unknown authors"""
        for yaml_file in self.objects_dir.glob("*.yaml"):
            if yaml_file.name == "_template.yaml":
                continue
                
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    
                obj_id = data['object_metadata']['object_id']
                title = data['object_metadata']['title']
                author = data['object_metadata'].get('author', '').strip()
                
                if not author or author == '':
                    desc_full = data['object_metadata']['functionality'].get('description_full', '')
                    desc_short = data['object_metadata']['functionality'].get('description_short', '')
                    
                    self.unknown_objects.append({
                        'object_id': obj_id,
                        'title': title,
                        'description_full': desc_full,
                        'description_short': desc_short,
                        'file_path': yaml_file
                    })
                    
            except Exception as e:
                print(f"Error processing {yaml_file}: {e}")
    
    def analyze_descriptions(self):
        """Analyze descriptions for potential author names"""
        print(f"Analyzing {len(self.unknown_objects)} objects with unknown authors...\n")
        
        findings = []
        
        for obj in self.unknown_objects:
            obj_findings = {
                'object_id': obj['object_id'],
                'title': obj['title'],
                'potential_authors': [],
                'patterns_found': []
            }
            
            # Check both full and short descriptions
            descriptions = [obj['description_full'], obj['description_short']]
            
            for desc in descriptions:
                if not desc:
                    continue
                    
                # Try each author pattern
                for pattern, pattern_name in self.author_patterns:
                    matches = re.findall(pattern, desc, re.IGNORECASE | re.MULTILINE)
                    for match in matches:
                        # Clean up the match
                        author = match.strip()
                        if len(author) > 2 and len(author) < 50:  # Reasonable length
                            # Remove common false positives
                            if not any(word in author.lower() for word in ['content', 'code', 'microcontroller', 'propeller', 'language', 'category']):
                                obj_findings['potential_authors'].append(author)
                                obj_findings['patterns_found'].append(pattern_name)
            
            if obj_findings['potential_authors']:
                findings.append(obj_findings)
        
        return findings
    
    def generate_report(self, findings):
        """Generate detailed report of findings"""
        print("="*80)
        print("UNKNOWN AUTHOR ANALYSIS REPORT")
        print("="*80)
        print(f"Total objects analyzed: {len(self.unknown_objects)}")
        print(f"Objects with potential author clues: {len(findings)}")
        print(f"Objects still unknown: {len(self.unknown_objects) - len(findings)}")
        print()
        
        if findings:
            print("OBJECTS WITH POTENTIAL AUTHORS:")
            print("-" * 50)
            
            for finding in findings:
                print(f"Object {finding['object_id']}: {finding['title']}")
                for i, author in enumerate(finding['potential_authors']):
                    pattern = finding['patterns_found'][i] if i < len(finding['patterns_found']) else 'unknown'
                    print(f"  → Potential author: '{author}' (via {pattern})")
                print()
        
        # Show objects that still have no clues
        no_clues = [obj for obj in self.unknown_objects if obj['object_id'] not in [f['object_id'] for f in findings]]
        if no_clues:
            print("OBJECTS STILL WITHOUT AUTHOR CLUES:")
            print("-" * 50)
            for obj in no_clues[:10]:  # Show first 10
                print(f"Object {obj['object_id']}: {obj['title']}")
            if len(no_clues) > 10:
                print(f"... and {len(no_clues) - 10} more")
        
        return findings
    
    def sample_descriptions(self, count=5):
        """Show sample descriptions for manual inspection"""
        print("\nSAMPLE DESCRIPTIONS FOR MANUAL INSPECTION:")
        print("-" * 50)
        
        for i, obj in enumerate(self.unknown_objects[:count]):
            print(f"\nObject {obj['object_id']}: {obj['title']}")
            print("Description excerpt:")
            desc = obj['description_full'][:500] + "..." if len(obj['description_full']) > 500 else obj['description_full']
            print(f'"{desc}"')
            print()

def main():
    objects_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects"
    
    analyzer = UnknownAuthorAnalyzer(objects_dir)
    analyzer.load_objects()
    
    print(f"Found {len(analyzer.unknown_objects)} objects with unknown authors")
    
    findings = analyzer.analyze_descriptions()
    analyzer.generate_report(findings)
    analyzer.sample_descriptions()

if __name__ == "__main__":
    main()