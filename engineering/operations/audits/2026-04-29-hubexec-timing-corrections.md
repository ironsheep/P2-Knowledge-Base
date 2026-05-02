# Hubexec Timing, Pin/Method Timing, ISR Dispatch & Data-Set-Wide Corrections

**Date:** 2026-04-29
**Auditor:** Claude (Opus 4.7) under user direction
**Scope:** P2 hubexec/cogexec timing model; CORDIC latency; FIFO depth; pin instruction execution-mode neutrality; Spin2-method bytecode-interpreter clock claims; ISR dispatch mechanism; PASM2 instruction-YAML systematic `timing.cycles: 1` errors
**Severity:** High — wrong timing claims propagated to AI consumers across ~80+ files
**Status:** Fixed in this session (verified against Silicon Doc v35 primary source + per-instruction YAMLs)

---

## Summary

This audit went through three rounds:

**Round 1** (initial finding): three files with wrong hubexec/inline-PASM characterizations (cog_hub_execution.yaml, hubexec.yaml, inline_pasm.yaml).

**Round 2** (deeper sweep): discovered that round-1 fixes themselves introduced new errors (used "4-16 clocks" for hub branches when correct is "minimum 13 clocks"; framed FIFO/streamer instructions as "slow" when they are FORBIDDEN in hubexec; said "16 longs deep" FIFO when it's 19 stages).

**Round 3** (data-set-wide sweep): found systematic problems across the entire data set:
- `timing.cycles: 1` errors in 18 PASM2 instruction YAMLs (hub-access ops + shifts misrepresenting their actual timing)
- Pin instruction Spin2 methods incorrectly claiming a cog-vs-hub execution-mode distinction (the underlying PASM is 2 clocks fixed in both modes)
- ~50 Spin2 method YAMLs publishing unsourceable bytecode-interpreter clock ranges (`2-9 clock cycles`, `~20-40`, `~8 + count×N`, etc.)
- Architecture YAMLs with: wrong CORDIC latency (54 vs verified 55), wrong cog branch_penalty framing (5-8 vs verified 4 + 5+ post-branch), wrong lock timings (2-18 vs verified 2-9/4-11), wrong xbyte software_dispatch overhead (~20-40 vs verified 9), unsourced "3-8 clock interrupt latency" claims throughout
- Spin2 concept files with unsourced floating-point cycle ranges and `~10-20 cycle method overhead` claims

**Round 4** (this round, 2026-04-30): user flagged two additional errors I had introduced. Both verified wrong against root sources:

1. **REP and ALTI "forbidden in hubexec" was wrong.** Silicon Doc v35 verbatim: *"REP works in hub memory, as well, but executes a hidden jump to get back to the top of the repeated instructions."* REP works in hubexec; it just pays the 13+-clock hub-branch cost on each iteration's hidden jump back to the top. ALTI is not in the Silicon Doc HUB EXECUTION forbidden list — it works in hubexec because it modifies the next pipelined instruction regardless of where the instruction was fetched from.

2. **Inline PASM "16 longs total (params + result + locals + code)" was wrong.** Spin2 v51 documentation verbatim describes TWO SEPARATE copies done by the interpreter: (1) "Copy the method's first 16 long variables ... from hub RAM to cog registers $1E0..$1EF" (variables only), and (2) "Copy the in-line PASM-code longs from hub RAM into cog registers, starting at the register address specified after the ORG (default is $000)" (code, separately). The 16-long limit applies to **variables only**; **code is buffered separately** and is not constrained by the 16-long figure.

**Round 5** (2026-05-02): Chip Gracey clarifications on the latest Spin2 Interpreter Analysis review. Three additional corrections plus one enrichment:

1. **Generalize ALTI to all ALTx.** Round-4 said "ALTI works in hubexec" — Chip explicitly broadened: "REP is allowed in hubexec and so is ALTI or any other ALTx instruction." Updated four files (cog_hub_execution.yaml in three spots, hubexec.yaml, execution_modes.yaml) to enumerate the full ALTx family (ALTI/ALTS/ALTD/ALTR/ALTB/ALTSN/ALTSB/ALTSW/ALTGN/ALTGB/ALTGW).

2. **Inline PASM code area constraint depends on multitasking.** Round-4 said code uses "$000..$11F (288 longs)". Chip clarified: "$000..$11F, assuming no multitasking. The total inline area is $000..$11F." When multitasking is used, $100..$11F is the taskptr table (building DOWNWARD from $11F). Programs using fewer than 32 tasks leave the LOWER portion free. Added `multitasking_taskptr_table:` block to inline_pasm.yaml and the inline_pasm2.yaml stub; also added taskptr_table_location to taskspin.yaml.

3. **Document phrasing rule — "lower" not "upper".** The taskptr table builds downward from $11F, so unused capacity is at the LOWER end of $100..$11F (closer to $100), NOT the upper end (closer to $11F). The wrong phrasing "unused upper portion" did not exist in our YAMLs but is now positively documented as "lower".

4. **Document the V50+ ORGH..END inline option.** This was already covered in `language/spin2/assembly-directives/orgh.yaml` but missing from `language/spin2/constructs/inline_pasm.yaml`. Added a new `syntax_form: orgh_inline` entry covering: code stays in hub RAM (no cog-RAM copy), runs as hub-exec, $FFFF-long maximum, same 16-long variable buffer/restore at $1E0..$1EF as ORG..END, bytecode $D6. Aligned `orgh.yaml` terminology to match ("First 16 long variables (params + result + locals) buffered at cog $1E0..$1EF on entry and restored to hub on exit").

5. **NOT changed (forward-looking commentary, not a current-state correction):** Chip's bytecode-optimization roadmap idea about combining bitfield setups with reads/writes and moving LOOKUP/LOOKDOWN to hub. This is a hypothetical future-design idea — do not document in current-state YAMLs.

All round-3, round-4, and round-5 issues have been corrected against root sources. New ingestion source file at `engineering/ingestion/sources/chip-gracey-clarifications/chip-clarifications-2026-05-02.md` records the round-5 verbatim findings.

---

## Authoritative numbers (final, verified)

| Fact | Value | Citation |
|---|---|---|
| Cog/LUT typical ALU instruction | **2 clocks** | Silicon Doc v35: "2-clock execution for all math and logic instructions" |
| Cog/LUT branch instruction (JMP/CALL/RET) | **4 clocks** | per-instruction YAMLs (jmp/call/ret cycles 4) |
| First instruction AFTER cog branch | **At least 5 clocks** (pipeline flush) | Silicon Doc v35 verbatim: "first instruction following the branch will take at least five clock cycles" |
| Conditionally canceled instruction | **2 clocks** (still moves through pipeline) | Silicon Doc verbatim |
| Pin instructions (output AND input) | **2 clocks fixed — same cogexec/lutexec/hubexec** | per-instruction YAMLs uniformly `cycles: 2, type: fixed` with no execution-mode distinction |
| Pin output propagation | +3 clocks before pin transitions | drvh.yaml |
| Pin input sampling (TESTP) | 2 clocks before instruction | testp.yaml |
| Pin input sampling (INA register read) | 3 clocks before instruction | io_pin_timing.yaml |
| Hub-exec sequential streaming | **2 clocks/instruction (same as cogexec)** | Silicon Doc qualitative + Chip Gracey clarification |
| Hub-exec branch | **Min 13 clocks (+1 if not long-aligned)** | Silicon Doc verbatim |
| FIFO depth | **(cogs+11) = 19 stages** | Silicon Doc verbatim |
| FIFO refill threshold | (cogs+7) = 15 stages | Silicon Doc verbatim |
| FIFO/streamer instructions in hubexec | **FORBIDDEN, not slow** | Silicon Doc verbatim list |
| **CORDIC result latency** | **55 clocks** | Silicon Doc verbatim: "Fifty-five clocks later, results will be available" |
| CORDIC pipeline depth | 54 clocks (separate from latency) | Silicon Doc verbatim |
| CORDIC cog issue interval | 8 clocks (8-cog P2) | Silicon Doc verbatim |
| GETQX/GETQY when CORDIC empty | **2 clocks** | Silicon Doc verbatim |
| **XBYTE bytecode dispatch overhead** | **6 clocks per bytecode** | Silicon Doc verbatim "6-clock custom-bytecode executor" |
| Software bytecode dispatch (no XBYTE) | **9 clocks** | Silicon Doc verbatim "2+3+4, or 9, clocks" |
| Minimum XBYTE loop (overhead + 2-clock routine + RET) | 8 clocks | Silicon Doc verbatim |
| RDLONG | `9...16 (cog) / 9...26 (hub)` | rdlong.yaml encoding |
| WRLONG | `3...10 (cog) / 3...20 (hub)` | wrlong.yaml encoding |
| RDBYTE/RDWORD | same as RDLONG range | per-instruction YAMLs |
| WRBYTE/WRWORD | same as WRLONG range | per-instruction YAMLs |
| RDLUT | 3 clocks | rdlut.yaml |
| WRLUT | 2 clocks | wrlut.yaml |
| PUSHA/PUSHB | range `3...10 (cog) / 3...20 (hub)` | per-instruction YAMLs |
| POPA/POPB | range `9...16 (cog) / 9...26 (hub)` | per-instruction YAMLs |
| RETA/RETB | range `11...18 (cog) / 20...40 (hub)` | per-instruction YAMLs |
| LOCKNEW | range `4...11` | locknew.yaml |
| LOCKRET/LOCKTRY/LOCKREL | range `2...9 (+2 if WC)` | per-instruction YAMLs |
| TJV | `2 not-taken / 4 taken (cog); 2 not-taken / 13-20 taken (hub)` | tjv.yaml encoding |
| RCL/ROL/ROR/SHL/SHR/SAL/SAR | 2 clocks each | per-instruction YAMLs |
| Hub-window slot wait | 0-7 clocks (8-cog rotation) | Silicon Doc egg beater |

## ISR Dispatch (verified from Silicon Doc v35 INTERRUPTS section)

| Fact | Value | Citation |
|---|---|---|
| Dispatch mechanism | Hardware inserts `CALLD IRETx,IJMPx WCZ` into the instruction pipeline | Silicon Doc verbatim |
| Entry overhead (cogexec) | **4 clocks** for the dispatched CALLD | calld.yaml encoding |
| Entry overhead (hubexec) | **13-20 clocks** (FIFO refill on the branch) | calld.yaml encoding |
| Exit overhead (RETI1/2/3) | 4 clocks (cog) / 13-20 clocks (hub) | reti1/2/3.yaml encoding |
| Exit overhead (RESI1/2/3) | 4 clocks (cog) / 13-20 clocks (hub) | resi1/2/3.yaml encoding |
| Round-trip minimum (cogexec) | **8 clocks** (4 entry + 4 exit), excluding ISR body | derived from above |
| Round-trip minimum (hubexec) | ~26 clocks (13 entry + 13 exit), excluding ISR body | derived from above |
| Deferral conditions | ALTxx/CRCNIB/SCA/SCAS/GETCT+WC/GETXACC/SETQ/SETQ2/XORO32/XBYTE executing; AUGS/AUGD pending; REP active; STALLI active; cog stalled in WAITx | Silicon Doc verbatim |
| Context-switch cost | **0 clocks for register state** — IJMPx/IRETx are dedicated registers, captured automatically by the dispatched CALLD | Silicon Doc verbatim |

This ISR dispatch detail was added in round 3 after the user asked specifically for more research into interrupt service routines. Silicon Doc does not publish a single "interrupt latency in N clocks" figure, but the CALLD-based dispatch mechanism has fully verifiable timing through the per-instruction YAMLs.

---

## Files changed (round 1 + 2 + 3 combined)

### Round 1+2 (already committed in commit fbbd9ee)

- `language/pasm2/concepts/cog_hub_execution.yaml` — major rewrite with canonical fifo_behavior section (round 3 corrected the "4-16 clocks" error in this file to use the verified "minimum 13 clocks" framing)
- `language/pasm2/concepts/execution_modes.yaml` — corrected systematic "1 cycle" claims (round 3 corrected branch numbers)
- `language/pasm2/hubexec.yaml` — notes block (round 3 corrected to "minimum 13 clocks")
- `language/spin2/constructs/inline_pasm.yaml` — execution_model + form descriptions
- `language/spin2/concepts/inline_pasm2.yaml` — demoted to redirect stub
- `architecture/fifo.yaml` — enriched with hubexec instruction-prefetch role

### Round 3 (this commit)

**Pin method execution-mode neutrality (6 files):**
- `language/spin2/methods/{pinhigh,pinlow,pintoggle,pinread,pinwrite,pinfloat}.yaml` — replaced unsourced "8-19 clock cycles when executed from hub" + "2 clock cycles in cog execution" with structured timing block citing underlying PASM (DRVH/DRVL/DRVNOT/TESTP/OUTNOT/FLTL — all 2 clocks fixed regardless of mode) + 3-clock pin propagation

**Spin2-method bytecode-interpreter timing (52 files):** removed unsourceable cycle ranges, replaced with structured `execution_model` + `underlying_pasm` (where one exists) per the "no interpreter clock counts" rule.
- akpin, cogatn, cogid, getct, getrnd, hubset, locknew, lockrel, lockret, locktry, pollatn, pollct, rdpin, rqpin (with single PASM backing)
- wordcomp, string, getsec, setregs, tasknext, byteswap, wordmove, cogstop, strcopy, lstring, bytecomp, taskstop, taskchk, cogchk, wordswap, nan, getcrc, pinclear, regload, taskhalt, getms, taskresume, wordfill, longfill, taskid, strsize, pinstart, longcomp, taskspin, call, waitms, waitus, longswap, longmove, lockchk, strcomp, getregs, muldiv64 (no clean PASM backing — timing block removed)

**Spin2 concept files (4 files):**
- `language/spin2/concepts/basic-io.yaml` — removed unsourced `method_calls: "~10-20 clock cycles overhead"` and `register_access: "~2-4 clock cycles"`
- `language/spin2/concepts/floating_point.yaml` — replaced unsourced ~100/200/300/400+ cycle claims with verifiable note pointing at CORDIC ops
- `language/spin2/concepts/random_generation.yaml` — reframed `getrnd: "Slower (2-9 cycles)"` to cite underlying GETRND PASM
- `language/spin2/concepts/cordic_solver.yaml` — corrected `38-55 clock cycles` to verified 55-clock latency

**Spin2 integration & inline_pasm:**
- `language/spin2/integration/spin2-pasm2-integration.yaml` — corrected `Variable speed, 4+ clocks per instruction` for hub_execution
- `language/spin2/constructs/inline_pasm.yaml` — removed `~50-200 clocks per operation` Spin2 estimate + `2-8 clocks per operation` PASM estimate; replaced with verifiable per-class PASM timings
- Same file — removed `~20 clocks of interpreter overhead` for END return, replaced with "we do not publish a clock count" note

**PASM2 instruction YAMLs with systematic `timing.cycles: 1` (18 files):**
- Shifts (rcl, rol, ror, sal, sar, shl, shr) — fixed to `cycles: 2`
- Hub-access ops (rdlong, wrlong, rdword, wrword, pusha, pushb, popa, popb, reta, retb) — replaced with verified ranges from encoding.clocks
- TJV — fixed to "2 not-taken / 4 taken (cog); 2 not-taken / 13-20 taken (hub)"

**Architecture files (8 files):**
- `architecture/cordic.yaml` — fixed 54 → 55 clocks for result latency (Silicon Doc verbatim); fixed 337.5ns → 343.75ns at 160MHz; reframed GETQX/GETQY timing to cite the 2-clock when-empty case
- `architecture/cog.yaml` — split branch_penalty into branch_instruction_time (4 clocks) + post_branch_first_instruction (5+ clocks per Silicon Doc); fixed instruction_timing per-class entries; replaced unsourced interrupt latency with full ISR dispatch detail (entry/exit/round-trip/deferral conditions)
- `architecture/hub.yaml` — fixed `2-9 clocks` claims for byte/word/long access (these conflated hub-window wait with full instruction time); reframed performance.latency block as "hub_window_slot_wait" with citation
- `architecture/locks.yaml` — corrected LOCKTRY (2-18 → 2 clocks range 2...9), LOCKNEW (was claimed 2 clocks, actually 4 clocks range 4...11), LOCKREL/LOCKRET (cited per-instruction YAML ranges)
- `architecture/xbyte_engine.yaml` — corrected software_dispatch from `~20-40 clocks` to verified 9 clocks (Silicon Doc verbatim)
- `architecture/cog_attention.yaml` — replaced unsourced "3-8 clock interrupt latency" with citation to ISR dispatch mechanism in architecture/interrupts.yaml
- `architecture/interrupts.yaml` — replaced unsourced `best_case: 3` / `worst_case: 8` with verified ISR dispatch detail (entry overhead 4 cog/13-20 hub; exit same; round-trip minimum 8 cog/26 hub; deferral conditions verbatim)
- `architecture/event_system.yaml` — replaced unsourced `latency: 3-8 clock cycles` and `event_detection_latency: 1 clock cycle` with verified mechanism + citation
- `architecture/debug_interrupt.yaml` — replaced unsourced `~10 clocks for minimal ISR` and `~20-30 clocks including hub write` with verified dispatch overhead breakdown

**PASM2 concept files (3 files):**
- `language/pasm2/concepts/stack_operations.yaml` — replaced "3 cycles" / "9 cycles" minimums with verified ranges from per-instruction YAMLs (added PUSHB/POPB to performance.operation_cycles)
- `language/pasm2/concepts/event_interrupt_config.yaml` — replaced unsourced `response_time: 3-4 cycles from event to ISR` and `debug_impact: ~20 cycles overhead` with verified ISR dispatch mechanism + citations
- `language/pasm2/concepts/skipf_branching.yaml` — corrected branch_timing to handle three cases (cog/LUT leap = 0 clocks; pipeline-cancel = 2-clock NOPs; hub-exec = always 2-clock NOPs per Silicon Doc verbatim "If SKIPF is used in hub exec, it will revert to SKIP behavior")

**Guides (1 file):**
- `guides/pasm2-getting-started.yaml` — replaced multiple `~20 clock cycles per access` / `~20 clocks` claims with verified per-op ranges

---

## Files NOT changed

- `architecture/p2-architecture-mental-model.yaml` — its "19-stage prefetch FIFO" claim is correct per Silicon Doc. Leave-as-is.
- All other PASM2 instruction YAMLs not in the 18-file `cycles: 1` list — they have correct timing values.

---

## Memory rules registered for future sessions

1. `feedback_no_unsourced_claims.md` — Bad info is outlawed; fix data-set-wide; don't ask about scope.
2. `feedback_no_interpreter_clock_timings.md` — Don't publish bytecode-interpreter clock counts. Use "we do not have a verifiable measurement" — never "varies with release."
3. `feedback_no_yaml_generators.md` — This KB does not use YAML generators. Editing source YAMLs in place is safe.

---

## Red-flag patterns for future sweeps

```bash
# Wrong hub-branch range:
grep -rn "4-16 (hub)\|4-16 clocks for branches\|4-16+ clocks" deliverables/

# Wrong cog-instruction time (1 cycle should be 2 clocks):
grep -rn "1 cycle per instruction\|single-cycle fetch" deliverables/

# Wrong FIFO depth (16 should be 19 in hubexec context):
grep -rn "16-long instruction cache" deliverables/

# Wrong CORDIC latency:
grep -rn "54 clocks for result\|337.5ns" deliverables/

# Unsourced bytecode-interpreter clock claims:
grep -rn "2-9 clock cycles\|~20-40 clock cycles\|~8 + .* clock cycles\|~10-20 clock cycles" deliverables/

# Pin Spin2 methods with bogus cog/hub split:
grep -rn "8-19 clock cycles when executed from hub" deliverables/

# Systematic timing.cycles:1 errors on hub-access ops:
grep -rn "^  cycles: 1$" deliverables/ai/P2/language/pasm2/

# "Varies with release" worry-language we should NOT use:
grep -rn "varies.*by.*release\|may change.*release" deliverables/
```
