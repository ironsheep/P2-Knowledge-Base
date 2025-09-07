#!/usr/bin/env python3
"""
Extract P2 architecture components from documentation
"""

from pathlib import Path

def extract_architecture():
    """Extract P2 architecture components"""
    
    # Paths
    architecture_dir = Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2/architecture")
    
    # Architecture components to extract
    components = []
    
    # COG Architecture
    components.append({
        'name': 'COG',
        'category': 'processor',
        'description': 'Symmetric 32-bit processor core',
        'count': 8,
        'features': {
            'pipeline': '5-stage pipeline architecture',
            'execution': '2-clock execution when pipeline full',
            'memory': {
                'register_ram': '512 longs (2KB)',
                'lookup_ram': '512 longs (2KB)',
                'dual_port': True
            },
            'registers': {
                'general_purpose': '496 registers ($000-$1EF)',
                'dual_purpose': '8 registers ($1F0-$1F7)',
                'special_purpose': '8 registers ($1F8-$1FF)'
            },
            'special_registers': {
                'PTRA': 'HUB pointer A',
                'PTRB': 'HUB pointer B',
                'DIRA': 'Pin output enables (31:0)',
                'DIRB': 'Pin output enables (63:32)',
                'OUTA': 'Pin output states (31:0)',
                'OUTB': 'Pin output states (63:32)',
                'INA': 'Pin input states (31:0)',
                'INB': 'Pin input states (63:32)'
            },
            'features': [
                'Independent execution',
                'Full I/O pin access',
                'Hardware stack (8 levels)',
                'Carry and Zero flags',
                'Interrupts (3 priority levels)',
                'Debug interrupt',
                'Event tracking (16 events)'
            ]
        }
    })
    
    # HUB Architecture
    components.append({
        'name': 'HUB',
        'category': 'shared_memory',
        'description': 'Central shared memory and resources',
        'features': {
            'memory': {
                'size': '512KB (P2X8C4M64P)',
                'max_size': '1MB addressable',
                'width': '8 bits',
                'access': '32-bits-per-clock sequential',
                'format': 'Little-endian'
            },
            'access_method': {
                'type': 'Egg-beater round-robin',
                'timing': 'Every cog gets hub window every 8 clocks',
                'bandwidth': '32 bits per clock per cog'
            },
            'special_features': [
                'Last 16KB write-protectable',
                'Boot ROM (16KB)',
                'FIFO for hub execution',
                '64-bit system counter',
                '16 semaphore locks'
            ]
        }
    })
    
    # CORDIC Solver
    components.append({
        'name': 'CORDIC',
        'category': 'math_engine',
        'description': '32-bit pipelined CORDIC solver',
        'features': {
            'pipeline_depth': 55,
            'operations': [
                '32x32 unsigned multiply → 64-bit result',
                '64/32 unsigned divide → 32-bit quotient + remainder',
                '64-bit → 32-bit square root',
                'Rotate (X,Y) by Theta',
                'Polar to Cartesian conversion',
                'Cartesian to Polar conversion',
                'Unsigned to logarithm (32 → 5.27)',
                'Logarithm to unsigned (5.27 → 32)'
            ],
            'timing': {
                'issue_rate': 'Every 8 clocks (8 cogs)',
                'result_latency': '55 clocks',
                'scale_correction': 'Automatic'
            }
        }
    })
    
    # Smart Pins
    components.append({
        'name': 'Smart_Pins',
        'category': 'io_system',
        'description': 'Autonomous I/O pin processors',
        'count': 64,
        'features': {
            'modes': 32,
            'mode_categories': {
                'standard_io': 'Basic digital I/O',
                'dac_modes': 'DAC with noise/dither options',
                'pulse_modes': 'Pulse and NCO generation',
                'pwm_modes': 'Triangle/sawtooth PWM',
                'counter_modes': 'Counting and quadrature',
                'timing_modes': 'Time measurement',
                'adc_modes': 'ADC with SINC2/SINC3 filtering',
                'scope_mode': 'Oscilloscope with trigger',
                'usb_mode': 'USB host/device support',
                'serial_modes': 'Sync/async serial'
            },
            'analog_features': {
                'dac': '8-bit, 120-ohm and 1k-ohm modes',
                'adc': 'Delta-sigma with 5 ranges',
                'oversampling': '16-bit with noise shaping',
                'calibration': 'VIO/GIO reference'
            },
            'digital_features': {
                'filtering': '2/3/5/8-bit unanimous',
                'relative_pins': 'Access -3 to +3 pins',
                'feedback': 'Local positive/negative',
                'comparator': 'Pin-to-pin and 8-bit level'
            }
        }
    })
    
    # Streamer
    components.append({
        'name': 'Streamer',
        'category': 'dma_engine',
        'description': 'High-speed data streaming engine',
        'features': {
            'modes': [
                'Hub RAM to pins/DACs',
                'Pins/ADCs to Hub RAM',
                'LUT to pins/DACs',
                'Immediate to pins/DACs',
                'DDS/Goertzel operations',
                'HDMI/DVI video output'
            ],
            'capabilities': {
                'colorspace': '3x3 matrix conversion',
                'pixel_ops': '8:8:8:8 blending',
                'fifo': '19-stage buffer',
                'bandwidth': 'Up to sysclock/2'
            }
        }
    })
    
    # Event System
    components.append({
        'name': 'Event_System',
        'category': 'synchronization',
        'description': 'Hardware event tracking and interrupts',
        'features': {
            'event_sources': 16,
            'event_types': [
                'Counter matches (CT1/CT2/CT3)',
                'Selectable events (SE1-SE4)',
                'Pattern match',
                'FIFO events',
                'Streamer events',
                'Pin events',
                'Attention signals'
            ],
            'interrupt_levels': 3,
            'operations': ['Poll', 'Wait', 'Interrupt trigger']
        }
    })
    
    # Clock System
    components.append({
        'name': 'Clock_System',
        'category': 'timing',
        'description': 'Flexible clock generation system',
        'features': {
            'sources': [
                'Internal RC (~24 MHz)',
                'Crystal oscillator',
                'External clock input',
                'Internal RC (~20 kHz low power)'
            ],
            'pll': {
                'divider': '1..64',
                'multiplier': '1..1024',
                'post_divider': '(1..15)*2'
            },
            'switching': 'Glitch-free source switching',
            'power_modes': ['Run', 'Low power', 'Stop']
        }
    })
    
    # XBYTE Engine
    components.append({
        'name': 'XBYTE_Engine',
        'category': 'bytecode_executor',
        'description': 'Hardware bytecode execution engine',
        'features': {
            'cycle_time': '6 clocks per bytecode',
            'lut_lookup': 'Automatic bytecode translation',
            'registers': {
                'PA': 'Bytecode value',
                'PB': 'FIFO pointer',
                'FLAGS': 'Optional C/Z update'
            },
            'applications': 'Spin2 interpreter, custom VMs'
        }
    })
    
    # Write YAML files
    created = 0
    for component in components:
        yaml_path = architecture_dir / f"arch_{component['name'].lower()}.yaml"
        
        # Build YAML content
        yaml_content = f"""name: {component['name']}
category: {component['category']}
description: "{component['description']}"
"""
        
        if 'count' in component:
            yaml_content += f"count: {component['count']}\n"
        
        # Add features with proper YAML formatting
        if 'features' in component:
            yaml_content += "features:\n"
            yaml_content += format_features(component['features'], 2)
        
        yaml_content += "source: P2 Silicon Documentation v35\n"
        
        with open(yaml_path, 'w') as f:
            f.write(yaml_content)
        
        created += 1
        print(f"Created: {component['name']}")
    
    print(f"\nComplete:")
    print(f"  Created: {created} architecture component files")

def format_features(features, indent_level):
    """Format nested feature dictionary as YAML"""
    result = ""
    indent = "  " * indent_level
    
    for key, value in features.items():
        if isinstance(value, dict):
            result += f"{indent}{key}:\n"
            result += format_features(value, indent_level + 1)
        elif isinstance(value, list):
            result += f"{indent}{key}:\n"
            for item in value:
                result += f"{indent}  - {item}\n"
        elif isinstance(value, bool):
            result += f"{indent}{key}: {str(value).lower()}\n"
        else:
            result += f"{indent}{key}: {value}\n"
    
    return result

if __name__ == "__main__":
    extract_architecture()