# The differential read — every changed YAML file, `v1.17.0..HEAD`, with a verdict

**Task «#325» · 2026-08-26 · entry HEAD `1bdd61ed`, tree clean at entry**

> **If you are `«#326»` and reading this cold: your entire scope is §1, "The one gutted file."**
> Everything else in this document is diagnosis that needs no repair. §4 and §5.2 list defects found
> in passing — they are real, but they are *surviving* content, not removals, and they are not yours.
>
> ✅ **«#326» has run (2026-08-27). The one gutted file is RESTORED; nothing in this document is
> still open as `gutted`. See §8 for what came back, from which source lines, and where it was put.**

Stephen chose this read over the other recovery strategies offered:

> *"we have a concise list of modified .yaml files. we know the prior content of each. how about a
> read of each for what was removed and why — did we gut needed content?"*

It was never done. This is it.

**Why no gate can answer this question.** Every instrument this project has measures *shape*,
*citation presence*, or *parse validity*. A file can be green on all of them while being thinner
than it should be, because "thinner" is a judgement about what a reader needs, and no regex holds
that. Worse, the instrumentation is *asymmetric*: removal was instrumented and retention never was.
So this document is a read, not a measurement — the measurements below only decide **what to read**.

---

## 0 — Scope, derived at entry

Every number here is derived, not carried. **Numbers that disagreed with the dispatch or with the
change ledger are listed in §5 rather than silently corrected.**

| Quantity | Measured | Command |
|---|---|---|
| YAML files changed | **85** | `git diff --name-only v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml' \| wc -l` |
| Modified / Added | **81 / 4** | `git diff --name-status v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml'` |
| Deleted / renamed | **0 / 0** | `git diff --diff-filter=DR -M --name-status …` |
| Lines | **+6137 / −3341** | `git diff --numstat … \| awk '{a+=$1;r+=$2} END{print a,r}'` |
| Top-level keys dropped and never returned | **41, across 18 files** | key-set comparison, §0.2 |
| Leaf facts whose value is absent from the whole shipped KB at HEAD | **1930** | §0.2 |

**Region spread (85).** hardware 27 · architecture 14 · language/spin2 12 · language/pasm2 8 ·
architecture/streamer 8 · architecture/smart-pins 4 · architecture/boot-rom 4 ·
application-notes 4 · guides 2 · code-examples 1 · architecture/system-registers 1.

### 0.1 The four verdicts

| Verdict | Meaning |
|---|---|
| **stronger** | What was removed was replaced by better-sourced content. |
| **equal** | Reworded or restructured; same substance. |
| **thinner-but-honest** | Removed because unsourced, wrong, or deliberately out of scope. Its absence is **correct**. |
| **gutted** | Removed content that the KB **needs** *and* that a source we hold **can support**. Both halves required. |
| *(new file, no baseline)* | Added in this range; nothing could have been removed from it. |

`thinner-but-honest` is a **real and correct outcome**, not a softened failure. Under CITE-OR-OMIT a
remote agent cannot weigh a hedge, so an unsupportable block is better absent. The only question
this document asks about a removal is whether **a source we hold can support it**.

### 0.2 How "what was removed" was measured

A raw `git diff` cannot answer this: a reflowed block shows as hundreds of removed lines while
losing nothing, and a *silently dropped leaf inside a surviving key* shows as one line among
hundreds. So both revisions of every file were parsed with `yaml.safe_load` and flattened to
`(path, value)` leaves, then compared three ways:

1. **Top-level key sets** — a key present at `v1.17.0` and absent at HEAD is a dropped *block*.
2. **Leaf values** — a value present at `v1.17.0` whose normalised string appears nowhere in the
   same file at HEAD is a candidate loss.
3. **KB-wide survival** — each candidate is then searched across **every** YAML in
   `deliverables/ai/P2/` at HEAD, so content that *moved to another file* is not counted as lost.

That third pass matters: 73 facts had merely relocated, most of them clock-configuration symbols
that moved to their definition home.

> 🔴 **The measurement over-reports, deliberately, and every candidate was read.** Rewording defeats
> string matching, so a fact restated in the source's own words scores as "gone". This was the
> single most common finding: of the leaf candidates read in `architecture/`, the large majority
> had returned **better sourced and reworded**, not vanished. A count alone would have been wrong in
> the alarming direction. **This is why the task is a read.**

### 0.3 Where the risk actually was

Two commit pairs did all the bulk removal, and they are the reason this task exists:

| Removal | Repopulation |
|---|---|
| `15c84de5` — 59/60 uncited quantitative blocks out of architecture, language, guides, app-notes (−1043) | `597d5eba` — 45 return cited, 13 stay gone as **disproven**, 1 held, 1 gap (+867) |
| `c733a223` — 59 uncited blocks out of `hardware/` (−1500) | `491f2b55` — 34 return cited, 24 stay out as **true but not actionable** (+1417) |

Plus `1f37ae58` (promotion filter; deleted a pin-current figure five times the absolute maximum) and
`9a1f14a3` (re-derived six architecture files whose provenance was fabricated).

**A block removed for being uncited is `thinner-but-honest` ONLY if no source we hold can support
it.** The decisive fact about timing: the repopulation passes ran **before** the Silicon Doc was
fully extracted (`22b06587`, 48/48 tables). A block ruled unsupportable then may be supportable now.
That is the single most likely source of a `gutted` verdict, and it is where this read pushed hardest.

---

## 1 — The answer

**No, we did not gut the KB. One file, and one file only, is `gutted`.**

| Verdict | Files | Share |
|---|---|---|
| **stronger** | 74 | 87% |
| **equal** | 6 | 7% |
| **thinner-but-honest** | **0 at file level** — see the note below | — |
| ✅ **gutted → RESTORED** | **1** — `guides/pasm2-getting-started.yaml`, restored by «#326» 2026-08-27 (§8) | 1% |
| *new file, no baseline* | 4 | 5% |
| **Total** | **85** | |

> **Why `thinner-but-honest` is zero at file level, and why that is not a dodge.** The verdict is
> assigned **per file**, and the removals were overwhelmingly paired with repopulation *in the same
> file*. A file that lost a fabricated drive ladder and gained cited absolute-maximum ratings is
> `stronger`, not `thinner` — even though the removed block itself was `thinner-but-honest`.
> **`thinner-but-honest` is the correct verdict for 41 individual blocks**, and they are
> dispositioned block-by-block in §3. Reporting only the file-level number would hide them, so both
> are given.

### The one gutted file — ✅ RESTORED by «#326», 2026-08-27 (§8)

**`deliverables/ai/P2/guides/pasm2-getting-started.yaml` — the CON clock-setup declarations.**

`15c84de5` deleted the whole `file_structure.required_blocks.CON` subtree; `597d5eba` never brought
it back. What remains, at line 69–70, is the *entire* clock content of the guide:

> `default: "With no clock-setup symbol declared and not in DEBUG mode, the compiler selects internal RCFAST, which runs at 20 MHz+ (v55:1723). _clkfreq is NOT required."`

**Why this is `gutted` and not `thinner-but-honest`** — both halves of the test are met:

- **The KB needs it.** The file itself says at `:71` that *"PASM-only programs which use any
  non-RCFAST clock mode get a 16-long clock-setter program automatically prepended"* — and then
  never says how to select one. An agent following this guide emits a program running at RCFAST
  ~20 MHz while its `WAITX` operands were computed for 200 MHz: **every delay is wrong by an order
  of magnitude, silently.** That is the same failure class `597d5eba` caught for `WAITMS`/`WAITUS`.
- **A source we hold supports it**, in a table written for exactly this purpose.

**Falsified, not assumed, that it merely moved:** `grep -nE '_clkfreq|_xtlfreq|_xinfreq|_rcfast|_rcslow|asmclk|ASMCLK|HUBSET'`
over the file returns **one line** — `:70`, the sentence above. Its `see_also` targets
(`special-registers.yaml`, `idioms/`, `patterns/`, `concepts/`, `manifests/P2/language/pasm2-manifest.yaml`)
were then searched for `_clkfreq|_xtlfreq|_rcfast`: **zero hits**. The content exists elsewhere in
the shipped set — `language/spin2/constants/special-configuration-symbols.yaml`,
`architecture/clock_system.yaml`, `language/pasm2/asmclk.yaml` — but is **unreachable from this
guide**, which is the artefact an agent starting PASM2 actually reads.

**The source that restores it.** `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt`:

| Line | What it gives |
|---|---|
| `:1708-1709` | Section "Clock Setup" and its opening rule |
| `:1710` | Table header — `CON symbol declarations \| Effect \| HUBSET %CC_SS` |
| `:1711-1719` | **All nine legal declaration combinations**, each with its effect and its `%CC_SS` value |
| `:1721` | `_errfreq` is optional, defaults to `1_000_000` |
| `:1722` | The 15 pF / 30 pF crystal-loading rule |
| `:1734-1736` | `ASMCLK`; the auto-prepended 16-long clock-setter; `_AUTOCLK = 0` to inhibit it |

Legal ceiling for any `_clkfreq` value:
`engineering/ingestion/sources/p2-datasheet/p2-datasheet-text.txt:2200` — PLL fed by direct drive or
crystal, min 3.33 / typ 180 / **max 320 MHz**; footnote 2 at `:2209`.

> **Locator correction («#326», 2026-08-27).** This entry originally gave the footnote as `:2205`.
> Re-read live: `:2205` is the `Cin` *Mode 3: Crystal < 16MHz — 30 pF* row. Footnote 2 —
> *"Nominal PLL frequency (system clock speed) is 180 MHz at up to 105 °C"* — is at **`:2209`**.
> In range, wrong content: the F-377 shape, caught before it was carried into a shipped file.

🔴 **Do not restore verbatim.** The deleted text said `_clkfreq` is *"REQUIRED for timing"*.
`spin2-v55-text.txt:1718` states the opposite — with no symbol and not in DEBUG mode the compiler
selects RCFAST, so nothing is required. Restore **source-first** from the table above.

🔴 **This is a two-file class, not one file.** `guides/spin2-getting-started.yaml:57-58` **kept** its
CON block and still carries the same wrong claim — *"System clock frequency in Hz - REQUIRED for
timing"* — with `:70` repeating `' Required: system clock frequency`. The PASM2 guide lost the
content; the Spin2 guide kept it and kept the error. Both need the same source-first pass.

---

## 2 — Verdicts, by region

Grouped as Stephen asked the change ledger to be grouped. `GONE` = leaf facts whose value is absent
from the whole shipped KB at HEAD (§0.2) — **an upper bound on loss, not a measure of it**; every one
was read.

### 2.1 `hardware/` — 27 files · 25 stronger · 2 new

| File | GONE | Verdict | Reason |
|---|---|---|---|
| `addon-av-breakout.yaml` | 0 | stronger | `signal_map` restructured, guide citation + per-board capture added. |
| `addon-click-adapter.yaml` | — | *new file* | Added by `ccddcbe6` from the #64008 schematic ingestion. |
| `addon-control-board.yaml` | 7 | stronger | Description/signal map returned cited; the `P_LOW_15K` read idiom **corrected** to require DIR high. |
| `addon-digital-video-out.yaml` | 2 | stronger | Same facts, reworded with a citation; ACC-5V bridge retained. |
| `addon-goertzel-touch.yaml` | 7 | stronger | `specifications` returned cited plus a board-revision note. |
| `addon-hd-audio.yaml` | 22 | stronger | `dac_board` returned with the four `P_DAC_*` constants and the parallel-pin impedance rule. |
| `addon-hyperram-hyperflash.yaml` | 10 | stronger | `configuration`/`specifications` returned cited; RES shunt now stated as a driver requirement. |
| `addon-led-matrix.yaml` | 2 | stronger | Charlieplex rule and ~4 mA retained; description now cited. |
| `addon-microsd.yaml` | 0 | stronger | Insertions only — `power_signals` gained a citation. |
| `addon-mini-prototyping.yaml` | 2 | stronger | Description, power rails, grid retained and cited. |
| `addon-motor-driver.yaml` | 62 | stronger | All 16 pin offsets, PWM interlock, 250 ns deadtime, 150 mV/A returned cited; a guide self-contradiction resolved and filed as errata. |
| `addon-rtc.yaml` | 15 | stronger | E-004 closed — the guide's "150 kΩ pull-up" mislabel restated as a P2 drive-strength mechanism; PCF8523 map + `$68` added. |
| `addon-serial-device.yaml` | 26 | stronger | LEDs at 0/1/6/7 and D-/D+ at 2/3, 4/5 returned cited; new even/odd smart-pin pairing note. |
| `addon-serial-host.yaml` | 62 | stronger | Enables at offsets 1/5, D-/D+ pairs, enable sequence returned cited; new Spin2 `code_patterns`. |
| `addon-wx-adapter.yaml` | 0 | stronger | Insertions only — citation + `sole_p2_wx_adapter` disambiguation. |
| `addon-wx-wifi.yaml` | 33 | stronger | `pin_descriptions` returned as a full table with SIP/DIP numbers; `part_variants` → cited `form_factors`. |
| `edge-32mb-module.yaml` | 224 | stronger | Pin map, boot table, 8 µs CS limit, PSRAM banks all returned cited; P58-P61 anchored to the boot-ROM listing; fabricated `alternate_part: 64000-ES` removed **with a note saying why**. |
| `edge-breadboard-carrier.yaml` | 43 | stronger | Wrong "6-9 V" and a non-existent on-board USB-to-serial gone; **5 VDC / 5.5 V max restored cited**. |
| `edge-mini-breakout.yaml` | 30 | stronger | Fabricated "USB connector onboard" removed; cited `connectivity` gives the real P0-P31 + P56-P63. |
| `edge-standard-breakout.yaml` | 27 | stronger | Same fabrication removed; cited `connectivity` adds the eight 2×6 headers. |
| `edge-standard-module.yaml` | 176 | stronger | `pin_mapping` returned cited with an explicit "LEDs are P56/P57, NOT P38/P39" warning. |
| `hardware-compatibility-matrix.yaml` | 2 | stronger | False "all add-ons use P0-P7" replaced by the correct single/dual-header model. |
| `hub75_adapter.yaml` | 58 | stronger | Manufacturer's **70 MHz** replaces the unsourced 40/35 MHz; three explicit `gap_*` keys record what was removed and what would settle it. |
| `p2-eval-board.yaml` | 36 | stronger | Rev D→Rev C, 320 MHz→180 MHz recommended, real flash part, 3.55 in; ~10 `TBD` placeholders replaced with sourced values. |
| `p2-hardware-feature-comparison.yaml` | 104 | stronger | Invented carrier part numbers replaced with real ones; **#64006G re-identified as the Goertzel board**, not a Digital I/O board. |
| `p2-package-mechanical.yaml` | — | *new file* | The G-021 gap, closed: TQFP-100 dimensions transcribed from `silicon-034.png`. |
| `programming-prop-plug.yaml` | 12 | stronger | 3 Mbaud ceiling, DTR/RTS reset selection, ~20 µs pulse returned cited; new `header_pinout`. |

### 2.2 `architecture/` (top level) — 14 files · 13 stronger · 1 new

| File | GONE | Verdict | Reason |
|---|---|---|---|
| `click_module_integration.yaml` | 20 | stronger | `documentation_source` went `code_analysis` → `schematic_primary`; all twelve CLICK_OFST values confirmed against the #64008 sheet with zero corrections; gained `uart_direction_caveat` and `header_span`. Removed `best_practices` is authored advice with no upstream — §3. |
| `clock_system.yaml` | 85 | stronger | Rebuilt from Spin2 v55's own "Clock Setup" closed set with `%CC_SS` per row; PLL fields, `%CC`/`%SS` tables and the datasheet's worked 148.5 MHz sequence all cited. **`pll_lock: ~10 microseconds` was wrong — three Parallax sources say 10 ms.** The symbol ranges moved to their definition home, which I confirmed carries them. |
| `cog_attention.yaml` | 36 | stronger | Fabricated `RDCOGID` deleted (absent from silicon doc, rejected by `pnut-ts`); **ATN corrected from event 15 to event 14** (`silicon-doc-text.txt:2053`); encodings replaced with the real ones. |
| `debug_interrupt.yaml` | 64 | stronger | Three invented configuration registers and the fabricated `NIXINT0`/`TRGINT0` removed; real `BRK`/`COGBRK`/`GETBRK` encodings substituted. |
| `event_system.yaml` | 52 | stronger | The whole 16-event catalogue restored verbatim and cited to `silicon-doc-text.txt:2037-2054`; `SETSE` restriction (pin/LUT/lock only) added. |
| `interrupts.yaml` | 78 | stronger | **The worst correction in the range**: the shipped file had IJMP3/IJMP1 inverted. Also: the `shadow_registers` model is disproven — there are no shadow banks, only `CALLD IRETx,IJMPx WCZ`. |
| `io_pin_timing.yaml` | 146 | stronger | The F-327 fabrication family (a milliamp drive ladder, programmable slew, and a propagation/rise/fall model built on both) removed; cited absolute-maximum ratings, the protection-diode mechanism and the 5 V series-resistor technique added. See §3 and §5. |
| `locks.yaml` | 26 | stronger | The invented `LOCKTRY` "query" form — which actually **acquires** — removed; real encodings substituted. |
| `lookup_ram.yaml` | 47 | stronger | Fabricated `RDLUTS` deleted; **LUT-sharing direction corrected** and `WRLUT`'s operand order fixed (D carries DATA, S carries ADDRESS). |
| `pin-drive-configuration.yaml` | — | *new file* | The replacement for the fabricated ladder: eight real rungs, cited. |
| `pin-power-domains.yaml` | 8 | stronger | The two-layer distinction rebuilt with sources — silicon 16 groups of 4, Edge board 8 LDOs of 8 — plus *why* a ratiometric measurement must stay within four. |
| `serial_loader.yaml` | 10 | stronger | All boot facts returned quoted from source, plus the P62 open-drain behaviour under a non-zero INA/INB mask. |
| `smart_pin_patterns.yaml` | 7 | stronger | Generic unsourced notes replaced by verbatim, cited statements; the timing cross-reference kept **and** promoted into `related:`. |
| `smart_pins.yaml` | 13 | stronger | `%AAAA`/`%BBBB`/`%FFF` selectors given full bit ranges and cited; the four global filter defaults now carry length, tap **and** the source's own arithmetic. |

### 2.3 `architecture/streamer/` — 8 files · 4 stronger · 3 equal · 1 new

| File | GONE | Verdict | Reason |
|---|---|---|---|
| `_index.yaml` | 0 | stronger | Gained the whole `pin_capture` routing entry plus aliases. |
| `dac-routing.yaml` | 2 | equal | Apparatus only — aliases added, `see_also` bare names → full paths. No content change. |
| `dds-goertzel.yaml` | 10 | stronger | Citations re-anchored from the partial `p2-documentation.txt` extract to the completed `silicon-doc-text.txt`; aliases added. **Two locators were only half re-anchored — §5.** |
| `modes-reference.yaml` | 4 | stronger | `field_notation_caveat` expanded with a second bench proof and a source. |
| `nco-timing.yaml` | 2 | equal | Apparatus only — aliases, full-path `see_also`. |
| `overview.yaml` | 0 | equal | Apparatus only — aliases, `related:`, full-path `see_also`. |
| `pin-capture.yaml` | — | *new file* | Added by `ad4f974f`; why a smart-pin bus must be watched from next door. |
| `pin-selection.yaml` | 34 | stronger | **F-361**: the dense sub-pin slot table no source states and the bench contradicts is gone; replaced by the real rule (`pin << 17`, `D[19:17] = pin & 7`). |

### 2.4 `architecture/smart-pins/` — 4 files · 4 stronger

| File | GONE | Verdict | Reason |
|---|---|---|---|
| `smart-pin-00000-normal-mode.yaml` | 2 | stronger | Both worked examples **corrected**: they taught the disproven `WRPIN P_HIGH_15K` + `DIRL` pull-up idiom. |
| `smart-pin-00011-dac-16bit-pwm-dither.yaml` | 6 | stronger | Dither facts returned verbatim from `part4-smart-pins.txt:284-308`, plus the `M[12:10]=%101` requirement. |
| `smart-pin-11000-adc-internal-clock.yaml` | 4 | stronger | `P_ADC_GIO`/`P_ADC_VIO` **redefined correctly** — they are calibration *sources*, not input ranges; the old "ground-referenced input" was a legal name with a wrong definition. |
| `smart-pin-11011-usb-host-device.yaml` | 2 | stronger | USB 12 Mbps / 1.5 Mbps returned with the `D_14` field, the DP/DM roles and the FPGA resistor note. |

### 2.5 `architecture/boot-rom/` — 4 files · 4 stronger

| File | GONE | Verdict | Reason |
|---|---|---|---|
| `_index.yaml` | 12 | stronger | Boot timing and all three path summaries returned cited, with pin directions named from the flash chip's side. |
| `boot-pattern-selection.yaml` | 7 | stronger | **Corrected**: the claim that the ROM issues no `HUBSET` is contradicted by its own listing — the `Prop_Clk` and shutdown paths both do, now cited to `ROM_Booter.lst`. |
| `spi-flash-boot.yaml` | 2 | stronger | Patterns returned verbatim; DI/DO direction disambiguated. |
| `taqoz-forth.yaml` | 0 | stronger | Gained `useful_for`, sourced to the author's own reviewer comment. |

### 2.6 `architecture/system-registers/` — 1 file · 1 stronger

| File | GONE | Verdict | Reason |
|---|---|---|---|
| `complete-system-registers-index.yaml` | 15 | stronger | 13 dangling `yaml_file:` pointers removed (F-364), content kept inline; `$1F6`/`$1F7` descriptions **corrected** — PA/PB hold the CALLD-imm *return* address and the CALLPA/CALLPB parameter, which "CALLD-imm parameter" named neither. |

### 2.7 `language/spin2/` — 12 files · 11 stronger · 1 equal

| File | GONE | Verdict | Reason |
|---|---|---|---|
| `concepts/basic-io.yaml` | 59 | stronger | Source-first rebuild; three disproven blocks deleted incl. `max_current_per_pin: 150mA` — **five times the datasheet's ±30 mA absolute maximum**, in the exact number used to size an LED resistor. |
| `conventions/johnny-mac-documentation-style.yaml` | 1 | stronger | Inline example corrected: `P_HIGH_150K "150K pullup resistor"` → `P_HIGH_15K` + `drvh`. Compiles. |
| `conventions/spin2-docs-jonnymac.yaml` | 1 | stronger | Same correction, uppercase variant. |
| `debug-commands/pc_key.yaml` | 5 | stronger | Every removed rule restated from v55; one new rule added (hub `@key` vs cog `#key`). |
| `debug-displays/logic.yaml` | 0 | stronger | Pure addition — capture-vs-display split, `pin-capture.yaml` cross-ref, cited worked example. |
| `methods/cogstop.yaml` | 1 | equal | One word: "pull-up/down resistors" → "**external** pull-up/down resistors". |
| `methods/getct.yaml` | 4 | stronger | Derived figures replaced by cited v55 + datasheet statements. **The ledger's item 2 — a missing `description` — was repaired by `75971308`; `description` is present at HEAD.** |
| `methods/pinfloat.yaml` | 1 | stronger | "external" added, plus a note that a `P_HIGH_*` selection goes inactive when the pin floats. |
| `methods/waitms.yaml` | 10 | stronger | The wrong 1–4,294,967 ms ceiling replaced by v55's `$8000_0000`-clock bound plus a `ceiling_formula`. |
| `methods/waitus.yaml` | 15 | stronger | Same correction; removals are quality commentary ("excellent/good/marginal resolution") — `thinner-but-honest` at block level under the KB entry rule. |
| `methods/wrpin.yaml` | 26 | stronger | All 26 are de-duplication; every one of the 13 mode constants and all four `P_TT_*` verified present exactly once in its canonical home. |
| `symbols/spin2-builtin-symbols-complete.yaml` | 20 | stronger | 874 → 1937 leaves carrying v55's own wording. The 20 are 3 corrected counts, 13 rewordings, **4 fabricated symbol names** — zero real losses. |

### 2.8 `language/pasm2/` — 8 files · 8 stronger

| File | GONE | Verdict | Reason |
|---|---|---|---|
| `concepts/basic-io.yaml` | 62 | stronger | Byte-twin of the Spin2 file; same disproven blocks removed, and the `Set DIR before OUT` glitch rule was **backwards** and is now corrected. |
| `concepts/streamer_smartpin_control.yaml` | 1 | stronger | The removed block returned structured and cited; a derived figure replaced by the source's own wording. |
| `drvh.yaml` | 0 | stronger | Citation added for the existing 3-clock pin latency. |
| `drvl.yaml` | 0 | stronger | Same citation, **plus a duplicate `timing:` key removed** — the surviving merged block keeps `cycles: 2`. |
| `getbrk.yaml` | 3 | stronger | `flags_affected: C/Z: No effect` was **wrong**; replaced with cited per-flag behaviour and the WZ polarity corrected. |
| `getxacc.yaml` | 1 | stronger | A dead locator re-anchored to a live, verified one. |
| `setxfrq.yaml` | 3 | stronger | All four SETXFRQ words retained; block now carries the source rule and per-value arithmetic. **See §5 — two values disagree with the rounding rule the block itself cites.** |
| `wrpin.yaml` | 6 | stronger | Six drifted one-line restatements de-duplicated to `architecture/smart_pins.yaml`, verified to carry all six with bit ranges. |

### 2.9 `application-notes/` — 4 files · 4 stronger

| File | GONE | Verdict | Reason |
|---|---|---|---|
| `p2an001-single-pin-instrumentation-adc.yaml` | 7 | stronger | Two removals were **corrections**: the designer's 15 mV became the hardware-verified ≤9 mV with an explicit "do not quote 15 mV", and "P2 spec max is 300 MHz" was simply wrong (datasheet PLL max 320 MHz). |
| `p2an002-cordic-for-real-work.yaml` | 7 | stronger | Six gotchas return with Silicon Doc quotes + EF-053; two dropped claims are **refuted**, not lost. Two broken locators — §5. |
| `p2an003-dac-analog-signal-generation.yaml` | 9 | stronger | `key_parameters` returns with verbatim dither text plus a new sourced `M[12:10]=%101` requirement. |
| `p2an004-frequency-rotation-rc-timing-measurement.yaml` | 9 | stronger | Gotchas re-anchored to the datasheet Pin Mode Legend and the `%AAAA`/`%BBBB` table. Carries a self-contradiction — §5. |

### 2.10 `guides/` — 2 files · 1 gutted *(now restored, §8)* · 1 equal · and `code-examples/` — 1 file · 1 equal

| File | GONE | Verdict | Reason |
|---|---|---|---|
| ✅ `guides/pasm2-getting-started.yaml` | 24 | **gutted → RESTORED** | The CON clock-setup declarations. Net a large improvement everywhere else, which is exactly why a gate would have passed it. **§1**; restored source-first by «#326» 2026-08-27, **§8**. |
| `guides/spin2-getting-started.yaml` | 7 | equal | Relative→absolute path re-anchors, all targets verified present, plus dropping "pull resistors" from a routing blurb — honest, since `basic-io.yaml` now states the P2 has no internal pull network. |
| `code-examples/smart-pins-002-button-reading.yaml` | 1 | equal | One word: "Pull-up or pull-down resistor" → "**External** …", so it cannot be read as an internal P2 pull. |

---

## 3 — Block-level disposition: the 41 top-level keys that never came back

This is where `thinner-but-honest` lives. Derived by comparing the top-level key set of every file at
`v1.17.0` and at HEAD — **41 keys across 18 files**, two more than the change ledger's table (§5).

| Disposition | Keys | Verdict for the block |
|---|---|---|
| **Fabricated / disproven** — no source states it, and in several cases a source contradicts it | 15 | `thinner-but-honest` |
| **True but not actionable** — cannot change emitted code; verified present in the ingestion tree | 24 | `thinner-but-honest` |
| **Authored here, no upstream** — correct, actionable, and unsupportable by anything we hold | 2 | *open gap*, F-352 |
| **Total** | **41** | |

### 3.1 Fabricated or disproven — 15 keys

`architecture/io_pin_timing.yaml` — 8 keys: `timing_specifications`, `clock_relationships`,
`drive_strength_configurations`, `slew_rate_control`, `input_characteristics`,
`special_timing_modes`, `protocol_timing_examples`, `compensation_techniques`.
`language/pasm2/concepts/basic-io.yaml` and `language/spin2/concepts/basic-io.yaml` — 3 keys each:
`drive_strength_configuration`, `timing_considerations`, `hardware_specifications`.
`hardware/p2-eval-board.yaml` — `video_audio`.

**Falsification run against the *completed* Silicon Doc extraction, not the 75% one.** Searched
`silicon-doc/`, `p2-datasheet/`, `p2-hardware-manual/`, `smart-pins/` and `spin2-v55/`:

| Term | Files | Hits |
|---|---|---|
| `slew` | **0** | **0** |
| `fall time` | **0** | **0** |
| `FR4` | **0** | **0** |
| `rise time` | 1 | 1 (unrelated) |
| `propagation delay` | 2 | 3 (unrelated) |
| `VIL` / `VIH` in `p2-datasheet/`, `silicon-doc/`, `p2-hardware-manual/` | **0** | **0** |

So the removed logic levels (`VIL_max 0.8V`, `VIH_min 2.0V`) and Schmitt thresholds
(`1.65 V / 1.35 V / ~300 mV hysteresis`) have **no source**. Schmitt appears 103 times across the
corpus — but always as an input **mode** (`Pin Schmitt`, `Adj Schmitt`, `P_SCHMITT_A`), never as a
threshold. That distinction is the whole point: **the mode is documented and is in the KB; the
electrical characterisation of it is not documented anywhere and is correctly absent.**

The `150 mA` per-pin figure was the sharpest: the datasheet's absolute maximum is **±30 mA**
(`p2-datasheet/p2-datasheet-text.txt:2142`). The removed figure was **five times the absolute
maximum**, in the exact number a reader uses to size an LED series resistor.

### 3.2 True but not actionable — 24 keys

All in `hardware/`, all ruled CORRECT-BUT-NOT-ACTIONABLE by the promotion filter, and — this is the
half that had to be checked rather than assumed — **all verified present in the ingestion tree
before they left the shipped set**, with a locator for each:

| File | Keys held out | Verified present at |
|---|---|---|
| `addon-hd-audio.yaml` | `set_contents`, `use_cases` | `sources/P2-HD-Audio-Add-on/complete-P2-HD-Audio-Add-on-reference.md:14,:25,:33,:36` |
| `addon-hyperram-hyperflash.yaml` | `host_note` | `sources/hyperRam-n-hyperFlash/hyperram-hyperflash-text.txt:41-42,:46,:139-141` |
| `addon-motor-driver.yaml` | `power_signals`, `protection` | `sources/p2-universal-motor-driver/complete-p2-universal-motor-driver-content.md:41-43,:61,:170,:176,:224` |
| `addon-rtc.yaml` | `power_signals`, `specifications` | `sources/P2-RTC-Add-on/P2-RTC-Add-on-text.txt:44-52,:92-93` |
| `addon-serial-device.yaml` | `specifications`, `rev_b_5v_note` | `sources/p2-eval-add-on-boards/complete-p2-eval-add-on-boards-reference.md:36` |
| `addon-serial-host.yaml` | `specifications`, `power_requirements`, `limitations` | same as above, `:36`; `p2-eval-add-on-boards-text.txt:40-41` |
| `addon-wx-wifi.yaml` | `part_variants`, `specifications` | `sources/parallax-wx-wifi/pdf2md-stripped.md:55-64`; `complete-wx-wifi-reference.md:54-56` |
| `edge-breadboard-carrier.yaml` | `specifications`, `specialized_features`, `power_specifications` | `sources/edge-module-breadboard/edge-module-breadboard-narrative.txt:163` |
| `edge-mini-breakout.yaml` | `specifications`, `power_management` | `sources/edge-mini-breakout/` |
| `edge-standard-breakout.yaml` | `specifications`, `power_management` | `sources/edge-breakout-board/` |
| `edge-standard-module.yaml` | `revision_history` | `sources/edge-standard-module/edge-standard-module-narrative.txt:519-550` |
| `hub75_adapter.yaml` | `power_requirements` | ⚠️ **see below — this one does not hold** |
| `edge-32mb-module.yaml` | `alternate_part` | Deliberately deleted as a **fabrication**, not held out — `#64000-ES` is a different product; the file now carries a note saying so. |

🔴 **One of the 24 was labelled wrongly.** `hub75_adapter power_requirements` was ruled
CORRECT-BUT-NOT-ACTIONABLE, which under the filter's own sub-rule P requires ingestion-tree presence
before removal. Its per-panel current figures (16×32 at 1.5 A/4 A, up to 64×64 at 5 A/20 A) exist in
**no** vendor source — searched all of `engineering/ingestion/` for `4A peak|8A peak|12A peak|20A peak|1\.5A typical|2\.5A typical`.
The only near-match is an *authored* knowledge file (`sources/p2-addon-board-circuit-knowledge.md:406-408`)
whose numbers **differ**. It should have been ruled UNSOURCED. **The outcome is right — it stays
gone — but the label is wrong and sub-rule P was not actually satisfied for this block.** Not a
restoration item; a disposition-hygiene item.

### 3.3 Authored here, with no upstream — 2 keys, and this is the real open gap

| File | Key | Status |
|---|---|---|
| `architecture/io_pin_timing.yaml` | `best_practices` | Generic PCB-layout guidance (match trace lengths, source termination, 22-33 Ω, minimise capacitive load). Recorded as **F-352**. |
| `architecture/click_module_integration.yaml` | `best_practices` | Driver-authoring guidance ("always use offset constants, never hardcode pins", "make base pin a runtime parameter", reset-during-init). Ruled **ACTIONABLE** — it is literally the shape of emitted code — then found to have no upstream. |

**These are NOT `gutted` by this document's test**, because the test's second half fails: no source we
hold can support them. They are also not comfortable. **Re-checked against the newly ingested
`p2-click-adapter/` source** (which did not exist when F-352 was filed): the #64008 schematic
establishes the twelve pin offsets and nothing about driver authoring, so the gap does **not** close.

The underlying defect is structural and worth naming once: **the removal rule has three branches
(in the ingestion tree → remove; should be written there first → write it; disproven → delete) and
no branch for "authored here, correct, and with no upstream to cite."** Both keys above fell through
that missing branch. Deciding what that branch should be is a policy call, not a repair.

---

## 4 — What this read found that the instruments could not

Three defects, all in files that pass **every** gate in the sweep. Each is a **surviving** defect,
not a removal — so `«#326»`'s restoration scope is §1 alone, and these belong wherever surviving-content
defects are routed.

### 4.1 🔴 A citation re-anchor that was only half applied

`architecture/streamer/dds-goertzel.yaml`. The F-365 pass (`491d033b`) re-anchored citations from the
partial `p2-documentation.txt` extract to the completed `silicon-doc-text.txt`. Five of seven are
correct. **Two carry a stale line range under the new filename:**

| Line | Ships | Lands on in `silicon-doc-text.txt` | Should be |
|---|---|---|---|
| `:74` | `silicon-doc-text.txt:1565 and :4062-4095` | `:4062-4095` is smart-pin **PWM/counter frame periods** | `:1597-1602` (the `%A` region-bound / `%T` phase-offset rule) |
| `:303` | `silicon-doc-text.txt:1636 (setup) and :4289-4305 (mode/data longs)` | `:4289-4305` is **Table 34 clock-count rows** | `:1686-1687` (`dds_d` / `dds_s`, the actual mode/data longs) |

**Why no gate catches it, and how I know:** I ran a class-wide check over the whole shipped KB —
every `<file>.txt:<N>` locator against that file's real line count. **Zero out of range.** These two
locators are *in range and wrong*, which is precisely the failure a range check cannot see. Only
reading the cited lines finds it.

Two more of the same class, in the same pass, found by the app-notes read:
`application-notes/p2an002-cordic-for-real-work.yaml:103` cites `silicon-doc-text.txt:434` for the
CORDIC summary (that line is blank; the quote is at **`:184`**) and `:5145,:5401` for the
GETQX/GETQY no-result event (those are `RDLONG`/`MERGEB` **encoding** lines; the event text is at
**`:2054`** and **`:2291`**).

### 4.2 🔴 A file that contradicts its own corrected block

`architecture/interrupts.yaml`. `9a1f14a3` correctly established at `:38-46` that
*"There are no shadow register banks"* — but the file's own top-level `description` still reads, at
`:26`:

> *"Each interrupt level has its own set of shadow registers for zero-overhead context switching."*

The `description` is the first thing a retrieving agent reads, and it states the exact model the
file below it disproves.

### 4.3 🟠 Uncited quantities that survived the purge in the file the purge edited

`guides/pasm2-getting-started.yaml:620-623` still ships
`clock_frequency: {default: "20 MHz crystal with PLL", typical: "200-300 MHz", maximum: "340+ MHz (silicon dependent)"}`.
No source states 340+ MHz — `p2-datasheet-text.txt:2200` gives a PLL maximum of **320 MHz**. And
`default: "20 MHz crystal with PLL"` contradicts the same file's own `:70`, which says the default
with no symbol declared is RCFAST. This is the class `15c84de5` existed to clear, in a file that
commit edited.

Also: `architecture/io_pin_timing.yaml` still cites `part3-pins.txt` in its header comment and in
`extraction_metadata` — **that file does not exist** in `sources/silicon-doc/`. It is the same
fabricated-provenance class `9a1f14a3` fixed for six files; `io_pin_timing.yaml` was not among them.
A residual `relationship: "Smart pins add ~1-2ns to base timing"` at `:174` is a surviving member of
the very nanosecond family the file's own description says is unsupportable.

---

## 5 — Numbers that disagreed, and defects found in passing

### 5.1 Every count that disagreed with what was carried in

| Carried in | Derived here | Why they differ |
|---|---|---|
| 72 changed files (dispatch) | **85** | Five commits landed after that number was written. |
| 61 changed files (change ledger §0.1) | **85** | The ledger was **correct when written**; 24 files changed after it. Its region spread is stale in the same way. |
| 1 new file (ledger §0.1) | **4** | `streamer/pin-capture.yaml`, `hardware/addon-click-adapter.yaml`, `hardware/p2-package-mechanical.yaml` landed after. |
| 43 top-level keys dropped (dispatch) | **41** | Different method; mine is a strict key-set delta at HEAD. |
| ~1,332 leaf values lost across 47 files (dispatch) | **1930 across 73 files** absent KB-wide; **1725** of them under *surviving* keys | Mine counts a value as lost only if its string appears nowhere in the file **and** nowhere in the KB. Both numbers over-report actual loss — §0.2. |
| `15c84de5`: "59 uncited blocks" | `597d5eba`: "Of the **60** blocks the purge removed" | **The two commit messages disagree with each other by one.** The ledger's independent count is 60. The dispatch repeats the 59. |
| `491f2b55`: "Of the 59 blocks … 34 return … 24 stay" | 34 + 24 = **58** | One hardware block is unaccounted for in that commit's own arithmetic. |
| Ledger §1.3 not-actionable table | **2 keys more** | `language/{pasm2,spin2}/concepts/basic-io.yaml hardware_specifications` appear in neither of the ledger's §1.3 tables; they were deleted by `1f37ae58`, not by the purge, which is why. |
| "A sample of 7 removals found 4 recoverable-but-not-recovered" (dispatch) | **1 of 85 files gutted** | Not reproduced. Every candidate this read examined was either restored-and-reworded, corrected, or genuinely unsupportable. I could not locate that sample in any artefact to reconcile against it — §5.3. |
| Ledger items **2**, **7**, **8** (🔴/🟠 pre-ship) | **All three already repaired** | `getct.yaml description` restored, `edge-breadboard-carrier` 5 VDC restored cited, `addon-serial-host description` restored — by `75971308` and siblings, after the ledger was written. |

### 5.2 Out-of-scope defects found while reading — named, not fixed

None of these are removals; none are in `«#326»`'s restoration scope. Recorded so they are not lost.

1. **`language/pasm2/setxfrq.yaml common_values` — two of four values contradict the rounding rule
   the block itself cites.** The block quotes the Silicon Doc footnote *"For fractions with
   remainders, the computed D/# value should be incremented"* (`sources/silicon-doc/part2-pixel-ops.txt:117`),
   yet `computation:` says `round(...)` and the shipped values match round-to-nearest:
   25.175 MHz @ 250 MHz → source rule gives `$0CE3_BCD4`, shipped `$0CE3_BCD3`; 44.1 kHz @ 250 MHz →
   source rule gives `$0005_C7C1`, shipped `$0005_C7C0`. **Two-file class** —
   `architecture/streamer/nco-timing.yaml video_rates` carries the same `$0CE3_BCD3`.
   Pre-existing (unchanged across the range), surfaced by attaching the rule to it.
2. **`language/spin2/methods/{waitms,waitus}.yaml` changed `notes:`/`limitations:` from YAML
   *sequences* to *mappings*.** Every sibling in `language/spin2/methods/` keeps them as lists. A
   schema inconsistency introduced by the repopulation.
3. **`application-notes/p2an004-…yaml` contradicts itself.** `:111` says the sensor's electrical
   figures "are deliberately not restated here" because the sensor datasheet is not in the ingestion
   tree; `:87` restates them and `:127` cites the datasheet by document number. One of the two has to go.
4. **Inconsistent treatment of derived arithmetic inside one region.** `p2an003:127` deletes
   `200 MHz / 256 = 781_250 sps` because derivations are "not statements taken from a Parallax
   source", while `p2an001:80` keeps `raw_sample_rate_sps: 1_562_500  # 200_000_000 / 128`, the
   identical construction, uncited.
5. **Locators off by a little, in files this range edited.**
   `guides/pasm2-getting-started.yaml:70` cites `v55:1723`; the statement is at
   `spin2-v55-text.txt:1718` (`:1723` is "During compilation, two constant symbols are defined").
   `p2an001…:93` cites `p2-datasheet-text.txt:2199`; the PLL row is `:2200` (`:2199` is the Crystal row).
6. **`P2-EMPIRICAL-FINDINGS.md:653` names `P2AN002/examples-library/cordic-pipeline-throughput.spin2`
   as a shipped artefact that violates EF-053.** The YAML now states the finding correctly; the
   example file it points at apparently does not.
7. **Authored-here buying-guide content is still un-dispositioned.**
   `hardware/p2-hardware-selection-guide.yaml` (all three blocks) and
   `hardware/p2-hardware-feature-comparison.yaml selection_criteria` were correctly retained under
   sub-rule P but never given a disposition. Same missing branch as §3.3.
8. **`architecture/io_pin_timing.yaml` cites a source file that does not exist** — `part3-pins.txt`,
   in both its header comment and `extraction_metadata`. §4.3.

### 5.3 What I could not reconcile

The dispatch states that *"a sample of 7 removals checked against sources found 4
recoverable-but-not-recovered."* **I could not find that sample recorded anywhere** — searched
`engineering/analysis/*.md` and `engineering/operations/P2KB-CORRECTION-FINDINGS.md` for
`recoverable`; the three hits are all about a purge being *recoverable from git*, a different sense.
This read did not reproduce a 4-in-7 rate: it found **1 gutted file in 85**. The most likely
explanation is that the sample predated `75971308` and its siblings, which repaired exactly the class
of hole such a sample would have hit — the ledger's own three red/orange items were all in that state
when the ledger was written and are all closed now (§5.1). **Stated rather than resolved**, because
the sample itself is not in the repo to check.

---

## 6 — Commands, for re-running

```bash
G="git -c safe.directory=/workspaces/P2-Knowledge-Base"

# Scope
$G diff --name-status v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml'
$G diff --numstat    v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml' | awk '{a+=$1;r+=$2} END{print a,r}'

# Dropped top-level keys, per file (the reliable instrument)
# parse both revisions with yaml.safe_load; report keys present at v1.17.0 and absent at HEAD

# Leaf-fact candidates (over-reports; every hit must be READ, not counted)
# flatten both revisions to (path, value); a value is a candidate only if its normalised
# string appears neither in the file at HEAD nor anywhere else under deliverables/ai/P2/

# The check no gate performs: every locator against its source file's real length
# (found 0 out of range — the two real defects in §4.1 are in-range and wrong)
```

**Verdict boundary used throughout:** `stronger` requires that removed content was replaced by
better-sourced content **or** that substantive sourced content landed. Apparatus-only changes —
aliases added, bare cross-reference names normalised to full paths — are `equal`, because the
content did not change. This is why three streamer files that improved are scored `equal`.

---

## 7 — Sweep at exit

All nine standing instruments re-run at completion. **No delta from the entry baseline.**

| Instrument | Exit |
|---|---|
| `verify-yaml-format.py` | 0 |
| `validate-crossref-keys.py` | 0 |
| `validation/audit-yaml-duplicate-keys.py deliverables/ai/P2` | 0 |
| `validation/audit-yaml-claim-sourcing.py` | 0 |
| `validation/audit-constant-fidelity.py` | 0 |
| `validation/audit-extraction-digit-density.py --all` | 0 |
| `validate-dod-release.py` | 0 |
| `validation/audit-register-hygiene.py … P2KB-CORRECTION-FINDINGS.md` | 0 |
| `validation/audit-register-hygiene.py … SOURCE-ERRATA.md` | 0 |
| `validation/audit-register-hygiene.py … P1-CORRECTION-FINDINGS.md` | **1** — `no-counter`, pre-existing, out of scope, unchanged |

**And that is the point of this document.** Nine instruments were green at entry, are green at exit,
and were green throughout the range in which `guides/pasm2-getting-started.yaml` lost the only
description of how to set the clock. Every gate passed a guide that will make an agent emit code
running twenty times slower than it computed its delays for. **No gate here measures whether a file
still says what a reader needs — only a read does.**

---

## 8 — Resolution: what «#326» restored, 2026-08-27

**Entry:** tree clean at `4caeb6cc`, all nine standing instruments green (§7).
**Scope:** exactly the one `gutted` entry in §1, plus the two-file class it belongs to and one
cite-or-omit fold-in the dispatch attached to the same file. **Nothing else was widened into.**

### 8.1 The restoration — `guides/pasm2-getting-started.yaml`, `file_structure.clock_setup`

**Restored, not reverted.** The deleted block's own wording (`_clkfreq` *"Required: system clock"* /
*"REQUIRED for timing"*) was **not** brought back; §1 was right that the source contradicts it. What
came back is the thing the file was actually missing: **how to declare a non-RCFAST mode at all.**

| What returned | From (re-read live at `4caeb6cc`) | Where it now lives |
|---|---|---|
| All **nine** legal CON declaration combinations, each with its verbatim effect and its `HUBSET %CC_SS` value | `spin2-v55-text.txt:1710-1719` | `file_structure.clock_setup.declaration_combinations` (a 9-element list; each element carries `con_symbols`, `effect`, `hubset_cc_ss`, and the `v55_line` it came from) |
| `_errfreq` is optional; defaults to `1_000_000` | `:1721` | `…clock_setup.errfreq_is_optional` |
| The `**` footnote — `x`=0/15 pF at `_xtlfreq >= 16_000_000`, else `x`=1/30 pF | `:1722` | `…clock_setup.the_x_bit` |
| ASMCLK: no operands, conditional prefix allowed, assembles to one or six PASM instructions | `:1734`, `:1738-1740` | `…clock_setup.asmclk` |
| The `clkmode_` manual crystal/PLL switch sequence (`HUBSET ##clkmode_ & !%11` / `WAITX` / `HUBSET`) | `:1725`, `:1738` | `…clock_setup.manual_switch` + `manual_switch_example` |
| PLL ceiling for a legal `_clkfreq` value | `p2-datasheet-text.txt:2200`, footnote 2 at `:2209` | `…clock_setup.what_value_is_legal` |
| Reciprocal cross-refs by index key | — | `…clock_setup.see_also` → `p2kbPasm2Asmclk`, `p2kbPasm2Hubset`, `p2kbSpin2SpecialConfigurationSymbols`, `p2kbArchClockSystem` |

Pre-existing keys were kept and two were repaired in place:

- `default:` cited **`v55:1723`**, which is *"During compilation, two constant symbols are defined…"*
  — in range, wrong content, the F-377 shape. Re-anchored to **`:1718`** (the *"No symbol and not
  DEBUG mode"* row that actually states it), and the DEBUG-mode row at `:1719` added, since the
  original sentence silently dropped the other half of the default.
- The file's `file_structure.source:` cited **"Clock Setup :1716-1725"**, a range that begins at the
  `_rcslow` row — it never covered the table header or the first five combinations, i.e. it cited
  the content that had been deleted while pointing past most of it. Widened to **`:1708-1726`** and
  **`:1734-1740`**.

**One divergence from the plain-text extraction, recorded in the file itself.** `spin2-v55-text.txt`
writes the XI-input-plus-PLL row's mode value as **`01_1 1`** at both `:1713` and `:1738`. That is an
extraction artifact, not the source: in `Parallax Spin2 Documentation v55.docx` the cell is one table
cell split across two Word runs (`01_1` + `1`), and checking `word/document.xml` for all nine values
shows it is **the only** split one — the other eight are whole runs. The file carries **`%01_11`**
and states this in `clock_setup.extraction_note_2026_08_27`. *(The extraction defect itself belongs
to the ingestion head — see the «#326» DEVIATIONS.)*

### 8.2 The class sweep — `guides/spin2-getting-started.yaml`

`grep -rn "REQUIRED for timing\|Required: system clock" deliverables/ai/P2 --include=*.yaml` returned
**two** hits, both in this file, and a widened sweep for any *"`_clkfreq` … required/mandatory/must"*
phrasing across the shipped set returned nothing further.

- `core_block_types.CON.required_constant` — the **key name itself** carried the wrong claim. Renamed
  `clock_setup_constants`, given its own `source:`, and re-headed with
  `is_a_clock_symbol_required: "No…"` anchored to `v55:1718`.
- The CON `example:` comment `' Required: system clock frequency` → `' optional: crystal+PLL, assumes
  a 20 MHz crystal` (`v55:1711`).
- The nine-combination table is **not duplicated** here; a keyed `see_also` points at
  `p2kbGuidePasm2GettingStarted` and `p2kbSpin2SpecialConfigurationSymbols`.

Side effect worth recording: this file cited **nothing anywhere** before, so it sat in
`audit-yaml-claim-sourcing`'s Tier 2. It now cites, which promotes its quantity-bearing block into
Tier 1's reach — and it passes, because the citation was added *inside* that block. Tier 2 went
49 → 48; Tier 1 stayed at 0.

### 8.3 Fold-in — `timing_considerations.clock_frequency`, same file, cite-or-omit

Not a `gutted` entry; surviving uncited content the dispatch attached to this task. It read
`default: "20 MHz crystal with PLL"` / `typical: "200-300 MHz system clock"` /
`maximum: "340+ MHz (silicon dependent)"`, uncited. All three were **replaced source-first, not
restored**:

- *"default: 20 MHz crystal with PLL"* — contradicted this same file's `clock_setup`. The compiler
  default is **RCFAST** (`v55:1718`); a 20 MHz crystal is only what `_clkfreq`-alone *assumes*
  (`v55:1711`).
- *"typical: 200-300 MHz"* — no source we hold states it; the datasheet's typical is **180 MHz**.
- *"maximum: 340+ MHz"* — `340 MHz` appears in our holdings **only** in
  `TAQOZ-Forth-Bitbashers-Guide/taqoz-bitbashers-text.txt:608,614` as an overclocking anecdote:
  community material, an upstream lead, never a citable authority. The datasheet maximum is
  **320 MHz**.

The block now carries the full AC Characteristics min/typ/max for RCFAST, RCSLOW, crystal, direct
drive and PLL from `p2-datasheet-text.txt:2196-2200` + footnote 2 at `:2209`, **labelled as the
datasheet's absolute limits rather than the Hardware Manual's recommended-use range** — the labelling
`SOURCE-ERRATA.md` **E-007** requires — and a `correction_2026_08_27:` note saying what was removed
and why.

### 8.4 Re-verdicts

**None.** The single `gutted` entry held up on re-read: both halves of §1's test were still met at
`4caeb6cc`, so it was restored rather than demoted to `thinner-but-honest`. No other file in this
document was found to be `gutted`.

### 8.5 Legality checks (pnut-ts v1.55.3 — legality only, never semantics)

Every declaration form written into the KB was assembled inside a PASM-only file:

- all **nine** combinations → exit 0;
- the three PLL forms **without** `_errfreq` → exit 0, which is what
  `errfreq_is_optional` asserts;
- `_AUTOCLK`: `_xtlfreq = 16_000_000` builds **80 bytes**, the same file plus `_AUTOCLK = 0` builds
  **16 bytes** — a difference of exactly **16 longs**, the auto-prepended clock-setter;
- `ASMCLK` under an external-clock declaration with `_AUTOCLK = 0` grows the build by exactly
  **6 longs** (4 → 28 bytes), which is why `asmclk` says *six*, not the three source lines v55 prints;
- `_clkfreq = 400_000_000` assembles, which is why `what_value_is_legal` says the datasheet ceiling
  binds *"even where the compiler accepts it"*.

### 8.6 Sweep at exit

All nine instruments re-run. **No delta from §7.** The two blocking gates were shown able to fail
before the green was accepted: a scratch file with the F-327 shape (a citing file plus an uncited
`150mA`/`2000Ohm`/`2ns` block) drove `audit-yaml-claim-sourcing` to **Tier 1 = 1, exit 1**, and a
doubled key in the same file drove `audit-yaml-duplicate-keys` to **exit 1**; both returned to 0 when
it was deleted. `audit-register-hygiene.py … P1-CORRECTION-FINDINGS.md` remains exit 1 `no-counter` —
pre-existing, out of scope, unchanged.
