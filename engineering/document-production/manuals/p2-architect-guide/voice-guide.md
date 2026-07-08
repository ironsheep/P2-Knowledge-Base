# The P2 Architect's Guide — Voice Guide

**Document:** The P2 Architect's Guide — Thinking in Cogs, Pins, and Forces
**Purpose:** Define the writing voice — a warm mentor's guided tour, from the design desk of a real project, through the rigor of the decomposition method, to the amplification of working with an agent — never glib, never prescriptive
**Created:** 2026-06-22 · **Re-scoped:** 2026-07-08 (v1.0.0 three-act realization)
**Companion:** `creation-guide.md` (what the manual is); `PLANNING.md` (why)

---

## 1. Voice Philosophy

### 1.1 The guiding principle
> **This guide sits beside a developer who already knows the Propeller 2 and helps them *design* with it —
> getting a real project off the ground, deriving its architecture onto the chip, then doing the same work
> with an agent. It is warm the whole way through, it treats the method with the seriousness it deserves,
> and it never hands down answers.**

The reader arrives having done *Getting Started with the Propeller 2* (the prerequisite) — so we do **not**
build orientation comfort here; that register left with the split. This is unapologetically the architect's /
designer's book. It speaks in **one voice** across all three acts — the same warm mentor — that adjusts its
*register* to the work at hand, not its warmth.

### 1.2 Where we post — the spectrum
Two existing documents bracket us, each "going too far" for our purpose:

| | Warmth | Persona | Density | Reads like |
|--|--------|---------|---------|-----------|
| **DeSilva** | high | **high** (a strong narrator: "Uff!", jokes, digressions) | spacious | a campfire story |
| **Spin2 v55 / PASM2 reference** | low | none | maximal | a dictionary |
| **This guide** | **high** | **low** | content-driven | **a mentor's guided tour** |

We sit between them: **high warmth · low persona · content-driven density.** The warmth comes from *clarity and
care* — a senior developer explaining design at a whiteboard — **not** from adopting a character. We are warmer
than the references and more disciplined than DeSilva.

### 1.3 The core move — one warm voice, three registers by act
Warmth is constant; the *register* shifts with the act:

| Part / Act | Warmth | Register | Notes |
|------------|--------|----------|-------|
| **Part I — Getting a Project Off the Ground** | high | concrete, practical, been-there | the voice of an engineer telling you how projects *actually* go — datasheets that fight you, pins that don't fit. Grounded and candid. |
| **Part II — Thinking in P2 (decomposition)** | **stays warm** | **rigor without glibness** | careful and precise; a serious method treated seriously; rigor carried by two worked derivations, not by lecturing; **never prescriptive.** The felt shift is "you're ready for this now." |
| **Part III — The Same Work, with an Agent** | high | amplification / practitioner | energized and honest about what changes and what doesn't; the exoskeleton voice — "here is how your reach extends," never hype. |

Never condescend, never turn cold or glib. The warmth is the through-line; the register is the tool.

### 1.4 Target audience
Two readers (see `creation-guide.md` §1.2): the working developer designing a real system, and the reader
asking how an agent changes the work; the migrating P1 veteran navigates by the "P1 note" sidebars. All have
the *Getting Started* orientation already — write **to a peer who knows the chip**, never down to a newcomer.

---

## 2. Voice Characteristics

### 2.1 What we DO
| Pattern | Example |
|---------|---------|
| Ground design in lived project reality (Act I) | "Datasheets come first, and they fight you. Some arrive in a language you don't read; some don't exist at all." |
| Lead with the question a force asks (Act II) | "The question is: for each serialized, stateful hardware resource — an I²C bus, a one-wire LED chain — *which single cog owns it?*" |
| Motivate before mechanism | "Because whenever data crosses a cadence boundary, *something must adapt the rate* — and that adapter is a distinct responsibility, so it's a distinct object." |
| Differentiate by contrast | "A cog is the strongest encapsulation boundary the silicon offers; a smart pin can *delete an entire software module* by absorbing its function into hardware." |
| Name what changes with an agent, honestly (Act III) | "The agent removes none of the judgment. You still own the pin map and hold the probe. What it changes is the *cost* and the *reach* of each step." |

### 2.2 What we DON'T
| Avoid | Why | Instead |
|-------|-----|---------|
| Heavy persona / jokes / "Uff!" | that's DeSilva; we're low-persona | warmth through clarity |
| Re-teaching orientation (what a cog/hub/smart pin *is*, how to read P2 code) | that's *Getting Started*, the prerequisite | assume it; reference it; link out |
| Dictionary dryness | loses the reader | motivate, then state |
| "Simply…", "just…", "obviously…" | dismissive of real difficulty (esp. Act II) | state the step plainly |
| Exhaustive enumeration | that's the reference manuals' job | orient + link out |
| **"The right design is…", "you should structure it as…"** (Act II) | **prescribes a unique-per-project outcome** | **"here's how to *derive* it; your answer will differ"** |
| Agent hype / "just prompt it and it's done" (Act III) | overclaims; erases the judgment that stays yours | amplification framed honestly, with the human's role named |
| Hedging ("maybe", "probably") on facts | undermines authority | state sourced facts directly |
| Marketing / undocumented roadmap | trust chain | present-tense, sourced facts |

### 2.3 The anti-glibness rule (Act II)
Functional decomposition is not lightweight, so we never make it *sound* lightweight. No "it's easy," no "just
split it up," no false reassurance. We respect the difficulty by being precise and by walking the reader
through real reasoning — two worked derivations, start to finish. Difficulty is honored, not hidden — and never
inflated to sound impressive either.

### 2.4 The anti-prescription rule (Act II) — load-bearing
The final decomposition is unique to every project (PLANNING §5, creation-guide §3.4). Part II prose teaches
*techniques for deriving*; it must never read as a recipe. Each worked derivation — the walking robot and the
streaming pipeline — is always framed as **one application's answer, shown to make the method visible** — never
"do it this way." If a sentence could be quoted as a design rule out of context, rewrite it as a question the
reader asks of *their* application. The two derivations exist precisely to prove the method generalizes: they
reach *different* answers on different hardware, and **none of their boundaries carry over — only the
procedure does.**

### 2.5 The amplification rule (Act III) — amplify, don't abandon
Part III is an *additive* lens, never a replacement. Two things stay true in every sentence: the agent
**amplifies** (the exoskeleton), and the agent **removes none of the judgment**. Name what stays the human's —
deciding what to build, the pin map, the probe, judging the cut against the hardest deadline — every time you
name what the agent takes on. The voice is energized but honest: no "the agent designs it for you." And keep
the book's own discipline visible — *confirm the agent's understanding before you let it proceed.*

---

## 3. Enhancement Markers & Sidebars

### 3.1 "P1 note" sidebars (woven, optional — Parts I–II)
Short bronze callouts (fenced `::: p1note`) for migrating P1 veterans — a newcomer can skip them entirely.
| Sidebar label | When |
|---------------|------|
| **same as P1** | the concept carries over (one owner per serialized resource; spatial thinking) |
| **changed in P2** | it exists but works differently (16× larger hub; egg-beater) |
| **new in P2** | no P1 analog (smart pins absorbing a protocol, CORDIC, streamer, events) |

### 3.2 Inline markers (use sparingly)
| Marker | When |
|--------|------|
| **💡 Tip:** | a non-obvious design insight |
| **⚠️ Watch out:** | a genuine pitfall with non-obvious consequences (e.g. the flat device list; snapping servos) |
Keep markers rare — this is a narrative guide, not a reference peppered with boxes.

---

## 4. Terminology Standards
| Canonical | Not | Note |
|-----------|-----|------|
| **cog** | CPU, core | the community treats the cog as *the computer*; lowercase in prose (capitalize only in a heading/title or at sentence start) — never "COG" |
| **embedded application** | machine | the thing being built; shorten to "application" only where the embedded context is already clear. Reserve "machine" for literal hardware. |
| **change-coupling** | connascence (except once) | the 2nd judging tool; "connascence" appears **once** as the formal anchor ("the design literature calls this connascence"), in the Appendix B (Page-Jones) cite, and in the glossary title — nowhere else in everyday prose |
| smart pin | smartpin, intelligent pin | canonical two words |
| hub | main memory (alone) | "hub" / "hub RAM" |
| Spin2 / PASM2 | Spin / PASM (when meaning P2) | reserve unqualified for P1 context |
- **No embedded code:** the book carries zero code examples by design (the mechanics belong to *Getting
  Started* and the reference manuals). Where code would once have appeared, describe the *technique* and link
  out. If a future snippet is ever added, it uses named **constants** not arithmetic, fenced (```spin2 /
  ```pasm2), `pnut_ts`-verified (`-d` for DEBUG), within the platform K=76 budget.
- Inherit `repo-voice-profile.md` + the shared platform voice; this guide layers the design/architect register
  on top.

---

## 5. Section-Specific Voice

### 5.1 Part I openers (the project front)
Ground the reader in a real, shippable project immediately, candid about how the work actually goes.
✅ *"Picture a real project — not a toy. Something you're going to build and then put in front of people… it
has to actually work, for someone who isn't you."* Lead with the lived shape of the front end, not a checklist.

### 5.2 Part II — the decomposition method (Act II)
Rigorous, warm, derivational. Open the part by stating the method-not-outcome thesis. Lead each force with the
*question it asks*, give the failure mode if ignored, then show it *deriving* — not dictating.
✅ *"Force 1 asks a correctness question, not a style one: which single cog owns this serialized resource? Get
it wrong and two cogs drive the same wire — there is no hardware referee. So the first cut traces the wire."*
❌ *"Put your I²C driver in its own cog."* (prescribes an outcome)

### 5.3 The worked derivations (walking robot · streaming pipeline)
Frame each, before and after, as a demonstration. Open: *"This is one application's answer, shown to make the
method visible — it is not a template. Read for the *moves*, never for the result."* Close by naming what did
and didn't carry over: *"None of these boundaries did — not the cog map, not the fan-out. The *procedure* did.
Carry the method, never the map."* The second derivation exists to reach a visibly *different* answer (a
data-plane pipeline vs. the robot's control plane) on purpose.

### 5.4 Part III — the agent voice (Act III)
Energized and honest. Every gain the agent brings is paired with what stays the human's. The exoskeleton is the
spine image: amplification, not replacement.
✅ *"The right image is not a faster typist; it is an exoskeleton — it amplifies, letting you do things you
could not have done on your own… you amplify what you already know, you don't abandon it."*
❌ *"Just hand it the datasheet and the agent builds the driver."* (erases judgment, overclaims)

### 5.5 In Closing (the send-off)
Warm, reflective, earned. Look back over the distance covered across the three acts; land on *method over
answers* (catalogue vs. craft) and the closing symmetry — the KB the agent draws on is the same body this
guide was written from. A generous, forward-looking close: *"So go build something."*

### 5.6 The appendices (reference register)
The back-matter appendices drop to a **precise reference register** — lower warmth, factual, scannable (the
"dictionary" voice is appropriate here). **Appendix A** (space/time + FPGA terminology) states the spectrum and
the terminology tables flatly, and **always carries the what-transfers/what-doesn't honesty** — never let the
borrowed words imply the P2 *is* an FPGA. **Appendix B** (further reading) is a terse annotated list; every
citation is real and verified (NEEDS-VERIFICATION until checked), each with a one-line "why it matters here."

---

## 6. Quality Checklist

**Warmth & register**
- [ ] Warm throughout; Part I concrete and candid, Part II rigorous, Part III amplifying
- [ ] Part II stays warm but rigorous; no "simply/just/easy"; difficulty honored
- [ ] The felt tone into Part II is "you're ready," not "brace yourself"
- [ ] No passage re-teaches orientation (that's *Getting Started*, the prerequisite)

**Anti-prescription (Act II)**
- [ ] No sentence reads as a design rule out of context
- [ ] Each worked derivation is framed as a demonstration, not a template, both before and after
- [ ] Every force/section teaches a *technique for deriving*, not an outcome
- [ ] The two derivations reach visibly different answers; only the procedure carries over

**Amplification (Act III)**
- [ ] Every agent gain is paired with what stays the human's judgment
- [ ] Exoskeleton framing, not hype; no "the agent designs it for you"
- [ ] The understanding gate (confirm before proceeding) is honored

**Discipline**
- [ ] Link out, never duplicate the reference manuals or *Getting Started*
- [ ] Low persona — warmth from clarity, not a character
- [ ] "cog" (lowercase) not "CPU"; "embedded application" not "machine"; "change-coupling" not "connascence" (save one formal anchor)
- [ ] No hedging on facts; no marketing; no undocumented roadmap claims

---

## 7. Summary — the voice equation
```
Our Voice = a senior dev's whiteboard warmth
          + design-desk candor (Act I)
          + reference-grade rigor, never glib (Act II)
          + honest amplification, judgment kept human (Act III)
          − DeSilva's persona
          − the dictionary's coldness
          − re-taught orientation (it's the prerequisite)
          − any prescribed answer
```
A warm, peer-to-peer guide that takes a developer who knows the chip somewhere real — deriving their own design
rather than being handed one, and reaching farther with an agent without giving up the judgment that was always
theirs.

---
*Version 1.1 — re-scoped 2026-07-08 to the shipped v1.0.0 three-act voice (warm throughout; Act I candor → Act
II rigor → Act III amplification). Supersedes the v0.1 orientation-comfort altitude gradient that left with
Getting Started. Derived from PLANNING.md §10/§16 and the shipped opus-master.*
