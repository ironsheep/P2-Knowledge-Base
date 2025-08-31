# Smart Pins 3-Block Code Pattern Specification

## Pattern Overview

Each Smart Pin mode section contains three distinct code blocks that need visual differentiation:

1. **Configuration Block** - Plain code block (no language specifier)
2. **Spin2 Example** - Code block with ````spin2` language tag  
3. **PASM2 Example** - Code block with ````pasm2` language tag

## Pattern Recognition

### Current Markdown Structure

Each mode follows this pattern:

```markdown
### Mode `%XXXXX` - Mode Name

**Configuration**
```
WRPIN: `%XXXXX` (`P_CONSTANT`)
WXPIN: Parameter description
WYPIN: Parameter description
Z Result: Result description
```

**Spin2 Example**
```spin2
PUB example() | value
  pinstart(PIN, MODE, X_PARAM, Y_PARAM)
  value := rdpin(PIN)
```

**PASM2 Example**
```pasm2
    wrpin   ##MODE, #PIN
    wxpin   ##X_PARAM, #PIN
    wypin   ##Y_PARAM, #PIN
    rdpin   value, #PIN
```
```

## Visual Differentiation Strategy

### Color Assignments (from De Silva template work)
- **Configuration**: Light blue pastel background (`lightblue!10`)
- **Spin2**: Green background (`green!10`)
- **PASM2**: De Silva yellow (`yellow!10`)

### Template Implementation

The `p2kb-smart-pins-content.sty` already contains tcolorbox environments:
- `\newtcolorbox{configblock}` - Light blue background
- `\newtcolorbox{spin2block}` - Green background  
- `\newtcolorbox{pasm2block}` - Yellow background

### Lua Filter Application

The `smart-pins-block-coloring.lua` filter identifies blocks by:
1. **Configuration**: Appears after "**Configuration**" heading, no language tag
2. **Spin2**: Has `spin2` language class
3. **PASM2**: Has `pasm2` language class

## Identification Rules

### Configuration Block Detection
- Follows immediately after a paragraph containing "**Configuration**"
- Is a plain code block (no language specifier)
- Contains WRPIN/WXPIN/WYPIN/Z Result lines

### Spin2 Block Detection
- Has `spin2` class in code block attributes
- Typically follows "**Spin2 Example**" heading
- Contains Spin2 syntax (PUB, |, pinstart, etc.)

### PASM2 Block Detection  
- Has `pasm2` class in code block attributes
- Typically follows "**PASM2 Example**" heading
- Contains PASM2 syntax (assembly instructions with # prefix)

## Pattern Consistency

All 32 Smart Pin modes follow this exact pattern:
1. Configuration parameters (always first)
2. Spin2 implementation example (always second)
3. PASM2 implementation example (always third)

Some modes may have additional code examples, but the core 3-block pattern remains consistent.

## Implementation Status

✅ **Template colors defined** - In `p2kb-smart-pins-content.sty`
✅ **Lua filter created** - `smart-pins-block-coloring.lua`
✅ **Pattern identified** - Consistent across all modes
⏳ **Testing required** - Need PDF generation to verify

## Testing Checklist

- [ ] Configuration blocks show light blue background
- [ ] Spin2 blocks show green background
- [ ] PASM2 blocks show yellow background
- [ ] Syntax highlighting preserved within colored blocks
- [ ] Page breaks don't split blocks awkwardly
- [ ] Colors print well in grayscale