#!/usr/bin/env python3
"""
P2 Architecture Component Extractor
Extracts and structures architecture components into YAML files
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class ArchitectureExtractor:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.components_dir = self.output_dir / "components"
        self.components_dir.mkdir(parents=True, exist_ok=True)
        
    def extract_components(self) -> Dict[str, Any]:
        """Define P2 architecture components"""
        components = {}
        
        # COG Component
        components['cog'] = {
            'metadata': {
                'id': 'p2_component_cog',
                'name': 'COG Processor',
                'category': 'processor',
                'version': '1.0',
                'extraction_date': datetime.now().isoformat()
            },
            'specifications': {
                'count': 8,
                'architecture': '32-bit RISC',
                'pipeline_stages': 5,
                'clock_speed': 'Up to 180MHz per cog',
                'memory': {
                    'cog_ram': '512 longs (2KB)',
                    'lut_ram': '512 longs (2KB)',
                    'special_registers': '16 hardware registers'
                }
            },
            'features': [
                '2-clock instruction execution when pipeline full',
                'Independent program counter',
                'Dedicated ALU and shifter',
                'Access to shared Hub RAM',
                'FIFO for streaming operations',
                'Interrupt capability (3 levels)',
                'Debug support'
            ],
            'programming_interface': {
                'start': 'COGINIT instruction',
                'stop': 'COGSTOP instruction',
                'id': 'COGID instruction',
                'communication': 'Hub RAM for inter-cog data'
            },
            'relationships': ['hub_memory', 'smart_pins', 'locks', 'events']
        }
        
        # Hub Memory Component
        components['hub_memory'] = {
            'metadata': {
                'id': 'p2_component_hub_memory',
                'name': 'Hub RAM',
                'category': 'memory',
                'version': '1.0',
                'extraction_date': datetime.now().isoformat()
            },
            'specifications': {
                'size': '512KB (1MB address space)',
                'width': '8-bit bytes, accessible as byte/word/long',
                'access_method': 'Egg-beater rotation',
                'timing': {
                    'window_size': '8 clocks',
                    'access_time': '13-20 clocks typical',
                    'burst_rate': '1 long per clock with FIFO'
                }
            },
            'features': [
                'Shared by all 8 cogs',
                'Egg-beater access ensures fairness',
                'FIFO streaming for predictable access',
                'Atomic read-modify-write operations',
                'Boot code storage'
            ],
            'programming_interface': {
                'read': ['RDBYTE', 'RDWORD', 'RDLONG'],
                'write': ['WRBYTE', 'WRWORD', 'WRLONG'],
                'streaming': ['RDFAST', 'WRFAST', 'RFBYTE', 'WFBYTE'],
                'block': 'SETQ + RD/WRLONG for block transfers'
            },
            'relationships': ['cog', 'fifo', 'streamer']
        }
        
        # CORDIC Component
        components['cordic'] = {
            'metadata': {
                'id': 'p2_component_cordic',
                'name': 'CORDIC Solver',
                'category': 'math_engine',
                'version': '1.0',
                'extraction_date': datetime.now().isoformat()
            },
            'specifications': {
                'pipeline_stages': 54,
                'bit_width': '32-bit',
                'operations': 8,
                'throughput': '1 result per clock when pipelined',
                'latency': '54 clocks for result'
            },
            'operations': [
                'QROTATE - Rotate 2D vector',
                'QVECTOR - Convert cartesian to polar',
                'QMUL - 32x32 multiply (64-bit result)',
                'QDIV - 64/32 divide',
                'QSQRT - Square root',
                'QLOG - Natural logarithm',
                'QEXP - Exponential',
                'QFRAC - Get fraction and exponent'
            ],
            'programming_interface': {
                'start': 'Q-prefixed instructions',
                'read_x': 'GETQX instruction',
                'read_y': 'GETQY instruction'
            },
            'relationships': ['cog']
        }
        
        # Smart Pins Component
        components['smart_pins'] = {
            'metadata': {
                'id': 'p2_component_smart_pins',
                'name': 'Smart Pin System',
                'category': 'io',
                'version': '1.0',
                'extraction_date': datetime.now().isoformat()
            },
            'specifications': {
                'count': 64,
                'modes': 'Multiple configurable modes',
                'adc_resolution': 'SINC2/SINC3 filtering',
                'dac_resolution': '8-bit with dithering',
                'max_frequency': 'System clock / 2'
            },
            'modes': [
                'Digital I/O',
                'PWM generation',
                'Pulse/edge detection',
                'Quadrature decode',
                'Serial transmit/receive',
                'ADC with filtering',
                'DAC output',
                'USB (pins 62-63)',
                'Frequency measurement',
                'Time measurement'
            ],
            'programming_interface': {
                'configure': 'WRPIN - Set pin mode',
                'set_x': 'WXPIN - Set X parameter',
                'set_y': 'WYPIN - Set Y parameter',
                'read': 'RDPIN - Read pin result',
                'check': 'RQPIN - Check pin status',
                'acknowledge': 'AKPIN - Acknowledge pin'
            },
            'relationships': ['cog', 'events']
        }
        
        # Streamer Component
        components['streamer'] = {
            'metadata': {
                'id': 'p2_component_streamer',
                'name': 'Streamer',
                'category': 'dma',
                'version': '1.0',
                'extraction_date': datetime.now().isoformat()
            },
            'specifications': {
                'channels': 1,
                'data_width': 'Configurable 1-32 bits',
                'modes': 'Multiple streaming modes',
                'max_rate': 'System clock rate'
            },
            'modes': [
                'Hub RAM to pins',
                'Pins to Hub RAM',
                'LUT to pins',
                'HDMI output mode',
                'ADC sampling with SINC filtering',
                'Goertzel mode for DSP'
            ],
            'features': [
                'Automatic hub addressing',
                'NCO for rate control',
                'Color space conversion',
                'HDMI encoding',
                'DMA without CPU intervention'
            ],
            'programming_interface': {
                'init': 'XINIT - Initialize streamer',
                'start': 'XCONT - Continue streaming',
                'stop': 'XSTOP - Stop streaming',
                'config': 'XZERO - Zero streamer state'
            },
            'relationships': ['hub_memory', 'fifo', 'smart_pins']
        }
        
        # FIFO Component
        components['fifo'] = {
            'metadata': {
                'id': 'p2_component_fifo',
                'name': 'FIFO System',
                'category': 'buffer',
                'version': '1.0',
                'extraction_date': datetime.now().isoformat()
            },
            'specifications': {
                'depth': '16 longs',
                'width': '32 bits',
                'modes': ['Read FIFO', 'Write FIFO'],
                'purpose': 'Hub memory streaming'
            },
            'features': [
                'Automatic hub address increment',
                'Depth tracking',
                'Block wrapping support',
                'Fast hub access (1 long/clock)',
                'Shared with streamer'
            ],
            'programming_interface': {
                'setup_read': 'RDFAST - Setup read FIFO',
                'setup_write': 'WRFAST - Setup write FIFO',
                'read': ['RFBYTE', 'RFWORD', 'RFLONG', 'RFVAR'],
                'write': ['WFBYTE', 'WFWORD', 'WFLONG'],
                'block': 'FBLOCK - Set block size'
            },
            'relationships': ['hub_memory', 'streamer', 'cog']
        }
        
        # Events Component
        components['events'] = {
            'metadata': {
                'id': 'p2_component_events',
                'name': 'Event System',
                'category': 'interrupt',
                'version': '1.0',
                'extraction_date': datetime.now().isoformat()
            },
            'specifications': {
                'event_sources': 16,
                'interrupt_levels': 3,
                'polling_modes': 'Event polling without interrupts'
            },
            'event_sources': [
                'Timer matches (CT1, CT2, CT3)',
                'Pin patterns',
                'Pin edges',
                'Hub FIFO levels',
                'Streamer ready',
                'ATN from other cogs',
                'Lock state changes',
                'CORDIC complete'
            ],
            'programming_interface': {
                'setup': ['SETINT1', 'SETINT2', 'SETINT3'],
                'trigger': ['TRGINT1', 'TRGINT2', 'TRGINT3'],
                'poll': ['POLLINT', 'POLLATN', 'POLLCT1'],
                'wait': ['WAITINT', 'WAITSE1', 'WAITATN']
            },
            'relationships': ['cog', 'smart_pins', 'cordic']
        }
        
        # Locks Component  
        components['locks'] = {
            'metadata': {
                'id': 'p2_component_locks',
                'name': 'Lock System',
                'category': 'synchronization',
                'version': '1.0',
                'extraction_date': datetime.now().isoformat()
            },
            'specifications': {
                'count': 16,
                'type': 'Hardware semaphores',
                'atomic': 'Atomic test-and-set'
            },
            'features': [
                'Inter-cog synchronization',
                'Resource protection',
                'Atomic operations',
                'No busy-waiting required'
            ],
            'programming_interface': {
                'new': 'LOCKNEW - Allocate new lock',
                'try': 'LOCKTRY - Try to acquire lock',
                'rel': 'LOCKREL - Release lock',
                'ret': 'LOCKRET - Return lock to pool'
            },
            'relationships': ['cog', 'hub_memory']
        }
        
        return components
    
    def write_component_yaml(self, name: str, data: Dict) -> None:
        """Write component data to YAML file"""
        filename = f"{name}.yaml"
        filepath = self.components_dir / filename
        
        with open(filepath, 'w') as f:
            # Write YAML manually
            f.write(f"# P2 Architecture Component: {data['metadata']['name']}\n")
            f.write(f"# Generated: {datetime.now().isoformat()}\n\n")
            
            # Metadata
            f.write("metadata:\n")
            for key, value in data['metadata'].items():
                f.write(f"  {key}: {value}\n")
            f.write("\n")
            
            # Specifications
            if 'specifications' in data:
                f.write("specifications:\n")
                self._write_dict(f, data['specifications'], indent=2)
                f.write("\n")
            
            # Features
            if 'features' in data:
                f.write("features:\n")
                for feature in data['features']:
                    f.write(f"  - {feature}\n")
                f.write("\n")
            
            # Other sections
            for section in ['operations', 'modes', 'event_sources']:
                if section in data:
                    f.write(f"{section}:\n")
                    for item in data[section]:
                        f.write(f"  - {item}\n")
                    f.write("\n")
            
            # Programming interface
            if 'programming_interface' in data:
                f.write("programming_interface:\n")
                self._write_dict(f, data['programming_interface'], indent=2)
                f.write("\n")
            
            # Relationships
            if 'relationships' in data:
                f.write("relationships:\n")
                for rel in data['relationships']:
                    f.write(f"  - {rel}\n")
    
    def _write_dict(self, f, d: Dict, indent: int) -> None:
        """Helper to write nested dict structure"""
        indent_str = "  " * (indent // 2)
        for key, value in d.items():
            if isinstance(value, dict):
                f.write(f"{indent_str}{key}:\n")
                self._write_dict(f, value, indent + 2)
            elif isinstance(value, list):
                f.write(f"{indent_str}{key}:\n")
                for item in value:
                    f.write(f"{indent_str}  - {item}\n")
            else:
                f.write(f"{indent_str}{key}: {value}\n")
    
    def generate_topology_map(self, components: Dict) -> None:
        """Generate architecture topology map"""
        topology_file = self.output_dir / "architecture-topology.md"
        
        with open(topology_file, 'w') as f:
            f.write("# P2 Architecture Topology Map\n\n")
            f.write(f"**Generated**: {datetime.now().isoformat()}\n\n")
            
            f.write("## Component Overview\n\n")
            f.write("```\n")
            f.write("┌─────────────────────────────────────────────────────────┐\n")
            f.write("│                    P2 Architecture                       │\n")
            f.write("├─────────────────────────────────────────────────────────┤\n")
            f.write("│                                                         │\n")
            f.write("│  ┌──────────┐ ┌──────────┐         ┌──────────┐       │\n")
            f.write("│  │  COG 0   │ │  COG 1   │  . . .  │  COG 7   │       │\n")
            f.write("│  └────┬─────┘ └────┬─────┘         └────┬─────┘       │\n")
            f.write("│       │            │                     │             │\n")
            f.write("│  ┌────┴────────────┴─────────────────────┴──────┐      │\n")
            f.write("│  │              Hub Memory (512KB)              │      │\n")
            f.write("│  │         (Egg-beater access rotation)         │      │\n")
            f.write("│  └───────────────┬──────────────────────────────┘      │\n")
            f.write("│                  │                                      │\n")
            f.write("│  ┌───────────────┴──────────────────────────────┐      │\n")
            f.write("│  │  Shared Resources:                           │      │\n")
            f.write("│  │  • CORDIC Solver (54-stage pipeline)         │      │\n")
            f.write("│  │  • 16 Hardware Locks                         │      │\n")
            f.write("│  │  • Event System                              │      │\n")
            f.write("│  │  • Streamer/FIFO                             │      │\n")
            f.write("│  └───────────────┬──────────────────────────────┘      │\n")
            f.write("│                  │                                      │\n")
            f.write("│  ┌───────────────┴──────────────────────────────┐      │\n")
            f.write("│  │         64 Smart Pins (P0-P63)               │      │\n")
            f.write("│  └───────────────────────────────────────────────┘      │\n")
            f.write("│                                                         │\n")
            f.write("└─────────────────────────────────────────────────────────┘\n")
            f.write("```\n\n")
            
            f.write("## Component Relationships\n\n")
            
            # Build relationship graph
            relationships = {}
            for comp_name, comp_data in components.items():
                if 'relationships' in comp_data:
                    relationships[comp_name] = comp_data['relationships']
            
            for comp, rels in relationships.items():
                f.write(f"### {comp.replace('_', ' ').title()}\n")
                f.write("Connects to:\n")
                for rel in rels:
                    rel_name = components.get(rel, {}).get('metadata', {}).get('name', rel)
                    f.write(f"  - {rel_name}\n")
                f.write("\n")
            
            f.write("## Data Flow Paths\n\n")
            f.write("1. **Cog ↔ Hub Memory**: Via egg-beater rotation windows\n")
            f.write("2. **Cog → CORDIC**: Start operations, read results after 54 clocks\n")
            f.write("3. **Hub Memory → Streamer → Pins**: DMA streaming for video/audio\n")
            f.write("4. **Pins → Smart Pin → Cog**: Input capture and measurement\n")
            f.write("5. **Cog ↔ Cog**: Via Hub RAM or ATN events\n")
            f.write("6. **FIFO ↔ Hub Memory**: Fast sequential access\n\n")
            
            f.write("## Performance Characteristics\n\n")
            f.write("- **Cog Execution**: 2 clocks per instruction (pipeline full)\n")
            f.write("- **Hub Access**: 13-20 clocks (window dependent)\n")
            f.write("- **FIFO Streaming**: 1 long per clock\n")
            f.write("- **CORDIC Result**: 54 clocks latency\n")
            f.write("- **Smart Pin Response**: 2 clocks typical\n")
        
        print(f"Topology map written to: {topology_file}")
    
    def run(self) -> None:
        """Run architecture extraction"""
        print("Extracting P2 architecture components...")
        
        # Extract component definitions
        components = self.extract_components()
        print(f"Defined {len(components)} architecture components")
        
        # Write YAML files
        for name, data in components.items():
            self.write_component_yaml(name, data)
            print(f"  Created: {name}.yaml")
        
        # Generate topology map
        print("\nGenerating architecture topology map...")
        self.generate_topology_map(components)
        
        print(f"\nArchitecture extraction complete:")
        print(f"  Components extracted: {len(components)}")
        print(f"  Output directory: {self.components_dir}")

if __name__ == "__main__":
    output_dir = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/knowledge-base/P2"
    
    extractor = ArchitectureExtractor(output_dir)
    extractor.run()