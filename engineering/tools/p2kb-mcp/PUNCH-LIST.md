# P2KB Download-on-Demand System — Punch List

*Created: 2026-02-27*
*Last Updated: 2026-05-07*

Backlog of improvements, fixes, and audit tasks for the P2KB MCP / Download-on-Demand system and its underlying YAML knowledge base.

---

## Open Items

*(none open — see Completed Items below)*

---

## Completed Items

### PL-003: SPI/SD/Protocol Content Lacks Timing-Method Guidance

**Priority:** High
**Discovered:** 2026-05-07 — An agent-authored SD card driver (built using P2KB) shipped with a GETCT-overflow bug and is being re-released to fix it. The agent had GETCT, GETMS, and GETSEC docs available but no domain-aware guidance pointing to GETMS for protocol-level timeouts. P2KB's mission is AI-optimized documentation for code generation; an agent shipping buggy code from a doc gap is a mission-level failure.
**Closed:** 2026-05-08 — Sweep completed. Reframed from "SD-card content gap" to "protocol-layer guidance gap": every SD/SPI-flash/SPI-sensor driver lands on the same SPI smart-pin pages, so fixing protocol-layer pages covers all driver-domain consumers.

**Work delivered (in the same commit that closed this item):**
- **Real bug fixes:** `methods/locktry.yaml` "Lock with timeout" example switched to wrap-aware compare; `concepts/timing_operations.yaml` `PUB ms_to_cycles` and `periodic_execution` pattern annotated with their overflow ceilings.
- **Annotation:** `methods/wxpin.yaml` `set_measure_ms` flagged with the overflow ceiling for the same trap in a smart-pin-X-register context.
- **Protocol-layer cross-references** to `language/spin2/concepts/timing_operations.yaml#method_selection` from: `architecture/smart_pin_patterns.yaml`, `architecture/smart_pins.yaml`, `architecture/io_pin_timing.yaml`, `language/pasm2/concepts/streamer_smartpin_control.yaml`, `language/spin2/patterns/applications/single_communication.yaml`.
- **Foundation (delivered in the prior session that filed this item):** `concepts/timing_operations.yaml` `method_selection` decision table; `getct_long_timeout` anti-pattern with the SDSC 24-second incident as the worked example; ms→cycles formula entry now flags overflow.

**Out of scope (verified during sweep):** No SD-card content currently exists in `community/obex/`. Hardware board YAMLs and architecture summary files have no timeout idioms requiring changes. Files mentioning the *word* "timeout" without a timeout *idiom* were not cross-referenced (signal-to-noise call).

### PL-001: Audit All YAML Instruction Timing Against Silicon Doc

**Priority:** Medium
**Discovered:** 2026-02-27 — WAITX timing error (description said "D+1", silicon doc says "2+D"; WC/WZ/WCZ randomized delay behavior was completely missing)
**Closed:** 2026-05-07 — **Superseded** by data-set-wide content audits, rounds 1–6 (and ongoing). The systematic timing/prose comparison this item called for has effectively been done across the YAML corpus through a series of broader audits.

**Superseding work (commits, oldest first):**
- `fbbd9ee` — Correct hub-exec timing model and inline-PASM execution-mode claims
- `96cf4e8` — Data-set-wide timing-claim corrections (round 3)
- `e77d676` — Correct REP/ALTI hubexec availability and inline-PASM 16-long limit (round 4)
- `f5b5a63` — Generalize ALTx family + multitasking taskptr caveat + ORGH inline (round 5)
- `a88ad9c` — Remove compiler bytecode values and bc_-prefixed symbol names (round 6)
- `c48cf81` / `85fc02f` — Async-serial N-1 word size and MSB-justified RX corrections

If a narrowly-scoped CSV-field comparison is still wanted later, it should be filed as a fresh item with the residual scope clearly delineated against what rounds 1–6 already covered.

### PL-002: p2kb_refresh Does Not Reload Index Structure

**Priority:** High
**Discovered:** 2026-02-27 — Added new YAML, regenerated index (1027→1028 entries), called p2kb_refresh. Server returned `refreshed: true` but `total_entries` stayed 1027. New key not discoverable.
**Closed:** 2026-05-07 — Resolved (per repo owner; MCP server source lives outside this tree).
