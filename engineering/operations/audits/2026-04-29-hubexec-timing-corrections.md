# Hubexec Timing & Inline-PASM Execution-Mode Corrections

**Date:** 2026-04-29
**Auditor:** Claude (Opus 4.7) under user direction
**Scope:** P2 hubexec instruction timing model; Spin2 inline PASM execution context; FIFO depth & forbidden-instruction list; cog/LUT execution timing baseline
**Severity:** High — multiple files were propagating wrong timing claims and a wrong execution-mode claim to AI consumers of the KB
**Status:** Fixed in this session (verified against Silicon Doc v35 primary source)

---

## Summary

Initial review (round 1) flagged three errors. Deep root-source verification then revealed:
1. The originally-flagged errors were real and broader than first cataloged.
2. Round-1 fixes themselves introduced **new wrong numbers** (used 4-16 clocks where the correct figure is minimum 13; framed FIFO/streamer instructions as "slow" when they are actually FORBIDDEN in hubexec).
3. Two additional files (`execution_modes.yaml`, `architecture/fifo.yaml`) carried adjacent errors / gaps that needed correction.

Round 2 of edits applies root-source-verified numbers throughout. This memo documents the final, verified state.

---

## Authoritative model (verified from primary sources)

All numbers below are cross-checked against:
- `engineering/ingestion/sources/silicon-doc/p2-documentation.txt` (Silicon Doc v35 raw text)
- `engineering/ingestion/sources/silicon-doc/INSTRUCTION-TIMING-AND-ENCODING.md`
- Per-instruction YAMLs in `deliverables/ai/P2/language/pasm2/` (compiler-extracted clock counts)
- Chip Gracey clarification (where Silicon Doc is qualitative rather than quantitative)

| Fact | Value | Citation |
|---|---|---|
| Cog/LUT typical ALU instruction (ADD, MOV, etc.) | **2 clocks** | `add.yaml: cycles 2 fixed`, `mov.yaml: cycles 2`; Silicon Doc: "2-clock execution for most math/logic instructions" |
| Cog/LUT branch (JMP, CALL, RET) | **4 clocks** | `jmp.yaml: clocks 4`, `call.yaml: cycles 4`, `ret.yaml: cycles 4` |
| Cog/LUT DJNZ | **2 clocks not-taken / 4 clocks taken** | `djnz.yaml: encoding clocks "2 or 4"` |
| **Hub-exec sequential streaming** | **2 clocks/instruction (IDENTICAL to cogexec)** | Silicon Doc HUB EXECUTION: "FIFO hardware to spool up instructions so that a stream of instructions will be available for continuous execution"; Chip Gracey clarification supplies the explicit "2 clocks" figure |
| Hub-exec branch refill | **Minimum 13 clocks; +1 if target not long-aligned** | Silicon Doc verbatim: *"Branching to a hub address takes a minimum of 13 clock cycles. If the instruction being branched to is not long-aligned, one additional clock cycle is required."* `jmp.yaml`/`call.yaml`/`ret.yaml: range 4 / 13...20` |
| Hub-exec DJNZ taken | **13...20 clocks** | `djnz.yaml: range 13...20` |
| FIFO depth | **(cogs+11) = 19 stages on 8-cog P2** | Silicon Doc verbatim: *"The FIFO contains (cogs+11) stages."* |
| FIFO refill threshold | **Loads when fewer than (cogs+7) = 15 stages filled; then up to 5 more longs may stream in** | Silicon Doc verbatim |
| **FIFO/streamer instructions in hubexec** | **FORBIDDEN, not slow** | Silicon Doc verbatim: *"While in hub execution mode, the FIFO cannot be used for anything else. So, during hub execution these instructions cannot be used: RDFAST / WRFAST / FBLOCK / RFBYTE / RFWORD / RFLONG / RFVAR / RFVARS / WFBYTE / WFWORD / WFLONG / XINIT / XZERO / XCONT - when the streamer mode engages the FIFO."* |
| Hub I/O (RDLONG/WRLONG/etc.) in hubexec | **Same as cogexec: 9-24 clocks reads, 3-12 clocks writes** (egg-beater dependent) | Silicon Doc HUB section, hub-window timing |
| Inline PASM in Spin2 method | **Loaded into cog RAM at runtime; runs as cog-exec, NOT hub-exec** | Spin2 v51 docs; production-code analysis; corroborates `inline_pasm2.yaml` original wording |

---

## Findings & corrections

### Round 1 (originally flagged) — now superseded by round 2 numbers

**Finding 1:** `p2kbPasm2CogHubExecution` (`cog_hub_execution.yaml`) characterized hubexec speed as "Variable (4-16+ clocks per instruction)" and claimed "Math: 2 clocks (cog) vs 4-16 (hub)." Both wrong — sequential hubexec is 2 clocks/instruction.

**Finding 2:** `p2kbPasm2Hubexec` (`hubexec.yaml`) note said "Slower than cog execution due to hub access timing" without distinguishing sequential vs branch.

**Finding 3:** `p2kbSpin2InlinePasm` (`inline_pasm.yaml`) claimed inline PASM "Runs in hub-exec mode at current location." Wrong — runs as cog-exec.

### Round 2 (deep-verification additions and self-corrections)

**Self-correction A:** Round-1 edits to `cog_hub_execution.yaml`, `hubexec.yaml`, and `inline_pasm.yaml` used "4-16 clocks" for hub-branch refill. **Correct figure is minimum 13 clocks (+1 if not long-aligned)** per Silicon Doc verbatim. Fixed throughout.

**Self-correction B:** Round-1 edits framed FIFO/streamer instructions as "FIFO-disrupting" with a timing cost. **They are forbidden in hubexec, not slow.** Reframed throughout with the explicit forbidden list.

**Self-correction C:** Round-1 said "FIFO is 16 longs deep." **Correct figure is 19 stages ((cogs+11) on 8-cog P2)** per Silicon Doc verbatim. Fixed.

**Self-correction D:** Round-1 used "JMP: 2 clocks (cog) vs 4-16 (hub)" and similar for CALL/RET/DJNZ. **Correct cog branch time is 4 clocks** (not 2) per per-instruction YAMLs. Fixed.

**New finding E:** `execution_modes.yaml` had systematic "1 cycle per instruction" claims for cog/LUT execution. **Correct figure is 2 clocks per typical instruction.** Also wrong: `fifo_buffering: "16-long instruction cache"`, `branch_penalties.within_cog: "2 cycles"`, `branch_penalties.within_hub: "2-19 cycles (FIFO reload)"`, `instruction_timing.hub_exec: "1-17 cycles"`. All fixed with verified numbers.

**New finding F:** `architecture/fifo.yaml` documented only the streamer/software-transfer role of the FIFO (64-byte blocks, RDFAST/WRFAST). It was silent on the hubexec instruction-prefetch role and the (cogs+11) = 19-stage depth in that role. **Enriched** (not corrected) with a second-role section, the depth/threshold figures, and the forbidden-in-hubexec list.

### Files that turned out to be correct

`p2-architecture-mental-model.yaml` — claim of "19-stage prefetch FIFO" is **CORRECT** per Silicon Doc (cogs+11). I had incorrectly flagged this for change in round 1; the verification confirmed leave-as-is.

`pin*.yaml` (pinhigh, pinlow, pintoggle, pinread, pinwrite, pinfloat) — `hub_access: "8-19 clock cycles when executed from hub"` is a Spin2-method total-time estimate that does not trace to a single primary-source figure but is not provably wrong. Silicon Doc cites bytecode-dispatch overhead of 9 clocks (default) or 8 clocks (with XBYTE), so the "8-19" range is plausible. **Left unchanged.** Flagged here for future verification if a tighter primary source surfaces.

---

## Final list of changes applied (round 1 + round 2 combined)

| File | Final state |
|------|------|
| `language/pasm2/concepts/cog_hub_execution.yaml` | Major rewrite. Correct numbers: cog ALU 2 clocks; cog branch 4 clocks; hubexec sequential 2 clocks; hubexec branch min 13 (+1 misaligned). New canonical `fifo_behavior:` block citing Silicon Doc verbatim. Forbidden-instruction list explicit. `hubexec_forbidden_instructions:` section. Cross-references upgraded to full-path form. |
| `language/pasm2/hubexec.yaml` | Notes block expanded with verified per-case timings + forbidden list + FIFO depth (19 stages). Cross-refs added. |
| `language/spin2/constructs/inline_pasm.yaml` | New `execution_model:` section establishing cog-exec semantics. All four `syntax_forms[].execution:` strings rewritten. `local_label_rule:` merged from sibling. Round-2 update: cog-branch=4 clocks; hub-form description cites min 13 clocks + forbidden FIFO/streamer list. |
| `language/spin2/concepts/inline_pasm2.yaml` | Demoted to redirect stub. Eliminates content drift; preserves `p2kbSpin2InlinePasm2` key for back-compat. |
| `language/pasm2/concepts/execution_modes.yaml` | All "1 cycle per instruction" claims corrected to "2 clocks per typical instruction." FIFO depth corrected from 16 longs to 19 stages. Branch penalties corrected (cog=4, hub min 13). Forbidden-instruction list added to hub_execution. Sources cited inline. |
| `architecture/fifo.yaml` | Enriched with hubexec instruction-prefetch role (19 stages, refill threshold, forbidden list). Streamer/software-transfer role description preserved. `verification_notes:` block added with Silicon Doc verbatim quotes. |

---

## Files NOT changed

- `architecture/p2-architecture-mental-model.yaml` — its "19-stage prefetch FIFO" claim is correct per Silicon Doc. Leave-as-is.
- `language/spin2/methods/pin*.yaml` — "8-19 clocks when executed from hub" is a fuzzy total-method estimate that does not contradict primary source.

---

## Source citation policy enforced in this round

Every changed timing claim now carries either:
- An inline `source:` line citing the Silicon Doc section verbatim, or
- A cross-reference to a per-instruction YAML whose timing was extracted directly from the PASM2 Manual 2022/11/01 / pnut compiler.

For the single sequential-hubexec figure (2 clocks) where the Silicon Doc is qualitative ("stream of instructions ... continuous execution") rather than quantitative, both the Silicon Doc text AND Chip Gracey's clarification are cited together.

---

## Red-flag patterns to grep for in future audits

```bash
# Wrong hub-branch range (should be 13-20, not 4-16):
grep -rn "4-16 (hub)\|4-16 clocks for branches" deliverables/

# Wrong cog-instruction time (should be 2 clocks, not 1 cycle):
grep -rn "1 cycle per instruction\|single-cycle fetch" deliverables/

# Wrong FIFO depth (should be 19 stages / (cogs+11), not 16 longs in hubexec context):
grep -rn "16-long instruction cache\|16 longs deep" deliverables/

# Wrong framing of forbidden instructions as "slow":
grep -rn "FIFO-disrupting" deliverables/  # verify each is correctly framed
```

---

## Verification steps performed

1. Read Silicon Doc HUB EXECUTION section verbatim from `engineering/ingestion/sources/silicon-doc/p2-documentation.txt`.
2. Cross-checked timing claims against per-instruction YAMLs (`jmp.yaml`, `call.yaml`, `ret.yaml`, `djnz.yaml`, `add.yaml`, `mov.yaml`, `drvh.yaml`).
3. Read all four edited files in full before and after editing.
4. Confirmed all `related:` cross-reference targets exist on disk.
5. After edits, ran the seven-step publishing process (validate-yaml-syntax → validate-crossref-keys → generate-p2kb-index → update-p2-reference-complete → gzip → validate-dod-release → spot-check) — see commit log for results.
