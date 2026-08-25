# Source Errata — where our sources are wrong, and what we established instead

> Backing doc **#5** of the ingestion set (README dashboard · `AUTHORITATIVE-SOURCES` ·
> `DOCUMENT-LINEAGE` · `KNOWLEDGE-GAPS` · **this**). Standing register, created 2026-08-25.
>
> **Next erratum ID: `E-011`**

## What this register is for

**A source says something wrong. We research it. What we establish becomes a trusted fact —
citable, and the thing the KB and the manuals are built on.** All three stages live in one row, so
the chain from *"the guide is wrong"* to *"here is what is true, and here is why"* never sits in
someone's head or in a closed conversation.

**An erratum is not a complaint, it is the start of a fact.** The value is not in cataloguing
Parallax's mistakes — it is that each one forces a question to be settled, and a settled question
outlives the document that got it wrong.

Three registers, three questions. **The test: if Parallax fixed their document tomorrow, would this
entry disappear?** Yes → erratum. No → our correction, or a gap.

| Register | Answers | Disposition |
|---|---|---|
| `operations/P2KB-CORRECTION-FINDINGS.md` | what is wrong in **our** shipped KB | fix it here |
| `KNOWLEDGE-GAPS.md` | what **no source** tells us | fill it, or ask an expert |
| **this** | what a **source document** gets wrong | **research it; record what is true** |

## Every entry cites all sides, in each document's own terms

An entry is only useful if you can **open the actual document and point at the sentence**. So each
one carries a **competing-claims table**: every side, with

- the **document and edition**,
- **where it lives in that document** — the section heading, table, or page a reader can navigate
  to. This is the locator to quote when confirming with Parallax;
- the **verbatim sentence**;
- our **extraction locator** (`file:line`), which is *ours*, for re-verification only — never quote
  it outside this project.

Where a claim has no navigable locator (OCR text with no headings), that is said, so nobody
presents a guess as a citation.

## Lifecycle

```
OPEN  ──►  RESEARCHING  ──►  RESOLVED   the fact is established; cite E-NNN
                         └►  GAP        not settleable from what we hold; what would settle it is
                                        named, and it also lands in KNOWLEDGE-GAPS Part B
```

**`RESOLVED` carries OUR FINDING** — one statement of what is true, with the evidence behind it.
That statement is a trusted fact and may be cited in shipped YAML and manual prose as
`SOURCE-ERRATA.md E-NNN`, the way an empirical result is cited as `EF-NNN`.

**Where it sits in the authority order.** A resolved erratum is **adjudication, not a new primary
source.** It ranks by the evidence behind it, never above it:

- settled on the **bench** → it is an empirical finding. Record it in `P2-EMPIRICAL-FINDINGS.md` as
  `EF-NNN`; this row cites that rather than becoming a second home for the same fact.
- settled by **another Parallax document**, or by **the document contradicting itself** → cite the
  documentary source; this row records the adjudication and why the outlier loses.
- settled by **`pnut-ts`** → legality only, never semantics.

`E-NNN` is a **pointer with the reasoning attached**, and the reasoning is the part that exists
nowhere else. It is never licence to state a fact no evidence supports — that is a `GAP`.

## Rules

- **Never edit an ingested source to "fix" an erratum.** The capture is evidence; editing it
  rewrites the basis of every finding that cites it.
- **Distinguish OUR extraction defect from THEIR document defect.** Check the **original capture**,
  not the derived summary — E-006 was filed only after confirming the contradiction is verbatim in
  the 2020-edition text.
- **`Reached our KB?` is mandatory** — follows / diverges / never carried. That column is the map of
  where this project knowingly departs from Parallax.
- **A row closes on `RESOLVED`, not on "reported".** If a later edition fixes the document, note it;
  that triggers a re-ingestion check.
- **`OUR FINDING` is one statement, not a discussion.** If it needs hedging, it is not resolved.

---

## Index

| # | Document | In one line | Reached our KB? | State |
|---|---|---|---|---|
| E-001 | P2 Hardware Manual | `COGATN` constant lost its `%` and does not assemble | never carried | `RESOLVED` |
| E-002 | P2 Hardware Manual | `ROLBYTE y,x` — no such two-operand form | never carried | `RESOLVED` |
| E-003 | P2 Hardware Manual | VCO "kept within 350 MHz" contradicts its own PLL Example | follows the majority | `RESOLVED` |
| E-004 | #64013 RTC Add-on Guide | pull-up mislabel, prescribed in input mode where it cannot work | diverged; **KB fixed 2026-08-25** | `RESOLVED` |
| E-005 | #64000 Eval Board Rev C Guide | §18 reverses the SPI/SD pin directions | never carried | `RESOLVED` |
| E-006 | #64006 Eval Add-on Guide | button "active-high" *and* "driven low when asserted" | ⚠️ **diverges** | `RESEARCHING` |
| E-007 | Hardware Manual vs Datasheet | clock limits — recommended-use vs absolute-limit framing | follows, unlabelled | `RESOLVED` |
| E-008 | #64010 Universal Motor Driver Guide | pin-definitions table duplicates channel X on offsets 9/8 and omits channel U | never carried | `RESOLVED` |
| E-009 | #64000 Eval Board Rev C Guide | board size printed as "3.55″ × 3.55″ (90 x 90 cm)" — the metric unit is wrong | never carried | `RESOLVED` |
| E-010 | P2 Edge Module (#P2-EC) v3.0 **and** P2-EC32MB Rev B v2.0 | "have I/O pin **pull-ups** activated" — the P2 has none; they are drive strengths, live only with DIR high | ⚠️ **diverges** — carried verbatim in **both** `hardware/` Edge YAMLs | `CONFIRMED` |

---

## E-001 — `COGATN` constant lost its `%` · `RESOLVED`

| Side | Document @ edition | Where in that document | Verbatim | Our locator |
|---|---|---|---|---|
| The claim | **P2 Hardware Manual**, 2022-11-01 | §**Cog Attention** (Heading 2) | `COGATN   #00001100` — commented *"Get attention of cogs 2 and 3"* | `sources/p2-hardware-manual/p2-hardware-manual-text.txt:481` (section) |
| Against | **`pnut-ts` v1.55.3** | assembling the line as printed | *Constant must be from 0 to 511 (m130)* | — |

**OUR FINDING.** The intended constant is **`%00001100`** (bits 2 and 3 = 12), matching the code's
own comment. As printed, `#00001100` is **decimal 1,100** and out of range. **A `%` is missing.**

**Evidence tier:** `pnut-ts` legality. Confirmed verbatim in the DOCX `word/document.xml`, so it is
the document's defect and not an extraction artifact. · **Reached our KB?** Never carried.

## E-002 — `ROLBYTE y,x` has no legal form · `RESOLVED`

| Side | Document @ edition | Where in that document | Verbatim | Our locator |
|---|---|---|---|---|
| The claim | **P2 Hardware Manual**, 2022-11-01 | §**SCOPE Data Pipe** (Heading 4) — 4 occurrences | `ROLBYTE y,x` | `p2-hardware-manual-text.txt:1460` (section) |
| Against | **P2 Instructions v35** | rows 94 / 95 | the only forms are `ROLBYTE D,{#}S,#N` and the `ALTGB`-alias `ROLBYTE D` | — |
| Against | **`pnut-ts` v1.55.3** | assembling the 2-operand form | *Expected ","* | — |

**OUR FINDING.** The intended form is **`ROLBYTE y,x,#0`** — fixed by the block's own comments
(*"rotate pinN byte into y"*, reading the `RDPIN` lower byte).

**Evidence tier:** `pnut-ts` legality + the instruction table. Verbatim in `word/document.xml`. ·
**Reached our KB?** Never carried.

## E-003 — the VCO note contradicts the manual's own PLL Example · `RESOLVED`

**This is the strongest kind to raise: the document disagrees with itself, and the other two
Parallax documents side against the outlier.**

| Side | Document @ edition | Where in that document | Verbatim | Our locator |
|---|---|---|---|---|
| **Outlier** | **P2 Hardware Manual**, 2022-11-01 | **Table 10**, the `%MMMMMMMMMM` row of the `HUBSET ##%0000_000E_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS 'set clock mode` table | *"The VCO frequency should be kept within 100 MHz to **350 MHz**."* | `p2-hardware-manual-text.txt:574` |
| **Same manual** | **P2 Hardware Manual**, 2022-11-01 | §**PLL Example** (Heading 3) | *"The PLL's VCO is designed to run between 100 MHz and **200 MHz** and should be kept within that range."* | `:603` |
| Agrees | **P2 Datasheet** (P2X8C4M64P), 2022-11-01 | **p.18** | *"…frequency should be kept within 100 MHz to **200 MHz**."* | `p2-datasheet-text.txt:793` |
| Agrees | **P2 Datasheet**, 2022-11-01 | **p.19**, §PLL Example | *"…designed to run between 100 MHz and **200 MHz** and should be kept within that range."* | `:850` |
| Agrees | **Propeller 2 Documentation** v35 Rev B/C | §**PLL Example** | same sentence, **200 MHz** | `silicon-doc/p2-documentation.txt:6233` |
| Context | **Propeller 2 Documentation** v35 Rev B/C | the `%PPPP` row, immediately after | *"For fastest **overclocking**, the PLL can be pushed to 350 MHz using the 'VCO / 1' mode (%PPPP = 15)."* | — |

**OUR FINDING.** The recommended VCO range is **100–200 MHz**. **350 MHz is the VCO/1 overclock
ceiling, not a recommendation** — the manual's Table 10 note substituted the ceiling into the
recommendation sentence. (Spin2 v51's clock solver also carries 350 MHz as its *upper bound*, which
is a third context in which the number is legitimate.)

**Evidence tier:** self-contradiction — needs no external authority — corroborated by two other
Parallax documents, each stating it twice. · **Reached our KB?** Follows the 100–200 MHz majority.

## E-004 — the pull-up mislabel, in a Parallax guide, prescribed where it cannot work · `RESOLVED`

| Side | Document @ edition | Where in that document | Verbatim | Our locator |
|---|---|---|---|---|
| The claim | **#64013 P2 RTC Add-on Board Guide**, v1.0 | §**Code Tip** (under *"The SCL, INT and CLKOUT functions share a single IO pin"*) | *"To use the I2C SCL function, set the I2C **output mode** to use **3.3 k-ohm pull-up**."* and *"…set the P2 Smartpin (or equivalent) **input mode** to **150 k-ohm pull-up**."* | `sources/P2-RTC-Add-on/P2-RTC-Add-on-text.txt:74-77` |
| Against | **Spin2 v55** built-in symbols table | the `P_HIGH_150K` row | *"Drive high 150kΩ"* — a **drive strength**, not a resistor | `sources/spin2-v55/spin2-v55-text.txt:1505` |
| Against | **P2 Datasheet**, 2022-11-01 | **p.24**, Pin Mode legend | *"DIR = direction bit; 0: input (float), 1: output (drive)"* | `p2-datasheet-text.txt:1144` |
| Against (mechanism, incidental) | **P2-EMPIRICAL-FINDINGS** | **EF-063 / EF-064** | *"P8..P31 held at a 15 kΩ low with `DIR` **high**"* — real silicon, so the drive-with-DIR-high mechanism demonstrably works. ⚠️ **These are NOT pull-up findings.** EF-063 certifies jumper continuity; EF-064 establishes streamer pin placement. The weak drive is their **rig apparatus**, not their subject, and the ledger holds **no** dedicated drive-strength finding. Corroboration, never the authority. | `external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md:827,840` |

**OUR FINDING.** Wrong twice. **(1) The P2 has no pull-up resistors** — `P_HIGH_150K` selects a
150 kΩ *drive strength*. **(2) Input mode means `DIR` low, and a drive selection is inactive while
the pin is an input**, so the second tip cannot work on its own terms. The working form is
`P_HIGH_150K` with **DIR high**.

**Evidence tier:** empirical (strongest), corroborated documentarily. · **Reached our KB?**
**Diverged; fixed 2026-08-25 by «#307».** `deliverables/ai/P2/hardware/addon-rtc.yaml`
`pin_mode_tip` no longer repeats the guide. It is now a map carrying (a) the board fact — SCL, INT
and CLKOUT share the single +0 pin, so only one can be in use at a time; (b) the working P2-side
mechanism — **`P_HIGH_150K` with `DIR` HIGH**, so the pin drives high through 150 kΩ, weak enough
for the RTC's open-drain output to pull low while `IN` still reports the pin state; and (c) an
explicit `do_not_copy_the_guides_wording` key quoting the guide's *"input mode to 150 k-ohm
pull-up"* and stating both errors, pointing here. The same block also records a **second, milder
mismatch this fix surfaced**: the Code Tip's companion *"3.3 k-ohm pull-up"* for SCL names a value
the P2 drive ladder does not carry at all — its drive-high rungs are FAST (30 mA), 1.5 kΩ, 15 kΩ,
150 kΩ, 1 mA, 100 µA, 10 µA and float (`sources/spin2-v55/spin2-v55-text.txt:1500-1509`) — and it
carries a GAP: the #64013 guide does not say whether the RTC board provides its own SDA/SCL
pull-ups, and no ingested source does either; the board schematic would settle it. Two prose
mentions of the driver library's "3.3K pull-up" setting elsewhere in the same file were relabelled
so they cannot be read as a P2 capability. Filed to the corrections register as part of **F-353**.

## E-005 — §18 reverses the SPI/SD pin directions · `RESOLVED`

| Side | Document @ edition | Where in that document | Verbatim | Our locator |
|---|---|---|---|---|
| The claim | **#64000 P2 Eval Board Rev C Guide** | **§18** | states the P58/P59 directions the other way round | — |
| Against | **P2 boot ROM listing** v33_01j | the pin-equate block | `spi_di = 59 (also sd_di)` · `spi_do = 58 (also sd_do)` | `sources/rom-booter/rom_booter_v33_01j.lst:135-138` |
| Against | **Propeller 2 Documentation** v35 Rev B/C | the boot-pattern table | agrees on P58/P59, and shows both `CSn (input)` and `CLK (input)` roles per boot source | `silicon-doc/p2-documentation.txt:9281-9302` |

**OUR FINDING.** **P58 = MISO** (card DO → P2 input); **P59 = MOSI** (card DI ← P2 output).
**Never cite §18 for these directions.**

> 🔴 **And do not carry a companion error while fixing this one.** P58/P59 hold their roles across
> both boot sources, but **P60 and P61 SWAP** depending on which one you are booting:
> **Flash SPI — P61 = CSn, P60 = CLK. SD — P61 = CLK, P60 = CSn.** The ROM booter states both in one
> line each: `spi_cs = 61  'also sd_ck` and `spi_ck = 60  'also sd_cs`
> (`rom_booter_v33_01j.lst:135-136`). Our KB has this right at
> `deliverables/ai/P2/architecture/boot-rom/boot-pattern-selection.yaml:84`. **An earlier draft of
> this very entry stated "P61 = CLK, P60 = CSn" flatly — which is the SD case written as though it
> were universal.** Same trap as the DI/DO note below, one pin pair over.

> *An apparent conflict here dissolved once **DI/DO ≡ MOSI/MISO** was recognised — SD-card
> vocabulary and SPI vocabulary naming the same two wires from opposite ends. It had been filed as
> needing a schematic or the bench; it needed neither. **Look for the vocabulary key before
> escalating a two-source conflict.***

**Evidence tier:** the ROM booter is the authority that actually runs. · **Reached our KB?** Never
carried — the KB was already correct and stands unchanged.

## E-006 — "active-high" and "driven low when asserted", in one sentence · `RESEARCHING`

| Side | Document @ edition | Where in that document | Verbatim | Our locator |
|---|---|---|---|---|
| The claim | **#64006 P2 Eval Add-on Boards Guide**, 2020 ed. | the **Control accessory board** description (*"The Control accessory board includes four push-buttons and four blue LEDs"*). ⚠️ **No navigable heading in the capture — OCR text.** Cite by the paragraph text. | *"Each **active-high** push-button has a 470 Ω series resistor to allow the I/O pin to be **driven low** while the button is asserted."* | `sources/p2-eval-add-on-boards/p2-eval-add-on-boards-2020-edition-ocr-text.txt:45` |
| Same guide | **#64006 …Guide**, 2020 ed. | next paragraph | *"The LEDs are active-high…"* — so the guide does use the term precisely elsewhere | `:47` |
| Our KB says | `hardware/addon-control-board.yaml` | — | *"the I/O pin **reads high** while the button is pressed"* | — |

**OUR FINDING — NOT YET ESTABLISHED.** The two halves cannot both be true, and **which one holds
decides whether generated code tests for high or low.** Our KB resolved it opposite to the guide's
mechanical description.

**Evidence tier:** self-contradiction confirmed verbatim in the **original** capture — not
introduced by our summarisation. Nothing yet settles which half is right. · **Reached our KB?**
⚠️ Diverges. · **See Part B.**

## E-007 — clock limits: a framing difference, not an error · `RESOLVED`

| Side | Document @ edition | Where in that document | Verbatim | Our locator |
|---|---|---|---|---|
| Framing A | **P2 Hardware Manual**, 2022-11-01 | §**Specifications** (Heading 2) | *"10 – 20 MHz crystal (P2 Clock PLL enabled) or 0 to 180 MHz (nominal) clock oscillator"* | `p2-hardware-manual-text.txt:195` (section) |
| Framing B | **P2 Datasheet**, 2022-11-01 | **p.48**, §AC Characteristics | Crystal (XI–XO) **1 / 50 MHz**; Direct drive (into XI) **DC / 200 MHz**; PLL **3.33 / 320 MHz** | `p2-datasheet-text.txt:2188` |

**OUR FINDING.** **Not an error.** The manual states **recommended use**; the datasheet states
**absolute limits**. Both are correct, and a reader taking either as "the range" is misled. **The KB
must label which framing it quotes.** Both agree on **180 MHz @ 105 °C nominal system clock**, so
only the *input* limits need the label.

**Evidence tier:** both documents read directly; no contradiction once the framings are named. ·
**Reached our KB?** Follows — but unlabelled today.

## E-008 — the motor-driver pin table duplicates channel X and loses channel U · `RESOLVED`

| Side | Document @ edition | Where in that document | Verbatim | Our locator |
|---|---|---|---|---|
| The claim | **#64010 Universal Motor Driver P2 Add-on Board Guide**, v2.0 (Rev B) | §**Pin Definitions for the P2 Dual Accessory Header Block 15–8** (p.10 table, last two rows) | pin **9** = `PWM_XH`, "PWM input for X channel High-side MOSFET driver"; pin **8** = `PWM_XL`, "…Low-side…" | `sources/p2-universal-motor-driver/p2-universal-motor-driver-text.txt:637-646` |
| Against (same document) | **#64010 …Guide**, v2.0 | §**1. Dual 2x6 way P2 Accessory Headers** (p.5 header pinout table) | the row reads `PWM_UH` &#124; 9 &#124; 8 &#124; `PWM_UL` | `sources/p2-universal-motor-driver/p2-universal-motor-driver-text.txt:238-244`; recovered table at `complete-p2-universal-motor-driver-content.md:143` |
| Against (same document) | **#64010 …Guide**, v2.0 | §**4. MOSFET Drivers** | *"One driver controls each of the 4 output channels labeled: U, V, W, X"* | `complete-p2-universal-motor-driver-content.md:164` |

**OUR FINDING.** **Offset +9 is `PWM_UH` and offset +8 is `PWM_UL`.** The board has four channels
and eight PWM pins; the p.10 table's last two rows repeat the X-channel labels from its first two
rows, which would leave channel **U** undocumented and channel X documented twice. The p.5 header
pinout is right.

> ⚠️ **This is the SOURCE's defect, not ours — and our own audit says otherwise.**
> `sources/p2-universal-motor-driver/p2-universal-motor-driver-complete-extraction-audit.md:45`
> records it as a *"docling table copy-error"*. It is not: the plain `pdftotext` text layer carries
> the same duplication (`…-text.txt:637-646`), so it is in the PDF. The audit reaches the right
> **answer** (use the U-channel values) for the wrong **reason**, and the reason matters — a
> docling artifact would be fixed by re-extracting, while a source defect never will be. The
> ingestion tree is evidence and was not edited; the ingestion head owns correcting that audit line.

**Evidence tier:** self-contradiction, confirmed in the original text layer as well as in the
recovered tables. · **Reached our KB?** Never carried — `hardware/addon-motor-driver.yaml`
`signal_map` was written from the p.5 pinout and records this erratum in a `pin_label_errata` key.

## E-009 — the eval board's own dimension line prints centimetres for millimetres · `RESOLVED`

| Side | Document @ edition | Where in that document | Verbatim | Our locator |
|---|---|---|---|---|
| The claim | **#64000 Propeller 2 Eval Board Rev C Guide**, v2.0 (29/6/2020) | **p.2**, Key Specifications, *PCB dimensions* row | *"3.55″ × 3.55″ (90 x 90 cm)"* | `sources/p2-eval-board/complete-p2-eval-board-reference.md:62`, errata note at `:302-303` |
| Against (same document) | **#64000 …Guide**, v2.0 | **p.17**, PCB Dimensions drawing | overall width labelled **3.55 in**; the bottom-right chamfer is labelled **1.5748 in = 40.00 mm**, which fixes the drawing's unit scale | `sources/p2-eval-board/complete-p2-eval-board-reference.md:253-266` |

**OUR FINDING.** The board is **3.55 in × 3.55 in ≈ 90 mm × 90 mm**. The parenthetical unit on p.2
is wrong by a factor of ten; 90 cm would be a board nearly a metre across. **Quote the inch figure.**

**Evidence tier:** internal contradiction plus an in-document unit anchor (the 1.5748 in = 40.00 mm
label). · **Reached our KB?** Never carried — `hardware/p2-eval-board.yaml` `specifications.physical`
states the inch figure and carries a `dimensions_note` pointing here.

## E-010 — both Edge Module guides tell the reader to "activate I/O pin pull-ups", and our KB repeats it verbatim · `CONFIRMED`

| Side | Document @ edition | Where in that document | Verbatim | Our locator |
|---|---|---|---|---|
| The claim | **P2 Edge Module (#P2-EC) Product Guide**, v3.0 (2022-06-03) | §**7. LED Buffer** | *"In user code those pins could be driven high or low, or **have I/O pin pull-ups activated**, to control the LEDs without the high-impedance behavior."* | `sources/edge-standard-module/edge-standard-module-narrative.txt:266-267` |
| The claim (again) | **P2-EC32MB Edge Module Rev B Guide**, v2.0 (2022-05-23) | §**7. LED Buffer** | *"In user code those pins could be driven high or low, or **have I/O pin pull-ups activated**, to control the LEDs without the high-impedance behaviour."* | `sources/edge-32mb-module/edge-32mb-module-narrative.txt:313-314` |
| Against | **P2 Datasheet**, 2022-11-01 | **p.24**, (M) Pin Mode table + Pin Mode Legend | The whole field is enumerated — C, I, O, HHH, LLL — and **there is no bias-resistor selector among them**; `HHH`/`LLL` are drive strengths | `p2-datasheet-text.txt:1131-1147` |
| Against | **P2 Datasheet**, 2022-11-01 | **p.24**, Pin Mode Legend | *"DIR = direction bit; 0: input (float), 1: output (drive)"* — a drive selection is inactive while the pin is an input | `p2-datasheet-text.txt:1144` |
| Against | **Spin2 v55** built-in symbols table | the `P_HIGH_15K` row | *"Drive high 15kΩ"* — a **drive strength**, not a resistor | `sources/spin2-v55/spin2-v55-text.txt:1504` |

**OUR FINDING.** Same defect class as **E-004**, in two more Parallax guides. **The P2 has no
pull-up or pull-down resistors to activate.** What exists is a per-side **drive-strength** selector
— eight rungs from FAST through 1.5 kΩ / 15 kΩ / 150 kΩ / 1 mA / 100 µA / 10 µA to float, chosen
independently for the high side (`HHH`) and the low side (`LLL`) — and a selection is live **only
while the pin is driving**, i.e. `DIR` high. So the guide's phrasing offers a third option
("driven high or low, **or** pull-ups activated") where there are only two, and the alternative it
names is the first option under another name. The **substance** of the sentence is fine — you can
hold an Edge LED pin deterministically with a weak drive — and the working form is `P_HIGH_15K`
with `DIR` **high**, exactly the `weak_high` idiom at
`deliverables/ai/P2/architecture/pin-drive-configuration.yaml:203-222`.

*Note the same guides get the neighbouring fact right:* they say the LED pins are *"not impacted by
the presence of the LEDs or **external** pull-up resistors"* — external ones, correctly. It is only
the P2-side capability that is misnamed.

**Evidence tier:** documentary, two agreeing Parallax sources against the guides. · **Reached our
KB?** ⚠️ **YES — diverges, carried verbatim, both files.**
`deliverables/ai/P2/hardware/edge-standard-module.yaml:155` and
`deliverables/ai/P2/hardware/edge-32mb-module.yaml:171` both end their `led_pins.mechanism` with
*"Drive the pins high or low (**or enable a pin pull-up**) to control the LEDs deterministically."*
Faithful ingestion of a wrong sentence. This is **not** covered by F-321, whose applied sweep was
scoped to `language/` — these are `hardware/` files, and the phrase carries no `P_*` constant, so
`audit-constant-fidelity.py` cannot see it either. Routed to the corrections register alongside
**F-356**, which records the parallel manual-side survival of the same class.

---

## Part B — what would settle the open ones

| # | The question | What would settle it | Runnable here? |
|---|---|---|---|
| **E-006** | On the **#64006A Control** board, does a pressed button make the P2 pin read **high** or **low**? | A **bench test**: configure the pin, press the button, read `INA`. Or the board schematic from Parallax. | **Yes** — jumper-only rig, no external instrument. The result becomes an `EF-NNN` empirical finding and E-006 cites it. |

---

## How an erratum gets here, and what happens after `RESOLVED`

`ingest-source` pass 6 (cross-source conflict audit) is the normal entry point: a conflict that
resolves to *"the source is wrong"* files here rather than to the corrections register or the gap
ledger. Defects found later — a manual audit, a semantic read of an example, a repopulation pass —
file here too.

**Reaching `RESOLVED` is not the end.** Three follow-ons, and the first is the one that gets skipped:

1. **If the KB `Diverges` from, or `Follows`, a wrong source — that is a correction.** File it to
   `P2KB-CORRECTION-FINDINGS.md` and fix the KB. **E-004 is the live example.**
2. **If a manual repeats it**, it is a manual correction too; route it the same way.
3. **If it was settled on the bench**, the result belongs in `P2-EMPIRICAL-FINDINGS.md` as `EF-NNN`,
   and this row cites it rather than restating it.
