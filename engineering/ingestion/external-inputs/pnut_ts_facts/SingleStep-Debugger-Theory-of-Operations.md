# Single-Step Debugger: Theory of Operations

> **Scope**: This document covers the PNut single-step debugger for the Parallax Propeller 2 (P2) microcontroller. It describes the complete debug system: the P2-side debug stub, the host-side debugger window, the serial communications protocol, the screen layout, user interaction, and breakpoint handling.
>
> **Reference Source**: `REF-V52A/` directory — PNut v52a Pascal and x86 assembly source. Key files: `DebuggerUnit.pas` (host UI), `DebugUnit.pas` (dispatcher), `Spin2_debugger.spin2` (P2 stub, embedded in `p2com.asm`), `GlobalUnit.pas` (shared state), `SerialUnit.pas` (serial layer).
>
> **Upstream Repository**: https://github.com/parallaxinc/P2_PNut_Public

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [P2-Side Debug Stub](#2-p2-side-debug-stub)
   - [Protected Hub RAM Layout](#21-protected-hub-ram-layout)
   - [Debugger Setup Sequence](#22-debugger-setup-sequence)
   - [Debug ISR (Interrupt Service Routine)](#23-debug-isr-interrupt-service-routine)
   - [Debug Entry and State Capture](#24-debug-entry-and-state-capture)
   - [Register Read/Write Mechanism](#25-register-readwrite-mechanism)
   - [Overlay Architecture](#26-overlay-architecture)
   - [Debug Exit and Stall Mechanism](#27-debug-exit-and-stall-mechanism)
3. [Communications Protocol](#3-communications-protocol)
   - [Serial Layer](#31-serial-layer)
   - [Byte Dispatch (Host Entry Point)](#32-byte-dispatch-host-entry-point)
   - [Breakpoint Exchange Protocol](#33-breakpoint-exchange-protocol)
   - [CRC-Based Change Detection](#34-crc-based-change-detection)
   - [Hub Read Request Format](#35-hub-read-request-format)
   - [Smart Pin Data Format](#36-smart-pin-data-format)
   - [BRK Condition Word Format](#37-brk-condition-word-format)
   - [Stall vs. Go Command](#38-stall-vs-go-command)
   - [COGBRK (Asynchronous Break)](#39-cogbrk-asynchronous-break)
4. [Debugger State Machine](#4-debugger-state-machine)
   - [States](#41-states)
   - [State Transitions](#42-state-transitions)
   - [Single-Step Mechanics](#43-single-step-mechanics)
   - [Repeat Mode Throttling](#44-repeat-mode-throttling)
   - [Breakpoint Timeout and Dimming](#45-breakpoint-timeout-and-dimming)
5. [Screen Layout and Drawing](#5-screen-layout-and-drawing)
   - [Window Setup](#51-window-setup)
   - [Triple-Buffer Rendering](#52-triple-buffer-rendering)
   - [Grid System and Coordinates](#53-grid-system-and-coordinates)
   - [Panel Layout Map](#54-panel-layout-map)
   - [Panel Definitions](#55-panel-definitions)
   - [Color Scheme](#56-color-scheme)
   - [Anti-Aliased Rendering System](#57-anti-aliased-rendering-system)
   - [Drawing Sequence Per Breakpoint](#58-drawing-sequence-per-breakpoint)
6. [Display Regions in Detail](#6-display-regions-in-detail)
   - [Register and LUT Heatmap Bitmaps](#61-register-and-lut-heatmap-bitmaps)
   - [C Flag, Z Flag, and Program Counter](#62-c-flag-z-flag-and-program-counter)
   - [SKIP/SKIPF Pattern](#63-skipskipf-pattern)
   - [XBYTE Status](#64-xbyte-status)
   - [Clock Ticks (CT)](#65-clock-ticks-ct)
   - [Disassembly View](#66-disassembly-view)
   - [Register Watch List](#67-register-watch-list)
   - [Special Function Registers (SFR)](#68-special-function-registers-sfr)
   - [Event Flags](#69-event-flags)
   - [Execution Mode](#610-execution-mode)
   - [Stack Registers](#611-stack-registers)
   - [Interrupt Status](#612-interrupt-status)
   - [Pointer Data (FPTR, PTRA, PTRB)](#613-pointer-data-fptr-ptra-ptrb)
   - [Status Indicators](#614-status-indicators)
   - [Pin Registers](#615-pin-registers)
   - [Smart Pin Watch](#616-smart-pin-watch)
   - [Hub Data Viewer](#617-hub-data-viewer)
   - [Hub Heatmap](#618-hub-heatmap)
   - [Hint Bar](#619-hint-bar)
7. [Breakpoint Control Buttons](#7-breakpoint-control-buttons)
   - [Button Layout](#71-button-layout)
   - [Break Condition Buttons](#72-break-condition-buttons)
   - [Go/Stop/Break Button](#73-gostopbreak-button)
8. [User Interaction](#8-user-interaction)
   - [Keyboard Shortcuts](#81-keyboard-shortcuts)
   - [Mouse Click Actions](#82-mouse-click-actions)
   - [Mouse Wheel Actions](#83-mouse-wheel-actions)
   - [Mouse Hover (Hint System)](#84-mouse-hover-hint-system)
9. [Debug Compilation](#9-debug-compilation)
   - [Debug Data Table](#91-debug-data-table)
   - [Debug Record Format (Bytecodes)](#92-debug-record-format-bytecodes)
   - [PASM2 Debug Value Encoding](#93-pasm2-debug-value-encoding)
   - [Debug Record Deduplication](#94-debug-record-deduplication)
   - [Debug Data Collapse](#95-debug-data-collapse)
   - [Debugger Insertion into Binary](#96-debugger-insertion-into-binary)
   - [Configuration Symbols](#97-configuration-symbols)
10. [Host-Side Session Lifecycle](#10-host-side-session-lifecycle)
    - [Debug Session Startup](#101-debug-session-startup)
    - [Debug Receive Loop](#102-debug-receive-loop)
    - [Debug Session Shutdown](#103-debug-session-shutdown)
11. [Appendix: Constants Reference](#11-appendix-constants-reference)
    - [Debugger Message Indices](#111-debugger-message-indices)
    - [Memory Size Constants](#112-memory-size-constants)
    - [SFR Register Names](#113-sfr-register-names)
    - [Event Names](#114-event-names)
    - [Debug ROM Disassembly Strings](#115-debug-rom-disassembly-strings)

---

## 1. Architecture Overview

The PNut single-step debugger is a three-layer system spanning the host PC and the P2 microcontroller:

```
+---------------------------+          Serial Link          +---------------------------+
|       HOST PC (Windows)   |  <=========================>  |    PROPELLER 2 (P2)       |
|                           |     2 Mbaud, 8-N-1, async     |                           |
|  EditorUnit.pas           |                               |  Spin2_debugger.spin2     |
|    - Compiles source      |                               |    - Debug ISR            |
|    - Inserts debugger     |                               |    - State capture        |
|    - Downloads binary     |                               |    - Serial protocol      |
|                           |                               |    - Overlay architecture |
|  DebugUnit.pas            |                               |                           |
|    - Byte dispatcher      |                               |  User Application         |
|    - Text console         |                               |    - BRK instructions     |
|    - Display routing      |                               |    - DEBUG statements     |
|                           |                               |                           |
|  DebuggerUnit.pas         |                               |                           |
|    - Single-step UI       |                               |                           |
|    - Breakpoint protocol  |                               |                           |
|    - Screen rendering     |                               |                           |
|    - User interaction     |                               |                           |
|                           |                               |                           |
|  SerialUnit.pas           |                               |                           |
|    - Ring-buffered I/O    |                               |                           |
|    - Hardware discovery   |                               |                           |
+---------------------------+                               +---------------------------+
```

**Compile-time** (`p2com.asm`): The compiler generates debug records from `DEBUG` statements, builds a debug data table, and inserts the debugger stub into the binary image.

**P2-side runtime** (`Spin2_debugger.spin2`): A PASM2 program prepended to the application binary. It installs the debug ISR into each cog, then launches the user's application. When a BRK fires, the ISR captures complete cog state and communicates with the host.

**Host-side runtime** (`DebuggerUnit.pas`): A per-cog graphical debugger window that receives cog state, renders the display, accepts user input (step/run/break), and sends commands back to the P2.

---

## 2. P2-Side Debug Stub

### 2.1 Protected Hub RAM Layout

The debugger reserves the top 16KB of hub RAM (`$FC000`-`$FFFFF`), protected from user-application access via `HUBSET`:

| Address Range | Size | Purpose |
|---|---|---|
| `$FC000` | Variable | DEBUG data table (bytecode records copied from compiler output) |
| `$FEA00` | ~1976 bytes | Save buffer for cog registers `$010`-`$1F7` (shared, one cog at a time via lock[15]) |
| `$FF1A0` | ~2656 bytes | Debugger program code + overlays + data |
| `$FFC00`-`$FFFFF` | 1024 bytes | Per-cog ISR and register buffers (8 cogs x 128 bytes) |

Each cog gets 128 bytes of fixed-address space, split into two 64-byte halves:

| Offset from `$FFF80 - cog*$80` | Purpose |
|---|---|
| `$00`-`$3F` (16 longs) | Register save buffer for `$000`-`$00F` (used by ROM debug entry/exit) |
| `$40`-`$7F` (16 longs) | Debug ISR code (loaded from debugger at setup) |

Within the ISR area, two special longs serve as per-cog mailbox:

| Offset | Purpose |
|---|---|
| `long[$C]` (byte offset `$30`) | BRK condition word (controls what triggers the next break) |
| `long[$D]` (byte offset `$34`) | COGBRK flag (set by another cog to force an async break) |

### 2.2 Debugger Setup Sequence

When the binary loads, the debugger stub runs first (before the user's application):

1. Configure TX pin (default 62) as async serial output
2. Configure RX pin (default 63) as long repository holding clock frequency
3. Set clock mode: start external clock source, wait 10ms, switch to PLL
4. Apply startup delay (from `DEBUG_DELAY` constant, in milliseconds)
5. Allocate lock[15] for mutual exclusion (all other locks returned to the pool)
6. Clear upper hub RAM (`$FC000`-`$FFFFF`)
7. Write debug ISR code to all 8 cog ISR buffers
8. Move debugger program to `$FF1A0`
9. Move DEBUG data table to `$FC000`
10. Enable debugging and protect upper hub RAM via `HUBSET`
11. Move application code down to `$00000` (it was offset by the debugger size)
12. Clear trailing hub RAM (gap left after moving application down)
13. Relaunch cog 0 from `$00000` to start the user's application

### 2.3 Debug ISR (Interrupt Service Routine)

The P2 silicon provides a ROM-based debug entry/exit sequence at cog addresses `$1F8`-`$1FF`. When a BRK fires:

```
ROM Entry ($1F8-$1FC):
  $1F8: SETQ    #$F              ; save registers $000..$00F to hub buffer
  $1F9: WRLONG  0, #$FFF80-cog<<7
  $1FA: SETQ    #$F              ; load registers $000..$00F from hub ISR code
  $1FB: RDLONG  0, #$FFFC0-cog<<7
  $1FC: JMP     #\0              ; execute ISR at register $000

ROM Exit ($1FD-$1FF):
  $1FD: SETQ    #$F              ; restore registers $000..$00F from hub buffer
  $1FE: RDLONG  0, #$FFF80-cog<<7
  $1FF: RETI0                    ; return from debug interrupt
```

The debug ISR occupies registers `$000`-`$00F` (16 longs). It is designed to be compact since these are the only registers available before the full debugger loads:

```
$000: cth      GETCT  cth  WC          ; capture 64-bit cycle counter (high word)
$001: ctl      GETCT  ctl              ; capture 64-bit cycle counter (low word)
$002: regh     AUGS   #sav_addr        ; load save buffer address ($FEA00) upper bits
$003: cond     MOV    regh, #(sav_addr & $1FF)  ; complete address (cond reused later)
$004: .wait    LOCKTRY #15  WC         ; acquire lock[15] (mutual exclusion)
$005:  if_nc   JMP    #.wait           ; spin until lock acquired
$006:          SETQ   #($1F7-$010)     ; save registers $010..$1F7 to save buffer
$007:          WRLONG $010, regh
$008:          SETQ   #($1F7-$004)     ; load debugger code into $004..$1F7
$009:          RDLONG $004, ##dbg_addr ; (augmented address spans two instructions)
$00A:          ---                     ; (second word of augmented RDLONG)
$00B:          JMP    #\debug_entry    ; jump into loaded debugger
$00C: brk_cond LONG   $00000010       ; BRK condition word (initial: break on BRK)
$00D: cogbrk   LONG   0               ; COGBRK flag (initially clear)
$00E:          ---                     ; (unused)
$00F:          ---                     ; (unused)
```

**Key design insight**: The ISR is only 16 longs. It captures timing, acquires a lock, saves all working registers to hub, then **overlays the entire cog** (`$004`-`$1F7`) with the debugger program from hub RAM. The user's code is completely swapped out during debug.

### 2.4 Debug Entry and State Capture

Once the debugger overlay is loaded, `debug_entry` captures complete cog state into named registers:

| Register | Source | Content |
|---|---|---|
| `cogn` | `COGID` | Cog number (0-7) |
| `brkcz` | `GETBRK WCZ` | Break status with both C and Z |
| `brkc` | `GETBRK WC` | Break status with C only |
| `brkz` | `GETBRK WZ` | Break status with Z only (SKIP pattern) |
| `cth2` | (from ISR) | Clock ticks high 32 bits |
| `ctl2` | (from ISR) | Clock ticks low 32 bits |
| `stk0`-`stk7` | `POP` x8 | Hardware stack (8 levels, top to bottom) |
| `iret` | `INB` | Debug interrupt return address (PC + C/Z flags) |
| `fptr` | `GETPTR` | FIFO pointer (RFxx/WFxx address) |
| `ptra_` | saved PTRA | PTRA register value |
| `ptrb_` | saved PTRB | PTRB register value |
| `freq` | RX pin repo | Clock frequency in Hz |

These 20 values (`cogn` through BRK condition) form the **debugger message** sent to the host.

The debugger then sets up the serial link by computing the baud divisor dynamically: `clkfreq / baud` via a 33-iteration long division (avoiding CORDIC to preserve user state). Both TX and RX pins are configured as async serial 8-N-1.

**Decision logic** after state capture:

1. If returning from STALL (bit 11 of saved `cond` set) -> go to breakpoint handler
2. If COGINIT detected (bit 23 of `brkcz`) -> output "CogN INIT" message, then check conditions
3. If COGBRK flag set -> clear flag, go to breakpoint handler
4. If COGINIT but BRK condition lacks COGINIT/MAIN bits -> exit (no break needed)
5. If DEBUG bit set in condition and BRK code != 0 -> process as normal `DEBUG` message
6. Otherwise -> go to breakpoint handler

### 2.5 Register Read/Write Mechanism

The `rdreg`/`rwreg` routines handle reading/writing any cog register address, accounting for the overlay:

| Address Range | Storage Location |
|---|---|
| `$000`-`$00F` | Hub buffer at per-cog ISR area (saved by ROM entry) |
| `$010`-`$1F7` | Hub save buffer at `$FEA00` (saved by ISR) |
| `$1F8`-`$1F9` | `ptra_`/`ptrb_` saved copies in debugger registers |
| `$1FA`-`$1FF` | Direct access via `ALTS`/`ALTD` (SFRs: DIRA/DIRB/OUTA/OUTB/INA/INB) |
| `$200`-`$3FF` | LUT RAM via `RDLUT`/`WRLUT` |

### 2.6 Overlay Architecture

The debugger uses an overlay strategy to fit its code within the cog's 496-register program space (`$004`-`$1F7`):

- **Static portion**: Core debug entry, exit, serial TX/RX, state capture
- **Overlay portions**: Breakpoint handler, normal DEBUG message handler — loaded from hub as needed via `RDLONG` with `SETQ`

When a breakpoint occurs, the breakpoint handler overlay is loaded into the overlay area, overwriting the normal-message handler.

### 2.7 Debug Exit and Stall Mechanism

`debug_done` prepares to exit:

1. Wait for serial TX to finish
2. Restore RX pin to repository mode (stores clock frequency)
3. Disable TX/RX smart pins
4. Restore hardware stack (`PUSH stk7` through `PUSH stk0`)
5. Restore PTRA and PTRB
6. Compute delay value (~1ms for normal exit)

Then the exit path diverges:

**Normal exit** (bit 11 of `cond` clear):
1. Enable COGBRK monitoring (set bit 8 in BRK condition)
2. Restore registers `$010`-`$1F7` from save buffer
3. Release lock[15]
4. Execute `BRK cond` to re-arm the debug interrupt with the new condition
5. Jump to ROM exit (`$1FD`): restores `$000`-`$00F`, executes `RETI0`

**Stall** (bit 11 of `cond` set):
1. Restore registers `$010`-`$1F7` from save buffer
2. Release lock[15]
3. Wait ~64ms (allowing other cogs to use the serial link)
4. Re-acquire lock[15]
5. Re-save registers `$010`-`$1F7`
6. Reload the debugger overlay from hub
7. Jump back to `debug_entry` for another protocol cycle

The stall loop creates a polling behavior: the halted cog repeatedly contacts the host (~15 times/second), allowing the host to display state and eventually send a "Go" command.

---

## 3. Communications Protocol

### 3.1 Serial Layer

The serial link operates at a configurable baud rate (default: same as download baud, typically 2 Mbaud), 8-N-1, no flow control.

**P2-side serial primitives** (in `Spin2_debugger.spin2`):

| Routine | Format |
|---|---|
| `txbyte` | Standard 8-bit async transmit via smart pin |
| `txword` | Packs 16-bit word as 18-bit frame: `%HHHHHHHH_01_LLLLLLLL` for single-transmit efficiency |
| `txlong` | Two `txword` calls (lower word first, then upper word) |
| `rxlong` | Receives 4 bytes, shifting into long LSB-first |

**Host-side serial primitives** (in `SerialUnit.pas`):

| Function | Description |
|---|---|
| `TByte(x)` | Enqueue one byte to 2MB TX ring buffer |
| `TLong(x)` | Send 32-bit value as 4 bytes, LSB first |
| `RByte` | Blocking read of one byte from 16MB RX ring buffer (500ms timeout) |
| `RWord` | Read 16-bit value (2 bytes, LSB first) |
| `RLong` | Read 32-bit value (4 bytes, LSB first) |
| `ReturnRByte` | Push back one byte (used when dispatcher needs to re-read a byte) |

The host uses a dedicated serial thread (`TSerialThread`) at `tpTimeCritical` priority that continuously pumps TX and RX ring buffers.

### 3.2 Byte Dispatch (Host Entry Point)

Every byte received from the P2 passes through `DebugForm.ChrIn(x)`:

| Byte Value | Action |
|---|---|
| `0`-`7` | **Debugger breakpoint**: Push byte back via `ReturnRByte`, create `TDebuggerForm` for that cog if not open, call `DebuggerForm[x].Breakpoint` for full protocol exchange |
| `27` (ESC) | **End debug session**: Set `DebugActive := False`, close form |
| `$60` (backtick) | **Start display string**: Begin accumulating bytes for a `DEBUG()` display command |
| `13` (CR, during display string) | **End display string**: Parse via `P2ParseDebugString`, create/update display windows |
| `$20`-`$7F` | **Printable character**: Render to text console |
| `13` (CR, normal) | **Newline**: Scroll terminal |
| `9` (TAB) | **Tab**: Advance to next 8-column boundary |

The cog ID byte (0-7) is the first byte of a breakpoint message. The dispatcher creates a per-cog `TDebuggerForm` instance on first contact and delegates the entire serial exchange to it.

### 3.3 Breakpoint Exchange Protocol

The protocol is strictly synchronous and lockstep. Every breakpoint triggers this complete exchange:

```
P2 ----[20 longs: cog state]----> Host
P2 ----[64 words: cog CRCs]----> Host
P2 ----[124 words: hub CRCs]---> Host
                                  Host processes, determines what changed
P2 <---[8 bytes: reg request]---- Host
P2 <---[16 bytes: hub request]--- Host
P2 <---[5 longs: hub reads]----- Host
P2 <---[1 long: COGBRK]--------- Host
P2 <---[1 long: BRK command]---- Host
                                  P2 gathers requested data
P2 ----[N longs: reg blocks]---> Host
P2 ----[N words: hub sub-CRCs]-> Host
P2 ----[N bytes: hub reads]----> Host
P2 ----[64 pins: smart data]---> Host
                                  Host renders display
                                  P2 executes COGBRK requests
                                  P2 installs new BRK condition
                                  P2 exits or stalls
```

#### Phase 1: P2 Sends Initial State

1. **Debugger message**: 20 longs (`DebuggerMsgSize`), transmitted via `txlong`. Contains complete cog state snapshot (see [Appendix 11.1](#111-debugger-message-indices)).

2. **Cog/LUT CRC words**: 64 words via `txword`. Each word is a 16-bit CRC (polynomial `$8005`) of a 16-register block, covering all 1024 addresses (`$000`-`$3FF` = cog + LUT). Computed using P2 `CRCNIB` instruction (8 nibbles per register = 32 bits).

3. **Hub checksum words**: 124 words via `txword`. Each word is a checksum of a 4KB hub block (`$00000`-`$7BFFF`). Computed as: sum all longs in the block, apply `SEUSSF` (non-linear hash), add upper and lower 16-bit halves.

#### Phase 2: Host Sends Requests

4. **Register block request bitmap**: 64 bits packed as 8 bytes (MSb-first within each byte). Bit N = 1 if `CogBlock[N] != CogBlockOld[N]` (CRC changed since last break).

5. **Hub sub-block request bitmap**: 124 bits packed as 16 bytes (padded to 128-bit boundary). Bit N = 1 if `HubBlock[N] != HubBlockOld[N]`.

6. **Hub read requests**: 5 longs via `TLong`, each formatted as `(byte_count << 20) | (address & $FFFFF)`:

   | Request | Content | Typical Size |
   |---|---|---|
   | 0 | Disassembly code (hub-execute only; 0 if cog-execute) | 64 bytes (16 longs) |
   | 1 | FPTR pointer data (centered on FPTR address) | 14 bytes |
   | 2 | PTRA pointer data (centered on PTRA address) | 14 bytes |
   | 3 | PTRB pointer data (centered on PTRB address) | 14 bytes |
   | 4 | Hub data viewer content | 128 bytes |

7. **COGBRK request**: 1 long via `TLong`. Bit N = 1 to force an asynchronous break in cog N. Cleared to 0 after sending.

8. **STALL/BRK command**: 1 long via `TLong`. Either `$00000800` (stall — keep cog halted) or a break condition word (resume execution with these break triggers).

#### Phase 3: P2 Sends Requested Data

9. **Changed register blocks**: For each of the 64 blocks whose bit was set in the request, send 16 longs via `txlong` (the full contents of registers in that block).

10. **Hub sub-block CRCs**: For each changed 4KB hub block, send 32 sub-block checksums (one word per 128-byte sub-block) via `txword`. This enables fine-grained hub heatmap tracking.

11. **Hub read data**: Raw bytes for each of the 5 read requests:
    - Disassembly: 16 longs via `txlong` (if requested)
    - FPTR/PTRA/PTRB: 14 bytes each via `txbyte`
    - Hub data: 128 bytes via `txbyte`

12. **Smart pin data**: For each group of 8 pins (8 groups total):
    - 1 byte: bitmask of pins with non-zero RQPIN values
    - For each set bit: 1 long via `txlong` (the RQPIN readback value)

### 3.4 CRC-Based Change Detection

The protocol uses a two-level change detection scheme to minimize serial traffic:

**Cog/LUT registers** (1024 registers, 4KB):
- 64 blocks of 16 registers each
- 16-bit CRC per block using polynomial `$8005`
- Only changed blocks are retransmitted (16 longs = 64 bytes each)
- On first connection, all CRCs differ from the initial value, so all blocks are sent

**Hub memory** (507,904 bytes):
- **Top level**: 124 blocks of 4KB each, with coarse checksums
- **Sub level**: Each 4KB block divided into 32 sub-blocks of 128 bytes
- Only changed top-level blocks have their sub-block checksums retransmitted
- Sub-block checksums drive the hub heatmap display
- Actual hub byte data is only read for specific viewer requests (not bulk transfer)

### 3.5 Hub Read Request Format

Each hub read request is a single 32-bit long:

```
Bits 31..20: Byte count (0 = no read requested)
Bits 19..0:  Start address in hub RAM
```

The host requests exactly the data it needs for the current display state. For example, if the disassembly view shows cog-execute code, request 0 is sent as `$00000000` (no hub code needed).

### 3.6 Smart Pin Data Format

Smart pin data uses a compressed encoding:

```
For each group of 8 pins (8 iterations):
  1 byte: enable mask (bit N = pin has non-zero RQPIN)
  For each set bit in mask:
    1 long: RQPIN value for that pin
```

This avoids transmitting data for inactive pins. Total: 8 mask bytes + 0 to 64 longs depending on active pin count.

### 3.7 BRK Condition Word Format

The BRK condition word controls what triggers the debug ISR. It is both stored in the cog's ISR area and sent as the STALL/BRK command:

| Bits | Mask | Meaning |
|---|---|---|
| 0 | `$001` | Break on MAIN instructions (single-step main code) |
| 1 | `$002` | Break on INT1 instructions |
| 2 | `$004` | Break on INT2 instructions |
| 3 | `$008` | Break on INT3 instructions |
| 4 | `$010` | Break on DEBUG instruction (BRK with non-zero code) |
| 5 | `$020` | Break on INT1 entry |
| 6 | `$040` | Break on INT2 entry |
| 7 | `$080` | Break on INT3 entry |
| 8 | `$100` | Break on COGINIT (independent flag, also enables COGBRK after init) |
| 9 | `$200` | Break on event (event ID in bits 15..12) |
| 10 | `$400` | Break on address match (address in bits 31..12) |
| 11 | `$800` | STALL flag (keep cog halted in debug ISR polling loop) |
| 15..12 | `$F000` | Event number (1-15) when bit 9 is set |
| 31..12 | `$FFFFF000` | Break address (20-bit) when bit 10 is set |

### 3.8 Stall vs. Go Command

- **`$00000800`** (StallCmd): Bit 11 set. The P2 enters its stall loop, waiting ~64ms and contacting the host again. The cog remains halted.
- **Any other value**: The P2 exits the debug ISR via `RETI0`, resuming execution with this break condition. The cog runs until the condition is met, then re-enters the debug ISR.

### 3.9 COGBRK (Asynchronous Break)

`RequestCOGBRK` is a global bitmask on the host. Setting bit N causes the P2 to execute `COGBRK` for cog N during the next breakpoint exchange. The target cog must have debugging enabled.

**Important limitation**: Async break only works if another cog is currently in its debug ISR (and thus processing the protocol). If no other cog is in debug, there is no way to force a break from the host.

---

## 4. Debugger State Machine

### 4.1 States

The debugger operates in three main states:

**Halted (A)**: The cog is stopped at a breakpoint. The display is fully rendered. The host continuously sends `StallCmd` ($800), causing the P2 to poll back every ~64ms. The `BreakpointTimer` (250ms) monitors for timeouts.

**Single Go (B)**: The user pressed SPACE or left-clicked Go. The host sends `BreakValue` once, then immediately reverts to `StallCmd`. The P2 resumes, executes until the break condition is met, and re-enters the debug ISR.

**Repeat Mode (C)**: The user pressed ENTER or right-clicked Go. The host alternates between sending `BreakValue` (to resume) and `StallCmd` (to throttle), maintaining ~20 breaks/second for visual tracking.

### 4.2 State Transitions

```
Halted --[SPACE / L-click Go]--> Single Go --> (P2 resumes, hits break) --> Halted
Halted --[ENTER / R-click Go]--> Repeat Mode --> (continuous execution)
Repeat Mode --[SPACE / ENTER / any Go click]--> Halted
Running (no break) --[250ms timeout]--> Dimmed display, "Break" button shown
```

### 4.3 Single-Step Mechanics

When the user presses SPACE (single Go) with `BreakValue = $001` (break on MAIN):

1. Host sets `StallBrk := BreakValue` ($001)
2. Protocol sends `TLong(StallBrk)` to P2 — the P2 receives $001
3. Host immediately sets `StallBrk := StallCmd` ($800)
4. P2 exits debug ISR with condition $001 (break on every MAIN instruction)
5. P2 executes one MAIN instruction
6. BRK fires, P2 re-enters debug ISR, sends new state
7. Host receives state, renders display
8. Protocol sends `TLong(StallBrk)` — now $800 — P2 stays halted
9. Display shows the result of one instruction step

### 4.4 Repeat Mode Throttling

In repeat mode, breaks are throttled to prevent overwhelming the serial link:

- Track `OldTickCount` (timestamp of last Go command)
- If `GetTickCount - OldTickCount < 50` (less than 50ms since last resume): send `StallCmd` instead of `BreakValue`
- This limits execution to ~20 breaks/second maximum
- The display updates on each break, allowing visual tracking of execution flow

### 4.5 Breakpoint Timeout and Dimming

When 250ms pass without a new breakpoint (`BreakpointTimer` fires):

1. Every pixel in the bitmap is halved in brightness (right-shift each RGB byte by 1)
2. Go button caption changes to "Break"
3. If another cog has recently been in debug (`LastDebugTick` within 100ms), a hint is shown
4. If no other cog is in debug, a warning hint appears: "To force an asynchronous break in this cog, another cog must be idling in its own debugger"

---

## 5. Screen Layout and Drawing

### 5.1 Window Setup

- **Font**: Configurable via `FontName` (global). Size auto-reduced until bitmap width fits within 4096 pixels (`SmoothFillMax`).
- **Character metrics**: `ChrWidth` = width of character 'X', `ChrHeight` = height of character 'X'
- **Bitmap dimensions**: `ChrWidth * 123` wide x `ChrHeight * 77 / 2` tall
- **Window title**: `'Debugger - Cog N'` (N = cog number 0-7)
- **Window position**: Cascaded by `DebuggerID * ChrHeight * 2` from the debug display origin

### 5.2 Triple-Buffer Rendering

Three `TBitmap` objects (24-bit RGB) eliminate flicker:

| Bitmap | Purpose |
|---|---|
| `Bitmap[2]` | **Base template** — drawn once at window creation with all static elements (boxes, labels, button outlines). Restored at the start of each breakpoint. |
| `Bitmap[0]` | **Working frame** — starts as a copy of `Bitmap[2]`, then dynamic data (values, highlights) is drawn on top. |
| `Bitmap[1]` | **Display copy** — `Bitmap[0]` is copied here, then to the screen canvas. Prevents tearing during draw. |

Per-breakpoint sequence:
1. `Bitmap[0].Canvas.Draw(0, 0, Bitmap[2])` — restore from base
2. Draw all dynamic content onto `Bitmap[0]`
3. Copy `Bitmap[0]` to `Bitmap[1]`, then `Bitmap[1]` to screen

### 5.3 Grid System and Coordinates

The display uses a grid of **123 columns x 77 half-rows**. Rows are measured in half-character heights, giving finer vertical positioning.

Sub-character positioning uses 7-bit fractional offsets:

```
q1 = 1 << 7 = 128   (1/4 character offset)
q2 = 2 << 7 = 256   (1/2 character offset)
q3 = 3 << 7 = 384   (3/4 character offset)
```

The `Frac(x, y)` function converts grid coordinates to pixels:
```
Result := ((x AND $7F) * 4 + (x >> 7)) * y / 4
```
Where `y` is `ChrWidth` or `ChrHeight` depending on the axis.

### 5.4 Panel Layout Map

Approximate spatial arrangement of the debugger window:

```
     Col 2      Col 13    Col 24                          Col 82  Col 96  Col 116
      |           |         |                               |       |       |
Row 1 [REG MAP ] [LUT MAP] [CF] [ZF] [PC---] [SKIP/SKIPF pattern--] [XBYTE] [CT---------]
      |           |         |                                                |
Row 4 [          ][         ] [DISASSEMBLY (16 lines)----------] [WATCH] [SFR----] [EVENT]
      |           |         |                                    |       |         |
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
Row 77+------- ---+---------+----------------------------------------------+
```

### 5.5 Panel Definitions

Each panel is defined by grid coordinates: left column (l), top half-row (t), width in columns (w), height in half-rows (h):

| Panel | l | t | w | h | Description |
|---|---|---|---|---|---|
| REGMAP | 2 | 1 | 9 | 75 | Cog register heatmap bitmap |
| LUTMAP | 13 | 1 | 9 | 75 | LUT register heatmap bitmap |
| CF | 24 | 1 | 3 | 2 | Carry flag value |
| ZF | 29 | 1 | 3 | 2 | Zero flag value |
| PC | 34 | 1 | 8 | 2 | Program counter (5 hex digits) |
| SKIP | 44 | 1 | 41 | 2 | SKIP/SKIPF pattern (32 binary bits) |
| XBYTE | 87 | 1 | 12 | 2 | XBYTE execution engine state |
| CT | 101 | 1 | 20 | 2 | Clock tick counter (64-bit, 16 hex digits) |
| DIS | 24 | 4 | 56 | 32 | Disassembly (16 lines x 2 half-rows each) |
| WATCH | 82 | 4 | 12 | 32 | Register-delta watch list (16 entries) |
| SFR | 96 | 4 | 18 | 32 | Special function registers ($1F0-$1FF) |
| EVENT | 116 | 4 | 5 | 32 | Event flags (16 events) |
| EXEC | 24 | 35 | 4 | 4 | Execution mode tab (MAIN/INT1/INT2/INT3) |
| STACK | 30 | 37 | 77 | 2 | Stack registers (8 longs) |
| INT | 24 | 40 | 13 | 6 | Interrupt status (INT1/INT2/INT3) |
| PTR | 39 | 40 | 68 | 6 | Pointer data (FPTR, PTRA, PTRB with bytes) |
| STATUS | 24 | 47 | 6 | 6 | Status indicators (INIT, STALLI, STR, MOD, LUTS) |
| PIN | 32 | 47 | 75 | 6 | Pin registers (DIR/OUT/IN, 64 bits binary) |
| SMART | 24 | 54 | 97 | 2 | Smart pin RQPIN-delta watch list (7 entries) |
| HUB | 24 | 57 | 97 | 16 | Hub data viewer (8 rows x 16 bytes hex+ASCII) |
| HINT | 29 | 74 | 92 | 2 | Context-sensitive hint/status bar |
| B (buttons) | 109 | 37 | 12 | 16 | Break control button box |

### 5.6 Color Scheme

The debugger uses a dark color scheme with 21 configurable color slots:

| Index | Variable | Default Color | Purpose |
|---|---|---|---|
| 0 | `cBackground` | Black (`$000000`) | Window background |
| 1 | `cBox` | Dark yellow (`$1F1F00`) | Primary box outlines |
| 2 | `cBox2` | Dark green (`$001F00`) | Secondary box outlines (disassembly, hint) |
| 3 | `cBox3` | Medium orange (`$7F3F00`) | Tertiary box outlines (CT box) |
| 4 | `cData` | White (`$FFFFFF`) | Primary data values |
| 5 | `cData2` | Medium green (`$007F00`) | Secondary data values |
| 6 | `cDataDim` | Very dark yellow (`$0F0F00`) | Dimmed data |
| 7 | `cIndicator` | Orange (`$FF7F00`) | Active status indicators |
| 8 | `cName` | Yellow (`$FFFF00`) | Label names |
| 9 | `cHighSame` | Dark yellow (`$3F3F00`) | Heatmap: high bit, unchanged |
| 10 | `cLowSame` | Very dark yellow (`$0F0F00`) | Heatmap: low bit, unchanged |
| 11 | `cHighDiff` | Bright yellow (`$FFFF00`) | Heatmap: high bit, changed |
| 12 | `cLowDiff` | Medium yellow (`$7F7F00`) | Heatmap: low bit, changed |
| 13 | `cModeButton` | Medium yellow (`$7F7F00`) | Active mode button background |
| 14 | `cModeText` | White | Active mode button text |
| 15 | `cModeButtonDim` | Dark yellow (`$3F3F00`) | Inactive mode button background |
| 16 | `cModeTextDim` | Very dark yellow (`$0F0F00`) | Inactive mode button text |
| 17 | `cCmdButton` | Bright orange (`$BF5F00`) | Command button (Go) background |
| 18 | `cCmdText` | White | Command button text |
| 19 | `cCmdButtonDim` | Dark orange (`$3F1F00`) | Dimmed command button |
| 20 | `cCmdTextDim` | Very dark orange (`$1F0F00`) | Dimmed command button text |

Color values are in `$RRGGBB` format. The `WinRGB` function swaps R and B channels for Windows GDI (`$BBGGRR`).

### 5.7 Anti-Aliased Rendering System

The debugger includes a custom anti-aliased rendering system:

- **`SmoothShape`**: Draws filled or outlined rounded rectangles with elliptical corners using trigonometric LUTs
- **`SmoothLine`/`SmoothDot`**: Anti-aliased line drawing with sub-pixel accuracy (256th-pixel coordinates)
- **`SmoothPixel`**: Individual pixel with opacity blending
- **`SmoothClip`/`SmoothClipTest`**: Cohen-Sutherland line clipping

Alpha blending uses **gamma-corrected** compositing:
```
Result := Round(Power((Power(dst, 2.0) * (255 - opacity) + Power(src, 2.0) * opacity) / 256, 0.5))
```

This is gamma 2.0 blending, providing more natural visual results than linear blending.

### 5.8 Drawing Sequence Per Breakpoint

On each breakpoint, the display is redrawn in this order:

1. Restore from base bitmap (static elements)
2. Draw C flag value ('0' or '1')
3. Draw Z flag value ('0' or '1')
4. Draw PC value (5 hex digits)
5. Draw SKIP/SKIPF pattern (32 binary bits) or "Suspended during MODE" message
6. Draw XBYTE config (3 hex digits + checkmark if C,Z affected)
7. Draw CT clock ticks (16 hex digits, two 8-digit groups)
8. Draw SFR values (16 x 8 hex digits)
9. Draw event flags (16 x single '0'/'1')
10. Draw execution mode label (MAIN/INT1/INT2/INT3)
11. Draw STACK values (8 x 8 hex digits)
12. Draw interrupt status (INT1/INT2/INT3: event name + idle/wait/busy)
13. Draw pointer data (FPTR, PTRA, PTRB: hex bytes + ASCII)
14. Draw status indicators (INIT, STALLI, STR, MOD, LUTS — highlighted if active)
15. Draw pin registers (DIR/OUT/IN: 64-bit binary, split by bytes)
16. Draw hub data (8 rows of 16 bytes: address + hex + ASCII)
17. Draw disassembly (16 lines with PC highlight and breakpoint markers)
18. Update register watch list and smart pin watch list
19. Update REG/LUT/HUB heatmap bitmaps
20. Update all buttons (highlighted if active condition)
21. Draw hint bar text
22. Copy working bitmap to display bitmap to screen

---

## 6. Display Regions in Detail

### 6.1 Register and LUT Heatmap Bitmaps

Two narrow bitmaps on the left side of the display, spanning nearly the full height:

**REG bitmap** (32 pixels wide x 512 pixels tall): Each row represents one cog register (`$000`-`$1FF`), each column represents one bit (MSB on left, LSB on right).

**LUT bitmap** (32 pixels wide x 512 pixels tall): Same structure for LUT addresses (`$200`-`$3FF`).

**Color encoding**: Each pixel blends between "same" colors (`cHighSame`/`cLowSame`) and "different" colors (`cHighDiff`/`cLowDiff`) based on the `CogImageHit[]` value:
- Hit value 254 = just changed (bright)
- Hit value decays by `HitDecayRate` (2) per break toward 0 (cold)
- High bits (=1) use `cHighSame`/`cHighDiff` colors
- Low bits (=0) use `cLowSame`/`cLowDiff` colors

The currently disassembled address range is highlighted slightly brighter (`shade = $40`).

Bitmaps are `StretchDraw`'d into their box regions (scaling from 32x512 pixels to the display size).

### 6.2 C Flag, Z Flag, and Program Counter

- **C flag**: Extracted from `DebuggerMsg[mIRET]` bit 31. Displayed as single character '0' or '1'.
- **Z flag**: Extracted from `DebuggerMsg[mIRET]` bit 30. Displayed as single character '0' or '1'.
- **PC**: Extracted from `DebuggerMsg[mIRET] AND $FFFFF` (20-bit address). Displayed as 5 hex digits.

### 6.3 SKIP/SKIPF Pattern

Source: `DebuggerMsg[mBRKZ]` (32-bit SKIP pattern).

- If bit 27 of `mBRKC` is 0: label shows "SKIPF" (instead of "SKIP")
- Pattern is only "active" when `ExecMode = 0` (MAIN) and `CallDepth = 0`
- If `CallDepth > 0`: shown dimmed with message "Suspended during CALL(n)"
- If `ExecMode != 0`: shown dimmed with "Suspended during MODE"

`CallDepth` = `DebuggerMsg[mBRKC] >> 28 AND $F`.

In the disassembly view, instructions with their SKIP bit set are drawn with a semi-transparent strikethrough (opacity 160).

### 6.4 XBYTE Status

Source: `DebuggerMsg[mBRKC] >> 16 AND $1FF` (9-bit XBYTE configuration).

Displayed as 3 hex digits. A checkmark glyph appears if bit 25 of `mBRKC` is set (C,Z affected by XBYTE). The hint bar shows a detailed description of the XBYTE execution mode.

### 6.5 Clock Ticks (CT)

64-bit value from `DebuggerMsg[mCTH2]` (high 32) and `DebuggerMsg[mCTL2]` (low 32).

Displayed as 16 hex digits split into two 8-digit groups. The hint bar shows elapsed seconds computed from the clock frequency: `CT / DebuggerMsg[mFREQ]`.

### 6.6 Disassembly View

Displays 16 lines of disassembled P2 instructions. Three modes controlled by `DisMode`:

| Mode | Constant | Behavior |
|---|---|---|
| Follow PC | `dmPC` (0) | Auto-scrolls to keep PC visible; tries to position PC at line 3 (4th from top) |
| Cog lock | `dmCog` (1) | Locked to a cog/LUT address; user can scroll with mouse wheel |
| Hub lock | `dmHub` (2) | Locked to a hub address; user can scroll with mouse wheel |

**Each line shows**:
- **Address**: In cog mode: `R-xxx` or `L-xxx` (3 hex digits); in hub mode: 5 hex digits
- **Raw instruction**: 8 hex digits
- **Disassembled text**: Via `P2Disassemble` (external x86 assembly routine). Addresses `$1F8`-`$1FF` show `[ROM]` prefix with hardcoded debug ROM strings.

**Visual indicators**:
- **PC line**: Inverse highlight — rounded rectangle in `cData` color behind instruction, text in `cBox2` color
- **SKIP**: If the instruction's SKIP bit is set, a semi-transparent strikethrough shape (opacity 160)
- **Address breakpoint**: If address breakpoint matches a visible line, semi-transparent highlight in `cName` color (opacity 64)

**Auto-scroll algorithm** (dmPC mode):
1. If PC jumped far (> 8 instructions for cog, > 32 bytes for hub): snap PC to ideal line (line 3)
2. If PC is above visible range: snap to top line
3. If PC is below visible range: snap to bottom line
4. Otherwise: after `DisScrollThreshold` (8) consecutive breaks, auto-scroll one line per break toward the ideal position
5. Scroll timer resets on Go/Repeat

### 6.7 Register Watch List

Automatically tracks which of the 496 general cog registers (`$000`-`$1EF`) have changed. Shows up to 16 entries.

**Algorithm**:
1. For each register: if value changed since last break, set watch counter to 1000. Otherwise, if counter > 1, decrement by 1.
2. For each register with counter > 0: find in the 16-entry visible list by register address, or replace the oldest entry.
3. Display: 3-digit hex address + 8-digit hex value, or delta symbol if slot is empty.

Registers with `$FFFF` counter (first pass) are reset to 0 to avoid false positives.

### 6.8 Special Function Registers (SFR)

Displays all 16 SFRs at addresses `$1F0`-`$1FF`:

```
1F0  IJMP3  xxxxxxxx      1F8   PTRA  xxxxxxxx
1F1  IRET3  xxxxxxxx      1F9   PTRB  xxxxxxxx
1F2  IJMP2  xxxxxxxx      1FA   DIRA  xxxxxxxx
1F3  IRET2  xxxxxxxx      1FB   DIRB  xxxxxxxx
1F4  IJMP1  xxxxxxxx      1FC   OUTA  xxxxxxxx
1F5  IRET1  xxxxxxxx      1FD   OUTB  xxxxxxxx
1F6     PA  xxxxxxxx      1FE    INA  xxxxxxxx
1F7     PB  xxxxxxxx      1FF    INB  xxxxxxxx
```

Values rendered in `cData` color. Clickable: IJMP/IRET values treated as code pointers (lock disassembly there), PA/PB/PTRA/PTRB treated as hub data pointers (navigate hub viewer).

### 6.9 Event Flags

16 P2 events displayed as single '0' or '1' characters:

```
INT  CT1  CT2  CT3  SE1  SE2  SE3  SE4  PAT  FBW  XMT  XFI  XRO  XRL  ATN  QMT
```

Event indices 0-15. Source: `DebuggerMsg[mBRKC] AND $FFFF` (bits 15..0 of the BRK C register).

Clicking on an event name sets `BreakEvent` for event-based breakpoints.

### 6.10 Execution Mode

Determined from `DebuggerMsg[mBRKCZ]` interrupt status bits:
- Bits 3..2 = 3 → ExecMode = 1 (INT1 active/busy)
- Bits 5..4 = 3 → ExecMode = 2 (INT2 active/busy)
- Bits 7..6 = 3 → ExecMode = 3 (INT3 active/busy)
- Otherwise → ExecMode = 0 (MAIN)

Displayed as a tab label: MAIN, INT1, INT2, or INT3.

### 6.11 Stack Registers

8 hardware stack values from `DebuggerMsg[mSTK0..mSTK7]`, displayed as 8-digit hex. STK0 is top of stack.

Clickable: values treated as code/hub pointers for navigation.

### 6.12 Interrupt Status

Three interrupt levels (INT1/INT2/INT3), each showing:

- **Event name**: From `DebuggerMsg[mBRKCZ]` — 4-bit fields: INT1 at bits 11..8, INT2 at bits 15..12, INT3 at bits 19..16. Maps to event name (INT, CT1, CT2, ..., QMT).
- **State**: From `DebuggerMsg[mBRKCZ]` — 2-bit fields: INT1 at bits 1..0, INT2 at bits 3..2, INT3 at bits 5..4.
  - 0 or 1 = 'idle' (or 'off' if event = 0)
  - 2 = 'wait'
  - 3 = 'busy'

### 6.13 Pointer Data (FPTR, PTRA, PTRB)

Three rows showing memory contents around each pointer:

```
Rxx  xxxxx  xx xx xx xx xx xx [xx] xx xx xx xx xx xx xx  ..............
PTRA xxxxx  xx xx xx xx xx xx [xx] xx xx xx xx xx xx xx  ..............
PTRB xxxxx  xx xx xx xx xx xx [xx] xx xx xx xx xx xx xx  ..............
```

- **Prefix**: 'R' or 'W' for FPTR (bit 20 of `mBRKCZ`: 0=Read, 1=Write); `PTRA`/`PTRB` for the others
- **Address**: 5 hex digits
- **Data**: 14 bytes centered on the pointer (`PtrCenter = 6`), shown as hex and ASCII
- **Center byte**: Index 6 highlighted with a box outline

### 6.14 Status Indicators

Five status flags, shown as labels that are highlighted (bright orange) when active or dimmed when inactive:

| Indicator | Source | Meaning |
|---|---|---|
| INIT | `mBRKCZ` bit 23 | COGINIT occurred |
| STALLI | `mBRKCZ` bit 1 | Stall interrupt active |
| STR | `mBRKCZ` bit 21 | Streamer active |
| MOD | `mBRKCZ` bit 22 | Color modulator active |
| LUTS | `mBRKC` bit 26 | LUT sharing active |

### 6.15 Pin Registers

Three rows of 64-bit binary values (split into two 32-bit halves with byte separators):

```
DIR  xxxxxxxx xxxxxxxx xxxxxxxx xxxxxxxx  xxxxxxxx xxxxxxxx xxxxxxxx xxxxxxxx
OUT  xxxxxxxx xxxxxxxx xxxxxxxx xxxxxxxx  xxxxxxxx xxxxxxxx xxxxxxxx xxxxxxxx
IN   xxxxxxxx xxxxxxxx xxxxxxxx xxxxxxxx  xxxxxxxx xxxxxxxx xxxxxxxx xxxxxxxx
```

Sources: DIR = DIRB:DIRA (`$1FB:$1FA`), OUT = OUTB:OUTA (`$1FD:$1FC`), IN = INB:INA (`$1FF:$1FE`).

### 6.16 Smart Pin Watch

Same algorithm as register watch but for 64 smart pins. Shows up to 7 entries. Each entry: pin number (P00-P61) + RQPIN value (8 hex digits).

Filters:
- Only pins 0-61 (pins 62/63 are TX/RX, excluded)
- By default, only pins with DIR bit set (toggleable via right-click)

### 6.17 Hub Data Viewer

8 rows x 16 bytes, showing hub memory contents:

```
xxxxx  xx xx xx xx xx xx xx xx  xx xx xx xx xx xx xx xx  ................
```

Each row: 5-digit address + 16 hex bytes (space-separated) + 16 ASCII characters (non-printable shown as '.').

Navigation:
- Arrow keys: UP/DOWN = +/- `$10` (one row)
- Page keys: PAGEUP/PAGEDOWN = +/- `$80` (normal), `$1000` (Ctrl), `$10000` (Shift)
- Mouse wheel on address digits: change individual hex nibble
- Mouse wheel in hub box: scroll by configurable step
- Click on hex data, ASCII, or heatmap: navigate to that address

Address wraps at `$FFFFF`.

### 6.18 Hub Heatmap

A small bitmap (64 x 62 pixels) showing block-level change activity across hub memory. Each pixel represents one 128-byte sub-block (3968 sub-blocks total). Colors blend from `cDataDim` to `cYellow` based on change detection.

### 6.19 Hint Bar

Context-sensitive status bar at the bottom of the window. Shows detailed information about whatever the mouse is hovering over:
- Register addresses and values
- Event descriptions
- XBYTE mode details
- Clock tick elapsed time
- Button descriptions
- Hub address details

---

## 7. Breakpoint Control Buttons

### 7.1 Button Layout

The button box occupies columns 109-120, rows 37-52. Two columns of buttons:

**Left column** (break condition enables):

| Button | Label | Position |
|---|---|---|
| BREAK | BREAK | Top-left |
| ADDR | ADDR | Below BREAK |
| INT3E | INT3E | Below ADDR |
| INT2E | INT2E | Below INT3E |
| INT1E | INT1E | Below INT2E |
| DEBUG | DEBUG | Below INT1E |

**Right column** (single-step mode):

| Button | Label | Position |
|---|---|---|
| INIT | INIT | Top-right |
| EVENT | EVENT | Below INIT |
| INT3 | INT3 | Below EVENT |
| INT2 | INT2 | Below INT3 |
| INT1 | INT1 | Below INT2 |
| MAIN | MAIN | Below INT1 |

**Bottom** (spanning both columns):

| Button | Label | Position |
|---|---|---|
| GO | Go/Stop/Break | Below all mode buttons |

### 7.2 Break Condition Buttons

Each button has distinct **left-click** (exclusive set) and **right-click** (toggle) behaviors:

| Button | Bit(s) | Left-Click | Right-Click |
|---|---|---|---|
| MAIN | `$001` | Set bit 0 exclusively (clear bits 1-7,9,10; keep bit 8) | Toggle bit 0; clear bit 4 (DEBUG) |
| INT1 | `$002` | Set bit 1 exclusively | Toggle bit 1; clear bit 4 |
| INT2 | `$004` | Set bit 2 exclusively | Toggle bit 2; clear bit 4 |
| INT3 | `$008` | Set bit 3 exclusively | Toggle bit 3; clear bit 4 |
| DEBUG | `$010` | Set bit 4 exclusively; clear bits 0-3,5-7 | Toggle bit 4; clear bits 0-3,5-7 (mutual exclusion with single-step modes) |
| INT1E | `$020` | Set bit 5 exclusively | Toggle bit 5; clear bit 4 |
| INT2E | `$040` | Set bit 6 exclusively | Toggle bit 6; clear bit 4 |
| INT3E | `$080` | Set bit 7 exclusively | Toggle bit 7; clear bit 4 |
| INIT | `$100` | OR in bit 8 (additive, independent) | XOR bit 8 (toggle) |
| EVENT | `$200` | Set bit 9 + event ID in bits 15..12 exclusively | Toggle bit 9 with event |
| ADDR | `$400` | Set bit 10 + address in bits 31..12 exclusively | Toggle bit 10 with address |
| BREAK | (none) | Clear bits 0-7,9,10 (keep bit 8 only — async break mode) | — |

**Key design**: Left-click sets one condition exclusively (replacing all others except INIT). Right-click toggles a condition on/off without affecting others. INIT (bit 8) is always independent — it's never cleared by other button clicks.

Active conditions are shown as highlighted (bright) buttons; inactive as dimmed.

### 7.3 Go/Stop/Break Button

The Go button has three visual states:

| Caption | When | Color |
|---|---|---|
| "Go" | Cog is halted, ready for user action | `cCmdButton` (bright orange) |
| "Stop" | Repeat mode is active (continuous execution) | `cCmdButton` |
| "Break" | Cog is running, 250ms timeout expired | `cCmdButtonDim` (dimmed) |

**Button actions**:
- **Left-click or SPACE**: Single Go — send BreakValue once, then StallCmd
- **Right-click or ENTER**: Repeat Mode — continuous execution with throttled updates
- **Click while in Repeat Mode**: Stop — revert to halted state

**Visual feedback**: A 100ms timer (`ButtonTimer`) provides a button-press flash effect.

---

## 8. User Interaction

### 8.1 Keyboard Shortcuts

| Key | Action |
|---|---|
| SPACE | Single-step (equivalent to left-click Go) |
| ENTER | Continuous run / stop (equivalent to right-click Go) |
| B | Click BREAK button (set async break mode, clear all conditions) |
| I | Toggle INIT break (right-click INIT button) |
| D | Toggle DEBUG break (right-click DEBUG button) |
| M | Toggle MAIN single-step (right-click MAIN button) |
| R | Reset register watch list |
| UP arrow | Hub viewer scroll up one row (`HubAddr -= $10`) |
| DOWN arrow | Hub viewer scroll down one row (`HubAddr += $10`) |
| PAGEUP | Hub viewer page up (`$80` normal, `$1000` with Ctrl, `$10000` with Shift) |
| PAGEDOWN | Hub viewer page down (same modifiers) |

All letter keys are uppercased before processing. Tab key is captured (`DLGC_WANTTAB`) to prevent dialog focus changes.

### 8.2 Mouse Click Actions

**Go button**: See [Section 7.3](#73-gostopbreak-button).

**Break condition buttons**: See [Section 7.2](#72-break-condition-buttons).

**Event names**: Click on an event name (CT1..QMT) → sets `BreakEvent` to that event index (1-15).

**Disassembly box**:
- Left-click: Lock disassembly to follow PC (`DisMode = dmPC`)
- Right-click: Toggle address breakpoint at the clicked line's address

**Register/LUT heatmap**: Click → lock disassembly to the cog/LUT address under the cursor.

**PC box**: Click → lock disassembly to follow PC.

**SFR values**: Click on an SFR value:
- IJMP3/IRET3/IJMP2/IRET2/IJMP1/IRET1 (addresses $1F0-$1F5): Navigate disassembly to value as code pointer
- PA/PB/PTRA/PTRB and below ($1F6-$1FF): Navigate hub viewer and disassembly to value as hub pointer

**Stack values**: Click on a stack value → navigate to it as a code/hub pointer.

**Pointer addresses/data**: Click → navigate hub viewer and disassembly to that address.

**Register watch box**: Click → reset watch list.

**Smart pin watch box**:
- Left-click: Reset smart pin watch list
- Right-click: Toggle between watching all pins vs. only pins with DIR set

**Hub data/chr/map**: Click → navigate hub address to clicked location.

### 8.3 Mouse Wheel Actions

**In disassembly box**:
- If in dmPC mode, switches to dmCog or dmHub (to allow free scrolling)
- Scroll deltas (instruction/byte units):

| Modifier | Cog delta | Hub delta |
|---|---|---|
| None | 1 | 16 |
| Ctrl | 4 | 1 |
| Shift | 16 | 4 |
| Ctrl+Shift | 32 | 128 |

**In hub address digits**: Each scroll step changes the hex nibble under the cursor by +/-1.

**In hub data box**: Scroll by configured step amounts (same modifier scheme as disassembly but with hub-specific deltas).

### 8.4 Mouse Hover (Hint System)

The mouse position is continuously tracked. For each region, `MouseWithin` tests if the cursor is inside and updates the `Hint` string with context-sensitive information.

A 50ms timer (`MouseMoveTimer`) detects when the mouse leaves the form and clears all hover states.

Hint content varies by region:
- Disassembly: instruction address and type
- Registers: address, name, and current value
- Events: event description
- Buttons: break condition description
- CT: elapsed seconds at current frequency
- XBYTE: detailed mode description
- Hub data: address and byte value

---

## 9. Debug Compilation

### 9.1 Debug Data Table

The `DebugData` buffer (up to `$4000` = 16KB) uses this layout:

| Offset | Size | Content |
|---|---|---|
| `$000`-`$001` | 1 word | Pointer to next free position (initially `$200`) |
| `$002`-`$1FF` | 255 words | Index table — word N is the offset to the debug record for BRK code N (1-255). Zero = unused. |
| `$200`+ | Variable | Actual debug command records (zero-terminated byte strings) |

### 9.2 Debug Record Format (Bytecodes)

Each debug record is a zero-terminated sequence of debug bytecodes.

**Simple commands** (byte < `$20`):

| Code | Name | Meaning |
|---|---|---|
| `$00` | `dc_end` | End of debug commands |
| `$01` | `dc_asm` | Switch to ASM mode (PASM debug) |
| `$02` | `dc_if` | IF(cond) — abort output if condition = 0 |
| `$03` | `dc_ifnot` | IFNOT(cond) — abort output if condition != 0 |
| `$04` | `dc_cogn` | Output "CogN  " header with optional timestamp |
| `$05` | `dc_chr` | Output single character |
| `$06` | `dc_str` | Output zero-terminated string from hub |
| `$07` | `dc_dly` | DLY(ms) — delay in milliseconds |
| `$08` | `dc_pc_key` | PC_KEY(ptr) — get keyboard input from host |
| `$09` | `dc_pc_mouse` | PC_MOUSE(ptr) — get mouse input from host |
| `$0A` | `dc_c_z_pre` | Output ", C=? Z=?" |
| `$0B` | `dc_c_z` | Output "C=? Z=?" |

**Argument commands** (byte >= `$20`):

Format: `TTTTTTSS` where bits [7:2] = command type, bits [1:0] = display specifier:

| Specifier | Format |
|---|---|
| `%00` | `", " + name_string + " = " + data` |
| `%01` | `name_string + " = " + data` |
| `%10` | `", " + data` |
| `%11` | `data` (bare value) |

Command types (bits [7:2]):

| Bits [7:2] | Base Command | Description |
|---|---|---|
| `001000` | BOOL | Boolean value |
| `001001` | ZSTR | Zero-terminated string |
| `001011` | FDEC | Float as decimal |
| `010000`-`010111` | UDEC variants | Unsigned decimal (auto/byte/word/long/array) |
| `011000`-`011111` | SDEC variants | Signed decimal |
| `100000`-`100111` | UHEX variants | Unsigned hexadecimal |
| `101000`-`101111` | SHEX variants | Signed hexadecimal |
| `110000`-`110111` | UBIN variants | Unsigned binary |
| `111000`-`111111` | SBIN variants | Signed binary |

Within each group, bits [4] distinguish single-value vs. array, and bits [3:2] select data width: `00`=auto/reg, `01`=byte, `10`=word, `11`=long.

### 9.3 PASM2 Debug Value Encoding

For PASM `DEBUG` statements (`dc_asm` mode), values are encoded inline in the debug record rather than on the Spin2 expression stack:

| Encoding | Format |
|---|---|
| `%1000_00xx %xxxx_xxxx` | 10-bit register address (big-endian) |
| `%00xx_xxxx %xxxx_xxxx` | 14-bit constant (big-endian) |
| `%0100_0000 + 4 bytes` | 32-bit constant (little-endian) |

### 9.4 Debug Record Deduplication

In `debug_enter_record`, the compiler checks if the current debug record byte-for-byte matches any existing record. If so, it reuses the same BRK index, preventing duplicate records from inflating the table. This is important since the BRK code space is limited to 255 entries.

### 9.5 Debug Data Collapse

After all compilation passes, `collapse_debug_data` compacts the index table:

1. Find the first empty (zero) entry in the 255-word index
2. Move all debug record data downward to close the gap between used index entries and the data area
3. Adjust all index pointers accordingly
4. Verify total size fits within `debug_size_limit` (`$2A00` = 10,752 bytes)

### 9.6 Debugger Insertion into Binary

`P2InsertDebugger` (called from EditorUnit) inserts the debugger stub:

1. Validate crystal/clock mode and frequency >= 10 MHz
2. Calculate total debug overhead: `debugger_size + collapsed_debug_data_size`
3. Move application code upward in the OBJ image by that amount
4. Copy the debugger stub (from compiled `Spin2_debugger.spin2`, included as `Spin2_debugger.inc`)
5. Copy collapsed debug data immediately after the debugger
6. Patch configuration fields into the debugger binary:

| Offset | Field | Source |
|---|---|---|
| `$0D4` | `_clkfreq_` | Clock frequency in Hz |
| `$0D8` | `_clkmode1_` | Clock mode without PLL (crystal start) |
| `$0DC` | `_clkmode2_` | Full clock mode (crystal + PLL) |
| `$0E0` | `_delay_` | Startup delay in clock ticks (from `DEBUG_DELAY`) |
| `$0E4` | `_appsize_` | Application size in bytes |
| `$0E8` | `_hubset_` | HUBSET value — low byte is cog enable mask (default `$FF`) |
| `$11C` | `_brkcond_` | Initial BRK condition (modified by `DEBUG_COGINIT`/`DEBUG_MAIN`) |
| `$140` | `_txpin_` | TX pin number |
| `$144` | `_rxpin_` | RX pin number (MSB set if `DEBUG_TIMESTAMP` defined) |
| `$148` | `_baud_` | Baud rate |

### 9.7 Configuration Symbols

The compiler recognizes these `CON` symbols to configure debugging:

| Symbol | Default | Effect |
|---|---|---|
| `DEBUG_DISABLE` | 0 | Non-zero disables all DEBUG statements |
| `DEBUG_MASK` | — | Bitmask for gated DEBUG (used with `[bit]` syntax) |
| `DEBUG_PIN_TX` (or `DEBUG_PIN`) | 62 | TX pin number |
| `DEBUG_PIN_RX` | 63 | RX pin number |
| `DEBUG_BAUD` | Download baud | Serial baud rate |
| `DEBUG_COGS` | `$FF` (all) | Which cogs to enable debugging on (bitmask) |
| `DEBUG_COGINIT` | — | If defined, break on COGINIT events (sets condition `$110`) |
| `DEBUG_MAIN` | — | If defined, break on initial cog execution (sets condition `$001`) |
| `DEBUG_DELAY` | 0 | Startup delay in milliseconds |
| `DEBUG_TIMESTAMP` | — | If defined, show 64-bit timestamps in output |
| `DEBUG_LEFT/TOP/WIDTH/HEIGHT` | — | Host terminal window position |
| `DEBUG_DISPLAY_LEFT/TOP` | — | Host display window position |
| `DEBUG_LOG_SIZE` | 0 | Host log file size (0 = disabled) |
| `DEBUG_WINDOWS_OFF` | 0 | Suppress host debug windows |

---

## 10. Host-Side Session Lifecycle

### 10.1 Debug Session Startup

Two paths to start a debug session:

**Compile and load** (normal path):
1. Editor sets `P2.DebugMode := True`
2. Compiler generates debug records and inserts debugger stub
3. `LoadHardware` downloads binary to P2 over serial
4. If debug conditions met (`DebugMode AND NOT DebugWindowsOff AND DebugBaud = DownloadBaud`): transitions directly to `OperateDebug` on the same serial connection

**Standalone attach** (debug toggle):
1. `RunDebugToggle` calls `StartDebug`
2. Opens COM port and enters `OperateDebug` without compilation

### 10.2 Debug Receive Loop

`OperateDebug` is the main event loop:

```pascal
DebugActive := True;
ResetDisplays;          // close old windows, reset symbols, open log
while DebugActive do begin
  for i := 1 to 100 do    // process up to 100 bytes per yield
    if RxHead <> RxTail then
      DebugForm.ChrIn(read byte from RX buffer)
    else break;
  Application.ProcessMessages;  // yield to Windows message pump
end;
CloseComm;
```

Key characteristics:
- Processes up to 100 bytes per iteration before yielding to the Windows message pump
- Runs on the main GUI thread (not the serial thread)
- `ChrIn` dispatches to the appropriate handler (debugger, display, or text console)
- When `ChrIn` encounters a cog byte (0-7), it calls `DebuggerForm[x].Breakpoint` which runs the entire synchronous protocol exchange before returning

### 10.3 Debug Session Shutdown

Shutdown uses a timer-based approach to safely close the session:

1. Set `DebugActive := False` (signals the receive loop to exit)
2. Arm `DebugTimer` (10ms interval) to wait for the COM port to close
3. `CloseComm` closes all display/debugger forms, closes log file, stops serial thread, closes COM handle
4. If a new operation was pending (e.g., recompile+load), the timer replays it after shutdown completes

---

## 11. Appendix: Constants Reference

### 11.1 Debugger Message Indices

| Index | Constant | Content |
|---|---|---|
| 0 | `mCOGN` | Cog number (bits 2..0 = cog ID 0-7) |
| 1 | `mBRKCZ` | Break status CZ: interrupt states, COGINIT, streamer, modulator, FIFO direction |
| 2 | `mBRKC` | Break status C: events (bits 15..0), XBYTE (bits 25..16), call depth (bits 31..28), LUT sharing (bit 26), SKIPF flag (bit 27) |
| 3 | `mBRKZ` | Break status Z: SKIP pattern (32 bits) |
| 4 | `mCTH2` | Clock ticks high 32 bits |
| 5 | `mCTL2` | Clock ticks low 32 bits |
| 6-13 | `mSTK0`..`mSTK7` | Hardware stack levels 0-7 (top to bottom) |
| 14 | `mIRET` | Interrupt return: bit 31 = C, bit 30 = Z, bits 19..0 = PC |
| 15 | `mFPTR` | FIFO pointer (RFxx/WFxx address) |
| 16 | `mPTRA` | PTRA register |
| 17 | `mPTRB` | PTRB register |
| 18 | `mFREQ` | Clock frequency (Hz) |
| 19 | `mCOND` | Initial BRK condition (used on first break only) |

`DebuggerMsgSize = 20`

### 11.2 Memory Size Constants

| Constant | Value | Purpose |
|---|---|---|
| `CogSize` | `$400` (1024) | Cog register space (cog + LUT) |
| `CogBlockSize` | `$10` (16) | Registers per CRC block |
| `CogBlocks` | 64 | Number of CRC blocks |
| `HubSize` | `$7C000` (507,904) | Debuggable hub RAM range |
| `HubBlockSize` | `$1000` (4096) | Bytes per hub checksum block |
| `HubBlocks` | 124 | Number of hub checksum blocks |
| `HubSubBlockSize` | `$80` (128) | Bytes per hub sub-block |
| `HubSubBlocks` | 3968 | Total hub sub-blocks |
| `HubBlockRatio` | 32 | Sub-blocks per block |
| `RegWatchSize` | `$1F0` (496) | Watchable cog registers ($000-$1EF) |
| `RegWatchListSize` | 16 | Visible register watch entries |
| `SmartPins` | 64 | Number of smart pins tracked |
| `SmartWatchListSize` | 7 | Visible smart pin watch entries |
| `DisLines` | 16 | Disassembly lines displayed |
| `PtrBytes` | 14 | Bytes displayed per pointer |
| `PtrCenter` | 6 | Center byte index in pointer display |
| `StallCmd` | `$00000800` | Stall command value |
| `HitDecayRate` | 2 | Heatmap decay per break |
| `DisLineIdeal` | 3 | Target line for PC (4th from top) |
| `DisScrollThreshold` | 8 | Breaks before auto-scroll kicks in |
| `SmoothFillMax` | 4096 | Max bitmap width in pixels |

### 11.3 SFR Register Names

| Address | Name | Address | Name |
|---|---|---|---|
| `$1F0` | IJMP3 | `$1F8` | PTRA |
| `$1F1` | IRET3 | `$1F9` | PTRB |
| `$1F2` | IJMP2 | `$1FA` | DIRA |
| `$1F3` | IRET2 | `$1FB` | DIRB |
| `$1F4` | IJMP1 | `$1FC` | OUTA |
| `$1F5` | IRET1 | `$1FD` | OUTB |
| `$1F6` | PA | `$1FE` | INA |
| `$1F7` | PB | `$1FF` | INB |

### 11.4 Event Names

| Index | Name | Index | Name |
|---|---|---|---|
| 0 | INT | 8 | PAT |
| 1 | CT1 | 9 | FBW |
| 2 | CT2 | 10 | XMT |
| 3 | CT3 | 11 | XFI |
| 4 | SE1 | 12 | XRO |
| 5 | SE2 | 13 | XRL |
| 6 | SE3 | 14 | ATN |
| 7 | SE4 | 15 | QMT |

### 11.5 Debug ROM Disassembly Strings

Hardcoded disassembly text for cog addresses `$1F8`-`$1FF` (the ROM debug entry/exit sequence):

```
$1F8: setq    #$F     'DEBUG Entry
$1F9: wrlong  0,#$FFF80-cog<<7
$1FA: setq    #$F
$1FB: rdlong  0,#$FFFC0-cog<<7
$1FC: jmp     #\0
$1FD: setq    #$F     'DEBUG Exit
$1FE: rdlong  0,#$FFF80-cog<<7
$1FF: reti0
```

---

*Document generated from PNut v52a reference source (`REF-V52A/`). Source files: `DebuggerUnit.pas`, `DebugUnit.pas`, `Spin2_debugger.spin2` (embedded in `p2com.asm`), `GlobalUnit.pas`, `SerialUnit.pas`, `EditorUnit.pas`.*
