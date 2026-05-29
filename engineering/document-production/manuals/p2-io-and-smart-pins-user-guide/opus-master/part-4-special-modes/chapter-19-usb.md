# Chapter 19: USB Host/Device

This chapter covers the USB Smart Pin mode P_USB_PAIR (%11011). The P2 provides hardware-assisted USB through Smart Pins, handling the differential signaling and timing while software manages the USB protocol stack.


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

PUB configure_usb_pins()
  ' Configure as USB pair with output enabled
  WRPIN(USB_DM, P_USB_PAIR | P_OE)
  DIRH(USB_DM)
  DIRH(USB_DP)
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

**Note:** J and K meanings swap for Low Speed vs Full Speed.

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
| X | USB configuration parameters |
| Y | Protocol control |
| Z | Data and status |

**Note:** Detailed register bit assignments require reference to USB implementation examples and Parallax documentation, as the silicon documentation is limited.

### IN Flag

The IN flag signals USB events that require software attention:

- Packet received
- Transmission complete
- Line state change


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

- Provides bus power (5V)
- Initiates all communication
- Enumerates and configures devices
- Must handle all connected device types

**Host implementation is significantly more complex than device mode.**


## 19.6 Using USB Libraries

### Recommended Approach

Rather than implementing USB from scratch, use existing libraries:

**Parallax OBEX (Object Exchange):**

- Search for USB objects
- CDC (serial port) implementations
- HID implementations

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

```spin2
CON
  _clkfreq = 200_000_000
  USB_DM = 56
  USB_DP = 57

PUB configure_usb()
  ' Reset both pins
  DIRL(USB_DM)
  DIRL(USB_DP)

  ' Configure USB mode with output enabled
  WRPIN(USB_DM, P_USB_PAIR | P_OE)

  ' Enable the USB pair
  DIRH(USB_DM)
  DIRH(USB_DP)
```

### PASM2 Configuration

```pasm2
DAT           org

              ' Reset USB pins
              dirl      #USB_DM
              dirl      #USB_DP

              ' Configure USB mode
              wrpin     usb_mode, #USB_DM

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
- May need level shifting if P2 runs at 3.3V

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
WRPIN(even_pin, P_USB_PAIR | P_OE)              ' Configure with output
DIRH(even_pin)                                  ' Enable DM
DIRH(even_pin+1)                                ' Enable DP
```

### Key Points

- Smart Pin handles physical layer signaling
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


*This chapter covered the USB Smart Pin mode. For a complete mode reference, see Appendix A. For application examples combining multiple modes, see Appendix C.*
