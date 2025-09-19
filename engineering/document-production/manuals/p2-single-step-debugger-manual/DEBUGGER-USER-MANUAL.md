# Parallax Propeller 2 Single-Step Debugger User Manual

## Table of Contents
1. [Overview](#overview)
2. [Invoking the Debugger](#invoking-the-debugger)
3. [Debugger Window Interface](#debugger-window-interface)
4. [User Commands and Controls](#user-commands-and-controls)
5. [Breakpoint Management](#breakpoint-management)
6. [Memory Inspection](#memory-inspection)
7. [Register Viewing and Modification](#register-viewing-and-modification)
8. [Advanced Features](#advanced-features)

## Overview

The Parallax Propeller 2 Single-Step Debugger provides comprehensive debugging capabilities for P2 microcontroller applications. It allows real-time inspection and control of up to 8 COGs (processors), with features including single-step execution, breakpoint management, memory inspection, and register modification.

### Key Features
- Step-by-step execution control (single-step, run, break)
- Memory inspection (COG, LUT, HUB)
- Register viewing and modification
- Disassembly with PC tracking
- Breakpoint management
- Call stack visualization
- Heat map visualization of memory access patterns
- Smart pin monitoring
- Interrupt and event tracking

## Invoking the Debugger

### Method 1: Enable Debug Mode in PNut
The debugger can be enabled through multiple methods in the PNut IDE:

#### Via Menu Commands
- **Run → Debug Enable (Ctrl+D)**: Enables debug mode for the current session
- **Run → Debug Disable**: Disables debug mode
- **Run → Debug Flash Enable**: Enables debug mode with flash programming
- **Run → Debug Load RAM**: Loads program to RAM with debug enabled
- **Run → Debug Load Flash**: Loads program to Flash with debug enabled

#### Via Command Line
```bash
pnut.exe myprogram.spin2 -bd    # Compile with debug enabled
pnut.exe myprogram.spin2 -cd    # Compile and download with debug enabled
```

### Method 2: Using DEBUG Statements in Code

The debugger is automatically invoked when the P2 executes a DEBUG statement in your Spin2 or PASM code:

```spin2
PUB main()
  DEBUG("Program starting")      ' Triggers debugger with message
  DEBUG                          ' Triggers debugger without message (breakpoint)

  ' Conditional debugging
  DEBUG_IF(condition)("Value: ", DEC(value))

  ' Various debug output formats
  DEBUG("Binary: ", BIN(value))
  DEBUG("Hex: ", HEX(value))
  DEBUG("Decimal: ", DEC(value))
  DEBUG("String: ", ZSTR(@mystring))
```

### Method 3: COGINIT with Debug

When starting a new COG with debug mode enabled, the debugger will break on COG initialization:

```spin2
COGINIT(COGEXEC_NEW, @entry, @stack)  ' Will break at entry if debug enabled
```

## Debugger Window Interface

The debugger window uses a 123x77 character grid layout with the following sections:

### Main Layout Areas

1. **COG/LUT Register Maps** (Top)
   - Visual heat map of register access patterns
   - COG registers $000-$1FF on left
   - LUT registers $200-$3FF on right
   - Color-coded to show read/write activity

2. **Control Registers** (Top-Right)
   - **C Flag**: Carry flag status
   - **Z Flag**: Zero flag status
   - **PC**: Program Counter (current execution address)
   - **SKIP**: Skip pattern register
   - **XBYTE**: XBYTE interpreter state
   - **CT**: 64-bit system counter

3. **Disassembly Window** (Middle)
   - Shows 16 lines of disassembled code
   - Current PC highlighted
   - Breakpoint indicators
   - Call depth tracking

4. **Watch Windows** (Middle-Right)
   - **Register Watch**: Monitor specific registers
   - **SFR**: Special Function Registers
   - **Events**: Event flag states

5. **Stack Display** (Bottom-Middle)
   - 8-level hardware stack contents
   - PTRA/PTRB pointer values

6. **HUB Memory Viewer** (Right)
   - Hexadecimal memory display
   - ASCII character representation
   - Mini-map for navigation

7. **Control Buttons** (Bottom-Right)
   - Mode selection buttons
   - GO/STOP control

## User Commands and Controls

### Keyboard Commands

| Key | Action | Description |
|-----|--------|-------------|
| **Space** | Step | Execute single instruction |
| **Enter** | GO/STOP | Toggle between run and break |
| **G** | GO | Start continuous execution |
| **S** | STOP | Break execution |
| **B** | BREAK Mode | Enable asynchronous break |
| **D** | DEBUG Toggle | Toggle DEBUG breakpoint |
| **I** | INIT Toggle | Toggle INIT (COGINIT) breakpoint |
| **M** | MAIN Toggle | Toggle MAIN mode breakpoint |
| **1** | INT1 Toggle | Toggle INT1 interrupt breakpoint |
| **2** | INT2 Toggle | Toggle INT2 interrupt breakpoint |
| **3** | INT3 Toggle | Toggle INT3 interrupt breakpoint |
| **A** | Address Mode | Enter address breakpoint mode |
| **W** | Watch | Add register to watch list |
| **C** | Clear | Clear all breakpoints |
| **R** | Reset | Reset current COG |
| **Q** | Quit | Exit debugger |
| **Tab** | Switch COG | Cycle through COGs 0-7 |
| **↑/↓** | Navigate | Move through disassembly |
| **PgUp/PgDn** | Page | Page through memory |
| **F1** | Help | Show help overlay |

### Mouse Controls

- **Left-Click on Button**: Activate button function
- **Right-Click on Button**: Toggle button state (for mode buttons)
- **Left-Click on Register**: Add to watch list
- **Double-Click on Value**: Edit value
- **Scroll Wheel**: Navigate through memory/disassembly

## Breakpoint Management

### Break Conditions

The debugger supports multiple simultaneous break conditions controlled by a 32-bit break condition register:

| Bit | Name | Description |
|-----|------|-------------|
| 0 | MAIN | Break on main code execution |
| 1 | INT1 | Break on INT1 interrupt |
| 2 | INT2 | Break on INT2 interrupt |
| 3 | INT3 | Break on INT3 interrupt |
| 4 | DEBUG | Break on DEBUG statement |
| 5 | INIT | Break on COGINIT |
| 6 | EVENT | Break on event trigger |
| 7 | ADDR | Break on address match |
| 8 | COGBRK | Enable asynchronous COG break |
| 11 | STALL | Stall mode (vs exit mode) |

### Setting Breakpoints

#### Address Breakpoints
1. Click **ADDR** button or press **A**
2. Enter address in hex (e.g., `$1234`)
3. Press Enter to confirm

#### Conditional Breakpoints
Use DEBUG_IF statements in code:
```spin2
DEBUG_IF(value > 100)("Threshold exceeded")
```

#### Event Breakpoints
1. Click **EVENT** button
2. Select event types to monitor
3. Debugger breaks when selected events occur

### Asynchronous Break (COGBRK)

The COGBRK feature allows one COG to break another COG's execution:
1. Enable BREAK mode in target COG
2. Another COG in DEBUG can trigger break
3. Useful for multi-COG debugging scenarios

## Memory Inspection

### COG Memory ($000-$1FF)
- 512 longs of COG RAM
- Direct register access
- Heat map shows access patterns
- Click to add to watch

### LUT Memory ($200-$3FF)
- 512 longs of Lookup Table RAM
- Shared between COG pairs (0-1, 2-3, 4-5, 6-7)
- Used for fast data access

### HUB Memory ($00000-$7BFFF)
- Up to 512KB shared RAM
- Hexadecimal and ASCII display
- Navigation via:
  - Arrow keys: Byte-by-byte
  - Page Up/Down: Page navigation
  - Click on mini-map: Jump to region
  - Enter address: Direct navigation

### Memory Editing
1. Double-click on value to edit
2. Enter new value in hex
3. Press Enter to confirm
4. Press Escape to cancel

## Register Viewing and Modification

### Special Function Registers (SFR)

| Register | Address | Description |
|----------|---------|-------------|
| IJMP3 | $1F0 | INT3 jump vector |
| IRET3 | $1F1 | INT3 return address |
| IJMP2 | $1F2 | INT2 jump vector |
| IRET2 | $1F3 | INT2 return address |
| IJMP1 | $1F4 | INT1 jump vector |
| IRET1 | $1F5 | INT1 return address |
| PA | $1F6 | Port A scratch register |
| PB | $1F7 | Port B scratch register |
| PTRA | $1F8 | Pointer A |
| PTRB | $1F9 | Pointer B |
| DIRA | $1FA | Direction register A |
| DIRB | $1FB | Direction register B |
| OUTA | $1FC | Output register A |
| OUTB | $1FD | Output register B |
| INA | $1FE | Input register A (read-only) |
| INB | $1FF | Input register B (read-only) |

### Modifying Registers
1. Click on register value in watch window
2. Enter new value (hex/decimal/binary)
3. Press Enter to apply

### Register Watch List
- Add registers by clicking or pressing **W**
- Remove with right-click
- Supports expressions (e.g., `$100+4`)
- Updates in real-time during execution

## Advanced Features

### Call Stack Tracking
- Displays up to 8 levels of CALL stack
- Shows return addresses
- Indicates call depth in disassembly

### Event Monitoring
The debugger monitors 16 event types:

| Event | Description |
|-------|-------------|
| INT | Interrupt occurred |
| CT1-CT3 | Counter matches |
| SE1-SE4 | Streamer events |
| PAT | Pattern match |
| FBW | FIFO block wrap |
| XMT | Transmit ready |
| XFI | Transmit finished |
| XRO | Receive overflow |
| XRL | Receive ready |
| ATN | Attention requested |
| QMT | Queue empty |

### Smart Pin Monitoring
- View configuration of smart pins
- Monitor pin states and modes
- Track pin-to-pin interactions

### Performance Analysis

#### Heat Map Visualization
- Red: Heavy write activity
- Yellow: Heavy read activity
- Green: Moderate activity
- Blue: Light activity
- Black: No activity

#### Execution Statistics
- Instruction count
- Cycle count
- Time elapsed
- Instructions per second

### Multi-COG Debugging

#### COG Selection
- Tab key cycles through COGs
- Click on COG number in display
- Status shows which COGs are active

#### Inter-COG Communication
- Monitor shared HUB memory
- Track LOCK usage
- View COG synchronization

### Debug Output Formatting

The debugger supports various output formats for DEBUG statements:

```spin2
' Decimal formats
DEBUG(DEC(value))           ' Decimal
DEBUG(UDEC(value))          ' Unsigned decimal
DEBUG(SDEC(value))          ' Signed decimal

' Hexadecimal formats
DEBUG(HEX(value))           ' Hex
DEBUG(UHEX(value))          ' Unsigned hex
DEBUG(SHEX(value))          ' Signed hex

' Binary formats
DEBUG(BIN(value))           ' Binary
DEBUG(UBIN(value))          ' Unsigned binary
DEBUG(SBIN(value))          ' Signed binary

' Floating point
DEBUG(FDEC(fpvalue))        ' Float decimal

' Strings
DEBUG(ZSTR(@string))        ' Zero-terminated string
DEBUG(LSTR(@string, len))   ' Length-specified string

' Arrays
DEBUG(UDEC_ARRAY(@array, count))  ' Array of values
```

### Debug Timing Control

Control execution timing with delays:

```spin2
DEBUG(DLY(1000))            ' Delay 1000ms after debug output
```

### PC Interaction

The debugger can interact with the host PC:

```spin2
' Get keyboard input
DEBUG(PC_KEY(@buffer))

' Get mouse input
DEBUG(PC_MOUSE(@x, @y, @buttons))
```

## Tips and Best Practices

### Effective Debugging Strategies

1. **Start Simple**: Begin with basic breakpoints before using advanced features
2. **Use Watch Windows**: Monitor critical variables continuously
3. **Leverage Heat Maps**: Identify unexpected memory access patterns
4. **Multi-COG Coordination**: Use COGBRK for synchronized debugging
5. **Save Debug Sessions**: Document breakpoint configurations for complex issues

### Performance Considerations

- Debugging adds overhead (~2-4KB code, ~1KB RAM per COG)
- Single-stepping is slower than continuous execution
- Heat map visualization may impact performance with rapid memory access
- Disable unused event monitoring to reduce overhead

### Common Debugging Scenarios

#### Finding Memory Corruption
1. Set write breakpoint on affected memory
2. Enable heat map to visualize access patterns
3. Use watch list to monitor surrounding memory

#### Debugging Interrupts
1. Enable appropriate INT breakpoints
2. Monitor event flags
3. Check interrupt vectors in SFR

#### Timing Issues
1. Use CT register to measure execution time
2. Monitor SKIP patterns for conditional execution
3. Check event timing with event monitor

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Debugger not triggering | Ensure debug mode enabled in PNut |
| COG not responding | Check STALLI flag, may be stalled |
| Can't modify register | Some registers are read-only (INA/INB) |
| Lost in memory | Use mini-map to navigate, press Home for start |
| Breakpoint not hitting | Verify address and break conditions |

## Conclusion

The P2 Single-Step Debugger is a powerful tool for developing and troubleshooting Propeller 2 applications. Master its features gradually, starting with basic stepping and breakpoints, then exploring advanced features as needed. The combination of visual feedback, comprehensive memory access, and flexible breakpoint control makes it an essential tool for P2 development.

For additional information, consult:
- Propeller 2 documentation
- PNut IDE user guide
- Spin2 language reference
- PASM instruction set reference