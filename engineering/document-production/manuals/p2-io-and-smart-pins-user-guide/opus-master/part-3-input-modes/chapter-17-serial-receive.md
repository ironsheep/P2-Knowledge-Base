# Chapter 17: Serial Receive {#ch17}

This chapter covers receiving serial data using smart pin modes P_SYNC_RX (%11101) for synchronous (SPI-style) reception and P_ASYNC_RX (%11111) for asynchronous (UART-style) reception. Topics include baud rate configuration, clock routing, data formatting, and error handling.


## 17.1 Serial Receive Modes Overview

### Available Modes

| Mode | Constant | Description |
|------|----------|-------------|
| %11101 | P_SYNC_RX | Synchronous serial receive (data + external clock) |
| %11111 | P_ASYNC_RX | Asynchronous serial receive (UART/RS-232 style) |

### Mode Selection

**Choose P_SYNC_RX when:**

- External clock signal available (SPI slave, shift register)
- Clock provided by transmitting device
- Precise bit timing controlled externally

**Choose P_ASYNC_RX when:**

- No external clock (UART, RS-232)
- Both ends agree on baud rate
- Standard serial communication


## 17.2 Mode %11111: P_ASYNC_RX (Asynchronous Receive)

### Operation

Receives serial data asynchronously with automatic start bit detection. The smart pin monitors for a high-to-low transition (start bit), samples data bits at mid-bit timing, and validates the stop bit.

```{=latex}
\DiagUartRxFrame
```

### X Register Configuration

```layout
X[31:16]: System clock periods per bit (integer part)
X[15:10]: Fractional clock periods (1/64th increments)
X[9:5]:   Reserved
X[4:0]:   Number of data bits minus 1 (0-31 for 1-32 bits)
```

### Baud Rate Calculation

**Basic formula:**
```formula
bit_period = sysclk / baud
X_value = (bit_period << 16) | (data_bits - 1)
```

**With fractional precision:**
```spin2
bit_period_frac := (_clkfreq * 65536) / baud
X_value := (bit_period_frac & $FFFFFC00) | (data_bits - 1)
```

**Common baud rates at 200 MHz:**

| Baud | Clocks/bit | X[31:16] Value |
|------|------------|----------------|
| 9600 | 20833 | $5161 |
| 19200 | 10417 | $28B1 |
| 38400 | 5208 | $1458 |
| 57600 | 3472 | $0D90 |
| 115200 | 1736 | $06C8 |
| 230400 | 868 | $0364 |
| 460800 | 434 | $01B2 |
| 921600 | 217 | $00D9 |

### Data Justification

RDPIN and RQPIN return the received word **MSB-justified** at Z[31]. For an N-bit word, the data occupies Z[31:32-N]; right-shift by **32 - N** to LSB-justify. Failing to shift produces incorrect values (a received 8-bit byte appears as a 32-bit value with the byte in the upper 8 bits and the low byte always zero).

| Data bits (N) | Z occupancy | Right shift |
|---------------|-------------|-------------|
| 8 | Z[31:24] | `>> 24` (Spin2) / `SHR D,#24` (PASM2) |
| 9 | Z[31:23] | `>> 23` |
| 16 | Z[31:16] | `>> 16` |
| 32 | Z[31:0] | none |

This applies equally to async and sync RX modes.

### Basic UART Reception

```spin2
CON
  _clkfreq = 200_000_000
  RX_PIN = 21
  BAUD = 115_200

PUB uart_init() | bit_period
  bit_period := _clkfreq / BAUD
  PINSTART(RX_PIN, P_ASYNC_RX, (bit_period << 16) | 7, 0)  ' 8 data bits

PUB receive_byte() : value
  REPEAT UNTIL PINREAD(RX_PIN)                  ' Wait for data
  value := RDPIN(RX_PIN) >> 24            ' LSB-justify 8-bit byte (32-8)
```

### Reception with Timeout

```spin2
PUB receive_with_timeout(timeout_ms) : value | deadline
  deadline := GETMS() + timeout_ms

  REPEAT
    IF PINREAD(RX_PIN)
      RETURN RDPIN(RX_PIN) >> 24      ' Data received (LSB-justify 8-bit)

    IF GETMS() >= deadline
      RETURN -1                                 ' Timeout

PUB has_data() : available
  available := PINREAD(RX_PIN) <> 0
```

### PASM2 UART Reception

```pasm2
CON
  _clkfreq = 200_000_000
  RX_PIN = 21
  BAUD = 115_200

DAT           org

              ' Calculate bit period
              mov       bit_period, ##_clkfreq / BAUD
              shl       bit_period, #16
              or        bit_period, #7            ' 8 data bits

              ' Configure UART receive
              dirl      #RX_PIN
              wrpin     ##P_ASYNC_RX, #RX_PIN
              wxpin     bit_period, #RX_PIN
              dirh      #RX_PIN

.receive_loop
              testp     #RX_PIN wc                ' Check IN flag
        if_nc jmp       #.receive_loop            ' Wait for data

              rdpin     rx_data, #RX_PIN        ' Read MSB-justified word
              shr       rx_data, #24      ' LSB-justify 8-bit byte (32-8)
              ' Process rx_data...

              jmp       #.receive_loop

bit_period    res       1
rx_data       res       1
```


## 17.3 Mode %11101: P_SYNC_RX (Synchronous Receive)

### Operation

Receives serial data synchronized to an external clock signal. Data is sampled on clock edges, with the A-input carrying data and B-input carrying the clock.

### Critical: Clock Routing

**The B-input defaults to the local pin, which is useless for SPI.** You MUST add a pin-selection constant:

```spin2
' WRONG - no clock routing:
mode := P_SYNC_RX                               ' Will not work!

' CORRECT - clock from adjacent pin:
mode := P_SYNC_RX | P_PLUS1_B                   ' Clock on pin+1
```

### Pin Selection Constants

| Constant | Clock Source |
|----------|--------------|
| P_PLUS1_B | Next pin (pin+1) |
| P_MINUS1_B | Previous pin (pin-1) |
| P_PLUS2_B | Pin+2 |
| P_PLUS3_B | Pin+3 |
| P_MINUS2_B | Pin-2 |
| P_MINUS3_B | Pin-3 |

### X Register Configuration

```layout
X[5]:   Sample timing (0=before edge, 1=on edge)
X[4:0]: Number of bits minus 1
```

**Sample Timing:**

- X[5]=0 (before edge): More tolerant, works with any transmitter
- X[5]=1 (on edge): Fast P2-to-P2 transfers, requires 2-clock hold time

### Data Justification

Received data is **left-justified** in the Z register. For less than 32 bits, right-shift to align:

| Bits | Z Register | Right Shift |
|------|------------|-------------|
| 8 | Z[31:24] | SHR #24 |
| 16 | Z[31:16] | SHR #16 |
| 32 | Z[31:0] | None |

### Basic SPI Slave Receive

```spin2
CON
  _clkfreq = 200_000_000
  MISO_PIN = 30                                 ' Data input
  SCK_PIN = 31                               ' Clock input (MISO_PIN + 1)

PUB spi_slave_init()
  ' 8-bit receive, clock on next pin, sample before edge
  PINSTART(MISO_PIN, P_SYNC_RX | P_PLUS1_B, %0_00111, 0)

PUB receive_byte() : value
  REPEAT UNTIL PINREAD(MISO_PIN)                ' Wait for 8 bits
  value := RDPIN(MISO_PIN) >> 24                ' Read and right-justify
```

### MSB-First Reception

Standard sync receive is LSB-first. For MSB-first protocols, reverse the bits:

```spin2
PUB receive_msb_first() : value
  REPEAT UNTIL PINREAD(MISO_PIN)
  value := RDPIN(MISO_PIN)
  value := value REV 32                         ' Reverse all 32 bits
  value := value & $FF                          ' Mask to 8 bits
```

**PASM2:**
```pasm2
              rdpin     data, #MISO_PIN
              rev       data                    ' Reverse all 32 bits
              zerox     data, #7                ' Keep only bits 0-7
```

### Clock Polarity

For inverted clock (sample on falling edge):

```spin2
PINSTART(DATA_PIN, P_SYNC_RX | P_PLUS1_B | P_INVERT_B, %0_00111, 0)
```

### PASM2 SPI Slave

```pasm2
CON
  _clkfreq = 200_000_000
  DATA_PIN = 30
  CLK_PIN = 31

DAT           org

              ' Configure sync receive, clock from pin+1
              dirl      #DATA_PIN
              wrpin     ##P_SYNC_RX | P_PLUS1_B, #DATA_PIN
              wxpin     #%0_00111, #DATA_PIN    ' Pre-edge, 8 bits
              dirh      #DATA_PIN

.receive_loop
              testp     #DATA_PIN wc            ' Check IN flag
        if_nc jmp       #.receive_loop

              rdpin     rx_byte, #DATA_PIN      ' Read data
              shr       rx_byte, #24            ' Right-justify

              ' Process rx_byte...
              jmp       #.receive_loop

rx_byte       res       1
```


## 17.4 Full-Duplex UART

### Transmit and Receive Configuration

```spin2
CON
  _clkfreq = 200_000_000
  TX_PIN = 20
  RX_PIN = 21
  BAUD = 115_200

VAR
  long tx_ready
  long rx_data

PUB serial_init() | bit_period
  bit_period := _clkfreq / BAUD

  ' Configure TX
  PINSTART(TX_PIN, P_ASYNC_TX | P_OE, (bit_period << 16) | 7, 0)

  ' Configure RX
  PINSTART(RX_PIN, P_ASYNC_RX, (bit_period << 16) | 7, 0)

PUB send_byte(value)
  REPEAT UNTIL PINREAD(TX_PIN)                  ' Wait for TX ready
  WYPIN(TX_PIN, value)

PUB receive_byte() : value
  REPEAT UNTIL PINREAD(RX_PIN)
  value := RDPIN(RX_PIN) >> 24                  ' LSB-justify 8-bit byte

PUB echo_test()
  ' Echo received bytes back to sender
  REPEAT
    IF PINREAD(RX_PIN)
      send_byte(RDPIN(RX_PIN) >> 24)       ' LSB-justify before resending
```

### Half-Duplex Coordination

For half-duplex protocols (RS-485, single-wire):

```spin2
CON
  DATA_PIN = 20
  DIR_PIN = 21                                  ' Direction control
  TX_PIN = DATA_PIN               ' Single-wire: TX and RX share DATA_PIN
  RX_PIN = DATA_PIN

PUB send_message(ptr, len) | i
  PINHIGH(DIR_PIN)                              ' Enable transmitter
  WAITUS(10)                                    ' Allow turnaround

  REPEAT i FROM 0 TO len-1
    send_byte(BYTE[ptr][i])

  REPEAT UNTIL PINREAD(TX_PIN)                  ' Wait for last byte
  WAITUS(100)                                   ' Bit time + margin
  PINLOW(DIR_PIN)                               ' Enable receiver

PUB receive_message(ptr, max_len, timeout_ms) : count | deadline, b
  count := 0
  deadline := GETMS() + timeout_ms

  REPEAT WHILE count < max_len
    IF PINREAD(RX_PIN)
      b := RDPIN(RX_PIN) >> 24                  ' LSB-justify 8-bit byte
      BYTE[ptr][count++] := b
      deadline := GETMS() + timeout_ms          ' Reset timeout
    ELSEIF GETMS() >= deadline
      QUIT                                     ' Timeout - end of message

PRI send_byte(b)
  ' Application-specific: TX byte b via DATA_PIN (configured for TX)
```


## 17.5 Buffered Reception

### Circular Buffer

```spin2
CON
  RX_PIN = 63
  BUFFER_SIZE = 256                             ' Must be power of 2
  BUFFER_MASK = BUFFER_SIZE - 1

VAR
  byte rx_buffer[BUFFER_SIZE]
  long head, tail

PUB buffer_init()
  head := 0
  tail := 0

PUB poll_rx()
  ' Call frequently to move data from pin to buffer
  IF PINREAD(RX_PIN)
    rx_buffer[head] := RDPIN(RX_PIN) >> 24      ' LSB-justify 8-bit byte
    head := (head + 1) & BUFFER_MASK
    ' Note: overwrites old data if buffer full

PUB available() : count
  count := (head - tail) & BUFFER_MASK

PUB read_byte() : value
  IF head == tail
    RETURN -1                                   ' Buffer empty

  value := rx_buffer[tail]
  tail := (tail + 1) & BUFFER_MASK
```

### Cog-Based Receiver

For continuous high-speed reception, use a dedicated cog:

```spin2
VAR
  long rx_cog
  long rx_stack[64]
  byte rx_buffer[1024]
  long rx_head

PUB start_receiver()
  rx_head := 0
  rx_cog := COGSPIN(NEWCOG, receiver_loop(), @rx_stack)

PRI receiver_loop()
  uart_init()

  REPEAT
    IF PINREAD(RX_PIN)
      rx_buffer[rx_head++] := RDPIN(RX_PIN) >> 24  ' LSB-justify byte
      IF rx_head >= 1024
        rx_head := 0                            ' Wrap around

PUB get_rx_head() : pos
  pos := rx_head
```


## 17.6 Error Detection

### Framing Error

A framing error occurs when the stop bit is not high. The P2 does not automatically flag this; framing errors are detected by examining received data:

```spin2
PUB receive_with_check() : value, error | raw
  ' Requires PINSTART configured for 9 data bits
  ' (X[4:0] = 8) to capture stop bit.
  REPEAT UNTIL PINREAD(RX_PIN)
  raw := RDPIN(RX_PIN) >> 23                    ' 9 bits, shift by 32-9

  ' After the shift: bits 7:0 are the data byte,
  ' bit 8 is the captured stop bit
  value := raw & $FF
  IF (raw & $100) == 0
    error := TRUE                               ' Missing stop bit
  ELSE
    error := FALSE

  value := raw & $FF
```

### Overrun Detection

Overrun occurs when new data arrives before previous data is read:

```spin2
VAR
  long last_read_time
  long overrun_count

PUB check_overrun() : overrun
  ' Track time between reads
  ' If the interval is too long, data is lost
  overrun := FALSE
  ' Application-specific logic based on baud rate
```

### Break Detection

A break is a prolonged low condition (longer than one frame):

```spin2
PUB detect_break(pin) : is_break | start_time
  IF PINREAD(pin) == 0                          ' Input is low
    start_time := GETMS()
    REPEAT WHILE PINREAD(pin) == 0
      IF (GETMS() - start_time) > 20            ' > frame time
        is_break := TRUE
        RETURN
  is_break := FALSE
```


## 17.7 RS-232 Signal Inversion

RS-232 uses inverted logic (mark=-3V to -15V, space=+3V to +15V). After level conversion to 3.3V logic, the signal is still inverted.

### Using P_INVERT_IN

```spin2
' For RS-232 with external level shifter
PINSTART(RX_PIN, P_ASYNC_RX | P_INVERT_IN, (bit_period << 16) | 7, 0)
```


## 17.8 Multi-Drop Networks

### RS-485 Reception

```spin2
CON
  _clkfreq = 200_000_000
  RX_PIN = 20
  TX_PIN = 21
  DE_PIN = 22                                   ' Driver Enable
  BAUD = 9600
  MY_ADDRESS = $05

PUB rs485_init() | bp
  bp := _clkfreq / BAUD
  PINSTART(RX_PIN, P_ASYNC_RX, (bp << 16) | 7, 0)
  PINSTART(TX_PIN, P_ASYNC_TX | P_OE, (bp << 16) | 7, 0)
  PINLOW(DE_PIN)                                ' Receiver enabled

PUB listen_for_address() : addressed | addr
  REPEAT
    IF PINREAD(RX_PIN)
      addr := RDPIN(RX_PIN) >> 24               ' LSB-justify 8-bit byte
      IF addr == MY_ADDRESS
        RETURN TRUE
      IF addr == $FF                            ' Broadcast
        RETURN TRUE
  RETURN FALSE
```


## 17.9 Application Examples

### Example 1: GPS NMEA Receiver

```spin2
CON
  _clkfreq = 200_000_000
  GPS_PIN = 20
  GPS_BAUD = 9600

VAR
  byte nmea_buffer[100]
  long buffer_idx

PUB gps_receiver() | ch
  ' Initialize 8N1 at 9600 baud
  PINSTART(GPS_PIN, P_ASYNC_RX, ((_clkfreq / GPS_BAUD) << 16) | 7, 0)

  buffer_idx := 0

  REPEAT
    IF PINREAD(GPS_PIN)
      ch := RDPIN(GPS_PIN) >> 24                ' LSB-justify 8-bit byte

      IF ch == "$"                              ' Start of sentence
        buffer_idx := 0

      nmea_buffer[buffer_idx++] := ch

      IF ch == 10                               ' End of line
        nmea_buffer[buffer_idx] := 0
        process_nmea(@nmea_buffer)
        buffer_idx := 0

      IF buffer_idx >= 99
        buffer_idx := 0                         ' Overflow protection

PRI process_nmea(ptr)
  ' Application-specific: parse NMEA sentence starting at ptr
```

### Example 2: SPI Sensor Read

```spin2
CON
  _clkfreq = 200_000_000
  MOSI_PIN = 30
  MISO_PIN = 31
  SCK_PIN = 32
  CS_PIN = 33

PUB read_sensor_register(reg_addr) : value
  ' Configure SPI
  PINSTART(MISO_PIN, P_SYNC_RX | P_PLUS1_B, %0_00111, 0)  ' 8 bits

  PINLOW(CS_PIN)                                ' Select device

  ' Send register address (would use TX pin)
  send_spi_byte(reg_addr | $80)                 ' Read flag

  ' Receive data
  REPEAT UNTIL PINREAD(MISO_PIN)
  value := RDPIN(MISO_PIN) >> 24

  PINHIGH(CS_PIN)                               ' Deselect

PRI send_spi_byte(b)
  ' Application-specific: clock byte b out via SPI TX pin
```

### Example 3: Command Parser

```{.spin2 caption="ch17-uart-command-loop.spin2"}
CON
  _clkfreq = 200_000_000
  RX_PIN = 21
  BAUD = 115_200

VAR
  byte cmd_buffer[64]
  long cmd_len

PUB command_loop() | ch
  PINSTART(RX_PIN, P_ASYNC_RX, ((_clkfreq / BAUD) << 16) | 7, 0)
  cmd_len := 0

  REPEAT
    IF PINREAD(RX_PIN)
      ch := RDPIN(RX_PIN) >> 24                 ' LSB-justify 8-bit byte

      CASE ch
        13:                                     ' Enter
          cmd_buffer[cmd_len] := 0
          execute_command(@cmd_buffer)
          cmd_len := 0

        8, 127:                                 ' Backspace/Delete
          IF cmd_len > 0
            cmd_len--

        32..126:                                ' Printable
          IF cmd_len < 63
            cmd_buffer[cmd_len++] := ch

PRI execute_command(ptr)
  IF STRCOMP(ptr, STRING("help"))
    send_string(STRING("Commands: help, status, reset"))
  ELSEIF STRCOMP(ptr, STRING("status"))
    send_string(STRING("System OK"))
  ' ... more commands

PRI send_string(ptr)
  ' Application-specific: TX null-terminated string at ptr
```


## 17.10 Quick Reference

### Mode Constants

| Constant | Mode | Description |
|----------|------|-------------|
| P_ASYNC_RX | %11111 | Asynchronous serial receive |
| P_SYNC_RX | %11101 | Synchronous serial receive |

### P_ASYNC_RX Configuration

**X Register:**

```layout
X[31:16]: Clocks per bit (sysclk / baud)
X[15:10]: Fractional clocks (precision)
X[4:0]:   Data bits - 1 (7 for 8-bit)
```

**Baud calculation:**
```spin2
X_value := ((sysclk / baud) << 16) | (bits - 1)
```

### P_SYNC_RX Configuration

**X Register:**
```layout
X[5]:   0=sample before edge, 1=sample on edge
X[4:0]: Data bits - 1
```

**Required modifier:** P_PLUS1_B (or similar) for clock routing

**Data justification:** Left-justified, SHR #(32-bits) to right-justify

### Related Modifiers

| Modifier | Function |
|----------|----------|
| P_INVERT_IN | Invert input (RS-232) |
| P_INVERT_B | Invert B-input clock |
| P_PLUS1_B | Clock on pin+1 |
| P_MINUS1_B | Clock on pin-1 |

### Common Patterns

**Blocking receive (8-bit example; shift by 32 - N for other widths):**
```spin2
REPEAT UNTIL PINREAD(pin)
value := RDPIN(pin) >> 24                       ' LSB-justify 8-bit byte
```

**Polled receive:**
```spin2
IF PINREAD(pin)
  value := RDPIN(pin) >> 24                     ' LSB-justify 8-bit byte
```

**With timeout:**
```spin2
deadline := GETMS() + timeout_ms
REPEAT UNTIL PINREAD(pin) OR (GETMS() >= deadline)
```


*This chapter covered serial reception. For special modes like USB, see Chapter 19. For inter-cog data sharing, see Chapter 18.*
