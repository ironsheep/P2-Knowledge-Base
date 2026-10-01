# Classification guidance — silicon errata vs. behaviour that needs documenting

**What this is.** The classification rule for P2 findings, as written by the HDL clean-room study
agent (from its study charter §12 — the rule its own published errata already follow). Received
2026-09-25 and recorded here **verbatim** below the rule line.

**Stephen's directive (2026-09-25).** This way of thinking — its three classes, its terms, and its
rules — governs **P2 Errata** first and its **peer manual** of undocumented behaviour second, and
propagates forward from those two into the other manuals as material is proven and integrated. The
creation guide and voice guide of each of those manuals adopt it by reference to this file; they do
not restate it.

**How it meets our pipeline.** The clean-room agent classifies from the design material alone — by
design it sees neither Parallax's published documentation nor the bench. **The final classification
is made here**, where all three meet: the study's reading, Parallax's published intent, and a run on
P2 hardware (the `EF` ledger). Two consequences, both deliberate:

- **Published intent counts as design material for us.** A statement in the Silicon Doc can supply
  the written intent that class 1 requires (see RDFAST: the Silicon Doc promises that a blocking
  `RDFAST` leaves the FIFO usable on the next instruction — silicon breaking that promise would be an
  erratum here, whatever the clean-room reading can see).
- **Nothing is integrated unproven.** The guidance below says class 2 gets no test brief — that is
  the study's rule for its own output. On our side, every class-2 item that enters a manual or the KB
  is proven on silicon first, exactly as the errata were.
- **Documented behaviour is not an erratum, however surprising.** Before classifying a new
  prediction, read what Parallax's documentation already says about the instruction. If it states
  the behaviour, the part does what its design says: class 2 at most, never class 1. *Example
  (2026-10-01):* the study's SO109 (a condition-false `BRK` still breaks, showing the previous code)
  is stated in the P2 Documentation's BRK text — documented behaviour, kept out of P2 Errata, and
  measured anyway (EF-085).

## What one erratum is — grouping (Stephen, 2026-10-01: "yes merge and record our reasoning")

**The unit of an erratum is one triggering condition with one workaround** — the one thing a
reader must do differently. Every symptom that condition produces is listed inside that erratum.

**Two observed failures belong to one erratum when measurement shows they share all three:**
1. **the trigger** — the same instruction or state starts them;
2. **the window or conditions** — the same distance, alignment or state bounds them;
3. **the workaround** — one rule prevents both.

**A shared mechanism is supporting evidence only, never the reason to group.** Our manuals cannot
cite the clean-room reading of the design, so a grouping that rests on mechanism alone is a
grouping the reader cannot check. Failures whose triggers or workarounds differ stay separate
errata and cross-reference each other, even when a common cause is suspected.

**Findability by symptom is kept inside the erratum,** not by splitting it: the caution box names
every symptom, and the manual gives a lookup from each symptom to its erratum (a symptom table in
the front matter, or index entries once the manual has an index).

**Numbers are permanent once published.** Before an erratum's first public release its scope
may be reshaped (merged or split); after it, never — later findings that meet the three tests are
added inside the existing erratum, and a new number is used only for a new condition.

**Worked example — E7 and O29 (decided 2026-10-01).** E7 was found on the bench: a blocking
`RDFAST` issued 8 to 15 clocks after a no-wait `RDFAST` skips its wait (EF-073/074). The study's O29
then predicted that a no-wait `RDFAST` releases whatever hub instruction is waiting in that window;
the bench confirmed it for every read and write width, the flags, `PTRA++` and block reads
(EF-084, EF-086, EF-087). The three tests:
- **Trigger:** a no-wait `RDFAST`, in both.
- **Window:** E7 fails at 8–15 clocks and is safe from 16; O29's releases end at 16.
- **Workaround:** E7's own workarounds — 16 clocks to the next `RDFAST`, or a blocking first `RDFAST`
  (EF-077, EF-084) — are the 16-clock rule and the waiting form that prevent every O29 symptom.

So O29 was merged into E7, before E7's first release, as one erratum ("after a no-wait `RDFAST`,
the next hub instruction can complete early") with one rule: start the next hub instruction at
least 16 clocks (7 non-hub instructions) after the no-wait `RDFAST`, or use the waiting form. It had
been planned as a separate E8 for symptom-first lookup; that was reversed once the runs showed one
condition reaching every hub instruction with one fix, and lookup by symptom is served by the
caution box and the symptom lookup. The ledger entries EF-084 … EF-087 and VO-J-021 … VO-J-024, written before
the merge, call it "E8"; read that as this erratum.

---

## The guidance (verbatim)

Silicon errata vs. behaviour that needs documenting: how P2 findings are classified

Every finding describes something the P2 does when a program runs. Each one goes into exactly one of three classes. What decides the class is what the chip's own design material says, not how bad the effect is.

1. Silicon erratum: the part does not do what its own design says it should.
- The delivered design material states an intent in a comment, a table, or a second place in the logic handling the same thing, and the logic breaks that intent.
- The test is strict: there has to be a specific written statement inside the design that the implementation contradicts.
- Errata also include the defects Parallax has published, and any found here that meet the same test.
- Each erratum gets a test brief to prove the defect on P2 hardware, plus a workaround if the design supports one. If none is known, it says so plainly.
- Example: the designer's own notes describe one accumulator as feeding a second, and say both are valid on the same clock. That can't be true, so every burst's last sample shows up in the next burst.

2. Anti-pattern (undocumented or under-documented behaviour): legal code that does something other than what it appears to do.
- The chip does what its design intends, or the design says nothing either way, but a programmer writing the obvious code gets a surprise: a silent no-op, a stale value, an ignored write, or a limit nothing enforces.
- These are documentation findings, not defects. They belong in the programming guide and the anti-pattern reference, never in the errata list.
- They get a clear explanation and the safe way to write the code. They get no test brief.
- This class includes cases where a comment or table in the design material is itself wrong and the rest of the design outvotes it. In those cases the description is wrong, not the chip.
- Example: reading from the fast FIFO right after arming it doesn't stall. The read completes with stale data and nothing flags it. The design never says what should happen, so this is undocumented behaviour, not an erratum.

3. Open question: the delivered material cannot settle it.
- Stated as exactly what is missing and what would settle it. It is not published as an erratum or as a hazard.

Rules for the manual:
- The errata manual lists only class 1. A documentation gap is never listed, titled, counted or labelled as an erratum or an "errata candidate", however much it bites.
- Use the three terms exactly as defined above, each defined once, in one sentence, in one place.
- The list is open-ended. Say "found so far", never "all" or "every".
