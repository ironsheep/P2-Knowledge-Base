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

**Campaigns:** [2026-06 — DEBUG windows & smart pins](campaigns/2026-06-debug-windows-and-smart-pins/README.md)

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

## Open / pending empirical questions

- *(none currently)*

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

### EF-020 · PLOT default coordinates are bottom-left / Y-UP — `CONFIRMED`
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
