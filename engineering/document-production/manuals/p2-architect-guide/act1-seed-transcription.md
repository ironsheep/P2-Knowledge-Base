# Act I Seed — The Project Process (transcription capture)

**Status:** ACTIVE CAPTURE — started 2026-07-04. Raw dictation from Stephen + light structuring.
This is the seed for **Act I** (the universal engineering process, agent-agnostic) and — mirrored
item-for-item — the spine for **Act III** (how an AI helps with each of the same things).
Not chapter prose yet; content first, chapter breakdown falls out later (Stephen's method).

> **Framing (Stephen, 2026-07-04).** Act I is framed *for the reader* as a **real project you're building
> to ship** — a commercial product, a contracted job, or a formal project you'll sell; any given reader's
> project is "always some blend of these." Act I is the collection of **things you had to do to get a project
> built** — everything that happens *before* the functional decomposition of Act II. Act III revisits
> **this exact list** and asks, for each item, *how does AI help me do it?*

> **Preface — the kind of engineer this material comes from (Stephen, 2026-07-04).** This suite of projects
> represents a **different kind of engineer** from one who builds a single product and ships it for sale.
> Stephen's engineering is **interest-based**: he picks up something he's interested in — or is asked to do —
> and researches and builds it *to see how the P2 applies to that project and that hardware*. So the source
> material below is exploratory, curiosity-/request-driven work, not ship-for-sale product development.
> **Implication for Act I:** the *concerns* are the same ones any shipping project faces (that's why the
> reader-facing frame above still holds), but they were surfaced through exploration rather than a
> commercial mandate. Keep the reader frame ("a project you'll ship") while honoring that the lived
> experience feeding it was interest-based. `[reconcile these two lenses when authoring Act I]`

> **Capture discipline.** Faithful to Stephen's facts/decisions/experience — nothing invented. Per-project
> raw material below; the recurring **concerns** (the Act I spine) are lifted out as they emerge. Anything
> that's really an Act II decomposition decision is flagged, not folded in. `[?]` = circle back.

---

## The emerging spine — things done *before* decomposition
*(The concern list. Each becomes an Act I topic and an Act III "how AI helps" counterpart.
**Process (Stephen 2026-07-04): capture ALL 12 projects first, then do the common-element analysis.**
Rows A–K below are a head-start seeded from Project 1 only; the real consolidation across all 12 —
merging duplicates, settling granularity, ordering — happens AFTER capture is complete.)*

| # | Concern (the thing I had to do) | Surfaced by (project) | Act II? | Notes |
|---|---------------------------------|-----------------------|---------|-------|
| A | Adopt & understand technology you didn't write (someone else's driver / IP) | BLDC | — | inherited Chip Gracey's BLDC control tech |
| B | Research the problem domain & its user communities (who uses it, how they think about it) | BLDC | — | how motor/servo communities control motors |
| C | Design a unifying, background-agnostic **interface** before implementing | BLDC | — | "first effort"; approachable from any motor/servo style |
| D | Layer higher-level **convenience abstractions** over the primitives | BLDC | — | 2WD + steering hides "two separate motors" |
| E | Adapt the new interface onto the **existing driver** + implement control | BLDC | partial | the bridge/impl work |
| F | Support **multiple instances of one driver** (sharing / replication) | BLDC | ⚠ Act II | two instances of the same motor driver — ties to shared-bus-replication |
| G | Absorb a **requirements change / new hardware variant** mid-project | BLDC | — | request to support a different motor type |
| H | **Characterize hardware empirically** → turn findings into features & limits | BLDC | — | wheels vs motor rpm vs battery sizes → became features |
| I | Build **development-time observability** (a live status display) | BLDC | — | HDMI live per-wheel motor status while developing |
| J | Select a **display** + rendering / font techniques | BLDC | — | find usable HDMI display + font/draw techniques (may merge with I; recurs on display projects) |
| K | Produce **documentation** as a deliverable | BLDC | — | lots of writing, tool-assisted → strong Act III mirror |

---

## Projects — raw capture
*(One block per project as dictated: what it was, what I found out, what I had to do, the decisions I
made, the things I had to deal with — all pre-decomposition. Roster captured 2026-07-04; ⬜ = awaiting
dictation, ✅ = captured.)*

### 1. P2-BLDC-MotorControl — ✅ captured
**What it was:** Chip Gracey (the P2's designer) had developed some amazing control technology for
BLDC motors. Stephen was asked to take that project and **make it more amenable for use by the
general P2 community**. The target was also a robot — a two-wheel-drive platform.

**What I found out / had to research:** how servos and motors are actually used — finding the
different communities that use motors and learning *how each of them thinks about controlling them*.

**What I had to do (pre-decomposition), in order:**
- **Find & design a unifying interface** *(the first effort)*. Unify everything found into a single,
  broad motor-control interface — one you can come to experienced with *any* motor or servo style and
  still know how to use.
- **Layer for ease of use.** A higher layer so a two-wheel-drive system (steering and the like) is
  common and easy — without the user having to think about controlling two separate motors. → concern **D**
- **Implement the adaptation + control** *(the second effort)*. Adapt the new interface onto Chip's
  existing driver and implement the control. → concern **E**
- **Share two instances of the same driver.** Work out how two instances of the same motor driver are
  shared and how that works. → concern **F** *(⚠ edges into Act II — object/image replication)*
- **Take on a new motor type (a requirements change).** A request came in for a *different* kind of
  motor → had to learn a different motor-control approach, then **characterize** that motor. → **G**, **H**
- **Characterize the hardware empirically.** How the 6.5-inch wheels vs. the very-high-rpm motor
  (~40,000 rpm `[?]`; "dokko" motor `[?]` — confirm) behaved under different power systems; characterize
  the different **battery sizes**, how each drove the motor, and the **battery-size limits** — and these
  characterizations *became features of the project*. → concern **H**
- **Add a development observability display.** An **HDMI display** showing live per-wheel motor status
  while developing the code. Had to find a usable HDMI display and usable **font / drawing techniques**
  for putting information on it. → concerns **I**, **J**
- **Produce documentation.** A lot of writing — tool-assisted, but much of it by hand. → concern **K**

**`[?]` to confirm later:** the motor rpm figure (~40,000?); the "dokko" motor name/spelling.
### 2. P2-Click-eInk — ✅ captured
**What it was:** Stephen was genuinely interested in **e-Ink technology**. There's a **Click** module
adaptor for the P2 (`[?]` dictated "Qlik" → almost certainly MikroE **Click / mikroBUS**; confirm) and a
micro-Click e-Ink adaptor module. The vendor sold a couple of e-Ink displays that work with that module;
he picked those up and started implementing how to **drive the e-Ink displays**.

**What I had to do (pre-decomposition):**
- **Locate source / documentation** telling how to talk to the display, then get it running.
- **Bring-up with a logic analyzer.** Inevitably, with new hardware, he routes the display interface
  through a **logic-analyzer adapter** so a logic analyzer can hook to *all* control pins. First question
  worked out: *am I talking to the display correctly, and am I getting output?* — the logic analyzer
  answers it. He has adapters for the Click module that add an **extra row of pins for logic analysis**,
  and has this for **all eval adapters** (logic-analysis boards he can reuse).
- **Scope the features.** Once the adapter + logic analysis work: *what features do I want?* Can I lay down
  **graphics**? **Text**? Handle **rotation** of the device?
- **The traditional closing sequence (done on EVERY project, incl. BLDC):** document the code correctly so
  the driver is **usable** → **post it to the repository** in a usable manner → **announce that it's
  available.**

**What broadened the project over time (display-to-display):**
- Adapt to **different display sizes**; across vendors, adapt to **different control chips**.
- Always **find the new driver documentation** — sometimes **in Chinese**, so **translate Chinese→English**
  before it's usable.
- Vendor **code examples often only partially working**, and **in different languages** — studying them and
  figuring out what to do was time-consuming (but taught a lot).
- Broadened into **color**, **different geometries**, **different vendors** — each a bit of **expense**
  (buying all the pieces and parts).
- **Photograph the devices** being controlled (documentation asset); make the driver **configurable by
  device**; **document how to configure** it at the repo.

**New-this-project concerns (raw, for the later analysis):** find/obtain vendor driver docs & code · logic-
analyzer bring-up & the physical eval/adapter rig · feature scoping (graphics/text/rotation) · the standard
release ritual (document → post to repo → announce) · portability across sizes/vendors/control-chips ·
foreign-language (Chinese) doc translation · digesting partial/multi-language vendor code · cost of parts ·
photographing devices · per-device configurability + its documentation.

**`[?]` to confirm later:** "Qlik" vs **Click/mikroBUS** naming.
### 3. P2-HUB75-Matrix-Driver — ✅ captured
**What it was:** His own interest, and a lot of fun — RGB **LED matrix panels** (HUB75). He loves
controlling rows of things; once he had the panels he could draw anything he wanted on them.

**The electrical / hardware problems he hit first:**
- **Level shifting 3.3 V ↔ 5 V.** He always wants to drive a device at **max speed**, so he had to find
  **level shifters fast enough** for the speeds the different boards could run at.
- **Pin count exceeded hand-wiring.** These need enough pins that it takes **two eval adapters** (more than
  8, fewer than 16 pins) — impossible to hand-wire. So he **designed a custom circuit board** carrying the
  level shifters, **logic-analysis pins**, and HUB75 connectors: connect + power the displays and talk to
  them through **his own HUB adapter** — which **Parallax eventually sold**. *(Custom interface hardware →
  became a product.)*

**Then bring-up and features:** with electrical + logic analyzer working, develop how to talk to the boards.
First display running → **display text**; handle **orientation** (tall / portrait / landscape / upside-down)
→ figure out **rotation**.

**Multi-panel reality (daisy-chaining):**
- Panels **daisy-chain**; he bought more that could, same style/controllers. Learned that **every panel he
  bought had a different controller**, so he started **buying in groups**.
- Had to learn **how the signal daisy-chains**; some panels must be **configured before they work** — send
  a **JTAG-like string down through all panels** to configure the controllers, then drive them.
- **Positional / topology mapping:** where each panel sits on the string, and what that means for **where
  pixels land on the combined display** — reorganize the panels and the "big pixels" move. Ended up building
  a **multi-tiered mapping**: pixel locations → the logical display → the underlying panels.

**The recurring research grind (intensified here):**
- Every new panel set = a **new chip set**. Finding chip driver **datasheets was nearly impossible**; many
  in **Chinese**, only partially described.
- Hunt **code sets** and interpret what they do and how they relate to P2 control; manual searches for more
  sources — sometimes **Arduino**, sometimes **NodeMCU** code, "all over the place."
- **Performance:** none of the reference drivers were as performant as he needed on the P2 — so he was
  always solving *"how do I do what they do, but at high performance?"* **Always chasing the boundaries.**
- Constant **in-head translation C → Python → Spin2**, figuring out how to use P2 resources *while learning*
  them.

**Cataloging / documentation:** catalog each board, catalog the **adapter-board design**, take **pictures**,
and describe the concepts — how to do a panel, how panels are organized *logically* within a display,
rotations of the *display* vs. rotations of the *panels*.

**Status:** ongoing to this day — new panels, large multi-panel displays, multi-panel rotations, best
achievable performance.

**New-this-project concerns (raw, for the later analysis):** electrical interfacing / level-shifting at speed
· pin budget exceeding hand-wiring → forced custom **PCB / adapter design** (that shipped as a product) ·
daisy-chain topology + pre-use controller configuration (JTAG-like) · multi-tier coordinate/pixel mapping
(display↔panels↔controllers) · controller variance across purchases (buy-in-groups) · datasheet hunting ·
multi-source code archaeology + cross-language translation (C/Py/Spin2) · **performance-beating** the
reference drivers · learning P2 resources while using them.
### 4. P2-HUB75-Morphing_Digits — ✅ captured
**What it was:** Completely different in character. He's always interested in *how* he displays things on
the panels. He saw someone on a **YouTube video** animating one digit morphing into another on LED panels
and thought: *I've got this matrix driver — what would it look like to add a morphing display as **objects
that sit above the driver but talk to the underlying driver API**?*

**A key insight he named:** every time he does something like this, it actually **makes the API richer**,
because he has to accommodate something he **didn't anticipate**. *(Layering a new capability on top of your
own driver feeds back and extends the driver's interface.)*

**What I had to do (pre-decomposition):**
- **Research the technique.** Saw the video → saw the concept → web research on how to do it. Learned he
  could use a **transition table**.
- **Code-generate the data.** Write **Python code that generates the transition table**, then hard-code it
  into the morphing-digits object so it knows how to go from any digit to another (2→7, 0→9). *(Tooling /
  codegen as a build step: write code to generate tables, then write code to use the tables to display.)*
- **Animate the segments.** It's a seven-segment display; animate each segment to transition one digit into
  another. Made it **general-purpose** — *any* digit to *any* digit, and digit **sequences**, not just fixed
  digits. Conceptually, "**it's just another font**."
- **Placement / composition.** Place four digits together as a **clock**: define the four digits, place them
  by **top-left position**, with **rotation** per digit. Had to think all of that through.
- **Build a demo.** Do a demo — and **ship the demo on top of the driver, *without* the driver itself** as
  this project. (This project = the morphing-digits object + its demo; it depends on the separate driver.)

**Documentation:** the usual picture aspects, plus **generating a video** so people can see how it runs.

**New-this-project concerns (raw, for the later analysis):** building on/extending your *own* prior work
(objects above an existing driver API) — and the feedback loop where that **enriches the API** · sourcing an
idea from the community (a YouTube demo) · research → **code-generation of data tables** as a build step ·
**generalizing** a feature (any-to-any, sequences) rather than narrow · conceptual reuse ("just another
font") · placement/composition (position + rotation, composing digits into a clock) · shipping a **demo** as
the deliverable (atop but excluding the driver) · **video** as a documentation asset.
### 5. P2-Magnetic-Imaging-Tile — ✅ captured
> **Note:** this is the same machine as the KB's **streaming-pipeline worked derivation** (Act II). The
> Act II example, this Act I project, and the Act III AI story are all *one machine* — a strong through-line.
> **Post-AI project** — one of the **driving proof-of-concepts for the P2KB MCP**; primary Act III material.

**What it was:** He'd always imagined what he'd do with a number of **Hall-effect sensors**. SparkFun
advertised a board — an **8×8 array of Hall-effect sensors** that displays magnetic fields as a color
spectrum across the field's poles (a guy on Linux/Arduino had made a video driving it). His challenge, as
always: *what does that look like on the P2, and how fast can I drive the sensor?*

**Feasibility / system study up front:**
- If I drive the array as fast as I can, **how do I display it?** It has to be video → **HDMI**. Also saw a
  nice **square OLED** → "the P2 is fast — let's do **both displays simultaneously**."
- **Hardware limits, studied first:** how fast can the OLED go? how fast can HDMI? What's *practical*? **60
  fps is more than enough** → draw *both* at 60 fps. Then: what happens with the tile?
- **Asked Claude Code (P2KB MCP proof-of-concept):** "study the sensor board — here's the documentation, the
  schematic, the datasheets for the on-board parts — tell me the **practical limit**, the **frame rate** we
  can read the sensor at." Answer: **~1,300 fps.**

**The reasoning that followed (pre-decomposition thinking):**
- Two displays: capture very fast → **dump into a FIFO** → pull from the FIFO and display. No point pushing
  1,300 fps when you only consume ~60 → **decimation** (mathematical-based decimation?). *(⚠ the FIFO +
  decimation design itself is Act II; what belongs to Act I is recognizing the rate problem and the
  approach.)*
- **Algorithmic discovery (research + Claude Code):** running **frame-to-frame deltas** lets him improve
  from **8×8 to almost 32×32** effective resolution — because so many frames are processed, and with a
  little **handheld-field jitter** you get super-resolution. Became a way to **prototype 32×32 from an 8×8
  sensor**.

**Why it was fun:** high-speed acquisition · fixed-speed output over *different buses* · FIFO management with
decimation between · getting frames to the displays appropriately.

**Pre-AI "what I had to do" (the part that informs *this* Act I chapter):**
- **Find datasheets** for the **Hall-effect sensors**, the **ADC**, and the **OLED** part.
- **HDMI**: *not* a datasheet — **find example code / a driver close enough to adapt** for his use.
- Realized he needed **PSRAM** for the display (**32 MB** on the Edge board) → **find a driver that supported
  it and adapt it**; he didn't know how those worked → **Claude Code helped him understand the driver**.
- As always: **where do I plug in the displays? what wiring?** — common to every project.

**New-this-project concerns (raw, for the later analysis):** up-front **feasibility / hardware-limit study**
(what's the practical frame rate; what's practical vs possible) · deciding on **dual simultaneous outputs** ·
recognizing a **rate mismatch → FIFO + decimation** approach (design ⇒ Act II) · an **algorithmic discovery**
(delta/jitter super-resolution) · discovering a **new resource requirement mid-project** (PSRAM) → find +
adapt its driver · understanding **unfamiliar driver code** · the ever-present **wiring / where-to-plug-in**.
**AI usage (Act III seed):** MCP-assisted datasheet study + feasibility numbers + driver comprehension +
algorithm research.
### 6. P2-Multi-servo — ✅ captured
**What it was:** A **six-axis arm with a gripper** on the end — something he'd always wanted to do. *(Pre-
Claude-Code project.)*

**The honest limit he named:** once he understands how to do a thing in code, he can do anything in code —
but **mathematics is not his forte**, and **inverse kinematics** is not something he can easily do natively.
This project ran into *his own* expertise ceiling. *(Strong Act III mirror: AI lifts this exact ceiling.)*

**What I had to do (pre-decomposition):**
- **Learn to control servos** — how do I *think* in terms of servos; how do I control one; get it working.
- **Reduce pin count.** Six servos are far too many to sit side-by-side on pins → found a **PWM driver
  chip** (cf. Project 8, PCA9685), hooked the servos to it, and talked **from the P2 to the driver chip**.
- **Model the indirection.** How do I talk to a servo *through* the driver chip on the far side of the bus?
  And how do I tell the **servo objects** that they're actually **behind a chip** — that I'm *not* talking to
  the servos directly? — "a real **reshaping** thing." *(⚠ object modeling edges into Act II.)*
- **Coordinate the motion.** When do I open (gripper)? Move which servo where? There's whole-arm rotation,
  multiple joints, the gripper — how do I control *what, when,* and how do I **overlap** motions? Ended up
  hand-building code for **certain specific motions** — which left him a little unhappy, because of the math
  limitation.
- **Characterize the servos.** Position testing and getting **repeatability** with servos to the degree you
  can.

**What the demo could do (then):** get the motors working and demonstrate **pick-something-up and move it**
— that was the extent. A good experiment, but frustrating: he couldn't go as far as he personally wanted.

**Act III contrast (his words):** *today, with Claude Code,* he could build an entire **inverse-kinematics
system** and add a **vision system** — "locate this, go find it," pick it up, place it elsewhere. That's the
system he'd build now; he couldn't then.

**New-this-project concerns (raw, for the later analysis):** running into the **engineer's own skill ceiling**
(math / IK) — a project bounded by personal expertise · pin-count reduction via an **external PWM driver
chip** · modeling **remote objects behind a bus/chip** (⇒ Act II) · **motion coordination / overlap**
(⇒ Act II) · servo **position-test + repeatability** characterization · demo as deliverable. **AI mirror
(strong):** AI raises the expertise ceiling — IK + vision that were out of reach pre-AI.
### 7. P2-OctoSerial — ✅ captured
**What it was:** A performance-and-reliability driver project — the questions he loves: *what performance
can I get out of the P2? how do I make performant code? how do I make communications **error-free at
speed**? how does the P2 help me do **lots** of it?* Technically the P2 can do **~30 channels of full-duplex
serial** (`[?]` confirm figure vs. the "Octo/8" name). Goal: a **very reliable** P2 serial driver.

**What I had to do (pre-decomposition):**
- **Build a verification rig.** Took **two P2s and lashed 16 wires between them**, then worked out serial
  comms with **full round-trip verification**: **checksums** on outbound messages, verification on the
  receiving end, responses/strings sent back and verified.
- **Push the speed.** Above **2 Mbit/s per channel** simultaneously; got close to **3 Mbit** across *all*
  channels at once.
- **Certify it.** Logic-analyzer-based; had to be **certified completely**.
- **Document the techniques as a community example.** Wrote up the techniques: **programming the pins**,
  **circular-buffering** for receive, how he verified all messages, and how he reached extreme speeds
  (>2 Mbit/s error-free). He routinely runs 2 Mbit now; the write-up became a **community example** of how
  to do this on the P2.

**New-this-project concerns (raw, for the later analysis):** **performance as the explicit goal** (push P2
limits) · **reliability / error-free-at-speed** (checksums + round-trip protocol verification) · a **paired-
device test/loopback rig** (two P2s + 16 wires) · **certification** via logic analyzer · producing a
**technique write-up as a community example** (documentation whose *product* is the method).
### 8. P2-PCA9685-Servo-Driver — ✅ captured
**What it was:** Producing a **reusable product** extracted from the **6-DOF arm** effort (Project 6) — the
servo driver, made reusable on its own.

**What I had to do (pre-decomposition):**
- **Re-architect the layering.** With the **PCA9685** chip driving the servos, **rebuild the servo code to
  sit *on top of* the chip** rather than controlling the driver directly. Organize the chip and the servo
  objects so that in the *application* you think you're "talking to servos," but the calls actually
  **cascade through the driver chip**, and the **chip maintains the servo state**. This was **re-engineering**
  all of it. *(⚠ layering/object modeling edges into Act II; the "make it reusable" intent is Act I.)*
- **Datasheets + keep-it-running.** Have the servo-driver **datasheets**; figure out how to keep the chip
  running, keep it **talking to the servos correctly**, and **map** that correctly.
- **Channel mapping / config.** **Record which channel each servo is on** (per-servo configuration).
- **Documentation + reuse shaping.** Documentation, and **shaping the thing into reusable parts**.

**New-this-project concerns (raw, for the later analysis):** **productizing / extracting a reusable
component** from a prior one-off (arm → standalone driver) · **re-architecting to layer over a driver chip
that holds state** (⇒ Act II) · datasheet dependency · **channel mapping / per-device config** · shaping for
**reuse** + its documentation.
### 9. P2-RoboDog — ✅ captured
> **Note:** this is the same machine as the KB's **robot-dog worked derivation** (Act II, control-plane).
> Like the imaging tile, it spans all three acts. **Post-AI project** — strong Act III material. It also
> *composes* other projects on this list: the **Voice-Sensor** (#12) and the **ToF/vision sensor** (#11).

**What it was:** A **robot-dog kit** he'd built a while ago, originally controlled by an **Arduino**. The
challenge: **take the Arduino off and drive it with the P2** — what would that mean? He had **no schematics**,
only **example code**.

**What I had to do (pre-decomposition), AI-assisted (Claude Code):**
- **Reverse-engineer the undocumented system.** Brought down the example code, pointed at the vendor
  website/documentation, and **studied the codebase** — how it was built and wired. **Reverse-engineered the
  communications** for all the sensors and actuators.
- **Postulate the P2 design.** Together with AI, worked out how to make the whole thing work — **decompose it
  onto the P2 and build the layers.** *(⚠ the decomposition is Act II; doing it AI-assisted is Act III.)*
- **Shape the behavior.** Adjusted the **animation layer into a motion-control layer** so the dog moves more
  **naturally / dog-like**, less robot-like.
- **The traditional things, still.** Same effort as porting code (in **multiple languages**) to P2: find the
  **datasheets**, find the **wiring**, hook it up, and **decide the pin layout**.

**AI impact (his words):** AI got it done in **a week or two instead of a month or two** by hand.

**Mechanical / fabrication (aside):** also needed **two rounds of 3D fabrication** — a platform to **bolt the
P2 onto the dog**, and mounting to **bolt on the voice sensor**. *(Recurring physical-build concern; cf. the
ToF fixture in #11.)*

**Cog-allocation insight (⚠ Act II — captured under #12):** the dog's several low-work discrete sensors +
LED actuators were grouped into **one cooperatively-tasked cog**. See Project #12 for the full note.

**Design choices / expansion (pre-decomposition, Act I-relevant):**
- **Choosing narrow-comms peripherals on purpose.** Adding a **voice sensor** to command the dog; replacing
  the **Raspberry Pi camera** with the **vision/ToF sensor** — deliberately choosing devices with **narrow
  communication (I²C / SPI)** over **breadth** (the Pi camera), to stay **embedded-systems-like**, writing a
  driver per new device.
- Likely add **Bluetooth** for phone control. **Expansion is easy**: a few more wires + a driver each adds
  major capability.

**New-this-project concerns (raw, for the later analysis):** **replatforming/porting** off another
controller (Arduino → P2) · **reverse-engineering an undocumented system** from example code + vendor docs ·
reverse-engineering **device communications** · **behavior shaping** (animation → natural motion) · multi-
language → P2 translation · datasheets / wiring / **pin-layout decision** · **peripheral & comms *selection***
(narrow I²C/SPI vs broad) for embedded-friendliness — a core Act I front-end concern · **design for
expandability**. **AI mirror (strong):** reverse-engineering, decomposition, and code all AI-assisted;
**weeks-not-months** productivity.
### 10. P2-RPi-ioT-Gateway — ✅ captured
**What it was:** An **offload-vs-port architecture** project. The P2 is *just* an embedded system — **no
internet, no OS**. So the framing question: if you need OS-level things (web, internet, time, mail), do you
**port all of that onto the P2**, or do you **lash up another device that's already good at it and just talk
to it?** *(A core Act I system-partitioning decision — what runs where.)*

**The design (offload to a companion device):**
- Use a **Raspberry Pi** (good at all those things), connected by **2 Mbit serial** to the P2.
- **Define a communications protocol** over that high-speed link (move + stage data fast).
- **Split responsibilities across the two devices:** file save/load on **P2 flash** *or* on the **Pi
  filesystem**; **web server** on the Pi; a **mail gateway**; **time via NTP** on the Pi → *the P2 suddenly
  knows what time it is*; **web-page controls** fire **commands down to the P2**, and the **P2 sends statuses
  back** for the Pi to display. Web pages end up controlling P2 actuators/LEDs.

**What I had to do (pre-decomposition):** figure out the **protocols**; stand up a **web server** and **web
pages**; **craft all the HTML**; write the **Python communications daemon** (runs as a daemon, does the P2
comms); plus the **P2 code**. Wrote it all up as **examples** — the whole project posted with **screenshots**
(and maybe video) so people could follow the **advanced technique** of offloading work to a more capable
device over high-speed comms.

**Expertise note (contrast):** he came in with **a lot of prior Linux / Raspberry Pi / web-server
knowledge**, so this one was **research-light** — the work was mostly writing the web pages and the Python
daemon. *(Opposite pole from Project 6's expertise ceiling.)*

**New-this-project concerns (raw, for the later analysis):** the **offload-vs-port / system-partitioning**
decision (what the P2 does vs. a companion device) — a core Act I front-end concern · **companion-device
integration** (Pi for OS/internet/web/time/mail) · **defining a host↔P2 protocol** over high-speed serial ·
**cross-device responsibility split** (storage, web, mail, time, command/status) · **full-stack build**
across two devices (HTML + Python daemon + P2 code) · **leveraging existing expertise** (research-light —
contrast to the ceiling projects) · examples + screenshots/video documentation.
### 11. P2-VL53L5CX-tof — ✅ captured
**What it was:** A **time-of-flight sensor** — and *not* a trivial one. Bought it because it looked fun,
then discovered the hard part: **the sensor runs its own uploaded firmware**. What you download is a
**binary image you upload *into* the sensor** — the code the sensor itself runs — and then you communicate
with that on-device code (send/receive data to it). And the vendor libraries were all in **C**.

**What I had to do (pre-decomposition), by hand (pre-AI, weeks and weeks):**
- **Hand-transcribe C/C++ → Spin2** to create an object for the P2 community's use of this ToF sensor.
- **Develop the interface** *and* **develop a loader** — take the **binary images** and send them up to the
  device from the P2, built into the codebase so it can be pushed **P2 → sensor**; then **establish
  communication** to the sensor. All **monitored with logic analysis**. Getting data back the first time was
  the fun payoff.
- **Multi-sensor array idea.** Robots usually **pivot** a distance sensor (or the whole robot) to look
  around. His idea: it's a **45° sensor — combine *four* for 180°, all running simultaneously.** That forced
  an **I²C shared bus**: talk to each sensor **independently**, get them **all scanning**, pull data back
  from **all** of them, **as fast as possible**. *(⚠ four identical sensors on one shared I²C bus = the KB's
  **shared-bus-replication** / addressing problem — Act II.)* Logic analyzer again: tight protocol, robust,
  error-free, handle the data. Proved it all **by hand**.

**Where it stands (incomplete — technical debt):** a year or two on, he realized **some returned data was
mapped to the wrong tables**, and it still needs **math** — applying angle correction to the per-angle
distances to get a **linear measurement across the whole space** — which he hasn't done yet. The vendor has
also **released new codebases**, and the thought of **studying the diffs and reporting on them** is
demotivating.

**Act III realization (his words):** *post-AI,* he can take the **original source, diff the new source,
surgically apply the changes** to augment/add capabilities, pull the new binaries, and get running — **days
instead of weeks** of auditing and understanding. Now he's **encouraged to finish it** (complete the sensor,
add the math + comms).

**Mechanical / fabrication (aside):** the array also needed a **3D-printed part** to hold the four sensors
at their **fixed geometric locations** (the 45°/180° layout depends on it), plus a **common I²C interface
board** wired to the fixture. *(A physical/mechanical build concern — fixturing + a custom interface board —
distinct from the electrical and software work; cf. the HUB75 custom adapter board, Project 3.)*

**Community:** a fun proof of concept; he always **demonstrates the logic-analyzer traces** at the website/
repo so people see how tight the comms are. Users were happy — and noted it was **incomplete** (tables +
math), which he'd love to fix.

**New-this-project concerns (raw, for the later analysis):** a **firmware-loaded device** (sensor runs an
uploaded binary) → **build a loader** + talk to on-device code · heavy **hand-transcription C/C++ → Spin2** ·
**multi-identical-sensor array** design (4×45°→180°) → **shared I²C bus + per-sensor addressing** (⇒ Act II,
shared-bus-replication) · logic-analyzer **protocol certification** · **project incompleteness / math debt**
(wrong tables, missing angle-linearization) · **vendor-update maintenance burden** (diff/study new
codebases) · **mechanical/fabrication** — 3D-printed sensor fixture + a common I²C interface board. **AI
mirror (strong):** **diff-and-surgically-port** vendor updates; days-not-weeks maintenance — the "pick up a
stalled project again" story.
### 12. P2-Voice-Sensor — ✅ captured
> Feeds the **RoboDog** (#9). **Post-AI project.**

**What it was:** Having the dog and wanting to add sensors, he asked: *how can I **command it by voice**?*

**What I had to do (pre-decomposition):**
- **Research & select the device.** Quick web research on what voice devices exist — and here he **used a
  *different* AI agent, Perplexity**, to identify candidates at a **price point he liked ($50–100)**. Found a
  voice sensor with an **I²C / serial interface**, **fully self-contained**, **trainable with new words**,
  and needing **no driver code** — you just **adapt to the integers that come down the line** identifying
  which trained word was recognized. *(Peripheral selection: pick a device that offloads the hard work.)*
- **Prototype communication + hook-up.** Treat it as a hardware block, prototype comms on the P2, hook it up.
  **Post-AI:** downloaded source; **Claude Code read the datasheets**, he figured out where to hook it up,
  and **Claude Code helped write tests** to get it working — a couple of rounds of code changes.
- **Integrate into the existing system.** Decide **how the driver should work inside the dog**.

**Cog-allocation insight (⚠ Act II decomposition — applies to BOTH this project and RoboDog #9):** for the
several **discrete sensors** that each need *very little* work to service (LEDs, the ping sensor + read its
result, the voice sensor), how do you **allocate them to a cog**? He found he could put **three or four such
sensors (including the voice sensor) into one separate cog** and run **cooperative tasking within that cog**
to round-trip them all — keeping every sensor and the LED actuators live and active. *(This is Force 1 ×
Force 3 cooperative-tasking-in-a-cog — Act II material, surfaced here from lived experience.)*

**New-this-project concerns (raw, for the later analysis):** **AI-assisted device/market research** (a
*second* agent, Perplexity) + selection by **price point** · choosing a **self-contained / no-code-needed
device** (interpret its output only) · prototype comms + hook-up · **fitting a new driver into an existing
system** · *(Act II)* **grouping low-work discrete sensors+actuators into one cooperatively-tasked cog**.
**AI mirror:** Perplexity for sourcing; Claude Code for datasheet reading + test authoring.

---

## Act III mirror — parking lot
*(For each spine concern, a note on where AI actually helped — captured opportunistically now so Act III
has raw material later. Not authored here; just don't-lose-it notes.)*

<!-- filled opportunistically -->
