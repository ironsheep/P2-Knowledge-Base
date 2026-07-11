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
| Y | yaml | full P2KB YAML delta | `v1.14.2` | 76 files (≈38 pasm2 z-flag notation + rdpin F-204 + 8 debug-display enrichments) | `CHANGESET-AUDIT-yaml-delta-2026-07-11.md` | 🔄 running (template pass) |
| 1 | manual | p2-debug-window-manual | `…-v1.0.2` | 58 files, ~1339+ | — | ⏳ queued |
| 2 | manual | p2-io-and-smart-pins-user-guide | `…-v1.0.4` | 34 files, ~350 | — | ⏳ queued |
| 3 | manual | p2-assembly-language-manual | `…-v3.1.2` | 9 files, ~235 | — | ⏳ queued |
| 4 | manual | p2-pasm-desilva-style | `…-v3.0.2` | 3 files, ~128 | — | ⏳ queued |
| 5 | manual | p2-streamer-programming-guide | `…-v1.0.5` | 1 file, ~14 | — | ⏳ queued |
| 6 | manual | p2-getting-started-guide | `…-v1.0.0` | 2 files, ~5 | — | ⏳ queued (trivial) |
| 7 | manual | p2-architect-guide | `…-v1.0.0` | 1 file, 1 line | — | ⏳ queued (trivial) |
| 8 | app-note | P2AN004 | `…-v1.0.0` | 2 files, ~3 | — | ⏳ queued (trivial) |
| 9 | app-note | P2AN001 | `…-v1.0.1` | 4 files (template-only, #160) | — | ⏳ pre-cleared candidate* |
| 10 | app-note | P2AN002 | `…-v1.0.0` | 4 files (template-only, #160) | — | ⏳ pre-cleared candidate* |
| 11 | app-note | P2AN003 | `…-v1.0.0` | 4 files (template-only, #160) | — | ⏳ pre-cleared candidate* |

\* P2AN001/002/003 deltas are the #160 diagram-mechanism template propagation — verified at copy time
to be byte-identical mechanism files from P2AN004 with **no per-note content changed** (inert, no
re-render). These trace cleanly to #160; candidate for a one-line pre-clear rather than a full pass.

**Excluded (no delta since release):** p2an005, p2an006.
**Not in a release-delta audit (never released / in-dev / instruments):** p2-layout-torture-test,
p2-single-step-debugger-manual, p2-smart-pins-tutorial, p2-xbyte-programming-guide.

## Flow
1. YAML template pass (running) → Stephen reviews report + approves the format.
2. Fan out the 7 manual passes + P2AN004 (+ pre-clear the 3 template-only app-notes).
3. Consolidate flags → Stephen adjudicates → rejects loop back to fix→re-commit→re-audit.
4. Clean fleet-wide → unblocks #180 render wave.
