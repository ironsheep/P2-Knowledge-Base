# Comprehensive Screenshot Requirements for All Documents
*Complete list of tables, diagrams, and sections needing screenshots*
*Date: 2025-08-15*

## 📘 SPIN2 DOCUMENTATION v51 (Priority: CRITICAL)

### Operator Tables
1. **Main Operators Table** (likely pages 10-15)
   - Title: "Operators" or "Spin2 Operators"
   - Should show all unary, binary, ternary operators
   - Need: Operator symbols, descriptions, examples

2. **Operator Precedence Table** (CRITICAL)
   - Title: "Operator Precedence" or "Precedence Levels"
   - Should show 16 levels of precedence
   - Need: Level numbers, operator groups at each level

3. **Floating-Point Operators Table**
   - Title: "Floating-Point Operators" or contains "Float"
   - Need: All operators ending in dot (.)
   - Includes: +., -., *., /., FSQRT., etc.

4. **Assignment Operators Table**
   - Title: "Assignment Operators" 
   - Need: :=, +=, -=, *=, /=, etc.
   - May be part of main operators table

### Control Flow Sections
5. **IF/IFNOT/ELSE/ELSEIF Statement**
   - Title: "IF Statement" or "Conditional Execution"
   - Need: Complete syntax, examples
   - Including: ELSEIF, ELSEIFNOT variations

6. **CASE/CASE_FAST Statement**
   - Title: "CASE Statement" or "CASE/CASE_FAST"
   - Need: Syntax, OTHER clause, range syntax
   - Difference between CASE and CASE_FAST

7. **REPEAT Statement Varieties**
   - Title: "REPEAT" or "Loop Statements"
   - Need: REPEAT, REPEAT WHILE, REPEAT UNTIL
   - Also: REPEAT FROM/TO/STEP syntax
   - NEXT and QUIT usage

8. **ABORT Statement**
   - Title: "ABORT" 
   - Need: ABORT with and without values
   - Trap handling

### Built-in Methods Tables
9. **COG Management Methods**
   - Title: "COG Methods" or contains "COGINIT"
   - Need: COGINIT, COGSTOP, COGID, COGCHK
   - Parameter details, return values

10. **Memory Operation Methods**
    - Title: "Memory Methods" or contains "BYTEMOVE"
    - Need: BYTEMOVE, WORDMOVE, LONGMOVE
    - Also: BYTEFILL, WORDFILL, LONGFILL
    - STRSIZE, STRCOMP methods

11. **Pin I/O Methods**
    - Title: "Pin Methods" or "Pin I/O"
    - Need: PINWRITE, PINREAD, PINSTART, PINCLEAR
    - Pin group operations
    - Smart pin integration methods

12. **Math Methods Table**
    - Title: "Math Methods" or "Math Functions"
    - Need: All built-in math functions
    - Including: GETRND, ROTXY, POLXY, XYPOL

13. **String Methods Table**
    - Title: "String Methods" or contains "STRING"
    - Need: String manipulation functions
    - Format specifiers

### Special Features
14. **DEBUG Display Types Table**
    - Title: "DEBUG Displays" or "DEBUG Windows"
    - Need: TERM, SCOPE, LOGIC, PLOT, FFT, etc.
    - Parameters for each display type

15. **Structure Definition Syntax**
    - Title: "STRUCT" or "Structures"
    - Need: STRUCT definition and usage
    - Member access syntax

16. **Inline PASM Rules/Restrictions**
    - Title: "Inline Assembly" or "ORG/ORGH"
    - Need: Rules for inline PASM2
    - Register usage, limitations

## 📙 SILICON DOCUMENTATION v35 (Priority: HIGH)

### Architecture Diagrams
17. **P2 Block Diagram**
    - Title: "P2 Architecture" or "Block Diagram"
    - Need: Overall chip architecture
    - COG/Hub/Smart Pin relationships

18. **COG Block Diagram**
    - Title: "COG Architecture" or "COG Block Diagram"
    - Need: Internal COG structure
    - ALU, registers, memory paths

19. **Hub Memory Map**
    - Title: "Hub Memory" or "Memory Map"
    - Need: Memory regions, addresses
    - Boot areas, debug areas

### Timing Tables
20. **Instruction Timing Table**
    - Title: "Instruction Timing" or "Clock Cycles"
    - Need: Cycles per instruction category
    - Hub timing effects

21. **Hub Slot Timing Diagram**
    - Title: "Egg Beater" or "Hub Timing"
    - Need: COG-to-hub access pattern
    - Window alignment

### Boot Process
22. **Boot Sequence Diagram/Table**
    - Title: "Boot Process" or "Boot Sequence"
    - Need: Complete boot flow
    - Decision points, device checks

23. **Boot Device Priority Table**
    - Title: "Boot Priority" or "Boot Devices"
    - Need: Order of device checking
    - Protocols for each device

### Event System
24. **Event Routing Matrix**
    - Title: "Events" or "Event Sources"
    - Need: All 16 event sources
    - COG routing possibilities

25. **Interrupt Priority Diagram**
    - Title: "Interrupts" or "Interrupt Priority"
    - Need: INT1/INT2/INT3/DEBUG priorities
    - Stacking behavior

### Special Features
26. **CORDIC Operations Table**
    - Title: "CORDIC" or "CORDIC Functions"
    - Need: All CORDIC operations
    - Command encoding, timing

27. **Streamer Modes Table**
    - Title: "Streamer" or "Streamer Modes"
    - Need: All streamer modes
    - Configuration details

28. **Smart Pin Mode Summary Table**
    - Title: "Smart Pin Modes" or "Pin Modes"
    - Need: All 32 modes listed
    - Basic parameters for each

## 📗 PASM2 MANUAL (Priority: MEDIUM)

### Instruction Tables
29. **Instruction Categories Table**
    - Title: "Instruction Categories" or "Instruction Groups"
    - Need: How instructions are organized
    - Category descriptions

30. **Flag Effects Table**
    - Title: "Flag Effects" or "C and Z Flags"
    - Need: Which instructions affect flags
    - How flags are modified

31. **Conditional Execution Table**
    - Title: "Conditions" or "Conditional Execution"
    - Need: All condition codes
    - When they're true/false

### Any Remaining Instructions
32. **Any instruction description pages not yet extracted**
    - Need: Complete instruction descriptions
    - Especially for the ~300 undocumented ones

## 📕 SMART PINS DOCUMENTATION (Priority: LOW - mostly complete)

### Mode Details
33. **Remaining Smart Pin Mode Tables** (modes 11-32)
    - Title: Individual mode titles
    - Need: Complete mode descriptions
    - X/Y/Z parameter usage

34. **Smart Pin Timing Diagrams**
    - Title: Any timing diagrams
    - Need: Setup/hold times
    - Synchronization details

## 📓 DATA SHEET / SPEC SHEET (If they exist)

35. **Electrical Specifications Table**
    - Title: "Electrical Specifications" or "Absolute Maximum Ratings"
    - Need: Voltage, current, temperature ranges

36. **AC/DC Characteristics Tables**
    - Title: "AC Characteristics" or "DC Characteristics"
    - Need: Timing specs, drive strengths

37. **Package Information**
    - Title: "Package" or "Mechanical"
    - Need: Dimensions, pinout

## 🎯 PRIORITY ORDER FOR SCREENSHOTS

### Must Have (Enables v1.0):
1. Spin2 Operator Precedence Table (#2)
2. Spin2 Complete Operators Table (#1)
3. Spin2 Control Flow Statements (#5-8)
4. Spin2 Built-in Methods (#9-13)

### Should Have (Improves quality):
5. Silicon Boot Process (#22-23)
6. Silicon Timing Tables (#20-21)
7. PASM2 Instruction Descriptions (#32)

### Nice to Have (Completeness):
8. Architecture Diagrams (#17-19)
9. Event/Interrupt Tables (#24-25)
10. Remaining Smart Pin Modes (#33-34)

## 📝 SCREENSHOT NAMING CONVENTION

Please name screenshots as:
`[doc]-[page#]-[title].png`

Examples:
- `spin2-p12-operator-precedence.png`
- `silicon-p24-boot-sequence.png`
- `pasm2-p45-instruction-add.png`

## ✅ CHECKLIST FORMAT

When providing screenshots, a simple list like:
```
✓ spin2-p12-operator-precedence.png - Operator Precedence Table
✓ spin2-p13-operators-complete.png - All Operators Table
✓ spin2-p20-if-statement.png - IF/ELSE syntax
```

This will help track what's been captured.

---

*This comprehensive list should allow one-pass screenshot collection*