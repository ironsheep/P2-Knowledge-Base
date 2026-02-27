# Complete Spin2 Documentation Guide for VSCode Extension

## Overview

This comprehensive guide covers how to write documentation comments in Spin2 code so that VSCode's Spin2 extension can extract and display them across three major tools: **hover tooltips/IntelliSense**, the **Generate Documentation File** command, and the **Outline panel**. The Spin2 language uses unique documentation conventions that differ from most programming languages. Understanding which comment forms each tool consumes — and which it ignores — is essential for producing clean, professional results.

## Key Concepts

### Unique Spin2 Documentation Placement
Unlike most languages that place documentation **before** declarations, Spin2 places method documentation **after** the method signature, making it part of the method body.

### Complete Comment Type Classification

The Spin2 extension recognizes six distinct comment forms. Each has different visibility across tools:

| Comment Form | Name | Doc Comment? | Hover/IntelliSense | Doc Generator Output | Outline Label |
|---|---|---|---|---|---|
| `''` (double apostrophe) | Doc comment (single line) | **Yes** | Yes (PUB methods) | **Yes** | Never (stripped from PUB/PRI) |
| `{{ ... }}` (double brace, multi-line) | Doc comment (block) | **Yes** | No | **Yes** | Never |
| `{{ text }}` (double brace, same line) | Doc comment (inline block) | **Yes** | No | **No** — explicitly skipped | Never |
| `'` (single apostrophe) | Regular comment | No | Yes (PRI methods, locals) | **Never** | Only on CON/VAR/OBJ/DAT lines |
| `{ text }` (single brace, same line) | Brace comment (inline) | No | No | **Never** | **Yes** — on CON/VAR/OBJ/DAT lines |
| `{ ... }` (single brace, multi-line) | Block comment | No | No | **Never** | Never |

**Key distinction:** `''` (double apostrophe) is a doc comment. `'` (single apostrophe) is not. They serve completely different purposes and appear in different tools.

### Tool-Specific Comment Summary

- **Hover/IntelliSense**: Uses `''` for PUB methods, `'` for PRI methods and local variables
- **Generate Documentation File**: Uses `''` and multi-line `{{ }}` only — never `'` or `{ }`
- **Outline panel**: Uses `{ }` (brace) and `'` (tic) on section header lines only — never on PUB/PRI lines

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

## Part 2: Constants, Variables, and Section Documentation

### Section Documentation Pattern

Every CON, VAR, OBJ, and DAT block should be documented with a **single-line comment on the section header line** that briefly describes what the block contains. This comment appears in the Outline panel and serves as the section's label.

Either form of non-doc comment works on the section header line:

```spin2
CON { Motor Configuration }        ' brace comment — appears in outline
VAR ' Instance Variables            ' tic comment — also appears in outline
```

Both `{ text }` (brace) and `' text` (tic) are picked up by the outline. If both appear on the same line, the **leftmost** comment is the one captured — regardless of type. In practice, use one or the other, not both.

Inside the section, use **single-line `'` comments** to describe groups of related declarations. These are regular implementation comments — they appear in hover tooltips for the items they precede but do NOT appear in generated documentation or the outline.

```spin2
CON { Motor Configuration }

  ' Speed limits
  MAX_SPEED = 1000
  MIN_SPEED = 100

  ' Acceleration parameters
  RAMP_RATE = 50
  ACCEL_TIME_MS = 200
```

**Do NOT use doc comments (`''`) or block comments (`{{ }}`) inside sections.** They serve no useful purpose there:
- `''` inside a CON/VAR/OBJ/DAT section before the first PUB **leaks into the file-top generated documentation** — producing unexpected output
- `{{ }}` multi-line blocks inside sections are invisible to hover and the outline
- `{ }` on lines other than the section header line are invisible to the outline

The correct pattern is always: **`{ }` or `'` comment on the section header line for the outline label, single-line `'` comments inside the block for group descriptions.**

### Comment Placement Options for Individual Declarations

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

---

## Part 3: Generate Documentation File Command

The VSCode Spin2 extension includes a command that generates a `.txt` public interface document from a `.spin2` or `.spin` source file. This is the primary mechanism for producing object documentation that other developers consume.

### Triggering the Generator

| Platform | Keybinding |
|---|---|
| macOS | `Ctrl+Alt+Cmd+D` |
| Windows/Linux | `Ctrl+Alt+D` |
| Command Palette | `Spin2: Generate Documentation File` |

The generator produces a `{filename}.txt` file in the same directory as the source.

### Two-Pass Generation Process

#### Pass 1: File-Top Documentation + PUB Signature List

The first pass walks every line from top to bottom.

**File-top doc comments** are collected from the beginning of the file until the first PUB section:
- `''` lines: Text after `''` (from character position 2 onward) is written to output. The `''` prefix is stripped.
- `{{ ... }}` multi-line blocks: Content is emitted line by line. Opening `{{` and closing `}}` lines emit text only if the trimmed line is longer than 2 characters. Interior lines are emitted as-is (trimmed).

**Critical behavior:** File-top collection does NOT stop at CON, VAR, OBJ, or DAT sections — it continues through them. It only stops at the first PUB. This means `''` doc comments inside a CON section before the first PUB **will** appear in the file-top documentation.

**At the first PUB**, the generator emits the interface header:
```
Object "{filename}" Interface:
  (Requires Spin2 Language v##)    ← only if {Spin2_v##} found in file-top

PUB firstMethod(params) : returns
PUB secondMethod(params)
...
```

All PUB signatures are listed with comments and local variables stripped.

#### Pass 2: PUB Method Details

The second pass emits detailed documentation for each PUB method:
```
___________________________________
PUB methodName(params) : returns

 doc comment content here...
```

**Doc comments for a PUB method** are the `''` lines and `{{ }}` multi-line blocks that appear **after** the PUB declaration line, up until the next section start (PUB, PRI, CON, VAR, OBJ, or DAT).

**Trailing doc comment on the PUB line itself:** If the PUB line contains `'' text` or `{{ text }}` after the signature, that text is emitted as the first line of documentation for that method.

**PRI methods are excluded.** When a PRI section is encountered, doc comment collection is turned off. PRI documentation never appears in the output.

### Language Version Spec

The generator searches for `{Spin2_v##}` (e.g., `{Spin2_v44}`) in the file-top area. If found, it emits `(Requires Spin2 Language v44)` in the interface header. Place the version spec in a non-doc comment to avoid duplication:
```spin2
{Spin2_v44}
'' My driver description
```

### Generated Output Structure Example

```
 File description line 1
 File description line 2

Object "myDriver" Interface:
  (Requires Spin2 Language v44)

PUB start(basePin, pinCount)
PUB configure(mode, value)
PUB getStatus() : status

___________________________________
PUB start(basePin, pinCount)

 Start the driver with given pins
 @param basePin - first pin to use
 @param pinCount - number of pins

___________________________
PUB configure(mode, value)

 Configure operating mode

__________________________
PUB getStatus() : status

 Return current status
 @returns status - current operating state

 File-bottom documentation here
```

### Doc Generator Pitfalls (What NOT to Do)

1. **Don't use single-line `{{ }}`** — Opening and closing `{{` `}}` on the same line is explicitly skipped by the generator. Use `''` instead, or break into a multi-line block.

2. **Don't use `'` (single apostrophe) expecting it in generated docs** — Only `''` (double apostrophe) is a doc comment. Single `'` is an implementation comment and never appears in generated output.

3. **Don't put section-organization `''` comments between PUB methods:**
   ```spin2
   PUB method1()
   '' method1 documentation

   '' ========== Motor Methods ==========    ← CAPTURED as method1's documentation!

   PUB method2()
   ```
   Use `'` (single apostrophe) for organizational separators between methods.

4. **Don't put `''` in early CON/VAR/OBJ sections** unless you want them in the file-top doc — file-top collection continues through all sections until the first PUB.

5. **Don't rely on blank `''` for spacing** — A `''` line with no text (exactly 2 characters) produces **no output**, not even a blank line. To get a blank line, use `''` followed by at least one space character (`'' `).

6. **Don't expect PRI method documentation to appear** — The generator only includes PUB methods.

7. **Watch for `{Spin2_v##}` duplication** — If `{Spin2_v44}` appears inside a `''` doc comment, it shows up twice (as literal text AND as the header line). Place it in a `{ }` non-doc comment instead.

### Related: Insert Doc Comment Command

The Insert Doc Comment command (`Ctrl+Alt+Cmd+C` on macOS) auto-generates `''` comment stubs for PUB/PRI methods. For PUB methods, it uses `''` (doc comments) for description, `@param`, and `@returns` lines, and `'` (non-doc) for local variables — correctly keeping locals out of generated documents.

---

## Part 4: Outline Panel Display

The VSCode Outline panel shows a navigable tree of section blocks and method declarations. Understanding what appears here — and how comments affect labels — helps write well-organized code.

### How the Outline Works

The outline is produced by a three-stage pipeline:
1. **Document Symbol Parsers** scan each source line and build outline symbols
2. **DocumentSymbolProvider** converts symbols into LSP `DocumentSymbol` responses (straight pass-through)
3. **VSCode** renders the Outline panel from the symbols

All comment logic lives in the parsers (step 1).

### Section Headers: CON, VAR, OBJ, DAT

For these four section types, a comment on the **same line** as the section keyword is included in the outline label. The comment text — including delimiters — is concatenated directly onto the keyword.

**Comment recognition:** Either `{ text }` (brace) or `' text` (tic) on the section header line is captured. If both appear on the same line, the **leftmost** one wins regardless of type.

| Source Line | Outline Label |
|---|---|
| `CON { Motor Constants }` | `CON { Motor Constants }` |
| `VAR ' Instance Variables` | `VAR ' Instance Variables` |
| `DAT` | `DAT` (no comment) |
| `OBJ { objects } ' more info` | `OBJ { objects }` (leftmost wins) |

**What does NOT work for the outline:**
- A comment on the line **above** the section keyword — invisible to the outline
- Multi-line `{ ... }` that starts with `{` but has no `}` on the same line — not captured
- `{{ text }}` — incidentally captures inner content between first `{` and first `}`, not intentional support

### Method Declarations: PUB, PRI

For PUB and PRI methods, comments are **actively stripped** from the outline. Only the method name, parameters, and return values survive.

The parser removes:
1. Tic comments (splits on `'`, keeps before)
2. Brace comments (splits on `{`, keeps before)
3. Local variables (splits on `|`, keeps before)

| Source Line | Outline Label |
|---|---|
| `PUB start(pin, freq)` | `PUB start(pin, freq)` |
| `PUB start(pin) ' Start motor` | `PUB start(pin)` |
| `PUB start(pin) { motor } \| tmp` | `PUB start(pin)` |

In Spin2, PUB entries show "Public" and PRI entries show "Private" as secondary detail text.

### DAT Section Children

DAT sections can contain child items: global PASM labels. These are identifiers in column 1 of DAT/PASM lines that are not reserved words, data declarations, local labels (`.` or `:`), or debug directives. They appear nested under their parent DAT entry, with no associated comments.

Spin2 also supports inline PASM labels (from `ORG`/`ORGH`/`ORGF` blocks inside PUB/PRI methods) as outline children.

### Lines the Outline Never Sees

Before any comment extraction, a state machine skips entire lines that are pure comments:
- `' text` (starts with single tic) — skipped
- `'' text` (starts with double tic) — skipped
- `{{ text }}` (single-line doc comment) — skipped
- `{{ ... }}` (multi-line doc comment block) — all lines skipped
- `{ ... }` (multi-line block comment) — all lines skipped
- Whitespace-only lines — skipped

Only lines that **begin with a section keyword** (CON, VAR, OBJ, DAT, PUB, PRI) in column 1 are candidates for outline entries.

### SymbolKind Icons

| Section | Icon Kind |
|---|---|
| CON | Method |
| VAR | Variable |
| OBJ | Class |
| DAT | EnumMember |
| PUB | Method |
| PRI | Field |
| DAT/PASM global labels | String |

### Guidelines for Outline-Friendly Code

1. **Label sections on the same line** as the keyword:
   ```spin2
   CON { Motor Constants }
   VAR ' Instance Variables
   ```

2. **Prefer brace comments `{ }` for section labels** — visually distinct and checked first.

3. **Comments above or below** the section keyword line do not appear in the outline.

4. **PUB/PRI comments never appear** in the outline — keep method documentation in `''` doc comments for the doc generator and hover tooltips.

---

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

### For AI Code Generation Agents

When generating or modifying Spin2 code, follow these rules to produce correct results across all three VSCode tools:

#### What TO Do
1. **Use `''` for all PUB method documentation** — appears in both hover tooltips AND generated interface docs
2. **Use `'` for PRI method documentation** — appears in hover tooltips, correctly excluded from generated docs
3. **Use `'` for local variable docs in PUB methods** (with `@local` tags) — keeps them out of generated docs
4. **Place method documentation immediately after the PUB/PRI line**, not before it
5. **Put a single-line comment on every CON/VAR/OBJ/DAT section line** to label the block for the outline — either `{ text }` or `' text` works (e.g., `CON { Motor Constants }` or `VAR ' Instance Variables`)
6. **Use `'` single-line comments inside sections** to describe groups of constants/variables (e.g., `' Speed limits` above a group of speed-related constants)
7. **Use `'` for organizational separators** between methods (e.g., `' ---- Motor Methods ----`)
8. **Place `{Spin2_v##}` in a non-doc `{ }` comment** to avoid duplication in generated docs
9. **Use `'' ` (with trailing space) when you need blank lines** in generated documentation

#### What NOT To Do
1. **Don't use `''` or `{{ }}` inside CON/VAR/OBJ/DAT sections** — `''` before the first PUB leaks into file-top generated docs; `{{ }}` is invisible to all tools in this context. Use `'` for all comments inside sections.
2. **Don't use multi-line block comments (`{{ }}` or `{ }`) as section introductions** — they don't appear in the outline, hover, or generated docs. Use a single-line `{ }` on the section header line instead.
3. **Don't put section descriptions on lines above or below the section keyword** — only same-line comments appear in the outline
4. **Don't use `''` for section separators between PUB methods** — they get captured as the preceding method's documentation
5. **Don't use single-line `{{ text }}`** for documentation — explicitly skipped by the doc generator
6. **Don't use `'` expecting it in generated docs** — only `''` and multi-line `{{ }}` produce output
7. **Don't expect PRI method docs to appear** in generated interface documents — only PUB methods are included

### Method Documentation Template
```spin2
PUB {methodName}({parameters}) : {returns} | {locals}
'' {description}...
''
'' @param {paramName} - {description}
'' @returns {returnName} - {description}

' Local Variables:
' @local {localName} - {description}

    {method implementation}
```

### Well-Structured File Template
```spin2
{Spin2_v44}
'' Object description for file-top documentation
'' Additional description lines

CON { Configuration Constants }

  _clkfreq = 200_000_000

VAR { Instance Variables }

  LONG  instanceData

OBJ { Child Objects }

  serial : "jm_serial"

PUB start(basePin, pinCount) : ok
'' Start the driver with given pins
''
'' @param basePin - first pin to use
'' @param pinCount - number of consecutive pins
'' @returns ok - true if started successfully

    ' implementation here

' ---- Sensor Methods ----

PUB readSensor(channel) : value
'' Read the specified sensor channel
''
'' @param channel - sensor channel number (0-7)
'' @returns value - raw sensor reading

    ' implementation here

PRI helper(x) : result
' Internal calculation helper
'
' @param x - input value
' @returns result - computed result

    result := x * 2

DAT { PASM Driver }

                org
entry           ' cog entry point
                ' PASM code here
```

## Summary

This documentation system is unique to Spin/Spin2 languages and provides tight integration between code and three distinct tools. Key points to remember:

### Comment Form Quick Reference
- **`''` (double apostrophe)** — Doc comment. Appears in: hover tooltips (PUB), generated documentation, NOT outline
- **`'` (single apostrophe)** — Regular comment. Appears in: hover tooltips (PRI, locals), outline (section headers only), NOT generated docs
- **`{ text }` (brace, same line)** — Inline brace comment. Appears in: outline (section headers), NOT hover, NOT generated docs
- **`{{ ... }}` (double brace, multi-line)** — Block doc comment. Appears in: generated documentation only
- **`{{ text }}` (double brace, same line)** — Explicitly skipped by doc generator. Avoid for documentation.

### Critical Rules
- **Method docs go AFTER the signature**, not before
- **Use `''` for all PUB method documentation** — this is the one form that works across hover AND doc generator
- **Use `'` for PRI methods, local variables, and implementation notes** — keeps them out of generated docs
- **Use `{ }` or `'` on section header lines** for outline labels (e.g., `CON { Motor Constants }` or `VAR ' Instance Variables`)
- **Don't put `''` between PUB methods** for organization — they get captured as the preceding method's documentation
- **Don't use `'` expecting it in generated docs** — only `''` and multi-line `{{ }}` appear there
- **Preceding comments take priority** over trailing comments for variables/constants in hover
- **Blank `''` lines produce no output** in generated docs — use `'' ` (with trailing space) for blank lines

### Tool Coverage
| Tool | What It Shows | Comment Forms Used |
|---|---|---|
| Hover/IntelliSense | Method docs, constant/variable docs | `''` (PUB), `'` (PRI, locals, CON/VAR) |
| Generate Documentation File | Public interface document | `''` and multi-line `{{ }}` only |
| Outline Panel | Section tree with labels | `{ }` or `'` on section header lines (leftmost wins if both present) |

The VSCode Spin2 extension leverages these conventions to provide a rich development experience with contextual help, navigable outlines, and publishable interface documentation right in the editor.