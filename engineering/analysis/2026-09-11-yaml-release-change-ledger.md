# YAML release change ledger — `v1.18.1..HEAD`

**What this release does, in one sentence.** It removes 40 places where the KB stated an *opinion*
(star ratings, scores, grades) instead of a *fact*, deletes one uncited derivation, and corrects one
wrong maximum — and it adds nothing new.

**How to read this document.** It is organised by *what a reader of the KB will now find*, not by
finding number. Every removal is shown verbatim, next to **the line that already answered the same
question** — because the only thing that makes a removal safe is what remains in its place. If
nothing remained, it is in §3 (Holes), which is the section to read first if you are short of time.

**Range.** `v1.18.1` (`57ef2e0d`, 2026-09-10) `..` `617c69d9` (2026-09-11). Measured on disk
2026-09-11; every count re-derived at HEAD.

**Supersedes** `2026-08-27-yaml-release-change-ledger.md`, archived to `analysis/archived/`
byte-identical to its last committed revision. *(That one was spent: its range `v1.17.0..b0057ec1`
shipped on 09-10 as v1.18.0/v1.18.1. A release ledger expires the moment its range ships.)*

---

## §1 — The shape, before any detail

```
20 files      +8 / −66 lines      3 commits touching deliverables/ai/P2
```

**This release is almost entirely subtraction.** 66 lines out, 8 in — and of those 8, **four** are
rewrites of prose lines, **two** are relabelled section banners, and **two** are added explanatory
clauses. No new claim about the P2 enters the KB in this release. If the diffstat showed meaningful
addition, something would be wrong.

---

## §2 — What left, and what now answers the same question

### 2a · Eight add-on boards — the bare "how educational is it" score

**Removed** (one line per file):

```yaml
educational:
  value: "very_high"      # addon-av-breakout, addon-led-matrix,
  value: "high"           # addon-mini-prototyping, addon-serial-device,
                          # addon-control-board, addon-digital-video-out,
                          # addon-goertzel-touch, addon-serial-host
```

**What still stands in the same block** — this is the whole block in `addon-led-matrix.yaml`, after:

```yaml
educational:
  complexity_level: "intermediate"
  concepts_taught:
    - "Charlieplexing (tri-state LED multiplexing)"
    - "Persistence of vision and refresh timing"
    - "Tri-state pin control (HIGH / LOW / float)"
    - "Bitmap/font rendering"
```

`very_high` told an agent nothing it could act on. `complexity_level` plus a named concept list
tells it what the board actually teaches. **The block got more useful by losing a line.**

### 2b · Six Edge / Eval board files — the "QUALITY RATINGS" block

**Removed**, in `edge-standard-module.yaml` (the largest case — four keys and their banner):

```yaml
# =============================================================================
# QUALITY RATINGS
# =============================================================================
quality_rating: "production"
recommendation_score: 5
educational_value: "high"
production_readiness: "excellent"
```

**What already answered those questions, and still does:**

| the removed key asked | what answers it now | where |
|---|---|---|
| is it production-grade? | `status: "active_production"` | `:23` |
| what is it for? | `use_cases:` (a list) | `:278` |
| who/what is it aimed at? | `target_applications:` (a list) | `:290` |

Same pattern in `edge-32mb-module`, `edge-standard-breakout`, `edge-mini-breakout`,
`edge-breadboard-carrier`, `p2-eval-board`. In `edge-32mb-module` the banner was **relabelled**
`CLASSIFICATION` rather than deleted, because `memory_class: "high_capacity"` remained under it —
that one is a fact.

⚠ **The banner itself was part of the defect.** A section literally headed `QUALITY RATINGS` is an
invitation to add more of them. It is gone from both modules.

### 2c · The compatibility matrix — six rows, two grades each

**Removed** from each of six module/carrier combinations:

```yaml
rating: "5_stars_perfect"          cost_efficiency: "optimal"
rating: "2_stars_limited"          cost_efficiency: "underutilized"
rating: "5_stars_professional"     cost_efficiency: "professional_premium"
rating: "3_stars_oversized"        cost_efficiency: "acceptable_but_oversized"
rating: "5_stars_perfect"          cost_efficiency: "optimal_memory_solution"
rating: "2_stars_overkill"         cost_efficiency: "expensive_overkill"
```

**What each row already carried, untouched** — this is one full row, after:

```yaml
- module: "P2-EC (Standard Edge Module)"
  carrier: "64019 (Mini Breakout)"
  module_free_pins: "P0-P55 (56 fully free; P56-P63 routed to peripherals)"
  carrier_header_pins: "P0-P31 and P56-P63 (40) at four 2x6 accessory headers plus one
    programming header; P32-P55 reach no header but may be picked up with jumper wires
    on the bottom side of the PCB"
  use_case: "Simple projects only"
```

The grade sat *directly beneath the facts that would have justified it*. An agent choosing a
carrier needs the pin story, and the pin story never left. **`expensive_overkill` is an opinion
about someone else's product**, published as knowledge-base fact.

### 2d · Two code examples and the schema field that required the score

**Removed:**

```yaml
educational_value: 10        # smart-pins-001-basic-io
educational_value: 9         # smart-pins-002-button-reading
```

and in `code-example-schema.yaml`, the schema field that *mandated* them plus the threshold that
gated on it:

```yaml
educational_value:
  type: "integer"
  required: true
  range: [1, 10]
  description: "How valuable for learning P2 programming"
...
minimum_educational_value: 5
```

⭐ **This is the one removal that prevents recurrence rather than just cleaning up.** The schema
said every code example *must* carry a 1-10 learning score. While that field was `required: true`,
the next example written would have had one — the defect was specified. Removing the two scores
without removing the schema field would have left the generator intact.

### 2e · `p2-eval-board.yaml` — rewritten, not removed

The only place where the fact was worth keeping and only the adjective had to go:

| before | after |
|---|---|
| `beginners: "Ideal - no hardware selection needed"` | `"No hardware selection needed -- board, USB and power are one part"` |
| `educators: "Perfect - built-in teaching aids"` | `"Built-in teaching aids (LEDs, buttons, headers) need no add-on to demonstrate"` |
| `professionals: "Good for rapid prototyping"` | `"Rapid prototyping -- all 64 pins at accessory headers, no carrier to select"` |
| `production: "Not suitable - use Edge modules"` | `"Not a production form factor -- the Edge modules are the deployable part"` |

Each line kept its routing value and lost the grade. *Ideal*, *Perfect*, *Good* and *Not suitable*
were the defect; everything after the dash was real.

### 2f · Two app-note companions

**`p2an001` — one uncited derivation removed:**

```yaml
raw_sample_rate_sps: 1_562_500        # 200_000_000 / 128
```

Arithmetic with a comment where a citation belongs. The ingestion tree was searched in three
spellings and **no Parallax source states this figure**. P2AN003 had already deleted the identical
construction, so the region was applying two opposite rules to one shape — that inconsistency was
the defect, not the number. **Nothing replaces it:** the note's own text does not depend on it.

**`p2an004` — a file that said three different things about itself.** It claimed it deliberately
does not restate the sensor's datasheet figures, and then restated them. Now:

| removed | kept, and why |
|---|---|
| `VDD = 5 V; 2.7-5.5 V operating (works at 3.3 V)` | — genuinely restated, no use here |
| `dark 0.4-10 Hz` | — same |
| | `fO = 250 kHz typ at Ee = 430 uW/cm^2, lambda_p = 635 nm` **kept** — the note's own `Ee = freq * 430 / 250_000` formula and its `CAL_UW`/`CAL_HZ` constants scale from it. Deleting it would have stranded the formula and recreated the p2an001 defect one line away. |

**`p2an004` — a wrong maximum, corrected:**

```yaml
-  runs at a legal 200 MHz (300 MHz max)
+  runs at 200 MHz, well inside the datasheet's PLL system-clock range
+  (180 MHz typical, 320 MHz maximum -- AC Characteristics) ...
```

F-413 had already ruled this figure wrong (the datasheet maximum is **320 MHz**) but was scoped to
P2AN001 and never looked at this companion.

⭐ **Worth knowing before anyone "cleans up" 300 MHz elsewhere:** the figure is genuinely sourced
three times and never as a maximum — Parallax's own *"Overclocking possible beyond 300 MHz"* feature
line on four board files, the compiler's accepted ceiling (`special-configuration-symbols.yaml`,
which correctly cites the datasheet's 200 MHz direct-XI limit beside it), and an example
`clock_freq` in two more. All four are correct and were left alone. **The defect was the role the
number was given, not the number.**

---

## §3 — Holes: removals that left nothing behind

**None.**

That is a measured claim, not a reassurance. The check applied to every one of the 40 removals was:
*does this file still answer the question the removed key was pretending to answer?* The answering
line is shown in §2 for each group. The two files that lost the most were checked individually:

| file | keys lost | what answers them now |
|---|---:|---|
| `edge-standard-module.yaml` | 4 | `status: "active_production"` · `use_cases:` · `target_applications:` |
| `p2-eval-board.yaml` | 3 + 4 rewritten | `status: "active_production"` · `production_readiness: "not_applicable"` (kept) · the four rewritten `target_audience` lines |

**Zero sites required a replacement fact to be written**, because in every case the fact was already
present. That is the argument that the grades were never carrying information — they were sitting
next to it.

---

## §4 — What looks like it should have gone, and deliberately did not

The near-misses, so you are not left wondering whether they were missed:

| kept | why |
|---|---|
| `addon-motor-driver.yaml:155` — `rating: "VIN and output-channel spring terminal blocks rated 32 A / 400 V"` | an **electrical spec**. The bare-key grep catches it by accident. |
| `production_readiness: "prototype_platform"` ×3 · `"not_applicable"` ×1 | **categorical facts** — they say what a board is *for*. Only `"excellent"` was a grade. |
| `edge-breadboard-carrier.yaml:225` — `educational_value:` | heads a block of `learning_objectives` and `course_integration` lists. The key *name* resembles the class; the content is facts. |
| `complexity_level` / `concepts_taught` in all 8 add-on files | utility, which the rule explicitly permits. |
| ~299 sites matching a bare `value:` key | an earlier over-broad sweep matched these and was **thrown out**; the overwhelming majority are legitimate. Not re-opened. |

---

## §5 — Still yours, and unchanged by this range

- **F-375's other half — the 383-file rename.** A scope call, not research.
- **The delivery-strip decision.** `fetch-kb-file.sh` strips five metadata fields from every
  delivered file. Of 396 `documentation_source` values, **363 (91%) are real provenance** — *PASM2
  Manual 2022/11/01 Pages 31-147*, *Silicon Doc v35*, *P2 Instructions v35 CSV* — and only 33 are
  bookkeeping tokens (`enhanced` 16, `original` 15, `code_analysis` 1, `redirect_stub` 1).
  **So the set satisfies cite-or-omit on disk and is delivered not satisfying it.** Every gate we run
  reads the tree, where the citation is still present; the consumer reads the stream, where it is
  not. The gate half of this is fixed (below); which way to resolve the strip is yours.
- **The release itself** — commit, tag, push. Nothing here is tagged or pushed.

---

## Appendix A — Counts

| key shape | sites removed |
|---|---:|
| `rating` | 12 |
| `educational_value` | 8 |
| `educational: value:` (nested) | 8 |
| `recommendation_score` | 6 |
| `quality_rating` | 6 |
| **subtotal — F-374 class** | **40** |
| `cost_efficiency` | 6 |
| `production_readiness: "excellent"` | 2 |
| `target_audience` prose | 4 *(rewritten, not removed)* |

Plus the `educational_value` schema field, its `minimum_educational_value` threshold, one uncited
derivation, one restated figure pair, and one wrong maximum.

## Appendix B — Where a record disagreed with the artifact

Three counts moved between filing and fixing. Recorded rather than smoothed, because the drift is
the point — **a finding written from a grep is a map, not an inventory:**

| record | said | measured at HEAD |
|---|---|---|
| F-374 | 40 sites / 18 files | **42 / 19** at re-derivation (`educational_value` had grown 7 → 9); 40 deleted, 2 legitimate |
| F-375 | 397 `documentation_source` values / 396 files | **396 / 395** |
| F-425 | two prose lines | **four**, and it never noticed the `QUALITY RATINGS` banner |

## Appendix C — Gate state at HEAD

```
verify-yaml-format.py      1133/1133 parsed clean
validate-crossref-keys.py  100% top-level resolution
validate-dod-release.py    12/12 PASS — "READY FOR RELEASE"
```

`validate-dod-release.py` gained its twelfth check in this range: the duplicate-key audit, which had
been armed and returning 0 across 1132 files while **nothing ran it**. Its `validate_metadata_filter`
was also repaired to parse the *delivered* payload rather than classify the lines it removed.
