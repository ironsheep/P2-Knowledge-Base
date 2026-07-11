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
| 2 | manual | p2-io-and-smart-pins-user-guide | `…-v1.0.4` | 34 files, ~350 | `CHANGESET-AUDIT-p2-io-and-smart-pins-…md` | ✅ CLEAN — ~120 hunks all traced (FABRICATION-AUDIT-SWEEP-CATALOG 148-row proofs + F-173/F-202/C-65); 8 examples compile+byte-identical; real bug-fixes confirmed (REV, PINLOW wrap) |
| 3 | manual | p2-assembly-language-manual | `…-v3.1.2` | 9 files, ~235 | `CHANGESET-AUDIT-p2-assembly-…md` | ⚠️ 2 FLAGS (mostly clean — 7 fabrications removed, AUG↔EF-033 confirmed): (1) Ch5 §5.7.6 vs Ch4 §4.1.4 clock-field naming contradiction introduced here — needs relabel; (2) GETCT 4→2 reasoning-derived, optional annotate. Neither is a fabrication. |
| 4 | manual | p2-pasm-desilva-style | `…-v3.0.2` | 3 files, ~128 | `CHANGESET-AUDIT-p2-pasm-desilva-…md` | ✅ CLEAN — ~46 hunks faithful (sweep-catalog proofs); 8 high-risk claims independently re-verified (TESTP polarity flip, per-cog→shared CORDIC fab, async-TX P_OE); examples byte-identical |
| 5 | manual | p2-streamer-programming-guide | `…-v1.0.5` | 1 file, ~14 (dense technical) | `CHANGESET-AUDIT-p2-streamer-…md` | ✅ CLEAN — 7/7 faithful, each verbatim-Silicon-Doc-sourced (NCO 32-bit-mask L2747, xinit L3512, VESA porch, $BF85 from X_DACS, long-align L6673); fixes a materially wrong FIFO-alignment claim |
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

## FLAGS awaiting Stephen adjudication (Assembly manual)
- **FLAG 1 — CONFIRMED (hand-verified), fix ready.** Ch5 §5.7.6 (`chapter-05-hardware.md:690`)
  labels the clock-config low fields `PPPP_XX_CC` with **XX=caps, CC=source**; Ch4 §4.1.4
  (`chapter-04-timing.md:71`, changed in this set) uses **CC=caps, SS=source** — the P2/Silicon-Doc
  standard. `CC` therefore means *source* in Ch5 and *caps* in Ch4. Bit values correct in both (code
  assembles); reader-decoding contradiction only. **Fix:** relabel Ch5 to the standard `PPPP_CC_SS`
  (`XX`→`CC`=caps, `CC`→`SS`=source) in the config-word line + comment. Recommend: apply.
- **FLAG 2 — optional.** GETCT overhead `4→2` cycles is reasoning-derived, not EF-grounded (the old
  `4` was equally unsourced; `2` is the more defensible figure). Recommend: annotate as an estimate
  (or leave — it raises correctness either way). Not a release blocker.

## Non-blocking follow-ups surfaced by the audit (not release gates)
- **Fleet-wide release-prep (IOSP audit):** the correction sweeps intentionally left CHANGELOGs
  un-bumped and un-rendered ("No version bumps, no re-render"). Each releasing manual needs its
  CHANGELOG entry authored (the audit reports are the input) + a re-render before ship — that IS the
  #180 render-wave / #181 release-wave prep, not an audit gap.
- **Streamer (out-of-scope):** the App-A mode table's adjacent 2-pin/4-pin RFBYTE rows still show
  `%ppp0`/`%pp00` where the Silicon Doc shows the `a` alt-bit (`pp0a`/`p00a`); this commit correctly
  fixed only the two 1-pin rows. Candidate for the next fabrication-audit pass (not this changeset).
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
