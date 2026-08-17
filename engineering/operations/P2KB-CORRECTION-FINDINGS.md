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

**Next finding ID: `F-289`**

**Archives** — search them before re-filing; a finding that reappears is usually a regression:
- F-001…F-124 → `correction-sweeps/2026-06-13-P2KB-CORRECTION-FINDINGS-archive.md`
- F-125…F-266 (closed) → `correction-sweeps/2026-08-15-P2KB-CORRECTION-FINDINGS-archive.md`

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

## Golden-source defect — duplicate EF id (2026-08-15) — F-267

### F-267 — `EF-020` names TWO unrelated findings in the empirical ledger, and both are cited from RELEASED documents. `DONE (2026-08-16) — renumbered, citations repointed`

> **APPLIED 2026-08-16 («#238»).** The PLOT entry is now **EF-061**; the `SETQ`+`WAITSEx` entry
> keeps EF-020. The renumbered heading carries an inline note recording the old id and why the
> other entry kept it, so a reader arriving from an old citation is not stranded. Three citation
> sites repointed — `PLOT_Theory_of_Operations.md` ×2 and the `YAML-HEAD-DASHBOARD.md` v1.14.3
> row (which also records the renumber, since that row describes a release that shipped under the
> old id). The v1.14.0 dashboard row and both `PUBLICATION-ROSTER.md` citations mean the SETQ
> entry and were left alone.
>
> **Verified all three ways:** every remaining `EF-020` hit resolves to the SETQ/WAITSEx meaning;
> `EF-061` resolves to the PLOT entry plus exactly its three repointed citations; and no EF id
> appears twice as a heading in the ledger. The auto-memory `reference_plot_cartesian_flipy_semantics`
> cites no EF number, so it needed no change.

**Location:** `engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md`
`:291` and `:794`. **The ledger is the golden source** — a citation into it must resolve to one fact.

- `:291` **EF-020** · `SETQ`+`WAITSEx` = single-instruction event-OR-timeout; no-SETQ `WCZ` is a free flag-clear.
- `:794` **EF-020** · PLOT default coordinates are bottom-left / Y-UP.

**Both are cited externally, in shipped material** — so "just renumber it" is a citation-identity
change, not a typo fix:

| Citation | Means |
|---|---|
| `PUBLICATION-ROSTER.md` — IOSP v1.0.1, Assembly v3.1.2 | the SETQ/WAITSEx entry |
| `YAML-HEAD-DASHBOARD.md` v1.14.0 | the SETQ/WAITSEx entry |
| `YAML-HEAD-DASHBOARD.md` v1.14.3 | the PLOT entry |
| Debug Window manual `REF/theory-of-operations/PLOT_Theory_of_Operations.md` ×2 | the PLOT entry |

**Proposed correction — Stephen's call, not swept.** The SETQ entry has priority: it was assigned
2026-07-04 with F-193. The PLOT entry was retro-absorbed later (folded in at KB v1.14.3, and it sits
in the ledger's *"Prior-session empirical facts (absorbed)"* section), taking a number already in use.
So **renumber the PLOT entry to `EF-061`** and update the four citation sites above. Do not renumber
the SETQ entry — it is the one cited from two released manuals' roster history.

**Surfaced by:** the duplicate-ID STOP rule in `.claude/skills/REGISTER-CONSULTATION.md`, while
appending EF-053…EF-060. Nothing in flight depends on it, so it was surfaced rather than resolved.

---

## ⛔ REVERSAL — a shipped KB correction went the wrong way (2026-08-16) — F-269

### F-269 — I/O pin power domains are groups of **FOUR**, not eight. F-211 corrected a correct fact into a wrong one, and it shipped in KB v1.15.0 and a RELEASED app note. `DONE (2026-08-16) — KB v1.16.3 + P2AN001 manual half applied`

**Surfaced by:** executing «#219», whose instruction was *"ground every number against the
DOMAIN_AUTHORITY (the ingestion tree, empirical findings first), **not** against F-211's summary
text — the finding is a pointer to the authority, not a substitute for it."* Doing exactly that
returned the opposite of what the task asked us to write. **The instruction worked.**

> **CHALLENGED AND RE-GROUNDED 2026-08-16 (Stephen).** *"Given the headers on the breakout boards I
> would suggest groups of 8 — but we have to absolutely ground this from ingested sources."*
> Correct on both counts, and the challenge produced the answer this entry now carries: **there are
> TWO real grouping layers, and they are different numbers.** Neither of us was wrong about our own
> layer; F-211's error was writing the board layer into the silicon file.

### The two layers — both grounded, both true, never to be conflated again

| Layer | Grouping | Grounded in |
|---|---|---|
| **SILICON** — `P2X8C4M64P` package | **16 domains of FOUR pins.** `VIO_0_3 … VIO_60_63` + `GIO_0_3 … GIO_60_63` | Silicon Doc v35 Part 1 p.9 pinout figure; P2 datasheet *"groups of 4"* |
| **BOARD** — P2 Edge modules + breakouts | **8 domains of EIGHT pins.** `V00`→P0-7, `V08`→P8-15, … `V56`→P56-63, 300 mA each | `extraction-matrices/edge-module-breakout-compatibility-matrix.md:69-83` — *"8 independent 3.3V LDO regulators"* + the VIO Supply Mapping table; `sources/edge-mini-breakout/…-extraction-audit.md:104` |

**Each Edge LDO feeds TWO silicon VIO pins** (`V00` → `VIO_0_3` + `VIO_4_7`). That is why the boards
present 8-pin headers while the chip has 16 domains — and why the breakout intuition is right about
the board and wrong about the chip.

**Which one governs the ADC guidance:** the **silicon** one. `P_ADC_GIO`/`P_ADC_VIO` reference the
pin's own `VIO_{x}_{y}`/`GIO_{x}_{y}` package rails, so the reference domain is **four pins**. Two
pins in adjacent 4-groups on an Edge module share an LDO *net* but not the same package pin or bond
wire, so IR drop and bond-wire drop still differ between them. **"Stay within four" is correct on
every board; "stay within eight" is an Edge-specific relaxation and must not be taught as the chip's
behaviour.** The 8-pin figure remains correct where it belongs — current budgeting on Edge hardware.

**The authority — two independent primary sources, both Parallax, both already in the ingestion tree:**

1. **The Silicon Doc's own package pinout** — `sources/silicon-doc/assets/images-20260706/P2-Silicon-Doc-v35-Part1_page09_render.png`
   (v35, Part 1, page 9). Read directly, and re-read at 5× magnification on both rails after the
   challenge above. The TQFP-100 perimeter carries **sixteen VIO pins** — `VIO_0_3 · VIO_4_7 ·
   VIO_8_11 · VIO_12_15 · VIO_16_19 · VIO_20_23 · VIO_24_27 · VIO_28_31 · VIO_32_35 · VIO_36_39 ·
   VIO_40_43 · VIO_44_47 · VIO_48_51 · VIO_52_55 · VIO_56_59 · VIO_60_63` — and **sixteen matching
   internal `GIO_0_3 … GIO_60_63` blocks** (verified separately; the GIO grouping is what the ADC's
   ground reference actually follows, so it was checked rather than assumed from VIO).

   **The rail pattern is the proof, not just the labels.** Both rails repeat on a strict six-pin
   cycle — `P(n) · P(n+1) · VIO_n_(n+3) · P(n+2) · P(n+3) · VDD` — placing each VIO pin **centred
   inside the exact four I/O pins it names**. Left rail: `TEST VDD P0 P1 VIO_0_3 P2 P3 VDD P4 P5
   VIO_4_7 P6 P7 VDD …`. Right rail: `P47 P46 VIO_44_47 P45 P44 VDD P43 P42 VIO_40_43 P41 P40 VDD …`.
2. **The P2 datasheet** — `sources/p2-datasheet/p2-datasheet-narrative.txt:226`, verbatim:
   *"Smart I/O pins: 3.3 VDC, powered in **groups of 4** via VIO pins."*

**The package arithmetic closes exactly, and leaves no room for any other arrangement:**
64 I/O + **16 VIO** + 16 VDD + TEST/RESN/XI/XO = **100 pins**, the full TQFP-100. Eight VIO pins
would leave eight package pins unaccounted for; the figure has none spare. GIO consumes no package
pins — it is drawn as internal blocks, which is why it does not appear in the count.

Corroborating, independently derived: the Silicon Doc image catalog
(`…/images-20260706/P2-Silicon-Doc-v35_image_catalog.md:84`) records the same labels from the same
figure, harvested in a separate pass.

**Why F-211 reached "8 groups of 8" — each of its three evidences fails on inspection:**

| F-211's evidence | What it actually is |
|---|---|
| `VERIFICATION-OPPORTUNITIES.md:57` — *"the 64 pins are 8 groups of 8"* | **Our own internal analysis note**, carrying no source of its own. F-211 cited us back to ourselves — circular, and the note is now known wrong. |
| Edge Mini Breakout: *"300 mA per 8-pin group; one VIO3V3/GND pair per 8-pin header"* | **True — of the board.** It describes the Edge's eight LDOs and header wiring, not the chip's VIO domains. **This is the whole error: a board fact imported into the chip's power-domain file.** The fix is not to delete it but to file it under the layer it belongs to. |
| *"The Silicon Doc uses `{x}_{y}` placeholders, so it does not state 4"* | True of the **text** pin-description table — and false of the **figure seven pages earlier in the same document**, which states it explicitly. Silence was inferred from a partial read. |

**And F-211 deleted a TRUE citation as fabricated.** Its applied-note records *"Removed the fabricated
`evidence` citation ('P2 Datasheet: Power for smart pins in groups of 4' — unverifiable)."* That
citation was **accurate**; the datasheet says it, at the line quoted above. A correct source was
removed because it disagreed with a conclusion drawn from a board document.

**What is and is not wrong.** The **mechanism** the KB teaches is correct and must be preserved:
VIO/GIO are per-group; a pin's `P_ADC_GIO`/`P_ADC_VIO` reference its own group's rails; that is what
makes a single-pin ratiometric read absolute; multi-pin shared-node measurements must stay inside one
group. **Only the size, count and boundaries invert** — 8→**4** pins, 8→**16** groups,
`0-7, 8-15, …` → `0-3, 4-7, …, 60-63`, and the straddle example returns from pins 7/8 to **3/4**.

**Blast radius — five published KB files and one released app note:**

| Artifact | State |
|---|---|
| `architecture/pin-power-domains.yaml` | canonical file; `group_size: 8`, `"8 groups"`, boundaries, oneliner, alias, and a `sources:` line quoting the **board** spec as if it established the silicon group size |
| `architecture/smart-pins/smart-pin-11000-adc-internal-clock.yaml` | `power_domain`, `multi_pin_layout`, `see_also`, and a code comment |
| `architecture/smart-pins/smart-pin-11001-adc-external-clock.yaml` | same class |
| `architecture/smart-pins/smart-pin-11010-adc-scope-trigger.yaml` | same class |
| `application-notes/p2an001-single-pin-instrumentation-adc.yaml:99` | the pitfall line |
| **P2AN001 (RELEASED app note)** | was "corrected" 4→8 in `f3e702ed` — **it was right before that commit** |
| `VERIFICATION-OPPORTUNITIES.md:57` | the internal note that seeded the error |
| IOSP `chapter-16-adc.md` | **correct as shipped — do not touch** (see F-261) |

**Explicitly NOT wrong, do not sweep:** `hardware/edge-standard-module.yaml:164`,
`hardware/edge-32mb-module.yaml:237` (*"One LDO per 8-pin group"*), and the other `hardware/*.yaml`
8-pin-group references. Those are **board-level and correct.** The lesson of this finding is exactly
that the two levels are different facts; a blind 8→4 sweep would break the true ones.

**The remediation is therefore an ENRICHMENT, not a revert.** Restoring "4" alone would leave the KB
one challenge away from flipping back — the breakout headers are visible to every reader, so "8" will
keep looking right until the KB explains why both numbers exist. `pin-power-domains.yaml` should
carry **both layers, named and separated**: the silicon's 16×4 VIO/GIO domains (what
`P_ADC_GIO`/`P_ADC_VIO` reference, and what the multi-pin layout rule follows) and the Edge boards'
8×8 LDO groups (what the 300 mA budget follows), with the note that one Edge LDO feeds two silicon
domains. The ADC files then point at it rather than restating a number.

**Process consequence, and it is the durable half.** The class-wide-sweep rule did its job — F-211
swept five files consistently. What no rule caught is that the *fact being swept* was wrong, so the
sweep propagated it faster and further. **A class-wide sweep amplifies whatever it starts with**, and
the grounding step therefore has to be *stronger* than for a single-site fix, not the same. Two
concrete gates this argues for: **(1)** a source that is a *board* document can never establish a
*silicon* fact — check the tier of the artifact, not just its trustworthiness; **(2)** "the primary
source is silent" is not a conclusion until the figures have been opened, per
[[feedback_exhaust_resources_at_hand_first]] and [[feedback_reverify_source_silent_before_expert]].

**Status:** `CONFIRMED`. Remediation is a **scope decision for Stephen** — it reverses a published KB
correction and touches a released app note, so it is deliberately not folded into Sprint 2 unasked.

---

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

### F-270 — `p2an001-…-adc.yaml`'s SINC2 tip carries the sampling-mode restriction into filtering mode, contradicting the correction P2AN001 v1.0.2 already shipped. `DONE (2026-08-16)`

**Surfaced by:** «#239»'s owed step 4 — *"confirm no OTHER P2AN001 site carries the old grouping."*
The power-domain line in the companion was already correct; reading its neighbours found this.

**The defect.** `deliverables/ai/P2/application-notes/p2an001-single-pin-instrumentation-adc.yaml:105`
carries, as a `tip`: *"Keep the SINC2 sample period a power of two (period = 2^X[3:0]); the builds
use 128 (%0111)."* The note's builds run **SINC2 filtering** mode, where that restriction **does not
apply** — and P2AN001 corrected exactly this in **v1.0.2** (2026-07-11), which the document and its
CHANGELOG both record. The correction was never propagated into the companion YAML, so the two
halves of the same released deliverable now say opposite things.

**Authority — Silicon Doc, read directly** (`sources/silicon-doc/p2-documentation.txt:8421-8425`),
verbatim: *"For modes other than SINC2 Sampling (X[5:4] > %00), WYPIN may be used after WXPIN to
override the initial period established by X[3:0] and replace it with the arbitrary value in
Y[13:0]. … The smart pin accumulators are 27 bits wide. This allows … up to 2^(27/2), or 11,585,
clocks in SINC2 filtering mode."* So: the power-of-two form is the **initial** period only, it is
overridable in every mode except SINC2 Sampling, and the filtering ceiling is 11,585 clocks — an
arbitrary value, not a power of two.

**Why it matters more than a stale tip.** An agent reading the companion gets a **false constraint**
and will refuse or round a legal period; the document it accompanies says the opposite on the same
page of the same release. A companion that contradicts its note is worse than a companion that omits
the point — it spends the note's credibility.

**Class sweep — DONE, and it is single-site.** Every other "power of two" period statement in the
tree is correctly scoped: `manuals/p2-io-and-smart-pins-user-guide/…/chapter-16-adc.md:601` says
*"In SINC2 **sampling** mode the period must be a power of two"* — correct as written;
`pasm2/getxacc.yaml:56`'s power-of-two guidance is the **Goertzel/SETXFRQ iteration-count**
constraint, an unrelated fact and correct. **No sweep beyond the one line.**

**The process point.** The v1.0.2 pass fixed the document and stopped. **A correction to an app note
is not complete until its YAML companion carries it** — the companion is half the deliverable and
ships under the same version. This belongs in the app-note correction checklist, not just in this
entry.

**Remediation:** rewrite `:105` to state the mechanism rather than a prohibition — `X[3:0]` sets a
power-of-two **initial** period (the builds use 128, `%0111`), and a `WYPIN` after the `WXPIN`
replaces it with any period up to 11,585 clocks in SINC2 filtering; the power-of-two restriction is
SINC2 **Sampling** mode only.

**Status:** `DONE (2026-08-16)`. **Stephen chose to fold it into v1.16.3** rather than spend a
v1.16.4 cycle — the bump was committed but not yet tagged, so it was the cheapest moment available.
Applied at `:105`, `Fixed` entry added to the v1.16.3 CHANGELOG, recorded in the
`YAML-HEAD-DASHBOARD` release row, index regenerated on top of the content commit, validators
re-run green.

**Survey note, stated rather than left implied:** folding added a file to v1.16.3's delta *after*
the YAML→manual impact survey had run. The added file is an app-note **companion**, and no manual
declares a companion as a source — companions derive from their note, not the reverse — so the
survey's conclusions are unchanged. Re-checked, not assumed.

---

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

### F-272 — the `%TT` setting for a DAC pin the STREAMER writes is not stated by any source we hold. `OPEN — question, not a defect claim`

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

**Status:** `OPEN`. Not a defect claim against any current text — the manual no longer makes the
claim in either direction.

---

## ROOT CAUSE of the XBYTE `_RET_ CALL` defect — the KB dropped a qualifier (2026-08-16) — F-273

### F-273 — `_RET_` returns **only if the instruction did not branch**. The KB documented it as an unconditional "Always + Return", and a manual built on that shipped a broken idiom. `DONE (2026-08-16) — KB v1.16.4 + XBYTE manual half applied («#227»)`

**This entry supersedes the framing in F-256/EF-058.** Those treated `_RET_ CALL` as a *hardware*
finding discovered on the bench. It is not. **It is documented Parallax behaviour that our KB failed
to carry**, and the bench merely re-observed the specification.

### The rule, from two independent Parallax primary sources

| Source | Wording |
|---|---|
| **P2 Assembly Language Manual** (Parallax, 2022-11-01), condition table **p.68** — stated twice (`pasm2-manual-narrative.txt:844`, `:3633`) | *"`_RET_`  `%0000`  **always; execute instruction then return if no branch**; no context restore"* |
| **P2 Instructions v35 – Rev B/C Silicon** spreadsheet, **row 410** (`p2-instructions-csv/…Sheet1.csv:434`), encoding `0000 ------- --- --------- ---------`, stack-effect column `Pop` | *"Execute `<inst>` always and return if no branch. **If `<inst>` is not branching then return by popping stack[19:0] into PC.**"* |

So `_RET_` is **not** "always execute and return." It is **execute, then return *only if the
instruction did not branch*.** `CALL` branches, so `_RET_ CALL` **never returns** — by
specification, not by malfunction. The prefix is architectural and says nothing about XBYTE.

### One rule explains every observation — no exceptions

| Site (EF-058 rig) | Branches? | Rule predicts | Observed |
|---|---|---|---|
| `_ret_ or tv, #0` | no | returns | handler returns, dispatch continues ✅ |
| `_ret_ setq #0` (XBYTE arming) | no | returns to `$1FF` | engine arms ✅ |
| `_ret_ call #helper` | **yes** | **no return**; callee returns to the next instruction | falls through into the following handler ✅ |
| `_RET_ SKIPF` (Silicon Doc `:1905`) | no | returns, pattern applies at the destination | documented as *"an automatic branch before skipping commences"* ✅ |

### The KB defect — what was wrong, and where

| File | Was | Now |
|---|---|---|
| `language/pasm2/concepts/conditional_execution.yaml` (the authoritative condition table) | `condition: "Always + Return"`, note *"Special: Always executes AND returns"* — **no branch qualifier** | the qualified rule, plus a new **`ret_prefix_rule:`** block (full semantics · the branch case · correct form · why it is silent · what it *does* work on · both sources) and a `common_mistakes` entry |
| `language/PASM2-ENCODING-REFERENCE.md` | `Always + Return`; *"always-execute + return"* | qualified table cell + a sourced callout under the condition table |
| `language/pasm2/call.yaml` | *"…or an instruction with a `_RET_` condition, to return…"* — true only for a non-branching instruction | qualified to **NON-BRANCHING**, plus a `ret_prefix_caveat:` naming the `_RET_ CALL` trap |
| `language/pasm2/ret.yaml` | no mention of the prefix form at all | `ret_prefix_form:` + `aliases:` + `related:` so a reader at RET finds it |
| `language/pasm2/concepts/manual_category_alignment_check.yaml` | *"`_RET_` **suffix**"*; **"PERFECT - Complete match"** | corrected to *prefix*; alignment restated honestly |

**Grep proof of the gap:** before this fix, *"if no branch"* appeared **zero times** in
`deliverables/ai/P2/`, while both Parallax sources state it.

### Why this is the finding that matters

**An author reading our KB was told the prefix "always executes AND returns."** Writing
`_RET_ CALL #set_nz` is the correct inference from that sentence. The XBYTE Guide's idiom is not a
careless mistake — it is the **predictable downstream consequence of a dropped qualifier**, and it
reached community review because every layer below it agreed with itself.

**The alignment check is the second lesson.** `manual_category_alignment_check.yaml` certified this
category *"PERFECT - Complete match"* — because it compared the **list of condition names**, which
was complete, and never compared the **semantics attached to them**. **Name coverage is not semantic
coverage.** A check that compares only names must say so rather than certify the category, or it
converts an unexamined area into a documented all-clear. Same failure shape as F-269's fan-out audit
and F-211's sweep: an artifact asserting correctness it never established.

### WE ALREADY FOUND THIS, IN JUNE — and half the fix landed

**The Assembly Language Manual's full audit of 2026-06-10 got the qualifier right, two months before
the bench run.** `audit/full-audit-2026-06-10/_ADJUDICATION-DETAIL.md:1532` adjudicates the
`%0000` / `IF_NEVER` confusion, concludes *"Do NOT edit the manual … Instead fix the SOURCE:
`PASM2-ENCODING-REFERENCE.md:49-52`"*, and prescribes the replacement text verbatim:

> *"`%0000` is the `_RET_` form (always-execute + **return-if-no-branch**); the assembler emits it
> only via the `_RET_` prefix. `%1111` is the default `IF_ALWAYS` …"*

It then says: **"Route to the P2KB corrections register."**

**Two things went wrong, and together they are the whole failure:**

1. **The fix was applied by halves.** The `IF_NEVER` clause landed in
   `PASM2-ENCODING-REFERENCE.md` — the note has read *"`%0000` is exclusively the `_RET_` prefix …
   it is NOT the encoding for `IF_NEVER`"* ever since. **The `return-if-no-branch` qualifier was
   dropped in transcription.** The half that mattered for correctness is the half that vanished.
2. **It was never filed in the register.** Grepping this file for `return-if-no-branch` or
   `IF_NEVER` returns **nothing**. With no entry, there was no record that a correction was owed,
   so nothing ever noticed that only part of it arrived.

So the qualifier was **found, written down correctly, routed — and lost**, and two months later a
guide under community review shipped `_RET_ CALL` because the KB it derives from no longer said it.
The bench then spent a rig, three build rounds and a day of Stephen's time re-discovering it.

**The durable rule this argues for:** *a correction is not routed until it is IN THE REGISTER.* An
adjudication that names the fix in an audit artifact and trusts the fix to be carried across by hand
has no closing gate — and a partially-applied correction is invisible precisely because the file
*did* change. If the register had carried this, the drain gate would have caught the missing half.
[[feedback_batch_and_verify_workflow]] · [[project_p2kb_corrections_register]].

*(The 2026-06-10 audit tree is gitignored working history, so its now-stale rows — e.g.
`part-iii-appendices-sourcing.md:56`, which records `_RET_ | %0000 | Always + Return | **VERIFIED**`
— are left as the record of what that pass concluded. The authority is here.)*

### Consequences for the other entries

- **F-256** — recast from `NEEDS-VERIFICATION`/hardware question to a **documentation** finding whose
  answer was in the ingested sources the whole time. **No further rig run is required** — not for
  generality outside XBYTE (the prefix is architectural) and not to confirm EF-058 (it can only
  re-observe the spec). The `[M-pre]` grade and the staged `DEBUG_COGS` re-run are **moot for the
  conclusion**.
- **EF-058** — its *"dispatch does not resume"* clause is **false** and is corrected there: the rig's
  own trail shows all four bytecodes dispatched, plus one spurious handler. The failure is **silent
  extra execution**, not a hang.
- **Manual halves owed:** the XBYTE Guide teaches this rule («#227» rework). The structural change
  already applied there — every `_RET_ CALL` replaced by `CALL` + `RET` — remains correct; only the
  *explanation* changes.

---

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

**Related, not fixed here:** pins 56/57 are also the Edge Module's onboard LED pins and the P56–P63
bank is the programming/WX-adapter header, so the chapter's example pin choice is worth a second look
on its own merits at IOSP's next pass. Any even/odd consecutive pair works.

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

### F-278 — wrong-code examples ship in ordinary syntax-highlighted blocks, distinguished only by a comment, in three manuals. `CONFIRMED`

**Locations (7 sites):** Streamer `streamer-body.md:1016` **(NOT RELEASED, v1.0.9)** · Debug Window
`ch12-bidirectional.md:66`, `:186` **(NOT RELEASED, v1.1.3)** · IOSP
`part-5-appendices/appendix-e-troubleshooting.md:98`, `:202`, `:278` and
`part-3-input-modes/chapter-17-serial-receive.md:172` **(RELEASED, v1.0.8)**.

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
editing a master is not releasing a document.

**IOSP RESOLVED 2026-08-17 («#246») — five sites, not four.** The four declared sites are converted.
A **fifth** turned up because this pass used the broader wrong-code pattern
(`WRONG|Wrong|INCORRECT|Do not do this`) rather than the `^' *WRONG` form that missed the Debug Window
blockquote: `part-2-output-modes/chapter-11-serial-transmit.md:174`, a `**Wrong:**`-labelled
```` ```spin2 ```` block already paired with its `**Correct:**` twin. **The narrow pattern under-counted
this finding in two manuals; the enumeration above is the floor, not the census.** Three of the IOSP
sites carried the wrong and correct forms in **one** block and were split the way Streamer's was —
```` ```antipattern ```` then ```` ```spin2 ```` — so the reader gets red-beside-green rather than two
comments in one box.

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

### F-281 — three code lines run off the page in the RELEASED Debug Window PDF, taking part of the program with them. `CONFIRMED` — **BLOCKS the v1.1.3 ship**

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

**fancyvrb ≥ 3.0 supports `breaklines=true` on `Verbatim`.** Adding it to the filter's Verbatim
options would convert silent truncation into visible wrapping **across the whole document set**, and
would make K a style budget rather than a correctness cliff. That is a platform change touching every
manual's rendering, so it wants a `forge-test` round-trip and a look at how existing long lines
re-flow — but it is a far better answer than re-authoring lines one at a time, and it protects
documents nobody has audited yet.

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

### F-282 — every `MANUAL-DESCRIPTOR.md` records a stale `last_published_tag`, so every diff-since-published audit reads the wrong baseline. `CONFIRMED`

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

### F-283 — the P2AN002 YAML companion disagrees with the note it ships beside, on both a measured pitfall and an attribution. `CONFIRMED` — **fails the app-note agreement gate**

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

### F-227 — un-backticked `PC_KEY`/`PC_MOUSE` inside a display message is sent to the window as **literal text**; the command never runs — `DONE (2026-07-26, compiler-proven)` · re-test pending

**Surfaced by Stephen's run-verification pass** over the Debug Window Manual's 34-program example
library on PNut/Windows: 30 ran, 4 failed. Three of the four are every example in the library that
uses `PC_KEY`/`PC_MOUSE` — a 3-of-3 hit rate on one construct.

**Root cause.** Everything following the display name in a backtick statement is *display text*. A
Spin2 debug command must tick back out of display text into command mode, exactly as `` `(expr) ``
does. All three examples omitted that second backtick. Proven with `pnut-ts -d` v1.55.0 by reading
the emitted display strings out of the two binaries:

| source | emitted display text |
|---|---|
| `` debug(`Adjust PC_KEY(@key)) `` | `` `Adjust PC_KEY(@key `` — the characters are transmitted to the window; **no command compiled** |
| `` debug(`Adjust `PC_KEY(@key)) `` | `` `Adjust `` + the real `PC_KEY` command bytes |

The pointer variable is therefore **never written**; the control loop polls forever and responds to
nothing. **No compile error** — same silent-failure class as double quotes in a display string
(`DEBUG-Statement-Quoting-Briefing`, §2). Uppercase after the tick compiles identically to the
lowercase form used in the bench-certified reference (`REF/robot-dog/test_dog_panel.spin2`:
`` DEBUG(`pnl `pc_key(@keyCode)) ``), which is what exposed the defect.

**Why it survived to release:** these three are the manual's only *interactive* examples. Their
figure-generator harnesses cannot be certified from a screenshot, and the 2026-07-11 run audit
accepted a structural argument in place of a hardware run. A structural contrast is only as good as
the idiom it is compared against — and the comparison against the dog-panel idiom was recorded as a
TODO and never performed.

- **KB fixed:** `debug-commands/pc_key.yaml`, `debug-commands/pc_mouse.yaml` — new `usage_rules`
  entry naming the silent failure, and both worked examples corrected. **Publishes on the next KB
  release rail (§9).**
- **Manual fixed:** examples `ch12-keyboard-adjust`, `ch12-mouse-pointer`, `ch15-control-panel` +
  their three `fig-*` harnesses; prose in `ch12-bidirectional.md` (the rule is now taught as rule 2
  of two, with the ✅/❌ contrast), `ch15-panels.md`, `appendix-a-command-reference.md`. Byte-identity
  across all 34 examples re-verified.
- **Also added (Stephen, from the dog panel):** ch15 now teaches the mouse-vs-artwork Y flip —
  drawn panels need none (draw and `PC_MOUSE` share PLOT space), BMP-authored panels need
  `py := (PANEL_H - 1) - py` because artwork is authored top-left. Bench-confirmed 2026-06-06 in
  `test_dog_panel.spin2:hitSlot()`.
- **Open:** the fourth failure (`ch14-scope-trace`, SCOPE window does not open) is **not** this
  defect and has no proven cause yet — see the note below.

**The fourth failure is a separate defect — see F-228.**

### F-228 — a display **named after a DEBUG keyword** is never declared; the window silently never opens — `DONE (2026-07-27, isolated on silicon)` · re-test pending

**Symptom** (Stephen, 2026-07-26/27, PNut/Windows): `ch14-scope-trace.spin2` opens its TERM
"Panel" window but **no SCOPE window**. The TERM create is issued *after* the SCOPE create, so the
program and the debug link are healthy — only the SCOPE create is rejected.

**Isolated by a six-way single-run probe** (`audit/verification-tests/probe-ch14-scope-create.spin2`),
built after a first pass produced an ambiguous count. Six SCOPE creates differing by one token
each; **A–E all opened, `Trace` did not**:

```spin2
debug(`SCOPE D     POS 0 0 SIZE 400 220 SAMPLES 256)   ' opened
debug(`SCOPE Trace POS 0 0 SIZE 400 220 SAMPLES 256)   ' did NOT open
```

Byte-identical apart from the name. `TRACE` is in the functional keyword vocabulary (SPECTRO/BITMAP
config). `parse_debug_string` classifies each element (`cmp al,dd_key`) before a name symbol can be
claimed, so a keyword token can never become a `dd_nam` — no display is declared, and every
`` `Trace … `` feed afterward addresses nothing. **No compile error.**

**Method note worth keeping.** The keyword hypothesis was raised early, then **correctly discarded**
when `figure-generators/screenshots/fig-14-scope-trace-scope_WDW.bmp` (2026-07-11) OCR'd as
*"Trace - SCOPE"* with channel "Signal" — a working window from this same create line. Only a
controlled probe *with a passing control* re-established it. Two runs, opposite results, same
source: the discriminator is which host rendered them (see the open question below), and neither
the screenshot nor the argument could settle it alone.

- **Fixed:** `ch14-scope-trace` display renamed `Trace` → `Scan` (example + opus-master code block +
  `fig-14-scope-trace.spin2`; SAVE filenames unchanged). Same class in prose: `` `PLOT Box `` in
  ch05 → `Canvas` (`BOX` is a PLOT shape directive).
- **Taught:** ch02 now carries the **complete five-part naming rule** with the silent-failure
  symptom; Appendix A points at it and states that the reserved set is wider than the appendix.
- **Definitive rules recorded (2026-07-27)** — Stephen commissioned an agent study of the **PNut
  v55** source and the result is now the citable reference:
  `manuals/p2-debug-window-manual/REF/DEBUG-WINDOW-NAME-RULES.md`. A name is legal iff: (1) leading
  letter/`_` then letters/digits/`_` — a leading digit parses as a *number* and aborts; (2) not one
  of the **103** reserved display words (`debug_symbols`, `p2com.asm:19335`) = 9 types + 11 colors
  (**`GREY` and `GRAY`**) + 19 color modes + 12 packed modes + 52 directives; (3) not a currently
  open display's name — freed and reusable after `CLOSE`; (4) **case-insensitive** matching, with
  original casing kept for display; (5) truncated at **30** characters, so shared 30-char prefixes
  collide. Mirrored into `statements/debug.yaml` `window_name_rules` (full 103 enumerated for code
  generation; count-verified).
- **Re-sweep against the full 103** (the earlier sweep used only the directive subset — it omitted
  the nine display types and `GREY`): across all 34 examples, the opus-master snippets, the figure
  generators and the probe, the only hits remain `Trace` and `Box`, both already fixed. No name
  exceeds 30 characters or starts with a digit.
- **Scope (Stephen, 2026-07-27) — two independent vocabularies, only one collides.** Spin2's
  reserved words are irrelevant: the compiler emits the display name as raw text and never
  interprets it. `ch05-plot-field.spin2` names a PLOT window `Field` — `FIELD` is a Spin2 keyword
  (the `FIELD[ptr]` alias, v37+) — and it runs correctly on his bench. Only the **host display
  parser's** directive vocabulary can collide. ch02 teaches the contrast with both examples.
- **Library sweep:** all display names across the 34 examples, the opus-master snippets and the
  figure generators were checked against the full keyword vocabulary — `Trace` and `Box` were the
  only two collisions, and both are fixed.

**Host divergence — Stephen's to carry (2026-07-27).** The Jul-11 capture proves this create line
rendered a window *then*, so a host accepted what PNut v55 rejects; the likely split is
`pnut_term_ts` (figure run) vs. PNut (the 2026-07-26 run). Per the standing rule (PNut is ground
truth, term-ts mirrors) that would be a term-ts repair item. **Stephen is handling it directly** —
no action or report from the doc side. The manual and KB fixes above stand regardless of which
host is at fault, because a keyword-named display is invalid against ground truth.

**Re-tested and closed (Stephen, 2026-07-27): the full 34-program example library runs under
PNut v55.** Ships in Debug Window Manual **v1.1.1** (released 2026-07-27) and KB **v1.15.0**.

**YAML→Manual impact survey (KB v1.15.0, release-yamls §8).** The delta (10 files: `pc_key`,
`pc_mouse`, `statements/debug`, 7 `debug-displays/*`) was intersected against every live manual's
`MANUAL-DESCRIPTOR.md` declared sources. **Two intersections, neither needing a re-audit flag:**
- `p2-debug-window-manual` — the consuming manual, whose twin **shipped simultaneously** (v1.1.1);
  it is the source of the delta, not a document lagging behind it.
- `pnut-term-ts-user-guide` — its descriptor declares an explicit **scope boundary** ("do NOT
  reproduce the `debug()` directive syntax … cross-reference only"), and it is an undrafted v0.1.0
  with no content, so nothing can be behind HEAD. No flag.

No other live manual declares these sources. Survey done, not skipped.

## Forum docs-feedback sweep (2026-08-14) — F-254…F-258

**Origin:** Parallax forum posts #104–#117 (2026-08-12/13), reviewing the deSilva tutorial, the
XBYTE Programming Guide, and the P2 Architect's Guide. Full analysis (with the tone/positioning
items that are *not* defects) lives at
`engineering/document-production/FORUM-NO-COMMMIT/Docs-findings-360813/DOCS-FINDINGS-ANALYSIS.md`
(gitignored — find it by path). Forum posts are the **lead**; every finding below was verified
against the live opus-master, `pnut-ts` 1.55.3, or P2KB before filing.

### F-254 — deSilva Acknowledgments: the author is listed among the "giants," reviewers are credited generically, and an AI claim is false. `DONE (2026-08-16) — applied in deSilva, ships in v3.0.6`

**Location:** `manuals/p2-pasm-desilva-style/opus-master/COMPLETE-OPUS-MASTER.md:113–160`.
**This is in a SHIPPED document (v3.0.5).** Three distinct defects in one block:

1. **Self-listing.** The section opens *"This manual stands on the shoulders of giants. We
   gratefully acknowledge:"* → `### Primary Contributors` → deSilva, **Iron Sheep Productions LLC
   (Stephen M Moraco)**, Chip Gracey. Structurally the text declares the giants and then lists the
   author among them. Raised by Christof Eb. (#109): *"Newton bows to other great scientists and
   makes himself small; Stephen has styled himself to be a giant here."* The idiom itself is
   canonical (AJL, #105, is right about that) — the defect is which side of it the author sits on.
   The Newton quote also appears **twice** (paraphrase at `:113`, quotation at `:154`).
2. **Unearned reviewer credit.** `### Technical Reviewers` — *"Special thanks to those who reviewed
   drafts, tested code examples, and provided invaluable feedback"* — lists only generic
   placeholders: *"The P2 Documentation Team at Parallax"*, *"Community members who beta-tested
   examples"*, *"Everyone who reported errors."* **No named person.** If that review did not occur
   as described, this claims a validation process we did not run — a trust-chain defect, not a
   style one.
3. **False factual claim.** *Production Notes* states the manual used *"AI-assisted content
   generation **trained on** deSilva's writing style."* **Nothing was trained.** The accurate
   statement is AI-assisted authorship *in the style of* deSilva's P1 tutorial, with every example
   compiled. Precision matters especially here — the same thread carries hostility about
   AI-generated content.

Also present and low-value: an `### Inspiration` block crediting the MIT AI Lab, Donald Knuth, and
the Demoscene, none of whom contributed to this work.

**Proposed correction** (essentially evanh's advice, #106 — *"delete the whole line, and the
'Primary Contributors' line too. Keep it formal. 'Acknowledgements' is all that's needed"*):
drop the giants opener and the closing Newton quote; drop the `Primary Contributors` heading;
**remove Iron Sheep / Stephen Moraco from the acknowledgments entirely** (the author belongs on the
title page); delete the Technical Reviewers block **unless real named reviewers can replace it**;
delete the Inspiration block; correct or delete the "trained on" sentence.

**Class-wide sweep — DONE TWICE, and the result is good news: this is ISOLATED to deSilva.**
The first pass swept deSilva's *wording*; the second swept the four *defect classes* independently,
across every manual and app-note opus-master, because matching strings is not the same as matching
the defect:

| Defect class | Swept for | Result |
|---|---|---|
| **Self-listing in acknowledgments** | `Iron Sheep`/`Moraco` outside copyright/trademark context | **deSilva `:119` only.** Every other hit is the cover byline `{\small Iron Sheep Productions, LLC\par}` (correct) or, in XBYTE `front-matter.md:153`, a *Sources* citation of our own P2KB YAML — honest provenance, not a thank-you. |
| **Unnamed / unearned reviewer credit** | `those who`, `beta.test`, `reviewers`, `reviewed drafts`, `tested code`, `everyone who`, `special thanks` | **deSilva `:129–135` only.** |
| **False AI-provenance claim** | `ai-assisted`, `ai-generated`, `trained on`, `LLM`, `large language model` | **deSilva `:150` only.** The Assembly Manual `front-matter.md:316` ("a format suited to both human reading and AI-assisted development") describes the *audience and format*, not how the text was produced — accurate, **leave it alone**. |
| **Padding credits** (parties with no connection to the work) | manual read of every acknowledgments block | **deSilva only** (MIT AI Lab, Knuth, Demoscene). |

**App-notes P2AN001–P2AN007 carry no acknowledgments section at all** — clean by absence.

All live manuals are already clean, formal, and correct —
Architect's, Assembly, XBYTE, IOSP, Getting Started, Debug Window, Streamer all credit Parallax,
Chip Gracey, the P2 community (and IOSP additionally Jon Titus) with no self-listing, no giants
line, no generic reviewer credits, no AI claim. deSilva is the **outlier**, consistent with it
being the oldest of the set — written before the house convention settled. Two further copies of the
text exist inside deSilva's own folder and are **inert** (not assembled into the render):
`opus-master/archived-2025/COMBINED-COMPLETE-MASTER.md` and
`initial-chapter-generation/00-acknowledgments.md`.

> **Sweep scope:** the **live set only** (roster Done / In progress / Upcoming). Roster-Abandoned
> documents are excluded from the search itself and are not reported on.

### F-255 — XBYTE §15.3: `set_nz` is never defined, and the contract shown cannot work. `DONE (2026-08-16) — applied in XBYTE («#227»), ships in v1.0.2`

**Location:** `manuals/p2-xbyte-programming-guide/opus-master/xbyte-body.md:1388–1401`
(Christof's "page 66"). Guide is **in community review**.

Two representative handlers end with `_ret_ call #set_nz` — `op_lda_imm` after loading `a`, and
`op_inx` after incrementing `x`. **`set_nz` is never defined anywhere in the manual** (it appears
only at these two call sites plus prose mentions at `:879` and `:1293`). Worse than missing:
`:1293` asserts *"A single shared `set_nz` helper serves most of the instruction set,"* but the two
call sites require flags from **different registers** and the helper takes **no operand** — no
shared result register, no calling convention, nothing. As written the pattern cannot do what the
text claims. Christof's objection (*"how should that routine guess from what it could set the Z
flag?"*) is correct and unanswerable.

**Second defect, same section:** §15.3's closing paragraph credits the handlers with *"each
opcode's table entry supplying the SKIPF pattern"* — but **none of the three handlers shown carries
a skip pattern**. The examples do not demonstrate the mechanism the prose attributes to them.
(Christof: *"There is no skip pattern."*)

**Proposed correction:** define `set_nz` and make its calling convention explicit (shared result
register, or an operand), show at least one handler family with real skip patterns, and **compile
the slice**.

**Scope check — deliberately NOT inflated.** A sweep of every `call`/`jmp` target inside the
guide's PASM2 blocks found **12 of 13 undefined as labels** (`pop_two`, `push_a`, `push_value`,
`read_opcode`, `hub_write_port`, `next_op`, `idle`, `int_ignore`, `odd_variant`, `special_case`,
`voice_on`, `set_nz`). **Only `set_nz` is a defect.** The others are legitimate illustrative
stand-ins whose names fully convey their job and whose internals are irrelevant to the lesson.
`set_nz` differs because the *surrounding text makes a claim about the helper's shareability* — its
contract is load-bearing, so it cannot be a stand-in. **Do not "fix" the other eleven.**
Corroborating the guide is not broadly broken: the complete VM in §12.2 (`xbyte-body.md:975–1044`)
was extracted and **compiles clean** under `pnut-ts -q`.

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

### F-257 — deSilva Appendix A platform comparison omits the current competitor and the axis where we are weakest. `DONE (2026-08-16) — applied in deSilva, ships in v3.0.6`

**Location:** `COMPLETE-OPUS-MASTER.md:5876+`. **SHIPPED document.** Raised by Christof (#111).

- **RP2040/RP2350 (Raspberry Pi Pico 2 / 2 W) is absent.** The table lists STM32, ESP32,
  Arduino/AVR, PIC32, P2. The RP2350 is the current default for a large share of hobby projects and
  its PIO is the nearest real competitor to the P2's pin-level story. Omitting it reads as
  avoidance.
- **The comparison is hardware-only.** It compares cores, peripheral location, and timing, and
  never mentions **libraries, ecosystem, or language** — Arduino/ESP-IDF/MicroPython versus having
  to learn Spin2 + PASM2 is for many readers *the* deciding factor. A comparison that omits the
  axis where we are weakest invites the "marketing leaflet" charge Christof levels.
- **Pricing** (Edge modules) is unmentioned; independently echoed by evanh in a separate thread.

**Proposed correction — fix, do not delete.** Add the RP2350 row; add a software/ecosystem
dimension that states plainly where the P2 loses; keep the technical claims, which are accurate and
already properly hedged (the "2 clocks" passage correctly calls itself a lower bound). Consider
adopting Christof's own framing of the P2's strength, which is sharper than ours and comes from a
critic: *"the probability to succeed in a project is higher, because you can always fall back to
dedicate a core to some time critical part — much more easy than working with interrupts."*

### F-258 — XBYTE's fitness for vintage-CPU emulation, raised by Wuerfel_21 (#112). `RESOLVED-INVALID` — the guide already argues this position, using Wuerfel_21's own projects as its evidence

> **Entry written 2026-08-17, three days after the fact it records.** F-258 was cited as resolved
> in the sprint plan and the analysis doc, and the section header above counts it — but **no entry
> was ever filed here.** A conclusion asserted in two planning documents and absent from the
> register is not routed, and this one is load-bearing: it is the stated reason a community member's
> detailed technical argument produced no change. Filed now, with every citation re-verified against
> the live master rather than carried from the analysis doc.

**The claim (#112):** XBYTE suits constructed bytecode machines, not vintage CPUs, because it
allows no common code between handlers — which virtual interrupts and cycle-precise timing require.
Cites MisoYume's per-instruction event checks; calls Chip's Space Invaders a hack that works only
because its single VBlank interrupt is not timing-critical.

**Verified against `xbyte-body.md` at HEAD (2026-08-17) — the guide reaches the same conclusion:**

| Where | What it says |
|---|---|
| `:100` | the book is behaviour-accurate, "not cycle-accurate, and that is a deliberate choice" |
| `:1203` | "Cycle-accurate timing, interrupt polling, bus sharing, refresh registers, tracing. If the answer is 'a lot,' you want a loop body, and **XBYTE takes it away. Stop at rung 2.**" |
| `:1225` | the 6502 capstone is named "a teaching artifact" |
| `:1875` | an entire section — **§18.7 "When XBYTE is the wrong tool"** |
| `:2081` | **Appendix C.4** is devoted to the Yume suite, credited to **wuerfel\_21** by name, with the IRQsome GitHub organization and the SourceHut mirror |
| `:2089` | "**These use no XBYTE at all** — the appendix's sharpest illustration that instruction shape does not decide the rung" |
| `:2091` | "the 65816 is byte-stream and opcode-first — by instruction shape the *ideal* XBYTE guest — and it takes rung 2 anyway" |

So the guide does not merely concede the boundary; it **builds its case on this poster's work and
credits it by name.** TonyB\_ (#116) confirms the same from the opposite side of the technical
argument — *"XBYTE is not always the right option **as the manual says more than once**"* — which
is independent evidence that a reader who works through the book does find it.

**Therefore: no content defect. Do not rewrite the framing.** Filed `RESOLVED-INVALID` so this is
not re-opened off the thread.

**What it does prove** is that the framing is **not reaching readers who sample the book rather
than work through it**. That is a findability problem, and it belongs with the findability item
Christof raised (#110) — not to the technical content.

**One genuinely open suggestion from the same post, not a defect and not yet queued:** a
**Brainfuck interpreter** as the guide's worked example — unambiguously a constructed bytecode
machine, and far less rope than a 6502 slice. Unactioned; no owner.

**Do not cite this thread as authority.** TonyB\_'s "XBYTE was designed for the Z80 in particular…
via the forum and behind-the-scenes" is a design-intent claim with no traceable source. If the
manual's framing ever needs it, it is a **question for Chip**, not a citation.

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

### F-259 — REVISED: the guide's DAC recipe is CORRECT. The real defect is composing pin constants with `+`. `DONE (2026-08-16) — KB + manual half both applied («#218», «#220»)`

> **KB APPLIED 2026-08-16 («#218»).** The house rule is now **stated once**, in
> `architecture/smart_pins.yaml` → `configuration_format.composition_rule`: combine pin-mode
> constants with `|`, never `+`; why (they are bit fields, not additive flags, and same-group names
> share bits); the worked `P_CHANNEL | P_OE` vs `P_CHANNEL + P_OE` contrast with the measured
> 6,737-vs-1,407 counts; and the "three names, one bit" note for readers meeting all three in the
> symbol list. `language/spin2/methods/wrpin.yaml` gains a `one_bit_three_names:` line that **points
> at** that rule rather than restating it. Source trace: Spin2 v55 symbol table group *"DIR/OUT
> Control (pick one)"* + EF-054.
> **MANUAL HALF APPLIED 2026-08-16 («#220») — uncommitted under the «#234» gate.** Verified in a
> coverage audit: the `+` sites are gone and §13.4 now carries a *Combine pin-mode constants with
> `|`, never `+`* subsection that teaches the field, the three context names for one bit, and the
> measured 6,737-vs-1,407 silent failure. The one remaining `+` in the file is the **deliberate
> labelled wrong-example** inside that teaching block — protected; do not "fix" it.
>
> ~~Still owed (manual head, «#220»): the two `+` sites at `streamer-body.md:1238`, `:1306`, and~~
> the prose statement of the rule derived from the KB entry above.

> **REVISED 2026-08-14 after running it on our own board. The community report is NOT reproduced,
> and the original filing above was wrong to accept it.** Bench: P2 Edge, 200 MHz, jumper P0→P1
> (continuity verified digitally before measuring).

**What the silicon says.** Sweeping the TT field with the DAC driven to full scale by `SETDACS`:

| Configuration | ADC counts |
|---|---|
| `TT=%00` (no drive) | 1,408 |
| **`TT=%01` (`P_CHANNEL`) — the guide's recipe** | **6,733 — DRIVES** |
| `TT=%10` (`P_BITDAC`) | 1,406 |
| `TT=%11` | 1,406 |
| `TT=%01`, OUT=1 | 6,735 (OUT is irrelevant) |
| **`P_CHANNEL + P_OE` composed with `+`** | **1,406 — DEAD** |

So `wrpin ##P_DAC_124R_3V + P_CHANNEL` **works as published**. The reporter's claim that it "leaves
the pin at ground" does not reproduce.

**Why his bench disagreed — the source explains it.** Spin2 v55's symbol table lists, under a group
headed **"DIR/OUT Control (pick one)"**:

```
%..._01_00000_0  P_TT_01
%..._01_00000_0  P_OE        Enable output in smart pin mode, regardless of DIR
%..._01_00000_0  P_CHANNEL   Enable DAC channel in non-smart pin DAC mode
%..._10_00000_0  P_BITDAC
```

**`P_OE` and `P_CHANNEL` are the identical bit** — two names for `TT=%01`, chosen by context.
They are not additive flags; they are one *field*. Consequently `P_CHANNEL + P_OE` = `%01 + %01`
= **`%10` = `P_BITDAC`** — a different mode, which our bench shows is dead (1,406). The reporter's
own rows (*"TT=%10/%11 any → ground"*) match ours exactly; his **interpretation** — that `P_OE` is
required — is what is wrong. He was comparing `%01` against `%10`, not "without OE" against
"with OE".

**THE ACTUAL DEFECT: `+` composition.** With `|`, combining two names from one field is idempotent
and harmless. With `+` it **silently carries into a neighbouring mode**. Class-wide sweep of smart-pin
configuration lines (`WRPIN`/`PINSTART`) across every live manual, app-note, and the KB YAML:

| Operator | Config lines |
|---|---|
| `\|` | **281** |
| `+` | **2 — both in the Streamer Guide** |

- `streamer-body.md:1238` — `wrpin ##P_TRANSITION + P_OE, #spi_clk`
- `streamer-body.md:1306` — `wrpin ##P_DAC_124R_3V + P_CHANNEL, dac_pins`

Both **produce correct values today** (their terms are in disjoint fields, so `+` == `|` there), so
this is a latent trap rather than a live bug — but it is the trap that produced a public bug report
against us, because the moment a reader adds a second term from the same field the mode silently
changes.

**Proposed correction.**
1. Change both Streamer Guide lines to `|`, matching the 281 lines everywhere else.
2. State the house rule where readers will meet it: **compose pin/mode constants with `|`, never
   `+`** — the fields are "pick one", and `+` carries.
3. Add a note that **`P_OE` and `P_CHANNEL` are the same bit** (smart-pin vs non-smart-pin DAC
   naming), so "add `P_OE` as well" is at best redundant and, with `+`, destructive.
4. Re-examine `wrpin.yaml:49`'s `p_oe_required_for` listing DAC: correct in substance, but for the
   cog-DAC path the bit's name is `P_CHANNEL`, and the phrasing invites exactly the mistake above.

**Note for F-245's class:** that sweep's "add `P_OE`" remedy is right for *smart-pin output modes*.
It must **not** be applied mechanically to non-smart-pin cog-DAC configuration, where the same bit
is `P_CHANNEL` and adding a second name for it with `+` breaks the mode.

### F-260 — Streamer §17.1 DDS/Goertzel: the mode WORKS; the guide's text is the whole defect, plus a protocol it never states. `DONE (2026-08-16) — KB + manual half both applied («#218», «#221»)`

> **KB APPLIED 2026-08-16 («#218»), and the MECHANISM IS NOW SOURCED — it is no longer an
> inference.** Silicon Doc `p2-documentation.txt:4096-4099`, read live and quoted here because it
> settles what the bench could only bound: *"both accumulators can be simultaneously captured into
> holding registers and cleared using the GETXACC instruction … Subsequent GETXACC instructions will
> return the same values until a new streamer command executes."* Corroborated by the Silicon Doc's
> own worked demo, whose read is commented *"get prior Goertzel acc's"* (`:4252`).
> That single rule accounts for every EF-056 observation without over-reaching: the accumulators
> **are** cleared, and the **holding register** is what persists — so the earlier "never zeroed"
> framing stays retired, and the `XINIT`-vs-`XCONT` question it raised is dissolved rather than
> asserted.
> **Landed:** `language/pasm2/getxacc.yaml` — `description` rewritten to lead with capture-into-
> holding-registers + the repeat-read rule; new `reading_protocol:` (one GETXACC per streamer
> command; read-before/read-after and take the difference in the discrete pattern; the failure is
> invisible because the value returned is large, stable and plausible); `notes:` corrected; the
> untraced `documentation_source: original` replaced with the Silicon Doc citation; `see_also:` added
> for findability. `architecture/streamer/dds-goertzel.yaml` — `reading_results` gains the four-step
> capture semantics + `holding_register_protocol:`.
> **MANUAL HALF APPLIED 2026-08-16 («#221») — uncommitted under the «#234» gate.** Verified in a
> coverage audit: §17.1 carries the four-pin-block correction, the raw-ADC-pin rule (mode `%00000`,
> no `DIRH` on the ADC pins), the gain-is-coupling note, and **Reading the result: one `GETXACC`
> per command** — the holding-register semantics and the read-before/read-after difference
> protocol, stated as a protocol rather than as a mechanism, per the finding's own constraint.

**Location:** `streamer-body.md:1324`, `:607`, `:990`. **RELEASED.**

> **Rewritten in place 2026-08-15.** This entry previously read `NEEDS-VERIFICATION (silicon)` and a
> second F-260 entry carrying the bench result had been appended ~100 lines below, so the register
> held two contradictory verdicts for one finding. One finding, one entry: the heading above is now
> the current verdict and the bench data is retained below as **evidence**, not as a second finding.
>
> **The silicon question is settled: the mode works and is sharply frequency-selective** — 411:1
> against a 2× detune, 3,700:1 against 0.5×, 2,460:1 null, with ADC density measured per row so no
> row can misreport its own input. **Do not present this mode as unbuildable.**
>
> **One correction to what the appended entry claimed.** It stated as measured fact that *"the
> Goertzel accumulators are never zeroed."* That is an over-reach and it is **not** the finding.
> What was measured, under a discrete `XINIT` → `WAITXFI` → `GETXACC` sequence: a fresh cog's first
> read equalled the previous cog's last read five times across `COGINIT`, and two identical commands
> returned exactly twice one command's total. Chip's shipped demo reads once per command in an
> `XCONT` loop and plots a live position — if nothing ever reset, his readings would ramp without
> bound, and they do not. **Author the protocol, never the mechanism:** read before the command,
> read after, take the difference. Which of `XINIT` vs `XCONT`, the wait, or the cog lifecycle
> accounts for the difference is **not established** and must not be asserted.
> Full graded write-up: `campaigns/2026-08-manual-corrections/BENCH-FINDINGS-FOR-AUTHORING.md` Test 5.

Two **confirmed documentation defects**, both verified in source:

1. **`:1324` — `xcont dds_cmd, dds_s`. `dds_s` is never declared.** It appears exactly once in the
   entire guide. The example cannot be assembled as printed.
2. **The ADC-pin field contradicts itself.** `:607` (`add cmd, ##adc_pin<<17 + 1024`) and `:990`
   (`mode := X_DDS_GOERTZEL_SINC1 | X_DACS_0N0_0N0 + adc_pin<<17 + cycles`) place the ADC pin at
   `<<17`, which **collides with the required config bits `%111` in D[18:16]**.

**Plus an unresolved silicon question.** With the pin path proven good by `SETDACS` (F-259), the
reporter built the command exactly per the guide and Assembly App. G — it runs (`WAITXFI` completes
on schedule) but **drives no DAC and accumulates nothing**. Swept without success: `%dddd` ∈
{1,2,4,8}, D[19] 0/1, D[23] set, accumulators read mid-run and after `WAITXFI`.

Three questions the guide must answer and currently cannot:
- exact `XINIT`/`XCONT` **S-operand semantics** for this mode;
- which field enumerates the **summed ADC pin(s)** ("m = ±1 per selected ADC pin, −3..+3");
- whether anything beyond the command word must be armed (`SETCMOD`? DAC channel enables?).

**Action:** fix the two doc defects now. The silicon behavior needs our own bench and, if it stays
unresolved, becomes a **question for Chip** (`DRAFTS/QUESTIONS-FOR-CHIP-GRACEY.md`). Until settled,
the guide should not present this mode as buildable. A verbatim, compile-tested, silicon-run
example would close all three questions at once.

### F-261 — REVERSED: the IOSP Guide's "groups of four" is CORRECT. The defect is ours, in the KB. `RESOLVED-INVALID (2026-08-16) — superseded by F-269`

> **REWRITTEN IN PLACE 2026-08-16.** This entry accepted **F-211**'s verdict and asked for three
> repairs to `chapter-16-adc.md:263` and `:382`. Grounding the numbers against the **domain
> authority** instead of F-211's summary text — which is what «#219» was written to require —
> shows the manual is **right** and F-211 is **wrong**. All three repairs would have INTRODUCED
> defects into correct released text, including the third: *"pins 40–47 — two full groups
> (40–43, 44–47)"* is exactly correct under four-pin groups.
>
> The reporter's observation stands — we **do** contradict ourselves, P2AN001 versus IOSP — but the
> contradiction resolves the other way. **The full evidence and the real blast radius are in
> F-269.** Nothing is owed against the IOSP manual for this finding.

**Location (for the record):** `manuals/p2-io-and-smart-pins-user-guide/opus-master/part-3-input-modes/chapter-16-adc.md:263`
and `:382`. **RELEASED — and correct as shipped**, including its citation *"(P2 datasheet, pin
descriptions)"*, which matches the source.

### F-262 — Debug Window Manual: the FFT chapter never states channel-definition defaults that the SCOPE chapter does. `DONE (2026-08-16) — manual applied, ships in v1.1.3`

**Location:** `manuals/p2-debug-window-manual/opus-master/ch09-fft.md` vs `ch07-scope.md:86`.
**RELEASED.**

> **APPLIED 2026-08-16 («#229») — uncommitted under the «#234» gate.** `ch09-fft.md`'s
> channel-declaration table gains an **`If omitted`** column, and the omission *rule* is stated in
> prose beneath it.
>
> **The PNut-observation requirement is discharged from source, and no bench or PNut-on-Windows run
> is owed.** The grounding is `p2-debug-window-manual/REF/theory-of-operations/FFT_Theory_of_Operations.md`
> — a Theory-of-Operations analysis of PNut v55's own Pascal (`DebugDisplayUnit.pas`, `DebugUnit.pas`,
> `SerialUnit.pas`, `GlobalUnit.pas`), living inside this manual's own `REF/` tree. **The Pascal *is*
> PNut**, so the code is upstream of any observation of it: running the window would show one
> rendered outcome, whereas the channel-init block states the defaults for all eight channels
> outright (`FFT_Theory_of_Operations.md:393-401`, quoting `DebugDisplayUnit.pas` 1607-1614).
> Defaults: `mag`=0 · `high`=`$7FFFFFFF` · `tall`=`vHeight` (the plot area, 256 px unless `SIZE`
> changes it) · `base`=0 · `grid`=0 · `color`= the shared `DefaultScopeColors` palette entry for that
> channel (`:3104-3119`).
>
> **The "verify, don't assume" instruction earned its keep — the proposed correction below would have
> shipped a wrong table.** FFT and SCOPE do not share a signature: SCOPE takes
> `'label' (AUTO | lo hi) {tall} {base} {grid} {color}`, FFT takes
> `'label' {mag {high {tall {base {grid {color}}}}}}`. Copying SCOPE's column verbatim would have
> introduced an `AUTO` keyword and an `lo` bound that FFT does not have, and dropped `mag`, which
> SCOPE does not have.
>
> **Second fact, not in the original filing, and probably the more useful half:** omission is a
> **positional abort**, not per-argument defaulting. Each parse step is
> `if not KeyVal(…) then Continue` (`:593-599`), so the *first* absent argument ends the scan and
> every later argument keeps its default — you cannot skip one to reach a later one. SCOPE's
> companion doc states the same rule (`SCOPE_Theory_of_Operations.md:415`, `:720`). This is a
> credible mechanism for the **pnut-term-ts strict-parser divergence** the reporter filed separately
> (`pnut-term-ts-fft-channeldef.md`): a strict and a lenient parser will disagree precisely on
> partial argument lists. Recorded as mechanism, not as a diagnosis of that filing — we have not
> examined it.

`ch07-scope.md:86` gives a proper `| Argument | Meaning | **If omitted** |` table. `ch09-fft.md` has
no "If omitted" column anywhere — its `:73` table gives defaults for *keywords* (`TEXTSIZE` etc.)
but never for the **channel-definition arguments** (`high`/`tall`). The manual says the arguments
are optional and then does not say what happens when they are omitted, so an implementer must guess.

The reporter identifies this as the plausible cause of a **pnut-term-ts strict-parser divergence**
he field-reported separately — i.e. this gap has already produced a real tool disagreement.

**Proposed correction:** copy SCOPE's "If omitted" column into the FFT chapter's channel-definition
table. **Verify the values against PNut** (ground truth) rather than assuming FFT matches SCOPE.

### F-263 — CONFIRMED with the cause identified: hub access inside a CORDIC loop loses results. Chip's model is correct. `DONE (2026-08-16) — KB + both documents applied`

> **KB APPLIED 2026-08-16 («#218»).** `architecture/cordic.yaml` →
> `critical_usage_pattern.keep_hub_access_out_of_both_loops`: the rule, why it matters (the failure
> is silent — wrong numbers, not missing ones), the measured arm table (RDLONG-in-fill wrong at
> FILL=2 · WRLONG-in-drain at FILL=3 · register-only clean through 7), and an explicit `scope:` note
> that this is the **tested shape**, not a law about "any hub access", with the cause left as
> unmeasured. `ops_in_flight_per_cog` upgraded from purely derived to empirically supported.
> Source trace: EF-053. **Evidence-scoping honoured:** the entry states *where* results are lost and
> does not assert *why*.
> ~~Still owed (manual head): `chapter-05-hardware.md:~100-126` («#228») and
> `P2AN002/examples-library/cordic-pipeline-throughput.spin2` («#236»)~~ — **both applied
> 2026-08-16; see the MANUAL HALVES note below.**

> **MANUAL HALVES APPLIED 2026-08-16 («#228», «#236») — uncommitted under the «#234» gate.**
> Both were rewritten to **ARM D's measured-clean shape**, not to a plausible-looking repair: the
> rig's own ARM D is register-only in *both* loops with `ALTS`/`ALTD` indexing a cog buffer and the
> hub traffic batched outside, and it also carries **no `CALL` inside the loops**. Assembly ch.5's
> `queue_rotation` helper is therefore gone rather than merely hoisted — reproducing the shape that
> was proven, instead of applying the rule's wording to the old structure.
> • **Assembly ch.5 §5.1.6** — block `RDLONG` in, `REP`-based register-only fill/steady/drain,
>   block `WRLONG` out, plus a `hardware` callout carrying the measured depths (2 · 3 · clean-to-7),
>   the silent-failure warning, and the throughput-not-buffer-depth cause. The old performance
>   claim ("roughly 320 vs 864 clocks — nearly 3× faster") described the *broken* code and was
>   **removed rather than recomputed** — no invented cycle counts on new code.
> • **P2AN002** — `examples-library/cordic-pipeline-throughput.spin2` and the note's code block
>   rewritten together and verified **byte-identical**; the "How this works" prose now describes
>   where the hub traffic actually is, and a new pitfall carries the same measured rule.
> Both slices compile clean under `pnut-ts -d`.

**Our board, our measurement.** P2 Edge @ 200 MHz. Control: queue one op, retrieve immediately —
stalled **58 clocks**, exactly the documented `GETQX` maximum (`2...58`), so the rig can see the
failure mode. Four shapes swept over fill depth 1–7, checked against single-op `ROTXY` ground truth:

| Shape | Hub access inside a CORDIC loop? | First failure |
|---|---|---|
| **ARM B** — P2AN002's shape (`RDLONG` in the fill) | fill | **FILL = 2** |
| **ARM C** — register-only fill, `WRLONG` in the drain | drain | **FILL = 3** |
| **ARM D** — register-only fill **and** drain, hub I/O batched after | none | **CLEAN THROUGH 7** |
| ARM A — Assembly ch.5 shape (2×`RDLONG` + `CALL`/`RET` per issue) | fill | 15 of 16 wrong at FILL=6 |

**Chip's clarification is vindicated.** Deep pipelining works — 6–7 operations in flight is real, and
`GETQX`/`GETQY` stall correctly. **The rule is: no hub access inside either CORDIC loop.** Issue and
retrieve at the 8-clock slot cadence; batch hub reads and writes outside. Break it in the fill and
you lose results from the fill onward; break it in the drain and you lose them from the drain onward.

**The community report is right in effect and wrong in cause.** It is not a 2-deep result buffer —
it is a fill/drain that cannot keep up with the pipeline. (Supporting evidence: the ARM B failure
depth **moved between otherwise identical runs** — FILL=3 in one, FILL=2 in another. A fixed
hardware buffer depth would be deterministic; a timing race is not.)

**Both of our documents are wrong, for exactly this reason:**

- **`app-notes/P2AN002/examples-library/cordic-pipeline-throughput.spin2` (RELEASED)** — `rdlong t, inp`
  inside the fill loop, `wrlong r, outp` inside the steady loop.
- **`manuals/p2-assembly-language-manual/.../chapter-05-hardware.md:~100–126` (RELEASED)** — the
  `queue_rotation` helper does **two** `RDLONG`s plus a `CALL`/`RET` per issue, and the steady loop
  does two `WRLONG`s per retrieval. Slower than ARM B, and it measures worst of all.

**Proposed correction (same fix for both):** hoist hub I/O out of the CORDIC loops — block-read the
inputs into cog registers first (or compute them in-register), keep fill and drain to
register-only operations, then block-write the results afterwards. State the rule explicitly next
to the example, because the pattern *looks* correct and fails silently with plausible-looking
numbers.

**EF candidate:** this belongs in `P2-EMPIRICAL-FINDINGS.md` — our own board, our own probe, with a
control that stalled at the documented maximum. Probe:
`campaigns/2026-08-manual-corrections/tests/test-f263-cordic-pipeline-depth.spin2`.

#### Bench evidence for F-260 — session of 2026-08-14

*(Evidence for the F-260 entry above, not a second finding. Retained verbatim except that its
"the accumulators are never zeroed" mechanism claim is corrected in that entry — see the note there.)*

**Bench result (P2 Edge 200 MHz, jumper pin 0 -> pin 1, `test-f260-goertzel-input.spin2` BUILD 11):**

| arm | ADC density | delta cos | delta sin | magnitude |
|-----|-------------|-----------|-----------|-----------|
| on-target, 1 MHz detector, 1 MHz tone | 1020/2000 | 1,051,655 | -124,573 | **1,059,000** |
| detuned, 2 MHz detector | 1021/2000 | -1,865 | 1,775 | 2,575 |
| detuned, 500 kHz detector | 1020/2000 | 207 | -198 | 286 |
| no tone, driven pin | 349/2000 | -409 | 134 | 430 |

Identical densities across the three tone rows, so the only variable is the detector
frequency. **Selectivity 411:1 against the 2x detune, 3,700:1 against the 0.5x detune, and a
2,460:1 null.** The DDS/Goertzel mode detects and is frequency-selective.

**THE PROTOCOL THE GUIDE NEVER STATES, and the reason 20+ probe rounds read flat:**
**the Goertzel accumulators are never zeroed.** A fresh cog inherits the previous cog's value
(measured: each SEQ pass's pre-command read equalled the previous pass's last read, five times
running, across `COGINIT`), and successive commands ADD (measured: two identical commands gave
exactly twice one command's total). So an absolute `GETXACC` read is meaningless. **Read before
the command, read after, and take the difference.** This is precisely what Chip's shipped
`Goertzel_DEBUG_Demo.spin2` does with its `xcal`/`ycal` subtraction -- that calibration removes
the inherited baseline, not an analog offset.

**Field semantics, all confirmed against Chip's shipped demo and our bench:**
`pppp`x4 = base pin of the four-pin input block (`base<<17` is his own idiom, valid because the
base is a multiple of four); `S[15:12]` = sum-select, `S[19:16]` = invert-select, `S[11:0]` =
loop size + LUT window; NCO scale is 2^31; DAC output inverts each LUT byte's MSB; and in
`DAC_MODE` with `TT=%01`, `M[3:0]` selects **which cog's** DAC channels drive the pin (his
`setnib dacmode,cogid,#2`) -- the pin's low two bits pick the channel.

**Corrections for the guide** (all still required; the working mode does not excuse them):
1. `:1324` `dds_s` undeclared -- and S is mandatory, since `S[15:12]` selects which ADC pins are
   summed. `S = 0` sums nothing.
2. `:990` / `:607` `adc_pin<<17` is correct **only** when `adc_pin` is a multiple of 4, because
   `(adc_pin>>2)<<19 == adc_pin<<17` exactly then. The field names a four-pin BLOCK.
3. The section must state the read-before/read-after protocol above.

### F-266 — the debug interrupt disrupts the streamer, and `DEBUG_COGS` defaults to ALL cogs. `DONE (2026-08-16) — KB + Streamer Guide warning both applied`

> **KB APPLIED 2026-08-16 («#218»).** `architecture/streamer/overview.yaml` gains
> `debug_interaction:` — the default `%11111111` mask, the one-CON-line fix
> (`DEBUG_COGS = %0000_0001`), the measured cost (accumulators 1,000,000-7,000,000 of corruption →
> true values in the hundreds), the general rule for any hardware sequencer measured under the
> debugger, and `see_also` pointers to `architecture/debug_interrupt.yaml` and the configuration-
> symbols entry. This is the *surfacing* the finding asked for: the limitation already existed in
> `debug_interrupt.yaml`, and now a streamer author meets it where they are standing.
> Source trace: EF-057.

> **MANUAL HALF APPLIED 2026-08-16 — uncommitted under the «#234» gate.** Found missing during a
> coverage audit of the forum findings: «#221» closed without it, and no open task carried it.
> `streamer-body.md` gains **§14.5 Debugging Streamer Code** — the default `%1111_1111` mask, the
> interrupt's priority, the one-`CON`-line fix, the measured corruption (accumulators reading
> 1,000,000–7,000,000 against true values in the hundreds, plausible enough to be believed), and
> the general rule that any hardware sequencer under measurement wants a cog the debugger is not
> interrupting. Appendix D gains a `-d` check under *Goertzel Results Invalid* plus a new
> *Measurements Change When You Add DEBUG* symptom; three index entries point at §14.5.

**Location:** Streamer Guide (no warning anywhere) + KB gap.

`p2kbArchDebugInterrupt` already records it under `limitations`: *"streamer_interaction: Debug can
disrupt streamer operations. Workaround: Disable debug when using streamer."* And
`DEBUG_COGS` defaults to `%11111111` -- every cog has debug capability at runtime.

**Measured cost:** with `-d` and the default mask, our streamer probe crashed into the
single-step debugger's memory dump, and its Goertzel accumulators read 1,000,000-7,000,000 of
pure corruption. Setting `DEBUG_COGS = %0000_0001` (report from cog 0 only) stopped the crash,
made the launched cogs' `CogN INIT` lines disappear, and collapsed the accumulators to their
true small values. Every streamer measurement taken before that fix was confounded.

**Why it matters to a reader:** anyone debugging streamer code with `-d` -- the normal way to
debug -- has the P2's highest-priority interrupt live inside their streaming cog by default, and
nothing in the guide warns them. **Action:** warn in the Streamer Guide, and surface the
existing KB limitation where a streamer author will meet it.

### F-264 — `wrpin.yaml`'s `tt_field` flattens four context-dependent `%TT` meanings into one, and tells readers to add `P_OE` to DAC outputs where it breaks them. `DONE (2026-08-16)`

> **APPLIED 2026-08-16 («#218»).** `language/spin2/methods/wrpin.yaml` `tt_field` gains
> `context_dependent:` — an explicit statement that `%TT` has **no single meaning**, that the
> `constants:` effects listed are the smart-pin-on non-DAC_MODE set **only**, and the four contexts
> named with the smart-pin-off `DAC_MODE` row spelled out (`%01` selects a **cog DAC channel** as the
> source). `p_oe_required_for` is rewritten to *"SMART-PIN output modes only …"* and now states
> outright that adding `P_OE`/`P_CHANNEL` to a level-driven DAC kills its output. The full table
> stays single-sourced in `architecture/smart_pins.yaml`; `wrpin.yaml` carries enough that a reader
> cannot conclude the wrong thing without following the pointer — which was the specific ask.
> Source trace: Silicon Doc `p2-documentation.txt:7646-7660` + `part4-locks.txt:118-139`;
> bench corroboration EF-055 (1,305 of 2,000 → 25).
> **Scoping check performed:** `architecture/smart_pins.yaml:263-265`'s `which_modes_need_p_oe` was
> re-read and is **already correctly scoped** — its DAC entry names `%00001-%00011`, which are the
> smart-pin DAC modes. Left untouched; the defect was specific to `wrpin.yaml`.

**Location:** `language/spin2/methods/wrpin.yaml` — the `tt_field` block. **RELEASED.**

**The Silicon Doc specifies `%TT` as four different meaning-sets**, selected by whether the smart pin
is on and whether `DAC_MODE` (`M[12:10] = %101`) is active — `part4-locks.txt:118-139` and
`p2-documentation.txt:7646-7660`. For **smart pin off**:

| `%TT` | non-`DAC_MODE` | **`DAC_MODE`** |
|-------|----------------|----------------|
| `%00` | OUT drives output | **OUT enables ADC, `M[7:0]` sets DAC level** |
| `%01` | OUT drives output | **OUT enables ADC, `M[3:0]` selects cog DAC channel** |
| `%10` | OTHER drives output | OUT drives BIT_DAC |
| `%11` | OTHER drives output | OTHER drives BIT_DAC |

**Our KB already carries this correctly** in `architecture/smart_pins.yaml:249-253`, verbatim.
`wrpin.yaml`'s `tt_field` does not: it gives one context-free effect per value — `P_TT_01:
"Output enabled regardless of DIR, SMART/OUT drives"` — which is the smart-pin-**on**, non-DAC
meaning presented as *the* meaning. Its only route to the truth is a `see_also` pointer.

**Two concrete harms:**

1. **`p_oe_required_for: "All output modes (NCO, PWM, Pulse, Transition, Serial TX, DAC, USB)"`
   is wrong for the non-smart-pin DAC.** There `P_OE`/`P_CHANNEL` is not an enable at all — it
   switches the DAC's source from the pin's own level field to a cog DAC channel. Applying the
   F-245 "add `P_OE`" remedy to a level-driven DAC **kills the output**. Measured on our bench
   the same day: a `P_DAC_124R_3V` pin driven from its level field read a spread of **1,305** of
   2,000 samples; adding `P_CHANNEL` dropped it to **25**.
2. **An agent reading `wrpin.yaml` alone builds a wrong model of DAC pins.** This is not
   hypothetical — it produced two successive wrong hypotheses during the 2026-08 bench campaign
   before `architecture/smart_pins.yaml` was consulted.

**Correction:** make `tt_field` state that `%TT` is context-dependent, name the four contexts, and
qualify `p_oe_required_for` to smart-pin output modes — with the `DAC_MODE`/smart-pin-off row
called out explicitly, since that is the cog-DAC and streamer-override case. Keep the full table
in `architecture/smart_pins.yaml` as the single source; `wrpin.yaml` needs enough to stop a reader
concluding the wrong thing without following the pointer.

**Note the shape:** this is F-245 and F-259 one level up. Both were resolved *against this file*,
and this file was incomplete on exactly the axis that mattered.

**Status:** `NOTED` 2026-08-14, resolution deferred until the bench campaign closes (Stephen's
standing rule: no doc/YAML editing until every bench question is conclusive).

### F-265 — the Silicon Doc contradicts itself on whether Goertzel ADC pins are smart pins; the KB must state the resolved answer. `DONE (2026-08-16)`

> **APPLIED 2026-08-16 («#218»), and this entry's own closing condition is met.**
> `architecture/streamer/dds-goertzel.yaml` gains `adc_input_pins:` stating the resolved answer —
> ADC mode, smart-pin mode field `%00000`, **no DIR** — and, per the ask, **names the tension** in
> `source_tension:` so the STREAMER intro's loose *"smart pins configured as ADC's"* cannot
> re-mislead. Source trace: Silicon Doc `p2-documentation.txt:3997-3998` (verbatim), corroborated by
> the Silicon Doc's own worked program at `:4174-4180`, which issues `wrpin adcmode,#adcpin` with
> mode field `%00000` and gives **`dirh` to the DAC pin only**.
> **The defect was wider than the finding named** — the file's own `usage_pattern` code was the very
> thing the finding warns against, and it carried three more defects besides. All repaired in the
> same pass, each against the Silicon Doc's worked program (`:4170-4185`, `:4289-4305`):
> (a) `drvl #adc_pin` removed (that was the DIR the rule forbids); (b) `xcont dds_cmd, #0` → a real
> `dds_s` — **S is mandatory**, `S[15:12]` selects which block pins are summed and `S=0` sums
> nothing; (c) the NCO frequency now set with `SETXFRQ` and the missing `shr xfrq,#1` restored, so
> the code matches the `frequency:` block directly above it (2³¹ scaling, not 2³²); (d) `P_ADC_100X`
> → `P_ADC_1X`, with a `gain_choice:` note that gain is a property of the **coupling**, not the mode.
> Also added: the four-pin **block** model (`D[22:19] = %pppp`, `%pppp × 4` = base pin), the
> `base_pin<<17` validity condition, and the S-operand field map — all `p2-documentation.txt:4002-4006`.
> **Guide-side §17.1 statement rides «#221»** and derives from this entry.

> **Rewritten in place 2026-08-15.** This read `NEEDS-VERIFICATION` while the answer had already been
> established on the bench — and while this register's own header line had it right. The contradiction
> was internal to this file.
>
> **The answer: the ADC pin is RAW** — `P_ADC_x` with smart-pin mode `%00000` and **no DIR**. The
> DDS/Goertzel section of the Silicon Doc is authoritative; the STREAMER intro's *"smart pins
> configured as ADC's"* is loose wording. Confirmed by our own working probe and by Chip's shipped
> demo (`campaigns/2026-08-manual-corrections/BENCH-FINDINGS-FOR-AUTHORING.md` Test 5).
>
> **Why this stays open:** the *fact* is settled; the *KB statement* is not written. A reader landing
> on the intro still configures a smart pin and gets nothing. Owed: state the resolved answer in
> `architecture/streamer/dds-goertzel.yaml` **and** name the tension so the intro's wording cannot
> re-mislead. Closes when that lands.

**Location:** KB gap — `architecture/streamer/dds-goertzel.yaml` (and the Streamer Guide's §17.1).

- Silicon Doc STREAMER intro (`part2-pixel-ops.txt:82`): the streamer can *"perform Goertzel
  computations from **smart pins configured as ADC's**."*
- Silicon Doc DDS/Goertzel section (`part2-more-content.txt:176`): the pins *"should be configured
  for ADC mode, so that their IN signals are raw delta-sigma bit streams, **with no smart pin mode
  selected**."*

These cannot both be operative. The detailed section is the more specific statement and is what our
probe follows (`P_ADC_1X`, smart-pin mode `%00000`), and the Silicon Doc's own worked example uses
`wrpin adcmode,#adcpin` with mode field `%00000` — which supports the detailed section. But the KB
currently says nothing about the tension, so a reader who lands on the intro will configure a smart
pin and get nothing.

**Action:** settle it with a bench arm (cheap — run the DDS/Goertzel arm both ways), then state the
answer in the KB and the guide rather than leaving the reader to reconcile two sources.

**Status:** `NOTED` 2026-08-14, arm to be added to the F-260 probe; resolution after the bench
campaign closes.


---

*Move-aside 2026-06-13 after the v1.9.0 release closed out F-001..F-124. The archive holds the full history; this active register carries only the carry-forward guardrails and the ingestion-tracked items. New findings continue at F-125.*

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

**NOT caused by the F-285 repair, and not new.** Independently checked against the **released v3.1.5
PDF** (recovered from git), which renders these lines differently — so the visible symptom changed
when the `&nbsp;` text was removed, but the filter defect predates it.

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

**Owed:** one Assembly render. **Assembly v3.1.6 is HELD from the release wave** until p.329 shows
the four TESTP forms each on one line; deSilva, P2AN001 and P2AN002 are unaffected (this filter is
Assembly-local) and released without it.

**Next finding ID after this block: F-289.**

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
