# Error Handling Usage Guide

## Overview

Spin2 provides an exception-like error handling mechanism using ABORT and the backslash trap operator. This allows methods to signal errors and callers to catch and handle them.

Key concepts:
- **ABORT** - Unwinds the call stack, optionally returning an error value
- **\ (backslash trap)** - Catches ABORT and allows execution to continue
- **Propagation** - Uncaught ABORTs propagate up the call chain until trapped or program terminates

## Basic Usage

### Signaling an Error with ABORT

```spin2
PUB read_sensor(channel) : value
  if channel < 0 OR channel > 7
    abort -1                     ' Signal error with code -1

  value := adc_read(channel)
```

### Catching Errors with Trap

```spin2
PUB safe_read(channel) : value
  value := \read_sensor(channel) ' Trap any ABORT
  if value == -1
    handle_error()
    value := 0
```

## ABORT Statement

### ABORT Without Value

```spin2
ABORT
```

Aborts execution and returns 0 to the caller (if trapped).

```spin2
PUB validate(data)
  if data == 0
    abort                        ' Return 0 to trapping caller
```

### ABORT With Value

```spin2
ABORT expression
```

Aborts execution and returns the expression value to the caller (if trapped).

```spin2
CON
  ERR_NONE     = 0
  ERR_TIMEOUT  = -1
  ERR_OVERFLOW = -2
  ERR_INVALID  = -3

PUB process_command(cmd) : result
  case cmd
    CMD_READ:
      result := do_read()
    CMD_WRITE:
      result := do_write()
    OTHER:
      abort ERR_INVALID          ' Return error code

PUB do_read() : data
  if NOT device_ready()
    abort ERR_TIMEOUT
  data := read_device()
  if data > MAX_VALUE
    abort ERR_OVERFLOW
```

## Trap Operator (\)

The backslash operator creates a "trap point" that catches ABORT statements.

### Instruction Context (Discard Result)

```spin2
\method_call()
```

Calls the method and catches any ABORT. The return value is discarded.

```spin2
PUB cleanup()
  \close_file()                  ' Don't care if it fails
  \release_resource()
  \stop_motor()
```

### Expression Context (Capture Result)

```spin2
result := \method_call()
```

Calls the method and catches any ABORT. Returns either:
- The method's normal return value (if no ABORT)
- The ABORT value (if ABORT occurred)
- 0 (if ABORT occurred without a value)

```spin2
PUB try_operation() : success, error_code
  error_code := \risky_operation()
  if error_code < 0
    success := FALSE
  else
    success := TRUE
```

### Trapping Object Method Calls

```spin2
result := \object.method()
result := \child_objects[i].method()
```

### Trapping Method Pointer Calls

```spin2
VAR
  long method_ptr

PUB call_with_trap() : result
  method_ptr := @some_method
  result := \method_ptr()
```

## Propagation Behavior

When ABORT executes:

1. The runtime searches up the call stack for a trap point
2. Stack frames are unwound (popped) until a trap is found
3. If trapped, execution continues at the caller with the abort value
4. If no trap exists, the program terminates

### Example: Propagation Through Call Chain

```spin2
PUB main()
  result := \level_1()           ' Trap point here
  debug("Result: ", sdec(result))

PRI level_1() : val
  val := level_2()               ' No trap - propagates through
  val += 10

PRI level_2() : val
  val := level_3()               ' No trap - propagates through
  val += 5

PRI level_3() : val
  abort -99                      ' ABORT propagates up to main()
  val := 1                       ' Never executed
```

Result: `main()` receives -99, the ABORT value.

### Nested Traps

Each trap only catches ABORTs from its own call:

```spin2
PUB outer() : result
  result := \inner()             ' Catches ABORT from inner() chain

PRI inner() : val
  val := \helper()               ' Catches ABORT from helper() only
  if val < 0
    abort val * 2                ' This ABORT goes to outer()
  val := other_work()

PRI helper() : val
  abort -1                       ' Caught by inner()'s trap
```

## RETURN vs ABORT

| Aspect | RETURN | ABORT |
|--------|--------|-------|
| Purpose | Normal completion | Error signaling |
| Stack behavior | Returns to immediate caller | Unwinds to trap point |
| Without trap | Returns normally | Program terminates |
| Return value | Method results | Error code |

```spin2
PUB example() : result
  if error_condition
    abort -1                     ' Unwind to trap point
  if done_early
    return 0                     ' Return to immediate caller
  result := compute()            ' Implicit return
```

## Patterns

### Error Code Pattern

```spin2
CON
  ' Error codes (negative = error, positive/zero = success)
  OK           =  0
  ERR_PARAM    = -1
  ERR_TIMEOUT  = -2
  ERR_BUSY     = -3
  ERR_NOTFOUND = -4

PUB operation(param) : result
  if param < 0
    abort ERR_PARAM
  if NOT resource_available()
    abort ERR_BUSY
  result := do_work(param)

PUB safe_operation(param) : result, error
  result := \operation(param)
  if result < 0
    error := result
    result := 0
  else
    error := OK
```

### Try-Finally Pattern

Spin2 doesn't have `finally`, but you can simulate cleanup:

```spin2
PUB with_resource() : result | resource, error
  resource := acquire_resource()

  error := \do_work_with(resource)

  release_resource(resource)     ' Always executes

  if error < 0
    abort error                  ' Re-throw if needed
  result := error
```

### Retry Pattern

```spin2
PUB retry_operation(max_attempts) : result | attempt, err
  repeat attempt from 1 to max_attempts
    err := \risky_operation()
    if err >= 0
      return err                 ' Success
    waitms(100)                  ' Delay before retry

  abort err                      ' All retries failed

PRI risky_operation() : result
  if random_failure()
    abort -1
  result := 42
```

### Graceful Degradation

```spin2
PUB read_with_fallback() : value
  value := \read_primary_sensor()
  if value < 0
    value := \read_backup_sensor()
    if value < 0
      value := DEFAULT_VALUE     ' Use safe default
```

### Resource Cleanup on Error

```spin2
PUB process_file(filename) : result | handle, err
  handle := open_file(filename)
  if handle < 0
    abort handle                 ' Can't open

  err := \process_contents(handle)

  close_file(handle)             ' Always close

  if err < 0
    abort err
  result := err

PRI process_contents(handle) : result
  ' May abort on error
  result := read_and_process(handle)
```

### Validation Chain

```spin2
PUB validate_all(data) : valid
  \validate_range(data)
  \validate_checksum(data)
  \validate_format(data)
  valid := TRUE                  ' All passed

PRI validate_range(data)
  if data.value < MIN OR data.value > MAX
    abort ERR_RANGE

PRI validate_checksum(data)
  if compute_checksum(data) <> data.checksum
    abort ERR_CHECKSUM

PRI validate_format(data)
  if data.header <> EXPECTED_HEADER
    abort ERR_FORMAT
```

### Error Logging

```spin2
PUB logged_operation() : result | err
  err := \actual_operation()
  if err < 0
    log_error(err)
  result := err

PRI log_error(code)
  debug("Error: ", sdec(code))
  error_count++
  last_error := code
```

## Anti-Patterns

### Uncaught ABORT

```spin2
' WRONG: ABORT terminates program if not trapped
PUB main()
  process()                      ' If this aborts, program dies

PRI process()
  if error
    abort -1                     ' Uncaught - program terminates!

' CORRECT: Always trap at top level
PUB main() | err
  err := \process()
  if err < 0
    handle_error(err)
```

### Ignoring Error Values

```spin2
' WRONG: Discarding error information
PUB bad_error_handling()
  \operation()                   ' Error code lost!
  continue_anyway()              ' May be in bad state

' CORRECT: Check error values
PUB good_error_handling() | err
  err := \operation()
  if err < 0
    handle_error(err)
    return
  continue_safely()
```

### Using ABORT for Normal Flow

```spin2
' WRONG: ABORT for non-error conditions
PUB find_item(target) : index | i
  repeat i from 0 to size-1
    if items[i] == target
      abort i                    ' Misusing ABORT for "found"!
  index := -1

' CORRECT: Use RETURN for normal flow
PUB find_item(target) : index | i
  repeat i from 0 to size-1
    if items[i] == target
      return i
  index := -1
```

### Resource Leak on ABORT

```spin2
' WRONG: Resource not released if ABORT occurs
PUB leaky_operation() | handle
  handle := acquire_resource()
  risky_work()                   ' If this aborts, handle leaks!
  release_resource(handle)

' CORRECT: Ensure cleanup
PUB safe_operation() | handle, err
  handle := acquire_resource()
  err := \risky_work()
  release_resource(handle)       ' Always release
  if err < 0
    abort err
```

### Deep Nesting Without Traps

```spin2
' PROBLEMATIC: Hard to know where errors come from
PUB level1()
  level2()

PRI level2()
  level3()

PRI level3()
  level4()

PRI level4()
  abort -1                       ' Where did this come from?

' BETTER: Trap at meaningful boundaries
PUB level1() | err
  err := \level2()
  if err < 0
    debug("Level2 failed: ", sdec(err))
```

### Mixing Error Codes and Valid Data

```spin2
' WRONG: -1 could be valid data
PUB read_value() : value
  if error
    abort -1
  value := sensor_read()         ' What if sensor returns -1?

' CORRECT: Use separate error indication
PUB read_value() : value, valid
  if error
    abort ERR_SENSOR
  value := sensor_read()
  valid := TRUE
```

## Summary Tables

### ABORT Variants

| Syntax | Returns | Use Case |
|--------|---------|----------|
| `ABORT` | 0 | Generic error, no details needed |
| `ABORT expr` | Expression value | Specific error code |

### Trap Contexts

| Syntax | Context | Result Handling |
|--------|---------|-----------------|
| `\method()` | Instruction | Result discarded |
| `x := \method()` | Expression | Result captured |

### Error Handling Strategy

| Scenario | Approach |
|----------|----------|
| Must not fail | Trap and provide default |
| Can retry | Trap in loop with attempts |
| Needs cleanup | Trap, cleanup, re-abort |
| Top-level | Always trap, log error |
| Library code | Document ABORT conditions |

## Related Documentation

- [Control-Flow-Usage-Guide.md](Control-Flow-Usage-Guide.md) - IF/CASE for error checking
- [Spin2-Object-Patterns-Guide.md](Spin2-Object-Patterns-Guide.md) - Error handling in objects
