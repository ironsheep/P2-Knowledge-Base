# Documentation Voices Catalog

## Identified Documentation Voices

### 1. Chip Voice (Silicon Truth)
**Characteristics**: Terse, essential, technically perfect
**Best For**: Experienced developers who want raw facts
**Example**: Instruction encoding tables, register definitions
**Strength**: Absolute technical accuracy
**When to Use**: Reference manuals, technical specifications
**Failure mode**: So terse it drops the *why* a non-expert needs; or **false precision** — a derived/measured value stated as if it were spec. Guard: state numbers only at their source's confidence.

### 2. deSilva Voice (Gentle Teacher)  
**Characteristics**: Progressive, patient, concept-building
**Best For**: Assembly language learners
**Example**: "Let's start with moving a value between registers..."
**Strength**: Makes complex concepts approachable
**When to Use**: Tutorial series, learning paths
**Failure mode**: Over-padding and excessive hand-holding; celebration fatigue ("Uff!" on every step). Warmth is the point — condescension is not. (Deliberate by charter for deSilva; do not "correct" its warmth toward reference voice.)

### 3. Parallax Educational Voice (Complete Learning System)
**Characteristics**: Self-contained projects with full context
**Best For**: Educators and students  
**Example**: "Build a line-following robot" with circuit diagram + code + explanation
**Strength**: Everything needed in one place
**When to Use**: Educational materials, workshop content
**Failure mode**: Bloat — "everything in one place" slides into everything-and-the-kitchen-sink, burying the lesson. Guard: one project, one learning goal per unit.

### 4. Stephen/IronSheep Voice (The Bridge)
**Characteristics**: Makes brilliance accessible, customer-facing
**Best For**: Developers needing production-ready solutions
**Example**: Flash File System with clean API and error handling
**Strength**: Practical, usable, well-documented interfaces
**When to Use**: Library documentation, API guides
**Failure mode**: Marketing-spin — over-claiming ("perfect", "complete", "seamless") and trading technical precision for approachability. Guard: no inflated artifact names or capability claims (see the no-inflated-names rule).

### 5. Claude Voice (AI-Pedagogical)
**Characteristics**: Adaptive depth, data-driven clarity
**Best For**: Varied audiences needing customized explanation
**Example**: Multiple explanation levels for same concept
**Strength**: Can adjust to reader's apparent understanding
**When to Use**: AI-assisted documentation, adaptive tutorials
**Failure mode** (the well-documented one): drifts into a **recognizably-AI register** — the whole of **R3**'s anti-pattern family at once (self-admiration, reader-as-foil, staged reveal, tutorial filler), plus a **metronomic closing beat** on nearly every section (**R4**). "Instantly recognizable and rapidly fatiguing." Worst, a closing flourish *manufactures a payoff*, smuggling in an overstated or unsourced claim (**R1**/**R2**). This voice needs the four house rules below more than any other. Detected by [[document-audit]] Dimensions #4c (payoff-sentence sweep) and #3c; R1 and R4 are the write-time guard.

### 6. Recipe/Cookbook Voice
**Characteristics**: Direct problem→solution format
**Best For**: Experienced developers seeking quick solutions
**Example**: "To read I2C sensor: [code snippet]"
**Strength**: Fast access to common patterns
**When to Use**: Quick reference guides, pattern libraries
**Failure mode**: Context-free cargo-cult — the snippet works but the reader learns no *why*, and edge cases/failure conditions go unstated. Guard: one line of *why* and the boundary conditions with each recipe.

### 7. Narrative/Story Voice
**Characteristics**: Problem-solving journey format
**Best For**: Conceptual understanding through experience
**Example**: "When we needed to synchronize 5 sensors..."
**Strength**: Memorable through storytelling
**When to Use**: Case studies, architectural decisions
**Failure mode**: Self-indulgent storytelling that buries the technical point; manufactured drama and withheld reveals for their own sake (**R3** staged reveal). Shares the Claude-voice cadence risk — subject to the same four house rules below.

## Voice Selection Guidelines

### Choose Based on:
1. **Audience Experience Level**
   - Beginner → deSilva or Narrative
   - Intermediate → Parallax Educational or Stephen/IronSheep
   - Expert → Chip or Recipe

2. **Learning Goal**
   - Conceptual Understanding → Narrative or deSilva
   - Practical Application → Stephen/IronSheep or Recipe
   - Complete Project → Parallax Educational
   - Technical Reference → Chip

3. **Time Constraints**
   - Quick lookup → Recipe or Chip
   - Deep learning → deSilva or Narrative
   - Project-based → Parallax Educational

## The Shared Discipline — the four house rules (R1–R4)

A voice sets *tone*; it never licenses a lower bar on truth or a fatiguing
rhythm. Four rules cut across all seven voices (origin: the XBYTE guide
review, 2026-07, where an expert reader flagged an "instantly recognizable,
over-confident, rapidly fatiguing" register).

**This file is where the four rules are STATED. They are stated nowhere else.**

### R1 — Calibrated confidence

**Never state a claim above its evidence.** A qualifier that reflects the true
state of the evidence ("usually", "on most guests") is **accuracy, not hedging**
— it is *required* wherever the bare claim would overstate. What is banned is
hedging that avoids commitment on a fact we actually know.

### R2 — The payoff-sentence test

A closing crescendo demands a punchy payoff, and when no true one exists an
invented claim fills the slot. At write time, **strip the flourish off any
section- or callout-closing sentence and read what remains as a bare claim** —
satisfy it or cut it. Two source-free tests: does the document already say the
opposite elsewhere? does the sentence lean on `never / always / every / only /
nothing / impossible / free / the single most`?

### R3 — The anti-pattern family

Four register defects, named as one family:

| anti-pattern | what it is |
|---|---|
| **Tutorial filler** | words that announce the writing instead of doing it — "you might wonder", "let's explore" |
| **Reader-as-foil** (besserwisser) | imputing a belief to the reader in order to correct it — "the obvious way is wrong", "it is tempting to…" |
| **Self-admiration** | the text praising its subject or its own explanation — "elegant", "free money", "the single most…" |
| **Staged reveal** | manufactured suspense — "and here is the trap", "hold that result" |

A voice guide may adopt, adapt, or reject **each row independently** — this is a
family, not a block.

### R4 — Cadence budget (the metronome)

One good beat is fine; the failure is *regularity*. At most ~half of section
closings may land a rhetorical beat, and never more than ~4 in a row; chapter
closers stay well below. **A declared refrain is structure, not a beat**, and an
**earned beat** (one that carries real information or *lowers* the text's
confidence) is protected — do not flatten a document to hit a number.

### R1 is not R3's first row — do not conflate them

**Calibrated confidence (R1) and tutorial filler (R3) are different defects.**
Conflating them is the root cause of every voice contradiction this standard
exists to prevent: a guide that bans "hedging" as a *word class* instructs an
author to strip exactly the qualifiers R1 requires, and the mechanical half of
the guide wins. A qualifier earning its place on partial evidence is R1
*compliance*. "You might wonder whether…" is R3 filler. Ban the second; require
the first.

### The fix pattern — always name the defect, never the word

Every contradiction found in the 2026-08 propagation study traced to one
mistake: **the rule was written by naming banned *words* instead of naming the
*defect*.** The fix, applied identically everywhere:

1. **Name the defect** ("vague hedging that avoids commitment"), never a word
   list. A blacklist of `may / might / probably / typically / usually` is always
   wrong — those words are R1 compliance as often as they are defects.
2. **Point at the local rule** — every site that touches a shared rule carries a
   cross-reference to that guide's own calibrated-confidence section.
3. **Checklists point, never re-encode.** A quality checklist is what an auditor
   runs mechanically; a checklist that restates a rule in its own words becomes a
   counter-order the moment the rule is refined.

### Three structural rules for the guide tree

1. **Never restate a shared rule — adapt it.** A guide states its *local*
   decision about a rule; the rule itself lives here.
2. **Record rejections with reasons.** An undocumented rejection reads as an
   oversight and gets "fixed" by the next sweep.
3. **Quality checklists point at rules rather than re-encoding them.**

### Where the rules land

**Three layers.** House canon (**this file**) → class
(`engineering/document-production/app-notes/APP-NOTE-VOICE-GUIDE.md`, which
governs every P2ANxxx app note) → document (each manual's or app note's own
`voice-guide.md`). **Every voice guide declares ADOPT / ADAPT / REJECT against
R1–R4, with a reason.** Adjacent files (`creation-guide.md`, `style-guide.md`)
**may reference voice rules, never restate them.**

Detection is [[document-audit]] Dimensions **#4c** (payoff-sentence sweep,
including a longest-consecutive-beat-run measure) and **#3c** (example
placement). The write-time counterparts live in each voice guide (template: the
XBYTE guide's §2.2a calibrated-confidence rule and §2.4 cadence budget) and the
[[document-finalize]] overlay. Reference-voice documents (entry-per-instruction
tables) rarely exhibit the defect; narrative, argument-driven documents are
where it concentrates.

## Implementation Notes
- Each document should declare its voice in the header
- Maintain voice consistency throughout a document
- Voice mixing is allowed between sections with clear transitions
- Community feedback will refine voice definitions over time
- **A voice's declared failure mode is a review checklist item** — audit a
  document against the failure mode of the voice it declares, not a generic one.