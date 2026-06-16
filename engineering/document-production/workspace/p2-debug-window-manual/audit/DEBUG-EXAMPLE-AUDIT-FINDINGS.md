# Debug Window Manual — Consolidated Audit Findings (2026-06-13)

Ground truth: **v55 Spin2 primary source** (`engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt`,
per-window directive tables ~L1118–1417) — used to RE-GROUND the YAML-based agent
audit after the YAML was found to contain errors. Rubric: `DEBUG-EXAMPLE-AUDIT-RUBRIC.md`.

**Headline:** the manual is in good shape; most chapters audited clean. The biggest
discovery is that the v1.8.0/v1.9.0 **reconciled YAMLs contain errors**, so several
agent findings were INVERTED (manual right / YAML wrong). YAML errors are logged to
the corrections register (**F-125…F-130**).

---

## A. CONFIRMED manual fixes (apply)

| # | Loc | Class | Fix | Evidence |
|---|-----|-------|-----|----------|
| M1 | Ch1 ~L260 "Strings" bullet | QUOTING/pedagogy | Rewrite to the **three-context** quoting model (plain-double / streamed-double / command-arg-single) + silent-failure emphasis. **Headline.** | debug.yaml `string_quoting`; rubric §A |
| M2 | Ch1 L310 "There is no close command" | WRONG | False. Document all close mechanisms: (a) per-window **`` `CLOSE ``**; (b) session on-chip `DEBUG(DEBUG_END_SESSION)` (const 27, {Spin2_v52}); (c) host end-marker — `debug("DEBUG_END_SESSION")` string OR any `debug("marker")` with `pnut-term-ts --end-marker "marker"` (the figure-capture workflow's `### CAPTURE DONE … ###`). Add CLOSE to "Commands common across windows". | v55 src L1140…1393 (CLOSE ×9), L101–110; DebugEndSession KB; (c) host-tool, KB-gap F-099 |
| M3 | Ch3 ~L698–702 default pairs "Lime" | WRONG | Default text pairs are GREEN-based, not LIME (not a P2 named color): 2=GREEN/BLACK, 3=BLACK/GREEN. | v55 src L1306 |
| M4 | Ch3 L812 "pair 3 (red)" / L814 "pair 2 (lime)" | WRONG-SEMANTICS | Dashboard (L793) sets NO COLOR → defaults. Either correct comments to default colors (pair3=black/green, pair2=green/black) OR add a COLOR directive so the red/green intent is real. | L793 (no COLOR); v55 src L1306 |
| M5 | Ch4 L902 BITMAP `RATE` default "full canvas" | WRONG-PARAM | Default is **line size** (per scan-line); `RATE -1` = whole bitmap. Fix table + add the -1 note. | v55 src L1333 |
| M6 | Ch5 ~L1259 PLOT config table | OMISSION | Add `color_mode` (LUT1..RGB24, default RGB24) and `LUTCOLORS` rows. | v55 src L1259–1260 |
| M7 | Ch7 ~L2269–2271, L2310 SCOPE "2048 buffer, draw 4–2047" | WRONG | "4–2047" is a LOGIC range; SCOPE `SAMPLES` = **16..2048** (default 256). Remove/soften the unsourced "2048 internal buffer" claim or scope it correctly. | v55 src L1153 (SCOPE), L1124 (LOGIC) |

## B. DISCARDED — inverted / false-positive agent findings (manual is RIGHT; do NOT change)

| Was flagged | Verdict | Why |
|---|---|---|
| Ch8 SCOPE_XY SIZE default → 256 (agent F-L) | manual RIGHT (128) | v55 src L1179 "SIZE radius … 128" |
| Ch7 SCOPE AUTO-trigger formula "unverifiable" (F-K) | manual RIGHT | v55 src L1165 = 33% arm / 50% trigger |
| Ch6 LOGIC `SAVE` w/o filename (F-H) | manual RIGHT | filename is optional `{}` (v55 src L1139) |
| `CLOSE` "fabricated" (all figure gens + Ch8 L2794) | manual RIGHT | CLOSE is real (drove F-125 + M2) — KEEP everywhere |

## C. VERIFY-with-Stephen / needs a runtime check before editing

| # | Loc | Question |
|---|-----|----------|
| V1 | Ch5 L1367 `debug(\`PLOT Rose … POLAR …)` on the creation line | Manual's own text (L1278) says PLOT POLAR is runtime-only, and v55 lists PLOT POLAR under *Feeding*. Does PLOT accept POLAR on the creation line? If not → move POLAR to a runtime line (make consistent). (Note: SCOPE_XY POLAR *is* a creation directive — window-dependent.) |
| V2 | Ch8 L2850 "samples buffered between repaints" | v55 SCOPE_XY has RATE (display-update divisor) and NO UPDATE/buffered mode — confirm the "buffered" wording isn't implying a buffered mode. |
| V3 | Ch5 SPRITEDEF illustrative snippets (L1676/1708) show 2 colors not 256 | Compile-illustrative only? The real figure generator `fig-05-plot-sprite.spin2` carries full data (audited OK). Add a "(abbreviated)" note vs. leaving as-is. |
| V4 | Ch2 L460 formatter callout (with-name `UDEC` vs value-only `udec_`) | Confirm whether with-name forms are valid in a backtick stream or strictly the `_` value forms; phrase precisely. |

## D. YAML corrections (logged to the register — YAML head)
`engineering/operations/P2KB-CORRECTION-FINDINGS.md` → **F-125** (CLOSE ×9 + statements),
**F-126** (logic LINESIZE 1..7 / SPACING 2..32 / SAMPLES 4..2048 / DOTSIZE), **F-127**
(scope_xy SIZE-default-128 / SAMPLES 0..512 / RATE 1..512), **F-128** (term default GREEN
not LIME), **F-129** (scope AUTO 33/50 + defaults), **F-130** (statements/debug.yaml legacy:
code-12-clear, trailing-backtick examples, misleading usage note).

## E. Figure generators
All 11 audited clean EXCEPT the `CLOSE` flag — which was an inversion: **CLOSE is correct,
keep it.** No figure-generator edits required. (Re-generation still pending per roster:
5/10 hero figures + TERM captures are placeholders.)

## F. Pedagogy plan (quoting + CLOSE — the no-error failure modes)
- **Home:** Ch1 — rewrite the "Strings" bullet (M1) + add a short "Strings: two quote rules"
  subsection with a contrast table and a `::: caution` **silent-failure** callout (✅ right /
  ❌ silent-loss pairs naming the outcome). Add CLOSE to shared commands (M2).
- **Point-of-use:** `::: caution` at each command-argument site (TITLE, SAVE, LAYER filename)
  in TERM/PLOT/etc.; reinforce SAVE auto-`.bmp` + single-quote rule.
- **Appendix A:** annotate every string-argument command "single-quoted; double quotes
  silently ignored (no error)."
- Reusable "Silent Failure" caution style, used consistently.

---

## STATUS — applied 2026-06-13
- **Manual fixes M1–M7 + Rose(V1): APPLIED** to `P2-Debug-Window-Manual.md`. Structurally-
  changed examples (Ch3 dashboard multi-line COLOR, Ch5 Rose, 2-color SPRITEDEF) compile
  clean under `pnut-ts -d`.
- **Pedagogy:** Ch1 "Strings: two quote rules" subsection + silent-failure callout added;
  CLOSE + the three session-end forms documented (Ch1 + shared commands); Appendix A gained
  a string-argument quoting note + a CLOSE shared-command row.
- **M3 extended:** Lime→Green fixed in BOTH the Ch3 table and Appendix C, plus the custom-
  scheme prose; LOGIC fabricated default-color list ("lime/olive", unsourced) reworded.
- **V2: DISCARDED** — no "buffered between repaints" text exists in Ch8 (agent mis-cite).
- **V3: manual was RIGHT** — 2-color SPRITEDEF is valid (compile-confirmed); the YAML was
  wrong → logged F-131.
- **YAML corrections logged:** F-125…F-131 in the register.
- **Figure generators:** unchanged (correct as-is).
- **Remaining:** prepare-manual → Forge render (once) + verify; hero-figure placeholders
  (5/10) are a pre-existing asset task, separate from this content pass.
