#!/usr/bin/env python3
"""
Generate minimal one-line stubs for all undefined methods in Debug Window Manual
"""

def generate_stub(method_name):
    """Generate appropriate one-line stub based on method name pattern"""
    
    # Common patterns and their stub implementations
    name = method_name.lower()
    
    # Reading/sensing patterns - return simulated values
    if name.startswith('read_') or name.startswith('get_'):
        if 'adc' in name:
            return f"PRI {method_name}() : v = demo_tick++ // 4096            ' 12-bit ADC simulation"
        elif 'temperature' in name or 'temp' in name:
            return f"PRI {method_name}() : v = 20 + demo_tick++ // 100      ' Temperature simulation"
        elif 'sensor' in name:
            return f"PRI {method_name}() : v = demo_tick++ // 100           ' Sensor range 0-99"
        elif 'button' in name or 'key' in name:
            return f"PRI {method_name}() : v = demo_tick & 1                ' Button state 0/1"
        elif 'analog' in name:
            return f"PRI {method_name}() : v = demo_tick & $FF             ' 8-bit analog value"
        elif 'value' in name or 'data' in name:
            return f"PRI {method_name}() : v = demo_tick++                  ' Incrementing value"
        elif 'position' in name or 'pos' in name:
            return f"PRI {method_name}() : v = demo_tick & $1FF            ' Position value"
        elif 'state' in name or 'status' in name:
            return f"PRI {method_name}() : v = (demo_tick >> 4) & $F       ' State machine 0-15"
        else:
            return f"PRI {method_name}() : v = demo_tick++ & $FFFF         ' Generic read"
    
    # Drawing/display patterns - use DEBUG commands
    elif name.startswith('draw_') or name.startswith('render_') or name.startswith('display_'):
        if 'line' in name:
            return f"PRI {method_name}(x1, y1, x2, y2, c)                   ' Draw line"
        elif 'box' in name or 'rect' in name:
            return f"PRI {method_name}(x, y, w, h, c)                       ' Draw box"
        elif 'circle' in name:
            return f"PRI {method_name}(x, y, r, c)                          ' Draw circle"
        elif 'text' in name or 'string' in name:
            return f"PRI {method_name}(x, y, str)                           ' Draw text"
        elif 'gauge' in name or 'meter' in name:
            return f"PRI {method_name}(x, y, v)                             ' Draw gauge"
        elif 'grid' in name:
            return f"PRI {method_name}(x, y, w, h, s)                      ' Draw grid"
        elif 'graph' in name or 'plot' in name:
            return f"PRI {method_name}(x, y, data)                         ' Draw graph"
        else:
            return f"PRI {method_name}(x, y)                               ' Generic draw"
    
    # Update/set patterns - modify state
    elif name.startswith('update_') or name.startswith('set_'):
        if 'display' in name or 'screen' in name:
            return f"PRI {method_name}()                                    ' Update display"
        elif any(x in name for x in ['value', 'data', 'param']):
            return f"PRI {method_name}(v) : r = v                           ' Set and return value"
        else:
            return f"PRI {method_name}(v)                                  ' Set value"
    
    # Processing/computation patterns
    elif any(x in name for x in ['process_', 'compute_', 'calculate_', 'analyze_']):
        if 'fft' in name:
            return f"PRI {method_name}() : v = demo_tick * 42               ' FFT simulation"
        elif any(x in name for x in ['average', 'mean']):
            return f"PRI {method_name}() : v = demo_tick // 10              ' Average calculation"
        elif 'filter' in name:
            return f"PRI {method_name}(v) : r = (v * 3) >> 2                ' Simple filter"
        else:
            return f"PRI {method_name}() : v = demo_tick++                  ' Process simulation"
    
    # Handler patterns
    elif name.startswith('handle_') or name.startswith('on_'):
        return f"PRI {method_name}() = ev_count++                        ' Event handler"
    
    # Initialization patterns
    elif name.startswith('init') or name.startswith('setup') or name.startswith('start'):
        return f"PRI {method_name}() = demo_tick := 0                    ' Initialize"
    
    # Reset/clear patterns
    elif 'reset' in name or 'clear' in name:
        return f"PRI {method_name}() = demo_tick := 0                    ' Reset state"
    
    # Capture/record patterns
    elif 'capture' in name or 'record' in name or 'sample' in name:
        return f"PRI {method_name}() : ptr = @demo_buffer                ' Return buffer"
    
    # Check/test patterns - return boolean
    elif name.startswith('is_') or name.startswith('has_') or name.startswith('check_'):
        return f"PRI {method_name}() : v = demo_tick & 1                 ' Boolean check"
    
    # Wait patterns
    elif name.startswith('wait_'):
        return f"PRI {method_name}() = waitms(1)                         ' Brief wait"
    
    # Send/transmit patterns
    elif name.startswith('send_') or name.startswith('transmit_') or name.startswith('tx_'):
        return f"PRI {method_name}(v)                                    ' Send data"
    
    # Receive patterns  
    elif name.startswith('receive_') or name.startswith('rx_'):
        return f"PRI {method_name}() : v = demo_tick & $FF              ' Receive simulation"
    
    # Configuration patterns
    elif 'config' in name or 'configure' in name:
        return f"PRI {method_name}(v)                                    ' Configure"
    
    # Enable/disable patterns
    elif 'enable' in name or 'disable' in name:
        return f"PRI {method_name}() = demo_tick := demo_tick ^ 1       ' Toggle enable"
    
    # Default fallback
    else:
        # Try to guess if it returns a value based on common patterns
        if any(x in name for x in ['get', 'read', 'check', 'is', 'has', 'measure', 'find']):
            return f"PRI {method_name}() : v = demo_tick++                  ' Returns value"
        else:
            return f"PRI {method_name}()                                    ' Action stub"

def main():
    # Read undefined methods
    with open('undefined_methods.txt', 'r') as f:
        undefined = [line.strip().split(',')[0] for line in f if line.strip()]
    
    # Generate header
    stub_content = """'==============================================================================
' Debug Window Manual - Helper Method Stubs
' Auto-generated minimal implementations for example compilation
'==============================================================================
'
' These are minimal one-line stubs that allow all examples to compile and run
' without external hardware. They provide simulated data and basic functionality.
'
' IMPORTANT: These are demonstration stubs only. In real applications, you would
' replace these with actual hardware interfaces and proper implementations.
'
'==============================================================================

CON
  ' Stub configuration constants
  STUB_VERSION = 1
  
VAR
  ' Shared simulation variables
  long demo_tick          ' Global counter for simulated data
  long ev_count           ' Event counter
  long demo_buffer[256]   ' Shared buffer for capture simulations
  long demo_var           ' General purpose variable

'------------------------------------------------------------------------------
' STUB IMPLEMENTATIONS
'------------------------------------------------------------------------------

"""
    
    # Group methods by prefix for organization
    groups = {
        'read_': [],
        'get_': [],
        'draw_': [],
        'render_': [],
        'display_': [],
        'update_': [],
        'set_': [],
        'process_': [],
        'compute_': [],
        'calculate_': [],
        'analyze_': [],
        'handle_': [],
        'init': [],
        'other': []
    }
    
    for method in sorted(undefined):
        added = False
        for prefix in groups.keys():
            if prefix != 'other' and method.startswith(prefix):
                groups[prefix].append(method)
                added = True
                break
        if not added:
            groups['other'].append(method)
    
    # Generate stubs by group
    for group, methods in groups.items():
        if not methods:
            continue
            
        # Add group header
        if group == 'read_':
            stub_content += "\n' Sensor/Input Reading Methods\n"
        elif group == 'get_':
            stub_content += "\n' Data Getter Methods\n"
        elif group in ['draw_', 'render_', 'display_']:
            stub_content += "\n' Drawing/Display Methods\n"
        elif group in ['update_', 'set_']:
            stub_content += "\n' Update/Setter Methods\n"
        elif group in ['process_', 'compute_', 'calculate_', 'analyze_']:
            stub_content += "\n' Processing/Computation Methods\n"
        elif group == 'handle_':
            stub_content += "\n' Event Handler Methods\n"
        elif group == 'init':
            stub_content += "\n' Initialization Methods\n"
        elif group == 'other':
            stub_content += "\n' Miscellaneous Methods\n"
        
        # Add stubs for this group
        for method in methods:
            stub_content += generate_stub(method) + "\n"
    
    # Write stub file
    with open('debug_window_stubs.spin2', 'w') as f:
        f.write(stub_content)
    
    print(f"Generated {len(undefined)} stub methods")
    print("Stub file created: debug_window_stubs.spin2")
    
    # Also create a version that can be inserted directly into the manual
    with open('stubs_for_manual.txt', 'w') as f:
        f.write(stub_content)
    
    return len(undefined)

if __name__ == "__main__":
    count = main()
    print(f"\n✅ Successfully generated {count} minimal stub implementations")