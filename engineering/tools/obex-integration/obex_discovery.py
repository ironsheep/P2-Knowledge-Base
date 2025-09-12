#!/usr/bin/env python3
"""
OBEX P2 Object Discovery Tool
Systematically discovers and catalogs P2-compatible objects from Parallax OBEX
"""

import requests
import re
import time
import yaml
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
import sys
from pathlib import Path

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
        self.authors_dir = self.base_dir / "authors"
        self.master_index_path = self.base_dir / "master-index.yaml"
        
        # Rate limiting
        self.request_delay = 1.0  # Respectful crawling
        
        # Statistics
        self.stats = {
            'pages_processed': 0,
            'objects_discovered': 0,
            'objects_validated': 0,
            'errors': []
        }

    def discover_category_objects(self, category: str = "spin2") -> List[Dict]:
        """
        Discover all objects in a specific category (spin2, pasm2, propeller-2)
        """
        print(f"🔍 Discovering objects in category: {category}")
        
        objects = []
        page = 1
        
        while True:
            # Handle different URL patterns
            if category == 'propeller-2':
                url = f"{self.base_url}/microcontroller/{category}/page/{page}/"
            else:
                url = f"{self.base_url}/code-language/{category}/page/{page}/"
            print(f"  📄 Processing page {page}: {url}")
            
            try:
                response = self.session.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                page_objects = self._extract_objects_from_page(soup, category)
                
                if not page_objects:
                    print(f"  ✅ No more objects found, stopping at page {page}")
                    break
                    
                objects.extend(page_objects)
                self.stats['pages_processed'] += 1
                
                print(f"  📦 Found {len(page_objects)} objects on page {page}")
                
                # Rate limiting
                time.sleep(self.request_delay)
                page += 1
                
            except requests.RequestException as e:
                error = f"Error processing page {page}: {e}"
                print(f"  ❌ {error}")
                self.stats['errors'].append(error)
                break
                
        print(f"🎯 Category {category} complete: {len(objects)} objects discovered")
        return objects
    
    def discover_author_objects(self, author_slug: str) -> List[Dict]:
        """
        Discover P2 objects by a specific author from their author page
        Author page has separate "Propeller 1" and "Propeller 2" tables
        """
        print(f"👤 Discovering P2 objects by author: {author_slug}")
        
        objects = []
        author_url = f"{self.base_url}/author/{author_slug}/"
        
        try:
            response = self.session.get(author_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the "Propeller 2" table section
            p2_section = None
            for heading in soup.find_all(['h2', 'h3', 'h4']):
                if 'Propeller 2' in heading.get_text():
                    p2_section = heading
                    break
            
            if not p2_section:
                print(f"  ⚠️  No Propeller 2 section found for {author_slug}")
                return objects
            
            # Find the table/list after the Propeller 2 heading
            # Look for links to object pages in the P2 section
            current = p2_section
            while current and current.next_sibling:
                current = current.next_sibling
                if hasattr(current, 'find_all'):
                    # Look for object links in this section
                    object_links = current.find_all('a', href=re.compile(r'/obex/[^/]+/

    def _extract_objects_from_page(self, soup: BeautifulSoup, category: str) -> List[Dict]:
        """Extract object metadata from a category page"""
        objects = []
        
        # Look for object listings - this may need adjustment based on OBEX structure
        object_links = soup.find_all('a', href=re.compile(r'/obex/[^/]+/$'))
        
        for link in object_links:
            try:
                # Extract basic info from category page
                title = link.get_text().strip()
                url = urljoin(self.base_url, link['href'])
                
                # Skip if not a proper object link
                if not title or '/page/' in url:
                    continue
                    
                # Extract object slug for ID extraction
                slug_match = re.search(r'/obex/([^/]+)/$', url)
                if not slug_match:
                    continue
                    
                slug = slug_match.group(1)
                
                # Try to find parent container for more metadata
                container = link.find_parent(['div', 'article', 'section'])
                author = ""
                if container:
                    author_text = container.get_text()
                    # Look for "by Author Name" patterns
                    author_match = re.search(r'by\s+([^,\n]+)', author_text)
                    if author_match:
                        author = author_match.group(1).strip()
                
                object_data = {
                    'title': title,
                    'slug': slug,
                    'url': url,
                    'author': author,
                    'category': category,
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
        """
        Extract detailed metadata from individual object page
        """
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
            
            # Extract description
            description = self._extract_description(soup)
            if description:
                object_data['description'] = description
            
            # Extract author information
            author_info = self._extract_author_info(soup)
            if author_info:
                object_data.update(author_info)
            
            # Extract technical details
            technical_details = self._extract_technical_details(soup)
            if technical_details:
                object_data.update(technical_details)
            
            # Extract related links
            links = self._extract_related_links(soup)
            if links:
                object_data['related_links'] = links
                
            self.stats['objects_validated'] += 1
            time.sleep(self.request_delay)  # Rate limiting
            
        except requests.RequestException as e:
            error = f"Error fetching details for {object_data['url']}: {e}"
            print(f"    ❌ {error}")
            self.stats['errors'].append(error)
        except Exception as e:
            error = f"Error processing details for {object_data['title']}: {e}"
            print(f"    ❌ {error}")
            self.stats['errors'].append(error)
            
        return object_data

    def _extract_object_id(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract Object ID from page"""
        # Look for "Object ID : XXXX" pattern
        text = soup.get_text()
        id_match = re.search(r'Object ID\s*:\s*(\d+)', text, re.IGNORECASE)
        if id_match:
            return id_match.group(1)
        return None

    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract object description"""
        # Look for description in various possible containers
        desc_selectors = [
            '.entry-content p',
            '.object-description',
            '.description',
            'p'
        ]
        
        for selector in desc_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text().strip()
                if len(text) > 50:  # Reasonable description length
                    return text
        return None

    def _extract_author_info(self, soup: BeautifulSoup) -> Dict:
        """Extract detailed author information"""
        author_info = {}
        
        # Look for author patterns in text
        text = soup.get_text()
        
        # Various author patterns
        patterns = [
            r'Author\s*:\s*([^\n]+)',
            r'By\s+([^\n,]+)',
            r'Created by\s+([^\n,]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                author_info['author_detailed'] = match.group(1).strip()
                break
                
        return author_info

    def _extract_technical_details(self, soup: BeautifulSoup) -> Dict:
        """Extract technical specifications"""
        details = {}
        text = soup.get_text()
        
        # Language detection
        languages = []
        if 'SPIN2' in text.upper() or 'SPIN 2' in text.upper():
            languages.append('SPIN2')
        if 'PASM2' in text.upper() or 'PASM 2' in text.upper():
            languages.append('PASM2')
        if 'PASM' in text.upper() and 'PASM2' not in text.upper():
            languages.append('PASM')
        
        if languages:
            details['languages'] = languages
        
        # P2 compatibility check
        if 'P2' in text or 'Propeller 2' in text:
            details['microcontroller'] = ['P2']
        
        return details

    def _extract_related_links(self, soup: BeautifulSoup) -> Dict:
        """Extract related links (GitHub, forum, etc.)"""
        links = {}
        
        # Find all links
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text().lower()
            
            if 'github.com' in href:
                links['github'] = href
            elif 'forums.parallax.com' in href:
                links['forum'] = href
            elif 'documentation' in text or 'docs' in text:
                links['documentation'] = href
                
        return links

    def save_object_metadata(self, object_data: Dict):
        """Save object metadata to individual YAML file"""
        if 'object_id' not in object_data:
            print(f"  ⚠️  No object ID for {object_data['title']}, skipping save")
            return
            
        object_id = object_data['object_id']
        file_path = self.objects_dir / f"{object_id}.yaml"
        
        # Convert to detailed YAML format
        detailed_metadata = self._convert_to_detailed_format(object_data)
        
        try:
            with open(file_path, 'w') as f:
                yaml.dump(detailed_metadata, f, default_flow_style=False, indent=2)
            print(f"  💾 Saved: {file_path}")
        except Exception as e:
            error = f"Error saving {file_path}: {e}"
            print(f"  ❌ {error}")
            self.stats['errors'].append(error)

    def _convert_to_detailed_format(self, object_data: Dict) -> Dict:
        """Convert discovered data to detailed YAML format"""
        return {
            'object_metadata': {
                'object_id': object_data.get('object_id', ''),
                'title': object_data.get('title', ''),
                'author': object_data.get('author_detailed', object_data.get('author', '')),
                'author_username': '',  # To be filled later
                
                'urls': {
                    'obex_page': object_data.get('url', ''),
                    'download_direct': object_data.get('download_url', ''),
                    'forum_discussion': object_data.get('related_links', {}).get('forum', ''),
                    'github_repo': object_data.get('related_links', {}).get('github', ''),
                    'documentation': object_data.get('related_links', {}).get('documentation', '')
                },
                
                'technical_details': {
                    'languages': object_data.get('languages', []),
                    'microcontroller': object_data.get('microcontroller', ['P2']),
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
                
                'architecture': {
                    'multi_cog': False,  # Default, to be analyzed
                    'cog_count': 1,
                    'memory_requirements': {
                        'hub_ram': '',
                        'cog_ram': ''
                    },
                    'performance_notes': ''
                },
                
                'compatibility': {
                    'p2_chip_versions': ['all'],
                    'tested_platforms': [],
                    'known_issues': [],
                    'dependencies': []
                },
                
                'community': {
                    'forum_posts': [],
                    'user_reviews': [],
                    'modification_notes': [],
                    'related_objects': []
                },
                
                'metadata': {
                    'discovery_date': object_data.get('discovery_date', datetime.now().isoformat()),
                    'last_verified': datetime.now().isoformat(),
                    'extraction_status': 'discovered',
                    'kb_integration': 'none',
                    'quality_score': 5  # Default, to be assessed
                },
                
                'notes': {
                    'extraction_notes': f"Auto-discovered from {object_data.get('category', 'unknown')} category",
                    'analysis_notes': '',
                    'integration_todo': []
                }
            }
        }

    def _categorize_object(self, object_data: Dict) -> str:
        """Automatically categorize object based on title and description"""
        title = object_data.get('title', '').lower()
        description = object_data.get('description', '').lower()
        text = f"{title} {description}"
        
        # Category detection rules
        if any(word in text for word in ['driver', 'interface', 'protocol']):
            return 'drivers'
        elif any(word in text for word in ['sensor', 'imu', 'compass', 'ping']):
            return 'sensors'
        elif any(word in text for word in ['display', 'matrix', 'led', 'nextion']):
            return 'display'
        elif any(word in text for word in ['motor', 'servo', 'stepper', 'bldc']):
            return 'motors'
        elif any(word in text for word in ['serial', 'uart', 'communication', 'wifi']):
            return 'communication'
        elif any(word in text for word in ['audio', 'sound', 'synth', 'fm']):
            return 'audio'
        elif any(word in text for word in ['demo', 'example', 'test']):
            return 'demos'
        elif any(word in text for word in ['tool', 'utility', 'library']):
            return 'tools'
        else:
            return 'misc'

    def _generate_tags(self, object_data: Dict) -> List[str]:
        """Generate tags based on object data"""
        tags = []
        title = object_data.get('title', '').lower()
        description = object_data.get('description', '').lower()
        text = f"{title} {description}"
        
        # Common tag patterns
        tag_patterns = {
            'serial': ['serial', 'uart', 'communication'],
            'display': ['display', 'led', 'matrix', 'screen'],
            'sensor': ['sensor', 'imu', 'compass', 'ping'],
            'motor': ['motor', 'servo', 'stepper'],
            'driver': ['driver', 'interface'],
            'wifi': ['wifi', 'esp32', 'wireless'],
            'audio': ['audio', 'sound', 'synth'],
            'demo': ['demo', 'example', 'test']
        }
        
        for tag, patterns in tag_patterns.items():
            if any(pattern in text for pattern in patterns):
                tags.append(tag)
                
        return tags

    def update_master_index(self, objects: List[Dict]):
        """Update the master index with discovered objects"""
        print(f"📝 Updating master index with {len(objects)} objects")
        
        try:
            # Load existing index or create new
            if self.master_index_path.exists():
                with open(self.master_index_path, 'r') as f:
                    index = yaml.safe_load(f)
            else:
                # Use template structure
                index = {
                    'metadata': {
                        'generated_date': datetime.now().isoformat(),
                        'last_updated': datetime.now().isoformat(),
                        'total_objects': 0,
                        'sources': [
                            "https://obex.parallax.com/code-language/spin2/",
                            "https://obex.parallax.com/code-language/pasm2/"
                        ],
                        'schema_version': "1.0"
                    },
                    'objects': [],
                    'indices': {
                        'by_author': {},
                        'by_category': {},
                        'by_hardware': {},
                        'by_language': {}
                    },
                    'statistics': {
                        'objects_by_category': {},
                        'objects_by_author': {},
                        'objects_by_language': {},
                        'most_active_authors': [],
                        'newest_objects': [],
                        'most_downloaded': []
                    },
                    'discovery_status': {
                        'categories_processed': [],
                        'pages_processed': self.stats['pages_processed'],
                        'objects_discovered': self.stats['objects_discovered'],
                        'objects_validated': self.stats['objects_validated'],
                        'errors_encountered': len(self.stats['errors']),
                        'last_discovery_run': datetime.now().isoformat()
                    }
                }
            
            # Update metadata
            index['metadata']['last_updated'] = datetime.now().isoformat()
            
            # Add objects to index
            existing_ids = {obj.get('object_id') for obj in index.get('objects', [])}
            
            for obj in objects:
                if obj.get('object_id') and obj['object_id'] not in existing_ids:
                    index_entry = {
                        'object_id': obj['object_id'],
                        'title': obj.get('title', ''),
                        'author': obj.get('author_detailed', obj.get('author', '')),
                        'url': obj.get('url', ''),
                        'download_url': obj.get('download_url', ''),
                        'languages': obj.get('languages', []),
                        'microcontroller': obj.get('microcontroller', ['P2']),
                        'category': self._categorize_object(obj),
                        'tags': self._generate_tags(obj),
                        'discovery_date': obj.get('discovery_date', datetime.now().isoformat())
                    }
                    
                    index['objects'].append(index_entry)
            
            # Update statistics
            index['metadata']['total_objects'] = len(index['objects'])
            index['discovery_status'].update({
                'pages_processed': self.stats['pages_processed'],
                'objects_discovered': self.stats['objects_discovered'],
                'objects_validated': self.stats['objects_validated'],
                'errors_encountered': len(self.stats['errors']),
                'last_discovery_run': datetime.now().isoformat()
            })
            
            # Save updated index
            with open(self.master_index_path, 'w') as f:
                yaml.dump(index, f, default_flow_style=False, indent=2)
                
            print(f"✅ Master index updated: {len(index['objects'])} total objects")
            
        except Exception as e:
            error = f"Error updating master index: {e}"
            print(f"❌ {error}")
            self.stats['errors'].append(error)

    def run_discovery(self, categories: List[str] = None) -> Dict:
        """
        Run complete discovery process
        """
        if categories is None:
            categories = ['spin2', 'pasm2', 'propeller-2']
            
        print(f"🚀 Starting OBEX discovery for categories: {categories}")
        print(f"📁 Output directory: {self.base_dir}")
        
        all_objects = []
        
        for category in categories:
            print(f"\n{'='*60}")
            print(f"Processing category: {category.upper()}")
            print(f"{'='*60}")
            
            # Discover objects in category
            category_objects = self.discover_category_objects(category)
            
            # Extract detailed metadata for each object
            detailed_objects = []
            for i, obj in enumerate(category_objects, 1):
                print(f"📋 Processing {i}/{len(category_objects)}: {obj['title']}")
                detailed_obj = self.extract_detailed_metadata(obj)
                detailed_objects.append(detailed_obj)
                
                # Save individual object file
                self.save_object_metadata(detailed_obj)
            
            all_objects.extend(detailed_objects)
        
        # Update master index
        self.update_master_index(all_objects)
        
        # Print final statistics
        print(f"\n{'='*60}")
        print("🎯 DISCOVERY COMPLETE")
        print(f"{'='*60}")
        print(f"📄 Pages processed: {self.stats['pages_processed']}")
        print(f"📦 Objects discovered: {self.stats['objects_discovered']}")
        print(f"✅ Objects validated: {self.stats['objects_validated']}")
        print(f"❌ Errors encountered: {len(self.stats['errors'])}")
        
        if self.stats['errors']:
            print(f"\n⚠️  Error Summary:")
            for error in self.stats['errors'][:10]:  # Show first 10 errors
                print(f"  • {error}")
            if len(self.stats['errors']) > 10:
                print(f"  ... and {len(self.stats['errors']) - 10} more errors")
        
        return {
            'success': True,
            'objects_found': len(all_objects),
            'statistics': self.stats
        }

def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Discover P2 objects from Parallax OBEX')
    parser.add_argument('--categories', nargs='+', default=['spin2', 'pasm2'], 
                       help='Categories to discover (default: spin2 pasm2)')
    parser.add_argument('--output-dir', help='Output directory for results')
    parser.add_argument('--delay', type=float, default=1.0,
                       help='Delay between requests in seconds (default: 1.0)')
    
    args = parser.parse_args()
    
    try:
        discovery = OBEXDiscovery(base_dir=args.output_dir)
        discovery.request_delay = args.delay
        
        result = discovery.run_discovery(categories=args.categories)
        
        if result['success']:
            print(f"\n✅ Discovery completed successfully!")
            print(f"Found {result['objects_found']} P2 objects")
            sys.exit(0)
        else:
            print(f"\n❌ Discovery failed")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n🛑 Discovery interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()))
                    
                    for link in object_links:
                        try:
                            title = link.get_text().strip()
                            url = urljoin(self.base_url, link['href'])
                            
                            # Extract object slug for processing
                            slug_match = re.search(r'/obex/([^/]+)/

    def _extract_objects_from_page(self, soup: BeautifulSoup, category: str) -> List[Dict]:
        """Extract object metadata from a category page"""
        objects = []
        
        # Look for object listings - this may need adjustment based on OBEX structure
        object_links = soup.find_all('a', href=re.compile(r'/obex/[^/]+/$'))
        
        for link in object_links:
            try:
                # Extract basic info from category page
                title = link.get_text().strip()
                url = urljoin(self.base_url, link['href'])
                
                # Skip if not a proper object link
                if not title or '/page/' in url:
                    continue
                    
                # Extract object slug for ID extraction
                slug_match = re.search(r'/obex/([^/]+)/$', url)
                if not slug_match:
                    continue
                    
                slug = slug_match.group(1)
                
                # Try to find parent container for more metadata
                container = link.find_parent(['div', 'article', 'section'])
                author = ""
                if container:
                    author_text = container.get_text()
                    # Look for "by Author Name" patterns
                    author_match = re.search(r'by\s+([^,\n]+)', author_text)
                    if author_match:
                        author = author_match.group(1).strip()
                
                object_data = {
                    'title': title,
                    'slug': slug,
                    'url': url,
                    'author': author,
                    'category': category,
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
        """
        Extract detailed metadata from individual object page
        """
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
            
            # Extract description
            description = self._extract_description(soup)
            if description:
                object_data['description'] = description
            
            # Extract author information
            author_info = self._extract_author_info(soup)
            if author_info:
                object_data.update(author_info)
            
            # Extract technical details
            technical_details = self._extract_technical_details(soup)
            if technical_details:
                object_data.update(technical_details)
            
            # Extract related links
            links = self._extract_related_links(soup)
            if links:
                object_data['related_links'] = links
                
            self.stats['objects_validated'] += 1
            time.sleep(self.request_delay)  # Rate limiting
            
        except requests.RequestException as e:
            error = f"Error fetching details for {object_data['url']}: {e}"
            print(f"    ❌ {error}")
            self.stats['errors'].append(error)
        except Exception as e:
            error = f"Error processing details for {object_data['title']}: {e}"
            print(f"    ❌ {error}")
            self.stats['errors'].append(error)
            
        return object_data

    def _extract_object_id(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract Object ID from page"""
        # Look for "Object ID : XXXX" pattern
        text = soup.get_text()
        id_match = re.search(r'Object ID\s*:\s*(\d+)', text, re.IGNORECASE)
        if id_match:
            return id_match.group(1)
        return None

    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract object description"""
        # Look for description in various possible containers
        desc_selectors = [
            '.entry-content p',
            '.object-description',
            '.description',
            'p'
        ]
        
        for selector in desc_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text().strip()
                if len(text) > 50:  # Reasonable description length
                    return text
        return None

    def _extract_author_info(self, soup: BeautifulSoup) -> Dict:
        """Extract detailed author information"""
        author_info = {}
        
        # Look for author patterns in text
        text = soup.get_text()
        
        # Various author patterns
        patterns = [
            r'Author\s*:\s*([^\n]+)',
            r'By\s+([^\n,]+)',
            r'Created by\s+([^\n,]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                author_info['author_detailed'] = match.group(1).strip()
                break
                
        return author_info

    def _extract_technical_details(self, soup: BeautifulSoup) -> Dict:
        """Extract technical specifications"""
        details = {}
        text = soup.get_text()
        
        # Language detection
        languages = []
        if 'SPIN2' in text.upper() or 'SPIN 2' in text.upper():
            languages.append('SPIN2')
        if 'PASM2' in text.upper() or 'PASM 2' in text.upper():
            languages.append('PASM2')
        if 'PASM' in text.upper() and 'PASM2' not in text.upper():
            languages.append('PASM')
        
        if languages:
            details['languages'] = languages
        
        # P2 compatibility check
        if 'P2' in text or 'Propeller 2' in text:
            details['microcontroller'] = ['P2']
        
        return details

    def _extract_related_links(self, soup: BeautifulSoup) -> Dict:
        """Extract related links (GitHub, forum, etc.)"""
        links = {}
        
        # Find all links
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text().lower()
            
            if 'github.com' in href:
                links['github'] = href
            elif 'forums.parallax.com' in href:
                links['forum'] = href
            elif 'documentation' in text or 'docs' in text:
                links['documentation'] = href
                
        return links

    def save_object_metadata(self, object_data: Dict):
        """Save object metadata to individual YAML file"""
        if 'object_id' not in object_data:
            print(f"  ⚠️  No object ID for {object_data['title']}, skipping save")
            return
            
        object_id = object_data['object_id']
        file_path = self.objects_dir / f"{object_id}.yaml"
        
        # Convert to detailed YAML format
        detailed_metadata = self._convert_to_detailed_format(object_data)
        
        try:
            with open(file_path, 'w') as f:
                yaml.dump(detailed_metadata, f, default_flow_style=False, indent=2)
            print(f"  💾 Saved: {file_path}")
        except Exception as e:
            error = f"Error saving {file_path}: {e}"
            print(f"  ❌ {error}")
            self.stats['errors'].append(error)

    def _convert_to_detailed_format(self, object_data: Dict) -> Dict:
        """Convert discovered data to detailed YAML format"""
        return {
            'object_metadata': {
                'object_id': object_data.get('object_id', ''),
                'title': object_data.get('title', ''),
                'author': object_data.get('author_detailed', object_data.get('author', '')),
                'author_username': '',  # To be filled later
                
                'urls': {
                    'obex_page': object_data.get('url', ''),
                    'download_direct': object_data.get('download_url', ''),
                    'forum_discussion': object_data.get('related_links', {}).get('forum', ''),
                    'github_repo': object_data.get('related_links', {}).get('github', ''),
                    'documentation': object_data.get('related_links', {}).get('documentation', '')
                },
                
                'technical_details': {
                    'languages': object_data.get('languages', []),
                    'microcontroller': object_data.get('microcontroller', ['P2']),
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
                
                'architecture': {
                    'multi_cog': False,  # Default, to be analyzed
                    'cog_count': 1,
                    'memory_requirements': {
                        'hub_ram': '',
                        'cog_ram': ''
                    },
                    'performance_notes': ''
                },
                
                'compatibility': {
                    'p2_chip_versions': ['all'],
                    'tested_platforms': [],
                    'known_issues': [],
                    'dependencies': []
                },
                
                'community': {
                    'forum_posts': [],
                    'user_reviews': [],
                    'modification_notes': [],
                    'related_objects': []
                },
                
                'metadata': {
                    'discovery_date': object_data.get('discovery_date', datetime.now().isoformat()),
                    'last_verified': datetime.now().isoformat(),
                    'extraction_status': 'discovered',
                    'kb_integration': 'none',
                    'quality_score': 5  # Default, to be assessed
                },
                
                'notes': {
                    'extraction_notes': f"Auto-discovered from {object_data.get('category', 'unknown')} category",
                    'analysis_notes': '',
                    'integration_todo': []
                }
            }
        }

    def _categorize_object(self, object_data: Dict) -> str:
        """Automatically categorize object based on title and description"""
        title = object_data.get('title', '').lower()
        description = object_data.get('description', '').lower()
        text = f"{title} {description}"
        
        # Category detection rules
        if any(word in text for word in ['driver', 'interface', 'protocol']):
            return 'drivers'
        elif any(word in text for word in ['sensor', 'imu', 'compass', 'ping']):
            return 'sensors'
        elif any(word in text for word in ['display', 'matrix', 'led', 'nextion']):
            return 'display'
        elif any(word in text for word in ['motor', 'servo', 'stepper', 'bldc']):
            return 'motors'
        elif any(word in text for word in ['serial', 'uart', 'communication', 'wifi']):
            return 'communication'
        elif any(word in text for word in ['audio', 'sound', 'synth', 'fm']):
            return 'audio'
        elif any(word in text for word in ['demo', 'example', 'test']):
            return 'demos'
        elif any(word in text for word in ['tool', 'utility', 'library']):
            return 'tools'
        else:
            return 'misc'

    def _generate_tags(self, object_data: Dict) -> List[str]:
        """Generate tags based on object data"""
        tags = []
        title = object_data.get('title', '').lower()
        description = object_data.get('description', '').lower()
        text = f"{title} {description}"
        
        # Common tag patterns
        tag_patterns = {
            'serial': ['serial', 'uart', 'communication'],
            'display': ['display', 'led', 'matrix', 'screen'],
            'sensor': ['sensor', 'imu', 'compass', 'ping'],
            'motor': ['motor', 'servo', 'stepper'],
            'driver': ['driver', 'interface'],
            'wifi': ['wifi', 'esp32', 'wireless'],
            'audio': ['audio', 'sound', 'synth'],
            'demo': ['demo', 'example', 'test']
        }
        
        for tag, patterns in tag_patterns.items():
            if any(pattern in text for pattern in patterns):
                tags.append(tag)
                
        return tags

    def update_master_index(self, objects: List[Dict]):
        """Update the master index with discovered objects"""
        print(f"📝 Updating master index with {len(objects)} objects")
        
        try:
            # Load existing index or create new
            if self.master_index_path.exists():
                with open(self.master_index_path, 'r') as f:
                    index = yaml.safe_load(f)
            else:
                # Use template structure
                index = {
                    'metadata': {
                        'generated_date': datetime.now().isoformat(),
                        'last_updated': datetime.now().isoformat(),
                        'total_objects': 0,
                        'sources': [
                            "https://obex.parallax.com/code-language/spin2/",
                            "https://obex.parallax.com/code-language/pasm2/"
                        ],
                        'schema_version': "1.0"
                    },
                    'objects': [],
                    'indices': {
                        'by_author': {},
                        'by_category': {},
                        'by_hardware': {},
                        'by_language': {}
                    },
                    'statistics': {
                        'objects_by_category': {},
                        'objects_by_author': {},
                        'objects_by_language': {},
                        'most_active_authors': [],
                        'newest_objects': [],
                        'most_downloaded': []
                    },
                    'discovery_status': {
                        'categories_processed': [],
                        'pages_processed': self.stats['pages_processed'],
                        'objects_discovered': self.stats['objects_discovered'],
                        'objects_validated': self.stats['objects_validated'],
                        'errors_encountered': len(self.stats['errors']),
                        'last_discovery_run': datetime.now().isoformat()
                    }
                }
            
            # Update metadata
            index['metadata']['last_updated'] = datetime.now().isoformat()
            
            # Add objects to index
            existing_ids = {obj.get('object_id') for obj in index.get('objects', [])}
            
            for obj in objects:
                if obj.get('object_id') and obj['object_id'] not in existing_ids:
                    index_entry = {
                        'object_id': obj['object_id'],
                        'title': obj.get('title', ''),
                        'author': obj.get('author_detailed', obj.get('author', '')),
                        'url': obj.get('url', ''),
                        'download_url': obj.get('download_url', ''),
                        'languages': obj.get('languages', []),
                        'microcontroller': obj.get('microcontroller', ['P2']),
                        'category': self._categorize_object(obj),
                        'tags': self._generate_tags(obj),
                        'discovery_date': obj.get('discovery_date', datetime.now().isoformat())
                    }
                    
                    index['objects'].append(index_entry)
            
            # Update statistics
            index['metadata']['total_objects'] = len(index['objects'])
            index['discovery_status'].update({
                'pages_processed': self.stats['pages_processed'],
                'objects_discovered': self.stats['objects_discovered'],
                'objects_validated': self.stats['objects_validated'],
                'errors_encountered': len(self.stats['errors']),
                'last_discovery_run': datetime.now().isoformat()
            })
            
            # Save updated index
            with open(self.master_index_path, 'w') as f:
                yaml.dump(index, f, default_flow_style=False, indent=2)
                
            print(f"✅ Master index updated: {len(index['objects'])} total objects")
            
        except Exception as e:
            error = f"Error updating master index: {e}"
            print(f"❌ {error}")
            self.stats['errors'].append(error)

    def run_discovery(self, categories: List[str] = None) -> Dict:
        """
        Run complete discovery process
        """
        if categories is None:
            categories = ['spin2', 'pasm2', 'propeller-2']
            
        print(f"🚀 Starting OBEX discovery for categories: {categories}")
        print(f"📁 Output directory: {self.base_dir}")
        
        all_objects = []
        
        for category in categories:
            print(f"\n{'='*60}")
            print(f"Processing category: {category.upper()}")
            print(f"{'='*60}")
            
            # Discover objects in category
            category_objects = self.discover_category_objects(category)
            
            # Extract detailed metadata for each object
            detailed_objects = []
            for i, obj in enumerate(category_objects, 1):
                print(f"📋 Processing {i}/{len(category_objects)}: {obj['title']}")
                detailed_obj = self.extract_detailed_metadata(obj)
                detailed_objects.append(detailed_obj)
                
                # Save individual object file
                self.save_object_metadata(detailed_obj)
            
            all_objects.extend(detailed_objects)
        
        # Update master index
        self.update_master_index(all_objects)
        
        # Print final statistics
        print(f"\n{'='*60}")
        print("🎯 DISCOVERY COMPLETE")
        print(f"{'='*60}")
        print(f"📄 Pages processed: {self.stats['pages_processed']}")
        print(f"📦 Objects discovered: {self.stats['objects_discovered']}")
        print(f"✅ Objects validated: {self.stats['objects_validated']}")
        print(f"❌ Errors encountered: {len(self.stats['errors'])}")
        
        if self.stats['errors']:
            print(f"\n⚠️  Error Summary:")
            for error in self.stats['errors'][:10]:  # Show first 10 errors
                print(f"  • {error}")
            if len(self.stats['errors']) > 10:
                print(f"  ... and {len(self.stats['errors']) - 10} more errors")
        
        return {
            'success': True,
            'objects_found': len(all_objects),
            'statistics': self.stats
        }

def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Discover P2 objects from Parallax OBEX')
    parser.add_argument('--categories', nargs='+', default=['spin2', 'pasm2'], 
                       help='Categories to discover (default: spin2 pasm2)')
    parser.add_argument('--output-dir', help='Output directory for results')
    parser.add_argument('--delay', type=float, default=1.0,
                       help='Delay between requests in seconds (default: 1.0)')
    
    args = parser.parse_args()
    
    try:
        discovery = OBEXDiscovery(base_dir=args.output_dir)
        discovery.request_delay = args.delay
        
        result = discovery.run_discovery(categories=args.categories)
        
        if result['success']:
            print(f"\n✅ Discovery completed successfully!")
            print(f"Found {result['objects_found']} P2 objects")
            sys.exit(0)
        else:
            print(f"\n❌ Discovery failed")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n🛑 Discovery interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main(), url)
                            if slug_match:
                                slug = slug_match.group(1)
                                
                                object_data = {
                                    'title': title,
                                    'slug': slug,
                                    'url': url,
                                    'author': author_slug,
                                    'category': 'propeller-2',  # Known to be P2
                                    'discovery_date': datetime.now().isoformat()
                                }
                                
                                objects.append(object_data)
                                self.stats['objects_discovered'] += 1
                                
                        except Exception as e:
                            error = f"Error processing author object link {link}: {e}"
                            self.stats['errors'].append(error)
                            continue
                
                # Stop when we hit another heading (next section)
                if hasattr(current, 'name') and current.name in ['h1', 'h2', 'h3', 'h4']:
                    if 'Propeller 1' in current.get_text():
                        break  # Found P1 section, stop here
            
            print(f"  📦 Found {len(objects)} P2 objects for {author_slug}")
            time.sleep(self.request_delay)
            
        except requests.RequestException as e:
            error = f"Error fetching author page {author_url}: {e}"
            print(f"  ❌ {error}")
            self.stats['errors'].append(error)
        except Exception as e:
            error = f"Error processing author {author_slug}: {e}"
            print(f"  ❌ {error}")
            self.stats['errors'].append(error)
            
        return objects

    def _extract_objects_from_page(self, soup: BeautifulSoup, category: str) -> List[Dict]:
        """Extract object metadata from a category page"""
        objects = []
        
        # Look for object listings - this may need adjustment based on OBEX structure
        object_links = soup.find_all('a', href=re.compile(r'/obex/[^/]+/$'))
        
        for link in object_links:
            try:
                # Extract basic info from category page
                title = link.get_text().strip()
                url = urljoin(self.base_url, link['href'])
                
                # Skip if not a proper object link
                if not title or '/page/' in url:
                    continue
                    
                # Extract object slug for ID extraction
                slug_match = re.search(r'/obex/([^/]+)/$', url)
                if not slug_match:
                    continue
                    
                slug = slug_match.group(1)
                
                # Try to find parent container for more metadata
                container = link.find_parent(['div', 'article', 'section'])
                author = ""
                if container:
                    author_text = container.get_text()
                    # Look for "by Author Name" patterns
                    author_match = re.search(r'by\s+([^,\n]+)', author_text)
                    if author_match:
                        author = author_match.group(1).strip()
                
                object_data = {
                    'title': title,
                    'slug': slug,
                    'url': url,
                    'author': author,
                    'category': category,
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
        """
        Extract detailed metadata from individual object page
        """
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
            
            # Extract description
            description = self._extract_description(soup)
            if description:
                object_data['description'] = description
            
            # Extract author information
            author_info = self._extract_author_info(soup)
            if author_info:
                object_data.update(author_info)
            
            # Extract technical details
            technical_details = self._extract_technical_details(soup)
            if technical_details:
                object_data.update(technical_details)
            
            # Extract related links
            links = self._extract_related_links(soup)
            if links:
                object_data['related_links'] = links
                
            self.stats['objects_validated'] += 1
            time.sleep(self.request_delay)  # Rate limiting
            
        except requests.RequestException as e:
            error = f"Error fetching details for {object_data['url']}: {e}"
            print(f"    ❌ {error}")
            self.stats['errors'].append(error)
        except Exception as e:
            error = f"Error processing details for {object_data['title']}: {e}"
            print(f"    ❌ {error}")
            self.stats['errors'].append(error)
            
        return object_data

    def _extract_object_id(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract Object ID from page"""
        # Look for "Object ID : XXXX" pattern
        text = soup.get_text()
        id_match = re.search(r'Object ID\s*:\s*(\d+)', text, re.IGNORECASE)
        if id_match:
            return id_match.group(1)
        return None

    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract object description"""
        # Look for description in various possible containers
        desc_selectors = [
            '.entry-content p',
            '.object-description',
            '.description',
            'p'
        ]
        
        for selector in desc_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text().strip()
                if len(text) > 50:  # Reasonable description length
                    return text
        return None

    def _extract_author_info(self, soup: BeautifulSoup) -> Dict:
        """Extract detailed author information"""
        author_info = {}
        
        # Look for author patterns in text
        text = soup.get_text()
        
        # Various author patterns
        patterns = [
            r'Author\s*:\s*([^\n]+)',
            r'By\s+([^\n,]+)',
            r'Created by\s+([^\n,]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                author_info['author_detailed'] = match.group(1).strip()
                break
                
        return author_info

    def _extract_technical_details(self, soup: BeautifulSoup) -> Dict:
        """Extract technical specifications"""
        details = {}
        text = soup.get_text()
        
        # Language detection
        languages = []
        if 'SPIN2' in text.upper() or 'SPIN 2' in text.upper():
            languages.append('SPIN2')
        if 'PASM2' in text.upper() or 'PASM 2' in text.upper():
            languages.append('PASM2')
        if 'PASM' in text.upper() and 'PASM2' not in text.upper():
            languages.append('PASM')
        
        if languages:
            details['languages'] = languages
        
        # P2 compatibility check
        if 'P2' in text or 'Propeller 2' in text:
            details['microcontroller'] = ['P2']
        
        return details

    def _extract_related_links(self, soup: BeautifulSoup) -> Dict:
        """Extract related links (GitHub, forum, etc.)"""
        links = {}
        
        # Find all links
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text().lower()
            
            if 'github.com' in href:
                links['github'] = href
            elif 'forums.parallax.com' in href:
                links['forum'] = href
            elif 'documentation' in text or 'docs' in text:
                links['documentation'] = href
                
        return links

    def save_object_metadata(self, object_data: Dict):
        """Save object metadata to individual YAML file"""
        if 'object_id' not in object_data:
            print(f"  ⚠️  No object ID for {object_data['title']}, skipping save")
            return
            
        object_id = object_data['object_id']
        file_path = self.objects_dir / f"{object_id}.yaml"
        
        # Convert to detailed YAML format
        detailed_metadata = self._convert_to_detailed_format(object_data)
        
        try:
            with open(file_path, 'w') as f:
                yaml.dump(detailed_metadata, f, default_flow_style=False, indent=2)
            print(f"  💾 Saved: {file_path}")
        except Exception as e:
            error = f"Error saving {file_path}: {e}"
            print(f"  ❌ {error}")
            self.stats['errors'].append(error)

    def _convert_to_detailed_format(self, object_data: Dict) -> Dict:
        """Convert discovered data to detailed YAML format"""
        return {
            'object_metadata': {
                'object_id': object_data.get('object_id', ''),
                'title': object_data.get('title', ''),
                'author': object_data.get('author_detailed', object_data.get('author', '')),
                'author_username': '',  # To be filled later
                
                'urls': {
                    'obex_page': object_data.get('url', ''),
                    'download_direct': object_data.get('download_url', ''),
                    'forum_discussion': object_data.get('related_links', {}).get('forum', ''),
                    'github_repo': object_data.get('related_links', {}).get('github', ''),
                    'documentation': object_data.get('related_links', {}).get('documentation', '')
                },
                
                'technical_details': {
                    'languages': object_data.get('languages', []),
                    'microcontroller': object_data.get('microcontroller', ['P2']),
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
                
                'architecture': {
                    'multi_cog': False,  # Default, to be analyzed
                    'cog_count': 1,
                    'memory_requirements': {
                        'hub_ram': '',
                        'cog_ram': ''
                    },
                    'performance_notes': ''
                },
                
                'compatibility': {
                    'p2_chip_versions': ['all'],
                    'tested_platforms': [],
                    'known_issues': [],
                    'dependencies': []
                },
                
                'community': {
                    'forum_posts': [],
                    'user_reviews': [],
                    'modification_notes': [],
                    'related_objects': []
                },
                
                'metadata': {
                    'discovery_date': object_data.get('discovery_date', datetime.now().isoformat()),
                    'last_verified': datetime.now().isoformat(),
                    'extraction_status': 'discovered',
                    'kb_integration': 'none',
                    'quality_score': 5  # Default, to be assessed
                },
                
                'notes': {
                    'extraction_notes': f"Auto-discovered from {object_data.get('category', 'unknown')} category",
                    'analysis_notes': '',
                    'integration_todo': []
                }
            }
        }

    def _categorize_object(self, object_data: Dict) -> str:
        """Automatically categorize object based on title and description"""
        title = object_data.get('title', '').lower()
        description = object_data.get('description', '').lower()
        text = f"{title} {description}"
        
        # Category detection rules
        if any(word in text for word in ['driver', 'interface', 'protocol']):
            return 'drivers'
        elif any(word in text for word in ['sensor', 'imu', 'compass', 'ping']):
            return 'sensors'
        elif any(word in text for word in ['display', 'matrix', 'led', 'nextion']):
            return 'display'
        elif any(word in text for word in ['motor', 'servo', 'stepper', 'bldc']):
            return 'motors'
        elif any(word in text for word in ['serial', 'uart', 'communication', 'wifi']):
            return 'communication'
        elif any(word in text for word in ['audio', 'sound', 'synth', 'fm']):
            return 'audio'
        elif any(word in text for word in ['demo', 'example', 'test']):
            return 'demos'
        elif any(word in text for word in ['tool', 'utility', 'library']):
            return 'tools'
        else:
            return 'misc'

    def _generate_tags(self, object_data: Dict) -> List[str]:
        """Generate tags based on object data"""
        tags = []
        title = object_data.get('title', '').lower()
        description = object_data.get('description', '').lower()
        text = f"{title} {description}"
        
        # Common tag patterns
        tag_patterns = {
            'serial': ['serial', 'uart', 'communication'],
            'display': ['display', 'led', 'matrix', 'screen'],
            'sensor': ['sensor', 'imu', 'compass', 'ping'],
            'motor': ['motor', 'servo', 'stepper'],
            'driver': ['driver', 'interface'],
            'wifi': ['wifi', 'esp32', 'wireless'],
            'audio': ['audio', 'sound', 'synth'],
            'demo': ['demo', 'example', 'test']
        }
        
        for tag, patterns in tag_patterns.items():
            if any(pattern in text for pattern in patterns):
                tags.append(tag)
                
        return tags

    def update_master_index(self, objects: List[Dict]):
        """Update the master index with discovered objects"""
        print(f"📝 Updating master index with {len(objects)} objects")
        
        try:
            # Load existing index or create new
            if self.master_index_path.exists():
                with open(self.master_index_path, 'r') as f:
                    index = yaml.safe_load(f)
            else:
                # Use template structure
                index = {
                    'metadata': {
                        'generated_date': datetime.now().isoformat(),
                        'last_updated': datetime.now().isoformat(),
                        'total_objects': 0,
                        'sources': [
                            "https://obex.parallax.com/code-language/spin2/",
                            "https://obex.parallax.com/code-language/pasm2/"
                        ],
                        'schema_version': "1.0"
                    },
                    'objects': [],
                    'indices': {
                        'by_author': {},
                        'by_category': {},
                        'by_hardware': {},
                        'by_language': {}
                    },
                    'statistics': {
                        'objects_by_category': {},
                        'objects_by_author': {},
                        'objects_by_language': {},
                        'most_active_authors': [],
                        'newest_objects': [],
                        'most_downloaded': []
                    },
                    'discovery_status': {
                        'categories_processed': [],
                        'pages_processed': self.stats['pages_processed'],
                        'objects_discovered': self.stats['objects_discovered'],
                        'objects_validated': self.stats['objects_validated'],
                        'errors_encountered': len(self.stats['errors']),
                        'last_discovery_run': datetime.now().isoformat()
                    }
                }
            
            # Update metadata
            index['metadata']['last_updated'] = datetime.now().isoformat()
            
            # Add objects to index
            existing_ids = {obj.get('object_id') for obj in index.get('objects', [])}
            
            for obj in objects:
                if obj.get('object_id') and obj['object_id'] not in existing_ids:
                    index_entry = {
                        'object_id': obj['object_id'],
                        'title': obj.get('title', ''),
                        'author': obj.get('author_detailed', obj.get('author', '')),
                        'url': obj.get('url', ''),
                        'download_url': obj.get('download_url', ''),
                        'languages': obj.get('languages', []),
                        'microcontroller': obj.get('microcontroller', ['P2']),
                        'category': self._categorize_object(obj),
                        'tags': self._generate_tags(obj),
                        'discovery_date': obj.get('discovery_date', datetime.now().isoformat())
                    }
                    
                    index['objects'].append(index_entry)
            
            # Update statistics
            index['metadata']['total_objects'] = len(index['objects'])
            index['discovery_status'].update({
                'pages_processed': self.stats['pages_processed'],
                'objects_discovered': self.stats['objects_discovered'],
                'objects_validated': self.stats['objects_validated'],
                'errors_encountered': len(self.stats['errors']),
                'last_discovery_run': datetime.now().isoformat()
            })
            
            # Save updated index
            with open(self.master_index_path, 'w') as f:
                yaml.dump(index, f, default_flow_style=False, indent=2)
                
            print(f"✅ Master index updated: {len(index['objects'])} total objects")
            
        except Exception as e:
            error = f"Error updating master index: {e}"
            print(f"❌ {error}")
            self.stats['errors'].append(error)

    def run_discovery(self, categories: List[str] = None) -> Dict:
        """
        Run complete discovery process
        """
        if categories is None:
            categories = ['spin2', 'pasm2', 'propeller-2']
            
        print(f"🚀 Starting OBEX discovery for categories: {categories}")
        print(f"📁 Output directory: {self.base_dir}")
        
        all_objects = []
        
        for category in categories:
            print(f"\n{'='*60}")
            print(f"Processing category: {category.upper()}")
            print(f"{'='*60}")
            
            # Discover objects in category
            category_objects = self.discover_category_objects(category)
            
            # Extract detailed metadata for each object
            detailed_objects = []
            for i, obj in enumerate(category_objects, 1):
                print(f"📋 Processing {i}/{len(category_objects)}: {obj['title']}")
                detailed_obj = self.extract_detailed_metadata(obj)
                detailed_objects.append(detailed_obj)
                
                # Save individual object file
                self.save_object_metadata(detailed_obj)
            
            all_objects.extend(detailed_objects)
        
        # Update master index
        self.update_master_index(all_objects)
        
        # Print final statistics
        print(f"\n{'='*60}")
        print("🎯 DISCOVERY COMPLETE")
        print(f"{'='*60}")
        print(f"📄 Pages processed: {self.stats['pages_processed']}")
        print(f"📦 Objects discovered: {self.stats['objects_discovered']}")
        print(f"✅ Objects validated: {self.stats['objects_validated']}")
        print(f"❌ Errors encountered: {len(self.stats['errors'])}")
        
        if self.stats['errors']:
            print(f"\n⚠️  Error Summary:")
            for error in self.stats['errors'][:10]:  # Show first 10 errors
                print(f"  • {error}")
            if len(self.stats['errors']) > 10:
                print(f"  ... and {len(self.stats['errors']) - 10} more errors")
        
        return {
            'success': True,
            'objects_found': len(all_objects),
            'statistics': self.stats
        }

def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Discover P2 objects from Parallax OBEX')
    parser.add_argument('--categories', nargs='+', default=['spin2', 'pasm2'], 
                       help='Categories to discover (default: spin2 pasm2)')
    parser.add_argument('--output-dir', help='Output directory for results')
    parser.add_argument('--delay', type=float, default=1.0,
                       help='Delay between requests in seconds (default: 1.0)')
    
    args = parser.parse_args()
    
    try:
        discovery = OBEXDiscovery(base_dir=args.output_dir)
        discovery.request_delay = args.delay
        
        result = discovery.run_discovery(categories=args.categories)
        
        if result['success']:
            print(f"\n✅ Discovery completed successfully!")
            print(f"Found {result['objects_found']} P2 objects")
            sys.exit(0)
        else:
            print(f"\n❌ Discovery failed")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n🛑 Discovery interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()