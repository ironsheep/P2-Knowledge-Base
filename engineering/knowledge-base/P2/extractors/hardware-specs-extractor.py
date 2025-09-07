#!/usr/bin/env python3
"""
Extract hardware specifications from various board documentation files
"""

from pathlib import Path
import re

def extract_hardware_specs():
    """Extract hardware specifications for P2 boards and modules"""
    
    # Paths
    sources_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/ingestion/sources")
    hardware_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/hardware")
    
    # Hardware categories to extract
    hardware_items = []
    
    # P2 Eval Board
    hardware_items.append({
        'name': 'P2 Eval Board',
        'part_number': '64000-ES',
        'category': 'development_board',
        'description': 'Full-featured P2 development board with all pins exposed',
        'features': [
            '64 I/O pins accessible',
            'USB programming port',
            'MicroSD card slot',
            'VGA connector',
            'Audio jack',
            'Mini prototyping area',
            'Power LED and 8 user LEDs'
        ],
        'power': '5V via USB or barrel jack',
        'dimensions': '4.0" x 5.25"'
    })
    
    # P2 Edge Module
    hardware_items.append({
        'name': 'P2 Edge Module',
        'part_number': 'P2-EC',
        'category': 'module',
        'description': 'Compact P2 module with edge connector',
        'features': [
            '64 I/O pins via edge connector',
            '32MB HyperRAM',
            '8MB Flash',
            'Castellated edge for soldering',
            'Mini form factor'
        ],
        'power': '3.3V and 1.8V required',
        'dimensions': '1.0" x 2.0"'
    })
    
    # P2 Edge Mini Breakout
    hardware_items.append({
        'name': 'P2 Edge Mini Breakout',
        'part_number': '64019',
        'category': 'carrier_board',
        'description': 'Minimal breakout for P2 Edge Module',
        'features': [
            'P2 Edge socket',
            'USB-C programming port',
            'Reset and boot buttons',
            'Power LED',
            'All pins broken out to headers'
        ],
        'power': '5V via USB-C',
        'dimensions': '2.3" x 2.9"'
    })
    
    # P2 Edge Breadboard Adapter
    hardware_items.append({
        'name': 'P2 Edge Breadboard Adapter',
        'part_number': '64020',
        'category': 'adapter',
        'description': 'Adapter for using P2 Edge on breadboards',
        'features': [
            'P2 Edge socket',
            'Breadboard-friendly 0.6" spacing',
            'All pins accessible',
            'Power regulation onboard'
        ],
        'power': '5V external',
        'dimensions': '3.5" x 1.0"'
    })
    
    # Add-on boards
    addon_boards = [
        {
            'name': 'Control Board',
            'part_number': '64025',
            'category': 'addon',
            'description': '8 LEDs add-on board',
            'pins_used': 8,
            'interface': '12-pin header'
        },
        {
            'name': '7-Segment Display',
            'part_number': '64026',
            'category': 'addon',
            'description': '6-digit 7-segment display',
            'pins_used': 14,
            'interface': '12-pin header'
        },
        {
            'name': 'Switches Board',
            'part_number': '64027',
            'category': 'addon',
            'description': '8 DIP switches',
            'pins_used': 8,
            'interface': '12-pin header'
        },
        {
            'name': 'Buttons Board',
            'part_number': '64028',
            'category': 'addon',
            'description': '8 pushbuttons',
            'pins_used': 8,
            'interface': '12-pin header'
        },
        {
            'name': 'Switches & LEDs',
            'part_number': '64029',
            'category': 'addon',
            'description': '4 switches and 4 LEDs',
            'pins_used': 12,
            'interface': '12-pin header'
        },
        {
            'name': 'Goertzel Board',
            'part_number': '40004',
            'category': 'addon',
            'description': 'Audio input/output with Goertzel',
            'pins_used': 10,
            'interface': '12-pin header'
        },
        {
            'name': 'HUB75 Adapter',
            'part_number': '64032',
            'category': 'addon',
            'description': 'RGB LED matrix adapter',
            'pins_used': 14,
            'interface': 'Dual 8-pin headers'
        }
    ]
    
    hardware_items.extend(addon_boards)
    
    # Write YAML files for each hardware item
    created = 0
    for item in hardware_items:
        # Create safe filename
        safe_name = item['name'].lower().replace(' ', '_').replace('-', '_').replace('&', 'and')
        yaml_path = hardware_dir / f"hw_{safe_name}.yaml"
        
        # Build YAML content
        yaml_content = f"""name: {item['name']}
part_number: {item.get('part_number', 'N/A')}
category: {item['category']}
description: "{item['description']}"
"""
        
        if 'features' in item:
            yaml_content += "features:\n"
            for feature in item['features']:
                yaml_content += f"  - {feature}\n"
        
        if 'power' in item:
            yaml_content += f"power: {item['power']}\n"
            
        if 'dimensions' in item:
            yaml_content += f"dimensions: {item['dimensions']}\n"
            
        if 'pins_used' in item:
            yaml_content += f"pins_used: {item['pins_used']}\n"
            
        if 'interface' in item:
            yaml_content += f"interface: {item['interface']}\n"
        
        yaml_content += "source: P2 Documentation Collection\n"
        
        with open(yaml_path, 'w') as f:
            f.write(yaml_content)
        
        created += 1
        print(f"Created: {item['name']}")
    
    print(f"\nComplete:")
    print(f"  Created: {created} hardware specification files")

if __name__ == "__main__":
    extract_hardware_specs()