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

### EF-002 · A formatted value fed to a named TERM arrives as a RAW byte — `CONFIRMED`
`` `udec_(value) `` into a NAMED TERM renders a single raw-byte glyph (char = the value),
not decimal text — and a bare formatter between text (`SDEC(x)`) showed nothing. The
formatter (`udec_`/`sdec_`) is a *plain-`debug()`* feature; a backtick named feed has only
single-quoted text + control codes + `` `(expr) `` substitution, no formatter slot.
*Proof:* `test1` W3 (nothing) + W4 (glyph char 42). *Date:* 2026-06-17. *Grounds:* F-136
(labeled-value idiom — open: see ledger note below).

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

---

## Open / pending empirical questions

- **Labeled value in a named TERM (F-136 sub-item).** EF-002 shows two formatter forms fail
  in a named TERM. One combo is still untested: single-quoted text **+** a bare formatter
  (`` `MyTerm 'T:', sdec_(x) ``). The backtick grammar (no formatter slot) implies it also
  fails → the resolution is likely "named TERMs don't format; use plain `debug()` for
  formatted/labeled output." Settle, then finish `term.yaml` ex2 + `ch03-term.md`.

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
