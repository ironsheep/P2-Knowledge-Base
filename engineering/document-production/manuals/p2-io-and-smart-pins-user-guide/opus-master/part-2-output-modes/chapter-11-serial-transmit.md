# Chapter 11: Serial Transmission {#ch11}

This chapter covers the serial transmission modes: **P_ASYNC_TX** (%11110) for asynchronous UART-style transmission and **P_SYNC_TX** (%11100) for synchronous SPI-style transmission.


## 11.1 Serial Transmission Overview

### Asynchronous vs Synchronous

| Aspect | Asynchronous (UART) | Synchronous (SPI) |
|--------|---------------------|-------------------|
| Clock | Implicit (baud rate) | Explicit (clock line) |
| Framing | Start/stop bits | None |
| Pins | 1 (TX) | 2 (Data + Clock) |
| Timing | Self-synchronizing | Clock-synchronized |
| Use case | Point-to-point | Bus communication |

### P2 Smart Pin Serial Features

- Hardware-generated timing and framing
- 1 to 32 bits per frame
- Fractional baud rate for precise timing
- Double-buffered transmission
- IN flag indicates ready for next data


## 11.2 P_ASYNC_TX Mode (%11110)

### Function

P_ASYNC_TX transmits asynchronous serial data with automatic start and stop bit generation. The output idles high, transitions low for the start bit, transmits data bits LSB first, then returns high for the stop bit.

### Frame Format

```{=latex}
\DiagUartTxFrame
```

### Configuration

| Register | Field | Purpose |
|----------|-------|---------|
| X[31:16] | Bit period | System clocks per bit (integer part) |
| X[15:10] | Fractional | Base-2 fractional clocks (1/64 increments), honored only when X[31:26]=0 (integer bit period < 1024 clocks) |
| X[4:0] | Bit count | Word size minus 1 (write 7 for 8-bit; supports 1-32 bits) |
| Y[31:0] | Data | Transmit data (LSB first) |

### Baud Rate Calculation

**Basic formula (integer only):**
```formula
X[31:16] = sysclk / baud_rate

Example: 200 MHz, 115200 baud
X[31:16] = 200,000,000 / 115,200 = 1736
```

**With fractional precision:**
```formula
bit_period = (sysclk / baud_rate) × 65536
X[31:10] = bit_period & $FFFFFC00

Example: 200 MHz, 115200 baud
bit_period = (200,000,000 / 115,200) × 65536 = 113,777,778
X[31:10] = 113,777,778 & $FFFFFC00 = $06C8_1C00
```

### Common Baud Rates at 200 MHz

| Baud Rate | X[31:16] (integer) | X (with fractional) | Error |
|-----------|-------------------|---------------------|-------|
| 9600 | 20833 | $5161_5400 | 0.00% |
| 19200 | 10416 | $28B0_A800 | 0.00% |
| 38400 | 5208 | $1458_5400 | 0.01% |
| 57600 | 3472 | $0D90_3800 | 0.01% |
| 115200 | 1736 | $06C8_1C00 | 0.01% |
| 230400 | 868 | $0364_0C00 | 0.01% |
| 460800 | 434 | $01B2_0400 | 0.01% |
| 921600 | 217 | $00D9_0000 | 0.01% |
| 1000000 | 200 | $00C8_0000 | 0.00% |

### Configuration Sequence

**Spin2:**
```spin2
CON
  _clkfreq = 200_000_000
  TX_PIN = 20
  BAUD = 115200

PUB uart_tx_init() | bit_period
  ' Calculate integer bit period (X[31:16] = clocks per bit)
  bit_period := (_clkfreq / BAUD) << 16

  PINFLOAT(TX_PIN)
  WRPIN(TX_PIN, P_ASYNC_TX | P_OE)
  WXPIN(TX_PIN, bit_period | 7)            ' 8 data bits (X[4:0] = N - 1)
  PINLOW(TX_PIN)

PUB tx_byte(value)
  ' Wait until transmitter ready
  repeat until PINREAD(TX_PIN)
  WYPIN(TX_PIN, value)
```

**PASM2:**
```pasm2
              mov       bit_period, ##(200_000_000 / 115200) << 16
              or        bit_period, #7     ' 8 data bits (X[4:0] = N - 1)

              dirl      #TX_PIN
              wrpin     ##(P_ASYNC_TX | P_OE), #TX_PIN
              wxpin     bit_period, #TX_PIN
              dirh      #TX_PIN

.wait         testp     #TX_PIN wc            ' Check IN flag
        if_nc jmp       #.wait
              wypin     data, #TX_PIN         ' Transmit byte
```

### RS-232 Polarity

Standard RS-232 uses inverted logic. Use P_INVERT_OUTPUT to match:

```spin2
mode := P_ASYNC_TX | P_OE | P_INVERT_OUTPUT
```

### Parity Implementation

P2 does not generate parity in hardware. Calculate and include parity as an extra bit:

```spin2
PUB tx_byte_with_parity(value) | parity, data9
  ' Calculate even parity
  parity := value
  parity ^= parity >> 4
  parity ^= parity >> 2
  parity ^= parity >> 1
  parity &= 1

  ' Combine 8 data bits + parity
  data9 := value | (parity << 8)

  ' Configure for 9 bits (X[4:0] = N - 1 = 8)
  WXPIN(TX_PIN, (bit_period & $FFFF0000) | 8)

  repeat until PINREAD(TX_PIN)
  WYPIN(TX_PIN, data9)
```


## 11.3 P_SYNC_TX Mode (%11100)

### Function

P_SYNC_TX transmits synchronous serial data clocked by an external or companion clock signal. Data shifts out on clock edges, with no start or stop bits. This mode is suitable for SPI master transmission, shift register control, and other synchronous protocols.

### Critical: Clock Routing

By default, the B-input reads from the local pin, which is useless for synchronous transmission where the clock is on a different pin.

**Required:** Add a pin-selection constant to route the clock:

| Constant | Clock Source |
|----------|--------------|
| P_PLUS1_B | Pin + 1 |
| P_MINUS1_B | Pin - 1 |
| P_PLUS2_B | Pin + 2 |
| P_MINUS2_B | Pin - 2 |
| P_PLUS3_B | Pin + 3 |
| P_MINUS3_B | Pin - 3 |

**Wrong:**
```antipattern
mode := P_SYNC_TX | P_OE                    ' NO CLOCK ROUTING!
```

**Correct:**
```spin2
mode := P_SYNC_TX | P_OE | P_PLUS1_B        ' Clock from pin+1
```

### Configuration

| Register | Field | Purpose |
|----------|-------|---------|
| X[5] | Mode | 0 = Continuous, 1 = Start-stop |
| X[4:0] | Bit count | Number of bits minus 1 (0-31 for 1-32 bits) |
| Y[31:0] | Data | Transmit data (LSB first) |

### Transmission Modes

**Continuous Mode (X[5] = 0):**

- Double-buffered for gapless transmission
- Prime shifter with first data before enabling
- Buffer automatically loads to shifter after transmission
- IN flag indicates buffer empty

**Start-Stop Mode (X[5] = 1):**

- Data can be modified before clock starts
- Suitable for non-continuous transmissions
- More control over timing

### Clock Edge Selection

| Clock Edge | Configuration |
|------------|---------------|
| Positive (rising) | Default (no modifier) |
| Negative (falling) | Add P_INVERT_B (inverts the B/clock input) |

### Configuration Sequence

**Spin2 (SPI Master TX, Positive Edge):**
```spin2
CON
  TX_PIN = 41
  CLK_PIN = 40

PUB spi_master_init() | tx_mode, clk_mode
  ' Configure data pin
  tx_mode := P_SYNC_TX | P_OE | P_MINUS1_B  ' Clock from CLK_PIN

  PINFLOAT(TX_PIN)
  WRPIN(TX_PIN, tx_mode)
  WXPIN(TX_PIN, %1_00111)                   ' Start-stop, 8 bits
  PINLOW(TX_PIN)

  ' Configure clock using transition mode
  clk_mode := P_TRANSITION | P_OE

  PINFLOAT(CLK_PIN)
  WRPIN(CLK_PIN, clk_mode)
  WXPIN(CLK_PIN, $1000)                     ' clocks between transitions
  PINLOW(CLK_PIN)

PUB spi_tx_byte(value)
  WYPIN(TX_PIN, value)                      ' Load data
  WYPIN(CLK_PIN, 16)                        ' 16 transitions = 8 clocks
```

**PASM2:**
```pasm2
              ' Setup sync serial TX (positive edge)
              dirl      #TX_PIN
              wrpin     ##(P_SYNC_TX | P_OE | P_MINUS1_B), #TX_PIN
              wxpin     #%1_00111, #TX_PIN    ' Start-stop, 8 bits
              dirh      #TX_PIN

              ' Setup clock generator
              dirl      #CLK_PIN
              wrpin     ##(P_TRANSITION | P_OE), #CLK_PIN
              wxpin     ##$1000, #CLK_PIN     ' clocks between transitions
              dirh      #CLK_PIN

              ' Transmit byte
              wypin     data, #TX_PIN         ' Load data
              wypin     #16, #CLK_PIN         ' Generate 8 clock cycles
```

### MSB-First Transmission

P_SYNC_TX transmits LSB first. For MSB-first protocols (like most SPI):

**Spin2:**
```spin2
PUB spi_tx_msb_first(value) | reversed
  ' reverse the data bits for MSB-first
  ' REV 7 reverses the low 8 bits (REV n covers bits 0..n)
  reversed := value REV 7

  WYPIN(TX_PIN, reversed)
  WYPIN(CLK_PIN, 16)
```

**PASM2:**
```pasm2
              shl       data, #32-8     ' left-justify byte into high bits
              rev       data            ' reverse to low 8 bits, MSB-first
              wypin     data, #TX_PIN
              wypin     #16, #CLK_PIN
```

### Continuous Streaming

For continuous data streams without gaps:

```spin2
PUB continuous_stream()
  ' Prime the shifter before enabling
  WYPIN(TX_PIN, first_byte)

  ' Enable pin
  PINLOW(TX_PIN)

  ' Load second byte into buffer
  WYPIN(TX_PIN, second_byte)

  ' Continuous transmission loop
  repeat
    if PINREAD(TX_PIN)                      ' IN raised = buffer ready
      WYPIN(TX_PIN, get_next_byte())        ' Load next
```


## 11.4 Clock Generation

### Using P_TRANSITION for SPI Clock

The P_TRANSITION mode generates clock signals for synchronous transmission:

```spin2
CON
  CLK_PIN = 40

PUB clock_setup(period)
  PINFLOAT(CLK_PIN)
  WRPIN(CLK_PIN, P_TRANSITION | P_OE)
  WXPIN(CLK_PIN, period)                    ' Clocks per half-period
  PINLOW(CLK_PIN)

PUB send_clocks(count)
  WYPIN(CLK_PIN, count * 2)                 ' 2 transitions per clock
```

### Clock Polarity (CPOL)

| CPOL | Idle State | Configuration |
|------|------------|---------------|
| 0 | Low | Default |
| 1 | High | Add P_INVERT_OUTPUT on clock pin |

### Clock Phase (CPHA)

| CPHA | Data Sample Edge | Data Change Edge |
|------|------------------|------------------|
| 0 | Leading (first) | Trailing (second) |
| 1 | Trailing (second) | Leading (first) |

For CPHA=1, add P_INVERT_B to the data pin, which inverts its B (clock) input and moves the shift edge.


## 11.5 Worked Examples

### Example 1: UART Debug Console

```spin2
CON
  _clkfreq = 200_000_000
  TX_PIN = 62
  BAUD = 115200

VAR
  long bit_period

PUB start()
  bit_period := (_clkfreq / BAUD) << 16

  PINFLOAT(TX_PIN)
  WRPIN(TX_PIN, P_ASYNC_TX | P_OE)
  WXPIN(TX_PIN, bit_period | 7)            ' 8 data bits (X[4:0] = N - 1)
  PINLOW(TX_PIN)

PUB tx(c)
  repeat until PINREAD(TX_PIN)
  WYPIN(TX_PIN, c)

PUB str(s) | c
  repeat
    c := byte[s++]
    if c == 0
      quit
    tx(c)

PUB dec(value) | digits[12], count
  count := 0
  if value < 0
    tx("-")
    value := -value
  repeat
    digits[count++] := value // 10 + "0"
    value /= 10
  until value == 0
  repeat count
    tx(digits[--count])

PUB hex(value, digits)
  repeat digits
    digits--
    tx(lookupz((value >> (digits * 4)) & $F : "0".."9", "A".."F"))

PUB newline()
  tx(13)
  tx(10)
```

### Example 2: SPI Master (Mode 0)

```{.spin2 caption="ch11-spi-master.spin2"}
CON
  _clkfreq = 200_000_000
  MOSI_PIN = 41
  CLK_PIN = 40
  CS_PIN = 39
  SPI_PERIOD = 50                           ' 2 MHz at 200 MHz sysclk

PUB spi_init()
  ' Configure MOSI
  PINFLOAT(MOSI_PIN)
  WRPIN(MOSI_PIN, P_SYNC_TX | P_OE | P_MINUS1_B)
  WXPIN(MOSI_PIN, %1_00111)                 ' Start-stop, 8 bits
  PINLOW(MOSI_PIN)

  ' Configure CLK
  PINFLOAT(CLK_PIN)
  WRPIN(CLK_PIN, P_TRANSITION | P_OE)
  WXPIN(CLK_PIN, SPI_PERIOD)
  PINLOW(CLK_PIN)

  ' Configure CS (active low)
  PINHIGH(CS_PIN)

PUB spi_select()
  PINLOW(CS_PIN)

PUB spi_deselect()
  PINHIGH(CS_PIN)

PUB spi_tx_byte(value) | reversed
  ' MSB first: reverse the 8 data bits (REV n covers bits 0..n)
  reversed := value REV 7

  WYPIN(MOSI_PIN, reversed)
  WYPIN(CLK_PIN, 16)                        ' 8 clock cycles

  ' Wait for the clock transitions to finish (IN on the P_TRANSITION clock
  ' pin rises when its transition count reaches zero; MOSI's IN only
  ' signals buffer-ready)
  repeat until PINREAD(CLK_PIN)

PUB spi_write_register(addr, value)
  spi_select()
  spi_tx_byte(addr)
  spi_tx_byte(value)
  spi_deselect()
```

### Example 3: Multi-Byte UART Transmission

```spin2
CON
  _clkfreq = 200_000_000
  TX_PIN = 20
  BAUD = 1_000_000                          ' 1 Mbps

PUB fast_uart_init() | bit_period
  bit_period := (_clkfreq / BAUD) << 16

  PINFLOAT(TX_PIN)
  WRPIN(TX_PIN, P_ASYNC_TX | P_OE)
  WXPIN(TX_PIN, bit_period | 7)            ' 8 data bits (X[4:0] = N - 1)
  PINLOW(TX_PIN)

PUB tx_buffer(ptr, count) | i
  ' Transmit buffer as fast as possible
  repeat i from 0 to count - 1
    repeat until PINREAD(TX_PIN)
    WYPIN(TX_PIN, byte[ptr + i])
```

### Example 4: PASM2 High-Speed Serial

```pasm2
CON
  _clkfreq = 200_000_000
  TX_PIN   = 20

DAT           org

' Initialize async TX
              mov       x_val, ##(200_000_000 / 115200) << 16
              or        x_val, #7            ' 8 data bits (X[4:0] = N - 1)

              dirl      #TX_PIN
              wrpin     ##(P_ASYNC_TX | P_OE), #TX_PIN
              wxpin     x_val, #TX_PIN
              dirh      #TX_PIN

' Transmit message
              mov       ptra, ##message
tx_loop
              rdbyte    data, ptra++
              cmp       data, #0 wz
        if_z  jmp       #done

.wait         testp     #TX_PIN wc
        if_nc jmp       #.wait

              wypin     data, #TX_PIN
              jmp       #tx_loop

done          jmp       #$

x_val         long      0
data          long      0
message       byte      "Hello, PASM2!", 13, 10, 0
              alignl
```


## 11.6 Baud Rate Error Analysis

### Error Calculation

```formula
actual_baud = sysclk / round(sysclk / target_baud)
error = abs(actual_baud - target_baud) / target_baud × 100%
```

### Maximum Allowable Error

UART receivers typically tolerate ±2-3% baud rate error. At 10 bits per frame (start + 8 data + stop), cumulative error must not exceed half a bit period.

### Fractional Timing Benefits

The X[15:10] fractional field is honored by the hardware only when X[31:26]=0 — that is, when the integer bit period is below 1024 clocks. At 200 MHz that condition is met only above ~195 kHz baud (230400 and up); for 9600-115200 baud the fractional bits are ignored and the integer-only error applies.

| Method | Precision | Error at 115200 baud (200 MHz) |
|--------|-----------|---------------------|
| Integer only | 1 clock | ~0.01% |
| With X[15:10] | 1/64 clock | ignored at this baud (period = 1736 clocks > 1024) |


## 11.7 Quick Reference

### P_ASYNC_TX Configuration

| Parameter | Register | Notes |
|-----------|----------|-------|
| Bit period | X[31:16] | sysclk / baud |
| Fractional | X[15:10] | 1/64 clock precision (honored only when X[31:26]=0, i.e. bit period < 1024 clocks) |
| Data bits | X[4:0] | Word size minus 1 (write 7 for 8-bit; supports 1-32 bits) |
| Data | Y | LSB first |
| Ready flag | IN | High when ready |

### P_SYNC_TX Configuration

| Parameter | Register | Notes |
|-----------|----------|-------|
| Mode | X[5] | 0=continuous, 1=start-stop |
| Bit count | X[4:0] | N-1 for N bits |
| Data | Y | LSB first |
| Buffer empty | IN | High when empty |
| Clock source | Mode | Must add P_PLUS1_B etc. |

### Mode Constants

| Constant | Value | Purpose |
|----------|-------|---------|
| P_ASYNC_TX | %11110 | Async serial transmit |
| P_SYNC_TX | %11100 | Sync serial transmit |
| P_OE | - | Enable output |
| P_INVERT_OUTPUT | - | Invert signal (RS-232) |
| P_PLUS1_B | - | Clock from pin+1 |
| P_MINUS1_B | - | Clock from pin-1 |

### Baud Rate Formula

```formula
X = (sysclk / baud) << 16 | data_bits

With fractional:
X = ((sysclk * 65536 / baud) & $FFFFFC00) | data_bits
```

### Reset State (DIR=0)

- P_ASYNC_TX: Output high (idle state)
- P_SYNC_TX: Output low, data can be primed


*This chapter covered serial transmission modes. For serial reception modes, see Chapter 17. For other input modes, see Part III.*
