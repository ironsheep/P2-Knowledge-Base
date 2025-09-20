# Spin2 Code Generation Patterns
*Generated from comprehensive YAML analysis*

## Core Language Patterns

### 1. Program Structure Pattern
```spin2
CON
  ' Configuration constants
  _CLKFREQ = 200_000_000
  
VAR
  ' Instance variables
  LONG cog
  
OBJ
  ' Child objects
  serial : "uart"
  
DAT
  ' Shared data and PASM2 code
  
PUB main()
  ' Entry point
  
PRI helper()
  ' Private methods
```

### 2. Object Lifecycle Pattern
```spin2
VAR
  LONG cog
  LONG stack[32]

PUB start(params) : success
  stop()
  ' Initialize
  cog := COGNEW(worker(), @stack) + 1
  success := cog > 0

PUB stop()
  IF cog
    COGSTOP(cog - 1)
    cog := 0

PRI worker()
  REPEAT
    ' Main loop
```

### 3. Pin I/O Patterns

#### Basic Digital I/O
```spin2
' Output
PINHIGH(pin)
PINLOW(pin)
PINTOGGLE(pin)

' Input
state := PINREAD(pin)
PINWAIT(pin, state, timeout)
```

#### Pin Group Operations
```spin2
CON
  LEDS = 56 ADDPINS 7  ' Pins 56-63

PUB flash_leds()
  PINHIGH(LEDS)
  WAITMS(100)
  PINLOW(LEDS)
```

### 4. Timing Patterns

#### Simple Delays
```spin2
WAITMS(1000)      ' Wait 1 second
WAITUS(100)       ' Wait 100 microseconds
```

#### Precise Timing
```spin2
VAR
  LONG start_time

PUB measure_event() : elapsed
  start_time := GETCT()
  ' Do something
  elapsed := GETCT() - start_time
```

#### Periodic Events
```spin2
PUB blink_1hz()
  REPEAT
    PINTOGGLE(LED)
    WAITCNT(GETCT() + CLKFREQ/2)
```

### 5. Memory Operation Patterns

#### Block Operations
```spin2
' Copy data
BYTEMOVE(@dest, @source, count)
WORDMOVE(@dest, @source, count)
LONGMOVE(@dest, @source, count)

' Fill memory
BYTEFILL(@buffer, value, count)
LONGFILL(@array, 0, 100)
```

### 6. COG Communication Patterns

#### Mailbox Pattern
```spin2
DAT
  command   LONG  0
  param1    LONG  0
  param2    LONG  0
  result    LONG  0

PUB send_command(cmd, p1, p2) : res
  param1 := p1
  param2 := p2
  command := cmd        ' Write command last
  REPEAT WHILE command  ' Wait for completion
  res := result
```

#### Shared Buffer Pattern
```spin2
DAT
  buffer    BYTE  0[256]
  head      LONG  0
  tail      LONG  0

PUB write_byte(b)
  buffer[head] := b
  head := (head + 1) & $FF

PUB read_byte() : b
  IF head <> tail
    b := buffer[tail]
    tail := (tail + 1) & $FF
```

### 7. Control Flow Patterns

#### State Machine
```spin2
CON
  #0, IDLE, INIT, RUNNING, ERROR

VAR
  BYTE state

PUB run()
  REPEAT
    CASE state
      IDLE:    handle_idle()
      INIT:    handle_init()
      RUNNING: handle_running()
      ERROR:   handle_error()
```

#### Event Loop
```spin2
PUB event_loop()
  REPEAT
    IF check_serial()
      handle_serial()
    IF check_pins()
      handle_pins()
    IF check_timer()
      handle_timer()
```

### 8. Math Operation Patterns

#### Clamping Values
```spin2
' Clamp x between min and max
x := min #> x <# max

' Ensure positive
x := x #> 0
```

#### CORDIC Operations
```spin2
' Rotate point
x, y := ROTXY(x, y, angle)

' Get polar coordinates
r, theta := XYPOL(x, y)
```

### 9. String Handling Patterns
```spin2
PUB print_string(str_ptr)
  REPEAT WHILE BYTE[str_ptr]
    send_char(BYTE[str_ptr++])

PUB copy_string(dest, source)
  BYTEMOVE(dest, source, STRSIZE(source) + 1)
```

### 10. Inline PASM2 Pattern
```spin2
PUB fast_operation(value) : result | tmp
  ORG
    MOV   tmp, value
    SHL   tmp, #2     ' Multiply by 4
    ADD   tmp, #1     ' Add 1
    MOV   result, tmp
  END
```

## Pattern Selection Guidelines

### When to Use Each Pattern

1. **Use Methods** for:
   - High-level logic
   - Complex control flow
   - String manipulation
   - User interface code

2. **Use Inline PASM2** for:
   - Timing-critical sections
   - Bit manipulation
   - Direct hardware control
   - Performance optimization

3. **Use DAT PASM2** for:
   - COG drivers
   - Real-time control
   - Parallel processing
   - Hardware interfaces

### Memory Allocation Strategy

- **CON**: Configuration, pin definitions, constants
- **VAR**: Instance state, buffers, working variables
- **OBJ**: Modular components, drivers, libraries
- **DAT**: Shared data, PASM2 code, lookup tables

### Performance Patterns

1. **Fast Pin Access**: Use PASM2 for <1µs timing
2. **Bulk Data**: Use LONGMOVE for 4x speed over BYTEMOVE
3. **Shared Resources**: Use DAT to avoid duplication
4. **Parallel Processing**: Distribute work across COGs

## Code Generation Rules

### Variable Naming
- Constants: UPPER_CASE
- Variables: lower_case or camelCase
- Methods: lower_case or snake_case
- Labels: .local_label

### Indentation
- 2 spaces per level
- Align operators vertically when listing multiple

### Comments
- High-level: explain why
- Low-level: explain how
- PASM2: document register usage

## Common Pitfalls to Avoid

1. **VAR in COG code** - COGs can't access VAR, use DAT
2. **Forgetting ORG 0** - PASM2 code must start with ORG
3. **Pin number confusion** - P2 has pins 0-63, not 0-31
4. **Stack size** - Allocate enough stack for COGNEW
5. **Mailbox ordering** - Write command last, clear when done

## Next Steps for Pattern Development

1. Build comprehensive example library
2. Create domain-specific templates (UART, SPI, I2C, etc.)
3. Develop performance benchmarks for patterns
4. Document anti-patterns and alternatives
5. Create pattern selection decision tree