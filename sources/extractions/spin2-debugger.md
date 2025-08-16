# SPIN2 Single-Step Debugger Extraction

**Source**: P2 Spin2 Documentation v51-250425.pdf  
**Extracted**: 2025-08-15  
**Focus**: PASM-level debugger, single-stepping, and breakpoint functionality  

## Overview

SPIN2 includes a sophisticated PASM-level debugger that enables single-stepping and breakpoint debugging directly within P2 assembly code. This debugger integrates seamlessly with the SPIN2 development environment.

**Key Features**:
- **PASM-level debugging**: Step through assembly instructions
- **Breakpoint support**: Set and manage breakpoints in code
- **Real-time scope displays**: Monitor variables and signals
- **Multi-COG debugging**: Debug multiple COGs simultaneously
- **Integration**: Works with both SPIN2 and PASM code

## PASM-Level Debugger

### Activation and Usage

The PASM-level debugger is invoked by placing `DEBUG` statements in SPIN2 or PASM code:

```spin2
' In SPIN2 code
DEBUG("Starting main loop")

' In PASM code
org
    debug       ' Invokes PASM-level debugger
    mov a, b
```

**Historical Development**:
- **v35u (2022-08-26)**: PASM-level debugger added with single-stepping and breakpoints
- **v35v (2022-09-11)**: Enhanced for early P2 Edge modules without serial pull-ups
- **v36 (2022-09-18)**: Automatic clock frequency adaptation added

### Single-Stepping Functionality

The debugger provides instruction-level stepping capabilities:

1. **Step Into**: Execute next instruction and stop
2. **Step Over**: Execute next instruction, stepping over calls
3. **Continue**: Resume normal execution until next breakpoint
4. **Break**: Interrupt execution at current instruction

### Breakpoint Management

**Setting Breakpoints**:
- Place `DEBUG` statements at desired break locations
- Conditional breakpoints supported through SPIN2 logic
- Multiple breakpoints can be active simultaneously

**Breakpoint Features**:
- **Line-level granularity**: Set breakpoints on specific instructions
- **Conditional execution**: Break only when conditions are met
- **Multi-COG support**: Independent breakpoints per COG
- **Dynamic management**: Add/remove breakpoints during debugging

## DEBUG SCOPE Displays

### Oscilloscope Functionality

The DEBUG system includes sophisticated scope displays for real-time signal monitoring:

```spin2
DEBUG(`SCOPE_XY samples x y color)   ' X-Y scope display
DEBUG(`SCOPE_XY AUTO)               ' Auto-scaling scope
```

**SCOPE Features**:
- **Real-time plotting**: Display changing values as waveforms
- **Multiple channels**: Monitor several signals simultaneously
- **Auto-scaling**: Automatic range adjustment for optimal viewing
- **Trigger support**: Automatic triggering on signal conditions
- **Color coding**: Different colors for different signals

### Trigger System

**Auto-triggering capability** added in v41:
```spin2
DEBUG(`SCOPE TRIGGER channel AUTO {offset})
```

**Trigger Features**:
- **Automatic triggering**: Start scope display on signal conditions
- **Channel selection**: Choose which signal triggers capture
- **Offset control**: Adjust trigger point within display window
- **Edge detection**: Trigger on rising/falling edges

## Advanced Debugging Features

### Clock Frequency Adaptation

**Dynamic frequency tracking** (v36+):
- Debugger adapts to run-time clock frequency changes
- Uses serial receive pin (P63) for frequency storage
- Maintains debugging accuracy across CLKSET operations
- Supports all P2 clock modes and frequencies

### Multi-COG Debugging

**Independent COG monitoring**:
- Each COG can have separate debug sessions
- Non-destructive monitoring of COG states
- Parallel debugging of multiple processes
- Coordinated breakpoints across COGs

### DEBUG Output Commands

**Enhanced output formatting**:
```spin2
DEBUG(`BOOL(value))     ' Output "TRUE" or "FALSE"
DEBUG(`?(boolean))      ' Backtick boolean output
DEBUG(`.(float))        ' Backtick floating-point output
```

**Mouse Interaction**:
- `PC_MOUSE` command reports pixel color at cursor
- Interactive debugging through mouse clicks
- Visual feedback for user interface debugging

## Practical Debugging Workflows

### Basic Single-Step Debugging

```spin2
PUB main() | i, result

    ' Set initial breakpoint
    DEBUG("Starting main function")
    
    repeat i from 0 to 9
        DEBUG("Loop iteration: ", DEC(i))  ' Break each iteration
        result := calculate(i)
        DEBUG("Result: ", DEC(result))
        
    DEBUG("Main function complete")

PRI calculate(value) : result | temp
    DEBUG("Entering calculate with: ", DEC(value))
    
    ' PASM section with debugging
    org
        debug           ' PASM-level breakpoint
        mov temp, value
        add temp, #10
        mov result, temp
        debug           ' Another breakpoint
    end
    
    DEBUG("Calculate returning: ", DEC(result))
```

### SCOPE Display Usage

```spin2
PUB monitor_sensors() | temperature, pressure

    ' Setup scope for real-time monitoring
    DEBUG(`SCOPE_XY samples temperature pressure $FF0000)
    DEBUG(`SCOPE TRIGGER temperature AUTO 100)
    
    repeat
        temperature := read_temperature()
        pressure := read_pressure()
        
        ' Feed data to scope display
        DEBUG(`SCOPE_XY_UPDATE temperature pressure)
        
        waitms(100)
```

### Multi-COG Debugging Setup

```spin2
PUB start_system()
    
    ' Start COG 1 - Sensor monitoring
    DEBUG("Starting sensor COG")
    cognew(sensor_cog(), @sensor_stack)
    
    ' Start COG 2 - Display updates  
    DEBUG("Starting display COG")
    cognew(display_cog(), @display_stack)
    
    ' Main COG - System coordination
    DEBUG("Main COG running coordination")
    coordination_loop()

PRI sensor_cog()
    DEBUG("Sensor COG started")
    repeat
        DEBUG("Reading sensors")
        ' Sensor reading code with breakpoints
        
PRI display_cog()  
    DEBUG("Display COG started")
    repeat
        DEBUG("Updating display")
        ' Display update code with breakpoints
```

## Integration with Development Environment

### Clock Mode Compatibility

**Automatic clock setup** (v36+):
- PASM-only programs get automatic clock-setter prepended
- No longer need ASMCLK instruction at program start
- Harmonized operation with debugger clock management
- Supports all P2 clock modes seamlessly

### Serial Communication

**Flexible baud rates**:
- `DEBUG_BAUD` symbol controls communication speed
- Default 2,000,000 baud for fast data transfer
- Adjustable for different hardware configurations
- Compatible with various terminal programs

### Flash Programming Support

**Production debugging**:
- Flash-programmed code retains debug capability
- Command-line DEBUG-only mode available
- Debug data preservation in flash memory
- Post-programming debug session support

## Error Handling and Diagnostics

### Common Issues and Solutions

**Floating-point exceptions** (fixed in v35g):
- Line-clipping routine improvements
- Memory-access violation prevention
- Stable scope display operation
- Robust mathematical operations

**Serial Communication Issues**:
- Pull-up resistor compatibility (v35v)
- Baud rate configuration options
- Hardware-specific adaptations
- Connection troubleshooting

### Debug Window Management

**Window control options**:
- `DEBUG_WINDOWS_OFF` symbol inhibits window opening
- Selective debug output control
- Resource management for embedded systems
- Headless operation support

## Performance Considerations

### Debug Impact Minimization

**Efficient debugging**:
- Minimal performance overhead when not active
- Conditional debug compilation with `__DEBUG__` symbol
- Selective breakpoint activation
- Resource-conscious scope displays

### Memory Usage

**Debug data storage**:
- Efficient breakpoint management
- Scope buffer optimization
- Multi-COG debug coordination
- Flash memory debug retention

## Educational Applications

### Learning Assembly Programming

**Step-by-step instruction analysis**:
- Visualize instruction execution effects
- Understand register and memory changes
- Learn PASM2 instruction behavior
- Practice optimization techniques

### System Understanding

**Hardware interaction visualization**:
- Monitor Smart Pin configurations
- Observe COG coordination patterns
- Understand timing relationships
- Debug hardware interface issues

### Advanced Concepts

**Real-time system debugging**:
- Multi-COG synchronization analysis
- Interrupt handling verification
- Performance bottleneck identification
- Resource contention resolution

---

**Trust Level**: ✅ Verified  
**Source Reference**: SPIN2 v51 Documentation, Multiple sections on DEBUG functionality  
**Extraction Quality**: Comprehensive - covers PASM debugger, scopes, and practical workflows  
**Educational Value**: Extremely High - enables hands-on P2 debugging education  
**Production Value**: High - essential for professional P2 development