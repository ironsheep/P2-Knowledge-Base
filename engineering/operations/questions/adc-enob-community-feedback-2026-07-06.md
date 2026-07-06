# ADC / ENOB — Community Feedback Capture

**Captured:** 2026-07-06 17:50 UTC
**Source:** User-relayed community feedback (via Stephen Moraco)
**Subject:** Misuse of "ENOB" in Parallax documentation; sigma-delta ADC schematic/behavior facts for P2
**Status:** CAPTURED — analysis pending (see § Analysis below, to be completed)

---

## Verbatim feedback (single paste — do not edit)

> Regarding ADC:
>
> Unfortunately in the Parallax documents "ENOB" is misused just as theoretical number of bits resolution. Proper use of ENOB does specify the number of bits, you can rely on. This is a big difference! https://en.wikipedia.org/wiki/Effective_number_of_bits
> (I have several times tried to bring in correction but it was just clicked away.) In the new manuals this should be corrected! To say, that ENOB=18 could be achieved is total nonsense! "ENOB" should be used correctly. If not known, then just use "bits resolution".
>
> There is a very helpful diagram of the sigma-delta hardware, which should be included into the manuals and the application sheet:
>
> I think it is by @evanh, posted here: https://forums.parallax.com/discussion/comment/1484327/#Comment_1484327
> What do we learn:
> 1. P2 has neither an internal reference voltage source, nor an input for one, it just uses the 3V3 supply of the pin group. So precision and noise of this has critical effect. Also internal activities in P2 and load on the pins will have effect.
> 2. If "gain" is altered from 1x to 100x, then the input impedance goes from 450k down to only 4k5, so you will need a low impedance source like a buffer!
> 3. The "calibration" sources for 3V3 and GND use their own resistors, so "calibration" cannot take into account the differences between the actual resistors.
> 4. Measurements have shown, that the gain of 100x does not provide better resolution than 31x, because there is just more noise.
>
> There is also complete internal schematic in https://forums.parallax.com/discussion/175609/improved-adc-pin-techniques/p3 #62.
>
> All in all in reality of P2 an ENOB of about 11 or 12 bits can be achieved.
>
> Schematics should be added in all interface chapters. What is connected to what and how?

---

## Referenced sources (from the feedback)

- **ENOB definition** — https://en.wikipedia.org/wiki/Effective_number_of_bits
- **Sigma-delta hardware diagram** — attributed to @evanh — https://forums.parallax.com/discussion/comment/1484327/#Comment_1484327
- **Complete internal schematic** — https://forums.parallax.com/discussion/175609/improved-adc-pin-techniques/p3 (post #62)

---

## Analysis

**Completed 2026-07-06.** Bottom line: **the terminology criticism is correct and
defensible from primary authority** — the P2 designer (Chip Gracey) is already on
record that the Silicon Doc's ENOB numbers are wrong and "need to change the docs."
The misuse originates in the Parallax Silicon Doc and was transcribed faithfully into
our manuals and one shipped YAML. Our app notes (P2AN001/P2AN003) already dodged the
trap by deferring ENOB to hardware.

### Q1 — Is the "don't misuse ENOB" criticism CORRECT? → YES (defensible three ways)

1. **Standard definition.** ENOB (Effective Number Of Bits) is a *measured* figure of
   merit, defined for ADCs by IEEE Std 1241: `ENOB = (SINAD_dB − 1.76) / 6.02`, computed
   from the **measured** signal-to-noise-and-distortion ratio (SINAD) of a full-scale
   sine input. By construction it is the resolution *after* all noise and distortion —
   "the bits you can actually rely on." It is **not** the theoretical output word width of
   the decimator. (Wikipedia ref in feedback is a correct lay summary of the IEEE metric.)

2. **The Silicon Doc literally conflates the two.** Root source
   `engineering/ingestion/smart-pins-catalog/ingestionSources/mode-11001-adc-external-clock/silicon-doc-extract.md`:
   - L60 footnote: *"ENOB = Effective Number of Bits, **or the sample resolution**"* — this
     equates ENOB with nominal decimation width, which is the error.
   - L89: *"SINC3 **doubles the ENOB**"* — the retracted "doubling" claim.
   The table's "Post-diff ENOB" column is just the decimation word width (N clocks →
   N-bit / 2N-bit word), relabeled "ENOB." That is exactly the misuse the feedback names.

3. **Primary authority already agrees.** In our own captured research
   (`app-notes/P2AN001/research/improved-adc-pin-techniques/thread-p1.md`), **Chip Gracey**
   (P2 silicon designer, Silicon Doc author) says:
   - *"I never did find out how you computed the ENOB in the Silicon Doc."*
   - *"I think that optimistic doubling of ENOB would only be if we had a second-order
     analog modulator. Need to change the docs."*
   The feedback author is almost certainly **Christof Eb.**, whose forum positions (rigorous
   ENOB definition, ENOB≈11 target, 450 kΩ input impedance, 2 kΩ sensor impedance) are
   already logged in `research/.../thread-p2.md` L273–275.

**Nuance — do NOT over-correct into banning the term.** The right fix is precision, not
avoidance:
- Where a column means "the decimator emits an N-bit word," relabel it **"sample resolution
  (bits)"** / **"nominal resolution"** — NOT ENOB.
- Reserve **"ENOB"** for an actual measured effective resolution. We have none certified →
  so we print **no ENOB number** (exactly what P2AN001/P2AN003 already do).
- **Remove / reframe the SINC3 "doubling" column** — it is the claim Chip retracted.
- The SINC2 *"+1 bit over bit-summing"* statement is a legitimate *nominal-resolution* claim
  (decimation math, Chip-confirmed) — keep it, just don't call the result ENOB.
- Optional: state a realistic **effective** figure (~11–12 bits) as a **community-measured**
  value, tiered as such — NOT as a Parallax spec. (Chip's bench "~17-bit" and Christof's
  "11" are both bench/request figures, not silicon spec.)

### Q2–Q6 — the six hardware facts, checked against what we already hold

| # | Feedback claim | Our current state | Verdict |
|---|----------------|-------------------|---------|
| 1 | No internal/external Vref; uses pin-group 3V3 supply; supply noise + activity + load matter | IOSP §16.8 L570 "references track the VIO supply… feed VIO from a clean LDO"; §16.3 L243 "references local to the pin's power group" | **Already covered** (well). Minor: make the "no dedicated Vref at all" point explicit. |
| 2 | Gain 1×→450 kΩ, 100×→4.5 kΩ; high gain needs a buffer | IOSP §16.8 L568 gives "≈500 kΩ **on the 1× range**" only; P2AN001 L555/628 "~500 kΩ, buffer high-Z." **Gain-dependent collapse NOT stated.** | **Gap** — add: input impedance scales down ~with gain (≈450 k/gain); at 100× ≈4.5 kΩ → needs a low-impedance/buffered source. |
| 3 | Calibration sources use own resistors → can't correct signal-path resistor mismatch | IOSP §16.8 L569 nails it: three separate matched on-chip resistors, ≈15 mV absolute-error floor, "self-cal by driving the pin to each rail." | **Already covered** (our framing is actually stronger — drive-the-pin self-cal sidesteps the limitation). |
| 4 | 100× gain no better than 31× (just more noise) | Not stated anywhere. | **Gap** — add as practical guidance (highest gain ≠ best resolution). *Empirical* claim → tier as community measurement, or verify on hardware before asserting. |
| 5 | Realistic achievable ENOB ≈ 11–12 bits | We print no number (deliberate). | **Optional add** — as community-measured, tiered; consistent with "no certified ENOB" stance. |
| 6 | Include the sigma-delta schematic in every interface chapter | No ADC front-end schematic in any manual. | **Gap / diagram task** — Stephen has evanh's schematic **and** a second summing/math diagram downloaded; redraw both as our own TikZ (circuitikz), add to ADC chapters + P2AN001. |

Numeric reconciliation to settle before publishing a number: input impedance we publish
"≈500 kΩ" vs evanh ">500 kΩ" vs feedback "450 kΩ" (all 1×) — pick one sourced figure and
state the gain-scaling law rather than a single point.

### Documents affected (inventory)

**A. Carry the raw misuse (must fix the "ENOB = word width" table + SINC3 doubling):**
- **Silicon Doc** (upstream root cause) — not ours to edit, but it's the origin; flag for any
  re-ingestion and as provenance in the corrections entry.
- **IOSP User Guide** — RELEASED (v1.0.2). `opus-master/part-3-input-modes/chapter-16-adc.md`
  §16.3 table + footnote; §16.2 "8-14 ENOB" (L12733); appendix glossary. *Already* has a good
  mitigating caveat (treat any ENOB figure as a bench result) but still prints the misused
  table. → correction + **minor version bump** on next release.
- **Smart Pins Green Book Tutorial** — in-development. Same table + "SINC3… Doubles the ENOB."
  → absorbs correction, **no bump**.
- **Shipped YAML** `deliverables/ai/P2/architecture/smart-pins/smart-pin-11001-adc-external-clock.yaml`
  L165–167 ("16 clocks = 8 ENOB" … "512 clocks = 18 ENOB"). → **yaml-head correction**,
  logged to `P2KB-CORRECTION-FINDINGS.md`.

**B. Already disciplined (no misuse; candidate ENRICHMENT only):**
- **P2AN001** — the "application sheet" the feedback names. RELEASED (v1.0.0). Prints no ENOB
  table; qualitative; defers ENOB to hardware. Aligned. Candidate adds: gain-vs-impedance,
  100×-vs-31×, the schematic, a short "what ENOB really means / ~11–12 bit reality" sidebar.
- **P2AN003 (DAC)** — RELEASED. Prints no ENOB figure, defers to hardware. Aligned. (Ties to
  the paused IOSP expert Q5 "DAC ENOB printable figure" — this feedback *confirms* the
  defer-don't-print decision was right.)

**C. Cross-cutting:**
- The paused IOSP expert-review queue Q5 (DAC ENOB) is effectively **answered** by this
  feedback: don't print a fabricated ENOB; if a number is given, it's a tiered community/bench
  figure.

### Recommended response (sequencing — NOT yet executed)

1. **Terminology fix (authority-backed, do first):** across IOSP + Green Book + the shipped
   YAML, relabel the "ENOB" decimation columns as **"sample resolution (bits)"**, drop/reframe
   the **SINC3 doubling** column, keep the SINC2 "+1 bit" nominal claim, and add one caveat line
   that *effective* (measured) resolution is lower and unmeasured here (~11–12 bits in practice
   per community measurement). Cite: IEEE ENOB definition + Chip's "need to change the docs."
2. **Hardware-fact enrichment:** add gain-dependent input impedance (≈450 k/gain, buffer at high
   gain) and the "100× ≠ better than 31×" guidance to IOSP §16.8 + P2AN001. Tier the empirical
   claims as community/bench, or gate on a hardware run.
3. **Diagrams:** redraw evanh's sigma-delta front-end schematic + the summing/math diagram as our
   own TikZ (circuitikz), place in IOSP §16.1, Green Book ADC section, and P2AN001.
4. **Log to registers:** YAML change → `P2KB-CORRECTION-FINDINGS.md`; released-manual changes ride
   the next IOSP release (minor bump); provenance = this capture doc.

### Decisions locked (Stephen, 2026-07-06)

1. **Green Book is RETIRED — drop it.** `p2-smart-pins-tutorial` is in PUBLICATION-ROSTER
   "Abandoned — retired," superseded by the IOSP User Guide. Remove it from the affected-docs
   set and stop surfacing it in research. **Corrected fix scope = IOSP User Guide + the shipped
   `smart-pin-11001-adc-external-clock.yaml`** (+ optional P2AN001 enrichment).
2. **Ship NO community numbers.** No "~11–12 ENOB," no "17-bit," no 450 k/4.5 k *as measured
   figures*, unless we reproduce them ourselves. The terminology correction needs no number and
   is stronger for it (relabel + remove doubling + caveat). Optional: Stephen may reproduce a
   *ballpark* on hardware **only if it's little-external-hardware and meaningfully strengthens the
   position** — acknowledged to be instance-specific / ballpark, not a spec.
3. **All swept documents ship as PATCH releases** after the adjustments (release model for this
   response).
4. **Diagrams: certified sources ONLY.** The two forum diagrams (evanh's) are community-produced
   → **not** publishable even as redraws. Certified candidate CONFIRMED IN-REPO: the **P2 Datasheet**
   (`external-inputs/archive/Propeller2-P2X8C4M64P-Datasheet-20221101.pdf`) and **Silicon Doc v35**
   (5-part PDF under `sources/silicon-doc/`). Our datasheet extraction notes flag *"Equivalent
   Schematics for Pin Configurations"* and *"ADC/DAC circuit details"* as diagrams present in the
   original but never extracted. **Next diagram step:** extract those figures, verify whether they
   show the sigma-delta front end; redraw as TikZ ONLY what the certified source depicts.

### Revised recommended response (post-decisions)

- **Terminology correction (number-free):** IOSP ch.16 table → relabel ENOB columns as *sample
  resolution (bits)*; delete the SINC3 "doubling" column; keep SINC2 "+1 bit" nominal; add a
  one-line caveat that measured effective resolution is lower and not characterized here. Same fix
  to the shipped YAML. Authority: IEEE ENOB definition + Chip's "need to change the docs."
- **Hardware-fact enrichment (qualitative only):** add gain-dependent input impedance ("scales down
  roughly with gain — buffer high-gain inputs") and "highest gain ≠ best resolution" as *qualitative*
  guidance, no numbers, unless reproduced.
- **Diagrams:** pending certified-source extraction (step above).
- **Releases:** IOSP + YAML corrections → patch releases; log YAML change to `P2KB-CORRECTION-FINDINGS.md`.

### Diagram research — CERTIFIED SOURCE FOUND (2026-07-06)

Rendered the ADC/analog pages of both certified PDFs at 200 DPI. Both certified sources carry the
same **"Equivalent Schematics for Each Unique I/O Pin Configuration"** set:

> **Tooling note (corrected after full Scope-A extraction):** the two certified PDFs are built
> differently. The **P2 Datasheet is vector line-art** — the 2025-09 `pdfimages` extraction MISSED
> the entire equivalent-schematics section (incl. all ADC/DAC panels); page-render was required.
> The **Silicon Doc v35 is DOCX-derived and embeds its schematics as raster**, so `pdfimages`
> *had* already captured them (under generic "Technical Diagram" labels). So the "vector was
> missed" root-cause applies to the **datasheet only**, not the Silicon Doc.

- **P2 Datasheet** `Propeller2-P2X8C4M64P-Datasheet-20221101.pdf` — p26 single I/O pin circuit;
  **p31** the ADC/DAC panels. Explicit *"Copyright © Parallax Inc. 2022/11/01"* footer → best
  provenance.
- **Silicon Doc v35** Part4 — p77 (Part4 p6) single I/O pin circuit; **p82 (Part4 p11)** ADC/DAC panels.

**Certified, publishable content (block/configuration level):**
1. **Top-level I/O pin block diagram** — Vxxyy/VIO, M[12:0], DIR/OUT/IN, CLK, PIN, ADJACENT PIN, GND.
2. **`%100 — ADC with Optional Drive`** — shows the **Δ-Σ ADC** block, PIN→Δ-Σ ADC→BIT→IN, select
   S2/S1/S0 = M9/M8/M7, and the **source/gain table**: `000 GND · 001 VIO · 010 Float · 011 1× ·
   100 3.2× · 101 10× · 110 32× · 111 100×`. → directly supports feedback #1 (GND/VIO sources) and
   #2 (gain steps).
3. **`%101 — DAC with Optional ADC`** — DAC block + Δ-Σ ADC + impedance table (990/600/124/75 Ω).
4. **`%11000 — Level Comparator with 1.5k`** — DAC→COMPARE→IN structure.

**NOT in any certified source (community/bench only — do NOT publish):** the transistor/resistor-level
**internal** of the sigma-delta modulator — the feedback-DAC + resistor network, the 450 kΩ→4.5 kΩ
input-impedance detail, the separate calibration resistors. That level exists only in evanh's forum
diagrams. **Consequence:** a certified TikZ redraw can show the ADC at *block/config* level (what's
connected to what, source + gain select) but NOT the internal modulator detail the feedback's fact
#2/#3 numbers come from. Those numbers stay out unless hardware-reproduced.

Rendered evidence (working, not committed): `/tmp/adc-research/` — datasheet p28–31, silicon-doc
Part4 p5–13.

**Scope-A full figure extraction — COMPLETE (2026-07-06).** Both certified docs re-cataloged via
vector-safe page-render (`pdftoppm @150 DPI`), verified (entry counts, renders present, no broken
embeds):
- **Datasheet:** `engineering/ingestion/sources/p2-datasheet/assets/images-20260706/`
  `Propeller2-P2X8C4M64P-Datasheet_image_catalog.md` — 16 figure pages → **38 figures** (P2DS-R001–R038).
  Genuinely *supersedes* the 2025-09 embedded-image catalog (it had missed all vector schematics).
- **Silicon Doc v35:** `engineering/ingestion/sources/silicon-doc/assets/images-20260706/`
  `P2-Silicon-Doc-v35_image_catalog.md` — 18 figure pages (P2SD-R001–R018). *Complements* (does not
  supersede) the 2025-09 catalog; adds full-page context, ASCII/text figures, and rich descriptions.
- Old `images-20250906/` folders retained for history.

**Certified ADC/analog figure inventory (redraw targets):**
- Datasheet **p31** — R030 `%100` ADC w/ Optional Drive (Δ-Σ + SSS gain table), R031 `%101` DAC w/
  Optional ADC (ZZ drive table), R032/R033 `%11000/%11001` Level Comparator 1.5k.
- Datasheet **p32** — R034–R037 `%11010/%11011/%111M0/%111M1` Level Comparators (local/separate feedback).
- Datasheet **p26** — R013 single I/O pin circuit (master front-end); **p30** R026–R029 Comparator modes.
- Silicon Doc **Part4 p11/p06** mirror the ADC/DAC panels + pin block diagram (raster equivalents).
- All **block/config level** — none show the internal modulator (feedback-DAC + resistor network,
  450 k/4.5 k impedance). That remains community/bench only.

### Still-open (facts to gather / decisions)
- **Extraction/catalog scope decision — RESOLVED (Stephen chose Scope A; DONE 2026-07-06).** Full
  figure sweep of both certified docs completed + verified; new dated catalogs are the source of
  truth (see above).
- If Stephen opts to reproduce a ballpark ENOB/impedance figure on hardware, that becomes an
  EF-ledger empirical item (own test + golden analysis) before any number is published.
