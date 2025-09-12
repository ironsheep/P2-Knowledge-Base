#!/usr/bin/env python3
"""
OBEX P2 Object Discovery Tool - Fixed Version
Primary focus: https://obex.parallax.com/microcontroller/propeller-2/
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

class OBEXDiscovery:
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
        
        # Statistics
        self.stats = {
            'pages_processed': 0,
            'objects_discovered': 0,
            'objects_validated': 0,
            'errors': []
        }

    def discover_p2_objects(self) -> List[Dict]:
        """
        Discover all P2 objects from the microcontroller/propeller-2 pages
        """
        print("🔍 Discovering P2 objects from microcontroller pages...")
        
        objects = []
        page = 1
        
        while True:
            url = f"{self.base_url}/microcontroller/propeller-2/page/{page}/"
            print(f"  📄 Processing page {page}: {url}")
            
            try:
                response = self.session.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                page_objects = self._extract_p2_objects_from_page(soup)
                
                if not page_objects:
                    print(f"  ✅ No more objects found, stopping at page {page}")
                    break
                    
                objects.extend(page_objects)
                self.stats['pages_processed'] += 1
                
                print(f"  📦 Found {len(page_objects)} objects on page {page}")
                
                # Rate limiting
                time.sleep(self.request_delay)
                page += 1
                
                # Safety limit
                if page > 50:  # Reasonable safety limit
                    print("  ⚠️  Reached page limit of 50, stopping")
                    break
                
            except requests.RequestException as e:
                error = f"Error processing page {page}: {e}"
                print(f"  ❌ {error}")
                self.stats['errors'].append(error)
                break
                
        print(f"🎯 P2 discovery complete: {len(objects)} objects discovered")
        return objects

    def _extract_p2_objects_from_page(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract P2 object metadata from microcontroller page"""
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
                
                # Find parent container for author and description
                container = link.find_parent(['div', 'article', 'section'])
                author = ""
                description = ""
                
                if container:
                    container_text = container.get_text()
                    
                    # Look for author pattern
                    author_match = re.search(r'(?:by|author:)\s*([^\n,]+)', container_text, re.IGNORECASE)
                    if author_match:
                        author = author_match.group(1).strip()
                    
                    # Look for description (paragraph text that's not the title)
                    for p in container.find_all('p'):
                        p_text = p.get_text().strip()
                        if p_text and p_text != title and len(p_text) > 20:
                            description = p_text[:200]  # First 200 chars
                            break
                
                object_data = {
                    'title': title,
                    'slug': slug,
                    'url': url,
                    'author': author,
                    'description': description,
                    'category': 'propeller-2',
                    'discovery_date': datetime.now().isoformat()
                }
                
                objects.append(object_data)
                self.stats['objects_discovered'] += 1
                
            except Exception as e:
                error = f"Error extracting object from link {link}: {e}"
                self.stats['errors'].append(error)
                continue
                
        return objects

    def extract_detailed_metadata(self, object_data: Dict) -> Dict:
        """Extract detailed metadata from individual object page"""
        print(f"  🔍 Extracting details: {object_data['title']}")
        
        try:
            response = self.session.get(object_data['url'])
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract Object ID
            object_id = self._extract_object_id(soup)
            if object_id:
                object_data['object_id'] = object_id
                object_data['download_url'] = f"{self.base_url}/wp-admin/admin-ajax.php?action=download_obex_zip&popcorn=salty&obuid=OB{object_id}"
            
            # Extract enhanced description if not found
            if not object_data.get('description'):
                description = self._extract_description(soup)
                if description:
                    object_data['description'] = description
            
            # Extract technical details
            technical_details = self._extract_technical_details(soup)
            object_data.update(technical_details)
                
            self.stats['objects_validated'] += 1
            time.sleep(self.request_delay)
            
        except Exception as e:
            error = f"Error processing {object_data['title']}: {e}"
            print(f"    ❌ {error}")
            self.stats['errors'].append(error)
            
        return object_data

    def _extract_object_id(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract Object ID from page"""
        text = soup.get_text()
        id_match = re.search(r'Object\s+ID\s*:?\s*(\d+)', text, re.IGNORECASE)
        if id_match:
            return id_match.group(1)
        return None

    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract object description from page"""
        for selector in ['.entry-content p', '.description p', 'p']:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text().strip()
                if len(text) > 50:
                    return text[:300]
        return None

    def _extract_technical_details(self, soup: BeautifulSoup) -> Dict:
        """Extract technical specifications"""
        details = {}
        text = soup.get_text().upper()
        
        # Language detection
        languages = []
        if 'SPIN2' in text or 'SPIN 2' in text:
            languages.append('SPIN2')
        if 'PASM2' in text or 'PASM 2' in text:
            languages.append('PASM2')
        
        if languages:
            details['languages'] = languages
        else:
            details['languages'] = ['SPIN2']  # Default for P2 objects
        
        # Always P2 since from P2 microcontroller page
        details['microcontroller'] = ['P2']
        
        return details

    def save_object_metadata(self, object_data: Dict):
        """Save object metadata to YAML file"""
        if 'object_id' not in object_data:
            print(f"  ⚠️  No object ID for {object_data['title']}, skipping save")
            return
            
        object_id = object_data['object_id']
        file_path = self.objects_dir / f"{object_id}.yaml"
        
        # Convert to detailed format
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
                    'microcontroller': ['P2'],
                    'version': '',
                    'file_format': 'ZIP',
                    'file_size': ''
                },
                
                'functionality': {
                    'category': self._categorize_object(object_data),
                    'subcategory': '',
                    'description_short': object_data.get('description', '')[:100] if object_data.get('description') else '',
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
                    'quality_score': 5
                }
            }
        }
        
        try:
            with open(file_path, 'w') as f:
                yaml.dump(yaml_data, f, default_flow_style=False, indent=2)
            print(f"  💾 Saved: {file_path}")
        except Exception as e:
            error = f"Error saving {file_path}: {e}"
            print(f"  ❌ {error}")
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

    def run_discovery(self) -> Dict:
        """Run complete P2 discovery process"""
        print("🚀 Starting P2 OBEX discovery...")
        print(f"📁 Output directory: {self.base_dir}")
        
        # Discover all P2 objects
        all_objects = self.discover_p2_objects()
        
        # Extract detailed metadata for each
        detailed_objects = []
        for i, obj in enumerate(all_objects, 1):
            print(f"📋 Processing {i}/{len(all_objects)}: {obj['title']}")
            detailed_obj = self.extract_detailed_metadata(obj)
            detailed_objects.append(detailed_obj)
            
            # Save individual file
            self.save_object_metadata(detailed_obj)
        
        # Final stats
        print(f"\\n{'='*60}")
        print("🎯 P2 DISCOVERY COMPLETE")
        print(f"{'='*60}")
        print(f"📄 Pages processed: {self.stats['pages_processed']}")
        print(f"📦 Objects discovered: {self.stats['objects_discovered']}")
        print(f"✅ Objects validated: {self.stats['objects_validated']}")
        print(f"❌ Errors: {len(self.stats['errors'])}")
        
        return {
            'success': True,
            'objects_found': len(detailed_objects),
            'statistics': self.stats
        }

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Discover P2 objects from OBEX')
    parser.add_argument('--delay', type=float, default=1.5, help='Request delay')
    args = parser.parse_args()
    
    try:
        discovery = OBEXDiscovery()
        discovery.request_delay = args.delay
        
        result = discovery.run_discovery()
        
        if result['success']:
            print(f"\\n✅ Found {result['objects_found']} P2 objects!")
        
    except Exception as e:
        print(f"\\n💥 Error: {e}")
        sys.exit(1)