# P2KB Correction Findings — ARCHIVE, swept 2026-08-19

> **This is an archive of CLOSED findings. It is never re-edited.** Ask "what is
> outstanding?" of `engineering/operations/P2KB-CORRECTION-FINDINGS.md` alone — never
> re-derive completion state from here. If an archived finding must be reopened, it
> returns as a **new** active finding that references this file.
>
> Contains 18 findings closed on or before 2026-08-19, each carrying a `DONE` /
> `WONTFIX` / `RESOLVED-INVALID` status token: F-227, F-228, F-254, F-255, F-257, F-258, F-259, F-260, F-261, F-262, F-263, F-264, F-265, F-266, F-267, F-269, F-270, F-273.
>
> Produced by **rename-then-trim** — this file began as a git-tracked rename of the live
> register and had the still-open findings subtracted from it, so its content is the
> original's, not a reconstruction.

---

## Header of the register at the time of the sweep (retained for context)

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

**Next finding ID: `F-302`**

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

---

## Appended in the same 2026-08-19 sweep — closed at the XBYTE sprint closeout

These four shipped in **XBYTE v1.1.0** and their statuses were flipped from `CONFIRMED`
("render owed") to `DONE` after the render was verified on the shipped PDF.

### F-295 — the XBYTE guide framed 32 MB as the ceiling for a guest image, and credited a shared community PSRAM driver to one of its users. `CONFIRMED` — `DONE (2026-08-19)` — **RELEASED in XBYTE v1.1.0.** Render verified on the shipped PDF: external memory reads as a subsystem (p16) and the decay-prone "32 MB" ceiling is absent.

**Surfaced by** Stephen's read pass over §7.3, on the instinct that the passage may "mis-read what
they are doing" — users run PSRAM setups far larger than an Edge module, e.g. 96 MB.

**Authority: the emulators' own shipped source**, in the guide's own `REF-NO-COMMIT/larger-emulators/`
— not forum recollection.

| Claim as written (§7.3) | What the source says | Verdict |
|---|---|---|
| "the 32 MB module (**P2-EC32MB**) maps all 32 MB as one linear space, room for **any** classic guest and its RAM several times over" | `NeoYume/RAMCONFIG.MD` documents **three** known-good boards — P2EDGE 32 MB (quad-chip, 1 bank, "the most common config"), **Rayslogic 96 MB** (dual-chip, **6 banks**), Rayslogic 24 MB (single-chip, 3 banks) — plus a HyperRAM option. Both repos are titled "…for Parallax P2 **+ memory expansion**" | **over-claim** |
| "**Capacity is not the contest** — 32 MB holds a large guest and a framebuffer with room to spare" | `neoyume_gamedb.spin2:921` — *"wierd holey memory map, doesn't fit in 32MB when it really should"* (King of Fighters '95). Capacity does bind, and awkward maps are why the bigger boards exist | **over-claim** |
| "a PSRAM driver that arbitrates between cogs — **MegaYume's** does exactly this" | `psram16drv.spin2` is **byte-identical** in MegaYume and NeoYume (md5 `e162125d…`) and its own header/licence read **"Copyright 2020, 2021, 2022 Roger Loh"** (rogloh). Both emulators carry it unmodified | **mis-attribution** |

**The arbitration behaviour itself was correct** and is now stated from the driver's own header:
a 3-long **mailbox per cog**, "strict priority and round-robin request polling (selectable per
COG)", per-cog burst limits, and unserviced cogs removable from the polling loop.

**Fixed in `opus-master/xbyte-body.md`:** §7.3 now names the P2-EC32MB as the usual home rather than
the ceiling, points at Appendix C for the 24–96 MB and HyperRAM setups, says bandwidth is *usually*
the contest while capacity *does* bind, and credits the driver as the shared community one both Yume
emulators use. §C.4 gained the board list and Roger Loh's authorship.

**Checked and NOT changed — the neighbouring MegaYume citation in §7.4 is sound.** Its Z80 dispatch
loop (`megayume_lower.spin2` ~5070) shows all three cited behaviours in the same few lines:
`if_ae waitx zk_cycles` + `getct zk_lastwait` (pacing), `incmod zk_refresh,#127` (the 7-bit Z80 `R`
register), `zbus_request`/`zbus_status` (guest bus arbitration) — and, incidentally, a textbook rung 2:
`call #zk_readcode` · `push #zk_nextop` · `rdlut` · `execf`. **Note the two are different kinds of
arbitration** and must not be merged: §7.4 is the *guest's* bus between Z80 and 68000; §7.3 is the
*P2's* PSRAM bus between cogs.

**Class-wide sweep: no spread.** Every other `32 MB`/`EC32MB` mention across the manual and app-note
set is a module specification (pin usage, flash size) or unrelated (Debug Window's 96 MB is PLOT
layer memory). The defect was confined to these two XBYTE paragraphs.

**The configured sizes, read out of each project's own `config.spin2` defaults** — this is the part
that makes the point, because two of the three do NOT default to an Edge module:

| Project | Enabled width | `PSRAM_BANKS` | Board that matches | Capacity |
|---|---|---|---|---|
| MegaYume | `USE_PSRAM16` (quad chip) | 1 | P2-EC32MB Edge | **32 MB** |
| NeoYume | `USE_PSRAM16` + `NOBANKS` | 1 | P2-EC32MB Edge | **32 MB** |
| **MisoYume** | `USE_PSRAM8` (dual chip) | **6** | Rayslogic on P2EVAL basepin 0 | **96 MB** |

MisoYume's shipped default (`PSRAM_CLK = 8 addpins 1`, `SELECT = 10`, `BASE = 0`, `BANKS = 6`,
`DELAY = 17`, both syncs true, `USE_PSRAM_SLOW`) is a byte-for-byte match for the "Rayslogic 96MB
PSRAM board" stanza in `NeoYume/RAMCONFIG.MD`. **The SNES emulator ships aimed at a 96 MB board.**

The capacity model is consistent across all three documented boards at **8 MB per chip**: width sets
chips-in-parallel (`PSRAM4`=1, `PSRAM8`=2, `PSRAM16`=4), `PSRAM_BANKS` multiplies them via
`PSRAM_SELECT`+n. 4x8x1 = 32 MB, 1x8x3 = 24 MB, 2x8x6 = 96 MB — each lands exactly on its board's
name. (The per-chip figure is documentary for the Edge module — the KB's `edge-32mb-module.yaml`
gives 64 Mbit/chip, 4 chips; for the third-party boards it is arithmetic from the board name and
bank count, not a datasheet, and is recorded as such.)

**Currency caveat, stated rather than glossed.** The local snapshot under `REF-NO-COMMIT/` dates
from **Oct 29 / Nov 3 / Dec 6 2025** (MegaYume / NeoYume / MisoYume) and carries `.gitignore` and
`.gitattributes` but no `.git`, so there is no commit hash and it cannot be asserted to be current.
Everything above is true of that snapshot. The guide's prose was deliberately written against the
*documented* configuration range rather than any project's mutable default, so a newer upstream
default cannot falsify it — but a re-pull before the next XBYTE release is worth doing.

**RESOLUTION AMENDED, 2026-08-18 (Stephen).** The first fix replaced one perishable claim with
several: it swapped "32 MB is the ceiling" for a vendor name, a 24-96 MB board range, and a HyperRAM
option. Same defect in a new form — a reader-facing catalog of third-party hardware decays, and a
decayed claim is an incorrect one. The prose now carries the **mechanism** instead:

> a guest too large for hub lives **whole in an external memory subsystem** and you **fetch from
> there**; the P2-EC32MB Edge module is a good **starting point**; larger boards come from other
> vendors and from community builders; a banked driver presents whichever board you have as a single
> address space. What the board decides is how much you hold and how fast you reach it — what it
> never changes is that the fetch is yours to write.

Specific third-party capacities and vendor names are **out** of both §7.3 and §C.4. The Parallax part
number stays: it is a documented product in our own KB, and it gives the reader a concrete place to
start. The capacity point survives in durable form — *a holey memory map can need far more address
space than the ROMs add up to* — which teaches the real mechanism instead of citing one game.

**THE RULE THIS ESTABLISHES, worth applying beyond this finding:** do not put anything in a reader
document that is **subject to becoming incorrect over time** when the durable statement is available.
Third-party product catalogs, "what is currently available", capacities, and vendor line-ups all
decay silently — nothing fails, the sentence just quietly stops being true, and no gate can see it.
Prefer the mechanism, which does not move; name a specific product only as a starting point, and
only when it is documented in our own sources.

**The transferable lesson on how it was caught.** The original claim was *plausible* and had a real
mechanism behind it — which is why it survived authoring and a full audit. What broke it was reading
the shipped artifact instead of the description of it: a config file listing three boards, a
game-database comment, and an md5.

**Next finding ID after this block: F-296.**

---

### F-296 — §7.4 read as a wall when the engine only moves the work, leaving three usable places to put it. `CONFIRMED` — `DONE (2026-08-19)` — **RELEASED in XBYTE v1.1.0.** Render verified: p40 reads *"That is a relocation, not a wall"*.

**Surfaced by** Stephen's read pass: "the 7.4 narrative felt too constraining." The section said the
cross-cutting work must be "replicated across all of them, confined to the few where it genuinely
matters, or dropped… a real cost and sometimes a prohibitive one," and pointed forward to a chapter
that **prices** it. A reader who stops at §7.4 concludes the boundary is solid. It is not.

**Three placements, every one built from facts the book already teaches:**

1. **Per family, not per instruction.** The shipped 8080 emulator (rung 3, XBYTE-armed) polls guest
   interrupts in the shared tail of its **control-flow** handlers — `jatn #int_event` annotated for
   twelve branch/call/return bytecodes and skipped on the injection path itself. Costs nothing: those
   instructions had to run anyway. `HLT` gets its own `jnatn`, because a halted guest never branches.
   Already priced in §17.3's third row ("nearly free") — §7.4 simply never said the answer existed.
2. **An optional prologue selected by the skip pattern.** `SKIPF` *leaps* rather than cancels, so a
   skipped prologue costs essentially nothing (§4.2); a second table over the same handler addresses
   with patterns that *include* it turns the work on — `SETQ` for a mode, `SETQ2` for exactly one
   bytecode (§10.3). **Two tables at once is shipped practice**: Parallax's Spin2 interpreter, and
   zog, which defines `RET_START_ALTERNATE`/`RET_CONTINUE_ALTERNATE` as `_ret_ setq2 #$100` against a
   main table at `setq #$0` — both halves of a 512-long LUT. Both use it to redirect dispatch, not to
   instrument; **instrumenting is the unexploited step.**
3. **The cog's own interrupts, which XBYTE never took.** §9.4 already states the engine is
   interruptible and resumes the stream afterwards. Periodic work — pacing, watchdog, device service
   — belongs there and costs the dispatch path nothing. §7.4 never connected the two.

**The point that makes placement 2 practical, and which the first draft of this fix got wrong:**
skipping is **suspended for the duration of a `CALL`** (§13.1, and the reason §16.3's shared `set_nz`
helper works at all). So the prologue is **one instruction** — a `CALL` — reaching a routine of any
length whose instructions are immune to the pattern that selected it. One pattern bit buys unbounded
work. The draft had claimed the prologue "spends pattern bits the body also wants," which is only
true if you inline it.

**Framing ruling (Stephen).** No verification rig was built, deliberately: *"if somebody's already
doing it, they'll spend a lot of time verifying it before they publish… We're not speaking for proof;
we're speaking for ideas and possible ways of doing things."* The distinction the prose must honour —
and does — is that **every component fact is verified and cited in-book**, while the **composition is
labelled a shape to consider, not a recipe**, with the reader told to prove it for their own guest.
That is not an unsourced claim; it is a sourced mechanism with an honestly-marked boundary. Also
per Stephen: do not characterise the shape as ideal or non-ideal.

**Collateral, verified:** §C.7 now records zog's second dispatch table (the §18.4 idiom in a
community interpreter rather than Parallax's own). §7.4's "had no choice" for the de-arm-and-trace
technique became "took the direct route" — the section now names alternatives, so the absolute
over-claimed. The hardware box no longer says "disaster" and instead names *where* the cost actually
bites: work that must happen on **every** instruction, cycle-accurate timing above all, is what
cannot be attached to a family.

**BLAST RADIUS, swept 2026-08-18 on Stephen's prompt — nine downstream sites carried the old claim.**
Revising a section is only half the job when other chapters cite its conclusion. A text search for
"7.4" was NOT sufficient: the damaging sites were the ones that echoed the claim in their own words.
Swept for both, and separated a **structural** statement ("there is no loop body" — still true) from
a **capability** claim ("there is nowhere to put the work" — no longer true):

| Site | Was | Now |
|---|---|---|
| §3.6 | "a place to work that it **removes**" | "a place to work that you **choose rather than inherit**" |
| §6.4 | "there is **nowhere** to put a `debug()`" | "a `debug()` has no place **in the dispatch itself**" |
| §8.8 | pacing "has **nowhere to live**" | "has no **cheap** home" + *why*: it is the one kind that cannot be confined to a family, so it is paid on every dispatch |
| Ch.13 opener | "XBYTE has **no such place**" | "no such place **in the dispatch itself**"; names where it can go |
| §17.1 | "there is **nowhere to put the check**" | "the check has no **default** home and you place it deliberately" |
| §17.3 | "**took away** the place where the check belonged" | "**left the check without a place of its own**" |
| App. D | "there is **no loop body** to instrument" | "the **dispatch itself** has no body to instrument" |
| §19.7 | remedy column omitted the interrupt route | adds periodic work in a cog interrupt (§9.4) |
| Index | "Loop body (there isn't one — what it costs)" | "…and where the work goes instead", plus a new **Placing cross-cutting work** entry |

§17.1 was the sharpest: "there is nowhere to put the check" sat two sections ahead of §17.3, which
exists entirely to say where to put the check. That contradiction pre-dates this sprint.

**Left deliberately unchanged, having been checked:** §3.5 ("This does not mean they are impossible…
down to nearly nothing if you can confine them") and §19.7's "*by default*" were already calibrated;
front-matter's "no loop body, because the loop is the silicon", Part IV's "a loop that has no body",
and §7.4's own title are **structural facts**, not capability claims. Ch.2's "leaves no gap" plants
the tension the revised §7.4 resolves — that is the intended arc, not a defect. The guide layer
(voice-guide, creation-guide, descriptor) carries no §7.4 reference at all.

**The transferable lesson.** A section can be factually correct and still leave the reader with a
false conclusion. Nothing in §7.4 was wrong; the omission of the answer did the damage, and only a
read-through caught it — no gate can test for "this reads as a dead end." And when a claim is
revised, **the sweep must be semantic**: the sites that quietly contradicted the new §7.4 mostly did
not cite it.

**Next finding ID after this block: F-297.**

---

### F-297 — the book taught the shared-handler idiom without the notation every real shared body uses. `CONFIRMED` — `DONE (2026-08-19)` — **RELEASED in XBYTE v1.1.0.** Render verified: the column-map notation is taught on p26.

**Surfaced by** Stephen: Chip's skip tables are *deeply documenting*, ours said what each
instruction does. Should we teach the best-in-class pattern so it is learned?

**What the notation is, verified against `Spin2_interpreter.spin2` (v51):** a fixed column per
bytecode in the comment field, keyed to a legend. **letter** = that bytecode runs the line ·
**`|`** = its pattern skips it · **blank** = not in play (not yet entered, or already returned).
Read across a row for who runs an instruction; read down a column for one bytecode's whole path.

**The load-bearing fact, and how it was actually established.** A column *is* the skip pattern
written out. First checked against `bc_read` (`%0111001110`) — 10/10 — but **that pattern is a
palindrome, so the decode agreed regardless of bit order and proved nothing about direction.**
Re-verified against `bc_var_inc` (`mod_iso | %00011111010110010`, 17 bits, not a palindrome):
**17/17 positions agree**, LSB-first from the entry point. Only the second test is evidence.

**Why it earns a teaching slot.** §4.6 already carried the design process, and its step 4 said
"assign each member's pattern" with no *how*, while its own warning — *"a `##` immediate is two
longs… count longs, not lines"* — was advisory. The map closes both: draw the grid one row per
long, and read the pattern off it. **You derive the pattern from the map rather than documenting
it afterwards**, and a `##` visibly occupies two rows, so the off-by-one cannot hide.

**Adopted at:** §4.4 (reading key, where the reader first meets a shared body), §4.6 step 4 (the
method), §14.3 (two members), §15.2 and §15.4 (in the shipped corpus). §10.2 is a two-line flag
fragment, not a skip-shared body — deliberately left alone.

**Collateral corrections the adoption forced:**
- The VM examples named their operand registers `a` and `b`, which **collide with the column
  letters**. Renamed to `x`/`y` (Chip's own convention) across the corpus and every mirrored block.
- `push_a` became `push_x` but `pop_a` did not — the rename was inconsistent until swept. Both are
  now `_x`.
- **Guest-CPU registers were correctly NOT renamed**: §8.5's Z80 fragment and §16.3's 6502 use
  `a`/`b` as the *guest's* accumulator and B register. A blanket rename would have corrupted them.
  This is the whole reason the sweep was scoped by block rather than by regex over the file.
- The §15.4 excerpt is **uncaptioned**, so the identity gate does not cover it, and it silently
  drifted from its file during the rename. Found by reading, not by a gate. **Uncaptioned excerpts
  of captioned files are an unguarded seam** — worth a gate of its own some day.

**Gates:** corpus identity GREEN (3/3 byte-identical), headers synced, all three examples compile
under `pnut-ts`, K=76 clean.

**Next finding ID after this block: F-299.**

---

### F-298 — §7.4 called the gated call-out a "prologue", contradicting the example it had just cited. `CONFIRMED` — `DONE (2026-08-19)` — **RELEASED in XBYTE v1.1.0.** Render verified by READING the shipped pages, not by assuming: "prologue" still appears on p41 and p114, which is correct — the reframing keeps it as ONE named placement among several. p41 teaches that each gated line has its own bit so a body can carry several independently-switched call-outs, and the Index lists *"a family's shared tail · an optional prologue"* as alternatives. The defect was prologue-as-the-only-placement; that is gone.

**Surfaced by** Stephen re-reading §7.4 — *"are we convinced that prolog vs epilog is the only
possible choice?"*, then sharpening it to *"aren't we saying before instruction execution vs.
after?"* Both halves were right.

**The defect.** F-296's text said a handler "can be built with an optional **prologue** in front
of its body." Wrong three ways:

1. **Not the only placement.** A pattern bit governs each line *independently*, so the gated line
   can sit anywhere in the 22-instruction window — and a body can carry **several**
   independently-switched call-outs, not one.
2. **It contradicted the worked example two paragraphs above it.** The shipped 8080 emulator puts
   its `JATN` in the shared **tail**, immediately before the closing `_RET_` — an epilogue. §7.4
   cited that emulator and then described the opposite placement.
3. **It landed on the one position the book elsewhere says to avoid.** §4.5: pattern bit 0 governs
   the line "you jumped there in order to run", so a normal entry leaves it clear — and §4.5 then
   spends that bit as **per-bytecode metadata** (the 6502 emulator packs cycle counts into the
   spare high bits the same way). A call-out as instruction 0 collides with both.

**The reframing:** the choice is not *where in the source* but **when relative to the guest
instruction's work**.

| Placement | Sees | Natural for |
|---|---|---|
| **Before** the body's work | the *previous* instruction's completed state | deciding whether to take a pending interrupt — a clean boundary. Must not be the body's first instruction (bit 0) |
| **After** the work, before the return | *this* instruction's result | cycle accounting, flag/refresh bookkeeping, tracing an outcome. **What the 8080 emulator does** |
| **Between steps** | mid-operation state | work that must interleave with a multi-step operation |

**Corroboration that "after" is usually right for interrupts:** §17.3's consistent-state rule
already said a handler that has finished its work and is about to return is a safe boundary, while
the middle of a multi-step address computation is not. **The book had the answer in Chapter 17 and
stated its opposite in Chapter 7.**

**The transferable lesson.** Second time this review that §7.4 was *internally* inconsistent rather
than factually wrong: it cited real evidence and then generalised past it. A worked example and the
generalisation drawn from it must be checked **against each other**, not only each against the
source.

**REGISTER HYGIENE, same pass:** two blocks both carried "Next finding ID after this block: F-298"
because the F-297 registration replaced the previous block's marker instead of only appending its
own. Corrected — F-296's block now closes at F-297. A marker that says the same thing twice is a
counter that has stopped counting.

**Next finding ID after this block: F-301.**

