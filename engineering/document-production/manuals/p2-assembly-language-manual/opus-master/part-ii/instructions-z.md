# Z Instructions

This section covers PASM2 instructions beginning with the letter Z.

---

## ZEROX — Math and Logic

Zero extend.

### Syntax
```pasm
        ZEROX   D, {#}S         {WC|WZ|WCZ}
```

### Result
The D value is zero-extended above the bit indicated by S and is stored in D. Optionally the C and Z flags are updated.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Register containing the value to zero-extend above bit S[4:0]. The result is written here. |
| S | Register or 9-bit literal whose value (lower 5 bits) identifies the bit of D to zero-extend beyond. |
| WC/WZ/WCZ | Optional effects to update flags. |

### Encoding
\simpleencoding{EEEE 0111010 CZI DDDDDDDDD SSSSSSSSS | D | MSB of result | Result = 0 | 2}

### Flags Affected
- **C**: Set to MSB of result (if WC or WCZ specified)
- **Z**: Set if result equals zero (if WZ or WCZ specified)

### Related Instructions
- [SIGNX](#signx) — Sign-extend value beyond designated bit

### Explanation
ZEROX fills the bits of D, above the bit indicated by S[4:0], with zeros, effectively zero-extending the value. This is handy when converting encoded or received unsigned values from a small bit width to a large bit width (32 bits).

For example, if D contains `$FFFF_FFFF` and S contains 7, ZEROX clears bits 31 down to bit 8, leaving only bits 7-0 intact. The result in D becomes `$0000_00FF`.

The instruction examines only the lower 5 bits of S (S[4:0]), allowing bit positions 0 through 31 to be specified. This makes ZEROX particularly useful for extracting and zero-extending bit fields from packed data structures or network protocols.

If the WC or WCZ effect is specified, the C flag is set to the result's MSB value (bit 31). If the WZ or WCZ effect is specified, the Z flag is set if the result is zero, or cleared if it is non-zero.

ZEROX is the complement to SIGNX. While ZEROX fills upper bits with zeros (for unsigned values), SIGNX fills upper bits with the value of the designated bit (for signed values). Use ZEROX when working with unsigned data, and SIGNX when working with signed data that needs proper sign extension.

### Example
```pasm
        ' Extract lower byte and zero-extend
        MOV     data, big_value
        ZEROX   data, #7        ' Keep bits 7-0, clear bits 31-8
                                ' If big_value was $FFFF_FFFF,
                                ' data becomes $0000_00FF
```
