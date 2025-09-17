#!/usr/bin/env python3
"""
Analyze each example in Debug Window Manual to identify specific method needs
"""

import re
from collections import defaultdict

def extract_examples_with_methods(file_path):
    """Extract each PUB method and the methods it calls"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Split into individual methods
    pub_pattern = r'^(PUB|PRI)\s+([a-z_][a-z0-9_]*)[^\n]*\n((?:(?!^(?:PUB|PRI))[^\n]*\n)*)'
    
    examples = {}
    for match in re.finditer(pub_pattern, content, re.MULTILINE):
        method_type = match.group(1)
        method_name = match.group(2)
        method_body = match.group(3)
        
        # Extract called methods from body
        called = set()
        call_pattern = r'\b([a-z_][a-z0-9_]*)\s*\('
        
        for line in method_body.split('\n'):
            # Skip comments
            if "'" in line:
                line = line[:line.index("'")]
            # Skip DEBUG statements
            if 'DEBUG' in line:
                continue
                
            for call_match in re.finditer(call_pattern, line):
                func = call_match.group(1)
                # Filter out Spin2 built-ins
                if func not in ['waitms', 'waitus', 'cognew', 'string', 'udec', 'sdec',
                               'hex', 'bin', 'udec_', 'sdec_', 'hex_', 'bin_',
                               'sin', 'cos', 'abs', 'sprintf', 'str', 'long', 'word', 'byte',
                               'repeat', 'if', 'else', 'case', 'pinread', 'pinwrite', 'pinstart',
                               'return', 'result', 'elseif']:
                    called.add(func)
        
        examples[method_name] = {
            'type': method_type,
            'calls': sorted(called),
            'body_lines': len([l for l in method_body.split('\n') if l.strip()])
        }
    
    return examples

def analyze_method_requirements(examples):
    """Analyze which helpers each example needs"""
    
    # Group by common patterns
    sensor_readers = []
    simple_demos = []
    graphics_demos = []
    interactive_demos = []
    instrument_demos = []
    
    for name, info in examples.items():
        calls = info['calls']
        
        if any('read_' in c or 'get_' in c for c in calls):
            sensor_readers.append((name, calls))
        
        if any('draw_' in c for c in calls):
            graphics_demos.append((name, calls))
            
        if any('handle_' in c or 'process_' in c for c in calls):
            interactive_demos.append((name, calls))
            
        if 'oscilloscope' in name or 'scope' in name or 'analyzer' in name:
            instrument_demos.append((name, calls))
        
        if len(calls) <= 3:
            simple_demos.append((name, calls))
    
    return {
        'sensor_readers': sensor_readers,
        'simple_demos': simple_demos,
        'graphics_demos': graphics_demos,
        'interactive_demos': interactive_demos,
        'instrument_demos': instrument_demos
    }

def calculate_inline_sizes(examples):
    """Calculate how big inline implementations would be"""
    
    print("\n📏 INLINE IMPLEMENTATION SIZES BY EXAMPLE\n")
    print("=" * 80)
    
    for name, info in sorted(examples.items()):
        if not info['calls']:
            continue
            
        print(f"\n{info['type']} {name}()  [{info['body_lines']} lines]")
        print(f"  Calls {len(info['calls'])} methods:")
        
        total_inline_lines = 0
        for method in info['calls']:
            # Estimate lines needed for inline implementation
            if 'read_' in method or 'get_' in method:
                lines = 1  # Simple return statement
            elif 'draw_' in method:
                lines = 2  # DEBUG command
            elif 'handle_' in method or 'process_' in method:
                lines = 2  # Simple state update
            elif 'update_' in method:
                lines = 1  # DEBUG command
            else:
                lines = 3  # Generic helper
            
            total_inline_lines += lines
            print(f"    - {method}() ~{lines} lines")
        
        print(f"  TOTAL INLINE: ~{total_inline_lines} lines")
        print(f"  EFFICIENCY: {info['body_lines'] + total_inline_lines} total lines")
        
        # Recommendation
        if total_inline_lines <= 10:
            print(f"  ✅ RECOMMENDATION: Include inline")
        elif total_inline_lines <= 20:
            print(f"  ⚠️  RECOMMENDATION: Consider local PRI methods")
        else:
            print(f"  ❌ RECOMMENDATION: Too large, needs shared helpers")

def generate_minimal_implementations(examples):
    """Generate actual minimal implementations for common patterns"""
    
    print("\n🔧 MINIMAL INLINE IMPLEMENTATIONS\n")
    print("=" * 80)
    
    # Identify the most commonly called methods
    method_calls = defaultdict(list)
    for name, info in examples.items():
        for called in info['calls']:
            method_calls[called].append(name)
    
    # Sort by frequency
    common_methods = sorted(method_calls.items(), key=lambda x: len(x[1]), reverse=True)
    
    print("\n📊 MOST COMMONLY CALLED METHODS:")
    for method, callers in common_methods[:20]:
        print(f"  {method}(): Called by {len(callers)} examples")
    
    print("\n💡 PATTERN-BASED MINIMAL IMPLEMENTATIONS:\n")
    
    # Sensor pattern
    print("' SENSOR SIMULATION PATTERN (1-2 lines each)")
    print("VAR long demo_tick")
    print("PRI read_sensor() : v")
    print("  return demo_tick++ // 10         ' Slow counter")
    print("PRI read_temperature() : v") 
    print("  return 20 + demo_tick++ // 100   ' 20-30°C range")
    print()
    
    # Drawing pattern  
    print("' DRAWING PATTERN (1 line each)")
    print("PRI draw_grid(x,y,w,h,s)")
    print("  DEBUG(`PLOT GRID `(x,y,w,h,s))   ' Single debug command")
    print("PRI draw_button(x,y,w,h,t)")
    print("  DEBUG(`PLOT BOX `(x,y,w,h) 't')  ' Box with text")
    print()
    
    # Event pattern
    print("' EVENT SIMULATION PATTERN (1-2 lines)")
    print("VAR long ev_queue[4], ev_ptr")
    print("PRI handle_mouse() : x, y")
    print("  return demo_tick & $FF, demo_tick >> 8 & $FF")
    print("PRI process_click()")
    print("  ev_queue[ev_ptr++ & 3] := $CLICK")
    
    return common_methods

if __name__ == "__main__":
    file_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/document-production/manuals/p2-debug-window-manual/opus-master/complete-opus-master-v0.md"
    
    # Extract and analyze
    examples = extract_examples_with_methods(file_path)
    
    # Show statistics
    print(f"\n📊 ANALYSIS SUMMARY")
    print(f"Total examples: {len(examples)}")
    print(f"Examples with no calls: {len([e for e in examples.values() if not e['calls']])}")
    print(f"Examples with 1-3 calls: {len([e for e in examples.values() if 1 <= len(e['calls']) <= 3])}")
    print(f"Examples with 4-10 calls: {len([e for e in examples.values() if 4 <= len(e['calls']) <= 10])}")
    print(f"Examples with >10 calls: {len([e for e in examples.values() if len(e['calls']) > 10])}")
    
    # Calculate inline sizes
    calculate_inline_sizes(examples)
    
    # Generate minimal implementations
    common = generate_minimal_implementations(examples)
    
    # Group analysis
    groups = analyze_method_requirements(examples)
    
    print("\n📦 GROUPED BY PATTERN:")
    print(f"Sensor readers: {len(groups['sensor_readers'])} examples")
    print(f"Graphics demos: {len(groups['graphics_demos'])} examples")
    print(f"Interactive demos: {len(groups['interactive_demos'])} examples")
    print(f"Instrument demos: {len(groups['instrument_demos'])} examples")
    print(f"Simple demos: {len(groups['simple_demos'])} examples")