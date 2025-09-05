# Complete Event, Interrupt, and COG/TASK Symbols Reference

## Events and Interrupt Sources - COMPLETE LIST

### Event Source Symbols (16 Total)
```spin2
EVENT_INT          ' %0000 - Pin edge/level interrupt
EVENT_CT1          ' %0001 - CT passed CT1 value
EVENT_CT2          ' %0010 - CT passed CT2 value  
EVENT_CT3          ' %0011 - CT passed CT3 value
EVENT_SE1          ' %0100 - Selectable event 1 executed
EVENT_SE2          ' %0101 - Selectable event 2 executed
EVENT_SE3          ' %0110 - Selectable event 3 executed
EVENT_SE4          ' %0111 - Selectable event 4 executed
EVENT_PAT          ' %1000 - INA/INB pattern matched
EVENT_FBW          ' %1001 - Hub FIFO block wrapped
EVENT_XMT          ' %1010 - Streamer command empty
EVENT_XFI          ' %1011 - Streamer command finished
EVENT_XRO          ' %1100 - Streamer NCO rolled over
EVENT_XRL          ' %1101 - Streamer read last LUT location
EVENT_ATN          ' %1110 - Attention requested from another cog
EVENT_QMT          ' %1111 - CORDIC/PIX operation done (GETQX/GETQY empty)
```

### Interrupt Control (PASM)
```spin2
INT_OFF            ' Disable interrupt (same value as EVENT_INT)
INT_ON             ' Enable interrupt
```

### Event Usage in PASM
```pasm
' Set up event
SETSE1 #EVENT_PAT         ' Configure SE1 for pattern match
SETPAT ##pattern, ##mask  ' Set pattern to match

' Wait for event
WAITSE1                    ' Wait for pattern match event

' Poll event
POLLSE1 WC                 ' Check if event occurred (C=1 if yes)

' Interrupt setup
SETINT1 #EVENT_XFI         ' Set INT1 to streamer finished
SETINT2 #EVENT_CT1         ' Set INT2 to timer match
SETINT3 #EVENT_ATN         ' Set INT3 to attention
```

---

## COG and TASK Control Symbols - COMPLETE LIST

### COGINIT Mode Symbols
```spin2
COGEXEC            ' %00_0000 - Start cog in cogexec mode (execute from cog RAM)
HUBEXEC            ' %10_0000 - Start cog in hubexec mode (execute from hub RAM)
COGEXEC_NEW        ' %01_0000 - Start any available cog in cogexec mode
HUBEXEC_NEW        ' %11_0000 - Start any available cog in hubexec mode
COGEXEC_NEW_PAIR   ' %01_0001 - Start available even/odd cog pair in cogexec
HUBEXEC_NEW_PAIR   ' %11_0001 - Start available even/odd cog pair in hubexec
```

### COGINIT Usage Examples
```spin2
' Start specific cog
COGINIT(COGEXEC + 3, @pasm_code, @parameters)  ' Start cog 3 in cogexec
COGINIT(HUBEXEC + 5, @hub_code, @parameters)   ' Start cog 5 in hubexec

' Start any available cog
cogid := COGINIT(COGEXEC_NEW, @pasm_code, @parameters)
cogid := COGINIT(HUBEXEC_NEW, @hub_code, @parameters)

' Start cog pair for LUT sharing
pair := COGINIT(COGEXEC_NEW_PAIR, @code, @params)  ' Returns even cog number
```

### COGSPIN Symbol
```spin2
NEWCOG             ' -1 (%01_0000) - Start in any available cog
```

### COGSPIN Usage
```spin2
' Start Spin2 method in new cog
cogid := COGSPIN(NEWCOG, method(param1, param2), @stack)

' Start in specific cog
cogid := COGSPIN(3, method(param1, param2), @stack)
```

### TASKSPIN Symbol
```spin2
NEWTASK            ' -1 - Start in any available task slot
```

### TASKSPIN Usage
```spin2
' Start method in new task within current cog
taskid := TASKSPIN(NEWTASK, method(params), @stack)

' Start in specific task slot (0-31)
taskid := TASKSPIN(2, method(params), @stack)
```

### TASKSTOP/TASKHALT Symbol
```spin2
THISTASK           ' -1 - Reference to current task
```

### Task Control Usage
```spin2
TASKSTOP(THISTASK)         ' Stop current task
TASKSTOP(taskid)           ' Stop specific task

TASKHALT(THISTASK)         ' Halt current task (can be resumed)
TASKHALT(taskid)           ' Halt specific task

TASKRESUME(taskid)         ' Resume halted task
TASKNEXT()                 ' Switch to next task
TASKWAIT(ticks)           ' Wait in current task
```

---

## Cog Pair Architecture

### LUT Sharing Between Cog Pairs
```
Cog Pairs with Shared LUT:
- Cogs 0-1 share LUT access
- Cogs 2-3 share LUT access
- Cogs 4-5 share LUT access
- Cogs 6-7 share LUT access
```

### Using COGEXEC_NEW_PAIR / HUBEXEC_NEW_PAIR
```spin2
' Start cooperating cogs with shared LUT
even_cog := COGINIT(COGEXEC_NEW_PAIR, @producer_code, @params1)
odd_cog := even_cog + 1  ' Companion cog is always even+1

' Producer (even cog) writes to shared LUT
WRLUT value, address

' Consumer (odd cog) reads from shared LUT  
RDLUT value, address
```

---

## Complete Task Architecture

### Task Distribution
```
8 Cogs × 32 Tasks = 256 Total Execution Contexts

Each cog can run up to 32 concurrent tasks:
- Tasks share cog resources
- Round-robin scheduling
- Hardware task switching (no overhead)
```

### Task Registers
```spin2
' Each task has its own:
' - Program counter (PC)
' - Stack pointer (PTRA)
' - Call stack (8 levels)
' - Z and C flags
```

---

## System Information Symbols

### Read-Only System Values
```spin2
CHIPVER            ' Chip version/revision number
CLKMODE            ' Current clock mode configuration
CLKFREQ            ' Current clock frequency in Hz
```

### Usage Examples
```spin2
' Display system info
DEBUG("Chip version: ", UHEX(CHIPVER))
DEBUG("Clock frequency: ", UDEC(CLKFREQ), " Hz")
DEBUG("Clock mode: ", UHEX(CLKMODE))

' Conditional compilation based on chip version
if CHIPVER == $00000002
  ' Rev B specific code
```

---

## Numeric Constants

### Boolean Values
```spin2
FALSE              ' $0000_0000 (0)
TRUE               ' $FFFF_FFFF (-1)
```

### Integer Limits
```spin2
POSX               ' $7FFF_FFFF - Maximum positive integer (+2,147,483,647)
NEGX               ' $8000_0000 - Maximum negative integer (-2,147,483,648)
```

### Mathematical Constants
```spin2
PI                 ' 3.141592654 (single-precision float $4049_0FDB)
E                  ' 2.718281828 (single-precision float)
```

### Usage Examples
```spin2
' Boolean operations
flag := TRUE
if flag == FALSE
  ' Do something

' Range checking
if value > POSX
  value := POSX     ' Clamp to max positive

' Mathematical calculations
angle := PI * 2.0   ' Full rotation in radians
growth := E ** time  ' Exponential growth
```

---

## Why These Symbols Are Essential

### Event System Power
- 16 independent event sources per cog
- Hardware event detection (no polling needed)
- Can trigger interrupts or be polled
- Essential for real-time response

### COG/TASK Flexibility
- Start cogs in different execution modes
- Automatic cog allocation with _NEW variants
- LUT sharing with _PAIR variants
- 256 total execution contexts possible

### System Constants
- No magic numbers in code
- Self-documenting intentions
- Portable across P2 variants
- Standard values across all programs

These symbols transform low-level bit manipulation into high-level, readable operations that clearly express programmer intent.