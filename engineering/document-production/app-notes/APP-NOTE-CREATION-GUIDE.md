# P2 Application Note — Creation Guide

**Applies to:** every document in `engineering/document-production/app-notes/` (the `P2ANxxx` series)
**Purpose:** define what a P2 application note *is*, how it is structured, the pedagogy behind that structure, and how its content is sourced and verified
**Created:** 2026-06-27
**Companion:** `APP-NOTE-VOICE-GUIDE.md` (how it reads). This guide governs *what goes where and why*; the voice guide governs *the prose*.

---

## 1. What an application note IS (and is NOT)

An application note sits in the gap between the reference manuals and the DeSilva-style tutorial. It is a **third document class** with its own contract with the reader.

**An app note IS:**
- **Application-driven.** It is organized around an outcome a developer wants ("generate PWM with no cog overhead," "read an analog voltage," "run two tasks in one cog"), not around the silicon taxonomy.
- **Focused and deep.** A note goes deep on *one thing* — either a single technique taught through one worked build, or a single capability-domain taught through a small set of runnable recipes the reader chooses among. It exhausts the *use*, not the silicon spec. (Two archetypes — see §1.1.)
- **A complete worked example.** The centerpiece is one runnable, validated program the reader can build on.
- **Empirically grounded.** It shows what success looks like and how to confirm it.
- **Short.** Typically 5–20 pages. If it's growing past that, it's probably two notes, or it's becoming a manual chapter.

**An app note is NOT:**
- **A reference manual.** It does not enumerate every mode or every bit. It uses the modes the build needs and *points to* the manual for the full enumeration.
- **A tutorial.** It does not teach the P2 from zero or walk a multi-lab progression. It assumes stated prerequisites and links to the tutorial/manuals for background.
- **A datasheet.** Hardware/electrical specifications live in `engineering/document-production/datasheets/`.

> **The test:** if you removed the worked example(s) and the note still made sense, it's a manual chapter, not an app note. If the note teaches the whole subsystem rather than *using* it, it's a manual chapter. An app note earns its name by being built around *doing* — one technique, or one capability-domain's worth of runnable recipes.

### 1.1 Two archetypes

A note takes one of two shapes. Both obey everything above; they differ only in how many builds carry the note.

- **Single-build** *(the default).* One technique, one centerpiece worked program, exhausted concept-through-adaptation. The canonical structure (§4) maps to it directly: one "Build It," one "Verify," one "Adapt It." Most notes are this. *(e.g. "generate PWM with no cog overhead.")*
- **Techniques-catalog.** One capability-*domain* taught through a **shared conceptual base** plus a small set of complete, runnable recipes the reader **selects among** by need. The P1 AN001 (Counters) genre model is this shape, and so is P2AN000 (instrumentation ADC: single-pin → 3-pin → filtered → range-extended). It is *not* a license to tour a subsystem.

Two guardrails keep a catalog an app note and not a manual chapter:

1. **Shared conceptual base first.** All recipes build on **one** "The Idea / How It Works" foundation, taught once, never re-explained per recipe. The recipes vary the *application*, not the mechanism.
2. **Every technique is a complete, verified, runnable recipe — plus a decision aid.** Each catalog entry is a build-it + verify (compiles under `pnut_ts`, shows expected output), not a described mode. A **decision table** (need → technique) gives the reader the "which one do I use" spine. If an entry is a mode description with no runnable recipe, it's manual-chapter content — cut it or move it to the manual.

**Decomposition rule (both archetypes).** Foundation belongs in the **manual**; the note **applies** it. When a note needs a mechanism the manual under-documents, *enrich the manual* and have the note cite it — do not grow the note into the manual. (P2AN000 rests on the enriched I/O & Smart Pins User Guide Ch.16; the note teaches the *use*, the chapter owns the *mechanism*.)

---

## 2. The P1 inheritance — what we keep, what we add

The Parallax P1 application notes (ingested 2026-06-27 as pattern donors — see `engineering/ingestion/P1-DOCUMENT-LINEAGE.md` §"App-note → P2 recreation candidacy") are an excellent genre model. We inherit their strengths and add the scaffolding they lack.

### 2.1 What the P1 notes do well (KEEP)

Drawn from AN001 (Counters), AN014 (Coroutines), AN008 (Sigma-Delta ADC):

- **The Abstract convention.** A 2–4 sentence bolded abstract stating the capability *and* its value. (AN001: "Use the counter modules as flexible subsystems that can often take the place of dedicated cogs or peripheral hardware, reducing code complexity and component count.") This is the single best thing the P1 notes do — keep it verbatim as a convention.
- **Single-feature focus.** Each note owns one subsystem and exhausts the *use*, not the spec.
- **Complete, runnable examples** on a *named* platform ("designed to run on the Propeller Demo Board… modified for other platforms by changing the CON section").
- **Worked numeric examples.** "If FRQA is `$8000_0000`… the resultant output on APIN will be 40 MHz or ½ the system clock." Concrete numbers, every time.
- **Empirical grounding.** Every behavioral claim is anchored to a measured scope capture.
- **Applications framing.** AN001's Table 3 ("Counter Modes Application Examples") maps each mode to real uses — outcome-first thinking.
- **Differentiation by contrast.** "DUTY modes on the surface appear similar to NCO… however the waveforms they produce are very different."
- **Honest gotcha lists.** AN014's numbered "points worth noting" (shared `acc` across `swap`, never rely on C/Z across a coroutine switch).

### 2.2 What the P1 notes lack (ADD)

These are pedagogically-motivated additions, not stylistic preferences:

| P1 weakness | Our addition | Why (learning science — §3) |
|---|---|---|
| **Register-first.** AN001 dives into CTRA bit fields on page 2, before the reader has a mental model. | A **"The Idea"** section: the concept *before* any register detail. | Advance organizer (Ausubel); conceptual model before mechanism (Norman). |
| **No stated outcome.** The reader doesn't know up front what they'll be able to *do*. | A **"What You'll Build"** line in the Abstract/opening. | Goal-orientation; problem-based learning anchors effort in a target. |
| **No prerequisites.** Assumes unstated background. | A **"Prerequisites & Hardware"** block with links. | Prior-knowledge activation; findability. |
| **No reader-side verification.** Scope captures show *the author's* result; the reader isn't told how to confirm *theirs*. | A **"See It Work / Verify"** section with expected output + a failure branch. | Feedback in the learning loop; trust. |
| **Gotchas scattered.** Notes appear inline, easy to miss. | **Consolidated, marked** pitfalls/tips (⚠️ 💡 🔧 🔍). | Cognitive load; findability of expert knowledge. |
| **Conclusion = capability list.** No consolidation of the concept. | A **conclusion that consolidates the idea**, then points onward. | Retrieval/consolidation. |
| **No "where next."** | **Resources + cross-references** to the manuals and related notes. | Builds the mental map across the doc set. |

---

## 3. Pedagogical framework

App notes optimize for a specific outcome: **the reader builds the thing once, understands it well enough to adapt it, and knows where to go for more.** That is neither the tutorial's "learn the whole subject" nor the manual's "find one fact fast." The structure (§4) is built from learning principles selected for *that* outcome.

| Principle | Source | How the app-note structure applies it |
|---|---|---|
| **Advance organizer** | Ausubel, 1968 | The Abstract + "The Idea" give the big picture and the mental model before any detail. |
| **Conceptual model first** | Norman, 1983 | "The Idea" precedes "How It Works" — you understand *what* before *how the bits are arranged*. |
| **Worked-example effect** | Sweller & Cooper, 1985; Renkl, 1997 | The note *is* a worked example. Novices learn a new schema far faster from a complete worked solution than from problem-solving unaided. |
| **Concreteness fading** | Goldstone & Son, 2005 | "Build It" is fully concrete (real pins, real numbers); "Adapt It" generalizes to the parameter space *after* the concrete anchor is set. |
| **Cognitive apprenticeship** | Collins, Brown & Newman, 1989 | The walkthrough makes the expert's reasoning visible ("we back up the accumulator so the edge lands N cycles from now"), not just the final code. |
| **Self-explanation** | Chi et al., 1989 | "How this code works" prompts the reader to connect each step to the concept — the PE Labs "How X.spin Works" donor pattern. |
| **Feedback loop** | (general) | "See It Work / Verify" closes the loop: the reader gets a concrete success signal and a diagnosis path for failure. |
| **Dual coding** | Paivio, 1971 | Diagram (TikZ) + prose + code + measured output — four representations of the same mechanism. |
| **Cognitive load** | Sweller, 1988 | One technique per note; consistent section order; markers that compress wisdom into findable notes. |
| **Transfer** | (general) | "Adapt It" explicitly targets near transfer — change this, vary that, here's where it breaks. |

These are the same classic frameworks the manual creation guides cite; the *selection and ordering* differ because the app note's job differs.

---

## 4. The canonical structure

Every `P2ANxxx` note follows this skeleton. Sections may be merged or lightly reordered for a given topic, but the **flow — orient → concept → mechanism → build → verify → adapt → consolidate** is fixed, because it is the pedagogy.

```
FRONT MATTER
├── Title + AN number + version
└── Applies-to line (P2 silicon, Spin2/PNut version, board/hardware)

1. ABSTRACT                  [teaching]   2–4 sentences: capability + value (P1 convention)
2. WHAT YOU'LL BUILD         [teaching]   the concrete outcome — the thing that runs at the end
3. PREREQUISITES & HARDWARE  [reference]  what to know first (links), board/parts, version gate
4. THE IDEA                  [teaching]   the mental model BEFORE any register detail
5. HOW IT WORKS              [reference]  the mechanism: modes/registers/instructions, diagram,
│                                          worked numeric example
6. BUILD IT                  [build]      one complete, runnable, pnut_ts-validated program,
│                                          walked through ("how this works")
7. SEE IT WORK / VERIFY      [empirical]  expected output (DEBUG/scope/logic) + failure branch
8. ADAPT IT / GOING FURTHER  [build]      the parameter space, variations, where it breaks
9. PITFALLS & NOTES          [markers]    consolidated ⚠️ 💡 🔧 🔍
10. CONCLUSION               [teaching]   consolidate the concept (not just a capability list)
11. RESOURCES                             example ZIP, related OBEX, related manuals/notes
12. REFERENCES                            numbered
13. REVISION HISTORY
14. (copyright / disclaimer per Parallax convention)
```

**Section notes:**

- **§2 What You'll Build** can be a single italic line right under the Abstract; it does not need its own heading on a short note. Its job is to put the outcome in view immediately.
- **§5 How It Works** is the one section that reads like a manual. Borrow the reference register here, and *cite the manual* for the full enumeration rather than reproducing it.
- **§6 Build It** is the centerpiece. The program is complete and runnable on the stated board. Every code block compiles under `pnut_ts` (§5 verification). The walkthrough explains *why*, never restates the instruction.
- **§7 Verify** is non-negotiable. A note without a verification step is not trustworthy. Show the expected DEBUG window / capture, the expected value, and at least one honest failure branch.
- **§8 Adapt It** is what separates an app note from a recipe — it teaches the reader to *change* the result, which is the actual point of a note.
- **Catalog mapping (§1.1).** This skeleton is written for the single-build archetype. A techniques-catalog keeps §1–§5 as the shared base, then **repeats §6–§7 (Build It + Verify) per recipe** after a decision table; §8 becomes "which recipe / going further." The fixed flow — orient → concept → mechanism → build → verify → adapt — is per-recipe once the shared base is set.

---

## 5. Source & verification protocol

App notes are downstream of the trust chain (`Trusted Sources → Trusted YAML → Trusted Documentation`). The same hallucination-prevention discipline the manuals use applies — **hallucinations happen at the moment of writing, not after.**

### 5.1 Authority hierarchy

When sources conflict, in order:
1. **Empirical / hardware-verified** findings (`engineering/ingestion/external-sources/hardware-verification/` — the EF ledger). Ground truth; outranks everything.
2. **P2 Knowledge Base YAML** (`deliverables/ai/P2/`) — the curated, version-tracked authority. Validate idioms against the KB *first* (it is what the code was generated from).
3. **`pnut_ts` compiler** — for code correctness and symbol↔value checks (compile DEBUG code with `-d`).
4. **Silicon / Spin2 documentation** — for mechanism and encoding.
5. **Official ROM / Parallax example code, then community (OBEX)** — for proven usage patterns.

### 5.2 Verification rules

- **Every code example compiles under `pnut_ts`** (with `-d` when it contains `debug()`), and is validated against the KB idioms before the compiler — never prefer a compiler guess over the YAML authority.
- **Every capability claim traces to a source.** No inference, no "reasonable" behavior invented to fill a gap. If it can't be sourced, it's a *finding* (route to `engineering/operations/P2KB-CORRECTION-FINDINGS.md`), not a sentence in the note.
- **Worked numbers are derived from an authority** (compiler/silicon/KB), not computed by reasoning and asserted.
- **Verification output is real.** The expected DEBUG/scope result shown in §7 must come from an actual run (Stephen runs hardware/GUI externally — see the hardware-verification model), not an imagined screenshot.

### 5.3 Red-flag phrases (stop and verify)

Same family the manuals flag: "automatically," "also provides," "side effect," "eliminates," "synchronizes," "enables" (vague capability). When you're about to write one, find the exact source line first or don't write it.

---

## 6. Conventions

### 6.1 Naming & numbering

- **Series prefix `P2AN` + a three-digit, zero-padded number, no separator:**
  `P2AN000`, `P2AN001`, … This is **our** P2 series.
- **P1 notes keep their bare `ANxxx`** (`AN001`–`AN019`) — that is **Parallax's
  authentic published designation**, preserved (we do not rename others'
  published documents; same provenance discipline as the trust chain). The
  `P2AN` / `AN` asymmetry is **deliberate** — it encodes *ours vs. theirs* and
  prevents `AN001` collisions across the two corpora we both hold.
- **Numbering is sequential and assigned at *commit-to-production*, not to
  candidates.** The number is a **stable identifier + build-order provenance —
  NOT a taxonomy.** Do **not** band numbers by family, and do **not** pre-number
  speculative candidates (a cut candidate would strand a permalink). Family /
  topic organization lives in the **roster / index** (`README.md` +
  `engineering/analysis/p2-app-note-roster.md`), never in the number — identity
  and organization are kept separate.
- **The published series starts at `P2AN001`** (matching Parallax's P1
  `AN001`–`AN019`, which had no `AN000`). `P2AN000` was the *experimental
  placeholder* — now **retired**. The existing ADC-instrumentation draft (the
  exemplar this guide cites) **renumbers `P2AN000` → `P2AN001`**; **CORDIC is
  `P2AN002`**. The renumber is a tracked repo-wide rename (folder + ~15 refs
  across app-notes, the `workspace/` render, the IOSP render, and the analysis
  docs) — this guide's `P2AN000` citations become `P2AN001` in the same pass.
- **Recreations of P1 notes do *not* automatically inherit the P1 number.** A P2
  recreation of P1's `AN001` (Counters → Smart Pins) is a *new* note with its own
  `P2AN` number; the lineage is recorded in `P1-DOCUMENT-LINEAGE.md`, not encoded
  in the number. (P1 `AN`-numbers and P2 `P2AN`-numbers are independent sequences.)
- Folder names may carry a topic slug once the topic is fixed: `P2AN007-smart-pin-pwm/`. Until then, the bare `P2ANxxx/` folder is fine.

### 6.2 Per-note folder layout

```
app-notes/
├── APP-NOTE-CREATION-GUIDE.md      ← this file (shared, governs all notes)
├── APP-NOTE-VOICE-GUIDE.md         ← shared voice (governs all notes)
├── README.md                       ← series index + pipeline from P1 lineage
└── P2ANxxx/
    ├── opus-master/                ← THE canonical source (edit here, never the workspace render)
    │   └── P2ANxxx.md
    ├── P2ANxxx-NOTES.md            ← working notes: topic, source traceability, open questions
    └── audit/                      ← (added at audit time) findings + verification log
```

The **opus-master is canonical** — the production workspace render is generated and overwrites edits. Edit `opus-master/`, never the workspace copy. (Same rule as the manuals.)

### 6.3 Production

App notes are short and use the **shared P2KB platform stack** (the same `p2kb-platform-*` templates/filters the twin manuals consume), via the standard `prepare-manual` → PDF Forge path. They follow the **same Three-Folder Rule as the manuals** (see `../PDF-PRODUCTION-ARCHITECTURE.md`): authoring in `app-notes/<name>/opus-master/`, then `workspace/<name>/` + `outbound/<name>/` keyed by canonical name. The opus-master splits into `front-matter.md` (the cover) + the body file; an `assemble-manual.sh` in the workspace concatenates them (its `OPUS_MASTER` path is the bridge from the `app-notes/` tree to the shared workspace).

Production specifics, **settled by the P2AN000 pilot (2026-06-28)**:
- **Template** — a thin class template `p2kb-appnote-reference.latex` + `p2kb-appnote-local.sty` that loads the shared `p2kb-platform-foundation`/`-content` stack. Future notes clone these. The local layer carries app-note deltas only: unnumbered short-doc headings (`secnumdepth 0`), and `\newunicodechar` substitutes for the four marker emoji (⚠️/💡/🔧/🔍 — absent from IBM Plex; mapped to colored amssymb shapes, matching the platform's missing-glyph pattern).
- **Cover** — the **same family artwork** (`book-artwork.png`) + title block as the manuals. The manuals' bottom-of-cover Parts/Chapters box is **repurposed** to an app-note **“What You'll Build”** box (the outcome + the technique list + an applies-to line) — a manual's chapter taxonomy does not fit a short, Part-less note.
- **Code-line budget** — inherit the platform **K = 76** and the platform code-box family; do not diverge the code font.
- **Marker authoring caveat** — the platform `mnemonic-bold` filter bolds bare PASM2/Spin2 mnemonics even in prose, and its English-word disambiguation is imperfect (it false-bolds e.g. “ones”). Avoid bare mnemonic-words as plain English in app-note prose (write “samples” not “ones”).
- **Cross-reference filter** — clickable Chapter/§ refs (`p2kb-platform-crossref`) is the planned next adoption per the platform crossref-filter tracker (opt-in, with a visual audit).

Code does **not** wrap; the `prepare-manual` line-length audit flags any source line wider than K. Over-long lines are an authorship defect, fixed in source.

---

## 7. The pipeline from P1 (where notes come from)

`engineering/ingestion/P1-DOCUMENT-LINEAGE.md` records, for each ingested P1 app note, its **P2 recreation candidacy** — how well its *value* carries to a P2 rewrite (verbatim porting is never the goal; P1 hardware idioms don't transcribe). The STRONG candidates are the natural early P2 notes:

| P1 note | P2 recreation | Candidacy |
|---|---|---|
| AN001 Counters | **Smart Pin modes** (NCO/PWM/DUTY→DAC, edge counting, Σ∆→ADC) | STRONG — the canonical "P2 Smart Pin Modes" note |
| AN008 Sigma-Delta ADC | **Smart-pin ADC** (on-chip feedback/decimation) | STRONG |
| AN014 Coroutines | **PASM2 `CALLD`** (flag save/restore collapses) | STRONG — strong voice exemplar |
| AN004 GUI/VGA | Streamer + smart-pin video | HIGH (framework) / MED-LOW (drivers rebuild) |
| AN013 WMF Menus | data-driven menu architecture on P2 | MED-HIGH / LOW-MED |

A recreation re-derives every number against P2 silicon and notes where a P1 idiom has *no* P2 home (e.g. AN001's LOGIC-equation and per-pin-PLL counter modes). New notes need not be recreations — any P2-specific application is fair game.

---

## 8. Quality checklist

**Identity**
- [ ] One application/outcome (or one capability-domain), in view from Abstract to Conclusion
- [ ] Archetype is clear (§1.1): single-build *or* techniques-catalog — not a subsystem tour
- [ ] If a catalog: one shared conceptual base + every technique a runnable, verified recipe + a decision aid
- [ ] Removing the worked example(s) would break the note (it's not a manual chapter in disguise)
- [ ] Mechanism the manual under-documents was added to the manual and cited, not grown into the note

**Structure**
- [ ] Flow is orient → concept → mechanism → build → verify → adapt → consolidate
- [ ] "The Idea" precedes any register/bit-field detail
- [ ] A 🔍 Verify step with expected output + a failure branch
- [ ] Resources + cross-references point onward to manuals/notes

**Sourcing**
- [ ] Every code block compiles under `pnut_ts` (`-d` if it has `debug()`)
- [ ] Idioms validated against the P2KB YAML before the compiler
- [ ] No unsourced capability claim; worked numbers derived from an authority
- [ ] Verification output came from a real run

**House**
- [ ] Voice per `APP-NOTE-VOICE-GUIDE.md` (register blend, markers, terminology)
- [ ] Symbolic constants taught, not raw numbers; "cog" lowercase; official titles
- [ ] Code line width ≤ K; no wrapped code

---

*Version 1.1 — adds the techniques-catalog archetype + its two guardrails and the decomposition rule (§1.1), surfaced by the P2AN000 instrumentation-ADC note. v1.0: initial app-note creation guide. Genre model: Parallax P1 application notes (AN001/004/008/013/014, ingested 2026-06-27). Pedagogical layer per §3. Companion: `APP-NOTE-VOICE-GUIDE.md`.*
