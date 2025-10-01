#!/usr/bin/env python3
"""
Analyze the keyword index to identify natural groupings similar to how 
'display' emerged as a cohesive group with 41 objects.
"""

import yaml
from collections import defaultdict
from pathlib import Path

def analyze_natural_groups():
    # Load the unified index
    with open('manifests/P2/community/obex-unified-index.yaml') as f:
        index_data = yaml.safe_load(f)
    
    keyword_index = index_data['keyword_index']
    objects_data = index_data['objects']
    
    # Group related keywords by analyzing co-occurrence
    keyword_groups = {
        'Communication Protocols': {
            'keywords': ['i2c', 'iic', 'twi', 'two-wire', 'spi', 'sspi', '3-wire', 
                        'uart', 'serial', 'async', 'tx', 'rx', 'dmx', 'dmx512',
                        '1-wire', 'onewire', 'can', 'canbus'],
            'objects': set(),
            'description': 'Serial communication protocols and interfaces'
        },
        
        'Display/Visual Output': {
            'keywords': ['display', 'screen', 'lcd', 'oled', 'tft', 'led', 'matrix',
                        'vga', 'epaper', 'e-ink', 'hmi', 'nextion', 'hub75', 'hub-75',
                        'neopixel', 'ws2812', 'ws2811', 'apa102', 'dotstar', 'rgb',
                        'hd44780', 'ssd1306', 'ili9341', 'st7735', 'max7219'],
            'objects': set(),
            'description': 'All forms of visual output including displays and LEDs'
        },
        
        'Sensors/Input': {
            'keywords': ['temperature', 'temp', 'humidity', 'pressure', 'light', 'lux',
                        'motion', 'imu', 'accelerometer', 'gyro', 'encoder', 'rotary',
                        'infrared', 'ir', 'bme280', 'dht11', 'dht22', 'ds18b20',
                        'mpu6050', 'bno08x', 'ads1118', 'tof', 'vl53l5cx'],
            'objects': set(),
            'description': 'Environmental and motion sensing'
        },
        
        'Motor Control': {
            'keywords': ['motor', 'stepper', 'servo', 'pwm', 'bldc', 'brushless',
                        'dc-motor', 'h-bridge', 'driver', 'park', 'step', 'dir'],
            'objects': set(),
            'description': 'Motor drivers and control systems'
        },
        
        'Audio/Sound': {
            'keywords': ['audio', 'sound', 'music', 'synth', 'synthesizer', 'wav',
                        'fm', 'ym2612', 'ym2608', 'opn', 'opna', 'opl', 'psg',
                        'sn76489', 'ay-3', 'sid', 'codec', 'speaker'],
            'objects': set(),
            'description': 'Audio generation, synthesis, and processing'
        },
        
        'Storage/Memory': {
            'keywords': ['storage', 'memory', 'sd', 'sdcard', 'flash', 'filesystem',
                        'eeprom', 'fram', 'sram', 'at24c', '24lc'],
            'objects': set(),
            'description': 'Data storage and memory interfaces'
        },
        
        'Time/Clock': {
            'keywords': ['rtc', 'clock', 'time', 'timer', 'neotimer', 'ds1307',
                        'ds3231', 'pcf8563'],
            'objects': set(),
            'description': 'Real-time clocks and timing utilities'
        },
        
        'Math/Computation': {
            'keywords': ['float', 'floating', 'math', 'decimal', 'integer', 'random',
                        'pllset', 'park', 'transform', 'qr', 'jpeg'],
            'objects': set(),
            'description': 'Mathematical and computational utilities'
        },
        
        'Module Standards': {
            'keywords': ['click', 'qwiic', 'grove', 'mikrobus', 'sparkfun', 'seeed'],
            'objects': set(),
            'description': 'Standardized module interfaces (Click, Qwiic, Grove)'
        },
        
        'Gaming/Entertainment': {
            'keywords': ['neoyume', 'megayume', 'neogeo', 'genesis', 'emulator',
                        'sprite', 'game', 'controller'],
            'objects': set(),
            'description': 'Game emulators and graphics engines'
        },
        
        'User Interface/Input': {
            'keywords': ['button', 'switch', 'twist', 'relay', 'ez-button', 
                        'accessory', 'board'],
            'objects': set(),
            'description': 'User input devices and interfaces'
        },
        
        'Text/Formatting': {
            'keywords': ['text', 'format', 'formatted', 'ansi', 'string'],
            'objects': set(),
            'description': 'Text processing and formatting utilities'
        }
    }
    
    # Populate each group with matching objects
    for group_name, group_data in keyword_groups.items():
        for keyword in group_data['keywords']:
            if keyword in keyword_index:
                group_data['objects'].update(keyword_index[keyword])
    
    # Analyze overlap between groups
    print("🔍 Natural Groupings Analysis")
    print("=" * 60)
    
    # Sort groups by object count
    sorted_groups = sorted(keyword_groups.items(), 
                          key=lambda x: len(x[1]['objects']), 
                          reverse=True)
    
    for group_name, group_data in sorted_groups:
        object_count = len(group_data['objects'])
        if object_count > 0:  # Only show groups with objects
            print(f"\n📦 {group_name}")
            print(f"   Description: {group_data['description']}")
            print(f"   Object count: {object_count}")
            
            # Show sample objects
            sample_ids = list(group_data['objects'])[:5]
            print(f"   Sample objects:")
            for obj_id in sample_ids:
                if obj_id in objects_data:
                    obj = objects_data[obj_id]
                    print(f"      - {obj['title']} ({obj_id})")
            
            if object_count > 5:
                print(f"      ... and {object_count - 5} more")
    
    # Find objects that appear in multiple groups (for insight)
    print("\n\n🔄 Objects in Multiple Groups (Cross-cutting concerns):")
    print("=" * 60)
    
    object_to_groups = defaultdict(set)
    for group_name, group_data in keyword_groups.items():
        for obj_id in group_data['objects']:
            object_to_groups[obj_id].add(group_name)
    
    multi_group_objects = {k: v for k, v in object_to_groups.items() if len(v) > 1}
    
    # Show top 10 most cross-cutting objects
    sorted_multi = sorted(multi_group_objects.items(), 
                         key=lambda x: len(x[1]), 
                         reverse=True)[:10]
    
    for obj_id, groups in sorted_multi:
        if obj_id in objects_data:
            obj = objects_data[obj_id]
            print(f"\n   {obj['title']} ({obj_id}):")
            for group in groups:
                print(f"      - {group}")
    
    # Suggest potential new categories based on natural groupings
    print("\n\n✨ Suggested Category Reorganization:")
    print("=" * 60)
    
    suggested_categories = [
        ("communication", "Communication Protocols", "I2C, SPI, UART, CAN, DMX, 1-Wire"),
        ("displays", "Display/Visual Output", "LCD, OLED, TFT, LED, VGA, E-paper"),
        ("sensors", "Sensors/Input", "Environmental, motion, light, encoders"),
        ("motors", "Motor Control", "Servo, stepper, DC, BLDC drivers"),
        ("audio", "Audio/Sound", "Synthesis, codecs, music generation"),
        ("storage", "Storage/Memory", "SD card, flash, EEPROM, filesystems"),
        ("timing", "Time/Clock", "RTC, timers, clock modules"),
        ("math", "Math/Computation", "Floating point, transforms, algorithms"),
        ("modules", "Module Standards", "Click, Qwiic, Grove boards"),
        ("ui", "User Interface", "Buttons, switches, input devices"),
        ("utilities", "General Utilities", "Text, formatting, misc tools")
    ]
    
    print("\nProposed categories to replace current structure:")
    for cat_id, cat_name, examples in suggested_categories:
        print(f"\n   {cat_id}/ ({cat_name})")
        print(f"      Examples: {examples}")
    
    # Compare with current categories
    print("\n\n📊 Current vs. Natural Distribution:")
    print("=" * 60)
    
    current_categories = defaultdict(int)
    for obj_id, obj in objects_data.items():
        # We need to get the original category from the loaded data
        # Since we don't have it in objects_data, we'll count from keywords
        if 'misc' in keyword_index and obj_id in keyword_index['misc']:
            current_categories['misc'] += 1
        elif 'drivers' in keyword_index and obj_id in keyword_index['drivers']:
            current_categories['drivers'] += 1
        elif 'sensors' in keyword_index and obj_id in keyword_index['sensors']:
            current_categories['sensors'] += 1
        elif 'motors' in keyword_index and obj_id in keyword_index['motors']:
            current_categories['motors'] += 1
        elif 'tools' in keyword_index and obj_id in keyword_index['tools']:
            current_categories['tools'] += 1
    
    print("\nCurrent category distribution:")
    for cat, count in sorted(current_categories.items(), key=lambda x: x[1], reverse=True):
        pct = (count / 113) * 100
        print(f"   {cat}: {count} objects ({pct:.1f}%)")
    
    print("\nNatural grouping distribution:")
    for group_name, group_data in sorted_groups[:8]:  # Top 8 groups
        count = len(group_data['objects'])
        pct = (count / 113) * 100
        print(f"   {group_name}: {count} objects ({pct:.1f}%)")

if __name__ == '__main__':
    analyze_natural_groups()