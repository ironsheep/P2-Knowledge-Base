# P2 Debugger Serial Protocol - Complete Specification

**Document Date**: 2025-08-30  
**Source**: Spin2_debugger.spin2 v51 (2025.04.02)  
**Purpose**: Complete protocol specification for P2 debugger communication  
**Key Finding**: The actual debugger protocol packet is **416 bytes**, not 80 bytes as sometimes referenced

---

## ⚠️ IMPORTANT CONCEPTUAL SEPARATION

### System Status Messages vs. Debugger Protocol

**COGINIT Messages**: These are **system status messages**, NOT part of the debugger protocol itself:
- Generated whenever a COG starts (with or without debugging)
- Simply inform which COGs are running
- ASCII text format for human readability
- Independent of debugger communication protocol

**Debugger Protocol**: The actual debugging communication protocol:
- Begins with the 416-byte breakpoint packet
- Binary format for efficiency
- Bidirectional command/response system
- Used for actual debugging operations

---

## 1. System Status Messages (NOT Protocol)

### 1.1 COGINIT Message (ASCII Text)

**PURPOSE**: System notification that a COG has started - independent of debugging protocol

When a COG is initialized, it sends an ASCII status message:

**Format**: `"CogN  INIT XXXXXXXX XXXXXXXX [load|jump]\r\n"`

**Field Breakdown**:
- `CogN` - COG identifier where N is 0-7 (4 bytes + 2 spaces = 6 bytes)
  - Line 639: `setnib _cog,cogn,#6` modifies the '0' in "Cog0  " string
  - Each COG gets its unique number inserted into the template string
- `INIT` - Fixed literal indicating initialization (4 bytes + 1 space = 5 bytes)
- `XXXXXXXX` - PTRB value in hex (8 bytes)
- ` ` - Space separator (1 byte)
- `XXXXXXXX` - PTRA value in hex (8 bytes)
- `[load|jump]` - Operation type (5-6 bytes including space)
- `\r\n` - Carriage return + line feed (2 bytes)

**Total Size**: 36-37 bytes (fixed for each COG)

**Examples**:
```
Cog0  INIT 00000000 00000000 load\r\n    # COG 0 loading from hub $00000000
Cog1  INIT 00001000 00000800 jump\r\n    # COG 1 jumping to hub $00001000
Cog7  INIT 0000FC00 00000000 load\r\n    # COG 7 loading from hub $0000FC00
```

### 1.2 Optional Timestamp Extension

If bit 31 of `_rxpin_` is set (line 644), a timestamp is prepended:

**Format**: `"CogN  HHHHHHHH_HHHHHHHH  INIT ..."`

Where:
- `HHHHHHHH` - CTH (upper 32 bits of 64-bit counter)
- `_` - Separator
- `HHHHHHHH` - CTL (lower 32 bits of 64-bit counter)
- Total adds 19 bytes to the message

### 1.3 COG Differentiation

**Each COG's message differs only in**:
1. The COG number (0-7) in the "CogN" field
2. The PTRA/PTRB values (COG's stack and code pointers)
3. The load/jump indicator

**Key Implementation Details**:
- Line 309: `cogid cogn` - Gets the actual COG ID (0-7)
- Line 983: `_cog byte "Cog0  ",0,0` - Template string
- Line 639: COG number dynamically inserted into nibble position 6

---

## 2. ACTUAL DEBUGGER PROTOCOL START

### 2.1 The Real Protocol: 416-Byte Breakpoint Packet

**THIS IS WHERE THE DEBUGGER PROTOCOL ACTUALLY BEGINS**

The debugger protocol starts with a **416-byte binary packet** (not 80 bytes!):

#### **Packet Structure Breakdown**

**Total Size: 416 bytes** consisting of:

##### **Part 1: Status Block (40 bytes)**

**Transmitted by lines 1010-1018**:

```
First Long: COG ID (4 bytes) - THIS IS WHY YOU SEE COG ID FIRST!
  - cogn (4 bytes) - COG ID (0-7) [**THIS EXPLAINS YOUR TRACE!**]

Following 9 longs:
  - brkcz (4 bytes) - Break status with C and Z flags
  - brkc  (4 bytes) - Break status with C flag only
  - brkz  (4 bytes) - Break status with Z flag only  
  - cth2  (4 bytes) - Upper 32 bits of 64-bit counter
  - ctl2  (4 bytes) - Lower 32 bits of 64-bit counter
  - stk0  (4 bytes) - Stack value 0
  - stk1  (4 bytes) - Stack value 1
  - stk2-stk7 - Additional stack values (not shown above)
  - freq  (4 bytes) - Clock frequency from RX pin repository
  - cond  (4 bytes) - BRK condition flags
```

**Subtotal**: 40 bytes

##### **Part 2: CRC Checksum Block (128 bytes)**

**Lines 1020-1031**: 64 16-bit CRC words for register groups
- Covers all COG registers in 16-register blocks
- Uses polynomial $8005 (reversed 15-bit)
- Allows host to detect which registers changed

**Subtotal**: 128 bytes

##### **Part 3: Hub Memory Checksums (248 bytes)**

**Lines 1033-1036**: 124 16-bit checksum words
- Covers hub memory from $00000 to $7BFFF
- 4KB blocks compressed to 16-bit checksums
- Uses SEUSSF instruction for compression

**Subtotal**: 248 bytes

#### **TOTAL DEBUGGER PROTOCOL PACKET: 416 BYTES**
- Part 1 (Status): 40 bytes
- Part 2 (CRC): 128 bytes  
- Part 3 (Checksums): 248 bytes
- **TOTAL**: **416 bytes of binary data**

### 2.2 Why This Matters for Logic Analyzer Traces

When looking at your logic analyzer:
1. **Ignore the ASCII COGINIT messages** - these are just status, not protocol
2. **Look for the 416-byte binary burst** - this is the actual protocol start
3. **First 4 bytes = COG ID** - this is why you see COG identification first
4. **Binary, not ASCII** - explains why the data looks different than expected
5. **416 bytes, not 80** - explains why packet boundaries didn't match expectations

---

## 3. Command/Response Protocol

### 3.1 Host → Debugger Commands (52 bytes)

After initial packet, debugger waits for commands (lines 1038-1043):

```
cmd_regs    (8 bytes)  - 2 longs: Register read request bitmap
cmd_sums    (16 bytes) - 4 longs: Hub checksum request bitmap  
cmd_read    (20 bytes) - 5 longs: Hub memory read addresses
cmd_cogbrk  (4 bytes)  - 1 long: COG break control flags
cmd_brk     (4 bytes)  - 1 long: Breakpoint condition update
```

### 3.2 Debugger → Host Responses

Based on commands received, debugger sends:

1. **Requested Registers** (lines 1045-1054)
   - 4 bytes per requested register
   - Only sends registers with corresponding bit set in cmd_regs

2. **Sub-4KB Hub Checksums** (lines 1056-1064)
   - 2 bytes per 128-byte sub-block
   - Only for regions with bits set in cmd_sums

3. **Raw Hub Memory** (lines 1066-1075)
   - Direct byte stream from requested addresses
   - Length encoded in upper 12 bits of address

4. **Smart Pin Values** (lines 1077-1090)
   - 1 byte pin mask (which pins have data)
   - 4 bytes per non-zero pin value

---

## 4. Special Protocol Features

### 4.1 18-bit Word Transmission Optimization

**Lines 439-445**: Words packed as 18-bit values for efficiency
```
Format: %HHHHHHHH_01_LLLLLLLL
- Allows single serial transmission
- Improves overlap of computation and transmission
```

### 4.2 COGBRK Remote Triggering

**Lines 1092-1098**: Host can trigger breakpoints in other COGs
- Sends COGBRK instruction to target COG
- Sets flag at COG's debug ISR location ($FFFC0+$D<<2)
- Target COG detects flag and enters debug mode

### 4.3 Fixed COG-Specific Memory Regions

Each COG has dedicated debug memory (hardcoded in P2 silicon):
```
COG 0: $FFF80-$FFFBF (buffer + ISR)
COG 1: $FFF00-$FFF3F
COG 2: $FFE80-$FFEBF
COG 3: $FFE00-$FFE3F
COG 4: $FFD80-$FFDBF
COG 5: $FFD00-$FFD3F
COG 6: $FFC80-$FFCBF
COG 7: $FFC00-$FFC3F
```

---

## 5. Protocol State Machine

### 5.1 Debugger States

1. **COGINIT**: Send ASCII init message → Send breakpoint packet → Wait for commands
2. **BREAKPOINT**: Send breakpoint packet → Wait for commands
3. **STALL**: Loop waiting for lock → Re-enter debugger
4. **EXIT**: Restore state → Enable next interrupt → Return to code

### 5.2 Message Triggers

- **COGINIT** (bit 23 of brkcz): Triggers ASCII "INIT" message
- **COGBRK** (flag at ptrb[$1D]): Remote breakpoint from another COG
- **DEBUG** (BRK instruction): Application-triggered breakpoint
- **MAIN** (bit 0 of cond): Main entry point break

---

## 6. Example Communication Sequences

### 6.1 COG 0 Initial Connection
```
→ "Cog0  INIT 00000000 00000000 load\r\n"    (37 bytes ASCII - SYSTEM STATUS)
→ [416-byte debugger packet begins here:]     ← ACTUAL PROTOCOL START
  → [Status block: 40 bytes binary - COG ID first!]
  → [CRC block: 128 bytes binary]  
  → [Hub checksums: 248 bytes binary]
← [Commands: 52 bytes binary]
→ [Requested data: variable length]
```

### 6.2 COG 3 Breakpoint Hit
```
→ [Status block with cogn=3: 40 bytes]
→ [CRC block: 128 bytes]
→ [Hub checksums: 248 bytes]
← [Commands: 52 bytes]
→ [Requested registers + memory]
```

### 6.3 Remote COG 5 Break Trigger
```
← [cmd_cogbrk with bit 5 set]
  (COG 5 receives COGBRK instruction)
  (COG 5 sets COGBRK flag and enters debugger)
→ "Cog5  ..." (from COG 5)
→ [COG 5's breakpoint packet]
```

---

## 7. Key Protocol Characteristics

1. **Protocol is 416 bytes**: Not 80 bytes as sometimes referenced
2. **COG ID is first**: First 4 bytes of protocol packet identify the COG
3. **Binary only**: The actual protocol is pure binary (COGINIT is separate)
4. **Compressed**: Checksums and CRCs minimize data transfer
5. **Bidirectional**: Full request/response command system
6. **Multi-COG**: Can debug all 8 COGs simultaneously
7. **Non-Intrusive**: Hardware ISR support preserves application state

## 8. Critical Clarifications for Logic Analyzer Analysis

### What You'll See on the Logic Analyzer

1. **ASCII Text (37 bytes)**: `"CogN  INIT..."` - This is NOT the protocol, just status
2. **Binary Burst (416 bytes)**: This IS the protocol
   - Bytes 0-3: COG ID (explains what you were seeing!)
   - Bytes 4-39: Status information
   - Bytes 40-167: CRC data
   - Bytes 168-415: Hub checksums
3. **Command Block (52 bytes)**: Host response
4. **Variable Data**: Based on commands

### Why "80 bytes" Was Confusing

The 80-byte reference likely came from:
- Misunderstanding or simplification
- Possibly an older protocol version
- Maybe someone counting only part of the packet
- Could be a specific configuration subset

**The actual protocol is definitively 416 bytes** as shown in the source code analysis.

---

## 8. Implementation Notes

- All multi-byte values are little-endian
- Serial format: 8-N-1 at configured baud rate
- TX pin must stay high when idle (line 58)
- RX pin used as clock frequency repository (lines 63-65)
- Lock[15] coordinates multi-COG debug access (line 201)

---

## 9. 🚨 CRITICAL DISCOVERY: Multi-COG Debug Blocking Behavior

### Lock #15 Serialization Creates Blocking

**This was previously unknown to the P2 community!** The debugger uses hardware lock #15 to serialize ALL debug output across COGs, creating a critical blocking behavior:

#### The Blocking Mechanism

```spin2
' From Spin2_debugger.spin2 lines 201-202:
.wait    locktry #15    wc    'wait for lock[15] so that we own the save buffer and tx/rx pins
if_nc    jmp    #.wait        'BUSY-WAIT loop until lock acquired!

' ... debug operations ...

' Line 235:
lockrel #15    'release lock[15] so other cogs can own the save buffer and tx/rx pins
```

#### What This Means

1. **Only ONE COG can send debug messages at a time**
   - Lock #15 protects both the save buffer AND the TX/RX pins
   - Other COGs attempting to debug will spin-wait for the lock

2. **Blocking Sequence**:
   - COG2 sends debug init → acquires lock #15
   - COG3 tries to send debug init → stuck at `locktry #15` 
   - COG3 spins in tight loop until COG2 releases lock
   - If COG2 waits for host response while holding lock → DEADLOCK!

3. **The Deadlock Scenario**:
   ```
   COG2: Send init message (holding lock #15)
   COG2: Wait for host acknowledgment (STILL holding lock)
   COG3: Try to send init message
   COG3: Stuck spinning at locktry #15 forever!
   Result: Only COG2's debug output visible, COG3 appears dead
   ```

#### Why This Matters

- **Debug tools must respond quickly** to prevent blocking other COGs
- **Multi-COG debug messages arrive serialized**, not simultaneously
- **Host cannot wait** for all COGs before responding to any
- **Each COG's session** must be handled independently and promptly

#### Implications for Debugging

1. **For Debug Tool Developers**:
   - Must handle serialized message arrival
   - Cannot assume simultaneous COG initialization
   - Must respond promptly to prevent system-wide blocking
   - Timeout handling becomes critical

2. **For P2 Developers**:
   - Understand that debug output is strictly serialized
   - One slow/hung COG can block all other debug output
   - Debug initialization happens one COG at a time

3. **For Troubleshooting**:
   - Missing COG debug output may indicate blocking, not failure
   - Check if earlier COG is waiting for host response
   - Look for spin-wait patterns in COG execution

This protocol enables sophisticated debugging while maintaining minimal impact on the running application, with clear differentiation between COGs and efficient data transfer mechanisms.