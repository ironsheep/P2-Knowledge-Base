# Getting Started with the Propeller 2 — Voice Guide

> **Split note (2026-06-24):** This guide was split from the original *P2 Architect's Guide*
> first draft (4 chapters). This book is now the **Getting Started** orientation on-ramp — warm
> and welcoming from start to finish. The rising-rigor / anti-prescription voice and the
> functional-decomposition chapter moved with the design book, *The P2 Architect's Guide*
> (folder `p2-architect-guide`).

**Document:** Getting Started with the Propeller 2 — a warm orientation on-ramp
**Purpose:** Define the writing voice — a warm, welcoming orientation that stays in one register the whole way through
**Created:** 2026-06-22 (split into the Getting Started book 2026-06-24)
**Companion:** `creation-guide.md` (what the manual is); `PLANNING.md` (why)

---

## 1. Voice Philosophy

### 1.1 The guiding principle
> **This guide makes a newcomer feel at home with the Propeller 2 — what the chip is, how to read its code,
> and how to put its features to work. It is warm, encouraging, and clear from start to finish: one register,
> the whole way through.**

Unlike the streamer/PASM2/Spin2 references (reference-primary with a teaching layer), this guide is the
inverse: **orientation-primary**. It does not switch between a "teaching voice" and a "reference voice," and it
does not change altitude between chapters — it speaks in **one warm mentor's voice** from Chapter 1 through
"Where to Next."

### 1.2 Where we post — the spectrum
Two existing documents bracket us, each "going too far" for our purpose:

| | Warmth | Persona | Density | Reads like |
|--|--------|---------|---------|-----------|
| **DeSilva** | high | **high** (a strong narrator: "Uff!", jokes, digressions) | spacious | a campfire story |
| **Spin2 v55 / PASM2 reference** | low | none | maximal | a dictionary |
| **This guide** | **high** | **low** | content-driven | **a mentor's guided tour** |

We sit between them: **high warmth · low persona · content-driven density.** The warmth comes from *clarity and
care* — a senior developer explaining the chip at a whiteboard — **not** from adopting a character. We are
warmer than the references and more disciplined than DeSilva.

### 1.3 The core move — one warm register, start to finish
The same voice in every chapter — warm, encouraging, clear:

| Chapter | Tone | Notes |
|---------|------|-------|
| **Ch1 Meet the Propeller 2** | warm, reassuring | feature-first, lots of intuition. Make the chip feel approachable. |
| **Ch2 Reading P2 Code** | warm, encouraging | "here's how to read what you're looking at." Comfort through seeing it work. |
| **Ch3 Putting It to Work** | warm, encouraging | "here's how you actually use these features." Comfort through doing. |

Never condescend; never turn cold or glib. The reader should feel welcomed and capable from the first page to
the last.

### 1.4 Target audience
Four readers (see `creation-guide.md` §1.2): newcomer, migrating P1 vet, working dev, AI agent. The single warm
voice serves all four — the newcomer is welcomed in; the working dev still finds it clear and quick to scan.

---

## 2. Voice Characteristics

### 2.1 What we DO
| Pattern | Example |
|---------|---------|
| Build intuition before mechanism | "Think of each cog as its own little computer that never stops to wait for the others — *that* independence is the whole point." |
| Address the reader warmly | "If you've used a microcontroller before, the first surprise is that there are eight of them." |
| Motivate before detail | "You reach for a smart pin when you want a pin to *do* something — count, measure, output a waveform — without spending a cog on it." |
| Differentiate by contrast | "A cog gives you a whole processor; a smart pin gives you one dedicated job at the edge. Reach for the smaller tool first." |
| Walk the reader through reading code | "Read it top-down: this line names the pin, this one starts the smart pin, and this one waits for the result. Once you can spot that shape, every example looks familiar." |

### 2.2 What we DON'T
| Avoid | Why | Instead |
|-------|-----|---------|
| Heavy persona / jokes / "Uff!" | That's DeSilva; we're low-persona | warmth through clarity |
| Dictionary dryness | loses the newcomer | motivate, then state |
| "Simply…", "just…", "obviously…" | dismissive of real difficulty | state the step plainly |
| Exhaustive enumeration | that's the reference manuals' job | orient + link out |
| Hedging ("maybe", "probably") on facts | undermines authority | state sourced facts directly (but keep *calibrated* qualifiers where true — §2.4) |
| Marketing / undocumented roadmap | trust chain | present-tense, sourced facts |
| "the obvious way to think about eight cogs is wrong" · "you might assume the hub is just RAM" · "read that again" | **Reader-as-foil** — telling the reader what they think, then correcting them; even a warm mentor never does this | state it plainly and let the reader form the picture |
| "this is the most elegant part of the P2" · "the smart pins are pure genius" · "nothing else comes close" | **Self-admiration** — the text praising its subject or its own explanation (a cousin of marketing) | say what the feature *does*; let the reader be impressed on their own |
| "and here's the catch" · "but we'll get to the surprise" · "hold that thought" | **Staged reveal** — withholding a fact to manufacture a beat | deliver the fact where it belongs, unstaged |

### 2.3 The anti-glibness rule
The P2's features aren't trivial, so we never make them *sound* trivial. No "it's easy," no "just wire it up,"
no false reassurance. We respect real difficulty by being precise and by walking the reader through what's
actually happening. Difficulty is honored, not hidden — and never inflated to sound impressive either.

### 2.4 Calibrated confidence and cadence — the shared narrative discipline
This is a warm narrative guide, which is exactly the register that most easily drifts into a
*recognizably-AI* voice — over-confident, self-admiring, and closing nearly every section on a
rhetorical beat. Two guards, adopted platform-wide (origin: the XBYTE guide review, Chip Gracey
2026-07; the canonical statement is `documentation-voices-catalog.md` §"Shared Discipline"):

- **Calibrated confidence, not false confidence.** Banning hedging does *not* mean banning
  *uncertainty*. A qualifier that reflects the true state of the evidence — "usually", "on most
  boards", "in practice" — is **accuracy**, not hedging, and is required wherever the bare claim
  would overstate. Never state a claim above its evidence. The warm-voice trap: a closing
  crescendo *demands* a punchy payoff, and where no true one exists an invented claim fills the
  slot — so strip the flourish off any closing sentence and read what remains as a bare claim
  before keeping it.
- **Cadence is budgeted (R4) — ADOPTED as written.** A *beat* is a closing sentence that lands a
  rhetorical punch rather than finishing the thought. One good beat is fine; the failure is
  *regularity* — "instantly recognizable and rapidly fatiguing." The budget, the run limit, the
  chapter-closer emphasis, the flat-close-is-rest carve-out and the protection for earned beats all
  apply to this guide unchanged; the numbers are stated once in the house canon (voices catalog, R4)
  rather than copied here, where they would drift from the rule.

Detection: `document-audit` Dimension #4c (payoff-sentence sweep, with a longest-run measure).

---

## 3. Enhancement Markers & Sidebars

### 3.1 "P1 note:" sidebars (woven, optional)
Short callouts for migrating P1 veterans — a newcomer can skip them entirely.
| Sidebar | When |
|---------|------|
| **P1 note — same as P1:** | the concept carries over (8 cogs, hub round-robin, locks) |
| **P1 note — changed in P2:** | it exists but works differently (hub egg-beater, clock setup, 64 pins) |
| **P1 note — new in P2:** | no P1 analog (smart pins, CORDIC, streamer, events/interrupts, LUT, XBYTE) |

### 3.2 Inline markers (use sparingly)
| Marker | When |
|--------|------|
| **💡 Tip:** | a non-obvious orientation insight |
| **⚠️ Watch out:** | a genuine pitfall with non-obvious consequences |
Keep markers rare — this is a narrative guide, not a reference peppered with boxes.

---

## 4. Terminology Standards
| Canonical | Not | Note |
|-----------|-----|------|
| **cog** | CPU, core | the community treats the cog as the computer; **lowercase in prose**, capitalized only in headings/titles/numbered labels/sentence-start (never all-caps "COG") |
| smart pin | smartpin, intelligent pin | canonical two words |
| hub | main memory (alone) | "hub" / "hub RAM" |
| Spin2 / PASM2 | Spin / PASM (when meaning P2) | reserve unqualified for P1 context |
- **Code:** show the compiler's symbolic **constants**, not arithmetic values (validate the symbol↔value off to
  the side; don't replace the symbol with a number). Instruction names and bit-field notation per platform
  standards. Fenced code (```spin2 / ```pasm2), `pnut-ts`-verified (`-d` for DEBUG).
- Inherit `repo-voice-profile.md` + the shared platform voice; this guide layers the orientation register on top.

---

## 5. Section-Specific Voice

### 5.1 Chapter openers
Warm advance organizer: what this chapter gives you and why it matters, in two or three sentences, before any
detail. Example: ✅ *"By the end of this chapter you'll be able to picture the whole chip — eight processors,
one shared hub, and a ring of clever pins — and know roughly what each part is for. That picture is all you need
before we start writing code."*

### 5.2 Feature introductions (Ch1 "Meet the Propeller 2")
One or two plain sentences on what it is, then what it's *for*, then a link out. ✅ *"The CORDIC solver is a
piece of math hardware shared by all eight cogs. You hand it an angle or a vector and it hands back sines,
magnitudes, logarithms — the trigonometry you'd otherwise write by hand. (The full operation list is in the
P2 Documentation v35; here, just know it's there and it's fast.)"*

### 5.3 Reading code (Ch2 "Reading P2 Code")
Warm and walked-through. Show a short example, then read it line by line in plain language so the reader learns
to recognize the shape. ✅ *"Don't try to memorize this — just notice the rhythm: name the pin, configure the
smart pin, then read its result. Almost every example you'll meet follows that same three-beat pattern."*

### 5.4 Putting features to work (Ch3 "Putting It to Work")
Warm and encouraging — "here's how you actually use this." Motivate the feature, show it doing real work, and
point at the reference for the full detail. ✅ *"When you want a pin to count edges for you, you hand the job to
its smart pin and walk away — your cog is free for everything else. Here's the smallest version that works, and
then where to go when you need more."*

## 6. Quality Checklist
**Warmth & consistency**
- [ ] Every chapter reads as welcoming; no abstraction that doesn't yet help the newcomer
- [ ] No "simply/just/easy"; difficulty honored, never inflated
- [ ] The tone is the same warm register from the first page to the last — no cold or glib turns

**Discipline**
- [ ] Link out, never duplicate the reference manuals
- [ ] Low persona — warmth from clarity, not a character
- [ ] "cog" not "CPU"/"core" (lowercase in prose); code constants not arithmetic; `pnut-ts`-verified code
- [ ] No hedging on facts; no marketing; no undocumented roadmap claims

---

## 7. Summary — the voice equation
```
Our Voice = a senior dev's whiteboard warmth
          + clear, careful precision
          − DeSilva's persona
          − the dictionary's coldness
```
A warm, welcoming orientation — the same encouraging register from start to finish — that respects the reader
enough to make the Propeller 2 genuinely approachable.

---
*Version 0.1 — initial voice guide, derived from PLANNING.md §10 (2026-06-22); split into the Getting Started book 2026-06-24.*
