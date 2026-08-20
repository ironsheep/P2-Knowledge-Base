# P2KB Correction Findings — Consolidated Register

**Purpose:** the register of everything we find that is **wrong or needs correction** — primarily in the P2 Knowledge Base YAML (`deliverables/ai/P2/`), but also any other source/content correctness issue worth tracking. This is the hand-off document for the agent that corrects the P2KB (via `yaml-knowledge-base-maintenance`).

**This file carries OPEN work only.** Closed findings are archived, not kept here. Ask "what is
outstanding?" of this file alone — never re-derive completion state from an archive.

**How to use it:**
- When any work (manual production, audits, example compilation, ingestion, bench) surfaces something incorrect, **add it here** — do not leave it only in a per-manual note.
- Each finding gets an ID, a status, the exact location, what is wrong, the evidence, and the proposed correction.
- **Annotate as you fix, in the same pass** — flip the status, add an applied-note and source trace, and log newly-surfaced defects as new findings. A register whose statuses lag the YAML lies and invites re-chasing.
- **One finding lives in exactly one place.** When a finding is revised, **rewrite its entry in place**; never append a correction below the entry it corrects. The prior text is in git and in the archives.
- Consultation protocol (status-before-content, duplicate IDs are a STOP): `.claude/skills/REGISTER-CONSULTATION.md`.

**Status legend:** `CONFIRMED` (verified against an authority; ready to fix) · `NEEDS-VERIFICATION` (suspected; must be checked before acting) · `PARTIAL` (some of it applied; the rest still owed) · `DONE` (corrected + verified) · `WONTFIX` (investigated, not a defect) · `RESOLVED-INVALID` (the reported defect does not exist) · `TRACKED → ingestion` (real, but the resolution lives in the ingestion head).

**A fix applied but not yet validated is NOT done** — it stays here until its validation lands (the `[~]` rule from `punch-list-maintenance`). That covers a YAML edit awaiting its EF entry, and a manual fix awaiting its re-test.

**Authority order for P2 facts:** empirical / hardware-verified results in `engineering/ingestion/external-sources/hardware-verification/` (strongest — they have overturned every other tier) → the `pnut-ts` compiler, for legality only → Parallax documentary sources under `engineering/ingestion/sources/` → the published P2KB YAML. Community/forum material is an upstream lead, never a citable authority.

**No inference or derivation.** Every correction must trace to an authoritative source. Aligning a file to an authority it contradicts is fine; **inventing a value or claim that no source states — by computation, reasoning, or "it must logically be" — is not.** If a change can only be justified by inference, log it as a finding that needs a source. Match the source's wording, not an interpretive paraphrase.

**Next finding ID: `F-311`**

**Archives** — search them before re-filing; a finding that reappears is usually a regression:
- F-001…F-124 → `correction-sweeps/2026-06-13-P2KB-CORRECTION-FINDINGS-archive.md`
- F-125…F-266 (closed) → `correction-sweeps/2026-08-15-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-08-19 (18 findings: F-227, F-228, F-254, F-255, F-257, F-258, F-259, F-260, F-261, F-262, F-263, F-264, F-265, F-266, F-267, F-269, F-270, F-273) → `correction-sweeps/2026-08-19-P2KB-CORRECTION-FINDINGS-archive.md`

> **Swept 2026-08-19** per `punch-list-maintenance`, as **rename-then-trim** (the archive is a
> git-tracked rename of the original; both files are subtractions from a preserved copy — see the
> skill's project overlay for why building the output loses content). 18 findings archived, 3,559 →
> 2,478 lines. **Classified by STATUS TOKEN only.** Sixteen findings whose headline reads "source
> fixed"/"tool fixed" **stayed open**, because their status is still `CONFIRMED` and most say
> "render owed" — this file's own rule is that a fix applied but not yet validated is NOT done. A
> first pass that trusted the prose would have archived all sixteen. Verified with
> `audit-register-hygiene.py --sweep-check`, which reads the pre-sweep revision out of git.
>
> **Swept 2026-08-15** per `punch-list-maintenance`: 129 closed findings archived, 3,161 lines → this
> file. The previous sweep was deferred on 2026-06-20 pending G-004 and G-005; G-005 closed
> 2026-07-04, and G-004's remainder was found to be out of KB scope entirely (see its entry), so the
> deferral's condition is discharged.

---

## Carry-forward guardrails — investigated and settled; do NOT re-file (full detail in the archive)

- **F-002 (`WONTFIX`):** `?` / `||` operator-form failures were an agent usage error — the KB is correct (`??var` = XORO32 random; `ABS()` not `||`; `?` is the ternary operator).
- **F-036 (`WONTFIX`):** `calld.yaml` — LOC loading a 20-bit address into PA/PB/PTRA/PTRB is not a defect.
- **F-093 (`WONTFIX`):** `lockrel.yaml` C-flag polarity — the appendix's "inverted" claim is the error; the YAML is correct (C = lock-was-held).
- **F-114b (`RESOLVED-INVALID`):** the MIDI display modes KEYBOARD / GRID / ROLL / MONITOR do **not** exist in PNut v55 — do **not** add them to `midi.yaml` (it carries an explicit `not_supported:` claim).
- **Verified-resolved (don't re-chase):** the Jan-2026 streamer KB audit's issues were all reconciled in the 2026-05/06 passes (DAC routing, 32-pin groups, mode encoding, xcont/xzero phase wording, setxfrq 2³¹ formula, streamer symbols). Only the XZERO concept text was open and is fixed (F-003).

---

## Open — CONFIRMED corrections (2026-08-11, DeSilva reader-report sweep)

> **Sweep origin:** a reader reported that the DeSilva tutorial's Ch.1 "Experiment 3:
> Fading" does not fade on a P2 EVAL (#64000 Rev B) — copied, pasted, triple-checked.
> Root cause: the smart-pin mode was written **without `P_OE`**, so the smart pin
> generated the PWM but the pin's output driver stayed disabled. Confirmed against
> `language/spin2/methods/wrpin.yaml` `tt_field` — `when_smart_pin_on: "x0=output
> disabled, x1=output enabled (regardless of DIR)"` and `p_oe_required_for: "All output
> modes (NCO, PWM, Pulse, Transition, Serial TX, DAC, USB)"`. The manual was fixed the
> same pass; **the same class is still present in the KB's own examples**, below.
> Note this class had already been fixed once in DeSilva (v3.0.3 corrected the
> async-serial TX recipe to `P_ASYNC_TX | P_OE`) but was **not swept class-wide** —
> which is how the PWM example survived to a reader.

- **F-250 — the #64000 Eval Board Rev C guide was ingested with EVERY DIGIT MISSING; any
  numeric fact traced to it is unsafe.** `engineering/ingestion/sources/p2-eval-board/`
  was extracted with a text-layer tool, but that PDF's font encoding does not map numerals —
  `pdftotext` silently drops them. Evidence: the shipped `p2-eval-board-narrative.txt` has
  digits on **91 of 1315 lines**; `pdf-ocr --force-ocr` + re-extract yields **368**. Lines
  read *"The Propeller has cores, KB of hub RAM, and Smart I/O pins"* (8 / 512 / 64 gone)
  and *"Buffered LEDs on top eight I/O pins"* survives only because "eight" is spelled out.
  **Consequences:** (1) the LED pin map sat as `TBD` in `hardware/p2-eval-board.yaml` for
  months while the answer was in the repo (F-248) — no grep for `P56` could hit a document
  with no digits; (2) **every** voltage, current, capacity, pin number, part number and page
  reference sourced from this extraction is suspect; (3) the extraction audit and
  cross-source analysis both list "LED pins" as a *gap*, so the loss was mistaken for the
  source being silent. **→ TRACKED → ingestion:** re-ingest this source with forced OCR,
  re-verify every numeric claim already derived from it, and — the general lesson —
  **add a digit-density sanity check to the ingestion pass**: a hardware document whose
  extraction is nearly digit-free has failed, not been read. Worth spot-checking the other
  board/hardware sources for the same font family. Status: `CONFIRMED`.

- **F-251 — the "why do the LEDs glow when I touch a pin" explanation must account for the
  LED BUFFER, and the freshly-shipped DeSilva v3.0.5 aside does not.** The #64000 guide
  (feature 12) and both Edge module YAMLs describe the onboard LEDs as **buffered** — the P2
  pin drives a buffer *input*, and the buffer drives the LED. DeSilva v3.0.5's new Chapter 1
  aside "Why Your LEDs Glow When You Touch Them" instead explains the effect as microamps
  coupling *through the LED itself*, which would produce a faint glow. On a buffered board
  the floating **buffer input** picks up the coupling and the buffer drives the LED at full
  strength — which matches the reader's actual report ("the leds will light up", not "glow
  faintly"). The aside's conclusion (floating pins have no opinion; drive them or use
  pull-ups) is right; the mechanism is wrong. **→ manual head:** correct the aside in the
  next DeSilva patch. Also worth stating there that on the #64000 **P58-P63 are shared with
  the USB-data and memory signals**, so those LEDs are active at power-up and after reset by
  design — a second, entirely non-mysterious reason a reader sees lit LEDs. Status:
  `CONFIRMED`.

- **F-252 — the Getting Started guide hardcodes `LED = 56` with no board caveat (same class
  as the DeSilva fix).** `p2-getting-started-guide/opus-master/getting-started-body.md:558`
  declares `LED = 56  ' the pin our LED is on`, used by the blink examples at `:493` and
  `:408`. On a **P2 Edge 32MB PSRAM Module** P56 is the PSRAM **clock** — the example lights
  nothing and drives the memory bus; the LEDs there are **P38/P39**. This is exactly the
  failure a reader hit this session, and it lands in the guide most likely to be a
  newcomer's *first* P2 program. **Fix:** one line naming the per-board LED pins (the
  DeSilva Ch.1 aside is the model, but Getting Started wants a single sentence, not a
  sidetrack). Sources now in the KB: `hardware/edge-standard-module.yaml` (P56/P57),
  `hardware/edge-32mb-module.yaml` (P38/P39), `hardware/p2-eval-board.yaml` (P56-P63,
  P56/P57 free). **→ manual head.** Surfaced by the v1.16.2 YAML→Manual impact survey.
  Status: `CONFIRMED`.

---

## Forum docs-feedback (2026-08-16) — the DDS LUT is not fixed at 512 entries — F-302

**Origin:** Christof Eb., Parallax forum 2026-08-16, reviewing the *P2 Streamer Programming
Guide* §17.2. Raw post + full analysis at
`engineering/document-production/FORUM-NO-COMMMIT/Docs-findings-260819/` (gitignored — find it
by path). Same reviewer as F-256. His parenthetical *"(No, it does not need to be 512
entries.)"* is **correct**, and it lands on the KB as well as the manual.

### F-302 — `p2kbArchDdsGoertzel` states the DDS/Goertzel LUT window as a flat `entries: 512`, hiding a selectable 8-way loop size, a bounded-region offset, and a phase-offset field. `CONFIRMED`

**Location:** the DDS/Goertzel architecture YAML behind P2KB key `p2kbArchDdsGoertzel` —
`lut_setup.entries: 512` and `s_operand.field_11_0: "loop size + LUT window"`.

**What is wrong.** `entries: 512` reads as a hardware requirement; it is only the `%000` case.
`field_11_0` names the field but carries none of its content, so nothing downstream can use it.
The KB is *not false* here in the way the manual is (the manual says "**must** contain 512
entries"), but it is thin in exactly the place the manual went wrong, and it is what a
downstream author would consult.

**Evidence — Silicon Doc `sources/silicon-doc/p2-documentation.txt:4062-4092`, verbatim table:**

| `S[11:0]` | Loop Size | NCO Bits | LUT Range |
|---|---|---|---|
| `%000_TTTTTTTTT` | 512 | 30..22 | `%000000000..%111111111` |
| `%001_ATTTTTTTT` | 256 | 30..23 | `%A00000000..%A11111111` |
| `%010_AATTTTTTT` | 128 | 30..24 | `%AA0000000..%AA1111111` |
| `%011_AAATTTTTT` | 64 | 30..25 | `%AAA000000..%AAA111111` |
| `%100_AAAATTTTT` | 32 | 30..26 | `%AAAA00000..%AAAA11111` |
| `%101_AAAAATTTT` | 16 | 30..27 | `%AAAAA0000..%AAAAA1111` |
| `%110_AAAAAATTT` | 8 | 30..28 | `%AAAAAA000..%AAAAAA111` |
| `%111_AAAAAAATT` | 4 | 30..29 | `%AAAAAAA00..%AAAAAAA11` |

and (`:4093-4095`, verbatim): *"On each clock, the lookup RAM is read at the 9-bit location
bound by the %A bits, with the lower bits being the sum of the %T bits and the topmost NCO
bits. This allows you to set bounded areas within the LUT and to shift or modulate the phase of
playback."*

**Proposed correction.** Replace `lut_setup.entries: 512` with a `lut_window:` block carrying
the eight loop sizes and their NCO index bits; expand `s_operand.field_11_0` into the three
sub-fields — loop-size selector `S[11:9]`, `%A` region-bound bits, `%T` phase-offset bits — and
state the two capabilities the Silicon Doc names explicitly: **bounded LUT sub-regions** (more
than one waveform resident at once) and **phase offset / modulation**. Keep `entries: 512` only
as the `%000` default, labelled as such.

**Why it matters beyond the correction.** The guide's §17.2 headline applications are
"Function generator, audio synthesis, **RF modulation**" — and the field that does modulation is
the one neither the KB nor the manual documents.

**Additional YAML sites found by the 2026-08-20 class-wide sweep — these are part of F-302, not
separate findings.** The correction above named `lut_setup.entries` and `s_operand.field_11_0`
only; the sweep found the same assumption stated four more times in the same file:

| `architecture/streamer/dds-goertzel.yaml` | What is wrong |
|---|---|
| `:57` | `operation.steps` step 1 — `"Read LUT entry at NCO[30:22]"` as an **unconditioned general rule**. This is the KB twin of the manual's §10.2 defect and was **missing from this finding's original correction text.** |
| `:89` | `' Build 512-entry sine/cosine table` (code example) |
| `:100` | `repeat i from 0 to 511` in the `sinc2_amplitude` example |
| `:227` | `usage_pattern.data` comment restating `512-entry LUT window` as fact |

Sibling files verified **correct** and usable as the fix template: `dds-goertzel.yaml:11,:18`
(`%1111_0ppp_p111` / `%1111_1ppp_p111`, with the correct `D[22:19]` multiple-of-four caveat).

**Downstream (manual head, not a YAML edit):** *Streamer Guide* §10.2 `:648`
(`LUT[NCO[30:22]]` stated as the general rule), §10.3 `:674` ("must contain 512 entries" —
**false**), §17.2 tip `:1458` ("the 512 entries"), the `:1424` code comment ("512-entry LUT
window"), and the `\DiagDdsGoertzel` diagram in
`workspace/p2-streamer-programming-guide/templates/p2kb-streamer-diagrams.sty` (which renders
`entry = LUT[NCO[30:22]]`) — plus its **cloned copies** at
`workspace/p2-layout-torture-test/templates/p2kb-torture-diagrams.sty:207` and the staged
`pdf-forge/interactive-testing/templates/p2kb-torture-diagrams.sty:207`. Tracked in
`engineering/planning/STREAMER-GUIDE-CORRECTNESS-SPRINT-PLAN.md`; fix ships with that release.

---

## Class-wide sweep of the Streamer findings — the same errors live in OTHER artifacts (2026-08-20) — F-303…F-305

**Origin.** The Streamer Guide's 2026-08-19 class audit produced four confirmed factual errors.
Sweeping them across every manual, app note, `deliverables/ai/P2/`, and workspace diagram template
found them **outside** that manual as well. Recorded here — **not** scoped into the Streamer
sprint, which is deliberately confined to its own document. **Stephen decides at that sprint's
release gate whether the affected artifacts co-release.** Full sweep detail + the verified-correct
list: `engineering/planning/STREAMER-GUIDE-CORRECTNESS-SPRINT-PLAN.md` §13.

> **Before fixing any of these, read the "verified correct" list in that plan section.** The sweep
> deliberately separated look-alikes: the Assembly Manual's Appendix G **ADC Sampling Modes** and
> **DDS/Goertzel** *constant-value* tables were decoded row by row and are **correct** — they are
> named-symbol value tables, not field-encoding templates. Do not "fix" them.

### F-303 — the RGBI8 `2:2:2:2` fabrication is in a second released manual and in two live KB files. `CONFIRMED`

The truth (Silicon Doc `p2-documentation.txt:3800`): RGBI8 is a **3-bit colour select + 5-bit
luminance** format, structurally the same as LUMA8. It has no per-channel R/G/B fields.

| Location | Status |
|---|---|
| `manuals/p2-assembly-language-manual/opus-master/part-iii/appendix-g-streamer-constants.md:115` — *"Read byte as RGBI 2:2:2:2 (16 colors + intensity)"* | **RELEASED** — Assembly Language Reference v3.1.6, 2026-08-18, 502pp |
| `deliverables/ai/P2/language/spin2/symbols/streamer-symbols.yaml:186` — `"RFBYTE → RGBI 2:2:2:2"` | **LIVE KB** (served by `p2kb-mcp`); the one wrong row in an otherwise-correct table |
| `deliverables/ai/P2/architecture/streamer/modes-reference.yaml:221` — same description, second copy | **LIVE KB** |
| `workspace/p2-layout-torture-test/templates/p2kb-torture-diagrams.sty:176` — `\DiagRgbFormats` cloned, draws `R 2 \| G 2 \| B 2 \| I 2` | not released, but **invoked** at `P2-Layout-Torture-Test.md:836`, so it renders into every build |

**Fix template already exists, in a released manual:** *P2 Debug Window Manual* v1.1.3
`ch04-bitmap.md:100` — *"Upper 3 bits select a color, lower 5 bits are intensity"* — and it
contrasts RGBI8 against LUMA8 immediately above. Copy that framing.

### F-304 — `modes-reference.yaml` hardcodes the streamer `D[19:16]` field, and elsewhere invents a free bit that does not exist. `CONFIRMED`

The KB twin of the Streamer Guide's Appendix A defect. Authority: Silicon Doc `:2995-3020` and
`:3125-3145` both print the field sequence
`pppa · pp0a · pp1a · p00a · p01a · p10a · 0110 · 0111 · 1110 · 1111 · 0000 · 0001`;
`%a` is `D[16]` (`:3653-3654`); DDS/Goertzel is `1111 dddd 0ppp p111` (`:3484`).

| `deliverables/ai/P2/architecture/streamer/modes-reference.yaml` | Defect |
|---|---|
| `:88`, `:93`, `:98` | IMM 4-pin rows give `d_19_16` as fixed `%0000`/`%0010`/`%0100`; truth is `p00a`/`p01a`/`p10a` |
| `:330` | `X_DDS_GOERTZEL_SINC1` `d_19_16: "%0111"`; truth is `p111` — `D[19]` is the low bit of the `D[22:19]` four-pin-block selector |
| `:186`, `:191`, `:196`, `:273`, `:278`, `:283` | **The mirror-image defect** — `"%p000 + 6"` etc. imply a free `D[19]` bit for the 8-pin RFBYTE/WFBYTE variants, where truth is **fully fixed** (`0110`/`0111`/`1110`) |

**Fix template in the same directory:** `dds-goertzel.yaml:11,:18` carry the correct encodings
plus the correct `D[22:19]` multiple-of-four caveat.

### F-305 — the Assembly Manual teaches a streamer DAC example without the pin-setup step. `CONFIRMED`

`manuals/p2-assembly-language-manual/opus-master/part-iii/appendix-g-streamer-constants.md:237`
shows `mov mode, ##X_RFBYTE_1P_1DAC1 | X_DACS_3_2_1_0` with no `WRPIN` DAC-mode configuration and
no `DIRH` — the same omission the Streamer sprint fixes book-wide. **RELEASED** in Assembly
Language Reference v3.1.6.

Per **F-272** (resolved 2026-08-20) the correct setup is now fully citable: `%TT = %01`
(`P_CHANNEL`) with the COGID in `M[3:0]`, `DIRH` the pin, channel selected by the pin's two low
bits. `deliverables/ai/P2/architecture/streamer/dds-goertzel.yaml:203` carries a worked example,
and `wrpin.yaml:54` documents the field.

**Note the asymmetry that makes this easy to get wrong** — and note the half of it that was itself
wrong until 2026-08-20. The **`WRPIN`** part applies to **DAC** output only: ordinary digital pin
output via `X_PINS_ON` (`D[23]=1`) needs no DAC mode, no COGID and no channel, so do not add *mode*
setup to digital-output examples. But it **does** need `DIRH` like any driven pin — `X_PINS_ON`
enables the streamer's contribution to the pin's output *state*, never its output *enable*. See
**F-308** / **EF-062** (bench-proven: DIR low 4-of-8, `DIRH` 8-of-8). The citation this note used to
carry, `Silicon Doc :3602-3603`, resolves to nothing in `engineering/ingestion/` and has been dropped.

### F-306 — `dds-goertzel.yaml`'s "Typical usage" configures a DAC output pin that nothing ever drives, and the Streamer sprint plan certified it as the fix template. `CONFIRMED`

**How it surfaced.** Authoring the Streamer Guide's new §11.0 (task «#269», 2026-08-20). The sprint
plan's §13 "Verified correct — do not fix these" list states that
`deliverables/ai/P2/architecture/streamer/dds-goertzel.yaml:203` *"carries a complete worked DAC-pin
setup"* and offers it as the answer §1 was missing. Read end to end, it does not.

**Location:** `deliverables/ai/P2/architecture/streamer/dds-goertzel.yaml`, `usage_pattern.code`
step 3 (`:203-204`) read against `usage_pattern.data` (`:225-228`).

**What is wrong.** Step 3 configures the pin and enables it —

```
' 3. Configure DAC output pin (this one DOES get DIR)
wrpin   ##P_DAC_124R_3V, #dac_pin
dirh    #dac_pin
```

— and **nothing in the example ever puts a value on that pin.** Two independent paths could, and
the example takes neither:

- **The streamer path is switched off.** The example's own `dds_cmd` is
  `%1111_0000_0000_0111<<16 + sinc2<<23 + cycles`, whose `%dddd` DAC-routing nibble at `D[27:24]`
  is **`%0000` = `X_DACS_OFF`**. No streamer DAC channel is routed anywhere.
- **The level path is never written.** `P_DAC_124R_3V` is defined in Spin2 v55
  (`sources/spin2-v55/spin2-v55-text.txt:1478`) as
  `%0000_0000_000_1011000000000_00_00000_0` — `M[12:10] = %101` (DAC_MODE), **`TT = %00`**, and
  `M[7:0] = 0`. Per Silicon Doc `:7645-7646`, `TT = %00` in DAC_MODE means *"M[7:0] sets DAC level"*
  — so the pin is level-driven at level **zero**, permanently, unless the level is rewritten.
  The Silicon Doc's own worked program does rewrite it (`setbyte dacmode,x,#1` / `wrpin
  dacmode,#dacpin`, `:4225-4305`); **the KB example dropped that step while keeping the setup.**

So an agent following this recipe gets a configured, enabled, silent pin, and no diagnostic. The
file's `applications:` block advertises `function_generator: "Load waveform to LUT, set output
frequency"` — the DDS-output half — which this code never enables.

**Evidence that the streamer-fed arrangement is the different one.** `TT = %01` selects a **cog DAC
channel** as the pin's source, which is the path the streamer overrides (Silicon Doc `:3521-3523`,
`:7647`, `:2705-2711`; see **F-272**, status `RESOLVED`, `:521`). This is measured, not reasoned:
**EF-054** swept `%TT` on a jumpered cog-DAC pin and read `%00` = 1,408 (no drive) versus **`%01` =
6,737**; **EF-055** drove a `P_DAC_124R_3V` pin from its level field and watched the spread collapse
from 1,305/2,000 samples to 25 when `P_CHANNEL` was added. Both are `[M-pre — streamer-free]`, so
they isolate the pin arrangement from the streamer entirely.

**Proposed correction.** Decide which arrangement the example is teaching and complete that one:

- If it stays a **Goertzel detector** (its `dds_cmd` says it is), **delete step 3** — the DAC pin is
  not part of a detector — or keep it and add the level-write the Silicon Doc program uses.
- If it is meant to show **DDS output**, route the DACs in `dds_cmd` and configure the pin as the
  streamer-fed arrangement requires: `P_DAC_124R_3V | P_CHANNEL`, the COGID in `M[3:0]`, `DIRH`,
  channel selected by the pin's two low bits.

**Blast radius — the plan claim must be corrected too, not just the YAML.** The Streamer sprint
plan's §13 lists this site under "Verified correct — **do not 'fix' these**", and that instruction
is carried into task «#288»'s co-release gate. Left standing, it tells the next reader the opposite
of this finding. Corrected in the plan in the same pass that filed this entry.

**Status:** `CONFIRMED — KB fix belongs to the yaml head (yaml-knowledge-base-maintenance), NOT to
the Streamer manual sprint. Surfaces with F-302…F-305 at that sprint's co-release gate.`

---

### F-307 — six PASM2 instruction YAMLs serve their description with literal backslashes in it: `\"CMOD\"` instead of `"CMOD"`. `CONFIRMED`

**How it surfaced.** Reading the five colorspace-converter instruction YAMLs as background for the
Streamer Guide's new Chapter 15 section (task «#274», 2026-08-20). The corruption is in the served
value, not just the file bytes.

**Location:** `deliverables/ai/P2/language/pasm2/` — `setcy.yaml`, `setci.yaml`, `setcq.yaml`,
`setcfrq.yaml`, `setcmod.yaml` (both `description:` and `oneliner:`), and `wxpin.yaml` (same two
keys). Eleven string values across six files. The generated
`deliverables/ai/P2/language/PASM2-ENCODING-REFERENCE.md` carries the same text at `:132-136` and
in the WXPIN row, so it is a **derived** occurrence that clears when the YAMLs are fixed and the
artifact is regenerated.

**What is wrong.** Each value is a **single-quoted** YAML scalar containing `\"`:

```yaml
description: 'Set the colorspace converter \"CMOD\" parameter to D[8:0].'
oneliner: Set the colorspace converter \"CMOD\" parameter to D[8:0]
```

In a single-quoted YAML scalar a backslash is a literal character, so this does **not** parse to
`"CMOD"` — it parses to `\"CMOD\"`, backslashes and all. Confirmed by parsing, not by grep:
`yaml.safe_load` over the whole `deliverables/ai/P2/` tree returns the backslashes in the value.
A consuming agent gets `Set the colorspace converter \"CMOD\" parameter to D[8:0]`.

**Authority.** All three documentary sources write plain double quotes:

- `sources/pasm2-manual/pasm2-manual-narrative.txt:8866-8874` — `Set the colorspace converter "CFRQ" parameter to D[31:0].`
- `sources/p2-datasheet/pasm2-complete-instruction-tables.md:489-493` — same, and `:222` for `Set "X" of smart pins …`
- `sources/silicon-doc/part2-video-output.txt:188-192` writes it with **no quotes at all**

The YAML's own `documentation_source:` names the PASM2 Manual, which is the first of these. The
escaping is a transcription artifact of the extraction pipeline, not anything a source states.

**Proposed correction.** Drop the backslashes — write `"CMOD"` in each of the eleven values. The
single-quoted form needs no other change: a single-quoted YAML scalar holds a bare `"` fine, and it
is only the backslash that has no meaning there. The bare `oneliner:` values are plain scalars and
likewise just lose the backslashes. Then regenerate `PASM2-ENCODING-REFERENCE.md`. **Scope is
exactly these six files** — see below.

**Deliberately NOT in scope — three look-alikes that are correct.** A grep for `\"` across the tree
returns 37 files; all but these six are legitimate:

- **`hardware/*.yaml`** (`"0.1\" spacing"`, etc.) — `\"` inside a **double-quoted** scalar is the
  correct escape and parses to `0.1" spacing`.
- **`language/pasm2/jmp.yaml`** — `"\" forces R = 0.` is *about* the backslash prefix that forces
  R = 0 in `JMP #\address`. The character is the subject; the text is right.
- **`language/spin2/constructs/escape-strings.yaml` and `concepts/string_constants.yaml`** — the
  Spin2 escape-string prefix genuinely **is** `@\"`. Spin2 v55 release notes,
  `sources/spin2-v55/spin2-v55-text.txt:50`: *"New `@\"string\n"` works like `@"string"`, but
  allows escape-character sequences."* Backslash-quote opens it and a plain quote closes it. These
  files are correct and a sweep that "normalizes" them would break real syntax.

**Status:** `CONFIRMED — belongs to the yaml head (yaml-knowledge-base-maintenance). Not a Streamer
manual defect; the manual does not quote these descriptions.`

---

### F-308 — "digital pin output through `X_PINS_ON` requires no `DIRH`" is wrong: the streamer feeds the pin's output STATE, and DIR is still the output ENABLE. `CONFIRMED`

**How it surfaced.** Two bench runs of the VO-J-003 rig (2026-08-20, logs in that rig's `logs/`).
Its digital self-test drove `DAC_PIN` through `X_PINS_ON` with DIR left low — on the strength of the
claim below — and scored **4 of 8** then **3 of 8** toggles, i.e. the pin was never driven and the
readback was float noise. Going to the primary source to explain it produced this finding.

**Locations (both live):**
- `engineering/document-production/manuals/p2-streamer-programming-guide/opus-master/streamer-body.md:834`
  — a `::: hardware` callout in §11.0: *"Ordinary pin output through `X_PINS_ON` drives the pin bus
  directly and requires no `WRPIN` and no `DIRH`."* **RELEASED in Streamer Guide v1.0.9**; v1.1.0 is
  in its correctness sprint now.
- `engineering/operations/P2KB-CORRECTION-FINDINGS.md:251` — F-305's closing note repeats the claim
  as guidance ("Do not add pin setup to digital-output examples") and cites `Silicon Doc :3602-3603`.
  **That citation does not resolve** to any extraction in `engineering/ingestion/`.

**What the primary source actually says.** *Parallax Propeller 2 Documentation v35 (Rev B/C
Silicon)*, text extracted from the shipped `.docx`:
- STREAMER section: *"Modes which can output to pins OR the streamer pin-output bus **with {OUTB,
  OUTA}** to produce the final 64 pin **output states** on each clock for the cog. For these modes,
  %e in D[23] must be '1' to enable pin output."*
- SMART PINS section: *"Normally, an I/O pin's **output enable is controlled by its DIR bit** and its
  **output state is controlled by its OUT bit**, while the IN bit returns the pin's read state."*

The streamer's pin data is OR'd into the **output state** — the OUT side. Nothing in the document
gives the streamer any authority over the output **enable**. The one documented way to drive a pin
with DIR low is the smart-pin `%TT` field (*"the %TT bits … will govern the pin's output enable,
regardless of the DIR state"*), and `X_PINS_ON` digital output uses no smart pin. So `DIRH` **is**
required, and D[23] enables the streamer's contribution to OUT, not the pin's driver.

**The "no `WRPIN`" half is correct** and should survive the fix — no smart-pin mode is needed. Only
the "no `DIRH`" half is wrong. Note the internal tension the claim already had:
`streamer-body.md:796`, twenty-eight lines earlier in the same section, states the general rule
correctly — *"**`DIRH`** on the pin. Until DIR is high, the pin does not drive."*

**Proposed correction.** Rewrite the §11.0 callout so it separates the two: digital output needs no
`WRPIN` (no DAC mode, no COGID, no channel), but it does need `DIRH` like any driven pin. Fix
F-305's note in the same pass and drop or replace its unresolvable citation.

**SEALED ON SILICON 2026-08-20 → EF-062.** VO-J-003's run 3 ran the A/B: the same streamer command
with DIR low and then `DIRH`, the `DIRH` leg starting from `OUT`=0 so a pass proves the streamer
overrode `OUT`. *Result:* `D1` plain drive (no streamer) **8 of 8** · `D2` DIR low **4 of 8** · `D3`
`DIRH` **8 of 8**. The prediction and its falsifying outcome ("if `D2` passes, reverse F-308") were
written into the program before the run; the bench was free to reverse this and did not.

**The class — the book is inconsistent with itself, and the majority of it is already right.**

*Correct, do not touch:* `streamer-body.md:796` ("Until DIR is high, the pin does not drive") ·
`:1490` the §15.2 HDMI program, which does `drvl #7<<6 + HDMI_BASE` · `:2038` the troubleshooting
checklist, "Pins configured as outputs (DRVH/DRVL as needed)" · `:623`, `:816`, `:1767` (ADC, DAC,
DDS pin enables).

*Wrong prose — **FIXED 2026-08-20**:* `:834` the §11.0 callout (rewritten: keeps "no `WRPIN`",
adds what `DIRH` is for and what a DIR-low streamer command looks like on a bench) · `:410` §5.2's
"the pin columns need none".

*Code blocks that omitted the pin enable — **ALL FIXED 2026-08-20** («#289»):*
- `:405` `X_IMM_32X1_LUT` (32-pin) -> `drvl ##31<<6` · `:435` `X_IMM_4X8_1DAC8` (8-pin) ->
  `drvl #7<<6 + pin` · `:470` `X_RFLONG_4X8_LUT` (32-pin) -> `drvl ##31<<6 + base` ·
  `:497` `X_RFBYTE_8P_1DAC8` (8-pin) -> `drvl #7<<6 + base`. Span forms compiled before use.
- §16.1 SPI — the configuration block set up `spi_clk` and never touched `spi_do`, the pin the
  streamer drives. Fixed earlier the same day.
- **§15.1 VGA — rebuilt.** It carried **four** defects, not the one this finding named, and they
  were fixed in a single edit rather than four passes: (1) no §11.0 DAC-pin setup at all for the RGB
  channels; (2) `VGA_BASE` undefined; (3) `framebuffer` undefined; (4) **a 640×480 framebuffer at
  16 bpp is 600 KB and hub RAM holds 512 KB** — the program could not have existed as written. It
  now declares `VGA_BASE = 16` (a multiple of 4, so each pin's low two bits pick its own DAC
  channel), does the §11.0 setup (`COGID` into `M[3:0]`, `P_CHANNEL`, `DIRH`) across a 4-pin span,
  and paints 350 lines into a declared `orgh` framebuffer while blanking the rest of an unchanged
  525-line field — the same trade §15.2's HDMI program already makes for the same reason (§7.1).
  **Extracted from the manuscript and compiled: 452,096 bytes**, matching §15.2's block exactly.
  The compiler caught a collision the new `CON` introduced — P2 symbols are case-insensitive, so a
  `VSYNC_PIN` constant clashed with the `vsync_pin` register; the constant was dropped.

*Not touched, and correctly so:* the §7.3 RGB pattern block already carries a `**Pattern**` label
and points at §11.0 for its DAC pins.

**Why the sweep was routed rather than done at filing time.** It was folded into «#289» and run
alongside «#280», the pass that reads every code block, so that one hand added the missing line to
every block under one contract. Routing inside a sprint, not deferral across a release — none of it
ships until v1.1.0. The failure mode being avoided is the one «#282» records: "the finding named a
row, the fix corrected a row, nobody swept the table." Worth noting that the sweep *earned its keep* —
it found §15.1 carrying four defects where this finding had named one, and a fifth `pin<<17` site
(`:435`) that the original enumeration missed.

**Sprint impact.** This is sprint decision #4 ("Digital ≠ DAC. `X_PINS_ON` needs NO wrpin/dirh"),
which later tasks were told to respect. **That decision is now half wrong and must not be applied as
written.** Surfaces at the Streamer v1.1.0 co-release gate («#288») with F-302…F-307.

**Status:** `PARTIAL — the Streamer Guide is DONE: prose at :410 and :834, and every code block
above, fixed 2026-08-20 with four gates green and §15.1 compiled from the manuscript. Confirmed on
silicon (EF-062). Open on two counts: the v1.1.0 PDF is not verified yet («#287»), and the Assembly
Language Reference's three sites are owed at the agreed CO-RELEASE.`

---

### F-309 — the `pin<<17` caution in §12.0 stops short of the 8-pin-and-wider modes, which is the case that actually fires. `PARTIAL`

> **This finding was FILED WRONG on 2026-08-20 and is rewritten here in place.** As first written it
> claimed the multi-pin example lines were defective for naming their operand `pin` rather than
> `base`, and that the manual carried no caution. **Both claims were false, and a single read of
> §12.0 would have shown it.** The finding was filed off a grep of example lines. What follows is
> what is actually owed, which is much narrower.

**What the manual already gets right — do NOT "fix" any of it.**
- §12.0 *explains and justifies* the naming: `pin<<17` puts `pin>>3` into the group field `D[22:20]`
  and `pin&7` into the sub-pin field `D[19:17]`, *"which is exactly the decomposition the two fields
  expect. That is why the idiom appears throughout this book with a plain pin number."* Renaming
  `pin` to `base` would contradict a deliberate, documented convention.
- §12.0 already carries a `::: caution` — *"The shift is arithmetic, not a pin-field operator"* —
  covering the fewer-than-8-pin modes and DDS/Goertzel.
- §12.1 (group field, 8-pin windows, wrap-around) and §12.2 (sub-pin split per pin count) are
  correct and are now **empirically confirmed** by **EF-064**.

**The actual gap.** That caution enumerated *"the fewer-than-8-pin modes"* and DDS/Goertzel. At
**eight pins and wider** `D[19:17]` holds **no** pin bits at all — every one of them is mode or
DAC-configuration — so the operand must be a multiple of 8. That case was not named, and it is the
one the bench fired: `X_IMM_4X8_1DAC8` with `pin = 20` assembled to `$60B6_FFFF` instead of
`$60AE_FFFF` and drove **P24..P31**, a different mode (`X_IMM_4X8_4DAC2`) at a different window.
The `+` composition carried the stray low bits out of `D[19:16]` and into the group field. Proven as
**EF-065**.

**Fix applied 2026-08-20** — one paragraph added to the existing §12.0 caution, stating the
8-pin-and-wider rule, what an unaligned value actually does (changes the mode, and carries into the
group), and the general preference for `|` over `+` when composing a mode word. Four gates green.
No example line was renamed.

**Sibling, already in the book:** §9.2 / **EF-059** is the same failure in another mode family
(`adc_pin<<17` changing the mode of `X_1ADC8_0P_1DAC8_WFBYTE`), and §12.0's first rule already points
at it. The `|` form fails differently and worse — it sets a bit the mode template already sets, so
the word is byte-identical to the aligned base and the stray value *vanishes* rather than carrying.

**Status:** `PARTIAL — §12.0 caution extended 2026-08-20, four gates green, grounded in EF-064 +
EF-065. Per this register's own rule — a fix applied but not yet validated is NOT done — it stays
open until the v1.1.0 PDF is verified at «#287». The naming claim in the original filing was wrong
and is retracted above.`

---

## Manual-side residue of an already-fixed YAML correction (2026-08-20) — F-310

### F-310 — the Streamer Guide sources the SINC2 constant-iteration constraint to a document that does not contain it. `DONE (2026-08-20)`

**Origin:** found while correcting the Streamer Guide's fan-out audit record at «#282». The audit
record claimed all 8 survivors had been applied; seven had. This is the eighth.

**The claim, as RELEASED in v1.0.9** (`streamer-body.md`, the §10.5 SINC2 caution):
*"a documented silicon limitation"* … *"(The constant-iteration constraint is recorded in the*
Parallax Propeller 2 Documentation *Goertzel note dated 2024.12.16.)"*

**Why it is wrong.** The **constraint itself is real and stands** — do not remove it. What is wrong
is where the manual sends the reader to check it. It is **not** in the released *Parallax Propeller 2
Documentation*. The 2026-07-10 fan-out audit flagged exactly this and marked it `unverifiable`; the
v35 text carries only the amplitude caveat (reduce the sine/cosine table from ±127 to ±10), and the
power-of-2 rule that IS in v35 belongs to the **smart-pin SINC2 sampling mode**, a different
mechanism. The real source is Chip Gracey, the P2's designer, reporting it on 2024-12-16 — ingested
at `engineering/ingestion/external-inputs/forum-threads/ProblemGoertzelSINC2mode/`.

**This was already decided once, on the YAML side, and the manual was not swept.** **F-190**
(`DONE 2026-07-02`, now in the 2026-08-15 archive) put the constraint into
`language/pasm2/getxacc.yaml` as `sinc2_constraint` and deliberately attributed it to *"Chip Gracey
(P2 designer), 2024-12-16; not yet in the released Silicon Doc"* — Stephen confirmed at the time that
the released document lacks the note. Six weeks later the manual still carried the attribution that
decision had already rejected. **The finding named the YAML, the fix corrected the YAML, nobody swept
the manual** — the same shape as the Appendix A row that was fixed while fifteen siblings were not.

**Class-wide sweep: done, and the class is small.** Exactly **one** live site, `opus-master/
streamer-body.md`. No other manual and no app note carries the claim. Deliberately NOT touched: the
workspace render and the outbound `.tex` (regenerated from the master), the fan-out audit file (a
historical record of what was found), and the v1.0.3 CHANGELOG entry — which is **correct as
written**, calling these *"Designer-authoritative guidance additions"* rather than
documentation-sourced.

**Fix applied 2026-08-20.** Headline now reads *"a silicon limitation reported by the P2's
designer"*; the closing parenthetical now reads *"Chip Gracey, the P2's designer, reported this
constraint on 2024-12-16. It has not reached the released* Parallax Propeller 2 Documentation*, so do
not expect to find it there."* Telling the reader why the citation will not be found there is the
part that makes the correction useful rather than merely accurate. Four prose gates green.

**Status:** `DONE (2026-08-20) — single site corrected, class swept and empty, source verified live
against the ingestion tree rather than against this register. Ships in Streamer Guide v1.1.0.`

---

## Golden-source defect — duplicate EF id (2026-08-15) — F-267

## ⛔ REVERSAL — a shipped KB correction went the wrong way (2026-08-16) — F-269

## YAML→Manual impact survey — KB v1.16.3 (2026-08-16, `release-yamls` §8)

Delta: `spin2/methods/wrpin.yaml` · `architecture/smart_pins.yaml` ·
`architecture/smart-pins/smart-pin-11011-usb-host-device.yaml` · `architecture/cordic.yaml` ·
`architecture/streamer/overview.yaml` · `architecture/streamer/dds-goertzel.yaml` ·
`pasm2/getxacc.yaml` · `spin2/integration/spin2-pasm2-integration.yaml` ·
`spin2/special-symbols/at.yaml`.

Intersected against every live manual's `MANUAL-DESCRIPTOR.md` declared sources. **Survey done, not
skipped.** Most intersections are already owned by an in-flight Sprint 2 task, so no duplicate flag
is raised for them; the ones that are **not** covered are flagged below.

| Element | Intersects on | Disposition |
|---|---|---|
| Streamer Guide | streamer, dds-goertzel, getxacc, DEBUG_COGS | **covered** — «#220» «#221» |
| IOSP | `architecture/smart-pins/`, smart_pins | **covered** — «#219» (and the F-264 %TT material rides its v1.0.9 pass) |
| Assembly Reference | cordic, streamer | **covered** — «#228» |
| P2AN002 | cordic | **covered** — «#236» |
| XBYTE Guide | streamer | **covered** — «#227» (§15.3 restructure); see the F-268 flag below |
| **P2AN001 / P2AN003** | wrpin | **⚑ FLAG — re-audit against v1.16.3.** These two were read site-by-site and taken OUT of the release wave, but that read answered **F-259's** question (does every executable example carry `\| P_OE`?). **F-264 is a different fact** — that `%TT` is context-dependent and that adding `P_OE`/`P_CHANNEL` to a **non-smart-pin cog DAC** kills it. Any cog-DAC or `P_DAC_*` configuration in these app notes was never checked against that. Do not treat the wave exclusion as covering it. |
| **P2AN004** | wrpin | **⚑ FLAG — same class as above**, and it was never in the wave at all. |
| **Architect's Guide** | CORDIC, streamer | **⚑ FLAG — re-audit against v1.16.3.** Not in the release wave. Declares both sources; the CORDIC hub-in-loop rule (F-263) and the `DEBUG_COGS` streamer caveat (F-266) are new since its last pass. |
| **DeSilva Tutorial** | CORDIC | **⚑ FLAG — re-audit against v1.16.3.** It *is* in the wave, but for §1/§2 (Acknowledgments, Appendix A) only — its CORDIC material is untouched by «#222»/«#223» and unexamined against F-263. |
| All elements showing PASM fragments | `spin2-pasm2-integration.yaml` | **⚑ FLAG — F-268 class sweep**, filed below and deliberately not folded into a correction task. |

These flags are the drift signal `document-audit` drains on each element's next pass. They are
**not** Sprint 2 scope and must not be pulled into it silently — surface them to Stephen as a scope
decision.

---

## Spin2/PASM2 boundary defect promoted from the empirical ledger (2026-08-16) — F-268

### F-268 — inside a Spin2 object, `##hubsymbol` in a `DAT` block resolves against `$400`, not the object's load address. `PARTIAL — KB DONE 2026-08-16; guide-side sweep owed`

**Origin:** EF-060, which had no F-number and no KB entry. Surfaced while getting the F-256/EF-058
rig working, so it is a by-product rather than a target — and it is the broadest-reach item the
2026-08 campaign produced.

**The fact.** A PASM fragment that is correct in a **standalone** PASM file reads **interpreter
memory** when pasted into a Spin2 object's `DAT` block: `##hubsym` resolves against `$400` rather
than the object's load address. Measured on real P2 silicon: `@disp` = `$1AF9` from Spin2 versus
`##disp` = `$0651` from PASM in the same object — **5,288 bytes apart**, and the `##` form returned
garbage.

**Why it matters more than its size suggests.** It bites anyone who copies a PASM fragment out of a
guide or reference into a Spin2 object — which is how most P2 code is written. It assembles, it
runs, and it reads the wrong memory. **Workaround:** pass hub addresses in from Spin2 with `@`, or
address through PTRA/PTRB.

> **KB APPLIED 2026-08-16 («#218»).**
> `language/spin2/integration/spin2-pasm2-integration.yaml` →
> `integration_rules.hub_address_resolution`: the rule, where it is instead correct (standalone
> PASM), why it bites, the workaround, and the measurement. Findability: a matching one-line pointer
> added to `language/spin2/special-symbols/at.yaml` `notes:`, since `@`'s
> object-relative-vs-absolute entry is exactly where a reader chasing this lands — that file already
> documented the Spin2 side of the same boundary and had no route to the PASM side.
> Source trace: EF-060.

**Still owed (manual head, NOT tasked in Sprint 2):** our guides present standalone-PASM fragments
without saying so. A class-wide sweep of `##hubsym`-style fragments across the live manual set is
the durable fix; scope it as its own item rather than folding it into a correction task.

---

## A shipped YAML companion contradicts its own released app note (2026-08-16) — F-270

## The whole app-note companion set is version-frozen (2026-08-16) — F-271

### F-271 — every `application-notes/*.yaml` companion still carries its maiden `version:` while the note it ships with has moved on, so an agent cannot tell which edition it holds. `CONFIRMED — scope decision owed, deliberately NOT swept`

**Surfaced by:** the F-270 content probe against the published MCP. The corrected SINC2 line came
back live and correct — sitting four lines under `version: "1.0.0"`, in a companion to a note that
is at **1.0.3** and going to 1.0.4.

**The defect, across all seven:**

| Companion | `version:` | Note's released version (roster) |
|---|---|---|
| p2an001-single-pin-instrumentation-adc | `1.0.0` | **1.0.3** (→1.0.4 in the wave) |
| p2an002-cordic-for-real-work | `1.0.0` | **1.0.2** |
| p2an003-dac-analog-signal-generation | `1.0.0` | **1.0.2** |
| p2an004-frequency-rotation-rc-timing-measurement | `1.0.0` | **1.0.2** |
| p2an005-cooperative-multitasking-tasks | `0.1.0` | **1.0.2** |
| p2an006-sizing-cog-task-stacks | `0.1.0` | **1.0.1** |
| p2an007-data-structures-new-facilities | `1.0.0` | **1.0.1** |

**Seven for seven — so this is the convention failing, not a missed file.** The stamp has never been
advanced by any release.

**Why it matters — and the severity claim this entry first carried was WRONG, corrected 2026-08-16
on Stephen's challenge ("why are there version numbers in the yaml?").**

The original text said a frozen stamp is *"worse than absent, because an agent that caches by version
sees no change and keeps serving the stale body."* **Nothing caches by version.** Checked, not
assumed: the published index carries exactly `path`, `mtime`, `sha256` per entry — change detection
is the git commit timestamp plus a content hash, both of which updated correctly when F-270 shipped.
A consumer mechanism was asserted without being verified, which is this sprint's own named failure
mode. **The field is inert.**

**What is left is real but smaller:** the stamp misleads anyone who *reads* it — a human opening the
file, or an agent quoting `version` when citing the companion. P2AN001's was edited twice this sprint
(F-269, F-270) and still reads `1.0.0`. It is a truthfulness defect in shipped metadata, not a
cache-correctness defect. **Priority drops accordingly** — this is not urgent, and it is certainly
not worth a bulk edit of seven published files.

**The deeper finding, which is the actual reason to keep this entry.** `version:` appears in only
**24 of 1129** published YAMLs, carrying **two unrelated meanings** under one key name, with no
schema doc defining either (`APP-NOTE-DESIGN-DECISIONS.md`, which the companion header cites as its
schema authority, does not mention `version` at all):

| Population | What `version:` means there | Tell |
|---|---|---|
| **17 files** — `architecture/smart_pins.yaml` (1.2), `architecture/streamer/_index.yaml` (2.0), `spin2/conventions/*` (1.0.0–2.0.0), `guides/*` | **the file's own content revision** | almost always paired with `last_updated:`; refers to nothing outside the file |
| **7 app-note companions** | positioned as **the note's** version — sits under `doc_id:` and above `kind: application-note`, beside the note's `title`/`subtitle` | no `last_updated:` |

**So "which meaning is right" has no documented answer, and the tree's majority reading is the
opposite of the one this entry first recommended.** That recommendation was made from the app-note
files alone, before the other seventeen were looked at.

**This is F-270's rule showing up structurally.** F-270 established that *an app-note correction is
not complete until its YAML companion carries it.* The companion here **did** carry the content — and
still shipped a false edition stamp. So the rule needs its second half: **the companion ships under
the note's version, and that stamp is advanced at release, not at edit.**

**Deliberately NOT swept.** Two things need Stephen's decision before any edit:
1. **Semantics.** Does `version:` mean *the note's version* (then all seven get stamped and it becomes
   a `release-manual` step) or *the companion's own schema/content revision* (then it needs renaming
   to say so, and a separate `note_version:` added)? The files carry no comment either way. Guessing
   here and sweeping seven published files is exactly the F-211 failure mode — a class-wide sweep
   amplifying an ungrounded reading.
2. **Whether it is a KB bump at all.** These are published `deliverables/ai/P2/` files, so any stamp
   change ships in a KB release; but the *natural* moment to advance them is each app note's own
   release. Those two cadences are not the same and the answer decides which skill owns the step.

**Ask the prior question first: what is this field FOR?** (Stephen, 2026-08-16: *"how is that version
useful to agents?"*) Worked through honestly, **a bare `version:` is of no use to an agent**:

- It is **not** how change is detected — that is `mtime` + `sha256` in the index, and they work.
- It is **not** how content is selected — an agent fetches by key and gets exactly one body. There is
  no version negotiation, no second edition to choose between, no `1.0.3` still on the shelf.
- It **cannot** be compared against anything the agent holds, because the agent has no prior copy.
- A stamp only earns its place if something can be **checked against** it. `1.0.4` next to nothing is
  a number an agent can only quote — and quoting it is precisely how a stale one does harm.

**What would actually serve an agent** is the *note's* version — not as a bare number, but as the
answer to a question an agent really has: *"the PDF in front of the user — does this digest match
it?"* That makes the useful field an explicit, self-describing link to the human artifact
(e.g. `describes_document: {doc_id: P2AN001, version: 1.0.4, released: 2026-08-16}`), which a
reader can compare against the cover of the PDF they are holding. The bare `version:` key answers no
question and, worse, reads as the *file's* version to anyone applying the tree's majority convention.

**Revised recommendation — cheaper and more honest than the original.** Do **not** stamp the seven
files with note versions and add a fourth version location to maintain. Instead:
1. **Delete the bare `version:` from the seven companions** — it is inert, ambiguous, and currently
   false. Removing a field that answers nothing beats maintaining it in seven places forever.
2. **If** the match-the-PDF question is worth answering, add the explicit `describes_document:`
   block in its place, stamped by `release-manual` alongside the roster row and cover/`request.json`
   — one self-describing field, not a number whose meaning must be inferred.
3. Leave the **17 non-app-note** files alone; there `version:` + `last_updated:` is a coherent
   file-revision convention. Worth documenting, not changing.

**Note the reversal:** this entry originally recommended stamping all seven to track the note. That
was written from the app-note files alone, before the other seventeen or the index schema were
looked at, and it would have institutionalised the ambiguity rather than removing it.
[[feedback_drop_techniques_that_lower_quality]] — when a shape keeps producing defects, remove the
shape rather than add a rule to maintain it.

**Status:** `RESOLVED — DECIDED AND PUNCH-LISTED (2026-08-16)`. **Do not re-file, do not work it now.**

**Stephen's decision supersedes both recommendations above, including the revised one.** The
principle is broader than this field: **the published KB has exactly one edition — the current one —
so nothing in the tree should cite currency or a version at all.** Every reference means *latest*.
That rules out the `describes_document:` block too; it is still a currency citation, just a
better-labelled one. **Delete the shape rather than maintain it.**

**Deferred deliberately, not forgotten** — *"we are trying to get to released documents, and we are
not there yet given our task list. We should stay away from any diversions at this point in time."*
Sprint 2's release wave comes first.

**Carried to → `engineering/tools/p2kb-mcp/PUNCH-LIST.md` PL-004**, which holds the full scope
(7 companions to strip; the other 17 `version:`/`last_updated:` bearers to review per-population,
NOT to sweep on the app-note reading; prose "as of" sweep; PDF versioning explicitly out of scope).

---

## Open question surfaced by «#221» — does a STREAMER-driven DAC need `P_CHANNEL`? (2026-08-16) — F-272

### F-272 — filed as "the `%TT` setting for a DAC pin the STREAMER writes is not stated by any source we hold." The premise was false, and the bench then confirmed the answer. `RESOLVED-INVALID`

**How it surfaced.** Streamer Guide §17.1 shipped `wrpin ##P_DAC_124R_3V + P_CHANNEL, dac_pins`
alongside `X_DACS_0N0_0N0` in the command — i.e. a **streamer-driven** differential DAC. «#220»
corrected the `+` to `|` (value-neutral). «#221» then had to decide whether `P_CHANNEL` belongs
there at all, and **could not ground it either way.**

**What the authority actually shows.** The Silicon Doc's worked Goertzel program
(`p2-documentation.txt:4225-4305`) does **not** drive its DAC from the streamer. Its command long is
`dds_d = %1111_0000_0000_0111<<16 + sinc2<<23 + cycles` — **DAC routing nibble `%0000`, i.e.
`X_DACS_OFF`** — and the DAC pin is updated by re-issuing `WRPIN` with the power byte inserted into
the mode word (`setbyte dacmode,x,#1` / `wrpin dacmode,#dacpin`). Its `dacmode` long is
`%0000_0000_000_10110_00000000_00_00000_0`: **`TT = %00`, smart pin off, DAC_MODE**, level driven
from `M[7:0]`. Per F-264 that is exactly the context where adding `P_OE`/`P_CHANNEL` **kills** the
output. So for the *level-driven* DAC the answer is settled: no `P_CHANNEL`.

**What remains open:** the guide's arrangement was a *different* one — DAC values supplied by the
**streamer** through the DAC-routing field. In that arrangement the pin must take its value from a
cog DAC channel, which is precisely what `P_CHANNEL` (`%01`) selects — so `P_CHANNEL` may well be
**required** there. No source we hold works that arrangement, and it was never on the bench.

**Resolution taken in the manual — avoid, do not guess.** §17.1 is titled *Goertzel Frequency
Detection*, so it was rewritten as a **detector**: DAC routing off (`X_DACS_OFF`), input pin only,
every line traceable to the Silicon Doc program. The generate-while-measuring case moved to a
forward reference to §17.2. **Nothing asserts a `%TT` value for a streamer-driven DAC**, which is
the honest state. [[feedback_understand_mechanism_before_documenting]] — a corrected-*looking*
recipe we have not seen work is worse than an obviously incomplete one.

**Why keep the question.** It is the same axis as **F-264**, whose impact survey already flagged
**P2AN001 / P2AN003 / P2AN004** for re-audit on cog-DAC configuration. If any of them configures a
streamer-fed DAC, this question governs it. Settle it on the bench (drive a DAC from the streamer
with `TT = %00` and with `%01`, compare) before writing the streamer-driven form into any document.

**Status:** `RESOLVED-INVALID (2026-08-20) — the premise was false: the mechanism IS stated by
sources we hold, in the three places tabled below. The bench then ran anyway and CONFIRMED the
answer — VO-J-003 → EF-063, arm T0 reading 1 ADC count at %TT = %00 against arm T1 reading 5,330
at %01. Documentary and empirical agree; nothing is owed. Note this status supersedes the earlier
"bench confirmation optional, not required" — it was optional, it happened, and it is recorded.`

### 2026-08-20 — this finding's premise is falsified. The Silicon Doc states the whole mechanism, in three separate places.

The entry above says *"the `%TT` setting for a DAC pin the STREAMER writes is not stated by any
source we hold."* That was written from the Goertzel demo alone. A targeted re-read found the
mechanism stated outright — not inferred, not assembled from reasoning, but three verbatim
statements that together answer it:

| Silicon Doc | Verbatim | Answers |
|---|---|---|
| `:7647` | *"01 = OUT enables ADC, **M[3:0] selects cog DAC channel**"* (under `for DAC_MODE:`, smart pin off) | `%TT = %01` **is** the cog-DAC-channel arrangement — i.e. `P_CHANNEL` **is required** |
| `:3523` | *"that pin must be set to DAC mode **with the COGID embedded**, via WRPIN, and **DIR must be set high**"* | what `M[3:0]` carries, and that `DIRH` is required |
| `:2705-2711` | *"Each cog outputs four 8-bit DAC channels… **DAC0 can drive the DAC's of all pins numbered %XXXX00**"* (DAC1→`%XXXX01`, DAC2→`%XXXX10`, DAC3→`%XXXX11`) | the channel is chosen by the **pin's two LSBs**, not by the mode word — which is why `M[3:0]` has room for the cog |

**So the two arrangements are different modes, and both are documented:**

- **Level-driven** (the Goertzel demo, and what the original entry analysed): `%TT = %00`,
  `M[7:0]` *is* the level. **No `P_CHANNEL`** — and per **F-264** adding it here kills the output.
- **Streamer/cog-channel-driven** (DDS, VGA, any `X_DACS_*` routing): `%TT = %01` (`P_CHANNEL`),
  `M[3:0]` = the **COGID**, `DIRH` the pin, channel selected by the pin's low two bits.

**Corroboration (upstream lead, NOT authority).** `flexprop/samples/vga/vga_tile_driver.spin2`
does exactly this: its comment reads `' put our COG id into the DAC info`, it `or`s `mycogid`
into the mode word (`:140-144`), its `dacmode_s` long carries `…_01_00000_0` — **`%TT = %01`,
smart pin off** (`:205`) — and it `wrpin`s + `dirh`s pins 0..3 to take the four channels
(`:166-176`). Community code is a lead only; it is cited here because it independently matches all
three Silicon Doc statements, not as the basis for the claim.

**Consequence.** The Streamer Guide's §17.1 original form (`P_DAC_124R_3V | P_CHANNEL` alongside
`X_DACS_0N0_0N0`) was **right**, and «#221» was correct to doubt only because the *documentary
basis* had not been found — not because the code was wrong. The sprint may now author the
streamer-fed DAC setup from documentary authority.

**A bench run is no longer required, but is still recommended** — this is the exact axis where
**F-264** proved the two arrangements invert (a constant that is mandatory in one context kills
the output in the other), so a jumper-rig confirmation is cheap insurance. It confirms rather than
decides. Rig spec: `engineering/planning/STREAMER-GUIDE-CORRECTNESS-SPRINT-PLAN.md` §1b.

**Still genuinely unstated by any source:** nothing load-bearing. `M[3:0]` is described as
carrying the COGID; no source decomposes it further, and none needs to.

**Downstream:** the P2AN001 / P2AN003 / P2AN004 cog-DAC re-audit named under **F-264** is
unblocked by this — it was waiting on this question.

---

## ROOT CAUSE of the XBYTE `_RET_ CALL` defect — the KB dropped a qualifier (2026-08-16) — F-273

## IOSP suppressed-qualifier probe (2026-08-16, «#230») — F-274…F-275

> **Method and full result:** `engineering/analysis/2026-08-16-iosp-suppressed-qualifier-probe.md`.
> The probe asked whether a qualifier was ever **never written** — the half no diff can see, after
> «#214» returned NIL on qualifier *removal*. Result is **not nil**: two findings, both in Ch.19,
> the one chapter our own `KNOWLEDGE-GAPS.md` already flags as OPEN (G-005).
>
> **The pattern is the useful part, and it inverts hedge-counting.** Ch.16 (ADC) — the chapter that
> qualifies most — is right, and says so explicitly (*"nominal resolution … not ENOB"*, *"a
> mechanism, not a guaranteed specification"*, *"never a datasheet value"*). Ch.19 — the chapter
> that qualifies least — is the one with the gap. The guide is well calibrated where its evidence
> is rich, and goes quiet about its own uncertainty exactly where the evidence is thinnest. The
> signature to look for is a missing **dependency**, not a missing **word**.
>
> **Neither finding ships in the current wave.** IOSP left it when F-261 reversed into F-269, so
> both wait for IOSP's next release rather than being force-fitted into this one.

### F-274 — IOSP Ch.19 §19.4 teaches an FS-USB configuration at exactly the clock its own source flags, and states no sysclk dependency anywhere. `CONFIRMED`

**Location:** `manuals/p2-io-and-smart-pins-user-guide/opus-master/part-4-special-modes/chapter-19-usb.md:122-128`.
**RELEASED (v1.0.8).**

The chapter's only worked baud example computes full-speed (12 Mbps) USB at **80 MHz**.
`engineering/ingestion/KNOWLEDGE-GAPS.md` **G-005 is OPEN**: *"Scope of smart-pin USB support;
documented sysclk floor (**FS-USB > 80 MHz**, LS-USB less)."* The chapter states **no sysclk
dependency for USB anywhere** — not in §19.4, not in §19.9 Limitations, not in the Quick Reference.
A reader following the worked example lands on the boundary the open gap is about with nothing to
tell them a boundary exists.

**Do NOT "fix" this by asserting the floor.** G-005's only source is a reviewer comment (Granville)
on the Titus document — an **upstream lead, not a citation**, and not something to carry into
reader-facing prose as fact. Doing so would trade a silence for an unsourced claim.

**Proposed correction:** rework the worked example at a clock unambiguously clear of the question
(the chapter's own Spin2 example at `:264` already runs at 200 MHz), and state that USB signaling
needs sysclk headroom with the exact floor unsettled. §19.4's existing transmit-pacing `::: caution`
is the shape to copy — it already names its own limit correctly.

**Not in scope of this finding:** the register-layer content (WXPIN config word, WYPIN line states,
the 16-bit RX status word, per-pin IN semantics) is properly sourced to Silicon
`p2-documentation.txt:8886-9006` and was verified sound during the probe. It is not implicated.

### F-275 — IOSP Ch.19 §19.5 states the P2 provides USB bus power; §19.8 correctly says it does not. `CONFIRMED`

**Location:** `…/chapter-19-usb.md:210` against `:329`. **RELEASED (v1.0.8).**

`:210` — *"As a USB host, the P2: **Provides bus power (5V)**"*. The P2's I/O is 3.3 V and it
sources no 5 V rail. `:329` correctly lists *"5V power supply for VBUS"* among the external
components a host design must provide.

A plain factual error, self-contradicted two sections later. Not a calibration defect — surfaced by
the same read-the-claims pass, and recorded here rather than split off because it was found by the
probe and belongs with its record.

**Proposed correction:** §19.5 says the P2 *initiates* communication and *requires* a board-supplied
5 V VBUS rail, pointing at §19.8 for the external components.

**RESOLVED 2026-08-17 («#246»).** The bullet is out of the P2-verb list — it never described anything
the P2 does — and the fact it was carrying now stands on its own after the list: a host port supplies
5 V on VBUS, the P2 cannot source it (3.3 V I/O), and §19.8 has the external supply and its current
limiting. Fixed in opus-master; **IOSP is not in the release wave**, so it ships at IOSP's next
release alongside F-278's site conversions.

**ROOT CAUSE, and the fix extended (Stephen, 2026-08-17).** The claim was not invented — **the P2 Edge
breakout boards really do carry 5 V to the I/O headers**, which is almost certainly where "the P2
provides bus power" came from. Removing the wrong sentence without explaining the true one would have
left the next reader to make the same inference from the same board. §19.8 now carries what the board
guides actually say, and it is more specific than "the headers have 5 V":

- Each 8-pin accessory header provides two grounds, a **Vxx** pin (3.3 V from that group's LDO), and
  **optionally** 5 V — **passed straight through from the power jack**, not generated by the board.
- **Two headers have no 5 V routed at all: P24–P31 and P56–P63.** The second bank contains **pins
  56/57, which is the pair this chapter's own examples use** — so the chapter was teaching a host
  design on the one header that cannot supply its VBUS.
- Because the header 5 V is the input supply passed through, it carries no current limit, so §19.8's
  current-limiting requirement still lands on the design.

**Sources (three board guides, consistent):** *P2 Edge Mini Breakout Board* (#64019) §6–§7, *P2 Edge
Breakout Board* (#64029) §6–§7, *P2 Edge Module Breadboard* (#64020) §12–§13 — the last gating header
5 V behind an ACC ON/OFF shunt. The guides anticipate the confusion themselves: *"5V OUTPUT VOLTAGE IS
PROVIDED TO POWER EXTERNAL ACCESSORIES & SENSORS. DO NOT CONNECT 5V DIRECTLY TO ANY OF THE P2 SMART
I/O PINS! ALL I/O PINS OPERATE AT 3.3V LOGIC LEVEL AND ARE NOT 5V TOLERANT!"*

**Class-wide sweep done, and it is clean.** Every other `5 V` mention across all manual and app-note
masters was read: the Architect's Guide (level shifters), deSilva ("P2 is 3.3V, not 5V tolerant"),
IOSP Ch.12 (legacy 5 V logic as an input case), and P2AN004 (the TSL235R's 2.7–5.5 V supply range) are
all correct. **F-275 was the only site** — verified rather than assumed.

**Related — looked at and FIXED 2026-08-17, at the next pass as scheduled.** Pins 56/57 are also the
Edge Module's onboard LED pins and sit in the programming/WX-adapter bank — and the manual itself uses
56 as `LED_PIN` in five places and 57 as `BUTTON_PIN`. Worse, this very release adds the statement
that P56–P63 carries no 5V, so the chapter would have demonstrated a **bus-powered** peripheral on the
one bank with no bus power. §19.8 had absorbed that by adding a caveat — *"the pin pair this chapter's
examples use... must take VBUS from elsewhere"* — which is a workaround for a pin choice, not a
reason for it.

**Chapter 19's examples now use P8/P9**: a free even/odd pair in a 5V-bearing bank, clear of every
other pin constant in the manual. The §19.8 caveat is gone with the need for it, and the bank fact
stands on its own. Verified: byte-identity GREEN 15/15, `ch19-usb-device-config.spin2` compiles clean
under `pnut-ts -d`, all IOSP gates clean. The "Valid pairs" enumeration still lists 56/57 — it is an
enumeration of what the silicon allows, which is unchanged.

**The lesson is the caveat itself.** Prose was written to explain around a defect instead of removing
it, and that prose then read as settled. A sentence that exists only to excuse a choice is a marker
for the choice, not a resolution of it.

**Next finding ID after this block: F-276.**

---

## Stephen's review of the Sprint 2 gate release (2026-08-16, «#234») — F-276…F-279

> **Full dispositions and reasoning:** `engineering/planning/SPRINT2-VISUAL-REVIEW-NOTES-2026-08-16.md`.
> Eight observations (V-1…V-8) worked one at a time against the gate commit `fea28f1c`. Four became
> findings; the rest were scope and structure decisions recorded in that file.
>
> **All four are tasked into the voice-conformance family «#240»–«#248» and are absorbed into the
> per-manual pass rather than applied as point fixes** — applying them first and conformance-checking
> after would write the same prose twice and have the second pass judge what the first just wrote.
>
> **Two of these were found by the review, not by the sprint's own sweeps**, and that is the useful
> part: F-277's site sits in body text no Sprint 2 task touched. A findings-driven sweep sees the
> diff; it does not see the document.

### F-276 — deSilva Appendix A grounds the P2's value in "missed deadlines," an argument that fails against the reader it is aimed at. `CONFIRMED`

**Location:** `manuals/p2-pasm-desilva-style/opus-master/COMPLETE-OPUS-MASTER.md` — §*"What You Are
Buying With That"* (`:5993-6001`), with the same shape at `:225`, `:6001`, `:6049`.
**NOT RELEASED** — written during Sprint 2, committed at `fea28f1c`, ships in v3.0.6.

The section argues that conventional MCUs turn hard real-time into a scheduling problem with "a long
tail of *why did that deadline slip once an hour?*", and that the P2 therefore "raises your odds of
finishing." Three defects:

1. **It argues against a strawman.** A correctly prioritised Cortex-M meets its deadlines; rate-monotonic
   analysis is fifty years old. An RP2350 PIO state machine meets them absolutely. The reader best
   qualified to judge the appendix concludes we are comparing the P2 against *badly built* alternatives.
2. **It is unfalsifiable and unsourced.** "Raises your odds of finishing" is a project-outcome claim with
   no evidence — a marketing claim in an engineering voice, in a document whose credibility is its
   checkability.
3. **It contradicts a passage two pages earlier.** The RP2350/PIO paragraph added in the same sprint
   (`:5868`) already tells the reader that cheap deterministic offload hardware exists.

It is also a declared **R1** violation under the manual's own `voice-guide.md` (ADOPT, scoped to
technical P2 claims), written the day before the prose was.

**Proposed correction:** replace with the **composability** claim — adding a task to a shared core
perturbs the timing of the tasks already there; giving a task its own cog does not. Take the concept
from the Architect's Guide Ch.7 but **not its vocabulary** (no "forces", no "cadence boundary"): use
cogs, pins and locks, which the reader has earned over sixteen chapters. The section must stand fully
alone for a reader who never opens that book. Sweep the same shape at `:225`, `:6001`, `:6049`;
`:4275` uses "deadline" legitimately (delta-vs-absolute comparison under counter wraparound) — leave it.

### F-277 — deSilva tells the reader that peripheral conflicts are impossible on the P2. They are not, and our own published manual documents why. `CONFIRMED`

**Location:** `…/COMPLETE-OPUS-MASTER.md:6045` — *"**64 smart pins** means peripheral conflicts become
impossible"* — and `:5940` — *"I/O flexibility that eliminates peripheral conflicts."*
**RELEASED (v3.0.5)** — both sites are pre-existing body text; neither was touched by any Sprint 2 task.

Smart pins eliminate the **pinmux** conflict: any pin can be any function, so a design never runs out of
"the SPI pins." They do **not** eliminate **resource** conflict. *The P2 Architect's Guide* (v1.0.3,
Ch.7 Force 1) states the opposite from the silicon: P2 pin outputs are OR'd with no hardware arbiter, so
two cogs driving one bus corrupt it — and the symptom "presents as flaky hardware — intermittent,
timing-dependent, and miserable to debug, because the symptom is three layers away from the cause."

This is the most expensive kind of wrong claim: it tells a beginner that a real, nasty bug class cannot
happen, in the manual most likely to be their first contact with the chip. It is also a declared **R1**
violation, whose stated reason is precisely this case — *"a tutorial's worked examples are exactly where
an overstated claim reaches a beginner who cannot yet check it."*

**Proposed correction:** state what smart pins actually remove (the pinmux conflict, and running out of
peripheral blocks) and keep single-ownership of a shared bus as a live concern. **Class-wide check
owed:** the same "conflicts impossible / eliminates conflicts" phrasing may appear in other manuals.

**Related, same pass, same manual — not separately numbered:** `:6042` "eliminates entire categories of
problems"; `:3897` "No surprises, ever / Timing is guaranteed", self-contradicted by the *correct* hedge
at `:5911` (5911 is right); `:3729` "impossible to achieve this precision with interrupts" (F-276's
strawman); `:5804`'s impossibility aside. ⚠️ **The reader-celebration at `:5804` STAYS** — deSilva's
voice guide explicitly protects celebration of reader progress as pedagogy, and an early draft of this
finding wrongly proposed cutting it.

### F-278 — wrong-code examples ship in ordinary syntax-highlighted blocks, distinguished only by a comment, in three manuals. `PARTIAL`

**Locations (8 sites — the 7 first enumerated, plus the 8th the narrow pattern missed).** Sites are
named by section rather than by line, because master line numbers move with every content task and a
stale number sends the next reader to the wrong block. **All 8 are CONVERTED, and 7 of them have
SHIPPED — verified against the release tags on 2026-08-20 («#282»), not inferred from this register:**

| Manual | Site | State |
|---|---|---|
| Streamer | §13.4's `\|`-vs-`+` pair | converted · **RELEASED v1.0.9** (2026-08-19) |
| Debug Window | `ch12-bidirectional.md`, both sites | converted · **RELEASED v1.1.3** (2026-08-18) |
| IOSP | `appendix-e-troubleshooting.md` ×3, `chapter-17-serial-receive.md`, `chapter-11-serial-transmit.md` | converted · **RELEASED v1.0.9** (2026-08-18) |
| Debug Window | `ch08-scope-xy.md` blockquote pair | **deliberately deferred** — see below |

**This annotation used to read `(NOT RELEASED, v1.0.9)` / `(NOT RELEASED, v1.1.3)` / `(RELEASED,
v1.0.8)`, and all three were stale.** The releases happened on 2026-08-18 and 2026-08-19 and nothing
came back to say so. Note the direction: the record understated what had been done, so a reader is
sent to redo finished work. `audit-register-hygiene.py` cannot see this class — it detects only the
opposite drift, a headline claiming a fix over a status token that does not agree. Same gap as F-272.

The platform provides `AntipatternBlock` (`p2kb-platform-content.sty:277` — red fill, red border, 4 pt
left rule), reachable as a ```` ```antipattern ```` fence or `::: antipattern` div via
`p2kb-platform-code-coloring.lua`. deSilva (6 sites) and Assembly (`appendix-h-reserved-words.md:569`)
use it correctly. The seven sites above do not — wrong code sits in ```` ```spin2 ````, marked only by a
`' WRONG` comment, so it carries identical highlighting and identical visual authority to correct code.

**Streamer's is the worst**, because the correct and the wrong form share **one block**. A reader
skimming code blocks — how people actually use a reference guide — can lift the wrong line without
reading the comment. It is the EF-053 `P_OE` material, where the failure is silent and total: measured
on silicon at 6,737 ADC counts for `|` against 1,407 for `+`, indistinguishable from no drive.

**Proposed correction:** split Streamer's into two **adjacent** blocks — correct stays ```` ```spin2 ````,
wrong becomes ```` ```antipattern ````. Green beside red is a stronger contrast than two comments in one
block, so the pedagogy improves rather than suffers. Convert the Debug Window and IOSP sites in place.

**Zero platform cost — verified:** `p2kb-streamer-reference.latex:21`, `p2kb-debugwin.latex:23` and
`p2kb-iosp-reference.latex:22` all already load `p2kb-platform-content.sty`. Markdown-only in all three.

**A fourth Debug Window site is deliberately NOT converted.** `ch08-scope-xy.md:71` pairs a wrong
line and its corrected form inside a **blockquote** callout (`> ```spin2`). Converting it would make
`> ```antipattern` the **first instance of that fence-inside-blockquote combination anywhere in the
set** — `> ```spin2` appears only in this one file (2 uses, shipped in v1.1.2, so that form is
render-proven; the antipattern form is not). Introducing an unverified fence combination into a
manual shipping in the current wave risks a silent render defect for a two-line paired contrast that
already reads correctly. **Action: verify `> ```antipattern` at the next Forge round-trip
(`forge-test`), then convert if it renders.** Same reasoning as the `\|`-in-a-table-code-span trap:
no precedent in the set is a render risk, not a green light.

**IOSP is not in the release wave.** Its sites are fixed in opus-master and ship at its next release —
editing a master is not releasing a document. *(That next release came: **v1.0.9, 2026-08-18**. All
five conversions are in the tag.)*

**IOSP RESOLVED 2026-08-17 («#246») — five sites, not four.** The four declared sites are converted.
A **fifth** turned up because this pass used the broader wrong-code pattern
(`WRONG|Wrong|INCORRECT|Do not do this`) rather than the `^' *WRONG` form that missed the Debug Window
blockquote: `part-2-output-modes/chapter-11-serial-transmit.md:174`, a `**Wrong:**`-labelled
```` ```spin2 ```` block already paired with its `**Correct:**` twin. **The narrow pattern under-counted
this finding in two manuals; the enumeration above is the floor, not the census.** Three of the IOSP
sites carried the wrong and correct forms in **one** block and were split the way Streamer's was —
```` ```antipattern ```` then ```` ```spin2 ```` — so the reader gets red-beside-green rather than two
comments in one box.

**Status:** `PARTIAL — 8 of 8 sites converted; 7 shipped (Streamer v1.0.9, Debug Window v1.1.3, IOSP
v1.0.9). What remains is ONE site and it is gated, not forgotten: ch08-scope-xy.md's blockquote pair
waits on verifying that `> ```antipattern` renders, because no manual in the set has ever used that
fence-inside-blockquote combination. Verify it at the next Debug Window Forge round-trip, convert if
it renders, and this finding closes.`

### F-279 — the XBYTE guide grounds a load-bearing hardware claim on a sibling manual in the same family, without disclosing it. `CONFIRMED`

**Location:** `manuals/p2-xbyte-programming-guide/opus-master/xbyte-body.md:1427`.
**NOT RELEASED** — written during Sprint 2 («#227»), ships in v1.0.2.

The `_RET_ CALL` hazard block cites *"the condition table in the **P2 Assembly Language Reference
Manual**"* for `_RET_`'s branch-conditional semantics. That title is **not fabricated** — it is the cover
title of our own manual (`p2-assembly-language-manual/opus-master/front-matter.md:20`). The defect is
**circularity**: a peer derivation cannot ground a hardware claim, and unlike `P2AN002.md:378` — which
cites the same manual while labelling it *"a companion P2 Knowledge Base publication"* — this site
discloses nothing, so it reads to a reader as an external authority.

**Proposed correction:** repoint to the Parallax primary sources F-273 was actually grounded on —
*Propeller 2 Assembly Language (PASM2) Manual* draft (2022-11-01, p.68) and *P2 Instructions v35*
(row 410). **Verify the citation against the live source, not against this register** — a ledger is not
citation authority, and this guide has shipped fabricated names before (Appendix C).

**No set-wide normalisation owed.** The other four sites naming this document were checked and are
sound: deSilva `:5845` uses the Parallax name correctly, and the remainder are our own cover title and a
CHANGELOG font note.

### F-280 — `pnut_ts` survives in 16 masters as a command that does not run. `CONFIRMED`

**Found:** 2026-08-17 during the P2AN001/P2AN002 voice pass («#247»), by checking the compiler name
the two notes hand the reader against the name of the binary that exists.

**This was already adjudicated and only half-swept.** Commit `c203fa52` (2026-08-11) established the
finding on its merits: `command -v pnut_ts` finds nothing, the installed binary is `pnut-ts`, and the
tool's own usage banner reads *"PNut-TS: Usage: pnut-ts [optons] filename"*. SSDB and the PNut-Term-TS
guide were corrected then — 21 sites — and both voice guides were amended so it could not come back.
**The rest of the set was never swept.** Thirty-three occurrences remain across eighteen files, against
thirty-nine correct ones — a near-even split, so the set currently teaches both.

**Fixed in this pass (2 sites, the two notes being touched):** `P2AN001/opus-master/CHANGELOG.md:37`
and `P2AN002/opus-master/CHANGELOG.md:35`. Both are reader-facing — an app-note CHANGELOG is promoted
to the published `p2anNNN-changelog.md` beside its PDF.

**Remaining (31 sites, 16 files) — the class-wide sweep this finding owns:**

| Element | Sites |
|---|---|
| Getting Started Guide | `getting-started-body.md` ×1 — **highest reader risk**: a beginner's first compile |
| Architect's Guide | `architect-guide-body.md` ×1, `CHANGELOG.md` ×2 |
| Assembly Language Manual | `CHANGELOG.md` ×1 |
| PNut-Term-TS Guide | `CHANGELOG.md` ×1 (the body was swept at `c203fa52`; its CHANGELOG was missed) |
| deSilva | `archived-2025/README-COMBINED-MASTER.md` ×3 — **archived scaffolding, not shipped; excluded** |
| P2AN003 – P2AN007 | body ×17, `CHANGELOG.md` ×5 |

**Not swept here on purpose.** Conform-on-touch: these elements are not being touched by Sprint 2, and
pulling sixteen masters into a voice pass is the big-bang sweep the rule exists to avoid. Each takes it
at its next visit — this row is what makes sure the visit knows.

**The correction is one substitution** — `pnut_ts` → `pnut-ts` — with no prose consequence. Check each
site is the *command*; the project name in running text is properly **PNut-TS**.

### F-281 — three code lines run off the page in the RELEASED Debug Window PDF, taking part of the program with them. `CONFIRMED` — **ALL THREE FIXED 2026-08-17; no longer blocks v1.1.3**

**Found:** 2026-08-17 running the wave's code-line gate before staging («#235»).
**RELEASED (v1.1.2), and v1.1.3 would re-publish it unchanged.**

**Looked at, not inferred.** Page 80 of `deliverables/documents/DOCs/P2-Debug-Window-Manual.pdf`
rendered at 130 dpi: the `DEBUG(\`Waves 'Sine' …` line of the "complete worked example" overruns the
blue code box, overprints the right margin, and is cut off at the paper edge — the third channel's
`200 0 $00AAFF)` is simply not on the page. A reader copying that example gets a program that does
not compile and an example that promises three channels while showing two and a fraction.
(`pdftotext` was the first signal, but it is only a claim; the page image is the evidence. An earlier
`pdftotext` hit on page 76 was a **different**, correctly-rendered passage — checking the image is
what separated them.)

**The three sites, all in captioned `.spin2` blocks with example-library twins. All three pages were
rendered and looked at; the severities are NOT equal:**

| Site | Len | Survives | What is lost | Program? |
|---|---|---|---|---|
| `ch07-scope.md:272` | 121 | ~101 | `100 200 0 $00AAFF)` — the **third SCOPE channel** | **BROKEN** — example promises three channels, shows two and a fraction |
| `ch06-logic.md:310` | 113 | ~101 | `SI' 1 $FFFF00)` — the **third LOGIC channel + the closing paren** | **BROKEN** — line does not even close |
| `ch14-multiwindow-pasm.md:299` | 110 | ~94 | `' fresh status block` — a **trailing comment only** | **INTACT** — code complete through its `)` |

**So only two of the three are functionally broken.** The ch14 site loses a comment and looks wrong;
its program is whole. That matters for triage: ch07 and ch06 hand the reader code that cannot run.

**Capacity is ~101 columns, measured from the left edge INCLUDING indentation.** That is why ch14 cuts
at 94 rather than 101 — it sits four spaces deeper. The budget is a *column* budget, not a
content-length budget, so a deeply nested line has less room than a top-level one.

**MECHANISM — and it points at a one-line platform fix.** Code blocks do **not** render through
`listings`. `p2kb-platform-code-coloring.lua` emits every block as
`\begin{Spin2Block}\begin{Verbatim}[xleftmargin=-10pt]…` — **fancyvrb's `Verbatim`, which has no line
breaking by default.** The `breaklines=true` in `p2kb-platform-foundation.sty`'s `\lstset` (line 317)
is **dead code for these blocks**; it configures a package this path never reaches. An over-wide line
therefore runs off the page instead of wrapping, and nothing stops the build.

**PROVEN ON THE DAEMON 2026-08-17 — and the fix is NOT what this finding first said.** Adding
`breaklines=true` to the filter's `Verbatim` options converts silent truncation into visible wrapping
across the whole document set and demotes K from a correctness cliff to a style budget. Confirmed by
round-trip, not by reading.

**Correction: `breaklines` is NOT a base-fancyvrb option.** The first attempt (`breaklines-v1`) failed
outright — `! Package keyval Error: breaklines undefined`, `No pages of output`. The Forge's
`fancyvrb.sty` does not know the key; `breaklines`, `breakanywhere`, `breaksymbolright` and
`breakindent` come from **`fvextra`**. So the platform change is TWO edits, not one:
1. `\RequirePackage{fvextra}` in `p2kb-platform-foundation.sty` (fvextra IS present in the Forge's
   TeX Live — verified), and
2. the options on every `Verbatim` the code-coloring filter emits (**10 sites**, not one).

**What it looks like (`breaklines-v2`, clean build, page rendered and READ).** Options used:
`breaklines=true, breakanywhere=false, breaksymbolright=\tiny\ensuremath{\hookrightarrow},
breakindent=2em`. Every previously-lost fragment came back:

| Case | Before | After |
|---|---|---|
| SCOPE, 121 cols | third channel gone | `'Noise' -1000 1000 100 200 0 $00AAFF)` visible, closing paren included |
| LOGIC, 113 cols | third channel + `)` gone | `'MOSI' 1 $FFFF00)` visible |
| IOSP, 103 cols (F-289) | comment cut at `bits 0..` | `(REV n covers bits 0..n)` visible |
| normal-width control | — | untouched: no wrap, no marker |

`breakanywhere=false` keeps breaks on whitespace, so no token is split mid-word, and the `↪` marker
appears at BOTH the break and the indented continuation — a reader cannot mistake a wrap for authored
structure, which was the open worry.

**REJECTED 2026-08-17 — and the round-trip is what disproved it.** Stephen: *"one thing we shouldn't
ever do is wrap code or comments within the code."* That policy is DECLARED, in two places, with this
exact reasoning: `p2kb-platform-code-coloring.lua`'s header (*"a typeset wrap can't break a comment and
re-indent it, nor add a language line continuation, so it produces wrong-looking code AND hides the
problem"*) and `audit-code-line-length.py`'s own docstring. It was proposed and tested against a
declared decision without that check being run first.

**The render is the evidence the policy is right.** Both failure modes the policy names showed up in
`breaklines-v2`:

| Case | What the continuation line actually printed | Why it is wrong |
|---|---|---|
| C (comment) | `(REV n covers bits 0..n)` | **no `'` prefix** — a comment's tail rendered as though it were code |
| A (statement) | `$FF0000 'Noise' -1000 1000 100 200 0 $00AAFF)` | **no Spin2 `...` continuation** — copy-paste yields a syntax error |

Worse than truncation in one specific way: a truncated line is *visibly* broken, so a reader notices.
A wrapped line looks complete and copies as broken. And it would have removed the pressure to fix the
source, which is the "hides the problem" half.

**Adoption reverted; the platform source never carried the patch** (it was tested on the daemon copies
only, now restored). `fvextra` availability is recorded here only so nobody re-derives it.
**Re-verified 2026-08-19: the tree is still clean of it.** No `fvextra` in the platform templates, and
`p2kb-platform-code-coloring.lua` emits `\begin{Verbatim}[xleftmargin=-10pt]` with no break options at
all 10 sites. The `breaklines=true` at `p2kb-platform-foundation.sty:317` is the pre-existing `\lstset`
dead code this finding identified — it is NOT residue of the patch, and removing it is not owed.

⚠️ **THE REJECTION DID NOT PROPAGATE, AND THAT IS THE MORE EXPENSIVE DEFECT. Swept 2026-08-19.**
The rejection landed here and in `PUNCH-LIST.md` on 2026-08-17 at 20:02. It never reached the task
tracker: todo «#250» was created the next day carrying this finding's **pre-rejection** text verbatim —
mechanism, `FIX: add breaklines=true`, `USE forge-test` — and from there the dead plan was cited as a
live commitment in four more places written over the following two days:

| Where | What it claimed | Written |
|---|---|---|
| todo «#250» | the fix, as work owed | 2026-08-18 (out of «#249»'s close) |
| `XBYTE-…-SPRINT-PLAN.md:626` | "not in this sprint" — i.e. still scheduled | 2026-08-18 04:36 |
| `PUNCH-LIST.md:437` | "same profile as the `breaklines` work «#250»" | 2026-08-18 21:12 |
| F-300 sequencing (this file) | "three set-wide render changes" | 2026-08-19 |
| F-299 (this file) | "Pair it with «#250»" | 2026-08-19 |
| `active_element` resume key | «#250» as "**THE REAL ONE**", top of next-work | 2026-08-19 |

Every one of those was authored **after** the rejection, by reading the task rather than the register.
Stephen caught it at the next session's resume — the front door recommended, as the single best next
piece of work, a change he had personally rejected on the render two days earlier.

**The mechanism, and it is general.** A finding's disposition can change after tasks have been cut
from it. The register is the source of truth, but the tracker is what a resume reads first, so a
reversal recorded only in the register is invisible where decisions actually get made. **When a
finding is rejected, reversed, or re-graded, sweep every artifact that carries its plan in the same
commit** — todo tasks first, then punch list, sprint plans, and any other finding that cites it.
`grep` for the finding ID *and* for the task number: this one propagated under «#250», not "F-281".
See [[feedback_classwide_sweep_on_every_finding]]; the class here is *pointers to a decision*, not
occurrences of a fact. All six sites above are now corrected (dated records — the closed XBYTE sprint
plan and the Streamer PUBLISH ledger line — are annotated, not rewritten).

**THE FIX IS AUTHORSHIP, as the policy always said.** Over-long lines get shortened in `opus-master` by
the sanctioned routes — comment moved to full lines above the instruction at its indent, or split with
the continuation comment's `'` aligned to the inline `'` column; a statement broken at a logical
boundary with the legal Spin2 `...`. The real mechanism is the **gate**, and F-289 just repaired it:
it had been skipping every captioned block, which is why 24 Debug Window and 11 IOSP lines went
unreported. A working gate plus authorship is the answer; a typeset wrap was never it.

**Re-authoring was therefore REQUIRED, and it was done — all three sites, 2026-08-17.** ⚠️ *This
paragraph previously read "with wrapping visible, the SCOPE and LOGIC lines are no longer losing
content, so shortening them becomes a style choice rather than a repair." That was written before the
rejection and survived it, sitting inside this entry asserting the opposite of the entry's own verdict.
**Corrected 2026-08-19.*** With the wrap rejected, nothing rescues an over-wide line at render time:
the SCOPE and LOGIC lines were losing content, shortening them was a repair and not a style choice, and
the LOGIC case did have to be solved on its own terms. Commits `2747fd91` (the last two over-cliff
lines) and `1b918d4c` (the LOGIC line) did it. **Verified 2026-08-19, not assumed:**
`audit-code-line-length.py` runs clean across all 30 Debug Window masters at K=76 — zero violations.

**The declared budget is right; the other 21 over-budget lines are lucky, not correct.** Twenty-four
lines exceed the manual's declared `code_line_budget_K: 76`. Measured against the shipped PDF, only
these three are actually lost — the real overflow threshold sits between 100 and 110 characters. That
is exactly why K is set conservatively at 76, and the twenty-one between 77 and 100 should come down
at the manual's next authoring pass. **They are not part of this fix**; only demonstrable breakage is.

**Why this is not a one-line edit.** These are compilable examples under a byte-identity gate, so any
change lands in `examples-library/*.spin2` too, and the shortened form has to be one that *works* —
not merely one that fits.

**The SCOPE fix is determined at the source level.** `vIndex` (the active-channel count) is set to `0`
in `SetDefaults` only, which runs **once at window creation** (`SCOPE_Theory_of_Operations.md` §21.1,
`DebugDisplayUnit.pas` 2880-2917). Nothing resets it per update message, and the channel-def branch
only ever increments it (`if vIndex <> Channels then Inc(vIndex)`, 1219). So three separate update
messages accumulate to three channels, identical to one message declaring three:

```spin2
debug(`Waves 'Sine'  -1000 1000 100   0 0 $00FF00)
debug(`Waves 'Tri'   -1000 1000 100 100 0 $FF0000)
debug(`Waves 'Noise' -1000 1000 100 200 0 $00AAFF)
```

Roughly 50 characters each. **Not applied**, because the mechanism being understood is not the same as
having seen it run, and a corrected-looking recipe is worse than a visibly broken one. This needs one
bench execution to close — the window either shows three stacked traces or it does not.

**A splice on one physical line is NOT available, and the control proved it.** `-` as a continuation
inside the backtick string **compiles clean and silently changes the program**: 9,338 bytes against
9,408 for the one-line form, the trailing channels dropped. A clean `pnut-ts` compile is legality,
never semantics — the byte-compare is what caught it.

**LOGIC checked and cleared — not the same defect.** `ch06-logic.md:310` puts channel labels on the
LOGIC *create* line, which for SCOPE would abort window creation entirely (EF-003). LOGIC's
Theory-of-Operations shows the opposite: labels belong on its create line, and only `TRIGGER` must be
split out — which this example already does correctly. **LOGIC's problem is length alone.** Because
its labels cannot move to a second message, the fix there is authorial (shorten `TITLE`, or drop the
explicit colors and take the defaults) and changes what the example teaches. `ch14`'s TERM site needs
its own positional check against `TERM_Theory_of_Operations.md` before being split.

**Platform observation worth its own look:** the overflow is *silent at build time*. The compile log
was clean, the Forge reported success, and the manual shipped. A code line that runs off the page with
no overfull-hbox stop is a render failure that only a human looking at the page will catch — which is
the whole reason the "verify the rendered PDF, not the log" rule exists, and an argument for making
the platform's listing environment fail loudly instead.

### F-282 — every `MANUAL-DESCRIPTOR.md` records a stale `last_published_tag`, so every diff-since-published audit reads the wrong baseline. `CONFIRMED` — **the 3 release-wave descriptors corrected 2026-08-17**

> **Wave descriptors fixed 2026-08-17**, each checked against `git tag` rather than against the file's
> own claim: Debug Window `v1.0.0`→**`v1.1.2`**, IOSP `unreleased`→**`v1.0.8`**, Assembly
> `v3.1.2`→**`v3.1.5`**. Their trailing baseline comments described the OLD tags (wrong dates, wrong
> page counts, one still calling IOSP a maiden release) and were rewritten to the real released dates
> and page counts. **A stale comment beside a corrected value is the same defect wearing a disguise.**
> Descriptors outside the wave are untouched and still stale.

> **Rewritten in place 2026-08-17, hours after it was filed.** The original text claimed the app-note
> *tags* were two to three releases behind and that the app-note release path "never lays the tag."
> **That was wrong, and the error was in the probe, not the repo.** The scan grepped for the
> uppercase prefix `P2AN001-`, but the app-note tag namespace switched to **lowercase** at the
> 2026-07-12 fleet release. `p2an001-v1.0.3`, `p2an002-v1.0.2`, `p2an003-v1.0.2`, `p2an004-v1.0.2`
> all exist, and `git for-each-ref --format='%(creatordate:short)'` shows each was created **on its
> release date** — not retroactively. Every app note and every manual is tagged current. The
> conclusion "specific to the app-note release path" was false in both halves.
>
> The *symptom* the finding described is real. The cause is below.

**Found:** 2026-08-17, enumerating what was pending for release alongside Debug Window and IOSP.
**Corrected the same day**, when preparing the six-element wave put the actual tag list on screen.

**The tags are complete.** Every released version of every manual and app note has a tag at the
commit that shipped it. Nothing is owed here.

**The descriptors are stale.** `document-audit`'s changeset-integrity dimension (Dimension #15) does
not read `git tag` — it reads the `last_published_tag:` field in each `MANUAL-DESCRIPTOR.md`. Those
fields were written at seed time and never advanced by a release:

| Element | Descriptor says | Actually released + tagged | Baseline error |
|---|---|---|---|
| P2AN001 | `unreleased` | **1.0.3** | whole doc reads as unreviewed |
| P2AN002 | `unreleased` | **1.0.2** | whole doc reads as unreviewed |
| P2AN003 | `unreleased` | **1.0.2** | whole doc reads as unreviewed |
| P2AN004 | `unreleased` | **1.0.2** | whole doc reads as unreviewed |
| Assembly | `v3.1.2` | **3.1.5** | 3 releases of published work |
| Streamer | `v1.0.6` | **1.0.8** | 2 releases |
| deSilva | `v3.0.1` | **3.0.5** | 4 releases |
| Debug Window | `v1.0.0` | **1.1.2** | 5 releases |
| XBYTE | `none` — "NOT yet released" | **1.0.1** | whole doc reads as unreviewed |

So this is **not** an app-note problem. It is fleet-wide, and it is worse on the manuals than on the
app notes — the opposite of what the original finding said.

**Why it bites.** With the recorded baseline several releases behind, the audit diffs against content
that shipped months ago and reports **already-published work as unreviewed change** — noise that
trains the reader to skip the signal. It fails in a direction that looks like diligence.

**A second, smaller defect, and the one that caused the misdiagnosis:** the app-note tag namespace is
**case-inconsistent** — `P2AN001-v1.0.0`/`-v1.0.1` uppercase, `p2an001-v1.0.2` onward lowercase. Any
case-sensitive lookup of a "latest tag" silently resolves to the pre-July tag. That is what made the
original probe read three missing releases that were never missing.

**Fix:** (a) advance every `last_published_tag:` to the element's actually-released tag, and make
advancing it a step in `release-manual` so it cannot drift again; (b) settle the app-note tag case
one way and treat lookups as case-insensitive until it is. No tags need to be created.

**Lesson, recorded because it cost a wrong finding:** the probe's *absence of a result* was read as
a fact about the repository. A grep locates; it never concludes. This is the same failure mode as
"a status line is not evidence," and it was caught only because a later task put the full `git tag`
output on screen for an unrelated reason.

### F-283 — the P2AN002 YAML companion disagrees with the note it ships beside, on both a measured pitfall and an attribution. `FIXED (2026-08-17)` — companion brought into agreement on four entries; agreement gate GREEN

**Found:** 2026-08-17, running the doc↔companion agreement check while preparing P2AN002 v1.0.3 for
the release wave.

`MANUAL-DESCRIPTOR.md` states the gate: *"doc and `companion_yaml` must AGREE (composition recipe,
key parameters, gotchas)."* Two disagreements, both introduced when the note advanced to v1.0.3 and
the companion did not:

1. **The measured pitfall is missing.** The note's v1.0.3 headline is that hub access inside either
   CORDIC loop loses results, and does so **silently** — measured on real silicon at 200 MHz, with
   the failure depths stated (`P2AN002.md:322`). The companion's `gotchas:` block carries the
   pipelining entry as *"keep issued-minus-retired within what the pipeline holds"* and says nothing
   about hub traffic. An agent reading only the companion gets the recipe that was measured wrong.
2. **The OBEX #2812 attribution contradicts the note.** The note credits **ersmith** and uses the
   live catalog title *Binary Floating Point Routines (IEEE-32 subset)* — a v1.0.3 correction made
   against the live catalog. The companion's `community_examples:` still reads *"OBEX #2812 Binary
   Floating-Point (Total Spectrum Software)."*

**Location:** `deliverables/ai/P2/application-notes/p2an002-cordic-for-real-work.yaml` —
`gotchas:` and `provenance.community_examples:`.

**Action:** carry both into the companion, sourced from the note's v1.0.3 CHANGELOG entry and the
live OBEX catalog respectively.

**FIXED 2026-08-17.** Both carried into
`deliverables/ai/P2/application-notes/p2an002-cordic-for-real-work.yaml`:

1. The measured hub-access pitfall is now its own `gotchas` entry, with the silicon-measured failure
   depths (RDLONG in the fill loop loses results at depth 2; a WRLONG in the drain at 3; register-only
   in both loops correct through 7, at 200 MHz), the **silent** failure mode, and the actual cause
   (throughput, not a limit on results in flight). Sourced from `P2AN002.md:322`.
2. The OBEX attributions now match the live catalog.

**Two MORE disagreements surfaced while fixing it — the finding under-counted.** F-283 named two;
sweeping the whole `community_examples` block against the live catalog found four entries wrong or
incomplete, because the finding was written from the two the note happened to call out rather than
from the block:

| Entry | Companion said | Live catalog |
|---|---|---|
| #2811 | Park Transformation (ManAtWork) | ✅ correct |
| #2812 | Binary Floating-Point (**Total Spectrum Software**) | Binary Floating Point Routines (IEEE-32 subset), **ersmith** |
| #5278 | "compass drivers", **no author** | QMC5883L HMC5883 BMM150 compass drivers, **m.k. borri** |
| #5361 | FFT/IFFT (**SaucySoliton**) | FFT IFFT, **James Smith** |

All four verified against the live OBEX catalog via `p2kb_obex_get`, not from this register and not
from the note — per the standing rule that reader-facing names are verified against the LIVE source.
The note's own Resources list was already correct on all four; only the companion had drifted.

**Lesson — the same shape as [[F-223]]: a finding derived from the sites a document mentions is not
a finding about the block.** Audit the FULL structure, then re-derive what is wrong. Two of these
four would have shipped again had the fix been scoped to the finding as written.

**No document impact** — the note's text was already right, so P2AN002's PDF is unaffected and needs
no re-render. Validators green after the edit: `verify-yaml-format.py` 1129/1129 parsed clean,
`validate-crossref-keys.py` all resolved.

**Note on scope:** only P2AN002's companion was checked, because only P2AN002 was in front of me.
The same drift is plausible in every app note whose doc has advanced since its companion was
written — a names-only pass on one file is not coverage of the category.



---

## Open — enhancement proposals (new content, not corrections)

- **ENH-01 — Harvest the Architect's Guide *project front-end* into a new KB node set.** *Scheduled
  2026-07-08 (deferred from the Architect's Guide v1.0.0 release); Stephen go/no-go before authoring.*
  Source: *The P2 Architect's Guide* v1.0.0, **Part I (Act I)**. The decomposition-reasoning layer
  (`architecture/decomposition/`) begins *at* "which cog owns what"; nothing in the KB captures the
  **pre-decomposition** front-of-project work Part I lays out. Candidate new node set — reusable P2
  **design-process** patterns that sit *above* the decomposition layer: feasibility-before-design ·
  **narrow-vs-broad comms selection** (I²C/SPI vs host-style ribbon) · **offload-vs-port /
  companion-device partitioning** · pin-budget → adapter-board · "characterization becomes the spec" ·
  firmware-loaded-device → loader. Also a small KB touch worth doing: **performance → P2-resource
  mapping** (which performance need → LUT RAM / PSRAM / CORDIC / streamer — Architect's Guide Act III
  P-7). **Do NOT harvest the Act III agentic principles** (about *using agents*, not the P2 — low KB
  value). Fuller rationale table lives in the manual's `PLANNING.md` (KB-harvest proposals).

---

## Open — TRACKED in the ingestion head (resolution lives there, not in a YAML edit)

- **F-123 — TAQOZ-Forth / ROM-Monitor capability detail rests partly on preliminary web research.** Grounding plan in `engineering/ingestion/sources/taqoz/taqoz-content-gaps-and-grounding-plan.md` (mine `ROM_Booter.lst`; verify vs Peter Jakacki's `TAQOZ.spin2`).

---

## P2KB YAML corrections

> **Sweep origin (2026-06-13):** surfaced while auditing the Debug Window Manual's
> examples against the DEBUG display windows KB. Ground truth used is the **v55 Spin2
> documentation primary source** (`engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt`,
> the per-window directive tables at lines ~1118–1417), which revealed the v1.8.0/v1.9.0
> reconciled `debug-displays/*.yaml` carry several errors/omissions vs that source. All
> findings below are CONFIRMED against the v55 primary source. The manual was, in several
> cases, MORE correct than the YAML.

> **✅ AUTHORITY CORRECTION — RESOLVED (2026-06-14).** The findings below were originally
> derived using the v55 **published documentation text** as authority. That was the wrong
> order: the **Pascal source** (`DebugDisplayUnit.pas`) is ground truth, and the
> `DEBUG-WINDOW-DIRECTIVE-MATRIX.md` (+ per-window theory-of-operations docs) are
> Pascal-derived — the published text is the derivative that carries the off-by-ones. The
> matrix + theory-of-operations were **re-audited against the Pascal source and re-imported**
> (2026-06-14, `REF/` under `p2-debug-window-manual`). The full analysis was **rerun against
> the matrix as authority** and the findings applied/closed below. Net outcome: in the
> majority case the matrix was right and the YAML already matched it (→ `RESOLVED-INVALID`);
> a smaller set were genuine defects (→ `DONE`); and three NEW writing-debug-statement defects
> surfaced during the rerun (F-132/F-133/F-134, all `DONE`). Every changed example was
> compile-verified with `pnut-ts -d`.

### F-207 — packed-data feed for **scrolling** LOGIC/SCOPE windows requires a **full-window array feed** (`` `uhex_long_array_ ``); a single `` `(packed) `` long does NOT fill the window — `PARTIAL — manual DONE + HW-verified · KB DONE (v1.15.0) · one manual design decision open`

> **Heading corrected in place 2026-08-15.** It read *"KB enrichment pending"* while this entry's own
> body recorded **"KB APPLIED 2026-07-11 — PUBLISHED in KB v1.15.0. Both facets landed."** Verified
> against the YAML rather than the note: `language/spin2/debug-displays/logic.yaml` carries the
> array-feed example **and** the sub-sample-width = channel-count rule; `scope.yaml` carries the
> array feed; `language/spin2/statements/debug.yaml` carries the cross-referencing example. **No KB
> work is owed — do not re-file this as a YAML item.**
>
> **What is actually still open, and it is manual-head:** whether `ch13-packed-logic-stream` becomes
> the richer **2-channel + `LONGS_2BIT`** demo. Today's single-channel `'D0'` + `LONGS_1BIT` version
> is internally consistent and hardware-confirmed, so nothing is broken; adopting the richer form
> costs one more render. **Stephen's design call.**
>
> **Ordering caveat worth carrying:** this entry's own "verify first" note says Facet B (the
> mode↔channel-count rule) was a **peer report, not our own hardware run**, and directs us to confirm
> on silicon *before* enriching the KB — but the KB enrichment shipped in v1.15.0 regardless, so that
> order was inverted. The 2-channel render above **is** the confirming run. Until it happens, Facet B
> in the KB rests on a peer report plus how LOGIC is documented to unpack, not on our own bench.

**Surfaced:** 2026-07-11, fleet-release sweep — two published Debug Window Manual ch13 examples rendered only a fragment. **Root cause hardware-verified** the same day (Stephen ran the reshaped figure-generators; Claire read the BMPs back via image-tools).

**What's wrong (empirical ground truth):** for the **scrolling time-series** windows (LOGIC, SCOPE), feeding packed sample data as a **single** `` `(packed) `` long per message renders only a fragment — it does **not** accumulate/unpack across the window. The **only** feed that fills the window is the **full-window array feed** `` `uhex_long_array_(@buff, N) ``, which is also the **only packed example the v55/v51 docs ever show** (v55 text line ~1144 / v51 line ~1858, identical). The BITMAP (frame-buffer) window **tolerates** a per-long packed feed — which is why `ch13-packed-bitmap-frame` was always correct and was left untouched; that isolates the defect to the **feed shape for scrolling windows**, not the packing mechanism itself.
- **Pre-fix measurements:** LOGIC — data only in the last long's band (right-edge fragment). SCOPE — data only in the first few bands (left-edge fragment).
- **Post-fix hardware renders (2026-07-11 19:00, `fig-13-*_WDW.bmp`):** LOGIC = **full-width** random D0 trace (left edge, blank pre-fix, now packed with transitions); SCOPE = **two 0–255 sawtooths** (A + B), full vertical sweep. Both fixes empirically confirmed.
- SCOPE also had a 2nd defect: channel-defs lacked the **required** range → fixed to `'A' 0 255 'B' 0 255` (per the `'label' AUTO|lo hi` rule, F-137/EF-003 lineage).

**Manual — DONE (this sweep, HW-confirmed).** Fixed lockstep in opus-master `ch13-packed-data.md` + examples-library + figure-generators (byte-identical example↔code-block; corpus identity GREEN 32/32; compile clean `pnut-ts -d`): logic → `VAR buff[8]` (8 longs = 256 samples) fed via `` `uhex_long_array_(@buff, 8) ``; scope → `VAR buff[128]` array feed + the `'A' 0 255 'B' 0 255` ranges; prose gained an array-feed paragraph.

**Facet B — packing mode must match the LOGIC channel count (user-reported + HW-CONFIRMED 2026-07-11).** Stephen, exercising the *shipped* ZIP, found the (old) `packed-logic-stream` example declared **two** channels but used **LONGS_1BIT** → **all samples drew on the first channel only**; changing it to **LONGS_2BIT** made both channels display. The rule (grounded in how LOGIC unpacks): for LOGIC the packing mode's **bits-per-sub-sample must equal the channel count** — `LONGS_1BIT` = 1 channel, `LONGS_2BIT` = 2, `LONGS_4BIT` = 4, `LONGS_8BIT` = 8; each sub-sample carries one bit **per channel** per time-step. (SCOPE differs: an 8-bit-packed SCOPE sub-sample is a full per-channel *value*, and channels interleave across consecutive sub-samples — cf. `ch13-packed-scope` = 2 channels A/B via `LONGS_8BIT`.) Our reshaped `ch13-packed-logic-stream` currently sidesteps this by using a **single** channel `'D0'` + `LONGS_1BIT` (consistent, HW-confirmed) — the shipped bug cannot recur in it — but the richer, on-intent demo is 2 channels + `LONGS_2BIT` (design decision open with Stephen; would need one more render).

**KB — enrichment pending (the class-wide/systemic angle → yaml head).** The shipped KB documents the packing **modes** (`debug-displays/logic.yaml:37`, `scope.yaml:39`) and the concept ("packed-data modes let you pack multiple sub-samples", `logic.yaml:88`), and `statements/debug.yaml` shows the normal per-sample feed — but **no KB file shows the packed full-window feed**, states the single-`` `(packed) ``-long-won't-fill-a-scrolling-window fact, **or ties the packing mode to the channel count** (`logic.yaml:38` only covers the multi-bit-*bus* `count` field, not mode↔channel-count). A remote agent generating packed LOGIC/SCOPE code from the KB would reproduce both the fragment defect and the all-on-channel-0 defect.

**Proposed KB action:** (1) add a **packed full-window array-feed example** to `debug-displays/logic.yaml` and `debug-displays/scope.yaml` (and the packed-mode note in `statements/debug.yaml`) — `` `uhex_long_array_(@buff, N) `` matching v55's only packed example — plus the caveat: *a single packed-long feed advances the scrolling window by one column only; the full window requires the array feed* (BITMAP is exempt). (2) Document the **mode↔channel-count** rule in `logic.yaml` (LONGS_NBIT ⇒ N one-bit channels) and the SCOPE value-interleave form in `scope.yaml`.

> **KB APPLIED 2026-07-11 — PUBLISHED in KB v1.15.0.** Both facets landed. `logic.yaml` — `packed:` gains the
> sub-sample-width = channel-count rule (Facet B) + a new LONGS_2BIT full-window array-feed example
> and an array-feed/unpack note (Facet A, unpack semantics quoted from v55 L1143/L1406). `scope.yaml`
> — `packed:` gains the per-channel-value interleave form (Facet B) + a LONGS_8BIT array-feed example
> and left-edge-fragment caveat (Facet A). `statements/debug.yaml` — a packed scrolling-window
> array-feed example cross-referencing both. D2 (Stephen): essential feed-shape snippet, NOT the
> verbatim v55 streamer example (incidental + misleading re streamer-required); unpack semantics
> quoted verbatim.

**Verify first (at fix time, §4.5):** open v55 text line ~1144 (and the REF Pascal-derived matrix / `DebugDisplayUnit.pas SetPack`) and match wording exactly — do not paraphrase. Facet A's feed-shape claim is grounded in the 2026-07-11 hardware renders + v55 showing only the array form. **Facet B is a peer report (Stephen), not yet our own hardware run — confirm on silicon before enriching the KB** (empirical > documentary); the LONGS_2BIT 2-channel render, if we adopt that example, IS that confirmation.

### F-208 — PLOT POLAR orientation (θ=0 baseline direction) is undocumented; the rotation-sense wording is murky/likely-wrong — `CONFIRMED` (Test J)

**Surfaced:** 2026-07-11 — Test J had to be run to *learn* the POLAR orientation because it is documented nowhere. Per the **test-to-learn = doc/KB gap** rule (Stephen's call this date), the learned fact must be written back into both the KB and the manual, not consumed once.

**What's wrong / missing:**
- **θ=0 baseline direction is documented NOWHERE** — neither `debug-displays/plot.yaml` nor ch05-plot.md states where angle 0 points. Test J resolved it: **θ=0 → East (+x); increasing θ is counter-clockwise** (math convention); no flip.
- **Rotation-sense wording is murky/likely-wrong:** `plot.yaml:62` — *"twopi -1/0 select clockwise/counter-clockwise sense."* The default `twopi` is `$1_0000_0000` (positive → CCW), **not** 0; and the "-1/0" shorthand fails to convey the actual rule — a **negative** `twopi` reverses to clockwise.

**Evidence:** Test J (`conflict-testJ-polar-theta0`, both platforms 2026-07-11): sampling ρ≈150 from origin — **East=RED (0°)**, North/up=GREEN (90°), West=BLUE (180°), South=YELLOW (270°) → θ=0 East, CCW. Recorded in `audit/v55-vs-REF-reconciliation-2026-07-10.md`; EF entry pending (§7.6 / #196).

**Proposed correction (KB → yaml head):** in `plot.yaml` POLAR directive, state that **θ=0 points East (+x)**; the default (positive `twopi`) sense is **counter-clockwise**; a **negative `twopi` reverses to clockwise**. Replace the `"twopi -1/0"` shorthand with that sign-based rule.

> **YAML APPLIED 2026-07-11 — PUBLISHED in KB v1.15.0.** `plot.yaml:62` POLAR now reads "*Orientation:
> theta=0 points East (+x); with the default (positive) twopi the angle increases counter-clockwise;
> a NEGATIVE twopi reverses the sweep to clockwise*" — the murky `"twopi -1/0"` shorthand is gone.
> Manual side already applied (#195). Grounded EF-032/Test J.

**Manual side (→ ch05-post #195-C):** add the same orientation fact to the ch05-plot.md POLAR section — re-scoped from "optional enhancement" to **required gap-fill**.

**Grounding:** Test J (empirical > documentary). Cite the EF once promoted.

## YAML additions & enrichments (gaps) — G-001…G-005

> **Surfaced by the Titus rev5 cross-source Q&A + IOSP cross-audit (2026-06-12/13).** These are **additions** (content the KB does not yet carry), not corrections — filed here so the v1.10.1 sweep executes them alongside the F-corrections. G-001 was previously named only in the head dashboards; now formally logged. Per-item gating noted; the gated parts do **not** block the rest.

### G-004 — `architecture/smart-pins/smart-pin-11011-usb-host-device.yaml` X/Y/Z registers were one-line stubs — `DONE (2026-08-16)`

> **APPLIED 2026-08-16 («#218»).** The `open_questions:` block (`:60-64`) is deleted and replaced by
> a single `electrical_characteristics:` routing line: the J/K/SE0/SE1 detector thresholds are
> datasheet territory, and the programming interface above is complete. A *routing* statement, not
> an *unknown* statement — which is the whole distinction this entry turned on. Verified by re-read:
> `deliverables/ai/P2/` now contains **no** `open_questions:` block. Closes G-004 in full.

> **Rewritten in place 2026-08-15. There is nothing Chip-gated here, and there never really was**
> (Stephen, 2026-08-15). The "gated remainder" was *receiver analog front-end detail and the exact
> electrical thresholds of the J/K/SE0/SE1 line-state detectors.* Those are **electrical
> characteristics, not programming facts** — out of scope for this KB. A programmer using the USB
> smart-pin mode sets baud / host-device / FS-LS, sends line states, and reads the 16-bit status
> word, all of which shipped 2026-06-20. Anyone needing a comparator threshold wants the datasheet,
> not us. So the content is complete and this is no longer PARTIAL on any gate.
>
> **What IS owed, and it is a defect rather than a gap:** the file ships an `open_questions:` block
> (`:60-64`) announcing what we do not know. In an **agent-consumed** deliverable that is a hedge in
> the one place hedges are unusable — an agent cannot act on it, it reads as a gap in the *P2* rather
> than in *our sourcing*, and it invites a later fill-in from inference. A class-wide sweep found it
> is the **only** such block in `deliverables/ai/P2/`, so it is an outlier, not a convention.
> **Correction:** delete the block; if anything replaces it, a one-line pointer that electrical
> characteristics live in the datasheet — a *routing* statement, which is legitimate, rather than an
> *unknown* statement, which is not. Rides this sprint's YAML patch release.
>
> **Note the precedent one entry below.** G-005 sat "OPEN pending hardware" while the hardware answer
> had been on the ledger since 2026-06-17. Both entries were stale rather than blocked, and the
> 2026-06-20 archival deferral was conditioned on exactly these two.
> **APPLIED 2026-06-20 (provable part):** replaced the one-line X/Y/Z stubs with the full Silicon-confirmable register layer — WXPIN config word (D[15] host/device, D[14] FS/LS, D[13:0] baud = 16-bit sysclk fraction, two MSBs 0), WYPIN line-state D-values (0=IDLE, 1=SE0, 2=K, 3=J, 4=EOP, $80=SOP) + packet-send protocol, the 16-bit RX status word (all 10 documented bit-fields), and per-pin IN semantics (odd/DP = TX-buffer-empty; even/DM = RX-status-change; C = RX error). All WXPIN/WYPIN/RDPIN issued on the lower/even pin. Authority: Silicon `p2-documentation.txt:8886-9006` (verbatim). **STILL OPEN (Chip-gated):** logged an in-file `open_questions:` block — RX analog front-end / line-state detector thresholds / any scope-style filter taps are NOT in Silicon and remain in the expert queue. This finding stays PARTIAL.
- The USB-host/device mode carries no register detail. **Add the Silicon-Doc-confirmable layer now:** WXPIN config word (D[15]=host/device, D[14]=FS/LS, D[13:0]=baud), WYPIN line-state D-values (0=IDLE…$80=SOP), RX 16-bit status word, per-pin IN semantics (odd/DP = TX-buffer-empty, even/DM = RX-status-change). **Authority:** Silicon `p2-documentation.txt:8886–8960`. **Gated remainder:** any figure not in Silicon (e.g. scope-style filter taps) stays in the expert queue (Chip). (IOSP RA-38/40/42/43/46/47.)

## Systematic `P_*` constant-name audit (2026-07-01) — F-177…F-183

> **Origin & method (Stephen's call).** After F-174/175/176 kept surfacing fictitious `P_*`
> constants ad-hoc, we ran a **corpus-wide audit** to make it the last time. Method: the
> **legality arbiter is `pnut-ts` v1.55** (our authority order: compiler → v55 doc → Silicon);
> the **v55 Spin2 manual is the enumeration**. Extracted every unique `P_[A-Z0-9_]+` token in
> `deliverables/ai/P2/` (115) and compile-tested each. **Result: after the fixes below, the
> YAMLs contain ONLY legal v55 constant names** — `Y-legal \ L` is empty (no legal-but-nonstandard
> names), and all 8 fictitious names are gone corpus-wide. Also ran the **Opus-Master propagation**:
> the manuals are clean in body (they'd already removed these — see F-176 vindication). Two
> non-blocking findings remain: **F-182** (coverage gap) and **F-183** (donor staleness).

### F-183 — count-mode *concise donors* (10100/10101/10110/10111) are broadly stale/divergent from published — `TRACKED → ingestion`
> Carved from F-176. The 4 donors carry undefined **mode-name** constants (`P_PERIODS_STATES`, `P_PERIODS_CLOCKS_TIME/STATES/PERIODS`) **and** a different mode taxonomy than the (hand-corrected) published files, on top of the now-removed `P_B_A_INPUT`. Published diverged from them long ago (proving the concise-YAML pipeline isn't re-run for these), so reseed-risk is currently latent. A **full donor↔published resync** (mode names + taxonomy) belongs to the ingestion/smart-pins-catalog head, not a published-YAML edit. Tracked, not release-blocking.

## ADC gain-mode input ranges framed ground-referenced, not centered on VIO/2 (2026-07-07) — F-202

### F-202 — IOSP §16.2 ADC input-mode table (and 5 propagated sites) frame the gain ranges as ground-referenced `0V–ceiling` — `PARTIALLY CONFIRMED: GIO/VIO-as-calibration + mid-supply bias grounded in Silicon Doc; exact centered endpoints UNVERIFIED (no trusted numeric source) → hardware campaign required`
> **Source of report:** community reviewer (2026-07-07, relayed by Stephen): *"the ranges are totally
> wrong… they are centred around 1.65V."* Community-tier input (Titus-tier): challenges our work, is not
> itself a citable source.
> **TRUST-CHAIN DISCIPLINE (Stephen, 2026-07-07):** the **P2AN\*** app notes are derived from the SAME
> ingested sources as the manuals — a **peer derivation, NOT an authority**. Do not justify manual content
> against P2AN001/§16.3; ground only against trusted **ingested** sources (Silicon Doc) or **empirical**
> hardware (EF ledger). This finding was re-grounded on that basis.
> **What the Silicon Doc (trusted ingested) DOES ground:**
> - **GIO/VIO are calibration sources, not input-range modes** — *"Delta-sigma ADC with 5 ranges, 2
>   **sources**, and **VIO/GIO calibration**."* The §16.2 table mislabels them as ranges (`GIO = 0V–3.3V`,
>   `VIO = VIO-relative`). WRONG per a trusted source.
> - **The ADC has a ~mid-supply bias point** — Rev C note: FLOAT mode "useful for determining the
>   **floating bias point of the ADC**." So the gain window sits around mid-supply, **not up from 0 V** —
>   the table's ground-referenced framing is wrong.
> - Tell-tale of how it happened: the table's ceilings (`1.04V / 330mV / 104mV / 33mV`) equal `3.3V ÷ gain`
>   — correct range **widths** placed at `[0, width]` (generic unipolar-PGA assumption) instead of around
>   the mid-supply bias. (§16.7 L469 and §16.3 already describe the bias/references correctly — but those
>   are peer manual sections, cited here only as internal-inconsistency evidence, not as authority.)
> **RESOLUTION — nominal transfer characteristic (releasable-correct without hardware):**
> The exact endpoints are a **nominal / definitional** quantity, not a measured one: the mid-supply
> reference is grounded (Silicon Doc float-bias-point) and the gain factors are grounded (Silicon Doc
> "5 ranges" + image catalog), so the window `= 1.65 V ± (1.65 V / gain)` about mid-supply is **DERIVED**
> (like the Ohm's-law drive currents and `clkfreq/2³²` NCO resolution we already print), NOT AT_RISK —
> **provided it is labelled *nominal* and carries the calibration caveat** (exact endpoints vary with device
> tolerance + VIO; for absolute work calibrate against GIO/VIO, §16.3). This mirrors the manual's already-correct
> nominal-vs-measured handling of resolution ([[F-201]]). This is the distinction I initially over-collapsed:
> a *measured precision spec* needs silicon; the *nominal transfer characteristic* does not. So §16.2 prints the
> nominal windows (labelled) — correct, complete, hardware-independent.
> **Verification split (per VERIFICATION-OPPORTUNITIES.md):**
> - **VO-J-001 (jumper-only — we do it):** on-chip DAC → jumper → ADC pin sweep confirms the centering + √10
>   window scaling on silicon (upgrades nominal → silicon-confirmed). Task #172. NOT a release blocker.
> - **VO-X-001 (external-hardware — cataloged, not committed):** calibrated external reference + precision meter
>   for tolerance-bounded absolute endpoints. Benefit: nominal → datasheet-grade. Deferred.
> **Propagated sites (all same root), IOSP opus-master `part-3-input-modes/chapter-16-adc.md` unless noted:**
> §16.2 table (L39–46) · §16.2 prose (L50–60) · §16.2 example "0-100mV sensor → 30x" (L64–66) ·
> §16.7 Example 4 thermocouple "0-50mV → 100x" (L505–517) · §16.7 quick-ref table (L636–640) ·
> `part-5-appendices/appendix-d-mode-comparison-charts.md` (L195–198). The **examples are the worst**:
> they feed a ground-referenced small-signal sensor (0-100 mV, 0-50 mV thermocouple, mic, strain gauge)
> into a 1.65 V-centered gain mode with **no mid-rail bias network** — they would not work as written.
> **NOT affected (checked, don't over-correct):** §16.3 ratiometric (correct) · §16.7 float note L469
> (correct) · **DAC ranges ch10** `0–3.3V`/`0–2.0V` (correct — DAC is genuinely unipolar 0-to-Vfs,
> matches Silicon Doc drive-level table). Defect is **specific to ADC gain modes**.
> **Secondary check:** `architecture/smart-pins/smart-pin-11000-adc-internal-clock.yaml` L144–145 calls
> GIO/VIO "Ground-referenced input / VIO-referenced input" — loose (they're calibration references);
> tighten wording, and confirm no range claim depends on the ground-referenced framing.
> **SILICON-CONFIRMED 2026-07-07 (EF-024) — supersedes the nominal formula.** VO-J-001 ran on real P2:
> gain modes ARE centered on mid-supply (~1.64 V measured) [structural, definitive], but the **derived
> `1.65 ± 1.65/gain` (3.3 V/gain width) was WRONG** — measured widths are ~1.4× wider (≈4.55 V/gain), √10-laddered.
> Measured representative windows (N=1): 3.16× 0.93–2.36 V · 10× 1.41–1.87 V · 31.6× 1.57–1.71 V · 100× 1.61–1.66 V.
> **Fold into IOSP v1.0.4** (staged): (a) GIO/VIO reclassified [APPLIED]; (b) mid-supply framing + examples
> fixed [APPLIED]; (c) **print the MEASURED windows** (table above) across §16.2 + Appendix B + Appendix C,
> labelled *measured on real P2 silicon, representative single-sample* (per the citation convention), NOT the
> derived formula; rebuild the two examples on the measured centering [PENDING apply]. With (c), F-202 is
> **CLOSED for release** and now hardware-grounded (not merely derived). VO-X-001 (absolute tolerance across
> parts) remains the optional datasheet-grade upgrade.

---

## Quantitative hardware-table audit batch (2026-07-07) — F-203

### F-203 — 4-manual fan-out audit of quantitative hardware tables vs trusted ingested sources — `14 CONFIRMED_WRONG (hand-verified) + 8 AT_RISK; fixes in progress`
> **Method:** 9-unit fan-out (IOSP ×5 parts, Streamer, Debug ×2, deSilva) enumerating every quantitative/encoding
> table cell, each classified GROUNDED/DERIVED/AT_RISK/WRONG against **ingested sources only** (Silicon Doc,
> Spin2 v55, P2 datasheet), then adversarially verified. Full verdicts: workflow `wx8vrj00a` output. 1 false
> alarm rejected on hand-verify (ch06 "30mA" — actually GROUNDED, spin2-v55:1502).
>
> **CONFIRMED_WRONG — IOSP (fold into v1.0.4):**
> - `ch02` `P_HIGH_FAST`/`P_LOW_FAST` drive impedance **`~100Ω` → `~17Ω`** (datasheet Vol 510mV@30mA ⇒ ~17Ω; 30mA is correct). **FIXED.**
> - `ch18` §18.6 Hub RAM **`8-15 clocks` → `9-16 clocks`** (datasheet RDLONG `9...16`). **FIXED.**
> - `appendix-b` + `appendix-c` (table **and** the `input_max = 3300mV/gain` formula) — **F-202 ADC-range recurrence** (2 more sites; ground-referenced `0-Xmv`). PENDING (rides the F-202 nominal-table fix across §16.2 + both appendices).
>
> **CONFIRMED_WRONG — deSilva (fold into v3.0.2):**
> - SETSE Event-Modes `%000` **"Never (disabled)" → "LUT read/write & hub-lock events"** (silicon-doc part3-interrupts:48-53). **FIXED.**
> - `EVENT_INT %0000` **"Pin matches interrupt configuration" → "An interrupt occurred"** (part2-video-output:360; pin-match is `EVENT_PAT %1000`). **FIXED.**
> - `EVENT_QMT %1111` **"CORDIC/PIX math complete" → "read with no CORDIC result available"** (part2-video-output:375 — the inverse meaning). **FIXED.**
>
> **CONFIRMED_WRONG — Streamer (needs own patch, NOT in current wave):**
> - §12.2 Sub-Pin Selection table treats `D[19:17]` as a uniform 3-bit selector for 1/2/4-pin; silicon encodes `pppa/pp?a/p??a` (pin-bits shrink 3/2/1; freed low bits = DAC sub-mode). 1-pin col correct; 2/4-pin cols wrong. (p2-documentation:3004-3009).
>
> **CONFIRMED_WRONG — Debug (needs own patch, NOT in current wave):**
> - `ch05` PLOT TEXTSTYLE **horizontal align 2/3 swapped** (source %10=right, %11=left) and **vertical align 2/3 swapped** (%10=bottom, %11=top) — spin2-v55:1282; plus downstream prose **"`$20` left-aligns" → right-aligns**.
> - `ch03` TERM **`TEXTSIZE` default `10` → "editor text size"** (spin2-v55:1305; the 10 is the PLOT default).
>
> **AT_RISK (unsourced specifics — disposition per finding):** IOSP `ch16` §16.8 ADC "input impedance ~500kΩ" + "absolute-error floor ~15mV" (from P2AN001, not in EF ledger — **jumper-only verifiable, VO-J candidate**); `ch10` DAC "Max Load >10kΩ…" (10× rule-of-thumb heuristic); `ch12` "input buffer ~2ns" (sub-component; 3-clk total IS grounded); `ch07` "180MHz rated / 250 overclock" (only 350 grounded; 180 cites external datasheet); Debug `ch05` weight "100/400/700/900" (OpenType nums unsourced; "thin"→"light"); Debug `ch14` "LOCK[15]" + "~10,000 msg/s" (tool/throughput, ungrounded). Disposition: remove the unsourced number or soften to qualitative; the ~15mV/~500kΩ ADC pair → VO-J jumper test.

## XBYTE technique-mining sweep — reference implementations expose two doc defects (2026-07-14) — F-217, F-218

> **Origin.** Stephen asked for a per-processor "what will hurt when you emulate this" table in the XBYTE
> Guide, and proposed we ground it by studying **live, working emulators** rather than reasoning from ISA
> facts. The study immediately surfaced two defects. Full evidence ledger:
> `engineering/document-production/manuals/p2-xbyte-programming-guide/TECHNIQUE-MINING.md`
> (per-source, because the techniques enter the manual body *anonymously* — the ledger is the only place
> the lineage lives). **Note the path:** it lives at the manual **root**, not in `audit/`, because
> `.gitignore:175` ignores `manuals/*/audit/` — a durable source-of-record cannot live there.

### F-218 — `SingleStep-Debugger-Theory-of-Operations.md` §6.4 mislabels `GETBRK` D[25] as "C,Z affected by XBYTE" — `NEEDS-VERIFICATION`

**Our own ingested doc says:**

> *"Displayed as 3 hex digits. A checkmark glyph appears if **bit 25** of `mBRKC` is set (**C,Z affected by
> XBYTE**)."*

**The Silicon Doc says otherwise.** Per P2KB `p2kbPasm2Getbrk`, `GETBRK D WC` returns:

| Field | Meaning (Silicon Doc) |
|---|---|
| D[27] | 1 = SKIP · 0 = SKIPF/EXECF/XBYTE |
| D[26] | LUT sharing enabled |
| **D[25]** | **XBYTE pending on next `_RET_`/`RET`** |
| D[24:16] | the 9-bit XBYTE mode |

"C,Z affected by XBYTE" is the **F bit**, which is the *low bit of the mode operand* — i.e. **D[16]**, not
D[25]. The two are different facts about different bits, and our doc appears to have conflated them.

- **NOT SETTLED, and deliberately not fixed.** The checkmark's meaning is decided by the **host-side**
  display code (PNut / term-ts), not by Chip's P2-side debug stub — `Spin2_debugger.spin2` only calls
  `getbrk` and ships the word to the host. So the P2-side source **cannot** adjudicate this. Settling it
  needs the host display source or Chip.
- **Two possible truths:** (i) our gloss is simply wrong and D[25] means "XBYTE pending"; or (ii) the
  debugger's checkmark genuinely reflects the F bit and our doc attributed it to the wrong bit index. Either
  way **the doc as written is wrong**; only the repair differs.
- **Consumer risk:** the XBYTE Guide is about to gain a "Debugging XBYTE" section citing `GETBRK` fields.
  It will cite **the Silicon Doc layout**, not this doc, until this is resolved.
- **Wider lesson (already a standing rule, freshly demonstrated):** our own ingested derivations are **peer
  tier, not authority**. This was caught only because the field layout was cross-checked against P2KB
  instead of being trusted.

## `architecture/xbyte_engine.yaml` — all three programming examples are broken (2026-07-14) — F-220…F-223

> **Origin.** Chasing an open question for the XBYTE Guide (*what does Chip's "no stack pop" mean?*), the
> authoritative KB entry `p2kbArchXbyteEngine` was consulted — and **every one of its three
> `programming_examples` is wrong.** This is the YAML an agent would use to generate XBYTE code.
> Ground truth used below: the **Silicon Doc** narrative + demo, **Chip's own Spin2 interpreter**,
> **Parallax's official `xbyte.spin2`**, plus Zog and the 8080 emulator — nine implementations, all
> agreeing. Evidence: `manuals/p2-xbyte-programming-guide/TECHNIQUE-MINING.md`.
>
> **File:** `deliverables/ai/P2/architecture/xbyte_engine.yaml`

### F-224 — Assembly Manual: the CORDIC interrupt hazard is documented on the `REP` page, but **not on the CORDIC pages** — `CONFIRMED` (low severity, cross-reference gap)

**Raised by F-217's class-wide sweep.** Having found that the XBYTE Guide sold interruptibility as a
pure benefit, the same question was asked of every other manual: *does anything show a CORDIC
issue/collect pair without telling the reader it must be fenced?*

**The Assembly Manual is NOT wrong.** `part-ii/instructions-r.md` teaches the fence properly, and even
uses a CORDIC example:

> `' Protect CORDIC operation from interrupts` … `qmul  y, x`

and states the mechanism outright: *"Interrupts are blocked during REP execution — including debug
interrupts that ordinary masking cannot hold off — to maintain timing precision and keep the repeated
block atomic."* It also carries the useful nuance that the idiom *"is only needed in PASM2 code with
interrupts enabled; Spin2 operators are already protected by the interpreter."*

**But the warning is not where the affected reader is standing:**

| Page | Content | Interrupt mentions |
|---|---|---|
| `instructions-q.md` | **QMUL · QROTATE · QDIV** — the CORDIC **issue** ops | **0** |
| `instructions-g.md` | **GETQX · GETQY** — the CORDIC **collect** ops | 3 — **all from GETBRK**, none about CORDIC |
| `instructions-r.md` | REP | ✅ the fence, with a CORDIC example |

A reader who looks up `QMUL` — which is exactly what someone about to *write* a CORDIC sequence does —
learns nothing about the hazard. They find it only by happening to read the `REP` page.

- **Severity: low.** This is an omission at the point of need, not a false claim. Same *class* as F-217,
  milder in kind: the information exists in the manual.
- **Fix (small):** a cross-reference note on the CORDIC issue/collect pages — "a CORDIC command and its
  result must not be split by an interrupt; see REP" — costing a few lines, no content change elsewhere.
- **Release consideration for Stephen:** the Assembly Manual shipped **v3.1.4 on 2026-07-14** (a
  render-only patch). This is a *content* change and would need its own bump. It is a documentation
  improvement, not a correctness bug in the shipped text, so it can ride the manual's next natural
  release rather than forcing one.

**RESOLVED 2026-08-17 («#235» wave prep).** Confirmed still open first — `instructions-q.md` had
**zero** interrupt mentions, and `instructions-g.md`'s three were all GETBRK. The rule now opens the
**Q instruction section** (where a reader looking up QMUL or QROTATE lands) and the **CORDIC
Coprocessor category** (which reaches GETQX/GETQY too), both pointing at REP for the pattern and both
noting Spin2 needs no fence. Plain reference prose, not `{.warningbox}` — that convention is reserved
for silicon bugs, and this is a programming hazard. **Rides v3.1.6**, which was otherwise the one wave
element with no prose change, so it costs nothing to carry.

**Also observed (not a defect):** 22 stray `*.backup-encoding-conversion` files sit in
`p2-assembly-language-manual/opus-master/part-ii/`. They are **untracked** — `git ls-files` returns
zero — so nothing ships and no glob in the assemble scripts reaches them (those use explicit
`REQUIRED_FILES[]`). Working-tree clutter only; worth sweeping, not a release concern.

## Interactive DEBUG examples never ran — `PC_KEY`/`PC_MOUSE` shipped without their escape backtick (2026-07-26) — F-227

## Forum docs-feedback sweep (2026-08-14) — F-254…F-258

**Origin:** Parallax forum posts #104–#117 (2026-08-12/13), reviewing the deSilva tutorial, the
XBYTE Programming Guide, and the P2 Architect's Guide. Full analysis (with the tone/positioning
items that are *not* defects) lives at
`engineering/document-production/FORUM-NO-COMMMIT/Docs-findings-360813/DOCS-FINDINGS-ANALYSIS.md`
(gitignored — find it by path). Forum posts are the **lead**; every finding below was verified
against the live opus-master, `pnut-ts` 1.55.3, or P2KB before filing.

### F-256 — `_RET_ CALL` never returns, because `_RET_` returns only if the instruction did not branch. A DOCUMENTATION defect, not a hardware one. `RESOLVED — root cause is F-273; KB applied, manual restructure applied 2026-08-16 («#227»)`

**Location:** `xbyte-body.md:879` (*"Chapter 15's `_RET_ CALL #set_nz` idiom depends entirely on
this"*), used at `:1391`, `:1400`, `:416`, `:793`.

Christof (#110) doubted *"you can combine a CALL with ret."* **Tested: `_ret_ call #set_nz`
assembles clean under `pnut-ts` 1.55.3**, and `language/pasm2/call.yaml:11` describes CALL paired
"with a `_RET_` condition" — so as stated the objection is wrong.

**But the compiler proves legality, not semantics.** The open question is what the hardware does
when one instruction both pushes a return address and returns: does control reach the helper and
then return to `$1FF` (XBYTE re-entry intact), or does the push/pop ordering break dispatch?
`architecture/xbyte_engine.yaml:71` is suggestive but addresses a *different* case (why a CALL
cannot substitute for `PUSH #$1FF` at arm time). **Not resolvable from the KB or the Silicon Doc;
no answer is asserted here.**

> **ANSWERED — AND THE ANSWER WAS IN THE INGESTED SOURCES ALL ALONG. See F-273.**
> This was never a hardware question. **`_RET_` executes the instruction and returns *only if that
> instruction did not branch*** — stated by *two* independent Parallax primary sources (Assembly
> Language Manual 2022-11-01, condition table p.68; P2 Instructions v35 Rev B/C Silicon, row 410:
> *"if `<inst>` is not branching then return by popping stack[19:0] into PC"*). `CALL` branches, so
> `_RET_ CALL` cannot return. **The behaviour is specified, not anomalous.**
>
> **The real defect is ours:** our KB documented the prefix as an unconditional *"Always + Return"*
> and the qualifier *"if no branch"* appeared **nowhere** in `deliverables/ai/P2/`. An author
> reading that writes `_RET_ CALL #set_nz` and is right to. **Root cause, KB fix and the
> alignment-check lesson are all in F-273.**
>
> **What the bench actually showed (EF-058, corrected there too):** the handler falls through into
> whatever follows it in cog RAM. In the rig that was another handler, which ran in full and whose
> own `ret` returned to `$1FF` — so **all four bytecodes dispatched and the VM finished normally.**
> The original claim *"dispatch does not resume"* is **false**. The failure mode is **silent extra
> execution**, and it is **layout-dependent**.
>
> **NO FURTHER RIG RUN IS REQUIRED.** Not for generality outside XBYTE — the prefix is architectural
> and the sources say nothing about XBYTE — and not to confirm EF-058, which can only re-observe the
> specification. The `[M-pre]` grade and the staged `DEBUG_COGS` re-run are **moot for the
> conclusion**; the conclusion now rests on documentation, with the bench as corroboration.
>
> **Applied in `xbyte-body.md` («#227», uncommitted under the «#234» gate):** every `_RET_ CALL`
> replaced by `CALL` + `RET` — §15.3's handlers and the shared `ld_imm` family, §4.4's `alu_body`,
> §5's `push_const`, §17's `voice_on` — plus the two explanations that endorsed the idiom (`:882`
> and §15.3). **That structural change stands; its EXPLANATION is being rewritten** to teach the
> documented rule rather than the mechanism previously inferred here. Slices recompile clean.

**Action:** jumper-free, single-board hardware test — arm XBYTE, run a handler ending in
`_RET_ CALL`, report whether dispatch continues. Ideal **VO-J** candidate; result goes to the EF
ledger either way. **A load-bearing idiom in a guide under community review must not stay
unverified.** If it fails, §15.3 and the Chapter 9 explanation both need rework.

## Community bench review — refaQtor, P2 Rev C @ 300 MHz (2026-08-14) — F-259…F-263

**Origin:** `p2-manuals-review-findings.md` (posted as `p2-manuals-review-findings.zip`, forum
#108), reviewing the manuals **as downloaded 2026-08-13**. Author states every claim has a
committed harness + log on **real P2 Rev C silicon at 300 MHz, pnut_ts 1.55**.

> **Trust note.** This is a *third party's* bench, not ours. It is far stronger than a forum
> opinion — reproducible rigs with logs — but it is **not** an accepted P2KB empirical finding and
> must **not** be written into `P2-EMPIRICAL-FINDINGS.md` as if it were our own test. Treat each
> claim as a **high-quality lead**: verify against our sources (done below), fix the documentation
> defect where the source proves it, and **replicate on our bench** anything we intend to cite as
> ground truth. His §5 "confirmations" are likewise corroboration, not EF entries.

**All five below are in RELEASED manuals.**

### F-284 — the 9-column encoding-table filter never escaped `&`, so two shipped instruction definitions print with the AND operator eaten by LaTeX. `CONFIRMED` — **fixed 2026-08-17; Assembly must re-render**

**Found:** 2026-08-17, verifying the six generated wave PDFs page by page. The compile log
reported **zero errors**; the defect was visible only on the page.

**Location:** `platform/filters/p2kb-platform-tables.lua` — the `cell_to_latex` helper in the
9-column instruction-encoding table handler. Visible at **P2-Assembly-Language-Manual pp.326
(TEST) and 329 (TESTN)**, sourced from `part-ii/instructions-t.md:38` and `:169`.

**Mechanism.** That handler flattens each cell with `pandoc.utils.stringify()` and emitted the
result verbatim. The near-identical 6-column handler beside it, at the same file, has always run
`text:gsub("&", "\\&")` plus `%`, `#`, `_`. So one of two adjacent code paths escaped and the
other did not. An unescaped `&` inside a `tblr` cell **is an alignment tab**: it ends the cell,
shifts every later column one to the right, and pushes the row past the table's right border —
which is what the 50.2pt overfull hbox in the log actually was.

The reader sees the TEST row's C column as `Parity of (D` and the next cell as `S)`. **The AND
operator is gone from a bit-level definition of what the instruction computes**, and the row's
remaining columns are all off by one. It has been shipping this way since at least v3.1.5.

**`%` is the worse latent case.** Through the same unescaped path it would comment out the rest
of the row — silent, complete, and with a clean log. Same class as F-281.

**Blast radius measured, not assumed:** 281 nine-column encoding tables across the manual,
scanned for `&`, `%`, `#`, `_` outside code spans. **Exactly 2 hits, both `&`, both in
`instructions-t.md`; zero `%`/`#`/`_` anywhere in that path.** The other five wave elements
contain no nine-column encoding tables and were verified unaffected. The five `&` sites elsewhere
in Assembly and deSilva all go through escaping paths and render correctly — checked in the `.tex`,
not inferred.

**Fix applied:** the 9-column helper now escapes the same four characters as its sibling. Since
`stringify()` has already flattened the cell to plain text, no intentional LaTeX can be harmed.

**Owed:** re-render `p2-assembly-language-manual` v3.1.6 and confirm pp.326/329 read
`Parity of (D & S)` and `Parity of (D & !S)` inside a 9-column row. The platform file is staged.
No version bump — v3.1.6 has not shipped.

**Lesson.** The gate that would have caught this does not exist: we check source characters and we
check compile logs, and this defect is invisible to both. It was found by rendering a page and
looking at it, prompted by triaging an overfull-hbox count. **An overfull hbox in a table is worth
opening**; it is the only signal this failure emits.

### F-286 — the escaping that stops F-284's class was per-call-site discretion, so it drifted to five more raw-emission sites. `CONFIRMED` — **fixed 2026-08-17; needs the Assembly render to validate**

**Found:** 2026-08-17, asking the process question after F-284/F-285: *what would routinely catch
these?* The answer turned out to be a structural fix rather than a checklist.

**The class.** A pandoc Lua filter that calls `stringify()` and emits the result inside a
`RawBlock` bypasses pandoc's escaping entirely. `stringify()` flattens an element to plain text,
so nothing in the result is intentional LaTeX — but `&` in a raw position IS an alignment tab, and
`%` silently comments out the rest of the line **with a clean compile log**. F-284 was one instance.

**The rule already existed, written down, with rationale — and was applied at one site in four.**
`p2kb-platform-code-coloring.lua` carried a comment stating the principle exactly ("Special LaTeX
characters in the title are re-escaped because the title text, once parsed by Pandoc, is emitted
into a raw-LaTeX block"), and its `esc()` helper was declared **inside a single `elseif` branch** —
so the sidetrack handler 100 lines below, which that very comment cites as using "the same
addcontentsline technique", emitted its title unescaped. `p2kb-platform-pagination.lua` was the same
shape: a `latex_escape()` helper at line 26, used for chapter subtitles, **not** used for the Part
title 28 lines below.

**Five unescaped raw-emission sites, all fixed:**

| Filter | Site | Raw position |
|---|---|---|
| `p2kb-platform-pagination.lua` | Part title | `\manualpart{}` |
| `p2kb-platform-figures.lua` | figure caption | `\caption{}` |
| `p2kb-platform-code-coloring.lua` | sidetrack title | `\addcontentsline{}{}{}` |
| `p2kb-platform-tables.lua` | table caption `stringify` fallback | `caption={}` outer key |
| `p2kb-platform-tables.lua` | cell renderer `pandoc.write` fallbacks (×3) | `tblr` cell |

Escaping is now a module-level helper in each filter with the invariant stated at its definition,
rather than a decision re-made at each call site. That is the actual fix: **per-call-site escaping
drifts; one shared helper is why it stops drifting.**

**Blast radius measured, not assumed — zero live exposure.** All 38 `# Part` headings and all
`figurecaption` divs across the live masters were scanned for `&` and `%`: the only hit is in a
`creation-guide.md` (not a rendered master). So the change is **inert on today's content** and the
five already-verified wave renders remain valid. The `tables.lua` cell-renderer holes are fallback
paths that fire only when `pandoc.write` fails.

**Deliberate scope limit.** `tables.lua`'s helper escapes `& % # _` — the same four its cell
renderers already escaped inline — and deliberately **not** `{ } \`, because instruction tables
legitimately carry P2 syntax like `{#}` and escaping those braces would change pages that render
correctly today. Closing a hole must not move correct output.

**Retires an authoring workaround.** Authors were told to spell "and" in Part titles because an `&`
there broke the build. That restriction was a workaround for this bug and is no longer needed.

**Owed:** the Assembly render already owed for F-285 validates all of it. Confirm p.329, and confirm
Part titles and table captions still render as before.

**The process changes that came out of this — the durable half:**
1. **`latex_escape_processor.py` now hard-fails on HTML entities in prose.** Not a warning: this
   processor escapes `&`→`\&` before pandoc runs, so `&nbsp;` becomes `\&nbsp;` and pandoc emits
   the literal text. **There is no configuration in which writing an entity here works**, which is
   why it is a gate and not advice. Verified against the real pre-fix source from git: all 32
   occurrences caught at exact line/column, and silent across all 128 live master files.
2. **`engineering/tools/validation/audit-tex-artifacts.py`** — new. Sweeps the returned `.tex` (the
   only artifact showing what LaTeX actually received) for entities, raw HTML, literal markdown,
   double-escapes, `{=latex}` leaks, `??`, TODO markers. Tuned to **zero false positives** across
   all eight outbound `.tex`; its exclusions are load-bearing and documented in the script header.
   Wired into `release-manual` as step 1e0.
3. **`release-manual` no longer says to ignore overfull hboxes.** That instruction is what let F-284
   ship: a 50.2pt overfull hbox was the defect's only signal, and the skill said to disregard it.
   Now triaged by magnitude and location (≥20pt, or any inside a table ⇒ open the page). Assembly's
   log carries 7,056 overfulls of which 36 are ≥20pt, so ranking is tractable where listing is not.
4. **`release-manual` 1d′ — read the whole page you opened.** F-285 cost nothing because it sat on
   F-284's page; a narrowly-scoped check would have passed it through again.

### F-287 — the P2AN001 companion states the ~15 mV error floor as fact; the note marks it designer-stated. `CONFIRMED` — **fixed 2026-08-17**

**Found:** 2026-08-17, acting on F-283's own scope note ("the same drift is plausible in every app
note whose doc has advanced since its companion was written"). P2AN001 was in the release flight, so
its pair was checked before shipping.

**The disagreement.** `P2AN001.md:626` is careful about provenance: *"The P2's designer reports having
seen pins read as much as 15 mV apart in absolute terms (Reference 2) — a designer-stated figure for
the pin-to-pin spread, **not a characterized specification**."* The companion's `gotchas` carried the
number flat — *"different pins can read up to ~15 mV apart in absolute terms. A hardware limit"* —
with no provenance at all.

**Why it matters more than a missing word.** An agent reading only the companion cites ~15 mV as a
specification. That is the **confidence/source mismatch** that this project treats as a trust-killer,
and it is the same failure as F-273: the qualifier is the half that goes missing, and its absence
reads as a stronger claim rather than an incomplete one. The note also names where the front-end
limits and calibration guidance live (I/O and Smart Pins User Guide §16.8); the companion did not.

**Fixed:** the `gotchas` entry now carries the designer-stated qualifier, the explicit "NOT a
characterized specification", the hardware-limit-not-noise distinction, the per-pin calibration
remedy, and the §16.8 pointer.

**Category swept, and it is otherwise clean.** All seven app-note companions were checked for OBEX
citations: P2AN001/005/006/007 carry none; P2AN002 had four wrong or incomplete (F-283); P2AN003 (4
citations) and P2AN004 (2) were verified against the live catalog and are **correct** — #2860 EZ Sound
(Jon McPhalen / jonnymac), #2831 P2_rctime (phonoclese), #2829 Quadrature Encoder (Jon McPhalen /
jonnymac), #2861 reSound. So the drift was specific to P2AN002, not systemic.

**One open question, deliberately NOT edited.** P2AN003's companion credits OBEX #2861 reSound to
**"Johannes Ahlebrand"**; the live catalog's author field reads only **"Johannes"**. The surname may
be correct from the object's own source header, and absence from the catalog field is not proof it is
wrong — so this is not treated as a defect to fix silently in a **published** note. Needs Stephen's
call: verify against the object source, or fall back to the catalog form.

### F-288 — an effect group in slash form is shaped exactly like a dual mnemonic, so 16 syntax forms print split across two lines. `CONFIRMED` — **filter fixed 2026-08-17; needs the Assembly render**

**Found:** 2026-08-17, during release verification of Assembly v3.1.6. Found by **reading the whole
of p.329** while confirming the F-285 repair — the repair itself is correct; this was the rest of the
page. (Third time in two days that the free evidence on an opened page carried the next defect.)

**Reader impact.** In the TESTB, TESTBN, TESTP and TESTPN entries — four syntax forms each, **16
lines** — the flag-effect group is orphaned onto its own line, with vertical gaps between the pairs:

```
TESTP {#}Dest          instead of      TESTP {#}Dest WC/WZ
WC/WZ                                  TESTP {#}Dest ANDC/ANDZ

TESTP {#}Dest
ANDC/ANDZ
```

In a reference manual's syntax block a form split across two lines reads as **two different forms**,
and these four instructions are exactly where a reader goes to learn which effects each accepts.

**Mechanism (code-verified, not inferred).** `workspace/p2-assembly-language-manual/filters/p2kb-pasm2-entry-format.lua`
inserts `\\` before every bold run that matches an instruction-mnemonic *shape*, one shape being
`^[A-Z][A-Z0-9_]*/[A-Z0-9_]+$` — intended for dual mnemonics like `CALL/RET`. **`WC/WZ`,
`ANDC/ANDZ`, `ORC/ORZ` and `XORC/XORZ` are character-for-character that same shape**, so each was
taken for a new mnemonic and given a break *before the effects*. The filter did try to exclude
effect flags — `not text:match("^{")` — but that only catches the **brace** form `{WC|WZ|WCZ}`,
which is precisely why TEST and TESTN, written that way, always rendered correctly while their
neighbours did not.

**Wider than the 16 visible lines.** The bare forms — `WC`, `WZ`, `WCZ`, `ANDZ`, `ORZ`, `XORZ`, nine
further sites — match the plain-CAPS shape and carried the same latent bug.

**The F-285 repair did not cause these defects — it ACTIVATED them.** (Corrects a first reading that
called it unrelated.) `is_syntax_paragraph()` rejects any paragraph containing a top-level word, and
the literal `&nbsp;` was exactly such a word — so in v3.1.5 the filter **never fired on these
paragraphs at all**, and the four tight lines came from pandoc's hard breaks alone. Removing the
entities made the paragraph parse as a syntax block for the first time, and the filter's latent bugs
took effect. The bugs predate v3.1.5; their visibility does not. Verified against the released v3.1.5
PDF recovered from git.

**A SECOND defect, found by reasoning about what the re-render would show before spending it.** Once
the effect-group breaks were fixed, the four forms would still have been separated by BLANK LINES:
the filter inserts `\\` before each mnemonic **unconditionally**, while the source already ends each
form with a trailing `\` — a markdown hard break pandoc renders as `\\`. The two compose to
`\\\\`, a blank line between every syntax form. The filter now honors an existing `LineBreak` and
supplies one only when the source lacks it — which preserves the reason the filter exists (forms
written on separate source lines with no hard break still get their break).

**Fix applied.** Shape-matching cannot separate these cases; **membership** can. A single
`is_mnemonic()` predicate now decides by membership in an explicit `EFFECT_FLAGS` set (handling the
brace, slash and bare forms), and **both** loops — the mnemonic count and the break insertion — call
it, so the two can never disagree about what a mnemonic is. Verified against the real token
inventory: `WC/WZ`/`ANDC/ANDZ`/`ORC/ORZ`/`XORC/XORZ`/`WC`/`WZ`/`WCZ` are not mnemonics, while
`CALL/RET`, `ABS`, `ADDCT1`, `MUL / MULS` still are. No PASM2 instruction is named `WC`, `ANDC`,
`ORC` or `XORC`, so there is no collision — and `WRC`/`WRZ`, which ARE instructions, are absent from
the flag set and stay mnemonics. Both copies of the filter (workspace + interactive-testing) fixed
and confirmed identical.

**Same class as F-286**, one day apart: a guard written for one shape, left to cover a family. The
countermeasure is the same — one predicate, one place, used by every caller.

**PROVEN ON THE FORGE DAEMON, not merely reviewed** (run `f288-syntax-v1`, 2026-08-17). A five-case
fixture was rendered and READ: the four slash-form `TESTP` forms print one per line with no gaps; the
`{WC|WZ|WCZ}` control is unchanged; bare `WC`/`WZ`/`WCZ` print inline; **and both no-regression cases
hold** — forms written without a hard break still receive an inserted break (the filter's actual
purpose), and `CALL/RET`, `WRC`, `WRZ` are still treated as mnemonics. Compile log clean on all five
serious signatures. This is what a Lua change with no local interpreter requires: the daemon, not a
code read.

**Owed:** one Assembly render (staged). **Assembly v3.1.6 is HELD from the release wave** until p.329
shows the four TESTP forms each on one line in the production build; deSilva, P2AN001 and P2AN002 are
unaffected (this filter is Assembly-local) and release without it.

### F-289 — the code-line gate skipped every CAPTIONED code block, so it reported clean on the manual whose pages were losing channels. `CONFIRMED` — **tool fixed 2026-08-17; all 11 IOSP sites repaired 2026-08-17, render owed**

**Found:** 2026-08-17, asking a plain status question about Debug Window and IOSP while waiting on the
Assembly render. Debug Window's code-line audit reported **clean** at K=76; measuring the same files
by hand found **29 code lines over 76 columns, the worst at 137 and 130** — both longer than any line
F-281 named. A gate that silently passes is worse than no gate: nobody goes looking.

**Mechanism.** `audit-code-line-length.py`'s `is_code_fence()` returned False for **any** fence info
string starting with `{`:

```python
# ```{=latex} / ```{=html} / ```{.foo} attribute syntax -> not a plain code box
if info.startswith('{'):
    return False
```

Only `{=format}` is a raw passthrough. Pandoc **attribute** syntax —
```` ```{.spin2 caption="ch07-scope-three-channel.spin2"} ```` — IS a code box, and it is the
**captioned** form: exactly the form paired with an `examples-library/` file under the byte-identity
rule. So the gate excluded the blocks that carry the shipped examples.

**Fleet exposure: 56 captioned blocks were never gated** — Debug Window 34, IOSP 15, Getting Started
4, deSilva 3.

**This is how F-281 shipped.** Both Debug Window lines that lose a whole channel on the page
(`ch07-scope.md:272`, 121 cols → the third SCOPE channel; `ch06-logic.md:310`, 113 cols → the third
LOGIC channel and the closing paren) sit in captioned fences. The gate declared the manual clean
while two of its pages were dropping code.

**Fixed:** skip only `{=`. The `{=latex}` exemption still holds — verified: `ch03-term.md:73` (137
cols) and `ch05-plot.md:784` (130 cols) are raw passthrough and are correctly still ignored.

**The true picture, now that the gate measures what it claimed to:**

| Manual | over K=76 | past the ~101-col render cliff |
|---|---|---|
| Debug Window (v1.1.2 released) | 24 | **3** — the F-281 trio |
| IOSP (v1.0.8 released) | 11 | **2 — NEW, and shipped** |
| deSilva · Assembly · Streamer · XBYTE · Architect · Getting Started | 0 | 0 |

**TWO SHIPPED IOSP TRUNCATIONS, verified on the released PDF by rendering the pages and looking:**

1. **p178** (`chapter-11-serial-transmit.md:433`, 103 cols) — `reversed := value REV 7` keeps its code,
   but the trailing comment runs past the code box's right border and is cut at the page edge:
   *"...for MSB-first (REV n covers bits 0.."* — the closing `n)` is gone.
2. **p163** (`chapter-10-dac-output.md:462`, 102 cols) — `WXPIN(AUDIO_PIN, …)` keeps its code; the
   comment is cut mid-word at *"a 256-clock multipl"*.

**Severity: below the F-281 SCOPE/LOGIC cases.** In both IOSP sites the CODE is intact and only a
comment tail is lost, so no reader can build a wrong program from them — but the line visibly
breaches the box border, and a truncated explanatory comment is still a reader-facing defect in a
published manual. Neither is a regression: both predate v1.0.8 (`git diff` against the tag shows the
lines unchanged).

**A first-match verification nearly missed this**, twice in one investigation: `reversed := value REV
7` appears on **p175 and p178**, and p175 (a different method, comment moved above the code) renders
perfectly. Checking only the first hit would have cleared a defect two pages later — the same trap
as F-284's `Parity of (D & S)` resolving to p414 instead of the instruction pages.

**Action:** both IOSP sites are repaired by the sanctioned comment fix (move it above the instruction,
as `spi_tx_msb_first` on p175 already does — the manual's own neighbouring example shows the form).
Rides IOSP **v1.0.9**, which is already owed a CHANGELOG entry. Debug Window's trio and its 21 other
over-budget lines ride **v1.1.3**. *(This sentence originally added "and the `breaklines` platform fix
may change what re-authoring is still needed there." It does not — `breaklines` was **REJECTED** later
the same day, see [[F-281]]. Nothing at render time rescues an over-wide line; authorship plus this
repaired gate is the whole mechanism. Corrected 2026-08-19.)*

**Done 2026-08-17 — and the scope was 11, not 2.** Repairing only the two cut sites would have left
nine lines over budget, one of them (`chapter-07-pulse-transition.md:306`, **88 cols**) past the
86-column box border and therefore already spilling into the margin — a visible defect, not a lucky
one. All 11 were brought under K=76 by the sanctioned form: standalone comment blocks rewrapped,
trailing comments moved to their own line above the instruction. Five captioned examples changed in
lockstep with their masters.

**Verified, not assumed:** code-line gate clean across all 30 IOSP masters (was 11 failures);
`verify-example-corpus-identity.py` GREEN 15/15; all five changed examples compile clean under
`pnut-ts -d`. **`pdftotext` reported the p163 comment complete while the rendered page cut it
mid-word at "multipl"** — the text object exists off-page, so extraction is not evidence of what
prints. The page image is.

**Still owed:** render v1.0.9 and confirm p163 and p178 on the page.

### F-290 — nothing continues a `debug()` directive line: the Spin2 `...` and CON symbols both compile clean and ship a different program. `CONFIRMED` — **mechanism established 2026-08-17; prepare-manual guidance corrected**

**Found:** 2026-08-17, looking for a way to bring `ch06-logic.md:310` (113 cols) under K without
losing what the example teaches. Both candidate fixes were compiled and the emitted binary inspected
rather than trusted.

**A `debug()` backtick directive is a LITERAL STRING assembled at compile time. It is not Spin2
source, so no Spin2 syntax applies inside it.** Two consequences, each verified by compiling with
`pnut-ts -d` and reading the directive text back out of the `.bin`:

| Attempt | Compiles | Bytes | What actually shipped |
|---|---|---|---|
| baseline | ✅ | 9,482 | `LOGIC SPIbus TITLE 'Software SPI' SAMPLES 200 SPACING 3 'CS' 1 $00FFFF 'CLK' 1 $00FF00 'MOSI' 1 $FFFF00` |
| Spin2 `...` continuation | ✅ | **9,438** | `LOGIC SPIbus TITLE 'Software SPI' SAMPLES 200 SPACING 3 ...` — **`...` embedded literally and ALL THREE CHANNELS DROPPED.** The window would be created with zero declared channels. |
| colors as `CON` symbols | ✅ | 9,476 | `'CS' 1 C_CS …` — **symbol names embedded verbatim, never resolved.** The PC-side `KeyColor` cannot read `C_CS`, so every channel silently falls back to `DefaultScopeColors`. |

Only the `` `(expr) `` form substitutes a value into a directive; a bare token is text.

**PROCESS DEFECT THIS EXPOSES — `prepare-manual`'s sanctioned fix is wrong for this line class.**
The code-line gate's guidance reads: *"for a **code** overflow, break at a logical boundary with the
legal Spin2 `...` line-continuation."* That is correct for ordinary Spin2 statements and **silently
destroys a `debug()` directive** — which is the majority of the over-long lines in the Debug Window
manual, i.e. exactly the population the guidance is aimed at. Corrected in the prepare-manual
project overlay.

**Same family as the trailing-`-` trap** already recorded under F-281 (compiles clean, 9,338 vs 9,408
bytes). The generalization is now explicit rather than one anecdote: **a `debug()` directive line
cannot be continued at all — it can only be shortened.** Byte-comparing the binary against the
one-line form is what catches it; the compiler never will.

**Applied to the LOGIC line (F-281, agreed with Stephen):** the create line drops `TITLE`, `SAMPLES`
and `SPACING`, reaching **70 cols** and keeping all three named channels with their exact hex colors:

```
  debug(`LOGIC SPIbus 'CS' 1 $00FFFF 'CLK' 1 $00FF00 'MOSI' 1 $FFFF00)
```

Costs nothing pedagogically — **checked, not assumed**: Chapter 6 already teaches all three dropped
keywords 250 lines earlier (a table row each at 69–72, prose deriving `SAMPLES × SPACING` = window
width at 87–89, and a prior worked example using `SAMPLES 64` at line 46). The over-long line sits in
*"A complete software-only example"*, whose job is the SPI flow, not re-teaching configuration. No
published figure is tied to that example, so nothing needs regenerating. Verified: compiles clean
under `pnut-ts -d`, the emitted directive carries all three channels, and the printed block is
byte-identical to `examples-library/ch06-logic-spi-bus.spin2`.

**Also ruled out, and left as a bench question:** dropping the explicit `1` counts. `LOGIC_Configure`
reads the next token as `count` via `KeyValWithin(v, 1, 32)` **before** reading the color, and whether
a failed count consumes the token is not determinable from the manual's REF. If it consumes, the color
is lost silently. Not usable without a PNut/bench check — which is also why the explicit `1` is
probably load-bearing in every channel declaration in the manual.

**Debug Window's remaining line work:** 23 lines over K=76, **2 still past the ~101-col cliff** —
`ch07-scope.md:272` (121, the SCOPE channel case, source-determined split available) and
`ch14-multiwindow-pasm.md:299` (110, trailing comment only, comment-above fix).

### F-291 — the escaper missed two code contexts, so five lines of a released manual print a literal backslash. `CONFIRMED` — **escaper fixed, sweep extended, sites verified clean 2026-08-17**

**Found:** 2026-08-17, testing F-278's deferred question (does `> ```antipattern` render inside a
blockquote?) on the daemon before risking a production render. The answer is **yes** — but the test
page showed the code inside the blockquote as `DEBUG(\`SCOPE\_XY W 128 'A')`, with a literal
backslash, while the identical pair *outside* the blockquote rendered `SCOPE_XY` correctly.

**Five lines are affected in the RELEASED Debug Window v1.1.2**, verified by extracting the shipped PDF:

| Page | Prints | Context |
|---|---|---|
| p88 | `DEBUG(\`SCOPE\_XY W 128 'A')` and the `W SIZE` line beside it | fenced block **inside a blockquote** |
| p159 | `PC\_KEY`, `PC\_MOUSE`, `DEBUG\_END\_SESSION` | **double-backtick** inline spans |

**Mechanism — two blind spots in `latex_escape_processor.py`, both proved by probe:**

| Context | Before | Correct? |
|---|---|---|
| prose | escapes `_`→`\_` | ✅ right |
| `` `single span` `` | protected | ✅ right |
| ``` ``double span`` ``` | **escaped** | ❌ → p159 |
| fenced block | protected | ✅ right |
| `> ` fenced block | **escaped** | ❌ → p88 |
| quoted prose | escapes | ✅ right |

1. **Fence detection was not blockquote-aware.** It tested `line.strip()`, which leaves the `> ` in
   place, so `> ```spin2` never registered as a fence; the body was treated as prose and escaped.
   Fixed by stripping leading blockquote markers before the fence test only — quoted *prose* must
   still escape exactly like unquoted prose, and it does.
2. **Double-backtick spans were unmatched.** The inline pattern is `(?<!`)(`[^`\n]+`)`: its body
   excludes backticks and it refuses a preceding backtick, so ``` ``DEBUG(`Name `PC_KEY(@v))`` ```
   — the form used precisely *because* the content contains a backtick — fell through to prose.
   Fixed by protecting double-backtick spans before single ones.

**Why the escaped character PRINTS rather than escaping:** both contexts still render verbatim
downstream, and inside verbatim `\_` is two literal characters. The escape was never wrong in
LaTeX terms; it was applied where LaTeX rules do not apply.

**`audit-tex-artifacts.py` (F-286) MISSED this, and now does not.** The sweep excluded verbatim
regions wholesale — correct for every other check, since code legitimately contains almost every
signature. But *inside* verbatim a backslash-escaped special is the one thing that IS a defect, so
the sweep now scans verbatim for exactly `\_ \& \# \% \$`. Verified it flags the leak and does
**not** flag legitimate PASM2 `#\label` (that is `\l`, not in the set) or correct prose escaping.
**A skip-list is an assumption, and this one had a hole in it.**

**Fixed and verified:** the staged Debug Window markdown now carries `SCOPE_XY`, `PC_KEY`,
`PC_MOUSE` and `DEBUG_END_SESSION` clean in their code contexts, while prose occurrences still
escape correctly (38 legitimate `\_` remain, all prose).

**F-278's deferred site is now converted.** With the fence-in-blockquote combination proven to
render — red antipattern box, correctly indented inside the quote, trailing quoted prose intact —
`ch08-scope-xy.md`'s wrong/right pair is split: the wrong form is an `antipattern` block, the
correct form a `spin2` block beside it, matching the Chapter 12 treatment. Rides v1.1.3.

### F-292 — six printed snippets teach a `...` continuation inside `debug()`, so each one silently ships a different program. `CONFIRMED` — **all six fixed 2026-08-17**

**Found:** 2026-08-17, answering "any more outstanding issues with this manual?" after F-290
established that a `debug()` directive cannot be continued at all. Searching the masters for the
pattern found six.

**Proved, not inferred.** The ch07 snippet compiled exactly as printed emits
`Waves 'Sine'  -1000 1000 100   0 0 $00FF00 ...` — **the `'Tri'` and `'Noise'` channels are gone**
and the literal `...` is embedded (9,328 vs 9,393 bytes). A reader who copies it gets a one-channel
scope where the page shows three.

| Site | Reader silently got | Route taken | Authority |
|---|---|---|---|
| `ch07-scope.md:109` | 1 of 3 SCOPE channels | three separate feeds | `SCOPE_Update` accepts a channel def and `vIndex` only resets in `SetDefaults` |
| `ch09-fft.md:163` | `'Left'` only, no `'Right'` | two separate feeds | `FFT_Update` accepts "CLEAR/SAVE/PC_KEY/PC_MOUSE **+ channel-defs** + samples" |
| `ch04-bitmap.md:144` | palette truncated at entry 7 | LUTCOLORS as its own feed | REF: "Replace LUT palette entries at runtime"; the house form is proven by generator `fig-13-packed-bitmap-frame.spin2` |
| `ch03-term.md:166` | colour pairs 2 and 3 lost | one line (`SIZE` dropped to fit) | `COLOR` is **config-only** for TERM — no `key_color` arm in `TERM_Update` |
| `ch10-spectro.md:145` | everything after `TRACE 12` lost | one line + waiver | `SPECTRO_Update` accepts only CLEAR/SAVE/PC_KEY/PC_MOUSE |
| `ch10-spectro.md:166` | everything after `TRACE 8` lost | one line + waiver | same |

**Verified by compiling all six fixed forms together and reading the emitted directives:** every
channel, colour pair and config keyword is present, and **zero** literal `...` remain in the binary.

**Why every gate missed them, and this is the transferable part.** These are *uncaptioned*
illustrative snippets — not paired with an `examples-library` file, so never compiled — and each
PHYSICAL line was short, because the `...` is what made them fit. So the width gate saw nothing and
the compile gate never ran. **The defect lived exactly in the gap between "too wide to print" and
"too broken to run", and neither gate covers it.** Extending compile certification to uncaptioned
fragments is a real question (fragments must be wrapped to compile) and is deliberately NOT decided
here.

**One pedagogical change, flagged rather than buried:** `ch04-bitmap.md`'s palette demo moves from
LUT4 with sixteen entries to **LUT2 with four** (pixels `& $03`), because sixteen `$RRGGBB` values
cannot fit a printable line by any means — `LUTCOLORS` overwrites from index 0, so it cannot be split
across messages either. The teaching survives intact (LUT mode, inline palette in one statement,
pixels as indices) at a smaller scale. The chapter's LUT-mode reference table still documents LUT4 as
4 bits / 16 entries.

**It also closes a punch-list question open since June.** The "Other" section asked whether the
original `fig-07` failure — a creation-line channel def drawing an empty "Channel 0" plot — "came
from a `...` line-continuation artifact." It did. The creation-line-versus-separate-feed debate was
chasing the wrong variable; the `...` was dropping the channels, so the REF source was right all
along and the TO-RECONCILE item closes on evidence rather than another capture.

**Next finding ID after this block: F-295.**

---

### F-301 — the cross-ref filter's adopt-at-next-release rule was passed over about a dozen times, because nothing read the tracker. `CONFIRMED` — **detected 2026-08-19 by comparing the tracker against every `request.json`**

**The rule, written into `CROSSREF-FILTER-ADOPTION.md` when the filter shipped 2026-06-26:**
*"The next time each manual is released (for any reason), its release MUST add
`p2kb-platform-crossref` to that manual's `request.json` `lua_filters` and visually audit the
rendered PDF."* The tracker even names its own consumer — *"`release-manual` Phase 1/Phase 4
**should** consult this tracker."*

**Measured, not assumed.** Every workspace `request.json` read directly against the tracker's rows:

| Document | Tracker | In `request.json`? | Releases since the rule |
|---|---|---|---|
| Assembly | ⏳ pending, at v3.1.0 | **no** | v3.1.1 → v3.1.6 |
| DeSilva | ⏳ pending, at v3.0.1 | **no** | v3.0.2 → v3.0.6 |
| Debug Window | ⏳ pending, at v1.0.1 | **no** | v1.0.2 → v1.1.3 |
| Getting Started | ⏳ pending, at v1.0.0 | **no** | v1.0.1 → v1.0.3 |
| Architect | ⏳ "in development" | **no** | released v1.0.3 |
| XBYTE | **absent from the table** | **no** | v1.0.0, v1.1.0 |
| 7 app notes | **absent from the table** | **no** | 20+ |
| IOSP | 🔧 adopting (pilot) | yes, ordering correct | audit never recorded |
| Streamer | ✅ adopted + audited | yes, ordering correct | — |

**Only two of fifteen ever adopted.** IOSP's row still reads "awaiting Stephen's regen + visual
audit" although it has released three times since, so its filter has certainly rendered — the
**audit** is what is unrecorded, and that half is the half that matters (a mis-fired auto-link is
exactly what the audit exists to catch).

**The statuses are not wrong. Nothing read them.** Every row above is an accurate record of a
decision that was then never consulted at the moment a release happened. This is the same failure
as [[F-281]]'s «#250» in a different costume — a correct record that is not where the decision gets
made — and it is why adoption state moved into `PLATFORM-FEATURE-ADOPTION.md`, which
`prepare-manual` consults on every prepare rather than "should" consult on release.

**FIX — structural, landed 2026-08-19:** one per-document × per-feature matrix
(`PLATFORM-FEATURE-ADOPTION.md`), seeded from **detected** state rather than from what each tracker
claimed, plus a `prepare-manual` check that surfaces a document's outstanding ⏳ features as work
owed **this** release. `CROSSREF-FILTER-ADOPTION.md` keeps the mechanism (including the mandatory
crossref-before-tables ordering) and its status table is frozen as history.

**Still owed per document:** the adopt + visual audit itself, at each document's next release —
that has not been shortcut, only made visible. **ssdb and pnut-term-ts release next and both sit at
⏳**, so they are the first two chances to stop the count growing.

### F-300 — every published PDF in the set ships with empty Title and Author properties. `CONFIRMED` — **MECHANISM LANDED + PROVEN 2026-08-19; adoption is per document, tracked in `PLATFORM-FEATURE-ADOPTION.md`**

> **RESOLUTION (2026-08-19).** The fix is **not** the one-line `pdfusetitle` this entry proposed —
> that would have populated the info dictionary and left the cover as a second hand-maintained copy
> of the same five strings, and would have shipped *wrong* titles on 9 of 15 (see the template table
> below). What landed instead: **every identity string lives once, in the document's `request.json`
> metadata, and reaches both the PDF info dictionary and the cover page from there**, via
> `\DocTitle`/`\DocSubtitle`/`\DocVersion`/`\DocDate`/`\DocAuthor` defined in
> `p2kb-platform-foundation.sty` (§ DOCUMENT METADATA). The macros carry the *value*; the cover keeps
> its *presentation*.
>
> **Proven on the interactive daemon, four round-trips, by reading the rendered PDF** — not the
> success flag. Both first converts (Single-Step Debugger, PNut-Term-TS User Guide) came back with
> compile logs clean on every serious signature and Title/Author/Subject populated for the first
> time, covers rendered and looked at. Commit `09958b0a`.
>
> **Unconverted documents are safe:** the foundation `\providecommand`s all five macros empty, so a
> template that has not opted in writes exactly what it wrote before. **Per-document adoption state
> is `PLATFORM-FEATURE-ADOPTION.md`**, and `prepare-manual` now reads it. The analysis below stands
> as the record of how the fix was found; only the proposed one-liner is superseded.

**Surfaced by** the Streamer v1.0.9 release verification — reading the delivered PDF's metadata
dictionary, then checking whether it was a Streamer regression. It is not: **all 15 PDFs in
`deliverables/documents/DOCs/` report `(empty)` for both `title` and `author`** — eight manuals and
seven app notes. Only `creator` (`LaTeX with hyperref`) and `producer` (`xdvipdfmx`) are set.

**What a reader sees.** A PDF viewer's title bar and Document Properties fall back to the *filename*
instead of the document's name, and anything indexing the file — a search tool, a library, a
citation manager — finds no title or author to key on.

**The mechanism, traced end to end.** The `.latex` template sets `\title{P2 Streamer Programming
Guide}` (generated `.tex` line 31), and `p2kb-platform-foundation.sty:259` sets a `\hypersetup`
block — but that block configures **only** link colors and bookmarks. It never sets `pdftitle` or
`pdfauthor`, and **hyperref does not derive them from `\title{}` on its own**; that requires either
`pdfusetitle` or explicit keys. So the title exists in the document body and never reaches the PDF
info dictionary.

**FIX (one line, in the shared platform):** add `pdfusetitle` — or explicit
`pdftitle={...}, pdfauthor={...}` — to the `\hypersetup` block at
`p2kb-platform-foundation.sty:259`. **Zero layout risk**: it writes the PDF info dictionary only and
cannot reflow a page. This is what distinguishes it from [[F-299]], which is parked because it
*does* move type.

**Corrects a claim in our own process doc.** The `prepare-manual` skill states that a `request.json`
metadata change "feeds PDF properties, not just the build." For this manual-production path that is
**not true** — the template hardcodes `\title{}`, and nothing carries `request.json`'s
`metadata.{title,author,version}` into the PDF info dictionary. Re-staging `request.json` on a
document switch is still mandatory for a different and real reason (input/template/filters), so the
rule stands; only its stated justification about PDF properties is wrong. Fix that sentence when the
platform fix lands.

**Sequencing.** No manual should re-render just for this. Let it ride with the next render each
document takes anyway, and take it in the same set-wide sweep as [[F-299]] — one `forge-test` pass,
two set-wide render changes.

> **Stale reference removed 2026-08-19.** This sentence named the fancyvrb `breaklines` work «#250»
> as a third member of the sweep. That work was **REJECTED 2026-08-17** on the round-trip evidence
> (see [[F-281]]); the reference was written after the rejection and never checked against it. The
> sweep is F-300 + F-299, and F-299 is polish. There is no breaklines work to schedule.

⚠️ **TRAP FOR WHOEVER TAKES THIS FIX — the two title sources already disagree.** Because nothing
consumes `request.json`'s metadata today, nobody has had to keep it in step with the cover, and it
has drifted. On the Streamer: the **cover** reads *"Comprehensive Reference for Propeller 2 Streamer
Hardware"* while `request.json` reads *"Comprehensive Reference for the Propeller 2 Streamer"*. The
moment `pdftitle`/`pdfsubject` start being populated, whichever source the fix wires up becomes
reader-visible, and a stale one ships silently. **Before adopting: audit cover-vs-`request.json`
across all 15 documents and reconcile, then decide which source is authoritative** (the cover is
what a reader actually sees, so it should win). Do not wire the metadata through without that pass.

**THAT AUDIT IS NOW MEASURED (2026-08-19), and the drift is systemic, not a Streamer typo.** Comparing
each master's cover block (`\fontsize{36}…\bfseries` title + `{\Large\itshape …}` subtitle) against
its `request.json` `metadata.subtitle`, over the 15 published documents:

| Verdict | Count | Which |
|---|---|---|
| **SAME** | 3 | Architect, Assembly, Getting Started |
| **DRIFT** | 8 | Debug Window, Streamer, P2AN001, P2AN002, P2AN003, P2AN004, P2AN005, P2AN007 |
| **cover block not matched by this scan** | 4 | IOSP, deSilva, XBYTE, P2AN006 — a different cover shape, **unresolved, not clean** |

**Two of the drifts are kinds of drift, not typos, and they change what the fix has to decide:**
1. **The app notes disagree structurally.** `request.json` carries a *catalog label* — "Application
   Note P2AN001 — No External ADC" — while the cover carries a *reader subtitle*: "No external ADC —
   a single-pin instrumentation ADC…". Neither is a stale copy of the other. Wiring the cover through
   verbatim drops the P2AN00N designator from the PDF's Title; wiring `request.json` through gives
   every app note a title that is not what its cover says. **Decide this before touching the
   platform** — likely `pdftitle` = title + designator, `pdfsubject` = the reader subtitle.
2. **Cover strings contain LaTeX.** PNut-Term-TS's cover subtitle carries a literal `\\` line break.
   PDF info-dictionary fields are plain text, so any such markup must be stripped, not passed through
   — one more reason `pdfusetitle` (which takes `\title{}` as-is) is not automatically the right
   mechanism for the subtitle half.

Truncation was not checked: two of these subtitles run past 50 characters and the register scan
compared full strings, so the counts above are exact for equality but say nothing about length limits.

---

**⚠️ THE SUBTITLE DRIFT IS NOT THE GATE. The gate is the templates, and nobody had looked at them
(traced 2026-08-19).** `pdfusetitle` populates `pdftitle` from `\title{}` and `pdfauthor` from
`\author{}` — it never touches the subtitle. So the drift table above gates only a `pdfsubject` we do
not have to wire. What actually decides whether this fix can be turned on and left to ride is what
each template declares, and **9 of the 15 declare something wrong:**

| Template `\title{}` | Documents | Verdict |
|---|---|---|
| `P2 Application Note` (hardcoded, SHARED) | **all 7 app notes** | **BROKEN** — `pdfusetitle` gives seven distinct documents one identical title. Worse than empty in a library or index. |
| `P2 XBYTE Programming Guide` | XBYTE | **STALE** — the released v1.1.0 cover reads *"P2 Interpreters & Emulators Guide"*. The template kept the pre-retitle name. |
| *(no `\title` and no `\author` at all)* | deSilva | **EMPTY** — would stay broken after the fix. |
| correct, matches cover | Architect, Assembly, Debug Window, Getting Started, IOSP, Streamer | ready |

`\author{Iron Sheep Productions, LLC}` is correct in every live template **except deSilva's**, which
has none.

**The one fact that makes all of this safe: `\title{}` is never rendered.** Every cover in the set is
hand-built in the master's `front-matter.md` (`\fontsize{36}{42}\selectfont\bfseries …`). There is no
`\maketitle` anywhere in the published set — the only one in the tree is in `ai-privacy-guide`, which
is not a published document. **So `\title{}` is metadata-only, and changing it cannot move a single
point of type on any page.** That is what turns this from a render-risk change into a ride-along.

**REVISED PLAN — prep in one commit, no renders, then ride:**
1. **Switch every live template from a hardcoded `\title{…}` to `\title{$title$}` / `\author{$author$}`.**
   `request.json` becomes the single source and a template can never go stale against its document
   again — this is what fixes the seven app notes and XBYTE at once, and it is durable rather than a
   catalog of literals to maintain. Verified safe: **`request.json` `metadata.title` equals the cover
   title for 14 of 15**, including all seven app notes (the cover carries the designator on its own
   eyebrow line — *"Propeller 2 • Application Note P2AN006"* — above the title, so nothing is lost).
2. **deSilva is the one real conflict, and it is BOTH fields.** Released cover: *"P2 Assembly
   Programming"* / *"A Human-Centered Approach to Parallel Processing"*. `request.json`:
   *"Discovering P2 Assembly"* / *"Build, Experiment, and Master the Propeller 2"*. The cover wins →
   update `request.json`, then give `p2kb-desilva.latex` the same `$title$`/`$author$` pair.
3. **Add `pdfusetitle`** to the `\hypersetup` at `p2kb-platform-foundation.sty:259`.
4. **Do NOT wire `pdfsubject`.** Leaving it out defers the whole subtitle question above at zero cost;
   revisit it as its own item whenever someone wants Subject populated.
5. **Add a `PLATFORM` ledger line and let each document absorb it at its next natural render.**
   Precedent for the standing: the 2026-07-13 mnemonic-bold line — *live-but-benign, not outstanding
   debt*. No manual re-renders for this.

**One `forge-test` still confirms three things before adoption**, none of them layout: that `$title$`
substitution actually reaches `\title{}` on this path, that `&` survives into the info dictionary
(IOSP *"P2 I/O & Smart Pins User Guide"*, P2AN006 *"Sizing Cog & Task Stacks"*), and that `pdfauthor`
lands. Read the output PDF's metadata dictionary, not the compile log.

### F-299 — wide `tblr` tables overhang the right text edge by ~5–6pt, in the platform, not the manual. `CONFIRMED` — **POLISH, NOT A GATE FAILURE: it is inside the project's own 20pt tolerance (re-graded 2026-08-19, same day, see the correction at the end)**

**Surfaced by** the Streamer v1.0.9 daemon pre-verify — a whole-document margin measurement of the
rendered PDF (every text span's `x1` against the 540pt text edge), not by the compile log, which was
clean on every serious signature in both the v1 and v2 renders.

**The defect.** Two of the Streamer's wide mode-reference tables push their rightmost column past
the text block: §6.2 *RDFAST → Pins/DACs* by **6.1pt** (`DAC Bits` header) and §8.x *Pins/DACs →
Hub* by **5.3pt** (`Hub Write` header). Visible as the table's horizontal rules extending past the
running-header rule directly above them. The compile log reports these as `Overfull \hbox
(26.6406pt too wide)` — the larger number is the whole `tblr` box including padding; the visible
overhang is the 5–6pt the measurement above reports.

**Why it is the platform's, not the manual's.** The column widths are computed by
`p2kb-platform-tables.lua`, which every manual in the set loads. Nothing in the Streamer's markdown
sets a width. A manual-side "fix" would mean hand-tuning a table the filter is supposed to own.

**NOT the two tables an earlier note predicted.** The Streamer release note expected the
`p2kb-platform-tables.lua` column fix to absorb "2 over-wide `Constant | Value | Description`
tables". These two are **6-column** `Mode | Symbol | Type | Pins | DAC Channels | DAC Bits` tables —
a different shape the fix does not reach. The prediction was not wrong about its own targets; it
was applied to the wrong pair. **A status note naming a fix is not evidence the fix covers what you
are looking at** — measure the artifact ([[feedback_status_line_is_not_evidence]]).

**Deliberately not fixed in this release.** A column-width change in
`p2kb-platform-tables.lua` reflows tables in **every** manual, so adopting it while Streamer is
mid-render means re-verifying the whole set against a changed table model for 6pt of rule overhang.
Schedule it when no manual is mid-render, and expect the absorbing manual's next render to shift
table layout. **Pair it with [[F-300]]** — both are set-wide render changes whose failure mode is a
page that looks fine in the log, and both want one `forge-test` sweep across the set rather than two.

> **Stale reference removed 2026-08-19.** This paragraph cited the fancyvrb `breaklines` work «#250»
> as the precedent it followed and the partner to pair with. That work was **REJECTED 2026-08-17**
> ([[F-281]]) — before this entry was written. The scheduling rule it borrowed is sound and stands on
> its own; the partner is F-300.

**Scope when taken:** measure every manual, not just the Streamer — the filter is shared, so any
manual with a 6-column table is a candidate.

---

⚠️ **CORRECTION, same day, before this entry could mislead anyone — I RE-GRADED MY OWN FINDING.**

I measured this with a hand-rolled PyMuPDF scan at a **4pt** threshold. **The project already has a
sanctioned instrument for exactly this** — `engineering/tools/validation/audit-pdf-margin-overflow.py`
— and I did not use it. Run against the shipped v1.0.9 PDF it reports:

```
text-block right edge: prose 540.0pt, code 540.0pt   (tolerance 20pt)
CLEAN  nothing crosses the margin (76 pages measured)
```

**The gate's tolerance is 20pt by design. These tables are 6.1pt and 5.3pt — comfortably inside it.**
So both statements are true and the second is the one that sets priority: the overhang is real and
visible if you look for it (the table rule extends a hair past the running-header rule), and it is
**not** something the project's own margin gate would ever block on.

There is direct precedent for accepting far more: the IOSP v1.0.9 PUBLISH line accepts a chart
bleeding **~24pt** past the text block on evidence — zero overlapping spans measured, every cell
readable — with the explicit note that *magnitude is never the verdict*. A 6pt rule overhang with no
overlap is a smaller version of the same accepted case.

**Re-grade: this is POLISH, not a defect owed.** Still worth taking in the set-wide sweep with
[[F-300]] because the fix is cheap once the platform is open anyway — but it must not be
described as a defect blocking anything, and no manual should re-render for it.

**The transferable lesson — the one worth more than the finding.** Reach for the project's own
instrument before hand-rolling a measurement. Mine was not wrong, but it carried **no calibrated
threshold**, so it reported a number without the judgement that makes the number mean something, and
I very nearly filed a tolerance-conformant table as a defect owed. A raw measurement is not a
verdict; the tolerance IS the verdict ([[feedback_validation_tool_verdict_is_a_claim]] — the inverse
case, where the tool PASSES and the hand-rolled scan is the one overstating).

### F-294 — a backtick inside a single-backtick span inverts every code span after it, printing seven lines of prose as code. `CONFIRMED` — **source fixed 2026-08-17; render owed**

**Found:** 2026-08-17, in the same Debug Window v1.1.3 audit as F-293 — by opening p84 because the
compile log's largest overfull (57.66pt) pointed there.

**What p84 prints.** The whole "Try it" paragraph of Chapter 7 is wrecked: a sentence-initial stray
`.`, a font that flips to monospace mid-sentence and stays there for two lines of ordinary prose
(*"and observe the waveform stand still instead of scrolling. Finally, vary the trigger"*), then
words fused without spaces — `triggeroffsetbetween0,SAMPLES/2,` and `ANDSAMPLES-1'` — and a stray
closing quote. It is the most visibly broken paragraph in the manual.

**Mechanism.** `ch07-scope.md:474` wrote a **single**-backtick span whose body contains a backtick:

    (`debug(`Waves TRIGGER 0 -500 500 256)`)

Pandoc closes a single-backtick span at the *first* backtick it meets, so the span is `debug(`; the
next backtick **opens** a new one that runs until the backtick before `offset`, swallowing two lines
of prose. Every span in the rest of the paragraph is then inverted — code reads as prose, prose reads
as code — which is exactly what the page shows.

**Fixed** by the double-backtick form this manual already uses precisely for backtick-bearing content
(the same form F-291 protected in the escaper): ``` (``debug(`Waves TRIGGER 0 -500 500 256)``) ```.
Verified balanced.

**Swept fleet-wide.** All 155 master files, paragraph-wise (a code span may legally wrap across
lines, so a line-wise check false-positives on four innocent sites). **This is the only real
occurrence.** Two other flagged paragraphs are `CONVENTIONS` authoring headers inside `<!-- -->` in
the Architect and Getting Started masters — confirmed absent from both shipped PDFs.

**⚠️ This overfull was on record as adjudicated and benign.** It was carried as *"the 57.66pt overfull
is an unbreakable `\lstinline` prose run, not a code line"* — which is mechanically true and entirely
misleading: the run is unbreakable **because a span inverted**, and the paragraph around it is
broken. The note explained the symptom accurately enough to stop anyone opening the page. **An
explanation is not a verification**, and "already adjudicated" is exactly the label that keeps a
defect alive — the second time in one audit that a status line was wrong (see F-293 on Assembly).

**Gate gap.** No gate we own sees this: the escaper hands the span through, `audit-tex-artifacts.py`
sees legal `.tex`, the code-line gate measures code blocks, and the compile is clean. The only signal
was an overfull box that had been explained away. A paragraph-wise backtick-balance check on the
masters is the missing instrument.

**Owed:** re-render, then confirm p84's "Try it" paragraph reads as prose throughout.


### F-293 — the escaper pre-escapes `^`, so eight exponent expressions across three manuals print a literal `^{}`. `CONFIRMED` — **escaper fixed 2026-08-17; renders owed**

**Found:** 2026-08-17, auditing the Debug Window v1.1.3 render. p107's bullet reads
`multiplies the FFT output by 2^{}shift` — braces on the page.

**Eight sites, verified by extracting the shipped/staged PDFs — not inferred from source:**

| Manual | Pages | Prints |
|---|---|---|
| Debug Window (v1.1.3, staged) | p104, p107 | `2^{}shift` |
| **Assembly (v3.1.6, rendered + marked releasable)** | p93, p209, p284 ×2, p350 | `2^{}x`, `2^{}128`, `2^{}32-1`, `2^{}32` |
| IOSP (v1.0.8, RELEASED) | p320 | `2^{}X[3:0]` |

**Mechanism — a double escape, and the sources are innocent.** Every master writes plain `2^shift`
/ `2^32`. `latex_escape_processor.py` replaced a bare `^` with `\^{}` in the *markdown*; Pandoc then
read `\^` as an escaped literal caret (emitting `\^{}` itself) and escaped the two braces it found
next, producing `\^{}\{\}` — which xelatex prints as `^{}`. The escape was correct LaTeX applied one
stage too early.

**The file already carried the right precedent and did not follow it.** Line 435: *"Don't escape
tildes - Pandoc handles them fine in markdown."* A bare caret is the identical case. The caret path
even had a comment naming the failure — *"If we escape ^ to `\^{}`, Pandoc outputs literal `^{}`
which breaks LaTeX"* — but the guard built from it only protects **matched** `^text^` superscript
pairs. Unmatched carets, which is how every one of these eight is written, fell straight through.

**Fixed in three places, not one.** The prose path plus two latent copies of the same bug — the
markdown-header path (whose `XPROTECT_CARET_X` dance defends the escaper against *itself* while
leaving Pandoc's second pass untouched) and the `\section{...}` content path. No master file changed;
fixing the tool fixes all eight sites at next render.

**Matched superscript pairs are unaffected** — `2^32^` in IOSP still resolves to true superscript.
That is why IOSP shows one broken site and not four.

**Owed:** re-render Debug Window, Assembly and IOSP, then confirm the listed pages print a caret and
no braces. **Pandoc's handling of a bare caret is reasoned, not yet observed** — local Pandoc is
off-limits, so the round-trip is the proof.

**⚠️ This unblocks nothing and blocks one thing: Assembly v3.1.6 was recorded "verified, releasable,
nothing blocking." It carries five of the eight sites.** The verification that cleared it was
thorough about what it looked for — outline, page count, F-288's pages, log signatures — and this was
not on the list. **A verification pass is only as wide as its checklist**, which is the F-285 lesson
arriving a second time.

**RESOLVED 2026-08-17 — the set standardizes on true superscript.** IOSP's appendix-c wrote `2^32^`
(superscript) at lines 35 and 501 but `2^X[3:0]` (literal) at 171 — one document, one concept, two
renderings. All 8 literal sites are now pandoc superscript pairs, joining the 5 that already were:
**13 consistent exponents across three manuals**, verified by re-sweep (0 unmatched carets remain in
renderable prose). The tool fix alone would have printed a correct-but-inconsistent circumflex; the
notation decision is separate from it and is now made, not deferred.

**Left alone deliberately:** `p2-pasm-desilva-style/opus-master/CHANGELOG.md:98` (`2^x`). CHANGELOGs
render into no PDF (verified across all four), and it is a released entry — rewriting shipped history
to fix text nobody renders is churn, not quality.

### F-285 — `&nbsp;` prints literally in 16 instruction-syntax lines of a RELEASED manual. `CONFIRMED` — **source fixed 2026-08-17; Assembly needs one more render**

**Found:** 2026-08-17, verifying the Assembly re-render for F-284. The F-284 fix was confirmed
good on p.326 and p.329 — and p.329 put this defect on screen at the same time. It is unrelated to
F-284 and was not caused by it.

**Location:** `part-ii/instructions-t.md` — 16 sites across the TESTB, TESTBN, TESTP and TESTPN
syntax blocks. Visible at **P2-Assembly-Language-Manual p.329** and neighbours as, literally:

    TESTP {#}Dest&nbsp;&nbsp;WC/WZ

**Mechanism.** The source writes `*Dest*&nbsp;&nbsp;**WC/WZ**`. Pandoc did not resolve `&nbsp;` as
an HTML entity; it treated the ampersand as literal text and emitted `\&nbsp;` into the `.tex`, so
xelatex prints the entity as characters. The escape script is not at fault — the workspace copy
still carries a bare `&nbsp;` — and it produces no warning or error at any stage.

**Not new, and not from the platform fix.** Introduced 2025-12-21 by `096230a4` ("Fix multi-page
tables and TESTP/TESTPN formatting"), present in the v3.1.5 tag's source, and therefore shipped in
at least v3.1.5. The F-284 filter change touches only 9-column table cells; these are body prose.

**It is a one-file anomaly, not a convention.** `&nbsp;` appears **nowhere else** in the manual —
not in the other 21 instruction-letter files, not in Part I, not in Part III. The TEST page's own
neighbouring syntax lines, four lines above the corrupted ones, use a plain space:
`**TEST** *Dest, {#}Src* **{WC|WZ|WCZ}**`. So the fix is to match the file's own surroundings.

**Fix applied:** all 16 `&nbsp;&nbsp;` replaced with a single space. No other file touched. No
version bump — v3.1.6 has not shipped.

**Owed:** one more Assembly render, then confirm p.329 reads `TESTP {#}Dest WC/WZ`.

**Lesson, and it is the same one twice in a day.** Both F-284 and F-285 are invisible to every gate
we own — clean log, no warning, correct source characters — and both were found by rendering a page
and looking at it. F-285 also shows the cheaper half: **the page you open to verify one fix is free
evidence about everything else on it.** Verifying narrowly would have missed this.
