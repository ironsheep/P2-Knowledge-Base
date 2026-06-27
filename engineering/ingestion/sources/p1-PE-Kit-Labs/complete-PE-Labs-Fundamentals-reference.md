# Propeller Education Kit Labs: Fundamentals — Curated Reference

**Source:** Parallax #122-32305, *Propeller Education Kit Labs: Fundamentals*, Version 1.2 (web release 2)
**Author:** Andy Lindsay (Parallax Inc.)
**ISBN:** 9781928982555 · build tag `1.2.0-10.07.12-HKTP`
**Copyright:** © 2006–2010 Parallax Inc.
**Platform:** Propeller 1 (**P8X32A**), Spin1 language, 40-Pin DIP "PE Platform" (Propeller Education Kit)
**Length:** 233 pages · 115 figures · 15 tables · 89 companion `.spin` example files
**Ingested:** 2026-06-27 (passes 1–5; PDF-only ladder; `pdf2md`/`pdftotext -layout` + `pdfimages` + `image-tools-mcp`)

> **Why this ingestion matters (downstream purpose):** This book is the *template* for a planned
> **P2 equivalent labs book with reshaped experiments**. The headline deliverable is therefore the
> **Document Pattern Profile** (last section), which captures the book's pedagogical structure and
> voice so the P2 labs book can inherit its proven teaching arc. Facts here are P1; the value is the
> *pattern*.

---

## 1. Document Map (table of contents)

| # | Chapter / Lab | Printed pp | Role |
|---|---------------|-----------|------|
| 1 | **Propeller Microcontroller & Labs Overview** | 7–16 | Architecture orientation (cogs, hub, Spin, objects, cog launching, loading RAM/EEPROM); PE Kit hardware tour; how the labs are organized |
| 2 | **Software, Documentation & Resources** | 17–18 | Download/install Propeller Tool + Parallax Serial Terminal; web sites; tech support |
| 3 | **Setup and Testing Lab for 40-Pin DIP PE Platform** | 19–44 | Hardware-build lab: inventory parts → assemble breadboards → wire power/regulators → test wiring → socket Propeller + EEPROM → load a test program → test I/O pins → regulation notes → troubleshooting |
| 4 | **I/O and Timing Basics Lab** | 45–68 | `dira`/`outa`/`ina` registers, group I/O, input→output, `waitcnt`/`cnt` timing, clock config (`_clkmode`/`_xinfreq`/PLL), operators, conditional `repeat`, shift displays, variables, timekeeping |
| 5 | **Methods and Cogs Lab** | 69–82 | Methods (local vars, parameters, `result`), calling methods, launching methods into cogs with `cognew`, stack sizing, `cogid`/`cognew`/`cogstop` |
| 6 | **Objects Lab** | 83–124 | Multi-object applications, dot notation, objects that launch cogs, Start/Stop conventions, documentation comments, PUB vs PRI, multiple instances, **PC terminal comms (Parallax Serial Terminal)**, DAT block + address passing, Float/FloatString, variable-address passing |
| 7 | **Counter Modules and Circuit Applications Lab** | 125–190 | The two per-cog **counter modules** (CTRA/CTRB, PHS/FRQ/CTR regs): RC decay sensing (POS detector), D/A via DUTY modes, NCO speaker tones, IR object/distance detection, edge counting (POSEDGE/NEGEDGE), PWM with NCO, PLL high-freq modes, LC metal detection |
| A | **Appendix A: Object Code Listings** | 191–200 | Full listings of `Parallax Serial Terminal.spin` and `SquareWave.spin` |
| B | **Appendix B: Study Solutions** | 201–223 | Answers to every lab's Questions / Exercises / Projects |
| C | **Appendix C: PE Kit Components Listing** | 224–225 | Master parts/components tables |
| D | **Appendix D: Propeller P8X32A Block Diagram** | 226 | Architecture reference figure |
| E | **Appendix E: LM2940CT-5.0 Current Limit Calculations** | 227–228 | Voltage-regulator engineering note |
| — | **Index** | 229–233 | |

Front matter (pp i–iv before printed p5): cover, Warranty / 14-day guarantee, Copyrights & Trademarks, Disclaimer, Discussion Lists, Errata, Table of Contents. **Preface** at p5.

---

## 2. Platform & Hardware (P1 facts)

**The PE Platform** = interlocking breadboards carrying a Propeller P8X32A microcontroller system. Two
build variants:
- **40-Pin DIP version** — every part/circuit plugged directly into breadboard (cheap to repair part-by-part; the focus of this text).
- **PropStick USB version** — a PCB module with surface-mount parts (faster to wire, costlier to replace). Has its own separate Setup & Testing lab (free download).

**On-board system** (Figure 3-2 components): Propeller P8X32A (40-pin DIP), 5.0 V and 3.3 V voltage
regulators, 32 KB EEPROM for non-volatile storage, **5.00 MHz external crystal**, reset button, LED
power indicator, 9 V battery-to-breadboard connector, serial-to-USB (Propeller Plug) for download +
bidirectional PC comms.

**Propeller P8X32A core facts** (as taught): 8 cogs (32-bit processors), 32 KB global hub RAM, 32 KB
ROM, each cog has 2 KB RAM + can run a Spin interpreter (from ROM) *or* a PASM program; each cog has
full access to all 32 I/O pins; **two counter modules per cog**. Supply 3.3 V; I/O high/low referenced
to 3.3 V. Default startup `dira`/`outa` bits = 0 (input). System clock to 80 MHz via `_clkmode =
xtal1 + pll16x`, `_xinfreq = 5_000_000`.

**Key parts tables:** Table 3-1 Breadboard Set (#700-32305) · Table 3-2 Propeller Plug (#32201) ·
Table 3-3 Propeller DIP Plus Kit (130-32305) · Table 7-1 Notes/Frequencies/FRQA-B register values for
80 MHz · Appendix C master components listing.

---

## 3. Per-Lab Content Summary

### Lab 3 — Setup and Testing (40-Pin DIP PE Platform)
Hardware-only lab (no Spin teaching). Procedure: inventory equipment/parts → assemble interlocking
breadboards → set up PE Platform wiring + voltage regulators → test the wiring → socket the Propeller
chip + EEPROM → load a test program (`PushbuttonLedTest`) and test I/O pins → "before changing
circuits" cautions → **"Propeller Supply Voltage Regulation — It's Important!"** → troubleshooting
table. Companion code: `DoNothing.spin` (empty `PUB main` to blank the chip) and
`PushbuttonLedTest-v1.0.spin`. Heavy on **wiring diagrams + build photos** (the only lab that provides
wiring diagrams; later labs give schematics only).

### Lab 4 — I/O and Timing Basics
Builds the foundational vocabulary. Progression of example apps (each introduces a technique):
LED on (`dira`/`outa` single bit) → groups of LEDs (`%111111` group writes, `dira[4..9]`) →
pushbutton→LED (`ina` read, condition) → group pushbutton→LED (parallel I/O) → synchronized on/off
(`waitcnt(clkfreq/4 + cnt)`) → clock config (`_clkmode`/`_xinfreq`/PLL) → display patterns (operators)
→ binary counts (`repeat`, conditional loops, operators) → shifting light display (shift ops) →
shifting display with pushbutton-controlled refresh (global+local vars) → timekeeping (synchronized
event timing independent of other tasks). Teaches `cnt`, `clkfreq`, pre/post operators, `:=` vs `==`,
variable scope/size. **"Study Time"** with 28 Questions, 14 Exercises, 5 Projects.

### Lab 5 — Methods and Cogs
Method mechanics → multiprocessing. Defining a method's behavior with local variables → calling a
method (program-control + parameter passing, Figure 5-2/5-3) → **launching methods into cogs**
(`cognew(Blink(4, clkfreq/3, 9), @stack[0])`, Figure 5-4) → how much stack space (Object Info window,
`Stack Length.spin`) → method calls and the `result` variable → `cogid` indexing. Examples ramp:
`CallBlink` → `BlinkWithParams` → `BlinkWithCogs` (3 cogs blinking at different rates) →
`CogStartStopWithButton`. Study Time at p80.

### Lab 6 — Objects
The transition from single-object to **multi-object architecture**. Method-call review → calling
methods in *other* objects with **dot notation** (`OBJ` block declaration) → objects that launch
processes into cogs → **Start/Stop method conventions for library objects** (`Start(...) : success`
returns cog+1, `Stop` calls `cogstop`) → documentation comments (`{{ }}` doc blocks, schematic-in-comment
using the Parallax font) → **PUB vs PRI** → multiple object instances → **Propeller↔PC terminal comms
with the Parallax Serial Terminal object** (`pst.Start(115_200)`, `pst.Str`, `pst.Dec`, `pst.Char`) →
sending values from PST to the Propeller → terminal input-state display / LED output control → **DAT
block + address passing** → Float & FloatString objects → objects that use variable addresses → passing
starting addresses to objects working on variable lists. Library objects authored here: `Blinker`
(cog manager), `Button`, `Bs2IoLite`. Study Time at p120.

### Lab 7 — Counter Modules and Circuit Applications
The capstone: the per-cog **counter modules**. Teaches PHS/FRQ/CTR register roles and 10 of the 32
counter modes across 8 task families:
- **RC decay** measurement with POS detector mode (potentiometer/phototransistor sensing) — `TestRcDecay`
- **D/A conversion** controlling LED brightness with DUTY modes — `LedDutySweep`, `DAC 2 Channel`, `DualDac`
- **NCO mode** speaker tones (audio range) — `DoReMi`, `Staccato`, `TwoTones`
- **NCO modulated IR** for object + distance detection — `IrDetector`, `IrObjectDetection`
- **POSEDGE/NEGEDGE** transition counting — `CountEdgeTest`, `BetterCountEdges`
- **PWM** with NCO modes — `TestDualPWM`, `MonitorPWM`, probe & display PWM
- **PLL modes** for high-frequency — `TestPllParameters`
- **LC metal detection** with PLL + POS detector — `CalibrateMetalDetector`
Library object authored here: `SquareWave.spin` (NCO 0–499 kHz / PLL 500 kHz–128 MHz frequency
synthesis). Uses oscilloscope screenshots (Figures 7-27/7-28) and scope/terminal output throughout.
Study Time at p185.

---

## 4. Recurring Spin1 / P1 idioms taught (for P1→P2 reshaping reference)

| P1 idiom (this book) | What it does | P2 reshape target |
|---|---|---|
| `dira[4..9] := %111111` / `outa[pin]~~` | I/O direction + output register bits | `pinh`/`pinl`/`drvh`, `dirh`, smart-pin or direct register |
| `waitcnt(clkfreq/4 + cnt)` | delay relative to system tick counter `cnt` | `waitct()`, `getct()`, `pollct()` |
| `_clkmode = xtal1 + pll16x` / `_xinfreq = 5_000_000` | 5 MHz xtal × PLL → 80 MHz | `_clkfreq`/`_xtlfreq` + P2 PLL |
| `cognew(Method(args), @stack[0])` | launch Spin method into a cog | `coginit`/`cognew` (Spin2) — same model |
| `ctra[30..26] := %01000` / `frqa` / `phsa` | counter module mode + frequency/phase regs | **smart pins** (replace nearly all CTRA/CTRB uses) |
| NCO mode square wave | numerically-controlled oscillator on a pin | smart pin NCO/transition modes |
| DUTY mode D/A (LED brightness) | counter PWM/duty for analog out | smart pin DAC modes / PWM modes |
| PLL mode high-freq | counter PLL frequency synthesis | smart pin / PLL |
| RC decay timing (POS detector) | charge cap, time discharge | smart pin time/pulse measurement modes |
| `pst.Start(115_200)` / Parallax Serial Terminal object | PC serial terminal I/O | `DEBUG`/serial in Spin2 + (P2) terminal |

---

## DOCUMENT PATTERN PROFILE
*(the headline deliverable — the reusable template for the planned P2 labs book)*

### A. Front / back matter structure
- **Front matter** (boilerplate, pp i–iv): Warranty · 14-Day Money-Back Guarantee · Copyrights &
  Trademarks (with educational-duplication grant) · ISBN/build tag · Disclaimer of Liability ·
  Internet Discussion Lists · Errata notice · Table of Contents.
- **Preface** (p5): sets audience + how to use the book.
- **Two orientation chapters before any lab:** Ch 1 *Overview* (architecture + hardware tour + "here's
  how the labs are organized") and Ch 2 *Software/Docs/Resources* (get the tools installed). Labs do
  not start until the reader is oriented and tooled.
- **Back matter:** Appendix A *full object code listings* (the long reusable library objects, printed
  in full so the book is self-contained) · Appendix B *Study Solutions* (every Question/Exercise/Project
  answered) · Appendix C *components listing* · Appendix D *block diagram* · Appendix E *engineering
  note* (regulator math) · Index.

### B. The recurring per-lab template (the exact slot sequence)
Each of the four teaching labs (4–7) follows this sequence. Name every slot:
1. **`Introduction`** — motivates the lab ("most microcontroller applications involve…"), then a
   **bulleted list of the lab's example applications, each paired with the coding technique it
   introduces.** This list *is* the lab's roadmap and the spine of the narrative.
2. **`Prerequisite Labs`** — explicit list of which earlier labs must be done first (cumulative:
   Lab 7 lists all four priors). Enforces the build-on-prior arc.
3. **`Parts List and Schematic`** (a.k.a. "Equipment, Parts, Schematic") — bulleted parts list with
   quantities + values, then **"► Build the schematic shown in Figure N-1."** Lab 7 repeats a smaller
   *Parts List / Schematic* pair per circuit family (RC, DUTY, NCO, IR, PWM, PLL, LC) inline.
4. **Teaching sections** (repeated N times — the body) — each is a **concept heading → code listing →
   "How <Filename>.spin Works" narration**:
   - A descriptive heading naming the concept ("Lights on with Direction and Output Register Bits").
   - A short prose lead-in naming the example object and what it makes the hardware do.
   - **An action bullet** with a ► glyph giving the literal Propeller-Tool step
     ("► Load LedOnP4 into RAM by clicking Run → Compile Current → Load RAM (or press F10)").
   - **The code listing** (with the standard `'' File: X.spin` header comment).
   - **A "How <Filename>.spin Works" subsection** narrating the code line-by-line / concept-by-concept.
   - Frequent **inline figures**: schematic, timing diagram (e.g. Figure 4-3 *waitcnt and the cnt
     register*), Object-Info-window screenshot, or terminal/scope screenshot.
5. **`Study Time`** (closes every teaching lab; "Solutions begin on page NNN.") — three graded
   sub-slots, always in this order:
   - **`Questions`** — comprehension recall (the Lab-4 set has 28). Conceptual, no coding.
   - **`Exercises`** — short "write a line/method that does X" coding drills (Lab-4 set has 14).
   - **`Projects`** — larger open-ended builds combining the lab's techniques (Lab-4 set has 5, e.g.
     a street-light controller, an alarm-clock minute-setter). Several **reappear as later labs'
     example apps**, i.e. projects foreshadow future content.
   All answers live in **Appendix B**, keyed by lab + sub-slot.

   *(Lab 3 is the exception — a pure hardware build-and-test lab with no Introduction-roadmap / Study
   Time; its slots are: PE Platform tour → Procedure Overview → Inventory → Assemble → Wire → Test →
   Socket ICs → Load test program → cautions → Troubleshooting.)*

### C. The narrative arc across the five labs
A deliberate capability ramp where each lab consumes the prior as a building block:
- **Setup & Testing** → a working, tested board (prerequisite for everything).
- **I/O & Timing** → the *single-object, single-method, single-cog* vocabulary (registers, timing,
  operators, variables). "The examples in this lab only involve single, top-level objects with just
  one method."
- **Methods & Cogs** → decompose into methods, then *parallelize* by launching methods into cogs.
- **Objects** → compose *multiple objects* (dot notation, library objects, Start/Stop conventions,
  PC terminal comms) — the software-architecture lab.
- **Counter Modules & Circuit Applications** → the hardware-capability capstone: offload timing-precise
  work to counter modules while cogs run, applied to real circuits (sensors, audio, IR, PWM, metal
  detection). Pulls together cogs + objects + timing + new peripheral.
The arc moves **bit → method → cog → object → peripheral**, and **software-only → software+circuits**.

### D. Voice / register / pedagogy
- **Second person, imperative for actions; explanatory third person for concepts.** Reader actions are
  set off with a **► action glyph** ("► Click the Documentation radio button…", "► Load … press F10").
  Concept narration is calm, declarative, analogy-friendly ("The Propeller is like a super-microcontroller
  with eight high-speed 32-bit processors inside").
- **Motivate-then-mechanism.** Every lab and most sections open with *why this matters in real
  applications* before the *how*. Counter intro: lists 8 real services counters provide before any code.
- **"How it works" is a named, recurring contract.** After each example the book stops and explains the
  code it just showed — never "code dump and move on."
- **Scaffolds difficulty by progressive refinement, not by jumping.** New capability is added one step
  at a time to a familiar example (see E).
- **Challenges are graded (Questions → Exercises → Projects)** and **answered in an appendix**, so the
  book supports self-study and classroom use equally (it states "hand-enter the code examples as you go…
  it'll give your mind time to consider each line").
- **Glossary-on-first-need.** "Propeller Nomenclature" (cog/Spin/method/object/variable) appears inside
  Lab 4 right where the terms are first load-bearing, not front-loaded.

### E. Example-naming + progressive-refinement style
Examples are named in **CamelCase after what they do**, and refined by **suffixing a delta word** so the
lineage is visible in the filename:
- `LedOnP4` → `LedOnOffP4` → `LedsOnOff` → `LedsOnOffAgain` → `LedsOnOff50Percent` → `LedsOnOff50PercentAgain`
- `CallBlink` → `BlinkWithParams` → `BlinkWithCogs` → `AnotherBlinker`
- `AddressBlinker` → `AddressBlinkerWithOffsets` → `AddressBlinkerControl` → `AddressBlinkerControlWithOffsets`
- `TestRcDecay` → `TestRcDecay (Modified Displays Poll Rate)` → `TestRcDecay (Modified for Concurrent Measurements)`
- `TwoTones` → `TwoTonesWithSquareWave`; `TestDualPWM` → `TestDualPWM (Project 2)` / `TestDualPWM(Exercise 12)`
The suffix (`Again`, `WithCogs`, `WithParams`, `WithOffsets`, `50Percent`, `Modified for …`) names the
single concept added. "Test…" prefixes a top object that exercises a separate library object of the
matching name (`TestSquareWaveMethod` ↔ `SquareWave`, `TestBs2IoLiteObject` ↔ `Bs2IoLite`).

### F. Media-usage pattern (how each medium is deployed in the teaching flow)
- **Parts lists** — bulleted, quantity-first, with component values; immediately followed by a "build
  the schematic" action. Co-located with the schematic as a *Parts List | Schematic* pair (often a
  two-column layout, repeated per circuit family in Lab 7).
- **Schematics** — the *circuit* representation used in all teaching labs (Labs 4–7). Drawn in the
  Propeller-Tool Parallax font in Lab 6 onward to model good object documentation. **The reader is
  expected to build from schematics** (only Setup & Testing gives wiring diagrams).
- **Wiring diagrams + build photos** — used **only** in the hardware Setup & Testing lab, where physical
  placement matters (breadboard layout, supply-strap/filter-cap close-ups, IC socketing). These are the
  "do exactly this with your hands" medium.
- **Code listings** — inline, with the standard `'' File:` header; long reusable objects (Parallax
  Serial Terminal, SquareWave) are excerpted inline but printed in full in Appendix A.
- **Screenshots** — Object Info window (stack/memory teaching), Propeller-Tool documentation view (doc
  comments), and **Parallax Serial Terminal** output (the primary "see your program's result" medium
  from Lab 6 on).
- **Scope/measurement captures** — oscilloscope screenshots (Lab 7) to show real analog/timing behavior
  the counter modules produce.
- **Conceptual diagrams** — architecture (Ch 1), and per-mechanism explainers (the `waitcnt`/`cnt`
  timing diagram, method-call/parameter-passing diagrams, dot-notation diagram, CTRA/B register maps,
  eddy-current physics for the metal detector).

### G. Actionable take for the P2 labs book
Inherit verbatim: the **per-lab slot template** (Intro-roadmap → Prereqs → Parts/Schematic → concept→code→"how it works" → Study Time{Questions/Exercises/Projects}), the **► action-glyph** convention,
the **progressive-refinement example-naming**, the **Appendix-B answer key**, and the **bit→method→cog→object→peripheral** arc. Re-target the *peripheral* capstone from **counter modules to smart pins**, the
platform from the **40-pin DIP PE Platform to a P2 Edge/eval board**, terminal I/O from **Parallax
Serial Terminal to Spin2 `DEBUG`**, and redraw all schematics in **TikZ/circuitikz** while **shooting
new breadboard/wiring photos** of the P2 environment (the original build photos are the reference for
those shoots).
