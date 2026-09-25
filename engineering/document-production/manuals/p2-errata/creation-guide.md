# P2 Errata — Creation Guide

How this manual is built, what it may say, and how every sentence in it is proven.
Read this, `voice-guide.md` and `CLASSIFICATION-GUIDANCE.md` before writing a line.

---

## 1. Document identity

| | |
|---|---|
| **Title** | P2 Errata (working title) |
| **Subtitle** | Silicon Defects of the Propeller 2 Found So Far, Proven on Real Parts |
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
  intent and a run on real silicon meet. Published intent (the Silicon Doc) counts as design
  material.
- **Proven on silicon before it enters.** An item whose bench run has not decided it is not a
  chapter. (At v0.1.0: `RDFAST`/`WRFAST` readiness and the Goertzel SINC2 iteration count are
  waiting on their runs and are not in the book.)

## 3. Structure

- **Front matter:** cover (shared `book-artwork.png`), contents, copyright and licence,
  acknowledgments, sources, *What counts as an erratum* (the three classes defined once),
  *How each chapter is built*, the **summary table** of every erratum found so far, and
  document conventions.
- **Chapter N is erratum EN.** Erratum numbers are **permanent**: a new erratum is appended as
  the next chapter, never inserted, and a number is never reused. Heading form:
  `# Chapter N: <plain reader title>` (colon, no em-dash; the pagination filter treats an
  em-dash after the number as a subtitle splitter).
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

## 4. The chapter, section by section

Every erratum chapter has the same sections, in this order, with these headings:

1. **Opening paragraph** (no heading): the defect in two or three sentences a reader can act on.
2. `## What the design says`: the written statement the part contradicts, and where it is
   written. For a vendor-published erratum, the published statement. **Quote Parallax
   documentation exactly.** Never quote design source code (see §6).
3. `## What the part does`: the defect, stated precisely: which instructions, in what
   arrangement, with what result.
4. `## The symptom`: the defect as it shows up in a program, including what does
   **not** go wrong (e.g. "the data lands correctly; only the pointer is wrong").
5. `## The workaround`: the fix, with a short code example, and whether the workaround was
   itself proven on silicon. If no workaround is known, say so plainly.
6. `## Why it happens`: the theory of operation, **in our own words** (§6).
7. `## How it was proven`: the test on real silicon: what it arranges, its controls, what it
   measured, and the numbers. Stated so a reader could rebuild the test.
8. `## The test program`: a walkthrough of the rig with short excerpts, and the filename in
   the examples archive.
9. `## Status`: the status table (§5).

## 5. The status table

Every chapter ends with the same two-column table:

| Field | Content |
|---|---|
| Erratum | E*n* |
| Published by Parallax | Yes, with where (e.g. *P2 Documentation, KNOWN BUGS*) · or No |
| Found by | Parallax · or a prediction from the clean-room design study, confirmed here |
| Confirmed on silicon | Yes, with the date and the conditions (board, clock) |
| Workaround proven on silicon | Yes · No · None known |
| Affects | the instructions and conditions, briefly |
| Test program | the filename in the examples archive |

**No internal identifiers in reader text:** no `EF-NNN`, `VO-*`, `O17`, `SO80`, `F-NNN`,
brief names or ledger names. The chip revision is stated once, in the front matter, once it
is confirmed.

## 6. Sources, authority, and what may not be quoted

| Source | Path | Use |
|---|---|---|
| **The bench ledger** (strongest) | `engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md` (EF-066..070) | every claim about what the part does, every number |
| **Raw logs** | `manuals/p2-errata/audit/verification-tests/logs/` | the numbers, read from the lines themselves |
| **The rigs** | `manuals/p2-errata/audit/verification-tests/*.spin2`, replicated to `hardware-verification/campaigns/2026-09-p2-errata-predictions/tests/` | walkthrough excerpts, verbatim |
| **Parallax P2 Documentation** | `engineering/ingestion/sources/silicon-doc/p2-documentation.txt` (KNOWN BUGS at 197–227) | *What the design says*; quote exactly |
| **KB YAML** | `deliverables/ai/P2/language/pasm2/*.yaml`, read from disk | instruction semantics and encodings |
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
  `pnut-ts` **1.55.8** (`/home/vscode/.local/pnut/pnut-ts-linux-arm64-015508/pnut_ts/pnut-ts`,
  add `-d` if it carries `debug()`), and the harness is kept beside the sidecar. (Since
  2026-09-23 `/usr/local/bin/pnut-ts` is 1.55.8; confirm with `pnut-ts --version`.)
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
