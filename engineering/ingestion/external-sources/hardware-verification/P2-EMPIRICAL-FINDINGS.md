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
