# The P2 Architect's Guide — Voice Guide

**Document:** The P2 Architect's Guide — Thinking in Cogs, Pins, and Forces
**Purpose:** Define the writing voice — a warm, welcoming orientation that rises to careful design rigor without ever turning glib or prescriptive
**Created:** 2026-06-22
**Companion:** `creation-guide.md` (what the manual is); `PLANNING.md` (why)

---

## 1. Voice Philosophy

### 1.1 The guiding principle
> **This guide makes a newcomer feel at home with the Propeller 2, then — only once they're comfortable —
> teaches them to think like an architect. It is warm the whole way up, and it never hands down answers.**

Unlike the streamer/PASM2/Spin2 references (reference-primary with a teaching layer), this guide is the
inverse: **orientation-primary**, with a rigor layer at the top. It does not switch between a "teaching voice"
and a "reference voice." It speaks in **one voice that *modulates by altitude*** — the same warm mentor, going
gradually more rigorous as the reader climbs.

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

### 1.3 The core move — voice modulates by altitude
The same voice, dialed differently per chapter:

| Chapter | Warmth | Rigor | Notes |
|---------|--------|-------|-------|
| **Ch1 Meet the P2** | maximal | low | reassuring, feature-first, lots of intuition. Make the chip feel approachable. |
| **Ch2 Putting It to Work** | maximal | low–moderate | encouraging, "here's how you actually do it." Comfort through doing. |
| **Ch3 Thinking in P2** | **stays warm** | **high, never glib** | careful and precise; rigor carried by the worked example, not by lecturing; **never prescriptive**. The felt shift is "you're ready for this now." |

The early chapters **earn the trust** that lets the reader follow into Ch3. Never condescend early; never turn
cold or glib late.

### 1.4 Target audience
Four readers (see `creation-guide.md` §1.2): newcomer, migrating P1 vet, working dev, AI agent. The single
modulating voice serves all four — the newcomer rides the warmth up; the working dev drops straight into the
rigorous summit and finds it still readable.

---

## 2. Voice Characteristics

### 2.1 What we DO
| Pattern | Example |
|---------|---------|
| Build intuition before mechanism | "Think of each cog as its own little computer that never stops to wait for the others — *that* independence is the whole point." |
| Address the reader warmly | "If you've used a microcontroller before, the first surprise is that there are eight of them." |
| Motivate before detail | "You reach for a smart pin when you want a pin to *do* something — count, measure, output a waveform — without spending a cog on it." |
| Differentiate by contrast | "A cog gives you a whole processor; a smart pin gives you one dedicated job at the edge. Reach for the smaller tool first." |
| In Ch3: teach a technique | "Ask first: what is the *one* serialized resource here, and which single cog will own it? That answer makes your first cut." |

### 2.2 What we DON'T
| Avoid | Why | Instead |
|-------|-----|---------|
| Heavy persona / jokes / "Uff!" | That's DeSilva; we're low-persona | warmth through clarity |
| Dictionary dryness | loses the newcomer | motivate, then state |
| "Simply…", "just…", "obviously…" | dismissive of real difficulty (esp. Ch3) | state the step plainly |
| Exhaustive enumeration | that's the reference manuals' job | orient + link out |
| **"The right design is…", "you should structure it as…"** (Ch3) | **prescribes a unique-per-project outcome** | **"here's how to *derive* it; your answer will differ"** |
| Hedging ("maybe", "probably") on facts | undermines authority | state sourced facts directly |
| Marketing / undocumented roadmap | trust chain | present-tense, sourced facts |

### 2.3 The anti-glibness rule (Ch3)
Functional decomposition is not lightweight, so we never make it *sound* lightweight. No "it's easy," no
"just split it up," no false reassurance. We respect the difficulty by being precise and by walking the reader
through real reasoning. Difficulty is honored, not hidden — and never inflated to sound impressive either.

### 2.4 The anti-prescription rule (Ch3) — load-bearing
The final decomposition is unique to every project (PLANNING §5, creation-guide §3.4). Ch3 prose teaches
*techniques for deriving*; it must never read as a recipe. The robot-dog derivation is always framed as **one
machine's answer, shown to make the method visible** — never "do it this way." If a sentence could be quoted as
a design rule out of context, rewrite it as a question the reader asks of *their* machine.

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
| **COG** | CPU, core | the community treats the COG as the computer |
| smart pin | smartpin, intelligent pin | canonical two words |
| hub | main memory (alone) | "hub" / "hub RAM" |
| Spin2 / PASM2 | Spin / PASM (when meaning P2) | reserve unqualified for P1 context |
- **Code:** show the compiler's symbolic **constants**, not arithmetic values (validate the symbol↔value off to
  the side; don't replace the symbol with a number). Instruction names and bit-field notation per platform
  standards. Fenced code (```spin2 / ```pasm2), `pnut_ts`-verified (`-d` for DEBUG).
- Inherit `repo-voice-profile.md` + the shared platform voice; this guide layers the orientation register on top.

---

## 5. Section-Specific Voice

### 5.1 Chapter openers (Chs 1–2)
Warm advance organizer: what this chapter gives you and why it matters, in two or three sentences, before any
detail. Example: ✅ *"By the end of this chapter you'll be able to picture the whole chip — eight processors,
one shared hub, and a ring of clever pins — and know roughly what each part is for. That picture is all you need
before we start writing code."*

### 5.2 Feature introductions (Ch1)
One or two plain sentences on what it is, then what it's *for*, then a link out. ✅ *"The CORDIC solver is a
piece of math hardware shared by all eight cogs. You hand it an angle or a vector and it hands back sines,
magnitudes, logarithms — the trigonometry you'd otherwise write by hand. (The full operation list is in the
Silicon Doc; here, just know it's there and it's fast.)"*

### 5.3 The decomposition chapter (Ch3)
Rigorous, warm, derivational. Lead each force with the question it answers, give the failure mode if ignored,
then show it deriving — not dictating. ✅ *"Force 1 asks a correctness question, not a style one: which single
cog owns this serialized resource? Get it wrong and two cogs drive the same wire — there is no hardware referee.
So the first cut traces the wire."* ❌ *"Put your I²C driver in its own cog."* (prescribes an outcome)

### 5.4 The worked derivation (robot dog)
Frame it before and after as a demonstration. Open: *"Let's watch the method run on one machine — a walking
robot dog. Yours will be different; the point is the moves, not the answer."* Close: *"Notice we never started
from a parts list — we started from the wires and the timing, and the object set fell out. Run the same routine
on your machine and you'll get a different, equally sound shape."*

---

## 6. Quality Checklist
**Warmth & altitude**
- [ ] Chs 1–2 read as welcoming; no abstraction that doesn't yet help the newcomer
- [ ] Ch3 stays warm but rigorous; no "simply/just/easy"; difficulty honored
- [ ] The felt tone shift into Ch3 is "you're ready," not "brace yourself"

**Anti-prescription (Ch3)**
- [ ] No sentence reads as a design rule out of context
- [ ] The robot dog is framed as a demonstration, not a template, both before and after
- [ ] Every force/section teaches a *technique for deriving*, not an outcome

**Discipline**
- [ ] Link out, never duplicate the reference manuals
- [ ] Low persona — warmth from clarity, not a character
- [ ] "COG" not "CPU"; code constants not arithmetic; `pnut_ts`-verified code
- [ ] No hedging on facts; no marketing; no undocumented roadmap claims

---

## 7. Summary — the voice equation
```
Our Voice = a senior dev's whiteboard warmth
          + reference-grade precision (dialed up by altitude)
          − DeSilva's persona
          − the dictionary's coldness
          − any prescribed answer
```
A warm, welcoming orientation that respects the reader enough to take them somewhere real — and trusts them to
derive their own design rather than handing them one.

---
*Version 0.1 — initial voice guide, derived from PLANNING.md §10 (2026-06-22).*
