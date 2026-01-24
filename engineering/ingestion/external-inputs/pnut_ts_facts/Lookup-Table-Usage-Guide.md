# Lookup Table Usage Guide

## Overview

Spin2 provides four lookup functions for table-driven programming:

- **LOOKUP / LOOKUPZ** - Given an index, return the value at that position
- **LOOKDOWN / LOOKDOWNZ** - Given a value, return the index where it's found

The "Z" suffix indicates zero-based indexing; without it, indexing is one-based.

These functions support both discrete value lists and ranges, making them useful for:
- Enum-to-value conversion
- Value validation
- Character classification
- State mapping

## Basic Usage

### LOOKUP - Index to Value (One-Based)

```spin2
PUB get_day_name(day_num) : name_ptr
  '' Return pointer to day name (1=Sunday, 7=Saturday)

  name_ptr := lookup(day_num : @"Sunday", @"Monday", @"Tuesday",
                               @"Wednesday", @"Thursday", @"Friday",
                               @"Saturday")
  if name_ptr == 0
    name_ptr := @"Invalid"
```

### LOOKUPZ - Index to Value (Zero-Based)

```spin2
PUB hex_digit(value) : char
  '' Convert 0-15 to hex character

  char := lookupz(value : "0", "1", "2", "3", "4", "5", "6", "7",
                          "8", "9", "A", "B", "C", "D", "E", "F")
```

### LOOKDOWN - Value to Index (One-Based)

```spin2
PUB is_vowel(char) : result
  '' Check if character is a vowel (returns 1-5 or 0 if not)

  result := lookdown(char : "A", "E", "I", "O", "U",
                            "a", "e", "i", "o", "u")
```

### LOOKDOWNZ - Value to Index (Zero-Based)

```spin2
PUB char_to_digit(char) : digit
  '' Convert '0'-'9' to 0-9, returns -1 if invalid

  digit := lookdownz(char : "0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
  if digit < 0                         ' Not found returns 0, but 0 is valid!
    digit := -1
```

## Syntax

### LOOKUP / LOOKUPZ

```spin2
value := LOOKUP(index : item1, item2, ..., itemN)
value := LOOKUPZ(index : item1, item2, ..., itemN)
```

- **index** - Expression that selects which item to return
- **items** - Comma-separated list of values or ranges
- **Returns** - The item at the index position, or 0 if index out of range

### LOOKDOWN / LOOKDOWNZ

```spin2
index := LOOKDOWN(target : item1, item2, ..., itemN)
index := LOOKDOWNZ(target : item1, item2, ..., itemN)
```

- **target** - Value to search for in the list
- **items** - Comma-separated list of values or ranges
- **Returns** - The index where target was found, or 0 if not found

### Using Ranges

Both LOOKUP and LOOKDOWN support ranges with the `..` operator:

```spin2
PUB classify_char(char) : category
  '' Classify character into categories

  if lookdown(char : "0".."9")
    category := CAT_DIGIT
  elseif lookdown(char : "A".."Z")
    category := CAT_UPPER
  elseif lookdown(char : "a".."z")
    category := CAT_LOWER
  else
    category := CAT_OTHER
```

Ranges expand to include all values between start and end:
- `"A".."Z"` expands to "A", "B", "C", ... "Z" (26 values)
- `0..9` expands to 0, 1, 2, ... 9 (10 values)
- `100..105` expands to 100, 101, 102, 103, 104, 105 (6 values)

## Index Base Comparison

| Function | Index Base | First Item | Last Item (N items) |
|----------|------------|------------|---------------------|
| LOOKUP | 1-based | Index 1 | Index N |
| LOOKUPZ | 0-based | Index 0 | Index N-1 |
| LOOKDOWN | 1-based | Returns 1 | Returns N |
| LOOKDOWNZ | 0-based | Returns 0 | Returns N-1 |

```spin2
CON
  ITEMS = 3

DAT
  values    long  10, 20, 30

PUB demo()
  ' LOOKUP (1-based)
  lookup(1 : 10, 20, 30)          ' Returns 10
  lookup(2 : 10, 20, 30)          ' Returns 20
  lookup(3 : 10, 20, 30)          ' Returns 30
  lookup(0 : 10, 20, 30)          ' Returns 0 (out of range)
  lookup(4 : 10, 20, 30)          ' Returns 0 (out of range)

  ' LOOKUPZ (0-based)
  lookupz(0 : 10, 20, 30)         ' Returns 10
  lookupz(1 : 10, 20, 30)         ' Returns 20
  lookupz(2 : 10, 20, 30)         ' Returns 30
  lookupz(3 : 10, 20, 30)         ' Returns 0 (out of range)

  ' LOOKDOWN (1-based)
  lookdown(10 : 10, 20, 30)       ' Returns 1
  lookdown(20 : 10, 20, 30)       ' Returns 2
  lookdown(30 : 10, 20, 30)       ' Returns 3
  lookdown(40 : 10, 20, 30)       ' Returns 0 (not found)

  ' LOOKDOWNZ (0-based)
  lookdownz(10 : 10, 20, 30)      ' Returns 0
  lookdownz(20 : 10, 20, 30)      ' Returns 1
  lookdownz(30 : 10, 20, 30)      ' Returns 2
  lookdownz(40 : 10, 20, 30)      ' Returns 0 (not found - same as first index!)
```

## Patterns

### Enum to String Conversion

```spin2
CON { error codes }
  ERR_NONE     = 0
  ERR_TIMEOUT  = 1
  ERR_OVERFLOW = 2
  ERR_INVALID  = 3
  ERR_BUSY     = 4

PUB error_name(code) : name_ptr
  '' Convert error code to human-readable name

  name_ptr := lookup(code + 1 : @"None", @"Timeout", @"Overflow",
                                @"Invalid", @"Busy")
  if name_ptr == 0
    name_ptr := @"Unknown"
```

### Value Validation

```spin2
CON { valid pin groups }
  PINS_P0_P15   = 0
  PINS_P16_P31  = 1
  PINS_P32_P47  = 2

PUB validate_pin_group(group) : valid
  '' Check if pin group is valid

  valid := lookdown(group : PINS_P0_P15, PINS_P16_P31, PINS_P32_P47) <> 0
```

### Range Validation

```spin2
CON { voltage settings }
  PWR_7p4V  = 74
  PWR_11p1V = 111
  PWR_12p0V = 120
  PWR_14p8V = 148
  PWR_24p0V = 240

PUB validate_voltage(voltage) : valid
  '' Check if voltage is in valid range

  valid := lookdown(voltage : PWR_7p4V..PWR_24p0V) <> 0
```

### Character Classification

```spin2
PUB is_alphanumeric(char) : result
  '' Check if character is letter or digit

  result := lookdown(char : "0".."9", "A".."Z", "a".."z") <> 0

PUB is_whitespace(char) : result
  '' Check if character is whitespace

  result := lookdown(char : " ", 9, 10, 13) <> 0    ' space, tab, LF, CR

PUB is_operator(char) : result
  '' Check if character is an operator

  result := lookdown(char : "!", "#", "&", "(", ")", "*", "+", ",",
                            "-", ".", "/", ":", "<", "=", ">", "?",
                            "@", "[", "\", "]", "^", "|", "~") <> 0
```

### Hex Conversion

```spin2
PUB hex_to_value(char) : value
  '' Convert hex character to value (0-15), returns -1 if invalid

  value := lookdownz(char : "0".."9")
  if value > 0 OR char == "0"
    return value

  value := lookdownz(char : "A".."F")
  if value > 0 OR char == "A"
    return value + 10

  value := lookdownz(char : "a".."f")
  if value > 0 OR char == "a"
    return value + 10

  return -1

PUB value_to_hex(value) : char
  '' Convert value (0-15) to hex character

  char := lookupz(value & $F : "0".."9", "A".."F")
```

### State Machine Dispatch

```spin2
CON { states }
  STATE_IDLE    = 0
  STATE_RUNNING = 1
  STATE_PAUSED  = 2
  STATE_ERROR   = 3

VAR
  long current_state
  long state_handlers[4]

PUB init()
  '' Initialize state handler table

  state_handlers[STATE_IDLE] := @handle_idle
  state_handlers[STATE_RUNNING] := @handle_running
  state_handlers[STATE_PAUSED] := @handle_paused
  state_handlers[STATE_ERROR] := @handle_error

PUB process_event(event) | handler
  '' Dispatch to appropriate state handler

  if lookdown(current_state : STATE_IDLE..STATE_ERROR)
    handler := state_handlers[current_state]
    handler(event)
```

### Comma-Formatted Numbers

```spin2
PUB print_with_commas(value)
  '' Print number with thousands separators

  repeat
    if flag ||= (digit := value / place // 10) or place == 1
      send("0" + digit)
      if lookdown(place : 1_000_000_000, 1_000_000, 1_000)
        send(",")
  while place /= 10
```

### Configuration Lookup

```spin2
CON { motor types }
  MOTOR_6_5_INCH = 0
  MOTOR_DOCO_4K  = 1

PUB get_motor_offset(motor_type, voltage_index) : offset
  '' Look up motor timing offset based on type and voltage

  case motor_type
    MOTOR_6_5_INCH:
      offset := lookup(voltage_index : 33, 33, 39, 40, 36, 37, 45)
    MOTOR_DOCO_4K:
      offset := lookup(voltage_index : 52, 53, 53, 53, 54, 54, 53)
    OTHER:
      offset := 0
```

## LOOKUP vs CASE vs Array

Choose the right approach based on your needs:

### Use LOOKUP When:
- Index-to-value mapping with small, fixed list
- Values are compile-time constants
- Need inline expression (no separate data structure)

```spin2
' Good for LOOKUP - simple index to value
pin := lookup(channel : 16, 17, 18, 19)
```

### Use CASE When:
- Complex logic per case
- Need to execute code, not just return value
- Non-sequential indices

```spin2
' Better as CASE - needs code execution
case command
  CMD_START: do_start()
  CMD_STOP:  do_stop()
  CMD_RESET: do_reset()
```

### Use Array When:
- Large number of values
- Values change at runtime
- Need random access by computed index

```spin2
' Better as array - many values, runtime modification
DAT
  sin_table   long  0, 174, 348, 523, ...   ' 256 entries

PUB get_sin(angle) : value
  value := sin_table[angle & $FF]
```

### Comparison Table

| Aspect | LOOKUP | CASE | Array |
|--------|--------|------|-------|
| Max practical size | ~20 items | ~20 cases | Unlimited |
| Runtime modifiable | No | No | Yes |
| Code execution | No | Yes | No |
| Memory | Inline | Inline | DAT/VAR |
| Index type | Sequential | Any | Sequential |

## Anti-Patterns

### Wrong Index Base

```spin2
' WRONG: Using 0 with one-based LOOKUP
pin_groups[0] := PINS_P0_P15
index := 0
pin := lookup(index : PINS_P0_P15, PINS_P16_P31)   ' Returns 0 (out of range!)

' CORRECT: Use LOOKUPZ for zero-based
pin := lookupz(index : PINS_P0_P15, PINS_P16_P31)  ' Returns PINS_P0_P15
```

### Ambiguous Zero Return

```spin2
' WRONG: Can't distinguish "not found" from "found at index 0"
index := lookdownz(value : 0, 1, 2, 3)
if index == 0
  ' Is this "found 0 at index 0" or "not found"?

' CORRECT: Check against expected range or use LOOKDOWN
if lookdown(value : 0, 1, 2, 3)       ' Returns 1-4, or 0 if not found
  found := TRUE

' Or validate the result
index := lookdownz(value : 0, 1, 2, 3)
if index >= 0 AND index <= 3 AND lookupz(index : 0, 1, 2, 3) == value
  found := TRUE
```

### Missing Range Check

```spin2
' WRONG: Assumes LOOKUP always returns valid value
day_name := lookup(day_num : @"Sun", @"Mon", @"Tue", @"Wed",
                             @"Thu", @"Fri", @"Sat")
print_string(day_name)                ' Crashes if day_num out of range (returns 0)

' CORRECT: Check return value
day_name := lookup(day_num : @"Sun", @"Mon", @"Tue", @"Wed",
                             @"Thu", @"Fri", @"Sat")
if day_name == 0
  day_name := @"Invalid"
print_string(day_name)
```

### Inefficient Large Tables

```spin2
' WRONG: LOOKUP with many items is inefficient
value := lookup(index : 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                        10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                        20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                        ...)  ' Many more values

' CORRECT: Use array for large tables
DAT
  values    long  0, 1, 2, 3, 4, 5, ...

PUB get_value(index) : value
  if index >= 0 AND index < TABLE_SIZE
    value := values[index]
```

### Using LOOKUP for Validation

```spin2
' WRONG: Using LOOKUP when you need LOOKDOWN
if lookup(user_input : VALID1, VALID2, VALID3)    ' This checks index, not value!
  process(user_input)

' CORRECT: Use LOOKDOWN to check if value exists
if lookdown(user_input : VALID1, VALID2, VALID3)
  process(user_input)
```

## Summary Tables

### Function Overview

| Function | Direction | Base | Returns on Failure |
|----------|-----------|------|-------------------|
| `LOOKUP` | Index -> Value | 1 | 0 |
| `LOOKUPZ` | Index -> Value | 0 | 0 |
| `LOOKDOWN` | Value -> Index | 1 | 0 |
| `LOOKDOWNZ` | Value -> Index | 0 | 0 |

### Common Use Cases

| Use Case | Function | Example |
|----------|----------|---------|
| Enum to string | LOOKUP | `lookup(code : @"A", @"B")` |
| Validate value | LOOKDOWN | `lookdown(val : 1, 2, 3) <> 0` |
| Char to digit | LOOKDOWNZ | `lookdownz(c : "0".."9")` |
| Array index mapping | LOOKUPZ | `lookupz(i : pin1, pin2)` |
| Range membership | LOOKDOWN | `lookdown(x : min..max)` |

### Index Relationship

```
Items:        A    B    C    D    E
              |    |    |    |    |
LOOKUP:       1    2    3    4    5    (out of range returns 0)
LOOKUPZ:      0    1    2    3    4    (out of range returns 0)
LOOKDOWN:     1    2    3    4    5    (not found returns 0)
LOOKDOWNZ:    0    1    2    3    4    (not found returns 0)
```

## Related Documentation

- [Control-Flow-Usage-Guide.md](Control-Flow-Usage-Guide.md) - CASE statement for complex dispatch
- [Operators-Usage-Guide.md](Operators-Usage-Guide.md) - Range operator (..)
- [String-Constants-Usage-Guide.md](String-Constants-Usage-Guide.md) - String table patterns
