# Instructions: Z

This section contains all PASM2 instructions beginning with the letter Z. There is currently one Z instruction: ZEROX for zero extension.



::: instrheader
## ZEROX {#zerox}
Zero Extend

[Math and Logic](instruction-categories.md#math-and-logic) - Zero-extends a value above the specified bit position.
:::

**ZEROX**  *Dest, {#}Src*  **{WC/WZ/WCZ}**

---

**Result:** Dest is zero-extended above the bit indicated by Src[4:0]. Optionally sets C to MSB of result and Z if result equals zero.

- Dest is the register containing the value to zero-extend.
- Src is a register or 9-bit literal identifying the bit position (0-31) beyond which to zero-extend.
- WC sets C to the MSB (bit 31) of the result.
- WZ sets Z if the result equals zero.
- WCZ sets both C and Z.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0111010 | CZI | DDDDDDDDD | SSSSSSSSS | D | MSB | Zero | 2 |


**Related:** [SIGNX](instructions-s.md#signx)

**Explanation:**

ZEROX fills the bits of Dest, above the bit indicated by Src[4:0], with zeros, effectively zero-extending the value. This is useful when converting encoded or received unsigned values from a smaller bit width to 32 bits.

For example, if Dest contains $FFFF_FFFF and Src contains 7, ZEROX clears bits 31 down to bit 8, leaving only bits 7-0 intact. The result in Dest becomes $0000_00FF.

The instruction examines only the lower 5 bits of Src (Src[4:0]), allowing bit positions 0 through 31 to be specified. This makes ZEROX particularly useful for extracting and zero-extending bit fields from packed data structures or network protocols.

::: pasm2
        ' Extract lower byte and zero-extend
        MOV     data, big_value
        ZEROX   data, #7         ' Keep bits 7-0, clear bits 31-8
                                 ' If big_value was $FFFF_FFFF,
                                 ' data becomes $0000_00FF
:::

ZEROX is the complement to SIGNX. While ZEROX fills upper bits with zeros (for unsigned values), SIGNX fills upper bits with the value of the designated bit (for signed values). Use ZEROX when working with unsigned data, and SIGNX when working with signed data that needs proper sign extension.

