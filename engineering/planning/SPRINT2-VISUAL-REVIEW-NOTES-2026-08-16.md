# Sprint 2 — Stephen's Review Notes (2026-08-16)

Delivered in chat after the «#234» opus-master gate was released (commit
`fea28f1c`). Recorded VERBATIM below; discussion and disposition follow in the
second section. These are content/pedagogy observations, not render defects —
they precede the «#235» release wave.

---

## VERBATIM — as given

```
my notes::DeSylva:
    - the whole missing deadlines argument likely fails.  What about applying concepts from our architecture manual instead of this argument?
    - re: library  for everything culture - there have to be better arguments than you are offering...
    - even the RP2350 familty still suffers from i/o comms choice mapping, less so than others, but if this matters....
Streamer Guide:
    - we now have right/wrong pattern are we using the correct color block form for it?
Xbyte:
    - decribing why _RET_ CALL doesn't work - is that appropriate? or are we decribing why we removed a bad example - and therefor talking about something we needn't?  We should tell the story if we need to, i'm just asking... to ensure is has real pedagogical purpose.
Manuals overall:
    - is there any value in containing a changelog when an external is provided for each manual we publish?
```

---

## Numbered observations (for discussion)

| # | Element | Observation |
|---|---------|-------------|
| **V-1** | deSilva | The "missing deadlines" argument likely fails. Consider applying concepts from the architecture manual instead. |
| **V-2** | deSilva | The "library for everything culture" argument needs better support than currently offered. |
| **V-3** | deSilva | Even the RP2350 family still suffers from I/O comms choice mapping — less so than others. Relevance to be decided. |
| **V-4** | Streamer Guide | A right/wrong pattern now exists — confirm the correct color block form is being used for it. |
| **V-5** | XBYTE | Is describing why `_RET_ CALL` doesn't work appropriate, or are we narrating the removal of a bad example (i.e. discussing something we needn't)? Tell the story only if it carries real pedagogical purpose. |
| **V-6** | Manuals overall | Is there value in an in-document changelog when an external CHANGELOG is published alongside each manual? |

---

## Disposition

*Filled in as each observation is discussed and decided. Nothing is applied
until all have a disposition.*

### V-8 — voice-guide conformance (Stephen, 2026-08-16) — **RESHAPED THE WHOLE PLAN**

> "have we reviewed each touched manual against its updated voicing guide?"

**Answer: no — and Sprint 2 was always supposed to.** Sprint 1 normalized every voice
guide (2026-08-15; deSilva's was *created* then) precisely so Sprint 2 could apply
them. Sprint 2's task list enumerated the nine correction targets and the
damage-investigation repairs but **never carried an "apply the voice guide" task**, so
the standard got built and then not applied. Tasking defect, not a scope change.

**This is not a new sprint.** It is open Sprint 2 work, sequenced before the wave.

**THE OPERATING RULE — conform-on-touch (Stephen):** all voice guides were normalized
up front so that *any* manual we later touch has a current standard waiting. Whatever
brings us to a manual, we bring that manual **fully forward** while we are in it.
Manuals we are **not** touching are **not** pulled in — they take their pass when
something next brings us to them. The fleet converges; no big-bang sweep is ever needed.

**Why full-manual and not diff-scoped.** Conformance is a property of the **artifact**,
not of a changeset. The masters predate the standard, so no body has ever been measured
against it. Evidence already in hand: of V-7's six deSilva findings, only A3/A5/B1 fall
in the Sprint 2 diff — **A1 (L6045), A2 (L5940), A4 (L3897) are pre-existing body text.**

**The instrument matters more than the effort.** My V-7 sweep was signature-based and
produced a **false positive the guide caught**: B1 recommended cutting reader-celebration
that deSilva's guide explicitly protects as pedagogy. Signature-sweeping without the
guide does not merely miss defects — it proposes damage. See the guardrail in «#240».

**Structure:** one pass per document, with that document's agreed V-findings **absorbed**
into the pass — not applied first and conformance-checked after, which would write the
same prose twice and have the second pass judge what the first just wrote.

Tasked as «#240» (method + guardrail) · «#241» deSilva · «#242» Streamer · «#243» Debug
Window · «#244» Assembly · «#245» XBYTE · «#246» IOSP (master only, not releasing) ·
«#247» P2AN001+P2AN002 · «#248» V-6. Wave «#235» gated behind all of them.

### ⚠️ Wave composition corrected (2026-08-16)

«#235»'s task text named the wrong seven — IOSP **in**, P2AN001 **out**, which is
backwards. Verified against the CHANGELOG **files**: seven elements carry a new
`2026-08-16` entry — deSilva 3.0.6 · Streamer 1.0.9 · Debug Window 1.1.3 · Assembly
3.1.6 · XBYTE 1.0.2 · **P2AN001 1.0.4** · P2AN002 1.0.3. **IOSP's latest is still v1.0.8
(2026-08-08)** — no entry, no bump. Left uncorrected, the wave would have tried to release
a manual with no changelog entry and skipped one that had both. *A status line is not
evidence* — second occurrence this sprint.

### How the passes are run (Stephen, 2026-08-17) — three constraints

> "generally find all there is to find, but be wary that our corrections are being
> applied correctly, we still need to make sure that our voice gating is correct
> for each manual"

**1. Exhaustive, not sampled.** Find everything there is to find in the manual being
touched. A partial pass that reports "conformant" is worse than no pass, because the
next visit trusts it.

**2. Verify the correction landed, don't assume it.** Applying a fix is not evidence the
fix is right. Each correction is re-read in place, in its final context — the surrounding
prose may no longer parse the way it did before the edit, and a repaired sentence can
break the paragraph around it. This is the same discipline as verifying the rendered PDF
rather than the compile log.

**3. ⚠️ THE GATE ITSELF IS UNDER TEST — the pass is bidirectional.** Each manual's
voice-guide declares ADOPT / ADAPT / REJECT per house rule. **Those declarations can be
wrong**, and this is the first time most of them meet their manual's actual body.

> **When a declared row fights the document, that is evidence about the ROW, not
> permission to force the prose.** Stop, adjudicate, and if the row is wrong, fix the
> guide — then apply the corrected row.

This is not hypothetical: it is precisely how the earlier damage happened. IOSP's
*"Never hedge"* row, applied mechanically, would strip exactly the qualifiers §2.2a
requires — the row needed a carve-out, not the prose needing flattening. deSilva's guide
already carries two corrections of this kind, both decided by measurement rather than
taste (*"ADOPT the defect — REJECT the phrase list"*; Self-admiration adapted to protect
reader celebration).

**Record every adjudication back into that manual's `voice-guide.md`** — an undocumented
rejection reads as an oversight and gets "fixed" by the next sweep. The guide's own words.

### What the voice changes were (Stephen, 2026-08-17)

The guide changes were **mostly narrative/prose**. Narrative-dominated manuals were worked
**first** and already carry their treatment. What remains — this family — is the manuals we
are here for **because they have errors**; the narrative changes ride along at the same
visit **so that work is not lost**.

**Scope the pass to prose, not to line count.** The guides govern narrative: explanatory
prose, chapter framing, transitions, asides, closings. They do **not** govern reference
apparatus — instruction tables, encodings, register layouts, code blocks, quick-reference
matter. Assembly and Streamer are mostly reference, so their real prose surface is far
smaller than file size implies. **deSilva is the outlier — almost entirely narrative, and
therefore the big one.**

### Standing directive (Stephen, 2026-08-16)

> "my goal to fix what's relevant, queue as little as possible"

Applied by splitting open items on **why** they wait. Blocked on **effort** ⇒ fix
now. Blocked on **evidence** ⇒ stays open, because fixing without a source is the
failure this sprint exists to remove.

| Item | Blocked on | Call |
|---|---|---|
| V-4 IOSP sites (×4) | nothing — my category error | **FIX NOW** |
| F-279 XBYTE citation | nothing | **FIX NOW** (in-wave) |
| **F-275** IOSP §19.5 5V bus power | nothing — §19.8 already correct; one-site internal contradiction | **FIX NOW** |
| **F-272** `%TT` streamer-driven DAC | **evidence** — ungrounded in every source we hold; needs a bench run | **stays open** (§17.1 correctly avoids the claim) |
| **F-274** IOSP §19.4 FS-USB at 80 MHz | **evidence** — the only source for the >80 MHz floor is a reviewer comment (upstream lead, not a citation) | **stays open** — asserting the floor would ship a wrong claim |
| F-268 guide-side sweep | nothing, but genuinely separable scope | flagged to Stephen, not silently absorbed |
| F-271 → PL-004 companion version strip | post-wave by design | punch list |

| # | Disposition | Notes |
|---|-------------|-------|
| V-1 | **ACCEPTED — rewrite** | Replace App. A *"What You Are Buying With That"* with a SHORTER section built on the composability claim (adding a task to a shared core perturbs existing timing; a cog does not), grounded in ownership + cadence. **Concept from the Architect's Guide, NOT its vocabulary** — no "forces"/"cadence boundary"/"Force 1"; use only cogs/pins/locks, which the reader has earned over 16 chapters. Cross-ref to Architect's Guide Ch.7 is an INVITATION, not a dependency. **Test: the section must stand fully alone for a reader who never opens that book.** Lighter = fewer new terms, NOT a weaker claim. Sweep the same shape at lines 225, 6001, 6049; line 4275 is legitimate technical usage — leave. Route as **F-276**. |
| V-2 | **ACCEPTED — rewrite** | Line 5985 cost statement stays EXACTLY as is (honest, and the price of being believed). Replace line 6013's "you understand every layer" consolation with: (1) PRIMARY — the unit of reuse differs, so library count is not apples-to-apples: elsewhere a library shares your thread of control and you inherit its blocking/interrupts/timing (two libraries wanting the same timer = debugging someone else's code inside your timing budget); on P2 the reused thing takes a cog + pins and hands you a mailbox, so that conflict class doesn't arise. (2) PRACTICAL — smart pins handle bit-level protocol timing, so a P2 driver written from the datasheet is a smaller job than the same sentence implies elsewhere. DROP the "help is available" tail (Community Resources owns it 3 paragraphs above). Vocabulary check: cogs/mailboxes/smart pins all earned (Ch.14, Ch.16). **BOUNDARY — keep argument 1 explicitly narrow:** it removes the INTEGRATION tax, not the writing cost. The gap is real and costs hours; do not let it drift into "the library gap doesn't matter" (that is the same overclaim we are removing). |
| V-3 | **ACCEPTED — rewrite, scarcity framing** | **DROP the pin-mapping angle** — research shows PIO reaches ALL GPIO ("SIO, PIO0, PIO1 and PIO2 can connect to all GPIO pins", DS §1.2.3), so mapping is the half that does NOT survive an expert reader. Constraint is real only for the HARDENED peripherals (2×UART, 2×SPI, 2×I²C on fixed repeating pin subsets). **Use scarcity + shared program store:** 12 state machines in 3 blocks, the 4 machines in a block sharing ONE **32-slot instruction memory** (DS §11.2, §11.2.8) — the wall PIO users actually hit. Contrast: 64 independent smart pins + 8 cogs with private 2 KB program stores. **2–3 sentences max.** Cite RP2350 Datasheet + Product Brief as DOCUMENTS (no revision-specific pages). **Never quote the agent doc's "up to 320 MHz"** — our KB rates P2 at `recommended_max_mhz: 180` / `overclock_tested_mhz: 320`; any side-by-side is 150 vs 180. |
| V-4 | **ACCEPTED — fix Streamer + Debug Window, log IOSP** | **Answer: no, we are not.** Platform provides `AntipatternBlock` (`p2kb-platform-content.sty:277`, red) via ` ```antipattern ` / `::: antipattern` (`p2kb-platform-code-coloring.lua`). **Verified BOTH templates already load it** — `p2kb-streamer-reference.latex:21`, `p2kb-debugwin.latex:23` — so **markdown-only, zero platform cost**. Set-wide audit: deSilva (6 sites) + Assembly (appendix-h L569) use ` ```antipattern ` ✅; **Streamer L1016, Debug Window ch12 L66+L186, IOSP appendix-e L98/202/278 + ch17 L172 use ` ```spin2 ` ❌**. Streamer is worst — correct AND wrong lines share ONE block with identical highlighting, and it is the EF-053 `P_OE` material where mis-copying is silent + total (6,737 vs 1,407 ADC counts). **FIX:** split Streamer into two ADJACENT blocks (correct = `spin2`, wrong = `antipattern`) — green beside red is stronger contrast than two comments. Fix Debug Window's 2 sites in the same pass (in-wave, same stack). ~~IOSP: log only~~ → **REVISED 2026-08-16 under Stephen's "fix what's relevant, queue as little as possible":** **FIX ALL SEVEN SITES including IOSP's 4.** My original call conflated *"in the release wave"* with *"fix now"* — they are independent. Editing IOSP's opus-master does NOT add IOSP to the 7-element wave; the correction sits in the master and ships at IOSP's next release. `p2kb-iosp-reference.latex:22` loads `p2kb-platform-content`, so IOSP is markdown-only too. Route as **F-278**, per-site table = the work list. |
| V-5 | **ACCEPTED — KEEP, make purpose visible** | **Answer to the question: it is NOT narrating our repair** — the §15.3 `::: hardware` block is written purely reader-facing (no prior version, no "we found"). It has real pedagogical purpose, and specifically it **discharges a debt the chapter's own teaching creates**: `set_nz` ends `_ret_ muxc` and `op_jmp_abs` ends `_ret_ rdfast` — the book folds returns TWICE within 20 lines — so a reader who just learned the idiom will ask "why not `_ret_ call`?" We induced the question; answering it closes a loop we opened. Reader also gets no help elsewhere: it **assembles clean** (pnut-ts = legality, never semantics) and the failure is silent + layout-dependent. **FIX: add one clause tying it to the `_ret_ muxc`/`_ret_ rdfast` examples**, converting it from a free-standing gotcha into "the boundary of the idiom you just learned." KEEP the silicon-measurement paragraph — it is what lets a reader RECOGNIZE the symptom. Trim ~1 sentence elsewhere. |
| **F-279** | **ACCEPTED — single site, in-wave** | ⚠️ **My first reading was WRONG and is corrected here.** I reported *"P2 Assembly Language Reference Manual"* (xbyte-body.md:1427) as a fabricated name. **It is not** — that is the cover title of OUR OWN manual (`p2-assembly-language-manual/opus-master/front-matter.md:20`). The actual defect is **circular grounding**: §15.3 grounds a load-bearing hardware claim (`_RET_` semantics) on a **sibling manual in the same family**, which is a peer derivation, not authority — and unlike P2AN002:378 it does NOT disclose the relationship, so it reads as external. **FIX: repoint to the Parallax primary source** — *Propeller 2 Assembly Language (PASM2) Manual* draft (2022-11-01, p.68) and/or *P2 Instructions v35* (row 410), which is what F-273 was actually grounded on. **No set-wide normalisation needed** — the other 4 sites are fine (deSilva 5845 uses the Parallax name correctly; the rest are a CHANGELOG font note and our own cover title). |
| V-6 | **ACCEPTED — demote, all 7 app notes** | **Premise is narrower than the question assumes: NO manual carries an in-doc changelog** — manuals are already external-only, nothing to remove. Only the **7 app notes** carry a "Revision History" table. **There IS real value, but narrow: the PDF travels alone.** `P2AN002.pdf` gets downloaded/emailed/forum-attached; `p2an002-changelog.md` does not go with it — and app notes ship CODE, so a reader must know whether their `-src.zip` matches their PDF. **What is NOT justified is the current form** — full narrative paragraphs duplicating the external changelog verbatim, costing three version locations to sync and two records that can disagree with no stated authority. **FIX: the two artifacts get DIFFERENT jobs** — external CHANGELOG = narrative record; in-doc section = **identity + provenance** (one terse line per version: version, date, short phrase + pointer to the external changelog). **Apply to ALL SEVEN app notes in opus-master**, not just the 2 in the wave — editing the master does not ship the document, and a half-migrated format across one family is worse than either end state; the other 5 carry it at their next release. NOTE: this is a **design decision, not a defect** — nothing is wrong today, only redundant. |
| **V-7** | **ACCEPTED — one group** | Sweep of deSilva for the same failure shapes (added by Stephen 2026-08-16). **Group A — factual overclaims:** A1 line 6045 "peripheral conflicts become impossible" and A2 line 5940 "eliminates peripheral conflicts" are **FALSE in the way that costs a reader time** — smart pins remove the *pinmux* conflict, NOT *resource* conflict; our own Architect's Guide Force 1 documents that two cogs on one bus corrupt it silently (P2 pin outputs are OR'd, no arbiter). **Route A1/A2 as F-277** (wrong technical claim, not weak argument) + class-wide check for the same phrasing in other manuals. A3 line 6042 "eliminates entire categories"; A4 line 3897 "No surprises, ever / Timing is guaranteed" (self-contradicted by the correct hedge at 5911 — 5911 is right); A5 line 3729 "impossible to achieve this precision with interrupts" (V-1 strawman). **Group B:** B1 line 5804 identity flattery ("you see solutions that others miss") + repeat of the impossibility strawman. **Group C — the one substantive addition:** C1 **Ch.11 "Why No Interrupts?"** reframe — an interrupt multiplexes several cadences onto one processor; a cog lets each cadence own hardware. **Narrow: reframe the opening argument only, do NOT rewrite the chapter** (examples/code are fine). Line 4314 "3 cycles, guaranteed" (LUT) — verify against KB before touching; believed correct. **BOUNDARY: this is not a voice rewrite.** deSilva's playfulness, dad jokes, and direct address are the inheritance and stay. We remove unsupported CLAIMS, not personality. |

---

### ⚠ V-6 scope — the two records disagree, and only half is done (2026-08-17, «#248»)

**Applied to P2AN001 (v1.0.4) and P2AN002 (v1.0.3) only. P2AN003–P2AN007 still carry the old
narrative Revision History.** This needs Stephen's call, because two of his own recorded decisions
point opposite ways and I did not want to resolve it silently while he was away:

- **This file's V-6 row says ALL SEVEN**, with a reason specific to this change — *"a half-migrated
  format across one family is worse than either end state."*
- **Task «#240» says the opposite**, recorded later: *"Applied: V-6 narrowed from 7 app notes to the
  2 in the wave"* — conform-on-touch, we only bring forward what we are touching.

I followed the **narrower** one, because it is the later decision and because widening scope
unilaterally is the worse error of the two: doing five more notes cannot be undone by a preference,
whereas doing them next is one short pass. **But the V-6 row's reasoning is the stronger argument on
the merits** — the format split is the whole point, and a family where two notes say "see the
changelog" and five reproduce it is exactly the disagreement V-6 exists to remove.

**The remaining work is small and mechanical**: each note's Revision History becomes a version/date/
one-phrase table plus the "this is version X, the ZIP is versioned with it, the changelog is the
authority" frame. P2AN001 and P2AN002 are the worked pattern. Say the word and it is one pass.
