# Act III Seed — The Same Work, with an Agent (transcription capture)

**Status:** CAPTURE COMPLETE (12/12); **SYNTHESIZED into the manual** as Act III / Part III (Ch 10–14,
v0.3.0 draft, 2026-07-08). **26 principles** now (P-1…P-26; P-25 autonomous-loop + P-26 understanding-gate
added 2026-07-08). The Act I ↔ Act III spine stays **item-for-item aligned**.
Raw dictation from Stephen + light structuring. Companion to `act1-seed-transcription.md`: for **each
of the same 12 projects**, walked **in the same order**, Stephen dictates *where an agent helped (or
didn't)*. This is the seed for **Act III Ch3 "The Same Work, with an Agent."** Kept parallel to the Act I
capture so the Act I ↔ Act III spine stays **item-for-item aligned** (the one structural invariant).

**Method (mirrors how Act I was built):** per project, Claude puts the project's **Act I attention-list**
in front of Stephen; Stephen dictates the agent story for that project; captured faithfully below. For the
**five post-AI projects** (#5, #6, #9, #11, #12) the Act I doc already holds real AI evidence — those are
shown back for confirm/correct/extend rather than re-dictated. When all 12 are captured, Claude studies the
whole set and synthesizes a **unified** Act III chapter (same as Act I's consolidated spine → Chapter 1).

> **Capture discipline.** Faithful to Stephen's facts/experience — nothing invented. `[?]` = circle back.

---

## CHAPTER-LEVEL PRINCIPLES (emerging across projects)

*Cross-cutting framings that should shape the whole Act III chapter, lifted out as they surface.*

- **P-1 · Don't prescribe the agent (Project 1).** Different agentic tools are built for different kinds
  of work — some are stronger at images, some at broad web research (e.g. **Perplexity**, which gives very
  broad information and then drills into examples and sources). This is *not* a knock on Claude Code; the
  same jobs are entirely doable there. It's habit and fit: Stephen reaches for the web-based tool for broad
  domain research and the terminal agent for build work. **We all have our favorite agents. The chapter
  must let the reader use whatever agents they're comfortable with — never prescribe a specific one.**
- **P-2 · Best-researched, not first-or-easiest (Project 1).** The deepest change an agent makes to
  Stephen's *method*: a broader domain search surfaces more possible answers, so the answer you commit to is
  "no longer the first or easiest — it's the **best researched**," and you're *more convinced* of the single
  direction you chose. That's how he likes to learn. *(Strong candidate for the Act III through-line.)*
- **P-3 · A KB-backed agent already knows the P2 techniques (Project 1).** What once required studying the
  code and talking to Chip directly, an agent backed by the **P2 Knowledge Base** now simply *knows* — it can
  enumerate the two/three/four techniques the P2 makes available for a given problem. *(Closing-symmetry tie:
  the KB this guide is drawn from is the same body the agent draws on.)*
- **P-4 · Agent as decision-partner, not just executor (Project 1).** Repeatedly the win isn't "the agent
  wrote the code" but "the agent helped me *decide*" — which axes of a part are worth characterizing, whether
  to keep a control layer or transform over it, how to unify two domains' APIs. It serves the judgment; it
  doesn't remove it.
- **P-5 · Instruments as troubleshooting partners (Project 2).** Two moves. (a) The agent **annotates the
  code** with the logic-analyzer pin/wire/color map spoken aloud during hookup — so code and documentation
  stay *together*, retiring the hand-kept journal Stephen used to verify by hand. (b) Show the agent a
  capture that *looks wrong* and it **proposes why** — a miswire, a connection to recheck. The instrument
  becomes a troubleshooting partner. Generalizes to **scopes and any external measuring equipment**.
- **P-6 · Theory-of-operations from any source (Project 2).** First-contact move on an unfamiliar codebase:
  have the agent **inventory the repo** (how many executables/programs; which are library, which matter to
  you) and generate a **theory of operations** — *what it does, why, how* — for each important piece,
  **regardless of language**. You learn the code deeply **without reading a line**, then reuse its techniques
  translated to Spin2/PASM2. *(The agentic form of Act I's "translate & digest reference code.")*
- **P-7 · You own the *why/where* of performance; the agent maps it to P2 resources (Project 2).** The
  developer decides **where** performance matters and **why**; the agent then helps decide **how** to meet it
  with P2-specific architecture — LUT RAM, PSRAM, CORDIC, the streamer. A clean division of labor: human owns
  the need, agent owns the resource-mapping.
- **P-8 · Design for the family up front, not per-instance rework (Project 2).** Bringing up instance 1, then
  2 (reveals some commonality), then 3 (reveals more) forces **rework each time**. Tell the agent the
  **family** you anticipate and it researches and **proposes the breadth of interface early** — study the
  *group*, not one at a time — so later instances slot in without rework. *(Project 3 extends this: the agent
  **accretes a per-family knowledge base** — documented "what's unique" for every panel set already brought
  up — so each new member onboards against all the prior ones: what the driver already enables, what's
  missing, how to coordinate.)*
- **P-9 · Name the frames of reference; the agent works within them (Project 3).** The complex, rework-prone
  code — rotation, daisy-chain topology, pixel mapping — becomes tractable once **the human establishes the
  perspectives**: *treat the set of panels as one display; the wiring entry point is here; the panel order on
  the single wire may vary; these config constants describe that order; the panels need an init chain.* Named
  those, the agent correctly derives the **wiring, the bit-ordering, the JTAG-like init chain, and the
  replication**. The human's real contribution is **defining the frames** so the agent stays inside them.
  *(Direct tie to Act II's plane/perspective conflation — naming the frame is the guard.)*
- **P-10 · Agentic output guides agentic code generation (Project 3).** A **theory of operations that captures
  timing**, generated first, then handed **back to the agent as its implementation guide**, measurably
  improves the **accuracy of the first-pass implementation**. Using agentic output as the input that steers
  agentic codegen is a code-strength technique. *(Two-stage: derive the intermediate doc → build from it.
  Extends P-6 from comprehension into construction.)*
- **P-11 · You define the documentation system; the agent maintains it (Project 3).** Cataloging boards,
  keeping a **changelog** of what changed each pass, and holding the **whole documentation repository**
  consistent are now the agent's to keep — **provided you guide it** on which documents do what, why, and
  **when each must be updated**. That guidance is itself a reusable **skill** Stephen brings to the agent.
- **P-12 · The mindset: *sufficient guidance*, not the perfect prompt (aside, Project 4 — spans ALL
  chapters; candidate to OPEN the chapter).** Stephen explicitly **rejects the "find the right prompt"**
  framing. His question is always: *how do I give the agent **sufficient guidance to do high-quality
  work**?* For generating code, that guidance runs along **three dimensions** (the questions he asks
  himself):
    1. **Requirements** — what the code must actually do.
    2. **Process** — how to apply the *process* of generating that code.
    3. **Foundational understanding of the target language** — a real grounding in Spin2/PASM2.

  Delivered through **three concrete mechanisms** — one per dimension:
    - **Requirements (1)** ← **documentation generated by agents on the problem domain** — the
      **theory-of-operations** docs (→ P-6/P-10) — used as the **input to what needs to be coded**.
    - **Process (2)** ← **process inscribed into skills.**
    - **Foundational language understanding (3)** ← the **P2 Knowledge Base MCP** — confirmed by Stephen as
      *"the third arm."* The **p2kb MCP fully describes the P2 architecture and the P2 language**, and the
      agent draws on it to **write correct code for the P2**. Stephen: **"This is deeply important."** *(This
      is the mechanism behind P-3, and it closes the chapter's loop — the same curated KB this guide is drawn
      from is what makes the agent a competent P2 partner.)*

  And around all three: **Stephen's own careful guidance of the design/implementation goals.** The three
  mechanisms supply requirements, process, and language; the human supplies **intent**.
- **P-13 · Cheap iteration unlocks exploration — and that's where the fun is (Project 4).** By hand,
  generating a *single* transition set is so much work that getting **one** working means **burnout** — he's
  done, no appetite to try another. The agent drops the **per-experiment cost** enough that he can **play with
  alternative techniques** and go **broader**. His recurring "where does the fun come from?" answer: *less
  time per aspect → more of the design space actually explored.* *(Complements P-2: P-2 is a better **single**
  answer drawn from breadth; P-13 is **more answers tried** because each one is now cheap.)*
- **P-14 · Isolation-test components so they enter the system already trusted (Project 5).** When he builds a
  middle component (e.g. the **FIFO**), he makes it a **standalone object** and uses the agent to **generate
  its regression test**, proving it works **before** wiring it into the driver. By the time the component is
  in the full application it is a **tested component** — so during system debugging it's **no longer a
  suspect**. Agent-written unit/regression tests shrink the space of "what's broken."
- **P-15 · The KB keeps improving — re-audit old code against the *current* KB to unlock what wasn't reachable
  before (Project 5).** He **never got the OLED fully performant**; since then the **p2kb has improved** —
  better examples, and **fixed bugs** that had blocked getting **smart pins** working for that OLED. The plan:
  go back with the agent, run a **full audit of the code against the current p2kb**, find what can be
  adjusted, drive the **smart pins**, and reach full speed — *"I have no doubt."* *(Reinforces P-3 and the
  closing symmetry: the better the KB, the better the partner — and a stalled-on-performance project revives
  because the KB moved. Sibling to Project 11's diff-and-port revival, but the lever here is the **improved
  KB**, not a vendor update.)*
- **P-16 · Diff your own old vs. new version to fix a self-introduced performance regression (Project 3,
  added on the Project 6 turn).** A user of an **earlier version** reports the **newest version is *less*
  performant**. The agent is good at studying the **early shipping code**, contrasting it against the **new
  shipping code**, **localizing the affected regions**, and **proposing the fix** to restore the original
  performance on the current codebase. Stephen is doing exactly this with the **LED-matrix** code right now.
  *(Third member of the "diff-based revival" family: **P-15** = diff vs. the improved KB; **Project 11** =
  diff vs. a vendor update; **P-16** = diff vs. your own prior version.)*
- **P-17 · The exoskeleton metaphor — amplification beyond your own reach (Project 6; chapter-defining
  image).** Stephen's central image: *agentic coding is to development time what an **exoskeleton** is to
  human strength and agility* — it **amplifies**, letting you do things **you could not have done yourself**.
  More in less time → **learn more, do more, have more fun** in shorter time; it makes the whole embedded
  environment fun again. Key facet: amplification lets you **exceed the scope of the single object** — once
  the agent makes the hard core (arm motion) tractable, you **compose in new capability** (add a vision
  sensor: locate → grab → place, vision watching the gripper) and go far beyond where the lone object could
  reach. **Amplify, don't abandon (Project 10):** you needn't **leave your comfort zone** or stop doing what
  you already do well — keep your own knowledge and use the agent to **amplify** it; the goal is **fun**.
  *(Umbrella over P-13 fun-from-breadth and the ceiling-lift; strong candidate for the chapter's spine
  image.)*
- **P-18 · You are the agent's senses and hands in the physical world — supply the constraints it can't
  observe (Project 6).** The agent can't see the mechanism or hold the probe, so **you feed it the physical
  constraints**: a servo's **range of travel** once mounted (so the agent constrains motion and the device
  **doesn't destroy itself** during testing), the **achievable repeatability** (build algorithms that stay
  within what the hardware can actually do), the wiring, what a fixture allows. These are **requirements** in
  the P-12 sense — the subclass only a human at the bench can provide. *(The constructive flip side of the
  draft chapter's "what stays stubbornly yours" — logic analyzer, wiring, fixture — here they become inputs
  you hand the agent, per P-5.)*
- **P-19 · Reshaping for a hardware change is cheap with the agent (Project 6).** When the **hardware topology
  changes** — e.g. moving a **servo object *behind* a PWM-generation chip**, so the servo object now speaks
  to the **PWM chip**, which in turn drives the servo — you **describe the new indirection** and the agent
  **reshapes the code**. What used to be a re-engineering slog is now practical and feasible, grounded by the
  **p2kb**; you **change the hardware and get back on the air**, continuing where you left off, in a much
  shorter time. *(The object-modeling/indirection concern from Act II, made cheap; ties to P-3 and P-8.)*
- **P-20 · The agent guides the physical hookup even though it can't touch it (Project 7).** A refinement of
  P-18: the human still holds the wire, but "figure out the wiring" becomes a **guided, documented
  procedure**. Describe the **rig** you want, the **range of pins**, and **how to set it up**, and the agent
  can **prompt you to wire it up** step by step (*"here's what you said you'd do — let's do it now"*),
  **showing you what you need**, **producing a wiring-map document**, and **interactively walking you
  through** the hardware setup. *(Nuances the draft chapter's "it can't hold the probe": true — but it can
  hand you the map and walk you through it.)*
- **P-21 · The agent readies a one-off for public reuse (Project 8).** As you **describe the hardware shape**,
  the agent **recognizes the standalone, reusable pieces** and **suggests publishing them** (e.g. to
  **OBEX**) — it now understands reusability. It then builds the **regression tests** (through the hardware
  lashback), a **theory of operations**, and the **public documentation**; suggests **how to wire it up and
  coordinate**, and **how to stand up multiple I/O chains** of the kind. Crucially, because it's grounded in
  the **p2kb**, when you say *"I'm making this object external and sharing it — what should the docs speak
  to?"* it **already knows which P2 techniques are feasible** and **adds them to the documentation** —
  surfacing capabilities you didn't think to mention. *(Composes P-14 + P-6 + P-11 + P-20 + P-8 under a
  publication-readiness lens, grounded by P-3; maps to the **OBEX** artifact type.)*
- **P-22 · The agent onboards you to an unfamiliar (or long-dormant) platform (Project 10).** A *different*
  ceiling from the math ceiling of P-6/P-17: not "I can't do this" but "I've **never been on this platform**"
  (or haven't in years). Standing up the **Raspberry-Pi/Linux** side — which packages to install and how to
  configure them to **run a web server**, **get high-precision internet time (NTP)**, **talk to external
  APIs** — is second nature to Stephen (decades of Linux) but a wall to a newcomer. The agent helps a new
  user understand **what facilities are available**, **why you'd choose each**, then **installs the pieces
  they choose**. Value for the **expert = amplification**; value for the **newcomer = crossing onto a
  platform they've never used** (or need reminding of). *(A two-audiences read of the same tool.)*
- **P-23 · The agent puts a mobile control-panel app (and its BLE bridge) in reach (aside, Project 11 — spans
  all chapters).** Agents can build **full-scale mobile apps** (Android/iOS), so an embedded developer's
  **handheld becomes a control panel** for their P2 system. Add **Bluetooth / BLE** to the project — *a
  couple of wires* — to expose **command + status**; the agent handles **which characteristics to expose**,
  **populating the GATT**, the **device-side Bluetooth implementation and communication**, and the **phone
  app** itself. Connecting to a BLE device from an iPhone/Android is easy. **The democratization:** Stephen
  (an iOS developer who built libraries) could always reach this **because he had the skill** — now the
  embedded developer with agentic help **doesn't need the skill**; you supply **intent** and (for iOS)
  **license the tooling**. Building the app that controls your devices is now feasible for anyone. *(A whole
  new artifact — the companion app — comes into reach; extends P-17 amplification and P-22 platform-onboarding
  into mobile.)*
- **P-24 · Agent-amplified part selection — from intent to chosen part, fast (Project 12).** The technique
  that recurs on **nearly every sensor/actuator choice**: **market research**, **price-point finding**, and
  **ease-of-communication** assessment. Agentic help here is **immense** — **coming down to an answer**,
  **finding usage examples**, **finding YouTube how-to videos** — all amplified, so the **time from intent to
  chosen product is dramatically shorter**. *(Generalizes the Perplexity-sourcing of #5/#12; ties P-1
  tool-choice + P-2 best-researched + P-17 amplification; maps to Act I's peripheral-selection concern A3.)*
- **P-25 · The closed autonomous loop — write → compile → run → read → iterate (added 2026-07-08).** A
  **hosted** agent (e.g. cloud Claude Code) equipped with the full P2 toolchain — the **pnut-ts** compiler,
  the **pnut-term-ts** terminal/DEBUG host, and the **p2kb MCP** — closes the *entire* loop by itself: write
  code, compile it, **download and run it on a real P2**, read the DEBUG output/logs, and round-trip again
  and again, working **autonomously**. The difference between an agent that drafts code for *you* to run and
  one that runs its own experiments on real silicon and **converges** to an acceptance check. Powers P-14
  (agent-written tests actually get run *and passed*); the human still owns the target and the definition of
  "done." *(Placed in Ch 12, Building.)*
- **P-26 · Confirm understanding before you let it proceed — the reliability gate (added 2026-07-08).**
  Providing the resources (P-12) is necessary but **not sufficient**. Before the agent produces anything
  headed for production, have it **tell you back** its reading of the requirements, the process, and the P2
  mechanisms it intends to use, and **iterate on that understanding until it is complete** — only then let
  it move ahead. Success = result meets expectation, reached far more reliably by closing the understanding
  gap *before* the work than by correcting output after. A misunderstanding caught here costs a sentence;
  caught after the run, a debugging session; shipped, far more. *(Placed in Ch 10, The Mindset; pairs with
  P-12 sufficient-guidance and gates P-25's autonomous loop — confirm understanding before you let it
  converge on its own.)*

---

## Projects — agent capture
*(One block per project, same order/numbering as `act1-seed-transcription.md`. ⬜ = awaiting dictation,
✅ = captured. Post-AI projects carry existing AI evidence to confirm/extend.)*

### 1. P2-BLDC-MotorControl — ✅ captured *(pre-AI project; agent story is "how I'd do it now")*

**Framing note (Stephen):** he can see how he'd use an agent here in his mind's eye. If he did the job well
the agent would likely land on a **somewhat different — but not too different — public API**.

**Per attention-item (agent lens):**
- **Research the domain** — this is where he'd reach for **Perplexity**: broad information first, then it
  drills down into examples and sources. Doable in Claude Code too; Perplexity is just more natural/habitual
  because it's web-based, not in the terminal. *(→ Principle P-1.)*
- **Design the unifying interface** — once *he* chooses the sources, the agent picks up the details of each
  source and **proposes a unified interface**: what parts of each source's interface stay, and how to unify
  similar pieces so one API spans **both forms of implementation**. Coming from **LEGO** is a different domain
  than coming from **raw servos**; a unified API that satisfies both must **share**, and needs **identifying
  parameters** that let it decide how to behave / how to treat the inputs for ease of use. The agent
  designing the structure would be reasoning about exactly this.
- **Adapt + implement the control** — the interesting research part: he had to **deeply understand what the
  control was**, then decide **how much to keep vs. implement our own**. (In the end he kept **exactly** the
  control.) An agent lets you research the possibilities first — *should I keep it? do I get more flexibility
  by not keeping it, or by putting a **transform layer** between how we need to think about it and how the
  driver thinks about it?* Broader search → more candidate answers → **more convinced** in the direction
  chosen: best-researched, not first-or-easiest. *(→ Principle P-2, P-4.)*
- **Share two instances of the same driver** — originally: him studying the code and **talking to Chip**.
  Now there's enough in the **p2kb** that the agent **already knows** how this can be done — it can
  automatically enumerate the techniques the P2 makes available (three or four). *(→ Principle P-3.)*
- **Absorb the requirements change (new motor type)** — *how does the underlying driver have to adapt to the
  new motors? how do the new motors control?* Researching that — reading the datasheets, **identifying the
  differences**, figuring out **which aspects affect our implementation** — is much easier and faster with an
  agent. *(→ Principle P-4.)*
- **Characterize the hardware** — the agent helps **decide how to range-test** a part and **which axes
  matter**. There are always many axes you could test; having the agent help pick the ones that actually
  teach you something, faster, is a genuinely useful technique. *(→ Principle P-4.)*
- **Add the observability display** — **second nature** for an agent. Once he **describes the channel and its
  freedoms** — the PLOT DEBUG interface (generate the graphics, then use the channel), or HDMI (adopt fonts,
  then say where things land on screen) — the agent is fully capable of doing all the work. Makes
  implementation of *any* observability display much quicker.
- **Produce documentation** — also second nature. The valuable human part is **identifying the audience and
  the voicing**: is this reader **returning** to a project they already deeply understand (a refresh), or is
  the concept **brand new** (teach the concepts before teaching the project)? Decide those, and the agent
  responds to those controls, reviews the result **from a pedagogical standpoint**, and produces genuinely
  beneficial documentation for humans.

### 2. P2-Click-eInk — ✅ captured *(pre-AI project; agent story is "how I'd do it now")*

**Per attention-item (agent lens):**
- **Locate source / documentation** — same as Project 1's domain research; nothing new. *(→ P-1.)*
- **Logic-analyzer bring-up** — the standout win. He *used to* keep a **handwritten journal**: which LA pins,
  which cable colors, mapped to where — a manual ledger verified by hand. With an agent he now **speaks the
  pin-up** (where the LA wires are, what color) and the agent **annotates the code** with all of it, so the
  code and its documentation stay together — no external journal, no drifting comments. Hookup is easier and
  *correct*. And when a capture **looks wrong**, he tells the agent what he's seeing and it **proposes why /
  what he did wrong / which connections to check** — the logic analyzer becomes a troubleshooting partner.
  Same for **scopes** and any external measuring gear. *(→ Principle P-5.)*
- **Scope the features** — ask the agent *what are the typical features this kind of thing has, if I want my
  driver most readily usable?* It surfaces the **range**; the **developer still decides which subset** to
  build. The agent is excellent at **implementing** them (knowing how to do rotations, buffering). Layered on
  top: **performance / architecture** — *where do I need performance on the P2? do I need LUT memory? PSRAM?
  CORDIC?* The user owns **why and where** performance is needed; the agent helps decide **how best to use P2
  resources** to meet it. *(→ Principle P-7; feature-implementation → P-4.)*
- **Portability across the family** — the rework story: bring up instance 1, then 2 shows what could be
  common, then 3 shows even more — rework every time. Let the agent **do the rework** *and* **identify in
  advance where rework will come from**: tell it the **family** you're considering and it researches and
  **proposes the breadth of interface early**, so additional instances don't force rework. *(→ Principle P-8.)*
- **Foreign-language docs** — unsure the agent itself translates, but the **web browser's translation** of a
  PDF is amazing; feed the **translated copy** to the agent to help understand what to do. A big, big win.
  *(Reinforces P-1: not everything is the agent — pair it with the right web utility.)*
- **Digest vendor code** — huge. First contact on new source: *what kinds of objects are in this repo — how
  many executables/programs?* For the important ones, **generate a theory of operations** (what/why/how),
  any language. Then **apply** those operations to what he wants, and **reuse techniques** from that source —
  translated to PNut/Spin2. The theory-of-operations is a **teaching document**: he can understand code he's
  **never looked at**, learn a huge amount without reading a line, because the agent did the research and
  produced the explanatory doc. Also **triage the codebase**: which pieces are usable, which are library,
  which are executable, which matter to *him*. Much faster. And the **study-a-group** move: ask it to study a
  group and it proposes how to handle the group + the best group APIs. *(→ Principles P-6, P-8.)*
- **Configurability** — the agent understands the **code shape** and **what needs to be configurable**. Two
  axes he names: **compile-time** configuration vs. **runtime** configuration. For adapting a display to a
  project the user identifies *which display* it is, plus **rotation** and the like. Once the driver is built
  and configurable, the agent helps **document how it's configured** and **choose the right technique**
  (runtime vs. static/compile-time). *(Mini-theme: compile-time-vs-runtime configurability — watch for
  recurrence before elevating to a principle.)*
### 3. P2-HUB75-Matrix-Driver — ✅ captured *(pre-AI project; agent story is "how I'd do it now")*

**Framing note (Stephen):** "not a lot more to say" on the electrical/PCB front this pass — the agent story
here is mostly about **bringing up new features** and taming the **complexity** that caused so much rework.

**Per attention-item (agent lens):**
- **Electrical / level-shifting at speed; custom PCB** — not specifically called out this pass (the standing
  research/datasheet-interpretation help applies).
- **Bring-up + features (the rotation trap)** — he's lost count of how often he thought **rotation** was one
  thing and had his eyes opened that it was actually a **two-tiered perspective**, or an artifact of **how he
  wired it** — causing repeated rework of very complex code. An agent tames that complexity **once you
  carefully describe the perspectives** and hold it inside them: *the set of panels is one display; the wiring
  entry point can be at a given location; the panel order on the single wire can vary.* Named those, the
  agent figures out the **wiring and the bit-ordering**. Tell it the panels **need initialization**, are
  **strung in a certain order**, and that **config constants describe that order**, and it knows how to send
  the **JTAG-equivalent chain** down to program them and how to do the **replication** — so it writes the code
  correctly. *(→ Principle P-9.)*
- **The research grind (per-panel-set)** — the agent **builds documentation for each panel set** and
  **extracts what's unique** to it, so he can correctly describe what's unique and how the driver must behave
  for that set. Adding a new set, it draws on **all previous sets**: knows how to coordinate, what's already
  enabled vs. missing in the driver. The uniqueness is **which controller chip** — the agent helps **find**
  the controller docs, **interpret** them, **map which driver features** this set needs, and understand its
  **timing needs**. New panel on the air in far less time; everything to configure it (chip docs, config
  examples) comes much quicker. *(→ Principles P-6, P-8-accretion.)*
- **Code sets / translation** — back to the **theory of operations**: one that captures **timing**, used as
  an **implementation guide** — by the agent itself — raises the **accuracy of the initial implementation**.
  Agentic output guiding agentic codegen matters. And a **changelog** of what changed each pass is now easy.
  *(→ Principles P-10, P-11.)*
- **Cataloging / documentation** — cataloging each board is the agent's now, and the **entire documentation
  repository stays correct** as long as he **guides the agent** on which docs do what, why, and which need
  updating when — part of a **skill set he uses with agents**. *(→ Principle P-11.)*
- **Performance-regression triage** *(added on the Project 6 turn — in progress now)* — a **user of an earlier
  version** reported the **newest version is *less* performant**; can the agent find why and fix it? The agent
  studies the **early shipping code**, contrasts it against the **new** code, **identifies the affected
  regions**, and **proposes the performance increase** to get the new codebase back to the old version's
  speed. Stephen is doing this with the LED-matrix code **right now**. *(→ Principle P-16.)*
### 4. P2-HUB75-Morphing_Digits — ✅ captured *(pre-AI project; agent story is "how I'd do it now")*

**Note:** Project 4's turn also produced the cross-chapter aside recorded as **Principle P-12** ("sufficient
guidance, not the perfect prompt") + its confirmed third arm (the p2kb MCP). Per-item agent lens below.

**Per attention-item (agent lens):**
- **Research the technique** — standing domain research (→ P-1); nothing new.
- **Code-generate the data** — so much easier with an agent. The agent **picks whatever language it likes**
  (probably Python, who knows); it already **knows how the digits are described**, so from "which digit is it
  going *to*" it reasons about the **segment transitions** needed to make the look **well-shaped**, and
  generates the table. *(A textbook agent strength; → P-4 executor + P-6 domain grounding.)*
- **Alternative animation techniques — where the fun is** — the standout. By hand, one transition set is so
  much work that he's **burned out** once **one** works, with no appetite for more. The agent would let him
  **do more** and **play with different techniques** — be **broader** because each aspect costs less time.
  That's the fun. *(→ Principle P-13.)*
- **Placement / composition; ship-demo-atop-driver** — not specifically called out ("not sure anything else
  is unique").
- **Documentation — video** — this is a **hardware video** (a real device moving), so **generative** video
  creation is unlikely to apply. But **emerging** agent video capabilities — **editing/shortening** the
  footage, **transcribing** the audio — could now help *produce* the video. Flagged as newer/advanced agentic
  capability just arriving.
### 5. P2-Magnetic-Imaging-Tile — ✅ captured *(post-AI — primary Act III material; same machine as the KB's streaming-pipeline derivation)*

**On record (confirmed, not disputed):** feasibility via the **p2kb MCP** (study board → **~1,300 fps**
practical rate) · **algorithm research** (frame delta + jitter → 8×8 to ~32×32 super-resolution) · **driver
comprehension** (Claude Code explained the **PSRAM** driver enough to adapt it).

**Added this pass (Stephen):**
- **Middle components built + tested in isolation** — when he builds something in the middle like the
  **FIFO**, he makes it a **standalone object** and uses AI to **generate the regression test**, confirming
  it works **before** putting it to work in the driver. So by the time these are in the whole application
  they're **tested components** — **no longer suspects** when something breaks. "A real important use of AI
  here." *(→ Principle P-14.)*
- **Performance revival against the improved KB** — on this project he **never got the OLED display running
  fully performant**. Since then the **p2kb has been improved**: better examples, and **fixed bugs** that had
  prevented getting **smart pins** working for the OLED. **Intent now:** go back **with the agent**, do a
  **full audit of the code against the current p2kb content**, identify where things can be adjusted, drive
  the **smart pins**, and get it running at **full speed** — *"I have no doubt."* *(→ Principle P-15.)*
- **Gaps not specifically AI-touched this pass:** the dual-simultaneous-output decision, the FIFO+decimation
  *design* reasoning (Act II), and the wiring/where-to-plug-in stayed human calls here.
### 6. P2-Multi-servo — ✅ captured *(post-AI mirror — the ceiling-lift headline)*

**On record (confirmed):** the **ceiling lifts** — with the agent he'd build a full **inverse-kinematics**
system + a **vision system** (locate → reach → place); the design out of personal (math) reach becomes
buildable.

**Added this pass (Stephen):**
- **Mechanical range-of-travel is a requirement *you* supply** — there are mechanical pieces the agent can't
  help with; your job is to give it what it can't see. Once a servo is **placed in a mechanism**, the
  mechanism may **limit its travel**. Tell the agent the **range of travel for every device** and it can
  **constrain overall movement** so the device **doesn't destroy itself** while you test and move it around.
  *(→ Principle P-18.)*
- **Model the indirection / reshape for a hardware change** — taking the **servo object** and moving it
  **behind a PWM-generation chip** (the servo object now speaks to the **PWM chip**, which in turn moves the
  servo), then **describing that move to the agent and letting it reshape the code**, is now **practical and
  feasible** thanks to the **p2kb**. Reshaping the project / **changing the hardware** — the agent gets it
  done quicker, so you're **back on the air** and continuing where you left off in far less time. *(→
  Principle P-19.)*
- **IK + coordinated motion** — yes, absolutely: do **inverse kinematics** and **coordinated** motor moves so
  the **whole arm reaches its target in the least time**, versus **serially** driving each servo's motion.
  *(→ ceiling-lift / P-17.)*
- **Center-of-gravity-aware motion** — with the agent's understanding of the **entire arm**, plan each move so
  the **center of gravity is least adversely impacted** and the arm **stays stable** — important learning
  that's **very hard without the agent understanding the math**. *(→ P-17 / ceiling-lift.)*
- **Fun via added sensors (amplification)** — once the arm moves well, the next thing he wants is to make it
  **go somewhere and *do* something** → **object identification** (a ping sensor, or for the most fun a
  **vision sensor with color + shape recognition**). The arm-motion complexity was **huge**; agentic coding
  made it **simple enough** that he can now **add sensors** and use them to **describe intent** — vision
  **locates** the object, **grab** it, **identify** where to put it, **go drop** it, vision **monitoring the
  gripper**. You can **go beyond the limits of the single object** by adding sensors — *"that's where the fun
  comes back in, and that's where your amplification comes in."* *(→ Principles P-17, P-13.)*
- **Requirements linkage (his callback to P-12)** — the human helps the agent by **providing requirements**,
  and the **servo range limits are exactly that**; so are **motion coordination/overlap** and **describing
  what you see in your mind's eye** for the agent to translate to code — *or* letting the agent **research the
  web** ("people do this; here are the techniques; which would you like to apply?"). **Surveying → finding
  approaches → choosing → switching** is itself a fun mechanism; it adds **research ability and playability**.
  "What used to take days, weeks, months can now be done in **days**." *(→ Principles P-12, P-2, P-13.)*
- **Characterize the servos = develop a test plan** — his reading of "characterize": **how do you test
  repeatability?** Then use the **achievable** repeatability as **guidance for moving** the servos; where
  repeatability **can't** be achieved, build algorithms that **stay within** what you can achieve. Deciding
  **how to test, what fixtures**, and **building the test code** — agents help, and you reach a **better
  solution** *because* you used agentic help. *(→ Principles P-14, P-18, P-4.)*
### 7. P2-OctoSerial — ✅ captured *(pre-AI; the 8-port serial/UART push-to-limits project)*

**Framing note (Stephen):** such a general **hardware-research / push-to-limits** project that there's **no
project-*specific* gain** beyond what's already been said — *not* that agents give little here (they give a
lot), just that this project surfaces nothing unique.

**Per attention-item (agent lens):**
- **Every general aspect applies** — identifying **and recording** the requirements; figuring out **how to
  hook up the logic analyzer** and **how to measure** the requirements; and the **certification code**: how
  to **certify a transmission is accurate**, how to **trap** that inaccuracies / communications failures are
  being caught, and **how much CRC** to cover the span of data being sent. All of it helps produce **better,
  more trusted test results**. *(→ Principles P-12, P-5, P-14, P-4 — nothing project-unique.)*
- **The agent guides the physical hookup** — the new nuance: the agent can help you **wire things up**.
  **Describe the rig** you want, the **range of pins**, and **how to set it up**, and it can **prompt you to
  wire it up** step by step (*"here's what you said you were going to do — let's do it now"*), **showing you
  what you need**. It can **create a document with the mapping** and **interactively walk you through** the
  hardware setup. *(→ Principle P-20.)*
### 8. P2-PCA9685-Servo-Driver — ✅ captured *(pre-AI; productize-for-reuse extracted from the arm)*

**Framing note (Stephen):** "not going to be much here that is new to this project" — the fresh angle is
**readying it for public reuse**.

**Per attention-item (agent lens):**
- **Recognize reusability → suggest OBEX publication** — as he describes the **hardware shape**, the agent
  can suggest these are **standalone pieces** he could provide to **OBEX** as a **reusable element**; it
  understands reusability and proposes it. *(→ Principle P-21.)*
- **Testing / a public-ready driver** — **exercise and provide regression tests** for the servos **through
  the hardware lashback**, making sure he has a **good driver ready for public use**. *(→ P-14.)*
- **Theory of operations** — create one for the driver. *(→ P-6.)*
- **Public documentation** — good docs, because he's **going public** with it. *(→ P-11.)*
- **Guide the wiring + coordination** — suggest **how to wire it up** and **how to coordinate** things.
  *(→ P-20.)*
- **Stand up multiple I/O chains** — suggest **how to stand up multiple I/O chains** of this kind. *(→ P-8.)*
- **KB-informed public docs** — the agent already has access (via the **p2kb**) to feasible P2 techniques;
  ask *"I'm making this object visible and external, sharing it — what aspects should we speak to in the
  documentation?"* and it **knows these are feasible ways to do things on the P2** and **adds them to the
  documentation**. *(→ Principles P-3, P-21.)*
### 9. P2-RoboDog — ✅ captured *(post-AI — control-plane derivation; on-record evidence confirmed)*

**On record (confirmed — Stephen: "covered pretty well, not going further"):** **reverse-engineering** the
undocumented system (example code + vendor docs) AI-assisted · **postulating the P2 decomposition and
building the layers** *with* the agent · **weeks-not-months** (a week or two vs. a month or two by hand).
Comms-selection (narrow I²C/SPI — the **AI-camera-over-I²C** swap), behavior-shaping, and expandability were
not separately elaborated this pass; the reverse-engineer/decompose/weeks-not-months story stands as the
capture. *(No new principles — reinforces P-6, the ceiling/reshape lens, and the diff-based family.)*
### 10. P2-RPi-ioT-Gateway — ✅ captured *(pre-AI; offload-vs-port — the research-light, expertise-rich pole)*

**Per attention-item (agent lens):**
- **Survey protocol styles + decide from stated needs** — many choices here ride on the user's **prior
  experience** vs. doing research (nothing wrong with that — capability always rests on experience). The agent
  can **survey different protocol styles** and say **why you might use one or not**. State your needs —
  **performance, reliability, store-and-forward** — and it proposes **the kind of code you'd need** and
  **candidate protocols**. State needs for **instrumentability / visibility** into what the protocol is
  doing, and it offers options: **build a decoder** to understand it, or **transfer text and dump it** so you
  can see what the protocol is doing. Genuinely useful when doing something **new**. *(→ P-4, P-2, P-12.)*
- **Amplify what you know — don't abandon it** — you **don't have to leave your comfort zone** or stop doing
  what you're familiar with. The idea is to **have fun**, so **don't abandon your own knowledge** just to do
  things with agents — **amplify what you know** and have more fun. *(→ P-17 facet.)*
- **Onboard a newcomer to the Raspberry Pi / Linux** — a lot of the **configuration and setup** is unique to
  Linux. Stephen has **tens of years** of Linux experience, but someone **new** to Linux/Pi would struggle
  to decide **which packages** to install and how to configure them to **stand up a web server**, **get
  high-precision internet time**, and **talk to external APIs**. The agent helps a new user understand **what
  facilities are available**, **why you'd choose each**, then **installs the pieces they choose** — meaningful
  when you've **never been on a platform**, or **haven't been on it in a long time** and need reminding.
  *(→ Principle P-22.)*
### 11. P2-VL53L5CX-tof — ✅ captured *(post-AI — the stalled-project revival; on-record confirmed)*

**On record (confirmed — "covered really well"):** **diff-and-surgically-port** vendor updates — take the
original source, **diff** the new release, apply just the meaningful changes, pull the binaries, run —
**days-not-weeks**; the stalled project is **revivable** and he's **encouraged to finish it**.

**Added this pass (Stephen):**
- **Direction is set** — bring it forward to the **latest release** over **I²C**, **add the math** in place,
  and **identify further performance** wins; all necessary and **on the books**. *"Too much fun a sensor to
  not use it."*
- **Reuse-by-composition** — once the driver/object exists, incorporating it at the device means he could
  drop a **180° field-of-view sensor onto the dog** at will. With the object **pre-tested**, **exported**,
  carrying a **theory of operations**, and **logic-analyzer-proven communications**, he has a **reusable
  element** — a very complex but **high-speed** sensor — and putting it on a **moving vehicle** is a
  **no-brainer**. **Keeping it up to date** is near-no-brainer too, because the agent keeps the code current.
  *(→ P-14 tested-component, P-21 export/reuse, P-6 theory-of-ops, P-15/P-16 keep-current, P-17
  compose-onto-the-dog — the ToF object dropping into #9 RoboDog.)*
- **Aside this turn → Principle P-23** (mobile control-panel app + BLE bridge in reach).
### 12. P2-Voice-Sensor — ✅ captured *(post-AI; two agents in play; on-record confirmed)*

**On record (confirmed — "covered so well, nothing to add"):** device/market research via **Perplexity**
(price point **$50–100**); **Claude Code** read the datasheets + helped write the tests. **Two different
agents** — reinforces **P-1**.

**Generalization added this pass (Stephen):** the **market-research technique** — **market research,
price-point finding, ease of communication** — applies across **nearly every** sensor/actuator choice; it's
a **very common** thing to do market research and identify the parts you'll use. **Agentic help is immense:**
**coming down to an answer**, **finding examples** of how to use it, **finding YouTube videos** of how to use
it — all amplified, so the **search duration from *intent* to *chosen product* is so much shorter**.
*(→ Principle P-24.)*
