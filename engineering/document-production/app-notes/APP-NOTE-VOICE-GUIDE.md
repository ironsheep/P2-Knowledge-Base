# P2 Application Note — Voice Guide

**Applies to:** every document in `engineering/document-production/app-notes/` (the `P2ANxxx` series)
**Purpose:** define the writing voice for P2 application notes — a register distinct from both the reference manuals and the DeSilva-style tutorial
**Created:** 2026-06-27
**Companion:** `APP-NOTE-CREATION-GUIDE.md` (structure, pedagogy, sources). This guide governs *how it reads*; the creation guide governs *what goes where*.

---

## 1. Voice Philosophy — the third register

The P2 documentation set already speaks in two established registers:

- the **reference register** of the manuals (Streamer, Smart Pins, I/O) — third person, authoritative, dense, no hedging, optimized for the hundredth lookup; and
- the **tutorial register** of the DeSilva PASM guide — warm, second person, progressive, celebratory, optimized for the first read-through.

An application note is **neither**. It is the third register, and it has its own job:

> **An application note answers one question completely: "I want to *do* this specific thing — show me how, end to end, and teach me enough of the underlying mechanism that I can adapt it to my own design."**

So the app-note voice is **guided application**. It is:

- **Application-anchored, not feature-anchored.** A manual is organized around the silicon (here are all the modes); an app note is organized around an outcome (here is how you build *this*, and the modes appear because the build needs them).
- **Single-technique deep, not broad.** One note does one thing thoroughly. Breadth is the manual's job.
- **Warmer than the reference manual, tighter than the tutorial.** It uses "you" freely and explains *why* before *how* (manual reference voice forbids both), but it never meanders, never celebrates, and never pads — it is moving the reader toward a working result.
- **Empirically grounded.** Like the Parallax P1 app notes that anchor every claim with a scope capture, our P2 notes show the reader *what success looks like* — a DEBUG window, a logic capture, an expected value — and how to confirm it on their own bench.

This is the genuine Parallax application-note house voice (AN001 Counters, AN014 Coroutines, AN008 Sigma-Delta ADC) **plus** the pedagogical scaffolding those notes lacked. See `APP-NOTE-CREATION-GUIDE.md` §3 for the learning-science basis.

> **Not the campaign voice.** `engineering/document-production/repo-voice-profile.md` characterizes Stephen's personal build-in-public voice (the discovery-arc, "Silly me," "so I'm past this!"). That voice is for the X/Patreon campaign, **not** for app notes. App notes carry the Parallax documentation voice, not the author's personal narration.

---

## 2. The register blend — four voices, one note

An app note deliberately shifts voice by section, because its sections do different jobs. Knowing which voice you are in prevents both the dry-manual failure and the rambling-tutorial failure.

| Section (see creation guide §4) | Voice | Person | Feel |
|---|---|---|---|
| **Abstract**, **The Idea** | **Teaching** | mixed | Plain, motivated. Mental model before mechanism. Light analogy allowed. |
| **How It Works** | **Reference** | third | Precise. Bit fields, smart-pin modes, worked numbers, exact encodings. This is the manual register, borrowed. |
| **Build It**, **Adapt It** | **Build** | second ("you") | Directive but unhurried. "You configure the pin, then start the cog." Walk the reader through the worked example. |
| **See It Work / Verify** | **Empirical** | second/third | Concrete and honest. "You will see X. If you see Y instead, the most likely cause is Z." |
| **Pitfalls & Notes** | **Marker** | imperative | Compressed expert knowledge (⚠️ 💡 🔧). |

**The handoff is the craft.** A good note flows teaching → reference → build → empirical without the seams showing. The reader is told *why this matters*, then *exactly how it works*, then *walked through building it*, then *shown how to confirm it ran* — and never notices the voice shifting under them.

---

## 3. What we DO say / what we DON'T

### 3.1 DO

| Pattern | Example |
|---|---|
| Anchor in the outcome | "By the end you'll have a 1 MHz PWM signal on a pin with no cog overhead." |
| Why before how | "Smart pins do this so the cog never has to toggle the pin itself." |
| Worked numbers (P1 habit, kept) | "At 200 MHz sysclock, a Y value of `$8000_0000` gives exactly 100 MHz." |
| Direct second person in the build | "Set `WRPIN` first, then `WXPIN`, then raise `DIR`." |
| Honest verification | "The DEBUG scope should show a steady square wave. A *drifting* edge means the period and the NCO frequency disagree." |
| Adaptation guidance | "To change the frequency, you change only `X`; everything else stays the same." |
| Name where to go deeper | "For every NCO mode and its exact encoding, see the Smart Pins User Guide." |

### 3.2 DON'T

| Avoid | Why | Instead |
|---|---|---|
| "Let's explore the wonderful world of…" | Tutorial padding | "This note shows how to…" |
| "Simply set the pin and you're done!" | Dismissive; hides real complexity | State the actual steps |
| "Congratulations, you did it!" | Tutorial celebration | (omit — the working result is the reward) |
| "You might wonder whether…" | Hedging | State the fact or the choice directly |
| Re-teaching P2 basics from zero | That's the manual/tutorial's job | Link to it; assume the stated prerequisites |
| A feature tour with no build | That makes it a manual chapter, not an app note | Keep one concrete outcome in view throughout |
| Unsourced capability claims | Trust-chain violation | Verify first (creation guide §5), or don't write it |

### 3.3 Register contrast

| Aspect | DeSilva Tutorial | **App Note (this series)** | Reference Manual |
|---|---|---|---|
| Organized around | a learning journey | **one application/outcome** | the silicon taxonomy |
| Person | second ("you") | **second for the build, third for the mechanism** | third |
| Breadth | broad, progressive | **single technique, deep** | comprehensive |
| Tone | warm, encouraging, celebratory | **warm but purposeful, never celebratory** | authoritative, neutral |
| Worked example | many, progressive | **one complete, runnable, validated** | targeted, illustrative |
| "Why" | extensively, with stories | **briefly, to motivate the build** | rarely (assumes it) |
| Reader leaves with | understanding + confidence | **a working result they can adapt** | a fact they looked up |

---

## 4. Enhancement markers

App notes use the same marker family as the manuals, so a reader moving between documents sees one consistent system. Markers compress into a findable note the expert knowledge a tutorial would spread across paragraphs.

| Marker | Use for | Example |
|---|---|---|
| **⚠️ Pitfall:** | A common mistake with a non-obvious or silent consequence | "⚠️ **Pitfall:** Configure the pin's mode with `WRPIN` *before* raising `DIR`. Reversed, the first output cycle is undefined." |
| **💡 Tip:** | A non-obvious technique, shortcut, or optimization | "💡 **Tip:** You can change the frequency on the fly by writing a new `X` with `WXPIN` — no need to stop the pin." |
| **🔧 Hardware:** | A silicon-level detail that affects how you use it | "🔧 **Hardware:** The smart pin runs from the cog's clock domain; at sysclock/2 the minimum period doubles." |
| **🔍 Verify:** | How to confirm, on the bench, that this step worked | "🔍 **Verify:** DEBUG should report a count within ±1 of the expected value once per second." |

`🔍 Verify` is **specific to app notes** — it carries the empirical-grounding job (P1 used scope captures inline; we mark the confirmation step so the reader always knows how to check their own result).

---

## 5. Terminology & formatting

App notes inherit the house formatting so code, symbols, and bit fields look identical across the documentation set.

- **Instructions / directives** in prose: **UPPERCASE, not bold** — "the WXPIN instruction." Write the bare mnemonic in uppercase; the shared `p2kb-platform-mnemonic-bold` filter (v3.0 policy, 2026-06-29) renders mnemonics uppercase in prose and code so a prose mention and a code occurrence read as the **same** token. **Do not wrap mnemonics in `**…**`** — bold is reserved for genuine emphasis, and spending it on every mnemonic dilutes that signal ("ransom-note" effect). This matches the P2 Assembly Language Reference Manual.
- **Symbols / constants** in monospace: `P_PWM_TRIANGLE`, `P_OE`.
- **Bit fields**: bracket notation — `D[31:28]`, `X[15:0]`.
- **Binary** with underscores: `%0001_0000`. **Hex** with `$`: `$8000_0000`.
- **Code** in fenced blocks labelled ` ```spin2 ` / ` ```pasm2 ` (never code-division fences — see the masters convention). Code does **not** wrap; over-long lines are an authorship defect (creation guide §6, code-line budget).
- **Teach the compiler's symbolic constants**, not their arithmetic values — show `P_PWM_TRIANGLE`, validate the symbol↔value off to the side rather than substituting the number.
- **"cog"**, lowercase in prose — never "CPU," never all-caps "COG" (capitalize "Cog" only in headings / sentence-start / numbered "Cog 0").
- **Version-gate** any feature that needs a minimum Spin2/PNut: state it in prose and let the gate live where the KB owns it.
- **Official titles**, not nicknames — no "Silicon Doc"/"Blue Book"; name a document a newcomer can search for.

---

## 6. Section-specific voice

**Abstract.** 2–4 sentences. The capability + the value proposition. Keep the P1 convention — it is the strongest thing the P1 notes do. "The P2's smart pins generate PWM with zero cog overhead. This note shows how to configure a pin for PWM, set its frequency and duty, and change them on the fly — a pattern that replaces a dedicated timer cog."

**The Idea.** Teaching voice. The mental model *before* any register detail. This is where we fix the P1 notes' biggest pedagogical weakness — they often open with bit-field tables. We open with the concept.

**How It Works.** Reference voice. Precise, worked, exact. Borrow the manual register wholesale here; this is the section a returning reader scans.

**Build It.** Build voice. One complete program, walked through. Every example compiles under `pnut-ts` (creation guide §5). Comments explain *why*, never restate the instruction.

**See It Work / Verify.** Empirical voice. What success looks like, and the honest failure branch. Never skip this — it is what makes a note trustworthy.

**Adapt It.** Build voice, generalizing. The parameter space, the variations, where it breaks. Concrete first, then general (concreteness fading).

**Conclusion.** Consolidate the *concept*, not just list capabilities (a small upgrade over the P1 conclusion-as-feature-list).

---

## 7. Quality checklist

**Voice**
- [ ] One concrete outcome is in view from the Abstract to the Conclusion
- [ ] "Why" precedes "how" in The Idea and How It Works
- [ ] Build sections address the reader directly; mechanism sections stay precise
- [ ] No tutorial padding ("let's explore"), no celebration ("congratulations")
- [ ] No hedging in factual statements

**Empirical honesty**
- [ ] A 🔍 Verify step tells the reader how to confirm success on their own bench
- [ ] At least one honest failure branch ("if you see X instead…")
- [ ] No capability claim that isn't sourced (creation guide §5)

**House consistency**
- [ ] Instructions UPPERCASE (not bold); symbols monospace; bit fields bracketed
- [ ] Symbolic constants taught, not raw numbers
- [ ] "cog" lowercase in prose
- [ ] Every code block compiles under `pnut-ts`
- [ ] Markers (⚠️ 💡 🔧 🔍) used where they earn their place
- [ ] Deeper material pointed to by official title, not re-taught

---

*Version 1.0 — initial app-note voice guide. Distilled from the Parallax P1 application notes (AN001/004/008/013/014) and the P2 manual voice family, with a pedagogical layer added. See `APP-NOTE-CREATION-GUIDE.md`.*
