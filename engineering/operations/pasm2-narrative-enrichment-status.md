# PASM2 Instruction Narrative Enrichment Status

## Date: 2025-09-22

## Current Situation

The heat map shows many instructions with scores < 60 that need narrative enrichment. These instructions currently have:
- Basic descriptions (single line)
- Minimal documentation fields
- No examples
- No practical use cases
- No related instruction references

## What Makes a Rich Narrative (Score 80+)

Based on high-scoring instructions like WAITX, a rich narrative includes:

1. **Multi-paragraph description** explaining:
   - What the instruction does
   - When to use it
   - Why it's important
   - Common use cases

2. **Multiple code examples** (3-5) showing:
   - Real-world applications
   - Different usage patterns
   - Integration with other instructions
   - Comments explaining the code

3. **Related instructions section**:
   - Similar instructions
   - Alternative approaches
   - Instruction families

4. **Notes section** with:
   - Important tips
   - Common pitfalls
   - Performance considerations
   - Best practices

5. **Proper metadata**:
   - documentation_level: comprehensive
   - documentation_source: enhanced
   - examples with source references

## Instructions Needing Enrichment (from Heat Map)

### Critical Priority (Score 35) - NEED FULL NARRATIVES
- **PUSHA** - Currently has only basic fields
- **PUSHB** - Currently has only basic fields

### High Priority (Score 40) - NEED FULL NARRATIVES
Stack Operations:
- **POPA** - Has basic enhancement, needs examples
- **POPB** - Has basic enhancement, needs examples

Interrupt Instructions:
- **NIXINT1**, **NIXINT2**, **NIXINT3** - Minimal documentation
- **TRGINT1**, **TRGINT2**, **TRGINT3** - Minimal documentation
- **SETINT1**, **SETINT2**, **SETINT3** - Minimal documentation

CRC Instructions:
- **CRCBIT** - Needs practical examples
- **CRCNIB** - Needs practical examples

Color Space:
- **SETCY**, **SETCFRQ**, **SETCQ**, **SETCI**, **SETCMOD** - Need examples

Pixel Operations:
- **MULPIX**, **SETPIX**, **SETPIV**, **BLNPIX**, **MIXPIX**, **RGBEXP**, **RGBSQZ**

Event Instructions:
- **SETSE1**, **SETSE2**, **SETSE3**, **SETSE4** - Need event handling examples

DAC/Streamer:
- **SETDACS** - Needs DAC examples
- **SETXFRQ** - Needs streamer examples

Hub Write:
- **WRC**, **WRBYTE**, **WRZ** - Need detailed write examples

### Medium Priority (Score 50) - NEED EXAMPLES & NOTES

These have basic documentation but lack examples and practical guidance:

Hub Operations:
- **WMLONG**, **WRLONG**, **WRWORD**, **WRFAST**
- **WFBYTE**, **WFWORD**, **WFLONG**
- **HUBSET**, **LOCKRET**, **LOCKNEW**
- **RDBYTE**, **RDPIN**, **RQPIN**

Control Flow:
- **SETQ**, **TJNZ**, **TJF**, **TJS**, **TJZ**
- **SKIP**, **REP**, **SKIPF**
- **JMP**, **JMPREL**, **JPAT**
- **JINT**, **JNINT**, **JXRO**, **JNXRO**
- **JXFI**, **JNXFI**, **JATN**, **JNATN**, **JNPAT**
- **RET**, **RETA**, **RETB**

Data Operations:
- **LOC**, **GETCT**, **GETPTR**
- **TESTB**, **SETPAT**
- **MERGEB**, **MERGEW**, **MOVBYTS**
- **SPLITB**, **SPLITW**
- **SUMZ**, **SUMC**

CORDIC/Math:
- **GETQX**, **GETQY**, **GETXACC**

Streamer:
- **XSTOP**, **XCONT**, **XZERO**, **XINIT**

FIFO:
- **FBLOCK**, **RFVAR**, **RFVARS**
- **RFBYTE**, **RFWORD**, **RFLONG**
- **EXECF**

Pin Operations:
- **WXPIN**, **WRNC**, **WRNZ**

Special:
- **NOP**, **ASMCLK**, **DEBUG**
- **SETSCP**, **GETSCP**, **SETLUTS**
- **SEUSSR**, **SEUSSF**
- **GETRND**, **XORO32**
- **RDLUT**, **WRLUT**
- **MUXC**, **MUXNC**

## Work Plan for Today

### Phase 1: Critical Instructions (PUSHA, PUSHB)
Create comprehensive narratives with:
- Detailed explanation of stack operations
- Examples showing stack usage patterns
- Integration with POPA/POPB
- Common pitfalls (stack overflow/underflow)

### Phase 2: High Priority Groups
Focus on instruction families:
1. **Interrupt System** (NIXINT, TRGINT, SETINT series)
2. **CRC Operations** (CRCBIT, CRCNIB)
3. **Pixel/Color Operations** (MULPIX, SETPIX, etc.)
4. **Event System** (SETSE1-4)

### Phase 3: Add Examples to Score 50 Instructions
These already have basic documentation, just need:
- 2-3 practical examples each
- Related instruction references
- Usage notes

## Files to Create/Update

Location: `/engineering/knowledge-base/P2/language/pasm2/`

Each instruction YAML needs:
```yaml
instruction: [NAME]
description: |
  Multi-paragraph description...
  
  Use cases...
  
  Important considerations...
  
examples:
- name: Example 1 Name
  description: What this shows
  code: |
    ' Full code example
    ' With comments
  source: reference_name
  
- name: Example 2 Name
  description: Another use case
  code: |
    ' More code
  source: reference_name
  
related_instructions:
- INSTRUCTION1: Brief description
- INSTRUCTION2: Brief description

notes:
- Important tip 1
- Common pitfall
- Performance consideration
- Best practice

documentation_level: comprehensive
documentation_source: enhanced
```

## Success Metrics

- Move all Score 35 instructions to Score 80+
- Move all Score 40 instructions to Score 70+
- Move all Score 50 instructions to Score 60+
- Achieve 0 instructions with score < 40