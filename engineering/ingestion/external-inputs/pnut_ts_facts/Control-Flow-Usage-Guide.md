# Control Flow Usage Guide

## Overview

Spin2 provides three main control flow mechanisms:
- **Conditionals** - IF/IFNOT/ELSEIF/ELSEIFNOT/ELSE for branching
- **CASE statements** - CASE and CASE_FAST for multi-way selection
- **REPEAT loops** - Six forms for different iteration patterns

Control flow blocks use indentation-based scoping. A block ends when a line appears at the same or lower indentation level as the control statement.

## Basic Usage

### Simple Conditional

```spin2
PUB check_value(n) | result
  if n > 0
    result := 1
  elseif n < 0
    result := -1
  else
    result := 0
```

### Simple Loop

```spin2
PUB blink_led(pin, count) | i
  repeat count
    pinwrite(pin, 1)
    waitms(500)
    pinwrite(pin, 0)
    waitms(500)
```

### Case Selection

```spin2
PUB process_command(cmd)
  case cmd
    "S", "s":
      start_motor()
    "P", "p":
      stop_motor()
    "R":
      reverse_motor()
    OTHER:
      report_error()
```

## Conditionals

### IF Statement

```spin2
PUB if_demo(value)
  if value > 100
    process_large()
  elseif value > 50
    process_medium()
  elseif value > 0
    process_small()
  else
    process_zero_or_negative()
```

Conditions evaluate as:
- **TRUE**: Any non-zero value
- **FALSE**: Zero only

### IFNOT Statement

IFNOT inverts the condition test. The block executes when the condition is FALSE (zero).

```spin2
PUB ifnot_demo(sensor_value)
  ' Execute if sensor_value is zero
  ifnot sensor_value
    handle_no_signal()

  ' Equivalent to:
  if sensor_value == 0
    handle_no_signal()
```

### ELSEIFNOT

```spin2
PUB complex_check(a, b)
  if a > 0
    handle_positive_a()
  elseifnot b              ' Execute if b is zero
    handle_zero_b()
  else
    handle_other()
```

### Condition Expressions

Any expression that produces a value can be a condition:

```spin2
PUB condition_examples(flags, ptr)
  ' Direct value test
  if flags
    process()

  ' Comparison
  if flags & MASK == EXPECTED
    match()

  ' Method return value
  if check_status()
    ready()

  ' Pointer validity (non-zero means valid)
  if ptr
    use_pointer(ptr)
```

### Nesting Conditionals

```spin2
PUB nested_demo(x, y)
  if x > 0
    if y > 0
      quadrant_1()
    else
      quadrant_4()
  else
    if y > 0
      quadrant_2()
    else
      quadrant_3()
```

## CASE Statements

### Basic CASE

```spin2
PUB handle_key(key)
  case key
    " ":
      toggle_pause()
    "Q", "q":
      quit_program()
    "0".."9":
      process_digit(key - "0")
    OTHER:
      ignore_key()
```

### Multiple Values Per Match

Separate values with commas:

```spin2
PUB categorize(char) : category
  case char
    "A".."Z", "a".."z":
      category := LETTER
    "0".."9":
      category := DIGIT
    " ", 9, 10, 13:           ' Space, tab, newline, carriage return
      category := WHITESPACE
    OTHER:
      category := SYMBOL
```

### Range Matching

The `..` operator specifies inclusive ranges:

```spin2
PUB grade_score(score) : grade
  case score
    90..100:
      grade := "A"
    80..89:
      grade := "B"
    70..79:
      grade := "C"
    60..69:
      grade := "D"
    0..59:
      grade := "F"
    OTHER:
      grade := "?"           ' Invalid score
```

Ranges are inclusive on both ends. The range `90..100` matches 90, 91, 92, ... 100.

### CASE_FAST

CASE_FAST generates a jump table for faster dispatch with integer ranges:

```spin2
PUB fast_dispatch(cmd)
  case_fast cmd
    0:
      cmd_idle()
    1:
      cmd_start()
    2:
      cmd_stop()
    3:
      cmd_reset()
    OTHER:
      cmd_unknown()
```

**When to use CASE_FAST:**
- Command dispatch with sequential integer codes
- State machine transitions
- Menu selections with numeric choices

**Constraints:**
- All case values must be within 255 of each other
- Works best with dense integer ranges (0, 1, 2, 3...)
- Generates larger code for sparse values

**When to use regular CASE:**
- Character matching
- Sparse value sets
- Ranges spanning more than 255

### OTHER Clause

OTHER handles all unmatched values. It must be the last clause:

```spin2
PUB with_other(value)
  case value
    1, 2, 3:
      handle_low()
    4, 5, 6:
      handle_mid()
    OTHER:                   ' Must be last
      handle_everything_else()
```

If OTHER is omitted and no match occurs, execution continues after the CASE block with no action taken.

## REPEAT Loops

### REPEAT (Infinite)

```spin2
PUB main_loop()
  repeat
    read_sensors()
    update_outputs()
    check_commands()
```

Exit an infinite loop with QUIT or RETURN:

```spin2
PUB wait_for_event() : event
  repeat
    event := check_event()
    if event
      quit
    waitms(10)
```

### REPEAT count

Execute a block a specific number of times:

```spin2
PUB flash_warning(times)
  repeat times
    led_on()
    waitms(100)
    led_off()
    waitms(100)

PUB send_header()
  repeat 8
    send_byte($FF)
```

If count is zero, the block does not execute:

```spin2
PUB conditional_repeat(n)
  repeat n                   ' If n=0, skips entirely
    process()
```

### REPEAT var FROM start TO end

Iterate through a range of values:

```spin2
PUB sum_range(first, last) : total
  total := 0
  repeat i from first to last
    total += i

PUB init_array() | i
  repeat i from 0 to 99
    buffer[i] := 0
```

The loop variable takes each value from start to end, inclusive.

### REPEAT var FROM start TO end STEP increment

Control the increment between iterations:

```spin2
PUB count_down() | i
  repeat i from 10 to 1 step -1
    display(i)
  display_message("Liftoff!")

PUB every_other() | i
  repeat i from 0 to 100 step 2
    process_even(i)

PUB scan_backwards() | addr
  repeat addr from $7FFF to 0 step -16
    scan_block(addr)
```

STEP can be positive or negative. If omitted, STEP defaults to 1.

### REPEAT count WITH var

Shorthand for counting from 0 to count-1:

```spin2
PUB init_indices() | i
  repeat 10 with i           ' i = 0, 1, 2, ..., 9
    indices[i] := i

' Equivalent to:
PUB init_indices_long() | i
  repeat i from 0 to 9
    indices[i] := i
```

Useful for array operations:

```spin2
CON
  BUFFER_SIZE = 256

PUB clear_buffer() | i
  repeat BUFFER_SIZE with i
    buffer[i] := 0

PUB fill_pattern() | i
  repeat 64 with i
    pattern[i] := i * 4
```

### REPEAT WHILE condition

Test condition before each iteration:

```spin2
PUB read_until_zero() : count | value
  count := 0
  repeat while (value := read_byte()) <> 0
    process(value)
    count++

PUB drain_fifo()
  repeat while fifo_not_empty()
    discard(read_fifo())
```

If the condition is initially false, the block never executes.

### REPEAT UNTIL condition

Test condition before each iteration; loop while condition is FALSE:

```spin2
PUB wait_for_ready()
  repeat until device_ready()
    waitms(1)

PUB find_marker() : position | i
  i := 0
  repeat until buffer[i] == MARKER OR i >= BUFFER_SIZE
    i++
  position := i
```

### Post-Condition WHILE/UNTIL

Place WHILE or UNTIL after the block to test after each iteration:

```spin2
PUB get_valid_input() : value
  repeat
    value := read_input()
  while value < 0 OR value > 100     ' Re-prompt if invalid

PUB read_packet() | byte_val
  repeat
    byte_val := receive()
    store(byte_val)
  until byte_val == END_MARKER
```

The block always executes at least once with post-condition loops.

## NEXT and QUIT

### NEXT - Continue to Next Iteration

```spin2
PUB process_valid_only() | i, value
  repeat i from 0 to 99
    value := data[i]
    if value < 0
      next                   ' Skip negative values
    process(value)
```

NEXT jumps to the next iteration, re-evaluating the loop condition.

### QUIT - Exit the Loop

```spin2
PUB find_first(target) : index | i
  index := -1                ' Not found
  repeat i from 0 to 99
    if data[i] == target
      index := i
      quit                   ' Found it, exit loop
```

QUIT exits the innermost enclosing REPEAT block.

### NEXT and QUIT with Nested Loops

NEXT and QUIT affect only the innermost loop:

```spin2
PUB search_matrix(target) : row, col | i, j
  row := -1
  col := -1
  repeat i from 0 to 9
    repeat j from 0 to 9
      if matrix[i][j] == target
        row := i
        col := j
        quit               ' Exits inner loop only
    if row >= 0
      quit                 ' Must quit outer loop separately
```

## Patterns

### State Machine

```spin2
CON
  STATE_IDLE    = 0
  STATE_RUNNING = 1
  STATE_PAUSED  = 2
  STATE_ERROR   = 3

VAR
  long state

PUB run_state_machine()
  repeat
    case_fast state
      STATE_IDLE:
        if start_requested()
          state := STATE_RUNNING
      STATE_RUNNING:
        do_work()
        if pause_requested()
          state := STATE_PAUSED
        if error_detected()
          state := STATE_ERROR
      STATE_PAUSED:
        if resume_requested()
          state := STATE_RUNNING
      STATE_ERROR:
        handle_error()
        state := STATE_IDLE
```

### Menu Dispatch

```spin2
PUB handle_menu(selection)
  case selection
    1:
      show_status()
    2:
      configure_settings()
    3:
      run_diagnostics()
    4:
      show_help()
    0:
      quit_application()
    OTHER:
      show_message("Invalid selection")
```

### Early Exit Pattern

```spin2
PUB validate_data(ptr, size) : valid | i
  valid := TRUE
  repeat i from 0 to size - 1
    if byte[ptr][i] == 0
      valid := FALSE
      quit
    if byte[ptr][i] > 127
      valid := FALSE
      quit
```

### Timeout Pattern

```spin2
PUB wait_with_timeout(ms) : success | deadline
  deadline := getms() + ms
  repeat
    if condition_met()
      success := TRUE
      quit
    if getms() >= deadline
      success := FALSE
      quit
    waitms(1)
```

### Retry Pattern

```spin2
PUB send_with_retry(data, max_attempts) : success | attempts
  success := FALSE
  repeat max_attempts with attempts
    if try_send(data)
      success := TRUE
      quit
    waitms(100)              ' Delay between retries
```

### Array Search

```spin2
PUB find_value(array_ptr, size, target) : index | i
  index := -1
  repeat size with i
    if long[array_ptr][i] == target
      index := i
      quit
```

### Nested Loop with Early Exit

```spin2
PUB find_in_2d(rows, cols, target) : found_row, found_col | r, c, found
  found_row := -1
  found_col := -1
  found := FALSE

  repeat rows with r
    repeat cols with c
      if grid[r * cols + c] == target
        found_row := r
        found_col := c
        found := TRUE
        quit
    if found
      quit
```

## Anti-Patterns

### Missing OTHER in CASE

```spin2
' PROBLEMATIC: No handling for unexpected values
PUB handle_state(state)
  case state
    0: idle()
    1: running()
    2: stopped()
  ' What if state is 3? Silent failure!

' BETTER: Always handle unexpected cases
PUB handle_state_safe(state)
  case state
    0: idle()
    1: running()
    2: stopped()
    OTHER:
      log_error("Unknown state")
      state := 0             ' Reset to known state
```

### Deeply Nested Conditionals

```spin2
' PROBLEMATIC: Hard to read and maintain
PUB process(a, b, c)
  if a > 0
    if b > 0
      if c > 0
        do_something()
      else
        do_other()
    else
      if c > 0
        do_third()
      else
        do_fourth()
  else
    ' ... more nesting

' BETTER: Use early returns or CASE
PUB process_flat(a, b, c)
  if a <= 0
    handle_non_positive_a()
    return

  if b <= 0
    handle_non_positive_b()
    return

  if c > 0
    do_something()
  else
    do_other()
```

### Infinite Loop Without Exit

```spin2
' PROBLEMATIC: No way to exit
PUB bad_loop()
  repeat
    process()
    ' No QUIT, no condition, no RETURN

' BETTER: Provide exit condition
PUB good_loop()
  repeat
    process()
    if should_stop()
      quit
```

### Modifying Loop Variable in FROM..TO

```spin2
' PROBLEMATIC: Undefined behavior
PUB bad_modify() | i
  repeat i from 0 to 10
    i += 2                   ' Don't do this!
    process(i)

' BETTER: Use WHILE for complex iteration
PUB good_modify() | i
  i := 0
  repeat while i <= 10
    process(i)
    i += 3
```

### Using CASE_FAST with Sparse Values

```spin2
' PROBLEMATIC: Inefficient - generates large jump table
PUB bad_case_fast(code)
  case_fast code
    1: handle_1()
    100: handle_100()
    1000: handle_1000()      ' Error: range > 255

' BETTER: Use regular CASE for sparse values
PUB good_sparse(code)
  case code
    1: handle_1()
    100: handle_100()
    1000: handle_1000()
```

### Forgetting Post-Condition Executes Once

```spin2
' PROBLEMATIC: May process invalid data
PUB risky_post_check() | value
  repeat
    value := read_input()
    process(value)           ' Processes even if invalid!
  until value == VALID

' BETTER: Check before processing
PUB safe_post_check() | value
  repeat
    value := read_input()
    if value == VALID
      process(value)
  until value == VALID

' OR use pre-condition
PUB safe_pre_check() | value
  repeat
    value := read_input()
  until value == VALID
  process(value)
```

## Summary Tables

### Conditional Statements

| Statement | Executes When |
|-----------|---------------|
| `IF cond` | cond is non-zero (TRUE) |
| `IFNOT cond` | cond is zero (FALSE) |
| `ELSEIF cond` | Previous conditions FALSE, this TRUE |
| `ELSEIFNOT cond` | Previous conditions FALSE, this FALSE |
| `ELSE` | All previous conditions FALSE |

### CASE Comparison

| Feature | CASE | CASE_FAST |
|---------|------|-----------|
| Value matching | Yes | Yes |
| Range matching | Yes | Yes |
| Character matching | Yes | Yes |
| Sparse values | Efficient | Inefficient |
| Dense integers | Good | Optimal |
| Max value span | Unlimited | 255 |
| Jump table | No | Yes |

### REPEAT Forms

| Form | Description | Loop Variable |
|------|-------------|---------------|
| `REPEAT` | Infinite loop | None |
| `REPEAT n` | Execute n times | None |
| `REPEAT var FROM a TO b` | Iterate a to b | var = a, a+1, ..., b |
| `REPEAT var FROM a TO b STEP s` | Iterate with step | var = a, a+s, a+2s, ... |
| `REPEAT n WITH var` | Count with index | var = 0, 1, ..., n-1 |
| `REPEAT WHILE cond` | Pre-test loop | None |
| `REPEAT UNTIL cond` | Pre-test (inverted) | None |
| `REPEAT ... WHILE cond` | Post-test loop | None |
| `REPEAT ... UNTIL cond` | Post-test (inverted) | None |

### Loop Control

| Statement | Effect |
|-----------|--------|
| `NEXT` | Skip to next iteration |
| `QUIT` | Exit innermost loop |
| `RETURN` | Exit method (and loop) |

## Related Documentation

- [Operators-Usage-Guide.md](Operators-Usage-Guide.md) - Comparison and logical operators in conditions
- [Error-Handling-Usage-Guide.md](Error-Handling-Usage-Guide.md) - ABORT as alternative exit mechanism
