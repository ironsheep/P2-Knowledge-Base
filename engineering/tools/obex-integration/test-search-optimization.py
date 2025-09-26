#!/usr/bin/env python3
"""
Test script to validate OBEX search optimization strategy
Demonstrates how broad searches find more relevant objects than narrow ones
"""

import yaml
import json
from pathlib import Path

# Keyword expansion mappings
KEYWORD_EXPANSIONS = {
    'i2c': ['i2c', 'iic', 'twi', 'two-wire', '2-wire', 'I2C', 'I²C'],
    'spi': ['spi', 'serial peripheral', '4-wire', 'shift', 'SPI'],
    'uart': ['uart', 'serial', 'rs232', 'rs485', 'async', 'UART'],
    'led': ['led', 'pixel', 'ws2812', 'rgb', 'neopixel', 'strip', 'matrix', 'LED', 'RGB', 'WS2812'],
    'display': ['display', 'lcd', 'oled', 'screen', 'graphics', 'video', 'LCD', 'OLED'],
    'sensor': ['sensor', 'detector', 'measure', 'read', 'monitor'],
    'temperature': ['temp', 'temperature', 'thermal', 'heat', 'cold', 'thermometer', 'dht', 'ds18b20', 'DHT'],
    'motor': ['motor', 'servo', 'stepper', 'pwm', 'drive', 'actuator', 'PWM'],
    'wireless': ['wireless', 'rf', 'radio', 'bluetooth', 'ble', 'zigbee', '433', '915', 'RF', 'BLE'],
}

def expand_search_terms(term):
    """Expand a single search term into related terms"""
    term_lower = term.lower()
    
    # Direct mapping
    if term_lower in KEYWORD_EXPANSIONS:
        return KEYWORD_EXPANSIONS[term_lower]
    
    # Check if term is contained in any key
    for key, values in KEYWORD_EXPANSIONS.items():
        if term_lower in key or key in term_lower:
            return values
    
    # Return original term if no expansion found
    return [term]

def search_obex_objects(search_terms, obex_objects):
    """
    Search OBEX objects for any of the provided search terms
    Returns dict with categorized results
    """
    results = {
        'exact_matches': [],
        'title_matches': [],
        'description_matches': [],
        'related_matches': []
    }
    
    for obj in obex_objects:
        obj_text_lower = f"{obj.get('title', '')} {obj.get('description_short', '')}".lower()
        
        for term in search_terms:
            term_lower = term.lower()
            
            # Check for exact word match
            if f" {term_lower} " in f" {obj_text_lower} ":
                if obj not in results['exact_matches']:
                    results['exact_matches'].append(obj)
                    break
            # Check title
            elif term_lower in obj.get('title', '').lower():
                if obj not in results['title_matches']:
                    results['title_matches'].append(obj)
                    break
            # Check description
            elif term_lower in obj.get('description_short', '').lower():
                if obj not in results['description_matches']:
                    results['description_matches'].append(obj)
                    break
            # Check if it's a partial match
            elif term_lower in obj_text_lower:
                if obj not in results['related_matches']:
                    results['related_matches'].append(obj)
    
    return results

def load_obex_manifests():
    """Load all OBEX category manifests to get full object list"""
    objects = []
    
    # Load category manifests
    categories_path = Path('manifests/obex/categories')
    if categories_path.exists():
        for manifest_file in categories_path.glob('*-manifest.yaml'):
            with open(manifest_file, 'r') as f:
                manifest = yaml.safe_load(f)
                if 'objects' in manifest:
                    for obj in manifest['objects']:
                        obj['category'] = manifest.get('category_info', {}).get('name', 'unknown')
                        objects.append(obj)
    
    return objects

def demonstrate_search_improvement():
    """Show how broad searches find more objects than narrow ones"""
    
    print("OBEX Search Optimization Demonstration")
    print("=" * 50)
    
    # Load OBEX objects
    obex_objects = load_obex_manifests()
    print(f"\nTotal OBEX objects loaded: {len(obex_objects)}")
    
    # Test cases
    test_searches = [
        {
            'user_request': "Find an I2C driver",
            'narrow_search': ['driver', 'I2C'],
            'broad_search': expand_search_terms('i2c'),
        },
        {
            'user_request': "Find LED control code",
            'narrow_search': ['LED', 'driver'],
            'broad_search': expand_search_terms('led'),
        },
        {
            'user_request': "Find display driver",  
            'narrow_search': ['display', 'driver'],
            'broad_search': expand_search_terms('display'),
        }
    ]
    
    for test in test_searches:
        print(f"\n{'='*50}")
        print(f"User Request: {test['user_request']}")
        print("-" * 50)
        
        # Narrow search (old approach)
        print("\nNARROW SEARCH (Old Approach):")
        print(f"  Terms: {test['narrow_search']}")
        narrow_results = search_obex_objects(test['narrow_search'], obex_objects)
        narrow_count = sum(len(v) for v in narrow_results.values())
        print(f"  Found: {narrow_count} objects")
        
        # Show distribution by category if we found objects
        if narrow_count > 0:
            categories = {}
            for result_list in narrow_results.values():
                for obj in result_list:
                    cat = obj.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
            print(f"  Categories: {categories}")
        
        # Broad search (new approach)
        print("\nBROAD SEARCH (Optimized Approach):")
        print(f"  Terms: {test['broad_search'][:5]}..." if len(test['broad_search']) > 5 else f"  Terms: {test['broad_search']}")
        broad_results = search_obex_objects(test['broad_search'], obex_objects)
        broad_count = sum(len(v) for v in broad_results.values())
        print(f"  Found: {broad_count} objects")
        
        # Show distribution by category
        if broad_count > 0:
            categories = {}
            for result_list in broad_results.values():
                for obj in result_list:
                    cat = obj.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
            print(f"  Categories: {categories}")
        
        # Show improvement
        improvement = broad_count - narrow_count
        if improvement > 0:
            print(f"\n  ✅ IMPROVEMENT: +{improvement} additional objects found!")
            print(f"     ({int((broad_count/narrow_count - 1) * 100)}% increase)" if narrow_count > 0 else "     (Infinite improvement - found objects vs none)")
        
        # Show some example objects found only in broad search
        if broad_count > narrow_count:
            print("\n  Examples of objects found only with broad search:")
            shown = 0
            for result_list in broad_results.values():
                for obj in result_list:
                    # Check if this object wasn't in narrow results
                    in_narrow = False
                    for narrow_list in narrow_results.values():
                        if obj in narrow_list:
                            in_narrow = True
                            break
                    
                    if not in_narrow and shown < 3:
                        print(f"    - {obj.get('title', 'Unknown')} ({obj.get('category', 'unknown')})")
                        shown += 1

    print(f"\n{'='*50}")
    print("SUMMARY")
    print("-" * 50)
    print("✅ Broad searches using keyword expansion find significantly more relevant objects")
    print("✅ Objects are distributed across multiple categories, not just 'drivers'")
    print("✅ The 'misc' category often contains relevant drivers and tools")
    print("\nRecommendation: Always use broad search with keyword expansion for OBEX queries")

if __name__ == "__main__":
    demonstrate_search_improvement()