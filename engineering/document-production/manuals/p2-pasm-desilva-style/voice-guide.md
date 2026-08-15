# P2 PASM deSilva-Style Manual — Voice Guide

**Document:** *Discovering P2 Assembly* — the deSilva-style PASM2 tutorial
**Purpose:** State this manual's position on the four house voice rules — and only that.
**Created:** 2026-08-15 (Sprint 1, guide-layer normalization)
**Companions:** `why-desilva-voice-works.md` (why the voice is what it is — the rationale
and its research basis) · `desilva-style-guide.md` (how it looks on the page — the source
of truth for formatting) · `creation-guide.md` (what the manual is and how it is built)

> **This file is deliberately thin.** The four rules are stated once, in
> `engineering/standards/documentation-standards/documentation-voices-catalog.md`
> ("The Shared Discipline — the four house rules"). This guide states what *this*
> manual does about them, with a reason for each. It does not restate the rules,
> and it does not duplicate the rationale or the formatting rules that already have
> homes above.

---

## 1. Reader and register

The reader is **learning assembly language**, often their first. They arrive able to
program, not able to think in registers and cycles. The manual's job is to get them
writing working PASM2 and *enjoying it* — not to be the reference they consult
afterwards (that is the *P2 Assembly Language Reference Manual*).

The register is **high warmth, high persona, spacious**: a strong narrator who tells
jokes, admits confusion, celebrates the reader's wins, and takes digressions. That is
a deliberate charter, defended on pedagogical grounds in `why-desilva-voice-works.md`,
not an accident to be tidied up.

**Two standing cautions before anyone edits this manual:**

1. `why-desilva-voice-works.md` carries an explicit **"DON'T Add These Modern
   'Improvements'"** list — learning-objective boxes, formal assessment questions,
   rigid structural requirements, academic citations in the main text. Check any
   proposed change against that list first. It exists because this manual has been
   "improved" before.
2. **Warmth is the charter; condescension is not.** Every rule below that constrains
   the voice constrains it in that one direction.

---

## 2. The four house rules — this manual's declaration

| rule | decision | reason |
|------|----------|--------|
| **R1** Calibrated confidence | **ADOPT**, scoped to technical claims about the P2 | Accuracy is register-independent, and a tutorial's worked examples are exactly where an overstated claim reaches a beginner who cannot yet check it. This voice is already close to native here — *"Acknowledge complexity: 'This is tricky, and that's okay'"* **is** calibration, and the persona is explicitly sometimes-wrong-but-honest. **Scope:** technical P2 claims only. The voice's playful self-assessment ("I may have got carried away there") is a different act and is not an evidence claim. |
| **R2** The payoff-sentence test | **ADOPT** | Same reason as R1, applied to the place claims are most likely to be invented: a closing sentence that needs a punchy ending. Chapter-end celebration is *not* what this rule targets — see the R3 self-admiration row. |
| **R3** Anti-pattern family | **per row — see §2.1** | The rows differ sharply for this voice; taking the family as a block would get two of the four backwards. |
| **R4** Cadence budget | **REJECT** | Two reasons, both from the sources rather than from taste. **(1) R4's own carve-out applies:** a declared refrain is structure, not a beat. This manual's Chapter End boxes and celebration moments are exactly that — announced, structural, and enumerated in `desilva-style-guide.md`'s box-type list. **(2)** `why-desilva-voice-works.md` defends emotional punctuation as pedagogy (Emotional Design; achievement milestones), so a budget that thins it would trade a documented learning benefit for a cadence metric. |

### 2.1 R3, row by row

| anti-pattern | decision | reason |
|---|---|---|
| **Tutorial filler** | **REJECT** | The house rule's own origin document treats this voice as a different register: the XBYTE guide's voice-comparison table lists deSilva as *"Tutorial filler: Occasional"*. Here it **is** the register — the conversational asides are the teaching, not padding around it. |
| **Reader-as-foil** | **ADOPT** | This *reinforces a rule the manual already has*: `desilva-style-guide.md` says **"No condescension: Respect reader intelligence."** Reader-as-foil is condescension with a friendly face — the besserwisser tells the reader what they think, then corrects them. ⚠ **Carve-out:** the manual's gentle prerequisite checks that offer an escape route ("If cogs are still fuzzy, Chapter 2 has you covered") are **not** caught by this. They offer an exit; they do not impute a belief in order to correct it. |
| **Self-admiration** | **ADOPT — adapted** | The defect is *the text admiring itself or its subject*. This manual celebrates **the reader's achievement** ("Uff!" as shared relief, the chapter-end congratulations), which is a different act and is protected pedagogy. Adopt against self-praise; leave celebration of reader progress entirely alone. |
| **Staged reveal** | **ADOPT the defect — REJECT the phrase list** | **Never withhold a fact *across* a paragraph or section boundary so its arrival lands a beat.** Announced signposts ("Here's the catch:") followed immediately by the fact are **structure**, and the style guide's *"Show before explaining"* sequencing is **pedagogy** — neither is staged reveal. **The test is distance:** if the fact arrives in the same breath as the signpost, it is a signpost. This wording is decided on measurement, not reputation — every reveal-vocabulary hit in the 6,176-line master was read in context and **the actual defect occurs zero times**, while the vocabulary appears three. Banning the phrases would have removed working signposts and still missed the defect. |

**Why the rows are declared even where they reject.** An undocumented rejection reads
as an oversight and gets "fixed" by the next sweep. Each reason above is the record
that this was decided, not missed.

---

## 3. What is NOT in this file

| you want | it lives in |
|---|---|
| the four rules themselves | `engineering/standards/documentation-standards/documentation-voices-catalog.md` |
| *why* the voice is warm, quirky, and celebratory — with the learning-theory basis, and the **"DON'T Add These Modern 'Improvements'"** guard | `why-desilva-voice-works.md` |
| box types, colours, code-block styling, mnemonic casing — every presentation decision | `desilva-style-guide.md` |
| chapter plan, sources, verification protocol, production workflow | `creation-guide.md` |

Reference these; do not copy them here. A rule with two homes drifts, and the copy is
what an author reads.
