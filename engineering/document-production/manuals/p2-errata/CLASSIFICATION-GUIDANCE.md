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
real silicon (the `EF` ledger). Two consequences, both deliberate:

- **Published intent counts as design material for us.** A statement in the Silicon Doc can supply
  the written intent that class 1 requires (see RDFAST: the Silicon Doc promises that a blocking
  `RDFAST` leaves the FIFO usable on the next instruction — silicon breaking that promise would be an
  erratum here, whatever the clean-room reading can see).
- **Nothing is integrated unproven.** The guidance below says class 2 gets no test brief — that is
  the study's rule for its own output. On our side, every class-2 item that enters a manual or the KB
  is proven on silicon first, exactly as the errata were.

---

## The guidance (verbatim)

Silicon errata vs. behaviour that needs documenting: how P2 findings are classified

Every finding describes something the P2 does when a program runs. Each one goes into exactly one of three classes. What decides the class is what the chip's own design material says, not how bad the effect is.

1. Silicon erratum: the part does not do what its own design says it should.
- The delivered design material states an intent in a comment, a table, or a second place in the logic handling the same thing, and the logic breaks that intent.
- The test is strict: there has to be a specific written statement inside the design that the implementation contradicts.
- Errata also include the defects Parallax has published, and any found here that meet the same test.
- Each erratum gets a test brief to prove the defect on a real part, plus a workaround if the design supports one. If none is known, it says so plainly.
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
