# Section 2.2 Restructuring Comparison

Three approaches to restructuring Section 2.2 Condition Codes.

---

# APPROACH B-REVISED: Comparison-First

*Principle: Progressive disclosure — what readers need most comes first*

---

## 2.2 Condition Codes (EEEE Field)

The condition field enables conditional execution of any instruction based on the current C and Z flags.

### 2.2.1 Comparison Conditions

After comparing values with CMP (unsigned) or CMPS (signed), use these conditions to test the result:

| Relationship     | Unsigned (CMP) | Signed (CMPS) | Flag State     |
|:-----------------|:---------------|:--------------|:---------------|
| Greater than     | IF_A           | IF_GT         | C=0 AND Z=0    |
| Greater or equal | IF_AE          | IF_GE         | C=0            |
| Less than        | IF_B           | IF_LT         | C=1            |
| Less or equal    | IF_BE          | IF_LE         | C=1 OR Z=1     |
| Equal            | IF_E           | IF_E          | Z=1            |
| Not equal        | IF_NE          | IF_NE         | Z=0            |

**Choosing the Right Comparison:**

| Data Type                 | Use Comparison | Example                              |
|:--------------------------|:---------------|:-------------------------------------|
| Memory addresses          | Unsigned       | `cmp ptr, limit wc` then `if_ae`     |
| Loop counters (0 to N)    | Unsigned       | `cmp count, #MAX wc` then `if_b`     |
| Signed integers           | Signed         | `cmps temp, #0 wc` then `if_lt`      |
| Temperature, position     | Signed         | `cmps delta, #0 wc wz` then `if_ge`  |

```pasm
' Unsigned comparison
        cmp     a, b            wc wz
if_ae   mov     result, #1              ' Unsigned: a >= b

' Signed comparison
        cmps    a, b            wc wz
if_ge   mov     result, #1              ' Signed: a >= b
```

### 2.2.2 The _RET_ Condition

[_RET_ content unchanged — special behavior section]

### 2.2.3 Conditional Execution Patterns

[Pattern examples unchanged]

### 2.2.4 Complete Condition Encoding Reference

For instruction encoding or advanced conditions, the full condition code table:

| EEEE | Mnemonic       | Condition      |
|:-----|:---------------|:---------------|
| 0000 | _RET_          | Always+return  |
| 0001 | IF_NC_AND_NZ   | C=0 AND Z=0    |
| 0010 | IF_NC_AND_Z    | C=0 AND Z=1    |
| 0011 | IF_NC          | C=0            |
| 0100 | IF_C_AND_NZ    | C=1 AND Z=0    |
| 0101 | IF_NZ          | Z=0            |
| 0110 | IF_C_NE_Z      | C≠Z            |
| 0111 | IF_NC_OR_NZ    | C=0 OR Z=0     |
| 1000 | IF_C_AND_Z     | C=1 AND Z=1    |
| 1001 | IF_C_EQ_Z      | C=Z            |
| 1010 | IF_Z           | Z=1            |
| 1011 | IF_NC_OR_Z     | C=0 OR Z=1     |
| 1100 | IF_C           | C=1            |
| 1101 | IF_C_OR_NZ     | C=1 OR Z=0     |
| 1110 | IF_C_OR_Z      | C=1 OR Z=1     |
| 1111 | IF_ALWAYS      | Always         |

**Condition Aliases:**

- **Comparison:** IF_GT, IF_GE, IF_LT, IF_LE (signed); IF_A, IF_AE, IF_B, IF_BE (unsigned)
- **Equality:** IF_E = IF_Z; IF_NE = IF_NZ
- **Flag patterns:** IF_SAME = IF_C_EQ_Z; IF_DIFF = IF_C_NE_Z
- **Bit patterns:** IF_00, IF_01, IF_10, IF_11; IF_0X, IF_1X, IF_X0, IF_X1

---

# APPROACH C-REVISED: Density-First

*Principle: Maximum information per lookup — one table, one callout*

---

## 2.2 Condition Codes (EEEE Field)

The condition field enables conditional execution of any instruction based on the current C and Z flags.

### 2.2.1 Condition Code Table

| EEEE | Condition      | Mnemonic (Aliases)                          |
|:-----|:---------------|:--------------------------------------------|
| 0000 | Always+return  | _RET_                                       |
| 0001 | C=0 AND Z=0    | IF_NC_AND_NZ (IF_GT, IF_A)                  |
| 0010 | C=0 AND Z=1    | IF_NC_AND_Z                                 |
| 0011 | C=0            | IF_NC (IF_GE, IF_AE)                        |
| 0100 | C=1 AND Z=0    | IF_C_AND_NZ                                 |
| 0101 | Z=0            | IF_NZ (IF_NE)                               |
| 0110 | C≠Z            | IF_C_NE_Z (IF_DIFF)                         |
| 0111 | C=0 OR Z=0     | IF_NC_OR_NZ                                 |
| 1000 | C=1 AND Z=1    | IF_C_AND_Z                                  |
| 1001 | C=Z            | IF_C_EQ_Z (IF_SAME)                         |
| 1010 | Z=1            | IF_Z (IF_E)                                 |
| 1011 | C=0 OR Z=1     | IF_NC_OR_Z                                  |
| 1100 | C=1            | IF_C (IF_LT, IF_B)                          |
| 1101 | C=1 OR Z=0     | IF_C_OR_NZ                                  |
| 1110 | C=1 OR Z=1     | IF_C_OR_Z (IF_LE, IF_BE)                    |
| 1111 | Always         | IF_ALWAYS                                   |

> **📋 Comparison Quick Reference**
> 
> After `CMP` (unsigned): IF_A (>), IF_AE (≥), IF_B (<), IF_BE (≤)  
> After `CMPS` (signed): IF_GT (>), IF_GE (≥), IF_LT (<), IF_LE (≤)  
> Either: IF_E (=), IF_NE (≠)

**Additional Aliases:** IF_00 = IF_NC_AND_NZ, IF_01 = IF_NC_AND_Z, IF_10 = IF_C_AND_NZ, IF_11 = IF_C_AND_Z; IF_0X = IF_NC, IF_1X = IF_C, IF_X0 = IF_NZ, IF_X1 = IF_Z; IF_NOT_xx inverts the pattern.

### 2.2.2 The _RET_ Condition

[_RET_ content unchanged — special behavior section]

### 2.2.3 Signed vs. Unsigned Comparisons

The same flag state has different meanings depending on data interpretation:

| Data Type                 | Use Comparison | Example                              |
|:--------------------------|:---------------|:-------------------------------------|
| Memory addresses          | Unsigned       | `cmp ptr, limit wc` then `if_ae`     |
| Loop counters (0 to N)    | Unsigned       | `cmp count, #MAX wc` then `if_b`     |
| Signed integers           | Signed         | `cmps temp, #0 wc` then `if_lt`      |
| Temperature, position     | Signed         | `cmps delta, #0 wc wz` then `if_ge`  |

```pasm
' Unsigned comparison
        cmp     a, b            wc wz
if_ae   mov     result, #1              ' Unsigned: a >= b

' Signed comparison
        cmps    a, b            wc wz
if_ge   mov     result, #1              ' Signed: a >= b
```

### 2.2.4 Conditional Execution Patterns

[Pattern examples unchanged]

---

# APPROACH HYBRID: Comparison-First + Streamlined Encoding

*Principle: Progressive disclosure + high density*

---

## 2.2 Condition Codes (EEEE Field)

The condition field enables conditional execution of any instruction based on the current C and Z flags.

### 2.2.1 Comparison Conditions

After comparing values with CMP (unsigned) or CMPS (signed), use these conditions:

| Relationship     | Unsigned (CMP) | Signed (CMPS) | Condition      |
|:-----------------|:---------------|:--------------|:---------------|
| Greater than     | IF_A           | IF_GT         | C=0 AND Z=0    |
| Greater or equal | IF_AE          | IF_GE         | C=0            |
| Less than        | IF_B           | IF_LT         | C=1            |
| Less or equal    | IF_BE          | IF_LE         | C=1 OR Z=1     |
| Equal            | IF_E           | IF_E          | Z=1            |
| Not equal        | IF_NE          | IF_NE         | Z=0            |

| Data Type                 | Use      | Example                              |
|:--------------------------|:---------|:-------------------------------------|
| Memory addresses, counters| Unsigned | `cmp ptr, limit wc` then `if_ae`     |
| Signed integers, deltas   | Signed   | `cmps temp, #0 wc` then `if_lt`      |

```pasm
' Unsigned comparison
        cmp     a, b            wc wz
if_ae   mov     result, #1              ' Unsigned: a >= b

' Signed comparison
        cmps    a, b            wc wz
if_ge   mov     result, #1              ' Signed: a >= b
```

### 2.2.2 Complete Condition Reference

All 16 condition codes with primary mnemonic and common aliases:

| EEEE | Condition      | Primary        | Comparison Alias |
|:-----|:---------------|:---------------|:-----------------|
| 0000 | Always+return  | _RET_          | —                |
| 0001 | C=0 AND Z=0    | IF_NC_AND_NZ   | IF_GT, IF_A      |
| 0010 | C=0 AND Z=1    | IF_NC_AND_Z    | —                |
| 0011 | C=0            | IF_NC          | IF_GE, IF_AE     |
| 0100 | C=1 AND Z=0    | IF_C_AND_NZ    | —                |
| 0101 | Z=0            | IF_NZ          | IF_NE            |
| 0110 | C≠Z            | IF_C_NE_Z      | —                |
| 0111 | C=0 OR Z=0     | IF_NC_OR_NZ    | —                |
| 1000 | C=1 AND Z=1    | IF_C_AND_Z     | —                |
| 1001 | C=Z            | IF_C_EQ_Z      | —                |
| 1010 | Z=1            | IF_Z           | IF_E             |
| 1011 | C=0 OR Z=1     | IF_NC_OR_Z     | —                |
| 1100 | C=1            | IF_C           | IF_LT, IF_B      |
| 1101 | C=1 OR Z=0     | IF_C_OR_NZ     | —                |
| 1110 | C=1 OR Z=1     | IF_C_OR_Z      | IF_LE, IF_BE     |
| 1111 | Always         | IF_ALWAYS      | —                |

**Additional Aliases:** IF_SAME = IF_C_EQ_Z, IF_DIFF = IF_C_NE_Z; Bit patterns: IF_00/01/10/11, IF_0X/1X/X0/X1, IF_NOT_xx.

### 2.2.3 The _RET_ Condition

[_RET_ content unchanged — special behavior section]

### 2.2.4 Conditional Execution Patterns

[Pattern examples unchanged]

---

# COMPARISON SUMMARY

| Aspect | B-Revised | C-Revised | Hybrid |
|--------|-----------|-----------|--------|
| **First thing reader sees** | Comparison table | Full encoding table | Comparison table |
| **Encoding table location** | End (§2.2.4) | First (§2.2.1) | Second (§2.2.2) |
| **Alias presentation** | Prose list at end | Inline + prose | Dedicated column |
| **Total tables** | 4 | 2 | 3 |
| **Comparison lookup** | Immediate | Via callout | Immediate |
| **EEEE lookup** | Scroll to end | Immediate | One section down |
| **Progressive disclosure** | ✅ Strong | ❌ Weak | ✅ Strong |
| **Information density** | Medium | High | High |
| **Redundancy** | Low | Low | Low |

---

*File: section-2.2-comparison.md*
*Purpose: Visual comparison for restructuring decision*
