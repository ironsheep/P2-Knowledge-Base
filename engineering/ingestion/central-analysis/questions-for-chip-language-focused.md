# Essential Questions for Chip - Language Understanding Focus
*What we actually need for AI code generation*
*Date: 2025-08-15*

## 🎯 THE REFRAME: We Need Language Semantics, Not Hardware Details

For AI to generate correct P2 code, we need to understand what instructions DO, not how chips boot or pins tolerate voltage.

## 🔴 PRIORITY 0: Empirical Conflicts Needing Chip Adjudication

*Bench results that contradict documented behavior. Added as they surface; each
is FROZEN in our docs/KB until Chip resolves it (empirical outranks documentary,
but a primary-source overturn is held pending Chip/isolation before we apply it).*

### ✅ RESOLVED 2026-07-11 — DEBUG_PIN_TX / DEBUG_PIN_RX "reversal" was a `pnut-ts` BUG, not a doc/silicon conflict — REMOVED from the ask-Chip queue
*Surfaced and resolved the same day (Debug-Window fleet-release sprint). No Chip adjudication needed.*

- **Resolution:** the reversal is a **`pnut-ts` bug in the SET-path** — it manifests **only when a
  program explicitly *sets* `DEBUG_PIN_TX` / `DEBUG_PIN_RX`**. With the defaults (TX=62 / RX=63) DEBUG
  works correctly, as proven by the entire fleet-release hardware campaign (which read DEBUG output on
  Stephen's bench throughout). Confirmed by Stephen + the pnut-ts agent 2026-07-11; `pnut-ts` is being
  patched.
- **The docs were RIGHT:** v55 (`DEBUG_PIN_TX=62` output / `DEBUG_PIN_RX=63` input) and our KB
  (`special-configuration-symbols.yaml:289-296`), Assembly App E, single-step-debugger REF, and
  Debug-Window ch02 all correctly copy the documented values. The triangulation that closed it: every
  documentary source agreed, the rig is hardwired-standard (Edge → adapter → PropPlug → USB, nothing
  to miswire), and DEBUG worked all project on the defaults → the tool's set-path was the only variable.
- **Doc/KB impact: NONE.** No manual, YAML, or example changes — the documented values stand. Tool bug
  → tool fix ("PNut is ground truth; a tool bug is a code fix").
- **Carve-out CLEARED:** `ch02-term-pin-config` is no longer blocked by this and can be certified — its
  documented pins are correct; the defect was in the tool's set-path (now being fixed), not the example.

## 🔴 PRIORITY 1: Instruction Semantics (The Real Gaps)

### Missing Instruction Descriptions (~300 instructions)
**Question for Chip**: "Can you provide one-sentence descriptions for these instruction groups?"

1. **Bit Manipulation Instructions**
   - TESTB, TESTBN, TESTB, BITL, BITH, BITC, BITNC, BITZ, BITNZ, BITRND, BITNOT
   - *What we need*: What each does to bits/flags

2. **ALU Operations** 
   - MODCZ, MODC, MODZ, SUMNC, SUMZ, SUMNZ
   - *What we need*: How they modify C/Z flags

3. **Branch/Skip Instructions**
   - MODCZ, MODZ, MODC effects on skipping
   - *What we need*: Exact skip conditions

4. **Special Operations**
   - SETQ, SETQ2, XORO32, XORO16
   - *What we need*: Purpose and usage patterns

**Why this matters**: Without knowing what instructions DO, AI can't choose the right one.

## 🟡 PRIORITY 2: Language Constructs

### Spin2 Operator Precedence
**Question**: "What's the complete precedence table for all Spin2 operators?"
- Need all 16 levels
- Especially floating-point and special operators

### Inline PASM2 Restrictions  
**Question**: "What are the exact rules for inline PASM2 in Spin2?"
- Register usage
- Label scope
- Instruction limitations

### Method Call Overhead
**Question**: "How many cycles for PUB/PRI calls with different parameter counts?"
- Helps AI choose between Spin2 and PASM2

## 🟢 PRIORITY 3: Common Patterns (Nice to Have)

### Multi-COG Coordination
**Question**: "What's your preferred pattern for COG communication?"
- Mailbox structure
- Lock usage
- Event signaling

### Performance Patterns
**Question**: "Any must-know optimization patterns?"
- Hub alignment tricks
- Pipeline-friendly sequences
- CORDIC usage patterns

## ❌ NOT NEEDED FOR CODE GENERATION

### Don't Ask About:
- Boot process (deployment concern)
- Electrical specs (hardware concern)  
- Silicon errata (tool concern)
- USB protocols (application-specific)
- Thermal characteristics (hardware)
- Package dimensions (hardware)

## 📝 THE SIMPLIFIED ASK FOR CHIP

"Hi Chip,

We're building an AI knowledge base for P2 code generation. We have the instruction syntax but need semantics. 

Could you provide:
1. One-sentence descriptions for the ~300 undocumented instructions?
2. Complete Spin2 operator precedence table?
3. Inline PASM2 rules and restrictions?

We DON'T need boot/hardware/electrical details - just language understanding.

This would enable AI to generate syntactically AND semantically correct P2 code.

Thanks!"

## 💡 WHY THIS APPROACH WORKS

1. **Focused Ask**: Language only, not hardware
2. **Manageable Scope**: ~300 sentences, not entire manuals
3. **Clear Value**: Enables AI code generation immediately
4. **Respects Time**: Specific, bounded request
5. **Separates Concerns**: Code generation ≠ deployment

## 🎯 BOTTOM LINE

**For AI Code Generation We Need:**
- What instructions DO (semantics)
- How language constructs work (precedence, rules)
- Common patterns (optional but helpful)

**We DON'T Need:**
- How hardware boots
- What voltages pins tolerate
- How USB protocols work
- Silicon manufacturing details

**This makes our ask 10x smaller and 10x more achievable!**

---

*This focused approach gets us to AI code generation faster*