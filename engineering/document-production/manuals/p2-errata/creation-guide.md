# P2 Errata — Creation Guide

How this manual is built, what it may say, and how every sentence in it is proven.
Read this, `voice-guide.md` and `CLASSIFICATION-GUIDANCE.md` before writing a line.

---

## 1. Document identity

| | |
|---|---|
| **Title** | P2 Errata (working title) |
| **Subtitle** | Silicon Defects of the Propeller 2 Found So Far, Proven on P2 Hardware |
| **Slug** | `p2-errata` |
| **Doc class** | reference |
| **Reader** | a P2 programmer who needs to know where the chip does not do what its design says, what that looks like in a program, and how to write around it |
| **Peer** | P2 Anti-Patterns (working title), which carries class 2. This manual never does. |

## 2. What goes in: classification

The classification rule is `CLASSIFICATION-GUIDANCE.md`, adopted **by reference**. It is not
restated here or anywhere else in this folder. Three consequences govern authoring:

- **Class 1 only.** A documentation gap is never listed, titled, counted or labelled as an
  erratum, however much it bites. There is **no** "behaviours mistaken for errata" section.
  The front matter defines the three classes, once, and points to the peer manual.
- **Final classification is made here**, where the clean-room reading, Parallax's published
  intent and a run on P2 hardware meet. Published intent (the Silicon Doc) counts as design
  material.
- **Proven on silicon before it enters.** An item whose bench run has not decided it is not a
  chapter. (At v0.2.0 the second bench session decided three more items: the DAC-mode ADC
  enable is E6; a blocking `RDFAST` that follows a still-arming no-wait `RDFAST` is E7; the
  Goertzel SINC2 iteration-count corruption is documented behaviour (the P2 Documentation's note
  on Goertzel SINC2 mode), so it is not an erratum; E5 names it only as a scope limit of its
  SINC1 fix. The no-wait `RDFAST` readiness boundary — a FIFO read too soon after a no-wait
  `RDFAST` alone — is class 2 and goes to P2 Anti-Patterns; E7 says it is a different case.
  On 2026-10-01 E7 was widened, before its first public release, to the whole condition: after
  a no-wait `RDFAST`, the next hub instruction (read, write, block read, or a waiting `RDFAST`)
  can complete early — `CLASSIFICATION-GUIDANCE.md`, *What one erratum is*.)

## 3. Structure

- **Front matter:** cover (shared `book-artwork.png`), contents, copyright and licence,
  acknowledgments, sources, *What counts as an erratum* (the three classes defined once),
  *How each chapter is built*, the **summary table** of every erratum found so far, and
  document conventions.
- **Chapter N is erratum EN.** Erratum numbers are **permanent once published**: a new erratum is
  appended as the next chapter, never inserted, and a number is never reused. What one erratum
  covers — one trigger with one workaround, every symptom inside it — and when two findings
  merge is decided by `CLASSIFICATION-GUIDANCE.md`, *What one erratum is*; an erratum's scope may
  be reshaped only before its first public release (E7 absorbed the planned E8 that way,
  2026-10-01). Heading form:
  `# Erratum EN: <plain reader title> {#ch-eN}` (colon, no em-dash). The platform pagination
  filter recognises `Erratum EN` as a chapter heading: it starts the page, and sets the chapter
  counter to N and its label to `EN`, so figures number `EN.1`. The heading text is what the
  TOC and running heads print, so both read *Erratum EN*. A cross-reference is written
  *Erratum EN*, never *Chapter N*.
- **Appendix A: The Test Programs**: every rig in the examples archive, what it proves, and
  how to run it.

Current numbering (decided 2026-09-25):

| E | Chapter file | Subject |
|---|---|---|
| E1 | `e1-setq-block-pointer-step.md` | `SETQ`/`SETQ2` block transfer: an intervening `ALTx`/`AUGS`/`AUGD` cancels the block-size `PTRx` step |
| E2 | `e2-altx-takes-pending-augs.md` | an `ALTx` with an immediate `#S` between `AUGS` and its target takes the augment, and does not cancel it |
| E3 | `e3-getct-stale-upper-long.md` | `GETCT WC` returns a stale upper long in a cog group that missed a wrap |
| E4 | `e4-getxacc-clear-gating.md` | `GETXACC` clears the Goertzel accumulators only during a Goertzel burst |
| E5 | `e5-goertzel-one-clock-lag.md` | the Goertzel accumulators trail their term by one active clock |
| E6 | `e6-dac-mode-adc-enable.md` | in a DAC smart-pin mode, `OUT` does not switch the ADC while `TT` bit 0 is clear |
| E7 | `e7-rdfast-blocking-after-no-wait.md` | after a no-wait `RDFAST`, the next hub instruction can complete early: hub reads return the previous read's data, hub writes are lost, block reads go wrong, a waiting `RDFAST` skips its wait (file name kept from the first-found case) |

## 4. The chapter, section by section

Every erratum chapter has the same parts, in this order, with these headings. The reader
decides from the first screen whether the erratum touches their program and what to change;
everything below *A proven workaround* is the evidence. Voice by section: `voice-guide.md` §2a.
Terminology (Stephen, 2026-09-26): the reader's change is a **workaround**, never a *fix* (a
fix is a silicon revision), and the manual offers **a** proven workaround, never *the* only one.

1. **CAUTION box** (no heading), the first thing under the chapter heading, in the platform's
   existing amber box, unchanged:

   ```
   ::: caution
   **Expected:** what the P2 Documentation says happens, in one sentence.

   **Actual:** what the part does instead, in one sentence.

   **Workaround:** the condition any workaround must meet, in one sentence, pointing to
   *A proven workaround*.
   :::
   ```

2. **Opening paragraph** (no heading): who is affected and when, in two or three sentences. It
   follows the box and does not restate it.
3. `## What the P2 is documented to do`: the written statement the part contradicts, and
   **whose** it is and where (*the P2 Documentation, section …*). For a vendor-published
   erratum, the published statement. **Quote Parallax documentation exactly.** Never quote
   design source code (see §6).
4. `## What the P2 does`: the defect, stated precisely: which instructions, in what
   arrangement, with what result.
5. `## What your program sees`: the defect as it shows up in a program, including what does
   **not** go wrong (e.g. "the data lands correctly; only the pointer is wrong").
6. `## A proven workaround`: **rule-first.** Open with the condition any workaround must
   meet (**What any workaround must do:** …), then **One way, proven on P2 hardware:** and the
   drop-in code block, byte-identical to the block a test program ran on silicon, then one
   sentence of guarantee naming its kind: *one-time startup workaround*, *rule at each use*,
   or *helper routine*. Then, where they exist, other ways that meet the same condition; then
   its cost and its limits. Only a block proven on a part is printed as the proven
   workaround; if none is proven, say so plainly and name any change given as unproven.
7. `## Why it happens`: the theory of operation, **in our own words** (§6).
8. `## How it was proven on P2 hardware`: the test on P2 hardware: what it arranges, its
   controls, what it measured, and the numbers. Stated so a reader could rebuild the test. The
   run that proved the workaround is reported here too.
9. `## The test program`: a walkthrough of the rig with short excerpts, and the filename in
   the examples archive (and the workaround's test program, if separate).
10. `## Status`: the status table (§5).

Section anchors: `{#sec-eN-documented}`, `{#sec-eN-actual}`, `{#sec-eN-sees}`,
`{#sec-eN-workaround}`, `{#sec-eN-why}`, `{#sec-eN-proof}`, `{#sec-eN-program}`,
`{#sec-eN-status}`.

## 5. The status table

Every chapter ends with the same two-column table:

| Field | Content |
|---|---|
| Erratum | E*n* |
| Published by Parallax | Yes, with where (e.g. *P2 Documentation, KNOWN BUGS*) · or No |
| Found by | Parallax · a prediction from the clean-room design study, confirmed here · or found on the bench here |
| Confirmed on silicon | Yes, with the date and the conditions (board, clock) |
| Workaround proven on silicon | Yes, with the date and its kind (one-time startup workaround / rule at each use / helper routine) · No · None known |
| Affects | the instructions and conditions, briefly |
| Test program | the filename(s) in the examples archive: the erratum's, and the workaround's if separate |

**No internal identifiers in reader text:** no `EF-NNN`, `VO-*`, `O17`, `SO80`, `F-NNN`,
brief names or ledger names. The chip revision is stated once, in the front matter, once it
is confirmed.

## 6. Sources, authority, and what may not be quoted

| Source | Path | Use |
|---|---|---|
| **The bench ledger** (strongest) | `engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md` (EF-066..087, the P2 errata entries, including the workaround runs) | every claim about what the part does, every number |
| **Raw logs** | `manuals/p2-errata/audit/verification-tests/logs/` | the numbers, read from the lines themselves |
| **The rigs** | `manuals/p2-errata/audit/verification-tests/*.spin2`, replicated to `hardware-verification/campaigns/2026-09-p2-errata-predictions/tests/` | walkthrough excerpts, verbatim |
| **Parallax P2 Documentation** | `engineering/ingestion/sources/silicon-doc/p2-documentation.txt` (v35; KNOWN BUGS at 197–227) and `silicon-doc-text.txt` (the current online edition) | *What the P2 is documented to do*; quote exactly |
| **Parallax Spin2 Language Documentation** | `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt` (v55) | *What the P2 is documented to do* where the statement is Spin2's (E3: `GETMS()`/`GETSEC()` at :552–553, the description column only — the `\|` and `GETMS ()` spacing are the table's); quote exactly, checked against the `.docx` |
| **KB YAML** | `deliverables/ai/P2/language/pasm2/*.yaml`, read from disk | authoring aid for instruction semantics and encodings; **never cited in reader text** |

**What reader text may cite (Stephen, 2026-09-26).** An erratum is the hardware contradicting a
written statement of intent, so the statement must be Parallax's own: **only official Parallax P2
documentation is cited** — the P2 Documentation (any official edition, named as such) and
Parallax's other published P2 documents. **Never cited**: our own manuals, the P2 Knowledge Base,
community-review drafts, forum threads, or the comment threads attached to a Parallax document
(a comment is discussion, not documentation). Our bench runs are the *evidence*, stated as such,
never the *statement of intent*.
| **Study briefs** | `manuals/p2-errata/code-validation/test-briefs/` (**git-ignored, Internal**) | the mechanism, for *Why it happens* only, **paraphrased** |

**The clean-room study's design material is never quoted.** No HDL fragments, no signal or
module names taken from it, no line references. *Why it happens* explains the mechanism in our
own words, at the level of the programmer's model. The study is credited by name in the
front matter. (Its formal name is **open**: Stephen settles it with Chip Gracey.)

**Where the KB disagrees with the bench, the bench wins**, and the disagreement goes to
`engineering/operations/P2KB-CORRECTION-FINDINGS.md`. At v0.1.0 the KB has not yet absorbed
E3–E5 (F-462..466): the manual cites the silicon, not the KB, for those.

## 7. Verification protocol (write-time)

Hallucinations happen at the moment of writing. Before a sentence goes into a chapter:

- Every **number** is read off the raw log line or the ledger entry, not recalled.
- Every **quotation** of Parallax documentation is copied from the source file, and its line
  is recorded in the chapter's verification sidecar (below).
- Every **code excerpt** from a rig is a contiguous run of lines copied verbatim, and its
  file and line range are recorded in the sidecar.
- Every **workaround snippet** not taken verbatim from a rig is compiled inside a harness with
  `pnut-ts` **1.55.8** (`/usr/local/bin/pnut-ts`; confirm with `pnut-ts --version`; add `-d`
  if it carries `debug()`), and the harness is kept beside the sidecar. **The proven
  workaround block is not a harness snippet:** it is byte-identical to the marked block inside the workaround's test
  program, which ran on silicon; the sidecar records both line ranges.
- Red-flag words (*also provides*, *automatically*, *eliminates*, *synchronizes*, *enables*)
  are either sourced or cut.

Each chapter has a sidecar `verification/eN-sources.md` mapping every number, quotation
and excerpt to its source file and line. The sidecar is how an audit re-checks the chapter; a
chapter without one is not finished. `verification/` is **tracked**, deliberately outside
`audit/` (which the repo git-ignores as transient working history): the sidecars and their
compile harnesses are the manual's standing proof trail, not working files.

## 8. Code

- Fences are ` ```pasm2 ` or ` ```spin2 `, never raw LaTeX code environments.
- Inline code is ASCII only (no ellipsis character, no Unicode minus, no smart quotes).
- Instructions in prose are uppercase in backticks (`SETQ`); registers as in the KB (`PTRA`).

## Code Line Budget

**Max code columns (K): 76**

Inherited from the platform reference budget. A code line longer than K is an authorship
defect: shorten the comment or split the line legally. Never let a code box wrap.

## 9. Production

1. Edit `opus-master/*.md` (canonical).
2. `prepare-manual`: assemble (`workspace/p2-errata/assemble-manual.sh`), gates
   (`validate-manual-release.py --slug p2-errata --phase prepare`), escape, stage changed files
   to `outbound/p2-errata/`.
3. Stephen deploys to the Forge's manual store and builds.
4. Before any public release: Parallax review of the whole manual (Stephen), and the study's
   formal credit name settled.
