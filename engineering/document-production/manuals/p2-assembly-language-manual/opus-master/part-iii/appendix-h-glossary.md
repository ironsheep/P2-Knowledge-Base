# Appendix H: Glossary of Encoding Terms

This glossary defines the terms used throughout the instruction encoding tables, syntax descriptions, and opcode documentation in this manual.


## Encoding Field Terms

**A / Addr**
: A 20-bit relative or absolute value used to change PC (the program counter). This field appears in branch and call instructions where the destination spans both the D and S fields of the instruction word.

**C / Carry Flag**
: A 1-bit persistent flag value representing a special state before or after instruction execution. Traditionally, the C flag indicates that an arithmetic operation resulted in a carry (addition) or borrow (subtraction). The P2 extends this with instruction-specific meanings for both input and output. When C appears in an instruction's opcode encoding, it indicates optional flag writing governed by the WC or WCZ effect.

**CZI / FX Field**
: The three bits at positions 20-18 in the instruction word. Bit 20 (C) enables writing to the C flag. Bit 19 (Z) enables writing to the Z flag. Bit 18 (I) indicates immediate mode for the S operand. Some instructions repurpose these bits for other functions, documented in the FX column of opcode tables.

**D / Dest / Destination**
: The target register that an instruction ultimately affects. Usually a 9-bit register address (0-511), but may be a 32-bit augmented value when preceded by an AUGD instruction. The destination register is often read, manipulated, and overwritten during instruction execution. The final value written is also called the Result.

**EEEE / Condition Field**
: The four bits at positions 31-28 that specify the execution condition. Default value 1111 means "always execute." Other values test combinations of C and Z flags—the instruction executes only if the condition is true.


## Flag and State Terms

**H / Hub Long**
: A Hub RAM long (4 bytes) used to store subroutine calling context states. This includes the C and Z flags plus the return address, allowing nested subroutine calls to preserve and restore processor state.

**I / Immediate Flag**
: When set (I=1), the S field contains a literal value rather than a register address. When clear (I=0), the S field is a register address and the instruction reads from that register. The `#` prefix in source code sets this bit.

**K / Stack**
: The 8-level hardware stack used for subroutine calls and temporary storage. On CALL, the stack stores C, Z, and PC (return address). PUSH and POP provide general-purpose 32-bit value storage. Stack overflow/underflow wraps silently—there is no trap or error indication.

**L / Literal Flag**
: When set (L=1), the D field contains a literal value rather than a register address. This is less common than immediate S operands and appears in specific instructions. The `#` prefix on the destination in source code sets this bit where valid.

**N / Index Number**
: A small index value (typically 0-1, 0-3, or 0-7) used as a third operand in some instructions. Examples include interrupt numbers (0-3), event selector indices, and bit position specifiers.

**PC / Program Counter**
: A dedicated internal register that determines the next instruction address. Automatically increments by 1 (COG/LUT execution) or 4 (Hub execution) after each instruction unless altered by a branch. Not directly accessible but affected by JMP, CALL, RET, and conditional branches.

**R / Relative Flag**
: When set (R=1), the address field is interpreted relative to the current PC. When clear (R=0), the address is absolute. Relative addressing enables position-independent code. The `\` prefix forces absolute addressing; its absence allows relative.

**Result**
: The value written at the end of instruction execution. Usually stored in the Destination register, but some instructions write to special registers or memory instead. The Result value determines the Z flag when WZ is specified.

**Z / Zero Flag**
: A 1-bit persistent flag value traditionally indicating that an operation produced a zero result. The P2 extends this with instruction-specific meanings. When Z appears in an instruction's opcode encoding, it indicates optional flag writing governed by the WZ or WCZ effect. The Z flag is also used for equality testing in comparisons.


## Operand Terms

**S / Src / Source**
: The origin value that instructions operate with. Can be a 9-bit literal value (when I=1), a register address (when I=0), or a 32-bit augmented value (when preceded by AUGS or the `##` prefix). The S field occupies bits 8-0 of the instruction word.

**W / Write Register**
: A 2-bit field (values 00-11) that selects which special register to write in certain instructions. The values map to PA (00), PB (01), PTRA (10), and PTRB (11). This appears in instructions that can target pointer registers.


## Opcode Table Columns

| Column | Description |
|--------|-------------|
| COND | Bits 31-28: Execution condition (EEEE pattern) |
| INSTR | Bits 27-21: Instruction opcode (7 bits) |
| FX | Bits 20-18: Flag effects and immediate mode (CZI or special) |
| DEST | Bits 17-9: Destination operand (9 bits) |
| SRC | Bits 8-0: Source operand (9 bits) |
| Write | What the instruction modifies (register, memory, flags) |
| C Flag | How the C flag is affected (if WC specified) |
| Z Flag | How the Z flag is affected (if WZ specified) |
| Clocks | Execution time in system clock cycles |


## Related Documentation

- **Chapter 2** — Detailed explanation of instruction encoding format
- **Chapter 3** — Complete coverage of flag behavior and conditional execution
- **Appendix A** — Encoding summary tables
- **Appendix H** — Complete opcode bit patterns for all instructions


