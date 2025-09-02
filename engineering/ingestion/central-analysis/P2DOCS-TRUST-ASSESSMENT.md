# P2docs.github.io Trust Assessment & Verification Requirements

## ⚠️ CRITICAL WARNING
**Ada is involved in Flexspin compiler development** - Some features may be compiler-specific, not hardware features!

## Trust Categories

### 🟩 HIGH TRUST - Hardware Features (Likely Accurate)
These align with multiple sources and are too specific to be compiler constructs:

1. **Pixel Operations (ADDPIX, MULPIX, BLNPIX, MIXPIX)**
   - ✅ Instruction names match CSV
   - ✅ Hardware acceleration makes sense
   - ✅ Too complex for compiler synthesis
   - **Trust: 90%**

2. **CORDIC Operations**
   - ✅ Matches Silicon Doc descriptions
   - ✅ 54-stage pipeline confirmed elsewhere
   - ✅ Hardware coprocessor well documented
   - **Trust: 95%**

3. **Smart Pin Modes**
   - ✅ Cross-validated with Silicon Doc
   - ✅ Matches official documentation
   - **Trust: 95%**

### 🟡 MEDIUM TRUST - Needs Verification
Could be hardware OR compiler features:

1. **Condition Flags/Codes**
   - ⚠️ **CRITICAL**: Could be Flexspin compiler aliases!
   - ⚠️ Any "new" condition codes not in Silicon Doc are suspect
   - ⚠️ Extended mnemonics might be compiler convenience
   - **Trust: 50%** - MUST verify against hardware

2. **Instruction Aliases/Variants**
   - ⚠️ Flexspin might provide pseudo-instructions
   - ⚠️ Macro expansions could look like real instructions
   - **Trust: 60%**

3. **Timing Claims (7-cycle pixel ops, 6-cycle bytecode)**
   - ⚠️ Could be compiler optimization estimates
   - ⚠️ Might include compiler overhead
   - **Trust: 60%**

### 🔴 LOW TRUST - Likely Compiler Features
High probability of being Flexspin-specific:

1. **Extended Addressing Modes**
   - ❌ Any addressing not in Silicon Doc
   - ❌ Convenience syntax
   - **Trust: 30%**

2. **High-Level Constructs**
   - ❌ Structured programming elements
   - ❌ Compiler directives
   - **Trust: 20%**

## Verification Requirements

### MUST VERIFY Against Silicon Doc:
1. **ALL condition codes/flags** mentioned in p2docs
2. **ANY instruction** not found in CSV
3. **ALL timing specifications**
4. **ANY "extended" features**

### Safe to Accept (with notation):
1. **Hardware block descriptions** (CORDIC, Smart Pins)
2. **Physical capabilities** (HDMI output, pixel operations)
3. **Architecture features** (pipeline, memory map)

### RED FLAGS - Probably Flexspin:
- "Convenience" instructions
- Extended mnemonics
- Compiler optimizations described as hardware
- Any feature that "makes programming easier"

## Specific Items to Re-examine

### From P2docs Instruction Table:
- [ ] Check ALL condition codes against Silicon Doc
- [ ] Verify instruction encodings match CSV exactly
- [ ] Confirm timing doesn't include compiler overhead
- [ ] Validate "special" addressing modes

### From P2docs Examples:
- [ ] Ensure code examples use hardware instructions only
- [ ] Check for Flexspin-specific syntax
- [ ] Verify assembly syntax matches PASM2 standard

## Documentation Strategy

### How to Document P2docs Information:
```markdown
## [Feature Name]
**Source**: p2docs.github.io
**Verification Status**: 
- 🟩 VERIFIED - Confirmed in Silicon Doc/CSV
- 🟡 UNVERIFIED - Awaiting hardware confirmation
- 🔴 FLEXSPIN - Compiler-specific feature

**Hardware vs Compiler**: 
- If hardware: Document normally
- If compiler: Note as "Flexspin extension"
- If uncertain: Flag for verification
```

### Trust Levels for Integration:
1. **Hardware confirmed**: Full integration
2. **Likely hardware**: Integrate with verification flag
3. **Possibly compiler**: Document separately as "Flexspin features"
4. **Definitely compiler**: Exclude from hardware docs

## Critical Questions to Ask

For EVERY p2docs feature:
1. Is this in the Silicon Doc?
2. Does the CSV have this encoding?
3. Could a compiler synthesize this?
4. Does this make hardware sense?
5. Is this "too convenient" to be hardware?

## Examples of Likely Flexspin Features

### Suspect Condition Codes:
- Extended aliases not in our compiler source
- "Convenience" conditions
- High-level comparisons

### Suspect Instructions:
- Anything that looks like multiple operations
- "Smart" instructions that do too much
- Convenience wrappers

### Suspect Syntax:
- Extended addressing modes
- Simplified operand formats
- High-level constructs

## Recommendation

### For P2 Knowledge Base:
1. **Create two sections**:
   - "P2 Hardware Features" (verified)
   - "Flexspin Extensions" (compiler-specific)

2. **Verification Priority**:
   - HIGH: Condition codes and flags
   - HIGH: Instruction variants
   - MEDIUM: Timing specifications
   - LOW: Well-documented hardware blocks

3. **Documentation Policy**:
   - Always note source as "p2docs.github.io"
   - Always include verification status
   - Separate hardware from compiler features
   - Flag all unverified claims

## Conclusion

P2docs remains valuable but requires careful verification. The site likely mixes:
- **Real hardware documentation** (valuable)
- **Flexspin compiler features** (different category)
- **Optimization techniques** (compiler, not hardware)

We must be especially careful with:
- **Condition codes/flags** - High risk of compiler aliases
- **Instruction variants** - Could be macros
- **Timing claims** - Might include compiler overhead

The safest approach: Trust hardware block descriptions, verify everything else.