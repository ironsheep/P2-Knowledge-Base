#!/usr/bin/env python3
"""
Scrape OBEX pages for GitHub repository URLs and version information.
Updates YAML files with repo URLs, version info, and upload dates.
"""

import yaml
import re
import time
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_obex_page(url):
    """
    Scrape an OBEX page for GitHub repo URL and version info.
    Returns dict with repo_url, version, upload_date
    """
    result = {
        'github_repo': '',
        'version': '',
        'upload_date': '',
        'scrape_timestamp': datetime.now().isoformat()
    }
    
    try:
        # Add delay to be polite to server
        time.sleep(0.5)
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for GitHub links
        github_patterns = [
            r'github\.com/[\w-]+/[\w-]+',
            r'https?://github\.com/[\w-]+/[\w-]+',
        ]
        
        text = soup.get_text()
        links = soup.find_all('a', href=True)
        
        # Search in links first
        for link in links:
            href = link.get('href', '')
            if 'github.com' in href:
                # Clean up the URL
                match = re.search(r'(https?://github\.com/[\w-]+/[\w-]+)', href)
                if match:
                    result['github_repo'] = match.group(1)
                    break
        
        # If not found in links, search in text
        if not result['github_repo']:
            for pattern in github_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    url_part = match.group(0)
                    if not url_part.startswith('http'):
                        url_part = 'https://' + url_part
                    result['github_repo'] = url_part
                    break
        
        # Look for version information
        version_patterns = [
            r'Version[:\s]+([vV]?\d+\.\d+(?:\.\d+)?)',
            r'v\d+\.\d+(?:\.\d+)?',
            r'\(repository Latest\)',
            r'Latest Version[:\s]+([vV]?\d+\.\d+(?:\.\d+)?)',
        ]
        
        for pattern in version_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if 'repository Latest' in match.group(0):
                    result['version'] = '(repository Latest)'
                else:
                    result['version'] = match.group(0) if match.lastindex is None else match.group(1)
                break
        
        # Look for upload date
        date_patterns = [
            r'Uploaded[:\s]+(\d{4}-\d{2}-\d{2})',
            r'Created[:\s]+(\d{4}-\d{2}-\d{2})',
            r'Date[:\s]+(\d{4}-\d{2}-\d{2})',
            r'(\d{4}-\d{2}-\d{2})',  # Generic date pattern
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                result['upload_date'] = match.group(1) if match.lastindex else match.group(0)
                break
        
        return result
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return result


def update_yaml_file(yaml_path, scraped_data):
    """
    Update a YAML file with scraped repository and version data.
    """
    try:
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Update URLs section
        if 'urls' in data['object_metadata']:
            data['object_metadata']['urls']['github_repo'] = scraped_data['github_repo']
        
        # Update or create version_tracking section
        if 'version_tracking' not in data['object_metadata']:
            data['object_metadata']['version_tracking'] = {}
        
        data['object_metadata']['version_tracking'].update({
            'obex_version': scraped_data['version'],
            'obex_upload_date': scraped_data['upload_date'],
            'last_scraped': scraped_data['scrape_timestamp'],
            'has_github_repo': bool(scraped_data['github_repo'])
        })
        
        # Update technical_details version if we found one
        if scraped_data['version'] and 'technical_details' in data['object_metadata']:
            data['object_metadata']['technical_details']['version'] = scraped_data['version']
        
        # Write back
        with open(yaml_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        
        return True
        
    except Exception as e:
        print(f"Error updating {yaml_path}: {e}")
        return False


def main():
    """
    Main function to process all OBEX objects.
    """
    objects_dir = Path('engineering/knowledge-base/P2/community/obex/objects')
    
    # Get all YAML files except template
    yaml_files = sorted([f for f in objects_dir.glob('*.yaml') if f.name != '_template.yaml'])
    
    print(f"Found {len(yaml_files)} OBEX objects to process")
    print("-" * 50)
    
    stats = {
        'total': len(yaml_files),
        'with_repo': 0,
        'with_version': 0,
        'processed': 0,
        'errors': 0
    }
    
    for yaml_path in yaml_files:
        object_id = yaml_path.stem
        
        # Read YAML to get OBEX page URL
        try:
            with open(yaml_path, 'r') as f:
                data = yaml.safe_load(f)
            
            obex_url = data['object_metadata']['urls'].get('obex_page', '')
            
            if not obex_url:
                print(f"⚠️  {object_id}: No OBEX page URL")
                stats['errors'] += 1
                continue
            
            print(f"Processing {object_id}: {data['object_metadata']['title'][:50]}...")
            
            # Scrape the OBEX page
            scraped = scrape_obex_page(obex_url)
            
            # Update the YAML file
            if update_yaml_file(yaml_path, scraped):
                stats['processed'] += 1
                if scraped['github_repo']:
                    stats['with_repo'] += 1
                    print(f"  ✅ Found repo: {scraped['github_repo']}")
                else:
                    print(f"  ℹ️  No GitHub repo found")
                
                if scraped['version']:
                    stats['with_version'] += 1
                    print(f"  📌 Version: {scraped['version']}")
            else:
                stats['errors'] += 1
                print(f"  ❌ Failed to update YAML")
            
        except Exception as e:
            print(f"❌ {object_id}: {e}")
            stats['errors'] += 1
    
    # Print summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("-" * 50)
    print(f"Total objects: {stats['total']}")
    print(f"Successfully processed: {stats['processed']}")
    print(f"Objects with GitHub repos: {stats['with_repo']}")
    print(f"Objects with version info: {stats['with_version']}")
    print(f"Errors: {stats['errors']}")
    print(f"Repository coverage: {stats['with_repo']/stats['total']*100:.1f}%")


if __name__ == "__main__":
    main()