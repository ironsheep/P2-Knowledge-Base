# Forum Thread Ingestion — Problem in the streamer's Goertzel SINC2 mode

- **Source URL:** https://forums.parallax.com/discussion/176065/problem-discovered-in-the-streamers-goertzel-sinc2-mode
- **Thread ID:** 176065
- **Pages:** 1 (single page; `/p2` returns HTTP 404)
- **Post count:** 3
- **OP author + date:** cgracey — 2024-12-16 10:48 (edited 10:50)
- **Fetched:** 2026-07-01
- **Topic class:** Silicon behavior / streamer Goertzel SINC2 mode defect (designer-reported hardware limitation + workaround)

## Thread purpose

Chip Gracey (the P2 chip designer), while experimenting with software-defined-radio ideas, discovered and reported a real defect in the P2 streamer's Goertzel **SINC2** mode: when the number of clocks per NCO/Goertzel cycle is **not a power of two**, the double-integration accumulators read out by GETXACC are periodically off by one integration, corrupting the current and next computed samples. He documents the mechanism, the affected conditions, a note he added to the silicon doc, and practical fixes/workarounds.

## Participant trust classification

| User | Trust | Basis |
|------|-------|-------|
| cgracey (Chip Gracey) | 🏆 Authoritative / trusted | P2 chip designer; ground truth comparable to Silicon Doc. He discovered, root-caused, and documented the defect. |
| ozpropdev | 🟢 Clearly knows what they're doing | Long-standing, highly regarded P2/P1 community expert (deep hardware/PASM contributor). Contributed only an acknowledgement here, no technical claim. |

## Chip Gracey findings (trusted gold)

### CG-1 · SINC2 mode corrupts GETXACC when iteration count varies (non-power-of-two)

> "I have been experimenting with software-defined-radio ideas and I just found a problem with the streamer's Goertzel SINC2 mode.
>
> When the number of clocks varies from the norm to complete a full NCO cycle, the X and Y values coming from GETXACC will be off by one double integration and it will corrupt the computed sample, along with the next one, before correcting.
>
> The fix is to only use Goertzel SINC2 mode with a power-of-two iteration count. For example, if you run at 256 MHz and are measuring for 1 MHz, that will always take 256 clocks per Goertzel cycle, so you have consistency in the SINC2 double-integration process."

**Means:** In Goertzel **SINC2** (double-integration) mode, the number of streamer iterations per Goertzel cycle must be **constant**. If `SETXFREQ`'s `D` value is not a power of two, the NCO cycle length varies by ±1 clock, so different Goertzel cycles integrate a different number of iterations. When GETXACC captures the double-accumulated X/Y, an off-by-one-iteration cycle produces a corrupted sample — and corrupts the following sample too before self-correcting. Choosing a clock frequency that makes the iteration count a power of two (e.g. 256 MHz sysclock measuring 1 MHz → exactly 256 clocks/cycle) keeps the iteration count consistent and avoids the error.

**Affects:** Streamer Goertzel SINC2 mode documentation; GETXACC / SETXFREQ descriptions; ADC/Goertzel measurement guidance.

### CG-2 · Silicon-doc note (verbatim), symptom rate, and workarounds

> "I made this note in the silicon doc:
>
> NOTE ABOUT GOERTZEL SINC2 MODE (2024.12.16)
> It has just been discovered that the SINC2 mode generates periodic problematic GETXACC readings when the number of iterations in a Goertzel cycle varies, due to SETXFREQ's D being a non-power-of-two value. The above example code was modified so that the clock frequency is now 256 MHz, instead of 250 MHz, so that the 1MHz being listened to will always take 256 clocks per Goertzel cycle. This causes the double-integrating accumulators in SINC2 mode to always have the same number of iterations before a GETXACC instruction executes and captures the double accumulations. Being off by a single clock cycle will corrupt the current and next samples."

> "@SaucySoliton, you were probably experiencing this problem and maybe didn't realize what was going on. This could have been causing periodic noise in your analog video measurements. It happens on the order of 30-60ms per error.
>
> The fix would be to run at some power-of-two frequency above the frequency you are analyzing, or just stick with SINC1 mode.
>
> If you want to simulate 1 clock of jitter before doing a GETXACC, just do a 'WAITX #1 WC' beforehand and you will get huge noise in your readings.
>
> If you always start with XZERO, instead of XCONT, and your measurement period is under 20ms, you may be fine using SINC2 in the Goertzel."

**Means:** Chip added an official Silicon-Doc note dated 2024.12.16, and updated the doc's example to run at 256 MHz (was 250 MHz) so the 1 MHz target always takes 256 clocks/cycle. Real-world symptom: periodic noise roughly every 30–60 ms per error (e.g. in analog-video measurements). Workarounds, in order of robustness:
> 1. Use a **power-of-two sysclock frequency** above the frequency being analyzed (makes iterations/cycle constant) — the primary fix.
> 2. **Use SINC1 mode instead** of SINC2 (single integration is not sensitive to this).
> 3. If you must use SINC2, **start each measurement with XZERO (not XCONT)** and keep the measurement period **under ~20 ms** — may be acceptable.
>
> Diagnostic tip: inserting `WAITX #1 WC` before a GETXACC deliberately injects 1 clock of jitter and reproduces "huge noise," demonstrating the mechanism.

**Affects:** Streamer Programming Guide (Goertzel/SINC2 section + any example using ~250 MHz), I/O & Smart Pins User Guide ADC/Goertzel chapter, Streamer/Goertzel YAML (GETXACC, SETXFREQ, XZERO/XCONT/XINIT streamer commands, streamer Goertzel mode).

## The problem / resolution

- **What the bug is:** In the streamer's Goertzel **SINC2** (double-integration) mode, GETXACC returns corrupted X/Y accumulations whenever the number of streamer iterations per Goertzel cycle is not constant. A varying iteration count arises when `SETXFREQ`'s `D` is a **non-power-of-two** value, causing the NCO cycle to complete in a varying number of clocks. An off-by-one-iteration cycle corrupts the current sample **and** the next one before the accumulator self-corrects.
- **Confirmed?** YES — **confirmed and root-caused by the P2 chip designer, Chip Gracey (cgracey, 🏆)**, who discovered it firsthand and reproduced the mechanism (via deliberate 1-clock jitter with `WAITX #1 WC`).
- **Root cause:** Non-constant iteration count per Goertzel cycle in SINC2's double-integrating accumulators; the two cascaded integrators are sensitive to the exact iteration count captured at GETXACC time. Single-integration (SINC1) is not affected.
- **Fix / workaround / erratum status:** No silicon change (this is a documented **behavioral limitation / erratum-class note**, recorded in the Silicon Doc dated 2024.12.16). Mitigations: (1) run at a power-of-two sysclock above the analyzed frequency so iterations/cycle is a power of two and constant (e.g. 256 MHz instead of 250 MHz for a 1 MHz target → 256 clocks/cycle); (2) use SINC1 mode; (3) if using SINC2, start with XZERO and keep measurement period under ~20 ms. Symptom cadence when unmitigated: an error roughly every 30–60 ms.

## Other credible technical contributions

- **ozpropdev (🟢):** Acknowledgement only — "Good to know Chip. Thanks for the head's up." No independent technical claim; corroborates that the finding was received as news by the expert community.
- **SaucySoliton (referenced, not a poster in captured text):** Chip addresses SaucySoliton directly, suggesting SaucySoliton's prior analog-video measurements were likely affected by this bug. Indicates a real, previously-unexplained field symptom now attributed to this defect.

## Doc-impact targets (reconciliation queue)

| # | Finding | Target doc/section | Suggested action | Trust |
|---|---------|--------------------|------------------|-------|
| 1 | SINC2 Goertzel mode requires a constant (power-of-two) iteration count per cycle; non-power-of-two `SETXFREQ` D corrupts GETXACC samples | Streamer Programming Guide — Goertzel / SINC2 section | Add a prominent caveat/warning documenting the constraint and mechanism (off-by-one integration corrupts current + next sample) | 🏆 |
| 2 | Recommended mitigations (power-of-two sysclock above target; or SINC1; or XZERO + <20 ms period) | Streamer Programming Guide — Goertzel usage/examples | Document the three workarounds; update any example that uses ~250 MHz to a power-of-two frequency (e.g. 256 MHz) | 🏆 |
| 3 | ADC/Goertzel measurement guidance should note SINC2 sensitivity (analog-video/SDR use cases; ~30–60 ms error cadence) | I/O & Smart Pins User Guide — ADC / Goertzel chapter | Cross-reference the SINC2 constraint where Goertzel filtering / ADC measurement is described | 🏆 |
| 4 | GETXACC / SETXFREQ / streamer Goertzel-mode semantics | Streamer & Goertzel YAML (GETXACC, SETXFREQ, XZERO/XCONT streamer commands, streamer Goertzel SINC1/SINC2 modes) | Add a note field: SINC2 double-integration requires constant iterations/cycle; link to Silicon-Doc 2024.12.16 note | 🏆 |
| 5 | Silicon Doc note (2024.12.16) exists and is authoritative source text | Ingestion / silicon-doc reconciliation | Verify the exact note is present in our Silicon Doc copy; treat as source of truth for the YAML/manual edits above | 🏆 |

## Open questions / unresolved

- **Exact clock-count boundary:** Chip says "under 20ms" and "30–60ms per error" — the precise relationship between measurement period, D value, and error onset is not fully quantified in the thread. Would need the Silicon-Doc example code / firsthand testing to characterize.
- **SINC3 (if applicable):** Thread discusses SINC1 vs SINC2 only; whether any higher-order integration mode exists/is affected is not addressed (P2 streamer Goertzel offers SINC1/SINC2 — confirm against Silicon Doc).
- **"Power-of-two iteration count" precise definition:** Chip frames the safe case as iterations/cycle being a power of two (256). Whether any constant non-power-of-two count is also safe (i.e., is it "constant" or specifically "power-of-two" that matters) is slightly ambiguous in the wording — the mechanism suggests **constancy** is the true requirement, with power-of-two being the practical way to guarantee it. Worth a clarifying note when reconciling.
- **SaucySoliton confirmation:** Whether SaucySoliton confirmed the attribution of their analog-video noise to this bug is not captured (no follow-up post on the fetched page).
