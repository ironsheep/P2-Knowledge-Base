# Manual Feature Distribution Guide

This document provides guidance for distributing Spin2/PASM2 language features across different manual types. Use this when updating or creating PASM2 and Spin2 reference and tutorial manuals.

---

## Overview

The PNut-TS compiler supports both Spin2 (high-level language) and PASM2 (assembly language). Language features must be documented in the appropriate manuals based on:

1. **Which language the feature primarily belongs to** (Spin2 vs PASM2)
2. **The purpose of the manual** (Reference vs Tutorial)

Reference manuals provide complete, authoritative syntax documentation.
Tutorial manuals provide progressive learning with practical examples.

---

## Feature Distribution Matrix

### BYTE, WORD, LONG Features

| Feature | PASM2 Ref | PASM2 Tutorial | Spin2 Ref | Spin2 Tutorial |
|---------|:---------:|:--------------:|:---------:|:--------------:|
| DAT block declarations (`BYTE val`, `WORD val`, `LONG val`) | ✓ Full | ✓ Intro | ✓ Full | - |
| DAT arrays with repetition (`BYTE 0[100]`) | ✓ Full | ✓ Examples | ✓ Full | - |
| BYTEFIT/WORDFIT directives | ✓ Full | - | ✓ Full | - |
| VAR block declarations | - | - | ✓ Full | ✓ Intro |
| Local variable declarations (`| BYTE x`) | - | - | ✓ Full | ✓ Intro |
| Method parameter types (`PUB Foo(BYTE x)`) | - | - | ✓ Full | ✓ Examples |
| Return type declarations (`: BYTE result`) | - | - | ✓ Full | ✓ Examples |
| Memory access operators (`BYTE[addr]`) | - | - | ✓ Full | ✓ Patterns |
| Type override (`.BYTE[n]`, `.WORD[n]`) | - | - | ✓ Full | - |
| Data constructors (`BYTE(v1, v2, ...)`) | - | - | ✓ Full | - |
| RDBYTE/RDWORD/RDLONG instructions | ✓ Full | ✓ Progressive | - | - |
| WRBYTE/WRWORD/WRLONG instructions | ✓ Full | ✓ Progressive | - | - |
| BYTEFILL/WORDFILL/LONGFILL | - | - | ✓ Full | ✓ Examples |
| BYTEMOVE/WORDMOVE/LONGMOVE | - | - | ✓ Full | ✓ Examples |
| BYTESWAP/WORDSWAP/LONGSWAP | - | - | ✓ Full | - |
| BYTECOMP/WORDCOMP/LONGCOMP | - | - | ✓ Full | - |
| Alignment directives (ALIGNW/ALIGNL) | ✓ Full | ✓ Why it matters | ✓ Full | - |

### STRUCT Features

| Feature | PASM2 Ref | PASM2 Tutorial | Spin2 Ref | Spin2 Tutorial |
|---------|:---------:|:--------------:|:---------:|:--------------:|
| STRUCT definition syntax | ✓ Layout only | - | ✓ Full | ✓ Intro |
| Typed members (BYTE/WORD/LONG) | ✓ Layout only | - | ✓ Full | ✓ Examples |
| Array members (`data[n]`) | ✓ Layout only | - | ✓ Full | ✓ Examples |
| Nested structures | ✓ Layout only | - | ✓ Full | ✓ When to use |
| Structure aliases (`STRUCT new = old`) | - | - | ✓ Full | - |
| VAR structure instances | - | - | ✓ Full | ✓ Intro |
| Local structure variables | - | - | ✓ Full | ✓ Examples |
| Structure parameters/returns | - | - | ✓ Full | ✓ Patterns |
| Dot notation member access | - | - | ✓ Full | ✓ Intro |
| Structure assignment (`:=`) | - | - | ✓ Full | ✓ Examples |
| Multi-value assignment (`s := v1, v2`) | - | - | ✓ Full | - |
| Structure swap (`:=:`) | - | - | ✓ Full | - |
| Clear/set all (`s~`, `s~~`) | - | - | ✓ Full | - |
| Structure comparison (`==`, `<>`) | - | - | ✓ Full | ✓ Examples |
| SIZEOF() operator | ✓ Full | ✓ For RES calc | ✓ Full | ✓ Examples |
| DAT structure declarations | ✓ Full | - | ✓ Full | - |

### Pointer Features

| Feature | PASM2 Ref | PASM2 Tutorial | Spin2 Ref | Spin2 Tutorial |
|---------|:---------:|:--------------:|:---------:|:--------------:|
| Typed pointer declarations (`^BYTE`, `^WORD`, `^LONG`) | - | - | ✓ Full | ✓ Intro |
| Structure pointers (`^structName`) | - | - | ✓ Full | ✓ When to use |
| Address-of operator (`@`) | ✓ Brief | ✓ Examples | ✓ Full | ✓ Intro |
| Pointer dereferencing (`BYTE[ptr]`, etc.) | - | - | ✓ Full | ✓ Patterns |
| Structure pointer member access (`ptr.member`) | - | - | ✓ Full | ✓ Examples |
| Bracket dereference (`[ptr]`) | - | - | ✓ Full | - |
| Pointer increment/decrement (`ptr++`, `--ptr`) | - | - | ✓ Full | ✓ Intro |
| Bracket increment notation (`ptr[++]`, `[++]ptr`) | - | - | ✓ Full | - |
| Indexed pointer access (`BYTE[ptr][i]`) | - | - | ✓ Full | ✓ Examples |
| Modify-and-assign through pointers | - | - | ✓ Full | - |
| Pointer parameters (`^BYTE pData`) | - | - | ✓ Full | ✓ Pass-by-ref |
| Pointer return values | - | - | ✓ Full | ✓ Examples |
| PTRA/PTRB usage | ✓ Full | ✓ Progressive | - | - |
| Auto-increment hub access (`RDLONG x, ptra++`) | ✓ Full | ✓ Patterns | - | - |

### FIELD Operator Features

| Feature | PASM2 Ref | PASM2 Tutorial | Spin2 Ref | Spin2 Tutorial |
|---------|:---------:|:--------------:|:---------:|:--------------:|
| Field pointer creation (`^@var.[h..l]`) | - | - | ✓ Full | ✓ Intro |
| FIELD read (`FIELD[ptr][i]`) | - | - | ✓ Full | ✓ Examples |
| FIELD write (`FIELD[ptr][i] := v`) | - | - | ✓ Full | ✓ Examples |
| FIELD modify-and-assign | - | - | ✓ Full | - |
| FIELD clear/set (`~`, `~~`) | - | - | ✓ Full | - |
| Bitfield width calculation | - | - | ✓ Full | ✓ Storage calc |
| Storage requirements | - | - | ✓ Full | ✓ Examples |
| Register bitfield access | - | - | ✓ Full | - |

---

## PASM2 Reference Manual Guidance

### What to Include

1. **DAT Block Data Declarations**
   - Complete BYTE/WORD/LONG syntax with all variations
   - Array notation with repetition counts
   - BYTEFIT/WORDFIT constraint directives
   - Alignment directives (ALIGNW, ALIGNL)
   - Inline type mixing

2. **Hub Memory Instructions**
   - RDBYTE, RDWORD, RDLONG - all addressing modes
   - WRBYTE, WRWORD, WRLONG - all addressing modes
   - PTRA/PTRB pointer register usage
   - Auto-increment/decrement variants
   - Timing and pipeline considerations

3. **SIZEOF() Operator**
   - Usage in RES calculations
   - Usage in address arithmetic
   - Example: `RES SIZEOF(structName) / 4`

4. **Structure Memory Layout**
   - How STRUCT definitions translate to memory
   - Member offset calculations
   - Accessing Spin2-declared structures from PASM2

### What NOT to Include

- Spin2 VAR/local/parameter syntax
- Typed pointer operations (`^BYTE`, etc.)
- FIELD operator (Spin2-only)
- Built-in functions (BYTEFILL, etc.)
- Dot notation member access

---

## PASM2 Tutorial Manual Guidance

### Learning Progression

1. **Chapter: Data Sizes**
   - Why we have BYTE, WORD, LONG
   - When to use each size
   - Memory efficiency considerations

2. **Chapter: DAT Block Basics**
   - Simple data declarations
   - Arrays and initialization
   - Labels and addressing

3. **Chapter: Hub Memory Access**
   - Simple RDLONG/WRLONG examples
   - Progress to RDWORD/WRWORD, RDBYTE/WRBYTE
   - When to use each size

4. **Chapter: Pointer-Based Access**
   - Using PTRA/PTRB
   - Auto-increment patterns
   - Walking through arrays

5. **Chapter: Working with Spin2 Data**
   - Accessing VAR-declared data from PASM2
   - Understanding structure layout
   - Using SIZEOF() for correct offsets

6. **Chapter: Alignment**
   - Why alignment matters
   - Performance implications
   - When to use ALIGNW/ALIGNL

---

## Spin2 Reference Manual Guidance

### What to Include

Include **complete coverage** of all features from:
- BYTE-WORD-LONG-Usage-Guide.md (Spin2 sections)
- STRUCT-Usage-Guide.md (all content)
- Pointer-Usage-Guide.md (all content)
- FIELD-Operator-Usage-Guide.md (all content)

### Organization Suggestion

1. **Data Types** - BYTE, WORD, LONG declarations and usage
2. **Structures** - STRUCT definition and operations
3. **Pointers** - Typed pointers and operations
4. **Bit Fields** - FIELD operator
5. **Memory Operations** - Built-in functions

---

## Spin2 Tutorial Manual Guidance

### Learning Progression

1. **Chapter: Variables and Types**
   - Choosing BYTE vs WORD vs LONG
   - VAR declarations
   - Local variables

2. **Chapter: Structures**
   - Why use structures
   - Basic STRUCT definition
   - Member access with dot notation
   - Practical examples (coordinates, sensors)

3. **Chapter: Pointers**
   - What pointers are and why use them
   - Typed pointers (`^BYTE`, `^WORD`, `^LONG`)
   - Address-of operator (`@`)
   - Pass-by-reference patterns

4. **Chapter: Advanced Pointers**
   - Structure pointers
   - Pointer arithmetic
   - Array traversal patterns

5. **Chapter: Packed Data with FIELD**
   - When memory efficiency matters
   - Creating field pointers
   - Boolean flag arrays
   - State machine storage

6. **Chapter: Memory Functions**
   - BYTEFILL/WORDFILL/LONGFILL
   - BYTEMOVE/WORDMOVE/LONGMOVE
   - When to use each

---

## Cross-Reference Points

When documenting in one manual, reference the other where appropriate:

### In PASM2 Manuals, Reference Spin2 For:
- "See Spin2 Reference for STRUCT definition syntax"
- "See Spin2 Reference for typed pointer operations"
- "See Spin2 Reference for FIELD operator details"

### In Spin2 Manuals, Reference PASM2 For:
- "See PASM2 Reference for hub memory instruction details"
- "See PASM2 Tutorial for accessing Spin2 data from assembly"
- "See PASM2 Reference for PTRA/PTRB register usage"

---

## Source Documentation

The following guides in the DOCs folder contain the detailed feature documentation:

| Guide | Primary Use |
|-------|-------------|
| `BYTE-WORD-LONG-Usage-Guide.md` | Both PASM2 and Spin2 manuals |
| `STRUCT-Usage-Guide.md` | Primarily Spin2 manuals |
| `Pointer-Usage-Guide.md` | Primarily Spin2 manuals |
| `FIELD-Operator-Usage-Guide.md` | Spin2 manuals only |

---

*This guide was created to assist with manual generation for the PNut-TS Spin2/PASM2 compiler documentation.*
