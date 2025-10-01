#!/usr/bin/env python3
"""
Create a unified OBEX index with natural grouping keywords.
This version adds explicit group keywords so searches like "communication" 
return ALL communication-related objects.
"""

import yaml
import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def build_unified_obex_index():
    # Collect all OBEX objects from author manifests
    all_objects = []
    authors_path = Path('manifests/P2/community/obex/authors')

    for author_file in authors_path.glob('*-manifest.yaml'):
        with open(author_file) as f:
            data = yaml.safe_load(f)
            if 'objects' in data:
                for obj in data['objects']:
                    all_objects.append(obj)
    
    # Natural grouping definitions - these will be added as explicit keywords
    natural_groups = {
        'communication': {
            'triggers': ['i2c', 'iic', 'twi', 'spi', 'uart', 'serial', 'dmx', 
                        '1-wire', 'can', 'rs232', 'rs485', 'async', 'tx', 'rx'],
            'description': 'All communication protocols and interfaces'
        },
        'displays': {
            'triggers': ['display', 'lcd', 'oled', 'tft', 'led', 'matrix', 'vga',
                        'epaper', 'e-ink', 'hmi', 'nextion', 'rgb', 'neopixel',
                        'ws2812', 'hub75', 'graphics', 'video', 'screen'],
            'description': 'All visual output devices and drivers'
        },
        'sensors': {
            'triggers': ['sensor', 'temperature', 'humidity', 'pressure', 'light',
                        'motion', 'imu', 'accelerometer', 'gyro', 'encoder', 
                        'infrared', 'ir', 'tof', 'adc', 'analog', 'input',
                        'bme280', 'dht', 'mpu', 'bno', 'ads'],
            'description': 'All sensor and input devices'
        },
        'motors': {
            'triggers': ['motor', 'servo', 'stepper', 'pwm', 'bldc', 'brushless',
                        'h-bridge', 'driver', 'actuator', 'park', 'step/dir'],
            'description': 'Motor control and actuators'
        },
        'audio': {
            'triggers': ['audio', 'sound', 'music', 'synth', 'wav', 'mp3', 'fm',
                        'codec', 'speaker', 'ym2612', 'opn', 'psg', 'ay-3'],
            'description': 'Audio generation and processing'
        },
        'storage': {
            'triggers': ['storage', 'memory', 'sd', 'flash', 'eeprom', 'filesystem',
                        'fat32', 'fram', 'sram', 'at24c'],
            'description': 'Data storage and memory'
        },
        'timing': {
            'triggers': ['rtc', 'clock', 'timer', 'time', 'ds1307', 'ds3231', 
                        'pcf8563', 'neotimer'],
            'description': 'Timing and clock functions'
        },
        'modules': {
            'triggers': ['click', 'qwiic', 'grove', 'mikrobus', 'sparkfun', 'seeed'],
            'description': 'Standard module ecosystems'
        },
        'math': {
            'triggers': ['float', 'decimal', 'math', 'integer', 'random', 'transform',
                        'fft', 'cordic', 'qr', 'algorithm'],
            'description': 'Mathematical and computational functions'
        },
        'gaming': {
            'triggers': ['game', 'emulator', 'sprite', 'neogeo', 'genesis', 'nintendo',
                        'controller', 'joystick'],
            'description': 'Gaming and entertainment'
        }
    }
    
    # Comprehensive keyword mappings for better search
    topic_mappings = {
        # Communication Protocols
        'i2c': {
            'aliases': ['i2c', 'iic', 'twi', 'two-wire', 'two wire'],
            'related': ['qwiic', 'grove', 'smbus'],
            'description': 'Inter-Integrated Circuit serial protocol'
        },
        'spi': {
            'aliases': ['spi', 'sspi', '3-wire', 'three-wire', 'mosi', 'miso'],
            'related': ['chip select', 'cs'],
            'description': 'Serial Peripheral Interface'
        },
        'uart': {
            'aliases': ['uart', 'serial', 'async', 'tx', 'rx'],
            'related': ['rs232', 'rs485', 'ttl'],
            'description': 'Universal Asynchronous Receiver-Transmitter'
        },
        'dmx': {
            'aliases': ['dmx', 'dmx512', 'dmx-512'],
            'related': ['lighting', 'stage'],
            'description': 'Digital Multiplex lighting control'
        },
        '1-wire': {
            'aliases': ['1-wire', 'onewire', 'one-wire', '1wire'],
            'related': ['dallas', 'maxim'],
            'description': 'Dallas 1-Wire protocol'
        },
        'can': {
            'aliases': ['can', 'canbus', 'can-bus', 'can bus'],
            'related': ['automotive', 'obd'],
            'description': 'Controller Area Network'
        },
        
        # Display Technologies
        'display': {
            'aliases': ['display', 'displays', 'screen', 'monitor'],
            'related': ['graphics', 'driver', 'interface', 'visual'],
            'description': 'All display technologies and drivers'
        },
        'lcd': {
            'aliases': ['lcd', 'liquid crystal'],
            'related': ['hd44780', '16x2', '20x4', 'character display', 'pcf8574'],
            'description': 'LCD character and graphic displays'
        },
        'oled': {
            'aliases': ['oled', 'organic led'],
            'related': ['ssd1306', 'ssd1331', 'sh1106'],
            'description': 'Organic LED displays'
        },
        'tft': {
            'aliases': ['tft', 'tft-lcd'],
            'related': ['ili9341', 'st7735', 'color display', 'touchscreen'],
            'description': 'TFT color displays'
        },
        'led': {
            'aliases': ['led', 'light emitting diode'],
            'related': ['neopixel', 'ws2812', 'ws2811', 'apa102', 'dotstar', 'rgb', 'pixel'],
            'description': 'LED control including addressable RGB'
        },
        'matrix': {
            'aliases': ['matrix', 'dot matrix'],
            'related': ['hub75', 'hub-75', 'max7219', 'led matrix', 'led panel'],
            'description': 'Matrix displays including LED panels'
        },
        'vga': {
            'aliases': ['vga', 'video'],
            'related': ['ansi', 'text mode', 'graphics'],
            'description': 'VGA video output'
        },
        'epaper': {
            'aliases': ['e-paper', 'epaper', 'e-ink', 'eink'],
            'related': ['waveshare', 'electronic paper'],
            'description': 'E-paper/E-ink displays'
        },
        'hmi': {
            'aliases': ['hmi', 'human machine interface'],
            'related': ['nextion', 'timi', 'touch'],
            'description': 'Human-machine interface displays'
        },
        
        # Sensor Types
        'temperature': {
            'aliases': ['temperature', 'temp', 'thermal'],
            'related': ['thermocouple', 'thermistor', 'ntc', 'rtd', 'max31855', 'dht11', 'dht22', 'bme280', 'ds18b20'],
            'description': 'Temperature sensing'
        },
        'humidity': {
            'aliases': ['humidity', 'rh', 'relative humidity'],
            'related': ['dht11', 'dht22', 'bme280', 'sht'],
            'description': 'Humidity sensing'
        },
        'pressure': {
            'aliases': ['pressure', 'barometer', 'barometric'],
            'related': ['bme280', 'bmp280', 'bmp180', 'bmp390'],
            'description': 'Pressure sensing'
        },
        'light': {
            'aliases': ['light', 'lux', 'illuminance', 'ambient light'],
            'related': ['bh1750', 'tsl2561', 'photoresistor', 'ldr'],
            'description': 'Light intensity sensing'
        },
        'motion': {
            'aliases': ['motion', 'movement', 'imu', 'inertial'],
            'related': ['accelerometer', 'gyro', 'gyroscope', 'mpu6050', 'mpu9250', '9dof', '6dof', 'bno08x'],
            'description': 'Motion and orientation sensing'
        },
        
        # Actuators
        'motor': {
            'aliases': ['motor', 'motors'],
            'related': ['stepper', 'servo', 'bldc', 'brushless', 'dc motor', 'h-bridge', 'driver', 'pwm', 'pca9685'],
            'description': 'Motor control and drivers'
        },
        'relay': {
            'aliases': ['relay', 'relays'],
            'related': ['switch', 'mosfet', 'solid state', 'ssr'],
            'description': 'Relay and switch control'
        },
        
        # Audio
        'audio': {
            'aliases': ['audio', 'sound', 'music'],
            'related': ['wav', 'mp3', 'i2s', 'dac', 'adc', 'codec', 'speaker', 'microphone'],
            'description': 'Audio generation and processing'
        },
        'synth': {
            'aliases': ['synth', 'synthesizer', 'synthesis'],
            'related': ['fm', 'ym2612', 'ym2608', 'ay-3', 'sid', 'opn', 'opna', 'opl', 'psg', 'sn76489'],
            'description': 'Sound synthesis and chip emulation'
        },
        
        # Storage
        'storage': {
            'aliases': ['storage', 'memory'],
            'related': ['sd', 'sdcard', 'flash', 'eeprom', 'fram', 'sram', 'at24c', 'filesystem', 'fat32'],
            'description': 'Data storage and memory'
        },
        
        # Timing
        'rtc': {
            'aliases': ['rtc', 'real time clock', 'realtime clock'],
            'related': ['ds1307', 'ds3231', 'pcf8563', 'time', 'clock'],
            'description': 'Real-time clock modules'
        },
        
        # Input Devices  
        'encoder': {
            'aliases': ['encoder', 'rotary encoder'],
            'related': ['quadrature', 'rotary', 'knob', 'dial', 'twist'],
            'description': 'Rotary and quadrature encoders'
        },
        'infrared': {
            'aliases': ['ir', 'infrared'],
            'related': ['remote', 'nec', 'sony', 'rc5', 'ircs'],
            'description': 'Infrared communication and remotes'
        },
        
        # Module Standards
        'click': {
            'aliases': ['click', 'mikrobus'],
            'related': ['mikroe', 'mikroelektronika'],
            'description': 'MikroElektronika Click boards'
        },
        'qwiic': {
            'aliases': ['qwiic'],
            'related': ['sparkfun', 'i2c'],
            'description': 'SparkFun Qwiic I2C modules'
        },
        'grove': {
            'aliases': ['grove'],
            'related': ['seeed', 'seeedstudio'],
            'description': 'Seeed Studio Grove modules'
        }
    }
    
    def extract_keywords(obj):
        """Extract all relevant keywords for an object"""
        keywords = set()
        
        # Normalize text
        title = (obj.get('title', '') or '').lower()
        desc = (obj.get('description_short', '') or '').lower()
        author = (obj.get('author', '') or '').lower()
        full_text = f"{title} {desc}"
        
        # Check against natural groups FIRST
        for group_name, group_def in natural_groups.items():
            for trigger in group_def['triggers']:
                if trigger in full_text:
                    keywords.add(group_name)  # Add the group keyword
                    break
        
        # Check against topic mappings
        for topic, mapping in topic_mappings.items():
            topic_found = False
            
            # Check aliases
            for alias in mapping['aliases']:
                if alias in full_text:
                    # Add the main topic keyword
                    keywords.add(topic)
                    # ALSO add all aliases as searchable keywords
                    for all_alias in mapping['aliases']:
                        keywords.add(all_alias.replace(' ', '-'))  # Replace spaces with hyphens
                    topic_found = True
                    break
            
            # Check related terms if not already found
            if not topic_found:
                for related in mapping.get('related', []):
                    if related.lower() in full_text:
                        # Add the main topic keyword
                        keywords.add(topic)
                        # Add all aliases for this topic
                        for alias in mapping['aliases']:
                            keywords.add(alias.replace(' ', '-'))
                        break
        
        # Add author keywords
        if 'jonnymac' in author or 'mcphalen' in author:
            keywords.add('jonnymac')
        elif 'moraco' in author:
            keywords.add('moraco')
        elif 'wuerfel' in author:
            keywords.add('wuerfel_21')
        elif 'ersmith' in author:
            keywords.add('ersmith')
        elif 'gracey' in author:
            keywords.add('chip_gracey')
        
        # Add languages
        for lang in obj.get('languages', []):
            keywords.add(lang.lower())
        
        # Extract chip/module numbers
        chip_patterns = [
            r'max\d+', r'bme\d+', r'bmp\d+', r'dht\d+', r'pcf\d+',
            r'at24c\d+', r'ym\d+', r'ay-?\d+', r'sn\d+', r'ds\d+',
            r'mpu\d+', r'bh\d+', r'ssd\d+', r'ili\d+', r'ws\d+',
            r'24lc\d+', r'mcp\d+', r'ads\d+', r'pca\d+', r'bno\d+',
            r'vl\d+'
        ]
        
        for pattern in chip_patterns:
            chips = re.findall(pattern, full_text)
            keywords.update(chips)
        
        return list(keywords)
    
    # Build the complete index
    objects_by_id = {}
    keyword_to_objects = defaultdict(list)
    
    for obj in all_objects:
        obj_id = obj['object_id']
        keywords = extract_keywords(obj)
        
        # Create enriched object entry
        entry = {
            'id': obj_id,
            'title': obj['title'],
            'author': obj.get('author', ''),
            'languages': obj.get('languages', []),
            'description': obj.get('description_short', ''),
            'keywords': keywords,
            'content': f"objects/{obj_id}.yaml"  # Standard field name
        }
        
        objects_by_id[obj_id] = entry
        
        # Build reverse index
        for keyword in keywords:
            keyword_to_objects[keyword].append(obj_id)
    
    # Create the unified index file
    index_data = {
        'index_metadata': {
            'version': '2.1',  # Added complete URLs
            'generated': datetime.now().isoformat(),
            'total_objects': len(objects_by_id),
            'total_keywords': len(keyword_to_objects),
            'github_raw_base': 'https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main',
            'content_base': '/engineering/knowledge-base/P2/community/obex',
            'description': 'Unified topical index with natural groupings and complete URLs'
        },
        
        'natural_groups': natural_groups,
        
        'topic_definitions': topic_mappings,
        
        'objects': objects_by_id,
        
        'keyword_index': dict(keyword_to_objects),
        
        'usage_instructions': {
            'natural_group_search': [
                "Use natural group keywords for broad searches:",
                "  'communication' - All comm protocols (I2C, SPI, UART, etc.)",
                "  'displays' - All visual output devices",
                "  'sensors' - All input/sensing devices",
                "  'motors' - All motor control",
                "  'audio' - All sound generation",
                "  'storage' - All memory/storage",
                "  'timing' - All RTC/timer functions",
                "  'modules' - Click/Qwiic/Grove boards"
            ],
            'search_strategy': [
                "1. Download this single index file",
                "2. Search keyword_index for your topic or natural group",
                "3. Get object IDs from keyword_index",
                "4. Look up full object details in objects section",
                "5. Construct URL: github_raw_base + content_base + content",
                "6. Fetch object YAML from constructed URL",
                "7. Object YAML contains download_direct URL for actual code"
            ],
            'url_construction': [
                "URL = github_raw_base + content_base + content",
                "Example:",
                "  github_raw_base: https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main",
                "  content_base: /engineering/knowledge-base/P2/community/obex",
                "  content: objects/2817.yaml",
                "  Result: https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/engineering/knowledge-base/P2/community/obex/objects/2817.yaml"
            ],
            'example_searches': {
                'Find all communication': "keyword_index['communication'] → all protocol objects",
                'Find all displays': "keyword_index['displays'] → all display objects",
                'Find I2C drivers': "keyword_index['i2c'] → specific I2C objects",
                'Find jonnymac objects': "keyword_index['jonnymac'] → author's objects"
            }
        }
    }
    
    # Save the index
    output_path = Path('manifests/P2/community/obex-unified-index.yaml')
    with open(output_path, 'w') as f:
        yaml.dump(index_data, f, default_flow_style=False, sort_keys=False, width=120)
    
    print(f"✅ Created enhanced unified OBEX index v2.0:")
    print(f"   - Total objects: {len(objects_by_id)}")
    print(f"   - Total keywords: {len(keyword_to_objects)}")
    print(f"   - File: {output_path}")
    
    # Show natural group statistics
    print("\n📊 Natural Group Coverage:")
    for group_name in natural_groups:
        if group_name in keyword_to_objects:
            count = len(keyword_to_objects[group_name])
            pct = (count / len(objects_by_id)) * 100
            print(f"   {group_name}: {count} objects ({pct:.1f}%)")
    
    # Show top keywords
    print("\n📊 Top 15 Keywords by frequency:")
    sorted_keywords = sorted(keyword_to_objects.items(), key=lambda x: len(x[1]), reverse=True)
    for keyword, obj_ids in sorted_keywords[:15]:
        print(f"   {keyword}: {len(obj_ids)} objects")
    
    return index_data

if __name__ == '__main__':
    index_data = build_unified_obex_index()
    
    # Test natural groups
    print("\n🔍 Natural Group Test:")
    test_groups = ['communication', 'displays', 'sensors', 'motors', 'audio', 
                   'storage', 'timing', 'modules', 'math', 'gaming']
    for keyword in test_groups:
        if keyword in index_data['keyword_index']:
            count = len(index_data['keyword_index'][keyword])
            print(f"   '{keyword}': {count} objects")