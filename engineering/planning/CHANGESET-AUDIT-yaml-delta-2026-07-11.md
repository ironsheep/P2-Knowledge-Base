# Changeset-Integrity Audit — YAML delta since v1.14.2

**Baseline tag:** `v1.14.2` (`0386ce61`)
**HEAD:** `ad1de9e0` (`ad1de9e00ed3a5b0bf088cd1b89361eea3477395`)
**Scope diff:** `git diff v1.14.2..HEAD -- deliverables/ai/P2/`
**Files changed:** 76 (68 `pasm2/*.yaml` + 8 `spin2/debug-displays/*` & `spin2/statements/debug.yaml`)
**Hunks:** 79 (77 PASM2 z-flag predicate edits across 67 files + 1 rdpin timing snippet + 11 debug-display enrichment hunks)
**Introduced by 2 commits:** `ccfe1c5e` (Fleet-release §3b + F-204) and `ad1de9e0` (Debug YAML enrichment F-205b/206/207/208)

## Bottom line: **CLEAN — 0 flags.** Every hunk traces to a registered finding (F-204/205b/206/207/208) and, for every behavioral claim, to a hardware EF (EF-015/028/031/032) or a verbatim v55 line (L1139/L1143/L1290/L1406). Two sub-threshold watch items are noted but neither rises to a defect. Safe to publish as-is.

---

## Traceability table

| file(s) | hunk summary | traced source | verdict | note |
|---|---|---|---|---|
| `pasm2/` 67 files, 77 predicates (abs, add, adds, addsx, and, andn, cmp, cmpm, cmps, cmpsub, decmod, encod×2, fge, fges, fle, fles, getqx, getqy, incmod, mov, mul, muls, muxc, muxnc, muxnz, muxz, neg×2, negc×2, negnc×2, negnz×2, negz×2, not×2, ones×2, or, pop, popa, popb, rcl, rcr, rdbyte, rdlong, rdlut, rdword, rfbyte, rflong, rfvar, rfvars, rfword, rol, ror, sal, sar, sca, scas, shl, shr, signx, sub, subr, subs, subsx, sumc, sumnc, test×2, testn, xor, zerox) | `encoding[].z` compare predicate `=` → `==` (`Result = 0`→`== 0`; `D=S`→`D==S`; `(D=0)\|(S=0)`→`==`; `Z AND (Result=0)`→`==`; `Product=0`→`==`; `(D & S)=0`, `(D & !S)=0`, `D=0`→`==`) | commit `ccfe1c5e` §3b; rule `feedback_behavior_notation_vs_code_operators` (`==`=compare in behavior descriptions) | **faithful** | Verified mechanically: ALL 77 changed encoding lines are `z:` fields; **zero `c:` (receives) lines touched**. Old/new pairs match 1-for-1. `cmpsub c: Unsigned(D => S)`, `incmod`/`sumc` `c: … D = D + 1` (assignments) correctly left as `=`. |
| `pasm2/rdpin.yaml` | `in_flag_reset_latency` snippet: two NOPs → one NOP; per-NOP "Clock 1/2" labels → "2 clocks: covers the IN-flag reset delay"; prose "Insert NOP instructions" → "one NOP is 2 clocks … insert one NOP" | **F-204** (DONE) + IOSP §4.13 (L542, doc already correct) + v35 Instructions CSV (NOP=2 clk) + **EF-015** (RDPIN-ack mechanism HW-confirmed) | **faithful** | 2-clock IN-flag reset latency was already in the (unchanged) prose; NOP=2 clk is documentary. One NOP (2 clk) covers a 2-clk delay — arithmetically exact, matches IOSP's own wording. Not an over/under-wait. |
| `debug-displays/{term,fft,logic,midi,scope,scope_xy}.yaml` (6 files) | `SAVE` line standardized to `SAVE {WINDOW} 'filename' … filename is REQUIRED; WINDOW optional` | **F-206** (CONFIRMED) + v55 **L1139** (also 1169/1194/1222/1246/1294) verbatim | **faithful** | v55 L1139 reads verbatim `SAVE {WINDOW} 'filename' \| Save a bitmap file (.bmp) of either the entire window or just the display area.` filename un-braced = required; WINDOW braced = optional — matches exactly. `plot.yaml` already correct, untouched (correct scoping). |
| `debug-displays/plot.yaml` (TEXTSTYLE) | Adds per-axis align mapping (horiz %10=right/%11=left; vert %10=top/%11=bottom; %00/%01=center) + weight caveat (0=thin,1=normal,2=bold,3=heavy; `$00`==`$01`; `$02`/`$03` not visibly heavier) | **F-205b** + **EF-031** (justify per-axis hybrid) + **EF-028** (weight not rendered distinctly, `$00`==`$01`) | **faithful** | Per-axis mapping matches EF-031 word-for-word. Weight mapping matches EF-028's Pascal `weight[0..3]=(100,400,700,900)`=thin/normal/bold/heavy and the `$00`≈`$01` measurement (18.66% vs 18.71%). See Watch-item 1. |
| `debug-displays/plot.yaml` (POLAR) | Replaces murky "twopi -1/0 select clockwise/counter-clockwise" with "θ=0 points East (+x); positive (default) twopi → CCW; NEGATIVE twopi → clockwise" | **F-208** + **EF-032** (θ=0 East, default CCW, no flip) + v55 **L1290** (`POLAR -12 -3 would be like a clock face`) | **faithful** | East + CCW-default are EF-032 verbatim (hardware). The negative-twopi→CW half is grounded in v55 L1290's own "clock face" example (negative twopi -12 = clockwise) — documentary, not fabricated. See Watch-item 2. |
| `debug-displays/logic.yaml` (`packed:`) | Appends "sub-sample WIDTH sets the channel count … 1-bit→1 ch, 2-bit→2, 4-bit→4, 8-bit→8 … LONGS_1BIT lands both channels on the first channel only" | **F-207** Facet B (user-reported + HW-CONFIRMED 2026-07-11) + v55 L1143 example (`'TX' 'IN'` = 2 ch via LONGS_2BIT) | **faithful** | The 1-ch/2-ch cases and the "LONGS_1BIT → all on first channel" claim are Stephen's hardware observation. 4/8-bit generalization is a mild extrapolation — consistent with v55's documented unpack mechanism. See Watch-item 3. |
| `debug-displays/logic.yaml` (example + note) | New LONGS_2BIT full-window array-feed example (`VAR long buff[16]`, 2 ch D0/D1, `uhex_long_array_(@buff,16)`) + note "single packed long advances window one column; LONGS_2BIT unpacks 16 sets/long; LONGS_1BIT → 32 1-bit values from LSB" | **F-207** Facet A (HW renders 2026-07-11) + v55 **L1143** & **L1406** verbatim | **faithful** | Example mirrors v55's own canonical LONGS_2BIT array-feed (2 channels, `uhex_long_array_`). Unpack sentences are near-verbatim v55 L1143 ("16 sets per long") and L1406 ("32 separate 1-bit values, starting from the LSB"). Buffer sizing (16 longs × 16 = 256) is arithmetically correct. |
| `debug-displays/scope.yaml` (`packed:` + example + note) | Appends per-channel-VALUE interleave ("two channels A/B via LONGS_8BIT pack four 8-bit values per long, low byte first, applied A,B,A,B") + LONGS_8BIT array-feed example (`VAR long buff[128]`, `'A' 0 255 'B' 0 255`) + left-edge-fragment caveat | **F-207** Facet B + HW renders ("two 0–255 sawtooths A+B", 2026-07-11) + v55 **L1409** ("4 separate 8-bit values … from the LSBs") | **faithful** | "low byte first" = v55 "starting from the LSBs". A,B,A,B interleave + required `'A' 0 255 'B' 0 255` ranges + `buff[128]` all match the HW-confirmed ch13 example. Buffer sizing (128 longs × 4 = 512 values = 256 A,B sets) correct. |
| `spin2/statements/debug.yaml` (example) | New packed scrolling-window array-feed cross-ref example (LONGS_2BIT, `uhex_long_array_(@buff,16)`) pointing to logic/scope yaml | **F-207** Facet A (cross-reference) | **faithful** | Consistent with the logic.yaml example; a pointer, asserts no new fact. |

---

## FLAGS

**Zero non-`faithful` verdicts.** Every hunk in the delta traces to a registered finding and every behavioral/semantic claim is anchored to a hardware EF or a verbatim v55 line (spot-checked against `spin2-v55-text.txt`). No `traces-to-nothing`, no `overstates-source`, no `introduces-new-claim`.

Evidence highlights that would have caught a problem if one existed:
- **No scope creep.** Both commits touch only files named in F-204/205b/206/207/208. The PASM2 sweep changed **only** `z:` fields (77/77) and **left every `c:` receives-line untouched** — verified by extracting all `-`/`+` encoding lines.
- **Every quoted source line is real and un-paraphrased-in-meaning.** `SAVE {WINDOW} 'filename'` is v55 L1139 verbatim; the LOGIC unpack sentences reproduce v55 L1143/L1406 almost word-for-word; the POLAR East/CCW facts are EF-032 verbatim.
- **Example code is safe to generate from.** The logic LONGS_2BIT (2 ch) and scope LONGS_8BIT (2 ch, ranges present) snippets each match both v55's canonical example and the 2026-07-11 hardware renders; buffer-length arithmetic checks out; the SCOPE channel-defs carry the required `lo hi` ranges (the F-207 second defect). An agent copying these would produce a window that fills correctly.

### Watch items (sub-threshold — noted for rigor, not defects, no rework required)

1. **plot.yaml TEXTSTYLE weight — "`$02`/`$03` are not visibly heavier."** EF-028 measured `$02`=11.6%, `$03`=12.3% ink vs `$00`/`$01`=~18.7% — i.e. `$02`/`$03` render *lighter*, not merely "not heavier." The YAML's phrasing is strictly true (they are not heavier) and faithful to the finding's conclusion (weights don't render as weights), so it is not an overstatement; but a maximally precise version would say "render differently but not as heavier weights." No reader/agent would be misled toward wrong code.

2. **plot.yaml POLAR — the `0`/`-1` shorthand dropped.** v55 L1290 documents `twopi` shorthands "use `0` or `-1`" for `+$100000000`/`-$100000000`. The rewrite replaces the (murky, partly-wrong) old "twopi -1/0" wording with the clearer sign-based rule and drops the literal `0`/`-1` encodings. This is a net improvement (the sign rule is correct and more general); the only cost is the two shorthand literals are no longer shown. Not a fact loss of any behavioral claim — purely a convenience-encoding omission.

3. **logic.yaml channel-count rule — 4-bit/8-bit generalization.** The hardware-observed cases are 1-bit (1 ch) and 2-bit (2 ch, LONGS_1BIT-lands-on-ch0). The extension to "4-bit→4 channels, 8-bit→8 channels" is an extrapolation, not directly in an EF or a verbatim v55 line — but it is a direct consequence of the v55-documented unpack mechanism (N-bit sub-sample = one bit per channel per time-step) and is internally consistent with the LONGS_NBIT table. Low risk; an agent declaring 4 channels would correctly reach for LONGS_4BIT. If a future audit wants zero-extrapolation purity, a hardware run of the 4-/8-channel case would close it, but it is not blocking.

---

## Recommendation

**Publish as-is.** This YAML delta is a disciplined, finding-anchored changeset: a mechanical operator-notation sweep (77 compare predicates, `c:` lines correctly untouched), one arithmetic timing correction (rdpin, doc-grounded), and eight debug-display enrichments each carrying a live finding ID plus a hardware-EF or verbatim-v55 anchor. Spot-checks of the v55 source text and the empirical ledger confirm the quotes and the magnitudes. No hunk must be reworked before the KB publish. The three watch items are optional precision refinements for a later pass, not release blockers.
