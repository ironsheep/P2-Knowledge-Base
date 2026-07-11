# Changeset-integrity audit — app-note CONTENT deltas (P2AN001/002/003/005)

**Gate:** §7.5 fleet-release. Closes **OPEN GAP A** in `CHANGESET-AUDIT-INDEX-2026-07-11.md` — the four
app-note `f3e702ed` **content** deltas that were mis-"pre-cleared" as template-only / no-change and never
got an independent pass. Baseline = each note's last public tag → HEAD, restricted to `opus-master/`.
Stance: *disprove each hunk is justified + proportionate.* Anchored to primary sources (Silicon Doc,
Smart Pins User Guide Ch10/Ch16, OBEX catalog, the note's own code) — **not** memory of intent.

**Verdict: ✅ CLEAN — 0 flags. All 10 hunks `faithful`; every one corrects a real pre-existing defect.**
One class-wide **KB-YAML** side-finding surfaced (filed **F-211**, below) — a manual↔YAML drift, not an
app-note defect.

Per-hunk verdict legend: `faithful` · `overstates-source` · `understates-source` · `introduces-new-claim` ·
`traces-to-nothing`.

---

## P2AN001 — single-pin instrumentation ADC (v1.0.1 → HEAD, 5 hunks)

| # | Hunk | Verdict | Source trace |
|---|------|---------|--------------|
| 1 | Power groups **"four" → "eight (P0–7, P8–15, …, P56–63)"** (three-source-rotation ¶) | `faithful` | Silicon Doc VIO/GIO per-group; `VERIFICATION-OPPORTUNITIES.md:57` "the 64 pins are 8 groups of 8 (P0-7, P8-15, …)"; edge-mini-breakout extraction "300mA per **8-pin group**". Old "four" was the error. |
| 2 | pins-32–35 tie: "4-pin power group (32–35)" → **"power group P32–39 (an 8-pin group)"** | `faithful` | Same. 32–35 all sit inside the 8-pin group P32–39. |
| 3 | Below-ground self-check: unified "reads negative" → **build-dependent** (CORDIC build signed/negative; the 5 muldiv64 builds unsigned → wraps off-scale high) | `faithful` | Verified against the note's own code: Recipe 3 `compute` does `abs pa wc` then `if_c neg pa` (carries sign, reads negative); base/R1/R2/R4/R5 use Spin2 `MULDIV64` (unsigned). Old "reads negative" was true only for the CORDIC build — a real error for the other five. |
| 4 | Pitfall: "isolated groups of **four** — pins 0–3, 4–7, …, 60–63" → **"groups of eight — pins 0–7, 8–15, …, 56–63"** | `faithful` | Same source set as #1. |
| 5 | Tip: "keep the sample period a power of two … SINC2 sampling mode 2^X[3:0]" → **"period is adjustable … SINC2 *filtering* mode does not restrict period to a power of two; WYPIN after WXPIN overrides up to ~11,585 clocks"** | `faithful` | Smart Pins Guide Ch16: L106 filtering-mode row; L297 "WYPIN override only applies when X[5:4] > %00 … a non-power-of-2 rate requires one of the filtering modes"; L311 SINC2 max = **11,585 clocks** (27-bit accumulator). The note's builds all use `%01_0111` (SINC2 *filtering*), so the old power-of-two claim was wrong for this note. |

## P2AN002 — CORDIC solver (v1.0.0 → HEAD, 3 hunks)

| # | Hunk | Verdict | Source trace |
|---|------|---------|--------------|
| 1 | 2³² overflow explanation refined: added that `$1_0000_0000 / STEPS` **won't compile** because the 2³² *dividend* is a 33-bit literal (the quotient itself fits) | `faithful` | Math-exact and more precise than the prior loose "that value would overflow." `$8000_0000/(STEPS/2)` = `2³²/STEPS` with a 32-bit-legal dividend. |
| 2 | OBEX **#2812** author "Total Spectrum Software" → **"ersmith"** | `faithful` | Authoritative OBEX catalog (`p2kb_obex_get 2812`) lists author = **ersmith**. Company→handle correction to match the record. |
| 3 | OBEX **#5361** author "SaucySoliton" → **"James Smith"** | `faithful` | OBEX catalog (`p2kb_obex_get 5361`) lists author = **James Smith**. Forum-handle→catalog-name correction. |

## P2AN003 — DAC output / audio (v1.0.0 → HEAD, 1 hunk)

| # | Hunk | Verdict | Source trace |
|---|------|---------|--------------|
| 1 | "Raising the period lowers the sample rate **(and the dither frequency)**" → "…lowers the sample rate, **though the PWM dither tone stays fixed at sysclock/256 regardless of the period**" | `faithful` | Silicon Doc L7930–31 (PWM sample period must be a multiple of 256; PWM dithers in 256-clock steps) + L7936 "**a frequency of Fclock/256 will be present in the output at −48 dB**." The dither tone is a per-256-clock PWM artifact, decoupled from the total period. Old "dither frequency lowers with period" was a real error. |

*(Bonus: this also settles the paused IOSP **Q4 "DAC dither cadence — sysclk vs /256"** from our own primary
source — PWM = fixed /256 (Silicon L7936); PRNG = every clock (Silicon L7918). Not an audit item; noted for
the IOSP expert-queue task «#54».)*

## P2AN005 — cooperative multitasking (v1.0.0 → HEAD, 1 hunk)

| # | Hunk | Verdict | Source trace |
|---|------|---------|--------------|
| 1 | "…which would need **a hardware mutex the P2 doesn't have**" → "…which would need **cross-cog lock coordination you avoid entirely by keeping the bus in one cog**" | `faithful` | The old clause was **false** — the P2 *does* have 16 hardware locks (LOCKNEW/LOCKTRY/LOCKREL/LOCKRET). The fix removes the false claim and states the accurate trade-off (splitting the bus across cogs would require lock coordination; single-cog ownership avoids it). Fixes a real defect. |

---

## Side-finding routed to the corrections register → **F-211** (KB YAML, not an app-note defect)

Verifying P2AN001 hunks #1/#2/#4 surfaced that the **same "groups of four" error** the manual just
corrected still lives in the shipped KB YAML — a manual↔YAML drift:
- `architecture/pin-power-domains.yaml` (canonical: title, body, `groups: "16 groups"`, oneliner, **and a
  datasheet citation quoting "groups of 4"** — likely fabricated; the Silicon Doc uses `{x}_{y}` placeholders).
- `architecture/smart-pins/smart-pin-11000-adc-internal-clock.yaml`, `…-11010-adc-scope-trigger.yaml`,
  `…-11001-adc-external-clock.yaml` (power_domain + see_also + code comment).
- `application-notes/p2an001-single-pin-instrumentation-adc.yaml:99` (companion YAML — still 4-pin after
  the manual went 8-pin).

Truth = **8 groups of 8** (P0-7 … P56-63). Full evidence + fix list in `P2KB-CORRECTION-FINDINGS.md` F-211.
This is `yaml`-head work (rides the KB rail); the app-note manuals are correct as-is.
