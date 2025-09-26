#!/usr/bin/env python3
"""
Extract and document the master tag taxonomy from Quick Bytes index pages.
This establishes the canonical categorization system.
"""

import requests
from bs4 import BeautifulSoup
import yaml
import time
from collections import defaultdict

def extract_master_tags():
    """Extract all unique tags from index pages"""
    
    all_tags = set()
    tag_to_quickbytes = defaultdict(list)
    
    print("Extracting master tag taxonomy from Quick Bytes index...")
    
    # Scrape both index pages
    for page_num in [1, 2]:
        url = f"https://www.parallax.com/propeller-2/quick-bytes/p2-quick-bytes-index/"
        if page_num > 1:
            url += f"page/{page_num}/"
            
        print(f"\nProcessing page {page_num}: {url}")
        
        try:
            time.sleep(1)
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Method 1: Find all tag links (clickable tags)
            tag_links = soup.find_all('a', {'rel': 'tag'})
            tag_links += soup.find_all('a', {'rel': 'category tag'})
            
            # Method 2: Look for tag containers
            tag_containers = soup.find_all('div', class_='tags')
            tag_containers += soup.find_all('div', class_='entry-tags')
            tag_containers += soup.find_all('span', class_='tags-links')
            
            for container in tag_containers:
                tag_links += container.find_all('a')
            
            # Extract unique tags
            page_tags = set()
            for link in tag_links:
                tag_text = link.get_text(strip=True)
                # Filter out generic/meta tags
                if tag_text and tag_text not in ['Quick Bytes', 'Propeller 2', 'P2']:
                    all_tags.add(tag_text)
                    page_tags.add(tag_text)
                    
                    # Try to associate with Quick Byte title
                    article = link.find_parent('article') or link.find_parent('div', class_='entry')
                    if article:
                        title_elem = article.find('h2') or article.find('h3')
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            tag_to_quickbytes[tag_text].append(title)
            
            print(f"Found {len(page_tags)} unique tags on page {page_num}")
            
        except Exception as e:
            print(f"Error processing page {page_num}: {e}")
    
    return sorted(all_tags), dict(tag_to_quickbytes)


def generate_tag_taxonomy(tags, tag_mappings):
    """Generate taxonomy YAML file"""
    
    # Categorize tags into groups
    categories = {
        'hardware_interfaces': [],
        'communication': [],
        'sensors': [],
        'displays': [],
        'development': [],
        'applications': [],
        'platforms': [],
        'components': []
    }
    
    # Categorization rules
    for tag in tags:
        tag_lower = tag.lower()
        
        if any(x in tag_lower for x in ['adc', 'dac', 'i2c', 'spi', 'uart', 'serial', 'protocol']):
            categories['communication'].append(tag)
        elif any(x in tag_lower for x in ['sensor', 'temperature', 'humidity', 'rtc', 'gps']):
            categories['sensors'].append(tag)
        elif any(x in tag_lower for x in ['lcd', 'led', 'vga', 'hdmi', 'display', 'visual']):
            categories['displays'].append(tag)
        elif any(x in tag_lower for x in ['tool', 'development', 'debug', 'util']):
            categories['development'].append(tag)
        elif any(x in tag_lower for x in ['motor', 'servo', 'pwm', 'control']):
            categories['hardware_interfaces'].append(tag)
        elif any(x in tag_lower for x in ['iot', 'wireless', 'wifi', 'bluetooth']):
            categories['communication'].append(tag)
        elif any(x in tag_lower for x in ['raspberry', 'pi', 'arduino']):
            categories['platforms'].append(tag)
        elif any(x in tag_lower for x in ['gaming', 'audio', 'robot']):
            categories['applications'].append(tag)
        else:
            categories['components'].append(tag)
    
    # Remove duplicates and sort
    for cat in categories:
        categories[cat] = sorted(list(set(categories[cat])))
    
    taxonomy = {
        'tag_taxonomy': {
            'version': '1.0',
            'last_updated': '2025-09-26',
            'total_tags': len(tags),
            'source': 'Quick Bytes Index Pages',
            
            'master_tags': tags,
            
            'categorized_tags': categories,
            
            'tag_descriptions': {
                'ADC / DAC': 'Analog-to-Digital and Digital-to-Analog conversion',
                'Audio': 'Sound generation and processing',
                'Development Tools': 'Programming and debugging utilities',
                'Environmental': 'Temperature, humidity, pressure sensors',
                'Gaming': 'Game development and controllers',
                'Human Input': 'Keyboards, buttons, touchscreens',
                'IoT': 'Internet of Things connectivity',
                'LCD': 'Liquid Crystal Displays',
                'LED': 'Light Emitting Diode control',
                'Memory': 'EEPROM, Flash, SD cards',
                'Motor Control': 'DC, stepper, servo motors',
                'Protocols': 'Communication protocols (I2C, SPI, UART)',
                'Raspberry Pi': 'Integration with Raspberry Pi',
                'Robotics': 'Robot control and sensors',
                'RTC': 'Real-Time Clock modules',
                'Sensors': 'Various sensor types',
                'Smart Pins': 'P2 Smart Pin features',
                'Utility': 'Helper functions and tools',
                'VGA / HDMI': 'Video output interfaces',
                'Visual': 'Graphics and visualization',
                'Wireless': 'WiFi, Bluetooth, RF communication'
            },
            
            'usage_stats': {}
        }
    }
    
    # Add usage statistics
    for tag, quickbytes in tag_mappings.items():
        if tag in tags:
            taxonomy['tag_taxonomy']['usage_stats'][tag] = {
                'count': len(quickbytes),
                'examples': quickbytes[:3]  # First 3 examples
            }
    
    return taxonomy


def main():
    """Main function"""
    
    print("=" * 60)
    print("QUICK BYTES TAG TAXONOMY EXTRACTION")
    print("=" * 60)
    
    # Extract tags
    tags, mappings = extract_master_tags()
    
    print(f"\n✅ Found {len(tags)} unique tags total")
    
    # Display tags
    print("\nMaster Tag List:")
    print("-" * 40)
    for i, tag in enumerate(tags, 1):
        count = len(mappings.get(tag, []))
        print(f"{i:2}. {tag:<25} ({count} Quick Bytes)")
    
    # Generate taxonomy
    taxonomy = generate_tag_taxonomy(tags, mappings)
    
    # Save to file
    output_file = 'quick-bytes-tag-taxonomy.yaml'
    with open(output_file, 'w') as f:
        yaml.dump(taxonomy, f, default_flow_style=False, sort_keys=False)
    
    print(f"\n✅ Tag taxonomy saved to {output_file}")
    
    # Print categorization summary
    print("\nTag Categories:")
    print("-" * 40)
    for category, tags in taxonomy['tag_taxonomy']['categorized_tags'].items():
        if tags:
            print(f"{category}: {len(tags)} tags")
            for tag in tags[:3]:
                print(f"  - {tag}")
            if len(tags) > 3:
                print(f"  ... and {len(tags)-3} more")
    
    return taxonomy


if __name__ == "__main__":
    main()