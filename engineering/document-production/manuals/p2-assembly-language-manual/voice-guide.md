# P2 Assembly Language Manual - Voice Guide

**Document:** P2 Assembly Language (PASM2) Manual
**Purpose:** Define the writing voice and tone for consistent, authoritative technical reference

---

## 1. Voice Philosophy

### 1.1 The Guiding Principle

> **The DeSilva manual teaches you to fish. This manual tells you exactly which fish are in the lake, their precise weight, and the water temperature - when you already know how to fish.**

This is a **technical reference**, not a tutorial. The voice must be:
- **Authoritative** - This is the source of truth
- **Precise** - No ambiguity, no hedging
- **Efficient** - Every word serves a purpose
- **Enhanced** - Goes beyond the original with actionable guidance

### 1.2 Relationship to Source Material

This manual evolves the voice established in the Parallax PASM2 Manual Draft (2022-11-01). We preserve what works and enhance what's missing.

**Source Location:** `/engineering/ingestion/sources/pasm2-manual/`

### 1.3 Narrative Brevity (Part I)

Part I prose explains the mental model in the fewest words that remain **complete
and accurate**. Prefer the short, harder-to-write explanation over the long one.
Where a concept is documented authoritatively elsewhere in the manual,
**cross-reference rather than re-explain**.

**Surface honest tradeoffs.** Do not present a capability without its cost when
that cost shapes how the reader actually writes code — e.g. introduce the
eight-cog parallelism alongside the random-hub-access latency that constrains it.
A reference that lists only strengths reads as marketing and misleads.

This principle bears hardest on the **front-matter / preface and Chapter 1**,
which were written first and carry the most redundancy and promotional residue.

---

## 2. Voice Analysis: Parallax Draft

### 2.1 Characteristics We Preserve

The Parallax draft established an appropriate technical reference voice:

**Technical Precision**
```
Original: "If the WC or WCZ effect is specified, the C flag is set (1) if
the summation results in a 32-bit overflow (unsigned carry), or is
cleared (0) if no overflow."
```
- Exact terminology: "9-bit literal," "32-bit augmented literal"
- Specific values: "Src[8:0]," "Dest[17:9]," "0-511"
- No hedging: "is set" not "may be set"

**Formal Tone**
- Third person throughout: "ADDS sums the two signed values..."
- Passive voice where appropriate: "The result is stored in Dest"
- No casual language or colloquialisms

**Structured Predictability**
- Every instruction follows identical format
- Tables for complex data
- Bulleted lists for parameters

**Dense Information**
- No padding or fluff
- Every sentence conveys technical content
- Complex instructions get proportionally more explanation

**Cross-Reference Network**
- "as described in Adding Two Multi-Long Values"
- "Related: SETD, SETS, SETR, ALTD, ALTS, and ALTR"
- Builds understanding through connections

### 2.2 Why This Voice Works for Reference

| Characteristic | Why It Works |
|----------------|--------------|
| Precision | Source of truth requires zero ambiguity |
| Formal tone | Signals authority and reliability |
| Predictable structure | Reduces cognitive load on lookup |
| Dense information | Respects reader's time |
| Cross-references | Builds comprehensive understanding |

---

## 3. Voice Enhancements: What We Add

The Parallax draft tells you *what* instructions do. Our manual also tells you *when*, *why*, and *watch out*.

### 3.1 Enhancement Categories

| Enhancement | Purpose | Marker |
|-------------|---------|--------|
| Pitfall warnings | Prevent common mistakes | ⚠️ **Pitfall:** |
| Usage guidance | When to choose this instruction | (in Operation or Notes) |
| Richer examples | Show *why*, not just *that* | EXAMPLE section |
| Architecture links | Connect to Part I concepts | "See Chapter X" |
| Pro tips | Non-obvious techniques | 💡 **Tip:** |
| Hardware notes | Silicon-level details | 🔧 **Hardware:** |

### 3.2 Enhancement Examples

**Original Parallax (what):**
```
If the WC or WCZ effect is specified, the C flag is set (1) if the
summation results in a 32-bit overflow (unsigned carry), or is
cleared (0) if no overflow.

To add unsigned, multi-long values, use ADD followed by ADDX as
described in Adding Two Multi-Long Values.
```

**Our Enhanced Version (what + watch out + why):**
```
If the WC or WCZ effect is specified, the C flag is set (1) if the
summation results in a 32-bit overflow (unsigned carry), or is
cleared (0) if no overflow.

To add unsigned, multi-long values, use ADD followed by ADDX as
described in Adding Two Multi-Long Values. See Chapter 1 for the
P2 execution model that makes this chaining possible.

⚠️ **Pitfall:** For multi-long addition, forgetting WC on the leading
ADD causes ADDX to receive incorrect carry-in. Always use WC or WCZ
on ADD when chaining to ADDX.

💡 **Tip:** ADD treats both operands as unsigned. For signed addition
where you need signed overflow detection, see ADDS.
```

### 3.3 When to Add Enhancements

**Add ⚠️ Pitfall when:**
- A common mistake has non-obvious consequences
- Flag effects are critical and easily forgotten
- Instruction behavior differs from intuitive expectation
- Order of operations matters (e.g., SETQ before RDxxxx)

**Add 💡 Tip when:**
- A non-obvious technique improves code
- An alternative approach exists for specific cases
- Performance implications are significant
- Instruction combinations create powerful patterns

**Add 🔧 Hardware when:**
- Silicon behavior differs from software expectation
- Timing has hardware implications
- Pipeline effects matter
- Hub access windows affect usage

**Add "See Chapter X" when:**
- A Part I concept explains the underlying mechanism
- Architectural understanding enhances instruction usage
- The explanation would otherwise be repeated across entries

---

## 4. Voice Rules

### 4.1 Always Do

| Rule | Example |
|------|---------|
| Use definitive statements | "The C flag is set" ✅ |
| Be specific about values | "9-bit immediate (0-511)" ✅ |
| Use consistent terminology | Always "C flag" not sometimes "carry" |
| Include all flag effects | Document C, Z for every instruction |
| Cross-reference related instructions | "Related: ADDX, ADDS, ADDSX" |
| Use third person | "The instruction performs..." ✅ |

### 4.2 Never Do

| Rule | Bad Example | Why |
|------|-------------|-----|
| Never hedge | "The C flag may be set" ❌ | Creates ambiguity |
| Never use first person | "We can see that..." ❌ | Tutorial voice |
| Never use second person | "You should use..." ❌ | Tutorial voice |
| Never be conversational | "Let's explore..." ❌ | DeSilva voice |
| Never minimize | "Simply use ADD" ❌ | Dismissive of complexity |
| Never celebrate | "Congratulations!" ❌ | Tutorial voice |
| Never assume context | "As you know..." ❌ | Reference must stand alone |
| Never market or promote | "ideal for video generation, motor control" ❌ | Sells instead of states; dates badly |
| Never reassure that the hardware is correct | "the result is properly sign-extended" ❌ | Congratulates the silicon; conveys nothing |
| Never justify an example with a vague domain | "commonly used for physics calculations" ❌ | A domain name-drop carries no information |
| Never restate a fact already given | intro → section → subsection each repeating "parallel execution" ❌ | Padding; state each fact once, then add only new detail |

### 4.3 Voice Comparison Table

| Aspect | DeSilva Tutorial | This Reference |
|--------|------------------|----------------|
| Person | Second ("you") | Third (instruction names) |
| Tone | Warm, encouraging | Authoritative, precise |
| Hedging | Occasional ("usually") | Never |
| Examples | Extensive, progressive | Targeted, illuminating |
| Celebration | Yes ("Well done!") | Never |
| Questions | Yes ("Why? Because...") | No |
| Asides | Yes ("Uff!") | Never |
| Pitfall warnings | Occasional | Systematic |

---

## 5. Terminology Standards

### 5.1 Canonical Terms

Use these terms consistently throughout:

| Canonical Term | NOT These | Notes |
|----------------|-----------|-------|
| C flag | carry flag, C, carry | Always "C flag" in prose |
| Z flag | zero flag, Z, zero | Always "Z flag" in prose |
| cog | COG, CPU | **Lowercase "cog" in prose.** Capitalize **Cog** only at sentence start, in headings/titles, and in numbered forms (Cog 0–7). **Never all-caps "COG."** Use "cog," never "CPU," for the processor unit. (Corrected v1.1 — was wrongly "all caps"; conflicts with the applied cog-casing sweep + Parallax corpus.) |
| hub | HUB | Same rule as **cog**: lowercase "hub" in plain reference prose; capitalize **Hub** only in titles/headings, special-meaning, or proper-noun uses. Be consistent, not artificial. |
| LUT | lut, Lut | All caps (Lookup Table) |
| register | location, address, variable | For cog memory locations |
| immediate | literal, constant, value | For # prefixed values |
| augmented immediate | long immediate, 32-bit literal | For ## prefixed values |
| effect | modifier, flag effect | For WC, WZ, WCZ |
| condition | conditional, IF | For IF_x prefixes |

### 5.2 Instruction References

When referring to instructions in prose:

- **Bold and uppercase:** "The **ADD** instruction performs..."
- **In lists:** ADD, SUB, MUL (no bold needed)
- **In code:** `ADD Dest, #5` (monospace)

### 5.3 Field References

When referring to bit fields:

- Use brackets: "Src[8:0]" "Dest[17:9]"
- Specify bit count when helpful: "the 9-bit Src field"
- Use field names from encoding: "the D field," "the S field"

---

## 6. Section-Specific Voice

### 6.1 Brief Description

One sentence, starts with verb, states primary function:

```
✅ "Add two unsigned values."
✅ "Get the absolute value of a number."
✅ "Substitute next instruction's field values from template."

❌ "This instruction adds two values." (wordy)
❌ "Used to add values." (passive, vague)
❌ "ADD is for addition." (circular)
```

### 6.2 Parameters

Bulleted list, each parameter explained:

```
✅ • Dest - Register containing first operand; receives the sum
✅ • Src - Register, 9-bit immediate (#0-511), or augmented immediate (##value)
✅ • WC - Set C flag if unsigned overflow (carry out of bit 31)

❌ • Dest - The destination (too vague)
❌ • Src - Where the source comes from (circular)
```

### 6.3 Operation (compact pseudocode line)

A curated **Operation:** line gives a scannable formal summary of what the
instruction does, placed immediately **after the syntax line and before
Result:**. (This supersedes the earlier procedural step-by-step "Operation"
idea, which the entries never used.)

**Add it ONLY where it earns its place** — where the result/flag formula is NOT
obvious from the mnemonic + syntax + one-line description (bit-field shuffles,
slice-indexed ops, signed/scaled math, non-obvious flag derivations, pixel ops,
ALT next-instruction side-effects, encode/decode/CRC), OR where the **flag
effects are non-default** even if the value is obvious (e.g. logic ops where
`C = parity`, shifts/rotates where C captures the shifted-out bit). Plain
whole-register ops (MOV, ADD, SUB, AND-value, OR, XOR-value, CMP, NOP) do **not**
get one.

**Format:** backticked monospace; result first, then C, then Z, separated by
`; `. **Source the expression from the Parallax instruction CSV** (column 5) —
reformat notation only; never invent semantics (no inference).

```
✅ **Operation:** `D = signed(D[15:0] × S[15:0])`; `Z = (S==0 OR D==0)`   (MULS)
✅ **Operation:** `D = 1 << S[4:0]`                                       (DECOD)

❌ A procedural 1-2-3-4 step list (too verbose for a scannable reference)
❌ An Operation line on a self-evident op like MOV/ADD (noise, not signal)
```

### 6.4 Flag Effects

Precise statement of when flags change:

```
✅ "C Flag: Set to 1 if addition produces carry (overflow beyond 32 bits);
          cleared to 0 otherwise. Only updated if WC or WCZ specified."

❌ "C is the carry flag." (doesn't say when it's set)
❌ "C may be set on overflow." (hedging with "may")
```

### 6.5 Examples

Code with comments that explain *why*:

```pasm2
✅ ' 64-bit addition: result in X_hi:X_lo
           add     X_lo, Y_lo      wc      ' Add low longs, MUST capture carry
           addx    X_hi, Y_hi              ' Add high longs with carry-in

❌          add     X_lo, Y_lo      wc      ' Add with carry
           addx    X_hi, Y_hi              ' Add extended
   (Comments just restate the instruction, don't explain why)
```

### 6.6 Notes (Pitfalls, Tips, Hardware)

Categorized with emoji markers, concise:

```
✅ ⚠️ **Pitfall:** Forgetting WC on the first ADD in a multi-long chain
   causes incorrect results. The carry MUST propagate to ADDX.

✅ 💡 **Tip:** ADD treats both operands as unsigned. For signed addition
   where you need signed overflow detection, see ADDS.

✅ 🔧 **Hardware:** The addition completes in a single clock cycle within
   the COG's ALU. No pipeline stalls occur.

❌ Note: Be careful with this instruction. (vague, no specific guidance)
```

---

## 7. Quality Checklist

Before finalizing any instruction entry, verify:

### Voice Consistency
- [ ] Third person throughout (no "you," "we," "I")
- [ ] No hedging language ("may," "might," "probably," "typically")
- [ ] No tutorial voice ("let's," "congratulations," "simply")
- [ ] Definitive statements only
- [ ] No marketing / promotional framing (state capability as fact, don't sell it)
- [ ] No hardware-correctness reassurance ("properly," "correctly," "automatically handles")
- [ ] Examples lead with what the code does, not a vague application domain
- [ ] Each fact stated once — no restatement across intro / section / subsection
- [ ] Honest tradeoffs surfaced where the cost shapes how code is written (Part I)

### Terminology Consistency
- [ ] "C flag" and "Z flag" (not "carry" or "zero")
- [ ] Instruction names in bold uppercase in prose
- [ ] Consistent field notation (Src[8:0], Dest[17:9])
- [ ] Canonical terms from Section 5.1

### Enhancement Completeness
- [ ] Pitfalls marked with ⚠️ where applicable
- [ ] Tips marked with 💡 where valuable
- [ ] Hardware notes marked with 🔧 where relevant
- [ ] Cross-references to Part I chapters where helpful
- [ ] Related instructions listed

### Clarity
- [ ] Brief description is one sentence, starts with verb
- [ ] Parameters explain what each can be
- [ ] Operation describes step-by-step behavior
- [ ] Flag effects are precise and complete
- [ ] Examples show *why*, not just *what*

---

## 8. Summary: The Voice Equation

```
Our Voice = Parallax Precision + Actionable Enhancements
```

**From Parallax, we keep:**
- Technical precision and specificity
- Formal, third-person tone
- Structured, predictable format
- Dense, efficient information
- Cross-reference network

**To Parallax, we add:**
- ⚠️ Pitfall warnings for common mistakes
- 💡 Tips for advanced techniques
- 🔧 Hardware notes for silicon details
- Richer examples that show *why*
- Connections to Part I architectural concepts
- "When to use" guidance for instruction selection

**The result:**
A source-of-truth reference that not only tells you what every instruction does, but helps you use them correctly and effectively.

---

*Last Updated: 2026-06-24*
*Version: 1.1 — Added brevity + de-marketing rules (§1.3, §4.2, §7): no marketing/promotion, no hardware-correctness reassurance, no vague-domain example justifications, say-each-fact-once, surface honest tradeoffs. Origin: P2 Assembly Language Reference user-suggestions sprint (`sprint/USER-SUGGESTIONS-2026-06-24.md`).*
*Version: 1.0 - Initial Voice Guide (2025-11-26)*
