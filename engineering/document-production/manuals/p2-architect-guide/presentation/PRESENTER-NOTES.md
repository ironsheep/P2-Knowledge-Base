# Thinking in P2: Functional Decomposition — Presenter Notes

*Talk track for each slide, listified for quick scanning. Generated from the deck.*

## Slide 1 — Thinking in P2: Functional Decomposition

*On screen:* The P2 Architect's Guide  •  Part II  •  just released v1.0.0

**OPENING (≈60s)**

- Welcome.
- Last night we shipped the P2 Architect's Guide, v1.0.0.
- Tonight I want to give you the heart of it — not the whole book, but its center: how you decide what goes on which cog in the first place.
- The book has three parts — getting a project off the ground, thinking in P2 (decomposition), and doing that same work with an AI agent.
- I'll set up Part I in one slide, spend our time in Part II, then open the floor — because a lot of you have decomposed real P2 designs, and I want those experiences to feed back into this document.
- Plan: ~12 minutes, then questions, then let's compare notes.

## Slide 2 — First: Getting a Project Off the Ground (Part I)

*On screen:* Four phases before any cog is assigned: · Decide what to build — feasibility, parts, pins, what the P2 should NOT do · Learn the hardware — datasheets, level shifters, the logic analyzer · Build the capability — interface design, translation, performance, characterize · Finish & ship — document, post, announce · Output handed to Part II: a wired-up app with a pin map, parts that talk, · and a feel for their rates and deadlines — the material we carve around · Not one cog is assigned yet. That is the point.

**PART I SETUP (≈90s)**

- Before you can ask Part II's question — which cog owns what? — there's a whole front end every real project makes you do.
- Deciding what to build (and often the biggest call: what the P2 shouldn't do at all — pair it with a Pi for the web stack rather than porting one).
- Learning the hardware — chasing datasheets, adding level shifters for 5V parts, and leaning on the logic analyzer as the court of final appeal.
- Building the capability — designing an interface someone can actually think in, translating reference drivers into Spin2, chasing performance, characterizing the real behavior (those measurements BECOME your product's spec).
- And finishing: document, post, announce — skip any of the three and you wasted the work.
- The key handoff: by the end of Part I you have parts that talk, a pin map, and a feel for the rates and deadlines — but NOT ONE COG assigned.
- That's exactly the raw material Part II works on.
- Tonight we're in Part II.

## Slide 3 — The Big Idea: Computing in Space, Not Just in Time

*On screen:* A conventional MCU computes in TIME — one instruction stream, go faster · An FPGA computes in SPACE — function laid out as parallel hardware · The P2 sits between them: a coarse-grained spatial fabric · 8 deterministic cogs + 64 smart pins you assign function to · Decompose WELL → parallel pipelines; throughput set by data RATE · Decompose BADLY → the same silicon collapses to one cog doing everything, · the other seven idle · Decomposition is how you keep the design on the spatial side of that line

**CHAPTER 5 (≈90s)**

- Here's the idea that makes the rest worth the effort.
- There are two ways a chip can compute.
- A normal microcontroller computes in TIME: one core, one instruction stream, and it does more by going faster or time-slicing.
- An FPGA is the opposite pole — it computes in SPACE: function laid out as actual parallel hardware, no single instruction stream.
- The P2 lives between them, closer to the spatial side than you'd expect — eight independent deterministic cogs and sixty-four smart pins form a coarse-grained spatial fabric.
- Here's the payoff and the warning in one: decomposed well, a P2 design behaves like spatial hardware — parallel pipelines whose throughput is set by the RATE data flows, not by how many instructions any one stage runs.
- Decomposed badly, the very same silicon collapses back into a slow sequential machine — one cog doing everything in turn while the other seven idle.
- That sentence is why this whole part exists.
- For P1 folks: you've been thinking this way all along — dedicate a cog, let it run.
- What the P2 changes is how MUCH fabric you have to spread onto.

## Slide 4 — Computing in Time vs. in Space

**FIGURE (show while covering the previous slide)**

- The spectrum: a single-core MCU at the TIME pole (one instruction stream), an FPGA at the SPACE pole (function as parallel hardware), and the Propeller 2 sitting between them as a coarse-grained spatial fabric — 8 cogs + 64 smart pins you assign function to.
- Leave this up while you deliver the decompose-well / decompose-badly point.
- You can merge this into the previous slide in Keynote if you'd rather have one slide.

## Slide 5 — Object Shape Is DERIVED, Not Chosen

*On screen:* On the P2, your object set is not a style picked from a menu — it's derived · Change the buses, deadlines, or data rates → the correct object set changes · Vocabulary vs. grammar: · Objects (driver, policy, buffer, coordinator…) are the NOUNS · The forces are the GRAMMAR — which nouns, how many, where the seams fall · Two axes, co-designed: · Logical — cohesion & coupling (decades of solid theory) · Physical — allocation onto a finite, heterogeneous lattice · A smart pin can DELETE large amounts of code by absorbing the work into hardware

**CHAPTER 6 (≈90s)**

- The central move of the whole part, stated plainly: on the P2 the shape of your object set is NOT a matter of taste picked from a menu.
- It's derived by reconciling a small number of physical and architectural forces.
- Change the buses, the deadlines, or the data rates and the correct object set changes with them.
- Why care?
- Because if decompositions were chosen by taste, the best you could do is collect examples and imitate the nearest one.
- Because they're DERIVED, you can learn the forces and produce a sound design for an app you've never seen.
- Separate two things: the OBJECTS — top-level app, device driver, semantic driver, policy layer, buffer, coordinator — are your vocabulary, the nouns.
- The FORCES are the grammar: the rules that decide which nouns, how many, and where the boundaries fall.
- Tonight is about the grammar.
- And the P2 adds a second axis classical software design doesn't have: a physical one — allocation onto eight cogs, sixty-four smart pins, one CORDIC, sixteen locks, bounded hub bandwidth.
- That physical axis isn't only a constraint, it's a design TOOL: a cog is the strongest encapsulation the silicon offers, and a smart pin can delete large amounts of code.
- 'Where's the boundary' and 'what hardware runs it' are ONE decision.

## Slide 6 — The Four Forces That Do the Cutting

*On screen:* Three PRIMARY forces cut horizontally — who owns what, how pieces relate: · Force 1 — Who owns this wire?   (correctness) · Force 2 — What does each seam promise?   (contracts) · Force 3 — Where do two cadences meet?   (rate adapters) · One EMERGENT force falls out vertically once the first three draw the structure: · Force 4 — How high does each piece sit?   (layering) · Lead with the QUESTION each force asks — that's what you carry away · For each force, the WHY matters more than the what

**CHAPTER 7 INTRO (≈60s)**

- Four forces do the work.
- Three are PRIMARY — they cut the object set horizontally, deciding who owns what and how the pieces relate.
- The fourth is EMERGENT: it falls out vertically once the first three have drawn the structure.
- I'll lead each with the QUESTION it asks, because that question — asked of your OWN application — is the technique you take home.
- And for each one, the WHY matters more than the what: an engineer who knows why a force exists on the P2 will generalize it to hardware we never imagined; one who memorizes a rule eventually meets the case the rule didn't cover and applies it wrongly.
- So we'll dwell on reasons.
- The examples — a robot dog, some I2C buses — are a force in motion, never a rule to transplant.

## Slide 7 — Force 1 — Who Owns This Wire?

*On screen:* A CORRECTNESS question — the only force that makes you flatly wrong, so it's first · For each serialized, stateful resource (an I²C bus, a one-wire chain): · exactly ONE owning cog. The boundary traces the WIRE, not your feature list · Why: P2 pin outputs are OR'd — there is no hardware referee · Two cogs on one bus = guaranteed corruption, not 'a race you might lose' · A lock coordinates shared DATA; it can't un-corrupt a half-issued I²C frame · The failure it prevents: the flat device list — every chip gets a sibling driver · One owner, several shapes: many callers / broker cog / replicated bus

**FORCE 1 (≈90s)**

- The first force asks a correctness question, not a style one.
- Of the four it's the only one that can make your program flatly WRONG rather than just inelegant — so it goes first.
- The question: for each serialized, stateful hardware resource — an I2C bus, a one-wire LED chain, a smart pin mid-transaction — which single cog owns it?
- The answer the force insists on: exactly one.
- One owner per resource, and the object boundary traces the WIRE, not your feature list.
- Why?
- It's physical.
- P2 pin outputs are OR'd together — there's no hardware referee arbitrating who drives the pin.
- If two cogs both drive SDA and SCL, they don't take polite turns; the outputs combine and the transaction corrupts.
- This isn't a race you might lose — a stateful protocol with two uncoordinated drivers is GUARANTEED to break.
- The chip gives you sixteen locks for shared DATA, but a lock can't un-corrupt a half-issued frame.
- The clean fix is structural: make the resource unshareable by giving it one owning object in one cog.
- The failure this prevents is the FLAT DEVICE LIST — every chip gets a driver, every driver a sibling off main().
- The moment two cogs touch one bus you get silent, intermittent corruption that presents as flaky hardware, three layers from its cause.
- Note: one owner is the RULE; a single shared code image is just its cheapest ENCODING when there's one bus.
- Two identical buses?
- Give each its own state; keep one writer per bus.

## Slide 8 — Force 2 — What Does Each Seam Promise?

*On screen:* Where two cogs meet, the 'contract' names the dependency — and draws the boundary · blocking call • latest-wins mailbox • ring buffer • published telemetry • fan-out · Stance: read a sensor continuously & publish its latest value — never on demand · Every seam is really THREE planes, ranked by cost of getting them wrong: · Data plane → waste bandwidth (visible, recoverable) · Control plane → corrupt state (an intermittent race) · Event plane → miss a deadline (silent until the field) · Discipline: write the payload first, bump the signalling counter LAST (atomic long)

**FORCE 2 (≈90s)**

- Once Force 1 scatters work across cogs, they have to exchange data.
- Force 2 asks: at each seam where two cogs meet, what does the exchange PROMISE?
- Does the sender wait?
- Does the receiver see the freshest value or every value?
- That promise is the CONTRACT, and choosing it IS a decomposition decision — the coupling you can tolerate decides where the boundary goes.
- Menu: a blocking call (tight coupling, caller waits on worst-case latency); a latest-wins mailbox (producer never waits, consumer always reads newest); a ring buffer (decouples rates, keeps every sample); published telemetry (one writer, many lockless readers); fan-out publication (one producer, many consumers, bulk frames).
- A design STANCE hides in the mailbox: for a sensor, read it continuously and publish its latest value — never reach out and read it at the moment you need it, because that couples your fast loop to the sensor's conversion latency.
- Now the sharpener: every seam is really THREE relationships superimposed, and I've ranked them by the cost of getting them wrong.
- Data plane — bulk movement; get it wrong, waste bandwidth, visible and recoverable.
- Control plane — commands and state; get it wrong, corrupt state, an intermittent race.
- Event plane — signalling and urgency; get it wrong, miss a deadline, and THAT one stays silent until the field.
- You spend design care in inverse order.
- The classic P2 abuse is building all three planes on one mechanism — polling a hub flag to deliver an urgent event.
- One discipline to memorize: publish-last — write the payload, bump the counter last; a single-long write is atomic, so a reader watching the counter can never catch a torn value.
- Costs nothing, removes a whole class of glitch.

## Slide 9 — Force 3 — Where Do Two Cadences Meet?

*On screen:* The one a beginner most often misses — it corresponds to no chip, no parts-line item · Devices live in different time domains: WS2812 (ns), servos (50 Hz), battery (1 Hz)… · Whenever data crosses a cadence boundary, something must adapt the rate → an object · A software clock-domain crossing — glitches if you don't handle it on purpose · Two adapters fall out: · Sampler / buffer — fast producer, slow consumer (every sample? or freshest?) · Slew / easing engine — a discrete 'walk' step → a smooth servo trajectory · Collides with Force 1: one bus, many cadences → cooperative tasks in the owner cog

**FORCE 3 (≈90s)**

- This is the force a beginner's instinct most often misses, because it corresponds to nothing you can point at — no chip, no line in a parts list.
- Devices live in different TIME DOMAINS.
- An LED chain wants nanosecond bit timing; servos want a smooth 50 Hz; a voice recognizer is polled lazily and stretches the clock; a battery reading matters about once a second; an ultrasonic echo happens when it happens.
- Force 3 asks: where does data cross from one cadence to another, and what has to sit at that crossing to reconcile the rates?
- Because whenever data crosses a cadence boundary, SOMETHING must adapt the rate — and that adapter is a distinct responsibility, so it's a distinct object.
- The P2 encourages putting different time domains on different cogs and pins — that's what they're for — but the instant you do, you've built the software equivalent of a clock-domain crossing, and like its hardware namesake it glitches if you don't handle it on purpose.
- Two adapters fall out.
- A SAMPLER or buffer, where a fast producer meets a slow consumer — and the whole design is one question about the consumer: every sample (a buffer) or only the freshest (a latest-wins slot)?
- And a SLEW or easing engine, where a discrete intent becomes a continuous stream — 'walk' arrives once, but a servo can't take a step; it needs a smooth ramp at its own frame rate.
- Pull the ramp out of both the policy and the driver and both stay clean.
- Best part: this COLLIDES with Force 1.
- Several devices share one bus but want different cadences — Force 1 forbids splitting the bus across cogs, Force 3 says separate the cadences.
- Neither wins by cutting.
- The answer is cooperative tasks WITHIN the one owning cog, each at its own cadence, yielding at transaction boundaries.
- You only find that by holding two forces in tension.

## Slide 10 — Force 4 — How High Does Each Piece Sit?

*On screen:* The emergent, VERTICAL consequence — answers 'how much code goes in one object?' · Not a line count. Split where the UNIT changes, or the axis of change changes · The canonical stack: bits on a wire → registers → physical units → behavior · each tier = one unit conversion, changes for exactly one reason · Underneath: Parnas's information hiding — decompose around what changes independently · Hard P2 limit: cog RAM is tiny (512 longs; 496 usable) — layering isn't free · Fold adjacent tiers when memory is tight — but SAY SO; never fold across reasons · Prevents the 'driver' that mixes register pokes with behavior logic

**FORCE 4 (≈90s)**

- The first three forces are horizontal — who owns what, how they talk.
- The fourth is the VERTICAL consequence that falls out once they've drawn the structure, which is why it's emergent, not primary.
- It answers the question every programmer eventually asks: how much code goes in one object?
- The honest answer is NOT a line count and not a component count.
- It's: split where the unit changes, or where the axis of change changes.
- Stack the objects so each tier does exactly one unit conversion and changes for exactly one reason.
- The canonical stack climbs from bits on a wire, to device registers, to physical units — millimeters, degrees, millivolts — to behavior.
- Each tier speaks a different unit than the one below, and that change of unit IS the seam.
- The principle underneath is old and durable: Parnas's information hiding — decompose around the things that change independently, not around processing steps.
- Two pieces that always change together for the same reason belong in one object; two that change for different reasons — a new chip vs a new behavior — belong apart, even in the same call chain.
- On the P2 this negotiates against a hard limit: cog-local memory is TINY — 512 longs, 496 usable.
- Unlimited layering isn't free; each tier costs a call and a little state.
- So default to one tier per unit conversion, with an explicit escape: when a cog is genuinely tight, fold two adjacent tiers — but SAY SO, and never fold two tiers that change for different reasons just to save space, because that quietly rebuilds the monolith.
- The failure it prevents: a 'driver' that mixes register pokes with behavior, so swapping the IMU chip forces you to re-test the walk cycle.
- And a word on reconciling: the real skill isn't applying each force, it's reconciling them — they pull against each other.
- Hold them together, let them argue, and let the hardware and the hardest deadline win.

## Slide 11 — Completing & Judging the Cut

*On screen:* The forces build a tree; some objects live ACROSS it — name them or they smear: · safety override • external-interface translator • config store • test seams • lifecycle sequencer · Keep a RESOURCE BUDGET as you derive — a blank row is a resource you forgot · 'Running out of cogs' = the design is too COUPLED. Re-cut, don't cram · Every cog needs a one-sentence reason: determinism / ownership / blocking I/O / throughput · Judge the cut — four tools of increasing sharpness: · coupling (countable longs) → change-coupling → back-pressure (min-cut) → observability · A decomposition is REVISABLE — expect to dial it in against real silicon

**CHAPTER 8 (≈100s)**

- The four forces build a clean tree — but a real app needs objects that don't live IN the tree, they live ACROSS it.
- Five recur: a safety override (a privileged supervisor above policy — low-battery cutoff, e-stop); an external-interface translator (quarantine a vendor's vocabulary behind one seam); a configuration store (per-unit trim and pin maps in DATA, so identical firmware runs on every board); testability seams (each object exercised standalone on real hardware — the seam you can test at is the seam you should cut at); and a lifecycle sequencer (power before buses, chip awake before you actuate it).
- These have to be EXPLICIT on the P2 because cogs are independent — a hung cog won't stop driving its pins, and init order isn't implied by your call structure.
- Place them AFTER the tree is drawn.
- Next, keep a RESOURCE BUDGET as you derive — an allocation table, not a report you write afterward.
- Eight cogs, sixty-four pins, sixteen locks, one CORDIC, bounded hub bandwidth, 512 longs per cog.
- The budget earns its keep with one sharp signal: 'running out of cogs' is the P2's concrete way of telling you the design is too COUPLED — so re-cut, don't cram.
- And a check before you run out: every cog you assign needs a one-sentence reason from a short list — determinism, resource ownership, blocking I/O, or throughput.
- Can't say it?
- Fold it in.
- Finally, JUDGING — turning 'that seems cleaner' into something checkable.
- Four tools, increasing sharpness: coupling as a countable integer (count the longs that cross a boundary); change-coupling, the sharpest — what must CHANGE together (the dangerous case is dynamic change-coupling crossing a cog boundary, which the hardware expresses as jitter and races); back-pressure as a min-cut (draw the boundary where the least, weakest coupling crosses the cheapest channel); and observability — can you WATCH it run?
- On the P2 that's nearly free: aim a separate cog at a lock-free seam and observe WITHOUT perturbing.
- Last honesty: a decomposition isn't right just because you balanced the forces carefully once.
- It's a hypothesis; building the thing tests it.
- Expect to dial it in — that's the method working.

## Slide 12 — The Method in Action — First-Contact Procedure

*On screen:* Deliberately inverts top-down: start from the hardware edge & the timing, not the data model · 1. Enumerate the wires  (always) · 2. Triage against smart pins — a pin can DELETE large amounts of code  (skip if no pin mode fits) · 3. Assign owners — one cog, one transport per bus group  (always) · 4. List the cadences   5. Resolve same-bus rate conflicts · 6. Draw the seams (per plane)   7. Layer each branch (one tier per unit) · 8. Place the cross-cutting objects   9. Reconcile against budget & deadline  (always) · The procedure is FRACTAL — run it again inside a cog that owns a bus

**CHAPTER 9 PROCEDURE (≈60s)**

- We have the forces, the cross-cutting objects, the budget, and the judging tools.
- The last thing you need is the ORDER to apply them — because the forces are orthogonal but the work isn't; you can't pick a seam's contract before you know where the cog boundaries are.
- The procedure deliberately INVERTS the classic top-down approach: you don't start from the data model, you start from the hardware edge and the timing budget and let the structure fall out.
- Nine steps — the spine steps always run, the others tell you when you can skip.
- Enumerate the wires.
- Triage against the smart pins — this is the physical axis used as a tool, a pin DELETES large amounts of code.
- Assign owners, one cog and one transport per bus group.
- List the cadences; resolve same-bus rate conflicts with cooperative tasks.
- Draw the seams per plane.
- Layer each branch, one tier per unit conversion.
- Place the cross-cutting objects — and name the ones you don't need.
- Reconcile against the budget and the hardest deadline.
- One more property: it's FRACTAL — after the top-level pass, run the very same routine INSIDE a cog that owns a bus; it has its own cadences, seams, and layers.
- When you're done you hold two things: the object-and-cog set, and the budget that proves it fits.
- Judge it with the four tools before you write a line.

## Slide 13 — Watch It Run: A Walking Robot

*On screen:* Input is ONLY the hardware — nothing about the objects is given: · I²C bus 1: 13 servos + IMU + battery ADC, behind a ~50 Hz motion deadline · I²C bus 2: one voice module that clock-stretches, polled slowly · 3 discretes: WS2812 chain, buzzer, ultrasonic ping/echo — smart pins carry the timing · The object set FALLS OUT: 3 cogs (orchestrator / body-control / I/O), ~8 smart pins, · 0 locks (single-writer atomic telemetry). It fits, with cogs to spare — a min-cut · Same protocol (I²C) lands on two cogs with two transport shapes — topology decided it · CARRY THE METHOD, NEVER THE MAP — a second app (streaming) gives a different answer

**CHAPTER 9 EXAMPLE (≈100s)**

- Let's watch the whole method run once, end to end, on a small walking robot — a quadruped dog.
- The one thing that matters most: this is ONE application's answer, shown to make the method visible — it is NOT a template.
- Read for the moves, never the result.
- The only input is the hardware: I2C bus 1 carries thirteen servos through a PWM chip, plus an IMU and a battery ADC, all behind a hard ~50 Hz motion deadline.
- I2C bus 2 carries one voice module that clock-stretches and is polled slowly.
- And three discrete signals — an addressable LED chain, a buzzer, an ultrasonic ping-and-echo.
- Nothing about the objects is given; we derive them.
- Triage: the three discretes each map onto a smart-pin mode that carries the timing, so no cog bit-bangs them — and because the pins carry the jitter, all three collapse onto ONE non-blocking I/O cog.
- The two I2C buses are multi-byte stateful protocols — no smart pin can own I2C — so they need software owners.
- Bus 1's three devices sit behind one body-control cog with a single shared transport.
- Bus 1 serves three cadences — servos 50, IMU 100, battery 1 Hz — so three cooperative tasks inside that one cog.
- Seams: a latest-wins command mailbox (publish-last), lock-free published telemetry, event-plane freshness counters — nothing blocks.
- The motion branch layers into four tiers by unit conversion: PWM register driver, servo pulse/channel, leg inverse-kinematics, gait policy.
- Cross-cutting: a critical-battery hard-halt above policy, a voice-vocabulary translator at the edge, a per-joint trim store, per-layer bring-up tests, and the orchestrator owning launch order.
- Reconcile: three cogs of eight, about eight smart pins, ZERO locks — it fits with cogs to spare, and it's a min-cut.
- Notice what happened: we never started from a parts list and grabbed a template.
- We started from the wires and the timing, ran the forces in order, and the object set fell out — including the same protocol (I2C) on two cogs with two different state models, decided purely by sharing topology.
- The book runs a SECOND app — a fast image sensor streaming to two displays — through the identical nine steps and gets a totally different answer: a genuine FIFO pipeline, a decimator that sets the rate, and hub BANDWIDTH as the binding budget instead of cogs.
- Same method, different map.
- That's the whole claim in one line: carry the method, never the map.

## Slide 14 — The Walking Robot: Object-and-Cog Map

**FIGURE (the visual payoff of the robot derivation)**

- This is the object set the nine steps PRODUCED — not a template.
- Walk it left to right: the orchestrator/sequencer up top owns launch order and the safety supervisor; COG A (body-control) owns I2C bus 1 with its four-tier stack — gait policy, leg IK, servo semantics, PWM register driver — plus the per-unit trim store hanging off it; COG B (I/O cog) non-blocking-multiplexes the discretes and the voice bus.
- The labeled arrows are the seams by plane — CONTROL, DATA, EVENT.
- Point out: three cogs of eight, zero locks, and the SAME protocol (I2C) on two cogs with two transport shapes.
- Read it for the moves, not the result.

## Slide 15 — A Second Application, a Different Answer

**FIGURE (the strongest evidence: same method, different map)**

- Run the SAME nine steps on a fast image sensor streaming to two displays and you get something the robot never showed: a genuine FIFO pipeline.
- The tile sensor pours ~1,300 fps into a capture FIFO; a single DECIMATOR sets the rate — plain decimation or delta-compositing, lifting 8x8 toward 32x32 — then fans out through a FIFO per display to OLED and HDMI at ~60 fps.
- Three things differ from the robot: the producer gets its own cog for DETERMINISM (not bus ownership); the rate adapter is a pipeline, not in-cog cooperative tasks; and the binding budget is HUB BANDWIDTH, not cogs.
- None of the robot's boundaries carried over — the PROCEDURE did.
- That is the whole claim in one line: carry the method, never the map.

## Slide 16 — Questions

*On screen:* Ask me anything on: · Computing in space vs. time — and where the P2 really sits · Any of the four forces — ownership, seams, cadences, layering · The resource budget and the four judging tools · The walking-robot derivation — or the streaming-pipeline contrast · The full treatment (plus appendices & glossary) is in the released Guide

**QUESTIONS (open-ended)**

- Take questions here.
- Likely ones and short answers: — 'Isn't three cogs wasteful when I have eight?' A healthy design ships with a cog or two in reserve; each cog in use should carry its one forcing sentence.
- Reserve beats reflexively filling all eight. — 'When do I use a lock vs. atomic publish?' Locks coordinate shared DATA; for a single-writer/many-reader telemetry hand-off you often need NO lock — publish-last on an atomic long. — 'What if a smart pin COULD do it but bit-banging is faster?' That's a signature to check, not a verdict — override it if you must, but record why and what would reverse the decision (the streaming example's OLED is exactly this). — 'How do I know my cut is good?' Run the four tools — and remember a decomposition is revisable; you dial it in against real silicon.
- If a question goes deep, point them to the released Guide — the appendices cover the FPGA borrowing and the decomposition literature.

## Slide 17 — Let's Discuss — Your Decomposition Experiences

*On screen:* I'd love to hear how YOU decompose P2 designs — let's compare notes: · How do YOU decide what goes on which cog? What's your first move? · A decomposition that FOUGHT you — what did you have to re-cut, and why? · Does the 'derived, not chosen' framing match how it actually feels? · Anything that guides YOUR decomposition we haven't named — a force we missed? · And if an example really fits the book's approach, it might inform a future edition — credited

**DISCUSSION (the real payoff — keep it going as long as it's live)**

- This is why I wanted to present tonight rather than just post the book.
- The Guide's method is derived from a dozen real projects, but many of YOU have decomposed P2 designs I've never seen — and I'd love to learn from that experience tonight.
- Prompts to get us going: How do you decide what goes on which cog — what's your very first move on a new hardware mix?
- Where have you run out of cogs, and looking back, was it genuinely at capacity or was it too-coupled in disguise?
- Tell me about a decomposition that FOUGHT you — the seam that looked clean on paper and turned awkward in code, the cut you had to redraw.
- Any case where a smart pin let you delete large amounts of code you'd otherwise have spent a cog on.
- And where a blocking call between cogs quietly serialized something that was meant to run in parallel.
- Big-picture: does 'object shape is derived, not chosen' match how it actually feels when you design, or does it feel more like taste to you?
- And the one I care about most: is there anything that guides your decomposition we haven't named tonight — a force we missed?
- Be honest — pushback makes the next edition better.
- I'll capture the strong examples; and if any really fit the book's approach, then with your permission they might inform a future edition, credited to you.
- Thank you — who wants to start?

