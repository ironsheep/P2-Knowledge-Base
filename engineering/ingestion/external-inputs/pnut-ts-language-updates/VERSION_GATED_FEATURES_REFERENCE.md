# Version-Gated Features Reference

**Source**: Official Spin2 Language Reference (pnut-ts)
**Purpose**: Identifies which features REQUIRE `{Spin2_vXX}` version directives

---

## Key Insight

**NOT all new features require version directives.** Only the features listed below require the `{Spin2_vXX}` directive at the start of the source file. Features introduced in a version but NOT listed here are simply available when using that compiler version or later - no directive needed.

---

## Version-Gated Features (Directive REQUIRED)

### V43 - `{Spin2_v43}`

| Feature | Type | Description |
|---------|------|-------------|
| LSTRING | Method | Declares a constant string preceded by a length byte |

---

### V44 - `{Spin2_v44}`

| Feature | Type | Description |
|---------|------|-------------|
| BYTESWAP | Method | Swap two ranges of bytes |
| WORDSWAP | Method | Swap two ranges of words |
| LONGSWAP | Method | Swap two ranges of longs |
| BYTECOMP | Method | Compare two ranges of bytes |
| WORDCOMP | Method | Compare two ranges of words |
| LONGCOMP | Method | Compare two ranges of longs |
| BOOL, BOOL_ | DEBUG | Output a boolean, "TRUE" if non-0 or "FALSE" if 0 |
| FILL | Method | Fill a structure with a byte value |
| COPY | Method | Copy one structure to another |
| SWAP | Method | Swap contents of structures |
| COMP | Method | Compare contents of structures |

---

### V45 - `{Spin2_v45}`

| Feature | Type | Description |
|---------|------|-------------|
| STRUCT | Keyword | In a CON block, precedes a structure definition |
| SIZEOF | Method | Returns the size of a structure in bytes |

---

### V46 - `{Spin2_v46}`

| Feature | Type | Description |
|---------|------|-------------|
| C_Z | DEBUG | Output the C and Z flag states |

---

### V47 - `{Spin2_v47}`

| Feature | Type | Description |
|---------|------|-------------|
| TASKSPIN | Method | Initialize a new task |
| TASKNEXT | Method | Switch to the next unhalted task |
| TASKSTOP | Method | Stop and free a task |
| TASKHALT | Method | Halt a task |
| TASKCONT | Method | Continue a task |
| TASKCHK | Method | Check the status of a task. Unused/running/halted = 0/1/2 |
| TASKID | Method | Get the ID of the current task |
| NEWTASK | Constant | (-1) For use in TASKSPIN |
| THISTASK | Constant | (-1) For use in TASKSTOP and TASKHALT |
| TASKHLT | Register | Register which holds the HALT bits (in reverse order) |

---

### V50 - `{Spin2_v50}`

| Feature | Type | Description |
|---------|------|-------------|
| DITTO | Directive | In a DAT block, begin/end an iterative generation section |

---

### V51 - `{Spin2_v51}`

| Feature | Type | Description |
|---------|------|-------------|
| POW | Operator | Floating-point x-to-power-of-y function |
| LOG2 | Operator | Floating-point base-2 logarithm function |
| EXP2 | Operator | Floating-point 2-to-power-of-x function |
| LOG10 | Operator | Floating-point base-10 logarithm function |
| EXP10 | Operator | Floating-point 10-to-power-of-x function |
| LOG | Operator | Floating-point natural logarithm function |
| EXP | Operator | Floating-point e-to-power-of-x function |

---

### V52 - `{Spin2_v52}`

| Feature | Type | Description |
|---------|------|-------------|
| ENDIANL | Method | Return reverse-endian long value |
| ENDIANW | Method | Return reverse-endian word value |
| DEBUG_END_SESSION | Constant | (27) for use in DEBUG |

---

## Features NOT Requiring Directives

The following features from V46-V52 are **NOT** in the gated list above, meaning they do NOT require a version directive - they're available when using the appropriate compiler version:

### V46 (No directive needed)
- `:=:` swap operator
- DEBUG_MASK constant
- Pointer types (^BYTE, ^WORD, ^LONG)

### V47 (No directive needed)
- Preprocessor directives (#DEFINE, #UNDEF, #IFDEF, #IFNDEF, #ELSEIFDEF, #ELSEIFNDEF, #ELSE, #ENDIF)
- Conditional DEBUG in PASM (IF_x DEBUG)

### V48 (No directive needed)
- External preprocessor symbols (command-line -D option)

### V49 (No directive needed)
- Structure export/import
- object.struct_t syntax
- Compiler limit increases

### V50 (No directive needed)
- Escape character strings (@\"...\")
- ORGH inline assembly in Spin2 methods
- Register constants in CON blocks (INA, OUTA, etc.)
- PLOT LAYER command
- PLOT CROP command
- $$ as DITTO iteration index (DITTO itself requires directive)

### V52 (No directive needed)
- MOVBYTS function
- NEXT level parameter
- QUIT level parameter

---

## Usage Pattern

**For gated features:**
```spin2
{Spin2_v51}                    ' REQUIRED at file start
CON
  _clkfreq = 200_000_000

PUB main() | x, y
  x := 8.0
  y := LOG2(x)                 ' LOG2 requires {Spin2_v51}
```

**For non-gated features:**
```spin2
' No version directive needed - just use newer compiler
CON
  _clkfreq = 200_000_000

PUB main()
  #IFDEF DEBUG_MODE            ' Preprocessor available in v47+ compiler
    debug("Debug enabled")
  #ENDIF
```

---

## Important Notes

1. **Directive enables ALL features for that version and earlier** - `{Spin2_v51}` enables v43, v44, v45, v46, v47, v50, AND v51 gated features.

2. **Non-gated features depend on compiler version** - You just need to use a compiler version that supports the feature.

3. **STRUCT/SIZEOF cascade** - STRUCT requires `{Spin2_v45}`, but many structure-related features (FILL, COPY, SWAP, COMP) require `{Spin2_v44}`.

4. **DITTO vs $$** - DITTO directive requires `{Spin2_v50}`, but once inside a DITTO block, $$ works without additional requirements.

---

*Parsed from official Spin2 language reference source - 2026-01-13*
