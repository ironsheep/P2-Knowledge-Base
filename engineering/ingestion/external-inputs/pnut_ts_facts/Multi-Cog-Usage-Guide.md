# Multi-Cog Usage Guide

## Overview

The Propeller 2 has eight independent processor cores (COGs) that can run simultaneously. Spin2 provides primitives for:

- **COG Lifecycle** - Starting, stopping, and identifying COGs
- **Synchronization** - Locks for coordinating shared resource access
- **Signaling** - Attention mechanism for inter-COG notification
- **Communication** - SEND/RECV mailbox for data exchange

Each COG has its own registers and can execute either PASM2 assembly or Spin2 code independently.

## Basic Usage

### Starting a Spin2 Method in a New COG

```spin2
VAR
  long cog_id
  long stack[100]            ' Stack space for new COG

PUB start()
  cog_id := cogspin(NEWCOG, worker_method(), @stack)
  if cog_id == -1
    handle_no_cog_available()

PUB stop()
  if cog_id >= 0
    cogstop(cog_id)
    cog_id := -1

PRI worker_method()
  repeat
    do_work()
```

### Starting PASM Code in a New COG

```spin2
VAR
  long cog_id
  long parameters[4]

PUB start()
  parameters[0] := pin_number
  parameters[1] := baud_rate
  cog_id := coginit(COGEXEC_NEW, @pasm_driver, @parameters)

DAT
              org     0
pasm_driver   mov     ptra, ptra              ' PTRA points to parameters
              rdlong  pin, ptra[0]
              rdlong  baud, ptra[1]
              ' ... PASM code continues
```

## COG Lifecycle

### COGSPIN - Start Spin2 Method

```spin2
cog_id := COGSPIN(cog_number, method_call(), @stack)
```

**Parameters:**
- `cog_number` - COG ID (0-7) or `NEWCOG` for automatic allocation
- `method_call()` - Spin2 method to execute (with any parameters)
- `@stack` - Address of stack array for the COG

**Returns:** COG ID (0-7) if successful, -1 if no COG available

```spin2
VAR
  long worker_stack[200]
  long cog

PUB start_worker(param1, param2)
  ' Start method with parameters in next available COG
  cog := cogspin(NEWCOG, process_data(param1, param2), @worker_stack)

PUB start_specific_cog()
  ' Start in specific COG (COG 3)
  cog := cogspin(3, worker_task(), @worker_stack)

PRI process_data(a, b)
  ' This runs in the new COG
  repeat
    result := a + b
    ' ...
```

### COGINIT - Start PASM Code

```spin2
cog_id := COGINIT(mode, @pasm_code, @parameters)
```

**Parameters:**
- `mode` - Execution mode (see table below)
- `@pasm_code` - Address of PASM code to execute
- `@parameters` - Parameter block address (passed via PTRA register)

**Execution Modes:**

| Mode | Value | Description |
|------|-------|-------------|
| `COGEXEC` | %000000 | Execute in current COG (replaces Spin2) |
| `HUBEXEC` | %100000 | Execute from HUB in current COG |
| `COGEXEC_NEW` | %010000 | Start new COG, load code to COG RAM |
| `HUBEXEC_NEW` | %110000 | Start new COG, execute from HUB RAM |
| `COGEXEC_NEW_PAIR` | %010001 | Start pair of adjacent COGs |
| `HUBEXEC_NEW_PAIR` | %110001 | Start COG pair from HUB RAM |

```spin2
VAR
  long pasm_cog
  long params[3]

PUB start_pasm_driver(pin, freq)
  params[0] := pin
  params[1] := freq
  params[2] := @shared_buffer
  pasm_cog := coginit(COGEXEC_NEW, @driver_code, @params)

DAT
              org     0
driver_code
              mov     ptra, ptra        ' Preserve PTRA (parameter block address)
              rdlong  pin_num, ptra[0]  ' Read parameters
              rdlong  frequency, ptra[1]
              rdlong  buffer_ptr, ptra[2]
              ' ... driver implementation
```

### COGSTOP - Stop a COG

```spin2
COGSTOP(cog_id)
```

Stops the specified COG immediately. The COG becomes available for reuse.

```spin2
PUB stop_all_workers() | i
  repeat i from 1 to 7       ' Don't stop COG 0 (main program)
    cogstop(i)
```

### COGID - Get Current COG ID

```spin2
my_cog := COGID()
```

Returns the ID (0-7) of the COG executing this code.

```spin2
PUB identify()
  debug("Running on COG ", udec(cogid()))
```

### COGCHK - Check if COG is Running

```spin2
running := COGCHK(cog_id)
```

Returns non-zero if the specified COG is running, zero if stopped.

```spin2
PUB wait_for_cog_to_finish(cog)
  repeat while cogchk(cog)
    waitms(1)
```

## Task Management

### TASKSPIN - Cooperative Multitasking

TASKSPIN enables multiple tasks within a single COG, using cooperative multitasking.

```spin2
cog := TASKSPIN(task_id, method_call(), @stack)
```

Unlike COGSPIN which uses separate COGs, TASKSPIN shares one COG among multiple tasks that voluntarily yield control.

## Synchronization with Locks

The P2 provides 16 hardware locks (0-15) for coordinating access to shared resources between COGs.

### Lock Lifecycle

```spin2
VAR
  long lock_id

PUB init_shared_resource()
  lock_id := locknew()
  if lock_id == -1
    handle_no_locks()

PUB cleanup()
  lockret(lock_id)
```

### LOCKNEW - Allocate a Lock

```spin2
lock_id := LOCKNEW()
```

Returns lock ID (0-15) if available, -1 if all 16 locks are in use.

### LOCKRET - Return a Lock

```spin2
LOCKRET(lock_id)
```

Returns the lock to the pool for reuse. Any COG waiting on this lock will be unblocked.

### LOCKTRY - Try to Acquire Lock

```spin2
acquired := LOCKTRY(lock_id)
```

Attempts to acquire the lock:
- Returns non-zero (TRUE) if lock acquired
- Returns zero (FALSE) if lock held by another COG

**Non-blocking** - returns immediately whether successful or not.

```spin2
PUB access_shared_resource()
  repeat until locktry(lock_id)
    ' Optionally do other work while waiting
    waitms(1)

  ' Critical section - exclusive access
  modify_shared_data()

  lockrel(lock_id)
```

### LOCKREL - Release Lock

```spin2
LOCKREL(lock_id)
```

Releases the lock, allowing other COGs to acquire it.

### LOCKCHK - Check Lock Status

```spin2
owned := LOCKCHK(lock_id)
```

Returns non-zero if lock is currently owned, zero if available.

### Lock Usage Pattern

```spin2
CON
  NO_LOCK = -1

VAR
  long shared_counter
  long counter_lock

PUB init()
  counter_lock := locknew()
  shared_counter := 0

PUB increment_counter() | acquired
  ' Spin until lock acquired
  repeat until locktry(counter_lock)

  ' Critical section
  shared_counter++

  ' Release lock
  lockrel(counter_lock)

PUB get_counter() : value
  repeat until locktry(counter_lock)
  value := shared_counter
  lockrel(counter_lock)

PUB cleanup()
  if counter_lock <> NO_LOCK
    lockret(counter_lock)
    counter_lock := NO_LOCK
```

## Inter-COG Signaling

The attention (ATN) mechanism provides lightweight signaling between COGs without data transfer.

### COGATN - Send Attention Signal

```spin2
COGATN(cog_mask)
```

Sends attention signal to COGs specified by bitmask:
- Bit 0 = COG 0
- Bit 1 = COG 1
- ...
- Bit 7 = COG 7

```spin2
PUB signal_cog(cog_id)
  cogatn(1 << cog_id)        ' Signal specific COG

PUB signal_all_workers()
  cogatn(%11111110)          ' Signal COGs 1-7 (not COG 0)
```

### POLLATN - Poll for Attention

```spin2
pending := POLLATN()
```

Checks for pending attention signal:
- Returns non-zero if attention signal received
- Returns zero if no signal pending
- **Clears** the signal after reading

```spin2
PRI worker_loop()
  repeat
    if pollatn()
      handle_attention()
    else
      do_normal_work()
```

### WAITATN - Wait for Attention

```spin2
WAITATN()
```

Blocks until attention signal received. More power-efficient than polling.

```spin2
PRI wait_for_command()
  repeat
    waitatn()                ' Sleep until signaled
    process_command()
```

### ATN Signaling Pattern

```spin2
' Main COG (coordinator)
VAR
  long worker_cog
  long command
  long worker_stack[100]

PUB start()
  command := CMD_IDLE
  worker_cog := cogspin(NEWCOG, worker_task(), @worker_stack)

PUB send_command(cmd)
  command := cmd
  cogatn(1 << worker_cog)    ' Signal worker

' Worker COG
PRI worker_task()
  repeat
    waitatn()                ' Wait for signal
    case command
      CMD_START: do_start()
      CMD_STOP:  do_stop()
      CMD_EXIT:  return
```

## Mailbox Communication

SEND and RECV provide a simple mailbox mechanism for data exchange. These are typically used with a custom send method pointer.

### SEND - Send Data

```spin2
SEND(value)
SEND(byte1, byte2, byte3, ...)
```

Sends one or more values through the configured send mechanism.

### RECV - Receive Data

```spin2
value := RECV()
```

Receives a value from the configured receive mechanism.

### Mailbox Setup

```spin2
PUB setup_mailbox()
  SEND := @my_send_method
  RECV := @my_recv_method

PRI my_send_method(value)
  ' Custom send implementation
  shared_mailbox := value
  cogatn(worker_mask)

PRI my_recv_method() : value
  ' Custom receive implementation
  waitatn()
  value := shared_mailbox
```

## COG Parameter Block Pattern

When starting COGs, use parameter blocks to pass configuration data.

### Spin2 COG with Configuration

```spin2
VAR
  long config[4]
  long worker_stack[200]
  long worker_cog

PUB start_worker(pin, rate, buffer_ptr, buffer_size)
  ' Pack configuration into first elements of stack
  ' Worker method will read these on startup
  config[0] := pin
  config[1] := rate
  config[2] := buffer_ptr
  config[3] := buffer_size

  worker_cog := cogspin(NEWCOG, worker_init(@config), @worker_stack)

PRI worker_init(cfg_ptr) | pin, rate, buf, size
  ' Unpack configuration
  pin := long[cfg_ptr][0]
  rate := long[cfg_ptr][1]
  buf := long[cfg_ptr][2]
  size := long[cfg_ptr][3]

  ' Now run main loop with configuration
  worker_loop(pin, rate, buf, size)

PRI worker_loop(pin, rate, buf_ptr, buf_size)
  repeat
    ' ... use configuration
```

### PASM COG with Parameter Block

```spin2
VAR
  long pasm_params[4]
  long pasm_cog

PUB start_driver(tx_pin, rx_pin, baud)
  pasm_params[0] := tx_pin
  pasm_params[1] := rx_pin
  pasm_params[2] := baud
  pasm_params[3] := @rx_buffer

  pasm_cog := coginit(COGEXEC_NEW, @uart_driver, @pasm_params)

DAT
              org     0
uart_driver
              ' PTRA contains address of pasm_params
              rdlong  tx_pin, ptra[0]
              rdlong  rx_pin, ptra[1]
              rdlong  baud_rate, ptra[2]
              rdlong  buffer_addr, ptra[3]

              ' ... driver code using these parameters
```

### Command/Status Block Pattern

For ongoing communication between COGs:

```spin2
CON
  ' Command block offsets
  CMD_COMMAND  = 0
  CMD_PARAM1   = 1
  CMD_PARAM2   = 2
  CMD_STATUS   = 3
  CMD_RESULT   = 4

  ' Commands
  CMD_IDLE     = 0
  CMD_START    = 1
  CMD_STOP     = 2
  CMD_READ     = 3

  ' Status values
  STAT_IDLE    = 0
  STAT_BUSY    = 1
  STAT_DONE    = 2
  STAT_ERROR   = 3

VAR
  long cmd_block[5]
  long worker_stack[200]
  long worker_cog

PUB start()
  cmd_block[CMD_COMMAND] := CMD_IDLE
  cmd_block[CMD_STATUS] := STAT_IDLE
  worker_cog := cogspin(NEWCOG, worker_main(@cmd_block), @worker_stack)

PUB send_command(cmd, p1, p2) : result
  ' Wait for worker to be idle
  repeat while cmd_block[CMD_STATUS] == STAT_BUSY

  ' Set up command
  cmd_block[CMD_PARAM1] := p1
  cmd_block[CMD_PARAM2] := p2
  cmd_block[CMD_STATUS] := STAT_BUSY
  cmd_block[CMD_COMMAND] := cmd

  ' Signal worker
  cogatn(1 << worker_cog)

  ' Wait for completion
  repeat while cmd_block[CMD_STATUS] == STAT_BUSY

  result := cmd_block[CMD_RESULT]

PRI worker_main(block_ptr) | cmd
  repeat
    waitatn()

    cmd := long[block_ptr][CMD_COMMAND]
    case cmd
      CMD_START:
        do_start(long[block_ptr][CMD_PARAM1])
        long[block_ptr][CMD_STATUS] := STAT_DONE

      CMD_READ:
        long[block_ptr][CMD_RESULT] := do_read()
        long[block_ptr][CMD_STATUS] := STAT_DONE

      CMD_STOP:
        long[block_ptr][CMD_STATUS] := STAT_IDLE
        return
```

## Patterns

### Driver Object Pattern

```spin2
' serial_driver.spin2
CON
  NO_COG = -1

VAR
  long cog_id
  long rx_head, rx_tail
  long tx_head, tx_tail
  byte rx_buffer[256]
  byte tx_buffer[256]
  long stack[100]

PUB start(rx_pin, tx_pin, baud) : ok
  stop()                     ' Stop if already running

  ' Initialize state
  rx_head := rx_tail := 0
  tx_head := tx_tail := 0

  ' Start driver COG
  cog_id := cogspin(NEWCOG, driver_loop(rx_pin, tx_pin, baud), @stack)
  ok := (cog_id >= 0)

PUB stop()
  if cog_id >= 0
    cogstop(cog_id)
    cog_id := NO_COG

PUB tx(char)
  ' Add to TX buffer (with flow control)
  repeat while ((tx_tail + 1) & $FF) == tx_head
  tx_buffer[tx_tail] := char
  tx_tail := (tx_tail + 1) & $FF

PUB rx() : char
  repeat while rx_head == rx_tail
  char := rx_buffer[rx_head]
  rx_head := (rx_head + 1) & $FF

PRI driver_loop(rxp, txp, baud)
  ' Configure pins and run TX/RX loop
  repeat
    ' ... handle TX/RX
```

### Lock-Protected Shared Data

```spin2
VAR
  long data_lock
  long shared_data[100]

PUB init()
  data_lock := locknew()

PUB read_data(index) : value
  repeat until locktry(data_lock)
  value := shared_data[index]
  lockrel(data_lock)

PUB write_data(index, value)
  repeat until locktry(data_lock)
  shared_data[index] := value
  lockrel(data_lock)

PUB atomic_increment(index) : old_value
  repeat until locktry(data_lock)
  old_value := shared_data[index]
  shared_data[index] := old_value + 1
  lockrel(data_lock)
```

### Producer-Consumer with Circular Buffer

```spin2
CON
  BUFFER_SIZE = 256
  BUFFER_MASK = BUFFER_SIZE - 1

VAR
  long head, tail
  long buffer[BUFFER_SIZE]
  long producer_cog, consumer_cog
  long prod_stack[100], cons_stack[100]

PUB start()
  head := tail := 0
  producer_cog := cogspin(NEWCOG, producer(), @prod_stack)
  consumer_cog := cogspin(NEWCOG, consumer(), @cons_stack)

PRI producer() | item
  repeat
    item := generate_item()

    ' Wait for space in buffer
    repeat while ((head + 1) & BUFFER_MASK) == tail

    buffer[head] := item
    head := (head + 1) & BUFFER_MASK

PRI consumer() | item
  repeat
    ' Wait for item in buffer
    repeat while head == tail

    item := buffer[tail]
    tail := (tail + 1) & BUFFER_MASK

    process_item(item)
```

## Anti-Patterns

### Missing Stack Space

```spin2
' WRONG: Insufficient stack
VAR
  long tiny_stack[10]        ' Too small!

PUB start()
  cogspin(NEWCOG, complex_method(), @tiny_stack)  ' Stack overflow!

' CORRECT: Adequate stack
VAR
  long adequate_stack[200]   ' Size based on method needs

PUB start()
  cogspin(NEWCOG, complex_method(), @adequate_stack)
```

### Forgetting to Track COG ID

```spin2
' WRONG: Can't stop the COG later
PUB start()
  cogspin(NEWCOG, worker(), @stack)  ' COG ID discarded!

PUB stop()
  ' Can't stop - don't know which COG!

' CORRECT: Track COG ID
VAR
  long worker_cog

PUB start()
  worker_cog := cogspin(NEWCOG, worker(), @stack)

PUB stop()
  if worker_cog >= 0
    cogstop(worker_cog)
    worker_cog := -1
```

### Race Condition - Missing Lock

```spin2
' WRONG: Unprotected shared access
VAR
  long counter

PRI worker1()
  repeat
    counter++              ' Race condition!

PRI worker2()
  repeat
    counter++              ' Both COGs modify simultaneously

' CORRECT: Lock-protected access
VAR
  long counter
  long counter_lock

PUB init()
  counter_lock := locknew()

PRI worker1()
  repeat
    repeat until locktry(counter_lock)
    counter++
    lockrel(counter_lock)
```

### Deadlock - Lock Ordering

```spin2
' WRONG: Potential deadlock
PRI cog1()
  repeat until locktry(lock_a)
  repeat until locktry(lock_b)    ' COG2 may hold lock_b waiting for lock_a
  ' ...
  lockrel(lock_b)
  lockrel(lock_a)

PRI cog2()
  repeat until locktry(lock_b)
  repeat until locktry(lock_a)    ' Deadlock!
  ' ...

' CORRECT: Consistent lock ordering
PRI cog1()
  repeat until locktry(lock_a)    ' Always acquire A first
  repeat until locktry(lock_b)
  ' ...
  lockrel(lock_b)
  lockrel(lock_a)

PRI cog2()
  repeat until locktry(lock_a)    ' Same order as cog1
  repeat until locktry(lock_b)
  ' ...
```

### Not Returning Locks

```spin2
' WRONG: Lock leak
PUB start()
  my_lock := locknew()

PUB stop()
  ' Forgot to return lock - now unavailable!

' CORRECT: Always return locks
PUB stop()
  if my_lock >= 0
    lockret(my_lock)
    my_lock := -1
```

### Polling Instead of Waiting

```spin2
' WRONG: Wastes power busy-polling
PRI worker()
  repeat
    if pollatn()
      process_command()
    ' Constantly checking - inefficient

' BETTER: Use WAITATN when appropriate
PRI worker()
  repeat
    waitatn()              ' COG sleeps until signaled
    process_command()
```

## Summary Tables

### COG Lifecycle

| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `COGSPIN` | cog, method(), @stack | COG ID or -1 | Start Spin2 method |
| `COGINIT` | mode, @code, @params | COG ID | Start PASM code |
| `COGSTOP` | cog_id | - | Stop a COG |
| `COGID` | - | COG ID (0-7) | Get current COG |
| `COGCHK` | cog_id | 0 or non-zero | Check if running |

### Lock Functions

| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `LOCKNEW` | - | Lock ID (0-15) or -1 | Allocate lock |
| `LOCKRET` | lock_id | - | Return lock |
| `LOCKTRY` | lock_id | 0 or non-zero | Try to acquire |
| `LOCKREL` | lock_id | - | Release lock |
| `LOCKCHK` | lock_id | 0 or non-zero | Check if owned |

### Signaling Functions

| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `COGATN` | cog_mask | - | Send attention |
| `POLLATN` | - | 0 or non-zero | Poll for attention |
| `WAITATN` | - | - | Wait for attention |

### COGINIT Modes

| Mode | Binary | Description |
|------|--------|-------------|
| `COGEXEC` | %000000 | Current COG, COG RAM |
| `HUBEXEC` | %100000 | Current COG, HUB RAM |
| `COGEXEC_NEW` | %010000 | New COG, COG RAM |
| `HUBEXEC_NEW` | %110000 | New COG, HUB RAM |

## Related Documentation

- [Pin-Operations-Usage-Guide.md](Pin-Operations-Usage-Guide.md) - Pin control from multiple COGs
- [Timing-Operations-Usage-Guide.md](Timing-Operations-Usage-Guide.md) - Timing coordination between COGs
- [Spin2-Object-Patterns-Guide.md](Spin2-Object-Patterns-Guide.md) - Driver object architecture
