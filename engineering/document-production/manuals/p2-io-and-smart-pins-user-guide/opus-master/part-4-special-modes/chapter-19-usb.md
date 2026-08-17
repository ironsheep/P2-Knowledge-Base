# Chapter 19: USB Host/Device {#ch19}

This chapter covers the USB smart pin mode P_USB_PAIR (%11011). The P2 provides hardware-assisted USB through smart pins, handling the differential signaling and timing while software manages the USB protocol stack.


## 19.1 USB Overview

### What the Smart Pin Provides

The USB mode handles the physical layer:

- Differential signaling (D+/D-)
- USB line state detection (J, K, SE0, SE1)
- Bit-level timing for USB 1.1 speeds
- Output driver control

### What Software Must Provide

The USB protocol stack:

- Packet formatting and parsing
- Endpoint management
- Device enumeration
- Class-specific protocols (HID, CDC, Mass Storage, etc.)

### Complexity Warning

USB is a complex protocol. Building a complete USB stack from scratch requires:

- Deep understanding of USB specification
- Significant development time
- Extensive testing with various devices

**Recommendation:** Use existing USB libraries from Parallax or the P2 community rather than implementing from scratch.


## 19.2 Pin Configuration

### Pin Pair Requirement

USB requires an even/odd consecutive pin pair:

| Pin | Function |
|-----|----------|
| Even (e.g., 56) | DM (D-) |
| Odd (e.g., 57) | DP (D+) |

Valid pairs: 0/1, 2/3, 4/5, ..., 56/57, 58/59, 60/61, 62/63

### Basic Configuration

```spin2
CON
  USB_DM = 56                                   ' D- on even pin
  USB_DP = 57                                   ' D+ on odd pin (DM+1)

PUB configure_usb_pins() | baud
  ' Configure BOTH pins of the pair with identical WRPIN D data
  WRPIN(USB_DM, P_USB_PAIR | P_OE)
  WRPIN(USB_DP, P_USB_PAIR | P_OE)
  ' WXPIN on the LOWER pin sets USB mode + baud:
  '   D[15]=1 host / 0 device, D[14]=1 full-speed / 0 low-speed
  '   D[13:0]=baud fraction
  baud := 12_000_000 / (clkfreq / $10000)  ' full-speed 12 Mbps
  WXPIN(USB_DM, $4000 | baud)                      ' device, full-speed
  PINHIGH(USB_DM)
  PINHIGH(USB_DP)
```

### Output Control

| WRPIN D Bit | Function |
|-------------|----------|
| D = %1_11011_0 | Output drive enabled (normal operation) |
| D = %0_11011_0 | Output drive disabled (sniffer mode) |

**Sniffer Mode:** Disables output drive to passively monitor USB traffic without affecting the bus.


## 19.3 USB Signaling

### Line States

USB uses differential signaling with specific line states:

| State | D+ | D- | Meaning |
|-------|----|----|---------|
| J | High | Low | Idle (Full Speed), Data 0 |
| K | Low | High | Data 1 (Full Speed) |
| SE0 | Low | Low | End of Packet, Reset, Disconnect |
| SE1 | High | High | Invalid (error condition) |

**Note:** J and K meanings swap for Low Speed vs Full Speed, because USB uses complementary (mirrored) line signaling. (This is a signaling-polarity difference tied to the speed setting, not a way to reassign the physical DP/DM pins.)

### USB Speeds

| Speed | Bit Rate | Supported |
|-------|----------|-----------|
| Low Speed (LS) | 1.5 Mbps | Yes |
| Full Speed (FS) | 12 Mbps | Yes |
| High Speed (HS) | 480 Mbps | No |

The P2 USB mode supports USB 1.1 speeds only.


## 19.4 Register Usage

### Overview

The USB mode uses the smart pin registers for configuration and data:

| Register | Function |
|----------|----------|
| X | USB configuration, set via WXPIN on the lower (even) pin: D[15]=1 host / 0 device, D[14]=1 full-speed / 0 low-speed, D[13:0]=baud rate as a 16-bit fraction of sysclk (target_Hz / clkfreq × $10000) |
| Y | Line-state and packet output, set via WYPIN on the lower pin (see table below) |
| Z | Receiver data + 16-bit status word, read via RDPIN/RQPIN on the lower pin (see bit layout below) |

**All smart pin access happens on the lower (even/DM) pin** — WXPIN, WYPIN, and RDPIN/RQPIN are all issued there. The upper (odd/DP) pin takes no WXPIN/WYPIN; software only reads its IN flag (with TESTP). WXPIN **must** be issued on the lower pin to establish host/device, speed, and baud rate *before* raising DIR. (Source: *Parallax Propeller 2 Documentation v35 - Rev B/C*, USB host/device mode.)

#### Baud Rate — Worked Example

The baud fraction's top two bits must be zero, so the baud rate must stay below ¼ of sysclk. For 12 Mbps (full-speed) on an 80 MHz clock:

```formula
baud_fraction = 12,000,000 / 80,000,000 × $10000 = $2666
```

Selecting host + full-speed (D[15]=1, D[14]=1, i.e. $C000) gives a WXPIN value of **$E666** (`$C000 | $2666`).

#### Y Register — Line States and Packet Output (WYPIN)

Write these with WYPIN on the lower pin to drive a line state or start a packet:

| WYPIN D | Action |
|---------|--------|
| 0 | Output IDLE (float, except an optional resistor to 3.3 V / GND) |
| 1 | Output SE0 (drive both DP and DM low) |
| 2 | Output K (drive the K state) |
| 3 | Output J (J state — like IDLE, but actively driven) |
| 4 | Output EOP (end-of-packet: SE0, SE0, J, then IDLE) |
| $80 | SOP — start-of-packet, then bytes, with automatic EOP when the buffer empties |

#### Z Register — Receiver Status Word

RDPIN/RQPIN on the lower pin returns a 16-bit status word (with `RDPIN ... WC`, the error flag also lands in C):

| Bit(s) | Meaning |
|--------|---------|
| [15:8] | Last byte received |
| [7] | Byte toggle — cleared on SOP, toggles on each byte received (use it to detect a *new* byte) |
| [6] | Error — cleared on SOP; set on bit-unstuff error, EOP with SE0 > 3 bits, or SE1 |
| [5] | EOP received |
| [4] | SOP received |
| [3] | SE1 in (illegal) |
| [2] | SE0 in (RESET) |
| [1] | K in (RESUME) |
| [0] | J in (IDLE) |

### IN Flag — Per-Pin Semantics

The two pins carry **different** IN meanings:

- **Upper (odd / DP) pin** — IN rises whenever the **output buffer empties**, signalling that the next output byte may be written (via WYPIN to the lower pin). Read it with TESTP.
- **Lower (even / DM) pin** — IN rises on any **change in receiver status**; read the 16-bit status word with RDPIN/RQPIN.

After a lower-pin status change, IN will not rise again until acknowledged with one of WRPIN/WXPIN/WYPIN/RDPIN/AKPIN — so always acknowledge before waiting for the next event, or the event is missed.

### Sending a Packet

1. `WYPIN #$80` on the lower pin to emit SOP.
2. After each **IN rise on the upper pin**, `WYPIN byte` on the lower pin to buffer the next byte.
3. Stop sending bytes and the transmitter appends EOP automatically.

Always confirm the upper pin's IN rose after each WYPIN before issuing the next one — even for a state change — because all output is paced by the baud generator and the buffer only empties at the next bit period.

### Transmitter and Receiver Are Independent

TX and RX have separate state machines; only the baud generator is shared. Note that the **receiver also sees all local transmit output** — the pin's own transmitted bytes appear in the RX status stream, so software must account for that loopback.

::: caution
**On an FPGA-emulated P2 the USB signaling resistors must be fitted externally** — the built-in resistors this mode relies on exist only on the ASIC. See Appendix G (FPGA Board Differences) for the specifics.
:::

::: caution
**Transmit pacing tightens as the system clock rises.** Beyond the basic IN-flag handshake above, community USB drivers report that at higher `clkfreq` the transmit buffer must not be re-fed too soon, or bit-stuffed bits can be dropped — the safe inter-byte spacing scales with the system clock. Both the host driver (OBEX #4198) and the device driver (OBEX #4727) insert sysclk-proportional delays between output bytes to stay reliable. This is a community-observed behaviour; the exact mechanism is not described in the current silicon documentation, so tune the per-clock delay against the actual clock rather than treating any single value as a published figure.
:::


## 19.5 Host vs Device Mode

### Device Mode

As a USB device, the P2:

- Waits for host to initiate communication
- Responds to USB requests
- Provides endpoints for data transfer
- Simpler to implement than host mode

**Common device classes:**

- CDC (Virtual COM Port)
- HID (Keyboard, Mouse, Gamepad)
- Mass Storage

### Host Mode

As a USB host, the P2:

- Initiates all communication
- Enumerates and configures devices
- Must handle all connected device types

Bus power is a board responsibility, not a P2 one. A host port supplies 5V on VBUS, which the P2 cannot source — its I/O operates at 3.3V. The external supply and its current limiting are covered in §19.8.

**Host implementation is significantly more complex than device mode.**


## 19.6 Using USB Libraries

### Recommended Approach

Rather than implementing USB from scratch, use existing libraries:

**Parallax OBEX (Object Exchange)** — two community drivers are the natural starting points, one for each role:

- **USBnew** (OBEX #4198, by Wuerfel_21) — a USB **host** / HID-input driver: with the P2 acting as host, it reads keyboards, mice, and gamepads.
- **USB Human-Interface-Device Driver** (OBEX #4727, by Chris Gadd) — a USB **device** driver: the P2 presents itself as a HID peripheral to a host.

These are the community implementations to study and build from; review each against the application's requirements and test it before relying on it.

**P2 Forums:**

- Community-developed USB stacks
- Example implementations
- Troubleshooting support

### Example: Using a USB Library

```spin2
' This is pseudocode showing typical USB library usage
' Actual syntax depends on the specific library

OBJ
  usb : "usb_cdc"                               ' USB CDC library

PUB main()
  usb.start(USB_DM, USB_DP)                     ' Initialize USB

  REPEAT
    IF usb.rx_check()                           ' Data available?
      process_data(usb.rx())                    ' Read and process

    IF have_data_to_send()
      usb.tx(output_data)                       ' Send data
```


## 19.7 Basic USB Configuration Example

### Pin Setup

```{.spin2 caption="ch19-usb-device-config.spin2"}
CON
  _clkfreq = 200_000_000
  USB_DM = 56
  USB_DP = 57

PUB configure_usb() | baud
  ' Reset both pins
  PINFLOAT(USB_DM)
  PINFLOAT(USB_DP)

  ' Configure both pins of the pair with identical WRPIN D data
  WRPIN(USB_DM, P_USB_PAIR | P_OE)
  WRPIN(USB_DP, P_USB_PAIR | P_OE)

  ' Set USB mode + baud on lower pin (D[15]=0 device, D[14]=1 full-speed)
  baud := 12_000_000 / (clkfreq / $10000)
  WXPIN(USB_DM, $4000 | baud)

  ' Enable the USB pair
  PINHIGH(USB_DM)
  PINHIGH(USB_DP)
```

### PASM2 Configuration

```pasm2
DAT           org

              ' Reset USB pins
              dirl      #USB_DM
              dirl      #USB_DP

              ' Configure USB mode on both pins (identical D data)
              wrpin     usb_mode, #USB_DM
              wrpin     usb_mode, #USB_DP
              ' Set USB mode + baud on lower pin only
              wxpin     usb_cfg, #USB_DM

              ' Enable USB pair
              dirh      #USB_DM
              dirh      #USB_DP

              ' Monitor for USB events
.loop
              testp     #USB_DM wc              ' Check IN flag
        if_c  call      #handle_usb_event

              jmp       #.loop

handle_usb_event
              rdpin     usb_data, #USB_DM       ' Read USB data/status
              ' Process USB event...
              ret

usb_mode      long      P_USB_PAIR | P_OE
usb_cfg       long      $4000 | ($10000 * 12 / 200)  ' device FS @ 200MHz
usb_data      res       1
```


## 19.8 Hardware Considerations

### External Components

USB host mode requires:

- 5V power supply for VBUS
- Current limiting for protection
- Pull-up/pull-down resistors for speed identification

USB device mode requires:

- Pull-up resistor on D+ (Full Speed) or D- (Low Speed)
- No level shifting needed on D+/D-: the P2's I/O is 3.3V, which matches USB low/full-speed signaling (only VBUS is 5V)

### Pin Selection

Choose USB pins based on:

- Physical proximity to USB connector
- Trace length matching for differential pair
- Isolation from noisy digital signals


## 19.9 Limitations

### What P2 USB Cannot Do

- USB 2.0 High Speed (480 Mbps)
- USB 3.x SuperSpeed
- Isochronous transfers with guaranteed timing (challenging)

### Software Requirements

Implementing USB requires:

- Precise timing for packet handling
- State machine for USB protocol
- Buffer management for endpoints
- Error handling and recovery

**Development time:** Expect weeks to months for a robust USB implementation.


## 19.10 Quick Reference

### Mode Constant

| Constant | Value | Description |
|----------|-------|-------------|
| P_USB_PAIR | %11011 | USB differential pair mode |

### Pin Requirements

- Even/odd consecutive pins
- Even pin = DM (D-)
- Odd pin = DP (D+)
- Both pins must be enabled (DIRH)

### Configuration Pattern

```spin2
WRPIN(even_pin, P_USB_PAIR | P_OE)        ' Configure DM (identical D data)
WRPIN(even_pin+1, P_USB_PAIR | P_OE)      ' Configure DP (identical D data)
' full-speed, lower pin only
WXPIN(even_pin, $4000 | (12_000_000 / (clkfreq / $10000)))
PINHIGH(even_pin)                         ' Enable DM
PINHIGH(even_pin+1)                       ' Enable DP
```

### Key Points

- Smart pin handles physical layer signaling
- Software must implement full USB protocol stack
- Use existing libraries when possible
- Supports USB 1.1 Full Speed and Low Speed only
- OUT signals are overridden by USB mode
- Limited official documentation - community resources essential

### Resources

- Parallax P2 Forums: forums.parallax.com
- Parallax OBEX: obex.parallax.com
- USB Specification: usb.org
- P2 USB implementation examples from community members


*This chapter covered the USB smart pin mode. For a complete mode reference, see Appendix F.*
