# SPEC VO-P-001 — the SPI alignment pad: is it a phase, and is it counted in clocks or in time?

**For:** the P2X8C4M64P / uSD-FAT32 project's bench (P2 Edge + SD card + working SPI driver).
**Written by:** P2-Knowledge-Base, 2026-09-19. **Status:** specification — not yet built.
**Results return to:** `EXTERNAL-HARDWARE-FINDINGS.md` as `XF-NNN`, citing the project and its rig.

---

## 1. Why this test exists — the decision each measurement feeds

The KB documents a **read-side** alignment pad: a `waitx #3` between starting a `P_TRANSITION`
SCK and starting a streamer that *samples* MISO (`p2kbPasm2StreamerSmartpinControl` →
`alignment_pad`). The value 3 is graded GOLDEN from `flash_loader.spin2:259`. The page then says:

> *"Different SCK rates may need different pad values — verify with a logic analyzer if you change
> either WXPIN or SETXFRQ."*

That is an instruction a reader cannot act on, and it is the only thing the KB says about rate.

Your project measured the **write** side — streamer driving `P_SYNC_TX` MOSI against a
`P_TRANSITION` SCK — and found the pad-vs-phase relationship is a **sawtooth of period `hp`**
(the SCK half-period in sysclks), with exactly one losing pad per `hp`, at `pad ≡ −6 (mod hp)`
across five rungs. At the losing phase the failure is **silent whole-sector write corruption**.
You flagged three things as unestablished, and this spec is built to settle exactly those:

| # | Question | What its answer changes |
|---|---|---|
| **Q1** | Is the safe pad counted in **sysclks**, in **absolute time**, or in **SCK periods**? | Whether a pad value is portable across clock frequencies at all. If it is time-based, every pad in every P2 SPI driver is wrong the moment `_clkfreq` changes, and the KB must say so. |
| **Q2** | Is there exactly **one** losing pad per `hp`, on both sides? | Whether "pick any pad but one" is safe advice, or whether the safe set must be measured per rate. |
| **Q3** | Does the **read** side behave the same way, and is `3` safe across rates or only at the flash-loader's? | Whether the KB's GOLDEN 3 needs a scope limit. This is the value shipping P2 code copies. |
| **Q4** | Does the sawtooth hold at `hp` = 2 and 3? | Whether the rule covers the fastest reachable rates, which is where an SPI driver actually lives. |

**Q1 is the one that matters most.** Everything else refines a rule; Q1 decides whether the rule
is a rule.

---

## 2. Design — a complete map, not a fit

⚠ **Do not fit a curve.** Only `hp` distinct phases exist, so for each `hp` the sweep over
`pad ∈ [0, hp-1]` is **exhaustive by construction** — there is nothing left to extrapolate. Report
the full pass/fail map. Five points produced `−6 mod hp`; a complete map either confirms it as a
law or shows what it actually is, and both are results.

### 2a. The three hypotheses, and the factorial that separates them

For a fixed `hp`, changing `_clkfreq` changes the SCK rate too, so one axis cannot tell the three
apart. Run **two axes**:

| Axis | Held constant | Varied | Separates |
|---|---|---|---|
| **A** | `hp` (in sysclks) | `_clkfreq` — e.g. 200, 250, 300 MHz | sysclk-count vs. time. SCK rate moves with it. |
| **B** | **SCK rate** (adjust `hp` with `_clkfreq` so `sysclk/(2·hp)` is constant — e.g. 200 MHz/`hp`=4 and 300 MHz/`hp`=6) | `_clkfreq` and `hp` together | sysclk-count vs. SCK-period |

**Predictions, to be written into the program before the run** (your convention and ours):

- **Sysclk-counted** → on axis A the losing pad is the **same integer** at every `_clkfreq`.
- **Time-constant** → on axis A the losing pad **scales with `_clkfreq`**: a pad of `p` at 200 MHz
  appears at ≈`1.5p` at 300 MHz. (This is the hypothesis your nanosecond-constant launch delay
  raises, and the reason this axis exists.)
- **SCK-period-counted** → on axis A it tracks `hp` and on axis B it does **not** move.

Any outcome that matches none of the three is the interesting one: report it as observed and do
not force it into a category.

### 2b. Controls — the run is void without them

1. **Positive control, every rung.** One pad value known to work at that `hp` must PASS. If it
   fails, the rig, the card or the clock changed; stop and diagnose before reading anything else.
2. **Negative control that must pass regardless of phase.** Include a block of all-`$00` and a
   block of all-`$FF`. These have no transitions to mis-sample, so they should pass at **every**
   pad, including the losing one. If a `$00`/`$FF` block ever fails, the failure is not phase —
   it is the card, the wiring or the driver, and the whole map is suspect.
3. **The discriminating pattern must have no short period.** Use a PRNG/LFSR-filled sector, not
   `$55`/`$AA`. A repeating pattern can alias: a one-bit phase error against `$55` reproduces
   `$AA`, which can read as a *different valid pattern* rather than as corruption.
4. **Prove the comparator can fail.** Once, deliberately corrupt one byte of the expected buffer
   and confirm the comparison reports a mismatch naming that offset. A comparator never seen to
   fail is not a detector.

### 2c. Expected values come from the device, not from our code

Sector size (512), CRC16 width, and response-token shapes come from the **SD specification**.
Do not derive an expected value from the driver's own constants — that makes the driver both the
subject and the authority.

---

## 3. Arms

### Arm W — write side (confirms and extends your existing result)

For each `hp` in {2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16} and each `pad` in `[0, hp-1]`:

1. Fill a sector buffer with a PRNG pattern seeded from `hp` and `pad` (so a stale buffer cannot
   masquerade as a pass).
2. Write the sector with that `pad` between `WYPIN` (SCK start) and `XINIT` (streamer start).
3. Read the sector back **using a known-good read configuration** — not the pad under test.
4. Compare byte-for-byte. Record PASS/FAIL and, on failure, the first differing offset and how
   many bytes differ.

Report a table: rows `hp`, columns `pad`, cells PASS/FAIL.

**Why read-back rather than a bus capture:** the failure you observed is silent at the protocol
level, so the card's stored content is the only ground truth about what it actually received.

### Arm R — read side (new; the KB's GOLDEN 3 is what is at stake)

Same sweep, inverted:

1. Write a PRNG sector **once**, with a known-good write configuration.
2. Read it back with the streamer sampling MISO, varying `pad` in `[0, hp-1]` per `hp`.
3. Compare to the known content.

Report the same table shape, and call out explicitly **whether `pad = 3` passes at every `hp`
tested** — that is the KB claim under test.

### Arm F — the frequency axes

Repeat Arms W and R at the axis-A and axis-B points of §2a. To keep the matrix affordable, run
the full `pad` sweep only for **three** representative `hp` values (one small, one mid, one large,
e.g. 3, 6, 14); for the rest, a single `_clkfreq` is enough.

### Arm S — scope of the claim (cheap, and it decides how we write it)

Record, once: board identity, SD card make/model/capacity, `_clkfreq` list, driver commit hash.
If a **second card** is available, run Arm W at three `hp` values with it. Two cards agreeing does
not make the rule universal, but two cards *disagreeing* would immediately bound it — and that is
the single cheapest way to find out that the pad is card-dependent rather than silicon-dependent.

---

## 4. What we will write from each outcome

| Outcome | What the KB will say |
|---|---|
| Sysclk-counted, one losing pad per `hp`, both sides | The pad is a **phase**: safe pad count has period `hp`, exactly one value loses, and a pad safe at one rate can be exactly wrong at another. Stated as mechanism, with the measured map cited. |
| Time-constant | **Every published pad value acquires a clock-frequency scope**, including the GOLDEN 3, and the KB says a pad must be re-derived whenever `_clkfreq` changes. This is the outcome with the widest blast radius. |
| Read side differs from write side | The two are documented separately and the existing page is scoped to reads explicitly, which it currently is not. |
| `−6 mod hp` does not generalize | We publish the **shape** (one losing phase per `hp`, silent corruption) without the formula. The shape is the actionable part. |

⛔ **We will not publish `−6 (mod hp)` as a rule on the current five points.** Whatever the map
shows, the KB will carry the relationship at the confidence the measurement supports, and the
scope from Arm S travels with it.

---

## 5. Notes from our side, so they are not rediscovered

- **Do not place a monitor pin on P62 in a `-d` build**, and do not assume a pin survives a
  `debug()` — every `debug()` reconfigures P62. This is your own RETRACTION-1, and it is the kind
  of thing that voids a run silently.
- **Restrict `DEBUG_COGS` to the reporting cog.** A debug-enabled cog takes a debug interrupt at
  every `COGINIT`; EF-057 measured accumulator corruption of 1,000,000–7,000,000 from exactly this,
  dropping to hundreds once restricted. A timing rig is the worst possible place to leave it on.
- **Report from a cog that is not measuring** (EF-057, and our VO-J-004 confirmed the contrast).
- **Compile with `pnut-ts -d`** or the contents of every `debug()` are ignored.
- `-D SYM=value` is rejected from **1.55.8** (exit 1, no output file) — it used to be accepted
  silently and define nothing. If your build scripts carry that form, they were always wrong and
  will now fail loudly.
