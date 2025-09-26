#!/usr/bin/env python3
"""
Scrape Parallax Quick Bytes for P2 Knowledge Base integration.
Handles both code-based tutorials and procedural/setup guides.
"""

import requests
from bs4 import BeautifulSoup
import yaml
import json
import time
from pathlib import Path
from datetime import datetime
import re

class QuickBytesScraper:
    def __init__(self, output_dir='engineering/knowledge-base/P2/community/quick-bytes'):
        self.output_dir = Path(output_dir)
        self.base_url = 'https://www.parallax.com'
        self.quick_bytes_data = {}
        self.stats = {
            'total': 0,
            'with_code': 0,
            'without_code': 0,
            'with_multiple_downloads': 0,
            'procedural': 0,
            'unique_tags': set(),
            'unique_authors': set()
        }
        
    def scrape_index_pages(self):
        """Scrape all index pages to get complete Quick Bytes list"""
        all_entries = []
        
        for page_num in [1, 2]:  # Page 3 returns empty
            url = f"{self.base_url}/propeller-2/quick-bytes/p2-quick-bytes-index/"
            if page_num > 1:
                url += f"page/{page_num}/"
                
            print(f"Scraping index page {page_num}: {url}")
            
            try:
                time.sleep(1)  # Be polite
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find Quick Bytes entries
                entries = soup.find_all('article', class_='quick-byte-entry')
                if not entries:
                    # Alternative structure
                    entries = soup.find_all('div', class_='entry-content')
                
                for entry in entries:
                    data = self.extract_index_entry(entry)
                    if data:
                        all_entries.append(data)
                        
            except Exception as e:
                print(f"Error scraping index page {page_num}: {e}")
                
        return all_entries
    
    def extract_index_entry(self, entry_html):
        """Extract Quick Byte data from index page entry"""
        data = {}
        
        try:
            # Extract title and URL
            title_elem = entry_html.find('h2') or entry_html.find('h3')
            if title_elem and title_elem.find('a'):
                data['title'] = title_elem.get_text(strip=True)
                data['url'] = title_elem.find('a')['href']
                
                # Extract slug from URL
                slug_match = re.search(r'/([^/]+)/$', data['url'])
                if slug_match:
                    data['slug'] = slug_match.group(1)
            
            # Extract date
            date_elem = entry_html.find('time')
            if date_elem:
                data['date'] = date_elem.get('datetime', '')
                
            # Extract author
            author_elem = entry_html.find('span', class_='author')
            if author_elem:
                data['author'] = author_elem.get_text(strip=True)
                
            # Extract tags/categories
            tags = []
            tag_elems = entry_html.find_all('a', {'rel': 'category tag'})
            if not tag_elems:
                tag_elems = entry_html.find_all('a', {'rel': 'tag'})
            
            for tag in tag_elems:
                tag_text = tag.get_text(strip=True)
                if tag_text and tag_text not in ['Quick Bytes', 'Propeller 2']:
                    tags.append(tag_text)
            data['tags'] = tags
                
            return data if data.get('title') else None
            
        except Exception as e:
            print(f"Error extracting entry: {e}")
            return None
    
    def scrape_individual_page(self, url):
        """Extract detailed data from individual Quick Byte page"""
        print(f"Scraping: {url}")
        
        try:
            time.sleep(1.5)  # Be extra polite for detailed pages
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            data = {
                'url': url,
                'scraped_timestamp': datetime.now().isoformat()
            }
            
            # Extract title
            title = soup.find('h1', class_='entry-title')
            if title:
                data['title'] = title.get_text(strip=True)
            
            # Extract description
            desc = soup.find('div', class_='entry-content')
            if desc:
                # Get first paragraph as description
                first_p = desc.find('p')
                if first_p:
                    data['description'] = first_p.get_text(strip=True)
            
            # Extract YouTube video
            iframe = soup.find('iframe', src=re.compile(r'youtube\.com|youtu\.be'))
            if iframe:
                data['youtube_url'] = iframe.get('src', '')
                # Try to extract video ID
                video_match = re.search(r'embed/([^?]+)', data['youtube_url'])
                if video_match:
                    data['youtube_id'] = video_match.group(1)
            
            # Extract tags (more comprehensive)
            data['tags'] = []
            
            # Method 1: Look for tag links
            tag_container = soup.find('div', class_='entry-tags') or soup.find('div', class_='tags')
            if tag_container:
                for tag_link in tag_container.find_all('a'):
                    tag_text = tag_link.get_text(strip=True)
                    if tag_text not in ['Quick Bytes', 'Propeller 2'] and tag_text not in data['tags']:
                        data['tags'].append(tag_text)
            
            # Method 2: Look for category links
            for link in soup.find_all('a', {'rel': re.compile(r'category|tag')}):
                tag_text = link.get_text(strip=True)
                if tag_text not in ['Quick Bytes', 'Propeller 2'] and tag_text not in data['tags']:
                    data['tags'].append(tag_text)
            
            # Determine if this is procedural/setup (no code)
            data['quick_byte_type'] = self.determine_type(soup, data.get('title', ''))
            
            # Extract source code links (may be multiple, or none for procedural)
            data['source_code_urls'] = []
            
            # Find all potential download links
            download_patterns = [
                r'Download.*Code',
                r'Example.*Code', 
                r'Source.*Code',
                r'.*\.zip',
                r'Code.*Download',
                r'Sample.*Code',
                r'Demo.*Code'
            ]
            
            for pattern in download_patterns:
                links = soup.find_all('a', text=re.compile(pattern, re.I))
                for link in links:
                    href = link.get('href', '')
                    link_text = link.get_text(strip=True)
                    if href and 'package' in href:  # Parallax package URLs
                        data['source_code_urls'].append({
                            'url': href,
                            'description': link_text
                        })
            
            # Remove duplicates
            seen_urls = set()
            unique_downloads = []
            for item in data['source_code_urls']:
                if item['url'] not in seen_urls:
                    seen_urls.add(item['url'])
                    unique_downloads.append(item)
            data['source_code_urls'] = unique_downloads
            
            data['has_code'] = len(data['source_code_urls']) > 0
                
            # Extract hardware/BOM
            data['hardware'] = []
            bom_section = soup.find(text=re.compile(r'Bill of Materials|Hardware|Requirements', re.I))
            if bom_section:
                parent = bom_section.find_parent()
                if parent:
                    ul = parent.find_next('ul')
                    if ul:
                        for li in ul.find_all('li'):
                            part = li.get_text(strip=True)
                            data['hardware'].append(part)
            
            # Extract author and date
            meta = soup.find('div', class_='entry-meta')
            if meta:
                author = meta.find('span', class_='author')
                if author:
                    data['author'] = author.get_text(strip=True)
                    
                date = meta.find('time')
                if date:
                    data['date'] = date.get('datetime', '')
            
            # Update stats
            self.update_stats(data)
            
            return data
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    def determine_type(self, soup, title):
        """Determine if Quick Byte is procedural/setup or code-based"""
        procedural_keywords = [
            'setup', 'install', 'getting started', 'introduction',
            'overview', 'configuration', 'how to set up', 'preparing',
            'first steps', 'quickstart', 'quick start'
        ]
        
        title_lower = title.lower()
        
        # Check title for procedural keywords
        for keyword in procedural_keywords:
            if keyword in title_lower:
                return 'procedural'
        
        # Check for absence of code blocks
        code_blocks = soup.find_all('pre') + soup.find_all('code')
        if len(code_blocks) < 2:  # Very few code blocks suggests procedural
            return 'procedural'
            
        return 'tutorial'
    
    def generate_code_note(self, data):
        """Generate descriptive note about code availability"""
        if not data.get('has_code'):
            if data.get('quick_byte_type') == 'procedural':
                return 'Procedural/setup guide - no code downloads'
            else:
                return 'No downloadable code provided'
        else:
            count = len(data.get('source_code_urls', []))
            if count > 1:
                return f'Multiple code downloads available ({count} files)'
            else:
                return 'Single code download available'
    
    def update_stats(self, data):
        """Update statistics from scraped data"""
        self.stats['total'] += 1
        
        if data.get('has_code'):
            self.stats['with_code'] += 1
            if len(data.get('source_code_urls', [])) > 1:
                self.stats['with_multiple_downloads'] += 1
        else:
            self.stats['without_code'] += 1
            
        if data.get('quick_byte_type') == 'procedural':
            self.stats['procedural'] += 1
            
        # Track unique tags
        for tag in data.get('tags', []):
            self.stats['unique_tags'].add(tag)
            
        # Track unique authors
        if data.get('author'):
            self.stats['unique_authors'].add(data['author'])
    
    def generate_yaml(self, data, quick_byte_id):
        """Generate YAML file for a Quick Byte"""
        yaml_data = {
            'quick_byte_metadata': {
                'quick_byte_id': quick_byte_id,
                'title': data.get('title', ''),
                'slug': data.get('slug', ''),
                'author': data.get('author', ''),
                'date': data.get('date', ''),
                'quick_byte_type': data.get('quick_byte_type', 'tutorial'),
                
                'urls': {
                    'parallax_page': data.get('url', ''),
                    'youtube_video': data.get('youtube_url', ''),
                    'youtube_id': data.get('youtube_id', ''),
                    'source_code_downloads': data.get('source_code_urls', [])  # List of download objects
                },
                
                'tags': data.get('tags', []),
                
                'code_availability': {
                    'has_code': data.get('has_code', False),
                    'download_count': len(data.get('source_code_urls', [])),
                    'code_type': 'downloadable' if data.get('has_code') else 'none',
                    'note': self.generate_code_note(data)
                },
                
                'hardware': data.get('hardware', []),
                
                'content': {
                    'description': data.get('description', ''),
                    'content_type': data.get('quick_byte_type', 'tutorial')
                },
                
                'relationships': {
                    'obex_objects': [],
                    'related_quickbytes': [],
                    'documentation_refs': []
                },
                
                'metadata': {
                    'ingestion_date': datetime.now().strftime('%Y-%m-%d'),
                    'last_verified': datetime.now().strftime('%Y-%m-%d'),
                    'last_scraped': data.get('scraped_timestamp', ''),
                    'status': 'complete'
                }
            }
        }
        
        return yaml_data
    
    def cross_validate_sources(self, index_entries, main_page_entries):
        """Cross-validate entries from index vs main page"""
        index_urls = {e['url'] for e in index_entries if 'url' in e}
        main_urls = {e['url'] for e in main_page_entries if 'url' in e}
        
        only_in_index = index_urls - main_urls
        only_in_main = main_urls - index_urls
        in_both = index_urls & main_urls
        
        print("\n=== Cross-Validation Report ===")
        print(f"Total unique Quick Bytes: {len(index_urls | main_urls)}")
        print(f"In both sources: {len(in_both)}")
        print(f"Only in index: {len(only_in_index)}")
        print(f"Only in main page: {len(only_in_main)}")
        
        if only_in_index:
            print("\nURLs only in index:")
            for url in list(only_in_index)[:5]:
                print(f"  - {url}")
                
        if only_in_main:
            print("\nURLs only in main page:")
            for url in list(only_in_main)[:5]:
                print(f"  - {url}")
        
        return list(index_urls | main_urls)
    
    def print_summary(self):
        """Print scraping summary statistics"""
        print("\n" + "=" * 50)
        print("QUICK BYTES SCRAPING SUMMARY")
        print("-" * 50)
        print(f"Total Quick Bytes processed: {self.stats['total']}")
        print(f"With downloadable code: {self.stats['with_code']}")
        print(f"  - With multiple downloads: {self.stats['with_multiple_downloads']}")
        print(f"Without code (procedural): {self.stats['without_code']}")
        print(f"Identified as procedural/setup: {self.stats['procedural']}")
        print(f"Unique tags discovered: {len(self.stats['unique_tags'])}")
        print(f"Unique authors: {len(self.stats['unique_authors'])}")
        
        if self.stats['unique_tags']:
            print("\nTop tags:")
            for tag in sorted(self.stats['unique_tags'])[:10]:
                print(f"  - {tag}")
        
        print("\nCode availability breakdown:")
        if self.stats['total'] > 0:
            code_pct = (self.stats['with_code'] / self.stats['total']) * 100
            print(f"  {code_pct:.1f}% have downloadable code")
            print(f"  {100-code_pct:.1f}% are procedural/setup guides")


def main():
    """Main function to run Quick Bytes scraping"""
    scraper = QuickBytesScraper()
    
    print("Starting Quick Bytes discovery...")
    
    # Step 1: Scrape index pages
    print("\n1. Scraping index pages...")
    index_entries = scraper.scrape_index_pages()
    print(f"Found {len(index_entries)} entries in index")
    
    # For now, we'll use index as primary source
    # Could add main page scraping for validation
    
    # Step 2: Process first 3 Quick Bytes as test
    print("\n2. Processing sample Quick Bytes...")
    
    for i, entry in enumerate(index_entries[:3]):
        if 'url' in entry:
            print(f"\nProcessing {i+1}/3: {entry.get('title', 'Unknown')}")
            
            # Scrape detailed page
            detailed = scraper.scrape_individual_page(entry['url'])
            
            if detailed:
                # Merge with index data
                detailed.update(entry)
                
                # Generate YAML
                quick_byte_id = f"QB{i+1:04d}"
                yaml_data = scraper.generate_yaml(detailed, quick_byte_id)
                
                # Print sample YAML
                if i == 0:
                    print("\nSample YAML output:")
                    print("-" * 40)
                    print(yaml.dump(yaml_data, default_flow_style=False, sort_keys=False)[:500])
                    print("...")
    
    # Print summary
    scraper.print_summary()
    
    print("\n✅ Test scraping complete!")
    print("Ready to process all Quick Bytes when approved.")


if __name__ == "__main__":
    main()