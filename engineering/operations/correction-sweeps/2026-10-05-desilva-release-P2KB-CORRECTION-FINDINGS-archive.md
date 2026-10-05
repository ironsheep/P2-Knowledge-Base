# P2KB Correction Findings — ARCHIVE, swept 2026-10-05 (after the deSilva v3.0.9 release)

> **This is an archive of CLOSED findings. It is never re-edited.** Ask "what is
> outstanding?" of `engineering/operations/P2KB-CORRECTION-FINDINGS.md` alone — never
> re-derive completion state from here. If an archived finding must be reopened, it
> returns as a **new** active finding that references this file.
>
> Contains 3 findings carrying a `DONE` status token: F-529 (both halves now released — Assembly v3.1.11
> and deSilva v3.0.9), F-532 (deSilva v3.0.9, tag `p2-pasm-desilva-style-v3.0.9`), and F-276 (shipped
> in deSilva v3.0.7/v3.0.8; its status token was normalised to `DONE` in the release commit so the
> register read it as closed). All verified on the released PDFs. None was the only finding under its
> section heading, so no heading moves.
>
> Swept by rename-then-trim: the register was `git mv`'d here and copied back; this copy was cut to
> the 3 findings, and the live copy had the same text removed with the edit tools. Every line below is
> the pre-sweep text (commit c8da1c38), verbatim; `audit-register-hygiene.py --sweep-check c8da1c38`
> proves it.

---

### F-529 — GETCT 64-bit capture taught without the stale-upper-long erratum (deSilva, Assembly); Assembly also reads the halves in the wrong order — `DONE` (Assembly half released in v3.1.11, 2026-10-05, verified on the PDF: page 214; deSilva half released in v3.0.9, 2026-10-05, verified on the PDF: page 117)
> **Assembly applied** (`instructions-g.md` GETCT): the example reads `GETCT WC` first, then plain `GETCT`
> ("GETCT WC + GETCT gets full CT" — P2 Datasheet :2084, PASM2 Manual; GETCT+WC interrupt-shielding,
> Silicon Doc :2349), plus a Rev C chip with the keeper-cog workaround. Compiled clean (pnut-ts).
> **deSilva applied** (Chapter 12, strategy 1): a Rev C silicon-note chip — in a cog whose group of four had no
> running cog at a wrap, the upper half comes back behind by one per missed wrap until the group's next wrap;
> keep one cog of each group you use running from start-up. Source: `getct.yaml` silicon_errata (EF-068,
> EF-075, EF-080). deSilva already reads WC first. Other errata swept against deSilva: E1 (no SETQ block
> transfer with PTRx), E2 (its ALTD examples follow a completed `##` MOV, no pending AUGS), E7 (every RDFAST is
> the waiting form) — none taught, none added. **Owed:** Assembly `instructions-g.md:110-116` («#385»).
Outside the two changesets (P2 Errata E3, KB since v1.22.0), found while reading them.
- deSilva `COMPLETE-OPUS-MASTER.md:4305-4309` recommends "Capture the full 64-bit count" (`GETCT D WC`)
  for schedulers over "minutes, hours, or days" with no caveat (`pasm2/getct.yaml` silicon_errata).
- Assembly `part-ii/instructions-g.md:110-116`: no erratum note, AND the example reads `getct low_word`
  then `getct high_word wc` — the KB ("GETCT WC followed by GETCT reads the full 64-bit value") and the
  Silicon Doc (GETCT+WC is an interrupt-shielding instruction, :2349) give WC first; low-then-high can tear
  at a wrap.
**Fix:** WC first in Assembly; both state the E3 window and its keeper-cog workaround (or point to P2
Errata E3). Assembly half under «#352».

### F-532 — deSilva: "2/13-20 (hub-exec)" and "REP and SKIP for zero-overhead loops" — `DONE` (low; released in deSilva v3.0.9, 2026-10-05, verified on the PDF: pages 110-112, 117)
> **Applied** (Chapter 12): the loop comment reads "2/13+ (hub-exec)"; the summary bullet reads "REP for
> zero-overhead loops, SKIP for shared code paths".
`COMPLETE-OPUS-MASTER.md:3992` (C3; the same file's :3339 is right) and `:4320` (C12: each skipped
instruction is a 2-clock NOP). **Fix:** "2/13+ (hub-exec)"; "REP for zero-overhead loops, SKIP for
shared code paths".

### F-276 — deSilva Appendix A grounds the P2's value in "missed deadlines," an argument that fails against the reader it is aimed at. — `DONE` (shipped in deSilva v3.0.7, 2026-09-10, and v3.0.8, 2026-09-22; all three sites corrected in opus-master — Appendix A 2026-08-17, the two residual shapes 2026-08-25 «#301»; status flipped 2026-09-28; token normalised 2026-10-05 so the register reads it as closed)

**Location:** `manuals/p2-pasm-desilva-style/opus-master/COMPLETE-OPUS-MASTER.md` — §*"What You Are
Buying With That"* (`:5993-6001`), with the same shape at `:225`, `:6001`, `:6049`.
**RELEASED — and the blast radius grew while this line said otherwise.** Written during Sprint 2,
committed at `fea28f1c`, and **v3.0.6 PUBLISHED 2026-08-17** (166pp). This annotation read
`NOT RELEASED … ships in v3.0.6` until 2026-08-23; it was a *prediction*, correct when written and
false the moment v3.0.6 shipped, and nothing came back to update it. The finding is **still open** —
re-verified against the master 2026-08-23, the shape survives at `:229` (*"Your sensor sampling never
misses a deadline"*) and `:6061` (*"missed timing deadlines"*). `:5995` uses "deadline" in the
project-schedule sense and `:4279` in the counter-wraparound sense — both legitimate, leave them.

The section argues that conventional MCUs turn hard real-time into a scheduling problem with "a long
tail of *why did that deadline slip once an hour?*", and that the P2 therefore "raises your odds of
finishing." Three defects:

1. **It argues against a strawman.** A correctly prioritised Cortex-M meets its deadlines; rate-monotonic
   analysis is fifty years old. An RP2350 PIO state machine meets them absolutely. The reader best
   qualified to judge the appendix concludes we are comparing the P2 against *badly built* alternatives.
2. **It is unfalsifiable and unsourced.** "Raises your odds of finishing" is a project-outcome claim with
   no evidence — a marketing claim in an engineering voice, in a document whose credibility is its
   checkability.
3. **It contradicts a passage two pages earlier.** The RP2350/PIO paragraph added in the same sprint
   (`:5868`) already tells the reader that cheap deterministic offload hardware exists.

It is also a declared **R1** violation under the manual's own `voice-guide.md` (ADOPT, scoped to
technical P2 claims), written the day before the prose was.

**Proposed correction:** replace with the **composability** claim — adding a task to a shared core
perturbs the timing of the tasks already there; giving a task its own cog does not. Take the concept
from the Architect's Guide Ch.7 but **not its vocabulary** (no "forces", no "cadence boundary"): use
cogs, pins and locks, which the reader has earned over sixteen chapters. The section must stand fully
alone for a reader who never opens that book. Sweep the same shape at `:225`, `:6001`, `:6049`;
`:4275` uses "deadline" legitimately (delta-vs-absolute comparison under counter wraparound) — leave it.

> **ALL THREE SITES NOW CORRECTED — the main one was ALREADY DONE and this entry did not know.**
> Re-measured on disk 2026-08-25 («#301»), and split into what was already fixed and what was not:
>
> **§*"What You Are Buying With That"* was rebuilt on 2026-08-17** by `361ac02a` (*"deSilva voice
> pass, part 2: Appendix A rebuilt"*), and it was rebuilt on **exactly the composability argument
> this finding proposed** — *"Put eight jobs on one processor and they are sharing it… Give each job
> its own cog and that simply stops being true — adding the eighth cog does not disturb the first
> seven, because they were never sharing anything to disturb."* It also does the two things the
> finding asked for and did not spell out: it concedes the P2 is *"often neither"* faster nor
> cheaper, and it hands the reader to an ESP32 where an ESP32 is the right answer. No "forces", no
> "cadence boundary". Nothing was owed here and nobody had said so.
>
> **The two residual shapes were real, and are fixed now** (`COMPLETE-OPUS-MASTER.md`, master
> line numbers as found today, not as this entry recorded them):
> - **`:229`** (Ch.1 *"Why P2?"*) read *"Your serial handler never delays your motor control. Your
>   sensor sampling never misses a deadline."* Both halves overreach: a cog can miss a deadline
>   perfectly well if the code in it is too slow. Replaced with the mechanism instead of the
>   promise — the handler *cannot* delay the motor control **because it is not on the same processor
>   to delay it**, and *"add another job later and the ones already running keep the timing they had
>   — they were never sharing anything for the new one to take."* Same claim as the rebuilt Appendix,
>   arriving 5,700 lines earlier, in Chapter 1 vocabulary.
> - **`:6061`** (Summary) read *"Engineers who've fought … missed timing deadlines … find P2
>   refreshing. You spend your time solving your actual problem, not fighting your MCU."* That is
>   defect 2 of this finding verbatim — an unfalsifiable project-outcome claim in an engineering
>   voice. Replaced with reader-recognition that keeps the pedagogy and drops the marketing: *"If you
>   have ever re-tuned a whole interrupt priority table because you added one handler… The work does
>   not disappear — you will still write the driver, and you will still get the timing wrong the
>   first time. What changes is that you stop having to redo it every time the design grows."*
>
> **`:5995` and `:4279` were re-read and deliberately left**, as this entry instructs: the first uses
> "deadline" in the project-schedule sense, the second in the counter-wraparound sense.
> **Gates:** `audit-code-line-length.py --budget 76` and `audit-inline-code-ascii.py` exit 0 on the
> master; no code block touched, so byte-identity is untouched. **Owed to «#302»/release:** the
> master is 166 pp at v3.0.6 and these are body-text reflows — confirm on the page, then release.
