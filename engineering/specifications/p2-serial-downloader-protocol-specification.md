# P2 Serial Downloader Protocol Specification

**Version**: 1.0  
**Date**: 2025-09-11  
**Authority**: Based on P2 Silicon Documentation v35, P2 Datasheet, and ROM Boot Loader analysis  
**Purpose**: Complete protocol specification for P2 serial boot loader implementation verification  

---

## Executive Summary

The P2 Serial Downloader is a built-in ASCII-based boot protocol residing in the P2's 16KB Boot ROM. It provides auto-baud detection from 9600 to 2 Mbaud, supports Intel Hex and Base64 data formats, and includes multi-chip addressing capabilities. This document provides complete implementation details for protocol verification and compliance testing.

## 1. Boot Sequence and Entry Conditions

### 1.1 Boot Priority Sequence
The P2 Boot ROM checks boot sources in this strict order:

1. **P61 Pull-up Check**: If P61 is pulled high → Enter Serial Loader
2. **P60 SPI Flash Check**: If P60 configured → Attempt SPI flash boot  
3. **P59 SD Card Check**: If P59 configured → Attempt SD card boot
4. **Default Execution**: Execute from hub $00000 if loaded

### 1.2 Serial Boot Entry Requirements
- **P61 (Boot Enable)**: Must be pulled HIGH (3.3V) via external resistor
- **P63 (Serial RX)**: Input pin for receiving host data
- **P62 (Serial TX)**: Output pin for transmitting responses to host
- **Timing**: 100ms initial detection window, 60-second timeout for first command

### 1.3 Pin Configuration Details
```
Pin Assignments (Fixed in ROM):
├── P63: Serial RX (Data FROM host TO P2)
├── P62: Serial TX (Data FROM P2 TO host)  
└── P61: Boot enable (HIGH = serial boot enabled)
```

**Critical Note**: Pin assignments are fixed in Boot ROM and cannot be changed.

## 2. Auto-Baud Detection Protocol

### 2.1 Detection Mechanism
The auto-baud system measures timing of the first CR (0x0D) character received to calculate baud rate.

**Detection Sequence**:
1. P2 transmits "> " (0x3E, 0x20) prompt on P62
2. Host sends any command terminated by CR (0x0D)
3. ROM measures bit timing of CR character  
4. ROM calculates baud divisor from measured timing
5. ROM configures UART hardware to match host baud rate

### 2.2 Supported Baud Rates
```
Minimum: 9600 baud
Maximum: 2,000,000 baud (2 Mbaud)

Common rates: 9600, 19200, 38400, 57600, 115200, 
             230400, 460800, 921600, 1000000, 2000000
```

**Accuracy Requirements**: Host baud rate must be within ±2% for reliable detection.

### 2.3 Detection Trigger Characters
- **Primary**: CR (0x0D) - Carriage return  
- **Secondary**: '>' (0x3E) - Greater than symbol

**Implementation Note**: The ROM can detect baud rate from either character, but CR is preferred for command termination.

## 3. Command Protocol Specification

### 3.1 Command Format
All commands are plain ASCII text terminated by CR (0x0D). The protocol is case-sensitive.

**General Format**: `Command_Name [parameters]<CR>`

### 3.2 Communication State Machine
```
States:
├── PROMPT: Display "> " and wait for command
├── COMMAND: Process received command string
├── DATA: Receive hex or base64 data 
├── EXECUTE: Validate and launch loaded program
└── ERROR: Return '?' and return to PROMPT
```

### 3.3 Response Codes
- **`> `** (0x3E, 0x20): Ready for command (prompt state)
- **`.`** (0x2E): Command acknowledged/processing/success
- **`?`** (0x3F): Error occurred, command invalid or failed

## 4. Core Commands

### 4.1 Prop_Chk - Communication Verification
**Purpose**: Verify communication link and identify chip version

**Syntax**: `Prop_Chk<CR>`

**Response**: `Prop_Ver Au<CR>` 
- "Au" indicates revision A silicon (current production)
- Future silicon revisions will return different codes

**Example Session**:
```
> Prop_Chk
Prop_Ver Au
.
>
```

### 4.2 Prop_Clk - Clock Configuration  
**Purpose**: Configure system clock before code loading

**Syntax**: `Prop_Clk P1 P2 P3<CR>`

**Parameters**:
- **P1**: Clock source selection
  - `0` = RCFAST (internal ~20MHz RC oscillator)
  - `1` = RCSLOW (internal ~20KHz RC oscillator)  
  - `2` = XI/Crystal (external crystal/oscillator)
- **P2**: PLL multiply factor (1-1024, only used if P1=2)
- **P3**: PLL divide factor (1-1024, only used if P1=2)

**Clock Calculation**: `Final_Frequency = Crystal_Frequency × P2 ÷ P3`

**Example Sessions**:
```
> Prop_Clk 0
.
> (now running on RCFAST ~20MHz)

> Prop_Clk 2 10 1  
.
> (now running on Crystal × 10, e.g., 20MHz crystal → 200MHz)
```

**Constraints**:
- Crystal frequency: 4-40MHz typical
- Final system frequency: Maximum 250MHz (P2 limit)
- PLL factors must result in valid VCO frequency range

### 4.3 Prop_Hex - Intel Hex Data Loading
**Purpose**: Load binary data in Intel HEX format

**Syntax**: `Prop_Hex<CR>`

**Data Format**: Standard Intel HEX records
```
Format: :LLAAAATTDD...DD CC
├── LL: Byte count (hex)
├── AAAA: Address (hex) 
├── TT: Record type (00=data, 01=end-of-file)
├── DD...DD: Data bytes (hex)
└── CC: Checksum (hex)
```

**Record Types Supported**:
- `00`: Data record (load data to specified address)
- `01`: End of file record (terminate loading)

**Example Session**:
```
> Prop_Hex
:10000000214601360121470136007EFE09D21940
:10001000104400011044000010440001104400013A
:00000001FF
.
(program executes)
```

**Checksum Validation**: Each record's checksum is verified. Invalid checksums return '?' and abort loading.

### 4.4 Prop_Txt - Base64 Data Loading
**Purpose**: Load binary data in Base64 format (more efficient than hex)

**Syntax**: `Prop_Txt ~<CR>`

**Data Format**: RFC 4648 standard Base64 encoding
- **Alphabet**: `A-Z`, `a-z`, `0-9`, `+`, `/`
- **Padding**: `=` character as needed
- **Terminator**: `~` character ends data stream
- **Whitespace**: Ignored (spaces, tabs, CR, LF allowed)

**Efficiency**: ~75% vs ~44% for Intel Hex

**Example Session**:
```
> Prop_Txt ~
UHJvcAQAAAAAAAIAAABQAf//QAH//0AB//8=
~
.
(program executes)
```

**Encoding Notes**:
- Data is loaded starting at hub address $00000
- Invalid Base64 characters return '?' and abort loading
- Terminator '~' must be present to complete loading

## 5. Data Loading and Execution

### 5.1 Memory Layout
All loaded data goes into Hub RAM starting at address $00000.

**Standard Program Structure**:
```
Address     Content
$00000      'Prop' signature (4 bytes)
$00004      Checksum (4 bytes, negative sum of all longs)
$00008      Data length (4 bytes)
$0000C      Program code starts here...
```

### 5.2 Checksum Verification
Before execution, the ROM verifies program integrity:

**Checksum Algorithm**:
1. Sum all 32-bit longs from $00000 to end of program
2. Result must equal zero (negative checksum at $00004)
3. If checksum fails, return '?' and remain in boot loader

**Validation Sequence**:
```assembly
; Pseudo-code for ROM checksum validation
checksum = 0
for address = $00000 to program_end step 4
    checksum += read_long(address)
if checksum != 0 then error
```

### 5.3 Program Execution
After successful checksum validation:
1. ROM performs `COGINIT #0, #$00000` 
2. COG 0 begins execution from hub address $00000
3. Boot ROM is no longer accessible
4. Program has full control of P2

## 6. Multi-Chip Support

### 6.1 INA/INB Masking
The serial loader supports selective addressing in multi-chip configurations.

**INA Masking (P31-P0)**:
- ROM reads INA register at boot time
- Only responds if INA matches expected pattern
- Used for addressing chips 0-31 in array

**INB Masking (P63-P32)**:  
- ROM reads INB register at boot time
- Only responds if INB matches expected pattern
- Used for addressing chips 32-63 in array

### 6.2 Broadcast Mode
When no masking is configured, all chips in system respond simultaneously, allowing synchronized loading of identical code.

**Implementation**: Host sends identical commands to all chips connected to same serial bus.

## 7. Error Handling

### 7.1 Error Conditions
- **Invalid command**: Unrecognized command name
- **Syntax error**: Malformed parameters
- **Checksum failure**: Intel Hex record or program checksum invalid  
- **Timeout**: No activity after initial 60-second window
- **Communication error**: Invalid characters or baud rate detection failure

### 7.2 Error Recovery
- **Single '?' response**: Command failed, ready for new command
- **Return to prompt**: All errors return to "> " prompt state
- **No state corruption**: Errors don't affect subsequent commands
- **Reset recovery**: Hardware reset restarts entire boot sequence

### 7.3 Error Prevention
- **Echo characters**: ROM echoes received characters for verification
- **Immediate feedback**: Errors reported immediately
- **Graceful degradation**: Partial failures don't crash system

## 8. Terminal Software Requirements

### 8.1 Communication Settings
- **Data Format**: 8 bits, No parity, 1 stop bit (8N1)
- **Flow Control**: None (no RTS/CTS or XON/XOFF)
- **Line Endings**: CR (0x0D) for command termination
- **Echo**: Local echo OFF (ROM provides echo)

### 8.2 Compatible Software
- **PuTTY**: Set to Serial, 8N1, no flow control
- **Tera Term**: Serial mode, appropriate baud rate
- **minicom**: Configure for 8N1, no hardware/software flow control
- **Windows Terminal**: Serial profile configuration
- **loadp2**: Official Parallax utility (recommended)

### 8.3 Development Tools Integration
- **PropellerIDE**: Built-in serial download support
- **FlexProp**: Integrated terminal and download
- **PNut**: Windows-based development environment
- **Custom tools**: Can implement protocol for automated systems

## 9. Performance Characteristics

### 9.1 Loading Speed vs Baud Rate
```
Baud Rate    Hex Efficiency    Base64 Efficiency    Max Transfer Rate
9600         44%               75%                  ~720 bytes/sec
115200       44%               75%                  ~8.6 KB/sec  
460800       44%               75%                  ~34.5 KB/sec
2000000      44%               75%                  ~150 KB/sec
```

### 9.2 Timing Specifications
- **Boot detection**: 100ms after power-on
- **First command timeout**: 60 seconds maximum
- **Subsequent commands**: No timeout after first command
- **Baud detection**: <10ms typical
- **Command processing**: <1ms for simple commands

### 9.3 Program Size Limits
- **Maximum program size**: Limited by available hub RAM (512KB or 1MB)
- **Practical limit**: ~400KB accounting for stack and variables
- **Boot ROM overhead**: 16KB reserved during boot only

## 10. Security Considerations

### 10.1 Access Control
- **Physical access required**: Serial connection needed
- **No authentication**: Protocol has no password protection
- **Boot pin control**: P61 can be grounded to disable serial boot
- **No encryption**: Data transmitted in plain text

### 10.2 Attack Surface
- **Limited exposure**: Only available during boot phase
- **Memory isolation**: Boot ROM becomes inaccessible after program launch
- **No persistent storage**: ROM cannot be modified by loaded programs

### 10.3 Production Deployment
- **Disable serial boot**: Ground P61 in production to prevent unauthorized access
- **Alternative boot sources**: Use SPI flash or SD card for secure boot
- **Physical security**: Protect serial pins from unauthorized access

## 11. Protocol Verification Test Cases

### 11.1 Basic Communication Tests
```
Test 1: Auto-baud detection at 115200
Expected: "> " prompt appears, commands accepted

Test 2: Prop_Chk command
Send: "Prop_Chk\r"
Expected: "Prop_Ver Au\r\n.\r\n> "

Test 3: Invalid command
Send: "Invalid_Cmd\r" 
Expected: "?\r\n> "
```

### 11.2 Data Loading Tests
```
Test 4: Minimal Intel Hex program
Send: "Prop_Hex\r"
Send: ":020000040000FA\r"
Send: ":10000000214601360121470136007EFE09D21940CC\r"
Send: ":00000001FF\r"
Expected: ".\r\n" then program execution

Test 5: Base64 loading
Send: "Prop_Txt ~\r"
Send: "UHJvcAQAAAAAAAIAAABA//8=\r"
Send: "~\r"
Expected: ".\r\n" then program execution
```

### 11.3 Error Condition Tests
```
Test 6: Checksum failure
Send hex data with invalid checksum
Expected: "?\r\n> " (error and return to prompt)

Test 7: Invalid hex format
Send: ":GG000000...\r"
Expected: "?\r\n> " (error on invalid hex digits)

Test 8: Communication timeout (if implemented)
Wait 60+ seconds without sending data
Expected: Return to boot sequence or timeout handling
```

### 11.4 Multi-Chip Tests (if applicable)
```
Test 9: INA masking
Configure INA pattern, verify selective response

Test 10: Broadcast mode
Send command to multiple chips, verify all respond
```

## 12. Implementation Notes for Verification

### 12.1 Critical Implementation Details
- **Command parsing**: Case-sensitive ASCII strings
- **Response timing**: Responses should be immediate (<1ms)
- **Echo handling**: All received characters echoed back to host
- **Checksum calculation**: Standard Intel Hex algorithm
- **Base64 decoding**: RFC 4648 compliant, ignore whitespace

### 12.2 Common Implementation Pitfalls
- **Baud rate tolerance**: Must handle ±2% baud rate variation
- **Line ending handling**: CR (0x0D) vs CRLF (0x0D,0x0A)
- **Character echo**: Must echo exactly as received
- **Timeout behavior**: Ensure proper timeout handling
- **Memory layout**: Respect fixed program header format

### 12.3 Verification Checklist
- [ ] Auto-baud detection works across full range (9600-2Mbaud)
- [ ] All four core commands implemented correctly
- [ ] Intel Hex parsing includes checksum validation
- [ ] Base64 decoding handles whitespace and padding
- [ ] Program checksum validation before execution
- [ ] Proper error responses ('?' character)
- [ ] Character echo functionality
- [ ] Multi-chip masking (if required)
- [ ] Compatible with standard terminal software

## 13. Reference Implementation

### 13.1 ROM Source Code Location
The actual Boot ROM source code can be found in the P2 knowledge base at:
- `engineering/ingestion/sources/rom-booter/` - ROM boot loader listings
- Analysis shows complete implementation details

### 13.2 Test Tools
- **loadp2**: Official Parallax command-line utility  
- **PropellerIDE**: Graphical development environment
- **Custom test scripts**: Python/C implementations for automated testing

### 13.3 Additional Documentation
- P2 Silicon Documentation v35: Complete protocol specification
- P2 Datasheet: Hardware requirements and pin assignments
- Boot ROM Analysis: Implementation details and optimization notes

---

## Appendix A: Command Reference Quick Sheet

| Command | Purpose | Parameters | Response |
|---------|---------|------------|-----------|
| `Prop_Chk` | Verify communication | None | `Prop_Ver Au` |
| `Prop_Clk` | Set clock | P1 P2 P3 | `.` |
| `Prop_Hex` | Load Intel Hex | Hex records | `.` after EOF |
| `Prop_Txt` | Load Base64 | Base64 + `~` | `.` after `~` |

## Appendix B: Error Code Reference

| Response | Meaning | Action |
|----------|---------|--------|
| `> ` | Ready for command | Send command |
| `.` | Success/Processing | Continue |
| `?` | Error occurred | Check command, retry |

## Appendix C: Pin Assignment Summary

| Pin | Direction | Function | Notes |
|-----|-----------|----------|--------|
| P63 | Input | Serial RX | Host → P2 |
| P62 | Output | Serial TX | P2 → Host |  
| P61 | Input | Boot Enable | Pull HIGH to enable |

---

**Document Status**: ✅ Complete for Protocol Verification  
**Validation Ready**: All implementation details specified for independent verification  
**Authority Level**: Based on official P2 documentation and ROM analysis