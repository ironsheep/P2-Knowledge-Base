# Changeset-integrity audit — fleet-release gate (index)

**Gate:** §7.5 of the fleet-release plan (Stephen 2026-07-11 stake). Each target's diff since its
last public release is audited as an **independent adversarial pass** (fresh context, "disprove each
hunk is justified + proportionate", anchored to `P2KB-CORRECTION-FINDINGS` / EF ledger / commit
rationale). Per-hunk verdict: `traces-to-nothing` (scope-creep red flag) · `faithful` ·
`overstates-source` · `understates-source` · `introduces-new-claim`. Stephen reviews the REPORTS.
**Nothing renders (manuals) or publishes (KB) until this clears fleet-wide.**

## Targets & status

| # | Rail | Target | Baseline | Delta | Report | Status |
|---|------|--------|----------|-------|--------|--------|
| Y | yaml | full P2KB YAML delta | `v1.14.2` | 76 files (67 pasm2 z-flag `=`→`==` + rdpin F-204 + 8 debug-display enrichments) | `CHANGESET-AUDIT-yaml-delta-2026-07-11.md` | ✅ CLEAN — 0 flags (3 sub-threshold watch items); scope-creep claim independently re-verified (77 `z:` lines, 0 other fields) |
| 1 | manual | p2-debug-window-manual | `…-v1.0.2` | 58 files, ~1339+ | `CHANGESET-AUDIT-p2-debug-window-manual-…md` | 🔄 independent pass running |
| 2 | manual | p2-io-and-smart-pins-user-guide | `…-v1.0.4` | 34 files, ~350 | `CHANGESET-AUDIT-p2-io-and-smart-pins-…md` | 🔄 independent pass running |
| 3 | manual | p2-assembly-language-manual | `…-v3.1.2` | 9 files, ~235 | `CHANGESET-AUDIT-p2-assembly-…md` | 🔄 independent pass running |
| 4 | manual | p2-pasm-desilva-style | `…-v3.0.2` | 3 files, ~128 | `CHANGESET-AUDIT-p2-pasm-desilva-…md` | 🔄 independent pass running |
| 5 | manual | p2-streamer-programming-guide | `…-v1.0.5` | 1 file, ~14 (dense technical) | `CHANGESET-AUDIT-p2-streamer-…md` | 🔄 independent pass running |
| 6 | manual | p2-getting-started-guide | `…-v1.0.0` | 2 files, ~5 | (inline) | ✅ inline-cleared — faithful† |
| 7 | manual | p2-architect-guide | `…-v1.0.0` | 1 file, 1 line | (inline) | ✅ inline-cleared — faithful† |
| 8 | app-note | P2AN004 | `…-v1.0.0` | 2 files, ~3 (clock-spec + filter claims) | `CHANGESET-AUDIT-P2AN004-…md` | ✅ CLEAN — 3/3 faithful (each deletes a real defect; ≈600 ns FILT1 + 100–200 MHz VCO both verbatim-sourced; the removed "300 MHz max" was the actual fabrication) |
| 9 | app-note | P2AN001 | `…-v1.0.1` | 4 files (template-only, #160) | (pre-clear) | ✅ pre-cleared* |
| 10 | app-note | P2AN002 | `…-v1.0.0` | 4 files (template-only, #160) | (pre-clear) | ✅ pre-cleared* |
| 11 | app-note | P2AN003 | `…-v1.0.0` | 4 files (template-only, #160) | (pre-clear) | ✅ pre-cleared* |

\* P2AN001/002/003 deltas are the #160 diagram-mechanism template propagation — verified at copy time
to be byte-identical mechanism files from P2AN004 with **no per-note content changed** (inert, no
re-render). These trace cleanly to #160; pre-cleared (one-line, not a full pass).

† **Inline-cleared by Claude** (not an independent pass — say the word if you want full independence):
- **p2-architect-guide** — one line: PSRAM regrouped from the on-chip resource list to "external
  PSRAM" (geography correctness; PSRAM is off-chip). Traces to f3e702ed. `faithful`.
- **p2-getting-started-guide** — (a) PLANNING.md roster status In-dev→Done (bookkeeping, non-reader);
  (b) "the 16 hardware locks from Chapter 1"→"16 hardware locks" (P2 has exactly 16 — fact, dedup);
  (c) the "two-clocks-per-instruction" overclaim softened to "most register-to-register instructions
  execute in two clocks, while branches and hub accesses take more" (correct nuance, safe direction).
  Traces to f3e702ed. All `faithful`.

**Excluded (no delta since release):** p2an005, p2an006.
**Not in a release-delta audit (never released / in-dev / instruments):** p2-layout-torture-test,
p2-single-step-debugger-manual, p2-smart-pins-tutorial, p2-xbyte-programming-guide.

## Non-blocking follow-ups surfaced by the audit (not release gates)
- **P2AN004** — "sit comfortably within spec" is rhetorically loose (200 MHz is the *top edge* of the
  100–200 MHz VCO range, not mid-band); optional wording tweak. NOT a sourced-number error.
- **P2AN004 companion YAML** — the KB filename still reads `…frequency-period-pulse-measurement.yaml`
  while the note retitled Period→Rotation; findability/consistency drift → candidate ENH for the
  corrections register (out of scope for this release gate).

## Flow
1. YAML template pass (running) → Stephen reviews report + approves the format.
2. Fan out the 7 manual passes + P2AN004 (+ pre-clear the 3 template-only app-notes).
3. Consolidate flags → Stephen adjudicates → rejects loop back to fix→re-commit→re-audit.
4. Clean fleet-wide → unblocks #180 render wave.
