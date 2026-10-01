# P2 Empirical Findings — Running Ledger

**Golden source.** Each entry is a P2 behavior we **proved by test**, not by reading a
document. Cite these when grounding a YAML or manual change. Format per entry: the
**fact**, **how proven** (test + rig), the **result** (verbatim excerpt), the
**verdict + date**, and **what it grounds**.

> **Authority note.** For what was *observed*, these entries are ground truth — the
> silicon answered. Documentary sources (Silicon Doc, Titus) and our YAML are
> *downstream* of this. Where a host tool (PNut-Term-TS) behavior is recorded, note
> it may since have been fixed; silicon behavior is stable.

**Status legend:** `CONFIRMED` (test proved the claim) · `CONFIRMED-FALSE` (test
disproved the claim) · `NOT-OBSERVED` (could not reproduce; not asserted) ·
`HOST` (a toolchain/host behavior, not silicon).

> **Sibling ledger.** Hardware results from a PARTNER PROJECT's bench live in
> [`EXTERNAL-HARDWARE-FINDINGS.md`](EXTERNAL-HARDWARE-FINDINGS.md) as `XF-NNN`. They are
> **equal in kind** to these entries — silicon answered there too. They are kept separate
> because `EF-NNN` carries a promise this ledger can keep and that one cannot: *we* built the
> test, *we* ran it, so its rig, its scope and its failure modes are ours to answer for. An
> `XF` entry names whose bench it was and carries that project's own scope statement verbatim.

**Campaigns:** [2026-06 — DEBUG windows & smart pins](campaigns/2026-06-debug-windows-and-smart-pins/README.md) · [2026-08 — manual corrections](campaigns/2026-08-manual-corrections/README.md)

---

## DEBUG display windows (Spin2 backtick protocol)

### EF-001 · Backtick display TEXT must be single-quoted — `CONFIRMED`
Double-quoted text in a backtick named-window feed is **silently dropped** (no compile
error); single-quoted text renders. *Proof:* `test1-term-string-quoting` — single-quoted
body displayed in full; both double-quoted bodies were blank. *Date:* 2026-06-17 (real P2,
Stephen). *Grounds:* F-136; `term.yaml`, `statements/debug.yaml`, `ch03-term.md`.

### EF-002 · A value-only FORMATTER fed to a named TERM renders as a glyph; use `` `(value) `` for text — `CONFIRMED`
`` `udec_(value) `` into a NAMED TERM renders a single raw-byte glyph (char = the value),
not decimal text — and a bare formatter between text (`SDEC(x)`) showed nothing. The
trailing-underscore value-only formatters (`udec_`/`sdec_`/`uhex_`) emit a *numeric data
element* — the form the graphical windows (SCOPE/LOGIC/FFT) consume as a data point — so a
TERM renders that number as a character glyph (value 42 → `*`). The value-to-TEXT path in a
named feed is **`` `(expr) `` substitution** (short for SDEC_): `` debug(`MyTerm 'count =
`(n)') ``. *Proof:* `test1` W3 (nothing) + W4 (glyph char 42). *Corroborated by docs:* Spin2
v55 `spin2-v55-text.txt` L1090 + the canonical named-TERM example L1299 `` debug(`MyTerm 1
'Temp = `(i)') ``. *Date:* 2026-06-17 (test); resolved 2026-06-18. *Grounds:* F-136 — DONE
(`term.yaml`, `ch03-term.md`).

### EF-003 · A SCOPE channel-def on the CREATE line prevents window creation — `CONFIRMED`
SCOPE channel/trigger config MUST be a separate message AFTER create. With six windows
created, only the one whose channel-def (`'SC inline' -1000 1000`) sat on the create line
failed to appear. LOGIC + SCOPE_XY create-line labels DO work (those are config-phase).
*Proof:* `test2-createline-vs-config` (clean run). *Date:* 2026-06-17. *Grounds:* F-137;
`scope.yaml`, `statements/debug.yaml`, `ch07-scope.md`. (Confirms the **3-phase window
lifecycle**: create → one-time config → looping updates.)

### EF-004 · An FFT window with NO channel declared renders nothing — `CONFIRMED`
The FFT window needs at least one channel declared (as a separate post-create message)
before fed samples render. *Proof:* `test2c-fft-baseline` (the manual's verbatim minimal
snippet, no channel) = **blank on BOTH PNut-Term-TS and real PNut**; `test2d-fft-with-channel`
(same + one channel-decl line + a phase accumulator) = **single clean peak**. *Date:*
2026-06-17/18. *Grounds:* F-138; `ch09-fft.md` (released-manual snippet fixed), `fft.yaml`.
*Note:* the published figure recipe also warns full-scale `$7FFF_FFFF` can make peaks
vanish — use ~1000 with matching amplitude.

### EF-H01 · PNut-Term-TS window-registration same-ms collision — `HOST` (fixed)
Two windows created in the same millisecond could collide on a `<type>-<ms>` id. Observed
earlier; a clean `test2` run confirms it is fixed in PNut-Term-TS. *Note:* the FFT
"render gap" was NOT a host bug — it was the missing channel decl (EF-004).

<!-- 2026-07 conflict-test suite (A–J): v55-text-vs-REF-Pascal conflicts + undocumented
     behaviors, settled on real P2. Sources versioned under
     campaigns/2026-07-debug-conflict-tests/. Read-back via image-tools-mcp + PIL
     (centroid / color / geometry) by Claire; run on real P2 by Stephen (I/J on both
     macOS + Windows). Full analysis: the manual's audit/v55-vs-REF-reconciliation-2026-07-10.md. -->

### EF-025 · TERM default color pair is `clLime` ($00FF00), NOT the `GREEN` keyword — `CONFIRMED`
The TERM default foreground is `clLime` = `$00FF00`, distinct from what the `GREEN` keyword
renders. *How proven:* `conflict-testA-term-color` — render the default TERM vs a
`GREEN`-keyword TERM; sample glyph-core RGB. *Result:* default glyph cores = **$00FF00**;
`greenkw` cores = **$09FF09** (exact, distinct). *Date/rig:* 2026-07-10, real P2 (Stephen),
read-back Claire. *Grounds:* C-R6 — v55 text "Green" INVERTS; `term.yaml` "Lime" + the manual
stand (add reader-note: no LIME keyword, reproduce with `GREEN`). *Source:* `campaigns/2026-07-debug-conflict-tests/conflict-testA-term-color.spin2`.

### EF-026 · FFT negative `LINESIZE` draws vertical FILLED BARS (width grows with |n|), not isolated lines — `CONFIRMED`
A negative FFT `LINESIZE` renders filled vertical bars whose width scales with `|n|`. *How
proven:* `conflict-testB-fft-linesize` — render at `+4`, `−4`, `−16`; measure bar geometry.
*Result:* `pos(+4)` = thin connected polyline; `neg(−4)` = filled bar ~6px; `neg16(−16)` =
rectangular filled bar ~12px. *Date/rig:* 2026-07-10, real P2 (Stephen). *Grounds:* C-R5 —
v55 text "isolated vertical lines" INVERTS; `fft.yaml` "filled bars of width |n|" + manual
stand. *Source:* `.../conflict-testB-fft-linesize.spin2`.

### EF-027 · LOGIC keyword ranges: `LINESIZE` default 3 (→32), `SAMPLES` max 2047, `SPACING` min 1 default 8 — `CONFIRMED`
*How proven:* `conflict-testC-logic-ranges` — render LOGIC at `LINESIZE` 1/3/7/20/32,
`SAMPLES` 1024/2047/2048, `SPACING` 1/2/8; use window-width as a pixel ruler + measure trace
thickness. *Result:* default `LINESIZE` = **3px** (= `ls3`), monotone 1→3→5→11→**17px** at 32,
no clamp; `SAMPLES` `s2047`=2097px vs `s2048`=2097px **identical** → **2048 clamps, max 2047**;
`SPACING 1` accepted (`sp1`114 ≠ `sp2`178), default `SPACING` = **8** (`def` width 562 =
64·8+50). *Date/rig:* 2026-07-10, real P2 (Stephen). *Grounds:* C-R1/C-R2/C-R3 — v55 text
(`1_to_7`/`4_to_2048`/`2_to_32`) INVERTS; `logic.yaml` + manual stand. *Source:* `.../conflict-testC-logic-ranges.spin2`.

> **⚠️ PARTIAL CORRECTION 2026-07-14 — the RANGES stand; the UNIT CONCLUSION was WRONG.**
> **STANDS:** `LINESIZE` default **3**, accepted to **32** (no clamp at 7); `SAMPLES` max **2047**;
> `SPACING` min **1**, default **8**. Those are unaffected.
> **RETRACTED: the "`LINESIZE 3` -> 3px, therefore 1:1 / whole-pixels" reading.** It took a single
> *small-n* point as proof of a 1:1 law. **EF-027's own curve refutes it:** widths 1,3,5,**11**,**17** for
> `LINESIZE` 1,3,7,**20**,**32** -> the slope from 20 to 32 is `(17-11)/(32-20)` = **0.5**. That is
> **half-pixels**, riding a ~1px anti-aliasing envelope that dominates at small n and vanishes at large n.
> Directly re-measured 2026-07-14 (`conflict-testL`, SCOPE, flat trace): `LINESIZE` 3/7/20/32 ->
> **2/4/10/16** logical px = **exactly n/2**. See **EF-041**.
> **Consequence:** the "half-pixel wording is BANNED" instruction derived from this entry was wrong, was
> propagated into the 2026-07-14 REF cleanup handoff, and caused correct half-pixel wording to be stripped
> from the REF. v55's "half-pixels" was right all along.

### EF-028 · PLOT TEXTSTYLE weight bits are honored but the DEBUG font does NOT visibly distinguish the four weights ($00 renders == $01) — `CONFIRMED`
The style byte's weight field (bits 0–1) selects nominal font weights — Pascal
`weight[0..3] = (100,400,700,900)` = thin/normal/bold/heavy (PLOT theory-of-ops) — but the
DEBUG display font does not render them distinctly: `$00` renders identically to `$01`, and
the source's own style-example notes `$02` = "same as 0". *How proven:*
`conflict-testD-textstyle` — render TEXT rows `$00`–`$03`; measure prefix ink %. *Result:*
`$00`=**18.66%** ≈ `$01`=**18.71%** (identical); `$02`=11.6%, `$03`=12.3%. *Date/rig:*
2026-07-10, real P2 (Stephen), PIL ink-% (Claire). *Grounds:* F-205a — the manual's "`$00` =
light (lighter than the `$01` default)" is REFUTED (no visible difference); the nominal
weight mapping (per Pascal) is correct as a *selector* but does not render distinctly. Fix
the manual to state the nominal mapping + this render caveat. *Source:* `.../conflict-testD-textstyle.spin2`.

### EF-029 · MIDI accepts a 24-bit `$RRGGBB` color (rgb24), not named-only — `CONFIRMED`
*How proven:* `conflict-testE-midi-color` — render MIDI keys colored via rgb24 (`$0000FF`,
`$00FF00`) vs the `GREEN` keyword; sample key colors. *Result:* `rgbBLUE($0000FF)`=blue,
`rgbGREEN($00FF00)`=green **== `keyword`(GREEN)**; a blue key cannot be a default/green-fluke →
rgb24 definitively parsed. *Date/rig:* 2026-07-10, real P2 (Stephen). *Grounds:* B26 — the
"force named-only" finding INVERTS; the manual's `$RRGGBB` example stands. *Source:* `.../conflict-testE-midi-color.spin2`.

### EF-030 · SCOPE default `SIZE` width is 256 (not 255) — `CONFIRMED`
*How proven:* `conflict-testF-scope-size` — render SCOPE at `SIZE` 255/256/512 + default;
measure window width. *Result:* `s255`=269px vs `s256`=270px (**exactly 1px apart**),
`s512`=526px (+256); `s_default`=**270 = the s256 rail**. *Date/rig:* 2026-07-10, real P2
(Stephen). *Grounds:* C-R7 — v55 text "255" INVERTS; `scope.yaml` "256×256" + manual stand.
*Source:* `.../conflict-testF-scope-size.spin2`.

### EF-031 · PLOT TEXTSTYLE justification is a per-axis HYBRID — horiz %10=right/%11=left, vert %10=top/%11=bottom — `CONFIRMED`
The value→direction mapping differs by axis. *How proven:* `conflict-testI-textstyle-justify`
— render a `$00` center-align control plus `$20`/`$30` (horiz) and `$80`/`$C0` (vert) against a
guide line; centroid analysis of ink vs the guide. *Result:* `$00` control straddles the guide
both axes (centroid ≈ anchor). **Horiz:** `$20`(%10) ink LEFT of anchor → right-justified;
`$30`(%11) RIGHT → left. **Vert:** `$80`(%10) ink below guide (top-edge pinned) → top; `$C0`(%11)
above → bottom. *Date/rig:* 2026-07-11 (00:58–00:59, both macOS + Windows), real P2 (Stephen),
centroid PIL (Claire). *Grounds:* F-205b — horiz **v55 text correct** (REF §4.3 inverts); vert
**REF correct** (v55 text inverts). Note vertical also confirms the Pascal source
(`2:ty:=h //top; 3:ty:=0 //bottom`); the manual's `2=bottom,3=top` is inverted → fix to
`2=top,3=bottom`. *Source:* `.../conflict-testI-textstyle-justify.spin2`.

> **RE-VERIFIED 2026-07-14 — EF-031 STANDS. Do not "correct" it, and do not align the manual to the REF here.**
> The 2026-07-14 REF rebuild asserts the **opposite ink on BOTH axes** (`%10` ⇒ *"the text sits to the RIGHT of
> the anchor"*) and adds the line *"Hardware measurement and the code agree."* **It does not.** Re-measured
> straight from the original `img-macOS/textI_horiz.bmp` / `textI_vert.bmp`, with PLOT's **Y-UP** mapping applied
> (`screen_y = 209 − user_y`; forgetting this is what makes the rows read in reverse order and is the trap here):
> both `$00` controls **straddle** the guide (so the instrument discriminates — the test is valid), and
> `$20`(%10) ink lands **LEFT** (x 72–157, centre 114.5, anchor 160) while `$30`(%11) lands **RIGHT**
> (163–247, centre 205.4); `$80`(%10) lands **BELOW** the guide (centre 122.4, guide 104) and `$C0`(%11)
> **ABOVE** (centre 89.6). Identical to the original record.
> The REF derives its claim from `2: tx := 0` and argues no implementation could put ink left of a zero offset —
> but silicon says it does, on both axes. **The mechanism is an open question for the REF/`.pas` side; the
> observation is not.** Manual `ch05:319-320` and `plot.yaml:67` match this ledger and are CORRECT — leave them.
> *(Aside: `conflict-testI` itself carried the ch05 COLOR/TEXT defect — the colour keyword sat before `SET`
> instead of before `TEXT`, so every row rendered default white and the intended colour-coding never happened.
> The test resolved anyway because its rows are separable by position. Fixed 2026-07-14.)*

### EF-032 · PLOT POLAR: θ=0 points EAST (+x); increasing θ is counter-clockwise; no flip — `CONFIRMED`
*How proven:* `conflict-testJ-polar-theta0` — render a POLAR wheel with four colored spokes at
0°/90°/180°/270°; sample color at ρ≈150 around the origin (200,200). *Result:* **East=RED(0°)**
(#BF0707), **North/up=GREEN(90°)** (#07BF07), West=BLUE(180°), South=YELLOW(270°) → θ=0 East,
increasing θ CCW (math convention), no flip. *Date/rig:* 2026-07-11 (both platforms), real P2
(Stephen). *Grounds:* F-208 — closes the ch05 POLAR flip-risk; fills a doc gap (θ=0 direction
was undocumented in manual + `plot.yaml`). *Source:* `.../conflict-testJ-polar-theta0.spin2`.

---

## PASM2 core & hub (silicon — 2026-07 conflict-test suite)

### EF-033 · AUGS/AUGD augment SURVIVES intervening instructions — "must immediately precede" is FALSE — `CONFIRMED-FALSE` (of the "immediately precede" claim)
The 23-bit augment prefix is consumed by the next instruction with a `#` immediate regardless
of intervening non-augmenting instructions. *How proven:* `conflict-testG-aug-intervening` —
compare a register's value after an augmented immediate reached via four intervening paths (M1
a NOP, M2 an ALU op (ROR), M3 two NOPs, M4 an ADD #S) vs an "absent-augment" rail. *Result:*
`noaug`=**$000001EF** (absent) vs `direct`=**$000055EF** (applied); M1/M2/M3/M4 **all =
$000055EF = direct**. *Date/rig:* 2026-07-10, real P2 (Stephen). *(Rig note: a run-1 `direct`
mismatch was rig-caught; relative rails unambiguous on re-run.)* *Grounds:* C-56 correct;
"augment must immediately precede" WRONG. Full write-up: catalog #644. *Source:* `.../conflict-testG-aug-intervening.spin2`.

### EF-034 · Hub egg-beater: scalar hub access ~15–16 clk each vs streaming ~2 clk/long (~7–8×) — `CONFIRMED`
*How proven:* `conflict-testH-eggbeater-timing` — cycle-count scalar `RDLONG` (×1, ×8) vs a
`SETQ`-block burst and a 16-long FIFO stream, using a base-2-clk NOP loop to resolve single
clocks. *Result:* `scalar1`=**15 clk**, `scalar8`=**16 clk/read**; `setq8`=**2 clk/long**,
`fifo16`=**2 clk/long**. *Date/rig:* 2026-07-10, real P2 (Stephen). *Grounds:* C-09 (scalar
RDLONG blocks ~9–16 clk) stands; egg-beater rotor confirmed. Full write-up: catalog #132.
*Source:* `.../conflict-testH-eggbeater-timing.spin2`.

### EF-035 · Two GETCTs bracketing a sequence add a fixed 2-clock measurement overhead (not 4) — `CONFIRMED`
The cost of measuring elapsed cycles with a GETCT pair is **2 clocks** (one GETCT's worth), not
4. *How proven:* `getct-overhead-char` — cog-resident (2-clk-exact) PASM: a back-to-back GETCT
pair (`d_ctrl`) plus 10-NOP (20-clk) and 20-NOP (40-clk) bracketed sequences (`d_10`/`d_20`).
*Result:* `d_ctrl`=**2**, `d_10`=**22**, `d_20`=**42** — overhead = 2 three independent ways
(`d_ctrl`; `d_10`−20; `d_20`−40), slope exactly 1 clk/clk (linearity confirms the reading tracks
inserted cycles, ruling out a fixed-value artifact — the two-tailed control). *Date/rig:*
2026-07-11, real P2 (Stephen), debug-log readback. *Grounds:* A-F2 — the Assembly manual's
"2-cycle measurement overhead" (chapter-04-timing) is CONFIRMED; the pre-sweep "4-cycle" figure
is REFUTED. **Scope note:** proves the overhead RESULT (2), NOT the intra-instruction latch
mechanism — a 2-clk overhead falls out for any consistent GETCT latch point (start *or* end), so
the manual states the result, not a "samples-at-start" rationale. *Source:*
`.../campaigns/2026-07-pasm2-timing/getct-overhead-char.spin2`.

---

## Smart pins

### EF-010 · %00101 (transition) Y=0 leaves the pin IDLE — `CONFIRMED-FALSE` (of the YAML claim)
Writing Y=0 in transition mode does NOT generate continuous transitions (the YAML claimed
it did) — the pin holds idle. Continuous square-wave generation is the NCO modes
(%00110/%00111). *Proof:* `test3-smartpin-00101-y0-continuous` over wired loopback P0→P2 /
P1→P3 — control pin at Y=2000 toggled then stopped; the Y=0 pin never toggled. *Date:*
2026-06-17. *Grounds:* F-135; `smart-pin-00101-transition-output.yaml` (false
`continuous_mode` block deleted).

### EF-011 · Universal smart-pin init order: enable BEFORE WYPIN — `CONFIRMED` (ratified)
The teachable order is **Reset (PINCLEAR/DIRL) → Setup (WRPIN/WXPIN) → Enable (PINHIGH/DIRH)
→ Operate (WYPIN)**. It is **REQUIRED** for trigger/serial modes (Y is held 0 during reset,
so WYPIN-before-enable never triggers) and **SAFE** for value modes (order-independent).
`pinstart()` (which does WYPIN before DIRH) is therefore **UNSAFE for the trigger modes**.
*Proof — the A/B sweep:* `test4` (transition: old order never toggled, new order worked);
`test60` pulse %00100 **PASS-REQUIRED** (old=0, new=1); `test61` NCO %00110 **PASS-SAFE**
(200/200); `test62` async-TX %11110 **PASS-REQUIRED** (0→1); `test63` DAC-noise %00001
**PASS-SAFE** (305/305). None failed. *Date:* 2026-06-17. *Grounds:* F-135/F-139; the
set-wide reorder across the smart-pin YAMLs.

### EF-012 · WRPIN #0 resets a RUNNING smart pin with NO DIR cycle — `CONFIRMED` (Titus right)
*Proof:* `batch1` RA-06 — `running=200, after=0`. *Date:* 2026-06-17. *Grounds:* IOSP ch4;
Titus cross-audit RA-06.

### EF-013 · NCO with Y=0 produces NO output (static) — `CONFIRMED`
*Proof:* `batch1` RA-12 — `Y=0 events=0`, control (Y>0) `events=200`. Corroborates EF-010
in a second mode. *Date:* 2026-06-17. *Grounds:* Titus cross-audit RA-12.

### EF-014 · DAC-noise (%00001) X=0 → sample period = 65 534 clocks (≈65536) — `CONFIRMED`
*Proof:* `batch1` RA-17 — measured `period = 65_534`. *Date:* 2026-06-17. *Grounds:* IOSP
ch18 §18.3; Titus cross-audit RA-17. (The "reduces switching power" half remains for Chip.)

### EF-015 · RDPIN acknowledge AUTO-RESTARTS an event-timing (%10010) measurement — `CONFIRMED`
*Proof:* `test50-eventtiming-rdpin-restart` — two successive measurements both arrived
(`ok1=1 Z1=99_949_010`, `ok2=1 Z2=99_999_239`). *Date:* 2026-06-17. *Grounds:* Titus
cross-audit RA-24; IOSP ch13.

### EF-016 · async-TX first-byte glitch + $FF-preclear — `NOT-OBSERVED` (real wire)
The widely-repeated "first async-TX byte is corrupted unless you send a $FF settling frame"
gotcha did NOT reproduce. Over a **real wired loopback (TX P0 → RX P2)**, the cold first
byte arrived clean with no settle and no preclear, for both `$A5` and `$01`. (Raw 32-bit
words showed a faint sub-bit line-settle signature that does not corrupt the decoded byte.)
*Proof:* `test51b-asynctx-firstbyte-glitch-wired`. *Date:* 2026-06-17. *Disposition:* do not
assert the gotcha as a rule; not forwarded to Chip (Stephen). *Grounds:* IOSP async chapter;
recorded in the IOSP disproven-findings staging doc. **Supersedes** the earlier inconclusive
internal-loopback `test51` (which had also accidentally applied the fix via the universal
init order).

### EF-017 · Concurrent single-signal counter cells (%10101/%10110/%10111) need BOTH A and B routed — `CONFIRMED`
The period-aligned X-clocks counter modes measure A-rise → B-rise (Y=%00). When several cells
watch one signal pin via relative-input routing, routing the **A-input only** (`P_MINUS*_A`)
**hangs**: each neighbour's B-input stays on its own idle pin, which never rises, so the window
never closes and IN never asserts. Routing **both** inputs (`P_MINUS*_A | P_MINUS*_B`) works.
*Proof:* `test70-f187-f192-concurrent-routing` — ~1 MHz NCO on P0 → P2 (jumper); rig phase
(mode %10010, A-only) proved all four cells' A-inputs LIVE (ticks≈199_850 for 1000 rises); then
**PASS A (A-only) → P3 TICKS / P4 HIGHS / P5 PERIODS all TIMEOUT**, **PASS B (A|B) → all READY**
(ticks=2_000_000, highs=1_000_000, periods=10_000, freq=1_000_000 Hz). A-routing byte-identical
across passes + proven A-liveness ⇒ the missing B-input is the sole cause. *Date:* 2026-07-04.
*Log:* `logs/debug_260704-125420.log`. *Grounds:* corrects F-187 (A-only); closes F-192. Agrees
with the Silicon Doc ("B can be tied to the A pin for single-pin measurement"), the working
`fb_measfreq2P` donor, and the released P2AN004 companion (`P_MINUS1_A | P_MINUS1_B`). *Applied:*
`smart-pin-10110/10111` YAML + IOSP ch15 §15 prose patched to route both inputs.

### EF-018 · Signed ADDS/SUBS/CMPS C-flag = TRUE SIGN (overflow-corrected), not bit-31 — `CONFIRMED`
On signed overflow the stored 32-bit result's bit 31 disagrees with the full-precision sign; silicon
sets C to the TRUE overflow-corrected sign — NOT bit 31, and NOT a signed-overflow flag. *Proof:*
`test71-signed-cflag-truesign` — six deliberately-overflowing cases, measured C = `0,1,0,1,1,0`, each
matching the true sign and OPPOSITE the bit-31 value: e.g. ADDS $7FFFFFFF+$1 → C=0 (result $80000000,
bit31=1); ADDS $80000000+$FFFFFFFF → C=1 (result $7FFFFFFF, bit31=0); SUBS/CMPS likewise. *Date:*
2026-07-04. *Grounds:* upgrades F-165 (adds/subs/cmps "true sign" wording) from documentary to empirical.

### EF-019 · Reordered smart-pin init preserves NCO phase-lock and sync-serial gapless streaming — `CONFIRMED`
The universal-order reorder (enable BEFORE WYPIN) does not disturb (a) a phase-locked NCO pair or
(b) sync-serial continuous double-buffering. *Proof (a):* `test72-nco-phaselock` — two NCOs set up with
the reordered init, 90° loaded via WXPIN, measured with mode %10011 through input routing (test70/F-192
machinery): period T=2000 clks exact, A→B offset **dead-stable at 1580 clks (0.79 T) across 4 repeats,
spread 0** ⇒ the pair starts and stays locked. *Proof (b):* `test73-syncserial-gapless` — %11100
continuous TX, reordered prime-after-enable: steady inter-word cadence 1584/1584/1592/1600 clks
(spread 16 ≈ one 8-bit word-time) ⇒ gapless double-buffer. *Date:* 2026-07-04. *Grounds:* closes the
F-139 residual hardware checks (the reorder was ratified order-insensitive by test61/EF-011; these two
special cases were flagged for a hardware look). *Note:* the phase read 0.79 T vs the ideal 0.75 T — a
fixed ~4% measurement/edge-definition offset, NOT drift (the zero spread is the phase-lock evidence).

### EF-020 · SETQ+WAITSEx = single-instruction event-OR-timeout; no-SETQ WCZ is a free flag-clear — `CONFIRMED`
A `SETQ` (future CT target) immediately before an event-wait makes that ONE stalling instruction release on whichever
comes first, reporting which via `WC`: event first → C=0, timeout first → C=1. With **no** preceding SETQ, no timer is
armed, so the event is always "first" and `WAITSEx WCZ` clears **both** C and Z (a legitimate free-flag-clear idiom).
*Proof:* `test74-waitse-setq-timeout` (P0, single cog, rising-edge event) — event-wins (edge before wait, far SETQ)
**C=0**; timeout-wins (P0 held low, near SETQ) **C=1**; no-SETQ `WCZ` (edge) **C=Z=0**. *Date:* 2026-07-04. *Grounds:*
refutes IOSP ch05's "no single instruction waits on an event and a timer at once" (F-193); confirms the forum
(evanh/TonyB) no-SETQ corner case. Mechanism is shared by the 14-instruction wait family (WAITSE1-4, WAITCT1-3,
WAITATN, WAITFBW, WAITINT, WAITPAT, WAITXFI, WAITXRL, WAITXRO). *Rig note:* first run used P16, which has external
hardware that held the level high (no-event case failed); moved to P0 + a discrete rising edge for determinism.

---

## Cross-cog data structures (silicon — 2026-07 P2AN007 rig suite)

*Campaign: `campaigns/2026-07-cross-cog-data-structures/` (5 rigs + GOLDEN analysis). All dual-tail:
each rig runs the correct discipline AND a deliberately-broken control with any injected delay applied
identically to both arms, and refuses to report PASS unless the broken arm actually fails. `pnut_ts`
v1.55.0 `-d`, real P2 silicon, RAM download, `_clkfreq = 200_000_000`, 2026-07-13.*

### EF-036 · Ring buffer: publishing the index BEFORE the record's fields tears every time — `CONFIRMED`
In a single-producer/single-consumer hub ring of multi-field records, advancing the publish index
**after** writing a slot's fields is what prevents a torn read; advancing it **first** exposes the slot
while it is still being written. *How proven:* `vt1-ring-buffer-integrity.spin2` — two arms, identical
1µs window between the two field writes, differing only in where the index advance happens; the
consumer checks the invariant `value == seq * 10` on every record it drains. *Result:* fields-then-index
= **0 torn records in 200,000**; index-then-fields = **200,000 torn in 200,000** (every record).
Reproduced identically on two runs. *Verdict:* CONFIRMED 2026-07-13. *Grounds:* P2AN007 R2 + the
`data-flow-contracts` ring/buffer-management patterns; the "publish the index LAST" rule is not a
stylistic preference but the entire safety property.

### EF-037 · A record packed into ONE long is NOT atomic unless it is published in ONE store — `CONFIRMED`
**The counter-intuitive one.** Spin2 v54 member bitfields let a whole record (opcode + argument +
sequence) occupy a single LONG. Fitting in one long does **not** make the record atomic: each bitfield
write is a **read-modify-write of the backing long**, so filling the *shared* record field-by-field is
several separate stores and a reader lands between them. Atomicity comes from staging the record in a
private local and publishing it with **one** whole-struct store (and snapshotting it with one
whole-struct load). *How proven:* `vt4-packed-long-atomicity.spin2` — two arms, identical 1µs window
between field writes, differing only in whether the fields are assembled privately first; the reader
takes a one-load snapshot and checks `arg == opcode * 100 and seq == opcode`. *Result:* staged +
one-store publish = **0 torn snapshots in 200,000**; the same fields written straight into the shared
long = **116,452 torn in 200,000** (109,642 on a prior run — reproduced). `SIZEOF(cmd_t)` = 4 bytes as
expected. *Verdict:* CONFIRMED 2026-07-13. *Grounds:* P2AN007 R5 + `concepts/struct-bitfields.yaml`;
this is the fact the recipe is built around, and it inverts the natural assumption that a
one-long record is inherently safe to publish.

### EF-038 · Latest-wins mailbox: the seq/ack handshake is LOAD-BEARING — removing it tears 100% for any worker that dispatches between reads — `CONFIRMED` (F-213)
A latest-wins mailbox whose worker reads `opcode`, `arg0`, `arg1` as three separate reads of shared
memory is protected **only** by the seq/ack handshake, which is what stops the writer overwriting the
command mid-read. *How proven:* `vt2-mailbox-publish-order.spin2` exp-2 — a **slow worker** (25µs
between reading the opcode and reading its arguments, modelling the near-universal `CASE cmd.opcode`
dispatch), with a matched control carrying the same slow worker and the ack present. *Result:* ack
present = **0 bad in 20,000**; ack removed = **20,000 bad in 20,000** (every single command torn). The
matched control is what isolates the ack as the cause rather than the injected delay. *Also measured
(the trap):* a **tight polling worker** with no work between its reads wins the race against the writer
and reports **zero** — so the missing ack *looks fine* under exactly the test most people would write.
Safety without the ack is contingent on worker timing. *Verdict:* CONFIRMED 2026-07-13. *Grounds:*
grounds **F-213** — P2AN007 v0.1.0's R3 invited the reader to drop the handshake ("drop that wait and
the newest command always wins"); v1.0.0 replaces it with a pitfall plus the two safe non-blocking
alternatives (pack the payload into one long per EF-037, or re-check the sequence after copying and
discard a straddling copy).

### EF-039 · One hardware lock serializes a concurrent enqueue read-modify-write; without it two writers collide — `CONFIRMED`
When two cogs enqueue to one queue, "advance the head index" is a read-modify-write they can interleave:
both read the same head, both write the same slot, and one record is lost while the head advances only
once. Bracketing the enqueue with a single P2 hardware lock (`LOCKTRY`/`LOCKREL`) makes it exclusive.
*How proven:* `vt3-lock-serializes-writers.spin2` — two writer cogs, identical 10µs window **inside**
the critical section in both arms, differing only in whether the lock brackets it; the consumer tracks
each writer's payload sequence and counts any gap or repeat as a lost/duplicated slot. *Result:* locked
= **0 anomalies in 20,000 drained**; unlocked = **3,331 anomalies**. *Verdict:* CONFIRMED 2026-07-13.
*Grounds:* P2AN007 R4 + `architecture/locks.yaml`. **Rig caveat worth carrying forward:** at a 1µs
window this rig reported 14,976 anomalies on one run and **0** on the next from a logic-identical
binary — two cogs running deterministic loops hold a near-fixed relative phase, so the collision was
decided at `cogspin` time rather than sampled. The 10µs window makes the overlap structural. See
`engineering/operations/lessons-learned/two-cog-race-rigs-must-be-structural.md`.

### EF-040 · STRUCT members pack with no padding — OFFSETOF/SIZEOF confirmed against the published layout numbers — `CONFIRMED`
Spin2 packs STRUCT members with no padding or alignment, and `OFFSETOF` (v53) / `SIZEOF` return exactly
that layout. *How proven:* `vt5-offsets-and-sizes.spin2` asserts every layout number P2AN007 prints to a
reader, then writes the header through raw addressing (`WORD[@buf + OFFSETOF(hdr_t.length)] := …`) and
reads it back by name through a `^struct` pointer view of the same bytes. *Result (11/11 PASS):* for
`hdr_t(LONG magic, WORD length, BYTE kind, BYTE flags)` — `OFFSETOF` magic=**0**, length=**4**,
kind=**6**, flags=**7**; `SIZEOF(hdr_t)`=**8**; payload starts at **+8**; every raw-addressed write read
back correctly by name. For `reading_t(LONG timestamp, LONG value, BYTE status)` — `SIZEOF`=**9**.
*Verdict:* CONFIRMED 2026-07-13. *Grounds:* P2AN007 R6/R1 + `methods/offsetof.yaml`; confirms the
Verify text the note prints is correct as published.


### EF-041 · `LINESIZE` and `DOTSIZE` units are decided by the shift constant: `shl 6` = HALF-pixels, `shl 7` = WHOLE pixels — `CONFIRMED`
The rendered size of a `LINESIZE`/`DOTSIZE` value is **not** one rule across the windows — it follows the
call site's shift, exactly as the v55 text says. *How proven:* `conflict-testK-dotsize-render` (isolated dots,
`LINESIZE 0`, constant feed) + `conflict-testL-scope-linesize` (flat trace, `DOTSIZE 0`); measured on the
captured BMPs, halved for the 2x Retina device-pixel scale (the window's own declared `SIZE` is the ruler).
*Result (logical px):*
| directive | path | measured | v55 says |
|---|---|---|---|
| SCOPE `DOTSIZE` | `shl 7` | 2→2, 4→4, 8→8, 16→16, 32→**32** (slope **1**) | "dot size **in pixels**" ✅ |
| SCOPE_XY `DOTSIZE` | `shl 6` | 2→1, 6→3, 12→6, 20→**10** (slope **½**) | "dot size in **half-pixels**" ✅ |
| SCOPE `LINESIZE` | `shl 6` | 3→2, 7→4, 20→10, 32→**16** (slope **½**) | "line size in **half-pixels**" ✅ |
**v55 is correct on every one.** `shl 7` face value = a whole-pixel **diameter**; `shl 6` face value = **half-pixels**
(i.e. rendered width = n/2). At small n a ~1px anti-aliasing envelope inflates the measurement — which is exactly
what made EF-027 misread its own data. FFT `DOTSIZE` is the same `shl 7` path as SCOPE (inferred, not measured).
**CONFIRMED ON PNut (ground truth) 2026-07-14** — captures re-run on real PNut (1×, no Retina) give the *same law*:
SCOPE `DOTSIZE` 2→2, 4→4, 8→8, 16→16, **32→32** (slope **1**); SCOPE_XY `DOTSIZE` 2→1, 6→3, 12→7, **20→11**;
SCOPE `LINESIZE` 3→2, 7→4, 20→10, **32→16** (slope **½** across the large-n points, where the ~1px AA floor stops
mattering). **PNut and pnut-term-ts agree, and both agree with v55** — so term-ts is at parity here, and the
correction rests on ground truth, not on the port.
*Date/rig:* 2026-07-14, real P2 (Stephen), **both PNut and pnut-term-ts**; corroborated 4 ways (v55 text + the
Pascal's shift geometry + both renders). *Grounds:* supersedes EF-027's unit conclusion; settles H-2/H-3.
*Source:* `campaigns/2026-07-debug-conflict-tests/conflict-testK-dotsize-render.spin2`, `campaigns/2026-07-debug-conflict-tests/conflict-testL-scope-linesize.spin2`.

### EF-042 · BITMAP `SPARSE` draws ROUND DOTS on a SOLID BACKGROUND FILL, and the `DOTSIZE >= 4` gate is REAL — `CONFIRMED (PNut + pnut-term-ts)`
*How proven:* `conflict-testM-bitmap-sparse` — a 6×4 canvas of pure-green `$00FF00` pixels at `DOTSIZE 12`, with
`SPARSE $FF0000`, captured via `SAVE WINDOW` (a plain BITMAP `SAVE` writes the bitmap **1× un-DOTSIZEd** and would
have shown nothing). Rail: the same window with **no** `SPARSE` contains **no red at all**. *Result:* the sparse
window renders as a **solid red field carrying a grid of round green dots** — the sparse colour is a full-cell
**background fill** behind a round dot drawn in the pixel's own colour (dot ≈ ¾ of the cell; measured green/(green+red)
= 43%, against 44% predicted for a ¾-diameter disc in its cell). *Date/rig:* 2026-07-14, real P2 (Stephen), pnut-term-ts.
*Grounds:* v55 L1331 ("large **round** pixels against a **coloured background**") and the REF ToO ("a solid fill of the
whole cell") are **CORRECT**; the manual's `ch04:49` ("outline each magnified pixel … the outline (grid) colour") and
`bitmap.yaml:32` ("grid-border colour") are **WRONG** — figure and ground inverted. `ch04:398-400` was already right.
**THE `DOTSIZE >= 4` GATE IS REAL — CONFIRMED 2026-07-14** (`conflict-testP-sparse-gate`, 20×15 canvas so even
`DOTSIZE 3` yields a real window; read reduced to a binary "is there any RED?"):
| capture | red | verdict |
|---|---|---|
| RAIL-OFF (DS12, no `SPARSE`) | **0.0 %** | rail holds — red can only come from `SPARSE` |
| RAIL-SHAPE (DS12, `SPARSE`) | **42.3 %** | rail holds — the instrument discriminates |
| **`DOTSIZE 3`** | **0.0 %** | **`SPARSE` self-disables** |
| **`DOTSIZE 4`** | **20.8 %** | **`SPARSE` active** |
Bracketed exactly at **3 → off / 4 → on**. *Rig:* pnut-term-ts (the PNut leg of this run was invalidated by *our*
test design, not by disagreement — see below).
> ⚠️ **Test-design lesson (recorded because the failure is instructive).** The first `conflict-testP` gave its four
> windows **no `POS`**. That is fine on pnut-term-ts, which **auto-arranges** them — but PNut has **no auto-layout**
> and **stacks** every no-POS window at the host origin. Since `SAVE WINDOW` is a **desktop scrape of a screen
> rectangle**, all four PNut windows occluded one another and both DS12 scrapes returned the **byte-identical**
> image (md5 `4856803a…`). Rails that cannot discriminate ⇒ INCONCLUSIVE, never a verdict.
> **That failure is itself independent confirmation of EF-043** — PNut windows *do* overlap. `conflict-testP` now
> carries an **explicit `POS` on every window** and is re-runnable on both tools.
> ### 🔴 PROVENANCE — THIS ENTRY RESTS ON THE MIRROR, NOT ON GROUND TRUTH (flagged by Stephen, 2026-07-14)
> **Every observation in EF-042 was made on pnut-term-ts.** The PNut leg of both runs is **VOID**:
> `conflict-testM`/`conflict-testP` gave their BITMAP windows **no `POS`**, and PNut (unlike term-ts) has **no
> auto-layout** — all four windows stacked at the host origin. Since `SAVE WINDOW` is a **desktop scrape**, every
> PNut capture grabbed whichever window was **topmost** (`Gp04`, created last). Proof: `gateP_ds03` is
> **byte-for-byte a top-left crop of `gateP_ds04`**, and the two DS12 scrapes were byte-identical (md5 `4856803a…`).
> **Not one PNut gateP capture shows the window it names.**
>
> **This matters:** EF-042 is what reverses `ch04:49` from "outline / grid-border" to "background fill" — a
> reader-facing change — and **pnut-term-ts is a PORT that has diverged from PNut four times this week**
> (SCOPE_XY polar, PLOT vertical TEXTSTYLE, PLOT `OPACITY`, `SAVE…CLOSE`). A render measured on the mirror is not
> ground truth. `reference_pnut_is_ground_truth_termts_mirrors`.
>
> **What DOES support it, short of a PNut render:** the Pascal (`SmoothShape` — a round dot over a full-cell square)
> and **v55 L1331** ("large **round** pixels against a **coloured background**") both agree with what term-ts drew.
> Three-way agreement, but **zero PNut pixels.**
>
> **TO CLOSE:** re-run the **fixed** `conflict-testP` on PNut — it now carries an **explicit `POS` on every window**,
> so they cannot occlude one another. Until then EF-042 must not be cited as PNut/P2 ground truth, and `ch04:49`
> must not ship on it.

**BONUS (pnut-term-ts log only — PNut emits no such log) — BITMAP window size = canvas × `DOTSIZE`, exactly 1:1** (read free from the pnut-term-ts placement log,
no measurement needed): `BITMAP 'SpGate' **18x12**` (canvas 6×4 at `DOTSIZE 3`) and `BITMAP 'SpOff'/'SpOn' **72x48**`
(same canvas at `DOTSIZE 12`). 6×3=18, 4×3=12; 6×12=72, 4×12=48. This also states plainly why the `DOTSIZE 3` capture
was unreadable — an 18×12 window is **smaller than its own title bar.** The log said so before a single pixel was
counted.
*Source:* `campaigns/2026-07-debug-conflict-tests/conflict-testM-bitmap-sparse.spin2`, `campaigns/2026-07-debug-conflict-tests/conflict-testP-sparse-gate.spin2`.

### EF-043 · No-POS window placement is TOOL-DEPENDENT — pnut-term-ts AUTO-ARRANGES (no overlap); PNut has no such feature — `CONFIRMED (pnut-term-ts)`
*How proven:* `conflict-testN-pos-origin-overlap` — three PLOT windows created with **no `POS`**, in decreasing size.
The instrument turned out to be the **log, not the screenshot**: pnut-term-ts emits a `WINDOW_PLACED` line per
auto-placed window. *Result:* `Pa` (400×300) → `POS 1076,60`; `Pb` (300×220) → `POS 622,60`; `Pc` (200×150) →
`POS 1680,60` — **distinct x, common y, tiled, NOT overlapping, NOT cascaded.** The 4th window, created with an
**explicit** `POS 500 0`, got **no** `WINDOW_PLACED` line — the layout engine only engages when `POS` is absent.
*Date/rig:* 2026-07-14, real P2 (Stephen), **pnut-term-ts**.
**PNut half now has DIRECT EVIDENCE (2026-07-14):** the `conflict-testP` PNut run gave four no-POS BITMAP windows,
and two same-sized `SAVE WINDOW` desktop scrapes came back **byte-identical** — which is only possible if the windows
were **stacked on top of one another at a common origin**. PNut overlaps; it does not tile and does not cascade.
**⚠️ THIS IS A TOOL BEHAVIOUR, NOT A P2/PNut FACT.** Stephen: *"pnut-term-ts has special auto-layout ability when no
POS directive is specified… PNut on Windows has no such capability."* PNut places every window at its host display
origin and display windows do **not** cascade, so successive no-POS windows there **overlap**. **Both are true, of
different tools.** *Consequences:* (1) `logic.yaml` / `term.yaml` claim windows "don't overlap" — that is **term-ts
behaviour recorded as P2 fact**, a KB defect. (2) The manual must **not** assert either placement; it should teach
"omit `POS` and your tool places the window for you" and print **no pixel values**.
*Source:* `campaigns/2026-07-debug-conflict-tests/conflict-testN-pos-origin-overlap.spin2`.

### EF-044 · SCOPE_XY `SIZE` is a RADIUS: the canvas is 2×SIZE, and the default is radius 128 (a 256×256 canvas) — `CONFIRMED`
*How proven:* read straight off the pnut-term-ts placement log in `conflict-testO`. *Result:* `SCOPE_XY Good SIZE 150`
→ window **340×340** (canvas 300×300 = 2×150, + 40px margins); `SCOPE_XY Bad` with **no** `SIZE` → window **296×296**
(canvas **256×256**, i.e. an implied radius of **128**). **PNut-CONFIRMED (2026-07-14):** the `SIZE`-is-a-radius half is independently visible in the PNut captures —
`conflict-testK`'s `SCOPE_XY SIZE 150` window saves at **360×360** (canvas **300** = 2×150, + margins). *(The
`default = 128` half still rests on the term-ts placement log; PNut emits no such log. Low risk — v55 states it —
but note the provenance.)*
*Date/rig:* 2026-07-14, real P2 (Stephen); radius half on **both PNut and pnut-term-ts**, default half term-ts only.
*Grounds:* v55 L1179 ("display **radius**", default **128**) is **CORRECT**; the pre-cleanup SCOPE_XY ToO §4a claim of
"SIZE default 256 (→ 512 px)" was wrong (it mistook the stored pixel width for the directive's argument), which the
2026-07-14 REF rebuild had already fixed. This is the independent confirmation. *Source:* `campaigns/2026-07-debug-conflict-tests/conflict-testO-scopexy-parser-hang.spin2` (log).

### EF-050 · BITMAP `SET` out-of-range is NOT clamped — the manual was RIGHT and the REF is WRONG — `CONFIRMED (PNut)`
**This one PREVENTED a regression: we were about to reverse correct shipped text.** *How proven:* `conflict-testQ` Q6 —
an 8×8 BITMAP cleared to black, then `` `SET 999 999 `` followed by a single **white** pixel. *Result:* the saved canvas
is **100 % BLACK — no white pixel anywhere.** A clamped `SET` would have put it at **(7,7)**. It is not there.
⇒ **`SET` out-of-range is NOT clamped.** The REF's "`KeyValWithin` = assign-and-clamp" reading does **not** hold for
`SET`, and the manual's `ch04:241` — *"an out-of-range coordinate is **ignored, not clamped**"* — **is CORRECT AS
SHIPPED. Do not reverse it.** (The `FIX-MANUAL` item that would have done so is **killed**.)
*Honest caveat:* the test fed exactly 64 pixels into a 64-pixel canvas, so the write pointer was already past the end
when `SET` fired — "ignored" and "accepted-then-drawn-off-canvas" both predict no white pixel. **The CLAMP hypothesis is
dead either way**, which is all the manual turns on; the precise mechanism is not cleanly isolated. A follow-up (feed 32
pixels, then `SET 999 999`, then a white pixel) would separate them.
*Date/rig:* 2026-07-14, real P2 (Stephen), PNut v55.
*Source:* `campaigns/2026-07-debug-conflict-tests/conflict-testQ-doc-claims-battery.spin2`.

### EF-051 · A keyword placed after `SAVE` is CONSUMED AND DISCARDED — `` `Win SAVE CLEAR `` writes no file AND loses the CLEAR — `CONFIRMED (PNut)`
*How proven:* `conflict-testQ` Q2 — two identical green BITMAPs. One is sent `` `SAVE CLEAR ``; the other (the **rail**)
is sent a plain `` `CLEAR ``. *Result:* the `SAVE CLEAR` window is **100 % GREEN** (the `CLEAR` never ran) and **no file
was written**; the rail window is **100 % BLACK** (a plain `CLEAR` works perfectly). The rail discriminates, so the
finding is real and not a dead feed. *Date/rig:* 2026-07-14, real P2 (Stephen), PNut v55.
**Reader consequence:** `SAVE` swallows the next keyword. Put `SAVE 'name'` **last**, or you silently lose both the file
and the command you thought you sent.
*Source:* `campaigns/2026-07-debug-conflict-tests/conflict-testQ-doc-claims-battery.spin2`.

### EF-052 · A runtime `` `RATE -1 `` FREEZES BITMAP auto-refresh — and v55's own Feeding table advertises it as legal — `CONFIRMED (PNut)`
*How proven:* `conflict-testQ` Q4/Q5 — two identical green BITMAPs are each fed a full canvas of **red**. One is first
sent `` `RATE -1 `` (the test); the other `` `RATE 6 `` (the **rail**). *Result:* the `RATE -1` window stays **100 %
GREEN — auto-refresh froze**; the rail window goes **94 % RED — still refreshing**. The rail proves the feed was alive,
so the freeze is real. *Mechanism (REF):* the `-1` → `width×height` substitution happens **only at the end of
`BITMAP_Configure`**; the update handler is a bare `KeyVal(vRate)`, and the rate cycle tests **equality** against a
counter that only counts up from 0 — so a negative rate can never match. A later `TRACE`, `CLEAR` or explicit `UPDATE`
un-freezes it. *Date/rig:* 2026-07-14, real P2 (Stephen), PNut v55.
**Reader consequence — a real trap:** **v55 L1342's Feeding table advertises `RATE -1` as a runtime directive.** It is
meaningful **only in the create message**. At runtime it silently kills the display.
*Source:* `campaigns/2026-07-debug-conflict-tests/conflict-testQ-doc-claims-battery.spin2`.

### EF-046 · PNut v55 `SAVE WINDOW` captures the WRONG RECTANGLE — truncated, offset, sometimes the neighbouring window — `CONFIRMED (PNut)` — TOOL BUG
`SAVE WINDOW 'name'` is meant to write a `.bmp` of the **entire window**. On PNut v55 the capture rectangle is both
**too small** and **mis-positioned**, and it fails **silently** — the file is a valid `.bmp` of plausible size, so
nothing signals that the capture is bad. *How proven:* `conflict-testQ-doc-claims-battery` + `conflict-testP-sparse-gate`
— several BITMAP windows at **explicit, non-overlapping `POS`**, each saved **both ways** (plain `SAVE` and `SAVE WINDOW`).
*Result:*
| observation | evidence |
|---|---|
| **Truncates the bottom** | window = ~50px title bar + 64px canvas ≈ **114px** tall; capture = **93px**. The bottom **~21 rows of canvas are missing**, and ~4px of desktop wallpaper bleeds in on the right ⇒ the rect is offset horizontally too. |
| **Can miss the window entirely** | four other windows' `SAVE WINDOW` files contain **nothing but desktop wallpaper** — correct dimensions, zero window content. |
| **Can capture the WRONG window** | the `SPARSE` window (`POS 300 0`) returned a **solid green** image — the content of its **non-sparse neighbour** at `POS 0 0`. A plain `SAVE` of that same window, moments later, correctly showed the red-background/green-dot sparse pattern. |
**The plain `SAVE` form is CORRECT in every case we exercised** — it writes the window's own buffer: occlusion-immune,
chrome-free, and accurate. *(It is 1× un-`DOTSIZE`d, per v55 L1347 — which is why `SAVE WINDOW` is the documented tool
for capturing a magnified view, and why this bug matters. A `SPARSE` window is the exception: it allocates at physical
size, so its plain `SAVE` comes out magnified.)*
*Date/rig:* 2026-07-14, real P2 (Stephen), PNut v55 (Windows); confirmed visually by Stephen.
*Grounds:* **This dissolves an apparent mystery** — we briefly suspected PNut's *screen* did not render `SPARSE`, because
`SAVE WINDOW` returned solid green for a sparse window. It was the same bug: the rect had drifted onto the neighbour.
**One bug, not two.** Bug report drafted: `DRAFTS/PNUT-BUG-save-window-wrong-rect.md`.
*Methodological note:* every `SAVE WINDOW`-based read in this campaign is therefore **void**; the tests were rewritten
to use plain `SAVE` throughout. Stephen called this early — *"I would think you'd get window specific content if using
save only even when overlap"* — and he was right, for a better reason than either of us had.

> **ROOT CAUSE (added 2026-07-14) — provenance: PNut-Term-TS team source/binary analysis, NOT our silicon run.**
> `KeySave` feeds the form's `Left/Top/Width/Height` straight into a `BitBlt` from a **desktop DC**, assuming the
> process's window coordinates are physical screen pixels. `PNut_v55.exe` ships with **no application manifest** ⇒
> the process is **DPI-unaware** ⇒ above 100% display scaling Windows virtualizes its coordinate space while the
> framebuffer stays physical. Our own numbers corroborate it: the file is **70×93** — the form's own `Width`/`Height`
> written straight through — against a window measuring **~114** on screen, and `93 × 1.25 = 116`. **Our observations
> above stand unchanged; this explains them.**
> **RETRACTED:** our bug report's original "suggested area to look at" (client-vs-outer-frame rectangle) was **wrong**
> — `Width`/`Height` on a VCL top-level form *are* the outer frame. Corrected in the report before routing.
> **One datum still unexplained:** we observed the wallpaper strip on the **right** edge; the DPI model predicts
> **left**. Open question back to us — Stephen's box is the only one that can settle it (re-run at 100% scaling).
*Source:* `campaigns/2026-07-debug-conflict-tests/conflict-testQ-doc-claims-battery.spin2`, `…/conflict-testP-sparse-gate.spin2`.

### EF-047 · `SAVE` writes the FRONT buffer — under `UPDATE` mode you capture the STALE previous frame — `CONFIRMED (PNut)`
*How proven:* `conflict-testQ` Q3 — a BITMAP created with `UPDATE` (buffered). Fill **RED** → `` `UPDATE `` (red is now
the front buffer) → fill **GREEN** but do **not** update → `` `SAVE ``. *Result:* the saved file is **100% RED**. The
live green buffer was not captured. *Date/rig:* 2026-07-14, real P2 (Stephen), PNut v55. *Grounds:* confirms the REF's
front-buffer reading. **Reader consequence:** in buffered mode you must send `` `UPDATE `` *before* `` `SAVE ``, or you
will silently save the previous frame. This is live in ch04, ch05 and ch15 — all of which run buffered.
*Source:* `campaigns/2026-07-debug-conflict-tests/conflict-testQ-doc-claims-battery.spin2`.

### EF-048 · PLOT `OPACITY 256` WRAPS to 0 — fully TRANSPARENT, the exact inverse of "fully opaque" — `CONFIRMED (PNut)`
*How proven:* `conflict-testQ` Q7 — two dots on a black PLOT: left at `OPACITY 255` (the rail), right at `OPACITY 256`.
*Result:* the capture shows **one dot**. The `OPACITY 255` dot is visible; the `OPACITY 256` dot is **absent**. The value
is assigned into a byte with range-checking off, so 256 → **0**. *Date/rig:* 2026-07-14, real P2 (Stephen), PNut v55.
**Reader consequence — a genuinely nasty trap:** a user reaching for "more opaque than 255" types 256, and **everything
they draw afterwards disappears**. The failure looks like "my drawing commands stopped working."
*Source:* `campaigns/2026-07-debug-conflict-tests/conflict-testQ-doc-claims-battery.spin2`.

### EF-049 · `CLOSE` is UPDATE-FIRST, CLOSE-SECOND — and a bare `SAVE` (no filename) writes nothing — `CONFIRMED (PNut)`
*How proven:* `conflict-testQ` Q8 + Q1. **Q8:** `` `q8 SAVE 'q8_saved' CLOSE `` — a single message carrying both.
*Result:* **`q8_saved.bmp` was written AND the window closed** (Stephen, visually). So the rest of the message executes
before the close — the `` `Win SAVE 'shot' CLOSE `` idiom is real and usable. **Q1:** a bare `` `SAVE `` with no
filename produced **no file at all**, silently (the rail — a normal `SAVE 'name'` — wrote its file). *Date/rig:*
2026-07-14, real P2 (Stephen), PNut v55. *Grounds:* confirms the REF's `p2com.asm` dispatch reading (EF-045) and the
`KeySave` grammar. **Reader consequence:** the filename is mandatory and must come last; without it nothing is written
and nothing complains.
*Source:* `campaigns/2026-07-debug-conflict-tests/conflict-testQ-doc-claims-battery.spin2`.

### EF-045 · A bare number in a SCOPE_XY create message HANGS PNut — and pnut-term-ts does NOT share the defect — `CONFIRMED (PNut) / REFUTED (pnut-term-ts)` — a TOOL DIVERGENCE
The suspected infinite loop (`SCOPE_XY_Configure`'s `while not NextEnd do` matching neither `NextKey` nor `NextStr`,
so `ptr` never advances) **does not occur in pnut-term-ts**. *How proven:* `conflict-testO-scopexy-parser-hang` — a TERM
**heartbeat** is the instrument, distinguishing "the tool hung" from "the window just didn't open". *Result:* the
heartbeat printed `pre 1…5`, the suspect line `` `SCOPE_XY Bad 128 'A' `` executed, and the heartbeat continued
`post 1…20` → **"NO HANG - parser recovered"**. Moreover the `Bad` window **was created**, at the **default** 256×256
canvas — so the stray number ended (or was skipped in) the config parse rather than hanging it, and the `'A'` label
after it was not applied. *Date/rig:* 2026-07-14, real P2 (Stephen), pnut-term-ts.
**🔴 PNut RESULT (2026-07-14, Stephen, visual): PNut HANGS — frozen at `` `Beat 13 'pre  ' 5 ``.** That is the last
output before the suspect line, i.e. the exact predicted signature. The source-derived hypothesis is **CORRECT for
PNut**: `SCOPE_XY_Configure`'s loop is `while not NextEnd do begin if NextKey then … else if NextStr then … end;` — an
`ele_num` element matches **neither** branch, so `ptr` is never advanced and `NextEnd` never fires. **Infinite loop.**

**This is a genuine TOOL DIVERGENCE, and the poster child for `PNut is ground truth; term-ts mirrors`:**
| tool | result |
|---|---|
| **PNut** | **HANGS** (heartbeat frozen at `pre 5`; the `Bad` window never opens) |
| **pnut-term-ts** | **No hang** — heartbeat ran `post 1…20`; the `Bad` window was even created, at its default 256×256 canvas (the stray number ended the parse rather than hanging it) |

**Why the instrument mattered:** a screenshot could not have answered this — a hung tool writes no file, and "no file"
is indistinguishable from "the window never opened". The **TERM heartbeat** is what separates *hung* from *absent*.

**Trigger is a PLAUSIBLE TYPO, not a contrived input:** `` debug(`SCOPE_XY W 128 'A') `` — a user who meant `SIZE 128`
and dropped the keyword. No error, no diagnostic: the tool simply locks up. **SCOPE and FFT are NOT exposed** (their
configure loops are `while NextKey do`, which merely truncates the parse).

**CLASS-WIDE SWEEP DONE (2026-07-14) — blast radius is exactly ONE window:**
| configure loop | windows | exposed? |
|---|---|---|
| `while NextKey do` | SCOPE, FFT, SPECTRO, PLOT, TERM, BITMAP, MIDI | **No** — a non-key element ends the loop |
| `while not NextEnd do` **+ `if NextNum then Break;`** | **LOGIC** | **No** — explicitly guarded |
| `while not NextEnd do`, **no number guard** | **SCOPE_XY** | 🔴 **YES — hangs** |

LOGIC and SCOPE_XY are the **only** two windows that accept **channel-label strings on the create line**, so they are
the only two that cannot use `while NextKey do` — they must run to end-of-message and dispatch on *key or string*.
`LOGIC_Configure` guards the third case (`if NextNum then Break;   // number not allowed`); **`SCOPE_XY_Configure` is
missing exactly that line.** The fix is one line, and LOGIC already contains it.
*(This also cross-checks **EF-003**: SCOPE uses `while NextKey do`, so a channel-def **string** on its create line ends
the config loop — which is precisely why the SCOPE window is never created.)*

*Consequences:* (1) **ch08 must now carry the warning** — it is a real hazard, and the "write nothing until confirmed"
hold is lifted. (2) **PNut v55 bug report drafted:** `DRAFTS/PNUT-BUG-scope-xy-parser-hang.md` (minimal repro,
mechanism, blast radius, one-line fix) — for Stephen to route to Parallax/Chip.
*Source:* `campaigns/2026-07-debug-conflict-tests/conflict-testO-scopexy-parser-hang.spin2`.

## 2026-08 manual-corrections campaign (P2 Edge, 200 MHz)

<!-- Bench leg 2026-08-14. Probes + logs: campaigns/2026-08-manual-corrections/tests/.
     Authoring source with full evidence grading: that campaign's BENCH-FINDINGS-FOR-AUTHORING.md.
     Grades used below: [M] measured after the DEBUG_COGS fix (EF-057); [M-pre] measured before it —
     trustworthy where the test uses no streamer. Documentary and inferred material from that
     campaign is deliberately NOT carried here; this ledger holds only what our board showed us. -->

### EF-053 · Hub access inside a CORDIC fill or drain loop silently loses results; register-only loops stay clean to FILL=7 — `CONFIRMED`
Deep CORDIC pipelining works. What breaks it is **hub I/O inside the fill or drain loop** — and it
fails *silently*: the reader gets wrong numbers, not missing ones. *How proven:*
`test-f263-cordic-pipeline-depth` — four arms issuing `QMUL` and retrieving with `GETQX`, differing
only in where hub access sits, swept FILL 1→7 against single-op `ROTXY` ground truth. **Control that
must fail:** queue-one-then-retrieve **stalled 58 clocks**, exactly the documented `GETQX` maximum
(`2…58`) — the rig was proven able to see the failure mode before any arm was trusted. *Result:* arm
**B** (`RDLONG` inside fill) first wrong at **FILL=2**; arm **C** (`WRLONG` inside drain) at
**FILL=3**; arm **D** (register-only fill *and* drain, hub I/O batched outside) **clean through
FILL=7**; arm **A** (Assembly ch.5 shape — two `RDLONG`s plus `CALL`/`RET` per issue) **15 of 16
results wrong**. Seven runs, fully consistent. *Date/rig:* 2026-08-14, real P2 (Stephen). [M-pre —
streamer-free, so the debug confound does not apply; 7 runs.] *Scope — do not overstate:* this
measures **where** results are lost, not **why**. We did not test every hub operation or cadence, so
state it as the tested shape — keep hub access out of both loops — not as an absolute law about "any
hub access", and do not prescribe a clock-level discipline we did not measure. *Grounds:* F-263;
**refutes** the community report of a ~2-deep result buffer; Chip's fill/steady/drain model stands.
**Two of our own shipped documents violate it:** `P2AN002/examples-library/cordic-pipeline-throughput.spin2`
and Assembly `chapter-05-hardware.md:~100-126`. *Source:* `campaigns/2026-08-manual-corrections/tests/test-f263-cordic-pipeline-depth.spin2`.

### EF-054 · A cog DAC drives with `TT=%01` alone; `P_OE`, `P_CHANNEL` and `P_TT_01` are ONE bit, so composing them with `+` breaks the mode — `CONFIRMED`
The Streamer Guide's cog-DAC recipe is **correct** — `TT=%01` drives, and `OUT` is irrelevant to it.
The real defect the sweep exposed is arithmetic: `P_OE`, `P_CHANNEL` and `P_TT_01` are three names for
the **same** bit-field value, so `P_CHANNEL + P_OE` carries `%01 + %01` into `%10` = `P_BITDAC`, a
different mode that does not drive. *How proven:* jumper P0→P1 (continuity verified digitally first);
P0 a cog DAC with `%TT` swept, P1 read by a smart-pin ADC (`P_ADC_1X | P_ADC`, `WXPIN` 12, `RDPIN`).
*Result:* `%00` = 1,408 (no drive) · **`%01` = 6,737 — drives** · `%10` = 1,409 · `%11` = 1,408 ·
`%01` with `OUT=1` = 6,737 (OUT irrelevant) · **`P_CHANNEL + P_OE` via `+` = 1,407 — dead**.
Reproduced three times; an independent replication returned 6,737 / 1,410. *Date/rig:* 2026-08-14,
real P2 (Stephen). [M-pre — streamer-free.] *Grounds:* F-259 — **CONFIRMED-FALSE** for the community
report that the recipe drives nothing (the reporter compared `%01` against `%10`, not with-OE against
without). Class sweep: 281 doc config lines use `|`, exactly **2** use `+`, both in the Streamer Guide
(`streamer-body.md:1238`, `:1306`) and both computing correctly today — a latent trap, not a live bug.
*Source:* `campaigns/2026-08-manual-corrections/tests/test-f260-goertzel.spin2`.

### EF-055 · In `DAC_MODE` with the smart pin off, `TT=%01` switches the DAC's SOURCE — adding `P_OE`/`P_CHANNEL` to a level-driven DAC kills its output — `CONFIRMED`
`%TT` is **context-dependent**, keyed on whether the smart pin is on and whether `DAC_MODE`
(`M[12:10]=%101`) is active. With the smart pin off in `DAC_MODE`, `TT=%01` does not "enable output" —
it selects a **cog DAC channel** as the source instead of the pin's own level field. *How proven:* a
`P_DAC_124R_3V` pin driven from its level field, measured before and after adding `P_CHANNEL`.
*Result:* level-driven spread **1,305 of 2,000 samples**; **adding `P_CHANNEL` dropped it to 25.**
*Date/rig:* 2026-08-14, real P2 (Stephen). [M-pre — streamer-free.] *Grounds:* F-264 — the KB's
`architecture/smart_pins.yaml:249-253` carries the four-context table correctly, but
`language/spin2/methods/wrpin.yaml`'s `tt_field` gives one context-free meaning and its
`p_oe_required_for: "All output modes (… DAC …)"` is **wrong for the non-smart-pin DAC**. **This is
the highest-severity class we carry: guidance that, applied in a legitimate context, breaks working
code** — F-245's "add `P_OE`" remedy must never be applied to a cog-DAC configuration.

### EF-056 · DDS/Goertzel works and is sharply frequency-selective; with a discrete `XINIT`/`WAITXFI`/`GETXACC` sequence the reads are RUNNING TOTALS — `CONFIRMED`
The mode detects, and it always did. *How proven:* an independent tone — smart-pin NCO
(`P_NCO_FREQ | P_OE`) on P0 producing a real 1 MHz square wave from cog 0, sharing no NCO with the
detector — read through the jumper on P1 by DDS/Goertzel in a launched cog. **Every row measures its
own ADC bitstream density before its Goertzel run**, so no row can misreport its own input.
*Result:* on-target 1 MHz detector, density 1020/2000 → magnitude **1,059,000**; 2× detuned → 2,575;
0.5× detuned → 286; no tone → 430. Densities identical across the three tone rows, so the only
variable is detector frequency: **selectivity 411:1, 3,700:1, and a 2,460:1 null.** *Date/rig:*
2026-08-14, real P2 (Stephen). [M — taken after the EF-057 fix.] **The protocol, which is the
finding:** with this discrete sequence a *fresh cog's first read equalled the previous cog's last
read* (five times, across `COGINIT`), and *two identical commands returned exactly twice one
command's total*. Absolute reads did not track the input; the difference across one command did.
**So read before the command, read after, and take the difference.** *Explicitly NOT established —
do not assert it:* that the accumulators are never zeroed. That over-reaches from one tested pattern,
and Chip's shipped `XCONT`-loop demo is evidence against it — his per-command reads plot a live
position and do not ramp without bound. Which of `XINIT` vs `XCONT`, the wait, or the cog lifecycle
accounts for the difference is **unknown**. *Grounds:* F-260, F-265 (the ADC pin is **raw** —
`P_ADC_x`, smart-pin mode `%00000`, no DIR). *Source:* `.../tests/test-f260-goertzel-input.spin2`.

### EF-057 · `DEBUG_COGS` defaults to ALL EIGHT cogs, and the debug interrupt corrupts streamer measurements — `CONFIRMED`
Debugging with `-d` — the normal way to debug — places the P2's **highest-priority interrupt inside
the cog running your streamer**, by default. *How proven:* not a question we set out to ask; our probe
crashed into the single-step debugger's memory dump. The `CogN INIT …` lines in every log were the
debugger announcing cog starts — direct evidence it was live inside the launched cogs. *Result:* with
the default mask the Goertzel accumulators read **1,000,000–7,000,000 of pure corruption**; setting
**`DEBUG_COGS = %0000_0001`** (report from cog 0 only) stopped the crash, made the launched cogs'
`INIT` lines disappear, and collapsed the accumulators to their true values **in the hundreds**.
**Every streamer measurement taken before this fix was confounded** — which is what the `[M-pre]`
grade on the entries above records. *Date/rig:* 2026-08-14, real P2 (Stephen). [M] *Grounds:* F-266.
`p2kbArchDebugInterrupt` already carries the limitation (*"Debug can disrupt streamer operations"*)
but nothing surfaces it where a streamer author will meet it. *General form worth teaching:* any
hardware sequencer measured under the debugger may be perturbed by it — restrict `DEBUG_COGS` to the
reporting cog when measuring.

### EF-058 · `_RET_ CALL` never returns — it is a plain `CALL`, and execution falls out of the routine — `CONFIRMED (corroborates documented behaviour — see F-273)`
> **REFRAMED 2026-08-16 (F-273). This is NOT a hardware discovery.** Parallax documents the rule in
> two independent primary sources: `_RET_` executes the instruction and returns **only if that
> instruction did not branch** (*P2 Assembly Language Manual* 2022-11-01 condition table p.68; *P2
> Instructions v35 Rev B/C Silicon* row 410 — *"if `<inst>` is not branching then return by popping
> stack[19:0] into PC"*). `CALL` branches, so the return is suppressed **by specification**. This
> test re-observed the spec; our KB had dropped the qualifier, which is the actual defect (F-273).
> **Two corrections to what this entry originally claimed:** the `_RET_` is not "silently
> ineffective" (it behaves exactly as documented), and **"dispatch does not resume" is FALSE** — see
> the corrected reading below.

The idiom **assembles**, so the objection "you cannot combine a CALL with ret" is wrong as stated —
and the reason is documented rather than mysterious: the prefix returns only on a non-branching
instruction. *How proven:* a
**differential** test, not an absolute one — two bytecode handlers doing identical work, differing
only in where the return lives (`$01` = `_ret_ call #helper`; `$04` = `call #helper` / `ret`, the
reference), both in the same cog and the same run. Handlers append tokens to a **trail**, so execution
*order* is readable rather than just a count. The reference arm runs first, so a dispatch failure
reports the idiom untested rather than disproven. **Control that must fail:** a handler deliberately
leaving XBYTE — its trail stopped at the break, exactly as required. *Result:* reference = 5 steps
(`h_plain → h_callret → helper → h_plain → h_halt`, correct); under test = **7 steps**
(`h_plain → h_retcall → helper → h_callret → helper → h_plain → h_halt`) — and **`$04` is not in that
bytecode stream**: `h_callret` ran because control fell into it. **Dispatch was not lost.** The test
stream was `$00 $01 $00 $03`, and all four bytecodes dispatched — steps 6 and 7 are the third and
fourth. The spurious handler ran to completion and **its** `ret` performed the return to `$1FF`, so
the VM finished normally having executed an entire handler it was never told to. **The failure mode
is silent EXTRA EXECUTION, not a hang**, and what runs is whatever the assembler placed after the
routine — so the damage is layout-dependent. The helper reported the pushed return
address as **`$8000_001A`**, and the map places `H_CALLRET` at cog `$01A`, the instruction immediately
after the `_ret_ call`; the reference pushed `$8000_001F`, its own `ret`. **Both forms pushed "next
instruction."** The compiler is not at fault: `_ret_ call #tgt` emits `$0DB00008` with `EEEE=%0000`
(the `_RET_` condition genuinely present) versus `$FDB00004`/`EEEE=%1111` for a plain call.
*Date/rig:* 2026-08-14, real P2 (Stephen). [M-pre — but a differential in one run: a confound acting
on both arms equally cannot manufacture a 7-vs-5 trail difference, and the result is self-consistent
three ways (trail, return address vs map, compiler encoding).] *Grounds:* F-256 — the XBYTE Guide's
`:879` claim and every use of the idiom (`:416`, `:793`, `:1391`, `:1400`); §15.3 needs
**restructuring**, not a patch. *The failure is silent and misleading:* the next handler in cog memory
executes spuriously, which a reader would hunt in their VM logic for days. *Source:*
`.../tests/test-f256-retcall-xbyte.spin2`.

### EF-059 · `adc_pin<<17` in `X_1ADC8_0P_1DAC8_WFBYTE` changes the streamer MODE — the byte-count signature proves it — `CONFIRMED`
That mode's template is `%1111_DDDD_W000_0010`: `D[22:20]` are fixed zeros, **there is no pin field**,
and the ADC channel is selected by `S[1:0]`. So `adc_pin<<17` lands inside `D[19:16]` and the `add`
carries, silently selecting a *different* streamer mode. *How proven:* nothing analog required — the
three candidate modes write 1, 2 and 4 bytes per NCO rollover, so the byte count reads out which mode
the silicon actually ran. A hub buffer pre-filled with a sentinel; the guide's line run verbatim at
three pin values; highest modified byte read back. *Result:* `adc_pin`=0 → `$F082_0400` → **1,024
bytes** (correct, 1-ADC8→WFBYTE); =1 → `$F084_0400` → **2,048** (2-ADC8→WFWORD); =2 → `$F086_0400` →
**4,096** (4-ADC8→WFLONG); corrected form → 1,024. Reproduced four times, hitting the a-priori
prediction exactly. *Date/rig:* 2026-08-14, real P2 (Stephen). [M-pre — this one *does* use the
streamer, so the grade is honest; but debug interference produces jitter and dropped samples and
cannot convert one byte per rollover into *exactly* two or *exactly* four — the write width is set by
the mode field. A confirming run is cheap insurance rather than an open question.] *Grounds:* F-260
sibling at `streamer-body.md:607` — the line is correct **only** for `adc_pin = 0` and never selects
the channel at all. *The defect is invisible in testing:* the capture "works", the buffer fills, and
the data is simply the wrong shape.

### EF-060 · Inside a Spin2 object, `##hubsymbol` in a `DAT` block resolves against `$400`, not the object's load address — `CONFIRMED`
A PASM fragment that is correct in a standalone file reads **interpreter memory** when pasted into a
Spin2 object. *How proven:* surfaced while getting the EF-058 rig working — compare the address Spin2
reports for a `DAT` symbol against the one PASM sees via `##`. *Result:* `@disp` = **`$1AF9`** from
Spin2 versus `##disp` = **`$0651`** from PASM — differing by **5,288 bytes**; the `##` form returned
garbage. In a **standalone PASM** file the precondition holds and `##hubsym` is correct. *Date/rig:*
2026-08-14, real P2 (Stephen). [M-pre — streamer-free.] *Grounds:* no F-number yet; this bites anyone
who copies a PASM fragment out of a guide into a Spin2 object, which is how most P2 code is written,
and our guides present standalone-PASM fragments without saying so. *Workaround:* pass hub addresses
in from Spin2 with `@`, or use PTRA.

---

### EF-062 · Streamer digital pin output through `X_PINS_ON` **requires `DIRH`** — the streamer feeds the pin's output STATE, not its output ENABLE — `CONFIRMED`
`X_PINS_ON` (`D[23]=1`) enables the streamer's contribution to the pin's **OUT** side; the pin still
does not drive until **DIR** is high. *How proven:* one streamer command, run twice, differing only
in whether the pin was enabled first — and the DIR-high leg started from `OUT`=0, so a pass proves
the streamer overrode `OUT` rather than the `OUT` bit doing the work. Bracketed by a plain-drive
control (no streamer at all) and by a digital continuity check on the jumper. *Result:* `D1` plain
pin drive **8 of 8** · `D2` streamer with DIR low **4 of 8** · `D3` same command with `DIRH`
**8 of 8**. The `4 of 8` is a *constant* readback scored against an alternating expectation — an
undriven pin, not a partly-working one. *Date/rig:* 2026-08-20, real P2 (Stephen); jumper P0→P1,
continuity certified digitally first (both legs, with a defined open-circuit answer — see EF-063's
rig note). [M — **caveat retired 2026-08-20 by VO-J-004**, which ran this identical measurement
twice in one program: leg A in cog 0 with the debug interrupt live, leg B in a launched debug-free
cog. Every digital count matched exactly (`D1` 8/8 & 8/8, `D2` 4/8 & 4/8, `D3` 8/8 & 8/8) and the
analog legs agreed in verdict. The debug interrupt did not change any answer here, and this is also
the confirming second run — no longer single-run.] *Grounds:* **F-308** — corrects the Streamer
Guide's §11.0 callout at `streamer-body.md:834`, *"Ordinary pin output through `X_PINS_ON` drives the
pin bus directly and requires no `WRPIN` and no `DIRH`"*, and the note repeating it at
`P2KB-CORRECTION-FINDINGS.md:251`. **The "no `WRPIN`" half is correct and stands** — digital output
needs no smart-pin mode, no DAC mode, no COGID, no channel. Only "no `DIRH`" is wrong. This matches
the Silicon Doc v35 read straight: streamer pin data is OR'd *"with {OUTB, OUTA} to produce the final
64 pin output states"*, while *"an I/O pin's output enable is controlled by its DIR bit"*. The
prediction was recorded in the program before the run, with the falsifying outcome named — the bench
was free to reverse F-308 and did not. *Source:*
`campaigns/2026-08-manual-corrections/tests/test-f272-streamer-dac-tt.spin2`.

### EF-063 · A **streamer-fed** DAC needs `%TT = %01` (`P_CHANNEL`); at `%TT = %00` the pin ignores the streamer and holds its own level field — `CONFIRMED`
Closes the one arm EF-054 and EF-055 did not cover: both are graded `[M-pre — streamer-free]`, having
swept `%TT` with the streamer uninvolved. *How proven:* a DAC on P0 jumpered to a smart-pin ADC on
P1, driven full-scale then zero-scale, reading the HI−LO spread; the same routing
(`X_DACS_X_X_X_0`) and the same streamer immediate at both `%TT` values, against a level-driven
control that uses no streamer at all. *Result:* control `C` (level-driven DAC, `TT=%00`) spread
**5,331** · `T0` streamer-fed at `TT=%00` spread **1** · `T1` streamer-fed with `P_CHANNEL` spread
**5,330**. `T1` tracks the control to within one count; `T0` is flat. *Mechanistically consistent
with EF-055*, which found `TT=%01` switches the DAC's **source**: at `%00` the pin takes its own
`M[7:0]` level (here the COGID, so a constant), and only at `%01` does it take the cog DAC channel
the streamer is feeding. *Date/rig:* 2026-08-20, real P2 (Stephen). [M — **confirmed twice**; see EF-062's
grade note. VO-J-004's second run read `C` 5,330 / `T0` 1 / `T1` 5,328 in cog 0 and `C` 5,331 /
`T0` 1 / `T1` 5,331 in a debug-free cog — same verdict both ways, and matching the first run's
5,331 / 1 / 5,330.] *Rig note worth keeping:* the jumper is certified **digitally, both legs, before
anything analog** — the far pin holds the net through a 15 kΩ drive while the near pin drives it
hard, so an open circuit reads the *opposite* value instead of an undefined float (a released P2 pin
holds its last state on pin capacitance long enough to read back as a false pass). *Grounds:*
**F-272**, which reached the same answer from documentary sources and is already `RESOLVED`; this is
the empirical seal, not a change of answer. *Source:*
`campaigns/2026-08-manual-corrections/tests/test-f272-streamer-dac-tt.spin2`.

### EF-064 · Streamer pin placement is **mode-dependent**, and the `DIRx/DRVx` pin-span form works as documented — `CONFIRMED`
Two facts one probe settled. (a) A **1-pin** mode reaches **any** pin: `X_IMM_32X1_1DAC1` at pin 20
drove P20 and nothing else, so its pin field spans `D[22:17]`. An **8-pin** mode takes a **window**:
`X_IMM_4X8_1DAC8` at base 16 drove exactly P16–P23, its group coming from `D[22:20]` in 8-pin steps,
with `D[19:17]` serving as DAC-configuration rather than pin bits. (b) `DRVH` over a pin span —
`#(count-1)<<6 + base`, the `+D[10:6]` form — drove exactly P16–P23 and nothing adjacent.
*How proven:* a **canvas** — P8..P31 held at a 15 kΩ low with `DIR` high, so an undriven pin reads 0
for a stated reason instead of floating, while any driven pin overpowers the pull and reads 1; the
readback is then a map of which pins were driven. Every canvas pin was certified free *weakly*
before anything drove hard. The no-streamer span test is the control the streamer tests depend on
and cannot prove for themselves. *Result:* canvas `$0000_0000` (all 24 pins free) · span `$0000_FF00`
· 8-pin mode base 16 `$0000_FF00` · 1-pin mode pin 20 `$0000_1000`. Masks are `pinread(P8..P31)`,
bit 0 = P8. *Date/rig:* 2026-08-20, real P2 (Stephen). [M — measured in a launched debug-free cog.]
*Grounds:* **confirms the Streamer Guide's Chapter 12 as written** — §12.1 (group field `D[22:20]`)
and §12.2 (sub-pin `D[19:17]`, and its statement that as the pin count rises those bits become
DAC-config bits) are correct and now empirically backed. It also dissolves an apparent conflict
between the Silicon Doc's *"%ppp in D[22:20] … in 8-pin increments"* and the manual's `pin<<17`
idiom: they never disagreed, the field is mode-dependent. *Source:*
`campaigns/2026-08-manual-corrections/tests/test-f308-cog-and-pingroup.spin2`.

### EF-065 · Composing an **unaligned** pin base with `+` in a multi-pin streamer mode silently selects a **different mode at a different pin group** — `CONFIRMED`
`X_IMM_4X8_1DAC8 + X_PINS_ON + 20<<17` assembles to `$60B6_FFFF`, not the intended
`$60AE_FFFF`: `20<<17` sets bit 19, `D[19:16]` already holds the mode template `%1110`, and the `+`
**carries** — leaving `D[19:16] = %0110` (`X_IMM_4X8_4DAC2`, a different mode) and `D[22:20] = %011`
(the P24–P31 window, not P16–P23). *How proven:* run it against the EF-064 canvas and read which
pins moved. *Result:* **`$00FF_0000` — P24..P31**, exactly the predicted wrong answer; the aligned
control drove P16–P23 in the same run. *Date/rig:* 2026-08-20, real P2 (Stephen). [M]
*The `|` form fails differently and worse:* `| 20<<17` sets a bit the template already sets, so the
word comes out **byte-identical** to base 16 — an unaligned base composed with `|` does not carry,
it silently *vanishes*. Neither form errors, and the compiler cannot see either. **This was caught
by reading the assembled constant out of the compiler listing before the run, not by the bench** —
the first draft of the test would have compared two identical command words and called it a result.
*Grounds:* **F-309** — the Streamer Guide's §12.0 caution covered the fewer-than-8-pin modes and
DDS/Goertzel but stopped short of **8 pins and wider**, where `D[19:17]` holds no pin bits at all and
the operand must therefore be a multiple of 8. Extended 2026-08-20. **The book's `pin` naming is
correct and was not changed** — §12.0 explains that `pin<<17` splits a plain pin number into
`pin>>3` (group) and `pin&7` (sub-pin), which is exactly what those fields expect. This is
**EF-059's failure in a second mode family** — there `adc_pin<<17` changed the mode of
`X_1ADC8_0P_1DAC8_WFBYTE` and the defect was invisible in testing because the capture still "worked".
*Source:* `campaigns/2026-08-manual-corrections/tests/test-f308-cog-and-pingroup.spin2`.

---

## P2 errata predictions (silicon — 2026-09 campaign, VO-J-007..011)

Five predicted silicon defects from an HDL-reading study, each decided by a test written from the
prediction alone and run on real P2 silicon. **All five held.** Two had been published by the vendor
(EF-066, EF-067) and are grounded on silicon here for the first time; **three had never been observed
on a part** (EF-068, EF-069, EF-070). Every test measures in a launched PASM cog with the debugger
kept out of it (`DEBUG_COGS = %0000_0001`, EF-057), gates its verdict on in-run controls, and fixed
both outcomes in the program before the run. Each verdict below was re-derived from the raw log
lines, not taken from the program's own `VERDICT` line. *Rig for all five:* bare P2 board, 200 MHz,
`pnut-ts` 1.55.8 `-d`, RAM download with reset, 2026-09-24 (Stephen). **Run twice**, from two builds
(as authored, then style-conformed with identical measuring engines): every measured value matched.
Each is N=1 real silicon; all five are structural yes/no behaviours, so one part is dispositive.
Campaign: `campaigns/2026-09-p2-errata-predictions/`.

### EF-066 · An `ALTx` with an immediate `#S` between `AUGS` and its target is itself augmented, and the target still gets the augment — `CONFIRMED`
The pending `AUGS` value fills bits 31:9 of the intervening `ALTx`'s own `S` and is **not** cancelled,
so the intended target receives it as well. **Where the damage lands:** an `ALTx` takes its base from
`S[8:0]` and its auto-increment from `S[17:9]`. The augment leaves `S[8:0]` alone, so the substituted
register is the one aimed at. What changes is the **auto-increment**, now taken from the `AUGS` value,
which silently moves the `ALTx`'s D register. *How proven:* `test-o1-altx-imm-s-steals-augs` —
`AUGS #$3C5C0A55` (`S[17:9]` = 5) then an immediate-`S` `ALTx` then `MOV 0-0,#$55`, against a
sentinel-filled register window; three passes in fresh cogs. *Result:* **A6** `ALTD idx,#0` →
`win[8]=$3C5C_0A55 dIdx=5` · **A7** `ALTR idx,#3` → `win[11]=$3C5C_0A55 dIdx=5`. Controls exact:
bare `MOV` `$0000_0055`; `AUGS`+`MOV` `$3C5C_0A55`; `ALTD` with a register `S` of `$A00` → `dIdx=5`
(the same auto-increment path, driven deliberately). **Workaround proven:** a register `S` on the
`ALTx` (**A5**) → `win[12]=$3C5C_0A55 dIdx=0`. **`AUGD` survives an intervening immediate-`S`
`ALTx`:** `AUGD` / `ALTS idxs,#0` / `WRLONG #$13C` wrote `$1357_9B3C` with `idxs` unchanged
(`$61`→`$61`). An `ALTx` has no immediate-`D` form, so it cannot consume a pending `AUGD`. One `ALTx`
variant was tested for this half. All 3 passes bit-identical. *Grounds:* `pasm2/augs.yaml`
`intervening_altx_immediate_s_consumes_augs` — the erratum, its workaround, where the effect lands, and
the `AUGD` half of its `scope_note`. *Source:* `…/tests/test-o1-altx-imm-s-steals-augs.spin2`.

### EF-067 · `SETQ`/`SETQ2` then `ALTD` then a block `RDLONG`/`WRLONG` with a `PTRx` update: the whole block moves, but `PTRx` takes the ordinary expression's step — `CONFIRMED`
The block transfer is unaffected — every long lands at the `ALTD`-redirected destination — but the
pointer update ignores the block size and applies the **plain `PTRx` expression's own step**. That is
+4 for `ptra++`, but **+12 for `ptra++[3]`**: the step is not "one long", it is whatever the
expression would do without `SETQ`. *How proven:* `test-o17-setq-altd-block-ptr-delta` — 15 arms ×
4 interleaved rounds; destination and a trap region pre-filled with `$5E5E_5E5E`; source long *k* =
`$A5A0_0000+k`. *Result (every round identical; trap region untouched in every arm):*

| Arm | Control Δ (no `ALTD`) | Hazard Δ (with `ALTD`) | Data |
|---|---|---|---|
| `setq #3` + `rdlong …, ptra++` | +16 | **+4** | 4/4 at the `ALTD` destination |
| `setq #7` + `rdlong …, ptra++` | +32 | **+4** | 8/8 |
| `setq #3` + `rdlong …, ptra++[3]` | +16 | **+12** | 4/4 |
| `setq #3` + `rdlong …, ptrb++` | +16 | **+4** | 4/4 |
| `setq #3` + `wrlong …, ptra++` | +16 | **+4** | 4/4 |
| `setq2 #3` + `rdlong` (LUT) `…, ptra++` | +16 | **+4** | 4/4 |

Controls also exact: plain `rdlong ptra++` +4, `ALTD` alone +4, plain `ptra++[3]` +12. **Workaround
proven:** keep `SETQ` adjacent to the transfer (the control column). Only `ALTD` was tested as the
intervening instruction; `AUGS`/`AUGD` and the other `ALTx` are named by the vendor, not tested here.
*Grounds:* `pasm2/setq.yaml` `block_transfer_ptrx_delta` (its "+4 for one long" is only the `[1]`
case), `concepts/setq_block_ops.yaml`, `pasm2/augs.yaml`; the Assembly Reference's Appendix J.
*Source:* `…/tests/test-o17-setq-altd-block-ptr-delta.spin2`.

### EF-068 · `GETCT WC` in a group of four cogs that had no running cog when the low `CT` long wrapped returns a **stale upper long** — `CONFIRMED` (new; not in any vendor source)
Cogs 0–3 and 4–7 each read their own copy of the 64-bit counter. A group's copy of the **upper** long
advances only at a wrap of the lower long **while at least one cog of that group is running**; the
lower long is always current. A cog started in a group that missed wraps reads an upper long **behind
by one per missed wrap**, until its group runs through the next wrap. From reset only cog 0 runs, so a
program whose first cog in 4–7 starts after the first wrap (2³² clocks — **21.5 s at 200 MHz**) gets a
wrong 64-bit time from that cog. *How proven:* `test-o18-getct-upper-stale-runA` / `-runB` — cog 0
brackets each sampler read with its own `GETCT WC`/`GETCT` pair (10 valid pairs per reading, all lower
longs between `$1000_0000` and `$F000_0000`); D = cog 0's upper long minus the sampler's. *Result:*
**Run A** (cog 4 first started after wrap 1): **D = 1** at hi=1, early and late (sampler reads
`$0000_0000_$1020_D8B3` beside cog 0's `$0000_0001_…`, lower long current); **D = 0** at hi=2 (its
group ran through the wrap); cog 4 then stopped and restarted after two missed wraps → **D = 2**
(sampler `$0000_0002_…` beside `$0000_0004_…`). **Run B** (cog 4 running from the start — the
workaround): **D = 0** at hi=0, 1 and 2. **Control:** cog 1 (group 0) **D = 0** in every reading of
both runs; running-cog mask and lower-long bracket held throughout. **Workaround proven:** keep a cog
of each group in use running from before the first wrap. *Grounds:* `pasm2/getct.yaml` — a new
`silicon_errata` entry. *Source:* `…/tests/test-o18-getct-upper-stale-runA.spin2`, `…-runB.spin2`.

### EF-069 · `GETXACC` does not clear the Goertzel accumulators unless the streamer is running in Goertzel mode; mid-burst, it neither drops nor double-counts a term — `CONFIRMED` (new; contradicts `getxacc.yaml`)
**Idle, or in any other streamer mode, `GETXACC` clears nothing:** it returns the live accumulator and
leaves it as it was, so repeated reads — including across a new non-Goertzel streamer command — return
the same value, and the accumulator keeps growing from burst to burst. **During a Goertzel burst** the
clear does act, and exactly partitions the burst: the read plus the next read sum to what one unread
burst gives. *How proven:* `test-so80-getxacc-clear-gating` — one engine cog drives P3 low (no jumper),
every LUT long `$173D_0000` so each active clock adds C = ±61 (sine ±23); 8 reps, each from a
measured baseline B. *Result:* **Half A** — `GETXACC` idle (G1), as the next instruction after
`XINIT` of a non-Goertzel mode `$4000_0400` (G2), ~100 clocks into it (G2L), and after it (G3):
**50 of 50 reads equal B bit-for-bit** (e.g. rep 0: B = G1 = G2 = G2L = G3 = 488). B itself grows
across reps (488 → 14,335) with no clear between them. **Half B** — rep 0: unread 256-clock burst
dA = 15,555 = **255 × 61**; with one read inside, R1 − P = 1,769 = **29 × 61**, then R2 = 13,786 =
**226 × 61**; 29 + 226 = 255, so **dd = 0**. All 8 reps dd = 0 as the read point moved from clock 29
to 189 (k1 = waitx − 1 every time). Controls: CAL sign flips with P3 (+3,843 / −3,843 = ±63 × 61),
LUT, streamer-finished flag and P3 level all held. *Grounds:* **`pasm2/getxacc.yaml` is wrong** where
it says `GETXACC` captures into holding registers and **clears** them and that values hold "until a new
streamer command executes" — idle reads never clear, and a new streamer command does not reset the
value either. Its read-before-and-after, take-the-difference rule is exactly what this behaviour
requires. *Source:* `…/tests/test-so80-getxacc-clear-gating.spin2`.

### EF-070 · The Goertzel accumulators trail their term by one active clock: a burst's last term lands in the **next** Goertzel burst — `CONFIRMED` (new)
A reading taken after a burst of N clocks holds **N − 1** terms; the last one waits in an internal
register no instruction reads, and is added on the first active clock of the next Goertzel burst.
Waiting does not deliver it. **Workaround proven:** follow each burst with a short zero-term burst
(same mode, input enables `imm[15:12]` clear) before reading — the reading then holds all N terms and
nothing spills into the next burst. *How proven:* `test-so84-goertzel-last-term-lag` — P3 driven by
the engine cog, every LUT long `$2513_0000` (C = ±19, sine ±37); N = 64 and 65, P3 low and high,
4 reps each = 16 sequences. *Result:* every sequence reads **d1 = (N−1)·C** after the burst (N=64,
C=−19: −1,197), **R1b − R1 = 0** 1,000 clocks later, and **d2 = C** after the zero burst (−19); the
carry arm reads (N−1)C, then **N·C** (carrying the stranded term), then C. 16 of 16; sign flips with
P3; the sine channel shows the same pattern with |C| = 37. Controls: measured C = −19 ×4 / +19 ×4,
every delta a whole multiple of 19, zero-after-zero moves 0. *Grounds:* `pasm2/getxacc.yaml` — a new
`silicon_errata` entry. *Source:* `…/tests/test-so84-goertzel-last-term-lag.spin2`.

---

## P2 errata — second bench session (silicon, 2026-09-25, VO-J-012..014)

Three tests built after the first five: the `RDFAST`/`WRFAST` readiness boundary (VO-J-012), Chip
Gracey's Goertzel SINC2 iteration-count report (VO-J-013), and the study's sixth prediction, the
DAC-mode ADC enable (VO-J-014). Same house rig as EF-066..070: measurement in a launched PASM cog,
`DEBUG_COGS = %0000_0001` (EF-057), verdicts gated on in-run controls, outcomes fixed in the program
before the run, every verdict **re-derived here from the raw log lines**. *Rig:* **Rev C** P2 on
Stephen's bench board (free pins P0–P7, P32–P47 only), 200 MHz, `pnut-ts` 1.55.8 `-d`, RAM download
with reset, 2026-09-25. **Run twice, same builds** (21:40 and 21:49 local log stamps): RDFAST's 1,496
report lines are identical; SO9 is identical except the running ADC's C2 toggle counts; SINC2 is
identical in every arm except the two deliberately jittered arms (JIT-S1/S2) and the verdict lines
quoting them. Campaign: `campaigns/2026-09-p2-errata-predictions/`.

### EF-071 · In a DAC smart-pin mode, `OUT` does not switch the ADC while `TT` bit 0 is clear — `CONFIRMED` (new; contradicts the published `%TT` table)
The P2 Documentation's `%TT` table (`p2-documentation.txt:7652-7657`) publishes, for every smart mode,
"x0 = output disabled, regardless of DIR", and for the DAC smart modes (`%SSSSS` = `%00001..%00011`)
"0x = OUT enables ADC in DAC_MODE". On silicon, with `TT` = `%00` raising `OUT` runs **nothing**: the
pin's read state stays exactly as with `OUT` low. With `TT` = `%01` (output enabled), `OUT` runs the
ADC, and the fast DAC drives the pin while it does. *How proven:* `test-so9-dac-mode-adc-enable` — P4
in DAC-noise mode (`$0014_0002` TT=`%00` / `$0014_0042` TT=`%01`), P5 configured `$7000_0000` (A input
= relative −1 pin, DIR low) so P4's read state is `INA` bit 5; one sample = 4,096 `INA` reads counting
bit 5; four conditions × 5 rounds. *Result (run 1 / run 2):* **C1** TT=`%01` OUT low: 0 every sample ·
**C2** TT=`%01` OUT high: 1,963–2,093 / 1,958–2,017 (the ADC's decisions toggling) · **C3** TT=`%00`
OUT low: 0 · **C4** TT=`%00` OUT high: **0 every sample**. C2 separates from C1 (the reading sees the
ADC); C4 does not separate from C3 and does separate from C2 — the pre-registered CONFIRMED pattern,
both runs. Controls: the P4→P5 plain-pin path read 4,096 high / 0 low before and after the rounds; all
three words decoded to the published fields and equal their Spin2 symbol compositions.
**Workaround proven:** set `TT` bit 0 and accept the fast DAC driving the pin (C2). Of the `TT`
settings, only `%00` and `%01` were tested; the `OTHER`-enable forms (`TT` = `%1x`) were not. *Also measured:* with the ADC off (C1, C3) the
read state is 0 in every sample. **Classification: silicon erratum** (a published statement
contradicted on silicon) → **P2 Errata E6**. *Grounds:* the KB's smart-pin `%TT` coverage needs a
`silicon_errata` entry (to register). *Source:* `…/tests/test-so9-dac-mode-adc-enable.spin2`.

### EF-072 · Chip Gracey's Goertzel SINC2 corruption reproduces value for value from the accumulator structure (SINC2's running first stage across unequal windows); his two workarounds hold — `CONFIRMED` (heading and classification corrected 2026-09-26: see *Correction* below)
Chip's 2024-12-16 report (`ingestion/external-inputs/forum-threads/ProblemGoertzelSINC2mode/INGEST.md`):
in SINC2 mode a non-power-of-two iteration count makes `GETXACC` "off by one double integration",
corrupting that sample and the next. Measured, and **explained value for value** by EF-070's carry:
the term held on a window's last clock is added on the next window's first, and in SINC2 that held
value is the first-stage integral J, so a window one clock longer or shorter than usual moves J
between two adjacent samples. *How proven:* `test-goertzel-sinc2-iteration-count` — P3 driven as the
Goertzel input (constant term C_X = ±1, C_Y = ±3 by P3 level), 14 arms of XCONT/XZERO streams with
power-of-two, non-power-of-two (2^23±64), 1 MHz (100 cycles) and 25,000-cycle windows, SINC1 and
SINC2 twins, and a `WAITX #1 WC` read-jitter pair. *Result:* **Q1** power-of-two SINC2: 0 of 1,020
samples off; non-power-of-two: every odd-length window corrupts that sample and the next, then clean
— NPS-S2 30 outliers in 15 pairs, NPL-S2 30 in 15, CHP-S2 12 in 6 (max |e| 1,968,115 / 1,966,097 /
36,619,996); no outlier without a window change, no window change without an outlier. **Q2** SINC1:
every sample = C × (clocks in its window); an odd window is off by exactly one term. **Q3** one clock
of read jitter: SINC2 75 % of samples off by ≥ 1,000 terms (max 4,124,674 / 4,149,250), SINC1 off by
at most one term — Chip's "huge noise" reproduced. **Q4** XZERO kept one window length and an
unchanging SINC2 sample at 10.24 µs, 100 µs and 25 ms windows, where the XCONT twins varied and
corrupted. **Q5 mechanism:** the carry model, J fitted once at k = 3 and then predicted from measured
window lengths alone, equals **every** sample — all 829 / 834 outliers and every clean sample — in
the four decisive arms. Worked pair (NPS-S2, k = 65/66): a 2,047-clock window gives e = −133,121 then
+131,073, sum −2,048, exactly the model. Controls: LUT readback 0 of 512 differ; CAL C sign flips
with P3 and C_Y = 3·C_X; the power-of-two loop locked at 2,048 clocks per window, g = 0.
**Classification:** not a new erratum. Chip's workarounds hold: a power-of-two iteration count, or XZERO.
**Correction (2026-09-26):** this entry first classified the corruption as "EF-070 (E5) seen in SINC2".
The rig's own model section (`test-goertzel-sinc2-iteration-count.spin2` header, "What the one-clock lag
itself contributes cannot be isolated in a continuous stream: it shifts every J by one C, which the fit
absorbs") does not support that: the same corrupted pairs follow from SINC2's first-stage running
integral crossing reading windows of unequal length, with or without the lag. And the behaviour is
**published** — the P2 Documentation's *NOTE ABOUT GOERTZEL SINC2 MODE (2024.12.16)*
(`silicon-doc-text.txt:1703-1704`) states that a varying iteration count "will corrupt the current and
next samples". Documented behaviour, confirmed on silicon: **not an erratum, and not part of E5**. P2
Errata E5 carries it only as a scope note (its SINC1 fix does not cover SINC2). Where it belongs, if
anywhere beyond the P2 Documentation: P2 Anti-Patterns.
**Scope note (study reading, untested):** in SINC2 the E5 zero-burst workaround does not flush the
first stage. *Grounds:* `pasm2/getxacc.yaml` `sinc2_constraint` (F-469 already open on its citation)
— now also its mechanism, citing this entry. *Source:*
`…/tests/test-goertzel-sinc2-iteration-count.spin2`.

### EF-073 · `RDFAST` readiness: a blocking `RDFAST` keeps its promise; a no-wait `RDFAST` needs 8–15 clocks, and a read before that returns zero — `CONFIRMED` (blocking) / measured (no-wait)
The P2 Documentation promises a **blocking** `RDFAST` (`D[31]` = 0) "will additionally wait until the
FIFO has begun receiving hub data, so that it can start being used in the next instruction"; for
**no-wait** (`D[31]` = 1) "your code must allow a sufficient number of clocks before any attempt is
made to read or write FIFO data" — a requirement with no number and no stated consequence.
*How proven:* `test-rdfast-wrfast-readiness-boundary` — every arm swept over all 8 hub slices × 8
phases (a whole egg-beater rotation, confirmed: 8 distinct `RDFAST` durations per slice) × 16 trials,
no-wait distances 2..44 clocks; six gating controls (clock arithmetic, `RDLONG` pattern, stale
priming, late no-wait read, blocking and late `WRFAST`) all correct in every trial.
*Result:* **Blocking read — the promise holds:** 3,072 of 3,072 next-instruction reads (`RFLONG`,
`RFWORD`, `RFBYTE`) returned the new first datum with consistent C/Z; `RDFAST` took **10–17 clocks**,
exactly the v35 instruction table. **No-wait read — the boundary:** the first all-correct distance is
8..15 clocks depending on hub alignment, the same range in every slice; **safe from 15 clocks** (=
`WAITX #11` after the no-wait `RDFAST`); no non-monotonic cell. **A read too early returns ZERO** —
all 8,704 wrong reads of 43,008, never stale data (the rig had predicted stale and pre-listed zero as
refuting that detail), with C/Z consistent with the zero and no stall. **No-wait write:** **no unsafe
distance observed** — 0 of 43,008 writes dropped, skipped or wrong from 2 clocks on, every slice.
**Re-arming (E_RENW):** a second no-wait `RDFAST` issued while the first is still arming wins — the
new data read in 43,008 of 43,008. **Classification:** the no-wait hazard is an **anti-pattern**
(documented requirement, undocumented number and consequence) → **P2 Anti-Patterns**, with the
measured 15-clock rule. Chip's mitigation ("allow enough clock cycles", SOURCE-ERRATA E-015) now has
its number. *Grounds:* `pasm2/rdfast.yaml` — the measured no-wait boundary and the zero read.
*Source:* `…/tests/test-rdfast-wrfast-readiness-boundary.spin2`.

### EF-074 · A blocking `RDFAST` issued while a no-wait `RDFAST` is still arming can skip its wait, and the next read returns zero — `CONFIRMED` (new; breaks the blocking promise)
The same test's E_REBLK arm: `rdfast $8000_0000,mid` (no-wait) · `waitx` gap · `rdfast #0,new`
(**blocking**) · `rflong` in the next instruction. The blocking promise quoted in EF-073 is unqualified.
*Result (identical in both runs):* in each of the 64 slice × phase cells, **exactly one gap fails, in
all 16 trials**, and at that gap the blocking `RDFAST` takes **2 clocks** — it does not wait — and the
next `RFLONG` returns **`$0000_0000`** (never the first `RDFAST`'s data, never stale). 1,024 of 43,008
reads. The failing gap moves with hub phase and falls on each of 8..15 clocks exactly eight times — the
same 8..15-clock window as EF-073's no-wait arming boundary: the blocking `RDFAST` is fooled when it is
issued at the moment the earlier no-wait fill begins arriving. On either side of the failing gap it
waits as usual (in slice 0, start 0: 12, 11… one clock earlier and the full 17 one clock later; the
value one clock later varies with alignment — slice 1, start 0 waits 10, log line 1369; corrected
2026-09-26, the earlier wording generalised slice 0). Every other gap, 41,984 reads, correct. Gated on the same six
controls as EF-073. **Classification: silicon erratum** (the published blocking promise is broken
on silicon) → **P2 Errata E7**, pending the chapter's own reproducer. This is plausibly the bug Chip
Gracey confirmed without explaining (SOURCE-ERRATA E-015: "Yes, but I can't explain it well").
**Workaround measured in this arm:** issue the blocking `RDFAST` more than 15 clocks after the no-wait
one — every gap from 16 to 44 clocks read correctly in every cell. *Not tested:* the `WRFAST` twin of
this arrangement; any other fix (e.g. making the earlier `RDFAST` blocking). *Grounds:* `pasm2/rdfast.yaml` — a `silicon_errata`
entry. *Source:* `…/tests/test-rdfast-wrfast-readiness-boundary.spin2`.

---

## P2 errata — workaround tests (silicon, 2026-09-26)

Three tests that each run, **byte for byte**, the drop-in workaround P2 Errata v0.2.0 prints (a
*workaround*, never a *fix*: the defect stays and code steps around it — Stephen, 2026-09-26) (between marker
comments in the rig), and reproduce the erratum in the **same run** as a positive control — a rig that
cannot see the defect prints `RIG FAIL`, never a verdict. Same house rig as EF-066..074; same bench
board (free pins P0–P7, P32–P47 only), 200 MHz, `pnut-ts` 1.55.8 `-d`, RAM download with reset,
2026-09-26 (Stephen), **run once each**; each downloaded `.bin` size equals the rig compiled here.
Every verdict **re-derived from the raw log lines**. Structural yes/no behaviours on one part, as
EF-066..070. Campaign: `campaigns/2026-09-p2-errata-predictions/` (tests 9–11).

### EF-075 · E3's workaround holds: a keeper cog started in cog 7 as the first line of `main()` keeps cogs 4–7 reading the current 64-bit counter across wraps — `CONFIRMED`
*How proven:* `e3-fix-keeper-cog-test` — the drop-in (`KEEPER_COG = 7`, a `jmp #keeper` loop,
`coginit(KEEPER_COG, @keeper, 0)` as the first line of `main()`) at boot, then samplers started and
stopped in cogs 4, 5, 6 around it; each reading = 10 bracketed `GETCT WC`/`GETCT` pairs against cog 0;
cog 1 is the group-0 control. *Result (log `debug_260926-015546`):* boot upper long `$0000_0000`,
running cogs `%10000001` (cog 0 + keeper) (l.22). Keeper alone in 4–7: hi=0 cog 4 **D = 0** (l.35);
after wrap 1 cog 5 **D = 0** (l.75), cog 6 late **D = 0** (l.111); after wrap 2 cog 4 **D = 0**
(l.138), cog 5 late **D = 0** (l.174); every reading 10 of 10 valid pairs. **Positive control:** keeper
stopped at `$0000_0002_$E088_2186` (l.186), wrap 3 missed → cog 6 **D = 1** (l.201) — the erratum,
reproduced in the same run. Controls: cog 1 **D = 0** in all six readings; running-cog mask
`%10000011` on every poll before the stop and `%00000011` after; cog 0's upper long equal to its own
wrap count on all 55 alive lines; 0 bracket failures. **Kind:** one-time startup fix. *Limits:* a busy
`jmp` loop only (a keeper parked in `WAITX`/`WAITATN` not tested); cog 7 only; 200 MHz. *Source:*
`…/tests/e3-fix-keeper-cog-test.spin2`.

### EF-076 · E4 and E5's workaround holds: the `burst_sums` helper routine returns exactly N terms of a SINC1 Goertzel burst, whatever ran before it — `CONFIRMED`
*How proven:* `e4-e5-fix-read-sums-test` — the printed routine (zero burst built from the caller's D/S
with count 4 and `S[15:12]` = 0 to deliver any held term, idle `GETXACC`, the caller's burst,
`WAITXFI`, zero burst, idle `GETXACC`, subtract), called 10 times back to back per record with
N = 1, 2, 3, 4, 7, 64, 65, 255, 256, 1001, 3 records at P3 low and 3 at P3 high, each record's first
call following a deliberately unflushed 7-clock burst; after every call an independent idle read
1,000 clocks later. *Result (log `debug_260926-015810`):* calibration C = **±61** cosine / **±23**
sine in all 6 records (e.g. l.31: 61,000 → 64,904 → 68,869 = 64C, 65C); **60 of 60 calls returned
exactly N·C on both channels** (cosine 61 … 61,061 at P3 low, l.34–43; sine −23 … −23,023 at P3 high,
l.76–85); each record's first call began exactly one C above the reading after the unflushed burst
(l.32 RD = 77,104 → l.34 B = 77,165), every later call began at the previous call's closing reading,
and every independent read equalled start + sum — nothing held, nothing moving. **Positive control
(same run, all 12 rows):** a "clearing" `GETXACC` read idle changed nothing (P2 = R1), and a 64-clock
burst, a 65-clock burst, a zero burst and a 7-clock burst read 63C, 65C (64 of its own terms plus the
one carried in), C (the carried term alone) and 6C (l.32: 3,843 / 3,965 / 61 / 366) — E4 and E5,
reproduced. Controls: the routine's zero-burst words `$F007_0004` /
`$0008_00A5`, 0 LUT mismatches (l.29); P3 level held around every record. **Kind:** helper routine.
*Limits:* SINC1 only (SINC2: EF-072, documented, not this fix); NCO `$8000_0000`, P3 input only, cog
RAM, 200 MHz. *Source:* `…/tests/e4-e5-fix-read-sums-test.spin2`.

### EF-077 · E7's workaround holds: `WAITX #12` after the no-wait `RDFAST` (16 clocks to the blocking one) gives a correct first read in every hub alignment — `CONFIRMED`
*How proven:* `e7-fix-rdfast-spacing-test` — the printed block (`rdfast nowait,hub_first` /
`waitx #12` / `rdfast #0,hub_next` / `rflong first_long`) swept over all 8 slices × 8 phases × 16
trials, first and second read checked; beside it the unspaced sweep of EF-074 (gaps 2..44) as the
positive control. *Result (log `debug_260926-015823`):* **printed block: 1,024 of 1,024** trials read
the new first long then the next (`$A5A5_0080`, `$A5A5_0081` in s0 p0), the blocking `RDFAST` waiting
**10..17 clocks**, 8 distinct values per slice (l.484–547, 556). **Positive control reproduced:** in
all 64 cells exactly one gap in 8..15 clocks failed in 16 of 16 trials, reading zero with a 2-clock
blocking `RDFAST` — 1,024 of 43,008 reads, 8 cells at each gap 8..15, the same per-cell pattern as
EF-074 (l.355–482, 552–554); gaps 16..44: first read correct in 29,696 of 29,696, no wrong second read
(l.555). Controls: `WAITX #12` measured 16 clocks issue to issue (2 + 14) in every trial (l.94–157);
clock, plain-read, primed-FIFO and late no-wait read correct in every trial (l.549). **Kind:** rule
at each use — at least 16 clocks from the start of the no-wait `RDFAST` to the start of the blocking
one. *Limits:* only `WAITX` tested between them (no hub-stalling instructions); the `WRFAST` twin not
tested. *Source:* `…/tests/e7-fix-rdfast-spacing-test.spin2`.

**The reader copies re-run (2026-09-26, Stephen, same bench, once each).** P2 Errata ships the 12
programs as style-conformed reader copies (`manuals/p2-errata/examples-library/`, the three
workaround tests renamed `e3-/e4-e5-/e7-workaround-…`): every measuring PASM image is
byte-identical to the as-run build, cog-0 Spin2 was restyled. Each downloaded `.bin` equals a fresh
compile of the archive source. Compared line by line with the original runs (logs in
`p2-errata/audit/verification-tests/logs-archive/debug_260926-1444*…1525*`): **every analysed
value, class and verdict matched in all 12.** Differences, all by design or by nature: labels and
ids (`O17`→`Erratum E1`, `F_FIX`→`W_BLOCK`, `F1`→`W1`, `accx`→`xsum`, "FIX"→"WORKAROUND"),
absolute hub addresses (E1 `before=/after=` +$18 as predicted; E7 and E7-workaround `bases:`),
E3 counter timestamps, E6's C2 ADC toggle counts (2,041–2,113; run-to-run by nature), and the
SINC2 test's JIT-S1/JIT-S2 arms (jittered by design). **One unexplained:** SINC2 arm XZS-S2's
first sample `k=0` read x = 90,090,539 (y = 270,271,617) where both original runs read
92,185,644 (276,556,932) — a start-up sample the program excludes (`WARM = 3`); every analysed
sample of that arm matched. Recorded as an open question below.

---

## P2 errata — E3 band follow-ups (silicon, 2026-09-27, VO-J-015..017)

Three tests that decide what the E3 chapter may say about the stale window — the **band** — that
EF-068 found: whether a *waiting* cog keeps its group current, whether cogs 0–3 behave as cogs 4–7
do, and whether the band closes in one wrap from a long lag, in Spin2's `GETMS()`/`GETSEC()` as
well as `GETCT WC`. Written by the arbiter (not an independent agent), then reviewed adversarially
before the run by a fresh agent per test: no blocker (VO-J-015..017). Same house engine as
EF-068/EF-075 (sampler words `$FD701A1A`/`$FD601C1A`; D = reference upper long − sampler upper
long; a reading = 10 bracketed pairs), same bench board, 200 MHz, `pnut-ts` 1.55.8 `-d`, RAM download
with reset, 2026-09-27 (Stephen), **run once each**; each downloaded `.bin` (13,291 / 13,497 / 14,906
bytes) equals the rig compiled here, and two header-comment edits made after the run leave the
binary byte-identical (rebuilt and compared). Every verdict **re-derived from the raw pair lines**,
not from the program's `VERDICT` line: all 40 counter readings (8 + 16 + 16) 10 of 10 valid pairs,
0 discards, 0 timeouts, 0 bracket failures; the 3 Spin2 readings 10 of 10 pairs in one class; no
`RIG FAIL`. Campaign: `campaigns/2026-09-p2-errata-predictions/`
(tests 12–14).

### EF-078 · A cog of 4–7 held in a wait at the wrap keeps its group current: `WAITATN` and `WAITX` both count as running — `CONFIRMED`
*How proven:* `e3-waiting-keeper-test` — a keeper in cog 7 held in `WAITATN` (`$FD603C24`; no cog sends
ATN) started by the first line of `main()` and alone in 4–7 through wrap 1; it was then stopped and a
keeper in cog 6 held in `WAITX ##$FFFF_FFF0` (`$FFFFFFFF`, `$FD67E01F`; 2 + D clocks, 14 short of
2^32, started with the lower long just past `$101F_xxxx` so the wait spans the wrap) alone through
wrap 2; then no keeper through wrap 3. Samplers started in cogs 4/5 for one reading each and
stopped; cog 1 the group-0 control. *Result (log `debug_260927-162313`):* boot `$0000_0000_$00C1_3C9C`,
running `%10000001` (l.22). hi=0 cog 4 **D = 0** (l.35). **After wrap 1 with only the `WAITATN`
keeper: cog 5 D = 0** (l.75; e.g. l.65 `ref=$0000_0001_$101F_D95F smp=$0000_0001_$101F_D97F`).
**After wrap 2 with only the `WAITX` keeper: cog 4 D = 0** (l.115). **Positive control:** no cog in
4–7 through wrap 3 → cog 5 **D = 1** (l.155; l.145 `smp=$0000_0002_$101F_EBE7` beside `ref=$0000_0003`).
Controls: cog 1 D = 0 in all four readings; running-cog mask on every poll `%10000011` (19) with the
`WAITATN` keeper, `%01000011` (17) with the `WAITX` keeper, `%00000011` (17) with none. **Grounds:**
the E3 chapter may say an application's own cog of 4–7 meets the workaround condition while it is
held in `WAITATN` or `WAITX`. *Limits:* two waits tested (not `WAITCT`, `WAITSEx`, `WAITPAT`,
`WAITINT`, `WAITFBW`/`WAITXFI`/`WAITXMT`/`WAITXRL`/`WAITXRO`); cogs 6 and 7 as the keeper; one
wrap each; 200 MHz. Spin2's `WAITCT()`/`WAITMS()`/`WAITUS()` are not wait instructions: the
interpreter polls `GETCT` in a loop (Spin2 interpreter v55, `pwct`), so a Spin2 cog in them is
executing, as the polling samplers of EF-068 were.
*Reader copy re-run (2026-09-27, Stephen):* the shipped `p2-errata/examples-library/e3-workaround-waiting-cog-test.spin2`,
whose `verdict()` was restructured to a single exit (measuring image identical, same offset), ran once
(`logs-archive/debug_260927-172602`, 13,291 bytes = the committed file compiled): every reading's D,
pair count and bracket result identical to the run above; both verdicts `CONFIRMED`.
*Source:* `…/tests/e3-waiting-keeper-test.spin2`.

### EF-079 · Cogs 0–3 show the same band as cogs 4–7 when every one of them is stopped across wraps, and it closes in one wrap — `CONFIRMED`
*How proven:* `e3-group0-idle-band-test` — cog 0 checked the boot state, started the test (Spin2) in
cog 4 with `COGSPIN`, and stopped itself; cog 4 was the reference from `$0000_0000_$00C1_3D4C` on
(started before wrap 1, its upper long equal to its own wrap count on every poll), cog 5 the group-1
control. Cogs 0–3 held empty through wraps 1 and 2, then cogs 1 and 3 started and never stopped.
*Result (log `debug_260927-162507`):* boot `%00000001` (l.21), cog 0 stops (l.22), cog 4 up (l.24).
Running-cog mask on every poll: **`%00110000` (35) — no cog of 0–3 — until the band opened**, then
`%00111010` (36). **In the band (hi = 2): cogs 1 and 3 D = 2, early and late** (l.84, 95, 131, 142; l.130
`ref=$0000_0002_$E013_B7FF smp=$0000_0000_$E013_B819`). **After the one closing wrap (hi = 3): D = 0,
early and late** (l.169, 180, 216, 227; l.159 `smp=$0000_0003_$1001_4BF1`), **and at hi = 4: D = 0**
(l.254, 265). Controls: cog 5 D = 0 in all six readings. **Grounds:** E3 is a property of both
groups, not of 4–7; the chapter's "measured on cogs 4–7" becomes "both groups". A Spin2 program is
exposed in 0–3 only if cog 0 stops (or its top method ends) while 0–3 is otherwise empty. *Limits:*
the group-0 cogs sampled were 1 and 3; a lag of two wraps; 200 MHz. *Source:*
`…/tests/e3-group0-idle-band-test.spin2`.

### EF-080 · The band closes at the first wrap its group runs through, in one step, from a lag of 8 wraps; Spin2 `GETMS()`/`GETSEC()` read short by the same time inside it — `CONFIRMED`
*How proven:* `e3-band-closes-in-one-wrap-test` — cogs 4–7 held empty through 8 wraps (171.8 s at
200 MHz), then PASM samplers in cogs 4 **and** 7 and a Spin2 sampler in cog 5 (`GETMS()` then
`GETSEC()` on each request) started and never stopped; cog 1 the group-0 control. The Spin2 pairs are
classed from cog 0's own `GETMS`/`GETSEC` before and after, against the time of 8 wraps computed from
`clkfreq` by `MULDIV64`: **171,798..171,799 ms, 171..172 s** (l.14). *Result (log
`debug_260927-162927`):* running-cog mask `%00000011` on all 131 polls up to the band, then
`%10110011` (36). **In the band (hi = 8): cogs 4 and 7 D = 8, early and late** (l.170, 181, 228, 239).
**After the one closing wrap (hi = 9): D = 0, early and late** (l.277, 288, 335, 346), **and at
hi = 10: D = 0** (l.373, 384). **Cog 4's own upper long went from 0 to 9 across that one wrap** (l.413;
last band pair `smp=$0000_0000_$E013_BB32`, first after it `smp=$0000_0009_$1001_546A`): a 64-bit
interval timed across it is 8 × 2^32 clocks too long. **Spin2:** all 20 band pairs SHORT (l.203,
261; offsets 171,798–171,799 ms and 172 s — e.g. l.260 cog 0 `ms=190_617 s=190`, cog 5 `ms=18_819
s=18`); all 10 pairs after the closing wrap CURRENT (l.310; l.300 both `ms=194_637 s=194`).
Controls: cog 1 D = 0 in all six readings. **Grounds:** the band closes at the first wrap its group
runs through, whatever the lag (1 in EF-068, 2 in EF-079, 8 here) — so *waiting out the band* (one
wrap after the group's first cog starts) is a proven workaround; and `GETMS()`/`GETSEC()`, which the
interpreter computes from the calling cog's `GETCT WC` + `GETCT` (Spin2 interpreter v55, `getms_`),
are affected exactly as `GETCT WC` is. *Limits:* one lag (8) beyond EF-068/EF-079's 1 and 2; the
Spin2 sampler in cog 5 only; 200 MHz. *Source:* `…/tests/e3-band-closes-in-one-wrap-test.spin2`.

### EF-081 · No PASM2 instruction that takes a CT target sees E3's stale upper long — `WAITCTn`, `POLLCTn`, `JCTn`, `JNCTn`, the CT interrupts, the `SETQ` timeout and `WAITX` time exactly as in a current group, in the window and across its closing wrap; a cog held in `WAITCT1` counts as running — `CONFIRMED`
*How proven:* `e3-scope-pasm2-ct-events-test` (VO-J-018) — a PASM2 probe runs one of seven commands
per request, each on three targets after its own arm-time `GETCT`: `ADDCT1-3` + `WAITCT1-3`;
`POLLCT1-3`; `JCT1-3`; `JNCT1-3`; `INT1-3` on CT-passed-CT1-3; three `SETQ` + `WAITATN WC` timeouts;
three `WAITX`. Control probes in cogs 1-3; stale probes in cogs 4-7, started after their group missed
a wrap (three windows: wraps 1, 3, 5 missed). Every command ran **IN** a window (targets 84–168 ms)
and **ACROSS** the wrap that closes it (armed at lower long ≈ $F801_xxxx, targets $0800_0000–$0900_0000
past the wrap, so the group's upper copy jumped while each target was pending), in both groups.
*Result (log `debug_260929-140800`, 2026-09-29, first run, clean):* running-cog mask exactly as
started on every poll (`%00001111` ×69, `%11111111` ×15, `%01111111` ×15, `%10001111` ×1). All 29
arms status 0 and bracket held (l.277–306); **all 87 targets fired 3–49 clocks after their target,
the same spread in the control arms as in the stale ones** (tolerance 1,000). Stale arms: Darm = 1 in
all 15 (l.307 — `GETCT WC` stale, the E3 control), Dend = 1 IN and 0 ACROSS (e.g. l.147 cog 4
`WAITCT` armed `$0000_0000_$F801_9270` beside cog 0's `$0000_0001_$F801_F1A3`, ended
`$0000_0002_$0901_9282`: Dend 0). `SETQ` timeouts: C = 1 in all 12. Every command `NOT AFFECTED`
(l.308–314). **K arm:** cog 7 alone in 4-7, held in `WAITCT1` through wrap 6, read Dend = 0 (l.272,
315). **Grounds:** the CT events, the `SETQ` timeout and `WAITX` use the lower long only, as the P2
Documentation defines the events (`silicon-doc-text.txt`:2040, :2084, :2137) — now measured, including
across the jump; and a cog held in `WAITCT1` keeps its group current, as `WAITATN` and `WAITX` do
(EF-078). *Limits:* `WAITATN` stands for the `SETQ`-timeout family (EF-020: one mechanism across the
wait family); lag 1 in each window; the K arm tests `WAITCT1` only; 200 MHz; run once.
*Source:* `…/tests/e3-scope-pasm2-ct-events-test.spin2`.

### EF-082 · No Spin2 counter method but `GETMS()`/`GETSEC()` sees E3's stale upper long — `WAITCT()`, `POLLCT()`, `WAITMS()`, `WAITUS()` and `GETCT()` are current in the window and across its closing wrap — `CONFIRMED`
*How proven:* `e3-scope-spin2-counter-methods-test` (VO-J-019) — a Spin2 probe runs `WAITCT(salo +
dn)`, `REPEAT UNTIL POLLCT(salo + dn)`, `WAITMS` or `WAITUS` on three targets after its own arm-time
`GETCT()`; control probes in cogs 1-3, stale probes in cogs 4-7 started after their group missed
wrap 1; each method IN the window and ACROSS its closing wrap, in both groups. `GETCT()` is judged by
a bracket against cog 0's reads at arm and end; `GETMS()`/`GETSEC()` at arm and end are classed
against cog 0's (one wrap = 21,474..21,475 ms, 21..22 s at 200 MHz, l.22). *Result (log
`debug_260929-140656`, 2026-09-29, first run, clean):* all 16 arms status 0 and bracket held
(l.159–175); all 48 targets ended 34–2,202 clocks after their target (tolerance 50,000). Stale arms
Darm = 1; Dend = 1 IN, 0 ACROSS. **`GETMS()`/`GETSEC()` short by one wrap at arm and end IN the
window, current at the end ACROSS it** (e.g. l.90: cog 0 22,827 ms / 22 s, probe 1,352 ms / 1 s —
short by 21,475 ms); current in every control arm. Verdicts l.176–181: `WAITCT()`, `POLLCT()`,
`WAITMS()`, `WAITUS()`, `GETCT()` `NOT AFFECTED`; `GETMS()`/`GETSEC()` `CONFIRMED AFFECTED`.
**Grounds:** measured, as the v55 interpreter reads: only `getms_` takes `GETCT WC`; `GETCT()`,
`pwct` (`WAITCT`/`POLLCT`) and `waitus_` (`WAITUS`/`WAITMS`) take the lower long only. *Limits:* lag
1; 200 MHz; run once. *Source:* `…/tests/e3-scope-spin2-counter-methods-test.spin2`.

### EF-083 · `DEBUG_TIMESTAMP` stamps a DEBUG line with the sending cog's own copy of the counter: a line sent from E3's stale window carries a stamp one wrap early, and prints out of time order beside cog 0's — `CONFIRMED`
*How proven:* `e3-scope-debug-timestamp-test` (VO-J-020) with `DEBUG_TIMESTAMP` declared and
`DEBUG_COGS` = cogs 0, 1, 4, 7 — per pair, cog 0 sends a stamped REF line carrying its own
`GETCT WC`/`GETCT`, a probe sends a stamped PRB line carrying its own, cog 0 sends a second REF.
Probes: cog 1 (Spin2, group 0, control), cog 4 (Spin2 `debug()`) and cog 7 (PASM2 `DEBUG`), both
started after group 1 missed wrap 1. Stamps judged by `e3-scope-debug-timestamp-verdict.py`, rules
fixed before the run. *Result (log `debug_260929-141026`, 2026-09-29, first run, clean):* all 471
DEBUG lines carry a `$HHHH_HHHH_LLLL_LLLL` stamp after `CogN`. **In the window, all 40 PRB
stamps from cogs 4 and 7 are one wrap behind cog 0's REF stamps and match their own stale payload**
— e.g. l.129–131: cog 0 `$0000_0001_10CC_275E`, cog 7 `$0000_0000_10CD_6197` (its payload
`$0000_0000_10CD_617E`, 25 clocks before), cog 0 `$0000_0001_10CE_9896`; so every one of the 40
prints earlier than the line sent before it. **After the closing wrap, all 20 are current** (l.353–355:
cog 4 `$0000_0002_1002_D5A2` between cog 0's `$0000_0002_1001_959E` and `$0000_0002_1004_0D0E`).
Controls: cog 1's 40 pairs current, in order, each stamp at its own payload; every REF stamp at its
own payload; program window line `AS NEEDED` (l.487). Verdict (script): `AFFECTED` for Spin2
`debug()` and PASM2 `DEBUG`. **Grounds:** the v55 debugger reads the stamp by `GETCT WC` / `GETCT`
in the sending cog's debug interrupt (`debug_isr`), so it inherits that cog's group copy — measured
here. The debugger's breakpoint view shows a CT read by the same code (`debug_entry`); not tested
separately. *Limits:* lag 1; 200 MHz; run once; PNut-Term-TS v1.1.0 passed the stamp through
unchanged. *Source:* `…/tests/e3-scope-debug-timestamp-test.spin2` +
`…/tests/e3-scope-debug-timestamp-verdict.py`.

### EF-084 · After a no-wait `RDFAST`, a `RDLONG` issued within 16 clocks is released before its own read and returns the previous hub read's long, and a `WRLONG` is released before it lands and is lost if another hub instruction follows; the waiting form prevents both, and 16 clocks (7 non-hub instructions) prevents the read (a write at 16 clocks was not run) — `CONFIRMED`
*How proven:* `test-o29-rdfast-nowait-releases-hub-op` (VO-J-021; the clean-room study's O29
prediction). Measuring cog 1 in cog execution, cog 0 reporting (`DEBUG_COGS = %0000_0001`). Each
trial: a primer `RDLONG` of `$A5A5_0001` (also fixing the hub phase), then `RDFAST` (D =
`$8000_0000` no-wait, or `0` waiting) of a stream long in slice `af`, k `NOP`s, then the instruction
under test on a long in slice `ar`; 64 (`af`, `ar`) cells × 16 repetitions per run; records read
after the cog settles. Image R: `RDLONG` of a sentinel `$5A5A_0002` into a destination seeded
`$C3C3_0003`. Image W: `WRLONG $F0F0_0005` over `$0F0F_0004`, read back at once (T3) or after a
`NOP` (T4), and again after settling. Each command echoed the mode it ran with.
*Result (log `debug_261001-000927`, 2026-10-01, first run, clean):* controls — C1 (`NOP` for the
`RDFAST`) sentinel 1024/1024 (l.49); PS (no-wait, `WAITX #200`, `RFLONG`) the stream's first long
1024/1024 (l.59); C3 `(new,new)` 1024/1024 (l.249); no unwritten record, no other value, every
cell's 16 repetitions identical (l.480). **T1, k = 0: 43 of 64 cells read the primer `$A5A5_0001`
in every repetition (688 of 1024), by δ = (`ar` − `af`) mod 8: 8 8 7 6 5 4 3 2** (rows l.151–158,
re-derived from the rows: 43, split as stated; l.159). **The k sweep, per repetition: 43, 54, 61, 64,
48, 32, 16, 0, 0 for k = 0..8** (rows l.161–238; totals over 16 repetitions 864, 976, 1024, 768,
512, 256, 0, 0, l.169–239), every δ split as the study predicted (l.493–501). The escaping cells at
k = 0 were the ones the study's phase inference named (no escape at `af` 2–3; `ar` 3 alone at
`af` 4; `ar` 0 and 3–7 at `af` 1, l.151–158). **T3: 43 cells `(old,old)` — the write lost — by δ
8 8 7 6 5 4 3 2, and 21 `(primer,new)` — the immediate read-back released instead** (l.263–272);
**T4: `(seed,new)` in all 64 — the write lands when no hub instruction follows** (l.274–283).
**Waiting form: C2 sentinel 1024/1024 at every k = 0..8 (l.69–149), C4 `(new,new)` 1024/1024
(l.260)**, in the same run. Verdicts l.502–505: RDLONG, WINDOW, WRLONG, WAITING FORM all
`CONFIRMED`. **E7 arms:** E7N (no-wait then blocking `RDFAST`, spacings 2 and 4–20 clocks)
reproduced E7 in 64 of 64 cells, failing spacing by phase 10, 9, 8, 15, 14, 13, 12, 11 clocks in
every slice, as EF-074 (l.481–490); **E7B (the first `RDFAST` blocking) read `new[s]` then
`new[s+1]` in all 18,432 trials**, the two `RDFAST`s taking 20–34 clocks (l.506–507).
**Grounds:** the P2 Documentation restricts only FIFO reads after a no-wait `RDFAST`
(`silicon-doc-text.txt`:3043) and says nothing of `RDLONG`/`WRLONG`, which are documented to read
and write their own address: a silicon erratum (P2 Errata E7 — planned as E8, merged into E7 on 2026-10-01: one trigger, one window, one workaround; `p2-errata/CLASSIFICATION-GUIDANCE.md`). E7's failing spacings (8–15 clocks)
and safe spacing (16) coincide with this window, so E7 is the same release acting on a waiting
blocking `RDFAST` (the study's mechanism: the no-wait `RDFAST`'s completion signal raised a second
time when its FIFO first holds data). The Spin2 v55 interpreter uses only the blocking form.
*Limits:* `RDLONG`/`WRLONG` only (byte/word, `SETQ` blocks and a no-wait `WRFAST`: VO-J-023);
the write runs (T3, T4, C4) ran at k = 0 only — no `WRLONG` at 16 clocks or more was run, so the
16-clock rule was proven here for reads, not writes (corrected 2026-10-01 from a title that said it
prevents both; found while writing the merged E7 chapter; **writes at 16 clocks: EF-088**);
`RETA` and an interrupt inside the window not tested; hub execution excluded by the P2
Documentation (`RDFAST` cannot be used there, :353-357); one cog; cog execution; 200 MHz; run
once. *Source:* `…/tests/test-o29-rdfast-nowait-releases-hub-op.spin2`.

### EF-085 · With break-on-`BRK` armed, a `BRK` whose condition is false still enters the debug interrupt, and `GETBRK` shows the last condition-true `BRK`'s code, not its own; a `SKIP` before or a taken `JMP` before cancels both — `CONFIRMED`
*How proven:* `test-so109-conditional-brk-breaks` (VO-J-022; the clean-room study's SO109
prediction), no DEBUG. Cog 0 enabled break-on-`BRK` for cog 1 alone (`HUBSET $2000_0002`), wrote a
16-long debug ISR to cog 1's load area `$FFF40` and read it back 16/16, started cog 1. The ISR
recorded each entry's `GETBRK` word and its return-address word (C bit 31, Z bit 30), re-armed
(`BRK #$10`) and returned. Report on P62, plain serial, 2,000,000 baud.
*Result (log `debug_261001-001006`, 2026-10-01, first run, clean):* 10 records, none unattributed
(l.72–82). Entry record: bit 23 set, return `$000` (l.72). Controls `p1` `$A1`, `p2` `$A9`
(l.73, 81). **Condition-false sites entered the ISR, each showing the previous condition-true
code, its saved flags confirming the condition was false: `e1` (`if_z`, Z = 0) code `$A1`;
`e2` (`if_nz`, Z = 1) `$D4`; `e3` (`if_c`, C = 0) `$D4`** (l.74, 77, 78); condition-true `t1`
`$C3`, `t2` `$D4` (l.75–76). No record from `s1` (`SKIP #1` before), `j1` (taken `JMP` before),
`w1` (`if_z JMP` taken), `w3` (`if_z SKIP #1` taken); `w2` delivered `$F4` and `w4` `$F6` with
the condition true for the break (l.79–80). Verdicts l.96–101: BREAK, CODE (stale), CANCELS,
IDIOMS all `CONFIRMED`. **Grounds:** as the P2 Documentation states — "Regardless of the execution
condition, the BRK instruction will trigger a debug interrupt, if enabled. The execution condition
only gates the writing of the 8-bit code" (`silicon-doc-text.txt`:2491) — so documented behaviour,
not an erratum. Spin2 v55's "a condition has no effect" (:62) is right about the break and, read
literally, wrong about the code. *Limits:* the `SKIP` idiom tested outside an ISR only; one cog;
200 MHz; run once. *Source:* `…/tests/test-so109-conditional-brk-breaks.spin2`.

### EF-086 · The no-wait `RDFAST` erratum's scope (P2 Errata E7): a no-wait `RDFAST` releases `RDBYTE`, `RDWORD`, `WRBYTE` and `WRWORD` exactly as `RDLONG`/`WRLONG`; a released read writes the flags of the value it returns and still steps `PTRA++`; a no-wait `WRFAST` releases nothing; a `SETQ` block `RDLONG` in the window wrote one wrong long and the cog then stopped responding — `CONFIRMED` (predicted arms) / `OBSERVED` (`WRFAST`, `SETQ`)
*How proven:* `test-o29b-rdfast-nowait-hub-op-scope` (VO-J-023), the EF-084 construction (primer,
`RDFAST`/`WRFAST`, k `NOP`s, instruction under test; 64 cells × 16 repetitions; each run with a
`NOP`-for-the-FIFO control and the waiting form), cog 0 reporting through a hub line buffer.
*Result (log `debug_261001-014330`, 2026-10-01, first run, clean):* **positive control** — C1, PS,
T1 at k = 0 (688 primer, 43 per repetition by δ 8 8 7 6 5 4 3 2) and k = 7 (sentinel 1024)
reproduced EF-084 (l.90). Every `NOP` control and waiting form correct in all 1024 records or
cells; no repetition disagreed in any run; **in every predicted test run the released cells were
exactly T1's 43** (re-derived from the rows).
- **Flags** (`RDLONG … WCZ`, flags preset C = 1 Z = 1, captured after the read): primer
  `$A5A5_0001` → released records `($A5A5_0001, C=1, Z=0)`; primer `$0000_0000` → `($0000_0000,
  C=0, Z=1)`; correct records `($5A5A_0002, C=0, Z=0)`; 688/336 each; no preset left, no late change
  (l.201, 203). A released read writes C and Z from the long it returns.
- **`PTRA++`:** `PTRA` stepped +4 in all 688 released and all 336 correct records (l.205): a
  released read still advances its pointer.
- **`RDBYTE` (offsets 0–3) and `RDWORD` (0, 2):** released in T1's 43 cells at k = 0, none at
  k = 7; each released value is the previous read's long shifted by the instruction's own offset and
  masked to its size (`$D4`/`$C3`/`$B2`/`$A1`; `$C3D4`/`$A1B2` from `$A1B2_C3D4`), with that value's
  flags (l.490, 495; totals R 688 S 336 in every test run).
- **`WRBYTE` (0–3) and `WRWORD` (0, 2):** with a read-back following, 43 cells kept the target's old
  long unchanged — the write lost — and 21 released the read-back; with nothing following, all 64
  landed (l.788, 793; old 1376 / new 336 / primer 336 in every W1 run).
- **No-wait `WRFAST`** (FIFO flushed by a blocking `RDFAST` after every trial): **no early release**
  of `RDLONG … WCZ` or `WRLONG` at k = 0 or k = 7 (reads: 2,048 test records correct with their
  flags; writes: `(new,new)` in all 1,024 cells at k = 0 and at k = 7; l.906, 908).
- **`SETQ #7` + `RDLONG` (block of 8)** into a guarded sacrificial register range: the `NOP` control
  and the waiting form read the right block in 1024/1024 records with cog RAM unchanged outside
  the range (l.922–937). After the no-wait `RDFAST` at k = 0, the first trial's record held **the
  previous read's long in register 0 and registers 1–7 not written** (l.942, 951); **the measuring
  cog then did not finish the run within 1 s** and cog 0 stopped it (l.940–941); 1,023 records were
  never written (l.952).
**Grounds:** the release is one mechanism across widths and directions (EF-084 → E7): every hub
read and write width is affected the same way, at the same cells. The returned value is the
previous read's long seen through this instruction's own size and offset, and the flags follow that
value. `WRFAST`'s no-wait form does not release a following hub instruction. A released block read
is the most damaging case seen: one wrong long, the rest unwritten, and the cog lost. *Limits:* the
`SETQ` result is one trial — why the cog stopped (stalled or running elsewhere), whether it wrote
hub RAM after, and k = 7 for the block read were not observed; `RETA` and an interrupt inside the
window not tested; hub execution cannot use `RDFAST`; one cog; cog execution; 200 MHz; run once.
*Source:* `…/tests/test-o29b-rdfast-nowait-hub-op-scope.spin2`.

### EF-087 · The no-wait `RDFAST` erratum's workaround (P2 Errata E7) protects a `SETQ` block `RDLONG` — the waiting form and 16, 18 and 20 clocks after a no-wait `RDFAST` read the right block with cog RAM intact; released at 4 clocks, a block read either writes one wrong long and overwrites cog registers `$000`–`$001`, or the cog does not finish — `CONFIRMED` (workaround) / `OBSERVED` (release)
*How proven:* `test-o29c-setq-block-workaround` (VO-J-024), the EF-086 construction with **every run
and every trial in a fresh measuring cog** (COGINIT, a cog-RAM baseline equal to the loaded image,
the run, COGSTOP). *Result (log `debug_261001-114625`, 2026-10-01, first run, clean):*
**positive control** reproduced EF-084 (l.84).
- **Release, single trials at k = 0** (`SETQ #7` + `RDLONG` starting 4 clocks after the no-wait
  `RDFAST`), 4 trials per cell, each cell the same in all 4: **af0/ar0 and af0/ar4** — block long 0
  the primer `$A5A5_0001`, longs 1–7 not written (seed `$C3C3_0003`), the cog finished and answered
  a ping, and **cog registers `$000` and `$001` changed** from `$FC78_00B0`/`$F605_8C64` to
  `$0000_0060` (af0/ar0) or `$0000_0061` (af0/ar4) and `$4000_0053` — neither block data nor the
  primer (l.107–160); **af2/ar0 and af1/ar3** — nothing written, the cog did not finish within 1 s
  (stopped) (l.161–193). The four cells are all released in EF-084's single-read map at k = 1
  (also 4 clocks), including the two that escape at k = 0. `NOP` controls: the right block, cog RAM
  intact, in all four (l.85–106).
- **Workaround, 1024 records each:** the waiting form, and a no-wait `RDFAST` with 6 `NOP`s (16
  clocks to the block `RDLONG`: the rule's boundary), 7 (18) and 8 (20): **the right block in
  1024/1024, 0 cog registers changed outside the destination, the cog finished** (l.213–271);
  verdicts `CONFIRMED` (l.273–283).
**Grounds:** E7's rule — the waiting form, or 16 clocks (7 non-hub instructions, `SETQ` counting as
one) — holds for block reads as for single ones. A released block read is the most damaging E7
case: one wrong long and seven unwritten, with cog registers outside the destination overwritten,
or a cog that does not finish. *Limits:* what wrote `$000`/`$001`, and whether a cog that did not
finish was stalled or running elsewhere, are not known; block distances between 4 and 16 clocks,
other cells, and a block read's flags were not measured; one cog; cog execution; 200 MHz; run once.
*Source:* `…/tests/test-o29c-setq-block-workaround.spin2`.

### EF-088 · The E7 workaround blocks P2 Errata prints hold for a single read and a single write: `WAITX #12` after a no-wait `RDFAST` (the next hub instruction at 16 clocks) protects `RDLONG … WCZ`, `WRLONG` with an immediate read-back, and `WRBYTE`/`WRWORD` at every offset; the waiting form protects a write and its read-back — `CONFIRMED`
*How proven:* `e7-workaround-hub-access-test` (VO-J-025, campaign test 22), the EF-084 construction
(primer `RDLONG` of `$A5A5_0001`, then the `RDFAST`, then the instruction under test; 64 (af, a)
cells × 16 repetitions = 1,024 records per run), cog 0 reporting through a hub line buffer (DEBUG
data 24 bytes). The three blocks the chapter prints ran between marker comments, nothing between
their instructions (W_READ `rdfast nowait,hub_stream` / `waitx #HUB_SPACING_WAITX` (12) /
`rdlong value,hub_addr wcz`; W_WRITE the same with `wrlong value,hub_addr` / `rdlong
check,hub_addr`; W_WAIT `rdfast #0,hub_stream` / `wrlong` / `rdlong … wcz`), flags preset C = 1 Z = 1
before the primer. *Result (log `debug_261001-140939`, 2026-10-01, first run, clean; downloaded
`.bin` 24,590 bytes = a fresh build of the source, `cmp` silent):* re-derived from the per-cell rows
(every cell's 16 repetitions identical, agree `.` in all 15 runs). **Controls:** K_CLK `getct` /
`waitx #12` / `getct` = 16 in all 1,024 (l.42); C1 sentinel C = 0 Z = 0, PS the stream's first long,
C3 (new,new), all 1,024 (l.52, 62, 72); `nowait` echoed `$8000_0000` after every run (l.184).
**Positive controls (same run):** P_READ — 43 cells per repetition the primer with C = 1 Z = 0, by
δ 8 8 7 6 5 4 3 2, 21 the sentinel with C = 0 Z = 0 (688/336, l.82); P_WRITE — 43 (old,old) by δ
8 8 7 6 5 4 3 2 and 21 (primer,new) (688/336, l.102): EF-084 reproduced. **Workarounds, 1,024 of
1,024 each:** W_READ the sentinel `$5A5A_0002` with C = 0 Z = 0 (l.92); W_WRITE (new,new) `$F0F0_0005`,
read back at once and read later (l.112); W_WAIT (new,new) with C = 1 Z = 0 (l.122); `WRBYTE` +0..+3
and `WRWORD` +0, +2 the merged long (`$4C3D_2EFB`, `$4C3D_FB1F`, `$4CFB_2E1F`, `$FB3D_2E1F`,
`$4C3D_EAFB`, `$EAFB_2E1F` from `$4C3D_2E1F`), read back at once and later (l.132–182). Verdicts
l.188–191 all `CONFIRMED`. **Grounds:** E7's rule — the waiting form, or the next hub instruction at
least 16 clocks after the no-wait `RDFAST` — now proven for writes of every width as well as reads;
P2 Errata prints the three blocks as proven (KB: F-472/F-478 carry it). *Limits:* only `WAITX #12`
as the spacing (16 clocks exactly; no other filler, no longer spacing); `WRLONG`/`WRBYTE`/`WRWORD`
with a following `RDLONG` of the same long only; `WMLONG`, block writes, `RETA`, an interrupt in the
window not tested; one cog; cog execution; 200 MHz; run once. *Source:*
`…/tests/e7-workaround-hub-access-test.spin2`.

**The E7 reader copies re-run (2026-10-01, Stephen, same bench, once each, same session as
EF-088).** `examples-library/e7-next-hub-instruction-test` (EF-084's rig), `e7-every-hub-width-test`
(EF-086's) and `e7-workaround-setq-block-test` (EF-087's): each measuring PASM image byte-identical
to the as-run build (1,112 / 1,800 / 896 bytes, compared at the object base), cog-0 Spin2 restyled
(the last two restructured to single-exit methods). Each downloaded `.bin` (30,090 / 44,438 / 32,254
bytes) equals the archive build. Compared line by line with the original runs (logs
`p2-errata/audit/verification-tests/logs-archive/debug_261001-141047`, `-141100`, `-141120` against
`logs/debug_261001-000927`, `-014330`, `-114625`): **same line count (491 / 957 / 288), and every
analysed value, class, count and verdict matched in all three**; the differing lines (21 / 31 / 53)
carry only labels (`O29`/`O29B`/`O29C`/`E8`/`EF-084` → E7 wording) and hub string addresses. The
block-read copy reproduced both released outcomes exactly (af0 cells: one wrong long, registers
`$000`/`$001` → `$0000_0060`/`$0000_0061` and `$4000_0053`; af1/af2: did not finish within 1 s).
**One post-run edit:** the release-test copy printed `VERDICT E7RDLONG:` (and `E7WINDOW`, `E7WRLONG`,
`E7WAITING`) — a space lost in the relabelling; the 28 strings were corrected after the run (Spin2
text only; the measuring image re-checked byte-identical, DEBUG data 24 bytes).


## Open / pending empirical questions

- **SINC2 XZS-S2 start-up sample moved with the restyled cog-0 code (2026-09-26).** In
  `test-goertzel-sinc2-iteration-count` / its reader copy, the first `XZERO` arm's `k=0` sample
  read x = 92,185,644 in both original runs (2026-09-25) and 90,090,539 in the reader-copy run;
  the difference, 2,095,105, is 2^21 − 2,047, and y moved by exactly 3× that (C_Y = 3·C_X). The
  measuring PASM is byte-identical; the cog-0 Spin2 that sequences the arms was restyled, so the
  leading hypothesis is that what the first-stage integral holds when this arm's first
  `GETXACC` lands depends on cog-0 timing between arms. Excluded from analysis (`WARM = 3`); no
  verdict or analysed value changed. To decide: re-run the as-run build and the reader copy
  back to back and compare `k=0` of every SINC2 arm.

### Resolved
- **Labeled value in a named TERM (F-136 sub-item) — RESOLVED 2026-06-18.** Settled from the
  v55 doc, no further probe needed: a named TERM **does** display a value's decimal text —
  via `` `(value) `` substitution (short for SDEC_), e.g. `` debug(`MyTerm 'T: `(x)') ``
  (v55 `spin2-v55-text.txt` L1090 + canonical example L1299). The earlier guess ("named
  TERMs don't format; use plain `debug()`") was wrong: EF-002's glyph result is the
  *value-only formatter* feeding a numeric data element, NOT proof that values can't be
  shown as text. `term.yaml` ex2 + `ch03-term.md` finished accordingly (see EF-002, F-136).

---

## Prior-session empirical facts (absorbed)

Established by capture/verification in earlier sessions; recorded here so the golden source
is whole. Their test artifacts predate this tree and are not yet migrated to a campaign
folder — backfill a campaign + `.spin2` when located.

### EF-061 · PLOT default coordinates are bottom-left / Y-UP — `CONFIRMED`
> **Renumbered 2026-08-16 (F-267).** This entry was absorbed into the ledger at KB v1.14.3 under
> the id **EF-020**, which was already held by the `SETQ`+`WAITSEx` finding assigned 2026-07-04
> (`:291`). That entry keeps EF-020 — it is the older assignment and the one cited from two
> released manuals' roster history. Cite this PLOT fact as **EF-061**.
The PLOT window's default origin is bottom-left with Y increasing **upward**. `CARTESIAN
flipy=1` flips it to Y-DOWN. The manual + theory-of-operations prose had this **backwards**;
trust the `PLOT_GetXY` formula + the capture, not the ToO prose. (Also verified: raw-hex
`COLOR $RRGGBB` works; the default draw color is `clCyan`.) *Evidence:* prior-session PLOT
capture verification. *Grounds:* the PLOT manual chapter; `plot.yaml`.

### EF-021 · DEBUG session-end mechanisms — three distinct forms — `CONFIRMED`
- per-window `` `CLOSE `` — frees ONE named window;
- on-chip `DEBUG(DEBUG_END_SESSION)` — constant **27**, `{Spin2_v52}` — ends the WHOLE
  session (all windows + DEBUG.LOG);
- host `--end-marker <string>` — the capture workflow uses `### CAPTURE DONE ###`.
*Evidence:* prior-session verification + compiler. *Grounds:*
`constants/debug-end-session.yaml`; the per-window `CLOSE` directives.

### EF-022 · DEBUG display-window 3-phase lifecycle — `CONFIRMED`
A display window runs in three phases: **create** → **one-time configuration**
(channels/triggers as their own message — e.g. SCOPE/FFT config is NOT on the create line,
see EF-003) → **looping data updates**. LOGIC and SCOPE_XY accept their channel/label on the
create line (config-phase); SCOPE/FFT do not (update-phase). *Evidence:* the EF-003 run +
prior-session window work. *Grounds:* the create/config/update split across the
debug-display YAMLs + `statements/debug.yaml`.

### EF-023 · Top-level Spin2 code runs as its cog's task 0; task IDs are cog-local — `CONFIRMED`
In each cog, the **top-level (initial) code runs as that cog's `TASKID` 0**; `TASKSPIN(NEWTASK)`
then allocates upward (1, 2, …). Task IDs are **cog-local** — every cog has its own 0–31 task
space. *How proven:* `f198-tasks-per-cog-probe.spin2` (pnut_ts v1.55.0, `-d`, real P2 silicon,
RAM download) launched a second cog via `COGSPIN`; each cog's top-level code plus its two
`TASKSPIN(NEWTASK)` tasks reported `COGID()`/`TASKID()`. *Result (verbatim, both cogs identical):*
`TOP-LEVEL TASKID=0` · `task TASKID=1` · `task TASKID=2` · `spawned ids=1,2` — for `COGID 0` **and**
`COGID 1`. Each task's self-reported id matched `TASKSPIN`'s return (triangulated); the quantity is
discrete/deterministic, so one run is dispositive. *Verdict:* CONFIRMED 2026-07-06. *Grounds:*
`methods/taskid.yaml` + `registers/taskhlt.yaml` (F-198) — replaces the prior **unsourced** "main
task is typically ID 0" with the cog-local fact. Test replicated under
`campaigns/2026-07-cooperative-tasking/tests/`.

### EF-024 · ADC gain modes measure a window CENTERED on mid-supply (~VIO/2), not ground-referenced — `CONFIRMED` (F-202)
**Structural fact (definitive):** the pin-ADC gain modes (`P_ADC_1X/3X/10X/30X/100X`) measure an input
window **centered on mid-supply (~VIO/2)**, NOT a ground-referenced `0..V` range. Every gain's transfer
curve crosses its 50% point at **~1.64 V**. This refutes the fabricated `0..V/gain` framing (F-202) and
also **supersedes the derived nominal `1.65 ± 1.65/gain` (= 3.3 V/gain width) — that formula was WRONG**
(under-estimated the width ~1.4×).
**Representative magnitudes (MEASURED ON REAL P2 SILICON, N=1 — one part; vary part-to-part / VIO /
temperature; not a guaranteed spec):** 2 mV fine sweep, gain-mode raw 0..131072, 5%/50%/95% crossings:

| Gain | low | center | high | width |
|------|-----|--------|------|-------|
| 3.16× | 0.93 V | 1.648 V | 2.36 V | 1.44 V |
| 10×   | 1.41 V | 1.642 V | 1.87 V | 0.46 V |
| 31.6× | 1.57 V | 1.640 V | 1.71 V | 0.15 V |
| 100×  | 1.61 V | 1.640 V | 1.66 V | 0.05 V |

(1× = full rail 0..3.3 V.) **Widths scale ~√10 per gain step** (ratios 3.15 / 3.12 / 2.9 — confirms the
documented gain ladder); measured width ≈ **4.55 V/gain**, not 3.3 V/gain.
**How proven:** `adc-gain-window-fine.spin2` (pnut_ts v1.55.0, `-d`, real P2, RAM download) — on-chip DAC
`P0` → jumper → ADC `P1` loopback. **Bracketed:** simple digital P0→P1 loopback confirmed the jumper
(low→0, high→1); GIO/VIO internal references bracketed the scale (GIO≈20.5k, VIO≈108k); `center_raw`
≈65.5k confirmed each 50% crossing is a real transition, not noise. Reproducible across coarse (100 mV)
and fine (2 mV) sweeps. Tests + logs: `engineering/operations/correction-sweeps/f202-adc-jumper-verification/`.
**Companion (F-203 note):** the ratiometric single-pin absolute error was **≤9 mV** (reproducible; small
positive offset at low V, ~0 at mid/high) — does NOT support a **~15 mV single-pin absolute** floor; the
"~15 mV *pin-to-pin* spread" claim needs the move-jumper multi-pin extension (still open).
**Grounds:** F-202 corrections to IOSP §16.2 + Appendix B + Appendix C (print the measured centered
windows, labelled representative single-sample; DELETE the ground-referenced `0..V` ranges and DO NOT use
the derived 3.3 V/gain formula). *Verdict:* CONFIRMED 2026-07-07.
