# Chip Gracey Clarifications — 2026-05-02

**Source:** Latest Spin2 Interpreter Analysis review by Chip Gracey
**Recorded by:** Claude (Opus 4.7) under user direction
**Audit context:** Follow-up review of the round-4 hubexec/inline-PASM corrections (commits e77d676/63e8f76)

---

## Verbatim findings

### 1. REP and ALTI/ALTx in hub-exec

> "Also REP and ALTI as instruction-stream modifier. Source: Silicon Doc v35 HUB EXECUTION section verbatim."
>
> REP is allowed in hubexec and so is ALTI or any other ALTx instruction.
>
> In hubexec, REP is realized with branches which take a lot of time.

**Implication:** Confirms our round-4 correction that REP works in hubexec (slower per iteration due to branches). **Extends the rule to all ALTx instructions** (not just ALTI) — none are restricted in hubexec.

### 2. SKIP / SKIPF in hub-exec

> In hubexec, SKIP and SKIPF both work, but SKIPF will revert to SKIP behavior, where it replaces instructions in the pipeline with NOPs.

**Implication:** Both work in hubexec. Already captured in `skipf_branching.yaml` after round 3, but should verify wording is fully consistent.

### 3. Multitasking taskptr table — "upper" vs "lower"

> "$100..$11F is the multitasking taskptr table, building downward from $11F. Programs that use fewer than 32 software tasks leave the unused upper portion of this range available for user code as well."
>
> Should read "unused **lower** portion," not "upper". Not sure why Claude knows it builds downward but then says the upper part is available.

**Implication:** A specific phrasing error to find and fix. The taskptr table builds *downward from $11F*, so unused space is at the **lower** end of the $100..$11F range, not the upper.

### 4. Inline PASM total area + ORGH..END inline option

> "Inline PASM (ORG ... END inside a Spin2 method) is loaded into cog RAM at runtime by the interpreter. It runs as cog-exec (not hub-exec). The total inline area is 16 longs, shared by parameters + result + locals + code (per p2kb p2kbSpin2InlinePasm)."
>
> The total inline area is **$000..$11F**, assuming no multitasking. The first 16 params + results + locals are loaded from hub into the buff block at **$1E0..$1EF**, and then restored after the inline code exits.

**Implication:** Refines our round-4 `code_buffering` correction with the *exact* range and an explicit dependency on multitasking. Code area is **$000..$11F** (288 longs) when no multitasking is used — this is the same range that the multitasking taskptr table claims when active.

> Note: There is also now an **ORGH..END inline option** where no code is loaded, but executed directly from hub. Also, the first 16 params + results + locals are buffered and restored like in ORG..END. I just updated that part of the documentation to cover ORGH.

**Implication:** New construct we don't currently document — `ORGH..END` inline. Like `ORG..END` but the PASM runs from hub-exec (no cog-RAM copy of code). The 16-long variable buffer at $1E0..$1EF behavior is the same.

### 5. Bytecode optimization opportunity (forward-looking, NOT a correction)

> I think the biggest win on bytecodes would come from combining bitfield setups with reads and writes. That would have sizable impact on applications that use bitfields. Most bitfield operations are read and write, so for each one of those, we'd save a byte. The problem is that we don't have the room to do this in the cog registers. I have thought, for a long time, that LOOKUP/LOOKDOWN could go into hub. That would definitely get the space we'd need.

**Implication:** Roadmap commentary, not a current-state correction. Don't change YAMLs based on this — it's a future-design idea.

---

## Status

Findings analyzed against current YAML state below. Proposed changes identified before editing per the user's "identify before doing anything" directive.
