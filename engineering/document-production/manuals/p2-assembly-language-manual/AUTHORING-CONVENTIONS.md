# PASM2 Manual - Markdown Authoring Conventions

**Purpose:** Comprehensive authoring guide for generating consistent instruction entries in Parallax format.

**Audience:** Claude instances generating Part II content for the P2 Assembly Language Manual.

---

## 1. Entry Structure Overview

Every instruction entry follows this exact structure:

```
## INSTRUCTION_NAME {#instruction-name}

Short description
[Category](#category-anchor) - One-line summary.

```
SYNTAX LINE(S)
```

**Operation:** `pseudocode`  ← OPTIONAL — only where the result/flag formula is non-obvious (see §1.1)

**Result:** Single sentence describing the outcome.

- Parameter 1 description
- Parameter 2 description
- Effects description (if applicable)

```{=latex}
\simpleencoding{...} or \begin{encodingtable}...\end{encodingtable}
```

**Related:** [INSTR1](#instr1), [INSTR2](#instr2)

**Explanation:**

Prose paragraphs...

---
```

---

## 1.1 The Operation Line (curated pseudocode)

Directly after the syntax line (before **Result:**), an entry MAY carry an
`**Operation:**` line: a compact, backticked pseudocode summary of the result
and any non-default flag effects.

**Add it only where it earns its place** — where the result/flag formula is not
obvious from the mnemonic + syntax + one-line summary (bit-field shuffles,
slice-indexed ops, signed/scaled math, non-obvious flag derivations, pixel ops,
ALT next-instruction side-effects, encode/decode/CRC), or where the flag effects
are non-default even when the value is obvious. Plain whole-register ops
(MOV/ADD/SUB/AND/OR/CMP/NOP) do not get one.

**Format:** result first, then C, then Z, separated by `; `; each expression in
backticks. Example:

```
**Operation:** `D = signed(D[15:0] × S[15:0])`; `Z = (S==0 OR D==0)`
```

**Source:** the Parallax instruction CSV (`P2 Instructions v35`, column 5),
cross-checked against Appendix C / the P2KB YAML. Reformat the notation only —
never invent semantics. See `voice-guide.md` §6.3.

---

## 2. Header Block

### 2.1 Instruction Name Heading

```markdown
## ADD {#add}
```

- Use H2 (`##`) for all instruction entries
- Include anchor in braces: `{#lowercase-name}`
- For instruction families: `## DIRZ / DIRNZ {#dirz}`

### 2.2 Short Description Line

```markdown
Add
```

- Human-readable verb or noun phrase
- Capitalized first word
- No period at end
- Examples: "Add", "Compare unsigned", "Jump if zero", "Set byte"

### 2.3 Category and One-Liner

```markdown
[Math Instruction](#math-instructions) - Add two unsigned values.
```

- Category is hyperlinked to Part I or Appendix B
- Hyphen separator (space-hyphen-space)
- One sentence summary ending with period
- Third person, present tense

**Valid Categories:**
- Math Instruction
- Logic Instruction
- Shift/Rotate Instruction
- Branch/Jump Instruction
- I/O Pin Instruction
- Smart Pin Instruction
- CORDIC Instruction
- Hub Memory Instruction
- COG Control Instruction
- LUT Instruction
- Streamer Instruction
- Event Instruction
- Flag Instruction
- Debug Instruction
- Misc Instruction

---

## 3. Syntax Block

### 3.1 Basic Format

```markdown
```
ADD  Dest, {#}Src  {WC|WZ|WCZ}
```
```

- Use triple backticks with no language tag
- Uppercase instruction mnemonic
- Two spaces between mnemonic and first operand
- Comma-space between operands
- Two spaces before effects

### 3.2 Notation Standards

| Notation | Meaning |
|----------|---------|
| `Dest` | Destination register |
| `Src` | Source operand |
| `{#}` | Optional immediate prefix |
| `{#}Src` | Src can be register or immediate |
| `#Src` | Src must be immediate |
| `{WC\|WZ\|WCZ}` | Optional flag effects |
| `{WC}` | Only WC effect available |

### 3.3 Multiple Syntax Forms

When an instruction has multiple forms, show each on its own line:

```markdown
```
GETBYTE  Dest, {#}Src, #Num  {WC|WZ|WCZ}
GETBYTE  Dest                {WC|WZ|WCZ}
```
```

---

## 4. Result Line

```markdown
**Result:** Sum of unsigned Src and unsigned Dest is stored in Dest.
```

- Bold "Result:" label
- Single sentence
- States the primary outcome
- Uses canonical terms (Dest, Src, not "destination" or "source")
- Present tense, third person

---

## 5. Parameters Section

```markdown
- Dest is a register containing the value to add Src to, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is added into Dest.
- WC, WZ, or WCZ are optional effects to update flags.
```

- Use dash-space bullet format
- Each parameter on its own bullet
- Describe what the parameter is and its constraints
- Always include effects bullet if WC/WZ/WCZ are available

### 5.1 Standard Parameter Descriptions

**Dest patterns:**
- "Dest is a register containing..." (when read and written)
- "Dest is a register where the result is written." (when only written)
- "Dest is a register specifying..." (when used as configuration)

**Src patterns:**
- "Src is a register or 9-bit literal..." (basic immediate)
- "Src is a register, 9-bit literal, or 32-bit augmented literal..." (supports ##)
- "Src is a register containing..." (register only)

**Effects pattern:**
- "WC, WZ, or WCZ are optional effects to update flags."

---

## 6. Encoding Table

### 6.1 Single-Row Encoding (Most Common)

Use `\simpleencoding{}` for instructions with one encoding:

```markdown
```{=latex}
\simpleencoding{EEEE}{0001000}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{carry of (D + S)}{Result = 0}{2}
```
```

**Arguments (9 total):**
1. COND - Usually `EEEE`
2. INSTR - 7-bit opcode (e.g., `0001000`)
3. FX - Flag/immediate bits (e.g., `CZI`, `NNI`, `00I`)
4. DEST - Usually `DDDDDDDDD`
5. SRC - Usually `SSSSSSSSS` or fixed value
6. Write - What's written (e.g., `D`, `D and PC`, `---`)
7. C Flag - C behavior or `---` for no change
8. Z Flag - Z behavior or `---` for no change
9. Clocks - Cycle count

### 6.2 Multi-Row Encoding

Use `\begin{encodingtable}` with `\encodingrow{}` and `\encodingrowcont{}`:

```markdown
```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1000111}{NNI}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{2}
\encodingrow{EEEE}{1000111}{000}{DDDDDDDDD}{000000000}{D}{---}{---}{2}
\end{encodingtable}
```
```

- `\encodingrowcont{}` - Row WITHOUT bottom border (for middle rows)
- `\encodingrow{}` - Row WITH bottom border (for last row)

### 6.3 When to Use Multi-Row

1. **Multiple syntax forms** with different encodings:
   - GETBYTE with Src,Num vs GETBYTE alone

2. **Instruction families** documented together:
   - DIRZ / DIRNZ sharing an entry
   - JCT1/JCT2/JCT3/JNCT1/JNCT2/JNCT3

3. **Related instructions** sharing documentation:
   - TESTB / TESTBN as a pair

### 6.4 Encoding Field Reference

| Field | Common Values | Notes |
|-------|---------------|-------|
| COND | `EEEE` | Always EEEE for conditional instructions |
| FX | `CZI` | C/Z modifiable, immediate allowed |
| FX | `0ZI` | C not modifiable |
| FX | `C0I` | Z not modifiable |
| FX | `NNI` | NN encodes sub-function (GETBYTE, etc.) |
| FX | `00I` | No flag modification |
| Write | `D` | Dest is written |
| Write | `D and PC` | Dest and PC written (jumps) |
| Write | `---` | Nothing written |
| C/Z | `---` | No change to flag |

---

## 7. Related Line

```markdown
**Related:** [ADDX](#addx), [ADDS](#adds), [ADDSX](#addsx), [SUB](#sub)
```

- Bold "Related:" label
- Comma-separated hyperlinks
- Each instruction linked to its anchor
- Order: Most closely related first
- Typically 3-6 related instructions

### 7.1 What to Include

- **Same family:** ADD → ADDX, ADDS, ADDSX
- **Opposite operation:** ADD → SUB
- **Similar purpose:** CMP → CMPS, CMPX, CMPSX
- **Prerequisites:** RDFAST → SETQ (for burst mode)
- **Alternatives:** WAITX → WAITCNT, WAITMS

---

## 8. Explanation Section

```markdown
**Explanation:**

ADD sums the two unsigned values of Dest and Src together and stores the result into the Dest register.

If the WC or WCZ effect is specified, the C flag is set (1) if the summation results in a 32-bit overflow (unsigned carry), or is cleared (0) if no overflow. This indicates that the result exceeded the maximum unsigned 32-bit value of $FFFF_FFFF.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result of Dest + Src equals zero, or is cleared (0) if it is non-zero.

To add unsigned multi-long values (64-bit or larger), use ADD for the least significant long, then ADDX for each subsequent long. ADDX carries the overflow from the previous addition into the current one. For example, to add two 64-bit values:

```pasm
        add     value_lo, addend_lo  wc    ' Add low longs, capture carry
        addx    value_hi, addend_hi        ' Add high longs with carry-in
```

ADD and ADDX are also used for adding signed multi-long values, with ADDSX ending the sequence to properly handle sign extension.
```

### 8.1 Structure Guidelines

1. **Opening paragraph:** Basic operation description
2. **C flag paragraph:** (if applicable) Dedicated paragraph for C flag behavior
3. **Z flag paragraph:** (if applicable) Dedicated paragraph for Z flag behavior
4. **Usage context:** When/why to use this instruction
5. **Examples:** Embedded in prose where they illuminate

### 8.2 Code Examples in Explanation

Use `pasm` language tag for code blocks:

```markdown
```pasm
        add     value_lo, addend_lo  wc    ' Add low longs, capture carry
        addx    value_hi, addend_hi        ' Add high longs with carry-in
```
```

**Formatting rules:**
- 8 spaces for label column (or instruction if no label)
- 8 characters for mnemonic column
- Operands with proper spacing
- Comments start with `'` (single quote)
- Align comments when multiple lines

---

## 9. Voice Guide Compliance

### 9.1 Required Voice

- **Third person only:** "The instruction adds..." not "You add..."
- **Present tense:** "The C flag is set..." not "The C flag will be set..."
- **Active voice preferred:** "ADD stores the result" not "The result is stored by ADD"
- **Definitive statements:** "The C flag is set if..." not "The C flag may be set if..."

### 9.2 Forbidden Patterns

| Don't Write | Write Instead |
|-------------|---------------|
| "You should use..." | "Use..." or "The typical approach is..." |
| "This will add..." | "This adds..." |
| "probably", "typically" | State the exact condition |
| "similar to ADD" | "Like ADD, this instruction..." |
| "basically" | (omit entirely) |
| "Let's explore..." | (inappropriate for reference) |

### 9.3 Terminology Consistency

| Use | Not |
|-----|-----|
| C flag | carry flag, C, carry |
| Z flag | zero flag, Z, zero |
| COG | cog, Cog |
| Hub | hub, HUB |
| LUT | lut, Lut |
| register | location, address |
| immediate | literal, constant |
| effect | modifier, flag effect |

---

## 10. Separator Line

End each entry with a horizontal rule:

```markdown
---
```

This provides visual separation between entries.

---

## 11. Copy-Paste Templates

### 11.1 Single-Encoding Instruction Template

```markdown
## INSTR {#instr}

Short description
[Category](#category) - One-line summary.

```
INSTR  Dest, {#}Src  {WC|WZ|WCZ}
```

**Result:** [What happens].

- Dest is a register [description].
- Src is a register, 9-bit literal, or 32-bit augmented literal [description].
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\simpleencoding{EEEE}{OPCODE}{CZI}{DDDDDDDDD}{SSSSSSSSS}{D}{C description}{Z description}{CLOCKS}
```

**Related:** [RELATED1](#related1), [RELATED2](#related2)

**Explanation:**

[Operation description paragraph.]

If the WC or WCZ effect is specified, the C flag is set (1) if [condition], or is cleared (0) if [opposite condition].

If the WZ or WCZ effect is specified, the Z flag is set (1) if [condition], or is cleared (0) if [opposite condition].

[Usage context and examples if helpful.]

---
```

### 11.2 Multi-Encoding Instruction Template

```markdown
## INSTR {#instr}

Short description
[Category](#category) - One-line summary.

```
INSTR  Dest, {#}Src, #Num  {WC|WZ|WCZ}
INSTR  Dest                {WC|WZ|WCZ}
```

**Result:** [What happens].

- Dest is a register [description].
- Src is a register or 9-bit literal [description].
- Num is a 2-bit value [description].
- WC, WZ, or WCZ are optional effects to update flags.

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{OPCODE1}{NNI}{DDDDDDDDD}{SSSSSSSSS}{D}{---}{---}{2}
\encodingrow{EEEE}{OPCODE2}{000}{DDDDDDDDD}{000000000}{D}{---}{---}{2}
\end{encodingtable}
```

**Related:** [RELATED1](#related1), [RELATED2](#related2)

**Explanation:**

[Operation description for first syntax form.]

[Operation description for second syntax form.]

---
```

### 11.3 Instruction Family Template

```markdown
## DIRZ / DIRNZ {#dirz}

Set pin direction if Z/not Z
[I/O Pin Instruction](#io-pin-instructions) - Conditionally set pin direction based on Z flag.

```
DIRZ   {#}Dest
DIRNZ  {#}Dest
```

**Result:** Pin direction is set to output if condition met.

- Dest is a register or 6-bit literal specifying the pin number (0-63).

```{=latex}
\begin{encodingtable}
\encodingrowcont{EEEE}{1101011}{CZI}{DDDDDDDDD}{001000100}{DIRx}{Orig DIRx base bit}{Orig DIRx base bit}{2}
\encodingrow{EEEE}{1101011}{CZI}{DDDDDDDDD}{001000101}{DIRx}{Orig DIRx base bit}{Orig DIRx base bit}{2}
\end{encodingtable}
```

**Related:** [DIRC](#dirc), [DIRNC](#dirnc), [DIRL](#dirl), [DIRH](#dirh)

**Explanation:**

DIRZ and DIRNZ conditionally set a pin's direction based on the current Z flag state.

DIRZ sets the pin specified by Dest to output mode if the Z flag is set (1). If Z is clear (0), the pin direction is unchanged.

DIRNZ sets the pin specified by Dest to output mode if the Z flag is clear (0). If Z is set (1), the pin direction is unchanged.

---
```

---

## 12. Directive Entry Format

Directives differ from instructions - no encoding table, different structure:

```markdown
## ORG {#org}

Set origin
Directive - Set the assembly origin address within COG memory.

```
DAT
        ORG   address
        ' assembly code here
```

**Result:** Subsequent instructions assemble starting at the specified address.

- address is an optional COG address (0-$1FF). If omitted, defaults to 0.

**Related:** [ORGH](#orgh), [FIT](#fit)

**Explanation:**

ORG sets the assembly origin for COG-resident code. All subsequent instructions are assembled as if they will execute at the specified address.

The address must be within COG memory range (0-$1FF, or 0-511 decimal). If address is omitted, ORG defaults to 0.

ORG is used when writing code that will be loaded into a COG for execution. The assembler uses this address to calculate relative jumps and to verify code fits within COG memory.

---
```

**Key differences:**
- No encoding table
- Syntax shown in DAT context
- No flag effects
- May include memory diagrams (TikZ)

---

## 13. Special Cases

### 13.1 Instructions with Footnotes

When encoding table needs footnotes for conditional behaviors:

```markdown
```{=latex}
\begin{encodingtable}
\encodingrow{EEEE}{1011110}{01I}{000000001}{SSSSSSSSS}{PC\textsuperscript{1}}{---}{---}{2 or 4 / 2 or 13-20}
\end{encodingtable}

\textsuperscript{1} PC is written only when the counter event flag is set.
```
```

### 13.2 Complex Clock Cycles

Some instructions have variable timing:

| Pattern | Meaning |
|---------|---------|
| `2` | Always 2 clocks |
| `2+` | 2 clocks minimum, may be more |
| `2 or 4` | 2 clocks if not taken, 4 if taken (branches) |
| `2 / 8-23` | 2 in COG, 8-23 in Hub |
| `9..35` | Range depending on operands |

### 13.3 Escaping Special Characters

In LaTeX passthrough blocks, escape these characters:
- `#` → `\#` (in text, not in encoding values)
- `%` → `\%`
- `&` → `\&`
- `_` → `\_`
- `{` → `\{` (when literal, not when LaTeX command)
- `}` → `\}` (when literal, not when LaTeX command)

### 13.4 Handling Sparse YAML Descriptions

When YAML source has minimal description:

```markdown
<!-- TECHNICAL REVIEW: Description sparse - expand from silicon doc -->
```

Place this comment after the entry separator to flag for later enhancement.

---

## 14. Validation Checklist

Before finalizing an entry, verify:

- [ ] Instruction name heading with anchor
- [ ] Short description (no period)
- [ ] Category link with one-liner (period at end)
- [ ] Syntax block with all forms
- [ ] Result line (bold label, single sentence)
- [ ] Parameters as bullet list
- [ ] Encoding table (correct macro, correct values)
- [ ] Related line with hyperlinks
- [ ] Explanation with operation, flags, usage
- [ ] Third person voice throughout
- [ ] No hedging words (probably, typically, usually)
- [ ] Consistent terminology (C flag, Z flag, COG, Hub)
- [ ] Separator line at end

---

## 15. File Organization

### 15.1 Part II Files

Instructions are organized by first letter:

```
opus-master/part-ii/
├── instructions-a.md    # ABS through AUGS
├── instructions-b.md    # BITC through BMASK
├── instructions-c.md    # CALL through CRCNIB
├── ...
├── instructions-z.md    # (if any Z instructions)
├── directives.md        # All 10 directives
├── constants.md         # All 6 constants
└── special-registers.md # DIRA, DIRB, INA, etc.
```

### 15.2 File Headers

Each instructions file starts with:

```markdown
# Instructions: A

This section contains all PASM2 instructions beginning with the letter A.

---
```

---

*Created: 2025-11-28*
*Sprint: PASM2 Manual Generation Phase 0.9*
