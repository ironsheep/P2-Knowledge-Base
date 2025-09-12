#!/usr/bin/env python3
"""
Comprehensive P2 OBEX Discovery - Pages 1,3-14
Skips broken page 2, processes all other available pages
"""

import requests
import re
import time
import yaml
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
import sys

class ComprehensiveP2Discovery:
    def __init__(self, base_dir: str = None):
        self.base_url = "https://obex.parallax.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'P2-Knowledge-Base/1.0 (Educational/Research Purpose)'
        })
        
        # Setup paths
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            self.base_dir = Path(__file__).parent.parent.parent / "knowledge-base" / "external-resources" / "obex"
        
        self.objects_dir = self.base_dir / "objects"
        self.request_delay = 1.5
        
        # Pages to process (skip broken page 2)
        self.pages_to_process = [1] + list(range(3, 15))  # 1,3,4,5,6,7,8,9,10,11,12,13,14
        
        # Statistics
        self.stats = {
            'pages_processed': 0,
            'pages_failed': 0,
            'objects_discovered': 0,
            'objects_validated': 0,
            'p2_objects': 0,
            'p1_objects_skipped': 0,
            'errors': []
        }

    def discover_all_p2_objects(self) -> List[Dict]:
        """Discover P2 objects from specified pages"""
        print(f"🔍 Starting comprehensive P2 discovery...")
        print(f"📄 Processing pages: {self.pages_to_process}")
        
        all_objects = []
        
        for page_num in self.pages_to_process:
            if page_num == 1:
                url = f"{self.base_url}/microcontroller/propeller-2/"
            else:
                url = f"{self.base_url}/microcontroller/propeller-2/page/{page_num}/"
                
            print(f"  📄 Processing page {page_num}: {url}")
            
            try:
                response = self.session.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                page_objects = self._extract_objects_from_page(soup, page_num)
                
                if page_objects:
                    all_objects.extend(page_objects)
                    self.stats['pages_processed'] += 1
                    print(f"  📦 Found {len(page_objects)} objects on page {page_num}")
                else:
                    print(f"  ⚠️  No objects found on page {page_num}")
                
                # Rate limiting
                time.sleep(self.request_delay)
                
            except requests.RequestException as e:
                error = f"Error processing page {page_num}: {e}"
                print(f"  ❌ {error}")
                self.stats['errors'].append(error)
                self.stats['pages_failed'] += 1
                continue
                
        print(f"🎯 Discovery complete: {len(all_objects)} objects discovered across {self.stats['pages_processed']} pages")
        return all_objects

    def _extract_objects_from_page(self, soup: BeautifulSoup, page_num: int) -> List[Dict]:
        """Extract object metadata from page"""
        objects = []
        
        # Look for object title links that go to /obex/object-name/
        object_links = soup.find_all('a', href=re.compile(r'/obex/[^/]+/$'))
        
        for link in object_links:
            try:
                title = link.get_text().strip()
                url = urljoin(self.base_url, link['href'])
                
                if not title or '/page/' in url:
                    continue
                    
                # Extract object slug
                slug_match = re.search(r'/obex/([^/]+)/$', url)
                if not slug_match:
                    continue
                    
                slug = slug_match.group(1)
                
                object_data = {
                    'title': title,
                    'slug': slug,
                    'url': url,
                    'page_discovered': page_num,
                    'discovery_date': datetime.now().isoformat()
                }
                
                objects.append(object_data)
                self.stats['objects_discovered'] += 1
                
            except Exception as e:
                error = f"Error extracting object from link {link}: {e}"
                self.stats['errors'].append(error)
                continue
                
        return objects

    def extract_detailed_metadata(self, object_data: Dict) -> Optional[Dict]:
        """Extract detailed metadata and filter P1 objects"""
        print(f"  🔍 Processing: {object_data['title']}")
        
        try:
            response = self.session.get(object_data['url'])
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract Object ID
            object_id = self._extract_object_id(soup)
            if not object_id:
                print(f"    ⚠️  No object ID found, skipping")
                return None
                
            object_data['object_id'] = object_id
            object_data['download_url'] = f"{self.base_url}/wp-admin/admin-ajax.php?action=download_obex_zip&popcorn=salty&obuid=OB{object_id}"
            
            # Extract technical details and check P1/P2 compatibility
            technical_details = self._extract_technical_details(soup)
            object_data.update(technical_details)
            
            # P1/P2 filtering - CRITICAL CHECK
            languages = object_data.get('languages', [])
            microcontrollers = object_data.get('microcontrollers', [])
            
            # Check for P1 contamination indicators
            page_text = soup.get_text().upper()
            is_p1_object = (
                'PROPELLER 1' in page_text or 
                ('PASM' in languages and 'PASM2' not in languages and 'SPIN2' not in languages) or
                ('P1' in microcontrollers and 'P2' not in microcontrollers)
            )
            
            if is_p1_object:
                print(f"    ❌ P1 object detected, skipping")
                self.stats['p1_objects_skipped'] += 1
                return None
            
            # Extract enhanced metadata
            object_data['description'] = self._extract_description(soup)
            object_data['author'] = self._extract_author(soup)
            
            self.stats['objects_validated'] += 1
            self.stats['p2_objects'] += 1
            print(f"    ✅ P2 object confirmed: {object_id}")
            
            time.sleep(self.request_delay)
            return object_data
            
        except Exception as e:
            error = f"Error processing {object_data['title']}: {e}"
            print(f"    ❌ {error}")
            self.stats['errors'].append(error)
            return None

    def _extract_object_id(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract Object ID from page"""
        text = soup.get_text()
        id_match = re.search(r'Object\s+ID\s*:?\s*(\d+)', text, re.IGNORECASE)
        if id_match:
            return id_match.group(1)
        return None

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract object description"""
        for selector in ['.entry-content p', '.description p', 'p']:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text().strip()
                if len(text) > 50:
                    return text[:300]
        return ""

    def _extract_author(self, soup: BeautifulSoup) -> str:
        """Extract author information"""
        text = soup.get_text()
        author_patterns = [
            r'(?:by|author:)\s*([^\n,]+)',
            r'Author:\s*([^\n,]+)',
            r'Created by:\s*([^\n,]+)'
        ]
        
        for pattern in author_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return ""

    def _extract_technical_details(self, soup: BeautifulSoup) -> Dict:
        """Extract and validate technical specifications"""
        details = {}
        text = soup.get_text().upper()
        
        # Language detection with P1/P2 awareness
        languages = []
        microcontrollers = []
        
        if 'SPIN2' in text or 'SPIN 2' in text:
            languages.append('SPIN2')
        if 'PASM2' in text or 'PASM 2' in text:
            languages.append('PASM2')
        if 'PASM' in text and 'PASM2' not in text:
            languages.append('PASM')  # P1 indicator
        
        # Microcontroller detection
        if 'PROPELLER 2' in text or 'P2' in text:
            microcontrollers.append('P2')
        if 'PROPELLER 1' in text:
            microcontrollers.append('P1')
            
        details['languages'] = languages if languages else ['UNKNOWN']
        details['microcontrollers'] = microcontrollers if microcontrollers else ['UNKNOWN']
        
        return details

    def save_object_metadata(self, object_data: Dict):
        """Save P2 object metadata to YAML file"""
        object_id = object_data['object_id']
        file_path = self.objects_dir / f"{object_id}.yaml"
        
        # Create comprehensive YAML metadata
        yaml_data = {
            'object_metadata': {
                'object_id': object_id,
                'title': object_data.get('title', ''),
                'author': object_data.get('author', ''),
                'author_username': '',
                
                'urls': {
                    'obex_page': object_data.get('url', ''),
                    'download_direct': object_data.get('download_url', ''),
                    'forum_discussion': '',
                    'github_repo': '',
                    'documentation': ''
                },
                
                'technical_details': {
                    'languages': object_data.get('languages', ['SPIN2']),
                    'microcontroller': ['P2'],  # Guaranteed P2 since P1 filtered out
                    'version': '',
                    'file_format': 'ZIP',
                    'file_size': ''
                },
                
                'functionality': {
                    'category': self._categorize_object(object_data),
                    'subcategory': '',
                    'description_short': object_data.get('description', '')[:100],
                    'description_full': object_data.get('description', ''),
                    'tags': self._generate_tags(object_data),
                    'hardware_support': [],
                    'peripherals': []
                },
                
                'compatibility': {
                    'p2_chip_versions': ['all'],
                    'tested_platforms': [],
                    'known_issues': [],
                    'dependencies': []
                },
                
                'metadata': {
                    'discovery_date': object_data.get('discovery_date', datetime.now().isoformat()),
                    'last_verified': datetime.now().isoformat(),
                    'extraction_status': 'discovered',
                    'kb_integration': 'none',
                    'quality_score': 5,
                    'page_discovered': object_data.get('page_discovered', 0)
                }
            }
        }
        
        try:
            with open(file_path, 'w') as f:
                yaml.dump(yaml_data, f, default_flow_style=False, indent=2)
            print(f"    💾 Saved: {file_path}")
        except Exception as e:
            error = f"Error saving {file_path}: {e}"
            print(f"    ❌ {error}")
            self.stats['errors'].append(error)

    def _categorize_object(self, object_data: Dict) -> str:
        """Categorize object based on title and description"""
        title = object_data.get('title', '').lower()
        description = object_data.get('description', '').lower()
        text = f"{title} {description}"
        
        if any(word in text for word in ['driver', 'interface', 'protocol']):
            return 'drivers'
        elif any(word in text for word in ['sensor', 'imu', 'compass', 'ping']):
            return 'sensors'
        elif any(word in text for word in ['display', 'matrix', 'led', 'hub75']):
            return 'display'
        elif any(word in text for word in ['motor', 'servo', 'stepper']):
            return 'motors'
        elif any(word in text for word in ['serial', 'uart', 'communication']):
            return 'communication'
        elif any(word in text for word in ['audio', 'sound']):
            return 'audio'
        elif any(word in text for word in ['demo', 'example', 'test']):
            return 'demos'
        elif any(word in text for word in ['tool', 'utility']):
            return 'tools'
        else:
            return 'misc'

    def _generate_tags(self, object_data: Dict) -> List[str]:
        """Generate tags from object data"""
        tags = []
        text = f"{object_data.get('title', '')} {object_data.get('description', '')}".lower()
        
        tag_words = ['serial', 'display', 'sensor', 'motor', 'driver', 'demo']
        for tag in tag_words:
            if tag in text:
                tags.append(tag)
                
        return tags

    def run_comprehensive_discovery(self) -> Dict:
        """Run complete comprehensive P2 discovery"""
        print("🚀 Starting comprehensive P2 OBEX discovery...")
        print(f"📁 Output directory: {self.objects_dir}")
        
        # Discover objects from all accessible pages
        all_objects = self.discover_all_p2_objects()
        
        # Process each object with P1/P2 filtering
        p2_objects = []
        for i, obj in enumerate(all_objects, 1):
            print(f"📋 Processing {i}/{len(all_objects)}: {obj['title']} (Page {obj['page_discovered']})")
            
            detailed_obj = self.extract_detailed_metadata(obj)
            if detailed_obj:  # Only P2 objects pass the filter
                p2_objects.append(detailed_obj)
                self.save_object_metadata(detailed_obj)
        
        # Final comprehensive stats
        print(f"\n{'='*70}")
        print("🎯 COMPREHENSIVE P2 DISCOVERY COMPLETE")
        print(f"{'='*70}")
        print(f"📄 Pages processed: {self.stats['pages_processed']}/{len(self.pages_to_process)}")
        print(f"📄 Pages failed: {self.stats['pages_failed']}")
        print(f"📦 Total objects found: {self.stats['objects_discovered']}")
        print(f"✅ P2 objects validated: {self.stats['p2_objects']}")
        print(f"❌ P1 objects skipped: {self.stats['p1_objects_skipped']}")
        print(f"💾 Objects saved: {len(p2_objects)}")
        print(f"⚠️  Errors: {len(self.stats['errors'])}")
        
        return {
            'success': True,
            'p2_objects_found': len(p2_objects),
            'total_objects_scanned': self.stats['objects_discovered'],
            'p1_objects_filtered': self.stats['p1_objects_skipped'],
            'pages_processed': self.stats['pages_processed'],
            'statistics': self.stats
        }

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Comprehensive P2 OBEX discovery (pages 1,3-14)')
    parser.add_argument('--delay', type=float, default=1.5, help='Request delay')
    args = parser.parse_args()
    
    try:
        discovery = ComprehensiveP2Discovery()
        discovery.request_delay = args.delay
        
        result = discovery.run_comprehensive_discovery()
        
        if result['success']:
            print(f"\n✅ SUCCESS: Found {result['p2_objects_found']} P2 objects!")
            print(f"📊 Filtered out {result['p1_objects_filtered']} P1 objects")
            print(f"📄 Processed {result['pages_processed']} pages")
        
    except Exception as e:
        print(f"\n💥 Error: {e}")
        sys.exit(1)