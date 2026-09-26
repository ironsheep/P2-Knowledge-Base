# HDL Clean-Room Study — Intake Analysis (planning level)

**Our document, not part of the delivery.** Written 2026-09-26 by the P2 Knowledge Base project to
record what this material is, how far it can be trusted, and what it would change. The files beside
it are the study's delivery (golden source 0.1.5); this one is ours.

> ⚠️ **STATUS: INDICATORS ONLY — NOT A TRUSTED SOURCE.**
> Nothing in this folder is authority for the P2 Knowledge Base or any manual until the claim in
> question has been **certified** (§4). Until then a claim here tells us *where to look*, never
> *what is true*. Do not cite it, do not copy a value from it, and never use this folder as a
> truth root for a validator.
> — Stephen, 2026-09-26: *"this is not a trusted source until we certify it. It is only indicators."*

**Planning state:** paused by choice, not finished. More planning is owed (§7). This document
exists so that none of the reasoning so far is lost.

**Evidence behind every statement here:** the report-only study
`engineering/analysis/p2-hdl-study-intake-study.md` — findings S-1…S-24, each with `file:line`
evidence on both sides. This document summarises it; where they differ, the study's evidence rules.

---

## 1. What the material is

An independent reader studied the P2's hardware design (its SystemVerilog source) and **nothing
else** — no Parallax documentation, no runs on hardware. Everything it says is derived from the
design alone. That independence is its value: it reaches conclusions our documentary sources could
not have led it to.

- **Which chip:** the **Rev C design** (Stephen, 2026-09-26: *"it read the design for the latest
  RevC chip. There's no question there."*). The delivery itself does not state a revision; that is
  an omission in the hand-off, not an open question.
- **Size:** 16 Markdown files, ≈ 1.26 MB, ≈ 15,800 lines.
- **Its own certainty marking:** body text = stated by the design; closing sections separate
  *what the design does not settle* and *what it implies but does not state*; the limits table
  marks each value stated / implied / not settled.
- **Its classes** (the ones we adopted on 2026-09-25): silicon erratum · anti-pattern · open
  question — see `manuals/p2-errata/CLASSIFICATION-GUIDANCE.md`.

## 2. The kinds of material

| Kind | File(s) | What it is | Best use to us |
|---|---|---|---|
| **Theory of operations** | `P2-THEORY-OF-OPERATIONS.md` (8,336 lines) | The whole chip, facility by facility, and how the parts interact | The *why* behind behaviour we already document; background for authors |
| **Anti-patterns** | `P2-ANTI-PATTERN-QUICKREF.md` (181 rows) | Legal code that does something other than it appears to | Candidates for *P2 Anti-Patterns*; pointers to KB gaps |
| **Limits and ranges** | `P2-BOUNDS-BY-QUANTITY.md` (≈ 445 rows) | Field widths, counters, reset values, saturation — each marked stated / implied / not settled | Cross-checking the numbers in our YAML |
| **Smart-pin mode guide** | `P2-MODE-PROGRAMMING-GUIDE.md` (32 modes) | Per mode: engine, traps, what a mode change carries over | Smart-pin YAML; the I/O & Smart Pins guide |
| **Mechanism reports** | `aspects/` (10 reports) | One smart-pin or pad mechanism each, written for documentation authors | Chapter material for the I/O & Smart Pins guide |
| **Open questions** | closing sections of the above | What the design itself cannot settle | Bench-test ideas; answers we can send back |

**Duplication:** the anti-pattern list *is* the Theory of Operations' §5a register, and the limits
table *is* its §8, re-indexed. A claim found in two of these files is **one source, not two** — never
count it as corroboration.

## 3. What we learned about its reliability

- **Strong where it has been tested.** Every one of its predictions our bench has decided — seven —
  held at the level of the behaviour. Two were facts no Parallax document states; one showed
  Parallax's own published `%TT` table to be wrong (EF-071, now P2 Errata E6).
- **No conflict with Parallax found.** About 110 of its claims were checked against the P2
  Documentation; none contradicted it.
- **Weaker below the behaviour.** Its one miss: it predicted a too-early `RDFAST` read returns stale
  data; silicon returns zero (EF-073). The headline — no stall, no flag — held. *Lesson: trust
  "this happens / this does not happen" more than "and the value you get is …".*
- **Two blind spots by design.** It cannot see **software** (it said `GETRND` repeats after every
  reset; the boot ROM re-seeds it from thermal noise) or **analog behaviour**.
- **It does not know what Parallax already wrote.** About a third of its anti-patterns are
  documented Parallax behaviour; two of its open questions are answered in the P2 Documentation.
- **Roughly a third of its anti-patterns are new to us** — a measured estimate of ≈ 45–70 of 181,
  from a random sample of 30 checked by hand. Earlier keyword searches claimed far more; they could
  not match the study's signal names to Parallax's behaviour names.
- **It adds no errata.** All six rows it marks as errata are already P2 Errata E1–E6.
- **Citations are file-level only** — no line numbers — so a reviewer cannot check a claim against
  the design text. This slows checking; it does not change which chip is described.
- **It is already useful as a lens on our own KB.** Reading it against the YAML exposed a defect
  Parallax's documentation confirms: all eight `reti0–3` / `resi0–3` YAMLs say the flags are
  unaffected, while each is a `CALLD … WCZ` that restores them.

## 4. Trust position — indicators until certified

**Today:** the whole delivery is at **indicator** level — the same footing as community material
(a source of questions, never of figures). This matches the existing rule that nothing from the study
is integrated until proven (CLASSIFICATION-GUIDANCE, 2026-09-25).

**What "certify" would mean** — a working proposal, *not yet decided*. Certification is per claim,
not per document; a claim leaves indicator status by one of these routes:

| Route | When it applies | What certifies it | What the reader is shown |
|---|---|---|---|
| **Parallax-documented** | Parallax states the behaviour (≈ ⅓ of anti-patterns) | the Parallax passage | a citation to Parallax — the study only pointed |
| **Explanation** | Parallax states the *what*; the study supplies the *why* | our own understanding, written in our words at the programmer's level; no value, count or timing taken from the study | an explanation, not a citation |
| **Bench-proven** | new behaviour a programmer would see | an `EF` (our bench) or `XF` (partner bench) run with pre-registered predictions and controls | the bench result |
| **Not certifiable** | cannot be decided from software (analog internals, design intent) | — | never stated as fact; at most "not specified" |

Anything not yet through a route stays an indicator.

## 5. What would make it stronger

1. **Check against Parallax first, by the programmer's name.** The study names signals; Parallax
   names behaviours. A row is only "new" after a search under the mnemonic, mode name and field name
   across the P2 Documentation, the KB YAML and our manuals.
2. **Prove new behaviour on hardware, grouped by engine.** One rig per smart-pin engine or facility
   can decide many rows at once (e.g. one mode-change rig covers a dozen anti-patterns). Jumper-only
   tests run on P0–P7 / P32–P47; instrument tests go to the partner bench or are catalogued.
3. **Take its behaviours, confirm its values.** Its record is strongest at "what happens", weakest at
   the exact value delivered.
4. **Respect its blind spots.** Anything touching the boot ROM, other firmware or analog behaviour
   gets extra scrutiny.
5. **Line-level citations** in future deliveries would let a reviewer check claims quickly.
6. **Close the loop.** Send back what the bench refuted (EF-073) and what Parallax already answers,
   so the next delivery is better. Sending *results* back does not break the clean room, which is
   about what the study *reads*.

## 6. What it would affect — how, and why

### Manuals

| Document | How | Why |
|---|---|---|
| **P2 Anti-Patterns** *(not started)* | Its main source — ≈ 45–70 candidates, each certified before entry | It is the class-2 peer of P2 Errata; this is the class-2 material |
| **I/O & Smart Pins User Guide** | New or deeper sections: what a mode change carries over, pad drive, serial / scope / USB engine behaviour | About half of the material is smart-pin |
| **Assembly Reference** | Flag behaviour, instruction interactions, cog start-up edge cases | The study reads instruction decoding directly |
| **Streamer Programming Guide** | Observing streamer output from a neighbour pin; Goertzel and colour-space details | Mechanism reports and anti-patterns in that area |
| **P2 Errata** | No change from this delivery | Every erratum it names is already a chapter |

### KB YAML

| YAML | How | Why |
|---|---|---|
| `architecture/smart_pins.yaml`, `architecture/smart-pins/*` | What survives a mode change; which modes override OUT; engine edge cases | The largest body of new material |
| `architecture/pin-drive-configuration.yaml` | DAC / ADC / drive-strength interactions | Pad and converter findings |
| `language/pasm2/*` | Flag semantics, instruction interactions (e.g. `ALTR` before `CALLPA`) | Instruction-decode findings; the RETI/RESI flags defect |
| `architecture/interrupts.yaml`, `event_system.yaml`, `debug_interrupt.yaml` | Event arming, dropped (not queued) interrupts, breakpoint re-arming | Interrupt and event mechanism |
| `architecture/cordic.yaml`, `hub.yaml`, `fifo.yaml`, `locks.yaml`, `lookup_ram.yaml`, `boot-rom/*`, `language/pasm2/coginit.yaml` | Edge cases: CORDIC results surviving a cog restart, cog-pair allocation, shared LUT collisions | Hub and cog mechanism |
| `architecture/streamer/*` | Undefined modes, video / DAC routing | Streamer and video findings |
| *possible new files* | the pad cell; the ALU as a whole | Facilities the KB describes only piecemeal |

### Our process documents

| Document | How | Why |
|---|---|---|
| `engineering/ingestion/AUTHORITATIVE-SOURCES.md` | Register the study at indicator tier | So no one treats it as authority by accident |
| `manuals/p2-errata/CLASSIFICATION-GUIDANCE.md` | Add the certification routes, once decided | It already governs the study's classes |
| `hardware-verification/VERIFICATION-OPPORTUNITIES.md` | Queue the bench campaigns | Where bench-proven certification happens |
| `engineering/operations/P2KB-CORRECTION-FINDINGS.md` | Route every KB gap or defect it exposes | All KB corrections go through the register |
| `engineering/document-production/PUBLICATION-ROSTER.md` | Re-scale P2 Anti-Patterns from "tens" to ≈ 45–70 candidates | The planning figure predates this delivery |

## 7. Planning still to do

Not decided yet — recorded so it is not lost:

1. **The certification routes** (§4) — adopt, change or replace.
2. **The intake of the 181 anti-patterns**, row by row, with the §5.1 search method, sorting each
   into a route.
3. **Where the "explanation" route draws its line** — what an author may say from the study without
   a Parallax passage or a bench run.
4. **Bench campaign order** — smart-pin engines first is the natural start; confirm.
5. **The feedback packet to the study**, and whether to ask for line-level citations and the two
   files its reading guide names but the delivery lacks (`P2-ERRATA.md`, `P2-MATERIAL-NEEDED.md`).
6. **When P2 Anti-Patterns is stood up** relative to the certification work.

**Ready whenever wanted (not blocked by planning):** the RETI/RESI flags correction — it rests on
Parallax's documentation, not on the study.
