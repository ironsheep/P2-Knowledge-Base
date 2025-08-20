# PASM2 Manual Extraction Audit Checklist
*For Stephen to verify against source document*

## AUDIT PURPOSE
Verify what we extracted vs. what's actually in the PASM2 manual to identify gaps

---

## PART 1: INSTRUCTION TABLES AUDIT

### What We Claim to Have Extracted
**We say**: 315 instructions documented from 219 tables

### Please Check: Table Count by Letter
*Mark ✓ if we have it, X if missing*

#### A Instructions
- [ ] ABS - Absolute value
- [ ] ADD - Add 
- [ ] ADDCT1 - Add to CT1
- [ ] ADDCT2 - Add to CT2
- [ ] ADDCT3 - Add to CT3
- [ ] ADDPIX - Add pixels
- [ ] ADDS - Add signed
- [ ] ADDSX - Add signed extended
- [ ] ADDX - Add with carry
- [ ] AKPIN - Acknowledge smart pin
- [ ] ALLONES - (check if exists)
- [ ] ALTB - Alter byte
- [ ] ALTD - Alter destination
- [ ] ALTGB - Alter get byte
- [ ] ALTGN - Alter get nibble
- [ ] ALTGW - Alter get word
- [ ] ALTI - Alter instruction
- [ ] ALTR - Alter result
- [ ] ALTS - Alter source
- [ ] ALTSB - Alter set byte
- [ ] ALTSN - Alter set nibble
- [ ] ALTSW - Alter set word
- [ ] AND - Logical AND
- [ ] ANDN - AND NOT
- [ ] AUGD - Augment destination
- [ ] AUGS - Augment source

#### B Instructions
- [ ] BITC - Bit to C
- [ ] BITH - Bit high
- [ ] BITL - Bit low
- [ ] BITNC - Bit to not C
- [ ] BITNOT - Bit not
- [ ] BITNZ - Bit to not Z
- [ ] BITRND - Bit random
- [ ] BITZ - Bit to Z
- [ ] BLNPIX - Blend pixels
- [ ] BMASK - Bit mask
- [ ] BRK - Break

[Continue through alphabet...]

### CRITICAL: Clock Timing Column
**For EACH instruction table, check if it has:**
- [ ] Instruction name column
- [ ] Syntax/format column  
- [ ] Encoding column (EEEE OOOOOOO CZI...)
- [ ] Description/narrative column
- [ ] **CLOCK CYCLES column (rightmost)** ← KEY MISSING DATA

### Sample Clock Timing Values to Look For
Please note examples you see:
- "2 clocks" = ___________
- "2..9 clocks" = ___________
- "hub-dependent" = ___________
- "CORDIC-dependent" = ___________
- Other patterns: ___________

---

## PART 2: INSTRUCTION NARRATIVES AUDIT

### For Instructions Starting with W-Z
*These are likely at document tail and may be missing*

Please check if these exist and have narratives:
- [ ] WAITATN - Wait for attention
- [ ] WAITCT1/2/3 - Wait for CT
- [ ] WAITEDG - Wait for edge
- [ ] WAITFBW - Wait for FIFO block wrap
- [ ] WAITINT - Wait for interrupt
- [ ] WAITPAT - Wait for pattern
- [ ] WAITSE1/2/3/4 - Wait for selectable events
- [ ] WAITX - Wait X clocks
- [ ] WAITXFI - Wait X clocks, FIFO
- [ ] WAITXMT - Wait for transmit
- [ ] WAITXRL - Wait for XRL
- [ ] WAITXRO - Wait for XRO
- [ ] WC/WZ/WCZ - Write flags
- [ ] WFBYTE - Write FIFO byte
- [ ] WFLONG - Write FIFO long
- [ ] WFWORD - Write FIFO word
- [ ] WMLONG - Write masked long
- [ ] WRBYTE - Write byte
- [ ] WRFAST - Write fast
- [ ] WRLONG - Write long
- [ ] WRLUT - Write LUT
- [ ] WRPIN - Write pin config
- [ ] WRWORD - Write word
- [ ] WXPIN - Write X to pin
- [ ] WYPIN - Write Y to pin
- [ ] XBYTE - Extract byte
- [ ] XCONT - Continue streamer
- [ ] XINIT - Initialize streamer
- [ ] XNOR - Exclusive NOR
- [ ] XOR - Exclusive OR
- [ ] XORO32 - XOR with RND
- [ ] XSTOP - Stop streamer
- [ ] XWORD - Extract word
- [ ] XZERO - Zero extend
- [ ] ZEROX - Zero extend

---

## PART 3: EXTRACTION COMPLETENESS CHECK

### Table Format Verification
Pick 5 random instructions and verify ALL columns present:

#### Instruction 1: ____________
- [ ] Name/mnemonic
- [ ] Syntax
- [ ] Encoding  
- [ ] Description
- [ ] Clock timing
- [ ] Flags affected

#### Instruction 2: ____________
- [ ] Name/mnemonic
- [ ] Syntax
- [ ] Encoding
- [ ] Description  
- [ ] Clock timing
- [ ] Flags affected

[Repeat for 3 more...]

---

## PART 4: WHAT TO REPORT BACK

### Summary Questions
1. **Total instruction tables in document**: _______
2. **Tables with clock timing column**: _______
3. **Instructions after 'W' in alphabet**: List them
4. **Multi-page tables**: List any
5. **Tables in appendices**: List any

### Missing Data Categories
- [ ] Clock timing not extracted at all
- [ ] Some instructions have no narratives
- [ ] Encoding patterns incomplete
- [ ] Flag effects missing
- [ ] Usage examples not captured

### Your Assessment
**Based on visual inspection, we missed:**
- [ ] 0-10% of content
- [ ] 10-25% of content  
- [ ] 25-50% of content
- [ ] More than 50% of content

---

## RECOMMENDATIONS

After your audit, please tell me:
1. Should we do targeted extraction of clock timing only?
2. Should we re-extract specific missing instructions?
3. Should we do complete re-extraction with better patterns?
4. Are the gaps small enough to handle manually?

---

*This checklist will help us understand exactly what we have vs. what exists*