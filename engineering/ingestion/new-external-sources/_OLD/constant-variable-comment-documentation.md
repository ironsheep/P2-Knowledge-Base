# Spin2 Language Server: Comment Documentation for Constants and Variables

## Overview
This document describes how the Spin2 semantic highlighter captures and displays comments for constants and variables in hover text tooltips.

## Comment Placement Rules

### Supported Comment Positions

The semantic highlighter recognizes two comment positions for constants and variables:

1. **Preceding Single-Line Comment**
   - Placed on the line immediately before the declaration
   - Must have no blank lines between comment and declaration

2. **Right-Edge (Trailing) Comment**
   - Placed on the same line after the declaration
   - Separated from the code by whitespace

### Comment Priority System

When both comment types are present, the system follows this priority:
- **Preceding comments take priority** over trailing comments
- If both exist, only the preceding comment is displayed in hover text
- Implementation: `_declarationComment()` method at `spin2.documentSemanticParser.ts:158`

## Examples by Section Type

### CON Section (Constants)

```spin
' This comment describes NEW_CONSTANT_1
NEW_CONSTANT_1 = 5

NEW_CONSTANT_2 = 7                ' This trailing comment describes NEW_CONSTANT_2

' Multi-line comments are supported
' They can span multiple lines
' All lines will be captured
VAL2 = ENUM_VAL_3
```

### Enum Constants

Multi-line preceding comments work well for documenting enum values:

```spin
' Enum with values commented:
'  ENUM_VAL_1  - First value because...
'  ENUM_VAL_2  - Second value for...
'  ENUM_VAL_3  - Third value when...
#0, ENUM_VAL_1, ENUM_VAL_2, ENUM_VAL_3
```

### VAR Section (Instance Variables)

```spin
' This comment describes forDocExplan1
LONG  forDocExplan1

LONG  forDocExplan2               ' This trailing comment describes forDocExplan2
```

### DAT Section (Data Variables)

```spin
' This comment describes sillyVar
sillyVar        long    0

sillyVar2       long    0        ' This trailing comment describes sillyVar2
```

## Comment Lifecycle

### Comment Capture
- Comments are captured during the pre-scan phase of parsing
- Stored in `priorSingleLineComment` and `rightEdgeComment` variables
- Associated with declarations via `_declarationComment()` method

### Comment Clearing Rules
Comments are cleared in these situations:
1. **After being consumed** - Once attached to a declaration
2. **Blank lines** - Any blank line clears pending preceding comments
3. **Preprocessor directives** - Clear pending comments
4. **Section changes** - Moving between CON, VAR, DAT, OBJ sections

## Hover Text Display

When hovering over a constant or variable reference, the system displays:

1. **Code Block** - The declaration line in Spin2 syntax highlighting
2. **Documentation** - The associated comment (if any)
3. **Missing Documentation** - For methods without doc-comments: `*(no doc-comment provided)*`

### Implementation Details
- Hover provider: `HoverProvider.ts:389`
- Comment retrieval: `tokenFindings.declarationComment`
- Markdown formatting with line breaks replaced by `<br>` tags

## Best Practices for Documentation

### For Constants
```spin
CON
  ' Maximum number of retries before timeout
  MAX_RETRIES = 10

  TIMEOUT_MS = 5000              ' Timeout in milliseconds
```

### For Enums
```spin
CON
  ' Motor control states:
  '  DCS_STOPPED   - Motor is completely stopped
  '  DCS_SPIN_UP   - Motor ramping up to target speed
  '  DCS_AT_SPEED  - Motor at target speed
  #0, DCS_STOPPED, DCS_SPIN_UP, DCS_AT_SPEED
```

### For Variables
```spin
VAR
  ' Current position in encoder counts
  LONG currentPosition

  LONG targetSpeed                ' Target speed in RPM
```

## Technical Implementation Notes

### Key Files
- **Parser**: `spin2.documentSemanticParser.ts`
  - `_declarationComment()`: Returns appropriate comment
  - `_getCON_DeclarationMultiLine()`: Processes constant declarations
  - `_getVAR_Declaration()`: Processes variable declarations

- **Hover Provider**: `HoverProvider.ts`
  - Retrieves and formats comments for display
  - Handles markdown conversion for tooltip rendering

### Comment Storage
- Comments stored with tokens via `setGlobalToken()` method
- Retrieved via `getGlobalToken()` for hover display
- Associated using line number and character position

## Instructions for Documentation Generators

When creating a documentation generator or Claude agent to document Spin2 code:

1. **Identify undocumented declarations** - Look for constants/variables without comments
2. **Choose comment placement**:
   - Use preceding comments for detailed explanations
   - Use trailing comments for brief descriptions
3. **Format appropriately**:
   - Single apostrophe `'` for regular comments
   - Double apostrophe `''` for documentation comments
4. **Maintain consistency** - Use the same style throughout the codebase
5. **Clear and concise** - Write meaningful descriptions that add value

### Example Generator Output
```spin
CON
  ' Clock frequency for the system in Hz
  CLK_FREQ = 270_000_000

  _clkfreq = CLK_FREQ            ' Set system clock from constant

  ' Pin assignments for SPI communication:
  '  SF_CS  - Chip select (active low)
  '  SF_SCK - Serial clock signal
  '  SF_SDO - Serial data output (MOSI)
  '  SF_SDI - Serial data input (MISO)
  SF_CS  = 61
  SF_SCK = 60
  SF_SDO = 59
  SF_SDI = 58
```

---

*This documentation is based on analysis of the Spin2 Language Server extension for VS Code.*