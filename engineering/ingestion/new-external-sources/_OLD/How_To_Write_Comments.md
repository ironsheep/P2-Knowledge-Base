# How To Write Comments - Spin2 Documentation Guide

## Overview

This guide describes the documentation comment conventions for Spin2 code, specifically for the Propeller 2 (P2) projects. Unlike most programming languages that place documentation comments before method declarations, Spin2 uses a unique convention where documentation appears immediately **after** the method signature.

## Comment Format and Structure

### Comment Prefixes
- `''` (double apostrophe) - Used for **public** method documentation
- `'` (single apostrophe) - Used for **private** method documentation and local variable sections

### Documentation Structure

The documentation block consists of:

1. **Description line** with placeholder (`...`)
2. **Blank comment line** (separator)
3. **Parameter documentation** using `@param` tags (only if parameters exist)
4. **Return value documentation** using `@returns` tags (only if return values exist)
5. **Local variables section** (optional, non-doc) using `@local` tags (only if local variables exist)
6. **Blank line** after the comment block before any code

Note: Do NOT include `@returns None` when there are no return values. Only document what actually exists.

## Complete Example

```spin2
PUB myMethod(param1, param2) : result | local1, local2
'' Description goes here...
''
'' @param param1 - Description of first parameter
'' @param param2 - Description of second parameter
'' @returns result - Description of return value

' Local Variables:
' @local local1 - Description of local variable
' @local local2 - Description of local variable

    ' method implementation starts here (note the blank line above)
    result := param1 + param2
    local1 := param1 * 2
    local2 := param2 * 2
```

## Documentation Tags

### @param Tag
- **Format:** `@param {paramName} - description`
- **Usage:** Document each method parameter
- **Example:** `@param frequency - The clock frequency in Hz`

### @returns Tag
- **Format:** `@returns {returnName} - description`
- **Usage:** Document each return value
- **Example:** `@returns result - True if successful, false otherwise`

### @local Tag
- **Format:** `@local {localName} - description`
- **Usage:** Document local variables (uses single apostrophe prefix)
- **Example:** `@local tempValue - Temporary storage for calculation`

## Method Signature Parsing

When documenting a method, parse the signature to identify:

1. **Method visibility** (PUB for public, PRI for private)
2. **Method name**
3. **Parameters** (comma-separated list in parentheses)
4. **Return values** (after colon `:`)
5. **Local variables** (after pipe `|`)

### Example Signature Breakdown

```spin2
PUB calculateArea(width, height) : area | temp1, temp2
```

- **Visibility:** PUB (public)
- **Method name:** calculateArea
- **Parameters:** width, height
- **Return value:** area
- **Local variables:** temp1, temp2

## Best Practices

1. **Placement:** Always place documentation comments immediately after the method signature line
2. **Blank Line Separation:** Always include a blank line after the comment block before the first line of code
3. **Completeness:** Document all parameters, return values, and significant local variables
4. **Clarity:** Write clear, concise descriptions that explain the purpose and usage
5. **Consistency:** Use the same format and style throughout your codebase
6. **Placeholders:** Use `...` as a placeholder for descriptions that need to be filled in

## Private Method Example

```spin2
PRI internalCalculation(value) : result | counter
' Internal calculation helper...
'
' @param value - Input value to process
' @returns result - Processed value

' Local Variables:
' @local counter - Loop iteration counter

    repeat counter from 0 to value
        result += counter
```

## Method Without Parameters or Returns

```spin2
PUB initialize()
'' Initializes the module to default state...
''

    ' initialization code here
    configure_pins()
    reset_variables()
```

Note: No `@param` or `@returns` tags needed since there are no parameters or return values.

## Method With Multiple Returns

```spin2
PUB getCoordinates() : x, y
'' Gets the current X and Y coordinates...
''
'' @returns x - The X coordinate value
'' @returns y - The Y coordinate value

    x := current_x
    y := current_y
```

## Replacing Existing Comments

When updating existing code to use this documentation format, you need to identify and replace comments that are incorrectly placed.

### Comments to Replace

Replace comments that appear in these locations:
1. **Above the method signature** (traditional placement in most languages)
2. **Immediately below the signature** (but not in the correct format)

### Replacement Process

#### Before (Incorrect - Comments Above):
```spin2
'' This method calculates the area
'' Takes width and height as parameters
PUB calculateArea(width, height) : area
    area := width * height
```

#### After (Correct - Formatted Comments After):
```spin2
PUB calculateArea(width, height) : area
'' Calculates the rectangular area from dimensions...
''
'' @param width - Width of the rectangle
'' @param height - Height of the rectangle
'' @returns area - Calculated area value
    area := width * height
```

#### Before (Incorrect - Unformatted Comments Below):
```spin2
PUB calculateArea(width, height) : area
    ' calculates area from width and height
    area := width * height
```

#### After (Correct - Properly Formatted):
```spin2
PUB calculateArea(width, height) : area
'' Calculates the rectangular area from dimensions...
''
'' @param width - Width of the rectangle
'' @param height - Height of the rectangle
'' @returns area - Calculated area value
    area := width * height
```

### Important Notes for Replacement

1. **Preserve Information:** When replacing existing comments, preserve any valuable information from the old comments and incorporate it into the new format
2. **Remove Old Comments:** Delete the old comment blocks completely after extracting their content
3. **Check Both Locations:** Always check both above AND below the signature for existing comments that need replacement
4. **Maintain Descriptions:** If the old comments contain good descriptions, use them in the new format rather than just using placeholders
5. **Single Replacement:** Replace all old comment styles with one properly formatted block immediately after the signature

## Automation Instructions

For automated documentation generation and comment replacement:

1. **Parse** the method signature to extract:
   - Visibility modifier (PUB/PRI)
   - Method name
   - Parameter list
   - Return value list
   - Local variable list

2. **Generate** the documentation block with:
   - Appropriate comment prefix based on visibility
   - Description line with placeholder
   - Blank separator line
   - Tagged documentation for each element

3. **Insert** the documentation block immediately after the method signature

4. **Format** according to the conventions:
   - Public methods use `''` prefix
   - Private methods and local sections use `'` prefix
   - Maintain consistent indentation
   - Include all identified elements

## Summary

This documentation style is unique to Spin/Spin2 where the documentation becomes part of the method body itself, appearing after the signature rather than before. This convention ensures that documentation is tightly coupled with the implementation and follows a consistent, parseable format that can be processed by automated tools.