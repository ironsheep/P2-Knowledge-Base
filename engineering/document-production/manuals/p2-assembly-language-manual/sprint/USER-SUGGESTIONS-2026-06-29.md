# P2 Assembly Language Reference — User Feedback + Source Research

**Manual:** p2-assembly-language-manual (released v3.1.0, 2026-06-25; this feedback → patch v3.1.1)
**Collected:** 2026-06-29
**Source:** Stephen M Moraco, relaying a community reviewer (with his own framing)
**Scope:** Chapter 1 (The P2 Execution Model) — §1.5 Pipeline / §1.6 Execution Modes
**Status:** 🔬 RESEARCH COMPLETE — recommended dispositions below, awaiting approval before any opus-master edit.

---

## How to read this document

Each comment is captured **faithfully first** (verbatim where given, lightly
structured where described). Then each gets a **Source Research** block —
findings traced to a trusted primary source (Silicon Doc text in
`engineering/ingestion/sources/silicon-doc/p2-documentation.txt`, corroborated
by the published P2KB) — and a **Recommended Disposition**. No opus-master
edit is made until Stephen approves the disposition.

**Primary source for this round:** P2 Silicon Doc, full text at
`engineering/ingestion/sources/silicon-doc/p2-documentation.txt`
(line numbers cited inline). Corroboration: `p2kb-mcp` published KB.

---

## Comments (faithful capture)

### OBS-A — Ch.1 §1.6: the cog-vs-LUT execution distinction "does not exist"
**Category:** Content (architectural accuracy) + Voicing (framing)
**Location:** Chapter 1, §1.6 Execution Modes (table + §1.6.1 / §1.6.2)

Reviewer reports that **the distinction between cog execution and LUT
execution does not exist** — for assembly programs, cog RAM and LUT RAM are
**just continuous memory**. The speed differences that *do* matter are tied to
**the need to refill the streamer cache [FIFO] and the pipeline** — i.e. a
hub-execution phenomenon, not a cog-vs-LUT one. The **REP instruction** should
also be mentioned in this discussion (tight loops without branching delay).

Stephen's instruction: *"Since we made that distinction, we need to source the
reason for our making a distinction, or remove it. We have to figure out which
we need to do."*

### OBS-B — Ch.1 should state: one single DMA channel per cog, called the Streamer
**Category:** Content (addition)
**Location:** Chapter 1 (general — likely near §1.4 hub / a new note)

It should be said in Chapter 1 that there is **one single DMA channel per cog,
called the Streamer**.

### OBS-C — RDLONG/WRLONG inside a REP block is a blocking, interrupt-blocking form of DMA
**Category:** Content (addition)
**Location:** Chapter 1 (or Ch.4 timing / Part II REP entry)

We should note somewhere that **RDLONG / WRLONG, when used with a REP
instruction, is a blocking form of DMA** — and that it is **interrupt-blocking**.

> All three are to be verified against Silicon Doc / trusted ingested sources
> before acting. (This document does that verification.)

---

## Source Research

### Finding A — cog/LUT/hub execution (OBS-A)

**The three-mode terminology is the Silicon Doc's own — it is SOURCED, not
invented.** The Silicon Doc names exactly three execution regions by PC range:

- `p2-documentation.txt:732-734` — **"REGISTER EXECUTION … commonly referred to
  as 'cog execution mode.' There is no special consideration when taking
  branches to a cog register address."** (PC $00000–$001FF)
- `:737-739` — **"LOOKUP EXECUTION … commonly referred to as 'LUT execution
  mode.' There is no special consideration when taking branches to a cog lookup
  address."** (PC $00200–$003FF)
- `:741-746` — **"HUB EXECUTION … the cog employs the FIFO hardware to spool up
  instructions… Branching to a hub address takes a minimum of 13 clock cycles…
  A branch must occur to get from cog to hub, since rolling from $3FF to $400
  will not initiate hub execution."** (PC $00400–$FFFFF)
- `:752-753` — **"It is not possible to execute code from hub addresses $00000
  through $003FF, as the cog will instead read instructions from the cog
  register or lookup RAM."**

**What this means for the reviewer's claim:**

1. **The reviewer is substantively right that cog and LUT execution are
   mechanically identical and contiguous.** Both run at a fixed **2 clocks/
   instruction** with no FIFO involvement; branching between them carries "no
   special consideration" (free); and the *only* boundary the Silicon Doc flags
   as requiring an explicit branch is **$3FF→$400 (LUT→hub)**. It says nothing
   prohibiting a roll from **$1FF→$200 (cog→LUT)** — by that explicit
   asymmetry, cog rolls into LUT seamlessly. To assembly, $000–$3FF is one
   contiguous fast execution space (cog RAM + LUT RAM).
2. **But the distinction is not fabricated** — "cog execution mode" and "LUT
   execution mode" are the Silicon Doc's own labels. So the answer to "source
   it or remove it" is: **it is sourced → keep it, but reframe** so it stops
   implying a meaningful cog↔LUT *switch cost* (there is none).
3. **The real speed boundary is hub execution.** The "refill the streamer cache
   and the pipeline" the reviewer names is the **FIFO instruction spool-up +
   the 5-stage pipeline flush** on a taken branch — a hub-exec cost (≥13 clocks
   per `:743-744`). The FIFO is the same hardware the streamer uses (hence the
   reviewer's loose "streamer cache"); the precise term is **the FIFO**.
4. **REP belongs here.** `:1701` — **"Single or multiple instructions can be
   repeated without branching delays in cog/LUT memory using the REP
   instruction."** REP removes the per-iteration branch (and thus the pipeline
   reload) for tight loops. `:1733` — REP also works in hub memory but "executes
   a hidden jump to get back to the top."

**Note (already partly correct in the manual):** §1.6.2 (opus-master
`chapter-01-execution-model.md:202`) already states "There are no special
considerations when branching between cog and LUT addresses." The fix sharpens
and foregrounds this, rather than introducing a new fact.

### Finding B — the Streamer (OBS-B)

- `p2-documentation.txt:2723-2725` — **"STREAMER. Each cog has a streamer which
  can automatically output timed state sequences to pins and DACs. It can also
  capture pin and ADC readings to hub RAM and perform Goertzel computations…"**
  → **"one streamer per cog" is SOURCED and correct.** The streamer is the
  cog's autonomous (background) data-movement engine between pins/DACs and hub.

- ⚠️ **"DMA" is NOT Silicon-Doc vocabulary** — but it **is** established house
  style in the Streamer Programming Guide. A full-text search of the Silicon
  Doc returns **zero** occurrences of "DMA" / "direct memory access"; the
  *concept* (autonomous data movement without per-element CPU instructions) is
  exactly what the streamer does. **The Streamer Programming Guide already sets
  the house register for this** (`p2-streamer-programming-guide/opus-master/
  streamer-body.md:17`): a call-out block —
  > *"**If you've used DMA before:** the streamer is a close cousin of a DMA
  > channel, with two important additions. First, it has that built-in
  > metronome, so it does paced transfers at an exact sample rate rather than
  > 'as fast as the bus allows.' Second, it reshapes data as it moves… If you
  > have never met DMA, don't worry: everything below stands on its own."*

  — i.e. **DMA as an opt-in analogy, anchored to the word "streamer," inclusive
  of readers who've never met DMA.** It also grounds one-per-cog the same way
  we need (`:11`, `:15`: "Every cog on the P2 has its own streamer" / "each cog
  has its own streamer and its own NCO"). **Decision: adopt that exact register
  in the Assembly manual** so the two manuals make the same comparison.

- ⚠️ **"single DMA channel per cog" needs one caveat.** The streamer shares the
  cog's **FIFO** with hub-execution instruction prefetch and with
  `RDFAST`/`WRFAST` streaming (`:748-751` — while in hub-exec "the FIFO cannot
  be used for anything else," and the streamer FIFO instructions XINIT/XZERO/
  XCONT are among those locked out). So "the streamer is the cog's one
  streaming/DMA engine" is accurate; "single DMA *channel*" is fine if we note
  it rides the shared FIFO.

### Finding C — RDLONG/WRLONG in a REP block (OBS-C)

The **interrupt-blocking** half of the claim is **solidly sourced**:

- `p2-documentation.txt:1734` — **"Any branch within the repeating instruction
  block will cancel REP activity. Interrupts will be ignored during REP
  looping."**
- `:2538` — a REP block **"is automatically shielded from interrupts, including
  non-stallable debug interrupts."**
- Published KB (`p2kbPasm2Rep`) corroborates: constraints list **"Interrupts
  stalled during execution"** and **"Branches within block cancel REP
  immediately."**

So a `REP { RDLONG/WRLONG … }` copy/transfer loop runs **atomically** — the
whole block is uninterruptible — at the cost of **interrupt latency** for its
duration. That is a genuine, citable gotcha worth stating.

- ⚠️ **"DMA" is imprecise here, and arguably backwards.** A REP+RDLONG/WRLONG
  loop is **CPU-driven**: the cog executes each transfer and **blocks** on each
  hub-access window — the opposite of autonomous DMA. The actual DMA-like fast
  paths on P2 are (a) the **streamer** (autonomous) and (b) **`SETQ`/`SETQ2` +
  RDLONG/WRLONG burst block moves** (already documented in §1.4.3 — one long/
  clock after alignment, amortizing the hub window). Recommend we describe
  OBS-C as an **interrupt-atomic block transfer**, and *contrast* it with the
  streamer/SETQ-burst rather than calling the REP loop "DMA."
- **This contrast lines up exactly with the Streamer guide's framing.** That
  guide's whole point about the streamer is that it does *paced, autonomous*
  transfer ("runs without the cog's help," `streamer-body.md:11`). The honest
  Assembly-manual sentence therefore writes itself in the same register: the
  streamer is the cog's autonomous DMA-cousin; a `REP{RDLONG/WRLONG}` block move
  is its **blocking, cog-driven counterpart** — and, because REP shields the
  block, **interrupt-atomic**. Same comparison, opposite pole.

---

## Recommended Dispositions

| # | Comment | Verdict | Recommended action |
|---|---------|---------|--------------------|
| **A** | cog-vs-LUT distinction | **KEEP (sourced) + REFRAME + add REP** | §1.6: present cog+LUT as one contiguous fast execution space ($000–$3FF, fixed 2-clock, free cog↔LUT branching, PC rolls $1FF→$200; only $3FF→$400 needs a branch). State the *real* speed boundary is hub-exec (FIFO spool-up + ≥13-clock branch / pipeline refill). Add REP as the way to loop in cog/LUT "without branching delays." Cite Silicon Doc. |
| **B** | streamer = 1 DMA/cog | **ADD (sourced) — "DMA" label RESOLVED** | Add a Ch.1 sentence: each cog has its own **streamer**, its autonomous engine for moving data between pins/DACs and hub (detailed in Ch.4 / the Streamer guide). Use the **Streamer guide's house register** — "a close cousin of a DMA channel," opt-in (`If you've used DMA before…`), anchored to "streamer," inclusive of DMA-newcomers. Note it rides the shared FIFO. |
| **C** | RDLONG/WRLONG+REP = blocking DMA, interrupt-blocking | **ADD the interrupt-atomic fact; reframe "DMA" as the blocking counterpart** | Add a note (Part II REP entry and/or Ch.1/Ch.4): a REP block is shielded from interrupts (incl. non-stallable debug), so a `REP{RDLONG/WRLONG}` block transfer is **interrupt-atomic** — uninterruptible for its duration, raising interrupt latency. Frame it as the **blocking, cog-driven counterpart** to the streamer's autonomous transfer (same comparison as the Streamer guide, opposite pole); also cross-reference `SETQ`-burst. Don't call the REP loop itself "DMA." |

### The headline answer to Stephen's question (OBS-A)
**We sourced it — do not remove it.** The cog/LUT/hub three-mode framing is the
Silicon Doc's own terminology. The reviewer's catch is real but narrower than
"the distinction doesn't exist": cog and LUT execution are *identical and
contiguous* (no switch cost), so the framing must be **reworded** to stop
implying a meaningful cog↔LUT boundary, foreground the **hub-exec FIFO +
pipeline** cost as the actual distinction, and bring in **REP**.

### Cross-cutting note — "DMA" terminology: RESOLVED via the Streamer guide
Both OBS-B and OBS-C lean on "DMA," a word the **Silicon Doc never uses** — so
the question was which house register to adopt. **Resolved: match the Streamer
Programming Guide**, which already frames the streamer as *"a close cousin of a
DMA channel"* in an opt-in call-out anchored to the word "streamer"
(`streamer-body.md:17`). The Assembly manual will make the **same** comparison
(consistent cross-manual terminology), and OBS-C naturally extends it as the
blocking/cog-driven *opposite pole* of that same analogy. No remaining open
decision on the DMA wording.

### Downstream (no action yet)
- No P2KB YAML change is implied by these three items — they are manual-text
  (Ch.1) corrections/additions grounded in already-ingested Silicon Doc facts.
  If the "DMA" terminology decision affects how the streamer is *defined*
  elsewhere, that would be a separate findability pass, not a correction.
