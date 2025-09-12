#!/usr/bin/env python3
"""
Re-extract authors for objects that had corrupted author names
"""

import os
import yaml
import re
import requests
import time
from pathlib import Path
from bs4 import BeautifulSoup

class AuthorReExtractor:
    def __init__(self, objects_dir):
        self.objects_dir = Path(objects_dir)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_empty_author_objects(self):
        """Get objects with empty author fields"""
        empty_author_objects = []
        
        for yaml_file in self.objects_dir.glob("*.yaml"):
            if yaml_file.name == "_template.yaml":
                continue
                
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    
                obj_id = data['object_metadata']['object_id']
                title = data['object_metadata']['title']
                author = data['object_metadata'].get('author', '').strip()
                obex_url = data['object_metadata']['urls'].get('obex_page', '')
                
                if not author or author == '':
                    empty_author_objects.append({
                        'object_id': obj_id,
                        'title': title,
                        'obex_url': obex_url,
                        'yaml_file': yaml_file
                    })
                    
            except Exception as e:
                print(f"Error processing {yaml_file}: {e}")
        
        return empty_author_objects
    
    def extract_author_from_page(self, url):
        """Extract author information directly from OBEX page"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            page_text = soup.get_text()
            
            # Enhanced author extraction patterns
            author_patterns = [
                r'Author\s*:?\s*([A-Za-z][A-Za-z\s\.\-_0-9]+?)(?:\s*(?:Content|Language|Microcontroller|Category|Licence|License|\n|<|$))',
                r'By\s+([A-Za-z][A-Za-z\s\.\-_0-9]+?)(?:\s*(?:Content|Language|Microcontroller|Category|\n|<|$))',
                r'Created\s+by\s+([A-Za-z][A-Za-z\s\.\-_0-9]+?)(?:\s*(?:Content|Language|Microcontroller|Category|\n|<|$))',
                r'Submitted\s+by\s+([A-Za-z][A-Za-z\s\.\-_0-9]+?)(?:\s*(?:Content|Language|Microcontroller|Category|\n|<|$))',
                r'Developed\s+by\s+([A-Za-z][A-Za-z\s\.\-_0-9]+?)(?:\s*(?:Content|Language|Microcontroller|Category|\n|<|$))',
                # Specific patterns for common usernames
                r'([A-Za-z]+(?:\d+|[A-Z])[A-Za-z\d]*)\s*(?:Content|Language|Microcontroller|Category)',
            ]
            
            for pattern in author_patterns:
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                for match in matches:
                    author = match.strip()
                    # Clean up common artifacts
                    author = re.sub(r'\s+', ' ', author)
                    
                    # Filter out obvious false positives
                    if (len(author) >= 3 and len(author) <= 50 and 
                        not any(word in author.lower() for word in [
                            'content', 'microcontroller', 'propeller', 
                            'language', 'category', 'licence', 'license',
                            'downloads', 'overview', 'object', 'archive'
                        ]) and
                        # Must contain at least one letter
                        re.search(r'[a-zA-Z]', author) and
                        # Not all uppercase (likely extraction error)
                        not author.isupper()):
                        return author
            
            return None
            
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def re_extract_authors(self):
        """Re-extract authors for empty author objects"""
        empty_objects = self.get_empty_author_objects()
        print(f"Found {len(empty_objects)} objects with empty authors")
        print("Beginning author re-extraction...\n")
        
        findings = []
        failed = []
        
        for i, obj in enumerate(empty_objects):
            print(f"Processing {i+1}/{len(empty_objects)}: Object {obj['object_id']} - {obj['title']}")
            
            if obj['obex_url']:
                author = self.extract_author_from_page(obj['obex_url'])
                if author:
                    findings.append({
                        'object_id': obj['object_id'],
                        'title': obj['title'],
                        'author': author,
                        'yaml_file': obj['yaml_file']
                    })
                    print(f"  ✓ Found author: {author}")
                else:
                    failed.append(obj)
                    print(f"  ✗ No author found")
            else:
                failed.append(obj)
                print(f"  ✗ No OBEX URL available")
            
            # Rate limiting
            time.sleep(1.2)
        
        return findings, failed
    
    def update_yaml_files(self, findings):
        """Update YAML files with discovered authors"""
        print(f"\nUpdating {len(findings)} YAML files with re-extracted authors...\n")
        
        updated = 0
        for finding in findings:
            try:
                with open(finding['yaml_file'], 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                # Update author field
                data['object_metadata']['author'] = finding['author']
                
                # Update metadata
                current_time = time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
                if 'metadata' not in data['object_metadata']:
                    data['object_metadata']['metadata'] = {}
                
                data['object_metadata']['metadata']['last_author_re_extraction'] = current_time
                
                # Write back to file
                with open(finding['yaml_file'], 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, sort_keys=False)
                
                print(f"✓ Updated {finding['object_id']}: {finding['author']}")
                updated += 1
                
            except Exception as e:
                print(f"✗ Error updating {finding['object_id']}: {e}")
        
        return updated

def main():
    objects_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects"
    
    extractor = AuthorReExtractor(objects_dir)
    
    # Re-extract authors
    findings, failed = extractor.re_extract_authors()
    
    print(f"\n" + "="*80)
    print(f"AUTHOR RE-EXTRACTION RESULTS")
    print(f"="*80)
    print(f"Objects needing re-extraction: {len(findings) + len(failed)}")
    print(f"Authors successfully re-extracted: {len(findings)}")
    print(f"Objects still unknown: {len(failed)}")
    print(f"Success rate: {len(findings)/(len(findings) + len(failed))*100:.1f}%" if (len(findings) + len(failed)) > 0 else "N/A")
    
    if findings:
        print("\nRE-EXTRACTED AUTHORS:")
        for finding in sorted(findings, key=lambda x: int(x['object_id'])):
            print(f"  {finding['object_id']}: {finding['title']} → {finding['author']}")
        
        # Update YAML files
        updated = extractor.update_yaml_files(findings)
        print(f"✓ Successfully updated {updated}/{len(findings)} files")
    
    if failed:
        print(f"\nOBJECTS STILL WITHOUT AUTHORS ({len(failed)}):")
        for obj in sorted(failed, key=lambda x: int(x['object_id'])):
            print(f"  {obj['object_id']}: {obj['title']}")

if __name__ == "__main__":
    main()