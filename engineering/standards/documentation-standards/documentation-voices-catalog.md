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
**Failure mode** (the well-documented one): drifts into a **recognizably-AI register** — over-confident, self-admiring ("elegant", "free money", "the single most…"), reader-as-foil ("the obvious way is wrong", "it is tempting to…"), manufactured reveals ("here is the trap"), and a **metronomic closing beat** on nearly every section. "Instantly recognizable and rapidly fatiguing." Worst, a closing flourish *manufactures a payoff*, smuggling in an overstated or unsourced claim. This voice needs the shared discipline below more than any other. Detected by [[document-audit]] Dimensions #4c (payoff-sentence sweep) and #3c; the calibrated-confidence and cadence-budget rules are the write-time guard.

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
**Failure mode**: Self-indulgent storytelling that buries the technical point; manufactured drama and withheld reveals for their own sake. Shares the Claude-voice cadence risk — subject to the same shared discipline below.

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

## The Shared Discipline — applies to every voice, narrative voices most

A voice sets *tone*; it never licenses a lower bar on truth or a fatiguing
rhythm. Three rules cut across all seven voices (origin: the XBYTE guide
review, 2026-07, where an expert reader flagged an "instantly recognizable,
over-confident, rapidly fatiguing" register):

1. **Calibrated confidence, not false confidence.** Never state a claim above
   its evidence. A qualifier that reflects the true state of the evidence
   ("usually", "on most guests") is accuracy, not hedging — required wherever
   the bare claim would overstate. Banned separately: *tutorial filler* ("you
   might wonder", "let's explore"). The two are different; do not conflate them.
2. **The payoff sentence carries risk.** A closing crescendo demands a punchy
   payoff, and when no true one exists an invented claim fills the slot. At
   write time, strip the flourish off any section- or callout-closing sentence
   and read what remains as a bare claim — satisfy it or cut it. Two source-free
   tests: does the document already say the opposite elsewhere? does the sentence
   lean on `never / always / every / only / nothing / impossible / free / the
   single most`?
3. **Cadence is budgeted.** One good beat is fine; the failure is *regularity*.
   At most ~half of section closings may land a rhetorical beat, and never more
   than ~4 in a row; chapter closers stay well below. A declared refrain is
   structure, not a beat, and an earned beat (one that carries real information
   or *lowers* the text's confidence) is protected — do not flatten a document
   to hit a number.

Detection is [[document-audit]] Dimensions **#4c** (payoff-sentence sweep,
including a longest-consecutive-beat-run measure) and **#3c** (example
placement). The write-time counterparts live in each manual's voice-guide
(template: the XBYTE guide's §2.2a calibrated-confidence rule and §2.4 cadence
budget) and the [[document-finalize]] overlay. Reference-voice documents
(entry-per-instruction tables) rarely exhibit the defect; narrative,
argument-driven documents are where it concentrates.

## Implementation Notes
- Each document should declare its voice in the header
- Maintain voice consistency throughout a document
- Voice mixing is allowed between sections with clear transitions
- Community feedback will refine voice definitions over time
- **A voice's declared failure mode is a review checklist item** — audit a
  document against the failure mode of the voice it declares, not a generic one.