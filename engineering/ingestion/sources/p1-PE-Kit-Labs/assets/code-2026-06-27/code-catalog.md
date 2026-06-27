# Code Catalog — PE Kit Labs: Fundamentals v1.2 companion source

**Source:** Parallax #122-32305 *Propeller Education Kit Labs: Fundamentals* v1.2 companion code archive
**Captured:** 2026-06-27 · verbatim copy, per-lab subfolder structure preserved
**Files:** 89 `.spin` (Propeller 1 / Spin1)
**`code_validated: false`** — no P1 compiler available (`pnut_ts` is P2-only; flexspin not installed; P1 charter §3). Files are **captured + cataloged, not compiled.**

**Encoding note:** Many files are **UTF-16 (little-endian, with BOM)** as authored by the Propeller
Tool — left **verbatim/untouched** (not normalized to UTF-8). LOC figures below are logical lines.
**Language:** Spin1 + (a few) inline PASM1. **`.spin` is the P1 file extension** (P2 uses `.spin2`).

**Top-object vs library/driver heuristic:** a file is a **top object** if it declares the application
entry (a `PUB` the loader runs, usually with `_clkmode`/`_xinfreq` CON or named `main`/`Init`/`Test…`);
a **library/driver object** exposes reusable methods (Start/Stop, Freq, etc.) and is declared in another
file's `OBJ` block. `OBJ=1` means the file *uses* another object (so it is a top/composing object).

---

## Lab 3 — Setup and Testing 40-Pin DIP PE Platform (2 files)
| File | LOC | Role | Demonstrates / teaching point |
|---|---|---|---|
| `DoNothing.spin` | 6 | top | Empty `PUB main` — load to blank the chip / stop all activity before re-wiring. |
| `PushbuttonLedTest-v1.0.spin` | 30 | top | First board bring-up test: read a pushbutton input, drive an LED output — verifies wiring + the download toolchain work. |

## Lab 4 — I/O and Timing Basics (21 files)
| File | LOC | Role | Demonstrates / teaching point |
|---|---|---|---|
| `LedOnP4.spin` | 11 | top | Single I/O pin: `dira[4]:=1`, `outa[4]:=1` — direction + output bit, endless `repeat`. |
| `LedOnOffP4.spin` | 14 | top | Add timing: blink one pin with `waitcnt`. |
| `GroupIoSet.spin` | 11 | top | Group I/O: set a contiguous pin group in one assignment. |
| `IncrementOuta.spin` | 14 | top | Write binary counts to an LED group via `outa`. |
| `IncrementUntilCondition.spin` | 14 | top | Conditional `repeat` (loop until a condition). |
| `LedsOnOff.spin` | 16 | top | Group blink `%111111` on 1/4 s, off 3/4 s (`clkfreq/4`, `clkfreq/4*3`). |
| `LedsOnOffAgain.spin` | 17 | top | Refinement: restructured timing of the same blink. |
| `LedsOnOff50Percent.spin` | 17 | top | Refinement: 50% duty version. |
| `LedsOnOff50PercentAgain.spin` | 16 | top | Refinement: alternate 50% implementation. |
| `ButtonToLed.spin` | 14 | top | Read `ina`, mirror to `outa` — input→output. |
| `ButtonShiftSpeed.spin` | 30 | top | Pushbutton changes a shifting-display refresh rate (global + local vars). |
| `ShiftRightP9toP4.spin` | 17 | top | Shift a lit-LED display using shift operators + conditional blocks. |
| `ConstantBlinkRate.spin` | 20 | top | `CON`-defined blink rate; constants in timing. |
| `TimeCounter.spin` | 39 | top | Count elapsed time; operators + conditions. |
| `TimekeepingBad.spin` | 22 | top | **Anti-pattern** — naive timing that drifts (teaches *why* it's wrong). |
| `TimekeepingGood.spin` | 26 | top | **Fix** — synchronized event timing independent of other work in the cog. |
| `SecondCountdownTimer.spin` | 49 | top | Binary-LED countdown timer application. |
| `MinuteSet.spin` | 42 | top | Alarm-clock-style minute setter (accelerating button repeat). |
| `NonActuatedStreetlights.spin` | 20 | top | Project: fixed-pattern street-light controller. |
| `ActuatedStreetlightsEW.spin` | 21 | top | Project: sensor-actuated street-light controller. |
| `LedFrequenciesWithoutCogs.spin` | 48 | top | Multiple blink rates from one cog (motivates cogs — "much easier with cogs"). |

## Lab 5 — Methods and Cogs (7 files)
| File | LOC | Role | Demonstrates / teaching point |
|---|---|---|---|
| `CallBlink.spin` | 26 | top | Call a `Blink` method from `main` — program control + parameter passing. |
| `BlinkWithParams.spin` | 19 | top | Method behavior parameterized (pin, rate, reps). |
| `AnotherBlinker.spin` | 17 | top | Variation reinforcing method definition/call. |
| `BlinkWithCogs.spin` | 23 | top | `cognew(Blink(...), @stack[n])` ×3 — launch a method into 3 cogs (parallel blink). |
| `CogStartStopWithButton.spin` | 40 | top | Start/stop a cog process from a button (`cognew`/`cogstop`, cog-ID tracking). |
| `ButtonBlink.spin` | 30 | top | Combine input handling with a blink method across methods. |
| `TestSquareWaveMethod.spin` | 37 | top | Exercises a `SquareWave`-style method; precursor to the Objects/Counter labs. |

## Lab 6 — Objects (27 files)
| File | LOC | Role | Demonstrates / teaching point |
|---|---|---|---|
| `Button.spin` | 13 | library | Minimal reusable object — a single `PUB` method to read a button. |
| `Blinker.spin` | 55 | library | **Cog-manager** object: `Start(pin,rate,reps):success` + `Stop` (cogstop) — the Start/Stop convention; schematic-in-doc-comment. |
| `Bs2IoLite.spin` | 46 | library | BASIC-Stamp-style I/O helper library (5 PUB methods: HIGH/LOW/etc.). |
| `DotNotationExample.spin` | 17 | top | Call another object's method with dot notation (`obj.Method`). |
| `CogObjectExample.spin` | 22 | top | A top object that launches a process object into a cog. |
| `CogObjectExampleWithSchematic.spin` | 39 | top | Same + schematic documentation comment. |
| `MultiCogObjectExample.spin` | 22 | top | Multiple instances launched into multiple cogs. |
| `ButtonAndBlink.spin` | 23 | top | Compose Button + Blink behavior in one app. |
| `ButtonBlink.spin` | 28 | top | Button-controlled blink across methods/objects. |
| `AddressBlinker.spin` | 44 | library | Object reading/updating caller variables by **address** (PUB+PRI). |
| `AddressBlinkerWithOffsets.spin` | 46 | library | Refinement: address + offset indexing into a variable list. |
| `AddressBlinkerControl.spin` | 46 | top | Top object driving `AddressBlinker` (declares it in `OBJ`). |
| `AddressBlinkerControlWithOffsets.spin` | 48 | top | Top object driving the offset variant. |
| `HelloPST.spin` | 27 | top | First **Parallax Serial Terminal** use: `pst.Start`, send a message. |
| `HelloPST (Modified to Display Counting).spin` | 28 | top | Refinement: display a running count in the terminal. |
| `HelloPST (Modified for 57.6 kpbs).spin` | 36 | top | Refinement: change the baud rate. |
| `DisplayPushbuttons.spin` | 45 | top | Display I/O-pin input states in the terminal. |
| `TerminalButtonLogger.spin` | 57 | top | Log button events to the terminal (2 PUB methods). |
| `TerminalLedControl.spin` | 53 | top | Control LEDs *from* terminal input (PC→Propeller values). |
| `EnterAndDisplayValues.spin` | 39 | top | Read values typed in PST and echo them. |
| `TestMessages.spin` | 31 | top | DAT-block string messages + address passing. |
| `TestMessages (Expanding DAT Section).spin` | 35 | top | Refinement: grow the DAT message table. |
| `FloatStringTest.spin` | 36 | top | Float + FloatString objects (format floats to the terminal). |
| `TestBs2IoLiteObject.spin` | 25 | top | Exercises the `Bs2IoLite` library object. |
| `StackLengthDemoModified.spin` | 86 | top | Measure how much stack a cog method actually used (Object Info / Stack Length teaching). |
| `TickTock.spin` | 78 | library | Cog-based time-of-day tracker (`Start(...)`/`Stop`, days/hours/min/sec). |
| `Led and Pushbutton Schematic.spin` | 34 | doc | A "schematic-only" .spin — the Lab-6 circuit drawn entirely in a doc comment (Parallax font). |

## Lab 7 — Counter Modules and Circuit Applications (32 files)
| File | LOC | Role | Demonstrates / teaching point |
|---|---|---|---|
| `SquareWave.spin` | 62 | library | **Frequency synthesizer** object: `Freq(Module,Pin,Frequency)` — NCO mode 0–499 kHz, PLL mode 500 kHz–128 MHz; the reusable counter object of the lab. |
| `SquareWaveTest.spin` | 21 | top | Exercises `SquareWave.Freq`. |
| `TestRcDecay.spin` | 64 | top | RC decay measurement, POS detector mode (`ctra[30..26]:=%01000`, `frqa:=1`, `phsa`), PST display. |
| `TestRcDecay (Modified Displays Poll Rate).spin` | 77 | top | Refinement: also display the poll rate. |
| `TestRcDecay (Modified for Concurrent Measurements).spin` | 73 | top | Refinement: two concurrent RC measurements (both counter modules). |
| `LedDutySweep.spin` | 29 | top | D/A via **DUTY mode** — sweep LED brightness. |
| `LedSweepWithSpr.spin` | 27 | top | Same using **special-purpose-register** (`spr[]`) access. |
| `DAC 2 Channel.spin` | 37 | library | 2-channel DAC via DUTY modes (3 PUB methods). |
| `Test DAC 2 Channel.spin` | 20 | top | Exercises the 2-channel DAC object. |
| `DualDac.spin` | 149 | library | Full dual-DAC driver (6 PUB / 2 PRI) — largest example. |
| `TestDualDAC.spin` | 70 | top | Exercises `DualDac`. |
| `DoReMi.spin` | 36 | top | NCO speaker tones — play a musical scale. |
| `Staccato.spin` | 24 | top | NCO tone with on/off articulation. |
| `TwoTones.spin` | 41 | top | Two simultaneous tones (both counters). |
| `TwoTonesWithSquareWave.spin` | 33 | top | Same, built on the `SquareWave` object. |
| `TerminalFrequencies.spin` | 63 | top | Enter a frequency in PST → synthesize it (3 PUB). |
| `IrDetector.spin` | 44 | library | Modulated-IR object detection driver (NCO + DUTY, 2 PUB). |
| `IrObjectDetection.spin` | 43 | top | IR object-presence detection application. |
| `TestIrDutyDistanceDetector.spin` | 35 | top | IR *distance* detection via duty/NCO. |
| `CountEdgeTest.spin` | 42 | top | POSEDGE/NEGEDGE transition counting. |
| `BetterCountEdges.spin` | 35 | top | Refinement: improved edge-count method. |
| `SinglePulseWithCounter.spin` | 22 | top | Generate a single timed pulse with a counter. |
| `SinglePwm with Time Increments.spin` | 29 | top | Single PWM signal parameterized by time increments. |
| `1Hz25PercentDutyCycle.spin` | 26 | top | NCO/PWM: 1 Hz, 25% duty. |
| `1Hz25PercentDutyCycleDiffSig.spin` | 29 | top | Refinement: differential-signal version. |
| `TestDualPWM.spin` | 34 | top | Two PWM signals from one cog's two counters. |
| `TestDualPWM (Project 2).spin` | 55 | top | Project variant of dual PWM. |
| `TestDualPWM(Exercise 12).spin` | 37 | top | Exercise variant of dual PWM. |
| `TestDualPwmWithProbes.spin` | 61 | top | Dual PWM + a probe object/cog to measure it. |
| `MonitorPWM.spin` | 103 | library | Measure/monitor an incoming PWM signal (3 PUB / 1 PRI). |
| `TestPllParameters.spin` | 52 | top | PLL-mode high-frequency parameter exploration. |
| `CalibrateMetalDetector.spin` | 71 | top | LC metal detector: PLL + POS detector, calibration + display. |

---

### Cross-lab observations
- **Progressive-refinement lineages are explicit in filenames** (`…`, `…Again`, `…WithCogs`,
  `…WithOffsets`, `…50Percent`, `Modified for …`). See the reference's Pattern Profile §E.
- **`Test…` top objects pair with same-named library objects** (`TestSquareWaveMethod`↔`SquareWave`,
  `TestBs2IoLiteObject`↔`Bs2IoLite`, `Test DAC 2 Channel`↔`DAC 2 Channel`, `TestDualDAC`↔`DualDac`).
- **Counter-module idioms (`ctra/ctrb`, `frqa/frqb`, `phsa/phsb`, mode bit-fields `[30..26]`)** are the
  dominant P1-specific surface in Lab 7 — the prime **smart-pin reshape** target for the P2 labs book.
- **External library objects referenced but NOT in this archive:** `Parallax Serial Terminal.spin`
  (Propeller Library; printed in full in the book's Appendix A), `Float`/`FloatString` (Propeller
  Library). These ship with the Propeller Tool, not the lab archive — captured as a knowledge note, not
  a missing file.
