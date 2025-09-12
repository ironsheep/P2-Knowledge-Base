#!/usr/bin/env python3
"""
OBEX Author Extraction Tool
Revisits individual object pages to extract accurate author and metadata
"""

import requests
import re
import time
import yaml
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from typing import Dict, Optional
from datetime import datetime
from pathlib import Path
import sys

class OBEXAuthorExtractor:
    def __init__(self, objects_dir: str):
        self.base_url = "https://obex.parallax.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'P2-Knowledge-Base/1.0 (Educational/Research Purpose)'
        })
        
        self.objects_dir = Path(objects_dir)
        self.request_delay = 1.2
        
        # Statistics
        self.stats = {
            'processed': 0,
            'updated': 0,
            'errors': 0,
            'authors_found': {}
        }

    def extract_author_from_page(self, object_id: str, obex_url: str) -> Dict:
        """Extract accurate author and metadata from OBEX object page"""
        print(f"  🔍 Extracting: Object {object_id}")
        
        try:
            response = self.session.get(obex_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract author information
            author_info = self._extract_author_info(soup)
            
            # Extract creation/update dates
            date_info = self._extract_date_info(soup)
            
            # Extract enhanced description and tags
            description_info = self._extract_description_info(soup)
            
            # Extract technical details
            technical_info = self._extract_technical_info(soup)
            
            result = {
                'object_id': object_id,
                'obex_url': obex_url,
                'extraction_date': datetime.now().isoformat(),
                **author_info,
                **date_info,
                **description_info,
                **technical_info
            }
            
            self.stats['processed'] += 1
            
            # Track authors
            if author_info.get('author'):
                author = author_info['author']
                if author not in self.stats['authors_found']:
                    self.stats['authors_found'][author] = []
                self.stats['authors_found'][author].append(object_id)
            
            time.sleep(self.request_delay)
            return result
            
        except Exception as e:
            print(f"    ❌ Error extracting {object_id}: {e}")
            self.stats['errors'] += 1
            return {
                'object_id': object_id,
                'error': str(e),
                'extraction_date': datetime.now().isoformat()
            }

    def _extract_author_info(self, soup: BeautifulSoup) -> Dict:
        """Extract author name and username"""
        author_info = {'author': '', 'author_username': ''}
        
        # Strategy 1: Look for "Author:" or "By:" labels
        text = soup.get_text()
        author_patterns = [
            r'Author:\s*([^\n\r,]+)',
            r'By:\s*([^\n\r,]+)',
            r'Created by:\s*([^\n\r,]+)',
            r'Submitted by:\s*([^\n\r,]+)'
        ]
        
        for pattern in author_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                author_name = match.group(1).strip()
                if len(author_name) > 2 and len(author_name) < 50:
                    author_info['author'] = author_name
                    break
        
        # Strategy 2: Look in metadata sections
        if not author_info['author']:
            for meta in soup.find_all(['meta', 'div', 'span'], attrs={'name': re.compile(r'author', re.I)}):
                content = meta.get('content', '') or meta.get_text().strip()
                if content and len(content) < 50:
                    author_info['author'] = content
                    break
        
        # Strategy 3: Extract username if present (often in URLs or links)
        username_match = re.search(r'/users/([a-zA-Z0-9_-]+)', str(soup))
        if username_match:
            author_info['author_username'] = username_match.group(1)
        
        return author_info

    def _extract_date_info(self, soup: BeautifulSoup) -> Dict:
        """Extract creation and update dates"""
        date_info = {'created_date': '', 'updated_date': ''}
        
        text = soup.get_text()
        
        # Look for date patterns
        date_patterns = [
            r'Created:\s*([0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{4})',
            r'Date:\s*([0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{4})',
            r'Updated:\s*([0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{4})',
            r'Posted:\s*([0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{4})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if 'created' in pattern.lower() or 'date' in pattern.lower() or 'posted' in pattern.lower():
                    date_info['created_date'] = match.group(1)
                elif 'updated' in pattern.lower():
                    date_info['updated_date'] = match.group(1)
        
        return date_info

    def _extract_description_info(self, soup: BeautifulSoup) -> Dict:
        """Extract enhanced description and tags"""
        desc_info = {'description_full': '', 'tags_extracted': []}
        
        # Look for description in common containers
        description_selectors = [
            '.entry-content',
            '.description', 
            '.object-description',
            'div[class*="description"]',
            'p'
        ]
        
        for selector in description_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text().strip()
                if len(text) > 50 and len(text) < 1000:  # Reasonable description length
                    desc_info['description_full'] = text
                    break
            if desc_info['description_full']:
                break
        
        # Extract tags from keywords or categories
        text = soup.get_text().lower()
        potential_tags = []
        
        tag_keywords = ['driver', 'sensor', 'display', 'motor', 'serial', 'i2c', 'spi', 
                       'uart', 'pwm', 'adc', 'led', 'servo', 'demo', 'example']
        
        for tag in tag_keywords:
            if tag in text:
                potential_tags.append(tag)
        
        desc_info['tags_extracted'] = potential_tags[:5]  # Limit to 5 tags
        
        return desc_info

    def _extract_technical_info(self, soup: BeautifulSoup) -> Dict:
        """Extract technical details like file size, language confirmation"""
        tech_info = {'file_size_extracted': '', 'languages_confirmed': []}
        
        text = soup.get_text().upper()
        
        # Look for file size
        size_match = re.search(r'(?:SIZE:|DOWNLOAD:)?\s*([0-9]+(?:\.[0-9]+)?\s*[KMG]?B)', text)
        if size_match:
            tech_info['file_size_extracted'] = size_match.group(1).strip()
        
        # Confirm languages mentioned on page
        if 'SPIN2' in text or 'SPIN 2' in text:
            tech_info['languages_confirmed'].append('SPIN2')
        if 'PASM2' in text or 'PASM 2' in text:
            tech_info['languages_confirmed'].append('PASM2')
        if 'PASM' in text and 'PASM2' not in text:
            tech_info['languages_confirmed'].append('PASM')  # P1 indicator
            
        return tech_info

    def update_object_metadata(self, object_file: Path, extracted_info: Dict):
        """Update existing object YAML with extracted information"""
        if 'error' in extracted_info:
            print(f"    ⚠️  Skipping update due to extraction error")
            return
            
        try:
            with open(object_file, 'r') as f:
                data = yaml.safe_load(f)
            
            obj = data['object_metadata']
            
            # Update author information
            if extracted_info.get('author'):
                obj['author'] = extracted_info['author']
                print(f"    ✅ Updated author: {extracted_info['author']}")
            
            if extracted_info.get('author_username'):
                obj['author_username'] = extracted_info['author_username']
            
            # Update dates if found
            if extracted_info.get('created_date'):
                obj['metadata']['created_date'] = extracted_info['created_date']
            
            # Update description if better than current
            current_desc = obj['functionality'].get('description_full', '')
            extracted_desc = extracted_info.get('description_full', '')
            if len(extracted_desc) > len(current_desc):
                obj['functionality']['description_full'] = extracted_desc
                obj['functionality']['description_short'] = extracted_desc[:100]
                print(f"    ✅ Updated description")
            
            # Add extracted tags
            if extracted_info.get('tags_extracted'):
                existing_tags = set(obj['functionality'].get('tags', []))
                new_tags = set(extracted_info['tags_extracted'])
                combined_tags = list(existing_tags.union(new_tags))
                obj['functionality']['tags'] = combined_tags
                print(f"    ✅ Updated tags: {combined_tags}")
            
            # Update technical details
            if extracted_info.get('file_size_extracted'):
                obj['technical_details']['file_size'] = extracted_info['file_size_extracted']
            
            # Update extraction metadata
            obj['metadata']['last_author_extraction'] = extracted_info['extraction_date']
            obj['metadata']['extraction_status'] = 'author_extracted'
            
            # Save updated file
            with open(object_file, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, indent=2)
                
            self.stats['updated'] += 1
            
        except Exception as e:
            print(f"    ❌ Error updating {object_file}: {e}")

    def extract_all_authors(self):
        """Process all object files to extract accurate author information"""
        print("🚀 Starting author extraction from OBEX object pages...")
        
        object_files = list(self.objects_dir.glob("*.yaml"))
        object_files = [f for f in object_files if f.name != '_template.yaml']
        
        print(f"📦 Found {len(object_files)} objects to process")
        
        for i, object_file in enumerate(object_files, 1):
            object_id = object_file.stem
            print(f"\n📋 Processing {i}/{len(object_files)}: Object {object_id}")
            
            # Load existing data to get OBEX URL
            try:
                with open(object_file, 'r') as f:
                    data = yaml.safe_load(f)
                    
                obex_url = data['object_metadata']['urls']['obex_page']
                
                if not obex_url:
                    print(f"    ⚠️  No OBEX URL found, skipping")
                    continue
                
                # Extract information from page
                extracted_info = self.extract_author_from_page(object_id, obex_url)
                
                # Update object file
                self.update_object_metadata(object_file, extracted_info)
                
            except Exception as e:
                print(f"    ❌ Error processing {object_file}: {e}")
                self.stats['errors'] += 1
        
        # Print final statistics
        print(f"\n{'='*60}")
        print("🎯 AUTHOR EXTRACTION COMPLETE")
        print(f"{'='*60}")
        print(f"📦 Objects processed: {self.stats['processed']}")
        print(f"✅ Objects updated: {self.stats['updated']}")
        print(f"❌ Errors: {self.stats['errors']}")
        
        print(f"\n👥 AUTHORS DISCOVERED:")
        for author, objects in sorted(self.stats['authors_found'].items(), key=lambda x: len(x[1]), reverse=True):
            print(f"  {author}: {len(objects)} objects")
            if len(objects) <= 5:
                print(f"    Objects: {', '.join(objects)}")

if __name__ == '__main__':
    objects_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/external-resources/obex/objects"
    
    extractor = OBEXAuthorExtractor(objects_dir)
    extractor.extract_all_authors()