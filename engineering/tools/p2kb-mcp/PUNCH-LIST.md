# P2KB Download-on-Demand System — Punch List

*Created: 2026-02-27*
*Last Updated: 2026-05-07*

Backlog of improvements, fixes, and audit tasks for the P2KB MCP / Download-on-Demand system and its underlying YAML knowledge base.

---

## Open Items

### PL-004: Remove version/currency stamps from the published YAMLs — the KB is always "latest"

**Priority:** Low — **PARTS 1 AND 3 DONE 2026-08-21; PART 2 STILL OPEN**
**Discovered:** 2026-08-16, from F-271 (`P2KB-CORRECTION-FINDINGS.md`)
**Decided:** 2026-08-16 by Stephen

**The principle, and it is the durable half.** **The published KB has exactly one edition: the
current one.** Every reference to it means *latest*. Nothing in the tree should cite currency or a
version, because there is no other edition to distinguish it from — and a stamp we must keep true
is a maintenance burden that buys nothing. Anything that reads as "as of version X" is a defect in
shape, not a value to keep updated.

**Why this came up.** F-271 found all seven `application-notes/*.yaml` companions frozen at their
maiden `version:` while their notes had moved to 1.0.1–1.0.3. The first two proposed fixes were both
wrong: stamping them (adds a fourth version location to maintain forever) and then a
`describes_document:` block (still a currency citation). The right answer is that the field should
not exist. **Delete the shape, do not maintain it.**

**Scope when this is worked:**
- **Delete** the bare `version:` from the **7 app-note companions** — inert (nothing consumes it;
  the index detects change by `mtime` + `sha256`), ambiguous, and currently false.
- **Review the other 17** `version:`/`last_updated:` bearers (`architecture/smart_pins.yaml`,
  `architecture/streamer/_index.yaml`, `spin2/conventions/*`, `guides/*`, the `_index.yaml` files)
  against the same principle. These use it as a *file revision*, which is a coherent convention but
  still a currency citation the "always latest" rule argues against. **Grounded decision needed per
  population — do not sweep on the app-note reading.** (F-211's lesson: a class-wide sweep amplifies
  whatever fact it starts with.)
- Sweep prose in published YAMLs for the same shape — "as of", "current as of", "latest version is".
- **Out of scope:** PDF manuals and app notes ARE versioned (cover + `request.json` + Revision
  History, per the three-version-locations rule), and the roster tracks those. This item is about
  the **KB/YAML layer only**, which ships continuously rather than in editions.

**Timing — gate DISCHARGED.** Stephen, 2026-08-16: *"we punch list it at this point because we are
trying to get to released documents, and we are not there yet given our task list."* Sprint 2's
release wave came first, and **Sprint 2 closed 2026-08-19**, so the condition was met.

**DONE 2026-08-21 — parts 1 and 3.**
- **Part 1:** the bare `version:` deleted from all seven app-note companions. Verified by parsing:
  no `version` key remains in any of them; `doc_id` untouched.
- **Part 3:** 25 build stamps rewritten across the tree, plus the `version_info` block in
  `tools/pnut-ts-compiler.yaml` — which read **v1.51.5, four minor versions behind** and was itself
  the proof of the principle. The line applied throughout is **cite the EDITION, never the BUILD**:
  `Spin2 v55` / `Added in PNut v47` / `{Spin2_v54}` / `minimum_version:` state a fact about the
  LANGUAGE that a reader can hit — all **278** survive untouched — while `compile-verified with
  pnut_ts v1.55.0` records only what someone happened to run. The seven app-note `toolchain:` lines
  were EDITED rather than deleted: their `-d` requirement, `_clkfreq` value and
  `{Spin2_v45}`/`{Spin2_v47}` gating are durable and load-bearing; only the `1.55` clause went.
- Removed under the same principle: `object-image-dedup.yaml`'s `toolchain:` line, which said
  *"pnut-ts v1.55.0 … re-verify on a compiler version bump"* while the installed compiler was
  v1.55.3 — the bump had happened, the re-verification had not, and the stamp had triggered nothing.
  A `method:` line saying how to measure replaced it. See **G-006**.

**STILL OPEN — part 2.** The other 17 `version:`/`last_updated:` bearers
(`architecture/smart_pins.yaml`, `architecture/streamer/_index.yaml`, `spin2/conventions/*`,
`guides/*`, the `_index.yaml` files) use the field as a *file revision* — a different population with
a coherent internal convention. The grounded per-population decision this item requires has NOT been
made, and they were deliberately not swept on the app-note reading (F-211's lesson). Also still open:
the prose sweep for "as of" / "current as of" / "latest version is".

---

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
