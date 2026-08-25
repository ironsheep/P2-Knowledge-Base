# Constant definition home — design for «#295» (plan §6)

**Status:** DESIGN, phase 1 of a two-phase task. Nothing implemented. No YAML created, edited or
deleted by this pass. Phase 2 implements the decisions below without re-deciding any of them.

**Findings addressed:** F-325 (`CONFIRMED`), F-326 (`CONFIRMED`), and — by the call recorded in
**D-D** — F-331 (`CONFIRMED`).

**Governing rules:** `P2KB-YAML-AUTHORING-GUIDE.md` R1 · R4 · R5 · R6 · R7 · R9, and plan decisions
D1 (three targets), D3 (match the source), D4 (ship only what the source states).

---

## 0. Measured entry state — every number re-verified against disk, 2026-08-25

Five of the numbers I was handed were stale or wrong. All values below were measured this session.

| Quantity | Prompt / body says | **Measured** | Note |
|---|---|---|---|
| `audit-constant-fidelity.py` Tier 1 `[UNDEFINED]` | body 50 → C1 **55** | **55** | C1 is right, body is stale |
| Tier 2 `[CONTRADICT]` advisories | 5 | **5** | «#296»'s target, not ours |
| Records in `spin2-builtin-symbols-complete.yaml` | 68 | **68** (48 of them `P_`) | correct |
| Distinct constants referenced by the KB | 122 | **118** raw / **115** real names | ✗ **body wrong** |
| Distinct `P_` constants in the tool's truth side | — | **120** | v51-era |
| Distinct `P_` constants in Spin2 v55 | tool docstring says 100 | **116** | ✗ **tool's own docstring wrong** |
| Constants the KB currently defines | — | **58** (48 + 17, 7 overlapping) | two homes already |
| Next free register ID | body F-328 → C3 **F-336** | **F-336** | C3 right; `audit-register-hygiene.py` re-run, `CLEAN`, `next-ID counter: F-336` |
| F-325 register line | body `:190` → C2 `:674` | **`:752`** | ✗ **both stale — resolve by ID** |
| F-326 register line | body `:207` → C2 `:769` | **`:769`** | C2 right |
| Datasheet six-field legend | C4 `:1052-1058` | **`:1054-1059`** | ✗ C4 off by 2 (the register entry itself is right) |
| Hardware Manual six-field legend | C4 `:785` | **`:786-791`** | ✗ C4 off by 1 |
| `%AAAA`/`%BBBB` table double-sourced | C5 | **confirmed** — datasheet `:1063-1074`, HW manual `:793-806`, cell-identical | C5 right |
| Shipped `pasm2/wrpin.yaml` `input_selectors:` | C5 "check it" | **correct, matches both** incl. `x101`=−3, `x111`=−1 | **nothing to add** |

Entry gates, all green before any change: `validate-crossref-keys.py` **0 unresolved / exit 0** ·
`verify-yaml-format.py` **1129/1129 parsed / exit 0** · `audit-yaml-claim-sourcing.py` **Tier 1 none
/ exit 0** (84 Tier 2 advisories) · `audit-constant-fidelity.py` **exit 1, 55 Tier 1**.

---

## D-A. Where does a definition live?

### The homes, and the boundary between them

**One home per fact — and there are two *different* facts here, so there are two homes.** Naming
them precisely is what stops phase 2 recreating F-321/F-323.

| Home | Owns | Does **not** own |
|---|---|---|
| **`deliverables/ai/P2/language/spin2/symbols/spin2-builtin-symbols-complete.yaml`** | **The per-constant record**: this name → the source's wording, its 32-bit value, its bit pattern, its group | how the hardware behaves |
| **`deliverables/ai/P2/architecture/pin-drive-configuration.yaml`** *(new)* | **The `%M..M` field**: its sub-field ranges, the drive ladder *by encoding*, the DIR/OUT rule, and the composed idioms | any per-constant description |
| **`deliverables/ai/P2/architecture/smart_pins.yaml`** `configuration_format:` *(exists)* | **The 32-bit word**: the six fields' bit ranges and the `%TT` behaviour-by-context table | the `%M..M` internals — it points at the new file |

"What does this name put in the word" and "what does the hardware do with that field" are different
facts. Both homes are legitimate **provided the new file never states a per-constant description**
— see the hard constraint in **D-C**.

### Where each of the 55 lands

**All 55 land in `spin2-builtin-symbols-complete.yaml`, as records.** There is no split. Every one
of the 55 is a name in the v55 "Built-In Symbols for Smart Pin Configuration" table, and that table
is exactly what this file catalogues. The drive-strength five (`P_HIGH_150K` · `P_HIGH_15K` ·
`P_HIGH_1K5` · `P_LOW_15K` · `P_LOW_1K5`, added by «#293»'s removal) are **not** an exception: they
get records here like the rest, and `pin-drive-configuration.yaml` reaches them by *encoding*, never
by restating their descriptions.

### Current record shape — read, and matched EXACTLY

The file is 959 lines: a header, `spin2_builtin_symbols:` with a `symbols:` list of 68 records, then
four trailing top-level blocks. The record shape (verbatim, `:586-596`):

```yaml
    - symbol_id: "p_high_100ua"
      symbol_name: "P_HIGH_100UA"
      category: "smartpin"
      subcategory: "high_drive_config"
      value: "$0000_2800"
      bit_pattern: "%0000_0000_000_0000000101000_00_00000_0"
      description: "Drive high 100μA"
      usage_context:
        - "SmartPin input/output configuration (WRPIN)"
        - "High-side drive strength selection"
      related_symbols: ["P_HIGH_1K5", "P_HIGH_15K", "P_HIGH_FAST", "P_HIGH_10UA"]
      hardware_relationship: "SmartPin output polarity control"
```

**Matching it exactly. Not changing it.** Nothing else reads this shape by field name — the two
consumers are `audit-constant-fidelity.py` (Form C: `symbol_name:` + `description:`) and the MCP,
which serves parsed YAML. Field frequency across the 68: `symbol_id`/`symbol_name`/`category`/
`subcategory`/`value`/`description`/`hardware_relationship` 68 each, `related_symbols` 67,
`usage_context` 63, `bit_pattern` 53.

**I verified the shape is trustworthy before adopting it.** All 48 existing `P_` records' `value:`
and `bit_pattern:` match the v55 table **exactly, zero mismatches** — so `bit_pattern` is the v55
`%value` column copied, and `value` is that pattern in hex, and both can be filled mechanically.
Fourteen `description:` values are *not* the source's wording; that is handled in **D-G step 3**.

### Rules for the four non-quoted fields (mechanical, no judgement)

- `symbol_id:` — `symbol_name` lowercased. Existing convention, no exceptions.
- `category:` — `"smartpin"` for all. (Real categories in the file: smartpin 48, system 8, clock 5,
  streamer 4, events 3.)
- `subcategory:` — from the file's existing vocabulary, per the table in **D-G step 2**. One new
  value is created: `b_input_selection` (the A-side already has `a_input_selection`).
- `usage_context:` / `hardware_relationship:` — **copied verbatim from an existing sibling record in
  the same `subcategory:`. Never newly authored.** Copying a structural group label onto a co-member
  of a "pick one" group the source itself defines adds no claim; writing a fresh sentence would be
  R9 inference. Where the subcategory is new, use the A-side sibling with A→B substituted.

---

## D-B. What does one definition record look like?

**Source wording is taken from Spin2 v55, which supersedes v51 (F4).** The two disagree for 20
constants, 8 of them in the 55 — see **D-E**. Two mechanical de-escapings apply and are *not*
glosses: `spin2-v55-text.txt` is an HTML-entity-escaped extraction, so `&gt;`→`>`, `&lt;`→`<`,
`&amp;`→`&`; and a description containing a literal `|` (only `P_OR_AB`) must be read from the
*third* pipe-delimited cell onward, not the last.

### 1 — a drive-strength selector

Source, verbatim: `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt:1503`
> `| %0000_0000_000_0000000001000_00_00000_0 | P_HIGH_1K5 | Drive high 1.5kΩ`

```yaml
    - symbol_id: "p_high_1k5"
      symbol_name: "P_HIGH_1K5"
      category: "smartpin"
      subcategory: "high_drive_config"
      value: "$0000_0800"
      bit_pattern: "%0000_0000_000_0000000001000_00_00000_0"
      description: "Drive high 1.5kΩ"
      usage_context:
        - "SmartPin input/output configuration (WRPIN)"
        - "High-side drive strength selection"
      related_symbols: ["P_HIGH_FAST", "P_HIGH_15K", "P_HIGH_150K", "P_HIGH_FLOAT"]
      hardware_relationship: "SmartPin output polarity control"
```

### 2 — a time/counter constant from the v55 table

Source, verbatim: `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt:1551`
> `| %0000_0000_000_0000000000000_00_10101_0 | P_COUNTER_TICKS | For periods of A in X+ ticks, count ticks`

```yaml
    - symbol_id: "p_counter_ticks"
      symbol_name: "P_COUNTER_TICKS"
      category: "smartpin"
      subcategory: "operating_modes"
      value: "$0000_002A"
      bit_pattern: "%0000_0000_000_0000000000000_00_10101_0"
      description: "For periods of A in X+ ticks, count ticks"
      usage_context:
        - "SmartPin mode selection (WRPIN)"
        - "Smart pin operating mode"
      related_symbols: ["P_COUNTER_HIGHS", "P_COUNTER_PERIODS", "P_PERIODS_TICKS"]
      hardware_relationship: "SmartPin operating mode selector"
```

### 3 — an ADC selector

Source, verbatim: `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt:1466`
> `| %0000_0000_000_1000000000000_00_00000_0 | P_ADC_GIO | ADC GIO → IN, output OUT`

```yaml
    - symbol_id: "p_adc_gio"
      symbol_name: "P_ADC_GIO"
      category: "smartpin"
      subcategory: "input_logic_mode"
      value: "$0010_0000"
      bit_pattern: "%0000_0000_000_1000000000000_00_00000_0"
      description: "ADC GIO → IN, output OUT"
      usage_context:
        - "SmartPin input/output configuration (WRPIN)"
        - "Low-level pin mode selection"
      related_symbols: ["P_ADC_VIO", "P_ADC_FLOAT", "P_ADC_1X"]
      hardware_relationship: "SmartPin low-level pin mode selector"
```

**No clarifying gloss anywhere.** `P_ADC_30X` is worded `"ADC 31.6x → IN, output OUT"` because that
is what the source says, despite the name reading `30X`. `P_DAC_124R_3V` is worded
`"DAC 123.75Ω, 3.3V peak, ADC 1x → IN"` for the same reason. Correcting either would be inference
(R9) and would trip the fidelity tool's `QUANTITY` check against its own truth table.

### Findability — the part the gate does not measure, and the reason the sprint exists

`generate-p2kb-index.py` `harvest_aliases_from_yaml()` harvests **top-level `aliases:` only**. This
file has no top-level `aliases:` key, so **not one of its 48 constants is reachable by name through
`p2kb_get`** — the index holds 12 `P_` aliases in total, all contributed by other files. Defining
55 more constants in a file nothing can look up satisfies the instrument and leaves the reporting
agent exactly where it started.

**Phase 2 adds a top-level `aliases:` list naming every constant the file defines** (116 after the
add). Cost: one block. Effect: every `P_` name resolves to its definition home. Aliases are a lookup
index, not a definition, so this does not violate R4; a handful become multi-target arrays
(`P_SYNC_RX`, `P_PLUS1_B`, `P_MINUS1_B`, `P_TT_*`, `P_OE`, `P_CHANNEL`, `P_BITDAC` are already
aliased from `wrpin.yaml`/`smart_pins.yaml`), which the v3.4.0 array form supports and reports.
Existing aliases elsewhere are **not** removed.

---

## D-C. `architecture/pin-drive-configuration.yaml`

### The hard constraint that makes one-home hold

🔴 **This file MUST NOT contain a YAML mapping whose KEY is a constant name and whose value is a
description.** `audit-constant-fidelity.py` `DEF_RE` (`^\s*"?([A-Z][A-Z0-9_]{2,})"?\s*:\s*(.+?)\s*$`)
reads that shape as a **definition**, which would make the drive ladder a second definition home for
16 constants and re-manufacture F-321/F-323 inside the very task chartered to end it — and would
raise a Tier 1 `DIVERGENT` the moment a word differed.

**The file therefore expresses the ladder by ENCODING, not by name→description.** A constant name
may appear as a *value* (`constant: "P_HIGH_15K"`) or inside prose; never as a defining key. That is
also what the source itself is: the datasheet's legend is a `HHH/LLL` → drive table, not a symbol
list.

### Sources — all four documentary, double-sourced where it matters

| Fact | Source | `file:line` |
|---|---|---|
| Six-field `D` layout | Silicon Doc | `sources/silicon-doc/part4-smart-pins.txt:10` |
| `%M..M: low-level pin control` + the deferral (F-326's evidence) | Silicon Doc | `part4-smart-pins.txt:55-58` |
| `(M) Pin Mode` table, `M[12:0]` as `mmmm_CIOHHHLLL` | P2 Datasheet 2022/11/01 p.24 | `sources/p2-datasheet/p2-datasheet-text.txt:1094-1121` |
| …same table, cell-identical | P2 Hardware Manual 2022/11/01 | `sources/p2-hardware-manual/p2-hardware-manual-text.txt:831-835` |
| Pin Mode Legend: `C`, `I`, `O`, `HHH/LLL` ladder, field definitions | P2 Datasheet p.24 | `p2-datasheet-text.txt:1131-1147`; reconciled table at `sources/p2-datasheet/complete-tables-reference.md:241-283` |
| `DIR = direction bit; 0: input (float), 1: output (drive)` | P2 Datasheet | `p2-datasheet-text.txt:1144` · HW manual `:871` |
| `OE = digital output enable (when DIR bit high)` | P2 Datasheet | `p2-datasheet-text.txt:1134` |
| Ladder in one sentence | P2 Datasheet feature list | `p2-datasheet-text.txt:117` |
| `for smart pin mode off (%SSSSS = %00000): DIR enables output` | Silicon Doc | `part4-smart-pins.txt:74-76` |
| Drive ladder read off the equivalent-schematic figures (third path) | Datasheet pp.27-32 | `p2-datasheet/complete-tables-reference.md:325-338` |
| **Empirical:** "the far pin holds the net through a **15 kΩ drive** while the near pin drives it hard" | **EF-063** | `external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md:827` |
| **Empirical:** "P8..P31 held at a **15 kΩ low with `DIR` high**, so an undriven pin reads 0" | **EF-064** | `P2-EMPIRICAL-FINDINGS.md:840` |
| **Empirical rig, the composition as run on silicon** | EF-063/EF-064 source | `.../campaigns/2026-08-manual-corrections/tests/test-f272-streamer-dac-tt.spin2:212-219` |

### 🔴 A correction to F-322 that phase 2 must not inherit

F-322 states: *"What the source actually prescribes — same file, §'Weak Pull-Up':
`WRPIN(pin, P_HIGH_15K | P_LOW_FLOAT)`"*, citing `part4-smart-pins.txt`.

**That section does not exist.** Case-insensitive search of `part4-smart-pins.txt` for
*pull-up*/*pull up*/*pullup*/*pull-down* returns **zero hits**. Across all of
`engineering/ingestion/sources/`, the only pull-up mentions are **external** resistors — v55 `:27`
("in case no pull-up resistor is present on P62") and the datasheet `:310` ("Connect to a resistor
to pull up to 3.3 V"). **No Parallax documentary source states a `P_HIGH_15K | P_LOW_FLOAT` idiom.**

Under D4 that string may **not** be shipped as sourced. What *is* available is stronger: the
**empirical** composition, run on real silicon (EF-063/EF-064), which is `WRPIN(pin, P_HIGH_15K)` +
`DIR=1, OUT=1` — and which does **not** include `P_LOW_FLOAT`. The idioms below are worded from
that, and the `P_LOW_FLOAT` variant is **not shipped**. Routed as a register finding — **R2** in
**D-F**.

### File skeleton

```yaml
# Pin Drive Configuration - the WRPIN %M..M field
# Single definition home for the 13-bit low-level pin-control field's sub-fields,
# the drive ladder, and the DIR/OUT rule that governs when a drive setting is active.
# Per-constant definitions live in language/spin2/symbols/spin2-builtin-symbols-complete.yaml.

component: Pin_Drive_Configuration
category: io_system
aliases:
  - "pin drive configuration"
  - "drive strength"
  - "weak drive"
  - "pull-up"            # what a reader searches for; the page explains the P2 has none
  - "pull-down"
  - "open drain"
  - "M field"
  - "HHH"
  - "LLL"
  - "WRPIN M field"

description: |
  ...one paragraph, from the datasheet's own words...

source: "Parallax P2 Datasheet 2022/11/01 p.24 (M) Pin Mode + Pin Mode Legend,
  engineering/ingestion/sources/p2-datasheet/p2-datasheet-text.txt:1094-1147; identical in
  P2 Hardware Manual 2022/11/01, p2-hardware-manual-text.txt:831-861; Silicon Doc v35
  part4-smart-pins.txt:55-76"

field_position:                       # where M sits in the 32-bit word
  wrpin_d_operand: "%AAAA_BBBB_FFF_MMMMMMMMMMMMM_TT_SSSSS_0"
  bits: "20:8"
  width: 13
  full_word_reference: "architecture/smart_pins.yaml (configuration_format)"
  source: "..."

sub_fields:                           # F-324 / R7 — every sub-field gets its range
  mode_select:      { bits: "M[12:9]",  purpose: "low-level pin mode", source: "..." }
  in_out_sampling:  { bits: "M[8]",     legend: "C", ... }
  in_polarity:      { bits: "M[7]",     legend: "I", ... }
  output_polarity:  { bits: "M[6]",     legend: "O", ... }
  drive_high:       { bits: "M[5:3]",   legend: "HHH", ... }
  drive_low:        { bits: "M[2:0]",   legend: "LLL", ... }

drive_ladder:                         # BY ENCODING — never name:description
  applies_to: "HHH (M[5:3], high side) and LLL (M[2:0], low side), selected independently"
  source: "..."
  encoding:
    - { bits: "%000", drive: "Fast",    high_constant: "P_HIGH_FAST",  low_constant: "P_LOW_FAST" }
    - { bits: "%001", drive: "1.5 kΩ",  high_constant: "P_HIGH_1K5",   low_constant: "P_LOW_1K5" }
    - { bits: "%010", drive: "15 kΩ",   high_constant: "P_HIGH_15K",   low_constant: "P_LOW_15K" }
    - { bits: "%011", drive: "150 kΩ",  high_constant: "P_HIGH_150K",  low_constant: "P_LOW_150K" }
    - { bits: "%100", drive: "1 mA",    high_constant: "P_HIGH_1MA",   low_constant: "P_LOW_1MA" }
    - { bits: "%101", drive: "100 µA",  high_constant: "P_HIGH_100UA", low_constant: "P_LOW_100UA" }
    - { bits: "%110", drive: "10 µA",   high_constant: "P_HIGH_10UA",  low_constant: "P_LOW_10UA" }
    - { bits: "%111", drive: "Float",   high_constant: "P_HIGH_FLOAT", low_constant: "P_LOW_FLOAT" }
  definitions_live_in: "language/spin2/symbols/spin2-builtin-symbols-complete.yaml"

dir_and_out_rule:                     # the sentence F-322 says no file contains
  ...

idioms:
  ...

related:
  - architecture/smart_pins.yaml
  - language/pasm2/wrpin.yaml
  - language/spin2/methods/wrpin.yaml
  - language/spin2/symbols/spin2-builtin-symbols-complete.yaml
```

Every top-level block that states a physical quantity carries its own `source:`. This is not
optional: the file will cite, so `audit-yaml-claim-sourcing.py` promotes any uncited
quantity-bearing block in it to **Tier 1 blocking**. `drive_ladder:` is the block that matters.

### `dir_and_out_rule:` — literal

```yaml
dir_and_out_rule:
  why_this_block_exists: |
    A drive-strength selection is active only while the pin drives. Setting a drive strength
    and then clearing DIR leaves a plain high-impedance pin, with the selection inactive.
  dir: "direction bit; 0: input (float), 1: output (drive)"
  out: "output latch bit; 0: low, 1: high."
  oe: "digital output enable (when DIR bit high)"
  smart_pin_mode_off: "for smart pin mode off (%SSSSS = %00000): DIR enables output"
  source: "Parallax P2 Datasheet 2022/11/01 p.24 Pin Mode Legend, p2-datasheet-text.txt:1134,1144
    (identical in p2-hardware-manual-text.txt:871); Silicon Doc v35 part4-smart-pins.txt:74-76"
```

Note `why_this_block_exists:` states no number and names no constant; it restates the two cited
sentences' consequence. If phase 2 judges even that to be a step beyond the source, delete the key —
the three quoted lines carry the rule on their own.

### Two literal worked idioms — DIR stated in both

🔴 **DIR is stated in every idiom, because F-322 is precisely the failure of omitting it.**

```yaml
idioms:
  note: |
    The P2 has no pull-up or pull-down resistors. Where a design calls for one, the pin drives
    weakly in that direction; the drive is active only while DIR is high.
  source: "Parallax P2 Datasheet 2022/11/01 p.24 Pin Mode Legend (drive ladder and the DIR
    definition), p2-datasheet-text.txt:1131-1147; compositions below are hardware-verified —
    EF-063 and EF-064 in
    engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md:827,840"

  weak_high:
    intent: "hold a line high weakly, so a stronger external drive can overpower it"
    mode_word: "P_HIGH_15K"
    dir: "1 — required; with DIR = 0 the pin floats and the 15 kΩ drive is inactive"
    out: "1 — the output latch selects the high side"
    drive_high: "%010 = 15 kΩ (M[5:3])"
    drive_low: "%000 = Fast (M[2:0], default) — reached only if OUT goes to 0"
    spin2: |
      pinclear(pin)                 ' clear any previous smart-pin configuration
      wrpin(pin, P_HIGH_15K)        ' high side drives through 15 kOhm
      pinhigh(pin)                  ' DIR = 1, OUT = 1 -- without this the pin floats
      level := pinread(pin)         ' reads 1 unless something stronger holds the line low
    evidence: "Hardware-verified: EF-063's jumper-continuity rig holds a net through a 15 kOhm
      drive and is overpowered by a hard drive on the same wire (P2-EMPIRICAL-FINDINGS.md:827);
      the code is the rig's own weak_read(), campaigns/2026-08-manual-corrections/tests/
      test-f272-streamer-dac-tt.spin2:212-219. Date/rig 2026-08-20, real P2."

  weak_low:
    intent: "hold a line low weakly, so an undriven pin reads 0 for a stated reason"
    mode_word: "P_LOW_15K"
    dir: "1 — required; with DIR = 0 the pin floats and the 15 kΩ drive is inactive"
    out: "0 — the output latch selects the low side"
    drive_low: "%010 = 15 kΩ (M[2:0])"
    drive_high: "%000 = Fast (M[5:3], default) — reached only if OUT goes to 1"
    spin2: |
      pinclear(pin)                 ' clear any previous smart-pin configuration
      wrpin(pin, P_LOW_15K)         ' low side drives through 15 kOhm
      pinlow(pin)                   ' DIR = 1, OUT = 0 -- without this the pin floats
      level := pinread(pin)         ' reads 0 unless something stronger holds the line high
    evidence: "Hardware-verified: EF-064 held P8..P31 at a 15 kOhm low with DIR high as a canvas,
      'so an undriven pin reads 0 for a stated reason instead of floating, while any driven pin
      overpowers the pull and reads 1' (P2-EMPIRICAL-FINDINGS.md:840). Date/rig 2026-08-20,
      real P2."
```

Both examples must compile under `pnut-ts` and be read for semantics (R8) before the file ships.

### What is NOT documented, under D4

Named here so the omissions are deliberate rather than silent:

- **Open-drain / open-source.** Not stated by any Parallax source as a `P_*` composition. (A
  community driver in the ingestion tree uses `P_HIGH_FLOAT` "requires external pull-up" — upstream
  lead, never citable.)
- **Keeper / bus-hold.** No source.
- **The `P_HIGH_15K | P_LOW_FLOAT` variant.** No documentary source (see the F-322 correction above)
  and no empirical record. **Gap filed, not content shipped** — **R1** in **D-F**.
- **Any per-pin current or impedance figure** beyond the eight ladder rungs the legend states. F-327
  is what inventing those looks like.

---

## D-D. `wrpin.yaml`'s `M` field, and where F-331 gets fixed

### The two `wrpin.yaml` files, and which is the home

Neither. **Both point at `architecture/smart_pins.yaml`, which is already the home** —
`configuration_format:` (`smart_pins.yaml:148-280`) carries `wrpin_d_parameter:`, an empirically
grounded `composition_rule:` (EF-054), and all six `fields:` with correct bit ranges and purposes
(`m` = "Low-level pin control (drive strength, DAC, ADC)" at `20:8`; `tt` = "Pin DIR/OUT control" at
`7:6` with the four-context behaviour table; `sssss` = "Smart pin mode selector (32 modes)").
`spin2/methods/wrpin.yaml:60` **already says so**: *"Full table: architecture/smart_pins.yaml
(configuration_format.fields.tt.behavior_by_context)"*. The deferral target exists; three files just
restate it anyway.

So this is not two copies, it is **three**, and D1's "expand or repoint" resolves to **repoint** —
which is also R4's "deletion is the correction".

### F-331 is fixed HERE, by «#295», not by «#296»

**The call, and why.** F-331's location is `pasm2/wrpin.yaml:34-36` — the exact three lines D1's
target 3 names. «#295» runs before «#296». If «#296» owned it, either «#295» edits those lines and
leaves them wrong (shipping a known defect through a protection point), or «#295» skips them and
«#296» re-opens a file «#295» just closed. One task, one edit.

**The evidence is now triple-sourced**, one better than F-331 records: the Silicon Doc agrees with
the datasheet and the Hardware Manual — `part4-smart-pins.txt:59` reads `%TT: pin DIR/OUT control
(default = %00)` and `:55` reads `%M..M: low-level pin control`. Three sources, and none says
"DAC/output mode", "DAC/output value", or "+ smart-pin mode".

**The repoint also settles the wording question F-331 leaves open.** The three sources word `M` two
ways ("pin mode" / "low-level pin control"); pointing at the single home means phase 2 picks no
wording at all, and `smart_pins.yaml` already carries the Silicon Doc's.

### The edits

**A. `deliverables/ai/P2/language/pasm2/wrpin.yaml:30-36`** — replace the six `fields:` descriptions
with a pointer plus the two sub-field pointers the deferral was hiding:

```yaml
  fields:
    reference: "architecture/smart_pins.yaml (configuration_format.fields) — all six fields,
      with bit ranges. Silicon Doc part4-smart-pins.txt:10-59."
    M_sub_fields: "architecture/pin-drive-configuration.yaml — the 13-bit field's sub-fields,
      the drive ladder and the DIR/OUT rule."
    input_selectors: "see input_selectors below"
```

Resolves **F-326** (the stub now follows its pointer) and **F-331** (the three wrong descriptions are
removed rather than re-worded). The correct `input_selectors:` block at `:37-52` is **not touched** —
C5 confirmed it against both new sources.

**B. `deliverables/ai/P2/language/spin2/methods/wrpin.yaml`** — stop defining `P_` constants:

- `common_smart_modes:` (`:98-111`, 13 keys) — **delete**, replaced by a pointer to the symbols file.
  This block is 13 Form-A definitions. Phase 2 adds all 13 of those names to the symbols file, so
  **leaving it turns 7 duplicate definitions into 17.** The duplication is created by this task and
  must be resolved by it.
- `tt_field.constants:` (`:42-46`, 4 keys) — **delete**, replaced by a pointer to
  `architecture/smart_pins.yaml (configuration_format.fields.tt.constants)`, which already carries
  the same four with their `value`/`binary`/**and the `P_OE`/`P_CHANNEL`/`P_BITDAC` aliases**, so
  nothing is lost. Removes 4 of the 7 pre-existing duplicates.
- Everything else in `tt_field:` — `context_dependent:`, `p_oe_required_for:`,
  `one_bit_three_names:`, `when_smart_pin_on:`, `source_selection:` — is **kept untouched**. It is
  cited, correct, and it is field *behaviour*, not a per-constant definition.

Net effect: **KB `P_` definitions drop from two homes to one.** The 7 existing duplicates
(`P_NORMAL`, `P_PWM_TRIANGLE`, `P_REPOSITORY`, `P_TT_00`, `P_TT_01`, `P_TT_10`, `P_TT_11`) go to
zero, and `audit-constant-fidelity.py` reports exactly one definition per constant.

**C. `deliverables/ai/P2/architecture/smart_pins.yaml`** — the *only* edit is adding a pointer inside
`configuration_format.fields.m:` to `architecture/pin-drive-configuration.yaml`. Its existing
`dac_mode_trigger:` and `bit_dac:` lines stay: they are cited Silicon Doc facts about the field's
place in the word, and moving them is «#298»'s promotion-filter question, not this task's.

---

## D-E. The v55 blind spot — deliverable for «#305»

`audit-constant-fidelity.py` cannot see `sources/spin2-v55/spin2-v55-text.txt`: `harvest_source()`
globs `*.md` only, and `ROW_RE` wants the constant in column 1 of a line beginning `|`, while this
file is a `.txt` whose rows are tab-indented with `%value` in column 1 and the name in column 2.
Recorded as the tool's own `KNOWN LIMITATIONS` item 4. **I read it by hand. `TRUTH_ROOTS` untouched.**

| Measure | Value |
|---|---|
| Distinct `P_` constants **v55 carries** | **116** (114 table rows, lines 1419-1562; two rows carry a name *and* a brevity alias — `P_TRUE_OUTPUT`/`P_TRUE_OUT`, `P_INVERT_OUTPUT`/`P_INVERT_OUT`) |
| Distinct `P_` names on the tool's **v51-era truth side** | **120** |
| Distinct `P_` names the **shipped KB references** | **115** (118 raw, less 3 wildcard-prose artifacts — see **D-F**) |
| The KB currently **defines** | **58** |
| **v55 names the truth side is missing** | **0** |
| **Constants v55 RE-DESCRIBES** vs v51 | **20**, of which **8 are among the 55** |
| v51-only names absent from v55 | **4** — `P_COMPARATOR`, `P_COMPARATOR_FB`, `P_FLOAT`, `P_PASS`; the KB references and defines **none** |

**The gap is not missing names — it is 20 superseded descriptions.** The tool's docstring frames the
blind spot as "wherever v55 ADDED or RE-DESCRIBED"; the ADDED half is empty and the RE-DESCRIBED half
is the whole exposure. Its stated figure of "100 distinct `P_` constants" in v55 is **wrong — it is
116.** Both corrections belong to «#305» when it arms this gate.

**Eight redescriptions land inside the 55, so phase 2 hits them directly.** Word from v55:

| Constant | v51 (what the tool will compare against) | **v55 — use this** |
|---|---|---|
| `P_ADC_EXT` | "ADC ext trigger" | "ADC sample/filter/capture, externally clocked" |
| `P_COUNT_HIGHS` | "Count A-highs" | "Inc on A-high, optionally dec on B-high" |
| `P_COUNT_RISES` | "Count A-rises" | "Inc on A-rise, optionally dec on B-rise" |
| `P_PWM_SMPS` | "PWM SMPS" | "PWM switch-mode power supply I/O" |
| `P_REG_UP` | "Inc on A-rise & B-high" | "Inc on A-rise when B-high" |
| `P_REG_UP_DOWN` | "Inc on A-rise, dec on A-fall" | "Inc on A-rise when B-high, dec on A-rise when B-low" |
| `P_SYNC_RX` | "Sync serial receive" | "Synchronous serial receive" |
| `P_SYNC_TX` | "Sync serial transmit" | "Synchronous serial transmit" |

**Divergence check — none of the eight breaks the gate.** `[UNDEFINED]` only asks whether a
definition exists. `QUANTITY` needs both sides to state a magnitude (none do). Tier 2 `CONTRADICT`
needs a fixed-lexicon concept clash (`drive_high`/`bias_up`/`float`/`invert`/`true` — none present).
Verified against the tool's own predicates: wording from v55 drives Tier 1 to 0 and adds no Tier 2.

The other 12 redescriptions sit on constants the KB already defines; 10 of those are handled anyway
by **D-G step 3**, and 2 (`P_TRUE_OUT`, `P_INVERT_OUT`) differ only by v51's parenthetical
`(for brevity)` and are already correct at HEAD.

**One further tool artifact, cosmetic here.** `strip_desc()` splits a row on `|` and keeps the last
cell, so a description *containing* a pipe is truncated. Only `P_OR_AB` ("Select A | B, B") does, and
the tool truncates both sides identically, so it self-cancels. The shipped record at
`spin2-builtin-symbols-complete.yaml:332` is **correct and must not be "fixed"** to the tool's
displayed `"B, B"`.

---

## D-F. Fabricated-name check

**Method.** Every `P_[A-Z0-9_]+` token in all 1129 KB YAMLs, differenced against the 116 v55 names,
then each residual put to `pnut-ts` — the legality arbiter — as `PUB main()` / `wrpin(0, NAME)`.
Five residuals, and only five.

### Genuine fabricated names — 2

| Name | `pnut-ts` | In v55? | In the v51 truth side? | Sites |
|---|---|---|---|---|
| **`P_LEVEL_B`** | **REJECTED** | no | no | `spin2-builtin-symbols-complete.yaml:427, 479, 492` |
| **`P_SCHMITT_B`** | **REJECTED** | no | no | `spin2-builtin-symbols-complete.yaml:453` |

All four sites are inside `related_symbols:` lists. Both are near-misses on legal siblings that *do*
exist (`P_LEVEL_A`, `P_LEVEL_A_FBN`, `P_LEVEL_B_FBP`, `P_LEVEL_B_FBN`; `P_SCHMITT_A`,
`P_SCHMITT_A_FB`, `P_SCHMITT_B_FB`) — all seven of which `pnut-ts` accepts, which is the control
proving the harness discriminates rather than rejecting everything.

**Not a definition gap. Do not invent definitions.** Per *"No fabricated names in KB tree — delete
invalid names outright"*, phase 2 **deletes the four list entries** and substitutes nothing (a
substitution would be R9 inference about what the author meant). Filed as **R3** in the table below.

**Why nothing has caught these:** `validate-crossref-keys.py` reads **top-level keys only**
(`if field_name not in content`), and every `related_symbols:` here is nested inside a record. That
is why the field reports "7 resolved" against a file holding 67 such lists. Worth a note to «#305»;
not this task's repair.

### Not names — 3

`P_ADC_`, `P_COMPARE_`, `P_DAC_` are the fidelity tool's `\b(P_[A-Z0-9_]+)\b` stopping at the `*` of
legitimate wildcard prose: `"Can combine with P_DAC_*, P_ADC_*, P_COMPARE_* modes"`
(`smart-pins/smart-pin-00000-normal-mode.yaml:129`), `"a P_ADC_* constant"`
(`streamer/dds-goertzel.yaml:27`), and `"Normal mode with P_DAC_*"`
(`smart-pins/smart-pin-000{10,11}-*.yaml:19{2,3}`). **No finding, no edit.**

### Register findings for phase 2 to file — F-336 onward, allocation re-checked at filing time

| Ref | Subject | Class |
|---|---|---|
| **R1** | **F-322 cites a Silicon Doc §"Weak Pull-Up" that does not exist.** Zero hits for pull-up/pull-down in `part4-smart-pins.txt`; the only pull-up mentions in `sources/` are external resistors. The `P_HIGH_15K \| P_LOW_FLOAT` idiom is unsourced. **«#296» must not ship that string as sourced.** Gap: a hardware-verified idiom set (D4's "file a gap") — extend the EF-063/EF-064 rig to sweep the ladder against a known load. | correction + gap |
| **R2** | Datasheet + Hardware Manual (agreeing, 2022/11/01) contradict the Silicon Doc on `%TT` in DAC_MODE: `00 = DIR enables DAC, M[7:0] sets DAC level` and `0x = OUT enables **DAC**…` vs Silicon Doc's `00 = OUT enables **ADC**…` / `0x = OUT enables **ADC**…`. Shipped `smart_pins.yaml` `fields.tt.behavior_by_context` follows the **minority** source. `p2-datasheet-text.txt:1175,1183` · `p2-hardware-manual-text.txt:897,905` · `part4-smart-pins.txt:83,98`. EF-054/EF-055 may already settle it. | source conflict |
| **R3** | `P_LEVEL_B` and `P_SCHMITT_B` are fabricated — `pnut-ts` rejects both, neither is in v55. 4 sites in `spin2-builtin-symbols-complete.yaml`. Deleted by phase 2 in the same pass; filed so the class is on record. | fabrication |
| **R4** | `audit-constant-fidelity.py`'s docstring states v55 carries **100** distinct `P_` constants; measured **116**. Its `KNOWN LIMITATIONS` item 4 also frames the blind spot as ADDED-or-REDESCRIBED when ADDED is **0** and REDESCRIBED is **20**. For «#305». | tool defect |
| **R5** | `validate-crossref-keys.py` validates **top-level keys only**, so nested `related_symbols:` (67 lists in one file) are never checked — which is how R3 survived. For «#305». | tool gap |

---

## D-G. Implementation plan

Ordered, mechanical. Phase 2 decides nothing.

**Preconditions.** `export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory
GIT_CONFIG_VALUE_0=/workspaces/P2-Knowledge-Base`. Back up
`spin2-builtin-symbols-complete.yaml` (959 lines) and `spin2/methods/wrpin.yaml` (161 lines) with
`engineering/tools/backup-file.sh` — Sacred Rule #1. `pasm2/wrpin.yaml` is 126 lines: no backup
owed, but the edit is surgical regardless.

1. **Extract the v55 table.** Parse `sources/spin2-v55/spin2-v55-text.txt:1419-1562` into
   `(name, value, description)`. Split each row on `|` with **maxsplit=2** (a description may contain
   a pipe). Un-escape `&gt;`/`&lt;`/`&amp;`. Take **all** names in the name cell (two rows carry two).
   Expect **116** distinct names.
2. **Add 68 records** to `spin2_builtin_symbols.symbols:` — the 55 required plus 13 more that give
   the file complete v55 coverage in the same pass (`P_ASYNC_RX`, `P_ASYNC_TX`, `P_DAC_DITHER_PWM`,
   `P_DAC_NOISE`, `P_HIGH_1MA`, `P_LOW_150K`, `P_LOW_1MA`, `P_NCO_DUTY`, `P_NCO_FREQ`, `P_PULSE`,
   `P_PWM_SAWTOOTH`, `P_QUADRATURE`, `P_TRANSITION`). Ten of those 13 are the ones currently defined
   in `spin2/methods/wrpin.yaml`, which step 5 deletes; the other three complete the drive ladder
   F-321 asks for. Shape per **D-B**. `bit_pattern` = the v55 `%value` verbatim; `value` = that
   pattern in hex, `$XXXX_XXXX`. Subcategory:

   | Family | `subcategory:` |
   |---|---|
   | `P_INVERT_B` | `b_input_config` |
   | `P_LOCAL_B` · `P_PLUS{1,2,3}_B` · `P_MINUS{1,2,3}_B` · `P_OUTBIT_B` | `b_input_selection` *(new)* |
   | `P_PLUS{2,3}_A` · `P_MINUS1_A` | `a_input_selection` |
   | `P_FILT1_AB` | `ab_input_combining` |
   | `P_SCHMITT_A` · `P_COMPARE_AB{,_FB}` · `P_LEVEL_A` · `P_ADC_*` (the 8 gain modes) · `P_DAC_*R_*V` | `input_logic_mode` |
   | `P_INVERT_OUTPUT` | `out_config` |
   | `P_HIGH_{1K5,15K,150K,FAST,1MA}` | `high_drive_config` |
   | `P_LOW_{1K5,15K,150K,1MA}` | `low_drive_config` |
   | every `%SSSSS` mode (`P_*_TICKS`, `P_COUNTER_*`, `P_COUNT_*`, `P_PERIODS_*`, `P_DAC_DITHER_RND`, `P_DAC_NOISE`, `P_PULSE`, `P_TRANSITION`, `P_NCO_*`, `P_PWM_*`, `P_QUADRATURE`, `P_REG_UP{,_DOWN}`, `P_ADC_{EXT,SCOPE}`, `P_USB_PAIR`, `P_SYNC_{TX,RX}`, `P_ASYNC_{TX,RX}`) | `operating_modes` |

   `usage_context:` / `hardware_relationship:` copied verbatim from a sibling in the same
   subcategory. Result: **136 records, 116 of them `P_`.**
3. **Re-word the 14 glossed descriptions** to v55 (`P_TRUE_A`, `P_INVERT_A`, `P_LOCAL_A`, `P_NORMAL`,
   `P_REPOSITORY`, `P_PWM_TRIANGLE`, `P_ADC`, `P_TT_00`, `P_TT_01`, `P_TT_10`, `P_TT_11`, `P_OE`,
   `P_BITDAC`, `P_CHANNEL`). These are live R1/D3 violations in the file being edited; leaving them
   ships a known defect through a protection point. The four `P_TT_*` glosses are the same class as
   F-331. Where a gloss carried behaviour (`P_TT_10`'s "Output disabled, OTHER source selected"), the
   behaviour is not lost — it is the field-behaviour home's, at `smart_pins.yaml`
   `configuration_format.fields.tt.behavior_by_context`; add a `behavior_reference:` key to those
   records naming it.
4. **Delete the 4 fabricated `related_symbols:` entries** — `P_LEVEL_B` at `:427, 479, 492`,
   `P_SCHMITT_B` at `:453`. Delete, substitute nothing.
5. **Add the top-level `aliases:` block** naming all 116 constants the file defines. Findability;
   see **D-B**.
6. **Create `deliverables/ai/P2/architecture/pin-drive-configuration.yaml`** per **D-C**. No
   constant-as-key mappings. Every quantity-bearing top-level block carries `source:`.
7. **Edit `language/pasm2/wrpin.yaml:30-36`** — repoint `fields:` (**D-D A**). Do not touch
   `input_selectors:`.
8. **Edit `language/spin2/methods/wrpin.yaml`** — delete `common_smart_modes:` and
   `tt_field.constants:`, replace each with a pointer (**D-D B**). Keep the rest of `tt_field:`.
9. **Edit `architecture/smart_pins.yaml`** — add the `fields.m:` pointer to the new file (**D-D C**).
   Nothing else.
10. **Compile both idiom examples**: `pnut-ts <file>.spin2`, and read them for semantics. A clean
    compile proves legality only — F-322 is eight examples that compiled and did not work.
11. **Annotate F-325, F-326 and F-331** in `engineering/operations/P2KB-CORRECTION-FINDINGS.md` with
    their traces. **Resolve by ID, not line** (`grep -n 'F-325' …`) — the body's `:190`/`:207` and
    C2's `:674` are all stale; F-325 is at `:752` today and will move again.
12. **File R1–R5** from **D-F** as F-336+. Re-check the allocation with
    `audit-register-hygiene.py engineering/operations/P2KB-CORRECTION-FINDINGS.md` immediately before
    filing; the hygiene gate rejects a finding filed `DONE` in an open-work register.
13. **Commit**, then **regenerate the index**, then validate — this order is required. Ordering
    rationale below.

### Verify — commands and expected values

| # | Command | Expected |
|---|---|---|
| V1 | `python3 engineering/tools/validation/audit-constant-fidelity.py --negative-control` | `Negative control PASSED` — run it first; a check that cannot fail has not been verified |
| V2 | `python3 engineering/tools/validation/audit-constant-fidelity.py` | **Tier 1: none**, `[UNDEFINED]` **0**, exit **0**. Tier 2 still **5** («#296»'s, not ours) |
| V3 | `… --inventory` | KB defines **116**; referenced **119**. Arithmetic: 115 real names today − 2 fabricated (step 4) + 3 newly recorded (`P_HIGH_1MA`, `P_LOW_150K`, `P_LOW_1MA`, currently referenced nowhere) = **116 real**, + the 3 wildcard-prose artifacts = 119. No `[DIVERGENT]` (one definition per constant), no `[ORPHAN]` (all 116 v55 names are present on the tool's truth side — measured, see **D-E**) |
| V4 | `python3 engineering/tools/verify-yaml-format.py` | 1130/1130 parsed, exit 0 |
| V5 | `python3 engineering/tools/validation/audit-yaml-claim-sourcing.py` | **Tier 1: none**, exit 0. Tier 2 stays 84 — if it rises, an uncited quantity block was added |
| V6 | `python3 engineering/tools/generate-p2kb-index.py` *(after commit)* | new key `p2kbArchPinDriveConfiguration`; alias count rises by ~104 |
| V7 | `python3 engineering/tools/validate-crossref-keys.py` | 0 unresolved, exit 0 |
| V8 | `pnut-ts` on both idiom examples | compile clean, then read for semantics |
| V9 | `python3 engineering/tools/validation/audit-register-hygiene.py engineering/operations/P2KB-CORRECTION-FINDINGS.md` | `CLEAN` |
| V10 | `grep -cP '\bP_LEVEL_B\b(?!_)\|\bP_SCHMITT_B\b(?!_)' -r deliverables/ai/P2/` | **0** |

**🔴 V6 must run after the commit, and V7 after V6.** `validate-crossref-keys.py` resolves against
`deliverables/ai/p2kb-index.json`, which will not contain `p2kbArchPinDriveConfiguration` until the
index is regenerated — so any `related:` entry pointing at the new file fails until then. And
`generate-p2kb-index.py` calls `get_git_mtime()`, which needs the file in git history. Commit →
regenerate → validate. Running V7 before V6 produces a red that means nothing.

**Every `related:` entry uses a FULL PATH, never a bare name.** Verified against the transformer:
`architecture/pin-drive-configuration.yaml` → `p2kbArchPinDriveConfiguration`;
`architecture/smart_pins.yaml` → `p2kbArchSmartPins`;
`language/spin2/symbols/spin2-builtin-symbols-complete.yaml` → `p2kbSpin2Spin2BuiltinSymbolsComplete`;
`language/pasm2/wrpin.yaml` → `p2kbPasm2Wrpin`; `language/spin2/methods/wrpin.yaml` → `p2kbSpin2Wrpin`.

**Protection point:** `[UNDEFINED]` 55 → 0 · crossref clean · format clean · claim-sourcing Tier 1
still none · F-325, F-326 and F-331 annotated with their traces, in the same pass.

---

## Risks phase 2 is most likely to get wrong

| # | Risk | Prevented by |
|---|---|---|
| 1 | Writing the drive ladder as `P_HIGH_15K: "Drive high 15kΩ"` in the new file — the natural shape, and it silently creates a **second definition home** for 16 constants, re-manufacturing F-321/F-323 inside the task that ends them | **D-C**'s hard constraint, with the exact `DEF_RE` that would fire; the ladder is specified **by encoding** |
| 2 | Adding the 13 mode records without deleting `common_smart_modes:` — turns 7 duplicate definitions into 17 | **D-D B** makes the deletion a numbered step; V3 catches the residue |
| 3 | Wording from the v51 extracts the tool's `[UNDEFINED]` lines cite — they are the **superseded** edition for 8 of the 55 | **D-E**'s explicit v51→v55 table; F4's precedence order |
| 4 | Shipping F-322's `P_HIGH_15K \| P_LOW_FLOAT` "Weak Pull-Up" idiom as sourced — a register finding *says* the source prescribes it, and **the section does not exist** | **D-C**'s correction, verified live not from the ledger; the idioms are grounded on EF-063/EF-064 instead, and the variant is filed as a gap |
| 5 | Omitting DIR from an idiom, or writing `PINFLOAT`/`DIRL` after configuring a drive — F-322's exact shape, and it compiles | DIR is a **required key** in every idiom, plus V8's read-for-semantics |
| 6 | Adding a `source:` to a *new top-level block* holding quantities without citing every sibling → the file flips from Tier 2 advisory to **Tier 1 blocking** | V5 with a stated expected value (84, not "passes"); **D-C** requires `source:` on every quantity-bearing block |
| 7 | Running `validate-crossref-keys.py` before regenerating the index and reading the red as a real failure | V6/V7 ordering called out with its mechanism |
| 8 | "Correcting" `P_OR_AB` to the tool's displayed `"B, B"`, or `P_ADC_30X` to `31.6x`, or `P_DAC_124R_3V` to `124Ω` | **D-B**'s no-gloss rule and **D-E**'s `strip_desc` note, each with the reason |
| 9 | Inventing a definition for `P_LEVEL_B`/`P_SCHMITT_B` because they look like the other 55 | **D-F**: `pnut-ts` rejects both; delete, substitute nothing |
| 10 | Resolving F-325/F-326 by the line numbers in the task body | **D-G step 11**: resolve by ID; the measured line for F-325 (`:752`) already differs from both the body and the correction |
