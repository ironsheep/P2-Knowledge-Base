# Spin2 Object Patterns Guide

## Overview

Spin2 objects are the fundamental units of code organization in the P2. Each `.spin2` file defines a single object that encapsulates constants, variables, methods, and data. This guide documents canonical object archetypes and patterns for building well-structured P2 applications.

**Object Capabilities:**
- **CON** - Named constants, enumerations
- **VAR** - Instance variables (separate per object instance)
- **OBJ** - Child object declarations
- **PUB** - Public methods (callable from parent objects)
- **PRI** - Private methods (internal only)
- **DAT** - Shared data, PASM code (shared across all instances)

**Key Design Principle:** Each object should have a single, clear responsibility. Combine simpler objects through composition rather than creating monolithic objects.

## Object Structure Basics

### Sections and Their Purpose

```spin2
CON                         ' Constants - named values, enums
  MAX_SIZE = 100
  BUFFER_MASK = MAX_SIZE - 1

VAR                         ' Instance variables - unique per object instance
  long count
  byte buffer[MAX_SIZE]

OBJ                         ' Child objects - composition
  serial : "serial_driver"

PUB method_name()           ' Public methods - external interface
  ' Implementation

PRI helper_method()         ' Private methods - internal implementation
  ' Implementation

DAT                         ' Data section - shared across instances, PASM code
              org     0
pasm_code     ' ...
```

### VAR vs DAT for State

| Aspect | VAR | DAT |
|--------|-----|-----|
| Scope | Per instance | Shared across all instances |
| Initialization | Zeroed on object creation | Initialized at compile time |
| Use case | Instance-specific data | Shared tables, PASM code, singletons |
| Memory | Allocated per instantiation | Single allocation for all |

```spin2
' VAR - each instance gets its own copy
VAR
  long instance_id           ' Unique per instance

' DAT - shared across all instances
DAT
  shared_table    long  1, 2, 3, 4    ' All instances see same data
  instance_count  long  0             ' Singleton counter
```

### PUB/PRI Visibility Design

**PUB (Public):** Methods callable by parent objects. These form the object's API.
- Keep the public interface minimal and stable
- Document parameters and return values
- Handle error cases gracefully

**PRI (Private):** Internal implementation methods.
- Use for shared code within the object
- Can change freely without affecting users
- Contain implementation details

```spin2
' Good API design - minimal public interface
PUB start(pin, rate) : ok
  ' Public: Initialize and start driver

PUB stop()
  ' Public: Clean shutdown

PUB tx(char)
  ' Public: Transmit one character

PUB rx() : char
  ' Public: Receive one character

PRI configure_hardware(pin, rate)
  ' Private: Implementation detail

PRI handle_interrupt()
  ' Private: Internal handler
```

## Object Archetypes

### 1. Top-Level Application

The top-level object is the entry point. It defines clock configuration and orchestrates other objects.

```spin2
'' ===========================================================================
''  Application: LED Blinker with Serial Output
'' ===========================================================================

CON { system configuration }

  _clkfreq = 200_000_000               ' 200 MHz system clock

CON { pin assignments }

  LED_PIN    = 56                      ' P2 Edge board LED
  SERIAL_TX  = 62                      ' Debug serial TX
  SERIAL_RX  = 63                      ' Debug serial RX
  BAUD_RATE  = 115_200

CON { application constants }

  BLINK_MS   = 500                     ' LED blink rate

OBJ

  serial : "serial_driver"

VAR

  long blink_count

PUB main() | ok
  '' Application entry point

  ' Initialize subsystems
  ok := serial.start(SERIAL_TX, SERIAL_RX, BAUD_RATE)
  if not ok
    repeat                             ' Halt on init failure

  serial.str(@"LED Blinker Started")
  serial.tx(13)

  ' Configure LED pin
  pinlow(LED_PIN)

  ' Main application loop
  repeat
    pintoggle(LED_PIN)
    blink_count++
    serial.str(@"Blink #")
    serial.dec(blink_count)
    serial.tx(13)
    waitms(BLINK_MS)

DAT

  app_name    byte  "LED Blinker v1.0", 0
```

**Key Characteristics:**
- Contains `_clkfreq` for clock configuration
- Owns a `main()` method (called by Spin2 runtime)
- Instantiates child objects
- Never instantiated by other objects

### 2. Driver Object

Driver objects provide hardware abstraction with a lifecycle (start/stop) and buffered I/O.

```spin2
'' ===========================================================================
''  Serial Driver - UART communication with buffering
'' ===========================================================================

CON { driver constants }

  NO_COG      = -1
  BUFFER_SIZE = 256
  BUFFER_MASK = BUFFER_SIZE - 1

VAR { instance state }

  long cog_id
  long rx_pin, tx_pin, baud
  long rx_head, rx_tail
  long tx_head, tx_tail
  byte rx_buffer[BUFFER_SIZE]
  byte tx_buffer[BUFFER_SIZE]
  long stack[100]

PUB start(txp, rxp, baudrate) : ok
  '' Initialize and start the serial driver
  '' Returns TRUE if successful

  stop()                               ' Stop if already running

  ' Store configuration
  tx_pin := txp
  rx_pin := rxp
  baud := baudrate

  ' Initialize buffers
  rx_head := rx_tail := 0
  tx_head := tx_tail := 0

  ' Start driver COG
  cog_id := cogspin(NEWCOG, driver_loop(), @stack)
  ok := (cog_id >= 0)

PUB stop()
  '' Stop the driver and release resources

  if cog_id >= 0
    cogstop(cog_id)
    cog_id := NO_COG

PUB tx(char)
  '' Transmit one character (blocks if buffer full)

  repeat while ((tx_head + 1) & BUFFER_MASK) == tx_tail
  tx_buffer[tx_head] := char
  tx_head := (tx_head + 1) & BUFFER_MASK

PUB rx() : char
  '' Receive one character (blocks until available)

  repeat while rx_head == rx_tail
  char := rx_buffer[rx_tail]
  rx_tail := (rx_tail + 1) & BUFFER_MASK

PUB rxcheck() : char
  '' Check for received character
  '' Returns character or -1 if none available

  if rx_head == rx_tail
    return -1
  char := rx_buffer[rx_tail]
  rx_tail := (rx_tail + 1) & BUFFER_MASK

PUB str(ptr)
  '' Transmit zero-terminated string

  repeat while byte[ptr]
    tx(byte[ptr++])

PUB dec(value) | d, i
  '' Transmit decimal value

  if value < 0
    tx("-")
    value := -value

  d := 1_000_000_000
  repeat 10
    if value >= d
      tx(value / d + "0")
      value //= d
    elseif d == 1
      tx("0")
    d /= 10

PRI driver_loop() | char
  '' Driver COG main loop

  ' Configure pins for UART
  pinstart(tx_pin, P_ASYNC_TX, 7, baud)
  pinstart(rx_pin, P_ASYNC_RX, 7, baud)

  repeat
    ' Handle receive
    if pinread(rx_pin)
      char := rdpin(rx_pin)
      if ((rx_head + 1) & BUFFER_MASK) <> rx_tail
        rx_buffer[rx_head] := char
        rx_head := (rx_head + 1) & BUFFER_MASK

    ' Handle transmit
    if tx_head <> tx_tail
      if not pintestn(tx_pin)          ' TX ready?
        wypin(tx_pin, tx_buffer[tx_tail])
        tx_tail := (tx_tail + 1) & BUFFER_MASK
```

**Key Characteristics:**
- `start()` / `stop()` lifecycle methods
- Tracks COG ID for cleanup
- Buffered I/O for non-blocking operation
- Hardware abstraction - callers don't need pin/timing details

### 3. Library Object (Stateless Utilities)

Library objects provide utility functions with no internal state. No initialization required.

```spin2
'' ===========================================================================
''  Math Library - Stateless mathematical utilities
'' ===========================================================================

PUB min(a, b) : result
  '' Return the smaller of two values

  result := a < b ? a : b

PUB max(a, b) : result
  '' Return the larger of two values

  result := a > b ? a : b

PUB clamp(value, low, high) : result
  '' Constrain value to range [low, high]

  result := value #> low <# high

PUB abs_val(value) : result
  '' Return absolute value

  result := abs value

PUB map(value, in_min, in_max, out_min, out_max) : result
  '' Map value from one range to another

  result := (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

PUB is_power_of_two(n) : result
  '' Check if n is a power of 2

  result := (n > 0) AND (ones n == 1)

PUB gcd(a, b) : result
  '' Greatest common divisor using Euclidean algorithm

  if b == 0
    return abs a
  repeat while b
    result := b
    b := a // b
    a := result

PUB crc8(ptr, length) : crc | i, byte_val
  '' Calculate CRC-8 checksum

  crc := 0
  repeat i from 0 to length - 1
    byte_val := byte[ptr][i]
    crc ^= byte_val
    repeat 8
      if crc & $80
        crc := (crc << 1) ^ $07
      else
        crc <<= 1
      crc &= $FF
```

**Key Characteristics:**
- No VAR section (no instance state)
- No initialization required
- All methods are pure functions
- Can be used immediately after instantiation

### 4. Singleton / Shared-State Object

Uses DAT section for state shared across all instances. Useful for system-wide resources.

```spin2
'' ===========================================================================
''  Logger - Singleton pattern using DAT for shared state
'' ===========================================================================

CON

  MAX_LOG_ENTRIES = 100
  ENTRY_SIZE      = 64

CON { log levels }

  LOG_DEBUG   = 0
  LOG_INFO    = 1
  LOG_WARNING = 2
  LOG_ERROR   = 3

DAT { shared state - all instances see the same log }

  log_lock      long  -1               ' Lock for thread safety
  log_head      long  0                ' Next write position
  log_count     long  0                ' Total entries written
  log_level     long  LOG_INFO         ' Minimum level to record
  log_buffer    byte  0[MAX_LOG_ENTRIES * ENTRY_SIZE]

PUB init() : ok
  '' Initialize the logger (call once at startup)

  if log_lock == -1
    log_lock := locknew()
  ok := (log_lock >= 0)

PUB shutdown()
  '' Release logger resources

  if log_lock >= 0
    lockret(log_lock)
    log_lock := -1

PUB set_level(level)
  '' Set minimum logging level

  log_level := level

PUB log(level, msg_ptr)
  '' Log a message if level >= current threshold

  if level < log_level
    return

  repeat until locktry(log_lock)

  ' Copy message to log buffer
  copy_entry(@log_buffer + (log_head * ENTRY_SIZE), msg_ptr, level)
  log_head := (log_head + 1) // MAX_LOG_ENTRIES
  log_count++

  lockrel(log_lock)

PUB get_entry(index, dest_ptr) : level
  '' Retrieve a log entry

  repeat until locktry(log_lock)

  if index < log_count AND index < MAX_LOG_ENTRIES
    level := retrieve_entry(@log_buffer + (index * ENTRY_SIZE), dest_ptr)
  else
    level := -1

  lockrel(log_lock)

PUB get_count() : count
  '' Return total number of log entries

  count := log_count

PRI copy_entry(dest, src, level) | i
  byte[dest][0] := level
  repeat i from 0 to ENTRY_SIZE - 2
    if byte[src][i] == 0
      quit
    byte[dest][i + 1] := byte[src][i]
  byte[dest][i + 1] := 0

PRI retrieve_entry(src, dest) : level | i
  level := byte[src][0]
  repeat i from 0 to ENTRY_SIZE - 2
    byte[dest][i] := byte[src][i + 1]
    if byte[src][i + 1] == 0
      quit
```

**Key Characteristics:**
- Uses DAT for state (shared across instances)
- Lock-protected for multi-COG safety
- Single initialization, multiple users
- Useful for logging, configuration, resource pools

### 5. Configurable Object (Constant Override)

Objects with overridable constants allow parent objects to customize behavior without code changes.

```spin2
'' ===========================================================================
''  Configurable Timer - Constants can be overridden by parent
'' ===========================================================================

CON { default configuration - can be overridden }

  DEFAULT_PERIOD_MS = 1000             ' Default: 1 second
  DEFAULT_COUNT     = 0                ' Default: unlimited (0 = forever)
  LED_PIN           = 56               ' Default: P2 Edge LED

VAR

  long period_ms
  long remaining
  long running

PUB start()
  '' Start the timer with default or overridden values

  period_ms := DEFAULT_PERIOD_MS
  remaining := DEFAULT_COUNT
  running := TRUE

  pinlow(LED_PIN)

PUB stop()
  '' Stop the timer

  running := FALSE
  pinfloat(LED_PIN)

PUB tick() : done
  '' Call periodically - returns TRUE when count exhausted

  if not running
    return FALSE

  pintoggle(LED_PIN)
  waitms(period_ms)

  if DEFAULT_COUNT > 0                 ' Only count if limit set
    remaining--
    if remaining == 0
      running := FALSE
      done := TRUE

PUB is_running() : status
  status := running
```

**Parent object using constant override:**

```spin2
'' ===========================================================================
''  Application using configurable timer
'' ===========================================================================

CON

  _clkfreq = 200_000_000

OBJ
  ' Three timers with different configurations
  fast_timer : "configurable_timer" | DEFAULT_PERIOD_MS = 100
  slow_timer : "configurable_timer" | DEFAULT_PERIOD_MS = 2000
  limited    : "configurable_timer" | DEFAULT_PERIOD_MS = 500, DEFAULT_COUNT = 10

PUB main()
  fast_timer.start()
  slow_timer.start()
  limited.start()

  repeat until limited.tick()         ' Run until limited timer exhausts
    fast_timer.tick()
    slow_timer.tick()

  fast_timer.stop()
  slow_timer.stop()
```

**Key Characteristics:**
- CON values serve as defaults
- Parent uses `| CONST = value` syntax to override
- Each override creates a separate object instance
- Enables compile-time configuration without preprocessor

### 6. Buffered I/O Object

Circular buffer pattern for producer-consumer communication.

```spin2
'' ===========================================================================
''  Ring Buffer - Circular buffer for streaming data
'' ===========================================================================

CON { default size - can be overridden }

  BUFFER_SIZE = 512                    ' Must be power of 2
  BUFFER_MASK = BUFFER_SIZE - 1

VAR

  long head                            ' Write position
  long tail                            ' Read position
  long buffer[BUFFER_SIZE]

PUB init()
  '' Initialize buffer to empty state

  head := tail := 0

PUB put(value) : ok
  '' Add value to buffer
  '' Returns TRUE if successful, FALSE if buffer full

  if ((head + 1) & BUFFER_MASK) == tail
    return FALSE                       ' Buffer full

  buffer[head] := value
  head := (head + 1) & BUFFER_MASK
  ok := TRUE

PUB get() : value
  '' Remove and return value from buffer
  '' Blocks if buffer empty

  repeat while head == tail
  value := buffer[tail]
  tail := (tail + 1) & BUFFER_MASK

PUB try_get() : value, ok
  '' Try to get value without blocking
  '' Returns ok=FALSE if buffer empty

  if head == tail
    ok := FALSE
    return

  value := buffer[tail]
  tail := (tail + 1) & BUFFER_MASK
  ok := TRUE

PUB peek() : value, ok
  '' View next value without removing
  '' Returns ok=FALSE if buffer empty

  if head == tail
    ok := FALSE
    return

  value := buffer[tail]
  ok := TRUE

PUB available() : count
  '' Return number of items in buffer

  count := (head - tail) & BUFFER_MASK

PUB space() : count
  '' Return space remaining in buffer

  count := (BUFFER_SIZE - 1) - available()

PUB is_empty() : empty
  '' Check if buffer is empty

  empty := (head == tail)

PUB is_full() : full
  '' Check if buffer is full

  full := (((head + 1) & BUFFER_MASK) == tail)

PUB flush()
  '' Discard all buffered data

  tail := head
```

**Key Characteristics:**
- Power-of-2 size enables fast modulo with AND
- Lock-free for single producer, single consumer
- Head/tail pointers track state
- Useful for inter-COG communication

### 7. State Machine Object

Encapsulates a state machine with explicit states and transitions.

```spin2
'' ===========================================================================
''  Connection State Machine - TCP-like connection lifecycle
'' ===========================================================================

CON { states }

  STATE_IDLE       = 0
  STATE_CONNECTING = 1
  STATE_CONNECTED  = 2
  STATE_CLOSING    = 3
  STATE_ERROR      = 4

CON { events }

  EVT_CONNECT      = 0
  EVT_CONNECTED    = 1
  EVT_SEND         = 2
  EVT_RECEIVE      = 3
  EVT_CLOSE        = 4
  EVT_TIMEOUT      = 5
  EVT_ERROR        = 6

VAR

  long current_state
  long error_code
  long retry_count

PUB init()
  '' Initialize state machine

  current_state := STATE_IDLE
  error_code := 0
  retry_count := 0

PUB process_event(event) : new_state
  '' Process an event and transition state

  case current_state
    STATE_IDLE:
      new_state := handle_idle(event)
    STATE_CONNECTING:
      new_state := handle_connecting(event)
    STATE_CONNECTED:
      new_state := handle_connected(event)
    STATE_CLOSING:
      new_state := handle_closing(event)
    STATE_ERROR:
      new_state := handle_error(event)
    OTHER:
      new_state := enter_error(ERR_INVALID_STATE)

  current_state := new_state

PUB get_state() : state
  state := current_state

PUB get_error() : code
  code := error_code

PRI handle_idle(event) : next_state
  case event
    EVT_CONNECT:
      retry_count := 0
      do_connect()
      next_state := STATE_CONNECTING
    OTHER:
      next_state := STATE_IDLE         ' Ignore other events

PRI handle_connecting(event) : next_state
  case event
    EVT_CONNECTED:
      next_state := STATE_CONNECTED
    EVT_TIMEOUT:
      retry_count++
      if retry_count < 3
        do_connect()
        next_state := STATE_CONNECTING
      else
        next_state := enter_error(ERR_TIMEOUT)
    EVT_ERROR:
      next_state := enter_error(ERR_CONNECT_FAILED)
    OTHER:
      next_state := STATE_CONNECTING

PRI handle_connected(event) : next_state
  case event
    EVT_SEND:
      do_send()
      next_state := STATE_CONNECTED
    EVT_RECEIVE:
      do_receive()
      next_state := STATE_CONNECTED
    EVT_CLOSE:
      do_close()
      next_state := STATE_CLOSING
    EVT_ERROR:
      next_state := enter_error(ERR_CONNECTION_LOST)
    OTHER:
      next_state := STATE_CONNECTED

PRI handle_closing(event) : next_state
  case event
    EVT_CONNECTED:                     ' Acknowledged close
      do_cleanup()
      next_state := STATE_IDLE
    EVT_TIMEOUT:
      do_cleanup()
      next_state := STATE_IDLE         ' Force close
    OTHER:
      next_state := STATE_CLOSING

PRI handle_error(event) : next_state
  case event
    EVT_CONNECT:                       ' Retry after error
      error_code := 0
      retry_count := 0
      do_connect()
      next_state := STATE_CONNECTING
    OTHER:
      next_state := STATE_ERROR        ' Stay in error

PRI enter_error(code) : state
  error_code := code
  do_cleanup()
  state := STATE_ERROR

PRI do_connect()
  ' Implementation: initiate connection

PRI do_send()
  ' Implementation: send data

PRI do_receive()
  ' Implementation: receive data

PRI do_close()
  ' Implementation: initiate close

PRI do_cleanup()
  ' Implementation: release resources

CON { error codes }

  ERR_NONE           = 0
  ERR_TIMEOUT        = -1
  ERR_CONNECT_FAILED = -2
  ERR_CONNECTION_LOST = -3
  ERR_INVALID_STATE  = -4
```

**Key Characteristics:**
- Explicit state enumeration
- Event-driven transitions
- Single point of state change (process_event)
- Error state for recovery
- Easy to add new states/events

### 8. Dual-COG Object (Spin2 API + PASM Background)

Provides a Spin2 API while running PASM code in a background COG for performance-critical operations.

```spin2
'' ===========================================================================
''  PWM Driver - Spin2 API with PASM background COG
'' ===========================================================================

CON { driver constants }

  NO_COG = -1

VAR { instance state }

  long cog_id
  long params[4]                       ' Parameter block for PASM COG

PUB start(pin, frequency) : ok
  '' Start PWM on specified pin at given frequency

  stop()                               ' Stop if already running

  ' Set up parameters for PASM COG
  params[0] := pin
  params[1] := clkfreq / frequency     ' Period in clock ticks
  params[2] := params[1] / 2           ' Default 50% duty
  params[3] := TRUE                    ' Running flag

  ' Start PASM driver
  cog_id := coginit(COGEXEC_NEW, @pwm_driver, @params)
  ok := (cog_id >= 0)

PUB stop()
  '' Stop the PWM driver

  if cog_id >= 0
    params[3] := FALSE                 ' Signal PASM to stop
    waitms(1)                          ' Allow graceful shutdown
    cogstop(cog_id)
    cog_id := NO_COG

PUB set_duty(percent)
  '' Set duty cycle (0-100%)

  percent := percent #> 0 <# 100
  params[2] := params[1] * percent / 100

PUB set_frequency(frequency)
  '' Change PWM frequency while running

  params[1] := clkfreq / frequency
  if params[2] > params[1]
    params[2] := params[1] / 2         ' Reset to 50% if duty exceeds period

PUB get_duty() : percent
  '' Get current duty cycle percentage

  if params[1] > 0
    percent := params[2] * 100 / params[1]
  else
    percent := 0

DAT { PASM PWM driver }

              org     0

pwm_driver
              ' Get parameters from hub
              mov     ptra, ptra              ' PTRA = @params
              rdlong  pin, ptra[0]            ' Pin number
              rdlong  period, ptra[1]         ' PWM period
              rdlong  duty, ptra[2]           ' Duty cycle

              ' Configure pin for output
              drvl    pin

              ' Get initial time
              getct   time

.loop
              ' Check if still running
              rdlong  running, ptra[3]
              tjz     running, #.stop

              ' Update parameters (can change while running)
              rdlong  period, ptra[1]
              rdlong  duty, ptra[2]

              ' High portion
              drvh    pin
              addct1  time, duty
              waitct1

              ' Low portion
              drvl    pin
              mov     temp, period
              sub     temp, duty
              addct1  time, temp
              waitct1

              jmp     #.loop

.stop
              drvl    pin                     ' Ensure pin low
              cogid   temp
              cogstop temp

              ' Variables
pin           res     1
period        res     1
duty          res     1
running       res     1
time          res     1
temp          res     1
```

**Key Characteristics:**
- Spin2 methods provide easy-to-use API
- PASM code handles timing-critical operations
- Parameter block for Spin2-PASM communication
- Can update parameters while running

### 9. PASM-Only Object

Contains only DAT section with PASM code, loaded and called by parent.

```spin2
'' ===========================================================================
''  Fast CRC Calculator - PASM-only for speed
'' ===========================================================================

DAT { PASM CRC calculator - called directly by parent }

              org     0

' Entry point: PTRA = pointer to parameter block
' param[0] = data pointer
' param[1] = data length
' param[2] = result pointer (output)

crc_calc
              mov     ptrb, ptra              ' Save param pointer

              rdlong  data_ptr, ptrb[0]       ' Get data pointer
              rdlong  data_len, ptrb[1]       ' Get length
              rdlong  result_ptr, ptrb[2]     ' Get result pointer

              mov     crc, #$FF               ' Initialize CRC

.byte_loop
              tjz     data_len, #.done        ' Exit if no more bytes

              rdbyte  byte_val, data_ptr      ' Read next byte
              add     data_ptr, #1
              sub     data_len, #1

              xor     crc, byte_val           ' XOR byte into CRC

              ' Process 8 bits
              rep     @.bit_end, #8
              shr     crc, #1         wc
        if_c  xor     crc, #$8C               ' CRC-8 polynomial
.bit_end

              jmp     #.byte_loop

.done
              wrlong  crc, result_ptr         ' Write result

              cogid   temp
              cogstop temp                    ' Stop this COG

' Variables
data_ptr      res     1
data_len      res     1
result_ptr    res     1
crc           res     1
byte_val      res     1
temp          res     1
```

**Parent object using PASM-only object:**

```spin2
OBJ
  crc_pasm : "fast_crc"

VAR
  long params[3]
  long result

PUB calculate_crc(data_ptr, length) : crc_value | cog
  params[0] := data_ptr
  params[1] := length
  params[2] := @result

  cog := coginit(COGEXEC_NEW, @crc_pasm.crc_calc, @params)
  if cog >= 0
    repeat while cogchk(cog)           ' Wait for completion
    crc_value := result
  else
    crc_value := -1                    ' Error
```

**Key Characteristics:**
- No Spin2 methods, only DAT/PASM
- Parent must use COGINIT to launch
- Communication via parameter block
- Maximum performance for compute-intensive tasks

## Data Sharing Patterns

### Pointer Passing

Pass data by reference for large data or when modification is needed.

```spin2
PUB process_buffer(buf_ptr, length) | i, sum
  '' Process buffer passed by pointer

  sum := 0
  repeat i from 0 to length - 1
    sum += long[buf_ptr][i]
  return sum

PUB caller()
  local_buffer[0] := 10
  local_buffer[1] := 20
  result := process_buffer(@local_buffer, 2)
```

### Shared DAT Singleton

Use DAT for data that must be shared across object instances.

```spin2
DAT
  shared_config   long  0              ' All instances share this

PUB set_config(value)
  shared_config := value               ' All instances see change

PUB get_config() : value
  value := shared_config
```

### Parameter Block Communication

For COG-to-COG communication, use a shared memory block.

```spin2
VAR
  long cmd_block[8]

PUB send_command(cmd, arg1, arg2)
  cmd_block[1] := arg1
  cmd_block[2] := arg2
  cmd_block[0] := cmd                  ' Write command last (signal)
  cogatn(1 << worker_cog)              ' Signal worker

' Worker reads:
' repeat
'   waitatn()
'   cmd := long[block_ptr][0]
'   arg1 := long[block_ptr][1]
```

### Lock-Protected Resources

Use locks when multiple COGs access shared data.

```spin2
VAR
  long data_lock
  long shared_data[100]

PUB init()
  data_lock := locknew()

PUB safe_read(index) : value
  repeat until locktry(data_lock)
  value := shared_data[index]
  lockrel(data_lock)

PUB safe_write(index, value)
  repeat until locktry(data_lock)
  shared_data[index] := value
  lockrel(data_lock)
```

## Anti-Patterns

### Missing Cleanup

```spin2
' WRONG: Resource leak
PUB start()
  cog := cogspin(...)

PUB stop()
  ' Forgot to stop COG!

' CORRECT: Always clean up
PUB stop()
  if cog >= 0
    cogstop(cog)
    cog := -1
  if lock >= 0
    lockret(lock)
    lock := -1
```

### Oversized Public Interface

```spin2
' WRONG: Too many public methods expose implementation
PUB init()
PUB setup_hardware()
PUB configure_registers()
PUB start_interrupts()
PUB internal_state()

' CORRECT: Minimal public interface
PUB start() : ok
  setup_hardware()
  configure_registers()
  start_interrupts()
  ok := TRUE

PRI setup_hardware()
PRI configure_registers()
PRI start_interrupts()
```

### VAR for Shared Data

```spin2
' WRONG: VAR is per-instance, not shared
VAR
  long shared_counter                  ' Each instance has own copy!

' CORRECT: DAT for shared data
DAT
  shared_counter  long  0              ' Single copy for all instances
```

### Missing Error Handling

```spin2
' WRONG: Ignores failures
PUB start()
  cogspin(NEWCOG, worker(), @stack)    ' What if no COG available?

' CORRECT: Handle errors
PUB start() : ok
  cog := cogspin(NEWCOG, worker(), @stack)
  if cog == -1
    ok := FALSE
  else
    ok := TRUE
```

### Uncontrolled State Access

```spin2
' WRONG: Anyone can corrupt state
VAR
  long state

PUB set_state(s)
  state := s                           ' No validation!

' CORRECT: Validate state transitions
PUB set_state(new_state) : ok
  case new_state
    STATE_IDLE, STATE_RUNNING, STATE_ERROR:
      state := new_state
      ok := TRUE
    OTHER:
      ok := FALSE
```

## Summary Tables

### Object Archetypes

| Archetype | Key Feature | Use Case |
|-----------|-------------|----------|
| Top-Level Application | `_clkfreq`, `main()` | Entry point |
| Driver Object | start/stop lifecycle | Hardware abstraction |
| Library Object | No state, pure functions | Utility functions |
| Singleton | DAT for shared state | System-wide resources |
| Configurable | Overridable constants | Compile-time variants |
| Buffered I/O | Circular buffer | Producer-consumer |
| State Machine | Explicit states/events | Protocol handling |
| Dual-COG | Spin2 API + PASM | Performance + usability |
| PASM-Only | DAT section only | Maximum performance |

### Section Purposes

| Section | Purpose | Instance Scope |
|---------|---------|----------------|
| CON | Constants, enums | N/A (compile-time) |
| VAR | Instance variables | Per instance |
| OBJ | Child objects | Per instance |
| PUB | Public methods | Per instance |
| PRI | Private methods | Per instance |
| DAT | Shared data, PASM | Shared (all instances) |

### Common Patterns

| Pattern | When to Use |
|---------|-------------|
| Pointer passing | Large data, modify in place |
| Shared DAT | Singleton state, lookup tables |
| Parameter block | COG communication |
| Lock protection | Multi-COG shared access |
| Constant override | Compile-time configuration |
| Circular buffer | Streaming data, I/O buffering |

## Related Documentation

- [Control-Flow-Usage-Guide.md](Control-Flow-Usage-Guide.md) - CASE for state machines
- [Multi-Cog-Usage-Guide.md](Multi-Cog-Usage-Guide.md) - COG management, locks
- [Error-Handling-Usage-Guide.md](Error-Handling-Usage-Guide.md) - ABORT patterns
- [Clock-Configuration-Usage-Guide.md](Clock-Configuration-Usage-Guide.md) - Top-level clock setup
- [Pin-Operations-Usage-Guide.md](Pin-Operations-Usage-Guide.md) - Driver hardware access
