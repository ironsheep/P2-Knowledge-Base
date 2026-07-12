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
| 1 | manual | p2-debug-window-manual | `…-v1.0.2` | 58 files, ~1339+ | `CHANGESET-AUDIT-p2-debug-window-manual-…md` | ⚠️ 3 FLAGS (all hand-verified CONFIRMED) — rest clean (15/15 examples compile+byte-identical, ~30 correction-groups faithful). All 3 = same class: f3e702ed trusted v55 over Pascal/REF. F1 HIGH PRECISE-default inverted, F2 MED Lime→Green (vs EF-025), F3 LOW-MED LOGIC DOTSIZE row dropped. |
| 2 | manual | p2-io-and-smart-pins-user-guide | `…-v1.0.4` | 34 files, ~350 | `CHANGESET-AUDIT-p2-io-and-smart-pins-…md` | ✅ CLEAN — ~120 hunks all traced (FABRICATION-AUDIT-SWEEP-CATALOG 148-row proofs + F-173/F-202/C-65); 8 examples compile+byte-identical; real bug-fixes confirmed (REV, PINLOW wrap) |
| 3 | manual | p2-assembly-language-manual | `…-v3.1.2` | 9 files, ~235 | `CHANGESET-AUDIT-p2-assembly-…md` | ⚠️ 2 FLAGS (mostly clean — 7 fabrications removed, AUG↔EF-033 confirmed): (1) Ch5 §5.7.6 vs Ch4 §4.1.4 clock-field naming contradiction introduced here — needs relabel; (2) GETCT 4→2 reasoning-derived, optional annotate. Neither is a fabrication. |
| 4 | manual | p2-pasm-desilva-style | `…-v3.0.2` | 3 files, ~128 | `CHANGESET-AUDIT-p2-pasm-desilva-…md` | ✅ CLEAN — ~46 hunks faithful (sweep-catalog proofs); 8 high-risk claims independently re-verified (TESTP polarity flip, per-cog→shared CORDIC fab, async-TX P_OE); examples byte-identical |
| 5 | manual | p2-streamer-programming-guide | `…-v1.0.5` | 1 file, ~14 (dense technical) | `CHANGESET-AUDIT-p2-streamer-…md` | ✅ CLEAN — 7/7 faithful, each verbatim-Silicon-Doc-sourced (NCO 32-bit-mask L2747, xinit L3512, VESA porch, $BF85 from X_DACS, long-align L6673); fixes a materially wrong FIFO-alignment claim |
| 6 | manual | p2-getting-started-guide | `…-v1.0.0` | 2 files, ~5 | (inline) | ✅ inline-cleared — faithful† |
| 7 | manual | p2-architect-guide | `…-v1.0.0` | 1 file, 1 line | (inline) | ✅ inline-cleared — faithful† |
| 8 | app-note | P2AN004 | `…-v1.0.0` | 2 files, ~3 (clock-spec + filter claims) | `CHANGESET-AUDIT-P2AN004-…md` | ✅ CLEAN — 3/3 faithful (each deletes a real defect; ≈600 ns FILT1 + 100–200 MHz VCO both verbatim-sourced; the removed "300 MHz max" was the actual fabrication) |
| 9 | app-note | P2AN001 | `…-v1.0.1` | template (#160) + **5-hunk content delta** | `CHANGESET-AUDIT-app-notes-content-…md` | ✅ CLEAN — 5/5 faithful (power-groups 4→8, SINC2 filtering, below-ground unsigned-wrap); each fixes a real defect. → F-211 (companion YAML drift). |
| 10 | app-note | P2AN002 | `…-v1.0.0` | template (#160) + **3-hunk content delta** | `CHANGESET-AUDIT-app-notes-content-…md` | ✅ CLEAN — 3/3 faithful (2³² overflow; OBEX #2812→ersmith, #5361→James Smith, both catalog-verified) |
| 11 | app-note | P2AN003 | `…-v1.0.0` | template (#160) + **1-hunk content delta** | `CHANGESET-AUDIT-app-notes-content-…md` | ✅ CLEAN — PWM dither fixed at Fclock/256 (Silicon L7936); fixes a real defect |
| 12 | app-note | P2AN005 | `…-v1.0.0` | **1-hunk content delta** | `CHANGESET-AUDIT-app-notes-content-…md` | ✅ CLEAN — "P2 has no hardware mutex" was false (P2 has 16 locks); fix removes it |

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

**Excluded (no delta since release):** p2an006. *(p2an005 was wrongly excluded — it has a 1-hunk content delta, now audited clean as row 12.)*
**Not in a release-delta audit (never released / in-dev / instruments):** p2-layout-torture-test,
p2-single-step-debugger-manual, p2-smart-pins-tutorial, p2-xbyte-programming-guide.

## Class-wide v55-over-Pascal sweep RESULT (2026-07-11) — class NOT clear; 5 more + 1 conflicted
The sweep paid off (report: `CHANGESET-AUDIT-debug-v55-over-pascal-sweep-2026-07-11.md`). The empirical
batch EF-025..032 had already reverted several (LOGIC ranges, FFT filled-bars, MIDI color, SCOPE size),
but **BITMAP was never conflict-tested** and POS/TITLE/FFT-legend were in no EF — so these slipped:
- **F-1 (FFT)** `grid`→"legend" fabricates bits 2–3 (Pascal FFT tests only bits 0/1 = baseline/top lines). *Fabrication.*
- **F-2 (BITMAP)** SPARSE reworded to round-dot/background/≥4; Pascal = bordered square blocks (vSparse=grid color), no ≥4 gate. Pre-sweep was correct.
- **F-3 (BITMAP)** LUT-without-palette "entries 0–7 default"; Pascal = uninitialized/garbage until LUTCOLORS. Pre-sweep was correct.
- **F-4 (POS default)** TERM/LOGIC/SCOPE_XY/MIDI say `0,0`; REF = cascaded/auto (windows cascade, not screen origin).
- **F-5 (TITLE default)** TERM/PLOT/LOGIC say `none`; REF = "(window name)".
- **S-6 (CONFLICTED)** "half-pixels" relabel of SCOPE/FFT LINESIZE + SCOPE_XY DOTSIZE: radius-arithmetic supports it, but **EF-027 measured LINESIZE 3→3px (1:1)** and LOGIC chapter says "pixels" for the same primitive → likely error; settle by reverting to "pixels" OR one targeted hardware test.
- **N-1** PLOT dropped accurate "default text color white ($FFFFFF)" — restore.
**APPLIED 2026-07-11 (commit `91eacf4b`), but STATUS SPLIT after Stephen's authority-model correction
(the agent-derived REF does NOT auto-outrank v55 — reconcile + prove, don't rank):**
- **SOLID — empirical:** S-6 (EF-027). *(D-F2 Lime = EF-025, solid, applied earlier.)*
- **SOLID — fabrication (no source supports the removed claim):** F-1 FFT legend-text bits 2–3 (pending a
  one-line confirm that v55 is also silent on legend text — if so, invented regardless of ranking).
- **⚠️ PROVISIONAL / UNRECONCILED — rest on the agent-derived REF alone:** D-F1 PRECISE, D-F3 DOTSIZE,
  F-2 BITMAP, F-3 LUT, F-4 POS, F-5 TITLE, N-1 text-color. **These must NOT ship as authoritative.**
  **Gate:** Debug re-audit/render is BLOCKED until reconciled — REF agent re-audits each against the
  **raw `DebugDisplayUnit.pas`** (non-circular; the raw `.pas` is NOT in-repo) reporting supports-v55 /
  supports-REF / silent; silent-or-render-dependent → hardware render test (PRECISE, BITMAP SPARSE,
  POS cascade, TITLE are directly visual on Stephen's rig). Awaiting Stephen to point the REF agent at
  the raw source.

## FLAGS — Debug manual (all hand-verified CONFIRMED) — ✅ ADJUDICATED + FIXED 2026-07-11 (F-209)
**Stephen agreed with recommendations; all three reverted in opus-master.** Class-wide v55-over-Pascal
sweep RUNNING to catch any others before Debug re-audit. **One class:** the pre-empirical sweep
`f3e702ed` trusted **v55 text over the higher-authority Pascal/REF** for the DEBUG windows.
- **F1 — HIGH — PRECISE default inverted (ch05-plot.md).** Manual now says sub-pixel is OFF by
  default / one `PRECISE` turns it ON. REF (Pascal-derived) is unambiguous: `vPrecise := 8` at
  `PLOT_Configure` = sub-pixel **ON at creation**, `PRECISE` XORs 8↔0. So one `PRECISE` turns it
  **OFF** — reader who wants smooth curves gets aliased output, the opposite of intent. Only source
  for "off" is v55 L1271. **Fix:** revert to sub-pixel-default (Pascal/REF). *Adjudicate: revert now,
  or hardware-verify (a "Test K") first? — mirrors the F-205 source-conflict pattern.*
- **F2 — MED — TERM default "Lime"→"Green" (ch03 + appendix-c + 2 example comments).** EF-025
  CONFIRMED default = `clLime $00FF00`, distinct from `GREEN` kw `$09FF09`; its disposition is
  explicitly "keep Lime, add reader-note (no LIME kw; reproduce with GREEN)." Sweep applied the
  inverted v55 reading; contradicts EF-025 + `term.yaml`. **Fix:** restore Lime + reader-note.
- **F3 — LOW-MED — LOGIC DOTSIZE config row removed (ch06-logic.md).** REF matrix L90 `DOTSIZE ✅`
  + L260 lists it in LOGIC config; sweep deleted it on v55's omission. **Fix:** restore the row.
- **Systemic (class-wide sweep):** since all 3 are the same v55-over-Pascal class, before fixing do a
  systematic pass over `f3e702ed`'s remaining **Debug** edits, cross-checking every DEBUG-window
  behavioral claim against the Pascal/REF theory-of-ops + directive matrix, to catch any other
  reversals — then fix the whole class + re-audit (feedback_classwide_sweep_on_every_finding).

## FLAGS — Assembly manual
- **FLAG 1 — ✅ FIXED 2026-07-11 (F-210).** Ch5 relabeled to standard `PPPP_CC_SS`. (Was:)
  **CONFIRMED (hand-verified), fix ready.** Ch5 §5.7.6 (`chapter-05-hardware.md:690`)
  labels the clock-config low fields `PPPP_XX_CC` with **XX=caps, CC=source**; Ch4 §4.1.4
  (`chapter-04-timing.md:71`, changed in this set) uses **CC=caps, SS=source** — the P2/Silicon-Doc
  standard. `CC` therefore means *source* in Ch5 and *caps* in Ch4. Bit values correct in both (code
  assembles); reader-decoding contradiction only. **Fix:** relabel Ch5 to the standard `PPPP_CC_SS`
  (`XX`→`CC`=caps, `CC`→`SS`=source) in the config-word line + comment. Recommend: apply.
- **FLAG 2 — optional.** GETCT overhead `4→2` cycles is reasoning-derived, not EF-grounded (the old
  `4` was equally unsourced; `2` is the more defensible figure). Recommend: annotate as an estimate
  (or leave — it raises correctness either way). Not a release blocker.

## Resolved threads
- **DEBUG TX/RX "reversal" (Stephen's rig) — RESOLVED 2026-07-11: it's a `pnut-ts` BUG (being patched),
  not a doc/silicon issue.** Triangulation closed it: v55 (`DEBUG_PIN_TX=62`/`RX=63`), both Edge boards
  (`P62=P2-TX`/`P63=P2-RX`), and our YAMLs all agree AND the rig is hardwired-standard AND DEBUG output
  worked all project → the tool was the only variable left. **No deliverable change** — the docs are
  validated correct; tool fix per "PNut is ground truth, tool bug = code fix." Not a corrections-register item.

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
- **P2AN004 companion YAML** — ~~the KB filename still reads `…frequency-period-pulse-measurement.yaml`
  while the note retitled Period→Rotation~~ **✅ RESOLVED 2026-07-11 (Stephen: retitle).** The note is
  now formally *Frequency / Rotation / RC-Timing Measurement* (its three instruments have no period/pulse
  recipe). Aligned in one coherent move: companion YAML renamed
  `…-frequency-rotation-rc-timing-measurement.yaml` + `title:`; manual-head source-of-truth updated
  (CHANGELOG, MANUAL-DESCRIPTOR, NOTES, PUBLICATION-ROSTER, app-notes/README, analysis roster). Published
  `deliverables/documents/` area + index key regen ride release-manual/release-yamls at §9 (they lag
  until publish); historical records (dated audit, PUBLISH ledger, ingestion source-map) left as-is.

## ⚠️ OPEN GAPS discovered 2026-07-11 (late) — MUST close before the release wave
The `f3e702ed` sweep ("342 fixes across 13 docs") touched more than the big manuals. Two gaps:

**A. Audit gap — app-note CONTENT deltas were NOT changeset-audited.** I mis-"pre-cleared"
P2AN001/002/003 as *template-only* (the #160 propagation) and marked P2AN005 as *no-change* — but each
has an `f3e702ed` **content** delta in `app-notes/<AN>/opus-master/` that no independent pass covered:
- **P2AN001** (5 hunks): I/O power groups **8-pin** (P0–7…P56–63) not 4-pin; SINC2 *filtering* period is
  adjustable (not power-of-two-locked); below-ground reading is unsigned-wrap in the muldiv64 builds,
  signed only in the CORDIC build. *(All look correct vs KB `reference_p2_adc_per_group_vio_gio` — but
  UNVERIFIED by a pass.)*
- **P2AN002** (4 hunks): 2^32 literal-overflow explanation refined; OBEX author names corrected
  (#2812 → ersmith, #5361 → James Smith). *(Author-name accuracy needs a check.)*
- **P2AN003** (1 hunk): PWM dither tone fixed at sysclock/256 regardless of period.
- **P2AN005** (1 hunk): cross-cog bus coordination wording.
→ **Action:** run the changeset-integrity pass on these 4 app-note content deltas (tiny) before they
release. P2AN004 already audited (clean). architect + getting-started were inline-cleared (OK).

> **✅ GAP A CLOSED 2026-07-11.** Independent adversarial pass run on all four content deltas —
> report `CHANGESET-AUDIT-app-notes-content-2026-07-11.md`. **CLEAN — 0 flags; all 10 hunks `faithful`,
> each corrects a real pre-existing defect.** Verified against primary sources: P2AN001 power-groups
> (8-groups-of-8: VERIFICATION-OPPORTUNITIES + edge-breakout 300mA/8-pin) + SINC2 filtering/11,585 (IOSP
> Ch16 L297/L311) + below-ground unsigned-wrap (note's own Recipe-3 code `abs…wc`/`if_c neg`); P2AN002
> OBEX authors (catalog: #2812=ersmith, #5361=James Smith) + 2³² dividend-overflow; P2AN003 PWM dither
> fixed at Fclock/256 (Silicon L7936); P2AN005 P2-has-16-locks. **Side-finding → F-211** (KB YAML still
> teaches 4-pin power groups; the app-note *manuals* are correct — `yaml`-head fix on the KB rail).

**B. CHANGELOG gap — these re-releasing docs still need entries + version bumps:**
architect (`v1.0.1`), getting-started (`v1.0.1`), P2AN001 (`v1.0.2`), P2AN002 (`v1.0.1`),
P2AN003 (`v1.0.1`), P2AN004 (`v1.0.1`), P2AN005 (`v1.0.1`). *(The 4 big manuals done; Debug deferred
on reconciliation.)* Author per `methodology/changelog-style-guide.md` AFTER their audit clears.

> **✅ GAP B CLOSED 2026-07-11.** All seven CHANGELOG entries authored (current-state voice, theme +
> bullets per the house accuracy-pass model; excluded non-user-discoverable housekeeping such as
> getting-started's "from Chapter 1" cross-ref dedup). Following the pre-staged big-manual pattern, only
> the `opus-master/CHANGELOG.md` entry is written now — the title-page version string in
> `front-matter.md` is promoted at release (§9, `release-manual`), not here. Debug's own changelog stays
> deferred on the REF↔v55 reconciliation.

## Flow
1. YAML template pass (running) → Stephen reviews report + approves the format.
2. Fan out the 7 manual passes + P2AN004 (+ pre-clear the 3 template-only app-notes).
3. Consolidate flags → Stephen adjudicates → rejects loop back to fix→re-commit→re-audit.
4. Clean fleet-wide → unblocks #180 render wave.
