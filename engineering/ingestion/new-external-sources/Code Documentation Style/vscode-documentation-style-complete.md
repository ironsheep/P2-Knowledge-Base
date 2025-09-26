# Complete Spin2 Documentation Guide for VSCode Extension

## Overview

This comprehensive guide covers how to write documentation comments in Spin2 code so that VSCode's Spin2 extension can extract and display them in hover tooltips and IntelliSense. The Spin2 language uses unique documentation conventions that differ from most programming languages.

## Key Concepts

### Unique Spin2 Documentation Placement
Unlike most languages that place documentation **before** declarations, Spin2 places method documentation **after** the method signature, making it part of the method body.

### Comment Types and Visibility
- `''` (double apostrophe) - **Public** method documentation and doc-comments
- `'` (single apostrophe) - **Private** method documentation and regular comments, and local variables of **Public** methods

---

## Part 1: Method Documentation

### Method Documentation Structure

Method documentation appears immediately **after** the method signature and follows this structure:

1. **Description line** with placeholder (`...`) or actual description
2. **Blank comment line** (separator)
3. **Parameter documentation** using `@param` tags (if parameters exist)
4. **Return value documentation** using `@returns` tags (if return values exist)
5. **Local variables section** using `@local` tags (if local variables exist)
6. **Blank line** before any implementation code

**Important:** Only document elements that actually exist. Don't include `@returns None` for methods without return values.

### Complete Method Example

```spin2
PUB calculateArea(width, height) : area | temp1, temp2
'' Calculates the rectangular area from given dimensions...
''
'' @param width - Width of the rectangle in units
'' @param height - Height of the rectangle in units
'' @returns area - Calculated area value

' Local Variables:
' @local temp1 - Temporary storage for width calculation
' @local temp2 - Temporary storage for height calculation

    temp1 := width * 2
    temp2 := height * 2
    area := width * height
```

### Documentation Tags Reference

| Tag | Format | Usage | Example |
|-----|--------|-------|---------|
| `@param` | `@param {paramName} - description` | Document method parameters | `@param frequency - The clock frequency in Hz` |
| `@returns` | `@returns {returnName} - description` | Document return values | `@returns result - True if successful` |
| `@local` | `@local {localName} - description` | Document local variables | `@local counter - Loop iteration counter` |

### Method Signature Parsing

When documenting a method, identify these elements from the signature:

```spin2
PUB methodName(param1, param2) : returnValue | local1, local2
```

- **Visibility:** `PUB` (public) or `PRI` (private)
- **Method name:** `methodName`
- **Parameters:** `param1, param2` (comma-separated in parentheses)
- **Return values:** `returnValue` (after colon `:`)
- **Local variables:** `local1, local2` (after pipe `|`)

### Various Method Documentation Examples

#### Private Method
```spin2
PRI internalHelper(value) : result | counter
' Internal calculation helper for complex operations...
'
' @param value - Input value to process
' @returns result - Processed result value

' Local Variables:
' @local counter - Iteration counter for processing loop

    repeat counter from 0 to value
        result += counter * 2
```

#### Method Without Parameters or Returns
```spin2
PUB initialize()
'' Initializes the module to default operational state...
''

    configure_pins()
    reset_variables()
    start_timers()
```

#### Method With Multiple Returns
```spin2
PUB getPosition() : x, y, z
'' Gets the current 3D position coordinates...
''
'' @returns x - X coordinate value
'' @returns y - Y coordinate value  
'' @returns z - Z coordinate value

    x := current_x_pos
    y := current_y_pos
    z := current_z_pos
```

### Replacing Existing Incorrect Comments

When updating existing code, replace comments in these incorrect locations:

#### Before (Incorrect - Above Signature):
```spin2
'' This method calculates the area
'' Takes width and height as parameters
PUB calculateArea(width, height) : area
    area := width * height
```

#### After (Correct - After Signature):
```spin2
PUB calculateArea(width, height) : area
'' Calculates the rectangular area from dimensions...
''
'' @param width - Width of the rectangle
'' @param height - Height of the rectangle
'' @returns area - Calculated area value

    area := width * height
```

---

## Part 2: Constants and Variables Documentation

### Comment Placement Options

The VSCode Spin2 extension recognizes two types of comments for constants and variables:

1. **Preceding Comments** (Higher Priority)
   - Placed on the line immediately before the declaration
   - No blank lines between comment and declaration
   - Takes priority if both types are present

2. **Trailing Comments** (Lower Priority)
   - Placed on the same line after the declaration
   - Separated from code by whitespace

### CON Section (Constants)

#### Single Constants
```spin
' Maximum number of connection retries before timeout
MAX_RETRIES = 10

TIMEOUT_MS = 5000              ' Timeout duration in milliseconds

' System clock frequency in Hz for timing calculations
CLK_FREQ = 270_000_000
```

#### Enum Documentation
```spin
' Motor control states for drive system:
'  DCS_STOPPED   - Motor completely stopped, no power
'  DCS_SPIN_UP   - Motor ramping up to target speed
'  DCS_AT_SPEED  - Motor running at target speed
'  DCS_SPIN_DOWN - Motor ramping down to stop
#0, DCS_STOPPED, DCS_SPIN_UP, DCS_AT_SPEED, DCS_SPIN_DOWN

' Pin assignments for SPI communication interface:
'  SF_CS  - Chip select signal (active low)
'  SF_SCK - Serial clock signal
'  SF_SDO - Serial data output (MOSI)
'  SF_SDI - Serial data input (MISO)
SF_CS  = 61
SF_SCK = 60
SF_SDO = 59
SF_SDI = 58
```

### VAR Section (Instance Variables)

```spin
VAR
  ' Current encoder position in counts
  LONG currentPosition

  LONG targetSpeed               ' Desired motor speed in RPM
  
  ' Buffer for incoming serial data packets
  BYTE serialBuffer[256]
  
  WORD statusFlags               ' System status bit flags
```

### DAT Section (Data Variables)

```spin
DAT
  ' Configuration table for sensor calibration
  sensorConfig    long    0, 100, 200, 300
  
  deviceName      byte    "P2 Controller", 0    ' Null-terminated device name string
  
  ' Lookup table for sine wave generation
  sineTable       word    0, 707, 1000, 707
```

## Comment Lifecycle and Behavior

### Comment Priority System
- **Preceding comments always take priority** over trailing comments
- If both types exist, only the preceding comment appears in hover text
- Implementation handles this via the `_declarationComment()` method

## Best Practices

### Documentation Quality
1. **Be Descriptive** - Write clear, meaningful descriptions that add value
2. **Include Units** - Specify units for numeric values (Hz, ms, RPM, etc.)
3. **Explain Purpose** - Don't just restate what the code does, explain why
4. **Stay Current** - Update documentation when code changes

### Formatting Consistency
1. **Use Consistent Style** - Choose preceding or trailing and stick to it
2. **Maintain Spacing** - Keep consistent whitespace and alignment
3. **Group Related Items** - Document related constants/variables together
4. **Use Meaningful Names** - Good names reduce documentation burden

### Multi-line Comments
```spin
' This is a multi-line comment that provides
' detailed explanation spanning several lines
' for complex constants or variables that need
' extensive documentation
COMPLEX_CONFIG = $12345678
```

## Automation Guidelines

### For Documentation Generators
When creating automated documentation tools:

1. **Parse Signatures** - Extract method elements (params, returns, locals)
2. **Identify Undocumented Items** - Find constants/variables/methods without comments
3. **Choose Appropriate Placement**:
   - Methods: Always after signature
   - Constants/Variables: Preceding for detailed, trailing for brief
4. **Generate Structured Comments** - Use proper tags and formatting
5. **Maintain Consistency** - Apply the same style throughout codebase

### Example Generator Template
```spin2
PUB {methodName}({parameters}) : {returns} | {locals}
'' {description}...
''
{@param tags for each parameter}
{@returns tags for each return value}

{@local tags for each local variable if any}

    {method implementation}
```

## Summary

This documentation system is unique to Spin/Spin2 languages and provides tight integration between code and documentation. Key points to remember:

- **Method docs go AFTER the signature**, not before
- **Use double apostrophes** (`''`) for public method documentation  
- **Use single apostrophes** (`'`) for private methods and variable comments, and local variables of public methods
- **Preceding comments take priority** over trailing comments for variables/constants
- **VSCode displays documentation** in hover tooltips and IntelliSense
- **Consistency is key** - establish patterns and follow them throughout your codebase

The VSCode Spin2 extension leverages these conventions to provide rich development experience with contextual help and documentation right in the editor.