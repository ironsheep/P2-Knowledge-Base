# Parallax Propeller 2 Single-Step Debugger User Manual

## Table of Contents

1. [Overview](#overview)
2. [Invoking the Debugger](#invoking-the-debugger)
3. [Debugger Window Layout](#debugger-window-layout)
4. [Keyboard Controls](#keyboard-controls)
5. [Mouse Controls](#mouse-controls)
6. [Breakpoint Control Buttons](#breakpoint-control-buttons)
7. [Display Regions](#display-regions)
8. [Multi-COG Debugging](#multi-cog-debugging)
9. [DEBUG Statement Formatting](#debug-statement-formatting)
10. [Configuration Symbols](#configuration-symbols)
11. [Tips and Common Scenarios](#tips-and-common-scenarios)

---

## Overview

The Parallax Propeller 2 Single-Step Debugger provides interactive debugging of PASM2 code running on the P2 microcontroller. It is a **bidirectional** system: the P2 captures cog state and transmits it to the host PC, while the host renders the display and sends commands back to the P2.

### Key Features

- Single-step and continuous execution control
- Real-time inspection of all 512 COG registers, 512 LUT registers, and 507,904 bytes of HUB RAM
- 8-level hardware stack display
- Heatmap visualization showing register and memory changes
- Disassembly with three viewing modes (follow PC, cog lock, hub lock)
- Automatic register change tracking (delta watch list)
- Smart pin monitoring (64 pins via RQPIN)
- Interrupt and event status
- Per-cog debugger windows (each cog gets its own window)
- Inter-cog debugging via COGBRK

### Important Notes

- The debugger is **read-only** — you cannot modify register or memory values from the debugger UI
- The top 16KB of HUB RAM (`$FC000`-`$FFFFF`) is reserved for the debugger infrastructure and is not visible in the HUB viewer
- The debuggable HUB range is `$00000`-`$7BFFF` (507,904 bytes)

---

## Invoking the Debugger

### DEBUG Statement in Code

The debugger opens automatically when the P2 executes a `DEBUG` statement:

```spin2
PUB main()
  DEBUG                          ' Triggers debugger breakpoint
```

### Break on COGINIT

Define `DEBUG_COGINIT` to break whenever a cog starts:

```spin2
CON
  DEBUG_COGINIT = 1              ' Break on every COGINIT
```

This sets the initial BRK condition to `$110` (INIT + DEBUG bits).

### Break on First Execution

Define `DEBUG_MAIN` to break on the first instruction executed:

```spin2
CON
  DEBUG_MAIN = 1                 ' Break at initial cog execution
```

This sets the initial BRK condition to `$001` (MAIN bit).

---

## Debugger Window Layout

Each cog gets its own debugger window titled "Debugger - Cog N". The window uses a **123-column x 77-half-row** character grid:

```
     Col 2      Col 13    Col 24                          Col 82  Col 96  Col 116
      |           |         |                               |       |       |
Row 1 [REG MAP ] [LUT MAP] [CF] [ZF] [PC---] [SKIP/SKIPF pattern--] [XBYTE] [CT---------]
      |           |         |                                                |
Row 4 [          ][         ] [DISASSEMBLY (16 lines)----------] [WATCH] [SFR----] [EVENT]
      |           |         |                                    |       |         |
Row 35|           |         | [EXEC] [STACK (8 longs)----------]        |   [BUTTONS----]
      |           |         |                                           |   |            |
Row 40|           |         | [INT---------] [PTR (FPTR/PTRA/PTRB)---] |   |            |
      |           |         |                                           |   |            |
Row 47|           |         | [STAT] [PIN (DIR/OUT/IN binary)--------] |   |            |
      |           |         |                                           |   [            ]
Row 54|           |         | [SMART PIN WATCH---------------------]   |
      |           |         |                                           |
Row 57|           |         | [HUB DATA (8 rows hex+ASCII)--------] [HUB MAP]
      |           |         |                                           |
Row 74|           |         |      [HINT BAR-----------------------]
Row 77+-----------+---------+----------------------------------------------+
```

---

## Keyboard Controls

| Key | Action | Description |
|-----|--------|-------------|
| **Space** | Single Step | Execute one instruction, then halt (sends BRK condition once) |
| **Enter** | Repeat Mode | Continuous execution with throttled updates (~20 breaks/sec); press again to stop |
| **B** | Break | Set async break mode — clears all conditions except INIT (bit 8) |
| **I** | INIT Toggle | Toggle INIT breakpoint (right-click INIT button equivalent) |
| **D** | DEBUG Toggle | Toggle DEBUG breakpoint (right-click DEBUG button equivalent) |
| **M** | MAIN Toggle | Toggle MAIN single-step (right-click MAIN button equivalent) |
| **R** | Reset Watches | Clear register and LUT delta watch lists |
| **Up Arrow** | Hub Scroll Up | Scroll HUB data viewer up one row (`HubAddr -= $10`) |
| **Down Arrow** | Hub Scroll Down | Scroll HUB data viewer down one row (`HubAddr += $10`) |
| **Page Up** | Hub Page Up | Scroll HUB viewer up: `$80` (normal), `$1000` (Ctrl), `$10000` (Shift) |
| **Page Down** | Hub Page Down | Scroll HUB viewer down: same modifier scheme |

All letter keys are case-insensitive.

---

## Mouse Controls

### Click Actions by Region

| Region | Left-Click | Right-Click |
|--------|------------|-------------|
| **Break condition buttons** | Set condition exclusively (replaces others except INIT) | Toggle condition on/off without affecting others |
| **Go button** | Single Go (same as Space) | Repeat Mode (same as Enter) |
| **Go button (while running)** | Stop execution | Stop execution |
| **Disassembly box** | Lock disassembly to follow PC (`dmPC` mode) | Toggle address breakpoint at clicked line |
| **REG/LUT heatmap** | Lock disassembly to clicked cog/LUT address | — |
| **PC box** | Lock disassembly to follow PC | — |
| **SFR values** | Navigate to value (IJMP/IRET as code pointers; PA/PB/PTRA/PTRB as hub pointers) | — |
| **Stack values** | Navigate to value as code/hub pointer | — |
| **Pointer addresses** | Navigate hub viewer and disassembly to address | — |
| **Register watch box** | Reset watch list | — |
| **Smart pin watch box** | Reset smart pin watch list | Toggle: all pins vs. only pins with DIR set |
| **Hub data/chr/map** | Navigate hub address to clicked location | — |
| **Event names** | Set break event to clicked event (CT1..QMT) | — |

### Mouse Wheel

**In disassembly box** (switches to cog/hub lock mode if in follow-PC mode):

| Modifier | Cog Scroll | Hub Scroll |
|----------|------------|------------|
| None | 1 register | 16 bytes |
| Ctrl | 4 registers | 1 byte |
| Shift | 16 registers | 4 bytes |
| Ctrl+Shift | 32 registers | 128 bytes |

**In hub address digits**: Each scroll step changes the hex nibble under the cursor by +/-1.

**In hub data box**: Same modifier scheme with hub-specific scroll amounts.

### Mouse Hover (Hint Bar)

Moving the mouse over any region displays context-sensitive information in the hint bar at the bottom of the window:
- Registers: address, name, and current value
- Events: event description
- Buttons: break condition description
- CT: elapsed seconds at current clock frequency
- XBYTE: detailed mode description
- Hub data: address and byte value

---

## Breakpoint Control Buttons

The button panel occupies the bottom-right of the window.

### Break Condition Buttons

Break conditions are **bitmask flags** that can be combined (not mutually exclusive enums):

| Button | Bit | Mask | Description |
|--------|-----|------|-------------|
| **MAIN** | 0 | `$001` | Single-step main code instructions |
| **INT1** | 1 | `$002` | Single-step INT1 instructions |
| **INT2** | 2 | `$004` | Single-step INT2 instructions |
| **INT3** | 3 | `$008` | Single-step INT3 instructions |
| **DEBUG** | 4 | `$010` | Break on DEBUG (BRK with non-zero code) |
| **INT1E** | 5 | `$020` | Break on INT1 entry |
| **INT2E** | 6 | `$040` | Break on INT2 entry |
| **INT3E** | 7 | `$080` | Break on INT3 entry |
| **INIT** | 8 | `$100` | Break on COGINIT (independent — never cleared by other buttons) |
| **EVENT** | 9 | `$200` | Break on event (event ID in bits 15..12) |
| **ADDR** | 10 | `$400` | Break on address match (address in bits 31..12) |
| **BREAK** | — | — | Clear all conditions except INIT (async break mode) |

**Bit 11** (`$800`) is the **STALL** flag — used internally to keep the cog halted in the debug polling loop. Not a user-settable button.

**Left-click** sets a condition exclusively (replaces all others except INIT). **Right-click** toggles a condition without affecting others. INIT (bit 8) is always independent.

### Go/Stop/Break Button

| Caption | State | Action |
|---------|-------|--------|
| **Go** | Cog is halted | Left-click or Space: single step; Right-click or Enter: repeat mode |
| **Stop** | Repeat mode active | Any click: stop execution |
| **Break** | Cog running, 250ms timeout expired | Display dims; waiting for next break |

When the cog is running and 250ms pass without a breakpoint, the display dims (each pixel halved in brightness) and the button shows "Break".

---

## Display Regions

### Register and LUT Heatmaps (Left Side)

Two narrow bitmaps spanning nearly the full window height:

- **REG bitmap**: 32 pixels wide x 512 pixels tall — one row per cog register (`$000`-`$1FF`), one column per bit (MSB left, LSB right)
- **LUT bitmap**: Same structure for LUT addresses (`$200`-`$3FF`)

**Color encoding** (yellow-based palette, not blue/white):
- **Just changed** (hit value = 254): bright yellow (`cHighDiff`/`cLowDiff`)
- **Decaying**: fades by 2 per break toward cold
- **Unchanged** (cold): dark yellow (`cHighSame`/`cLowSame`)
- High bits (=1) use `cHigh*` colors; low bits (=0) use `cLow*` colors

Click on a heatmap cell to lock the disassembly view to that address.

### C Flag, Z Flag, and Program Counter (Top Row)

- **C flag**: Single character '0' or '1' (from bit 31 of interrupt return register)
- **Z flag**: Single character '0' or '1' (from bit 30 of interrupt return register)
- **PC**: 5 hex digits (20-bit program counter)

### SKIP/SKIPF Pattern (Top Row)

32-bit pattern showing which instructions are skipped. Label shows "SKIP" or "SKIPF" depending on mode. Shown dimmed with explanatory message when suspended during CALL or interrupt.

### XBYTE Status (Top Row)

9-bit XBYTE configuration displayed as 3 hex digits. Checkmark glyph appears if C/Z are affected by XBYTE.

### Clock Ticks (Top Row)

64-bit CT value displayed as 16 hex digits in two 8-digit groups. Hint bar shows elapsed seconds computed from the clock frequency.

### Disassembly View (Middle)

16 lines of disassembled P2 instructions. Three modes:

| Mode | Description |
|------|-------------|
| **Follow PC** (`dmPC`) | Auto-scrolls to keep PC visible; positions PC at line 4 (from top) |
| **Cog Lock** (`dmCog`) | Locked to a cog/LUT address; scroll with mouse wheel |
| **Hub Lock** (`dmHub`) | Locked to a hub address; scroll with mouse wheel |

Each line shows: address + raw 32-bit opcode + disassembled mnemonic and operands. The current PC line is highlighted with an inverse-color rounded rectangle. Instructions with SKIP bits set show a semi-transparent strikethrough. Address breakpoints show as semi-transparent highlights.

### Register Watch List (Middle-Right)

Automatically tracks up to 16 cog registers (`$000`-`$1EF`) that have changed. Shows 3-digit hex address + 8-digit hex value. Entries persist for ~1000 breaks after last change, then age out. Press **R** to clear.

### Special Function Registers (Middle-Right)

All 16 SFRs at `$1F0`-`$1FF` displayed in two columns:

```
$1F0  IJMP3  xxxxxxxx      $1F8   PTRA  xxxxxxxx
$1F1  IRET3  xxxxxxxx      $1F9   PTRB  xxxxxxxx
$1F2  IJMP2  xxxxxxxx      $1FA   DIRA  xxxxxxxx
$1F3  IRET2  xxxxxxxx      $1FB   DIRB  xxxxxxxx
$1F4  IJMP1  xxxxxxxx      $1FC   OUTA  xxxxxxxx
$1F5  IRET1  xxxxxxxx      $1FD   OUTB  xxxxxxxx
$1F6     PA  xxxxxxxx      $1FE    INA  xxxxxxxx
$1F7     PB  xxxxxxxx      $1FF    INB  xxxxxxxx
```

Click on IJMP/IRET values to navigate disassembly to that address. Click on PA/PB/PTRA/PTRB to navigate the hub viewer.

### Event Flags (Right)

16 P2 events displayed as single '0' or '1' characters:

| Index | Event | Index | Event |
|-------|-------|-------|-------|
| 0 | INT | 8 | PAT |
| 1 | CT1 | 9 | FBW |
| 2 | CT2 | 10 | XMT |
| 3 | CT3 | 11 | XFI |
| 4 | SE1 | 12 | XRO |
| 5 | SE2 | 13 | XRL |
| 6 | SE3 | 14 | ATN |
| 7 | SE4 | 15 | QMT |

Click on an event name to set it as the event breakpoint target.

### Execution Mode (Below Disassembly)

Tab label showing current execution context: **MAIN**, **INT1**, **INT2**, or **INT3**.

### Stack Registers

8 hardware stack values displayed as 8-digit hex. STK0 is top of stack. Click on a value to navigate to it as a code/hub pointer.

### Interrupt Status

Three interrupt levels (INT1/INT2/INT3), each showing the assigned event name and state (idle, wait, or busy).

### Pointer Data (FPTR, PTRA, PTRB)

Three rows showing 14 bytes of memory centered on each pointer:

```
Rxx  xxxxx  xx xx xx xx xx xx [xx] xx xx xx xx xx xx xx  ..............
PTRA xxxxx  xx xx xx xx xx xx [xx] xx xx xx xx xx xx xx  ..............
PTRB xxxxx  xx xx xx xx xx xx [xx] xx xx xx xx xx xx xx  ..............
```

FPTR prefix shows 'R' (read) or 'W' (write). Center byte (index 6) is highlighted. Click to navigate.

### Status Indicators

Five flags highlighted in bright orange when active, dimmed when inactive:

| Indicator | Meaning |
|-----------|---------|
| INIT | COGINIT occurred |
| STALLI | Stall interrupt active |
| STR | Streamer active |
| MOD | Color modulator active |
| LUTS | LUT sharing active |

### Pin Registers

Three rows of 64-bit binary values (DIR, OUT, IN) split into byte groups:

```
DIR  xxxxxxxx xxxxxxxx xxxxxxxx xxxxxxxx  xxxxxxxx xxxxxxxx xxxxxxxx xxxxxxxx
OUT  xxxxxxxx xxxxxxxx xxxxxxxx xxxxxxxx  xxxxxxxx xxxxxxxx xxxxxxxx xxxxxxxx
IN   xxxxxxxx xxxxxxxx xxxxxxxx xxxxxxxx  xxxxxxxx xxxxxxxx xxxxxxxx xxxxxxxx
```

### Smart Pin Watch

Automatically tracks up to 7 smart pins with changed RQPIN values. Shows pin number (P00-P61) + 8-digit hex value. Pins 62/63 (TX/RX) are excluded. By default only pins with DIR bit set are shown; right-click to toggle showing all pins.

### Hub Data Viewer

8 rows x 16 bytes of hub memory:

```
xxxxx  xx xx xx xx xx xx xx xx  xx xx xx xx xx xx xx xx  ................
```

Each row: 5-digit address + 16 hex bytes + 16 ASCII characters (non-printable shown as '.'). Address wraps at `$FFFFF`.

Navigation: arrow keys (Up/Down = +/-`$10`), page keys with modifiers, mouse wheel on address digits to change individual nibbles, click on hub heatmap to jump.

### Hub Heatmap

Small bitmap (64 x 62 pixels) showing block-level change activity across hub memory. Each pixel represents one 128-byte sub-block (3,968 sub-blocks total). Brighter = recently changed.

### Hint Bar

Context-sensitive status bar at the bottom showing details about whatever the mouse is hovering over.

---

## Multi-COG Debugging

Each cog that hits a breakpoint gets its **own separate debugger window**. There is no tab-switching between cogs — you work with multiple windows simultaneously.

### COGBRK (Asynchronous Break)

One cog can force another into the debugger using the `COGBRK` instruction:

```spin2
COGBRK  #3             ' Force cog 3 into debugger
```

**Important limitations**:
- The target cog must have debugging enabled
- Async break from the host only works when another cog is currently halted in its debug ISR (and thus processing the serial protocol)
- If no cog is in debug, there is no way to force a break from the host

### Viewing Another Cog's State

When a cog is halted at a breakpoint, you can request COGBRK for other cogs via the protocol. The target cog enters its debug ISR and opens its own debugger window.

---

## DEBUG Statement Formatting

The debugger supports various output formats for `DEBUG` statements in the text console:

```spin2
' Decimal formats
DEBUG(UDEC(value))             ' Unsigned decimal
DEBUG(SDEC(value))             ' Signed decimal

' Hexadecimal formats
DEBUG(UHEX(value))             ' Unsigned hex
DEBUG(SHEX(value))             ' Signed hex

' Binary formats
DEBUG(UBIN(value))             ' Unsigned binary
DEBUG(SBIN(value))             ' Signed binary

' Floating point
DEBUG(FDEC(fpvalue))           ' Float as decimal

' Strings
DEBUG(ZSTR(@string))           ' Zero-terminated string

' Boolean
DEBUG(BOOL(value))             ' Boolean value

' Arrays (append _ARRAY suffix and add count)
DEBUG(UDEC_BYTE_ARRAY(@array, count))

' Timing
DEBUG(DLY(1000))               ' Delay 1000ms after output

' PC interaction
DEBUG(PC_KEY(@buffer))         ' Get keyboard input from host
DEBUG(PC_MOUSE(@buffer))       ' Get mouse input from host

' Flags
DEBUG(C_Z)                     ' Output "C=? Z=?"
```

Each format supports display specifiers controlling separator and label output.

---

## Configuration Symbols

Define these `CON` symbols in your Spin2 source to configure debugging:

| Symbol | Default | Effect |
|--------|---------|--------|
| `DEBUG_DISABLE` | 0 | Non-zero disables all DEBUG statements |
| `DEBUG_PIN_TX` (or `DEBUG_PIN`) | 62 | TX pin number |
| `DEBUG_PIN_RX` | 63 | RX pin number |
| `DEBUG_BAUD` | Download baud | Serial baud rate |
| `DEBUG_COGS` | `$FF` (all) | Bitmask of cogs to enable debugging on |
| `DEBUG_COGINIT` | — | If defined, break on COGINIT events |
| `DEBUG_MAIN` | — | If defined, break on initial cog execution |
| `DEBUG_DELAY` | 0 | Startup delay in milliseconds |
| `DEBUG_TIMESTAMP` | — | If defined, show 64-bit timestamps in output |
| `DEBUG_LEFT/TOP/WIDTH/HEIGHT` | — | Host terminal window position |
| `DEBUG_DISPLAY_LEFT/TOP` | — | Host display window position |
| `DEBUG_LOG_SIZE` | 0 | Host log file size (0 = disabled) |
| `DEBUG_WINDOWS_OFF` | 0 | Suppress host debug windows |

---

## Tips and Common Scenarios

### Understanding the Display States

- **Halted**: Cog stopped at breakpoint. Display fully rendered. Go button shows "Go".
- **Single Go**: After pressing Space. Cog executes until break condition met, then halts again.
- **Repeat Mode**: After pressing Enter. Cog runs continuously with throttled updates (~20 breaks/sec). Press Enter or Space to stop.
- **Running (dimmed)**: 250ms timeout without a breakpoint. Display dims, Go button shows "Break".

### Finding Memory Corruption

1. Place `DEBUG` statements around suspicious code
2. Run until breakpoint
3. Examine the **hub heatmap** for unexpected bright spots (recently written areas)
4. Click the hot region to jump the hex dump to that address
5. Switch disassembly to hub mode, navigate to suspect code
6. Single-step while watching the hub heatmap for the write

### Debugging Interrupts

1. Enable the appropriate **INT1/INT2/INT3** single-step button (left column)
2. Or enable **INT1E/INT2E/INT3E** entry break button to catch interrupt entry
3. Monitor the **Event Flags** panel to see which events are triggering
4. Check interrupt vectors in the **SFR** panel (IJMP1/IRET1, etc.)

### Watching Register Changes

The register watch list automatically populates when registers change between breakpoints. This is purely automatic — you don't manually add registers. The heatmap provides a visual overview, and the watch list shows specific values. Press **R** to clear the accumulated watch list.

### Navigating Disassembly

- **Follow PC mode** (default): Disassembly auto-scrolls to keep PC visible
- Use **mouse wheel** in the disassembly box to switch to cog/hub lock mode for free scrolling
- **Click on the PC box** to return to follow-PC mode
- **Click on an SFR** (IJMP/IRET) to navigate disassembly to that address
- **Right-click** in disassembly to set/clear an address breakpoint at that line

### Performance Overhead

- The debugger stub occupies the top 16KB of hub RAM (`$FC000`-`$FFFFF`)
- Lock[15] is reserved for debugger mutual exclusion
- Serial pins (default 62/63) are used for debug communication
- Clock frequency must be at least 10 MHz

### Troubleshooting

| Symptom | Cause / Solution |
|---------|-----------------|
| Debugger window not opening | Ensure debug mode is enabled; check that `DEBUG_WINDOWS_OFF` is not set |
| Cog not breaking | Verify break condition bits match your intent; check `DEBUG_COGS` bitmask includes the target cog |
| Display dimmed, showing "Break" | Cog is running and hasn't hit a break condition in 250ms; check your break condition settings |
| COGBRK not working | Another cog must be halted in its debugger for async break to work; if no cog is in debug, the host cannot force a break |
| Hub data not updating | Only changed 4KB blocks are re-transferred; if the data hasn't changed since last break, it won't refresh |

---

For technical details on the debugger's internal protocol, CRC-based change detection, overlay architecture, and rendering system, see the [Single-Step Debugger: Theory of Operations](pascal-REF/SingleStep-Debugger-Theory-of-Operations.md).
