# P2 App-Note Roster & Production Plan

> **Status:** v1 (2026-06-30), *Capability Coverage & App-Note Roster* sprint,
> Phase 6 (task #138) — the sprint's payoff. Built from the coverage matrix
> (`p2-capability-coverage-matrix.md`), the placement rubric
> (`engineering/standards/documentation-standards/artifact-placement-rubric.md`),
> and the capability spine (`engineering/standards/p2-capability-taxonomy.md`).
> Inputs: P1 mapping (`p1-app-note-spine-mapping.md`), manual coverage
> (`p2-manual-coverage-by-domain.md`), the Quick Bytes catalog
> (`deliverables/ai/P2/community/quick-bytes/`), and the re-scraped OBEX catalog.

---

## 1. The organizing principle — what becomes an app note (and what doesn't)

Two discriminators decide placement; together they explain the whole roster.

- **Architecture *concept* vs. language *feature/technique*.** How to *structure*
  a system (decomposition, inter-cog communication seams, coordination) is an
  **architecture concept** → the **Architect's Guide** + the decomposition YAML
  layer. A specific **language feature or applied technique** that needs
  how-to-use guidance (TASK\*, STRUCT, stack-sizing, CORDIC application) → an
  **app note**, because the Architect's Guide is a *method* book and the Spin2
  Reference Manual is parked.
  - *Refinement — a single topic can split across the line.* "Inter-cog
    communication" is both: the **contract decision** (which structure, why) is
    architecture → the Guide; the **concrete data-structure implementation** (the
    worked FIFO/queue/deque code) is technique → an app note (C2). Cut by
    *concept vs. implementation*, not by topic name.
- **Reference-exists → app note, not a guide.** A full **programming guide**
  (Streamer, XBYTE) is warranted only when the *reference itself* needs
  assembling **and** the usage is a large methodology. Where the reference
  already exists (e.g. CORDIC: the QROTATE/QVECTOR/… ops are in the 503pp PASM2
  manual + `cordic.yaml` + Spin2 operators) and only the *applied* layer is
  missing, an **app note** is the right form. Guides are *earned*, not presumed.

App notes are the **narrow, worked, task-specific** layer (the P2AN001 shape) —
deliberately what the Architect's Guide refuses to give (its load-bearing
anti-prescription rule: teach the method, never the recipe). They **complement**
the manuals and the Guide; they never compete.

## 2. The production methodology — boundary-determination by example-mining

Every roster item is produced by the **P2AN001 playbook** (proven on the ADC
foundation sprint): **locate + download source examples (OBEX / Quick Bytes /
external) → study them → delineate** what is *foundational* (belongs in the
owning manual) from what is *advanced technique* (becomes the app note). The
examples are what make the boundary objective rather than guessed.

This front-end **forks into two pipelines** (see §6):
- **Document-enrichment pipeline** — foundational content enriches the owning
  manual (IOSP, XBYTE, Streamer, Spin2 ref…).
- **App-note pipeline** — the advanced technique becomes an app note (doc + YAML
  companion, per the four-artifact model).

The same mining can feed *manual enrichment with no app note at all* (e.g.
bolster the **XBYTE manual** with working XBYTE examples — the guide already
exists, so there's no app note, only enrichment).

---

## 3. The roster — three families + a standalone + the exemplar

Each item: rank, the *belongs-here-because*, the example sources to mine, the
owning-manual boundary, and status.

### Exemplar (shipped) — **P2AN001: Single-Pin ADC Instrumentation** · v1.0.1 (released 2026-07-03)
The proof of the model: advanced ADC technique → app note; foundational ADC →
IOSP Ch.16. Every item below follows its shape.

### Family A — Smart-Pin Instrumentation
*Owning manual: I/O & Smart Pins User Guide (IOSP). Boundary: basic modes → IOSP; advanced worked instruments → app note.*

| # | App note | Belongs-here-because | Examples to mine | Status |
|---|---|---|---|---|
| A0 | **ADC Instrumentation** | *(done — P2AN001)* | 6 OBEX (SAR/ADS1118/hi-res/4-20mA) + 3 QB | ✅ v1.0.1 |
| A1 | **DAC & Analog Signal Generation** → **P2AN003** | the *output* sibling to ADC; advanced DAC (dithering, audio streaming, waveform synth) is worked technique, not reference | QB "ADC→DAC + Analog Frequency to DAC"; sound-engine | ✅ **released v1.0.0 2026-07-03** (5 recipes + reSound ceiling) |
| A2 | **Frequency / Rotation / RC-Timing Measurement** → **P2AN004** | the timing-instrumentation region (freq, period, duty, rctime, count) — many modes, non-obvious, recurring (tachometer, freq counter, ToF) | QB TSL235R (freq); OBEX P2_rctime (pulse); quadrature | ✅ **v1.0.0 released 2026-07-03** (3 recipes; rendered circuit/timing diagrams) |

### Family B — Math (worked technique; reference already in PASM2/Spin2)
*Owning manuals: PASM2 / Spin2 reference (building blocks already there). Author as a coordinated pair/trio.*

| # | App note | Belongs-here-because | Examples to mine | Status |
|---|---|---|---|---|
| B1 | **CORDIC for Real Work** ⭐ **LEAD** | P2-unique solver; reference assembled but *applied* guidance (rotation, distance+heading, scale, transcendentals) taught nowhere | `cordic.yaml`; QB Goertzel; OBEX CORDIC/FFT libs | ✅ **released v1.0.0 (P2AN002, 2026-07-03)** |
| B2 | **Extended-Precision Integer Math** | building blocks (carry-chain ADDX/SUBX, `muldiv64`) in the manual; composed 64/96/128-bit technique only in community | **OBEX 5189** (64/96/128-bit); float objects 2812/4047 | candidate |
| B3 | **Fixed-Point Math on the P2** | fractional math with no FPU — recurring, P2-specific technique, no guided home | DSP/filter examples; CORDIC fixed-point formats | candidate |

> **CORDIC guide-promotion trigger:** start B1 as an app note. *If* the
> pipelining-for-throughput / streamer-interaction material proves to need
> systematic depth that bloats the note, split it or promote the **Math family**
> into a single "P2 Math Programming Guide." Let the content decide — do **not**
> pre-build a guide (the reference already exists; a guide would mostly
> re-present it).

### Family C — Concurrency & New Language Features
*Owning manual: Spin2 Reference Manual (parked) → so app notes are the guided home. All `{Spin2_v47}`-era features with reference-only coverage.*

| # | App note | Belongs-here-because | Examples to mine | Status |
|---|---|---|---|---|
| C1 | **Cooperative Multitasking with Spin2 TASK Methods** | new `{Spin2_v47}` TASK\* family (intra-cog cooperative tasks); reference-only, no guided pattern; P1 AN014 (Coroutines) successor | TASK\* method YAMLs; v55 ingestion examples | **→ P2AN005, RELEASED v1.0.0 (2026-07-07)** |
| C2 | **Data Structures with the New Language Facilities** *(in-cog **and** cross-cog)* | unifies STRUCT (in-cog queues/lists) **and** the worked *implementation* of cross-cog FIFOs/queues/deques (hub-shared, STRUCT-based, with indexing+locking); P1 AN003 successor. **Implementation layer only** — the *contract decision* (which structure, why) stays with the Architect's Guide. More coherent than STRUCT-alone. | language-map STRUCT; **PNut minimalistic data-handling idioms**; `data-flow-contracts.yaml` patterns; v55 examples | **→ P2AN007, **RELEASED v1.0.0 (2026-07-13, 16pp)** (single note, not split); extended beyond the original scope with R5 member bitfields ({Spin2_v54}) + R6 OFFSETOF ({Spin2_v53}) — the only reader-facing P2 doc covering either; all cross-cog claims hardware-confirmed (EF-036…EF-040) |
| C3 | **Sizing Cog & Task Stacks** | `TASKSPIN` requires a sized stack per task; the stack-check mechanism makes "size it right" a *worked* recipe; P1 AN019 successor; **companion to C1** | TASKSPIN stack examples; isp_stack_check utility | **→ P2AN006, RELEASED v1.0.0 (2026-07-07)** (separate companion note to C1, not folded) |

### Standalone — **USB Device/Host with P2 Smart Pins**
*Genuinely hard; under-documented; high value. Examples already exist — no hunting.*
- **Belongs-here-because:** the smart-pin USB-mode mechanics → IOSP; the hard
  *composition* of a working device/host → app note.
- **Examples to mine (in hand):** OBEX **USBnew**, **USB HID Driver**.
- **Status:** candidate (high value, hard). **Its example-mining front-end runs early**
  as the **IOSP Release Campaign's USB study (Input 1)** — those findings enrich IOSP's
  USB smart-pin content now; the standalone note stays a candidate.

---

## 4. Disposition ledger — what routes elsewhere (and why)

The discipline that makes the roster credible: most matrix gaps are **not** app
notes.

| Gap / topic | Routes to | Why |
|---|---|---|
| Multicore decomposition, inter-cog **communication styles** *(the contract decision — which structure, why)*, coordination | **Architect's Guide** + decomposition YAML layer | architecture *concept*; `data-flow-contracts.yaml` already names the comm styles (latest-wins mailbox, ring buffer, req/resp+ack, lock-free) with a worked mailbox. **NB:** the *implementation* of cross-cog FIFOs/queues/deques (the worked STRUCT code) is **not** here — it goes to **app note C2** (the concept/implementation split) |
| Streamer applications | **Streamer Programming Guide** | guide exists |
| Emulation / VM building | **XBYTE Programming Guide** (in dev) | guide exists; bolster it with mined XBYTE examples |
| Mixed-voltage interface (AN010) | **IOSP** electrical appendix | hardware reference, not guided composition |
| Pin conditioning / filtering / PWM-NCO | **IOSP enrichment** (mostly) | foundational; PWM/NCO also community-saturated |
| FAT filesystem (AN006), sensors, motors, audio, displays, protocols (E/F/G/H/J) | **OBEX** (community parts) | richly served; incl. Stephen's 4261/5404/5405; one OBEX-adoption nudge: DS1302 (2816, archiver import) |
| GUI window-manager series (AN004/005/013) | community / optional QB suggestion | ambitious, display community-saturated |
| Hardware-design assets (KiCAD/PCB/3D) | **excluded** | non-capability resources (per the taxonomy) |

*We commit only to what **we** produce. QB suggestions to Parallax are noted, not
committed work.*

---

## 5. The plan — sequence toward the outcomes

1. **B1 CORDIC** — the lead. (The Architect's Guide is expected to ship before
   the second app note, so the conceptual layer lands first; CORDIC's applied
   layer follows cleanly.) Run the §2 playbook: mine CORDIC examples → delineate
   PASM2/`cordic.yaml` reference vs. applied → author the app note (+ YAML
   companion); watch the guide-promotion trigger.
2. **Family A (A1 DAC → P2AN003, A2 measurement → P2AN004)** — **committed +
   stood up 2026-06-30 as Inputs 2 & 3 of the IOSP Release Campaign**
   (`engineering/planning/IOSP-RELEASE-CAMPAIGN-SPRINT-PLAN.md`).
   Each runs the §2 playbook, delineates against IOSP, **augments IOSP with its
   foundational fork**, and is taken to PDF. The campaign's **USB study** (Input 1)
   also mines the Standalone USB note's examples to enrich IOSP (the note itself stays
   a candidate). IOSP releases LAST, after all three forks land.
3. **Family C (C1 multitasking, C2 STRUCT, C3 stacks)** — the new-feature notes;
   C1+C3 authored together.
4. **B2/B3 (extended-precision, fixed-point)** — complete the Math family;
   consider the guide-promotion decision once B1+B2+B3 scope is known.
5. **USB** — when there's appetite for the hard one; examples are ready.

Each item also emits **document-enrichment** work on its owning manual (the
foundational fork) — tracked alongside the app note (§6). Schema for the
app-note **YAML companion** is designed in the first authoring pass (pilot:
P2AN001), per `APP-NOTE-DESIGN-DECISIONS.md`.

---

## 6. Tracking model — two pipelines, one front-end

```
            ┌─ BOUNDARY-DETERMINATION PASS (per region) ─┐
 candidate →│  locate+download examples → study →        │
            │  delineate foundational ⟂ advanced         │
            └───────────────┬───────────────┬────────────┘
                            │               │
        foundational fork ──┘               └── advanced fork
                 │                                   │
   ┌─────────────▼──────────────┐      ┌─────────────▼──────────────┐
   │  DOCUMENT-ENRICHMENT pipe   │      │     APP-NOTE pipe          │
   │  enrich owning manual       │      │  author app note           │
   │  (IOSP / XBYTE / Streamer / │      │  (doc + YAML companion,    │
   │   Spin2 ref) + KB/YAML       │      │   four-artifact model)     │
   └─────────────────────────────┘      └────────────────────────────┘
```

**Per-item states:** `candidate → examples-located → boundary-delineated →
[enrichment: pending|done] + [app-note: pending|drafting|authored|released]`.

**This roster doc is the register** for that backlog. The two pipelines map onto
existing heads: the **app-note pipeline** is a document-production element
(recognized in the head-dispatch model, #131); the **document-enrichment
pipeline** is manual revision (prepare/finalize/release skills). The shared
front-end — *processing external community code to determine documentation
boundaries* — is a **new standing activity** distinct from KB-fact ingestion;
candidate for its own lightweight skill/process once it has run a few times
(logged as a future-process candidate).

> **Next actions:** (1) **B1 CORDIC** ✅ released v1.0.0 (P2AN002, 2026-07-03) (#140, separate Math
> track). (2) The **IOSP Release Campaign** (`engineering/planning/IOSP-RELEASE-CAMPAIGN-SPRINT-PLAN.md`)
> drives **A1→P2AN003 (DAC)** and **A2→P2AN004 (Freq/Rotation/RC-Timing)** through the §2
> playbook + IOSP enrichment + PDF, plus a USB study, then releases IOSP. Remaining
> items are registered candidates above.
