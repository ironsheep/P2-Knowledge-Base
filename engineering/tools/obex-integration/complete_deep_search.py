#!/usr/bin/env python3
"""
Complete deep search for all unknown authors with automatic updates
"""

import os
import yaml
import re
import requests
import time
from pathlib import Path
from bs4 import BeautifulSoup

class CompleteAuthorSearcher:
    def __init__(self, objects_dir):
        self.objects_dir = Path(objects_dir)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_unknown_objects(self):
        """Get list of objects with unknown authors"""
        unknown_objects = []
        
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
                    unknown_objects.append({
                        'object_id': obj_id,
                        'title': title,
                        'obex_url': obex_url,
                        'yaml_file': yaml_file
                    })
                    
            except Exception as e:
                print(f"Error processing {yaml_file}: {e}")
        
        return unknown_objects
    
    def extract_author_from_page(self, url):
        """Extract author information directly from OBEX page"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            page_text = soup.get_text()
            
            # Multiple author extraction patterns - refined based on previous findings
            author_patterns = [
                r'Author\s*:?\s*([A-Za-z][A-Za-z\s\.\-_0-9]+?)(?:\s*(?:Content|Language|Microcontroller|Category|Licence|License|\n|<|$))',
                r'By\s+([A-Za-z][A-Za-z\s\.\-_0-9]+?)(?:\s*(?:Content|Language|Microcontroller|Category|\n|<|$))',
                r'Created\s+by\s+([A-Za-z][A-Za-z\s\.\-_0-9]+?)(?:\s*(?:Content|Language|Microcontroller|Category|\n|<|$))',
                r'Submitted\s+by\s+([A-Za-z][A-Za-z\s\.\-_0-9]+?)(?:\s*(?:Content|Language|Microcontroller|Category|\n|<|$))',
                r'Developed\s+by\s+([A-Za-z][A-Za-z\s\.\-_0-9]+?)(?:\s*(?:Content|Language|Microcontroller|Category|\n|<|$))',
                # Common username patterns from forum/OBEX
                r'([A-Za-z]+(?:\d+|[A-Z])[A-Za-z\d]*)\s*(?:Content|Language|Microcontroller|Category)',  # Handles usernames like "ersmith", "vonszarvas"
            ]
            
            for pattern in author_patterns:
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                for match in matches:
                    author = match.strip()
                    # Clean up common artifacts
                    author = re.sub(r'\s+', ' ', author)  # Multiple spaces to single
                    
                    # Filter out obvious false positives
                    if (len(author) >= 3 and len(author) <= 50 and 
                        not any(word in author.lower() for word in [
                            'content', 'microcontroller', 'propeller', 
                            'language', 'category', 'licence', 'license',
                            'downloads', 'overview', 'object'
                        ]) and
                        # Must contain at least one letter
                        re.search(r'[a-zA-Z]', author)):
                        return author
            
            return None
            
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def search_all_unknowns(self):
        """Search all unknown objects for author information"""
        unknown_objects = self.get_unknown_objects()
        print(f"Found {len(unknown_objects)} objects with unknown authors")
        print("Beginning complete deep author search...\n")
        
        findings = []
        failed = []
        
        for i, obj in enumerate(unknown_objects):
            print(f"Processing {i+1}/{len(unknown_objects)}: Object {obj['object_id']} - {obj['title']}")
            
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
        print(f"\nUpdating {len(findings)} YAML files with discovered authors...\n")
        
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
                
                data['object_metadata']['metadata']['last_author_deep_search'] = current_time
                
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
    
    searcher = CompleteAuthorSearcher(objects_dir)
    
    # Search all unknown objects
    findings, failed = searcher.search_all_unknowns()
    
    print(f"\n" + "="*80)
    print(f"COMPLETE DEEP AUTHOR SEARCH RESULTS")
    print(f"="*80)
    print(f"Objects with unknown authors: {len(findings) + len(failed)}")
    print(f"Authors successfully discovered: {len(findings)}")
    print(f"Objects still unknown: {len(failed)}")
    print(f"Success rate: {len(findings)/(len(findings) + len(failed))*100:.1f}%")
    
    if findings:
        print("\nDISCOVERED AUTHORS:")
        for finding in sorted(findings, key=lambda x: int(x['object_id'])):
            print(f"  {finding['object_id']}: {finding['title']} → {finding['author']}")
        
        # Automatically update YAML files
        print(f"\nUpdating YAML files automatically...")
        updated = searcher.update_yaml_files(findings)
        print(f"✓ Successfully updated {updated}/{len(findings)} files")
    
    if failed:
        print(f"\nOBJECTS STILL WITHOUT AUTHORS ({len(failed)}):")
        for obj in sorted(failed, key=lambda x: int(x['object_id'])):
            print(f"  {obj['object_id']}: {obj['title']}")

if __name__ == "__main__":
    main()