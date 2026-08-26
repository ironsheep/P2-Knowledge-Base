# silicon-doc — reviewer-comment harvest (pass 6, leg 3)

**Source:** `word/comments.xml` of `Parallax Propeller 2 Documentation v35 - Rev B_C Silicon.docx`
**Harvested:** 2026-08-26 · **27 comments**, each paired to its anchor via the
`commentRangeStart`/`commentRangeEnd` ids in `word/document.xml`.

## Why this document's comments are unusual

Most harvested review threads are community feedback. **This one contains the designer.**
Chip Gracey answers in the `KNOWN SILICON BUGS` thread, which changes the tier of what is said
there: a community claim Chip affirms stops being a community claim. Everything *else* here stays
an upstream lead — credible, never citable, and never promoted to a published number.

**Two forum URLs appear in the comments (ids 8 and 12). Neither was fetched** — this project does
not probe `forums.parallax.com`. Those leads are recorded by description only.

## Routed

| Comment | Author | Anchor | Routed to |
|---|---|---|---|
| **[0]–[4]** | Wuerfel21 + **Chip Gracey** | `KNOWN SILICON BUGS` | **E-015** (section omits the RDFAST corruption bug, designer-confirmed) + **Q-009** (mechanism — only Chip can close) |
| **[21]**, [22] | Bart Grantham | the `S/#/PTRx` operand list | **E-012** — list omits RDLUT/WRLUT, contradicted by the document's own encoding table |
| **[15]**, [16] | Christof Eberspaecher | *"In every mode… three %ppp bits"* | **E-013** — false by the document's own four-pin-block text |
| **[25]** | Nicolas Benezan | the boot *"steps"* | **E-014** (microSD boot omitted) + **G-026** (the selecting pin condition is NOT established) |
| **[24]** | Anonymous | *"IN is raised"* | **G-023** — trigger polarity, A-low vs A-high; bench-testable |
| **[12]** | Wuerfel21 | SETS/SETD/SETR pipeline delay | **G-024** — one-NOP dual-port hazard; forum thread NOT fetched |
| **[11]** | rayslogic | `BITC 0,bitindex` | **G-025** — claimed break for bitindex > 31 since ADDPINS |

## Recorded, not routed

Each of these is real feedback that does not produce a register entry — listed so the absence is
visible rather than silent.

| Comment | Author | Why not routed |
|---|---|---|
| [6] | Bart Grantham | *"Was there more to this sentence after this comma?"* — editorial; anchored to a bare `,`. A genuine copy defect, too small to carry a register ID. |
| [7] | Ethan Childerhose | *"I agree"* — a reply, no claim. |
| [9] | Raymond Allen | Explains `%`, `x`, `{wc}` notation — correct, and already covered by the document's own field legend (`silicon-doc-text.txt:180-190`). |
| [10] | Jacob Jones | *"Add tab between index,' and #table"* — a whitespace/typography note on an example. **Worth noting for us specifically:** the DOCX extraction preserves those tabs, so our capture is not affected. |
| [13] | Raymond Allen | *"the regular behavior of `_RET_` with regular instructions is not described here anywhere"* — a documentation-completeness complaint about the source. Plausible, but establishing *"described nowhere"* requires reading the whole document for a negative, which was not done in this pass. **Deliberately not filed as an erratum on an unverified negative.** |
| [14] | Christof Eberspaecher | `rdfast #0,#bytecodes ?!` — questions an operand form in an example; the extracted `cell-02.txt` shows `rdfast #0,bytecodes`. Needs a `pnut-ts` probe to settle, not done here. |
| [17], [19], [20] | Nicolas Benezan | Clarity complaints about nibble-swap ordering and long-alignment wording. Editorial; no factual claim to test. |
| [5] | Anonymous | Distinguishes *field* from *operand* — a terminology observation, correct and non-controversial. |
| [8] | Wuerfel21 | Forum link about hubexec below `$400`. **URL not fetched.** No claim stated in the comment itself. |
| [18] | Anonymous | *"fix this"* — no content. |
| [23] | rayslogic | *"Think this requires that X.[15..0] is set to 1… This whole section needs more explaining"* — hedged (*"think"*), and the author does not state what the correct behaviour is. Not actionable as written. |
| [26] | **Stephen Moraco** | Proposes documenting the checksum responses (`'.'` valid, `'!'` failed, code not loaded/run). A content-addition request to Parallax rather than a defect in what is written. |

## Discipline applied

- **Designer vs community.** Chip Gracey's *"Yes"* is what makes E-015 an erratum rather than a
  gap. Wuerfel21's original report, alone, would have been an upstream lead.
- **No negative asserted without reading for it.** [13] claims something is described *nowhere*;
  that is a whole-document negative and was not verified, so it is not filed.
- **No forum figure promoted.** Two threads referenced, neither fetched, nothing quantitative taken.
- **Every comment accounted for.** 7 routed, 20 recorded-not-routed, 27 total.
