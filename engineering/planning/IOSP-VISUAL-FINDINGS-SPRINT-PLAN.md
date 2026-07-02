# IOSP Visual-Findings Correction — Sprint Plan

**Document:** I/O & Smart Pins User Guide (`manual:p2-io-and-smart-pins-user-guide`)
**Created:** 2026-07-02
**Status:** 🟡 COLLECTING — Stephen is reviewing the current PDF and feeding findings
one at a time (~8–10 expected). We accumulate them here with full detail, then
**chase them all at once** in a single correction pass (batch-and-verify — minimize
Forge round-trips).

## Working rules (apply to every item)

- Edit the **opus-master**, never the workspace render
  (`manuals/p2-io-and-smart-pins-user-guide/opus-master/...`).
- Code examples: `pnut-ts` compile-certified (`-d` if they use `debug()`), and
  ≤ K=76 columns. Code fences (```` ```spin2 ````/```` ```pasm2 ````), prose callouts as `:::`.
- Show the compiler's symbolic constants, not raw arithmetic values.
- After all items are applied: re-prepare → regenerate PDF → verify render, then this
  rolls into the IOSP release (§4 of the release campaign, toward v1.0.0).

---

## Findings

### F1 — Ch. 5 §5.1: add "waiting strategies" examples (typical embedded interaction)

**Location:** Chapter 5 "Working with Smart Pins," §5.1 "The Read/Acknowledge Cycle"
(`part-1-fundamentals/chapter-05-working-with-smart-pins.md`).

**What's there now:** §5.1 shows the **poll-spin** patterns (`PINREAD` / `TESTP` loops)
and a `GETCT()`-based "time-limited wait." It does **not** show the true blocking stall
or the event-based timeout blend — both are standard embedded-interaction patterns worth
adding.

**Add (two examples confirmed useful; a third optional):**

1. **Blocking wait via the event system (`SETSE`/`WAITSE`) — the true stall.**
   Configure a selectable event on the pin's IN-high, then `WAITSE`: the cog *halts*
   (no instruction execution, low power) until the smart pin raises IN — distinct from
   the poll-spin, which burns cycles looping. There are 4 event slots (SE1–SE4). After
   it fires, still `RDPIN` to read + acknowledge (which lowers IN); the event auto-clears
   on the matched `WAITSEn`.
   - Proven pattern already in our ADC chapter (`part-3-input-modes/chapter-16-adc.md:535,538`):
     ```pasm2
     setse1  #%001<<6 + PIN    ' Event on IN high
     waitse1                   ' Cog stalls until the pin is ready
     ```
   - Sources: Silicon Doc `part2-video-output.txt:419` (`WAITSE1..4 — Wait for the
     selectable-event flag`); `part2-interrupts.txt:105` (SEn cleared on matched
     POLLSEn/WAITSEn/JSEn/JNSEn); `part3-end.txt` (IN = the smart pin's "completed" flag).

2. **Wait-with-timeout (pin-ready OR timer) — never hang.**
   There is **no single instruction that blocks on an SE and a CT at once** — each
   `WAITxxx` waits on exactly one event flag. Get the blend by **polling both** and
   branching on whichever fires first:
   - CT timer events: `ADDCT1 target` (set deadline) / `WAITCT1` (stall until reached) /
     `POLLCT1` (poll). Sources: Silicon Doc `part2-video-output.txt:416,471`.
   - Pattern: `POLLSE1` (pin) + `POLLCT1` (timeout) in a loop → "read the pin, but no
     longer than T."
   - Cross-reference the smart pin's **own hardware timeout** as the zero-overhead
     alternative: mode `%10010` with `Y[2]=1` (`P_EVENTS_TICKS`, Ch. 13) raises IN on the
     event **or** after X clocks with no event — the blend done in silicon, so a single
     `WAITSE` covers it. And the **windowed** measurement modes `%10101/%10110/%10111`
     ("for periods in X+ clock cycles") give a fixed-dwell "wait exactly this long, then
     read." Sources: Silicon Doc `part4-smart-pins.txt:704–716, 758`; IOSP
     `appendix-f-mode-reference.md:687–700`.

3. *(optional — decide scope)* **Interrupt-driven servicing.** Route SE1→INT1 so the
   smart pin is serviced in the background while the cog does other work. May belong in
   §5.1 or a dedicated section; confirm before drafting.

**Fix:** add these to §5.1 (or a new "5.1a Waiting Strategies" subsection), each
compile-certified. F1 originated from the Ch. 5 examples discussion on 2026-07-02.

---

### F2 — Quick Mode Selection matrix: table refs not clickable to chapter
The Quick Mode Selection matrix (a table) doesn't let you click a chapter reference to
jump there. **Instance of F4** (cross-ref filter doesn't reach table cells).

### F3 — Front/intro material wrongly nested under the "Copyright and License" heading
All the intro material is bookmarked/headed under the copyright-and-license chapter
heading in the PDF outline — incorrect. Front-matter heading structure bug (heading
level / outline nesting). Fix in `front-matter.md` (and/or how the outline is built).

### F4 — Cross-ref clickability must include TABLES (filter gap)
Every "Chapter N" / "§N.N" reference should be a clickable link. The cross-ref filter
(`p2kb-platform-crossref.lua`) handles body prose but **not references inside table
cells** — so all table-borne refs (e.g. the Quick Mode Selection matrix, F2) are dead.
Fix = extend the filter to walk table-cell inlines. **Shared-platform change** (affects
every manual that adopts the cross-ref filter) — test on IOSP, then it benefits all.

### F5 — Standardize how we show fields-within-a-value (DECISION NEEDED)
The manual currently shows bit/field layouts **three different ways**: (a) the Chapter 4
"Configuration Value Format" positions-above / meaning-below form; (b) a plain text table
(the P_constant architecture table Stephen is questioning); (c) a colored table in
Appendix B. Three forms in one manual is inconsistent. PASM2 Assembly manual uses colored
tables — cross-manual consistency is also in play.
**Question posed:** what's the best pedagogical standard for this doc? Diagram with
colored field-spans vs. text table vs. colored table?
**My recommendation (see chat / to confirm):** standardize on a **colored bit-field
"ruler"** — positions/spans across the top (color-coded), a field-meaning table directly
below (same colors) — i.e. formalize the Chapter 4 form *with color*, and adopt the same
visual language PASM2 uses so the manuals read consistently. Then convert the P_constant
text table and reconcile Appendix B to this one standard. **Confirm the form before the
sweep** (3→1 across the manual = high rework if the form changes).

### F6 — Split hyphenated cover title into Title + Subtitle
Reference example: the Debug Window Manual cover. Break the hyphenated IOSP title into a
title line + subtitle line. Fix in `front-matter.md` cover block (mirror the Debug Window
Manual's front-matter pattern).

### F7 — §9.3 "Configuration Sequence" heading orphaned at page bottom
The §9.3 heading lands at the bottom of a page with its content on the next — a heading
widow. Inspect the outbound `.tex`/`.log`; sweep for **any** heading landing at page
bottom. Fix = keep-heading-with-next-content (`\needspace` / `\nopagebreak` after headings)
in the platform heading definition. **Shared-platform template change.**

### F8 — LaTeX escape artifacts leaking into rendered text
Escapes are leaking into visible text, e.g. a 27-bit accumulator rendering as
`2^{}(27/2)` in a table. **Hunt the entire opus-master** for escape leakage (mangled
superscripts `^{...}`, stray `\_`, `\{`, `\%`, etc. that reach the reader). Fix each at
source (opus-master), and check whether the escape script itself mishandles a construct.

### F9 — FPGA board notes: consolidate into a dedicated appendix (DECISION NEEDED)
FPGA boards are largely out of common use; FPGA caveats are scattered through the text and
distract from the ASIC-P2 mainline. **Question posed:** carry them inline, or move to a
dedicated FPGA appendix?
**My recommendation (to confirm):** gather all FPGA-specific notes into one **"FPGA Board
Differences" appendix**, and where an inline note is load-bearing leave a single short
pointer to it. Do **not** delete (trust chain / info preservation) — relocate. Confirm
before the move (structural).

### F10 — Appendix F: thin the red corner marker's horizontal stroke
Every mode entry in Appendix F carries a red top-left corner mark (vertical + horizontal
strokes). The **horizontal** part is too heavy — reduce to ~1–2 pt. Template/`.sty` tweak
(locate the corner-rule definition; scope to Appendix-F mode heads).

---

## Decisions blocking the batch (need Stephen's nod)
- **F5** — confirm the field-layout standard (recommended: colored bit-field ruler +
  meaning-table, PASM2-consistent) before the 3→1 standardization sweep.
- **F9** — confirm relocating FPGA notes into a dedicated appendix.

## Fix sequencing (batch-and-verify — ONE render at the end)
Mechanical/independent (no decision): F3, F6, F8, F10. Platform filter/template: F4
(+F2), F7. Decision-gated: F5, F9. Apply the whole batch, then a single re-prepare →
regenerate → verify.

## Execution status (2026-07-02)
- **F10 — DONE.** `content.sty` `ModeBlock` top rule `borderline north` 4pt → 1.5pt
  (vertical `west` stays 4pt). Shared-platform file → re-stages on the final prepare.
- **F3 — DONE.** `front-matter.md`: promoted Acknowledgments / How to Use This Guide /
  Document Conventions / Quick Mode Selection Matrix from `##` to `#` (top-level outline
  siblings, no longer nested under Copyright); Trademarks `###`→`##`; their subsections
  `###`→`##`. Headings are unnumbered (chapters carry "Chapter N:" as literal text), so
  no numbering side effect.
- **F8 — DONE.** The escaper turns an *unpaired* `^` into `\^{}` but only protects *paired*
  `^text^`; a lone `2^(27/2)` leaked as `2\^{}(27/2)`. Fence-aware scan found the true
  prose/table leaks (inline-code + `formula` fences render fine → left alone). Fixed to
  pandoc superscripts `2^N^`: Ch.16 SINC2/SINC3 accumulator rows, Appendix C:35/504, and
  the Appendix F `X[3:0]` row.
- **F6 — DONE.** Chapter titles were hyphen-joined (` - `), but the shared `pagination.lua`
  splits only on ` — ` (em-dash) → they never split and wrapped. Converted to em-dash:
  Ch.1/2/3 (were hyphenated) + Ch.7/15/18 (long, no separator). Now render as short title
  + `\chaptersubtitle`, consistent with Debug Window Manual. No filter/template change.
- **F4/F2 — DONE.** Added "Ch" to the crossref filter's Form-A keywords + resolve; rewrote
  all 45 Quick Mode Matrix Chapter/Chapters cells from bare numbers to "Ch N" (filter links
  them → clickable). Escaper-safe (filter builds the link at AST stage, after escaping, so
  no `#` in source). Shared-platform filter + front-matter.
- **F7 — DONE.** Prepended `\needspace` to the section/subsection/subsubsection star-form
  formats (no shape change) so a heading can't widow at page bottom (fixes §9.3).
  Shared-platform (`foundation.sty`).
- **F5 — READY (heavy).** Author one colored bit-field "ruler" macro (positions/colored
  spans above, color-matched meaning-table below; PASM2 palette); convert the Ch.2 P_
  Constant text table + reconcile Appendix B (quick-ref keeps compact colored-table role).
- **F9 — READY (heavy).** New "FPGA Board Differences" appendix; relocate scattered FPGA
  notes there, leave one-line pointers where load-bearing; never delete.

---

## Resolved investigations (recorded so they are not re-chased)

- **MULDIV64 provenance (audited 2026-07-02).** **It is a genuine Spin2 language
  built-in — NOT user-created.** Listed in the Spin2 **v55** language reference
  (`spin2-v55-text.txt:566` — `MULDIV64(mult1,mult2,divisor) : quotient`), used in Chip
  Gracey's own v55 reference example, present in v51, and implemented in the interpreter
  (bytecode `$92 bc_muldiv64`). Ground-truth confirmed: `pnut-ts` compiles it clean.
  Our usage (F-186/188/189 in KB v1.13.2, IOSP Ch. 15/16, P2AN002) is correct — no change.
