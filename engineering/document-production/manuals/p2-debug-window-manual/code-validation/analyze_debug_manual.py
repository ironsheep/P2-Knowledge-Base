#!/usr/bin/env python3
"""
Analyze Debug Window Manual for method completeness
"""

import re
from pathlib import Path

def extract_method_definitions(content):
    """Extract all PUB and PRI method definitions"""
    pattern = r'^(PUB|PRI)\s+([a-z_][a-z0-9_]*)\s*(?:\(|$)'
    methods = []
    for line_num, line in enumerate(content.split('\n'), 1):
        match = re.match(pattern, line)
        if match:
            methods.append({
                'type': match.group(1),
                'name': match.group(2),
                'line': line_num
            })
    return methods

def extract_method_calls(content):
    """Extract all method calls (exclude definitions and DEBUG statements)"""
    # Pattern for method calls
    pattern = r'\b([a-z_][a-z0-9_]*)\s*\('
    calls = set()
    
    for line_num, line in enumerate(content.split('\n'), 1):
        # Skip method definitions
        if line.strip().startswith(('PUB ', 'PRI ')):
            continue
        # Skip DEBUG statements (they're special)
        if 'DEBUG(' in line or 'DEBUG`' in line:
            continue
            
        matches = re.findall(pattern, line)
        for match in matches:
            # Filter out known Spin2 built-ins
            if match not in ['waitms', 'waitus', 'cognew', 'string', 'udec', 'sdec', 
                           'hex', 'bin', 'udec_', 'sdec_', 'hex_', 'bin_', 
                           'sin', 'cos', 'abs', 'sprintf', 'str', 'long', 'word', 'byte',
                           'repeat', 'if', 'else', 'case', 'pinread', 'pinwrite', 'pinstart']:
                calls.add(match)
    
    return sorted(calls)

def analyze_completeness(file_path):
    """Analyze the manual for method completeness"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract definitions and calls
    definitions = extract_method_definitions(content)
    calls = extract_method_calls(content)
    
    # Get just the method names from definitions
    defined_names = {m['name'] for m in definitions}
    
    # Find undefined methods
    undefined = [call for call in calls if call not in defined_names]
    
    # Print results
    print(f"ANALYSIS OF: {file_path}")
    print("=" * 80)
    
    print(f"\n📊 STATISTICS:")
    print(f"  Total method definitions: {len(definitions)}")
    print(f"  Total unique method calls: {len(calls)}")
    print(f"  Undefined methods: {len(undefined)}")
    
    print(f"\n✅ DEFINED METHODS ({len(definitions)}):")
    for method in sorted(definitions, key=lambda x: x['name']):
        print(f"  {method['type']} {method['name']} (line {method['line']})")
    
    print(f"\n❌ UNDEFINED METHODS ({len(undefined)}):")
    if undefined:
        for method in sorted(undefined):
            print(f"  - {method}()")
    else:
        print("  None - All methods are defined!")
    
    print(f"\n🔍 DETAILED UNDEFINED METHOD LIST:")
    if undefined:
        # Group by likely category
        sensor_methods = [m for m in undefined if 'sensor' in m or 'read_' in m or 'get_' in m]
        display_methods = [m for m in undefined if 'draw_' in m or 'display_' in m or 'show_' in m or 'render_' in m]
        debug_methods = [m for m in undefined if 'debug_' in m]
        process_methods = [m for m in undefined if 'process_' in m or 'handle_' in m or 'execute_' in m]
        update_methods = [m for m in undefined if 'update_' in m]
        other_methods = [m for m in undefined if m not in sensor_methods + display_methods + debug_methods + process_methods + update_methods]
        
        if sensor_methods:
            print("\n  SENSOR/READ METHODS:")
            for m in sorted(sensor_methods):
                print(f"    - {m}()")
        
        if display_methods:
            print("\n  DISPLAY/DRAW METHODS:")
            for m in sorted(display_methods):
                print(f"    - {m}()")
        
        if process_methods:
            print("\n  PROCESS/HANDLE METHODS:")
            for m in sorted(process_methods):
                print(f"    - {m}()")
                
        if update_methods:
            print("\n  UPDATE METHODS:")
            for m in sorted(update_methods):
                print(f"    - {m}()")
        
        if debug_methods:
            print("\n  DEBUG HELPER METHODS:")
            for m in sorted(debug_methods):
                print(f"    - {m}()")
        
        if other_methods:
            print("\n  OTHER METHODS:")
            for m in sorted(other_methods):
                print(f"    - {m}()")
    
    return undefined

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/document-production/manuals/p2-debug-window-manual/opus-master/complete-opus-master-v0.md"
    undefined = analyze_completeness(file_path)