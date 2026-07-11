# Changeset-Integrity Audit — p2-debug-window-manual

**Adversarial, fresh-eyes audit of the diff since the last public release.**

| | |
|---|---|
| Manual | `p2-debug-window-manual` |
| Baseline tag | `p2-debug-window-manual-v1.0.2` (`cbdea2f3`) |
| HEAD | `60d0a18a` |
| Diff scope | `git diff p2-debug-window-manual-v1.0.2..HEAD -- engineering/document-production/manuals/p2-debug-window-manual/` |
| Files changed | 58 (17 opus-master chapters/appendices · examples-library README + 15 `.spin2` + 2 `.bmp` · assets-needed spec · figure-generators workspace) |
| Commits | 13 (`f3e702ed` … `60d0a18a`) |
| Examples re-verified | 15/15 compile clean `pnut-ts -d`; 11/11 spot-checked twins **byte-identical** to opus-master code blocks |
| **Bottom line** | **3 FLAGS** — 1 HIGH (PRECISE default inverted), 1 MEDIUM (Lime→Green vs EF-025), 1 LOW-MED (LOGIC DOTSIZE row dropped). All three trace to the **oldest** commit (`f3e702ed`, pre-empirical sweep) and share one root cause: they followed **v55 text over the higher-authority Pascal/REF** (or over a later EF). Everything else in the changeset is well-grounded and faithful. |

The dominant story of this changeset is **good**: ~30 distinct correction-groups, the large majority anchored to hardware-empirical findings (EF-025…032), the corrections register (F-206/F-207/F-208/F-205/F-130), or verbatim Spin2 v55 text and the Pascal-derived REF. The three flags are regressions that the later empirical/reconciliation work fixed *around* but never caught.

---

## 1. Traceability table

Verdicts: `faithful` · `overstates` · `understates` · `new-claim` · `traces-to-nothing`. Repeated hunks are grouped (identity confirmed).

| File(s) | Hunk summary | Traced source | Verdict | Note |
|---|---|---|---|---|
| ch05-plot.md | **PRECISE default: "sub-pixel by default" → "whole-pixel by default; PRECISE toggles ON to sub-pixel"** | fanout S20/A31 → **v55 L1271 "disabled"**; but Pascal `PLOT_Configure` `vPrecise:=8` / REF PLOT-theory L383 "Starts at 8 (on)" | **FLAG — understates/inverts** | Contradicts Pascal ground truth. See FLAG 1. |
| appendix-c, ch03 (table + prose + 2 example comments) | **TERM default pair color "Lime" → "Green"** | **EF-025** (`clLime $00FF00`, NOT GREEN kw) + C-R6 disposition "keep Lime; add reader-note" + `term.yaml` "LIME" | **FLAG — overstates/contradicts-EF** | Reverts the confirmed label the wrong way; reader-note absent. See FLAG 2. |
| ch06-logic.md | **LOGIC `DOTSIZE` config row removed** | v55 LOGIC table omits it; but REF matrix L82/L90/L260 lists **DOTSIZE ✅ 0–32/0 for LOGIC** | **FLAG — understates** | Drops a keyword the higher-authority Pascal/REF documents. See FLAG 3. |
| ch05-plot.md | POLAR: θ=0 points East (+x), CCW; twopi 0/−1 shorthand restored | **EF-032** (θ=0 East, CCW, no flip) + v55 L1290 + F-208 | faithful | Empirically confirmed; commit `60d0a18a` watch-item #2. |
| ch05-plot.md, examples-library/ch05-plot-gauge | gauge comment "theta 0 points up" → "right (+x), +90 up"; POLAR moved to feed line | EF-032; POLAR is a feeding command | faithful | Twin byte-identical; compiles. |
| ch05-plot.md | TEXTSTYLE weight `0=light`→`0=thin`; default `$00`→`$01`; **weight-not-a-progression caveat ($02/$03 slightly less ink)** | **EF-028** (ink% $00≈$01; $02=11.6/$03=12.3) | faithful | Commit `60d0a18a` watch-item #1; matches ink measurements. |
| ch05-plot.md | TEXTSTYLE vertical align `2=bottom,3=top` → `2=top,3=bottom` | **EF-031** ("manual's 2=bottom,3=top is inverted → fix to 2=top,3=bottom") | faithful | Horiz 2=right/3=left left unchanged (also EF-031). |
| ch05, ch06, ch10, ch11 (SAVE, 4 chapters) | `SAVE` → **filename required**; `{WINDOW}` optional | **F-206** (CONFIRMED, YAML applied) + v55 L1139/1169/1194/1222/1246/1294 | faithful | Identical remediation across chapters. |
| ch13-packed-data.md + examples (stream/scope) | Packed feed: one-long-per-call → **`uhex_long_array_(@buff,N)` full-window array feed**; SCOPE ranges as separate feed | **F-207 Facet A** (CONFIRMED, HW-verified; v55 L1144 shows only the array form) | faithful | Twins byte-identical; compile clean. |
| ch13-packed-data.md + new ch13-packed-logic-multi | **New dual-channel demo** `LONGS_2BIT` + mode↔channel-count rule (LONGS_NBIT ⇒ N 1-bit channels) | **F-207 Facet B** (HW-confirmed 2026-07-11; run-list A15) | faithful | New file compiles; twin byte-identical; README indexed. |
| ch13-packed-bitmap-frame (+ example) | `LUT2`→`LUT1` for 1-bit source + `LUTCOLORS`; `bit … &1` | v55 L1260 (LUT default colors 0..7); LUT1 = 2-color | faithful | Twin byte-identical; compiles. |
| appendix-b, ch13 (ALT, 3 hunks) | ALT "swap adjacent fields / butterfly" → **"per-byte end-to-end reversal of sub-units"** | **v55 L1403** verbatim ("within each byte sent … reordered end-to-end … within each byte") | faithful | Old wording was wrong; new is verbatim-accurate. |
| ch07, ch08, ch09 (LINESIZE/DOTSIZE units) | "pixels" → **"half-pixels"** (SCOPE LINESIZE, SCOPE_XY DOTSIZE, FFT LINESIZE) | **v55 L1156/L1183/L1212** + reconciliation C-R8 (APPLY; REF non-contradicting) | faithful | Correctly **NOT** applied to LOGIC (C-R8 caveat). "3 = 1.5px" arithmetic correct. |
| ch09-fft.md, appendix-a | FFT neg LINESIZE = **filled bars, wider with \|n\|** | **EF-026** (filled bars, width∝\|n\|; v55 "isolated lines" inverts) | faithful | v55's wrong "isolated lines" correctly rejected. |
| ch09-fft.md (3 hunks) | "grid flags bit0/1" → **"legend flags %abcd: bit0 min line, bit1 max line, bit2 min legend, bit3 max legend"** | **v55 L1162** verbatim (%abcd = max legend/min legend/max line/min line) | faithful | Bit mapping matches v55. |
| ch09-fft.md, appendix-a | LOGSCALE "log2-based" + "power-of-2 markers (1,2,4,8)" **removed** → "logarithmic, arbitrary power units" | No source supports log2/markers (v55 LOG2 is an unrelated FP operator) | faithful | Safe retraction of an unsourced claim. |
| ch09-fft.md | "Cooley-Tukey FFT" → "an FFT" | unverifiable algorithm name removed | faithful | Retraction; no fact lost. |
| ch07-scope.md | `` `() `` clarified as **shorthand for `SDEC_` (signed)**; warns `udec_` sends 4294967291 for −5 | **v55 L1090** ("`(value)` … Short for SDEC_") + F-130 resolution | faithful | Arithmetic (−5 unsigned = 4294967291) correct. |
| ch06-logic.md + example | LOGIC channel `'CS' $color` → `'CS' 1 $color` (bit-count added) | **v55 L1130** `'name' {1_to_32 {color}}` | faithful | Real fix: old form ate the color as a bit-count. Compiles. |
| ch06-logic.md | sample `%1011` bit-mapping corrected (DATA low→high, CS high→low) | arithmetic (%1011: bit1=1, bit2=0) | faithful | Old text was arithmetically wrong. |
| ch04-bitmap.md (+ example) | SPARSE "square block + grid border" → **"large round dot on background color; needs DOTSIZE≥4"** | **v55 v35s changelog** ("large round pixels against a background color") + Pascal sparse-center `vDotSize shr 2` inset / SmoothShape rounded-rect (REF L2222/2261) | faithful | "≥4" is a sound derivation (inset = DOTSIZE/4 → 0 below 4); REF has a `dotsize 4` example. Note: derived, not verbatim. |
| ch04-bitmap.md | LUMA/HSV `X` "expand range" → **"ramp black→color→white, peaking in white"** | Pascal BITMAP-theory L636–648 (LUMA8X inverts to white when p≥$80) | faithful | More precise than REF matrix's terse "expanded range"; grounded in Pascal. |
| ch04-bitmap.md | LUT-without-palette "renders as garbage" → **"entries 0–7 hold default colors; LUT1/LUT2 all-default, LUT4/LUT8 upper undefined"** | **v55 L1260** ("default colors 0..7") | faithful | Old overstatement corrected. |
| ch03, ch04, ch05, ch06, ch08, ch11 (TITLE/POS defaults) | TITLE default `TERM`/`Plot`/`MIDI`→`none`; POS `auto`/`cascaded`→`0,0` | **v55 L1122/L1123** (`TITLE <none>`, `POS 0,0`) + REF matrix | faithful | Consistent across chapters. |
| ch11-midi.md (+ example) | MIDI COLOR "each `$RRGGBB`" → **"named color (opt brightness) or `$RRGGBB`"**; example `$00FF00`→`GREEN` | **EF-029** (MIDI accepts rgb24 AND GREEN kw; both render green) | faithful | Named or rgb24 both valid; twin byte-identical. |
| ch02-getting-started.md | `QROTATE`→`ROTXY`; `?`→`??` (RNG operator) | **v55 L561** (ROTXY is the Spin2 method) + **v55 L412** (`??` = XORO32 iterate) | faithful | QROTATE is PASM-only; `?` is not the Spin2 RNG op. |
| ch02-getting-started.md | formatters: "the value-only formatters are …" → "such as … every DEBUG output command has a trailing-underscore value-only form" | debug-formatters-overview (value-only `_` is general) | faithful | Generalization is correct. |
| ch01-foundation.md | bandwidth "you can count on ~100–150 KB/s" → "as a rough working estimate, on the order of" | hedge of an un-guaranteeable figure | faithful | Removes overstatement. |
| ch13-packed-data.md | "`pnut_term_ts` is **certified** at 2 Mbaud" → "**runs** at 2 Mbaud" | removes unsupported "certified" claim | faithful | Softening; no fact lost. |
| ch14-multiwindow-pasm.md + 3 examples | SCOPE channel-def split off creation line into a separate feed | F-207 create-vs-feed pattern; consistent with SCOPE grammar | faithful | Twins byte-identical; compile clean. |
| Many chapters | Multi-line `DEBUG(… …)` continuations collapsed to single lines (de-`...`) | cosmetic (code-line formatting); twins updated in lockstep | faithful | No semantic change; all compile; byte-identity preserved. |
| examples-library/README.md | index adds `ch13-packed-logic-multi` (2-ch `LONGS_2BIT`); stream re-labelled single-channel | matches new/changed examples | faithful | Consistent with corpus. |
| examples-library/digits.bmp, panel_bg.bmp | new binary assets for ch15 LAYER/sprite examples | ch15 assets-needed spec | n/a | New assets; not reader-prose. |
| assets-needed/ch15-panel-plot-bmp-spec.md; figure-generators/* (new) | new internal workspace (BMP spec, figure generators, HARDWARE-RUN-LIST) | supporting tooling, not published reader content | n/a | Out of reader-facing claim scope; no claims injected into the manual. |

---

## 2. FLAGS

### FLAG 1 — HIGH — PRECISE default inverted (ch05-plot.md, "PRECISE — sub-pixel positioning")

**What the changeset now claims:** "By default `PRECISE` mode is **off** and coordinates are taken in whole pixels; issuing `PRECISE` turns it **on** … Each `PRECISE` flips between **whole-pixel mode (the default)** and sub-pixel mode … a single `PRECISE` enters [sub-pixel mode]."

**What the source supports:** The Pascal-derived REF (`PLOT_Theory_of_Operations.md`) is unambiguous — `PLOT_Configure` initializes `vPrecise := 8` (`// Sub-pixel precision enabled`), and the update-directive table states `PRECISE … Starts at 8 (on) … XOR vPrecise 8↔0`. Sub-pixel is the **creation default**. The only source for "off by default" is **v55 text L1271** ("Default: disabled") — the lowest tier of the DEBUG-window authority chain (Pascal → REF → v55), the same tier that EF-025/026/027/030/031/032 have repeatedly shown to carry errors. The manual's **original** wording ("the window keeps sub-pixel precision by default") was correct. The change was applied in `f3e702ed` from fanout finding S20/A31 ("precise-default-inverted"), which cited v55 + a shallow "toggle" reading and **missed the Pascal `vPrecise:=8` init**.

**Concrete failure scenario:** A reader wants smooth, anti-aliased curves. The manual tells them sub-pixel "is the right choice … a single `PRECISE` enters it." They issue one `PRECISE`. Because sub-pixel is already ON at creation (`vPrecise=8`), that single `PRECISE` **XORs it to 0 — turning sub-pixel OFF** — and their curves render aliased/whole-pixel, the exact opposite of the intent. The manual's instruction produces the wrong visual result.

**Fix:** Revert to the sub-pixel-is-default description (matching Pascal/REF); or, if there is genuine doubt, hardware-verify (an EF-style POLAR/TEXTSTYLE-grade test) before shipping — but do not ship the v55-text reading, which the project's own methodology treats as unreliable against Pascal.

### FLAG 2 — MEDIUM — TERM default color "Lime" relabelled "Green" (appendix-c; ch03 table + prose + example comments)

**What the changeset now claims:** TERM default pairs 2/3 foreground = **"Green"** (color table, running prose "green-on-black", and two example comments changed lime→green).

**What the source supports:** **EF-025 (CONFIRMED, real silicon 2026-07-10):** the default renders `clLime = $00FF00`, measurably **distinct** from the `GREEN` keyword (which renders `$09FF09`). The reconciliation doc C-R6 disposition is explicit: *"keep 'Lime' (matches source constant + YAML); do **not** apply the green finding … add a one-line note that there is no `LIME` keyword and a reader reproduces it with `GREEN`"* (catalog #250). `term.yaml` still says "LIME/BLACK, BLACK/LIME". So the manual now (a) contradicts the confirmed empirical label, (b) disagrees with the shipped KB YAML, and (c) omits the EF-025-mandated reader-note. The relabel was made in the oldest commit `f3e702ed`, following v55 text's "Green" — the reading EF-025 later proved **inverted**.

**Concrete failure scenario:** This changeset *also* converts examples to the `GREEN` keyword (MIDI, ch03 dashboard). A reader sees the color table call the default "Green," then types `COLOR … GREEN …` expecting the table's default — and gets `$09FF09`, not the `$00FF00` the table depicts. That is exactly the default-vs-keyword conflation EF-025 was written to prevent. (Visual harm is small — both look green — which is why this is MEDIUM, not HIGH; correctness/consistency harm is real.)

**Fix:** Restore "Lime" in the color table (appendix-c + ch03) and the "green-on-black" prose, and add the one-line reader-note (no `LIME` keyword; reproduce with `GREEN`, which renders a near-identical `$09FF09`). This is tracked as catalog #250 but remains unapplied at HEAD.

### FLAG 3 — LOW-MEDIUM — LOGIC `DOTSIZE` config row removed (ch06-logic.md)

**What the changeset now claims:** LOGIC has no `DOTSIZE` keyword (the `DOTSIZE | pixels | 0 | 0–32 | Dot diameter at each sample` row was deleted from the config table; no residual mention remains).

**What the source supports:** The **Pascal-derived REF matrix** lists `DOTSIZE x {y}` as **✅ for LOGIC** (header L82 order = LOGIC first; DOTSIZE row L90), range 0–32/default 0, and the per-window card §5.1 LOGIC config explicitly enumerates "…RATE, **DOTSIZE**, LINESIZE…". Only the v55 text LOGIC instantiation table omits it. Per the authority chain (Pascal/REF > v55 text), LOGIC does support `DOTSIZE`, and the deleted row was accurate. Removed in `f3e702ed` on the strength of the v55 omission. (No EF exists either way — EF-027 tested LOGIC LINESIZE/SAMPLES/SPACING, not DOTSIZE.)

**Concrete failure scenario:** A reader wanting a dot marker at each LOGIC sample finds no `DOTSIZE` documented and assumes it is unavailable, though the window accepts it. A lost capability, not a wrong result — hence LOW-MEDIUM.

**Fix:** Restore the LOGIC `DOTSIZE` row (0–32, default 0), or, if a hardware check shows LOGIC `DOTSIZE` is a genuine no-op, document *that* explicitly rather than silently deleting a keyword the Pascal source recognizes.

---

## 3. Bottom-line recommendation

**Not safe to render as-is — resolve the three flags first (they are small, surgical edits).**

- **FLAG 1 (PRECISE)** must be fixed before release: as written it actively misdirects the reader into turning sub-pixel mode OFF while believing they turned it on. Revert to the (correct) sub-pixel-default wording.
- **FLAG 2 (Lime→Green)** should be fixed in the same pass: restore "Lime" + add the EF-025 reader-note. It is already tracked (#250) and contradicts both an EF and the shipped `term.yaml`.
- **FLAG 3 (LOGIC DOTSIZE)** should be restored or its removal justified against the REF matrix.

All three are the *same class of error* — trusting v55 text over the Pascal/REF ground truth — introduced in the pre-empirical sweep `f3e702ed` and never re-caught. Recommend one grep-level pass over `f3e702ed`'s remaining ch-level edits for any other "v55-text-over-Pascal" reversals not surfaced here.

**Everything else is clean and shippable.** The empirical and reconciliation-driven corrections (POLAR, TEXTSTYLE weight + vertical-justify, SAVE-filename, packed array-feed + mode↔channel rule, ALT per-byte reversal, half-pixel units, FFT filled-bars/legend-flags, LOGSCALE de-fabrication, SDEC_ shorthand, LOGIC channel bit-width, SPARSE round-dots, LUMA/HSV X-ramp, TITLE/POS defaults, MIDI named colors, ROTXY/`??`) are each anchored to an EF, an F-finding, or verbatim v55/REF at the right magnitude. All 15 changed examples compile clean under `pnut-ts -d`, and every spot-checked examples-library twin is byte-identical to its opus-master code block — the identity model holds.

**Process note (not a content flag):** `CHANGELOG.md` was **not** touched in this diff — there is no `v1.0.3` entry describing this substantial changeset. That is expected if the CHANGELOG is promoted at release time, but it must be written (and should itself omit KB-plumbing) before publish.
